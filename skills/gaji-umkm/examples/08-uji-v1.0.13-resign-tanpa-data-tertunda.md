# 08 — Uji v1.0.13: karyawan resign tanpa data Januari–Agustus tidak menahan yang lain (skenario gelombang 21)

> Uji **pembuat** (bukan penguji independen), 17-10-2026, skill gaji-umkm **1.0.13** (sudah memuat perbaikan temuan
> pemeriksa independen 17-10-2026, termasuk putaran 3). Semua keluaran di bawah adalah hasil nyata `scripts/gaji.py` versi ini (disalin apa
> adanya). Data **fiktif**, sama dengan pesan uji bot Telegram gelombang 21 (16-10-2026, skor dengan skill v1.0.12: 4
> karena seluruh hitungan ditahan menunggu data Lina). Belum diuji ulang di bot.

## Permintaan pemilik (sama dengan gelombang 21)
"Mulai pakai aplikasi gaji. Daftar 12 karyawan saya ada di data/karyawan.csv. UMK kota kami Rp 5.396.761, JKK 0,54%,
gajian tgl 25. Gaji September 2026 fiktif: Andi bonus 500 ribu & kasbon 250 ribu, Indah lembur 2 jam dan 3 jam di hari
kerja, Kiki masuk 15 September, Lina resign 14 September. Tolong hitung slip dan rekap setoran BPJS/PPh21-nya."

`data/karyawan.csv` (fiktif; tanpa data Januari–Agustus, tanpa nominal prorata):
```
kode;nama;jabatan;jenis;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;bpjs;jkk;hari_kerja;masuk;nik;bank;rekening;atas_nama;kode_absensi
K01;Andi Fiktif;Kepala Gudang;tetap;K/1;6.500.000;750.000;400.000;kes,tk,jp;0,54;6;2019-03-01;;BCA;0000000001;Andi Fiktif;A01
K02;Budi Fiktif;Sopir;tetap;K/2;5.400.000;300.000;500.000;kes,tk,jp;0,54;6;2020-06-15;;BRI;0000000002;Budi Fiktif;A02
K03;Citra Fiktif;Kasir;tetap;TK/0;5.400.000;;300.000;kes,tk,jp;0,54;6;2021-01-10;;BCA;0000000003;Citra Fiktif;A03
K04;Dewi Fiktif;Admin;tetap;TK/0;5.600.000;250.000;;kes,tk,jp;0,54;6;2021-09-01;;Mandiri;0000000004;Dewi Fiktif;A04
K05;Eko Fiktif;Staf Gudang;kontrak;K/0;5.400.000;;350.000;kes,tk;0,54;6;2024-02-01;;BRI;0000000005;Eko Fiktif;A05
K06;Fajar Fiktif;Staf Gudang;kontrak;TK/0;5.400.000;;350.000;kes,tk;0,54;6;2024-02-01;;BRI;0000000006;Fajar Fiktif;A06
K07;Gita Fiktif;Marketing;tetap;TK/0;6.000.000;500.000;;kes,tk,jp;0,54;6;2022-04-18;;BCA;0000000007;Gita Fiktif;A07
K08;Hadi Fiktif;Teknisi;tetap;K/3;7.000.000;600.000;;kes,tk,jp;0,54;6;2018-11-05;;Mandiri;0000000008;Hadi Fiktif;A08
K09;Indah Fiktif;Staf Produksi;tetap;TK/0;5.400.000;;300.000;kes,tk,jp;0,54;6;2023-03-13;;BCA;0000000009;Indah Fiktif;A09
K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;kes,tk;0,54;6;2025-01-06;;BRI;0000000010;Joko Fiktif;A10
K11;Kiki Fiktif;Staf Produksi;kontrak;TK/0;5.400.000;;;kes,tk;0,54;6;2026-09-15;;BCA;0000000011;Kiki Fiktif;A11
K12;Lina Fiktif;Supervisor;tetap;K/0;10.000.000;1.000.000;;kes,tk,jp;0,54;6;2017-08-01;;Mandiri;0000000012;Lina Fiktif;A12
```

## Langkah agent (SKILL.md Langkah A.0): satu perintah, tanpa database, ±0,2 detik
```bash
python3 <folder-skill>/scripts/gaji.py hitung-cepat --data data/karyawan.csv --bulan 2026-09 \
  --umk 5.396.761 --jkk 0,54 --isi "Andi: bonus=500rb; kasbon=250rb" --isi "Indah: lembur-hari-kerja=2+3" \
  --masuk "Kiki=2026-09-15" --keluar "Lina=2026-09-14" --json
```
JSON penting: `mode: "pratinjau"`, `disimpan: false`, `bisa_final: false`, 11 karyawan di `karyawan`,
`tertunda: [K12 Lina]` dengan `langkah_agent` = `saldo-awal --karyawan K12 --tahun 2026 --sampai-bulan 8 --bruto <1>
--pph21 <2> --iuran <3>` → `hitung --bulan 2026-09`, atau pilihan (b) `hitung --bulan 2026-09 --pph-sementara`.

### `teks` (siap tempel ke pemilik — tanpa nama perintah, jalur file, atau istilah teknis; 3234 karakter)
```
REKAP GAJI SEPTEMBER 2026 - (nama usaha)
Status: PRATINJAU (hitung cepat, belum disimpan) | 11 karyawan dihitung, 1 tertunda

| Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |
|---|---|---:|---:|---:|---:|---:|
| K01 | Andi Fiktif | 8.150.000 | 625.009 | 85.009 | 7.524.991 | 8.914.150 |
| K02 | Budi Fiktif | 6.200.000 | 244.189 | 16.189 | 5.955.811 | 6.800.780 |
| K03 | Citra Fiktif | 5.700.000 | 260.710 | 44.710 | 5.439.290 | 6.269.160 |
| K04 | Dewi Fiktif | 5.850.000 | 279.998 | 45.998 | 5.570.002 | 6.466.590 |
| K05 | Eko Fiktif | 5.750.000 | 207.085 | 45.085 | 5.542.915 | 6.211.160 |
| K06 | Fajar Fiktif | 5.750.000 | 207.085 | 45.085 | 5.542.915 | 6.211.160 |
| K07 | Gita Fiktif | 6.500.000 | 345.182 | 85.182 | 6.154.818 | 7.185.100 |
| K08 | Hadi Fiktif | 7.600.000 | 383.678 | 79.678 | 7.216.322 | 8.401.040 |
| K09 | Indah Fiktif | 5.980.925 | 262.817 | 46.817 | 5.718.108 | 6.550.085 |
| K10 | Joko Fiktif | 5.700.000 | 162.000 | 0 | 5.538.000 | 6.161.160 |
| K11 | Kiki Fiktif (baru) | 5.400.000 | 190.306 | 28.306 | 5.209.694 | 5.861.160 |
| | **Total** | **68.580.925** | **3.168.059** | **522.059** | **65.412.866** | **75.031.545** |
(angka tabel dalam rupiah)

Yang harus dibayar/disetor (BELUM termasuk yang tertunda: Lina Fiktif):
- Transfer gaji bersih ke karyawan: Rp 65.412.866
- Setor BPJS Kesehatan (4% perusahaan + 1% karyawan): Rp 3.265.000
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 5.581.620
- Setor PPh 21: Rp 522.059
- Total biaya gaji perusahaan: Rp 75.031.545

TERTUNDA - belum dihitung, menunggu data:
- Lina Fiktif (K12, keluar 14/09/2026): September 2026 adalah Masa Pajak Terakhir: PPh 21-nya dihitung ulang setahun. Butuh total Januari–Agustus 2026: (1) penghasilan bruto (angka di bukti potong bulanan, termasuk iuran JKK, JKM & BPJS Kesehatan bagian perusahaan), (2) PPh 21 yang sudah dipotong, (3) iuran JHT 2% + JP 1% yang dipotong dari gajinya. Pilihan: (a) kirim angka itu, lalu dihitung ulang setahun (final); atau (b) hitung bulan ini saja dengan tarif bulanan (TER) sebagai angka SEMENTARA - wajib dilengkapi sebelum bukti potong 1721-A1 dibuat. Gaji terakhir Lina Fiktif penuh atau prorata 14/30 hari kalender (gaji pokok Rp 10.000.000 × 14 ÷ 30 hari = Rp 4.666.667; tunjangan tetap Rp 1.000.000 × 14 ÷ 30 = Rp 466.667)?

Perlu diperhatikan:
- Masuk/keluar tengah bulan, gaji dihitung PENUH (asumsi; ikut perjanjian kerja). Bila prorata hari kalender: Kiki Fiktif (masuk 15/09/2026): gaji pokok Rp 5.400.000 × 16 ÷ 30 hari = Rp 2.880.000. Mohon pastikan mana yang dipakai.

_Alat bantu hitung, bukan nasihat hukum/pajak. Angka dari mesin hitung gaji, PPh 21 dan THR Komunitech. Dasar: Perpres 64/2020; PP 44, 45, 46/2015 & PP 6/2025 (BPJS); PP 35/2021 (lembur); PP 58/2023 & PMK 168/2023 (PPh 21); PMK 105/2025 (DTP); Permenaker 6/2016 (THR); berlaku per 23 September 2026. Pembulatan: iuran BPJS & lembur ke rupiah terdekat, PPh 21 ke bawah; belum dicocokkan dengan Coretax/aplikasi BPJS - bila berbeda, ikuti sistem resmi. Kasus khusus: konsultan pajak, Kring Pajak 1500200, BPJS, atau Disnaker._

Belum disimpan. Bila sudah benar (atau setelah dikoreksi), balas "simpan" agar data karyawan & gaji bulan ini tersimpan di komputer ini.
```

## Pilihan (b): `--pph-sementara` (bulan berjalan saja, TER, berlabel SEMENTARA)
```
| K12 | Lina Fiktif (keluar) | 11.000.000 | 843.634 | 403.634 (sementara) | 10.156.366 | 12.159.400 |
| | **Total** | **79.580.925** | **4.011.693** | **925.693** | **75.569.232** | **87.190.945** |
(sementara) PPh 21 Lina Fiktif dihitung untuk bulan ini saja dengan tarif efektif bulanan (TER) karena data Januari–Agustus 2026 belum ada. Perhitungan setahun (Masa Pajak Terakhir) BELUM FINAL - wajib dilengkapi sebelum bukti potong 1721-A1 (BPA1) dibuat; PPh 21 dan gaji bersihnya bisa berubah.

Yang harus dibayar/disetor:
- Transfer gaji bersih ke karyawan: Rp 75.569.232
- Setor BPJS Kesehatan (4% perusahaan + 1% karyawan): Rp 3.815.000
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 6.631.020
- Setor PPh 21: Rp 925.693
  Setoran PPh 21 ini memakai angka SEMENTARA untuk Lina Fiktif (Rp 403.634); angka finalnya bisa berubah setelah data lengkap.
- Total biaya gaji perusahaan: Rp 87.190.945
```
Slip Lina diberi kepala "PPh 21 SEMENTARA - perhitungan setahun (Masa Pajak Terakhir) belum final" dan catatan wajib
dilengkapi sebelum bukti potong 1721-A1 (BPA1). Periode tidak bisa dikunci selama angka sementara masih ada.

## Pilihan (a): pemilik mengirim data Januari–Agustus Lina (fiktif)
`--saldo-awal "Lina: bruto=92.259.200; pph21=3.229.072; iuran=2.630.948"` (di database: perintah `saldo-awal`).
Data fiktif konsisten dengan 8 bulan gaji penuh: bruto pajak 11.532.400/bulan; PPh 21 TER A 3,5% = 403.634/bulan;
iuran JHT 2% 8 × 220.000 + JP 1% dengan batas upah JP 10.547.400 (Januari–Februari 2026: 2 × 105.474) dan 11.086.300
(Maret–Agustus: 6 × 110.000) = 2.630.948.
```
| K12 | Lina Fiktif (keluar) | 12.337.572 | 440.000 | -1.337.572 * | 11.897.572 | 12.159.400 |
| | **Total** | **80.918.497** | **3.608.059** | **-815.513** | **77.310.438** | **87.190.945** |
* PPh 21 dihitung ulang setahun (Masa Pajak Terakhir: Desember/bulan keluar).

Yang harus dibayar/disetor:
- Transfer gaji bersih ke karyawan: Rp 77.310.438
- Setor BPJS Kesehatan (4% perusahaan + 1% karyawan): Rp 3.815.000
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 6.631.020
- PPh 21 dipotong bulan ini: Rp 522.059
- Kelebihan PPh 21 dikembalikan ke karyawan (Lina Fiktif, sudah di gaji bersih): Rp 1.337.572
- Perkiraan setor PPh 21: Rp 0 (dipotong - dikembalikan; SPT Masa digabung semua karyawan, PMK 168/2023 Pasal 21)
- Lebih bayar PPh 21 Rp 815.513: tidak disetor; bisa diperhitungkan ke PPh 21 bulan berikutnya lewat SPT Masa (Pasal 21 ayat (3)), tidak otomatis.
  Kelebihan dikembalikan ke karyawan paling lambat akhir bulan berikutnya. Konfirmasi angka setor ke konsultan pajak/Coretax sebelum membayar.
- Total biaya gaji perusahaan: Rp 87.190.945
```

## Pagar BPJS juga berlaku di hitung cepat
`--isi "Andi: gaji-pokok-dibayar=3jt; bonus=4jt"` (Andi bekerja sebulan penuh) tanpa persetujuan khusus pemilik → Andi
**tidak dihitung**, 10 karyawan lain tetap dihitung, JSON `masalah_kepatuhan: ["K01:dasar_bpjs_turun_bulan_penuh"]`:
```
- Andi Fiktif (K01): belum dihitung, perlu persetujuan khusus pemilik: gaji pokok + tunjangan tetap diisi Rp 3.750.000, di bawah data karyawan Rp 7.250.000 padahal bekerja sebulan penuh, jadi dasar iuran BPJS ikut turun. Wajib BPJS dengan upah sebenarnya (UU 24/2011 Pasal 15); boleh hanya dengan alasan sah yang disetujui pemilik (mis. iuran lewat sistem lain, cuti di luar tanggungan sesuai perjanjian kerja), bila tidak perbaiki datanya.
```
Dengan `--ya-saya-paham --alasan-khusus "..."` (hanya atas keputusan pemilik) Andi dihitung; keterangan persetujuan
menempel di kalimat yang sama (satu kalimat, bukan dua) dan jujur "belum disimpan":
```
- Andi Fiktif: gaji pokok + tunjangan tetap diisi Rp 3.750.000, di bawah data karyawan Rp 7.250.000 padahal bekerja sebulan penuh, jadi dasar iuran BPJS Kesehatan & Ketenagakerjaan ikut turun. (Dipakai atas persetujuan khusus pemilik; belum disimpan, dicatat saat disimpan. Alasan: cuti di luar tanggungan 12 hari sesuai perjanjian kerja pasal 7, disetujui pemilik.)
```
Bila ada dua karyawan atau lebih yang perlu persetujuan khusus, kalimat dasar hukumnya (UU 24/2011 Pasal 15) cukup
sekali. Bila karyawan yang dipagari juga di Masa Pajak Terakhir (Desember/keluar) tanpa data, kebutuhan datanya disebut
di baris yang sama ("Selain itu, data Masa Pajak Terakhir-nya juga belum ada …") supaya pemilik tidak ditanya dua kali.

## Alur database (setelah pemilik setuju menyimpan) — angka identik
```
init --ya → atur --umk 5.396.761 --jkk 0,54 --tanggal-gajian 25 → karyawan impor --ya → karyawan keluar Lina 2026-09-14 --ya
→ isi Andi --bonus 500rb --kasbon 250rb → isi Indah --lembur-hari-kerja 2+3 → hitung --bulan 2026-09
DB hitung: 11 dihitung; tertunda ['K12'] ; bisa_final False ; setor Kes 3265000 TK 5581620 PPh 522059 THP 65412866
final --ya → GAGAL: September 2026 belum bisa dikunci (final) karena: Lina Fiktif (tertunda: data Januari s.d. bulan lalu
             untuk Masa Pajak Terakhir belum lengkap). Lengkapi/perbaiki datanya, hitung ulang tanpa angka sementara, lalu
             kunci. Angka karyawan lain tetap bisa diperiksa di rekap draf.
slip --bulan 2026-09 → Slip September 2026 DRAF (11 file)
saldo-awal Lina (bruto 92.259.200; PPh 3.229.072; iuran 2.630.948) → hitung → 12 dihitung; tertunda [] ; bisa_final True ;
             Kes 3815000 TK 6631020 dipotong 522059 kembali 1337572 setor 0 lebih bayar 815513 THP 77310438
final --ya → TERSIMPAN. Kunci periode September 2026.
```
Bulan yang **terlewat** setelah aplikasi dipakai (mis. saldo awal s.d. Agustus, September–Oktober final, November belum
dihitung, lalu Desember dihitung) tidak dimintai jumlah manual: teks menyebut "Gaji November 2026 belum dihitung &
dikunci di aplikasi ini: hitung dan kunci dulu bulan itu" dan `langkah_agent` = `hitung --bulan 2026-11` → `final
--bulan 2026-11` → `hitung --bulan 2026-12` (tes `test_bulan_terlewat_disarankan_hitung_dan_kunci`). Bulan tepat
setelah saldo awal yang tidak dihitung (saldo s.d. Agustus, aplikasi mulai Oktober, September kosong) diberi dua
pilihan: "hitung dan kunci dulu bulan itu (bila gajinya dibayar di luar aplikasi, kirim totalnya Januari–September 2026
sebagai saldo awal)"; `langkah_agent` memuat `hitung`/`final --bulan 2026-09` dan alternatif `saldo-awal --sampai-bulan 9`
(tes `test_bulan_terlewat_setelah_saldo_awal`).

## Verifikasi independen (Python Decimal, tanpa mesin hitung)
| Angka | Hitung ulang | Script | Cocok |
|---|---|---|---|
| Lembur Indah: 5.400.000 ÷ 173 × 9 jam setara (2 jam = 1,5 + 2 = 3,5; 3 jam = 1,5 + 2 + 2 = 5,5) | Rp 280.925 | Rp 280.925 | ✅ |
| Setor BPJS Kesehatan 11 orang: Σ (4% + 1%) × min(max(upah, UMK), 12 jt), dibulatkan per komponen | Rp 3.265.000 | Rp 3.265.000 | ✅ |
| Setor BPJS Ketenagakerjaan 11 orang: JHT 3,7% + 2%, JKK 0,54%, JKM 0,3%, JP 2% + 1% (yang ikut JP; batas 11.086.300) | Rp 5.581.620 | Rp 5.581.620 | ✅ |
| Acuan penilai G21 (12 orang, sebulan penuh): Kes 3.815.000, TK 6.631.020; dikurangi Lina (Kes 550.000; TK 1.049.400) | 3.265.000 / 5.581.620 | sama | ✅ |
| PPh 21 TER (braket PP 58/2023): Andi B 8.500.900 × 1% = 85.009; Budi B 6.475.880 × 0,25% = 16.189; Citra A 5.961.360 × 0,75% = 44.710; Hadi C 7.967.840 × 1% = 79.678; Joko B 5.961.360 × 0% = 0; Kiki A 5.661.360 × 0,5% = 28.306 | sama | sama | ✅ |
| Setor PPh 21 11 orang (Σ per karyawan) | Rp 522.059 | Rp 522.059 | ✅ |
| Lina (b) TER A: bruto 11.532.400 × 3,5% | Rp 403.634 | 403.634 (sementara) | ✅ |
| Lina (a) Masa Pajak Terakhir: bruto Jan–Sep 92.259.200 + 11.532.400 = 103.791.600 − biaya jabatan 4.500.000 (5% = 5.189.580, maks. 500.000 × 9) − iuran 2.630.948 + 330.000 = 2.960.948 − PTKP K/0 58.500.000 = 37.830.652 → PKP **dibulatkan ke bawah ke ribuan** 37.830.000 → 5% = 1.891.500 − sudah dipotong 3.229.072 | −Rp 1.337.572 (dikembalikan) | −1.337.572 | ✅ |
| Setor PPh 21 setelah (a): dipotong 522.059 − dikembalikan 1.337.572 → setor 0, lebih bayar 815.513; transfer 65.412.866 + Lina 11.897.572 | 77.310.438 | Rp 77.310.438 | ✅ |
| Prorata hari kalender (bila dipilih): Kiki 5.400.000 × 16 ÷ 30; Lina 10.000.000 × 14 ÷ 30 dan 1.000.000 × 14 ÷ 30 | 2.880.000; 4.666.667; 466.667 | sama | ✅ |

Tes otomatis (`tests/uji_regresi.py`, kelas `UjiV1013` & `UjiV1013Pemeriksa`) juga mencocokkan setiap karyawan dengan
`payroll.py` **asli** skill slip-gaji-bpjs yang dijalankan langsung dengan baris yang disusun tes sendiri.

## Panjang `teks` (target ≤ 3.800 karakter, batas pesan Telegram 4.096)
Diukur dengan argumen yang sama persis dengan tes `test_panjang_teks_semua_varian_satu_pesan` (12 karyawan G21 fiktif;
"CSV minimal" = hanya kolom `nama;ptkp;gaji_pokok` + `--isi` Andi/Indah, `--masuk` Kiki, `--keluar` Lina, UMK 5.396.761).
Sebelum = 1.0.13 putaran 2 (diukur pemeriksa ulang), sesudah = putaran 3.

| Varian | Sebelum | Sesudah |
|---|---:|---:|
| CSV minimal, JKK 0,40 | 4.033 | 3.702 |
| CSV minimal + saldo awal Lina | 4.109 | 3.692 |
| CSV minimal + prorata kalender | 4.202 | 3.606 |
| CSV minimal + saldo + prorata | 4.432 | 3.696 |
| CSV minimal + PPh sementara | 3.812 | 3.528 |
| CSV minimal + PPh sementara + prorata | 4.124 | 3.521 |
| CSV minimal, JKK 0,54 + saldo + prorata | 4.123 | 3.480 |
| CSV minimal tanpa JKK + saldo + prorata | 4.245 | 3.602 |
| G21 (file lengkap) | 3.338 | 3.234 |
| G21 + saldo awal Lina | 3.410 | 3.220 |
| G21 + prorata | 3.454 | 3.085 |
| G21 + saldo + prorata | 3.737 | 3.228 |
| G21 + PPh sementara | 3.118 | 3.061 |
| G21 + PPh sementara + prorata | 3.429 | 3.053 |
| G21 tanpa JKK umum (tarif per baris 0,54) | 3.495 | 3.273 |
| G21 tanpa JKK umum + saldo + prorata | 3.894 | 3.267 |
| G21 JKK 0,40 per baris | 3.804 | 3.488 |
| G21 dua karyawan tanpa BPJS (pagar) | 4.067 | 3.659 |
| Pagar Andi (tanpa persetujuan) | 3.715 | 3.611 |
| Pagar + saldo + prorata | 4.209 | 3.700 |
| Persetujuan khusus + alasan panjang | 4.174 | 3.601 |
| Persetujuan khusus (alasan "uji") | 4.095 | 3.522 |
| Persetujuan + prorata | 3.982 | 3.373 |
| Persetujuan + saldo + prorata | 4.344 | 3.595 |
| Persetujuan + PPh sementara + prorata | 4.041 | 3.420 |
| **Maksimum 25 varian** | **4.432** | **3.702** |
| Alur database ala examples/01 (tanpa / dengan saldo awal) | — | 3.278 / 3.108 |
| G21 Desember tanpa data (isi `error`) | — | 970 |

25 varian di atas **bukan** semua kasus. Pemeriksa ulang (putaran 3) mengukur 75 varian `hitung-cepat`; dengan versi ini:
**47 muat satu pesan** (maks. 3.781), **23 dibagi 2–3 pesan** lewat `teks_bagian` (tiap bagian 1.009–3.759; dipotong di
batas bagian/baris, judul tabel diulang, judul rekap tidak sendirian, pesan terakhir tidak hanya kalimat penutup), dan 5
galat semua-tertunda (isi `error` ≤ 1.480). Yang dibagi antara lain: **CSV minimal (jalur Langkah A.0) + pagar BPJS**
(4.079 → 2.947 + 1.130), CSV minimal + persetujuan khusus ± saldo/prorata/sementara (3.888–4.181), file lengkap + alasan
persetujuan sangat panjang + saldo + prorata (3.899), dua karyawan tanpa BPJS + pagar + saldo + prorata (3.918–4.085),
CSV minimal + 3 masuk/2 keluar (4.011), CSV minimal dengan UMK Rp 7.000.000 (3.983–4.073), 20 karyawan (3.999 / 4.295),
45–50 karyawan (5.700–7.562). Tes `test_teks_panjang_dibagi_aman`, `test_pemotong_judul_dan_penutup_tidak_sendirian`.

## Cara agent membalas di chat
Agent **menempel `teks` di atas apa adanya** sebagai satu pesan (3.234 karakter, muat satu pesan Telegram) — tidak
diringkas, tidak ditulis ulang. Semua yang perlu ditanyakan sudah ada di dalamnya: pilihan (a)/(b) dan data
Januari–Agustus Lina, pertanyaan "penuh atau prorata" untuk Lina & Kiki, dan penutup "balas 'simpan'". Tidak ada daftar
pertanyaan tambahan dan ajakan "simpan" tidak diulang.

Bila JSON memuat `teks_bagian` (teks > 3.800 karakter, mis. CSV minimal + pagar BPJS: 4.079 karakter → 2.947 + 1.130),
tiap bagian dikirim berurutan sebagai pesan terpisah, juga apa adanya. Pesan tambahan hanya untuk hal yang belum ada di
`teks` (mis. pemilik menanyakan hal lain), singkat dan terpisah.

## Hasil
- Satu karyawan dengan data kurang tidak lagi menahan 11 karyawan lain: slip & rekap setoran langsung keluar di balasan
  pertama (11 dihitung, 1 tertunda), dan data yang dibutuhkan + pilihan (a)/(b) disebut dalam satu pesan.
- `final` tetap menolak sampai data Lina lengkap (periode pajak tidak dikunci dengan angka yang belum final).
- `python3 tests/uji_regresi.py` → 69 tes OK (termasuk 8 tes putaran 3 dan 3 tes putaran 4). `python3 scripts/validate.py` → valid.
- **Catatan jujur:** uji pembuat, bukan penguji independen; belum diuji ulang di bot Telegram asli. Praktik penagihan
  iuran BPJS untuk bulan masuk/keluar bila gaji diprorata belum diverifikasi ke BPJS (PERLU REVIEW).
