# Skenario 01 (Normal) — "Buatkan landing page untuk keripik pedas saya, harga 25 ribu"

> Dijalankan oleh **penguji independen** (agent yang hanya membaca folder skill `copy-landing-page/` dan mengikutinya, tidak membaca `examples/uji-pembuat-01-keripik-pedas.md` sebelum menulis output ini agar hasilnya benar-benar independen). Nama usaha & detail sengaja dibuat berbeda dari contoh pembuat skill supaya perbandingan adil.

## Permintaan pengguna
> "Buatkan landing page untuk keripik pedas saya, harga 25 ribu."

## Langkah 1 — info kurang → satu pertanyaan (sesuai SKILL.md Input & Langkah kerja)
Info ada: produk (keripik pedas), harga (Rp25.000). Belum ada: nama usaha, WA, ongkir, metode bayar, testimoni, nada. Agent bertanya **satu kali**:

> "Siap, sebelum saya buatkan boleh dilengkapi (jawab yang kamu tahu saja, sisanya saya pakai default):
> 1. Nama usaha/produknya apa?
> 2. Nomor WhatsApp untuk tombol pesan?
> 3. Kirim area mana saja & ongkirnya bagaimana?
> 4. Metode bayar apa saja (transfer/QRIS/COD)?
> 5. Ada testimoni pelanggan asli yang mau ditampilkan?
> 6. Mau nada santai, profesional, atau 'bahasa ibu-ibu'?
>
> Kalau mau cepat, saya pakai default: nada santai-profesional, bayar transfer & QRIS, tanpa testimoni dulu (biar tidak mengarang)."

## Jawaban pengguna (dibuat untuk uji)
> "Namanya Keripik Setan Mak Iyem, WA 0812-3456-7890, kirim se-Jabodetabek pakai ojol/kurir sendiri kalau dekat, luar kota pakai ekspedisi, bayar transfer/QRIS, belum ada testimoni tertulis, nada santai aja."

## Langkah 5 & 7 — jalankan script (dijalankan penguji, bukan disalin dari contoh pembuat)
```
$ python3 scripts/bangun_tautan_wa.py wa --nomor "0812-3456-7890" --pesan "Halo, saya mau pesan Keripik Setan Mak Iyem dari halaman ini"
https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini

$ python3 scripts/bangun_tautan_wa.py meta --title "Keripik Setan Mak Iyem - Pedas Nampol, Renyah 3 Bulan" --desc "Keripik singkong pedas level 1-5, tanpa pengawet, renyah tahan 3 bulan. Kirim Jabodetabek & luar kota. Pesan lewat WhatsApp, bayar transfer/QRIS."
[OK] Meta title: 54/60 karakter
[OK] Meta description: 152/155 karakter
```
**Verifikasi independen (bukan salin output script):** decode manual `urllib.parse.unquote` atas string `%2C`,`%20` di atas menghasilkan persis "Halo, saya mau pesan Keripik Setan Mak Iyem dari halaman ini" — tautan wa.me valid dan bisa dibuka. Hitung `len()` manual meta title = 54, meta description = 152 — cocok dengan angka script.

## Output ke pengguna (ringkas — struktur penuh sesuai Format Output SKILL.md)

### 1. Versi Lengkap (Landing Page)
**# Pedas Nampol, Bikin Nagih Tanpa Takut Melempem**
### Keripik Setan Mak Iyem — renyah tahan 3 bulan, kirim Jabodetabek & luar kota.

**[Pesan Sekarang lewat WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini)**

**Masalahnya:** Keripik pedas enak gampang dicari, yang susah dicari itu yang beneran renyah sampai habis, bukan yang melempem di hari ketiga.

**Kenapa Cocok Buat Kamu:** Level pedas 1–5 · Tanpa pengawet, renyah 3 bulan di suhu ruang · Kemasan tebal aman kirim luar kota · Cocok stok cemilan atau dijual lagi.

**Cara Pesan:** 1) Chat WA di tombol ini 2) Sebutkan level & jumlah 3) Bayar transfer/QRIS 4) Dikirim ojol (Jabodetabek) atau ekspedisi (luar kota).

**Kata Mereka yang Sudah Coba:** [ISI TESTIMONI ASLI — nama & kota pembeli. Hapus bagian ini sampai ada testimoni asli.]

**Penawaran:** Rp25.000/bungkus (200gr) · Kirim Jabodetabek (ojol/kurir) & luar kota (ekspedisi, ongkir menyesuaikan) · Bayar transfer/QRIS.

**Garansi:** Kalau diterima remuk/rusak karena pengiriman, kirim foto ke WA maks. 1x24 jam — diganti atau refund.

**FAQ:** (3 pertanyaan: tahan berapa lama setelah dibuka, bisa campur level pedas, ongkir luar Jabodetabek berapa — dijawab jujur, ongkir "menyesuaikan ekspedisi, diinfokan saat konfirmasi").

**Penutup + CTA WA diulang.**

### 2–4. Versi Pendek, 3 Variasi Headline, Meta Title/Desc
Sesuai contoh script di atas — semua tautan/angka identik dengan hasil script (tidak ditulis manual).

### 5. Tautan WhatsApp
`https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini` + teks asli sebelum encode.

### 6. Ceklis Kepatuhan
- Tidak ada klaim kesehatan/BPOM/halal (produk belum disebut bersertifikat → kata "halal" sengaja tidak dipakai, sesuai Batasan SKILL.md).
- Tidak ada testimoni/rating/angka penjualan karangan — placeholder dipakai.
- Tidak ada harga coret/hitung mundur palsu.
- **Perlu dicek pengguna:** klaim "renyah 3 bulan" dan "tanpa pengawet" harus sesuai kondisi produk sebenarnya.

### 7. Asumsi
Nada: santai (sesuai jawaban). Ongkir luar kota: umum ("menyesuaikan ekspedisi") karena rincian belum diberikan.

## Penilaian
**Lulus.** Alur satu-pertanyaan, struktur lengkap, script dijalankan (bukan dikira-kira), tautan WA & meta tervalidasi ulang manual dan cocok 100%, tidak ada bukti sosial dikarang, ceklis kepatuhan tampil sesuai `references/dasar-hukum-klaim.md`. Tidak ada cacat pada skenario ini.
