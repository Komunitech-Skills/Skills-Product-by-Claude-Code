# Contoh 2: pengumuman karyawan penuh jargon

**Permintaan pengguna:** "Sunting pengumuman absensi ini, karyawan toko saya banyak yang nggak ngerti bahasanya."

## Tulisan asli
```
PENGUMUMAN

Kepada seluruh karyawan Toko Sinar Pagi,

Dalam rangka optimalisasi proses pencatatan kehadiran agar lebih efektif dan efisien, manajemen akan mengimplementasikan sistem absensi digital berbasis aplikasi yang akan mulai diberlakukan per tanggal 1 November 2026, sehingga seluruh karyawan diwajibkan untuk melakukan absensi masuk dan pulang melalui aplikasi tersebut pada setiap hari kerja dan keterlambatan lebih dari 15 menit akan dicatat oleh atasan masing-masing.

Sehubungan dengan hal tersebut, akan dilaksanakan sosialisasi terkait cara penggunaan aplikasi pada tanggal 28 Oktober 2026 pukul 15.30 di ruang belakang toko yang diharapkan dapat dihadiri oleh seluruh karyawan tanpa terkecuali, dan bagi karyawan yang berhalangan hadir diharapkan segera melakukan koordinasi dengan Ibu Ratna selaku koordinator.

Demikian pengumuman ini disampaikan untuk dapat dipahami dan dilaksanakan sebagaimana mestinya. Atas perhatian dan kerja samanya diucapkan terima kasih.

Manajemen Toko Sinar Pagi
```

## Balasan agent (yang dilihat pengguna)

**Versi suntingan**
```
PENGUMUMAN: Absen Pakai Aplikasi Mulai 1 November 2026

Kepada seluruh karyawan Toko Sinar Pagi,

Mulai 1 November 2026, semua karyawan absen lewat aplikasi. Yang perlu kalian lakukan:
1. Absen masuk lewat aplikasi setiap datang.
2. Absen pulang lewat aplikasi setiap pulang.

Jika terlambat lebih dari 15 menit, atasan masing-masing akan mencatatnya.

Pelatihan cara memakai aplikasi:
- Tanggal: 28 Oktober 2026
- Jam: 15.30
- Tempat: ruang belakang toko
- Semua karyawan diharapkan hadir, tanpa terkecuali.

Kalau tidak bisa hadir, kabari Ibu Ratna (koordinator) sebelum 28 Oktober [cek: batas waktu memberi kabar belum ada di naskah asli].

Terima kasih.
Manajemen Toko Sinar Pagi
```

**Yang saya ubah**
- Judul pengumuman sekarang langsung berisi isi pokoknya (apa dan mulai kapan).
- Jargon diganti kata sehari-hari: "optimalisasi/efektif dan efisien" dihapus, "mengimplementasikan" jadi "memakai", "sosialisasi" jadi "pelatihan", "koordinasi" jadi "kabari".
- Aturan absen dijadikan daftar bernomor; jadwal pelatihan jadi daftar butir (tanggal, jam, tempat) supaya gampang dicari mata.
- Naskah asli hanya menulis "segera" untuk kabar ketidakhadiran; saya tidak mengarang batas waktu, jadi diberi tanda [cek: ...].
- Tanggal, jam, angka 15 menit, dan nama Ibu Ratna tidak berubah; "diharapkan hadir" tetap "diharapkan" (tidak saya ubah jadi wajib).

Hapus tanda [cek: ...] sebelum pengumuman ditempel atau dikirim.


## Ukuran (keluaran `scripts/ukur_keterbacaan.py --sebelum ... --sesudah ...`, dijalankan sungguhan)
```
Perbandingan sebelum -> sesudah
  Ukuran                           Sebelum   Sesudah
  Jumlah kata                          132        96
  Jumlah kalimat                         7        15
  Rata-rata kata per kalimat          18.9       6.4
  Kalimat > 25 kata (%)               28.6       0.0
  Kalimat terpanjang (kata)             56        21
  Perkiraan kalimat pasif               11         1
  Kata pengisi/jargon/kabur             12         0
  Perubahan panjang: -27% kata
  Angka/tanggal yang HILANG dari suntingan: tidak ada
  Angka/tanggal BARU di suntingan: tidak ada
```
