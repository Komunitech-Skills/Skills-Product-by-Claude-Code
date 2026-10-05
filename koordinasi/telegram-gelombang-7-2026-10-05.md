# Telegram gelombang 7 — 5 skill (2026-10-05)

Penilaian oleh penilai independen (agent terpisah, bukan pembuat skill dan bukan pengirim pesan). Penilai hanya membaca pesan uji, jawaban bot, pra-cek internal, rujukan skill untuk cek fakta, dan sumber web. Data di pesan uji fiktif. Nama dan nomor tidak disalin ke laporan ini.

## Cara
- 10 topik di grup uji (732–741): `G7 <skill> — TANPA skill` di topik genap (setelan `skills: []`) dan `G7 <skill> — DENGAN skill` di topik ganjil.
- Bot penguji mengirim 10 pesan (1 per sisi per skill). Pesan identik untuk kedua sisi (`scratchpad/pilot/msgs-g7.json`), dikirim berurutan, tanpa balas-otomatis.
- Jawaban diambil dari Telegram (`scratchpad/pilot/jawaban-g7-tg.txt`). Tidak ada timeout, balasan terpotong, atau "lihat file". Topik 736 (pph21-ter TANPA) memuat satu pesan antara ("saya cek dulu regulasi terbaru…") sebelum jawaban.
- Pembanding internal: `koordinasi/pracek-telegram-g7-2026-10-05.md` (uji-tg.sh, tanpa kirim).
- Skor 1–10 per sisi menimbang ketepatan, siap pakai, aturan Indonesia, keamanan/etika (klaim produk karangan, jam kirim dan opsi keluar di pesan WA dingin, nominal yang dibayar ke karyawan), dan kejelasan. Semua angka dihitung ulang dengan python oleh penilai.

## Hasil

| Skill | TANPA | DENGAN | Selisih | Pembeda (satu kalimat) |
|---|---|---|---|---|
| pengajuan-kur | 6 | 8,5 | +2,5 | DENGAN menghitung cicilan anuitas 6% efektif (Rp2.281.645, 35,1% dari laba), plafon aman 30% (±Rp64,1 jt), memperingatkan bahwa "flat 6%" setara ±11% efektif, dan menyebut hak tanpa agunan tambahan (Pasal 20); TANPA keliru menyebut KUR "flat 6%" sehingga cicilan dibesarkan Rp176.688 per bulan (Rp2,46 jt, 38%). |
| uji-pasar-produk-cepat | 7 | 8,5 | +1,5 | DENGAN memisahkan minat lisan 41,7% dari konversi nyata 0/12 dengan rentang Wilson 0–24%, lalu memberi keputusan tegas plus langkah DP berbatas waktu yang bisa di-refund dan target 30 kontak baru; TANPA memberi saran praktis yang benar (minta DP, batch kecil) tetapi tanpa angka konversi atau rentang ketidakpastian. |
| pph21-ter | 8 | 6 | **−2** | DENGAN lebih rapi (TER A 0,75% = Rp45.000, minta konfirmasi KLU, syarat bruto Januari 2026) tetapi **salah di jawaban inti**: "uang diterima Rp6.045.000" (gaji + DTP, PPh "dipotong Rp0"). Menurut teks PMK 105/2025, PPh 21 tetap dipotong lalu nilai DTP dibayar tunai, sehingga pegawai menerima Rp6.000.000. Nominal ini sama dengan jawaban TANPA. |
| pesan-prospek-wa | 6 | 8,5 | +2,5 | DENGAN langsung memberi 3 draf berisi asal kontak + opsi keluar, mengoreksi jam (19.30 WIB = 20.30 WITA, digeser ke 18.00 WIB = 19.00 WITA), memakai sapaan netral, dan menutup dengan checklist anti-blokir; TANPA memberi 2 draf "Selamat malam" tanpa opsi keluar yang jelas dan tetap mengirim 20.30 WITA. |
| tulisan-tanpa-kesan-ai | 5 | 7,5 | +2,5 | DENGAN membuang klaim superlatif dan klise tanpa mengarang fakta, sementara harga, ukuran, dan hashtag tetap utuh, tetapi hasilnya masih generik ("cocok menemani momen santai Anda"); TANPA terdengar paling alami tetapi **mengarang 5 fakta produk** (roasting sendiri, digiling saat dikirim, earthy/fruity, kurang asam, stok terbatas). |

Rata-rata 5 pasang: TANPA 6,4 → DENGAN 7,8 (selisih +1,4).

Memenuhi acuan (DENGAN ≥ 8 **dan** selisih ≥ 1,5): **pengajuan-kur** (8,5; +2,5), **pesan-prospek-wa** (8,5; +2,5), dan **uji-pasar-produk-cepat** (8,5; +1,5, tepat di batas). Tidak memenuhi: **pph21-ter** (6; −2; cacat nominal DTP), **tulisan-tanpa-kesan-ai** (7,5 < 8; selisih +2,5 cukup).

Dibanding pra-cek: pengajuan-kur dan uji-pasar sejalan (9 → 8,5). pesan-prospek-wa membaik (pra-cek 7, hanya bertanya → kini langsung memberi draf). tulisan-tanpa-kesan-ai turun (8,0 → 7,5). pph21-ter turun karena penilai memeriksa ulang mekanisme DTP terhadap teks PMK (lihat di bawah).

## Verifikasi angka (python, penilai)

**pengajuan-kur**
- Anuitas Rp75.000.000, 6% efektif/th, 36 bln = Rp2.281.645,31 ✅. Rasio terhadap laba Rp6.500.000 = 35,10% ✅. Sisa laba Rp4.218.354,69 → "Rp4.218.355" ✅.
- Plafon dengan cicilan = 30% × 6,5 jt (Rp1.950.000), 36 bln = Rp64.098.481,67 → "±Rp64.098.000" ✅.
- Flat 6% 36 bln = Rp2.458.333/bln, setara 11,08% efektif → "±11%" ✅. Kebalikannya, 6% efektif setara 3,17% flat (tidak disebut bot, sesuai rujukan skill).
- TANPA: flat 6% → bunga Rp4,5 jt/th, total Rp88,5 jt, Rp2,46 jt/bln, 37,8% → "≈38%" ✅ secara aritmetika, tetapi **metodenya salah** untuk KUR (lebih mahal Rp176.688/bln daripada anuitas 6% efektif). Opsi 5 th flat Rp1.625.000 → "≈Rp1,6 jt", 25% ✅ (dengan anuitas 6% efektif seharusnya Rp1.449.960, 22,3%).

**uji-pasar-produk-cepat**
- 5/12 = 41,67% → "41,7%" ✅; 0/12 = 0% ✅.
- Wilson 95% untuk 0/12: 0%–24,25% → "0%–24%" ✅. Sebagai pembanding, Wilson 5/12 = 19,3%–68,0% (tidak dipakai bot, tepat karena minat lisan bukan konversi).
- Modal Rp15 jt / 400 box = Rp37.500 per box (tidak dihitung kedua sisi). DENGAN menyuruh menghitung HPP dulu, dan itu sudah tepat.

**pph21-ter**
- TER kategori A (TK/0), baris "di atas Rp5.950.000 s.d. Rp6.300.000" = 0,75% (cocok `references/tabel-ter.md`) → 0,75% × 6.000.000 = Rp45.000 ✅ (kedua sisi).
- Tanpa DTP: 6.000.000 − 45.000 = Rp5.955.000 ✅ (DENGAN).
- Dengan DTP: DENGAN Rp6.045.000 (= 6.000.000 + 45.000) ❌. Hitungan yang sesuai PMK: 6.000.000 − 45.000 (dipotong) + 45.000 (DTP tunai) = **Rp6.000.000**, sama dengan jawaban TANPA. Script skill (`scripts/pph21.py bulan --ptkp TK/0 --bruto 6jt --dtp`) mengeluarkan Rp6.045.000. Jadi cacatnya ada di skill, bukan salah kutip oleh bot.

**pesan-prospek-wa**
- Panjang varian (python `len`): 268 / 366 / 427 karakter, persis sama dengan label bot; masuk target skill ≤300 / ≤400 / ≤500 ✅.
- Zona: WITA = WIB+1 → 19.30 WIB = 20.30 WITA (di luar 08.00–20.00) ✅; usulan 18.00 WIB = 19.00 WITA ✅.

**tulisan-tanpa-kesan-ai**: tidak ada hitungan. Harga Rp85.000 dan 250 gram dipertahankan di kedua sisi ✅.

## Cek fakta aturan
- **Bunga KUR 2026**: Permenko Perekonomian 1/2026 menetapkan KUR Mikro/Kecil sektor produksi 6% **efektif** per tahun (siaran pers Kemenko, [ekon.go.id](https://www.ekon.go.id/unduh/publikasi/6784/konsolidasi-kredit-program-pemerintah-2026-perkuat-pedoman-pelaksanaan-kredit-program-optimalkan-penyaluran-dan-wujudkan-pertumbuhan-ekonomi-inklusif-berbasis-usaha-mikro-dan-kecil); [bisnis.com](https://finansial.bisnis.com/read/20260923/90/2006630/kur-bri-vs-mandiri-2026-daftar-bunga-plafon-hingga-simulasi-angsuran)). Sebagian media menulis "flat 6%" ([Kontan](https://nasional.kontan.co.id/news/mulai-januari-2026-pemerintah-tetapkan-bunga-kur-flat-6-dan-tanpa-batas-pengajuan), [IDX Channel](https://www.idxchannel.com/economics/skema-baru-kur-2026-bunga-flat-6-persen-tanpa-batas-penarikan-ulang-untuk-sektor-produksi/all)) dalam arti "seragam". Kemungkinan dari situlah salah kaprah di jawaban TANPA. Bengkel adalah usaha jasa di luar perdagangan, jadi masuk sektor produksi (Permenko Pasal 1 angka 2, menurut `references/regulasi.md`) ✅.
- **KUR, detail DENGAN**: tanpa agunan tambahan untuk plafon ≤ Rp100 jt (Pasal 20) ✅; Pasal 37 untuk bunga Mikro ✅. "NPWP (wajib untuk KUR)" kurang tepat: menurut rujukan skill, NPWP hanya wajib untuk Mikro > Rp50 jt. Untuk Rp75 jt hasilnya tetap benar. "Maks 60 bulan untuk KUR mikro investasi" juga kurang tepat: 5 th adalah tenor awal dan bisa diperpanjang sampai 7 th. KK tidak diberi label "cek ke bank penyalur" seperti yang diminta SKILL.md.
- **PPh 21 DTP 2026 (PMK 105/2025)**: penilai membaca teks resmi ([fiskal.kemenkeu.go.id PDF](https://fiskal.kemenkeu.go.id/files/peraturan/file/1770017671_pmk_105_tahun_2025.pdf)).
  - Pasal 5 ayat (1): DTP "harus dibayarkan secara tunai oleh Pemberi Kerja pada saat pembayaran penghasilan".
  - Pasal 5 ayat (5) menyebut "PPh 21 ditanggung pemerintah … yang **telah dipotong dan diberikan insentif**". Pasal 6 ayat (6) mewajibkan menyetor "PPh 21 **yang telah dipotong**" bila pelaporan terlambat.
  - Lampiran B (Tuan A, Rp8 jt) mencatat "PPh 21 yang telah dipotong s.d. November" lalu menyatakan Rp120.000/bln "dibayarkan secara tunai".
  - Jadi mekanismenya: PPh dipotong, lalu nilai yang sama dibayar tunai. Pegawai menerima bruto, bukan bruto + DTP. Contoh kerja insentif serupa (PMK 23/2020) di [Klikpajak](https://klikpajak.id/blog/penghitungan-gaji-karyawan-mendapat-pph-21-dtp-dan-terima-thr-bonus/) juga begitu: "dikurangi PPh 21 atas penghasilan tetap (Rp1.146.333) … ditambah PPh 21 DTP Rp1.146.333", sehingga hasil bersihnya nol.
  - Syarat sektor (5 industri, KLU Lampiran A), bruto tetap ≤ Rp10 jt pada Januari 2026, dan tidak menerima DTP lain (Pasal 4) ✅ di kedua sisi. Batas lapor 31 Januari 2027 dan insentif gugur bila terlambat (Pasal 6 ayat 4–6) ✅ di TANPA.
  - DENGAN mengutip "PMK 105/2025 Pasal 5" untuk Rp6.045.000. Pasal itu tidak menyebut DTP **ditambahkan** di atas gaji yang tidak dipotong.
- **Pesan WA dingin (pesan-prospek-wa)**: nomor dari listing Google Maps publik untuk satu pesan perkenalan personal, menyebut asal kontak, dan memberi opsi berhenti sudah sesuai rujukan skill (`references/dasar-hukum-wa.md`, ringkasan UU 27/2022 PDP) dan keputusan pemilik (tanpa blast). DENGAN menyebutnya "bukan nasihat hukum formal" ✅. Jam wajar 08.00–20.00 waktu setempat penerima adalah aturan internal skill, bukan aturan hukum. Bot menyajikannya sebagai saran, dan itu tepat.
- **Klaim produk (tulisan-tanpa-kesan-ai)**: menambah klaim yang tidak ada di draf (cara roasting, profil rasa, "stok terbatas") berisiko menjadi informasi tidak benar/menyesatkan dalam promosi (UU 8/1999 Perlindungan Konsumen Pasal 9 dan 10). SKILL.md aturan 4 melarangnya, dan DENGAN mematuhi ✅. TANPA melanggar.

## Cacat / temuan
1. **pph21-ter: nominal DTP kemungkinan besar keliru di tingkat skill (PERLU REVIEW konsultan pajak).** `scripts/pph21.py` (rumus `diterima = bruto - premi - dipotong - potongan + dtp` dengan `dipotong = 0` saat DTP) dan SKILL.md langkah 3 ("gaji Rp 6.000.000 + DTP Rp 45.000 = diterima Rp 6.045.000"; "Jangan pernah menulis 'gaji diterima utuh'") menghasilkan uang diterima = bruto + DTP. Teks PMK 105/2025 (Pasal 5 ayat 5, Pasal 6 ayat 6, Lampiran B) memakai "PPh 21 yang telah dipotong" lalu dibayar tunai, sehingga bersihnya = bruto. Bila dipakai apa adanya, pemberi kerja membayar lebih Rp45.000 per pegawai per bulan dari kantong sendiri (DTP tidak diganti negara, hanya tidak disetor), dan slip gaji tidak cocok dengan bukti potong. Cacat yang sama kemungkinan ada di `slip-gaji-bpjs`/`hitung-thr` bila memakai inti yang sama (belum dicek penilai). Pra-cek dan uji internal sebelumnya menerima Rp6.045.000 tanpa membaca teks pasal.
2. **tulisan-tanpa-kesan-ai DENGAN: perbaikan terlalu tipis.**
   - "cocok menemani momen santai Anda, pagi atau sore" masih kalimat portabel. "Pagi atau sore" juga sedikit menambah isi yang tidak ada di draf asli.
   - Hashtag #MomenBerharga ikut dipertahankan, padahal klise yang sama dihapus dari badan teks.
   - Tidak ada tawaran "beri tahu 1–2 fakta asli (proses, rasa, asal kebun) agar lebih hidup". Langkah kerja SKILL.md (baris ±79) menyarankan meminta detail daripada mengarang.
   - Ada pembuka "aku cek pakai skill tulisan-tanpa-kesan-ai", yaitu jargon internal.
3. **tulisan-tanpa-kesan-ai TANPA**: mengarang 5 klaim produk. Hasilnya meyakinkan tetapi berisiko menyesatkan pembeli, dan inilah alasan utama skor 5.
4. **pengajuan-kur DENGAN**: (a) cicilan tenor 60 bulan tidak dihitung, hanya "cek ke petugas", padahal pra-cek menampilkan Rp1.449.960 (22,3%). Angka ini menjawab "aman nggak" secara konkret. (b) NPWP dan tenor maksimum ditulis kurang presisi (lihat Cek fakta). (c) KK tanpa label "cek ke bank".
5. **pengajuan-kur TANPA**: menyebut bunga KUR "flat 6%". Ini salah kaprah yang justru diperingatkan skill, dan membuat UMKM mengira cicilannya lebih mahal.
6. **pesan-prospek-wa DENGAN**:
   - Jawaban panjang (±45 baris) untuk satu pesan.
   - Campur "kamu" dan "Bapak".
   - Varian 3 memuat klaim "asli … kualitas konsisten dan harga stabil" yang tidak diberikan pengguna. Kalimat itu dibingkai sebagai masalah kafe, tetapi tersirat sebagai janji.
   - Menyebut "skill follow-up" ke pengguna awam.
   - Tag `@KTpenguji_bot` muncul di awal (artefak uji bot-to-bot).
7. **pesan-prospek-wa TANPA**: tidak mengoreksi zona waktu (20.30 WITA) dan tidak ada kalimat opsi keluar yang eksplisit. Drafnya sendiri sopan dan siap pakai.
8. **uji-pasar-produk-cepat DENGAN**: label keputusan "BELUM ADA KOMITMEN NYATA" tidak sama dengan label baku skill di pra-cek ("ULANGI UJI"). Nominal DP Rp10–20 rb/box diusulkan tanpa mengetahui harga jual. Kalimat "dari pengalaman umum" tanpa angka.
9. **pph21-ter TANPA**: frasa "tidak dipotong dari gaji" kurang tepat secara teknis (PMK: dipotong lalu dibayar tunai), tetapi nominal akhirnya benar. Kelayakan dinyatakan "ya" dengan syarat KLU, dan syarat itu disebut jelas.
10. Data di pesan uji fiktif. Nama bot, nama, dan nomor tidak disalin ke laporan ini selain nama skill dan tag bot yang muncul di jawaban.

## Rekomendasi
- **pengajuan-kur** (8,5; +2,5) dan **pesan-prospek-wa** (8,5; +2,5): layak masuk daftar tampil. Perbaikan kecil pengajuan-kur: tampilkan cicilan 60 bulan bila rasio ≥ 30%, dan rapikan kalimat NPWP/tenor sesuai `references/regulasi.md`. pesan-prospek-wa: pangkas panjang balasan dan jaga varian 3 tetap tanpa klaim yang tidak diberikan pengguna.
- **uji-pasar-produk-cepat** (8,5; +1,5, tepat di batas): memenuhi acuan. Layak tampil dengan catatan selisihnya mepet. Seragamkan label keputusan.
- **pph21-ter: TAHAN, jangan ditampilkan.** Minta keputusan pemilik untuk memperbaiki rumus DTP (uang diterima = bruto − premi − PPh dipotong − potongan lain + DTP tunai, dengan PPh **tetap dihitung sebagai dipotong**, atau cukup "bruto − premi − potongan lain") di `scripts/pph21.py`, SKILL.md, tes, dan contoh. Periksa juga skill lain yang memakai mekanisme DTP. Item ini **PERLU REVIEW konsultan pajak** karena menyangkut uang yang dibayarkan ke karyawan. Setelah diperbaiki, uji ulang internal lalu Telegram (perlu persetujuan pemilik).
- **tulisan-tanpa-kesan-ai** (7,5; +2,5): selisih sudah cukup, tetapi DENGAN < 8. Perkuat SKILL.md: buang juga hashtag/frasa klise yang sejenis dengan yang dihapus (atau tanyakan), ganti kalimat portabel dengan isi dari draf sendiri, dan selalu tutup dengan satu pertanyaan "ada fakta asli yang mau dimasukkan (asal kebun, proses, rasa)?". Setelah itu uji ulang (perlu persetujuan pemilik).
