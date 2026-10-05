# Momen Belanja Lokal & Bobot Minggu

Pakai untuk mengisi `--bobot-minggu` (mis. `1 1 1 2` = minggu ke-4 anggaran dua kali lipat). Momen berubah tiap tahun: **jangan menebak** tanggal yang bergantung kalender agama/keputusan pemerintah; minta pengguna mengonfirmasi. Daftar momen bertanggal tetap per bulan bisa dicetak dengan `python3 scripts/alokasi_anggaran.py --momen TAHUN-BULAN` (isi script = tabel ini; ubah keduanya bersamaan). Jangan menyimpulkan "bulan ini tidak ada momen" tanpa mencocokkan bulan itu ke tabel.

| Momen | Waktu | Catatan perencanaan |
|---|---|---|
| Gajian & tanggal tua | sekitar tanggal 25-1 (gajian); tanggal tua 15-24 | Naikkan anggaran menjelang gajian, tahan di tanggal tua untuk produk non-esensial; produk murah/esensial lebih tahan |
| Tanggal kembar (9.9, 10.10, 11.11, 12.12) | tanggal tetap | Kampanye marketplace besar; bergantung program platform, cek Seller Center untuk syarat ikut voucher/gratis ongkir |
| Harbolnas (Hari Belanja Online Nasional) | **12 Desember (12.12)**; beberapa tahun dibuat rangkaian beberapa hari di sekitar 12.12, cek pengumuman resmi tahun berjalan. **11.11 bukan Harbolnas** (11.11 = tanggal kembar) | Persiapan stok & kreatif 2-3 minggu sebelumnya; naikkan anggaran bertahap (maks +20% per langkah), jangan melonjak mendadak |
| Ramadan & Lebaran | tanggal berubah tiap tahun (cek keputusan pemerintah) | Puncak fashion, makanan, hampers, kirim paket; pesanan awal jauh sebelum Lebaran karena batas kirim ekspedisi |
| Tahun ajaran baru | sekitar Juli | Seragam, alat tulis, tas, les |
| 17 Agustus | tanggal tetap | Atribut, lomba, promo bertema |
| Hari Ibu | 22 Desember | Hadiah, fashion, kuliner |
| Natal & Tahun Baru | 25 Desember, 1 Januari | Hampers, kuliner, liburan |
| Awal bulan/bonus/THR | bervariasi | Bonus dan THR menggeser waktu belanja; tanyakan pola pembeli |

Cara menaruh bobot: minggu momen puncak berbobot 2, minggu persiapan 1, minggu tanggal tua 1 (atau dikurangi dengan `--bobot-minggu 1 1 1 2` lalu ubah manual bila produk tidak esensial). Bobot hanya bilangan bulat 1-99.
