# 00 — Uji A/B skenario 01: agent TANPA skill vs DENGAN gaji-umkm

> Penguji independen Akun B, 26-09-2026. Permintaan & data sama dengan `01-gaji-september-12-karyawan.md`.
> "Tanpa skill" = penguji (Claude, tanpa membaca folder gaji-umkm) mengerjakan sendiri permintaan yang sama dengan Python + pengetahuan umum + web search — ini justru **batas atas** agent tanpa skill; agent umum biasanya lebih buruk.

## Hasil tanpa skill
- Angka: setelah ± 1 jam kerja (mengetik ulang tabel TER PP 58/2023 A/B/C, mencari batas JP 2026 di web, menulis kalkulator Decimal), penguji **bisa** menghasilkan angka yang sama persis untuk 12 karyawan (itulah verifikator independen di 01).
- Tetapi jebakan yang nyata untuk agent umum tanpa skill (dilihat juga di skill publik pesaing, lihat 00-banding-pesaing):
  - batas upah JP masih Rp 10.547.400 (berlaku s.d. Feb 2026) → JP Citra/Eka/Hadi salah;
  - bruto TER tanpa premi JKK/JKM/BPJS Kes perusahaan → PPh 21 kurang potong (Eka: Rp 900.000 vs benar Rp 1.092.420);
  - dasar BPJS Kes tidak dinaikkan ke UMK untuk gaji di bawah UMK (Budi);
  - Lina (resign 14/09) dihitung TER biasa, padahal Masa Pajak Terakhir → seharusnya kelebihan Rp 931.100 dikembalikan.
- Tidak ada: database/riwayat bulan lalu, kunci periode, revisi tercatat + selisih, slip per karyawan, CSV transfer, penyamaran NIK/rekening, cadangan otomatis, rekap tahunan & cek bukti potong, pengingat tenggat. Bulan depan semua harus diulang dari nol, dan Desember butuh data Jan–Nov yang tidak tersimpan.
- Konsistensi: format berubah tiap kali; tidak ada pratinjau/persetujuan sebelum perubahan.

## Hasil dengan skill
- 12/12 karyawan cocok dengan verifikasi independen (semua komponen), dalam ± 6 perintah dan < 1 menit waktu script.
- Menolak menghitung Lina sebelum data Jan–Agu tersedia, lalu menghitung ulang setahun dengan benar.
- Peringatan UMK, kelebihan potong, disclaimer + dasar aturan + tanggal berlaku + catatan Coretax otomatis.
- Setelah final: slip, CSV transfer (rekening disamarkan/lengkap hanya di file), revisi dengan selisih.

## Kesimpulan
Dengan skill **jelas lebih baik**: bukan hanya angka (yang bisa benar tanpa skill bila agent sangat teliti), tetapi alur operasional bulanan yang tidak bisa dicapai jawaban sekali jadi. Bahan "sebelum/sesudah" README valid.
