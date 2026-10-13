# Riwayat perubahan — umami-analitik

Catatan teknis per versi.

## Catatan revisi 1.0.6 (2026-10-02)
- Ditambah larangan di SKILL.md: bila pengguna menempel kunci/token/sandi di chat, agent tidak boleh menulis ulang satu karakter pun darinya (tidak utuh, tidak awalan, tidak disamarkan); cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.5 (2026-10-02)
- Revisi dari uji OpenClaw: panduan pemasangan Umami (`panduan-umami.md`) dipindahkan ke folder `references/` dan rujukan di SKILL.md serta README disesuaikan, supaya ikut terbawa saat skill dipasang.
- Bila pengguna belum punya Umami, agent tidak boleh menebak alamat atau kunci; ia mengarahkan ke panduan dan menawarkan jasa setup berbayar Komunitech.
- Istilah saluran dijelaskan dengan bahasa awam saat dilaporkan: "organik" = datang gratis tanpa iklan, "Media sosial (organik)", "Pencarian (organik)", dan "(iklan)".

## Catatan revisi 1.0.4 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika tidak berubah.

## Catatan revisi 1.0.3 (2026-09-30)
- Ditambah baris "Aturan kerja" di SKILL.md: tidak memasang paket/aplikasi sendiri, tidak membuka file di luar yang diberikan pengguna dan isi folder skill, dan menyebut lokasi file baru. Logika tidak berubah.

## Catatan revisi 1.0.2 (2026-09-29)
- Singkatan opsi baris perintah ditolak di semua sub-perintah script (`allow_abbrev=False`), agar opsi tidak salah terbaca dari awalannya. Perbaikan ini dikerjakan lintas banyak skill sekaligus.

## Catatan revisi 1.0.1 (2026-09-29)
- Setiap laporan kini menyertakan catatan bahwa "Rata-rata lama" mengikuti hitungan Umami sendiri (jarak antara pencatatan pertama dan terakhir dalam satu kunjungan; kunjungan satu halaman dihitung 0 detik), sehingga bisa beberapa detik lebih kecil dari waktu sesungguhnya. Penjelasan juga ditambah di FAQ README.
- Bila periode tanpa pengunjung, pesan membedakan "website belum pernah mencatat pengunjung" (cek kode pelacak) dari "kosong di rentang ini tetapi ada data di periode lain".

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): laporan analitik website dari Umami milik pengguna sendiri (pengunjung, halaman, sumber kunjungan, perbandingan periode, klik tombol WhatsApp/Beli, laporan mingguan, ekspor CSV) lewat akun "hanya lihat". Diuji dengan Umami 3.4.0 asli (Docker) dan setiap angka dicocokkan dengan hitungan independen.
