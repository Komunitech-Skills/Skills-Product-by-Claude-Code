# 02. Pengguna memutuskan: gabung nama, buang duplikat

**Lanjutan dari 01.** Pengguna membalas: "Nama 1, 2, 3 gabung. Yogyakarta pakai 'Yogyakarta'. Buang yang kembar."

**Cara dijalankan:** `python3 scripts/rapikan.py examples/data-contoh.csv --gabung-kelompok 1,2,3 --nama-baku "4=Yogyakarta" --buang-duplikat-persis`

## Balasan yang diharapkan

Sudah. Yang berubah dari hasil sebelumnya:
- Nama disatukan: 6 nama diganti ("Bpk. Budi Santoso", "Santoso Budi", "Budi Santosa" jadi "Budi Santoso"; "Muh. Rizal Pratama" jadi "Muhammad Rizal Pratama"; "Dewi Lestary" jadi "Dewi Lestari"; "Jogja" jadi "Yogyakarta").
- Setelah nama disatukan, ternyata ada satu pasangan kembar baru: baris 9 dan 10 (Rizal Pratama, 7 Okt, Kue Kering, Rp2.500.000) sama persis. Total 3 baris kembar dibuang: baris 10, 14, dan 16. Ketiganya disimpan di file terpisah, tidak hilang.
- Sekarang 37 baris (dari 40).

Tanggal "05/10/2026" dan 7 lainnya masih saya baca 5 Oktober; koreksi saya kalau salah.

## Blok angka dari alat (disalin apa adanya)

Selesai dirapikan: 40 baris data; di file bersih: 37 baris, 3 baris duplikat persis dibuang atas permintaan.
- Nomor HP diseragamkan ke format 62: 34
- Telepon rumah/kantor (bukan WhatsApp; dipisah ke kolom _telepon_rumah, tidak ada di kolom HP): 1 sel
  - baris 24 "(021) 555-0123"
- Sel berisi lebih dari satu nomor: 1 sel
  - baris 23 "0831 4444 5555 / 0896 6666 7777" -> dipakai sebagai HP: 6283144445555; nomor lain dicatat: 6289666667777
- Tanggal diseragamkan ke YYYY-MM-DD: 37
- Tanggal ambigu (bisa hari/bulan atau bulan/hari; dibaca hari/bulan kecuali ada bukti lain): 8 -> baris 2, 5, 6, 11, 12, 13, 14, 41
- Nominal rupiah jadi angka: 34
- Nama/produk/kota dirapikan huruf dan spasinya: 7
- Baris kembar persis (semua kolom sama): 3 grup
  - baris 9 & 10 (Muhammad Rizal Pratama)
  - baris 13 & 14 (Hendra Gunawan)
  - baris 15 & 16 (Toko Maju Jaya)
- Nomor HP sama tetapi nama beda (belum tentu orang yang sama, TIDAK digabung): 0 kelompok
- Nama yang sudah digabung atas persetujuan pengguna: 4 kelompok (6 sel diganti)
  - no. 1 -> "Budi Santoso"
  - no. 2 -> "Muhammad Rizal Pratama"
  - no. 3 -> "Dewi Lestari"
  - no. 4 -> "Yogyakarta"
- Sel tidak bisa diperbaiki (dibiarkan apa adanya): 9 sel di 8 baris
  - baris 17 kolom Tanggal Order "31/02/2026": tanggal tidak ada di kalender (mis. 31 Februari)
  - baris 18 kolom No HP "0812-ABC-5555": ada huruf di dalam nomor
  - baris 19 kolom No HP "6.28123E+11": nomor berubah jadi notasi ilmiah oleh Excel (digitnya sudah hilang); ekspor ulang dengan kolom bertipe teks
  - baris 20 kolom No HP "0812345": panjang nomor HP tidak wajar (6 angka setelah 0/62; wajar 9-12)
  - baris 21 kolom No HP "+60 12 345 6789": tampaknya nomor luar negeri (bukan +62)
  - baris 21 kolom Total Bayar "abc": bukan angka rupiah yang dikenali
  - baris 31: baris hampir kosong: hanya berisi nomor urut
  - baris 32: jumlah kolom kurang (6 dari 7); dilengkapi kosong
  - baris 33: jumlah kolom berlebih; kemungkinan koma/pemisah di dalam isi sel yang tidak diberi tanda kutip

## Verifikasi angka
- 40 baris - 3 dibuang = 37 (laporan: `jumlah_baris_keluar` = 37, `nama_digabung_otomatis` = 6).
- Nama diganti: Budi (baris data No 3, 4, 5 = 3), Rizal No 8 (1), Dewi No 11 (1), kota Jogja No 19 (1) = 6. Baris "Budi Santoso" No 1, 2 sudah benar.
- Total harga yang terbaca di 37 baris = Rp12.228.001 (dihitung ulang dari file hasil; 1 dari nilai itu hasil pembulatan Rp 1.500,50 jadi 1501).
- Baris kembar baru (9-10) muncul hanya setelah penggabungan nama: bukti bahwa menggabung nama sebelum mencari duplikat lebih tepat.
- Berkas `dibuang-duplikat.csv` berisi 3 baris dengan nomor baris asal.
