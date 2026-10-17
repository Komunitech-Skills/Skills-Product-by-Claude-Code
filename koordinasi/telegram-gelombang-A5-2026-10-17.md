# Gelombang Telegram A5 — 2026-10-17 (bot pertama)

Uji ini berlangsung di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A) di OpenClaw 2026.10.2, pada 17 Okt 2026 pukul 06:12–06:27 UTC, di topik baru 2072–2079. Pesan uji sama persis di sisi TANPA (topik dengan `skills: []`) dan DENGAN skill. Pesan dan kunci jawaban diambil dari `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json`, dan pra-ceknya ada di `koordinasi/pracek-telegram-akun-a-2026-10-17.md`. Penilai 1 (independen, bukan pembuat skill) memakai skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Semua angka kunci dihitung ulang dengan Decimal: data kasir+CRM dari isi `pilot/seed-laporan-harian.sh` (kemarin 2026-10-16, hari ini 2026-10-17), CSV dari `pilot/data-a-cepat/rekap-penjualan-csv/penjualan-september.csv`, tanggal dan nama hari dengan kalender Python, dan aturan tenggat dari `skills/kalender-pajak/SKILL.md` (PMK 81/2024). Bukti kirim dicocokkan ke log gateway `gw-20261017-0612.log`. Jawaban ganda yang identik di transkrip adalah salinan log dan hanya dihitung sekali.

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka atau fakta kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| laporan-harian-usaha | 1.1.4 | 2072 / 2073 | 3,5 | 8,0 | +4,5 | **LULUS** (batas bawah DENGAN) | Dengan skill, Anda langsung mendapat rekap dari kasir dan buku calon pembeli Anda sendiri: omzet hari ini Rp172.600, turun 3,6% dari kemarin, ada 1 follow-up yang terlambat, dan pengingat bahwa kasir belum ditutup. Tanpa skill, bot memakai berkas contoh yang tertinggal di folder, jadi angkanya bukan angka toko Anda, dan bot tidak bisa membandingkan dengan kemarin. |
| buku-piutang | 1.0.5 | 2074 / 2075 | 7,5 | 4,0 | −3,5 | **BELUM** | Dengan skill, balasan pertama hanya meminta izin membuat buku piutang ("balas ya"). Belum ada daftar siapa yang menunggak dan belum ada draf tagihan. Tanpa skill, bot langsung mencatat bon, menghitung sisa dan keterlambatan dengan benar, lalu memberi draf pesan tagih. |
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
