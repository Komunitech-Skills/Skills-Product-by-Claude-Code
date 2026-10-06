# Format input untuk hitungan pesanan

Agent menyusun file ini dari chat pelanggan yang berantakan. Isinya hanya data yang benar-benar ada di chat atau diberikan pemilik toko. Yang tidak diketahui dikosongkan (script akan menandainya `[isian]`), **jangan diisi tebakan**.

## A. Teks sederhana (paling mudah)
Satu blok per pesanan, dipisah baris `---`. Kunci tidak peka huruf besar/kecil.

```
TANGGAL: 2026-10-06
---
pelanggan: Kak Dina            ← nama panggilan dari chat
item: merah x2; biru x1         ← nama/alias katalog + jumlah, dipisah ;
diskon: 10%                     ← persen atau nominal (50rb / 50000); kosong = 0
ongkir: 18rb                    ← kosong = belum diketahui; "gratis" = 0
kurir: JNE REG                  ← kurir + layanan (boleh juga baris "layanan:")
bayar: transfer                 ← transfer / COD / QRIS
status: belum                   ← "lunas" bila pemilik sudah cek mutasi sendiri
dibayar: 100rb                  ← opsional, untuk DP/bayar sebagian
penerima: Dina Lestari
hp: 0812-3456-7890
alamat: Jl. Melati No. 12 RT 03/04, Kel. Sukamaju, Kec. Cibeunying, Bandung 40123
catatan: bungkus kado
```

Bentuk item yang terbaca: `merah x2`, `2 merah`, `2x merah`, `Box Kado x2 @25rb` (harga dari pengguna, menimpa katalog). Item tanpa jumlah ditandai "jumlah tidak jelas".

## B. JSON
```json
{"tanggal": "2026-10-06",
 "pesanan": [{"kode": "", "pelanggan": "Kak Dina",
   "item": [{"nama": "merah", "qty": 2}, {"nama": "Box Kado", "qty": 1, "harga": 25000}],
   "diskon": "10%", "ongkir": 18000, "kurir": "JNE", "layanan": "REG", "bayar": "transfer",
   "status": "belum", "penerima": "Dina Lestari", "hp": "081234567890", "alamat": "...", "catatan": ""}],
 "katalog": [{"nama": "Kaos Polos Merah", "harga": 85000, "kode": "KM", "alias": ["merah"], "stok": 10}]}
```
`katalog` di JSON opsional (dipakai bila tidak ada CSV).

## C. Katalog CSV
Kolom wajib `nama,harga`; opsional `kode`, `alias` (beberapa sebutan pelanggan dipisah `|`), `stok`. Harga boleh `85.000`, `85rb`, `Rp85.000`. Pemisah `,` atau `;`.

```
kode,nama,harga,alias,stok
KM,Kaos Polos Merah,85000,merah|kaos merah,10
```

## Perintah
```
python3 scripts/rekap_pesanan.py pesanan.txt --katalog katalog.csv --format teks
python3 scripts/rekap_pesanan.py pesanan.json --format json --mulai 5
```
Windows: `python` atau `py`. `--mulai 5` = nomor urut kode pesanan dimulai dari 05 (bila hari ini sudah ada 4 pesanan). `--tanggal 2026-10-06` menimpa tanggal di file. Kode pesanan = `TAHUNBULANTANGGAL-urut`, mis. `20261006-01`; kode yang sudah diberi pengguna dipakai apa adanya.

## Arti tanda di keluaran
- `!` masalah hitungan (harga/jumlah/ongkir belum diketahui, diskon dibatasi). Total pesanan itu **tidak** masuk omzet.
- `?` data kirim kurang (alamat, kode pos, HP, kurir). Jadi pertanyaan ke pelanggan di pesan konfirmasi.
- `PESANAN GANDA`: pelanggan + isi pesanan sama (dan HP sama atau salah satunya kosong) = dianggap tempelan dobel, dihitung sekali. Bila pelanggan memang pesan dua kali, beri `kode` berbeda atau bedakan isinya.
- Kode keluar 2 = input rusak (file kosong, JSON salah, katalog tanpa kolom harga, tanggal salah format). Perbaiki input, jangan menghitung manual diam-diam.
