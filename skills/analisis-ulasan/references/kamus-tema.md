# Kamus Tema & Cara Menambah

Script `scripts/olah_ulasan.py` menandai **kandidat** tema per klausa. Klausa = potongan kalimat yang dipisah
titik/tanda seru/baris baru, kata sambung "tapi/namun/cuma/padahal/untung", lalu koma. Satu ulasan boleh punya
beberapa tema (mis. "barang bagus tapi pengiriman lama" → pujian kualitas + keluhan pengiriman).

## Normalisasi yang dilakukan sebelum dicocokkan
1. Huruf kecil, URL dibuang, huruf berulang dirapikan (`bagusss` → `bagus`), kata ulang (`barang2`, `barang-barang` → `barang`).
2. Frasa: `fast respon` → `respons cepat`, `slow respon` → `respons lambat`, `real pict` → `sesuai foto`,
   `worth it` → `sepadan`, `bubble wrap` → `bubblewrap`, `murmer` → `murah`, `repeat order`/`ke-2 kali` → `order lagi`,
   `exp/expired/kadaluarsa` → `kedaluwarsa`, `size chart` → `tabel ukuran`.
3. Slang/singkatan per kata (±310 entri, termasuk bahasa Inggris dasar: good quality, fast delivery, will buy again), contoh: `brg`→barang, `bgt`→banget, `gk/ga/gak/nggak/tdk`→tidak,
   `blm`→belum, `krg`→kurang, `mantul/mantab/joss`→mantap, `cpt/cepet/kilat`→cepat, `lelet/lemot`→lambat,
   `packing/paking/bungkus`→kemasan, `seller`→penjual, `cs/min`→admin, `size/uk`→ukuran, `ori`→asli, `kw`→palsu,
   `kegedean`→kebesaran, `enk/endul/maknyus`→enak, `krispi/kriuk`→renyah.
4. Negasi digabung: `tidak sesuai` → `tidak_sesuai`, `kurang rapi` → `kurang_rapi`, `belum sampai` → `belum_sampai`,
   `tidak begitu bagus` → `tidak_bagus`, `tidak pernah kecewa` → `tidak_kecewa`.
   `tidak ada yang rusak` / `tanpa cacat` → `tidak_ada_rusak` / `tidak_ada_cacat` (dihitung sebagai pujian).
5. Data pribadi (email, nomor HP, @akun, kode pesanan, sapaan+nama) **disamarkan sebelum kalimat dipecah**, jadi kutipan
   dan kata teratas tidak memuat potongan email/nama. Titik di antara angka (Rp 1.500.000) tidak memecah kalimat.
6. Presedensi dalam satu klausa: keluhan kemasan mengalahkan "cacat produk" (`kemasan penyok`), keluhan
   mengalahkan pujian aspek yang sama, "warna beda dengan foto" = tidak sesuai foto (bukan salah kirim).
   Antar-keluhan juga berlaku per kalimat ("ga sesuai deskripsi, warnanya beda" dihitung satu tema: tidak sesuai).
   "Tidak terlalu manis/asin" tidak dihitung sebagai keluhan rasa. "Nunggu paket lama" = pengiriman; "pelayanan lama" = waktu tunggu.
   "Puas secara umum" hanya dihitung bila ulasan tidak punya pujian yang lebih spesifik.

## Daftar id tema
| id | Label | Area yang memperbaiki |
|---|---|---|
| k_tidak_sesuai | Barang tidak sesuai deskripsi/foto | produk & listing |
| k_kualitas | Kualitas buruk / cacat / cepat rusak | produk |
| k_ukuran | Ukuran tidak pas / info ukuran kurang jelas | produk & listing |
| k_pengiriman | Pengiriman/proses kirim lambat | proses kirim & kurir |
| k_kemasan | Kemasan kurang aman / rusak / bocor | packing (gudang) |
| k_salah_kirim | Salah kirim / barang kurang / varian keliru | packing (gudang) |
| k_respons | Respons penjual/CS lambat atau kurang ramah | layanan (admin/CS) |
| k_harga | Harga terasa mahal / tidak sepadan | harga & nilai |
| k_rasa | Rasa kurang enak / tidak konsisten | produk |
| k_bau | Bau tidak sedap | produk & penyimpanan |
| k_kedaluwarsa | Kedaluwarsa / tanggal expired dekat | stok & penyimpanan |
| k_retur | Komplain/retur/garansi dipersulit | layanan (admin/CS) |
| k_waktu_tunggu | Waktu tunggu/penyajian lama (tempat makan & jasa) | layanan (dapur/kasir/staf) |
| k_kebersihan | Kebersihan / benda asing (rambut, serangga) — **prioritas keamanan** | kebersihan & keamanan pangan |
| k_fasilitas | Fasilitas kurang (parkir, toilet, AC, wifi, tempat) | fasilitas tempat |
| p_sesuai | Sesuai deskripsi/foto | produk & listing |
| p_kualitas | Kualitas bagus / awet | produk |
| p_pengiriman | Pengiriman/proses cepat | proses kirim & kurir |
| p_kemasan | Kemasan rapi & aman | packing (gudang) |
| p_harga | Harga terjangkau / sepadan | harga & nilai |
| p_respons | Penjual/CS ramah & responsif | layanan (admin/CS) |
| p_rasa | Rasa enak | produk |
| p_aroma | Aroma wangi | produk |
| p_ukuran | Ukuran pas / sesuai tabel ukuran | produk & listing |
| p_repeat | Pembeli berulang / akan beli lagi | loyalitas |
| p_bonus | Bonus / hadiah kecil / sentuhan personal | packing & layanan |
| p_suasana | Suasana/tempat nyaman | fasilitas tempat |
| p_kebersihan | Bersih & higienis | kebersihan & keamanan pangan |
| p_fasilitas | Fasilitas lengkap (parkir, toilet, wifi) | fasilitas tempat |
| p_umum | Puas secara umum (tanpa detail) | umum |

## Menambah slang atau tema (`--kamus-tambahan`)
Buat file JSON di folder kerja pengguna (contoh lengkap: `templates/kamus-contoh.json`):
```json
{
  "slang": {"mantaf": "mantap"},
  "tema": [
    {"id": "k_level_pedas", "label": "Level pedas tidak sesuai", "jenis": "keluhan", "pihak": "produk",
     "pola": ["\\bkepedasan\\b", "\\blevel\\W+\\d\\W+(?:\\w+\\W+){0,3}(?:kayak|seperti|beda)"]},
    {"id": "p_rasa", "pola": ["\\bpedasnya\\W+pas\\b"]}
  ]
}
```
- `"kecualikan": ["regex", ...]` → potongan kalimat yang cocok dengan pola ini **tidak** dihitung untuk tema itu
  (untuk membuang salah tangkap, mis. `"\\bmati\\W+lampu\\b"` pada `k_kualitas`). Jumlah yang dikecualikan tercatat di `sumber.dikecualikan`.
- Alternatif cepat tanpa file: `--abaikan-id k_respons:3,14` (bisa diulang) membuang tema dari ulasan ber-id tersebut setelah dibaca.
- `id` yang sudah ada → polanya **ditambahkan** ke tema itu. `id` baru → tema baru (`jenis`: `keluhan`/`pujian`).
- Pola adalah regex Python yang dicocokkan ke teks **setelah normalisasi** (huruf kecil, slang diganti, negasi
  bergabung dengan `_`). Tulis kata versi baku (mis. `tidak_enak`, bukan `ga enak`).
- Jalankan ulang script agar jumlahnya dihitung, lalu cek hasilnya dengan `--detail-tema <id>`.

## Keterbatasan yang harus diingat agent
- Sarkasme ("mantap, 2 minggu baru nyampe") bisa terbaca pujian; bintang rendah membantu mendeteksinya.
- Kata bermakna ganda: "lama" (sudah lama langganan vs pengiriman lama) — script mensyaratkan kata pengiriman di dekatnya.
- Bahasa daerah & bahasa Inggris panjang hanya dikenali sebagian → masuk "belum terklasifikasi" untuk dibaca agent.
