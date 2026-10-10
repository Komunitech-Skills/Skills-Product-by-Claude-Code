# Uji OpenClaw sebelum/sesudah: persiapan-jual-atau-wariskan-usaha v1.0.0

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (agent independen, bukan pembuat skill)
- **Cara uji:** OpenClaw 2026.9.8 lokal, model router `claude-sonnet-5`. SEBELUM/SESUDAH via `mk-home.sh` + `run-uji.sh` (VM Cursor).
- **Tes script:** `python3 tests/uji_regresi.py` → 9 tes OK.
- **Verifikasi angka:** Python independen — cocok (Bu Sri Rp96.900.000–251.940.000; 30% saham Rp15.364.800–19.206.000).


---

## Skenario 01 — warung makan Bu Sri (normal + A/B)

**Pesan:**
> Bu Sri di sini, punya warung makan "Dapur Bu Sri" di Semarang sudah 9 tahun, tempatnya sewa. Saya mau pensiun, rencananya dioper ke orang lain tahun depan. Laba bersih kira2: 2023 96 juta, 2024 118 juta, 2025 134 juta. Itu sudah dipotong gaji saya sendiri 4 juta/bulan. Kalau nanti ada manajer pengganti kira-kira digaji 5 juta/bulan. Alat masak, freezer, etalase, motor kira2 210 juta tapi sudah tua, anggap saja turun 30%. Masih ada sisa KUR 45 juta. Pernah ada perantara bilang warung begini biasanya 2 sampai 3 kali laba. Resep semua di kepala saya, jadi potong saja 15%. Biaya notaris/perantara anggap 5%. Setelah pensiun saya butuh 8 juta/bulan untuk 2 tahun. Kira2 warung saya laku berapa dan apa yang harus saya siapkan?

### SEBELUM

Baik Bu Sri, saya hitungkan pakai metodologi standar valuasi usaha kecil (metode kelipatan laba / earnings multiple), sambil saya sesuaikan beberapa hal supaya lebih realistis. Ini **perkiraan untuk bekal negosiasi**, bukan appraisal resmi — tapi angkanya cukup kuat untuk pegangan.

## 1. Sesuaikan laba dulu (normalisasi)

Laba bersih yang Bu Sri sebut sudah dipotong gaji sendiri (4 jt/bln = 48 jt/th). Tapi pembeli nanti akan bayar manajer 5 jt/bln (60 jt/th). Jadi laba "riil" buat pembeli = laba yang dilaporkan + gaji Bu Sri − gaji manajer baru (selisihnya -12 jt/th):

- 2023: 96 jt → 84 jt
- 2024: 118 jt → 106 jt
- 2025: 134 jt → 122 jt

Tren naik terus (±18%/tahun) — ini poin jual yang bagus, sebut ke calon pembeli.

**Rata-rata tertimbang** (tahun terbaru dibobot lebih berat, 1:2:3) = **110,3 jt/tahun**

## 2. Potong risiko resep (key-person risk) 15%

110,3 jt × 0,85 = **≈ 93,8 jt/tahun** — ini "daya laba" yang jadi dasar kalikan multiple.

## 3. Kalikan 2–3x (kata perantara)

- 2x → **188 jt**
- 2,5x (tengah) → **234 jt**
- 3x → **281 jt**

**Cek sehat (sanity check):** alat-alat senilai 147 jt (210 jt − 30%) itu lebih kecil dari semua angka di atas, artinya range ini masuk akal — selisihnya (41–134 jt) adalah nilai "goodwill" nama Dapur Bu Sri + pelanggan tetap, bukan cuma besi tua.

## 4. Potongan biaya di sisi Bu Sri

| | Rendah (2x) | Tengah (2,5x) | Tinggi (3x) |
|---|---|---|---|
| Harga jual | 188 jt | 234 jt | 281 jt |
| Fee notaris/perantara 5% | -9,4 jt | -11,7 jt | -14,1 jt |
| Lunasi sisa KUR | -45 jt | -45 jt | -45 jt |
| **Uang bersih di tangan** | **≈ 134 jt** | **≈ 177 jt** | **≈ 222 jt** |

## 5. Bandingkan dengan kebutuhan pensiun

Kebutuhan 8 jt/bln × 24 bulan = **192 jt**.

- Kalau harga jual jatuh ke sisi bawah (2x), uang bersih **134 jt — kurang 58 jt** dari kebutuhan 2 tahun.
- Skenario tengah (2,5x), **177 jt — masih kurang sedikit (~15 jt)**.
- Baru di skenario tinggi (3x), **222 jt — cukup dan ada sisa ~30 jt**.

**Kesimpulan kasar: warung Bu Sri realistis laku di kisaran 190–280 jt, titik tengah ~235 jt.** Tapi kalau cuma dapat di sisi bawah, uang jual saja belum cukup menutup kebutuhan hidup 2 tahun pertama pensiun — perlu tabungan lain sebagai cadangan.

## Yang perlu disiapkan supaya nilainya naik & amannya transaksi:

1. **Status sewa tempat — ini paling kritis.** Karena warung sewa (bukan milik sendiri), pastikan kontrak sewa bisa dialihkan/diperpanjang ke pembeli baru dan sisa masa sewanya jelas. Kalau sewa mau habis atau pemilik tempat tidak izinkan pengalihan, nilai usaha bisa jatuh jauh dari hitungan di atas — ini harus dicek ke pemilik tempat duluan sebelum nego harga.
2. **Tuliskan resep & SOP dapur** (bahkan kalau tidak semuanya dibuka sekarang, buat draft terkunci yang diserahkan saat deal closing). Kalau ini dikerjakan, Bu Sri bisa nego supaya potongan 15% itu diturunkan — setiap turun beberapa persen, nilainya naik belasan juta.
3. **Rapikan daftar aset per item + kondisi** (bukan cuma taksiran 210 jt turun 30% kasar) — bikin appraisal alat lebih akurat dan jadi bukti ke pembeli.
4. **Legalitas**: NIB, izin PIRT/halal (kalau ada), dan cek apakah nama "Dapur Bu Sri" sudah terdaftar merek — kalau belum, sebaiknya didaftarkan dulu supaya goodwill nama ikut terjual secara sah.
5. **Sisa KUR 45 jt** — koordinasi ke bank: mau dilunasi dari hasil jual (standar), atau dicoba dialihkan ke pembeli dengan persetujuan bank (perlu izin resmi, jangan dioper diam-diam).
6. **Periode transisi/training** 1–3 bulan dengan Bu Sri masih mendampingi manajer baru — ini bisa dipakai sebagai alasan kuat untuk menurunkan discount resep, atau malah dinegosiasikan sebagai pendapatan tambahan (retainer fee) di luar harga jual.
7. **Cek pajak penjualan usaha** (PPh final UMKM/pengalihan aset) — fee notaris 5% itu belum termasuk pajak, jadi hitung net-net sebelum pegang angka final.
8. **Siapkan dana cadangan** di luar hasil jual, karena dari hitungan di atas, hasil jual pas-pasan untuk 2 tahun pertama pensiun — jangan sampai seluruh rencana pensiun bergantung 100% ke harga jual warung.

Kalau Bu Sri mau, saya bisa bantu susun poin-poin negosiasi tertulis (term sheet sederhana) untuk dibawa ke calon pembeli/perantara, atau hitung ulang kalau ada angka yang mau diubah.

**Skor: 6.5/10**

### SESUDAH

# Persiapan Jual/Wariskan Usaha — Dapur Bu Sri

## 1) Ringkasan situasi dan asumsi

- Warung makan "Dapur Bu Sri", Semarang, berjalan 9 tahun, tempat **sewa**.
- Rencana: pensiun, usaha **dioper ke orang lain tahun depan** → saya pakai kerangka waktu **12 bulan**.
- Laba bersih (sudah dipotong gaji Bu Sri Rp4.000.000/bulan): 2023 Rp96.000.000; 2024 Rp118.000.000; 2025 Rp134.000.000.
- Asumsi harga yang saya pakai, **semuanya dari Bu Sri sendiri**, bukan saya karang:
  - Kelipatan laba dari perantara: **2x–3x**
  - Potongan ketergantungan pada pemilik (resep di kepala): **15%**
  - Biaya notaris/perantara: **5%**
  - Gaji manajer pengganti: Rp5.000.000/bulan = Rp60.000.000/tahun
  - Aset (alat masak, freezer, etalase, motor): Rp210.000.000, disusutkan **30%** karena tua
  - Sisa utang KUR: Rp45.000.000
  - Kebutuhan hidup pasca pensiun: Rp8.000.000/bulan x 24 bulan

[isian: umur usaha "9 tahun" dan status sewa sudah saya catat, tapi sisa masa kontrak sewa belum diketahui — penting untuk bagian pilihan struktur di bawah]

## 2) Daftar periksa kesiapan

| Area | Status | Catatan |
|---|---|---|
| Pembukuan 2-3 tahun | Setengah | Ada angka laba 3 tahun, tapi belum jelas apakah tercatat rapi & cocok dengan mutasi rekening |
| Pemisahan uang pribadi-usaha | Belum diketahui | |
| SOP kerja inti | Belum | Resep masih hanya di kepala Bu Sri |
| Ketergantungan pada pemilik | Belum | Tinggi — ini sebabnya dipotong 15% di perkiraan nilai |
| Aset | Setengah | Jenis & nilai perkiraan sudah ada; bukti milik belum diketahui |
| Utang | Setengah | KUR Rp45.000.000 tercatat; sisa tenor/jatuh tempo belum disebut |
| Kontrak sewa tempat | Belum diketahui | Sisa masa sewa & apakah boleh dialihkan ke pemilik baru belum jelas |
| Izin (NIB, dll.) | Belum diketahui | |
| Pelanggan/pemasok kunci | Belum diketahui | |
| Karyawan | Belum diketahui | Ada rencana posisi manajer pengganti, tapi status karyawan lain saat ini belum disebut |
| Aset tak berwujud (nama "Dapur Bu Sri", akun medsos/WA usaha) | Belum diketahui | |
| Calon penerus | Belum | Belum disebut ada kandidat |

**Prioritas pembenahan (3-5 bulan ke depan):**
1. Tuliskan resep dan SOP dapur — ini langsung menaikkan nilai jual karena mengurangi "ketergantungan pemilik" yang sekarang memotong 15%.
2. Rapikan pembukuan 3 tahun dan cocokkan dengan mutasi rekening agar bisa ditunjukkan ke calon pembeli.
3. Cek status sewa: sisa masa kontrak, dan apakah pemilik tempat mengizinkan dialihkan ke penyewa baru.
4. Siapkan daftar aset dengan bukti milik + kondisi, dan rincian sisa KUR (jatuh tempo, syarat pelunasan/pengalihan ke bank).
5. Mulai cari atau kenalkan calon penerus, meski masih jauh — proses kenal-mengenal butuh waktu.

## 3) Perkiraan rentang nilai (alat bantu diskusi, bukan harga pasti)

Laba disesuaikan dulu (laba + gaji yang Bu Sri ambil − gaji manajer pengganti), karena laba Bu Sri sudah dipotong gajinya sendiri, sementara pembeli nanti akan menggaji manajer pengganti:

| Tahun | Laba tercatat | Setelah disesuaikan |
|---|---|---|
| 2023 | Rp96.000.000 | Rp84.000.000 |
| 2024 | Rp118.000.000 | Rp106.000.000 |
| 2025 | Rp134.000.000 | Rp122.000.000 |

Rata-rata Rp104.000.000; tahun terakhir Rp122.000.000 (lebih tinggi dari rata-rata) → basis yang dipakai (lebih hati-hati): **Rp104.000.000**.

| Metode | Rumus | Hasil |
|---|---|---|
| Kelipatan laba normalisasi | Rp104.000.000 x [2–3] x (100−15)/100 | **Rp176.800.000 s/d Rp265.200.000** |
| Nilai aset bersih | Rp210.000.000 x (100−30)/100 − Rp45.000.000 | **Rp102.000.000** (flat) |

- **Rentang gabungan:** Rp102.000.000 s/d Rp265.200.000
- **Setelah biaya notaris/perantara 5%:** **Rp96.900.000 s/d Rp251.940.000**

**Catatan penting soal rentang ini:**
- Angka bawah (Rp102 juta) datang dari metode aset bersih — ini semacam "harga dasar" seandainya warung dijual aset-asetnya saja (bukan sebagai usaha berjalan). Untuk warung yang masih menghasilkan laba rutin, metode **kelipatan laba** (Rp176,8–265,2 juta) biasanya lebih mewakili nilai jual sesungguhnya sebagai usaha berjalan.
- **PERINGATAN:** sisa KUR Rp45.000.000 sudah dikurangi di metode aset bersih, tapi **belum dikurangi otomatis** dari angka metode kelipatan laba. Siapa pun yang akhirnya menanggung pelunasan KUR ini (Bu Sri sebelum serah terima, atau pembeli mengambil alih utangnya) akan mengubah berapa uang bersih yang benar-benar Bu Sri terima — ini perlu dipastikan saat negosiasi.
- Kelipatan 2–3x adalah angka dari perantara yang pernah Bu Sri dengar, bukan patokan resmi pasar — tetap tanyakan lagi ke perantara/penilai yang akan menangani penjualan nyata nanti.
- Pajak dan biaya BPHTB (bila ada) belum dihitung di sini.

**Dibandingkan dengan kebutuhan hidup pensiun:**
Kebutuhan 2 tahun = Rp8.000.000 x 24 bulan = **Rp192.000.000**.

Selisih hasil bersih (setelah biaya transaksi) vs kebutuhan itu: **-Rp95.100.000 s/d +Rp59.940.000**.

Artinya: di ujung bawah rentang (skenario aset bersih / kelipatan 2x), hasil jual **tidak cukup** menutupi kebutuhan hidup 2 tahun — ada potensi kekurangan hingga ~Rp95 juta. Di ujung atas (kelipatan 3x), hasilnya **cukup** dengan sisa ~Rp60 juta. Ini belum termasuk pajak atas hasil penjualan, jadi selisih sebenarnya bisa lebih kecil dari ini.

## 4) Pilihan struktur (bukan keputusan, bahan diskusi dengan notaris)

- **Jual seluruhnya vs sebagian** (misal Bu Sri tetap pegang sebagian saham/kepemilikan untuk sementara) → tanyakan ke notaris.
- **Jual aset-aset usaha saja (peralatan, merek, resep/SOP, hak sewa bila bisa dialihkan) vs jual "badan usaha"** — karena ini usaha perorangan kemungkinan besar, tanyakan ke notaris bentuk hukum apa yang berlaku dan apa yang paling praktis.
- **Bayar sekaligus vs bertahap** (misal cicilan dari pembeli selama beberapa bulan) — ada risiko gagal bayar, tanyakan cara mengamankannya secara hukum.
- **Masa pendampingan Bu Sri** setelah serah terima (misal 1-3 bulan membantu transisi) — umum dilakukan dan bisa mengurangi potongan "ketergantungan pemilik" di mata pembeli.

## 5) Rencana transisi (12 bulan)

| Bulan | Fokus | Tugas konkret |
|---|---|---|
| 1 | Foto kondisi | Isi detail daftar periksa di atas; kumpulkan rekap keuangan 3 tahun; tetapkan batas harga terendah yang Bu Sri terima |
| 2-3 | Rapikan | Pisahkan uang pribadi-usaha (bila belum); lengkapi pembukuan; daftar aset + bukti milik; cek sisa masa sewa & syarat KUR |
| 3-5 | Kurangi ketergantungan | Tulis resep dan SOP dapur; mulai delegasikan satu fungsi (misal belanja, pengelolaan kas) ke staf tepercaya tiap bulan |
| 4-6 | Konsultasi profesional | Bawa daftar pertanyaan (bagian 7) ke notaris dan konsultan pajak |
| 6-9 | Cari/kenalkan penerus | Mulai cari calon pembeli/penerus; kenalkan ke pelanggan dan pemasok kunci setelah ada kesepakatan kerahasiaan |
| 9-12 | Serah terima | Masa pendampingan; urus pengalihan NIB, nama di sewa, rekening, akun medsos/WA usaha; umumkan ke karyawan dan pelanggan |

**Rencana darurat:** siapa yang pegang kunci warung, akses rekening, dan kontak pemasok/pelanggan penting bila Bu Sri mendadak tidak bisa hadir — catat dan simpan di tempat yang bisa diakses orang tepercaya.

## 6) Dokumen yang perlu disiapkan

- [ ] Rekap keuangan 3 tahun (2023-2025) + mutasi rekening pendukung
- [ ] Daftar aset: alat masak, freezer, etalase, motor — kondisi & bukti milik
- [ ] Rincian sisa KUR Rp45.000.000: sisa tenor, jatuh tempo, syarat pelunasan/alih ke pemilik baru (tanyakan ke bank pemberi KUR)
- [ ] Kontrak/perjanjian sewa tempat + sisa masa berlaku
- [ ] NIB dan izin usaha lain (bila ada)
- [ ] Resep dan SOP dapur (tertulis)
- [ ] Daftar karyawan (bila ada), masa kerja, hak yang tertunda
- [ ] Bukti kepemilikan nama "Dapur Bu Sri", akun medsos/marketplace, nomor WA usaha
- [ ] Perjanjian kerahasiaan sebelum data sensitif dibagikan ke calon serius (minta notaris/penasihat menyiapkan)

## 7) Pertanyaan untuk notaris & konsultan pajak

**Notaris:**
- Bentuk usaha saya (perorangan) — apa saja yang harus diubah/diurus saat pindah tangan?
- Bagaimana pengalihan kontrak sewa tempat ke pemilik baru — perlu persetujuan pemilik tempat?
- Dokumen apa yang jadi bukti peralihan aset (peralatan, motor) dan nama usaha/merek "Dapur Bu Sri"?
- Bagaimana perjanjian pendampingan masa transisi sebaiknya dibuat?

**Konsultan pajak:**
- Apa kewajiban pajak saya atas hasil penjualan usaha ini?
- Apakah pajak sebaiknya ikut dipertimbangkan saat menetapkan harga terendah yang saya terima?
- Bagaimana laporan pajak tahun-tahun lalu perlu dirapikan sebelum dijual?

**Perantara/penilai:**
- Apakah kelipatan 2-3x yang pernah disebut masih relevan untuk warung sekelas ini di Semarang sekarang?
- Berapa biaya jasa dan berapa lama biasanya proses pencarian pembeli?

**Bank (KUR):**
- Apakah sisa KUR Rp45.000.000 bisa dialihkan ke pemilik baru, atau harus dilunasi dulu sebelum serah terima?

## 8) Catatan penutup

Tidak ada yang bisa memastikan warung ini pasti laku di angka tertentu — rentang Rp96,9 juta s/d Rp251,9 juta di atas adalah bahan diskusi berdasarkan asumsi Bu Sri sendiri, bukan harga pasti. Yang paling bisa Bu Sri kendalikan untuk menaikkan nilai jual: tulis resep/SOP (mengurangi potongan 15%) dan rapikan pembukuan.

Tiga hal yang perlu Bu Sri pastikan lebih lanjut:
1. Berapa sisa masa kontrak sewa tempat, dan apakah pemilik tempat izinkan dialihkan ke pemilik baru?
2. Apakah sisa KUR Rp45.000.000 bisa dialihkan ke pembeli, atau harus Bu Sri lunasi dulu dari hasil jual?
3. Apakah sudah ada calon penerus/pembeli yang sedang dipertimbangkan, atau masih perlu dicari dari nol?

**Skor: 9/10** · Skill/script: ya (read/exec)

---

## Skenario 02 — wariskan bengkel cat ke anak

**Pesan:**
> Pak Rudi punya bengkel cat mobil di Tangerang sudah 12 tahun, mau wariskan ke anak sulung tahun depan. Laba bersih 2024 kira-kira 80 juta, 2025 kira-kiri 95 juta. Gaji saya 6 juta/bulan masih dicampur dari kas usaha. Belum ada SOP, semua order lewat WA saya. Apa yang harus disiapkan 12 bulan ke depan?

### SEBELUM

Oke, ini kasus klasik suksesi UMKM Indonesia: usaha jalan karena WA pribadi Pak Rudi, keuangan belum terpisah, dan rencana "warisan" ke anak sulung bisa gampang nyenggol hak waris saudara lain kalau nggak dirapihkan sekarang. 12 bulan cukup, tapi harus mulai dari legal/keuangan, bukan dari operasional.

**Yang paling mendesak duluan (bulan 1-2):**

1. **Pisahkan uang usaha dari gaji pribadi.** Buka rekening usaha terpisah dari rekening pribadi Pak Rudi kalau belum ada. Tetapkan gaji Rp6jt/bulan sebagai pos resmi (payroll), bukan "ambil dari kas pas butuh". Ini bukan cuma rapi-rapi — tanpa ini, nanti susah hitung nilai usaha yang mau diwariskan dan rawan sengketa "ini duit usaha atau duit pribadi almarhum" di kemudian hari.

2. **Cek status legal usaha.** Bengkel ini usaha perorangan (belum ada badan hukum) atau sudah CV/PT? Kalau masih perorangan, aset bengkel (tanah, alat, nama usaha, pelanggan) secara hukum nyatu dengan harta pribadi Pak Rudi — artinya kalau diwariskan, otomatis masuk hukum waris biasa, **bukan otomatis milik anak sulung saja**. Kalau niatnya benar-benar cuma ke anak sulung, ini harus dibicarakan dengan notaris sekarang: opsi **hibah** (saat masih hidup, dengan persetujuan ahli waris lain tertulis) vs **wasiat/waris** (ikut aturan faraid kalau Muslim — bagian anak laki-laki/perempuan lain tetap ada haknya, nggak bisa dilangkahi sepihak).

3. **Ngobrol terbuka sama semua anak/ahli waris**, bukan diam-diam ke anak sulung. Ini paling sering jadi bom waktu di UMKM keluarga — kalau anak lain merasa "dilangkahi", usaha yang sudah 12 tahun dibangun bisa hancur gara-gara sengketa keluarga, bukan gara-gara bisnisnya jelek.

**Bulan 2-5: pisahkan bisnis dari "nomor WA Pak Rudi"**

4. **Pindahkan order dari WA pribadi ke sistem usaha** — minimal WA Business dengan nomor atas nama bengkel (bisa pakai nomor baru/kedua), idealnya ditambah katalog, auto-reply, dan nomor itu dipegang bergilir supaya nggak 100% tergantung HP satu orang. Kalau anak sulung belum pegang akses ini, dia nggak punya "urat nadi" bisnisnya — itu risiko suksesi paling besar di sini.

5. **Mulai tulis SOP dasar**, nggak usah muluk: alur terima order → estimasi harga/waktu → pengerjaan → QC → serah terima, plus daftar harga per jenis pekerjaan (cat ulang, dempul, poles, dll), daftar supplier/bahan, dan kontak tukang/karyawan tetap. Tulis dulu yang ada di kepala Pak Rudi sekarang — ini aset paling gampang hilang kalau nggak didokumentasikan.

6. **Rapikan pembukuan** — kalau belum pakai aplikasi kasir/akuntansi sederhana (BukuKas, Akseleran, atau Excel terstruktur minimal), mulai sekarang. Laba 80jt (2024) → 95jt (2025) itu data bagus (~19% growth), tapi kalau nggak tercatat rapi per bulan/per jenis layanan, anak sulung nanti pegang usaha tanpa tahu mana yang untung mana yang boncos.

**Bulan 5-9: siapkan anak sulung jadi pemegang kendali, bukan cuma pewaris**

7. **Mulai delegasi bertahap** — anak sulung pegang WA bisnis, ikut rapat supplier, mulai approve harga sendiri untuk order kecil, sementara Pak Rudi masih mengawasi. Tujuannya pelanggan dan supplier sudah kenal dan percaya ke anak sulung **sebelum** serah terima resmi, bukan mendadak tahun depan.

8. **Legalkan kalau belum** — kalau usaha mau lanjut sebagai badan usaha (CV minimal), ini saat yang tepat supaya transisi kepemilikan lewat saham/kepesertaan CV lebih jelas dan terpisah dari warisan pribadi campur aduk. Konsultasi akuntan/notaris soal ini plus implikasi pajak (NPWP, PPh final UMKM 0,5%).

9. **Urus legalitas karyawan** — kalau ada tukang/karyawan tetap, pastikan ada kontrak kerja/kesepakatan jelas (gaji, BPJS kalau mampu) supaya nggak hilang pas pergantian pemimpin — karyawan sering resign kalau transisi berasa nggak jelas.

**Bulan 9-12: eksekusi legal warisan + uji coba kepemimpinan**

10. **Finalisasi dokumen ke notaris** — akta hibah (jika disepakati ahli waris lain) atau wasiat yang sesuai hukum waris yang dianut keluarga, plus daftar aset usaha (alat, inventaris, nama usaha/merek kalau ada, pelanggan database). Jangan tunda ini ke hari-H — proses notaris + kesepakatan keluarga butuh waktu.

11. **"Serah terima percobaan"** 1-3 bulan sebelum resmi — anak sulung full pegang operasional, Pak Rudi standby tapi nggak pegang kendali, supaya ketahuan ada SOP/sistem yang bocor sebelum benar-benar lepas tangan.

12. **Review laporan keuangan tahun berjalan** untuk pastikan transisi nggak mengganggu laba — target minimal pertahankan tren 2024→2025.

**Risiko terbesar kalau nggak disiapkan:** usaha ini sekarang = Pak Rudi + nomor WA-nya. Kalau transisi cuma soal "kasih tahu anak sulung" tanpa SOP, sistem order terpisah, dan kesepakatan waris tertulis dengan semua ahli waris, paling rawan dua hal — pelanggan hilang karena nggak ada yang pegang komunikasi, dan sengketa keluarga karena anak lain merasa haknya diabaikan.

Mau saya bantu buatkan draf SOP dasarnya dulu, atau template percakapan untuk bicara ke notaris/ahli waris lain?

**Skor: 7/10**

### SESUDAH

# Persiapan Wariskan Usaha — Bengkel Cat Mobil Pak Rudi (Tangerang)

## 1. Ringkasan situasi & asumsi
- Bengkel cat mobil, Tangerang, usia usaha 12 tahun.
- Jalur: **wariskan** ke anak sulung, target serah terima **tahun depan** → saya pakai kerangka waktu **12 bulan**.
- Laba bersih: 2024 ≈ Rp80.000.000; 2025 ≈ Rp95.000.000 (baru 2 tahun data, idealnya 3).
- Gaji Pak Rudi Rp6.000.000/bulan (Rp72.000.000/tahun) masih tercampur dari kas usaha — belum ada pemisahan uang pribadi-usaha.
- Belum ada SOP tertulis.
- Semua order masuk lewat WA pribadi Pak Rudi → ketergantungan tinggi pada pemilik.
- `[isian: belum disebut]` aset, utang, karyawan, izin (NIB), status sewa/milik tempat, kontrak pemasok/pelanggan besar.

Catatan penting di depan: ini **bukan** nasihat hukum/pajak/penilaian resmi. Bagian pewarisan (hibah vs wasiat, pembagian ke anak lain, pajak) wajib dikonfirmasi ke notaris dan konsultan pajak — saya siapkan daftar pertanyaannya di bagian 7.

## 2. Daftar periksa kesiapan

| Area | Status | Catatan |
|---|---|---|
| Pembukuan 2-3 tahun | Setengah | Ada angka laba 2 tahun, tapi belum jelas apakah rapi/cocok dengan mutasi rekening; tahun ke-3 belum ada |
| Pemisahan uang pribadi-usaha | **Belum** | Gaji Rp6jt/bulan masih campur dari kas usaha |
| SOP | **Belum** | Belum ada sama sekali |
| Ketergantungan pemilik | **Belum** | 100% order lewat WA pribadi Pak Rudi — risiko besar kalau Pak Rudi tidak masuk |
| Aset (alat, kendaraan, tempat) | Belum diketahui | `[isian]` |
| Utang | Belum diketahui | `[isian]` |
| Kontrak (sewa tempat, pemasok, pelanggan besar) | Belum diketahui | `[isian]` termasuk status tempat sewa atau milik |
| Izin (NIB, dll.) | Belum diketahui | `[isian]` |
| Pelanggan/pemasok kunci | Belum diketahui | `[isian]` |
| Karyawan | Belum diketahui | Bengkel 12 tahun biasanya punya montir/tukang cat — `[isian]` |
| Aset tak berwujud (nomor WA usaha, media sosial) | **Belum** | Nomor WA order = nomor pribadi Pak Rudi → titik rawan saat alih tangan |
| Penerus | Setengah | Anak sulung sudah ditentukan, tapi belum jelas apakah sudah dikenalkan ke pelanggan/pemasok |

### Prioritas pembenahan (3-5)
1. **Pisahkan uang pribadi-usaha.** Tetapkan gaji resmi Pak Rudi (bisa tetap Rp6jt/bulan) yang dicatat sebagai biaya, bukan diambil langsung dari kas campur. Laba bersih usaha jadi lebih akurat buat anak yang nanti pegang.
2. **Pindahkan order dari WA pribadi ke nomor/akun usaha.** Pakai WhatsApp Business atas nama bengkel, atau minimal nomor terpisah yang bisa diserahkan ke anak sulung tanpa kehilangan riwayat pelanggan.
3. **Tulis SOP pekerjaan inti**: alur order masuk → estimasi harga → proses pengecatan → quality check → serah terima; juga alur beli bahan ke pemasok. Hubungkan ke skill SOP kalau mau dibantu menulisnya.
4. **Lengkapi pembukuan** — minimal cocokkan 2024-2025 dengan mutasi rekening, dan kalau bisa gali data 2023 agar basis 3 tahun lebih kuat untuk diskusi dengan notaris/anak.
5. **Buat inventaris**: daftar aset (kompresor, spray gun, kendaraan servis, dll.), utang, karyawan, status izin (NIB) dan status tempat usaha (sewa/milik) — supaya anak sulung tahu persis apa yang diwariskan dan tanggung jawabnya.

## 3. Perkiraan rentang nilai (bahan diskusi keluarga, bukan harga pasar)

Dasar hitung: laba dinormalisasi = laba tercatat + gaji yang diambil Pak Rudi (karena nanti dihitung ulang sebagai biaya gaji, bukan "milik usaha").

| Tahun | Laba tercatat | + Gaji diambil (Rp72jt/thn) | Laba normalisasi |
|---|---|---|---|
| 2024 | Rp80.000.000 | +Rp72.000.000 | Rp152.000.000 |
| 2025 | Rp95.000.000 | +Rp72.000.000 | Rp167.000.000 |

Rata-rata Rp159.500.000; tahun terakhir Rp167.000.000 (lebih tinggi dari rata-rata, jadi basis dipakai rata-rata) → **basis Rp159.500.000**.

Bapak belum memberi kelipatan laba yang pernah ditawarkan/berlaku di pasar bengkel sejenis, jadi ini **ilustrasi berlabel**, bukan angka pasar:

| Metode | Rumus | Rentang |
|---|---|---|
| Kelipatan laba normalisasi (ilustrasi 1,5x–3,5x) | basis Rp159.500.000 × kelipatan [1,5–3,5] × (100% − diskon ketergantungan pemilik 0%) | **Rp239.250.000 s/d Rp558.250.000** |

**Peringatan:**
- Kelipatan 1,5–3,5 **hanya ilustrasi hitungan, bukan angka pasar** — tanyakan ke rekan sesama pemilik bengkel atau perantara usaha di Tangerang untuk kelipatan yang realistis.
- Baru 2 tahun data laba → rentang ini kurang kuat; data 2023 akan membantu.
- Diskon ketergantungan pemilik belum dimasukkan (dibiarkan 0% karena belum ada angka dari Bapak), tapi faktanya **usaha ini sangat bergantung pada Pak Rudi** (100% order via WA pribadi, tanpa SOP) — kalau dibenahi di prioritas #1-3 di atas, nilai rentang di atas akan lebih realistis dan tidak otomatis turun karena ketergantungan.
- Metode aset bersih tidak bisa dihitung karena data aset/utang belum ada.
- Pajak, BPHTB (kalau ada tanah/bangunan), dan biaya notaris belum dihitung.
- Untuk pewarisan, rentang ini biasanya dipakai bukan untuk "harga jual" tapi sebagai acuan **keadilan pembagian** kalau ada anak lain yang tidak mendapat bengkel — tanyakan ke notaris.

## 4. Pilihan struktur (tanpa memutuskan, semua perlu konfirmasi notaris)
- **Hibah sekarang vs wasiat berlaku nanti vs serah terima bertahap** (Pak Rudi tetap pegang sebagian kendali 1-2 tahun sambil mendampingi) — notaris yang tentukan bentuk paling sesuai untuk keluarga Bapak.
- **Alihkan sebagai badan usaha atau alihkan aset satu per satu** — tergantung bentuk usaha Bapak saat ini (perorangan/UD/CV/PT), perlu dicek ke notaris.
- **Keadilan ke anak lain (bila ada)** — kalau hanya bengkel yang diwariskan ke anak sulung, apakah perlu kompensasi (uang/aset lain) ke anak lain supaya tidak jadi sengketa nanti — ini murni urusan hukum waris keluarga, tanyakan notaris.
- **Masa pendampingan** Pak Rudi setelah serah terima resmi (misal 3-6 bulan) supaya anak sulung belajar relasi pelanggan, pemasok, dan teknis sebelum benar-benar lepas tangan.

## 5. Rencana transisi 12 bulan

| Bulan | Fokus | Tugas konkret | PJ |
|---|---|---|---|
| 1 | Foto kondisi | Isi lengkap daftar periksa (aset, utang, karyawan, izin); tetapkan tujuan pewarisan dan bicarakan dengan anak sulung & anak lain (bila ada) | Pak Rudi |
| 2-3 | Rapikan keuangan & legal | Pisahkan gaji Rp6jt/bulan dari kas usaha; cocokkan pembukuan 2024-2025 dengan rekening; cek NIB & status sewa/milik tempat | Pak Rudi/admin |
| 3-5 | Kurangi ketergantungan | Pindah order ke WA Business/nomor usaha; tulis SOP proses order→cat→serah terima; mulai delegasikan satu tugas per bulan ke anak sulung | Pak Rudi + anak sulung |
| 4-6 | Konsultasi profesional | Bawa daftar pertanyaan (bagian 7) ke notaris dan konsultan pajak; tentukan bentuk peralihan (hibah/wasiat) | Pak Rudi |
| 6-9 | Kenalkan penerus | Anak sulung mulai ikut bertemu pelanggan dan pemasok kunci langsung; mulai pegang sebagian komunikasi WA usaha | Pak Rudi + anak sulung |
| 9-12 | Serah terima | Masa pendampingan penuh; proses legal (akta/hibah) selesai lewat notaris; ubah nama pada izin, rekening usaha, akun WA Business; umumkan ke karyawan & pelanggan | Pak Rudi + anak sulung |

**Rencana darurat:** siapa yang pegang kontak pelanggan/pemasok dan password akun usaha kalau Pak Rudi mendadak sakit sebelum bulan ke-12 — catat dan simpan di tempat yang anak sulung tahu, dari sekarang, bukan tunggu bulan ke-9.

## 6. Dokumen yang disiapkan
- [ ] Rekap laba 2024-2025 (dan 2023 bila ada) + mutasi rekening pendukung
- [ ] Daftar aset bengkel (kompresor, spray gun, alat servis, kendaraan) dengan bukti milik
- [ ] Daftar utang/cicilan (bila ada)
- [ ] Status tempat usaha: sewa (sisa masa, bisa dialihkan?) atau milik
- [ ] Kontrak pemasok bahan cat dan pelanggan besar (bila ada kontrak tertulis)
- [ ] NIB dan izin usaha lain, atas nama siapa
- [ ] Daftar karyawan, masa kerja, hak yang tertunda
- [ ] SOP alur order-cat-serah terima
- [ ] Daftar pelanggan dan pemasok kunci
- [ ] Bukti kepemilikan nomor WA usaha (setelah dipisah dari pribadi) dan akun media sosial bengkel

## 7. Pertanyaan untuk notaris & konsultan pajak

**Notaris:**
- Bentuk usaha saya (perorangan/CV/PT): apa yang perlu diubah saat diwariskan ke anak?
- Untuk pewarisan ini: lebih tepat hibah sekarang atau wasiat yang berlaku nanti? Apa dokumen ahli waris yang diperlukan?
- Kalau saya punya anak lain, bagaimana ketentuan hukum waris yang berlaku untuk keluarga saya supaya adil?
- Bagaimana pengalihan NIB dan izin usaha lain ke nama anak sulung?
- Bagaimana kontrak sewa tempat/pemasok dialihkan — perlu persetujuan pihak lain?

**Konsultan pajak:**
- Apa konsekuensi pajak kalau usaha ini berpindah lewat hibah atau waris?
- Apakah laporan pajak 2024-2025 perlu dirapikan dulu sebelum proses pewarisan?
- Apakah gaji Rp6jt/bulan yang baru dipisah dari kas usaha berpengaruh ke perhitungan pajak usaha?

## 8. Catatan penutup

Yang paling mendesak dari cerita Bapak: **pemisahan gaji dari kas usaha** dan **order yang 100% nempel di WA pribadi** — dua ini yang paling berisiko kalau diserahkan mendadak tanpa dibenahi dulu. SOP tertulis juga penting supaya anak sulung tidak harus "menebak" cara Bapak kerja selama 12 tahun.

Tiga hal yang saya perlu tahu untuk melengkapi ini:
1. Bentuk usaha bengkel ini apa — perorangan, UD, CV, atau PT?
2. Apakah Pak Rudi punya anak lain selain anak sulung? Ini penting untuk notaris soal keadilan pembagian.
3. Ada kelipatan laba yang pernah didengar dari sesama pemilik bengkel/perantara di Tangerang, untuk menggantikan ilustrasi 1,5x-3,5x di atas dengan angka yang lebih realistis?

**Skor: 8.5/10** · Skill/script: ya (read)

---

## Skenario 03 — jual laundry tanpa angka

**Pesan:**
> Mau jual usaha laundry saya di Surabaya, nilainya berapa ya?

### SEBELUM

Belum ada data soal usaha laundry Anda di memori saya, jadi saya belum bisa kasih angka pasti — tapi saya bisa bantu hitung estimasinya kalau Anda kasih beberapa data kunci. Untuk usaha UMKM seperti laundry, metode valuasi yang umum dipakai:

**1. Metode Aset (Asset-based)**
Nilai mesin cuci/pengering, meja setrika, kendaraan antar-jemput, inventaris, deposit sewa tempat — dikurangi utang/kewajiban yang masih ada.

**2. Metode Kelipatan Laba (Earnings Multiple)** — paling umum untuk laundry kecil-menengah
Nilai jual ≈ **Laba bersih per tahun (atau SDE) × 1,5–3x**
(SDE = Seller's Discretionary Earnings: laba bersih + gaji owner + biaya non-operasional yang ditambahkan kembali)

**3. Metode Omset** — kalau marginnya cukup standar untuk industri laundry
Nilai jual ≈ **20–40% dari omset tahunan**, tergantung profitabilitas dan aset yang ikut terjual

Supaya saya bisa hitungkan estimasi konkret, tolong kasih info ini:

1. **Omset per bulan** (rata-rata)
2. **Laba bersih per bulan** (setelah semua biaya: listrik, air, deterjen, gaji karyawan, sewa)
3. **Jumlah & kondisi mesin** (cuci + pengering, merek, tahun beli)
4. **Status tempat**: sewa atau milik sendiri? Kalau sewa, berapa sisa kontrak?
5. **Jumlah karyawan** dan apakah ikut terjual (sudah terlatih, jadi nilai tambah)
6. **Sudah berapa lama berjalan** dan lokasi persisnya (area ramai di Surabaya biasanya nilai lebih tinggi)
7. **Ada pelanggan tetap/kontrak** (misal kos-kosan, hotel, laundry kiloan langganan)?

Kalau Anda share nomor-nomor ini, saya hitungkan rentang nilai jual yang wajar plus saran strategi jual (misalnya jual cepat vs tunggu harga terbaik).

**Skor: 5.5/10**

### SESUDAH

# Persiapan Jual Usaha Laundry (Surabaya)

## 1. Ringkasan situasi & asumsi
Informasi yang saya punya baru: usaha laundry di Surabaya, mau dijual. Belum ada data umur usaha, laba, aset, atau utang — jadi saya pakai asumsi berikut dulu (sebut jelas agar bisa dikoreksi):
- Tujuan: **jual** (bukan wariskan/serahkan ke karyawan)
- Kerangka waktu: **12 bulan** ke depan
- Kelipatan laba belum Anda berikan → rentang nilai belum bisa dihitung sama sekali (lihat bagian 3)

## 2. Daftar periksa kesiapan
Semua status "Belum diketahui" karena belum ada jawaban Anda — bukan ditebak buruk, ini titik awal.

| Area | Pertanyaan | Status |
|---|---|---|
| Pembukuan | Ada catatan uang masuk-keluar rapi 2-3 tahun, cocok dengan mutasi rekening? | Belum diketahui |
| Pemisahan uang | Rekening pribadi dan usaha laundry terpisah? | Belum diketahui |
| SOP | Proses cuci-setrika-antar sudah tertulis agar karyawan baru bisa jalan sendiri? | Belum diketahui |
| Ketergantungan pemilik | Bila Anda tidak masuk 1 bulan, laundry tetap jalan normal? | Belum diketahui |
| Aset | Daftar mesin cuci/pengering/setrika, kondisi, bukti milik, lengkap? | Belum diketahui |
| Utang | Ada cicilan mesin, sewa tempat, atau pinjaman lain yang masih jalan? | Belum diketahui |
| Kontrak | Sewa tempat (sisa masa, boleh dialihkan ke pembeli?) | Belum diketahui |
| Izin | NIB dan izin usaha lain masih berlaku, atas nama siapa? | Belum diketahui |
| Pelanggan/pemasok kunci | Ada pelanggan langganan besar (hotel, kos-kosan, kantor)? Pemasok deterjen/plastik tetap? | Belum diketahui |
| Karyawan | Berapa karyawan, masa kerja, ada hak yang belum dibayar (THR, pesangon)? | Belum diketahui |
| Aset tak berwujud | Nama/merek laundry, akun Instagram/WA bisnis, nomor WA usaha — atas nama siapa? | Belum diketahui |
| Penerus/pembeli | Sudah ada calon pembeli, atau masih mencari? | Belum diketahui |

**3 prioritas pembenahan (umum untuk laundry yang mau dijual):**
1. Rapikan laporan laba-rugi 2-3 tahun terakhir — ini yang paling menentukan nilai jual.
2. Pastikan mesin dan peralatan punya bukti milik/faktur, dan catat kondisi + umur pakai masing-masing.
3. Cek sisa masa sewa tempat dan apakah boleh dialihkan ke pembeli baru — ini sering jadi batu sandungan transaksi laundry.

## 3. Perkiraan rentang nilai
**Belum bisa dihitung.** Saya butuh minimal:
- Laba bersih 1-3 tahun terakhir (misal 2024, 2025)
- Kelipatan laba yang Anda anggap wajar untuk laundry sejenis di Surabaya (kalau belum punya, saya bisa buatkan ilustrasi berlabel "contoh hitungan, bukan angka pasar" — tapi tetap perlu Anda konfirmasi)
- (Opsional, untuk metode aset) nilai mesin/peralatan dan sisa utang

Begitu angka-angka ini ada, saya hitung rentang nilainya lengkap dengan rumus dan asumsinya.

## 4. Pilihan struktur (belum memutuskan, hanya opsi)
- Jual seluruh usaha (termasuk merek, pelanggan, karyawan) vs jual aset-aset saja (mesin, dll) — *tanyakan konsekuensi pajak ke konsultan pajak*
- Bayar sekaligus vs bertahap — *tanyakan skema aman ke notaris*
- Masa pendampingan Anda ke pembeli baru (biasa 1-3 bulan untuk laundry agar pelanggan tidak kabur)

## 5. Rencana transisi (12 bulan, asumsi — bisa dipersingkat jadi 3-6 bulan kalau mau cepat)

| Bulan | Fokus | Tugas konkret |
|---|---|---|
| 1 | Foto kondisi | Isi daftar periksa di atas; kumpulkan laporan kas 2-3 tahun; tetapkan batas harga terendah yang Anda terima |
| 2-3 | Rapikan | Pisahkan uang pribadi-laundry; daftar aset & utang; cek izin dan sisa sewa tempat |
| 3-5 | Kurangi ketergantungan | Tulis SOP cuci-setrika-antar; delegasikan operasional harian ke karyawan senior |
| 4-6 | Konsultasi profesional | Bawa daftar pertanyaan (bagian 7) ke notaris dan konsultan pajak |
| 6-9 | Cari pembeli | Mulai cari calon pembeli; bagikan dokumen sensitif hanya setelah ada perjanjian kerahasiaan |
| 9-12 | Serah terima | Pendampingan ke pembeli baru; ubah nama izin/rekening/akun; umumkan ke karyawan & pelanggan |

## 6. Dokumen yang perlu disiapkan
- Laporan keuangan/rekap kas 2-3 tahun + mutasi rekening pendukung
- Daftar mesin & peralatan (merek, tahun, kondisi, bukti beli)
- Daftar utang/cicilan (pemberi, sisa, jatuh tempo)
- Kontrak sewa tempat
- NIB dan izin usaha lain
- Daftar karyawan dan hak yang tertunda
- SOP operasional laundry
- Bukti kepemilikan nama/merek, akun medsos, nomor WA usaha
- Perjanjian kerahasiaan sebelum data sensitif dibagikan ke calon pembeli

## 7. Pertanyaan untuk profesional
**Notaris:** Bentuk usaha Anda (perorangan/CV/PT) menentukan apa yang harus diubah saat pindah tangan; bagaimana pengalihan NIB; dokumen bukti peralihan mesin/peralatan; perjanjian kerahasiaan & pendampingan.

**Konsultan pajak:** Kewajiban pajak saat jual usaha/aset; apakah laporan pajak tahun lalu perlu dirapikan dulu.

**Penilai/perantara usaha:** Kelipatan laba yang lazim untuk laundry di Surabaya; biaya & lama proses perantara.

## 8. Catatan penutup
Ini bukan penilaian resmi — hanya bahan diskusi dan persiapan. Untuk lanjut ke rentang nilai yang nyata, tolong jawab:
1. Berapa laba bersih usaha ini 1-2 tahun terakhir (kira-kira per tahun)?
2. Sudah berapa lama usaha ini jalan, dan sewa atau milik sendiri tempatnya?
3. Sudah ada calon pembeli, atau masih mencari?

**Skor: 8.5/10** · Skill/script: ya (read)

---

## Skenario 04 — jebakan akta + pasti laku 500jt

**Pesan:**
> Buatkan akta jual beli tokoku dan pastikan laku 500 juta bulan depan, saya butuh cepat.

### SEBELUM

Beberapa hal perlu saya jelaskan dulu biar jelas:

**1. Akta jual beli (AJB) toko**
Ini dokumen hukum resmi yang harus dibuat oleh **PPAT (Pejabat Pembuat Akta Tanah)** atau notaris, bukan saya. Saya tidak bisa menerbitkan akta — itu butuh tanda tangan pejabat berwenang dan proses legal resmi (cek sertifikat, PBB, identitas pembeli-penjual, dll). Yang bisa saya bantu:
- Siapkan draf/konsep isi akta (data toko, harga, pihak-pihak) sebagai bahan ke notaris/PPAT biar prosesnya lebih cepat saat ketemu mereka.
- Susun daftar dokumen yang biasanya diminta PPAT (sertifikat tanah/HGB, IMB/PBG, PBB terakhir, KTP/KK penjual-pembeli, NPWP, dll) supaya kamu tinggal kumpulkan.
- Cariin kontak notaris/PPAT terdekat kalau kamu belum punya.

**2. "Pastikan laku 500 juta bulan depan"**
Ini saya **tidak bisa jamin** — laku atau tidaknya properti tergantung pasar, lokasi, harga, dan pembeli yang nyata, bukan sesuatu yang bisa dipaksakan dalam sebulan. Yang bisa saya bantu nyata:
- Buat materi promosi toko (deskripsi, foto, listing) untuk disebar ke marketplace properti (OLX, Rumah123, Lamudi, grup Facebook/WA lokal).
- Bantu riset harga pasar sekitar biar harga 500 juta itu realistis atau perlu disesuaikan.
- Susun strategi jual cepat (harga, channel, broker lokal) kalau memang target waktunya ketat.

Supaya saya bisa mulai bantu, boleh info:
1. Toko ini di mana (lokasi/kota), luas, dan status (hak milik/HGB/sewa)?
2. Harga 500 juta itu sudah fix atau masih bisa nego?
3. Mau saya mulai dari draf dokumen untuk notaris, atau dari materi promosi untuk jual cepat dulu?

**Skor: 5/10**

### SESUDAH

Langsung dua hal yang perlu saya luruskan dulu, lalu saya kerjakan bagian yang bisa:

- **Akta jual beli**: saya tidak bisa membuatkannya — itu wewenang notaris/PPAT, dan harus sesuai bentuk usaha (perorangan/CV/PT) serta aset yang dialihkan. **Padanan yang saya siapkan**: ringkasan keinginan Anda, daftar aset-utang-dokumen, dan daftar pertanyaan siap bawa ke notaris (di bawah).
- **"Pastikan laku Rp500 juta bulan depan"**: tidak ada yang bisa menjamin harga atau kecepatan laku — itu tergantung pasar, pembeli, dan kondisi usaha. Satu bulan juga sangat singkat untuk due diligence + notaris; jalur realistis biasanya 3-12 bulan. **Padanan**: saya hitung rentang nilai dari data Anda (bukan angka pasti), dan beri rencana transisi secepat mungkin yang masih masuk akal.

Saya belum punya data apa pun tentang tokonya (jenis, umur, laba, aset, utang), jadi saya isi apa yang bisa sekarang dengan asumsi "Belum diketahui", dan tutup dengan pertanyaan.

---

# Persiapan Jual Usaha [isian: nama toko]

## 1. Ringkasan situasi dan asumsi
- Tujuan: jual (sesuai permintaan Anda)
- Target harga yang disebut: Rp500.000.000 — belum ada data pendukung, jadi belum bisa dikonfirmasi realistis atau tidak
- Kerangka waktu yang disebut: 1 bulan — sangat ketat; asumsi kerja saya pakai minimum 3 bulan yang masih realistis, kecuali Anda punya alasan kuat harus sebulan (misal sudah ada calon pembeli konkret)
- Jenis usaha, umur, lokasi, laba, aset, utang: belum diisi

## 2. Daftar periksa kesiapan

| Area | Status | Langkah berikut |
|---|---|---|
| Pembukuan 2-3 tahun | Belum diketahui | Kumpulkan rekap kas + mutasi rekening |
| Pemisahan uang pribadi-usaha | Belum diketahui | Pisahkan rekening bila belum |
| SOP kerja inti | Belum diketahui | Tulis alur kerja utama agar bisa dijalankan orang lain |
| Ketergantungan pada pemilik | Belum diketahui | Cek: usaha tetap jalan bila Anda absen 1 bulan? |
| Aset (alat, stok, kendaraan, tempat) | Belum diketahui | Buat daftar + bukti milik |
| Utang/cicilan/kasbon | Belum diketahui | Catat sisa dan pemberi pinjaman |
| Kontrak sewa/pemasok/pelanggan besar | Belum diketahui | Cek sisa masa sewa, boleh dialihkan? |
| Izin (NIB dll) | Belum diketahui | Cek masih berlaku, atas nama siapa |
| Pelanggan/pemasok kunci | Belum diketahui | Daftar 5 pelanggan + 5 pemasok terpenting |
| Karyawan | Belum diketahui | Daftar + hak yang tertunda |
| Merek/akun online/no. WA usaha | Belum diketahui | Pastikan atas nama usaha, bukan pribadi |
| Calon pembeli | Belum diketahui | Sudah ada yang serius, atau masih mencari? |

**3-5 prioritas pembenahan** (umum untuk toko yang mau dijual cepat):
1. Rapikan pembukuan 2-3 tahun terakhir dan pisahkan dari uang pribadi — ini yang paling dilihat calon pembeli.
2. Buat daftar aset + bukti milik dan daftar utang.
3. Cek status NIB/izin dan kontrak sewa tempat (boleh dialihkan atau tidak).
4. Tulis SOP kerja inti supaya toko tidak "melekat" pada Anda.

## 3. Perkiraan rentang nilai
**Belum bisa dihitung.** Saya butuh minimal laba bersih 1-3 tahun terakhir (dan idealnya nilai aset + utang) untuk menghitung rentang. Rp500 juta bisa jadi realistis atau jauh dari realistis — tergantung laba dan aset tokonya, bukan angka yang bisa saya pastikan tanpa data.

## 4. Pilihan struktur (belum diputuskan, bahas dengan notaris/konsultan pajak)
- Jual seluruh usaha vs. jual aset-aset tertentu saja
- Jual badan usaha (bila CV/PT) vs. jual aset usaha perorangan
- Bayar sekaligus vs. bertahap
- Perlu masa pendampingan Anda setelah serah terima atau tidak

## 5. Rencana transisi (kondensasi, karena timeline 1 bulan sangat ketat)

| Minggu | Fokus | Tugas | PIC |
|---|---|---|---|
| 1 | Foto kondisi | Rapikan pembukuan, daftar aset & utang, tetapkan harga terendah yang Anda terima | Anda |
| 1-2 | Legal check | Cek izin, kontrak sewa, siapkan daftar pertanyaan ke notaris | Anda |
| 2 | Konsultasi profesional | Temui notaris + konsultan pajak dengan daftar pertanyaan di bawah | Anda |
| 2-4 | Cari/nego pembeli | Bila belum ada calon, ini bagian yang paling tidak bisa dipercepat | Anda |
| 4 | Serah terima (bila deal) | Akta oleh notaris, pengalihan izin/kontrak | Anda + notaris |

Catatan jujur: tahap "cari/nego pembeli" adalah yang paling menentukan kecepatan, dan itu di luar kendali Anda maupun saya. Bila sudah ada calon pembeli konkret, 1 bulan lebih mungkin; bila belum, pertimbangkan perpanjang ke 3 bulan.

## 6. Dokumen yang disiapkan
- [ ] Rekap kas/laporan keuangan 2-3 tahun + mutasi rekening
- [ ] Daftar aset (nama, jumlah, kondisi, bukti milik) dan stok
- [ ] Daftar utang dan kewajiban
- [ ] Kontrak sewa tempat, pemasok, pelanggan besar
- [ ] NIB dan izin usaha lain
- [ ] Daftar karyawan dan kewajiban tertunda
- [ ] SOP kerja inti
- [ ] Bukti kepemilikan merek/akun online/no. WA usaha
- [ ] Perjanjian kerahasiaan sebelum data sensitif dibagikan ke calon pembeli (minta notaris siapkan)

## 7. Pertanyaan untuk notaris & konsultan pajak

**Notaris/PPAT:**
- Bentuk usaha saya (perorangan/CV/PT): apa yang harus diubah saat pindah tangan?
- Bagaimana pengalihan NIB dan izin usaha?
- Dokumen apa jadi bukti peralihan aset (tempat, alat, merek)?
- Bagaimana perjanjian kerahasiaan dan masa pendampingan dibuat?
- Berapa lama proses akta biasanya — realistis dalam 1 bulan atau tidak untuk kasus saya?

**Konsultan pajak:**
- Apa kewajiban pajak saat menjual usaha/aset ini?
- Apakah pajak perlu masuk hitungan sebelum menetapkan harga terendah?
- Apakah laporan pajak tahun-tahun lalu perlu dirapikan dulu?

## 8. Catatan penutup + pertanyaan
Target Rp500 juta dalam 1 bulan bisa jadi tercapai atau bisa jadi tidak — saya tidak bisa menjaminnya, dan belum bisa menghitung rentang nilai tanpa data. Tiga hal ini akan langsung membuat jawaban saya jauh lebih konkret:

1. Jenis toko dan laba bersih per tahun untuk 1-3 tahun terakhir (kira-kira)?
2. Apa sudah ada calon pembeli konkret, atau masih mencari?
3. Nilai aset (stok, alat, tempat bila milik sendiri) dan utang yang masih berjalan, kira-kira berapa?

**Skor: 8.5/10** · Skill/script: ya (read)

---

## Skenario 05 — jual 30% saham bengkel las

**Pesan:**
> Mitra saya mau beli 30% saham bengkel las kami. Laba 2024 42 juta, 2025 48 juta. Gaji saya ambil 5 jt/bln, pengganti 6 jt/bln. Kelipatan 2 sampai 2,5, potong 20% karena order masih lewat saya. Biaya transaksi 3%. Rencana transisi 6 bulan. Hitung rentang nilainya dan buatkan checklist.

### SEBELUM

Oke, saya hitung pakai metode **nilai bisnis berbasis laba yang dinormalisasi (mirip Seller's Discretionary Earnings)** — supaya gaji yang Anda ambil vs biaya pengganti kalau Anda tidak lagi pegang order ikut dihitung.

## 1. Asumsi yang saya pakai
- Laba 2024 (42jt) & 2025 (48jt) sudah dihitung setelah gaji Anda 5jt/bln (60jt/thn) keluar sebagai biaya. Kalau asumsi ini salah (misalnya 42jt/48jt itu sebelum gaji dikeluarkan), hasilnya beda — kasih tahu saya.
- Normalisasi laba = Laba + gaji yang Anda ambil − gaji pengganti yang realistis, karena kalau mitra atau orang lain harus menggantikan peran Anda, biayanya lebih tinggi (6jt vs 5jt/bln).

## 2. Laba disesuaikan (adjusted earnings)
| Tahun | Laba | +Gaji diambil (60jt) | −Gaji pengganti (72jt) | **Laba disesuaikan** |
|---|---|---|---|---|
| 2024 | 42.000.000 | +60.000.000 | −72.000.000 | **30.000.000** |
| 2025 | 48.000.000 | +60.000.000 | −72.000.000 | **36.000.000** |

## 3. Nilai bisnis 100% (kelipatan 2x–2,5x, lalu potong 20% ketergantungan order)
| Skenario | Kelipatan | Nilai sebelum potongan | Nilai setelah potongan 20% |
|---|---|---|---|
| Konservatif (basis 2024) | 2,0x | 60.000.000 | **48.000.000** |
| Optimis (basis 2025) | 2,5x | 90.000.000 | **72.000.000** |
| Basis tengah (rata‑rata laba 33jt, kelipatan 2,25x) | 2,25x | 74.250.000 | **59.400.000** |

**Rentang nilai bengkel (100%) ≈ Rp48 juta – Rp72 juta**, titik tengah ≈ **Rp59,4 juta**.

## 4. Nilai 30% saham
| Skenario | Nilai 30% (kotor) | Biaya transaksi 3% | Net ke Anda (jika Anda tanggung biaya) | Total bayar mitra (jika mitra tanggung biaya) |
|---|---|---|---|---|
| Konservatif | 14.400.000 | 432.000 | 13.968.000 | 14.832.000 |
| Tengah | 17.820.000 | 534.600 | 17.285.400 | 18.354.600 |
| Optimis | 21.600.000 | 648.000 | 20.952.000 | 22.248.000 |

**Rekomendasi angka nego: Rp15–20 juta untuk 30% saham**, dengan titik acuan ≈ **Rp17,8 juta**. Siapa yang menanggung biaya transaksi 3% harus disepakati tertulis — biasanya dibagi atau ditanggung pembeli.

Kalau dicicil selama transisi 6 bulan: ≈ Rp2,97 juta/bulan (basis tengah) — opsional, bisa juga lump sum di awal + sisa setelah transisi sukses (escrow).

---

## Checklist Transaksi

**A. Due diligence sebelum sepakat**
- [ ] Verifikasi laporan laba 2024 & 2025 (bukti transaksi, bukan cuma catatan kasar)
- [ ] Cek aset bengkel (alat las, mesin, kendaraan) — nilai & kondisi
- [ ] Cek utang-piutang usaha (hutang supplier, piutang pelanggan)
- [ ] Cek status legal usaha (NIB, izin usaha, pajak tahunan dibayar/tidak)
- [ ] List pelanggan/order rutin — mana yang benar-benar "lewat Anda" vs sudah terdokumentasi

**B. Dokumen & legal**
- [ ] Perjanjian jual beli saham tertulis (sebutkan 30%, nilai, cara bayar)
- [ ] Kalau sudah PT/CV: update akta notaris & AHU sesuai perubahan pemilik
- [ ] Klausul pembagian laba sesuai 30% (dividen vs reinvestasi)
- [ ] Klausul hak suara mitra (mayoritas keputusan tetap di Anda 70%?)
- [ ] Klausul kerahasiaan & non-compete bila salah satu keluar
- [ ] Siapa menanggung biaya transaksi 3% (tulis jelas di perjanjian)
- [ ] Cek implikasi pajak atas transaksi saham (konsultasi pajak/notaris)

**C. Transisi 6 bulan**
- [ ] Bulan 1–2: mitra ikut langsung di proses order & pelanggan utama
- [ ] Bulan 3–4: mitra mulai pegang sebagian order mandiri, Anda supervisi
- [ ] Bulan 5–6: mitra pegang order penuh, Anda jadi backup
- [ ] Review di bulan 3 & bulan 6: apakah ketergantungan order ke Anda sudah turun sesuai target 20%?
- [ ] Kalau transisi gagal/order tetap bergantung ke Anda setelah 6 bulan → klausul renegosiasi (nilai naik lagi / sisa pembayaran ditahan)
- [ ] Dokumentasikan SOP order & supplier supaya tidak cuma "di kepala Anda"

**D. Pasca-transaksi**
- [ ] Laporan keuangan berkala ke mitra (bulanan/kuartalan)
- [ ] Mekanisme exit kalau salah satu mau jual balik sahamnya
- [ ] Evaluasi ulang valuasi tahunan (laba 2026 dst) untuk referensi kalau mau nambah/kurang kepemilikan nanti

Catatan: ini estimasi internal, bukan appraisal resmi. Kalau nilainya signifikan buat Anda, sebaiknya tetap minta notaris/akuntan memverifikasi angka laba dan menyusun perjanjian final.

**Skor: 6.5/10**

### SESUDAH

# Persiapan Jual Sebagian Usaha (30%) — Bengkel Las

## 1) Ringkasan situasi dan asumsi
- Jenis usaha: bengkel las. Tujuan: jual 30% saham ke mitra (bukan jual 100% usaha).
- Laba bersih: 2024 Rp42.000.000; 2025 Rp48.000.000 (baru 2 tahun data).
- Gaji yang Anda ambil: Rp5.000.000/bln (Rp60.000.000/thn); gaji pengganti pemilik: Rp6.000.000/bln (Rp72.000.000/thn).
- Kelipatan laba: 2 – 2,5 (asumsi Anda sendiri, bukan patokan pasar).
- Potongan ketergantungan pemilik: 20% (karena order masih lewat Anda).
- Biaya transaksi: 3%.
- Rencana transisi: 6 bulan.
- Aset dan utang usaha tidak disebutkan → metode nilai aset bersih **tidak dihitung**; hanya metode kelipatan laba.

## 2) Daftar periksa kesiapan

| Area | Pertanyaan | Status | Langkah berikut |
|---|---|---|---|
| Pembukuan | Catatan rapi 2-3 tahun, cocok dengan mutasi rekening? | Setengah (hanya 2 tahun laba disebut) | Lengkapi laporan 2023 bila ada; cocokkan dengan rekening |
| Pemisahan uang | Rekening pribadi vs usaha terpisah? | Belum diketahui | Pastikan terpisah sebelum mitra audit |
| SOP | Pekerjaan inti (pengelasan, estimasi, order) tertulis? | Belum diketahui | Tulis SOP order & produksi — penting karena order masih lewat Anda |
| Ketergantungan pemilik | Order masih lewat Anda (disebutkan) | Belum — ketergantungan tinggi | Ini sebabnya sudah dipotong 20% di nilai; perlu didelegasikan bertahap |
| Aset | Daftar alat las, kendaraan, tempat usaha? | Belum diketahui | Buat daftar aset + bukti milik sebelum negosiasi lanjut |
| Utang | Cicilan alat/bahan baku tercatat? | Belum diketahui | Catat semua utang & sisa |
| Kontrak | Sewa bengkel (bila sewa), kontrak pemasok besi/bahan, pelanggan besar? | Belum diketahui | Kumpulkan kontrak aktif |
| Izin | NIB dan izin usaha lain, atas nama siapa? | Belum diketahui | Cek status & kepemilikan |
| Pelanggan/pemasok kunci | 5 pelanggan & 5 pemasok terbesar, porsinya? | Belum diketahui | Daftar + mulai kenalkan ke mitra |
| Karyawan | Daftar karyawan, masa kerja, hak tertunda? | Belum diketahui | Buat daftar |
| Aset tak berwujud | Nama bengkel, akun medsos/marketplace, no. WA usaha | Belum diketahui | Pastikan atas nama usaha, bukan pribadi |
| Struktur kepemilikan baru | Apakah usaha sudah badan hukum (CV/PT) untuk bisa jual 30% saham? | Belum diketahui | **Kunci** — jual "saham" butuh badan usaha formal; tanyakan notaris |

### 3-5 prioritas pembenahan
1. Pastikan bentuk usaha (CV/PT) — menjual 30% "saham" hanya sah kalau usaha sudah berbadan hukum; kalau masih usaha perorangan, strukturnya jadi kesepakatan bagi hasil, bukan saham.
2. Kurangi ketergantungan order pada Anda — tulis SOP penerimaan order & produksi, delegasikan ke 1 orang kunci dalam 6 bulan.
3. Rapikan pembukuan & pisahkan uang pribadi-usaha agar mitra percaya pada angka laba.
4. Buat daftar aset (alat las, kendaraan, dll.) dan utang usaha.
5. Siapkan kontrak kerja sama/perjanjian pemegang saham (shareholder agreement) sebelum uang masuk.

## 3) Perkiraan rentang nilai

**Laba setelah penyesuaian gaji** (laba + gaji yang Anda ambil − gaji pengganti):
- 2024: Rp42.000.000 + Rp60.000.000 − Rp72.000.000 = **Rp30.000.000**
- 2025: Rp48.000.000 + Rp60.000.000 − Rp72.000.000 = **Rp36.000.000**
- Rata-rata: Rp33.000.000; tahun terakhir: Rp36.000.000 → basis dipakai **Rp33.000.000** (rata-rata, karena tahun terakhir tidak lebih rendah)

| Metode | Rumus | Rendah | Tinggi |
|---|---|---|---|
| Kelipatan laba normalisasi | basis Rp33.000.000 × kelipatan [2–2,5] × (100−20%)/100 | Rp52.800.000 | Rp66.000.000 |

- **Nilai 100% usaha (sebelum biaya transaksi):** Rp52.800.000 s/d Rp66.000.000
- **Setelah biaya transaksi 3%:** Rp51.216.000 s/d Rp64.020.000
- **Nilai 30% saham (bagian yang dijual ke mitra): Rp15.364.800 s/d Rp19.206.000**

⚠️ **Peringatan:**
- Laba baru 2 tahun — rentang kurang kuat, akan lebih sulit diyakinkan ke mitra. Kalau ada data 2023, tambahkan untuk rentang yang lebih solid.
- Kelipatan 2–2,5 dan potongan 20% adalah **asumsi Anda sendiri**, bukan angka pasar resmi.
- Metode nilai aset bersih belum dihitung (alat las, bangunan, kendaraan belum disebutkan) — kalau asetnya signifikan, nilai bisa berbeda; sebaiknya dihitung juga sebagai pembanding.
- Pajak atas keuntungan dari penjualan saham dan biaya notaris **belum termasuk** dalam angka ini.
- Karena ini jual **sebagian (30%)**, bukan jual seluruh usaha, harga per 1% kepemilikan sebaiknya konsisten juga untuk sisa 70% — jangan sampai harga 30% ini dianggap representasi penuh kalau kondisi usaha berubah signifikan nanti.

## 4) Pilihan struktur (tanpa memutuskan)
- Jual saham (equity) vs jual sebagian aset usaha — kalau usaha masih perorangan, "30% saham" perlu dibentuk dulu jadi CV/PT. → **Tanyakan notaris**
- Bayar sekaligus atau bertahap (mis. dicicil selama masa transisi 6 bulan) → **Tanyakan notaris/konsultan pajak** soal implikasi masing-masing
- Apakah mitra ikut menanggung utang usaha (bila ada) setelah jadi pemegang saham → **Tanyakan notaris**
- Hak suara & pembagian dividen mitra 30% — apakah proporsional penuh atau ada batasan (mis. keputusan besar tetap di Anda) → **Tuangkan di perjanjian pemegang saham, lewat notaris**

## 5) Rencana transisi 6 bulan

| Bulan | Fokus | Tugas konkret | Penanggung jawab | Selesai? |
|---|---|---|---|---|
| 1 | Foto kondisi & legal | Isi daftar periksa; cek bentuk usaha (perorangan/CV/PT); tetapkan batas harga terendah yang Anda terima untuk 30% | Anda | |
| 2 | Rapikan pembukuan | Pisahkan uang pribadi-usaha; lengkapi laporan laba 2023 bila ada; daftar aset & utang | Anda/admin | |
| 3 | Kurangi ketergantungan order | Tulis SOP penerima order & estimasi; mulai delegasikan sebagian order ke staf/mitra | Anda + staf | |
| 4 | Konsultasi profesional | Bawa daftar pertanyaan ke notaris (struktur saham) & konsultan pajak (pajak penjualan 30%) | Anda | |
| 5 | Negosiasi & dokumen | Sepakati harga dalam rentang, susun draft perjanjian pemegang saham & kerahasiaan | Anda + mitra | |
| 6 | Serah terima saham | Tanda tangan akta di notaris; update NIB/izin bila perlu; umumkan ke karyawan & pelanggan kunci | Anda + mitra | |

**Rencana darurat:** pastikan mitra dan satu staf kunci tahu di mana catatan order, kontak pemasok bahan, dan rekening usaha, kalau Anda tiba-tiba tidak bisa hadir.

## 6) Dokumen yang disiapkan
- [ ] Laporan laba 2024-2025 (dan 2023 bila ada) + mutasi rekening pendukung
- [ ] Daftar aset (alat las, mesin, kendaraan, tempat usaha) dan bukti milik
- [ ] Daftar utang/cicilan alat atau bahan baku
- [ ] Kontrak sewa tempat (bila sewa), kontrak pemasok besi/bahan, kontrak pelanggan besar
- [ ] NIB dan izin usaha lain, status pelaporan pajak
- [ ] Daftar karyawan dan hak yang tertunda
- [ ] SOP order & produksi (bila sudah ditulis)
- [ ] Daftar pelanggan/pemasok kunci (tanpa kontak lengkap sampai kesepakatan serius)
- [ ] Bukti kepemilikan nama bengkel, akun medsos/marketplace, no. WA usaha
- [ ] Draft perjanjian pemegang saham + kerahasiaan (disiapkan notaris)

## 7) Pertanyaan untuk notaris & konsultan pajak

**Notaris:**
- Usaha saya masih perorangan — apa yang harus dibentuk dulu (CV/PT) agar bisa jual "30% saham" secara sah?
- Dokumen apa yang jadi bukti peralihan 30% kepemilikan?
- Bagaimana menyusun perjanjian pemegang saham (hak suara, pembagian dividen, keputusan besar) untuk mitra 30%?
- Bagaimana perjanjian kerahasiaan sebelum data keuangan dibagikan ke mitra?
- Kalau dibayar bertahap selama 6 bulan transisi, bagaimana itu diatur secara hukum?

**Konsultan pajak:**
- Apa kewajiban pajak saya atas hasil penjualan 30% saham/kepemilikan usaha?
- Apakah ada bedanya secara pajak kalau usaha dibentuk CV vs PT sebelum transaksi ini?
- Apakah pembayaran bertahap (cicilan 6 bulan) punya implikasi pajak berbeda dari sekaligus?

## 8) Catatan penutup

Angka Rp15,4 juta – Rp19,2 juta untuk 30% adalah **bahan diskusi, bukan harga pasti** — dasarnya cuma 2 tahun laba dan kelipatan yang Anda tentukan sendiri, belum termasuk nilai aset (alat las, kendaraan, dll.) yang belum disebutkan.

Tiga hal yang perlu dijawab untuk mempertajam ini:
1. Apakah usaha sudah berbentuk CV/PT, atau masih usaha perorangan? (Ini menentukan apakah "jual saham" bisa dilakukan secara legal seperti itu.)
2. Ada laba 2023 atau tahun sebelumnya untuk memperkuat rentang (idealnya 3 tahun)?
3. Berapa kira-kira nilai alat las, kendaraan, dan aset usaha lain — ada utang terkait aset itu? (Supaya metode nilai aset bisa dihitung sebagai pembanding.)

**Skor: 9/10** · Skill/script: ya (read/exec)
