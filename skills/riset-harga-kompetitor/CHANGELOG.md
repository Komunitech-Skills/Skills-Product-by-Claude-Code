# Riwayat perubahan — riset-harga-kompetitor

Catatan teknis per versi.

## Catatan revisi 1.0.5 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.4 (2026-09-29)
- Aturan kerja standar library: tidak menginstal paket, tidak membuka/mencari file di luar yang diberikan, lokasi file baru disebut, hasil di folder kerja yang disepakati (bukan /tmp).

## Catatan revisi 1.0.3 (2026-09-29)
- Satuan kemasan/jumlah mengalikan ukuran: `10 sachet 25 gr` = 250 g, `2 karung 1 kg` = 2 kg, `1 lusin 100 gr` = 1.200 g (12 x 100 g), `2 kodi 50 gr` = 2 kg, `100 gr x 2 lusin` = 2.400 g (dengan catatan "cek"); `1 lusin` sendiri = 12 pcs, `1 kodi` = 20 pcs, `1 rim` = 500 lembar. Jumlah butir di dalam (`isi 10 sachet 25 gr`) tidak dikalikan. Uji regresi 44.

## Catatan revisi 1.0.2 (2026-09-29)
- Ukuran `500 gr isi 2`, `250gr (isi 2)`, `2 pack 500 gr`, `3 botol 250 ml` dibaca sebagai isi total (1 kg / 500 g / 1 kg / 750 ml) dengan catatan "cek: bila angka itu sudah total, tulis ulang ukurannya"; jumlah butir di dalam (`isi 10 pcs 250 gr`, `250 gr isi 20 sachet`) tidak dikalikan; `isi 2 pack 500 gr` dibaca total 500 g dengan catatan cek. Sampaikan catatan "cek" ke pengguna bila harga setara pesaing itu memengaruhi rekomendasi.

## Catatan revisi 1.0.1 (2026-09-28)
- Perbaikan hasil uji independen - ukuran pecahan (`1/2 kg`, `setengah kilo`) dan paket (`250 g x 2`, `isi 2 @250gr`, `250 g + 250 g`, `2 pcs @ 250 gr`) dibaca benar; pesaing jauh dari median dikeluarkan dari statistik (`--pakai-semua` untuk mengikutkan); strategi premium kini P75-P90; mode pasar saja tanpa HPP; CSV ANSI/UTF-16 & kolom bergeser ditangani; harga < Rp 100 ditolak; pilih satuan yang sama bila teks memuat beberapa ukuran; pesan error lebih jelas; bagian "Cara menguji harga baru".

## Catatan revisi 1.0.0 (2026-09-28)
- Rilis awal (uji internal).
