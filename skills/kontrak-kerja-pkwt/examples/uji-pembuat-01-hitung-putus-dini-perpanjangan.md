# Uji Pembuat 01 — Kontrak diperpanjang lalu diputus lebih cepat (mode Hitung + Periksa singkat)

> Uji oleh **pembuat skill** (bukan uji independen Tahap 6). Tanggal: 25 September 2026.
> Tujuan: memastikan script, rumus manual, dan format jawaban konsisten.

## Input pengguna
> "Saya punya toko bangunan di Sidoarjo. Andi admin gudang proyek renovasi cabang, kontrak pertama 1 Februari 2025 – 31 Januari 2026, lalu diperpanjang 1 Feb – 31 Juli 2026. Gaji pokok Rp3.200.000 + tunjangan jabatan tetap 400rb. Proyeknya saya hentikan, Andi terakhir kerja 20 Mei 2026. Saya harus bayar apa aja? Di kontraknya ada tulisan 'bila perusahaan mengakhiri kontrak lebih awal, pekerja tidak berhak menuntut apa pun'. UMK saya isi 3,5 juta ya (nanti saya cek lagi)."

## Perintah script
```bash
python3 scripts/hitung_pkwt.py --periode "1 Februari 2025 s.d. 31 Januari 2026" \
  --periode "01/02/2026 s.d. 31/07/2026" --gaji-pokok "Rp3.200.000" --tunjangan-tetap 400rb \
  --berhenti "20 Mei 2026" --pihak-mengakhiri pengusaha --upah-minimum "Rp3.500.000"
```

## Output script (apa adanya)
```
HITUNG KOMPENSASI AKHIR PKWT
Upah 1 bulan : Rp3.600.000 (gaji pokok Rp3.200.000 + tunjangan tetap Rp400.000)
Total PKWT   : 1 Februari 2025 s.d. 31 Juli 2026 = 18 bulan (batas 5 tahun: s.d. 31 Januari 2030) OK

| Periode | Kontrak | Dijalani | Masa kerja | Bulan | Rumus | Kompensasi |
|---|---|---|---|---|---|---|
| 1 | 1 Februari 2025 s.d. 31 Januari 2026 | s.d. 31 Januari 2026 | 12 bulan | 12 | 12 bulan: 1 x upah = Rp3.600.000 | Rp3.600.000 |
| 2 | 1 Februari 2026 s.d. 31 Juli 2026 | s.d. 20 Mei 2026 | 3 bulan 20 hari | 3,6452 | 3,6452 / 12 x Rp3.600.000 = Rp1.093.548 | Rp1.093.548 |

TOTAL KOMPENSASI (dibayar pengusaha ke pekerja): Rp4.693.548

GANTI RUGI PENGAKHIRAN DINI (UU 13/2003 Pasal 62): Rp8.477.419
  Sisa kontrak 21 Mei 2026 s.d. 31 Juli 2026 = 2 bulan 11 hari -> 2,3548 bulan x Rp3.600.000 = Rp8.477.419
  Arah: pengusaha membayar ke pekerja
```

## Verifikasi manual (pembuat)
- Periode 2: 1 Feb → 1 Mei 2026 = 3 bulan penuh; 1–20 Mei = 20 hari; bulan berjalan 1 Mei–31 Mei = 31 hari → 3 + 20/31 = 3,645161. × 3.600.000 ÷ 12 = 1.093.548,39 → **Rp1.093.548** ✅
- Sisa: 21 Mei → 21 Juli = 2 bulan; 21–31 Juli = 11 hari; bulan berjalan 21 Jul–20 Agu = 31 hari → 2,354839 × 3.600.000 = 8.477.419,35 → **Rp8.477.419** ✅
- Kompensasi periode 1 (Rp3.600.000) seharusnya sudah dibayar saat 31 Januari 2026. Jika belum, masih terutang.

## Jawaban agent (ringkas, format yang diharapkan)
**Yang perlu Bapak bayar ke Andi:**
| Komponen | Jumlah | Dasar |
|---|---|---|
| Kompensasi kontrak pertama (12 bulan), bila belum dibayar 31 Jan 2026 | Rp3.600.000 | PP 35/2021 Pasal 15–16 |
| Kompensasi perpanjangan (3 bulan 20 hari dijalani) | Rp1.093.548 | PP 35/2021 Pasal 17 |
| Ganti rugi sisa kontrak 21 Mei – 31 Juli 2026 | Rp8.477.419 | UU 13/2003 Pasal 62 |
| Upah Mei yang belum dibayar & THR bila jatuh tempo | cek terpisah | — |

**Temuan periksa kontrak:**
| Kalimat di kontrak | Risiko | Alasan | Usulan pengganti |
|---|---|---|---|
| "bila perusahaan mengakhiri kontrak lebih awal, pekerja tidak berhak menuntut apa pun" | 🔴 | Bertentangan dengan Pasal 62 UU 13/2003 dan Pasal 17 PP 35/2021. Klausul yang melepas hak minimum pekerja berisiko tidak berlaku. | "Pihak yang mengakhiri perjanjian sebelum jangka waktu berakhir wajib membayar ganti rugi sebesar upah sampai batas waktu berakhirnya perjanjian, dan PIHAK PERTAMA tetap memberikan uang kompensasi atas masa kerja yang telah dijalani." |
| "admin gudang proyek renovasi cabang" | 🟢 | Alasan waktu tertentu (proyek) jelas. Pastikan tercantum di pasal jabatan. | — |

**Catatan:** Cara hitung "bulan" memakai asumsi skill (tanggal mulai & akhir ikut dihitung; sisa hari sebagai pecahan bulan). Upah Rp3.600.000 ≥ UMK yang Bapak isi (Rp3.500.000); pastikan angka UMK Sidoarjo 2026 di situs Disnaker.

Disclaimer: bukan nasihat hukum; dasar UU 13/2003 jo. UU 6/2023, PP 35/2021, Putusan MK 168/PUU-XXI/2023 (dicek 25 September 2026). RUU Pelindungan Ketenagakerjaan belum disahkan per tanggal cek. Untuk kesepakatan pengakhiran, konsultasikan ke Disnaker Sidoarjo atau konsultan hukum ketenagakerjaan.

## Hasil
- Script: angka cocok dengan hitungan manual.
- Tes regresi `python3 tests/uji_regresi.py`: **LULUS semua 98 cek** (25 September 2026).
- Catatan untuk penguji independen: uji juga mode Susun (masa percobaan diminta pengguna), mode Periksa draf bahasa Inggris saja, dan permintaan PHK karyawan tetap (di luar cakupan).
