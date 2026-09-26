# Uji A/B — Agent TANPA skill vs DENGAN skill (skenario 1: ringkasan stok opname)

**Permintaan pengguna:** "Grist saya file-nya di `toko-berkah-jaya.grist`, ringkas stok yang
menipis/habis dong."

## Tanpa skill `grist-usaha`
Agent umum (tanpa panduan skill ini) tidak tahu bahwa file `.grist` adalah SQLite biasa dengan
tabel metadata `_grist_Tables`/`_grist_Tables_column`, atau di mana letak file itu biasanya
disimpan (Desktop vs Docker). Perilaku yang realistis:
- Kemungkinan besar mencoba membuka file sebagai spreadsheet biasa (Excel/CSV) dan gagal, atau
  menyarankan pengguna membuka Grist secara manual dan membaca layarnya sendiri.
- Bila mencoba membaca sebagai SQLite tanpa tahu skema, harus menebak nama tabel data
  (`sqlite_master` mencantumkan puluhan tabel `_grist*`/`_gristsys*` internal bercampur dengan
  tabel data pengguna) — berisiko salah baca tabel metadata sebagai data, atau butuh beberapa
  putaran tanya-jawab untuk pengguna awam yang juga tidak tahu nama tabelnya.
- Tidak ada aturan baca **read-only** yang eksplisit — risiko kecil tapi nyata agent mencoba
  `sqlite3` tanpa `mode=ro`, yang bisa memodifikasi file dokumen Grist pengguna secara tidak
  sengaja (mis. lock file/rollback journal) bila prosesnya terganggu.
- Tidak tahu rumus `sisa = masuk - keluar` dan aturan "MENIPIS hanya bila BatasMinimum > 0" —
  harus menebak logika bisnis pengguna dari nol tiap sesi.

## Dengan skill `grist-usaha`
```
python3 scripts/grist.py daftar-tabel toko-berkah-jaya.grist
python3 scripts/grist.py ringkasan toko-berkah-jaya.grist StokOpname --n 8
```
→ langsung dapat daftar tabel data pengguna yang benar (memfilter tabel internal `_grist*` lewat
metadata resmi), lalu ringkasan lengkap (jumlah baris, kolom + tipe + status rumus, contoh data)
dalam satu perintah, dijamin read-only (`PRAGMA query_only=1` + `mode=ro` di URI SQLite,
diverifikasi test `test_benar_benar_read_only_tidak_menulis`).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Tahu file `.grist` = SQLite & skema metadatanya | Tidak (harus menebak/riset ulang) | Ya, langsung |
| Risiko menulis tidak sengaja ke file pengguna | Ada (tidak ada jaminan read-only) | Tidak ada (dijamin & diuji) |
| Waktu ke jawaban | Berputar-putar / butuh beberapa pertanyaan | 2 perintah, langsung |
| Filter tabel internal Grist vs data pengguna | Manual, rawan salah | Otomatis & benar |

## Kesimpulan
Skill memberi nilai tambah **jelas dan nyata**: bukan cuma kemasan instruksi, tapi mencegah
risiko konkret (menulis tidak sengaja ke dokumen produksi pengguna) dan mempercepat jawaban dari
berputar-putar/menebak menjadi 2 perintah pasti.
