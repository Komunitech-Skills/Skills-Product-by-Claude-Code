# Pesan Pertama ke Calon Pelanggan, Tak Terkesan Spam

**Punya kontak calon pelanggan baru (dari referral, pameran, Google Maps, IG, atau grup)? Dapatkan pesan pembuka WhatsApp yang personal, jelas asal-usulnya, dan tidak terkesan spam — dalam 3 pilihan panjang, siap kirim.**

Diuji AI penguji independen di OpenClaw: 6,0 → 9,0 dari 10 (dengan skill pesan dicek skrip dan jam kirim dikoreksi, mis. 19.30 WIB = 20.30 WITA di Makassar, tanpa tawaran kirim otomatis).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Wajib menyebut **dari mana kontak didapat** — bukan basa-basi "kenalan yuk", inti dari pesan pertama yang dipercaya, bukan dicurigai penipuan
- ✅ 3 varian sekaligus (singkat/sedang/dengan nilai tambah) sesuai kebutuhan: pemilik usaha sibuk vs penjelasan yang lebih lengkap untuk jualan ke bisnis lain (B2B)
- ✅ **Dicek otomatis oleh script**: panjang pesan, kalimat kepanjangan, huruf kapital berlebihan, kata pemicu spam ("GRATIS!!!", "100% dijamin"), jumlah link, ada/tidaknya opsi keluar sopan, dan jam kirim wajar — bukan sekadar ditulis lalu dikirim tanpa dicek
- ✅ Tautan WhatsApp (`wa.me`) otomatis dibentuk dengan benar, siap klik
- ✅ Sadar hukum: mengingatkan UU PDP (Pelindungan Data Pribadi; asal data kontak yang sah), tanpa mengarang bukti/testimoni, dengan opsi keluar yang sopan (dicek skrip)
- ✅ Tegas beda fungsi dengan skill lain: bukan untuk follow-up susulan, bukan untuk broadcast massal — jadi sulit disalahgunakan untuk spam

## Cocok untuk siapa
- Pemilik UMKM yang baru dapat kontak calon pelanggan dari pameran/bazar, Google Maps, atau rekomendasi teman
- Sales/marketing yang menawarkan ke bisnis lain (B2B) dan mulai pendekatan ke calon klien baru satu per satu
- Freelancer/jasa (desainer, event organizer, vendor) yang mencari klien dari media sosial atau grup komunitas bisnis
- **Bukan untuk:** menindaklanjuti prospek yang sudah dihubungi (pakai `follow-up-prospek`), promo massal ke banyak kontak (pakai `broadcast-wa`), atau mencari daftar calon pelanggan (pakai `riset-calon-pelanggan`)

## Contoh sebelum & sesudah
**Sebelum:** "Halo kak, kenalin aku dari usaha X, mau nawarin produk nih, boleh?" — dikirim ke nomor asing tanpa menjelaskan dari mana nomornya didapat, bisa langsung dicurigai penipuan/spam dan diblokir. Dalam uji OpenClaw, AI tanpa skill hanya membuat satu pesan tanpa opsi keluar sopan, tidak menyinggung beda jam WIB dan WITA, dan malah menawarkan mengirimkannya sendiri ke nomor calon pelanggan.

**Sesudah (cukup ceritakan):** "Saya lihat usaha katering ini di Google Maps, mau nawarin jasa desain kemasan, nomor WA-nya segini"

Cuplikan hasil (dipotong; keluaran asli dari uji simulasi oleh pembuat skill, data fiktif; `examples/uji-pembuat-01-jasa-desain-kemasan.md`):
```
Varian 1 — Singkat
Selamat siang, Pak Andra. Saya Nadia dari Studio Kemas Ceria, dapat nomor Bapak dari
Google Maps saat mencari usaha katering di area Malang. Boleh saya kirim contoh
desain kemasan katering? Boleh diabaikan bila belum relevan, Pak.
…
Jumlah karakter : 230
Sebut asal kontak terdeteksi : Ya
Opsi keluar terdeteksi       : Ya
Jam kirim wajar (08.00-20.00) : Ya

[OK] Tidak ada masalah yang terdeteksi oleh pemeriksaan otomatis ini.
```
Hasil lengkapnya juga memuat varian sedang dan varian dengan nilai tambah, serta tautan WhatsApp siap klik.

## Cara pakai
Setelah terpasang, cukup ceritakan siapa calon pelanggannya dan dari mana kontaknya didapat, misalnya:
- "Dapat kontak ini dari temen pas pameran UMKM, tolong bikinkan pesan perkenalan."
- "Lihat usaha ini di Instagram, mau nawarin jasa saya, bikinin chat pembukanya."
- "Ada rekomendasi klien baru dari rekan bisnis, gimana pesan pembukanya?"

Kalau info belum lengkap, AI akan tanya sekali dalam satu pesan (nama pengirim, nada bahasa, dll). **Satu hal yang wajib disebutkan: dari mana nomor/kontak itu didapat** — tanpa ini, pesan tidak akan dibuat, karena penting untuk kepercayaan dan kepatuhan aturan data pribadi.

## Instalasi singkat
Salin folder `pesan-prospek-wa` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** tiga sumber, skor 1–10 penguji independen.
- **Uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026** (versi sebelum 1.0.7; angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **6,0** → dengan skill **9,0** (lulus). Dengan skill ada 3 draf pesan WhatsApp, asal kontak wajib disebut, zona jam benar, panjang pesan dicek skrip, dan tanpa tawaran kirim massal.
- **Uji ulang v1.0.7 dalam konteks Telegram, 5 Okt 2026** (OpenClaw dengan kanal Telegram, tanpa kirim sungguhan; berkas sama): **8,7** (rata-rata tiga percobaan, ketiganya lulus).
- **Uji di bot Telegram asli, 5 Okt 2026:** satu pesan tanpa dan dengan skill, skor **6** → **8,5** dari 10, lulus acuan kami. Rinciannya ada di bagian "Bukti uji di bot Telegram" di bawah.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji muat CLI) dan Claude Code (simulasi agent). Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli milik Komunitech (grup uji internal) pada 5 Okt 2026; versi skill saat uji tidak tercatat. Satu pesan yang sama dikirim ke bot tanpa skill dan bot dengan skill: minta pesan perkenalan ke calon pelanggan yang nomornya didapat dari Google Maps, dengan rencana kirim pukul 19.30 WIB ke penerima di zona WITA. Tanpa skill **6** → dengan skill **8,5** dari 10 (selisih +2,5): lulus acuan kami.
- Dengan skill: bot langsung memberi 3 draf pesan pertama yang menyebut asal kontak dan memberi opsi berhenti, mengoreksi jam kirim (19.30 WIB sama dengan 20.30 WITA, digeser ke 18.00 WIB), memakai sapaan netral, dan menutup dengan daftar periksa anti-blokir. Panjang tiga draf (268, 366, dan 427 karakter) dihitung ulang dan sesuai batas skill.
- Tanpa skill: bot memberi 2 draf "Selamat malam" tanpa kalimat opsi berhenti yang jelas dan tetap menyarankan kirim pukul 20.30 WITA.
- Catatan jujur: jawaban dengan skill cukup panjang (sekitar 45 baris) untuk satu pesan, sapaannya bercampur "kamu" dan "Bapak", dan draf ketiga memuat klaim "asli … kualitas konsisten dan harga stabil" yang tidak Anda berikan, jadi hapus kalimat itu bila tidak benar.

## FAQ
**Bisa dipakai untuk kirim ke banyak kontak sekaligus?**
Tidak. Skill ini khusus pesan pertama yang dikirim **satu per satu oleh manusia** ke satu calon pelanggan setiap kali. Untuk promo ke banyak kontak sekaligus (dengan persetujuan & opt-out yang diatur ketat), pakai skill `broadcast-wa`.

**Apakah boleh pakai nomor dari database yang saya beli?**
Tidak disarankan dan skill ini akan menolak membantu jika sumbernya jelas database beli/bocoran/scraping berlogin — berisiko melanggar UU PDP dan nomor Anda bisa diblokir WhatsApp. Skill ini hanya untuk kontak dari sumber sah (referral, pameran, listing bisnis publik, media sosial usaha, grup komunitas).

**Kalau prospek tidak membalas, apa langkah selanjutnya?**
Skill ini berhenti di pesan pertama. Untuk menindaklanjuti prospek yang belum membalas dengan jadwal H+1/H+3/H+7/H+14 (1, 3, 7, dan 14 hari setelah pesan pertama), pakai skill `follow-up-prospek`.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.

Skill ini diadaptasi dari struktur marketing skill open-source (MIT, coreyhaines31/marketingskills); teks, contoh Indonesia, script cek pesan, dan aturan anti-spam milik Komunitech. Komunitech tidak berafiliasi dengan pembuat sumber.
