# Hitung THR Karyawan Sesuai Aturan Terbaru

**Sebutkan tanggal hari raya dan data karyawan, langsung dapat rincian THR, potongan pajaknya, batas bayar, dan pengumuman siap kirim.**

Diuji AI penguji independen: 9 dari 10 (uji ulang di OpenClaw, hanya dengan skill: 8,5 dari 10); tanpa skill, masa kerja bisa salah hitung (kelebihan Rp 400.000) dan pajak tidak dihitung.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Mengikuti Permenaker 6/2016 dan Surat Edaran Menaker THR 2026 — termasuk karyawan baru, kontrak, dan harian lepas
- ✅ Kasus tepi dihitung dengan aturan yang jelas: masa kerja 11 bulan (proporsional) vs 12 bulan (penuh), kurang dari 1 bulan, karyawan PHK menjelang hari raya
- ✅ Menampilkan tambahan potongan PPh 21 (pajak penghasilan karyawan) di bulan THR dibayar, dihitung dari tabel TER (tarif pajak bulanan resmi), jadi karyawan tidak kaget
- ✅ Mengingatkan batas bayar paling lambat 7 hari sebelum hari raya (H-7) dan denda 5% bila terlambat
- ✅ Draf pengumuman THR siap kirim ke grup WhatsApp/email

## Cocok untuk siapa
- Pemilik usaha/UMKM yang membayar THR Lebaran, Natal, Nyepi, Waisak, atau Imlek
- Admin/HR yang harus menyiapkan daftar THR untuk banyak karyawan
- Karyawan yang ingin mengecek apakah THR-nya sudah sesuai aturan

## Contoh sebelum & sesudah
**Sebelum:** Bingung karyawan yang baru 8 bulan dapat berapa, uang makan ikut dihitung atau tidak, dan kenapa gaji bulan Lebaran dipotong pajak lebih besar.

**Sesudah (cukup ketik):** "Lebaran 10 Maret 2027. Rina kontrak gaji 4,8 juta, masuk 15 Juni 2026, TK/0."
→ AI menghitung masa kerja, THR, tambahan pajak, dan batas bayar, lalu menyiapkan draf pengumuman. Cuplikan keluaran nyata dari uji (baris karyawan lain dipotong):
```
Rincian THR Idul Fitri 1448 H — CV Contoh Maju Jaya
Hari raya: Rabu, 10 Maret 2027 · Batas bayar (H-7): Rabu, 3 Maret 2027 · Rencana bayar: Rabu, 3 Maret 2027

| Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | PPh 21 karena THR | THR diterima |
|---|---|---:|---:|---|---:|---:|---:|
…
| Contoh Rina | Kontrak (PKWT) | 8 bln | Rp 4.800.000 | 8/12 × upah | Rp 3.200.000 | Rp 120.000 | Rp 3.080.000 |
…
- Contoh Rina: PPh 21 bulan THR dibayar (TER A) = 1,5% × (Rp 4.800.000 + THR Rp 3.200.000) = Rp 120.000; tanpa THR 0% × Rp 4.800.000 = Rp 0 → tambahan Rp 120.000.
- THR wajib dibayar penuh (tidak dicicil) paling lambat 7 hari sebelum hari raya. Terlambat: denda 5% dari total THR, dan THR tetap wajib dibayar (Permenaker 6/2016 Pasal 10).
```
(TK/0 = status pajak belum menikah, tanpa tanggungan; PKWT = karyawan kontrak; TER = tarif PPh 21 bulanan. Draf pengumuman lengkapnya ada di folder `examples/`.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Hitung THR Lebaran untuk karyawan di file karyawan.csv, Lebaran tanggal 10 Maret 2027." (file daftar karyawan dari Excel yang disimpan sebagai CSV, yaitu file tabel sederhana)
- "Karyawan masuk 1 Mei, gaji 4 juta, THR Natal 25 Desember berapa?"
- "Buatkan pengumuman THR untuk karyawan."

## Instalasi singkat
Salin folder `hitung-thr` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Hasil uji (jujur)

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (simulasi Claude Code; 4 karyawan: tetap, kontrak, harian lepas, dan yang di-PHK).
- Tanpa skill: bila masa kerja Rina dihitung per bulan kalender, THR-nya kelebihan Rp 400.000 (yang benar 8 bulan penuh = Rp 3.200.000); Joko (harian lepas) hanya "sekitar Rp 3 juta" (yang benar rata-rata 12 bulan = Rp 3.008.333); Wati yang di-PHK 20 Februari 2027 sering dianggap tidak berhak padahal berhak Rp 5.200.000; pajak tidak dihitung.
- Dengan skill: angka-angka di atas cocok dengan hitungan penguji, lengkap dengan batas bayar Rabu, 3 Maret 2027, tambahan PPh 21 per orang, dan pengumuman tanpa nominal pribadi.
- Skor penguji independen: 9 dari 10 (v1.0.1; 4.000 kasus acak dibandingkan dengan kalkulator terpisah, selisih 0). Uji ulang di OpenClaw (1 Okt 2026, hanya dengan skill): 8,5 dari 10.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## Catatan penting
- Alat bantu hitung, **bukan nasihat hukum atau pajak**. Dasar aturan: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026 (SE Menaker THR 2026), serta PP 58/2023 dan PMK 168/2023 (PPh 21 tarif TER); berlaku per 23 September 2026. Untuk hari raya tahun berikutnya, cek SE Menaker THR yang terbit menjelang hari raya.
- Pembulatan PPh 21 belum dicocokkan dengan Coretax (sistem pajak DJP). Bagian PPh 21 DTP (PPh 21 yang ditanggung pemerintah, PMK 105/2025) masih menunggu review konsultan pajak.
- Untuk sengketa atau kasus khusus, hubungi Disnaker setempat, Posko THR (poskothr.kemnaker.go.id), Kring Pajak 1500200, atau konsultan.

## FAQ
**Uang makan dan transport ikut dihitung THR?**
Tidak, bila sifatnya tidak tetap (tergantung kehadiran). Dasar THR adalah gaji pokok ditambah tunjangan tetap. Kalau perusahaan ingin memberi lebih besar, skill akan memakai angka perusahaan.

**Kenapa gaji bulan THR dipotong pajak lebih besar?**
THR digabung dengan gaji di bulan dibayar, sehingga tarif PPh 21 (TER) naik ke baris tabel yang lebih tinggi. Skill menunjukkan berapa tambahan potongannya. Kelebihan/kekurangan akan disesuaikan saat hitung ulang di bulan Desember.

**Tanggal hari raya diambil dari mana?**
Anda yang menyebutkan tanggalnya (sesuai kalender libur nasional resmi). Untuk Idul Fitri/Idul Adha, skill mengecek tanggal itu dengan perkiraan kalender Hijriah dan mengingatkan bila meleset, lalu menghitung batas bayar H-7 secara otomatis.

## Riwayat perubahan

Versi terkini: **1.0.9**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
