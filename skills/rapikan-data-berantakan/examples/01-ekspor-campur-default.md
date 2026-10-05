# 01. Ekspor pelanggan campur (kerjakan dulu, tanya di akhir)

**Berkas:** `examples/data-contoh.csv` (40 baris data fiktif: nama, nomor, dan transaksi karangan, bukan orang nyata).
**Pesan pengguna:** "Ini ekspor pelanggan toko online saya, berantakan banget. Tolong rapikan."

**Cara dijalankan (untuk penguji):** `python3 scripts/rapikan.py examples/data-contoh.csv`

## Balasan yang diharapkan (utuh di chat)

Selesai dirapikan: 40 baris. Diperbaiki: 35 nomor HP, 37 tanggal, 34 harga, 7 nama dan kota (+1 spasi berlebih, 2 isian "-"/"N/A" jadi kosong).
9 sel tidak bisa diperbaiki (dibiarkan seperti aslinya, daftar di bawah). Tidak ada data yang dihapus.

**Contoh perbaikan**
| Isi | Sebelum | Sesudah |
|---|---|---|
| Nomor HP | +62 812-3450-0101 | 6281234500101 |
| Nomor HP | 0812.3450.0101 | 6281234500101 |
| Tanggal | 7 Okt 2026 | 2026-10-07 |
| Tanggal | Senin, 5 Oktober 2026 | 2026-10-05 |
| Harga | Rp1.250.000,- | 1250000 |
| Harga | 1,5jt / 150rb | 1500000 / 150000 |
| Nama | budi santoso | Budi Santoso |
| Nama | siti  rahmawati (spasi ganda) | Siti Rahmawati |

**Perlu keputusan Anda**
1. Nama yang tampaknya sama: "Budi Santoso" / "Bpk. Budi Santoso" / "Santoso Budi" / "Budi Santosa" (baris 2-6, semuanya nomor yang sama); "Muh. Rizal Pratama" / "Muhammad Rizal Pratama" (baris 9-10); "Dewi Lestari" / "Dewi Lestary" (baris 11-12); kota "Yogyakarta" / "Jogja" (baris 19-21). Mau disatukan? Usul saya: nama yang paling sering muncul.
2. Dua pasang baris kembar persis: baris 13-14 (Hendra Gunawan, 12 Okt, Rp310.000) dan baris 15-16 (Toko Maju Jaya, 13 Okt, Rp68.500). Sisakan satu per pasang?
3. 8 tanggal bentuknya "05/10/2026" yang bisa 5 Oktober atau 10 Mei. Saya baca 5 Oktober (hari/bulan). Benar?

**Tidak bisa diperbaiki** (dibiarkan apa adanya): nomor HP "0812-ABC-5555" (berhuruf, baris 18), "6.28123E+11" (Excel menghilangkan digitnya, perlu ekspor ulang kolom itu sebagai teks, baris 19), "0812345" (terlalu pendek, baris 20), "+60 12 345 6789" (nomor luar negeri, baris 21); tanggal "31/02/2026" (tidak ada di kalender, baris 17); harga "abc" (baris 21); baris 31 hampir kosong; baris 32 kurang satu kolom; baris 33 kelebihan kolom.
Catatan lain: 1 sel punya dua nomor (baris 23, dipakai yang pertama), 1 nomor telepon rumah (baris 24, bukan WhatsApp), 1 harga bersen dibulatkan (Rp 1.500,50 jadi 1501), 1 jam dibuang dari tanggal, 1 harga "gratis" dicatat 0.

Mau file bersihnya? Balas "kirim file".

## Verifikasi angka (independen dari script)
Dihitung terpisah dari data mentah:
- HP: 39 sel terisi, 4 tidak bisa diperbaiki -> 35 diubah (tidak ada yang sudah berformat 628).
- Tanggal: 39 terisi, 1 tidak valid (31/02) -> 38 terbaca; 1 sudah ISO (baris 3) -> 37 diubah.
- Harga: 39 terisi, 2 placeholder jadi kosong, 1 "abc" -> 36 terbaca; 2 sudah bilangan polos (baris 3 dan 10) -> 34 diubah.
- Tanggal ambigu (hari dan bulan sama-sama <= 12 dan berbeda): baris 2, 5, 6, 11, 12, 13, 14, 41 = 8.
- 5 Oktober 2026 memang hari Senin (cocok dengan "Senin, 5 Oktober 2026").
- Uji otomatis `tests/uji_rapikan.py` memeriksa nilai per baris dari data ini.
