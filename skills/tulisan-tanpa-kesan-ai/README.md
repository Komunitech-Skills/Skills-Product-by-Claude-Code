# Hilangkan Bau AI dari Tulisan Anda, Tanpa Kaku

**Cek atau perbaiki caption, deskripsi produk, pesan WA, email, sampai artikel — pola tulisan
"kedengaran AI" khas Bahasa Indonesia ditandai dan diperbaiki, suara asli Anda tetap dijaga.**

*Diuji AI penguji independen di OpenClaw: 5,0 → 8,7 dari 10 (pembeda: AI biasa "memperbaiki" dengan mengarang stok terbatas dan janji kirim hari ini, skill menjaga harga dan fakta persis; di bot Telegram asli unggulnya lebih tipis, 5 → 7,5).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Menandai pola tulisan AI **khas Bahasa Indonesia** ("Di era digital ini", "Mari kita simak",
  "Tidak hanya X tetapi juga Y", "Semoga bermanfaat!") — bukan sekadar daftar kata bahasa Inggris
  yang diterjemahkan asal-asalan
- ✅ Dua mode: **periksa** (tandai pola + kutipan persis, tanpa menulis ulang) atau **perbaiki**
  (tulis ulang langsung, siap tempel)
- ✅ Suara asli Anda dijaga — bukan disulap jadi tulisan formal/kaku ala template korporat
- ✅ Dirancang agar tidak mengarang klaim, angka, atau testimoni baru saat memperbaiki tulisan (tetap baca hasilnya sebelum diposting)
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
**Sebelum:** "Di era digital ini, memilih kopi berkualitas menjadi hal yang sangat penting. Kopi Arabika Gayo kami
tidak hanya nikmat, tetapi juga memberikan pengalaman tak terlupakan di setiap tegukan. Dengan harga hanya Rp85.000
per 250 gram, ini adalah solusi terbaik nomor satu untuk para pecinta kopi! Mari kita nikmati secangkir kebahagiaan
bersama. Yuk order sekarang! Semoga bermanfaat! ☕🔥✨"

**Sesudah (cukup ketik):** "kak tolong perbaiki caption ig ini biar ga keliatan ditulis AI dong" + draf di atas
```
✏️ Tulisan hasil perbaikan:
Kopi Arabika Gayo kami nikmat dan ngasih sensasi beda di setiap tegukan. Harga Rp85.000 per 250 gram, worth it buat kamu pecinta kopi. Yuk order sekarang! ☕

**Yang diubah:**
- Pembuka basa-basi ("Di era digital ini, memilih kopi berkualitas menjadi hal yang sangat penting") → dihapus, langsung ke produk.
- Kontras biner palsu ("tidak hanya nikmat, tetapi juga memberikan pengalaman tak terlupakan") → disederhanakan jadi kalimat langsung ("nikmat dan ngasih sensasi beda di setiap tegukan").
- Klaim superlatif tanpa bukti ("solusi terbaik nomor satu untuk para pecinta kopi") → diganti kalimat netral yang tetap mempertahankan info harga ("worth it buat kamu pecinta kopi"), tanpa klaim ranking yang tidak ada datanya.
…
```
(Cuplikan hasil uji OpenClaw dengan data contoh, dipotong; `examples/00-openclaw-sebelum-sesudah.md`.) Harga dan ukuran
tetap persis, dan tidak ada klaim baru seperti "stok terbatas" yang ditambahkan. Catatan jujur dari penguji: frasa "worth it" dan "sensasi beda" sedikit bernuansa klaim, jadi tetap baca hasilnya sebelum diposting.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Cek caption ini kedengaran AI banget nggak?"
- "Perbaiki draf email ini biar lebih natural"
- "Hilangkan bau AI dari pesan WA ini tapi jangan diubah jadi kaku"

Kalau Anda tidak sebut mode, AI otomatis pilih yang paling masuk akal: kata "cek/audit/apakah AI" →
mode periksa (hanya tandai, tidak menulis ulang); ada draf tanpa instruksi lain → langsung diperbaiki.

## Instalasi singkat
Salin folder `tulisan-tanpa-kesan-ai` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.3), skor 1–10: tanpa skill **5,0** → dengan skill **8,7** (LULUS). Caption kopi Gayo Rp85.000/250 g: DENGAN harga & ukuran persis, skrip pemeriksa pola (`cek_pola.py`) **100/100**, daftar "Yang diubah" enam pola; TANPA skill, AI mengarang stok terbatas/petani langsung/kirim hari ini. Bot Telegram asli, gelombang 7 (2026-10-05): tanpa skill **5** → dengan skill **7,5** (hasilnya masih terasa generik, jadi unggulnya lebih tipis daripada di OpenClaw). Sumber skor OpenClaw: `examples/00-openclaw-sebelum-sesudah.md`; skor Telegram dari uji terpisah di bot asli.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-02; muat CLI) dan bot Telegram asli (gelombang 7). Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Skill kurasi MIT (petergyang/no-ai-slop) — lihat `ATTRIBUTION.md`. Bukan detektor "% AI" seperti GPTZero.

## FAQ
**Apakah ini bisa membuktikan tulisan saya "lolos" pendeteksi AI seperti GPTZero/Turnitin?**
Tidak, dan skill ini sengaja tidak mengklaim itu. AI-detector menebak-nebak dan sering salah. Skill
ini hanya menandai pola tulisan yang bisa Anda baca dan nilai sendiri dari kutipan barisnya — bukan
skor "% AI" yang tidak bisa dipertanggungjawabkan.

**Hasil perbaikannya bakal jadi kaku/formal, kayak surat resmi?**
Tidak — justru sebaliknya itu yang dihindari. Skill ini menjaga suara asli Anda (santai tetap santai,
blak-blakan tetap blak-blakan); yang dihilangkan hanya pola klise/template, bukan kepribadian
tulisan Anda.

**Harus pakai Python?**
Tidak wajib. Kalau Python ada, deteksi pola & skor awal dihitung otomatis lewat script (lebih cepat
untuk draf panjang). Kalau tidak ada, AI agent tetap bisa memeriksa/memperbaiki secara manual memakai
daftar pola yang sama.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
