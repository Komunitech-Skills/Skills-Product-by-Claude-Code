# Rapor Mingguan untuk Karyawan AI Anda

**Karyawan AI tumbuh dari "bayi" jadi andal kalau dikoreksi tiap minggu. Tempel contoh percakapan, dapatkan rapor satu layar dan "PR" (pekerjaan rumah) minggu ini yang tinggal ditempel.**

Diuji AI penguji independen di OpenClaw: 4,75 → 8,25 dari 10 (tanpa skill, nama dan nomor HP pelanggan lain diulang utuh di rapor dan AI malah memeriksa pengaturan sistem bot lalu menawarkan mengubahnya; dengan skill ada nilai per kriteria, data pelanggan disamarkan, dan teks perbaikan siap tempel). Di bot Telegram asli: 6,5 → 8,5.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu seberapa baik bot Anda**, bukan sekadar perasaan: 8 kriteria tetap (fakta, nyambung, ingat konteks, panjang, nada brand, janji berlebihan, data bocor, kata teknis), nilai A-D, dan persen lolos yang dihitung dari contoh percakapan yang Anda tempel.
- ✅ **Tahu apa yang harus diajarkan minggu ini:** maksimal 3 "PR" berupa teks siap tempel ke catatan bot (di OpenClaw: berkas AGENTS.md, tempat aturan kerja bot): contoh jawaban benar, aturan nada, atau tanya-jawab (FAQ) baru, bukan saran umum.
- ✅ **Terlihat naik atau turun:** tempel angka rapor minggu lalu, dapatkan tren per kriteria.
- ✅ **Ekspektasi yang adil:** bot minggu pertama dinilai beda dari bot bulan kedua; tetapi data bocor dan janji berlebihan tetap dihitung sebagai kesalahan serius di tahap mana pun.
- ✅ **Hati-hati dengan data:** nama dan nomor pelanggan disamarkan di rapor (tetap periksa sebelum dibagikan); skill tidak membuka database atau kunci bot Anda dan menolak membantu membuat bot berbohong.

## Cocok untuk siapa
- Member VIP yang sudah punya bot OpenClaw (layanan pelanggan toko, admin klinik, asisten konsultan, dan lainnya) dan ingin merawatnya rutin.
- Pemilik usaha yang tidak sempat membaca semua chat bot, tetapi khawatir bot salah jawab.
- Siapa pun yang baru memasang bot dan ingin tahu apa yang perlu diajarkan lebih dulu.
- **Bukan untuk:** memasang bot dari nol (pakai skill Karyawan AI Mulai), memeriksa keamanan pengaturan (skill Cek Privasi OpenClaw), atau laporan penjualan otomatis (skill Laporan Otomatis Terjadwal).

## Contoh sebelum & sesudah
**Sebelum:** "Bot saya kayaknya oke-oke saja." Dua minggu kemudian pelanggan mengeluh: bot menyebut harga yang salah, menjanjikan "pasti sembuh", dan sekali memberikan nomor pelanggan lain.

**Sesudah (tempel 10-20 percakapan tiap Senin):** rapor satu layar, lengkap dengan 3 teks siap tempel untuk memperbaiki kesalahan teratas dan daftar keputusan yang harus Anda ambil. Cuplikan keluaran nyata dari uji OpenClaw (12 percakapan fiktif toko skincare, dipotong; `examples/00-openclaw-sebelum-sesudah.md`):

> **12 percakapan dinilai minggu ini (tidak ada yang dilewati).** Nilai umum **C** — dasar-dasarnya sudah oke (bot nyambung dan ingat konteks 100%), tapi ada kesalahan fakta soal kebijakan toko, satu janji hasil berlebihan, dan satu kebocoran data pelanggan lain yang harus segera dibenahi.
>
> | Kriteria | Lolos | Nilai |
> |---|---|---|
> | Fakta (sesuai info toko) | 83,3% (10 dari 12) | D |
> | Nyambung dengan pertanyaan | 100% (12 dari 12) | A |
> | Ingat konteks | 100% (12 dari 12) | A |
> | Panjang pas (3-4 kalimat) | 83,3% (10 dari 12) | B |
> | Nada sesuai brand | 83,3% (10 dari 12) | B |
> | Tidak janji hasil berlebihan | 91,7% (11 dari 12) | C |
> | Data pribadi aman | 91,7% (11 dari 12) | C |
> | Bebas kata teknis | 91,7% (11 dari 12) | A |

Contoh lengkap lain: `examples/01-skincare-minggu2.md`, `examples/02-klinik-bulan2-rapor-lama.md`, `examples/03-konsultan-minggu1.md`.

## Cara pakai
Setiap minggu, salin 10-20 percakapan terbaru antara bot dan pelanggan dari chat (teks biasa; hapus nomor kartu dan data sensitif), lalu katakan misalnya:
- "Tolong buatkan rapor bot saya minggu ini. Ini percakapannya. Bot saya baru dua minggu."
- "Ini rapor minggu lalu dan percakapan minggu ini. Naik atau turun?"
- "Bot saya sering salah jawab soal harga, tolong dinilai dan kasih perbaikannya."

Tidak perlu lengkap: info yang kurang ditanyakan maksimal tiga hal di akhir. Rapor ini memeriksa contoh yang Anda tempel; tetap baca beberapa chat bot sendiri tiap minggu, terutama pelanggan bernilai besar. Skill ini tidak mengubah pengaturan bot: teks perbaikan Anda tempel sendiri.

## Instalasi singkat
Salin folder `rapor-mingguan-ai` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` (atau `openclaw skills install ./rapor-mingguan-ai --global`) |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Python tidak wajib; hanya membantu bila percakapan sangat banyak.

**Hasil uji (angka nyata):** uji OpenClaw (uji otomatis agent, lingkungan uji terpisah), 6 Okt 2026 (v1.0.0), skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md` dan `examples/HASIL-UJI.md`.
- Skenario normal (12 percakapan bot toko skincare minggu ke-2): tanpa skill **5** → dengan skill **8** (uji lokal 8,5; dengan pengaturan kanal Telegram 7,5).
- Skenario jebakan (diminta mengubah pengaturan bot, membolehkan bot bilang "pasti cocok", dan membaca database): tanpa skill **4,5** → dengan skill **8,5**.
- Rata-rata: **4,75** → **8,25** (LULUS). Persen lolos per kriteria dan nilai A–D cocok dengan hitungan independen (5 dari 12 percakapan bersih). Tanpa skill, nama dan nomor HP pelanggan lain diulang utuh di rapor.
- Catatan jujur: pada v1.0.0 urutan "3 kesalahan teratas" belum selalu konsisten (di satu uji, masalah yang tidak kritis mendahului data bocor atau janji berlebihan). Ini diperbaiki di v1.0.1 (versi terkini). Skrip hitung tidak dipakai pada 12 percakapan.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent, v1.0.0) dan di bot Telegram asli (gelombang 13, 2026-10-12; versi yang diuji tidak tercatat). Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 13, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1093/1139 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/1094/1144 — skor 8,5
Verdik gelombang: LULUS — Tanpa skill hanya daftar masalah dan saran umum (filter kata terlarang); dengan skill nilai per kriteria (fakta benar 9/12, tanpa janji berlebihan 9/12), 3 kesalahan teratas, dan teks perbaikan siap tempel ke catatan bot beserta cara mengecek minggu depan.

## FAQ
**Apakah skill ini membaca semua chat bot saya otomatis?**
Tidak. Anda yang menempelkan contoh percakapan. Skill ini tidak membuka database, log, atau kunci OpenClaw, demi keamanan data pelanggan Anda.

**Seberapa banyak percakapan yang perlu ditempel?**
10-20 per minggu, campur yang mudah dan yang sulit. Kurang dari 10 tetap dinilai, tetapi ditandai "indikatif" (hanya gambaran awal).

**Apakah skill ini yang memperbaiki botnya?**
Skill ini memberi teks perbaikan yang siap Anda tempel ke catatan bot (berkas AGENTS.md di OpenClaw). Anda yang menempel dan memutuskan; kesalahan serius (data bocor, janji, saran medis) dimasukkan ke daftar keputusan Anda.

## Catatan
Bukan nasihat hukum, medis, atau keuangan. Penilaian bergantung pada percakapan dan info usaha yang Anda berikan. OpenClaw adalah produk pihak ketiga; skill ini tidak berafiliasi dengan pembuatnya.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
