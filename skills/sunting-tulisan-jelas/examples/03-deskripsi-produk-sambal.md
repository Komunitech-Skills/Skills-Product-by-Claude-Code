# Contoh 3: deskripsi produk yang melambung

**Permintaan pengguna:** "Perjelas deskripsi produk ini buat Shopee dan WA."

## Tulisan asli
```
Sambal Roa Bu Tini

Sambal Roa Bu Tini merupakan produk sambal yang dibuat dengan menggunakan bahan-bahan berkualitas terbaik dan diolah secara higienis sehingga menghasilkan cita rasa yang sangat luar biasa dan cocok untuk dinikmati oleh berbagai kalangan dan berbagai macam hidangan. Sambal ini dibuat dari ikan roa asap pilihan yang dipadukan dengan cabai segar dan rempah-rempah yang diracik secara tradisional, tanpa pengawet, sehingga rasanya pedas gurih yang benar-benar nikmat. Sambal ini dikemas dalam botol kaca isi 250 gram dan dapat disimpan selama 3 bulan pada suhu ruang. Harga hanya Rp38.000 per botol. Untuk pemesanan dapat menghubungi WhatsApp 0812-5550-1122 dan jangan sampai kehabisan karena produk ini terbatas.
```

## Balasan agent (yang dilihat pengguna)

**Versi suntingan**
```
Sambal Roa Bu Tini, Pedas Gurih untuk Segala Lauk

Sambal dari ikan roa asap, cabai segar, dan rempah yang diracik secara tradisional, diolah higienis. Rasanya pedas dan gurih, cocok dimakan dengan nasi, mi, atau gorengan.

Detail produk:
- Isi: 250 gram, dalam botol kaca
- Tahan 3 bulan di suhu ruang
- Tanpa pengawet [cek: apakah memang tanpa pengawet, dan apakah izin PIRT sudah ada?]
- Harga: Rp38.000 per botol

Stok terbatas. Pesan lewat WhatsApp: 0812-5550-1122.
```

**Yang saya ubah**
- Judul diberi manfaat nyata ("Pedas Gurih untuk Segala Lauk") dan kalimat pembuka langsung menyebut bahannya.
- Data produk (isi 250 gram, botol kaca, tahan 3 bulan, harga Rp38.000) dipindah ke daftar supaya pembeli menemukannya dalam sekali lihat.
- Kata kabur "berkualitas terbaik", "sangat luar biasa", "benar-benar nikmat", "berbagai kalangan" dihapus karena tidak bisa dibuktikan; diganti contoh makanan yang cocok (nasi, mi, gorengan). Contoh itu saran penggunaan, bukan klaim baru.
- Klaim "tanpa pengawet" tetap ada tetapi diberi tanda [cek: ...] karena bisa bermasalah bila tidak benar.
- Kalimat "terbatas" dipertahankan jadi "Stok terbatas." tanpa tambahan urgensi baru.

Bila ada bukti kualitas (mis. cabai dari kebun sendiri, jumlah pembeli, izin PIRT), kirim ke saya dan akan saya masukkan.


## Ukuran (keluaran `scripts/ukur_keterbacaan.py --sebelum ... --sesudah ...`, dijalankan sungguhan)
```
Perbandingan sebelum -> sesudah
  Ukuran                           Sebelum   Sesudah
  Jumlah kata                          106        72
  Jumlah kalimat                         6        10
  Rata-rata kata per kalimat          17.7       7.2
  Kalimat > 25 kata (%)               33.3       0.0
  Kalimat terpanjang (kata)             37        15
  Perkiraan kalimat pasif                8         3
  Kata pengisi/jargon/kabur              5         0
  Perubahan panjang: -32% kata
  Angka/tanggal yang HILANG dari suntingan: tidak ada
  Angka/tanggal BARU di suntingan: tidak ada
```
