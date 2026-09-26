# Contoh 3 — Bersihkan CSV lalu impor ke tabel Grist yang sudah ada

**Konteks uji:** `bersihkan-csv` dijalankan sungguhan dengan file CSV nyata (bukan simulasi).
`impor-csv` dipanggil ke **server Grist TIRUAN** yang sama seperti Contoh 2 (belum ke server
sungguhan).

## Percakapan

> **Pengguna:** "Ini ada file pelanggan baru dari pameran kemarin (`pelanggan-baru.csv`), tolong
> masukkan ke Grist tabel Pelanggan."

File asli `pelanggan-baru.csv`:
```
Nama,Telepon,Kota,Sumber
Toko Sumber Rejeki,0821-7777-6666,Yogyakarta,Marketplace
Bengkel Jaya Motor,+62 815-2222-3333,Solo,Referensi
```

Agent membersihkan dulu (merapikan nama kolom agar sah untuk Grist, angka Rupiah bila ada):

```
$ python3 grist.py bersihkan-csv pelanggan-baru.csv
SELESAI membersihkan 'pelanggan-baru.csv' -> 'pelanggan-baru-bersih.csv'
Baris data: 2
Kolom (nama asli -> nama Grist, jenis):
  - 'Nama' -> Nama  (Text)
  - 'Telepon' -> Telepon  (Text)
  - 'Kota' -> Kota  (Text)
  - 'Sumber' -> Sumber  (Text)
Angka Rupiah/desimal dirapikan jadi angka polos (mis. 'Rp 1.234.567,89' -> 1234567.89).
Periksa dulu file hasil sebelum diimpor. Lanjut: 'impor-csv' (perlu REST API) atau
seret file ini ke Grist lewat menu Import (selalu tersedia, tanpa API).
```

Kolom sudah cocok persis dengan tabel `Pelanggan` yang sudah ada (Contoh 2). Agent menunjukkan
pratinjau impor, minta konfirmasi, baru mengeksekusi:

```
$ python3 grist.py impor-csv pelanggan-baru-bersih.csv --dokumen "Data Usaha Saya" --tabel Pelanggan
PRATINJAU — impor 2 baris dari 'pelanggan-baru-bersih.csv' ke tabel 'Pelanggan' (docId: docABC123):
Kolom: Nama, Telepon, Kota, Sumber
  contoh: {'Nama': 'Toko Sumber Rejeki', 'Telepon': '0821-7777-6666', 'Kota': 'Yogyakarta', 'Sumber': 'Marketplace'}
  contoh: {'Nama': 'Bengkel Jaya Motor', 'Telepon': '+62 815-2222-3333', 'Kota': 'Solo', 'Sumber': 'Referensi'}

Catatan: tabel & kolom di atas HARUS SUDAH ADA di Grist (buat dulu dengan 'buat-tabel'
atau manual di Grist). Perintah ini hanya MENAMBAH baris baru, tidak membuat kolom.

Belum diimpor. Jalankan ulang dengan --ya setelah pengguna menjawab 'ya'.
```

> **Pengguna:** "ya, masukkan"

```
$ python3 grist.py impor-csv pelanggan-baru-bersih.csv --dokumen "Data Usaha Saya" --tabel Pelanggan --ya
... (pratinjau sama) ...
BERHASIL: 2 baris ditambahkan ke tabel 'Pelanggan'.
```

**Balasan agent:**

> 2 pelanggan baru (Toko Sumber Rejeki, Bengkel Jaya Motor) sudah masuk ke tabel Pelanggan di
> Grist. Kolom rumus **WA Rapi** otomatis terisi untuk baris baru ini juga.

## Skenario angka Rupiah (uji terpisah, lihat juga `uji-pembuat/UJI-PEMBUAT-v1.0.0.md`)
File dengan kolom harga campuran format:
```
Tanggal Pesanan,Nama Pembeli,Barang,Qty,Harga Satuan (Rp),Diskon (%)
2026-09-20,Toko Maju Jaya,Kopi Robusta 1kg,3,"Rp 85.000,00",0
2026-09-21,Warung Bu Sari,Gula Aren 1kg,2,"32.500",5
2026-09-22,CV Sinar Abadi,Cup Kertas 12oz,50,"1.250",0
```
Hasil `bersihkan-csv` (dijalankan sungguhan):
```
Kolom (nama asli -> nama Grist, jenis):
  - 'Tanggal Pesanan' -> TanggalPesanan  (Text)
  - 'Nama Pembeli' -> NamaPembeli  (Text)
  - 'Barang' -> Barang  (Text)
  - 'Qty' -> Qty  (Numeric)
  - 'Harga Satuan (Rp)' -> HargaSatuanRp  (Numeric)
  - 'Diskon (%)' -> Diskon  (Numeric)
```
Isi setelah dibersihkan:
```
TanggalPesanan,NamaPembeli,Barang,Qty,HargaSatuanRp,Diskon
2026-09-20,Toko Maju Jaya,Kopi Robusta 1kg,3,85000,0
2026-09-21,Warung Bu Sari,Gula Aren 1kg,2,32500,5
2026-09-22,CV Sinar Abadi,Cup Kertas 12oz,50,1250,0
```
`Rp 85.000,00`, `32.500`, dan `1.250` semuanya benar dirapikan jadi angka polos (`85000`,
`32500`, `1250`) — walau formatnya berbeda-beda (ada yang pakai `Rp`+koma desimal, ada yang
cuma titik ribuan). **Catatan jujur:** kolom `Tanggal Pesanan` tetap jadi `Text` (bukan `Date`)
karena skrip tidak menebak-nebak format tanggal — agent perlu mengatur tipe kolom `Date` secara
manual di Grist setelah impor, atau menyamakan formatnya lebih dulu bila penting.
