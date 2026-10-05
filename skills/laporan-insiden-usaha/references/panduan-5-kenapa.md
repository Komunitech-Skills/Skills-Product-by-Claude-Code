# Panduan "5 Kenapa" Tanpa Menyalahkan Orang

Dipakai saat menyusun bagian **Akar Masalah** di `laporan-insiden-usaha`. Tujuannya: berhenti di penyebab yang **bisa diperbaiki lewat proses/alat/SOP**, bukan di "karena si A lalai".

## Cara pakai
Tanyakan "kenapa" berulang (biasanya 3–5 kali) dari gejala yang terlihat sampai ketemu penyebab sistemik. Setiap jawaban jadi pertanyaan "kenapa" berikutnya.

### Contoh 1 — Pesanan salah kirim massal
1. Kenapa banyak pesanan tertukar? → Karena label pengiriman tercetak salah alamat untuk 40 pesanan.
2. Kenapa label bisa salah alamat? → Karena admin menyalin data dari sheet yang belum di-refresh setelah update alamat terbaru.
3. Kenapa sheet tidak di-refresh dulu? → Karena tidak ada langkah "cek ulang sheet sebelum cetak label" di SOP packing.
4. Kenapa langkah itu tidak ada di SOP? → Karena SOP packing terakhir dibuat sebelum volume pesanan naik 3x saat promo, belum diperbarui.
**Akar masalah:** SOP packing belum menyesuaikan volume tinggi saat promo — tidak ada langkah verifikasi data sebelum cetak label massal.

### Contoh 2 — Mesin kasir/QRIS error saat jam sibuk
1. Kenapa QRIS error? → Karena koneksi internet toko putus-nyambung.
2. Kenapa koneksi tidak stabil? → Karena hanya mengandalkan 1 sumber internet tanpa cadangan.
3. Kenapa tidak ada cadangan? → Karena belum pernah dianggap perlu, insiden ini yang pertama separah ini.
**Akar masalah:** Tidak ada jalur pembayaran/internet cadangan untuk jam sibuk.

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
