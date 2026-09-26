# Contoh 01 — Toko sembako, satu tahun, cek kesiapan KUR (angka diketik)

> Contoh dari pembuat skill (output asli `scripts/rasio.py` v1.0.2, dijalankan 2026-09-26). Bukan hasil uji penguji independen.

**Permintaan pengguna:** "Toko sembako saya setahun: omzet 480 juta, HPP 408 juta, laba bersih 24 juta. Kas 12 jt, piutang 6 jt, stok 40 jt, peralatan 42 jt. Utang supplier 20 jt, utang lain 5 jt, pinjaman bank jangka panjang 15 jt, modal 60 jt. Mau ambil KUR cicilan 500 ribu/bulan, aman?"

**Perintah:**
```bash
python3 scripts/rasio.py --jenis warung --nama-usaha "Toko Sembako Berkah" --penjualan "Rp 480.000.000" --hpp 408jt \
  --laba-bersih 24jt --kas 12jt --piutang 6jt --persediaan 40jt --aset-tetap 42jt --utang-usaha 20jt \
  --utang-lancar-lain 5jt --utang-jangka-panjang 15jt --modal 60jt --bulan 12 --cicilan-bulanan 500rb
```

**Verifikasi manual (kalkulator):** aset lancar 12+6+40 = 58 jt; utang lancar 20+5 = 25 jt → rasio lancar 58/25 = 2,32. Rasio cepat (58−40)/25 = 0,72. Margin kotor (480−408)/480 = 15,0%. ROA 24/100 = 24%. ROE 24/60 = 40%. DER 40/60 = 0,67. Umur stok 40×365/408 = 35,8 hari. Laba per bulan 24/12 = 2 jt → cicilan 0,5/2 = 25%.

**Output script:**

# Analisis Rasio Keuangan — Toko Sembako Berkah
Jenis usaha: Dagang (warung, toko, grosir, reseller, toko online) · Periode dianalisis: periode ini · Status data: **LENGKAP**

## Ringkasan untuk pemilik
Pada periode ini, usaha UNTUNG Rp 24.000.000 (5,0% dari penjualan). Dari 11 rasio yang dinilai terhadap ambang usaha dagang: 10 baik, 1 waspada, 0 bahaya. Perlu diperhatikan: Umur stok 35,8 hari.

## Likuiditas — sanggup bayar tagihan jangka pendek? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Rasio lancar (current ratio) | 2,32x | aset lancar ÷ utang lancar | ≥ 1,50x baik · 1,00x–1,50x waspada · < 1,00x bahaya | 🟢 Baik | Setiap Rp 1 utang jangka pendek dijamin Rp 2,32 aset lancar. |
| Rasio cepat (quick ratio) | 0,72x | (aset lancar − persediaan) ÷ utang lancar | ≥ 0,50x baik · 0,20x–0,50x waspada · < 0,20x bahaya | 🟢 Baik | Tanpa menjual stok, tersedia Rp 0,72 untuk tiap Rp 1 utang jangka pendek. |
| Rasio kas (cash ratio) | 0,48x | kas & bank ÷ utang lancar | ≥ 0,20x baik · 0,10x–0,20x waspada · < 0,10x bahaya | 🟢 Baik | Uang kas/bank yang ada menutup 48% dari utang jangka pendek. |
| Modal kerja bersih | Rp 33.000.000 | aset lancar − utang lancar | — | ⚪ Info | Aset lancar melebihi utang lancar sebesar Rp 33.000.000. |

## Profitabilitas — seberapa untung? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Margin laba kotor | 15,0% | laba kotor ÷ penjualan × 100 | ≥ 15,0% baik · 8,0%–15,0% waspada · < 8,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, sisa setelah modal barang Rp 15.000. |
| Margin laba bersih | 5,0% | laba bersih ÷ penjualan × 100 | ≥ 5,0% baik · 2,0%–5,0% waspada · < 2,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, laba bersih Rp 5.000. |
| ROA disetahunkan (laba ÷ aset) | 24,0% | laba bersih ÷ total aset × 100 × (365 ÷ 365 hari) | ≥ 10,0% baik · 5,0%–10,0% waspada · < 5,0% bahaya | 🟢 Baik | Tiap Rp 100.000 aset usaha menghasilkan laba Rp 24.000 setahun. |
| ROE disetahunkan (laba ÷ modal) | 40,0% | laba bersih ÷ modal akhir × 100 × (365 ÷ 365 hari) | ≥ 15,0% baik · 6,0%–15,0% waspada · < 6,0% bahaya | 🟢 Baik | Tiap Rp 100.000 modal pemilik menghasilkan laba Rp 40.000 setahun. |

## Solvabilitas — seberapa besar bergantung pada utang? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| DER (utang ÷ modal) | 0,67x | total utang ÷ modal | ≤ 1,00x baik · 1,00x–2,00x waspada · > 2,00x bahaya | 🟢 Baik | Utang = 67% dari modal sendiri. |
| DAR (utang ÷ aset) | 40,0% | total utang ÷ total aset × 100 | ≤ 50,0% baik · 50,0%–67,0% waspada · > 67,0% bahaya | 🟢 Baik | 40,0% aset usaha dibiayai utang. |

## Aktivitas — seberapa cepat stok & piutang jadi uang? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Perputaran persediaan (per periode) | 10,20x | HPP ÷ persediaan akhir | — | ⚪ Info | Stok 'habis dan diisi ulang' sekitar 10,2 kali dalam periode ini. |
| Umur stok (hari) | 35,8 hari | persediaan akhir × hari periode ÷ HPP | ≤ 30,0 hari baik · 30,0 hari–60,0 hari waspada · > 60,0 hari bahaya | 🟡 Waspada | Barang rata-rata diam di gudang/rak ±36 hari sebelum terjual. |
| Perputaran piutang (per periode) | 80,00x | total penjualan ÷ piutang akhir | — | ⚪ Info | Piutang tertagih ±80,0 kali dalam periode ini. |
| Lama piutang tertagih (hari) | 4,6 hari | piutang akhir × hari periode ÷ total penjualan | ≤ 30,0 hari baik · 30,0 hari–45,0 hari waspada · > 45,0 hari bahaya | 🟢 Baik | Uang dari penjualan tempo rata-rata masuk setelah ±5 hari. Dihitung dari total penjualan (tunai + tempo), jadi angka sebenarnya untuk pelanggan tempo lebih lama. |
| Lama bayar pemasok (hari) | 17,9 hari | utang usaha × hari periode ÷ HPP | — | ⚪ Info | Pemasok rata-rata dibayar setelah ±18 hari. |
| Siklus kas (hari stok + hari piutang − hari utang) | 22,5 hari | hari stok + hari piutang − hari utang | — | ⚪ Info | Uang usaha tertahan ±22 hari dari beli barang sampai uang kembali. |
| Perputaran aset disetahunkan | 4,80x | penjualan ÷ total aset × (365 ÷ hari) | — | ⚪ Info | Tiap Rp 1 aset menghasilkan penjualan Rp 4,80 setahun. |

## Kesiapan pengajuan KUR/kredit (dari sisi angka)
**ANGKA CUKUP SEHAT untuk dibawa ke bank**
- ✓ Usaha UNTUNG Rp 24.000.000 pada periode ini.
- ✓ Modal sendiri Rp 60.000.000 positif.
- ✓ DER 0,67x (utang dibanding modal).
- ✓ Rasio lancar 2,32x.
- ✓ Cicilan Rp 500.000/bulan = 25,0% dari laba bersih per bulan Rp 2.000.000 → 🟢 AMAN.
- Laba bersih rata-rata per bulan: Rp 2.000.000.
_Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill pengajuan-kur._

## Saran tindakan (urut prioritas)
1. **Umur stok (hari)** — Stok terlalu lama mengendap. Catat stok per barang (skill buku-stok), stop belanja barang yang tidak laku 30 hari, beli lebih sering dalam jumlah kecil, dan promo barang lama.

## Asumsi yang dipakai
- [periode ini] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- Ambang 'wajar' = pedoman praktis untuk jenis usaha dagang (references/ambang-wajar.md).

_Disclaimer: Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis (lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM._
