# HASIL UJI — hitung-thr v1.0.1 (uji ulang)

- Tanggal: 2026-09-23
- Penguji: agent penguji independen (simulasi, Claude Code)
- Versi diuji: **v1.0.1** (commit `1ead12f`), menggantikan hasil uji v1.0.0 (skor 6, REVISI)
- Folder kerja: `/tmp/uji-hitung-thr/`, `/tmp/uji-pph/`

## Verifikasi independen
Kalkulator THR penguji ditulis sendiri (tidak mengimpor script skill). Dasarnya:
- Permenaker 6/2016 dan SE Menaker M/3/HK.04.00/III/2026, dibaca dari pindaian JDIH.
- PMK 168/2023: Mantan Pegawai (Pasal 12 ayat 8, Pasal 16 ayat 6, contoh Tuan O).
- PMK 105/2025: DTP Pasal 2 ayat 3 dan Pasal 4 ayat 2 huruf b.
- Tabel TER yang diurai sendiri dari PDF PP 58/2023.

Masa kerja dihitung ulang dengan fungsi penambahan bulan milik penguji, memakai konvensi inklusif v1.0.1.

| Uji | Jumlah kasus | Selisih |
|---|---:|---:|
| THR acak: tetap/kontrak/harian/satuan, hari raya Jan 2026–Des 2027, masa kerja 0–26 bulan (banyak di sekitar 1 dan 12 bulan), PHK 1–60 hari sebelum hari raya, PTKP acak, bruto bulan bayar ada/tidak, DTP 2026/2027 dengan/tanpa `bruto_tetap_januari`. Dibandingkan: besaran THR, PPh 21 karena THR (TER / Pasal 17 mantan pegawai / Masa Pajak Terakhir), status DTP | 4.000 | 0 |

Hasil kasus lama dan contoh resmi:
- **Contoh resmi Tuan O** (PMK 168/2023 Lampiran VI.3: 5% × Rp 60 jt = Rp 3.000.000): kasus analog (THR Rp 60 jt dibayar setelah bulan berhenti) → metode `mantan_pegawai`, **Rp 3.000.000**. Cocok.
- **Cacat berat 1 v1.0.0 (PHK 20 Feb 2027, gaji Rp 20 jt, THR dibayar 3 Mar 2027):** kini Rp 1.000.000 (Pasal 17 × bruto), sebelumnya Rp 4.600.000. **Tertutup.**
- **Cacat berat 2 v1.0.0 (DTP untuk THR Maret 2027, gaji Rp 20 jt):** kini ditolak dengan ⚠️ "hanya untuk Masa Pajak Januari–Desember 2026", dan PPh dipotong normal Rp 4.600.000. Kasus DTP yang sah (THR November 2026, gaji Rp 8 jt, `bruto_tetap_januari` Rp 8 jt) → Rp 1.000.000 (DTP), benar. **Tertutup.**
- **Cacat sedang v1.0.0 (masa kerja):** 11 Mar 2026 s.d. 10 Mar 2027 kini 12 bulan (THR penuh Rp 4.800.000). Mulai 14 Mar 2026 → 11 bulan dengan ⚠️ "kurang 3 hari lagi menjadi 12 bulan (THR penuh)". **Tertutup.**
- Contoh di SKILL.md (Budi Rp 5.500.000 / Rp 286.500; Rina Rp 3.200.000 / Rp 120.000) tetap cocok.
- Contoh `01` diperbarui: Wati kini berlabel Mantan Pegawai. Angka tetap Rp 260.000 karena 5% × Rp 5,2 jt kebetulan sama dengan selisih TER lama.
- Uji otomatis skill: `test_thr.py` OK.

## Skor

| Kriteria | Skor (1–10) |
|---|---:|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 9 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 9 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 10 |
| **SKOR AKHIR** | **9** |

- Uji A/B: dengan skill jelas lebih baik.
- Banding pesaing (adamriofc `thr-calculator`, MIT): menang telak.
- Audit keamanan: tetap aman. Hanya library standar; tanpa jaringan dan tanpa kredensial. Pengumuman tanpa nominal pribadi.

## Cacat tersisa
**Berat:** tidak ada.

**Sedang:** tidak ada.

**Ringan:**
1. THR yang dibayar di Desember atau di bulan berhenti hanya diarahkan ke `pph21-ter`/`slip-gaji-bpjs`. Saran: pakai `ter_core.hitung_masa_terakhir` (sudah tersedia di folder yang sama) dengan kolom opsional data Jan s.d. bulan lalu, agar skill mandiri.
2. PPh 21 pekerja harian/satuan atas THR tidak dihitung (hanya diarahkan). Saran: hitung dengan TER bulanan bila upah dibayar bulanan (PMK 168 Pasal 16 ayat 2 huruf c).
3. Konvensi inklusif memotong ke akhir bulan (31 Jan + 1 bulan = 28/29 Feb). Akibatnya mulai 31 Januari s.d. 27 Februari (28 hari) sudah dihitung 1 bulan. Ini kasus tepi yang menguntungkan pekerja dan sudah terdokumentasi (regulasi baris 19); cukup diketahui.
4. Bila `bruto_tetap_januari` kosong, syarat DTP memakai gaji pokok + tunjangan tetap saat ini (ada ⚠️). Karyawan yang naik gaji setelah Januari bisa ditolak padahal berhak. Saran: agent menanyakan gaji tetap Januari bila `dtp=ya`.
5. Denda keterlambatan hanya dirujuk ke Permenaker 6/2016 Pasal 10. Saran: verifikasi dan tambahkan rujukan PP 36/2021 tentang Pengupahan.

## Status
**LULUS** (skor 9).

## Riwayat revisi 1.0.9 (2026-10-05) — menunggu uji ulang independen; PERLU REVIEW konsultan pajak
- Pemicu: temuan penilai gelombang 7 di skill `pph21-ter` (uang diterima DTP ditulis gaji + DTP). Skill ini diperiksa dengan teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5 ayat 1 & 5, Pasal 6 ayat 6, Lampiran B).
- Hasil: angka `scripts/thr.py` **sudah benar** — `thr_setelah_pph` = THR bila DTP (tambahan PPh dipotong lalu dibayar tunai kembali). Contoh TK/0 gaji Rp 8.000.000, THR dibayar Juni 2026, DTP: THR diterima = THR (tidak berubah dari versi sebelumnya).
- Perubahan: kalimat penjelasan DTP di rekap (PPh dipotong, DTP tunai nilai sama, setoran ke negara Rp 0); SKILL.md; `references/dtp-pmk105.md` (baru); tes `test_dtp` diperluas. `scripts/test_thr.py`: 38 tes OK.

## Uji ulang DTP PMK 105/2025 — 2026-10-05

Penguji independen (bukan pembuat; tidak mengubah kode/SKILL.md). Teks PMK 105/2025 dibaca langsung: Pasal 2 ayat 1 (PPh 21 **wajib dipotong**), Pasal 2 ayat 3 (Masa Pajak Januari–Desember 2026), Pasal 3 (industri alas kaki, tekstil & pakaian jadi, furnitur, kulit, pariwisata + KLU Lampiran A, 133 baris), Pasal 4 ayat 2–4 (pegawai tetap: bruto tetap & teratur Januari 2026/bulan pertama kerja **≤ Rp10.000.000**; tidak tetap: rata-rata ≤ Rp500.000/hari atau ≤ Rp10.000.000 bila bulanan), Pasal 5 ayat 1–2 (DTP **dibayar tunai**, bukan penghasilan kena pajak), Pasal 5 ayat 5 (kelebihan DTP tidak dikembalikan), Pasal 6 ayat 4–6 (lapor SPT Masa paling lambat 31 Januari 2027, lewat batas → PPh yang telah dipotong wajib disetor), Lampiran B (Tuan A 8.000.000 − 120.000 + 120.000 = 8.000.000; Tuan B K/1). Kesimpulan mekanisme: **dipotong = PPh TER/Pasal 17, DTP tunai = nilai sama, setoran ke negara Rp 0, diterima = bruto − potongan lain** (bukan bruto + DTP).

Metode: kalkulator independen Python `Decimal` milik penguji (tabel TER ditulis ulang, tidak mengimpor script skill), dicocokkan dulu dengan Lampiran B PMK 105/2025 (Tuan A Desember 540.000 / setahun 1.860.000; Tuan B Desember 480.000 / setahun 4.050.000 — cocok). Lalu CLI skill dijalankan (`--format json`/`--json`) dan dibandingkan per kolom: dipotong, DTP tunai, disetor ke negara, diterima.

| # | Kasus (CLI `thr.py`, hari raya 20-03-2026, bayar 10-03-2026, PKWTT sejak 2020) | THR | Tambahan PPh (dipotong) | DTP tunai | Disetor | THR diterima | Selisih |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | TK/0 gaji Rp6.000.000, DTP — TER A 4% × 12 jt − 0,75% × 6 jt | 6.000.000 | 435.000 | 435.000 | 0 | 6.000.000 | 0 |
| 2 | TK/0 Rp6.000.000 tanpa DTP (sektor tidak memenuhi) | 6.000.000 | 435.000 | 0 | 435.000 | 5.565.000 | 0 |
| 3 | K/1 Rp9.500.000 DTP — TER B 8% × 19 jt − 1,5% × 9,5 jt | 9.500.000 | 1.377.500 | 1.377.500 | 0 | 9.500.000 | 0 |
| 4 | TK/0 tepat Rp10.000.000 DTP — 9% × 20 jt − 2% × 10 jt | 10.000.000 | 1.600.000 | 1.600.000 | 0 | 10.000.000 | 0 |
| 5 | TK/0 Rp10.000.001 DTP → ditolak otomatis | 10.000.001 | 1.600.000 | 0 | 1.600.000 | 8.400.001 | 0 |
| 6 | TK/0 Rp6.000.000 DTP, THR 2027 → di luar masa | 6.000.000 | 435.000 | 0 | 435.000 | 5.565.000 | 0 |
| 7 | Natal, bayar Desember 2026, DTP → script tidak menghitung TER dan mengarahkan ke hitung ulang setahun (Masa Pajak Terakhir) | 6.000.000 | – | – | – | – | sesuai |
| 8 | Mantan pegawai (berhenti 25-02-2026, THR dibayar Maret) `dtp=ya` → Pasal 17 5% × 6 jt, DTP tidak diterapkan + peringatan | 6.000.000 | 300.000 | 0 | 300.000 | 5.700.000 | 0 |

Teks rekap DTP: "Rp 435.000 tetap dipotong, lalu Rp 435.000 dibayar tunai kembali bersama THR, jadi THR diterima utuh; setoran PPh 21 ke negara untuk bagian ini Rp 0". JSON tidak punya kunci "disetor" terpisah (tersirat dari `dtp`), cukup karena teks menuliskannya.

Lain-lain: `test_thr.py` 38 tes OK · `validate.py` ✅ · `uji_openclaw.sh` (instalasi uji terpisah) 117/117.

**Total selisih: 0 dari 8 kasus.** Cacat baru: tidak ada. Catatan: kasus 8 (mantan pegawai) — PMK 105/2025 tidak memberi DTP bagi bukan pegawai; perlakuan konservatif skill wajar, tetap untuk review konsultan.

**Skor: 9/10. Verdik: LULUS uji ulang angka DTP** (tetap **PERLU REVIEW konsultan pajak**).

## Riwayat uji OpenClaw sebelum/sesudah per skill
| Tanggal | Versi | Uji | Tanpa skill | Dengan skill | Selisih | Verdik | Catatan |
|---|---|---|:-:|:-:|:-:|---|---|
| 2026-10-14 | 1.0.9 | OpenClaw 2026.10.2 lokal, hanya skill ini vs tanpa skill; 5 skenario (3 normal + 1 Telegram + 1 input kurang); penguji independen | 6,1 | 8,0 | +1,9 | **LULUS** (tipis, tepat di ambang 8) | Rincian di `00-openclaw-sebelum-sesudah.md`. Semua angka DENGAN skill cocok dengan hitung ulang penguji. Cacat: input kurang dijawab 5 pertanyaan tanpa hitungan bersyarat; kata proses ("skill", "script") dan path sandbox bocor di 3 dari 5 balasan; nama usaha karangan di teks grup. |
| 2026-10-14 | 1.0.10 | Uji ulang singkat OpenClaw 2026.10.2 lokal, hanya sisi DENGAN skill; 3 skenario (S4 input kurang, S3 harian lepas + grup, S2 Natal + PPh 21), pesan sama dengan uji 1.0.9; penguji independen | 5,0 (dari uji 1.0.9, tidak diulang) | 8,0 | +3,0 | **BELUM (tipis)** | S4 7,5 · S3 8,5 · S2 8. Tanpa salah angka. Cacat 1 (input kurang tanpa hitungan) **hilang**: hitung bersyarat + 3 pertanyaan. Cacat 2 (kata proses/path/nama skill lain) **hilang** di 3/3 balasan. Cacat 3 **sebagian**: nama karangan hilang, tetapi `[isi: nama usaha]` tidak muncul di teks grup mana pun ("kami"/"Manajemen"/"toko"/"perusahaan"; cadangan `perusahaan or "kami"` di `thr.py`). Cacat baru: S4 Tini ditulis "12 bln" tanpa label asumsi dan tidak ditanyakan. Rincian di bagian atas `00-openclaw-sebelum-sesudah.md`. |
