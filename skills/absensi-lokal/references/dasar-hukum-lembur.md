# Dasar Hukum Waktu Kerja & Upah Lembur — berlaku per 24 September 2026

> Ringkasan untuk alat bantu hitung, **bukan nasihat hukum**. Untuk kasus di luar cakupan (sektor usaha tertentu, sengketa lembur, perjanjian kerja khusus), tanyakan ke **Dinas Tenaga Kerja (Disnaker) setempat**, pengawas ketenagakerjaan, atau konsultan hukum/HR. Bila Peraturan Perusahaan (PP), Perjanjian Kerja (PK), atau Perjanjian Kerja Bersama (PKB) memberi ketentuan yang lebih baik bagi pekerja, ikuti ketentuan itu.

**Sumber utama:** Peraturan Pemerintah Nomor 35 Tahun 2021 tentang Perjanjian Kerja Waktu Tertentu, Alih Daya, Waktu Kerja dan Waktu Istirahat, dan Pemutusan Hubungan Kerja. Ditetapkan dan diundangkan **2 Februari 2021** (Lembaran Negara RI Tahun 2021 Nomor 45). Salinan resmi JDIH Kemnaker: https://jdih.kemnaker.go.id/asset/data_puu/PP352021.pdf (teks pasal di bawah dibaca langsung dari salinan itu pada 23 September 2026). PP ini melaksanakan UU 11/2020 tentang Cipta Kerja; UU tersebut kemudian diganti Perppu 2/2022 yang ditetapkan menjadi UU 6/2023. Per tanggal cek, belum ditemukan peraturan yang mencabut Pasal 21–33 PP 35/2021 — **pengguna tetap diminta memeriksa perubahan terbaru** di JDIH Kemnaker.

## Pasal yang dipakai skill

| Pasal | Isi (dikutip/diringkas dari teks resmi) | Dipakai untuk |
|---|---|---|
| 21 ayat (2) | Waktu kerja: a. 7 jam/hari dan 40 jam/minggu untuk 6 hari kerja; b. 8 jam/hari dan 40 jam/minggu untuk 5 hari kerja | Pilihan pola 5/6 hari kerja |
| 22 | Istirahat mingguan 1 hari untuk 6 hari kerja, atau 2 hari untuk 5 hari kerja | Default hari istirahat (Minggu; Sabtu–Minggu) + peringatan bila tidak sesuai |
| 23–25, 30 | Sektor usaha/pekerjaan tertentu boleh menerapkan waktu kerja lain; ketentuan lembur berlaku untuk semua perusahaan **kecuali** sektor tersebut | **Batasan**: sektor tertentu tidak didukung |
| 26 ayat (1)–(2) | Lembur paling lama 4 jam/hari dan 18 jam/minggu; batas ini tidak termasuk lembur pada hari istirahat mingguan dan/atau hari libur resmi | Peringatan > 4 jam/hari dan > 18 jam/minggu (hari kerja) |
| Penjelasan 26 ayat (2) | "Hari libur resmi" = hari libur nasional, hari yang diliburkan secara nasional, atau hari libur yang ditetapkan Pemerintah Daerah | Arti tabel `libur` |
| 27 ayat (1)–(5) | Wajib bayar upah lembur; dikecualikan bagi pekerja **golongan jabatan tertentu** (pemikir, perencana, pelaksana, dan/atau pengendali jalannya perusahaan, waktu kerja tidak dapat dibatasi, upah lebih tinggi) yang **diatur di PK/PP/PKB**; bila tidak diatur, pengusaha wajib membayar lembur | Opsi `--tanpa-lembur ya` (keputusan pengguna) |
| 28 ayat (1)–(3) | Lembur harus ada **perintah pengusaha dan persetujuan pekerja** secara tertulis dan/atau melalui media digital; boleh berupa daftar pekerja yang bersedia lembur; pengusaha membuat daftar pelaksanaan lembur (nama + lamanya) | **Lembur hanya dari daftar lembur disetujui**, tidak otomatis dari jam pulang; kolom catatan "disetujui oleh" |
| 29 | Wajib upah lembur, kesempatan istirahat, dan makan-minum ≥ 1.400 kkal bila lembur ≥ 4 jam (tidak dapat diganti uang) | Hanya pengingat (tidak dihitung) |
| 31 ayat (1) | Lembur hari kerja: **jam pertama 1,5 × upah sejam; setiap jam berikutnya 2 ×** | Pengali hari kerja |
| 31 ayat (2) huruf a | Hari istirahat mingguan/libur resmi, pola 6 hari kerja & 40 jam: **jam 1–7 = 2×; jam 8 = 3×; jam 9, 10, 11 = 4×** | Pengali libur pola 6 hari |
| 31 ayat (2) huruf b | Jika **hari libur resmi jatuh pada hari kerja terpendek** (pola 6 hari): **jam 1–5 = 2×; jam 6 = 3×; jam 7, 8, 9 = 4×** | Pengali "6p" (default hari terpendek = Sabtu, bisa diubah) |
| 31 ayat (3) | Hari istirahat mingguan/libur resmi, pola 5 hari kerja & 40 jam: **jam 1–8 = 2×; jam 9 = 3×; jam 10, 11, 12 = 4×** | Pengali libur pola 5 hari |
| 32 ayat (1)–(2) | Perhitungan lembur berdasarkan upah bulanan; **upah sejam = 1/173 × upah sebulan** | Rumus upah sejam |
| 32 ayat (3) | Bila upah = upah pokok + tunjangan tetap → dasar lembur 100% dari upah | Dasar default |
| 32 ayat (4) | Bila ada tunjangan tidak tetap dan (upah pokok + tunjangan tetap) < 75% keseluruhan upah → dasar = **75% keseluruhan upah** | Aturan 75% |
| 33 ayat (1) | Upah harian: upah sebulan = upah sehari × **25** (6 hari kerja) atau × **21** (5 hari kerja) | Opsi `--upah-harian` |
| 33 ayat (2)–(3) | Upah satuan hasil: upah sebulan = rata-rata 12 bulan; bila di bawah upah minimum, pakai upah minimum | **Tidak didukung** (isi upah sebulan sendiri) |

## Tabel pengali (jam setara)

| Jam lembur | Hari kerja | Libur, 5 hari | Libur, 6 hari | Libur resmi di hari terpendek (6 hari) |
|---|---|---|---|---|
| 1 | 1,5 | 2 | 2 | 2 |
| 2 | 3,5 | 4 | 4 | 4 |
| 4 | 7,5 | 8 | 8 | 8 |
| 5 | 9,5 | 10 | 10 | 10 |
| 6 | 11,5 | 12 | 12 | 13 |
| 7 | 13,5 | 14 | 14 | 17 |
| 8 | 15,5 | 16 | 17 | 21 |
| 9 | 17,5 | 19 | 21 | 25 |
| 10 | 19,5 | 23 | 25 | ditolak (> 9 jam) |
| 11 | 21,5 | 27 | 29 | ditolak |
| 12 | 23,5 | 31 | ditolak (> 11 jam) | ditolak |

Upah lembur = jam setara × upah sebulan ÷ 173. Lembur hari kerja di atas 4 jam tetap dihitung tetapi diberi peringatan (Pasal 26).

## Keputusan desain skill (bukan aturan)
- **Pembulatan:** total upah lembur per karyawan per periode dihitung dari jumlah jam setara, lalu **dibulatkan sekali ke rupiah terdekat** (0,5 ke atas) — sama dengan skill `slip-gaji-bpjs`. Rincian per hari hanya tampilan (dibulatkan terpisah, bisa selisih Rp 1 dengan total).
- **Jam pecahan** (mis. 1,5 jam) dihitung proporsional di setiap anak tangga pengali. Aturan tidak mengatur pecahan jam secara rinci; jika perusahaan membulatkan per 30 menit/per jam, masukkan jam yang sudah dibulatkan.
- **Tanggal lembur** = tanggal mulai shift (shift malam yang lewat tengah malam dihitung ke tanggal masuknya).
- Jam lembur yang disetujui dipakai apa adanya; bila lebih panjang dari yang terlihat di jam absen, script memberi peringatan (tidak mengurangi sendiri).
- **Cuti bersama** tidak otomatis dianggap hari libur resmi. Bagi swasta, cuti bersama umumnya mengurangi hak cuti tahunan dan pelaksanaannya mengikuti kebijakan perusahaan; apakah lembur pada hari itu dibayar dengan tarif hari libur **PERLU dikonfirmasi** ke Disnaker/PP perusahaan. Catat di `libur` hanya bila pengguna memutuskan demikian.
- Terlambat/pulang cepat, toleransi, dan jam istirahat adalah **kebijakan perusahaan**, bukan angka dari PP 35/2021.
- Belum dicocokkan dengan aplikasi HRIS/payroll lain; jika hasil berbeda, periksa dasar upah dan jam yang dimasukkan.

## Disclaimer untuk output
"Upah lembur: PP 35/2021 Pasal 31–32 (upah sejam = 1/173 × upah sebulan), hanya dari lembur yang disetujui, dibulatkan ke rupiah terdekat. Alat bantu hitung, bukan nasihat hukum; kasus khusus tanyakan ke Disnaker/konsultan."
