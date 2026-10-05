# Contoh 4 — Input tidak lengkap / ambigu

## 4a. Tidak menyebut dokumen mana, dan ada 2 dokumen mirip namanya

> **Pengguna:** "Buatkan tabel stok di Grist usaha aku"

Kunci API yang tersimpan ternyata bisa mengakses 2 dokumen yang namanya mengandung kata "usaha":

```
$ python3 grist.py buat-tabel stok --dokumen usaha --ya
GAGAL: Ada 2 dokumen bernama mirip 'usaha'. Sebutkan salah satu docId ini:
  - Data Usaha Saya (docId: docABC123, workspace: Home)
  - Data Usaha Cabang (docId: docXYZ789, workspace: Home)
(kode keluar: 2)
```

**Balasan agent (tanya sekali, satu pesan):**

> Kunci Grist Anda bisa mengakses 2 dokumen yang namanya mirip: **"Data Usaha Saya"** dan
> **"Data Usaha Cabang"**. Tabel stoknya mau dibuat di dokumen yang mana?

## 4b. Nama dokumen salah ketik / belum ada

> **Pengguna:** "Buat tabel stok di dokumen 'Toko Saya'" *(padahal nama sebenarnya beda)*

```
$ python3 grist.py buat-tabel stok --dokumen "Toko Saya" --ya
GAGAL: Dokumen 'Toko Saya' tidak ditemukan. Dokumen yang bisa diakses kunci ini:
  - Data Usaha Saya (workspace: Home, org: docs)
  - Data Usaha Cabang (workspace: Home, org: docs)
(kode keluar: 2)
```

**Balasan agent:**

> Tidak ada dokumen bernama "Toko Saya" yang bisa diakses kunci API Anda. Yang saya temukan:
> **Data Usaha Saya** dan **Data Usaha Cabang**. Maksudnya yang mana? (Atau, kalau dokumennya
> baru saja dibuat, pastikan sudah menyimpan kunci API yang benar — lihat
> `docs/panduan-grist.md` bagian 6.)

## 4c. Minta "buatkan tabel" tanpa bilang jenisnya apa

> **Pengguna:** "Bantu aku rapikan data di Grist dong"

Terlalu umum untuk langsung dieksekusi — agent tidak menebak, tapi juga tidak diam. Balasan
(satu pesan, beberapa pertanyaan singkat sekaligus, sesuai prinsip "instan" di CLAUDE.md):

> Boleh, supaya pas: (1) datanya tentang apa — pelanggan, pesanan, stok, atau jadwal konten
> sosmed? (2) sudah ada tabelnya di Grist atau perlu dibuatkan baru? (3) nama dokumen Grist-nya
> apa? Kalau mau cepat, saya asumsikan pola standar untuk jenisnya lalu tinggal dikonfirmasi.

## 4d. Nama kolom CSV tidak sah untuk Grist, langsung mau diimpor

> **Pengguna:** *(mengirim CSV dengan header "Nama Pelanggan", "No. HP")* "impor ini ke Grist ya"

```
$ python3 grist.py impor-csv daftar.csv --dokumen "Data Usaha Saya" --tabel Pelanggan --ya
GAGAL: Nama kolom 'Nama Pelanggan' tidak sesuai aturan Grist (harus diawali huruf, hanya
huruf/angka/garis bawah). Jalankan 'bersihkan-csv' dulu.
(kode keluar: 2)
```

**Balasan agent:** menjalankan `bersihkan-csv` dulu tanpa perlu ditanya lagi (ini bagian dari
alur kerja normal, bukan input yang benar-benar kurang — lihat Contoh 3), baru menunjukkan
pratinjau `impor-csv`.
