# Skenario 04 — Input buruk & galat (Dolibarr asli 22.0.4)

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-24. Dolibarr **asli** 22.0.4 di container Linux (PHP 8.4, MariaDB 10.11), zona PHP Asia/Jakarta. Data fiktif.

Semua kasus berhenti dengan pesan bahasa awam + saran, **tanpa menulis apa pun** dan tanpa menampilkan kunci API.

```
$ env DOLIBARR_API_KEY=kunci-lama-yang-sudah-diganti python3 scripts/dolibarr.py cek
GAGAL: Kunci API ditolak Dolibarr (401). Kunci salah, sudah diganti, atau user-nya nonaktif.
Saran: Buat ulang kunci di Dolibarr (Pengguna & Grup > user API > Token for API) lalu simpan lagi dengan `simpan-kunci`.
(kode keluar 5)

$ env DOLIBARR_URL=http://localhost:8099/dolibarr python3 scripts/dolibarr.py laporan-harian
GAGAL: Dolibarr di http://localhost:8099/dolibarr tidak bisa dihubungi ([Errno 111] Connection refused).
Saran: Nyalakan Dolibarr dulu (Windows: menu Start > Dolibarr > Tools > Start DoliWamp server), lalu buka http://localhost:8099/dolibarr di browser untuk memastikan.
(kode keluar 3)

$ python3 scripts/dolibarr.py stok
GAGAL: Modul 'API / Web services (REST server)' di Dolibarr belum aktif.
Saran: Masuk Dolibarr sebagai admin > Pengaturan > Modul/Aplikasi > aktifkan 'API / Layanan Web (server REST)'. Lihat docs/panduan-dolibarr.md.
(kode keluar 4)

$ env DOLIBARR_URL=http://192.168.1.20/dolibarr python3 scripts/dolibarr.py cek
GAGAL: Alamat 192.168.1.20 bukan komputer ini. Demi keamanan, skill ini hanya bicara dengan Dolibarr lokal.
Saran: Jika Dolibarr memang di komputer/server lain milik Anda, ulangi dengan --izinkan-url-luar (atau ENV DOLIBARR_IZINKAN_URL_LUAR=1) dan pastikan memakai https://.
(kode keluar 2)

$ env DOLIBARR_URL=http://tokoku.contoh.id/dolibarr python3 scripts/dolibarr.py cek --izinkan-url-luar
GAGAL: Alamat internet wajib https:// agar kunci API tidak bisa disadap.
(kode keluar 2)

$ python3 scripts/dolibarr.py invoice buat --pelanggan 1 --item Kopi|dua|85000
GAGAL: Item 1: jumlah 'dua' bukan angka.
(kode keluar 2)

$ python3 scripts/dolibarr.py invoice buat --pelanggan 1 --item Kopi|2
GAGAL: Item 1: harga wajib diisi untuk barang/jasa tanpa kode produk.
(kode keluar 2)

$ python3 scripts/dolibarr.py invoice buat --pelanggan 99 --item Kopi|2|85000
GAGAL: Pelanggan ID 99 tidak ada. Cari dulu: pelanggan cari "nama"
(kode keluar 2)

$ python3 scripts/dolibarr.py invoice buat --pelanggan 1 --item @TIDAKADA|2
GAGAL: Produk dengan kode 'TIDAKADA' tidak ada di Dolibarr.
(kode keluar 2)

$ python3 scripts/dolibarr.py pelanggan cari a
GAGAL: Kata pencarian terlalu pendek (minimal 2 huruf/angka).
(kode keluar 2)

$ python3 scripts/dolibarr.py pelanggan tambah --nama Budi --telepon 123
GAGAL: Nomor telepon '123' tidak wajar (8-15 angka).
(kode keluar 2)

$ python3 scripts/dolibarr.py laporan-harian --tz Europe/London
GAGAL: Zona waktu 'Europe/London' tidak dikenal. Pakai WIB, WITA, atau WIT.
(kode keluar 2)
```

Kasus lain yang diuji di Dolibarr asli: modul Invoice dimatikan → Dolibarr menjawab **403** (bukan 501); `cek` menampilkan "TIDAK BISA DIBACA (modul belum aktif, atau user API tidak punya hak baca)" dan `laporan-harian` tetap mengirim bagian stok. Pengalihan alamat (redirect), file kunci berizin longgar, URL berisi sandi, dan draf ganda diuji di `tests/uji_regresi.py` (server tiruan).
