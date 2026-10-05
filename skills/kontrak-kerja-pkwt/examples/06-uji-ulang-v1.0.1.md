# Uji 06 — Uji ulang independen v1.0.1

> Penguji independen kedua (bukan pembuat, bukan perevisi), 25 September 2026. Salinan skill dijalankan di scratchpad (`uji2-pkwt/skill/`), Python 3 standar. Uji simulasi agent → `claude-code (simulasi agent)`.

## 1. Tes bawaan
`python3 tests/uji_regresi.py` → **LULUS semua 130 cek** (exit 0; v1.0.0: 98 cek).

## 2. Verifikasi angka independen
Implementasi penguji ditulis **hanya dari rumus SKILL.md** (bagian Rumus no. 1–6), tanpa membaca kode script, memakai `fractions.Fraction`:
- masa kerja: mulai & akhir inklusif; bulan penuh dari tanggal ulang yang dihitung dari tanggal mulai asli (dijepit ke akhir bulan); sisa hari ÷ panjang "bulan berjalan";
- kompensasi (PP 35/2021 Pasal 15–16): < 1 bulan → 0; tepat 12 → 1 × upah; lainnya bulan ÷ 12 × upah; per periode;
- ganti rugi Pasal 62: sisa = bulan(periode berjalan) − bulan(dijalani di periode itu); × upah; periode perpanjangan yang belum dimulai tidak dihitung;
- pembulatan ke rupiah terdekat (setengah ke atas).

**Uji acak (seed 20260925):** 17.994 kasus — 6.000 periode tunggal (2024–2030, panjang 0–800 hari), 6.000 putus dini acak, 3.000 rangkaian 2–3 perpanjangan tanpa jeda, ±3.000 putus dini dalam rangkaian; 6 besaran upah (Rp1.000.001, 3 jt, 4,8 jt, 5 jt, Rp7.777.777, Rp12.345.678).
- Kompensasi per periode & ganti rugi: **0 selisih rupiah**.
- 8 perbedaan hanya representasi: berhenti tepat di hari terakhir periode awal sebelum perpanjangan dimulai → script menampilkan ganti rugi **Rp0** (+ peringatan "perpanjangan belum dimulai"), implementasi penguji "tidak ada ganti rugi". Nilainya sama.
- **Aditivitas dijalani + sisa = panjang periode berjalan: 0 pelanggaran** (v1.0.0: 52% kasus gagal). `bulan_pecahan` di JSON sama persis dengan Fraction penguji di semua kasus.

**Kasus tepi & angka yang diubah perevisi** (upah 5 jt kecuali disebut; format: kompensasi per periode / ganti rugi):

| Kasus | Script | Mandiri | Status |
|---|---|---|---|
| 1–30 Jan 2026 (<1 bln) | [0] / GR - | [0] / GR - | cocok |
| 1–31 Jan 2026 (tepat 1 bln) | [416667] / GR - | [416667] / GR - | cocok |
| 1 Jan–31 Des 2026 (12 bln) | [5000000] / GR - | [5000000] / GR - | cocok |
| 1 Jan 2026–1 Jan 2027 (12 bln+1 hr) | [5013441] / GR - | [5013441] / GR - | cocok |
| 31 Jan–27 Feb 2026 | [416667] / GR - | [416667] / GR - | cocok |
| 31 Jan–28 Feb 2026 | [430108] / GR - | [430108] / GR - | cocok |
| 31 Jan–29 Feb 2028 kabisat | [430108] / GR - | [430108] / GR - | cocok |
| 29 Feb 2028–28 Feb 2029 | [5014368] / GR - | [5014368] / GR - | cocok |
| Perpanjangan 12+6 normal | [5000000, 2500000] / GR - | [5000000, 2500000] / GR - | cocok |
| Putus hari pertama (1 Jan, kontrak 12 bln) | [0] / GR 59838710 | [0] / GR 59838710 | cocok |
| Putus H-1 (30 Des, kontrak 12 bln) | [4986559] / GR 161290 | [4986559] / GR 161290 | cocok |
| Putus 15 Feb (1 Jan–31 Mar, 3 jt, pekerja) | [383929] / GR 4392857 | [383929] / GR 4392857 | cocok |
| 'dini sisa hari' 15 Mar 2026, 4,8 jt | [4800000, 993548] / GR 16877419 | [4800000, 993548] / GR 16877419 | cocok |
| 03 varian 15 Mar 2027 | [5000000, 1034946] / GR 17580645 | [5000000, 1034946] / GR 17580645 | cocok |
| 03 utama 31 Mar 2027 | [5000000, 1250000] / GR 15000000 | [5000000, 1250000] / GR 15000000 | cocok |
| 01 toko roti 1 Okt 2026–30 Sep 2027, 4,15 jt | [4150000] / GR - | [4150000] / GR - | cocok |
| Putus hari pertama perpanjangan (1 Jan 2027) | [5000000, 0] / GR 29838710 | [5000000, 0] / GR 29838710 | cocok |
| Putus 31 Jan pd kontrak mulai 31 Jan–30 Apr 2026, 15 Mar | [631720] / GR 7580645 | [631720] / GR 7580645 | cocok |
| Putus 28 Feb kabisat 2028 kontrak 31 Jan–30 Jun | [416667] / GR 20161290 | [416667] / GR 20161290 | cocok |

Semua angka yang disebut perevisi terkonfirmasi: 15 Feb → **Rp4.392.857** (41/28 × 3 jt); "dini sisa hari" → **Rp16.877.419** (109/31 × 4,8 jt); varian 03 tgl 15 Maret 2027 → **Rp17.580.645** (109/31 × 5 jt); skenario 01 tetap **Rp4.150.000**/orang; skenario 03 tetap **Rp5.000.000 + Rp1.250.000 + Rp15.000.000**.

**Penilaian metode pecahan bulan:** wajar dan kini konsisten (sisa = total − dijalani, jadi pengusaha/pekerja tidak pernah membayar lebih atau kurang dari panjang kontrak). Dinyatakan jelas di SKILL.md Rumus no. 2 & 4 (dengan contoh 15 Feb) dan di footer/rumus output script ("(3 - 1,5357) = 1,4643 bulan"). Konsekuensi yang perlu disadari (sudah dicatat sebagai asumsi skill): kontrak 1–28 Feb di tahun kabisat = 28/29 bulan → tidak berhak kompensasi, sedangkan di tahun biasa = 1 bulan → berhak. Aturan tidak merinci; skill menyebutnya asumsi.

## 3. Verifikasi temuan uji pertama
| Temuan | Hasil uji ulang | Status |
|---|---|---|
| **S1** aditivitas ganti rugi | 0 pelanggaran di ±9.000 kasus putus dini; angka contoh cocok | ✅ Tuntas |
| **S2** jam kerja | Checklist B7: "6 hari kerja = 7 jam/hari dan 40 jam/minggu (mis. Senin–Jumat 7 jam + Sabtu 5 jam) atau 5 hari kerja = 8 jam/hari dan 40 jam/minggu"; 🔴 bila > 58 jam/minggu (40 + lembur 18). SKILL.md mode Susun langkah 5 menambah cek jam kerja. Template Pasal 4 sudah benar. Sesuai PP 35/2021 Pasal 21 & 26. | ✅ Tuntas |
| **S3** periode pendek berurutan | 20+20 hari tanpa jeda → peringatan PERLU REVIEW dengan tafsir (a) Rp0 dan (b) gabungan 1,3214/12 × 5 jt = **Rp550.595** (dicek manual ✅). 3 × 10 hari → (b) Rp416.667 ✅. Dengan jeda 39 hari → tidak ada peringatan S3 (benar), ada peringatan jeda. Putus di hari pertama perpanjangan setelah 12 bulan → (a) Rp5.000.000 / (b) Rp5.013.441 ✅. SKILL.md menyuruh agent menyampaikan kedua tafsir tanpa memilih. | ✅ Tuntas |
| **R1** format rupiah | "Rp 5.000.000,-", "Rp5.000.000,00", "5.000.000.-", "IDR 5,000,000", "5 jt", "5JT", "Rp4,5jt" diterima benar; "1/1/2026-31/12/2026" & "2026-01-01-2026-12-31" diterima | ✅ |
| **R2** upah kecil | "4.500", "5.000", "499999" → peringatan **PERIKSA UPAH** + saran; "500rb" tanpa peringatan (batas < Rp500.000); SKILL.md menyuruh agent bertanya dulu | ✅ |
| **R3** banyak pekerja | Ada paragraf di Input (per orang, script per pekerja, total = jumlah) | ✅ |
| **R4** tanggal mulai tak diketahui | Ada paragraf (rumus manual, label "dihitung manual", tanggal `[isi]`) | ✅ |
| **R5** > 5 tahun | Peringatan tambahan "angka setelah batas 5 tahun hanya ilustrasi" | ✅ |

## 4. Data rusak baru
| Input | Hasil | Status |
|---|---|---|
| "Rp. 5.000.000.-" (titik setelah Rp + ".-") | ERROR "format tidak dikenali" (exit 2) | 🟢 minor, pesan jelas |
| "5 juta rupiah", "lima juta", "5jt500rb", "1e9" | ERROR jelas, exit 2 | ✅ |
| "4,5" (maksudnya 4,5 juta) | dibulatkan ke **Rp5**, PERIKSA UPAH menyarankan "Rp5.000?" | 🟢 R-baru-3: saran kurang tepat, tetapi peringatan muncul dan agent wajib bertanya |
| "5.000.000,50" | Rp5.000.001 (dibulatkan) | ✅ wajar |
| "999999999999999999" | diterima tanpa peringatan | 🟢 tidak realistis, tidak berbahaya |
| "29/2/2027", "1/13/2026" | ERROR "tidak ada di kalender" | ✅ |
| Periode tumpang tindih | ERROR "tumpang tindih" | ✅ |
| Periode spasi saja, upah minimum "abc" | ERROR jelas | ✅ |
| `--tunjangan-tetap -100rb` | argparse menampilkan usage (dianggap opsi), bukan pesan ramah; `--tunjangan-tetap=-100rb` → ERROR "nilai negatif" | 🟢 minor |
| Berhenti = akhir kontrak | dihitung normal + peringatan | ✅ |
| 1 Jan 1990 – 31 Des 2100 | MELEBIHI + ilustrasi, tanpa crash | ✅ |

## 5. Ulang skenario 02 (mode Periksa, draf kafe Yogyakarta) dengan SKILL.md v1.0.1
Input sama dengan `02-periksa-draf-kafe.md`. Script (3 periode × 24 bulan, 2,8 jt + 200 rb) → total 72 bulan, **MELEBIHI** (batas 31 Oktober 2031), kompensasi 3 × Rp6.000.000 = Rp18.000.000 + peringatan baru "angka setelah batas 5 tahun hanya ilustrasi". Ilustrasi tambahan: bila pengusaha memutus di akhir "masa percobaan" (31 Jan 2027) → kompensasi Rp750.000 + ganti rugi (24 − 3) × 3 jt = **Rp63.000.000** — memperkuat alasan menghapus Pasal 3.

Output agent (ringkas):

HASIL PERIKSA DRAF PKWT — Barista Kopi Senja
Ringkasan: **9 🔴 tinggi · 4 🟠 sedang · 2 🟢 rendah → Konsultasikan dulu** (barista kafe umumnya pekerjaan tetap; rencana total 6 tahun).

| # | Pasal | Temuan | Risiko | Dasar | Usulan (siap tempel) |
|---|---|---|---|---|---|
| 1 | Pasal 3 masa percobaan | Masa percobaan di PKWT | 🔴 | UU 13/2003 Pasal 58 jo. UU 6/2023; PP 35/2021 Pasal 12 | "Perjanjian ini tidak mensyaratkan masa percobaan kerja." |
| 2 | Pasal 1 barista tanpa alasan waktu tertentu | Pekerjaan tetap di-PKWT | 🔴 | UU 13/2003 Pasal 59; PP 35/2021 Pasal 4–5 | Tulis alasan sementara yang jujur, atau PKWTT |
| 3 | Pasal 2 2 + 2 × 2 tahun | 72 bulan > 5 tahun; batas 31 Okt 2031 | 🔴 | PP 35/2021 Pasal 8; Putusan MK 168/PUU-XXI/2023 | "... total seluruh PKWT tidak melebihi 5 (lima) tahun." |
| 4 | Pasal 5 tanpa BPJS | Tanpa BPJS TK & Kesehatan | 🔴 | UU 24/2011 Pasal 15 | Wajib daftar, iuran sesuai porsi |
| 5 | Pasal 6 denda Rp10 jt | Penalti berlebihan (≈ 3,3× upah) | 🔴 | UU 13/2003 Pasal 62; checklist C1 | Ganti rugi dua arah sebesar upah sisa kontrak |
| 6 | Pasal 6 gaji terakhir hangus | Upah yang sudah dikerjakan ditahan | 🔴 | checklist C1 | Hapus |
| 7 | Tanpa pasal kompensasi | Tanpa uang kompensasi | 🔴 | UU 13/2003 Pasal 61A; PP 35/2021 Pasal 15–17 | masa kerja ÷ 12 × upah; 24 bulan = Rp6.000.000 (enam juta rupiah) |
| 8 | Pasal 3 putus sewaktu-waktu tanpa kompensasi | Pengusaha memutus tanpa ganti rugi | 🔴 | UU 13/2003 Pasal 62; PP 35/2021 Pasal 17 | Ganti rugi dua arah + kompensasi masa dijalani |
| 9 | Pasal 7 6 hari 10.00–22.00, istirahat 1 jam | 11 × 6 = **66 jam/minggu** > 58 (40 + lembur 18) | **🔴** (v1.0.0: 🟠) | PP 35/2021 Pasal 21 & 26 | "Waktu kerja 7 jam/hari dan 40 jam/minggu untuk 6 hari kerja (mis. Senin–Jumat 7 jam, Sabtu 5 jam); lembur dengan persetujuan, maks. 4 jam/hari & 18 jam/minggu, dibayar 1/173 × upah sebulan per jam." |
| 10–13 | THR tidak disebut; cuti tidak diatur; tidak ada rencana pencatatan; Pasal 8 "diatur kemudian" (isi minimal kurang); upah Rp3 jt vs UMK `[isi: UMK Kab. Sleman 2026 — cek situs Disnaker]` | masing-masing | 🟠 | checklist B5, B8, A7, A6, B1 | kalimat pengganti per butir (THR sesuai peraturan, cuti 12 hari setelah 12 bulan, pencatatan daring maks. 3 hari kerja) |
| 14–15 | Terbilang, rangkap/paraf | | 🟢 | | |

Catatan penguji: usulan jam kerja kini aritmetis benar (bukan lagi "7 jam × 6 hari"). THR yang tidak disebut di draf diperlakukan agent sebagai 🟠 "belum diatur" (checklist B5 memberi 🔴 hanya untuk "tidak disebut atau hanya untuk karyawan tetap" — ambigu untuk draf yang sekadar diam); tidak mengubah kesimpulan. UMK tidak dikarang. Disclaimer baku dengan status RUU ditempel. Hasil: ✅ **Lulus**, temuan utama (percobaan, denda Rp10 jt, tanpa BPJS, 6 tahun) semua 🔴 dengan kalimat pengganti.

## 6. Kepatuhan format
- SKILL.md **139 baris** (< 300). Frontmatter hanya `name` & `description`.
- Disclaimer baku (dasar-hukum §6) memuat MK 168/PUU-XXI/2023, tenggat UU baru Oktober 2026, status RUU belum disahkan per 25 Sep 2026; SKILL.md bagian Batasan menyebutkannya; footer script ada.
- Tidak ada angka lama (Rp4.548.387 / Rp17.500.000 / Rp16.800.000) di SKILL.md, README, atau references.

## 7. Temuan baru (semua rendah)
- **R-baru-1 — Label sisa masa berbeda dari angka yang dipakai.** Output: "Sisa kontrak 16 Februari 2026 s.d. 31 Maret 2026 = 1 bulan 16 hari -> (3 - 1,5357) = 1,4643 bulan". "1 bulan 16 hari" bila dihitung dengan Rumus no. 2 dari 16 Feb = 1 + 16/31 = 1,5161, bukan 1,4643. Rumusnya ditampilkan sehingga angka akhirnya jelas, tetapi pengguna yang mencocokkan manual bisa bingung. Usulan: tampilkan hanya tanggal sisa + "(3 − 1,5357) = 1,4643 bulan", atau beri catatan "label hari hanya informasi".
- **R-baru-2 — Rentang terbalik saat sisa 0.** Berhenti di hari terakhir periode awal sebelum perpanjangan: "Sisa kontrak 1 Januari 2027 s.d. 31 Desember 2026 = 0 bulan ... Rp0". Nilai benar (+ peringatan perpanjangan belum dimulai), tampilan membingungkan. Usulan: jangan cetak blok ganti rugi (atau tulis "tidak ada sisa di periode berjalan").
- **R-baru-3 — `--metode bulan-penuh` tidak aditif.** Kompensasi memakai bulan penuh (1 bulan) tetapi ganti rugi tetap pecahan (1,4643): 1 + 1,4643 ≠ 3. Bukan default; SKILL.md tidak menjelaskan kapan opsi ini dipakai. Usulan: jelaskan satu kalimat, atau jadikan konsisten.
- **R-baru-4 — Saran PERIKSA UPAH untuk "4,5"** menyarankan Rp5.000 (maksud pengguna kemungkinan 4,5 juta). Agent tetap diwajibkan bertanya.
- **R-baru-5 — Checklist B5 THR** ambigu untuk draf yang sekadar tidak menyebut THR (🔴 vs 🟠).

## 8. Skor: **9/10** (lihat HASIL-UJI.md bagian "Uji ulang v1.0.1").
