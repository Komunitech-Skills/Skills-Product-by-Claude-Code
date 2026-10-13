# Riwayat perubahan — vikunja-tugas

Catatan teknis per versi.

## Catatan revisi 1.0.13 (2026-10-02)
- Aturan token yang tertempel di chat diperketat: agent tidak boleh menulis ulang token secara utuh, sebagian, atau sebagai awalan/akhiran (mis. "tk_7f3a9..."), apa pun alasannya.

## Catatan revisi 1.0.12 (2026-10-02)
- Bila pengguna menempel token di chat, balasan wajib memuat templat peringatan yang mengandung kalimat "segera ganti token ini" (token dianggap sudah bocor, hapus di Vikunja lalu buat yang baru). Ditambah butir di daftar periksa.

## Catatan revisi 1.0.11 (2026-10-02)
- Aturan baru di SKILL.md: bila pengguna menempel kunci/token/password di chat, agent tidak boleh menulis ulang satu karakter pun darinya dan cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.10 (2026-10-02)
- Salinan panduan pasang Vikunja untuk UMKM (bahasa awam) ditambahkan ke dalam folder skill di `references/panduan-vikunja.md`, supaya ikut terbawa saat skill dipasang. Semua rujukan di SKILL.md, referensi, dan pesan galat script diperbarui. Panduan memuat catatan tawaran jasa setup berbayar Komunitech dan keterangan bahwa Komunitech tidak berafiliasi dengan Vikunja.

## Catatan revisi 1.0.9 (2026-10-02)
- Pemicu `dari-teks` diperjelas: setiap kali pengguna menempel notulen rapat, rangkuman grup WA, atau daftar poin ("ubah jadi to-do"), agent wajib menjalankan `dari-teks` lebih dulu dan tidak menyusun tugas, PIC, atau tenggat dari kepala sendiri.
- Bila Vikunja belum terpasang, agent tidak mengunduh atau memasang sendiri, tetapi mengarahkan ke panduan pemasangan dan menawarkan jasa setup berbayar Komunitech.

## Catatan revisi 1.0.8 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.7 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.6 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.5 (2026-09-29)
- `dari-teks` tidak lagi menangkap kata permintaan pembuka sebagai nama PIC ("Mohon:", "Tolong:", "Harap:", "Silakan:", "Dimohon:", "Pastikan:", "Please:"). Nama asli dan `--anggota` tetap diprioritaskan. 71 tes lulus.

## Catatan revisi 1.0.4 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.

## Catatan revisi 1.0.3 (2026-09-29)
- `dari-teks` tidak lagi salah menganggap kata judul umum sebagai nama PIC, mis. "TOPIC:", "INFO:", "UPDATE:", "STATUS:", "SUBJECT:", "AGENDA:", "FYI:", "Perihal:" (daftar kata Inggris dan Indonesia diperluas). Nama anggota yang diberikan lewat `--anggota` tetap menang. 69 tes lulus.

## Catatan revisi 1.0.2 (2026-09-28)
- Dokumentasi penugasan `--ke`: orang yang dituju harus sudah menjadi kolaborator proyek di Vikunja, lengkap dengan cara menambahkannya (SKILL.md bagian D.4).
- `dari-teks` kini mengenali label eksplisit `PIC: Nama` di awal, tengah, atau akhir baris. 67 tes lulus (uji ulang 9/10).

## Catatan revisi 1.0.1 (2026-09-26)
- Tindak lanjut uji independen pertama (8/10) dengan Vikunja 2.6.0 asli: penugasan `--ke` terbukti didukung token API bila token memiliki izin kelompok "Tasks Assignees". Panduan izin token dikoreksi (kotak yang benar bernama "Projectusers" di kelompok Projects), dan pesan galat 401 di langkah penugasan kini menyebut penyebab itu.
- Laporan `hari-ini` dan `terlambat` memberi catatan bahwa tugas yang sama bisa muncul di keduanya. 64 tes lulus.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): mengoperasikan Vikunja (manajer tugas open-source milik pengguna sendiri) lewat REST API resmi. Daftar proyek, tugas hari ini/terlambat/minggu ini, cari tugas, tambah tugas dengan tanggal Indonesia, tandai selesai, ringkasan, dan jadwal laporan.
