# Format Input `hitung_hpp.py`

Angka boleh ditulis gaya Indonesia: `"14.000"`, `"1,5"`, `"1,5jt"`, `"Rp 250.000"`. Pakai titik untuk ribuan dan koma untuk desimal.

## JSON (disarankan)
| Kunci | Isi | Default |
|---|---|---|
| `nama_produk`, `satuan_produk` | Nama & satuan produk jadi (pcs, loyang, kemeja, proyek) | "Produk", "unit" |
| `jenis` | `produk` atau `jasa` (hanya label) | produk |
| `hasil_per_batch` | Unit jadi per 1x produksi/resep | 1 |
| `produksi_per_bulan` | Unit per bulan; **wajib** bila ada biaya `per: bulan` atau `alat` | — |
| `susut_bahan_persen` | Cadangan bahan terbuang, hanya untuk `bahan` | 0 |
| `bahan[]` | Lihat "Item biaya"; default `per: batch` | — |
| `tenaga_kerja[]` | Item biaya; default `per: batch` | — |
| `overhead[]` | Item biaya; default `per: batch` | — |
| `kemasan[]` | Item biaya; default `per: unit` | — |
| `alat[]` | `nama`, `harga`, `umur_bulan`, `nilai_sisa` (default 0) | — |
| `biaya_tetap_lain[]` | `nama`, `biaya` per bulan; **hanya untuk BEP**, tidak masuk HPP | — |
| `target_margin_persen` / `markup_persen` | Pilih salah satu | tabel pilihan margin |
| `harga_jual` | Harga saat ini untuk cek laba & BEP | — |
| `banding_harga` | Daftar harga lain yang ingin dibandingkan, mis. `[18000, 19500]` (laba, margin, markup, BEP tiap harga). CLI: `--banding-harga "18000;19500"` | — |
| `bulatkan` | Kelipatan pembulatan ke atas harga rekomendasi | 500 |

### Item biaya (pilih salah satu cara)
1. Langsung: `{"nama": "Gas", "biaya": "5.000", "per": "batch"}`
2. Dari pembelian: `{"nama": "Tepung", "harga_beli": "14.000", "isi_beli": 1, "satuan_beli": "kg", "pakai": 250, "satuan_pakai": "g"}`
3. Upah per jam: `{"nama": "Penjahit", "upah_per_jam": "20.000", "jam": 1.5, "per": "unit"}`

`per` = `unit` (per produk jadi), `batch` (per 1x produksi), atau `bulan` (dibagi `produksi_per_bulan`).

### Satuan yang dikenali
- Berat: mg, g/gr/gram, ons (100 g), kg/kilo, ton
- Volume: ml/cc, l/liter/ltr
- Panjang: mm, cm, m/meter, yard/yd (91,44 cm), inci/inch (2,54 cm)
- Jumlah: pcs/pc/buah/bh/biji/butir/lembar/lbr/unit/item, lusin (12), kodi (20), gross (144), rim (500)
- Satuan lain (sachet, ikat, pasang, sdm) boleh dipakai **hanya jika satuan beli = satuan pakai**.

## CSV sederhana
Baris pertama header. Kolom `kategori` wajib: `bahan`, `tenaga_kerja`, `overhead`, `kemasan`, `alat`, `biaya_tetap`. Kolom lain sama dengan kunci JSON (`nama`, `harga_beli`, `isi_beli`, `satuan_beli`, `pakai`, `satuan_pakai`, `biaya`, `per`, `upah_per_jam`, `jam`, `harga`, `umur_bulan`, `nilai_sisa`). Pengaturan (hasil per batch, produksi per bulan, margin) diberikan lewat argumen. Pemisah `;` disarankan. Contoh: `templates/contoh-hpp.csv`.
