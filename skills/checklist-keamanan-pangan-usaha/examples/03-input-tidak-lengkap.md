# Skenario 3: Input tidak lengkap

- Tanggal: 2026-10-12 | skill v1.0.2 | OpenClaw, model claude-sonnet-5
- Nilai: SEBELUM 5.5 -> SESUDAH 8.5

## Input

Bikinin checklist keamanan pangan buat usaha saya.

## Output SESUDAH (dengan skill)

> # Paket Keamanan Pangan - Kafe/Warung
>
> **Asumsi** (karena belum ada detail usaha, saya pakai default umum — sebutkan detail usaha Anda dan saya sesuaikan):
> - Jenis usaha: **kafe/warung**
> - Menu/bahan utama: ayam, telur, nasi, santan, susu (gorengan dan makanan penahan panas)
> - Staf: 3 orang, 1 penanggung jawab
> - Peralatan: ada kulkas & freezer, **belum ada termometer pangan** — ini penting, lihat catatan di bagian Log Suhu
> - Jam buka: `[isian: jam buka]`
>
> Penafian singkat: ini alat bantu menyusun kebiasaan kerja aman, bukan pengganti pelatihan penjamah makanan atau pemeriksaan resmi Dinkes/BPOM. Angka suhu dari WHO/FDA/USDA (dicek 2026-10-12). Bagian perizinan **PERLU REVIEW** ke instansi setempat.
>
> ---
>
> ## 1. Daftar Periksa Harian
>
> **[Nama Usaha]** — Tanggal: ______ Petugas: ______
>
> ### Saat datang
> - [ ] Cuci tangan dengan sabun 20 detik; rambut tertutup, kuku pendek, tanpa perhiasan
> - [ ] Staf sakit (muntah, diare, demam, kuning)? Jangan pegang makanan, lapor penanggung jawab
> - [ ] Cek tanda hama (kotoran, bungkus digigit) dan sampah semalam sudah keluar
> - [ ] Baca suhu kulkas dan freezer, catat di log
>
> ### Sebelum buka
> - [ ] Permukaan kerja dibersihkan lalu disanitasi
> - [ ] Talenan/pisau terpisah: mentah vs matang
> - [ ] Bahan lama di depan (FIFO); buang yang lewat tanggal
> - [ ] Sabun, tisu, sanitizer, penutup sampah tersedia
> - [ ] Alergen: bahan dan alat berlabel jelas
>
> ### Selama jam sibuk
> - [ ] Makanan panas tetap ≥ 60 °C; cek tiap 2 jam, catat
> - [ ] Ayam/unggas matang inti ≥ 74 °C (ukur bagian paling tebal); panasan ulang ≥ 74 °C
> - [ ] Makanan matang tidak di suhu ruang lebih dari 2 jam (1 jam bila ruangan > 32 °C)
> - [ ] Cuci tangan setelah pegang mentah, uang, ponsel, sampah
> - [ ] Kain lap basah diganti; wadah tertutup
>
> ### Saat tutup
> - [ ] Sisa matang: dinginkan cepat (wadah dangkal) ke 21 °C dalam 2 jam, lalu ≤ 5 °C dalam 4 jam berikutnya; atau buang
> - [ ] Semua bahan diberi label nama + tanggal, tutup rapat
> - [ ] Alat, talenan, lantai dapur dibersihkan; saluran air bersih
> - [ ] Sampah dibuang, tempat sampah tertutup
> - [ ] Baca suhu kulkas/freezer terakhir, catat; tanda tangan: ______
>
> ---
>
> ## 2. Daftar Mingguan dan Bulanan
>
> | Periode | Kegiatan |
> |---|---|
> | Mingguan | Cek hama (celah dinding, sampah, jebakan); bersihkan dalam kulkas; bersihkan penyedot asap & saluran air |
> | Mingguan | FIFO menyeluruh — buang bahan yang lewat tanggal |
> | Bulanan | Kalibrasi termometer (uji es batu: harus ± 0 °C) |
> | Bulanan | Cek stok sabun, sanitizer, tisu; servis rutin kulkas/freezer bila perlu |
>
> ---
>
> ## 3. Log Suhu
>
> > **Catatan penting:** Anda belum punya termometer pangan. Log suhu di bawah **tidak bisa diisi dengan akurat** tanpa alat ukur — tebakan dari rasa/warna bukan penentu aman. Sarankan beli termometer pangan tusuk (murah, tersedia di toko alat dapur/online, mulai puluhan ribu rupiah). Sementara menunggu, pakai checklist visual: catat jam makanan keluar dari penahan panas/kulkas, dan jangan biarkan lebih dari 2 jam di suhu ruang.
>
> **[Nama Usaha]** — Bulan: ______
>
> | Alat | Batas | Jika melebihi, lakukan |
> |---|---|---|
> | Kulkas | ≤ 5 °C | Cek pintu/isi terlalu penuh; ukur ulang 30 menit; bila tetap > 5 °C dan bahan berisiko sudah > 2 jam: buang bahan itu; panggil teknisi |
> | Freezer | ≤ -18 °C | Cek pintu/colokan; jangan buka berulang; bila bahan sudah lunak/cair sebagian: jangan dibekukan ulang, masak segera atau buang |
> | Penahan panas | ≥ 60 °C | Panaskan ulang cepat sampai ≥ 74 °C lalu tahan; bila sudah < 60 °C lebih dari 2 jam: buang |
> | Masak ayam/unggas (inti), bentuk apa pun | ≥ 74 °C | Lanjut masak, ukur ulang di bagian paling tebal |
> | Masak daging giling, hidangan telur | ≥ 71 °C | Lanjut masak, ukur ulang |
> | Pemanasan ulang | ≥ 74 °C inti dalam ≤ 2 jam | Lanjut panaskan; jangan pakai penahan panas untuk memanaskan ulang |
>
> | Tanggal | Jam | Alat | Suhu (°C) | OK? | Tindakan | Paraf |
> |---|---|---|---|---|---|---|
> | | | Kulkas | | | | |
> | | | Freezer | | | | |
> | | | Penahan panas | | | | |
> | | | Masak: ____ | | | | |
>
> ---
>
> ## 4. Kartu Staf — 10 Aturan Dapur
>
> 1. Cuci tangan sabun 20 detik: sebelum kerja, habis toilet, habis pegang mentah, sampah, HP, uang.
> 2. Sakit perut, muntah, diare, demam, mata kuning: jangan pegang makanan, lapor, pulang dulu.
> 3. Mentah dan matang dipisah: talenan, pisau, wadah, dan rak kulkas (matang di atas, mentah di bawah).
> 4. Dingin tetap dingin (≤ 5 °C), panas tetap panas (≥ 60 °C). Jangan biarkan lama di antaranya.
> 5. Matang sampai dalam: semua ayam/unggas (utuh, potong, goreng, bakar) dan sisa panasan ≥ 74 °C. Ukur, jangan kira-kira.
> 6. Sisa panas dinginkan cepat: wadah dangkal, jangan ditutup rapat saat masih panas, lalu kulkas.
> 7. Semua bahan berlabel nama + tanggal. Yang lama dipakai dulu. Lewat tanggal: buang, jangan diganti label.
> 8. Ada pesanan alergi (kacang, susu, telur, gandum, dll; juga kelapa/santan bila pelanggan alergi kelapa)? Beri tahu penanggung jawab, pakai alat bersih.
> 9. Bersihkan dulu, baru sanitasi. Kain lap kotor diganti.
> 10. Ragu soal aman atau tidak? Buang dan tanya penanggung jawab.
>
> ---
>
> ## 5. Peta Risiko Menu (berdasarkan asumsi: ayam, telur, nasi, santan, susu)
>
> | Bahan | Risiko | Batas aman | Alergen |
> |---|---|---|---|
> | Ayam | Salmonella, Campylobacter; kontaminasi silang | Matang inti ≥ 74 °C di bagian paling tebal; talenan terpisah dari sayur/matang | — |
> | Telur | Salmonella | Langsung saji ≥ 63 °C; hidangan/ditahan ≥ 71 °C; simpan kulkas | Telur (wajib disebut) |
> | Nasi | Bacillus cereus (spora tahan masak) | Jangan di suhu ruang lama; dinginkan cepat atau tahan ≥ 60 °C | — |
> | Santan | Cepat basi | Masak sampai mendidih; simpan dingin; jangan campur santan baru & lama | **Kelapa** (sebut terpisah, bukan "susu") |
> | Susu/krim | Cepat berkembang bakteri | Kulkas ≤ 5 °C, catat tanggal buka | Susu hewani (wajib disebut) |
>
> **Kontaminasi silang spesifik:** talenan ayam mentah tidak boleh dipakai untuk sayur lalapan/bahan siap santap tanpa dicuci-sanitasi dulu.
>
> ---
>
> ## 6. Perizinan (PERLU REVIEW — cek ke Dinkes/DPMPTSP/BPOM/BPJPH setempat)
>
> | Izin | Relevan untuk | Instansi | Catatan |
> |---|---|---|---|
> | NIB | Semua usaha | OSS | Dasar usaha, juga syarat daftar halal |
> | SLHS + pelatihan penjamah makanan | Kafe/warung | Dinkes kab/kota | PERLU REVIEW syarat terbaru |
> | **Sertifikasi halal: WAJIB** (bukan opsional) | Semua makanan/minuman yang dijual | BPJPH (ptsp.halal.go.id) | UMK wajib mulai **18 Okt 2026**; menengah/besar sejak 18 Okt 2024. UMK bisa Self Declare/SEHATI (gratis). Tenggat UMK tinggal beberapa hari dari sekarang — sarankan segera daftar. |
> | PIRT/SPP-IRT | Bila ada produk kemasan dijual (kue kering, minuman kemasan) | Dinkes kab/kota | Tidak semua jenis pangan bisa PIRT |
>
> ---
>
> Untuk menyempurnakan checklist ini jadi lebih spesifik ke usaha Anda, boleh dijawab (maksimal 3):
> 1. Jenis usaha apa persis (kafe, katering rumahan, toko kue, minuman, atau frozen food)?
> 2. Menu utama apa saja yang dijual?
> 3. Berapa staf dan sudah ada termometer pangan atau belum?

## Catatan

SEBELUM 5,5: checklist umum 10 bagian, tidak disesuaikan jenis usaha (tidak ada log suhu, kartu staf, peta risiko), kulkas ≤4 °C (lebih ketat, tidak salah), halal "wajib bertahap untuk banyak kategori" kabur tanpa tanggal, 1 pertanyaan di akhir. SESUDAH 8,5: langsung kerja dengan asumsi eksplisit (kafe/warung), paket 6 bagian siap cetak, angka konsisten (74/71/63, 5/-18/60 °C, 2 jam/1 jam, 21 °C/2 jam lalu 5 °C/4 jam), jujur soal tanpa termometer, halal WAJIB 18 Okt 2026, tepat 3 pertanyaan. Kekurangan: sangat panjang dan menebak menu (ayam, susu) sehingga sebagian tidak relevan.

Perbandingan lengkap dengan hasil SEBELUM: `00-openclaw-sebelum-sesudah.md`.
