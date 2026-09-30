---
name: strategi-konten-iklan
description: Menyusun strategi pilar konten (3-5 pilar, sudut pesan, format, corong awareness-pertimbangan-beli) DAN rencana alokasi anggaran iklan bulanan per kanal (Meta/Instagram, TikTok, Shopee Ads, TikTok Shop Ads, Google Ads) per minggu untuk UMKM Indonesia dengan anggaran Rp500rb-Rp20jt per bulan; target CPA, ROAS, titik impas dari margin dan harga rata-rata, serta batas uji dihitung script. Gunakan saat diminta strategi konten, content pillar, budget iklan, bagi anggaran iklan, ads budget planning, target ROAS/CPA, atau "iklan saya harus mulai dari mana". Content strategy, content pillars, paid ads budget allocation, media plan, break-even ROAS.
---

# Strategi Konten & Anggaran Iklan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menjawab dua pertanyaan pemilik usaha dalam **satu dokumen**: (1) "konten apa yang harus saya buat, dan untuk siapa di tahap mana?" dan (2) "uang iklan bulan ini dibagi ke mana, berapa per minggu, dan berapa hasil minimal supaya tidak rugi?". Semua angka uang dihitung **script**, bukan dikira.

## Kapan digunakan
- "Saya punya Rp3 juta untuk iklan sebulan, bagi ke IG/TikTok/Shopee dong."
- "Konten toko saya harus fokus ke apa? Bingung mau posting apa."
- "Berapa ROAS minimal supaya iklan saya tidak rugi? Margin saya 35%."
- Menyiapkan bulan promo 11.11/12.12, Ramadan/Lebaran, tahun ajaran baru.

## Kapan TIDAK digunakan
- Rencana marketing menyeluruh 1-12 bulan (tujuan, target pasar, KPI) -> `rencana-marketing-usaha`.
- Jadwal posting harian 30 hari -> `kalender-konten-30hari` (tawarkan sesudah pilar jadi).
- Membaca ekspor iklan yang sudah tayang dan menyimpulkan performanya -> `laporan-iklan-mingguan`.
- Menulis caption/naskah live/pesan WA lengkap -> skill caption, naskah live, broadcast WA (tawarkan).
- Membuat/menjalankan/mengoptimalkan iklan di akun pengguna (skill ini hanya merencanakan; tidak login, tidak menekan tombol beli/tayang).
- Kategori terlarang (judi, rokok/vape, miras, narkoba, senjata, pinjol ilegal, konten dewasa): tolak singkat.

## Input
| Info | Wajib? | Default jika kosong |
|---|---|---|
| Jenis usaha, produk/jasa utama, kota/jangkauan | Ya | tanyakan |
| Anggaran iklan per bulan | Ya | tanyakan; di bawah Rp100rb: sarankan konten organik dulu |
| Tujuan bulan ini: penjualan / awareness / leads (calon pembeli via WA/formulir) | Tidak | penjualan (disebut sebagai asumsi) |
| Harga rata-rata per pesanan (AOV) | Wajib untuk penjualan & leads | tanyakan |
| Margin kotor (setelah harga pokok, biaya admin marketplace, ongkir yang ditanggung) | Wajib untuk penjualan & leads | tanyakan; bantu hitung dari harga jual - modal - biaya |
| Persen calon pembeli yang jadi membeli (khusus leads) | Wajib untuk leads | tanyakan |
| Kanal yang dipakai/punya toko (IG, TikTok, Shopee, TikTok Shop, Google) | Tidak | Semua yang cocok; **Shopee/TikTok Shop Ads hanya bila punya toko di sana** |
| Momen belanja dalam bulan itu | Tidak | Lihat `references/momen-belanja.md`; tanggal yang berubah tiap tahun tidak ditebak |
| Kategori produk | Tidak | umum; kesehatan/keuangan/kripto diberi catatan aturan iklan |
| Kemampuan produksi konten (video/minggu) | Tidak | 3 konten/minggu per kanal utama |

Jika info wajib kurang, tanyakan **sekali** (maks. 6 pertanyaan bernomor dalam satu pesan). Bila pengguna ingin cepat, pakai default dan tulis asumsinya di awal dokumen.

## Langkah kerja
1. **Cek kelayakan.** Anggaran < Rp100rb/bulan atau margin belum dikenal -> bantu dulu hitung margin; jangan menebak. Kategori terlarang -> tolak. Kategori kesehatan/keuangan/kripto -> lanjut dengan catatan pembatasan (lihat Batasan).
2. **Bangun 3-5 pilar konten** memakai `references/pilar-konten.md`: pilih dari kebutuhan pembeli (pertanyaan yang sering masuk ke WA/DM, keberatan sebelum beli, alasan repeat order), bukan dari selera pemilik. Tiap pilar: tujuan, tahap corong (awareness/pertimbangan/beli/repeat), 3 sudut pesan, format, contoh 5 judul konkret untuk usaha itu. Promosi langsung maksimal +-30% dari total konten.
3. **Petakan corong ke iklan.** Konten yang sudah dapat respons organik baik (simpan/bagikan/tanya harga) boleh diiklankan; konten baru diuji kecil dulu. Kreatif berbeda per tahap: awareness (cerita/hook), pertimbangan (bukti: ulasan asli, demo), beli (penawaran + batas waktu asli).
4. **Hitung anggaran dengan script** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 scripts/alokasi_anggaran.py --anggaran 10jt --tujuan penjualan --aov 150rb --margin 40% \
     --kanal meta,tiktok,shopee --bobot-minggu 1 1 1 2 --kategori umum
   ```
   Opsi: `--tujuan awareness|penjualan|leads`, `--closing 20%` (leads), `--minggu 1-5`, `--min-harian 20rb`, `--json`. Angka diterima gaya Indonesia: `1.500.000`, `1,5jt`, `500rb`, `2 juta`. Angka **ambigu** (`1,500`, `1.5`, `5M`, margin `0,4`) **ditolak** dengan pesan jelas: tanyakan ulang ke pengguna, jangan ditebak.
5. **Baca keluaran script apa adanya.** Salin tabel kanal, tabel minggu, target impas, dan batas uji ke dokumen. Jangan mengubah angka tangan. Bila script menyingkirkan kanal (bagian di bawah batas uji) jelaskan alasannya dengan bahasa awam: "uangnya terlalu tipis untuk diuji di kanal itu; fokus dulu ke kanal yang cukup".
6. **Susun dokumen** sesuai Format Output, sertakan kalender momen dan aturan keputusan mingguan (`references/aturan-keputusan.md`): kapan lanjut, kapan hentikan, kapan tambah anggaran.
7. **Tutup** dengan 3 langkah pertama yang bisa dikerjakan hari ini dan tawaran skill lanjutan (kalender 30 hari, caption, laporan iklan mingguan).

## Yang dihitung script (dan yang TIDAK)
- Pembagian anggaran per kanal menurut tujuan (titik awal, bisa diubah) dan per minggu (bobot minggu untuk momen). Aman 70% / uji 30% per kanal.
- Titik impas ROAS = 1 / margin (dibulatkan ke atas 2 desimal, tidak pernah dianggap lebih ringan dari kenyataan). CPA impas = laba kotor per pesanan. Target aman = 70% laba kotor (sisakan 30% untuk biaya lain & laba). ROAS target = harga rata-rata / CPA target.
- Pesanan minimal agar anggaran bulan itu impas (syarat, bukan perkiraan).
- Batas uji: jumlah iklan aktif maksimum = anggaran minggu terkecil / (7 hari x minimum harian per iklan). Minimum harian adalah **aturan praktis Komunitech** (Meta 25rb, TikTok 30rb, Shopee 10rb, TikTok Shop 20rb, Google 25rb), bukan syarat platform: minta pengguna mengecek minimum di Ads Manager.
- Rupiah dibulatkan ke terdekat; total selalu sama dengan anggaran; sisa pembulatan ditampilkan dan ditambahkan ke bagian terbesar.
- **Tidak dihitung:** perkiraan penjualan, jumlah klik, CPM/CTR, "hasil yang akan didapat". Jangan mengarangnya.

## Format Output
Gunakan `templates/dokumen-strategi.md` sebagai kerangka. Isi:
1. **Ringkasan & asumsi** (3-5 baris: usaha, anggaran, tujuan, asumsi yang dipakai).
2. **Angka kunci**: margin, laba kotor per pesanan, ROAS impas & target, CPA impas & target, pesanan minimal impas.
3. **Strategi pilar konten**: tabel pilar (pilar | tahap | tujuan | 3 sudut | format | 5 judul contoh) + porsi konten.
4. **Rencana anggaran**: tabel kanal, tabel per minggu, batas uji, kanal yang tidak dipakai + alasan.
5. **Kreatif per tahap** dan rencana uji (1 variabel per uji: sudut pesan dulu, baru visual/hook).
6. **Kalender momen** bulan itu + bobot minggu yang dipakai.
7. **Aturan keputusan mingguan** dan tanda berhenti.
8. **Catatan kepatuhan** (kategori terbatas, klaim, hak cipta musik/foto, label konten AI).
9. **3 langkah pertama.**

## Contoh singkat
Masukan: "Toko kaos lokal, anggaran Rp5 juta, harga rata-rata Rp150.000, margin 40%, punya Shopee & IG."
Perintah: `python3 scripts/alokasi_anggaran.py --anggaran 5jt --aov 150rb --margin 40% --kanal meta,shopee`
Keluaran inti: Meta Rp3.181.818 (35/55), Shopee Rp1.818.182; ROAS impas 2,50x, target aman 3,58x; CPA maks Rp42.000. Lihat `examples/01-toko-kaos-shopee-ig.md` untuk dokumen lengkap.

## Batasan & penanganan error
- **Tanpa janji hasil.** Jangan menulis "pasti laku", "ROI pasti", atau angka penjualan perkiraan. Pembagian anggaran adalah titik awal yang dikoreksi lewat data mingguan.
- **Bukan pengelola iklan.** Tidak membuka akun iklan, tidak meminta password/OTP/token (bila pengguna menempelkannya: jangan diulang atau disimpan, sarankan diganti). Pengguna yang menekan tombol tayang.
- **Aturan platform berubah.** Tarif, minimum anggaran, format, dan kebijakan iklan diperbarui platform; skill ini tidak menyebut angka platform sebagai fakta selain minimum praktis di atas. Sarankan cek Ads Manager/Seller Center untuk keadaan terbaru.
- **Kategori terbatas:** kesehatan (jangan klaim sembuh/sebelum-sesudah/testimoni medis; iklan layanan kesehatan punya aturan khusus), keuangan (butuh izin & verifikasi; jangan janji untung), kripto (dilarang/butuh izin di banyak platform; jangan janji profit). Tandai "cek kebijakan iklan platform dan konsultasi pihak berwenang". Script menambah catatan ini otomatis lewat `--kategori`.
- **Klaim iklan** harus benar dan dapat dibuktikan (harga, stok, diskon asli, ulasan asli). Tidak memakai testimoni palsu, harga coret palsu, atau urgensi bohong (UU 8/1999 Perlindungan Konsumen; aturan platform).
- **Hitung margin dulu:** margin dari harga jual saja tanpa biaya admin/ongkir membuat target terlalu longgar. Minta pengguna memakai margin bersih dari biaya tersebut. PPN dan pajak lain tidak dihitung di skill ini.
- **Data pribadi pelanggan** (nomor WA, alamat) jangan dimasukkan ke dokumen strategi atau ke tabel audiens. Gunakan segmen umum.
- **Skrip gagal** (`GAGAL: ...`): tampilkan alasannya dalam bahasa sehari-hari, minta koreksi. Bila script tidak bisa dijalankan sama sekali, hitung manual dengan rumus di atas dan tulis "dihitung manual, belum diverifikasi script".
- Anggaran di bawah batas uji: katakan terus terang bahwa 1 kanal dengan 1 iklan adalah maksimum; sarankan mengumpulkan anggaran atau memperkuat konten organik dulu.
