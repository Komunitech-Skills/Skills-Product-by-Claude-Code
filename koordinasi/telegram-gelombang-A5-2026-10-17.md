# Gelombang Telegram A5 — 2026-10-17 (bot pertama)

Uji ini berlangsung di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A) di OpenClaw 2026.10.2, pada 17 Okt 2026 pukul 06:12–06:27 UTC, di topik baru 2072–2079. Pesan uji sama persis di sisi TANPA (topik dengan `skills: []`) dan DENGAN skill. Pesan dan kunci jawaban diambil dari `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json`, dan pra-ceknya ada di `koordinasi/pracek-telegram-akun-a-2026-10-17.md`. Penilai 1 (independen, bukan pembuat skill) memakai skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Semua angka kunci dihitung ulang dengan Decimal: data kasir+CRM dari isi `pilot/seed-laporan-harian.sh` (kemarin 2026-10-16, hari ini 2026-10-17), CSV dari `pilot/data-a-cepat/rekap-penjualan-csv/penjualan-september.csv`, tanggal dan nama hari dengan kalender Python, dan aturan tenggat dari `skills/kalender-pajak/SKILL.md` (PMK 81/2024). Bukti kirim dicocokkan ke log gateway `gw-20261017-0612.log`. Jawaban ganda yang identik di transkrip adalah salinan log dan hanya dihitung sekali.

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka atau fakta kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| laporan-harian-usaha | 1.1.4 | 2072 / 2073 | 3,5 | 8,0 | +4,5 | **LULUS** (batas bawah DENGAN) | Dengan skill, Anda langsung mendapat rekap dari kasir dan buku calon pembeli Anda sendiri: omzet hari ini Rp172.600, turun 3,6% dari kemarin, ada 1 follow-up yang terlambat, dan pengingat bahwa kasir belum ditutup. Tanpa skill, bot memakai berkas contoh yang tertinggal di folder, jadi angkanya bukan angka toko Anda, dan bot tidak bisa membandingkan dengan kemarin. |
| buku-piutang | 1.0.5 | 2074 / 2075 | 7,5 | ~~4,0~~ | ~~−3,5~~ | **DIBATALKAN** (pemeriksa kedua: TIDAK SAH, izin "ya" belum dikirim) → diganti A7: 7,5 (TANPA A5, topik 2074) → 8,5 (DENGAN A7, topik 2125), dua putaran berbeda, BELUM (+1,0) | Dengan skill, balasan pertama hanya meminta izin membuat buku piutang ("balas ya"). Belum ada daftar siapa yang menunggak dan belum ada draf tagihan. Tanpa skill, bot langsung mencatat bon, menghitung sisa dan keterlambatan dengan benar, lalu memberi draf pesan tagih. |
| kalender-pajak | 1.0.7 | 2076 / 2077 | 5,5 | 8,0 | +2,5 | **LULUS** | Dengan skill, setelah profil dijawab Anda mendapat kepastian: Oktober tidak ada setoran, omzet baru lewat Rp500 juta di November, dan setoran pertama paling lambat Selasa, 15 Desember 2026. Tanpa skill, bot memberi tanggal setor PPh 21/23 yang sudah tidak berlaku (10 Oktober, padahal kini tanggal 15) dan berhenti dengan pertanyaan lagi, tanpa kesimpulan. |
| rekap-penjualan-csv | 1.2.5 | 2078 / 2079 | 8,0 | 6,5 | −1,5 | **BELUM** | Kedua versi menghitung omzet Rp5.519.000 dan produk terlaris dengan benar. Versi dengan skill menambah rincian batal/refund dan persentase, tetapi bagian "Insight" salah: Topi Baseball disebut paling banyak terjual dan paling murah, padahal yang paling banyak terjual dan paling murah adalah Tote Bag. |

Pembanding: pra-cek konteks Telegram 17 Okt memberi keempat skill status SIAP KIRIM (8,0 / 8,0 / 8,0 / 8,5). Di bot asli dua skill turun: buku-piutang karena buku piutang baru pertama kali dibuat di bot ini (pra-cek tidak menangkap langkah izin awal), rekap-penjualan-csv karena salah tafsir di bagian insight.

Catatan lintas skill:
- **Istilah proses atau jalur berkas yang tampil:**
  - laporan-harian-usaha DENGAN menyebut nama alat lain ("buku-stok, absensi-lokal, dan pengingat-follow-up belum dipakai di komputer ini") dan singkatan "CRM" tanpa penjelasan. Nama alat itu tidak bermakna bagi pembeli; lebih baik "data stok, absensi, dan tagihan belum dicatat".
  - laporan-harian-usaha TANPA menyebut jalur `laporan/masuk/penjualan/contoh-penjualan-17okt.csv` dan "resep laporan".
  - buku-piutang DENGAN menyebut "Zona: WIB" dan "Termin default" (istilah setelan).
  - kalender-pajak DENGAN dan rekap-penjualan-csv DENGAN bersih dari kata proses. Kata "skill"/"script" yang muncul saat pra-cek tidak muncul lagi.
- **Tabel Markdown mentah:** tidak ada di kedelapan jawaban. rekap-penjualan-csv DENGAN memakai judul `##`/`###` dan miring `_..._`; terkirim sebagai 1 pesan tanpa keluhan format di log.
- **Panjang:** semua jawaban 1 bagian (`chunkCount=1`; pesan 2082, 2086, 2089, 2092, 2094/2096, 2099/2102, 2105, 2108). Terpanjang: rekap-penjualan-csv DENGAN (±1.800 karakter); kalender-pajak TANPA ±1.300 karakter per giliran.
- **Terpotong:** tidak ada.
- **Kontaminasi antarsisi / sisa uji lama:**
  - Workspace bot bersama masih berisi berkas uji sebelumnya (`laporan/RESEP-*.md`, `laporan/masuk/penjualan/contoh-penjualan-17okt.csv`). Sisi TANPA laporan-harian-usaha (2072) membaca contoh itu sebagai "penjualan hari ini". Untuk uji berikutnya, bersihkan `laporan/` sebelum sisi TANPA.
  - Sisi TANPA kalender-pajak (2076) mencoba membaca `~/.openclaw/skills/laporan-otomatis-terjadwal/...`; log mencatat `Path escapes sandbox root` sehingga gagal. Jawaban tidak terpengaruh, tetapi berarti topik `skills: []` masih bisa "melihat" jalur skill dari riwayat.
  - Sisi TANPA buku-piutang (2074) benar-benar menulis `laporan/masuk/piutang/piutang-toko-sembako-berkah-sep2026.csv`. Klaim "sudah saya catat" terbukti.

## Rincian per skill

### laporan-harian-usaha 1.1.4 — TANPA 3,5 → DENGAN 8,0 (+4,5) LULUS

**Pengiriman:** topik 2073, pesan 2086, 1 bagian, utuh (30 detik). Sisi TANPA topik 2072, pesan 2082.

**Angka kunci (dihitung ulang dari isi skrip seed):**
- Kemarin 16 Okt, 3 nota: 2×18.000 + 22.000 = 58.000; 3×20.000 + 15.000 = 75.000; 16.000 + 2×15.000 = 46.000. Total **Rp179.000**.
- Hari ini 17 Okt, 4 nota: 36.000; 22.000 + 16.000 = 38.000; 30.000 + 20.000 = 50.000; 3×18.000 = 54.000 − 10% = 48.600. Total **Rp172.600**, rata-rata Rp43.150.
- Perubahan (172.600 − 179.000) ÷ 179.000 = −3,575% → **turun 3,6%**.
- Tunai 36.000 + 48.600 = Rp84.600; QRIS 38.000 + 50.000 = Rp88.000.
- Terlaris Kopi Susu Gula Aren 5 gelas, 36.000 + 48.600 = Rp84.600.
- CRM: prospek baru 1 (Bu Lestari, follow-up besok); terlambat 1 (Pak Hendra, follow-up 13 Okt, Rp2.500.000); deal 1 (Pak Agus Rp1.800.000). Kasir hari ini dibuka 07:30 dan belum ditutup.

Semua angka DENGAN benar. Sisi TANPA tidak menemukan data kasir/CRM dan memakai berkas contoh (omzet Rp715.000), sehingga **angka kunci salah** (maks 5).

Kutipan DENGAN:
> - Omzet bersih: Rp 172.600
> - vs kemarin (Jum 16/10): Rp 179.000 → **turun 3,6%**
> - Follow-up: terlambat 1, hari ini 0, besok 1 … Deal periode ini: 1 senilai Rp 1.800.000
> 1. Kasir belum ditutup (dibuka 07:30) — tutup kasir biar uang laci dicocokkan.

**Alasan skor DENGAN 8,0:**
- (+) Semua angka benar, dari data pengguna sendiri, dan menjawab "naik atau turun" langsung di baris kedua.
- (+) Nama dan nomor prospek tidak ditampilkan di grup; pengguna diarahkan mengetik perintah bila perlu.
- (+) Bagian "Perlu perhatian" berguna (kasir belum ditutup, follow-up terlambat), dan kesimpulan mengingatkan bahwa data baru setengah hari.
- (−) Baris "Konversi prospek baru: 0,0%" di samping "Deal 1" masih terbaca kontradiktif (cacat lama, sudah dicatat saat pra-cek).
- (−) "vs Sabtu lalu: Rp 0 → naik dari Rp 0" adalah baris tanpa makna; lebih baik dihilangkan bila belum ada data.
- (−) Nama alat lain dan istilah "CRM" bocor (lihat catatan lintas skill).

**Alasan skor TANPA 3,5:** Jujur bahwa berkasnya hanya contoh dan tidak ada data kemarin atau calon pembeli, tetapi tetap menampilkan omzet Rp715.000 sebagai "penjualan 17 Okt". Tidak membaca kasir dan CRM yang sebenarnya ada, sehingga tidak ada satu pun angka kunci yang benar. Jalur berkas disebut.

### buku-piutang 1.0.5 — TANPA 7,5 → DENGAN 4,0 (−3,5) BELUM

**Pengiriman:** topik 2075, pesan 2092, 1 bagian (42 detik). Sisi TANPA topik 2074, pesan 2089 (±4 menit).

**Angka kunci (dihitung ulang):** Bu Tini 1/9 + 14 hari = jatuh tempo 15/9, per 17/10 lewat **32 hari**, Rp1.250.000. Kafe Senja 5/9 + 7 hari = 12/9, sisa 2.400.000 − 1.000.000 = **Rp1.400.000**, lewat **35 hari**. Pak Joko 25/9 + 30 hari = **25/10**, Rp850.000, belum jatuh tempo. Total lewat tempo **Rp2.650.000**.

Kutipan DENGAN:
> Siap, saya catet. Sebelum mulai saya perlu bikin buku piutangnya dulu untuk Toko Sembako Berkah (baru pertama kali pakai di grup ini).
> … Termin default: 30 hari (asumsi …) - Zona: WIB
> Kalau oke, balas "ya" dan saya langsung: 1. Catat bon …

**Alasan skor DENGAN 4,0:**
- (−) Tidak ada hasil sama sekali di balasan pertama: belum ada daftar tunggakan, belum ada angka, belum ada draf tagih. Ini melanggar "kerjakan dulu, tanya di akhir". Pengguna harus membalas "ya" dulu hanya untuk membuat buku kosong.
- (−) Istilah setelan ("Termin default", "Zona: WIB", "Pengirim draf") asing bagi pembeli.
- (+) Rencana langkah benar dan menegaskan draf tagih dikirim sendiri oleh Sari, bukan oleh bot.
- Catatan penyebab: SKILL.md menggolongkan `init` sebagai perubahan besar yang wajib pratinjau → "ya". Di pra-cek buku sudah ada, sehingga langkah ini tidak terlihat. Di bot asli, buku baru dibuat untuk pertama kali.

**Alasan skor TANPA 7,5:**
- (+) Ketiga bon tercatat, jatuh tempo, sisa, dan hari lewat tempo benar semua; pengelompokan "belum bayar / lewat tempo / belum jatuh tempo" jelas.
- (+) Draf tagih sopan, menyebut nota, pembayaran sebagian, dan sisa.
- (−) Total lewat tempo Rp2.650.000 tidak disebut; tidak ada tautan wa.me siap klik.
- (−) Menawarkan "Mau saya kirimkan langsung ke nomor itu?", padahal pesan ke pelanggan seharusnya dikirim manusia.

**Perbaikan paling berdampak (BELUM):**
1. Saat buku piutang belum ada, jangan berhenti di izin. Buat buku dengan nama usaha dan pengirim dari pesan (membuat buku kosong tidak menghapus apa pun), atau hitung rekap dan draf tagih dulu dari pesan, lalu minta "ya" untuk menyimpan di akhir balasan yang sama.
2. Balasan pertama wajib memuat daftar tunggakan dengan total lewat tempo dan draf tagih + tautan wa.me.
3. Sembunyikan istilah setelan (termin default, zona); tanyakan rekening hanya sebagai pertanyaan penutup.
4. Tambahkan skenario "pemakaian pertama, buku belum ada" ke pra-cek dan uji internal, agar langkah ini tertangkap sebelum gelombang.

### kalender-pajak 1.0.7 — TANPA 5,5 → DENGAN 8,0 (+2,5) LULUS

**Pengiriman:** topik 2077, pesan 2099 (giliran 1) dan 2102 (giliran 2), masing-masing 1 bagian. Sisi TANPA topik 2076, pesan 2094 dan 2096.

**Fakta kunci (dicek ulang):**
- Omzet Rp600 juta merata = Rp50 juta/bulan. Kumulatif Sep Rp450 juta, Okt Rp500 juta (belum lewat batas Rp500 juta), Nov Rp550 juta (lewat).
- Setoran pertama untuk masa November paling lambat 15 Des 2026 = **Selasa** (dicek dengan kalender).
- SPT Tahunan OP: 31 Maret 2027 (Rabu; tidak bergeser).
- Menurut PMK 81/2024, setor PPh 21/23/unifikasi paling lambat **tanggal 15** bulan berikutnya dan lapor tanggal 20. Tanggal 10 sudah tidak berlaku.

Kutipan DENGAN (giliran 2):
> **Kabar baiknya: bulan Oktober 2026 ini TIDAK ada setoran/lapor pajak yang jatuh tempo.**
> - Kumulatif baru **melewati** Rp500 juta di **November 2026** (jadi Rp550 juta).
> - Setoran pertama Anda jatuh di masa **November 2026**, paling lambat **Selasa, 15 Desember 2026** …
> ⚠️ Catatan: ini perkiraan berdasarkan asumsi omzet rata-rata merata per bulan …

**Alasan skor DENGAN 8,0:**
- (+) Kesimpulan tepat dan menenangkan untuk pertanyaan "biar ga kena denda"; asumsi merata ditulis; ada tawaran rincian per bulan dan disclaimer + Kring Pajak.
- (+) Giliran 1 menanyakan 4 hal dalam satu pesan (sesuai desain skill, 1 pertanyaan di atas batas 3, tetapi singkat dan relevan).
- (−) SPT Tahunan OP 31 Maret 2027 tidak disebut, padahal ada di kunci dan muncul saat pra-cek.
- (−) Perkiraan setoran November (0,5% × Rp50 juta = Rp250.000) tidak disebut; ini akan menambah nilai.
- (−) Giliran 1 tidak memberi hasil apa pun sebelum profil dijawab.

**Alasan skor TANPA 5,5:**
- (+) Giliran 2 memahami batas Rp500 juta untuk orang pribadi dan menyebut SPT Tahunan 31 Maret 2027.
- (−) Giliran 1 memuat fakta usang: setor PPh 21/23/26 "10 Oktober → geser Senin 12 Oktober", padahal kini tanggal 15.
- (−) Giliran 2 tetap bilang "bayar … paling lambat 15 Oktober" padahal hari ini sudah 17 Oktober, lalu berhenti dengan pertanyaan omzet Januari–September walau omzet setahun sudah diberikan. Tidak ada kesimpulan.
- (−) Gaya "lo/gue" berganti-ganti.

### rekap-penjualan-csv 1.2.5 — TANPA 8,0 → DENGAN 6,5 (−1,5) BELUM

**Pengiriman:** topik 2079, pesan 2108, 1 bagian (43 detik). Sisi TANPA topik 2078, pesan 2105.

**Angka kunci (dihitung ulang dari CSV, 72 baris):**
- Selesai 66 pesanan **Rp5.519.000**; Batal 4 Rp238.000; Pengembalian Dana 2 Rp272.000.
- Per produk (omzet, pcs, harga satuan): Kaos Oversize Abu Rp1.659.000, 21 pcs, Rp79.000 (30,1%); Kaos Polos Putih Rp1.062.000, 18 pcs, Rp59.000; Kaos Polos Hitam Rp1.003.000, 17 pcs, Rp59.000; Topi Baseball Rp990.000, 22 pcs, Rp45.000; **Tote Bag Natural Rp805.000, 23 pcs, Rp35.000**.
- Omzet tertinggi 5 Sep Rp549.000; terendah 18 Sep Rp35.000; 29 hari berjualan; rata-rata Rp183.967 (30 hari) / Rp190.310 (29 hari).
- Pesanan terbanyak: 1 Sep dan 5 Sep, masing-masing 5 (seri).
- Per hari dalam seminggu: Senin omzet tertinggi Rp1.155.000; Selasa transaksi terbanyak 12.
- Tanggal batal/refund: 2, 10, 11, 25, 26, 28 Sep.

Angka utama DENGAN benar semua. Namun Insight 2 menulis "Topi Baseball qty terjual paling banyak (22 pcs) … harganya paling murah di antara 5 produk ini". Keduanya **salah**: Tote Bag 23 pcs dan Rp35.000 (lebih murah dari Topi Rp45.000). Insight 1 juga menyebut "margin per unit" padahal yang dibandingkan adalah harga jual, bukan margin. Sisi TANPA benar semua, termasuk klaim Senin/Selasa dan Tote Bag terlaris per jumlah.

Kutipan DENGAN:
> **Total omzet:** Rp 5.519.000 _(dari 66 pesanan selesai)_
> 2. Topi Baseball qty terjual paling banyak (22 pcs) tapi omzetnya di posisi ke-4 — berarti harganya paling murah di antara 5 produk ini, cek lagi apakah harganya kurang kompetitif …

**Alasan skor DENGAN 6,5:**
- (+) Omzet, status pesanan beserta nilainya, peringkat 5 produk dengan persentase, hari tertinggi/terendah, dan seri 1 & 5 Sep: benar dan lengkap.
- (−) Satu fakta salah yang bertentangan dengan daftar di atasnya sendiri, disertai saran bisnis yang keliru ("cek apakah harganya kurang kompetitif"). Pemilik toko bisa salah mengambil keputusan harga.
- (−) "Margin per unit" salah istilah; judul `##` dan dua jenis rata-rata menambah panjang.
- (−) Tidak menjawab produk terlaris per jumlah (Tote Bag 23 pcs), padahal sisi TANPA menyebutnya.

**Alasan skor TANPA 8,0:**
- (+) Semua angka benar, ringkas, menjawab tiga pertanyaan langsung; membedakan terlaris per omzet (Kaos Oversize Abu) dan per jumlah (Tote Bag); menambah pola hari Senin/Selasa yang benar.
- (−) Nilai batal/refund tidak disebut; "Senin & Selasa cenderung rame" ditarik dari satu bulan tanpa catatan.

**Perbaikan paling berdampak (BELUM):**
1. Insight wajib diambil dari angka yang sudah dihitung (peringkat jumlah dan harga satuan dari hasil hitungan), bukan dikarang. Bila tidak ada angka pendukung, insight dihilangkan.
2. Tampilkan terlaris per omzet **dan** per jumlah dalam satu baris masing-masing; ini yang biasanya ditanyakan "produk paling laku".
3. Jangan pakai istilah "margin" bila data tidak memuat modal/HPP; pakai "harga jual".
4. Ringkas untuk chat: satu rata-rata saja, tanpa judul `##`.
5. Tambahkan kunci di uji internal yang memeriksa setiap kalimat insight terhadap angka (mis. "produk dengan pcs terbanyak = Tote Bag").

## Pemeriksa kedua (2026-10-17)

Pemeriksa kedua independen (bukan pembuat skill, bukan penilai 1). Bahan yang dibaca: kedelapan transkrip `scratchpad/openclaw-real/hasil/a5/2072–2079-*.md`, `pilot/kandidat-a-cepat.json`, `pilot/seed-laporan-harian.sh`, `pilot/data-a-cepat/rekap-penjualan-csv/penjualan-september.csv`, dan SKILL.md keempat skill. Angka dihitung ulang sendiri dengan Decimal dan kalender Python.

**Angka kunci yang dicek ulang (semua cocok dengan penilai 1):**
- Kasir: kemarin Rp179.000; hari ini Rp172.600 (rata-rata Rp43.150), −3,6%; tunai Rp84.600, QRIS Rp88.000.
- Piutang per 17/10: Bu Tini jatuh tempo 15/9, lewat 32 hari; Kafe Senja jatuh tempo 12/9, sisa Rp1.400.000, lewat 35 hari; Pak Joko jatuh tempo 25/10 (8 hari lagi); total lewat tempo Rp2.650.000.
- Pajak: 15 Des 2026 = Selasa; 31 Mar 2027 = Rabu; PPh masa November 0,5% × Rp50.000.000 = Rp250.000 (kumulatif Oktober tepat Rp500 juta, jadi seluruh omzet November di atas batas).
- CSV: 72 baris; Selesai 66 / Rp5.519.000, Batal 4 / Rp238.000, Pengembalian Dana 2 / Rp272.000. Per produk (pcs, harga satuan): Oversize Abu 21 @79.000, Polos Putih 18 @59.000, Polos Hitam 17 @59.000, Topi 22 @45.000, **Tote Bag 23 @35.000**. Ada 29 hari berjualan; tertinggi 5/9 Rp549.000; terendah 18/9 Rp35.000; pesanan terbanyak 1/9 dan 5/9 (5 pesanan). Senin Rp1.155.000 dan Selasa 12 pesanan, keduanya benar. Catatan kecil: September 2026 punya 5 hari Selasa dan 4 hari Senin, jadi "Selasa paling banyak transaksi" sebagian karena jumlah harinya.

### Per skill

| Skill | Penilai 1 | Pemeriksa kedua | Skor koreksi | Verdik akhir |
|---|---|---|---|---|
| laporan-harian-usaha 1.1.4 | 3,5 → 8,0, LULUS | **Setuju** | tetap | **LULUS** |
| buku-piutang 1.0.5 | 7,5 → 4,0, BELUM | **Tidak setuju** dengan status final | skor DENGAN 4,0 **dibatalkan** | **TIDAK SAH — perlu kirim ulang dengan lanjutan "ya"** |
| kalender-pajak 1.0.7 | 5,5 → 8,0, LULUS | **Setuju** | tetap | **LULUS** |
| rekap-penjualan-csv 1.2.5 | 8,0 → 6,5, BELUM | **Setuju** | tetap | **BELUM** |

**(1) buku-piutang: TIDAK SAH.** Balasan DENGAN (2075) mengikuti SKILL.md persis.
- Aturan wajib 5 menggolongkan `init` sebagai perubahan besar: jalankan pratinjau dulu, lalu `--ya` hanya setelah pengguna setuju.
- Langkah A.1–A.2 meminta `info`, lalu `init` dengan pratinjau dan persetujuan, bila database belum ada.
- Aturan 2 melarang menghitung sisa atau umur piutang tanpa script, jadi rekap memang tidak bisa diberikan sebelum buku dibuat.

Bot di sini menjalankan skill dengan benar. Masalahnya ada pada desain uji: pra-cek memakai buku yang sudah ada, dan kandidat tidak memuat `lanjutan`, padahal uji `buku-stok` dan `absensi-lokal` di berkas yang sama memakai `"lanjutan": "ya"`. Skor 4,0 mengukur giliran yang belum selesai, bukan hasil skill, jadi tidak dipakai untuk verdik.

Kritik penilai 1 tetap berlaku sebagai **usulan desain**, bukan cacat eksekusi: buku kosong untuk pemakaian pertama cukup dibuat dengan nama usaha dan pengirim dari pesan, tanpa giliran tambahan. Bila pemilik ingin satu giliran saja, Aturan 5 dan Langkah A perlu diubah di versi berikutnya. Sisi TANPA 7,5: setuju. Nilai minusnya yang terberat adalah tawaran "Mau saya kirimkan langsung ke nomor itu?", karena bertentangan dengan aturan bahwa manusia yang mengirim.

**(2) laporan-harian-usaha: perbandingan tetap sah.** Sisa berkas `laporan/masuk/penjualan/contoh-penjualan-17okt.csv` hanya memengaruhi sisi TANPA. Tanpa berkas itu, TANPA paling-paling menjawab jujur "belum ada data kasir/calon pembeli" (perkiraan 3–4,5), karena data kasir dan CRM tersimpan di database alat yang hanya dikenali lewat skill. Berkas sisa tidak menguntungkan sisi DENGAN, yang membaca kasir dan CRM hasil seed.
- Selisih terburuk: 8,0 − 4,5 = 3,5, masih ≥ 1,5.
- Semua angka DENGAN cocok dengan seed.
- Baris "vs Sabtu lalu: Rp 0 → naik dari Rp 0" memang aturan SKILL.md (Perubahan %, pembanding Rp 0). Itu cacat desain, bukan salah eksekusi, dan pengurangan nilainya wajar.

Hanya saja, sebelum uji berikutnya `laporan/` perlu dibersihkan dan sisi TANPA dijalankan di home bersih, sesuai `tester-umum.md` ("buat ulang bersih per skenario").

**(3) rekap-penjualan-csv: klaim penilai 1 benar.** Dari CSV, jumlah terjual terbanyak adalah Tote Bag Natural (23 pcs, bukan Topi 22 pcs) dan yang termurah juga Tote Bag (Rp35.000, bukan Topi Rp45.000). Insight 2 bertentangan dengan daftar peringkat di atasnya dan memberi saran harga yang keliru. Ini juga melanggar SKILL.md ("Insight harus berdasarkan data"). Istilah "margin per unit" juga salah, karena data tidak memuat modal.

Angka utama (omzet, terlaris per omzet, hari ramai) benar, jadi batas "salah angka kunci = maks 5" tidak dipakai. Skor 6,5 wajar. BELUM.

**(4) kalender-pajak: SPT Tahunan tidak disebut, bobotnya ringan.** Pertanyaannya "bulan Oktober ini", dan tenggat 31 Mar 2027 masih ±5 bulan lagi, jadi tidak ada risiko denda dalam jendela yang ditanyakan. Kesimpulan inti (Oktober tidak ada setoran; setoran pertama paling lambat Selasa 15 Des 2026) benar dan tidak menyesatkan.

Untuk freelancer orang pribadi dengan tarif 0,5%, SPT Tahunan tetap wajib dan tahun 2026 adalah tahun pertama ia melewati Rp500 juta, jadi pengingat itu bernilai. Pengurangan sekitar −0,5 sudah tercermin dalam 8,0 penilai 1. Bukan salah fakta kunci. Usulan untuk versi berikutnya: satu baris "Jangan lupa: SPT Tahunan 2026 paling lambat Rabu, 31 Mar 2027" dan perkiraan setoran November Rp250.000.

Untuk sisi TANPA 5,5: tanggal 10 Oktober untuk PPh 21/23 memang usang, tetapi tidak berlaku untuk profil ini (tanpa karyawan), jadi batas maks 5 tidak dipakai. Setuju.

### Uji yang perlu dikirim ulang

1. **buku-piutang 1.0.5, sisi DENGAN saja**, di topik baru dengan bot pertama. Sisi TANPA (2074, 7,5) tetap dipakai dan **jangan dikirimi "ya"**, karena giliran terakhirnya bertanya "Mau saya kirimkan langsung ke nomor itu?" dan "ya" bisa dibaca sebagai izin mengirim WA ke pelanggan (di luar grup uji).
   - Prasyarat: `~/KomunitechData/piutang/piutang.db` di HOME bot **belum ada**, agar jalur pemakaian pertama yang diuji. Hapus juga `laporan/masuk/piutang/piutang-toko-sembako-berkah-sep2026.csv` sisa sisi TANPA dari workspace bersama. Restart gateway bila `channels.*` diubah.
   - Pesan 1 (persis): `@KTclaude1_bot tolong catet bon ya: Warung Bu Tini ambil beras 1.250.000 tgl 1/9/2026 nota B-0901 tempo 2 minggu. Kafe Senja ambil gula & minyak 2,4jt tgl 5/9/2026 nota B-0905 tempo seminggu, tgl 15/9 kafe senja transfer 1jt. Pak Joko 850rb tgl 25/9/2026 nota B-0925 tempo 30 hari. siapa aja yg belum bayar & yg udah lewat jatuh tempo? bikinin pesan tagih buat kafe senja ya, wa nya 0812-3456-7890. toko saya Toko Sembako Berkah, nama saya Sari`
   - Lanjutan (persis, hanya bila balasan 1 berupa pratinjau pembuatan buku): `@KTclaude1_bot ya`
   - Kunci tidak berubah: Kafe Senja sisa Rp1.400.000, lewat 35 hari; Bu Tini Rp1.250.000, lewat 32 hari; total lewat tempo Rp2.650.000; Pak Joko Rp850.000, jatuh tempo 25 Okt; draf tagih + tautan wa.me, dikirim Sari sendiri. Nilai dua giliran sebagai satu jawaban (seperti kalender-pajak).
   - Tambahkan `"lanjutan": "ya"` ke entri buku-piutang di `pilot/kandidat-a-cepat.json` dan skenario "buku belum ada" ke pra-cek.
2. laporan-harian-usaha, kalender-pajak, rekap-penjualan-csv: **tidak perlu kirim ulang.**

Verdik akhir gelombang A5: LULUS 2 (laporan-harian-usaha, kalender-pajak), BELUM 1 (rekap-penjualan-csv), TIDAK SAH 1 (buku-piutang, menunggu kirim ulang).
