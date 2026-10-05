# Contoh 01, normal: ekspor penjualan toko kue (CSV)

> Dibuat oleh pembuat skill (bukan pengganti uji independen Tahap 6). Data fiktif: `data-contoh.csv`. Tanggal acuan 2026-10-05.

## Permintaan pengguna
> "Toko kue saya banyak pelanggan yang dulu langganan lalu hilang. Ini ekspor penjualannya (CSV, namanya data-contoh.csv). Tolong bantu ajak balik. Saya belum mau kasih diskon."

## Langkah agen
```bash
python3 scripts/segmentasi.py examples/data-contoh.csv --hari-ini 2026-10-05
```
Keluaran script (UNTUK AGENT SAJA, tidak ditampilkan mentah ke pengguna):
```
UNTUK AGENT SAJA -- ringkasan hitungan. Jangan tempel mentah ke pengguna; sampaikan hasilnya dengan bahasa biasa.
Tanggal acuan: 2026-10-05 | Baris data dibaca: 29 | Pelanggan unik valid: 23 | Ditolak: 5
Dianggap pasif bila sudah >= 45 hari sejak beli terakhir. Masih aktif (tidak dihubungi): 5

SEGMEN (hari sejak beli terakhir)
  A Baru senyap : 45-90 hari | B Senyap : 91-180 | C Lama hilang : 181-365 | D Sangat lama : 366+
  kode | segmen       | jumlah | rata-rata belanja | nilai belanja (rata-rata x jumlah) | skenario 10% kembali
  A    | Baru senyap  |      3 |       Rp1.076.667 |                        Rp3.230.000 | Rp323.000
  B    | Senyap       |      7 |       Rp1.048.571 |                        Rp7.340.000 | Rp734.000
  C    | Lama hilang  |      6 |         Rp662.500 |                        Rp3.975.000 | Rp397.500
  D    | Sangat lama  |      2 |         Rp790.000 |                        Rp1.580.000 | Rp158.000
  TOTAL: 18 pelanggan pasif | nilai belanja historis Rp16.125.000 | skenario Rp1.612.500 (kira-kira 1.8 pelanggan kembali)
  Catatan: angka 'nilai belanja' = rata-rata belanja per pelanggan x jumlah (bukan ramalan). Skenario = ASUMSI persentase kembali yang bisa diubah (--target-balik), bukan janji hasil.

JADWAL (18 pelanggan x 3 pesan = 54 pesan; maks 10 pesan/hari; tanpa hari Minggu; mulai 2026-10-05, selesai paling lambat 2026-10-30)
  Urutan = nilai belanja terbesar dulu. Pesan 2 & 3 HANYA bila pelanggan belum membalas dan tidak komplain/minta berhenti.
  no | segmen | nama | no_wa | hari | total | tag | pesan1 | pesan2 | pesan3
  1 | B | Bu Maryam | 6281234567809 | 140 | Rp3.050.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  2 | A | Bu Wati | 6281234567805 | 76 | Rp2.300.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  3 | C | Bu Tini | 6281234567813 | 233 | Rp1.900.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  4 | D | Bu Sri | 6281234567817 | 383 | Rp1.250.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  5 | B | Mbak Lilis | 6281234567807 | 97 | Rp1.180.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  6 | B | Pak Agus | 6281234567806 | 92 | Rp975.000 | beli 2x | 2026-10-05 | 2026-10-15 | 2026-10-29
  7 | B | Mbak Dewi | 6281234567811 | 168 | Rp780.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  8 | B | [nama pelanggan] | 6281234567828 | 138 | Rp700.000 | beli 2x | 2026-10-05 | 2026-10-15 | 2026-10-29
  9 | C | Mbak Fitri | 6281234567815 | 298 | Rp690.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  10 | A | Mbak Sinta | 6281234567803 | 56 | Rp620.000 | langganan | 2026-10-05 | 2026-10-15 | 2026-10-29
  11 | C | Pak Rudi | 6281234567814 | 248 | Rp505.000 | beli 2x | 2026-10-06 | 2026-10-16 | 2026-10-30
  12 | C | Mbak Ayu | 6281234567819 | 361 | Rp450.000 | beli 2x | 2026-10-06 | 2026-10-16 | 2026-10-30
  13 | B | Pak Yusuf | 6281234567810 | 156 | Rp415.000 | beli 2x | 2026-10-06 | 2026-10-16 | 2026-10-30
  14 | D | Pak Joko | 6281234567818 | 467 | Rp330.000 | beli 1x | 2026-10-06 | 2026-10-16 | 2026-10-30
  15 | A | Kak Dimas | 6281234567804 | 64 | Rp310.000 | beli 1x | 2026-10-06 | 2026-10-16 | 2026-10-30
  16 | C | Kak Andi | 6281234567816 | 336 | Rp275.000 | beli 1x | 2026-10-06 | 2026-10-16 | 2026-10-30
  17 | B | Kak Reza | 6281234567808 | 115 | Rp240.000 | beli 1x | 2026-10-06 | 2026-10-16 | 2026-10-30
  18 | C | Kak Bagas | 6281234567812 | 211 | Rp155.000 | beli 1x | 2026-10-06 | 2026-10-16 | 2026-10-30

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

### Verifikasi independen angka (hitungan terpisah dengan python, tanpa memakai script)
Tanggal acuan 2026-10-05; hari = selisih tanggal; pelanggan dihitung per nomor unik; total dijumlahkan per nomor.

| Segmen | Jumlah | Total belanja | Rata-rata |
|---|---|---|---|
| A (45-90 hari) | 3 | 3.230.000 | 1.076.667 |
| B (91-180) | 7 | 7.340.000 | 1.048.571 |
| C (181-365) | 6 | 3.975.000 | 662.500 |
| D (366+) | 2 | 1.580.000 | 790.000 |
| Total pasif | 18 | 16.125.000 | |
| Masih aktif (di bawah 45 hari) | 5 | 4.170.000 | tidak dihubungi |

Sama dengan keluaran script. Catatan: "Bu Ratna" muncul dua kali (nomor sama); digabung menjadi satu, tanggal terbaru 28/09/2026, sehingga masih aktif.

## Balasan ke pengguna

Dari 23 pelanggan di data, **18 sudah lebih dari 45 hari tidak belanja**, dan total belanja mereka dulu **Rp16.125.000**. Lima pelanggan lain masih aktif, jadi tidak perlu dihubungi.

| Segmen | Lama diam | Jumlah | Rata-rata belanja | Total belanja dulu |
|---|---|---|---|---|
| A. Baru senyap | 45-90 hari | 3 | Rp1.076.667 | Rp3.230.000 |
| B. Senyap | 91-180 hari | 7 | Rp1.048.571 | Rp7.340.000 |
| C. Lama hilang | 181-365 hari | 6 | Rp662.500 | Rp3.975.000 |
| D. Sangat lama | lebih dari 1 tahun | 2 | Rp790.000 | Rp1.580.000 |

Angka ini nilai belanja mereka sebelumnya, bukan ramalan. Sebagai gambaran saja: kalau 10% dari mereka kembali dan belanja sebesar rata-rata, nilainya sekitar Rp1,6 juta. Angka 10% ini hanya pengandaian.

**Dihubungi duluan (nilai belanja terbesar):** Bu Maryam (Rp3.050.000, 11 transaksi), Bu Wati (Rp2.300.000), Bu Tini (Rp1.900.000), Bu Sri, Mbak Lilis. Mulai dari 10 nama teratas saja dulu.

**Jadwal 4 minggu (maksimal 10 pesan per hari, tidak hari Minggu, jam 09.00-20.00):**
- Pesan 1 mulai Senin 5 Oktober: 10 nama pertama hari itu, sisanya Selasa 6 Oktober.
- Pesan 2 sekitar 10 hari kemudian (15-16 Oktober), **hanya kalau belum dibalas**.
- Pesan 3 sekitar 29-30 Oktober, pesan terakhir.

**Teks pesan (tinggal salin, ganti isian dalam kurung siku):**

**Pesan 1, segmen A (45-90 hari), langganan** (Bu Wati, Mbak Sinta)
```
Halo Bu Wati, apa kabar? Ini [nama Anda] dari [nama usaha]. Sudah agak lama kita belum ketemu, terakhir [yang dulu dibeli] sekitar bulan Juli. Semoga sehat dan lancar selalu ya. Kalau ada yang kurang pas dari kami kemarin, boleh cerita, kami senang dengar masukannya. Kalau tidak ingin dihubungi lagi, tinggal balas "stop", tidak apa-apa.
```

**Pesan 1, segmen A, pembeli sekali** (Kak Dimas)
```
Halo Kak Dimas, ini [nama Anda] dari [nama usaha]. Beberapa waktu lalu Kakak pernah belanja [yang dulu dibeli] di tempat kami, terima kasih ya. Mau tanya sedikit, bagaimana kesannya? Masukan apa pun berguna buat kami. Kalau tidak ingin dihubungi lagi, balas "stop" saja.
```

**Pesan 1, segmen B (91-180 hari)** (Bu Maryam, Mbak Lilis, Mbak Dewi, dst.)
```
Halo Bu Maryam, ini [nama Anda] dari [nama usaha]. Sudah beberapa bulan sejak terakhir Ibu belanja di tempat kami, dan kami cuma ingin menyapa. Boleh tahu, ada yang kurang cocok atau memang sedang tidak butuh? Jujur saja tidak apa-apa, justru membantu kami berbenah. Kalau tidak ingin dihubungi lagi, balas "stop" ya.
```

**Pesan 1, segmen C (181-365 hari)** (Bu Tini, Mbak Fitri, dst.)
```
Selamat siang Bu Tini. Saya [nama Anda] dari [nama usaha]. Dulu Ibu pernah langganan [yang dulu dibeli] di tempat kami, dan kami masih ingat. Apa kabar? Kalau ada waktu, boleh cerita apa yang membuat Ibu jarang mampir lagi? Tidak ada maksud memaksa. Kalau tidak berkenan dihubungi lagi, balas "stop" saja.
```

**Pesan 1, segmen D (lebih dari 365 hari)** (Bu Sri, Pak Joko)
```
Halo Bu Sri, ini [nama Anda] dari [nama usaha]. Sudah lebih dari setahun sejak terakhir kita ketemu, semoga Ibu sehat selalu. Kalau nomor ini sudah bukan Bu Sri, mohon maaf mengganggu. Kalau tidak ingin dihubungi lagi, balas "stop" ya.
```

**Pesan 2 (sekitar hari ke-10, hanya bila belum ada balasan)**
```
Halo Bu Maryam, [nama Anda] dari [nama usaha]. Mau sekadar menanyakan lagi, kira-kira apa yang paling Ibu cari dari [jenis usaha] seperti kami? Kalau bisa kami bantu, dengan senang hati. Kalau tidak, juga tidak apa-apa dan terima kasih sudah pernah mampir.
```
Kalau ada hal nyata yang berubah (menu baru, jam buka, layanan antar), sebutkan di pesan ini: "Sejak terakhir Ibu datang, ada perubahan di tempat kami: [perubahan nyata]." Kalau tidak ada, pakai versi di atas.

**Pesan 3 (sekitar hari ke-24, pesan terakhir)**
```
Halo Bu Maryam, ini pesan terakhir dari saya, [nama Anda] dari [nama usaha]. Terima kasih sudah pernah jadi pelanggan kami. Pintu kami selalu terbuka kalau Ibu ingin mampir atau pesan lagi, tinggal kabari lewat chat ini. Kami tidak akan mengirim pesan lagi, kecuali Ibu yang menghubungi duluan. Sehat dan sukses selalu!
```

**Kapan berhenti:**
- Pelanggan membalas apa pun: berhenti kirim pesan berikutnya, balas seperti percakapan biasa.
- Pelanggan kecewa atau komplain: berhenti seketika, minta maaf dan dengarkan dulu, tanpa penawaran.
- Pelanggan minta berhenti: terima kasih, hormati, catat supaya tidak dihubungi lagi.
- Setelah pesan 3 tanpa balasan: selesai, jangan ulangi sebelum 3-6 bulan.

Dua hal kecil: ada 5 baris data yang tidak bisa dipakai (misalnya tanggal 31/02/2026, nomor terlalu pendek, total tertulis "tidak ada"), dan satu pelanggan tanpa nama. Perbaiki di file Anda bila ingin ikut dihubungi.

**Asumsi saya:** belum ada penawaran (pesan pertama dan kedua memang tidak menjual), batas "mulai pasif" 45 hari, mulai kirim hari ini.

**Tiga pertanyaan:**
1. Ada penawaran yang benar-benar bisa Anda berikan di pesan ketiga (mis. gratis ongkir atau bonus kecil)? Kalau tidak, pesan terakhir tetap sopan tanpa penawaran.
2. Ada pelanggan dalam daftar yang pernah komplain atau sedang bermasalah? Sebutkan, saya keluarkan.
3. Nama Anda dan usaha untuk mengisi `[nama Anda]` dan `[nama usaha]`, plus apa yang biasanya mereka beli supaya `[yang dulu dibeli]` bisa diisi?

---
## Catatan pembuat
- Pesan di bawah 90 kata (diperiksa), opsi "stop" di pesan 1 dan 3, tidak ada urgensi/klaim/penawaran karangan.
- Balasan tidak menyebut script/file/path. Angka sesuai hitungan independen di atas.
