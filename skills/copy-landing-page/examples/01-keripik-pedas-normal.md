> **Sumber keluaran:** penguji independen Akun B, 2026-10-13, Claude Code (simulasi agent), data fiktif; menggantikan contoh lama yang memuat atribut/klaim tanpa sumber.

# Skenario 01 (Normal) — "Buatkan landing page untuk keripik pedas saya, harga 25 ribu"

Dijalankan oleh agent yang hanya membaca folder skill `copy-landing-page/` (termasuk `references/` dan
`scripts/`) dan mengikuti `SKILL.md` apa adanya. Nama usaha & detail sengaja dibuat berbeda dari contoh
pembuat skill. Fokus ulang uji ini: atribut produk yang tidak diberikan pengguna tidak boleh ditulis sebagai
fakta, melainkan `[isian: ...]`.

## Input pengguna (giliran 1)
> "Buatkan landing page untuk keripik pedas saya, harga 25 ribu."

## Output (giliran 1) — info kurang → satu pertanyaan (sesuai SKILL.md Input & Langkah kerja)
Info ada: produk (keripik pedas), harga (Rp25.000). Belum ada: nama usaha, target pembeli, detail produk, WA,
ongkir, metode bayar, garansi, testimoni, nada. Agent bertanya **satu kali**:

> "Siap, sebelum saya buatkan boleh dilengkapi (jawab yang kamu tahu saja; sisanya saya pakai default atau
> saya tandai [isian] supaya kamu yang mengisi):
> 1. Nama usahanya apa, dan detail apa yang mau ditonjolkan (bahan, ukuran/isi, varian rasa atau level pedas,
>    masa simpan, izin PIRT/BPOM bila ada)?
> 2. Target pembelinya siapa?
> 3. Nomor WhatsApp untuk tombol pesan?
> 4. Kirim ke area mana saja & ongkirnya bagaimana? Bayar lewat apa saja (transfer/QRIS/COD)?
> 5. Ada garansi/retur yang benar-benar kamu berlakukan?
> 6. Ada testimoni pelanggan asli yang mau ditampilkan?
> 7. Mau nada santai, profesional, atau 'bahasa ibu-ibu'? Mau landing page lengkap saja, atau sekalian
>    versi pendek untuk link-in-bio?
>
> Detail produk yang tidak kamu sebut tidak akan saya tebak. Kalau mau cepat, saya pakai default: nada
> santai-profesional, bayar transfer & QRIS, nomor WA placeholder, tanpa testimoni."

## Input pengguna (giliran 2, dibuat untuk uji)
> "Namanya Keripik Setan Mak Iyem, WA 0812-3456-7890, kirim se-Jabodetabek pakai ojol/kurir sendiri kalau dekat, luar kota pakai ekspedisi, bayar transfer/QRIS, belum ada testimoni tertulis, nada santai aja."

Fakta yang boleh dipakai: nama usaha, produk keripik pedas, harga Rp25.000, WA 0812-3456-7890, pengiriman
(Jabodetabek: ojol/kurir sendiri bila dekat; luar kota: ekspedisi), bayar transfer/QRIS, tanpa testimoni,
nada santai. **Tidak diberikan:** bahan, jenis keripik, ukuran/isi, satuan harga, varian/level pedas, masa
simpan, pengawet, izin edar, garansi, ongkir, estimasi waktu kirim, target pembeli.

## Langkah 5 & 7 — script dijalankan (bukan dikira-kira)
```
$ python3 scripts/bangun_tautan_wa.py wa --nomor "0812-3456-7890" --pesan "Halo, saya mau pesan Keripik Setan Mak Iyem dari halaman ini"
https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini

$ python3 scripts/bangun_tautan_wa.py meta --title "Keripik Setan Mak Iyem - Keripik Pedas Rp25.000, Pesan WA" --desc "Keripik Setan Mak Iyem: keripik pedas Rp25.000. Pesan lewat WhatsApp, kirim ke Jabodetabek & luar kota, bayar transfer atau QRIS."
[OK] Meta title: 57/60 karakter
[OK] Meta description: 129/155 karakter
```
Percobaan pertama meta title "... Pesan via WA" menghasilkan 61/60 (PERINGATAN), lalu dipersingkat menjadi
"Pesan WA" (57/60). Verifikasi independen: `urllib.parse.unquote` atas `%2C`/`%20` menghasilkan persis
"Halo, saya mau pesan Keripik Setan Mak Iyem dari halaman ini"; `len()` manual title = 57, description = 129.
Nomor rusak (`--nomor abc`) ditolak script dengan pesan jelas dan exit code 1.

## Output (giliran 2) — ke pengguna, utuh
````
⚠️ Pengingat izin edar: keripik adalah pangan olahan, jadi izin edar (PIRT/SPP-IRT atau BPOM) wajib ada
SEBELUM dijual dan dipromosikan. Kamu belum menyebut punya izin, jadi halaman ini tidak memuat klaim izin
apa pun.

## 1. Versi Lengkap (Landing Page)

# Pesan Keripik Pedas Mak Iyem Lewat WhatsApp, Dikirim ke Rumahmu
### Keripik Setan Mak Iyem — Rp25.000 [isian: per bungkus/ukuran]. Kirim ke Jabodetabek dan luar kota, bayar transfer atau QRIS.

**[Pesan Sekarang lewat WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini)**

## Masalahnya
Lagi pengen ngemil pedas, tapi malas keluar rumah buat nyari? Atau sudah ketemu yang enak, tapi bingung
cara pesannya dan bayarnya gimana? Di sini cukup chat lewat WhatsApp, bayar transfer atau QRIS, lalu
pesananmu dikirim.

## Kenapa Keripik Setan Mak Iyem Cocok Buat Kamu
- **Pesan tinggal chat:** semua lewat WhatsApp, tanpa ribet.
- **Bisa dikirim ke rumahmu:** Jabodetabek lewat ojol atau kurir sendiri (untuk lokasi yang dekat), luar kota lewat ekspedisi.
- **Bayar sesuai kebiasaanmu:** transfer atau QRIS.
- **Harga jelas di awal:** Rp25.000 [isian: per bungkus/ukuran, isi berapa gram].
- **Rasa dan tingkat pedas:** [isian: varian rasa/level pedas yang tersedia dan deskripsi rasa sesuai produkmu].

## Cara Pesan
1. Klik tombol WhatsApp di halaman ini.
2. Tulis jumlah pesananmu [isian: dan varian/level pedas bila ada] serta alamat pengiriman.
3. Bayar lewat transfer atau QRIS.
4. Pesananmu dikirim: Jabodetabek lewat ojol atau kurir sendiri (bila lokasimu dekat), luar kota lewat ekspedisi. Estimasi waktu: [isian: estimasi waktu kirim].

## Kata Mereka yang Sudah Coba
[ISI TESTIMONI ASLI — nama & kota pembeli. Hapus bagian ini sampai ada testimoni asli.]

## Penawaran
- Harga: Rp25.000 [isian: per bungkus/ukuran]
- Yang kamu dapat: [isian: isi/ukuran kemasan dan varian yang tersedia]
- Pengiriman: Jabodetabek (ojol atau kurir sendiri bila dekat), luar kota (ekspedisi). Ongkir: [isian: ongkir atau cara menghitung ongkir]
- Cara bayar: transfer atau QRIS

## Garansi
[isi: garansi/retur Keripik Setan Mak Iyem, hanya yang benar-benar kamu berlakukan. Hapus bagian ini bila belum ada kebijakan.]

## Pertanyaan yang Sering Ditanyakan
**Cara pesannya bagaimana?**
Klik tombol WhatsApp, tulis jumlah pesanan dan alamat pengiriman, lalu bayar lewat transfer atau QRIS.

**Bayarnya pakai apa?**
Transfer atau QRIS.

**Dikirim ke mana saja?**
Jabodetabek lewat ojol atau kurir sendiri (untuk lokasi yang dekat), luar kota lewat ekspedisi. Ongkir: [isian: ongkir atau cara menghitung ongkir].

**Ada varian atau level pedas apa saja?**
[isian: daftar varian/level pedas yang benar-benar tersedia]

**Tahan berapa lama?**
[isian: masa simpan sesuai yang tertulis di label kemasan]

## Siap Ngemil Pedas?
Pesan Keripik Setan Mak Iyem sekarang, cukup lewat WhatsApp.

**[Pesan Sekarang lewat WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini)**

## 2. Versi Pendek (Link-in-Bio / 1 Layar HP)

# Pesan Keripik Setan Mak Iyem Lewat WhatsApp
Rp25.000 [isian: per bungkus/ukuran]. Dikirim ke Jabodetabek dan luar kota, bayar transfer atau QRIS.

**[Pesan Sekarang lewat WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini)**

## 3. Variasi Headline (untuk dites bergantian)
1. **Hasil:** Pesan Keripik Pedas Mak Iyem Lewat WhatsApp, Dikirim ke Rumahmu
2. **Pertanyaan:** Lagi Pengen Ngemil Pedas? Chat Mak Iyem Sekarang
3. **Sebelum → Sesudah:** Dari "Pengen yang Pedas-Pedas" Jadi Tinggal Satu Chat WhatsApp

## 4. Meta Title & Meta Description
- Meta title: Keripik Setan Mak Iyem - Keripik Pedas Rp25.000, Pesan WA (57/60 karakter) ✅
- Meta description: Keripik Setan Mak Iyem: keripik pedas Rp25.000. Pesan lewat WhatsApp, kirim ke Jabodetabek & luar kota, bayar transfer atau QRIS. (129/155 karakter) ✅

## 5. Tautan WhatsApp
- Tautan: https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Setan%20Mak%20Iyem%20dari%20halaman%20ini
- Pesan asli (belum di-encode): Halo, saya mau pesan Keripik Setan Mak Iyem dari halaman ini

## 6. Ceklis Kepatuhan
- Izin edar (PIRT/SPP-IRT atau BPOM): belum kamu sebut → tidak ada klaim izin di halaman. Pastikan ada sebelum dijual dan dipromosikan.
- Kata "halal" tidak dipakai (belum ada sertifikat yang kamu sebut). Info dari `references/dasar-hukum-klaim.md`: UMK makanan-minuman wajib bersertifikat halal mulai 18 Okt 2026 — cek status usahamu.
- Tidak ada klaim kesehatan, testimoni, rating, angka penjualan, harga coret, hitung mundur, atau stok terbatas.
- Atribut produk (bahan, jenis keripik, ukuran, tingkat pedas, masa simpan, "tanpa pengawet") tidak ditulis karena kamu belum menyebutnya; isi hanya dengan fakta dan label kemasan yang sebenarnya.
- Janji layanan: hanya pengiriman dan cara bayar dari jawabanmu. Garansi, ongkir, dan estimasi waktu masih [isian].
- Mohon konfirmasi: nomor WA 0812-3456-7890 benar, dan kalimat "ojol atau kurir sendiri (bila lokasi dekat)" sesuai maksudmu.

## 7. Asumsi
Nada santai (sesuai jawabanmu). Satuan harga (per bungkus/ukuran) tidak diketahui → [isian]. Target pembeli
tidak disebut → halaman ditulis umum untuk pencinta camilan pedas. Ganti semua [isian] dan bagian
testimoni sebelum halaman dipublikasikan.
````

## Catatan penguji
**Karangan di contoh lama (sudah dihapus; tidak ada di input pengguna):** "keripik singkong" (meta
description), "level pedas 1–5", "tanpa pengawet", "renyah 3 bulan di suhu ruang" (headline, sub-headline,
meta title, manfaat, dan ceklis), "200gr", "kemasan tebal aman kirim luar kota", "cocok stok atau dijual
lagi", garansi "diganti atau refund maks. 1x24 jam", serta jawaban FAQ ("tahan berapa lama setelah dibuka",
"bisa campur level pedas"). Contoh lama juga meringkas bagian halaman ("Penutup + CTA diulang", "sesuai
contoh di atas") padahal SKILL.md mewajibkan seluruh isi halaman tampil di chat, dan tidak memuat pengingat
izin edar untuk pangan olahan.

**Cara menanganinya sekarang:** halaman hanya memakai fakta dari pengguna (nama, produk, harga, WA,
pengiriman, bayar, tanpa testimoni). Bahan, ukuran/satuan, varian/level pedas, masa simpan, garansi, ongkir,
dan estimasi kirim ditulis `[isian: ...]` dan dimasukkan ke FAQ/penawaran sebagai tempat mengisi. Manfaat
memakai hal yang memang diketahui (pesan lewat chat, pengiriman, cara bayar, harga jelas). Tidak ada angka
atau klaim eksternal.

**Sengaja tidak diklaim:** rasa/kerenyahan, masa simpan, bahan, pengawet, halal/izin edar, kecepatan kirim,
jumlah pelanggan, garansi.

**Diverifikasi:** tautan wa.me dan panjang meta dari script lalu dicek ulang manual (lihat atas). Semua
tautan/angka di output identik dengan hasil script. Trade-off: halaman lebih "tipis" untuk keunggulan produk
dan butuh 5 isian dari pemilik (varian, ukuran/satuan, masa simpan, ongkir/estimasi, garansi) sebelum
dipublikasikan.
