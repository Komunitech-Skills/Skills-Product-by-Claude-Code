# Cara kerja aturan peringatan (untuk agent & pengguna yang ingin tahu)

Semua angka dihitung `scripts/peringatan_dini.py` dengan Decimal. Agent **tidak** menghitung
ulang atau mengubah angka.

## Arah metrik
| Arah | Artinya | Ditebak dari nama kolom (bisa dikoreksi `--arah kolom=...`) |
|---|---|---|
| `naik` | makin besar makin buruk | reject, cacat, rusak, gagal, retur, keluhan/komplain, telat/terlambat, absen/izin/sakit/tidak_hadir, downtime, waste/buang, void/batal/refund, lembur, susut |
| `turun` | makin kecil makin buruk | output, produksi, hasil, penjualan, omzet, transaksi, hadir, pengunjung, pesanan/order, terkirim, tepat_waktu, pendapatan |
| `dua` | belum jelas (mis. suhu) | hanya aturan sigma & 5 hari beruntun, target diabaikan |

Kolom `stok_*` + `pakai_*` diperlakukan sebagai pasangan stok (bukan metrik biasa).
Bila ada kolom reject **dan** output, ditambah metrik `% reject` = reject ÷ output × 100, supaya
reject yang naik karena produksi naik tidak disalahartikan.

## Aturan dan warna
| Aturan | 🟡 kuning | 🟠 oranye | 🔴 merah | Data minimum |
|---|---|---|---|---|
| Jarak dari rata-rata (σ) | – | ≥ 2σ ke arah buruk | ≥ 3σ | 14 angka sebelum hari ini |
| Pola bergeser | – | ≥ 7 angka terakhir berturut-turut di sisi buruk rata-rata | – | 14 angka |
| Beruntun | naik/turun 3–4 kali berturut-turut | ≥ 5 kali | – | 4 angka (celah > 3 hari memutus) |
| Banding hari yang sama (1–4 minggu lalu) | 20–34% lebih buruk | ≥ 35% | – | 2 minggu, dan rata-rata ≥ 5 (angka kecil seperti 1→2 keluhan tidak dipersenkan) |
| Target | lebih buruk < 10% | ≥ 10%, atau ≥ 3 dari 7 hari terakhir gagal | ≥ 50% | 1 angka + target |
| Proyeksi kasar | tren 7 hari (R² ≥ 0,5) diperkirakan melewati target dalam ≤ 7 hari | – | – | 5 angka dalam 7 hari |
| Sisa stok (L = lead time pemasok, default 2 hari) | ≤ 3L hari | ≤ 2L hari | ≤ L hari | 3 hari pemakaian |

Warna akhir satu metrik = aturan terberat yang kena. Semua alasan ditulis di laporan.

## Garis dasar
- Maksimal 28 angka tercatat **sebelum** hari laporan (hari ini tidak ikut, supaya lonjakan hari
  ini tidak melebarkan batasnya sendiri).
- Pencilan lama (|z| > 3 terhadap garis dasar) dibuang **sekali** lalu rata-rata & σ dihitung
  ulang — mis. hari listrik padam tidak membuat batas terlalu longgar. Tanggalnya dicatat di JSON
  `dasar.pencilan_diabaikan`.
- Hari khusus (libur nasional, Lebaran, event bazar) sebaiknya dikeluarkan dengan
  `--abaikan-tanggal`, karena pola hari itu memang tidak normal.

## Kejujuran statistik
- σ dan batas kendali mengandaikan angka harian relatif stabil. Usaha musiman (Ramadan, akhir
  tahun, awal bulan gajian) wajar memicu peringatan — itu tanda untuk dicek, bukan vonis.
- Proyeksi hanya garis lurus dari 7 hari terakhir; ditulis "perkiraan kasar". Tidak ada model
  ramalan, tidak ada jaminan.
- Hari kosong tidak diisi tebakan. Angka 0 dianggap angka sungguhan (bukan kosong).
