# HASIL UJI — katalog-reseller

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Folder kerja uji:** `/tmp/uji-katalog-reseller/`

## Ringkasan pengujian
| Uji | Hasil |
|---|---|
| Audit keamanan | `hitung_tier.py` hanya library standar. Menulis file hanya ke path `--csv-keluar` yang diminta pengguna. Tidak ada jaringan, subprocess, penghapusan, atau kredensial. Tidak ada prompt injection. ✅ |
| Verifikasi independen | **300 kombinasi acak** (mode diskon & margin, biaya produsen, biaya jual mitra 0–15%, ongkir, maks. diskon konsumen, harga eceran diturunkan script) dihitung ulang dengan python terpisah (pecahan eksak). Harga tiap tier, margin produsen Rp, untung mitra di eceran & di harga minimum, eceran usulan → **cocok 300/300** ✅ |
| Arah pembulatan | Mode diskon: ke **bawah** ke Rp 100 (diskon mitra ≥ janji) ✓. Mode margin: ke **atas** (margin produsen ≥ target) ✓. Eceran usulan: ke atas ke Rp 1.000 ✓. Harga minimum: ke bawah ✓. Contoh di SKILL.md (Rp 75.600 / 66.700 / 57.800; saran 22% → Rp 69.400, untung Rp 10.700) direproduksi persis ✓ |
| Biaya marketplace reseller | Dikurangkan dari harga jual mitra (eceran × f) ✓. Peringatan tipis muncul ✓ |
| Data rusak/tepi | HPP 0, tier tanpa nilai, mode diskon tanpa eceran, config kosong, nama tier kembar → `ERROR` kode 2 ✓. `1.500.000,50` & `Rp 2.000.000` terbaca ✓. Eceran < HPP → PRODUSEN RUGI + ruang harga negatif ✓. Min. beli sama → peringatan ✓ |
| Piramida & denda | S5: bonus rekrut, komisi downline 3 level, biaya daftar, kewajiban stok, denda Rp 1 juta → semua ditolak dengan alternatif sah ✓. Script tidak punya parameter rekrut (by design) ✓ |
| Uji A/B | Skill jelas lebih baik: agent umum salah menyatakan "semua aman" |
| Banding pesaing | Tidak ditemukan pesaing sebanding |

## Skor
| Kriteria | Skor (1–10) | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Jelas; batas dengan harga-jual-marketplace & surat penawaran tegas |
| Kemudahan awam | 8 | Output tabel jelas; mode margin vs diskon perlu dipilih agent |
| Kualitas output | 9 | Tabel internal/eksternal terpisah, S&K 14 butir, pesan rekrut jujur |
| Akurasi (angka/fakta) | 8 | Rumus & pembulatan tepat. Dua asumsi model keliru (ongkir untuk dropshipper; eceran usulan tanpa biaya jual) |
| Penanganan input kurang | 9 | Satu kali bertanya, default contoh diberi label |
| Penanganan di luar cakupan | 10 | Anti-piramida & tanpa denda sangat tegas, dengan dasar hukum dan alternatif |
| Keamanan | 10 | – |

## SKOR AKHIR: **8 / 10 — LULUS**

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Ongkir ke mitra dikurangkan juga dari tier Dropshipper.** `scripts/hitung_tier.py`, `hitung_produk`: `untung = eceran - h - fee - ongkir_mitra` dan `untung_min` berlaku untuk semua tier. Dropshipper tidak menerima kiriman stok, sehingga untungnya tercatat Rp 1.500 terlalu kecil (contoh 01). **Perbaikan:** lewati `ongkir_mitra` untuk tier yang namanya mengandung "drop" (sudah ada deteksi serupa untuk `min_margin_dropship`), atau tambahkan field tier ke-5 `tanpa_ongkir`. Tulis di SKILL.md bagian Opsi.
2. **Harga eceran usulan mengabaikan biaya jual mitra & ongkir.** `hitung_produk`: `eceran = bulat(tertinggi / (1 - tm/100), …)`. Dengan `--biaya-jual-mitra 8`, script mengusulkan eceran yang langsung ditandainya sendiri "MARGIN MITRA TIPIS" (contoh 02: 13,3% < 15%). **Perbaikan:** `eceran = (tertinggi + ongkir_mitra) / (1 - tm/100 - fee_mitra/100)`, lalu bulatkan ke atas. Sesuaikan juga teks catatan ("agar mitra tier itu mendapat ±X% **bersih setelah biaya jual**").

### Ringan
3. `--csv-keluar` (untuk dibagikan ke mitra) memuat kolom "Untung per unit di harga eceran" yang sudah dipotong perkiraan biaya marketplace, tanpa keterangan. Tambahkan judul kolom "(setelah perkiraan potongan X%)" agar mitra tidak salah paham.
4. Default tier 15/25/35% dengan biaya jual 10% hampir selalu membuat dropshipper TIPIS. Pertimbangkan default dropshipper 20% di `TIER_DEFAULT["diskon"]`, atau sebutkan di SKILL.md bahwa default mengasumsikan jualan langsung.
5. Saat pengguna menyarankan diskon tier yang membuat harga dua tier sama setelah pembulatan (mis. dropship 25% & reseller 25%), peringatan hanya muncul untuk "min beli sama". Tambahkan peringatan "harga dua tier sama".

## Verifikasi angka script
**Ya.** `/tmp/uji-katalog-reseller/indep.py` (300 kasus acak) cocok 100%. Angka di contoh 01–03 dicek manual (lihat catatan penguji tiap file).
