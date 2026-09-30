# Skenario 01 — Konveksi: sambungkan, buat papan produksi, tambah kartu (normal)

**Penguji:** pembuat skill, 2026-09-30. Dijalankan sungguhan terhadap **Kanboard v1.2.54 asli** (kode sumber resmi tag git `v1.2.54`, PHP 8.4 + SQLite, `http://127.0.0.1:8080`, zona waktu aplikasi Asia/Jakarta). Akun AI: `ayu` (peran Manajer) dengan token pribadi yang disimpan lewat `simpan-kunci` (token tidak pernah tampil). Data fiktif. Baris `$` ditampilkan tanpa tanda kutip; saat mengetik sendiri, bungkus nilai yang berisi spasi dengan tanda kutip.

## Permintaan pengguna
> "Saya punya usaha konveksi. Tolong cek Kanboard saya sudah nyambung, buatkan papan produksi, lalu masukkan order seragam SD Harapan 120 pcs, deadline Jumat jam 10, PIC saya (Ayu), catatan DP 50% sudah masuk."

## 1. Cek koneksi
```
$ python3 scripts/kanboard.py cek
KANBOARD TERHUBUNG
Alamat: http://127.0.0.1:8080
Versi: v1.2.54
Mode: token pribadi pengguna 'ayu' (peran app-manager) - hanya papan tempat akun ini jadi anggota.
Zona waktu server Kanboard: Asia/Jakarta
Papan terlihat: 0
(kode keluar 0)
```

## 2. Pratinjau papan (belum menulis)
```
$ python3 scripts/kanboard.py buat-papan --jenis produksi --nama Produksi Konveksi Ayu
PRATINJAU PAPAN BARU: Produksi Konveksi Ayu
Template: produksi - Alur Produksi (konveksi, makanan, kerajinan, percetakan)
Jenis: papan tim (anggota diatur admin di Kanboard)
Kolom:
  1. Order Masuk - Pesanan baru yang sudah dikonfirmasi pelanggan
  2. Siapkan Bahan - Belanja/cek stok bahan baku
  3. Produksi (batas 5 kartu) - Sedang dikerjakan; batasi agar tidak menumpuk
  4. Cek Kualitas - QC sebelum dikemas
  5. Siap Kirim - Sudah dikemas, menunggu kurir/diambil
  6. Selesai - Sudah diterima pelanggan
Belum ada yang dibuat. Simpan ke Kanboard? (ya/tidak) - ulangi dengan --ya bila ya.
(kode keluar 0)
```

Agent menampilkan pratinjau dan bertanya: "Simpan papan ini ke Kanboard? (ya/tidak)". Pengguna: "ya".

## 3. Setelah "ya"
```
$ python3 scripts/kanboard.py buat-papan --jenis produksi --nama Produksi Konveksi Ayu --ya
PAPAN DIBUAT: Produksi Konveksi Ayu (id 1)
Template: produksi - Alur Produksi (konveksi, makanan, kerajinan, percetakan)
Kolom:
  1. Order Masuk
  2. Siapkan Bahan
  3. Produksi
  4. Cek Kualitas
  5. Siap Kirim
  6. Selesai
Buka: http://127.0.0.1:8080/?controller=BoardViewController&action=show&project_id=1
(kode keluar 0)
```

## 4. Kartu: pratinjau, lalu simpan setelah "ya"
```
$ python3 scripts/kanboard.py tambah-kartu --papan Konveksi Ayu --judul Seragam SD Harapan 120 pcs --tenggat Jumat jam 10:00 --ke ayu --catatan DP 50% sudah masuk; ukuran S-M-L terlampir di WA
PRATINJAU KARTU BARU
Papan: Produksi Konveksi Ayu (id 1)
Kolom: Order Masuk
Judul: Seragam SD Harapan 120 pcs
Jatuh tempo: Jumat, 2 Oktober 2026 jam 10:00 WIB
PIC: Ayu Lestari
Catatan: DP 50% sudah masuk; ukuran S-M-L terlampir di WA
Belum disimpan. Simpan ke Kanboard? (ya/tidak) - ulangi dengan --ya bila ya.
(kode keluar 0)
```

```
$ python3 scripts/kanboard.py tambah-kartu --papan Konveksi Ayu --judul Seragam SD Harapan 120 pcs --tenggat Jumat jam 10:00 --ke ayu --catatan DP 50% sudah masuk; ukuran S-M-L terlampir di WA --ya
KARTU DIBUAT: #1
Papan: Produksi Konveksi Ayu (id 1)
Kolom: Order Masuk
Judul: Seragam SD Harapan 120 pcs
Jatuh tempo: Jumat, 2 Oktober 2026 jam 10:00 WIB
PIC: Ayu Lestari
Catatan: DP 50% sudah masuk; ukuran S-M-L terlampir di WA
(kode keluar 0)
```

## Verifikasi independen
Dibaca ulang langsung lewat JSON-RPC (token aplikasi, di luar skill): kartu #1 `date_due` = 2026-10-02 10:00 +07:00, `owner_id` = 3 (Ayu Lestari), kolom "Order Masuk" — cocok dengan pratinjau. Enam kolom papan tampil persis urutan template; batas WIP kolom Produksi = 5.

## Jawaban agent ke pengguna (ringkas)
Kanboard tersambung (v1.2.54). Papan **Produksi Konveksi Ayu** sudah dibuat dengan 6 tahap (Order Masuk → Siapkan Bahan → Produksi [maks 5] → Cek Kualitas → Siap Kirim → Selesai). Kartu **#1 Seragam SD Harapan 120 pcs** masuk ke *Order Masuk*, jatuh tempo Jumat 2 Oktober 2026 jam 10:00 WIB, PIC Ayu Lestari.
