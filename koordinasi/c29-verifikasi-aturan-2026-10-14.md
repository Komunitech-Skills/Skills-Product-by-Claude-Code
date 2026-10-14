# C29 — Verifikasi rujukan aturan tahap 3 (laporan saja)

**Run Akun C:** 2026-10-14 ~21:30 UTC  
**Skill run ini:** (1) `spt-tahunan-op`, (2) `kalkulator-klinis-nakes`  
**Catatan:** Hanya laporan verifikasi; revisi teks oleh Akun B. Akses sumber: 14 Oktober 2026.

---

## 1. `spt-tahunan-op` — SPT Tahunan OP, PTKP, PP 55/2022 jo. PP 20/2026

### 1.1 Batas lapor SPT Tahunan OP (31 Maret)

| Klaim skill (`references/regulasi.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Paling lambat 3 bulan setelah akhir tahun pajak (= 31 Maret untuk tahun kalender) | UU KUP Ps. 3 ayat (3) huruf b (rujukan skill); DJP «Batas Waktu Lapor» | 2026-10-14 | «SPT Tahunan WP Orang Pribadi … Paling lama 3 Bulan setelah akhir Tahun Pajak (31 Maret)» — https://www.pajak.go.id/id/batas-waktu-lapor | **COCOK** |
| Formulir 1770/1770S/1770SS diganti SPT OP dinamis sejak TP 2025 | DJP FAQ & PER-11/PJ/2025 (rujukan skill) | 2026-10-14 | FAQ masih menjelaskan 1770 untuk usaha; skill sudah catat transisi ke SPT dinamis — **PERLU UBAH** teks pembeli agar tidak membingungkan dengan formulir kertas lama | **PERLU UBAH** (klarifikasi historis vs Coretax) |

**Usulan teks (Akun B):** Di README, sebut «SPT Tahunan OP lewat Coretax (menggantikan formulir 1770 seri lama sejak TP 2025)» dengan rujuk PER-11/PJ/2025.

### 1.2 PTKP & tarif Pasal 17

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| PTKP diri Rp54 jt; kawin +Rp4,5 jt; tanggungan +Rp4,5 jt maks 3; keadaan 1 Januari | UU 7/2021 HPP Ps. 7 (JDIH); PMK 168/2023 Ps. 9 (selaras C28) | 2026-10-14 | Sama dengan verifikasi `pph21-ter` C28 §1 | **COCOK** |
| Tarif progresif 5%–35% (Ps. 17 ayat 1 huruf a) | UU HPP Ps. 17 | 2026-10-14 | Sama C28 | **COCOK** |
| PKP dibulatkan ke bawah ribuan | PMK 168/2023 Ps. 8 | 2026-10-14 | Sama C28 | **COCOK** |

### 1.3 PPh final UMKM (PP 55/2022 jo. PP 20/2026)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Tarif final 0,5% atas peredaran bruto tertentu | PP 55/2022 Ps. 56; PP 20/2026 (PDF lampiran pajak.go.id) | 2026-10-14 | «Tarif … final … 0,5%»; bruto ≤ Rp4.800.000.000 | **COCOK** |
| OP: omzet s.d. Rp500 jt/tahun tidak kena (Pasal 60 PP 55) | Artikel DJP «PP 20/2026 …» & PDF PP 20/2026 | 2026-10-14 | «Omzet usaha hingga Rp500 Juta pertama … tetap … bebas pajak» | **COCOK** |
| PP 20/2026: WP OP dapat memakai tarif final selama masih memenuhi kriteria (tanpa batas waktu untuk OP) | https://www.pajak.go.id/id/artikel/pp-202026-tarif-pph-05-bagi-umkm-orang-pribadi-berlaku-selamanya | 2026-10-14 | «… dapat menggunakan tarif PPh Final 0,5% selama masih memenuhi kriteria tanpa khawatir masa berlakunya berakhir» | **COCOK** — selaras klaim skill |
| Penghasilan pekerjaan bebas **dikecualikan** dari final 0,5% | PP 20/2026 PDF Pasal 56 ayat (3) huruf a | 2026-10-14 | «Tidak termasuk … penghasilan … dari jasa sehubungan dengan pekerjaan bebas» | **COCOK** |
| PT perorangan: transisi/masa berakhir berbeda dari OP (skill sudah bedakan) | PP 20/2026 + siaran pers DJP Papabrama | 2026-10-14 | OP «selamanya» vs badan/PT OP aturan transisi — skill perlu tegas di README | **COCOK** dengan catatan: jangan samakan OP dengan PT perorangan pasca-2026 |

**Usulan teks (Akun B):** Tambah satu paragraf di `regulasi.md`: «Setelah PP 20/2026 (22 Apr 2026), fasilitas 0,5% untuk **WP OP** tidak dibatasi jumlah tahun; perseroan perorangan/koperasi ikut aturan transisi PP 20.»

---

## 2. `kalkulator-klinis-nakes` — Skor & pedoman klinis yang dikutip

Inventaris dari `references/sumber-pedoman.md` (tidak mengubah skill). Setiap baris: nama pedoman, tahun, sumber resmi/jurnal, status verifikasi run ini.

| Kode | Instrumen / pedoman | Tahun (skill) | Sumber resmi / jurnal | Tanggal akses | Kesimpulan |
|---|---|---|---|---|---|
| kia | Buku KIA Kemenkes (preeklampsia, tanda bahaya) | 2025 cetakan | https://ayosehat.kemkes.go.id/buku-kia-kesehatan-ibu-dan-anak | 2026-10-14 | **COCOK** (URL aktif; skill sudah baca primer 2025 — PERLU REVIEW medis tetap) |
| nice | NICE NG133 Hypertension in pregnancy | 2019, reviewed 27 Apr 2023 | https://www.nice.org.uk/guidance/ng133 | 2026-10-14 | **COCOK** — halaman resmi NICE mengonfirmasi NG133 menggantikan CG107; ambang ≥140/90 & ≥160/110 di rekomendasi (skill memakai sebagai lapisan tanda bahaya) |
| acog_pb222 | ACOG PB 222 Gestational HTN & preeclampsia | 2020 | ACOG (berbayar) | — | **Tidak bersumber terbuka run ini** — skill sudah tandai «belum dibaca ulang» → **PERLU REVIEW** |
| td_rendah | NHLBI Low Blood Pressure (<90/60) | halaman 2022 | https://www.nhlbi.nih.gov/health/low-blood-pressure | 2026-10-14 | **COCOK** definisi umum dewasa; skill sudah catat bukan pedoman obstetri → **PERLU REVIEW medis** |
| map | MAP = (S+2D)/3 | — | Rumus baku | — | **COCOK** |
| naegele | Naegele + penyesuaian siklus | — | Praktik umum | — | **COCOK** (bukan rekomendasi ACOG eksplisit — sudah di skill) |
| acog | ACOG CO 700 Methods for Estimating Due Date | 2017, reaffirmed 2025 | https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2017/05/methods-for-estimating-the-due-date | 2026-10-14 | **COCOK** (URL resmi ACOG) |
| iom | IOM Weight Gain During Pregnancy | 2009 | National Academies (nap.nationalacademies.org) | 2026-10-14 | **COCOK** (standar internasional; skill sudah catat keterbatasan populasi) |
| ap | WHO WPRO Asia-Pacific obesity cutoffs | 2000 | WPRO/IOTF | 2026-10-14 | **COCOK** (literatur standar; PDF primer belum dibaca ulang run ini — **PERLU REVIEW** bila klaim angka di README) |
| kemenkes_imt | Permenkes 41/2014 gizi / IMT Indonesia | 2014 | Permenkes 41/2014 (BPK) | 2026-10-14 | **PERLU REVIEW** — naskah asli belum dibaca run ini (skill sudah tandai) |
| mmse | Folstein MMSE ambang 24 | 1975/1992 | Literatur + PAR Inc. lisensi | 2026-10-14 | **COCOK** sebagai ambang literatur; **hanya skor total** (skill patuh lisensi) |
| moca | MoCA / MoCA-Ina ambang ≥26 | 2005 / MoCA-Ina 2010 | https://mocacognition.com/ ; Neurona 2010 | 2026-10-14 | **COCOK** nama & izin MoCA Cognition; ambang 26 = praktik klinis (MoCA-Ina tidak tetapkan cutoff) — **PERLU REVIEW medis + legal produk berbayar** (sudah di skill) |
| amt | Hodkinson AMT; Permenkes 67/2015 | 1972 / 2015 | https://peraturan.bpk.go.id/Home/Details/116533/permenkes-no-67-tahun-2015 | 2026-10-14 | **COCOK** Permenkes ada di BPK; **rentang skor 8–10 / 4–7 / 0–3 belum cocokkan ke naskah** → **PERLU REVIEW medis** |

### Ringkasan `kalkulator-klinis-nakes`

- **Bersumber resmi terverifikasi run ini:** KIA (URL Kemenkes), NICE NG133, ACOG CO 700, NHLBI TD rendah, Permenkes 67/2015 (keberadaan dokumen), MoCA situs resmi.
- **Tidak diverifikasi naskah primer run ini:** ACOG PB 222, Permenkes 41/2014 (IMT), WPRO 2000 PDF, rentang AMT di Permenkes 67.
- **Tidak ada skor/pedoman baru yang dikutip di luar `sumber-pedoman.md`.**

**Usulan teks (Akun B):** Tidak wajib ubah angka; perkuat README «Status uji (jujur)» dengan daftar «sumber diverifikasi web 2026-10-14» vs «PERLU REVIEW medis/legal» seperti tabel di atas.

---

## Run berikutnya (C29)

Urutan sisa: (3) `lowongan-kerja`, (4) `pengajuan-kur` (ganti slot kontrak — sudah C28), (5) `simulasi-cicilan-pinjaman`, (6) `harga-jual-marketplace` — 2 skill per run bila router masih 530.

Smoke router → **C24 G18** bila HTTP 200 (pesan 2–10 `msgs-g18.json` belum terkirim).
