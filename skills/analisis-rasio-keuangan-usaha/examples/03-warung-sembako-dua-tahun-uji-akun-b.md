# Uji 03 (Akun B) — Warung sembako, data 2 tahun (2024 vs 2025), rencana KUR

> Penguji independen (Akun B), 2026-09-26. Folder uji: salinan skill di scratchpad (bukan `.claude/skills/`). Script `scripts/rasio.py` v1.0.0 dijalankan apa adanya. Skenario normal #1 (dipakai juga untuk uji A/B & banding pesaing).

**Permintaan pengguna (simulasi):** "Ini angka warung sembako saya 2024 dan 2025. Omzet naik tapi kok kas makin tipis? Saya mau ambil KUR cicilan 750 ribu per bulan, aman nggak?"

**Data (`s1-warung.csv`, pemisah `;`, format Rupiah campuran):**
```
Pos;2024;2025
Omzet;Rp 360.000.000;Rp 420.000.000
HPP;306.000.000;361.200.000
Laba bersih;14.400.000;16.800.000
Kas;8.000.000;6.500.000
Piutang;2.000.000;4.200.000
Stok barang;35.000.000;48.000.000
Peralatan;20.000.000;18.000.000
Utang supplier;15.000.000;26.000.000
Utang lain;2.000.000;3.000.000
Utang jangka panjang;0;0
Modal;48.000.000;47.700.000
Bulan;12;12
```
Neraca seimbang di kedua tahun (2024: 65 jt = 17 jt + 48 jt; 2025: 76,7 jt = 29 jt + 47,7 jt).

**Perintah:**
```bash
python3 scripts/rasio.py s1-warung.csv --jenis "warung sembako" --nama-usaha "Warung Sembako Bu Tini" --cicilan-bulanan 750rb
```
Sinonim baris ("Omzet", "Stok barang", "Utang supplier", "Peralatan") terbaca semua; jenis "warung sembako" → dagang. Keluar kode 0.

**Output script (lengkap):**

# Analisis Rasio Keuangan — Warung Sembako Bu Tini
Jenis usaha: Dagang (warung, toko, grosir, reseller, toko online) · Periode dianalisis: 2024, 2025 · Status data: **LENGKAP**

## Ringkasan untuk pemilik
Pada 2025, usaha UNTUNG Rp 16.800.000 (4,0% dari penjualan). Dari 11 rasio yang dinilai terhadap ambang usaha dagang: 7 baik, 4 waspada, 0 bahaya. Perlu diperhatikan: Rasio cepat 0,37x; Margin laba kotor 14,0%; Margin laba bersih 4,0%.

## Likuiditas — sanggup bayar tagihan jangka pendek? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Rasio lancar (current ratio) | 2,02x | aset lancar ÷ utang lancar | ≥ 1,50x baik · 1,00x–1,50x waspada · < 1,00x bahaya | 🟢 Baik | Setiap Rp 1 utang jangka pendek dijamin Rp 2,02 aset lancar. |
| Rasio cepat (quick ratio) | 0,37x | (aset lancar − persediaan) ÷ utang lancar | ≥ 0,50x baik · 0,20x–0,50x waspada · < 0,20x bahaya | 🟡 Waspada | Tanpa menjual stok, tersedia Rp 0,37 untuk tiap Rp 1 utang jangka pendek. |
| Rasio kas (cash ratio) | 0,22x | kas & bank ÷ utang lancar | ≥ 0,20x baik · 0,10x–0,20x waspada · < 0,10x bahaya | 🟢 Baik | Uang kas/bank yang ada menutup 22% dari utang jangka pendek. |
| Modal kerja bersih | Rp 29.700.000 | aset lancar − utang lancar | — | ⚪ Info | Aset lancar melebihi utang lancar sebesar Rp 29.700.000. |

## Profitabilitas — seberapa untung? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Margin laba kotor | 14,0% | laba kotor ÷ penjualan × 100 | ≥ 15,0% baik · 8,0%–15,0% waspada · < 8,0% bahaya | 🟡 Waspada | Dari tiap Rp 100.000 penjualan, sisa setelah modal barang Rp 14.000. |
| Margin laba bersih | 4,0% | laba bersih ÷ penjualan × 100 | ≥ 5,0% baik · 2,0%–5,0% waspada · < 2,0% bahaya | 🟡 Waspada | Dari tiap Rp 100.000 penjualan, laba bersih Rp 4.000. |
| ROA disetahunkan (laba ÷ aset) | 23,7% | laba bersih ÷ rata-rata total aset × 100 × (365 ÷ 365 hari) | ≥ 10,0% baik · 5,0%–10,0% waspada · < 5,0% bahaya | 🟢 Baik | Tiap Rp 100.000 aset usaha menghasilkan laba Rp 23.712 setahun. |
| ROE disetahunkan (laba ÷ modal) | 35,1% | laba bersih ÷ rata-rata modal × 100 × (365 ÷ 365 hari) | ≥ 15,0% baik · 6,0%–15,0% waspada · < 6,0% bahaya | 🟢 Baik | Tiap Rp 100.000 modal pemilik menghasilkan laba Rp 35.110 setahun. |

## Solvabilitas — seberapa besar bergantung pada utang? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| DER (utang ÷ modal) | 0,61x | total utang ÷ modal | ≤ 1,00x baik · 1,00x–2,00x waspada · > 2,00x bahaya | 🟢 Baik | Utang = 61% dari modal sendiri. |
| DAR (utang ÷ aset) | 37,8% | total utang ÷ total aset × 100 | ≤ 50,0% baik · 50,0%–67,0% waspada · > 67,0% bahaya | 🟢 Baik | 37,8% aset usaha dibiayai utang. |

## Aktivitas — seberapa cepat stok & piutang jadi uang? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Perputaran persediaan (per periode) | 8,70x | HPP ÷ rata-rata persediaan | — | ⚪ Info | Stok 'habis dan diisi ulang' sekitar 8,7 kali dalam periode ini. |
| Umur stok (hari) | 41,9 hari | rata-rata persediaan × hari periode ÷ HPP | ≤ 30,0 hari baik · 30,0 hari–60,0 hari waspada · > 60,0 hari bahaya | 🟡 Waspada | Barang rata-rata diam di gudang/rak ±42 hari sebelum terjual. |
| Perputaran piutang (per periode) | 135,48x | total penjualan ÷ rata-rata piutang | — | ⚪ Info | Piutang tertagih ±135,5 kali dalam periode ini. |
| Lama piutang tertagih (hari) | 2,7 hari | rata-rata piutang × hari periode ÷ total penjualan | ≤ 30,0 hari baik · 30,0 hari–45,0 hari waspada · > 45,0 hari bahaya | 🟢 Baik | Uang dari penjualan tempo rata-rata masuk setelah ±3 hari. Dihitung dari total penjualan (tunai + tempo), jadi angka sebenarnya untuk pelanggan tempo lebih lama. |
| Lama bayar pemasok (hari) | 26,3 hari | utang usaha × hari periode ÷ HPP | — | ⚪ Info | Pemasok rata-rata dibayar setelah ±26 hari. |
| Siklus kas (hari stok + hari piutang − hari utang) | 18,4 hari | hari stok + hari piutang − hari utang | — | ⚪ Info | Uang usaha tertahan ±18 hari dari beli barang sampai uang kembali. |
| Perputaran aset disetahunkan | 5,93x | penjualan ÷ total aset × (365 ÷ hari) | — | ⚪ Info | Tiap Rp 1 aset menghasilkan penjualan Rp 5,93 setahun. |

## Tren antarperiode
| Pos / rasio | 2024 | 2025 | Perubahan terakhir |
|---|---|---|---|
| Rasio lancar (current ratio) | 2,65x | 2,02x | memburuk (turun) |
| Rasio cepat (quick ratio) | 0,59x | 0,37x | memburuk (turun) |
| Rasio kas (cash ratio) | 0,47x | 0,22x | memburuk (turun) |
| Modal kerja bersih | Rp 28.000.000 | Rp 29.700.000 | naik |
| Margin laba kotor | 15,0% | 14,0% | memburuk (turun) |
| Margin laba bersih | 4,0% | 4,0% | tetap |
| ROA disetahunkan (laba ÷ aset) | 22,2% | 23,7% | membaik (naik) |
| ROE disetahunkan (laba ÷ modal) | 30,0% | 35,1% | membaik (naik) |
| DER (utang ÷ modal) | 0,35x | 0,61x | memburuk (naik) |
| DAR (utang ÷ aset) | 26,2% | 37,8% | memburuk (naik) |
| Perputaran persediaan (per periode) | 8,74x | 8,70x | turun |
| Umur stok (hari) | 41,7 hari | 41,9 hari | memburuk (naik) |
| Perputaran piutang (per periode) | 180,00x | 135,48x | turun |
| Lama piutang tertagih (hari) | 2,0 hari | 2,7 hari | memburuk (naik) |
| Lama bayar pemasok (hari) | 17,9 hari | 26,3 hari | naik |
| Siklus kas (hari stok + hari piutang − hari utang) | 25,9 hari | 18,4 hari | turun |
| Perputaran aset disetahunkan | 5,54x | 5,93x | naik |
| Penjualan / pendapatan usaha bersih | Rp 360.000.000 | Rp 420.000.000 | membaik (naik) +16,7% |
| Laba (rugi) bersih | Rp 14.400.000 | Rp 16.800.000 | membaik (naik) +16,7% |

## Kesiapan pengajuan KUR/kredit (dari sisi angka)
**BELUM SIAP — perbaiki poin ✗ dulu**
- ✓ Usaha UNTUNG Rp 16.800.000 pada periode ini.
- ✓ Modal sendiri Rp 47.700.000 positif.
- ✓ DER 0,61x (utang dibanding modal).
- ✓ Rasio lancar 2,02x.
- ✗ Cicilan Rp 750.000/bulan = 53,6% dari laba bersih per bulan Rp 1.400.000 → 🔴 TERLALU BERAT.
- Laba bersih rata-rata per bulan: Rp 1.400.000.
_Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill pengajuan-kur._

## Saran tindakan (urut prioritas)
1. **Rencana cicilan** — Cicilan melebihi 30% laba bersih per bulan. Kecilkan plafon, pilih tenor lebih panjang, atau pinjam bertahap; hitung plafon yang aman dengan skill pengajuan-kur sebelum ke bank.
2. **Rasio cepat (quick ratio)** — Aset lancar terlalu banyak tertahan di stok. Kurangi belanja stok yang lambat laku, jual/promo barang lama, dan sisihkan kas cadangan minimal 1 bulan biaya tetap.
3. **Margin laba kotor** — Selisih harga jual vs modal barang tipis. Cek harga beli di pemasok lain/beli lebih banyak sekaligus, naikkan harga produk yang laris secara bertahap, dan kurangi barang bermargin rendah (hitung per produk dengan skill hitung-hpp).
4. **Margin laba bersih** — Laba bersih kecil dibanding penjualan. Urutkan biaya operasional dari yang terbesar, pangkas yang tidak menambah penjualan, dan cek apakah gaji/sewa sudah terlalu besar untuk omzet sekarang.
5. **Umur stok (hari)** — Stok terlalu lama mengendap. Catat stok per barang (skill buku-stok), stop belanja barang yang tidak laku 30 hari, beli lebih sering dalam jumlah kecil, dan promo barang lama.

## Asumsi yang dipakai
- [2024] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- [2025] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- Ambang 'wajar' = pedoman praktis untuk jenis usaha dagang (references/ambang-wajar.md).

_Disclaimer: Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis (lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM._

---
## Penilaian penguji
- **Angka:** 35/35 nilai (rasio 2024 & 2025 + rasio cicilan) cocok dengan verifikasi Decimal independen (lihat `HASIL-UJI.md`). Rasio cicilan 750.000 ÷ 1.400.000 = 53,6% cocok.
- **Tafsiran awam:** bagus ("Setiap Rp 1 utang jangka pendek dijamin Rp 2,02 aset lancar", "Barang rata-rata diam ±42 hari"). Rasio cepat 0,37 dinilai 🟡 (ambang dagang), bukan "bahaya" seperti bila memakai Kasmir 1,5. Ini tepat untuk warung.
- **Pertanyaan "kenapa kas tipis"** terjawab lewat tren: rasio kas 0,47 → 0,22, DER 0,35 → 0,61, utang pemasok naik, stok naik 13 jt.
- **KUR:** "BELUM SIAP" hanya karena cicilan 53,6% > 50%. Saran nomor 1 = kecilkan plafon/tenor lebih panjang + rujuk `pengajuan-kur`. Tidak menjanjikan kredit.
- **Temuan (sedang) — tren campur basis:** 2025 memakai **rata-rata** saldo (karena ada 2024), sedangkan 2024 memakai **saldo akhir**. Akibatnya:
  - ROA tampil "membaik" 22,2% → 23,7%. Dengan basis yang sama (saldo akhir) ROA 2025 = 16,8 ÷ 76,7 = **21,9% → sebenarnya sedikit memburuk**.
  - Umur stok tampil 41,7 → 41,9 hari (nyaris tetap). Dengan saldo akhir, 2025 = 48 × 365 ÷ 361,2 = **48,5 hari** (naik ±7 hari). Kenaikan stok justru penyebab kas tipis, tetapi tabel tren menyamarkannya.
