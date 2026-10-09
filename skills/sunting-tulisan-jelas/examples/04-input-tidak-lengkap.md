# Contoh 4: tulisan kurang konteks (input tidak lengkap)

**Permintaan pengguna:** "Rapikan pesan WA ini ke Bu Rina biar jelas."

## Tulisan asli
```
Bu Rina, terkait hal yang kemarin itu sudah saya tindaklanjuti ya, nanti kalau sudah ada perkembangan akan segera saya kabari. Mohon ditunggu sebentar.
```

## Balasan agent (yang dilihat pengguna)

**Versi suntingan**
```
Bu Rina, soal [cek: hal yang dimaksud, mis. "pesanan nomor ..."] yang kemarin, sudah saya tangani. Kalau sudah ada perkembangan, saya kabari [cek: kapan, mis. "hari ini"]. Mohon ditunggu sebentar.
```

**Yang saya ubah**
- Kata kabur "hal yang kemarin itu" dan "segera" tidak bisa dijernihkan tanpa info dari pengirim, jadi saya tidak menebak. Keduanya diberi tanda [cek: ...].
- "terkait" dan "tindaklanjuti" diganti "soal" dan "tangani"; tulisan dipecah dari dua jadi tiga kalimat.

Dua hal yang perlu Anda isi sebelum dikirim:
1. Hal yang kemarin itu sebenarnya soal apa (pesanan, pembayaran, jadwal)?
2. Kapan Bu Rina akan dikabari?

(Kalau pengguna hanya menulis "tolong rapikan tulisan saya" tanpa menempelkan teks, balasan agent hanya satu kalimat: "Silakan tempel tulisannya di sini, saya rapikan. Kalau mau, sebut juga siapa yang akan membacanya dan tujuannya (mis. minta persetujuan).")


## Ukuran (keluaran `scripts/ukur_keterbacaan.py --sebelum ... --sesudah ...`, dijalankan sungguhan)
```
Perbandingan sebelum -> sesudah
  Ukuran                           Sebelum   Sesudah
  Jumlah kata                           23        29
  Jumlah kalimat                         2         3
  Rata-rata kata per kalimat          11.5       9.7
  Kalimat > 25 kata (%)                0.0       0.0
  Kalimat terpanjang (kata)             20        15
  Perkiraan kalimat pasif                1         2
  Kata pengisi/jargon/kabur              2         0
  Perubahan panjang: +26% kata
  Angka/tanggal yang HILANG dari suntingan: tidak ada
  Angka/tanggal BARU di suntingan: tidak ada
```
