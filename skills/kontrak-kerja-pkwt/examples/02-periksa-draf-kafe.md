# Uji 02 — Mode Periksa: draf PKWT buatan sendiri pemilik kafe

> Penguji independen, 25 September 2026. Mengikuti SKILL.md mode Periksa + `references/checklist-periksa.md` + script.

## Input pengguna
> "Ini kontrak yang saya bikin sendiri buat barista kafe saya di Yogyakarta. Tolong cek aman nggak ya sebelum ditandatangani."
>
> *(draf ditempel)*
> **SURAT KONTRAK KERJA** — Kopi Senja, Jl. Kaliurang km 5, Sleman. Pekerja: [nama], barista.
> Pasal 1. Pekerja bekerja sebagai barista di Kopi Senja.
> Pasal 2. Kontrak berlaku 2 (dua) tahun mulai 1 November 2026, dan dapat diperpanjang 2 (dua) kali masing-masing 2 (dua) tahun.
> Pasal 3. Tiga bulan pertama adalah **masa percobaan**. Selama masa percobaan perusahaan dapat memutus hubungan kerja sewaktu-waktu tanpa kompensasi apa pun.
> Pasal 4. Gaji pokok Rp2.800.000 + tunjangan tetap Rp200.000 per bulan, dibayar tanggal 1.
> Pasal 5. Upah sudah termasuk semua tunjangan. **Perusahaan tidak menanggung BPJS**; pekerja mengurus sendiri.
> Pasal 6. Apabila pekerja **mengundurkan diri sebelum kontrak selesai, pekerja wajib membayar denda Rp10.000.000** dan gaji bulan terakhir tidak dibayarkan.
> Pasal 7. Kerja 6 hari seminggu, jam 10.00–22.00, istirahat 1 jam.
> Pasal 8. Hal lain diatur kemudian.
> Ditandatangani pemilik dan pekerja.

## Script
```bash
python3 scripts/hitung_pkwt.py --periode "1 November 2026 s.d. 31 Oktober 2028" --periode "1 November 2028 s.d. 31 Oktober 2030" \
  --periode "1 November 2030 s.d. 31 Oktober 2032" --gaji-pokok 2,8jt --tunjangan-tetap 200rb
```
```
Upah 1 bulan : Rp3.000.000 (gaji pokok Rp2.800.000 + tunjangan tetap Rp200.000)
Total PKWT   : 1 November 2026 s.d. 31 Oktober 2032 = 72 bulan (batas 5 tahun: s.d. 31 Oktober 2031) MELEBIHI
| 1 | 1 November 2026 s.d. 31 Oktober 2028 | ... | 24 bulan | 24 | 24 / 12 x Rp3.000.000 = Rp6.000.000 | Rp6.000.000 |
| 2 | 1 November 2028 s.d. 31 Oktober 2030 | ... | 24 bulan | 24 | ... | Rp6.000.000 |
| 3 | 1 November 2030 s.d. 31 Oktober 2032 | ... | 24 bulan | 24 | ... | Rp6.000.000 |
TOTAL KOMPENSASI (dibayar pengusaha ke pekerja): Rp18.000.000
PERINGATAN: MELEBIHI BATAS: total PKWT termasuk perpanjangan 72 bulan ... Paling lambat berakhir 31 Oktober 2031 ...
```

## Output agent

HASIL PERIKSA DRAF PKWT — Barista Kopi Senja
Ringkasan: **8 🔴 tinggi · 4 🟠 sedang · 2 🟢 rendah → Konsultasikan dulu** (ada 🔴 yang tidak cukup diperbaiki dengan menulis ulang klausul: barista kafe umumnya pekerjaan tetap, dan rencana total 6 tahun).

| # | Pasal di draf | Temuan | Risiko | Dasar | Usulan perbaikan (siap tempel) |
|---|---|---|---|---|---|
| 1 | Pasal 3 "Tiga bulan pertama adalah masa percobaan ... memutus sewaktu-waktu tanpa kompensasi" | Masa percobaan di PKWT | 🔴 | UU 13/2003 Pasal 58 jo. UU 6/2023; PP 35/2021 Pasal 12: batal demi hukum, masa kerja tetap dihitung | Hapus Pasal 3, ganti: "Perjanjian ini tidak mensyaratkan masa percobaan kerja." Bila ingin menilai dulu, gunakan karyawan tetap (PKWTT) dengan masa percobaan maks. 3 bulan. |
| 2 | Pasal 1 "barista di Kopi Senja" (tanpa alasan waktu tertentu) | Pekerjaan bersifat tetap dikontrak PKWT | 🔴 | UU 13/2003 Pasal 59 ayat (1)–(3) jo. UU 6/2023; PP 35/2021 Pasal 4–5 | Jika ada alasan sementara yang jujur (mis. cabang baru uji coba), tulis: "Pekerjaan ini bersifat tidak tetap karena [alasan]." Jika barista adalah posisi tetap kafe → gunakan PKWTT. |
| 3 | Pasal 2 "2 tahun ... diperpanjang 2 kali masing-masing 2 tahun" | Total 6 tahun (72 bulan) > 5 tahun; batas akhir 31 Oktober 2031 | 🔴 | PP 35/2021 Pasal 8; Putusan MK 168/PUU-XXI/2023 | "Perjanjian ini berlaku 24 bulan, 1 November 2026 s.d. 31 Oktober 2028, dan dapat diperpanjang dengan kesepakatan tertulis dengan total seluruh PKWT tidak melebihi 5 (lima) tahun." |
| 4 | Pasal 5 "Perusahaan tidak menanggung BPJS" | Tanpa BPJS TK & Kesehatan | 🔴 | UU 24/2011 Pasal 15 | "PIHAK PERTAMA mendaftarkan PIHAK KEDUA sebagai peserta BPJS Ketenagakerjaan dan BPJS Kesehatan dengan iuran sesuai porsi yang ditentukan peraturan." |
| 5 | Pasal 6 "denda Rp10.000.000" | Penalti berlebihan (Rp10 jt ≈ 3,3× upah) dan bukan ganti rugi Pasal 62 | 🔴 | UU 13/2003 Pasal 62; checklist C1 | "Pihak yang mengakhiri perjanjian sebelum jangka waktu berakhir wajib membayar ganti rugi kepada pihak lainnya sebesar upah PIHAK KEDUA sampai batas waktu berakhirnya jangka waktu perjanjian." |
| 6 | Pasal 6 "gaji bulan terakhir tidak dibayarkan" | Upah yang sudah dikerjakan ditahan | 🔴 | Upah atas pekerjaan yang sudah dilakukan wajib dibayar; checklist C1 | Hapus. |
| 7 | Tidak ada pasal kompensasi; Pasal 3 "tanpa kompensasi apa pun" | Tanpa uang kompensasi akhir PKWT | 🔴 | UU 13/2003 Pasal 61A jo. UU 6/2023; PP 35/2021 Pasal 15–17 | "Saat perjanjian berakhir, PIHAK PERTAMA memberikan uang kompensasi sebesar masa kerja (bulan) ÷ 12 × 1 bulan upah (gaji pokok + tunjangan tetap). Perkiraan untuk 24 bulan: Rp6.000.000 (enam juta rupiah)." |
| 8 | Pasal 3 "memutus sewaktu-waktu tanpa kompensasi" | Pengusaha boleh memutus kapan saja tanpa ganti rugi | 🔴 | UU 13/2003 Pasal 62; PP 35/2021 Pasal 17 | Ganti dengan klausul ganti rugi dua arah (lihat no. 5) + kompensasi atas masa yang dijalani. |
| 9 | Pasal 7 "6 hari, 10.00–22.00, istirahat 1 jam" | 11 jam/hari × 6 = 66 jam/minggu, jauh > 40 jam, tanpa lembur | 🟠 | UU 13/2003 Pasal 77 jo. UU 6/2023; PP 35/2021 Pasal 21 & 26 | "Waktu kerja 40 jam seminggu untuk 6 hari kerja, dengan pembagian shift [isi]. Kerja lembur dengan persetujuan pekerja, maks. 4 jam/hari & 18 jam/minggu, upah lembur sesuai peraturan." |
| 10 | Pasal 4 upah Rp3.000.000 | UMK Kabupaten Sleman 2026 belum diketahui | 🟠 (🔴 bila di bawah UMK) | UU 13/2003 Pasal 88E & 185 jo. UU 6/2023 | Isi: "Upah tidak lebih rendah dari UMK Kabupaten Sleman 2026 sebesar Rp[isi: cek situs Disnaker]." |
| 11 | Tidak ada THR, cuti | Hak normatif tidak disebut | 🟠 | Permenaker 6/2016; UU 13/2003 Pasal 79 | Tambah pasal THR (masa kerja ≥ 1 bulan) dan cuti tahunan 12 hari setelah 12 bulan. |
| 12 | Kop "Jl. Kaliurang km 5, Sleman" vs "kafe saya di Yogyakarta"; identitas pekerja kosong; tidak ada tempat/tanggal dibuat | Isi minimal tidak lengkap | 🟠 | PP 35/2021 Pasal 13 | Lengkapi identitas, jenis usaha, tempat & tanggal dibuat; pastikan kabupaten/kota tempat kerja benar (menentukan UMK). |
| 13 | Tidak ada rencana pencatatan | — | 🟢→🟠 | PP 35/2021 Pasal 14 | "Perjanjian ini dicatatkan PIHAK PERTAMA ke instansi ketenagakerjaan paling lambat 3 hari kerja setelah ditandatangani." |
| 14 | Judul "Surat Kontrak Kerja"; rangkap & meterai tidak disebut | Kerapian | 🟢 | UU 10/2020 (meterai bukan syarat sah) | Judul "Perjanjian Kerja Waktu Tertentu", 2 rangkap asli, bahasa Indonesia & huruf latin. |

Yang sudah baik: tertulis dalam bahasa Indonesia; upah pokok 93% dari upah tetap (≥ 75%); tanggal gajian jelas.
Data yang perlu dicek sendiri: UMK Kabupaten Sleman / Kota Yogyakarta 2026 = [isi]; apakah posisi barista memang sementara.
Hitungan (dari script): rencana total 72 bulan **melebihi** batas 5 tahun (batas akhir 31 Oktober 2031). Kompensasi bila hanya kontrak pertama 24 bulan: **Rp6.000.000** (24/12 × Rp3.000.000), dibayar 31 Oktober 2028. Denda Rp10 juta di draf lebih besar daripada kompensasi yang menjadi hak pekerja selama 2 tahun.

Disclaimer: Draf/hasil ini bantuan administrasi, bukan nasihat hukum. Dasar: UU 13/2003 sebagaimana diubah UU 6/2023, PP 35/2021, dan Putusan MK 168/PUU-XXI/2023 (dicek 25 September 2026). MK memerintahkan UU Ketenagakerjaan baru paling lambat Oktober 2026; per tanggal cek, RUU Pelindungan Ketenagakerjaan belum disahkan, sehingga aturan PKWT bisa berubah. Sebelum ditandatangani, konsultasikan ke Disnaker setempat atau konsultan hukum ketenagakerjaan.

## Verifikasi independen
- 3 × 24 bulan = 72 bulan > 60 ✅; 1 Nov 2026 + 60 bulan − 1 hari = 31 Okt 2031 ✅.
- 24/12 × 3.000.000 = 6.000.000 ✅.
- Semua temuan wajib dari tugas (masa percobaan, denda Rp10 jt, tanpa BPJS, total 6 tahun) terdeteksi 🔴 dengan dasar & kalimat pengganti.

## Penilaian
Lulus. Catatan: jam kerja 66 jam hanya diberi 🟠 oleh checklist (B7); untuk pelanggaran sebesar ini penguji menilai 🔴 lebih tepat. Script menghitung kompensasi periode ke-3 penuh walau sebagian melewati batas 5 tahun (hanya peringatan) — wajar untuk mode Periksa, tetapi angka Rp18 jt jangan disajikan sebagai "hak" tanpa penjelasan (agent tidak menampilkannya).
