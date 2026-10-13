# Slip Gaji Rapi, BPJS dan Pajak Beres

**Kirim daftar gaji, langsung jadi slip gaji siap cetak dan rekap payroll lengkap dengan BPJS, lembur, dan PPh 21.**

## Manfaat
- ✅ Slip gaji per karyawan siap cetak/PDF (HTML) dan siap tempel (Markdown), plus rekap CSV untuk Excel
- ✅ Potongan BPJS Kesehatan & Ketenagakerjaan otomatis, termasuk batas upah Jaminan Pensiun terbaru (Rp 11.086.300 mulai Maret 2026)
- ✅ Lembur dihitung sesuai PP 35/2021 (1/173, 1,5x lalu 2x, tarif hari libur)
- ✅ PPh 21 memakai tabel TER resmi, termasuk hitung ulang Desember
- ✅ Tahu total biaya perusahaan dan jumlah yang harus disetor ke BPJS dan pajak, plus peringatan bila gaji di bawah UMK

## Cocok untuk siapa
- Pemilik UMKM dengan 1–50 karyawan yang masih menggaji pakai Excel/kalkulator
- Admin/HR/keuangan yang tiap bulan membuat slip gaji
- Pengusaha yang ingin tahu biaya sebenarnya satu karyawan (gaji + BPJS)

## Contoh sebelum & sesudah
**Sebelum:** Menghitung BPJS satu per satu, lupa batas upah JP naik, lembur hari Minggu dihitung asal, slip diketik ulang di Word.

**Sesudah (cukup ketik):** "Buat slip gaji September: Budi K/1 gapok 5 juta, tunjangan 500 ribu, uang makan 600 ribu, lembur 2+3 jam dan 8 jam hari Minggu, kasbon 100 ribu. UMK 5.396.761."
→ Slip siap cetak: lembur Rp 794.798, BPJS Rp 220.000, PPh 21 Rp 53.707, take home pay Rp 6.521.091, biaya perusahaan Rp 7.474.498 — plus file rekap CSV.

**Hasil uji (OpenClaw, uji otomatis agent, 1 Oktober 2026):** rata-rata nilai 5,0 tanpa skill menjadi 9,0 dengan skill (skala 10). Pada slip Desember Budi (K/1, gaji pokok Rp 7.500.000), tanpa skill PPh 21 Desember dihitung Rp 165.000 (premi BPJS yang dibayar perusahaan tidak masuk bruto pajak, kurang Rp 156.595) dan gaji bersih Rp 7.035.000. Dengan skill script menghitung ulang setahun: PPh 21 Desember Rp 321.595, gaji bersih Rp 6.878.405, plus biaya perusahaan dan file slip. Asumsi uji: gaji Januari–November dianggap sama tiap bulan. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan slip gaji bulan ini dari file karyawan.csv."
- "Gaji 8 juta TK/0, potongan BPJS dan pajaknya berapa?"
- "Hitung lembur 3 jam hari kerja dan 6 jam hari libur untuk gaji 5 juta."

## Instalasi singkat
Salin folder `slip-gaji-bpjs` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 4, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/578/588 — skor: lihat catatan gelombang
- Dengan skill: https://t.me/c/4407409583/579/590 — skor: lihat catatan gelombang
Verdik gelombang: — — PPh 21 Desember TANPA Rp165.000 (premi BPJS yang dibayar perusahaan tidak masuk bruto pajak) vs DENGAN Rp321.595, plus biaya perusahaan dan file slip (selisih Rp156.595).

## FAQ
**Apakah UMK daerah saya sudah ada di dalam skill?**
Tidak, karena UMK berbeda tiap kota dan berubah tiap tahun. Kamu cukup menyebutkan angka UMK dari SK Gubernur/Disnaker, lalu skill memberi peringatan bila ada gaji di bawahnya.

**Bagaimana dengan slip bulan Desember?**
Desember pajaknya dihitung ulang setahun, jadi skill akan meminta total penghasilan dan PPh 21 Januari–November. Ini sesuai aturan PMK 168/2023.

**Apakah data gaji karyawan dikirim ke internet?**
Tidak. Hitungan berjalan di komputer kamu dan file slip disimpan di folder yang kamu tentukan.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak, hukum, atau ketenagakerjaan. Dasar aturan (berlaku per 23 September 2026): BPJS Kesehatan Perpres 64/2020; BPJS Ketenagakerjaan PP 44/2015 (JKK, JKM), PP 46/2015 (JHT), dan PP 45/2015 (JP) dengan batas upah JP Rp 11.086.300 mulai 1 Maret 2026; lembur PP 35/2021; PPh 21 TER PP 58/2023 dan PMK 168/2023; PPh 21 DTP PMK 105/2025. Batas upah JP dan UMK berubah tiap tahun, jadi cek ulang. Pembulatan iuran dan lembur (ke rupiah terdekat) serta PPh 21 (ke bawah) belum dicocokkan dengan aplikasi BPJS maupun Coretax. Bagian PPh 21 DTP PERLU REVIEW konsultan pajak.

## Catatan revisi 1.0.7 (2026-10-12)
- Di Telegram/WhatsApp, slip gaji kini **tampil langsung di chat** (teks rapi tanpa tabel): semua slip untuk 1–3 karyawan, atau 3 slip pertama + rekap total bila lebih dari 3. File siap cetak dilampirkan bila bisa; bila tidak, cukup balas "kirim file". Rumus dan angka tidak berubah.

## Catatan revisi 1.0.6 (2026-10-05)
- Pemeriksaan ulang PPh 21 DTP terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B): hitungan slip **sudah benar** sejak awal (PPh 21 tetap dipotong, DTP dengan nilai sama dibayar tunai, take home pay tidak berkurang karena pajak, setoran PPh 21 bagian DTP Rp 0). Yang diperbaiki: catatan di slip (Markdown & HTML) kini menulis jelas PPh dipotong, DTP dibayar tunai, dan **setoran ke negara Rp 0** per karyawan; tambah tes regresi dan ringkasan dasar hukum `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**
