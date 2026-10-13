# Uji A/B: skenario 01 tanpa skill vs dengan skill

**Penguji:** agent independen, 2026-09-25. Data: katering fiktif, Meta Ads 6 iklan, hasil = chat WA (lihat `01-meta-wa-minggu-ini-vs-lalu.md`).
**Permintaan sama:** "Ini ekspor Meta Ads minggu ini sama minggu lalu, hasilnya itu chat WA. Tolong buatin laporannya."
A/B dijalankan pada **dua bentuk file**, karena hasilnya bergantung pada bentuk file:
- **File-1 (ekspor apa adanya):** iklan tanpa chat punya sel `Results` kosong.
- **File-0:** sel kosong itu diisi `0`.

## A. TANPA skill (agent umum, tanpa SKILL.md & script)
Simulasi jujur. Penguji menjalankan cara yang biasa dipakai agent umum (membaca CSV dengan Python/pandas atau membacanya langsung) pada file yang sama:
1. Membaca CSV, lalu memilih kolom sendiri. Pandas `sum()` menganggap sel kosong sebagai 0, sehingga **total biaya Rp 4.302.180 benar** di File-1 maupun File-0. Iklan "Retargeting" (Rp 356.900, 0 chat) terlihat jelas di tabel.
2. Kesalahan yang sering muncul (dihitung penguji dari file yang sama):
   - "Rata-rata biaya per chat" dari **rata-rata kolom `Cost per results`** = **Rp 46.615** (benar: Rp 30.297). Perbandingan dengan minggu lalu dengan cara ini: Rp 57.327 → "turun 18,7%" (benar: **naik 1,5%**).
   - "CTR rata-rata" dari rata-rata kolom CTR = 1,24% (benar 1,33% → 1,3%); "CPC rata-rata" Rp 1.533 (benar Rp 1.337).
   - Format angka campur (`4302180`, `$`/`IDR`, titik desimal Inggris), pembulatan tidak konsisten, istilah Inggris (CPA/CPL) tanpa penjelasan.
   - Saran bersifat umum ("perbaiki creative", "uji audience baru") tanpa angka. Kadang ada janji seperti "bisa menurunkan biaya per chat 20–30%".
3. Setiap minggu cara hitung bisa berubah, tergantung kolom mana yang kebetulan dipakai agent.

Contoh output tipikal tanpa skill:
```
Ringkasan Meta Ads 14–20 Sep
Spend: Rp 4.302.180 (naik dari Rp 3.970.000)
Results (WA): 142 | Avg cost per result: Rp 46.615 (turun 18,7%)
CTR rata-rata 1,24%, CPC rata-rata Rp 1.533
Iklan terbaik: Video Testimoni. Iklan terburuk: Foto Produk Nasi Box (Rp 124.687,50/result)
Retargeting Pengunjung IG belum ada hasil.
Rekomendasi: refresh creative, uji audience lookalike baru, naikkan budget iklan terbaik.
```

## B. DENGAN skill
- **File-0:** output lengkap di `01` bagian B. Total Rp 4.302.180; biaya per chat **Rp 30.297 (naik 1,5%)**; CPC Rp 1.337, CPM Rp 17.820, CTR 1,3%; 3 terbaik/3 perlu perhatian; saran berangka ("Retargeting Rp 356.900 tanpa chat", "Foto Produk Rp 124.688, 4,5x rata-rata"); penafian "bukan jaminan hasil". **Semua angka cocok 100%.**
- **File-1 (ekspor apa adanya):** total **Rp 3.945.280 (salah, kurang Rp 356.900)**, biaya "**turun 0,6%**" (benar naik 8,4%), biaya per chat Rp 27.784 "**turun 6,9%**" (benar naik 1,5%). Iklan Retargeting yang menghabiskan Rp 356.900 tanpa chat **hilang** dari laporan dan saran. Yang tersisa hanya peringatan `{'angka tidak terbaca: hasil': 1}`.

## Perbandingan
| Kriteria | Tanpa skill | Dengan skill, File-0 | Dengan skill, File-1 (apa adanya) |
|---|---|---|---|
| Total belanja | ✅ 4.302.180 | ✅ | ❌ 3.945.280 |
| Biaya per chat & arah perubahan | ❌ 46.615 "turun 18,7%" | ✅ 30.297 naik 1,5% | ❌ 27.784 "turun 6,9%" |
| CPC/CPM/CTR dari total | ❌ rata-rata kolom | ✅ | ❌ (baris hilang) |
| Iklan 0 hasil yang makan biaya | ✅ terlihat | ✅ saran no. 1 | ❌ **hilang** |
| Format Rupiah & pembulatan konsisten | ❌ | ✅ | ✅ |
| Saran berangka tanpa janji | ❌ umum / kadang berjanji | ✅ | ✅ (tapi saran utama hilang) |
| Hasil sama tiap minggu (siap dijadwalkan) | ❌ | ✅ | ✅ (tapi konsisten salah) |

**Kesimpulan:** kalau sel hasil berisi `0`, skill **jelas lebih baik** (angka benar, konsisten, saran berangka). Tetapi pada **ekspor apa adanya** yang realistis untuk Meta (sel kosong), skill menghasilkan **angka utama dan arah perbandingan yang salah** dan menyembunyikan iklan terburuk. Pada poin itu agent tanpa skill justru benar. Hasil A/B **belum jelas lebih baik** untuk skenario normal pertama sebagaimana file biasanya diekspor. Sesuai `pedoman kurasi Komunitech` Tahap 6 no. 4, **skor maksimal 6** sampai cacat T1 (sel kosong) diperbaiki dan diuji ulang.
