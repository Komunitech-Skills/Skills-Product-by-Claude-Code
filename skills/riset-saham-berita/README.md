# Riset Saham Cepat, Fakta Rapi Bersumber

**Sebut kode sahamnya, dapatkan rangkuman berita, aksi korporasi (dividen, stock split atau pemecahan saham, dll.), dan rasio laporan keuangan dalam satu catatan netral, lengkap dengan sumber & tanggal.**

*Diuji AI penguji independen di OpenClaw: 3,5 → 8,75 dari 10 (pembeda: rasio dihitung skrip dan angka yang dibaca ditampilkan untuk dicocokkan, serta permintaan sinyal beli murah dan PIN sekuritas ditolak; memakai data fiktif).*

> Skill ini alat riset, **bukan penasihat investasi**. Tidak ada rekomendasi beli/jual, target harga, atau sinyal, dan tidak ada janji untung atau hasil investasi. Keputusan dan risikonya sepenuhnya di tangan Anda.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Hemat waktu riset:** berita, keterbukaan informasi (pengumuman resmi emiten ke bursa), dan jadwal dividen/RUPS/stock split dirangkum jadi satu catatan; setiap fakta diupayakan disertai tautan & tanggal. Pengambilan berita langsung dari situs bursa/media belum diuji langsung (uji memakai angka laporan yang ditempel).
- ✅ **Rasio dihitung, bukan dikira:** pertumbuhan pendapatan & laba, margin bersih, ROE (laba dibanding modal sendiri), DER (utang dibanding modal sendiri), EPS (laba per lembar saham), nilai buku, PER (harga dibanding laba per saham), PBV (harga dibanding nilai buku), dan imbal dividen dihitung skrip dari angka laporan keuangan (paham format "Rp1,2 T", "1.234,5 miliar", "(12.000)", dan laporan "dalam jutaan")
- ✅ **Data lama diberi tanda:** laporan basi, harga lama, laporan sebagian tahun (interim), ekuitas negatif, dan neraca yang tidak seimbang ditandai
- ✅ **Tahu apa yang harus ditanyakan:** daftar risiko (fakta) dan pertanyaan yang perlu Anda cek sendiri di laporan resmi
- ✅ **Daftar pantauan (watchlist) & level harga pribadi:** jurnal pantauan milik Anda sendiri dan pemberitahuan saat harga melewati level yang **Anda** tetapkan. Hanya pemberitahuan, bukan sinyal beli/jual; jadwal otomatis ke Telegram belum diuji langsung.

## Cocok untuk siapa
- Investor ritel pemula yang bingung membaca laporan keuangan dan pengumuman bursa
- Pengusaha/profesional yang punya saham tapi tidak sempat membaca berita setiap hari
- Anggota komunitas investasi yang ingin catatan riset rapi dan bersumber sebelum berdiskusi

## Contoh sebelum & sesudah
**Sebelum:** Buka 6 tab berita, satu PDF laporan keuangan 120 halaman, dan grup Telegram yang ramai "saham ini pasti naik". Hitung PER di kalkulator HP, salah satuan karena laporan "dalam jutaan".

**Sesudah (cukup ketik):** "Riset CNTH, ini angka laporan semester 1-nya, harga 685. Menurutmu layak beli nggak?"
```
Maaf, saya tidak bisa menilai layak beli atau tidak - itu keputusan Anda dan wewenang penasihat
berizin OJK. Berikut catatan riset netral dari angka yang Anda berikan.

# Catatan Riset: CNTH - PT Contoh Pangan Nusantara Tbk (fiktif)
Disusun: 2026-09-29 | Data terbaru yang dipakai: LK 6M2026 (per 2026-06-30), harga per 2026-09-26

## 1. Ringkasan fakta
- Pendapatan semester 1 2026 Rp4,81 T, naik 6,94% dari Rp4,50 T (Sumber: ditempel pengguna, LK 6M2026).
- Laba bersih Rp361,20 M, turun 10,35% dari Rp402,90 M (Sumber: ditempel pengguna, LK 6M2026).
- DER 0,66x; utang berbunga 0,28x ekuitas (Sumber: hitungan script dari angka pengguna).
- Dividen tahun buku 2025 Rp24 per saham (Sumber: ditempel pengguna; tanggal pembayaran perlu dicek).
…
```
(Contoh dengan data fiktif dari `examples/contoh-pembuat-cnth.md`, dipotong. LK = laporan keuangan, T = triliun, M = miliar.) Catatan lengkapnya juga memuat rasio lain, pertanyaan yang perlu dicek, dan daftar data yang belum ditemukan. Tanpa kalimat "layak beli" atau "target harga".

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Rangkum berita dan pengumuman terbaru saham ASII sebulan terakhir."
- "Ini laporan keuangan tahunan (saya tempel). Hitung ROE, DER, PER kalau harganya 4.500."
- "Kapan cum date dividen emiten ini (batas terakhir membeli agar berhak dividen), dan berapa imbal dividennya di harga sekarang?"
- "Buat daftar pantauan (watchlist) 5 saham saya, kabari kalau lewat level yang saya tulis."

Kalau AI agent Anda tidak bisa membuka situs bursa/berita (sering diblokir), cukup tempel teks atau kirim PDF laporannya. Skill ini tidak memakai akun/aplikasi sekuritas Anda.

## Instalasi singkat
Salin folder `riset-saham-berita` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Tidak perlu API key, akun, atau instalasi tambahan (hitungan memakai Python bawaan; tanpa Python pun tetap bisa dengan hitung manual yang ditandai "belum diverifikasi script").

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.5), skor 1–10: tanpa skill **3,5** → dengan skill **8,75** (LULUS). Contoh jebakan: diminta level beli murah ("serok") dan batas jual rugi ("cut loss") sambil memberi PIN aplikasi sekuritas — dengan skill AI menolak auto-beli dan sinyal; rasio emiten fiktif KRPK PER 7,68x, ROE 13,94% (disetahunkan, yaitu dikonversi ke setahun penuh) tanpa target harga. Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`. Contoh "Sesudah" di atas memakai emiten fiktif lain (CNTH) dari `examples/contoh-pembuat-cnth.md`, bukan dari uji OpenClaw.

**Status uji (jujur):** sudah diuji OpenClaw sebelum/sesudah otomatis (2026-10-01) + muat CLI. Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Pengambilan berita dari situs bursa/media dan jadwal cek level harga ke Telegram belum diuji langsung. Bukan nasihat investasi; angka rasio dari laporan yang Anda berikan.

## FAQ
**Kenapa AI-nya tidak mau bilang saham ini bagus dibeli atau tidak?**
Karena rekomendasi investasi adalah wewenang pihak berizin OJK, dan AI bisa salah atau terpengaruh informasi palsu di internet. Skill ini sengaja berhenti di fakta, angka, risiko, dan pertanyaan, supaya keputusan Anda berdasar data, bukan ikut-ikutan.

**Apakah bisa beli/jual otomatis atau terhubung ke aplikasi sekuritas saya?**
Tidak, dan jangan pernah memberikan PIN/password sekuritas ke AI. Level harga di watchlist hanya untuk pemberitahuan; transaksi tetap Anda lakukan sendiri di aplikasi sekuritas resmi.

**Seberapa akurat angkanya?**
Rasio dihitung script dari angka yang tertulis di laporan, dan script menampilkan "angka yang dibaca" supaya Anda bisa mencocokkan. Akurasi tetap tergantung sumbernya: selalu cocokkan dengan laporan resmi di idx.co.id atau situs emiten, terutama bila ada tanda DATA BASI atau HARGA LAMA.

---
_Bukan nasihat investasi, tanpa janji untung; investasi saham berisiko rugi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
