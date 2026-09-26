# 07 — Uji ulang v1.0.2 (penguji independen Akun B, 26-09-2026)

> Uji perawatan atas perbaikan temuan uji ulang v1.0.1 (U19): celah `isi --gaji-pokok-dibayar` di bulan penuh [SEDANG-RENDAH] dan teks penutup pratinjau PERLU PERSETUJUAN KHUSUS [RENDAH]. Skill disalin ke scratchpad `rt-u19b/sk/`, database baru, data **fiktif**, simulasi agent `claude-code`. v1.0.1 pembanding diambil dari `git archive 230da94`. Kode skill tidak diubah.

## Data
"CV Uji Gaji Fiktif", UMK diisi 4.500.000, JKK default 0,24%. 11 karyawan (impor CSV): E01–E08 bulan penuh (TK/0 s.d. K/3, gaji 4,5–25 jt, E06 tanpa JP), **E09 masuk 01/10/2026**, **E10 masuk 13/10/2026**, **E11 keluar 20/10/2026** (saldo awal Jan–Sep: bruto 61.155.900, PPh 764.442, iuran 1.755.000).

## 1. Pagar `isi` yang menurunkan dasar BPJS di bulan penuh
| Uji | Hasil |
|---|---|
| E04 (penuh) `isi --gaji-pokok-dibayar 5jt --bonus 4,5jt` tanpa flag | **GAGAL exit 1**, "PERLU PERSETUJUAN KHUSUS … Rp 5.000.000 lebih kecil dari data karyawan Rp 9.500.000 … sebulan penuh", dasar UU 24/2011 Ps. 15, Perpres 82/2018 jo. 64/2020 Ps. 32, PP 86/2013; DB `cmp` identik ✅ |
| Sama + `--ya` | ditolak, DB identik ✅ |
| `--json` | `{"ok": false, "masalah_kepatuhan": ["dasar_bpjs_turun_bulan_penuh"]}` ✅ |
| `+ --ya-saya-paham --alasan-khusus "cuti di luar tanggungan …"` | tersimpan; tabel `log` baris `isi` berisi `konfirmasi_kepatuhan` {masalah, pesan, alasan, waktu} ✅ |
| E05 `--tunjangan-tetap-dibayar 0` (penuh) | ditolak ✅ |
| E09 masuk **tanggal 1** (batas) `--gaji-pokok-dibayar 8jt` | ditolak — tanggal 1 = bulan penuh, benar ✅ |
| E05 gp 13 jt + tunj. 2 jt (jumlah = data 15 jt) / E03 gp = data | tidak dipagari (dasar tidak turun) ✅ |
| **E10 masuk 13/10 prorata** gp 5.565.217 + tunj. 278.261 | tersimpan tanpa hambatan ✅ |
| **E11 keluar 20/10 prorata** gp 4.239.130 | tersimpan tanpa hambatan ✅ |
| `isi --file` (E07 gp 15 jt + bonus 10 jt, E01 bonus) pratinjau | berlabel PERLU PERSETUJUAN KHUSUS; `--ya` ditolak, DB identik; `--ya --ya-saya-paham --alasan-khusus` tersimpan, log `isi --file` `['dasar_bpjs_turun_bulan_penuh:E07']` + alasan ✅ |
| `hitung --bulan 2026-10` | "Perlu diperhatikan" menyebut Dodi & Gilang (dasar turun di bulan penuh) ✅ |
| DB celah uji 06 (Eka Jan 2027 disimpan v1.0.1 tanpa pagar) dibuka v1.0.2 → `hitung` | kini diingatkan ✅ |

Pratinjau berlabel PERLU PERSETUJUAN KHUSUS (`karyawan tambah --bpjs tidak`, `isi --file`) kini ditutup "BELUM BISA DISIMPAN DENGAN --ya SAJA … jalankan perintah yang sama + --ya --ya-saya-paham --alasan-khusus "..." … Jangan menambahkan --ya-saya-paham atas inisiatif sendiri." — tidak lagi bertentangan ✅. Pesan GAGAL `isi` menyebut "+ --ya --ya-saya-paham"; untuk `isi` (perintah kecil) `--ya` tidak wajib, tetapi tidak salah (dengan `--ya` juga tersimpan).

Catatan **[RENDAH, desain]**: `karyawan ubah --gaji-pokok 5jt` (E05, 15 jt → 5 jt) hanya pratinjau biasa tanpa peringatan dasar BPJS. Menurunkan gaji di data induk bisa sah (perubahan kontrak), jadi wajar tidak dipagari; pencegahan "turunkan lalu kembalikan" bergantung pada Aturan wajib 7. Pertimbangkan peringatan bila turun > 25%.

## 2. Angka BPJS & PPh 21 — verifikasi Decimal independen (21 karyawan-bulan)
Kalkulator penguji `verif_u19b.py` (Decimal, ditulis tanpa membaca kode gaji-umkm/mesin): Kes 4%/1% dasar min UMK maks 12 jt; JHT 3,7%/2%; JKK 0,24%; JKM 0,3%; JP 2%/1% maks 11.086.300; lembur upah/173 × (1,5 + 2×(jam−1)); TER PP 58/2023 (tabel A/B/C diketik dari lampiran PP oleh penguji Akun B sebelumnya); Masa Pajak Terakhir Ps. 17, biaya jabatan 5% maks 500rb/bulan, PKP dibulatkan ke bawah ribuan.

**Oktober 2026 (11 karyawan): 11/11 cocok** (bruto pajak, PPh 21, gaji bersih, 8 komponen iuran):
E01 0 · E02 28.748 · E03 144.948 · E04 0 · E05 933.660 (Kes & JP kena batas) · E06 15.681 · E07 3.088.195 · E08 0 (lembur 234.104) · E09 287.485 · E10 0 (prorata, dasar 5.843.478) · E11 **−667.692** (Masa Pajak Terakhir, Kes pakai UMK 4,5 jt karena upah prorata 4.239.130 < UMK).
Total cocok: Kes 3.157.739 + 789.435 = **3.947.174**; BPJS TK **7.565.852**; PPh dipotong **4.498.717**, dikembalikan **667.692**, perkiraan setor **3.831.025**.
**November 2026 (10 karyawan, setelah Oktober final): 10/10 cocok**; setor Kes **4.075.000**, BPJS TK **8.450.178**, PPh 21 **4.732.780**.

**Tidak berubah dari v1.0.1:** DB yang sama dihitung dengan v1.0.1 (`git archive 230da94`) dan v1.0.2 → `payroll` per karyawan & `total` **identik** untuk Oktober (11) dan November (10); v1.0.2 hanya menambah 2 baris peringatan. DB uji 06 dibaca v1.0.2: Sep PPh 4.018.864 − 931.100 = **3.087.764**, Kes 4.332.014, TK 7.945.967, biaya 111.295.747; Des 3.186.783 − 590.436 = **2.596.347**, Kes 3.987.176, TK 7.356.846, biaya 127.959.820 — sama persis.

## 3. Tanpa regresi
- `python3 tests/uji_regresi.py` → **40 tes OK** di repo; salinan scratchpad 40 OK (1 dilewati: repo skill sumber tidak ada).
- `python3 scripts/validate.py --skill gaji-umkm` → ✅ valid.
- Belum dikerjakan (tidak diklaim v1.0.2): baris JP tanpa geser di `pengingat` masih menampilkan total seluruh iuran BPJS TK (P3/RENDAH lama).

**Skor: 9/10.**
