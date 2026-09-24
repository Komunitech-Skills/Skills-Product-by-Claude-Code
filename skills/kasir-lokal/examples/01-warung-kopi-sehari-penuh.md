# 01 — Warung kopi: satu hari penuh (impor produk → 12 nota → void → retur → tutup kasir → rekap Telegram → struk 58 mm)

**Skenario:** Pemilik "Kedai Kopi Senja" (fiktif) di Bandung, bukan PKP, printer thermal 58 mm. Mengirim daftar menu dari Excel (CSV `;` + BOM, harga ditulis `Rp 18.000`), lalu kasir Rina mengetik pesanan sepanjang hari dengan kalimat campur (angka kata "dua/tiga/empat/lima", diskon item & nota bertingkat, tunai/QRIS/debit/transfer/GoPay/campuran), ada 1 salah bayar, 1 dobel ketik, 1 void, 1 retur sebagian, kas keluar, lalu tutup kasir dengan selisih dan rekap harian untuk Telegram.

Dijalankan sungguhan: `scripts/kasir.py` dengan DB uji `/tmp/uji-kasir-lokal/a/kasir.db` (ENV `KOMUNITECH_KASIR_DB`), tanggal 24/09/2026.

---

## 1. Mulai & impor produk

**Input pengguna:**
> pakai kasir buat kedai saya ya. nama Kedai Kopi Senja, Jl. Contoh No. 1 Bandung, telp 0812-0000-1111. belum PKP, printer 58. ini menunya (produk.csv)

`produk.csv` (dari Excel: UTF-8 BOM, pemisah `;`, CRLF):
```
Kode;Nama Produk;Varian;Harga Jual;Satuan;Stok
KSGA;Kopi Susu Gula Aren;;Rp 18.000;cup;
KH;Kopi Hitam;;12.000;cup;
KT;Kopi Tubruk;;10.000;cup;
AME;Americano;Ice;20.000;cup;
CAP;Cappuccino;;22.000;cup;
LAT;Cafe Latte;;22.000;cup;
ETM;Es Teh Manis;;6.000;gelas;
ETL;Es Teh Lemon;;8.000;gelas;
COK;Coklat Panas;;15.000;cup;
RB;Roti Bakar;Coklat;15.000;porsi;
RBK;Roti Bakar;Keju;17.000;porsi;
PGR;Pisang Goreng;;12.000;porsi;
MIE;Indomie Goreng Telur;;13.500;porsi;
KTG;Kentang Goreng;;14.000;porsi;
AM600;Air Mineral;600 ml;4.000;botol;
```

**Output (agent, dari pratinjau script):**
```
Saya siapkan kasirnya dulu (belum disimpan):
- Toko: Kedai Kopi Senja (fiktif) | Pajak: tanpa pajak | Stok: tidak dilacak | Kertas struk: 58 mm
- Database: ~/KomunitechData/kasir/kasir.db

Menu terbaca dari produk.csv (pemisah ';'):
Pemetaan kolom: kode <- 'Kode', nama <- 'Nama Produk', varian <- 'Varian', harga <- 'Harga Jual', satuan <- 'Satuan', stok <- 'Stok'
Produk baru: 15 | baris rusak: 0
- KSGA | Kopi Susu Gula Aren | Rp 18.000/cup
- KH | Kopi Hitam | Rp 12.000/cup
- ... (15 produk, termasuk RB Roti Bakar Coklat Rp 15.000/porsi dan RBK Roti Bakar Keju Rp 17.000/porsi)
- AM600 | Air Mineral 600 ml | Rp 4.000/botol

Simpan? Balas "ya".
```
Pengguna: "ya" → `init ... --ya`, `produk impor produk.csv --ya` → "Tersimpan, 15 produk. Backup otomatis dibuat."

**Buka kasir** — "buka kasir, modal 200rb, kasir Rina" (dicatat mulai 07.00):
```
TERSIMPAN.
Buka kasir 24/09/2026 07:00 | kas awal (modal kembalian) Rp 200.000 | kasir Rina
```

## 2. Transaksi (kalimat pengguna diteruskan apa adanya ke `jual --pesan`)

Contoh percakapan nota pertama:

> **Rina:** dua kopi susu, satu roti bakar keju, bayar tunai 50rb

```
Pesanan belum bisa disimpan: pembayaran KURANG Rp 3.000 (total Rp 53.000, dibayar Rp 50.000).
Minta kekurangannya ke pembeli atau ubah cara bayar.
```
> **Rina:** oh salah, bayarnya 100rb

```
Nota N-260924-0001 (belum disimpan):
1. Kopi Susu Gula Aren 2 x Rp 18.000 = Rp 36.000
2. Roti Bakar Keju 1 x Rp 17.000 = Rp 17.000
TOTAL Rp 53.000 | Tunai Rp 100.000 | Kembalian Rp 47.000
Catatan: "kopi susu" saya baca sebagai Kopi Susu Gula Aren (KSGA).
Simpan? Balas "ya".
```
> **Rina:** ya

```
Tersimpan, nota N-260924-0001. Kembalian Rp 47.000. Mau dicetak struknya?
```

Ringkasan 12 nota yang tersimpan (angka persis dari script, diverifikasi independen):

| Jam | Kalimat pengguna | Nota | Total | Bayar | Kembalian |
|---|---|---|---:|---|---:|
| 07:15 | dua kopi susu, satu roti bakar keju, bayar tunai 100rb | N-0001 | 53.000 | Tunai 100.000 | 47.000 |
| 07:40 | kopi hitam 2, pisang goreng x3, bayar qris | N-0002 | 60.000 | QRIS 60.000 | 0 |
| 08:05 | 3 es teh manis diskon 10%+5%, 1 indomie, bayar pas | N-0003 | 28.890 | Tunai 28.890 | 0 |
| 08:30 | 1 americano, 2 cappuccino diskon 2rb, diskon 10%, bayar tunai 60rb | N-0004 | 55.800 | Tunai 60.000 | 4.200 |
| 09:10 | tiga kopi tubruk, dua pisang goreng, bayar qris 30rb, tunai 24rb | N-0012* | 54.000 | QRIS 30.000 + Tunai 24.000 | 0 |
| 10:20 | 1 cafe latte, 1 roti bakar coklat, bayar debit | N-0005 | 37.000 | Debit 37.000 | 0 |
| 11:45 | empat es teh lemon, 2 kentang goreng, diskon 5rb, bayar tunai 100rb | N-0006 | 55.000 | Tunai 100.000 | 45.000 |
| 12:10 | lima indomie, 5 es teh manis, bayar transfer | N-0007 | 97.500 | Transfer 97.500 | 0 |
| 13:30 | 2 coklat panas, 1 air mineral, bayar gopay | N-0008 | 34.000 | E-wallet 34.000 | 0 |
| 15:00 | 1 kopi susu, 1 kentang goreng diskon 10%, bayar tunai 50rb | N-0009 | 30.600 | Tunai 50.000 | 19.400 |
| 16:40 | 2 KH, 2 RB, diskon 10%+2rb, bayar qris 40rb, tunai 20rb | N-0010 | 46.600 | QRIS 40.000 + Tunai 20.000 | 13.400 |
| 19:05 | kopi susu 3, roti bakar keju 1, bayar tunai 100rb | N-0011 | 71.000 | Tunai 100.000 | 29.000 |

\* Nota 09:10 awalnya ditolak (`bayar qris 30rb, tunai 20rb` → "Pembayaran KURANG Rp 4.000"), dicatat belakangan dengan `--waktu "2026-09-24 09:10"` sehingga nomornya N-260924-0012 (nomor urut mengikuti urutan pencatatan, jam mengikuti waktu transaksi).

Contoh pratinjau diskon bertingkat & diskon nota (N-0004 dan N-0003):
```
Nota N-260924-0004 | 24/09/2026 08:30
1. Americano Ice (AME) 1 x Rp 20.000 = Rp 20.000
2. Cappuccino (CAP) 2 x Rp 22.000 = Rp 44.000
   diskon Rp 2.000: -Rp 2.000
Subtotal: Rp 62.000
Diskon nota 10%: -Rp 6.200
TOTAL: Rp 55.800
Bayar: Tunai Rp 60.000 | Kembalian: Rp 4.200

Nota N-260924-0003 | 24/09/2026 08:05
1. Es Teh Manis (ETM) 3 x Rp 6.000 = Rp 18.000
   diskon 10%+5%: -Rp 2.610
2. Indomie Goreng Telur (MIE) 1 x Rp 13.500 = Rp 13.500
Subtotal: Rp 28.890
TOTAL: Rp 28.890
Bayar: Tunai Rp 28.890 | Kembalian: Rp 0
Catatan: 'indomie' dibaca sebagai Indomie Goreng Telur (MIE)
```

**Dobel ketik (19:08, isi sama persis dengan N-0011):**
```
Nota ini SAMA PERSIS dengan N-260924-0011 (19:05), kurang dari 10 menit lalu.
Ini pembeli berbeda atau tercatat dobel?
```
Pengguna: "dobel, abaikan" → tidak disimpan. (Script juga menolak `--ya` tanpa `--izinkan-duplikat`.)

**Pesanan ambigu** — "kopi, bayar" / "es teh 2 sama roti bakar":
```
Pesanan belum bisa dicatat:
- 'es teh': cocok dengan beberapa produk. Pilih salah satu: Es Teh Manis (ETM) Rp 6.000; Es Teh Lemon (ETL) Rp 8.000
- 'roti bakar': ada beberapa varian. Pilih salah satu: Roti Bakar Coklat (RB) Rp 15.000; Roti Bakar Keju (RBK) Rp 17.000
```

## 3. Void & retur

> **Rina:** batalin nota yg jam 11.45 tadi, salah input, pembelinya batal

```
VOID R-260924-0001 atas nota N-260924-0006 | 24/09/2026 11:50  (belum disimpan)
Alasan: salah input, pembeli batal
- Es Teh Lemon (ETL) 4 x | nilai -Rp 29.333
- Kentang Goreng (KTG) 2 x | nilai -Rp 25.667
Uang dikembalikan: Tunai Rp 55.000
Nota asal tidak dihapus; entri ini membalik nilainya.
Simpan? Balas "ya".
```
(Diskon nota Rp 5.000 dibagi proporsional: ETL 2.667, KTG 2.333.)

> **Rina:** cappuccino nota 08.30 tumpah 1, uangnya balikin tunai

```
RETUR R-260924-0002 atas nota N-260924-0004 | 24/09/2026 08:45
Alasan: tumpah
- Cappuccino (CAP) 1 x | nilai -Rp 18.900
Uang dikembalikan: Tunai Rp 18.900
```
(Baris CAP bersih 44.000 − 2.000 − 4.200 bagian diskon nota = 37.800 → separuhnya 18.900.)

**Kas keluar:** "ambil 25rb dari laci buat es batu & gas" → `kas --keluar 25rb --catatan "beli es batu & gas"` → "Kas keluar Rp 25.000 dari laci: beli es batu & gas".

## 4. Tutup kasir

> **Pemilik:** tutup kasir, uang di laci 425.000, setor 225rb

```
TUTUP KASIR - Kedai Kopi Senja (fiktif)
Sesi 2026-09-24 07:00 s/d 2026-09-24 21:00 | kasir Rina
Nota jual: 12 | retur/void: 2 | total transaksi Rp 549.490

Uang tunai di laci:
  Kas awal            Rp 200.000
  + Tunai bersih      Rp 250.990
  - Kas keluar        Rp 25.000
  = Seharusnya        Rp 425.990
  Dihitung (fisik)    Rp 425.000
  SELISIH             KURANG Rp 990

Non-tunai (cocokkan dengan mutasi bank/aplikasi QRIS):
  Debit              Rp 37.000
  E-wallet           Rp 34.000
  QRIS               Rp 130.000
  Transfer           Rp 97.500

Disetor ke pemilik: Rp 225.000 | sisa di laci: Rp 200.000
Catatan: Ada selisih kas KURANG Rp 990. Cek ulang hitungan uang, nota yang belum dicatat, kembalian salah, atau pengeluaran laci yang belum dicatat (perintah kas --keluar).
```
Agent menambahkan: "Selisih Rp 990 kecil; paling mungkin dari nota uang pas Rp 28.890 (08.05) yang dibayar Rp 28.000/29.000, atau kembalian dibulatkan. Tidak perlu menyalahkan siapa pun." Backup otomatis dibuat saat tutup kasir.

## 5. Rekap harian (teks siap kirim Telegram)

`rekap --tanggal hari-ini` (juga dijadwalkan lewat OpenClaw, lihat bawah):
```
REKAP KASIR Kamis, 24/09/2026
Kedai Kopi Senja (fiktif)
Nota jual: 12 | retur 1 | void 1
Penjualan kotor : Rp 648.000
Diskon          : -Rp 24.610
Retur/void      : -Rp 73.900
Penjualan bersih: Rp 549.490
Uang diterima   : Rp 549.490
Rata-rata/nota  : Rp 51.949

Per metode bayar:
- Tunai         Rp 250.990
- QRIS          Rp 130.000
- Transfer      Rp 97.500
- Debit         Rp 37.000
- E-wallet      Rp 34.000

Produk terlaris (penjualan bersih):
1. Kopi Susu Gula Aren - 6 cup - Rp 108.000
2. Indomie Goreng Telur - 6 porsi - Rp 81.000
3. Pisang Goreng - 5 porsi - Rp 60.000
4. Es Teh Manis - 8 gelas - Rp 45.390
5. Kopi Hitam - 4 cup - Rp 44.711
6. Roti Bakar Coklat - 3 porsi - Rp 40.889
7. Roti Bakar Keju - 2 porsi - Rp 34.000
8. Coklat Panas - 2 cup - Rp 30.000
9. Kopi Tubruk - 3 cup - Rp 30.000
10. Cafe Latte - 1 cup - Rp 22.000
(+4 produk lain)

Per jam:
07.00-07.59  2 nota  Rp 113.000
08.00-08.59  2 nota  Rp 84.690
09.00-09.59  1 nota  Rp 54.000
10.00-10.59  1 nota  Rp 37.000
11.00-11.59  1 nota  Rp 55.000
12.00-12.59  1 nota  Rp 97.500
13.00-13.59  1 nota  Rp 34.000
15.00-15.59  1 nota  Rp 30.600
16.00-16.59  1 nota  Rp 46.600
19.00-19.59  1 nota  Rp 71.000
```

**Jadwal Telegram (OpenClaw, Pilihan 1 dari `references/openclaw-jadwal.md`):**
> **Pemilik:** kirim rekap kasir ke telegram saya tiap jam 9 malam

```
Saya akan membuat jadwal ini (butuh persetujuan Anda):
openclaw automations add --name "Rekap kasir harian" --cron "0 21 * * *" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/kasir-lokal/scripts/kasir.py","rekap","--tanggal","hari-ini"]' \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
Jadwal hanya MEMBACA (rekap), tidak pernah mencatat/membatalkan nota. Komputer kasir + OpenClaw harus menyala jam 21.00 dan jamnya WIB. Lanjut?
```
Penguji: sintaks diterima CLI OpenClaw 2026.9.5 asli (semua opsi dikenali; ditolak hanya karena Gateway uji tidak punya kredensial — bukan salah tulis). Pengiriman Telegram tidak diuji (butuh bot token).

## 6. Struk 58 mm

"cetak struk nota 08.30, kertas 58" → `struk --nota N-260924-0004 --kertas 58`:
```
   KEDAI KOPI SENJA (FIKTIF)
   Jl. Contoh No. 1, Bandung
         0812-0000-1111
--------------------------------
No                 N-260924-0004
Tgl             24/09/2026 08:30
--------------------------------
Americano Ice
  1 cup x 20.000          20.000
Cappuccino
  2 cup x 22.000          44.000
  Diskon Rp 2.000         -2.000
--------------------------------
Subtotal                  62.000
Diskon 10%                -6.200
TOTAL                  Rp 55.800
Tunai                     60.000
Kembalian                  4.200
--------------------------------
          Terima kasih
```
Render Chromium headless → PDF 57,8 × 84,0 mm, 1 halaman, tidak ada teks terpotong (`scrollWidth == clientWidth`). Gambar: `struk-58mm-warung-kopi.png`, `struk-80mm-warung-kopi.png` (80 mm: PDF 80,1 × 87,1 mm).

---

## Catatan penguji
- **Bagus:** semua angka (12 nota, void, retur, tutup kasir, rekap per metode/jam/produk) cocok 100% dengan script verifikasi independen (`verif_a.py`, 0 beda terhadap DB). Pembayaran kurang, dobel ketik, produk ambigu ditolak dengan pesan jelas; tidak pernah menebak. Pratinjau → "ya" → simpan konsisten.
- Angka kata ("dua", "tiga", "empat", "lima"), `x3`, `kopi hitam 2`, kode `KH` semua terbaca.
- **Kurang:** (1) struk nota yang sudah diretur sebagian tidak memberi tanda "ada retur R-…"; (2) `struk --teks` (untuk chat) ikut menaikkan hitungan cetak, sehingga cetak kertas pertama berlabel "SALINAN"; (3) "Rata-rata/nota" ikut menghitung nota yang di-void (51.949 = 623.390 / 12; tanpa nota void: 568.390 / 11 = 51.672); (4) nama kasir sesi ("Rina") tidak otomatis tercetak di struk bila `--kasir` tidak disebut per nota; (5) usaha kedai kopi dengan meja-kursi bisa jadi wajib PBJT (pajak restoran daerah) — kasir tidak punya mode PBJT (lihat HASIL-UJI).
