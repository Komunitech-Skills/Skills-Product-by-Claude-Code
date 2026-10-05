# Telegram gelombang 10 — 3 skill (2026-10-05)

Persetujuan pemilik: keputusan no. 17. Data di pesan uji fiktif. Nama dan nomor tidak disalin ke laporan ini.

> **Catatan independensi:** di sesi ini alat untuk memanggil agent penilai terpisah tidak tersedia, sehingga penilaian dilakukan oleh agent yang juga menjalankan pengiriman (bukan pembuat skill). Penilai hanya memakai pesan uji, jawaban bot, pra-cek internal, isi folder skill untuk cek fakta, dan sumber web. Semua angka dihitung ulang dengan python. Bila perlu, skor dapat dinilai ulang oleh agent independen dari `scratchpad/pilot/jawaban-g10-tg.txt`.

## Cara
- 6 topik di grup uji (865–870): topik ganjil = `TANPA skill` (setelan `skills: []` per topik di `openclaw.json`, hot reload), topik genap = `DENGAN skill`.
- Sebelum kirim, skill di bot produksi disinkronkan ke versi repo (backup `scratchpad/openclaw-real/skills-backup-20261005-g10`; config dibackup `openclaw.json.before-gelombang10-*`). laporan-status-kantor sudah sama; sop-onboarding dan strategi-konten-iklan diperbarui.
- Bot penguji mengirim 6 pesan (1 per sisi per skill), identik untuk kedua sisi (`scratchpad/pilot/msgs-g10.json`, teks dari `teks-g9.json`), berurutan dengan jeda, tanpa balas-otomatis. Semua 6 terkirim (`ok: True`, 18:16–18:25 UTC).
- Jawaban diambil dari Telegram (`scratchpad/pilot/jawaban-g10-tg.txt`). Tidak ada timeout. Balasan sop-onboarding DENGAN terpecah menjadi 3 pesan Telegram (utuh, tidak terpotong).
- Versi yang diuji (catalog.csv): sop-onboarding **1.0.5**, strategi-konten-iklan **1.0.6**, laporan-status-kantor **1.0.7**.
- Pembanding internal: `koordinasi/pracek-telegram-g9-2026-10-05.md` (versi 1.0.4: sop-onboarding 5 dan strategi-konten-iklan 6,5 di konteks Telegram karena hanya bertanya; laporan-status-kantor 8,5), uji ulang konteks Telegram di `examples/00-openclaw-sebelum-sesudah.md` masing-masing skill (sop-onboarding 1.0.5 LULUS, strategi-konten-iklan 1.0.6 LULUS rata-rata 8,25, laporan-status-kantor 1.0.7 LULUS rata-rata 8,5), dan gelombang 9 (laporan-status-kantor 1.0.5: 5 → 6).
- Skor 1–10 per sisi menimbang ketepatan, siap pakai, aturan Indonesia, keamanan/etika (klaim pelangsing, janji ROAS, privasi gaji/THR), dan kejelasan di Telegram.

## Hasil

| Skill | TANPA | DENGAN | Selisih | Pembeda (satu kalimat) |
|---|---|---|---|---|
| sop-onboarding | 6,5 | 8,5 | +2 | DENGAN langsung memberi paket utuh dengan jadwal yang tepat (checkpoint 10 Nov/10 Des/9 Jan, batas masa percobaan 11 Jan 2027, evaluasi keputusan Rabu 6 Jan 2027), SOP kasir, checklist BPJS, dan cek UMK; TANPA menulis evaluasi "paling lambat 12 Jan 2027" (melewati batas 3 bulan yang ia tulis sendiri, 11 Jan) dan "~20 hari kerja" untuk 12–31 Okt (seharusnya 18 hari kerja bila 6 hari/minggu). |
| strategi-konten-iklan | 6 | 8,5 | +2,5 | DENGAN menolak "turun 5kg seminggu" dengan dasar yang tepat (UU 8/1999, PerBPOM 1/2022 untuk pangan olahan vs PerBPOM 34/2022 untuk obat tradisional/suplemen, cek kategori di cekbpom), memberi ROAS impas 2,5x, target aman 3,58x, dan anggaran per minggu Rp300rb/600rb/300rb/300rb yang naik di minggu 10.10; TANPA memberi ROAS impas benar tetapi salah menjelaskan ("Rp1 iklan harus balik jadi Rp2.500"), memberi patokan "3–5x" tanpa sumber, dan menyarankan video "testimoni" untuk produk pelangsing. |
| laporan-status-kantor | 4,5 | 5 | +0,5 | Kedua sisi menolak nominal THR per orang di grup dengan benar, tetapi **keduanya tidak memberi teks pengumuman**; DENGAN menyebut 25 Des 2026 dan 1 Jan 2027 serta rumus THR, namun tetap menanyakan tanggal cuti bersama yang sudah ada di rujukan skill. |

Rata-rata 3 pasang: TANPA 5,7 → DENGAN 7,3 (selisih +1,7).

Memenuhi acuan (DENGAN ≥ 8 **dan** selisih ≥ 1,5): **strategi-konten-iklan** (8,5; +2,5) dan **sop-onboarding** (8,5; +2). Tidak memenuhi: **laporan-status-kantor** (5 < 8; selisih +0,5 < 1,5).

Dibanding pra-cek g9 (versi 1.0.4): sop-onboarding naik 5 → 8,5 dan strategi-konten-iklan naik 6,5 → 8,5. Perbaikan "kerjakan dulu, tanya di akhir" terbukti di bot produksi untuk dua skill ini. laporan-status-kantor gagal untuk kedua kalinya di bot produksi (g9 1.0.5: 6; g10 1.0.7: 5) padahal uji ulang konteks Telegram 1.0.7 di alat uji lulus 3/3 dengan teks utuh.

## Verifikasi angka (python, penilai)

**sop-onboarding** (mulai Senin 12 Okt 2026, PKWTT, percobaan 3 bulan)
- 12 Okt 2026 = **Senin** ✅ (kedua sisi).
- Hasil `scripts/jadwal_onboarding.py --mulai "12 Oktober 2026" --hari-kerja 6 --jenis pkwtt` dijalankan ulang oleh penilai: akhir minggu 1 18 Okt (Minggu) → 19 Okt; checkpoint +29/+59/+89 hari = **10 Nov 2026 / 10 Des 2026 / 9 Jan 2027**; batas hukum **11 Jan 2027 (Senin)**; evaluasi keputusan **6 Jan 2027 (Rabu)** = 5 hari kerja mundur (11, 9, 8, 7, 6 Jan; Minggu 10 Jan dilewati). Tabel DENGAN **identik** ✅.
- Dengan 5 hari kerja/minggu, evaluasi keputusan menjadi 4 Jan 2027; DENGAN menyebut asumsi 6 hari dan menawarkan hitung ulang ✅.
- TANPA: masa percobaan "12 Okt 2026 s/d 11 Jan 2027" ✅, tetapi "Evaluasi akhir … paling lambat 12 Jan 2027" ❌ (melewati batas 3 bulan) dan "Akhir bulan 3 (11 Jan 2027): evaluasi final" ⚠️ (keputusan di hari terakhir, tidak ada waktu proses). "12–31 Okt = ~20 hari kerja" ❌: 20 hari kalender; hari kerja = **18** (6 hari/minggu) atau **15** (5 hari/minggu).
- Gaji Rp2.800.000: kedua sisi meminta mencocokkan dengan UMK kota, tanpa mengarang angka UMK ✅.

**strategi-konten-iklan** (anggaran Rp1.500.000, margin 40%, TikTok)
- ROAS impas = 1 ÷ 0,4 = **2,50x** ✅ (kedua sisi).
- TANPA: "tiap Rp1 belanja iklan minimal harus balik jadi Rp2.500" ❌ (seharusnya Rp2,50; atau Rp1.000 iklan → Rp2.500 penjualan). "±Rp50.000/hari" ≈ 1.500.000 ÷ 30 ✅.
- DENGAN (dengan asumsi AOV Rp100.000 yang disebut jelas): laba kotor 40% × 100.000 = **Rp40.000** ✅; CPA aman 70% × 40.000 = **Rp28.000** ✅; ROAS target 100.000 ÷ 28.000 = 3,571 → **3,58x** (dibulatkan ke atas sesuai aturan skill) ✅; pesanan impas ⌈1.500.000 ÷ 40.000⌉ = **38**, omzet Rp3.800.000 ✅; aman/uji 70/30 = **Rp1.050.000 / Rp450.000** ✅; per minggu 300.000 + 600.000 + 300.000 + 300.000 = **Rp1.500.000** ✅ (sama dengan `alokasi_anggaran.py … --bobot-minggu 1 2 1 1`, dan `--momen 2026-10` menempatkan 10.10 di minggu 2) ✅; minggu terkecil 300.000 ÷ 7 = Rp42.857/hari ≥ Rp30.000 → maks. **1 iklan aktif** ✅.
- 10 Okt 2026 = Sabtu (tanggal kembar 10.10) ✅.

**laporan-status-kantor**
- 25 Des 2026 = **Jumat**, 24 Des 2026 = **Kamis** (cuti bersama), 1 Jan 2027 = **Jumat**, batas THR H-7 = **Jumat 18 Des 2026**.
- DENGAN menyebut 25 Des 2026 dan 1 Jan 2027 tanpa nama hari ✅, tetapi tidak mencantumkan cuti bersama 24 Des maupun batas THR H-7, walau keduanya ada di `references/libur-nasional-2026.md` ❌. TANPA tidak menyebut tanggal sama sekali.
- Rumus THR di DENGAN ("masa kerja ≥ 12 bulan = 1× gaji") ✅ (Permenaker 6/2016 Pasal 3 ayat (1) huruf a).

## Cek fakta aturan
- **Masa percobaan**: hanya untuk PKWTT, maks. 3 bulan (UU 13/2003 Pasal 60 ayat (1); PKWT dilarang masa percobaan, PP 35/2021 Pasal 12); upah masa percobaan tidak boleh di bawah upah minimum (Pasal 60 ayat (2)). DENGAN menyebut semuanya dan menandai tafsir tanggal batas sebagai bukan kepastian hukum ✅. Rujukan skill: `skills/sop-onboarding/references/dasar-hukum-onboarding.md`.
- **BPJS Ketenagakerjaan "paling lambat 30 hari sejak mulai kerja"** (DENGAN): sesuai praktik pendaftaran BPJS Ketenagakerjaan dan aturan bahwa pemberi kerja wajib mendaftarkan pekerja paling lambat 30 hari sejak mempekerjakan ([hukumonline.com](https://www.hukumonline.com/klinik/a/wajibkah-pengusaha-mendaftarkan-pekerjanya-di-bpjs-kesehatan-dan-ketenagakerjaan-lt5bec1c6a0aba6/); [PP 44/2015, bpjsketenagakerjaan.go.id](https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104557_PP%2044%20Tahun%202015.pdf)) ✅. Sanksi administratif: PP 86/2013.
- **Klaim pelangsing**: UU 8/1999 Pasal 9 ayat (1) dan Pasal 17 ayat (1); PerBPOM 1/2022 Pasal 28 (pangan olahan dilarang klaim mencegah/mengobati); PerBPOM 34/2022 (iklan obat tradisional/suplemen wajib persetujuan BPOM). Rujukan skill `references/kepatuhan-klaim-iklan.md` (sumber pasal.id, peraturan.bpk.go.id). DENGAN tepat ✅; catatan kecil: Pasal 17 ditujukan terutama ke pelaku usaha periklanan, Pasal 9 lebih tepat untuk penjual (sama dengan catatan g8/g9).
- **Kebijakan iklan TikTok (manajemen berat badan)**: TikTok melarang klaim penurunan berat badan yang cepat/dijamin/berangka dan gambar sebelum-sesudah, serta membatasi iklan produk berat badan untuk usia 18+ ([TikTok Ads Policy: Weight Management](https://ads.tiktok.com/help/article/tiktok-ads-policy-weight-management)). TANPA menyebut risiko penolakan iklan TikTok ✅ tetapi menyarankan "UGC/testimoni" untuk produk pelangsing ⚠️. DENGAN tidak menyebut kebijakan TikTok sama sekali (hanya aturan BPOM/UU) ⚠️, dan tidak menyebut batas usia 18+.
- **THR**: Permenaker 6/2016 Pasal 5 ayat (4): dibayar paling lambat 7 hari sebelum hari raya keagamaan (dicek di g9). **Privasi**: UU 27/2022 PDP; data keuangan pribadi termasuk data spesifik (dicek di g9). DENGAN menyebut "masalah hukum ketenagakerjaan soal kerahasiaan upah" ⚠️: tidak ada aturan ketenagakerjaan umum yang mewajibkan kerahasiaan upah; dasar yang tepat adalah UU PDP.
- **Libur 2026**: SKB 3 Menteri No. 1497, 2, 5 Tahun 2025 (Natal Jumat 25 Des, cuti bersama Kamis 24 Des) — dicek di g9 ([setneg.go.id](https://setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026)).

## Cacat / temuan
1. **laporan-status-kantor DENGAN: lagi-lagi tidak ada teks pengumuman** (gagal kedua kali di bot produksi, g9 dan g10).
   - SKILL.md 1.0.7 sudah mewajibkan "langsung tulis teks lengkapnya di balasan pertama" dan "tanggal dari `references/` dicantumkan, bukan ditanyakan"; bot tetap bertanya tanggal cuti bersama dan menunda teks.
   - Pra-cek konteks Telegram 1.0.7 (`uji-tg.sh`, home berisi skill ini saja) lulus 3/3. Bot produksi memuat ±120 skill (termasuk `hitung-thr`, `gaji-umkm`, `slip-gaji-bpjs`); dugaan kuat permintaan "nominal THR tiap karyawan" membuat model berpindah ke alur hitung THR dan mengabaikan aturan laporan-status-kantor. Pra-cek dengan satu skill tidak menangkap ini.
   - Menawarkan menghitung THR 20 karyawan + "PPh 21 kalau perlu" (boleh karena `hitung-thr` terpasang di bot, tetapi menggeser fokus dari pengumuman).
   - Kata proses: "file CSV/Excel".
   - Klaim "masalah hukum ketenagakerjaan soal kerahasiaan upah" kurang tepat (dasar yang benar UU PDP).
2. **laporan-status-kantor TANPA**: menolak nominal di grup dengan benar dan menyarankan japri, tetapi tidak menulis teks apa pun dan menanyakan tanggal libur.
3. **sop-onboarding DENGAN** (cacat kecil):
   - Tabel Markdown 6 kolom tampil sebagai teks berpipa di Telegram, sulit dibaca di ponsel.
   - Kata "skill" bocor: "Tanggal batas 3 bulan di atas adalah tafsir skill ini".
   - Balasan panjang terpecah 3 pesan; "5. Catatan Aturan" terpisah dari isinya.
   - Tidak ada pesan sambutan WA (ditawarkan sebagai lanjutan; sesuai aturan "bagian lain ditawarkan").
4. **sop-onboarding TANPA**: tanggal evaluasi akhir 12 Jan 2027 melewati batas yang ia tulis sendiri; hitungan hari kerja prorata salah; tidak ada SOP kasir yang konkret per langkah. BPJS wajib dan cek UMK sudah benar.
5. **strategi-konten-iklan DENGAN** (cacat kecil):
   - AOV diasumsikan Rp100.000 lalu dipakai untuk CPA dan 38 pesanan; disebut jelas sebagai asumsi dan diminta koreksi, tetapi SKILL.md menganjurkan `[isian: AOV]`. Angka 38 pesanan bisa terbaca sebagai fakta.
   - Tidak menyebut kebijakan iklan TikTok untuk produk berat badan (batas usia 18+, larangan sebelum-sesudah).
   - UU 8/1999 dirujuk ke Pasal 17 saja (Pasal 9 lebih tepat).
   - Tidak ada kata proses ("script"/"file") ✅. Pertanyaan maks. 3 di akhir ✅.
6. **strategi-konten-iklan TANPA**: salah satuan "Rp2.500 per Rp1"; patokan ROAS "3–5x" tanpa sumber; menyarankan konten "testimoni" untuk produk pelangsing; tidak ada pembagian anggaran per minggu dalam Rupiah; tagline "bantu jaga … metabolisme" masih klaim fungsi yang perlu sesuai izin edar.
7. Tidak ada pesan sistem OpenClaw (heartbeat) yang bocor di topik g10.

## Kesimpulan
- **strategi-konten-iklan 1.0.6** (6 → 8,5; +2,5): **LULUS** di bot asli. Layak tampil. Perbaikan kecil: catatan kebijakan TikTok/Meta untuk produk berat badan (18+, tanpa sebelum-sesudah), dan saat AOV kosong tulis `[isian: AOV]` di samping contoh angka.
- **sop-onboarding 1.0.5** (6,5 → 8,5; +2): **LULUS** di bot asli. Layak tampil. Perbaikan kecil: di kanal chat ganti tabel 6 kolom dengan daftar bertanggal, dan hapus frasa "tafsir skill ini".
- **laporan-status-kantor 1.0.7** (4,5 → 5; +0,5): **BELUM**, jangan ditampilkan. Gagal dua kali berturut-turut di bot produksi. Sesuai keputusan pemilik 2026-10-03, skill di bawah acuan setelah perbaikan **tidak diiterasi lagi**; usulan status (tetap di bundle tanpa promosi seperti 12 skill lain, atau arsip) menunggu keputusan pemilik karena skill ini ada di `paket-kantor`, `paket-kantor-manajemen`, `paket-klinik`, dan panduan solusi-vip. Temuan proses: pra-cek `uji-tg.sh` dengan satu skill tidak mewakili bot produksi berisi ±120 skill; pertimbangkan pra-cek dengan set skill produksi untuk permintaan yang bisa memicu skill lain.
