---
name: pph-final-umkm
description: Menghitung PPh Final UMKM 0,5% per bulan dengan pelacak omzet kumulatif setahun untuk orang pribadi (Rp500 juta pertama bebas pajak, bulan saat melewati batas dihitung proporsional) maupun badan, lengkap tabel per bulan, batas setor, catatan PPh 22 marketplace, peringatan batas Rp4,8 miliar, dan disclaimer. Gunakan saat pengguna tanya "pajak UMKM bulan ini berapa", "PPh 0,5%", "omzet 500 juta bebas pajak", atau small business final income tax Indonesia, PP 55 PP 20/2026. Bukan untuk PPN (pakai hitung-ppn) atau laporan keuangan (pakai laporan-keuangan-emkm).
---

# PPh Final UMKM 0,5%

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pelaku UMKM tahu berapa PPh Final 0,5% yang perlu disetor tiap bulan, berapa sisa omzet bebas pajak, dan kapan batas-batas penting terlewati — dengan tabel yang siap disimpan atau diserahkan ke admin/konsultan.

## Kapan digunakan
- "Omzet saya Jan–Jun sekian, pajaknya berapa per bulan?"
- "Kapan omzet saya mulai kena pajak (lewat Rp500 juta)?"
- "PT perorangan/koperasi saya omzet X, PPh finalnya berapa?"
- Rekap tahunan omzet vs batas Rp4,8 miliar.

## Kapan TIDAK digunakan
- PPN → skill `hitung-ppn`. Laporan laba rugi/neraca → skill `laporan-keuangan-emkm`.
- Penghasilan dari jasa pekerjaan bebas (dokter, notaris, konsultan, dsb.), gaji (PPh 21), atau WP yang memakai pembukuan & tarif umum → di luar cakupan, arahkan ke konsultan pajak/DJP.
- Mengisi SPT, membuat kode billing, atau lapor di Coretax → beri tahu bahwa skill ini hanya menghitung.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Omzet (peredaran bruto) per bulan | Ya | — (tanyakan) |
| Jenis wajib pajak: orang pribadi atau badan (PT perorangan, koperasi, CV, firma, PT) | Ya | Orang pribadi, sebutkan asumsinya |
| Tahun pajak | Tidak | Tahun berjalan |
| Bulan pertama data | Tidak | Januari |
| Omzet tahun ini sebelum bulan pertama data | Tidak | Rp 0 (beri pengingat bila data tidak mulai Januari) |
| PPh 22 yang sudah dipotong marketplace per bulan | Tidak | Rp 0 |
| Tahun NPWP terdaftar (untuk batas jangka waktu tarif 0,5%) | Tidak | Tidak dihitung — script tetap memberi aturan umumnya; tanyakan bersama pertanyaan lain bila memang perlu bertanya |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Omzet = total penjualan kotor sebelum dikurangi biaya, dari **semua** usaha.

## Langkah kerja
1. Kumpulkan omzet per bulan. Data berupa file? Terima CSV (`bulan;omzet;pph22`) atau JSON.
2. Jalankan script. Script ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill); jalankan dari sana, jangan mencari ke seluruh disk (`find /`). Windows: `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/pph_final.py --jenis op --tahun 2026 --omzet 45jt 60jt 80jt 120jt 150jt 90jt
   ```
   - Mulai bukan Januari: `--bulan-awal 7 --omzet-sebelumnya 320jt`.
   - Badan: `--jenis badan --jenis-badan pt-perorangan|koperasi|cv|firma|pt|lainnya`.
   - PPh 22 marketplace: `--pph22 0 0 250rb ...` (urutan sama dengan omzet).
   - Dari file: `--file omzet.csv` (kolom `bulan`, `omzet`, opsional `pph22`).
   - Tahun NPWP terdaftar disebut pengguna (mis. "NPWP dari 2021")? Wajib tambahkan `--tahun-terdaftar 2021`.
   - `--hari-ini 2026-09-23` untuk menentukan tanggal acuan (default hari ini); bulan dengan PPh > 0 yang batas setornya sudah lewat ditandai "SUDAH LEWAT".
   - `--format json` untuk angka mentah.
3. Salin tabel & ringkasan dari script apa adanya ke balasan chat. Tambahkan 1–2 kalimat penjelasan dengan bahasa sederhana (mis. "Bulan Juni omzet Anda melewati Rp500 juta, jadi hanya Rp45 juta yang kena pajak").
4. Selalu sertakan catatan penting dan disclaimer dari output — salin apa adanya, jangan diringkas jadi "sesuai aturan terbaru". **Dua catatan ini wajib muncul di balasan bila ada di output:**
   - **Batas setor jatuh hari libur** (mis. "15 November 2026 jatuh hari Minggu → boleh disetor paling lambat Senin 16 November 2026, PMK 81/2024 Pasal 100"). Sebut tanggal hari kerjanya, bukan hanya tanggal 15.
   - **Batas jangka waktu tarif 0,5%** (PP 55/2022 Pasal 59: orang pribadi 7 tahun pajak sejak terdaftar, mis. NPWP 2021 → s.d. 2027) beserta keterangan bahwa perubahan oleh PP 20/2026 belum diverifikasi.
5. **Fallback tanpa Python:** hitung manual dengan rumus di bawah, tunjukkan tiap bulan, dan beri tahu bahwa hasil dihitung manual.
6. Periksa checklist.

## Rumus (untuk hitung manual)
Dasar: PP 55/2022 jo. PP 20/2026; berlaku per 2026-09-23. Detail & sumber: `references/regulasi.md`.

Untuk tiap bulan, berurutan:
```
kumulatif_sebelum = omzet tahun ini sebelum bulan ini
kumulatif_sesudah = kumulatif_sebelum + omzet bulan ini

ORANG PRIBADI:
  omzet_kena_pajak = maks(0, kumulatif_sesudah − maks(kumulatif_sebelum, 500.000.000))
BADAN:
  omzet_kena_pajak = omzet bulan ini   (tanpa pembebasan Rp500 juta)

PPh final = 0,5% × omzet_kena_pajak, dibulatkan ke bawah ke rupiah penuh
```
Contoh orang pribadi: kumulatif sampai Mei Rp455 juta, omzet Juni Rp90 juta → kumulatif Rp545 juta → kena pajak Rp545 jt − Rp500 jt = Rp45 juta → PPh Juni = Rp225.000. Juli omzet Rp70 juta → seluruhnya kena → Rp350.000.

Batas setor yang ditampilkan: tanggal 15 bulan berikutnya (PMK 81/2024 Pasal 94). Bila jatuh Sabtu/Minggu/libur nasional/cuti bersama → hari kerja berikutnya (Pasal 100 ayat (1)); data libur 2026–2027 di `references/libur-nasional-<tahun>.csv`.
Jangka waktu tarif 0,5% (PP 55/2022 Pasal 59): orang pribadi 7 tahun pajak; koperasi, CV, firma, PT perorangan 4; PT 3 — dihitung sejak tahun terdaftar (terdaftar sebelum 2018 → sejak 2018). Status setelah PP 20/2026 belum diverifikasi.

## Format output
```
## PPh Final UMKM 0,5% - Tahun <tahun> (<Orang pribadi/Badan>)

| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
...
**Ringkasan** (omzet kumulatif, total PPh, sisa omzet bebas pajak, sisa ruang sebelum Rp4,8 M)
**Catatan penting** (dari script)
_Dasar aturan + berlaku per + disclaimer_
```

## Contoh
**Input pengguna:** "Saya jualan online pribadi. Omzet Jan 45jt, Feb 60jt, Mar 80jt, Apr 120jt, Mei 150jt, Jun 90jt, Jul 70jt. Juli dipotong PPh 22 Shopee 350 ribu. Pajak saya berapa?"

**Perintah:** `python3 <folder-skill-ini>/scripts/pph_final.py --jenis op --tahun 2026 --omzet 45jt 60jt 80jt 120jt 150jt 90jt 70jt --pph22 0 0 0 0 0 0 350rb`

**Output (dipersingkat):**
```
| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
| Mei | Rp 150.000.000 | Rp 455.000.000 | Rp 0 | Rp 0 | - | 2026-06-15 | masih dalam Rp500 juta bebas |
| Juni | Rp 90.000.000 | Rp 545.000.000 | Rp 45.000.000 | Rp 225.000 | - | 2026-07-15 | melewati Rp500 juta; hanya Rp 45.000.000 yang kena pajak |
| Juli | Rp 70.000.000 | Rp 615.000.000 | Rp 70.000.000 | Rp 350.000 | Rp 350.000 | 2026-08-15 (libur -> 2026-08-18) | - |
| **Total** | **Rp 615.000.000** | | | **Rp 575.000** | Rp 350.000 | | |

Juni adalah bulan pertama Anda kena pajak: hanya bagian di atas Rp500 juta (Rp45 juta) yang dihitung.
PPh 22 Rp350.000 yang dipotong Shopee dicatat terpisah; angka PPh final BELUM dikurangi PPh 22 — tanyakan ke DJP/konsultan cara memperhitungkannya.
```

## Checklist sebelum mengirim hasil
- [ ] Jenis WP benar (orang pribadi vs badan) dan asumsinya disebut.
- [ ] Omzet kumulatif memperhitungkan bulan-bulan sebelumnya di tahun yang sama.
- [ ] Bulan saat melewati Rp500 juta hanya menghitung selisihnya.
- [ ] PPh 22 marketplace hanya dicatat, **tidak** dikurangkan otomatis, dan diberi catatan cek DJP/konsultan.
- [ ] Hal yang belum terverifikasi (masa transisi CV/firma/PT, perubahan batas jangka waktu oleh PP 20/2026) **tidak** dinyatakan pasti, tetapi batas jangka waktu menurut PP 55/2022 tetap **disebut** (dengan tahun akhirnya bila tahun terdaftar diketahui).
- [ ] Batas setor yang jatuh di hari libur disebut beserta tanggal hari kerja berikutnya.
- [ ] Peringatan Rp4,8 miliar muncul bila relevan.
- [ ] Disclaimer + dasar aturan + tanggal berlaku ada.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` untuk omzet bukan angka/negatif, bulan ganda, bulan di luar 1–12, lebih dari 12 bulan, atau file tanpa kolom `bulan`/`omzet`. Jelaskan dengan bahasa sederhana dan minta data yang benar.
- Omzet negatif dari baris CLI (`-5jt`) dibaca sebagai opsi dan ditolak; minta angka positif.
- CV, firma, dan PT biasa dikeluarkan dari skema 0,5% oleh PP 20/2026 dengan masa transisi yang **belum terverifikasi** → hasil untuk mereka hanya simulasi; wajib arahkan cek DJP.
- Pasangan suami-istri, usaha dengan beberapa NPWP/NITKU, atau tahun pertama terdaftar bisa punya perlakuan khusus → arahkan ke konsultan/DJP.
- Jangan menyatakan PPh 22 marketplace pasti bisa dikreditkan/mengurangi PPh final.
