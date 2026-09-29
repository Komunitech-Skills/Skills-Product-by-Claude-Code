# 11 - Data rusak: kunci salah, server mati, HTTP, 500, redirect

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```

$ kunci salah
PERINGATAN: file kunci-salah.txt bisa dibaca pengguna lain. Jalankan: chmod 600 kunci-salah.txt
GALAT: Kunci API ditolak Fider (salah/sudah diganti). Buat kunci baru di Fider (Settings > API Key) lalu jalankan simpan-kunci --ya.
kode=3
$ kunci salah (ENV)
GALAT: Kunci API berisi spasi/baris baru; simpan ulang dengan simpan-kunci --ya.
kode=3
$ tanpa kunci (HOME kosong)
GALAT: Kunci API Fider belum ada. Jalankan SENDIRI: python3 scripts/fider.py simpan-kunci (kunci dibuat di Fider: menu profil > Settings > API Key).
kode=3
$ server mati (port 3999)
GALAT: Fider tidak terjangkau di http://localhost:3999 ([Errno 111] Connection refused). Pastikan Fider menyala (docker compose ps) dan alamatnya benar.
kode=4
$ host tak ada
GALAT: Fider tidak terjangkau di https://tidak-ada-host.invalid (Tunnel connection failed: 502 Bad Gateway). Pastikan Fider menyala (docker compose ps) dan alamatnya benar.
kode=4
$ HTTP internet
GALAT: Alamat Fider di internet wajib HTTPS (kunci API tidak boleh lewat HTTP polos).
kode=2
$ HTTP host bernama 10.x (bypass HTTPS?)
GALAT: Fider menjawab galat 503.
kode=5
$ url sandi
GALAT: Alamat Fider tidak boleh memuat sandi di dalamnya.
kode=2
$ 500 html
GALAT: Fider menjawab galat 500.
kode=5
$ 200 html
GALAT: Jawaban Fider bukan JSON (mungkin alamat salah atau ada proxy di depannya).
kode=5
$ 429
GALAT: Fider membatasi kecepatan permintaan (429). Tunggu semenit lalu ulangi.
kode=5
$ redirect
GALAT: Fider mengalihkan (redirect) permintaan; ditolak demi keamanan kunci. Periksa alamat (mungkin harus https://).
kode=4
$ bentuk jawaban asing
GALAT: Bentuk jawaban daftar pos tidak dikenal (versi Fider berbeda?).
kode=5
```
