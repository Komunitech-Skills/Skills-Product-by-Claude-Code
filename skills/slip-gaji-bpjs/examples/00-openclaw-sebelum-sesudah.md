# Uji OpenClaw asli SEBELUM vs SESUDAH — slip-gaji-bpjs

**Tanggal:** 2026-10-01 · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji

- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member).
- SEBELUM = home tanpa skill ini; SESUDAH = home berisi skill ini saja. Home dibuat ulang bersih per skenario; pesan identik di kedua sisi; balasan lanjutan (bila ada) juga identik.
- Angka diverifikasi independen dengan Python + aturan Indonesia.
- Home SEBELUM: `k-slip-gaji-bpjs`. Home SESUDAH: `s-slip-gaji-bpjs` lalu `s9-slip-gaji-bpjs`: proses lain di mesin uji (penguji paralel) menjalankan `rm -rf homes/s-*` sehingga run SESUDAH pertama skenario 1 dan giliran 2 skenario 2 gagal di tengah (ENOENT, bukan kesalahan skill). Run tersebut diulang utuh di home bersih bernama `s9-slip-gaji-bpjs` (isi identik: hanya skill ini).


## Skenario 1 — Normal: slip 2 karyawan, lembur, kasbon, UMK

### Giliran 1 — pesan pengguna
~~~~text
Tolong bikinin slip gaji Oktober 2026 buat 2 karyawan Toko Makmur (toko sembako):
1. Andi, K/0, gaji pokok 5.200.000, tunjangan transport tetap 400.000, lembur 2 jam hari Senin dan 3 jam hari Rabu
2. Sari, TK/0, gaji pokok 4.800.000, ada kasbon 200.000
Dua-duanya ikut BPJS Kesehatan & BPJS Ketenagakerjaan. UMK sini 5.396.761. Sama take home pay dan total biaya saya berapa
~~~~

**SEBELUM (tanpa skill)** — tools: tool_search, ls, memory_search, tool_call, exec

~~~~text
**Slip Gaji Oktober 2026 — Toko Makmur**

**1) Andi (K/0)**
- Gaji Pokok: Rp5.200.000
- Tunjangan Transport (tetap): Rp400.000
- Lembur (Senin 2 jam + Rabu 3 jam): Rp291.329
  _(upah/jam = (gapok+tunjangan tetap)÷173 = Rp32.370; jam pertama 1,5x, jam berikutnya 2x — formula Permenaker 100/2021)_
- **Gaji Bruto: Rp5.891.329**

Potongan:
- BPJS Kesehatan (1%): Rp56.000
- BPJS JHT (2%): Rp112.000
- BPJS JP (1%): Rp56.000
- PPh21 (skema TER A, 0,5%): Rp29.457
- **Total Potongan: Rp253.457**

**Take Home Pay Andi: Rp5.637.872**

Iuran ditanggung Toko (employer):
- BPJS Kesehatan 4%: Rp224.000
- JKK 0,24%: Rp13.440
- JKM 0,3%: Rp16.800
- JHT 3,7%: Rp207.200
- JP 2%: Rp112.000
- **Total iuran employer: Rp573.440**

**Total Biaya Perusahaan utk Andi: Rp6.464.769**

---

**2) Sari (TK/0)**
- Gaji Pokok / Gaji Bruto: Rp4.800.000

Potongan:
- BPJS Kesehatan 1%: Rp48.000
- BPJS JHT 2%: Rp96.000
- BPJS JP 1%: Rp48.000
- Kasbon: Rp200.000
- PPh21: Rp0 (bruto masih di bawah ambang TER A Rp5.400.000)
- **Total Potongan: Rp392.000**

**Take Home Pay Sari: Rp4.408.000**

Iuran ditanggung Toko (employer):
- BPJS Kesehatan 4%: Rp192.000
- JKK 0,24%: Rp11.520
- JKM 0,3%: Rp14.400
- JHT 3,7%: Rp177.600
- JP 2%: Rp96.000
- **Total iuran employer: Rp491.520**

**Total Biaya Perusahaan utk Sari: Rp5.291.520**

---

**REKAP**
- Total Take Home Pay (2 karyawan): **Rp10.045.872**
- Total Biaya Perusahaan (gaji bruto + BPJS employer, 2 karyawan): **Rp11.756.289**

⚠️ **Yang perlu diperhatikan:**
- Gaji pokok Sari (Rp4.800.000) **di bawah UMK** setempat (Rp5.396.761) — ini pelanggaran ketenagakerjaan, berisiko kena sanksi/teguran. Perlu dinaikkan minimal ke UMK, atau susun ulang komponen gapok+tunjangan tetap agar totalnya ≥ UMK (seperti skema Andi: gapok+transport = Rp5.600.000, sudah aman).
- JKK employer saya pakai kelas risiko terendah (0,24%) — standar utk usaha ritel/toko kelontong. Kalau BPJS Ketenagakerjaan menetapkan kelas risiko lain untuk toko sembakonya, nilainya bisa beda.
- PPh21 pakai skema TER (PMK 168/2023): Andi (K/0) dan Sari (TK/0) sama-sama masuk kategori TER A.

Mau saya buatkan versi PDF/print-nya juga?
~~~~

**SESUDAH (dengan skill)** — tools: read, exec (scripts/payroll.py), ls, write

~~~~text
Siap, sudah jadi. Ringkasan payroll Oktober 2026 — Toko Makmur:

| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |
|---|---:|---:|---:|---:|---:|
| Andi (K/0) | Rp 5.891.329 | Rp 270.091 | Rp 46.091 | **Rp 5.621.238** | Rp 6.464.769 |
| Sari (TK/0) | Rp 4.800.000 | Rp 397.968 | Rp 0 | **Rp 4.402.032** | Rp 5.315.390 |
| **Total** | **Rp 10.691.329** | | | **Rp 10.023.270** | **Rp 11.780.159** |

**Jawaban langsung:**
- Take home pay total: **Rp 10.023.270** (Andi Rp 5.621.238 + Sari Rp 4.402.032)
- Total biaya perusahaan: **Rp 11.780.159**

Rincian setor:
- BPJS Kesehatan (4%+1%): Rp 549.838
- BPJS Ketenagakerjaan (JHT+JKK+JKM+JP): Rp 960.960
- PPh 21: Rp 46.091 (dari Andi; Sari Rp 0 karena masih di bawah PTKP efektif TER)

Detail Andi: lembur 2 jam Senin + 3 jam Rabu dihitung sesuai PP 35/2021 (upah sejam dari gaji pokok+tunjangan tetap ÷173) → lembur jadi Rp 291.329.
Detail Sari: kasbon Rp 200.000 masuk sebagai potongan lain.

⚠️ **Peringatan penting:**
1. **Sari**: gaji pokok Rp 4.800.000 **di bawah UMK Rp 5.396.761**. Perlu dicek — kecuali Toko Makmur termasuk usaha mikro/kecil yang punya pengaturan upah tersendiri, ini berpotensi melanggar ketentuan upah minimum. Sebaiknya disesuaikan.
2. Tarif JKK tidak disebutkan, jadi saya pakai default 0,24% (risiko sangat rendah). Kalau toko sembako Anda punya tarif JKK lain dari sertifikat BPJS Ketenagakerjaan, beri tahu saya untuk dihitung ulang.

Asumsi lain: pola kerja 5 hari/minggu, kedua karyawan ikut BPJS Kesehatan & semua komponen BPJS Ketenagakerjaan (termasuk JP), tidak ada bonus/THR/PPh 21 DTP.

File tersimpan di folder kerja (`payroll/2026-10/`):
- `slip-gaji-2026-10.md` — slip siap tempel
- `slip-gaji-2026-10.html` — buka di browser → Print/Save as PDF (1 slip/halaman)
- `rekap-payroll-2026-10.csv` — buka di Excel

CSV input (`karyawan-oktober-2026.csv`) saya buat dari data chat Anda dan sudah tersimpan di folder yang sama — mau saya hapus sekarang karena isinya data gaji, atau dibiarkan untuk referensi bulan depan?
~~~~

### Verifikasi
Hitung independen (Python):
- Andi: upah sejam (5.200.000+400.000)/173 = 32.369,94; lembur Senin 2 jam = 1,5+2 = 3,5; Rabu 3 jam = 1,5+2+2 = 5,5 → 9 × 32.369,94 = **Rp 291.329**; total pendapatan **Rp 5.891.329**.
- Bruto pajak Andi = 5.891.329 + JKK 0,24% 13.440 + JKM 0,3% 16.800 + BPJS Kes 4% 224.000 = **6.145.569** (PMK 168/2023 Pasal 5: premi JKK, JKM, BPJS Kes bagian perusahaan masuk bruto) → TER A >5,95–6,3 jt = 0,75% → **Rp 46.091**. Potongan 56.000+112.000+56.000+46.091 = 270.091 → THP **Rp 5.621.238**.
- Sari: dasar BPJS Kesehatan minimal UMK (Perpres 64/2020) → 1% × 5.396.761 = **Rp 53.968** (bukan 48.000); JHT 96.000, JP 48.000, kasbon 200.000 → THP **Rp 4.402.032**; bruto pajak 5.041.790 → TER A 0%.
- SESUDAH: semua angka **cocok persis** (THP total Rp 10.023.270, biaya perusahaan Rp 11.780.159), peringatan UMK & JKK default ada, file MD/HTML/CSV di folder kerja (bukan /tmp), menawarkan menghapus CSV input.
- SEBELUM: lembur benar, tetapi (a) PPh 21 Andi Rp 29.457 — **salah** (bruto tanpa JKK/JKM/BPJS Kes 4%, jadi tarif 0,5% bukan 0,75%); (b) BPJS Kes Sari dari Rp 4,8 jt — **salah** (harus dari UMK); THP Andi & Sari, biaya Sari, dan total semuanya meleset.

### Skor
| | Skor | Alasan |
|---|---:|---|
| SEBELUM | 6 | Rapi dan lembur benar, peringatan UMK ada; tetapi dua kesalahan hitung (bruto PPh 21 & dasar BPJS Kes minimal UMK) membuat THP/biaya salah; tanpa file slip cetak. |
| SESUDAH | 9 | Semua angka benar, slip siap cetak + CSV rekap, rincian setoran BPJS/PPh, peringatan & asumsi jelas, privasi data gaji dijaga. |

Skill terpakai: Ya (SKILL.md dibaca, `scripts/payroll.py` dijalankan).

## Skenario 2 — Jebakan Desember (hitung ulang setahun) + data kurang

### Giliran 1 — pesan pengguna
~~~~text
Bikinin slip gaji Desember 2026 buat Budi ya, status K/1, gaji pokok 7.500.000, ikut BPJS Kesehatan & Ketenagakerjaan semua. Usaha saya percetakan. Potongan pajak sama gaji bersihnya berapa?
~~~~

**SEBELUM (tanpa skill)** — tools: ls, memory_search, tool_call, tool_search, write, edit, read

~~~~text
Udah jadi, Slip gaji Budi untuk Desember 2026 (status K/1, usaha percetakan):

**Pendapatan bruto:** Rp 7.500.000 (gaji pokok)

**Potongan:**
| Komponen | Tarif | Jumlah |
|---|---|---|
| BPJS Kesehatan (karyawan) | 1% | Rp 75.000 |
| BPJS Ketenagakerjaan – JHT (karyawan) | 2% | Rp 150.000 |
| BPJS Ketenagakerjaan – JP (karyawan) | 1% | Rp 75.000 |
| PPh 21 (TER Kategori B) | 2% | Rp 150.000 |
| **Total potongan** | | **Rp 450.000** |

**Gaji bersih (take home pay): Rp 7.050.000**

Catatan:
- Status K/1 masuk kategori TER **B**; gaji Rp 7.500.000 kena bracket 2% (ambang Rp 7.300.000–9.200.000 di kategori B).
- JKK & JKM 100% ditanggung perusahaan, tidak motong gaji Budi — tapi saya tambahkan di file biar kamu tahu total biaya tenaga kerja buat pembukuan.
- Semua angka saya hitung dari gaji penuh karena jauh di bawah batas upah maksimum BPJS Kesehatan maupun JP.

⚠️ Satu catatan jujur: koneksi internet saya lagi nggak bisa saya pakai buat cek ulang apakah tarif TER/BPJS 2026 ada perubahan dari aturan terakhir yang saya tahu (PP 58/2023). Kalau penting banget akurat 100% buat laporan resmi, aku saranin cek sekali lagi ke pajak.go.id atau bpjsketenagakerjaan.go.id, atau bilang aja nanti aku coba cek ulang pas koneksi normal.

File lengkap (termasuk rincian kontribusi perusahaan) saya simpan di `slip-gaji/2026-12-budi.md`.
~~~~

**SESUDAH (dengan skill)** — tools: read, exec

~~~~text
Siap, Pak! Untuk slip gaji Desember, karena ini bulan terakhir tahun pajak, PPh 21 harus dihitung ulang setahun penuh (bukan cuma bulanan biasa) — jadi saya butuh beberapa data tambahan dari Budi untuk Januari–November 2026. Boleh dijawab singkat ya:

1. Budi mulai kerja di percetakan sejak bulan apa tahun 2026 ini? (kalau sudah dari Januari, cukup jawab "Januari" / sudah 11 bulan kerja sebelum Desember)
2. Total penghasilan bruto kena pajak Budi dari Januari s.d. November 2026 (gaji + tunjangan + premi BPJS yang dibayar perusahaan)?
3. Total PPh 21 yang sudah dipotong dari gaji Budi Januari s.d. November 2026?
4. Total potongan JHT (2%) + JP (1%) karyawan yang sudah dipotong Januari s.d. November 2026?
5. (Opsional) UMK/UMP kota tempat usaha percetakannya, untuk saya cek batas bawah BPJS Kesehatan — kalau tidak tahu, saya lewati pengecekan ini dan sebutkan sebagai asumsi.

Catatan asumsi sementara yang akan saya pakai kalau tidak dikoreksi: tunjangan tetap = 0, tarif JKK = 0,24% (default/risiko rendah — percetakan bisa jadi lebih tinggi, tolong koreksi kalau tahu tingkat risikonya), pola kerja 5 hari/minggu, tanpa lembur/bonus/potongan lain.
~~~~

### Giliran 2 — pesan pengguna
~~~~text
Dia kerja dari Januari, gajinya 7,5 juta terus tiap bulan, nggak ada tunjangan, bonus, THR atau kasbon. Percetakan bukan sektor DTP. PPh 21 Jan-Nov yang udah dipotong saya nggak nyatet, tolong hitungin aja dari data itu.
~~~~

**SEBELUM (tanpa skill)** — tools: web_fetch, tool_call, write, edit

~~~~text
Udah saya hitung ulang pakai data itu (gaji flat Rp 7.500.000 dari Januari, tanpa tunjangan/bonus/THR/kasbon, dan percetakan bukan sektor DTP jadi nggak ada subsidi pajak).

**Koreksi dulu:** di hitungan sebelumnya saya salah pakai tarif TER B 2% — setelah saya cek ulang tabel resmi PMK 168/2023, gaji Rp 7.500.000 itu masuk bracket **Rp 7.300.001–9.200.000 → tarif 1%**. Sudah saya perbaiki.

**PPh 21 Januari–November** (TER Kategori B, 1% x gaji bruto):
- Rp 75.000/bulan × 11 bulan = **Rp 825.000**

**PPh 21 Desember** (bulan ini WAJIB direkonsiliasi pakai tarif Pasal 17 atas setahun penuh, bukan tarif TER lagi):
- Gaji setahun: Rp 90.000.000
- Dikurangi biaya jabatan (5%, maks Rp 6jt/th): Rp 4.500.000
- Dikurangi iuran JHT+JP karyawan (deductible): Rp 2.700.000
- Penghasilan neto setahun: Rp 82.800.000
- PTKP K/1: Rp 63.000.000
- PKP: Rp 19.800.000 → PPh 21 setahun (5%) = Rp 990.000
- Dikurangi yang sudah dipotong Jan-Nov (Rp 825.000)
- **PPh 21 potongan Desember = Rp 165.000**

**Total PPh 21 setahun 2026: Rp 990.000**

**Gaji bersih:**
| | Jan–Nov (per bulan) | Desember |
|---|---|---|
| Gaji pokok | 7.500.000 | 7.500.000 |
| BPJS Kesehatan (1%) | -75.000 | -75.000 |
| BPJS TK JHT (2%) | -150.000 | -150.000 |
| BPJS TK JP (1%) | -75.000 | -75.000 |
| PPh 21 | -75.000 | -165.000 |
| **Gaji bersih** | **Rp 7.125.000** | **Rp 7.035.000** |

⚠️ Penting: angka Jan-Nov ini saya hitung dari data yang kamu kasih tadi (gaji flat tanpa variasi), bukan dari catatan potongan aktual — karena kamu bilang nggak nyatet. Kalau potongan yang benar-benar keluar dari rekening Budi selama ini beda dari Rp 75.000/bulan (misal perusahaan sempat salah tarif), angka rekonsiliasi Desember di atas bisa berubah. Cocokkan dulu ke slip/bukti transfer kalau ada.

Saya simpan rinciannya di:
- `slip-gaji/2026-12-budi.md` (slip Desember, sudah dikoreksi)
- `slip-gaji/2026-rekap-tahunan-budi.md` (rekap perhitungan Jan-Des lengkap)
~~~~

**SESUDAH (dengan skill)** — tools: exec (scripts/payroll.py), read

~~~~text
Sudah selesai, Pak. Berikut hasil slip gaji Desember 2026 untuk Budi:

**Rekap payroll Desember 2026 — Percetakan Budi** (1 karyawan)
| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |
|---|---:|---:|---:|---:|---:|
| Budi (K/1) | Rp 7.500.000 | Rp 621.595 | Rp 321.595 | **Rp 6.878.405** | Rp 8.268.000 |

Rincian potongan: BPJS Kesehatan 1% Rp75.000, JHT 2% Rp150.000, JP 1% Rp75.000, **PPh 21 Rp321.595**.

**Kenapa PPh 21 Desember jauh lebih besar dari bulan biasa (~Rp78.405/bulan)?** Karena Desember wajib hitung ulang pajak setahun penuh (Masa Pajak Terakhir, Pasal 17 UU HPP) — bukan pakai tarif TER bulanan lagi:
- Bruto setahun: Rp 94.086.000 → neto kena pajak (setelah biaya jabatan maks Rp6jt + iuran pensiun) Rp 86.681.700 → PKP (setelah PTKP K/1 Rp63jt) Rp 23.681.000 → pajak setahun **Rp 1.184.050**.
- Sudah dipotong Jan–Nov (dihitung dari data gaji tetap Rp7,5jt/bulan tanpa variasi, sesuai arahan Anda) **Rp 862.455**.
- Sisa yang dipotong di slip Desember = Rp 1.184.050 − Rp 862.455 = **Rp 321.595**.

Ditanggung perusahaan (tidak memotong gaji): BPJS Kes 4% Rp300.000, JHT 3,7% Rp277.500, JKK 0,24% Rp18.000, JKM 0,3% Rp22.500, JP 2% Rp150.000 → total Rp768.000.

**File tersimpan di:**
`.openclaw/workspace/payroll/payroll-2026-12/`
- `slip-gaji-2026-12.md`
- `slip-gaji-2026-12.html` (buka di browser → Print/Save as PDF)
- `rekap-payroll-2026-12.csv`

⚠️ **Asumsi yang saya pakai** (tolong koreksi bila tidak sesuai):
- Gaji Jan–Nov dianggap flat Rp7,5jt/bulan tanpa tunjangan/bonus, jadi kumulatif bruto & PPh21 sebelumnya saya hitung sendiri (bukan dari catatan Anda) — kalau sebenarnya ada kenaikan gaji, bonus, atau potongan lain di tengah tahun, hasil ini bisa meleset dan perlu dihitung ulang dengan angka asli.
- UMK tidak diisi → cek upah minimum & batas bawah BPJS Kesehatan dilewati.
- Tarif JKK 0,24% (risiko sangat rendah) — percetakan kadang masuk risiko rendah-sedang (0,54%), tolong cek klasifikasi risiko usaha Anda di BPJSTK kalau mau lebih akurat.
- Bukan sektor DTP (sudah sesuai info Anda) → PPh 21 dipotong normal, tidak ada subsidi tunai.

PPh 21 dibulatkan ke bawah, iuran dibulatkan ke rupiah terdekat. Alat bantu hitung, bukan nasihat hukum/pajak — dasar: Perpres 64/2020, PP 44/45/46/2015, PP 35/2021, PP 58/2023 & PMK 168/2023, berlaku per 23 Sep 2026.
~~~~

### Verifikasi
Hitung independen (Python):
- Bruto pajak bulanan = 7.500.000 + JKK 18.000 + JKM 22.500 + BPJS Kes 4% 300.000 = 7.840.500 → TER B 1% = Rp 78.405; Jan–Nov = **Rp 862.455**.
- Setahun: 94.086.000 − biaya jabatan 4.704.300 − iuran JHT+JP (225.000 × 12) 2.700.000 = neto 86.681.700; PTKP K/1 63.000.000 → PKP 23.681.000 → 5% = 1.184.050 → **PPh 21 Desember Rp 321.595**; THP **Rp 6.878.405**.
- SEBELUM giliran 1: memakai TER untuk Desember (salah metode) **dan** tarif 2% untuk Rp 7,5 jt kategori B (salah; benar 1%) → PPh Rp 150.000. Giliran 2 mengoreksi metode, tetapi bruto tanpa JKK/JKM/BPJS Kes 4% → PPh Desember **Rp 165.000 (salah, kurang Rp 156.595)**, THP Rp 7.035.000 (salah).
- SESUDAH giliran 1: tidak menebak — meminta data Jan–Nov, bulan mulai kerja, UMK (sesuai aturan skill). Giliran 2: PPh Desember **Rp 321.595** dan THP **Rp 6.878.405 — cocok**, menyebut asumsi bahwa kumulatif Jan–Nov dihitung dari gaji flat, file slip dibuat.

### Skor
| | Skor | Alasan |
|---|---:|---|
| SEBELUM | 4 | Giliran 1 salah metode & tarif; giliran 2 masih salah bruto pajak sehingga PPh Desember kurang Rp 156.595. Ada kejujuran soal keterbatasan, tetapi angka tidak bisa dipakai. |
| SESUDAH | 9 | Menolak menebak data Desember, lalu menghitung ulang setahun dengan benar, menjelaskan kenapa Desember lebih besar, asumsi JKK/UMK disebut, disclaimer + dasar aturan. |

Skill terpakai: Ya (SKILL.md dibaca, `scripts/payroll.py` dijalankan).

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---:|---:|
| 1. Slip 2 karyawan | 6 | 9 |
| 2. Desember / data kurang | 4 | 9 |
| **Rata-rata** | **5,0** | **9,0** |

**VERDIK: LULUS** — sesudah ≥ 8, jelas di atas sebelum, tanpa kesalahan angka/fakta.

**Cacat untuk pembuat (minor):**
1. Giliran 1 skenario 2 versi SESUDAH meminta "total bruto pajak Jan–Nov" & "total iuran" — istilah berat untuk awam. Saran: tambahkan di SKILL.md opsi eksplisit "bila gaji sama setiap bulan sejak Januari, cukup jawab 'gajinya sama terus' — skill menghitung kumulatifnya sendiri" (script sudah mampu, terbukti di giliran 2).
2. Tarif JKK default 0,24% untuk percetakan disebut "kadang 0,54%" oleh agent; bagus, tapi SKILL.md bisa memberi contoh kelompok tarif per jenis usaha umum agar asumsi lebih tepat.

**Cuplikan jualan:**
- "Tanpa skill, bot menghitung PPh 21 Desember Rp 165.000; dengan skill Rp 321.595 — sesuai hitung ulang setahun PMK 168/2023 (uji OpenClaw asli, 1 Okt 2026)."
- "Iuran BPJS Kesehatan karyawan bergaji di bawah UMK otomatis dihitung dari UMK, dan Anda diberi peringatan upah minimum."

