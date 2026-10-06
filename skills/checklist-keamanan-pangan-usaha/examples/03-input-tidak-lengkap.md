# Skenario 3: input tidak lengkap

**Input:** "checklist keamanan pangan dong"

## Catatan
Catatan penguji: langsung bekerja dengan asumsi default skill dan menyebutnya, 3 pertanyaan di akhir. Cacat kecil: alergen menyebut kacang & gandum "ada di menu asumsi" padahal asumsi menu (ayam, telur, nasi, santan, susu) tidak memuatnya. Nilai: sebelum 6,0, sesudah 8,0.

## Output SESUDAH (skill aktif)

Paket Keamanan Pangan - Kafe/Warung (asumsi, belum ada detail usaha)

**Asumsi** (karena belum ada detail, saya pakai default — kasih tahu kalau mau disesuaikan):
- Jenis usaha: kafe/warung
- Menu/bahan utama: ayam, telur, nasi, santan, susu
- Jumlah staf: 3 orang, 1 penanggung jawab
- Peralatan: kulkas ada, freezer ada, termometer **belum ada**
- Jam buka: [isian: jam buka]

---

## 1. Daftar Periksa Harian

**Saat datang**
- [ ] Cuci tangan sabun 20 detik; rambut tertutup, kuku pendek, tanpa perhiasan
- [ ] Staf sakit (muntah, diare, demam, kuning)? Jangan pegang makanan, lapor penanggung jawab
- [ ] Cek tanda hama (kotoran, bungkus digigit), sampah semalam sudah keluar
- [ ] Baca suhu kulkas dan freezer, catat di log (lihat catatan termometer di bawah)

**Sebelum buka**
- [ ] Permukaan kerja dibersihkan lalu disanitasi
- [ ] Talenan/pisau terpisah: mentah vs matang (ayam vs sayur/lalapan)
- [ ] Bahan lama di depan (FIFO); buang yang lewat tanggal
- [ ] Sabun, tisu, sanitizer, penutup sampah tersedia

**Jam sibuk**
- [ ] Makanan panas tetap >= 60 °C; cek tiap 2 jam, catat
- [ ] Makanan matang tidak di suhu ruang lebih dari 2 jam
- [ ] Cuci tangan setelah pegang mentah, uang, ponsel, sampah
- [ ] Kain lap basah diganti; wadah tertutup

**Tutup**
- [ ] Sisa matang: dinginkan cepat (wadah dangkal) lalu kulkas, atau buang
- [ ] Semua bahan diberi label nama + tanggal, tutup rapat
- [ ] Alat, talenan, lantai dapur dibersihkan; saluran air bersih
- [ ] Baca suhu kulkas/freezer terakhir, catat; tanda tangan: ____

## 2. Mingguan / Bulanan

- [ ] Cek hama: celah dinding, sampah menumpuk, jebakan tikus/lipas
- [ ] Bersihkan bagian dalam kulkas, penyedot asap, saluran air
- [ ] FIFO ulang semua stok, buang yang lewat tanggal
- [ ] Kalibrasi termometer: uji air es, harus 0 °C (toleransi ±1)
- [ ] Cek stok sabun dan sanitizer

## 3. Log Suhu

**Catatan penting:** belum ada termometer pangan. Log suhu tidak bisa diisi dengan angka sampai alat ukur ada — sarannya beli termometer pangan digital (murah, ada di toko alat dapur/online). Sementara ini, pakai cek visual: kulkas dingin terasa saat dibuka, tidak ada bau basi, makanan panas masih mengeluarkan asap/uap, dan catat jam mulai makanan keluar dari kulkas/panas supaya tidak lewat 2 jam di suhu ruang.

Setelah ada termometer, batas yang dipakai:

| Alat | Batas | Jika melebihi |
|---|---|---|
| Kulkas | <= 5 °C | Cek pintu/isi, ukur ulang 30 menit; tetap >5 dan bahan sudah >2 jam: buang, panggil teknisi |
| Freezer | <= -18 °C | Cek pintu/colokan; bahan lunak sebagian: jangan dibekukan ulang, masak segera atau buang |
| Penahan panas | >= 60 °C | Panaskan ulang cepat sampai >=74 °C lalu tahan; <60 lebih dari 2 jam: buang |
| Masak (inti ayam/sisa panasan) | >= 74 °C | Lanjut masak, ukur di bagian paling tebal |

| Tanggal | Jam | Alat | Suhu (°C) | OK? | Tindakan | Paraf |
|---|---|---|---|---|---|---|
| | | Kulkas | | | | |
| | | Freezer | | | | |
| | | Penahan panas | | | | |

## 4. Kartu Staf - 10 Aturan Dapur

1. Cuci tangan sabun 20 detik: sebelum kerja, habis toilet, habis pegang mentah, sampah, HP, uang.
2. Sakit perut, muntah, diare, demam, mata kuning: jangan pegang makanan, lapor, pulang dulu.
3. Mentah dan matang dipisah: talenan, pisau, wadah, rak kulkas (matang atas, mentah bawah).
4. Dingin tetap dingin, panas tetap panas. Jangan biarkan lama di antaranya.
5. Ayam dan sisa panasan matang sampai dalam (>=74 °C). Ukur, jangan kira-kira — sementara pakai: potong, pastikan tidak ada bagian merah/berair di dalam.
6. Sisa panas dinginkan cepat: wadah dangkal, jangan ditutup rapat saat masih panas, lalu kulkas.
7. Semua bahan berlabel nama + tanggal. Yang lama dipakai dulu. Lewat tanggal: buang, jangan diganti label.
8. Ada pesanan alergi (susu, telur, kacang, gandum)? Beri tahu penanggung jawab, pakai alat bersih.
9. Bersihkan dulu, baru sanitasi. Kain lap kotor diganti.
10. Ragu soal aman atau tidak? Buang dan tanya penanggung jawab.

## 5. Peta Risiko Menu (asumsi bahan)

| Bahan | Risiko | Batas waktu/suhu | Cara aman |
|---|---|---|---|
| Ayam | Salmonella, Campylobacter; kontaminasi silang | Matang inti >=74 °C | Talenan terpisah, cuci tangan setelahnya |
| Telur | Salmonella | Simpan kulkas, matang penuh | Hindari setengah matang untuk anak/lansia |
| Nasi | Bacillus cereus (spora tahan masak) | Jangan di suhu ruang >2 jam | Dinginkan cepat atau tahan >=60 °C |
| Santan | Cepat basi | Habiskan cepat | Jangan campur santan baru dengan lama |
| Susu | Cepat berkembang bakteri | Kulkas <=5 °C | Catat tanggal buka, jangan isi ulang wadah lama |

**Alergen:** susu, telur, kacang, gandum ada di menu asumsi ini — cantumkan di menu tiap hidangan, jangan klaim "bebas alergen" kalau dapur sama dengan bahan tersebut.

**Kontaminasi silang spesifik:** talenan ayam vs talenan sayur/lalapan harus beda; cuci tangan setelah pegang ayam mentah sebelum sentuh bahan matang.

## 6. Perizinan (PERLU REVIEW — bukan nasihat hukum, cek ke Dinkes/DPMPTSP/OSS/BPJPH setempat)

| Izin | Relevan | Instansi | Catatan |
|---|---|---|---|
| NIB (OSS) | Semua usaha | OSS | Dasar usaha |
| SLHS + pelatihan penjamah makanan | Kafe/warung | Dinkes kab/kota | PERLU REVIEW syarat terbaru |
| Halal (Self Declare untuk usaha mikro-kecil yang memenuhi syarat) | Produk dijual | BPJPH | PERLU REVIEW tenggat per skala |
| PIRT | Bila ada produk kemasan dijual | Dinkes kab/kota | Tidak semua jenis pangan boleh PIRT |

---

Mau saya sesuaikan dengan detail usaha asli? Tiga hal yang membantu:
1. Jenis usaha dan menu/bahan utama yang sebenarnya?
2. Jumlah staf dan jam buka?
3. Sudah ada termometer pangan, atau perlu saya kasih rekomendasi beli yang murah dulu?

Pengingat: ini kebiasaan kerja aman, bukan pengganti pelatihan penjamah makanan atau pemeriksaan resmi Dinkes/BPOM.
