# Uji 05 (Akun B) — Konveksi kecil, persediaan & piutang besar, tren 2 semester, kesiapan KUR

> Penguji independen (Akun B), 2026-09-26. Skenario normal #3. Tabel dipisah TAB, angka format "jt" dengan koma desimal, periode 6 bulan (uji penyetahunan).

**Permintaan pengguna (simulasi):** "Konveksi saya jual ke toko-toko pakai tempo. Ini angka semester 1 dan 2 tahun 2025. Mau ajukan KUR, cicilannya kira-kira 1,8 juta sebulan. Dari angka, siap nggak? Apa yang memburuk?"

**Data (`s3-konveksi.csv`, TAB):**
```
Pos	Sem-1 2025	Sem-2 2025
Penjualan	300jt	330jt
Penjualan tempo	180jt	231jt
HPP	210jt	237,6jt
Laba bersih	21jt	16,5jt
Beban bunga	1,5jt	2,1jt
Kas	9jt	5jt
Piutang	60jt	95jt
Persediaan	70jt	98jt
Aset tetap	60jt	57jt
Utang usaha	35jt	52jt
Utang lancar lain	10jt	24jt
Utang jangka panjang	30jt	40jt
Modal	124jt	139jt
Bulan	6	6
```
Neraca seimbang (199 = 75 + 124; 255 = 116 + 139).

**Perintah:**
```bash
python3 scripts/rasio.py s3-konveksi.csv --jenis konveksi --nama-usaha "Konveksi Rapi Jaya" --cicilan-bulanan 1,8jt
```

**Output script (lengkap):**

# Analisis Rasio Keuangan — Konveksi Rapi Jaya
Jenis usaha: Produksi/manufaktur kecil (konveksi, makanan olahan, kuliner, katering, kerajinan) · Periode dianalisis: Sem-1 2025, Sem-2 2025 · Status data: **LENGKAP**

## Ringkasan untuk pemilik
Pada Sem-2 2025, usaha UNTUNG Rp 16.500.000 (5,0% dari penjualan). Dari 12 rasio yang dinilai terhadap ambang usaha manufaktur: 8 baik, 2 waspada, 2 bahaya. Paling mendesak: Rasio kas 0,07x; Lama piutang tertagih 61,2 hari.

## Likuiditas — sanggup bayar tagihan jangka pendek? (Sem-2 2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Rasio lancar (current ratio) | 2,61x | aset lancar ÷ utang lancar | ≥ 1,50x baik · 1,10x–1,50x waspada · < 1,10x bahaya | 🟢 Baik | Setiap Rp 1 utang jangka pendek dijamin Rp 2,61 aset lancar. |
| Rasio cepat (quick ratio) | 1,32x | (aset lancar − persediaan) ÷ utang lancar | ≥ 0,80x baik · 0,50x–0,80x waspada · < 0,50x bahaya | 🟢 Baik | Tanpa menjual stok, tersedia Rp 1,32 untuk tiap Rp 1 utang jangka pendek. |
| Rasio kas (cash ratio) | 0,07x | kas & bank ÷ utang lancar | ≥ 0,20x baik · 0,10x–0,20x waspada · < 0,10x bahaya | 🔴 Bahaya | Uang kas/bank yang ada menutup 7% dari utang jangka pendek. |
| Modal kerja bersih | Rp 122.000.000 | aset lancar − utang lancar | — | ⚪ Info | Aset lancar melebihi utang lancar sebesar Rp 122.000.000. |

## Profitabilitas — seberapa untung? (Sem-2 2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Margin laba kotor | 28,0% | laba kotor ÷ penjualan × 100 | ≥ 25,0% baik · 15,0%–25,0% waspada · < 15,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, sisa setelah modal barang Rp 28.000. |
| Margin laba bersih | 5,0% | laba bersih ÷ penjualan × 100 | ≥ 8,0% baik · 4,0%–8,0% waspada · < 4,0% bahaya | 🟡 Waspada | Dari tiap Rp 100.000 penjualan, laba bersih Rp 5.000. |
| ROA disetahunkan (laba ÷ aset) | 14,5% | laba bersih ÷ rata-rata total aset × 100 × (365 ÷ 183 hari) | ≥ 8,0% baik · 4,0%–8,0% waspada · < 4,0% bahaya | 🟢 Baik | Tiap Rp 100.000 aset usaha menghasilkan laba Rp 14.537 setahun. |
| ROE disetahunkan (laba ÷ modal) | 25,1% | laba bersih ÷ rata-rata modal × 100 × (365 ÷ 183 hari) | ≥ 15,0% baik · 6,0%–15,0% waspada · < 6,0% bahaya | 🟢 Baik | Tiap Rp 100.000 modal pemilik menghasilkan laba Rp 25.095 setahun. |

## Solvabilitas — seberapa besar bergantung pada utang? (Sem-2 2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| DER (utang ÷ modal) | 0,83x | total utang ÷ modal | ≤ 1,00x baik · 1,00x–2,00x waspada · > 2,00x bahaya | 🟢 Baik | Utang = 83% dari modal sendiri. |
| DAR (utang ÷ aset) | 45,5% | total utang ÷ total aset × 100 | ≤ 50,0% baik · 50,0%–67,0% waspada · > 67,0% bahaya | 🟢 Baik | 45,5% aset usaha dibiayai utang. |
| Cakupan bunga (laba usaha ÷ bunga) | 8,86x | (laba bersih + bunga + pajak) ÷ beban bunga | ≥ 3,00x baik · 1,50x–3,00x waspada · < 1,50x bahaya | 🟢 Baik | Laba usaha cukup untuk membayar bunga 8,9 kali. |

## Aktivitas — seberapa cepat stok & piutang jadi uang? (Sem-2 2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Perputaran persediaan (per periode) | 2,83x | HPP ÷ rata-rata persediaan | — | ⚪ Info | Stok 'habis dan diisi ulang' sekitar 2,8 kali dalam periode ini. |
| Umur stok (hari) | 64,5 hari | rata-rata persediaan × hari periode ÷ HPP | ≤ 60,0 hari baik · 60,0 hari–90,0 hari waspada · > 90,0 hari bahaya | 🟡 Waspada | Barang rata-rata diam di gudang/rak ±65 hari sebelum terjual. |
| Perputaran piutang (per periode) | 2,98x | penjualan tempo ÷ rata-rata piutang | — | ⚪ Info | Piutang tertagih ±3,0 kali dalam periode ini. |
| Lama piutang tertagih (hari) | 61,2 hari | rata-rata piutang × hari periode ÷ penjualan tempo | ≤ 45,0 hari baik · 45,0 hari–60,0 hari waspada · > 60,0 hari bahaya | 🔴 Bahaya | Uang dari penjualan tempo rata-rata masuk setelah ±61 hari. |
| Lama bayar pemasok (hari) | 39,9 hari | utang usaha × hari periode ÷ HPP | — | ⚪ Info | Pemasok rata-rata dibayar setelah ±40 hari. |
| Siklus kas (hari stok + hari piutang − hari utang) | 85,8 hari | hari stok + hari piutang − hari utang | — | ⚪ Info | Uang usaha tertahan ±86 hari dari beli barang sampai uang kembali. |
| Perputaran aset disetahunkan | 2,91x | penjualan ÷ total aset × (365 ÷ hari) | — | ⚪ Info | Tiap Rp 1 aset menghasilkan penjualan Rp 2,91 setahun. |

## Tren antarperiode
| Pos / rasio | Sem-1 2025 | Sem-2 2025 | Perubahan terakhir |
|---|---|---|---|
| Rasio lancar (current ratio) | 3,09x | 2,61x | memburuk (turun) |
| Rasio cepat (quick ratio) | 1,53x | 1,32x | memburuk (turun) |
| Rasio kas (cash ratio) | 0,20x | 0,07x | memburuk (turun) |
| Modal kerja bersih | Rp 94.000.000 | Rp 122.000.000 | naik |
| Margin laba kotor | 30,0% | 28,0% | memburuk (turun) |
| Margin laba bersih | 7,0% | 5,0% | memburuk (turun) |
| ROA disetahunkan (laba ÷ aset) | 21,1% | 14,5% | memburuk (turun) |
| ROE disetahunkan (laba ÷ modal) | 33,9% | 25,1% | memburuk (turun) |
| DER (utang ÷ modal) | 0,60x | 0,83x | memburuk (naik) |
| DAR (utang ÷ aset) | 37,7% | 45,5% | memburuk (naik) |
| Cakupan bunga (laba usaha ÷ bunga) | 15,00x | 8,86x | memburuk (turun) |
| Perputaran persediaan (per periode) | 3,00x | 2,83x | turun |
| Umur stok (hari) | 60,8 hari | 64,5 hari | memburuk (naik) |
| Perputaran piutang (per periode) | 3,00x | 2,98x | turun |
| Lama piutang tertagih (hari) | 60,8 hari | 61,2 hari | memburuk (naik) |
| Lama bayar pemasok (hari) | 30,4 hari | 39,9 hari | naik |
| Siklus kas (hari stok + hari piutang − hari utang) | 91,2 hari | 85,8 hari | turun |
| Perputaran aset disetahunkan | 3,02x | 2,91x | turun |
| Penjualan / pendapatan usaha bersih | Rp 300.000.000 | Rp 330.000.000 | membaik (naik) +10,0% |
| Laba (rugi) bersih | Rp 21.000.000 | Rp 16.500.000 | memburuk (turun) -21,4% |

## Kesiapan pengajuan KUR/kredit (dari sisi angka)
**BELUM SIAP — perbaiki poin ✗ dulu**
- ✓ Usaha UNTUNG Rp 16.500.000 pada periode ini.
- ✓ Modal sendiri Rp 139.000.000 positif.
- ✓ DER 0,83x (utang dibanding modal).
- ✓ Rasio lancar 2,61x.
- ✗ Cicilan Rp 1.800.000/bulan = 65,5% dari laba bersih per bulan Rp 2.750.000 → 🔴 TERLALU BERAT.
- Laba bersih rata-rata per bulan: Rp 2.750.000.
_Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill pengajuan-kur._

## Saran tindakan (urut prioritas)
1. **Rencana cicilan** — Cicilan melebihi 30% laba bersih per bulan. Kecilkan plafon, pilih tenor lebih panjang, atau pinjam bertahap; hitung plafon yang aman dengan skill pengajuan-kur sebelum ke bank.
2. **Rasio kas (cash ratio)** — Kas tunai tipis dibanding tagihan jangka pendek. Buat pos 'dana cadangan' terpisah, setor rutin (mis. 5% dari penjualan harian), dan jadwalkan pembayaran besar setelah hari ramai.
3. **Lama piutang tertagih (hari)** — Pelanggan terlalu lama membayar. Tetapkan batas tempo tertulis, kirim pengingat sopan sebelum jatuh tempo (skill tagih-piutang), dan batasi bon untuk pelanggan yang telat.
4. **Margin laba bersih** — Laba bersih kecil dibanding penjualan. Urutkan biaya operasional dari yang terbesar, pangkas yang tidak menambah penjualan, dan cek apakah gaji/sewa sudah terlalu besar untuk omzet sekarang.
5. **Umur stok (hari)** — Stok terlalu lama mengendap. Catat stok per barang (skill buku-stok), stop belanja barang yang tidak laku 30 hari, beli lebih sering dalam jumlah kecil, dan promo barang lama.

## Asumsi yang dipakai
- [Sem-1 2025] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- [Sem-2 2025] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- Ambang 'wajar' = pedoman praktis untuk jenis usaha manufaktur (references/ambang-wajar.md).

_Disclaimer: Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis (lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM._

---
## Penilaian penguji
- **Angka:** 37/37 nilai kedua semester (termasuk rasio cicilan) cocok dengan verifikasi Decimal, termasuk penyetahunan 365 ÷ 182,5 hari, rata-rata saldo, dan lama piutang dari **penjualan tempo** (bukan total penjualan).
- **Bagus:** tren menunjukkan hampir semua rasio memburuk sementara omzet naik 10% dan laba turun 21,4%. Rasio kas 🔴 & lama piutang 🔴 disorot. Saran piutang merujuk skill `tagih-piutang` (ada di repo). Kesiapan KUR "BELUM SIAP" karena cicilan 65,5% laba/bulan.
- **Temuan (sedang) — tren campur basis (sama dengan Uji 03):** Sem-2 memakai rata-rata saldo, Sem-1 memakai saldo akhir.
  - Lama piutang tampil 60,8 → 61,2 hari (+0,4). Dengan basis saldo akhir yang sama, Sem-2 = 95 × 182,5 ÷ 231 = **75,1 hari** (+14,3 hari).
  - Umur stok tampil 60,8 → 64,5 hari. Dengan saldo akhir, Sem-2 = 98 × 182,5 ÷ 237,6 = **75,3 hari**.
  - ROA tampil 21,1% → 14,5%. Dengan saldo akhir, Sem-2 = **12,9%**.
  Arah tren tetap benar di skenario ini, tetapi **besarnya pemburukan piutang & stok terlihat jauh lebih kecil** dari kenyataan. Padahal inilah pertanyaan inti usaha konveksi ber-tempo.
- **Catatan ringan:** ringkasan pemilik tidak menyebut "laba turun 21,4%" walau ada di tabel tren. Satu kalimat tren di ringkasan akan membantu pembaca awam.
