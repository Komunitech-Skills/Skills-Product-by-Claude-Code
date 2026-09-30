# Skenario 09 — Input tidak lengkap: URL/token belum diset (uji independen)

**Penguji:** agent penguji independen (Claude Code, bukan pembuat), 2026-09-30 ±19:55–21:00 WIB. **Kanboard v1.2.54 asli** di-clone sendiri oleh penguji (tag git resmi `v1.2.54`, commit `9ce6a5e`), dijalankan `APP_VERSION=v1.2.54 php -S 127.0.0.1:8090` (PHP 8.4.19 + SQLite), database BARU milik penguji. Akun uji buatan penguji: `sari` (Manajer), `dimas` (Pengguna), `rina` (Pengguna). Token pribadi dibuat acak oleh penguji dan ditulis ke kolom `api_access_token` (setara tombol "Generate token baru"), disimpan di file kunci izin 600 dan dipakai lewat `KANBOARD_KUNCI_FILE` — token tidak pernah tampil. Server tiruan pembuat **tidak** dipakai. Data fiktif. `kanboard.py` = `python3 scripts/kanboard.py`; `(kode keluar N)` ditambahkan pembungkus uji.

Setiap perintah dijalankan dengan `env -i` (tanpa ENV lain) dan HOME baru yang kosong, kecuali ENV yang ditulis di baris `$`.

## Permintaan pengguna
> "Cek Kanboard saya dong, terus tambahin kartu order baru." (belum pernah menyimpan token, alamat belum diatur)

## Log
```
## Belum ada kunci & URL (HOME baru, tanpa ENV)
$ kanboard.py cek
GAGAL: File kunci (file kunci default) tidak ditemukan: <folder-uji>/home2/.komunitech/kanboard-kunci.json
SARAN: Pengguna menjalankan SENDIRI di terminalnya: python3 scripts/kanboard.py simpan-kunci (lihat docs/panduan-kanboard.md bagian 5). Jangan tempel token di chat.
(kode keluar 3)
## Kunci ada tapi Kanboard di port default 8080 (mati)
$ KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py cek
GAGAL: Kanboard di http://127.0.0.1:8080 tidak bisa dihubungi ([Errno 111] Connection refused).
SARAN: Pastikan Kanboard menyala (docs/panduan-kanboard.md bagian 3) dan alamatnya benar - buka alamat itu di browser.
(kode keluar 4)
## URL benar tapi token salah
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/salah.json kanboard.py daftar-papan
GAGAL: 401 dari Kanboard: nama pengguna atau token salah.
SARAN: Cek token di Kanboard (Profil saya > API, atau Pengaturan > API untuk 'jsonrpc'), lalu simpan ulang: simpan-kunci --ya. Akun dengan 2FA wajib memakai token, bukan sandi.
(kode keluar 5)
## File kunci rusak & izin longgar
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/rusak.json kanboard.py cek
PERINGATAN: file <folder-uji>/rahasia/rusak.json bisa dibaca pengguna lain. Jalankan: chmod 600 <folder-uji>/rahasia/rusak.json
GAGAL: File kunci (ENV KANBOARD_KUNCI_FILE) rusak: <folder-uji>/rahasia/rusak.json
SARAN: Simpan ulang dengan 'simpan-kunci --ya'.
(kode keluar 3)
## Hanya ENV user tanpa token
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_USER=sari kanboard.py cek
GAGAL: File kunci (file kunci default) tidak ditemukan: <folder-uji>/home2/.komunitech/kanboard-kunci.json
SARAN: Pengguna menjalankan SENDIRI di terminalnya: python3 scripts/kanboard.py simpan-kunci (lihat docs/panduan-kanboard.md bagian 5). Jangan tempel token di chat.
(kode keluar 3)
## tambah-kartu tanpa --papan / tanpa judul
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py tambah-kartu --judul Order baru
GAGAL: Sebutkan papannya: --papan "nama atau id" (lihat daftar-papan).
(kode keluar 2)
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py tambah-kartu --papan Mekar
GAGAL: Judul kartu wajib diisi (maks 200 karakter).
(kode keluar 2)
## tenggat tidak dikenal / jam tidak valid
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py tambah-kartu --papan Mekar --judul X --tenggat secepatnya
GAGAL: Tenggat tidak dikenali: 'secepatnya'.
SARAN: Format yang didukung: 'hari ini', 'besok', 'lusa', 'N hari lagi', nama hari ('Jumat', 'Jumat depan'), 'minggu depan', 'akhir bulan', 'awal bulan depan', '25/10' (tanggal/bulan), '25/10/2026', '25 Oktober 2026', '2026-10-25'; boleh ditambah 'jam 14:00'.
(kode keluar 2)
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py tambah-kartu --papan Mekar --judul X --tenggat besok jam 25:00
GAGAL: Jam tidak valid di tenggat: 'besok jam 25:00'
(kode keluar 2)
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py tambah-kartu --papan Mekar --judul X --tenggat 31/02/2026
GAGAL: Tenggat tidak dikenali: '31/02/2026'.
SARAN: Format yang didukung: 'hari ini', 'besok', 'lusa', 'N hari lagi', nama hari ('Jumat', 'Jumat depan'), 'minggu depan', 'akhir bulan', 'awal bulan depan', '25/10' (tanggal/bulan), '25/10/2026', '25 Oktober 2026', '2026-10-25'; boleh ditambah 'jam 14:00'.
(kode keluar 2)
## URL tanpa skema / papan tidak ada
$ KANBOARD_URL=127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py cek
GAGAL: Alamat Kanboard '127.0.0.1:8090' tidak valid. Contoh: http://127.0.0.1:8080
(kode keluar 2)
$ KANBOARD_URL=http://127.0.0.1:8090 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py kolom --papan Gudang
GAGAL: Papan 'Gudang' tidak ditemukan. Papan yang ada: Produksi Konveksi Mekar Jaya, Proyek Studio Desain Kirana.
(kode keluar 2)
## Kanboard membalas bukan JSON (alamat menunjuk aplikasi lain): python http.server
$ KANBOARD_URL=http://127.0.0.1:8095 KANBOARD_KUNCI_FILE=<folder-uji>/rahasia/sari.json kanboard.py cek
GAGAL: Kanboard membalas galat server 501.
SARAN: Cek log server Kanboard; coba lagi beberapa saat.
(kode keluar 4)
```

Pemeriksaan token: jumlah kemunculan token asli di log ini = **0**.

## Jawaban agent yang diharapkan (sesuai SKILL.md)
"Kanboard Anda belum terhubung karena kunci API belum disimpan. Langkahnya (sekali saja, **di terminal Anda sendiri**, jangan tempel token di chat): 1) Buka Kanboard → avatar → Profil saya → API → Generate token baru; 2) jalankan `python3 <folder-skill>/scripts/kanboard.py simpan-kunci`, isi nama pengguna lalu tempel token; 3) bila Kanboard tidak di `http://127.0.0.1:8080`, beri tahu alamatnya. Setelah itu saya cek lagi. Untuk kartu barunya, sebutkan juga: papan mana, judul, tenggat, PIC."

## Penilaian
- Kode keluar sesuai tabel SKILL.md: 3 (kunci tidak ada/rusak), 4 (Kanboard mati), 5 (401), 2 (input/alamat) ✔. Setiap GAGAL disertai SARAN yang bisa diikuti orang awam ✔. File kunci izin 644 diberi PERINGATAN chmod ✔.
- **Rendah:** `KANBOARD_USER` diisi tanpa `KANBOARD_TOKEN` → diam-diam jatuh ke file default; pesan tidak menyebut bahwa ENV tidak lengkap.
- **Rendah:** alamat yang menunjuk aplikasi lain (server web biasa, membalas 501) dilaporkan sebagai "galat server" (kode 4), bukan "alamat ini bukan Kanboard" — saran kurang tepat.
- `31/02/2026` dan `besok jam 25:00` ditolak dengan jelas ✔.
