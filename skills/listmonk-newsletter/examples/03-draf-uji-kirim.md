# 03 - Draf kampanye + uji kirim (hasil nyata)

**Pengguna:** "Buatkan email promo keripik varian baru diskon 15% sampai Minggu, ajakan pesan lewat WA."

Agent menawarkan 3 subjek (mis. "Diskon 15% keripik varian baru untuk Anda"), menulis isi dari `templates/email-promo.html`, lalu:
```
$ listmonk.py buat-kampanye --nama "Promo Keripik Baru" --subjek "Diskon 15% keripik varian baru untuk Anda" --list 4 --isi-file promo.html --dari "Keripik Bu Sri <halo@...>"
Draf kampanye dibuat: #3 'Promo Keripik Baru' - status draft (BELUM dikirim ke siapa pun).
Langkah berikutnya: uji-kirim 3 --ke <email Anda>
$ listmonk.py uji-kirim 3 --ke pemilik@example.test
Email uji dikirim ke p***@example.test. Minta pengguna memeriksa kotak masuk DAN folder spam...
$ listmonk.py periksa-kampanye 3
Tidak ada masalah terdeteksi.
Sudah diuji-kirim (isi sama persis): YA
```
Uji lain: subjek "PROMO GILA GILAAN HARI INI SAJA!!!" memunculkan saran "banyak HURUF BESAR" dan "banyak tanda seru". Tautan berhenti berlangganan dihapus dari isi + template -> GALAT, kirim ditolak.
