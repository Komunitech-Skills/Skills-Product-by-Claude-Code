# Riset Saham Cepat, Fakta Rapi Bersumber

**Sebut kode sahamnya, dapatkan rangkuman berita, aksi korporasi, dan rasio laporan keuangan dalam satu catatan netral, lengkap dengan sumber & tanggal.**

> Skill ini alat riset, **bukan penasihat investasi**. Tidak ada rekomendasi beli/jual, target harga, atau sinyal. Keputusan tetap di tangan Anda.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Hemat waktu riset:** berita, keterbukaan informasi, dan jadwal dividen/RUPS/stock split dirangkum jadi satu catatan, setiap fakta ada tautan & tanggalnya
- ✅ **Rasio dihitung, bukan dikira:** pertumbuhan pendapatan & laba, margin bersih, ROE, DER, EPS, nilai buku, PER, PBV, dan imbal dividen dihitung script dari angka laporan keuangan (paham format "Rp1,2 T", "1.234,5 miliar", "(12.000)", dan laporan "dalam jutaan")
- ✅ **Tidak tertipu data lama:** laporan basi, harga lama, laporan interim, ekuitas negatif, dan neraca yang tidak seimbang ditandai jelas
- ✅ **Tahu apa yang harus ditanyakan:** daftar risiko (fakta) dan pertanyaan yang perlu Anda cek sendiri di laporan resmi
- ✅ **Watchlist & level harga pribadi:** jurnal pantauan milik Anda sendiri dan pemberitahuan saat harga melewati level yang **Anda** tetapkan

## Cocok untuk siapa
- Investor ritel pemula yang bingung membaca laporan keuangan dan pengumuman bursa
- Pengusaha/profesional yang punya saham tapi tidak sempat membaca berita setiap hari
- Anggota komunitas investasi yang ingin catatan riset rapi dan bersumber sebelum berdiskusi

## Contoh sebelum & sesudah
**Sebelum:** Buka 6 tab berita, satu PDF laporan keuangan 120 halaman, dan grup Telegram yang ramai "saham ini pasti naik". Hitung PER di kalkulator HP, salah satuan karena laporan "dalam jutaan".

**Sesudah (cukup ketik):** "Riset CNTH, ini angka laporan semester 1-nya, harga 685."
→ Catatan riset: laba turun 10,35% walau pendapatan naik 6,94%, ROE 18,32% (disetahunkan dari 6 bulan, ditandai), DER 0,66x, EPS Rp136,72, PER 5,01x, PBV 0,92x, imbal dividen 3,50%, plus 5 pertanyaan yang perlu dicek (mis. "kenapa laba turun saat pendapatan naik?") dan daftar data yang belum ditemukan. Tanpa kalimat "layak beli" atau "target harga".

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Rangkum berita dan pengumuman terbaru saham ASII sebulan terakhir."
- "Ini laporan keuangan tahunan (saya tempel). Hitung ROE, DER, PER kalau harganya 4.500."
- "Kapan cum date dividen emiten ini, dan berapa imbal dividennya di harga sekarang?"
- "Buat watchlist 5 saham saya, kabari kalau lewat level yang saya tulis."

Kalau AI agent Anda tidak bisa membuka situs bursa/berita (sering diblokir), cukup tempel teks atau kirim PDF laporannya. Skill ini **tidak pernah** memakai akun/aplikasi sekuritas Anda.

## Instalasi singkat
Salin folder `riset-saham-berita` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Tidak perlu API key, akun, atau instalasi tambahan (hitungan memakai Python bawaan; tanpa Python pun tetap bisa dengan hitung manual yang ditandai "belum diverifikasi script").

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.5), skor 1–10: tanpa skill **3,5** → dengan skill **8,75** (LULUS). Contoh jebakan: minta level serok/cut loss + PIN Stockbit — dengan skill menolak auto-beli dan sinyal; rasio fiktif KRPK PER 7,68x, ROE 13,94% (disetahunkan) tanpa target harga. Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`.

**Status uji (jujur):** sudah diuji OpenClaw sebelum/sesudah otomatis (2026-10-01) + muat CLI. Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Bukan nasihat investasi; angka rasio dari laporan yang Anda berikan.

## FAQ
**Kenapa AI-nya tidak mau bilang saham ini bagus dibeli atau tidak?**
Karena rekomendasi investasi adalah wewenang pihak berizin OJK, dan AI bisa salah atau terpengaruh informasi palsu di internet. Skill ini sengaja berhenti di fakta, angka, risiko, dan pertanyaan, supaya keputusan Anda berdasar data, bukan ikut-ikutan.

**Apakah bisa beli/jual otomatis atau terhubung ke aplikasi sekuritas saya?**
Tidak, dan jangan pernah memberikan PIN/password sekuritas ke AI. Level harga di watchlist hanya untuk pemberitahuan; transaksi tetap Anda lakukan sendiri di aplikasi sekuritas resmi.

**Seberapa akurat angkanya?**
Rasio dihitung script dari angka yang tertulis di laporan, dan script menampilkan "angka yang dibaca" supaya Anda bisa mencocokkan. Akurasi tetap tergantung sumbernya: selalu cocokkan dengan laporan resmi di idx.co.id atau situs emiten, terutama bila ada tanda DATA BASI atau HARGA LAMA.

---
_Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
