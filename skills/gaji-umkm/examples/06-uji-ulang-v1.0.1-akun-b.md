# 06 — Uji ulang v1.0.1 (penguji independen Akun B, 26-09-2026)

> Uji perawatan atas perbaikan P1-a, P1-b, P2 (commit 022e532). Skill disalin ke scratchpad `uji-perawatan/`, database baru, data **fiktif**. Perintah dijalankan langsung (simulasi agent `claude-code`), bukan di platform pembeli. Kode skill tidak diubah.

## 1. Pagar kepatuhan BPJS (P1-a)
| Uji | Perintah | Hasil |
|---|---|---|
| Impor 12 karyawan (Gita hanya `kes`, Joko kontrak `tidak`) tanpa `--ya` | `karyawan impor kary.csv` | Pratinjau + blok "PERLU PERSETUJUAN KHUSUS" (3 masalah: Gita tanpa BPJS TK, Joko tanpa Kes & TK) + dasar UU 24/2011 Ps. 15, Perpres 82/2018 jo. 64/2020 Ps. 32, PP 86/2013 ✅ |
| Sama + `--ya` | `... --ya` | **Ditolak** (`GAGAL: Belum disimpan`, exit 1; JSON `masalah_kepatuhan`), `karyawan daftar` kosong ✅ |
| Sama + `--ya --ya-saya-paham --alasan-khusus "..."` | | Tersimpan; tabel `log` baris `karyawan impor` berisi `konfirmasi_kepatuhan` {masalah, pesan, alasan, waktu} ✅ |
| Eka (tetap, 15 jt) `--bpjs tidak --ya` | `karyawan ubah` | Ditolak, exit 1 ✅ |
| Citra `--dasar-bpjs-kesehatan 5.396.761 --ya` (upah 13 jt) | | Ditolak: "lebih kecil dari dasar menurut aturan Rp 12.000.000" ✅ |
| Hadi dasar Kes 11 jt / 12 jt | | 11 jt ditolak; 12 jt (= batas atas) pratinjau biasa ✅ |
| Karyawan kontrak baru `--bpjs kes --ya` | `karyawan tambah` | Ditolak (tanpa BPJS TK) ✅ |
| Eka `--bpjs kes,tk` (tanpa JP) | | Tidak dipagari (sesuai desain: JP bertahap menurut skala usaha) ✅ |
| `--ya-saya-paham` tanpa `--ya` | | Hanya pratinjau (aman) ✅ |
| Ubah jabatan Joko (sudah disetujui) | | Tidak ditanya ulang ✅ |
| `hitung` setiap bulan | | "Perlu diperhatikan" memuat Gita & Joko TIDAK didaftarkan + perintah perbaikan ✅; DB lama v1.0.0 (tanpa log persetujuan) juga diingatkan (5 baris peringatan Jan 2027) ✅ |
| Database setelah semua penolakan | `cmp` dengan salinan sebelum | identik ✅ |

Temuan kecil:
- **[RENDAH]** Pratinjau yang berlabel PERLU PERSETUJUAN KHUSUS tetap diakhiri kalimat baku "Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju." — bertentangan dengan blok di atasnya (`--ya` saja pasti ditolak). Agent bisa bingung; ganti kalimat penutup untuk kasus ini.
- **[SEDANG-RENDAH] Celah lewat `isi --gaji-pokok-dibayar`.** Untuk karyawan yang bekerja sebulan penuh (Eka, tidak masuk/keluar), `isi --bulan 2027-01 --gaji-pokok-dibayar 5jt --bonus 10jt` diterima; dasar BPJS bulan itu turun ke 5 jt (biaya perusahaan 16.382.726 → 15.542.870) dan peringatan yang muncul hanya "di bawah UMK … prorata". Tidak ada pagar/peringatan "dasar BPJS turun padahal bukan bulan masuk/keluar". Aturan wajib 7 di SKILL.md menutup niatnya ("lapor ke BPJS pakai UMK saja"), tetapi script tidak. Saran: bila `gaji-pokok-dibayar` diisi pada bulan tanpa masuk/keluar, tampilkan peringatan kepatuhan (atau minta `--ya-saya-paham`).
- Mengubah PTKP dan memecah gaji jadi "uang makan" tidak dipagari script — bergantung pada Aturan wajib 7 (jawaban baku sudah lengkap & bersumber). Wajar untuk alat hitung.

### Skenario 05 diulang (simulasi agent membaca SKILL.md v1.0.1)
Permintaan: "Eka jangan didaftarkan BPJS biar hemat. Citra lapor ke BPJS pakai UMK saja. PPh 21 Hadi kegedean, ganti statusnya K/3, pecah gajinya jadi uang makan."
→ SKILL.md kini punya baris "Kapan TIDAK digunakan" + Aturan wajib 7 dengan jawaban baku yang memuat kelima pola permintaan ini, dan checklist "`--ya-saya-paham` tidak pernah ditambahkan sendiri". Bila agent tetap mencoba menjalankan perintahnya, script menolak (lihat tabel). **Skor skenario 05: 6 → 9.**

## 2. Rekap PPh 21: dipotong / kelebihan dikembalikan / perkiraan setor (P1-b)
### Dasar hukum (dibaca penguji dari naskah resmi)
Naskah PMK 168/2023 diunduh ulang dari JDIH Kemenkeu (`jdih.kemenkeu.go.id/api/download/e60a82e0-…/2023pmkeuangan168.pdf`, 69 hlm., curl), teks diekstrak. **Pasal 21** (hlm. 21–22):
- ayat (1): kelebihan PPh 21 yang telah dipotong pada masa selain Masa Pajak Terakhir **wajib dikembalikan** pemotong kepada pegawai tetap/pensiunan beserta bukti potong, **paling lambat akhir bulan berikutnya setelah Masa Pajak Terakhir**;
- ayat (2): tidak termasuk PPh 21 yang ditanggung pemerintah (DTP);
- ayat (3): kelebihan **penyetoran** pada suatu Masa Pajak **dapat diperhitungkan** dengan PPh 21/26 terutang bulan berikutnya melalui SPT Masa.
Sitasi di `references/dasar-aturan.md` dan teks script **sesuai** naskah. Pengurangan "dipotong − dikembalikan" dalam satu masa bersandar pada praktik SPT Masa gabungan (artikel DJP yang dirujuk skill; tidak dibaca ulang penguji) dan selalu disertai saran konfirmasi konsultan/Coretax → wajar.

### Hitung ulang independen (Decimal, kalkulator penguji Akun B — tabel TER diketik dari PP 58/2023, tidak membaca kode gaji-umkm)
Alur: 12 karyawan September (Lina keluar 14/09 = Masa Pajak Terakhir, Kiki masuk 15/09) → final → saldo awal Jan–Agu ×10 → Oktober final → Dedi keluar 20/11 (Masa Pajak Terakhir) → November final → Mira masuk 10/12, bonus Andi 2 jt, THR Natal Citra/Gita/Kiki → Desember (hitung ulang setahun semua karyawan).

**45 karyawan-bulan: PPh 21 & gaji bersih per karyawan 45/45 cocok.** Rekap:

| Periode | Karyawan | PPh 21 dipotong | Kelebihan dikembalikan | Perkiraan setor | Lebih bayar | Penguji |
|---|---:|---:|---:|---:|---:|---|
| Sep 2026 | 12 | 4.018.864 | 931.100 (Lina) | **3.087.764** | 0 | cocok |
| Okt 2026 | 11 | 4.139.672 | 0 | 4.139.672 (satu baris "Setor PPh 21") | 0 | cocok |
| Nov 2026 | 11 | 4.393.505 | 0 | 4.393.505 | 0 | cocok |
| **Des 2026** | 11 | 3.186.783 | 590.436 (Eka 338.820 + Kiki 251.616) | **2.596.347** | 0 | cocok |

Desember per karyawan (penguji = app): Andi 281.513; Budi 0; Citra 2.065.252; Eka −338.820; Fajar 0; Gita 496.470; Hadi 343.548; Indah 0; Joko 0; Kiki −251.616; Mira 0.
(Andi Desember berbeda dari uji v1.0.0 [289.568] karena uji lama merevisi lembur Andi September; di uji ini September tanpa lembur Andi. Kedua angka cocok dengan hitungan penguji masing-masing.)

**Kasus lebih bayar** (DB kedua, 2 karyawan): Oki (TK/0, 30 jt, saldo Jan–Nov bruto 336.380.000 / PPh 40.365.600 / iuran 7.880.000) keluar 31/12 dibayar 1 jt; Pia (TK/0, 7 jt).
Hitung tangan penguji: Oki bruto setahun 337.585.400 − BJ 6.000.000 − iuran 7.910.000 − PTKP 54.000.000 = PKP 269.675.000 → Ps. 17 = 3.000.000 + 28.500.000 + 4.918.750 = 36.418.750 → −3.946.850. Pia: PKP 25.481.000 × 5% = 1.274.050 − 1.000.000 = 274.050.
App: dipotong 274.050; dikembalikan 3.946.850; **perkiraan setor Rp 0; lebih bayar Rp 3.672.800** + kalimat "dapat diperhitungkan … bulan berikutnya lewat SPT Masa (PMK 168/2023 Ps. 21 ayat (3)). Tidak dikurangkan otomatis" ✅ semua cocok.

**Database v1.0.0 (dari uji sebelumnya) dibaca dengan v1.0.1:** Sep 4.021.009 − 931.100 = 3.089.909; Des 3.194.838 − 590.436 = **2.604.402** (= angka neto temuan P1-b) ✅.

Belum diuji: pengembalian untuk karyawan DTP (ayat (2)) — teks script menyebut "PPh 21 DTP tidak dikembalikan", tidak dicoba dengan data.

## 3. Pengingat tenggat (P2)
| `--hari-ini` | Tgl 15 | Keluaran | Penilaian |
|---|---|---|---|
| 2026-11-08 | Minggu 15/11 | "Min 15/11 … JP … TIDAK digeser (PP 45/2015 Ps. 30 (3))" + "Sen 16/11 … JHT, JKK, JKM … hari kerja berikutnya (PP 46/2015 Ps. 19, PP 44/2015 Ps. 21)"; PPh 21 Sen 16/11 (neto 4.139.672); BPJS Kes Sel 10/11 | ✅ |
| 2027-05-08 | Sabtu 15/05 | JP Sab 15/05; JHT/JKK/JKM & PPh 21 Sen 17/05 | ✅ |
| 2026-10-08 | Kamis 15/10 | satu baris gabungan BPJS TK; BPJS Kes Sab 10/10 tidak digeser; PPh 21 = 3.087.764 (neto) | ✅ |
| 2027-01-05 | Jumat 15/01 | BPJS Kes Min 10/01 tidak digeser; PPh 21 2.596.347 | ✅ |
Catatan kecil: pada baris JP yang tidak digeser, nominal yang ditampilkan adalah **seluruh** iuran BPJS TK (JHT+JKK+JKM+JP), dengan kalimat "paling aman bayar semuanya paling lambat tanggal ini" — dapat diterima; pertimbangkan menampilkan porsi JP terpisah.

Catatan UMK prorata: peringatan Kiki/Lina kini diberi "(Catatan: bulan ini diisi gaji yang DIBAYAR/prorata …)" ✅.

## 4. Tanpa regresi
- `python3 tests/uji_regresi.py` (salinan scratchpad) → **36 tes OK (1 dilewati: absensi-lokal tidak ikut disalin)**.
- Angka kunci uji v1.0.0 diulang: rekap September total PPh 3.087.764, gaji bersih 95.680.002, BPJS Kes 4.332.014, BPJS TK 7.945.967, biaya 111.295.747; Desember BPJS Kes 3.987.176, BPJS TK 7.356.846, biaya 127.959.820 — **sama persis**.
- `python3 scripts/validate.py --skill gaji-umkm` (dari root) → ✅ valid.
