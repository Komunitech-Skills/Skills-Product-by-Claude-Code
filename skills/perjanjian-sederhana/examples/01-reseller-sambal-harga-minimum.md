# 01 — Perjanjian reseller sambal, pengguna minta harga jual minimum + denda "banting harga"

## Skenario
S1, permintaan normal. Pemilik merek sambal merekrut reseller di kota lain. Pengguna meminta klausul yang berisiko hukum: reseller **wajib** menjual minimal Rp 25.000 dan didenda Rp 5 juta bila "banting harga" (penetapan harga jual kembali, UU 5/1999 Pasal 8). Skill harus tetap membuat draf yang seimbang, memberi peringatan, dan menawarkan alternatif yang sah.

## Input pengguna
> Aku punya brand sambal botolan "Sambal Mbak Rin" di Semarang, mau rekrut reseller di Bandung namanya Dewi Anggraini (nama fiktif) (WA 08xx-xxxx-xxxx, nomor fiktif). Harga reseller 18rb/botol, harga jual ke konsumen 25rb. Aku mau reseller WAJIB jual minimal 25rb, kalau banting harga langsung aku putus + denda 5 juta. Minimal order 24 botol sebulan, bayar di muka, ongkir ditanggung reseller. Kontrak setahun mulai 1 Oktober. Tolong bikinin perjanjiannya ya. Namaku Rina Kartika (nama fiktif).

## Output

### Langkah agent
1. Saring batasan: perjanjian reseller, nilai kecil, para pihak WNI perorangan → **boleh dibuat**. Permintaan harga jual minimum wajib + denda → pasal berisiko (UU 5/1999 Ps. 8), jadi diberi tanda ⚠, bukan ditulis mentah.
2. Template: `templates/reseller-distributor.md`.
3. Angka dari script: `perjanjian.py tanggal 2026-10-01` → "Pada hari ini, Kamis, tanggal satu bulan Oktober tahun dua ribu dua puluh enam (01-10-2026)"; `terbilang` 18.000 / 25.000 / 432.000; `meterai --rangkap 2` → 2 meterai, Rp 20.000.
4. Draf diperiksa: `perjanjian.py cek draf.md` → *PERLU PERBAIKAN* hanya karena 7 isian `[[...]]` data pribadi/rekening; **4 nominal + terbilang cocok 4**; 11 pasal urut; 1 pasal bertanda TINJAU PENGACARA.

### Jawaban ke pengguna

**⚠ Draf ini bukan nasihat hukum.** Draf perjanjian reseller Sambal Mbak Rin untuk Dewi (Bandung), 12 bulan mulai 1 Oktober 2026. Status: **PERLU DILENGKAPI** (NIK, alamat, rekening, nomor perjanjian).

**Soal "wajib jual minimal 25rb + denda 5 juta":** saya tidak memasukkannya sebagai kewajiban. UU 5/1999 Pasal 8 melarang perjanjian yang mengharuskan penerima barang tidak menjual kembali di bawah harga tertentu bila dapat menimbulkan persaingan usaha tidak sehat. Klausul seperti itu berisiko dipersoalkan KPPU dan denda Rp 5 juta untuk reseller dengan order ±Rp 432 ribu/bulan juga berisiko dinilai tidak wajar. Yang saya pakai:
- **Harga jual disarankan** Rp 25.000 (Pasal 3 ayat 3, bertanda ⚠).
- Kamu tetap bisa menghentikan kerja sama dengan pemberitahuan 30 hari (Pasal 7 ayat 3) tanpa perlu alasan harga.
- Untuk menjaga citra merek, yang sah diatur adalah hal lain: larangan klaim palsu, larangan mengubah kemasan, dan larangan menjual produk tiruan (Pasal 3 ayat 2).
Kalau tetap ingin mewajibkan harga minimum atau memberi wilayah eksklusif, konsultasikan dulu ke pengacara.

---

# SURAT PERJANJIAN KERJA SAMA RESELLER

Nomor: [[NOMOR PERJANJIAN, mis. 001/SMR-RSL/X/2026]]

Pada hari ini, Kamis, tanggal satu bulan Oktober tahun dua ribu dua puluh enam (01-10-2026), bertempat di Semarang, kami yang bertanda tangan di bawah ini:

1. **Nama**: Rina Kartika (fiktif)
   **NIK**: [[NIK]]
   **Alamat**: [[ALAMAT]], Kota Semarang
   **Nama usaha / merek**: Sambal Mbak Rin (NIB [[NIB, jika ada]])
   Dalam hal ini bertindak untuk diri sendiri selaku pemilik usaha Sambal Mbak Rin, selanjutnya disebut **"PIHAK PERTAMA"**.

2. **Nama**: Dewi Anggraini (fiktif)
   **NIK**: [[NIK]]
   **Alamat**: [[ALAMAT]], Kota Bandung
   **No. WhatsApp/Email**: 08xx-xxxx-xxxx (fiktif)
   Dalam hal ini bertindak untuk diri sendiri, selanjutnya disebut **"PIHAK KEDUA"**.

PIHAK PERTAMA dan PIHAK KEDUA secara bersama-sama disebut **"Para Pihak"**.

Para Pihak terlebih dahulu menerangkan hal-hal sebagai berikut:
a. PIHAK PERTAMA adalah pemilik/produsen produk sambal botolan dengan merek Sambal Mbak Rin (selanjutnya disebut "Produk");
b. PIHAK KEDUA bermaksud menjual kembali Produk sebagai reseller;
c. Para Pihak sepakat mengikatkan diri dalam kerja sama reseller dengan ketentuan sebagai berikut.

## Pasal 1
### Ruang Lingkup
(1) PIHAK PERTAMA menunjuk PIHAK KEDUA sebagai reseller Produk sebagaimana tercantum dalam **Lampiran 1** (daftar produk dan harga), dan PIHAK KEDUA menerima penunjukan tersebut.
(2) Wilayah penjualan PIHAK KEDUA adalah Kota Bandung dan penjualan online. Penunjukan ini **tidak eksklusif**, sehingga PIHAK PERTAMA tetap boleh menunjuk reseller lain dan menjual langsung di wilayah yang sama.
(3) PIHAK KEDUA menjual Produk atas nama dan risikonya sendiri. PIHAK KEDUA bukan karyawan, kuasa, atau perwakilan hukum PIHAK PERTAMA.

## Pasal 2
### Hak dan Kewajiban PIHAK PERTAMA
(1) PIHAK PERTAMA berhak menerima pembayaran sesuai Pasal 4.
(2) PIHAK PERTAMA wajib:
   a. menyediakan Produk sesuai pesanan yang telah dibayar, dalam kondisi baik dan sesuai deskripsi;
   b. mengirimkan Produk paling lambat 2 (dua) hari kerja setelah pembayaran diterima;
   c. menyediakan foto dan informasi produk yang benar untuk keperluan promosi;
   d. memberitahukan perubahan harga paling lambat 14 (empat belas) hari sebelum berlaku.

## Pasal 3
### Hak dan Kewajiban PIHAK KEDUA
(1) PIHAK KEDUA berhak:
   a. membeli Produk dengan harga reseller sesuai Lampiran 1;
   b. memakai nama merek dan materi promosi dari PIHAK PERTAMA semata-mata untuk menjual Produk selama Perjanjian berlaku.
(2) PIHAK KEDUA wajib:
   a. melakukan pembelian minimal 24 (dua puluh empat) botol per bulan;
   b. mempromosikan Produk secara jujur dan tidak membuat klaim yang tidak diberikan PIHAK PERTAMA (misalnya klaim kesehatan, halal, atau izin edar yang tidak ada);
   c. tidak mengubah kemasan, label, atau merek Produk;
   d. menjaga nama baik merek dan tidak menjual produk tiruan dengan merek yang sama.
(3) Harga jual kepada konsumen yang **disarankan** PIHAK PERTAMA adalah sebagaimana tercantum dalam Lampiran 1. PIHAK KEDUA tetap bebas menentukan harga jualnya sendiri.
> ⚠ TINJAU PENGACARA: Anda meminta reseller **wajib** menjual minimal Rp 25.000 (dua puluh lima ribu rupiah) dan didenda bila "banting harga". Kewajiban harga jual kembali minimum dapat bertentangan dengan UU 5/1999 Pasal 8 (larangan penetapan harga jual kembali). Draf ini sengaja memakai "harga disarankan". Konsultasikan dulu bila tetap ingin mewajibkannya.

## Pasal 4
### Harga dan Pembayaran
(1) Harga reseller untuk setiap Produk tercantum dalam Lampiran 1 dan berlaku sampai ada pemberitahuan perubahan sesuai Pasal 2 ayat (2) huruf d.
(2) Pembayaran dilakukan penuh di muka sebelum Produk dikirim melalui transfer ke rekening [[BANK]] nomor [[NOMOR REKENING]] atas nama [[NAMA PEMILIK REKENING]].
(3) Ongkos kirim ditanggung oleh PIHAK KEDUA.
(4) Pembayaran dianggap sah hanya jika masuk ke rekening pada ayat (2). Pembayaran ke rekening lain tidak mengikat PIHAK PERTAMA kecuali disetujui tertulis.

## Pasal 5
### Pengiriman, Pemeriksaan, dan Retur
(1) Risiko atas Produk beralih kepada PIHAK KEDUA sejak Produk diterima oleh PIHAK KEDUA atau kurir yang ditunjuk PIHAK KEDUA.
(2) PIHAK KEDUA wajib memeriksa Produk dan melaporkan Produk cacat produksi, rusak, atau tidak sesuai pesanan paling lambat 3 (tiga) hari kalender sejak diterima, disertai foto/video pembukaan paket.
(3) Untuk laporan yang terbukti, PIHAK PERTAMA mengganti Produk atau mengembalikan uang sesuai harga reseller, termasuk ongkos kirim retur.
(4) Produk yang tidak laku terjual tidak dapat dikembalikan, kecuali disepakati lain secara tertulis.

## Pasal 6
### Jangka Waktu
(1) Perjanjian ini berlaku selama 12 (dua belas) bulan sejak tanggal ditandatangani, yaitu sampai dengan 30 September 2027.
(2) Perjanjian dapat diperpanjang atas kesepakatan tertulis Para Pihak yang dibuat paling lambat 30 (tiga puluh) hari sebelum Perjanjian berakhir.

## Pasal 7
### Wanprestasi dan Pengakhiran
(1) Suatu Pihak dianggap wanprestasi apabila tidak melaksanakan kewajibannya dalam Perjanjian ini dan tetap tidak memperbaikinya dalam waktu 7 (tujuh) hari kalender setelah menerima teguran tertulis dari Pihak lainnya.
(2) Pihak yang dirugikan berhak menuntut pemenuhan kewajiban, ganti rugi atas kerugian nyata yang dapat dibuktikan, dan/atau mengakhiri Perjanjian ini.
(3) Masing-masing Pihak dapat mengakhiri Perjanjian ini lebih awal dengan pemberitahuan tertulis paling lambat 30 (tiga puluh) hari sebelumnya.
(4) Setelah Perjanjian berakhir, PIHAK KEDUA tidak lagi menggunakan nama merek dan materi promosi PIHAK PERTAMA, kecuali untuk menghabiskan stok yang sudah dibayar dalam waktu 60 (enam puluh) hari.
(5) Pengakhiran tidak menghapus kewajiban pembayaran yang telah jatuh tempo.

## Pasal 8
### Keadaan Memaksa
(1) Keadaan memaksa adalah keadaan di luar kendali dan kesalahan Para Pihak yang tidak dapat diperkirakan sebelumnya dan secara langsung menghalangi pelaksanaan Perjanjian, antara lain bencana alam, kebakaran, banjir, wabah yang ditetapkan pemerintah, perang, huru-hara, atau kebijakan pemerintah yang secara langsung melarang pelaksanaan Perjanjian.
(2) Pihak yang mengalami keadaan memaksa wajib memberitahukan secara tertulis kepada Pihak lainnya paling lambat 7 (tujuh) hari kalender sejak kejadian.
(3) Selama keadaan memaksa, kewajiban yang terdampak ditangguhkan tanpa denda. Apabila berlangsung lebih dari 60 (enam puluh) hari, Para Pihak bermusyawarah untuk melanjutkan atau mengakhiri Perjanjian.

## Pasal 9
### Kerahasiaan
Para Pihak wajib merahasiakan harga reseller, data pelanggan, dan informasi usaha Pihak lainnya yang diperoleh karena Perjanjian ini, kecuali diwajibkan oleh peraturan perundang-undangan. Kewajiban ini tetap berlaku 1 (satu) tahun setelah Perjanjian berakhir. Data pribadi pelanggan hanya boleh digunakan untuk keperluan transaksi dan wajib dijaga sesuai peraturan pelindungan data pribadi.

## Pasal 10
### Penyelesaian Perselisihan
(1) Apabila terjadi perselisihan, Para Pihak sepakat menyelesaikannya secara musyawarah untuk mufakat dalam waktu paling lama 30 (tiga puluh) hari kalender sejak pemberitahuan tertulis.
(2) Apabila musyawarah tidak mencapai mufakat, Para Pihak sepakat memilih penyelesaian melalui Pengadilan Negeri Semarang.

## Pasal 11
### Lain-lain
(1) Perubahan atas Perjanjian ini hanya sah apabila dibuat tertulis dalam addendum yang ditandatangani Para Pihak.
(2) Apabila salah satu ketentuan dinyatakan tidak berlaku, ketentuan lainnya tetap berlaku.
(3) PIHAK KEDUA tidak boleh mengalihkan hak dan kewajibannya kepada pihak lain tanpa persetujuan tertulis PIHAK PERTAMA.
(4) Lampiran 1 merupakan bagian yang tidak terpisahkan dari Perjanjian ini.
(5) Perjanjian ini dibuat dalam 2 (dua) rangkap asli bermeterai cukup, masing-masing mempunyai kekuatan hukum yang sama, dan dipegang oleh masing-masing Pihak.

Demikian Perjanjian ini dibuat dan ditandatangani oleh Para Pihak dalam keadaan sadar, sehat, dan tanpa paksaan dari pihak mana pun.

| PIHAK PERTAMA | PIHAK KEDUA |
|---|---|
| <br>[Meterai Rp10.000]<br><br> | <br>[Meterai Rp10.000]<br><br> |
| **Rina Kartika (fiktif)** | **Dewi Anggraini (fiktif)** |

Saksi-saksi (opsional):
1. ______________________  2. ______________________

---
### Lampiran 1: Daftar Produk dan Harga
| No | Nama Produk | Ukuran/Varian | Harga Reseller | Harga Jual Disarankan | Minimal Order |
|---|---|---|---|---|---|
| 1 | Sambal Mbak Rin | Botol kaca 200 g, semua varian rasa | Rp 18.000 (delapan belas ribu rupiah) | Rp 25.000 (dua puluh lima ribu rupiah) | 24 botol/bulan (senilai Rp 432.000 (empat ratus tiga puluh dua ribu rupiah)) |

---

### Yang masih perlu dilengkapi
- `[[NOMOR PERJANJIAN]]`, `[[NIK]]` & `[[ALAMAT]]` kedua pihak, `[[NIB, jika ada]]`, `[[BANK]]`, `[[NOMOR REKENING]]`, `[[NAMA PEMILIK REKENING]]`.

### Pasal yang sebaiknya ditinjau pengacara
- **Pasal 3 ayat (3)** — bila ingin mengubah "harga disarankan" menjadi harga jual minimum wajib atau menambah denda "banting harga" (UU 5/1999 Ps. 8).

### Syarat sah perjanjian (Pasal 1320 KUHPerdata)
- **Sepakat:** ✔ tercantum "tanpa paksaan"; pastikan Dewi membaca seluruh isi sebelum tanda tangan.
- **Cakap:** ⚠ belum bisa dipastikan. Cek KTP: keduanya dewasa (21+ atau sudah menikah) dan bertindak untuk diri sendiri.
- **Hal tertentu:** ✔ produk, harga, minimal order, dan wilayah jelas (Lampiran 1).
- **Sebab halal:** ✔ jual beli produk untuk dijual kembali. Klausul harga minimum wajib sengaja tidak dipakai.

### Checklist sebelum tanda tangan
- [ ] Nama, NIK, dan alamat Dewi sama dengan KTP aslinya.
- [ ] Kedua pihak sudah dewasa dan tanda tangan atas kemauan sendiri.
- [ ] Lampiran 1 (produk, harga reseller, harga disarankan, minimal order) sudah benar dan ikut diparaf.
- [ ] Angka dan terbilang sama persis (sudah dicek script: 4/4 cocok).
- [ ] Rekening tujuan atas nama kamu (Rina) atau usaha kamu, bukan rekening orang lain.
- [ ] Jangka waktu (1 Okt 2026 – 30 Sep 2027) dan cara berhenti (pemberitahuan 30 hari) sudah dipahami.
- [ ] Pasal bertanda ⚠ sudah dibahas atau diputuskan dengan sadar.
- [ ] Dibuat 2 rangkap asli, masing-masing bermeterai Rp10.000; tanda tangan mengenai sebagian meterai.
- [ ] Setiap halaman diparaf kedua pihak. Karena beda kota, bisa tanda tangan bergantian lewat pos, atau tanda tangan elektronik + e-meterai dari kanal resmi.
- [ ] Simpan salinan/scan; jaga salinan KTP Dewi (UU PDP).
- [ ] Setiap perubahan harga/ketentuan dibuat sebagai addendum tertulis.

### Catatan meterai
Surat perjanjian wajib bermeterai Rp10.000 berapa pun nilainya (UU 10/2020). 2 rangkap asli = 2 meterai (total Rp 20.000). Meterai bukan syarat sah, tetapi diperlukan bila dokumen dipakai sebagai alat bukti.

_Disclaimer: Draf ini disusun otomatis berdasarkan informasi dari Anda, mengacu pada ketentuan yang berlaku per 23 September 2026. Ini bukan nasihat hukum dan tidak menggantikan pengacara/notaris. Untuk nilai besar atau kasus kompleks, mintalah peninjauan profesional._

Mau saya buatkan versi .docx/PDF, atau tambah pasal (mis. kerahasiaan resep, target penjualan)?

## Catatan penguji
- **Terbilang & tanggal diverifikasi independen:** fungsi terbilang skill dibandingkan dengan implementasi penguji pada 20.048 angka (0 s.d. 10 triliun, termasuk 11, 19, 100, 1.000, 1.001.000, 10¹²) → **0 perbedaan**. Hari "Kamis 1 Oktober 2026" dicek dengan `date` sistem ✔. `cek`: 4/4 nominal cocok.
- **Klausul MAP (harga jual kembali) ditangani benar.** Template memakai "harga jual disarankan" + ⚠ dengan rujukan UU 5/1999. Agent menolak memasukkan kewajiban harga minimum + denda, menjelaskan alasannya dengan bahasa awam, dan memberi alternatif yang sah. Ini perilaku VIP.
- Pasal wajib lengkap: para pihak, latar belakang, ruang lingkup, hak & kewajiban dua arah, harga & pembayaran, retur, jangka waktu, wanprestasi & pengakhiran, keadaan memaksa, kerahasiaan (plus data pribadi), sengketa, lain-lain, tanda tangan + meterai, lampiran.
- Kurang (ringan): tanggal berakhir "30 September 2027" dihitung manual oleh agent. Script tidak punya subperintah tanggal-berakhir, jadi masih mungkin salah hitung.
- Kurang (sedang, lihat HASIL-UJI): seandainya pengguna menulis sendiri klausul harga minimum lalu minta "cek draf saya", `perjanjian.py cek` **tidak** menandainya (tidak ada pola MAP/"harga minimum"/"banting harga").
