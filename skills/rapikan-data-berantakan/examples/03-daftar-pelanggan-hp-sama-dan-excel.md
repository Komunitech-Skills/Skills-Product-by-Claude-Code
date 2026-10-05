# 03. Mode daftar: HP sama ditandai, dibuka di Excel

**Pesan pengguna:** "Anggap ini daftar pelanggan (satu orang satu baris), bukan daftar transaksi. Nanti saya buka di Excel."

**Cara dijalankan:** `python3 scripts/rapikan.py examples/data-contoh.csv --jenis daftar --hp-untuk-excel`

## Balasan yang diharapkan
Dalam mode daftar, nomor HP yang sama ditandai sebagai kemungkinan orang yang sama:
- Di luar 2 pasang baris kembar persis (Hendra Gunawan, Toko Maju Jaya; sudah ditandai sebagai duplikat), ada 7 nomor yang dipakai lebih dari satu baris. Tiga di antaranya dengan nama yang tulisannya berbeda: nomor 6281234500101 (Budi Santoso / Bpk. Budi Santoso / Budi Santosa / Santoso Budi, baris 2-6), 6289900003030 (Muh. Rizal Pratama / Muhammad Rizal Pratama, baris 9-10), 6281355500404 (Dewi Lestari / Dewi Lestary, baris 11-12). Itu bukti kuat bahwa nama-nama tersebut satu orang.
- Empat lainnya nama sama, tetapi beda tanggal pesanan (pelanggan yang beli berulang): Siti Rahmawati, Lia Anggraini, Fajar Nugraha, Wulan Sari. Kalau yang Anda butuhkan satu baris per orang, gabungkan manual atau minta saya menyusun daftar unik.
- Nomor HP ditulis dalam bentuk khusus agar Excel tidak mengubahnya menjadi 6,28E+11. File ini baik dibuka di Excel; kalau mau diimpor ke aplikasi lain, bilang saja supaya saya buat versi polos.

## Verifikasi angka
- Grup nomor sama (laporan `nomor_hp_sama`): 6281234500101 (5 baris), 6285770000202 (2), 6289900003030 (2), 6281355500404 (2), 6283144445555 (2), 6281377779999 (2), 6285122221111 (2) = 7 grup. Dihitung ulang terpisah dari kolom HP bersih: total 9 nomor dipakai >1 baris; 2 di antaranya (6287811112222, 6281122223333) adalah baris kembar persis dan sudah tercatat di grup duplikat persis, sehingga tidak dihitung dua kali.
- Mode transaksi (contoh 01) tidak menandai nomor sama; mode daftar menandai. Pembeda ini disengaja: pelanggan yang membeli berulang itu wajar di data transaksi.
- Format Excel: sel HP berbentuk `="6281234500101"`. Uji: berkas dibuka kembali dengan pembaca CSV standar; isinya tepat bentuk itu.
