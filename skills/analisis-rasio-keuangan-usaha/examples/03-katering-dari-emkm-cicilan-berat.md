# Contoh 03 — Katering, lanjutan dari laporan-keuangan-emkm (JSON), rencana cicilan terlalu berat

> Contoh dari pembuat skill (2026-09-26). Laporan dibuat dulu dengan `skills/laporan-keuangan-emkm/scripts/laporan_emkm.py ... --format json` dari buku kas 3 bulan (termasuk pencairan KUR Rp 10 jt dan pembelian kompor/freezer), lalu dianalisis.

**Perintah:**
```bash
python3 laporan_emkm.py katering.csv --nama-usaha "Katering Bu Rina" --persediaan-akhir 800rb --umur-aset-tahun 4 --format json > laporan-katering-q1.json
python3 scripts/rasio.py laporan-katering-q1.json --jenis katering --bagian-lancar-utang-bank 4jt --cicilan-bulanan 950rb
```

**Verifikasi manual:** aset lancar 12,5 + 0,8 = 13,3 jt; utang lancar = bagian bank 4 jt → 3,33. DER 10/9,3 = 1,08. Laba/bulan 5 jt/3 = 1.666.667 → cicilan 950rb = 57,0% (> 50% = terlalu berat). Umur stok rata-rata (0+0,8)/2 × 90 hari / 3,7 jt = 9,7 hari.

**Output script:**

# Analisis Rasio Keuangan — Katering Bu Rina
Jenis usaha: Produksi/manufaktur kecil (konveksi, makanan olahan, kuliner, katering, kerajinan) · Periode dianalisis: 1 Januari 2026 s.d. 31 Maret 2026 · Status data: **LENGKAP**

## Ringkasan untuk pemilik
Pada 1 Januari 2026 s.d. 31 Maret 2026, usaha UNTUNG Rp 5.000.000 (41,7% dari penjualan). Dari 11 rasio yang dinilai terhadap ambang usaha manufaktur: 9 baik, 2 waspada, 0 bahaya. Perlu diperhatikan: DER 1,08x; DAR 51,8%.

## Likuiditas — sanggup bayar tagihan jangka pendek? (1 Januari 2026 s.d. 31 Maret 2026)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Rasio lancar (current ratio) | 3,33x | aset lancar ÷ utang lancar | ≥ 1,50x baik · 1,10x–1,50x waspada · < 1,10x bahaya | 🟢 Baik | Setiap Rp 1 utang jangka pendek dijamin Rp 3,33 aset lancar. |
| Rasio cepat (quick ratio) | 3,13x | (aset lancar − persediaan) ÷ utang lancar | ≥ 0,80x baik · 0,50x–0,80x waspada · < 0,50x bahaya | 🟢 Baik | Tanpa menjual stok, tersedia Rp 3,13 untuk tiap Rp 1 utang jangka pendek. |
| Rasio kas (cash ratio) | 3,13x | kas & bank ÷ utang lancar | ≥ 0,20x baik · 0,10x–0,20x waspada · < 0,10x bahaya | 🟢 Baik | Uang kas/bank yang ada menutup 313% dari utang jangka pendek. |
| Modal kerja bersih | Rp 9.300.000 | aset lancar − utang lancar | — | ⚪ Info | Aset lancar melebihi utang lancar sebesar Rp 9.300.000. |

## Profitabilitas — seberapa untung? (1 Januari 2026 s.d. 31 Maret 2026)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Margin laba kotor | 69,2% | laba kotor ÷ penjualan × 100 | ≥ 25,0% baik · 15,0%–25,0% waspada · < 15,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, sisa setelah modal barang Rp 69.167. |
| Margin laba usaha | 41,7% | laba usaha ÷ penjualan × 100 | — | ⚪ Info | Dari tiap Rp 100.000 penjualan, laba usaha Rp 41.667. |
| Margin laba bersih | 41,7% | laba bersih ÷ penjualan × 100 | ≥ 8,0% baik · 4,0%–8,0% waspada · < 4,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, laba bersih Rp 41.667. |
| ROA disetahunkan (laba ÷ aset) | 105,1% | laba bersih ÷ total aset × 100 × (365 ÷ 90 hari) | ≥ 8,0% baik · 4,0%–8,0% waspada · < 4,0% bahaya | 🟢 Baik | Tiap Rp 100.000 aset usaha menghasilkan laba Rp 105.066 setahun. Angka >100% biasa terjadi bila aset/modal tercatat kecil (usaha rumahan, peralatan pribadi tidak dicatat) atau periode pendek disetahunkan — jangan dijadikan patokan tunggal. |
| ROE disetahunkan (laba ÷ modal) | 283,6% | laba bersih ÷ rata-rata modal × 100 × (365 ÷ 90 hari) | ≥ 15,0% baik · 6,0%–15,0% waspada · < 6,0% bahaya | 🟢 Baik | Tiap Rp 100.000 modal pemilik menghasilkan laba Rp 283.605 setahun. Angka >100% biasa terjadi bila aset/modal tercatat kecil (usaha rumahan, peralatan pribadi tidak dicatat) atau periode pendek disetahunkan — jangan dijadikan patokan tunggal. |

## Solvabilitas — seberapa besar bergantung pada utang? (1 Januari 2026 s.d. 31 Maret 2026)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| DER (utang ÷ modal) | 1,08x | total utang ÷ modal | ≤ 1,00x baik · 1,00x–2,00x waspada · > 2,00x bahaya | 🟡 Waspada | Utang = 108% dari modal sendiri. |
| DAR (utang ÷ aset) | 51,8% | total utang ÷ total aset × 100 | ≤ 50,0% baik · 50,0%–67,0% waspada · > 67,0% bahaya | 🟡 Waspada | 51,8% aset usaha dibiayai utang. |

## Aktivitas — seberapa cepat stok & piutang jadi uang? (1 Januari 2026 s.d. 31 Maret 2026)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Perputaran persediaan (per periode) | 9,25x | HPP ÷ rata-rata persediaan | — | ⚪ Info | Stok 'habis dan diisi ulang' sekitar 9,3 kali dalam periode ini. |
| Umur stok (hari) | 9,7 hari | rata-rata persediaan × hari periode ÷ HPP | ≤ 60,0 hari baik · 60,0 hari–90,0 hari waspada · > 90,0 hari bahaya | 🟢 Baik | Barang rata-rata diam di gudang/rak ±10 hari sebelum terjual. |
| Lama piutang tertagih (hari) | 0,0 hari | rata-rata piutang × hari periode ÷ total penjualan | ≤ 45,0 hari baik · 45,0 hari–60,0 hari waspada · > 60,0 hari bahaya | 🟢 Baik | Tidak ada piutang — semua penjualan sudah dibayar. |
| Lama bayar pemasok (hari) | 0,0 hari | utang usaha × hari periode ÷ HPP | — | ⚪ Info | Tidak ada utang ke pemasok — belanja dibayar tunai. |
| Siklus kas (hari stok + hari piutang − hari utang) | 9,7 hari | hari stok + hari piutang − hari utang | — | ⚪ Info | Uang usaha tertahan ±10 hari dari beli barang sampai uang kembali. |
| Perputaran aset disetahunkan | 2,52x | penjualan ÷ total aset × (365 ÷ hari) | — | ⚪ Info | Tiap Rp 1 aset menghasilkan penjualan Rp 2,52 setahun. |

## Kesiapan pengajuan KUR/kredit (dari sisi angka)
**BELUM SIAP — perbaiki poin ✗ dulu**
- ✓ Usaha UNTUNG Rp 5.000.000 pada periode ini.
- ✓ Modal sendiri Rp 9.300.000 positif.
- ⚠ DER 1,08x (utang dibanding modal).
- ✓ Rasio lancar 3,33x.
- ✗ Cicilan Rp 950.000/bulan = 57,0% dari laba bersih per bulan Rp 1.666.667 → 🔴 TERLALU BERAT.
- Laba bersih rata-rata per bulan: Rp 1.666.667.
_Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill pengajuan-kur._

## Saran tindakan (urut prioritas)
1. **Rencana cicilan** — Cicilan melebihi 30% laba bersih per bulan. Kecilkan plafon, pilih tenor lebih panjang, atau pinjam bertahap; hitung plafon yang aman dengan skill pengajuan-kur sebelum ke bank.
2. **DER (utang ÷ modal)** — Utang besar dibanding modal sendiri. Jangan ambil pinjaman baru dulu, dahulukan melunasi utang berbunga tertinggi, dan tahan prive agar laba menambah modal.
3. **DAR (utang ÷ aset)** — Sebagian besar aset dibiayai utang. Kurangi ketergantungan pada pinjaman; tahan laba di usaha (prive secukupnya) agar porsi modal sendiri naik.

## Asumsi yang dipakai
- [1 Januari 2026 s.d. 31 Maret 2026] Bagian utang bank yang jatuh tempo ≤ 12 bulan: Rp 4.000.000 (sisanya jangka panjang).
- Ambang 'wajar' = pedoman praktis untuk jenis usaha manufaktur (references/ambang-wajar.md).

_Disclaimer: Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis (lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM._
