# 02 — Sewa kios pasar 1 tahun, bayar 2 tahap, deposit

> **Catatan 1.0.9:** isian di contoh ini diseragamkan ke gaya `[isi: ...]` dan kalimat "dicek script" di jawaban diganti "sudah dihitung ulang". Naskah di bawah ditampilkan dalam format berkas/terminal (judul `#`, tabel). Di kanal chat (Telegram/WhatsApp) sejak 1.0.9 naskah yang sama dikirim sebagai teks biasa per "Bagian 1/N" (< 3.800 karakter, dipotong antar-pasal) hasil `perjanjian.py bagi`, tanpa jalur berkas dan tanpa kata script.

## Skenario
S2, permintaan normal. Pemilik kios menyewakan kiosnya ke pedagang pulsa. Pembayaran dua tahap dan ada deposit. Info cukup lengkap, kecuali NIK, alamat, nomor sertifikat, dan rekening.

## Input pengguna
> Saya mau nyewain kios saya di Pasar Fiktif Blok B no 12 Jogja, ukuran 3x4, ke Pak Joko Santoso buat jualan pulsa & aksesoris HP. Setahun 18 juta, bayarnya 2x: separuh pas tanda tangan, separuh 6 bulan lagi. Deposit 1,5 juta. Listrik sama iuran pasar dia yang bayar. Kiosnya SHM atas nama saya, Sri Wahyuni. Mulai 5 Oktober ini. Tolong bikinkan surat perjanjian sewanya.

## Output

### Langkah agent
1. Saring batasan: sewa tempat 1 tahun, Rp 18 juta → dalam cakupan (bukan jual beli tanah, < Rp500 juta, ≤ 5 tahun).
2. Template `templates/sewa-tempat.md`. Peringatan wajib di PANDUAN AGENT ditampilkan (harta bersama, PPh sewa).
3. Script: `tanggal 2026-10-05` (Senin); `termin --total "18 juta" --persen 50,50` → Rp 9.000.000 + Rp 9.000.000, cek total cocok; `terbilang 1.500.000`; `denda --nilai "Rp 9.000.000" --persen-per-hari 0,1 --hari 30 --maks-persen 5` → contoh denda 30 hari Rp 270.000, maksimum Rp 450.000.
4. `cek` → PERLU PERBAIKAN hanya karena isian `[isi: ...]`; **4/4 nominal-terbilang cocok**; 10 pasal urut; 1 pasal ⚠.

### Jawaban ke pengguna

**⚠ Draf ini bukan nasihat hukum.** Draf sewa kios Pasar Fiktif Blok B No. 12 untuk Pak Joko, 5 Oktober 2026 – 4 Oktober 2027, Rp 18.000.000 dibayar 2 tahap + deposit Rp 1.500.000. Status: **PERLU DILENGKAPI**.

Dua hal penting sebelum lanjut:
- Jika kios ini **harta bersama** (dibeli selama menikah), suami/istri Ibu perlu ikut menyetujui secara tertulis. Sudah saya siapkan baris "Menyetujui" di bagian tanda tangan (UU 1/1974 Ps. 36).
- Ada ketentuan **PPh final atas sewa tanah/bangunan**. Saya tidak menghitungnya. Tanyakan ke konsultan pajak/KPP siapa yang memotong/menyetor. Pasal 3 ayat (5) sudah mengaturnya secara umum.

---

# PERJANJIAN SEWA-MENYEWA TEMPAT USAHA

Nomor: [isi: NOMOR PERJANJIAN]

Pada hari ini, Senin, tanggal lima bulan Oktober tahun dua ribu dua puluh enam (05-10-2026), bertempat di Yogyakarta, kami yang bertanda tangan di bawah ini:

1. **Nama**: Sri Wahyuni (fiktif)
   **NIK**: [isi: NIK]
   **Alamat**: [isi: ALAMAT]
   Bertindak untuk diri sendiri selaku pemilik objek sewa, selanjutnya disebut **"PIHAK PERTAMA"** atau **"Pemilik"**.

2. **Nama**: Joko Santoso (fiktif)
   **NIK**: [isi: NIK]
   **Alamat**: [isi: ALAMAT]
   Bertindak untuk diri sendiri, selanjutnya disebut **"PIHAK KEDUA"** atau **"Penyewa"**.

Para Pihak terlebih dahulu menerangkan:
a. PIHAK PERTAMA adalah pemilik sah atas 1 (satu) unit kios yang terletak di Pasar Fiktif Blok B Nomor 12, [isi: KELURAHAN/KECAMATAN], Kota Yogyakarta, dengan luas kurang lebih 12 m² (3 x 4 meter), berdasarkan Sertifikat Hak Milik Nomor [isi: NOMOR SHM] atas nama Sri Wahyuni (fiktif) (selanjutnya disebut **"Objek Sewa"**);
b. PIHAK KEDUA bermaksud menyewa Objek Sewa untuk kegiatan usaha penjualan pulsa, kartu perdana, dan aksesoris telepon seluler;
c. Para Pihak sepakat membuat Perjanjian Sewa-Menyewa dengan ketentuan sebagai berikut.

## Pasal 1
### Objek Sewa dan Peruntukan
(1) PIHAK PERTAMA menyewakan kepada PIHAK KEDUA Objek Sewa beserta fasilitas sebagaimana tercantum dalam **Lampiran 1** (berita acara kondisi dan fasilitas), dan PIHAK KEDUA menerima sewa tersebut.
(2) Objek Sewa hanya digunakan untuk usaha penjualan pulsa, kartu perdana, dan aksesoris telepon seluler dan tidak boleh digunakan untuk kegiatan yang melanggar hukum, kesusilaan, atau ketertiban lingkungan.

## Pasal 2
### Jangka Waktu
(1) Sewa berlangsung selama 1 (satu) tahun, terhitung sejak 5 Oktober 2026 sampai dengan 4 Oktober 2027.
(2) PIHAK KEDUA mendapat prioritas memperpanjang sewa dengan menyampaikan permohonan tertulis paling lambat 60 (enam puluh) hari sebelum sewa berakhir. Harga dan syarat perpanjangan disepakati kemudian secara tertulis.

## Pasal 3
### Harga Sewa dan Pembayaran
(1) Harga sewa adalah Rp 18.000.000 (delapan belas juta rupiah) untuk seluruh jangka waktu sewa.
(2) Harga sewa dibayar bertahap sesuai jadwal pada ayat (3) melalui transfer ke rekening [isi: BANK] nomor [isi: NOMOR REKENING] atas nama [isi: NAMA PEMILIK REKENING]. Setiap pembayaran dibuatkan kuitansi.
(3) Jadwal pembayaran:
   a. pembayaran pertama 50% sebesar Rp 9.000.000 (sembilan juta rupiah) pada saat penandatanganan Perjanjian ini, 5 Oktober 2026;
   b. pembayaran kedua 50% sebesar Rp 9.000.000 (sembilan juta rupiah) paling lambat 5 April 2027.
(4) PIHAK KEDUA menyerahkan uang jaminan (deposit) sebesar Rp 1.500.000 (satu juta lima ratus ribu rupiah) pada saat penandatanganan. Uang jaminan dikembalikan tanpa bunga paling lambat 14 (empat belas) hari setelah Objek Sewa diserahkan kembali, setelah dikurangi biaya perbaikan kerusakan dan tagihan yang belum dibayar PIHAK KEDUA (dengan rincian tertulis).
(5) Kewajiban pajak yang timbul dari sewa ini dipenuhi oleh Pihak yang diwajibkan sesuai peraturan perpajakan yang berlaku.

## Pasal 4
### Hak dan Kewajiban PIHAK PERTAMA
(1) PIHAK PERTAMA berhak menerima harga sewa tepat waktu dan memeriksa kondisi Objek Sewa dengan pemberitahuan terlebih dahulu paling lambat 1 (satu) hari sebelumnya.
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
(3) Barang tambahan yang dipasang PIHAK KEDUA dengan persetujuan boleh dibongkar dan dibawa pada akhir sewa, dengan mengembalikan kondisi seperti semula. Barang yang tertinggal lebih dari 7 (tujuh) hari setelah sewa berakhir dianggap ditinggalkan dan dapat disingkirkan PIHAK PERTAMA atas biaya PIHAK KEDUA.

## Pasal 6
### Pengalihan Kepemilikan
Apabila Objek Sewa dijual atau dialihkan selama masa sewa, sewa tetap berlaku sampai berakhirnya jangka waktu sewa, dan PIHAK PERTAMA wajib memberitahukan perjanjian ini kepada pemilik baru.

## Pasal 7
### Wanprestasi dan Pengakhiran
(1) Suatu Pihak dianggap wanprestasi apabila tidak melaksanakan kewajibannya dan tetap tidak memperbaikinya dalam waktu 14 (empat belas) hari kalender setelah menerima teguran tertulis.
(2) Keterlambatan pembayaran sewa bertahap dikenakan denda 0,1% (nol koma satu persen) per hari dari jumlah yang terlambat, paling banyak 5% (lima persen).
(3) Apabila PIHAK KEDUA wanprestasi, PIHAK PERTAMA berhak mengakhiri sewa dan PIHAK KEDUA wajib mengosongkan Objek Sewa paling lambat 14 (empat belas) hari setelah pemberitahuan pengakhiran. Sisa uang sewa yang telah dibayar untuk periode setelah pengakhiran dikembalikan secara proporsional setelah dikurangi tunggakan dan biaya perbaikan kerusakan.
> ⚠ TINJAU PENGACARA: pilihan sisa uang sewa tidak dikembalikan, serta pengosongan tanpa putusan pengadilan, sebaiknya dikonsultasikan. Pengosongan paksa tanpa proses hukum dapat menimbulkan masalah hukum baru.
(4) Apabila PIHAK PERTAMA wanprestasi sehingga Objek Sewa tidak dapat digunakan, PIHAK KEDUA berhak mengakhiri sewa dan menerima kembali sisa uang sewa secara proporsional beserta uang jaminan.

## Pasal 8
### Keadaan Memaksa
(1) Keadaan memaksa adalah keadaan di luar kendali dan kesalahan Para Pihak yang tidak dapat diperkirakan sebelumnya, antara lain bencana alam, kebakaran yang bukan karena kelalaian Para Pihak, banjir, wabah yang ditetapkan pemerintah, huru-hara, atau kebijakan pemerintah yang secara langsung melarang penggunaan Objek Sewa.
(2) Pihak yang mengalami keadaan memaksa wajib memberitahukan secara tertulis paling lambat 7 (tujuh) hari kalender sejak kejadian.
(3) Apabila Objek Sewa tidak dapat digunakan karena keadaan memaksa lebih dari 30 (tiga puluh) hari, Para Pihak bermusyawarah mengenai perpanjangan masa sewa sebagai pengganti atau pengembalian sisa uang sewa secara proporsional.

## Pasal 9
### Penyelesaian Perselisihan
(1) Perselisihan diselesaikan secara musyawarah untuk mufakat dalam waktu paling lama 30 (tiga puluh) hari kalender sejak pemberitahuan tertulis.
(2) Apabila musyawarah tidak mencapai mufakat, Para Pihak sepakat memilih penyelesaian melalui Pengadilan Negeri Yogyakarta.

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
| **Sri Wahyuni (fiktif)** | **Joko Santoso (fiktif)** |

Menyetujui (bila Objek Sewa harta bersama): ______________________ (suami/istri Pemilik)

Saksi-saksi (opsional): 1. ______________________  2. ______________________

---
### Lampiran 1: Berita Acara Kondisi dan Fasilitas Objek Sewa
| No | Bagian/Fasilitas | Kondisi saat serah terima | Keterangan/foto |
|---|---|---|---|
| 1 | [isi: mis. Pintu rolling door] | [isi: baik/rusak ringan] | [isi: ...] |
| 2 | [isi: Listrik: daya ... VA, meter no. ...] | [isi: ...] | [isi: angka meter awal] |
| 3 | [isi: Air: PDAM/sumur, meter no. ...] | [isi: ...] | [isi: angka meter awal] |
Kunci diserahkan: [isi: jumlah] buah. Ditandatangani Para Pihak pada saat serah terima.

---

### Yang masih perlu dilengkapi
- `[isi: NOMOR PERJANJIAN]`, `[isi: NIK]`/`[isi: ALAMAT]` kedua pihak, `[isi: KELURAHAN/KECAMATAN]`, `[isi: NOMOR SHM]`, `[isi: BANK]`/`[isi: NOMOR REKENING]`/`[isi: NAMA PEMILIK REKENING]`.
- Lampiran 1 (kondisi kios, angka meter listrik/air, jumlah kunci) diisi bersama saat serah terima.

### Pasal yang sebaiknya ditinjau pengacara
- **Pasal 7 ayat (3):** pengakhiran & pengosongan bila penyewa wanprestasi. Pengosongan paksa tanpa proses hukum bisa menimbulkan masalah baru. Pilihan "sisa sewa dikembalikan proporsional" sudah dipakai karena lebih seimbang.

### Syarat sah perjanjian (Pasal 1320 KUHPerdata)
- **Sepakat:** ✔ kalimat penutup "tanpa paksaan"; harga dan jadwal jelas.
- **Cakap:** ⚠ cek KTP kedua pihak; bila kios harta bersama, perlu persetujuan pasangan.
- **Hal tertentu:** ✔ objek (kios 12 m², alamat, SHM), jangka, harga jelas. Nomor SHM belum diisi.
- **Sebab halal:** ✔ sewa untuk usaha pulsa & aksesoris.

### Checklist sebelum tanda tangan
- [ ] Cocokkan KTP Pak Joko dengan data di perjanjian.
- [ ] Siapkan fotokopi SHM (nama pemilik = Ibu Sri). Bila kios harta bersama, pasangan ikut tanda tangan di baris "Menyetujui".
- [ ] Cek aturan pengelola pasar: apakah kios boleh disewakan ke pihak lain dan apakah perlu izin/lapor ke pengelola.
- [ ] Angka dan terbilang sama persis (sudah dihitung ulang: 4/4 cocok).
- [ ] Rekening tujuan atas nama Ibu Sri.
- [ ] Isi Lampiran 1 bersama saat serah terima kunci, termasuk angka meter listrik awal, lalu foto kondisi kios.
- [ ] Buat kuitansi untuk pembayaran Rp 9.000.000 dan deposit Rp 1.500.000. Kuitansi > Rp5.000.000 wajib bermeterai Rp10.000.
- [ ] Catat tanggal penting: pembayaran kedua 5 April 2027; permohonan perpanjangan paling lambat 60 hari sebelum 4 Oktober 2027.
- [ ] 2 rangkap asli masing-masing bermeterai Rp10.000; setiap halaman diparaf.
- [ ] Pasal ⚠ (Pasal 7 ayat 3) sudah dipahami.

### Catatan meterai
Surat perjanjian wajib bermeterai Rp10.000 berapa pun nilainya (UU 10/2020); 2 rangkap asli = 2 meterai (Rp 20.000). Kuitansi pembayaran Rp 9.000.000 juga wajib bermeterai karena > Rp5.000.000. Meterai bukan syarat sah, tetapi diperlukan bila dokumen dipakai sebagai alat bukti.

_Disclaimer: Draf ini disusun otomatis berdasarkan informasi dari Anda, mengacu pada ketentuan yang berlaku per 23 September 2026. Ini bukan nasihat hukum dan tidak menggantikan pengacara/notaris. Untuk nilai besar atau kasus kompleks, mintalah peninjauan profesional._

Mau saya buatkan versi .docx/PDF, atau kuitansi pembayaran pertamanya?

## Catatan penguji
- Angka diverifikasi independen: 50% × 18.000.000 = 9.000.000 (2×) ✔; denda 0,1% × 9.000.000 × 30 = 270.000, batas 5% = 450.000 ✔; terbilang cocok (lihat 01). Senin 5 Oktober 2026 dicek dengan `date` ✔.
- Bagus: peringatan harta bersama dan PPh sewa muncul (diminta PANDUAN AGENT); template seimbang (Pasal 7 ayat 4 memberi hak penyewa bila pemilik wanprestasi; Pasal 6 melindungi penyewa bila kios dijual, sesuai KUHPerdata Ps. 1576); denda dibatasi 5%; deposit ada batas waktu pengembalian.
- Tambahan agent (bukan dari skill): mengingatkan aturan pengelola pasar. Kios di pasar sering bukan SHM perorangan, tetapi hak pakai dari pengelola/pemda. SKILL.md tidak menyinggung ini, dan kasus "sewa ulang hak pakai kios pasar" cukup umum. Saran ringan: tambahkan ke PANDUAN AGENT `sewa-tempat.md`.
- Kurang (ringan): tanggal berakhir (4 Oktober 2027) dan jatuh tempo termin (5 April 2027) dihitung manual. Script belum punya subperintah tanggal.
