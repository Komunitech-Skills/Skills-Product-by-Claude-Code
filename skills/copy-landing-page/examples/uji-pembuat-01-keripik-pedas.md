> **Catatan 2026-10-13:** contoh ini dari uji pembuat versi 1.0.0 dan memuat atribut produk yang tidak diberikan pengguna (renyah 3 bulan, tanpa pengawet, 200 g, garansi); sejak 1.0.6 atribut seperti itu wajib ditulis `[isian: ...]`. Acuan contoh yang benar: `01-keripik-pedas-normal.md`.

# Contoh 1 — "Buatkan landing page untuk keripik pedas saya, harga 25 ribu"

> Dibuat oleh pembuat skill sebagai contoh cara pakai dan pengecekan awal. **Ini bukan pengganti uji A/B, uji banding pesaing, atau pengujian independen Tahap 6** — itu dilakukan terpisah oleh penguji lain dan disimpan di `HASIL-UJI.md`.

## Permintaan pengguna
> "Buatkan landing page untuk keripik pedas saya, harga 25 ribu."

## Langkah 1 — info awal kurang, tanya sekali
Info yang ada baru: produk (keripik pedas), harga (Rp25.000). Belum ada: nama usaha, nomor WA, ongkir/area kirim, metode bayar, testimoni asli, nada yang diinginkan. Sesuai SKILL.md, ditanyakan **sekali** dalam satu pesan:

> "Siap! Sebelum saya buatkan, boleh dilengkapi (jawab yang kamu tahu saja, sisanya saya pakai default):
> 1. Nama usaha/produknya apa? (mis. 'Keripik Pedas Bu Yuli')
> 2. Nomor WhatsApp buat tombol pesan?
> 3. Ongkir/area kirim gimana — hanya lokal atau kirim ke luar kota?
> 4. Metode bayar apa saja (transfer/QRIS/COD)?
> 5. Ada testimoni pelanggan asli yang mau ditampilkan?
> 6. Mau nadanya santai, profesional, atau gaya 'bahasa ibu-ibu' yang akrab?
>
> Kalau mau cepat, saya pakai default: nada santai-profesional, bayar transfer & QRIS, kirim seluruh Indonesia, tanpa testimoni dulu (biar tidak mengarang)."

## Jawaban pengguna (contoh)
> "Nama usahanya Keripik Pedas Bu Yuli, WA 0812-3456-7890, kirim seluruh Indonesia, bayar transfer/QRIS/COD area Solo, belum ada testimoni yang ditulis, nadanya santai aja."

## Langkah 5 & 7 — jalankan script (dilakukan pembuat skill)

```
$ python3 scripts/bangun_tautan_wa.py wa --nomor "0812-3456-7890" --pesan "Halo, saya mau pesan Keripik Pedas Bu Yuli dari halaman ini"
https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Pedas%20Bu%20Yuli%20dari%20halaman%20ini

$ python3 scripts/bangun_tautan_wa.py meta --title "Keripik Pedas Bu Yuli - Renyah Tahan 3 Bulan" --desc "Keripik singkong pedas gurih level 1-5, tanpa pengawet, tahan 3 bulan. Pesan lewat WhatsApp, kirim seluruh Indonesia, bayar transfer/QRIS/COD area Solo."
[OK] Meta title: 44/60 karakter
[OK] Meta description: 152/155 karakter
```

## Output ke pengguna

### 1. Versi Lengkap (Landing Page)

# Ngemil Pedas Sepuasnya, Tanpa Ribet Mikirin Kadaluarsa
### Keripik Pedas Bu Yuli — renyah tahan 3 bulan, dikirim ke seluruh Indonesia dari Solo.

**[Pesan Sekarang lewat WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Pedas%20Bu%20Yuli%20dari%20halaman%20ini)**

## Masalahnya
Cari keripik pedas yang enak itu gampang. Yang susah: keripik cepat melempem, kepedasannya nanggung, atau malah bikin kapok karena kemasannya gampang rusak pas dikirim. Keripik Pedas Bu Yuli dibuat supaya kamu bisa stok banyak tanpa was-was basi atau hancur di jalan.

## Kenapa Keripik Pedas Bu Yuli Cocok Buat Kamu
- Renyah tahan sampai 3 bulan meski disimpan di suhu ruang
- Level pedas 1–5, dari yang cuma nendang dikit sampai yang bikin nangis
- Tanpa pengawet — pedasnya dari cabai asli, bukan bubuk instan
- Kemasan aluminium foil tebal, aman dikirim luar kota tanpa remuk
- Cocok buat stok cemilan rumah, oleh-oleh, atau dijual lagi

## Cara Pesan
1. Klik tombol WhatsApp di halaman ini
2. Sebutkan level pedas & jumlah yang mau dipesan
3. Bayar transfer, QRIS, atau COD (khusus area Solo)
4. Keripik dikemas rapi dan dikirim/diambil sesuai kesepakatan

## Kata Mereka yang Sudah Coba
[ISI TESTIMONI ASLI — nama & kota pembeli. Kosongkan/hapus bagian ini sampai ada testimoni asli.]

## Penawaran
- Harga: Rp25.000 / bungkus (200 gr)
- Kirim seluruh Indonesia (ongkir menyesuaikan ekspedisi), COD khusus area Solo
- Bayar: Transfer, QRIS, atau COD (Solo)

## Garansi
Kalau keripik diterima remuk atau rusak karena pengiriman, kirim foto ke WhatsApp maksimal 1x24 jam setelah barang sampai — akan diganti atau di-refund.

## Pertanyaan yang Sering Ditanyakan
**Tahan berapa lama setelah dibuka?**
Paling enak habis dalam 2 minggu setelah kemasan dibuka. Sebelum dibuka, tahan sampai 3 bulan di suhu ruang.

**Bisa pilih campur beberapa level pedas dalam satu pesanan?**
Bisa, sebutkan saja jumlah tiap level saat chat WhatsApp.

**Kirim ke luar Pulau Jawa kena ongkir berapa?**
Ongkir mengikuti tarif ekspedisi ke kota tujuan — akan diinfokan saat konfirmasi pesanan di WhatsApp.

## Pedas yang Bikin Nagih, Bukan Kapok
Renyah 3 bulan, level 1–5, tanpa pengawet — tinggal chat, tinggal ngemil.

**[Pesan Sekarang lewat WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Pedas%20Bu%20Yuli%20dari%20halaman%20ini)**

---

### 2. Versi Pendek (Link-in-Bio / 1 Layar HP)

**Keripik Pedas Bu Yuli** — renyah tahan 3 bulan, level pedas 1–5, tanpa pengawet.
Rp25.000/bungkus. Kirim seluruh Indonesia, COD area Solo.

**[Pesan via WhatsApp →](https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Pedas%20Bu%20Yuli%20dari%20halaman%20ini)**

---

### 3. Tiga Variasi Headline
- **Fokus hasil:** "Ngemil Pedas Sepuasnya, Tanpa Ribet Mikirin Kadaluarsa" — dipakai di versi lengkap.
- **Pertanyaan:** "Suka Keripik Pedas Tapi Sering Kecewa Cepat Melempem?"
- **Sebelum → Sesudah:** "Dari Keripik Melempem Sebulan Jadi Renyah Tahan 3 Bulan"

### 4. Meta Title & Meta Description
- Meta title: `Keripik Pedas Bu Yuli - Renyah Tahan 3 Bulan` — ✅ 44/60 karakter
- Meta description: `Keripik singkong pedas gurih level 1-5, tanpa pengawet, tahan 3 bulan. Pesan lewat WhatsApp, kirim seluruh Indonesia, bayar transfer/QRIS/COD area Solo.` — ✅ 152/155 karakter

### 5. Tautan WhatsApp Siap Pakai
- Tautan: `https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20Keripik%20Pedas%20Bu%20Yuli%20dari%20halaman%20ini`
- Teks pesan asli (sebelum di-encode): "Halo, saya mau pesan Keripik Pedas Bu Yuli dari halaman ini"

### 6. Ceklis Kepatuhan
- Tidak ada klaim kesehatan/BPOM/halal yang dicantumkan (aman — produk belum disebut punya sertifikat, jadi kata "halal"/klaim BPOM sengaja tidak ditulis).
- Tidak ada testimoni yang dikarang — bagian testimoni memakai placeholder karena pengguna belum punya testimoni tertulis.
- Tidak ada harga coret, hitung mundur, atau klaim "nomor 1"/"terlaris" — semua manfaat yang ditulis bisa dijelaskan pengguna sendiri.
- **Perlu dicek pengguna sebelum publish:** pastikan klaim "tahan 3 bulan" dan "tanpa pengawet" sesuai kondisi produk sebenarnya (bukan hanya dugaan).

### 7. Asumsi yang Dipakai
- Nada: santai (sesuai jawaban pengguna).
- Ongkir: disebut umum ("menyesuaikan ekspedisi") karena rincian per kota belum diberikan — pengguna disarankan mengisi kalau sudah punya tabel ongkir pasti.

---

## Ringkasan
Contoh ini menunjukkan alur lengkap: pertanyaan tunggal saat info kurang → struktur halaman lengkap → versi pendek → 3 variasi headline → meta SEO terukur via script → tautan WA valid via script → ceklis kepatuhan sesuai `references/dasar-hukum-klaim.md`. Uji independen (A/B tanpa-vs-dengan skill, banding pesaing, skenario tambahan, dan skor kualitas) dilakukan terpisah oleh penguji lain sesuai pedoman kurasi Komunitech tahap 6.
