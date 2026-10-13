# Hitung PPh 21 Karyawan Sesuai Tabel Resmi

**Ketik gaji dan status karyawan, langsung dapat potongan PPh 21 (pajak penghasilan karyawan) per bulan sampai Desember — sesuai tabel TER resmi (tarif efektif rata-rata, cara potong PPh 21 bulanan sejak 2024).**

*Diuji AI penguji independen: 7,25 → 8,9 dari 10 (selisih tipis karena angka tarif tanpa skill juga benar; skill unggul di kecepatan, cek sektor usaha untuk PPh 21 ditanggung pemerintah, dan hitungan Desember plus THR yang konsisten).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tarif diambil dari tabel TER resmi PP 58/2023 (127 baris), bukan dikira-kira — dicocokkan dengan contoh hitungan resmi di PP 58/2023, PMK 168/2023, dan PMK 105/2025 lewat uji otomatis
- ✅ Desember atau bulan karyawan resign dihitung ulang otomatis, termasuk kelebihan potong yang harus dikembalikan
- ✅ Bisa untuk karyawan tetap, karyawan baru/keluar di tengah tahun, dan pekerja harian/borongan
- ✅ Mengecek hak PPh 21 Ditanggung Pemerintah (DTP) 2026 (PMK 105/2025) untuk industri tertentu — sektor usaha ditanyakan dulu, bukan diasumsikan
- ✅ Hasil berupa tabel per bulan + ringkasan setahun yang siap ditempel ke laporan

## Cocok untuk siapa
- Pemilik usaha yang menggaji karyawan sendiri tanpa software penggajian (payroll)
- Admin/HR/staf keuangan yang harus setor dan lapor PPh 21 tiap bulan
- Karyawan yang ingin mengecek potongan pajak di slip gajinya

## Contoh sebelum & sesudah
**Sebelum:** Mencari tabel TER di internet, bingung karyawan K/1 masuk kategori mana, lalu kaget potongan Desember jauh lebih besar dan tidak tahu cara menghitungnya.

**Sesudah (cukup ketik):** "Karyawan saya statusnya K/1, gaji 12 juta sebulan. THR 12 juta dibayar bulan Maret. Iuran JHT+JP yang dipotong dari gajinya 360 ribu per bulan. PPh 21 setahun 2026 berapa aja per bulannya?" (K/1 = menikah dengan 1 tanggungan; JHT dan JP = iuran BPJS untuk hari tua dan pensiun)

*Cuplikan hasil nyata dari `examples/01-setahun-dengan-thr.md` (bulan lain dan sebagian rincian dipotong):*
```
**PPh 21 2026 — status K/1 (TER kategori B)**
| Bulan | Penghasilan bruto | Tarif TER | PPh 21 dipotong |
|---|---:|---:|---:|
| Januari | Rp 12.000.000 | 3% | Rp 360.000 |
| Maret | Rp 24.000.000 | 9% | Rp 2.160.000 |
…
| Desember | Rp 12.000.000 | Pasal 17 (hitung ulang) | Rp 642.000 |
| **Jumlah** | **Rp 156.000.000** | | **Rp 6.402.000** |
**Hitung ulang Masa Pajak Terakhir (Desember)**
…
- PTKP K/1: Rp 63.000.000
- PKP (dibulatkan ke bawah ke ribuan): Rp 82.680.000
- PPh 21 terutang setahun: Rp 6.402.000
- Sudah dipotong bulan-bulan sebelumnya: Rp 5.760.000
- **PPh 21 dipotong di Desember: Rp 642.000**
```
(TER = tarif efektif rata-rata; PTKP = batas penghasilan yang tidak dikenai pajak; PKP = penghasilan yang dikenai pajak.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "PPh 21 gaji 8,5 juta status TK/0 berapa?"
- "Karyawan K/2 gaji 15 juta, THR dibayar Maret, hitung PPh 21 setahun."
- "Karyawan resign akhir Agustus, gaji 17,5 juta TK/0, PPh 21 terakhirnya berapa?"
- "Tukang harian 300 ribu sehari kerja 20 hari, PPh 21-nya?"

## Instalasi singkat
Salin folder `pph21-ter` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, di OpenClaw (uji otomatis agent, 5 Oktober 2026, v1.0.5; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 7,25 tanpa skill menjadi 8,9 dengan skill. Catatan jujur: selisihnya tipis karena angka tarif tanpa skill juga benar di uji ini. Pembeda skill: menanyakan sektor/KLU (kode bidang usaha di data pajak) dulu sebelum menyimpulkan PPh 21 DTP 2026 (gaji Rp 6.000.000, TK/0: PPh dipotong Rp 45.000, DTP dibayar tunai Rp 45.000, setoran ke negara Rp 0, uang diterima Rp 6.000.000), dan hitungan Desember plus THR selesai dalam sekitar 40 detik oleh script (tanpa skill sekitar 11 menit dengan 12 pencarian web). Catatan jujur lain: pada uji di bot Telegram (bagian berikut) versi 1.0.4 sempat kalah (skor 6 lawan 8) karena salah menyebut uang yang diterima pegawai penerima DTP; ini diperbaiki di versi 1.0.5.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 7, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/736/754 — skor 8
- Dengan skill: https://t.me/c/4407409583/737/757 — skor 6
Verdik gelombang: BELUM — DENGAN lebih rapi (TER A 0,75% = Rp45.000, minta konfirmasi KLU, syarat bruto Januari 2026) tetapi **salah di jawaban inti**: "uang diterima Rp6.045.000" (gaji + DTP, PPh "dipotong Rp0"). Menurut teks PMK 105/2025, PPh 21 tetap dipotong lalu nilai DTP dibayar tunai, sehingga pegawai menerima Rp6.000.000. Nominal ini sama dengan jawaban TANPA.

Kekurangan ini diperbaiki di versi 1.0.5 (lihat `CHANGELOG.md`).

## FAQ
**Kenapa potongan Desember berbeda dari bulan lain?**
Aturannya memang begitu: Januari–November memakai tarif TER dari tabel, sedangkan Desember (atau bulan karyawan berhenti) dihitung ulang dengan tarif pajak tahunan lalu dikurangi potongan sebelumnya. Skill ini menampilkan rincian hitungannya supaya mudah dijelaskan ke karyawan.

**Apakah hasilnya sama dengan Coretax (sistem pajak online DJP)?**
Tarif dan rumusnya sama dengan aturan resmi dan sudah dicocokkan dengan contoh resmi pemerintah yang dipakai sebagai uji otomatis. Pembulatan rupiah belum dicocokkan dengan Coretax; jika ada selisih kecil, ikuti angka Coretax.

**Perusahaan saya di industri tekstil, apakah dapat PPh 21 DTP?**
Skill akan menanyakan sektor dan mengecek syarat gaji (maks. Rp 10 juta). Kepastian KLU (kode bidang usaha) perusahaan tetap perlu dicek di data pajak perusahaan (Coretax) atau ke kantor pajak. Bila berhak, PPh 21 karyawan tetap dipotong lalu nilai yang sama **wajib Anda bayarkan tunai** kembali ke karyawan bersama gaji, dan bagian itu tidak perlu disetor ke negara. Hasilnya karyawan menerima gaji tanpa berkurang pajak (mis. gaji Rp 6.000.000 − PPh Rp 45.000 + DTP Rp 45.000 = diterima Rp 6.000.000; setoran Rp 0). Skill menuliskan angka ini dari hitungan script.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak. Dasar aturan (berlaku per 23 September 2026): PP 58/2023 (tabel TER, berlaku sejak 1 Januari 2024), PMK 168/2023, UU HPP (tarif Pasal 17), dan PMK 105/2025 untuk PPh 21 ditanggung pemerintah Masa Pajak Januari–Desember 2026. PPh dibulatkan ke bawah dan pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Bagian PPh 21 DTP PERLU REVIEW konsultan pajak. Kasus khusus: Kring Pajak 1500200 atau konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
