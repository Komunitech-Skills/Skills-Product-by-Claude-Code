# Template Surat Resmi per Jenis + Contoh Kasus Lokal

Semua template memakai kop & blok tanggal yang sama:
```
[NAMA USAHA/ORGANISASI]
[Alamat] | Telp/WA [..] | Email [..]
________________________________________________________________
Nomor    : [nomor dari script]                        [Kota], [tanggal dari script]
Lampiran : [jumlah] — hapus baris jika tidak ada
Perihal  : [perihal]
```

---
## 1. Surat Permohonan
**Contoh kasus:** Panitia bazar UMKM warga Sukajadi, Bandung, memohon izin memakai lahan parkir untuk bazar Sabtu malam.
```
Perihal  : Permohonan Izin Penggunaan Lahan Parkir untuk Bazar UMKM

Yth. Ketua RW 07 Kelurahan Sukajadi
di Bandung

Dengan hormat,
Kami, [nama usaha/panitia], bermaksud menyelenggarakan Bazar UMKM Sukajadi yang akan
dilaksanakan pada
hari, tanggal : Sabtu, 17 Oktober 2026
pukul         : 16.00–22.00 WIB
tempat        : lahan parkir Jalan [..]
peserta       : ±25 pelapak UMKM warga sekitar

Sehubungan dengan hal tersebut, kami memohon izin penggunaan lahan parkir tersebut.
Kami bertanggung jawab atas kebersihan, keamanan, dan ketertiban selama acara berlangsung.
Susunan acara dan denah lokasi kami lampirkan.

Atas perhatian dan izin Bapak, kami mengucapkan terima kasih.

Hormat kami,
Ketua Panitia,


[Nama]
```
Variasi: permohonan cuti karyawan, permohonan sponsor (non-komersial; untuk kerja sama berbayar pakai `proposal-kerjasama`), permohonan peminjaman aula, permohonan data/dokumen.

---
## 2. Surat Pemberitahuan
**Contoh kasus:** Toko "Grosir Berkah" di Pekalongan memberi tahu pelanggan tetap bahwa toko libur Maulid Nabi dan jam operasional baru.
```
Perihal  : Pemberitahuan Perubahan Jam Operasional

Yth. Bapak/Ibu Pelanggan Grosir Berkah
di tempat

Dengan hormat,
Kami memberitahukan bahwa mulai Senin, 5 Oktober 2026, jam operasional Grosir Berkah berubah
menjadi:
Senin–Sabtu : pukul 07.00–17.00 WIB
Minggu      : tutup

Pesanan melalui WhatsApp [nomor] tetap kami terima setiap hari dan diproses pada hari kerja
berikutnya.

Atas perhatian dan kepercayaan Bapak/Ibu, kami mengucapkan terima kasih.

Hormat kami,
Pemilik,


[Nama]
```

---
## 3. Surat Undangan
Pakai `--acara` di script untuk nama hari. Rincian acara ditulis berkolom (hari, tanggal / pukul / tempat / acara). Tambahkan "Konfirmasi kehadiran kepada [nama] ([WA]) paling lambat [tanggal]" bila perlu.
Variasi: undangan rapat internal, RAT koperasi, syukuran pembukaan cabang, rapat wali murid, rapat RT.

---
## 4. Surat Kuasa (sederhana)
**Contoh kasus:** Pemilik CV di Semarang memberi kuasa kepada staf admin untuk mengambil dokumen di kantor samsat/leasing, atau mewakili rapat asosiasi.
```
SURAT KUASA
Nomor: [nomor] (opsional untuk kuasa pribadi)

Yang bertanda tangan di bawah ini:
Nama              : [nama pemberi kuasa]
Nomor identitas   : [NIK/nomor KTP]
Jabatan           : [jabatan, bila atas nama usaha]
Alamat            : [alamat]
selanjutnya disebut Pemberi Kuasa.

Dengan ini memberikan kuasa kepada:
Nama              : [nama penerima kuasa]
Nomor identitas   : [NIK/nomor KTP]
Jabatan           : [jabatan]
Alamat            : [alamat]
selanjutnya disebut Penerima Kuasa.

KHUSUS
Untuk dan atas nama Pemberi Kuasa [uraian tindakan yang jelas dan terbatas, mis. "mengambil
dokumen BPKB kendaraan Nomor Polisi H 1234 AB di kantor [nama leasing] cabang Semarang"],
termasuk menandatangani tanda terima yang diperlukan untuk keperluan tersebut.

Surat kuasa ini berlaku sejak ditandatangani sampai dengan [tanggal/urusan selesai] dan tidak
dapat dialihkan kepada pihak lain.

[Kota], [tanggal]

Penerima Kuasa,                      Pemberi Kuasa,
                                     [meterai Rp10.000]

[Nama]                               [Nama]
```
Catatan untuk pengguna: lampirkan fotokopi KTP kedua pihak; banyak instansi/leasing meminta meterai dan format mereka sendiri, jadi tanyakan dulu. Kuasa untuk pengadilan, jual beli tanah/rumah, atau urusan bank tertentu biasanya butuh format khusus/notaris.

---
## 5. Surat Keterangan (Kerja/Magang/Usaha)
**Contoh kasus:** Klinik kecantikan di Makassar membuat surat keterangan kerja untuk mantan terapis yang melamar kerja baru.
```
SURAT KETERANGAN KERJA
Nomor: [nomor]

Yang bertanda tangan di bawah ini:
Nama     : [nama]
Jabatan  : [jabatan]
menerangkan dengan sebenarnya bahwa:
Nama     : [nama karyawan]
Jabatan  : [jabatan terakhir]
telah bekerja di [nama usaha] sejak [tanggal mulai] sampai dengan [tanggal akhir / "saat ini"].
[Opsional, hanya bila pengguna menyatakan: Selama bekerja, yang bersangkutan menunjukkan kinerja
yang baik dan tidak pernah melakukan pelanggaran berat.]

Surat keterangan ini dibuat untuk dipergunakan sebagaimana mestinya.

[Kota], [tanggal]
[Jabatan],


[Nama]
```
Aturan: hanya fakta dari pengguna. Tidak menulis gaji kecuali diminta; tidak menulis alasan berhenti yang merugikan tanpa diminta.

---
## 6. Surat Pengantar
**Contoh kasus:** Konveksi di Bandung mengirim sampel seragam ke sekolah; atau HR mengantar karyawan baru ke BPJS/klinik untuk medical check-up.
```
Perihal  : Pengantar Pengiriman Sampel Seragam

Yth. Kepala SMP [..]
di Cimahi

Dengan hormat,
Bersama ini kami kirimkan barang/dokumen sebagai berikut:
| No | Uraian | Jumlah | Keterangan |
|---|---|---|---|
| 1 | Sampel kemeja seragam ukuran M | 1 potong | untuk dicoba |
| 2 | Katalog bahan | 1 buku | — |

Mohon diterima dengan baik. Jika ada pertanyaan, silakan menghubungi [nama] di [WA].

Hormat kami,
[Jabatan],


[Nama]

Diterima oleh: ______________  Tanggal: ________
```
Catatan: surat pengantar pengiriman barang tidak dikenai bea meterai (UU 10/2020 Pasal 7 — dokumen terkait lalu lintas orang & barang).
