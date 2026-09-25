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

Cara kerja singkat (v1.0.1):
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
   maks. 84 selama masih ada isian, dan status dokumen = BELUM SIAP. "skor_struktur" = skor bila semua diisi.
"""
import argparse
import bisect
import html
import json
import os
import re
import sys
import unicodedata

VERSI = "1.0.1"
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
OBJEK_EN = r"(?:data|information|info|details|database)"
NEGARA = (r"(?:singapura|singapore|amerika( serikat)?|united states|\busa?\b|eropa|europe|uni eropa|jepang|japan|malaysia|"
          r"australia|irlandia|ireland|india|hong ?kong|tiongkok|china|korea|taiwan|jerman|germany|belanda|netherlands|"
          r"inggris|united kingdom|finlandia|finland|swedia|sweden|kanada|canada|brasil|brazil)")
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
                 r"(kebijakan|pemberitahuan)( privasi)?( ini)? (berlaku|dibuat|diterbitkan) (untuk|bagi|oleh)",
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
        "pola": [r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", r"\bwhatsapp\b|\bwa\b", r"(telepon|telp|nomor hp|no\. hp)",
                 r"(\+62|\b0)8\d{1,3}[- ]?\d{3,4}[- ]?\d{3,5}",
                 r"hubungi kami", r"contact us", r"\bemail\b|\be-mail\b|\bsurel\b", r"alamat (kantor|usaha|toko|klinik)"],
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
                 r"digunakan untuk", r"untuk keperluan", r"\bpurposes?\b", r"we use (your )?(personal )?(data|information)"],
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
                 r"(server|pusat data|data center|disimpan|diproses|hosting|di-?hosting|stored|hosted|processed)[^.\n]{0,60}" + NEGARA,
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
        "pola": [r"keamanan (data|informasi)", r"mengamankan|melindungi data", r"enkripsi|terenkripsi|tersandi|kata sandi|autentikasi|verifikasi (dua|2) langkah",
                 r"akses (terbatas|dibatasi)", r"membatasi akses|pembatasan akses", r"\bhttps\b|\bssl\b|\btls\b",
                 r"\bsecurity\b|\bsecure\b|encrypt|safeguard", r"protect your"],
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
              r"|(dapat|akan|boleh|bisa) kami (jual|sewakan|perjualbelikan|perdagangkan|monetisasi|tukar)\b",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"(mengalihkan|membagikan|memberikan|menyerahkan|mengungkapkan|meneruskan|mentransfer|menukar(kan)?)[^.;\n]{0,80}?"
              r"(dengan|untuk|sebagai|demi) (imbalan|bayaran|kompensasi|uang|keuntungan)",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"(?:(?:share|disclose|transfer|provide)" + SAMBUNG + r" )*\b" + V_JUAL_EN + r"\b(?:" + SAMBUNG + r" (?:" + V_JUAL_EN[3:-1] + r"|share|disclose))*"
              r"(?: (?:your|the|all|any|such|our|customer|customers'|user|users'))*(?: personal)? " + OBJEK_EN,
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"\b" + OBJEK_EN + r"\b[^.;\n]{0,40}?\b(sold|rented|leased|traded|monetized|monetised)\b",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"(share|disclose|provide|transfer|give)[^.;\n]{0,80}?(for (payment|money|compensation|a fee|profit|monetary)|in exchange for|to data brokers)",
         tingkat="TINGGI", alasan=_JUAL_ALASAN, saran=_JUAL_SARAN, cek_negasi=True),
    dict(pola=r"(share|disclose|provide|transfer)[^.;\n]{0,80}?(third[- ]part(y|ies)|partners|advertisers)[^.;\n]{0,60}?for (their )?(own )?(marketing|advertising|promotional)"
              r"|(membagikan|mengungkapkan|memberikan|menyerahkan|meneruskan)[^.;\n]{0,80}?(pihak ketiga|mitra|pengiklan)[^.;\n]{0,60}?untuk (keperluan |tujuan |kepentingan )?(pemasaran|promosi|iklan)",
         tingkat="SEDANG", alasan="Memberikan data ke pihak lain untuk pemasaran MEREKA memerlukan persetujuan eksplisit per tujuan (Pasal 20 ayat (2) huruf a & Pasal 22) dan penerima yang jelas (Pasal 16 ayat (2)).",
         saran="Sebut penerima & tujuannya, dan lakukan hanya dengan persetujuan aktif yang bisa ditolak.", cek_negasi=True,
         kecuali=r"persetujuan|setuju|consent|opt-?in"),
    # --- persetujuan dianggap / tidak bisa ditarik ---
    dict(pola=r"persetujuan[^.;\n]{0,30}?dianggap (telah )?(diberikan|ada|sah)", tingkat="TINGGI", alasan=_DIANGGAP_ALASAN,
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
    dict(pola=r"(mengubah|memperbarui|merevisi|diubah|diperbarui|berubah|perubahan)[^.;\n]{0,80}?tanpa (pemberitahuan|memberi ?tahu|diberitahukan)"
              r"|(change|modify|update|amend)[^.;\n]{0,60}?without (prior |any )?(notice|notification|informing)",
         tingkat="SEDANG", alasan=_UBAH_ALASAN, saran=_UBAH_SARAN, cek_negasi=True),
    dict(pola=r"(kebijakan|ketentuan|syarat|policy|terms)[^.;\n]{0,60}?(diubah|diperbarui|berubah|direvisi|mengubah|memperbarui|merevisi|changed|modified|updated|amended|change|modify|update|amend)"
              r"[^.;\n]{0,40}?(sewaktu-? ?waktu|kapan saja|kapan pun|setiap saat|at any time|from time to time)"
              r"|(mengubah|memperbarui|merevisi|change|modify|update|amend) (kebijakan|ketentuan|syarat|this policy|these terms|our policy)[^.;\n]{0,40}?"
              r"(sewaktu-? ?waktu|kapan saja|kapan pun|setiap saat|at any time|from time to time)",
         tingkat="SEDANG", alasan=_UBAH_ALASAN, saran=_UBAH_SARAN, cek_negasi=True,
         kecuali=BERITAHU_ID + "|" + BERITAHU_EN),
    dict(pola=r"(kepada|dengan) (siapa ?pun|pihak mana ?pun|semua pihak|pihak ketiga mana ?pun)|with any(one| third part(y|ies))",
         tingkat="SEDANG", alasan="Berbagi data tanpa batas penerima & tujuan tidak memenuhi prinsip terbatas dan spesifik (Pasal 16 ayat (2)).",
         saran="Sebutkan penerima secara spesifik (kategori + tujuan).", cek_negasi=True),
    dict(pola=r"(semua|seluruh|segala) (data|informasi)[^.\n]{0,30}(di|pada) (perangkat|ponsel|hp|galeri|kontak) anda|all (data|information) on your device",
         tingkat="SEDANG", alasan="Mengumpulkan melebihi keperluan melanggar prinsip minimisasi (Pasal 16 ayat (2) huruf a).",
         saran="Batasi ke data yang benar-benar diperlukan.", cek_negasi=True),
    dict(pola=r"\bgdpr\b|\bccpa\b|california|general data protection regulation|european economic area|uni eropa",
         tingkat="SEDANG", alasan="Tampaknya disalin dari kebijakan luar negeri (GDPR/CCPA). Hak & kewajiban di Indonesia mengikuti UU 27/2022.",
         saran="Tulis ulang dengan rujukan UU 27/2022 (batas 3×24 jam, pemberitahuan kebocoran, dasar pemrosesan Pasal 20).", cek_negasi=False),
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
TANPA = re.compile(r"\b(?:tanpa|without)\b")
KLAUSA = re.compile(
    r"[;:]|\s[-–—]\s|,?\s+(?:tetapi|tapi|namun|melainkan|sedangkan|padahal|but|however|whereas|although|meskipun|walaupun)\b"
    r"|,\s*(?:dan |and |serta |lalu |kemudian |then )?(?:kami|we|anda|you|data|informasi|information|mereka|they|pihak)\b"
    r"|\s(?:dan|and) (?:kami|we)\b")
AKHIR_KALIMAT = re.compile(r"\n|\x1e|[.!?]+(?=\s|$)")
SINGKATAN = {"jl", "no", "pt", "cv", "ud", "tbk", "dll", "dsb", "mis", "dr", "drg", "sdr", "bpk", "hlm", "tgl", "telp",
             "e.g", "i.e", "etc", "vs", "mr", "mrs", "ms", "ps", "ay", "ir", "prof", "kec", "kab", "kel", "rt", "rw"}
BATAS_SKOR_ISIAN = 84   # skor maksimum selama masih ada isian kosong (di bawah ambang CUKUP LENGKAP 85)
JENDELA = 60   # karakter maksimum sebelum kecocokan yang diperiksa untuk penyangkal

PLACEHOLDER = re.compile(r"\[(?:isi|fill)\s*:[^\]\n]*\]|\[(?:isi|fill)\]|\[\[[^\]\n]*\]\]|\[\.\.\.\]|\{jika[^}\n]*\}|\{if[^}\n]*\}|lorem ipsum|\bxxx+\b", re.I)

# Layanan pihak ketiga yang umumnya menyimpan data di luar Indonesia (pemicu saran transfer_ln)
LAYANAN_LN = re.compile(r"google|gmail|drive|meta|facebook|instagram|whatsapp|tiktok|shopify|aws|amazon web|cloudflare|mailchimp|zoom|openai|chatgpt|claude|dropbox|microsoft|notion", re.I)

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

    def cari(self, t, terima):
        """Seperti finditer, tetapi bila kecocokan ditolak (`terima(m)` False, mis. disangkal),
        pencarian diulang dari karakter berikutnya agar kecocokan lebih pendek di dalamnya tetap ditemukan
        ("Kami tidak menyimpan data kartu, dan data pesanan disimpan selamanya")."""
        if self.awalan is not None and not any(a in t for a in self.awalan):
            return
        pos = 0
        n = len(t)
        while pos <= n:
            m = self.re.search(t, pos)
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
        self.neg = [m.start() for m in NEGASI.finditer(t)]
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

    def jendela(self, m_awal):
        k = self.klausa[bisect.bisect_right(self.klausa, m_awal) - 1]
        return max(k, m_awal - JENDELA)

    @staticmethod
    def _hitung(daftar, a, b):
        return bisect.bisect_left(daftar, b) - bisect.bisect_left(daftar, a)

    def disangkal(self, m):
        """True bila ada penyangkal di klausa sebelum/di dalam kecocokan."""
        return self._hitung(self.neg, self.jendela(m.start()), m.end()) > 0

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
    sudah = set()
    terpotong = False
    for r in RISIKO:
        n_pola = 0
        terima = (lambda m: not idx.disangkal(m)) if r["cek_negasi"] else (lambda m: True)
        for m in r["re"].cari(idx.t, terima):
            ak = idx.awal_kalimat(m.start())
            kunci = (ak, r["tingkat"])
            if kunci in sudah:
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
            sudah.add(kunci)
            n_pola += 1
            if n_pola > MAKS_TEMUAN_PER_POLA or len(temuan) >= MAKS_TEMUAN_TOTAL:
                terpotong = True
                break
            temuan.append({"tingkat": r["tingkat"], "baris": idx.baris(m.start()), "kutipan": _kutipan(bersih, idx, m),
                           "cocok": m.group(0), "alasan": r["alasan"], "saran": r["saran"]})
    temuan.sort(key=lambda x: (0 if x["tingkat"] == "TINGGI" else 1, x["baris"]))
    return temuan, terpotong


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
            nilai_sub, kurang, belum = {}, [], []
            for k, pol in u["sub_re"].items():
                bukti, di_isian = cari_bukti(pol, idx)
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
            hasil.append({"id": u["id"], "label": u["label"], "status": status, "nilai": round(nilai, 2), "bobot": u["bobot"],
                          "kurang": kurang, "belum_diisi": belum, "dasar": u["dasar"], "saran": u["saran"] if (kurang or belum) else ""})
        else:
            bukti, di_isian = cari_bukti(u["pola_re"], idx, u.get("boleh_negatif", False))
            nilai = 0 if not bukti else (u["bobot"] * (0.5 if di_isian else 1))
            struktur = u["bobot"] if bukti else 0
            status = "TIDAK ADA" if not bukti else ("BELUM DIISI" if di_isian else "ADA")
            saran = u["saran"] if not bukti else ("Lengkapi isian kosong di bagian ini." if di_isian else "")
            hasil.append({"id": u["id"], "label": u["label"], "status": status, "nilai": nilai, "bobot": u["bobot"],
                          "bukti": bukti or "", "dasar": u["dasar"], "saran": saran})
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
        hasil.append({"id": u["id"], "label": u["label"], "status": status, "nilai": nilai, "bobot": u["bobot"],
                      "bukti": bukti or "", "pemicu": pemicu, "dasar": u["dasar"],
                      "saran": u["saran"] if not bukti else ("Lengkapi isian kosong di bagian ini." if di_isian else "")})

    skor = int(round(100.0 * dapat / total)) if total else 0
    skor_struktur = int(round(100.0 * dapat_struktur / total)) if total else 0
    isian = PLACEHOLDER.findall(teks)
    if isian:
        skor = min(skor, BATAS_SKOR_ISIAN)   # dokumen berisian kosong tidak pernah tampil "hampir sempurna"
    risiko, terpotong = cari_risiko(bersih, idx)
    n_tinggi = sum(1 for r in risiko if r["tingkat"] == "TINGGI")
    # Urutan status: KURANG LENGKAP > PERLU PERBAIKAN (frasa TINGGI) > BELUM SIAP (isian kosong) > PERLU PERBAIKAN > CUKUP LENGKAP
    if skor < 60 and not (isian and skor_struktur >= 60 and not n_tinggi):
        status = "KURANG LENGKAP"
    elif n_tinggi:
        status = "PERLU PERBAIKAN"
    elif isian:
        status = "BELUM SIAP"
    elif skor < 85:
        status = "PERLU PERBAIKAN"
    else:
        status = "CUKUP LENGKAP"

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
        "jumlah_kata": jumlah_kata,
        "isian_kosong": len(isian),
        "unsur": hasil,
        "risiko": risiko,
        "catatan": catatan,
        "peringatan": "Pemeriksa bantu berbasis kata kunci & polaritas kalimat, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.",
    }


def cetak_teks(r, nama):
    out = []
    out.append("PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — {}".format(nama))
    kepala = "Skor kelengkapan: {}/100".format(r["skor"])
    if r["isian_kosong"]:
        kepala += " (struktur {}/100 bila {} isian kosong dilengkapi)".format(r["skor_struktur"], r["isian_kosong"])
    out.append("{}  |  Status: {}  |  {} kata".format(kepala, r["status"], r["jumlah_kata"]))
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
        out.append("FRASA BERISIKO:")
        for x in r["risiko"]:
            out.append("  - [{}] baris {}: \"{}\"".format(x["tingkat"], x["baris"], x["kutipan"]))
            out.append("      Alasan: {}".format(x["alasan"]))
            out.append("      Saran : {}".format(x["saran"]))
    else:
        out.append("FRASA BERISIKO: tidak ditemukan.")
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
    out.append("Status: CUKUP LENGKAP (skor >= 85, tanpa frasa TINGGI, tanpa isian kosong) · BELUM SIAP (ada [isi: ...]) · "
               "PERLU PERBAIKAN (skor 60-84 atau ada frasa TINGGI) · KURANG LENGKAP (skor < 60).")
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
