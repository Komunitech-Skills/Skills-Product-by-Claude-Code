# Singkatan besaran uang yang didukung `bersihkan-csv` (sejak v1.0.1)

Ditambahkan menindaklanjuti temuan TINGGI Akun B (`examples/HASIL-UJI.md`,
`examples/03-rekap-operasional-csv.md` temuan #1): README/SKILL v1.0.0 mengklaim contoh
**"Rp 1,25jt"** "dirapikan otomatis", padahal `_bersihkan_angka("Rp 1,25jt")` sungguhan
mengembalikan `None`. Sejak v1.0.1 klaim itu benar — didukung lewat `Decimal` (bukan float,
supaya perkalian presisi, tidak ada galat pembulatan biner).

## Sufiks yang dikenali (di akhir teks, tanpa pandang huruf besar/kecil kecuali disebut lain)
| Sufiks | Pengali | Contoh | Hasil |
|---|---|---|---|
| `ribu`, `rb` | × 1.000 | `500rb`, `500 ribu` | 500000 |
| `k` (huruf tunggal) | × 1.000 | `50k` | 50000 |
| `juta`, `jt` | × 1.000.000 | `Rp 1,25jt`, `1,25 juta` | 1250000 |
| `miliar` | × 1.000.000.000 | `1,2 miliar` | 1200000000 |
| `M` (huruf **BESAR** tunggal) | × 1.000.000.000 | `1,5M` | 1500000000 |

Bagian angka sebelum sufiks boleh pakai **satu** pemisah desimal, koma ATAU titik (tidak boleh
dua-duanya sekaligus — itu dianggap ambigu dan ditolak dengan alasan jelas, bukan ditebak):
`1,25jt` = `1.25jt` = 1.250.000. `1.250,5jt` (koma DAN titik) → **ditolak** (`None` + alasan).

## Keputusan ambiguitas huruf `m` kecil (penting, baca sebelum mengubah)
Instruksi kerja sesi ini secara eksplisit meminta kehati-hatian: *"M" alone is ambiguous — treat
'm'/'M' as miliar only when explicitly 'miliar'/'M' after a number ... if you judge it risky,
reject and say so*. Keputusan yang diambil:

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
