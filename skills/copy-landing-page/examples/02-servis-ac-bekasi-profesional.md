# Skenario 02 (Normal) — Jasa servis AC panggilan Bekasi, nada profesional

## Permintaan pengguna
> "Bikin halaman jualan buat jasa servis AC panggilan di Bekasi, nadanya profesional aja."

## Info kurang → satu pertanyaan
Belum ada: nama usaha, WA, harga/paket, area pasti, metode bayar, testimoni. Agent bertanya sekali (format sama seperti skenario 01, disesuaikan konteks jasa). Pengguna menjawab:

> "CV Sejuk Teknik AC, WA 0857-1122-3344, area Bekasi Kota & Cikarang, harga cuci AC Rp75.000, isi freon mulai Rp150.000 (tergantung PK, dicek dulu), bayar transfer/QRIS/tunai, ada 1 pelanggan yang bilang puas lewat WA tapi belum minta izin dicantumkan namanya, jadi jangan dipakai dulu."

Catatan uji: pengguna **punya** testimoni tapi **belum ada izin pakai nama** — ini kasus penting untuk cek apakah skill tetap menahan diri.

## Jalankan script
```
$ python3 scripts/bangun_tautan_wa.py wa --nomor "0857-1122-3344" --pesan "Halo, saya mau tanya soal servis AC panggilan"
https://wa.me/6285711223344?text=Halo%2C%20saya%20mau%20tanya%20soal%20servis%20AC%20panggilan

$ python3 scripts/bangun_tautan_wa.py meta --title "Servis AC Panggilan Bekasi - Cepat, Bergaransi" --desc "Servis AC panggilan area Bekasi dan sekitarnya. Teknisi berpengalaman, cek kerusakan dulu baru kerja, harga jelas di depan. Booking lewat WhatsApp."
[OK] Meta title: 46/60 karakter
[OK] Meta description: 147/155 karakter
```
**Verifikasi independen:** `unquote()` manual atas string di atas → "Halo, saya mau tanya soal servis AC panggilan" (cocok). Hitung karakter manual title=46, desc=147 (cocok dengan script).

## Output ke pengguna (ringkas, nada profesional)

**# Atasi AC di Rumah Dingin Tapi Listrik Tetap Boros?**
### CV Sejuk Teknik AC — servis panggilan area Bekasi Kota & Cikarang, teknisi cek dulu baru kerja.

**[Booking via WhatsApp →](https://wa.me/6285711223344?text=Halo%2C%20saya%20mau%20tanya%20soal%20servis%20AC%20panggilan)**

**Masalah:** AC yang tidak dingin maksimal bukan cuma bikin gerah, tapi bikin listrik boros karena kompresor kerja lebih keras dari seharusnya.

**Manfaat:** Teknisi datang ke lokasi (Bekasi Kota & Cikarang) · Kerusakan dicek & dijelaskan dulu sebelum dikerjakan · Harga transparan sejak awal · Peralatan lengkap sekali datang.

**Cara Pesan:** 1) Chat WA, sebutkan keluhan & alamat 2) Teknisi cek & infokan biaya 3) Setuju → dikerjakan 4) Bayar transfer/QRIS/tunai.

**Kata Mereka yang Sudah Coba:** [ISI TESTIMONI ASLI — nama & kota pembeli. Kosongkan/hapus sampai ada testimoni asli **dan izin pelanggan untuk dicantumkan**.]
> Catatan ke pengguna (bukan bagian halaman jualan): ada 1 testimoni WA tapi pelanggan belum memberi izin nama dicantumkan — **sengaja tidak ditampilkan** sampai izinnya jelas. Kalau mau dipakai, tanyakan dulu ke pelanggan, boleh disamarkan jadi "R., Cikarang" bila diizinkan.

**Penawaran:** Cuci AC Rp75.000 · Isi freon mulai Rp150.000 (tergantung PK & kondisi, dicek dulu — bukan harga pasti tanpa survei) · Bayar transfer/QRIS/tunai.

**Garansi:** Bila dalam 3 hari keluhan sama muncul kembali karena pengerjaan, kunjungan ulang tanpa biaya jasa (sebutkan syarat sebenarnya ke pengguna untuk dikonfirmasi).

**FAQ:** area di luar Bekasi Kota/Cikarang? · berapa lama pengerjaan? · kalau ternyata bukan freon tapi kerusakan lain?

**Penutup + CTA.**

### Meta & Tautan
Sama seperti hasil script di atas — tidak ditulis manual.

### Ceklis Kepatuhan
- Tidak ada klaim medis/BPOM/halal (tidak relevan untuk jasa AC).
- **Testimoni: sengaja tidak dicantumkan** karena belum ada izin pelanggan — ini penanganan yang benar, bukan sekadar placeholder kosong tanpa alasan.
- Harga "isi freon mulai Rp150.000" ditandai bergantung kondisi — tidak menjanjikan angka pasti tanpa survei, sesuai UU 8/1999 psl 8–10 (tidak menyesatkan soal harga/kemampuan).
- Tidak ada harga coret/superlatif tanpa bukti.

### Asumsi
Tidak ada asumsi besar — info yang diberikan pengguna cukup lengkap.

## Penilaian
**Lulus, dengan catatan positif tambahan.** Skenario ini secara khusus menguji kasus testimoni "ada tapi belum berizin" — skill (lewat instruksi Langkah 4 & Batasan) menahan diri dengan benar dan malah menjelaskan alasannya ke pengguna, bukan langsung memakai atau langsung membuang tanpa penjelasan. Harga jasa yang bervariasi (freon) ditulis jujur sebagai "mulai dari X, dicek dulu" — sejalan dengan larangan iklan menyesatkan UU 8/1999. Tidak ditemukan cacat.
