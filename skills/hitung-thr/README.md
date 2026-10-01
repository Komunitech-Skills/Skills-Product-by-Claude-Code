# Hitung THR Karyawan Sesuai Aturan Terbaru

**Sebutkan tanggal hari raya dan data karyawan, langsung dapat rincian THR, potongan pajaknya, batas bayar, dan pengumuman siap kirim.**

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

## FAQ
**Uang makan dan transport ikut dihitung THR?**
Tidak, bila sifatnya tidak tetap (tergantung kehadiran). Dasar THR adalah gaji pokok ditambah tunjangan tetap. Kalau perusahaan ingin memberi lebih besar, skill akan memakai angka perusahaan.

**Kenapa gaji bulan THR dipotong pajak lebih besar?**
THR digabung dengan gaji di bulan dibayar, sehingga tarif PPh 21 (TER) naik ke baris tabel yang lebih tinggi. Skill menunjukkan berapa tambahan potongannya. Kelebihan/kekurangan akan disesuaikan saat hitung ulang di bulan Desember.

**Tanggal hari raya diambil dari mana?**
Kamu yang menyebutkan tanggalnya (sesuai kalender libur nasional resmi). Skill lalu menghitung batas bayar H-7 secara otomatis.

## Catatan revisi 1.0.4 (2026-10-01)
- Tahun Hijriah hari raya kini **dihitung** dengan script kecil `scripts/tahun_hijriah.py` (kalender Hijriah tabular; mis. 10 Maret 2027 = 1 Syawal 1448 H), bukan ditebak. Bila tidak dihitung, tahun Hijriah tidak dicantumkan (temuan uji: Lebaran Maret 2027 sempat ditulis 1449 H).
- AI diinstruksikan tidak memakai nama dari contoh (mis. "Budi") di balasan; bila nama karyawan tidak diberikan, dipakai "Karyawan 1, 2, …".
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill. Script `thr.py` tidak berubah (salinannya di gaji-umkm tetap identik); 29 uji otomatis lulus (3 uji baru).
