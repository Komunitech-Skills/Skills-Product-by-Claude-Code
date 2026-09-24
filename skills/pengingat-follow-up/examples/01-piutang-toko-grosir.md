# 01 — Toko grosir: catat 4 piutang dari kalimat campur, lalu rekap

**Skenario:** Pemilik toko grosir sembako (awam teknologi) mengetik daftar bon pelanggan dalam satu pesan
dengan format tanggal & nominal campur, lalu minta rekap. Hari acuan uji: Kamis, 1 Oktober 2026
(`--hari-ini 2026-10-01`). Semua nama fiktif.

## Input pengguna (persis)
> tolong catet bon2 ini ya biar ga lupa nagih:
> - Bu Rina 4,5 jt jatuh tempo 3 Okt, nota 0412 beras & minyak
> - CV Maju 750rb tgl 20/9 nota 0398
> - Toko Sinar Rp1.250.000 besok, nota 0405
> - Pak Harto 2 jt 300 rb tgl 1, katanya mau transfer sore
> terus hari ini saya harus nagih siapa aja?

## Proses (perintah yang dijalankan agent, dari folder kerja)
Daftar banyak sekaligus → agent menampilkan ringkasan & minta "ya" (SKILL.md Langkah 1). Setelah pemilik
menjawab "ya", agent menjalankan `tambah` per baris (teks tanggal/nominal diserahkan apa adanya ke script):
```bash
S="python3 <folder-skill>/scripts/cek_jatuh_tempo.py --hari-ini 2026-10-01"
$S --teks tambah --jenis piutang --nama "Bu Rina"   --tanggal "3 Okt"  --nominal "4,5 jt"      --perihal "nota 0412 beras & minyak"
$S --teks tambah --jenis piutang --nama "CV Maju"   --tanggal "20/9"   --nominal "750rb"       --perihal "nota 0398"
$S --teks tambah --jenis piutang --nama "Toko Sinar" --tanggal "besok" --nominal "Rp1.250.000" --perihal "nota 0405"
$S --teks tambah --jenis piutang --nama "Pak Harto" --tanggal "tgl 1"  --nominal "2 jt 300 rb" --catatan "janji transfer sore"
$S --teks rekap
```

## Output (balasan agent ke pemilik)

Ini ringkasan yang saya baca, sudah benar?
1. Bu Rina: Rp 4.500.000, jatuh tempo 3 Okt, nota 0412 beras & minyak
2. CV Maju: Rp 750.000, jatuh tempo 20 Sep, nota 0398
3. Toko Sinar: Rp 1.250.000, jatuh tempo besok (2 Okt), nota 0405
4. Pak Harto: Rp 2.300.000, jatuh tempo tgl 1 (hari ini). Catatan pribadi: janji transfer sore

Balas **ya** untuk menyimpan.

*(pemilik: "ya")*

```
Tersimpan #1: piutang - Bu Rina, Sabtu, 3 Oktober 2026, Rp 4.500.000 (nota 0412 beras & minyak).
Catatan: Tahun tidak disebut; dipakai 3 Okt 2026 (tanggal terdekat ke depan). Ubah bila maksudnya lain.
Tersimpan #2: piutang - CV Maju, Minggu, 20 September 2026, Rp 750.000 (nota 0398).
Catatan: Tahun tidak disebut; dipakai 20 Sep 2026 yang baru lewat 11 hari (item masuk TERLAMBAT). Kalau maksudnya tahun depan, tulis tahunnya.
Tersimpan #3: piutang - Toko Sinar, Jumat, 2 Oktober 2026, Rp 1.250.000 (nota 0405).
Tersimpan #4: piutang - Pak Harto, Kamis, 1 Oktober 2026, Rp 2.300.000.
Catatan: Bulan tidak disebut; dipakai 1 Okt 2026 (tanggal 1 terdekat ke depan). Ubah bila maksudnya lain.
```

Ini yang perlu ditagih hari ini:

```
PENGINGAT FOLLOW-UP - Kamis, 1 Oktober 2026

TERLAMBAT (1)
1. #2 Piutang - CV Maju | Rp 750.000 | nota 0398 | lewat 11 hari (jatuh tempo 20 Sep 2026)

HARI INI (1)
1. #4 Piutang - Pak Harto | Rp 2.300.000 | jatuh tempo hari ini
   Catatan: janji transfer sore

BESOK / H-1 (1)
1. #3 Piutang - Toko Sinar | Rp 1.250.000 | nota 0405 | besok, 2 Okt 2026

Total piutang tertunggak (terlambat + hari ini): Rp 3.050.000
Piutang jatuh tempo besok: Rp 1.250.000
Menyusul 7 hari ke depan: 1 item

DRAF PESAN (cek dulu, lalu salin & kirim sendiri dari WA/email Anda)

#2 untuk CV Maju:
Selamat pagi CV Maju. Kami menindaklanjuti pembayaran nota 0398 sebesar Rp 750.000 yang sudah lewat 11 hari dari jatuh tempo (20 Sep 2026). Mohon informasikan tanggal pasti pembayarannya, paling lambat 4 Okt 2026. Jika ada kendala, kami terbuka membicarakan jadwal pembayaran. Terima kasih.
(Saran: Sudah lewat >= 7 hari: bila sudah pernah diingatkan tanpa hasil, pakai skill tagih-piutang untuk pemberitahuan resmi, denda (hanya jika tertulis di kontrak), atau surat teguran (>= 30 hari dan sudah >= 2 kali diingatkan).)

#4 untuk Pak Harto:
Selamat pagi Pak Harto, kami mengingatkan pembayaran tagihan sebesar Rp 2.300.000 jatuh tempo hari ini, 1 Okt 2026. Jika sudah transfer, mohon kirimkan bukti transfernya agar bisa kami catat. Abaikan pesan ini jika sudah membayar. Terima kasih.

#3 untuk Toko Sinar:
Selamat pagi Toko Sinar, izin mengingatkan pembayaran nota 0405 sebesar Rp 1.250.000 yang jatuh tempo besok, 2 Okt 2026. Pembayaran bisa melalui [rekening]. Abaikan pesan ini jika sudah membayar. Terima kasih.

Balas misalnya: "selesai 3", "tunda 3 ke Senin", "hapus 3".
```
Ganti `[rekening]` dengan rekening toko sebelum dikirim. Pesan dikirim sendiri dari WA Bapak/Ibu, bukan oleh bot.

### Lanjutan (2 Okt): "Toko Sinar udah lunas, Pak Harto baru bayar 1 jt"
```bash
$S --hari-ini 2026-10-02 --teks selesai --id 3 --catatan "lunas transfer 2 Okt"
$S --hari-ini 2026-10-02 --teks ubah --id 4 --nominal "1 jt 300 rb" --catatan "bayar sebagian 1 jt tgl 2 Okt"
```
```
#3 Toko Sinar ditandai selesai
#4 diubah: nominal Rp 1.300.000; catatan "bayar sebagian 1 jt tgl 2 Okt"
```

### Rekap pagi Sabtu 3 Okt (`--hari-ini 2026-10-03`), potongan
```
TERLAMBAT (2)
1. #2 Piutang - CV Maju | Rp 750.000 | nota 0398 | lewat 13 hari (jatuh tempo 20 Sep 2026)
2. #4 Piutang - Pak Harto | Rp 1.300.000 | lewat 2 hari (jatuh tempo 1 Okt 2026)
   Catatan: bayar sebagian 1 jt tgl 2 Okt

HARI INI (1)
1. #1 Piutang - Bu Rina | Rp 4.500.000 | nota 0412 beras & minyak | jatuh tempo hari ini

Total piutang tertunggak (terlambat + hari ini): Rp 6.550.000
```

### Draf CV Maju bila masih belum bayar pada 25 Okt (lewat 35 hari → pemberitahuan tertulis)
```
Yth. CV Maju, bersama pesan ini kami sampaikan secara tertulis bahwa pembayaran nota 0398 sebesar Rp 750.000 yang jatuh tempo 20 Sep 2026 sudah lewat 35 hari dan belum kami terima. Mohon pembayaran diselesaikan paling lambat 1 Nov 2026 melalui [rekening], atau hubungi kami sebelum tanggal tersebut bila ingin membahas jadwal cicilan secara tertulis. Terima kasih atas perhatiannya.
```

## Verifikasi angka (independen, `verif.py` terpisah, tidak mengimpor script)
| Angka | Script | Hitung ulang | Status |
|---|---|---|---|
| Total tertunggak 1 Okt (750.000 + 2.300.000) | Rp 3.050.000 | 3.050.000 | cocok |
| Jatuh tempo besok | Rp 1.250.000 | 1.250.000 | cocok |
| CV Maju lewat (1 Okt − 20 Sep) | 11 hari | 11 | cocok |
| Batas "paling lambat" (hari ini + 3) | 4 Okt 2026 | 4 Okt 2026 | cocok |
| Total 3 Okt (750.000 + 1.300.000 + 4.500.000) | Rp 6.550.000 | 6.550.000 | cocok |
| CV Maju lewat pada 25 Okt | 35 hari | 35 | cocok |
| "20/9" diucapkan 1 Okt (11 hari lalu, ≤ 60) | 2026, TERLAMBAT | aturan ≤ 60 hari → tahun ini | cocok |

## Catatan penguji
- Bagus: semua format campuran ("3 Okt", "20/9", "besok", "tgl 1", "4,5 jt", "750rb", "Rp1.250.000",
  "2 jt 300 rb") terbaca benar. `Catatan:` tahun/bulan ditebak ikut ditampilkan. Aturan "baru lewat ≤ 60 hari
  = terlambat" untuk "20/9" tepat. Nada draf naik bertahap. Catatan pribadi ("janji transfer sore") tidak
  masuk ke draf.
- Kurang: "Menyusul 7 hari ke depan: 1 item" tidak menyebut siapa (Bu Rina). `ubah --catatan` **mengganti**
  catatan lama ("janji transfer sore" hilang), padahal SKILL.md bilang "tambahkan catatan". Untuk bayar sebagian,
  draf tetap berbunyi "pembayaran tagihan sebesar Rp 1.300.000" kecuali agent ingat mengisi `--perihal "sisa ..."`.

---
## Uji ulang v1.0.1 (2026-09-24)
Input yang sama menghasilkan angka yang sama (tertunggak Rp 3.050.000, besok Rp 1.250.000). Tambahan di rekap:
```
Umur piutang terlambat: 1-30 hari: Rp 750.000 (1)
Menyusul 7 hari ke depan: #1 Bu Rina (3 Okt 2026)
...
(Saran: Setelah pesan dikirim, balas "terkirim 2" agar nada berikutnya menyesuaikan. ...)
Balas misalnya: "selesai 3", "terkirim 3", "tunda 3 ke Senin", "hapus 3".
```
- `ubah --id 4 --catatan ...` kini **menambahkan**: `janji transfer sore | bayar sebagian 1 jt tgl 2 Okt`.
- `terkirim --id 2` menaikkan kolom `diingatkan`. Pada 5 Okt (lewat 15 hari, sudah 1x diingatkan) draf CV Maju naik ke
  pemberitahuan tertulis ("paling lambat 12 Okt 2026"). Pada 25 Okt (35 hari, 2x) muncul saran somasi lewat `tagih-piutang`.
- `draf --id 1` pada 1 Okt kini berbunyi "jatuh tempo **lusa**, 3 Okt 2026" (sebelumnya "besok").
