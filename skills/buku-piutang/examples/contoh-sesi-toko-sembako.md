# Contoh sesi: Toko Sembako Berkah (data fiktif)

Keluaran asli `scripts/piutang.py` v1.0.0, dijalankan pembuat skill dengan tanggal simulasi `--hari-ini` (opsi uji). Semua nama, nomor (0812-0000-xxxx), dan rekening fiktif. Tautan wa.me dipotong agar ringkas.

## Pemilik: "Pakai buku piutang untuk Toko Sembako Berkah, saya Sari, rekening BCA ..., biasanya tempo 2 minggu." (1 Sep; pratinjau sudah disetujui)

```
$ piutang.py init --nama-usaha 'Toko Sembako Berkah' --pengirim Sari --rekening 'BCA 0000000000 a.n. Sari (contoh)' --termin 14 --ya
TERSIMPAN. Buku piutang siap.
Database piutang baru: /home/sari/KomunitechData/piutang/piutang.db
Nama usaha: Toko Sembako Berkah | Pengirim draf: Sari | Rekening di draf: BCA 0000000000 a.n. Sari (contoh)
Termin default: 14 hari | Zona: WIB
Cadangan otomatis: /home/sari/KomunitechData/piutang/backup-piutang
```

## "Catat bon Warung Bu Tini 1.250.000, nota B-0901, nomornya 0812-0000-2001." (1 Sep)

```
$ piutang.py catat --pelanggan 'Warung Bu Tini' --wa 0812-0000-2001 --nota B-0901 --tanggal 01/09/2026 --nominal 1.250.000
Tercatat nota B-0901 untuk Warung Bu Tini (P0001, pelanggan baru): Rp 1.250.000 | tanggal 1 Sep 2026 | jatuh tempo Selasa, 15 September 2026 (14 hari)
Saldo piutang Warung Bu Tini: Rp 1.250.000 (1 nota terbuka).
Catatan: Jatuh tempo belum disebut; dipakai termin 14 hari dari tanggal nota.
```

## "Kafe Senja ambil gula & minyak 2,4 juta, nota B-0905, tempo seminggu." (5 Sep)

```
$ piutang.py catat --pelanggan 'Kafe Senja' --wa 0812-0000-2002 --nota B-0905 --tanggal 05/09/2026 --termin 7 --nominal 2,4jt --keterangan 'gula 50 kg, minyak 2 dus'
Tercatat nota B-0905 untuk Kafe Senja (P0002, pelanggan baru): Rp 2.400.000 | tanggal 5 Sep 2026 | jatuh tempo Sabtu, 12 September 2026 (7 hari)
Saldo piutang Kafe Senja: Rp 2.400.000 (1 nota terbuka).
```

## "Invoice INV-0910 ke CV Maju Jaya, DPP 10 juta plus PPN, tempo 30 hari." (10 Sep)

```
$ piutang.py catat --pelanggan 'CV Maju Jaya' --nota INV-0910 --tanggal 10/09/2026 --termin 30 --dpp 10jt --ppn 11
Tercatat nota INV-0910 untuk CV Maju Jaya (P0003, pelanggan baru): Rp 11.100.000 | tanggal 10 Sep 2026 | jatuh tempo Sabtu, 10 Oktober 2026 (30 hari)
Saldo piutang CV Maju Jaya: Rp 11.100.000 (1 nota terbuka).
Catatan: Rincian: DPP Rp 10.000.000 + PPN 12% x DPP nilai lain 11/12 = Rp 1.100.000 (efektif 11%, dibulatkan ke bawah) = Rp 11.100.000. PPN dihitung dari DPP persis lalu dibulatkan ke bawah sekali (tidak pernah melebihi tarif). Pembulatan ini belum dicocokkan dengan Coretax; faktur pajak resmi tetap mengikuti Coretax.
```

## "Pak Joko bon 350 ribu, seminggu." (20 Sep)

```
$ piutang.py catat --pelanggan 'Pak Joko' --wa 0812-0000-2004 --nota B-0920 --tanggal 20/09/2026 --termin 7 --nominal 350rb
Tercatat nota B-0920 untuk Pak Joko (P0004, pelanggan baru): Rp 350.000 | tanggal 20 Sep 2026 | jatuh tempo Minggu, 27 September 2026 (7 hari)
Saldo piutang Pak Joko: Rp 350.000 (1 nota terbuka).
```

## "Kafe Senja transfer 1 juta tanggal 15."

```
$ piutang.py bayar --pelanggan 'Kafe Senja' --jumlah 1jt --metode transfer --tanggal 15/09/2026
Pembayaran B0001 dicatat: Rp 1.000.000 dari Kafe Senja (P0002), 15 Sep 2026, transfer.
Dipakai untuk: B-0905 Rp 1.000.000 (sisa Rp 1.400.000).
Saldo piutang Kafe Senja: Rp 1.400.000 (1 nota terbuka).
```

## "Bu Tini bayar tunai 1,3 juta." (26 Sep) - ditolak dulu karena melebihi utang

```
$ piutang.py bayar --pelanggan 'Bu Tini' --jumlah 1,3jt --metode tunai
GAGAL: Pembayaran Rp 1.300.000 melebihi seluruh tagihan terbuka Warung Bu Tini Rp 1.250.000 (kelebihan Rp 50.000). TIDAK dicatat, supaya saldo tidak minus diam-diam. Tanyakan ke pengguna, lalu ulangi perintah yang sama dengan salah satu: --kelebihan kredit (disimpan sebagai deposit/kelebihan bayar pelanggan, bisa dipakai untuk nota berikutnya); --kelebihan kembalikan (uang lebihnya sudah dikembalikan ke pelanggan). Atau periksa lagi jumlahnya (salah ketik?).
```

## Agent bertanya; pemilik: "Lebihnya 50 ribu buat deposit saja, nanti dipotong bon berikutnya."

```
$ piutang.py bayar --pelanggan 'Bu Tini' --jumlah 1,3jt --metode tunai --kelebihan kredit
Pembayaran B0002 dicatat: Rp 1.300.000 dari Warung Bu Tini (P0001), 26 Sep 2026, tunai.
Dipakai untuk: B-0901 Rp 1.250.000 (LUNAS).
Kelebihan Rp 50.000 disimpan sebagai DEPOSIT/kelebihan bayar Warung Bu Tini (dipakai untuk nota berikutnya dengan perintah pakai-kredit).
Saldo piutang Warung Bu Tini: Rp 0 (0 nota terbuka) | kelebihan bayar/deposit: Rp 50.000 | saldo bersih: DEPOSIT milik pelanggan Rp 50.000 (bukan utang pelanggan).
```

## "Tagihan yang jatuh tempo apa saja?" (26 Sep)

```
$ piutang.py jatuh-tempo
JATUH TEMPO PIUTANG - Sabtu, 26 September 2026 (WIB)
Terlewat: Rp 1.400.000 (1 nota) | Hari ini: Rp 0 (0) | 7 hari ke depan: Rp 350.000 (1)

TERLEWAT (1 nota, Rp 1.400.000)
1. B-0905 | Kafe Senja (P0002) | sisa Rp 1.400.000 dari Rp 2.400.000 | JT 12 Sep 2026 (lewat 14 hari)

MINGGU INI (besok s.d. 3 Okt 2026) (1 nota, Rp 350.000)
1. B-0920 | Pak Joko (P0004) | sisa Rp 350.000 | JT 27 Sep 2026 (1 hari lagi)

Draf pesan tagihan: minta "bikinin pesan tagihan untuk <pelanggan>". Pesan dikirim sendiri, satu per satu.
```

## "Umur piutangnya gimana?"

```
$ piutang.py umur
UMUR PIUTANG - per Sabtu, 26 September 2026
Total piutang: Rp 12.850.000 (3 nota)
Belum jatuh tempo Rp 11.450.000 (89,1%) | 1-30 hari Rp 1.400.000 (10,9%) | 31-60 hari Rp 0 (0,0%) | 61-90 hari Rp 0 (0,0%) | >90 hari Rp 0 (0,0%)

1. CV Maju Jaya (P0003): Rp 11.100.000 = Belum jatuh tempo Rp 11.100.000
2. Kafe Senja (P0002): Rp 1.400.000 = 1-30 hari Rp 1.400.000
3. Pak Joko (P0004): Rp 350.000 = Belum jatuh tempo Rp 350.000
```

## "Bikinin pesan tagihan buat Kafe Senja."

```
$ piutang.py draf --pelanggan 'Kafe Senja'
DRAF PESAN TAGIHAN untuk Kafe Senja (P0002) [terlewat] - periksa dulu, lalu kirim sendiri:

Halo Bapak/Ibu di Kafe Senja, semoga sehat selalu. Saya Sari dari Toko Sembako Berkah.

Kami ingin menanyakan tagihan berikut yang sudah melewati jatuh tempo:
- Nota B-0905 (5 Sep 2026): sisa Rp 1.400.000, jatuh tempo 12 Sep 2026

Pembayaran bisa ditransfer ke BCA 0000000000 a.n. Sari (contoh).
Mohon dibantu informasikan kapan rencana pembayarannya, supaya bisa kami catat. Kalau sudah membayar, mohon kirimkan bukti transfernya.
Terima kasih atas perhatiannya.

Buka di WhatsApp (teks sudah terisi, tekan Kirim sendiri):
https://wa.me/6281200002002?text=Halo%20Bapak%2FIbu%20di%20Kafe%20Senja... (dipotong)
Setelah terkirim: piutang.py terkirim --pelanggan P0002
Saran: Tagihan ini sudah lewat 14 hari / diingatkan 0x. Untuk pemberitahuan resmi bertahap atau surat teguran, pakai skill tagih-piutang (data: piutang.py ekspor --format tagih-piutang).
```

## "Sudah kukirim."

```
$ piutang.py terkirim --pelanggan 'Kafe Senja'
Dicatat: pengingat sudah dikirim untuk Kafe Senja (P0002): B-0905 (ke-1).
```

## Jadwal OpenClaw 07.45 (27 Sep), versi disamarkan, masuk ke Telegram pemilik

```
$ piutang.py ringkasan --samarkan
RINGKASAN PIUTANG Toko Sembako Berkah - Minggu, 27 September 2026 (WIB)
Total piutang: Rp 12.850.000 (3 nota, 3 pelanggan)
Terlewat: Rp 1.400.000 (1 nota) | Hari ini: Rp 350.000 (1) | 7 hari ke depan: Rp 0 (0)
Pembayaran masuk kemarin: Rp 1.300.000 (1) | hari ini: Rp 0 (0)
Umur: Belum jatuh tempo Rp 11.450.000 (89,1%) | 1-30 hari Rp 1.400.000 (10,9%) | 31-60 hari Rp 0 (0,0%) | 61-90 hari Rp 0 (0,0%) | >90 hari Rp 0 (0,0%)
Kelebihan bayar pelanggan (deposit) belum dipakai: Rp 50.000

TERLEWAT (1 nota, Rp 1.400.000)
1. B-0905 | Kafe S. (P0002) | sisa Rp 1.400.000 dari Rp 2.400.000 | JT 12 Sep 2026 (lewat 15 hari) | diingatkan 1x (terakhir 26 Sep)

JATUH TEMPO HARI INI (1 nota, Rp 350.000)
1. B-0920 | Pak J. (P0004) | sisa Rp 350.000 | JT 27 Sep 2026 (hari ini)

Minta draf pesan tagihan ke agent di komputer Anda (mis. "pesan tagihan untuk P0002"). Pesan dikirim sendiri, satu per satu.
```

## "Rekap piutang bulan ini." (30 Sep)

```
$ piutang.py rekap --periode bulan-ini
REKAP PIUTANG - bulan September 2026 (1 Sep 2026 s.d. 30 Sep 2026)
Nota piutang baru: 4 nota, Rp 15.100.000
Pembayaran diterima: 2 kali, Rp 2.300.000
Potongan (retur/diskon/hapus): Rp 0 | Nota dibatalkan: 0 (Rp 0) | Kelebihan bayar dikembalikan: Rp 0
Posisi per 30 Sep 2026: piutang Rp 12.850.000 (3 nota, 3 pelanggan) | deposit pelanggan Rp 50.000
Umur: Belum jatuh tempo Rp 11.100.000 (86,4%) | 1-30 hari Rp 1.750.000 (13,6%) | 31-60 hari Rp 0 (0,0%) | 61-90 hari Rp 0 (0,0%) | >90 hari Rp 0 (0,0%)
Status hari ini (30 Sep 2026): terlewat Rp 1.750.000 (2 nota) | jatuh tempo hari ini Rp 0 (0) | 7 hari ke depan Rp 0 (0)
Terlewat terbesar: 1. Kafe Senja (P0002) Rp 1.400.000, paling lama 18 hari; 2. Pak Joko (P0004) Rp 350.000, paling lama 3 hari
```
## Cek angka (manual)
- Nota September: 1.250.000 + 2.400.000 + 11.100.000 + 350.000 = **15.100.000**.
- PPN INV-0910: 10.000.000 × 12% × 11/12 = 1.100.000 (tanpa pecahan) → total 11.100.000.
- Pembayaran: 1.000.000 (Kafe Senja) + 1.300.000 (Bu Tini) = **2.300.000**; 1.250.000 melunasi B-0901, sisa 50.000 menjadi deposit.
- Posisi 30 Sep: 15.100.000 − 1.000.000 − 1.250.000 = **12.850.000** (deposit 50.000 dicatat terpisah, tidak mengurangi piutang pelanggan lain).
- Umur 30 Sep: B-0905 lewat 18 hari + B-0920 lewat 3 hari = 1.400.000 + 350.000 = 1.750.000 (1–30 hari); 1.750.000 ÷ 12.850.000 = 13,62% → **13,6%**.
