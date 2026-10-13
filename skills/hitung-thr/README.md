# Hitung THR Karyawan Sesuai Aturan Terbaru

**Sebutkan tanggal hari raya dan data karyawan, langsung dapat rincian THR, potongan pajaknya, batas bayar, dan pengumuman siap kirim.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Sesuai Permenaker 6/2016 dan Surat Edaran Menaker THR 2026 — termasuk karyawan baru, kontrak, dan harian lepas
- ✅ Tidak salah di kasus tepi: masa kerja 11 bulan (proporsional) vs 12 bulan (penuh), kurang dari 1 bulan, karyawan PHK menjelang hari raya
- ✅ Menampilkan tambahan potongan PPh 21 di bulan THR dibayar (tabel TER resmi), jadi karyawan tidak kaget
- ✅ Mengingatkan batas bayar H-7 dan denda 5% bila terlambat
- ✅ Draf pengumuman THR siap kirim ke grup WhatsApp/email

## Cocok untuk siapa
- Pemilik usaha/UMKM yang membayar THR Lebaran, Natal, Nyepi, Waisak, atau Imlek
- Admin/HR yang harus menyiapkan daftar THR untuk banyak karyawan
- Karyawan yang ingin mengecek apakah THR-nya sudah sesuai aturan

## Contoh sebelum & sesudah
**Sebelum:** Bingung karyawan yang baru 8 bulan dapat berapa, uang makan ikut dihitung atau tidak, dan kenapa gaji bulan Lebaran dipotong pajak lebih besar.

**Sesudah (cukup ketik):** "Lebaran 10 Maret 2027. Rina kontrak gaji 4,8 juta, masuk 15 Juni 2026, TK/0."
→ Masa kerja 8 bulan → THR 8/12 × Rp 4.800.000 = Rp 3.200.000, tambahan PPh 21 Rp 120.000, batas bayar Rabu, 3 Maret 2027, plus draf pengumuman.

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (simulasi Claude Code; 4 karyawan: tetap, kontrak, harian lepas, dan yang di-PHK).
- Tanpa skill: bila masa kerja Rina dihitung per bulan kalender, THR-nya kelebihan Rp 400.000 (yang benar 8 bulan penuh = Rp 3.200.000); Joko (harian lepas) hanya "sekitar Rp 3 juta" (yang benar rata-rata 12 bulan = Rp 3.008.333); Wati yang di-PHK 20 Februari 2027 sering dianggap tidak berhak padahal berhak Rp 5.200.000; pajak tidak dihitung.
- Dengan skill: semua angka di atas benar, lengkap dengan batas bayar Rabu, 3 Maret 2027, tambahan PPh 21 per orang, dan pengumuman tanpa nominal pribadi.
- Skor penguji independen: 9 dari 10 (v1.0.1; 4.000 kasus acak dibandingkan dengan kalkulator terpisah, selisih 0). Uji ulang di OpenClaw (1 Okt 2026, hanya dengan skill): 8,5 dari 10.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Hitung THR Lebaran untuk karyawan di file karyawan.csv, Lebaran tanggal 10 Maret 2027."
- "Karyawan masuk 1 Mei, gaji 4 juta, THR Natal 25 Desember berapa?"
- "Buatkan pengumuman THR untuk karyawan."

## Instalasi singkat
Salin folder `hitung-thr` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## Catatan penting
- Alat bantu hitung, **bukan nasihat hukum atau pajak**. Dasar aturan: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026 (SE Menaker THR 2026), serta PP 58/2023 dan PMK 168/2023 (PPh 21 tarif TER); berlaku per 23 September 2026. Untuk hari raya tahun berikutnya, cek SE Menaker THR yang terbit menjelang hari raya.
- Pembulatan PPh 21 belum dicocokkan dengan Coretax. Bagian PPh 21 DTP (PMK 105/2025) masih menunggu review konsultan pajak.
- Untuk sengketa atau kasus khusus, hubungi Disnaker setempat, Posko THR (poskothr.kemnaker.go.id), Kring Pajak 1500200, atau konsultan.

## FAQ
**Uang makan dan transport ikut dihitung THR?**
Tidak, bila sifatnya tidak tetap (tergantung kehadiran). Dasar THR adalah gaji pokok ditambah tunjangan tetap. Kalau perusahaan ingin memberi lebih besar, skill akan memakai angka perusahaan.

**Kenapa gaji bulan THR dipotong pajak lebih besar?**
THR digabung dengan gaji di bulan dibayar, sehingga tarif PPh 21 (TER) naik ke baris tabel yang lebih tinggi. Skill menunjukkan berapa tambahan potongannya. Kelebihan/kekurangan akan disesuaikan saat hitung ulang di bulan Desember.

**Tanggal hari raya diambil dari mana?**
Kamu yang menyebutkan tanggalnya (sesuai kalender libur nasional resmi). Untuk Idul Fitri/Idul Adha, skill mengecek tanggal itu dengan perkiraan kalender Hijriah dan mengingatkan bila meleset, lalu menghitung batas bayar H-7 secara otomatis.

## Riwayat perubahan

Versi terkini: **1.0.9**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
