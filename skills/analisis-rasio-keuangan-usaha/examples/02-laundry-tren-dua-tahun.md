# Contoh 02 — Laundry, tren dua tahun dari tabel tempel (CSV titik koma)

> Contoh dari pembuat skill (output asli `scripts/rasio.py` v1.0.2, 2026-09-26). Termasuk baris yang tidak dikenal untuk menunjukkan penanganan input kotor.

**Permintaan pengguna:** "Ini angka laundry saya 2024 dan 2025. Omzet naik tapi kok uang terasa seret? Bandingkan dong."

**File `laundry.csv`:**
```
Pos;2024;2025
Pendapatan;Rp 180.000.000;Rp 216.000.000
HPP;54jt;71.280.000
Laba bersih;27.000.000;23.760.000
Kas;8jt;4jt
Piutang;3jt;9jt
Persediaan;2jt;3jt
Aset tetap;60jt;75jt
Utang usaha;4jt;6jt
Utang bank jangka pendek;6jt;12jt
Utang jangka panjang;20jt;35jt
Modal;43jt;38jt
Catatan kaki;x;y
```

**Perintah:** `python3 scripts/rasio.py laundry.csv --jenis laundry --nama-usaha "Laundry Bersih"`

**Verifikasi manual:** 2025 aset lancar 4+9+3 = 16 jt, utang lancar 6+12 = 18 jt → 0,89 (di bawah 1). DER 53/38 = 1,39. ROE pakai rata-rata modal (43+38)/2 = 40,5 jt → 23,76/40,5 = 58,7%. Penjualan +20% (180→216), laba −12% (27→23,76).

**Output script:**

# Analisis Rasio Keuangan — Laundry Bersih
Jenis usaha: Jasa (laundry, salon, bengkel, konsultan, jasa lain) · Periode dianalisis: 2024, 2025 · Status data: **SEMENTARA**

## Ringkasan untuk pemilik
Pada 2025, usaha UNTUNG Rp 23.760.000 (11,0% dari penjualan). Dari 10 rasio yang dinilai terhadap ambang usaha jasa: 4 baik, 5 waspada, 1 bahaya. Paling mendesak: Rasio lancar 0,89x.

## Likuiditas — sanggup bayar tagihan jangka pendek? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Rasio lancar (current ratio) | 0,89x | aset lancar ÷ utang lancar | ≥ 1,20x baik · 1,00x–1,20x waspada · < 1,00x bahaya | 🔴 Bahaya | Setiap Rp 1 utang jangka pendek dijamin Rp 0,89 aset lancar. |
| Rasio cepat (quick ratio) | 0,72x | (aset lancar − persediaan) ÷ utang lancar | ≥ 1,00x baik · 0,70x–1,00x waspada · < 0,70x bahaya | 🟡 Waspada | Tanpa menjual stok, tersedia Rp 0,72 untuk tiap Rp 1 utang jangka pendek. |
| Rasio kas (cash ratio) | 0,22x | kas & bank ÷ utang lancar | ≥ 0,30x baik · 0,15x–0,30x waspada · < 0,15x bahaya | 🟡 Waspada | Uang kas/bank yang ada menutup 22% dari utang jangka pendek. |
| Modal kerja bersih | −Rp 2.000.000 | aset lancar − utang lancar | — | ⚪ Info | Utang lancar melebihi aset lancar sebesar Rp 2.000.000. |

## Profitabilitas — seberapa untung? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Margin laba kotor | 67,0% | laba kotor ÷ penjualan × 100 | ≥ 40,0% baik · 25,0%–40,0% waspada · < 25,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, sisa setelah modal barang Rp 67.000. |
| Margin laba bersih | 11,0% | laba bersih ÷ penjualan × 100 | ≥ 15,0% baik · 8,0%–15,0% waspada · < 8,0% bahaya | 🟡 Waspada | Dari tiap Rp 100.000 penjualan, laba bersih Rp 11.000. |
| ROA disetahunkan (laba ÷ aset) | 29,0% | laba bersih ÷ rata-rata total aset × 100 × (365 ÷ 365 hari) | ≥ 15,0% baik · 7,0%–15,0% waspada · < 7,0% bahaya | 🟢 Baik | Tiap Rp 100.000 aset usaha menghasilkan laba Rp 28.976 setahun. |
| ROE disetahunkan (laba ÷ modal) | 58,7% | laba bersih ÷ rata-rata modal × 100 × (365 ÷ 365 hari) | ≥ 15,0% baik · 6,0%–15,0% waspada · < 6,0% bahaya | 🟢 Baik | Tiap Rp 100.000 modal pemilik menghasilkan laba Rp 58.667 setahun. |

## Solvabilitas — seberapa besar bergantung pada utang? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| DER (utang ÷ modal) | 1,39x | total utang ÷ modal | ≤ 1,00x baik · 1,00x–2,00x waspada · > 2,00x bahaya | 🟡 Waspada | Utang = 139% dari modal sendiri. |
| DAR (utang ÷ aset) | 58,2% | total utang ÷ total aset × 100 | ≤ 50,0% baik · 50,0%–67,0% waspada · > 67,0% bahaya | 🟡 Waspada | 58,2% aset usaha dibiayai utang. |

## Aktivitas — seberapa cepat stok & piutang jadi uang? (2025)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Perputaran persediaan (per periode) | 28,51x | HPP ÷ rata-rata persediaan | — | ⚪ Info | Stok 'habis dan diisi ulang' sekitar 28,5 kali dalam periode ini. |
| Umur stok (hari) | 12,8 hari | rata-rata persediaan × hari periode ÷ HPP | — | ⚪ Info | Barang rata-rata diam di gudang/rak ±13 hari sebelum terjual. |
| Perputaran piutang (per periode) | 36,00x | total penjualan ÷ rata-rata piutang | — | ⚪ Info | Piutang tertagih ±36,0 kali dalam periode ini. |
| Lama piutang tertagih (hari) | 10,1 hari | rata-rata piutang × hari periode ÷ total penjualan | ≤ 45,0 hari baik · 45,0 hari–60,0 hari waspada · > 60,0 hari bahaya | 🟢 Baik | Uang dari penjualan tempo rata-rata masuk setelah ±10 hari. Dihitung dari total penjualan (tunai + tempo), jadi angka sebenarnya untuk pelanggan tempo lebih lama. |
| Lama bayar pemasok (hari) | 30,7 hari | utang usaha × hari periode ÷ HPP | — | ⚪ Info | Pemasok rata-rata dibayar setelah ±31 hari. |
| Siklus kas (hari stok + hari piutang − hari utang) | -7,8 hari | hari stok + hari piutang − hari utang | — | ⚪ Info | Pemasok dibayar setelah uang pelanggan masuk (±8 hari lebih dulu) — menguntungkan kas. |
| Perputaran aset disetahunkan | 2,63x | penjualan ÷ total aset × (365 ÷ hari) | — | ⚪ Info | Tiap Rp 1 aset menghasilkan penjualan Rp 2,63 setahun. |

## Tren antarperiode
_Tren memakai basis SAMA untuk semua periode: saldo AKHIR tiap periode (persediaan, piutang, aset, modal). Tabel rasio periode terakhir di atas memakai rata-rata saldo awal-akhir bila tersedia, jadi angkanya bisa sedikit berbeda dari kolom terakhir tabel tren._

| Pos / rasio | 2024 | 2025 | Perubahan terakhir |
|---|---|---|---|
| Rasio lancar (current ratio) | 1,30x | 0,89x | memburuk (turun) |
| Rasio cepat (quick ratio) | 1,10x | 0,72x | memburuk (turun) |
| Rasio kas (cash ratio) | 0,80x | 0,22x | memburuk (turun) |
| Modal kerja bersih | Rp 3.000.000 | −Rp 2.000.000 | turun |
| Margin laba kotor | 70,0% | 67,0% | memburuk (turun) |
| Margin laba bersih | 15,0% | 11,0% | memburuk (turun) |
| ROA disetahunkan (laba ÷ aset) | 37,0% | 26,1% | memburuk (turun) |
| ROE disetahunkan (laba ÷ modal) | 62,8% | 62,5% | memburuk (turun) |
| DER (utang ÷ modal) | 0,70x | 1,39x | memburuk (naik) |
| DAR (utang ÷ aset) | 41,1% | 58,2% | memburuk (naik) |
| Perputaran persediaan (per periode) | 27,00x | 23,76x | turun |
| Umur stok (hari) | 13,5 hari | 15,4 hari | memburuk (naik) |
| Perputaran piutang (per periode) | 60,00x | 24,00x | turun |
| Lama piutang tertagih (hari) | 6,1 hari | 15,2 hari | memburuk (naik) |
| Lama bayar pemasok (hari) | 27,0 hari | 30,7 hari | naik |
| Siklus kas (hari stok + hari piutang − hari utang) | -7,4 hari | -0,2 hari | naik |
| Perputaran aset disetahunkan | 2,47x | 2,37x | turun |
| Penjualan / pendapatan usaha bersih | Rp 180.000.000 | Rp 216.000.000 | membaik (naik) +20,0% |
| Laba (rugi) bersih | Rp 27.000.000 | Rp 23.760.000 | memburuk (turun) -12,0% |

## Kesiapan pengajuan KUR/kredit (dari sisi angka)
**BELUM SIAP — perbaiki poin ✗ dulu**
- ✓ Usaha UNTUNG Rp 23.760.000 pada periode ini.
- ✓ Modal sendiri Rp 38.000.000 positif.
- ⚠ DER 1,39x (utang dibanding modal).
- ✗ Rasio lancar 0,89x.
- Laba bersih rata-rata per bulan: Rp 1.980.000.
- Cicilan belum diisi. Untuk cek kemampuan bayar, sebutkan total cicilan per bulan (lama + rencana) → --cicilan-bulanan.
_Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill pengajuan-kur._

## Saran tindakan (urut prioritas)
1. **Rasio lancar (current ratio)** — Utang jangka pendek hampir/melebihi aset lancar. Tunda pembelian aset & prive besar, negosiasikan tempo pemasok lebih panjang, tagih piutang lebih cepat, dan hindari menutup utang dengan utang baru.
2. **Rasio cepat (quick ratio)** — Kas + piutang tidak cukup menutup utang jangka pendek, dan stok bukan penyebabnya (stok kecil). Fokus ke utang & kas: minta tenor cicilan/tempo pemasok lebih panjang, tagih piutang, tahan prive & pembelian alat, dan sisihkan dana cadangan dari penjualan harian.
3. **Rasio kas (cash ratio)** — Kas tunai tipis dibanding tagihan jangka pendek. Buat pos 'dana cadangan' terpisah, setor rutin (mis. 5% dari penjualan harian), dan jadwalkan pembayaran besar setelah hari ramai.
4. **Margin laba bersih** — Laba bersih kecil dibanding penjualan. Urutkan biaya operasional dari yang terbesar, pangkas yang tidak menambah penjualan, dan cek apakah gaji/sewa sudah terlalu besar untuk omzet sekarang.
5. **DER (utang ÷ modal)** — Utang besar dibanding modal sendiri. Jangan ambil pinjaman baru dulu, dahulukan melunasi utang berbunga tertinggi, dan tahan prive agar laba menambah modal.
6. **Lainnya** — 1 masalah lain ada di tabel (status 🟡/🔴). Kerjakan 3 saran teratas dulu, lalu hitung ulang bulan depan.

## Perlu dicek
- Baris 13 'Catatan kaki' tidak dikenal → dilewati (ganti nama pos atau hapus bila bukan angka laporan).

## Asumsi yang dipakai
- [2024] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- [2024] Panjang periode tidak disebut → dianggap laporan 1 tahun (12 bulan, 365 hari).
- [2025] Total aset lancar dihitung dari rincian; Aset lancar lain tidak diisi → dianggap Rp 0.
- [2025] Panjang periode tidak disebut → dianggap laporan 1 tahun (12 bulan, 365 hari).
- Ambang 'wajar' = pedoman praktis untuk jenis usaha jasa (references/ambang-wajar.md).

_Disclaimer: Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis (lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM._
