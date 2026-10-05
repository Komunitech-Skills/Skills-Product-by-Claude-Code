# 04. Input tidak lengkap

## Kasus A: tanpa data
**Pesan pengguna:** "Tolong rapikan data pelanggan saya."

**Balasan yang diharapkan (satu kali tanya, maks. 3 pertanyaan):**
Siap. Supaya tepat sasaran, mohon kirim:
1. Datanya: file CSV (Excel: *File > Save As > CSV UTF-8*) atau tempel langsung kalau kurang dari 40 baris.
2. Isi kolomnya apa saja (nama, nomor HP, tanggal beli, total belanja, kota)?
3. Mau dipakai untuk apa (kirim pesan ke pelanggan yang setuju, laporan, pindah ke aplikasi kasir)? Itu menentukan apakah satu baris = satu orang atau satu transaksi.

Nomor HP akan saya seragamkan jadi 628xxxxxxxxxx, tanggal jadi 2026-10-05, harga jadi angka. Nama yang mirip hanya saya tandai, tidak digabung tanpa persetujuan Anda.

## Kasus B: file hanya satu kolom nama
**Berkas (8 baris):** `siti aminah`, `SITI AMINAH`, `Siti Aminah`, `Siti Aminh`, `rudi hartono`, `Rudi Hartono ` (spasi di ujung), `bu Ratna`, `Ratna`.
**Cara dijalankan:** `python3 scripts/rapikan.py nama.csv`

**Balasan yang diharapkan (kerjakan dulu, tanya di akhir):**
Selesai dirapikan: 8 baris. 4 nama diperbaiki (huruf besar-kecil/spasi). Tidak ada kolom nomor HP, tanggal, atau harga di file ini, jadi bagian itu tidak disentuh.

Perlu keputusan Anda
1. "Siti Aminah" (3 kali) dan "Siti Aminh" (baris 5) mungkin orang yang sama, salah ketik satu huruf. Disatukan jadi "Siti Aminah"? "Bu Ratna" dan "Ratna" (baris 8-9) juga mirip: satu orang?
2. Ada dua nama yang muncul berulang persis: "Siti Aminah" (baris 2, 3, 4) dan "Rudi Hartono" (baris 6, 7). Kalau ini daftar pelanggan, sisakan satu baris per nama?

Karena hanya ada nama, saya tidak bisa memastikan mana orang yang sama (nomor HP akan membantu).

## Verifikasi
- 8 baris data; nama diubah: "siti aminah", "SITI AMINAH", "rudi hartono", "bu Ratna" = 4; "Rudi Hartono " (spasi ujung) dihitung sebagai spasi, bukan nama = 1 (ditampilkan di laporan sebagai `spasi_dirapikan` = 1).
- Kelompok mirip: {Siti Aminah x3, Siti Aminh}, {Bu Ratna, Ratna} = 2; duplikat persis: Siti Aminah (baris 2-4), Rudi Hartono (baris 6-7) = 2 grup. Sesuai keluaran alat.
- Perilaku diperiksa: tidak muncul peringatan "pemisah mungkin salah" untuk berkas satu kolom (diperbaiki di versi 1.0.0).
