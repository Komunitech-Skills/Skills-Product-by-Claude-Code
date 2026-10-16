# Gelombang Telegram 19 — 2026-10-16 (bot kedua)

Keputusan otomatis **90/92/93** (2026-10-16). Bot uji kedua `@KTclaude2bot` (OpenClaw 2026.10.2, model router Komunitech), grup uji internal Komunitech, topik baru 1620–1629. Pesan uji identik di sisi TANPA (topik `skills: []`) dan DENGAN skill. Indeks 0–2 terkirim 09:46–09:49 UTC; indeks 3 tertunda router mati (09:53–17:06) dan gateway terputus (17:02–17:12), diproses 17:12 sebagai pesan 1699; indeks 4–9 terkirim 17:18–17:33 UTC. Penilaian: satu penilai independen per skill + pemeriksa kedua yang berusaha membantah (angka dihitung ulang, kutipan dicocokkan ke id pesan); koreksi pemeriksa sudah diterapkan di tabel.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| surat-penawaran-harga (1.0.6) | 6,5 | 8,5 | +2 | **LOLOS** | Hanya sisi DENGAN yang memberi surat penawaran lengkap dengan perihal, terbilang, syarat bayar dan kirim yang pasti, isian kosong untuk rekening dan penanda tangan, daftar asumsi, dan teks WhatsApp siap kirim, sedangkan sisi TANPA hanya memberi surat polos dengan angka benar (dan keterangan tanpa PPN yang juga benar) serta syarat pembayaran "didiskusikan". |
| presentasi-instan (1.1.5) | 6,9 | 7,5 | +0,6 | **BELUM** (DENGAN < 8) | Hanya sisi DENGAN yang menandai data yang tidak Anda berikan (nama tim, ukuran pasar, pesaing, rincian dana, kontak) sebagai kolom [isi] dan menuliskan angka asumsinya (proyeksi 5 outlet Rp95 juta, valuasi Rp3 miliar = Rp450 juta dibagi 15%), tetapi berkas deck-nya tidak sampai ke chat Telegram, sedangkan sisi TANPA langsung mengirim file .pptx. |
| positioning-persona-usaha (1.0.6) | 5 | 8,5 | +3,5 | **LOLOS** | Hanya sisi DENGAN memilih satu target utama (karyawan kantoran, skor 86 lawan 82), membuat tokoh pembeli lengkap dengan pemicu dan keberatannya, memberi bio WA 100 karakter dan judul grup FB yang siap tempel, tidak mengarang klaim "higienis", dan mengingatkan untuk cek izin ke Dinkes. |
| cv-lamaran-ats (1.1.3) | 7 | 8 | +1 | **BELUM** (selisih < 1,5) | Hanya sisi DENGAN yang menghitung seberapa cocok Anda dengan lowongan (77 dari 100, lengkap dengan alasan dan celahnya), lalu menyertakan surat lamaran, email singkat, daftar periksa sebelum kirim (simpan PDF, nama berkas, tanpa NIK/agama), dan tiga pertanyaan bernomor soal VLOOKUP/Pivot Table, WMS, dan scan barcode; kedua sisi sama-sama tidak mengarang keahlian itu. |
| audit-akun-iklan (1.0.6) | 7,5 | 6 | −1,5 | **BELUM** (DENGAN < 8) | Hanya sisi DENGAN yang mulai memeriksa kesehatan pengaturan akun (pemasangan pixel, tujuan kampanye, keamanan 2 langkah, jumlah video iklan) lewat 8 pertanyaan, tetapi belum memberi skor, urutan perbaikan, atau rencana, sehingga untuk satu kalimat curhat "rasanya boncos" jawaban tanpa skill justru lebih berguna. |

Pembanding uji internal (skor promosi / `examples/`):
- surat-penawaran-harga: 6,0 → 8,5 (1.0.5).
- presentasi-instan: 6,0 → 8,5 (1.1.5).
- positioning-persona-usaha: 6,25 → 8,75 (1.0.5).
- cv-lamaran-ats: 6,0 → 8,5 (1.1.3).
- audit-akun-iklan: 6,0 → 8,5 (1.0.5).

Beda terhadap uji internal:
- **surat-penawaran-harga:** Di uji internal (1.0.5, jasa desain, diskon 10%) sisi TANPA kena kota "Jakarta" yang dikarang, kalimat "belum termasuk PPN" yang menyesatkan, dan surat yang hanya disimpan sebagai berkas (6,0). Di bot Telegram ketiga cacat itu tidak muncul: surat penuh tampil di chat, kota dari alamat, dan kalimat PPN benar. Karena itu TANPA naik ke 6,5 dan selisihnya menyempit dari 2,5 menjadi 2,0. Sisi DENGAN sama kuatnya (8,5), hanya ditambah penyebutan berkas lokal yang tidak muncul di uji internal.
- **presentasi-instan:** Di uji internal, deck HTML dibuat dan diperiksa langsung sehingga DENGAN 8,5 dan selisih +2,5; di bot Telegram berkas HTML tidak terkirim ke chat dan jawaban memuat istilah proses, sehingga DENGAN turun ke 7,5. Sisi TANPA di bot juga sedikit lebih baik daripada di uji internal (6,5 vs 6,0) karena langsung mengirim file .pptx dan memberi tanda estimasi pada angka proyeksi, sehingga selisih menyempit menjadi +1,0.
- **positioning-persona-usaha:** Selisih di bot (+3,5) lebih besar daripada uji internal (+2,5) karena jawaban TANPA di bot memuat klaim "higienis" yang dikarang, sedangkan skor DENGAN hampir sama (8,5 dibanding 8,75). Skenario uji internal berbeda (keripik tempe Malang dan tagline teh pelangsing), sehingga perbandingan ini hanya indikatif.
- **cv-lamaran-ats:** Di bot asli selisihnya hanya 1,0 (7,0 → 8,0) dibanding 2,5 pada uji internal: jawaban TANPA lebih rapi dan jujur daripada TANPA uji internal, sedangkan jawaban DENGAN terganggu penyebutan nama alat, sudut pandang orang ketiga, dan skor kata kunci yang berisik. Tugas uji internal juga berbeda (memancing gelar S1/Brevet/SAP palsu dan celah 21 bulan), sedangkan pesan di bot hanya meminta penyesuaian CV, sehingga keunggulan menolak karangan dan menandai celah kurang menonjol.
- **audit-akun-iklan:** Di uji internal pengguna membawa bukti lengkap (data iklan Shopee dan pengaturan akun) sehingga skill bisa menghitung skor 0-100, prioritas, dan titik impas sekaligus; di bot Telegram pengguna hanya menulis satu kalimat, jadi skill baru memberi titik impas dan daftar pertanyaan, sementara jawaban tanpa skill sudah lebih lengkap.

Catatan jujur (untuk pembeli):
- **surat-penawaran-harga:** DP 50% dan waktu kirim 3–7 hari kerja adalah tebakan bawaan, bukan dari Anda, jadi ubah sebelum surat dikirim. Nama penanda tangan dan nomor rekening masih kosong. Balasan juga menyebut berkas yang tersimpan di komputer bot dan tidak bisa dibuka dari Telegram, dan tabelnya lebar sehingga perlu digeser di layar ponsel.
- **presentasi-instan:** Di Telegram, berkas deck tidak ikut terkirim sehingga Anda perlu meminta filenya terpisah, dan deck masih menyisakan banyak kolom [isi] (nama tim, ukuran pasar, pesaing, rincian dana, kontak) yang harus Anda lengkapi sendiri sebelum bertemu investor. Jawabannya juga masih memuat istilah teknis seperti "cek otomatis".
- **positioning-persona-usaha:** Pemilihan karyawan kantoran sebagai target utama hanyalah perkiraan (skor 86 lawan 82 hampir seri dan bukan data pasar), jadi perlu dibuktikan dengan bertanya ke pelanggan sendiri; tokoh Mbak Dian rekaan, dan judul grup FB "Mulai 27rb/porsi" belum memakai harga langganan yang setara Rp25.000 per porsi. Rincian persona, tabel pembeda, dan uji 7 hari baru muncul bila Anda membalas "lengkap".
- **cv-lamaran-ats:** Skor kata kunci (mis. 45%) hanya hitungan kata sederhana dan bisa tampak rendah padahal CV sudah sesuai, jadi jangan dijadikan patokan lolos seleksi. Balasan juga memuat beberapa detail kecil yang tidak Anda sebutkan (lokasi perusahaan, "bekerja di bawah tekanan", "disampaikan ke atasan") dan masa kerja "2 tahun" hanya ditebak dari 2022–2024, jadi periksa lagi sebelum dikirim.
- **audit-akun-iklan:** Kalau pengguna hanya menulis satu kalimat tanpa data pengaturan akun, skill berhenti di titik impas lalu meminta 8 jawaban sebelum skor keluar, jadi pembeli awam bisa merasa belum dibantu. Skor kesehatan, prioritas, dan rencana 7 hari baru muncul setelah pemilik iklan menjawab atau menempelkan bukti.

Salah angka/fakta yang ditemukan:
- surat-penawaran-harga: tidak ada
- presentasi-instan: tidak ada
- positioning-persona-usaha: TANPA: klaim "lebih higienis" (dimasak & dianter khusus, bukan dipajang di etalase), "menu konsisten", dan "gak kena ongkir & biaya aplikasi" tidak disebut pemilik usaha, jadi karangan; sisi DENGAN tidak punya salah angka/fakta.
- cv-lamaran-ats: tidak ada
- audit-akun-iklan: tidak ada

Pemeriksa kedua:
- **surat-penawaran-harga:** koreksi — Message_id cocok: 1677 (topik 1620) dan 1680 (topik 1621) dari KTclaude2bot. Pesan 1679 "Working" diabaikan, dan tidak ada dokumen terkirim. Semua kutipan ada kata per kata. Hitung ulang dengan Python cocok: 3.750.000 + 3.000.000 + 12.000.000 = 18.750.000; diskon 937.500; total 17.812.500. Terbilang dan tanggal berlaku 30-10-2026 juga cocok. Skor 6,5 → 8,5 dan verdik LOLOS sesuai aturan, jadi tida
- **presentasi-instan:** koreksi — Kutipan dan id pesan cocok: 1689 berisi dokumen Bersih_Kilat_Pitch_Deck.pptx, 1690 ada di topik 1622, 1701 di topik 1623, dan tidak ada dokumen di 1623. Angka sudah dihitung ulang: 450 jt/0,15 = Rp3.000.000.000 (pra-uang 2,55 M), 38/2×5 = 95 jt, jumlah slide 12 dan 13. Tidak ada salah angka, dan verdik BELUM tetap. Masalahnya ada di skor TANPA. Rata-rata subskornya (7+8+5,5+6,5+7,5)/5 = 6,9, bukan
- **positioning-persona-usaha:** koreksi — Skor dan verdik cocok. Pesan 1703 (topik 1624) dan 1706 (topik 1625) dari KTclaude2bot. Pesan 1705 ("Working") diabaikan. Semua kutipan cocok persis dan tidak membalik makna. Hitung ulang: 125.000/5 = 25.000, bio = 100 karakter, 86−82 = 4 (≤ 5, jadi SETARA). Angka 27rb, 125rb, dan jam 10-11 sesuai pesan uji. Klaim "higienis" di 1703 dikarang, jadi TANPA maks. 5 sudah benar. DENGAN 8,5 dan selisih 
- **cv-lamaran-ats:** koreksi — Kutipan dan id cocok: 1708 di topik 1626, lalu 1718–1720 di topik 1627 dari KTclaude2bot (1712 "Working" diabaikan). Angka sudah dihitung ulang: (60×35+90×30+90×15)/80=76,875≈77; 14/31=45,16%; balasan 1718 terkirim 17:28 UTC = 00:28 WIB 17 Okt 2026, jadi tanggal surat benar. Skor 7→8 wajar dan verdik BELUM benar karena selisih 1,0<1,5. Ada dua cacat. Pertama, pembeda membesar-besarkan: balasan 170
- **audit-akun-iklan:** setuju — Penilaian ini saya setujui. Pesan 1725 (topik 1628) dan 1739 (topik 1629) berasal dari KTclaude2bot. Pesan 1733 berisi "Working" dan diabaikan. Tidak ada giliran konfirmasi lanjutan. Kutipan cocok dengan teks asli dan tidak membalik makna. Hasil hitung ulang Python: website 55.500 (62,36 %), GMV Max 33.695 (37,86 %), potongan 12.905 dan komisi 8.900. ROAS impas 1,6036/2,6413, dibulatkan ke atas me

## Kutipan balasan (dipendekkan, `…` = dipotong)

### surat-penawaran-harga — TANPA (topik 1620, pesan 1677)

> SURAT PENAWARAN HARGA
> No: 045/PSJ/SPH/X/2026 … Subtotal: Rp 18.750.000
> Diskon 5%: -Rp 937.500
> Ongkos kirim: Gratis (dalam kota)
> Total Penawaran: Rp 17.812.500 … • Harga berlaku selama 14 hari sejak tanggal surat ini.
> • Waktu pengerjaan dan pembayaran dapat didiskusikan lebih lanjut sesuai kesepakatan. … Mau saya buatkan versi PDF/Word-nya juga?

Alasan skor TANPA: Angka benar semua. Hitung ulang dengan Python: 500 x 7.500 = 3.750.000; 20 x 150.000 = 3.000.000; 1.000 x 12.000 = 12.000.000; subtotal 18.750.000; diskon 5% = 937.500; total 17.812.500; ongkir gratis; tanpa PPN karena belum PKP. Kota diambil dari alamat usaha, nomor surat 45 dipakai (ditulis 045/PSJ/SPH/X/2026), dan surat penuh tampil di chat. Kekurangannya: tidak ada terbilang, perihal, tempat nama penanda tangan, maupun teks WhatsApp. Syarat bayar dan kirim hanya "dapat didiskusikan lebih lanjut", padahal bendahara sekolah butuh ketentuan pasti. Masa berlaku 14 hari ditulis begitu saja tanpa dinyatakan sebagai tebakan, dan tidak ada daftar asumsi. Penutupnya hanya menawarkan PDF/Word. Surat bisa dipakai, tetapi pengguna masih harus melengkapi syaratnya sendiri.

### surat-penawaran-harga — DENGAN (topik 1621, pesan 1680)

> Nomor : 045/SPH/SJ/X/2026 … Diskon tambahan (5%) | −Rp 937.500 … TOTAL                | Rp 17.812.500 … Terbilang: Tujuh Belas Juta Delapan Ratus Dua Belas Ribu Lima Ratus Rupiah … 1. Harga final; penjual bukan PKP sehingga tidak memungut PPN. … ke [Bank – No. Rek – a.n.] … • Syarat bayar: DP 50% + pelunasan sebelum kirim (default) … Total: *Rp 17.812.500* (tanpa PPN, bukan PKP) … File lengkap juga tersimpan di workspace sebagai SPH-045.md

Alasan skor DENGAN: Semua angka benar dan sama dengan hitung ulang Python: ketiga baris, subtotal 18.750.000, diskon 937.500, total 17.812.500, terbilang "Tujuh Belas Juta Delapan Ratus Dua Belas Ribu Lima Ratus Rupiah", dan masa berlaku 14 hari dari 16 Okt 2026 = 30 Okt 2026. Total di tabel, terbilang, dan teks WhatsApp konsisten, tanpa PPN karena belum PKP. Surat lengkap berisi nomor, perihal, tabel, syarat bayar dan kirim, kolom rekening [Bank – No. Rek – a.n.] serta nama/jabatan penanda tangan yang dibiarkan kosong, lalu daftar asumsi (kota dari alamat, tanggal hari ini, DP 50%, kirim 3–7 hari kerja), catatan "bukan nasihat pajak", dan teks WhatsApp siap kirim. Kekurangannya: (1) menyebut berkas "SPH-045.md" tersimpan di workspace, yang tidak bisa dibuka dari Telegram (kata proses/path); (2) DP 50% dan 3–7 hari kerja adalah tebakan bawaan yang ikut masuk ke teks WhatsApp, meski sudah diberi tanda sebagai asumsi; (3) tabel tujuh kolom lebar di layar ponsel; (4) tidak ada tawaran revisi di akhir; (5) kode surat "SJ" dan format 045 tidak dicantumkan di daftar asumsi.

### presentasi-instan — TANPA (topik 1622, pesan 1689, 1690)

> Halo! Ini draft pitch deck Bersih Kilat (12 slide, format .pptx) — siap dipakai/diedit buat ketemu investor minggu depan: 1. Cover 2. Ringkasan Eksekutif 3. Masalah … 9. Penggunaan Dana (rincian Rp 450 juta) … 12. Penawaran — Rp 450 juta untuk 15% saham … Slide 12: valuasi post-money ~Rp 3 miliar itu cuma placeholder biar slide-nya lengkap, belum dihitung dari basis valuasi yang sebenarnya disepakati.

Alasan skor TANPA: Angka dihitung ulang dengan Python: valuasi Rp450 juta / 15% = Rp3.000.000.000 (pasca-uang; pra-uang Rp2.550.000.000), jadi sebutan "post-money ~Rp 3 miliar" benar; 12 judul slide yang disebut cocok dengan "12 slide". Plus: berkas Bersih_Kilat_Pitch_Deck.pptx (12 slide) benar-benar terkirim sebagai dokumen dan bisa diedit; jawaban mengakui angka volume kg dan proyeksi omzet di slide 5 dan 10 hanya hitungan kasar dari data pengguna, dan menyuruh cek ulang sebelum ke investor. Minus: isi berkas .pptx tidak dapat diperiksa penilai, hanya teks chat. Chat menyebut "rincian alokasi + grafik batang" untuk penggunaan dana Rp450 juta padahal pengguna tidak memberi rincian, tanpa label contoh atau [isian], sehingga berisiko tampil sebagai rencana nyata (pola yang sama dengan hasil uji internal). Asumsi "outlet baru menyusul outlet lama dalam 12 bulan" dikarang model tetapi disebutkan. Valuasi disebut "placeholder" padahal murni pembagian. Tidak menanyakan atau menandai nama tim dan kontak. Nilai: kebenaran 7, siap pakai 8, kepatuhan 5,5, perilaku 6,5, bahasa 7,5.

### presentasi-instan — DENGAN (topik 1623, pesan 1701; berkas: TANPA (topik 1622): Bersih_Kilat_Pitch_Deck.pptx, DENGAN (topik 1623): tidak ada berkas terkirim)

> Pitch deck untuk Bersih Kilat sudah jadi: pitch-bersih-kilat.html (13 slide) … Buka file-nya dua kali klik … Valuasi implied post-money Rp 3.000.000.000, dihitung murni dari Rp 450 juta ÷ 15% … Proyeksi omzet 5 outlet (Rp 95 juta) diasumsikan outlet baru punya performa rata-rata sama dengan outlet lama — ditandai jelas sebagai asumsi di slide … Perlu Anda lengkapi (ditandai kuning [isi] di slide): Nama lengkap Anda & nama adik Anda • Estimasi ukuran pasar Depok & Bogor • Data pembanding 2-3 laundry kiloan pesaing terdekat • Rincian rencana pakai dana • Nomor WA/email kontak … Hasil cek otomatis: LULUS, tanpa peringatan.

Alasan skor DENGAN: Angka dihitung ulang dengan Python dan semua benar: valuasi implisit pasca-uang Rp450 juta / 15% = Rp3.000.000.000 (disebut "implied post-money"); omzet Rp38 juta / 2 outlet = Rp19 juta, x 5 outlet = Rp95 juta; 13 judul slide yang disebut cocok dengan "13 slide"; omzet, pelanggan, dan harga dipakai persis. Plus: data yang tidak diberikan (nama pendiri dan adik, ukuran pasar Depok-Bogor, pembanding pesaing, rincian dana, target buka, kontak) ditandai kuning [isi]; asumsi (palet warna, valuasi, proyeksi) ditulis terbuka; kerjakan dulu tanpa bertanya; panduan buka, edit, dan cetak PDF jelas. Minus: (1) tidak ada berkas terkirim di topik 1623 sehingga pengguna Telegram tidak punya deck untuk dibuka, dan jawaban tidak menawarkan "balas kirim file"; (2) memuat istilah proses ("Hasil cek otomatis: LULUS, tanpa peringatan", "pakai skill laporan keuangan") dan nama berkas; (3) isi slide tidak tampil di chat, hanya daftar judul, dan enam hal harus dilengkapi pengguna. Isi HTML tidak dapat diperiksa karena tidak terkirim. Nilai: kebenaran 9, siap pakai 5, kepatuhan 7,5, perilaku 8, bahasa 8. Pesan uji 1691 dan balasan error 1692 diabaikan; balasan 1700 ("Working") diabaikan; hanya 1701 yang dinilai.

### positioning-persona-usaha — TANPA (topik 1624, pesan 1703)

> Untuk karyawan kantoran dan anak kos di Tembalang & Banyumanik yang nggak sempat masak atau bosan jajan sembarangan, Rantang Bu Wulan adalah katering rumahan harian yang rasanya kayak masakan rumah — diantar langsung tiap siang, lebih hemat dan higienis dibanding warteg atau GoFood/GrabFood. … vs Warteg: nggak usah keluar/antre, menu konsisten, lebih higienis (dimasak & dianter khusus, bukan dipajang di etalase). … Anak kos: butuh hemat — tekankan paket 5 hari (Rp25rb/porsi, lebih murah dari harga satuan Rp27rb) …

Alasan skor TANPA: Angka benar (paket 5 hari = Rp25.000/porsi, lebih murah dari Rp27.000) dan bahasanya enak dibaca, ada pernyataan positioning, pembeda terhadap tiga pesaing, tagline, dan contoh pesan WA. Kelemahannya: positioning dan pembeda memuat klaim "higienis", "menu konsisten", dan "tanpa ongkir" yang tidak pernah disebut pemilik (rawan jadi klaim menyesatkan bila ditempel ke iklan), "persona" yang dibuat hanya sosok Bu Wulan sebagai merek sehingga tidak ada tokoh pembeli beserta pemicu dan keberatannya, tidak ada pemilihan satu target utama (karyawan dan anak kos digabung), tidak ada teks bio yang sudah dihitung, tidak ada peringatan izin usaha pangan, dan ada placeholder [menu] tanpa penanda isian. Skor dibatasi maks. 5 karena ada fakta karangan.

### positioning-persona-usaha — DENGAN (topik 1625, pesan 1706)

> Segmen utama: karyawan kantoran Tembalang-Banyumanik (skor 86, nyaris sama dengan anak kos yang kerja skor 82 — SETARA, menang karena rute antar lebih hemat kalau konsentrasi di area kantor). … Persona: Mbak Dian, 26 th, staf admin kantor di Tembalang, gaji sekitar UMR Semarang. Buru-buru tiap pagi, males masak, order H-1 malam lewat WA, bayar transfer. Pemicu beli: capek dan nggak sempat; keberatan: takut menu bosan/telat … Positioning: Untuk karyawan Tembalang-Banyumanik yang nggak sempat masak siang, Rantang Bu Wulan adalah langganan makan siang rumahan yang diantar pas jam makan (10-11) … • Bio WA Business (100 karakter, aman): "Katering harian Tembalang & Banyumanik. Antar jam 10-11. 27rb/porsi, langganan 5hr 125rb. Order WA 👇" … Belum pakai klaim "sehat/bergizi/higienis" karena belum disebutkan … Mau versi lengkap (…)? Balas: lengkap.

Alasan skor DENGAN: Semua angka cocok dengan pesan uji dan hitungan ulang (Rp27.000 per porsi, paket 5 hari Rp125.000, antar 10-11, bio tepat 100 karakter; selisih skor 86 dan 82 = 4 poin sehingga memang SETARA). Hasilnya ringkas dalam satu pesan, urut dari kesimpulan (target utama, persona Mbak Dian, positioning, langkah pertama) ke teks siap tempel (bio, 5 tagline, sapaan WA dengan isian [isi: menu], judul grup FB). Klaim "sehat/bergizi/higienis" sengaja tidak dipakai karena belum disebut pemilik, skor ditandai perkiraan bukan data pasar, ada catatan izin SPP-IRT/Dinkes, dan versi lengkap ditawarkan lewat "Balas: lengkap". Cacat: judul grup FB "Mulai 27rb/porsi" padahal paket langganan setara Rp25.000/porsi; rincian persona (gaji sekitar UMR, order H-1, bayar transfer, tetap pesan GoFood sesekali) adalah dugaan tetapi tidak ditandai; istilah "SETARA" dan "skor" kurang dijelaskan untuk pembaca awam; positioning memuat nama GoFood dan warteg (cocok untuk internal, tidak untuk dipublikasikan); anti-persona dan uji 7 hari baru ada bila membalas "lengkap".

### cv-lamaran-ats — TANPA (topik 1626, pesan 1708)

> CV — Siti Rahma (disesuaikan untuk: Staff Admin Gudang — PT Sumber Makmur Logistik) … Staff Admin Gudang dengan pengalaman 2 tahun menangani pencatatan keluar-masuk barang, kartu stok manual, dan laporan stok bulanan. … Catatan dari saya: beberapa kualifikasi di lowongan (VLOOKUP/Pivot Table spesifik, aplikasi WMS, dan scan barcode) nggak kelihatan ada di pengalaman kamu yang diceritain ke saya — jadi nggak saya tulis di CV supaya nggak terkesan mengada-ada saat wawancara. …

Alasan skor TANPA: Balasan 1 pesan, tuntas dan siap tempel. Kejujuran inti terjaga: VLOOKUP/Pivot Table, WMS, dan scan barcode tidak ditulis di CV, dijelaskan alasannya, dan ditawarkan baris "bersedia belajar" atau pembaruan bila memang pernah. Kata kunci lowongan terpakai (Staff Admin Gudang, kartu stok, Microsoft Excel, inventory, stock opname, teliti, disiplin, SMK); format satu kolom tanpa tabel/foto, ramah ATS; nada santai konsisten tanpa kata proses. Kekurangan: tidak ada penilaian kecocokan atau skor kata kunci, tidak ada surat lamaran/email, tidak ada saran ATS (PDF, nama berkas). Ada tambahan kecil yang tidak disebut pengguna: butir "memastikan kesesuaian data stok fisik dengan catatan administrasi", "disiplin bekerja sesuai prosedur gudang", "target/deadline"; masa kerja "2 tahun" disimpulkan dari 2022–2024 tanpa ditandai sebagai asumsi. Nilai 7,0 (jujur dan rapi, tetapi minim tambahan).

### cv-lamaran-ats — DENGAN (topik 1627, pesan 1718, 1719, 1720)

> Skor akhir: 77/100 — Cocok, lamar sambil perkuat celah di surat lamaran … Skor Kecocokan Kata Kunci: 45% (14/31 kata kunci lowongan ditemukan di draf CV) … CV Versi ATS (siap tempel) … Surat Lamaran (Formal) … Email Singkat … Checklist Sebelum Kirim • Tidak ada pengalaman/gelar yang dikarang — semua dari data Kak Siti • CV satu kolom, tanpa tabel/foto … Perlu dikonfirmasi ke Kak Siti 1. Pernah pakai rumus VLOOKUP atau Pivot Table di Excel? … 2. Pernah pakai aplikasi WMS … 3. Pernah mengoperasikan mesin scan barcode? Kalau jawabannya "pernah", kabari saja — saya update CV-nya tanpa menebak-nebak dulu.

Alasan skor DENGAN: Balasan 3 pesan berurutan (kelanjutan mulus), semua utuh di chat. Angka benar: skor akhir 77/100 cocok dengan rumus bobot (60×35 + 90×30 + 90×15) ÷ 80 = 76,875 setelah dimensi preferensi dikeluarkan karena tak ada datanya; 14/31 = 45%; tanggal surat 17 Oktober 2026 benar menurut jam WIB saat balasan dikirim. Tidak mengarang WMS/barcode/VLOOKUP/Pivot Table; hanya ditandai sebagai celah dan ditanyakan 3 pertanyaan di akhir, setelah hasil diserahkan lebih dulu. Kata kunci lowongan terpakai lebih penuh (termasuk "di bawah tekanan"); format satu kolom ramah ATS; ada saringan wajib, surat lamaran, email, dan daftar periksa (PDF, tanpa NIK/agama/status). Kekurangan: kalimat pembuka menyebut "skill cv-lamaran-ats" dan "via script" dan ada kata "cek" (kata proses); pengguna disebut "Kak Siti" dengan sudut pandang orang ketiga padahal diajak bicara langsung; skor kata kunci 45% berisik (kata tunggal seperti "sistem" dan "kartu") dan bisa membingungkan; detail kecil tidak berdasar: "Bekasi" sebagai lokasi perusahaan, "disampaikan ke atasan", "terbiasa bekerja di bawah tekanan", "Excel dasar", dan "2 tahun" tidak ditandai asumsi, sementara daftar periksa menyatakan semuanya dari data pengguna. Nilai 8,0.

### audit-akun-iklan — TANPA (topik 1628, pesan 1725)

> Oke, saya hitungkan dulu unit economics-nya biar jelas boncos di mana.
> 
> Margin kotor per botol (sebelum biaya iklan)
> 
> Serum 20ml, harga jual Rp89.000, modal Rp32.000, kemas Rp1.500 → biaya dasar Rp33.500.
> 
> • Website (Shopify): kontribusi = 89.000 − 33.500 = Rp55.500/botol (margin 62,4%)
> • TikTok Shop (GMV Max): kena potongan platform 14,5% (Rp12.905) + afiliasi 10% (Rp8.900) = Rp21.805 fee tambahan → kontribusi = 89.000 − 33.500 − 21.805 = Rp33.695/botol (margin cuma 37,9%)
> 
> Jadi dari harga jual yang sama, channel TikTok Shop "kehilangan" hampir Rp22rb/botol lebih banyak dibanding jualan di w…

Alasan skor TANPA: Hitungan benar semua (hitung ulang sendiri): margin website 89.000 − 32.000 − 1.500 = 55.500 (62,4 %), GMV Max 55.500 − 12.905 − 8.900 = 33.695 (37,9 %), ROAS impas 1,60 dan 2,64, volume impas ±82 dan ±179 botol per bulan. Langsung menjawab "di mana boncosnya" dengan angka, memberi 3 saran, dan bertanya satu hal di akhir. Cacat kecil: "hampir 2x lipat" padahal rasionya 1,65x, "biang keladi boncosnya" ditulis sebelum ada data ROAS aktual, dan tidak menyentuh pengaturan akun.

### audit-akun-iklan — DENGAN (topik 1629, pesan 1739)

> Audit lagi jalan — saya udah hitung breakeven dulu dari data yang kamu kasih, sebelum nembak kesimpulan "boncos":
> 
> ROAS impas (titik psbk, di bawah ini pasti rugi):
> 
> • Serum 20ml, harga Rp89rb, modal Rp32rb
> • TikTok Ads → website (Shopify): potongan platform 0% (cuma modal+kemas) → ROAS impas = 1,61
> • TikTok Shop GMV Max: potongan 14,5% + komisi afiliasi 10% = 24,5%, + kemas Rp1.500 → laba kotor/pesanan Rp33.695 → ROI impas = 2,65
> 
> Jadi kalau ROAS TikTok Ads kamu di bawah 1,61, atau ROI GMV Max di bawah 2,65 — itu udah pasti rugi per pesanan, bukan cuma "kerasa" boncos.
> 
> Supaya bisa saya kasih skor kesehatan lengkap + urutan prioritas benerinnya (bukan cuma breakeven doang), tolong jawab sekali ini aja ya:
> 
> 1. ROAS rata-rata TikTok Ads (ke website) bulan ini & ROI rata-rata GMV Max bulan ini — berapa?
> 2. Tujuan kampanye TikTok Ads yang dipilih: Konversi/Penjualan, atau Traffic/lainnya?…

Alasan skor DENGAN: Angka benar: ROAS impas website 1,61 dan GMV Max 2,65 (pembulatan ke atas dari 1,6036 dan 2,6413, sengaja konservatif) dan laba kotor GMV Max Rp33.695; klaim "boncos" dikaitkan jelas dengan ambang angka. Namun laba per botol website (55.500) tidak disebut eksplisit, tidak ada margin persen, volume impas, atau saran, "Audit lagi jalan" memberi kesan hasil akan menyusul padahal menunggu 8 jawaban, ada salah ketik ("titik psbk"), dan 8 pertanyaan sekaligus berat untuk pembeli awam. Tidak ada skor, prioritas, atau rencana 7 hari.
