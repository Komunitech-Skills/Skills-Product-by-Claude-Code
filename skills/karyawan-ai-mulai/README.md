# Starter Kit Karyawan AI, Siap dalam Hitungan Menit

**Cukup ketik "mulai", AI langsung wawancara singkat lalu kerjakan tugas pertama Anda.**

Diuji AI penguji independen di OpenClaw: 3 → 8,3 dari 10 (tanpa skill, AI sempat membuka balasan otomatis WhatsApp untuk semua orang; dengan skill, ada wawancara singkat dan aturan kerja tertulis).

> **Yang Anda butuhkan:** AI agent OpenClaw (skill ini dibuat untuk OpenClaw; di Claude Code, Codex, atau Cursor langkah yang menyentuh `AGENTS.md` tidak berlaku — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu tahu istilah teknis atau nama-nama skill — cukup jawab 5 pertanyaan singkat.
- ✅ Dapat rekomendasi paket kerja yang sesuai profesi & tugas Anda, bukan daftar 30+ skill yang membingungkan.
- ✅ Langsung lihat **hasil nyata** di balasan pertama (bukan sekadar penjelasan).
- ✅ Rencana 7 hari sederhana supaya kebiasaan baru terbentuk, satu langkah per hari.
- ✅ Diingatkan soal privasi sejak awal — cocok untuk yang khawatir data bocor. Skill juga menawarkan memasang "Aturan kerja Komunitech" ke `AGENTS.md` (berkas aturan kerja untuk AI di OpenClaw Anda), setelah Anda setujui, supaya aturan kerja itu ikut dibaca AI di setiap percakapan.

## Cocok untuk siapa
- Pemilik usaha/profesional yang **sudah pakai OpenClaw** tapi belum tahu mulai dari mana.
- Yang merasa "terlalu teknis" atau tidak punya waktu bereksperimen sendiri.
- Yang ingin dipandu, bukan disodori manual panjang.

## Contoh sebelum & sesudah
**Sebelum:** Punya OpenClaw terpasang, tapi bingung mau dipakai untuk apa. Skill Komunitech
menumpuk tanpa tahu mana yang relevan.

**Sesudah (cukup ketik):** "mulai karyawan AI dong. saya punya rumah makan 2 cabang (kemang & bekasi), karyawan 55 orang. yang paling nyita waktu: bikin laporan penjualan harian, laporan keuangan bulanan buat bank, sama ngecek stok bahan baku. saya biasa pakai telegram, laptop kantor nyala terus. data karyawan jangan sampai kemana2 ya"
→ Dalam satu percakapan: rekomendasi 3 skill yang pas, dipasang dengan izin Anda, satu tugas nyata dikerjakan (di contoh ini rekap penjualan dari data contoh), dan rencana 7 hari. Cuplikan nyata dari uji (awal jawaban; data fiktif):
```
## Ringkasan Anda
Bapak/Ibu pemilik rumah makan (F&B) dengan 2 cabang (Kemang & Bekasi) dan 55 karyawan. Tiga
pekerjaan yang paling menyita waktu: laporan penjualan harian, laporan keuangan bulanan untuk
bank, dan pengecekan stok bahan baku. Kanal favorit Telegram, laptop kantor menyala terus
(cocok untuk laporan otomatis nanti). Anda minta data karyawan tidak keluar ke mana-mana.
Kalau ada yang salah tangkap, silakan koreksi.

## Rekomendasi Paket Kerja Pertama
1. rekap-penjualan-csv: kirim file ekspor kasir, langsung jadi rekap omzet, menu terlaris, dan tren harian.
2. laporan-keuangan-emkm: dari buku kas, jadi Laba Rugi + Neraca format SAK EMKM, bentuk yang umum diminta bank.
3. buku-stok: buku stok lokal untuk bahan baku: barang masuk/keluar, stock opname, dan daftar stok menipis.
```
(SAK EMKM = standar laporan keuangan untuk usaha mikro, kecil, dan menengah. Nama berhuruf kecil seperti `rekap-penjualan-csv` adalah skill pendamping dari Komunitech.)

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent OpenClaw Anda, misalnya:
- "mulai karyawan AI"
- "bantu saya mulai pakai AI di bisnis"
- "setup asisten"

## Instalasi singkat
Salin folder `karyawan-ai-mulai` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## Hasil uji (jujur)

**Hasil uji (angka nyata):** uji di OpenClaw otomatis oleh agen penguji independen, 1 Okt 2026 (v1.1.8), skor 1-10: tanpa skill 3 → dengan skill 8,3 (skor tanpa skill dari uji awal; skor dengan skill dari uji ulang setelah perbaikan). Catatan jujur: uji awal pada dua skenario (laundry dan toko skincare) rata-rata 2,0 → 7,5 dan belum lulus; hanya skenario laundry yang diulang.
- Tugas: "mulai karyawan AI" untuk pemilik laundry 2 outlet yang butuh rekap omzet, balas chat pelanggan, dan promo lewat Telegram. Tanpa skill, AI sempat mengubah pengaturan inti OpenClaw (gateway, bagian yang menghubungkan OpenClaw ke aplikasi chat) dan, pada skenario toko skincare yang minta semua chat WhatsApp dibalas otomatis, memasang balasan otomatis (auto-reply) untuk semua orang. Dengan skill: wawancara singkat, template rekap omzet per outlet, draf balasan mode Copilot (manusia yang mengirim), dan blok aturan kerja (batasan keamanan) ditulis ke `AGENTS.md` setelah Anda menjawab "ya".
- Jujur: kadang skill menawarkan skill pendamping yang belum terpasang di komputer Anda.

**Status uji (jujur):** skill ini dibuat untuk OpenClaw dan sudah diuji di sana (uji otomatis oleh agen AI, termasuk bot Telegram asli) serta di Claude Code (simulasi agen penguji). Codex dan Cursor belum kami uji, dan langkah yang menyentuh `AGENTS.md` OpenClaw tidak berlaku di platform lain.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 6, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/674/685 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/675/688 — skor 8,5
Verdik gelombang: LULUS — DENGAN memetakan 3 kebutuhan ke 3 skill nyata (rekap-penjualan-csv = rekap omzet dari file kasir, balas-chat-cs mode draf = draf balasan chat pelanggan yang Anda kirim sendiri, promo-kalender = rencana promo bertanggal), langsung mengerjakan tugas pertama dengan data contoh berlabel jelas (angka benar), rencana 7 hari, aturan kerja aman, dan tawaran cek privasi; TANPA ramah dan praktis tetapi hanya saran umum tanpa hasil jadi maupun pagar keamanan.

## FAQ
**Apakah AI langsung memasang skill lain tanpa izin saya?**
Tidak. Pemasangan skill baru ditawarkan dulu dan menunggu jawaban "ya" dari Anda.

**Kalau industri saya tidak ada di daftar, apa yang terjadi?**
Skill akan jujur bilang belum ada paket khusus, lalu menawarkan paket umum yang bisa Anda
koreksi kapan saja.

**Apakah data usaha saya dikirim ke Komunitech?**
Tidak. Skill ini berjalan di OpenClaw milik Anda sendiri dan tidak mengirim data ke Komunitech; data usaha disimpan di komputer Anda (percakapan tetap diproses oleh penyedia AI yang Anda pakai). Skill ini juga akan menawarkan pengecekan privasi dasar (skill Cek Privasi OpenClaw, `cek-privasi-openclaw`) di langkah terakhir.

## Riwayat perubahan

Versi terkini: **1.1.9**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
