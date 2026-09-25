# Uji 03 — Mode Hitung: kontraktor, PKWT 12 bulan + perpanjangan 6 bulan, diputus di bulan ke-15

> Penguji independen, 25 September 2026.

## Input pengguna
> "Saya kontraktor di Bekasi. Tukang las saya kontrak 12 bulan mulai 1 Januari 2026, terus diperpanjang 6 bulan (1 Januari–30 Juni 2027). Proyeknya dibatalkan klien, jadi saya putus dia di bulan ke-15, terakhir kerja 31 Maret 2027. Gajinya 4,5 juta + tunjangan tetap 500 ribu, plus uang makan 25 ribu per hari masuk. Saya harus bayar berapa?"

## Proses agent
- Mode **Hitung**. "Bulan ke-15" dari 1 Jan 2026 = Maret 2027; pengguna menyebut hari kerja terakhir 31 Maret 2027 → dipakai sebagai `--berhenti`.
- Uang makan harian **tidak** masuk upah dasar (SKILL.md Rumus no. 1: tergantung kehadiran).
- Pengakhiran oleh **pengusaha** (proyek dibatalkan klien bukan alasan Pasal 61 ayat (1), kecuali tercantum sebagai "keadaan tertentu" di PKWT → agent menanyakan hal ini dalam catatan).

```bash
python3 scripts/hitung_pkwt.py --periode "1 Januari 2026 s.d. 31 Desember 2026" --periode "1 Januari 2027 s.d. 30 Juni 2027" \
  --gaji-pokok 4,5jt --tunjangan-tetap 500rb --berhenti "31 Maret 2027" --pihak-mengakhiri pengusaha
```
Output apa adanya:
```
HITUNG KOMPENSASI AKHIR PKWT
Upah 1 bulan : Rp5.000.000 (gaji pokok Rp4.500.000 + tunjangan tetap Rp500.000)
Total PKWT   : 1 Januari 2026 s.d. 30 Juni 2027 = 18 bulan (batas 5 tahun: s.d. 31 Desember 2030) OK

| Periode | Kontrak | Dijalani | Masa kerja | Bulan | Rumus | Kompensasi |
|---|---|---|---|---|---|---|
| 1 | 1 Januari 2026 s.d. 31 Desember 2026 | s.d. 31 Desember 2026 | 12 bulan | 12 | 12 bulan: 1 x upah = Rp5.000.000 | Rp5.000.000 |
| 2 | 1 Januari 2027 s.d. 30 Juni 2027 | s.d. 31 Maret 2027 | 3 bulan | 3 | 3 / 12 x Rp5.000.000 = Rp1.250.000 | Rp1.250.000 |

TOTAL KOMPENSASI (dibayar pengusaha ke pekerja): Rp6.250.000

GANTI RUGI PENGAKHIRAN DINI (UU 13/2003 Pasal 62): Rp15.000.000
  Sisa kontrak 1 April 2027 s.d. 30 Juni 2027 = 3 bulan -> 3 bulan x Rp5.000.000 = Rp15.000.000
  Arah: pengusaha membayar ke pekerja
  Catatan: Tidak berlaku bila berakhir karena pekerja meninggal, putusan pengadilan, selesainya pekerjaan (PKWT berdasarkan selesainya pekerjaan), atau keadaan yang tercantum di PK/PP/PKB (UU 13/2003 Pasal 61 & 62). Sisa hari dihitung pecahan bulan.

Cara hitung bulan: tanggal mulai & akhir ikut dihitung; masa kerja = bulan penuh + sisa hari (metode pecahan). Rupiah dibulatkan ke rupiah terdekat.

Bukan nasihat hukum. Dasar: PP 35/2021 Pasal 15-17, UU 13/2003 Pasal 62 jo. UU 6/2023, Putusan MK 168/PUU-XXI/2023 (dicek 25 September 2026). Konfirmasi ke Disnaker/konsultan hukum.
```

## Output agent

**Yang perlu Bapak bayar ke tukang las:**

| Komponen | Jumlah | Kapan | Dasar |
|---|---|---|---|
| Kompensasi kontrak pertama (12 bulan) — **seharusnya sudah dibayar 31 Desember 2026**; bila belum, masih terutang | Rp5.000.000 | 31 Des 2026 | PP 35/2021 Pasal 15 ayat (4) & 16 |
| Kompensasi perpanjangan (3 bulan dijalani, 1 Jan–31 Mar 2027) | Rp1.250.000 | saat berhenti | PP 35/2021 Pasal 17 |
| Ganti rugi sisa kontrak (1 Apr–30 Jun 2027 = 3 bulan × Rp5.000.000) | Rp15.000.000 | saat berhenti | UU 13/2003 Pasal 62 |
| **Total bila kompensasi pertama sudah dibayar** | **Rp16.250.000** | | |
| Total bila belum sama sekali | Rp21.250.000 | | |
| Upah Maret 2027 & uang makan hari masuk yang belum dibayar, THR bila jatuh tempo | cek terpisah | | — |

Penjelasan singkat: upah dasar = gaji pokok + tunjangan tetap = Rp5.000.000; uang makan harian tidak ikut karena bergantung kehadiran. Karena Bapak yang mengakhiri sebelum 30 Juni 2027, Bapak membayar ganti rugi sebesar upah sisa kontrak. Pembatalan proyek oleh klien **tidak** otomatis membebaskan ganti rugi, kecuali "berakhirnya proyek karena dibatalkan pemberi kerja" tercantum sebagai keadaan tertentu di kontrak/peraturan perusahaan, atau kontraknya berbasis selesainya pekerjaan. Mohon cek bunyi kontraknya. Kalau ada klausul seperti itu, hubungi Disnaker Kabupaten/Kota Bekasi sebelum membayar.

Cara hitung bulan: tanggal mulai & akhir ikut dihitung (asumsi skill; aturan tidak merinci).

Disclaimer: Draf/hasil ini bantuan administrasi, bukan nasihat hukum. Dasar: UU 13/2003 sebagaimana diubah UU 6/2023, PP 35/2021, dan Putusan MK 168/PUU-XXI/2023 (dicek 25 September 2026). MK memerintahkan UU Ketenagakerjaan baru paling lambat Oktober 2026; per tanggal cek, RUU Pelindungan Ketenagakerjaan belum disahkan, sehingga aturan PKWT bisa berubah. Sebelum ditandatangani, konsultasikan ke Disnaker setempat atau konsultan hukum ketenagakerjaan.

## Verifikasi independen (Fraction, manual)
| Komponen | Hitung manual | Script | Cocok |
|---|---|---|---|
| Upah dasar | 4.500.000 + 500.000 = 5.000.000 (uang makan dikecualikan) | 5.000.000 | ✅ |
| Periode 1 | 1 Jan–31 Des 2026 = 12 bulan → 1 × 5.000.000 | 5.000.000 | ✅ |
| Periode 2 dijalani | 1 Jan–31 Mar 2027 = 3 bulan → Fraction(3,12) × 5.000.000 = 1.250.000 | 1.250.000 | ✅ |
| Ganti rugi | 1 Apr–30 Jun 2027 = 3 bulan → 3 × 5.000.000 = 15.000.000 | 15.000.000 | ✅ |
| Cek jumlah | dijalani 3 + sisa 3 = 6 bulan = panjang perpanjangan ✅ | | ✅ |

Perlakuan perpanjangan: kompensasi periode 1 dihitung **terpisah** dan disebut "dibayar saat periode sebelum perpanjangan selesai" (PP 35/2021 Pasal 15 ayat (4)) ✅.

### Varian tengah bulan (uji tambahan): berhenti 15 Maret 2027
Script: dijalani 2 bulan 15 hari = 2 + 15/31 = 2,4839 → **Rp1.034.946**; sisa 16 Mar–30 Jun = 3 bulan 15 hari, 15/30 → 3,5 bulan → **Rp17.500.000**.
Manual: kompensasi 2,483871 × 5.000.000 / 12 = 1.034.946,24 → Rp1.034.946 ✅.
Catatan: dijalani 2,4839 + sisa 3,5 = **5,9839 bulan ≠ 6 bulan** kontrak. Cara kalender (16–31 Mar = 16/31 + Apr + Mei + Jun) memberi sisa 3,5161 bulan = **Rp17.580.645** (selisih Rp80.645, merugikan pekerja). Lihat HASIL-UJI temuan S1.

## Penilaian
Lulus untuk skenario utama: angka tepat, arah pembayaran jelas, uang makan dikecualikan dengan alasan, disclaimer ada. Temuan: pecahan sisa hari ganti rugi tidak konsisten dengan pecahan masa dijalani (varian tengah bulan).
