# Rapor Mingguan untuk Karyawan AI Anda

**Karyawan AI tumbuh dari "bayi" jadi andal kalau dikoreksi tiap minggu. Tempel contoh percakapan, dapatkan rapor satu layar dan PR minggu ini yang tinggal ditempel.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu bot Anda sebenarnya bagus atau tidak**, bukan sekadar perasaan: 8 kriteria tetap (fakta, nyambung, ingat konteks, panjang, nada brand, janji berlebihan, data bocor, kata teknis), nilai A-D, dan persen lolos yang dihitung.
- ✅ **Tahu apa yang harus diajarkan minggu ini:** maksimal 3 "PR" berupa teks siap tempel ke AGENTS.md atau catatan bot (contoh jawaban benar, aturan nada, FAQ baru), bukan saran umum.
- ✅ **Terlihat naik atau turun:** tempel angka rapor minggu lalu, dapatkan tren per kriteria.
- ✅ **Ekspektasi yang adil:** bot minggu pertama dinilai beda dari bot bulan kedua; tetapi data bocor dan janji berlebihan tidak pernah dimaafkan.
- ✅ **Aman:** nama dan nomor pelanggan disamarkan di rapor; tidak membuka database atau kunci bot Anda; tidak membantu membuat bot berbohong.

## Cocok untuk siapa
- Member VIP yang sudah punya bot OpenClaw (CS toko, admin klinik, asisten konsultan, dan lainnya) dan ingin merawatnya rutin.
- Pemilik usaha yang tidak sempat membaca semua chat bot, tetapi khawatir bot salah jawab.
- Siapa pun yang baru memasang bot dan ingin tahu apa yang perlu diajarkan lebih dulu.
- **Bukan untuk:** memasang bot dari nol (`karyawan-ai-mulai`), memeriksa keamanan pengaturan (`cek-privasi-openclaw`), atau laporan penjualan otomatis (`laporan-otomatis-terjadwal`).

## Contoh sebelum & sesudah
**Sebelum:** "Bot saya kayaknya oke-oke saja." Dua minggu kemudian pelanggan mengeluh: bot menyebut harga yang salah, menjanjikan "pasti sembuh", dan sekali memberikan nomor pelanggan lain.

**Sesudah (tempel 10-20 percakapan tiap Senin):** rapor satu layar: nilai umum C karena tiga kesalahan serius; kesalahan itu ditemukan di minggu pertama, lengkap dengan 3 teks siap tempel untuk memperbaikinya, dan daftar keputusan yang harus Anda ambil. Contoh lengkap: `examples/01-skincare-minggu2.md`, `examples/02-klinik-bulan2-rapor-lama.md`, `examples/03-konsultan-minggu1.md`.

## Cara pakai
Setiap minggu, salin 10-20 percakapan terbaru antara bot dan pelanggan dari chat (teks biasa; hapus nomor kartu dan data sensitif), lalu katakan misalnya:
- "Tolong buatkan rapor bot saya minggu ini. Ini percakapannya. Bot saya baru dua minggu."
- "Ini rapor minggu lalu dan percakapan minggu ini. Naik atau turun?"
- "Bot saya sering salah jawab soal harga, tolong dinilai dan kasih perbaikannya."

Tidak perlu lengkap: info yang kurang ditanyakan maksimal tiga hal di akhir. Rapor ini memeriksa contoh yang Anda tempel; tetap baca beberapa chat bot sendiri tiap minggu, terutama pelanggan bernilai besar. Skill ini tidak mengubah pengaturan bot: teks perbaikan Anda tempel sendiri.

## Instalasi singkat
Salin folder `rapor-mingguan-ai` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` (atau `openclaw skills install ./rapor-mingguan-ai --global`) |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Python tidak wajib; hanya membantu bila percakapan sangat banyak.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 13, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1093/1139 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/1094/1144 — skor 8,5
Verdik gelombang: LULUS — Tanpa skill hanya daftar masalah dan saran umum (filter kata terlarang); dengan skill nilai per kriteria (fakta benar 9/12, tanpa janji berlebihan 9/12), 3 kesalahan teratas, dan teks perbaikan siap tempel ke catatan bot beserta cara mengecek minggu depan.

## FAQ
**Apakah skill ini membaca semua chat bot saya otomatis?**
Tidak. Anda yang menempelkan contoh percakapan. Skill ini tidak membuka database, log, atau kunci OpenClaw, demi keamanan data pelanggan Anda.

**Seberapa banyak percakapan yang perlu ditempel?**
10-20 per minggu, campur yang mudah dan yang sulit. Kurang dari 10 tetap dinilai, tetapi ditandai "indikatif".

**Apakah skill ini yang memperbaiki botnya?**
Skill ini memberi teks perbaikan yang siap Anda tempel ke AGENTS.md atau catatan bot. Anda yang menempel dan memutuskan; kesalahan serius (data bocor, janji, saran medis) selalu masuk daftar keputusan Anda.

## Catatan
Bukan nasihat hukum, medis, atau keuangan. Penilaian bergantung pada percakapan dan info usaha yang Anda berikan. OpenClaw adalah produk pihak ketiga; skill ini tidak berafiliasi dengan pembuatnya.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
