# Dasar aturan gaji-umkm — berlaku per 23 September 2026

> Ringkasan untuk alat bantu hitung, bukan nasihat hukum/pajak. **gaji-umkm tidak menetapkan tarif sendiri.** Semua tarif, batas upah, tabel TER, dan rumus berasal dari script skill Komunitech berikut, disalin persis di `scripts/mesin/` (sha256 di `scripts/mesin/SUMBER.json`). Rincian sumber resmi & status verifikasi ada di dokumen skill sumbernya.

| Hitungan | Mesin (skill sumber, versi) | Dasar aturan (dicatat skill sumber, status per 2026-09-23) |
|---|---|---|
| BPJS Kesehatan 4% perusahaan + 1% karyawan; dasar = gaji pokok + tunjangan tetap, min. UMK (bila diisi), maks. Rp 12.000.000 | `payroll.py` (slip-gaji-bpjs 1.0.1) | Perpres 82/2018 jo. Perpres 64/2020 Pasal 30 & 32 |
| JHT 3,7% + 2%; JKK 0,24/0,54/0,89/1,27/1,74% (perusahaan); JKM 0,3% (perusahaan); dasar = gaji pokok + tunjangan tetap | `payroll.py` | PP 44/2015 Pasal 16, 18, 19; PP 46/2015 |
| JP 2% + 1%, batas upah **Rp 10.547.400 (Mar 2025–Feb 2026)** dan **Rp 11.086.300 (Mar 2026–Feb 2027)**; di luar rentang itu script meminta `--batas-jp` | `payroll.py` | PP 45/2015; surat BPJS Ketenagakerjaan B/1226/022026 (25 Feb 2026) |
| Lembur: 1/173 upah sebulan; hari kerja jam ke-1 ×1,5, berikutnya ×2; hari libur sesuai tangga pola 5/6 hari | `payroll.py` | PP 35/2021 Pasal 26, 31, 32 |
| PPh 21 TER bulanan (kategori A/B/C), bruto pajak termasuk premi JKK, JKM, BPJS Kesehatan perusahaan | `payroll.py` + `ter_core.py` + `ter_tabel.json` | PP 58/2023 (tabel TER), PMK 168/2023 |
| Masa Pajak Terakhir (Desember/bulan berhenti): hitung ulang setahun dengan tarif Pasal 17, biaya jabatan 5% maks Rp 500.000 × jumlah bulan kerja, PTKP, PKP dibulatkan ke bawah ribuan | `payroll.py` + `ter_core.py`; dicek ulang dengan `pph21.py` (pph21-ter 1.0.1) | PMK 168/2023 Pasal 8–10; UU 7/2021 HPP (PTKP & Pasal 17) |
| PPh 21 DTP 2026 (sektor tertentu, bruto tetap ≤ Rp 10 jt) | `payroll.py` | PMK 105/2025 |
| THR: ≥12 bulan = 1 bulan upah; 1–<12 bulan = masa kerja/12 × upah; batas bayar H-7 | `thr.py` (hitung-thr 1.0.1) | Permenaker 6/2016; SE Menaker M/3/HK.04.00/III/2026 |

## Pembulatan (standar seluruh library Komunitech)
- Iuran BPJS dan lembur: ke rupiah terdekat per komponen. PPh 21: **ke bawah** ke rupiah penuh; PKP ke bawah ke ribuan.
- **Belum dicocokkan dengan Coretax maupun aplikasi BPJS.** Bila berbeda, ikuti sistem resmi.

## Aturan yang diikuti untuk masuk/keluar tengah bulan
- Bulan masuk dihitung sebagai satu bulan kerja untuk PPh 21 (`bulan_mulai` = bulan tanggal masuk bila di tahun berjalan) — cara `slip-gaji-bpjs`/`pph21-ter`.
- Bulan keluar = Masa Pajak Terakhir (`berhenti=ya`): PPh 21 dihitung ulang setahun; kelebihan potong dikembalikan di slip (kecuali DTP).
- **Prorata gaji tidak diatur di skill sumber**, jadi tidak dihitung otomatis. Nominal yang benar-benar dibayar diisi pemilik sesuai perjanjian kerja (`--gaji-pokok-dibayar`); mesin memakainya sebagai gaji pokok bulan itu (termasuk dasar iuran BPJS & lembur).
- Potongan tidak masuk hanya bila diatur di PK/PP/PKB (PP 36/2021; lihat `absensi-lokal`) dan dipotong sebagai "potongan lain" setelah pajak, sama seperti `slip-gaji-bpjs`.

## Tenggat untuk `pengingat` (dicek 26 September 2026)
| Tenggat | Ketentuan | Status | Sumber |
|---|---|---|---|
| Setor iuran BPJS Kesehatan | Paling lambat **tanggal 10 setiap bulan** (Perpres 82/2018 Pasal 39 ayat (1)). Tidak digeser saat libur (ketentuan pergeseran ayat (2) belum dibaca) | Terverifikasi (teks Perpres di Wikisumber) | [1] |
| Setor iuran BPJS Ketenagakerjaan (JKK, JKM) | Paling lambat **tanggal 15 bulan berikutnya**; bila hari libur → hari kerja berikutnya (PP 44/2015 Pasal 21 ayat (2)–(3)). JHT & JP ditagih bersama; pasal tenggatnya di PP 46/2015 & PP 45/2015 belum dibaca langsung — **PERLU REVIEW** | Terverifikasi resmi (PDF situs BPJS Ketenagakerjaan) | [2] |
| Setor PPh 21 | **Tanggal 15 bulan berikutnya**; libur → hari kerja berikutnya | Dari skill `kalender-pajak` (PMK 81/2024 Ps. 94 & 100; status di sana: Konsisten, PERLU REVIEW naskah resmi) | [3] |
| Lapor SPT Masa PPh 21 | **Tanggal 20 bulan berikutnya**; libur → hari kerja berikutnya | Dari skill `kalender-pajak` (PMK 81/2024 Ps. 171 & 173) | [3] |

`pengingat` hanya menggeser Sabtu/Minggu. Libur nasional & cuti bersama tidak dicek — gunakan skill `kalender-pajak` untuk tanggal pasti.

## Sumber
1. Perpres 82/2018 hlm. 26 (Wikisumber): https://id.wikisource.org/wiki/Halaman:Perpres_Nomor_82_Tahun_2018_tentang_Jaminan_Kesehatan.pdf/26
2. PP 44/2015 (situs resmi BPJS Ketenagakerjaan): https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104557_PP%2044%20Tahun%202015.pdf
3. `skills/kalender-pajak/references/aturan-tenggat.md` (butir 1, 2, 8, 9)
4. Sumber tarif & batas BPJS/lembur: `skills/slip-gaji-bpjs/references/regulasi.md`; PPh 21: `skills/pph21-ter/references/regulasi.md`; THR: `skills/hitung-thr/references/regulasi.md`.

_Untuk kasus khusus (pesangon, gross-up, WNA, sengketa upah) hubungi konsultan pajak, Kring Pajak 1500200, BPJS, atau Disnaker._
