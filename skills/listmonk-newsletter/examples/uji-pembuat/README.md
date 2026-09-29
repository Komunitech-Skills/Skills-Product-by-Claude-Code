# Uji pembuat (bukan HASIL-UJI resmi)

- **listmonk 6.2.0 asli** (`listmonk/listmonk:v6.2.0`, digest label revision `ef0a758`, + `postgres:17`), port `127.0.0.1`, SMTP penampung lokal (tidak ada email keluar ke internet), data fiktif `example.test`. Tanggal 29 Sep 2026.
- Pengguna API berperan terbatas (`subscribers:get/manage/import`, `campaigns:*`, `lists:*`, `templates:get`, `media:*`); tanpa izin `subscribers:sql_query` (pencarian memakai parameter `search`).
- Dijalankan: `cek`, `daftar-list`, `buat-list`, `periksa-kontak`, `impor` (ditolak/`--ya`), `kirim-optin`, konfirmasi opt-in (klik tautan di email), `buat-kampanye`, `uji-kirim`, `kirim`/`jadwal` (ditolak & disetujui), `batalkan` (jadwal), `statistik --tautan` (buka + klik nyata), `hapus-pelanggan`, server mati, alamat internet tanpa izin.
- Temuan yang mengubah desain: (1) uji kirim hanya untuk alamat yang sudah jadi pelanggan; (2) `query` butuh izin SQL; (3) klik hanya dilacak bila tautan berakhiran `@TrackLink`; (4) pembatalan jadwal = kembali ke draf; (5) impor `unconfirmed` tidak mengirim email opt-in otomatis.
- Uji regresi otomatis: `python3 tests/uji_regresi.py` (23 skenario dengan server tiruan).
- **Belum diuji:** SMTP sungguhan, inbox Gmail/Yahoo, Windows/macOS, versi listmonk lain, impor `.xlsx` sungguhan dari Excel (diuji dengan berkas .xlsx buatan test), ribuan kontak. **PERLU UJI NYATA** oleh penguji independen dan pemilik (`docs/uji-platform.md`).
