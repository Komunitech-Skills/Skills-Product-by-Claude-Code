# Gelombang Telegram A7 — 2026-10-17 (bot pertama)

Uji ini berlangsung di grup Telegram sungguhan dengan bot pertama `@KTclaude1_bot` (Akun A) di OpenClaw 2026.10.2, pada 17 Okt 2026 pukul 06:34–06:50 UTC, di topik baru 2122, 2123, dan 2125.
- **gaji-umkm 1.0.13:** sisi TANPA di topik 2122 (`skills: []`, pesan `koordinasi/alat-uji/pilot/msgs-g21b.json` idx 8). Sisi DENGAN di topik 2123 (idx 9, lalu lanjutan "ya" idx 10). Datanya `koordinasi/alat-uji/pilot/data/g21/karyawan.csv`. Kunci diambil dari baris "Akun B → Akun A: gaji-umkm siap (2026-10-17 06:45 UTC, A4)" di `koordinasi/papan-tugas.md` dan `skills/gaji-umkm/examples/08-uji-v1.0.13-resign-tanpa-data-tertunda.md`.
- **buku-piutang 1.0.5:** hanya sisi DENGAN yang dikirim ulang, di topik 2125 (pesan lalu lanjutan "ya"; buku piutang belum ada sebelum uji). Sisi TANPA tetap 7,5 dari topik 2074. Kuncinya ada di bagian "Pemeriksa kedua" `koordinasi/telegram-gelombang-A5-2026-10-17.md`. Dua giliran dinilai sebagai satu jawaban.

Penilai independen (bukan pembuat skill) memakai `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Transkrip ada di `scratchpad/openclaw-real/hasil/a7/`. Jawaban ganda yang identik adalah salinan log dan hanya dihitung sekali. Semua angka dihitung ulang dengan Decimal dari CSV, tanpa skrip skill:
- TER A/B/C PP 58/2023;
- BPJS: dasar gaji pokok + tunjangan tetap, Kes 4%+1%, JHT 3,7%+2%, JKK 0,54%, JKM 0,3%, JP 2%+1% (batas 11.086.300);
- lembur sesuai PP 35/2021.

Tanggal dihitung dengan kalender Python.

Acuan: **LULUS** bila DENGAN ≥ 8, selisih ≥ 1,5, dan tidak ada salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| gaji-umkm | 1.0.13 | 2122 / 2123 | 3,5 | 8,5 | +5,0 | **LULUS** | Dengan skill, Anda langsung mendapat gaji bersih 11 karyawan, dan semuanya benar sampai rupiah (transfer Rp65.412.866, BPJS Kesehatan Rp3.265.000, BPJS Ketenagakerjaan Rp5.581.620, PPh 21 Rp522.059). Gaji Lina, yang resign, ditahan sambil ditawarkan dua pilihan, karena pajaknya harus dihitung ulang setahun. Tanpa skill, gaji per orang meleset, dan pajak Lina dihitung seperti bulan biasa. |
| buku-piutang | 1.0.5 (kirim ulang) | 2074 / 2125 | 7,5 | 8,5 | +1,0 | **BELUM** (selisih < 1,5) | Dengan skill, bot langsung menunjukkan siapa yang menunggak dan total lewat tempo (Rp2.650.000), dan memberi draf tagih dengan tautan WA siap klik yang Anda kirim sendiri. Namun versi tanpa skill juga sudah menghitung semua tunggakan dengan benar, sehingga selisihnya kecil. |

Pembanding: gelombang G21 lama memberi gaji-umkm TANPA 0 (habis waktu) dan DENGAN 4 (1.0.12, seluruh hitungan ditahan). Gelombang A5 memberi buku-piutang DENGAN 4,0, tetapi skor itu dinyatakan TIDAK SAH oleh pemeriksa kedua. Pra-cek `koordinasi/pracek-telegram-akun-a-2026-10-17.md` memberi gaji-umkm 8,5 SIAP KIRIM.

Catatan lintas skill:
- **Panjang:** semua pesan ≤ 4.096 karakter, masing-masing 1 bagian. Rinciannya: gaji DENGAN 3.726 dan 3.133, TANPA 256 dan 1.921, piutang DENGAN 2.482 dan 169. Tidak ada yang terpotong.
- **Tabel Markdown mentah:** tidak ada. gaji-umkm kini memakai butir per karyawan; tabel 7 kolom yang muncul saat pra-cek sudah hilang.
- **Istilah proses atau jalur berkas:**
  - gaji DENGAN: tidak ada nama perintah, opsi, atau jalur berkas.
  - gaji TANPA: menyebut folder `laporan/gaji/` dan nama berkas CSV, serta membocorkan label uji ("topik ini ditandai TANPA skill").
  - piutang DENGAN: menyebut "ada skill terpisah buat itu".
- **Basis data buku piutang:** tidak diperiksa langsung oleh penilai. Klaim "udah dicatat semua" dinilai dari transkrip saja.

## Rincian per skill

### gaji-umkm 1.0.13 — TANPA 3,5 → DENGAN 8,5 (+5,0) LULUS

**Angka kunci (dihitung ulang, Decimal), 11 karyawan tanpa Lina:**

| Karyawan | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |
|---|---:|---:|---:|---:|---:|
| Andi (K/1, bonus 500 rb, kasbon 250 rb) | 8.150.000 | 625.009 | 85.009 | 7.524.991 | 8.914.150 |
| Budi (K/2) | 6.200.000 | 244.189 | 16.189 | 5.955.811 | 6.800.780 |
| Citra | 5.700.000 | 260.710 | 44.710 | 5.439.290 | 6.269.160 |
| Dewi | 5.850.000 | 279.998 | 45.998 | 5.570.002 | 6.466.590 |
| Eko (kontrak, tanpa JP) | 5.750.000 | 207.085 | 45.085 | 5.542.915 | 6.211.160 |
| Fajar | 5.750.000 | 207.085 | 45.085 | 5.542.915 | 6.211.160 |
| Gita | 6.500.000 | 345.182 | 85.182 | 6.154.818 | 7.185.100 |
| Hadi (K/3, TER C) | 7.600.000 | 383.678 | 79.678 | 7.216.322 | 8.401.040 |
| Indah (lembur 9 × 5.400.000/173 = 280.925) | 5.980.925 | 262.817 | 46.817 | 5.718.108 | 6.550.085 |
| Joko | 5.700.000 | 162.000 | 0 | 5.538.000 | 6.161.160 |
| Kiki (penuh) | 5.400.000 | 190.306 | 28.306 | 5.209.694 | 5.861.160 |
| **Total** | **68.580.925** | **3.168.059** | **522.059** | **65.412.866** | **75.031.545** |

Hasil setoran: BPJS Kesehatan Rp3.265.000 dan BPJS Ketenagakerjaan Rp5.581.620. Prorata Kiki: 5.400.000 × 16 ÷ 30 = 2.880.000. Prorata Lina: 10.000.000 × 14 ÷ 30 = 4.666.667 dan 1.000.000 × 14 ÷ 30 = 466.667. **Semua angka DENGAN identik** dengan hitungan penilai dan dengan kunci examples/08.

Kutipan DENGAN (giliran 1):
> REKAP GAJI SEPTEMBER 2026 — 11 karyawan dihitung, 1 tertunda
> • Transfer gaji bersih ke karyawan: Rp 65.412.866 … Setor PPh 21: Rp 522.059
> TERTUNDA — Lina Fiktif (resign 14/9) … (a) kirim 3 angka itu → saya hitung ulang final, atau (b) hitung September-nya dulu pakai tarif bulanan sebagai angka SEMENTARA
> Kalau mau prorata hari kalender (16 dari 30 hari): gaji pokok 5.400.000 × 16/30 = 2.880.000.

Giliran 2 ("ya"): bot menganggap "ya" sebagai "simpan" dan mengatakannya terang-terangan ("Sudah saya simpan datanya"). Data berstatus DRAF, periode jujur belum dikunci, dan pertanyaan soal Lina dan Kiki diulang. Bot juga menawarkan slip dan berkas transfer setelah kedua hal itu dijawab.

**Alasan skor DENGAN 8,5:**
- (+) Semua syarat LOLOS terpenuhi:
  - hitungan tidak ditahan seluruhnya;
  - Lina tertunda dengan pilihan (a) dan (b), dan setoran tertulis tegas "BELUM termasuk Lina";
  - prorata Kiki tampil sebagai pilihan;
  - tidak ada nama perintah, opsi, atau jalur berkas;
  - tiap pesan ≤ 4.096 karakter;
  - "ya" dijawab.
- (+) Angka benar semua, dengan butir per orang (bukan tabel) yang terbaca di HP. Dasar aturan, catatan pembulatan, dan Coretax disebut.
- (+) Pertanyaan di akhir hanya tiga: data Lina, Lina penuh atau prorata, Kiki penuh atau prorata.
- (−) Giliran 2 mengulang seluruh daftar 11 karyawan (±3,1 ribu karakter) padahal angkanya tidak berubah. Label (a)/(b) juga hilang.
- (−) "Masa Pajak Terakhir" dan "bruto" tidak dijelaskan dengan bahasa awam.
- (−) Pratinjau meminta balasan "simpan", tetapi "ya" diterima tanpa konfirmasi singkat. Ini wajar, tetapi sebaiknya diakui eksplisit.

**Alasan skor TANPA 3,5:**
- (−) **Angka kunci salah**, sehingga skor maks 5:
  - gaji bersih per orang meleset, misalnya Andi Rp7.528.500 (benar Rp7.524.991) dan Indah Rp5.720.068 (benar Rp5.718.108);
  - Lina dihitung prorata 12/26 dengan pajak bulanan biasa, tanpa perhitungan ulang setahun (Masa Pajak Terakhir), yang merupakan kesalahan fakta pajak;
  - Kiki prorata 14/26 tanpa ditanya dulu.
- (−) Bot membocorkan label uji ("TANPA skill"), mengaku menyimpan berkas CSV beserta jalurnya, dan tidak memisahkan setoran BPJS Kesehatan dan Ketenagakerjaan.
- (+) Asumsi ditulis dengan jelas, struktur ringkas, dan lembur Indah benar (280.925).

### buku-piutang 1.0.5 (kirim ulang DENGAN) — TANPA 7,5 → DENGAN 8,5 (+1,0) BELUM

**Angka kunci (dihitung ulang, per 17/10/2026):**
- Kafe Senja: jatuh tempo 12/9, sisa 2.400.000 − 1.000.000 = Rp1.400.000, lewat 35 hari.
- Bu Tini: jatuh tempo 15/9, Rp1.250.000, lewat 32 hari.
- Total lewat tempo: **Rp2.650.000**.
- Pak Joko: Rp850.000, jatuh tempo 25/10 (8 hari lagi).

Semua angka DENGAN benar. Tautan wa.me ke 6281234567890 setelah di-decode sama persis dengan draf.

Kutipan DENGAN:
> **Belum bayar & sudah lewat jatuh tempo** (per hari ini, 17 Okt 2026): Kafe Senja: sisa Rp 1.400.000, lewat 35 hari … Total terlewat: Rp 2.650.000
> Draf pesan tagih untuk Kafe Senja (periksa dulu, lalu kirim sendiri ya — saya nggak kirim otomatis)
> Tautan WA (teks sudah terisi, tinggal tekan kirim): https://wa.me/6281234567890?text=…

Giliran 2 ("ya"): bot bertanya balik apakah "ya" berarti pesan sudah terkirim atau rekening perlu diisi. Bot tidak menganggap "ya" sebagai izin mengirim, jadi perilakunya aman.

Catatan desain: kirim ulang ini membatalkan masalah A5. Balasan pertama sudah memuat rekap dan draf tanpa berhenti di izin membuat buku.

**Alasan skor DENGAN 8,5:**
- (+) Ketiga kunci lengkap di balasan pertama: daftar tunggakan, total lewat tempo, dan draf tagih dengan tautan wa.me. Draf ditegaskan dikirim pengguna sendiri.
- (+) Istilah setelan seperti "Termin default" dan "Zona" yang muncul di A5 sudah hilang. Rekening ditanyakan sebagai catatan penutup.
- (−) Draf berisi "Pembayaran bisa melalui cara yang biasa". Kalimat ini samar dan sebaiknya diganti `[isian rekening]` atau dihapus.
- (−) Ada kata proses "skill terpisah". Tautan wa.me mentah sangat panjang di chat.
- (−) Jawaban atas "ya" berupa pertanyaan klarifikasi tanpa hasil baru. Ini wajar, tetapi tidak menambah nilai.

**Alasan TANPA 7,5 (dari A5, tidak dinilai ulang):** angka benar, tetapi tidak ada total lewat tempo dan tidak ada tautan wa.me. Bot juga menawarkan mengirim langsung ke nomor pelanggan.

**Perbaikan paling berdampak (BELUM):**
1. Tambahkan nilai yang tidak dimiliki model dasar di balasan pertama, misalnya:
   - urutan prioritas tagih (paling lama atau paling besar dulu);
   - jadwal tagih ulang (misalnya "tagih lagi 3 hari lagi bila belum dibalas");
   - draf kedua untuk Bu Tini sekaligus, karena ia juga lewat tempo.
2. Di draf, ganti "cara yang biasa" dengan `[isian rekening]` atau hapus kalimatnya.
3. Sembunyikan kata "skill". Tawarkan surat teguran dengan bahasa awam ("bisa saya buatkan surat teguran resmi").
4. Untuk uji berikutnya, pakai kasus yang biasanya membuat model dasar salah, misalnya beberapa cicilan sebagian, bon lintas bulan, atau pembayaran yang melebihi satu nota. Dengan kasus seperti itu, nilai tambah buku dan script bisa terukur.

Verdik akhir gelombang A7: LULUS 1 (gaji-umkm 1.0.13), BELUM 1 (buku-piutang 1.0.5, selisih +1,0).
