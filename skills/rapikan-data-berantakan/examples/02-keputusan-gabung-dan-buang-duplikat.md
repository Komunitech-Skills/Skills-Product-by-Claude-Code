# 02. Pengguna memutuskan: gabung nama, buang duplikat

**Lanjutan dari 01.** Pengguna membalas: "Nama 1, 2, 3 gabung. Yogyakarta pakai 'Yogyakarta'. Buang yang kembar."

**Cara dijalankan:** `python3 scripts/rapikan.py examples/data-contoh.csv --gabung-kelompok 1,2,3 --nama-baku "4=Yogyakarta" --buang-duplikat-persis`

## Balasan yang diharapkan

Sudah. Yang berubah dari hasil sebelumnya:
- Nama disatukan: 6 nama diganti ("Bpk. Budi Santoso", "Santoso Budi", "Budi Santosa" jadi "Budi Santoso"; "Muh. Rizal Pratama" jadi "Muhammad Rizal Pratama"; "Dewi Lestary" jadi "Dewi Lestari"; "Jogja" jadi "Yogyakarta").
- Setelah nama disatukan, ternyata ada satu pasangan kembar baru: baris 9 dan 10 (Rizal Pratama, 7 Okt, Kue Kering, Rp2.500.000) sama persis. Total 3 baris kembar dibuang: baris 10, 14, dan 16. Ketiganya disimpan di file terpisah, tidak hilang.
- Sekarang 37 baris (dari 40).

Tanggal "05/10/2026" dan 7 lainnya masih saya baca 5 Oktober; koreksi saya kalau salah.

## Verifikasi angka
- 40 baris - 3 dibuang = 37 (laporan: `jumlah_baris_keluar` = 37, `nama_digabung_otomatis` = 6).
- Nama diganti: Budi (baris data No 3, 4, 5 = 3), Rizal No 8 (1), Dewi No 11 (1), kota Jogja No 19 (1) = 6. Baris "Budi Santoso" No 1, 2 sudah benar.
- Total harga yang terbaca di 37 baris = Rp12.228.001 (dihitung ulang dari file hasil; 1 dari nilai itu hasil pembulatan Rp 1.500,50 jadi 1501).
- Baris kembar baru (9-10) muncul hanya setelah penggabungan nama: bukti bahwa menggabung nama sebelum mencari duplikat lebih tepat.
- Berkas `dibuang-duplikat.csv` berisi 3 baris dengan nomor baris asal.
