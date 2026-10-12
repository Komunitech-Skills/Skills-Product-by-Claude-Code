# Hasil uji: checklist-keamanan-pangan-usaha v1.0.2

- **Tanggal:** 2026-10-12
- **Penguji:** agent penguji independen Komunitech (bukan pembuat); uji ulang setelah perbaikan fakta (unggas >= 74 °C, pendinginan 2 tahap, alergen BPOM, halal wajib)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router Komunitech claude-sonnet-5; skenario 1 SESUDAH di konteks kanal Telegram (tanpa mengirim)
- **Rincian:** `00-openclaw-sebelum-sesudah.md`, ringkasan `01`-`04`; hasil lama v1.0.1 diarsip sebagai `*-v1.0.1.md`

## Skor kualitas: 8/10 (sesudah 8,25)

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1 Katering nasi box + "ayam 63 °C cukup kan?" (SESUDAH di Telegram) | 6,0 | 8,0 |
| 2 Warung bakso + es campur, apa yang diubah dulu | 5,0 | 8,0 |
| 3 Input kurang ("checklist keamanan pangan buat usaha saya") | 5,5 | 8,5 |
| 4 Jebakan label halal & bebas alergen tanpa dasar | 6,0 | 8,5 |
| **Rata-rata** | **5,6** | **8,25** |

**VERDIK: LULUS** (sesudah 8,25 >= 8; selisih +2,6 >= 1,5; tanpa kesalahan fakta keselamatan pada jawaban SESUDAH).

## Pemeriksaan fakta (SESUDAH, 4 jawaban)
| Fakta | Hasil |
|---|---|
| Ayam/unggas >= 74 °C, 63 °C ditolak | Benar (S1 menolak tegas, menjelaskan 63 °C hanya untuk ikan/telur langsung saji/sapi utuh; S3, S4 74 °C) |
| Daging giling >= 71 °C | Benar (S2) |
| Zona bahaya 5-60 °C; 2 jam, 1 jam bila > 32 °C | Benar (S1, S2, S3, S4) |
| Kulkas <= 5 °C; freezer <= -18 °C | Benar |
| Pendinginan 21 °C/2 jam lalu 5 °C/4 jam | Benar (S1, S3, S4) |
| Santan = kelapa, bukan susu | Benar, ditulis terpisah (S1, S3, S4) |
| Halal WAJIB, UMK 18 Okt 2026 ("6 hari lagi" dari 12 Okt = benar), UU 33/2014 & PP 42/2024 | Benar (S1-S4); tidak pernah ditulis "opsional" |
| "Bebas alergen" ditolak, diganti "diproses di dapur yang juga mengolah ..." | Benar (S4) |
SEBELUM (tanpa skill): S2 menyarankan batas "±4-6 jam di suhu ruang panas" dan S1 menyebut "batas mutlak 4 jam" (kedua angka salah/berbahaya); S1 menaruh halal di "Sangat disarankan" tanpa tenggat; S1 versi Telegram memakai Permenkes 1096/2011 (sudah dicabut) dan mengira ayam tidak bisa Self Declare. Ayam 74 °C dijawab benar di sisi SEBELUM.

## Script dan tests
- `python3 tests/uji_regresi.py`: 12/12 lulus.
- `cek_log_suhu.py` dengan data uji baru (`examples/data/log-suhu-uji-v1.0.2.csv`, 9 baris): ayam goreng 63 °C ditandai melanggar (batas >= 74), daging giling 70 °C melanggar (>= 71), penahan panas 55 °C melanggar, pemanasan ulang 72 °C melanggar, freezer -18 OK, kulkas 6 °C pukul 09:00 pulih 11:30 = 150 menit (cocok hitungan penguji). Log contoh (`log-suhu.csv`, kulkas 180 menit) cocok dengan hitungan python penguji.
- Data rusak (`log-suhu-rusak.csv`), berkas tak ada (rc=1, pesan jelas), berkas biner: tidak crash, baris bermasalah dilaporkan.
- Cacat kecil script: berkas yang semua barisnya tak terbaca tetap mencetak "Tidak ada pelanggaran batas pada data yang terbaca" (menyesatkan; sebaiknya "tidak ada data terbaca"); penahan panas yang tak pulih dicetak "bisa sampai 0 menit".

## Alasan skor
- (+) Menolak "ayam 63 °C cukup" dengan alasan dan angka benar, plus saran biar cepat tanpa menurunkan suhu (potong lebih kecil).
- (+) Paket utuh siap cetak di chat (termasuk konteks Telegram, tanpa file), jujur soal tanpa termometer, 3 pertanyaan di akhir.
- (+) Fakta keselamatan dan hukum konsisten di keempat jawaban; model dasar sudah tahu 74 °C tetapi mengarang batas waktu 4-6 jam dan menaruh halal sebagai saran.
- (+) Jebakan: tolak singkat -> padanan sah (kalimat alergen jujur, jalur Self Declare/SEHATI) -> tetap kerjakan; tidak melebih-lebihkan ancaman pidana.
- (-) S1: permintaan "daftar alergen untuk label" tidak dijawab dengan bagian tersendiri/kalimat label siap tempel; alergen tersebar di peta risiko (versi SEBELUM di Telegram justru memberi daftar dan kalimat label).
- (-) S2: tidak menyebut target <= 5 °C untuk cooler box atau membuang stok yang sudah lewat; halal hanya ditawarkan.
- (-) S3/S4: menebak menu (ayam, susu), sangat panjang; S4 membuat paket lengkap padahal diminta label; `[isian: jam buka]` terbawa ke S1 katering.

## Catatan jujur
- Satu run per skenario per sisi (router stabil, tanpa timeout). Nilai SEBELUM versi Telegram skenario 1 sekitar 6,5; selisih tetap > 1,5.
- Model dasar sudah bagus untuk 74 °C; pembeda ada di fakta waktu/suhu lengkap, halal wajib bertanggal, dan paket siap cetak.

## PERLU REVIEW
- Perizinan dan tenggat halal (PP 42/2024, BPJPH) perlu dicek ulang menjelang/ sesudah 18 Okt 2026.
- Alergen BPOM 31/2018 jo. 20/2021 dan perlakuan "kelapa" dicek oleh orang berwenang bila dipakai pada label kemasan.
