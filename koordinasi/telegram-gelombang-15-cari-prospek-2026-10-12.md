# Gelombang Telegram 15 — cari-prospek-web (bot pertama) — 2026-10-12

Tugas **C11** (keputusan otomatis no. 40). Penilai: Akun C (Cursor Cloud). Skill **cari-prospek-web** 1.0.2 × TANPA/DENGAN, **2 pesan**, topik **1289–1290** (`topik-g15-cari-prospek.json`). Pesan: `msgs-g15-cari-prospek.json` (Bandung, 15 kafe/katering/toko kue + kontak bisnis). `tools.web.search.provider=duckduckgo` di config bot uji; gateway di-restart setelah `patch-topik.py`. Transkrip: `alat-uji/pilot/jawaban-g15-cari-prospek-tg.txt`.

**Catatan teknis:** sesi DENGAN (1290) ~18 menit (banyak panggilan model + beberapa `browser` gagal); balasan utama utuh 1864 karakter (msg 1299). TANPA selesai ~3 menit, 1403 karakter (msg 1293). Tidak ada `PlatformMessageNotDispatchedError`.

## Skor & verdik

| Skill | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| cari-prospek-web | 7,0 | 8,5 | +1,5 | **LULUS** | DENGAN menempatkan katering nasi box dulu dengan tautan situs/Google Maps per usaha dan catatan nomor bisnis resmi; TANPA sudah 15 nama dari direktori publik tapi tanpa prioritas kemasan dan sumber per baris. |

## Rekomendasi

- Bot asli dengan web_search hidup di VM Cursor **mengonfirmasi** uji lokal 6,7→8,2; **tidak** usul arsip (keputusan 24 tahap 2).
- Cuplikan promosi **layak** dengan catatan waktu jawab DENGAN panjang (~18 menit) — sama seperti temuan uji internal skill.
- **Berikutnya:** uji independen `ubah-draf-ke-dokumen` v1.0.0 (pembuat ≠ penguji) atau C8 `kartu-belajar-anki`.
