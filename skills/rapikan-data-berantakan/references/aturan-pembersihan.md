# Aturan pembersihan manual

Dipakai bila alat hitung tidak bisa dijalankan atau datanya hanya tempelan kecil. Hasil manual wajib disebut "dikerjakan manual, belum diverifikasi alat hitung". Hitung jumlah perubahan satu per satu.

## Nomor HP -> `628xxxxxxxxxx`
1. Buang semua selain angka (spasi, strip, titik, kurung, `+`). Buang `(0)` di dalam `+62 (0) 812`.
2. Awalan `0062` -> buang `00`. Awalan `62` -> pakai. Awalan `0` -> ganti dengan `62`. Awalan `8` (nol hilang) -> tambah `62`.
3. Panjang wajar nomor HP: setelah `62` ada 9-12 angka, diawali `8`. Di luar itu: jangan ditebak, tandai.
4. Berisi huruf, notasi ilmiah (`6.28E+11`), atau `+` selain `+62`: tandai "tidak bisa diperbaiki".
5. Dua nomor dalam satu sel: pakai yang pertama, catat yang kedua.

## Tanggal -> `YYYY-MM-DD`
- Nama bulan: Jan, Feb, Mar, Apr, Mei, Jun, Jul, Agu/Agt, Sep, Okt, Nov, Des (Inggris: May, Aug, Oct, Dec ikut dikenali). Nama hari dan jam dibuang.
- Tahun dua digit: 00-69 -> 2000-2069, 70-99 -> 1970-1999.
- `a/b/tahun` dengan a dan b <= 12 dan a berbeda b: ambigu. Bila ada tanggal lain di kolom yang sama dengan angka > 12 di posisi pertama (`13/10`) -> hari/bulan; di posisi kedua (`10/13`) -> bulan/hari. Tanpa bukti: hari/bulan dan tanyakan.
- Tanggal yang tidak ada di kalender (31/02): tandai, jangan diganti.

## Rupiah -> bilangan bulat
- Buang `Rp`, `IDR`, spasi, `,-`. Titik dengan 3 digit di belakang = pemisah ribuan (`1.500.000`). Koma dengan 1-2 digit = desimal (`15.000,50` -> 15001, dibulatkan setengah naik).
- Satuan: `rb`/`ribu`/`k` = x1.000; `jt`/`juta` = x1.000.000; `miliar` = x1.000.000.000 (`1,5jt` = 1.500.000).
- `(50.000)` atau `-50.000` = negatif. "gratis" = 0. `1,500` ambigu: dibaca 1.500 dan ditandai.
- Bukan angka (`abc`, `12,34,56`): tandai.

## Nama
- Buang spasi ganda/tepi dan karakter tak terlihat. Title Case untuk kata yang seluruhnya huruf kecil atau seluruhnya kapital; kata campuran (`iPhone`) dan kata berangka (`5kg`) dibiarkan. `PT`, `CV`, `UD`, `RS` tetap kapital; `bin`, `binti`, `dan`, `van` kecil.
- Kemiripan (hanya ditandai, tidak digabung): nama sama dengan urutan kata beda (Budi Santoso / Santoso Budi), ada sapaan (Bpk., Ibu, Mas, Hj.), singkatan (Muh./Muhammad), ejaan beda satu-dua huruf (Santoso/Santosa). Nama yang beda angka (Kopi 250ml / Kopi 500ml) dianggap barang berbeda.
