# Skenario 04 — File rusak / tidak lengkap (wajib menurut Tahap 6)

Data rekaan sengaja rusak: BOM UTF-8, baris dengan koma ekstra tidak konsisten (menyerupai qty
notasi ilmiah "4E+17" ala Excel), qty "abc", qty 0 dan -1, baris kosong total, baris tanpa
identitas barang (SKU & nama kosong), baris duplikat persis, dan baris ringkasan "TOTAL" di akhir.

## Perintah
```
python3 scripts/resi.py in_rusak.csv --json
```

## Hasil
`ok: true` (skrip tidak crash), `jumlah_pesanan_total = jumlah_pesanan_aktif = 2`,
`total_barang = 3`. Baris yang dilewati dilaporkan dengan alasan **dan nomor baris**:
- 3 baris "jumlah tidak terbaca" dilewati (baris 3, 4, 11)
- 2 baris "jumlah nol atau negatif" dilewati (baris 5, 6)
- 1 baris "tanpa identitas barang" dilewati (baris 8)
- 1 baris "baris duplikat" dilewati (baris 10)
- 1 pesanan tanpa nomor resi diberi tahu masuk kelompok "(Resi belum ada)"

Verifikasi manual: dari 10 baris data mentah, hanya baris `G-9001` (qty 2) dan bagian valid dari
`G-9006` (qty 1, tapi baris duplikat persisnya ikut dilewati sehingga tidak dobel dihitung) yang
sebenarnya lolos — cocok dengan `total_barang = 3` (2 dari G-9001 + 1 dari G-9006).

Uji tambahan (baris "Total" di kolom No. Pesanan dengan qty angka asli, bukan kosong): tetap
dilewati dengan benar sebagai "tanpa identitas barang" karena SKU & nama produknya kosong — jadi
baris ringkasan tidak pernah ikut kehitung sebagai barang asli selama SKU/nama-nya kosong. Kalau
suatu saat ekspor markletplace mengisi SKU pada baris total (jarang, belum ditemukan contohnya),
baris itu berisiko lolos — dicatat sebagai catatan kecil, bukan temuan kritikal karena tidak
terjadi pada data uji manapun.

## Kesimpulan skenario 04
Tidak ada crash, tidak ada angka salah hitung, dan setiap baris bermasalah dilaporkan dengan alasan
+ nomor baris yang bisa ditelusuri pengguna — sesuai klaim "Batasan & penanganan error" di SKILL.md.
