# Contoh 03 - Siklus bulan kedua (cara membaca tren)
Bulan 1 disimpan sebagai `anonim-2026-09.csv` (garis dasar, tanpa tren). Di akhir Oktober pengguna mengirim ekspor baru; agent menjalankan
script atas file baru saja (atau atas gabungan) dan membandingkan `selisih_persen_poin`.

Perkiraan format hasil untuk isu pengiriman (angka ilustrasi, bukan dari data contoh):
| Isu | Sept | Okt | Selisih | Ukuran keberhasilan | Keputusan |
|---|---|---|---|---|---|
| Pengiriman telat | 23,5% | 8,0% | -15,5 poin | < 10% | Tercapai -> tutup, pantau 1 bulan |
| Kemasan bocor | 11,8% | 10,5% | -1,3 poin | < 3% | Belum -> lanjut, ganti pemasok wadah |
Aturan: tren hanya dilaporkan bila kedua bulan punya ≥ 5 masukan; selain itu script menulis "data kurang".
