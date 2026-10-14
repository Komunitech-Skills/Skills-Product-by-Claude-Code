# Uji OpenClaw sebelum/sesudah: hitung-thr 1.0.9 (uji ulang 1.0.10 di bagian atas)

## Uji ulang 1.0.10 (2026-10-14) — hanya sisi DENGAN skill

- **Penguji:** agent penguji independen Komunitech (bukan pembuat; SKILL.md, README, `catalog.csv`, dan scripts tidak diubah).
- **Versi skill:** 1.0.10 (sesuai `catalog.csv`). Tujuan: memeriksa tiga cacat uji 1.0.9 (di bawah): (1) input kurang hanya bertanya tanpa hitungan bersyarat, (2) kata proses/path/nama skill lain bocor ke balasan, (3) nama usaha dikarang padahal seharusnya `[isi: nama usaha]`.
- **Cara uji:** OpenClaw lokal yang sama (`uji.sh`, `openclaw agent --local`, satu giliran), model router `claude-sonnet-5`. Home dibuat ulang bersih per skenario (`mk-home.sh thr10-s4|s3|s2 hitung-thr`) berisi **hanya** `hitung-thr`. Pesan **identik** dengan uji 1.0.9 di bawah. Satu run per skenario (tidak ada timeout), satu `uji.sh` milik penguji per waktu. Sisi TANPA skill **tidak diulang**; pembandingnya skor TANPA uji 1.0.9. Tanggal agent: 14 Oktober 2026 (TZ Asia/Jakarta).
- **Alat yang dipanggil agent:** S4 read + exec + write (file kerja berisi Wawan dan Tini `masa_kerja_bulan` = 12) · S3 read + exec · S2 read + exec + write. Tanpa web, tanpa pesan terkirim. Durasi 82 / 90 / 95 detik.
- **Verifikasi angka:** kalkulator Python milik penguji (tidak mengimpor script skill): masa kerja bulan penuh inklusif sampai hari raya; THR < 12 bulan = masa kerja/12 × (gaji pokok + tunjangan tetap); harian lepas = rata-rata upah per bulan; batas H-7 dan nama hari dari kalender Python. Hasil: Ujang mulai 1 Sep = 6 bln (Rp1.400.000), mulai 30 Sep = 5 bln (Rp1.166.667) · Pak Slamet 10 bln, rata-rata Rp2.600.000 → Rp2.166.667 · Maria 7 bln → Rp2.100.000 · Yohanes Rp5.750.000 · 10 Mar 2027 = Rabu, 3 Mar 2027 = Rabu, 25 Des 2026 = Jumat, 18 Des 2026 = Jumat. Perkiraan PPh 21 Desember Yohanes (K/2, Pasal 17 setahun, tanpa iuran): bruto Rp74.750.000 − biaya jabatan Rp3.737.500 − PTKP Rp67.500.000 → PKP Rp3.512.000 × 5% = Rp175.600.

### Ringkasan skor 1.0.10

| Skenario | Tanpa skill (uji 1.0.9, tidak diulang) | Dengan 1.0.9 | **Dengan 1.0.10** |
|---|:-:|:-:|:-:|
| 4. Input kurang: 3 gaji tanpa hari raya & tanggal masuk | 4 | 6,5 | **7,5** |
| 3. Tukang harian lepas + "umumkan ke grup, sebut masing-masing dapat berapa" | 6 | 8,5 | **8,5** |
| 2. Kafe, THR Natal 2026 + "PPh 21-nya gimana?" | 5 | 8 | **8** |
| **Rata-rata 3 skenario** | **5,0** | **7,7** | **8,0** |

- **Kesalahan angka di sisi DENGAN skill:** tidak ada (semua THR, rentang, total, masa kerja, dan batas H-7 sama dengan hitung ulang penguji).

### Status tiga cacat 1.0.9

| Cacat 1.0.9 | Status 1.0.10 | Bukti |
|---|---|---|
| 1. Input kurang: hanya bertanya, tanpa hitungan | **Hilang** | S4: kalimat pertama menyebut asumsi Idul Fitri 2027 (perkiraan Rabu, 10 Maret 2027), lalu tabel, rentang Ujang Rp1.166.667–Rp1.400.000, total Rp7.666.667–Rp7.900.000, dan tepat 3 pertanyaan bernomor di akhir. Tetapi muncul cacat baru (Tini, lihat bawah). |
| 2. Kata proses, path, nama skill lain | **Hilang** | 0 dari 3 balasan memuat "skill", "script", "exec", "JSON", nama file, path (`/opt/...`, workspace), nama skill lain, atau "belum terpasang" (diperiksa dengan grep). Rujukan pajak memakai kalimat awam ("Pajak THR ini bisa saya hitungkan terpisah"). |
| 3. Nama usaha karangan di teks grup | **Sebagian** | Nama karangan hilang ("Bengkel Motor"/"Toko Bangunan" tidak muncul lagi), tetapi **`[isi: nama usaha]` tidak dipakai di satu pun dari 3 teks grup**. Gantinya kata umum: "karyawan kami" + "Salam, Manajemen" (S4), "toko akan membayarkan" (S3), "perusahaan" + "pemilik/pengelola" (S2). SKILL.md melarang pengganti jenis usaha/"kami". Akar masalah: agent tidak memberi `--perusahaan`, dan `scripts/thr.py` (baris 355 & 376) memakai cadangan `perusahaan or "kami"` / `"Manajemen "` alih-alih `[isi: nama usaha]`. |

### Cacat baru / sisa (DENGAN skill 1.0.10)
1. **S4, asumsi tak disebut (sedang):** Tini tidak punya keterangan masa kerja sama sekali, tetapi ditulis "12 bln" tanpa label asumsi (Wawan diberi label "asumsi 'sudah lama'", Tini tidak) dan **tidak ditanyakan** (pertanyaan no. 2 hanya soal Ujang). SKILL.md meminta dua baris ("bila ≥ 12 bulan" / "bila < 12 bulan, mis. 6 bulan") dan tanggal masuk semua orang dalam satu pertanyaan. Bila Tini ternyata baru 6 bulan, THR-nya Rp1.750.000, bukan Rp3.500.000 (total meleset Rp1.750.000). Hitungannya sendiri benar untuk asumsi itu, jadi tidak dihitung sebagai salah angka.
2. **S4, teks grup dengan tanggal perkiraan (ringan):** teks grup dibuat padahal tidak diminta dan tanggal hari raya masih perkiraan; SKILL.md meminta ditunda, atau tanggal ditulis `[isi: tanggal batas bayar]`.
3. **S2, PPh 21 kurang tajam (ringan):** penjelasan Desember = hitung ulang setahun benar, Yohanes "kemungkinan besar tetap kena potongan" benar (perkiraan penguji ±Rp175.600), tetapi tanpa perkiraan angka. Maria disebut "belum bisa dipastikan", padahal penghasilan 2026 dari kafe (8 × Rp3.600.000 + THR Rp2.100.000 = Rp30.900.000) di bawah PTKP terendah TK/0 Rp54.000.000, jadi kemungkinan besar Rp0 apa pun statusnya (kecuali ada penghasilan dari pemberi kerja lain di 2026). Akibatnya pertanyaan PTKP Maria di akhir tidak perlu.
4. **S3 (ringan):** denda 5% bila telat tidak disebut (di 1.0.9 ada); tidak menawarkan draf pesan pribadi per orang.

### Verdik uji ulang 1.0.10: **BELUM (tipis)**
Rata-rata DENGAN skill 8,0 (tepat di ambang 8) dan tanpa salah angka; cacat 1 dan 2 **hilang**. Namun cacat 3 baru **sebagian** hilang (`[isi: nama usaha]` tidak muncul di teks grup mana pun), dan perbaikan cacat 1 memunculkan asumsi tak disebut untuk Tini. Syarat "ketiga cacat hilang" belum terpenuhi. Selisih terhadap TANPA skill pada 3 skenario ini +3,0 poin (pembanding TANPA dari uji 1.0.9).

**Perbaikan paling berdampak (urut):**
1. `scripts/thr.py`: cadangan nama usaha kosong → `[isi: nama usaha]` (bukan "kami"/"Manajemen "), sehingga teks grup aman walau agent lupa `--perusahaan`; tambah tes.
2. SKILL.md "Info wajib kurang": tegaskan **setiap** orang tanpa keterangan masa kerja (contoh "Tini 3,5jt") wajib dua baris berlabel asumsi dan disebut di pertanyaan no. 2 bersama orang lain; tambah butir checklist "tidak ada masa kerja tanpa sumber/label asumsi".
3. Data kurang: teks grup hanya bila diminta; bila dibuat, tanggal `[isi: tanggal batas bayar]`.
4. THR Desember: beri perkiraan PPh 21 bertanda "perkiraan" bila PTKP & gaji tetap diketahui; untuk penghasilan setahun jelas di bawah PTKP TK/0 sebut "kemungkinan Rp0".

**Kalimat pembeda (tetap berlaku):** tanpa skill, AI menghitung THR karyawan baru dari masa kerja "sampai hari ini" (Ujang Rp233.333); dengan skill 1.0.10, AI langsung memberi hitungan sampai Lebaran 2027 dengan rentang Rp1.166.667–Rp1.400.000 dan batas bayar Rabu, 3 Maret 2027, lalu bertanya maks. 3 hal.

### Skenario 4 (1.0.10): input kurang

**Pesan:** sama dengan skenario 4 di bawah.

> THR untuk 3 karyawan, saya hitung pakai Idul Fitri 2027 (perkiraan tanggal **Rabu, 10 Maret 2027** — belum ada tanggal resmi dari pemerintah, jadi ini asumsi dulu).
>
> ### A. Rekap per orang — khusus Anda/pemilik (jangan ditempel ke grup)
>
> Batas bayar THR (H-7): **Rabu, 3 Maret 2027**
>
> | Nama | Masa kerja | Gaji pokok | Rumus | THR |
> |---|---:|---:|---|---:|
> | Wawan | ≥12 bln (asumsi "sudah lama") | Rp3.000.000 | 1 × gaji | **Rp3.000.000** |
> | Tini | 12 bln | Rp3.500.000 | 1 × gaji | **Rp3.500.000** |
> | Ujang | 5–6 bln (masuk bulan lalu) | Rp2.800.000 | masa kerja ÷ 12 × gaji | **Rp1.166.667 – Rp1.400.000** |
>
> **Total THR: Rp7.666.667 – Rp7.900.000** (tergantung tanggal pasti masuknya Ujang)
>
> Catatan:
> - PPh 21 belum dihitung karena status PTKP belum diisi — kalau mau, bisa saya bantu sekalian.
> - THR wajib dibayar penuh (tidak dicicil), paling lambat H-7 sebelum hari raya. Telat bayar kena denda 5% dari total THR.
> - Masa kerja dihitung bulan penuh sampai hari raya.
>
> ### B. Teks grup — draf, silakan tempel sendiri (tanpa nominal per orang)
>
> ```
> Yth. Rekan-rekan karyawan kami,
>
> Menyambut Idul Fitri 1448 H, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan paling lambat Rabu, 3 Maret 2027 (7 hari sebelum hari raya).
>
> Ketentuan besaran THR (Permenaker 6/2016):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah.
> • Masa kerja 1 s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.
>
> Rincian THR masing-masing akan dikirim secara PRIBADI oleh bagian keuangan. Ada pertanyaan tentang THR Anda, silakan hubungi langsung.
>
> Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu.
>
> Salam,
> Manajemen
> ```
>
> Supaya angkanya pasti (bukan rentang), ada 3 hal yang bisa membantu:
> 1. Tanggal Lebaran dipakai tanggal perkiraan di atas, atau sudah ada tanggal resmi?
> 2. Ujang masuk tanggal berapa persisnya bulan lalu (1, 15, 30)?
> 3. Ada tunjangan tetap lain (transport/makan tetap) di luar gaji pokok untuk ketiganya?
>
> Data gaji yang saya catat untuk hitungan ini mau saya hapus setelah selesai, atau disimpan saja?

**Nilai: 7,5** (1.0.9: 6,5). Hitung dulu dengan asumsi di kalimat pertama, angka benar, 3 pertanyaan, tanpa kata proses, tawaran hapus data gaji. Kurang: Tini "12 bln" tanpa label asumsi dan tidak ditanyakan; teks grup dibuat dengan tanggal perkiraan dan tanpa `[isi: nama usaha]` ("karyawan kami", "Manajemen"). **Skill/script terpakai?** Ya: SKILL.md + script lewat exec, file kerja ditulis.

### Skenario 3 (1.0.10): tukang harian lepas + pengumuman grup

**Pesan:** sama dengan skenario 3 di bawah.

> Sudah saya hitung. Untuk nominal per orang, saya pisahkan dari teks grup — karena gaji/THR itu data pribadi karyawan, idealnya disampaikan lewat pesan pribadi, bukan diumumkan di grup bersama supaya tidak jadi bahan perbandingan antar karyawan.
>
> **A. RINCIAN PER ORANG — untuk Anda/pemegang kas saja**
> Idul Fitri 1448 H, Rabu 10 Maret 2027 · Batas bayar THR (H-7): **Rabu, 3 Maret 2027**
>
> - **Pak Slamet** (harian lepas, mulai 4 Mei 2026 → masa kerja 10 bulan saat Lebaran)
>  Rata-rata upah dari 6 bulan yang Anda kasih (Mei–Okt): (2,4+2,6+2,5+2,8+2,7+2,6)/6 = **Rp 2.600.000**
>  THR = 10/12 × Rp 2.600.000 = **Rp 2.166.667**
> - **Rini** (admin tetap, kerja sejak 2023 → masa kerja 50 bulan, jadi full)
>  THR = 1 × gaji = **Rp 4.000.000**
> - **Total THR yang perlu disiapkan: Rp 6.166.667**
>
> ⚠️ Catatan: masa kerja Pak Slamet itu 10 bulan, tapi data upah yang Anda kasih baru 6 bulan (Mei–Okt), karena sisanya (Nov 2026–Feb 2027) belum kejadian/belum ada datanya. Saya hitung rata-ratanya dari 6 bulan yang ada dulu. PPh 21 belum saya hitung karena status PTKP keduanya belum disebutkan — kalau mau sekalian dipotong pajaknya, kasih tahu status PTKP masing-masing (TK/0, K/1, dst).
>
> **B. TEKS UNTUK DIUMUMKAN DI GRUP KARYAWAN** (tanpa nominal per orang — tinggal tempel sendiri)
>
> ```
> Yth. Rekan-rekan karyawan,
>
> Menyambut Idul Fitri 1448 H, toko akan membayarkan THR Keagamaan paling lambat Rabu, 3 Maret 2027 (7 hari sebelum Lebaran).
>
> Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker THR 2026):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah.
> • Masa kerja 1 bulan s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • Untuk pekerja harian lepas, upah 1 bulan dihitung dari rata-rata upah selama bekerja.
> • THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.
>
> Rincian nominal masing-masing akan disampaikan secara PRIBADI oleh pemilik/bagian keuangan, bukan di grup. Kalau ada pertanyaan soal THR masing-masing, silakan tanya langsung ke pemilik.
>
> Selamat menyambut Idul Fitri, terima kasih atas kerja keras Bapak/Ibu semua.
> ```
>
> Pajak THR (PPh 21) dihitung terpisah kalau nanti mau dipotongkan — tinggal bilang saja.
>
> Pertanyaan: karena upah Pak Slamet 4 bulan terakhir (Nov 2026–Feb 2027) belum terjadi, nanti mendekati Lebaran mau saya hitung ulang pakai upah aktual bulan-bulan itu, atau cukup pakai rata-rata Rp 2,6 juta seperti sekarang untuk perkiraan awal?
>
> Data gaji yang saya catat untuk hitungan ini mau saya hapus setelah selesai, atau dibiarkan saja untuk referensi nanti?

**Nilai: 8,5** (1.0.9: 8,5). Angka benar dan rumus rata-rata ditunjukkan; peringatan data upah 6 bulan vs masa kerja 10 bulan jelas; pola tolak → alasan privasi → teks grup tanpa nominal tetap dibuat; satu pertanyaan + tawaran hapus data; tanpa kata proses atau path. Kurang: teks grup "toko akan membayarkan" tanpa `[isi: nama usaha]`; denda 5% tidak disebut; tidak menawarkan draf pesan pribadi. **Skill/script terpakai?** Ya: SKILL.md + script lewat exec.

### Skenario 2 (1.0.10): kafe, THR Natal 2026 + PPh 21

**Pesan:** sama dengan skenario 2 di bawah.

> **A. RINCIAN THR NATAL 2026 — untuk Anda/HR saja**
>
> Natal 2026 jatuh **Jumat, 25 Desember 2026**. Batas bayar THR paling lambat **H-7 = Jumat, 18 Desember 2026** (kalau cair lebih awal dari itu juga boleh).
>
> | Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR |
> |---|---|---:|---:|---|---:|
> | Maria (Barista) | Tetap | 7 bulan (20 Mei → 25 Des 2026) | Rp 3.600.000 | 7/12 × upah | **Rp 2.100.000** |
> | Yohanes (Kepala Dapur) | Tetap | 42 bulan (sejak Juni 2023) | Rp 5.750.000 (gaji pokok 5jt + tunjangan tetap 750rb) | ≥ 12 bulan → 1 × upah | **Rp 5.750.000** |
> | **Total** | | | | | **Rp 7.850.000** |
>
> Catatan:
> - Maria kerja belum genap setahun, jadi THR-nya proporsional: 7/12 × gaji.
> - Yohanes sudah lewat 12 bulan, jadi dapat THR penuh 1× gaji pokok + tunjangan tetap.
> - THR wajib dibayar penuh sekaligus (tidak boleh dicicil). Kalau telat, ada denda 5% dari total THR dan THR-nya tetap harus dibayar.
> - THR tidak jadi dasar hitungan iuran BPJS.
>
> **Soal PPh 21-nya:**
> Karena THR ini cair di bulan **Desember**, aturannya beda dari bulan biasa — PPh 21 Desember dihitung ulang setahun penuh (bukan dipotong bulanan pakai tarif TER seperti bulan-bulan lain). Jadi angka potongan pastinya baru bisa dikeluarkan saat perhitungan setahun itu dilakukan, bukan dari hitungan THR saja. Untuk Yohanes (status nikah anak 2 / K-2) kemungkinan besar tetap kena potongan karena penghasilannya di atas batas tidak kena pajak; Maria, karena saya belum tahu status pernikahannya, belum bisa dipastikan kena atau tidak. Pajak THR ini bisa saya hitungkan terpisah kalau mau — tinggal bilang saja.
>
> ---
>
> **B. TEKS UNTUK GRUP KARYAWAN** — draf untuk Anda tempel sendiri (tanpa nominal per orang, karena itu data pribadi):
>
> ```
> Yth. Rekan-rekan karyawan,
>
> Menyambut Natal 2026, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan paling lambat Jumat, 18 Desember 2026 (7 hari sebelum hari raya).
>
> Ketentuan besaran THR (sesuai aturan ketenagakerjaan yang berlaku):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
> • Masa kerja 1 s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil, dan dikenai potongan PPh 21 sesuai ketentuan pajak.
>
> Rincian THR masing-masing (nominal dan potongan pajak) akan disampaikan secara pribadi oleh pemilik/pengelola. Mohon tidak membahas nominal pribadi di grup. Ada pertanyaan soal THR Anda, silakan hubungi langsung.
>
> Selamat menyambut Natal. Terima kasih atas kerja keras selama ini.
> ```
>
> ---
>
> Dua hal kecil untuk melengkapi:
> 1. Mau saya hitungkan juga potongan PPh 21 setahun yang sebenarnya (butuh info PTKP Maria — lajang/menikah, ada tanggungan atau tidak)?
> 2. Data gaji yang saya catat untuk hitungan ini mau saya hapus setelah selesai?

**Nilai: 8** (1.0.9: 8). THR, total, H-7 Jumat 18 Des 2026, denda 5%, "tidak dicicil", THR bukan dasar BPJS: benar. PPh 21 Desember = hitung ulang setahun dijelaskan dengan bahasa awam tanpa angka karangan dan tanpa nama skill lain. Kurang: tanpa perkiraan angka Yohanes; Maria "belum bisa dipastikan" padahal kemungkinan besar Rp0; teks grup "perusahaan" tanpa `[isi: nama usaha]`. **Skill/script terpakai?** Ya: SKILL.md + script lewat exec, file kerja ditulis.

---

**Di bawah ini: uji sebelum/sesudah lengkap 1.0.9 (2026-10-14), dasar perbandingan uji ulang di atas.**


- **Tanggal:** 2026-10-14 (Asia/Jakarta)
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill; brief pembuat dan transkrip agent lain tidak dibaca)
- **Versi skill:** 1.0.9 (sesuai `catalog.csv`)
- **Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per skenario), model router Komunitech `claude-sonnet-5` (sama dengan bot member). SESUDAH = home dibuat ulang bersih (`mk-home.sh`) berisi **hanya** `hitung-thr`. SEBELUM = home bersih tanpa skill. Pesan identik di kedua sisi; semua data ditempel di pesan (tanpa file). Skenario 1 juga dijalankan di konteks kanal Telegram (`uji-tg.sh`, `--channel telegram`, tanpa mengirim) di kedua sisi. Satu `uji.sh` per waktu.
- **Data:** fiktif (nama karyawan, usaha, gaji).
- **Verifikasi angka:** kalkulator Python milik penguji (tidak mengimpor script skill): masa kerja bulan penuh sampai hari raya, THR = masa kerja/12 × upah (gaji pokok + tunjangan tetap) bila < 12 bulan, 1 × upah bila ≥ 12 bulan; harian lepas < 12 bulan = rata-rata upah per bulan selama masa kerja (Permenaker 6/2016 Pasal 3; PP 36/2021); batas bayar H-7; hari dihitung dengan kalender Python. Script skill juga dijalankan penguji dengan data yang sama: hasil identik. `scripts/test_thr.py`: 38 tes OK.
- **Alat yang dipanggil agent (SESUDAH):** SKILL.md + `thr.py` (dan `tahun_hijriah.py` untuk Lebaran) lewat exec; file CSV kerja ditulis di folder kerja agent. Tidak ada akses web, tidak ada pesan terkirim. SEBELUM: tanpa alat, kecuali skenario 2 (agent mencoba mencari di web, gagal).
- **Durasi:** SESUDAH 32-127 detik; SEBELUM 24-367 detik.
- Uji lama berbentuk gabungan (paket/solusi VIP Kantor & Manajemen, dan bersama `laporan-status-kantor`) tidak diulang di sini; catatannya ada di `solusi-vip/*/UJI-OPENCLAW.md` (untuk skill ini `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` dan `UJI-GABUNGAN-2026-10-03.md`) serta `UJI-OPENCLAW-ULANG*.md` di folder ini.

## Ringkasan skor

| Skenario | Tanpa skill | Dengan skill 1.0.9 |
|---|:-:|:-:|
| 1. Normal utama: bengkel, 4 karyawan, Lebaran 10 Mar 2027 (lokal) | 8 | 8,5 |
| 1T. Skenario 1 di konteks Telegram | 7,5 | 8,5 |
| 2. Normal kedua: kafe, THR Natal 2026 + "PPh 21-nya gimana?" | 5 | 8 |
| 3. Normal ketiga: tukang harian lepas + "umumkan ke grup, sebut masing-masing dapat berapa" | 6 | 8,5 |
| 4. Input kurang: 3 gaji tanpa hari raya & tanggal masuk | 4 | 6,5 |
| **Rata-rata** | **6,1** | **8,0** |

- **Selisih:** +1,9 poin.
- **Kesalahan angka/fakta di sisi DENGAN skill:** tidak ada (semua THR, total, masa kerja, dan batas H-7 sama dengan hitung ulang penguji).
- **Verdik: LULUS** (DENGAN 8,0 ≥ 8; selisih 1,9 ≥ 1,5; tanpa kesalahan angka/fakta). Tipis: rata-rata tepat di ambang.

**Kalimat pembeda (untuk materi jualan):** Tanpa skill, AI menghitung THR karyawan baru dari masa kerja "sampai hari ini" (Ujang dapat Rp233.333, padahal seharusnya dihitung sampai hari raya), menebak PPh 21 THR Desember dengan tarif TER, dan menulis nominal tiap orang di pengumuman grup; dengan skill, THR dihitung sampai hari raya dengan batas bayar H-7 (Rabu, 3 Maret 2027 / Jumat, 18 Desember 2026), PPh 21 Desember diarahkan ke hitung ulang setahun, dan teks grup selalu tanpa nominal pribadi.

**Cacat utama (DENGAN skill):**
1. Input kurang (skenario 4): agent hanya bertanya 5 pertanyaan tanpa menghitung apa pun, padahal bisa memberi hitungan bersyarat (mis. bila untuk Lebaran 2027) lalu bertanya maks. 3. Sumbernya SKILL.md ("tanyakan sekali ... maks. 5 pertanyaan").
2. Kata proses bocor ke pembeli di 3 dari 5 balasan ("pakai script resmi skill THR", "pakai skill THR", "skill `pph21-ter` (belum terpasang di sini)") dan path sandbox `/opt/ochome/...` ditampilkan.
3. Nama usaha karangan di teks grup ("Bengkel Motor", "Toko Bangunan") padahal SKILL.md meminta `[isi: nama usaha]` bila nama tidak diberikan.

---

## Skenario 1: Normal utama: bengkel motor, 4 karyawan, Lebaran 10 Maret 2027

**Pesan:**

> Pak tolong bantu, lebaran tahun depan katanya 10 Maret 2027. Saya punya bengkel motor, karyawan 4 orang:
> - Andi mekanik tetap, kerja dari Januari 2021, gaji pokok 3,8jt + tunjangan jabatan 400rb tiap bulan, plus uang makan 25rb per hari masuk
> - Sari kasir, masuk 1 April 2026, gaji 3,2jt
> - Dodi helper, masuk 2 Agustus 2026, gaji 2,9jt + tunjangan transport tetap 200rb/bulan
> - Yanto kontrak, mulai 15 Januari 2026, gaji 3,5jt
> THR mereka masing2 berapa, totalnya berapa, dan paling telat dibayar kapan?

**Angka penguji:** Andi 74 bln → Rp4.200.000 (uang makan harian tidak dihitung) · Sari 11 bln → 11/12 × 3.200.000 = Rp2.933.333 · Dodi 7 bln → 7/12 × 3.100.000 = Rp1.808.333 · Yanto 13 bln → Rp3.500.000 · **Total Rp12.441.666** · batas H-7 **Rabu, 3 Maret 2027**.

### SEBELUM (skill mati)

> Berikut rincian THR berdasarkan aturan THR Keagamaan (PP 36/2021 jo. Permenaker No. 6/2016): THR = 1 bulan upah untuk masa kerja ≥12 bulan terus-menerus, atau proporsional (masa kerja/12 × upah) untuk masa kerja 1–<12 bulan. Komponen upah = gaji pokok + tunjangan tetap (uang makan yang tergantung hari masuk itu tunjangan tidak tetap, jadi tidak dihitung).
>
> **1. Andi (mekanik tetap, sejak Jan 2021 → masa kerja >12 bulan, THR penuh)**
> - Gaji pokok 3.800.000 + tunjangan jabatan tetap 400.000 = 4.200.000
> - Uang makan harian tidak dihitung (variabel, bukan tunjangan tetap)
> - **THR Andi = Rp 4.200.000**
>
> **2. Sari (kasir, masuk 1 Apr 2026 → s.d. Lebaran 10 Mar 2027 = 11 bulan masa kerja)**
> - 11/12 × 3.200.000 = 2.933.333,33
> - **THR Sari = Rp 2.933.333**
>
> **3. Dodi (helper, masuk 2 Agu 2026 → s.d. Lebaran = 7 bulan masa kerja)**
> - Upah dasar THR = gaji pokok 2.900.000 + tunjangan transport tetap 200.000 = 3.100.000
> - 7/12 × 3.100.000 = 1.808.333,33
> - **THR Dodi = Rp 1.808.333**
>
> **4. Yanto (kontrak, mulai 15 Jan 2026 → s.d. Lebaran = sudah lewat 12 bulan, THR penuh)**
> - Status kontrak (PKWT) tidak mengurangi hak THR, tetap dapat penuh 1 bulan upah karena masa kerja sudah >12 bulan
> - **THR Yanto = Rp 3.500.000**
>
> **Total THR 4 karyawan = Rp 12.441.666**
> (4.200.000 + 2.933.333 + 1.808.333 + 3.500.000)
>
> **Batas paling lambat pembayaran:**
> Sesuai aturan, THR wajib dibayar paling lambat H-7 sebelum Hari Raya. Karena Lebaran 2027 jatuh 10 Maret 2027, maka paling lambat **Rabu, 3 Maret 2027** semua THR harus sudah cair.
>
> Catatan asumsi: perhitungan masa kerja per bulan dihitung sampai tanggal 10 Maret 2027 (tanggal Lebaran), dibulatkan ke bawah untuk bulan yang belum genap. Kalau Bapak mau hitung sampai tanggal pembayaran riil (3 Maret) hasilnya sama karena belum melewati tanggal anchor bulan berikutnya untuk Sari & Dodi.

### SESUDAH (skill 1.0.9 aktif)

> Siap Pak, berikut hasil hitungnya (pakai script resmi skill THR, jadi sudah sesuai Permenaker 6/2016):
>
> ### A. REKAP PER ORANG — KHUSUS PEMILIK/HR (jangan ditempel ke grup)
>
> **Rincian THR Idul Fitri 2027 — Bengkel Bapak**
> Hari raya: Rabu, 10 Maret 2027 · **Batas bayar paling lambat (H-7): Rabu, 3 Maret 2027**
>
> | Nama | Status | Masa kerja | Upah 1 bulan | Rumus | **THR** |
> |---|---|---:|---:|---|---:|
> | Andi | Tetap, sejak Jan 2021 | 74 bln (≥12) | Rp 4.200.000 (3,8jt + 400rb) | 1 × upah | **Rp 4.200.000** |
> | Sari | Tetap, masuk 1 Apr 2026 | 11 bln | Rp 3.200.000 | 11/12 × upah | **Rp 2.933.333** |
> | Dodi | Tetap, masuk 2 Agu 2026 | 7 bln | Rp 3.100.000 (2,9jt + 200rb) | 7/12 × upah | **Rp 1.808.333** |
> | Yanto | Kontrak, mulai 15 Jan 2026 | 13 bln (≥12) | Rp 3.500.000 | 1 × upah | **Rp 3.500.000** |
> | **TOTAL** | | | | | **Rp 12.441.666** |
>
> Catatan:
> - Uang makan Andi (25rb/hari masuk, tergantung kehadiran) **tidak dimasukkan** ke komponen upah THR karena bukan tunjangan tetap — hanya gaji pokok + tunjangan jabatan yang dihitung.
> - PPh 21 atas THR belum saya hitung karena status PTKP masing-masing belum diberikan. Kalau mau sekalian, kasih tahu status PTKP tiap orang (TK/0, K/1, dst.) nanti saya hitungkan potongannya.
> - Yanto berstatus kontrak tapi tetap wajib dapat THR karena masa kerja sudah ≥1 bulan (aturan ini sama untuk PKWT maupun PKWTT).
> - THR wajib dibayar penuh (tidak dicicil); kalau terlambat dari batas H-7, kena denda 5% dari total THR dan THR tetap wajib dibayar.
> - File rekap tersimpan di `/opt/ochome/.openclaw/workspace/thr-bengkel-2027/rekap-thr.csv`. Mau saya hapus setelah ini atau disimpan?
>
> ### B. TEKS GRUP — draf untuk Anda tempel sendiri (tanpa nominal per orang)
>
> ```
> Yth. Rekan-rekan karyawan kami,
>
> Menyambut Idul Fitri, bengkel akan membayarkan Tunjangan Hari Raya (THR) Keagamaan paling lambat Rabu, 3 Maret 2027 (7 hari sebelum hari raya).
>
> Ketentuan besaran THR (Permenaker 6/2016):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
> • Masa kerja 1 s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil.
>
> Rincian THR masing-masing akan disampaikan secara PRIBADI oleh pemilik/HR. Mohon tidak membagikan rincian pribadi di grup.
>
> Terima kasih atas kerja keras Bapak/Ibu. Selamat menyambut hari raya.
> ```
>
> **Ringkas jawaban pertanyaan Anda:**
> - Andi: Rp 4.200.000 | Sari: Rp 2.933.333 | Dodi: Rp 1.808.333 | Yanto: Rp 3.500.000
> - **Total THR: Rp 12.441.666**
> - **Paling lambat dibayar: Rabu, 3 Maret 2027**
>
> Teks grup di atas siap Anda tempel sendiri — saya tidak mengirim apa pun ke grup. Nominal per orang kirim lewat pesan pribadi ya, bukan ke grup bersama, karena itu data pribadi karyawan.

**Nilai:** SEBELUM **8** · SESUDAH **8,5**
- SEBELUM: Semua angka benar, uang makan harian dikeluarkan dan tunjangan transport tetap dimasukkan dengan alasan yang tepat, H-7 Rabu 3 Maret 2027 benar. Kurang: tidak menyebut denda 5% keterlambatan, tidak menyinggung PPh 21, tidak ada draf pengumuman (memang tidak diminta).
- SESUDAH: Semua angka sama dengan hitung ulang penguji. Tambahan yang berguna: denda 5% bila telat, "tidak dicicil", catatan PPh 21 belum dihitung karena PTKP tidak ada, teks grup tanpa nominal, tawaran menghapus CSV gaji. Kurang: kata proses "pakai script resmi skill THR" dan path sandbox ditampilkan.
- **Skill/script terpakai?** Ya: SKILL.md, `thr.py` lewat exec, CSV kerja ditulis di folder kerja.

---

## Skenario 1T: Skenario 1 di konteks kanal Telegram

**Pesan:** sama dengan skenario 1.

### SEBELUM (skill mati)

> Siap Pak, saya hitung pakai aturan THR Permenaker No. 6/2016, dengan asumsi Lebaran jatuh 10 Maret 2027 (catatan: tanggal resminya baru fix lewat sidang isbat, tapi untuk perencanaan ini saya pakai acuan dari Bapak).
>
> **Prinsip hitungnya:**
> - Kerja ≥ 12 bulan terus-menerus → THR penuh = 1× gaji pokok + tunjangan tetap
> - Kerja ≥ 1 bulan tapi < 12 bulan → THR proporsional = (jumlah bulan kerja ÷ 12) × upah sebulan
> - Tunjangan yang nilainya mengikuti kehadiran (uang makan per hari masuk Andi) TIDAK dihitung sebagai komponen upah THR, karena bukan tunjangan tetap
> - Tunjangan transport tetap (Dodi) IKUT dihitung karena memang tetap tiap bulan, tidak tergantung masuk/tidak
>
> **Rincian per karyawan:**
>
> - **Andi** (kerja sejak Jan 2021, >12 bulan) → THR penuh
>   Upah dasar: 3.800.000 + 400.000 (tunj. jabatan) = 4.200.000
>   **THR Andi = Rp 4.200.000**
>
> - **Sari** (masuk 1 Apr 2026 → 10 Mar 2027 = 11 bulan penuh, belum genap setahun)
>   11/12 × 3.200.000
>   **THR Sari = Rp 2.933.333**
>
> - **Dodi** (masuk 2 Agu 2026 → 10 Mar 2027 = 7 bulan penuh)
>   Upah dasar: 2.900.000 + 200.000 (transport tetap) = 3.100.000
>   7/12 × 3.100.000
>   **THR Dodi = Rp 1.808.333**
>
> - **Yanto** (kontrak, mulai 15 Jan 2026 → 15 Jan 2027 sudah genap 12 bulan, berarti sudah lewat setahun saat Lebaran) → THR penuh. Status kontrak/PKWT tidak mengurangi hak THR.
>   **THR Yanto = Rp 3.500.000**
>
> **Total THR 4 karyawan = Rp 12.441.667** (tepatnya Rp 12.441.666,67)
>
> **Batas akhir pembayaran:**
> Wajib dibayar paling lambat H-7 sebelum Lebaran. Kalau Lebaran 10 Maret 2027, berarti paling lambat **3 Maret 2027**. Saran saya siapkan dananya lebih awal, jangan mepet tanggal itu.

### SESUDAH (skill 1.0.9 aktif)

> Sudah saya hitung pakai skema THR resmi (Permenaker 6/2016 & SE Menaker THR). Catatan penting dulu: uang makan harian Andi (Rp25rb/hari masuk) **tidak** termasuk komponen THR karena itu tunjangan tidak tetap (nilainya berubah sesuai hari masuk) — yang dihitung hanya gaji pokok + tunjangan tetap (jabatan/transport).
>
> ### A. REKAP PER ORANG — KHUSUS PEMILIK/HR (rahasia, kirim per orang via pesan pribadi, jangan ditempel ke grup)
>
> **Rincian THR Idul Fitri 1448 H — Bengkel Motor**
> Hari raya: Rabu, 10 Maret 2027 · **Batas bayar (H-7): Rabu, 3 Maret 2027**
>
> | Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR |
> |---|---|---:|---:|---|---:|
> | Andi | Tetap, mekanik | 74 bln (≥12) | Rp 4.200.000 (3,8jt + 400rb) | 1 × upah | **Rp 4.200.000** |
> | Sari | Tetap, kasir | 11 bln | Rp 3.200.000 | 11/12 × upah | **Rp 2.933.333** |
> | Dodi | Tetap, helper | 7 bln | Rp 3.100.000 (2,9jt + 200rb) | 7/12 × upah | **Rp 1.808.333** |
> | Yanto | Kontrak | 13 bln (≥12) | Rp 3.500.000 | 1 × upah | **Rp 3.500.000** |
> | **Total** | | | | | **Rp 12.441.666** |
>
> Catatan:
> - PTKP tidak Anda sebutkan, jadi potongan PPh 21 atas THR belum dihitung (asumsikan TER dulu atau beri tahu status pajak masing-masing kalau mau saya hitung).
> - THR wajib dibayar penuh (tidak dicicil); terlambat kena denda 5% dari total THR, dan tetap wajib dibayar.
> - Masa kerja dihitung bulan penuh inklusif sampai 10 Maret 2027.
> - File rekap tersimpan di `/opt/ochome/.openclaw/workspace/thr-bengkel/rekap-thr.csv`.
>
> ### B. TEKS GRUP — draf untuk Anda tempel sendiri (tanpa nama & nominal per orang)
>
> ```
> Yth. Rekan-rekan karyawan Bengkel Motor,
>
> Menyambut Idul Fitri 1448 H, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan paling lambat Rabu, 3 Maret 2027 (7 hari sebelum hari raya).
>
> Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
> • Masa kerja 1 s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil.
>
> Rincian THR masing-masing akan dikirim secara PRIBADI oleh bagian keuangan. Mohon tidak membagikan rincian pribadi di grup.
>
> Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu.
>
> Salam,
> Manajemen Bengkel Motor
> ```
>
> Jadi intinya: **total THR Rp 12.441.666**, paling lambat cair **Rabu, 3 Maret 2027**. Mau saya hapus file CSV data karyawan tadi, atau simpan dulu? Kalau mau saya hitung potongan PPh 21-nya juga, kasih tahu status PTKP masing-masing (TK/0, K/1, dst).

**Nilai:** SEBELUM **7,5** · SESUDAH **8,5**
- SEBELUM: THR per orang benar; catatan sidang isbat baik. Total ditulis "Rp 12.441.667 (tepatnya Rp 12.441.666,67)" padahal jumlah THR per orang yang ditampilkan Rp12.441.666 (selisih Rp1 antara total dan rinciannya). Tanpa denda 5%, tanpa PPh 21.
- SESUDAH: Angka benar, 2.515 karakter (aman untuk satu pesan Telegram), alasan uang makan tidak dihitung ditaruh di awal. Kurang: nama usaha karangan "Bengkel Motor" di teks grup, path sandbox disebut.
- **Skill/script terpakai?** Ya: SKILL.md, `thr.py`.

---

## Skenario 2: Normal kedua: kafe, THR Natal 2026 untuk 2 karyawan + pertanyaan PPh 21

**Pesan:**

> Saya punya kafe kecil, 2 karyawan saya Kristen jadi THR-nya pas Natal tahun ini. Maria barista masuk 20 Mei 2026 gaji 3,6 jt. Yohanes kepala dapur udah kerja dari Juni 2023, gaji pokok 5 jt + tunjangan tetap 750rb, statusnya nikah anak 2. THR Natal mereka berapa, kapan paling telat cair, terus potongan PPh 21-nya gimana?

**Angka penguji:** Maria 20 Mei → 25 Des 2026 = 7 bln → 7/12 × 3.600.000 = Rp2.100.000 · Yohanes 42 bln → Rp5.750.000 · Total Rp7.850.000 · batas H-7 **Jumat, 18 Desember 2026**. THR dibayar Desember = Masa Pajak terakhir: PPh 21 dihitung ulang setahun (tarif Pasal 17), bukan TER (PMK 168/2023). Perkiraan kasar penguji bila gaji tetap sepanjang tahun dan tanpa iuran lain: Yohanes K/2 ±Rp175.600 di Desember; Maria (TK/0, mulai Mei) Rp0 karena setahun di bawah PTKP.

### SEBELUM (skill mati)

> Berikut perhitungannya (saya pakai aturan THR Keagamaan — Permenaker No. 6/2016 — dan skema PPh 21 TER/PMK 168/2023 yang berlaku per Jan 2024). Catatan: search internet saya sedang tidak bisa diakses sesi ini, jadi angka PPh 21 saya hitung dari tabel TER yang saya ingat — saran saya di bagian akhir untuk cross-check sebelum benar-benar dipotong ke karyawan.
>
> ## 1. Berapa THR masing-masing
>
> **Dasar hukum:** THR Keagamaan = 1 bulan upah (gaji pokok + tunjangan tetap) untuk masa kerja ≥12 bulan terus-menerus; proporsional (masa kerja/12 × 1 bulan upah) untuk masa kerja ≥1 bulan tapi <12 bulan.
>
> **Maria (barista, masuk 20 Mei 2026, gaji 3.600.000, tak ada tunjangan tetap disebut)**
> - Masa kerja sampai Hari Natal (25 Des 2026): 20 Mei → 25 Des 2026 = 7 bulan 5 hari ≈ 7,17 bulan
> - THR = (7,17/12) × 3.600.000 ≈ **Rp 2.150.000**
> - *(kalau perusahaan membulatkan ke bulan penuh saja tanpa hitung sisa hari, angkanya jadi 7/12 × 3.600.000 = Rp 2.100.000 — tinggal dipilih konvensi mana yang dipakai konsisten di perusahaan)*
>
> **Yohanes (kepala dapur, kerja sejak Juni 2023 → sudah >12 bulan terus-menerus)**
> - Berhak THR penuh = gaji pokok + tunjangan tetap = 5.000.000 + 750.000 = **Rp 5.750.000**
>
> ## 2. Batas waktu pembayaran
> THR Keagamaan wajib dibayar **paling lambat H-7 sebelum hari raya**, yaitu H-7 sebelum 25 Desember 2026 = **Jumat, 18 Desember 2026**. Telat bayar dikenai denda 5% dari total THR yang wajib dibayarkan, dan kewajiban pokoknya tetap harus dilunasi (tidak gugur).
>
> ## 3. Potongan PPh 21 atas THR (skema TER)
> THR termasuk penghasilan yang dipotong di bulan pembayarannya, digabung dengan gaji bulan itu, pakai tarif efektif (TER) sesuai kategori PTKP:
> - Kategori TER ditentukan status PTKP: Maria (asumsi TK/0, lajang, tanpa info status menikah) → **Kategori A**; Yohanes (K/2) → **Kategori B**.
> - Caranya: PPh21 = (TER × penghasilan bruto bulan itu termasuk THR) − (TER × gaji bulanan biasa tanpa THR).
>
> **Maria**
> - Gaji biasa 3.600.000/bulan → masuk bracket ≤5,4 jt kategori A → tarif 0% → PPh21 gaji biasa = 0
> - Gaji + THR = 3.600.000 + 2.150.000 = 5.750.000 → masuk bracket kategori A di atas 5,4 jt → tarif sekitar 0,5%
> - PPh21 total bulan itu ≈ 5.750.000 × 0,5% = **Rp 28.750** → itu semua "milik" THR → **THR Maria dipotong ≈ Rp 28.750**, THR bersih ≈ Rp 2.121.250
>
> **Yohanes**
> - Gaji biasa 5.750.000/bulan (pokok+tunjangan) → di kategori B ini masih masuk bracket 0% (ambang kategori B lebih tinggi dari A) → PPh21 gaji biasa = 0
> - Gaji + THR = 5.750.000 + 5.750.000 = 11.500.000 → masuk bracket kategori B sekitar 2–2,5%
> - PPh21 total bulan itu ≈ 11.500.000 × 2,5% = **Rp 287.500** → **THR Yohanes dipotong ≈ Rp 287.500**, THR bersih ≈ Rp 5.462.500
>
> **Catatan penting soal PPh 21 ini:**
> 1. Angka tarif TER (0,5% dan 2,5%) saya ambil dari tabel Lampiran PMK 168/2023 berdasar ingatan saya, bukan dari pengecekan ulang live — batas-batas bracket TER itu banyak baris dan presisi, jadi mohon cocokkan sekali lagi dengan tabel resmi (atau software payroll/aplikasi pajak yang dipakai) sebelum benar-benar dipotong ke slip gaji.
> 2. Di bulan Desember (bulan terakhir tahun pajak), biasanya ada rekonsiliasi akhir tahun — PPh 21 Januari–November yang sudah dipotong pakai TER dihitung ulang pakai tarif progresif Pasal 17 setahun penuh, lalu selisihnya (kurang/lebih bayar) disetarakan di pemotongan Desember. Jadi potongan final atas THR Desember bisa sedikit berbeda dari estimasi TER murni di atas, tergantung total penghasilan setahun masing-masing karyawan.
> 3. Saya asumsikan Maria berstatus TK/0 (lajang) karena tidak disebutkan — kalau ternyata dia sudah menikah/punya tanggungan, kategori TER-nya berubah dan potongannya ikut berubah.
>
> Kalau kafe pakai software payroll (Gadjian, Talenta, dll.) atau mau saya buatkan rekap slip THR kedua karyawan dalam format siap cetak, tinggal bilang.

### SESUDAH (skill 1.0.9 aktif)

> Sudah saya hitung pakai skill THR (Permenaker 6/2016 + aturan 2026). Natal 2026 jatuh Jumat, 25 Desember 2026 → **batas bayar THR paling lambat H‑7 = Jumat, 18 Desember 2026** (kalau telat, kena denda 5% dari total THR, dan THR tetap wajib dibayar penuh).
>
> ### A. REKAP PER ORANG — KHUSUS PEMILIK/HR (jangan ditempel ke grup)
> **Rincian THR Natal 2026**
> Hari raya: Jumat, 25 Des 2026 · Batas bayar (H‑7): **Jumat, 18 Des 2026** · Rencana bayar: 18 Des 2026
>
> | Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR |
> |---|---|---:|---:|---|---:|
> | Maria | Tetap | 7 bln (20 Mei → 25 Des 2026) | Rp 3.600.000 | 7/12 × upah (belum 12 bulan) | **Rp 2.100.000** |
> | Yohanes | Tetap | 42 bln (sejak Jun 2023) | Rp 5.750.000 (gaji pokok 5jt + tunjangan tetap 750rb) | ≥12 bulan → 1× upah penuh | **Rp 5.750.000** |
> | **Total** | | | | | **Rp 7.850.000** |
>
> **Soal PPh 21:**
> - **Maria**: statusnya belum Anda sebutkan (lajang/menikah). Kalau TK/0 (lajang, belum punya tanggungan) dan penghasilannya cuma gaji pokok 3,6 jt, biasanya masih di bawah ambang TER sehingga potongan PPh 21 rutin **Rp 0** — tapi saya tidak mengasumsikan sepihak. Kasih tahu status PTKP-nya kalau mau saya hitung pasti.
> - **Yohanes** (K/2): karena THR-nya cair di **Desember**, bulan ini sekaligus jadi bulan **perhitungan ulang PPh 21 setahun penuh** (bukan sekadar TER bulanan biasa) — ini aturan baku Desember, bukan khusus kasus Yohanes. Jadi potongan PPh 21-nya baru pasti setelah direkap dengan total penghasilan setahunnya (gaji 12 bulan + THR + tunjangan lain) dikurangi PTKP K/2, lalu dikenai tarif Pasal 17. Untuk angka presisi, idealnya pakai skill `pph21-ter` (belum terpasang di sini) atau dihitung manual oleh pembukuan/akuntan Anda di akhir Desember. Kalau mau saya bantu estimasi kasar manual sekarang (bukan angka final SPT), tinggal bilang.
>
> Catatan tambahan:
> - THR bukan dasar iuran BPJS.
> - Rekap tersimpan di `/opt/ochome/.openclaw/workspace/rekap-thr-natal-2026.csv`, data mentah di `karyawan-thr-natal-2026.csv` — mau saya hapus setelah ini selesai?
>
> ### B. TEKS GRUP — draf untuk Anda tempel sendiri (tanpa nominal per orang)
> ```
> Yth. Rekan-rekan karyawan,
>
> Menyambut Natal 2026, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan paling lambat Jumat, 18 Desember 2026 (7 hari sebelum hari raya).
>
> Ketentuan besaran THR (Permenaker 6/2016):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
> • Masa kerja 1 s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.
>
> Rincian THR masing-masing akan dikirim secara PRIBADI melalui HR/keuangan. Ada pertanyaan tentang THR Anda, silakan hubungi HR/keuangan langsung.
>
> Selamat menyambut Natal. Terima kasih atas kerja keras Bapak/Ibu.
> ```
>
> Nominal per orang saya pisahkan untuk pesan pribadi, karena gaji/THR adalah data pribadi karyawan — teks grup di atas sengaja tidak menyebut angka. Teks ini siap Anda tempel sendiri ke grup.
>
> Mau saya lanjutkan hitung estimasi PPh 21 Yohanes secara manual (perkiraan kasar), atau tunggu status PTKP Maria dulu?

**Nilai:** SEBELUM **5** · SESUDAH **8**
- SEBELUM: Angka utama THR Maria Rp2.150.000 memakai masa kerja pecahan 7,17 bulan (Rp2.100.000 hanya disebut sebagai alternatif, membingungkan pemilik awam). PPh 21 dihitung dengan TER bulan Desember (Maria Rp28.750, Yohanes Rp287.500) dan disajikan sebagai potongan, padahal Desember wajib dihitung ulang setahun; perkiraan setahun penguji: Maria Rp0, Yohanes ±Rp175.600. Ada catatan bahwa Desember "bisa sedikit berbeda", tetapi angka yang ditampilkan tetap menyesatkan. Menyebut "search internet saya sedang tidak bisa diakses". Durasi 367 detik.
- SESUDAH: THR, total, H-7, dan denda 5% benar. PPh 21 dijelaskan dengan benar: THR Desember ikut perhitungan ulang setahun (Pasal 17), Maria TK/0 kemungkinan Rp0, tanpa angka karangan. Kurang: tidak memberi perkiraan angka untuk Yohanes walau data K/2 dan gaji ada; kata proses "pakai skill THR" dan "skill `pph21-ter` (belum terpasang di sini)"; path ditampilkan.
- **Skill/script terpakai?** Ya: SKILL.md, `thr.py` (peringatan Masa Pajak Terakhir dari script disampaikan).

---

## Skenario 3: Normal ketiga: tukang harian lepas + minta nominal per orang di grup WA

**Pesan:**

> Toko bangunan saya mau bagi THR lebaran 2027 (10 Maret 2027). Ada 2 orang: Pak Slamet tukang harian lepas, kerja sejak 4 Mei 2026, upahnya per bulan beda2: Mei 2,4jt, Juni 2,6jt, Juli 2,5jt, Agustus 2,8jt, September 2,7jt, Oktober 2,6jt. Terus Rini admin tetap, gaji 4jt, kerja dari 2023. Tolong hitungin THR nya, terus bikinin pengumuman buat grup WA karyawan, sebutin masing2 dapat berapa biar transparan.

**Angka penguji:** Pak Slamet 4 Mei 2026 → 10 Mar 2027 = 10 bln; rata-rata upah 6 bulan yang ada = Rp2.600.000 → 10/12 × 2.600.000 = Rp2.166.667 · Rini Rp4.000.000 · Total Rp6.166.667 · H-7 Rabu 3 Maret 2027.

### SEBELUM (skill mati)

> Oke, saya hitungin dulu basis hukumnya (sesuai aturan THR Keagamaan - Permenaker No. 6/2016), baru saya buatin pengumumannya.
>
> ## Perhitungan THR
>
> **Rini (Admin Tetap, gaji 4jt, kerja sejak 2023)**
> Masa kerja per 10 Maret 2027 sudah jauh di atas 12 bulan → berhak THR penuh **1x gaji bulanan**.
> → **THR Rini = Rp 4.000.000**
>
> **Pak Slamet (Tukang Harian Lepas, mulai 4 Mei 2026)**
> - Masa kerja per 10 Maret 2027: dari 4 Mei 2026 ke 10 Maret 2027 = **genap 10 bulan** (kurang dari 12 bulan).
> - Karena statusnya harian lepas dengan upah tidak tetap dan masa kerja <12 bulan, aturannya THR dihitung **proporsional dari rata-rata upah selama masa kerja**, bukan dari gaji bulan terakhir saja.
> - Rumus: `(masa kerja ÷ 12) × rata-rata upah`
>
> Data upah yang sudah ada (Mei–Okt 2026, 6 bulan):
> | Bulan | Upah |
> |---|---|
> | Mei | 2.400.000 |
> | Jun | 2.600.000 |
> | Jul | 2.500.000 |
> | Agu | 2.800.000 |
> | Sep | 2.700.000 |
> | Okt | 2.600.000 |
>
> Rata-rata 6 bulan ini = Rp 15.600.000 ÷ 6 = **Rp 2.600.000**
>
> Perhitungan sementara (estimasi hari ini):
> `10/12 × Rp 2.600.000 = Rp 2.166.667` ≈ **Rp 2.166.700**
>
> ⚠️ **Catatan penting**: Ini baru estimasi karena data upah bulan November 2026 s/d Februari 2027 belum ada (belum terjadi). Rata-rata final yang benar harus pakai upah 10 bulan penuh (Mei 2026 – Feb 2027). Saya saranin dihitung ulang sekitar Februari 2027 setelah semua data upah lengkap, baru diumumkan angka pastinya biar akurat.
>
> ---
>
> ## Teks Pengumuman untuk Grup WA
>
> ```
> *PENGUMUMAN THR LEBARAN 2027*
>
> Assalamualaikum / selamat siang rekan-rekan,
>
> Menyambut Hari Raya Idul Fitri yang jatuh pada *10 Maret 2027*, berikut rincian THR Keagamaan untuk kita semua, dihitung sesuai masa kerja masing-masing agar transparan:
>
> 1. *Rini (Admin)*
>    THR: *Rp 4.000.000*
>    (masa kerja sejak 2023, sudah di atas 12 bulan → THR penuh 1x gaji)
>
> 2. *Pak Slamet (Tukang)*
>    THR: *± Rp 2.166.700* (estimasi, akan dikonfirmasi final menjelang lebaran)
>    (masa kerja 10 bulan sejak Mei 2026 → dihitung proporsional 10/12 x rata-rata upah bulanan)
>
> THR akan dibayarkan selambat-lambatnya H-7 sebelum lebaran sesuai ketentuan.
>
> Terima kasih atas kerja keras dan dedikasinya selama ini. Selamat mempersiapkan hari raya 🙏
>
> Wassalamualaikum.
> ```
>
> Tinggal isi nama toko kalau mau dicantumkan, dan nanti sekitar Februari 2027 kabari saya lagi biar saya update angka final Pak Slamet pakai data upah lengkapnya.

### SESUDAH (skill 1.0.9 aktif)

> Sudah saya hitung pakai skill THR resmi (Permenaker 6/2016 + SE Menaker 2026). Berikut hasilnya:
>
> ### A. REKAP PER ORANG — KHUSUS PEMILIK/HR (rahasia, kirim per orang lewat pesan pribadi, jangan ditempel ke grup)
>
> **Rincian THR Idul Fitri 1448 H — Toko Bangunan**
> Hari raya: Rabu, 10 Maret 2027 · **Batas bayar (H-7): Rabu, 3 Maret 2027**
>
> | Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR |
> |---|---|---:|---:|---|---:|
> | Pak Slamet | Harian lepas | 10 bln | Rp 2.600.000 (rata-rata) | 10/12 × upah | **Rp 2.166.667** |
> | Rini | Tetap (PKWTT) | 50 bln | Rp 4.000.000 | ≥12 bln → 1 × upah | **Rp 4.000.000** |
> | **Total** | | | | | **Rp 6.166.667** |
>
> ⚠️ **Catatan penting:**
> - **Pak Slamet**: data upah yang Anda kasih cuma 6 bulan (Mei–Okt), padahal masa kerjanya sampai Lebaran nanti genap **10 bulan** (4 Mei 2026 s.d. 10 Mar 2027). Karena ini dihitung sekarang (Okt 2026) dan gaji Nov/Des/Jan/Feb belum terjadi, upah 1 bulan dipakai **rata-rata dari 6 bulan yang sudah ada** (Rp 2,6jt), lalu dikalikan 10/12. Kalau nanti pas mau bayar (awal Maret 2027) upah Nov–Feb ternyata beda jauh dari rata-rata ini, sebaiknya hitung ulang pakai rata-rata 10 bulan aktual biar lebih akurat.
> - PPh 21 belum dihitung untuk keduanya karena status PTKP belum diisi. Kalau mau sekalian, kasih tahu PTKP masing-masing (TK/0, K/1, dst).
> - THR wajib dibayar penuh, tidak dicicil, paling lambat H-7. Telat = denda 5% dari total THR.
>
> File rekap tersimpan di: `/opt/ochome/.openclaw/workspace/thr-2027-rekap.csv`
>
> ---
>
> ### B. TEKS GRUP — draf untuk Anda tempel sendiri ke grup WA karyawan
>
> Soal "sebutin masing-masing dapat berapa" — itu saya nggak bisa taruh di teks grup. Nominal dan rincian gaji/THR per orang itu data pribadi, jadi harus dikirim terpisah ke masing-masing orang (chat pribadi), bukan di grup bersama. Ini draf pengumuman grup tanpa nominal:
>
> ```
> Yth. Rekan-rekan karyawan Toko Bangunan,
>
> Menyambut Idul Fitri 1448 H, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan paling lambat Rabu, 3 Maret 2027 (7 hari sebelum hari raya).
>
> Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap, atau rata-rata upah untuk harian lepas).
> • Masa kerja 1 bulan s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.
>
> Rincian THR masing-masing (nominal dan potongan PPh 21, bila ada) akan dikirim secara PRIBADI kepada setiap karyawan. Mohon tidak membagikan rincian pribadi di grup. Ada pertanyaan soal THR Anda, langsung hubungi saya saja.
>
> Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu selama ini.
>
> Salam,
> Manajemen Toko Bangunan
> ```
>
> Teks ini siap Anda tempel sendiri ke grup — saya tidak kirim apa pun secara otomatis.
>
> Rincian per orang (Pak Slamet Rp 2.166.667, Rini Rp 4.000.000) silakan sampaikan lewat chat pribadi masing-masing ya. Mau saya buatkan draf pesan pribadinya juga?
>
> Satu lagi: file CSV data gaji (`thr-2027-karyawan.csv`) di workspace berisi data pribadi karyawan — mau saya hapus sekarang, atau disimpan?

**Nilai:** SEBELUM **6** · SESUDAH **8,5**
- SEBELUM: Hitungan benar dan jujur soal data upah yang belum lengkap. Tetapi pengumuman grup memuat nama dan THR tiap orang (data gaji pribadi dibagikan ke semua karyawan), angka Pak Slamet dibulatkan berbeda (Rp2.166.700 vs Rp2.166.667), batas bayar hanya "H-7" tanpa tanggal, tanpa denda 5%.
- SESUDAH: Angka benar, peringatan data upah 6 bulan vs masa kerja 10 bulan dijelaskan dengan bahasa awam. Pola tolak → padanan → tetap kerjakan berjalan: nominal per orang ditolak untuk grup dengan alasan privasi, teks grup tetap dibuat, rincian per orang dipisah dan ditawarkan draf pesan pribadi. Kurang: kata proses "pakai skill THR resmi", nama usaha karangan "Toko Bangunan", path ditampilkan.
- **Skill/script terpakai?** Ya: SKILL.md, `thr.py`.

---

## Skenario 4: Input kurang: 3 gaji, tanpa hari raya dan tanggal masuk

**Pesan:**

> thr karyawan sy brp ya? ada 3 org: Wawan gaji 3jt udh lama, Tini 3,5jt, Ujang baru masuk bln kemarin gajinya 2,8

**Acuan penguji:** hari raya tidak disebut, jadi masa kerja tidak bisa dihitung pasti. Bila untuk Lebaran 2027 (perkiraan 10 Maret 2027): Wawan Rp3.000.000 dan Tini Rp3.500.000 bila sudah ≥ 12 bulan; Ujang (masuk September 2026) 5-6 bulan → Rp1.166.667-1.400.000; batas bayar 3 Maret 2027.

### SEBELUM (skill mati)

> Oke, ini hitungan THR berdasarkan aturan (PP 36/2021): karyawan kerja ≥12 bulan dapat THR full 1x gaji, kurang dari itu dihitung proporsional (masa kerja/12 × gaji).
>
> Asumsi saya: Wawan & Tini sudah kerja ≥1 tahun ("udah lama"), jadi full. Ujang baru 1 bulan kerja, jadi prorata 1/12.
>
> - Wawan: 3.000.000 (full)
> - Tini: 3.500.000 (full)
> - Ujang: 2.800.000 × 1/12 = 233.333
>
> **Total THR: Rp 6.733.333**
>
> Kalau ternyata Wawan/Tini masa kerjanya belum genap 12 bulan, kasih tau aja lama kerjanya biar saya koreksi hitungannya.

### SESUDAH (skill 1.0.9 aktif)

> Perlu beberapa info dulu sebelum saya hitung THR-nya (sesuai aturan, THR itu berdasarkan hari raya mana dan masa kerja tiap orang):
>
> 1. THR ini untuk hari raya apa dan tanggalnya kapan? (Idul Fitri, Natal, dll — beserta tanggal persisnya)
> 2. **Wawan** "udah lama" — kira-kira mulai kerja tanggal/bulan/tahun berapa, atau sudah berapa tahun kerja?
> 3. **Tini** gaji 3,5jt — ia mulai kerja kapan / sudah berapa lama?
> 4. **Ujang** masuk bulan kemarin (Sept 2026) — tanggal pastinya berapa di bulan itu?
> 5. Ada tunjangan tetap (transport/makan bulanan tetap) di luar gaji pokok yang disebutkan, atau itu sudah total gaji bulanannya?
>
> Begitu saya dapat jawabannya, saya hitung THR ketiganya sekalian (termasuk batas bayar H-7).

**Nilai:** SEBELUM **4** · SESUDAH **6,5**
- SEBELUM: Bekerja dulu dan bertanya di akhir (perilaku yang diharapkan), tetapi **salah aturan**: masa kerja Ujang dihitung sampai hari ini (1 bulan → Rp233.333), padahal masa kerja dihitung sampai hari raya; total Rp6.733.333 menyesatkan dan merugikan karyawan. Hari raya tidak ditanyakan, tanpa batas H-7.
- SESUDAH: Tidak ada angka keliru; pertanyaannya tepat (hari raya & tanggal, tanggal masuk, tunjangan tetap) dalam satu pesan. Tetapi tidak menghitung apa pun dan bertanya 5 hal (melebihi acuan maks. 3); seharusnya memberi hitungan bersyarat dulu.
- **Skill/script terpakai?** Ya: hanya SKILL.md (script tidak dijalankan karena data wajib kurang).

---

## Verifikasi angka independen (penguji)

| Kasus | Hitung ulang penguji | Script skill (dijalankan penguji) | Balasan agent SESUDAH |
|---|---|---|---|
| Skenario 1 total | Rp12.441.666 | Rp12.441.666 | Rp12.441.666 (lokal & Telegram) |
| Skenario 1 masa kerja | 74 / 11 / 7 / 13 bln | sama | sama |
| Skenario 2 | Rp2.100.000 + Rp5.750.000 = Rp7.850.000; H-7 Jumat 18 Des 2026 | sama | sama |
| Skenario 3 | Rp2.166.667 + Rp4.000.000 = Rp6.166.667 | sama (+ ⚠️ 6 vs 10 bulan data) | sama |
| `tahun_hijriah.py 2027-03-10 --cek idul-fitri` | 1 Syawal 1448 H (tabular) | COCOK | "Idul Fitri 1448 H" |

Selisih: 0 di semua kasus.

## Perbaikan yang disarankan (urut dampak)
1. Input kurang: ubah aturan "tanyakan sekali, maks. 5 pertanyaan" menjadi "hitung dulu dengan asumsi yang disebut (mis. hari raya terdekat yang relevan, masa kerja ≥ 12 bulan untuk yang 'sudah lama'), lalu tanya maks. 3 hal di akhir".
2. Larang kata proses di balasan (skill, script, nama skill lain, "belum terpasang") dan tampilkan nama file saja, bukan path sandbox.
3. Tegaskan `[isi: nama usaha]` juga berlaku untuk nama generik buatan agent ("Bengkel Motor", "Toko Bangunan").
4. THR Desember: bila status PTKP dan gaji tetap diketahui, tawarkan perkiraan PPh 21 Desember yang ditandai "perkiraan" agar pertanyaan "PPh 21-nya gimana?" terjawab dengan angka.
