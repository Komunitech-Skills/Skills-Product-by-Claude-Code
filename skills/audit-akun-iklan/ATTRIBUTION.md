# Atribusi

Skill ini adalah karya **kurasi (ATM)** Komunitech (komunitech.com) yang diadaptasi dari:

- **claude-ads** oleh agricidaniel — https://github.com/AgriciDaniel/claude-ads
  Lisensi: **MIT** (teks lengkap di `LICENSE-MIT`, Copyright (c) 2026 agricidaniel).
  Versi yang dibaca: commit `ac21644933910419529bcf81efb95a9ca71edf81` (2026-09-11).

## Yang diambil dari sumber (lalu diubah)
- Metode skor: status `pass/fail/unknown/not_applicable`, bobot keparahan (critical 5 / high 3 /
  medium 1), skor kategori = bobot lulus ÷ bobot diketahui, bobot kategori dinormalkan ulang,
  cakupan bukti dengan ambang 80% / 60%, dan skor gabungan berbobot porsi belanja
  (sumber: `ads/references/scoring-system.md`).
- Gagasan tema cek (nama cek, bukan kriteria): pixel/CAPI, event, struktur & fase belajar, audiens
  pengecualian, frekuensi, kelelahan materi, jaringan/kata kunci negatif Google, dll.
  (sumber: `ads/references/meta-audit.md`, `tiktok-audit.md`, `google-audit.md`).

## Yang ditulis baru oleh Komunitech
- Seluruh kriteria lulus/gagal, bukti yang bisa diberikan orang awam, dan langkah perbaikan
  (sumber hanya memuat nama cek tanpa kriteria).
- Cek Shopee Ads dan iklan TikTok Shop/Tokopedia (tidak ada di sumber), ROAS/ROI impas.
- Status `sebagian`, label skor bahasa awam, bobot kategori versi Komunitech, prioritas dampak ×
  kemudahan, kenaikan skor per perbaikan, rencana 7 hari, contoh kasus Indonesia, dan script
  `scripts/skor_audit.py` (Python standar, Decimal) beserta tesnya. Tidak ada kode sumber yang disalin.

File di skill ini **telah diubah** dari sumber aslinya. Komunitech tidak berafiliasi dengan
pembuat claude-ads, Meta, TikTok, Google, Shopee, maupun Tokopedia; nama platform disebut hanya
sebagai penyebut produk.

Penggunaan paket tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian; bagian yang
berasal dari claude-ads tetap tunduk pada `LICENSE-MIT`.
