# Skenario 1: Normal utama: katering nasi box, tanpa termometer, jebakan 63 °C untuk ayam (SESUDAH dijalankan di konteks Telegram `uji-tg.sh`)

- Tanggal: 2026-10-12 | skill v1.0.2 | OpenClaw, model claude-sonnet-5
- Nilai: SEBELUM 6.0 -> SESUDAH 8.0

## Input

Katering rumahan nasi box (ayam goreng potong utuh, telur balado, sayur santan), 3 staf, kulkas tanpa termometer, antar pakai motor 1 jam: bikinkan checklist keamanan pangan harian, daftar alergen untuk label, dan izin apa saja yang perlu. Ayam 63 °C cukup kan biar cepat?

**Sumber acuan angka dan aturan pada output di bawah** (ditambahkan kurator 2026-10-13, sama dengan `references/` skill): ayam/unggas ≥ 74 °C inti — FDA, *Food Code 2022* (+ Supplement 2024), bab 3 dan USDA FSIS, *Safe Minimum Internal Temperature Chart* (diperbarui 2024); hidangan telur yang ditahan (telur balado) ≥ 71 °C — USDA FSIS, *Safe Minimum Internal Temperature Chart* (diperbarui 2024); 63 °C hanya untuk ikan/seafood, telur langsung saji, dan daging sapi/kambing utuh — FDA, *Food Code 2022* (+ Supplement 2024), bab 3 dan USDA FSIS, *Safe Minimum Internal Temperature Chart* (diperbarui 2024); batas 2 jam di suhu ruang (1 jam bila > 32 °C) — USDA FSIS, *Safe Minimum Internal Temperature Chart* (diperbarui 2024) dan WHO, *Five Keys to Safer Food* (2006); kulkas ≤ 5 °C — FDA, *Food Code 2022* (+ Supplement 2024), bab 3 dan WHO, *Five Keys to Safer Food* (2006); pendinginan 21 °C dalam 2 jam lalu ≤ 5 °C dalam 4 jam berikutnya — FDA, *Food Code 2022*, 3-501.14; alergen — Peraturan BPOM No. 31 Tahun 2018 Pasal 49 ayat (3), diubah Peraturan BPOM No. 20 Tahun 2021; halal (usaha mikro/kecil wajib mulai 18 Okt 2026) — UU 33/2014 tentang Jaminan Produk Halal dan PP 42/2024 (mencabut PP 39/2021); BPJPH (2026); NIB/SLHS/PIRT — Permenkes 2/2023 (mencabut Permenkes 1096/2011) dan Peraturan BPOM 31/2018; syarat SLHS/PIRT PERLU REVIEW ke Dinkes/OSS. Kalibrasi termometer dengan air es 0 °C adalah praktik umum.

## Output SESUDAH (dengan skill)

> **Ayam 63 °C: tidak, jangan.** Ayam/unggas — digoreng utuh, potong, berapa pun bentuknya — wajib matang inti **≥ 74 °C** di bagian paling tebal. Salmonella dan Campylobacter di bagian dalam ayam baru mati di suhu itu; 63 °C hanya berlaku untuk ikan/seafood, telur langsung saji, atau daging sapi/kambing utuh — bukan ayam. Kalau mau lebih cepat: potong lebih kecil/pipih biar matang merata, bukan turunkan suhu. Termometer tusuk (bukan infrared) wajib untuk cek ini — infrared cuma baca permukaan.
>
> Berikut paket lengkapnya, disesuaikan dengan kateringmu.
>
> **Paket Keamanan Pangan — Katering Rumahan Nasi Box**
>
> **Asumsi** (koreksi kalau meleset):
> - Menu: nasi, ayam goreng potong utuh, telur balado, sayur santan
> - 3 staf, 1 bertindak penanggung jawab harian
> - Ada kulkas, belum ada freezer terpisah, belum ada termometer
> - Pengantaran motor ±1 jam dari matang/kemas sampai ke pelanggan
> - Jam masak/kemas: [isian: jam buka]
>
> **1. Checklist Harian**
>
> Saat datang:
> - [ ] Cuci tangan sabun 20 detik; rambut tertutup, kuku pendek
> - [ ] Staf sakit (muntah/diare/demam/mata kuning)? Jangan pegang makanan, lapor dulu
> - [ ] Cek tanda hama, sampah semalam sudah keluar
> - [ ] Lihat kondisi kulkas (dingin terasa, tidak ada bau busuk) — catat di log
>
> Sebelum masak:
> - [ ] Permukaan kerja dibersihkan + disanitasi
> - [ ] Talenan/pisau terpisah: mentah (ayam) vs matang/sayur
> - [ ] Bahan lama dipakai dulu (FIFO); buang yang lewat tanggal
> - [ ] Ayam disimpan terpisah, tidak menetes ke bahan lain
>
> Saat masak & kemas (titik paling kritis untuk kalian):
> - [ ] Ayam goreng: ukur inti bagian paling tebal, wajib ≥ 74 °C sebelum diangkat
> - [ ] Telur balado: masak sampai inti ≥ 71 °C (ini hidangan matang yang ditahan, bukan telur langsung saji)
> - [ ] Sayur santan: didihkan sampai benar-benar mendidih, jangan campur santan baru dengan sisa lama
> - [ ] Catat jam makanan selesai matang/mulai dikemas — ini jam mulai hitungan suhu ruang
> - [ ] Nasi box dikemas secepat mungkin, jangan dibiarkan terbuka lama di meja
>
> Saat antar (motor, ±1 jam):
> - [ ] Total waktu dari matang sampai dimakan maksimal **2 jam** di suhu ruang biasa, **1 jam saja** kalau cuaca/boks panas (>32 °C, misal siang terik atau boks kena matahari langsung)
> - [ ] 1 jam perjalanan + waktu kemas + waktu nunggu pelanggan makan = cek totalnya, jangan cuma hitung waktu jalan
> - [ ] Pakai boks tertutup rapat, kalau bisa boks berinsulasi, supaya panas bertahan lebih lama
> - [ ] Rute jauh/macet: prioritaskan antar dulu yang dimasak paling awal
>
> Saat tutup:
> - [ ] Sisa matang yang tidak terjual: dinginkan cepat (wadah dangkal) ke 21 °C dalam 2 jam, lalu ≤5 °C dalam 4 jam berikutnya — atau buang kalau tidak sempat
> - [ ] Semua bahan diberi label nama + tanggal
> - [ ] Alat, talenan, area masak dibersihkan
> - [ ] Tanda tangan penanggung jawab: ____
>
> **2. Mingguan/Bulanan**
> - [ ] Cek hama: celah, sampah, jebakan tikus/kecoa
> - [ ] Bersih dalam kulkas total, buang bahan kadaluarsa
> - [ ] Stok sabun cuci tangan dan sanitizer cukup
> - [ ] Setelah beli termometer: uji kalibrasi pakai air es, harus baca ±0 °C
>
> **3. Log Suhu — catatan penting**
>
> Tanpa termometer, log suhu **tidak bisa diisi jujur** — jangan ditulis asal bagus, itu cuma bikin kalian merasa aman padahal tidak tahu kondisi sebenarnya. Belinya murah (termometer pangan tusuk, bukan infrared, cek harga di toko Anda). Sementara ini pakai cara visual:
> - [ ] Kulkas terasa dingin solid, tidak ada bahan "hangat" di dalamnya
> - [ ] Catat jam ayam/telur selesai dimasak setiap batch, bukan suhunya
> - [ ] Catat jam berangkat antar dan estimasi jam sampai
>
> Begitu ada termometer, format log:
> Tanggal | Jam | Alat/masakan | Suhu °C | OK? | Tindakan | Paraf
> Batas: kulkas ≤5 °C, ayam masak ≥74 °C, telur ≥71 °C, santan mendidih.
>
> **4. Kartu Staf (tempel di dapur)**
> 1. Cuci tangan sabun 20 detik: sebelum kerja, habis toilet, habis pegang ayam mentah, HP, uang
> 2. Sakit perut/muntah/diare/demam: jangan pegang makanan, lapor dulu
> 3. Ayam mentah dan matang dipisah: talenan, pisau, wadah beda
> 4. Ayam goreng matang WAJIB sampai dalam, ≥74 °C — ukur, jangan kira-kira dari warna/garing luar
> 5. Telur balado matang sampai inti, ≥71 °C
> 6. Santan dimasak sampai mendidih penuh, tidak dicampur sisa santan lama
> 7. Catat jam makanan matang/dikemas — ini penentu batas waktu antar
> 8. Nasi box diantar maksimal 2 jam dari matang (1 jam kalau cuaca panas)
> 9. Bahan berlabel nama + tanggal; yang lama dipakai dulu; lewat tanggal dibuang
> 10. Ragu soal aman? Jangan dikirim — tanya penanggung jawab dulu
>
> **5. Peta Risiko Menu**
>
> Ayam goreng (potong utuh)
> - Risiko: Salmonella/Campylobacter, kontaminasi silang dari ayam mentah
> - Aman: talenan terpisah, matang inti ≥74 °C di bagian paling tebal, cuci tangan setelah pegang ayam mentah
> - Alergen: kalau dilumuri tepung terigu sebelum goreng → gluten (serealia bergluten); kalau tepung bebas gluten, tidak perlu dicantumkan
>
> Telur balado
> - Risiko: Salmonella pada telur mentah/setengah matang
> - Aman: masak sampai inti ≥71 °C karena ini hidangan yang ditahan di boks, bukan langsung disajikan panas
> - Alergen: telur; cek juga kecap/saus balado — kalau pakai kecap, tambahkan kedelai
>
> Sayur santan
> - Risiko: cepat basi di suhu ruang, bukan susu jadi beda penanganan dari produk susu
> - Aman: didihkan tuntas, dinginkan cepat kalau sisa, jangan campur santan baru-lama
> - Alergen: kelapa (santan) — sebutkan terpisah untuk pelanggan yang alergi kelapa, bukan ditulis "susu/santan"
>
> Nasi
> - Risiko: Bacillus cereus kalau didiamkan lama di suhu ruang hangat
> - Aman: masak cukup, jangan dibiarkan di rice cooker hangat berjam-jam tanpa putar stok, segera kemas setelah matang
>
> Kontaminasi silang spesifik dapur kalian: talenan ayam mentah jangan dipakai untuk sayur/lalapan sama sekali, meski sudah "dicuci sekilas" — pakai talenan warna berbeda kalau bisa.
>
> **6. Perizinan (PERLU REVIEW ke Dinkes/DPMPTSP/BPOM/BPJPH setempat, bukan nasihat hukum final)**
> - NIB — dasar legalitas usaha, urus lewat OSS, juga syarat daftar halal
> - SLHS (Sertifikat Laik Higiene Sanitasi) + pelatihan penjamah makanan — relevan untuk jasa boga/katering, lewat Dinkes kab/kota
> - PIRT — hanya kalau ada produk kemasan yang dijual terpisah (bukan nasi box harian biasa), lewat Dinkes kab/kota
> - **Sertifikasi Halal: WAJIB, bukan opsional.** Untuk usaha mikro/kecil wajib mulai **18 Oktober 2026 — itu 6 hari lagi dari sekarang.** Daftar di BPJPH (ptsp.halal.go.id), jalur Self Declare/SEHATI biasanya gratis untuk UMK. Ini paling mendesak di antara semua izin — sarankan daftar minggu ini juga.
>
> Pengingat: ini kebiasaan kerja aman, bukan pengganti pelatihan penjamah makanan resmi atau pemeriksaan Dinkes/BPOM — cocokkan angka dan syarat izin dengan instansi setempat.
>
> Tiga hal biar lebih pas:
> 1. Freezer ada atau cuma kulkas tunggal?
> 2. Rata-rata berapa porsi/hari dan jarak antar terjauh (selain yang 1 jam ini)?
> 3. Ada produk dijual terpisah dalam kemasan (misal sambal/kerupuk kemasan) selain nasi box?

## Catatan

SEBELUM 6,0 (lokal; versi Telegram 6,5): menolak 63 °C dengan benar (74 °C), daftar alergen terpisah ada (versi Telegram malah lebih rapi dari SESUDAH), tetapi: "batas mutlak 4 jam" di zona bahaya (angka karangan, standar 2 jam/1 jam >32 °C), halal ditaruh di "Sangat disarankan" tanpa tanggal (seharusnya WAJIB, UMK 18 Okt 2026), versi Telegram menyebut Permenkes 1096/2011 (sudah dicabut Permenkes 2/2023) dan mengira ayam tidak bisa Self Declare. SESUDAH 8,0: 74 °C ditegaskan dengan alasan, 63 °C dijelaskan hanya untuk ikan/telur langsung saji/sapi utuh; 2 jam/1 jam >32 °C, pendinginan 21 °C/2 jam lalu 5 °C/4 jam, telur balado 71 °C, santan = kelapa bukan susu (ditulis terpisah), halal WAJIB dengan tenggat 18 Okt 2026 "6 hari lagi" (benar: 12 Okt -> 18 Okt), SLHS/PIRT/NIB, tanpa termometer ditulis jujur lalu cek visual; paket utuh di chat (tanpa file). Kekurangan: tidak ada bagian "daftar alergen untuk label" tersendiri dan tidak ada kalimat label siap tempel (alergen hanya di peta risiko, tanpa daftar BPOM utuh/kacang/kedelai kecuali kecap); jam buka diisi placeholder yang tidak relevan untuk katering.

Perbandingan lengkap dengan hasil SEBELUM: `00-openclaw-sebelum-sesudah.md`.
