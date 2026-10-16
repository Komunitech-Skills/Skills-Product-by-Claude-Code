# HASIL UJI — ekstrak-nota-faktur

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** Python 3 lokal. `scripts/cek_nota.py` dijalankan sungguhan di `/tmp/uji-ekstrak-nota-faktur/`. Verifikasi dengan script terpisah (`verif/verif.py`) yang tidak mengimpor kode skill.
- **Skenario:** 01–05 + uji A/B (`00-pembanding-tanpa-skill.md`) + banding pesaing (`00-banding-pesaing.md`)
- **Jalur:** KURASI dari manairalabs/bicara-skills `invoice-extract-id` (MIT)

## Audit keamanan
- `cek_nota.py`: hanya library standar. Tidak ada jaringan, `subprocess`, `eval`/`exec`, atau penghapusan file. Hanya membaca JSON yang diberikan (atau stdin) dan menulis `--output`.
- SKILL.md, README, `references/*`, dan template bersih dari prompt injection. Ada pengaman: larangan kata "palsu/tidak sah", format identitas hanya sebagai peringatan, data pribadi tidak disebarkan, rujukan DJP/konsultan. Contoh memakai data fiktif. **Aman.**

## Pemeriksaan ATTRIBUTION.md (jalur kurasi)
| Cek | Hasil |
|---|---|
| Teks MIT asli lengkap | ✅ **Identik byte-per-byte** dengan `LICENSE` di `main` bicara-skills saat ini (diff kosong), termasuk "Copyright (c) 2026 Manaira Labs" |
| Sumber, versi, tanggal | ✅ URL dan folder benar. v0.1.0 = commit awal `7de3633` 2026-04-17 (terverifikasi dari riwayat git). Commit sesudahnya (2026-09-20) hanya mengubah README. |
| Perubahan disebut | ✅ 10 butir perubahan (aturan PPN 11/12, format Coretax 17 digit/NITKU 22, script baru, rekap, TIDAK_TERBACA, skema baru, output awam, contoh baru, referensi regulasi, field yang dihapus). Klaim tentang sumber (12% × DPP penuh, menolak NPWP selain 15/16 digit, "still fill required fields") **sesuai** dengan isi SKILL.md sumber. |
| Tidak menyalin utuh | ✅ Isi ditulis ulang dalam Bahasa Indonesia. Hanya ide skema/jebakan yang sama. Tidak ada paragraf yang disalin. |
| Catatan | `LISENSI.txt` yang dirujuk tidak ada di folder skill (kemungkinan dibuat di tahap paket). Pastikan ATTRIBUTION.md ikut di setiap paket jual, karena MIT mewajibkan notice ikut serta. |

## Verifikasi angka (independen)
| Uji | Hasil |
|---|---|
| PPN tanggal ≥ 2025 barang biasa = floor(DPP × 11/100) (= 12% × 11/12, dibulatkan ke bawah): 1.300.000 → 143.000; 10.750.000 → 1.182.500; 1.234.567 → 135.802 (tertulis 135.803 masih dalam toleransi ±1); 999.999 → 109.999 | ✅ Script sama |
| 12% penuh untuk barang biasa (1.290.000; 148.148; 1.800.000) | ✅ Diberi peringatan dengan angka seharusnya |
| Tarif menurut tanggal: 2021 → 10%, Des 2024 → 11%, mewah Jan 2025 → 11% (transisi), mewah Feb 2025 → 12% | ✅ |
| Struk harga termasuk PPN: DPP = harga × 100/111. PPN salah tarif (DPP 100.000 + PPN 19.200) | ✅ Selisih terdeteksi |
| DPP nilai lain 11/12 (9.854.166,67 vs tertulis 9.854.167) | ✅ Dalam toleransi |
| Terbilang: 331 angka (0 s.d. ~10¹², termasuk 11, 100, 1.000, 1.001.000, sebelas, seratus, seribu) dibandingkan dengan implementasi terpisah per kelompok 3 digit | ✅ 331/331 identik |
| Pembacaan terbilang: 200 dokumen acak (huruf besar, "# … saja #"), 50 sengaja salah Rp 1.000 | ✅ 200/200 benar. Dengan sen ("sembilan puluh sen"), "25.000,-", dan "saja" juga benar. |
| Rekap S1 9.792.700 / PPN 154.813; S2 17.590.000 | ✅ |
| **TIDAK_TERBACA tidak ditebak/dijumlah** (S3 foto buram, contoh N1, kuitansi J) | ✅ `total_rekap` null, dokumen masuk daftar "belum masuk total", subtotal tidak dihitung bila ada item tidak terbaca, terbilang yang terbaca tidak dipakai untuk mengisi total |
| Data rusak/tepi: `Rp 1.500.000`, `1.500.000,50`, `25.000,-`, `1,8 juta`, `0`, format Inggris `1,250,000.00` (ditolak), angka parsial `3?1.500` (ditolak), tanggal 31/02 (ditolak), file kosong, `{"dokumen":[]}`, `{}` | ✅ Dihitung benar, atau ditolak dengan pesan `ERROR:` dan kode keluar 2 |

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Frasa awam + Inggris (receipt/invoice OCR), batas dengan buat-invoice/hitung-ppn jelas |
| Kemudahan awam | 9 | Kirim foto → tabel + "yang perlu dicek" + CSV Excel |
| Kualitas output | 9 | Status per dokumen, rekap tiga sudut, meterai, PPh, deteksi dobel, CSV aman untuk nol di depan |
| Akurasi (angka/fakta) | 9 | Semua hitungan dan aturan PPN benar. Ada alarm palsu kecil (NPWP 15 digit pada faktur 2024). |
| Penanganan input kurang | 8 | Default + asumsi baik. Panduan "hanya angka diketik" belum ada. |
| Penanganan di luar cakupan | 9 | Coretax/DJP/konsultan, tanpa kata "palsu" |
| Keamanan | 10 | Bersih, lokal |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: skill **jelas lebih baik**. Tanpa skill, agent keliru menuduh PPN 12% × 11/12 sebagai kurang bayar, serta melewatkan meterai dan terbilang. Banding pesaing: unggul jelas atas skill sumber `invoice-extract-id`, yang memakai aturan PPN usang (2 alarm palsu di S1, kelebihan PPN Rp 107.500 lolos di S2) dan meminta kolom tetap diisi walau ragu. Kurasi ini memberi nilai tambah nyata. Tidak ada cacat berat atau sedang.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
1. **Angka hasil hitungan tidak ditandai di CSV/JSON.** Bila `subtotal` null dan item lengkap, `subtotal` diisi jumlah item (`cek_nota.py` baris 486–487), dan bila DPP tidak tertulis, `dpp = dasar` (baris 512–514). Keduanya tampil di kolom CSV Subtotal/DPP seolah angka dokumen (S1: N2 Subtotal 720500). Ini bertentangan dengan `references/skema-data.md` bagian 1. **Saran:** simpan di `subtotal_dihitung`/`dpp_dihitung`, atau tambahkan kolom CSV "Dihitung script", dan kosongkan kolom dokumen.
2. **Peringatan NPWP 15 digit tidak melihat tanggal** (`cek_npwp`, baris 297–313). Faktur Desember 2024 menjadi "PERLU DICEK" padahal formatnya wajar untuk tanggal itu (S2). **Saran:** teruskan `tanggal`. Bila < 2025-01-01, jadikan level `info`.
3. **Tidak ada `ppn_seharusnya`/`total_seharusnya` di hasil** saat PPN keliru, sehingga agent menghitung selisih dan total yang benar sendiri (S2, S4), padahal SKILL.md langkah 4 meminta angka dari script. **Saran:** tambahkan kedua field ke JSON dan pesan peringatan.
4. **Penanda tidak konsisten di CSV:** `TIDAK_TERBACA` (tanggal/nomor, via `str_bersih`) vs `TIDAK TERBACA` (angka/ID, baris 767–768, 780–781). Satukan.
5. **Satu nilai rusak menggagalkan seluruh batch** (`GalatInput` di `cek_dokumen` menghentikan semua dokumen). **Saran:** tangkap per dokumen, beri status "INPUT TIDAK VALID" + pesan, lanjutkan dokumen lain.
6. Info "Ada PPN tapi NPWP penjual tidak tercantum" juga muncul bila NPWP hanya belum diketik pengguna (S4). SKILL.md sebaiknya menyebut: "abaikan info ini bila data berasal dari ketikan, bukan dokumen".
7. SKILL.md bagian Input belum memandu kasus "pengguna hanya mengetik angka tanpa foto" (S4). Tambahkan satu baris.
8. Skill rujukan `hitung-ppn` masih kosong di repo, dan tidak ada kalimat cadangan bila skill rujukan tidak terpasang (S5).
9. Bila `total` TIDAK_TERBACA tetapi terbilang terbaca (mis. "Tiga juta seratus ribu rupiah"), script diam. Saran: tampilkan sebagai **petunjuk** ("terbilang terbaca bernilai Rp 3.100.000, cocokkan dengan nota asli"), bukan untuk mengisi total.

## Ide dari pesaing (bukan salinan)
Tambahkan kolom jatuh tempo dan rekening tujuan (juga untuk mencegah penipuan "ganti rekening"), jenis PO/surat jalan, dan promosikan `--format json` untuk impor ERP.

## Contoh disegarkan ke v1.0.5 (2026-10-16)
Bukan uji baru: skor **8/10 — LULUS** (uji 2026-09-23) **tidak berubah**. Keluaran script di contoh 01–04 dijalankan ulang dengan `scripts/cek_nota.py` v1.0.5 (`--hari-ini 2026-09-23`, data hasil baca yang sama) agar kolom, label, dan status sama dengan versi sekarang. Angka kunci dihitung ulang terpisah dengan `Decimal`: cocok semua.

| Contoh | Yang berubah di keluaran | Angka kunci (tidak berubah kecuali disebut) |
|---|---|---|
| 01 rekap 4 nota | CSV memakai kolom **Subtotal Hitung Ulang / DPP Hitung Ulang / PPN Seharusnya / Total Seharusnya / Total Untuk Rekap**; Subtotal N1 & N2 kini kosong (tidak tertulis di dokumen) dan hasil jumlah pindah ke Subtotal Hitung Ulang (temuan Ringan 1 selesai) | N2 Subtotal Hitung Ulang 720.500 vs Total 730.500 (selisih Rp 10.000); rekap Rp 9.792.700; PPN tercantum Rp 154.813 |
| 02 faktur PPN 12% penuh | **F2 kini COCOK** (NPWP 15 digit pada faktur 2024 hanya info; temuan Ringan 2 selesai); PPN/Total Seharusnya F1 dari script (temuan Ringan 3 selesai) | F1 PPN seharusnya Rp 1.182.500, total seharusnya Rp 11.932.500, beda Rp 107.500; rekap Rp 17.590.000; PPN faktur pajak Rp 1.840.000 |
| 03 foto buram | sel tak terbaca seragam `TIDAK_TERBACA` (temuan Ringan 4 selesai); catatan pola `?` (v1.0.4) dan INPUT TIDAK VALID per dokumen (temuan Ringan 5 selesai) | belum masuk rekap; total pengeluaran 0; besi 12 × 87.500 = 1.050.000 |
| 04 input kurang | total seharusnya kini dari script | PPN seharusnya Rp 1.650.000, total seharusnya Rp 16.650.000, beda Rp 150.000 |
| 05 di luar cakupan | tidak memuat keluaran script; tidak berubah | ilustrasi PPN Rp 2.200.000 |

Kanal chat (aturan v1.0.5): contoh 01–04 kini punya bagian **"Versi kanal chat (Telegram/WhatsApp)"** tanpa tabel Markdown — satu baris padat per dokumen, berkas CSV dilampirkan sebagai dokumen (tanpa menyebut jalur folder), dan bila CSV ikut ditampilkan di chat memakai `--pemisah tab` dengan kolom yang kosong di semua baris dibuang. Tampilan bertabel di bagian "Output" tetap untuk Claude Code/Cursor. Temuan lama di "Daftar cacat" dibiarkan sebagai riwayat uji.
