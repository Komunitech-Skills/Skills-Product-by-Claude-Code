# Singkatan besaran uang yang didukung `bersihkan-csv` (sejak v1.0.1, diperketat v1.0.2)

Ditambahkan menindaklanjuti temuan TINGGI Akun B (`examples/HASIL-UJI.md`,
`examples/03-rekap-operasional-csv.md` temuan #1): README/SKILL v1.0.0 mengklaim contoh
**"Rp 1,25jt"** "dirapikan otomatis", padahal `_bersihkan_angka("Rp 1,25jt")` sungguhan
mengembalikan `None`. Sejak v1.0.1 klaim itu benar — didukung lewat `Decimal` (bukan float,
supaya perkalian presisi, tidak ada galat pembulatan biner).

## Sufiks yang dikenali (di akhir teks, tanpa pandang huruf besar/kecil kecuali disebut lain)
| Sufiks | Pengali | Contoh | Hasil |
|---|---|---|---|
| `ribu`, `rb` | × 1.000 | `500rb`, `2,5 rb` | 500000, 2500 |
| `k` (huruf tunggal) | × 1.000 | `10k`, `10K` | 10000 |
| `juta`, `jt` | × 1.000.000 | `Rp 1,25jt`, `1,25 juta` | 1250000 |
| `miliar`, `milyar` | × 1.000.000.000 | `1,2 miliar` | 1200000000 |
| `M` (huruf **BESAR** tunggal) | × 1.000.000.000 | `1,5M` | 1500000000 |

Awalan `Rp`/`Rp.`/`IDR`, tanda minus (`-Rp 18.500`, `Rp -500rb`), dan ekor kuitansi `,-`
(`Rp 1.250.000,-`) dikenali. Semua nilai dihitung dengan `Decimal` dan ditulis persis ke file hasil
(tanpa notasi ilmiah, tanpa pembulatan — `Rp 12.345.678.901,55` → `12345678901.55`).

## Aturan angka di depan singkatan (v1.0.2)
- Boleh **satu** pemisah desimal, koma ATAU titik, dengan **1–2 angka** di belakangnya:
  `1,25jt` = `1.25jt` = 1.250.000; `1.5` = `1,5` = 1,5 (tanpa singkatan pun sama).
- **Tepat 3 angka** di belakang pemisah sebelum singkatan (`1.500rb`, `1,250jt`) → **ditolak**
  (ambigu: 1,5 ribu atau 1.500 ribu?). Tanpa singkatan, `1.500` tetap = 1500 (titik ribuan gaya
  Indonesia, perilaku sejak v1.0.0).
- Koma DAN titik sekaligus (`1.250,5jt`) atau lebih dari satu pemisah → **ditolak**.

## Bentuk gabungan (v1.0.2)
`3 jt 500 rb` / `3jt500rb` = 3.500.000; `1 miliar 250 jt` = 1.250.000.000. Syarat: satuan urut
turun, tiap bagian angka bulat, dan bagian bawah lebih kecil dari satuan di atasnya. Selain itu
ditolak dengan alasan: `3jt500` (ekor tanpa satuan — ribu? rupiah?), `500 rb 3 jt` (urutan naik),
`3 jt 1500 rb` (bagian bawah melebihi), `1,5jt 200rb` (desimal di bentuk gabungan).

## Angka tanpa singkatan
Sama seperti v1.0.0 (`Rp 1.234.567,89`, `1234567.89`, `1.234.567`, `12,5`, `1,234` = 1234), tapi
pengelompokan ribuan yang rusak (`1.23.456`, `12,5.5`) sekarang **ditolak dengan alasan**, bukan
dibaca asal-asalan. Satuan non-uang (`1kg`) juga ditolak dengan alasan. Teks biasa (nama barang,
"belum diisi") tetap `None` tanpa alasan — itu memang kolom teks.

## Keputusan ambiguitas huruf `m` kecil (penting, baca sebelum mengubah)
Keputusan yang diambil (huruf `M` sendirian berisiko ambigu):

- Huruf **BESAR** tunggal `M` (mis. `1,5M`, `Rp 2M`) → **diterima** sebagai miliar. Ini konvensi
  yang sudah lazim dipakai pebisnis Indonesia di percakapan/dokumen informal (mis. "omzet 1,5M"),
  dan huruf besar jarang dipakai untuk arti lain (bukan satuan SI resmi apa pun untuk uang).
- Huruf **kecil** tunggal `m` (mis. `2m`, `1.5m`) → **SENGAJA DITOLAK** (`None` + alasan eksplisit
  "ambigu"), BUKAN ditebak jadi miliar. Alasan: `m` kecil adalah simbol SI resmi untuk **meter**,
  dan juga potongan umum kata lain; menerkanya sebagai "miliar" berisiko salah kalau sel aslinya
  memang satuan panjang/berat/singkatan lain yang kebetulan diketik tanpa spasi sebelum huruf
  `m`. ATURAN INI HANYA berlaku untuk huruf `m` **tunggal** setelah digit murni tanpa spasi —
  kata **penuh** `miliar` (atau `Miliar`/`MILIAR`, karena kata penuh dicek case-insensitive) tetap
  diterima seperti biasa, karena kata penuh tidak ambigu.
- Kalau pengguna memang bermaksud "miliar" tapi menulis `m` kecil, agent yang memakai skill ini
  perlu **bertanya balik** atau minta pengguna menulis ulang `miliar`/`M` (huruf besar) — jangan
  menebak nilainya sendiri di luar script.

## Kolom yang sebagian gagal (temuan SEDANG Akun B)
Perilaku "satu sel gagal parse → satu KOLOM PENUH batal dikonversi" (all-or-nothing per kolom)
**dipertahankan apa adanya** sejak v1.0.0 — ini sengaja aman (tidak ada kolom campur angka/teks
setengah-jadi, tidak ada nilai salah diam-diam). Yang berubah di v1.0.1: kalau sebuah kolom
**sebagian** selnya berhasil jadi angka tapi ada sel lain yang gagal (sehingga seluruh kolom itu
dibiarkan Text), output sekarang **selalu** menyebutkan baris & nilai penyebabnya — lewat
peringatan di layar dan field `kolom_gagal_sebagian` pada `--json`. Kolom yang **memang** isinya
teks murni (tidak pernah ada sel yang berhasil jadi angka sama sekali, mis. kolom "Nama Barang")
TIDAK dianggap "gagal" dan tidak dilaporkan di sini — itu bukan kegagalan, memang kolom teks.
