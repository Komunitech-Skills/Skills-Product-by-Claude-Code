# Uji 04: tiga skenario normal (penguji independen, 2026-09-29)

Penguji: agent terpisah dari pembuat, hanya membaca folder skill + pedoman kurasi Komunitech. Semua data fiktif. "Hari ini" = 2026-09-29.
Jadwal di bawah adalah keluaran nyata `scripts/jadwal_peluncuran.py`; tanggal & pergeseran hari sudah diverifikasi independen (lihat HASIL-UJI.md).

---

## Skenario 1 (normal, pangan) - dipakai juga untuk uji A/B dan banding pesaing

**Input pengguna:** "Kak, aku Sari dari Semarang. Mau launching keripik tempe pedas 100 g harga Rp 15.000, HPP Rp 8.500. Tanggal 7 November. Kontak WA sekitar 250, IG 1.200 pengikut, udah punya toko Shopee (300 pengikut). Anggaran promo+iklan 1 juta. Sekali produksi bisa 300 bungkus seminggu, bahan datang 3 hari setelah pesan."

**Perintah:** `python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-07 --produk "Keripik Tempe Pedas Mbak Sari" --jenis pangan --hari-ini 2026-09-29`

### 1. Asumsi
- Pendaftar daftar tunggu diperkirakan 100 orang (40% dari 250 kontak WA + sebagian IG) - ganti dengan angka nyata saat T-7.
- Biaya admin Shopee dipakai 8% sebagai patokan; hitung angka pastinya dengan skill `harga-jual-marketplace`.
- Promo peluncuran: diskon 10% selama 7 hari untuk daftar tunggu.

### 2. Ringkasan
- Produk: Keripik Tempe Pedas Mbak Sari 100 g, Rp 15.000
- T0: Sabtu, 7 November 2026 (39 hari lagi, jadwal penuh T-30 masih bisa dijalankan)
- Kanal: daftar tunggu WA (milik) + Instagram (sewa) + Shopee (sewa) + 3-5 KOL mikro kuliner Semarang (pinjam)
- Target: 15-25 pesanan minggu 1 (patokan 20), 40 pre-order soft launch
- Anggaran: Rp 1.000.000 (rincian di bawah, sisa cadangan Rp 100.000)

### 3. Kesiapan & angka
Gerbang kesiapan (jawab jujur sebelum T-30): satu janji jelas ("pedas gurih, renyah sampai hari ke-30")? Sudah dicoba 5-10 orang di luar keluarga? Kemasan, label, cara simpan lengkap? Bila belum, jalankan soft launch kecil dulu.

| Hitungan | Rumus | Hasil |
|---|---|---|
| Pesanan minggu 1 | 100 pendaftar x 15-25% | 15-25 (patokan 20) |
| Stok awal minggu 1 | 20 x 1,3 | 26 bungkus |
| Ditambah pre-order soft launch | 26 + 40 | 66 -> siapkan 70 bungkus (catatan penguji: rumus skill tidak menyebut penambahan ini) |
| Penjualan harian | 20 / 7 | 2,9 bungkus |
| Titik pesan ulang bahan | 3 hari x 2,9 | 9 bungkus |
| Laba/bungkus harga normal, Shopee | 15.000 - 8.500 - 1.200 (8%) | Rp 5.300 |
| Laba/bungkus harga promo 13.500, Shopee | 13.500 - 8.500 - 1.080 | Rp 3.920 (masih positif) |
| Laba/bungkus harga promo, WA langsung | 13.500 - 8.500 | Rp 5.000 |

Anggaran: iklan IG Rp 30.000 x 10 hari = 300.000; iklan Shopee Rp 20.000 x 10 hari = 200.000; sampel+ongkir 5 KOL x Rp 50.000 = 250.000; potongan promo Rp 1.500 x 100 bungkus = 150.000. Total Rp 900.000, cadangan Rp 100.000.

### 4. Jadwal bertanggal (keluaran script)
### Jadwal peluncuran: Keripik Tempe Pedas Mbak Sari

- Tanggal peluncuran (T0): **Sabtu, 2026-11-07**
- Jenis produk: pangan
- Jumlah tugas: 42


##### Kamis, 2026-10-08 (T-30)
- [ ] [Pra-peluncuran | Strategi] Tulis 1 kalimat janji produk, calon pembeli utama, dan target angka (mis. jumlah pesanan hari 1-7)
- [ ] [Pra-peluncuran | Harga] Kunci HPP dan harga tayang; hitung margin setelah biaya marketplace (skill hitung-hpp, harga-jual-marketplace)
- [ ] [Legalitas | Izin] Cek status izin & label: NIB, PIRT/BPOM, sertifikat halal (pangan). Ini pengingat; keputusan tetap di instansi resmi

##### Jumat, 2026-10-09 (T-28)
- [ ] [Stok & operasional | Pemasok] Pesan bahan/barang dan kemasan untuk stok awal; minta kepastian tanggal tiba tertulis _(digeser dari 2026-10-10 (Sabtu) karena bukan hari kerja)_
- [ ] [Legalitas | Label] Finalkan teks label kemasan (komposisi, netto, produsen, tanggal kedaluwarsa, nomor izin/halal) lalu minta cek 2 orang _(digeser dari 2026-10-10 (Sabtu) karena bukan hari kerja)_

##### Selasa, 2026-10-13 (T-25)
- [ ] [Pra-peluncuran | Aset] Foto/video produk: minimal 1 foto putih bersih, 1 foto suasana, 1 video 15 detik (skill foto-produk-brief)
- [ ] [Pra-peluncuran | Waitlist] Buat formulir daftar tunggu (Google Form atau tautan wa.me) dengan 3 isian: nama panggilan, nomor WA, rasa/varian diminati

##### Sabtu, 2026-10-17 (T-21)
- [ ] [Pra-peluncuran | Instagram/TikTok] Posting teaser 1: masalah pelanggan + petunjuk produk (belum sebut nama/harga); ajak isi daftar tunggu
- [ ] [Pra-peluncuran | WA grup/komunitas] Kabari 10-20 teman dekat/pelanggan lama lewat WA pribadi (bukan blast) dan minta mereka jadi 'tim pertama'

##### Selasa, 2026-10-20 (T-18)
- [ ] [Pra-peluncuran | Marketplace] Siapkan draf listing di marketplace (judul, foto, deskripsi, variasi, berat & ukuran paket) - skill listing-marketplace

##### Kamis, 2026-10-22 (T-16)
- [ ] [Stok & operasional | Pemasok] Cek kemajuan produksi/pesanan pemasok; bila mundur >3 hari, geser tanggal peluncuran SEKARANG

##### Sabtu, 2026-10-24 (T-14)
- [ ] [Soft launch | Waitlist] Buka soft launch untuk daftar tunggu: pre-order terbatas (mis. 30-50 unit) dengan tanggal kirim jelas
- [ ] [Pra-peluncuran | Instagram/TikTok] Posting teaser 2: di balik layar pembuatan/produksi

##### Senin, 2026-10-26 (T-12)
- [ ] [Pra-peluncuran | KOL mikro] Kirim sampel/undangan ke 3-5 kreator mikro yang cocok (1.000-50.000 pengikut); catat kesepakatan tertulis di chat

##### Rabu, 2026-10-28 (T-10)
- [ ] [Stok & operasional | Pengemasan] Beli kemasan pengiriman (dus, bubble wrap, lakban, stiker) untuk stok pesanan hari 1-14
- [ ] [Stok & operasional | Uji] Uji coba kirim 2 paket ke alamat teman di luar kota; catat lama tiba dan kondisi barang

##### Jumat, 2026-10-30 (T-7)
- [ ] [Stok & operasional | Stok] Hitung stok awal vs perkiraan pesanan; tetapkan batas 'stok habis' dan pesan ulang _(digeser dari 2026-10-31 (Sabtu) karena bukan hari kerja)_

##### Sabtu, 2026-10-31 (T-7)
- [ ] [Soft launch | Umpan balik] Tanya 10 pembeli soft launch: 3 hal disuka, 1 hal kurang; perbaiki listing/label/kemasan bila perlu
- [ ] [Promo | Harga] Putuskan promo peluncuran (aturan di references/aturan-promo.md); hitung margin di harga promo terendah

##### Senin, 2026-11-02 (T-5)
- [ ] [Pra-peluncuran | Instagram/TikTok] Posting teaser 3: countdown + tanggal & jam peluncuran + tautan daftar tunggu
- [ ] [Pra-peluncuran | Offline] Bila ikut bazar/titip jual: konfirmasi stan/tempat, jam, dan stok yang dibawa

##### Rabu, 2026-11-04 (T-3)
- [ ] [Pra-peluncuran | Marketplace] Selesaikan listing (belum aktif/atur jadwal tayang), pasang voucher toko & iklan dengan anggaran harian kecil
- [ ] [Legalitas | Label] Pastikan foto listing menampilkan label & nomor izin yang benar; sama dengan kemasan fisik

##### Kamis, 2026-11-05 (T-2)
- [ ] [Stok & operasional | Stok] Stok fisik sudah di tangan dan dihitung ulang; kemasan pengiriman siap; barang tersimpan di tempat layak
- [ ] [Peluncuran | Tim] Rapat 15 menit: siapa balas chat, siapa kemas, siapa posting; siapkan jawaban cepat (skill balas-chat-cs)

##### Jumat, 2026-11-06 (T-1)
- [ ] [Peluncuran | Semua kanal] Go/No-Go: stok ada, harga & promo terpasang, listing tayang terjadwal, akun iklan aktif, nomor WA berfungsi
- [ ] [Peluncuran | WA grup/komunitas] Kirim pengingat H-1 ke daftar tunggu (satu per satu atau lewat siaran WA resmi bagi yang sudah opt-in)

##### Sabtu, 2026-11-07 (T0)
- [ ] [Peluncuran | Semua kanal] Pagi: aktifkan listing, posting pengumuman utama di IG/TikTok, story dengan tautan, kirim pesan ke daftar tunggu
- [ ] [Peluncuran | Live/TikTok] Siang/malam: sesi live singkat 30-60 menit atau posting video 'unboxing' (skill naskah-live-jualan)
- [ ] [Peluncuran | Operasional] Balas semua chat <15 menit, kemas pesanan sore itu, catat pesanan & kendala per jam
- [ ] [Peluncuran | Pengukuran] Malam: catat 5 angka hari-1 (kunjungan, chat, pesanan, omzet, stok sisa)

##### Minggu, 2026-11-08 (T+1)
- [ ] [Pasca-peluncuran | Konten] Posting ucapan terima kasih + bukti sosial (tangkapan layar pesanan/testimoni dengan izin) _(jatuh di Minggu: jadwalkan posting, jangan andalkan pemasok/kurir)_

##### Senin, 2026-11-09 (T+1)
- [ ] [Pasca-peluncuran | Kirim] Kirim semua pesanan hari-1; unggah resi; kabari pembeli lewat pesan singkat _(digeser dari 2026-11-08 (Minggu) karena bukan hari kerja)_

##### Selasa, 2026-11-10 (T+3)
- [ ] [Pasca-peluncuran | Ulasan] Minta ulasan dari pembeli yang barangnya sudah tiba (sekali saja, sopan); balas ulasan (skill balas-ulasan-pelanggan)
- [ ] [Pasca-peluncuran | Pengukuran] Tinjau 3 hari pertama: pesanan vs target, keluhan terbanyak, biaya iklan vs omzet

##### Sabtu, 2026-11-14 (T+7)
- [ ] [Pasca-peluncuran | Pengukuran] Laporan minggu 1 (skill laporan-iklan-mingguan + rekap penjualan); putuskan lanjut/ubah/stop tiap kanal

##### Senin, 2026-11-16 (T+7)
- [ ] [Pasca-peluncuran | Stok & operasional] Pesan ulang stok bila sisa < kebutuhan 2 minggu; tetapkan waktu tunggu pemasok _(digeser dari 2026-11-14 (Sabtu) karena bukan hari kerja)_

##### Sabtu, 2026-11-21 (T+14)
- [ ] [Pasca-peluncuran | Promo] Akhiri/ubah promo peluncuran; umumkan harga normal secara jujur (tanpa coret harga palsu)
- [ ] [Pasca-peluncuran | Konten] Posting pelajaran: testimoni, tanya-jawab dari chat, 'ternyata pembeli suka ini'

##### Sabtu, 2026-11-28 (T+21)
- [ ] [Pasca-peluncuran | Retensi] Hubungi pembeli pertama: tanya kepuasan, tawarkan pembelian ulang/paket hemat (satu pesan pribadi)

##### Senin, 2026-12-07 (T+30)
- [ ] [Pasca-peluncuran | Pengukuran] Tinjauan 30 hari: omzet, margin nyata, pembeli ulang, keluhan; putuskan produk lanjut/perbaiki/tambah varian
- [ ] [Pasca-peluncuran | Pengukuran] Catat 3 pelajaran dan 3 perbaikan untuk peluncuran berikutnya di file terpisah

Catatan: jadwal libur dari SKB 2026/2027 dan bisa berubah; label/izin hanya pengingat, cek situs resmi instansi.

### 5. Teks siap tempel
**WA pribadi ke tim pertama (Sabtu 17 Okt, T-21):**
Halo Kak Rina, aku Sari. Aku lagi siapin keripik tempe pedas bikinanku sendiri, rencana rilis 7 November. Boleh minta tolong jadi salah satu yang pertama nyobain dan kasih masukan jujur? Kalau mau, balas "IKUT" ya, nanti Kakak aku kabari duluan plus harga khusus. Makasih banyak!

**Teaser IG 1 (17 Okt):** Keripik tempe yang pedasnya cuma di awal terus hilang? Kami juga kesel. Lagi ada yang disiapkan di dapur Semarang, pedas gurihnya nempel sampai remahan terakhir. Mau tahu duluan? Isi daftar tunggu di link bio (gratis, kuota terbatas).
**Teaser IG 2 (24 Okt):** Video 15 detik proses iris tempe tipis + goreng. "Tiap lembar diiris manual. Rilis 7.11."
**Teaser IG 3 (2 Nov):** "5 hari lagi. Sabtu 7 November jam 08.00. Daftar tunggu dapat harga Rp 13.500 selama 7 hari pertama. Link di bio."

**Pembuka soft launch ke daftar tunggu (24 Okt):** Halo Kak [nama panggilan], makasih sudah daftar tunggu Keripik Tempe Pedas Mbak Sari. Kakak dapat akses duluan: pre-order 40 bungkus khusus daftar tunggu, Rp 13.500/bungkus, dikirim mulai Senin 2 November. Balas: nama, alamat, jumlah. Kalau tidak mau dikabari lagi, balas STOP ya.

**Pengingat H-1 (6 Nov):** Kak [nama], besok Sabtu 7 Nov jam 08.00 keripiknya resmi rilis di Shopee dan WA. Harga daftar tunggu Rp 13.500 berlaku sampai Jumat 13 Nov. Balas STOP kalau tidak mau dikabari lagi.

**Hari-H IG (7 Nov):** "RESMI RILIS! Keripik Tempe Pedas Mbak Sari 100 g. Harga perkenalan Rp 13.500 (normal Rp 15.000) sampai 13 November. Pesan lewat Shopee atau WA, link di bio."

**Pesan ke KOL mikro:** Halo Kak [nama], aku Sari, UMKM keripik tempe di Semarang. Aku suka konten kuliner Kakak. Boleh aku kirim 3 bungkus sampel gratis? Kalau Kakak suka dan mau review, mohon diunggah antara 7-10 November dengan tautan Shopee kami dan tanda #iklan/#kolaborasi ya. Tidak ada kewajiban review positif, jujur saja.

**Balasan cepat:** Harga: Rp 15.000/100 g (promo Rp 13.500 s.d. 13 Nov). Ongkir: cek otomatis di Shopee / hitung JNE-J&T dari Semarang. Tahan berapa lama: sesuai tanggal kedaluwarsa di label; setelah dibuka simpan di toples tertutup. Halal/izin: jawab sesuai sertifikat yang benar-benar dimiliki. Retur: barang rusak saat tiba, kirim video unboxing, kami ganti.

### 6. Runbook hari-H & Go/No-Go (Jumat 6 Nov)
07.00 cek stok & tautan -> 08.00 posting + story + pesan daftar tunggu -> tiap jam balas chat <15 menit -> 15.00 serahkan paket ke kurir (Sabtu, pastikan ekspedisi buka) -> 19.00 live 30 menit -> 21.00 catat 5 angka.
Go/No-Go: stok 70 dihitung ulang | harga & voucher Shopee benar | laba di harga promo Rp 3.920 > 0 | foto listing = label kemasan | iklan aktif Rp 30rb/20rb per hari | link bio, wa.me, formulir diuji dari HP lain | admin WA siap | kurir terjadwal. Satu "tidak" pada stok/harga/label = No-Go.

### 7. Pengukuran & legalitas
Catat tiap malam 7-14 Nov: kunjungan Shopee, chat WA/DM, pesanan, omzet, stok sisa. Tinjauan 10 Nov (hari 3), 14 Nov (hari 7), 7 Des (hari 30) di `templates/rencana-peluncuran.md`. Tiap kanal pakai kode sendiri: WA = "TEMPEWA", IG = "TEMPEIG", KOL = kode per kreator.
Legalitas (pengingat, bukan keputusan): NIB (oss.go.id), PIRT dari dinas kesehatan Kota Semarang, sertifikat halal (halal.go.id), label berisi komposisi/netto/produsen/kedaluwarsa/nomor izin. Jangan pasang logo halal sebelum sertifikat terbit. Data daftar tunggu: beri tahu tujuannya dan sediakan cara berhenti (UU 27/2022 PDP).

### 8. Tiga langkah hari ini (29 Sep)
1. Cek status NIB/PIRT/halal sekarang - bila PIRT belum ada, pengurusan bisa lebih lama dari 39 hari; geser T0 lebih awal diputuskan.
2. Tulis janji produk 1 kalimat + hitung HPP final dengan `hitung-hpp`.
3. Buat Google Form daftar tunggu (nama panggilan, nomor WA, level pedas) dan pasang di bio IG.

**Catatan penguji (S1):** format 8 bagian lengkap, angka dihitung, tanggal benar. Kelemahan yang terlihat: jadwal menaruh "Tanya 10 pembeli soft launch" (Sab 31 Okt, T-7) sebelum stok fisik wajib ada (Kam 5 Nov, T-2) - agen harus mengarang tanggal kirim soft launch sendiri (di sini 2 Nov) agar logis; rumus stok tidak memasukkan pre-order soft launch.

---

## Skenario 2 (normal, fashion, lintas tahun + libur tambahan)

**Input:** "Aku jualan gamis linen, mau rilis koleksi baru 15 Januari 2027 buat persiapan Ramadan. Harga Rp 289.000. WA 600 kontak, IG 4.500, TikTok 2.000, Shopee & TikTok Shop ada. Anggaran Rp 3 juta. Konveksi tutup 31 Desember."
**Perintah:** `python3 scripts/jadwal_peluncuran.py --tanggal 2027-01-15 --produk "Gamis Linen Aisyah" --jenis lain --hari-ini 2026-09-29 --libur-tambahan 2026-12-31`

Hasil yang diperiksa (39 tugas, T-30 Rabu 16 Des 2026 s.d. T+30 Minggu 14 Feb 2027):
- T-10 = Selasa 5 Jan 2027 (Isra Mikraj) -> tugas kemasan & uji kirim digeser mundur ke Senin 4 Jan. Benar.
- T-5 = Minggu 10 Jan -> bazar/offline digeser ke Jumat 8 Jan. Benar.
- T-21 (teaser 1) jatuh Jumat 25 Des (Natal), T-14 (soft launch) jatuh Jumat 1 Jan (Tahun Baru): diberi catatan, tidak digeser. Sesuai aturan skill; agen menyarankan menjadwalkan teaser dan memindah soft launch ke Sabtu 2 Jan karena pembeli sedang libur.
- T+21 = Jumat 5 Feb 2027 (cuti bersama Imlek) diberi catatan. Benar.
- Libur tambahan 31 Des tidak mengenai tugas hari kerja mana pun (tidak ada efek, benar).
Agen menambahkan: kanal TikTok Shop live pada T0 Jumat malam; stok per ukuran S-XL dihitung dari patokan 20% x daftar tunggu; peringatan bahwa Ramadan 2027 mulai sekitar 8 Feb sehingga T+14 s.d. T+30 masuk musim puncak (pengetahuan agen, bukan dari skill).
Kekurangan: jenis "lain" tetap memuat tugas "Uji coba kirim 2 paket" dll. (cocok untuk fashion). Tidak ada tugas ukuran/size chart - wajar untuk skill umum.

---

## Skenario 3 (normal, kosmetik, tanggal kembar)

**Input:** "Brand skincare lokal kami mau launching serum niacinamide 20 ml Rp 79.000 tanggal 12.12 biar ikut ramai. Sudah notifikasi BPOM. IG 15 ribu, TikTok 8 ribu, anggaran 5 juta."
**Perintah:** `python3 scripts/jadwal_peluncuran.py --tanggal 2026-12-12 --produk "Serum Niacinamide Glowa" --jenis kosmetik --hari-ini 2026-09-29`

Hasil: 40 tugas, T0 Sabtu 12 Des 2026, peringatan "Dekat tanggal kembar 12.12" muncul. T-28 Sabtu 14 Nov -> Jumat 13 Nov; T-7 stok Sabtu 5 Des -> Jumat 4 Des; T+1 kirim Minggu 13 Des -> Senin 14 Des; T+7 pesan ulang Sabtu 19 Des -> Senin 21 Des. T+30 Senin 11 Jan 2027. Semua benar.
Agen menyarankan: tetap 12.12 sebagai momen (anggaran cukup) tetapi naikkan batas iklan harian dan kunci voucher dengan hitungan margin gabungan terburuk (`references/aturan-promo.md` aturan 3); larangan klaim medis ("menyembuhkan jerawat") dari `references/legalitas-label.md`; minta nomor notifikasi BPOM dicek di cekbpom.pom.go.id sebelum dicantumkan di listing.
Kekurangan: untuk `--jenis kosmetik` script hanya menambah 1 tugas (cek notifikasi BPOM, T-30). Tugas "Finalkan teks label" (T-28) dan "Pastikan foto listing menampilkan label & nomor izin" (T-3) khusus pangan, padahal kosmetik juga wajib mencantumkan nomor notifikasi dan label yang sama dengan listing.
