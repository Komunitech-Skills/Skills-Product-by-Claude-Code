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

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah UMK daerah saya sudah ada di dalam skill?**
Tidak, karena UMK berbeda tiap kota dan berubah tiap tahun. Kamu cukup menyebutkan angka UMK dari SK Gubernur/Disnaker, lalu skill memberi peringatan bila ada gaji di bawahnya.

**Bagaimana dengan slip bulan Desember?**
Desember pajaknya dihitung ulang setahun, jadi skill akan meminta total penghasilan dan PPh 21 Januari–November. Ini sesuai aturan PMK 168/2023.

**Apakah data gaji karyawan dikirim ke internet?**
Tidak. Hitungan berjalan di komputer kamu dan file slip disimpan di folder yang kamu tentukan.
