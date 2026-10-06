# Skenario 2 (normal kedua): diskon persen + DP, pengingat bayar & pesan resi

**Input:** `data/pesan-skenario-2.txt`.

**Hitung ulang independen:** Rahma 495.000 − 49.500 + 18.000 = 463.500, sisa 263.500. Joko 435.000 − 54.375 (12,5%) + 25.000 = 405.625, sisa 255.625. Mega 315.000 − 15.750 + 15.000 = 314.250, lunas. Omzet 1.125.375, tagihan 1.183.375, belum bayar 519.125. Semua cocok.

## Output SESUDAH

````
Berikut rekap 3 pesanan kue lebaran **Dapur Bunda Ani** hari ini (2026-10-06), lengkap dengan pesan konfirmasi, nota, label kirim, serah-terima kurir, pengingat bayar, dan pesan resi.

**Ringkasan:** 3 pesanan, total tagihan **Rp1.183.375**. Kak Mega sudah lunas & terkirim; Bu Rahma dan Pak Joko masih kurang bayar (DP saja).

---

## 1) Bu Rahma — kode `20261006-01`
**Rekap**
- Nastar 500g x3 @Rp95.000 = Rp285.000
- Kastengel 500g x2 @Rp105.000 = Rp210.000
- Subtotal: Rp495.000
- Diskon langganan (10%): −Rp49.500
- Ongkir JNE REG: Rp18.000
- **TOTAL: Rp463.500**
- Sudah DP: Rp200.000 → **Sisa: Rp263.500**
- Status: dibayar sebagian

**Pesan konfirmasi (siap kirim):**
```
Halo Kak Rahma, terima kasih sudah order di Dapur Bunda Ani 🙏
Pesanannya kami rekap ya:

20261006-01
• Nastar 500g x3 = Rp285.000
• Kastengel 500g x2 = Rp210.000
Subtotal: Rp495.000
Diskon langganan: -Rp49.500
Ongkir JNE REG: Rp18.000
*Total: Rp463.500*

Sudah kami terima DP Rp200.000, sisa yang perlu dilunasi: *Rp263.500*
Transfer ke:
BRI 0987-01-000123-50-1 a.n. Ani Suryani
Mohon kirim bukti transfernya di chat ini ya, Kak.

Supaya paket tidak nyasar, boleh dilengkapi:
1. Alamat lengkap (jalan, RT/RW, kelurahan, kecamatan, kota, kode pos)
2. Nomor HP penerima yang aktif

Terima kasih, Kak 😊
```

**Nota:**
```
NOTA PESANAN — Dapur Bunda Ani
No.     : 20261006-01
Tanggal : 2026-10-06
Kepada  : Bu Rahma

Nastar 500g x3 @Rp95.000      Rp285.000
Kastengel 500g x2 @Rp105.000  Rp210.000
Subtotal                 Rp495.000
Diskon langganan 10%    -Rp49.500
Ongkir JNE REG            Rp18.000
TOTAL                    Rp463.500
Status : BELUM LUNAS (sisa Rp263.500)
Bayar ke: BRI 0987-01-000123-50-1 a.n. Ani Suryani

Terima kasih sudah berbelanja 🙏
```

**Label:**
```
================================
KEPADA : Bu Rahma
HP     : [isian: HP penerima]
ALAMAT : [isian: alamat lengkap]
--------------------------------
DARI   : Dapur Bunda Ani
ISI    : Nastar 500g x3, Kastengel 500g x2
KURIR  : JNE REG     RESI: [isian: resi]
NON-COD
No. pesanan: 20261006-01
================================
```

---

## 2) Pak Joko — kode `20261006-02`
**Rekap**
- Putri Salju 500g x4 @Rp85.000 = Rp340.000
- Nastar 500g x1 @Rp95.000 = Rp95.000
- Subtotal: Rp435.000
- Diskon reseller (12,5%): −Rp54.375
- Ongkir J&T: Rp25.000
- **TOTAL: Rp405.625**
- Sudah DP: Rp150.000 → **Sisa: Rp255.625**
- Status: dibayar sebagian

**Pesan konfirmasi (siap kirim):**
```
Halo Pak Joko, terima kasih sudah order di Dapur Bunda Ani 🙏
Pesanannya kami rekap ya:

20261006-02
• Putri Salju 500g x4 = Rp340.000
• Nastar 500g x1 = Rp95.000
Subtotal: Rp435.000
Diskon reseller: -Rp54.375
Ongkir J&T: Rp25.000
*Total: Rp405.625*

Sudah kami terima DP Rp150.000, sisa yang perlu dilunasi: *Rp255.625*
Transfer ke:
BRI 0987-01-000123-50-1 a.n. Ani Suryani
Mohon kirim bukti transfernya di chat ini ya, Pak.

Supaya paket tidak nyasar, boleh dilengkapi:
1. Alamat lengkap (jalan, RT/RW, kelurahan, kecamatan, kota, kode pos)
2. Nomor HP penerima yang aktif

Terima kasih 😊
```

**Nota:**
```
NOTA PESANAN — Dapur Bunda Ani
No.     : 20261006-02
Tanggal : 2026-10-06
Kepada  : Pak Joko

Putri Salju 500g x4 @Rp85.000  Rp340.000
Nastar 500g x1 @Rp95.000       Rp95.000
Subtotal                 Rp435.000
Diskon reseller 12,5%   -Rp54.375
Ongkir J&T                Rp25.000
TOTAL                    Rp405.625
Status : BELUM LUNAS (sisa Rp255.625)
Bayar ke: BRI 0987-01-000123-50-1 a.n. Ani Suryani

Terima kasih sudah berbelanja 🙏
```

**Label:**
```
================================
KEPADA : Pak Joko
HP     : [isian: HP penerima]
ALAMAT : [isian: alamat lengkap]
--------------------------------
DARI   : Dapur Bunda Ani
ISI    : Putri Salju 500g x4, Nastar 500g x1
KURIR  : J&T     RESI: [isian: resi]
NON-COD
No. pesanan: 20261006-02
================================
```

---

## 3) Kak Mega — kode `20261006-03` (LUNAS & sudah dikirim ✅)
**Rekap**
- Kastengel 500g x3 @Rp105.000 = Rp315.000
- Subtotal: Rp315.000
- Diskon (5%): −Rp15.750
- Ongkir JNE REG: Rp15.000
- **TOTAL: Rp314.250**
- Dibayar: Rp299.250 + ongkir Rp15.000 = Rp314.250 ✅ **cocok pas, lunas**

**Pesan resi (siap kirim ke Kak Mega):**
```
Halo Kak Mega, pesanan 20261006-03 (Kastengel 500g x3) sudah kami kirim hari ini lewat JNE REG 📦
No. resi: 0123 4567 8910 11
Bisa dilacak di aplikasi/situs resmi JNE.
Terima kasih sudah belanja di Dapur Bunda Ani!
```

**Nota:**
```
NOTA PESANAN — Dapur Bunda Ani
No.     : 20261006-03
Tanggal : 2026-10-06
Kepada  : Kak Mega

Kastengel 500g x3 @Rp105.000   Rp315.000
Subtotal                 Rp315.000
Diskon 5%                -Rp15.750
Ongkir JNE REG             Rp15.000
TOTAL                    Rp314.250
Status : LUNAS
Bayar ke: BRI 0987-01-000123-50-1 a.n. Ani Suryani

Terima kasih sudah berbelanja 🙏
```

---

## Serah-terima kurir hari ini
```
SERAH-TERIMA JNE — 2026-10-06
Toko: Dapur Bunda Ani
No | Kode         | Penerima | Layanan | Isi                              | COD | Resi
1  | 20261006-01  | Bu Rahma | REG     | Nastar x3, Kastengel x2          | -   | [isian: resi]
2  | 20261006-03  | Kak Mega | REG     | Kastengel x3                     | -   | 0123 4567 8910 11
Jumlah paket: 2   Total nilai COD: -

SERAH-TERIMA J&T — 2026-10-06
Toko: Dapur Bunda Ani
No | Kode         | Penerima | Layanan | Isi                              | COD | Resi
1  | 20261006-02  | Pak Joko | -       | Putri Salju x4, Nastar x1        | -   | [isian: resi]
Jumlah paket: 1   Total nilai COD: -
```

## Pengingat bayar (untuk dikirim sendiri ke pelanggan)
**Ke Bu Rahma:**
```
Halo Kak Rahma, sekadar mengingatkan pesanan 20261006-01 (Nastar 3, Kastengel 2) sebesar Rp463.500 — sudah kami terima Rp200.000, kurang Rp263.500.
Transfer ke BRI 0987-01-000123-50-1 a.n. Ani Suryani. Kalau sudah transfer, boleh kirim bukti transfernya ya, Kak, biar langsung kami kemas.
Terima kasih 🙏
```

**Ke Pak Joko:**
```
Halo Pak Joko, sekadar mengingatkan pesanan 20261006-02 (Putri Salju 4, Nastar 1) sebesar Rp405.625 — sudah kami terima Rp150.000, kurang Rp255.625.
Transfer ke BRI 0987-01-000123-50-1 a.n. Ani Suryani. Kalau sudah transfer, boleh kirim bukti transfernya ya, Pak, biar langsung kami kemas.
Terima kasih 🙏
```

---

## Rekap harian (tanpa HP & alamat)
- Jumlah pesanan: 3 (3 angka lengkap)
- Omzet barang: Rp1.125.375
- Ongkir ditagihkan: Rp58.000
- **Total tagihan: Rp1.183.375**
- Terlaris: Kastengel 500g (5), Nastar 500g (4), Putri Salju 500g (4)
- Belum bayar: 2 pesanan, total sisa **Rp519.125**
  - 20261006-01 Bu Rahma: sisa Rp263.500
  - 20261006-02 Pak Joko: sisa Rp255.625
- COD: tidak ada

**CSV:**
```
kode,tanggal,pelanggan,isi_pesanan,jumlah_barang,subtotal,diskon,ongkir,total,kurir,layanan,cod,status_bayar,sisa_tagihan
20261006-01,2026-10-06,Bu Rahma,"Nastar 500g x3, Kastengel 500g x2",5,495000,49500,18000,463500,JNE,REG,tidak,dibayar sebagian,263500
20261006-02,2026-10-06,Pak Joko,"Putri Salju 500g x4, Nastar 500g x1",5,435000,54375,25000,405625,J&T,,tidak,dibayar sebagian,255625
20261006-03,2026-10-06,Kak Mega,Kastengel 500g x3,3,315000,15750,15000,314250,JNE,REG,tidak,lunas,0
```

---

**Asumsi:** diskon "langganan" (Rahma) dan "reseller" (Joko) dihitung dari subtotal barang saja (sebelum ongkir); pembayaran Rahma & Joko dianggap DP/sebagian, bukan pembayaran salah hitung.

**Pertanyaan (maks 3):**
1. Alamat lengkap + no. HP penerima untuk Bu Rahma dan Pak Joko — belum ada di chat, jadi labelnya masih kosong.
2. Resi untuk paket Bu Rahma (JNE) dan Pak Joko (J&T) — kalau sudah dikirim, kabari ya biar pesan susulannya langsung dibuatkan.
3. Ada batas waktu pelunasan DP yang mau disebut ke Bu Rahma/Pak Joko (mis. H-3 sebelum kirim)?````

## Catatan
- Resi dari pengguna dipakai apa adanya; resi lain `[isian: resi]`.
- Minor: sapaan 'Kak Rahma' (chat: 'Bu Rahma'); paket belum lunas ikut daftar serah-terima.
