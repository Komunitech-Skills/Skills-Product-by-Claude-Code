# Panduan "5 Kenapa" Tanpa Menyalahkan Orang

Dipakai saat menyusun bagian **Akar Masalah** di `laporan-insiden-usaha`. Tujuannya: berhenti di penyebab yang **bisa diperbaiki lewat proses/alat/SOP**, bukan di "karena si A lalai".

## Cara pakai
Tanyakan "kenapa" berulang (biasanya 3–5 kali) dari gejala yang terlihat sampai ketemu penyebab sistemik. Setiap jawaban jadi pertanyaan "kenapa" berikutnya.

### Contoh 1 — Pesanan salah kirim massal
(Pengguna hanya menyebut: 40 label salah alamat, admin menyalin dari sheet lama. Langkah 3–4 di bawah adalah dugaan, jadi ditandai.)
1. Kenapa banyak pesanan tertukar? → Karena label pengiriman tercetak salah alamat untuk 40 pesanan.
2. Kenapa label bisa salah alamat? → Karena admin menyalin data dari sheet lama yang belum diperbarui.
3. Kenapa sheet lama yang dipakai? → Mungkin tidak ada langkah "cek ulang sheet sebelum cetak label" di SOP packing. (dugaan, perlu dikonfirmasi)
4. Kenapa langkah itu tidak ada? → Mungkin SOP packing belum disesuaikan dengan volume promo. (dugaan, perlu dikonfirmasi)
**Dugaan akar masalah (belum dikonfirmasi pemilik):** tidak ada langkah verifikasi data sebelum cetak label massal.
Mohon konfirmasi: apakah SOP packing sudah punya langkah cek sumber data alamat sebelum cetak?

### Contoh 2 — Mesin kasir/QRIS error saat jam sibuk
(Pengguna hanya menyebut: QRIS error saat jam sibuk, internet putus-nyambung.)
1. Kenapa QRIS error? → Karena koneksi internet toko putus-nyambung.
2. Kenapa koneksi tidak stabil? → Mungkin hanya mengandalkan 1 sumber internet tanpa cadangan. (dugaan, perlu dikonfirmasi)
3. Kenapa tidak ada cadangan? → Mungkin belum pernah dianggap perlu. (dugaan, perlu dikonfirmasi)
**Dugaan akar masalah (belum dikonfirmasi pemilik):** tidak ada jalur pembayaran/internet cadangan untuk jam sibuk.

## Fakta vs dugaan (wajib)
- Yang ditulis sebagai fakta hanya yang **disebut pengguna**. Setiap "kenapa" lanjutan yang berasal dari penalaran sendiri (SOP, kebiasaan kerja, alat, beban kerja) diberi tanda `(dugaan, perlu dikonfirmasi)`.
- Akar masalah selalu ditulis sebagai **dugaan akar masalah** sampai pemilik mengonfirmasi; tutup dengan 1–2 pertanyaan konfirmasi singkat.
- Dugaan tidak masuk draf maaf ke pelanggan dan ringkasan WA; di sana cukup "kami sedang menelusuri penyebabnya".

## Kalimat yang HARUS dihindari (menyalahkan individu)
- "Karena kasir lalai/ceroboh/tidak teliti"
- "Karena karyawan X tidak becus"
- "Human error" tanpa penjelasan sistem apa yang seharusnya menangkap kesalahan itu

## Ganti dengan arah sistemik
- "Karena tidak ada langkah cek ulang sebelum [aksi]"
- "Karena SOP belum mencakup situasi [kondisi tertentu]"
- "Karena tidak ada alat/cadangan untuk [situasi]"
- "Karena informasi [X] tidak sampai ke [pihak] tepat waktu"

## Kapan nama orang tetap boleh disebut
Boleh disebut di **kronologi** ("kasir shift pagi melaporkan ke supervisor pukul 09.15") karena itu fakta kejadian, bukan penilaian. Yang dihindari adalah menjadikan nama orang sebagai **akar masalah** atau kesimpulan sebab-akibat.
