# Contoh 1: email ke klien yang bertele-tele

**Permintaan pengguna:** "Tolong rapikan email ini ke klien, kepanjangan dan bikin pusing."

## Tulisan asli
```
Yth. Bapak Hendra,

Selamat siang. Sehubungan dengan adanya pesanan kemasan kardus Bapak sebanyak 5.000 pcs dengan nomor pesanan PO-0412, dengan ini kami ingin menyampaikan bahwa pada dasarnya proses produksi yang sedianya dijadwalkan selesai pada tanggal 10 Oktober 2026 dikarenakan adanya keterlambatan pengiriman bahan kertas dari pihak supplier kami maka pengerjaannya akan mengalami penyesuaian jadwal sehingga pengiriman barang kepada Bapak baru dapat kami lakukan pada tanggal 17 Oktober 2026, dan untuk hal tersebut kami mohon pengertian dari Bapak.

Perlu kami informasikan juga bahwa agar proses produksi dapat segera dilanjutkan, kami sangat mengharapkan apabila Bapak berkenan untuk dapat melakukan konfirmasi persetujuan terhadap revisi desain yang telah kami kirimkan melalui email pada tanggal 3 Oktober 2026 paling lambat sebelum tanggal 8 Oktober 2026.

Adapun mengenai pembayaran, uang muka sebesar 50% atau Rp9.375.000 dari total Rp18.750.000 telah kami terima, dan sisanya dilakukan pada saat barang sudah sampai di lokasi Bapak. Demikian kami sampaikan, atas perhatian dan kerja samanya kami ucapkan terima kasih.

Hormat kami,
Dewi, CV Maju Jaya Kemasan
```

## Balasan agent (yang dilihat pengguna)

**Versi suntingan**
```
Yth. Bapak Hendra,

Selamat siang. Pengiriman kemasan kardus Bapak (PO-0412, 5.000 pcs) mundur dari 10 Oktober menjadi 17 Oktober 2026. Pemasok kertas kami terlambat mengirim bahan, sehingga produksi ikut tertunda. Kami mohon pengertian Bapak.

Agar produksi bisa lanjut, kami butuh satu hal dari Bapak: persetujuan revisi desain yang kami kirim lewat email pada 3 Oktober 2026. Mohon balas sebelum 8 Oktober 2026.

Soal pembayaran, uang muka 50% (Rp9.375.000 dari total Rp18.750.000) sudah kami terima. Sisanya dibayar saat barang tiba di lokasi Bapak.

Terima kasih atas perhatian dan kerja samanya, Pak.

Hormat kami,
Dewi, CV Maju Jaya Kemasan
```

**Yang saya ubah**
- Satu kalimat 72 kata dipecah jadi tiga hal terpisah: apa yang mundur, penyebabnya, permintaan maaf/pengertian.
- Kabar utama (pengiriman mundur ke 17 Oktober) dipindah ke kalimat pertama; permintaan ke klien dibuat satu paragraf sendiri dengan tenggat 8 Oktober.
- Pengisi dan kata bertele dibuang ("sehubungan dengan", "pada dasarnya", "dengan ini kami ingin menyampaikan bahwa", "dikarenakan", "apabila").
- Pembayaran dijelaskan dalam dua kalimat pendek; semua angka (5.000 pcs, 50%, Rp9.375.000, Rp18.750.000) tidak berubah.
- Pelaku disebut jelas: "Pemasok kertas kami terlambat mengirim bahan".

Saya anggap pembacanya klien yang sibuk dan nadanya tetap sopan. Kalau Bapak Hendra biasanya dikirimi surat lebih formal, kabari saya.

## Ukuran (keluaran `scripts/ukur_keterbacaan.py --sebelum ... --sesudah ...`, dijalankan sungguhan)
```
Perbandingan sebelum -> sesudah
  Ukuran                           Sebelum   Sesudah
  Jumlah kata                          165        97
  Jumlah kalimat                         8        12
  Rata-rata kata per kalimat          20.6       8.1
  Kalimat > 25 kata (%)               37.5       0.0
  Kalimat terpanjang (kata)             72        22
  Perkiraan kalimat pasif                4         1
  Kata pengisi/jargon/kabur             11         0
  Perubahan panjang: -41% kata
  Angka/tanggal yang HILANG dari suntingan: tidak ada
  Angka/tanggal BARU di suntingan: tidak ada
```
