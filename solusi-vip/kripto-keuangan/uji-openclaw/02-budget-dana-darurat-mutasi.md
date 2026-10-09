# Uji OpenClaw 02 — Budget bulanan & dana darurat dari mutasi rekening

Tanggal: 2026-10-01 (Asia/Jakarta) · Agent: OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member. SEBELUM = home `kosong-kripto-keuangan` (tanpa skill), SESUDAH = home `sol-kripto-keuangan` (6 skill paket). Kedua home dibuat ulang bersih sebelum skenario ini.

## Pesan member (identik di kedua sisi)

> kak ini mutasi rekening saya bulan september, filenya mutasi-september.csv. tolong bikinin budget bulanan yg masuk akal ya, sama dana darurat saya harusnya berapa. saya udah nikah anak 1, istri ga kerja. tabungan saya sekarang cuma 4 juta. jujur tiap akhir bulan suka mepet 😅

## Tool yang dipakai

Data: `mutasi-september.csv` fiktif identik di workspace kedua home (24 baris; gaji Rp9,5 jt, proyek Rp1,25 jt, kontrakan, cicilan motor, Shopee PayLater, 2× top-up Indodax total Rp2,5 jt, dst.; saldo berjalan dicek penguji konsisten).
- SEBELUM: `find / -iname mutasi-september.csv` (cari ke seluruh disk), lalu `read` file. Semua hitungan di kepala model.
- SESUDAH: membaca `atur-keuangan-pribadi/SKILL.md`, juga `find /` ke seluruh disk, lalu menjalankan `scripts/keuangan.py anggaran` (2×) dan `keuangan.py dana-darurat` (3×).

## SEBELUM (tanpa skill) — balasan utuh

> Udah aku bedah mutasinya kak, dan ketemu "biang keladi" kenapa tiap akhir bulan mepet 😅 — bukan cuma perasaan, emang defisit beneran.
>
> **Ringkasan September:**
> - Pemasukan: Gaji Rp9.500.000 + proyek desain Rp1.250.000 + bunga Rp8.200 = **Rp10.758.200**
> - Pengeluaran: **Rp12.468.000**
> - Selisih: **minus Rp1.709.800** (makanya saldo nyusut dari 4,15jt ke 2,44jt)
>
> **Ke mana larinya:**
> - Wajib (kontrakan 2jt, cicilan motor 1,15jt, listrik 350rb, pulsa 150rb, SPP PAUD 350rb, admin bank 12,5rb) = Rp4.012.500
> - Kirim ortu = Rp1.000.000
> - Belanja rumah tangga (Superindo+pasar+Indomaret) = Rp1.787.500
> - **Top up Indodax (crypto) = Rp2.500.000** ← ini paling gede dan jadi masalah utama
> - Shopee Paylater cicilan = Rp650.000 (utang konsumtif, hati-hati ini)
> - Topup Gopay+OVO = Rp800rb, tarik tunai ATM = Rp500rb → total Rp1,3jt ini "jajan gak jelas larinya ke mana"
> - Arisan RT 500rb, Shopee order 412rb, KFC 186rb, bensin 120rb
>
> Intinya: gaji 9,5jt itu sebenernya cukup buat hidup, tapi kebobol karena rutin nyicil ke crypto 2,5jt/bulan + cicilan paylater, padahal cashflow lagi minus dan tabungan tipis. Investasi itu bagus, tapi kalau bikin defisit dan dana darurat kosong, urutannya kebalik.
>
> **Usulan budget bulanan (dari gaji Rp9,5jt, proyek sampingan dianggap bonus):**
> - Wajib (sewa, cicilan motor, listrik, pulsa, SPP anak, admin) → Rp4.012.500 (42%)
> - Kirim ortu → Rp1.000.000 (11%)
> - Belanja rumah tangga → Rp1.800.000 (19%)
> - Jajan/makan luar + transport + arisan (digabung, dibatasi) → Rp1.000.000 (11%)
> - Lunasi Shopee Paylater → Rp650.000 (7%) — setelah lunas, stop pakai paylater lagi
> - **Tabung ke dana darurat → Rp1.000.000 (10%) minimum**
> - Crypto: **jeda dulu** sampai dana darurat aman minimal 1 bulan pengeluaran
>
> Kalau proyek sampingan dateng (kayak bulan ini 1,25jt), langsung full ke dana darurat/pelunasan paylater, jangan masuk budget harian.
>
> **Dana darurat, harusnya berapa?**
> Kamu single breadwinner + istri gak kerja + anak 1 → risikonya lebih tinggi dari orang lajang, jadi idealnya **9-12 bulan pengeluaran rutin**, bukan cuma 3-6 bulan kayak saran umum.
>
> Pengeluaran rutin (sewa+cicilan motor+listrik+pulsa+SPP+admin+kirim ortu+belanja) ≈ **Rp6.800.000/bulan**
>
> Target bertahap:
> - Milestone 1 (buffer napas): 1 bulan = **Rp6,8jt** (dari 4jt, tinggal kurang 2,8jt — ±2 bulan kalau nabung 1jt/bln + sampingan)
> - Milestone 2 (aman minimum): 6 bulan = **Rp40,8jt**
> - Target ideal: 9-12 bulan = **Rp61-82jt**
>
> Keliatan jauh, tapi dengan jeda crypto + rapihin "jajan gak jelas" tadi, kamu bisa realistis nabung 1-1,5jt/bulan dari gaji aja, belum termasuk proyek sampingan. Itu paling krusial langkah pertamanya: **stop dulu topup crypto rutin selama dana darurat < 1 bulan pengeluaran**, dan jangan nambah paylater baru.
>
> Mau aku bikinin reminder bulanan buat cek progress nabung dana darurat, atau bikinin breakdown spreadsheet-nya sekalian?

## SESUDAH (dengan paket skill) — balasan utuh

> Udah saya cek mutasi rekeningnya, dan ketemu polanya kak — bulan September itu kamu defisit **Rp1.709.800** (saldo awal Rp4.150.000 → akhir Rp2.440.200), padahal pemasukan bulan itu lagi bagus (ada proyek desain tambahan). Penyebab utamanya kelihatan jelas di mutasi: top-up ke **Indodax total Rp2.500.000** (dua kali, tgl 5 & 22) — ini pengeluaran terbesar ketiga setelah kontrakan dan cicilan motor, lebih besar dari belanja dapur sebulan.
>
> ## Ringkasan
> Dengan gaji tetap Rp9,5 juta dan pola keluarga (nikah, anak 1, istri gak kerja), pengeluaran wajib kamu memang di atas rata-rata (kontrakan + cicilan + anak sekolah), tapi defisit tiap bulan itu bukan karena kurang gaji — itu karena setoran ke kripto nggak dianggarkan, jadi "mencuri" uang yang harusnya buat dana darurat. Kalau setoran kripto itu digeser ke dana darurat dulu (bukan disuruh berhenti total ya, cuma diurutkan), bulan depan bisa langsung zero-based tanpa mepet.
>
> ## Anggaran Bulanan (zero-based, dari Gaji Rp9.500.000 saja — proyek desain gak dihitung karena gak rutin)
>
> | Pos | Kelompok | Jumlah |
> |---|---|---:|
> | Kontrakan | Wajib | Rp2.000.000 |
> | Cicilan Motor Adira | Wajib | Rp1.150.000 |
> | Cicilan Shopee Paylater (lunasi, jangan tambah) | Wajib | Rp650.000 |
> | Belanja dapur (pasar+minimarket) | Wajib | Rp1.787.500 |
> | Token Listrik | Wajib | Rp350.000 |
> | SPP PAUD Anak | Wajib | Rp350.000 |
> | Pulsa & Data | Wajib | Rp150.000 |
> | Bensin | Wajib | Rp120.000 |
> | Kiriman Ibu | Sosial | Rp1.000.000 |
> | Arisan RT | Tabungan | Rp500.000 |
> | **Dana Darurat (setoran baru)** | **Tabungan** | **Rp750.000** |
> | Jajan/hiburan/e-wallet | Keinginan | Rp692.500 |
> | **Total** | | **Rp9.500.000 (sisa Rp0)** |
>
> Catatan dari hitungan: kebutuhan kamu (Kontrakan+Cicilan+Dapur+dst) = 79,5% dari gaji — di atas pola ideal 70/10/20, tapi itu wajar untuk keluarga dengan anak dan kontrakan Rp2jt. Total cicilan (motor+paylater) = 18,9% dari gaji, masih di bawah batas aman 30%, jadi aman — asal gak nambah cicilan baru.
>
> **Soal proyek freelance & setoran Indodax:** proyek desain yang masuk bulan ini (Rp1.250.000) itu bonus tak tentu — kalau muncul lagi bulan depan, langsung masukin ke dana darurat, jangan jadi uang jajan. Setoran ke Indodax Rp2,5jt itu saya gak akan sarankan beli/jual apa-apa (di luar kapasitas saya), tapi sebagai alokasi anggaran: selama dana darurat kamu masih jauh dari aman, itu uang yang lebih mendesak dipakai buat jaring pengaman dulu — bukan dilarang trading selamanya, cuma diurutkan belakangan.
>
> ## Dana Darurat
> Status kamu "menikah + anak" → target standar **9–12 bulan** pengeluaran pokok (bukan gaji, tapi yang wajib dibayar walau penghasilan berhenti: kontrakan, cicilan, dapur, listrik, anak sekolah) ≈ Rp6.907.500/bulan.
>
> | Target | Jumlah Dibutuhkan | Kurang (dari saldo 4jt) | Lama tercapai (setoran 750rb/bln) |
> |---|---:|---:|---:|
> | 9 bulan (minimum) | Rp62.167.500 | Rp58.167.500 | ~6 tahun 6 bulan |
> | 12 bulan (ideal) | Rp82.890.000 | Rp78.890.000 | ~8 tahun 10 bulan |
>
> Progres sekarang baru ~6% dari target minimum. 6,5 tahun kedengarannya lama, tapi itu wajar kalau cuma pakai Rp750rb/bulan — makin naik gaji atau makin dikurangi pos keinginan, makin cepat.
>
> ## Asumsi yang dipakai
> - Pemasukan budget = gaji tetap Rp9,5jt saja (proyek freelance dianggap bonus, bukan pemasukan rutin).
> - Pengeluaran pokok dana darurat dihitung dari pos wajib: Rp6.907.500/bulan.
> - Saldo tabungan awal dana darurat = Rp4.000.000 (sesuai info kamu), setoran Rp750rb/bulan.
> - Pola anggaran dibandingkan dengan 70/10/20 (bukan 50/30/20 standar) karena kebutuhan keluarga dengan anak + kontrakan.
> - Shopee Paylater dianggap cicilan wajib yang harus dilunasi, bukan ditambah lagi.
>
> ## Langkah minggu ini
> 1. Set auto-debit/reminder Rp750rb ke rekening/tabungan **terpisah** untuk dana darurat, tanggal 1 pas gajian (bayar diri sendiri duluan).
> 2. Kurangi setoran Indodax sementara — alihkan dulu ke dana darurat sampai minimal 1 bulan pengeluaran pokok (~Rp6,9jt) terkumpul, biar ada bantalan kalau ada kejadian darurat.
> 3. Cek saldo utang Shopee Paylater kamu (total sisa, bukan cuma cicilan bulanan) — kalau mau, kirim detailnya, saya bisa bikinkan simulasi kapan lunasnya.
> 4. Gabungkan GoPay + OVO jadi satu e-wallet biar gak dobel top-up tanpa sadar (bulan ini total top-up Rp800rb).
> 5. Pantau 1 bulan ke depan pakai anggaran di atas — kalau masih mepet di akhir bulan, kabari saya, kita tinjau ulang posnya.
>
> ⚠️ Bukan nasihat keuangan/investasi, termasuk soal kripto. Angka di atas simulasi dari mutasi & asumsi di atas. Untuk kasus lebih rumit, konsultasikan ke perencana keuangan bersertifikat.

## Verifikasi independen penguji

Hitung ulang penguji (python): total debit Rp12.468.000, kredit Rp10.758.200, defisit **Rp1.709.800**, saldo akhir Rp2.440.200. Belanja dapur (Indomaret+Superindo+pasar) Rp1.787.500. Kedua sisi benar untuk angka ini.

**SEBELUM**
- Kelompok "wajib" Rp4.012.500 ✅; pengeluaran rutin ≈Rp6,8 jt (wajib + kiriman ortu + dapur) ✅; 6 bln Rp40,8 jt ✅; 9–12 bln Rp61–82 jt ✅ (61,2–81,6).
- Usulan budget menjumlah **Rp9.462.500**, sisa Rp37.500 tidak dialokasikan dan tidak disebut (bukan zero-based, minor).
- Klaim "rutin nyicil ke crypto 2,5jt/bulan" disimpulkan dari satu bulan data (asumsi).
- Nilai tambah: milestone 1 bulan (Rp6,8 jt) yang realistis lebih dulu.

**SESUDAH** (dijalankan ulang penguji dengan argumen yang sama → keluaran identik)
- Anggaran zero-based menjumlah tepat Rp9.500.000 ✅; cicilan 1.800.000/9.500.000 = 18,9% ✅; "kebutuhan 79,5%" = (wajib Rp6.557.500 + kiriman ibu Rp1 jt)/9,5 jt = 79,55% ✅.
- Dana darurat: pokok Rp6.907.500 × 9 = Rp62.167.500 ✅, ×12 = Rp82.890.000 ✅; kekurangan/Rp750rb = 77,6 → 78 bln (6 th 6 bln) ✅, 105,2 → 106 bln (8 th 10 bln) ✅.
- **Kesalahan:** pengeluaran pokok Rp6.907.500 **tidak memasukkan cicilan PayLater Rp650rb**, padahal catatan script sendiri menyebut pokok mencakup "cicilan minimum" dan balasan menulis "kontrakan, cicilan, dapur…". Seharusnya ±Rp7.557.500 (target 9 bln ±Rp68 jt). Selisih ±Rp5,85 jt.
- Pos jajan/e-wallet dipotong ke Rp692.500 padahal September nyata ±Rp1,9 jt (e-wallet 800rb + Shopee 412rb + tarik tunai 500rb + KFC 186rb); pemotongan sebesar itu tidak dibahas kelayakannya.
- Arisan dikategorikan "Tabungan" (bisa diperdebatkan, tidak salah).
- Lama 6,5 tahun ke target minimum disajikan jujur; langkah "1 bulan pokok dulu" ada di langkah minggu ini.

**Keduanya**: tidak memberi rekomendasi koin; keduanya menyarankan menunda/mengurangi top-up kripto sampai ada dana darurat (sesuai PANDUAN 5f). Keduanya menjalankan `find /` ke seluruh disk (menemukan salinan file di folder penguji dan home lain) — perilaku agent, bukan dari skill, tetapi skill tidak mencegahnya.

## Nilai

| | Sebelum | Sesudah |
|---|---|---|
| Skor (1–10) | 7 | 8 |

- SEBELUM 7: diagnosis tajam dan bahasa enak; angka umumnya benar walau tanpa script; budget tidak pas nol, tanpa disclaimer.
- SESUDAH 8: semua angka dari script dan terverifikasi, tabel siap pakai, asumsi ditulis, disclaimer, tawaran simulasi pelunasan PayLater. Dikurangi karena pokok dana darurat lupa cicilan PayLater (target kekecilan ±Rp5,85 jt) dan potongan jajan yang terlalu tajam tanpa catatan.
- Skill terpakai: `atur-keuangan-pribadi` (SKILL.md + `keuangan.py`). Selisih kualitas nyata tetapi sedang; SEBELUM sudah cukup baik untuk kasus ini.
