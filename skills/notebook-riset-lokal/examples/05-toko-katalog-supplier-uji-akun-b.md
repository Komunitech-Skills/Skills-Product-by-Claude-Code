# 05 — Skenario normal 3: pemilik toko membandingkan katalog 3 supplier

**Diuji terhadap Open Notebook 1.14.0 asli.** Pemilik toko ingin mengumpulkan tautan katalog 3 supplier lalu membandingkan.

## Langkah 1 — buat notebook
```
$ python3 scripts/notebook.py buat-notebook --nama "Katalog Supplier" --deskripsi "Perbandingan 3 supplier kemasan" --ya
{"dibuat": true, "id": "notebook:w8stc3pfdq7lc6fr24uz", "nama": "Katalog Supplier"}
```
✅ Berhasil.

## Langkah 2 — tambah sumber tipe `link` (katalog supplier A) — ❌ GAGAL
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Katalog Supplier" --tipe link --sumber-url "https://example.com/katalog-a" --ya
GALAT: 422: [{'type': 'missing', 'loc': ['body', 'type'], 'msg': 'Field required', 'input': None}]
```
❌ **Bug #1 yang sama** (lihat `03-...` dan `HASIL-UJI.md`) — kali ini dikonfirmasi untuk tipe `link`, bukan cuma `teks`. Jadi **kedua** tipe sumber yang didukung skill (`link` dan `teks`) gagal 100% terhadap server v1.14.0 asli. Pemilik toko tidak bisa mengumpulkan katalog supplier manapun lewat skill ini sampai bug ini diperbaiki.

## Dampak untuk skenario ini
Tanpa perbaikan `cmd_tambah_sumber` (kirim `multipart/form-data`, bukan JSON, ke `POST /api/sources`), skenario "kumpulkan 3 katalog supplier lalu bandingkan" **tidak bisa dijalankan sama sekali** lewat skill — pemilik toko harus diarahkan manual ke `http://127.0.0.1:8502` untuk menambah link satu-satu, yang justru meniadakan nilai jual utama skill ("cukup ketik permintaan biasa").

## Pratinjau (bagian yang tetap berfungsi)
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Katalog Supplier" --tipe link --sumber-url "https://example.com/katalog-a"
[PRATINJAU - belum dikirim] Akan menambah sumber ke notebook
  notebook_id: notebook:w8stc3pfdq7lc6fr24uz
  sumber: {'notebooks': ['notebook:w8stc3pfdq7lc6fr24uz'], 'type': 'link', 'url': 'https://example.com/katalog-a'}
  catatan: Tambahkan --ya untuk benar-benar menambah. ...
```
Pratinjau (tanpa `--ya`) tetap benar — masalahnya murni di pengiriman `--ya` ke server sungguhan.
