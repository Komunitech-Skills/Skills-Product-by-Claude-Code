# Contoh 02, normal: ada penawaran, daftar jangan-dihubungi, batas 5 pesan/hari

> Dibuat oleh pembuat skill. Data fiktif yang sama (`data-contoh.csv`) dengan daftar `jangan-dihubungi-contoh.txt`.

## Permintaan pengguna
> "Lanjut ya. Bu Wati bulan lalu komplain pesanannya telat, jadi jangan dihubungi dulu. Pak Agus minta berhenti, nomornya 0812-3456-7806. Gratis ongkir untuk pesanan berikutnya boleh, berlaku sampai 31 Oktober 2026. Saya cuma bisa kirim 5 chat per hari, mulai besok Selasa."

## Langkah agen
```bash
python3 scripts/segmentasi.py examples/data-contoh.csv --hari-ini 2026-10-05 --mulai 2026-10-06 --per-hari 5 --kecualikan examples/jangan-dihubungi-contoh.txt
```
Keluaran script (UNTUK AGENT SAJA):
```
UNTUK AGENT SAJA -- ringkasan hitungan. Jangan tempel mentah ke pengguna; sampaikan hasilnya dengan bahasa biasa.
Tanggal acuan: 2026-10-05 | Baris data dibaca: 29 | Pelanggan unik valid: 23 | Ditolak: 5
Dianggap pasif bila sudah >= 45 hari sejak beli terakhir. Masih aktif (tidak dihubungi): 5
Dikecualikan (daftar jangan-dihubungi): 2

SEGMEN (hari sejak beli terakhir)
  A Baru senyap : 45-90 hari | B Senyap : 91-180 | C Lama hilang : 181-365 | D Sangat lama : 366+
  kode | segmen       | jumlah | rata-rata belanja | nilai belanja (rata-rata x jumlah) | skenario 10% kembali
  A    | Baru senyap  |      2 |         Rp465.000 |                          Rp930.000 | Rp93.000
  B    | Senyap       |      6 |       Rp1.060.833 |                        Rp6.365.000 | Rp636.500
  C    | Lama hilang  |      6 |         Rp662.500 |                        Rp3.975.000 | Rp397.500
  D    | Sangat lama  |      2 |         Rp790.000 |                        Rp1.580.000 | Rp158.000
  TOTAL: 16 pelanggan pasif | nilai belanja historis Rp12.850.000 | skenario Rp1.285.000 (kira-kira 1.6 pelanggan kembali)
  Catatan: angka 'nilai belanja' = rata-rata belanja per pelanggan x jumlah (bukan ramalan). Skenario = ASUMSI persentase kembali yang bisa diubah (--target-balik), bukan janji hasil.

JADWAL (16 pelanggan x 3 pesan = 48 pesan; maks 5 pesan/hari; tanpa hari Minggu; mulai 2026-10-06, selesai paling lambat 2026-11-03)
  Urutan = nilai belanja terbesar dulu. Pesan 2 & 3 HANYA bila pelanggan belum membalas dan tidak komplain/minta berhenti.
  no | segmen | nama | no_wa | hari | total | tag | pesan1 | pesan2 | pesan3
  1 | B | Bu Maryam | 6281234567809 | 140 | Rp3.050.000 | langganan | 2026-10-06 | 2026-10-16 | 2026-10-30
  2 | C | Bu Tini | 6281234567813 | 233 | Rp1.900.000 | langganan | 2026-10-06 | 2026-10-16 | 2026-10-30
  3 | D | Bu Sri | 6281234567817 | 383 | Rp1.250.000 | langganan | 2026-10-06 | 2026-10-16 | 2026-10-30
  4 | B | Mbak Lilis | 6281234567807 | 97 | Rp1.180.000 | langganan | 2026-10-06 | 2026-10-16 | 2026-10-30
  5 | B | Mbak Dewi | 6281234567811 | 168 | Rp780.000 | langganan | 2026-10-06 | 2026-10-16 | 2026-10-30
  6 | B | [nama pelanggan] | 6281234567828 | 138 | Rp700.000 | beli 2x | 2026-10-07 | 2026-10-17 | 2026-10-31
  7 | C | Mbak Fitri | 6281234567815 | 298 | Rp690.000 | langganan | 2026-10-07 | 2026-10-17 | 2026-10-31
  8 | A | Mbak Sinta | 6281234567803 | 56 | Rp620.000 | langganan | 2026-10-07 | 2026-10-17 | 2026-10-31
  9 | C | Pak Rudi | 6281234567814 | 248 | Rp505.000 | beli 2x | 2026-10-07 | 2026-10-17 | 2026-10-31
  10 | C | Mbak Ayu | 6281234567819 | 361 | Rp450.000 | beli 2x | 2026-10-07 | 2026-10-17 | 2026-10-31
  11 | B | Pak Yusuf | 6281234567810 | 156 | Rp415.000 | beli 2x | 2026-10-08 | 2026-10-19 | 2026-11-02
  12 | D | Pak Joko | 6281234567818 | 467 | Rp330.000 | beli 1x | 2026-10-08 | 2026-10-19 | 2026-11-02
  13 | A | Kak Dimas | 6281234567804 | 64 | Rp310.000 | beli 1x | 2026-10-08 | 2026-10-19 | 2026-11-02
  14 | C | Kak Andi | 6281234567816 | 336 | Rp275.000 | beli 1x | 2026-10-08 | 2026-10-19 | 2026-11-02
  15 | B | Kak Reza | 6281234567808 | 115 | Rp240.000 | beli 1x | 2026-10-08 | 2026-10-19 | 2026-11-02
  16 | C | Kak Bagas | 6281234567812 | 211 | Rp155.000 | beli 1x | 2026-10-09 | 2026-10-20 | 2026-11-03

PERLU DILENGKAPI / BARIS DITOLAK (5) -- tidak masuk jadwal:
  baris 24 | Pak Darmo | tanggal tidak ada di kalender '31/02/2026' (dibaca dd/mm/yyyy)
  baris 25 | Mbak Rina | bukan nomor seluler Indonesia yang wajar '08123456'
  baris 26 | Kak Wahyu | format tanggal tidak dikenali 'kemarin' (pakai dd/mm/yyyy)
  baris 27 | Bu Lastri | total belanja bukan angka 'tidak ada'
  baris 28 | Pak Eko | tanggal beli terakhir di masa depan (2026-12-05)

CATATAN DATA:
  baris 29: nama kosong, ditulis [nama pelanggan]
  baris 30: nomor 6281234567801 sudah ada (Bu Ratna (Toko Kue Ratna)), digabung: tanggal terbaru, total dijumlahkan
```

### Verifikasi independen
- Dikeluarkan 2: Bu Wati (nama) dan Pak Agus (nomor 6281234567806). Pasif 18 menjadi 16.
- Total belanja pasif: 16.125.000 - 2.300.000 (Bu Wati) - 975.000 (Pak Agus) = **12.850.000**. Sama dengan script.
- Segmen A: 3.230.000 - 2.300.000 = 930.000 (2 orang, rata-rata 465.000). Segmen B: 7.340.000 - 975.000 = 6.365.000 (6 orang, rata-rata 1.060.833). Sama.
- 16 pelanggan x 3 pesan = 48 pesan; dengan 5/hari dan tanpa Minggu, pelanggan terakhir selesai 3 Nov 2026 (26 hari sejak pesan pertamanya, 9 Okt).

## Balasan ke pengguna

Siap. Bu Wati dan Pak Agus sudah dikeluarkan dari daftar, jadi tidak akan ada pesan untuk mereka. Karena Bu Wati sempat kecewa soal pesanan telat, lebih baik Anda sendiri yang menyapa beliau secara pribadi suatu hari nanti, bukan lewat urutan pesan.

**Sekarang tersisa 16 pelanggan pasif** dengan total belanja dulu **Rp12.850.000** (segmen A 2 orang, B 6, C 6, D 2).

**Jadwal dengan 5 pesan per hari, mulai Selasa 6 Oktober:**
- Selasa 6 Okt: Bu Maryam, Bu Tini, Bu Sri, Mbak Lilis, Mbak Dewi
- Rabu 7 Okt: 5 nama berikutnya (Mbak Fitri, Mbak Sinta, Pak Rudi, Mbak Ayu, pelanggan tanpa nama di data)
- Kamis 8 Okt: Pak Yusuf, Pak Joko, Kak Dimas, Kak Andi, Kak Reza
- Jumat 9 Okt: Kak Bagas
- Pesan 2 mulai Jumat 16 Okt dan pesan 3 mulai Jumat 30 Okt, sesuai urutan yang sama, **hanya bagi yang belum membalas**. Semua urutan selesai paling lambat Selasa 3 November.
Batas 5 per hari berlaku untuk semua jenis pesan, jadi jarak pesan 2 dan 3 bisa bergeser satu-dua hari dari patokan 10 dan 24 hari.

**Pesan 3 dengan penawaran (sudah disetujui Anda: gratis ongkir sampai 31 Oktober 2026):**
```
Halo Bu Maryam, ini pesan terakhir dari saya, [nama Anda] dari [nama usaha]. Kalau Ibu berkenan mampir atau pesan lagi, kami siapkan gratis ongkir untuk pesanan berikutnya, berlaku sampai 31 Oktober 2026. Kalau belum waktunya, tidak masalah dan terima kasih banyak sudah pernah jadi pelanggan. Balas "stop" bila tidak ingin dihubungi lagi.
```
Penawaran hanya ada di pesan 3. Pesan 3 untuk pelanggan yang dijadwalkan setelah 31 Oktober (pelanggan nomor 11-16) tidak boleh memakai kalimat batas waktu itu lagi; mau diperpanjang? Sebutkan tanggal barunya dan saya sesuaikan.

Pesan 1 dan 2 tetap sama seperti sebelumnya (tanpa jualan), dan aturan berhenti tidak berubah: begitu ada balasan, komplain, atau permintaan berhenti, hentikan urutan.

**Tiga pertanyaan:**
1. Mau diperpanjang batas gratis ongkirnya agar pesan 3 yang terjadwal awal November tetap valid?
2. Gratis ongkir berlaku untuk semua kota atau ada syarat minimal belanja? Kalau ada, saya tulis di pesan 3.
3. Mau saya buatkan daftar kerja harian (siapa dikirim hari apa) dalam bentuk tabel yang bisa Anda centang?

---
## Catatan pembuat
- Penawaran hanya dari yang disebut pengguna; batas waktu ditulis karena benar-benar ada. Tidak ada diskon/stok karangan.
- Pelanggan yang komplain dikeluarkan dan disarankan kontak pribadi (sesuai aturan "ulasan jelek lalu berhenti = telepon").
- Catatan nama pada daftar harian: nomor 7 di sini menyebut pelanggan tanpa nama yang di data ditulis `[nama pelanggan]`; pemilik perlu melengkapi namanya.
