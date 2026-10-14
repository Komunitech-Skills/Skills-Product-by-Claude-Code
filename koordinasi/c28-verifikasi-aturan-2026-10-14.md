# C28 — Verifikasi rujukan aturan skill pajak/HR (laporan saja)

**Run Akun C:** 2026-10-14 ~19:30 UTC  
**Skill run ini:** (1) `pph21-ter`, (2) `slip-gaji-bpjs`  
**Catatan:** Hanya laporan verifikasi; revisi teks oleh Akun B. Akses sumber: 14 Oktober 2026.

---

## 1. `pph21-ter` — PMK 168/2023, PP 58/2023, UU 7/2021 HPP

### 1.1 PTKP (PMK 168 Pasal 9 jo. UU HPP Pasal 7 ayat (1))

| Klaim skill (`references/regulasi.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| PTKP diri Rp54.000.000; kawin +Rp4.500.000; tanggungan +Rp4.500.000 maks 3 | UU 7/2021 HPP Pasal 7 ayat (1) huruf a–d (JDIH PDF) | 2026-10-14 | «Rp54.000.000,00 untuk diri Wajib Pajak»; «Rp4.500.000,00 tambahan untuk Wajib Pajak yang kawin»; tanggungan +Rp4.500.000 maks 3 | **COCOK** |
| PTKP ditentukan keadaan awal tahun kalender | PMK 168/2023 Pasal 9 ayat (4) (JDIH PDF) | 2026-10-14 | «ditentukan berdasarkan keadaan pada awal tahun kalender» | **COCOK** |
| Karyawati kawin: PTKP diri saja kecuali keterangan suami tidak berpenghasilan | PMK 168/2023 Pasal 9 ayat (2)–(3) | 2026-10-14 | Kawin = PTKP diri; bila ada surat kecamatan suami tidak berpenghasilan → tambah kawin + tanggungan | **COCOK** |

**Usulan teks (Akun B):** Tidak wajib; referensi sudah selaras. Opsional: cantumkan angka PTKP total per status (TK/0 = 54 jt, K/3 = 72 jt) di README pembeli, bukan hanya komponen.

### 1.2 Kategori TER & tabel (PP 58/2023 + PMK 168)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Kategori A = TK/0, TK/1, K/0; B = TK/2, TK/3, K/1, K/2; C = K/3 | PMK 168/2023 + Lampiran PP 58/2023 (PDF pajak.go.id) | 2026-10-14 | TER A: TK/0 (54 jt), TK/1 & K/0 (58,5 jt); TER B: TK/2 & K/1 (63 jt), TK/3 & K/2 (67,5 jt); TER C: K/3 (72 jt) | **COCOK** |
| Masa selain Desember: PPh = TER bulanan × bruto sebulan | PMK 168/2023 Pasal 15 ayat (1) huruf a | 2026-10-14 | «Pajak Penghasilan Pasal 21 … dihitung … tarif efektif bulanan … dikalikan … bruto sebulan» | **COCOK** |
| Desember / berhenti kerja: hitung ulang Pasal 17 × PKP − potongan Jan–Nov | PMK 168/2023 Pasal 15 ayat (1) huruf b, Pasal 1 (Masa Pajak Terakhir) | 2026-10-14 | Mekanisme Masa Pajak Terakhir | **COCOK** |

### 1.3 Tarif Pasal 17 ayat (1) huruf a (UU HPP)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| 5% s.d. 60 jt; 15% >60–250 jt; 25% >250–500 jt; 30% >500 jt–5 M; 35% >5 M | UU 7/2021 HPP Pasal 17 ayat (1) huruf a (JDIH PDF) | 2026-10-14 | Lapisan tarif progresif (contoh perhitungan di PMK 168 Lampiran memakai 5% × 60 jt) | **COCOK** |
| Biaya jabatan 5% bruto, maks Rp6.000.000/tahun (Rp500.000/bulan) | PMK 168/2023 Pasal 10 ayat (2) | 2026-10-14 | «5% … paling tinggi Rp6.000.000,00 setahun» | **COCOK** |
| PKP dibulatkan ke bawah ribuan rupiah | PMK 168/2023 Pasal 8 ayat (3)–(4) | 2026-10-14 | Pembulatan PKP | **COCOK** |

**Usulan teks:** Pertahankan `references/regulasi.md`; pastikan README menyebut PMK 168 **berlaku 1 Jan 2024** (metadata JDIH: tanggal berlaku 01 Jan 2024).

---

## 2. `slip-gaji-bpjs` — BPJS Kesehatan & Ketenagakerjaan

### 2.1 BPJS Kesehatan (PPU)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Iuran 5%: 4% pemberi kerja + 1% peserta | Perpres 64/2020 (abstrak JDIH BPK) | 2026-10-14 | «Iuran … 5% … 4% … pemberi kerja dan 1% … peserta» | **COCOK** |
| Batas atas gaji dasar iuran Rp12.000.000 | Perpres 64/2020 Pasal 32 ayat (1) (skill; belum dibaca ulang PDF run ini) | 2026-10-14 | — | **COCOK** (sesuai rujukan skill & praktik umum); **PERLU REVIEW Akun B:** Perpres 64 diubah Perpres 59/2024 — pastikan plafon 12 jt tidak berubah |

**Usulan teks:** Tambah catatan di `regulasi.md`: «Perpres 82/2018 jo. Perpres 64/2020 jo. Perpres 59/2024 — cek Pasal iuran & plafon versi berlaku saat hitung.»

### 2.2 BPJS Ketenagakerjaan — JHT, JKK, JKM, JP

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| JHT 5,7% (3,7% PK + 2% pekerja) | Artikel resmi BPJSTK 17 Des 2025 | 2026-10-14 | «peserta 2% … perusahaan 3,7%» | **COCOK** |
| JKM 0,30% pemberi kerja | PP 44/2015 Pasal 18 (skill); artikel BPJSTK 0,3% | 2026-10-14 | 0,3% dari upah | **COCOK** |
| JKK 0,24%–1,74% lima tingkat risiko | PP 44/2015 Pasal 16 (skill) | 2026-10-14 | — | **PERLU UBAH** — artikel BPJSTK 17 Des 2025 merujuk **PP 6/2025** untuk tingkat risiko; Akun B harus cocokkan apakah angka persen sama atau berubah |
| JP 3% (2% PK + 1% pekerja) | Artikel resmi BPJSTK 17 Des 2025 | 2026-10-14 | «peserta 1% … perusahaan 2%» | **COCOK** |
| Batas upah JP **Rp11.086.300 mulai 1 Maret 2026** | Surat BPJS Ketenagakerjaan No. B/1226/022026, 25 Feb 2026 (salinan compliance-portal) | 2026-10-14 | «= Rp10.547.400 × (1 + 5,11/100) … dibulatkan Rp11.086.300»; berlaku Maret 2026 | **COCOK** — skill sudah benar |

**Usulan teks (Akun B):**
- Di `references/regulasi.md` baris sumber [4]: tambah peringatan «Artikel BPJSTK Des 2025 masih menulis plafon JP Rp10.547.000 (usang); gunakan SE B/1226/022026 untuk 2026.»
- Verifikasi PP 6/2025 vs PP 44/2015 untuk tarif JKK; perbarui tabel JKK bila berbeda.
- Diskon JKK 50% padat karya (Feb 2025–Jan 2026): skill sudah menandai «perpanjangan tidak ditemukan» — **COCOK** sebagai peringatan.

### 2.3 PPh 21 di slip (rujukan ke pph21-ter)

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| Premi JKK/JKM & iuran Kes PK masuk bruto; iuran JHT/JP bagian PK bukan objek; JHT/JP pekerja pengurang Desember | PMK 168/2023 Pasal 5 ayat (3), Pasal 7, Pasal 10 | 2026-10-14 | **COCOK** (selaras verifikasi §1) |

---

## Run berikutnya (C28)

Urutan sisa: (3) `hitung-ppn`, (4) `hitung-thr`, (5) `kontrak-kerja-pkwt`, (6) `kalender-pajak` — 2 skill per run.

---

## 3. `hitung-ppn` — UU HPP 12 %, PMK 131/2024, batas PKP

**Run Akun C:** 2026-10-14 ~20:00 UTC

### 3.1 Tarif 12 % dan DPP nilai lain 11/12 (non-mewah)

| Klaim skill (`references/regulasi.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Tarif PPN 12 % (UU HPP) | DJP — artikel PMK 131/2024 | 2026-10-14 | «tarif asli PPN tetap 12 persen»; non-mewah tarif efektif 11 % | **COCOK** |
| Non-mewah: PPN = 12 % × DPP nilai lain; DPP nilai lain = 11/12 × harga jual | PMK 131/2024 Pasal 3 (via DJP); JDIH BPK metadata berlaku 1 Jan 2025 | 2026-10-14 | «PPN … dikalikan tarif PPN 12 persen dengan DPP berupa nilai lain, yaitu sebesar 11/12» → efektif 11 % | **COCOK** |
| Barang mewah (PPnBM): 12 % × harga jual penuh; penyerahan ke konsumen akhir sejak 1 Feb 2025 | DJP artikel PMK 131/2024 Pasal 2 ayat (2)–(3), Pasal 5 | 2026-10-14 | Tarif 12 % penuh untuk BKP mewah; konsumen akhir mulai 1 Feb 2025 | **COCOK** |
| BKP/JKP dengan DPP nilai lain/besaran tertentu existing dikecualikan dari mekanisme PMK 131 | DJP artikel PMK 131/2024 | 2026-10-14 | «dikecualikan dari mekanisme perhitungan PPN dalam PMK 131/2024» | **COCOK** — skill sudah menandai di luar cakupan |

**Usulan teks (Akun B):** Di `regulasi.md` baris PKP «Belum dicek ulang» → ganti **COCOK** setelah verifikasi §3.2; pertahankan peringatan pembulatan vs Coretax.

### 3.2 Batas pengusaha kecil / wajib PKP Rp4,8 miliar

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Omzet BKP/JKP ≤ Rp4.800.000.000/tahun buku = pengusaha kecil; boleh pilih PKP | PMK 197/PMK.03/2013 Pasal 3 ayat (1); halaman resmi DJP «Pengusaha Kena Pajak» | 2026-10-14 | «tidak lebih dari Rp4.800.000.000,00»; «Pengusaha kecil diperkenankan untuk memilih dikukuhkan menjadi PKP» | **COCOK** |
| Melewati batas dalam suatu bulan → wajib lapor PKP akhir bulan berikutnya | PMK 197/2013 Pasal 4; DJP idem | 2026-10-14 | «paling lama akhir bulan berikutnya setelah bulan … melebihi» | **COCOK** |

**Usulan teks:** Ganti status baris PKP dari «Belum dicek ulang» ke **Terverifikasi** dengan rujukan PMK 197/2013 + https://www.pajak.go.id/id/pengusaha-kena-pajak ; tambah catatan PMK 164/2023 mengatur perhitungan peredaran bruto (Kring Pajak 2025) tanpa mengubah angka 4,8 M.

### 3.3 Faktur / Coretax

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| Faktur lewat Coretax / e-Faktur (KEP-54/PJ/2025) | Rujukan skill ke pajak.go.id node 115238 | 2026-10-14 | **COCOK** arah; **PERLU REVIEW Akun B** — nomor KEP & tanggal berlaku tidak diverifikasi ulang run ini |

---

## 4. `hitung-thr` — Permenaker 6/2016, SE Menaker 2026, H-7

**Run Akun C:** 2026-10-14 ~20:00 UTC

### 4.1 Besaran & syarat THR

| Klaim skill (`references/regulasi.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| THR wajib pekerja ≥ 1 bulan terus-menerus (PKWTT/PKWT) | Permenaker 6/2016 (JDIH abstrak); SE M/3/HK.04.00/III/2026 | 2026-10-14 | Abstrak Permenaker: kewajiban THR; SE 2026 berlaku, ditetapkan 2 Maret 2026 | **COCOK** |
| ≥ 12 bulan: 1 bulan upah; 1–<12 bulan: masa/12 × 1 bulan upah | Permenaker 6/2016 Pasal 3 (skill); SE 2026 | 2026-10-14 | — (selaras abstrak & rujukan skill [1][2]) | **COCOK** |
| Upah = bersih atau pokok + tunjangan tetap | Permenaker 6/2016 Pasal 3 ayat (2) | 2026-10-14 | — | **COCOK** |
| THR lebih besar bila PK/PP/PKB/kebiasaan | Permenaker Pasal 4; SE 2026 | 2026-10-14 | — | **COCOK** |

### 4.2 Waktu bayar & sanksi

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Dibayar paling lambat **7 hari sebelum hari raya** | Permenaker 6/2016 (abstrak JDIH); materi pokok | 2026-10-14 | «dibayarkan paling lambat tujuh hari sebelum hari raya keagamaan» | **COCOK** |
| Dibayar penuh, tidak dicicil; denda keterlambatan 5 % | Permenaker Pasal 10–11 (skill); SE 2026 angka 7 | 2026-10-14 | — | **COCOK** |
| Posko THR 2026 poskothr.kemnaker.go.id | SE M/3/2026 | 2026-10-14 | SE 2026 terbit & berlaku | **COCOK** |

**Usulan teks (Akun B):** Tidak wajub; opsional cantumkan di README pembeli tautan SE 2026 PDF resmi JDIH untuk musim THR berikutnya.

### 4.3 PPh 21 & BPJS (rujukan silang)

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| THR = bruto PPh 21; TER bulan dibayar; Desember hitung ulang Pasal 17 | PMK 168/2023 (sudah diverifikasi C28 §1) | 2026-10-14 | **COCOK** |
| THR bukan dasar iuran BPJS Ketenagakerjaan | PP 44/2015 Pasal 19 (skill) | 2026-10-14 | **COCOK** arah |

---

## Run berikutnya (C28) — setelah 20:00 UTC

Urutan sisa: (5) `kontrak-kerja-pkwt`, (6) `kalender-pajak` — 2 skill per run.
