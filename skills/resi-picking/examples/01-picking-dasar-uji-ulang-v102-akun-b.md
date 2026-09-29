# Uji ulang v1.0.2 — Skenario normal 1: Shopee (header resmi ID) + lokasi rak + stok

Data uji (fiktif, dibuat khusus untuk uji ulang ini, disimpan di scratchpad, BUKAN di repo):
`pesanan-shopee.csv` (6 baris: 4 aktif, 1 belum bayar, 1 batal), `lokasi-rak.csv`, `stok.csv`.

## Perintah
```
python3 scripts/resi.py pesanan-shopee.csv --lokasi lokasi-rak.csv --stok stok.csv --json
```

## Hasil kunci
- `pemetaan_kolom`: semua 9 field terpetakan benar ke header resmi Shopee ID (No. Pesanan, No. Resi,
  Status Pesanan, Opsi Pengiriman, Nama Produk, Nomor Referensi SKU, Nama Variasi, Jumlah, Catatan
  dari Pembeli) — tanpa override.
- `kolom_ambigu`: `{}` (tidak ada kolom yang bentrok pada file ini).
- Peringatan stok: SDL-JP-40 butuh 2 vs stok 1 → kurang; SPT-SNK-42 butuh 1 vs stok 0 → kurang;
  SPT-SNK-43 tidak ada di file stok → SKU tak dikenal. SDL-JP-41 (butuh 1, stok 5) **benar tidak**
  diperingatkan.
- Status "belum bayar" dan "batal" masing-masing 1 pesanan dilewati dari daftar ambil & urutan resi.

## Verifikasi independen (dihitung manual dari CSV, bukan dari kode)
| Pesanan | SKU | Qty | Status |
|---|---|---|---|
| A1 | SDL-JP-40 | 2 | aktif |
| A2 | SDL-JP-41 | 1 | aktif |
| A3 | SPT-SNK-42 | 1 | aktif |
| A4 | SPT-SNK-43 | 3 | aktif |
| A5 | SDL-JP-40 | 1 | belum bayar → dilewati |
| A6 | SPT-SNK-42 | 1 | batal → dilewati |

Total pesanan aktif = 4 (cocok). Jenis barang aktif = 4 SKU unik (cocok). Total pcs = 2+1+1+3 = **7**
(cocok dengan "Total: 4 pesanan aktif, 4 jenis barang, 7 pcs." di `daftar-ambil.md`).
Pengelompokan rak: A1 → SDL-JP-40, SDL-JP-41; B2 → SPT-SNK-42, SPT-SNK-43 — cocok `lokasi-rak.csv`.
Urutan resi: 2 kurir (JNE Reguler 2 pesanan, Shopee Express 2 pesanan) — cocok.

**Hasil: BENAR, tidak ada selisih.**
