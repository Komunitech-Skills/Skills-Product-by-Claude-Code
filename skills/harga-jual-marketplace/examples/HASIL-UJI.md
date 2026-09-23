# HASIL UJI — harga-jual-marketplace

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja `/tmp/uji-harga-jual-marketplace/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (00)

## Audit keamanan
- `scripts/harga_marketplace.py`: hanya `argparse, json, re, sys, decimal`. Hanya membaca file `--config` yang diberikan; tidak menulis file, tidak ada jaringan/subprocess/kredensial.
- SKILL.md/README/references/templates: tidak ada prompt injection. **Aman.**

## Verifikasi angka (independen)
- Script terpisah (`verif.py`, model laba sendiri dengan `fractions.Fraction`, pencarian harga sendiri; tidak mengimpor script skill) membandingkan **300 konfigurasi acak** (1–4 komponen persen dengan/ tanpa batas maksimum, biaya per pesanan dibagi 1–3 barang, biaya lain, voucher persen ± maks / voucher rupiah, PPh 22 ya/tidak, target margin/laba/markup, pembulatan 1/500/1000) → **0 selisih** pada harga impas, harga tepat target, harga rekomendasi, dan laba pada harga rekomendasi. Mode cek harga (`--harga-jual`) pada harga yang sama juga cocok.
- Contoh SKILL.md (M 35.000, admin 8%, layanan 4%, pembayaran 1,5%, proses 1.250, margin 20% → impas Rp42.152, rekomendasi Rp55.000, laba Rp11.050): **benar**.
- **README "Sesudah" TIDAK konsisten** — lihat cacat sedang no. 1.
- Data tepi: "Rp 35.000", "1.500.000,50", "8,5" (persen), modal 0 (diberi catatan), biaya platform 0 (diberi catatan) → benar. Target mustahil (total persen + margin ≥ 100%), admin 100%, voucher 100%, qty per pesanan 1,5, modal "abc"/kosong, JSON rusak/kosong → ditolak dengan `ERROR:` yang jelas. Harga di bawah impas → "RUGI Rp… per barang".

## Kepatuhan fokus khusus
- Angka biaya platform: SKILL.md melarang mengarang; template diberi `_catatan` dan nama "(contoh - cek Seller Center)". Pada S4 agent bertanya, pada S2 label contoh tampil. Namun catatan script tetap menyebut "berasal dari input Anda" (cacat sedang no. 2).
- PPh 22 0,5%: selalu dihitung kecuali `--pph22 tidak`; pengecualian (OP, omzet ≤ Rp500 juta, wajib surat pernyataan/SKB) dan "bukan pajak baru, cara memperhitungkan tanya DJP" dijelaskan jujur. TikTok Shop belum terverifikasi sebagai pemungut → script tetap memotong tanpa catatan (ringan).

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Frasa awam ("harga jual di Shopee berapa biar untung", "potongan marketplace") + EN |
| Kemudahan awam | 8 | Satu kalimat cukup bila tahu persen biaya; pengguna awam sering tidak tahu → harus bertanya |
| Kualitas output | 9 | Harga impas + rekomendasi + rincian + margin & markup + saran; perbandingan antar-platform |
| Akurasi (angka/fakta) | 8 | 0 selisih pada 300 kasus; tetapi contoh README salah untuk inputnya |
| Penanganan input kurang | 9 | Tanya sekali, 5 pertanyaan, opsi angka contoh berlabel |
| Penanganan di luar cakupan | 8 | Rujukan ke hitung-hpp/listing-marketplace jelas; tanpa kalimat cadangan |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: dengan skill jelas lebih baik — agent tanpa skill melewatkan PPh 22 walau pengguna menyinggungnya, sehingga harga tepat & laba salah, dan tidak memberi harga impas. Tidak ada cacat berat pada perhitungan; cacat README harus diperbaiki sebelum rilis.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Contoh README "Sesudah" menampilkan angka yang tidak sesuai dengan kalimat inputnya.** Input README: "Modal 35 ribu, admin Shopee 8%, gratis ongkir 4%, biaya proses 1.250. Mau margin 20%" (tanpa biaya pembayaran 1,5%), tetapi hasil yang dijanjikan "Harga minimal Rp42.152, rekomendasi Rp55.000, uang diterima Rp46.050, laba Rp11.050" — itu angka untuk input **dengan** pembayaran 1,5%. Pembeli yang mencoba prompt README akan mendapat **Rp41.429 / Rp54.000 / Rp46.000 / Rp11.000**. Saran: di README bagian "Contoh sebelum & sesudah", tambahkan "pembayaran 1,5%" ke kalimat input, atau ganti angka hasil menjadi Rp41.429 / Rp54.000 / Rp46.000 / Rp11.000.
2. **Catatan script mengklaim "Persentase biaya platform berasal dari input Anda" walaupun dijalankan dari template contoh** (S2). Label "contoh" hanya ada di nama platform, jadi bisa hilang bila agent/pengguna mengganti nama. Saran: di `main()`, bila JSON punya `_catatan` atau nama platform mengandung "contoh", ganti catatan pertama menjadi "PERHATIAN: persentase biaya adalah ANGKA CONTOH, bukan tarif resmi — cek Seller Center" dan letakkan di baris paling atas output; tambahkan kunci eksplisit `"angka_contoh": true` di template.

### Ringan
3. PPh 22 dipotong otomatis untuk platform bernama TikTok Shop tanpa catatan, padahal `references/regulasi.md` menandai TikTok Shop BELUM TERVERIFIKASI sebagai pemungut. Saran: bila nama platform mengandung "tiktok", tambahkan catatan "status pemungut belum terverifikasi; PPh 22 dimasukkan sebagai perhitungan konservatif".
4. Baris tabel dibulatkan sendiri-sendiri sehingga jumlah yang terlihat bisa beda Rp1 dari "Uang diterima" (S4: 3.023 + 233 dari 3.022,50 + 232,50). Saran: tambahkan catatan kecil di bawah tabel atau tampilkan 2 desimal bila ada pecahan .50.
5. `references/regulasi.md`: tanggal "berlaku 1 Agustus 2026" untuk PPh 22 tertulis di judul tanpa status verifikasi. Saran: tambahkan baris "Tanggal mulai efektif | 1 Agustus 2026 | status + sumber".
6. SKILL.md "Kapan TIDAK digunakan": tambahkan kalimat cadangan bila skill rujukan (`hitung-hpp`, `listing-marketplace`, `pph-final-umkm`) tidak dimiliki pembeli.
