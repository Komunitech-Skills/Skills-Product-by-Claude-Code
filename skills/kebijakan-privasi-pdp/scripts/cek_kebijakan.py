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

Ini pemeriksa BANTU berbasis kata kunci (ID & EN), bukan penilaian hukum.
Kata kunci yang ditemukan belum tentu berarti isinya benar/memadai.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

VERSI = "1.0.0"

# ---------------------------------------------------------------------------
# Unsur wajib/pokok. Tiap unsur: id, label, bobot, pola (regex, huruf kecil), dasar, saran.
# ---------------------------------------------------------------------------
UNSUR = [
    {
        "id": "identitas",
        "label": "Identitas pengendali data (nama usaha/pemilik)",
        "bobot": 1,
        "pola": [r"pengendali data", r"data controller", r"(kebijakan|pemberitahuan) privasi (ini )?(berlaku|dibuat|diterbitkan) (untuk|oleh)",
                 r"(dikelola|dioperasikan|dimiliki) oleh", r"(operated|owned|managed) by", r"\bkami adalah\b", r"\bwe are\b",
                 r"\b(pt|cv|ud)\.? [a-z]", r"nama usaha", r"tentang kami", r"about us"],
        "dasar": "UU 27/2022 Pasal 21 & 31 (pengendali wajib jelas identitasnya)",
        "saran": "Sebutkan nama usaha/badan usaha dan nama pemilik atau penanggung jawab sebagai pengendali data.",
    },
    {
        "id": "kontak",
        "label": "Kontak yang bisa dihubungi (email/WA/alamat)",
        "bobot": 1,
        "pola": [r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", r"\bwhatsapp\b|\bwa\b", r"(telepon|telp|nomor hp|no\. hp)",
                 r"hubungi kami", r"contact us", r"\bemail\b|\be-mail\b|\bsurel\b", r"alamat (kantor|usaha|toko)"],
        "dasar": "UU 27/2022 Pasal 21 & 46 ayat (2) (narahubung)",
        "saran": "Cantumkan email dan/atau nomor WhatsApp khusus urusan data pribadi, plus alamat usaha.",
    },
    {
        "id": "jenis_data",
        "label": "Jenis data pribadi yang dikumpulkan",
        "bobot": 1,
        "pola": [r"data (pribadi )?yang (kami )?(kumpulkan|kami kumpulkan|dikumpulkan|diproses|kami proses)",
                 r"jenis data", r"informasi yang (kami )?(kumpulkan|dikumpulkan)", r"(data|information) (we|that we) (collect|process)",
                 r"personal data we", r"types? of (personal )?data", r"(nama|name)[^.\n]{0,40}(nomor|alamat|email|phone|address)"],
        "dasar": "UU 27/2022 Pasal 21 ayat (1) huruf c & e",
        "saran": "Tulis daftar data yang dikumpulkan (mis. nama, nomor WA, alamat kirim, riwayat pesanan).",
    },
    {
        "id": "tujuan",
        "label": "Tujuan pemrosesan",
        "bobot": 1,
        "pola": [r"tujuan (pemrosesan|pengumpulan|penggunaan)", r"\btujuan\b[ ,]+(dan )?dasar", r"\buntuk apa\b", r"(dipakai|dipergunakan) untuk", r"(kami )?(gunakan|menggunakan|memakai) (data|informasi)[^.\n]{0,40}untuk",
                 r"digunakan untuk", r"untuk keperluan", r"\bpurposes?\b", r"we use (your )?(personal )?(data|information)"],
        "dasar": "UU 27/2022 Pasal 16 ayat (2) huruf b & Pasal 21 ayat (1) huruf b",
        "saran": "Jelaskan untuk apa setiap data dipakai (proses pesanan, pengiriman, layanan pelanggan, promosi bila setuju).",
    },
    {
        "id": "dasar_pemrosesan",
        "label": "Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.)",
        "bobot": 1,
        "pola": [r"dasar (hukum )?(pemrosesan|pengolahan)", r"pasal 20", r"legal basis", r"lawful basis",
                 r"kepentingan (yang )?sah", r"legitimate interest", r"(pemenuhan )?kewajiban (perjanjian|hukum)",
                 r"performance of (a )?contract", r"legal obligation", r"legalitas (dari )?pemrosesan"],
        "dasar": "UU 27/2022 Pasal 20 ayat (2) & Pasal 21 ayat (1) huruf a",
        "saran": "Sebutkan dasar pemrosesan per tujuan: persetujuan, pelaksanaan perjanjian/pesanan, kewajiban hukum (mis. pajak), atau kepentingan yang sah.",
    },
    {
        "id": "penerima",
        "label": "Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan)",
        "bobot": 1,
        "pola": [r"pihak ketiga", r"third[- ]part", r"(kami )?(bagikan|membagikan|berbagi|meneruskan|mengungkapkan)",
                 r"kurir|ekspedisi|jasa (pengiriman|kirim)", r"payment gateway|penyedia (layanan )?pembayaran",
                 r"prosesor data", r"service providers?", r"penyedia (layanan|jasa)", r"(we )?share (your )?(personal )?(data|information)",
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
                 r"pasal 56"],
        "dasar": "UU 27/2022 Pasal 56",
        "saran": "Jelaskan apakah data disimpan/diproses di luar Indonesia (mis. Google Drive, Meta/WhatsApp, layanan cloud) dan pelindungannya.",
    },
    {
        "id": "masa_simpan",
        "label": "Masa simpan (retensi) data",
        "bobot": 1,
        "pola": [r"(masa|jangka waktu|lama) (simpan|penyimpanan|retensi)", r"disimpan (selama|paling lama|sampai|hingga)",
                 r"(kami )?simpan (selama|paling lama|sampai|hingga)", r"\bretensi\b", r"\bretention\b", r"\bretain(ed)?\b",
                 r"(kept|stored) (for|until)", r"how long we (keep|store)"],
        "dasar": "UU 27/2022 Pasal 21 ayat (1) huruf d & f, Pasal 43–44",
        "saran": "Tulis berapa lama data disimpan per jenis (mis. data pesanan 10 tahun untuk pembukuan pajak, chat CS 1 tahun) lalu dihapus.",
    },
    {
        "id": "hak_subjek",
        "label": "Hak subjek data (akses, koreksi, hapus, tarik persetujuan)",
        "bobot": 2,
        "sub": {
            "akses": [r"(meng)?akses (ke |terhadap |atas )?data", r"hak (untuk )?(mengakses|akses)", r"salinan data", r"access (to )?your",
                      r"right (of|to) access", r"copy of your"],
            "koreksi": [r"memperbaiki|perbaikan|koreksi|memperbarui|pembaruan|melengkapi", r"correct|rectif|update your"],
            "hapus": [r"menghapus|penghapusan|dihapus|pemusnahan|memusnahkan", r"delet|eras"],
            "tarik_persetujuan": [r"menarik (kembali )?persetujuan|penarikan (kembali )?persetujuan|tarik persetujuan",
                                  r"withdraw(al of)? (your )?consent"],
        },
        "dasar": "UU 27/2022 Pasal 5–13 & Pasal 21 ayat (1) huruf g",
        "saran": "Tuliskan hak-hak berikut dengan bahasa sederhana: mengakses & minta salinan, memperbaiki, menghapus, menarik persetujuan (juga: keberatan atas keputusan otomatis, membatasi pemrosesan, gugat ganti rugi).",
    },
    {
        "id": "cara_ajukan",
        "label": "Cara mengajukan permintaan hak & batas waktu tanggapan",
        "bobot": 1,
        "pola": [r"(ajukan|mengajukan|kirim(kan)?|sampaikan) (permintaan|permohonan)", r"cara (mengajukan|menggunakan hak)",
                 r"hubungi kami (melalui|di|lewat|untuk)", r"3 ?(x|×) ?24 jam", r"(submit|send|make) (a |your )?request",
                 r"exercise (your|these|any of these) rights", r"72 (jam|hours)"],
        "dasar": "UU 27/2022 Pasal 30, 32, 40 (tanggapan paling lambat 3×24 jam)",
        "saran": "Tulis cara mengajukan (email/WA mana, data apa yang perlu disertakan) dan janji tanggapan paling lambat 3×24 jam.",
    },
    {
        "id": "keamanan",
        "label": "Langkah keamanan data",
        "bobot": 1,
        "pola": [r"keamanan (data|informasi)", r"mengamankan|melindungi data", r"enkripsi|terenkripsi|kata sandi|autentikasi",
                 r"akses (terbatas|dibatasi)", r"\bsecurity\b|\bsecure\b|encrypt|safeguard", r"protect your"],
        "dasar": "UU 27/2022 Pasal 35–39",
        "saran": "Jelaskan langkah keamanan secara jujur dan umum (akses dibatasi, kata sandi + verifikasi 2 langkah, perangkat terkunci, cadangan).",
    },
    {
        "id": "kebocoran",
        "label": "Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data)",
        "bobot": 1,
        "pola": [r"(kegagalan pelindungan|kebocoran|insiden|bocor)[^.\n]{0,160}(beri ?tahu|memberitahu|memberi tahu|pemberitahuan|umumkan|laporkan)",
                 r"(beri ?tahu|memberitahu|memberi tahu|pemberitahuan)[^.\n]{0,160}(kegagalan pelindungan|kebocoran|insiden)",
                 r"(breach|security incident)[^.\n]{0,160}(notify|inform|notification)", r"(notify|inform)[^.\n]{0,160}(breach|incident)",
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
        "pola": [r"(perubahan|mengubah|memperbarui|diubah|diperbarui|berubah)[^.\n]{0,120}(beri ?tahu|memberitahu|memberi tahu|pemberitahuan|umumkan|mengumumkan|informasikan)",
                 r"(beri ?tahu|memberitahu|umumkan|mengumumkan|informasikan)[^.\n]{0,80}(perubahan|diubah|diperbarui)",
                 r"(change|update|amend)[^.\n]{0,120}(notify|announce|inform|notice before)", r"(notify|announce|inform)[^.\n]{0,60}(change|update)"],
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
        "pemicu": [r"\banak\b", r"di bawah umur", r"belum dewasa", r"\bsiswa\b|\bmurid\b|\bbalita\b|\bbayi\b",
                   r"\bchild(ren)?\b", r"\bminors?\b", r"under (the age of )?1[3-8]"],
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

# Frasa berisiko. (pola, tingkat, alasan, saran, cek_negasi)
RISIKO = [
    (r"tidak (akan )?bertanggung ?jawab (atas|terhadap) (segala |setiap |semua )?(bentuk )?(kebocoran|kehilangan|penyalahgunaan|kerugian|akses)",
     "TINGGI", "Pengendali tetap bertanggung jawab atas pemrosesan & wajib melindungi data (Pasal 35, 46, 47). Klausul lepas tanggung jawab tidak menghapus kewajiban ini dan merusak kepercayaan.",
     "Hapus. Ganti dengan komitmen menjaga keamanan dan memberi tahu paling lambat 3×24 jam bila terjadi kebocoran.", False),
    (r"(not|no) (be )?(held )?(responsible|liable) for (any )?(data )?(breach|leak|loss|misuse|unauthori)",
     "TINGGI", "Klausul lepas tanggung jawab atas kebocoran bertentangan dengan kewajiban pengendali (Pasal 35, 46, 47).",
     "Remove; commit to safeguards and 3×24-hour breach notification.", False),
    (r"(dapat|boleh|berhak|akan|bisa) (menjual|memperjualbelikan|menyewakan)", "TINGGI",
     "Mengungkapkan/menggunakan data pribadi orang lain secara melawan hukum dilarang (Pasal 65 ayat (2)-(3)) dan diancam pidana (Pasal 67). Menjual data hampir pasti tidak punya dasar pemrosesan yang sah (Pasal 20).",
     "Hapus. Tegaskan: \"Kami tidak menjual data pribadi Anda.\"", True),
    (r"data[^.\n]{0,40}(dapat|boleh|akan|bisa) dijual", "TINGGI",
     "Mengungkapkan/menggunakan data pribadi secara melawan hukum dilarang (Pasal 65) dan diancam pidana (Pasal 67).", "Hapus. Tegaskan: \"Kami tidak menjual data pribadi Anda.\"", True),
    (r"(may|can|will) (sell|rent|trade) (your )?(personal )?(data|information)", "TINGGI",
     "Unlawful disclosure/use of personal data is prohibited (Art. 65) and criminally sanctioned (Art. 67) under Law 27/2022.", "Remove; state \"We do not sell your personal data.\"", True),
    (r"persetujuan[^.\n]{0,30}dianggap (telah )?(diberikan|ada)", "TINGGI",
     "Persetujuan harus eksplisit, tertulis/terekam, untuk tujuan tertentu (Pasal 20 ayat (2) huruf a & Pasal 22). Persetujuan 'dianggap' tidak memenuhi.",
     "Ganti dengan kotak centang/balasan \"SETUJU\" yang aktif dari pelanggan, per tujuan.", False),
    (r"dianggap (telah )?(menyetujui|setuju|memberikan persetujuan)", "TINGGI",
     "Persetujuan diam-diam/dianggap tidak memenuhi syarat persetujuan eksplisit (Pasal 20 & 22).",
     "Minta persetujuan aktif (centang/ketik SETUJU), dan untuk pemrosesan wajib (pesanan) gunakan dasar 'pelaksanaan perjanjian'.", False),
    (r"(deemed|assumed|considered) to (have )?(consent|agree|accept)", "TINGGI",
     "Deemed consent does not meet the explicit-consent requirement (Art. 20 & 22).", "Use active opt-in consent per purpose.", False),
    (r"persetujuan[^.\n]{0,40}tidak (dapat|bisa) (ditarik|dicabut|dibatalkan)|(consent|agreement) (is )?(irrevocable|cannot be withdrawn)",
     "TINGGI", "Subjek data berhak menarik persetujuan kapan saja (Pasal 9 & 40).",
     "Hapus. Tulis cara menarik persetujuan dan bahwa pemrosesan dihentikan paling lambat 3×24 jam.", False),
    (r"(disimpan|menyimpan|simpan)[^.\n]{0,40}(selamanya|tanpa batas( waktu)?|seumur hidup)|(retain|store|keep)[^.\n]{0,40}(indefinitely|forever|permanently)",
     "TINGGI", "Data wajib dihapus bila tidak lagi diperlukan untuk tujuannya (Pasal 43) dan masa retensi harus diinformasikan (Pasal 21).",
     "Tetapkan masa simpan per jenis data, lalu hapus/musnahkan.", True),
    (r"(tidak (dapat|bisa|berhak) (menuntut|mengajukan (tuntutan|gugatan)))|melepaskan (hak|segala tuntutan)|waive (any|all|your) (rights?|claims?)",
     "TINGGI", "Subjek data berhak menggugat & menerima ganti rugi (Pasal 12). Pelepasan hak sepihak berisiko batal.",
     "Hapus klausul pelepasan hak.", False),
    (r"dengan (menggunakan|mengakses|mengunjungi|mendaftar|melanjutkan)(?:(?!dianggap)[^.\n]){0,80}(setuju|menyetujui|menerima)",
     "SEDANG", "'Dengan memakai layanan, Anda setuju' bukan persetujuan eksplisit per tujuan (Pasal 20 & 22). Boleh untuk menyatakan telah membaca kebijakan, bukan sebagai dasar pemrosesan data.",
     "Ubah menjadi pemberitahuan (\"Kebijakan ini menjelaskan...\") dan minta persetujuan terpisah untuk promosi/data spesifik.", False),
    (r"by (using|accessing|visiting|continuing)[^.\n]{0,80}(you )?(agree|consent|accept)", "SEDANG",
     "Browse-wrap consent is not explicit consent per purpose (Art. 20 & 22).", "Use it only as notice; collect separate opt-in consent.", False),
    (r"(mengubah|memperbarui|merevisi|diubah|diperbarui|berubah)[^.\n]{0,80}tanpa (pemberitahuan|memberi ?tahu|pemberitahuan terlebih dahulu)|(change|modify|update)[^.\n]{0,60}without (prior )?notice",
     "SEDANG", "Pengendali wajib memberi tahu subjek data SEBELUM informasi pemrosesan berubah (Pasal 21 ayat (2)).",
     "Ganti: \"Perubahan akan kami umumkan paling lambat [isi: 7] hari sebelum berlaku.\"", False),
    (r"(kepada|dengan) (siapa ?pun|pihak mana ?pun|semua pihak|pihak ketiga mana ?pun)|with any(one| third part(y|ies))",
     "SEDANG", "Berbagi data tanpa batas penerima & tujuan tidak memenuhi prinsip terbatas dan spesifik (Pasal 16 ayat (2)).",
     "Sebutkan penerima secara spesifik (kategori + tujuan).", True),
    (r"(semua|seluruh|segala) (data|informasi)[^.\n]{0,30}(di|pada) (perangkat|ponsel|hp|galeri|kontak) anda|all (data|information) on your device",
     "SEDANG", "Mengumpulkan melebihi keperluan melanggar prinsip minimisasi (Pasal 16 ayat (2) huruf a).",
     "Batasi ke data yang benar-benar diperlukan.", True),
    (r"\bgdpr\b|\bccpa\b|california|general data protection regulation|european economic area|uni eropa",
     "SEDANG", "Tampaknya disalin dari kebijakan luar negeri (GDPR/CCPA). Hak & kewajiban di Indonesia mengikuti UU 27/2022.",
     "Tulis ulang dengan rujukan UU 27/2022 (batas 3×24 jam, pemberitahuan kebocoran, dasar pemrosesan Pasal 20).", False),
    (r"100 ?% aman|tidak (mungkin|akan pernah) bocor|dijamin aman sepenuhnya|completely secure|100 ?% secure",
     "SEDANG", "Klaim keamanan mutlak menyesatkan dan bertentangan dengan kewajiban menyiapkan penanganan kebocoran (Pasal 46).",
     "Ganti dengan langkah keamanan nyata yang dilakukan.", False),
]

NEGASI = re.compile(r"(tidak|tak|bukan|tanpa|never|not|do not|don't|does not|won't|will not|jamais)\W+(\w+\W+){0,3}$")

PLACEHOLDER = re.compile(r"\[(?:isi|fill):[^\]]*\]|\[\[[^\]]*\]\]|\[isi\]|\[\.\.\.\]|lorem ipsum|xxx+", re.I)

# Layanan pihak ketiga yang umumnya menyimpan data di luar Indonesia (pemicu saran transfer_ln)
LAYANAN_LN = re.compile(r"google|gmail|drive|meta|facebook|instagram|whatsapp|tiktok|shopify|aws|amazon web|cloudflare|mailchimp|zoom|openai|chatgpt|claude|dropbox|microsoft|notion", re.I)


class GalatInput(Exception):
    pass


def baca_teks(path):
    if not path:
        raise GalatInput("Nama file belum diberikan. Contoh: python3 cek_kebijakan.py kebijakan.md")
    if not os.path.exists(path):
        raise GalatInput("File tidak ditemukan: {}. Periksa nama & lokasi file.".format(path))
    if os.path.isdir(path):
        raise GalatInput("{} adalah folder, bukan file. Berikan file .md atau .txt kebijakan privasi.".format(path))
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise GalatInput("File tidak bisa dibuka ({}).".format(e.strerror or e))
    if not data.strip():
        raise GalatInput("File kosong. Tempel isi kebijakan privasi ke file .md/.txt lalu coba lagi.")
    if data[:4] == b"PK\x03\x04":
        raise GalatInput("File tampaknya .docx/.zip. Simpan ulang sebagai .txt/.md (Word: File > Save As > Plain Text) atau tempel teksnya.")
    if data[:5] == b"%PDF-":
        raise GalatInput("File tampaknya PDF. Salin teksnya ke file .txt/.md, lalu periksa ulang.")
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        teks = data.decode("utf-16")
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


def normalisasi(teks):
    t = unicodedata.normalize("NFKC", teks).lower()
    t = t.replace("’", "'").replace("‘", "'")
    t = re.sub(r"[*_`#>|]+", " ", t)          # markup markdown
    t = re.sub(r"[ \t ]+", " ", t)
    return t


TOLAK = re.compile(r"\btanpa\b|\bwithout\b|\btidak (akan )?(memberi|kami beri)")


def ada(pola_list, t, tolak=None):
    """Kembalikan potongan teks pertama yang cocok. Bila `tolak` diberikan, abaikan
    kecocokan yang memuat kata penyangkal (mis. 'tanpa pemberitahuan')."""
    for p in pola_list:
        for m in re.finditer(p, t):
            if tolak is not None and tolak.search(m.group(0)):
                continue
            return m.group(0)
    return None


def cari_risiko(t, teks_asli_baris):
    temuan = []
    sudah = set()
    for pola, tingkat, alasan, saran, cek_negasi in RISIKO:
        for m in re.finditer(pola, t):
            if cek_negasi:
                awal = t[max(0, m.start() - 40):m.start()]
                awal = re.split(r"[.!?;:\n]", awal)[-1]  # hanya kalimat yang sama
                if NEGASI.search(awal) or re.match(r"(tidak|tak|not|never)\b", m.group(0)):
                    continue
            no_baris = t.count("\n", 0, m.start()) + 1
            kunci = (no_baris, tingkat)
            if kunci in sudah:
                continue
            sudah.add(kunci)
            kutipan = teks_asli_baris[no_baris - 1].strip() if no_baris - 1 < len(teks_asli_baris) else m.group(0)
            if len(kutipan) > 160:
                kutipan = kutipan[:157] + "..."
            temuan.append({"tingkat": tingkat, "baris": no_baris, "kutipan": kutipan, "alasan": alasan, "saran": saran})
    temuan.sort(key=lambda x: (0 if x["tingkat"] == "TINGGI" else 1, x["baris"]))
    return temuan


def periksa(teks):
    t = normalisasi(teks)
    baris_asli = teks.splitlines()
    hasil = []
    total = 0.0
    dapat = 0.0
    for u in UNSUR:
        total += u["bobot"]
        if "sub" in u:
            ada_sub = {k: bool(ada(v, t)) for k, v in u["sub"].items()}
            n = sum(ada_sub.values())
            nilai = u["bobot"] * n / len(ada_sub)
            status = "ADA" if n == len(ada_sub) else ("SEBAGIAN" if n else "TIDAK ADA")
            kurang = [k for k, v in ada_sub.items() if not v]
            hasil.append({"id": u["id"], "label": u["label"], "status": status, "nilai": round(nilai, 2), "bobot": u["bobot"],
                          "kurang": kurang, "dasar": u["dasar"], "saran": u["saran"] if kurang else ""})
            dapat += nilai
        else:
            bukti = ada(u["pola"], t, TOLAK if u["id"] in ("perubahan", "kebocoran") else None)
            hasil.append({"id": u["id"], "label": u["label"], "status": "ADA" if bukti else "TIDAK ADA",
                          "nilai": u["bobot"] if bukti else 0, "bobot": u["bobot"], "bukti": bukti or "",
                          "dasar": u["dasar"], "saran": "" if bukti else u["saran"]})
            dapat += u["bobot"] if bukti else 0
    for u in UNSUR_BERSYARAT:
        pemicu = ada(u["pemicu"], t)
        if not pemicu:
            continue
        total += u["bobot"]
        bukti = ada(u["pola"], t)
        dapat += u["bobot"] if bukti else 0
        hasil.append({"id": u["id"], "label": u["label"], "status": "ADA" if bukti else "TIDAK ADA",
                      "nilai": u["bobot"] if bukti else 0, "bobot": u["bobot"], "bukti": bukti or "", "pemicu": pemicu,
                      "dasar": u["dasar"], "saran": "" if bukti else u["saran"]})

    skor = int(round(100.0 * dapat / total)) if total else 0
    risiko = cari_risiko(t, baris_asli)
    n_tinggi = sum(1 for r in risiko if r["tingkat"] == "TINGGI")
    if skor >= 85 and n_tinggi == 0:
        status = "CUKUP LENGKAP"
    elif skor >= 60:
        status = "PERLU PERBAIKAN"
    else:
        status = "KURANG LENGKAP"
    if n_tinggi and status == "CUKUP LENGKAP":
        status = "PERLU PERBAIKAN"
    isian_kosong = len(PLACEHOLDER.findall(teks))
    if isian_kosong and status == "CUKUP LENGKAP":
        status = "PERLU DILENGKAPI"

    catatan = []
    jumlah_kata = len(re.findall(r"\w+", t))
    if jumlah_kata < 150:
        catatan.append("Teks sangat pendek ({} kata). Kebijakan privasi yang memadai biasanya > 400 kata.".format(jumlah_kata))
    ph = PLACEHOLDER.findall(teks)
    if ph:
        catatan.append("Masih ada {} isian kosong (mis. {}). Lengkapi sebelum dipublikasikan.".format(len(ph), ph[0]))
    tln = next((h for h in hasil if h["id"] == "transfer_ln"), None)
    m_ln = LAYANAN_LN.search(teks)
    if tln and tln["status"] == "TIDAK ADA" and m_ln:
        catatan.append("Teks menyebut layanan '{}' yang umumnya menyimpan data di luar Indonesia; jelaskan transfer ke luar negeri (Pasal 56).".format(m_ln.group(0)))
    if not re.search(r"pejabat pelindungan data|petugas pelindungan data|\bppdp\b|\bdpo\b|data protection officer", t):
        catatan.append("Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.")

    return {
        "versi_pemeriksa": VERSI,
        "skor": skor,
        "status": status,
        "jumlah_kata": jumlah_kata,
        "isian_kosong": isian_kosong,
        "unsur": hasil,
        "risiko": risiko,
        "catatan": catatan,
        "peringatan": "Pemeriksa bantu berbasis kata kunci, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.",
    }


def cetak_teks(r, nama):
    out = []
    out.append("PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — {}".format(nama))
    out.append("Skor kelengkapan: {}/100  |  Status: {}  |  {} kata".format(r["skor"], r["status"], r["jumlah_kata"]))
    out.append("")
    out.append("UNSUR:")
    for h in r["unsur"]:
        tanda = {"ADA": "[v]", "SEBAGIAN": "[~]", "TIDAK ADA": "[ ]"}[h["status"]]
        baris = "  {} {} — {}".format(tanda, h["label"], h["status"])
        if h.get("kurang"):
            baris += " (kurang: {})".format(", ".join(k.replace("_", " ") for k in h["kurang"]))
        out.append(baris)
    kurang = [h for h in r["unsur"] if h["status"] != "ADA"]
    if kurang:
        out.append("")
        out.append("YANG PERLU DITAMBAHKAN:")
        for i, h in enumerate(kurang, 1):
            out.append("  {}. {} [{}]".format(i, h["saran"], h["dasar"]))
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
    out = ["Unsur yang diperiksa (bobot):"]
    for u in UNSUR:
        out.append("  - {} ({}) — {}".format(u["label"], u["bobot"], u["dasar"]))
    out.append("Unsur bersyarat (hanya bila teks menyebut hal terkait):")
    for u in UNSUR_BERSYARAT:
        out.append("  - {} ({}) — {}".format(u["label"], u["bobot"], u["dasar"]))
    out.append("Frasa berisiko yang dideteksi: {} pola (ID & EN).".format(len(RISIKO)))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Periksa kelengkapan Kebijakan Privasi terhadap UU 27/2022 (PDP).")
    ap.add_argument("file", nargs="?", help="File .md/.txt berisi kebijakan privasi")
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
