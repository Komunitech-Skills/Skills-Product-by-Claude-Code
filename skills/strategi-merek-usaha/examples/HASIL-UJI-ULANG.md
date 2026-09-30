
## Uji ulang 1.0.1 (2026-09-30)

**Penguji:** agent independen. Skill disalin ke scratchpad; tidak ada file lain diubah, tanpa commit.

| Temuan lama | Hasil (input baru) |
|---|---|
| S1 format angka | Diperbaiki. `38.000`, `Rp1.250.000`, `45rb`, `2,5jt`, `38.000,50`, bonus `Tas=1.500` terbaca benar; `38.5`, `38,000`, `1..000`, bonus `1.5` ditolak (kode 2). Harga < Rp1.000 diberi PERINGATAN. Laba dihitung ulang tangan: Rp85.000/diskon 15%/platform 8,5%/refund 3% = Rp27.191; Rp125.000/10%/6,5%/2% = Rp36.937 (cocok, pembulatan half-up) |
| S2 kelas Nice 5/37/44 | Benar (WIPO/USPTO); edisi ke-13 versi 2026 berlaku 1 Jan 2026 terkonfirmasi |
| R1 nama tanpa huruf | Diperbaiki ("2.5", "12345" ditolak) |
| R2 Pasal 17 | Benar: subjek pelaku usaha periklanan (teks ayat 1-2 dicek). Catatan kecil: huruf e (memanfaatkan peristiwa/orang tanpa izin) dan f (melanggar etika periklanan) tidak disebut |
| R3 kata generik | Diperbaiki: merek "Kopi"/"Warung" tak lagi menandai; "Kopi Kenangan" tetap menandai "Kenangan"; `--tanpa-generik` berfungsi |
| R4 "eu" | Diperbaiki (Seulas=2, Keukeuh=2, "Pak Eu" benar) |

`tests/uji_regresi.py`: 25 tes OK. `validate.py --skill`: lolos. Skenario end-to-end (nama kopi + merek pembanding + penawaran): benar. Regresi: tidak ada. Sisa minor: R5-R7 belum disentuh (titik desimal margin, peringatan RUGI hanya di teks, bukan JSON; `--generik` duplikat "kedai" di JSON).

**Skor: 9/10** - semua temuan sedang/rendah yang diklaim diperbaiki terverifikasi.
