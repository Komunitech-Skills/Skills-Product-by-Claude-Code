# 03 — Klinik: catat absen lewat chat, laporan harian ke Telegram, ekspor untuk slip-gaji-bpjs

> **Catatan revisi 1.0.8:** teks rekap di bawah disesuaikan dengan keluaran skrip terbaru (kode karyawan disembunyikan, "kelonggaran telat" menggantikan "toleransi terlambat"). Angkanya tidak berubah dari hasil uji aslinya.

**Skenario:** normal, pencatatan manual (tanpa mesin). Klinik fiktif, 4 karyawan pola 6 hari (Senin–Jumat 08.00–16.00, Sabtu 08.00–13.00), toleransi 10 menit, mulai memakai alat pada 23/09/2026. Admin mengetik absen lewat chat. Pengujian memakai opsi tersembunyi `--sekarang` hanya untuk membekukan jam uji (23–24/09/2026); pembeli tidak memakainya.

## Input pengguna (persis, beberapa pesan)

> Andi masuk 08.12
>
> Sari izin sakit
>
> Rina masuk 07.58
>
> Tono 25.10 eh salah, Tono masuk 08.31
>
> kirimin rekap hari ini dong, terus tiap hari jam 10 kirim ke telegram saya ya

(Akhir bulan) 
> rekap september + masukin lemburnya ke file gaji saya ini (gaji-september.csv) buat slip

## Output (mengikuti SKILL.md)

**"Andi masuk 08.12"** → `catat --karyawan Andi --masuk 08.12`:
```
Saya akan mencatat (belum disimpan):
- Andi - Kamis 24/09/2026: masuk 08.12
Catatan: Terlambat 12 menit (jadwal 08.00, kelonggaran telat 10 menit).
Simpan? Balas "ya".
```

**"Sari izin sakit"** → agent memilih jenis `sakit` (kata "sakit" disebut) dan menyebut asumsinya → `keterangan --karyawan Sari --jenis sakit --tanggal 2026-09-24 --catatan "izin via WA"`:
```
Saya akan mencatat (belum disimpan):
- Sari: SAKIT pada 1 hari kerja (24/09/2026)
Saya catat sebagai SAKIT (bukan izin biasa). Simpan? Balas "ya".
```

**"Tono 25.10"** → script menolak: `GAGAL: Jam masuk '25.10' tidak valid. Contoh benar: 08.12 atau 17:05 (jam 00-23, menit 00-59).` → agent: "Jam 25.10 tidak ada. Maksudnya jam berapa?" — pengguna sendiri sudah mengoreksi: 08.31 → pratinjau "Terlambat 31 menit" → "ya".

**Laporan harian** (`harian`, siap tempel ke Telegram/WA):
```
ABSENSI KAMIS, 24/09/2026 (per 10.05) - Klinik Sehat Sentosa (fiktif)
Hadir 3 dari 4 karyawan terjadwal
Terlambat: Andi 08.12 (12 menit), Tono 08.31 (31 menit)
Izin/sakit/cuti/alpa/dinas: Sari (sakit)
```

**Jadwal Telegram tiap jam 10** (mengikuti `references/openclaw-jadwal.md`, Telegram = default; minta izin dulu):
```
Saya akan membuat jadwal di OpenClaw (belum dibuat). Syarat: komputer ini menyala 24 jam dan
bot Telegram sudah tersambung. Jadwal hanya MEMBACA laporan, tidak pernah mengubah data.

openclaw automations add --name "Absensi harian" --cron "0 10 * * 1-6" --tz Asia/Jakarta \
  --command-argv '["python3","/home/NAMA/.openclaw/skills/absensi-lokal/scripts/absensi.py","harian"]' \
  --announce --channel telegram --to <chat-id-telegram-Anda>

Setelah dibuat, uji sekarang: openclaw automations run <id>, lalu cek openclaw automations runs <id>.
Boleh saya buat? Saya perlu chat id Telegram Anda.
```

**Akhir bulan** — `rekap --bulan 2026-09 --csv-gaji gaji-september-lembur.csv --gabung gaji-september.csv` (lembur Andi 23/09 2 jam "dr. Maya (WA 23/09 15.30)" sudah dicatat sebelumnya):
```
REKAP ABSENSI SEPTEMBER 2026 - Klinik Sehat Sentosa (fiktif)
Periode 01/09/2026-24/09/2026 | kelonggaran telat 10 menit

1. Andi - Perawat
   Hadir 2 dari 2 hari kerja
   Terlambat 1x (12 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 16 jam 8 menit
   Lembur disetujui: hari kerja 2 jam, hari libur 0 jam (setara 3,5 jam) -> Rp 84.971

2. Sari - Admin
   Hadir 1 dari 2 hari kerja | Sakit 1
   Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 7 jam 1 menit

3. Rina - Apoteker
   Hadir 2 dari 2 hari kerja
   Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 14 jam 4 menit

4. Tono - Kebersihan
   Hadir 2 dari 2 hari kerja
   Terlambat 1x (31 menit) | Pulang cepat 1x (40 menit)
   Jam kerja 12 jam 59 menit

Total upah lembur: Rp 84.971

Upah lembur: PP 35/2021 Pasal 31-32 (...) bukan nasihat hukum; (...)

File untuk slip-gaji-bpjs: gaji-september-lembur.csv
Catatan: Jalankan slip-gaji-bpjs dengan --hari-kerja 6.
Catatan: slip-gaji-bpjs menghitung ulang rupiah lembur dari gaji pokok + tunjangan tetap di file gajinya; bandingkan dengan angka rekap ini.
```
`gaji-september-lembur.csv` (file gaji pengguna + kolom lembur terisi):
```
nama;jabatan;nik;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;lembur_hari_kerja;lembur_hari_libur;bonus;potongan_lain
Andi;Perawat;K01;K/1;3.800.000;400.000;;2;;;
Sari;Admin;K02;TK/0;3.500.000;300.000;;;;;
Rina;Apoteker;K03;K/2;5.000.000;500.000;;;;;
Tono;Kebersihan;K04;TK/0;3.200.000;;;;;;50.000
```
Dijalankan ke `slip-gaji-bpjs/scripts/payroll.py --periode 2026-09 --hari-kerja 6`: diterima, lembur Andi di slip = Rp 84.971 (sama dengan rekap).

## Catatan penguji
- Angka dicek manual: Andi 23/09 07.55–18.10 − 60 = 9:15, 24/09 08.12–16.05 − 60 = 6:53 → 16:08 ✓; Tono 07.50–15.20 − 60 = 6:30 dan 08.31–16.00 − 60 = 6:29 → 12:59 ✓, pulang cepat 40 menit ✓; lembur 3,5 × 4.200.000 ÷ 173 = 84.971,10 → Rp 84.971 ✓.
- Sintaks `openclaw automations add` (termasuk `--command-argv`, `--tz`, `--announce --channel telegram --to`, `--session isolated --tools exec,read`) dicek dengan CLI OpenClaw 2026.9.5 asli: opsi diterima, perintah berhenti di tahap kredensial Gateway (tidak ada Gateway di lingkungan uji). Pengiriman Telegram tidak diuji.
- Bagus: jam tidak valid ditolak dengan contoh; terlambat langsung disebut; `--gabung` mengisi file gaji tanpa mengubah kolom lain; laporan harian ringkas.
- Kurang: (1) "izin sakit" ambigu — SKILL.md tidak memberi aturan izin vs sakit; (2) cron contoh `1-6` (Senin–Sabtu) cocok untuk pola 6 hari, tetapi untuk usaha pola 5 hari laporan Sabtu akan kosong — referensi sebaiknya menyebut `1-5`; (3) nama karyawan kembar/awalan (mis. "An") ditangani script (ambigu → minta kode), baik.
