# Telegram gelombang 10 — 3 skill (2026-10-05)

Persetujuan pemilik: keputusan no. 17. Penilaian oleh **penilai independen** (agent terpisah, bukan pembuat skill dan bukan pengirim pesan). Data di pesan uji fiktif. Nama dan nomor tidak disalin ke laporan ini.

## Cara
- 6 topik di grup uji (865–870): topik ganjil = `TANPA skill` (setelan `skills: []` per topik), topik genap = `DENGAN skill`.
- Sebelum kirim, skill di bot produksi disinkronkan ke versi repo oleh agent pengirim (backup `scratchpad/openclaw-real/skills-backup-20261005-g10` dan config `openclaw.json.before-gelombang10-*`). laporan-status-kantor sudah sama; sop-onboarding dan strategi-konten-iklan diperbarui.
- Bot penguji mengirim 6 pesan (1 per sisi per skill), identik untuk kedua sisi (`scratchpad/pilot/msgs-g10.json`), berurutan dengan jeda, tanpa balas-otomatis. Semua 6 terkirim (18:16–18:25 UTC). Jawaban diambil dari Telegram (`scratchpad/pilot/jawaban-g10-tg.txt`). Tidak ada timeout. Balasan sop-onboarding DENGAN terpecah menjadi 3 pesan Telegram (utuh).
- Versi yang diuji (catalog.csv): sop-onboarding **1.0.5**, strategi-konten-iklan **1.0.6**, laporan-status-kantor **1.0.7**.
- **Penilaian:** versi pertama laporan ini dinilai sendiri oleh agent pengirim (menyalahi aturan "penilai terpisah"). Laporan ini **ditulis ulang oleh penilai independen** yang menilai dari nol; skor pengirim hanya dicantumkan sebagai pembanding. Penilai hanya membaca pesan uji, jawaban bot, folder skill untuk cek fakta, dan sumber web. Semua angka dihitung ulang dengan python; `scripts/jadwal_onboarding.py` dan `scripts/alokasi_anggaran.py` dijalankan ulang.
- Skor 1–10 per sisi menimbang ketepatan, siap pakai, aturan Indonesia, keamanan/etika (klaim pelangsing, janji ROAS, privasi gaji/THR), dan kejelasan di Telegram.

## Hasil

| Skill | TANPA | DENGAN | Selisih | Verdik | Skor pengirim (pembanding) |
|---|---|---|---|---|---|
| sop-onboarding | 6,5 | 8 | +1,5 | **LULUS** (tepat di batas) | 6,5 → 8,5 (+2), LULUS |
| strategi-konten-iklan | 6 | 8,5 | +2,5 | **LULUS** | 6 → 8,5 (+2,5), LULUS |
| laporan-status-kantor | 4,5 | 5 | +0,5 | **BELUM** | 4,5 → 5 (+0,5), BELUM |

Rata-rata 3 pasang: TANPA 5,7 → DENGAN 7,2 (selisih +1,5).

Pembeda (satu kalimat):
- **sop-onboarding:** DENGAN memberi paket utuh dengan jadwal yang tepat (checkpoint 10 Nov/10 Des/9 Jan, batas masa percobaan 11 Jan 2027, evaluasi keputusan Rabu 6 Jan 2027), SOP kasir 7 langkah, checklist BPJS, dan cek UMK; TANPA menulis evaluasi "paling lambat 12 Jan 2027" (melewati batas 11 Jan yang ia tulis sendiri) dan "~20 hari kerja" untuk 12–31 Okt (seharusnya 18).
- **strategi-konten-iklan:** DENGAN menolak "turun 5kg seminggu" dengan dasar yang tepat (UU 8/1999, PerBPOM 1/2022 Pasal 28 huruf g vs PerBPOM 34/2022, cek kategori izin edar), memberi ROAS impas 2,50x, target aman 3,58x, dan anggaran per minggu Rp300rb/600rb/300rb/300rb yang naik di minggu 10.10; TANPA salah menjelaskan ROAS ("Rp1 iklan harus balik jadi Rp2.500"), memberi patokan "3–5x" tanpa sumber, dan menyarankan video "testimoni" untuk produk pelangsing.
- **laporan-status-kantor:** kedua sisi menolak nominal THR per orang di grup dengan benar, tetapi **keduanya tidak memberi teks pengumuman**; DENGAN menanyakan tanggal cuti bersama yang sudah ada di rujukan skill.

**Beda dengan pengirim:** hanya sop-onboarding DENGAN (8 vs 8,5). Penilai mengurangi 0,5 karena tabel Markdown 6 kolom berisi kalimat panjang tampil sebagai teks berpipa di Telegram (sulit dibaca di ponsel), judul "5. Catatan Aturan" terpisah dari isinya karena pecahan pesan, urutan baris "Evaluasi keputusan 6 Jan" diletakkan setelah "Batas hukum 11 Jan" (urutan tanggal membingungkan), dan kata "skill" bocor. Isinya tetap benar dan siap pakai, sehingga verdik **tidak berubah**: selisih +1,5 tepat memenuhi acuan. Verdik ketiga skill sama dengan pengirim; `promosi/sebelum-sesudah.jsonl` tidak diubah.

Memenuhi acuan (DENGAN ≥ 8 **dan** selisih ≥ 1,5): **strategi-konten-iklan** (8,5; +2,5) dan **sop-onboarding** (8; +1,5, mepet di kedua batas). Tidak memenuhi: **laporan-status-kantor** (5 < 8; +0,5 < 1,5).

## Verifikasi angka (python, penilai independen)

**sop-onboarding** (mulai Senin 12 Okt 2026, PKWTT, percobaan 3 bulan, 6 hari kerja/minggu)
- 12 Okt 2026 = **Senin** ✅ (kedua sisi).
- `jadwal_onboarding.py --mulai 2026-10-12 --hari-kerja 6 --jenis pkwtt` dijalankan ulang: akhir minggu 1 = 18 Okt (Minggu) → **19 Okt**; checkpoint +29/+59/+89 hari = **10 Nov 2026 (Sel) / 10 Des 2026 (Kam) / 9 Jan 2027 (Sab, hari kerja bila 6 hari)**; batas hukum **11 Jan 2027 (Senin)**; evaluasi keputusan **6 Jan 2027 (Rabu)** = 5 hari kerja mundur (11, 9, 8, 7, 6 Jan; Minggu 10 Jan dilewati). Tabel DENGAN **identik** ✅.
- Dengan 5 hari kerja/minggu evaluasi keputusan menjadi **5 Jan 2027** (11, 8, 7, 6, 5 Jan). DENGAN menyebut asumsi 6 hari dan menawarkan hitung ulang ✅.
- TANPA: masa percobaan "12 Okt 2026 s/d 11 Jan 2027" ✅; "Evaluasi akhir … paling lambat 12 Jan 2027" ❌ (12 Jan = Selasa, sehari setelah batas); "evaluasi final 11 Jan" ⚠️ (keputusan di hari terakhir). "12–31 Okt = ~20 hari kerja" ❌: 20 hari kalender; hari kerja **18** (6 hari/minggu) atau **15** (5 hari/minggu); tidak ada libur nasional di rentang ini.
- Gaji Rp2.800.000: kedua sisi meminta pencocokan dengan UMK kota tanpa mengarang angka UMK ✅.

**strategi-konten-iklan** (Rp1.500.000/bulan, margin 40%, TikTok)
- ROAS impas = 1 ÷ 0,4 = **2,50x** ✅ (kedua sisi).
- TANPA: "tiap Rp1 … balik jadi Rp2.500" ❌ (seharusnya Rp2,50; atau Rp1.000 → Rp2.500). "±Rp50.000/hari" = 1.500.000 ÷ 30 ✅.
- DENGAN (asumsi AOV Rp100.000, disebut jelas): laba kotor **Rp40.000** ✅; CPA aman 70% × 40.000 = **Rp28.000** ✅; ROAS target 100.000 ÷ 28.000 = 3,571 → **3,58x** (dibulatkan ke atas, sama dengan 1 ÷ (0,4 × 0,7)) ✅; pesanan impas ⌈1.500.000 ÷ 40.000 = 37,5⌉ = **38**, omzet **Rp3.800.000** ✅; aman/uji = **Rp1.050.000 / Rp450.000** ✅; per minggu 300.000 + 600.000 + 300.000 + 300.000 = **Rp1.500.000** ✅.
- `alokasi_anggaran.py --anggaran 1500000 --momen 2026-10 --aov 100000 --margin 40% --kanal tiktok --bobot-minggu 1 2 1 1` dijalankan ulang: semua angka di atas identik; 10.10 jatuh di **minggu 2**; 10 Okt 2026 = **Sabtu** ✅; minggu terkecil 300.000 ÷ 7 = Rp42.857/hari ≥ Rp30.000 → maks. **1 iklan aktif** ✅.
- Catatan kecil: porsi 70% aman / 30% uji dan "cuma 1 iklan aktif" sedikit bertabrakan (uji dan aman tidak bisa jalan bersamaan); sebaiknya dijelaskan bergantian per minggu.

**laporan-status-kantor**
- 24 Des 2026 = **Kamis** (cuti bersama), 25 Des 2026 = **Jumat** (Natal), 1 Jan 2027 = **Jumat**, batas THR H-7 = 25 Des − 7 = **Jumat 18 Des 2026**; masuk kembali Senin 28 Des 2026 dan Senin 4 Jan 2027.
- DENGAN menyebut 25 Des 2026 dan 1 Jan 2027 tanpa nama hari ✅, tetapi tidak mencantumkan cuti bersama 24 Des maupun batas THR H-7, walau keduanya ada di `references/libur-nasional-2026.md` ❌. TANPA tidak menyebut tanggal sama sekali.
- Rumus THR DENGAN ("masa kerja ≥ 12 bulan = 1× gaji") ✅ (Permenaker 6/2016 Pasal 3 ayat (1) huruf a).

## Cek fakta aturan
- **Masa percobaan**: hanya PKWTT, maks. 3 bulan, upah tidak boleh di bawah upah minimum (UU 13/2003 Pasal 60 ayat (1)–(2) jo. UU 6/2023); PKWT tidak boleh mensyaratkan masa percobaan, bila disyaratkan batal demi hukum (PP 35/2021 Pasal 12) ([pasal.id PP 35/2021 Pasal 12](https://pasal.id/peraturan/pp/pp-no-35-tahun-2021/pasal-12); [wageindicator.org](https://wageindicator.org/id-id/bekerja-di-indonesia/hukum-tenaga-kerja/kontrak-dan-pemecatan/pkwtt/)). DENGAN menyebut semuanya dan menandai tanggal batas sebagai tafsir ✅. Pengecualian upah minimum usaha mikro/kecil (UU 6/2023 Pasal 90B) disebut DENGAN; sudah ditandai PERLU REVIEW di skrip skill.
- **BPJS Ketenagakerjaan "paling lambat 30 hari sejak mulai kerja"** (DENGAN) ✅ ([hukumonline.com](https://www.hukumonline.com/klinik/a/wajibkah-pengusaha-mendaftarkan-pekerjanya-di-bpjs-kesehatan-dan-ketenagakerjaan-lt5bec1c6a0aba6/); [PP 44/2015](https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104557_PP%2044%20Tahun%202015.pdf)); sanksi administratif PP 86/2013.
- **Klaim pelangsing**:
  - PerBPOM 1/2022 **Pasal 28 huruf g**: label/iklan pangan olahan dilarang memuat klaim dapat mencegah, mengobati, atau menyembuhkan penyakit ([pasal.id](https://pasal.id/peraturan/perban/peraturan-bpom-no-1-tahun-2022)) ✅.
  - PerBPOM 34/2022 (iklan obat tradisional/suplemen wajib persetujuan BPOM) dan PerBPOM 25/2023 (registrasi obat bahan alam), sesuai rujukan skill `references/kepatuhan-klaim-iklan.md` ✅.
  - UU 8/1999: **Pasal 17 ayat (1) ditujukan ke "pelaku usaha periklanan"** ([pasal.id](https://pasal.id/peraturan/uu/uu-no-8-tahun-1999/pasal-17)); untuk penjual, Pasal 9 ayat (1) lebih tepat. DENGAN hanya menyebut Pasal 17 ⚠️ (kecil, sama dengan catatan g8/g9).
- **Kebijakan iklan TikTok (Weight Management)** ([ads.tiktok.com](https://ads.tiktok.com/help/article/tiktok-ads-policy-weight-management)): klaim penurunan berat badan hanya untuk audiens **18+**; dilarang klaim produk saja (tanpa diet/olahraga) menurunkan berat badan, menyiratkan hasil mudah/dijamin, atau penurunan tidak realistis. TANPA menyebut risiko penolakan iklan TikTok ✅ tetapi menyarankan "UGC/testimoni" ⚠️ (rawan klaim hasil). DENGAN tidak menyebut kebijakan TikTok sama sekali, termasuk batas 18+ ⚠️, padahal ada di rujukan skill. (Catatan: larangan foto sebelum-sesudah yang ditulis pengirim tidak ditemukan pada teks halaman kebijakan yang dibaca penilai; tidak dipakai sebagai dasar.)
- **THR**: Permenaker 6/2016 Pasal 5: THR diberikan sekali setahun **sesuai hari raya keagamaan masing-masing pekerja** (kecuali disepakati lain) dan dibayar paling lambat 7 hari sebelum hari raya ([llg-bwi.org, teks Permenaker 6/2016](https://llg-bwi.org/file_publish/Permenaker%20Nomor%206%20Tahun%202016.pdf); [pasal.id](https://pasal.id/peraturan/permen/permenaker-no-6-tahun-2016)). **Temuan baru penilai:** DENGAN menawarkan "hitung THR 20 karyawan" untuk Natal, dan TANPA menulis "info umum THR … akan ditransfer"; tidak ada yang menyebut bahwa THR Natal umumnya hanya untuk karyawan yang merayakan Natal (yang lain menerima di hari rayanya sendiri).
- **Privasi gaji**: UU 27/2022 PDP; data keuangan pribadi termasuk data spesifik. DENGAN menyebut "masalah hukum ketenagakerjaan soal kerahasiaan upah" ⚠️: tidak ada aturan ketenagakerjaan umum yang mewajibkan kerahasiaan upah; dasar yang tepat UU PDP.
- **Libur**: SKB 3 Menteri No. 1497, 2, 5 Tahun 2025 (2026: Natal Jumat 25 Des, cuti bersama Kamis 24 Des) ([setneg.go.id](https://setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026)); SKB No. 1205, 3, 5 Tahun 2026 (ditandatangani 15 Sep 2026) untuk 2027: 1 Jan 2027 Tahun Baru ([setneg.go.id](https://setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2027); [detik.com](https://www.detik.com/sulsel/berita/d-8671318/skb-3-menteri-cuti-bersama-2027-ini-daftar-lengkap-dan-link-pdf-nya)).

## Cacat / temuan
1. **laporan-status-kantor DENGAN: lagi-lagi tidak ada teks pengumuman** (gagal kedua kali di bot produksi, g9 dan g10).
   - SKILL.md 1.0.7 sudah mewajibkan teks lengkap di balasan pertama, tanggal dari `references/` dicantumkan (bukan ditanyakan), dua blok tetap (TEKS GRUP / REKAP PRIBADI), dan larangan kata "file"; bot melanggar keempatnya.
   - Dugaan (pengirim, disetujui penilai sebagai hipotesis): bot produksi memuat ±120 skill (termasuk `hitung-thr`, `gaji-umkm`, `slip-gaji-bpjs`); permintaan "nominal THR tiap karyawan" menarik model ke alur hitung THR. Pra-cek `uji-tg.sh` dengan satu skill tidak menangkap ini.
   - Menawarkan hitung THR 20 karyawan untuk Natal tanpa catatan agama (lihat Cek fakta) dan "PPh 21 kalau perlu" (menggeser fokus).
   - Dasar "kerahasiaan upah" kurang tepat (seharusnya UU PDP).
2. **laporan-status-kantor TANPA**: menolak nominal di grup dan menyarankan japri dengan benar, tetapi tidak menulis teks apa pun dan menanyakan tanggal libur.
3. **sop-onboarding DENGAN**:
   - Tabel Markdown 6 kolom tampil sebagai teks berpipa di Telegram; di ponsel sulit dibaca (alasan utama skor 8, bukan 8,5).
   - Baris evaluasi keputusan (6 Jan) diletakkan setelah batas hukum (11 Jan); pembaca awam bisa salah urut.
   - Kata "skill" bocor ("tafsir skill ini"); pecahan pesan memisahkan judul "5. Catatan Aturan" dari isinya.
   - Pesan sambutan WA tidak ada (ditawarkan sebagai lanjutan; sesuai aturan).
4. **sop-onboarding TANPA**: tanggal evaluasi akhir 12 Jan 2027 melewati batas; hari kerja prorata salah; SOP kasir hanya daftar topik pelatihan, bukan langkah kerja. BPJS dan cek UMK benar; tidak menyebut bahwa upah masa percobaan tidak boleh di bawah UMK sebagai aturan masa percobaan (hanya cek UMK umum).
5. **strategi-konten-iklan DENGAN**:
   - AOV diasumsikan Rp100.000 (disebut jelas sebagai asumsi dan diminta koreksi), tetapi SKILL.md menganjurkan `[isian: AOV]`; angka 38 pesanan bisa terbaca sebagai fakta.
   - Tidak menyebut kebijakan iklan TikTok produk berat badan (18+, tanpa janji hasil mudah/dijamin).
   - UU 8/1999 hanya dirujuk ke Pasal 17 (Pasal 9 lebih tepat untuk penjual).
   - Porsi aman/uji 70/30 vs "1 iklan aktif" perlu penjelasan urutan.
   - Campur "aku"/"saya" (kecil). Tidak ada kata proses ✅. Pertanyaan maks. 3 di akhir ✅.
6. **strategi-konten-iklan TANPA**: salah satuan "Rp2.500 per Rp1"; patokan ROAS "3–5x" tanpa sumber; menyarankan "testimoni"; tidak ada pembagian per minggu dalam Rupiah; tagline "bantu jaga … metabolisme" masih klaim fungsi yang harus sesuai izin edar.
7. Tidak ada pesan sistem OpenClaw (heartbeat) yang bocor di topik g10.

## Kesimpulan
- **strategi-konten-iklan 1.0.6** (6 → 8,5; +2,5): **LULUS** di bot asli, layak tampil. Perbaikan kecil: sebut kebijakan TikTok/Meta untuk produk berat badan (18+, tanpa janji hasil), tulis `[isian: AOV]` di samping contoh angka, rujuk UU 8/1999 Pasal 9.
- **sop-onboarding 1.0.5** (6,5 → 8; +1,5): **LULUS**, tetapi tepat di kedua batas acuan. Layak tampil; sebelum gelombang/promosi berikutnya sebaiknya di kanal chat ganti tabel 6 kolom dengan daftar bertanggal berurutan (evaluasi keputusan sebelum batas hukum) dan hapus frasa "tafsir skill ini". Tanpa perbaikan itu, uji ulang berikutnya berisiko jatuh di bawah acuan.
- **laporan-status-kantor 1.0.7** (4,5 → 5; +0,5): **BELUM**, jangan ditampilkan. Sesuai keputusan pemilik 2026-10-03, skill di bawah acuan setelah perbaikan **tidak diiterasi lagi**; usulan status (tetap di bundle tanpa promosi seperti 12 skill lain, atau arsip) menunggu keputusan pemilik karena skill ini ada di `paket-kantor`, `paket-kantor-manajemen`, `paket-klinik`, dan panduan solusi-vip. Temuan proses: pra-cek `uji-tg.sh` dengan satu skill tidak mewakili bot produksi berisi ±120 skill; pertimbangkan pra-cek dengan set skill produksi untuk permintaan yang bisa memicu skill lain. Bila suatu saat dirawat: tambahkan catatan bahwa THR Natal hanya untuk karyawan yang merayakan.
