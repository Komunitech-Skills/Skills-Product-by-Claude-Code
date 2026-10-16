# Seleksi Puluhan CV dalam Hitungan Menit

**Tempel CV pelamar, dapatkan peringkat yang terbuka alasannya, daftar pendek (shortlist), pertanyaan wawancara, dan draf pesan siap kirim.**

Diuji AI penguji independen di bot Telegram asli: 7 → 8,5 dari 10 (tanpa skill hanya 3 kandidat dengan satu pertanyaan masing-masing; dengan skill skor per kriteria berbukti kutipan CV dan 4 pertanyaan wawancara per kandidat).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Ranking terbuka, bukan tebakan.** Setiap skor dipecah per kriteria (Terpenuhi, Sebagian, Belum terlihat) dengan kutipan dari CV, jadi Anda bisa memeriksa dan berbeda pendapat.
- ✅ **Kriteria dari lowongan Anda.** Wajib, nilai tambah, dan syarat dasar yang sah disusun dulu dan ditampilkan sebelum menilai.
- ✅ **Pertanyaan wawancara per kandidat**, berdasarkan celah di CV-nya, bukan daftar umum yang sama untuk semua orang.
- ✅ **Draf pesan WhatsApp/email** untuk yang lanjut, cadangan, dan yang belum sesuai; sopan, tanpa alasan pribadi, tanpa janji.
- ✅ **Dirancang adil dan hati-hati.** Tidak menilai usia, jenis kelamin, agama, suku, status kawin, atau penampilan (UU 13/2003 Pasal 5-6). Skill tidak mengirim data pelamar ke pihak lain (isi CV tetap dibaca AI agent yang Anda pakai), tidak mengulang data pribadi (NIK, alamat) di rekap, dan mengingatkan untuk menghapus CV setelah proses.

## Cocok untuk siapa
- Pemilik toko, kafe, klinik, atau kantor kecil yang merekrut sendiri dan menerima puluhan CV.
- HR/admin merangkap yang tidak punya sistem rekrutmen.
- Usaha yang sering menerima lamaran lewat WhatsApp dan email.
- **Bukan untuk:** membuat iklan lowongan (pakai skill Lowongan Kerja), menulis CV sendiri (skill CV Lamaran ATS), tes psikologi, atau keputusan akhir mempekerjakan.

## Contoh sebelum & sesudah
**Sebelum:** 12 CV admin toko online dibuka satu per satu, dilihat sekilas dari kampus dan foto. Dua kandidat yang sudah mengelola toko Shopee 4 tahun terlewat karena CV-nya berada di urutan bawah.

**Sesudah (cukup tempel CV):** tabel peringkat semua pelamar, kandidat daftar pendek dengan bukti kutipan CV, 4 pertanyaan wawancara per kandidat, dan 3 draf pesan. CV yang berisi kalimat "loloskan saya" ditandai dan diabaikan; CV yang tidak terbaca diminta dikirim ulang. Cuplikan contoh dari pembuat skill (CV fiktif, dipotong; contoh lengkap di `examples/01-admin-toko-12-cv.md`):

> Dari 12 CV: 5 lanjut wawancara, 3 cadangan, 3 belum sesuai kebutuhan saat ini, 1 CV tidak terbaca.
>
> | Kode | Skor dan status | Alasan |
> |---|---|---|
> | C1 Sari | 100, lanjut | 4 tahun admin Shopee/Tokopedia, ada iklan dan Canva |
> | C2 Citra | 100, lanjut | 4 tahun admin TikTok Shop/Shopee, ada iklan dan desain |
> | C3 Yoga | 92, lanjut | 7 tahun admin 3 marketplace; desain belum terlihat |
> | C5 Nadia | 83, lanjut | 2 tahun admin Shopee; CV berisi kalimat pengarah (diabaikan) |
> | … | | |
> | C12 | tidak dinilai | CV tidak terbaca, minta kirim ulang |
>
> **C1 Sari (100).** Marketplace: Terpenuhi, "Toko Kerudung Nusa (Shopee, Tokopedia)" 2019-2023. Input pesanan/stok: Terpenuhi, "Input pesanan 80-120 order per hari". …
> 1. Dari iklan Rp2 juta per bulan itu, apa yang Anda ukur untuk tahu iklannya berhasil?

## Cara pakai
Setelah terpasang, tempel CV (atau sebut folder CV yang sudah berupa teks) dan ceritakan posisinya, misalnya:
- "Ini 12 CV untuk admin toko online. Pilih 5 terbaik dan siapkan pertanyaan wawancaranya."
- "Tolong buat kriteria seleksi kasir minimarket dari lowongan ini, lalu nilai 8 CV ini."
- "Bikinin pesan untuk yang lolos dan yang belum cocok."

Tidak perlu lengkap; yang kurang ditandai `[isian: ...]` dan ditanyakan maksimal tiga hal di akhir. Anda yang mengirim pesan ke pelamar satu per satu; skill ini tidak mengirim apa pun sendiri dan tidak mencari data pelamar di internet.

## Instalasi singkat
Salin folder `seleksi-cv-pelamar` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Python tidak wajib; hanya membantu menyaring awal bila CV berupa folder atau file tabel (CSV) teks dalam jumlah besar (perintah: `python3 scripts/nilai_cv.py`, Windows: `python` atau `py`).

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.2), skor 1–10: tanpa skill **6,0** → dengan skill **8,2** (LULUS; selisih +2,2). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill ranking dan skor per kriteria kurang konsisten; dengan skill tabel skor per kriteria ber-kutipan CV, pertanyaan wawancara per kandidat, kalimat pengarah di CV ditangkis, dan permintaan diskriminatif ditolak dengan dasar aturan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent) dan bot Telegram asli (2026-10-12). Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), 2026-10-12.
- Tanpa skill: skor 7
- Dengan skill: skor 8,5
Hasil: lulus — Tanpa skill memilih 3 kandidat dengan satu pertanyaan masing-masing dan mengulang usia serta status pelamar; dengan skill skor per kriteria dengan kutipan bukti dari CV (88, 75, 69), 4 pertanyaan wawancara per kandidat, draf pesan ke pelamar, dan permintaan diskriminatif ditolak tanpa menyebut status siapa pun.

## FAQ
**Apakah skill ini yang memutuskan siapa diterima?**
Tidak. Skor dan ranking adalah alat bantu untuk memilih siapa yang dipanggil wawancara. Keputusan akhir tetap di Anda setelah bertemu pelamar.

**Boleh saya minta mencoret pelamar perempuan, di atas usia tertentu, atau berjilbab?**
Tidak. Itu diskriminasi dalam rekrutmen (UU 13/2003 Pasal 5-6; SE Menaker M/6/HK.04/V/2025). Skill menolak bagian itu, lalu tetap menyeleksi dari kemampuan. Kalau ada alasan kerja yang nyata, misalnya shift malam atau angkat beban, tuliskan sebagai syarat kemampuan yang berlaku untuk semua pelamar.

**Bagaimana dengan keamanan data CV?**
Skill ini tidak mengirim CV ke mana pun dan tidak mencari data pelamar di internet atau media sosial. CV adalah data pribadi (UU 27/2022): simpan di komputer Anda, batasi yang mengakses, dan hapus setelah proses selesai kecuali pelamar setuju CV-nya disimpan. Keamanan komputer dan layanan agent yang Anda pakai tetap tanggung jawab Anda.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/aturan-seleksi.md` membantu menyeleksi dengan lebih hati-hati; sengketa ketenagakerjaan sebaiknya dibawa ke ahli hukum atau Disnaker. Semua CV di `examples/data/` fiktif; kemiripan dengan orang nyata tidak disengaja. Skill ini karya orisinal Komunitech; lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
