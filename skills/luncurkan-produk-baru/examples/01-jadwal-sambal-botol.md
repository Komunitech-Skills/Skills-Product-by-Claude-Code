# Contoh 1: Jadwal peluncuran Sambal Botol Bu Rina (fiktif)

Data fiktif. Bu Rina (usaha rumahan fiktif) akan meluncurkan sambal botol 180 g pada Sabtu 14 November 2026. Hari ini 20 Oktober 2026. Stok awal 150 botol, kontak WA 120, IG 800 pengikut, anggaran promo Rp 500.000.

Perintah: `python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-14 --produk "Sambal Botol Bu Rina" --jenis pangan --hari-ini 2026-10-20`

Angka pendamping (dihitung agen, rumus di runbook bagian B): perkiraan pesanan minggu 1 dari daftar tunggu 80 orang x 20% = 16 (patokan awal); rumus stok awal = (pre-order soft launch + perkiraan pesanan minggu 1) x 1,3: (40 pre-order soft launch + 16) x 1,3 = 72,8 -> 73 botol; stok 150 botol cukup, sisa 77 untuk minggu 2-3. Urutan soft launch: pre-order dibuka T-14 (31 Okt), dikirim T-10 (4 Nov), umpan balik ditanya T-5 (9 Nov) setelah barang tiba.
Catatan: pada keluaran di bawah, tugas T-30 (15 Okt) dan T-28 sudah LEWAT karena hari ini 20 Okt; agen menyarankan mengerjakan cek izin/label dan pesan kemasan hari itu juga.

## Keluaran script (apa adanya)

# Jadwal peluncuran: Sambal Botol Bu Rina

- Tanggal peluncuran (T0): **Sabtu, 2026-11-14**
- Jenis produk: pangan
- Jumlah tugas: 43

## Perhatian
- Waktu tersisa 25 hari (<30): tugas sebelum hari ini ditandai LEWAT; padatkan atau geser peluncuran.


### Kamis, 2026-10-15
- [ ] **T-30** [Legalitas | Izin] Cek status izin & label: NIB, PIRT/BPOM, sertifikat halal (pangan). Ini pengingat; keputusan tetap di instansi resmi _(LEWAT: kerjakan secepatnya atau padatkan jadwal)_
- [ ] **T-30** [Pra-peluncuran | Harga] Kunci HPP dan harga tayang; hitung margin setelah biaya marketplace (skill hitung-hpp, harga-jual-marketplace) _(LEWAT: kerjakan secepatnya atau padatkan jadwal)_
- [ ] **T-30** [Pra-peluncuran | Strategi] Tulis 1 kalimat janji produk, calon pembeli utama, dan target angka (mis. jumlah pesanan hari 1-7) _(LEWAT: kerjakan secepatnya atau padatkan jadwal)_

### Jumat, 2026-10-16
- [ ] **T-28** [Legalitas | Label] Finalkan teks label kemasan (komposisi, netto, produsen, tanggal kedaluwarsa, nomor izin/halal) lalu minta cek 2 orang _(digeser dari 2026-10-17 (Sabtu) karena bukan hari kerja; LEWAT: kerjakan secepatnya atau padatkan jadwal)_
- [ ] **T-28** [Stok & operasional | Pemasok] Pesan bahan/barang dan kemasan untuk stok awal; minta kepastian tanggal tiba tertulis _(digeser dari 2026-10-17 (Sabtu) karena bukan hari kerja; LEWAT: kerjakan secepatnya atau padatkan jadwal)_

### Selasa, 2026-10-20
- [ ] **T-25** [Pra-peluncuran | Aset] Foto/video produk: minimal 1 foto putih bersih, 1 foto suasana, 1 video 15 detik (skill foto-produk-brief)
- [ ] **T-25** [Pra-peluncuran | Waitlist] Buat formulir daftar tunggu (Google Form atau tautan wa.me) dengan 3 isian: nama panggilan, nomor WA, rasa/varian diminati

### Sabtu, 2026-10-24
- [ ] **T-21** [Pra-peluncuran | Instagram/TikTok] Posting teaser 1: masalah pelanggan + petunjuk produk (belum sebut nama/harga); ajak isi daftar tunggu
- [ ] **T-21** [Pra-peluncuran | WA grup/komunitas] Kabari 10-20 teman dekat/pelanggan lama lewat WA pribadi (bukan blast) dan minta mereka jadi 'tim pertama'

### Selasa, 2026-10-27
- [ ] **T-18** [Pra-peluncuran | Marketplace] Siapkan draf listing di marketplace (judul, foto, deskripsi, variasi, berat & ukuran paket) - skill listing-marketplace

### Kamis, 2026-10-29
- [ ] **T-16** [Stok & operasional | Pemasok] Cek kemajuan produksi/pesanan pemasok; bila mundur >3 hari, geser tanggal peluncuran SEKARANG

### Sabtu, 2026-10-31
- [ ] **T-14** [Pra-peluncuran | Instagram/TikTok] Posting teaser 2: di balik layar pembuatan/produksi
- [ ] **T-14** [Soft launch | Waitlist] Buka soft launch untuk daftar tunggu: pre-order terbatas (mis. 30-50 unit) dengan tanggal kirim jelas (paling lambat T-10); catat jumlah pre-order (dipakai untuk hitungan stok/kapasitas)

### Senin, 2026-11-02
- [ ] **T-12** [Pra-peluncuran | KOL mikro] Kirim sampel/undangan ke 3-5 kreator mikro yang cocok (1.000-50.000 pengikut); catat kesepakatan tertulis di chat

### Rabu, 2026-11-04
- [ ] **T-10** [Soft launch | Kirim] Kirim pre-order soft launch (batch kecil dari produksi pertama) dan unggah resi; umpan balik baru ditanya setelah barang tiba
- [ ] **T-10** [Stok & operasional | Pengemasan] Beli kemasan pengiriman (dus, bubble wrap, lakban, stiker) untuk stok pesanan hari 1-14
- [ ] **T-10** [Stok & operasional | Uji] Uji coba kirim 2 paket ke alamat teman di luar kota; catat lama tiba dan kondisi barang

### Jumat, 2026-11-06
- [ ] **T-7** [Stok & operasional | Stok] Hitung stok awal = (pre-order soft launch + perkiraan pesanan minggu 1) x 1,3 dan bandingkan dengan stok; tetapkan batas 'stok habis' dan pesan ulang _(digeser dari 2026-11-07 (Sabtu) karena bukan hari kerja)_

### Sabtu, 2026-11-07
- [ ] **T-7** [Promo | Harga] Putuskan promo peluncuran (aturan di references/aturan-promo.md); hitung margin di harga promo terendah

### Senin, 2026-11-09
- [ ] **T-5** [Pra-peluncuran | Instagram/TikTok] Posting teaser 3: countdown + tanggal & jam peluncuran + tautan daftar tunggu
- [ ] **T-5** [Pra-peluncuran | Offline] Bila ikut bazar/titip jual: konfirmasi stan/tempat, jam, dan barang/materi yang dibawa
- [ ] **T-5** [Soft launch | Umpan balik] Setelah barang/layanan diterima, tanya 10 pembeli soft launch: 3 hal disuka, 1 hal kurang; perbaiki listing/label/kemasan bila perlu

### Rabu, 2026-11-11
- [ ] **T-3** [Legalitas | Label] Pastikan foto listing menampilkan label & nomor izin yang benar; sama dengan kemasan fisik
- [ ] **T-3** [Pra-peluncuran | Marketplace] Selesaikan listing (belum aktif/atur jadwal tayang), pasang voucher toko & iklan dengan anggaran harian kecil

### Kamis, 2026-11-12
- [ ] **T-2** [Peluncuran | Tim] Rapat 15 menit: siapa balas chat, siapa kemas, siapa posting; siapkan jawaban cepat (skill balas-chat-cs)
- [ ] **T-2** [Stok & operasional | Stok] Stok fisik sudah di tangan dan dihitung ulang; kemasan pengiriman siap; barang tersimpan di tempat layak

### Jumat, 2026-11-13
- [ ] **T-1** [Peluncuran | Semua kanal] Go/No-Go: barang/kapasitas layanan siap, harga & promo terpasang, listing tayang terjadwal, akun iklan aktif, nomor WA berfungsi
- [ ] **T-1** [Peluncuran | WA grup/komunitas] Kirim pengingat H-1 ke daftar tunggu (satu per satu atau lewat siaran WA resmi bagi yang sudah opt-in)

### Sabtu, 2026-11-14 (T0)
- [ ] **T0** [Peluncuran | Live/TikTok] Siang/malam: sesi live singkat 30-60 menit atau posting video 'unboxing' (skill naskah-live-jualan)
- [ ] **T0** [Peluncuran | Operasional] Balas semua chat <15 menit, kemas pesanan sore itu, catat pesanan & kendala per jam
- [ ] **T0** [Peluncuran | Pengukuran] Malam: catat 5 angka hari-1 (kunjungan, chat, pesanan, omzet, sisa barang/slot)
- [ ] **T0** [Peluncuran | Semua kanal] Pagi: aktifkan listing, posting pengumuman utama di IG/TikTok, story dengan tautan, kirim pesan ke daftar tunggu

### Minggu, 2026-11-15
- [ ] **T+1** [Pasca-peluncuran | Konten] Posting ucapan terima kasih + bukti sosial (tangkapan layar pesanan/testimoni dengan izin) _(jatuh di Minggu: jadwalkan posting, jangan andalkan pemasok/kurir)_

### Senin, 2026-11-16
- [ ] **T+1** [Pasca-peluncuran | Kirim] Kirim semua pesanan hari-1; unggah resi; kabari pembeli lewat pesan singkat _(digeser dari 2026-11-15 (Minggu) karena bukan hari kerja)_

### Selasa, 2026-11-17
- [ ] **T+3** [Pasca-peluncuran | Pengukuran] Tinjau 3 hari pertama: pesanan vs target, keluhan terbanyak, biaya iklan vs omzet
- [ ] **T+3** [Pasca-peluncuran | Ulasan] Minta ulasan dari pembeli yang barangnya sudah tiba (sekali saja, sopan); balas ulasan (skill balas-ulasan-pelanggan)

### Sabtu, 2026-11-21
- [ ] **T+7** [Pasca-peluncuran | Pengukuran] Laporan minggu 1 (skill laporan-iklan-mingguan + rekap penjualan); putuskan lanjut/ubah/stop tiap kanal

### Senin, 2026-11-23
- [ ] **T+7** [Pasca-peluncuran | Stok & operasional] Pesan ulang stok bila sisa < kebutuhan 2 minggu; tetapkan waktu tunggu pemasok _(digeser dari 2026-11-21 (Sabtu) karena bukan hari kerja)_

### Sabtu, 2026-11-28
- [ ] **T+14** [Pasca-peluncuran | Konten] Posting pelajaran: testimoni, tanya-jawab dari chat, 'ternyata pembeli suka ini'
- [ ] **T+14** [Pasca-peluncuran | Promo] Akhiri/ubah promo peluncuran; umumkan harga normal secara jujur (tanpa coret harga palsu)

### Sabtu, 2026-12-05
- [ ] **T+21** [Pasca-peluncuran | Retensi] Hubungi pembeli pertama: tanya kepuasan, tawarkan pembelian ulang/paket hemat (satu pesan pribadi)

### Senin, 2026-12-14
- [ ] **T+30** [Pasca-peluncuran | Pengukuran] Tinjauan 30 hari: omzet, margin nyata, pembeli ulang, keluhan; putuskan produk lanjut/perbaiki/tambah varian
- [ ] **T+30** [Pasca-peluncuran | Pengukuran] Catat 3 pelajaran dan 3 perbaikan untuk peluncuran berikutnya di file terpisah

Catatan: jadwal libur dari SKB 2026/2027 dan bisa berubah; label/izin hanya pengingat, cek situs resmi instansi.
