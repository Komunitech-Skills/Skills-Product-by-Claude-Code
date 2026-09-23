# Resep laporan: Stok Menipis

_Salin ke `laporan/RESEP-stok-menipis.md`, isi bagian `<isi>`._

## Jalur utama: pengguna sudah memakai skill `buku-stok`

Tanyakan lebih dulu apakah pengguna sudah memakai skill `buku-stok` (database SQLite lokal,
biasanya di `~/KomunitechData/stok.db`). Kalau **ya**, pakai jalur ini -- **tidak perlu**
`cek_sumber_data.py`/CSV sama sekali; `buku-stok` sudah punya databasenya sendiri.

### Langkah hitung
1. Cek database ada & lihat umur data (HANYA BACA):
   ```bash
   python3 <folder-skill-buku-stok>/scripts/stok.py info --db "<isi, path stok.db>" --json
   ```
   - Kalau `"ok": false` atau file database tidak ditemukan: **jangan lanjut**, katakan ke
     pengguna bahwa database `buku-stok` belum ada/belum di-`init`, dan hentikan (sama seperti
     "data belum ada" -- jangan kirim laporan kosong seolah tidak ada yang menipis).
   - Ambil `mutasi_terakhir` sebagai penanda umur data untuk dicantumkan di pesan.
2. Ambil daftar produk menipis (HANYA BACA -- **jangan** pernah menambahkan `--ya` atau flag
   tulis apa pun ke perintah ini):
   ```bash
   python3 <folder-skill-buku-stok>/scripts/stok.py laporan menipis --db "<isi>" --json
   ```
3. Baca field `jumlah` dan `produk` (tiap item: `nama`, `stok`, `stok_min`,
   `kurang_dari_minimum`, `rata2_terjual_per_hari_30h`, `perkiraan_habis_hari`).
   **`"jumlah": 0` artinya TIDAK ADA produk menipis -- ini kabar baik yang valid, BUKAN data
   kosong/gagal.** Laporkan apa adanya ("Tidak ada produk menipis hari ini"), jangan diperlakukan
   sebagai error.

### Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Stok Menipis"
- Baris angka: Jumlah produk menipis (dari field `jumlah`, termasuk saat nilainya 0)
- Daftar (hanya kalau `jumlah` > 0): "Produk menipis" -- tiap item format
  `Nama -- sisa X -- ambang Y -- perkiraan habis ~Z hari` (dari `stok`, `stok_min`,
  `perkiraan_habis_hari`), urut `kurang_dari_minimum` terbesar dulu, batasi 10 item pertama
  (sebutkan jumlah sisanya bila lebih dari 10)
- Catatan (netral, bukan peringatan): umur data dari `mutasi_terakhir` (`stok.py info`)
- Kalau `jumlah = 0`: cukup baris angka "Jumlah produk menipis: 0" + catatan umur data, tanpa
  bagian daftar.

### Automation
Prompt job (lihat contoh lengkap di `SKILL.md` Langkah 5) HARUS eksplisit menyuruh agent
**hanya membaca** (`stok.py info`/`stok.py laporan menipis`, tanpa `--ya` atau perintah tulis
`stok.py masuk`/`keluar`/`opname`), dan eksplisit menyebut bahwa `jumlah: 0` = "Tidak ada produk
menipis hari ini" (bukan error). Batasi `--tools` job ini ke `exec,read` saja (lihat
`openclaw automations add --help` untuk `--tools`) supaya job tidak bisa menjalankan perintah
lain di luar yang diminta.

## Jalur cadangan: TANPA `buku-stok` (CSV dari aplikasi kasir/inventori lain)

Skill ini **tidak punya** script hitung stok sendiri -- jalur ini murni membaca & membandingkan
angka dari CSV yang sudah diekspor aplikasi lain.

### Sumber data
- Folder: `<isi>` · Pola file: `<isi, mis. stok*.csv>`
- **CSV wajib berisi SEMUA produk** (bukan hanya yang menipis) -- kolom nama produk, stok saat
  ini, stok minimum/ambang. Kalau aplikasi sumbernya hanya bisa mengekspor "yang menipis saja",
  file itu **kosong di hari tanpa produk menipis**, dan `cek_sumber_data.py` akan salah
  menganggapnya "data belum ada" padahal itu kabar baik -- karena itu ekspor **semua** produk,
  lalu bandingkan ambangnya di langkah 2 di bawah, bukan sebaliknya.

### Langkah hitung
1. Cek kesiapan data:
   ```bash
   python3 <folder-skill-laporan-otomatis-terjadwal>/scripts/cek_sumber_data.py \
     --folder "<folder sumber>" --pola "<isi>" --label "stok" --maks-umur-hari 1
   ```
2. Baca CSV, filter baris dengan `stok saat ini <= stok minimum/ambang`, urutkan dari yang
   paling kritis (selisih terbesar di bawah ambang). Perbandingan angka sederhana, boleh
   dilakukan langsung tanpa script tambahan, TAPI **wajib membaca angka apa adanya dari file**,
   tidak menaksir.
3. Tidak ada baris yang menipis setelah dibandingkan: itu **hasil yang valid** (CSV tetap berisi
   semua produk, jadi ini bukan file kosong) -- laporkan "Tidak ada produk menipis hari ini".

### Format pesan
Sama seperti jalur utama (judul, baris jumlah, daftar maks. 10 item, catatan umur data), tanpa
`perkiraan_habis_hari` (tidak tersedia dari CSV biasa) kecuali file sumbernya memang punya kolom
itu.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi -- pemilik/admin/bagian gudang>`
