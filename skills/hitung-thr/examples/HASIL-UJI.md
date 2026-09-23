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
