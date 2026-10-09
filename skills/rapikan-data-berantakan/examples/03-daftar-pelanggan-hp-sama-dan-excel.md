# 03. Mode daftar: HP sama ditandai, dibuka di Excel

**Pesan pengguna:** "Anggap ini daftar pelanggan (satu orang satu baris), bukan daftar transaksi. Nanti saya buka di Excel."

**Cara dijalankan:** `python3 scripts/rapikan.py examples/data-contoh.csv --jenis daftar --hp-untuk-excel`

## Balasan yang diharapkan
Dalam mode daftar, nomor HP yang sama ditandai sebagai kemungkinan orang yang sama:
- Di luar 2 pasang baris kembar persis (Hendra Gunawan, Toko Maju Jaya; sudah ditandai sebagai duplikat), ada 7 nomor yang dipakai lebih dari satu baris. Tiga di antaranya dengan nama yang tulisannya berbeda: nomor 6281234500101 (Budi Santoso / Bpk. Budi Santoso / Budi Santosa / Santoso Budi, baris 2-6), 6289900003030 (Muh. Rizal Pratama / Muhammad Rizal Pratama, baris 9-10), 6281355500404 (Dewi Lestari / Dewi Lestary, baris 11-12). Itu bukti kuat bahwa nama-nama tersebut satu orang.
- Empat lainnya nama sama, tetapi beda tanggal pesanan (pelanggan yang beli berulang): Siti Rahmawati, Lia Anggraini, Fajar Nugraha, Wulan Sari. Kalau yang Anda butuhkan satu baris per orang, gabungkan manual atau minta saya menyusun daftar unik.
- Nomor HP ditulis dalam bentuk khusus agar Excel tidak mengubahnya menjadi 6,28E+11. File ini baik dibuka di Excel; kalau mau diimpor ke aplikasi lain, bilang saja supaya saya buat versi polos.

## Blok angka dari alat (disalin apa adanya)

Selesai dirapikan: 40 baris data; di file bersih: 40 baris, tidak ada baris yang dihapus.
- Nomor HP diseragamkan ke format 62: 34
- Telepon rumah/kantor (bukan WhatsApp; dipisah ke kolom _telepon_rumah, tidak ada di kolom HP): 1 sel
  - baris 24 "(021) 555-0123"
- Sel berisi lebih dari satu nomor: 1 sel
  - baris 23 "0831 4444 5555 / 0896 6666 7777" -> dipakai sebagai HP: 6283144445555; nomor lain dicatat: 6289666667777
- Tanggal diseragamkan ke YYYY-MM-DD: 37
- Tanggal ambigu (bisa hari/bulan atau bulan/hari; dibaca hari/bulan kecuali ada bukti lain): 8 -> baris 2, 5, 6, 11, 12, 13, 14, 41
- Nominal rupiah jadi angka: 34
- Nama/produk/kota dirapikan huruf dan spasinya: 7
- Baris kembar persis (semua kolom sama): 2 grup
  - baris 13 & 14 (Hendra Gunawan)
  - baris 15 & 16 (Toko Maju Jaya)
- Nomor HP sama tetapi nama beda (belum tentu orang yang sama, TIDAK digabung): 3 kelompok
  - baris 2, 3, 4, 5, 6 (Bpk. Budi Santoso / Budi Santosa / Budi Santoso / Santoso Budi)
  - baris 9 & 10 (Muh. Rizal Pratama / Muhammad Rizal Pratama)
  - baris 11 & 12 (Dewi Lestari / Dewi Lestary)
- Nomor HP sama, tetapi isi lain juga ada yang beda (bukan kembar persis): 7 kelompok
  - baris 2, 3, 4, 5, 6
  - baris 7 & 8
  - baris 9 & 10
  - baris 11 & 12
  - baris 22 & 23
  - baris 26 & 27
  - baris 30 & 32
- Nama mirip yang menunggu keputusan: 4 kelompok
  - no. 1: "Budi Santoso" (baris 2 & 3) / "Bpk. Budi Santoso" (baris 4) / "Budi Santosa" (baris 5) / "Santoso Budi" (baris 6)
  - no. 2: "Muh. Rizal Pratama" (baris 9) / "Muhammad Rizal Pratama" (baris 10)
  - no. 3: "Dewi Lestari" (baris 11) / "Dewi Lestary" (baris 12)
  - no. 4: "Yogyakarta" (baris 19 & 21) / "Jogja" (baris 20)
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

Telepon rumah di baris 24 ditulis di kolom `_telepon_rumah` sebagai `="0215550123"` (supaya nol depan tidak hilang di Excel); kolom HP baris itu kosong.

## Verifikasi angka
- Grup nomor sama (laporan `nomor_hp_sama`): 6281234500101 (5 baris), 6285770000202 (2), 6289900003030 (2), 6281355500404 (2), 6283144445555 (2), 6281377779999 (2), 6285122221111 (2) = 7 grup. Dihitung ulang terpisah dari kolom HP bersih: total 9 nomor dipakai >1 baris; 2 di antaranya (6287811112222, 6281122223333) adalah baris kembar persis dan sudah tercatat di grup duplikat persis, sehingga tidak dihitung dua kali.
- Mode transaksi (contoh 01) tidak menandai nomor sama; mode daftar menandai. Pembeda ini disengaja: pelanggan yang membeli berulang itu wajar di data transaksi.
- Format Excel: sel HP berbentuk `="6281234500101"`. Uji: berkas dibuka kembali dengan pembaca CSV standar; isinya tepat bentuk itu.
