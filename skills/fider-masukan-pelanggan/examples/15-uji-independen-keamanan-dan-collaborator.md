# 15 - Keamanan dan Collaborator

Penguji independen, Fider v0.38.0 ASLI (Docker+PostgreSQL 17), 2026-09-29. Data fiktif. Kunci tidak dicetak.

```
impor key.txt -> pratinjau memuat kunci? jumlah kemunculan: 1
cek --kunci-file /etc/hostname (kunci dari file sembarang; terkirim ke server lokal):
GALAT: Kunci API ditolak Fider (salah/sudah diganti). Buat kunci baru di Fider (Settings > API Key) lalu jalankan simpan-kunci --ya.
GALAT: Waktu habis/jaringan putus saat menghubungi Fider: timed out
real	0m20.099s
    raise EOFError
EOFError
Alamat tersimpan: http://10.contoh.com
100:    if os.environ.get("FIDER_API_KEY", "").strip():
101:        return os.environ["FIDER_API_KEY"].strip()
102:    if os.environ.get("FIDER_API_KEY_FILE"):
103:        return _baca_file(os.path.expanduser(os.environ["FIDER_API_KEY_FILE"]), "FIDER_API_KEY_FILE")
120:    if os.environ.get("FIDER_URL", "").strip():
121:        return os.environ["FIDER_URL"].strip().rstrip("/"), True
SELESAI: tag pembayaran dipasang pada pos #5.
SELESAI: #6 digabung ke #5. Suara #5 sekarang 2.
SELESAI: komentar ditulis di pos #5.
GALAT: Fider menjawab galat 400: This has already been posted before.
```
