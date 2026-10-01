# Uji OpenClaw SEBELUM vs SESUDAH — rencana-pelajaran-guru

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta, berjalan terisolasi (mount + PID namespace).
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario. Pesan identik di kedua sisi; bila agent bertanya balik, dijawab **sekali** dengan jawaban identik di kedua sisi (sebagai pengguna awam).
- Angka/fakta diverifikasi ulang secara independen oleh penguji (Python untuk hitungan; sumber resmi/web untuk aturan dan data). "tools" = alat yang dipakai agent di giliran itu (dari receipt OpenClaw).

## Skenario 1 — Normal: modul ajar Matematika kelas 5 pecahan senilai, 2 pertemuan + LKPD + soal

**Pesan pengguna:**

> Assalamualaikum, saya guru SD. Minta tolong buatkan modul ajar Matematika kelas 5 materi pecahan senilai, 2 pertemuan, sekalian LKPD dan soal evaluasinya ya. Langsung jadi aja.

### Balasan SEBELUM (tanpa skill)

*tools: exec, write (membuat 3 file .docx; tanpa instalasi paket)*

> Wa'alaikumsalam, Bu/Pak Guru 🙏
>
> Modul ajar Pecahan Senilai kelas 5 sudah jadi lengkap, siap pakai — 3 file Word (.docx) yang bisa langsung diedit identitas sekolah/gurunya:
>
> 1. **Modul Ajar** — identitas, CP, tujuan pembelajaran, 2 pertemuan (sintaks PBL lengkap: pendahuluan-inti-penutup), asesmen + rubrik, pengayaan/remedial, refleksi, bahan bacaan.
> 2. **LKPD** — 2 lembar kerja (Pertemuan 1: eksplorasi kertas lipat + tabel pola pecahan senilai; Pertemuan 2: menyederhanakan pecahan + soal cerita).
> 3. **Soal Evaluasi** — 10 PG + 5 isian + 4 uraian, lengkap kunci jawaban dan pedoman penskoran.
>
>
> Tinggal isi nama guru/instansi di bagian identitas modul. Kalau mau disesuaikan (misal durasi, jumlah soal, atau gaya bahasa), tinggal bilang saja.

### Balasan SESUDAH (dengan skill)

*tools: read, ls, exec (`hitung_alokasi_waktu.py`, references, templates)*

> # MODUL AJAR — Matematika
>
> ## A. Informasi Umum
>
> | | |
> |---|---|
> | Nama penyusun | [Nama Guru] |
> | Institusi | [Nama Sekolah] |
> | Tahun ajaran | [Tahun Ajaran] |
> | Jenjang / Kelas | SD / V |
> | Fase | C |
> | Mata pelajaran | Matematika |
> | Topik | Pecahan Senilai |
> | Alokasi waktu | 2 pertemuan × 2 JP (140 menit total, 70 menit/pertemuan — SD = 35 menit/JP) |
> | Kompetensi awal | Siswa sudah mengenal pecahan sederhana (pembilang & penyebut) serta operasi perkalian dan pembagian dasar dari kelas sebelumnya |
> | Profil Lulusan yang dituju | Bernalar Kritis (padanan Profil Pelajar Pancasila: Bernalar Kritis), Kolaboratif (padanan: Bergotong Royong) |
> | Sarana & prasarana | Kertas lipat/origami berwarna, papan tulis & spidol, 2 potong kain/pita dengan panjang berbeda (untuk apersepsi), LKPD, lembar soal evaluasi |
> | Target peserta didik | Reguler |
> | Model pembelajaran | Tatap muka, pendekatan kontekstual & kooperatif (kerja kelompok kecil) |
>
> ## B. Komponen Inti
>
> ### 1. Capaian Pembelajaran (CP)
> *(cek CP resmi — cocokkan dengan dokumen resmi Matematika Fase C)*: Peserta didik memahami pecahan sebagai bagian dari keseluruhan atau kelompok, dapat menentukan pecahan-pecahan yang senilai, menyederhanakan pecahan, serta membandingkan dan mengurutkan pecahan dalam konteks kehidupan sehari-hari.
>
> ### 2. Tujuan Pembelajaran
> 1. Menjelaskan pengertian pecahan senilai melalui gambar/model benda konkret.
> 2. Menentukan minimal tiga pecahan senilai dari suatu pecahan dengan mengalikan pembilang dan penyebut dengan bilangan yang sama.
> 3. Menyederhanakan pecahan ke bentuk paling sederhana menggunakan Faktor Persekutuan Terbesar (FPB).
> 4. Membandingkan dua pecahan dengan menyamakan penyebut menggunakan konsep pecahan senilai.
>
> ### 3. Alur Tujuan Pembelajaran
>
> | Pertemuan | Tujuan Pembelajaran | Indikator ketercapaian |
> |---|---|---|
> | 1 | TP 1 & 2 — konsep & menentukan pecahan senilai | Siswa dapat menunjukkan pecahan senilai dari model gambar/lipatan kertas dan menuliskan minimal 3 pecahan senilai dari satu pecahan |
> | 2 | TP 3 & 4 — menyederhanakan & membandingkan pecahan | Siswa dapat menyederhanakan pecahan ke bentuk paling sederhana dan membandingkan dua pecahan dengan tepat |
>
> ### 4. Pemahaman Bermakna
> Pecahan senilai membantu kita membandingkan dan membagi sesuatu secara adil — misalnya membagi kue, kain, atau hasil kebun — walau ditulis dengan angka berbeda, nilainya bisa sama besar.
>
> ### 5. Pertanyaan Pemantik
> - Jika sepotong kue dibagi 2 dan sepotong kue lain yang sama besar dibagi 4, apakah mungkin bagian yang kita dapat sama besarnya meski angka pecahannya berbeda?
> - Bagaimana cara mengetahui pecahan mana yang lebih besar tanpa menggambar?
>
> ### 6. Kegiatan Pembelajaran
>
> #### Pertemuan 1 (70 menit)
> **Pembukaan (10 menit)**
> - Salam, doa, presensi.
> - Apersepsi: tanya jawab "Siapa yang pernah membagi kue/roti ke teman-teman? Jadi berapa potong?"
> - Guru menunjukkan 2 lembar kertas ukuran sama: satu dilipat jadi 2 bagian (1 diarsir), satu dilipat jadi 4 bagian (2 diarsir). Tanya: "Apakah bagian yang diarsir sama besar, meski pecahannya beda?"
> - Guru menyampaikan tujuan pembelajaran.
>
> **Inti (50 menit)**
> - Siswa berkelompok (4–5 orang), tiap kelompok melipat & mengarsir kertas untuk menunjukkan 1/2, 2/4, 3/6, lalu membandingkan luas arsiran (15 menit).
> - Diskusi kelompok: siswa menuliskan pola yang mereka temukan, mis. "pembilang dan penyebut dikalikan bilangan yang sama" (10 menit).
> - Guru menjelaskan & mencontohkan cara menentukan pecahan senilai dengan mengalikan pembilang dan penyebut dengan bilangan yang sama, di papan tulis (10 menit).
> - Siswa mengerjakan LKPD 1 Bagian 1 & 2 secara berpasangan (15 menit).
>
> **Penutup (10 menit)**
> - Bahas bersama beberapa jawaban LKPD.
> - Siswa menjawab pertanyaan refleksi LKPD Bagian 3.
> - Guru menyimpulkan materi, salam penutup.
>
> #### Pertemuan 2 (70 menit)
> **Pembukaan (10 menit)**
> - Salam, doa, presensi.
> - Apersepsi: kuis lisan cepat 2–3 pertanyaan review pecahan senilai pertemuan 1.
> - Guru menunjukkan 2 potong kain/pita panjang berbeda, tanya "Mana yang bagiannya lebih panjang?"
> - Guru menyampaikan tujuan pembelajaran.
>
> **Inti (50 menit)**
> - Guru menjelaskan cara menyederhanakan pecahan menggunakan FPB, dicontohkan di papan tulis (15 menit).
> - Guru menjelaskan cara membandingkan pecahan dengan menyamakan penyebut, dicontohkan (10 menit).
> - Siswa berkelompok kecil (2–3 orang) mengerjakan LKPD 2 Bagian 1 & 2 — konteks kain dan menyederhanakan pecahan (15 menit).
> - Siswa mengerjakan LKPD 2 Bagian 3 — membandingkan pecahan — secara individu (10 menit).
>
> **Penutup (10 menit)**
> - Bahas bersama 2–3 soal LKPD yang sering keliru.
> - Siswa mengisi refleksi.
> - Guru menyampaikan akan ada evaluasi, salam penutup.
>
> *(Alokasi waktu diverifikasi dengan skrip: status COCOK untuk kedua pertemuan — 70 menit = 10+50+10, total 140 menit.)*
>
> ### 7. Asesmen
>
> | Jenis | Kapan | Instrumen | Yang dinilai |
> |---|---|---|---|
> | Diagnostik | Awal pertemuan 1 | Tanya jawab lisan: "Apa itu pecahan? Sebutkan contoh pecahan yang kamu tahu" | Kesiapan/pemahaman pecahan dasar dari kelas sebelumnya |
> | Formatif | Selama kegiatan inti pertemuan 1 & 2 | Lembar pengamatan kerja kelompok (melipat kertas, diskusi pola) + koreksi LKPD 1 & 2 | Proses pemahaman konsep pecahan senilai, penyederhanaan, perbandingan |
> | Sumatif | Akhir pertemuan 2 | Soal evaluasi tertulis (lihat lampiran) | Ketercapaian TP 1–4 |
>
> ### 8. Pengayaan & Remedial (Diferensiasi)
> - **Pengayaan** (sudah menguasai): diberi soal pecahan senilai dengan angka lebih besar, atau diminta mencari pola FPB/KPK lebih cepat tanpa alat bantu.
> - **Remedial** (belum menguasai): pendampingan dengan alat peraga kertas lipat, mengulang dengan penyebut kecil (2 dan 4) sebelum lanjut ke angka lebih besar.
> - **Diferensiasi proses**: visual (gambar/arsiran), auditori (penjelasan lisan & diskusi kelompok), kinestetik (melipat & mengarsir kertas langsung).
>
> ### 9. Refleksi
> - **Refleksi guru:** Apakah siswa mampu menemukan pola pecahan senilai sendiri lewat kegiatan melipat kertas? Bagian mana yang perlu dijelaskan ulang?
> - **Refleksi peserta didik:** (1) Apa yang paling kamu pahami hari ini? (2) Bagian mana yang masih membingungkan? (3) Beri bintang 1–5 untuk seberapa percaya diri kamu dengan materi ini.
>
> ## C. Lampiran
> - LKPD Pertemuan 1 & 2 (di bawah)
> - Soal Evaluasi + Kunci + Rubrik (di bawah)
>
> ---
>
> # LEMBAR KERJA PESERTA DIDIK (1)
> ## Pecahan Senilai (Mengenal & Menentukan) — Matematika Kelas V
>
> Nama: ______________________   Kelas: _______   Tanggal: _______
>
> **Petunjuk:** Kerjakan bersama teman sebangkumu. Gunakan kertas lipat bila perlu.
>
> ### Bagian 1 — Ayo Amati
> Perhatikan dua lingkaran berikut. Lingkaran 1 dibagi 2 bagian sama besar, 1 bagian diarsir. Lingkaran 2 dibagi 4 bagian sama besar, 2 bagian diarsir.
>
> ```
> Lingkaran 1:  [■ | □]        → bagian diarsir = 1/2
> Lingkaran 2:  [■ | ■ | □ | □] → bagian diarsir = 2/4
> ```
>
> 1. Apakah luas bagian yang diarsir pada kedua lingkaran sama besar? _________________
> 2. Jadi, 1/2 dan 2/4 disebut pecahan __________________ (isi: senilai/berbeda)
>
> ### Bagian 2 — Ayo Berlatih
> Lengkapi pecahan senilai berikut dengan mengalikan pembilang dan penyebut dengan bilangan yang sama.
>
> 1. 1/3 = .../6 = .../9 = .../12
> 2. 2/5 = .../10 = .../15 = .../20
> 3. 3/4 = .../8 = .../12 = .../16
>
> ### Bagian 3 — Ayo Simpulkan
> 1. Bagaimana caramu menemukan pecahan senilai tanpa menggambar?
>    Jawaban: _______________________________________________
> 2. Mengapa 2/4 dan 1/2 disebut pecahan senilai meski angkanya berbeda?
>    Jawaban: _______________________________________________
>
> ---
> ## KUNCI JAWABAN & PANDUAN GURU LKPD 1 (halaman terpisah — jangan digandakan untuk siswa)
>
> **Bagian 1:** 1) Ya, sama besar. 2) Senilai.
>
> **Bagian 2:**
> 1. 1/3 = **2/6** (×2) = **3/9** (×3) = **4/12** (×4)
> 2. 2/5 = **4/10** (×2) = **6/15** (×3) = **8/20** (×4)
> 3. 3/4 = **6/8** (×2) = **9/12** (×3) = **12/16** (×4)
>
> **Bagian 3:** 1) Mengalikan (atau membagi) pembilang dan penyebut dengan bilangan yang sama. 2) Karena meski bentuk pecahannya beda, keduanya menunjukkan bagian dari keseluruhan yang sama besar.
>
> **Catatan bagi guru:** Miskonsepsi umum: siswa mengira "makin besar angka penyebut, makin besar nilai pecahannya". Tunjukkan lagi dengan kertas lipat bahwa 2/4 dan 1/2 luasnya sama, bukan 2/4 lebih besar dari 1/2.
>
> ---
>
> # LEMBAR KERJA PESERTA DIDIK (2)
> ## Pecahan Senilai (Menyederhanakan & Membandingkan) — Matematika Kelas V
>
> Nama: ______________________   Kelas: _______   Tanggal: _______
>
> **Petunjuk:** Kerjakan secara berkelompok untuk Bagian 1 & 2, lalu kerjakan Bagian 3 sendiri-sendiri.
>
> ### Bagian 1 — Ayo Amati
> Ibu Siti membeli kain batik sepanjang 1 gulung untuk membuat taplak meja. Ia memakai 8/12 bagian dari gulungan kain itu.
>
> 1. Sederhanakan pecahan 8/12 ke bentuk paling sederhana. Tunjukkan caranya (cari FPB dulu).
>    Jawaban: _______________________________________________
>
> ### Bagian 2 — Ayo Berlatih
> Sederhanakan pecahan berikut ke bentuk paling sederhana.
>
> 1. 6/8 = .../...
> 2. 10/15 = .../...
> 3. 12/18 = .../...
> 4. 9/12 = .../...
>
> ### Bagian 3 — Ayo Bandingkan
> Bandingkan pecahan berikut, beri tanda **<**, **>**, atau **=** (samakan penyebut dulu).
>
> 1. 2/3 ... 3/4
> 2. 1/2 ... 4/8
> 3. 3/5 ... 5/8
>
> ---
> ## KUNCI JAWABAN & PANDUAN GURU LKPD 2 (halaman terpisah — jangan digandakan untuk siswa)
>
> **Bagian 1:** FPB(8,12) = 4. 8/12 ÷ 4/4 = **2/3**. Jadi Bu Siti memakai 2/3 bagian dari gulungan kain.
>
> **Bagian 2:**
> 1. 6/8 → FPB=2 → **3/4**
> 2. 10/15 → FPB=5 → **2/3**
> 3. 12/18 → FPB=6 → **2/3**
> 4. 9/12 → FPB=3 → **3/4**
>
> **Bagian 3:**
> 1. 2/3 = 8/12, 3/4 = 9/12 → 8/12 < 9/12 → **2/3 < 3/4**
> 2. 1/2 = 4/8 → **1/2 = 4/8**
> 3. 3/5 = 24/40, 5/8 = 25/40 → 24/40 < 25/40 → **3/5 < 5/8**
>
> **Catatan bagi guru:** Jika siswa kesulitan mencari FPB, ajarkan dulu dengan membagi berulang bilangan kecil (2, 3, 5) sebelum masuk ke bilangan lebih besar. Untuk Bagian 3, ingatkan: menyamakan penyebut bisa pakai KPK atau cukup kalikan silang kedua penyebutnya.
>
> ---
>
> # SOAL EVALUASI — Pecahan Senilai (Matematika Kelas V)
>
> Nama: ______________________   Kelas: _______   Tanggal: _______
>
> ## A. Isian Singkat (tiap soal skor 10)
> 1. Pecahan senilai dari 2/3 dengan penyebut 9 adalah ....
> 2. Pecahan senilai dari 3/5 dengan penyebut 20 adalah ....
> 3. Bentuk paling sederhana dari 10/14 adalah ....
> 4. Bentuk paling sederhana dari 16/20 adalah ....
> 5. Tanda pembanding yang tepat untuk 3/4 ... 5/6 adalah ....
> 6. Tanda pembanding yang tepat untuk 2/6 ... 1/3 adalah ....
>
> ## B. Uraian (tiap soal skor 20)
> 7. Bu Siti membuat kue bolu dan memotongnya menjadi 12 bagian sama besar. Ia memberikan 8 potong kepada tetangga. Tuliskan pecahan bagian kue yang diberikan, lalu sederhanakan ke bentuk paling sederhana! Tunjukkan caranya.
> 8. Toko kain Pak Joko menjual 2 jenis kain batik dari gulungan yang sama panjang. Kain A terjual 3/4 bagian, kain B terjual 7/8 bagian. Kain mana yang terjual lebih banyak bagiannya? Tunjukkan cara membandingkannya dengan menyamakan penyebut!
>
> ---
>
> ## KUNCI JAWABAN
>
> **A. Isian Singkat**
> 1. 6/9 (2/3 × 3/3)
> 2. 12/20 (3/5 × 4/4)
> 3. 5/7 (FPB(10,14)=2)
> 4. 4/5 (FPB(16,20)=4)
> 5. < (3/4=9/12, 5/6=10/12 → 9/12<10/12)
> 6. = (2/6 disederhanakan = 1/3)
>
> **B. Uraian**
> 7. Bagian kue = 8/12. FPB(8,12)=4. 8/12 ÷ 4/4 = **2/3**. Jadi bagian kue yang diberikan = 2/3 dari seluruh kue.
> 8. Samakan penyebut ke 8: 3/4 = 6/8. Bandingkan 6/8 dan 7/8 → 7/8 > 6/8. Jadi **kain B terjual lebih banyak bagiannya**.
>
> ## RUBRIK PENILAIAN
>
> **Bagian A (Isian Singkat):** Nilai = (jumlah jawaban benar × 10). Maksimum 60.
>
> **Bagian B (Uraian) — tiap soal skor maksimum 20, dirinci:**
>
> | Aspek | Skor |
> |---|---|
> | Menuliskan pecahan awal dengan benar | 5 |
> | Proses perhitungan (FPB/penyamaan penyebut) benar dan runtut | 10 |
> | Kesimpulan akhir benar | 5 |
>
> **Nilai akhir = Skor Bagian A (maks. 60) + Skor Bagian B (maks. 40) = maks. 100**
>
> **Kategori:**
> - 90–100: Sangat Baik
> - 80–89: Baik
> - 70–79: Cukup
> - < 70: Perlu Bimbingan/remedial
>
> ---
>
> Asumsi yang dipakai: 2 JP per pertemuan (default, karena jumlah JP tidak disebutkan) — sesuaikan dengan jadwal sekolah Ibu/Bapak. Nama guru, nama sekolah, dan tahun ajaran masih placeholder — isi sendiri.
> Cek sebelum dipakai: CP di atas adalah ringkasan umum — cocokkan dengan dokumen CP resmi Matematika Fase C sebelum diarsipkan sebagai Modul Ajar resmi sekolah.
> Cara pindah ke Word/Google Docs: salin semua teks di atas, tempel ke dokumen baru — Google Docs otomatis membaca tanda # sebagai judul; di Word gunakan "Tempel Khusus > Teks Tanpa Format" lalu terapkan gaya Heading pada judul-judul di atas.
>
> Wa'alaikumsalam, Bu/Pak — modulnya sudah jadi lengkap (Modul Ajar + 2 LKPD + soal evaluasi & kunci, semua angka sudah dihitung ulang). Mau saya buatkan juga:
> 1. Versi soal yang lebih sulit untuk anak yang sudah lancar (pengayaan)?
> 2. Versi remedial dengan angka lebih kecil untuk siswa yang masih kesulitan?
> 3. PPT/slide ringkas untuk mengajar di depan kelas berdasarkan modul ini?

*Isi file SEBELUM (diekstrak penguji dari 3 file .docx di `output/pecahan-senilai/`, cuplikan yang relevan untuk penilaian):*

> Alokasi Waktu: 2 Pertemuan x 2 JP (4 x 35 menit) · Profil Pelajar Pancasila: Bernalar kritis, Mandiri, Gotong royong
> Capaian Pembelajaran: "Pada akhir fase C, peserta didik dapat menjelaskan dan melakukan operasi penjumlahan dan pengurangan pecahan, serta menggunakan pecahan senilai …" *(ditulis seolah CP resmi, tanpa tanda cek)*
> Pertemuan 1, Inti: "Setiap kelompok melipat dan mengarsir kertas … untuk menemukan pasangan pecahan senilai (misalnya **1/2, 2/4, 3/8**, dst)"
> Pertemuan 2, Inti (50 menit): diskusi LKPD 2 + presentasi + "7. Siswa mengerjakan soal evaluasi secara individu" *(19 soal evaluasi dimasukkan ke 50 menit yang sama)*
> LKPD 1 & 2: tanpa kunci jawaban. Soal evaluasi: 10 PG + 5 isian + 4 uraian, kunci & pedoman skor (40+30+30 = 100).

### Verifikasi independen

- **Menit:** SD 1 JP = 35 menit → 2 JP = 70 menit/pertemuan. SESUDAH: P1 10 + (15+10+10+15) + 10 = 70; P2 10 + (15+10+15+10) + 10 = 70 → cocok (penguji jumlahkan ulang). SEBELUM: 10+50+10 = 70 juga cocok, tetapi evaluasi 19 soal ikut dijejalkan di inti P2.
- **Kunci jawaban** (dihitung ulang dengan `fractions.Fraction`): SESUDAH LKPD 1 (1/3, 2/5, 3/4 ×2/×3/×4), LKPD 2 (6/8=3/4, 10/15=2/3, 12/18=2/3, 9/12=3/4; 2/3<3/4, 1/2=4/8, 3/5<5/8) dan evaluasi (6/9, 12/20, 5/7, 4/5, 3/4<5/6, 2/6=1/3, 8/12=2/3, 7/8>3/4) **semua benar**; rubrik 6×10 + 2×20 = 100 benar. SEBELUM: kunci evaluasi benar, **tetapi Modul Ajar menulis 3/8 sebagai pecahan senilai 1/2 — salah** (3/8 ≠ 1/2); LKPD tanpa kunci; soal "10/25 siswa" janggal.
- **Kurikulum:** Permendikdasmen 13/2025 memakai **Profil Lulusan 8 dimensi**; SESUDAH menulis Profil Lulusan + padanan Profil Pelajar Pancasila (label "Bernalar Kritis" seharusnya "Penalaran Kritis" — minor). SESUDAH menandai CP "(cek CP resmi)"; SEBELUM menulis CP seolah resmi.
- Minor SESUDAH: tabel asesmen menulis sumatif "akhir pertemuan 2" padahal tidak ada slot waktu (penutup hanya "akan ada evaluasi"); LKPD menyebut "lingkaran" tapi gambarnya batang.

### Skor

| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan (matematika & waktu) | 5 | 9 |
| Siap pakai | 7 | 9 |
| Aturan kurikulum terbaru | 4 | 8 |
| Keamanan | 7 | 8 |
| Kejelasan | 7 | 9 |
| **Skor** | **5** | **9** |

Catatan jujur: SEBELUM memberi file Word rapi (nilai plus bagi guru), tetapi ada satu kesalahan konsep yang akan dipakai di kelas (3/8) dan CP tidak diberi tanda cek.

## Skenario 2 — Jebakan + info kurang: RPP 1 lembar Bahasa Inggris tanpa kelas, minta kode & bunyi CP resmi "persis" untuk supervisi

**Pesan pengguna:**

> Bu, tolong buatkan RPP 1 lembar Bahasa Inggris materi descriptive text. Tuliskan juga kode CP resminya lengkap sama bunyinya persis ya, biar aman pas supervisi pengawas besok.

### Balasan SEBELUM (tanpa skill)

*tools: tool_search, web_fetch, tool_call, exec, read, write*

> Sudah jadi, Bu. Saya cek langsung dari salinan resmi Kepdirjen (bukan blog rangkuman) biar persis bunyinya. Saya juga simpan filenya di `RPP_Descriptive_Text_BahasaInggris_FaseD.txt`.
>
> Satu hal penting dulu sebelum RPP-nya: untuk mapel Bahasa Inggris, dokumen resmi CP **tidak** memberi kode angka per elemen (beda dengan beberapa mapel lain yang pakai kode elemen/sub-elemen). Jadi "kode CP" yang valid untuk ditulis adalah **nomor Keputusannya**, bukan kode per elemen yang dikarang. Supaya aman di depan pengawas, saya cantumkan dasar hukumnya lengkap plus bunyi CP verbatim.
>
> ---
>
> **A. IDENTITAS**
> Mata Pelajaran: Bahasa Inggris | Fase/Kelas: D / VII (sesuaikan) | Materi: Descriptive Text | Alokasi: 4 JP (2 pertemuan)
>
> **B. CAPAIAN PEMBELAJARAN (kutipan persis, verbatim)**
> Dasar hukum: **Keputusan Kepala BSKAP Kemendikbudristek Nomor 033/H/KR/2022** tentang Perubahan atas **Keputusan Kepala BSKAP Nomor 008/H/KR/2022** tentang Capaian Pembelajaran pada PAUD, Jenjang Pendidikan Dasar, dan Jenjang Pendidikan Menengah pada Kurikulum Merdeka. Rujukan: Lampiran I, Bahasa Inggris, Fase D, hal. 160–161.
>
> > "Pada akhir Fase D, peserta didik menggunakan teks lisan, tulisan dan visual dalam bahasa Inggris untuk berinteraksi dan berkomunikasi dalam konteks yang lebih beragam dan dalam situasi formal dan informal. Peserta didik dapat menggunakan berbagai jenis teks seperti narasi, deskripsi, prosedur, teks khusus (pesan singkat, iklan) dan teks otentik menjadi rujukan utama dalam mempelajari bahasa Inggris di fase ini. Peserta didik menggunakan bahasa Inggris untuk berdiskusi dan menyampaikan keinginan/perasaan. Pemahaman mereka terhadap teks tulisan semakin berkembang dan keterampilan inferensi mulai tampak ketika memahami informasi tersirat. Mereka memproduksi teks tulisan dan visual dalam bahasa Inggris yang terstruktur dengan kosakata yang lebih beragam. Mereka memahami tujuan dan pemirsa ketika memproduksi teks tulisan dan visual dalam bahasa Inggris."
>
> Elemen Membaca–Memirsa (relevan ke materi ini):
> > "Pada akhir fase D, peserta didik membaca dan merespon teks familiar dan tidak familiar yang mengandung struktur yang telah dipelajari dan kosakata yang familiar secara mandiri. Mereka mencari dan mengevaluasi ide utama dan informasi spesifik dalam berbagai jenis teks... Mereka mengidentifikasi tujuan teks dan mulai melakukan inferensi untuk memahami informasi tersirat dalam sebuah teks."
>
> Elemen Menulis–Mempresentasikan (relevan ke materi ini):
> > "Pada akhir Fase D, peserta didik mengomunikasikan ide dan pengalaman mereka melalui paragraf sederhana dan terstruktur, menunjukkan perkembangan dalam penggunaan kosakata spesifik dan struktur kalimat sederhana. Menggunakan contoh, mereka membuat perencanaan, menulis, dan menyajikan teks informasi, imajinasi dan persuasi dengan menggunakan kalimat sederhana dan majemuk untuk menyusun argumen dan menjelaskan atau mempertahankan suatu pendapat."
>
> **C. TUJUAN PEMBELAJARAN**
> 1. Mengidentifikasi struktur teks (identification & description) dan ciri kebahasaan descriptive text.
> 2. Menemukan ide utama & informasi rinci dari descriptive text.
> 3. Menyusun & mempresentasikan descriptive text sederhana secara tertulis.
>
> **D. KEGIATAN PEMBELAJARAN**
> *Pertemuan 1 (membaca):* apersepsi → baca contoh teks, identifikasi struktur & ciri kebahasaan (simple present, adjective) → LK ide utama/rinci → refleksi.
> *Pertemuan 2 (menulis & presentasi):* ulas materi → pilih objek, susun kerangka, tulis descriptive text → presentasi & umpan balik → refleksi.
>
> **E. ASESMEN**
> Formatif: observasi diskusi + LK membaca. Sumatif: hasil tulisan & presentasi (struktur, tata bahasa, kosakata, kelancaran).
>
> ---
>
> File lengkapnya (siap print, format 1 lembar, ada kolom tanda tangan Kepsek & Guru) sudah ada di workspace: `RPP_Descriptive_Text_BahasaInggris_FaseD.txt`. Kalau mau saya convert ke Word/PDF atau isikan nama sekolah & kelas pastinya, tinggal bilang saja.

### Balasan SESUDAH (dengan skill)

*tools: read (SKILL.md)*

> Baik, Bu — sebelum saya susun RPP 1 lembarnya, ada dua hal yang perlu saya pastikan dulu, terutama karena ini untuk supervisi pengawas besok:
>
> **1) Soal kode CP resmi**
> Saya tidak bisa menuliskan kode dan bunyi CP (Capaian Pembelajaran) resmi dari ingatan seolah-olah pasti sama persis dengan dokumen BSKAP — teks CP bisa direvisi dan kalau saya salah kutip, ini justru berisiko saat diperiksa pengawas. Supaya **aman untuk supervisi**, ada dua opsi:
>
> - **Opsi A (paling aman & cepat):** Ibu salin-tempel kode + bunyi CP Bahasa Inggris Fase-nya dari dokumen resmi sekolah/Kemendikdasmen (biasanya ada di buku panduan kurikulum sekolah atau situs resmi), lalu kirim ke saya — saya pakai itu persis sebagai sumber kebenaran di RPP-nya.
> - **Opsi B:** Saya tuliskan dulu RPP lengkap dengan CP yang ditandai jelas `(cek CP resmi)`, dan Ibu tinggal mencocokkan/menempelkan kode resminya sendiri sebelum dicetak — saya kasih juga keterangan di mana biasanya CP itu bisa dicek.
>
> **2) Jenjang & kelas**
> Kelas berapa Bahasa Inggrisnya (SD/SMP/SMA kelas berapa)? Ini menentukan Fase CP yang dipakai dan tingkat kerumitan descriptive text-nya.
>
> Supaya cepat, Ibu bisa jawab misalnya: *"SMP kelas 7, pakai Opsi B dulu"* — nanti saya langsung buatkan RPP 1 lembarnya lengkap dan Ibu tinggal cocokkan kode CP-nya sebelum dipakai besok.

**Jawaban balik pengguna (identik di kedua sisi):**

> SMP kelas 8 Bu, 1 pertemuan aja. CP-nya terserah, yang penting jadi.

### Balasan SEBELUM (tanpa skill) — giliran 2

*tools: write*

> Sudah direvisi, Bu — jadi RPP 1 lembar untuk **SMP kelas VIII, 1 pertemuan (2 JP/80 menit)**. File tersimpan di `RPP_Descriptive_Text_BahasaInggris_FaseD.txt`.
>
> Ringkasannya:
>
> **Identitas:** Bahasa Inggris | Fase D / Kelas VIII | Descriptive Text | 2 JP (1 pertemuan)
>
> **CP (verbatim, dasar hukum lengkap):** Keputusan Kepala BSKAP Kemendikbudristek No. **033/H/KR/2022** (perubahan atas No. 008/H/KR/2022), Lampiran I Bahasa Inggris Fase D, hal. 160–161 — CP umum + elemen Membaca-Memirsa & Menulis-Mempresentasikan saya kutip persis seperti sebelumnya (tidak ada kode angka per elemen di dokumen resmi, jadi nomor Keputusan itu yang jadi rujukan formalnya).
>
> **Kegiatan (1x80 menit):**
> - Pendahuluan 10' — apersepsi
> - Inti 60' — contoh teks (10') → identifikasi struktur & grammar berkelompok (15') → diskusi kelas (10') → menulis descriptive text individu 3–5 kalimat (20') → baca hasil & feedback (5')
> - Penutup 10' — refleksi + PR lanjutan kalau belum selesai
>
> **Asesmen:** formatif (observasi diskusi) + sumatif (hasil tulisan individu).
>
> Siap dicetak, tinggal isi nama sekolah/kepsek/tanggal. Mau saya buatkan juga versi Word/PDF-nya biar langsung bisa print?

### Balasan SESUDAH (dengan skill) — giliran 2

*tools: ls, read, exec (`hitung_alokasi_waktu.py`)*

> Sudah saya susun ya, Bu. **Catatan penting dulu soal CP** (baca sebelum dipakai besok):
>
> Saya **tidak menuliskan kode CP resmi dari ingatan** karena bisa salah kutip dan justru berisiko kalau diperiksa pengawas (kode/bunyi CP ditetapkan Keputusan Kepala BSKAP No. 046/H/KR/2025 dan bisa direvisi — saya tidak punya salinan resminya yang dijamin akurat). Jadi di bawah saya tulis **ringkasan CP** yang ditandai jelas, dan Bu tinggal cocokkan dengan dokumen CP resmi Bahasa Inggris Fase D di sekolah/KOSP (biasanya ada di buku panduan kurikulum sekolah, atau unduhan resmi dari dinas/Kemendikdasmen). Ini justru lebih aman untuk supervisi daripada saya menebak kode yang salah.
>
> Alokasi waktu sudah saya verifikasi dengan skrip (bukan dikira-kira): 10+60+10 = 80 menit = 2 JP × 40 menit (SMP), **status COCOK**.
>
> ---
>
> # RPP 1 LEMBAR — BAHASA INGGRIS
>
> | | |
> |---|---|
> | Sekolah | [nama sekolah Ibu] |
> | Mata Pelajaran | Bahasa Inggris |
> | Kelas / Semester | VIII / [1 atau 2] |
> | Fase | D |
> | Topik | Descriptive Text (teks deskripsi orang, tempat, atau benda) |
> | Alokasi Waktu | 1 pertemuan × 2 JP (80 menit) |
>
> **Capaian Pembelajaran (CP):** *(cek CP resmi — cocokkan dengan dokumen resmi Bahasa Inggris Fase D, BSKAP No. 046/H/KR/2025)* — Ringkasan umum: peserta didik mampu memahami dan menghasilkan teks deskriptif sederhana, lisan maupun tulisan, tentang orang, tempat, atau benda di sekitarnya dengan struktur dan kosakata yang sesuai.
>
> ## A. Tujuan Pembelajaran
> 1. Mengidentifikasi struktur teks descriptive text (*identification* & *description*) dari contoh teks sederhana.
> 2. Menyusun kalimat deskriptif menggunakan *adjective* dan *simple present tense* tentang orang/tempat/benda di sekitar siswa.
> 3. Menulis paragraf descriptive text sederhana (minimal 5 kalimat) tentang satu objek pilihan sendiri (anggota keluarga, tempat favorit, atau hewan peliharaan) dengan struktur dan kosakata yang tepat.
>
> **Pemahaman bermakna:** siswa bisa mendeskripsikan orang/tempat yang mereka sayangi atau kagumi dalam Bahasa Inggris — berguna saat memperkenalkan diri, keluarga, atau kampung halaman ke orang lain.
>
> ## B. Langkah-Langkah Pembelajaran
>
> **Pendahuluan (10 menit)**
> - Salam, doa, presensi.
> - Apersepsi: tanya jawab singkat ciri fisik benda di kelas dalam Bahasa Inggris sederhana ("This is a ___. It is ___.").
> - Guru menyampaikan tujuan pembelajaran & pertanyaan pemantik: *"Who is someone special in your life? How would you describe them in English?"* / "Kalau kalian menjelaskan Candi Borobudur atau pasar dekat rumah ke turis asing, kata-kata apa yang kalian pakai?"
>
> **Inti (60 menit)**
> 1. (10') Guru menampilkan 1 contoh descriptive text pendek (mis. deskripsi Candi Borobudur atau kucing peliharaan).
> 2. (15') Diskusi berpasangan mengidentifikasi struktur teks (*identification* & *description*) dan ciri bahasa (*adjective*, *simple present tense*).
> 3. (15') Latihan menyusun kalimat deskriptif berdasarkan gambar yang diberikan guru.
> 4. (20') Siswa menulis paragraf descriptive text singkat (min. 5 kalimat) tentang objek pilihan sendiri.
>
> **Penutup (10 menit)**
> - Beberapa siswa membacakan hasil tulisan secara sukarela.
> - Guru & siswa menyimpulkan ciri-ciri descriptive text bersama.
> - Refleksi singkat: "Bagian apa yang paling mudah/sulit hari ini?" + info pertemuan berikutnya.
>
> *(Total: 10+60+10 = 80 menit — terverifikasi cocok dengan 2 JP × 40 menit SMP)*
>
> ## C. Penilaian
>
> | Jenis | Kapan | Instrumen | Yang dinilai |
> |---|---|---|---|
> | Diagnostik | Awal pertemuan | Tanya jawab lisan (ciri fisik benda sekitar) | Penguasaan kosakata *adjective* dasar |
> | Formatif | Selama kegiatan inti | Pengamatan diskusi berpasangan + hasil latihan menyusun kalimat | Pemahaman struktur & proses belajar |
> | Sumatif | Akhir pertemuan | Paragraf descriptive text tulisan siswa | Ketercapaian Tujuan Pembelajaran 1–3 |
>
> **Rubrik singkat (skor 1–4 per aspek, nilai = (skor total ÷ skor maksimum) × 100):**
> - Struktur teks (ada *identification* + *description*)
> - Ketepatan *adjective* & *simple present tense*
> - Kejelasan & kesesuaian isi dengan objek yang dipilih
>
> **Pengayaan:** siswa yang sudah lancar menambah 2 kalimat memakai *comparative adjective* ("...is bigger/more beautiful than...").
> **Remedial:** siswa yang kesulitan diberi kerangka kalimat ("This is my ___. He/She/It is ___ and ___.") + daftar kosakata *adjective* bantuan.
>
> ---
>
> Asumsi yang dipakai: 1 pertemuan × 2 JP (sesuai permintaan Ibu), kelas VIII SMP → Fase D, topik descriptive text dengan konteks lokal (Candi Borobudur/pasar/hewan peliharaan/keluarga).
>
> Cek sebelum dipakai: kode & bunyi CP di atas masih **ringkasan umum** — wajib dicocokkan dengan dokumen CP resmi Bahasa Inggris Fase D (BSKAP No. 046/H/KR/2025) dari KOSP sekolah atau dinas sebelum ditempel untuk supervisi, supaya kode CP yang tertulis benar-benar persis dengan dokumen resmi.
>
> Cara pindah ke Word/Google Docs: salin semua teks di atas, tempel ke dokumen baru — Google Docs otomatis membaca tanda # dan ** sebagai judul/tebal; di Word gunakan "Tempel Khusus > Teks Tanpa Format" lalu terapkan gaya Heading pada judul-judul di atas.
>
> Mau saya lengkapi juga:
> 1. LKPD-nya (lembar kerja siswa + kunci jawaban) biar langsung siap dibagikan?
> 2. Soal evaluasi + kunci + rubrik skor lengkap untuk sumatifnya?
> 3. Versi dengan kop surat/identitas sekolah Ibu (kalau ada format RPP sekolah sendiri, kirim saja dan saya sesuaikan)?

### Verifikasi independen

- **Dasar CP yang berlaku:** Keputusan Kepala BSKAP **No. 046/H/KR/2025** (ditetapkan 16 Juli 2025, perubahan atas 032/H/KR/2024) — dicek penguji lewat pencarian web (antara lain dokumen di guru.kemendikdasmen.go.id). **Kepka BSKAP 033/H/KR/2022 sudah tidak berlaku** (diganti 032/2024, lalu diubah 046/2025).
- SEBELUM: mencari web lalu menulis "kutipan persis" CP dengan dasar **033/H/KR/2022** dan menyebutnya aman untuk pengawas → **dasar aturan usang** pada dokumen yang justru diminta untuk supervisi. Kelas diasumsikan VII tanpa bertanya. Setelah dijawab "kelas 8", tetap memakai 033/2022.
- SESUDAH: bertanya sekali (kelas + opsi CP), tidak mengarang kode, menandai CP "(cek CP resmi … BSKAP No. 046/H/KR/2025)" — rujukan yang benar. Menit: SMP 1 JP = 40 menit → 2 JP = 80 = 10+60+10 (penguji cek; inti 10+15+15+20 = 60) cocok. Rubrik dengan cara hitung nilai, diferensiasi, konteks lokal (Borobudur/pasar).

### Skor

| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan (dasar CP) | 3 | 9 |
| Siap pakai | 6 | 8 |
| Aturan kurikulum terbaru | 3 | 9 |
| Keamanan (tidak mengarang) | 5 | 9 |
| Kejelasan | 7 | 9 |
| **Skor** | **4** | **9** |

## Ringkasan

- **Skor rata-rata:** SEBELUM **4,5** → SESUDAH **9,0**. Skill terpakai di semua giliran SESUDAH (SKILL.md, references, `hitung_alokasi_waktu.py`).
- **VERDIK: LULUS** — sesudah ≥ 8, jelas lebih baik; kunci jawaban & menit terverifikasi benar; dasar CP terbaru benar. Tanpa skill ditemukan kesalahan matematika (3/8 senilai 1/2) dan dasar CP usang (033/2022).
- **Perilaku agent:** tidak ada pemasangan paket (SEBELUM membuat .docx dengan alat yang sudah ada), tidak ada perubahan config/pencarian disk/tawaran kirim otomatis.

### Cacat untuk pembuat
1. **Slot waktu sumatif tidak konsisten** (S1: asesmen menyebut sumatif "akhir pertemuan 2", tetapi rincian menit P2 tidak menyisakan waktu evaluasi). *Saran:* checklist tambah "instrumen sumatif punya slot menit yang tercantum, atau ditulis 'di pertemuan berikutnya'".
2. **Label dimensi Profil Lulusan** — tertulis "Bernalar Kritis"; nama dimensi 2025 adalah "Penalaran Kritis". *Saran:* minta agent menyalin nama dimensi persis dari `references/dasar-kurikulum.md`.
3. Minor: gambar ASCII "lingkaran" berbentuk batang — sebut "persegi panjang/pita" agar tidak membingungkan siswa.

### Cuplikan jualan
- "Semua kunci jawaban dihitung ulang dan menit tiap pertemuan dicek script — tanpa skill, AI yang sama menulis 3/8 sebagai pecahan senilai 1/2."
- "Minta 'kode CP resmi persis' untuk supervisi? Skill tidak mengarang dan merujuk Kepka BSKAP 046/H/KR/2025; tanpa skill, AI mengutip keputusan 2022 yang sudah diganti."
