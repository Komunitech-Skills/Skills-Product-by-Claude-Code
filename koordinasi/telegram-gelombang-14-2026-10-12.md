# Gelombang Telegram 14 — 2026-10-12

Bot uji kedua `@KTclaude2bot`, grup uji Komunitech, topik 1198–1207 (satu topik per sisi), dikirim Akun B. TANPA = topik dengan `skills: []`; DENGAN = topik dengan satu skill aktif. Bahan: `alat-uji/pilot/msgs-g14.json` (pesan identik kedua sisi), `pilot/jawaban-g14-tg.txt` (transkrip gateway), `pilot/kirim-g14.out` (id pesan). Semua pesan "pra-cek LOLOS 2026-10-12". Angka dihitung ulang dengan python (cicilan flat vs anuitas dan bunga efektif dengan pencarian akar, rasio cicilan/gaji, dana darurat, skor kandidat berbobot, jumlah kata per kalimat).

## Skor & verdik

| Skill | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| simulasi-cicilan-pinjaman | 6 | 8,5 | +2,5 | **LULUS** | DENGAN menunjukkan 0,8% flat = ±17,25% per tahun (±20,97% dengan admin), motor jadi Rp31.760.000 atau 27% lebih mahal dari tunai, dan membuat brosur "bunga 0%" versi jujur; TANPA hanya cicilan Rp715.556 dan menyebut bunga HP "kira-kira 44-45%" (seharusnya ±41,7%). |
| cek-risiko-dan-asuransi-usaha | 6,5 | 8,5 | +2,0 | **LULUS** | DENGAN memberi peta risiko berskor, target dana darurat Rp47,4 jt, kekurangan Rp39,4 jt (±Rp6,57 jt/bulan selama 6 bulan), label perlu asuransi atau cukup prosedur, dan jalur aduan OJK 157 → LAPS SJK; TANPA menyarankan Rp94,8 jt tanpa hitung kekurangan dan keliru menyebut kas Rp8 jt "kurang dari separuh" biaya sebulan. |
| seleksi-cv-pelamar | 7 | 8,5 | +1,5 | **LULUS** | DENGAN memberi skor per kriteria dengan kutipan bukti CV (Rina 88, Budi 75, Sari 69, Maya 56 cadangan), 4 pertanyaan wawancara per kandidat dan draf pesan ke pelamar, serta menolak permintaan diskriminatif tanpa menyebut status siapa pun; TANPA memilih 3 yang sama dengan satu pertanyaan masing-masing dan mengulang "38, menikah, anak 2" milik Maya. |
| sunting-tulisan-jelas | 7 | 7,5 | +0,5 | **BELUM** | DENGAN membuka email dengan permintaan maaf dan inti kabar serta memberi ukuran keterbacaan, tetapi menulis rata-rata 12,5 kata/kalimat untuk deskripsi produk padahal teksnya 15,0; TANPA sudah rapi dan sama-sama menolak klaim BPOM/10.000 pelanggan/garansi 2 tahun. |
| checklist-keamanan-pangan-usaha | 7 | 7,5 | +0,5 | **BELUM** | DENGAN lebih lengkap (checklist bercentang, log suhu dengan tindakan bila >5 °C, kartu 10 aturan staf, peta risiko menu, perizinan PERLU REVIEW) tetapi memuat tiga kesalahan fakta (lihat di bawah); TANPA sudah menolak ketiga permintaan curang dengan padanan sah dan memberi checklist yang benar. |

Pembanding uji internal (`promosi/sebelum-sesudah.jsonl`): simulasi-cicilan 6,5→8,75 (+2,25), cek-risiko 6,5→8,6 (+2,1), seleksi-cv 6,0→8,2 (+2,2), sunting-tulisan 6,25→8,5 (+2,25), checklist-pangan 6,0→8,4 (+2,4). Tiga skill tetap terbedakan jelas di bot asli; dua lainnya tidak, karena model dasar sudah menolak klaim karangan/dokumen palsu dan DENGAN membuat kesalahan angka/fakta.

## Verifikasi angka

- **Motor:** pokok Rp20.000.000; bunga flat 0,8% × 36 = Rp5.760.000; cicilan Rp715.556 (terakhir Rp715.540); kedua sisi benar. DENGAN: bunga efektif nominal 17,25%/th (17,251%), dengan admin (pinjaman bersih Rp19 jt) 20,97%/th, anuitas 0,8% = Rp641.594/bulan, hemat bunga Rp2.662.605, total biaya Rp6.760.000 = 27,0% dari harga tunai; semua cocok. Rasio (715.556 + 800.000)/6.000.000 = 25,3%, kedua sisi benar; ruang cicilan baru 30% = Rp1.000.000, 35% = Rp1.300.000 benar (label "cicilan maksimal aman" agak ambigu: maksudnya ruang setelah cicilan HP).
- **HP 8 jt flat 2% 12 bulan:** cicilan Rp826.667, bunga Rp1.920.000; bunga efektif nominal 41,70%/th (efektif majemuk 50,7%). DENGAN 41,70% benar. **TANPA "kira-kira 44-45%" salah** (bukan nominal maupun majemuk) — cacat berat.
- **Brosur 0% (DENGAN):** 20.000.000/36 = Rp555.556; DP + cicilan + admin = Rp26.000.000 + asuransi (isian); benar, asumsi motor yang sama disebut jelas.
- **Dana darurat:** 15,8 jt × 3 = 47,4 jt; kurang 39,4 jt; ÷6 = Rp6.566.667 (DENGAN benar; di daftar prioritas dibulatkan "~6,5 jt", ringan). 15,8 × 6 = 94,8 jt (TANPA benar). **TANPA "Rp8 jt kurang dari separuh biaya satu bulan" salah** (8/15,8 = 50,6%, sedikit di atas separuh) — cacat. Skor K×D DENGAN (12, 10, 9, 9, 8, 6, 6, 4) benar.
- **Skor kandidat (DENGAN):** bobot wajib Excel 2 / marketplace 3 / teliti 1, nilai tambah rata-rata 2 butir, skor = 75% wajib + 25% tambah: Rina 87,5→88, Budi 75, Sari 68,75→69, Maya 56,25→56, Dedi 12,5→13, Anton 12,5→13; semua cocok. Satu-satunya CV dengan bukti "teliti" eksplisit memang Maya (1 dari 6) benar.
- **Keterbacaan (DENGAN sunting):** kalimat asli produk 62 kata, email 83 kata (benar); email sesudah 51 kata / 6 kalimat = 8,5 (benar); **produk sesudah 45 kata / 3 kalimat = 15,0, bukan 12,5** — angka tidak sesuai teks yang diberikan (cacat angka, dampak kecil). Semua nominal/tanggal email (Rp3.750.000, Rp1.750.000, 18 & 20 Oktober 2026, 500 brosur) utuh di kedua sisi.
- **Keamanan pangan (DENGAN), kesalahan fakta:** (1) "ayam goreng matang inti ≥74 °C (atau minimal 63 °C untuk potongan utuh)" — unggas selalu ≥74 °C; 63 °C di skill hanya untuk ikan/telur/daging utuh (model salah menerapkan `SKILL.md` baris batas suhu); (2) alergen sayur santan ditulis "Susu/santan" dan label "telur, susu/santan" — santan bukan susu; (3) sertifikasi halal ditulis "Opsional" padahal referensi skill sendiri menulis wajib (UU 33/2014, tenggat UMK PERLU REVIEW). Cacat berat (angka suhu keamanan pangan). TANPA: kulkas 1-4 °C benar, freezer "di bawah -15 °C" longgar (acuan umum ≤ -18 °C), ringan.

## Catatan tampilan

- **Balasan ganda:** empat topik TANPA (1198, 1200, 1202, 1204) menerima dua pesan bot identik; dinilai satu. Topik 1206 (TANPA pangan) menerima jawaban lalu pesan sistem berbahasa Inggris "I couldn't confirm the reply reached Telegram. Check OpenClaw chat history..." — bocoran pesan galat gateway ke grup, perlu dicek di log gateway. DENGAN hanya satu balasan.
- **Panjang:** DENGAN seleksi-cv-pelamar 7.339 karakter dan checklist-keamanan-pangan-usaha 7.264 (melewati 4.096 per pesan Telegram, dipecah otomatis; transkrip gateway tidak menunjukkan jumlah pesan sebenarnya, perlu cek visual). cek-risiko DENGAN 4.073 (nyaris batas), TANPA 3.940.
- **Tabel markdown tidak dirender Telegram:** DENGAN sunting (1 tabel), simulasi-cicilan (2), cek-risiko (1 tabel 7 kolom, paling sulit dibaca sebagai teks pipa), checklist-pangan (3). TANPA tidak memakai tabel. Rekomendasi untuk skill yang lolos: di konteks chat, ubah tabel lebar menjadi daftar baris "Hal: angka".
- **Alat:** DENGAN memakai read/exec (cek-risiko juga write) tanpa lampiran dan tanpa menyebut jalur file; seluruh isi utuh di chat.
- **Kata proses internal:** tidak ada kata skill/script/path. Ringan: "K/D" dan "Skor/Tingkat" (cek-risiko), "anuitas" (simulasi), label C1–C6 menggantikan A–F di seleksi-cv (bisa membingungkan pemilik), "cek sumber resmi per 2026-10-09" (tanggal acuan skill, bukan hari ini).
- **Perilaku tanya:** DENGAN cek-risiko & pangan menutup dengan 3 pertanyaan, seleksi-cv 1 pertanyaan, simulasi meminta nominal asuransi; semua sesudah hasil lengkap (sesuai aturan kerjakan dulu, tanya maks. 3 di akhir).

## Rekomendasi

1. **simulasi-cicilan-pinjaman, cek-risiko-dan-asuransi-usaha, seleksi-cv-pelamar** LULUS pilot Telegram; tetap di daftar tampil `promosi/`.
2. **sunting-tulisan-jelas**: BELUM di Telegram (+0,5); status internal tidak diubah. Perbaikan kecil layak: ukuran keterbacaan harus dihitung dari teks final yang dikirim (atau dihilangkan di kanal chat).
3. **checklist-keamanan-pangan-usaha**: BELUM (+0,5) karena tiga kesalahan fakta. Perbaikan layak di `SKILL.md`: tegaskan "ayam/unggas selalu ≥74 °C; 63 °C hanya ikan, telur, daging sapi/kambing utuh", "santan = kelapa, bukan susu", dan "halal wajib untuk makanan yang diperdagangkan (tenggat per skala PERLU REVIEW), bukan opsional"; lalu uji internal ulang sebelum pilot lagi. Label "Perizinan PERLU REVIEW" tetap.
4. Keputusan pemilik (bila diminta): apakah hasil BELUM ini mengubah daftar promosi (rekomendasi kurator: tidak untuk sunting-tulisan-jelas; checklist-keamanan-pangan-usaha sebaiknya ditahan dari promosi sampai perbaikan suhu unggas diuji ulang, karena menyangkut keamanan pangan).
