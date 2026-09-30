# HASIL UJI ULANG - program-referral-loyalitas

## Uji ulang 1.0.1 (2026-09-30)

- **Penguji:** agent independen (bukan pembuat). Hanya membaca folder skill, `HASIL-UJI.md` (temuan 1.0.0, skor 6) dan catatan revisi di README. Skill disalin ke scratchpad `.../scratchpad/uji-referral-101/`, tidak dipasang di `.claude/skills` repo.
- **Platform:** claude-code (simulasi agent). Uji muat OpenClaw tidak diulang di sesi ini.
- **Skor: 8,5/10 -> LULUS uji ulang** (ambang 7). Rincian di bawah.

### 1. Ringkasan
| Uji | Hasil |
|---|---|
| T1 format angka Indonesia di semua argumen | **Teratasi.** Bentuk valid terbaca benar, bentuk ambigu ditolak `GAGAL` kode 2 (bukti bagian 2) |
| T2 fasilitas kesehatan | **Teratasi.** Dasar aturan benar dan terverifikasi (bagian 4); 3 skenario kesehatan lulus. Ada 1 catatan SEDANG soal kode etik dokter gigi (N1) |
| S1 status saat pesanan pertama rugi | **Teratasi.** Status `RUGI DI PESANAN PERTAMA` (bukan `AMAN`) |
| S2 hadiah pemberi terbaca sebagai anjuran | **Teratasi.** Label `BATAS ATAS ... (bukan anjuran)` + baris `Hadiah pemberi SARAN` (konservatif) |
| R1 `%%` ganda di pesan galat | Teratasi (`hadiah teman 150% di luar batas wajar`) |
| 06-10 dijalankan ulang dengan 1.0.1 | Lulus; file `examples/06`-`10` diperbarui |
| 11 skenario normal baru: toko sembako grosir + reseller | Lulus (`examples/11-uji-toko-sembako-reseller.md`) |
| Contoh pembuat 01, 02, 04 | Keluaran script dijalankan ulang: identik dengan isi file (tidak ada regresi) |
| `python3 tests/uji_regresi.py` | 43 tes OK |
| `python3 scripts/validate.py --skill program-referral-loyalitas` | ✅ 1 skill valid, 113 baris katalog sesuai (setelah file uji diperbarui) |

### 2. Format angka Indonesia (input BARU buatan penguji)
Diterima dan benar (dibandingkan dengan hitungan independen `fractions.Fraction`):
```
poin --belanja-per-poin 12.500 --nilai-poin 150 --margin 47,5 --poin-beredar 73.215 --minimum-tukar 1.200 --breakage 12,5 --aov Rp137.500 --omzet-bulan 42,75jt
  -> 1,2% belanja; 2,53% margin; 11 poin = Rp1.650; laba Rp65.313 -> Rp63.663; omzet Rp513.000 / Rp448.875;
     LIABILITY 73.215 poin maks Rp10.982.250, perkiraan Rp9.609.469; minimum 1.200 poin = Rp15.000.000 / Rp180.000   (semua cocok)
poin ... --belanja-per-poin 12,5rb --nilai-poin Rp150,- --margin 47.5 --poin-beredar 73215 --minimum-tukar 1,2rb   -> hasil sama
poin ... --poin-beredar 1.234.567            -> 1.234.567 poin, Rp123.456.700 (benar)
simulasi --pelanggan-aktif 2.350 --aov 95.000 --margin 35 --hadiah-pemberi 7.500 --hadiah-teman 5% --skenario uji:7,5:1,5:22,5 --pesanan-ulang 0,5 --anggaran 2,5jt --cac-iklan 31.500
  -> 176 -> 264 -> 59 pembeli; omzet Rp8.407.500; biaya Rp722.750; laba kotor Rp2.942.625; bersih Rp2.219.875; ROI 307,14% (cocok)
simulasi --pelanggan-aktif 1,5rb ...         -> 1.500 pelanggan
impas --aov 95rb --margin 35 --hadiah-pemberi 10rb --frekuensi-bulan 0,25 --umur-bulan 18 --porsi-ltv 22,5
  -> LTV Rp149.625 (4,5 pesanan); batas Rp33.665; SARAN Rp16.625 (cocok)
biaya --aov 95rb --margin 35 --jumlah-referral 1.250 --anggaran 12.345.678 --hadiah-teman 9.500
  -> total Rp11.875.000; sisa anggaran Rp470.678; 28,57% laba (cocok)
biaya --aov "Rp 1.500.000,-" / 1,5jt / 1.5jt / 1.250,50  -> Rp1.500.000 / Rp1.500.000 / Rp1.500.000 / Rp1.250,50
```
Ditolak `GAGAL` kode 2 dengan pesan awam (benar, tidak ditebak):
```
--poin-beredar 73,215   -> ambigu: koma bisa desimal atau ribuan
--poin-beredar 73.2     -> ambigu: titik di Indonesia pemisah ribuan
--poin-beredar 1,5 / 40.000,5 / --jumlah-referral 12,5  -> harus bilangan bulat
--poin-beredar Rp5.000  -> jumlah, bukan rupiah; tulis tanpa 'Rp'
--pelanggan-aktif 2,350 -> ambigu
--frekuensi-bulan 1.000 / 1,000, --umur-bulan 1.000, --pesanan-ulang 1.000 / 1.5, --skenario a:10:1.000:20  -> ambigu
--hadiah-pemberi 12,5   -> ambigu: Rp12,5 kurang dari seribu; maksud 12,5rb?
--minimum-tukar 0       -> harus lebih dari 0
```
Catatan: rupiah `95,000` diterima sebagai Rp95.000 (gaya Inggris; tiga angka di belakang koma tidak masuk akal sebagai sen). Wajar, tetapi berbeda dengan jumlah `1,000` yang ditolak; lihat R-baru-1.

### 3. Status RUGI & label BATAS ATAS (input baru)
```
impas --aov 125rb --margin 32 --hadiah-pemberi 30rb --hadiah-teman 15% --biaya-lain 2.500 --frekuensi-bulan 0,5 --umur-bulan 12
  LPO Rp40.000; biaya Rp51.250; STATUS: RUGI DI PESANAN PERTAMA; PERHATIAN: RUGI Rp11.250 ... pesanan ke-2
  BATAS ATAS (bukan anjuran) Rp50.750; SARAN Rp0 + catatan "tidak ada ruang hadiah pemberi versi konservatif"
impas ... --hadiah-pemberi 60rb --hadiah-teman 20%   -> biaya Rp85.000 > batas Rp72.000: STATUS PERHATIAN + baris RUGI Rp45.000, pesanan ke-3, bulan ke-4
impas ... --hadiah-pemberi 250rb --hadiah-teman 20%  -> STATUS TIDAK DISARANKAN + RUGI Rp235.000, pesanan ke-7 > 6 pesanan seumur
impas ... --hadiah-teman 30rb                        -> AMAN, SARAN Rp0 (hadiah teman sudah 75% laba)
biaya --aov 125rb --margin 32 --hadiah-pemberi 30rb --hadiah-teman 12,5% --biaya-lain 2.500 --anggaran 1,5jt --cac-iklan 55rb
  -> teman Rp15.625; biaya Rp48.125 (38,5% / 120,31%); -Rp8.125 + PERHATIAN; kuota 31; lebih murah Rp6.875
```
Semua dihitung ulang independen: LPO, ceil(biaya/LPO), ceil((n-1)/frekuensi), LTV, floor(30% LTV), batas atas = batas - teman - lain, SARAN = floor(50% LPO) - teman - lain (min 0). Cocok semua. Status tidak pernah `AMAN` saat laba pesanan pertama negatif. (Bila biaya juga melewati batas aman, status `PERHATIAN`/`TIDAK DISARANKAN` tetap disertai baris `PERHATIAN: RUGI ...`; benar.)

### 4. Regulasi kesehatan (verifikasi web, 2026-09-30)
- **Permenkes 1787/MENKES/PER/XII/2010 Pasal 5 huruf m:** "mengiklankan promosi penjualan dalam bentuk apa pun termasuk pemberian potongan harga (diskon), imbalan atas pelayanan kesehatan dan/atau menggunakan metode penjualan multi-level marketing"; huruf n testimoni. Teks dikonfirmasi dari pasal.id (status "Berlaku") dan Klinik Hukumonline. PDF Kemkes (kms.kemkes.go.id, buku peraturan iklan) berhasil diunduh tetapi teksnya tidak terbaca utuh oleh alat penguji; salinan sireka.pom.go.id gagal TLS; peraturan.bpk.go.id menolak (403). Kutipan skill **sesuai**.
- **PP 28/2024:** PDF resmi dibaca (teks OCR). Pasal 1169: peraturan pelaksanaan dari PP yang dicabut "tetap berlaku sepanjang tidak bertentangan"; Pasal 1170 hanya mencabut PP (tidak ada Permenkes 1787/2010). Tidak ditemukan pasal pengganti tentang iklan/promosi fasilitas pelayanan kesehatan (yang ada: iklan sediaan farmasi, alkes, susu formula, tembakau, yankes tradisional). Klaim skill "tidak ditemukan pencabutan di PP 28/2024" **sesuai**.
- **UU 17/2023 Pasal 453:** teks pasal tidak berhasil dibaca langsung (peraturan.go.id 503, BPK 403); sumber sekunder menyebut ketentuan penutup mempertahankan peraturan pelaksanaan lama sepanjang tidak bertentangan. Klaim skill wajar; nomor pasal belum diverifikasi kata per kata oleh penguji.
- **KODEKGI 2020 (PB PDGI, PDF dibaca):** Pasal 3 cakupan 1: dilarang "promosi dalam bentuk apapun ... memberi janji baik langsung maupun tidak langsung ... dengan tujuan agar pasien datang"; cakupan 1.2.4: dilarang "membagi-bagikan/membuat selebaran atau spanduk potongan harga, kartu-nama dan identitas lain yang bertujuan komersial"; **Pasal 5 "Rabat dan komisi"**: dokter gigi "tidak diperkenankan menjaring pasien secara pribadi, melalui pasien atau agen" (penjelasan: termasuk kupon diskon). Klaim skill **sesuai**, tetapi Pasal 5 (paling tepat untuk referral) belum dikutip.
- **KODEKI 2012 (PB IDI, PDF dibaca):** penjelasan Pasal 3: dokter dilarang "berbagi imbalan/komisi/diskon, termasuk pola pemasaran beragam jenjang (multi-level marketing)" dan dilarang "menerima pemberian imbalan jasa apapun untuk pengiriman/rujukan pasien". Skill hanya menyebut "melarang memuji diri" (Pasal 4) untuk KODEKI; Pasal 3 lebih tepat.

Skenario kesehatan (penguji sebagai agent yang memakai skill; tanpa script karena tidak ada imbalan):
| Skenario | Perilaku skill | Hasil |
|---|---|---|
| Klinik kecantikan (facial + suntik botoks + laser): "ajak teman diskon 15% + poin tiap perawatan" | Dikenali sebagai fasilitas kesehatan (tindakan medis); diskon/poin/hadiah untuk merujuk tidak dirancang, termasuk untuk produk yang dijual klinik; alternatif: edukasi perawatan kulit umum, pengingat kontrol oleh staf, kartu info tanpa kode, tarif jujur, tanpa foto sebelum-sesudah/testimoni; PERLU REVIEW | Lulus |
| Praktik dokter gigi mandiri: "pasien yang bawa pasien baru dapat voucher belanja Rp50rb (bukan medis)" | Ditolak sopan: hadiah non-medis juga tidak dirancang ("dalam bentuk apa pun"); dasar Permenkes 1787/2010 Pasal 5 + KODEKGI; alternatif contoh 03; tidak meminta nomor teman pasien | Lulus (lihat N1) |
| Apotek: "member poin tiap Rp10rb = 1 poin, ajak teman diskon 10% obat" | Apotek = fasilitas kesehatan: diskon obat/poin/referral tidak dirancang; alternatif edukasi pemakaian obat, pengingat tebus ulang oleh staf untuk yang setuju, informasi harga jujur; bila pemilik tetap ingin, konfirmasi tertulis dinkes/organisasi profesi | Lulus (lihat R-baru-3) |

### 5. Temuan tersisa
**SEDANG**
- **N1. Alternatif "kartu info klinik boleh dibagikan pasien" dan "kelas edukasi" perlu catatan kode etik dokter gigi.** KODEKGI 2020 Pasal 3 cakupan 1.2.4 melarang membagikan "kartu-nama dan identitas lain yang bertujuan komersial"; cakupan 1.2.1-1.2.2 membatasi artikel/presentasi publik yang bertujuan agar pasien datang (perlu persetujuan MKEKG untuk hal tertentu). `pola-per-usaha.md` bagian 3 dan `examples/03` menganjurkan kartu info yang diberikan pasien ke kenalan dan kelas edukasi tanpa menyebut batas ini. Usulan: untuk dokter/dokter gigi, kartu info = informasi faktual yang diberikan **bila diminta**, tidak disebar; kelas edukasi non-komersial, tanpa penjualan, dan bila perlu mengikuti ketentuan MKEKG/MKEK; kutip KODEKGI Pasal 5 (rabat & komisi) dan KODEKI Pasal 3 (imbalan/komisi/diskon, imbalan rujukan). Sudah di bawah label PERLU REVIEW, jadi tidak memblokir.

**RENDAH**
- R-baru-1. Rupiah `95,000` diterima sebagai Rp95.000, sedangkan jumlah `1,000` ditolak ambigu. Tidak salah hitung, tetapi tidak konsisten dengan kalimat SKILL.md "angka yang bisa dibaca dua arah ditolak"; bisa disebut di SKILL.md.
- R-baru-2. `impas --porsi-ltv 22,5` menampilkan "Batas hadiah aman (23% ...)" (dibulatkan 0 desimal) dan baris penutup tetap menyebut "porsi 30%". Angka rupiah benar (Rp33.665); hanya label.
- R-baru-3. Apotek diperlakukan sama dengan klinik untuk seluruh produk (termasuk barang non-obat). Aman (konservatif) tetapi mungkin terlalu ketat; Kode Etik Apoteker (IAI) belum dirujuk. Biarkan di bawah PERLU REVIEW.
- R-baru-4. `impas --umur-bulan 0,5` tanpa hadiah: muncul "PERHATIAN: pesanan yang dibutuhkan untuk balik modal lebih banyak dari perkiraan pesanan seumur pelanggan" walau biaya Rp0. Kasus pinggir.
- Masih terbuka dari 1.0.0: R2 (`biaya --anggaran` saat biaya Rp0 diabaikan diam-diam), R3 (data anak/persetujuan orang tua belum disebut skill), R4 (omzet simulasi memakai nilai penuh), R6 (pesan argparse bahasa Inggris).

### 6. Alasan skor 8,5
Dua temuan TINGGI dan dua SEDANG dari 1.0.0 teratasi dengan benar dan teruji (43 tes regresi; puluhan input baru format Indonesia dihitung ulang independen, tidak ada selisih; tidak ada regresi di contoh 01-05). Bagian kesehatan kini menolak imbalan rujukan dengan dasar aturan yang terverifikasi dan memberi alternatif patuh. Nilai dikurangi karena N1 (alternatif klinik gigi belum memperhitungkan batas kode etik soal kartu/selebaran) dan beberapa temuan rendah. Bagian fasilitas kesehatan tetap **PERLU REVIEW tenaga medis/hukum** sebelum rilis.

### 7. File uji yang diperbarui/ditambah
`06-uji-toko-hijab-shopee-wa.md` (tambah `impas` opsi Rp50.000 + 20%: RUGI DI PESANAN PERTAMA), `07-uji-kafe-poin-stempel.md` (`52.340` kini diterima), `08-uji-les-privat-referral-orang-tua.md`, `09-uji-input-kurang-salon.md`, `10-uji-di-luar-cakupan-blast-mlm.md`, `11-uji-toko-sembako-reseller.md` (baru).

Sumber: https://pasal.id/peraturan/permen/permenkes-no-1787-menkes-per-xii-2010-tahun-2010 ; https://www.hukumonline.com/klinik/a/ketentuan-iklan-pelayanan-kesehatan-alternatif-di-televisi-lt5ad4049e8a0df/ ; https://kms.kemkes.go.id/contents/1715917225382-bukuperaturaniklanpublikasikes.pdf ; https://www.ipkindonesia.or.id/media/2024/08/Peraturan-Pemerintah-No-28-Tahun-2024-Tentang-Peraturan-Pelaksanaan-UU-No-17-Tahun-2023-Tentang-Kesehatan.pdf ; https://fkg.unair.ac.id/en/wp-content/uploads/2021/06/Buku-Kode-Etik-Kedokteran-Gigi-2020.pdf ; https://equalsid.or.id/dokumen/101124182354_KODEKI-Tahun-2012.pdf

### Catatan revisi 1.0.2 (2026-09-30, oleh kurator, bukan penguji)
- Temuan SEDANG uji ulang 1.0.1 (kartu info dibagikan pasien): kartu info klinik kini untuk pasien sendiri; klinik tidak meminta/mendorong pasien menyebarkannya. Rujukan KODEKGI 2020 Pasal 3 butir 1.2.4 & Pasal 5 serta KODEKI Pasal 3 ditambahkan di SKILL.md, references/pola-per-usaha.md, examples/03. Hanya teks, tanpa perubahan script.
- Skor katalog: 8 (uji ulang 8,5 dibulatkan ke bawah). Bagian fasilitas kesehatan tetap PERLU REVIEW tenaga medis/hukum.
