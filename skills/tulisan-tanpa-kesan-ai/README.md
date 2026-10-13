# Hilangkan Bau AI dari Tulisanmu, Tanpa Jadi Kaku

**Cek atau perbaiki caption, deskripsi produk, pesan WA, email, sampai artikel — pola tulisan
"kedengaran AI" khas Bahasa Indonesia ditandai dan diperbaiki, suara aslimu tetap dijaga.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Menandai pola tulisan AI **khas Bahasa Indonesia** ("Di era digital ini", "Mari kita simak",
  "Tidak hanya X tetapi juga Y", "Semoga bermanfaat!") — bukan sekadar daftar kata bahasa Inggris
  yang diterjemahkan asal-asalan
- ✅ Dua mode: **periksa** (tandai pola + kutipan persis, tanpa menulis ulang) atau **perbaiki**
  (tulis ulang langsung, siap tempel)
- ✅ Suara aslimu tetap terjaga — bukan disulap jadi tulisan formal/kaku ala template korporat
- ✅ Tidak pernah mengarang klaim, angka, atau testimoni baru saat memperbaiki tulisan
- ✅ Paham beda konteks: caption santai boleh emoji wajar, email kantor tetap sopan tanpa jadi kaku,
  deskripsi produk fokus fakta

## Cocok untuk siapa
- Pemilik UMKM/toko online yang draf captionnya "ditulis AI dulu" tapi terasa generik dan mirip
  semua toko lain
- Admin sosial media/tim marketing yang mau memoles draf sebelum posting
- Profesional yang menulis email kerja atau pesan follow-up ke klien lewat WA
- **Bukan untuk:** membuktikan sebuah tulisan "AI atau bukan" secara ilmiah (lihat FAQ), atau
  "melancarkan" nada dokumen legal/kontrak resmi yang memang butuh formal

## Contoh sebelum & sesudah
**Sebelum:** "Di era digital ini, belanja online menjadi kebiasaan banyak orang. Sepatu lari kami
tidak hanya nyaman, tetapi juga stylish. Solusi terbaik nomor satu untuk kamu yang aktif! Yuk simak
detail produk selengkapnya! Semoga bermanfaat! 🔥🔥✨"

**Sesudah (cukup ketik):** "Perbaiki deskripsi produk ini biar nggak kelihatan AI"
→ "Sepatu lari ini pakai bahan breathable yang ringan, cocok dipakai seharian tanpa bikin kaki panas.
Sol karetnya dirancang untuk cengkeraman lebih baik di aspal maupun trotoar basah..." — lengkap dengan
daftar "Yang diubah" per pola. Lihat contoh penuh (termasuk hasil deteksi skor) di
`examples/01-caption-marketplace.md` dan `examples/02-pesan-wa-follow-up.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Cek caption ini kedengaran AI banget nggak?"
- "Perbaiki draf email ini biar lebih natural"
- "Hilangkan bau AI dari pesan WA ini tapi jangan diubah jadi kaku"

Kalau kamu tidak sebut mode, AI otomatis pilih yang paling masuk akal: kata "cek/audit/apakah AI" →
mode periksa (hanya tandai, tidak menulis ulang); ada draf tanpa instruksi lain → langsung diperbaiki.

## Instalasi singkat
Salin folder `tulisan-tanpa-kesan-ai` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.3), skor 1–10: tanpa skill **5,0** → dengan skill **8,7** (LULUS). Caption kopi Gayo Rp85.000/250 g: DENGAN harga & ukuran persis, `cek_pola.py` **100/100**, daftar "Yang diubah" enam pola; TANPA mengarang stok terbatas/petani langsung/kirim hari ini. Bot Telegram gelombang 7 (2026-10-05): tanpa **5** → dengan **7,5** (BELUM promosi — masih generik). Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-02; muat CLI) dan bot Telegram asli (gelombang 7). Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Skill kurasi MIT (petergyang/no-ai-slop) — lihat `ATTRIBUTION.md`. Bukan detektor "% AI" seperti GPTZero.

## FAQ
**Apakah ini bisa membuktikan tulisan saya "lolos" pendeteksi AI seperti GPTZero/Turnitin?**
Tidak, dan skill ini sengaja tidak mengklaim itu. AI-detector menebak-nebak dan sering salah. Skill
ini hanya menandai pola tulisan yang bisa kamu baca dan nilai sendiri dari kutipan barisnya — bukan
skor "% AI" yang tidak bisa dipertanggungjawabkan.

**Hasil perbaikannya bakal jadi kaku/formal, kayak surat resmi?**
Tidak — justru sebaliknya itu yang dihindari. Skill ini menjaga suara aslimu (santai tetap santai,
blak-blakan tetap blak-blakan); yang dihilangkan hanya pola klise/template, bukan kepribadian
tulisanmu.

**Harus pakai Python?**
Tidak wajib. Kalau Python ada, deteksi pola & skor awal dihitung otomatis lewat script (lebih cepat
untuk draf panjang). Kalau tidak ada, AI agent tetap bisa memeriksa/memperbaiki secara manual memakai
daftar pola yang sama.
