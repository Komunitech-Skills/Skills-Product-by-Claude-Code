# Gelombang Telegram 17 — 2026-10-14 (bot kedua)

Keputusan otomatis **72** (2026-10-14). Bot uji kedua `@KTclaude2bot` (OpenClaw 2026.10.2, model claude-sonnet-5), grup uji internal Komunitech, topik 1441–1446 (satu topik per sisi: ganjil = TANPA, topik dengan `skills: []`; genap = DENGAN). Pesan: `alat-uji/pilot/msgs-g17.json` (pesan identik di kedua sisi; skenario normal utama uji internal, data fiktif); topik: `topik-g17.json`; balasan: `pilot/updates-g2.jsonl` (getUpdates, thread 1441–1446, balasan terpecah digabung berurutan); id kirim: `pilot/sent-g2.jsonl`. 6 pesan terkirim, semua dibalas. Pesan ke topik 1446 gagal pada kiriman pertama (URLError 06:51 UTC, tidak sampai ke grup) lalu dikirim ulang 06:59 UTC; yang dinilai adalah balasan kiriman ulang itu. SKILL.md di home bot identik dengan repo: bandingkan-pemasok-vendor 1.0.2, rencana-restok-barang 1.0.2, panduan-wawancara-kerja 1.0.1. Penilai: agent penilai independen (bukan pembuat), memakai bagian "Penilaian" di `alat-uji/brief/tester-umum.md`. Tanggal dicek dengan python: 17 Agu dan 5 Okt 2026 jatuh pada Senin, 14 Okt 2026 pada Rabu.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| bandingkan-pemasok-vendor (1.0.2) | 6,5 | 8 | +1,5 | **LOLOS** (tepat di ambang) | Kedua sisi memilih Sentosa dengan total yang benar. Hanya DENGAN yang menandai status PPN Sentosa belum jelas (bila kena PPN totalnya Rp7.576.860, hanya Rp48.840 lebih murah daripada Mitra), memasukkan PPN atas ongkir Mitra, dan memberi pesan WA klarifikasi siap kirim; semuanya muat dalam satu pesan. |
| rencana-restok-barang (1.0.2) | 7 | 8 | +1,0 | **BELUM** | DENGAN memberi jumlah pesan pasti dengan stok pengaman (beras 47 karung, minyak 82 botol, gula 75 kg), tanggal habis, dan batas pesan telur/mie. TANPA sudah benar menghitung sisa hari, menandai beras darurat, dan mengurutkan prioritas, hanya jumlahnya berupa kisaran. |
| panduan-wawancara-kerja (1.0.1) | 6 | 8,5 | +2,5 | **LOLOS** | Sejak kalimat pertama DENGAN menyatakan syarat iklan "wanita, maks. 28 tahun, berpenampilan menarik" tidak boleh dipakai, lalu memberi paket berbobot lengkap (ciri jawaban kuat/lemah, tes berkunci, rubrik berjangkar, kartu skor, daftar "jangan ditanyakan → ganti dengan"). TANPA tidak menyinggung syarat itu, tetap mencantumkan "status" di data dasar, dan memberi skor pada kesediaan lembur. |

Pembanding uji internal (`examples/HASIL-UJI.md`):
- Pemasok, skenario 1T (pesan sama, konteks Telegram lokal): 6,5 → 8,5.
- Restok, skenario 2 (pesan sama): 6,5 → 9.
- Wawancara, skenario 1T (pesan sama): 5,5 → 8,0.

Di bot asli, wawancara justru lebih baik daripada uji lokal. Untuk pemasok dan restok, selisihnya menyempit karena dua hal:
- jawaban TANPA di bot setara atau sedikit lebih baik daripada jawaban TANPA lokal;
- jawaban DENGAN di bot lebih ringkas daripada versi lokal. Di restok, daftar pesanan dan draf WA hilang.

## Kutipan balasan (dipendekkan, `…` = dipotong)

### bandingkan-pemasok-vendor

TANPA (topik 1441, 1.540 karakter, 1 pesan):
> 1. Toko Tepung Sentosa … • Diskon 5% → 6.726.000 • + Ongkir 100rb = Rp 6.826.000
> 2. PT Mitra Pangan Jaya • 600 x 11.200 = 6.720.000 • + PPN 11% = 739.200 → 7.459.200 • + Ongkir 150rb = Rp 7.609.200
> 3. CV Berkah Gandum … • Kirim 5-7 hari ⚠️ ini masalah — deadline ibu 5 hari, estimasi mereka bisa molor sampai hari ke-7
> Kesimpulan:
> Kalau murni soal harga + aman waktu: Toko Tepung Sentosa paling untung, total termurah (Rp6.826.000) dan kirimnya pasti 2-3 hari …
> Mitra Pangan Jaya jadi pilihan kedua kalau ibu lagi butuh modal kerja — … meski lebih mahal ~Rp783rb dibanding Sentosa.
> CV Berkah Gandum saya skip duluan — … estimasi kirim 5-7 hari itu terlalu berisiko, apalagi harus transfer full dulu …

DENGAN (topik 1442, 2.644 karakter, 1 pesan setelah pesan "Working"):
> • Toko Tepung Sentosa — Total Rp6.826.000 (Rp11.377/kg) — termurah sementara — kirim 3 hari — bayar tunai saat terima — skor 86,5 (peringkat 1)
> • PT Mitra Pangan Jaya — Total Rp7.625.700 (Rp12.710/kg) — lebih mahal Rp799.700 (11,7%) — kirim 4 hari — tempo 30 hari — skor 85,8 (peringkat 2)
> • CV Berkah Gandum — Total Rp7.140.000 (Rp11.900/kg) — lebih mahal Rp314.000 (4,6%) — kirim 7 hari (melewati tenggat 5 hari) — bayar penuh di muka — skor 63,0 (peringkat 3)
> Rekomendasi: Toko Tepung Sentosa (skor 86,5, hampir seri dengan PT Mitra Pangan Jaya, beda 0,7 poin)
> • Bila ternyata Toko Tepung Sentosa itu PKP dan harga belum termasuk PPN: totalnya naik jadi Rp7.576.860, dan hanya lebih MURAH Rp48.840 daripada PT Mitra Pangan Jaya — rekomendasi berubah ke PT Mitra Pangan Jaya …
> Pesan WA (siap kirim ke Toko Tepung Sentosa): "Siang Pak/Bu 🙏 mau konfirmasi untuk pesanan 60 dus (600 kg) terigu protein sedang: toko sudah PKP atau belum, dan harga Rp118rb/dus itu sudah termasuk PPN atau belum ya? …"
> Data yang belum ada: [isian: status PKP & apakah harga Rp118rb/dus sudah termasuk PPN dari Toko Tepung Sentosa]
> 2. Mau pesan WA di atas langsung saya siapkan versi kirimnya, atau ada yang mau diubah?

### rencana-restok-barang

TANPA (topik 1443, 1.583 karakter, 1 pesan):
> Beras 5kg — rata-rata 22 karung/minggu (~3,1/hari) … Stok 9 karung cuma cukup ~2,9 hari. … BERAS BISA HABIS SEBELUM BARANG DATANG …
> → Pesan hari ini juga. Untuk cukup 2 minggu: pesan ±38-40 karung.
> Minyak Goreng 2L — ini trennya naik terus: 30 → 45 dalam 8 minggu … Stok 25 cuma cukup ~4,1 hari …
> → Pesan besok paling lambat. Untuk 2 minggu (dengan tren naik): pesan ±65-70 botol.
> Gula Pasir 1kg — … rata-rata 39,75/minggu (~5,7/hari) … Stok 30 cukup ~5,3 hari …
> → Pesan dalam 1-2 hari, tidak darurat. Untuk 2 minggu: pesan ±50 kg.
> … Perkiraan kebutuhan 2 minggu: telur ±110-115 kg, mie ±15-16 dus …
> Ringkas urutan prioritas pesan: beras (darurat) → minyak (besok) → gula (santai) → cek stok telur/mie dulu baru putuskan.

DENGAN (topik 1444, 1.377 karakter, 1 pesan setelah pesan "Working"):
> ⚠️ AKAN KOSONG DULUAN
> Beras 5 kg habis ±2 hari lagi, padahal kiriman grosir butuh 2-3 hari → berisiko kosong ±1 hari. Pilihan: pesan HARI INI, atau minta grosir percepat/ambil sebagian dulu dari toko terdekat.
> PESAN SEKARANG
> • Beras 5 kg: stok 9, laku ±3,14 karung/hari (stabil), habis ±2 hari (16 Okt) → pesan 47 karung
> • Minyak Goreng 2 L: stok 25, laku ±5,89/hari (naik 27%), habis ±4 hari (18 Okt) → pesan 82 botol
> PESAN MINGGU DEPAN
> • Gula Pasir 1 kg: stok 30, laku ±5,68/hari (stabil), habis ±5 hari → pesan sekitar 15 Okt, jumlah 75 kg
> BELUM BISA DIHITUNG (stok belum diketahui)
> • Telur: laku ±7,95 kg/hari (stabil) → pesan ulang kalau stok tinggal ≤28 kg
> • Mie Instan: laku ±1,07 dus/hari (naik 25%) → pesan ulang kalau stok tinggal ≤5 dus
> Catatan: saya pakai lead time 3 hari (sesuai info "2-3 hari" dari grosir), tingkat layanan 95%, dan stok target untuk cukup 14 hari ke depan setelah barang datang. …

### panduan-wawancara-kerja

TANPA (topik 1445, 3.365 karakter, 1 pesan setelah pesan "Working"):
> ⏱️ Breakdown 40 menit/orang
> • 0-5 menit: Perkenalan santai + konfirmasi data dasar (domisili Bekasi Timur, status, bisa kerja Senin-Sabtu 08.00-16.00, siap lembur pas tanggal kembar)
> …
> 🧪 Tes Praktik Singkat (pilih 2, @7-8 menit)
> 1. Simulasi chat CS - kasih HP/laptop, suruh balas 3 chat dummy: nanya stok, komplain paket telat, nego harga. …
> 2. Mini tes Excel/Sheet - kasih data dummy ~15 baris order …
> 📊 Rubrik Penilaian (skala 1-5, biar gampang dibandingin ke-4 kandidat)
> … • Kecocokan jam kerja & lokasi (Bekasi Timur, siap lembur campaign)
> Total skor max 30 → gampang buat ranking 4 kandidat setelah semua kelar diwawancara.

DENGAN (topik 1446, 9.501 karakter, 4 pesan: 3.818 + 150 + 3.763 + 1.770, setelah pesan "Working"):
> Satu hal dulu: di iklannya ada syarat "wanita, maks. 28 tahun, berpenampilan menarik" — ini termasuk syarat yang tidak boleh dipakai untuk menyaring pelamar … Jadi saya tidak masukkan ke kriteria wawancara, diganti jadi penilaian kemampuan kerja.
> 1. Ketelitian proses pesanan & pencatatan (30%, kritis) — …
> Situasional: "Pesanan masuk Kerudung Segi Empat Motif 3 pcs, stok catatan tinggal 2, sistem sudah bisa cetak resi otomatis. Apa yang Anda lakukan?"
> — Kuat: menahan dulu, cek stok fisik, hubungi pembeli … Lemah: tetap cetak & kirim meski stok kurang.
> Kunci: pesanan 1 & 5 aman dicetak; 2, 3, 4 wajib dicek dulu sebelum resi dicetak.
> K1 — 1: sering salah cetak resi/tidak cek stok. … 5: seperti 4 + punya cara sistematis sendiri yang terbukti menekan kesalahan.
> • Ketersediaan kerja (ya/tidak, TIDAK dinilai skor): bersedia jam kerja Senin-Sabtu 08.00-16.00? …
> • Usia pasti/tanggal lahir → cukup pastikan usia kerja minimal 18 tahun; sisanya nilai dari kompetensi.
> • Status menikah/rencana menikah, anak/rencana hamil → "Jam kerja Senin-Sabtu 08.00-16.00, kadang lembur saat campaign tanggal kembar — apakah bisa Anda penuhi?"

## Verifikasi angka

**bandingkan-pemasok-vendor.** Script dijalankan dengan data pesan uji (`--barang "tepung terigu protein sedang"`, 600 kg, tenggat 5 hari), lalu angka kunci dihitung ulang sendiri dengan Decimal (PPN 11% dibulatkan ke bawah):

| Pemasok | Hitung ulang | DENGAN | TANPA |
|---|---|---|---|
| Sentosa | 60 dus × 118.000 × 0,95 = 6.726.000 + 100.000 = **6.826.000** (11.377/kg) | sama | sama |
| Mitra | 6.720.000 + 150.000 = DPP 6.870.000; PPN 755.700 → **7.625.700** (12.710/kg) | sama | 7.609.200 (12.682/kg): PPN hanya atas barang, PPN ongkir Rp16.500 tidak dihitung |
| Berkah | 600 × 11.900 = **7.140.000** | sama | sama |
| Selisih | Mitra − Sentosa 799.700 (11,72%); Berkah − Sentosa 314.000 (4,60%) | sama (11,7%; 4,6%) | 783.200 ("~Rp783rb", konsisten dengan totalnya) |
| Sentosa bila PKP & belum PPN | 6.826.000 × 1,11 = 7.576.860; masih 48.840 lebih murah daripada Mitra | sama | tidak dibahas |

Skor 86,5 / 85,8 / 63,0, "telat 7 hari → tiba hari ke-10", dan 2× = Rp13.552.000 cocok dengan keluaran script. **Tidak ada kesalahan angka di kedua sisi.** Selisih Rp16.500 di sisi TANPA adalah asumsi yang berbeda (PPN atas ongkir yang ditagih pemasok PKP). Asumsi skill memang lebih tepat, tetapi masih bertanda PERLU REVIEW konsultan pajak.

**rencana-restok-barang.** Script dijalankan dengan data mingguan yang sama (`--data-per minggu --lead-time 3 --hari-ini 2026-10-14`, stok beras 9 / minyak 25 / gula 30). Lalu dihitung ulang sendiri dengan Decimal: rata-rata = total ÷ 56 hari; tren = 4 minggu terakhir ÷ 4 minggu sebelumnya; simpangan harian = simpangan mingguan ÷ √7; stok pengaman = 1,65 × simpangan × √3; target = laju × 17 + stok pengaman.

| Barang | Laju dipakai | Stok pengaman | Titik pesan | Target | Habis | Pesan | DENGAN |
|---|---|---|---|---|---|---|---|
| Beras | 3,1429 (stabil +9,5%) | 2,16 | 11,59 → 12 | 55,59 → 56 | 2,86 → 2 hari (16 Okt); kosong ±1 hari | 47 | sama |
| Minyak | 5,8929 (naik +26,9%) | 6,34 | 24,02 → 25 | 106,52 → 107 | 4,24 → 4 hari (18 Okt) | 82 | sama |
| Gula | 5,6786 (stabil +1,3%) | 1,80 | 18,84 → 19 | 98,34 → 99 | 5,28 → 5 hari | titik pesan tercapai +1 hari (15 Okt) → 75 | sama |
| Telur | 7,9464 (stabil +7,0%) | 3,78 | 27,62 → 28 | 138,87 → 139 | stok belum ada | 139 − stok | batas 28 sama; "139 − stok" tidak ditulis |
| Mie | 1,0714 (naik +25%) | 1,54 | 4,75 → 5 | 19,75 → 20 | stok belum ada | 20 − stok | batas 5 sama; "20 − stok" tidak ditulis |

Sisi TANPA juga benar: beras 22/minggu dan 2,9 hari; minyak 42,3/minggu dan 4,1 hari; gula 39,75/minggu dan 5,3 hari; telur 55,6/minggu; jumlah 2 minggu dikurangi stok (44 − 9; 79,5 − 30 ≈ 50); kebutuhan 2 minggu telur 111 kg. **Tidak ada kesalahan angka di kedua sisi.** Jumlah pesan TANPA berupa kisaran untuk "cukup 2 minggu sejak hari ini", tanpa memperhitungkan lama kirim dan stok pengaman.

**panduan-wawancara-kerja.** Hasil `skor_wawancara.py --alur 40 --kompetensi 5 --tes 15` = 4/15/3×5/4/2 menit, total 40, sama persis dengan DENGAN. Hal lain yang dicek:
- bobot 30+25+20+15+10 = 100, dengan 2 kompetensi kritis;
- kunci tes benar: pesanan 2 stoknya 2 < 3, pesanan 3 alamatnya tidak lengkap, pesanan 4 terindikasi duplikat;
- situasional K5 benar: 42 resi − 40 catatan = 2 pesanan;
- usia kerja minimal 18 tahun benar.

Di TANPA, 4 × 40 menit = 2 jam 40 menit, dan dengan 3 jeda 5–10 menit menjadi "sekitar 3 jam", juga benar.

## Alasan skor & cacat

- **bandingkan-pemasok-vendor**
  - **TANPA (6,5):** Total ketiga pemasok benar, tenggat dan termin dinilai dengan tepat, rekomendasi masuk akal. Hal yang tidak ada:
    - status PPN Sentosa tidak dipertanyakan;
    - PPN atas ongkir Mitra tidak dihitung;
    - tidak ada pesan WA, skenario "kalau berubah", maupun disclaimer.

    Nilainya sama dengan jawaban TANPA lokal yang hampir identik (6,5).
  - **DENGAN (8):** Semua angka sama dengan script dan hitung ulang. Jawaban ringkas, muat satu pesan (2.644 karakter; versi lokal 1.0.1 masih 4.115–4.553). Isinya lengkap:
    - "termurah sementara" karena status PPN Sentosa belum jelas, beserta hitungan alternatifnya;
    - skenario telat dan skenario 2×;
    - 2 risiko dan pesan WA klarifikasi ke Sentosa;
    - asumsi, disclaimer, dan maksimal 3 pertanyaan.

    Minus:
    1. INTI tidak disalin utuh. Baris "Asumsi pajak: ongkir PT Mitra ikut kena PPN (Rp16.500)" hilang, padahal aturan skill meminta asumsi pajak ditulis terbuka. Akibatnya pembaca tidak tahu mengapa total Mitra Rp7.625.700, bukan Rp7.609.200.
    2. Skor 86,5/85,8 dan "hampir seri" tampil tanpa penjelasan bobot. Bagi orang awam membingungkan bahwa pemasok yang Rp799.700 lebih mahal disebut hampir seri.
    3. Baris "Data yang belum ada: [isian: …]" mengulang pertanyaan 1 dan isi pesan WA. Pertanyaan 2 ("mau pesan WA di atas langsung saya siapkan versi kirimnya?") tidak berguna karena pesannya sudah siap kirim.
- **rencana-restok-barang**
  - **TANPA (7):**
    - Plus: sisa hari stok benar; beras ditandai "bisa habis sebelum barang datang"; tren minyak dan mie terbaca; waktu pesan per barang jelas (hari ini / besok / 1–2 hari); urutan prioritas ringkas; bahasa awam.
    - Minus: jumlah pesan berupa kisaran (±38–40, ±65–70, ±50) tanpa stok pengaman dan tanpa tanggal; tidak ada titik pesan ulang; tidak ada daftar pesanan atau draf WA; tidak ada disclaimer.
    - Lebih baik daripada jawaban TANPA lokal (6,5), yang memakai "buffer 30%" tanpa dasar dan kisaran yang tidak konsisten.
  - **DENGAN (8):**
    - Plus: semua angka cocok; bagian "akan kosong" ada di paling atas beserta pilihannya; tren per barang; tanggal habis; batas pesan untuk barang yang stoknya belum diketahui; 3 pertanyaan yang tepat (stok telur/mie, harga beli, grosir); disclaimer.
    - Minus:
      1. Daftar pesanan dan draf WA ke grosir tidak muncul, padahal format skill mewajibkannya dan versi lokal (skor 9) memuatnya.
      2. Judul "PESAN MINGGU DEPAN" bertentangan dengan "pesan sekitar 15 Okt", yaitu besok. Bila pembeli mengikuti judulnya, gula habis ±19 Okt sebelum kiriman datang.
      3. Untuk telur/mie hanya ada batas kapan pesan, tanpa "jumlah = 139 − stok" / "20 − stok". Ada juga istilah teknis ("lead time", "tingkat layanan 95%", "stok target"), dan rentang data tidak disebut.
- **panduan-wawancara-kerja**
  - **TANPA (6):** Alur 40 menit, 10 pertanyaan, 3 pilihan tes praktik, rubrik 6 butir, dan tips berdua cukup berguna. Kekurangannya:
    - syarat diskriminatif di iklan (jenis kelamin, usia, penampilan) tidak disinggung;
    - "status" ditanyakan di data dasar;
    - kesediaan lembur dan lokasi diberi skor;
    - tanpa ciri jawaban kuat/lemah, tanpa jangkar rubrik, dan tanpa bahan atau kunci tes (pengguna harus membuat data dummy sendiri);
    - salah ketik "doal".
  - **DENGAN (8,5):** Semua perbaikan 1.0.1 terlihat di bot asli:
    - tanpa nama skill lain ("Kalau mau, iklannya juga bisa saya bantu rapikan nanti");
    - ketersediaan kerja ya/tidak tanpa skor;
    - soal tes sama untuk 4 kandidat di hari yang sama;
    - 6 aturan pakai;
    - daftar terlarang lengkap 7 butir.

    Minus:
    1. Panjang 9.501 karakter dipecah menjadi 4 pesan, salah satunya hanya 150 karakter (satu pertanyaan situasional K4). Isi tetap utuh.
    2. Dasar aturan ditulis "UU Ketenagakerjaan, UU Cipta Kerja Pasal 5-6" dan "SE Menaker M/6/HK.04/V/2025 … berlaku per 14 Oktober 2026". Kalimat ini terbaca seolah SE berlaku mulai 14 Okt 2026, padahal maksudnya status ringkasan per tanggal itu. Pasal 5–6 adalah pasal UU 13/2003. Sudah ada catatan "nomor pasal belum dicocokkan".
    3. 3 menit per kompetensi untuk 2 pertanyaan, tanpa saran "dahulukan pertanyaan perilaku". Jadwal sehari untuk 4 pelamar juga tidak dibuat, padahal TANPA membuatnya.

## Perilaku bot asli vs uji lokal

- **Pemicu:** ketiga skill terpicu di sisi DENGAN. Gaya dan angka sama persis dengan keluaran script masing-masing. Tidak ada kata proses (skill/script/path/file) di keenam balasan. Sisi TANPA tidak menunjukkan jejak skill.
- **Panjang dan pemotongan:**
  - Pemasok 2.644 karakter, satu pesan. Perbaikan panjang di 1.0.2 terbukti di bot asli.
  - Restok 1.377 karakter, lebih pendek daripada versi lokal sehingga daftar pesanan dan draf WA hilang.
  - Wawancara 9.501 karakter dipecah otomatis menjadi 4 pesan, tidak terpotong, tetapi ada potongan 1 kalimat sebagai pesan tersendiri.
- **File:** tidak ada file atau lampiran di keenam balasan; semua isi ada di chat. TANPA wawancara menawarkan versi file tanpa mengklaim sudah melampirkan.
- **Pesan "Working":** sebelum balasan muncul satu pesan berbahasa Inggris "Working" yang mengutip pesan pengguna, di 4 dari 6 topik, termasuk TANPA wawancara. Ini perilaku platform, bukan skill. Pesannya tetap tertinggal di chat.
- **Waktu balas** (kirim → balasan terakhir): pemasok TANPA ±50 detik dan DENGAN ±95 detik; restok ±80 dan ±60 detik; wawancara TANPA ±70 detik dan DENGAN ±3 menit 25 detik.
- **Tanya di akhir:** DENGAN pemasok 3 pertanyaan, restok 3, wawancara 2; semuanya mengerjakan dulu. TANPA restok hanya meminta stok telur/mie dihitung. TANPA wawancara menawarkan versi file.

## Rekomendasi

1. **panduan-wawancara-kerja: LOLOS.** Tetap di daftar tampil `promosi/`. Bagian "Bukti uji di bot Telegram" sudah ditambahkan di README. Usulan perbaikan kecil yang tidak menunda rilis:
   - ganti kalimat dasar aturan menjadi "ringkasan aturan per 14 Oktober 2026: UU 13/2003 Pasal 5-6 …" (setahu penilai, kedua pasal ini tidak diubah UU 6/2023; tetap PERLU REVIEW);
   - tambahkan jadwal sehari bila pengguna menyebut jumlah pelamar.
2. **bandingkan-pemasok-vendor: LOLOS, tepat di ambang (+1,5).** Bila dipromosikan, sebut jujur bahwa AI biasa pun memilih pemasok yang sama. Pembedanya ada di status PPN yang belum jelas, PPN atas ongkir, dan pesan klarifikasi. Perbaikan kecil yang layak:
   - SKILL.md mewajibkan baris "Asumsi pajak" tetap ada walau ringkasan diperpendek;
   - jelaskan bobot skor dalam satu kalimat awam, atau sembunyikan angka skor bila selisih biaya besar;
   - jangan bertanya ulang hal yang sudah tercantum di "Data yang belum ada" atau di pesan WA.
3. **rencana-restok-barang: BELUM (+1,0).** Mengikuti aturan 2026-10-03 dan pola gelombang 16, skill ini tetap di bundle/`beta` karena uji internal LULUS (6,1 → 8,7), tidak dipromosikan sebagai tampilan Telegram, dan tidak diiterasi lagi kecuali pemilik meminta. Bila pemilik meminta satu revisi, tiga perbaikan paling berdampak:
   1. di kanal chat, "Daftar pesanan + draf WA" wajib tetap ada walau jawaban diringkas;
   2. ganti judul "PESAN MINGGU DEPAN" menjadi "PESAN DALAM 7 HARI" dan tulis "pesan besok (15 Okt)" bila jaraknya ≤ 2 hari;
   3. barang yang stoknya belum diketahui diberi "jumlah = target − stok sekarang", dan istilah teknis diganti ("lama kirim", "peluang tidak kehabisan").
4. Catatan platform untuk `alat-uji/README.md`: pesan "Working" dari OpenClaw muncul sebagai pesan terpisah di grup. Bila mengganggu tampilan promosi, cek apakah ada setelan status/typing di config bot uji. Perubahan config bot dilakukan dengan backup dan restart gateway sesuai aturan.
