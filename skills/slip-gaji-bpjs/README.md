# Slip Gaji Rapi dengan Hitungan BPJS dan Pajak

**Kirim daftar gaji, langsung jadi slip gaji siap cetak dan rekap payroll (penggajian) lengkap dengan BPJS, lembur, dan PPh 21 (pajak penghasilan karyawan).**

*Diuji AI penguji independen: 5,0 → 9,0 dari 10 (PPh 21 bulan Desember dihitung ulang setahun, sedangkan tanpa skill premi BPJS dari perusahaan terlewat sehingga pajaknya terlalu kecil).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Slip gaji per karyawan siap cetak/PDF (HTML) dan siap tempel (Markdown), plus rekap dalam file CSV (tabel sederhana) yang bisa dibuka di Excel
- ✅ Potongan BPJS Kesehatan & Ketenagakerjaan otomatis, termasuk batas upah Jaminan Pensiun (Rp 11.086.300 sejak Maret 2026; cek ulang tiap tahun)
- ✅ Lembur dihitung sesuai PP 35/2021 (1/173, 1,5x lalu 2x, tarif hari libur)
- ✅ PPh 21 memakai tabel TER resmi (tarif efektif rata-rata, cara potong bulanan sejak 2024), termasuk hitung ulang Desember
- ✅ Tahu total biaya perusahaan dan jumlah yang harus disetor ke BPJS dan pajak, plus peringatan bila gaji di bawah UMK (upah minimum kota/kabupaten)

## Cocok untuk siapa
- Pemilik UMKM dengan 1–50 karyawan yang masih menggaji pakai Excel/kalkulator
- Admin/HR/keuangan yang tiap bulan membuat slip gaji
- Pengusaha yang ingin tahu biaya sebenarnya satu karyawan (gaji + BPJS)

## Contoh sebelum & sesudah
**Sebelum:** Menghitung BPJS satu per satu, lupa batas upah JP naik, lembur hari Minggu dihitung asal, slip diketik ulang di Word.

**Sesudah (cukup ketik):** "Buat slip gaji September: Budi K/1 gapok 5 juta, tunjangan 500 ribu, uang makan 600 ribu, lembur 2+3 jam dan 8 jam hari Minggu, kasbon 100 ribu. UMK 5.396.761."
(K/1 = menikah dengan 1 tanggungan; gapok = gaji pokok. Pesan aslinya memuat 3 karyawan; yang ditampilkan di bawah hanya slip Budi.)

*Cuplikan hasil nyata dari `examples/01-slip-gaji-3-karyawan.md` (sebagian baris dipotong):*
```
# SLIP GAJI — CV Contoh Maju Jaya
**Periode:** September 2026  
**Nama:** Contoh Budi Santoso · Staf Gudang  
**Status PTKP:** K/1
…
| Lembur | Rp 794.798 |
| **Total pendapatan** | **Rp 6.894.798** |
…
| BPJS Kesehatan 1% | Rp 55.000 |
| BPJS TK - JHT 2% | Rp 110.000 |
| BPJS TK - JP 1% | Rp 55.000 |
| PPh 21 | Rp 53.707 |
| Potongan lain | Rp 100.000 |
| **Total potongan** | **Rp 373.707** |
### TAKE HOME PAY: Rp 6.521.091
```
(PTKP = status keluarga yang dipakai untuk hitungan pajak.) Rekap di chat juga menampilkan biaya perusahaan untuk Budi sebesar Rp 7.474.498, plus file rekap CSV (tabel sederhana yang bisa dibuka di Excel).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan slip gaji bulan ini dari file karyawan.csv."
- "Gaji 8 juta TK/0, potongan BPJS dan pajaknya berapa?"
- "Hitung lembur 3 jam hari kerja dan 6 jam hari libur untuk gaji 5 juta."

## Instalasi singkat
Salin folder `slip-gaji-bpjs` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, di OpenClaw (uji otomatis agent, 1 Oktober 2026; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 5,0 tanpa skill menjadi 9,0 dengan skill. Pada slip Desember Budi (K/1, gaji pokok Rp 7.500.000), tanpa skill PPh 21 Desember dihitung Rp 165.000 (premi BPJS yang dibayar perusahaan tidak masuk bruto pajak, kurang Rp 156.595) dan gaji bersih Rp 7.035.000. Dengan skill script menghitung ulang setahun: PPh 21 Desember Rp 321.595, gaji bersih Rp 6.878.405, plus biaya perusahaan dan file slip. Asumsi uji: gaji Januari–November dianggap sama tiap bulan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Bukti uji di bot Telegram ada di bagian berikut.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 4, 2026-10-03. Versi yang diuji tidak tercatat di catatan uji (versi repo saat itu: 1.0.5).
- Tanpa skill: https://t.me/c/4407409583/578/588 — skor tidak dicatat di gelombang itu
- Dengan skill: https://t.me/c/4407409583/579/590 — skor tidak dicatat di gelombang itu
Verdik gelombang: tidak dicatat di gelombang itu — PPh 21 Desember TANPA Rp165.000 (premi BPJS/JKK/JKM yang dibayar perusahaan tidak dimasukkan ke bruto pajak), gaji bersih Rp7.035.000; DENGAN Rp321.595, gaji bersih Rp6.878.405, plus biaya perusahaan Rp8.268.000 dan file slip (selisih Rp156.595; angka dicek ulang kurator dengan python dan cocok).

Diperbaiki di versi 1.0.7 (slip gaji tampil utuh di chat Telegram; 1.0.6 memperjelas catatan PPh 21 DTP di slip, hitungan tidak berubah), belum diuji ulang di bot Telegram.

## FAQ
**Apakah UMK daerah saya sudah ada di dalam skill?**
Tidak, karena UMK berbeda tiap kota dan berubah tiap tahun. Anda cukup menyebutkan angka UMK dari SK Gubernur/Disnaker, lalu skill memberi peringatan bila ada gaji di bawahnya.

**Bagaimana dengan slip bulan Desember?**
Desember pajaknya dihitung ulang setahun, jadi skill akan meminta total penghasilan dan PPh 21 Januari–November. Ini sesuai aturan PMK 168/2023.

**Apakah data gaji karyawan dikirim ke internet?**
Script hitungnya tidak memakai internet: hitungan berjalan di komputer Anda dan file slip disimpan di folder yang Anda tentukan. Isi percakapan (termasuk data gaji yang Anda ketik atau lampirkan) tetap dibaca oleh AI agent yang Anda pakai.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak, hukum, atau ketenagakerjaan. Dasar aturan (berlaku per 23 September 2026): BPJS Kesehatan Perpres 64/2020; BPJS Ketenagakerjaan PP 44/2015 (JKK, JKM), PP 46/2015 (JHT), dan PP 45/2015 (JP) dengan batas upah JP Rp 11.086.300 mulai 1 Maret 2026; lembur PP 35/2021; PPh 21 TER PP 58/2023 dan PMK 168/2023; PPh 21 DTP (ditanggung pemerintah) PMK 105/2025. Batas upah JP dan UMK berubah tiap tahun, jadi cek ulang. Pembulatan iuran dan lembur (ke rupiah terdekat) serta PPh 21 (ke bawah) belum dicocokkan dengan aplikasi BPJS maupun Coretax (sistem pajak online DJP). Bagian PPh 21 DTP PERLU REVIEW konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
