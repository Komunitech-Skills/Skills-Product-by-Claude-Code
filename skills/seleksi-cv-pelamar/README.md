# Seleksi Puluhan CV dalam Hitungan Menit

**Tempel CV pelamar, dapatkan ranking yang adil, shortlist beralasan, pertanyaan wawancara, dan draf pesan siap kirim.**

## Manfaat
- ✅ **Ranking terbuka, bukan tebakan.** Setiap skor dipecah per kriteria (Terpenuhi, Sebagian, Belum terlihat) dengan kutipan dari CV, jadi Anda bisa memeriksa dan berbeda pendapat.
- ✅ **Kriteria dari lowongan Anda.** Wajib, nilai tambah, dan syarat dasar yang sah disusun dulu dan ditampilkan sebelum menilai.
- ✅ **Pertanyaan wawancara per kandidat**, berdasarkan celah di CV-nya, bukan daftar umum yang sama untuk semua orang.
- ✅ **Draf pesan WhatsApp/email** untuk yang lanjut, cadangan, dan yang belum sesuai; sopan, tanpa alasan pribadi, tanpa janji.
- ✅ **Adil dan aman.** Tidak menilai usia, jenis kelamin, agama, suku, status kawin, atau penampilan (UU 13/2003 Pasal 5-6). Data pelamar tidak dikirim ke mana pun, tidak diulang di rekap (NIK, alamat), dan diingatkan untuk dihapus setelah proses.

## Cocok untuk siapa
- Pemilik toko, kafe, klinik, atau kantor kecil yang merekrut sendiri dan menerima puluhan CV.
- HR/admin merangkap yang tidak punya sistem rekrutmen.
- Usaha yang sering menerima lamaran lewat WhatsApp dan email.
- **Bukan untuk:** membuat iklan lowongan (pakai `lowongan-kerja`), menulis CV sendiri (`cv-lamaran-ats`), tes psikologi, atau keputusan akhir mempekerjakan.

## Contoh sebelum & sesudah
**Sebelum:** 12 CV admin toko online dibuka satu per satu, dilihat sekilas dari kampus dan foto. Dua kandidat yang sudah mengelola toko Shopee 4 tahun terlewat karena CV-nya berada di urutan bawah.

**Sesudah (cukup tempel CV):** tabel ranking semua pelamar, 5 kandidat shortlist dengan bukti kutipan ("input pesanan 80-120 order per hari"), 4 pertanyaan wawancara per kandidat, dan 3 draf pesan. CV yang berisi kalimat "loloskan saya" ditandai dan diabaikan; CV yang tidak terbaca diminta dikirim ulang. Contoh lengkap: `examples/01-admin-toko-12-cv.md`.

## Cara pakai
Setelah terpasang, tempel CV (atau sebut folder CV yang sudah berupa teks) dan ceritakan posisinya, misalnya:
- "Ini 12 CV untuk admin toko online. Pilih 5 terbaik dan siapkan pertanyaan wawancaranya."
- "Tolong buat kriteria seleksi kasir minimarket dari lowongan ini, lalu nilai 8 CV ini."
- "Bikinin pesan untuk yang lolos dan yang belum cocok."

Tidak perlu lengkap; yang kurang ditandai `[isian: ...]` dan ditanyakan maksimal tiga hal di akhir. Anda yang mengirim pesan ke pelamar satu per satu; skill ini tidak mengirim apa pun sendiri dan tidak mencari data pelamar di internet.

## Instalasi singkat
Salin folder `seleksi-cv-pelamar` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Python tidak wajib; hanya membantu pra-saring bila CV berupa folder atau CSV teks dalam jumlah besar (perintah: `python3 scripts/nilai_cv.py`, Windows: `python` atau `py`).

## FAQ
**Apakah skill ini yang memutuskan siapa diterima?**
Tidak. Skor dan ranking adalah alat bantu untuk memilih siapa yang dipanggil wawancara. Keputusan akhir tetap di Anda setelah bertemu pelamar.

**Boleh saya minta mencoret pelamar perempuan, di atas usia tertentu, atau berjilbab?**
Tidak. Itu diskriminasi dalam rekrutmen (UU 13/2003 Pasal 5-6; SE Menaker M/6/HK.04/V/2025). Skill menolak bagian itu, lalu tetap menyeleksi dari kemampuan. Kalau ada alasan kerja yang nyata, misalnya shift malam atau angkat beban, tuliskan sebagai syarat kemampuan yang berlaku untuk semua pelamar.

**Apakah data CV aman?**
Skill ini tidak mengirim CV ke mana pun dan tidak mencari data pelamar di internet atau media sosial. CV adalah data pribadi (UU 27/2022): simpan di komputer Anda, batasi yang mengakses, dan hapus setelah proses selesai kecuali pelamar setuju CV-nya disimpan. Keamanan komputer dan layanan agent yang Anda pakai tetap tanggung jawab Anda.

## Catatan versi
- **1.0.0 (2026-10-05):** rilis awal.
- **1.0.1 (2026-10-05):** permintaan terlarang (jenis kelamin, status kawin, usia, agama, penampilan, medsos pelamar) selalu ditolak singkat dengan dasar hukum lalu seleksi tetap dikerjakan; tabel skor per kriteria dan rumus tetap wajib ditulis agar skor stabil; draf "belum sesuai" tidak membandingkan kandidat; script: kode C1.. ikut urutan berkas, baris kursus/pelatihan tidak dihitung pengalaman kerja.
- **1.0.2 (2026-10-05):** atribut terlarang (status kawin, usia, agama, dsb.) tidak pernah disebut di keluaran mana pun, termasuk saat menolak; "Belum terlihat" hanya setelah pencarian kata kunci (pra-saring wajib, nilai minimal Sebagian bila kata kunci ada); tabel skor per kriteria untuk semua kandidat; label "terbaik" hanya untuk shortlist, cadangan ditulis "cadangan"; pertanyaan jeda kerja hanya bila 6 bulan atau lebih; script: baris judul kursus/bootcamp/sertifikasi di bawah rentang tahun tidak dihitung pengalaman kerja.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/aturan-seleksi.md` membantu menyeleksi dengan aman; sengketa ketenagakerjaan sebaiknya dibawa ke ahli hukum atau Disnaker. Semua CV di `examples/data/` fiktif; kemiripan dengan orang nyata tidak disengaja. Skill ini karya orisinal Komunitech; lihat `ATTRIBUTION.md`.
