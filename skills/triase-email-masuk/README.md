# Pilah Inbox, Balas yang Penting Dulu

**Tempel email yang menumpuk, dapatkan urutan kerja, ringkasan, draf balasan siap edit, dan peringatan bila ada yang mirip penipuan.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu email mana yang dibalas dulu.** Tenggat, nominal, klien penting, dan kata "segera" menentukan urutan P1-P3, lengkap dengan alasan pendek.
- ✅ **Ringkasan 1-2 kalimat per email** dan daftar tindakan dengan tenggat, jadi tidak perlu membaca ulang semuanya.
- ✅ **Draf balasan siap edit** yang sopan. Harga, tanggal, dan janji yang belum Anda putuskan ditandai `[isian]`, tidak dikarang.
- ✅ **Peringatan phishing tanpa membuka tautan:** nama pengirim vs alamat sebenarnya, tautan mencurigakan, permintaan OTP/PIN, dan modus "ganti rekening baru".
- ✅ **Aman dan privat:** email tetap di komputer Anda; rekap untuk tim tanpa nama lengkap, alamat, rekening, atau angka rahasia.

## Cocok untuk siapa
- Pemilik usaha yang menerima penawaran, tagihan, dan keluhan lewat email.
- Konsultan/freelancer dengan banyak klien.
- Admin kantor yang mengurus tagihan vendor.
- **Bukan untuk:** meringkas grup WhatsApp (`ringkas-grup-wa`), memilah keluhan marketplace (`triase-keluhan-pelanggan`), atau mengirim/membalas email otomatis dan masuk ke akun email (skill ini tidak melakukannya).

## Contoh sebelum & sesudah
**Sebelum:** 10 email pagi hari. Tagihan Rp7.450.000 jatuh tempo dua hari lagi terbenam di bawah promosi, dan email "rekening kami berganti, mohon transfer ke rekening baru" nyaris dibalas.

**Sesudah (cukup tempel emailnya):** tagihan di urutan teratas, permintaan penawaran Rp18.000.000 berikutnya, dua email dicurigai phishing dengan alasannya, promosi diarsipkan, draf balasan untuk semua yang perlu dijawab. Contoh lengkap: `examples/01-pemilik-usaha-10-email.md`.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.0):** rata-rata nilai 5,5 tanpa skill menjadi 8,0 dengan skill (skala 10). Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Tempel email (pengirim, subjek, isi), lalu tulis misalnya:
- "Ini 10 email pagi ini. Mana yang duluan? Siapkan balasannya."
- "Email ini asli atau penipuan?"
- "Ringkas 6 email klien ini dan buat daftar tindakan minggu ini."

Tidak perlu lengkap. Yang kurang ditandai `[isian]` dan ditanyakan maksimal tiga hal di akhir. Anda yang membaca dan mengirim balasannya; skill ini tidak masuk ke akun email, tidak membuka tautan, dan tidak mengirim apa pun.

## Instalasi singkat
Salin folder `triase-email-masuk` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Python tidak wajib; hanya dipakai bila Anda menyerahkan folder atau CSV berisi banyak email.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 13, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1101/1186 — skor 7,5
- Dengan skill: https://t.me/c/4407409583/1102/1188 — skor 8
Verdik gelombang: BELUM — Tanpa skill sudah menandai email penipuan dan memberi 5 draf (namun menjanjikan ganti rugi tanpa tanya pemilik); dengan skill memakai isian untuk keputusan pemilik dan 3 pertanyaan di akhir, tetapi selisihnya belum mencapai acuan 1,5.

## FAQ
**Apakah skill ini membaca atau membalas email saya sendiri?**
Tidak. Anda yang menempelkan email, dan Anda yang mengirim balasannya. Tidak ada koneksi ke akun email.

**Seberapa yakin deteksi phishingnya?**
Hanya dugaan dari teks. Email penipuan bisa tampak rapi dan email asli bisa tampak aneh, jadi hasilnya selalu "dicurigai" dengan cara verifikasi lewat jalur lain (telepon ke nomor resmi).

**Apakah isi email saya dikirim ke pihak lain?**
Skill ini sendiri tidak mengirim apa pun. Namun email yang Anda tempel diproses oleh model AI di aplikasi agent Anda, jadi ikuti kebijakan privasi aplikasi itu. Samarkan data yang sangat rahasia sebelum menempel.

## Catatan
Bukan nasihat hukum atau keuangan. Karya orisinal Komunitech; merek pihak ketiga hanya disebut sebagai contoh dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
