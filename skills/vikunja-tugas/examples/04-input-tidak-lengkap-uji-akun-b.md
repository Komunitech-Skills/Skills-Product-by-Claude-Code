# Skenario 4 (uji Akun B) — Input tidak lengkap / tidak jelas

## 4a. Tanpa proyek sama sekali
```
$ python3 vikunja.py tambah --judul "Beli galon air" --tenggat "hariiniii"
GALAT: Tugas 'Beli galon air': proyek tidak disebutkan (--proyek, atau isi field 'proyek' di --batch).
```
exit code 2. Benar: proyek dicek lebih dulu sebelum sempat mengeluh soal tenggat "hariiniii" yang juga
salah ketik — pengguna cukup diberi satu masalah dulu untuk diperbaiki, tidak membanjiri dengan dua
galat sekaligus.

## 4b. Proyek ada, tenggat tidak dikenali
```
$ python3 vikunja.py tambah --proyek "Kafe Senja" --judul "Cuci gorden" --tenggat "kapan-kapan"
GALAT: Tenggat tidak dikenali: 'kapan-kapan'. Format yang didukung: 'hari ini', 'besok', 'lusa',
'N hari lagi', nama hari ('Jumat', 'Jumat depan'), 'minggu depan', '25/10', '25/10/2026',
'25 Oktober 2026', '2026-10-25' — boleh diakhiri 'jam 14:00'.
```
exit code 2. Pesan menyebutkan seluruh format yang didukung — cukup untuk agent menyusun ulang
pertanyaan ke pengguna tanpa menebak-nebak.

## 4c. Nama proyek sebagian (bukan persis) tapi tidak ambigu
```
$ python3 vikunja.py tambah --proyek "Toko" --judul "Test" --tenggat besok
PRATINJAU TAMBAH TUGAS
1.
   Judul : Test
   Proyek: Toko Bangunan Sinar Jaya (id 4)
   Tenggat: Minggu, 27 September 2026
Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan ke Vikunja.
```
Benar: "Toko" cocok tepat satu proyek nyata ("Toko Bangunan Sinar Jaya") dari 4 proyek yang ada
(termasuk "Inbox" bawaan), jadi diterima tanpa perlu tanya ulang — sesuai prinsip "instan, tapi
reliable" di CLAUDE.md.

## 4d. Nama proyek ambigu (cocok ke DUA proyek) — diuji ulang setelah menambah proyek kedua "Toko Elektronik Jaya"
```
$ python3 vikunja.py tambah --proyek "Toko" --judul "Test ambigu" --tenggat besok
GALAT: Nama proyek 'Toko' cocok lebih dari satu: Toko Bangunan Sinar Jaya (id 4); Toko Elektronik Jaya (id 7). Sebutkan id-nya.
```
exit code 2. Benar dan sesuai dokumentasi: kedua opsi disebutkan lengkap dengan id-nya, tidak menebak.
