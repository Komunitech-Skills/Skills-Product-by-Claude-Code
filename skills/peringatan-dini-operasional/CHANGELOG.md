# Riwayat perubahan — peringatan-dini-operasional

Catatan teknis per versi.

## Catatan revisi 1.0.7 (2026-10-02)
- Jadwal harian (Langkah 4) hanya dibahas bila pengguna memintanya; agent tidak lagi menawarkannya sendiri.

## Catatan revisi 1.0.6 (2026-10-02)
- Revisi cacat dari uji OpenClaw: rujukan ke skill `laporan-insiden-usaha` hanya dipakai bila skill itu terpasang. Bila belum, agent meminta pengguna mencatat kronologi dan dampak secara tertulis.
- Pertanyaan penyebab di laporan dibuat umum ("mesin/peralatan: setting, kalibrasi, atau kondisi alat produksi berubah?"), tidak terpaku pada oven atau mixer. Uji regresi menyesuaikan.

## Catatan revisi 1.0.5 (2026-10-02)
- Hasil uji OpenClaw: agent dilarang memeriksa atau menyetel kanal, plugin, dan sesi, serta dilarang menawarkan kiriman ke grup atau pihak ketiga.
- Peringatan tidak menyalahkan orang (fakta disertai pertanyaan klarifikasi). `laporan_teks` wajib ditempel utuh dalam blok kode.
- Pencilan di 7 hari terakhir tidak lagi dibuang dari garis dasar (dulu angka kemarin bisa disebut "angka ekstrem lama"), dan baris info menyebut tanggalnya. Ditambah tes regresi data katering dari uji OpenClaw.

## Catatan revisi 1.0.4 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.3 (2026-09-29)
- Hasil uji OpenClaw 2026.9.6: agent selalu menyebut file log dan periode yang dipakai; nama usaha tidak pernah dikarang; tabel yang ditempel disimpan di folder kerja; aturan kerja standar ditambahkan (tidak memasang paket, tidak membuka file di luar yang diberikan, lokasi file hasil disebut).

## Catatan revisi 1.0.2 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/jadwal-openclaw.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.
- Lulus uji ulang (8/10); FAQ tanda kuning ditambahkan di README.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi dari uji independen (6/10): aturan warna diganti model peluang (normal, hitungan Poisson, kejadian, konstan) dengan syarat selisih minimal dan bertahan. 🟡 = 2σ satu hari; 🟠 = 3σ, atau 2σ di 2 dari 3 hari; 🔴 = 4σ, atau 3σ dan kemarin masih ≥ 2σ. Banding dengan hari yang sama paling tinggi 🟡.
- Metrik yang biasanya nol dan angka konstan tidak lagi "Normal" saat melonjak; opsi `--kejadian`; kolom teks tidak dikutip kecuali `--sertakan-catatan`; stok kurang dari 1 hari ditulis "habis besok" dengan perkiraan hari kosong; target 0, duplikat, dan angka ambigu di laporan teks ditangani; saran `--urutan-tanggal mdy`.
- Pada data sintetis yang stabil, hari berstatus 🟠 atau lebih turun dari 31% menjadi sekitar 3%, dan 🔴 dari 5,9% menjadi sekitar 0,2%.

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): membaca log harian operasional (CSV/Excel/tabel tempel), menghitung rata-rata 7 hari, tren, banding target dan hari yang sama 4 minggu lalu, batas kendali, dan sisa hari stok, lalu menandai peringatan dini.
