# Uji OpenClaw SEBELUM vs SESUDAH — hitung-thr

> **Baca dulu:** belum ada uji sebelum/sesudah yang menyalakan dan mematikan `hitung-thr` seorang diri di OpenClaw. Bukti yang ada berasal dari dua uji yang memakai `hitung-thr` **bersama skill lain**: (A) **diuji sebagai bagian paket Kantor & Manajemen**, dan (B) diuji bersama skill `laporan-status-kantor`. Skor di bawah adalah skor seluruh jawaban, bukan skor `hitung-thr` saja, jadi selisihnya tidak boleh dibaca sebagai hasil `hitung-thr` sendirian. Uji ulang khusus skill ini ada di bagian terakhir, tetapi hanya sisi dengan skill (tanpa pembanding).

**Tanggal uji:** A = 2026-10-03, B = 2026-10-02 (Asia/Jakarta).
**Versi skill saat uji:** A = uji pertama kira-kira 1.0.7, uji ulang kira-kira 1.0.8 (catatan uji tidak menulis versi; disimpulkan dari riwayat versi katalog). B = 1.0.6 (tertulis). Versi katalog saat ini 1.0.9; versi itu belum diuji sebelum/sesudah di OpenClaw.
**Penguji:** agent penguji independen (bukan pembuat skill).
Sumber: catatan uji internal kurator (tidak disertakan dalam paket), 2026-10-03 (uji A).
Sumber: catatan uji internal kurator (tidak disertakan dalam paket), 2026-10-02 (uji B).

## Cara uji
- OpenClaw lokal (`openclaw agent --local`), sesi baru untuk tiap skenario, tanpa Telegram atau WhatsApp tersambung. Model router Komunitech yang sama dengan bot yang dipakai member, di kedua sisi. Uji B memakai OpenClaw 2026.9.6; catatan uji A tidak menulis versi OpenClaw.
- **SEBELUM** = OpenClaw bersih tanpa skill. **SESUDAH** = OpenClaw berisi skill yang disebut di tiap bagian. Pesan dan data fiktif identik di kedua sisi.
- Angka dihitung ulang penguji dengan Python (Permenaker 6/2016; PP 58/2023 dan PMK 168/2023 untuk PPh 21 TER; iuran BPJS).

## A. Diuji sebagai bagian paket Kantor & Manajemen (2026-10-03)
SESUDAH = 18 skill inti paket Kantor & Manajemen (termasuk `hitung-thr`) pada uji pertama, lalu 20 skill pada uji ulang 1 dan 2 dan 21 skill pada uji ulang 3, **ditambah blok aturan agent bawaan paket** di `AGENTS.md`. SEBELUM = tanpa skill dan tanpa blok aturan itu. Skenario 1 dari 3 skenario paket: HRD merangkap admin sebuah distributor bahan bangunan meminta THR Natal 2026 (Natal 25 Desember) untuk 4 karyawan fiktif, slip gaji Oktober 2026 dengan PPh 21 TER dan BPJS, serta ringkasan untuk grup Telegram kantor.

| Putaran | Skor tanpa skill | Skor dengan skill | Catatan penguji |
|---|:-:|:-:|---|
| Uji pertama | 1 | 7 | Satu angka salah: "total biaya gaji perusahaan" tertulis Rp27.798.120, seharusnya Rp28.800.120 (kurang Rp1.002.000, dijumlah di kepala, bukan script). `find /` tiga kali ke seluruh disk mencari skill slip gaji dan PPh 21 yang tidak ada di paket. |
| Uji ulang 1 (dua sesi) | 1 (dipakai ulang) | 8 dan 9 | Angka benar (biaya gaji Rp28.800.120 dari script); satu sesi menawarkan pengingat otomatis yang tidak diminta. Tanpa `find /`. |
| Uji ulang 2 (dua sesi) | 1 (dipakai ulang) | 9 dan 8 | Semua angka dari script; satu sesi menulis di teks grup "sudah disetor" padahal belum. Tanpa `find /`. |
| Uji ulang 3 | 1 (tidak diulang) | 9 | Semua angka dari script (Rp28.800.120 benar). |

Sisi tanpa skill: dua percobaan, **keduanya tanpa jawaban**. Percobaan 1 berhenti karena batas waktu model, percobaan 2 dihentikan penguji setelah 10 menit; agent berputar sekitar 30 kali membuka halaman web untuk mencari tabel TER dan BPJS. Skor 1 berarti "tidak ada jawaban", bukan jawaban yang jelek.

Angka yang dicek penguji dan benar di sisi dengan skill (uji pertama): THR tiap karyawan dan total Rp23.220.833 (dari `thr.py`), batas bayar H-7 Jumat 18 Desember 2026, tarif TER dan PPh 21 tiap karyawan (dari `ter_core.py`), dan PPh 21 atas THR Desember disebut sebagai masa pajak terakhir yang dihitung ulang setahun, tidak dikarang.

## B. Diuji bersama skill laporan-status-kantor (2026-10-02)
Uji ini terutama menguji `laporan-status-kantor`; `hitung-thr` ikut terpasang karena keduanya dijual dalam paket Kantor & Manajemen. SESUDAH = `laporan-status-kantor` 1.0.4 + `hitung-thr` 1.0.6, OpenClaw dibuat ulang bersih untuk tiap sesi. SEBELUM = tanpa skill (hasil dari uji sebelumnya dipakai ulang, pesan dan data identik).

| Skenario | Skor tanpa skill | Skor dengan skill |
|---|:-:|:-:|
| 1. Pengumuman libur Natal ke grup + THR satu karyawan, nominal diminta dicantumkan di grup | 6,5 | 8,7 (rata-rata 3 sesi: 9,2; 8,4; 8,4) |
| 2. "Umumkan THR ke grup, sebut masing-masing dapat berapa", dengan file data 4 karyawan | 6 | 9,4 (2 sesi: 9,4; 9,4) |
| **Rata-rata** | **6,3** (dari 6,25) | **9,0** |

Hasil periksa di sisi dengan skill (5 sesi): THR benar 5 dari 5 (satu karyawan Rp3.000.000; empat karyawan total Rp13.766.667); teks grup tanpa nama dan tanpa nominal per orang 5 dari 5 (uji sebelumnya dengan `hitung-thr` 1.0.5: nominal per orang bocor ke teks grup di 2 dari 4 balasan); rekap per orang hanya di blok khusus pemilik/HR 5 dari 5; tanpa tawaran menyambungkan WhatsApp atau kirim otomatis 5 dari 5; tanggal masuk di masa depan ditandai 2 dari 2.

Petunjuk kecil tentang `hitung-thr` aktif vs tidak (sampel kecil, versi `laporan-status-kantor` sama 1.0.3): tanpa `hitung-thr` (uji 2026-10-01) agent menghitung THR sendiri dan 1 dari 3 sesi salah (Rp3.333.333, seharusnya Rp3.000.000); dengan `hitung-thr` 1.0.5 (uji 2026-10-02) THR benar 3 dari 3.

## Verdik
- **Uji A (kata sumber, tingkat paket):** uji pertama BELUM LULUS (skor dengan skill 7 / 6 / 7 untuk tiga skenario, rata-rata 6,7, melawan tanpa skill 1 / 3 / 3); setelah tiga putaran uji ulang LULUS. Untuk skenario 1 yang memakai `hitung-thr`: 7 pada uji pertama, 8 sampai 9 pada uji ulang, melawan 1 tanpa skill.
- **Uji B (kata sumber, untuk pasangan skill):** LULUS pada 9,0 melawan 6,3. Uji sebelumnya (6,3 → 6,9) BELUM LULUS karena nominal per orang bocor ke teks grup.

## Pembeda (satu kalimat)
Hanya saat skill aktif: THR dihitung script dengan batas bayar H-7, dan hasilnya selalu dua blok terpisah (rekap per orang untuk pemilik/HR dan teks grup tanpa nama atau nominal), sedangkan tanpa skill jawaban paket tidak keluar sama sekali karena kehabisan waktu (uji A) dan draf pengumuman grup memuat nama serta nominal THR (uji B).

## Catatan jujur
- Ini uji gabungan. Skor menilai seluruh jawaban (slip gaji, PPh 21 TER, ringkasan grup, atau pengumuman libur), bukan hanya THR. Di uji A, sisi SESUDAH juga memuat blok aturan agent paket, jadi perbaikan antar putaran sebagian berasal dari paket dan aturan, bukan dari `hitung-thr`.
- Selisih besar di uji A sebagian besar karena sisi tanpa skill gagal menjawab. Di uji B model tanpa skill menghitung THR dengan benar; skor ketepatan angka sama-sama tinggi (tanpa skill 9 di kedua skenario, dengan skill 8 sampai 10). Pembeda nyata ada pada privasi (nominal per orang tidak masuk grup), format dua blok, dan perilaku yang lebih aman (tidak memeriksa kanal gateway, tidak menawarkan menyambungkan WhatsApp), bukan pada kemampuan menghitung.
- Cacat uji pertama A yang menyangkut skill ini: `hitung-thr` merujuk skill slip gaji dan PPh 21 yang tidak terpasang di paket, sehingga agent mencari ke seluruh disk. Satu baris ditambahkan ke SKILL.md (cek skill lain hanya di folder skills; bila tidak ada, jangan dicari; total biaya gaji hanya dari skill slip gaji) dan cacat itu tidak muncul lagi pada uji ulang 1 dan 2 (uji ulang 3 tidak mencatatnya secara tersendiri).
- Uji B menemukan pencarian web berulang untuk tanggal libur di 2 dari 5 sesi (9 dan 10 panggilan), yang membuat tanggal cuti bersama jadi isian kosong; tabel libur 2026 ditambahkan ke skill sesudahnya.
- Hanya skenario THR Natal (satu dan empat karyawan, masa kerja di bawah dan di atas 12 bulan). Karyawan kontrak, harian lepas, dan PHK tidak diuji sebelum/sesudah di OpenClaw.
- Kedua uji tanpa Telegram atau WhatsApp tersambung: teks grup hanya draf yang ditempel sendiri oleh pemakai. PPh 21 atas THR Desember sengaja tidak dihitung di uji A (butuh gaji Januari sampai November).

## Bukan sebelum/sesudah: uji ulang khusus hitung-thr (hanya dengan skill)
Rincian ada di `UJI-OPENCLAW-ULANG.md` dan `UJI-OPENCLAW-ULANG-2.md` di folder ini. Pesan sama di kedua putaran: gaji Rp4.500.000, mulai kerja 1 Maret 2026, Lebaran "20 Maret 2027".

| Tanggal | Versi | Skor dengan skill | Hasil |
|---|---|:-:|---|
| 2026-10-01 | 1.0.4 | 7 | Nama contoh dari skill tidak bocor lagi dan THR Rp4.500.000 benar, tetapi agent bertanya nama dulu dan tidak menanggapi tanggal Lebaran yang keliru (20 Maret 2027 = 11 Syawal 1448 H). Keluaran versi sebelumnya dinilai penguji sekitar 6 (skor aslinya tidak tercatat). |
| 2026-10-01 | 1.0.5 | 8,5 (LULUS) | Hitungan lengkap di giliran pertama tanpa bertanya nama; tanggal keliru ditanggapi (perkiraan Idul Fitri 10 Maret 2027, batas bayar 3 Maret 2027); THR Rp4.500.000 benar. |

Uji ini tidak punya sisi tanpa skill, jadi tidak boleh dipakai sebagai bukti selisih sebelum/sesudah.
