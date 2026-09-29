# HASIL UJI (penguji independen) - umami-analitik 1.0.0 - 29 Sep 2026
Lingkungan: Umami 3.4.0 asli (Docker), akun view-only. 5 skenario (06-10) + A/B + banding pesaing. Python 3.11.

**Skor: 8/10.** Angka cocok dengan API mentah, DB, dan data fiktif penguji sendiri; keamanan (view-only, kunci disamarkan, tanpa redirect, HTTPS, injeksi diabaikan) lolos; A/B menang; pesaing tidak lebih baik untuk sasaran. Regresi 28/28; validate.py lolos. Status yang disarankan: layak `lulus`, uji platform asli oleh pemilik masih perlu (Windows/macOS/Telegram belum diuji siapa pun).

## Panduan docs/panduan-umami.md vs dokumentasi resmi
- docker-compose.yml resmi: image `umami:latest`, port 3000, `postgres:15-alpine`, healthcheck heartbeat, `TWO_FACTOR_ENCRYPTION_KEY`: sesuai; 4 perubahan pengaman jelas ditandai.
- Halaman resmi docs.umami.is/docs/api hanya menyebut kunci API untuk Cloud dan login untuk self-hosted; panduan bagian 7 (kunci API self-hosted 3.4.0) tidak tercantum di sana, tetapi terbukti jalan di instansi asli (Bearer). Tambahkan catatan "berdasar uji Komunitech, bukan dokumen resmi".
- Kredensial: tidak ada sandi/kunci tercetak di keluaran uji.

## Daftar perbaikan (tidak diperbaiki penguji)
1. (Sedang) Jelaskan bahwa "rata-rata lama" mengikuti Umami dan bisa lebih kecil dari selisih waktu sesungguhnya bila kunjungan diakhiri event (uji: 70 vs 73 dtk).
2. (Kecil) Periode tak dikenal memicu pesan argparse Inggris; buat pesan Indonesia dengan daftar periode.
3. (Kecil) Rentang kosong di masa lalu/depan: petunjuk "cek kode pelacak" menyesatkan; bedakan rentang sebelum data ada.
4. (Kecil) Hari berisi hanya event tampil "0 pengunjung unik"/tingkat konversi "-"; beri catatan.
5. (Kecil) Cantumkan di panduan §7 bahwa kunci API self-hosted belum ada di dokumentasi resmi.
6. Netralisasi rumus CSV tidak dapat diuji end-to-end (Umami menolak nama event berawalan = dan -); andalkan uji regresi.
