# Loker Rapi Siap Posting, Bebas Syarat Bermasalah

**Sebut posisinya, dapat iklan lowongan lengkap untuk JobStreet, LinkedIn, Glints, Instagram, dan grup WA.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Satu permintaan, tiga versi: lengkap (JobStreet/LinkedIn/Glints), Instagram, dan grup WhatsApp
- ✅ Kualifikasi dipisah "wajib" dan "nilai plus", sehingga pelamar yang cocok tidak mundur
- ✅ Bonus 5–7 pertanyaan screening untuk menyaring pelamar lebih cepat
- ✅ Otomatis mengingatkan jika ada syarat diskriminatif (usia, gender, "good looking") yang dilarang Kemnaker, lengkap dengan kalimat pengganti
- ✅ Tidak mengarang gaji atau benefit yang tidak kamu sebutkan

## Cocok untuk siapa
- Pemilik UMKM, toko, kafe, dan online shop yang rekrut sendiri tanpa tim HR
- Staf HR/admin yang sering memasang loker di banyak kanal sekaligus
- Recruiter yang ingin loker lebih menarik dan aman dari kritik publik

## Contoh sebelum & sesudah
**Sebelum:** "Dicari admin cewek maks 25 th good looking, gaji UMR, minat WA." Sedikit pelamar yang cocok dan berisiko diprotes warganet.

**Sesudah (cukup ketik):** "Buatin loker admin olshop hijab di Bandung, gaji UMR, lamar via WA"
→ Iklan lengkap berisi tugas, kualifikasi wajib dan nilai plus, benefit, dan cara melamar, plus versi IG dan WA, pertanyaan screening, dan catatan tentang syarat yang sebaiknya dihapus.

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.0.3), skor 1-10 dari agen penguji independen: tanpa skill 4,5 → dengan skill 8,5.
- Tugas: loker admin online shop dengan syarat "wanita, maks 25 tahun, belum menikah, berpenampilan menarik", gaji Rp2,5-3 juta di Sidoarjo. Tanpa skill, syarat gender, usia, dan status pernikahan dipasang apa adanya. Dengan skill, syarat itu diganti syarat kemampuan kerja (dasar SE Menaker M/6/HK.04/V/2025), keluar paket JobStreet + Instagram + WhatsApp dengan 6 pertanyaan screening, dan gaji diingatkan untuk dicek terhadap UMK (hasil periksa penguji: UMK Sidoarjo 2026 Rp5.191.541, jauh di atas gaji yang ditulis).
- Jujur: tanpa skill, AI sudah mengenali loker penipuan berbayar dan gaji di bawah UMK. Pembeda utamanya ada di syarat diskriminatif dan paket loker yang lengkap.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan lowongan barista part-time untuk kedai kopi di Jogja"
- "Bikin loker kurir COD di Medan, versi WA grup saja"
- "Cek loker saya ini, ada yang diskriminatif nggak?"

## Instalasi singkat
Salin folder `lowongan-kerja` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 5, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/631/650 — skor 5
- Dengan skill: https://t.me/c/4407409583/632/652 — skor 9
Verdik gelombang: LULUS — DENGAN menghapus keempat syarat diskriminatif (wanita, maks 25 th, belum menikah, berpenampilan menarik) dengan dasar SE Menaker M/6/HK.04/V/2025 + 3 versi (portal/IG/WA) + pertanyaan seleksi + cek UMK; TANPA masih memuat "wanita, usia maks 25" dan menawarkan menambah kembali syarat yang dihapus.

## Catatan penting
- **Bukan nasihat hukum.** Dasar aturan: SE Menaker No. M/6/HK.04/V/2025 (28 Mei 2025) tentang larangan diskriminasi dalam rekrutmen; UU 13/2003 Pasal 88E s.t.d.d. UU 6/2023 dan PP 36/2021 untuk upah minimum; berlaku per 23 September 2026. UMK berbeda per kota dan berubah tiap tahun, jadi cek angka terbaru ke Disnaker/Pemda.
- Untuk sengketa rekrutmen, konsultasikan ke Disnaker atau ahli hukum ketenagakerjaan.

## FAQ
**Kenapa syarat usia saya dihapus?**
Sejak Mei 2025 Kemnaker melarang syarat diskriminatif seperti batas usia dan "berpenampilan menarik" di lowongan, kecuali ada alasan pekerjaan yang nyata. Skill ini tetap memberi kalimat pengganti yang fokus pada kemampuan.

**Apakah angka UMR otomatis diisi?**
Tidak. UMK berbeda per kota dan berubah tiap tahun, jadi kamu yang mengisi angkanya agar tidak salah.

**Bisa dibuat dalam bahasa Inggris untuk LinkedIn?**
Bisa. Minta saja "versi bahasa Inggris".

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
