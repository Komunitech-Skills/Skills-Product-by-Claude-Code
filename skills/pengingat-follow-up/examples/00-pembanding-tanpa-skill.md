# 00 — Uji A/B: skenario 01 TANPA skill vs DENGAN skill

Tanggal uji: 2026-09-23 · Penguji: agent penguji independen (simulasi, Claude Code) · Hari acuan skenario: Kamis 1 Okt 2026.

**Input (sama untuk keduanya):**
> tolong catet bon2 ini ya biar ga lupa nagih:
> - Bu Rina 4,5 jt jatuh tempo 3 Okt, nota 0412 beras & minyak
> - CV Maju 750rb tgl 20/9 nota 0398
> - Toko Sinar Rp1.250.000 besok, nota 0405
> - Pak Harto 2 jt 300 rb tgl 1, katanya mau transfer sore
> terus hari ini saya harus nagih siapa aja?

## A. TANPA skill (agent umum, tanpa memuat skill apa pun; dijawab seperti AI agent biasa)
```
Baik, ini catatan piutang Anda (hari ini 1 Oktober 2026):

| Pelanggan  | Nominal      | Jatuh tempo  | Status              |
|------------|--------------|--------------|---------------------|
| Bu Rina    | Rp4.500.000  | 3 Oktober    | 2 hari lagi         |
| CV Maju    | Rp750.000    | 20 September | Terlambat 11 hari   |
| Toko Sinar | Rp1.250.000  | 2 Oktober    | Besok               |
| Pak Harto  | Rp2.300.000  | 1 Oktober    | Hari ini            |

Total piutang: Rp8.800.000

Yang perlu ditagih hari ini:
1. CV Maju (sudah terlambat 11 hari) - Rp750.000
2. Pak Harto (jatuh tempo hari ini) - Rp2.300.000

Contoh pesan penagihan:
"Halo Bapak/Ibu, kami ingin mengingatkan bahwa tagihan Anda sebesar [nominal] sudah jatuh tempo.
Mohon segera melakukan pembayaran. Terima kasih."

Catatan: saya tidak bisa menyimpan data ini atau mengingatkan Anda secara otomatis di kemudian hari.
Sebaiknya simpan daftar ini di Excel/Google Sheets dan pasang pengingat di kalender HP Anda.
```

## B. DENGAN skill `pengingat-follow-up`
Output lengkap di `01-piutang-toko-grosir.md`. Inti:
```
Tersimpan #1..#4 (+ Catatan: tahun/bulan ditebak, "20/9" masuk TERLAMBAT 11 hari)

PENGINGAT FOLLOW-UP - Kamis, 1 Oktober 2026
TERLAMBAT (1)  #2 CV Maju | Rp 750.000 | nota 0398 | lewat 11 hari (jatuh tempo 20 Sep 2026)
HARI INI (1)   #4 Pak Harto | Rp 2.300.000 | jatuh tempo hari ini  (Catatan: janji transfer sore)
BESOK / H-1 (1) #3 Toko Sinar | Rp 1.250.000 | nota 0405 | besok, 2 Okt 2026
Total piutang tertunggak (terlambat + hari ini): Rp 3.050.000
Piutang jatuh tempo besok: Rp 1.250.000
DRAF PESAN per pelanggan (nada sesuai tahap: CV Maju minta tanggal pasti s.d. 4 Okt; Pak Harto ramah hari-H;
Toko Sinar pengingat H-1), dikirim sendiri oleh pemilik.
```

## Penilaian berdampingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Pembacaan tanggal/nominal campur | Benar untuk kasus ini | Benar, plus `Catatan:` asumsi tahun/bulan |
| Angka | Total Rp 8.800.000 (semua piutang) — benar, tapi tidak memisahkan yang sudah jatuh tempo | Tertunggak Rp 3.050.000 + besok Rp 1.250.000, dihitung script, terverifikasi independen |
| Tersimpan & bisa diperbarui ("Toko Sinar lunas") | Tidak (hilang setelah sesi) | Ya, file lokal `pengingat/DAFTAR.csv`, perintah selesai/tunda/ubah |
| Pengingat otomatis | Tidak ada; menyarankan kalender HP | Rekap 08.00 WIB ke Telegram pemilik via OpenClaw (sintaks teruji) |
| Draf pesan | Satu template generik dengan placeholder, nada "segera" untuk semua | Draf per pelanggan, nominal & nota terisi, nada bertahap, tanpa ancaman |
| Privasi | Tidak dibahas | Nomor HP/email/NIK ditolak, catatan pribadi tidak masuk draf |
| Siap kirim | Perlu diedit | Siap salin (tinggal isi `[rekening]`) |

**Kesimpulan A/B:** dengan skill **jelas lebih baik**: daftar tersimpan dan bisa diubah lewat chat, rekap
terkelompok (terlambat/hari ini/H-1), angka dari script, draf per pelanggan dengan nada bertahap, serta jadwal
otomatis ke Telegram. Agent polos memberi jawaban sekali pakai tanpa tindak lanjut. Bahan "sebelum/sesudah"
README sudah sesuai dengan perbandingan ini.
