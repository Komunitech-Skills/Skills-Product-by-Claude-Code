# 05 - Input tidak lengkap, error, dan di luar cakupan

**Input tidak lengkap:** "Masukkan usulan dari WA." tanpa catatan → agent bertanya SEKALI: "Tempel catatannya (satu usulan per butir). Papan Fider Anda publik atau privat? Ada tag yang mau dipakai?" tanpa menulis apa pun.

**Galat nyata (Fider v0.38.0 asli):**
```
$ cek --kunci-file salah.txt        -> GALAT: Kunci API ditolak Fider (salah/sudah diganti). ... (kode 3)
$ cek (server mati)                 -> GALAT: Fider tidak terjangkau di http://localhost:3999 ([Errno 111] Connection refused). ... (kode 4)
$ cek (FIDER_URL=http://contoh.com) -> GALAT: Alamat Fider di internet wajib HTTPS (kunci API tidak boleh lewat HTTP polos). (kode 2)
$ lihat 9999                        -> GALAT: Tidak ditemukan (/api/v1/posts/9999). Nomor pos/tag salah? (kode 2)
$ impor berkas-kosong.txt           -> GALAT: Berkas ... kosong. (kode 6)
```
Kunci tidak pernah tampil di keluaran (diuji otomatis).

**Di luar cakupan:** "Hapus semua usulan spam dan ganti nama papan." → agent menolak dengan sopan: skill tidak punya perintah hapus/ubah pengaturan; lakukan manual di layar Fider (Settings). "Analisis tema keluhan dari 500 chat WA" → arahkan ke `iterasi-dari-masukan-pelanggan`. "Kirim kabar ke semua pelanggan yang vote" → tolak (tidak ada broadcast); tawarkan draf balasan untuk dikirim pemilik sendiri.
