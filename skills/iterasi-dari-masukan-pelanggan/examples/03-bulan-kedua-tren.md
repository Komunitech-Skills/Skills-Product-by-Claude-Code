# Contoh 03 - Siklus bulan kedua (cara membaca tren)
Bulan 1 disimpan sebagai `anonim-2026-09.csv` (garis dasar, tanpa tren). Di akhir Oktober pengguna mengirim ekspor baru; agent menjalankan
script atas file baru saja (atau atas gabungan) dan membandingkan `selisih_persen_poin`.

Perkiraan format hasil untuk isu pengiriman (angka Okt ilustrasi, bukan dari data contoh). *Disegarkan 2026-10-16 (dicek ulang dengan script v1.0.13): kolom Sept memakai persen keluhan bulan September dari keluaran script pada data contoh (`tren_per_bulan` 2026-09 di keluaran contoh 01): Pengiriman 7 dari 35 = 20,0%, Kemasan 5 dari 35 = 14,3%. Angka Sept di versi lama tabel ini (23,5% dan 11,8%) adalah angka ilustrasi tulisan tangan, bukan keluaran script versi mana pun; sebagai pembanding, script v1.0.1 pada data yang sama sebenarnya menghasilkan Pengiriman 6 dari 34 = 17,6% dan Kemasan 5 dari 34 = 14,7%. Kolom Okt tetap ilustrasi.*

| Isu | Sept | Okt | Selisih | Ukuran keberhasilan | Keputusan |
|---|---|---|---|---|---|
| Pengiriman telat | 20,0% | 8,0% | -12,0 poin | < 10% | Tercapai -> tutup, pantau 1 bulan |
| Kemasan bocor | 14,3% | 10,5% | -3,8 poin | < 3% | Belum -> lanjut, ganti pemasok wadah |
Aturan: tren hanya dilaporkan bila kedua bulan punya ≥ 5 masukan; selain itu script menulis "data kurang".
