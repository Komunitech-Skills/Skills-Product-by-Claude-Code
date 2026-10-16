# Gelombang Telegram 22 — 2026-10-16 (bot kedua)

Keputusan otomatis **90/92/93** (2026-10-16). Bot uji kedua `@KTclaude2bot` (OpenClaw 2026.10.2, model router Komunitech), grup uji internal Komunitech, topik baru 1663–1672. Pesan uji identik di sisi TANPA (topik `skills: []`) dan DENGAN skill; dikirim berurutan oleh bot penguji (rantai otomatis dua jalur, keputusan 93). Penilaian: satu penilai independen per skill + pemeriksa kedua yang berusaha membantah (angka dihitung ulang, kutipan dicocokkan ke id pesan); koreksi pemeriksa sudah diterapkan di tabel.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| copy-landing-page (1.0.7) | 3 | 8 | +5 | **LOLOS** | Dengan skill, bot langsung menulis teks landing page lengkap di chat: versi panjang, versi link-in-bio, 3 headline, judul dan deskripsi Google yang hurufnya sudah dihitung, serta tautan WA yang bisa diklik. Bot juga mengingatkan izin PIRT/BPOM dan wajib halal, dan semua yang belum diberikan (varian rasa, ukuran, masa simpan, garansi) ditulis [isian]. Tanpa skill, bot hanya mengirim ringkasan isi yang memuat klaim karangan ("fresh", "dibuat dari hati"), dan file HTML-nya gagal terkirim, jadi tidak ada teks yang bisa dipakai. |
| analisis-rasio-keuangan-usaha (1.0.5) | 6,5 | 8 | +1,5 | **LOLOS** | Hanya versi dengan skill yang menghitung umur stok 35,8 hari (satu-satunya rasio berstatus waspada) beserta langkah perbaikannya, menyebut kas + piutang Rp18 jt < utang jangka pendek Rp25 jt sebagai risiko likuiditas SEDANG (versi tanpa skill hanya menulis rasio cepat 18/25 = 0,7x "agak tipis, tapi wajar"), dan menjawab "aman" secara bersyarat karena bank juga menilai SLIK OJK, agunan, dan legalitas. |
| tagih-piutang (1.0.8) | 5 | 8,5 | +3,5 | **LOLOS** | Hanya DENGAN yang menghitung keterlambatan (42 hari) dan menaikkan nada jadi surat teguran resmi yang tetap sopan, dengan batas bayar 24 Oktober, versi WA singkat, dan langkah berikutnya bila tetap tidak dibayar; TANPA hanya membuat pengingat ketiga yang sama lunaknya, tanpa batas waktu. |
| tender-checklist (1.0.8) | 5 | 7,5 | +2,5 | **BELUM** (DENGAN < 8) | Dengan skill, bot langsung memberi vonis "IKUT DENGAN SYARAT" dan memakai batas usaha kecil yang berlaku (Rp15 miliar; tanpa skill masih batas lama Rp2,5 miliar). Bot juga menulis terbilang total Rp44.142.480 dan menyebut persis 23,86% HPS, di bawah ambang 80% yang memicu klarifikasi kewajaran harga, tetapi daftar dokumen yang ditanyakan justru tidak muncul. |
| follow-up-prospek (1.0.4) | 6,5 | 8,5 | +2 | **LOLOS** | Dengan skill, bot sadar demo sudah 25 hari lewat, lalu menyusun 4 pesan WA bertanggal pasti (Senin 19 Okt s.d. Senin 2 Nov), termasuk ajakan telepon 10 menit bersama Bapak & Ibu. Tanpa skill, bot hanya membuat satu pesan yang masih menulis "terima kasih … kemarin", seolah demo baru sehari lalu. |

Pembanding uji internal (skor promosi / `examples/`):
- copy-landing-page: 6,0 → 8,0 (1.0.4).
- analisis-rasio-keuangan-usaha: 7,0 → 9,0 (1.0.5).
- tagih-piutang: 6,7 → 8,5 (1.0.7).
- tender-checklist: 7,25 → 9,0 (1.0.7).
- follow-up-prospek: 6,25 → 8,0 (1.0.4).

Beda terhadap uji internal:
- **copy-landing-page:** Di bot asli, skor TANPA lebih rendah (3,0 vs 6,0) karena file HTML-nya ditolak lampiran Telegram, jadi tidak ada isi yang sampai ke pengguna. DENGAN sama-sama 8,0, tetapi cacat di versi 1.0.4 (isi hanya di file, garansi 1×24 jam dikarang) sudah hilang: isi utuh di chat dan tidak ada karangan. Gantinya ada cacat baru: isian satuan harga yang sebenarnya sudah diberikan pemilik.
- **analisis-rasio-keuangan-usaha:** Uji internal memakai kasus yang lebih menjebak (perusahaan dagang Rp9,6 M, kas Rp420 jt vs utang bank jatuh tempo Rp900 jt), dan di kasus itu jawaban tanpa skill melewatkan risikonya. Di bot, kasusnya toko sembako sederhana yang rasionya sudah dihitung benar oleh jawaban tanpa skill. Selisih menyempit dari 2,0 ke 1,5, dan sisi DENGAN turun dari 9,0 ke 8,0 karena kata proses bocor dan label "Asumsi:" tidak dipakai.
- **tagih-piutang:** Skor DENGAN di bot asli sama dengan uji internal (8,5), tetapi selisihnya lebih besar (+3,5 vs +1,8). Penyebabnya, TANPA hanya membuat pengingat lunak dan salah menyalin nama pemilik rekening; kali ini juga tidak ada kata proses yang bocor. Hari terlambat dihitung per tanggal WIB saat bot membalas (17 Okt, 42 hari), bukan per 16 Okt (41 hari) seperti di brief.
- **tender-checklist:** Uji internal (1.0.7, kasus meubel HPS Rp248,5 jt) memberi sisi DENGAN 9,0 dengan semua bagian lengkap, termasuk jaminan pelaksanaan dan PPh 22. Di bot (1.0.8) hitungan tetap tepat, tetapi checklist dokumen, dasar aturan, dan pengingat PPh 22 hilang sehingga skornya turun ke 7,5; sisi TANPA jatuh ke 5 karena memakai batas usaha kecil lama Rp2,5 miliar.
- **follow-up-prospek:** Uji internal 1.0.4 memakai skenario penawaran jasa foto, dengan pembeda utama nama hari yang salah di sisi tanpa skill. Di bot Telegram (skenario demo kasir yang tanggalnya sudah lewat 25 hari), sisi tanpa skill tidak salah nama hari tetapi menulis "kemarin", sedangkan sisi dengan skill menjadwal ulang dari hari ini dengan semua tanggal benar (6,5 → 8,5, sedikit lebih tinggi dari uji internal).

Catatan jujur (untuk pembeli):
- **copy-landing-page:** Harga ditulis "Rp25.000 [isian: per bungkus/ukuran]" walaupun pemilik sudah menyebut "per bungkus", jadi isian itu harus dihapus sendiri. Hasilnya berupa teks untuk ditempel ke pembuat halaman web atau link-in-bio, bukan file halaman web yang langsung jadi.
- **analisis-rasio-keuangan-usaha:** Kemampuan bayar KUR hanya dibandingkan dengan laba bersih; cicilan pinjaman bank yang sudah berjalan belum ikut dihitung kecuali Anda menyebutkannya. Label risiko "SEDANG" di samping rasio berwarna hijau bisa membingungkan, dan hasilnya tetap bacaan angka, bukan keputusan bank.
- **tagih-piutang:** Untuk pelanggan lama, langkah sesudah tenggat langsung menyarankan advokat atau gugatan sederhana tanpa langkah lunak (telepon atau bertemu), dan tenggatnya jatuh hari Sabtu. Jawaban juga menganggap layanan katering masih berjalan padahal pengguna tidak menyebutnya.
- **tender-checklist:** Di bot Telegram, daftar dokumen penawaran bisa tidak muncul walau ditanyakan, sehingga pengguna perlu memintanya lagi. Balasan juga belum menyertakan dasar aturan, penafian, dan pengingat bahwa bendahara memotong PPN/PPh 22 saat membayar.
- **follow-up-prospek:** Hasilnya berupa urutan 4 pesan lengkap dengan aturan main, lebih panjang dari satu pesan WA yang diminta. Pesan ke-2 memuat contoh fitur (laporan penjualan di HP) yang perlu Anda pastikan memang ada di produk sebelum dikirim, dan jadwal disusun dengan anggapan belum pernah ada follow-up sebelumnya.

Salah angka/fakta yang ditemukan:
- copy-landing-page: TANPA: daftar 'Kenapa harus beli' memuat klaim 'fresh' dan 'dibuat dari hati'. Pemilik tidak pernah menyebut keduanya, jadi ini klaim karangan dan skor dibatasi maks 5. DENGAN: tidak ada salah angka/fakta. Yang sudah dicek ulang: nomor WA 0812-3456-7890 → wa.me/6281234567890 (URL di balik tautan sudah di-encode benar), panjang meta title 47/60 dan deskripsi 135/155 karakter, serta tanggal wajib halal UMK makanan-minuman 18 Okt 2026 (cocok dengan rujukan BPJPH). Kalimat asumsi 'satuan harga tidak disebut' adalah salah baca pesan pemilik; dicatat sebagai cacat, bukan salah fakta di isi halaman.
- analisis-rasio-keuangan-usaha: tidak ada
- tagih-piutang: Sisi TANPA: rekening ditulis "a.n. Dapur Sehati", padahal data pengguna "a.n. Dapur Sehati Fiktif" (nama pemilik rekening berubah di instruksi transfer)
- tender-checklist: TANPA: menyebut batas paket untuk Usaha Kecil/Koperasi "s.d. Rp2,5 M". Itu angka lama Perpres 16/2018 sebelum diubah; batas yang berlaku sejak Perpres 12/2021 (dipertahankan Perpres 46/2025) adalah Rp15 miliar. Kesimpulan "layak" tetap benar, tetapi angka aturannya salah. Sisi DENGAN tidak punya salah angka/fakta. Hasil hitung ulang Python: 150×52.500 = 7.875.000; 24×1.250.000 = 30.000.000; 500×3.750 = 1.875.000; 1,5×12.000 = 18.000; DPP 39.768.000; PPN 12%×11/12×DPP = 4.374.480 (bulat ke bawah); total 44.142.480 = 23,86% HPS (ambang 80% = 148.000.000); terbilang benar. Batas unggah 14 Okt 15.00 sudah lewat; balasan dikirim 17 Okt sekitar 01.00 WIB (Sabtu), jadi kedua sisi benar menyebutnya sudah lewat.
- follow-up-prospek: tidak ada

Pemeriksa kedua:
- **copy-landing-page:** koreksi — Kutipan dan id cocok: 1788 (topik 1663) dan 1791–1793 (topik 1664) dari KTclaude2bot, dan kedua kutipan adalah awalan yang sama persis dengan teks aslinya. Angka sudah dihitung ulang dengan Python: judul 47 dan deskripsi 135 karakter, href text_link sama dengan quote() menjadi wa.me/6281234567890, 18 Okt 2026 jatuh 2 hari setelah tanggal uji, dan isian "Rp25.000 [isian" muncul 4 kali. Skor 3→8 dan
- **analisis-rasio-keuangan-usaha:** koreksi — Kutipan dan id benar: 1795 (topik 1665) dan 1801 (topik 1666) dari KTclaude2bot; 1799 hanya "Working". Hitung ulang Python cocok: 58/25 = 2,32; 18/25 = 0,72; 12/25 = 0,48; margin kotor 15%; margin bersih 5%; ROA 24%; ROE 40%; DER 0,667; DAR 40%; umur stok 35,78 hari; piutang 4,56 hari; pemasok 17,89 hari; cicilan 25%. Ada 11 rasio yang dinilai (lama bayar pemasok hanya info). Skor 6,5 → 8,0 dan LO
- **tagih-piutang:** setuju — Pesan 1803 (topik 1667) dan 1810 (topik 1668) berasal dari KTclaude2bot. Pesan 1805 hanya "Working". Semua potongan kutipan cocok persis dan tidak ada konteks yang terbalik. Balasan 1810 terkirim 00.57 WIB 17 Okt. Hitungan Python: 5 Sep→17 Okt = 42 hari, sedangkan per 16 Okt = 41 hari (sesuai catatan khusus). Tanggal 24 Okt jatuh hari Sabtu dan 25 Okt hari Minggu, cocok dengan tenggat 7 hari. Nomi
- **tender-checklist:** setuju — Kedua kutipan ada utuh: msg 1813 di topik 1669 dan msg 1819 di topik 1670, keduanya dari KTclaude2bot, tanpa konteks yang terpotong. Hitung ulang dengan Python cocok: DPP 39.768.000, PPN 4.374.480, total 44.142.480 (23,86% HPS, ambang 80% = 148 jt), terbilangnya benar. Balasan terkirim Sabtu 17 Okt pukul 00.59/01.01 WIB. Batas Rp2,5 M di TANPA memang salah fakta (aturan yang berlaku Rp15 M, Pasal 
- **follow-up-prospek:** setuju — Kedua kutipan ada kata per kata: msg 1823 (topik 1671) dan 1838 (topik 1672), keduanya dari KTclaude2bot. Msg 1826 hanya "Working". Pesan uji terkirim 01.01 WIB, 17 Okt 2026. Hitung ulang dengan Python: 22 Sep ke Sabtu 17 Okt = 25 hari. Aturan SKILL.md (geser akhir pekan + jarak minimal) menghasilkan Senin 19 Okt, Rabu 21 Okt (H+3 20 Okt dijarakkan ≥2 hari), Senin 26 Okt, Senin 2 Nov, sama dengan 

## Kutipan balasan (dipendekkan, `…` = dipotong)

### copy-landing-page — TANPA (topik 1663, pesan 1788)

> Landing page-nya udah jadi, Mak! File HTML siap pakai, tinggal hosting atau buka langsung di browser.
> 
> Isinya:
> 
> • Hero section dengan nama "Keripik Setan Mak Iyem" + harga Rp25.000/bungkus + tombol order WA
> • Kenapa harus beli (pedas beneran, dibuat dari hati, harga bersahabat, fresh)
> • Cara pesan (4 langkah: chat WA → cek harga+ongkir → bayar → dikirim)
> • Info pengiriman dibagi 2: Jabodetabek pakai ojol/kurir sendiri, luar kota pakai ekspedisi
> • Pembayaran: transfer/QRIS (detail dikirim via WA biar aman)
> • Testimoni dibuat jujur apa adanya — "belum ada testimoni tertulis, jadilah yang pertam…

Alasan skor TANPA: Bot bilang landing page sudah jadi sebagai file HTML, tetapi file keripik-setan-mak-iyem.html ditolak sistem lampiran. Di chat hanya ada daftar isi halaman, dan pemilik tidak menerima satu kalimat pun yang bisa ditempel atau dipublikasikan. Ringkasan itu juga memuat klaim karangan ("fresh", "dibuat dari hati"), sehingga skor dibatasi maks 5. Ada sisi baiknya: testimoni ditangani jujur ("belum ada, jadilah yang pertama"), pengiriman dan cara bayar sesuai pesan, dan nadanya santai. Tetapi tidak ada pengingat izin PIRT/BPOM atau halal, tidak ada teks utuh, tidak ada tautan WA yang bisa dicek, dan pesan error berisi nama file ikut terkirim ke pengguna. Pada praktiknya pengguna tidak mendapat apa-apa.

### copy-landing-page — DENGAN (topik 1664, pesan 1791, 1792, 1793; berkas: TANPA: tidak ada berkas terkirim (keripik-setan-mak-iyem.html ditolak sistem lampiran, hanya pesan error yang muncul), DENGAN: tidak ada berkas, seluruh isi ada di chat)

> ⚠️ Pengingat izin edar: keripik itu pangan olahan, jadi PIRT/SPP-IRT atau izin BPOM wajib ada SEBELUM dijual & dipromosikan. Karena belum disebut ada izin, halaman ini tidak memuat klaim izin apa pun.
> 
> 1. Versi Lengkap (Landing Page)
> 
> Pesan Keripik Pedas Mak Iyem Lewat WhatsApp, Dikirim ke Rumahmu
> Keripik Setan Mak Iyem — Rp25.000 [isian: per bungkus/ukuran]. Kirim ke Jabodetabek dan luar kota, bayar transfer atau QRIS.
> 
> 👉 Pesan Sekarang lewat WhatsApp: https://wa.me/6281234567890?text=Halo%2C saya mau pesan Keripik Setan Mak Iyem dari halaman ini
> 
> Masalahnya
> Lagi pengen ngemil pedas tapi males keluar rumah nyari? Atau udah nemu yang enak tapi bingung cara pesan & bayarnya? Tinggal chat WA, bayar transfer/QRIS, pesanan dikirim.
> 
> Kenapa Keripik Setan Mak Iyem Cocok Buat Kamu
> 
> • Pesan tinggal chat WhatsApp, tanpa ribet.
> • Bisa dikirim ke rumah: Jabodetabek lewat ojol/kurir sendiri (kalau…

Alasan skor DENGAN: Seluruh teks halaman utuh di chat (3 pesan berurutan) dan siap tempel. Isinya: versi lengkap (headline, masalah, alasan beli, cara pesan 4 langkah, penawaran, FAQ, ajakan penutup), versi link-in-bio, 3 variasi headline, meta title/description dengan hitungan karakter yang benar, tautan wa.me ke nomor yang benar beserta pesan pembuka, ceklis kepatuhan, dan asumsi. Bot tidak mengarang bahan, level pedas, ukuran, masa simpan, garansi, testimoni, maupun izin; semuanya ditulis sebagai [isian]. Bagian testimoni diberi tanda untuk dihapus sampai ada testimoni asli. Ada peringatan izin PIRT/SPP-IRT/BPOM di atas, dan pengingat wajib halal UMK mulai 18 Okt 2026, dua hari setelah tanggal uji, jadi sangat relevan. Nadanya santai sesuai permintaan, dan tidak ada kata proses atau jalur file.

Kekurangan:
(1) Pesan pemilik sudah menyebut "per bungkus", tetapi harga tetap ditulis 4 kali sebagai "Rp25.000 [isian: per bungkus/ukuran]". Bagian asumsi bahkan menyebut satuan itu tidak disebut, bertentangan dengan meta deskripsi "Rp25.000/bungkus". Pola ini sama dengan contoh di SKILL.md, sehingga tampaknya ikut tertiru.
(2) Teks URL yang tampil masih berisi spasi mentah. Tombolnya di Telegram berfungsi, tetapi kalau teks URL itu disalin apa adanya ke pembuat halaman web, pesan pembukanya bisa terpotong.
(3) Penanda isian tidak seragam ("[isi: garansi…]" vs "[isian: …]").
(4) Tidak ada petunjuk singkat ke mana teks ini ditempel (pembuat halaman atau link-in-bio) untuk pembeli awam yang memintanya sebagai "landing page".
(5) Karena data produk sedikit, isi persuasifnya agak tipis, meski ini konsekuensi wajar dari aturan tidak mengarang.

### analisis-rasio-keuangan-usaha — TANPA (topik 1665, pesan 1795)

> • Current ratio = 58/25 = 2,3x → sehat
> • Quick ratio (tanpa stok) = 18/25 = 0,7x → agak tipis, tapi wajar untuk toko sembako …
> • Cicilan 500rb/bulan = 25% dari laba bersih bulanan → masih dalam batas aman (umumnya cicilan dianjurkan maks 30-35% dari laba bersih/arus kas)
> 
> Kesimpulan: aman untuk ambil KUR 500rb/bulan. Modal masih lebih besar dari utang (DER 0,67x), dan beban cicilan barunya cuma seperempat dari laba bersih bulanan. Dua hal yang perlu dijaga: …

Alasan skor TANPA: 6,5. Hitung ulang Python cocok untuk semua angka: aset lancar 58, utang lancar 25, rasio lancar 58/25 = 2,32 (ditulis 2,3x), rasio cepat 18/25 = 0,72 (0,7x), DER 40/60 = 0,67, margin kotor 15%, margin bersih 5%, ROA 24%, ROE 40%, laba per bulan 2 jt, cicilan 25% dari laba bulanan. Ada cek keseimbangan neraca (40 + 60 = 100) dan bahasanya runtut. Pembulatan "0,67x (66%)" sedikit tidak konsisten (yang tepat 66,7% ≈ 67%), tetapi tidak mengubah kesimpulan sehingga tidak dihitung salah angka. Kekurangannya: (1) kesimpulan langsung "aman untuk ambil KUR" tanpa menyebut bahwa bank yang memutuskan (SLIK, agunan) dan tanpa disclaimer; (2) rasio aktivitas tidak dihitung, padahal stok Rp40 jt adalah 40% aset dan umurnya 35,8 hari; (3) ambang "cicilan maks 30–35%" disebut tanpa sumber; (4) tidak ada ambang per jenis/skala usaha dan tidak ada saran tindakan konkret; (5) cicilan pinjaman bank 15 jt yang sudah ada tidak ikut ditimbang. Dua catatan praktisnya (margin tipis, laba harus benar-benar jadi kas) berguna.

### analisis-rasio-keuangan-usaha — DENGAN (topik 1666, pesan 1801)

> Ringkasan: Toko untung Rp 24 juta setahun (margin 5,0%). Dari 11 rasio yang dinilai (ambang usaha dagang, skala mikro): 10 baik, 1 waspada, 0 bahaya.
> …
> • Tapi: risiko likuiditas jangka pendek SEDANG — kas+piutang (Rp 18 jt) belum cukup menutup total utang jangka pendek (Rp 25 jt = utang supplier 20 jt + utang lain 5 jt). Kas sendiri cuma menutup 48% dari situ. …
> • ⚠️ Umur stok 35,8 hari (waspada, idealnya ≤30 hari) — stok agak lama mengendap
> …
> Kesiapan KUR: ANGKA CUKUP SEHAT untuk dibawa ke bank.
> ✓ Cicilan Rp 500rb/bulan = 25% dari laba bersih bulanan (Rp 2 jt) → 🟢 AMAN secara angka
> 
> Saran: fokus benahi perputaran stok — coba catat stok per barang, kurangi belanja barang yang lambat laku, beli lebih sering tapi sedikit-sedikit.
> 
> Catatan penting: ini bacaan angka, bukan keputusan kredit — bank juga menilai SLIK OJK, agunan, dan legalitas. …

Alasan skor DENGAN: 8,0. Semua angka cocok dengan hitung ulang Python: rasio lancar 2,32; rasio cepat 0,72; rasio kas 0,48; margin kotor 15%; margin bersih 5%; ROA 24%; ROE 40%; DER 0,67 (67% modal); DAR 40%; umur stok 40×365/408 = 35,8 hari; lama piutang 6×365/480 = 4,6 hari (±5); bayar pemasok 20×365/408 = 17,9 hari (±18); kas menutup 12/25 = 48% utang lancar; cicilan 0,5/2 = 25%. Hitungan "11 rasio: 10 baik, 1 waspada" cocok dengan yang ditampilkan, dan skala mikro (penjualan 480 jt) sesuai. Nilai tambahnya: lampu status per rasio memakai ambang usaha dagang, umur stok ditandai waspada beserta langkah konkret (catat stok per barang, kurangi barang lambat laku, beli lebih sering sedikit-sedikit), dan risiko likuiditas SEDANG dijelaskan (kas + piutang 18 jt < 25 jt). Ia juga menanyakan apakah sebagian pinjaman bank jatuh tempo ≤ 12 bulan. Kesiapan KUR dijawab bersyarat ("bacaan angka, bukan keputusan kredit", SLIK OJK, agunan, legalitas) dan ada disclaimer. Pengurangnya: (1) kata proses bocor ke jawaban: "pakai skill rasio keuangan … pakai script" dan "bisa pakai skill pengajuan-kur"; (2) jenis dan skala usaha tidak diberi label "Asumsi:"; (3) agak membingungkan, karena rasio cepat diberi hijau sementara risiko likuiditas SEDANG, lalu ditutup "kalau pinjaman bank semuanya jangka panjang, berarti aman"; (4) rasio cicilan hanya memakai cicilan KUR baru, tanpa cicilan pinjaman bank 15 jt yang sudah ada; (5) hanya satu saran tindakan.

### tagih-piutang — TANPA (topik 1667, pesan 1803)

> Selamat siang Bu Dewi,
> 
> Mohon maaf mengganggu waktunya. Saya ingin menindaklanjuti tagihan katering makan siang bulan Agustus dari Dapur Sehati untuk PT Fiktif Makmur Sejahtera:
> 
> • No. Invoice: INV-KT-0825
> • Nominal: Rp 6.300.000
> • Jatuh tempo: 5 September 2026
> 
> Sebelumnya saya sudah mengirimkan pengingat via WhatsApp pada 8 dan 15 September, namun belum ada konfirmasi pembayaran dari pihak kami terima. … Pembayaran bisa ditransfer ke rekening berikut:
> BCA 000-000-0000 a.n. Dapur Sehati …

Alasan skor TANPA: Pesannya sopan dan ditujukan ke Bu Dewi. Isinya sudah memuat INV-KT-0825, Rp 6.300.000, jatuh tempo 5 September 2026, riwayat WA 8 & 15 September, rekening BCA, dan permintaan bukti transfer, lalu menawarkan versi WA. Namun nama pemilik rekening salah salin ("a.n. Dapur Sehati", padahal datanya "Dapur Sehati Fiktif"), sehingga skor maks. 5. Tanpa kesalahan itu skornya kira-kira 6. Kekurangan lain: (1) Dua pengingat sudah dibaca tanpa balasan, tetapi ini pengingat ketiga yang sama lunaknya; nada tidak naik. (2) Tidak ada hitungan hari terlambat, tenggat atau tanggal pasti, maupun langkah berikutnya. (3) Ada kalimat janggal "belum ada konfirmasi pembayaran dari pihak kami terima". (4) Pengirim hanya "Dapur Sehati", tanpa nama orangnya.

### tagih-piutang — DENGAN (topik 1668, pesan 1810)

> • Sudah terlambat 42 hari (dihitung per hari ini, 17 Oktober 2026) … • Karena ini pelanggan lama dan sudah 2x diingatkan tanpa hasil, tahapnya sudah masuk surat teguran resmi, bukan sekadar WA pengingat lagi … Kepada Yth.
> PT Fiktif Makmur Sejahtera
> u.p. Bu Dewi – Bagian GA … Mengingat kerja sama yang sudah terjalin baik selama ini, kami berharap pembayaran sebesar Rp 6.300.000 dapat diselesaikan paling lambat 24 Oktober 2026, ke rekening BCA 000-000-0000 a.n. Dapur Sehati Fiktif. … Apabila terdapat kendala atau sudah ada rencana pembayaran, mohon kabari kami agar dapat kami sesuaikan jadwalnya secara tertulis. … Tenggat di pesan ini: Sabtu, 24 Oktober 2026. Kalau sampai tanggal itu belum ada pembayaran atau kabar, pada Minggu, 25 Oktober 2026 sebaiknya konsultasikan ke advokat (misalnya opsi gugatan sederhana) — jangan kirim ancaman sendiri lewat WA. …

Alasan skor DENGAN: Ringkasan angka benar: Rp 6.300.000, tanpa denda, total sama. Telat 42 hari dihitung per 17 Okt (balasan 00.57 WIB, waktu Surabaya); hitung ulang Python: 5 Sep→16 Okt = 41, →17 Okt = 42. Nada naik sesuai riwayat: dua pengingat diabaikan, jadi dibuat surat teguran resmi yang tetap hormat ("Mengingat kerja sama yang sudah terjalin baik"), membuka opsi jadwal bayar tertulis, tanpa ancaman dan tanpa denda. Surat memuat u.p. Bu Dewi – Bagian GA, kronologi 8 & 15 Sep, tenggat 24 Okt (Sabtu, benar), dan rekening BCA a.n. Dapur Sehati Fiktif persis. Ada versi WA singkat plus saran melampirkan surat sebagai PDF, tanpa mengaku sudah mengirim. Bagian lain: tahap berikutnya 25 Okt (Minggu, benar), saran menyimpan bukti, kesepakatan cicilan tertulis bermeterai, dan disclaimer. Hanya satu pertanyaan di akhir (nama penandatangan); tidak ada kata proses. Minus 1,5: (1) menganggap "layanan katering masih berjalan", padahal tidak disebut pengguna; (2) sesudah satu minggu langsung menyarankan advokat/gugatan sederhana untuk pelanggan lama Rp6,3 juta, tanpa langkah lunak seperti telepon atau bertemu; (3) tenggat jatuh hari Sabtu; (4) nomor surat "-/DSF/ST/X/2026" setengah isian; (5) dasar hukum tidak menyebut UU Bea Meterai padahal menyarankan meterai.

### tender-checklist — TANPA (topik 1669, pesan 1813)

> Batas unggah penawaran yang disebutkan adalah 14 Oktober 2026, jam 15.00 — itu sudah lewat 3 hari. … Nilai HPS Rp185 jt / pagu Rp190 jt masih di kategori Usaha Kecil (batas pengadaan barang untuk Usaha Kecil/Koperasi: s.d. Rp2,5 M). … Dokumen yang biasanya dibutuhkan (pascakualifikasi via SPSE, pengadaan barang): … Subtotal (belum PPN) = Rp39.768.000
> 
> • PPN 11% = Rp4.374.480 … total rincian kamu (±Rp44 jt) cuma ~24% dari HPS Rp185 jt …

Alasan skor TANPA: Sisi ini kuat. Batas unggah yang sudah lewat langsung ditandai di awal. Ada daftar dokumen administrasi/teknis/kualifikasi yang cukup lengkap. Keempat baris rincian dihitung benar (DPP Rp39.768.000, PPN Rp4.374.480, total Rp44.142.480), dan ada peringatan bahwa total hanya ±24% HPS sehingga bisa kena evaluasi kewajaran. Ada salah fakta aturan: batas usaha kecil disebut Rp2,5 M (angka lama), sehingga skor dibatasi maks 5. Kekurangan lain: PPN disebut "tarif umum 11%" (padahal tarif 12% dengan DPP 11/12; nominalnya benar); ambang jaminan penawaran "di bawah Rp200 jt" rancu; ambang 80% HPS dan terbilang tidak disebut. Ada juga kata proses dan path ("saya cek dulu CSV-nya", "data/rincian-atk.csv"), tanpa dasar aturan atau penafian. Tanpa salah fakta skornya sekitar 7.

### tender-checklist — DENGAN (topik 1670, pesan 1819)

> batas unggah tender ini 14 Oktober 2026 jam 15.00 — sudah lewat 3 hari … 1. Kelayakan: IKUT DENGAN SYARAT (kalau jadwalnya belum lewat)
> • ✅ Pagu Rp190 juta (< Rp15 M) → dicadangkan untuk usaha kecil/koperasi … Subtotal (DPP): Rp39.768.000
> • PPN 11% (karena PKP): Rp4.374.480
> • Total: Rp44.142.480 — Empat Puluh Empat Juta Seratus Empat Puluh Dua Ribu Empat Ratus Delapan Puluh Rupiah … total penawaran cuma 23,86% dari HPS Rp185 juta — jauh di bawah ambang 80%. … siap-siap klarifikasi kewajaran harga dari pokja (bukti harga pemasok/nota beli), karena di bawah 80% HPS. …

Alasan skor DENGAN: Semua angka benar dan tidak ada rujukan pasal yang dikarang. Batas unggah yang sudah lewat menjadi hal pertama yang disampaikan, disertai saran cek adendum di SPSE. Kelayakan diberi vonis jelas (IKUT DENGAN SYARAT) dengan batas Rp15 M yang benar, KBLI, PKP, dan butir ❓ (pengalaman, daftar hitam, SPSE+TOTP). Cek harga lengkap: per baris, DPP, PPN, total, terbilang benar, dan 23,86% HPS dengan ambang 80% plus saran bukti harga pemasok. Ada bagian jadwal (semua tahap H sudah lewat, tawaran hitung ulang) dan 5 butir awas gugur yang relevan, termasuk Berita Acara Penjelasan dan adendum. Kekurangan: checklist dokumen yang ditanyakan pengguna tidak ada sama sekali, padahal bot sendiri menyebut "hasil cek lengkapnya". Tidak ada baris dasar aturan/penafian dan tidak ada pengingat PPh 22. Kalimat "tidak perlu jaminan penawaran/pelaksanaan kecuali nilai kontrak >Rp200jt" rancu, karena jaminan penawaran barang tidak terkait Rp200 jt. Ada kata proses "hitungan script".

### follow-up-prospek — TANPA (topik 1671, pesan 1823)

> Siap, ini draft follow-up WA buat Pak Joni:
> 
> ───
> 
> Selamat siang Pak Joni 🙏
> 
> Saya Rudi dari KasirPintar. Terima kasih sudah meluangkan waktu kemarin untuk demo aplikasi kasir di Resto Padang Rasa Minang.
> 
> Mau tanya kabar, apakah sudah sempat diskusi dengan Ibu soal paket KasirPintar (Rp199rb/bulan, gratis biaya setup)?
> 
> Oh ya, soal pertanyaan Bapak kemarin — printer struk lama (Epson TM-U220) bisa langsung dipakai, jadi tidak perlu beli printer baru.
> 
> Kalau ada pertanyaan lain atau mau jadwalkan sesi lanjutan sama Ibu, saya siap bantu kapan saja, Pak. 🙏
> 
> Salam,
> Rudi
> …

Alasan skor TANPA: Satu pesan WA yang singkat dan sopan. Isinya menyebut diskusi dengan Ibu secara wajar, harga Rp199rb/bulan + gratis setup, dan menjawab bahwa printer Epson TM-U220 bisa. Tidak ada diskon karangan dan tidak menekan. Kelemahannya, pesan menulis "meluangkan waktu kemarin" dan "pertanyaan Bapak kemarin", padahal demo 22 Sep sudah ±3,5 minggu lalu, jadi terasa basi/keliru bila dikirim hari ini (tidak dihitung salah fakta keras karena pengguna sendiri menulis "kemarin"). Selain itu tidak ada saran waktu kirim, tidak ada rencana bila tetap tidak dibalas, dan ajakan penutupnya longgar ("siap bantu kapan saja").

### follow-up-prospek — DENGAN (topik 1672, pesan 1838)

> Karena hari ini (Sabtu, 17 Oktober) sudah 25 hari sejak demo 22 September dan belum ada follow-up terkirim, saya buat ulang jadwalnya mulai dari hari ini (bukan dari 22 Sept yang sudah lewat jauh)…
> • Ke-1 · Senin, 19 Okt 2026 (digeser dari Minggu)
> • Ke-2 · Rabu, 21 Okt 2026
> • Ke-3 · Senin, 26 Okt 2026
> • Ke-4 · Senin, 2 Nov 2026
> 
> Pesan ke-1 · Senin, 19 Oktober 2026 · WA
> Selamat pagi, Pak Joni 🙏 Saya Rudi dari KasirPintar Fiktif. Beberapa waktu lalu saya sempat demo aplikasi kasir untuk Resto Padang Rasa Minang — paket Rp199.000/bulan, gratis setup, dan sudah dipastikan bisa langsung cetak struk ke printer Epson TM-U220 yang Bapak pakai sekarang. Apakah sudah sempat dibahas dengan Ibu? Kalau masih ada yang perlu dijelaskan, saya siap bantu, Pak.
> …

Alasan skor DENGAN: Bot menyadari sudah 25 hari sejak demo, lalu menyusun ulang jadwal mulai hari ini. Hasilnya 4 pesan WA bertanggal dengan nama hari dan jarak yang benar. Pesan ke-1 memakai "beberapa waktu lalu", bukan "kemarin", dan semua fakta (199 rb, gratis setup, Epson TM-U220) benar. Ibu disebut dengan sopan, dan pesan ke-3 menawarkan telepon 10 menit dengan Bapak & Ibu sekaligus dengan ajakan yang mudah dijawab ("balas 1 atau 2"). Fitur yang tidak diberikan pengguna diberi label "usulan — konfirmasi dulu", tidak ada diskon, ada pesan pamit yang sopan, dan ada aturan main jam kirim yang cocok untuk resto. Kekurangannya: hasilnya jauh lebih panjang dari permintaan satu pesan WA, satu baris asumsi memakai istilah proses ("sesuai aturan skill"), dan "belum ada follow-up terkirim" adalah asumsi yang tidak datang dari pengguna.
