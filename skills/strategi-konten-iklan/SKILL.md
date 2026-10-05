---
name: strategi-konten-iklan
description: Menyusun pilar konten (3-5 pilar, sudut pesan, format, corong) DAN membagi anggaran iklan BULAN INI per kanal per minggu (Meta/Instagram, TikTok, Shopee Ads, TikTok Shop Ads, Google Ads) untuk UMKM Indonesia dengan anggaran Rp500rb-Rp20jt per bulan; target CPA, ROAS, titik impas dari margin dan harga rata-rata, tujuan campuran (mis. awareness 30% + penjualan 70%), dan batas uji dihitung script. Pakai untuk "bagi anggaran iklan Rp5 juta ke IG/TikTok/Shopee", content pillar, target ROAS/CPA, "iklan saya harus mulai dari mana". Aturan: KERJAKAN DULU, TANYA DI AKHIR - bila anggaran & margin sudah disebut, langsung beri ROAS impas (1/margin), rencana iklan ringkas dengan [isian], dan tolak klaim berlebihan disertai dasar aturannya; tidak ada ROAS "pasti"; jangan menyebut proses internal (script, file, cek). BUKAN untuk rencana marketing menyeluruh 1-12 bulan (gunakan rencana-marketing-usaha). Content strategy, content pillars, monthly paid ads budget split, media plan, break-even ROAS.
---

# Strategi Konten & Anggaran Iklan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menjawab dua pertanyaan pemilik usaha dalam **satu dokumen**: (1) "konten apa yang harus saya buat, dan untuk siapa di tahap mana?" dan (2) "uang iklan bulan ini dibagi ke mana, berapa per minggu, dan berapa hasil minimal supaya tidak rugi?". Semua angka uang dihitung **script**, bukan dikira.

## Aturan utama: kerjakan dulu, tanya di akhir
Jika pengguna sudah menyebut **produk**, **anggaran**, dan **margin**, JANGAN membalas hanya dengan pertanyaan (mis. menunggu harga rata-rata/AOV). Dalam **satu balasan yang sama**, berurutan:
1. **Tolak klaim bermasalah + dasar aturan** bila ada (mis. "turun 5 kg seminggu", "pasti sembuh", "ROAS pasti"): jelaskan klaim itu tidak bisa dibuktikan dan melanggar aturan, sebut dasarnya dari `references/kepatuhan-klaim-iklan.md` (UU 8/1999 Perlindungan Konsumen, aturan label & iklan pangan/BPOM, izin edar), dan beri 2-3 tagline pengganti yang aman. Produk makanan/minuman/suplemen/pelangsing: pengguna perlu memastikan izin edar BPOM dan klaim sesuai izin.
2. **ROAS impas = 1 / margin langsung** (margin 40% = 2,5x; CPA impas = laba kotor per pesanan) tanpa menunggu AOV. Jelaskan dengan bahasa sehari-hari: di bawah angka itu iklan merugi; angka itu batas, bukan hasil. **Tidak ada "ROAS pasti"**: ROAS baru diketahui dari data iklan yang berjalan; yang bisa dipastikan hanya batas impas dan target aman.
3. **Rencana iklan ringkas** dari anggaran: bagi per kanal & per minggu (bantu angka dari alat hitung; tulis dibulatkan), 3 pilar konten + contoh judul aman, aturan keputusan mingguan, dengan `[isian: AOV]`/`[isian: kanal yang dipakai]` untuk data yang kurang; sebut asumsinya.
4. **Maks. 3 pertanyaan di akhir** (mis. harga rata-rata per pesanan, jualan di marketplace mana, sudah punya izin edar?). Hanya **anggaran atau margin yang benar-benar kosong** yang boleh menahan rencana.

**Dilarang menulis kata proses ke pengguna:** "script", "saya jalankan", "dihitung pakai script", "file", "LULUS/GAGAL". Tulis hasil hitungannya saja; bila alat hitung tidak bisa dijalankan, tulis singkat "dihitung manual".

## Kapan digunakan
- "Saya punya Rp3 juta untuk iklan sebulan, bagi ke IG/TikTok/Shopee dong."
- "Konten toko saya harus fokus ke apa? Bingung mau posting apa."
- "Berapa ROAS minimal supaya iklan saya tidak rugi? Margin saya 35%."
- Menyiapkan bulan promo 11.11/12.12, Ramadan/Lebaran, tahun ajaran baru.

## Kapan TIDAK digunakan
- **Rencana marketing menyeluruh** (analisis pasar, target pasar, tujuan & KPI, kanal organik + berbayar + offline, rencana 1-12 bulan) -> gunakan `rencana-marketing-usaha`; skill ini hanya menjawab "uang iklan BULAN INI dibagi ke mana per kanal per minggu" dan pilar kontennya. Bila pengguna butuh keduanya, susun rencana marketing dulu lalu pakai skill ini untuk bulan yang berjalan.
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
| Tujuan bulan ini: penjualan / awareness / leads (calon pembeli via WA/formulir), boleh campuran berporsi (mis. awareness 30% + penjualan 70%) | Tidak | penjualan (disebut sebagai asumsi) |
| Jenis usaha untuk memilih kanal bila uang tipis: jualan di marketplace / jasa lokal (bengkel, servis, klinik) / lainnya | Tidak | umum; tanyakan bila anggaran < Rp2jt |
| Harga rata-rata per pesanan (AOV) | Wajib untuk penjualan & leads | tanyakan |
| Margin kotor (setelah harga pokok, biaya admin marketplace, ongkir yang ditanggung) | Wajib untuk penjualan & leads | tanyakan; bantu hitung dari harga jual - modal - biaya |
| Persen calon pembeli yang jadi membeli (khusus leads) | Wajib untuk leads | tanyakan |
| Kanal yang dipakai/punya toko (IG, TikTok, Shopee, TikTok Shop, Google) | Tidak | Semua yang cocok; **Shopee/TikTok Shop Ads hanya bila punya toko di sana** |
| Penjualan selama ini paling banyak terjadi di mana (Shopee, TikTok Shop, DM IG/WA, situs) | Wajib bila punya toko marketplace DAN kanal lain | tanyakan; bila pengguna ingin cepat dan punya toko marketplace, anggap marketplace itu kanal utama (sebut asumsinya) |
| Bulan rencana & momen belanja | Tidak | bulan berjalan (tulis di asumsi); momen **wajib** dari `scripts/alokasi_anggaran.py --momen TAHUN-BULAN` / tabel `references/momen-belanja.md`; tanggal yang berubah tiap tahun tidak ditebak |
| Kategori produk | Tidak | umum; kesehatan/keuangan/kripto diberi catatan aturan iklan |
| Kemampuan produksi konten (video/minggu) | Tidak | 3 konten/minggu per kanal utama |

Jika produk, anggaran, dan margin sudah ada: kerjakan dulu (Aturan utama), tanyakan maks. 3 hal di akhir. Jika salah satunya kosong, tanyakan **sekali** (maks. 6 pertanyaan bernomor dalam satu pesan). Bila pengguna ingin cepat, pakai default dan tulis asumsinya di awal dokumen.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Cek kelayakan.** Anggaran < Rp100rb/bulan atau margin belum dikenal -> bantu dulu hitung margin; jangan menebak. Margin sangat tipis (ROAS impas >= 10x, margin <= 10%) atau nol/negatif -> sarankan perbaiki harga/margin dulu sebelum beriklan (`strategi-harga-produk`, `hitung-hpp`). Kategori terlarang -> tolak. Kategori kesehatan/keuangan/kripto -> lanjut dengan catatan pembatasan (lihat Batasan).
2. **Bangun 3-5 pilar konten** memakai `references/pilar-konten.md`: pilih dari kebutuhan pembeli (pertanyaan yang sering masuk ke WA/DM, keberatan sebelum beli, alasan repeat order), bukan dari selera pemilik. Tiap pilar: tujuan, tahap corong (awareness/pertimbangan/beli/repeat), 3 sudut pesan, format, contoh 5 judul konkret untuk usaha itu. Promosi langsung maksimal +-30% dari total konten.
3. **Petakan corong ke iklan.** Konten yang sudah dapat respons organik baik (simpan/bagikan/tanya harga) boleh diiklankan; konten baru diuji kecil dulu. Kreatif berbeda per tahap: awareness (cerita/hook), pertimbangan (bukti: ulasan asli, demo), beli (penawaran + batas waktu asli). **Retargeting** (sisihkan dari porsi 'aman', bukan tambahan): sasar orang yang sudah menonton video, mengunjungi toko/profil, atau chat WA tetapi belum membeli; kreatif = jawaban keberatan, ulasan asli, penawaran nyata berbatas waktu; jangan memakai daftar nomor/data pelanggan tanpa persetujuan mereka dan sesuai aturan platform.
4. **Hitung anggaran dengan script** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 scripts/alokasi_anggaran.py --anggaran 10jt --tujuan penjualan --aov 150rb --margin 40% \
     --kanal meta,tiktok,shopee --bobot-minggu 1 1 1 2 --kategori umum
   ```
   Opsi: `--tujuan awareness|penjualan|leads` atau campuran `--tujuan awareness:30,penjualan:70` (total porsi wajib 100; jangan dibagi/dijumlah tangan), `--jenis umum|marketplace|jasa-lokal`, `--kanal-utama shopee` (kanal tempat penjualan terbanyak; porsinya dibuat 2x kanal pendukung terbesar, kecuali tujuan awareness murni; default Shopee/TikTok Shop bila `--jenis marketplace`), `--closing 20%` (leads), `--minggu 1-5`, `--min-harian 20rb`, `--momen 2026-10` (cetak momen bulan itu dari tabel referensi + minggu script + saran `--bobot-minggu`; boleh tanpa `--anggaran`), `--json`. Alias kanal diterima: `ig`, `instagram`, `fb`, `facebook`, `tiktok shop`, `tokopedia` (dihitung sebagai TikTok Shop Ads), `google ads`. Margin nol/negatif ditolak dengan penjelasan (setiap penjualan rugi). Angka diterima gaya Indonesia: `1.500.000`, `1,5jt`, `500rb`, `2 juta`. Angka **ambigu** (`1,500`, `1.5`, `5M`, margin `0,4`) **ditolak** dengan pesan jelas: tanyakan ulang ke pengguna, jangan ditebak.
   **Wajib benar-benar menjalankan script** setiap kali angka anggaran disusun atau berubah (termasuk giliran lanjutan setelah pengguna menjawab pertanyaan). Kata "script"/"dihitung pakai script" **tidak boleh muncul di jawaban ke pengguna** (lihat Aturan utama); angka tetap harus berasal dari script yang benar-benar dijalankan pada giliran itu. Bila tidak bisa menjalankan alat, ikuti aturan "Skrip gagal" di Batasan dan tulis singkat "dihitung manual".
   **Kanal penjualan utama:** penjual yang transaksinya terjadi di marketplace (mis. Shopee) dipasang `--jenis marketplace` atau `--kanal-utama shopee`, sehingga iklan marketplace (Shopee Ads) mendapat porsi terbesar dan Meta/TikTok menjadi pendukung. Bila penjualan terbanyak lewat DM IG/WA, pakai `--kanal-utama meta`. Jangan membenarkan porsi terbesar untuk kanal yang bukan tempat pembeli bertransaksi tanpa alasan dari pengguna.
5. **Baca keluaran script apa adanya.** Salin tabel kanal, tabel minggu, target impas, dan batas uji ke dokumen. Jangan mengubah angka tangan. Bila script menyingkirkan kanal jelaskan alasannya dengan bahasa awam: "uangnya terlalu tipis untuk diuji di kanal itu; fokus dulu ke kanal yang cukup" (anggarannya sudah dialihkan; total tetap).
   **Aturan pemilihan kanal saat uang tipis (dihitung script, jelaskan ke pengguna):** (a) kanal layak bila minggu TERKECIL-nya cukup untuk 1 iklan selama 7 hari (dasar yang sama dengan kolom "iklan aktif maks"); (b) bila kanal berprioritas tertinggi sendiri tidak layak, kanal berprioritas lebih rendah dibuang agar uang terpusat di sana; bila tidak, kanal tidak layak berprioritas terendah yang dibuang; (c) bila satu kanal pun tidak layak, dicari kanal lain yang layak dengan seluruh anggaran, kalau tidak ada tabel diberi tanda "DI BAWAH BATAS" plus catatan. Prioritas menurut `--jenis`: marketplace = Shopee, TikTok Shop, Meta, TikTok, Google; jasa-lokal = Google, Meta, TikTok; umum = menurut bobot tujuan. **Pilih `--jenis` dari jawaban pengguna** (mis. jual di Shopee -> `marketplace`; bengkel/servis/klinik lokal -> `jasa-lokal`); untuk jasa lokal yang mengandalkan WA/DM boleh juga tawarkan `--kanal meta`. Tanpa `--kanal` eksplisit atau `--jenis marketplace`, Shopee/TikTok Shop tidak dipakai sebagai kanal pengganti (belum tentu punya toko).
6. **Susun dokumen** sesuai Format Output. **Momen bulan itu wajib dicek, bukan diingat:** tulis bulan yang dipakai di asumsi (bila pengguna tidak menyebut, pakai bulan berjalan), jalankan `python3 scripts/alokasi_anggaran.py --momen TAHUN-BULAN` (atau cocokkan sendiri ke tabel `references/momen-belanja.md` bila script tidak bisa dijalankan) dan salin hasilnya ke Kalender momen. **Dilarang** menulis "bulan ini tidak ada momen" tanpa cek itu: tanggal kembar 9.9, 10.10, 11.11, 12.12 jatuh tiap September-Desember, gajian ada tiap bulan, Ramadan/Lebaran ditanyakan. **Nama & tanggal momen diambil apa adanya dari tabel `references/momen-belanja.md`**, jangan dari ingatan: Harbolnas (Hari Belanja Online Nasional) = **12.12**; 11.11 adalah tanggal kembar, **bukan** Harbolnas. Sebutkan juga bahwa script menghitung 4 x 7 = 28 hari; sisa hari di bulan 30/31 hari dipakai evaluasi. Sertakan kalender momen dan aturan keputusan mingguan (`references/aturan-keputusan.md`): kapan lanjut, kapan hentikan, kapan tambah anggaran.
7. **Tutup** dengan 3 langkah pertama yang bisa dikerjakan hari ini dan tawaran skill lanjutan (kalender 30 hari, caption, laporan iklan mingguan).

## Yang dihitung script (dan yang TIDAK)
- Pembagian anggaran per kanal menurut tujuan (titik awal, bisa diubah; tujuan campuran = rata-rata tertimbang bobot tiap tujuan sesuai porsinya) dan per minggu (bobot minggu untuk momen). Aman 70% / uji 30% per kanal.
- Titik impas ROAS = 1 / margin (dibulatkan ke atas 2 desimal, tidak pernah dianggap lebih ringan dari kenyataan). CPA impas = laba kotor per pesanan. Target aman = 70% laba kotor (sisakan 30% untuk biaya lain & laba). ROAS target = harga rata-rata / CPA target.
- Pesanan minimal agar anggaran bulan itu impas (syarat, bukan perkiraan).
- Batas uji: jumlah iklan aktif maksimum = anggaran minggu terkecil / (7 hari x minimum harian per iklan). Minimum harian adalah **aturan praktis Komunitech** (Meta 25rb, TikTok 30rb, Shopee 10rb, TikTok Shop 20rb, Google 25rb), bukan syarat platform: minta pengguna mengecek minimum di Ads Manager.
- Rupiah dibulatkan ke terdekat; total selalu sama dengan anggaran; sisa pembulatan ditampilkan dan ditambahkan ke bagian terbesar.
- **Tidak dihitung:** perkiraan penjualan, jumlah klik, CPM/CTR, "hasil yang akan didapat". Jangan mengarangnya.

## Checklist sebelum mengirim
- [ ] Klaim bermasalah ditolak dengan dasar aturan + tagline pengganti.
- [ ] ROAS impas (1/margin) langsung disebut tanpa menunggu AOV; dijelaskan tidak ada ROAS "pasti".
- [ ] Rencana iklan ringkas ada di chat dengan `[isian]`; pertanyaan maks. 3 dan di akhir.
- [ ] Tidak ada kata proses (script, file, cek, LULUS/GAGAL).

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
Masukan: "Toko kaos lokal, anggaran Rp5 juta, harga rata-rata Rp150.000, margin 40%, punya Shopee & IG, kebanyakan pesanan masuk lewat Shopee."
Perintah: `python3 scripts/alokasi_anggaran.py --anggaran 5jt --aov 150rb --margin 40% --kanal meta,shopee --jenis marketplace`
Keluaran inti: Shopee Ads Rp3.333.333 (kanal utama, 2x Meta), Meta Rp1.666.667; ROAS impas 2,50x, target aman 3,58x; CPA maks Rp42.000. (Tanpa `--jenis marketplace`/`--kanal-utama`, Meta mendapat porsi terbesar: cocok hanya bila penjualan terbanyak lewat DM IG/WA.) Lihat `examples/01-toko-kaos-shopee-ig.md` untuk contoh dokumen lengkap (dibuat dengan versi sebelum aturan kanal utama).

## Batasan & penanganan error
- **Tanpa janji hasil.** Jangan menulis "pasti laku", "ROI pasti", atau angka penjualan perkiraan. Pembagian anggaran adalah titik awal yang dikoreksi lewat data mingguan.
- **Bukan pengelola iklan.** Tidak membuka akun iklan, tidak meminta password/OTP/token (bila pengguna menempelkannya: jangan diulang atau disimpan, sarankan diganti). Pengguna yang menekan tombol tayang.
- **Aturan platform berubah.** Tarif, minimum anggaran, format, dan kebijakan iklan diperbarui platform; skill ini tidak menyebut angka platform sebagai fakta selain minimum praktis di atas. Sarankan cek Ads Manager/Seller Center untuk keadaan terbaru.
- **Kategori terbatas:** kesehatan (jangan klaim sembuh/sebelum-sesudah/testimoni medis; iklan layanan kesehatan punya aturan khusus), keuangan (butuh izin & verifikasi; jangan janji untung), kripto (dilarang/butuh izin di banyak platform; jangan janji profit). Tandai "cek kebijakan iklan platform dan konsultasi pihak berwenang". Script menambah catatan ini otomatis lewat `--kategori` (kata kunci seperti skincare, kosmetik, suplemen, obat, klinik, pinjaman, investasi, asuransi, kripto ikut dikenali); tetap cek sendiri bila kategori tidak terdeteksi.
- **Klaim iklan** (dasar & sumber lengkap: `references/kepatuhan-klaim-iklan.md`) harus benar dan dapat dibuktikan (harga, stok, diskon asli, ulasan asli). Tidak memakai testimoni palsu, harga coret palsu, atau urgensi bohong (UU 8/1999 Perlindungan Konsumen; aturan platform).
- **Hitung margin dulu:** margin dari harga jual saja tanpa biaya admin/ongkir membuat target terlalu longgar. Minta pengguna memakai margin bersih dari biaya tersebut. PPN dan pajak lain tidak dihitung di skill ini.
- **Data pribadi pelanggan** (nomor WA, alamat) jangan dimasukkan ke dokumen strategi atau ke tabel audiens. Gunakan segmen umum.
- **Skrip gagal** (`GAGAL: ...`): tampilkan alasannya dalam bahasa sehari-hari, minta koreksi. Bila script tidak bisa dijalankan sama sekali, hitung manual dengan rumus di atas dan tulis "dihitung manual, belum diverifikasi script".
- Anggaran di bawah batas uji: katakan terus terang bahwa 1 kanal dengan 1 iklan adalah maksimum; sarankan mengumpulkan anggaran atau memperkuat konten organik dulu.
