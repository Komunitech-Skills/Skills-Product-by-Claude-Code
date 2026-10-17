# Hitung THR Karyawan Sesuai Aturan Terbaru

**Sebutkan tanggal hari raya dan data karyawan, langsung dapat rincian THR, potongan pajaknya, batas bayar, dan pengumuman siap kirim.**

Diuji AI penguji independen di OpenClaw: 6,1 → 8,0 dari 10 (versi 1.0.9, 2026-10-14; tanpa skill, THR karyawan baru dihitung dari masa kerja "sampai hari ini" dan nominal tiap orang ditulis di pengumuman grup; dengan skill, masa kerja dihitung sampai hari raya, batas bayar H-7 disebut lengkap dengan tanggalnya, dan teks grup tanpa nominal pribadi).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

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
- Data belum lengkap? Ketik saja, mis. "THR karyawan saya berapa? Dedi 3 juta sudah lama, Lina baru masuk bulan lalu 2,8 juta." AI langsung menghitung dengan asumsi yang disebut jelas, lalu menanyakan paling banyak 3 hal supaya angkanya pasti.

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

**Hasil uji (angka nyata):** uji sebelum/sesudah oleh AI penguji independen di OpenClaw (uji otomatis, versi 1.0.9, 14 Oktober 2026, data fiktif). Pertanyaan yang sama dikirim tanpa dan dengan skill dalam 5 skenario: bengkel dengan 4 karyawan untuk Lebaran 2027 (juga dalam konteks bot Telegram), THR Natal kafe plus pertanyaan pajaknya, tukang harian lepas yang upahnya berubah-ubah plus permintaan "sebut nominal tiap orang di grup", dan data yang belum lengkap. Rata-rata nilai **6,1 tanpa skill → 8,0 dengan skill** (dari 10).
- Tanpa skill: karyawan yang baru masuk dihitung dari masa kerja "sampai hari ini", sehingga THR-nya hanya Rp233.333 (bila untuk Lebaran 2027, seharusnya 5–6 bulan sampai hari raya: Rp1.166.667–Rp1.400.000); pajak THR yang dibayar Desember ditebak dengan tarif bulanan, padahal Desember wajib dihitung ulang setahun; pengumuman grup memuat nama dan nominal tiap orang.
- Dengan skill: semua angka cocok dengan hitungan ulang penguji (total THR 4 karyawan bengkel Rp12.441.666; batas bayar Rabu, 3 Maret 2027 untuk Lebaran dan Jumat, 18 Desember 2026 untuk Natal); pajak THR Desember diarahkan ke hitung ulang setahun; teks grup selalu tanpa nominal pribadi.
- Catatan jujur: nilainya tepat di ambang lulus. Saat data belum lengkap (tanpa tanggal hari raya dan tanggal masuk), AI hanya mengajukan 5 pertanyaan tanpa memberi angka (nilai 6,5); di beberapa balasan masih muncul istilah teknis dan nama usaha karangan di teks grup. Ketiganya diperbaiki di versi 1.0.10 (lihat status di bawah).
- Uji hitungan sebelumnya (versi 1.0.1): 4.000 kasus acak dibandingkan dengan kalkulator terpisah, selisih 0.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia; terakhir versi 1.0.9, 14 Oktober 2026) dan Claude Code (simulasi agen penguji). Versi 1.0.10 berisi perbaikan teks instruksi (data kurang tetap dihitung dulu dengan asumsi yang disebut lalu paling banyak 3 pertanyaan, tanpa istilah teknis di balasan, nama usaha tidak dikarang) ditambah satu opsi bantu perkiraan tanggal Lebaran berikutnya (lulus uji otomatis); versi 1.0.10 diuji ulang 14 Oktober 2026 pada tiga skenario (rata-rata 8,0, tanpa salah angka; istilah teknis hilang, data kurang tetap dihitung dulu), lalu 1.0.11 mengganti sisa teks "kami/Manajemen" di pengumuman menjadi `[isi: nama usaha]` bila nama tidak diberikan (perubahan teks script, belum diuji ulang). Rumus dan angka hitungan tidak berubah. Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## Catatan penting
- Alat bantu hitung, **bukan nasihat hukum atau pajak**. Dasar aturan: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026 (SE Menaker THR 2026), serta PP 58/2023 dan PMK 168/2023 (PPh 21 tarif TER); berlaku per 23 September 2026. Untuk hari raya tahun berikutnya, cek SE Menaker THR yang terbit menjelang hari raya.
- Pembulatan PPh 21 belum dicocokkan dengan Coretax (sistem pajak DJP). Bagian PPh 21 DTP (PPh 21 yang ditanggung pemerintah, PMK 105/2025) masih menunggu review konsultan pajak.
- Untuk sengketa atau kasus khusus, hubungi Disnaker setempat, Posko THR (poskothr.kemnaker.go.id), Kring Pajak 1500200, atau konsultan.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, data fiktif) pada 17 Oktober 2026, versi 1.0.11, dengan pesan yang sama untuk kedua sisi (tanpa skill dan dengan skill): bengkel motor dengan 4 karyawan (karyawan tetap lama dengan tunjangan jabatan dan uang makan harian, kasir yang masuk April 2026, helper yang masuk Agustus 2026, dan karyawan kontrak sejak Januari 2026) minta dihitungkan THR untuk Lebaran 2027, kapan paling lambat dibayar, dan dibuatkan pengumuman untuk grup karyawan. Skor 1–10 dari penilai independen: tanpa skill **7** → dengan skill **8**, selisih **+1**: **belum lulus acuan kami**, karena selisihnya di bawah 1,5 (jawaban tanpa skill sudah kuat).

Dengan skill, THR tiap orang benar (total Rp12.441.666; uang makan harian tidak ikut dihitung; karyawan kontrak 13 bulan mendapat THR penuh), tanggal Lebaran ditandai sebagai perkiraan, batas bayar disebut lengkap dengan harinya (Rabu, 3 Maret 2027), ada info denda 5% bila terlambat, draf pengumuman grup tanpa nominal per orang, dan tawaran menghitung potongan PPh 21 atas THR. Namun jawaban tanpa skill juga sudah menghitung THR tiap orang dengan benar dan menyebut batas 3 Maret 2027, jadi bedanya kecil. Semua angka sudah dihitung ulang terpisah.

Catatan jujur: dengan skill, rekap per orang masih berupa tabel 5 kolom yang tampil sebagai teks bergaris di Telegram dan sulit dibaca di HP; bagian "khusus pemilik, jangan ditempel ke grup" yang memuat nominal per orang justru tampil di grup tempat pertanyaan dikirim; dan satu pertanyaan penutup mengulang soal status pajak (PTKP). Ini satu pesan uji per sisi, bukan uji berulang.

## FAQ
**Uang makan dan transport ikut dihitung THR?**
Tidak, bila sifatnya tidak tetap (tergantung kehadiran). Dasar THR adalah gaji pokok ditambah tunjangan tetap. Kalau perusahaan ingin memberi lebih besar, skill akan memakai angka perusahaan.

**Kenapa gaji bulan THR dipotong pajak lebih besar?**
THR digabung dengan gaji di bulan dibayar, sehingga tarif PPh 21 (TER) naik ke baris tabel yang lebih tinggi. Skill menunjukkan berapa tambahan potongannya. Kelebihan/kekurangan akan disesuaikan saat hitung ulang di bulan Desember.

**Tanggal hari raya diambil dari mana?**
Anda yang menyebutkan tanggalnya (sesuai kalender libur nasional resmi). Bila belum Anda sebutkan, AI menghitung dulu untuk perkiraan Lebaran berikutnya (disebut jelas sebagai asumsi), lalu menanyakan tanggal pastinya. Untuk Idul Fitri/Idul Adha, skill mengecek tanggal itu dengan perkiraan kalender Hijriah dan mengingatkan bila meleset, lalu menghitung batas bayar H-7 secara otomatis.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
