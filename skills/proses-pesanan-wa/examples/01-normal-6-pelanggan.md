# Skenario 1 (normal utama): 6 pelanggan, chat WA berantakan

**Input:** `data/pesan-skenario-1.txt` (katalog 5 produk, ongkir 3 kota, 7 baris chat: Rina kirim dua kali, Dewi alamat menyusul, Sinta COD J&T, Fitri minta warna 'sage' yang tidak ada, Ayu ambil sendiri, Bu Ratna sudah lunas).

**Hitung ulang independen:** Rina Rp177.000, Sinta Rp169.000 (COD), Dewi Rp127.000, Fitri bergo navy Rp35.000 + ongkir Rp12.000 (pashmina sage tidak dihitung), Ayu Rp95.000, Ratna Rp280.000 lunas. Omzet (5 pesanan lengkap) Rp782.000, ongkir Rp66.000, tagihan Rp848.000, belum bayar Rp399.000. Terlaris: Bros Mutiara 8, Inner Ninja 5. Semua cocok dengan jawaban agent (kedua konteks).

## Output SESUDAH (konteks lokal)

````
Sudah saya proses semua chat masuk tanggal **06/10/2026** pakai daftar harga Nayla Hijab. Hasilnya lengkap di bawah — tinggal salin dan kirim.

## Ringkasan
6 pesanan masuk (1 chat dobel dari Rina sudah digabung jadi 1). Total tagihan hari ini **Rp848.000** dari 5 pesanan yang angka-nya sudah pasti; 1 pesanan (Fitri) masih menunggu konfirmasi warna. Belum bayar: 4 pesanan (Rp399.000 + 1 belum pasti), COD: 1 pesanan, lunas: 1 pesanan (Bu Hj. Ratna).

---

## 1) Rina Bdg — `20261006-01`
**Rekap:** Pashmina Ceruty Babydoll Mocca x2 = Rp90.000; Pashmina Ceruty Babydoll Dusty Pink x1 = Rp45.000; Bros Mutiara x3 = Rp30.000 | Subtotal Rp165.000 | Ongkir JNE REG Rp12.000 | **Total Rp177.000** | Belum bayar | JNE REG
*(Chat jam 08.12 & 09.20 isinya sama → dihitung satu kali)*

```
Halo Kak Rina, terima kasih sudah order di Nayla Hijab 🙏
Pesanan yang tadi pagi sudah kami terima ya, tidak perlu dikirim ulang 😊

20261006-01
• Pashmina Ceruty Babydoll Mocca x2 = Rp90.000
• Pashmina Ceruty Babydoll Dusty Pink x1 = Rp45.000
• Bros Mutiara x3 = Rp30.000
Subtotal: Rp165.000
Ongkir JNE REG: Rp12.000
*Total: Rp177.000*

Pembayaran via transfer ke:
BCA 1234567890 a.n. Nayla Putri
Mohon transfer sesuai total, lalu kirim bukti transfernya di chat ini ya, Kak.

Terima kasih, Kak 😊
```

```
NOTA PESANAN — Nayla Hijab
No.     : 20261006-01
Tanggal : 2026-10-06
Kepada  : Rina Bdg

Pashmina Ceruty Babydoll Mocca x2 @Rp45.000       Rp90.000
Pashmina Ceruty Babydoll Dusty Pink x1 @Rp45.000  Rp45.000
Bros Mutiara x3 @Rp10.000                         Rp30.000
Subtotal                 Rp165.000
Ongkir JNE REG            Rp12.000
TOTAL                    Rp177.000
Status : BELUM BAYAR
Bayar ke: BCA 1234567890 a.n. Nayla Putri

Terima kasih sudah berbelanja 🙏
```

```
KEPADA : Rina Marlina
HP     : 0812-2233-4455
ALAMAT : Jl. Cigadung Raya Timur No. 45 RT02/RW05, Kel. Cigadung, Kec. Cibeunying Kaler, Bandung 40191
--------------------------------
DARI   : Nayla Hijab | 0811-2000-3000
ISI    : Pashmina Ceruty Babydoll Mocca x2, Pashmina Ceruty Babydoll Dusty Pink x1, Bros Mutiara x3
KURIR  : JNE REG          RESI: [isian: resi]
NON-COD
CATATAN: -
No. pesanan: 20261006-01
================================
```

---

## 2) Sinta — `20261006-02`
**Rekap:** Gamis Rayon Polos L x1 = Rp129.000; Inner Ninja Rajut x2 = Rp30.000 | Subtotal Rp159.000 | Ongkir J&T Rp10.000 | **Total Rp169.000** | COD | J&T

```
Halo Kak Sinta, terima kasih sudah order di Nayla Hijab 🙏
Pesanannya kami rekap ya:

20261006-02
• Gamis Rayon Polos L x1 = Rp129.000
• Inner Ninja Rajut x2 = Rp30.000
Subtotal: Rp159.000
Ongkir J&T: Rp10.000
*Total: Rp169.000*

Pembayaran *COD* sebesar Rp169.000 dibayar ke kurir saat paket diterima (J&T COD). Mohon pastikan ada yang menerima di alamat ya, Kak.

Terima kasih, Kak 😊
```

```
NOTA PESANAN — Nayla Hijab
No.     : 20261006-02
Tanggal : 2026-10-06
Kepada  : Sinta

Gamis Rayon Polos L x1 @Rp129.000   Rp129.000
Inner Ninja Rajut x2 @Rp15.000      Rp30.000
Subtotal                 Rp159.000
Ongkir J&T                Rp10.000
TOTAL                    Rp169.000
Status : COD
Bayar ke: bayar ke kurir saat barang diterima

Terima kasih sudah berbelanja 🙏
```

```
KEPADA : Sinta
HP     : 0857-1122-3344
ALAMAT : Jl. Kemang Pratama Raya Blok AB No. 12 RT 005/RW 012, Bojong Rawalumbu, Rawalumbu, Kota Bekasi 17116
--------------------------------
DARI   : Nayla Hijab | 0811-2000-3000
ISI    : Gamis Rayon Polos L x1, Inner Ninja Rajut x2
KURIR  : J&T COD         RESI: [isian: resi]
COD Rp169.000 — bayar ke kurir
CATATAN: -
No. pesanan: 20261006-02
================================
```

---

## 3) Mbak Dewi — `20261006-03`  ⚠️ data kirim belum lengkap
**Rekap:** Bergo Instan Jersey Coklat x2 = Rp70.000; Bergo Instan Jersey Hitam x1 = Rp35.000 | Subtotal Rp105.000 | Ongkir (Surabaya) Rp22.000 | **Total Rp127.000** | Belum bayar | Kurir belum dipilih

```
Halo Kak Dewi, terima kasih sudah order di Nayla Hijab 🙏
Pesanannya kami rekap ya:

20261006-03
• Bergo Instan Jersey Coklat x2 = Rp70.000
• Bergo Instan Jersey Hitam x1 = Rp35.000
Subtotal: Rp105.000
Ongkir (Surabaya): Rp22.000
*Total: Rp127.000*

Pembayaran via transfer ke:
BCA 1234567890 a.n. Nayla Putri
Mohon transfer sesuai total, lalu kirim bukti transfernya di chat ini ya, Kak.

Supaya paket tidak nyasar, boleh dilengkapi:
1. Alamat lengkap (jalan & nomor rumah, RT/RW, kelurahan, kecamatan, kode pos)
2. Pilih kurir: JNE atau J&T ya, Kak

Terima kasih, Kak 😊
```

```
NOTA PESANAN — Nayla Hijab
No.     : 20261006-03
Tanggal : 2026-10-06
Kepada  : Mbak Dewi

Bergo Instan Jersey Coklat x2 @Rp35.000   Rp70.000
Bergo Instan Jersey Hitam x1 @Rp35.000    Rp35.000
Subtotal                 Rp105.000
Ongkir (Surabaya)         Rp22.000
TOTAL                    Rp127.000
Status : BELUM BAYAR
Bayar ke: BCA 1234567890 a.n. Nayla Putri

Terima kasih sudah berbelanja 🙏
```

```
KEPADA : Dewi
HP     : 0813-3344-5566
ALAMAT : [isian: alamat lengkap dari Kak Dewi — belum dikirim]
--------------------------------
DARI   : Nayla Hijab | 0811-2000-3000
ISI    : Bergo Instan Jersey Coklat x2, Bergo Instan Jersey Hitam x1
KURIR  : [isian: JNE/J&T]        RESI: [isian: resi]
NON-COD
CATATAN: menunggu alamat & pilihan kurir
No. pesanan: 20261006-03
================================
```

---

## 4) Fitri — `20261006-04`  ⚠️ varian tidak ada
Warna **sage** tidak ada di daftar harga (pashmina hanya hitam/mocca/dusty pink) — item pashmina belum dihitung, sudah ditanyakan ke pelanggan.

**Rekap (yang pasti saja):** Bergo Instan Jersey Navy x1 = Rp35.000 | Ongkir JNE REG Rp12.000 | Total: **menunggu pilihan warna pashmina**

```
Halo Kak Fitri, terima kasih sudah order di Nayla Hijab 🙏
Mohon maaf, warna *sage* untuk Pashmina Ceruty Babydoll belum ada ya, Kak. Yang tersedia: hitam, mocca, dusty pink.

Sementara kami rekap yang sudah pasti (kode 20261006-04):
• Bergo Instan Jersey Navy x1 = Rp35.000
Ongkir JNE REG: Rp12.000

Total akan kami kabari setelah warna pashmina-nya dikonfirmasi ya, Kak.

Boleh pilih salah satu warna pashmina: hitam / mocca / dusty pink, Kak?

Terima kasih, Kak 😊
```

```
NOTA PESANAN — Nayla Hijab
No.     : 20261006-04
Tanggal : 2026-10-06
Kepada  : Fitri

Bergo Instan Jersey Navy x1 @Rp35.000             Rp35.000
Pashmina Ceruty Babydoll [isian: warna] x2 @Rp45.000  [isian]
Subtotal                 [isian: subtotal]
Ongkir JNE REG            Rp12.000
TOTAL                    [isian: total]
Status : BELUM BAYAR (menunggu konfirmasi warna)
Bayar ke: BCA 1234567890 a.n. Nayla Putri
```

```
KEPADA : Fitri
HP     : 0899-1122-3344
ALAMAT : Jl. Dago No. 120 RT 03/RW 02, Kel. Lebakgede, Kec. Coblong, Bandung 40132
--------------------------------
DARI   : Nayla Hijab | 0811-2000-3000
ISI    : Bergo Instan Jersey Navy x1, Pashmina Ceruty Babydoll [isian: warna pengganti] x2
KURIR  : JNE REG          RESI: [isian: resi]
NON-COD
CATATAN: menunggu pilihan warna pashmina (sage tidak tersedia)
No. pesanan: 20261006-04
================================
```

---

## 5) Ayu — `20261006-05` (ambil sendiri)
**Rekap:** Bros Mutiara x5 = Rp50.000; Inner Ninja Rajut x3 = Rp45.000 | Subtotal Rp95.000 | Ongkir - | **Total Rp95.000**

```
Halo Kak Ayu, terima kasih sudah order di Nayla Hijab 🙏
Pesanannya kami rekap ya:

20261006-05
• Bros Mutiara x5 = Rp50.000
• Inner Ninja Rajut x3 = Rp45.000
Subtotal: Rp95.000
*Total: Rp95.000*

Pesanan bisa diambil di toko sore ini ya, Kak. Pembayaran bisa langsung di tempat saat ambil.

Terima kasih, Kak 😊
```

```
NOTA PESANAN — Nayla Hijab
No.     : 20261006-05
Tanggal : 2026-10-06
Kepada  : Ayu

Bros Mutiara x5 @Rp10.000          Rp50.000
Inner Ninja Rajut x3 @Rp15.000     Rp45.000
Subtotal                 Rp95.000
Ongkir (ambil sendiri)    Rp0
TOTAL                    Rp95.000
Status : BELUM BAYAR (bayar di tempat saat ambil)

Terima kasih sudah berbelanja 🙏
```
*(Ambil sendiri → tidak perlu label pengiriman)*

---

## 6) Bu Hj. Ratna — `20261006-06` ✅ LUNAS
**Rekap:** Gamis Rayon Polos XL x2 = Rp258.000 | Subtotal Rp258.000 | Ongkir JNE REG Rp22.000 | **Total Rp280.000** | Lunas | JNE REG

```
Walaikumsalam Bu Hj. Ratna, terima kasih sudah order di Nayla Hijab 🙏
Pesanannya kami rekap ya:

20261006-06
• Gamis Rayon Polos XL x2 = Rp258.000
Subtotal: Rp258.000
Ongkir JNE REG: Rp22.000
*Total: Rp280.000*

Transfer sudah kami terima, *LUNAS* ya, Bu. Pesanan segera kami siapkan dan kirim. Terima kasih 🙏
```

```
NOTA PESANAN — Nayla Hijab
No.     : 20261006-06
Tanggal : 2026-10-06
Kepada  : Bu Hj. Ratna

Gamis Rayon Polos XL x2 @Rp129.000   Rp258.000
Subtotal                 Rp258.000
Ongkir JNE REG            Rp22.000
TOTAL                    Rp280.000
Status : LUNAS
Bayar ke: BCA 1234567890 a.n. Nayla Putri

Terima kasih sudah berbelanja 🙏
```

```
KEPADA : Bu Hj. Ratna
HP     : 0813-5577-8899
ALAMAT : Jl. Rungkut Asri Tengah No. 8, Kel. Rungkut Kidul, Kec. Rungkut, Surabaya 60293
--------------------------------
DARI   : Nayla Hijab | 0811-2000-3000
ISI    : Gamis Rayon Polos XL x2
KURIR  : JNE REG          RESI: [isian: resi]
NON-COD
CATATAN: -
No. pesanan: 20261006-06
================================
```

---

## Serah-terima kurir

**JNE REG — 3 paket**
| No | Kode | Penerima | Isi | COD | Resi |
|---|---|---|---|---|---|
| 1 | 20261006-01 | Rina Marlina | Pashmina Mocca x2, Pashmina Dusty x1, Bros x3 | - | [isian: resi] |
| 2 | 20261006-04 | Fitri | Bergo Navy x1 (+ pashmina, menunggu warna) | - | [isian: resi] |
| 3 | 20261006-06 | Bu Hj. Ratna | Gamis XL x2 | - | [isian: resi] |

**J&T COD — 1 paket**
| No | Kode | Penerima | Isi | COD | Resi |
|---|---|---|---|---|---|
| 1 | 20261006-02 | Sinta | Gamis L x1, Inner x2 | Rp169.000 | [isian: resi] |

**Kurir belum dipilih — 1 paket**
| No | Kode | Penerima | Isi | COD | Resi |
|---|---|---|---|---|---|
| 1 | 20261006-03 | Dewi | Bergo Coklat x2, Bergo Hitam x1 | - | [isian: resi] |

**Ambil sendiri (bukan lewat kurir):** Ayu (20261006-05)

Total paket lewat kurir: 5 | Total nilai COD: Rp169.000

---

## Pesan susulan (isi setelah ada resi / saat kirim)
```
Halo Kak [nama], pesanan [kode] sudah kami kirim hari ini lewat [kurir layanan] 📦
No. resi: [isian: resi]
Bisa dilacak di aplikasi/situs resmi [kurir].
Terima kasih sudah belanja di Nayla Hijab!
```

**Pengingat bayar (siap pakai bila belum transfer sore ini):**
```
Halo Kak Rina, sekadar mengingatkan pesanan 20261006-01 (pashmina & bros) sebesar *Rp177.000* belum kami terima pembayarannya.
Transfer ke BCA 1234567890 a.n. Nayla Putri. Kalau sudah transfer, boleh kirim bukti transfernya ya, Kak.
Terima kasih 🙏
```
```
Halo Kak Dewi, sekadar mengingatkan pesanan 20261006-03 (bergo jersey) sebesar *Rp127.000* belum kami terima pembayarannya. Alamat & pilihan kurirnya juga masih kami tunggu ya, Kak.
Transfer ke BCA 1234567890 a.n. Nayla Putri. Terima kasih 🙏
```

---

## Rekap harian (06/10/2026) — tanpa HP & alamat
- Jumlah pesanan: 6 (5 angka lengkap, 1 menunggu konfirmasi warna: 20261006-04)
- Omzet barang: **Rp782.000**
- Ongkir ditagihkan: **Rp66.000**
- Total tagihan: **Rp848.000**
- Terlaris: Bros Mutiara (8), Inner Ninja Rajut (5), Bergo Instan Jersey Coklat (2), Gamis Rayon Polos XL (2), Pashmina Ceruty Babydoll Mocca (2)
- Belum bayar: 4 pesanan, Rp399.000 pasti + 1 belum pasti
  - 20261006-01 Rina Bdg — Rp177.000
  - 20261006-03 Mbak Dewi — Rp127.000
  - 20261006-04 Fitri — [isian: total, menunggu warna]
  - 20261006-05 Ayu — Rp95.000 (bayar di tempat saat ambil)
- COD: 1 paket — 20261006-02 Sinta, Rp169.000
- Lunas: 20261006-06 Bu Hj. Ratna, Rp280.000
- Stok kurang: tidak ada data stok, jadi tidak dicek

**CSV (tempel ke spreadsheet):**
```
kode,tanggal,pelanggan,isi_pesanan,jumlah_barang,subtotal,diskon,ongkir,total,kurir,layanan,cod,status_bayar,sisa_tagihan
20261006-01,2026-10-06,Rina Bdg,"Pashmina Ceruty Babydoll Mocca x2, Pashmina Ceruty Babydoll Dusty Pink x1, Bros Mutiara x3",6,165000,0,12000,177000,JNE,REG,tidak,belum bayar,177000
20261006-02,2026-10-06,Sinta,"Gamis Rayon Polos L x1, Inner Ninja Rajut x2",3,159000,0,10000,169000,J&T,COD,ya,COD (bayar saat terima),169000
20261006-03,2026-10-06,Mbak Dewi,"Bergo Instan Jersey Coklat x2, Bergo Instan Jersey Hitam x1",3,105000,0,22000,127000,,,tidak,belum bayar,127000
20261006-04,2026-10-06,Fitri,"pashmina sage x2, Bergo Instan Jersey Navy x1",3,,0,12000,,JNE,REG,tidak,belum bayar,
20261006-05,2026-10-06,Ayu,"Bros Mutiara x5, Inner Ninja Rajut x3",8,95000,0,0,95000,Ambil sendiri,,tidak,belum bayar,95000
20261006-06,2026-10-06,Bu Hj. Ratna,Gamis Rayon Polos XL x2,2,258000,0,22000,280000,JNE,REG,tidak,lunas,0
```

---

## Asumsi yang saya pakai
- Chat Rina jam 08.12 dan 09.20 dianggap pesanan yang sama (dikirim ulang), dihitung satu kali.
- Ongkir pakai tarif dari daftar harga sesuai tujuan kota (Bandung 12rb, Bekasi 10rb, Surabaya 22rb); Dewi diasumsikan ke Surabaya sesuai yang disebut di chat.
- Bu Hj. Ratna: transfer Rp280.000 pas sama total, jadi ditandai lunas sesuai konfirmasi "sudah masuk" dari kakak.

## Pertanyaan untuk kakak (maks. 3)
1. Order Ayu ambil sendiri sore ini — bayar langsung di tempat saat ambil (asumsi saya), atau tetap minta transfer dulu?
2. Pesanan Dewi (20261006-03) masih menunggu alamat lengkap & pilihan kurir dari dia — sudah saya tanyakan ke pelanggan, nanti tinggal dilengkapi.
3. Nomor resi untuk kelima paket (JNE x3, J&T x1) belum ada — kirimkan setelah diserahkan ke kurir, biar pesan "pesanan dikirim" bisa langsung saya siapkan.````

## Catatan
- Konteks Telegram (lihat 00): angka sama persis, tetapi nota pesanan 2–6 disingkat dan tidak ada template pesan resi (nilai 7,5).
- Privasi: HP & alamat hanya di label; rekap harian & CSV bersih.
- Fitri: varian tidak ada ditanyakan dengan benar ke pelanggan, tetapi item tetap tercantum di label/serah-terima sebagai pending dan total ditahan.
