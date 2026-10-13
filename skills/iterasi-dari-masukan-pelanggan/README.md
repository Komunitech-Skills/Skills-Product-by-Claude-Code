# Dari Keluhan Jadi Perbaikan Tiap Bulan

**Satukan chat WA, ulasan, komentar, dan survei jadi daftar "perbaiki ini dulu" - lengkap dengan balasan ke pelanggan.**

Diuji AI penguji independen di OpenClaw: 6,9 → 8,6 dari 10 (pembedanya data pelanggan disamarkan dan angka disalin dari skrip, dengan temuan 88,9% keluhan WhatsApp tidak dibalas admin; tanpa skill, AI menyebut sekitar 10 nama pelanggan dan salah hitung jumlah chat).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Masukan dari WhatsApp, Shopee/Tokopedia/Google Maps, Instagram/TikTok, dan survei dibaca sekaligus, bukan satu-satu; ekspor (file unduhan) Shopee/Tokopedia/TikTok Shop, Google Form, dan chat WA langsung terbaca (kolom yang dipakai disebutkan, file rusak diberi pesan jelas)
- ✅ Nama, nomor HP, email, alamat, dan nomor pesanan pelanggan disamarkan otomatis sebelum dianalisis (penyamaran otomatis belum sempurna, lihat FAQ)
- ✅ Angka dihitung script: isu teratas (rasa, kemasan, harga, pengiriman, layanan, tempat, antrean), sentimen (nada positif/netral/negatif), NPS (seberapa besar pelanggan mau merekomendasikan Anda, dari survei 0-10), dan tren naik/turun tiap bulan
- ✅ Menghitung keluhan pelanggan yang **belum dibalas admin** di chat WA (dan ulasan yang belum dibalas penjual) - sering jadi isu terpenting
- ✅ Rencana perbaikan berurutan (bukti, tindakan, siapa, tenggat, ukuran berhasil), plus draf balasan ke pelanggan dan "Kabar Perbaikan" (kabar ke pelanggan bahwa masukannya ditindaklanjuti) siap dikirim, supaya pelanggan tahu masukannya didengar

## Cocok untuk siapa
- Pemilik katering, kafe, toko online, salon, klinik, atau jasa yang dapat masukan lewat banyak kanal
- Admin/CS yang perlu bahan rapat evaluasi bulanan
- Pemilik usaha yang ingin rutin memperbaiki produk tanpa menebak-nebak

## Contoh sebelum & sesudah
**Sebelum:** Chat WA, ulasan, dan komentar tercecer. Yang diperbaiki hanya keluhan yang paling terakhir atau paling pedas.

**Sesudah (cukup ketik):** "kak saya punya toko kue online Kue Nara. ini chat WA pelanggan (chat-wa-september.txt) sama ulasan shopee bulan september (ulasan-shopee-september.csv). tolong dibaca semua ya, apa yg harus saya benahi duluan? yg chat dari 'Admin Kue Nara' itu admin saya"

Cuplikan balasan (dipotong; data fiktif; dari `examples/00-openclaw-sebelum-sesudah.md`):
```
Rencana Perbaikan — Kue Nara (September 2026, 31 masukan)
2. 88,9% keluhan di WhatsApp sama sekali tidak dibalas admin (8 dari 9), dan cuma 2 dari 13 chat dibalas ≤24 jam. …
| # | Tema | Keluhan (%) | Pujian | Dampak | Skor | Kanal | Prioritas |
|---|---|---|---|---|---|---|---|
| 1 | Keamanan produk (jamur, benda asing) | 5 (16,1%) | 0 | 5 | 25 | Shopee, WA | Segera |
| 2 | Rasa / tekstur | 5 (16,1%) | 8 | 4 | 20 | Shopee, WA | Segera |
| 3 | Kemasan / packing | 4 (12,9%) | 1 | 3 | 12 | Shopee, WA | Bulan ini |
| 4 | Pengiriman / ketepatan waktu | 4 (12,9%) | 2 | 3 | 12 | Shopee, WA | Bulan ini |
…
Data 31 masukan tergolong sedikit (ambang skill 30) — persentase di bawah ini arah, bukan angka pasti.
```
Hasil lengkapnya juga memuat bukti kutipan per isu, rencana perbaikan berurutan, draf balasan, dan kabar perbaikan; bulan depan ditambah tren.

## Cara pakai
Ketik permintaan biasa, misalnya:
- "Olah masukan pelanggan bulan ini, file-nya chat-wa.txt dan ulasan.csv"
- "Buatkan rencana perbaikan dari komentar Instagram ini" (lalu tempel)
- "Tulis kabar perbaikan untuk pelanggan, sudah kami ganti kemasan dan kurir"
Cara mengunduh (ekspor) chat WhatsApp: lihat `templates/cara-ekspor-chat-whatsapp.txt`. Tidak perlu akun atau kunci akses (API key).

## Instalasi singkat
Salin folder `iterasi-dari-masukan-pelanggan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Setelah itu mulai sesi baru.

Skrip hitung memakai Python standar (`python3`, di Windows `python` atau `py`). Skill tetap berguna walau skrip tidak bisa dijalankan (agent menghitung manual dan menandainya).

**Hasil uji (angka nyata):** satu sumber, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.10** (angka dari `examples/00-openclaw-sebelum-sesudah.md`; versi terkini di katalog 1.0.11): rata-rata nilai 6,9 tanpa skill menjadi 8,6 dengan skill. Dari chat WA dan ulasan Shopee sebuah toko kue fiktif (31 masukan), AI tanpa skill menyebut sekitar 10 nama pelanggan di laporan dan salah hitung jumlah chat (16, padahal 13); dengan skill data pelanggan disamarkan dan angka disalin dari script, dengan temuan 88,9% (8 dari 9) keluhan WhatsApp tidak dibalas admin, lengkap dengan draf balasan siap kirim. Catatan jujur dari berkas uji: masih ada selip kecil pada label (kalimat ringkasan bisa terbaca "5 jamur" padahal 4 jamur dan 1 semut), bukan salah hitung.

**Status uji (jujur):** baru diuji di OpenClaw (uji otomatis agent); Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah data pelanggan dikirim ke luar?** Script berjalan di komputer Anda tanpa internet. Penyamaran nama/nomor otomatis, tetapi tidak
sempurna; agent membaca ulang kutipan dan Anda tetap perlu menyimpan file mentah dengan aman. Data dibaca oleh AI agent yang Anda pakai,
sesuai kebijakan agent tersebut.

**Beda dengan skill Analisis Ulasan (`analisis-ulasan`)?** Skill itu fokus ulasan marketplace (bintang + ide konten). Skill ini menyatukan semua kanal
(chat, komentar, survei), membuat rencana perbaikan, balasan, dan siklus bulanan. Keduanya bisa dipakai bersama.

**Bisa mengirim balasan otomatis ke pelanggan?** Tidak. Skill hanya menyiapkan draf; pengiriman oleh manusia (menurunkan risiko nomor WhatsApp diblokir, dan lebih personal).

## Isi paket (teknis)
`SKILL.md` (alur kerja), `scripts/olah_masukan.py` (+ `uji_olah_masukan.py`, `tests/uji_regresi.py`, `tests/uji_regresi_104.py`, `tests/uji_regresi_105.py` s/d `tests/uji_regresi_108.py`), `templates/` (tema untuk katering, fashion, kafe, laundry/jasa; berkas koreksi; backlog, balasan, kabar perbaikan, cara ekspor WA),
`references/` (prioritas, privasi, siklus bulanan), `examples/` (data fiktif katering harian), `ATTRIBUTION.md`.

## Lisensi & atribusi
Diadaptasi dari phuryn/pm-skills (MIT) dan product-on-purpose/pm-skills (Apache-2.0) dengan tambahan besar Komunitech.
Rincian: `ATTRIBUTION.md`, `NOTICE`, dan file lisensi asli. Tidak berafiliasi dengan pembuat sumber.
