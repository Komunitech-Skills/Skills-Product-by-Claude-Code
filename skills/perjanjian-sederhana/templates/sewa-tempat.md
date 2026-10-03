<!--
PANDUAN AGENT (hapus blok ini dari hasil akhir)
Jenis: sewa tempat usaha (kios, ruko, lapak, rumah untuk usaha, gudang, booth).
PIHAK PERTAMA = pemilik/yang menyewakan. PIHAK KEDUA = penyewa.
Info wajib: identitas kedua pihak, alamat & luas objek, bukti kepemilikan (jenis & nomor sertifikat atau dasar hak menyewakan), peruntukan usaha, jangka waktu, harga sewa & cara bayar, uang jaminan (deposit), siapa bayar listrik/air/PBB/iuran, kota sengketa.
Default: sewa 1 tahun dibayar penuh di muka; deposit 1 bulan sewa dikembalikan 14 hari setelah serah terima kembali; listrik/air/iuran lingkungan ditanggung penyewa; PBB ditanggung pemilik; renovasi harus izin tertulis. Kios pasar: iuran/retribusi pengelola pasar default ditanggung penyewa (Pasal 5); tulis pihak yang SAMA di daftar asumsi, jangan disebut di kewajiban pemilik.
Peringatan wajib ditampilkan ke pengguna:
- Jika yang menyewakan BUKAN pemilik di sertifikat → minta surat kuasa/izin pemilik; jika sewa ulang (sublet) → minta izin tertulis pemilik asli.
- Jika objek harta bersama suami-istri → persetujuan tertulis pasangan pemilik.
- Kios/los di PASAR, MAL, atau pusat belanja sering berstatus hak pakai/sewa dari pengelola (PD Pasar, pengelola gedung). Orang yang "menyewakan" mungkin hanya pemegang hak pakai: minta bukti hak pakai/kartu kios dan IZIN TERTULIS pengelola untuk menyewakan ulang; cek juga aturan pengelola (jam buka, jenis usaha, iuran). Ganti huruf a latar belakang: "pemegang hak pakai atas kios ... berdasarkan ... dari [pengelola]" dan lampirkan izin pengelola.
- Tanggal berakhir sewa dihitung dengan: perjanjian.py sampai YYYY-MM-DD --tahun 1 (atau --bulan N).
- Sewa > 5 tahun, nilai >= Rp500 juta, sewa tanah untuk dibangun penyewa (bangun-guna-serah), atau ada opsi membeli → rujuk pengacara/notaris.
- Ada ketentuan PPh atas sewa tanah/bangunan; jangan hitung, arahkan ke konsultan pajak/DJP.
-->
# PERJANJIAN SEWA-MENYEWA TEMPAT USAHA

Nomor: [[NOMOR PERJANJIAN]]

[[KALIMAT PEMBUKA TANGGAL]], bertempat di [[KOTA]], kami yang bertanda tangan di bawah ini:

1. **Nama**: [[NAMA PIHAK PERTAMA]]
   **NIK**: [[NIK]]
   **Alamat**: [[ALAMAT]]
   Bertindak untuk diri sendiri selaku pemilik objek sewa [[atau: selaku kuasa dari ... berdasarkan Surat Kuasa tanggal ...]], selanjutnya disebut **"PIHAK PERTAMA"** atau **"Pemilik"**.

2. **Nama**: [[NAMA PIHAK KEDUA]]
   **NIK**: [[NIK]]
   **Alamat**: [[ALAMAT]]
   Bertindak untuk diri sendiri, selanjutnya disebut **"PIHAK KEDUA"** atau **"Penyewa"**.

Para Pihak terlebih dahulu menerangkan:
a. PIHAK PERTAMA adalah pemilik sah atas [[JENIS BANGUNAN, mis. 1 (satu) unit kios]] yang terletak di [[ALAMAT LENGKAP OBJEK]], dengan luas kurang lebih [[LUAS]] m², berdasarkan [[JENIS & NOMOR BUKTI HAK, mis. SHM No. ... atas nama ...]] (selanjutnya disebut **"Objek Sewa"**);
b. PIHAK KEDUA bermaksud menyewa Objek Sewa untuk kegiatan usaha [[JENIS USAHA]];
c. Para Pihak sepakat membuat Perjanjian Sewa-Menyewa dengan ketentuan sebagai berikut.

## Pasal 1
### Objek Sewa dan Peruntukan
(1) PIHAK PERTAMA menyewakan kepada PIHAK KEDUA Objek Sewa beserta fasilitas sebagaimana tercantum dalam **Lampiran 1** (berita acara kondisi dan fasilitas), dan PIHAK KEDUA menerima sewa tersebut.
(2) Objek Sewa hanya digunakan untuk usaha [[JENIS USAHA]] dan tidak boleh digunakan untuk kegiatan yang melanggar hukum, kesusilaan, atau ketertiban lingkungan.

## Pasal 2
### Jangka Waktu
(1) Sewa berlangsung selama [[1]] ([[satu]]) tahun, terhitung sejak [[TANGGAL MULAI]] sampai dengan [[TANGGAL BERAKHIR]].
(2) PIHAK KEDUA mendapat prioritas memperpanjang sewa dengan menyampaikan permohonan tertulis paling lambat [[60]] ([[enam puluh]]) hari sebelum sewa berakhir. Harga dan syarat perpanjangan disepakati kemudian secara tertulis.

## Pasal 3
### Harga Sewa dan Pembayaran
(1) Harga sewa adalah [[Rp ... (terbilang)]] untuk seluruh jangka waktu sewa.
(2) Harga sewa dibayar [[PILIH: sekaligus di muka paling lambat pada tanggal ... / bertahap sesuai jadwal pada ayat (3)]] melalui transfer ke rekening [[BANK]] nomor [[NOMOR REKENING]] atas nama [[NAMA PEMILIK REKENING]]. Setiap pembayaran dibuatkan kuitansi.
(3) [[JADWAL TERMIN, jika bertahap. Hitung dengan: perjanjian.py termin]]
(4) PIHAK KEDUA menyerahkan uang jaminan (deposit) sebesar [[Rp ... (terbilang)]] pada saat penandatanganan. Uang jaminan dikembalikan tanpa bunga paling lambat [[14]] ([[empat belas]]) hari setelah Objek Sewa diserahkan kembali, setelah dikurangi biaya perbaikan kerusakan dan tagihan yang belum dibayar PIHAK KEDUA (dengan rincian tertulis).
(5) Kewajiban pajak yang timbul dari sewa ini dipenuhi oleh Pihak yang diwajibkan sesuai peraturan perpajakan yang berlaku.

## Pasal 4
### Hak dan Kewajiban PIHAK PERTAMA
(1) PIHAK PERTAMA berhak menerima harga sewa tepat waktu dan memeriksa kondisi Objek Sewa dengan pemberitahuan terlebih dahulu paling lambat [[1]] ([[satu]]) hari sebelumnya.
(2) PIHAK PERTAMA wajib:
   a. menyerahkan Objek Sewa dalam keadaan baik dan dapat digunakan pada tanggal mulai sewa;
   b. menjamin bahwa Objek Sewa tidak dalam sengketa, tidak sedang dijaminkan dengan cara yang dapat mengganggu penyewaan, dan PIHAK KEDUA dapat menikmati Objek Sewa dengan tenteram selama masa sewa;
   c. menanggung perbaikan besar (struktur bangunan, atap, instalasi utama) yang bukan akibat kesalahan PIHAK KEDUA;
   d. membayar Pajak Bumi dan Bangunan (PBB) atas Objek Sewa.

## Pasal 5
### Hak dan Kewajiban PIHAK KEDUA
(1) PIHAK KEDUA berhak menggunakan Objek Sewa sesuai peruntukan selama masa sewa.
(2) PIHAK KEDUA wajib:
   a. membayar harga sewa sesuai Pasal 3;
   b. membayar biaya pemakaian listrik, air, internet, kebersihan, keamanan, dan iuran lingkungan selama masa sewa;
   c. merawat Objek Sewa dan menanggung perbaikan kecil akibat pemakaian sehari-hari;
   d. tidak mengubah, membongkar, atau merenovasi Objek Sewa tanpa persetujuan tertulis PIHAK PERTAMA;
   e. tidak menyewakan kembali atau mengalihkan Objek Sewa kepada pihak lain tanpa persetujuan tertulis PIHAK PERTAMA;
   f. mengurus sendiri izin usaha yang diperlukan untuk kegiatan usahanya;
   g. menyerahkan kembali Objek Sewa pada akhir masa sewa dalam keadaan seperti semula, kecuali aus karena pemakaian wajar.
(3) Barang tambahan yang dipasang PIHAK KEDUA dengan persetujuan boleh dibongkar dan dibawa pada akhir sewa, dengan mengembalikan kondisi seperti semula. Barang yang tertinggal lebih dari [[7]] ([[tujuh]]) hari setelah sewa berakhir dianggap ditinggalkan dan dapat disingkirkan PIHAK PERTAMA atas biaya PIHAK KEDUA.

## Pasal 6
### Pengalihan Kepemilikan
Apabila Objek Sewa dijual atau dialihkan selama masa sewa, sewa tetap berlaku sampai berakhirnya jangka waktu sewa, dan PIHAK PERTAMA wajib memberitahukan perjanjian ini kepada pemilik baru.

## Pasal 7
### Wanprestasi dan Pengakhiran
(1) Suatu Pihak dianggap wanprestasi apabila tidak melaksanakan kewajibannya dan tetap tidak memperbaikinya dalam waktu [[14]] ([[empat belas]]) hari kalender setelah menerima teguran tertulis.
(2) Keterlambatan pembayaran sewa bertahap dikenakan denda [[0,1]]% ([[nol koma satu persen]]) per hari dari jumlah yang terlambat, paling banyak [[5]]% ([[lima persen]]).
(3) Apabila PIHAK KEDUA wanprestasi, PIHAK PERTAMA berhak mengakhiri sewa dan PIHAK KEDUA wajib mengosongkan Objek Sewa paling lambat [[14]] ([[empat belas]]) hari setelah pemberitahuan pengakhiran. Sisa uang sewa yang telah dibayar untuk periode setelah pengakhiran [[PILIH: dikembalikan secara proporsional / tidak dikembalikan]].
> ⚠ TINJAU PENGACARA: pilihan sisa uang sewa tidak dikembalikan, serta pengosongan tanpa putusan pengadilan, sebaiknya dikonsultasikan. Pengosongan paksa tanpa proses hukum dapat menimbulkan masalah hukum baru.
(4) Apabila PIHAK PERTAMA wanprestasi sehingga Objek Sewa tidak dapat digunakan, PIHAK KEDUA berhak mengakhiri sewa dan menerima kembali sisa uang sewa secara proporsional beserta uang jaminan.

## Pasal 8
### Keadaan Memaksa
(1) Keadaan memaksa adalah keadaan di luar kendali dan kesalahan Para Pihak yang tidak dapat diperkirakan sebelumnya, antara lain bencana alam, kebakaran yang bukan karena kelalaian Para Pihak, banjir, wabah yang ditetapkan pemerintah, huru-hara, atau kebijakan pemerintah yang secara langsung melarang penggunaan Objek Sewa.
(2) Pihak yang mengalami keadaan memaksa wajib memberitahukan secara tertulis paling lambat [[7]] ([[tujuh]]) hari kalender sejak kejadian.
(3) Apabila Objek Sewa tidak dapat digunakan karena keadaan memaksa lebih dari [[30]] ([[tiga puluh]]) hari, Para Pihak bermusyawarah mengenai perpanjangan masa sewa sebagai pengganti atau pengembalian sisa uang sewa secara proporsional.

## Pasal 9
### Penyelesaian Perselisihan
(1) Perselisihan diselesaikan secara musyawarah untuk mufakat dalam waktu paling lama [[30]] ([[tiga puluh]]) hari kalender sejak pemberitahuan tertulis.
(2) Apabila musyawarah tidak mencapai mufakat, Para Pihak sepakat memilih penyelesaian melalui Pengadilan Negeri [[KOTA LOKASI OBJEK SEWA]].

## Pasal 10
### Lain-lain
(1) Perubahan Perjanjian hanya sah apabila dibuat tertulis dalam addendum yang ditandatangani Para Pihak.
(2) Apabila salah satu ketentuan dinyatakan tidak berlaku, ketentuan lainnya tetap berlaku.
(3) Lampiran 1 merupakan bagian yang tidak terpisahkan dari Perjanjian ini.
(4) Perjanjian ini dibuat dalam 2 (dua) rangkap asli bermeterai cukup, masing-masing mempunyai kekuatan hukum yang sama.

Demikian Perjanjian ini dibuat dan ditandatangani oleh Para Pihak dalam keadaan sadar dan tanpa paksaan.

| PIHAK PERTAMA (Pemilik) | PIHAK KEDUA (Penyewa) |
|---|---|
| <br>[Meterai Rp10.000]<br><br> | <br>[Meterai Rp10.000]<br><br> |
| **[[NAMA PIHAK PERTAMA]]** | **[[NAMA PIHAK KEDUA]]** |

Menyetujui (bila Objek Sewa harta bersama): ______________________ (suami/istri Pemilik)

Saksi-saksi (opsional): 1. ______________________  2. ______________________

---
### Lampiran 1: Berita Acara Kondisi dan Fasilitas Objek Sewa
| No | Bagian/Fasilitas | Kondisi saat serah terima | Keterangan/foto |
|---|---|---|---|
| 1 | [[mis. Pintu rolling door]] | [[baik/rusak ringan]] | [[...]] |
| 2 | [[Listrik: daya ... VA, meter no. ...]] | [[...]] | [[angka meter awal]] |
| 3 | [[Air: PDAM/sumur, meter no. ...]] | [[...]] | [[angka meter awal]] |
Kunci diserahkan: [[jumlah]] buah. Ditandatangani Para Pihak pada saat serah terima.
