# Dari Keluhan Jadi Perbaikan Tiap Bulan

**Satukan chat WA, ulasan, komentar, dan survei jadi daftar "perbaiki ini dulu" - lengkap dengan balasan ke pelanggan.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Masukan dari WhatsApp, Shopee/Tokopedia/Google Maps, Instagram/TikTok, dan survei dibaca sekaligus, bukan satu-satu; ekspor Shopee/Tokopedia/TikTok Shop, Google Form, dan chat WA langsung terbaca (kolom yang dipakai selalu disebut, file rusak diberi pesan jelas)
- ✅ Nama, nomor HP, email, alamat, dan nomor pesanan pelanggan disamarkan otomatis sebelum dianalisis
- ✅ Angka dihitung script: isu teratas (rasa, kemasan, harga, pengiriman, layanan, tempat, antrean), sentimen, NPS survei 0-10, dan tren naik/turun tiap bulan
- ✅ Menghitung keluhan pelanggan yang **belum dibalas admin** di chat WA (dan ulasan yang belum dibalas penjual) - sering jadi isu terpenting
- ✅ Rencana perbaikan berurutan (bukti, tindakan, siapa, tenggat, ukuran berhasil), plus draf balasan ke pelanggan dan "Kabar Perbaikan" siap dikirim, supaya pelanggan tahu masukannya didengar

## Cocok untuk siapa
- Pemilik katering, kafe, toko online, salon, klinik, atau jasa yang dapat masukan lewat banyak kanal
- Admin/CS yang perlu bahan rapat evaluasi bulanan
- Pemilik usaha yang ingin rutin memperbaiki produk tanpa menebak-nebak

## Contoh sebelum & sesudah
**Sebelum:** Chat WA, ulasan, dan komentar tercecer. Yang diperbaiki hanya keluhan yang paling terakhir atau paling pedas.
**Sesudah (cukup ketik):** "Ini chat WA pelanggan, ulasan Shopee, dan komentar IG bulan September. Apa yang harus kami benahi dulu?"
→ Laporan: "Pengiriman telat: 9 dari 51 masukan (17,6%), muncul di 4 kanal", "3 laporan rambut/ulat = Segera", backlog dengan ukuran berhasil,
draf balasan, dan kabar perbaikan. Bulan depan: tren menunjukkan perbaikan berhasil atau belum.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.10):** rata-rata nilai 6,9 tanpa skill menjadi 8,6 dengan skill (skala 10). Dari chat WA dan ulasan Shopee sebuah toko kue fiktif (31 masukan), AI tanpa skill menyebut sekitar 10 nama pelanggan di laporan dan salah hitung jumlah chat (16, padahal 13); dengan skill data pelanggan disamarkan dan angka disalin dari script, dengan temuan 88,9% (8 dari 9) keluhan WhatsApp tidak dibalas admin, lengkap dengan draf balasan siap kirim. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Ketik permintaan biasa, misalnya:
- "Olah masukan pelanggan bulan ini, file-nya chat-wa.txt dan ulasan.csv"
- "Buatkan rencana perbaikan dari komentar Instagram ini" (lalu tempel)
- "Tulis kabar perbaikan untuk pelanggan, sudah kami ganti kemasan dan kurir"
Cara ekspor chat WhatsApp: `templates/cara-ekspor-chat-whatsapp.txt`. Tidak perlu akun/API key; script memakai Python standar
(`python3`, di Windows `python` atau `py`). Skill tetap berguna walau script tidak bisa dijalankan (agent menghitung manual dan menandainya).

## Instalasi singkat
Salin folder `iterasi-dari-masukan-pelanggan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Setelah itu mulai sesi baru.

## Isi paket
`SKILL.md` (alur kerja), `scripts/olah_masukan.py` (+ `uji_olah_masukan.py`, `tests/uji_regresi.py`, `tests/uji_regresi_104.py`, `tests/uji_regresi_105.py` s/d `tests/uji_regresi_108.py`), `templates/` (tema untuk katering, fashion, kafe, laundry/jasa; berkas koreksi; backlog, balasan, kabar perbaikan, cara ekspor WA),
`references/` (prioritas, privasi, siklus bulanan), `examples/` (data fiktif katering harian), `ATTRIBUTION.md`.

## FAQ
**Apakah data pelanggan dikirim ke luar?** Script berjalan di komputer Anda tanpa internet. Penyamaran nama/nomor otomatis, tetapi tidak
sempurna; agent membaca ulang kutipan dan Anda tetap perlu menyimpan file mentah dengan aman. Data dibaca oleh AI agent yang Anda pakai,
sesuai kebijakan agent tersebut.
**Beda dengan `analisis-ulasan`?** `analisis-ulasan` fokus ulasan marketplace (bintang + ide konten). Skill ini menyatukan semua kanal
(chat, komentar, survei), membuat rencana perbaikan, balasan, dan siklus bulanan. Keduanya bisa dipakai bersama.
**Bisa mengirim balasan otomatis ke pelanggan?** Tidak. Skill hanya menyiapkan draf; pengiriman oleh manusia (aman dari risiko blokir WhatsApp dan lebih personal).

## Lisensi & atribusi
Diadaptasi dari phuryn/pm-skills (MIT) dan product-on-purpose/pm-skills (Apache-2.0) dengan tambahan besar Komunitech.
Rincian: `ATTRIBUTION.md`, `NOTICE`, dan file lisensi asli. Tidak berafiliasi dengan pembuat sumber.
