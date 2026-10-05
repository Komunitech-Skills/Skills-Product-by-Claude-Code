# 09 — Uji independen: input tidak lengkap / kredensial belum diatur (skenario 4)

> **Sumber keluaran:** penguji independen, 30 Sep 2026, Odoo Community ASLI 18.0 & 19.0 lokal. HOME diganti folder kosong. Path disingkat.

**Permintaan pengguna (baru beli, belum setup):** "Cek penjualan Odoo saya hari ini dong."

```
$ python3 scripts/odoo.py penjualan --url http://localhost:8070
GAGAL: Kunci API Odoo belum diatur.
Saran: Buat kunci di Odoo (klik foto profil > Preferensi/My Profile > Keamanan Akun > Kunci API Baru), lalu jalankan SENDIRI di terminal: python3 scripts/odoo.py simpan-kunci . Jangan tempel kunci di chat.
(kode keluar: 5)
```
Respons agent yang benar menurut SKILL: jelaskan langkah buat kunci, minta pengguna menjalankan `simpan-kunci` sendiri di terminal, **tidak** meminta kunci ditempel di chat, lalu `cek`.

| Kasus | Keluaran (dipotong) | Kode | Nilai |
|---|---|---|---|
| Odoo 18 tanpa `--db/--login` | "Nama database Odoo belum diatur (wajib untuk XML-RPC)." + cara melihat nama db | 2 | Benar |
| Kunci salah (Odoo 18) | "Login ke Odoo ditolak (kunci API, login, atau nama database salah)." | 5 | Benar, kunci tak tercetak |
| Kunci salah (Odoo 19, `--json`) | `{"ok": false, "kode_keluar": 5, "galat": "Kunci API ditolak Odoo (401: Invalid apikey)."...}` | 5 | Benar (pesan 401 asli Odoo) |
| Kunci Odoo 18 dipakai ke Odoo 19 | "Kunci API ditolak Odoo (401: Invalid apikey)." | 5 | Benar |
| File kunci izin 644 | "File kunci ... bisa dibaca pengguna lain. Amankan dulu: chmod 600 ..." | 5 | Benar |
| Paksa `--protokol json2` ke Odoo 18 | "Protokol JSON-2 baru ada di Odoo 19 ke atas (server ini 18.0-20260926)." | 4 | Benar |
| Port mati (8099) | "Odoo di http://localhost:8099 tidak bisa dihubungi ([Errno 111] Connection refused)." | 3 | Benar |
| `simpan-kunci` lewat stdin | "Kunci disimpan di …/odoo-kunci.txt" (tanpa potongan kunci); folder 700, file 600 | 0 | Benar |
| `odoo.json` berisi `api_key` | "PERINGATAN: … field 'api_key' (mirip rahasia). DIABAIKAN." Nilai kunci tidak tercetak | 0 | Benar |
| Harga `62,500` | "harga '62,500' ambigu … Tulis 62500 atau 62.500." | 2 | Benar |
| Jumlah `abc` | "jumlah 'abc' bukan angka biasa" | 2 | Benar |
| Produk `a` | "cocok ke beberapa produk: #2 … #1 … #3 … #4 … Tanyakan yang mana, lalu pakai #id." | 7 | Benar |
| Pelanggan ID 999 | "Pelanggan ID 999 tidak ditemukan. Cari dulu dengan `pelanggan cari`." | 2 | Benar |

Pemindaian kebocoran: 22 berkas keluaran (teks, `--json`, stderr, log server pengalih) diperiksa terhadap 8 kunci API asli (utuh, 12 karakter awal, dan 12 karakter akhir) → **0 kebocoran**.
