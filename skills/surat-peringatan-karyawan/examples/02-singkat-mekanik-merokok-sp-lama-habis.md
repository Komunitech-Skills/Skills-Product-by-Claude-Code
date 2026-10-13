# Contoh 02 – Permintaan singkat: pengguna minta SP2, padahal SP1 lama sudah berakhir

## Skenario
S2, permintaan singkat/malas. Pemilik bengkel di Medan minta "SP2" untuk mekanik yang merokok dekat tangki bensin. SP1 sebelumnya terbit 2 Januari 2026. Skill harus mengecek dengan script dan menemukan bahwa SP1 sudah berakhir, lalu menyarankan SP1 kembali (kecuali PP bengkel mengatur lain). Semua nama fiktif.

## Input pengguna
```
bikinin dong SP2 buat dedi, mekanik bengkel aku di medan. tgl 18 sept kemarin ketahuan ngerokok deket tangki bensin, ada rekaman cctv. dulu udah pernah SP1 tgl 2 januari 2026 soal ngerokok juga
```

## Proses (dijalankan agent)
```
$ python3 scripts/masa_berlaku.py --terbit "2 Januari 2026" --cek "18 September 2026" --format teks
Berlaku s.d.     : Rabu, 1 Juli 2026
Cek tanggal      : Pada 18 September 2026 SP ini SUDAH BERAKHIR. Pelanggaran baru umumnya dimulai lagi dari SP1 (kecuali PK/PP/PKB mengatur lain).
$ python3 scripts/masa_berlaku.py --terbit "23-09-2026" --format teks
Kalimat untuk SP : Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026 sampai dengan 22 Maret 2027.
```

## Output

⚠️ **Sebelum membuat SP2, ada yang perlu kamu tahu:** SP1 tanggal 2 Januari 2026 **sudah berakhir pada 1 Juli 2026** (masa berlaku 6 bulan, dicek dengan script). Pelanggaran tanggal 18 September terjadi setelah SP1 habis. Jadi menurut PP 35/2021, SP yang tepat umumnya **SP1 lagi**, bukan SP2.

SP2 langsung hanya aman jika **Peraturan Perusahaan/Perjanjian Kerja bengkel** mengatur bahwa merokok di area bahan bakar adalah pelanggaran berat yang bisa langsung SP2/SP3. Kalau aturan itu ada, kirim bunyi pasalnya dan aku ubah suratnya.

Merokok dekat tangki bensin memang berbahaya (risiko kebakaran). Karena itu SP1 di bawah menulis alasan keselamatan dengan tegas dan menyebut riwayat SP sebelumnya sebagai catatan.

```
[NAMA BENGKEL]
[Alamat lengkap], Medan | Telp/WA [nomor]
________________________________________________________________

SURAT PERINGATAN PERTAMA (SP-1)
Nomor: [nomor urut]/SP-1/[SINGKATAN]/IX/2026

Yang bertanda tangan di bawah ini:
Nama     : [nama pemilik]
Jabatan  : Pemilik [Nama Bengkel]
dengan ini memberikan Surat Peringatan Pertama kepada:
Nama     : Dedi [nama lengkap]
Jabatan  : Mekanik
Bagian   : Servis

A. Pelanggaran
Berdasarkan rekaman CCTV bengkel, Saudara tercatat merokok di dekat tangki bahan bakar
di area servis pada tanggal 18 September 2026. Perbuatan ini membahayakan keselamatan
Saudara, rekan kerja, pelanggan, dan bengkel karena berisiko menimbulkan kebakaran.
Sebagai catatan, Saudara pernah menerima Surat Peringatan Pertama tanggal 2 Januari 2026
untuk pelanggaran sejenis (masa berlakunya telah berakhir pada 1 Juli 2026).

B. Dasar
Perbuatan tersebut melanggar [Pasal .. Peraturan Perusahaan / Tata Tertib Bengkel tentang
larangan merokok di area kerja/bahan bakar]. Saudara telah didengar penjelasannya pada
[tanggal] sebagaimana tercatat dalam Berita Acara Klarifikasi terlampir.

C. Harapan perbaikan
Kami meminta Saudara untuk:
1. Tidak merokok di seluruh area servis dan area penyimpanan bahan bakar.
2. Merokok hanya di tempat yang ditentukan: [lokasi area merokok].
Apabila selama masa berlaku surat ini Saudara kembali melakukan pelanggaran, perusahaan
dapat memberikan Surat Peringatan Kedua sesuai ketentuan yang berlaku.

D. Masa berlaku
Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026
sampai dengan 22 Maret 2027.

Demikian surat peringatan ini dibuat untuk diperhatikan dan menjadi bahan perbaikan.

Medan, 23 September 2026

Pemberi peringatan,                       Diterima oleh,


[Nama pemilik]                             Dedi [nama lengkap]
Pemilik                                    Tanggal terima: ______________

Saksi,


[Nama, Jabatan]

Lampiran: Berita Acara Klarifikasi; tangkapan layar rekaman CCTV 18 September 2026
Tembusan: 1. Arsip personalia  2. [Kepala mekanik]
```

```
BERITA ACARA KLARIFIKASI
Nomor: [nomor]

Pada hari [hari], tanggal [tanggal], pukul [jam], bertempat di [lokasi], telah dilakukan klarifikasi:
Pihak perusahaan : [nama, jabatan]
Karyawan         : Dedi [nama lengkap], Mekanik
Saksi            : [nama, jabatan]

Pokok permasalahan:
Merokok di dekat tangki bahan bakar di area servis pada 18 September 2026, berdasarkan rekaman CCTV.

Penjelasan karyawan:
[tulis apa adanya, dengan kata-kata karyawan]

Tanggapan/kesepakatan:
[mis. karyawan mengakui / tidak mengakui; komitmen perbaikan; tindak lanjut]

Demikian berita acara ini dibuat dengan sebenarnya dan dibaca ulang di hadapan para pihak.

Pihak perusahaan,          Karyawan,               Saksi,


[Nama]                     Dedi                    [Nama]
```

---
**CATATAN PROSES (untuk kamu, jangan dicetak)**
1. Panggil Dedi dulu secara pribadi dengan 1 saksi. Tunjukkan rekaman CCTV, dengarkan penjelasannya, dan catat di berita acara. Setelah itu baru serahkan SP.
2. Pastikan ada **area merokok yang jelas** dan tanda "Dilarang Merokok" di area bahan bakar. Tanpa itu, dasar SP lemah.
3. Jika bengkel belum punya Peraturan Perusahaan (umumnya wajib bila karyawan ≥ 10 orang — UU 13/2003 Pasal 108), buat tata tertib tertulis yang ditandatangani semua karyawan. Cantumkan larangan merokok di area bahan bakar sebagai pelanggaran berat supaya ke depan jelas tingkat sanksinya.
4. Minta tanda tangan penerimaan. Jika Dedi menolak, tulis "menolak menandatangani" dan minta saksi tanda tangan.
5. Isi nama lengkap, nama bengkel, pasal tata tertib, dan nama saksi.

Disclaimer: Draf ini adalah bantuan administrasi, bukan nasihat hukum. Masa berlaku 6 bulan mengikuti
PP 35/2021 Pasal 52 (per 23 September 2026), kecuali Perjanjian Kerja/Peraturan Perusahaan/PKB
perusahaan mengatur lain. Aturan ketenagakerjaan sedang dalam proses perubahan. Untuk PHK, pelanggaran
pidana, atau sengketa, konsultasikan dengan ahli hukum ketenagakerjaan atau Disnaker setempat.

## Catatan penguji
- **Bagus (penting):** skill tidak menuruti begitu saja permintaan "SP2". Script membuktikan SP1 sudah berakhir 1 Juli 2026, dan skill menjelaskan konsekuensinya serta jalan keluarnya (PP bengkel yang mengatur pelanggaran berat). Ini persis kasus 4 di `references/template-sp.md`. Tanggal diverifikasi independen: 2 Januari + 6 bulan − 1 hari = 1 Juli 2026 (Rabu).
- **Bagus:** permintaan malas tetap menghasilkan SP lengkap dengan placeholder yang jelas. Info yang kurang (nama lengkap, nama bengkel, pemberi) tidak ditanyakan, sesuai aturan "jika pengguna ingin cepat, buat dengan placeholder".
- **Kurang (ringan):** menyebut "SP1 lama" di bagian A bisa diperdebatkan (SP yang sudah berakhir sebaiknya tidak memberatkan). SKILL.md tidak mengatur hal ini. Saran: tambahkan ke *Batasan*: "SP yang sudah berakhir boleh disebut sebagai riwayat, tapi jangan dijadikan dasar menaikkan tingkat."
