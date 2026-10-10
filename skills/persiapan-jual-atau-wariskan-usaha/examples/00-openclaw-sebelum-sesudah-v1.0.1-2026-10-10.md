# Uji OpenClaw sebelum/sesudah: persiapan-jual-atau-wariskan-usaha v1.0.1

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (independen, bukan pembuat v1.0.1)
- **Cara uji:** OpenClaw 2026.9.8, router claude-sonnet-5; `mk-home.sh` + `run-uji.sh` (VM Cursor, tanpa unshare). S1 SESUDAH juga `run-uji-tg.sh` (9539 karakter, utuh di chat).
- **Tes script:** `tests/uji_regresi.py` 15/15 OK.
- **Verifikasi angka:** S1 Rp136–204jt & hasil bersih Rp112,56–177,84jt; S2 bagian 40% Rp189,6–243jt — cocok `nilai_usaha.py`.

---

## Skenario 01 — Warung bakso + biaya sekali 2024

**Skor:** SEBELUM 6.5 · SESUDAH 9.0. Script + format 8 bagian; biaya 2024=12jt → rentang s/d Rp204jt (bukan Rp232jt v1.0.0).

**Pesan:**
> Saya Pak Darto, jualan bakso "Bakso Mas Darto" di Klaten...

### SEBELUM

# Hitung-hitungan Harga Jual Bakso Mas Darto

## 1. Laba yang pantas dipakai dasar kelipatan (bukan laba mentah)

Laba bersih yang Pak Darto laporkan sudah dipotong ambilan pribadi 3 jt/bulan (36 jt/tahun). Tapi kalau dijual, pembeli bukan Pak Darto — dia harus bayar orang 3,5 jt/bulan (42 jt/tahun) buat jaga. Jadi angkanya perlu disesuaikan: tambah balik ambilan lama, kurangi gaji pegawai baru. 2024 juga ada renovasi 12 jt yang sifatnya sekali-sekali, jadi ditambah balik supaya tidak menurunkan rata-rata.

| Tahun | Laba lapor | Koreksi | Laba "bersih riil" |
|---|---|---|---|
| 2023 | 84 | +36 (ambilan) −42 (gaji pegawai) | 78 |
| 2024 | 97 | +12 (renovasi) +36 −42 | 103 |
| 2025 | 91 | +36 −42 | 85 |

**Rata-rata laba riil ≈ Rp 89 juta/tahun** — ini yang dipakai kali lipat, bukan rata-rata laba lapor (90,7 jt).

## 2. Terapkan kelipatan 2–3x, lalu potong risiko

| | 2,0x | 2,5x | 3,0x |
|---|---|---|---|
| Nilai goodwill (89 jt × kelipatan) | 177 | 222 | 266 |
| − diskon resep rahasia 20% | 142 | 178 | 213 |
| + nilai alat (65 jt − 25% = 48,75 jt) | 190 | 226 | 262 |
| **= Harga jual wajar (gross)** | **190** | **226** | **262** |
| − utang koperasi 18 jt | 172 | 208 | 244 |
| − notaris/perantara 4% dari harga jual | −7,6 | −9,1 | −10,5 |
| **= Uang bersih diterima Pak Darto** | **~165** | **~199** | **~234** |

## 3. Kesimpulan angka

- **Harga jual wajar ditawarkan ke calon pembeli: Rp 190–260 juta**, titik tengah realistis **~Rp 225 juta**.
- **Uang bersih masuk kantong Pak Darto setelah lunasi utang koperasi dan notaris: Rp 165–234 juta**, titik tengah **~Rp 200 juta**.
- Kebutuhan pensiun 6 jt × 18 bulan = **Rp 108 juta** — bahkan skenario paling konservatif (165 jt) masih sisa ~57 juta buffer di luar kebutuhan itu. Aman.
- Tawaran tetangga "2x laba" (≈181 jt) kemungkinan pakai laba lapor mentah, belum masukkan nilai alat terpisah dan belum potong risiko resep. **Jangan terima mentah-mentah** — jelaskan ke dia breakdown di atas, atau tanyakan apakah 2x itu sudah termasuk alat atau belum.

## 4. Dua hal yang menahan Pak Darto di angka bawah (2x), bukan 3x

1. **Sisa kontrak kios tinggal 2 tahun** — pembeli tidak punya kepastian lokasi jangka panjang, risiko buat dia.
2. **Resep rahasia hanya Pak Darto yang tahu** — kalau tidak ada transfer/pendampingan, nilai usaha rapuh.

**Cara menaikkan harga ke arah 3x:** tawarkan masa pendampingan/training resep 1–3 bulan ke pembeli secara tertulis, dan coba negosiasi perpanjangan sewa kios dengan pemilik sebelum serah terima. Dua langkah ini langsung mengurangi alasan diskon 20% tadi.

## 5. Yang harus disiapkan sebelum nego

- Laporan laba-rugi 3 tahun (2023–2025) dicetak rapi, siap ditunjukkan.
- Daftar alat + kondisi + foto (gerobak, freezer, meja-kursi, motor) untuk justifikasi nilai 48,75 jt.
- Surat keterangan sisa utang koperasi dari koperasinya (buat kepastian angka 18 jt, dan siapa yang melunasi — Pak Darto sebelum closing, atau dipotong dari harga jual).
- Cek klausul kontrak sewa kios: bisa dialihkan ke pembeli baru atau tidak (assignment clause).
- Draft perjanjian jual-beli usaha (pakai notaris) yang memuat: harga, cara bayar, masa pendampingan resep, status pegawai, alih sewa kios, pelunasan utang koperasi.
- Pisahkan dulu Rp 108 juta untuk biaya hidup 18 bulan (taruh di rekening/deposito terpisah), sisanya baru dipikir buat investasi pensiun.
- Tanyakan ke kantor pajak/konsultan kecil soal kewajiban pajak penjualan usaha — ini belum dihitung di atas dan bisa mengurangi net yang diterima.
- Tetapkan **harga minimum (walk-away) ~Rp 190 juta gross** sebelum mulai nego — di bawah itu jangan dilepas.

### SESUDAH

# Persiapan Jual/Wariskan Usaha Bakso Mas Darto

## 1. Ringkasan situasi dan asumsi
- Usaha: warung bakso perorangan, 7 tahun jalan, kios sewa (sisa kontrak 2 tahun), Klaten.
- Tujuan: pensiun, rencana oper ke pembeli tahun depan (saya pakai kerangka waktu 12 bulan).
- Laba bersih 2023 Rp84.000.000, 2024 Rp97.000.000, 2025 Rp91.000.000 — sudah dipotong ambilan pribadi Rp3.000.000/bulan.
- Asumsi yang saya pakai persis dari angka Bapak: kelipatan laba 2–3x (dari perkiraan Bapak sendiri), potongan ketergantungan pemilik 20% (karena resep hanya Bapak yang tahu), penyesuaian aset turun 25%, biaya notaris/perantara 4%, utang koperasi Rp18.000.000 **dilunasi Bapak dari hasil jual** (default karena belum disebutkan ikut ke pembeli atau tidak — tolong konfirmasi), porsi yang berpindah 100% (jual usaha utuh, bukan sebagian).
- Biaya renovasi kios+gerobak Rp12.000.000 di 2024 saya tambahkan kembali ke laba 2024 saja (sekali jalan, bukan biaya rutin).
- Gaji pengganti: saya hitung biaya mempekerjakan orang untuk "jaga" Rp3.500.000/bulan (Rp42.000.000/tahun) sebagai pengganti tenaga Bapak, dikurangi dari laba; ambilan Bapak Rp3.000.000/bulan (Rp36.000.000/tahun) ditambahkan kembali karena itu kompensasi pribadi, bukan biaya operasional murni.

## 2. Daftar periksa kesiapan

| Area | Status | Catatan |
|---|---|---|
| Pembukuan | Setengah | Ada angka laba bersih 3 tahun, tapi belum jelas apakah tercatat rapi dan cocok dengan mutasi rekening/kas harian |
| Pemisahan uang pribadi-usaha | Belum diketahui | [isian] |
| SOP | Belum | Resep bumbu hanya diingat Bapak, belum tertulis |
| Ketergantungan pemilik | Belum | Resep rahasia = usaha sangat bergantung pada Bapak; ini sebab potongan 20% di nilai |
| Aset | Setengah | Ada daftar dan perkiraan nilai (Rp65.000.000), tapi bukti kepemilikan (nota beli, BPKB motor) belum disebut |
| Utang | Siap | Sisa utang koperasi Rp18.000.000 diketahui jelas |
| Kontrak | Setengah | Sisa sewa 2 tahun diketahui; apakah pemilik kios mengizinkan sewa dialihkan ke pembeli belum diketahui |
| Izin | Belum diketahui | NIB/izin usaha atas nama siapa, masih berlaku atau tidak |
| Pelanggan/pemasok kunci | Belum diketahui | [isian] |
| Karyawan | Belum diketahui | Saat ini siapa yang bantu jaga, status kerja mereka |
| Aset tak berwujud | Belum diketahui | Nama "Bakso Mas Darto", akun medsos/nomor WA usaha atas nama siapa |
| Penerus | Setengah | Tetangga sudah menawar; belum ada kesepakatan tertulis |

### 3-5 prioritas pembenahan
1. **Tulis resep & SOP racikan bumbu secara rinci** — ini risiko terbesar: tanpa ini, nilai usaha di sisi atas (mendekati Rp204 juta) sulit dipercaya pembeli, dan usaha bisa "mati rasa" begitu Bapak pergi.
2. **Cek dan pastikan kontrak sewa kios bisa dialihkan** ke pembeli/penerus — sisa 2 tahun ini aset penting, tapi kalau tidak bisa dialihkan nilainya turun.
3. **Rapikan pembukuan 2023-2025 dan pisahkan uang pribadi-usaha**, cocokkan dengan kas/rekening agar laba yang disebut bisa dibuktikan ke calon pembeli.
4. **Siapkan daftar aset dengan bukti kepemilikan** (nota gerobak/freezer/meja-kursi, BPKB motor).
5. **Pastikan status NIB/izin usaha dan nama "Bakso Mas Darto"** (merek, akun medsos, nomor WA) — siapa pemegangnya dan bagaimana dialihkan.

## 3. Ketergantungan pada pemilik
Kalau Bapak tidak masuk 1 bulan sekarang, apa yang berhenti? Dari info yang ada: racikan bumbu berhenti total karena hanya Bapak yang tahu resepnya — ini kelemahan paling besar untuk proses jual-beli. Begitu didokumentasikan dan diajarkan ke calon pembeli/karyawan, potongan ketergantungan 20% itu bisa turun, artinya harga jual bisa naik. Ini pekerjaan nomor satu sebelum pensiun tahun depan.

## 4. Perkiraan rentang nilai (bahan diskusi, bukan harga pasti)

| Metode | Rentang | Rumus/asumsi |
|---|---|---|
| Kelipatan laba normalisasi | Rp136.000.000 s/d Rp204.000.000 | basis laba Rp85.000.000 x kelipatan [2-3] x (100-20%)/100 |
| Nilai aset setelah penyesuaian | Rp48.750.000 (batas bawah bila hanya aset dijual) | Rp65.000.000 x (100-25%)/100 |

- Laba setelah penyesuaian: 2023 Rp78.000.000; 2024 Rp103.000.000 (sudah termasuk tambahan balik renovasi Rp12.000.000); 2025 Rp85.000.000.
- Rata-rata 3 tahun Rp88.666.667, tapi laba tahun terakhir (2025) lebih rendah (Rp85.000.000) — basis yang dipakai angka yang lebih hati-hati ini, **Rp85.000.000**.
- **Nilai usaha 100% (sebelum utang): Rp136.000.000 s/d Rp204.000.000.**
- Utang koperasi Rp18.000.000: saya asumsikan dilunasi Bapak dari hasil jual (bukan ikut ke pembeli) — harga yang dibayar pembeli tetap di rentang di atas.
- Setelah biaya notaris/perantara 4%: **Rp130.560.000 s/d Rp195.840.000**.
- **Hasil bersih ke Bapak (setelah biaya transaksi dan pelunasan utang Rp18 juta): Rp112.560.000 s/d Rp177.840.000.**
- Kebutuhan hidup 18 bulan x Rp6.000.000 = Rp108.000.000. Selisih hasil bersih vs kebutuhan: **+Rp4.560.000 s/d +Rp69.840.000** — di sisi atas cukup lega, tapi di sisi bawah (kelipatan 2x, laba basis rendah) hanya selisih tipis Rp4,56 juta. Pajak belum masuk di sini, jadi jangan dianggap sudah pasti aman.
- Sebagai perbandingan: tawaran tetangga "2 kali laba" (tanpa potongan ketergantungan) ≈ Rp170 juta — itu masuk di dalam rentang kami (Rp136-204 juta), jadi tawaran itu bukan tidak masuk akal, tapi masih di bawah titik tengah.

**PERINGATAN:**
- Kelipatan 2-3x dan semua persentase di atas adalah **asumsi Bapak sendiri**, bukan angka pasar yang pasti.
- Pajak atas keuntungan jual usaha, BPHTB (bila ada tanah/bangunan), dan biaya transaksi riil belum masuk — bisa mengurangi hasil bersih lebih jauh.
- Nilai aset (Rp48,75 juta) jauh di bawah batas bawah kelipatan laba (Rp136 juta) — wajar, karena usaha berjalan (goodwill + pelanggan tetap) biasanya lebih berharga dari sekadar alat-alatnya.

## 5. Pilihan struktur (belum diputuskan, bahan diskusi)
- **Jual seluruhnya sekaligus** vs **bertahap** (misal DP + cicilan dari laba bulan berjalan) — cicilan lebih aman untuk pembeli tapi ada risiko gagal bayar untuk Bapak; *tanyakan ke notaris cara mengamankan cicilan*.
- **Jual usaha+resep sekaligus** vs **hanya alat-alat (aset)** dan Bapak pensiun total tanpa warisi nama/resep — nilainya jauh beda (lihat tabel di atas).
- **Masa pendampingan** 1-3 bulan setelah serah terima untuk mengajarkan resep dan kenalkan ke pelanggan — ini yang membuat harga sisi atas lebih masuk akal bagi pembeli.
- Semua pilihan ini: *tanyakan ke notaris/konsultan pajak* cara teraman menuliskannya.

## 6. Rencana transisi (12 bulan, target oper tahun depan)

| Bulan | Fokus | Tugas konkret |
|---|---|---|
| 1 | Foto kondisi | Tulis resep & SOP bumbu secara rinci; kumpulkan rekap laba 2023-2025 + mutasi rekening; tetapkan harga terendah yang Bapak terima |
| 2-3 | Rapikan | Pisahkan uang pribadi-usaha; daftar aset dengan bukti milik; cek sisa kontrak sewa kios & tanya pemilik kios apakah bisa dialihkan |
| 3-5 | Kurangi ketergantungan | Latih calon penerus/karyawan meracik bumbu sendiri; delegasikan buka-tutup kios |
| 4-6 | Konsultasi profesional | Bawa daftar pertanyaan (bagian 7) ke notaris dan konsultan pajak |
| 6-9 | Penerus/pembeli | Bicara serius dengan tetangga (atau calon lain) soal harga, struktur bayar; kenalkan ke pelanggan tetap |
| 9-12 | Serah terima | Masa pendampingan; urus pengalihan NIB/izin, nama kios, akun medsos; lunasi utang koperasi dari hasil jual; umumkan ke karyawan/pelanggan |

**Rencana darurat:** siapa yang pegang resep, kunci kios, dan kontak pemasok bila Bapak mendadak sakit sebelum serah terima selesai — catat dan titipkan ke orang terpercaya.

## 7. Dokumen yang disiapkan untuk calon pembeli
- Rekap laba 2023-2025 + mutasi rekening pendukung
- Daftar aset (gerobak, freezer, meja-kursi, motor) dengan bukti milik
- Rincian utang koperasi (sisa, jatuh tempo)
- Salinan kontrak sewa kios (sisa masa, syarat pengalihan)
- NIB dan izin usaha lain
- Resep bumbu tertulis (dibagikan hanya setelah ada perjanjian kerahasiaan)
- Daftar pelanggan/pemasok kunci (tanpa kontak lengkap sebelum calon serius)
- Bukti nama "Bakso Mas Darto" & akun medsos/WA usaha
- Perjanjian kerahasiaan sebelum data sensitif dibagikan (minta notaris siapkan)

## 8. Pertanyaan untuk notaris & konsultan pajak
**Notaris/PPAT:**
- Usaha perorangan seperti ini, dokumen apa yang jadi bukti peralihan alat dan nama usaha?
- Apakah sewa kios bisa dialihkan ke pemilik baru, dan apa yang harus disetujui pemilik kios lebih dulu?
- **Harta bersama:** apakah usaha ini termasuk harta bersama dengan istri, dan perlu persetujuan tertulis beliau untuk menjualnya?
- Bagaimana perjanjian kerahasiaan dan masa pendampingan dibuat agar mengikat?
- Apakah penerus/pembeli perlu NIB sendiri, dan apa yang terjadi dengan NIB Bapak?

**Konsultan pajak:**
- Berapa kewajiban pajak atas keuntungan jual usaha ini (PPh), dan apakah ada komponen PPN bila Bapak PKP?
- Bagaimana laporan pajak tahun-tahun lalu perlu dirapikan sebelum dijual?
- Apakah pajak sebaiknya ikut dipertimbangkan saat menetapkan harga terendah yang Bapak terima?

**Karyawan (bila ada staf saat ini):** apakah karyawan otomatis ikut ke pemilik baru, dan hak apa saja yang harus dijaga?

## Catatan penutup
Angka rentang di atas (Rp112,56 juta s/d Rp177,84 juta hasil bersih untuk Bapak) adalah **bahan diskusi, bukan harga pasti** — pajak belum dihitung dan kelipatannya dari perkiraan Bapak sendiri, bukan angka pasar resmi. Prioritas paling mendesak: tuliskan resep sebelum apa pun lain, karena itu yang paling menentukan apakah usaha ini bisa dinilai mendekati sisi atas atau terjebak di sisi bawah rentang.

Tiga hal yang perlu saya ketahui untuk menajamkan ini:
1. Kalau utang koperasi Rp18 juta itu ternyata disepakati ikut ke pembeli (bukan dilunasi Bapak), hasil bersih Bapak akan beda — mana yang Bapak rencanakan?
2. Apakah pemilik kios sudah tahu rencana pengoperan, dan apakah izin sewa bisa dialihkan?
3. Apakah Bapak bersedia memberi masa pendampingan (1-3 bulan) ke pembeli untuk mengajarkan resep, supaya harga di sisi atas lebih bisa dipertahankan?

---

## Skenario 02 — Beli bagian sekutu CV (porsi 40%)

**Skor:** SEBELUM 6.0 · SESUDAH 9.0. Beli-keluar mitra: porsi 40%, utang dikurangi dulu → Rp189,6–243jt cocok Decimal.

**Pesan:**
> Saya Rudi, punya CV Mitra Teknik...

### SEBELUM

Oke Rudi, saya hitungkan pakai metode yang biasa dipakai untuk valuasi usaha kecil/jasa (gabungan laba + aset bersih, dikurangi utang), lalu daftar yang perlu diurus secara legal.

## 1. Normalisasi laba dulu

Laba yang disepakati (240jt & 270jt) itu **sudah termasuk gaji kalian berdua** (7jt/bln masing-masing = 168jt/thn total). Begitu Yanto keluar, posisinya diganti kepala teknisi gaji 6jt/bln — lebih murah 1jt/bln dari gaji Yanto. Jadi laba ke depan perlu disesuaikan (ditambah) karena biaya operasional turun:

- Rata-rata laba 2024–2025: (240 + 270) / 2 = **Rp255 juta**
- Penghematan gaji (7jt → 6jt = 1jt/bln): +Rp12 juta/tahun
- **Laba disesuaikan (dasar valuasi): ≈ Rp267 juta/tahun**

## 2. Hitung nilai usaha

| Komponen | 2,0x | 2,5x |
|---|---|---|
| Laba disesuaikan × multiple | 534 jt | 667,5 jt |
| + Aset (alat, mobil ops) 180jt, nilai wajar turun 20% → 144 jt | +144 jt | +144 jt |
| = Nilai usaha kotor | 678 jt | 811,5 jt |
| – Utang leasing mobil 60 jt | 618 jt | 751,5 jt |
| **Nilai ekuitas bersih CV** | **618 jt** | **751,5 jt** |

## 3. Bagian Yanto (40%)

- Rentang: Rp247,2 juta – Rp300,6 juta
- Titik tengah (pakai multiple 2,25x): **≈ Rp274 juta**

## 4. Biaya notaris & admin (3%)

- Dihitung dari nilai transaksi (bagian Yanto): ≈ Rp7,4 – 9 juta (titik tengah ≈ Rp8,2 juta)

## Kesimpulan angka

- **Nilai bagian Yanto: kira-kira Rp247–301 juta, titik tengah ≈ Rp274 juta**
- **Dana total yang perlu disiapkan Rudi (sudah + notaris): ≈ Rp255–310 juta, titik tengah ≈ Rp282 juta**

**Catatan asumsi yang perlu kalian konfirmasi** (karena ini memengaruhi angka cukup besar):
- Saya anggap "2–2,5x laba" itu nilai *goodwill/earning power* saja, dan aset (144jt) ditambahkan terpisah. Kalau maksud kalian "2–2,5x laba" sudah mewakili *seluruh* nilai usaha (termasuk aset di dalamnya), maka jangan tambahkan 144jt lagi — hasilnya akan lebih rendah (bagian Yanto jadi sekitar Rp190–243jt). Sebaiknya samakan dulu persepsi ini berdua sebelum deal final.
- Saya anggap "turun 20%" = nilai pasar wajar aset sekarang 80% dari 180jt. Kalau 180jt itu sudah nilai sekarang (bukan nilai beli), tidak perlu dipotong lagi 20% → aset bersih langsung 180jt.

## 5. Yang harus diurus (legal & administratif)

1. **Perjanjian jual-beli porsi/penyertaan modal** (tertulis) — memuat nilai transaksi, skema pembayaran (tunai/cicilan + jadwal), tanggal efektif, dan klausul pelepasan tanggung jawab Yanto atas utang/kewajiban CV ke depan (indemnity & release).
2. **Akta notaris perubahan CV** — perubahan susunan sekutu (sekutu komplementer/komanditer), perubahan modal, nama pengurus baru.
3. **Pendaftaran perubahan ke AHU (Kemenkumham)** via SABU — update data CV secara resmi.
4. **Update OSS/NIB** — ganti data pengurus/penanggung jawab, perizinan usaha.
5. **Update NPWP** perusahaan (dan cek kewajiban pajak Yanto pribadi — konsultasikan ke konsultan pajak apakah ada pajak atas selisih nilai pengalihan porsi).
6. **Rekening bank perusahaan** — ganti specimen tanda tangan, hapus akses Yanto, update otorisasi.
7. **Leasing mobil (utang 60jt)** — konfirmasi atas nama siapa; jika atas nama Yanto pribadi, perlu dialihkan/dilunasi/di-take over atas nama CV atau Rudi.
8. **Aset lain atas nama bersama** (kendaraan, properti, rekening) — balik nama jika perlu.
9. **Surat pernyataan lunas & pelepasan hak** dari Yanto setelah pembayaran selesai, supaya tidak ada klaim di kemudian hari.
10. **Klausul non-kompetisi** (opsional tapi disarankan) — agar Yanto tidak buka usaha servis AC sejenis yang bersaing langsung di area yang sama dalam periode tertentu.
11. **Serah terima operasional** — handover klien, SOP teknis, relasi supplier dari Yanto ke kepala teknisi baru.
12. **Rekrut & onboarding kepala teknisi pengganti** (gaji 6jt/bln) sebelum/bersamaan Yanto keluar, supaya operasional tidak terganggu.
13. Libatkan **notaris + akuntan/konsultan pajak independen** untuk finalisasi angka dan legalitas — terutama karena nilainya ratusan juta, worth it untuk memastikan tidak ada sengketa di kemudian hari.

Kalau mau, saya bisa bantu buatkan draf perjanjian jual-beli porsi atau checklist dokumen yang lebih detail — tinggal bilang.

### SESUDAH

# Persiapan Beli Bagian Sekutu — CV Mitra Teknik (Bandung)

## 1. Ringkasan situasi & asumsi

Rudi (60%) membeli bagian Yanto (40%) di CV Mitra Teknik — bukan jual seluruh usaha, tapi **beli/lepas bagian sekutu CV**. Asumsi yang saya pakai (semua dari Anda berdua, kecuali disebut lain):

| Item | Angka |
|---|---|
| Laba bersih 2024 | Rp240.000.000 (sudah dipotong gaji Rudi+Yanto masing² Rp7jt/bln) |
| Laba bersih 2025 | Rp270.000.000 (sama) |
| Penyesuaian: gaji Yanto ditambah balik, gaji kepala teknisi pengganti dikurangkan | +Rp84.000.000/thn, −Rp72.000.000/thn |
| Aset operasional (alat, mobil, dll) | Rp180.000.000, disusutkan 20% |
| Utang leasing mobil | Rp60.000.000 |
| Kelipatan laba (disepakati Anda & Yanto) | 2x – 2,5x |
| Biaya notaris dkk | 3% |
| Porsi yang berpindah | 40% (bagian Yanto) |

Catatan: hanya 2 tahun laba (bukan 3) — rentang di bawah kurang kuat untuk diyakinkan ke pihak lain, tapi cukup untuk diskusi internal Anda berdua.

## 2. Daftar periksa kesiapan

| Area | Status | Langkah berikut |
|---|---|---|
| Pembukuan 2-3 tahun | Setengah (ada laba 2 tahun) | Lengkapi neraca & mutasi rekening pendukung |
| Pemisahan uang pribadi-usaha | Belum diketahui | Pastikan sebelum ke notaris |
| SOP kerja inti | Belum diketahui | Tulis SOP servis/pasang AC sebelum Yanto keluar |
| Ketergantungan pemilik | Belum diketahui — **kunci**: apakah pelanggan besar/pemasok melekat ke Yanto pribadi? | Cek dan rencanakan pengenalan ke kepala teknisi baru |
| Aset | Ada nilai (Rp180jt) | Lengkapi bukti milik (BPKB mobil, kartu alat) |
| Utang | Ada (leasing mobil Rp60jt) | Cek sisa persis + **apakah Yanto jadi penjamin pribadi** |
| Kontrak | Belum diketahui | Sewa bengkel/kios, kontrak pelanggan B2B (gedung, apartemen dll)? |
| Izin | Belum diketahui | NIB CV, izin usaha (mis. instalasi listrik/AC) atas nama siapa |
| Pelanggan/pemasok kunci | Belum diketahui | Daftar 5 pelanggan & pemasok terbesar |
| Karyawan | Setengah (pengganti Yanto sudah ada) | Daftar teknisi lain, status kerja, hak tertunda |
| Aset tak berwujud | Belum diketahui | Nama "Mitra Teknik", akun medsos/WA usaha — atas nama siapa? |

**Prioritas pembenahan:**
1. Sepakati siapa menanggung biaya notaris & pajak, dan cara bayar ke Yanto (sekaligus/cicil dari laba).
2. Lengkapi bukti milik aset + cek status jaminan pribadi Yanto di leasing mobil.
3. Tulis SOP kerja teknisi inti sebelum serah terima ke kepala teknisi baru.
4. Cek NIB/izin usaha CV dan pastikan sudah/bisa diubah tanpa gangguan operasional.
5. Siapkan akta perubahan CV di notaris sebelum Yanto resmi keluar.

## 3. Perkiraan rentang nilai (bahan diskusi, bukan harga pasti)

| Langkah | Hasil |
|---|---|
| Laba setelah disesuaikan | 2024: Rp252.000.000; 2025: Rp282.000.000 |
| Basis dipakai (rata-rata, karena tahun terakhir lebih tinggi) | Rp267.000.000 |
| **Nilai usaha 100%, kelipatan 2-2,5x** (sebelum utang) | **Rp534.000.000 – Rp667.500.000** |
| Nilai aset saja (batas bawah pembanding, sebelum utang) | Rp144.000.000 |
| Utang leasing Rp60jt: karena ini jual sebagian, utang tetap di badan usaha → dikurangkan dulu, baru dikali porsi | — |
| **Bagian Yanto (40%) — harga yang dibayar Rudi** | **Rp189.600.000 – Rp243.000.000** |
| Setelah biaya notaris dkk 3% (asumsi dipotong dari nilai transaksi) | Rp183.912.000 – Rp235.710.000 |

Pembanding: bila usaha ditutup total dan aset dijual (aset Rp144jt − utang Rp60jt), nilainya cuma Rp84.000.000 untuk 100% — jauh di bawah kelipatan laba, jadi usaha **berjalan** jelas lebih bernilai daripada ditutup. Masuk akal untuk Yanto tetap pakai metode kelipatan laba.

**Peringatan:**
- Hanya 2 tahun laba dipakai — kalau mau rentang lebih meyakinkan, tambah data 2023.
- Siapa menanggung 3% biaya notaris (Rudi, Yanto, atau dibagi) **belum ditentukan** — ini akan menggeser angka yang benar-benar diterima Yanto.
- Kelipatan 2-2,5x dan 3% adalah asumsi Anda berdua, bukan angka pasar resmi.

## 4. Pilihan struktur (tanyakan ke notaris/konsultan pajak)

- **Bayar sekaligus** vs **dicicil dari laba usaha** beberapa bulan/tahun — pengaruh ke arus kas CV dan risiko bila laba turun.
- **Jaminan pribadi Yanto di leasing mobil**: dilepas (perlu persetujuan leasing company) atau tetap sampai lunas — penting diputuskan sebelum akta perubahan.
- **Masa pendampingan Yanto** untuk transisi ke kepala teknisi baru (berapa bulan, dibayar atau tidak).
- **Siapa menanggung biaya notaris & pajak** — tulis tegas di kesepakatan.

## 5. Rencana transisi (3-6 bulan, lebih cepat karena ini buyout internal)

| Bulan | Fokus | Tugas |
|---|---|---|
| 1 | Sepakati angka & syarat | Tetapkan harga final dari rentang di atas, cara bayar, siapa tanggung biaya; mulai cek jaminan pribadi di leasing |
| 1-2 | Rapikan dokumen | Lengkapi bukti aset, cek NIB/izin, lengkapi neraca |
| 2-3 | Ke notaris | Bawa daftar pertanyaan di bawah; siapkan akta perubahan CV |
| 2-4 | Transisi operasional | Tulis SOP; kenalkan kepala teknisi baru ke pelanggan/pemasok kunci; Yanto mendampingi |
| 4-6 | Serah terima resmi | Tanda tangan akta, lunasi/transfer pembayaran, ubah nama di izin/rekening/akun usaha; umumkan ke karyawan & pelanggan |

Rencana darurat: pastikan Rudi (atau kepala teknisi baru) pegang akses rekening, kontak pemasok/pelanggan kunci, dan kunci bengkel — jangan hanya ada di Yanto.

## 6. Dokumen yang perlu disiapkan

- Akta pendirian CV (dan akta perubahan sebelumnya jika ada) — cek dulu apa sudah diatur soal sekutu keluar
- Laporan laba 2024-2025 + neraca/mutasi rekening pendukung
- Daftar aset (alat, mobil) dengan bukti milik (BPKB, kartu alat)
- Dokumen leasing mobil (sisa utang, siapa penjamin pribadi)
- NIB dan izin usaha CV
- Kontrak kerja kepala teknisi pengganti
- Daftar karyawan lain, kontrak sewa bengkel/kios bila ada
- Kesepakatan tertulis harga & cara bayar (draft sebelum ke notaris)

## 7. Pertanyaan untuk notaris & konsultan pajak

**Notaris:**
- Akta perubahan CV untuk sekutu keluar: dokumen apa saja dan bagaimana pendaftarannya? (prosedur pastinya belum terverifikasi di sumber saya — tanyakan langsung, jangan andalkan asumsi)
- Apa yang diatur akta pendirian CV soal sekutu keluar — apakah ada hak beli lebih dulu, cara hitung bagian?
- Bagaimana melepaskan jaminan pribadi Yanto atas utang leasing — perlu persetujuan kreditur?
- **Harta bersama:** apakah bagian usaha ini termasuk harta bersama Rudi/Yanto dengan pasangan masing², perlu persetujuan tertulis istri?
- Bagaimana bentuk pembayaran bertahap diatur agar mengikat secara hukum?

**Konsultan pajak:**
- PPh atas keuntungan Yanto dari penjualan bagiannya di CV — bagaimana dihitung?
- Apakah ada PPN jika ada aset (alat/mobil) yang ikut dialihkan dan CV sudah PKP?
- Bagaimana laporan pajak CV perlu dirapikan sebelum transaksi ini dicatat?
- Apakah pembayaran bertahap punya konsekuensi pajak berbeda dari sekaligus?

## 8. Catatan penutup

Perkiraan **bagian Yanto: sekitar Rp184 juta – Rp236 juta** (setelah 3% biaya, siapa yang bayar masih perlu disepakati) — ini bahan diskusi Anda berdua, bukan harga pasti, dan belum termasuk pajak yang mungkin dikenakan ke Yanto.

Tiga hal yang perlu dijawab untuk melanjutkan:
1. Siapa menanggung 3% biaya notaris — Rudi, Yanto, atau dibagi?
2. Apakah Yanto masih jadi penjamin pribadi di leasing mobil — sudah dibicarakan dengan pihak leasing?
3. Akta pendirian CV sebelumnya sudah mengatur cara sekutu keluar/harga, atau ini dibuat baru dari nol?

---

## Skenario 03 — Jual laundry tanpa angka

**Skor:** SEBELUM 5.0 · SESUDAH 8.0. Sesudah kerja dulu dengan asumsi; sebelum hanya minta data.

**Pesan:**
> Mau jual usaha laundry saya di Surabaya, nilainya berapa ya?

### SEBELUM

Belum ada catatan soal usaha laundry ini di memori saya, dan web search lagi nggak tersedia — jadi aku nggak bisa langsung kasih angka pasti. Tapi aku bisa bantu hitung estimasinya kalau kamu kasih beberapa data kunci, karena valuasi usaha laundry itu biasanya dihitung dari kombinasi beberapa pendekatan ini:

**Metode yang umum dipakai untuk usaha laundry (UMKM jasa):**

1. **Asset-based (nilai aset)** — total nilai mesin cuci/pengering, properti/sewa tempat, peralatan, stok deterjen, kendaraan antar-jemput (kalau ada), dikurangi utang.
2. **Earnings multiple (kelipatan laba bersih)** — untuk usaha jasa kecil di Indonesia, biasanya dihargai **2-4x laba bersih tahunan**, tergantung stabilitas pelanggan, lokasi, dan apakah ada sistem/brand yang established.
3. **Revenue multiple** — kadang dipakai juga 0,5-1x omzet tahunan sebagai cross-check.

**Yang aku butuh dari kamu buat kasih estimasi konkret:**
- Omzet per bulan dan laba bersih per bulan (rata-rata 6-12 bulan terakhir)
- Jumlah & kondisi mesin (cuci + pengering), usia mesin
- Status tempat: sewa atau milik sendiri? Kalau sewa, berapa sisa kontraknya?
- Jumlah pelanggan tetap/langganan vs walk-in
- Jumlah karyawan dan gaji
- Lokasi di Surabaya (area mana — dekat kampus/kos-kosan biasanya lebih bernilai)
- Berapa lama sudah berjalan dan apakah ada brand/nama yang dikenal

Kasih aku angka-angka itu (minimal omzet & laba bulanan + jumlah mesin), nanti aku hitungkan range harga jualnya pakai metode kelipatan laba + nilai aset biar lebih akurat daripada tebak-tebakan.

### SESUDAH

Oke, saya bantu siapkan jual usaha laundry Surabaya-nya. Satu hal dulu: saya bukan penilai resmi dan ini bukan patokan harga pasti — hasilnya bahan diskusi, biar Anda datang ke calon pembeli/notaris dengan bahan yang rapi.

# Persiapan Jual Usaha Laundry [isian: nama usaha]

## 1. Ringkasan situasi dan asumsi
- Lokasi: Surabaya [isian: umur usaha, sewa/milik tempat]
- Tujuan: jual (asumsi, sebut bila beda — mis. mau serahkan ke karyawan/keluarga malah lebih murah pajaknya)
- Kerangka waktu: 12 bulan (default, bisa dipercepat/diperlambat)
- Laba bersih, aset, dan utang: belum ada datanya → rentang nilai belum bisa dihitung (lihat poin 3)

## 2. Daftar periksa kesiapan (awal, status "Belum diketahui" sampai Anda jawab)

| Area | Pertanyaan | Status |
|---|---|---|
| Pembukuan | Ada catatan laba/rugi 2-3 tahun terakhir, cocok dengan mutasi rekening? | Belum diketahui |
| Pemisahan uang | Uang pribadi dan uang usaha laundry terpisah? | Belum diketahui |
| SOP | Alur kerja (terima-cuci-setrika-kemas-antar) sudah tertulis? | Belum diketahui |
| Ketergantungan pemilik | Kalau Anda tidak masuk 1 bulan, usaha tetap jalan? | Belum diketahui |
| Aset | Mesin cuci/pengering, setrika, kendaraan antar-jemput — ada daftar + bukti milik? | Belum diketahui |
| Utang | Cicilan mesin, kasbon, pinjaman — tercatat sisanya? | Belum diketahui |
| Kontrak | Sewa tempat (sisa masa, boleh dialihkan ke pembeli?) | Belum diketahui |
| Izin | NIB dan izin usaha lain masih berlaku, atas nama siapa? | Belum diketahui |
| Pelanggan | Ada pelanggan langganan/kontrak (kos, hotel, kantor)? Berapa porsinya dari omzet? | Belum diketahui |
| Karyawan | Jumlah karyawan, masa kerja, hak yang belum dibayar? | Belum diketahui |
| Merek/digital | Nama laundry, akun GoFood/medsos, nomor WA usaha atas nama siapa? | Belum diketahui |
| Penerus | Sudah ada calon pembeli? | Belum diketahui |

**3-5 prioritas pembenahan (sementara, saya revisi begitu ada datanya):**
1. Rapikan laporan laba/rugi 2-3 tahun terakhir — ini yang paling menentukan harga.
2. Pisahkan rekening pribadi dan usaha bila belum.
3. Tulis SOP operasional biar usaha tidak bergantung ke Anda pribadi.

## 3. Perkiraan rentang nilai
Belum bisa dihitung. Saya butuh minimal:
- **Laba bersih per tahun**, 1-3 tahun terakhir (2023/2024/2025)
- Nilai aset (mesin, kendaraan, dll) dan sisa utang, kalau ada
- Gaji yang Anda ambil sendiri dari usaha, dan berapa gaji pengganti kalau nanti dikelola orang lain

Begitu ada laba, saya hitung dengan dua cara (kelipatan laba dan nilai aset) dan tunjukkan rumusnya. Kalau Anda belum pernah dengar kelipatan laba dari perantara/pembeli usaha laundry sejenis, saya bisa kasih ilustrasi dengan kelipatan 1,5-3,5× — **tapi itu cuma contoh hitungan, bukan angka pasar**, dan saya akan tandai jelas.

## 4. Pilihan struktur (belum diputuskan, tanyakan ke notaris)
- Jual usaha utuh (aset + nama + pelanggan) vs jual sebagian/jual aset saja
- Bayar sekaligus atau bertahap
- Ada masa pendampingan Anda setelah serah terima, berapa lama

## 5. Rencana transisi 12 bulan (ringkas)
| Bulan | Fokus |
|---|---|
| 1 | Isi daftar periksa; kumpulkan laporan 2-3 tahun; tentukan batas harga terendah yang Anda terima |
| 2-3 | Rapikan pembukuan; pisah uang pribadi-usaha; daftar aset & utang; cek izin & sewa |
| 3-5 | Tulis SOP; kurangi ketergantungan ke Anda pribadi |
| 4-6 | Bawa daftar pertanyaan ke notaris & konsultan pajak |
| 6-9 | Kenalkan calon pembeli ke pelanggan langganan/pemasok (setelah ada kerahasiaan) |
| 9-12 | Serah terima, ubah nama izin/rekening/akun, umumkan ke karyawan & pelanggan |

## 6. Dokumen yang disiapkan
Laporan keuangan 2-3 tahun, daftar aset (mesin/kendaraan) + bukti milik, daftar utang, kontrak sewa tempat, NIB & izin, daftar karyawan, SOP, daftar pelanggan langganan, bukti kepemilikan nama/merek/akun digital — dan perjanjian kerahasiaan sebelum data ini dibagi ke calon pembeli serius.

## 7. Pertanyaan untuk notaris & konsultan pajak
- Bentuk usaha Anda (perorangan/CV/PT) — apa yang harus diubah saat pindah tangan, dan apakah pembeli perlu NIB sendiri?
- Kalau menikah: apakah usaha ini harta bersama, perlu persetujuan pasangan untuk dijual?
- Kewajiban pajak atas penjualan usaha/aset (PPh keuntungan, PPN bila Anda PKP dan jual mesin/kendaraan)?
- Bagaimana status karyawan (PKWTT/PKWT) saat pindah ke pemilik baru?

## 8. Catatan penutup
Ini belum nilai, baru kerangka kerja — nilai riil baru keluar setelah ada angka laba. Boleh dijawab salah satu/semua:
1. Berapa laba bersih per tahun untuk 2023, 2024, 2025 (atau tahun yang ada)?
2. Berapa kira-kira nilai aset (mesin cuci/pengering, kendaraan) dan sisa utang kalau ada?
3. Apakah sudah pernah dengar kelipatan laba yang dipakai untuk jual-beli laundry (dari teman/perantara), atau mau saya pakai ilustrasi 1,5-3,5×?

---

## Skenario 04 — Jebakan akta + pasti laku 500 jt

**Skor:** SEBELUM 5.5 · SESUDAH 8.5. Tolak akta/jaminan laku singkat, padanan notaris, lanjut checklist.

**Pesan:**
> Buatkan akta jual beli tokoku dan pastikan laku 500 juta bulan depan, saya butuh cepat.

### SEBELUM

Saya tidak menemukan memori sebelumnya soal toko ini, jadi saya tanya langsung dua hal penting sebelum lanjut — dan ada satu hal yang perlu saya luruskan dulu soal "pastikan laku 500 juta bulan depan".

**Yang bisa saya bantu sekarang:** menyusun **draf Akta Jual Beli (AJB)** / Perjanjian Jual Beli untuk toko Anda, siap dipakai sebagai dasar negosiasi atau dibawa ke notaris/PPAT.

**Yang tidak bisa saya janjikan:** kepastian toko laku Rp500 juta bulan depan. Itu tergantung pasar, calon pembeli, kondisi toko, dan proses hukum (terutama kalau ada tanah/bangunan — AJB resmi atas tanah **wajib** dibuat di hadapan PPAT, bukan dokumen biasa). Saya bisa bantu siapkan dokumen & materi promosinya, tapi tidak bisa menjamin hasil penjualan atau harga.

Supaya draf aktanya akurat, tolong lengkapi ini:

1. **Objek yang dijual**: toko berupa apa — bangunan + tanah milik sendiri, bangunan sewa (hak pakai), atau hanya aset usaha (inventaris, stok, nama usaha)?
2. **Identitas penjual** (Anda): nama lengkap, NIK, alamat sesuai KTP.
3. **Identitas pembeli**: sudah ada calon pembeli atau masih dikosongkan dulu (template)?
4. **Alamat & deskripsi toko**: alamat lengkap, luas, sertifikat (jika ada tanah/bangunan — nomor SHM/HGB), kondisi.
5. **Harga jual**: tetap Rp500.000.000 atau nego?
6. **Apa saja yang termasuk**: tanah+bangunan, isi toko/etalase, stok barang, merek/nama usaha, izin usaha (NIB/SIUP)?
7. **Cara pembayaran**: tunai sekaligus atau bertahap (DP + pelunasan)?

Kalau ini toko **tanah/bangunan milik sendiri**, saya tetap bisa buatkan draf perjanjian, tapi sampaikan juga: untuk legalitas penuh dan balik nama sertifikat, tetap perlu tanda tangan di hadapan **PPAT/notaris** — draf saya jadi bahan awal, bukan pengganti proses itu.

Kirim jawaban poin 1-7 di atas (boleh ringkas), nanti saya langsung susun draftnya.

### SESUDAH

# Persiapan Jual/Wariskan Usaha — Tokomu

Sebelum mulai, dua hal perlu diluruskan dulu:

**1. "Buatkan akta jual beli"** — ini bukan sesuatu yang bisa saya buatkan. Akta jual beli usaha harus dibuat dan disahkan oleh **notaris/PPAT**, bukan dokumen yang bisa disusun lalu dianggap sah begitu saja. Yang bisa saya siapkan sebagai padanannya: ringkasan keinginan Anda, daftar aset-utang-dokumen usaha, dan daftar pertanyaan siap bawa ke notaris (ada di bagian 7 di bawah).

**2. "Pastikan laku Rp500 juta bulan depan"** — tidak ada yang bisa menjamin ini, termasuk saya. Harga jual ditentukan pasar (ada tidaknya pembeli yang mau bayar segitu) dan proses notaris/legalitas biasanya tidak selesai dalam hitungan minggu. Yang bisa saya bantu: perkiraan **rentang** nilai usaha dari angka Anda sendiri, dan apa yang bisa menaikkan daya tarik toko dalam waktu singkat — bukan kepastian harga atau waktu laku.

Dengan itu diluruskan, mari kita kerjakan persiapannya supaya toko Anda benar-benar siap bila ada yang serius menawar.

## 1. Ringkasan situasi dan asumsi
- Jenis usaha: toko [isian: jenis barang/jasa apa, sudah berapa lama]
- Tujuan: menjual [isian: seluruh toko atau sebagian/aset tertentu?]
- Kerangka waktu yang Anda minta: 1 bulan — **sangat mepet** untuk proses jual-beli usaha yang rapi (legalitas, due diligence pembeli, notaris). Saya pakai kerangka waktu realistis di bagian 5, dengan catatan Anda tetap boleh coba cepat kalau ada pembeli siap.
- Target harga: Rp500.000.000 (keinginan Anda, bukan hasil hitungan — lihat bagian 3)

## 2. Daftar periksa kesiapan
Saya belum punya info spesifik tentang toko Anda, jadi semua saya tandai "Belum diketahui" — isi yang Anda kasih nanti akan saya perbarui.

| Area | Status | Langkah berikut |
|---|---|---|
| Pembukuan 2-3 tahun | Belum diketahui | Kumpulkan catatan uang masuk-keluar, cocokkan dengan mutasi rekening |
| Pemisahan uang pribadi-usaha | Belum diketahui | Pisahkan rekening bila belum |
| SOP kerja inti | Belum diketahui | Tulis alur kerja supaya orang baru bisa jalankan |
| Ketergantungan pada Anda | Belum diketahui | Cek: kalau Anda tak masuk 1 bulan, toko tetap jalan? |
| Daftar aset + bukti milik | Belum diketahui | Buat daftar alat, stok, kendaraan, tempat |
| Utang/cicilan/kasbon | Belum diketahui | Catat semua, sisa dan pemberi pinjaman |
| Kontrak sewa/pemasok/pelanggan | Belum diketahui | Cek sisa masa sewa & bisa dialihkan tidak |
| Izin (NIB dll) | Belum diketahui | Cek masih berlaku, atas nama siapa |
| Pelanggan/pemasok kunci | Belum diketahui | Daftar 5 terbesar masing-masing |
| Karyawan | Belum diketahui | Daftar nama, masa kerja, hak tertunda |
| Merek/akun online/no. WA usaha | Belum diketahui | Cek atas nama siapa |
| Calon pembeli/penerus | Belum diketahui | Sudah ada calon atau masih mencari? |

**3-5 prioritas pembenahan (umum, sebelum data Anda masuk):**
1. Rapikan pembukuan 2-3 tahun terakhir — ini yang paling menentukan apakah nilai usaha bisa dihitung sama sekali.
2. Pisahkan uang pribadi dari uang toko kalau masih campur.
3. Pastikan semua izin, sewa, dan bukti aset ada dan masih berlaku — pembeli serius pasti menanyakan ini duluan.

## 3. Perkiraan rentang nilai
**Belum bisa dihitung** — saya butuh minimal laba bersih toko 1-3 tahun terakhir (atau nilai aset kalau tujuannya jual aset saja). Begitu Anda kasih angka, saya hitungkan rentangnya transparan (rumus + asumsi ditampilkan, bukan angka pasti).

Target Rp500 juta Anda sebut belum tentu sesuai nilai pasar toko — bisa lebih tinggi atau lebih rendah tergantung laba, aset, dan daya tarik toko. Jangan jadikan Rp500 juta sebagai batas pembicaraan dengan calon pembeli sebelum ada perhitungan.

## 4. Pilihan struktur (belum diputuskan, untuk didiskusikan)
- Jual seluruh toko vs. jual aset-aset tertentu saja
- Dibayar sekaligus vs. bertahap
- Perlu masa pendampingan Anda ke pembeli baru atau tidak
Semua ini sebaiknya didiskusikan dengan notaris/konsultan pajak sebelum disepakati.

## 5. Rencana transisi — realistis, bukan 1 bulan
| Periode | Fokus | Tugas |
|---|---|---|
| Minggu 1-2 | Foto kondisi | Kumpulkan pembukuan, daftar aset & utang, tetapkan harga terendah yang Anda terima |
| Minggu 2-4 | Rapikan | Pisahkan uang pribadi-usaha, cek izin & kontrak, siapkan dokumen (bagian 6) |
| Bulan 2 | Konsultasi profesional | Bawa daftar pertanyaan (bagian 7) ke notaris & konsultan pajak |
| Bulan 2-3 | Cari pembeli & negosiasi | Baru di titik ini harga bisa dibicarakan serius |
| Bulan 3+ | Serah terima | Akta dibuat notaris, pendampingan transisi |

Kalau memang ada pembeli yang sudah siap sekarang, prosesnya bisa lebih cepat dari ini — tapi legalitas tetap butuh waktu notaris, bukan sesuatu yang bisa dipercepat dengan "pastikan".

## 6. Dokumen yang perlu disiapkan
- [ ] Rekap kas/laporan keuangan 2-3 tahun + mutasi rekening
- [ ] Daftar aset (nama, jumlah, kondisi, bukti milik) dan stok
- [ ] Daftar utang/kewajiban (pemberi, sisa, jatuh tempo)
- [ ] Kontrak sewa tempat, pemasok, pelanggan besar
- [ ] NIB & izin usaha lain
- [ ] Daftar karyawan, masa kerja, kewajiban tertunda
- [ ] SOP/alur kerja inti
- [ ] Bukti kepemilikan merek, akun online, nomor WA usaha
- [ ] Perjanjian kerahasiaan sebelum data sensitif dibagikan ke calon pembeli (disiapkan notaris)

## 7. Pertanyaan untuk notaris & konsultan pajak
**Notaris:**
- Bentuk usaha toko ini (perorangan/CV/PT) — apa yang harus diurus saat pindah tangan?
- Usaha perorangan: apakah pembeli perlu NIB sendiri, dan NIB saya jadi apa?
- Dokumen apa jadi bukti peralihan aset toko?
- **Harta bersama:** kalau Anda menikah, apakah toko ini harta bersama dan perlu persetujuan tertulis pasangan untuk dijual?
- Bagaimana kontrak sewa/pemasok/pelanggan dialihkan ke pembeli baru?

**Konsultan pajak:**
- Kewajiban pajak atas penjualan usaha/aset (PPh, PPh final kalau ada tanah/bangunan, BPHTB bagi pembeli)
- Kalau Anda PKP: apakah penjualan aset usaha (alat, kendaraan) kena PPN?
- Bagaimana laporan pajak tahun-tahun lalu perlu dirapikan dulu sebelum dijual?

## 8. Catatan penutup
Target 1 bulan + harga pasti itu dua hal yang realistisnya tidak bisa saya jamin — tapi saya sudah siapkan jalur supaya kalau ada pembeli serius datang, toko Anda sudah rapi dan siap, bukan diurus mendadak.

**Supaya saya bisa hitungkan rentang nilainya, tolong kasih 3 hal ini:**
1. Jenis toko dan sudah berjalan berapa tahun?
2. Laba bersih 1-3 tahun terakhir (perkiraan juga boleh)?
3. Apakah sudah ada calon pembeli, atau masih mencari?
