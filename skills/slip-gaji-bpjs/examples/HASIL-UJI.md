# HASIL UJI — slip-gaji-bpjs v1.0.1 (uji ulang)

- Tanggal: 2026-09-23
- Penguji: agent penguji independen (simulasi, Claude Code)
- Versi diuji: **v1.0.1** (commit `1ead12f`), menggantikan hasil uji v1.0.0 (skor 6, REVISI)
- Folder kerja: `/tmp/uji-slip-gaji-bpjs/`, `/tmp/uji-pph/`

## Verifikasi independen
Kalkulator payroll & PPh 21 penguji ditulis sendiri (tidak mengimpor script skill). Tabel TER diurai sendiri dari PDF PP 58/2023, aturan dari PMK 168/2023, PMK 105/2025, dan PP 35/2021.

| Uji | Jumlah kasus | Selisih |
|---|---:|---:|
| Slip bulanan acak: gaji, tunjangan tetap/tidak tetap, lembur hari kerja (pecahan jam) & hari libur pola 5/6 hari, bonus, kasbon, UMK, 5 tarif JKK, batas JP Feb vs Sep 2026 (regresi v1.0.0) | 3.000 | 0 |
| Desember/bulan berhenti: data Jan s.d. bulan lalu acak, `jumlah_bulan_kerja` atau `bulan_mulai` (pegawai baru), dengan/tanpa DTP, dengan/tanpa `bruto_tetap_januari` | 2.024 | 0 |
| Desember/berhenti tanpa `jumlah_bulan_kerja`/`bulan_mulai` → wajib ERROR (kode 2) | 976 | 0 |
| DTP masa Mei 2026/2027, gaji di sekitar Rp 10 jt, dengan/tanpa `bruto_tetap_januari`: status DTP, PPh, PPh disetor | 1.000 | 0 |

Hasil kasus lama:
- **Cacat berat v1.0.0 (DTP untuk gaji Rp 15 jt):** kini DTP ditolak dengan ⚠️ "TIDAK memenuhi syarat… lebih dari Rp 10.000.000 (PMK 105/2025 Pasal 4 ayat 2 huruf b)", dan "Setor PPh 21: Rp 1.089.270". **Tertutup.**
- **Cacat sedang v1.0.0 (Desember pegawai masuk September):** tanpa `bulan_mulai` → ERROR yang jelas; dengan `--bulan-mulai 9` → pengembalian Rp 2.726.150 (benar; v1.0.0 memberi Rp 2.832.650). **Tertutup.**
- Contoh S1–S3 tidak berubah angkanya (regresi 0). Contoh S4 diperbarui (menambahkan `--bulan-mulai 1`).
- Uji otomatis skill: `test_payroll.py` OK.

Sumber aturan (tetap dari uji v1.0.0): PP 35/2021 Pasal 31–33 dibaca langsung. Iuran BPJS TK (JHT 3,7/2%, JKK, JKM 0,3%, JP 2/1%) dari artikel resmi bpjsketenagakerjaan.go.id. Batas JP Rp 11.086.300 mulai Maret 2026 dari akun resmi @BPJSTKinfo dan SE B/1226/022026 (dikutip bsc.co.id). Perpres 64/2020 tidak dibaca ulang penguji.

## Skor

| Kriteria | Skor (1–10) |
|---|---:|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 9 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 10 |
| **SKOR AKHIR** | **9** |

- Uji A/B (`00-pembanding-tanpa-skill.md`): dengan skill jelas lebih baik.
- Banding pesaing (`00-banding-pesaing.md`): menang telak.
- Audit keamanan: tetap aman. Hanya library standar; tidak ada jaringan, kredensial, atau perintah destruktif di script produk.

## Cacat tersisa
**Berat:** tidak ada.

**Sedang:** tidak ada.

**Ringan:**
1. Bila `bruto_tetap_januari` kosong, syarat DTP dicek memakai gaji bulan berjalan (ada ⚠️). Karyawan yang naik gaji setelah Januari (contoh resmi PMK 105 Tuan B) bisa ditolak DTP padahal berhak. Saran: di SKILL.md bagian Langkah, minta agent menanyakan gaji tetap Januari bila `dtp=ya` dan gaji bulan ini > Rp 10 jt.
2. Dasar iuran BPJS Kesehatan = gaji pokok + tunjangan tetap masih berstatus "Sekunder" di `references/regulasi.md`. Saran: verifikasi ke peraturan BPJS Kesehatan.
3. Pembulatan iuran dan PPh belum dicocokkan dengan aplikasi BPJS/Coretax (sudah diakui di skill).

## Status
**LULUS** (skor 9).

## Riwayat revisi 1.0.6 (2026-10-05) — menunggu uji ulang independen; PERLU REVIEW konsultan pajak
- Pemicu: temuan penilai gelombang 7 di skill `pph21-ter` (uang diterima DTP ditulis gaji + DTP). Skill ini diperiksa dengan teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5 ayat 1 & 5, Pasal 6 ayat 6, Lampiran B).
- Hasil: angka `scripts/payroll.py` **sudah benar** — potongan "PPh 21" tetap diisi, pendapatan "PPh 21 DTP dibayar tunai" bernilai sama, `pph_disetor` = 0. Contoh TK/0 gaji Rp 6.000.000, tanpa JP: PPh dipotong Rp 47.043, DTP tunai Rp 47.043, setoran Rp 0, take home pay Rp 5.820.000 (= gaji − BPJS karyawan; tidak berubah dari versi sebelumnya).
- Perubahan: fungsi `catatan_dtp` (slip Markdown & HTML) menampilkan PPh dipotong, DTP tunai, setoran ke negara; tes `test_dtp_dipotong_lalu_dibayar_tunai`; SKILL.md (rumus + checklist), `references/regulasi.md`, `references/dtp-pmk105.md` (baru). `scripts/test_payroll.py`: 27 tes OK.

## Uji ulang DTP PMK 105/2025 — 2026-10-05

Penguji independen (bukan pembuat; tidak mengubah kode/SKILL.md). Teks PMK 105/2025 dibaca langsung: Pasal 2 ayat 1 (PPh 21 **wajib dipotong**), Pasal 2 ayat 3 (Masa Pajak Januari–Desember 2026), Pasal 3 (industri alas kaki, tekstil & pakaian jadi, furnitur, kulit, pariwisata + KLU Lampiran A, 133 baris), Pasal 4 ayat 2–4 (pegawai tetap: bruto tetap & teratur Januari 2026/bulan pertama kerja **≤ Rp10.000.000**; tidak tetap: rata-rata ≤ Rp500.000/hari atau ≤ Rp10.000.000 bila bulanan), Pasal 5 ayat 1–2 (DTP **dibayar tunai**, bukan penghasilan kena pajak), Pasal 5 ayat 5 (kelebihan DTP tidak dikembalikan), Pasal 6 ayat 4–6 (lapor SPT Masa paling lambat 31 Januari 2027, lewat batas → PPh yang telah dipotong wajib disetor), Lampiran B (Tuan A 8.000.000 − 120.000 + 120.000 = 8.000.000; Tuan B K/1). Kesimpulan mekanisme: **dipotong = PPh TER/Pasal 17, DTP tunai = nilai sama, setoran ke negara Rp 0, diterima = bruto − potongan lain** (bukan bruto + DTP).

Metode: kalkulator independen Python `Decimal` milik penguji (tabel TER ditulis ulang, tidak mengimpor script skill), dicocokkan dulu dengan Lampiran B PMK 105/2025 (Tuan A Desember 540.000 / setahun 1.860.000; Tuan B Desember 480.000 / setahun 4.050.000 — cocok). Lalu CLI skill dijalankan (`--format json`/`--json`) dan dibandingkan per kolom: dipotong, DTP tunai, disetor ke negara, diterima.

| # | Kasus (CLI `payroll.py`, JKK 0,24%, BPJS lengkap) | Bruto pajak | Dipotong | DTP tunai | Disetor | Take home pay | Selisih |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | TK/0 Rp6.000.000, Mar 2026, DTP | 6.272.400 | 47.043 | 47.043 | 0 | 5.760.000 | 0 |
| 2 | TK/0 Rp6.000.000 tanpa DTP (sektor tidak memenuhi) | 6.272.400 | 47.043 | 0 | 47.043 | 5.712.957 | 0 |
| 3 | K/1 Rp9.500.000 DTP (TER B 1,5%) | 9.931.300 | 148.969 | 148.969 | 0 | 9.120.000 | 0 |
| 4 | TK/0 tepat Rp10.000.000 DTP | 10.454.000 | 261.350 | 261.350 | 0 | 9.600.000 | 0 |
| 5 | TK/0 Rp10.000.001 DTP → ditolak otomatis | 10.454.001 | 261.350 | 0 | 261.350 | 9.338.651 | 0 |
| 6 | TK/0 Rp6.000.000 + THR Rp6.000.000 bulan sama, DTP | 12.272.400 | 490.896 | 490.896 | 0 | 11.760.000 | 0 |
| 7 | TK/0 Rp6.000.000 DTP periode 2027-03 → di luar masa | 6.272.400 | 47.043 | 0 | 47.043 | 5.712.957 | 0 |
| 8 | TK/0 Rp6.000.000 Desember 2026 DTP (hitung ulang Pasal 17; Jan–Nov 11 × 6.272.400, PPh 11 × 47.043, iuran 11 × 180.000) | 6.272.400 | 249.777 | 249.777 | 0 | 5.760.000 | 0 |

Take home pay DTP = gaji − iuran BPJS karyawan (PPh dipotong dan dikembalikan tunai), cocok dengan Lampiran B. Slip Markdown & HTML menulis "PPh 21 Rp 47.043 tetap dipotong, lalu Rp 47.043 dibayar tunai kembali … Setoran PPh 21 ke negara: Rp 0"; ringkasan "Setor PPh 21 (tanpa DTP): Rp 0". SKILL.md (rumus & checklist) sesuai.

Lain-lain: `test_payroll.py` 27 tes OK · `validate.py` ✅ · `uji_openclaw.sh` (instalasi uji terpisah) 117/117.

**Total selisih: 0 dari 8 kasus.** Cacat baru: tidak ada. Catatan: periode 2027 butuh `--batas-jp` manual (perilaku lama, pesan jelas).

**Skor: 9/10. Verdik: LULUS uji ulang angka DTP** (tetap **PERLU REVIEW konsultan pajak**).
