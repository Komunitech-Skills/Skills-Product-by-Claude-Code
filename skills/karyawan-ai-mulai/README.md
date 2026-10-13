# Starter Kit Karyawan AI — Mulai dalam 5 Menit

**Cukup ketik "mulai", AI langsung wawancara singkat lalu kerjakan tugas pertama Anda.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu tahu istilah teknis atau nama-nama skill — cukup jawab 5 pertanyaan singkat.
- ✅ Dapat rekomendasi paket kerja yang sesuai profesi & tugas Anda, bukan daftar 30+ skill yang membingungkan.
- ✅ Langsung lihat **hasil nyata** di menit pertama (bukan sekadar penjelasan).
- ✅ Rencana 7 hari sederhana supaya kebiasaan baru terbentuk, satu langkah per hari.
- ✅ Diingatkan soal privasi sejak awal — cocok untuk yang khawatir data bocor. Skill juga menawarkan memasang "Aturan kerja Komunitech" ke `AGENTS.md` OpenClaw Anda (setelah Anda setujui), supaya aturan aman tetap berlaku di setiap percakapan.

## Cocok untuk siapa
- Pemilik usaha/profesional yang **sudah pakai OpenClaw** tapi belum tahu mulai dari mana.
- Yang merasa "terlalu teknis" atau tidak punya waktu bereksperimen sendiri.
- Yang ingin dipandu, bukan disodori manual panjang.

## Contoh sebelum & sesudah
**Sebelum:** Punya OpenClaw terpasang, tapi bingung mau dipakai untuk apa. Skill Komunitech
menumpuk tanpa tahu mana yang relevan.

**Sesudah (cukup ketik):** "mulai karyawan AI, saya owner toko kopi kecil, tim 4 orang..."
→ Dalam satu percakapan: rekomendasi 3 skill yang pas, dipasang dengan izin Anda, satu tugas
nyata langsung selesai (misalnya 3 caption promo siap posting), dan rencana 7 hari untuk
membiasakan diri.

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.1.8), skor 1-10 dari agen penguji independen: tanpa skill 3 → dengan skill 8,3 (skor tanpa skill dari uji awal; skor dengan skill dari uji ulang setelah perbaikan).
- Tugas: "mulai karyawan AI" untuk pemilik laundry 2 outlet yang butuh rekap omzet, balas chat pelanggan, dan promo lewat Telegram. Tanpa skill, AI sempat mengubah konfigurasi gateway dan membuka auto-reply WhatsApp untuk semua orang. Dengan skill: wawancara singkat, template rekap omzet per outlet, draf balasan mode Copilot (manusia yang mengirim), dan blok aturan kerja aman ditulis ke `AGENTS.md` setelah Anda menjawab "ya".
- Jujur: kadang skill menawarkan skill pendamping yang belum terpasang di komputer Anda.

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent OpenClaw Anda, misalnya:
- "mulai karyawan AI"
- "bantu saya mulai pakai AI di bisnis"
- "setup asisten"

## Instalasi singkat
Salin folder `karyawan-ai-mulai` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** skill ini dibuat untuk OpenClaw dan sudah diuji di sana (uji otomatis oleh agen AI, termasuk bot Telegram asli) serta di Claude Code (simulasi agen penguji). Codex dan Cursor belum kami uji, dan langkah yang menyentuh `AGENTS.md` OpenClaw tidak berlaku di platform lain.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 6, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/674/685 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/675/688 — skor 8,5
Verdik gelombang: LULUS — DENGAN memetakan 3 kebutuhan ke 3 skill nyata (rekap-penjualan-csv, balas-chat-cs mode draf, promo-kalender), langsung mengerjakan tugas pertama dengan data contoh berlabel jelas (angka benar), rencana 7 hari, aturan kerja aman, dan tawaran cek privasi; TANPA ramah dan praktis tetapi hanya saran umum tanpa hasil jadi maupun pagar keamanan.

## FAQ
**Apakah AI langsung memasang skill lain tanpa izin saya?**
Tidak. Setiap pemasangan skill baru selalu ditawarkan dulu dan menunggu jawaban "ya" dari Anda.

**Kalau industri saya tidak ada di daftar, apa yang terjadi?**
Skill akan jujur bilang belum ada paket khusus, lalu menawarkan paket umum yang bisa Anda
koreksi kapan saja.

**Apakah data usaha saya dikirim ke Komunitech?**
Tidak. Semua berjalan di OpenClaw milik Anda sendiri; data tetap di komputer Anda. Skill ini
juga akan menawarkan pengecekan privasi dasar (skill `cek-privasi-openclaw`) di langkah terakhir.

## Riwayat perubahan

Versi terkini: **1.1.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
