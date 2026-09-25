#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pemeriksa kelengkapan Kebijakan Privasi terhadap unsur pokok UU 27/2022 (UU PDP).

Hanya memakai library standar Python 3. Lintas OS.

Pemakaian:
    python3 cek_kebijakan.py kebijakan.md                # laporan teks
    python3 cek_kebijakan.py kebijakan.txt --format json # untuk diproses agent
    python3 cek_kebijakan.py --daftar                    # tampilkan daftar unsur yang diperiksa
    (Windows: ganti python3 dengan python atau py)

Kode keluar: 0 = pemeriksaan berjalan (apa pun skornya), 2 = input tidak bisa dibaca.
Dengan --ketat: 1 bila status bukan "CUKUP LENGKAP".

Ini pemeriksa BANTU berbasis kata kunci + polaritas kalimat (ID & EN), bukan penilaian hukum.
Kata kunci yang ditemukan belum tentu berarti isinya benar/memadai.

Cara kerja singkat (v1.0.2):
1. Teks dibersihkan: tag HTML & komentar dibuang, entitas (&nbsp;) diurai, markup markdown dihapus.
   Nomor baris tetap mengikuti file asli.
2. Teks dipecah menjadi kalimat dan klausa (batas: . ! ? baris baru ; : "tetapi/namun/but/however",
   serta koma yang diikuti subjek baru seperti ", kami" / ", we").
3. Frasa berisiko: kecocokan diabaikan bila ada kata penyangkal (tidak, tak, bukan, belum, never,
   not, don't, ...) di klausa yang sama sebelum kecocokan ATAU di dalam kecocokan
   ("Data Anda tidak akan dijual" = aman). Pola yang memang berisi penyangkal
   ("tidak bertanggung jawab atas kebocoran") tidak memakai cek ini.
4. Unsur hanya dihitung terpenuhi oleh kalimat berpolaritas POSITIF: jumlah penyangkal
   (termasuk "tanpa/without") di klausa itu harus genap. "Kami tidak akan memberi tahu bila bocor"
   = negatif (tidak dihitung); "tidak akan mengubah ... tanpa pemberitahuan" = positif (negasi ganda).
5. Isian kosong ([isi: ...], [fill: ...], {JIKA ...}) menurunkan skor: unsur yang buktinya hanya ada
   di kalimat berisian kosong (atau hanya di judul) dihitung setengah (status BELUM DIISI), skor dibatasi
   maks. 84 selama masih ada isian. "skor_struktur" = skor bila semua diisi. Urutan status: lihat URUTAN_STATUS
   (KURANG LENGKAP mengalahkan BELUM SIAP bila strukturnya pun < 60).
6. (v1.0.2) Satu temuan per kalimat: bila beberapa pola cocok di kalimat yang sama, dipakai tingkat tertinggi dan
   alasannya digabung ("cocok_lain"). Klausa setelah "tetapi/namun/kecuali/except" dinilai tersendiri, sehingga
   "tidak menjual data, tetapi dapat membagikannya ke mitra iklan" tetap ditandai. Idiom "bukan tidak mungkin"
   dibaca sebagai "mungkin". Semua unsur di JSON memakai kunci yang sama.
7. (v1.0.3) Script ini PEMERIKSA KEDUA, bukan penyaring risiko. Pada uji buta independen, pola kata kunci hanya
   menangkap sekitar 4 dari 10 kalimat berisiko yang ditulis dengan kata-kata lain (parafrasa/eufemisme). Karena itu,
   bila tidak ada pola yang cocok, keluaran menyatakan dengan jujur bahwa itu BUKAN jaminan aman dan merujuk ke
   pembacaan manual per kategori (references/kategori-risiko-cek.md). Pola "kepada pihak mana pun" kini memeriksa
   penyangkal di seluruh klausa ("Kami tidak menjual ... kepada pihak mana pun" = patuh).
"""
import argparse
import bisect
import html
import json
import os
import re
import sys
import unicodedata

VERSI = "1.0.3"
BATAS_BYTE = 5 * 1024 * 1024        # file > 5 MB ditolak dengan pesan ramah
MAKS_TEMUAN_PER_POLA = 20
MAKS_TEMUAN_TOTAL = 60
BATAS_BLOK = "\x1e"                  # pengganti tag HTML tingkat blok (batas kalimat, tanpa menambah baris)

# ---------------------------------------------------------------------------
# Kosakata bersama
# ---------------------------------------------------------------------------
V_JUAL_ID = r"(?:menjual|memperjualbelikan|menyewakan|memperdagangkan|menukar(?:kan)?|memonetisasi|mengomersialkan|mengkomersialkan)"
V_JUAL_EN = r"(?:sell|rent|lease|trade|monetize|monetise)"
SAMBUNG = r"(?:,| dan/atau| dan| atau| maupun| serta| and/or| and| or| &)+"
OBJEK_ID = r"(?:data|informasi|database|basis data|kontak|daftar pelanggan)"
OBJEK_EN = r"(?:data|information|info|details|database|(?:customer|user|member|contact|mailing|email) (?:lists?|records|profiles|contacts))"
NEGARA = (r"\b(?:singapura|singapore|amerika( serikat)?|united states|\busa\b|u\.s\.(?:a\.)?|eropa|europe|uni eropa|jepang|japan|malaysia|"
          r"australia|irlandia|ireland|india|hong ?kong|tiongkok|china|korea|taiwan|jerman|germany|belanda|netherlands|"
          r"inggris|united kingdom|finlandia|finland|swedia|sweden|kanada|canada|brasil|brazil)\b")
V_BAGI_ID = (r"(?:(?:mem|di)?bagikan|berbagi|(?:mem|di)?berikan|(?:meng|di)?ungkapkan|(?:meny|dis|s)erahkan|(?:men|di)?teruskan|"
             r"(?:meng|di)?alihkan|(?:meng|di)?kirimkan|(?:men|di)?transfer(?:kan)?|(?:mem|di)?pindahtangankan|(?:men|di)?tawarkan|"
             r"(?:meny|dis|s)ediakan|(?:mem|di)?pasok(?:kan)?|menyalurkan|(?:di)?salurkan)(?:nya)?")
V_BAGI_EN = (r"(?:share[sd]?|sharing|disclose[sd]?|disclosing|provide[sd]?|providing|transfer(?:s|red|ring)?|give|given|giving|"
             r"sell|sold|rent(?:ed)?|lease[sd]?|licen[sc]e[sd]?|made available|make (?:it |them )?available)")
IKLAN_ID = r"(?:iklan|periklanan|pemasaran|promosi|marketing|kampanye|penawaran|calon (?:pelanggan|pembeli|nasabah)|prospek|leads?)"
# tujuan pemberian: "untuk keperluan promosi", "sebagai bagian dari program pemasaran", "dalam rangka kampanye iklan"
TUJUAN_IKLAN_ID = (r"(?:untuk|demi|bagi|guna|sebagai|sebagai bagian dari|dalam rangka)(?: (?:keperluan|tujuan|kepentingan|program|kegiatan|materi|bahan))*"
                   r" " + IKLAN_ID)
# kalimat harus menyebut data/informasi orang (agar "memberikan diskon kepada pelanggan untuk promosi" tidak ditandai)
OBJEK_ORANG = (r"\b(?:data|informasi|info|nomor|kontak|email|e-mail|alamat|profil|riwayat|identitas|ktp|database|daftar|nama|foto|lokasi)\b|"
               r"\b[a-z]+nya\b|\b(?:information|details|contacts?|lists?|profiles?|records|personal|your|history|location|usage)\b|\b(?:it|them)\b")
# penerima yang jelas-jelas untuk iklan/pemasaran
SASARAN_IKLAN_ID = (r"(?:(?:mitra|rekanan|partner|agen(?:si)?|jaringan|platform|perusahaan|pihak)(?: [a-z]+){0,2} " + IKLAN_ID + r"|pengiklan|"
                    r"(?:pihak ketiga|pihak lain|mitra|rekanan|afiliasi|partner)[^.;\n]{0,40}?(?:untuk|demi|bagi) (?:keperluan |tujuan |kepentingan )?"
                    + IKLAN_ID + r")")
SASARAN_IKLAN_EN = (r"(?:advertisers|advertising (?:partners|networks?|companies|agencies)|ad (?:networks?|partners|tech)|"
                    r"marketing (?:partners|companies|agencies|affiliates)|marketers|data brokers|"
                    r"(?:third[- ]part(?:y|ies)|partners|affiliates|others)[^.;\n]{0,40}?for (?:their (?:own )?)?(?:targeted )?(?:direct )?"
                    r"(?:marketing|advertising|promotional)(?: purposes)?)")
PERLU_IKLAN = r"iklan|pemasaran|promosi|marketing|kampanye|penawaran|calon|prospek|\blead|advertis|marketer|broker|\bad (?:networks?|partners|tech)"
PERSETUJUAN = r"persetujuan|setuju|menyetujui|consent|opt-?in|opt in|memilih ikut"
DURASI = r"\d+\]?\s*(?:hari|minggu|bulan|tahun|days?|weeks?|months?|years?)\b"
BERITAHU_ID = (r"(?:beri ?tahu|memberi ?tahu|memberitahu(?:kan)?|pemberitahuan|umumkan|mengumumkan|informasikan|"
               r"menginformasikan|mengabari|mengabarkan|melaporkan|laporkan|menghubungi)")
BERITAHU_EN = r"(?:notify|notification|inform|announce|notice|let you know)"

# ---------------------------------------------------------------------------
# Unsur wajib/pokok. Tiap unsur: id, label, bobot, pola (regex, huruf kecil), dasar, saran.
# ---------------------------------------------------------------------------
UNSUR = [
    {
        "id": "identitas",
        "label": "Identitas pengendali data (nama usaha/pemilik)",
        "bobot": 1,
        "pola": [r"pengendali data", r"data controller",
                 r"(kebijakan|pemberitahuan)( privasi)?( ini)? (berlaku|dibuat|diterbitkan) (untuk|bagi|oleh) "
                 r"(?!(semua|seluruh|setiap|para|pengguna|pelanggan|pengunjung|anda|siapa|kami)\b)(?![^.;\n]{0,60}\bkami\b)",
                 r"(policy|notice) (applies to|is issued by)",
                 r"(dikelola|dioperasikan|dimiliki) oleh", r"(operated|owned|managed|run) by", r"\bkami adalah\b", r"\bwe are\b",
                 r"\b(usaha|toko|bisnis|klinik|perusahaan|praktik|salon|situs|website|aplikasi)( [a-z0-9&'-]+){0,3} milik\b",
                 r"\bmilik (ibu|bapak|pak|bu|sdr|saudara|dr|drg)\b", r"yang (mengelola|mengoperasikan|memiliki) (situs|website|aplikasi|toko|akun|layanan)",
                 r"adalah (usaha|toko|perusahaan|badan usaha|klinik|praktik)",
                 r"\b(klinik|toko|usaha|praktik|apotek|salon|kursus|yayasan|cv|pt|ud)\b[^.\n]{2,40}\b(memakai|menggunakan|memproses|mengumpulkan|mencatat) data",
                 r"\b(pt|cv|ud)\.? [a-z]", r"nama usaha", r"tentang kami", r"about us"],
        "dasar": "UU 27/2022 Pasal 5 (hak atas informasi kejelasan identitas pihak yang meminta data) & Pasal 21 ayat (1)",
        "saran": "Sebutkan nama usaha/badan usaha dan nama pemilik atau penanggung jawab sebagai pengendali data.",
    },
    {
        "id": "kontak",
        "label": "Kontak yang bisa dihubungi (email/WA/alamat)",
        "bobot": 1,
        "pola": [r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", r"\bwa\.me/|\bwa\.link/|api\.whatsapp\.com",
                 r"(\+62|\b0)[- ]?(8\d{1,3}|[1-9]\d{1,2})[- ]?\d{3,4}[- ]?\d{3,5}",
                 r"(hubungi|kontak|contact|narahubung|reach|tanyakan|pertanyaan|keluhan|questions?)[^.;\n]{0,60}"
                 r"(\bemail\b|\be-mail\b|\bsurel\b|\bwhatsapp\b|\bwa\b|telepon|\btelp\b|phone)",
                 r"hubungi kami", r"contact us", r"alamat (kantor|usaha|toko|klinik)"],
        "dasar": "UU 27/2022 Pasal 5 & Pasal 21 ayat (1) huruf g (agar subjek data dapat memakai haknya); narahubung dalam pemberitahuan kebocoran disebut PP 33/2026 menurut sumber sekunder (nomor pasal belum diverifikasi)",
        "saran": "Cantumkan email dan/atau nomor WhatsApp khusus urusan data pribadi, plus alamat usaha.",
    },
    {
        "id": "jenis_data",
        "label": "Jenis data pribadi yang dikumpulkan",
        "bobot": 1,
        "pola": [r"data (pribadi )?yang (kami )?(kumpulkan|kami kumpulkan|dikumpulkan|diproses|kami proses|kami catat|dicatat)",
                 r"jenis data", r"informasi yang (kami )?(kumpulkan|dikumpulkan)", r"(data|information) (we|that we) (collect|process)",
                 r"personal data we", r"types? of (personal )?data",
                 r"(memakai|menggunakan|memproses|mengumpulkan|mencatat) data[^.\n]{0,40}\(",
                 r"(nama|name|identitas)[^.\n]{0,60}(nomor|no\.? ?wa|alamat|email|phone|address|keluhan|tanggal lahir)"],
        "dasar": "UU 27/2022 Pasal 21 ayat (1) huruf c & e",
        "saran": "Tulis daftar data yang dikumpulkan (mis. nama, nomor WA, alamat kirim, riwayat pesanan).",
    },
    {
        "id": "tujuan",
        "label": "Tujuan pemrosesan",
        "bobot": 1,
        "pola": [r"tujuan (pemrosesan|pengumpulan|penggunaan)", r"\btujuan\b[ ,]+(dan )?dasar", r"\buntuk apa\b", r"(dipakai|dipergunakan) untuk",
                 r"(gunakan|menggunakan|memakai) (data|informasi)[^.\n]{0,40}untuk",
                 r"penggunaan (data|informasi)", r"bagaimana kami (menggunakan|memakai)", r"how we use",
                 r"digunakan untuk", r"untuk keperluan",
                 r"\b(gunakan|pakai|manfaatkan|proses|olah|dimanfaatkan|diolah|diproses) (hanya )?untuk", r"\bpurposes?\b", r"we use (your )?(personal )?(data|information)"],
        "dasar": "UU 27/2022 Pasal 16 ayat (2) huruf b & Pasal 21 ayat (1) huruf b",
        "saran": "Jelaskan untuk apa setiap data dipakai (proses pesanan, pengiriman, layanan pelanggan, promosi bila setuju).",
    },
    {
        "id": "dasar_pemrosesan",
        "label": "Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.)",
        "bobot": 1,
        "pola": [r"dasar (hukum )?(pemrosesan|pengolahan)", r"pasal 20", r"legal basis", r"lawful basis",
                 r"kepentingan (yang )?sah", r"legitimate interest", r"kewajiban (perjanjian|hukum)",
                 r"pelaksanaan perjanjian", r"performance of (a )?contract", r"legal obligation", r"legalitas (dari )?pemrosesan"],
        "dasar": "UU 27/2022 Pasal 20 ayat (2) & Pasal 21 ayat (1) huruf a",
        "saran": "Sebutkan dasar pemrosesan per tujuan: persetujuan, pelaksanaan perjanjian/pesanan, kewajiban hukum (mis. pajak), atau kepentingan yang sah.",
    },
    {
        "id": "penerima",
        "label": "Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan)",
        "bobot": 1,
        "pola": [r"pihak ketiga", r"third[- ]part", r"(bagikan|membagikan|berbagi|meneruskan|mengungkapkan)",
                 r"kurir|ekspedisi|jasa (pengiriman|kirim)", r"payment gateway|penyedia (layanan )?pembayaran",
                 r"prosesor data", r"service providers?", r"penyedia (layanan|jasa)", r"share (your )?(personal )?(data|information)",
                 r"penerima data", r"recipients?"],
        "dasar": "UU 27/2022 Pasal 21 & Pasal 51 (prosesor)",
        "saran": "Sebutkan kepada siapa data diberikan dan untuk apa (kurir, payment gateway, marketplace, penyedia cloud, platform iklan).",
    },
    {
        "id": "transfer_ln",
        "label": "Transfer/penyimpanan data di luar negeri",
        "bobot": 1,
        "pola": [r"luar negeri", r"luar wilayah (hukum )?(negara )?(republik )?indonesia", r"di luar indonesia", r"lintas (negara|batas)",
                 r"outside (of )?indonesia", r"cross[- ]border", r"\babroad\b", r"international transfer", r"transfer(red)? (to|outside)",
                 r"negara lain", r"other countries", r"server (asing|luar)",
                 r"(server|pusat data|data center|disimpan|diproses|hosting|di-?hosting|berlokasi|berada|store[sd]?|storing|host(?:s|ed|ing)?|"
                 r"process(?:es|ed|ing)?|located|kept|transferred)[^.\n]{0,60}" + NEGARA,
                 r"pasal 56"],
        "boleh_negatif": True,   # "tidak kami kirim ke luar negeri" juga informasi yang sah (opsi (b) template)
        "dasar": "UU 27/2022 Pasal 56",
        "saran": "Jelaskan apakah data disimpan/diproses di luar Indonesia (mis. Google Drive, Meta/WhatsApp, layanan cloud, hosting Singapura) dan pelindungannya.",
    },
    {
        "id": "masa_simpan",
        "label": "Masa simpan (retensi) data",
        "bobot": 1,
        "pola": [r"(masa|jangka waktu|lama) (simpan|penyimpanan|retensi)", r"disimpan (selama|paling lama|sampai|hingga)",
                 r"simpan (selama|paling lama|sampai|hingga)", r"\bretensi\b", r"\bretention\b", r"\bretain(ed)?\b",
                 r"(simpan|disimpan|menyimpan|penyimpanan|retain|keep|store|kept|stored)[^.\n]{0,60}?" + DURASI,
                 r"(dihapus|dimusnahkan|hapus|musnahkan|deleted|erased|destroyed)[^.\n]{0,60}?" + DURASI,
                 r"(kept|stored) (for|until)", r"how long we (keep|store)"],
        "dasar": "UU 27/2022 Pasal 21 ayat (1) huruf d & f, Pasal 43–44",
        "saran": "Tulis berapa lama data disimpan per jenis (mis. data pesanan 10 tahun untuk pembukuan pajak, chat CS 1 tahun) lalu dihapus.",
    },
    {
        "id": "hak_subjek",
        "label": "Hak subjek data (akses, koreksi, hapus, tarik persetujuan)",
        "bobot": 2,
        "sub": {
            "akses": [r"akses (ke |terhadap |atas )?data", r"hak (untuk )?(mengakses|akses)", r"salinan data", r"access (to )?your",
                      r"right (of|to) access", r"copy of your", r"\bmengakses\b", r"(meminta|minta) (salinan|akses)",
                      r"hak[^.\n]{0,60}\bakses\b", r"(^|\n)\s*(\d+\.\s*)?akses\b"],
            "koreksi": [r"memperbaiki|perbaikan|koreksi|memperbarui|pembaruan|melengkapi", r"correct|rectif|update your"],
            "hapus": [r"menghapus|penghapusan|dihapus|pemusnahan|memusnahkan", r"delet|eras"],
            "tarik_persetujuan": [r"(menarik|mencabut) (kembali )?persetujuan|(penarikan|pencabutan) (kembali )?persetujuan|(tarik|cabut) persetujuan",
                                  r"withdraw(al of)? (your )?consent|revoke (your )?consent"],
        },
        "dasar": "UU 27/2022 Pasal 5–13 & Pasal 21 ayat (1) huruf g",
        "saran": "Tuliskan hak-hak berikut dengan bahasa sederhana: mengakses & minta salinan, memperbaiki, menghapus, menarik persetujuan (juga: keberatan atas keputusan otomatis, membatasi pemrosesan, gugat ganti rugi).",
    },
    {
        "id": "cara_ajukan",
        "label": "Cara mengajukan permintaan hak & batas waktu tanggapan",
        "bobot": 1,
        "pola": [r"(ajukan|mengajukan|kirim(kan)?|sampaikan) (permintaan|permohonan)", r"cara (mengajukan|menggunakan hak)",
                 r"hubungi kami[^.\n]{0,60}(permintaan|permohonan|\bhak\b|mengajukan)",
                 r"hubungi[^.\n]{0,60}untuk (akses|mengakses|perbaikan|memperbaiki|penghapusan|menghapus|menarik)",
                 r"(menanggapi|merespons|memproses|menindaklanjuti) (setiap )?(permintaan|permohonan)",
                 r"3 ?(x|×) ?24 jam", r"(submit|send|make) (a |your )?request",
                 r"contact[^.\n]{0,60}to (access|correct|delete|exercise|withdraw)",
                 r"exercise (your|these|any of these) rights", r"72 (jam|hours)"],
        "dasar": "UU 27/2022 Pasal 30, 32, 40 (tanggapan paling lambat 3×24 jam)",
        "saran": "Tulis cara mengajukan (email/WA mana, data apa yang perlu disertakan) dan janji tanggapan paling lambat 3×24 jam.",
    },
    {
        "id": "keamanan",
        "label": "Langkah keamanan data",
        "bobot": 1,
        "pola": [r"enkripsi|terenkripsi|tersandi|kata sandi|\bsandi\b|autentikasi|otentikasi|verifikasi (dua|2) langkah|\b2fa\b",
                 r"akses[^.;\n]{0,40}(terbatas|dibatasi)", r"membatasi akses|pembatasan akses|hak akses", r"\bhttps\b|\bssl\b|\btls\b",
                 r"firewall|antivirus|anti-?malware|cadangan (data|berkala)|backup|perangkat (terkunci|dikunci)|dikunci",
                 r"langkah(-langkah)? (keamanan|pengamanan|pelindungan) (teknis|organisasi|berikut|yang kami)",
                 r"encrypt|password|two[- ]factor|multi[- ]factor|access controls?|restrict(ed|s)? access|limit(ed|s)? access|firewall",
                 r"(implement|use|apply|maintain|employ)[^.;\n]{0,40}(security measures|safeguards)"],
        "dasar": "UU 27/2022 Pasal 35–39",
        "saran": "Jelaskan langkah keamanan secara jujur dan umum (akses dibatasi, kata sandi + verifikasi 2 langkah, perangkat terkunci, cadangan).",
    },
    {
        "id": "kebocoran",
        "label": "Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data)",
        "bobot": 1,
        "pola": [r"(kegagalan pelindungan|kebocoran|insiden|bocor)[^.\n]{0,160}" + BERITAHU_ID,
                 BERITAHU_ID + r"[^.\n]{0,160}(kegagalan pelindungan|kebocoran|insiden)",
                 r"(breach|security incident|leak)[^.\n]{0,160}" + BERITAHU_EN, BERITAHU_EN + r"[^.\n]{0,160}(breach|incident)",
                 r"breach notification", r"pasal 46"],
        "dasar": "UU 27/2022 Pasal 46",
        "saran": "Tulis bahwa bila terjadi kegagalan pelindungan data, Anda akan memberi tahu pelanggan secara tertulis paling lambat 3×24 jam.",
    },
    {
        "id": "tanggal",
        "label": "Tanggal berlaku / terakhir diperbarui",
        "bobot": 1,
        "pola": [r"berlaku (sejak|mulai|efektif)", r"terakhir (diperbarui|diubah)", r"tanggal berlaku", r"diperbarui (pada|tanggal)",
                 r"last (updated|revised|modified)", r"effective (date|as of|from)"],
        "dasar": "UU 27/2022 Pasal 21 ayat (2) (perubahan informasi)",
        "saran": "Tulis \"Berlaku sejak: [tanggal]\" dan \"Terakhir diperbarui: [tanggal]\" di bagian atas.",
    },
    {
        "id": "perubahan",
        "label": "Cara memberi tahu perubahan kebijakan",
        "bobot": 1,
        "pola": [r"(perubahan|mengubah|memperbarui|diubah|diperbarui|berubah)[^.\n]{0,120}" + BERITAHU_ID,
                 BERITAHU_ID + r"[^.\n]{0,80}(perubahan|diubah|diperbarui)",
                 r"(change|update|amend)[^.\n]{0,120}(notify|announce|inform|notice)", r"(notify|announce|inform)[^.\n]{0,60}(change|update)"],
        "dasar": "UU 27/2022 Pasal 21 ayat (2)",
        "saran": "Tulis bahwa perubahan akan diberitahukan SEBELUM berlaku (mis. lewat website/WA/email).",
    },
]

# Unsur bersyarat: hanya diwajibkan bila pemicunya muncul di teks.
UNSUR_BERSYARAT = [
    {
        "id": "data_anak",
        "label": "Data anak: persetujuan orang tua/wali",
        "bobot": 1,
        "pemicu": [r"\banak\b", r"di bawah (umur|usia)", r"di bawah \d{1,2} tahun", r"(usia|berusia|umur) (di bawah|kurang dari) \d{1,2}",
                   r"belum dewasa", r"\bsiswa\b|\bmurid\b|\bbalita\b|\bbayi\b",
                   r"\bchild(ren)?\b", r"\bminors?\b", r"under (the age of )?\d{1,2}\b"],
        "pola": [r"orang ?tua", r"\bwali\b", r"parent", r"guardian"],
        "dasar": "UU 27/2022 Pasal 4 ayat (2) huruf e & Pasal 25",
        "saran": "Tulis bahwa data anak hanya diproses dengan persetujuan orang tua/wali, dan bagaimana persetujuan itu diminta.",
    },
    {
        "id": "data_spesifik",
        "label": "Data spesifik (kesehatan, biometrik, keuangan, dll.): perlakuan khusus",
        "bobot": 1,
        "pemicu": [r"kesehatan|rekam medis|riwayat (penyakit|medis)|\bpasien\b|diagnosis|alergi", r"biometri|sidik jari|pengenalan wajah|face ?id",
                   r"genetik|\bdna\b", r"catatan kejahatan|catatan kriminal|\bskck\b", r"data keuangan|slip gaji|mutasi rekening|riwayat kredit|\bslik\b",
                   r"\bhealth\b|medical|\bpatients?\b|biometric|genetic|criminal record|financial data"],
        "pola": [r"(data (pribadi )?(yang )?(bersifat )?spesifik)", r"persetujuan (tertulis|eksplisit|khusus|terpisah)",
                 r"pasal 4 ayat \(?2\)?", r"sensitive (personal )?data", r"special categor", r"explicit consent"],
        "dasar": "UU 27/2022 Pasal 4 ayat (2), Pasal 20 & 34 (penilaian dampak bila berisiko tinggi)",
        "saran": "Sebut jelas bahwa data kesehatan/biometrik/keuangan/anak adalah data spesifik, diproses dengan persetujuan eksplisit terpisah dan akses yang lebih ketat.",
    },
]

# ---------------------------------------------------------------------------
# Frasa berisiko.
#   cek_negasi=True  → abaikan bila klausa itu disangkal (tidak/never/not ... sebelum atau di dalam kecocokan)
#   cek_negasi=False → pola memang berisi penyangkal (mis. "tidak bertanggung jawab atas kebocoran")
#   kecuali          → abaikan bila kalimat yang sama memuat pola ini dengan polaritas positif
# ---------------------------------------------------------------------------
_JUAL_ALASAN = ("Mengungkapkan/menggunakan data pribadi orang lain secara melawan hukum dilarang (Pasal 65 ayat (2)-(3)) dan "
                "diancam pidana (Pasal 67). Menjual data hampir pasti tidak punya dasar pemrosesan yang sah (Pasal 20).")
_JUAL_SARAN = "Hapus. Tegaskan: \"Kami tidak menjual data pribadi Anda.\" (EN: \"We do not sell your personal data.\")"
_LEPAS_ALASAN = ("Pengendali tetap bertanggung jawab atas pemrosesan & wajib melindungi data (Pasal 35, 46, 47). Klausul lepas "
                 "tanggung jawab tidak menghapus kewajiban ini dan merusak kepercayaan.")
_LEPAS_SARAN = "Hapus. Ganti dengan komitmen menjaga keamanan dan memberi tahu paling lambat 3×24 jam bila terjadi kebocoran."
_BOCOR_ALASAN = ("Pengendali WAJIB memberi tahu subjek data dan lembaga secara tertulis paling lambat 3×24 jam bila terjadi "
                 "kegagalan pelindungan data (Pasal 46). Klausul tidak memberi tahu/merahasiakan kebocoran melanggar kewajiban ini.")
_BOCOR_SARAN = "Hapus. Tulis: \"Bila terjadi kegagalan pelindungan data, kami memberi tahu Anda secara tertulis paling lambat 3×24 jam.\""
_DIANGGAP_ALASAN = ("Persetujuan harus eksplisit, tertulis/terekam, untuk tujuan tertentu (Pasal 20 ayat (2) huruf a & Pasal 22). "
                    "Persetujuan 'dianggap' tidak memenuhi.")
_IKLAN_ALASAN = ("Memberikan data ke pihak lain untuk iklan/pemasaran memerlukan persetujuan eksplisit per tujuan (Pasal 20 ayat (2) huruf a "
                 "& Pasal 22) dan penerima yang jelas (Pasal 16 ayat (2)). Kalimat \"tidak menjual, tetapi membagikan ke mitra iklan\" tetap berisiko.")
_IKLAN_SARAN = ("Sebut penerima & tujuannya, dan lakukan hanya dengan persetujuan aktif terpisah yang bisa ditolak; atau tegaskan "
                "\"Kami tidak membagikan data Anda kepada pengiklan.\"")
_ANAK_ALASAN = ("Batas usia 13 tahun berasal dari aturan AS (COPPA). Di Indonesia, UU 27/2022 Pasal 25 mewajibkan persetujuan orang tua/wali "
                "untuk data anak 'sesuai ketentuan peraturan perundang-undangan'; UU 35/2014 (Perlindungan Anak) Pasal 1 angka 1: anak = belum "
                "berusia 18 tahun. UU PDP sendiri tidak memuat batas usia lain.")
_ANAK_SARAN = ("Ganti batas usia menjadi \"di bawah 18 tahun\" dan tulis bahwa data anak hanya diproses dengan persetujuan orang tua/wali "
               "(EN: \"under 18 ... with the consent of a parent or guardian\").")
_UBAH_ALASAN = "Pengendali wajib memberi tahu subjek data SEBELUM informasi pemrosesan berubah (Pasal 21 ayat (2))."
_UBAH_SARAN = "Ganti: \"Perubahan akan kami umumkan paling lambat [isi: 7] hari sebelum berlaku.\""

RISIKO = [
    # --- lepas tanggung jawab / tidak memberi tahu kebocoran (pola berisi penyangkal) ---
    dict(pola=r"tidak (akan )?(ikut )?bertanggung ?jawab (atas|terhadap|jika|bila|apabila|kalau|untuk)[^.;\n]{0,60}?"
              r"(kebocoran|bocor|kehilangan|penyalahgunaan|kerugian|akses|diretas|peretasan|pencurian)",
         tingkat="TINGGI", alasan=_LEPAS_ALASAN, saran=_LEPAS_SARAN, cek_negasi=False),
    dict(pola=r"(dibebaskan|terbebas|terlepas|lepas) dari (segala |setiap |semua )?(bentuk )?(tanggung ?jawab|tuntutan|kewajiban)",
         tingkat="TINGGI", alasan=_LEPAS_ALASAN, saran=_LEPAS_SARAN, cek_negasi=True),
    dict(pola=r"(not|no) (be )?(held )?(responsible|liable) for[^.;\n]{0,40}?(breach|leak|loss|misuse|unauthori|hack)",
         tingkat="TINGGI", alasan=_LEPAS_ALASAN, saran="Hapus. Ganti dengan komitmen keamanan & pemberitahuan kebocoran 3×24 jam.", cek_negasi=False),
    dict(pola=r"(tidak|tak)( akan| perlu| wajib| harus)? (memberi ?tahu|memberitahu(kan)?|menginformasikan|mengabarkan|mengabari|melaporkan|mengumumkan)"
              r"[^.;\n]{0,80}?(bocor|kebocoran|insiden|kegagalan pelindungan|peretasan|diretas)",
         tingkat="TINGGI", alasan=_BOCOR_ALASAN, saran=_BOCOR_SARAN, cek_negasi=False),
    dict(pola=r"(bocor|kebocoran|insiden|kegagalan pelindungan|peretasan)[^.;\n]{0,80}?(tidak|tak)( akan| perlu| wajib| harus)? "
              r"(diberitahukan|diumumkan|dilaporkan|diinformasikan|memberi ?tahu|memberitahu(kan)?|menginformasikan|melaporkan|mengumumkan)",
         tingkat="TINGGI", alasan=_BOCOR_ALASAN, saran=_BOCOR_SARAN, cek_negasi=False),
    dict(pola=r"(merahasiakan|menyembunyikan|menutupi|tutupi|rahasiakan) (setiap |segala |adanya )?(kebocoran|insiden|kegagalan pelindungan|peretasan)",
         tingkat="TINGGI", alasan=_BOCOR_ALASAN, saran=_BOCOR_SARAN, cek_negasi=True),
    dict(pola=r"(not|never|no obligation to) (be )?(notify|inform|disclose|report)[^.;\n]{0,80}?(breach|leak|incident)"
              r"|(breach|leak|incident)[^.;\n]{0,80}?(will|shall) not (be )?(notif|disclos|report|inform)",
         tingkat="TINGGI", alasan=_BOCOR_ALASAN, saran=_BOCOR_SARAN, cek_negasi=False),
    # --- jual/sewakan/monetisasi data ---
    dict(pola=V_JUAL_ID + r"(?:" + SAMBUNG + r" " + V_JUAL_ID + r")*(?: kembali| lagi)? (?:seluruh |semua |segala |sebagian )?" + OBJEK_ID,
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"(dapat|boleh|berhak|akan|bisa|mungkin) " + V_JUAL_ID + r"[^.;\n]{0,60}?\b" + OBJEK_ID,
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"\b" + OBJEK_ID + r"\b[^.;\n]{0,40}?\b(dijual|disewakan|diperjualbelikan|diperdagangkan|dimonetisasi|dikomersialkan|ditukar(kan)?)\b"
              r"|(dapat|akan|boleh|bisa) kami (jual|sewakan|perjualbelikan|perdagangkan|monetisasi|tukar)\b"
              r"|\b" + OBJEK_ID + r"\b[^.;\n]{0,60}?\bkami (jual|sewakan|perjualbelikan|perdagangkan|monetisasi)\b",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"(" + V_BAGI_ID + r"|menukar(kan)?|ditukar(kan)?)[^.;\n]{0,80}?"
              r"(dengan|untuk|sebagai|demi|atas) (imbalan|bayaran|kompensasi|uang|keuntungan|komisi|biaya|fee|pembayaran)",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True,
         perlu=r"imbalan|bayaran|kompensasi|uang|keuntungan|komisi|biaya|\bfee\b|pembayaran"),
    dict(pola=r"(?:(?:share|disclose|transfer|provide)" + SAMBUNG + r" )*\b" + V_JUAL_EN + r"\b(?:" + SAMBUNG + r" (?:" + V_JUAL_EN[3:-1] + r"|share|disclose))*"
              r"(?: (?:your|the|all|any|such|our|customer|customers'|user|users'|some|certain|this|that|collected|contact|account|profile|usage|"
              r"location|demographic|behaviou?ral|aggregated?|anonymi[sz]ed|de-identified|non-personal|identifiable|personal|and|or|&|,))* " + OBJEK_EN,
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"\b" + OBJEK_EN + r"\b[^.;\n]{0,40}?\b(sold|rented|leased|traded|monetized|monetised)\b",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"(share|disclose|provide|transfer|give)[^.;\n]{0,80}?(for (payment|money|compensation|a fee|profit|monetary)|in exchange for|to data brokers)",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    # --- berbagi data ke mitra iklan/pemasaran (B-1/B-2): polaritas dinilai per klausa ---
    dict(pola=V_BAGI_ID + r"[^.;\n]{0,80}?(?:kepada|ke|dengan|untuk|bagi) " + SASARAN_IKLAN_ID
              + r"|" + V_BAGI_ID + r" (?:kepada|ke|dengan) [^.;\n]{1,50}?" + TUJUAN_IKLAN_ID
              + r"|" + SASARAN_IKLAN_ID + r"[^.;\n]{0,60}?\b" + V_BAGI_ID + r"\b"
              + r"|\b" + V_BAGI_EN + r"\b[^.;\n]{0,80}?\b(?:with|to|among)\b[^.;\n]{0,60}?" + SASARAN_IKLAN_EN
              + r"|\b" + V_BAGI_EN + r" (?:it|them|(?:[a-z']+ ){0,3}" + OBJEK_EN + r")\b[^.;\n]{0,60}?\bfor (?:targeted |direct |their (?:own )?)?(?:advertising|marketing|promotional)(?: purposes)?",
         tingkat="SEDANG", alasan=_IKLAN_ALASAN, saran=_IKLAN_SARAN, cek_negasi=True, kecuali=PERSETUJUAN, perlu=PERLU_IKLAN,
         syarat_kalimat=OBJEK_ORANG),
    # "tidak membagikan ... kecuali kepada mitra iklan" = tetap berbagi ke mitra iklan
    dict(pola=r"\b(?:kecuali|selain|except|other than|apart from)\b(?: (?:kepada|ke|untuk|dengan|bagi|to|with|for))? (?:para |our |the |kami )?"
              r"(?:" + SASARAN_IKLAN_ID + r"|" + SASARAN_IKLAN_EN + r")",
         tingkat="SEDANG", alasan=_IKLAN_ALASAN, saran=_IKLAN_SARAN, cek_negasi=True, kecuali=PERSETUJUAN, perlu=PERLU_IKLAN),
    # --- persetujuan dianggap / tidak bisa ditarik ---
    dict(pola=r"(diam(nya)?|tidak (membalas|menjawab|menolak|merespons|keberatan)|silence|inaction|failure to (respond|object|reply))[^.;\n]{0,80}?"
              r"(dianggap|kami anggap|kami artikan|berarti|diartikan|deemed|treated as|considered|constitutes?)[^.;\n]{0,20}?(setuju|persetujuan|menyetujui|consent|agreement|acceptance)"
              r"|kami (anggap|artikan|perlakukan) (sebagai )?(tanda )?(persetujuan|setuju|menyetujui)"
              r"|(treat|consider|take|regard) (your )?(silence|inaction|continued use)[^.;\n]{0,20}? as (your )?(consent|agreement|acceptance)",
         tingkat="TINGGI", alasan=_DIANGGAP_ALASAN,
         saran="Ganti dengan kotak centang/balasan \"SETUJU\" yang aktif dari pelanggan, per tujuan. Diam bukan persetujuan.", cek_negasi=True),
    dict(pola=r"persetujuan[^.;\n]{0,30}?(dianggap|kami anggap) (telah )?(diberikan|ada|sah)", tingkat="TINGGI", alasan=_DIANGGAP_ALASAN,
         saran="Ganti dengan kotak centang/balasan \"SETUJU\" yang aktif dari pelanggan, per tujuan.", cek_negasi=True),
    dict(pola=r"dianggap (telah )?(menyetujui|setuju|memberikan persetujuan|menerima)", tingkat="TINGGI",
         alasan="Persetujuan diam-diam/dianggap tidak memenuhi syarat persetujuan eksplisit (Pasal 20 & 22).",
         saran="Minta persetujuan aktif (centang/ketik SETUJU); untuk pemrosesan wajib (pesanan) gunakan dasar 'pelaksanaan perjanjian'.", cek_negasi=True),
    dict(pola=r"(deemed|assumed|considered) to (have )?(consent|agree|accept)", tingkat="TINGGI",
         alasan="Persetujuan 'dianggap' (deemed consent) tidak memenuhi syarat persetujuan eksplisit (Pasal 20 & 22).",
         saran="Ganti dengan persetujuan aktif per tujuan (opt-in).", cek_negasi=True),
    dict(pola=r"persetujuan[^.;\n]{0,40}?tidak (dapat|bisa|boleh) (ditarik|dicabut|dibatalkan)|(consent|agreement) (is )?(irrevocable|cannot be withdrawn|may not be withdrawn)",
         tingkat="TINGGI", alasan="Subjek data berhak menarik persetujuan kapan saja (Pasal 9 & 40).",
         saran="Hapus. Tulis cara menarik persetujuan dan bahwa pemrosesan dihentikan paling lambat 3×24 jam.", cek_negasi=False),
    # --- simpan selamanya ---
    dict(pola=r"(disimpan|menyimpan|simpan)[^.;\n]{0,40}?(selamanya|tanpa batas( waktu)?|seumur hidup|secara permanen|permanen)"
              r"|(retain|store|keep|kept|stored|retained)[^.;\n]{0,40}?(indefinitely|forever|permanently)",
         tingkat="TINGGI", alasan="Data wajib dihapus bila tidak lagi diperlukan untuk tujuannya (Pasal 43) dan masa retensi harus diinformasikan (Pasal 21).",
         saran="Tetapkan masa simpan per jenis data, lalu hapus/musnahkan.", cek_negasi=True),
    # --- pelepasan hak ---
    dict(pola=r"(tidak (dapat|bisa|berhak) (menuntut|mengajukan (tuntutan|gugatan)))|melepaskan (hak|segala tuntutan)|waive (any|all|your) (rights?|claims?)",
         tingkat="TINGGI", alasan="Subjek data berhak menggugat & menerima ganti rugi (Pasal 12). Pelepasan hak sepihak berisiko batal.",
         saran="Hapus klausul pelepasan hak.", cek_negasi=False),
    # --- SEDANG ---
    dict(pola=r"dengan (menggunakan|mengakses|mengunjungi|mendaftar|melanjutkan)(?:(?!dianggap)[^.\n]){0,80}(setuju|menyetujui|menerima)",
         tingkat="SEDANG", alasan="'Dengan memakai layanan, Anda setuju' bukan persetujuan eksplisit per tujuan (Pasal 20 & 22). Boleh untuk menyatakan telah membaca kebijakan, bukan sebagai dasar pemrosesan data.",
         saran="Ubah menjadi pemberitahuan (\"Kebijakan ini menjelaskan...\") dan minta persetujuan terpisah untuk promosi/data spesifik.", cek_negasi=True),
    dict(pola=r"by (using|accessing|visiting|continuing)[^.\n]{0,80}(you )?(agree|consent|accept)", tingkat="SEDANG",
         alasan="Persetujuan 'dengan memakai situs, Anda setuju' (browse-wrap) bukan persetujuan eksplisit per tujuan (Pasal 20 & 22).",
         saran="Jadikan pemberitahuan saja; minta persetujuan aktif terpisah untuk promosi/data spesifik.", cek_negasi=True),
    dict(pola=r"(kebijakan|ketentuan|syarat|privasi|pemberitahuan ini)[^.;\n]{0,80}?\b((meng|di)?ubah|(mem|di)?perbarui|(me|di)?revisi|berubah|perubahan)(nya)?\b"
              r"[^.;\n]{0,80}?tanpa (pemberitahuan|memberi ?tahu|diberitahukan)"
              r"|(mengubah|memperbarui|merevisi|perubahan)( atas| terhadap)? (kebijakan|ketentuan|syarat)[^.;\n]{0,80}?tanpa (pemberitahuan|memberi ?tahu|diberitahukan)"
              r"|(mengubah|memperbarui|merevisi)nya[^.;\n]{0,40}?tanpa (pemberitahuan|memberi ?tahu|diberitahukan)"
              r"|(policy|policies|terms|privacy|notice)[^.;\n]{0,80}?(change|modif|update|amend|revis)[^.;\n]{0,60}?without (prior |any )?(notice|notification|informing)"
              r"|(change|modify|update|amend|revise) (it|this|our|the|these|such|any)( privacy)? ?(policy|policies|terms|notice)?[^.;\n]{0,60}?without (prior |any )?(notice|notification|informing)",
         tingkat="SEDANG", alasan=_UBAH_ALASAN, saran=_UBAH_SARAN, cek_negasi=True),
    dict(pola=r"(kebijakan|ketentuan|syarat|policy|terms)[^.;\n]{0,60}?(diubah|diperbarui|berubah|direvisi|mengubah|memperbarui|merevisi|changed|modified|updated|amended|change|modify|update|amend)"
              r"[^.;\n]{0,40}?(sewaktu-? ?waktu|kapan saja|kapan pun|setiap saat|at any time|from time to time)"
              r"|(kebijakan|ketentuan|syarat)[^.;\n]{0,40}?\b(ubah|perbarui|revisi)\b[^.;\n]{0,40}?(sewaktu-? ?waktu|kapan saja|kapan pun|setiap saat)"
              r"|(mengubah|memperbarui|merevisi|change|modify|update|amend) (kebijakan|ketentuan|syarat|pemberitahuan privasi|this policy|these terms|our policy|this notice)[^.;\n]{0,40}?"
              r"(sewaktu-? ?waktu|kapan saja|kapan pun|setiap saat|at any time|from time to time)",
         tingkat="SEDANG", alasan=_UBAH_ALASAN, saran=_UBAH_SARAN, cek_negasi=True,
         kecuali=r"\b(?:" + BERITAHU_ID + r")(?! privasi| ini\b)|\b(?:" + BERITAHU_EN + r")(?! (?:is|applies))"),
    dict(pola=r"(kepada|dengan) (siapa ?pun|pihak mana ?pun|semua pihak|pihak ketiga mana ?pun)|with any(one| third part(y|ies))",
         tingkat="SEDANG", alasan="Berbagi data tanpa batas penerima & tujuan tidak memenuhi prinsip terbatas dan spesifik (Pasal 16 ayat (2)).",
         saran="Sebutkan penerima secara spesifik (kategori + tujuan).", cek_negasi=True, negasi_klausa=True),
    dict(pola=r"(untuk|demi|for) (tujuan|keperluan|kepentingan) (apa ?pun|lain ?nya|lain apa pun|apa saja)|for any (other )?purpose(s)? (whatsoever|we (deem|see fit))|for any purpose",
         tingkat="SEDANG", alasan="Tujuan pemrosesan wajib spesifik dan terbatas (Pasal 16 ayat (2) huruf b); \"untuk tujuan apa pun\" tidak memenuhi.",
         saran="Sebutkan tujuan secara spesifik (mis. memproses pesanan, pengiriman, layanan pelanggan).", cek_negasi=True),
    dict(pola=r"(semua|seluruh|segala) (data|informasi)[^.\n]{0,30}(di|pada) (perangkat|ponsel|hp|galeri|kontak) anda|all (data|information) on your device",
         tingkat="SEDANG", alasan="Mengumpulkan melebihi keperluan melanggar prinsip minimisasi (Pasal 16 ayat (2) huruf a).",
         saran="Batasi ke data yang benar-benar diperlukan.", cek_negasi=True),
    dict(pola=r"\bgdpr\b|\bccpa\b|california|general data protection regulation|european economic area|uni eropa",
         tingkat="SEDANG", alasan="Tampaknya disalin dari kebijakan luar negeri (GDPR/CCPA). Hak & kewajiban di Indonesia mengikuti UU 27/2022.",
         saran="Tulis ulang dengan rujukan UU 27/2022 (batas 3×24 jam, pemberitahuan kebocoran, dasar pemrosesan Pasal 20).", cek_negasi=False),
    dict(pola=r"(under|below|younger than) (the age of |age )?1[0-6]\b|(under|below)[- ]1[0-6]s?\b|di bawah (usia |umur )?1[0-6] tahun|"
              r"(usia|umur|berusia) (di bawah|kurang dari) 1[0-6] tahun|\bcoppa\b",
         tingkat="SEDANG", alasan=_ANAK_ALASAN, saran=_ANAK_SARAN, cek_negasi=False),
    dict(pola=r"100 ?% aman|dijamin aman sepenuhnya|aman sepenuhnya|completely secure|100 ?% secure|fully secure|perfectly secure",
         tingkat="SEDANG", alasan="Klaim keamanan mutlak menyesatkan dan bertentangan dengan kewajiban menyiapkan penanganan kebocoran (Pasal 46).",
         saran="Ganti dengan langkah keamanan nyata yang dilakukan.", cek_negasi=True),
    dict(pola=r"tidak (mungkin|akan pernah|akan) bocor|(can|will) never be (hacked|breached|leaked)",
         tingkat="SEDANG", alasan="Klaim keamanan mutlak menyesatkan dan bertentangan dengan kewajiban menyiapkan penanganan kebocoran (Pasal 46).",
         saran="Ganti dengan langkah keamanan nyata yang dilakukan.", cek_negasi=False),
]

# Penyangkal. Pengecualian: "tidak hanya/not only", "tidak lebih dari/no more than", "not limited to", "no. hp/no wa".
NEGASI = re.compile(
    r"\b(?:tidak|tak|bukan|belum|jangan|takkan|tiada|never|not|cannot|nor|neither|none|no|"
    r"(?:don|doesn|didn|won|wouldn|isn|aren|wasn|weren|can|couldn|shouldn|hasn|haven|hadn|mustn)'t)\b"
    r"(?!\s*(?:hanya|only|saja|lebih|melebihi|melewati|more|longer|later|limited|terbatas pada|sekadar)\b)"
    r"(?![.\d])(?!\s*(?:hp|wa|telp|telepon|rekening|rek|ktp|npwp|handphone|whatsapp|pesanan|resi|invoice|\d))")
# Idiom yang bentuknya negatif tetapi maknanya "mungkin" (penyangkal di dalamnya diabaikan)
IDIOM_MUNGKIN = re.compile(r"\b(?:bukan tidak mungkin|bukan mustahil|tidak mustahil|tak mustahil|tidak menutup kemungkinan|tak menutup kemungkinan|"
                           r"tidak tertutup kemungkinan|tidak jarang|not impossible|not unlikely|not uncommon|cannot rule out|can't rule out)\b")
TANPA = re.compile(r"\b(?:tanpa|without)\b")
KLAUSA = re.compile(
    r"[;:]|\s[-–—]\s|,?\s+(?:tetapi|tapi|namun|melainkan|sedangkan|padahal|kecuali|selain itu|but|however|whereas|although|except|meskipun|walaupun)\b"
    r"|,\s*(?:dan |and |serta |lalu |kemudian |then )?(?:kami|we|anda|you|data|informasi|information|mereka|they|pihak)\b"
    r"|\s(?:dan|and) (?:kami|we)\b")
AKHIR_KALIMAT = re.compile(r"\n|\x1e|[.!?]+(?=\s|$)")
SINGKATAN = {"jl", "no", "pt", "cv", "ud", "tbk", "dll", "dsb", "mis", "dr", "drg", "sdr", "bpk", "hlm", "tgl", "telp",
             "e.g", "i.e", "etc", "vs", "mr", "mrs", "ms", "ps", "ay", "ir", "prof", "kec", "kab", "kel", "rt", "rw"}
URUTAN_STATUS = (
    "1. KURANG LENGKAP — skor < 60: banyak bagian pokok belum ada. Ini mengalahkan BELUM SIAP: dokumen berisian kosong [isi: ...] "
    "tetap KURANG LENGKAP bila skor strukturnya (seandainya semua isian dilengkapi) pun < 60 atau ada frasa TINGGI.",
    "2. PERLU PERBAIKAN — ada frasa berisiko TINGGI.",
    "3. BELUM SIAP — masih ada isian kosong [isi: ...], struktur sudah cukup.",
    "4. PERLU PERBAIKAN — skor 60-84.",
    "5. CUKUP LENGKAP — skor >= 85, tanpa frasa TINGGI, tanpa isian kosong.",
)
PESAN_RISIKO_KOSONG = (
    "Pola kata kunci tidak menemukan frasa berisiko. Ini BUKAN jaminan kebijakan aman: script hanya mengenali "
    "kata-kata tertentu dan sering melewatkan kalimat berisiko yang ditulis dengan kata lain (mis. \"kami kolaborasikan "
    "dengan mitra\", \"made available to partners\", \"at our sole discretion\"). Baca seluruh dokumen secara manual "
    "per kategori di references/kategori-risiko-cek.md.")
PESAN_RISIKO_ADA = (
    "Daftar ini hanya penanda awal dari pola kata kunci dan TIDAK lengkap. Kalimat berisiko lain yang ditulis dengan "
    "kata berbeda tetap harus dicari dengan membaca manual per kategori (references/kategori-risiko-cek.md).")
BATAS_SKOR_ISIAN = 84   # skor maksimum selama masih ada isian kosong (di bawah ambang CUKUP LENGKAP 85)
JENDELA = 60   # karakter maksimum sebelum kecocokan yang diperiksa untuk penyangkal

PLACEHOLDER = re.compile(r"\[(?:isi|fill)\s*:[^\]\n]*\]|\[(?:isi|fill)\]|\[\[[^\]\n]*\]\]|\[\.\.\.\]|\{jika[^}\n]*\}|\{if[^}\n]*\}|lorem ipsum|\bxxx+\b", re.I)

# Layanan pihak ketiga yang umumnya menyimpan data di luar Indonesia (pemicu saran transfer_ln)
LAYANAN_LN = re.compile(r"\b(?:google|gmail|google drive|meta|facebook|instagram|whatsapp|tiktok|shopify|aws|amazon web|cloudflare|mailchimp|zoom|openai|chatgpt|claude|dropbox|microsoft|notion)\b", re.I)  # v1.0.4 U4-2: batas kata

TAG_BLOK = re.compile(r"</?(?:p|div|br|li|ul|ol|h[1-6]|tr|td|th|table|section|article|header|footer|nav|main|title|blockquote|hr|dd|dt|dl)\b", re.I)
TAG = re.compile(r"<[a-zA-Z/!][^<>]{0,2000}>")
TANDA_HTML = re.compile(r"<(?:!doctype|html|head|body|p|div|span|br|b|strong|em|i|u|h[1-6]|li|ul|ol|a|table|tr|td|section|article|footer|header|meta|script|style)\b[^<>]{0,2000}>", re.I)
ENTITAS = re.compile(r"&(?:[a-zA-Z]{2,8}|#\d{1,6}|#x[0-9a-fA-F]{1,6});")


def _pisah_atas(p):
    """Pisahkan pola pada '|' tingkat teratas (di luar kurung & kelas karakter)."""
    bagian, dalam, kelas, mulai, i = [], 0, False, 0, 0
    while i < len(p):
        ch = p[i]
        if ch == "\\":
            i += 2
            continue
        if kelas:
            kelas = ch != "]"
        elif ch == "[":
            kelas = True
        elif ch == "(":
            dalam += 1
        elif ch == ")":
            dalam -= 1
        elif ch == "|" and dalam == 0:
            bagian.append(p[mulai:i])
            mulai = i + 1
        i += 1
    bagian.append(p[mulai:])
    return bagian


def _awalan(p):
    """Kata awal yang WAJIB muncul agar pola bisa cocok (untuk melewati pola secara cepat).
    Kembalikan None bila tidak bisa ditentukan dengan pasti."""
    hasil = set()
    for alt in _pisah_atas(p):
        while alt.startswith("\\b"):
            alt = alt[2:]
        if alt.startswith("(?:") or alt.startswith("("):
            buka = 3 if alt.startswith("(?:") else 1
            dalam, j = 1, buka
            while j < len(alt) and dalam:
                if alt[j] == "\\":
                    j += 2
                    continue
                dalam += {"(": 1, ")": -1}.get(alt[j], 0)
                j += 1
            if j < len(alt) and alt[j] in "?*{":
                return None                      # grup opsional → tidak pasti
            sub = _awalan(alt[buka:j - 1])
            if sub is None:
                return None
            hasil |= sub
        else:
            m = re.match(r"[a-z]{3,}", alt)
            if not m:
                return None
            hasil.add(m.group(0))
    return hasil or None


class Pola:
    """Regex + daftar kata awal untuk dilewati cepat bila tidak ada satu pun di teks."""

    def __init__(self, p):
        self.re = re.compile(p.replace(r"[^.\n]", "[^.\n\x1e]").replace(r"[^.;\n]", "[^.;\n\x1e]"))
        self.pattern = p
        self.awalan = _awalan(p)

    def finditer(self, t):
        if self.awalan is not None and not any(a in t for a in self.awalan):
            return iter(())
        return self.re.finditer(t)

    def cari(self, t, terima, awal=0, akhir=None):
        """Seperti finditer, tetapi bila kecocokan ditolak (`terima(m)` False, mis. disangkal),
        pencarian diulang dari karakter berikutnya agar kecocokan lebih pendek di dalamnya tetap ditemukan
        ("Kami tidak menyimpan data kartu, dan data pesanan disimpan selamanya")."""
        if self.awalan is not None and not any(a in t for a in self.awalan):
            return
        pos = awal
        n = len(t) if akhir is None else akhir
        while pos <= n:
            m = self.re.search(t, pos, n)
            if not m:
                return
            if terima(m):
                yield m
                pos = m.end() if m.end() > m.start() else m.start() + 1
            else:
                pos = m.start() + 1


def _c(p):
    return Pola(p)


for _u in UNSUR + UNSUR_BERSYARAT:
    for _k in ("pola", "pemicu"):
        if _k in _u:
            _u[_k + "_re"] = [_c(p) for p in _u[_k]]
    if "sub" in _u:
        _u["sub_re"] = {k: [_c(p) for p in v] for k, v in _u["sub"].items()}
for _r in RISIKO:
    _r["re"] = _c(_r["pola"])
    _r["kecuali_re"] = _c(_r["kecuali"]) if _r.get("kecuali") else None
    _r["perlu_re"] = re.compile(_r["perlu"]) if _r.get("perlu") else None
    _r["syarat_re"] = re.compile(_r["syarat_kalimat"]) if _r.get("syarat_kalimat") else None


class GalatInput(Exception):
    pass


# ---------------------------------------------------------------------------
# Membaca file
# ---------------------------------------------------------------------------
def _coba_utf16_tanpa_bom(data):
    contoh = data[:8192]
    n = len(contoh) // 2
    if n < 2:
        return None
    nol_genap = contoh[0::2].count(0)
    nol_ganjil = contoh[1::2].count(0)
    if nol_ganjil > 0.3 * n and nol_genap < 0.05 * n:
        enc = "utf-16-le"
    elif nol_genap > 0.3 * n and nol_ganjil < 0.05 * n:
        enc = "utf-16-be"
    else:
        return None
    try:
        teks = data[: len(data) - (len(data) % 2)].decode(enc)
    except UnicodeDecodeError:
        return None
    kendali = sum(1 for ch in teks[:4000] if unicodedata.category(ch) == "Cc" and ch not in "\n\r\t")
    return teks if kendali <= 0.01 * max(1, len(teks[:4000])) else None


def baca_teks(path):
    if not path:
        raise GalatInput("Nama file belum diberikan. Contoh: python3 cek_kebijakan.py kebijakan.md")
    if not os.path.exists(path):
        raise GalatInput("File tidak ditemukan: {}. Periksa nama & lokasi file.".format(path))
    if os.path.isdir(path):
        raise GalatInput("{} adalah folder, bukan file. Berikan file .md atau .txt kebijakan privasi.".format(path))
    try:
        ukuran = os.path.getsize(path)
    except OSError:
        ukuran = 0
    if ukuran > BATAS_BYTE:
        raise GalatInput("File terlalu besar ({:.1f} MB; batas 5 MB). Kebijakan privasi biasanya < 100 KB. "
                         "Salin hanya teks kebijakannya ke file .md/.txt.".format(ukuran / 1048576.0))
    try:
        with open(path, "rb") as f:
            data = f.read(BATAS_BYTE + 1)
    except OSError as e:
        raise GalatInput("File tidak bisa dibuka ({}).".format(e.strerror or e))
    if not data.strip():
        raise GalatInput("File kosong. Tempel isi kebijakan privasi ke file .md/.txt lalu coba lagi.")
    if data[:4] == b"PK\x03\x04":
        raise GalatInput("File tampaknya .docx/.zip. Simpan ulang sebagai .txt/.md (Word: File > Save As > Plain Text) atau tempel teksnya.")
    if data[:5] == b"%PDF-":
        raise GalatInput("File tampaknya PDF. Salin teksnya ke file .txt/.md, lalu periksa ulang.")
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        try:
            teks = data.decode("utf-16")
        except UnicodeDecodeError:
            raise GalatInput("File UTF-16 rusak. Simpan ulang sebagai UTF-8 (Notepad: Save As > Encoding: UTF-8).")
    elif b"\x00" in data:
        teks = _coba_utf16_tanpa_bom(data)
        if teks is None:
            raise GalatInput("File tampaknya biner (bukan teks). Berikan file .md/.txt. Jika ini file teks UTF-16, "
                             "simpan ulang sebagai UTF-8 (Notepad: Save As > Encoding: UTF-8).")
    else:
        teks = None
        for enc in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                teks = data.decode(enc)
                break
            except UnicodeDecodeError:
                continue
    if "\x00" in teks:
        raise GalatInput("File tampaknya biner (bukan teks). Berikan file .md/.txt.")
    if not teks.strip():
        raise GalatInput("File kosong setelah dibaca.")
    return teks


# ---------------------------------------------------------------------------
# Normalisasi (linier; nomor baris dipertahankan)
# ---------------------------------------------------------------------------
def _pertahankan_baris(s):
    return "\n" * s.count("\n")


def _buang_blok(teks, buka, tutup):
    """Buang blok seperti <!-- ... --> atau <script>...</script> dengan satu kali lintas (linier)."""
    rendah = teks.lower()
    keluar = []
    i = 0
    while True:
        a = rendah.find(buka, i)
        if a < 0:
            keluar.append(teks[i:])
            break
        b = rendah.find(tutup, a + len(buka))
        if b < 0:
            keluar.append(teks[i:a])
            keluar.append(_pertahankan_baris(teks[a:]))
            break
        keluar.append(teks[i:a])
        keluar.append(_pertahankan_baris(teks[a:b + len(tutup)]))
        i = b + len(tutup)
    return "".join(keluar)


def buang_html(teks):
    teks = _buang_blok(teks, "<!--", "-->")
    if TANDA_HTML.search(teks):
        teks = _buang_blok(teks, "<script", "</script>")
        teks = _buang_blok(teks, "<style", "</style>")

        def ganti(m):
            s = m.group(0)
            return _pertahankan_baris(s) + (BATAS_BLOK if TAG_BLOK.match(s) else "")
        teks = TAG.sub(ganti, teks)
    if ENTITAS.search(teks):
        teks = html.unescape(teks)
    return teks


def normalisasi(teks):
    """Kembalikan (bersih, t): `bersih` untuk kutipan, `t` = huruf kecil dengan panjang yang sama."""
    b = buang_html(teks)
    b = unicodedata.normalize("NFKC", b)
    b = b.replace("’", "'").replace("‘", "'").replace("\r\n", "\n").replace("\r", "\n")
    b = re.sub(r"[*_`#>|]+", " ", b)          # markup markdown
    b = re.sub(r"[ \t ]+", " ", b)
    t = b.lower()
    if len(t) != len(b):
        t = "".join(c.lower() if len(c.lower()) == 1 else c for c in b)
    return b, t


class Indeks:
    """Indeks posisi (baris, kalimat, klausa, penyangkal, isian kosong) untuk pencarian O(log n)."""

    def __init__(self, t):
        self.t = t
        self.nl = [m.start() for m in re.finditer("\n", t)]
        awal = [0]
        for m in AKHIR_KALIMAT.finditer(t):
            if t[m.start()] == ".":
                kata = re.search(r"([a-z]{1,4}(?:\.[a-z])?)$", t[max(0, m.start() - 6):m.start()])
                if kata and kata.group(1) in SINGKATAN:
                    continue
            awal.append(m.end())
        self.kalimat = awal
        klausa = set(awal)
        for m in KLAUSA.finditer(t):
            klausa.add(m.start())
        self.klausa = sorted(klausa)
        idiom = [(m.start(), m.end()) for m in IDIOM_MUNGKIN.finditer(t)]
        self.neg = [m.start() for m in NEGASI.finditer(t)
                    if not any(a <= m.start() < b for a, b in idiom[bisect.bisect_right(idiom, (m.start(), 10 ** 9)) - 1:][:1])]
        self.tanpa = [m.start() for m in TANPA.finditer(t)]
        # Kalimat yang memuat isian kosong ([isi: ...]) → bukti di kalimat ini hanya bernilai setengah
        self.kalimat_isian = set(self.awal_kalimat(m.start()) for m in PLACEHOLDER.finditer(t))

    def tandai_judul(self, teks_asli):
        """Judul markdown (# ...) hanya menunjukkan struktur, bukan isi: diperlakukan seperti kalimat berisian kosong."""
        for i, s in enumerate(teks_asli.splitlines(), 1):
            if s.lstrip().startswith("#"):
                awal = 0 if i == 1 else (self.nl[i - 2] + 1 if i - 2 < len(self.nl) else len(self.t))
                self.kalimat_isian.add(self.awal_kalimat(awal))

    def baris(self, pos):
        return bisect.bisect_right(self.nl, pos - 1) + 1 if pos > 0 else 1

    def awal_kalimat(self, pos):
        return self.kalimat[bisect.bisect_right(self.kalimat, pos) - 1]

    def akhir_kalimat(self, pos):
        i = bisect.bisect_right(self.kalimat, pos)
        return self.kalimat[i] if i < len(self.kalimat) else len(self.t)

    def jendela(self, m_awal, seluruh_klausa=False):
        k = self.klausa[bisect.bisect_right(self.klausa, m_awal) - 1]
        return k if seluruh_klausa else max(k, m_awal - JENDELA)

    @staticmethod
    def _hitung(daftar, a, b):
        return bisect.bisect_left(daftar, b) - bisect.bisect_left(daftar, a)

    def disangkal(self, m, seluruh_klausa=False):
        """True bila ada penyangkal di klausa sebelum/di dalam kecocokan.
        seluruh_klausa=True: seluruh klausa diperiksa (tanpa batas JENDELA karakter), untuk pola ekor kalimat
        seperti "kepada pihak mana pun" yang sering jauh dari kata "tidak" di awal kalimat."""
        return self._hitung(self.neg, self.jendela(m.start(), seluruh_klausa), m.end()) > 0

    def positif(self, m):
        """True bila polaritas positif: jumlah penyangkal (+ tanpa/without) genap.
        Dihitung pada klausa tempat kecocokan BERAKHIR (inti pernyataan), mis.
        "Jika terjadi kebocoran yang tidak disengaja, kami akan memberi tahu ..." = positif."""
        k = self.klausa[bisect.bisect_right(self.klausa, max(m.start(), m.end() - 1)) - 1]
        a = max(k, m.start() - JENDELA)
        return (self._hitung(self.neg, a, m.end()) + self._hitung(self.tanpa, a, m.end())) % 2 == 0


# ---------------------------------------------------------------------------
# Pemeriksaan
# ---------------------------------------------------------------------------
def cari_bukti(pola_re, idx, boleh_negatif=False):
    """Cari kecocokan berpolaritas positif. Kembalikan (bukti, di_baris_isian) atau (None, False).
    Kecocokan di baris tanpa isian kosong diutamakan."""
    cadangan = None
    for p in pola_re:
        for m in p.cari(idx.t, (lambda m: True) if boleh_negatif else idx.positif):
            if idx.awal_kalimat(m.start()) in idx.kalimat_isian:
                if cadangan is None:
                    cadangan = m.group(0)
                continue
            return m.group(0), False
    if cadangan is not None:
        return cadangan, True
    return None, False


def _kutipan(bersih, idx, m):
    a, b = idx.awal_kalimat(m.start()), idx.akhir_kalimat(m.start())
    s = bersih[a:b].replace(BATAS_BLOK, " ")
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > 160:
        rel = max(0, m.start() - a - 40)
        ujung = min(b, a + rel + 150)
        s = ("..." if rel else "") + re.sub(r"\s+", " ", bersih[a + rel:ujung].replace(BATAS_BLOK, " ")).strip() + ("..." if ujung < b else "")
    return s


def cari_risiko(bersih, idx):
    temuan = []
    per_kalimat = {}      # awal kalimat -> temuan (B-5: satu temuan per kalimat, tingkat tertinggi, alasan digabung)
    terpotong = False
    for r in RISIKO:
        n_pola = 0
        if not r["cek_negasi"]:
            terima = (lambda m: True)
        elif r.get("negasi_klausa"):
            terima = (lambda m: not idx.disangkal(m, seluruh_klausa=True))
        else:
            terima = (lambda m: not idx.disangkal(m))
        if r["perlu_re"] is not None:
            # hanya kalimat yang memuat kata wajib (cepat untuk teks besar)
            rentang = []
            for mp in r["perlu_re"].finditer(idx.t):
                a = idx.awal_kalimat(mp.start())
                if not rentang or rentang[-1][0] != a:
                    rentang.append((a, idx.akhir_kalimat(mp.start())))
            cocok = (m for a, b in rentang for m in r["re"].cari(idx.t, terima, a, b))
        else:
            cocok = r["re"].cari(idx.t, terima)
        for m in cocok:
            ak = idx.awal_kalimat(m.start())
            if r["syarat_re"] is not None and not r["syarat_re"].search(idx.t, ak, idx.akhir_kalimat(m.start())):
                continue
            lama = per_kalimat.get(ak)
            if lama is not None and r["alasan"] in lama["_alasan"] and (lama["tingkat"] == "TINGGI" or r["tingkat"] == "SEDANG"):
                continue
            if r["kecuali_re"] is not None:
                kal = idx.t[ak:idx.akhir_kalimat(m.start())]
                ok = False
                for mk in r["kecuali_re"].finditer(kal):
                    a = ak + mk.start()
                    # polaritas kata pengecualian di kalimat yang sama
                    neg = Indeks._hitung(idx.neg, max(ak, a - JENDELA), ak + mk.end()) + Indeks._hitung(idx.tanpa, max(ak, a - JENDELA), ak + mk.end())
                    if neg % 2 == 0:
                        ok = True
                        break
                if ok:
                    continue
            if lama is not None:
                _gabung(lama, r, m.group(0))
                continue
            n_pola += 1
            if n_pola > MAKS_TEMUAN_PER_POLA or len(temuan) >= MAKS_TEMUAN_TOTAL:
                terpotong = True
                break
            x = {"tingkat": r["tingkat"], "baris": idx.baris(m.start()), "kutipan": _kutipan(bersih, idx, m),
                 "cocok": m.group(0), "alasan": r["alasan"], "saran": r["saran"], "cocok_lain": [],
                 "_alasan": [r["alasan"]], "_saran": [r["saran"]]}
            per_kalimat[ak] = x
            temuan.append(x)
    for x in temuan:
        x["alasan"] = " Juga: ".join(x.pop("_alasan"))
        x["saran"] = " Juga: ".join(x.pop("_saran"))
    temuan.sort(key=lambda x: (0 if x["tingkat"] == "TINGGI" else 1, x["baris"]))
    return temuan, terpotong


def _gabung(x, r, cocok):
    """Gabungkan temuan kedua di kalimat yang sama: tingkat tertinggi dipakai, alasan & saran digabung."""
    if r["tingkat"] == "TINGGI" and x["tingkat"] != "TINGGI":
        x["cocok_lain"].append(x["cocok"])
        x["tingkat"], x["cocok"] = "TINGGI", cocok
        x["_alasan"].insert(0, r["alasan"])
        x["_saran"].insert(0, r["saran"])
    else:
        x["cocok_lain"].append(cocok)
        if r["alasan"] not in x["_alasan"]:
            x["_alasan"].append(r["alasan"])
        if r["saran"] not in x["_saran"]:
            x["_saran"].append(r["saran"])


def _unsur_json(u, status, nilai, bukti, kurang=None, belum=None, pemicu="", saran=""):
    """Semua unsur memakai kunci yang sama (B-8), agar konsumen JSON tidak terkena KeyError."""
    return {"id": u["id"], "label": u["label"], "status": status, "nilai": nilai, "bobot": u["bobot"],
            "bukti": bukti or "", "kurang": kurang or [], "belum_diisi": belum or [], "pemicu": pemicu or "",
            "bersyarat": "pemicu" in u, "dasar": u["dasar"], "saran": saran}


def periksa(teks):
    bersih, t = normalisasi(teks)
    idx = Indeks(t)
    if PLACEHOLDER.search(teks):
        idx.tandai_judul(teks)
    hasil = []
    total = dapat = dapat_struktur = 0.0
    for u in UNSUR:
        total += u["bobot"]
        if "sub" in u:
            nilai_sub, kurang, belum, bukti_sub = {}, [], [], []
            for k, pol in u["sub_re"].items():
                bukti, di_isian = cari_bukti(pol, idx)
                if bukti:
                    bukti_sub.append(bukti)
                nilai_sub[k] = 0.0 if not bukti else (0.5 if di_isian else 1.0)
                if not bukti:
                    kurang.append(k)
                elif di_isian:
                    belum.append(k)
            n = len(nilai_sub)
            nilai = u["bobot"] * sum(nilai_sub.values()) / n
            struktur = u["bobot"] * sum(1 for v in nilai_sub.values() if v) / n
            if not kurang and not belum:
                status = "ADA"
            elif not kurang and belum:
                status = "BELUM DIISI"
            else:
                status = "SEBAGIAN" if len(kurang) < n else "TIDAK ADA"
            hasil.append(_unsur_json(u, status, round(nilai, 2), "; ".join(bukti_sub), kurang=kurang, belum=belum,
                                     saran=u["saran"] if (kurang or belum) else ""))
        else:
            bukti, di_isian = cari_bukti(u["pola_re"], idx, u.get("boleh_negatif", False))
            nilai = 0 if not bukti else (u["bobot"] * (0.5 if di_isian else 1))
            struktur = u["bobot"] if bukti else 0
            status = "TIDAK ADA" if not bukti else ("BELUM DIISI" if di_isian else "ADA")
            saran = u["saran"] if not bukti else ("Lengkapi isian kosong di bagian ini." if di_isian else "")
            hasil.append(_unsur_json(u, status, nilai, bukti, saran=saran))
        dapat += nilai
        dapat_struktur += struktur
    for u in UNSUR_BERSYARAT:
        pemicu, _ = cari_bukti(u["pemicu_re"], idx)
        if not pemicu:
            continue
        total += u["bobot"]
        bukti, di_isian = cari_bukti(u["pola_re"], idx)
        nilai = 0 if not bukti else (u["bobot"] * (0.5 if di_isian else 1))
        dapat += nilai
        dapat_struktur += u["bobot"] if bukti else 0
        status = "TIDAK ADA" if not bukti else ("BELUM DIISI" if di_isian else "ADA")
        hasil.append(_unsur_json(u, status, nilai, bukti, pemicu=pemicu,
                                 saran=u["saran"] if not bukti else ("Lengkapi isian kosong di bagian ini." if di_isian else "")))

    skor = int(round(100.0 * dapat / total)) if total else 0
    skor_struktur = int(round(100.0 * dapat_struktur / total)) if total else 0
    isian = PLACEHOLDER.findall(teks)
    if isian:
        skor = min(skor, BATAS_SKOR_ISIAN)   # dokumen berisian kosong tidak pernah tampil "hampir sempurna"
    risiko, terpotong = cari_risiko(bersih, idx)
    n_tinggi = sum(1 for r in risiko if r["tingkat"] == "TINGGI")
    # Urutan status: KURANG LENGKAP > PERLU PERBAIKAN (frasa TINGGI) > BELUM SIAP (isian kosong) > PERLU PERBAIKAN > CUKUP LENGKAP
    if skor < 60 and not (isian and skor_struktur >= 60 and not n_tinggi):
        status, alasan_status = "KURANG LENGKAP", URUTAN_STATUS[0]
    elif n_tinggi:
        status, alasan_status = "PERLU PERBAIKAN", URUTAN_STATUS[1]
    elif isian:
        status, alasan_status = "BELUM SIAP", URUTAN_STATUS[2]
    elif skor < 85:
        status, alasan_status = "PERLU PERBAIKAN", URUTAN_STATUS[3]
    else:
        status, alasan_status = "CUKUP LENGKAP", URUTAN_STATUS[4]

    catatan = []
    jumlah_kata = len(re.findall(r"\w+", t))
    if jumlah_kata < 150:
        catatan.append("Teks sangat pendek ({} kata). Kebijakan privasi yang memadai biasanya > 400 kata.".format(jumlah_kata))
    if isian:
        catatan.append("Masih ada {} isian kosong (mis. {}). Skor sekarang {}/100; bila semua diisi, skor struktur {}/100. "
                       "Lengkapi sebelum dipublikasikan.".format(len(isian), isian[0], skor, skor_struktur))
    tln = next((h for h in hasil if h["id"] == "transfer_ln"), None)
    m_ln = LAYANAN_LN.search(bersih)
    if tln and tln["status"] == "TIDAK ADA" and m_ln:
        catatan.append("Teks menyebut layanan '{}' yang umumnya menyimpan data di luar Indonesia; jelaskan transfer ke luar negeri (Pasal 56).".format(m_ln.group(0)))
    if not re.search(r"pejabat pelindungan data|petugas pelindungan data|\bppdp\b|\bdpo\b|data protection officer", t):
        catatan.append("Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.")
    if terpotong:
        catatan.append("Frasa berisiko sangat banyak; hanya {} temuan pertama yang ditampilkan (maks. {} per pola).".format(len(risiko), MAKS_TEMUAN_PER_POLA))

    return {
        "versi_pemeriksa": VERSI,
        "skor": skor,
        "skor_struktur": skor_struktur,
        "status": status,
        "alasan_status": alasan_status.split(" — ", 1)[1],
        "jumlah_kata": jumlah_kata,
        "isian_kosong": len(isian),
        "unsur": hasil,
        "risiko": risiko,
        "pesan_risiko": PESAN_RISIKO_ADA if risiko else PESAN_RISIKO_KOSONG,
        "risiko_kosong_bukan_jaminan_aman": True,
        "catatan": catatan,
        "peringatan": ("Pemeriksa bantu berbasis kata kunci & polaritas kalimat, bukan pemeriksa hukum. Kata kunci yang ditemukan "
                       "belum tentu isinya memadai, dan kata kunci yang tidak ditemukan belum tentu berarti aman. "
                       "Penilaian risiko wajib lewat pembacaan manual (references/kategori-risiko-cek.md)."),
    }


def cetak_teks(r, nama):
    out = []
    out.append("PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — {}".format(nama))
    kepala = "Skor kelengkapan: {}/100".format(r["skor"])
    if r["isian_kosong"]:
        kepala += " (struktur {}/100 bila {} isian kosong dilengkapi)".format(r["skor_struktur"], r["isian_kosong"])
    out.append("{}  |  Status: {}  |  {} kata".format(kepala, r["status"], r["jumlah_kata"]))
    out.append("Arti status: " + r["alasan_status"])
    out.append("")
    out.append("UNSUR:")
    for h in r["unsur"]:
        tanda = {"ADA": "[v]", "SEBAGIAN": "[~]", "BELUM DIISI": "[?]", "TIDAK ADA": "[ ]"}[h["status"]]
        baris = "  {} {} — {}".format(tanda, h["label"], h["status"])
        if h.get("kurang"):
            baris += " (kurang: {})".format(", ".join(k.replace("_", " ") for k in h["kurang"]))
        if h.get("belum_diisi"):
            baris += " (belum diisi: {})".format(", ".join(k.replace("_", " ") for k in h["belum_diisi"]))
        out.append(baris)
    kurang = [h for h in r["unsur"] if h["status"] != "ADA"]
    if kurang:
        out.append("")
        out.append("YANG PERLU DITAMBAHKAN / DILENGKAPI:")
        for i, h in enumerate(kurang, 1):
            out.append("  {}. {} — {} [{}]".format(i, h["label"], h["saran"], h["dasar"]))
    out.append("")
    if r["risiko"]:
        out.append("FRASA BERISIKO (penanda awal dari pola kata kunci):")
        for x in r["risiko"]:
            out.append("  - [{}] baris {}: \"{}\"".format(x["tingkat"], x["baris"], x["kutipan"]))
            out.append("      Alasan: {}".format(x["alasan"]))
            out.append("      Saran : {}".format(x["saran"]))
        out.append("  ! " + r["pesan_risiko"])
    else:
        out.append("FRASA BERISIKO (pola kata kunci): tidak ada pola yang cocok.")
        out.append("  ! " + r["pesan_risiko"])
    if r["catatan"]:
        out.append("")
        out.append("CATATAN:")
        for c in r["catatan"]:
            out.append("  - " + c)
    out.append("")
    out.append("⚠ " + r["peringatan"])
    return "\n".join(out)


def cetak_daftar():
    out = ["Pemeriksa kebijakan privasi v{}".format(VERSI), "Unsur yang diperiksa (bobot):"]
    for u in UNSUR:
        out.append("  - {} ({}) — {}".format(u["label"], u["bobot"], u["dasar"]))
    out.append("Unsur bersyarat (hanya bila teks menyebut hal terkait):")
    for u in UNSUR_BERSYARAT:
        out.append("  - {} ({}) — {}".format(u["label"], u["bobot"], u["dasar"]))
    out.append("Frasa berisiko yang dideteksi: {} pola (ID & EN), dengan cek negasi per klausa.".format(len(RISIKO)))
    out.append("Status (diperiksa berurutan, yang pertama cocok dipakai):")
    for s in URUTAN_STATUS:
        out.append("  " + s)
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Periksa kelengkapan Kebijakan Privasi terhadap UU 27/2022 (PDP).")
    ap.add_argument("file", nargs="?", help="File .md/.txt/.html berisi kebijakan privasi")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    ap.add_argument("--daftar", action="store_true", help="Tampilkan daftar unsur yang diperiksa")
    ap.add_argument("--ketat", action="store_true", help="Keluar dengan kode 1 bila status bukan CUKUP LENGKAP")
    args = ap.parse_args(argv)

    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    if args.daftar:
        print(cetak_daftar())
        return 0
    try:
        teks = baca_teks(args.file)
    except GalatInput as e:
        if args.format == "json":
            print(json.dumps({"galat": str(e)}, ensure_ascii=False))
        else:
            print("GALAT: {}".format(e), file=sys.stderr)
        return 2
    r = periksa(teks)
    if args.format == "json":
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(cetak_teks(r, os.path.basename(args.file)))
    if args.ketat and r["status"] != "CUKUP LENGKAP":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
