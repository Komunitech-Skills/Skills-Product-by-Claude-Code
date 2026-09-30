# Uji 08 (normal 3): Penawaran jasa servis bengkel motor

> Uji independen 2026-09-30. Script dijalankan sungguhan; angka diverifikasi ulang dengan hitungan penguji sendiri (cocok semua).

**Input pengguna:** "Bengkel motor saya di Surabaya sepi. Servis rutin + ganti oli Rp150.000. Modal oli Rp45.000, upah mekanik Rp35.000, bahan habis pakai Rp5.000. Bayar tunai/QRIS (potongan QRIS 0,3%). Mau bikin penawaran, jangan cuma diskon. Kapasitas 12 motor per hari."

## Tuas terlemah (perkiraan, bukan data)
**Keyakinan** (takut "diakali" bengkel) dan **kerepotan** (antre lama). Perbaikan: garansi servis ulang + laporan foto part yang diganti + jadwal booking.

## Hitungan
Versi A — bonus (`--harga 150000 --hpp 85000 --platform 0.3 --bonus "Cuci motor=5000;Cek aki & tekanan ban=1500" --refund 3 --margin-minimal 25`):
```
Harga tayang        : Rp150.000
Potongan platform   : -Rp450
HPP                 : -Rp85.000
Bonus Cuci motor    : -Rp5.000 (biaya modal)
Bonus Cek aki & tekanan ban: -Rp1.500 (biaya modal)
Perkiraan refund 3% : -Rp4.500
LABA per unit       : Rp53.550 (margin 35.7%)
Ruang biaya bonus maksimum agar margin >= 25%: Rp22.550 per unit; memenuhi.
```
Versi B — diskon 20% tanpa bonus: harga Rp120.000, laba **Rp31.040** (margin 25,9%), ruang bonus hanya Rp1.040.
Versi A lebih untung **Rp22.510 per motor**. Rekomendasi: versi A.

Verifikasi penguji (A): 150.000 - 450 (0,3%) - 85.000 - 6.500 - 4.500 (3%) = **53.550**; 53.550/150.000 = 35,7%; ruang = 150.000 - 450 - 85.000 - 4.500 - 37.500 = **22.550**. (B): 120.000 - 360 - 85.000 - 3.600 = **31.040**. Cocok.
Catatan: "refund 3%" di sini dipakai sebagai perkiraan biaya garansi servis ulang (asumsi; ganti dengan angka nyata bila ada).

## Penawaran: "Servis Tenang Surabaya"
- **Inti:** servis rutin + ganti oli [isi: merek & volume oli], pengecekan [isi: daftar cek].
- **Bonus:** cuci motor; cek aki & tekanan ban; foto part lama yang diganti dikirim via WA.
- **Garansi:** "Keluhan sama muncul lagi dalam 7 hari / 500 km? Servis ulang gratis (tanpa biaya part baru)." Syarat: bawa nota.
- **Batas nyata:** 12 motor per hari; booking lewat WA; slot penuh = tanggal berikutnya.
- **Nama opsi:** "Servis Tenang", "Paket Motor Sehat", "Servis Pagi Beres Siang".
- **Bayar:** tunai / QRIS.

## WhatsApp (pelanggan yang pernah servis)
> Halo Kak [nama], motornya sudah waktunya servis? Paket Servis Tenang Rp150.000: servis rutin + ganti oli, **gratis cuci motor** dan cek aki & ban. Part lama kami fotokan ke WA Kakak. Keluhan sama muncul lagi dalam 7 hari/500 km? Servis ulang gratis. Slot 12 motor per hari — mau booking jam berapa? Balas "BOOKING". (Balas STOP kalau tidak mau dikabari lagi.)

## Instagram
Pembuka (pilih satu): "Servis motor tanpa was-was part diganti diam-diam." / "Motor beres, Kakak tinggal ngopi." / "Servis sekali, dicek tiga kali."
Caption: Paket Servis Tenang Rp150.000 — servis rutin + ganti oli, gratis cuci & cek aki/ban, foto part lama via WA, garansi servis ulang 7 hari/500 km. 12 slot per hari, booking DM "BOOKING".

## Google Maps / marketplace jasa
Judul: Servis Rutin + Ganti Oli Motor — Gratis Cuci, Garansi 7 Hari
- Foto part yang diganti dikirim ke WA
- Booking jadwal, tanpa antre panjang
- Garansi servis ulang 7 hari/500 km (syarat: nota)

## Ceklis kepatuhan
Semua angka sama dengan hitungan; kuota 12/hari nyata; bonus benar diberikan; tidak ada "termurah se-Surabaya"; tidak ada testimoni karangan.

## Penilaian penguji
- Baik: dua versi dibandingkan, laba dihitung script, kelangkaan berbasis kapasitas nyata, WA hanya ke pelanggan lama + STOP.
- Temuan: bila pengguna minta nama bengkel sekaligus, tabel kelas Nice di `references/cek-merek-pdki.md` **tidak memuat kelas 37** (reparasi/servis kendaraan, juga binatu). Agent harus menebak; contoh 03 pembuat menyebut kelas 37 tapi referensi tidak.
- Temuan: script tidak punya konsep "biaya garansi jasa"; `--refund` dipakai sebagai proksi — perlu kalimat panduan untuk usaha jasa.
- Kosmetik: margin di keluaran teks memakai titik desimal ("35.7%"), sementara teks lain memakai format Indonesia.
