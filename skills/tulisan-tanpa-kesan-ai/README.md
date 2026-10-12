# Hilangkan Bau AI dari Tulisanmu, Tanpa Jadi Kaku

**Cek atau perbaiki caption, deskripsi produk, pesan WA, email, sampai artikel — pola tulisan
"kedengaran AI" khas Bahasa Indonesia ditandai dan diperbaiki, suara aslimu tetap dijaga.**

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

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 7, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/740/765 — skor 5
- Dengan skill: https://t.me/c/4407409583/741/767 — skor 7,5
Verdik gelombang: BELUM — DENGAN membuang klaim superlatif dan klise tanpa mengarang fakta, sementara harga, ukuran, dan hashtag tetap utuh, tetapi hasilnya masih generik ("cocok menemani momen santai Anda"); TANPA terdengar paling alami tetapi **mengarang 5 fakta produk** (roasting sendiri, digiling saat dikirim, earthy/fruity, kurang asam, stok terbatas).

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
