# Gelombang Telegram A4 — 2026-10-17 (bot pertama)

Uji ini berlangsung di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A) di OpenClaw 2026.10.2, pada 17 Okt 2026 pukul 05:48–06:10 UTC, di topik baru 2031–2038. Pesan uji sama persis di sisi TANPA (topik dengan `skills: []`) dan DENGAN skill. Pesan dan kunci jawaban diambil dari `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json`, dan pra-ceknya ada di `koordinasi/pracek-telegram-akun-a-2026-10-17.md`. Penilai independen (bukan pembuat skill) memakai skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Semua angka kunci dihitung ulang dengan Decimal: CSV laporan dari `pilot/data-a-cepat/laporan-otomatis-terjadwal/`, tarif TER B dari `skills/pph21-ter/references/tabel-ter.md`, dan THR dengan aturan di `skills/hitung-thr/SKILL.md`. Bukti kirim dicocokkan ke log gateway `gw-20261017-0547.log`. Jawaban ganda yang identik di transkrip adalah salinan log dan hanya dihitung sekali.

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| laporan-otomatis-terjadwal | 1.1.9 | 2031 / 2032 | 5,0 | 8,0 | +3,0 | **LULUS** | Dengan skill, Anda lebih dulu melihat contoh laporan dari data Anda sendiri (omzet Rp1.861.000, hari terbaik dan terendah, produk terlaris, semuanya benar), dan tidak ada jadwal yang dipasang sebelum tujuan kirimnya jelas. Tanpa skill, bot langsung memasang jadwal sungguhan ke grup dan memindahkan berkas Anda tanpa bertanya, padahal belum ada satu angka pun yang ditunjukkan. |
| checklist-keamanan-pangan-usaha | 1.0.3 | 2033 / 2034 | 7,0 | 8,5 | +1,5 | **LULUS** (batas bawah) | Dengan skill, Anda mendapat checklist yang siap dicentang, kartu 10 aturan untuk ditempel di dapur, dan batas waktu matang-sampai-dimakan. Anda juga diingatkan bahwa sertifikasi halal usaha mikro dan kecil wajib mulai 18 Oktober 2026 (besok). Kedua versi sama-sama menolak ayam 63 °C. |
| pph21-ter | 1.0.6 | 2035 / 2036 | 4,5 | 9,0 | +4,5 | **LULUS** | Dengan skill, potongan bulanan benar (Rp85.000, dan Maret Rp1.190.000). Desember terlihat sebagai kelebihan potong Rp94.250 yang wajib dikembalikan ke karyawan. Tanpa skill, tarif bulanannya salah, sehingga potongan setiap bulan dan angka Desember juga salah. |
| hitung-thr | 1.0.11 | 2037 / 2038 | 7,0 | 8,0 | +1,0 | **BELUM** (selisih < 1,5) | Dengan skill, Anda juga mendapat hari batas bayar (Rabu, 3 Maret 2027), info denda 5% bila terlambat, dan draf pengumuman grup tanpa nominal per orang. Namun versi tanpa skill sudah menghitung THR tiap orang dengan benar, sehingga selisihnya kecil. |

Pembanding uji internal lama (`examples/00-openclaw-sebelum-sesudah.md`): hitung-thr 1.0.10 rata-rata 5,0 → 7,7 / 8,0 (BELUM tipis). Untuk pph21-ter dan laporan-otomatis-terjadwal, rata-rata DENGAN di uji lama 8,0 dan 7,5. Pra-cek konteks Telegram 17 Okt memberi keempat skill status SIAP KIRIM (8,0 / 8,0 / 8,5 / 8,0).

Catatan lintas skill:
- **Istilah proses atau jalur berkas yang tampil:**
  - laporan-otomatis-terjadwal DENGAN menyebut folder `laporan/masuk/penjualan-mingguan/` dan "sesuai aturan privasi data usaha". Folder itu milik pengguna, jadi masih wajar.
  - Sisi TANPA menyebut folder yang sama, nama berkas CSV, dan mengaku sudah memindahkan berkas.
  - checklist DENGAN menampilkan label kurator "PERLU REVIEW" di judul Perizinan. Istilah ini asing bagi pembeli; lebih baik diganti "perlu dicek ke dinas".
- **Tabel Markdown mentah:**
  - hitung-thr DENGAN memuat tabel 5 kolom yang lebar, tampil sebagai garis `|` di Telegram, dan sulit dibaca di HP.
  - Draf teks grup ada di blok kode. Itu wajar karena memudahkan disalin.
  - Skill lain tidak memakai tabel. pph21-ter kini memakai butir, bukan tabel 4 kolom seperti saat pra-cek.
- **Panjang:**
  - checklist DENGAN 8.368 karakter terkirim dalam 4 bagian (`chunkCount=4`, pesan 2060), utuh dan berurutan.
  - Sisi TANPA 8.445 karakter terkirim dalam 2 pesan (2053–2054).
  - Jawaban lain 1 bagian.
- **Terpotong:** tidak ada.
- **Kontaminasi antarsisi:** sisi TANPA (2031) memindahkan CSV ke `laporan/masuk/penjualan-mingguan/`, lalu sisi DENGAN (2032) membaca berkas di folder baru itu, karena workspace bot dipakai bersama. Ini tidak mengubah angka. Untuk uji berikutnya, kembalikan berkas sebelum sisi DENGAN dijalankan.

## Rincian per skill

### laporan-otomatis-terjadwal 1.1.9 — TANPA 5,0 → DENGAN 8,0 (+3,0) LULUS

**Bukti kirim:** sisi TANPA di topik 2031, pesan 2046. Log gateway mencatat `cron: job added` (12:56:13 WIB) sebelum balasan. Jadwal sungguhan "Laporan Penjualan Mingguan (Senin 07:00)" dengan `cron 0 7 * * 1 @ Asia/Jakarta` → `announce -> telegram:-1004407409583:topic:2031` (`hasil/a4/cron-2031-dicatat.txt`), lalu dihapus Akun A (`cron: job removed` 13:11:21). Sisi DENGAN di topik 2032, pesan 2051. Di log **tidak ada** `cron.add` selama giliran 2032, jadi tidak ada jadwal yang dibuat.

**Angka kunci (dihitung ulang dari CSV):** 57 baris, omzet Rp1.861.000, 103 pcs, dan rata-rata per hari Rp1.861.000 ÷ 7 = Rp265.857. Hari terbaik 6 Okt Rp311.000 dan terendah 7 Okt Rp209.000. Produk menurut omzet: Roti Bakar Keju 29 pcs Rp580.000, Kopi Susu Gula Aren 31 pcs Rp558.000, Americano 19 pcs Rp285.000. Semua angka DENGAN benar. Sisi TANPA tidak menampilkan angka.

Kutipan DENGAN:
> Oke, saya sudah cek dulu datanya sebelum janji apa-apa. 👇
> **Contoh laporan (dari data ini, bukan contoh karangan):**
> > Total omzet: Rp 1.861.000 … Rata-rata omzet/hari: Rp 265.857 … Hari terbaik: 6 Okt 2026 (Rp 311.000)
> Jadwalnya saya catat: tiap Senin jam 7 pagi WIB.
> … laporan ini **tidak boleh dikirim ke grup ini** (harus ke pemilik/admin pribadi saja …). Boleh tolong kirim pesan apa saja ke bot saya lewat chat pribadi (DM) …

**Alasan skor DENGAN 8,0:**
- (+) Sesuai aturan skill: tidak ada aksi kirim atau jadwal sebelum tujuan dan persetujuan jelas. Bagi pembeli awam, ini sisi yang **lebih aman**.
- (+) Contoh laporan dari data asli, dengan semua angka benar.
- (+) Laporan menolak dikirim ke grup dan memberi jalan keluar yang benar: bot Telegram baru tahu ID chat pribadi setelah pengguna mengirim DM.
- (−) "Jadwalnya saya catat" ambigu, karena bisa dibaca seolah jadwal sudah aktif. Belum ada ringkasan rencana dengan "uji kirim sekali" dan pertanyaan "Lanjut? (ya/tidak)".
- (−) Label "Transaksi: 57 baris penjualan" kurang awam.
- (−) Ada sebutan folder dan frasa "aturan privasi".

**Alasan skor TANPA 5,0:** Secara teknis permintaan terlaksana: jadwal Senin 07:00 WIB benar-benar terpasang. Namun bot bertindak tanpa konfirmasi:
- Jadwal sungguhan dipasang ke **grup** (topik 2031), padahal pengguna meminta "telegram saya". Bot sendiri mengakui hal ini, tetapi tetap memasangnya "supaya jadwalnya tetap jalan".
- Berkas pengguna dipindahkan tanpa izin.
- Bot mengklaim "file yang sudah terpakai otomatis diarsipkan" tanpa bukti.
- Tidak ada contoh laporan atau angka apa pun.

Bila ini akun pembeli, data penjualan akan terkirim otomatis ke grup setiap Senin.

### checklist-keamanan-pangan-usaha 1.0.3 — TANPA 7,0 → DENGAN 8,5 (+1,5) LULUS (batas bawah)

**Pengiriman:** topik 2034, pesan 2060, `chunkCount=4`, utuh. Sisi TANPA (2033) terkirim sebagai pesan 2053–2054.

**Kunci:**

| Kunci | DENGAN | TANPA |
|---|---|---|
| Ayam inti ≥ 74 °C, 63 °C ditolak | Ya | Ya, dengan penjelasan sous-vide yang benar |
| SPP-IRT tidak untuk nasi box, yang relevan SLHS | Ya | Ya, dan menambah "Golongan A1" |
| Halal UMK wajib 18 Okt 2026 | Ya, ditambah jalur Self Declare/SEHATI | Hanya "wajib bertahap", tanpa tanggal |

Kutipan DENGAN:
> Soal ayam 63 °C dulu: **tidak boleh, tolong jangan dipakai.** Ayam … wajib matang inti **≥ 74 °C** … Lebih cepat matang: potong lebih kecil/tipis sebelum digoreng, bukan menurunkan target suhu.
> ☐ Total waktu dari makanan matang keluar wadah panas sampai dimakan pelanggan: **maksimal 2 jam** (kalau cuaca panas terik/siang bolong, anggap **maksimal 1 jam** saja)
> Saat ini **log suhu belum bisa diisi dengan akurat karena belum ada termometer** — jangan diisi kira-kira …
> - **Sertifikasi halal: WAJIB**, bukan opsional. Usaha mikro/kecil wajib mulai 18 Oktober 2026 (tinggal beberapa hari lagi) …

**Alasan skor DENGAN 8,5:**
- (+) Checklist siap dicentang (☐) per tahap: datang, masak, kemas, antar, dan tutup. Ada juga daftar mingguan, kartu 10 aturan staf, dan peta risiko per menu, termasuk Bacillus cereus di nasi.
- (+) Bot jujur soal log suhu tanpa termometer. Batas waktu dikaitkan dengan antar 1 jam.
- (+) Asumsi ditulis, dan pertanyaan di akhir dibatasi tiga.
- (−) Label "PERLU REVIEW" tampil ke pembeli.
- (−) Suhu telur sedikit membingungkan ("≥ 63–71 °C").
- (−) Saran membeli termometer kulkas tidak eksplisit (yang disebut termometer tusuk). Kedelai/kecap tidak dibahas.
- (−) "Tinggal beberapa hari lagi" kurang tepat, karena tenggatnya besok.
- (−) Sangat panjang (4 bagian).

**Alasan skor TANPA 7,0:** Isinya benar dan praktis: 74 °C dengan cara cek tanpa termometer, termometer kulkas Rp30–50 rb, SLHS bukan PIRT, dan pelatihan penjamah. Kekurangannya:
- Tanggal wajib halal tidak disebut.
- Format berupa daftar tips, bukan checklist untuk dicentang.
- Alergen dikarang lebar: kacang "kadang pakai", dan MSG disebut padahal bukan alergen.
- Tidak ada log atau kartu staf.

### pph21-ter 1.0.6 — TANPA 4,5 → DENGAN 9,0 (+4,5) LULUS

**Pengiriman:** topik 2036, pesan 2066, 1 bagian, utuh.

**Angka kunci (dihitung ulang, Decimal):**
- TER B Rp8.500.000 masuk rentang 7,3–9,2 jt, jadi tarifnya 1% = Rp85.000.
- Maret Rp17.000.000 masuk rentang 16,4–18,45 jt, jadi tarifnya 7% = Rp1.190.000.
- Jan–Nov = 10 × 85.000 + 1.190.000 = Rp2.040.000.
- Setahun: bruto Rp110.500.000, biaya jabatan 5% Rp5.525.000, iuran 3% × Rp102.000.000 = Rp3.060.000, neto Rp101.915.000, dikurangi PTKP K/1 Rp63.000.000, PKP Rp38.915.000, dan PPh 5% = Rp1.945.750.
- Desember = 1.945.750 − 2.040.000 = **−Rp94.250** (lebih potong).

Semua angka DENGAN benar. Sisi TANPA memakai TER B 1,25% (Rp106.250) dan 5% untuk Maret (Rp850.000). Akibatnya Jan–Nov Rp1.912.500 dan Desember +Rp33.250, sehingga **angka kunci salah** (maks 5). Total setahun Rp1.945.750 di sisi TANPA benar, karena berasal dari perhitungan Pasal 17.

Kutipan DENGAN:
> • Jan, Feb, Apr–Nov (10 bulan): bruto Rp 8.500.000 → tarif TER 1% → PPh 21 Rp 85.000/bulan
> • Maret (gaji + THR): bruto Rp 17.000.000 → tarif TER 7% → PPh 21 Rp 1.190.000
> • Desember: … **lebih potong Rp 94.250** (bukan bayar lagi, malah kelebihan)
> Bapak wajib kembalikan kelebihan itu ke karyawan, paling lambat akhir Januari 2027.

**Alasan skor DENGAN 9,0:**
- (+) Benar, ringkas (1 pesan, tanpa tabel), dan menjawab "kenapa Desember beda" dengan bahasa awam.
- (+) Tenggat pengembalian kelebihan potong disebut.
- (+) Asumsi ditulis (tidak ada premi JKK/JKM, tidak ada DTP karena bengkel bukan sektor PMK 105/2025). Ada dasar aturan dan disclaimer.
- (−) Istilah "Masa Pajak Terakhir" dan "bruto" tidak dijelaskan.
- (−) Tidak ada catatan pembulatan yang belum dicocokkan dengan Coretax.

**Alasan skor TANPA 4,5:** Struktur dan penjelasan Pasal 17 benar. Namun tarif TER salah, sehingga potongan setiap bulan salah dan Desember menjadi "kurang potong", padahal seharusnya lebih potong. Pemilik akan memotong dan menyetor angka yang salah selama 11 bulan.

### hitung-thr 1.0.11 — TANPA 7,0 → DENGAN 8,0 (+1,0) BELUM

**Pengiriman:** topik 2038, pesan 2071, 1 bagian, utuh.

**Angka kunci (dihitung ulang):**

| Karyawan | Masa kerja s.d. 10 Mar 2027 | Perhitungan | THR |
|---|---|---|---|
| Andi | 74 bulan | 3.800.000 + 400.000 (uang makan harian tidak ikut) | Rp4.200.000 |
| Sari | 1 Apr 2026, 11 bulan | 11/12 × 3.200.000 = 2.933.333,33 | Rp2.933.333 |
| Dodi | 2 Agu 2026, 7 bulan | 7/12 × 3.100.000 = 1.808.333,33 | Rp1.808.333 |
| Yanto | 15 Jan 2026, 13 bulan, PKWT | penuh | Rp3.500.000 |

Total per orang setelah pembulatan Rp12.441.666. Batas bayar: 10 Mar 2027 − 7 hari = Rabu, 3 Maret 2027.

DENGAN benar semua. TANPA benar per orang, tetapi totalnya Rp12.441.667: ini total dari angka belum bulat, berselisih Rp1 dari jumlah barisnya sendiri. Ini dicatat sebagai selisih pembulatan, bukan salah angka kunci.

Kutipan DENGAN:
> Lebaran 2027 saya anggap jatuh **Rabu, 10 Maret 2027** (perkiraan; tanggal resminya menunggu penetapan pemerintah) …
> | **Total THR** | | | | **Rp 12.441.666** |
> - **Paling lambat dibayar: Rabu, 3 Maret 2027** (H-7 sebelum lebaran). Kalau telat, ada denda 5% dari total THR dan THR tetap wajib dibayar penuh.
> **B. TEKS GRUP — draf untuk Anda tempel sendiri (tanpa nominal per orang)**

**Alasan skor DENGAN 8,0:**
- (+) Angka benar, dan tanggal Lebaran ditandai sebagai perkiraan.
- (+) Ada info denda 5%, draf pengumuman tanpa nominal, dan tawaran menghitung PPh 21 THR bila status PTKP diberikan.
- (−) Tabel 5 kolom tampil mentah di Telegram. Ini cacat yang paling terlihat.
- (−) Bagian "KHUSUS PEMILIK/HR … jangan ditempel ke grup" justru tampil di topik grup dengan nominal per orang.
- (−) Satu pertanyaan penutup mengulang soal PTKP.

**Alasan skor TANPA 7,0:**
- (+) Semua THR per orang benar, termasuk uang makan yang dikeluarkan dan PKWT 13 bulan yang mendapat THR penuh. Batas 3 Maret 2027 benar.
- (−) Selisih total Rp1.
- (−) Tidak ada nama hari, info denda, draf pengumuman, atau catatan bahwa tanggal Lebaran masih perkiraan.

**Perbaikan paling berdampak (BELUM):**
1. Untuk kanal chat, ganti tabel rekap dengan butir per orang ("• Andi — 74 bln — 1 × Rp4.200.000 = **Rp4.200.000**").
2. Bila permintaan datang dari grup, jangan tampilkan nominal per orang di grup. Tampilkan total dan draf pengumuman saja, lalu tawarkan rincian lewat chat pribadi.
3. Tampilkan dampak PPh 21 THR sebagai nilai tambah yang tidak dimiliki model dasar. Contohnya: tambahan potongan di bulan THR dengan asumsi status PTKP yang ditandai, bukan sekadar ditawarkan.
4. Untuk uji berikutnya, pakai kasus yang biasanya membuat model dasar salah: harian lepas atau satuan hasil (rata-rata upah), masuk di tengah bulan dengan masa kerja < 1 bulan, atau karyawan yang di-PHK sebelum Lebaran. Dengan kasus seperti itu, nilai tambah skill bisa terukur.
