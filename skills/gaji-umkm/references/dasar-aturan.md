# Dasar aturan gaji-umkm — berlaku per 23 September 2026 (diperbarui 26 September 2026, v1.0.2)

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
| Setor iuran BPJS Kesehatan | Paling lambat **tanggal 10 setiap bulan** (Perpres 82/2018 Pasal 39 ayat (1)). Ayat lanjutan Pasal 39 menggeser ke hari kerja berikutnya bila tgl 10 hari libur (dibaca penguji Akun B, hlm. 27); `pengingat` tetap menampilkan tgl 10 (konservatif, lebih awal) | Terverifikasi (teks Perpres di Wikisumber) | [1], [1a] |
| Setor iuran JKK, JKM | Paling lambat **tanggal 15 bulan berikutnya**; bila hari libur → hari kerja berikutnya (PP 44/2015 Pasal 21 ayat (2)–(3)) | Terverifikasi resmi (PDF situs BPJS Ketenagakerjaan) | [2] |
| Setor iuran JHT | Paling lambat **tanggal 15 bulan berikutnya**; bila hari libur → hari kerja berikutnya (PP 46/2015 Pasal 19 ayat (2)–(3)) → `pengingat` menggeser Sabtu/Minggu | Terverifikasi resmi (PDF situs BPJS Ketenagakerjaan, dibaca penguji Akun B 26-09-2026). PERLU REVIEW v1.0.0 **ditutup** | [5] |
| Setor iuran JP | **Setiap bulan paling lambat tanggal 15 bulan berikutnya** (PP 45/2015 Pasal 30 ayat (3)); pasal ini **tidak** memuat pergeseran hari libur → `pengingat` **tidak** menggeser JP. Karena JP ditagih bersama JHT/JKK/JKM, pengingat menyarankan membayar semuanya paling lambat tgl 15 | Terverifikasi resmi (PDF situs BPJS Ketenagakerjaan, dibaca penguji Akun B 26-09-2026). PERLU REVIEW v1.0.0 **ditutup** | [6] |
| Setor PPh 21 | **Tanggal 15 bulan berikutnya**; libur → hari kerja berikutnya | Dari skill `kalender-pajak` (PMK 81/2024 Ps. 94 & 100; status di sana: Konsisten, PERLU REVIEW naskah resmi) | [3] |
| Lapor SPT Masa PPh 21 | **Tanggal 20 bulan berikutnya**; libur → hari kerja berikutnya | Dari skill `kalender-pajak` (PMK 81/2024 Ps. 171 & 173) | [3] |

`pengingat` hanya menggeser Sabtu/Minggu. Libur nasional & cuti bersama tidak dicek — gunakan skill `kalender-pajak` untuk tanggal pasti.

## Setoran PPh 21 bila ada kelebihan potong (v1.0.1, dicek 26 September 2026)
- **Aturan:** PMK 168/2023 Pasal 21 ayat (1): bila PPh 21 yang dipotong pada masa selain Masa Pajak Terakhir lebih besar dari PPh 21 terutang setahun/bagian tahun, kelebihannya **wajib dikembalikan** pemotong kepada pegawai tetap bersama bukti potong, paling lambat akhir bulan berikutnya setelah Masa Pajak Terakhir; ayat (2): kecuali PPh 21 DTP. Ayat (3): kelebihan penyetoran pajak terutang pada suatu masa **dapat diperhitungkan** dengan PPh 21/26 terutang bulan berikutnya lewat SPT Masa. [7]
- **Penerapan DJP:** jumlah PPh 21 di SPT Masa dihitung gabungan semua karyawan; pemberi kerja "berhak mengklaim kompensasi lebih bayar dalam pelaporan SPT Masa PPh Pasal 21, jika secara akumulatif atas semua karyawannya terdapat kelebihan pemotongan" (artikel pegawai DJP di pajak.go.id, 12 Maret 2025). [8]
- **Yang dilakukan script:** "PPh 21 dipotong bulan ini" (jumlah PPh 21 positif) − "Kelebihan dikembalikan ke karyawan" = **"Perkiraan setor PPh 21"** (tidak kurang dari 0). Bila minus → "Lebih bayar" yang dapat diperhitungkan ke bulan berikutnya; **tidak** dikurangkan otomatis dari bulan berikutnya. Selalu disertai saran konfirmasi ke konsultan pajak/Coretax dan catatan pembulatan belum dicocokkan dengan Coretax.
- Status: **Terverifikasi** dari naskah PMK (JDIH Kemenkeu) + artikel DJP. Rincian isian SPT Masa di Coretax tidak diuji.

## Pagar kepatuhan BPJS (v1.0.1)
- UU 24/2011 Pasal 15 ayat (1)–(2): pemberi kerja wajib mendaftarkan dirinya dan pekerjanya ke BPJS serta memberikan data yang lengkap dan benar. PP 86/2013: sanksi administratif (teguran tertulis, denda, tidak mendapat pelayanan publik tertentu). Perpres 82/2018 jo. 64/2020 Pasal 32: dasar iuran BPJS Kesehatan = gaji pokok + tunjangan tetap, batas atas Rp 12.000.000 (batas bawah UMK di mesin slip-gaji-bpjs).
- v1.0.2: gaji pokok/tunjangan tetap "dibayar" (`isi`) yang lebih kecil dari data karyawan pada bulan **penuh** ikut dipagari, karena dasar iuran BPJS (Kesehatan & Ketenagakerjaan) bulan itu ikut turun; bulan masuk/keluar tengah bulan (prorata) tidak dipagari.
- JP tidak dipagari karena kewajiban JP bertahap menurut skala usaha (usaha mikro/kecil belum wajib JP) — tetap tampil di data karyawan.

## Sumber
1. Perpres 82/2018 hlm. 26 (Wikisumber): https://id.wikisource.org/wiki/Halaman:Perpres_Nomor_82_Tahun_2018_tentang_Jaminan_Kesehatan.pdf/26
1a. Perpres 82/2018 hlm. 27 (Wikisumber): https://id.wikisource.org/wiki/Halaman:Perpres_Nomor_82_Tahun_2018_tentang_Jaminan_Kesehatan.pdf/27
2. PP 44/2015 (situs resmi BPJS Ketenagakerjaan): https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104557_PP%2044%20Tahun%202015.pdf
3. `skills/kalender-pajak/references/aturan-tenggat.md` (butir 1, 2, 8, 9)
5. PP 46/2015 (situs resmi BPJS Ketenagakerjaan): https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
6. PP 45/2015 (situs resmi BPJS Ketenagakerjaan): https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2045%20Tahun%202015.pdf
7. PMK 168/2023, naskah resmi JDIH Kemenkeu, Pasal 21 & 22 (hlm. 21–22), diunduh dan dibaca 26 September 2026: https://jdih.kemenkeu.go.id/api/download/e60a82e0-b218-40f5-9d18-b924aa1e11ce/2023pmkeuangan168.pdf
8. "Di Formulir 1721-A1 Lebih Potong? Belum Tentu SPT Anda Lebih Bayar", Dinny Anggraeny (pegawai DJP), pajak.go.id, 12 Maret 2025, dibaca 26 September 2026: https://www.pajak.go.id/en/node/114629
4. Sumber tarif & batas BPJS/lembur: `skills/slip-gaji-bpjs/references/regulasi.md`; PPh 21: `skills/pph21-ter/references/regulasi.md`; THR: `skills/hitung-thr/references/regulasi.md`.

_Untuk kasus khusus (pesangon, gross-up, WNA, sengketa upah) hubungi konsultan pajak, Kring Pajak 1500200, BPJS, atau Disnaker._
