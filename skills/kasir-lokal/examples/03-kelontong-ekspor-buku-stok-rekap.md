# 03 — Toko kelontong: ekspor ke buku-stok & rekap-penjualan-csv (tanpa potong stok dobel)

**Skenario:** "Toko Kelontong Berkah" (fiktif) sudah memakai skill **buku-stok** untuk stok (beras & telur per kg). Kasir diatur `--stok buku-stok` (kasir tidak memotong stok). Sepanjang hari: 5 nota, 1 void siang, 1 retur sebagian (barang rusak, tidak kembali ke stok), 1 void sore atas nota yang **sudah** diimpor ke buku-stok. Ekspor diimpor dua kali ke buku-stok, plus sekali impor ulang untuk memastikan tidak dobel. Semua skill dijalankan sungguhan (`kasir.py`, `buku-stok/scripts/stok.py`, `rekap-penjualan-csv/scripts/rekap.py`) dengan DB di `/tmp/uji-kasir-lokal/c/`.

**Input pengguna:**
> tiap sore tolong kurangi stok di buku stok dari penjualan kasir hari ini, terus bikinin rekap penjualannya juga ya

Data awal buku-stok: BRS Beras 50 kg, MYK2 Minyak 24 pouch, GUL Gula 30 kg, TLR Telur 20 kg, IMG Indomie 120 bungkus, SBN Sabun 40 pcs, KCP Kecap 18 botol. Kode produk kasir = SKU buku-stok.

Transaksi 23/09/2026:
| Jam | Pesan | Nota | Total |
|---|---|---|---:|
| 07:00 | 2,5 kg beras, 1 minyak goreng, bayar tunai 100rb | N-0001 | 76.750 |
| 08:15 | setengah kg telur, 5 indomie, bayar pas | N-0002 | 32.000 |
| 09:00 | 2 sabun, 1 kecap, 1 kg gula, bayar qris | N-0003 | 38.500 |
| 09:05 | void N-0003 "pembeli batal" | R-0001 | −38.500 |
| 10:30 | 10 indomie diskon 5%, 1,25 kg telur, bayar tunai 70rb | N-0004 | 69.500 |
| 11:00 | retur 3 indomie dari N-0004, "kemasan sobek", `--stok-kembali tidak` | R-0002 | −9.975 |
| 17:00 | 1 minyak, 2 kg beras, bayar tunai 70rb | N-0005 | 69.000 |
| 18:00 | void N-0001 "salah input, pembeli tidak jadi" (N-0001 sudah diimpor siang) | R-0003 | −76.750 |

## Output

### Ekspor & impor ke buku-stok (siang, sebelum N-0004)
```
Ekspor 7 baris (3 nota) 23/09/2026 - 23/09/2026 untuk buku-stok: jual-kasir.csv
Impor di buku-stok: stok.py impor-pesanan "jual-kasir.csv" --platform lainnya (pratinjau dulu). ...
```
Pratinjau buku-stok:
```
Pesanan baru: 2 | sudah pernah diimpor (dilewati): 0
Diabaikan: batal 1, retur/refund 0, belum bayar 0
Stok berkurang (total 9):
  - IMG Indomie Goreng: -5 (stok 120 -> 115)
  - BRS Beras Pandan Wangi: -2,5 (stok 50 -> 47,5)
  - MYK2 Minyak Goreng - 2 liter: -1 (stok 24 -> 23)
  - TLR Telur Ayam: -0,5 (stok 20 -> 19,5)
```
→ pengguna "ya" → tersimpan (buku-stok membuat backup).

### Ekspor & impor sore (seluruh hari)
```
Ekspor 11 baris (5 nota) 23/09/2026 - 23/09/2026 untuk buku-stok: jual-kasir2.csv
Catatan: Retur sebagian TIDAK ada di file ini (buku-stok tidak menerima jumlah minus). Setelah barang dicek, catat di buku-stok: masuk --jenis retur-pembeli. Daftar: R-260923-0002 IMG x3 (2026-09-23)
```
Isi file (UTF-8 BOM, `;`):
```
Nomor Pesanan;Tanggal;SKU;Nama Produk;Varian;Jumlah;Harga Satuan;Status
N-260923-0001;2026-09-23 07:00;BRS;Beras Pandan Wangi;;2,5;15500;Dibatalkan
N-260923-0001;2026-09-23 07:00;MYK2;Minyak Goreng;2 liter;1;38000;Dibatalkan
N-260923-0002;2026-09-23 08:15;TLR;Telur Ayam;;0,5;29000;Selesai
N-260923-0002;2026-09-23 08:15;IMG;Indomie Goreng;;5;3500;Selesai
N-260923-0003;2026-09-23 09:00;SBN;Sabun Mandi;Lifebuoy 75g;2;4500;Dibatalkan
N-260923-0003;2026-09-23 09:00;KCP;Kecap Manis;275 ml;1;12000;Dibatalkan
N-260923-0003;2026-09-23 09:00;GUL;Gula Pasir;;1;17500;Dibatalkan
N-260923-0004;2026-09-23 10:30;IMG;Indomie Goreng;;10;3325;Selesai
N-260923-0004;2026-09-23 10:30;TLR;Telur Ayam;;1,25;29000;Selesai
N-260923-0005;2026-09-23 17:00;MYK2;Minyak Goreng;2 liter;1;38000;Selesai
N-260923-0005;2026-09-23 17:00;BRS;Beras Pandan Wangi;;2;15500;Selesai
```
Pratinjau buku-stok:
```
Pesanan baru: 2 | sudah pernah diimpor (dilewati): 2
Diabaikan: batal 1, retur/refund 0, belum bayar 0
Pesanan lama yang kini BATAL (stok dikembalikan): N-260923-0001
Stok berkurang (total 14,25):
  - IMG Indomie Goreng: -10 (stok 115 -> 105)
  - BRS Beras Pandan Wangi: -2 (stok 50 -> 48)
  - TLR Telur Ayam: -1,25 (stok 19,5 -> 18,25)
  - MYK2 Minyak Goreng - 2 liter: -1 (stok 24 -> 23)
```
Impor ulang file yang sama (uji dobel):
```
Pesanan baru: 0 | sudah pernah diimpor (dilewati): 4
PERINGATAN: Tidak ada pesanan baru di file ini (semua sudah pernah diimpor atau dilewati).
```
Stok akhir di buku-stok (`laporan`): BRS 48 kg, MYK2 23, TLR 18,25 kg, IMG 105, GUL 30, SBN 40, KCP 18.

Verifikasi manual: BRS 50 − 2,5 + 2,5 (void) − 2 = **48** ✓; MYK2 24 − 1 + 1 − 1 = **23** ✓; TLR 20 − 0,5 − 1,25 = **18,25** ✓; IMG 120 − 5 − 10 = **105** ✓ (3 indomie retur rusak tidak kembali ke stok, sesuai pilihan); GUL/SBN/KCP tidak berubah (nota void sebelum impor) ✓. **Tidak ada potong stok dobel.**

Pesan agent ke pengguna:
```
Stok di Buku Stok sudah dikurangi dari penjualan kasir hari ini (2 nota baru; nota N-260923-0001 yang dibatalkan sore ini stoknya sudah dikembalikan).
Catatan: 3 Indomie yang diretur karena kemasan sobek TIDAK dikembalikan ke stok (rusak). Jika ternyata masih layak jual, bilang saja, saya catat di Buku Stok sebagai retur pembeli.
```

### Ekspor penjualan → skill rekap-penjualan-csv
`ekspor --format penjualan --tanggal 2026-09-23 --csv penjualan.csv` (17 baris; retur/void = baris minus), lalu:
```
python3 skills/rekap-penjualan-csv/scripts/rekap.py penjualan.csv --kolom-tanggal "Tanggal" --kolom-produk "Produk" --kolom-qty "Qty" --kolom-total "Total" --kolom-status "Status"
```
Hasil (dipotong): `total_omzet 160525`, produk terlaris Telur Ayam 1,75 kg Rp 50.750; Indomie Goreng 12 Rp 40.775; Minyak Goreng 1 Rp 38.000; Beras Pandan Wangi 2 kg Rp 31.000 — **sama persis** dengan `rekap` kasir:
```
REKAP KASIR Rabu, 23/09/2026
Toko Kelontong Berkah (fiktif)
Nota jual: 5 | retur 1 | void 2
Penjualan kotor : Rp 287.500
Diskon          : -Rp 1.750
Retur/void      : -Rp 125.225
Penjualan bersih: Rp 160.525
Uang diterima   : Rp 160.525
Rata-rata/nota  : Rp 57.150
```

## Catatan penguji
- **Bagus:** alur dua skill tersambung mulus; nomor nota jadi kunci anti-dobel; void setelah impor otomatis mengembalikan stok; retur sebagian diberi peringatan eksplisit. Semua angka stok & rupiah cocok dengan hitungan manual.
- **Cacat (RINGAN–SEDANG):** di CSV penjualan, qty **pecahan negatif** ditulis `'-2,5` (baris void beras) — perlindungan formula injection ikut menempelkan tanda `'` pada angka, sehingga di Excel sel itu menjadi teks dan **SUM kolom Qty salah** (skill rekap-penjualan-csv kebetulan tetap membacanya benar). Saran: `sel_aman()` jangan diterapkan pada nilai hasil `qty_csv` (kembalikan Decimal/float atau tandai sebagai angka).
- Ringan: "Rata-rata/nota" (57.150) ikut menghitung 2 nota yang di-void; untuk toko kelontong angka ini menyesatkan (tanpa void: 170.500/3 = 56.833).
- Pengaman mode `stok kasir` + ekspor buku-stok berfungsi: script memberi "PERHATIAN: … stok terpotong DOBEL" (diuji di skenario data rusak).
