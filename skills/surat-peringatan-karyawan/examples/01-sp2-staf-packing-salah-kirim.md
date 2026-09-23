# Contoh 01 – SP2 untuk staf packing yang salah kirim saat SP1 masih berlaku

## Skenario
S1, permintaan normal dan cukup lengkap. Online shop skincare di Tangerang. Staf packing salah kirim 5 paket dalam 2 minggu. Ia masih terkena SP1 yang terbit 14 Juli 2026, dan sudah dipanggil untuk klarifikasi. Skill harus memakai script untuk mengecek apakah SP1 masih berlaku, lalu menaikkan ke SP2. Semua nama fiktif.

## Input pengguna
```
Tolong buatkan SP lanjutan untuk Bayu Pratama, staf packing di online shop skincare saya (Glowria Skin, Tangerang). Dia masih kena SP1 nomor 004/SP-1/GS/VII/2026 tanggal 14 Juli 2026 karena salah kirim juga. Sekarang salah kirim lagi 5 paket: tanggal 8, 10, 11, 15, dan 17 September, semuanya ada komplain pembeli dan video packing. Kemarin (21 Sept) sudah saya panggil, katanya kurang fokus karena sering begadang. Di peraturan perusahaan kami Pasal 12 soal kewajiban mengikuti SOP packing. Saya pemiliknya, Rudi Hartono.
```

## Proses (dijalankan agent)
```
$ python3 scripts/masa_berlaku.py --terbit "14-07-2026" --cek "08-09-2026" --format teks
Cek tanggal : Pada 8 September 2026 SP ini MASIH AKTIF (sisa 127 hari) ...
$ python3 scripts/masa_berlaku.py --terbit "14-07-2026" --cek "17-09-2026" --format teks
Berlaku s.d. : Rabu, 13 Januari 2027
Cek tanggal  : Pada 17 September 2026 SP ini MASIH AKTIF (sisa 118 hari) ...
$ python3 scripts/masa_berlaku.py --terbit "23-09-2026" --format teks
Kalimat untuk SP : Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026 sampai dengan 22 Maret 2027.
```

## Output

**Tingkat SP yang disarankan: SP2 (Surat Peringatan Kedua).**
Alasannya, SP1 tanggal 14 Juli 2026 berlaku sampai 13 Januari 2027 (dicek dengan script). Kelima pelanggaran (8–17 September 2026) terjadi saat SP1 masih aktif, dan jenis pelanggarannya sama. Menurut matriks proporsionalitas, pelanggaran berulang saat SP aktif dinaikkan satu tingkat.

```
GLOWRIA SKIN
[Alamat lengkap], Tangerang | Telp/WA [nomor] | [email]
________________________________________________________________

SURAT PERINGATAN KEDUA (SP-2)
Nomor: [nomor urut]/SP-2/GS/IX/2026

Yang bertanda tangan di bawah ini:
Nama     : Rudi Hartono
Jabatan  : Pemilik Glowria Skin
dengan ini memberikan Surat Peringatan Kedua kepada:
Nama     : Bayu Pratama
Jabatan  : Staf Packing
Bagian   : Gudang & Pengiriman
NIK Karyawan (jika ada): [nomor induk karyawan]

A. Pelanggaran
Berdasarkan laporan komplain pembeli dan rekaman video packing, Saudara tercatat salah
mengirim barang sebanyak 5 (lima) paket, yaitu pada tanggal 8, 10, 11, 15, dan 17 September
2026 (daftar nomor pesanan dan komplain terlampir).
Pelanggaran ini terjadi pada saat Surat Peringatan Pertama Nomor 004/SP-1/GS/VII/2026
tanggal 14 Juli 2026 masih berlaku (berlaku s.d. 13 Januari 2027), yang diberikan untuk
pelanggaran sejenis.

B. Dasar
Perbuatan tersebut melanggar Pasal 12 Peraturan Perusahaan Glowria Skin tentang kewajiban
mengikuti SOP packing yang berbunyi "[kutipan singkat Pasal 12]". Saudara telah didengar
penjelasannya pada 21 September 2026 sebagaimana tercatat dalam Berita Acara Klarifikasi
terlampir.

C. Harapan perbaikan
Kami meminta Saudara untuk:
1. Mencocokkan barang dengan resi sebelum dibungkus untuk setiap paket, sesuai SOP packing.
2. Merekam video packing untuk 100% paket yang dikirim.
3. Tidak melakukan kesalahan kirim (0 paket) selama masa berlaku surat ini.
Perusahaan bersedia memberikan pelatihan ulang SOP packing pada [tanggal] dan meninjau
pembagian jam kerja bila beban kerja menjadi penyebab.
Apabila selama masa berlaku surat ini Saudara kembali melakukan pelanggaran, perusahaan
dapat memberikan Surat Peringatan Ketiga (terakhir) sesuai ketentuan yang berlaku.

D. Masa berlaku
Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026
sampai dengan 22 Maret 2027.

Demikian surat peringatan ini dibuat untuk diperhatikan dan menjadi bahan perbaikan.

Tangerang, 23 September 2026

Pemberi peringatan,                       Diterima oleh,


Rudi Hartono                               Bayu Pratama
Pemilik                                    Tanggal terima: ______________

Saksi,


[Nama, Jabatan]

Lampiran: Berita Acara Klarifikasi; daftar 5 nomor pesanan & komplain pembeli; SP-1 Nomor 004/SP-1/GS/VII/2026
Tembusan: 1. Arsip personalia  2. [Atasan langsung/Admin gudang]
```

```
BERITA ACARA KLARIFIKASI
Nomor: [nomor]

Pada hari Senin, tanggal 21 September 2026, pukul [jam], bertempat di [lokasi], telah dilakukan klarifikasi:
Pihak perusahaan : Rudi Hartono, Pemilik
Karyawan         : Bayu Pratama, Staf Packing
Saksi            : [nama, jabatan]

Pokok permasalahan:
Kesalahan pengiriman 5 (lima) paket pada tanggal 8, 10, 11, 15, dan 17 September 2026 berdasarkan
komplain pembeli dan rekaman video packing, pada saat SP-1 Nomor 004/SP-1/GS/VII/2026 masih berlaku.

Penjelasan karyawan:
"Kurang fokus karena sering begadang." [lengkapi dengan kata-kata karyawan sendiri]

Tanggapan/kesepakatan:
[mis. karyawan mengakui kesalahan; bersedia mengikuti pelatihan ulang SOP packing; tindak lanjut]

Demikian berita acara ini dibuat dengan sebenarnya dan dibaca ulang di hadapan para pihak.

Pihak perusahaan,          Karyawan,               Saksi,


Rudi Hartono               Bayu Pratama            [Nama]
```

---
**CATATAN PROSES (untuk kamu, jangan dicetak)**
1. Berita acara di atas mencatat pertemuan 21 September. Lengkapi penjelasan Bayu dengan kata-katanya sendiri dan mintakan tanda tangan semua pihak. Jika pertemuan itu belum dicatat, catat sekarang sebelum SP diserahkan.
2. Serahkan SP2 secara pribadi (bukan di depan rekan), rangkap 2. Minta Bayu menandatangani dan menulis tanggal terima. Jika menolak, tulis "Karyawan menolak menandatangani pada [tanggal, jam]" dan minta saksi tanda tangan.
3. Alasan "sering begadang" perlu ditanggapi: cek apakah ada lembur/shift malam dari toko. Jika ada, perbaikan jadwal juga menjadi tanggung jawab usaha.
4. Jangan memotong gaji untuk mengganti ongkos retur kecuali diatur jelas di PK/PP.
5. Catat tanggal berakhir SP2 (22 Maret 2027) di kalender. Setelah SP3, langkah berikutnya menyangkut PHK dan wajib dikonsultasikan ke ahli hukum/Disnaker.
6. Isi nomor urut surat, kutipan Pasal 12, nama saksi, dan tanggal pelatihan ulang.

Disclaimer: Draf ini adalah bantuan administrasi, bukan nasihat hukum. Masa berlaku 6 bulan mengikuti
PP 35/2021 Pasal 52 (per 23 September 2026), kecuali Perjanjian Kerja/Peraturan Perusahaan/PKB
perusahaan mengatur lain. Aturan ketenagakerjaan sedang dalam proses perubahan. Untuk PHK, pelanggaran
pidana, atau sengketa, konsultasikan dengan ahli hukum ketenagakerjaan atau Disnaker setempat.

## Catatan penguji
- **Script dijalankan sungguhan** untuk tanggal pelanggaran pertama (8/9) dan terakhir (17/9): keduanya "MASIH AKTIF". SP1 berakhir 13 Januari 2027, SP2 berlaku 23 September 2026 s.d. 22 Maret 2027. **Diverifikasi independen** dengan Python terpisah (rumus bulan kalender, brute force 2025–2028 × 1–12 bulan: 0 selisih). Nama hari "Rabu, 13 Januari 2027" dan "Senin, 21 September 2026" benar.
- **Bagus:** fakta terukur (tanggal, jumlah, bukti), tidak ada kata merendahkan, dasar pasal diisi dari pengguna, harapan perbaikan terukur ("0 paket"), tidak ada ancaman PHK. Catatan proses menangkap akar masalah (begadang) secara manusiawi.
- **Kurang (ringan):** Format output SKILL.md menaruh kalimat "telah didengar penjelasannya" di bagian B (Dasar). Di bagian itu kalimat tersebut terasa kurang pas, karena bukan dasar hukum. Tidak salah, hanya struktur.
- **Kurang (ringan):** SKILL.md hanya menyebut `--cek "<tanggal pelanggaran baru>"`, satu tanggal. Untuk pelanggaran berulang, sebaiknya disebut: "cek tanggal pelanggaran **pertama**" (yang paling menentukan). Di sini agent mengecek dua tanggal atas inisiatif sendiri.
