# Uji 04 (Akun B) — Laundry dengan utang bank, cakupan bunga & cicilan berjalan

> Penguji independen (Akun B), 2026-09-26. Skenario normal #2. Angka diketik lewat opsi dengan format Indonesia campuran.

**Permintaan pengguna (simulasi):** "Laundry saya setahun omzet 186 juta, bahan (deterjen, plastik, gas) 41 juta, laba usaha 26,4 juta, bunga bank 7,2 juta, laba bersih 19,2 juta. Kas 5,5 jt, piutang langganan hotel 3,1 jt, stok bahan 1,2 jt, mesin & ruko 118 jt. Utang supplier 2,4 jt, bagian pinjaman bank 12 bulan ke depan 21 jt, sisa pinjaman bank 64 jt, modal 40,4 jt. Cicilan bank sekarang 2,35 jt per bulan. Usaha saya sehat?"

**Perintah:**
```bash
python3 scripts/rasio.py --jenis laundry --nama-usaha "Laundry Kilat Mas Dedi" --penjualan "Rp 186.000.000" --hpp "41.000.000" \
  --laba-bersih "19,2 jt" --laba-usaha 26,4jt --beban-bunga "7.200.000" --kas 5,5jt --piutang 3.100.000 --persediaan 1,2jt \
  --aset-tetap 118jt --utang-usaha 2,4jt --utang-lancar-lain 21.000.000 --utang-jangka-panjang 64jt --modal 40,4jt \
  --bulan 12 --cicilan-bulanan 2,35jt
```
Neraca seimbang: 127,8 jt = 87,4 jt + 40,4 jt.

**Output script (lengkap):**

# Analisis Rasio Keuangan — Laundry Kilat Mas Dedi
Jenis usaha: Jasa (laundry, salon, bengkel, konsultan, jasa lain) · Periode dianalisis: periode ini · Status data: **LENGKAP**

## Ringkasan untuk pemilik
Pada periode ini, usaha UNTUNG Rp 19.200.000 (10,3% dari penjualan). Dari 11 rasio yang dinilai terhadap ambang usaha jasa: 5 baik, 2 waspada, 4 bahaya. Paling mendesak: Rasio lancar 0,42x; Rasio cepat 0,37x; DER 2,16x.

## Likuiditas — sanggup bayar tagihan jangka pendek? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Rasio lancar (current ratio) | 0,42x | aset lancar ÷ utang lancar | ≥ 1,20x baik · 1,00x–1,20x waspada · < 1,00x bahaya | 🔴 Bahaya | Setiap Rp 1 utang jangka pendek dijamin Rp 0,42 aset lancar. |
| Rasio cepat (quick ratio) | 0,37x | (aset lancar − persediaan) ÷ utang lancar | ≥ 1,00x baik · 0,70x–1,00x waspada · < 0,70x bahaya | 🔴 Bahaya | Tanpa menjual stok, tersedia Rp 0,37 untuk tiap Rp 1 utang jangka pendek. |
| Rasio kas (cash ratio) | 0,24x | kas & bank ÷ utang lancar | ≥ 0,30x baik · 0,15x–0,30x waspada · < 0,15x bahaya | 🟡 Waspada | Uang kas/bank yang ada menutup 24% dari utang jangka pendek. |
| Modal kerja bersih | −Rp 13.600.000 | aset lancar − utang lancar | — | ⚪ Info | Utang lancar melebihi aset lancar sebesar Rp 13.600.000. |

## Profitabilitas — seberapa untung? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Margin laba kotor | 78,0% | laba kotor ÷ penjualan × 100 | ≥ 40,0% baik · 25,0%–40,0% waspada · < 25,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, sisa setelah modal barang Rp 77.957. |
| Margin laba usaha | 14,2% | laba usaha ÷ penjualan × 100 | — | ⚪ Info | Dari tiap Rp 100.000 penjualan, laba usaha Rp 14.194. |
| Margin laba bersih | 10,3% | laba bersih ÷ penjualan × 100 | ≥ 15,0% baik · 8,0%–15,0% waspada · < 8,0% bahaya | 🟡 Waspada | Dari tiap Rp 100.000 penjualan, laba bersih Rp 10.323. |
| ROA disetahunkan (laba ÷ aset) | 15,0% | laba bersih ÷ total aset × 100 × (365 ÷ 365 hari) | ≥ 15,0% baik · 7,0%–15,0% waspada · < 7,0% bahaya | 🟢 Baik | Tiap Rp 100.000 aset usaha menghasilkan laba Rp 15.023 setahun. |
| ROE disetahunkan (laba ÷ modal) | 47,5% | laba bersih ÷ modal akhir × 100 × (365 ÷ 365 hari) | ≥ 15,0% baik · 6,0%–15,0% waspada · < 6,0% bahaya | 🟢 Baik | Tiap Rp 100.000 modal pemilik menghasilkan laba Rp 47.525 setahun. |

## Solvabilitas — seberapa besar bergantung pada utang? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| DER (utang ÷ modal) | 2,16x | total utang ÷ modal | ≤ 1,00x baik · 1,00x–2,00x waspada · > 2,00x bahaya | 🔴 Bahaya | Utang = 216% dari modal sendiri. |
| DAR (utang ÷ aset) | 68,4% | total utang ÷ total aset × 100 | ≤ 50,0% baik · 50,0%–67,0% waspada · > 67,0% bahaya | 🔴 Bahaya | 68,4% aset usaha dibiayai utang. |
| Cakupan bunga (laba usaha ÷ bunga) | 3,67x | laba usaha ÷ beban bunga | ≥ 3,00x baik · 1,50x–3,00x waspada · < 1,50x bahaya | 🟢 Baik | Laba usaha cukup untuk membayar bunga 3,7 kali. |

## Aktivitas — seberapa cepat stok & piutang jadi uang? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Perputaran persediaan (per periode) | 34,17x | HPP ÷ persediaan akhir | — | ⚪ Info | Stok 'habis dan diisi ulang' sekitar 34,2 kali dalam periode ini. |
| Umur stok (hari) | 10,7 hari | persediaan akhir × hari periode ÷ HPP | — | ⚪ Info | Barang rata-rata diam di gudang/rak ±11 hari sebelum terjual. |
| Perputaran piutang (per periode) | 60,00x | total penjualan ÷ piutang akhir | — | ⚪ Info | Piutang tertagih ±60,0 kali dalam periode ini. |
| Lama piutang tertagih (hari) | 6,1 hari | piutang akhir × hari periode ÷ total penjualan | ≤ 45,0 hari baik · 45,0 hari–60,0 hari waspada · > 60,0 hari bahaya | 🟢 Baik | Uang dari penjualan tempo rata-rata masuk setelah ±6 hari. Dihitung dari total penjualan (tunai + tempo), jadi angka sebenarnya untuk pelanggan tempo lebih lama. |
| Lama bayar pemasok (hari) | 21,4 hari | utang usaha × hari periode ÷ HPP | — | ⚪ Info | Pemasok rata-rata dibayar setelah ±21 hari. |
| Siklus kas (hari stok + hari piutang − hari utang) | -4,6 hari | hari stok + hari piutang − hari utang | — | ⚪ Info | Pemasok dibayar setelah uang pelanggan masuk (±5 hari lebih dulu) — menguntungkan kas. |
| Perputaran aset disetahunkan | 1,46x | penjualan ÷ total aset × (365 ÷ hari) | — | ⚪ Info | Tiap Rp 1 aset menghasilkan penjualan Rp 1,46 setahun. |

## Kesiapan pengajuan KUR/kredit (dari sisi angka)
**BELUM SIAP — perbaiki poin ✗ dulu**
- ✓ Usaha UNTUNG Rp 19.200.000 pada periode ini.
- ✓ Modal sendiri Rp 40.400.000 positif.
- ✗ DER 2,16x (utang dibanding modal).
- ✗ Rasio lancar 0,42x.
- ✗ Cicilan Rp 2.350.000/bulan = 146,9% dari laba bersih per bulan Rp 1.600.000 → ⛔ laba tidak cukup untuk cicilan.
- Laba bersih rata-rata per bulan: Rp 1.600.000.
_Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill pengajuan-kur._

## Saran tindakan (urut prioritas)
1. **Rencana cicilan** — Cicilan melebihi 30% laba bersih per bulan. Kecilkan plafon, pilih tenor lebih panjang, atau pinjam bertahap; hitung plafon yang aman dengan skill pengajuan-kur sebelum ke bank.
2. **Rasio lancar (current ratio)** — Utang jangka pendek hampir/melebihi aset lancar. Tunda pembelian aset & prive besar, negosiasikan tempo pemasok lebih panjang, tagih piutang lebih cepat, dan hindari menutup utang dengan utang baru.
3. **Rasio cepat (quick ratio)** — Aset lancar terlalu banyak tertahan di stok. Kurangi belanja stok yang lambat laku, jual/promo barang lama, dan sisihkan kas cadangan minimal 1 bulan biaya tetap.
4. **DER (utang ÷ modal)** — Utang besar dibanding modal sendiri. Jangan ambil pinjaman baru dulu, dahulukan melunasi utang berbunga tertinggi, dan tahan prive agar laba menambah modal.
5. **DAR (utang ÷ aset)** — Sebagian besar aset dibiayai utang. Kurangi ketergantungan pada pinjaman; tahan laba di usaha (prive secukupnya) agar porsi modal sendiri naik.
6. **Lainnya** — 2 masalah lain ada di tabel (status 🟡/🔴). Kerjakan 3 saran teratas dulu, lalu hitung ulang bulan depan.

## Asumsi yang dipakai
- [periode ini] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- Ambang 'wajar' = pedoman praktis untuk jenis usaha jasa (references/ambang-wajar.md).

_Disclaimer: Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis (lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM._

---
## Penilaian penguji
- **Angka:** 20/20 nilai cocok dengan verifikasi Decimal (termasuk cakupan bunga 26,4 ÷ 7,2 = 3,67 dan cicilan 146,9%).
- **Bagus:** ambang jasa dipakai (margin kotor 78% 🟢; umur stok hanya "info" untuk jasa). Masalah utama langsung tampak: utang jangka pendek > aset lancar (0,42), DER 2,16, DAR 68,4%. Kesimpulan KUR "BELUM SIAP" dan cicilan ⛔ melebihi laba, jujur tanpa menakut-nakuti.
- **Temuan (sedang) — saran tidak sesuai konteks:** saran #3 untuk rasio cepat berbunyi "Aset lancar terlalu banyak tertahan di stok. Kurangi belanja stok yang lambat laku…". Untuk laundry dengan stok hanya Rp 1,2 jt, penyebabnya adalah **utang lancar besar**, bukan stok. Saran rasio cepat sebaiknya bercabang: bila persediaan kecil dibanding aset lancar, arahkan ke utang lancar/kas.
- **Catatan ringan:** laba bersih sudah dikurangi bunga, sedangkan cicilan 2,35 jt memuat pokok + bunga. Rasio cicilan menjadi sedikit konservatif (bunga terhitung dua kali). Wajar, tetapi bisa disebut di Asumsi.
