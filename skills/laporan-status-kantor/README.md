# Laporan Kantor Rapi, Tinggal Kirim

**Dari chat berantakan jadi laporan siap kirim ke atasan, tim, atau klien — info yang kurang ditandai, bukan dikarang.**

Diuji AI penguji independen di OpenClaw: 6,3 → 9,0 dari 10 (tanpa skill, nominal THR per orang bisa ikut masuk teks pengumuman grup); di bot Telegram asli belum lulus (4,5 → 5 dari 10, lihat bukti uji di bawah).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Ubah catatan chat/poin acak/transkrip voice note jadi laporan 3P (Progres-Rencana-Kendala) yang rapi
- ✅ Satu skill untuk 9 format komunikasi kantor: laporan mingguan, harian, newsletter (buletin internal), pengumuman, FAQ (daftar tanya-jawab karyawan), memo, laporan insiden
- ✅ Format siap tempel langsung ke WA grup kantor/Telegram (`*tebal*`, bullet pendek) atau email formal
- ✅ Dirancang tidak mengarang progres/angka — info yang kurang ditandai jelas atau ditanyakan (tetap baca ulang sebelum dikirim)
- ✅ Nada otomatis menyesuaikan: sopan-formal khas kantor Indonesia atau santai-profesional ala startup

## Cocok untuk siapa
- Pemilik UMKM/usaha kecil-menengah yang minta tim lapor progres mingguan
- Admin/office manager yang bertugas menyusun newsletter atau pengumuman internal
- Team lead yang harus laporan ke atasan/klien tapi tidak sempat menyusun format rapi
- HR yang sering menjawab pertanyaan berulang karyawan (cuti, THR, jam kerja)
- Siapa saja yang WFH/WFO dan diminta laporan harian singkat

## Contoh sebelum & sesudah
**Sebelum:** Poin-poin tim yang berantakan dan campur Indonesia-Inggris — "landing page udah deploy ke production", "ada 2 orang tim resign minggu ini jadi rada kacau workload-nya", "budget server bulan ini over dikit gara2 traffic naik".

**Sesudah (cukup ketik):** "bikinin update mingguan buat tim ya, santai aja gaya startup gitu. terus sekalian versi yang bisa dikirim ke klien kita, PT Maju Bersama, tapi jangan ada info internal yang sensitif." (disertai poin-poinnya)

Cuplikan versi untuk klien (contoh dengan data fiktif; dipotong dari `examples/02-startup-tim-dan-klien.md`; production = sudah tayang untuk pengguna, payment gateway = sistem pembayaran online):
```
Yth. Bapak/Ibu PT Maju Bersama,

Berikut update progres proyek untuk periode 21–25 Sep 2026.

Progres:
- Landing page telah selesai dan sudah tayang di production.
- Dashboard analytics sedang berjalan sesuai rencana, ditargetkan selesai minggu depan.

Rencana selanjutnya:
- Mulai proses testing untuk fitur baru minggu depan.

Catatan:
- Integrasi payment gateway masih menunggu proses dari pihak vendor terkait; kami akan
  menginformasikan estimasi waktu penyelesaian segera setelah ada kepastian dari vendor.
…
```
Di contoh ini, kabar karyawan yang resign dan anggaran server yang membengkak sengaja tidak ikut masuk ke versi klien; versi santai untuk tim dibuat dalam jawaban yang sama. Hasilnya tinggal Anda baca ulang lalu tempel ke WA grup atau email.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan laporan 3P mingguan untuk tim Marketing dari poin-poin ini: ..."
- "Rapikan jadi newsletter kantor bulan ini dari chat grup HR"
- "Buat pengumuman libur Idul Fitri, kantor libur 20-24 Sep"
- "Tolong susun FAQ karyawan dari pertanyaan-pertanyaan ini soal cuti dan THR"
- "Buat laporan insiden: server down 2 jam kemarin, sudah diperbaiki"

Jika info penting kurang (nama tim, periode, penerima), agent akan tanya sekali dalam satu
pesan singkat — bukan bolak-balik tanya jawab.

## Instalasi singkat
Salin folder `laporan-status-kantor` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code (belum diuji langsung) | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## Hasil uji (jujur)

**Hasil uji (angka nyata):** uji di OpenClaw otomatis oleh agen penguji independen, 2 Okt 2026 (v1.0.4, dipasang bersama skill `hitung-thr` v1.0.6), skor 1-10: tanpa skill 6,3 → dengan skill 9,0.
- Tugas: pengumuman libur Natal 2026 untuk grup WA karyawan, lengkap dengan nominal THR. Tanpa skill, AI kadang menghitung THR sendiri (salah Rp 3.333.333 di satu sesi, yang benar Rp 3.000.000 = 9/12 × Rp 4.000.000) dan memuat nominal per orang di teks grup. Dengan skill (dipasang bersama skill Hitung THR, `hitung-thr`, yang menghitung nominal THR): THR benar (total 4 karyawan Rp 13.766.667), nominal per orang hanya di blok khusus pemilik/HR, teks grup aman, dan tanggal masuk yang janggal ditandai.
- Jujur: di bot Telegram asli hasilnya belum lulus (lihat bagian bukti uji di bawah).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, termasuk bot Telegram asli). Claude Code, Codex, dan Cursor memakai format skill yang sama, tetapi belum kami uji langsung.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), 5 Oktober 2026 (v1.0.7).
- Tanpa skill: skor 4,5
- Dengan skill: skor 5
Hasil: belum lulus — Kedua sisi menolak nominal THR per orang di grup dengan benar, tetapi keduanya tidak memberi teks pengumuman; DENGAN malah menanyakan tanggal cuti bersama yang sudah ada di rujukan skill.

## Catatan penting
- Skill ini hanya menyusun teks (draf yang Anda tempel sendiri), **bukan nasihat hukum**. Nominal THR tidak dihitung di sini; gunakan skill Hitung THR (`hitung-thr`; dasar Permenaker 6/2016, THR dibayar paling lambat 7 hari sebelum hari raya).
- Tanggal libur nasional dan cuti bersama 2026 mengikuti SKB 3 Menteri (Surat Keputusan Bersama tiga menteri, Nomor 1497, 2, dan 5 Tahun 2025, ditandatangani 19 September 2025). Cek kembali ke kalender resmi pemerintah bila ada perubahan.

## FAQ
**Apakah skill ini menghitung nominal THR atau gaji?**
Tidak. Skill ini hanya menyusun teks pengumuman/laporan. Untuk menghitung nominal, gunakan
skill `hitung-thr` atau skill hitung terkait, lalu hasilnya bisa dimasukkan ke pengumuman.

**Apakah harus punya akses Slack/Google Drive/email seperti skill sumbernya (buatan
luar negeri)?**
Tidak perlu. Skill ini dirancang untuk bekerja langsung dari bahan yang Anda berikan
(tempel chat, ketik poin-poin, atau tempel transkrip voice note) — tanpa integrasi apa pun.

**Bisa untuk kantor yang santai/startup, bukan cuma yang formal?**
Bisa. Sebut saja "santai" atau "gaya startup" saat minta, atau agent akan mengikuti gaya
bahan mentah yang Anda berikan. Defaultnya sopan-formal karena mayoritas kantor Indonesia
lebih sesuai dengan nada itu, terutama untuk laporan ke atasan/pemilik dan klien.

## Riwayat perubahan

Versi terkini: **1.0.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
