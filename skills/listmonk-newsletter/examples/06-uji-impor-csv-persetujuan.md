# 06 - Normal 1: impor CSV dengan persetujuan (penguji independen, listmonk 6.2.0 ASLI)
Lingkungan: image resmi listmonk v6.2.0 + postgres:17, port 127.0.0.1, pengguna API berperan sesuai panduan §7 (dibuat lewat API admin), SMTP penampung lokal. Data fiktif example.test.
Input: kontak.csv 10 baris (duplikat beda huruf besar, email rusak, `setuju=tidak`, `setuju` kosong, `gmial.com`, nama berawalan `=`).
- `periksa-kontak`: valid 7, tidak valid 1, duplikat 1, menolak 1; typo `c***@gmial.com` ditandai; kolom `kota` jadi atribut. Angka cocok hitungan manual.
- `impor` tanpa `--saya-punya-izin` -> DITOLAK (kode 6). Tanpa `--ya` -> ringkasan, belum jalan (6). Dengan `--ya` -> "Impor finished: 7 dari 7", status `unconfirmed`.
- `kirim-optin` tanpa angka -> ditahan; dengan `--ya --konfirmasi-penerima 7` -> 7 email "Confirm subscription" tiba di penampung (bahasa Inggris, sesuai catatan panduan §6). Klik 3 tautan -> `daftar-pelanggan`: 3 konfirmasi / 4 belum.
- Impor ulang file sama: tidak ada duplikat. Orang yang sudah berhenti/blocklist TIDAK hidup lagi walau `--sudah-terkonfirmasi` (listmonk menjaga), tetapi pesan skill tetap "7 dari 7" (menyesatkan, lihat HASIL-UJI).
Temuan: baris dengan kolom `setuju` KOSONG (Fajar) ikut diimpor sebagai setuju; nama `=cmd|'/c calc'!A1` hanya dilucuti `=` (sisa payload tetap tersimpan).
