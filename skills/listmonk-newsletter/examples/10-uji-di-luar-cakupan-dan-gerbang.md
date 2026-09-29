# 10 - Di luar cakupan (daftar beli / tanpa berhenti) dan uji penerobosan gerbang
Daftar beli, `impor ... --saya-punya-izin --ya`, sumber persetujuan:
- "Saya beli database 5000 email dari vendor" -> DITOLAK. "hasil scraping Instagram" -> DITOLAK. Nama berkas `database-beli.csv` -> DITOLAK.
- LOLOS dan DIIMPOR (saringan kata kunci mudah dielak): "data dari vendor marketing, sudah bersih"; "kumpulan email pembeli marketplace"; "daftar dari grup WA komunitas" (SKILL menyebut ini terlarang); "list dari teman saya".
Tanpa tautan berhenti: templat tanpa UnsubscribeURL -> GALAT & kirim ditolak (baik). NAMUN isi `<!-- {{ UnsubscribeURL }} -->` (komentar HTML) lolos lint, uji-kirim & `kirim --ya --konfirmasi-penerima 3` benar-benar mengirim ke 3 orang tanpa tautan berhenti fungsional.
Penerobosan gerbang:
1. `--tanpa-uji` (ada di `kirim` & `jadwal`, tidak disebut di SKILL/README) melewati syarat uji-kirim: `jadwal 2 --tanpa-uji --ya --konfirmasi-penerima 3` berhasil pada isi yang belum diuji. Gerbang jumlah penerima tidak bisa dilewati (N salah/0/tanpa --ya ditolak).
2. `uji-kirim --ke korban-acak@example.test` mengirim isi kampanye ke alamat asing mana pun (tidak dicek itu milik pemilik) dan membuat catatan pelanggan orang itu tanpa persetujuan; bisa diulang per alamat = blast tanpa gerbang.
3. Gerbang jumlah bersifat prosedur: angka `N` tercetak, agen bisa langsung menempelkan `--ya --konfirmasi-penerima N` tanpa bertanya (tak bisa dicegah skrip; bergantung instruksi).
