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

## Model per metrik (v1.0.1)
| Model | Kapan | Cara menilai hari ini |
|---|---|---|
| `kejadian` | nama kolom kecelakaan/K3/cedera/luka/insiden/kebakaran/keracunan/near_miss, atau `--kejadian kolom` | setiap angka > 0 = 🔴 |
| `hitungan` | semua angka bulat dan rata-rata garis dasar < 20/hari (keluhan, retur, telat, absen), ≥ 7 angka | peluang Poisson P(X ≥ hari ini) dengan λ = rata-rata (min. 0,5/n bila selalu 0); bila datanya lebih "liar" dari Poisson, dipakai peluang normal yang lebih besar (lebih hati-hati). Selisih minimal: 🟡 ≥ 1, 🟠 ≥ 1,5, 🔴 ≥ 2,5 di atas λ |
| `normal` | selain itu, ≥ 14 angka garis dasar, σ > 0 | z = (hari ini − rata) / σ → peluang normal satu sisi; selisih minimal 3% dari rata-rata |
| `konstan` | σ = 0 (angka selalu sama), ≥ 7 angka | persen selisih: 🟡 ≥ 5%, 🟠 ≥ 20%, 🔴 ≥ 50% |

## Aturan dan warna
Peluang ambang: P2 = 0,02275 (setara 2σ), P3 = 0,00135 (3σ), P4 = 0,0000317 (4σ). Angka
kemarin/lusa dinilai terhadap garis dasar miliknya sendiri (angka sebelum hari itu).

| Aturan | 🟡 kuning | 🟠 oranye | 🔴 merah | Data minimum |
|---|---|---|---|---|
| Peluang (σ / Poisson) | ≤ P2 satu hari | ≤ P3, atau ≤ P2 dan 1 dari 2 angka sebelumnya juga ≤ P2 ("2 dari 3 hari") | ≤ P4, atau ≤ P3 dan kemarin ≤ P2 | normal 14 / hitungan 7 angka |
| Biasanya nol (λ < 1) | hari ini > angka tertinggi sebelumnya | (lewat aturan peluang) | – | 7 angka |
| Pola bergeser (selisih ≥ 3% dan ≥ ½σ) | 7–8 angka berturut-turut di sisi buruk rata-rata | ≥ 9 | – | 14 / 7 angka |
| Beruntun (hari ini harus di sisi buruk rata-rata) | naik/turun 3–4 kali | ≥ 5 kali | – | 4 angka (celah > 3 hari memutus) |
| Banding hari yang sama (1–4 minggu lalu) | ≥ 25% lebih buruk **dan** selisih ≥ 2σ (hitungan: ≥ 2√rata) | – | – | 2 minggu, rata-rata ≥ 5 |
| Target | lebih buruk < 10% | ≥ 10%, atau ≥ 3 dari 7 hari terakhir gagal, atau target 0 terlewati | ≥ 50% | 1 angka + target |
| Proyeksi kasar | tren 7 hari (R² ≥ 0,5) diperkirakan melewati target dalam ≤ 7 hari | – | – | 5 angka dalam 7 hari |
| Sisa stok (L = lead time, default 2 hari) | ≤ 3L hari | ≤ 2L hari | ≤ L hari, atau stok 0 | 3 hari pemakaian |

Warna akhir satu metrik = aturan terberat yang kena. Semua alasan ditulis di laporan.

Uji alarm palsu (tests/uji_regresi.py, data sintetis stabil 7 kolom, 600 hari laporan): hari dengan
≥ 🟠 ≤ 5% (terukur ±3%), hari dengan 🔴 ≤ 1% (terukur ±0,2%). Kuning masih muncul ±24% hari
(sengaja peka, artinya "perhatikan", bukan "bertindak").

## Sisa stok
Stok = sisa **akhir** hari laporan. Sisa hari = stok ÷ rata-rata pemakaian 7 angka terakhir
(ditampilkan dibulatkan ke bawah 1 desimal). "Cukup sampai" = hari penuh terakhir; "mulai kurang"
= hari berikutnya. < 1 hari → "habis besok". Bila sisa ≤ lead time, ditulis perkiraan hari kosong
walau dipesan hari ini (lead time − sisa hari).

## Garis dasar
- Maksimal 28 angka tercatat **sebelum** hari laporan (hari ini tidak ikut, supaya lonjakan hari
  ini tidak melebarkan batasnya sendiri).
- Pencilan lama (|z| > 3 terhadap garis dasar **dan** ≥ 7 hari kalender sebelum hari laporan)
  dibuang **sekali** lalu rata-rata & σ dihitung
  ulang (tidak dibuang bila σ jadi 0; model hitungan memakai semua angka) — mis. hari listrik padam tidak membuat batas terlalu longgar. Tanggalnya dicatat di JSON
  `dasar.pencilan_diabaikan` dan di baris ℹ️ laporan. Angka ekstrem dalam 7 hari terakhir tidak
  dibuang (bagian tren yang sedang berjalan, v1.0.5). Garis dasar < 14 angka: tidak ada yang
  dibuang.
- Hari khusus (libur nasional, Lebaran, event bazar) sebaiknya dikeluarkan dengan
  `--abaikan-tanggal`, karena pola hari itu memang tidak normal.

## Kejujuran statistik
- σ dan batas kendali mengandaikan angka harian relatif stabil. Usaha musiman (Ramadan, akhir
  tahun, awal bulan gajian) wajar memicu peringatan — itu tanda untuk dicek, bukan vonis.
- Proyeksi hanya garis lurus dari 7 hari terakhir; ditulis "perkiraan kasar". Tidak ada model
  ramalan, tidak ada jaminan.
- Hari kosong tidak diisi tebakan. Angka 0 dianggap angka sungguhan (bukan kosong).
