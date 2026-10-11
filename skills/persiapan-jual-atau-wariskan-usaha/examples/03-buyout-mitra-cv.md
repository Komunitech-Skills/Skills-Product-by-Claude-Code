# Skenario 3 (normal): sekutu CV ingin membeli bagian mitra yang keluar

- Tanggal: 2026-10-09 · Penguji independen · `claude-code (simulasi agent)` · data fiktif

## Pesan pengguna

> Saya Rudi, punya CV Mitra Teknik (servis & pasang AC) di Bandung bareng Yanto. Porsi saya 60%, Yanto 40%. Yanto mau keluar, saya mau beli bagiannya. Laba 2024 240 juta, 2025 270 juta (sudah dipotong gaji kami masing2 7 juta/bulan). Pengganti Yanto nanti kepala teknisi gaji 6 juta/bulan. Alat, mobil operasional dll 180 juta, turun 20%. Utang leasing mobil 60 juta. Kami berdua sepakat pakai 2 sampai 2,5 kali laba. Biaya notaris dll anggap 3%. Bagian Yanto kira2 berapa, dan apa saja yang harus diurus?

## Perintah hitung

```
python3 scripts/nilai_usaha.py --laba 2024=240000000 2025=270000000 --kelipatan 2 2.5 --aset 180000000 \
  --utang 60000000 --penyesuaian-aset 20 --gaji-diambil 84000000 --gaji-pengganti 72000000 --biaya-transaksi 3
```
(Gaji Rudi tetap dianggap biaya karena ia tetap bekerja; yang ditambahkan kembali hanya gaji Yanto Rp84 juta, diganti kepala teknisi Rp72 juta.) Porsi 40% dihitung agent secara eksplisit karena script tidak punya opsi porsi.

## Output agent (SESUDAH)

# Persiapan Pengalihan Bagian Sekutu "CV Mitra Teknik"

**1. Ringkasan dan asumsi**
- Jalur: **serahkan ke mitra** (Rudi membeli 40% bagian Yanto). Kerangka default 6 bulan (belum disebut; sebut bila berbeda).
- Laba sudah dipotong gaji kalian berdua. Karena Yanto keluar, gajinya (Rp84.000.000/tahun) ditambahkan kembali dan diganti gaji kepala teknisi (Rp72.000.000/tahun).
- Kelipatan 2-2,5: **kesepakatan kalian berdua**, bukan angka pasar.
- Laba baru 2 tahun: rentang kurang kuat.

**2. Daftar periksa kesiapan** (ringkas)

| Area | Status | Langkah berikut |
|---|---|---|
| Pembukuan | Setengah (2 tahun) | Lengkapi laporan, cocokkan dengan rekening CV |
| Ketergantungan pada Yanto | Belum diketahui | Pelanggan/proyek mana yang dipegang Yanto? |
| SOP | Belum diketahui | Tulis SOP pasang & servis sebelum Yanto keluar |
| Aset & utang | Siap (alat/mobil Rp180 juta; leasing Rp60 juta) | Leasing atas nama siapa? |
| Akta CV & izin | Belum diketahui | Siapkan akta pendirian/perubahan CV, NIB |
| Kontrak pelanggan/garansi | Belum diketahui | Garansi pemasangan yang masih berjalan siapa yang tanggung? |
| Karyawan | Belum diketahui | Teknisi tetap & hak yang tertunda |

**Prioritas:** (1) baca akta CV soal keluarnya sekutu, (2) daftar proyek/pelanggan yang dipegang Yanto, (3) SOP dan serah terima pengetahuan teknis.

**3. Perkiraan rentang nilai** *(bahan negosiasi, bukan harga pasti)*

Laba setelah penyesuaian: 2024 Rp252.000.000; 2025 Rp282.000.000; rata-rata/basis Rp267.000.000.

| Metode | Rumus | Hasil seluruh CV |
|---|---|---|
| Kelipatan laba | Rp267.000.000 × [2-2,5] × (100 - 0)/100 | Rp534.000.000 s/d Rp667.500.000 |
| Nilai aset bersih | Rp180.000.000 × (100 - 20)/100 - Rp60.000.000 | Rp84.000.000 |
| Rentang gabungan, setelah biaya 3% | | Rp81.480.000 s/d Rp647.475.000 |

**Bagian Yanto 40%** dari metode kelipatan laba: Rp534.000.000 × 40% = **Rp213.600.000** s/d Rp667.500.000 × 40% = **Rp267.000.000**.
Catatan: utang leasing Rp60.000.000 adalah utang CV. Bila penilai/notaris menyarankan utang dikurangkan dulu: (Rp534.000.000 - Rp60.000.000) × 40% = Rp189.600.000 s/d (Rp667.500.000 - Rp60.000.000) × 40% = Rp243.000.000. Siapa menanggung biaya notaris juga perlu disepakati. Pajak belum dihitung.

**4. Pilihan struktur (tanyakan ke notaris/konsultan pajak):** bayar sekaligus atau cicil (mis. 12 bulan: Rp17.800.000 s/d Rp22.250.000 per bulan dari angka 40% di atas, belum termasuk bunga/kesepakatan lain); Yanto mendampingi 1-3 bulan; perlu sekutu baru atau CV diubah/diganti bentuknya bila tinggal satu sekutu.

**5. Rencana transisi 6 bulan:** bulan 1 baca akta CV + sepakati angka; bulan 2 notaris & konsultan pajak; bulan 2-3 serah terima proyek/pelanggan Yanto, SOP; bulan 3-4 akta perubahan, pembayaran; bulan 4-6 perubahan data izin, rekening, leasing; umumkan ke pelanggan.

**6. Dokumen:** akta pendirian & perubahan CV, NIB, laporan keuangan 2024-2025, daftar aset & BPKB, perjanjian leasing, daftar proyek & garansi berjalan, daftar karyawan.

**7. Pertanyaan untuk notaris & konsultan pajak:** bagaimana bentuk usaha kami harus diubah saat Yanto keluar; dokumen bukti peralihan; bagaimana kontrak leasing/pelanggan dialihkan; apa kewajiban pajak atas pengalihan bagian ini; perlukah laporan pajak lama dirapikan dulu.

**8. Penutup.** Ini persiapan, bukan nasihat hukum/pajak atau penilaian resmi; tanggal acuan Oktober 2026. Pertanyaan: (1) Yanto sekutu aktif atau pasif di akta? (2) Target selesai kapan? (3) Leasing atas nama CV atau pribadi?

## Catatan penguji

- Angka diverifikasi independen (Decimal): 240+84-72=252; 270+84-72=282; rata 267; ×2 = 534; ×2,5 = 667,5; aset 180×0,8-60 = 84; ×0,97: 81,48 dan 647,475 juta; 40%: 213,6 dan 267 juta; setelah utang: 189,6 dan 243 juta; cicil /12: 17,8 dan 22,25 juta. **Semua cocok.**
- Kekurangan yang berasal dari skill: tidak ada panduan untuk **pembelian bagian mitra** (porsi kepemilikan, utang badan usaha dikurangkan atau tidak, siapa menanggung biaya), padahal description menyebut "serahkan ke mitra". Script tidak punya opsi porsi; agent harus berimprovisasi. Pertanyaan notaris belum menyebut **akta perubahan CV & pendaftaran perubahan** atau **persetujuan sekutu/organ (untuk PT: UU 40/2007 Pasal 57)**. Script juga menerapkan biaya transaksi 3% ke nilai aset bersih, yang membingungkan dalam konteks ini.
- Nilai: **7,0/10.**
