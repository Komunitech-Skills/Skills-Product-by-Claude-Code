# HASIL UJI - listmonk-newsletter 1.0.0 (penguji independen, 29 Sep 2026)
Lingkungan: listmonk v6.2.0 ASLI (Docker, postgres:17, port lokal, SMTP penampung), pengguna API berperan sesuai panduan §7. Penguji hanya membaca folder skill, panduan, CLAUDE.md. `validate.py --skill listmonk-newsletter` lolos. Berkas 06-10 dan 00-* adalah hasil penguji.

## Audit
- Format: frontmatter hanya name+description (791 karakter), SKILL.md 112 baris, README lengkap (jualan, FAQ 3), ATTRIBUTION ada. Catatan: catalog.csv menulis jalur `kurasi`, padahal karya orisinal.
- Lisensi: AGPL listmonk dipakai terpisah lewat HTTP, tidak disalin/didistribusi, "tidak berafiliasi" ada di README, ATTRIBUTION, panduan. Sesuai.
- Skrip: stdlib saja, tanpa eval/shell, tanpa redirect, alamat internet wajib HTTPS + `--izinkan-jarak-jauh`, token tak pernah tercetak (diuji), `simpan-akun` menolak non-terminal, `<script>` ditolak, bom XML ditahan Python. Tidak ada rahasia tertanam.

## Panduan vs dokumentasi resmi
Docker compose + `--install --idempotent --yes` + `LISTMONK_ADMIN_USER/PASSWORD` + pg >=12: cocok dokumentasi resmi dan BERHASIL saya jalankan dari nol. Peran §7 (13 izin) cukup untuk semua perintah skill. Email opt-in bawaan berbahasa Inggris (cocok catatan §6). Harga Brevo/SES bertanda "cek sendiri" (tidak diverifikasi ulang). UU PDP: No. 27/2022, berlaku penuh 17 Okt 2024 - benar. Kelemahan: §10 menyebut "dasar persetujuan" seolah satu-satunya; Pasal 20 UU PDP memuat beberapa dasar (kontrak, kepentingan sah, dll.) dan persetujuan harus tercatat/eksplisit - aman sebagai kebijakan, tapi sebaiknya jujur bahwa ini pilihan hati-hati.

## Skenario
| # | Skenario | Hasil |
|---|---|---|
| 1 | Impor CSV berpersetujuan (06) | Lulus dengan catatan |
| 2 | Draf + uji kirim (07) | Lulus |
| 3 | Jadwal + statistik (08) | Lulus, angka benar |
| 4 | Input kurang (argumen wajib, waktu, kolom email, nama list ambigu) | Lulus |
| 5 | Di luar cakupan: daftar beli/tanpa berhenti (10) | SEBAGIAN: saringan kata mudah dielak |
Data rusak (09): baik, satu Traceback mentah. Gerbang jumlah penerima tidak bisa dilewati; gerbang uji-kirim bisa (--tanpa-uji).
A/B (00-pembanding): skill menang telak. Pesaing (00-banding-pesaing): menang untuk audiens sasaran.

## Skor kualitas: 7/10 (lulus bersyarat; tidak rilis sebelum P1 selesai)
Kuat: alur nyata teruji di listmonk asli, angka benar, gerbang jumlah kokoh, sidik isi, keamanan token, panduan bekerja. Turun karena klaim keamanan tidak sepenuhnya benar (README: "kirim ditolak bila belum uji kirim"; "menolak daftar beli") dan tiga celah nyata.

## Daftar perbaikan
P1 (wajib)
1. Hapus `--tanpa-uji` (atau tolak untuk `kirim`), sesuaikan SKILL/README.
2. Lint tautan berhenti: abaikan komentar HTML/`{{ }}` di dalam `<!-- -->`; lebih baik periksa hasil render uji-kirim (tautan `/subscription/` di email uji).
3. `uji-kirim`: batasi ke alamat yang pemilik nyatakan miliknya (mis. wajib `--ini-email-saya`, maks. beberapa alamat uji, tidak membuat pelanggan untuk alamat asing) agar tidak jadi jalan blast.
4. Saringan sumber persetujuan: perluas (vendor, grup WA, marketplace, teman, "tidak tahu") dan ubah ke daftar sumber sah yang diizinkan (formulir, QR, checkout dengan kotak tak tercentang, dsb.); jujur di README bahwa saringan hanya pengaman tambahan.
P2
5. Kolom setuju kosong = tidak setuju (atau minta konfirmasi) bukan setuju.
6. Bersihkan nama berawalan `=+-@` sepenuhnya/tandai; pesan impor "7 dari 7" beri catatan bila sebagian sudah berhenti/blocklist (tidak dihidupkan lagi).
7. Tangkap `ParseError` xlsx menjadi pesan ramah; pesan 404 "bukan listmonk?".
8. Catalog jalur -> `orisinal`; panduan §10 lunakkan kalimat dasar hukum; catat `docker-compose` tanpa `restart` dsb. tidak perlu.
9. Uji nyata belum dilakukan: SMTP sungguhan, inbox, Windows/macOS, Root URL/HTTPS - tetap PERLU UJI NYATA (uji platform asli pemilik).
Setelah P1, uji ulang oleh penguji independen.
