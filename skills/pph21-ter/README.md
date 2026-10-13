# Hitung PPh 21 Karyawan Tanpa Salah Tabel

**Ketik gaji dan status karyawan, langsung dapat potongan PPh 21 per bulan sampai Desember — sesuai tabel TER resmi.**

## Manfaat
- ✅ Tarif diambil dari tabel TER resmi PP 58/2023 (127 baris), bukan dikira-kira — sudah diuji dengan semua contoh hitungan resmi DJP
- ✅ Desember atau bulan karyawan resign dihitung ulang otomatis, termasuk kelebihan potong yang harus dikembalikan
- ✅ Bisa untuk karyawan tetap, karyawan baru/keluar di tengah tahun, dan pekerja harian/borongan
- ✅ Mengecek hak PPh 21 Ditanggung Pemerintah 2026 (PMK 105/2025) untuk industri tertentu — tanpa asal menganggap
- ✅ Hasil berupa tabel per bulan + ringkasan setahun yang siap ditempel ke laporan

## Cocok untuk siapa
- Pemilik usaha yang menggaji karyawan sendiri tanpa software payroll
- Admin/HR/staf keuangan yang harus setor dan lapor PPh 21 tiap bulan
- Karyawan yang ingin mengecek potongan pajak di slip gajinya

## Contoh sebelum & sesudah
**Sebelum:** Mencari tabel TER di internet, bingung karyawan K/1 masuk kategori mana, lalu kaget potongan Desember jauh lebih besar dan tidak tahu cara menghitungnya.

**Sesudah (cukup ketik):** "Karyawan K/0 gaji 10 juta, iuran pensiun 100 ribu, PPh 21 setahun berapa?"
→ Tabel Januari–Desember: Rp 200.000 per bulan (TER 2%), Desember Rp 515.000, lengkap dengan rincian biaya jabatan, PTKP, dan PKP — sama persis dengan contoh resmi pemerintah.

**Hasil uji (OpenClaw, uji otomatis agent, 5 Oktober 2026, v1.0.5):** rata-rata nilai 7,25 tanpa skill menjadi 8,9 dengan skill (skala 10). Catatan jujur: selisihnya tipis karena angka TER tanpa skill juga benar di uji ini. Pembeda skill: menanyakan sektor/KLU dulu sebelum menyimpulkan PPh 21 DTP 2026 (gaji Rp 6.000.000, TK/0: PPh dipotong Rp 45.000, DTP dibayar tunai Rp 45.000, setoran ke negara Rp 0, uang diterima Rp 6.000.000), dan hitungan Desember plus THR selesai dalam sekitar 40 detik oleh script (tanpa skill sekitar 11 menit dengan 12 pencarian web). Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "PPh 21 gaji 8,5 juta status TK/0 berapa?"
- "Karyawan K/2 gaji 15 juta, THR dibayar Maret, hitung PPh 21 setahun."
- "Karyawan resign akhir Agustus, gaji 17,5 juta TK/0, PPh 21 terakhirnya berapa?"
- "Tukang harian 300 ribu sehari kerja 20 hari, PPh 21-nya?"

## Instalasi singkat
Salin folder `pph21-ter` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 7, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/736/754 — skor 8
- Dengan skill: https://t.me/c/4407409583/737/757 — skor 6
Verdik gelombang: BELUM — DENGAN lebih rapi (TER A 0,75% = Rp45.000, minta konfirmasi KLU, syarat bruto Januari 2026) tetapi **salah di jawaban inti**: "uang diterima Rp6.045.000" (gaji + DTP, PPh "dipotong Rp0"). Menurut teks PMK 105/2025, PPh 21 tetap dipotong lalu nilai DTP dibayar tunai, sehingga pegawai menerima Rp6.000.000. Nominal ini sama dengan jawaban TANPA.

## FAQ
**Kenapa potongan Desember berbeda dari bulan lain?**
Aturannya memang begitu: Januari–November memakai tarif TER dari tabel, sedangkan Desember (atau bulan karyawan berhenti) dihitung ulang dengan tarif pajak tahunan lalu dikurangi potongan sebelumnya. Skill ini menampilkan rincian hitungannya supaya mudah dijelaskan ke karyawan.

**Apakah hasilnya pasti sama dengan Coretax?**
Tarif dan rumusnya sama dengan aturan resmi dan sudah dicocokkan dengan contoh resmi DJP. Pembulatan rupiah belum dicocokkan dengan Coretax; jika ada selisih kecil, ikuti angka Coretax.

**Perusahaan saya di industri tekstil, apakah dapat PPh 21 DTP?**
Skill akan menanyakan sektor dan mengecek syarat gaji (maks. Rp 10 juta). Kepastian KLU perusahaan tetap perlu dicek di data pajak perusahaan (Coretax) atau ke kantor pajak. Bila berhak, PPh 21 karyawan tetap dipotong lalu nilai yang sama **wajib Anda bayarkan tunai** kembali ke karyawan bersama gaji, dan bagian itu tidak perlu disetor ke negara. Hasilnya karyawan menerima gaji tanpa berkurang pajak (mis. gaji Rp 6.000.000 − PPh Rp 45.000 + DTP Rp 45.000 = diterima Rp 6.000.000; setoran Rp 0). Skill menuliskan angka ini dari hitungan script.

> **Catatan penting:** alat bantu hitung, bukan nasihat pajak. Dasar aturan (berlaku per 23 September 2026): PP 58/2023 (tabel TER, berlaku sejak 1 Januari 2024), PMK 168/2023, UU HPP (tarif Pasal 17), dan PMK 105/2025 untuk PPh 21 ditanggung pemerintah Masa Pajak Januari–Desember 2026. PPh dibulatkan ke bawah dan pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Bagian PPh 21 DTP PERLU REVIEW konsultan pajak. Kasus khusus: Kring Pajak 1500200 atau konsultan pajak.

## Catatan revisi 1.0.5 (2026-10-05)
- **Koreksi PPh 21 DTP (PMK 105/2025):** versi 1.0.4 menulis "PPh 21 dipotong Rp 0" dan "uang diterima = gaji + DTP" (contoh Rp 6.045.000). Setelah teks resmi dibaca ulang (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B), mekanisme yang benar: PPh 21 tetap dipotong, DTP dengan nilai sama dibayar tunai ke pegawai, sehingga pegawai menerima **Rp 6.000.000** (gaji tidak berkurang pajak), dan setoran ke negara untuk bagian DTP Rp 0. Script kini mencetak empat baris: PPh dipotong, DTP tunai, setoran ke negara, uang diterima. Ringkasan dasar hukum: `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**

## Catatan revisi 1.0.4 (2026-10-01)
> **DIKOREKSI di 1.0.5 (2026-10-05):** butir DTP di bawah ini **keliru** dan dibiarkan hanya sebagai riwayat. Menurut PMK 105/2025, PPh 21 DTP **tetap dipotong** (bukan Rp 0) lalu nilai yang sama dibayar tunai, sehingga pegawai gaji Rp 6.000.000 **menerima Rp 6.000.000**, bukan Rp 6.045.000. Lihat "Catatan revisi 1.0.5" di atas dan `references/dtp-pmk105.md`.

- ~~Dari uji OpenClaw sebelum/sesudah: untuk karyawan penerima **PPh 21 DTP 2026**, jawaban sempat menyebut gaji diterima "Rp 6.000.000 utuh", padahal PMK 105/2025 Pasal 5 mewajibkan PPh 21 DTP **dibayarkan tunai** ke karyawan (yang benar Rp 6.045.000). Kini hitungan satu bulan (`bulan`) juga mendukung `--dtp` dan mencetak tiga baris wajib: PPh 21 dipotong dari gaji (Rp 0), DTP yang wajib dibayar tunai, dan **uang yang diterima pegawai**; AI wajib mengutip baris itu dari script. Hitungan setahun dengan DTP juga menegaskan hal yang sama.~~ *(dikoreksi di 1.0.5: yang benar PPh 21 dipotong Rp 45.000, DTP tunai Rp 45.000, diterima Rp 6.000.000 sesuai PMK 105/2025)*
- Istilah seperti KLU, TER, Masa Pajak Terakhir, dan DTP kini dijelaskan dengan bahasa sehari-hari saat pertama muncul.
