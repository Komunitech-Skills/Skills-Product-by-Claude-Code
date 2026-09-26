# 01 — Normal: gaji September 2026, 12 karyawan (penguji independen Akun B)

> Uji oleh penguji **independen** (Akun B), 26-09-2026, skill disalin ke scratchpad, database baru. Semua nama FIKTIF.
> Status uji: `claude-code (simulasi agent)` — perintah dijalankan langsung sesuai SKILL.md, bukan di platform pembeli.

## Permintaan pemilik
"Mulai pakai aplikasi gaji. Ini daftar 12 karyawan saya (CSV). UMK kota kami Rp 5.396.761, JKK 0,54%, gajian tgl 25.
Gaji September: Andi bonus 500 ribu & kasbon 250 ribu, Indah lembur 2 jam dan 3 jam di hari kerja.
Kiki baru masuk 15 September (dibayar prorata Rp 4.266.667), Lina resign 14 September (dibayar Rp 4.666.667)."

## Data uji (mencakup kategori TER A/B/C, batas BPJS Kes & JP, BPJS sebagian/tidak, JKK per orang, masuk/keluar tengah bulan)
| Kode | PTKP | Gaji pokok + tunj. tetap | BPJS | Catatan |
|---|---|---|---|---|
| K01 Andi | K/1 (B) | 6.000.000 + 750.000 (+400.000 tidak tetap) | kes,tk,jp | bonus, kasbon, NIK & rekening BCA |
| K02 Budi | TK/0 (A) | 4.000.000 | kes,tk,jp | di bawah UMK → dasar BPJS Kes = UMK |
| K03 Citra | K/3 (C) | 12.000.000 + 1.000.000 | kes,tk,jp | batas BPJS Kes 12 jt & JP 11.086.300 |
| K04 Dedi | TK/2 (B) | 9.000.000 + 500.000 | kes,tk,jp | |
| K05 Eka | K/0 (A) | 15.000.000 | kes,tk,jp | |
| K06 Fajar | K/2 (B) | 5.500.000 | kes,tk | JKK 0,89% |
| K07 Gita | TK/1 (A) | 7.000.000 + 300.000 | kes | |
| K08 Hadi | TK/3 (B) | 20.000.000 + 2.000.000 | kes,tk,jp | |
| K09 Indah | K/1 (B) | 5.400.000 | kes,tk,jp | lembur 2+3 jam |
| K10 Joko | K/2 (B) | 3.800.000 | tidak | kontrak |
| K11 Kiki | TK/0 (A) | 8.000.000 | kes,tk,jp | masuk 15/09, prorata diisi |
| K12 Lina | K/0 (A) | 10.000.000 | kes,tk,jp | keluar 14/09 → Masa Pajak Terakhir |

## Jalannya (perintah nyata)
1. `init` → pratinjau → `--ya`; `atur --umk 5.396.761 --jkk 0,54 --tanggal-gajian 25`.
2. `karyawan impor kary.csv` → pratinjau menampilkan NIK `************0001`, rekening `BCA ******7890` → `--ya`.
3. `isi` untuk bonus/kasbon/lembur/gaji-pokok-dibayar.
4. `hitung --bulan 2026-09` → **DITOLAK** dengan benar: Lina keluar September = Masa Pajak Terakhir, data Jan–Agu belum ada (daftar 8 bulan disebut) + saran `saldo-awal`.
5. `saldo-awal --karyawan K12 --tahun 2026 --sampai-bulan 8 --bruto 83.872.000 --pph21 2.096.800 --iuran 2.400.000` (angka dihitung penguji).
6. `hitung` ulang → hasil di bawah.

## Keluaran script (dipotong, apa adanya)
```
REKAP GAJI SEPTEMBER 2026 - CV Uji Fiktif Makmur
Status: DRAF (belum final) | 12 karyawan

| Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |
|---|---|---:|---:|---:|---:|---:|
| K01 | Andi Fiktif | Rp 7.650.000 | Rp 599.767 | Rp 79.767 | Rp 7.050.233 | Rp 8.361.450 |
| K02 | Budi Fiktif | Rp 4.000.000 | Rp 173.968 | Rp 0 | Rp 3.826.032 | Rp 4.477.470 |
| K03 | Citra Fiktif | Rp 13.000.000 | Rp 1.034.431 | Rp 543.568 | Rp 11.965.569 | Rp 14.291.926 |
| K04 | Dedi Fiktif | Rp 9.500.000 | Rp 529.397 | Rp 149.397 | Rp 8.970.603 | Rp 10.501.300 |
| K05 | Eka Fiktif | Rp 15.000.000 | Rp 1.623.283 | Rp 1.092.420 | Rp 13.376.717 | Rp 16.382.726 |
| K06 | Fajar Fiktif | Rp 5.500.000 | Rp 165.000 | Rp 0 | Rp 5.335.000 | Rp 5.988.950 |
| K07 | Gita Fiktif | Rp 7.300.000 | Rp 186.880 | Rp 113.880 | Rp 7.113.120 | Rp 7.592.000 |
| K08 | Hadi Fiktif | Rp 22.000.000 | Rp 2.710.695 | Rp 2.039.832 | Rp 19.289.305 | Rp 23.700.526 |
| K09 | Indah Fiktif | Rp 5.680.925 | Rp 216.000 | Rp 0 | Rp 5.464.925 | Rp 6.250.085 |
| K10 | Joko Fiktif | Rp 3.800.000 | Rp 0 | Rp 0 | Rp 3.800.000 | Rp 3.800.000 |
| K11 | Kiki Fiktif (baru) | Rp 4.266.667 | Rp 181.968 | Rp 0 | Rp 4.084.699 | Rp 4.761.577 |
| K12 | Lina Fiktif (keluar) | Rp 5.597.767 | Rp 193.968 | -Rp 931.100 * | Rp 5.403.799 | Rp 5.187.737 |
| | **Total** | **Rp 103.295.359** | **Rp 7.615.357** | **Rp 3.087.764** | **Rp 95.680.002** | **Rp 111.295.747** |
* PPh 21 dihitung ulang setahun (Masa Pajak Terakhir: Desember/bulan keluar).

Yang harus dibayar/disetor:
- Transfer gaji bersih ke karyawan: Rp 95.680.002
- Setor BPJS Kesehatan (4% perusahaan + 1% karyawan): Rp 4.332.014
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 7.945.967
- Setor PPh 21: Rp 4.018.864
- Kelebihan PPh 21 dikembalikan ke karyawan (sudah di gaji bersih): Rp 931.100
- Total biaya gaji perusahaan: Rp 111.295.747

Perlu diperhatikan:
- Budi Fiktif: gaji pokok + tunjangan tetap Rp 4.000.000 di bawah UMK yang Anda isi (Rp 5.396.761). Pastikan tidak melanggar ketentuan upah minimum (usaha mikro/kecil punya aturan tersendiri).
- Kiki Fiktif: gaji pokok + tunjangan tetap Rp 4.266.667 di bawah UMK yang Anda isi (Rp 5.396.761). Pastikan tidak melanggar ketentuan upah minimum (usaha mikro/kecil punya aturan tersendiri).
- Lina Fiktif: gaji pokok + tunjangan tetap Rp 4.666.667 di bawah UMK yang Anda isi (Rp 5.396.761). Pastikan tidak melanggar ketentuan upah minimum (usaha mikro/kecil punya aturan tersendiri).
- Lina Fiktif: PPh 21 lebih potong Rp 931.100 dikembalikan ke karyawan di slip ini.
- Joko Fiktif: gaji pokok + tunjangan tetap Rp 3.800.000 di bawah UMK yang Anda isi (Rp 5.396.761). Pastikan tidak melanggar ketentuan upah minimum (usaha mikro/kecil punya aturan tersendiri).


Langkah berikut: periksa angka ini bersama pemilik. Slip draf: gaji.py slip --bulan 2026-09. Bila sudah benar: gaji.py final --bulan 2026-09 (pratinjau, lalu --ya).
```
(disclaimer lengkap tercetak di akhir: dasar aturan, berlaku per 23 September 2026, pembulatan belum dicocokkan dengan Coretax, rujukan konsultan pajak/Kring Pajak/BPJS/Disnaker.)

## Verifikasi angka independen (Decimal, tanpa membaca kode gaji-umkm)
Penguji menulis kalkulator sendiri dari aturan (Perpres 82/2018 jo. 64/2020: Kes 4%+1%, dasar min UMK maks 12 jt; PP 44/2015 JKK/JKM; PP 46/2015 JHT 3,7%+2%; PP 45/2015 JP 2%+1% batas **Rp 11.086.300 mulai Maret 2026** — dikonfirmasi web: surat BPJS TK B/1226/022026 & akun resmi @BPJSTKinfo; PP 35/2021 lembur 1/173; PP 58/2023 tabel TER A/B/C diketik ulang; PMK 168/2023 bruto = penghasilan + JKK + JKM + BPJS Kes perusahaan; Pasal 17 UU HPP; PKP dibulatkan ke bawah ribuan; PPh ke bawah).

| Kode | Bruto pajak | TER | PPh 21 penguji | PPh 21 app | Gaji bersih penguji | app | Hasil |
|---|---:|---|---:|---:|---:|---:|---|
| K01 | 7.976.700 | B 1% | 79.767 | 79.767 | 7.050.233 | 7.050.233 | cocok |
| K02 | 4.249.470 | A 0% | 0 | 0 | 3.826.032 | 3.826.032 | cocok |
| K03 | 13.589.200 | C 4% | 543.568 | 543.568 | 11.965.569 | 11.965.569 | cocok |
| K04 | 9.959.800 | B 1,5% | 149.397 | 149.397 | 8.970.603 | 8.970.603 | cocok |
| K05 | 15.606.000 | A 7% | 1.092.420 | 1.092.420 | 13.376.717 | 13.376.717 | cocok |
| K06 | 5.785.450 | B 0% | 0 | 0 | 5.335.000 | 5.335.000 | cocok |
| K07 | 7.592.000 | A 1,5% | 113.880 | 113.880 | 7.113.120 | 7.113.120 | cocok |
| K08 | 22.664.800 | B 9% | 2.039.832 | 2.039.832 | 19.289.305 | 19.289.305 | cocok |
| K09 | 5.942.285 (lembur 280.925) | B 0% | 0 | 0 | 5.464.925 | 5.464.925 | cocok |
| K10 | 3.800.000 | B 0% | 0 | 0 | 3.800.000 | 3.800.000 | cocok |
| K11 | 4.518.377 | A 0% | 0 | 0 | 4.084.699 | 4.084.699 | cocok |
| K12 | setahun 88.793.737; BJ 4.439.686; iuran 2.540.000; PKP 23.314.000; PPh setahun 1.165.700 | Pasal 17 | −931.100 | −931.100 | 5.403.799 | 5.403.799 | cocok |

Semua 8 komponen iuran per karyawan (Kes p/k, JHT p/k, JKK, JKM, JP p/k) juga identik. Rekap setoran: BPJS Kes 4.332.014, BPJS TK 7.945.967, gaji bersih 95.680.002, PPh 21 terutang neto 3.087.764 — **semua cocok**.

## Catatan penguji
- ✅ Batas BPJS Kes (Citra/Hadi 12 jt), batas JP 2026 (JP karyawan Citra 110.863), dasar Kes minimal UMK (Budi 53.968), JKK per orang (Fajar 0,89%), BPJS "kes saja" (Gita), tanpa BPJS (Joko) benar.
- ✅ Lina: kelebihan potong dikembalikan di slip, disebut di "Perlu diperhatikan".
- ⚠️ "Setor PPh 21: Rp 4.018.864" = jumlah PPh positif; kelebihan Lina Rp 931.100 dibayar perusahaan ke karyawan tetapi **tidak** dikurangkan dari setoran (neto 3.087.764). Lihat HASIL-UJI temuan P1-b (PERLU REVIEW).
- ⚠️ Peringatan UMK muncul juga untuk gaji prorata Kiki/Lina ("di bawah UMK") — bisa membingungkan pemilik (prorata bukan pelanggaran UMK).
- ⚠️ Joko (kontrak, 3,8 jt, BPJS "tidak"): ada peringatan UMK, tetapi **tidak ada** peringatan bahwa pekerja wajib didaftarkan BPJS.
- Skor skenario: 9/10.
