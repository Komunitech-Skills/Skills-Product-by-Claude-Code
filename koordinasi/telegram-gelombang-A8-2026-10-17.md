# Gelombang Telegram A8 — 2026-10-17 (bot pertama) — bagian 1 & 2

Uji ini berlangsung di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A) di OpenClaw 2026.10.2, pada 17 Okt 2026 pukul 07:47–07:56 UTC, di topik baru 2183–2188. Pesan uji sama persis di sisi TANPA (topik dengan `skills: []`; selama sisi TANPA folder skill juga dipindah keluar HOME bot, dan log tidak menunjukkan akses ke folder skill) dan sisi DENGAN. Setiap sisi mendapat dua giliran: pesan utama, lalu lanjutan "ya". Pesan, lanjutan, dan kunci jawaban diambil dari `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json` (entri buku-stok, versi 1.1.7), dan pra-ceknya ada di `koordinasi/pracek-telegram-akun-a-2026-10-17.md` kelompok 5. Penilai independen (bukan pembuat skill) memakai skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Dua giliran dinilai sebagai satu jawaban. Angka kunci dihitung ulang dengan Decimal. Jawaban ganda yang identik di transkrip adalah salinan log dan hanya dihitung sekali.

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| buku-stok | 1.1.7 | 2183 / 2184 | 5,0 | 9,0 | +4,0 | **LULUS** | Dengan skill, Anda lebih dulu melihat ringkasan yang akan disimpan, lengkap dengan kode barang dan modal rata-rata Rp34.662. Data baru disimpan setelah Anda membalas "ya", lalu bot menyebut nilai stok Rp3.825.000. Tanpa skill, bot langsung menyimpan tanpa bertanya, mengarang rak penyimpanan dan "sisa 3 pcs" yang tidak pernah Anda sebut, serta menampilkan nama berkas. |

Pembanding uji internal lama (`skills/buku-stok/examples/00-openclaw-sebelum-sesudah.md`, v1.1.5, OpenClaw 2026.9.6 lokal): rata-rata SEBELUM 6,0 → SESUDAH 8,5 (LULUS). Pra-cek konteks Telegram 17 Okt (kelompok 5): 8,5, SIAP KIRIM.

## Rincian

### buku-stok 1.1.7 — TANPA 5,0 → DENGAN 9,0 (+4,0) LULUS

**Angka kunci (dihitung ulang, Decimal):**
- Biaya barang datang: 50 × 34.000 + 25.000 = Rp1.725.000. Ongkir per pcs 25.000 ÷ 50 = Rp500, jadi Rp34.500 per pcs.
- Kaos hitam M: (24 × 35.000 + 1.725.000) ÷ 74 = 2.565.000 ÷ 74 = 34.662,16, dibulatkan menjadi **Rp34.662**. Stok **74**.
- Nilai persediaan: 2.565.000 + 30 × 33.000 + 15 × 18.000 = **Rp3.825.000**.

Sisi DENGAN benar semua: Rp34.500 per pcs, stok 24 → 74, HPP Rp35.000 → Rp34.662, dan nilai persediaan Rp3.825.000. Sisi TANPA menulis stok 74 dan HPP "~Rp34.662" dengan benar, serta total biaya Rp1.725.000. Nilai persediaan tidak disebut.

Kutipan DENGAN:
> Siap, saya catat ya. Ini yang akan saya simpan (belum tersimpan):
> - Barang datang hari ini: Kaos Hitam M +50 @ Rp 34.000 (+ ongkir Rp 25.000, jadi Rp 34.500 per pcs) → stok 24 → 74. Modal rata-rata per barang (HPP) Rp 35.000 → Rp 34.662
> Kode barang saya buatkan dari nama barangnya; kalau mau diganti, tinggal bilang. Simpan? Balas "ya".
>
> (giliran 2) Sudah tersimpan. Stok sekarang: Kaos Hitam M 74, Kaos Putih M 30, Tote Bag Natural 15. Nilai persediaan (total modal yang tertahan di stok) Rp 3.825.000.

**Alasan skor DENGAN 9,0:**
- (+) Sesuai kunci: pratinjau dulu dengan "belum tersimpan" dan "Balas ya". Penyimpanan baru terjadi di giliran 2.
- (+) Kode barang (SKU) dijelaskan dan boleh diganti. Istilah HPP dijelaskan sebagai "modal rata-rata per barang". Nilai persediaan juga dijelaskan dengan bahasa awam.
- (+) Tidak ada jalur berkas atau kata proses. Kalimat "tersimpan di komputer ini" cukup jujur.
- (+) Ringkas: 1 pesan per giliran, tanpa tabel.
- (−) Margin per barang (jual − modal) tidak ditampilkan. Ini nilai tambah kecil yang mudah diberikan.
- (−) Penutup giliran 2 tidak memberi contoh kalimat untuk mencatat penjualan, misalnya "terjual 3 kaos hitam M".

**Alasan skor TANPA 5,0:** HPP dan stok 74 benar, termasuk ongkir yang ikut dihitung. Kekurangannya:
- Bot mengarang fakta. Kaos hitam M disebut "yang sudah ada di data, sisa 3 pcs @35rb", padahal pengguna menulis 24 pcs. Klaim ini juga tidak cocok dengan stok 74 yang ditulis bot sendiri. Lokasi rak "A3" dan "B4" juga tidak pernah disebut pengguna.
- Data langsung disimpan tanpa pratinjau atau konfirmasi. Giliran "ya" tidak menambah apa pun.
- Nama berkas `data/barang-masuk.csv` ditampilkan ke pembeli.
- Tidak ada kode barang dan tidak ada nilai persediaan. HPP ditulis dengan tanda "~" (kira-kira).

Catatan: rak dan "sisa 3 pcs" kemungkinan berasal dari data lama di workspace bot yang dipakai bersama, bukan dari pesan uji. Sisi DENGAN tidak terpengaruh, karena menghitung dari 24 pcs sesuai pesan. Untuk uji berikutnya, workspace bot sebaiknya dibersihkan sebelum sisi TANPA.

**Lintas cek:**
- Istilah proses atau jalur berkas: hanya di sisi TANPA.
- Tabel Markdown mentah: tidak ada.
- Terpotong: tidak ada.
- Panjang: 1 bagian per giliran di kedua sisi.

## Bagian 2 — kirim ulang 21 Okt 2026 (setelah router mati ±92 jam)

Router mati sejak 17 Okt ±07:56 UTC sampai 21 Okt ±04:25 UTC. Pengiriman ulang pertama (04:28–04:59 UTC) tidak diterima karena sambungan Telegram gateway macet setelah kontainer restart; antrean 3 pesan itu dibuang (getUpdates dengan offset eksplisit, saat gateway mati) supaya tidak dijawab belakangan, gateway dinyalakan ulang, lalu dikirim lagi 05:16–05:32 UTC. Sisi TANPA pph-final-umkm di topik 2187 timeout model (tidak sah) dan diulang sekali di topik baru 2226 (topik 2227 ikut terbuat, tidak dipakai). Penilai independen Opus untuk tiap skill, kriteria sama dengan bagian 1.

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| absensi-lokal | 1.0.8 | 2185 / 2186 | 6,5 | 7,5 | +1,0 | **BELUM** | Dengan skill, rekapnya lengkap dan benar semua (total menit telat, jam kerja, dan Andi 25/09 tanpa tap pulang yang terlewat tanpa skill), tetapi saat Anda membalas "ya" untuk menyimpan, bot malah bertanya ulang dan tidak menyimpan apa pun. |
| pph-final-umkm | 1.0.6 | 2226 / 2188 | 6,5 | 9,0 | +2,5 | **LULUS** | Angka sama di kedua sisi (kurang setor September Rp165.000, sudah lewat 15 Okt), tetapi tanpa skill bot keliru menyebut 2026 tahun terakhir tarif 0,5% (batas 7 tahun sudah dihapus PP 20/2026); dengan skill aturannya benar, ada ringkasan siap simpan dan pengingat surat pernyataan ke Shopee. |

Usulan perbaikan absensi-lokal (untuk Akun B): bila pertanyaan terakhir berbunyi 'Balas "ya" untuk simpan', anggap "ya" tunggal sebagai jawaban simpan, langsung simpan dan sebut jumlahnya ("121 catatan tersimpan: Andi 41, Sari 38, Joko 42"); hindari kata "kemarin" dalam percakapan yang sama. Usulan kecil pph-final-umkm: kalimat pembuka "Yang telat: kurang setor September Rp165.000", tambah langkah setor e-Billing + sanksi bunga, dan tanyakan potongan Shopee sebelum 1 Okt 2026.

### absensi-lokal 1.0.8 — TANPA 6,5 → DENGAN 7,5 (+1,0) BELUM

**Angka kunci (dihitung ulang dari CSV):**
- Berkas berisi **121 catatan**: Andi 41, Sari 38, Joko 42. Ada 22 hari kerja Senin–Jumat (01–30/09/2026) dan tidak ada tap di akhir pekan.
- Batas masuk dengan toleransi adalah 08.10. Andi terlambat **3x**: 02/09 08.23 (23 menit), 15/09 08.12 (12 menit), 22/09 08.31 (31 menit). Totalnya **66 menit = 1 jam 6 menit**. Joko terlambat **3x**: 03/09 08.14 (14 menit), 10/09 08.16 (16 menit), 24/09 08.45 (45 menit). Totalnya **75 menit = 1 jam 15 menit**. Sari **0x**.
- Hari kosong: **14/09 kosong untuk ketiga karyawan**. Sari juga kosong pada **21/09 dan 22/09**. Andi pada **25/09 hanya tap masuk (07.50), tanpa tap pulang**.
- Jam kerja dihitung sebagai (pulang − masuk − 1 jam), dengan menit dibulatkan ke bawah per hari, untuk hari yang tap-nya lengkap. Hasilnya: Andi 165 jam 18 menit, Sari 159 jam 19 menit, Joko 172 jam 57 menit. Angka ini cocok persis dengan sisi DENGAN.
- Kunci pra-cek terverifikasi sama.

Sisi DENGAN benar semua. Ini mencakup jumlah telat dan totalnya (1 jam 6 menit, 1 jam 15 menit), hadir 21/19/21 dari 22 hari, tiga hari kosong Sari, 14/09, dan 25/09 Andi tanpa tap pulang. Sisi TANPA juga benar untuk jumlah telat, tanggal, jam telat, dan hari kosong. Total menit telat tidak disebut, dan **25/09 Andi tanpa tap pulang terlewat**.

Kutipan DENGAN:
> 1. Andi — Hadir 21 dari 22 hari kerja | Tanpa keterangan 1 — Terlambat 3x (total 1 jam 6 menit) — Jam kerja 165 jam 18 menit (+1 hari data tidak lengkap, belum dihitung)
> PERLU DICEK: Andi, 25/09: cuma ada jam masuk (07.50), jam pulangnya gak kecatat
> 3. Mau saya simpan data ini biar bulan depan tinggal upload file baru aja …? Balas "ya" kalau mau.
>
> (giliran 2) Mau konfirmasi dulu ya Kak, soalnya "ya" tadi menjawab yang mana nih — ada 3 hal yang saya tanyakan kemarin … tolong konfirmasi biar datanya yang tersimpan nanti benar, bukan saya tebak sendiri

**Alasan skor DENGAN 7,5:**
- (+) Semua angka kunci benar, termasuk total menit telat dan jam kerja per orang. Hari yang tap-nya tidak lengkap dikeluarkan dari hitungan jam kerja, dan hal itu disebut terus terang.
- (+) Menangkap 25/09 Andi tanpa tap pulang sebagai "PERLU DICEK". Hari kosong disebut "belum ada keterangan izin/sakit/cuti", bukan langsung dicap alpa.
- (+) Jujur soal asumsi: tanggal merah belum dimasukkan, dan 14/09 ditanyakan sebagai kemungkinan toko tutup. Ada tepat 3 pertanyaan di akhir. Tidak ada jalur berkas atau kata proses. Bahasanya awam dan siap dibaca.
- (−) **Giliran 2 gagal.** Bot sendiri menulis 'Balas "ya" kalau mau' pada pertanyaan no. 3, tetapi balasan "ya" tidak ditindaklanjuti dengan menyimpan data. Kunci uji mengharapkan 121 catatan tersimpan (Andi 41, Sari 38, Joko 42). Bot malah bertanya ulang, dan tidak ada konfirmasi tersimpan maupun jumlah catatan. Pengguna awam akan bingung karena sudah menjawab sesuai instruksi.
- (−) Kata "kemarin" di giliran 2 tidak tepat, karena pertanyaan itu baru diajukan beberapa saat sebelumnya.
- (−) Ringkasan hari bolong ditulis dua kali, di daftar per orang dan di daftar "Hari bolong". Ini sedikit berulang.

**Alasan skor TANPA 6,5:**
- (+) Jumlah telat, tanggal, dan jam telat benar untuk ketiga karyawan. Hari kosong 14/09, 21/09, dan 22/09 benar. Jumlah 22 hari kerja benar.
- (+) Tafsiran 14/09 masuk akal: kemungkinan toko tutup, perlu dicek. Ringkas dan mudah dibaca.
- (−) **25/09 Andi tanpa tap pulang terlewat.** Ini temuan "bolong" yang justru ditanyakan pengguna.
- (−) Tidak ada total menit telat, jam kerja, atau jumlah hadir. Rekapnya kurang siap pakai untuk potongan gaji atau evaluasi.
- (−) Tidak ada tawaran untuk menyimpan data untuk bulan berikutnya. Balasan "ya" ditanggapi dengan "aku diam aja di sini", yang terdengar seperti kalimat proses dan kurang membantu.

**Perbaikan paling berdampak (urut dampak):**
1. Bila pertanyaan terakhir berbunyi 'Balas "ya" untuk simpan', anggap "ya" tunggal sebagai jawaban untuk penyimpanan. Langsung simpan dan konfirmasi jumlah catatan, misalnya "121 catatan tersimpan: Andi 41, Sari 38, Joko 42". Pertanyaan 1–2 yang belum dijawab tetap dicatat "tanpa keterangan" dan bisa diubah nanti.
2. Letakkan pertanyaan simpan sebagai satu-satunya pertanyaan yang dijawab "ya", atau beri kode balasan per pertanyaan (mis. "balas 1 tutup / 2 izin / ya simpan") agar tidak ambigu.
3. Hindari kata waktu yang tidak akurat seperti "kemarin" dalam percakapan yang sama.
4. Gabungkan daftar hari bolong ke satu tempat agar pesan lebih ringkas.

### pph-final-umkm 1.0.6: TANPA 6,5 → DENGAN 9,0 (+2,5), LULUS

**Angka kunci (dihitung ulang, Decimal; PPh dibulatkan ke bawah):**
- Omzet kumulatif: Jan–Jul Rp448.500.000. Agustus Rp521.500.000, jadi bulan ini melewati Rp500 juta. September Rp587.500.000.
- Agustus: yang kena pajak hanya 521,5 jt − 500 jt = Rp21.500.000. PPh final 0,5% = **Rp107.500**. September: 0,5% × 66 jt = **Rp330.000**. Total Jan–Sep **Rp437.500**.
- PPh 22 Shopee yang dikurangkan per bulan (total Rp345.000):
  - Agustus: dipungut 180.000, terutang 107.500, jadi **lebih dipungut Rp72.500**.
  - September: dipungut 165.000, terutang 330.000, jadi **kurang setor Rp165.000**.
- Batas setor September jatuh Kamis 15 Okt 2026, hari kerja. Per 21 Okt, **sudah lewat 6 hari**.
- Sisa sebelum ambang Rp4,8 M: 4.800.000.000 − 587.500.000 = **Rp4.212.500.000**.

Kedua sisi benar untuk semua angka di atas. Sisa batas Rp4,8 M hanya ada di sisi DENGAN.

**Fakta yang hanya disebut satu sisi (dicek):**
- **Batas 7 tahun (hanya TANPA).** TANPA menulis: "jatah 0,5% … cuma 7 tahun pajak: 2020–2026 … Mulai 2027 wajib pindah ke tarif normal." Menurut aturan lama (PP 55/2022 Pasal 59), hitungan itu benar karena 2020–2026 memang 7 tahun. Namun PP 20/2026 (diundangkan 22 April 2026) Pasal I angka 6 **menghapus Pasal 59**. Orang pribadi kini memakai 0,5% tanpa batas tahun selama omzet ≤ Rp4,8 M (dicocokkan dengan `references/regulasi.md` skill, yang merujuk naskah JDIH Kemenkeu dan salindia DJP). Jadi pernyataan TANPA **salah menurut aturan yang berlaku**, dan sarannya berdampak nyata: menyiapkan pindah ke pembukuan/NPPN untuk 2027 tidak perlu. Ini salah fakta, bukan salah angka kunci, jadi batas maks 5 tidak berlaku. Skor tetap dipotong cukup besar. Catatan: penilai tidak membaca naskah PP 20/2026 sendiri. Status "dihapus" diambil dari rujukan skill yang menyebut sumber resmi.
- **Surat pernyataan ke Shopee (hanya DENGAN).** Bila omzet melewati Rp500 juta, surat pernyataan dikirim paling lambat akhir bulan saat ambang terlewati, yaitu 31 Agustus 2026. Hal ini sesuai FAQ DJP PMK 37/2025 no. 9 menurut rujukan skill. Benar dan relevan.
- **Kelebihan Agustus.** TANPA menulis "dicatat untuk nanti direkonsiliasi di SPT Tahunan". Untuk PPh final, ini kurang tepat. FAQ DJP mengatur bahwa selisih lebih diajukan pengembalian (permohonan pengembalian pajak yang seharusnya tidak terutang), bukan dikompensasi di SPT. DENGAN menulis "bisa diajukan pengembalian ke DJP", sesuai rujukan.
- **Kode setor (hanya TANPA).** Kode akun 411128 dengan jenis setoran 420 memang kode umum PPh final UMKM. Ini nilai tambah kecil yang benar.
- **Waktu mulai pungutan Shopee.** Rujukan skill mencatat pemungutan Shopee dimulai 1 Okt 2026 (rencana 1 Agustus ditunda), padahal pengguna menyebut ada potongan di Agustus–September. Kedua sisi menerima angka pengguna tanpa bertanya. Kekurangan kecil yang sama di kedua sisi, jadi tidak dihukum.

**Kutipan DENGAN:**
> **September** · omzet Rp66.000.000 · PPh Rp330.000
> Dipungut marketplace Rp165.000; kurang Rp165.000, setor sendiri paling lambat Kamis 15 Okt 2026 (SUDAH LEWAT).
> …
> - Tarif 0,5% untuk orang pribadi kini tanpa batas tahun (PP 20/2026 menghapus batas 7 tahun lama), selama omzet setahun tidak lebih dari Rp4,8 miliar.

**Alasan skor DENGAN 9,0:**
- (+) Semua angka kunci benar. Ada baris "Hari ini". Bulan yang sudah lewat batas setor ditandai, termasuk nama harinya. Ringkasan berisi total, pungutan, kurang dan lebih bayar, serta sisa batas Rp4,8 M.
- (+) Aturan terbaru disebut dengan benar: batas 7 tahun sudah dihapus. Omzet online dan toko rumah digabung. Ada pengingat surat pernyataan ke Shopee. Kelebihan disebut "bisa diajukan pengembalian".
- (+) Mencantumkan dasar aturan dan disclaimer singkat (Kring Pajak 1500200). Tidak ada kata proses atau jalur berkas, dan tidak ada tabel mentah. Tiga pertanyaan penutup relevan, diletakkan setelah pekerjaan selesai.
- (−) Kalimat pembuka janggal dan bisa membingungkan: "Tidak ada yang telat dari potongan Shopee kecuali September". Lebih jelas bila ditulis "Yang telat: kurang setor September Rp165.000".
- (−) Tidak ada langkah setor praktis (e-Billing, kode setor) dan tidak menyebut sanksi bunga keterlambatan. Sisi TANPA justru menyebut keduanya.
- (−) Tidak mempertanyakan potongan Shopee di Agustus–September, padahal rujukan skill sendiri mencatat pemungutan baru dimulai 1 Oktober.

**Alasan skor TANPA 6,5:**
- (+) Semua angka kunci benar. Hitungan kumulatif per bulan ditulis terbuka. Batas setor lewat 6 hari terdeteksi. Ada langkah cepat (e-Billing dengan kode setor, STP bunga, Kring Pajak), dan bot jujur bahwa tarif bunga tidak bisa dipastikan.
- (−) Salah fakta yang menonjol: menyebut 2026 sebagai tahun terakhir tarif 0,5% dan menyuruh pindah ke tarif normal mulai 2027, padahal batas itu sudah dihapus PP 20/2026. Hal ini ditempatkan sebagai "poin penting" paling atas, jadi menyesatkan.
- (−) Perlakuan kelebihan pungutan kurang tepat (disebut rekonsiliasi SPT Tahunan, seharusnya pengajuan pengembalian). Penjelasan "basisnya beda" lalu tetap dikreditkan juga agak membingungkan.
- (−) Tidak ada pengingat surat pernyataan ke Shopee dan tidak ada sisa batas Rp4,8 M. Bot juga menyebut tidak bisa akses internet, kalimat proses yang tidak perlu untuk pembeli.

**Lintas cek:**
- Istilah proses atau jalur berkas: tidak ada di DENGAN. TANPA menulis "nggak bisa akses internet live".
- Tabel Markdown mentah: tidak ada di kedua sisi.
- Terpotong: tidak ada.
- Panjang: 1 pesan per sisi, keduanya masih wajar untuk chat.

## Catatan Akun A (17 Okt)
Sisi TANPA buku-stok (2183) kemungkinan membaca berkas sisa uji lain di workspace bot (`data/stok.csv`, `data/lokasi-rak.csv` dari A1 resi-picking) — asal "sisa 3 pcs" & rak A3/B4. Pengaruhnya menurunkan skor TANPA, jadi selisih +4,0 mungkin sedikit lebih besar dari semestinya; walau TANPA dinaikkan ke 7, selisih tetap ≥ 1,5 (LULUS tetap). Sejak 08:05 UTC sisa berkas uji lama di workspace bot dipindahkan ke cadangan scratchpad sebelum tiap gelombang.
