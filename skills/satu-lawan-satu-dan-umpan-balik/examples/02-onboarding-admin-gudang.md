# Contoh 2: Normal kedua: onboarding admin gudang 30 hari

> Hasil uji OpenClaw asli versi 1.0.2 (2026-10-12, model claude-sonnet-5, uji otomatis agent). Perbandingan lengkap sebelum/sesudah: `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
"Senin depan 19 Okt ada anak baru masuk, Bagas, jadi admin gudang di toko bahan kue saya. Timnya 6 orang. Pendampingnya Bu Wati. Bikinin rencananya ya."

## Keluaran di chat (dengan skill)

> # Rencana Onboarding 30 Hari — Bagas (Admin Gudang)
>
> Mulai Senin, 19 Oktober 2026. Pendamping: Bu Wati. Tim: 6 orang.
>
> ## Hari Pertama — Senin, 19 Oktober
> - Sambutan singkat dari Anda ke seluruh tim (6 orang), perkenalkan Bagas dan perannya sebagai admin gudang.
> - Bu Wati mengajak keliling gudang: lokasi penyimpanan per kategori bahan (tepung, gula, mentega, cokelat, dll), alur barang masuk dari supplier, cara pencatatan stok yang dipakai toko.
> - Satu tugas kecil selesai hari itu juga (ditemani Bu Wati): menghitung dan mencatat stok satu rak/kategori kecil, supaya Bagas langsung merasa berkontribusi.
> - Bu Wati mendampingi penuh sepanjang shift hari ini.
>
> ## Minggu 1 — Senin 19 s.d. Minggu 25 Oktober
> Tujuan: kenal gudang dan bahan baku, paham cara pencatatan stok, paham prinsip barang lama dipakai/dijual dulu sebelum barang baru.
> - Ikut proses terima barang dari minimal satu supplier bersama Bu Wati.
> - Belajar kartu stok / sistem pencatatan yang dipakai (sebut nama alat/bukunya: [isian]).
> - Paham lokasi penyimpanan tiap kategori bahan.
> - Pendampingan: penuh, Bu Wati di sisi Bagas setiap shift.
>
> **Cek hari ke-7:** jatuh Minggu 25 Oktober, digeser dari Minggu 25 Oktober ke **Senin, 26 Oktober**. Ngobrol singkat 10-15 menit: apa yang sudah dipahami, apa yang masih bingung.
>
> ## Minggu 2 — Senin 26 Oktober s.d. Minggu 1 November
> Tujuan: mulai mencatat stok masuk/keluar sendiri, ikut opname kecil, mulai peka pada barang yang hampir habis atau mendekati kedaluwarsa.
> - Bagas mencatat sendiri, Bu Wati mengecek hasilnya tiap hari.
> - Dilatih lapor ke Bu Wati kalau ada selisih stok.
> - Pendampingan: aktif tapi mulai dikurangi — Bu Wati cek hasil kerja, bukan mendampingi tiap langkah.
>
> **Cek hari ke-14:** jatuh Minggu 1 November, digeser dari Minggu 1 November ke **Senin, 2 November**. Evaluasi ketelitian dan kecepatan pencatatan; sepakati perbaikan kalau perlu.
>
> ## Minggu 3 — Senin 2 s.d. Minggu 8 November
> Tujuan: pegang alur gudang dari awal sampai akhir (terima - catat - simpan - keluar) dengan pengawasan jarak jauh.
> - Mulai komunikasi langsung dengan supplier untuk konfirmasi pengiriman.
> - Bu Wati hanya memantau, tidak lagi mendampingi langsung kecuali diminta.
>
> ## Minggu 4 — Senin 9 s.d. Selasa 17 November
> Tujuan: kerja mandiri penuh, Bu Wati jadi tempat bertanya saja.
> - Bagas pegang tanggung jawab penuh pencatatan stok harian.
> - Siap dievaluasi di hari ke-30.
>
> **Cek hari ke-30:** **Selasa, 17 November** (tidak digeser). Evaluasi bersama Anda dan Bu Wati: apa yang sudah dikuasai, apa yang masih perlu didampingi, keputusan lanjut (lepas mandiri atau perpanjang pendampingan).
>
> ---
>
> ## Pesan WA Sambutan untuk Bagas
> "Halo Bagas, selamat ya sudah gabung jadi admin gudang di toko. Senin tanggal 19 Oktober ditunggu jam [isian: jam masuk]. Bu Wati yang akan mendampingi kamu minggu-minggu pertama, jadi langsung cari beliau begitu sampai. Sampai ketemu Senin!"
>
> ## Pesan WA untuk Bu Wati
> "Bu Wati, terima kasih sudah bersedia mendampingi Bagas, admin gudang baru yang mulai Senin 19 Oktober. Minggu pertama tolong didampingi penuh, minggu kedua mulai dilepas bertahap sambil dicek hasil pencatatannya. Kita ngobrol bareng lagi di hari ke-7 (Senin 26 Okt), hari ke-14 (Senin 2 Nov), dan evaluasi 30 hari (Selasa 17 Nov)."
>
> ---
>
> ## Asumsi
> - Toko tutup/libur hari Minggu, sehingga titik cek yang jatuh di hari Minggu digeser ke Senin berikutnya.
> - Jam masuk, nama alat pencatatan stok, dan tugas kecil hari pertama belum disebutkan, saya tandai `[isian]`.
>
> ## Pertanyaan
> 1. Apakah toko memang libur/tutup hari Minggu, atau tetap buka 7 hari?
> 2. Pencatatan stok pakai buku manual atau aplikasi/sistem kasir tertentu?
> 3. Jam kerja standar Bagas mulai pukul berapa, supaya pesan sambutan bisa diisi pasti?

## Catatan penguji

**Nilai: SEBELUM 5,5 | SESUDAH 9,0**
- SEBELUM: rencana hanya sekitar 2 minggu (bukan 30 hari), tanpa tanggal cek (hanya "Hari 1 - Senin 19 Okt" benar), tanpa pesan WA sambutan/pendamping; menulis ke memori agent (efek samping) dan menyebut "Dicatat juga di memori"; menutup dengan menu penawaran.
- SESUDAH: rencana per minggu dengan hari/tanggal benar dan terverifikasi python: hari ke-7 = Minggu 25 Okt digeser ke Senin 26 Okt, hari ke-14 = Minggu 1 Nov digeser ke Senin 2 Nov, hari ke-30 = Selasa 17 Nov (aturan hari pertama = hari ke-1 diterapkan benar; di 1.0.1 salah hitung). Ada tugas kecil selesai di hari pertama, pesan WA sambutan untuk Bagas dan pesan WA untuk pendamping Bu Wati, hal tidak diketahui `[isian]`, asumsi + 3 pertanyaan. Kekurangan kecil: asumsi "toko libur hari Minggu" dikarang (tapi dinyatakan sebagai asumsi dan ditanyakan); kalimat "digeser dari Minggu 25 Oktober ke Senin" agak canggung.
