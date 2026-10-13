# Riwayat perubahan — cari-prospek-web

Catatan teknis per versi.

## Catatan revisi 1.0.3 (2026-10-13)
- SKILL.md: ditambah aturan bahwa alasan prospek hanya menyebut apa yang tertulis di sumber yang dikutip; kebutuhan atau ukuran usaha ('pasti butuh', 'terbesar') tidak boleh ditulis sebagai kepastian, melainkan sebagai perkiraan yang perlu dicek. Alur kerja dan batas 3 pencarian + 6 halaman tidak berubah.
- Folder `examples/` dirapikan karena ikut dikirim ke pembeli: nomor telepon/WA dan email usaha disamarkan (sisa 4 digit terakhir), nama perorangan diganti `[nama pemilik]`, dan alasan prospek yang spekulatif diganti kalimat hati-hati yang hanya menyebut isi sumber. Skor, verdik, tanggal uji, dan jumlah prospek tidak diubah; data fiktif untuk uji skrip tidak diubah.
- Tes `tests/uji_regresi.py` dijalankan ulang: lolos.

## Catatan revisi 1.0.2 (2026-10-06)
- Jalur pencarian dipersingkat agar selesai kurang dari sekitar 5 menit: hanya memakai halaman direktori publik (Google Maps, Kadin, marketplace B2B, media lokal) dengan batas 3 pencarian dan 6 halaman direktori; situs usaha tidak lagi dibuka satu per satu. Hasil 8-15 prospek, bukan 10-20.
- Bagian "Permintaan di luar batas" dipindah ke depan dan diubah menjadi tabel: penolakan 1-2 kalimat wajib menjadi kalimat pertama jawaban (login akun, scraping grup, beli database, WA massal), lalu padanan yang sah, lalu daftar tetap dibuat. Nomor HP perorangan tidak masuk tabel maupun CSV.
- Setelah web_search bawaan bot uji dihidupkan, skill diuji ulang pada 2026-10-10 dan lulus pada 2026-10-11 (skor uji OpenClaw 6,7 naik ke 8,2) tanpa perubahan isi skill.

## Catatan revisi 1.0.1 (2026-10-06)
- Revisi setelah uji pertama (skor 5,8 naik ke 7,9 dengan catatan lambat dan batas diabaikan): ditambah bagian "Batas waktu & upaya" (maksimal sekitar 25 halaman, sekitar 15 di kanal chat; tebak halaman kontak hanya sekali; hasil parsial lebih baik daripada tidak menjawab).
- Placeholder/dummy disaring (nomor berderet seperti 0812 3456 7890, alamat "No. 123", email @example, teks "Lorem"); penolakan permintaan terlarang ditaruh di awal jawaban; nama skill lain tidak disebut ke pengguna (ditawarkan dengan kalimat awam); bila menyebut beberapa jenis usaha, hasil dibagi merata.
- Script `saring_prospek.py` menambah penghapusan duplikat dan pengenalan alias. Uji regresi diperbarui.

## Catatan revisi 1.0.0 (2026-10-06)
- Rilis awal (uji internal): mencari calon pelanggan B2B dari web publik berdasarkan profil pelanggan ideal, dengan tabel prospek bersumber (URL dan tanggal cek), tiga prospek prioritas beserta satu kalimat pembuka, dan CSV siap tempel. Hanya kontak bisnis yang dipublikasikan; mode Rencana bila agent tidak punya alat pencarian web; script `saring_prospek.py` untuk merapikan daftar.
