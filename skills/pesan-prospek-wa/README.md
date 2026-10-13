# Pesan Pertama ke Calon Pelanggan, Sopan & Tidak Terkesan Spam

**Punya kontak calon pelanggan baru (dari referral, pameran, Google Maps, IG, atau grup)? Dapatkan pesan pembuka WhatsApp yang personal, jelas asal-usulnya, dan aman dari kesan spam — dalam 3 pilihan panjang, siap kirim.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Wajib menyebut **dari mana kontak didapat** — bukan basa-basi "kenalan yuk", inti dari pesan pertama yang dipercaya, bukan dicurigai penipuan
- ✅ 3 varian sekaligus (singkat/sedang/dengan nilai tambah) sesuai kebutuhan: pemilik usaha sibuk vs penjelasan B2B yang lebih lengkap
- ✅ **Dicek otomatis oleh script**: panjang pesan, kalimat kepanjangan, huruf kapital berlebihan, kata pemicu spam ("GRATIS!!!", "100% dijamin"), jumlah link, ada/tidaknya opsi keluar sopan, dan jam kirim wajar — bukan sekadar ditulis lalu dikirim tanpa dicek
- ✅ Tautan `wa.me` otomatis dibentuk dengan encoding yang benar, siap klik
- ✅ Sadar hukum: mengingatkan UU PDP (asal data kontak yang sah), tanpa mengarang bukti/testimoni, selalu ada opsi keluar
- ✅ Tegas beda fungsi dengan skill lain: bukan untuk follow-up susulan, bukan untuk broadcast massal — jadi tidak disalahgunakan untuk spam

## Cocok untuk siapa
- Pemilik UMKM yang baru dapat kontak calon pelanggan dari pameran/bazar, Google Maps, atau rekomendasi teman
- Sales/marketing B2B yang mulai pendekatan ke calon klien baru satu per satu
- Freelancer/jasa (desainer, event organizer, vendor) yang mencari klien dari media sosial atau grup komunitas bisnis
- **Bukan untuk:** menindaklanjuti prospek yang sudah dihubungi (pakai `follow-up-prospek`), promo massal ke banyak kontak (pakai `broadcast-wa`), atau mencari daftar calon pelanggan (pakai `riset-calon-pelanggan`)

## Contoh sebelum & sesudah
**Sebelum:** "Halo kak, kenalin aku dari usaha X, mau nawarin produk nih, boleh?" — dikirim ke nomor asing tanpa menjelaskan dari mana nomornya didapat, sering langsung dicurigai penipuan/spam dan diblokir.

**Sesudah (cukup ceritakan):** "Saya lihat usaha katering ini di Google Maps, mau nawarin jasa desain kemasan, nomor WA-nya segini"
→ 3 varian pesan yang menyebut jelas "dapat nomor dari Google Maps saat mencari usaha katering di area X", satu ajakan ringan, opsi keluar sopan, sudah dicek otomatis (panjang, spam, jam kirim), dan tautan `wa.me` siap klik. Lihat contoh penuh di `examples/uji-pembuat-01-jasa-desain-kemasan.md`.

## Cara pakai
Setelah terpasang, cukup ceritakan siapa calon pelanggannya dan dari mana kontaknya didapat, misalnya:
- "Dapat kontak ini dari temen pas pameran UMKM, tolong bikinkan pesan perkenalan."
- "Lihat usaha ini di Instagram, mau nawarin jasa saya, bikinin chat pembukanya."
- "Ada rekomendasi klien baru dari rekan bisnis, gimana pesan pembukanya?"

Kalau info belum lengkap, AI akan tanya sekali dalam satu pesan (nama pengirim, nada bahasa, dll). **Satu hal yang wajib disebutkan: dari mana nomor/kontak itu didapat** — tanpa ini, pesan tidak akan dibuat, karena penting untuk kepercayaan dan kepatuhan aturan data pribadi.

## Instalasi singkat
Salin folder `pesan-prospek-wa` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), Okt 2026 (v1.0.7), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **9,0** (LULUS; uji ulang pra-cek bot **8,7**). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dengan skill draf WA + email, asal kontak wajib, zona jam benar, cek panjang lewat `cek_pesan.py`, tanpa blast. Uji bot Telegram gelombang 7 (2026-10-05): 6 → 8,5 LULUS tampilan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji muat CLI) dan Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli.

## FAQ
**Bisa dipakai untuk kirim ke banyak kontak sekaligus?**
Tidak. Skill ini khusus pesan pertama yang dikirim **satu per satu oleh manusia** ke satu calon pelanggan setiap kali. Untuk promo ke banyak kontak sekaligus (dengan persetujuan & opt-out yang diatur ketat), pakai skill `broadcast-wa`.

**Apakah boleh pakai nomor dari database yang saya beli?**
Tidak disarankan dan skill ini akan menolak membantu jika sumbernya jelas database beli/bocoran/scraping berlogin — berisiko melanggar UU PDP dan nomor kamu bisa diblokir WhatsApp. Skill ini hanya untuk kontak dari sumber sah (referral, pameran, listing bisnis publik, media sosial usaha, grup komunitas).

**Kalau prospek tidak membalas, apa langkah selanjutnya?**
Skill ini berhenti di pesan pertama. Untuk menindaklanjuti prospek yang belum membalas dengan jadwal H+1/H+3/H+7/H+14, pakai skill `follow-up-prospek`.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.

Skill ini diadaptasi dari struktur marketing skill open-source (MIT, coreyhaines31/marketingskills); teks, contoh Indonesia, script cek pesan, dan aturan anti-spam milik Komunitech. Komunitech tidak berafiliasi dengan pembuat sumber.
