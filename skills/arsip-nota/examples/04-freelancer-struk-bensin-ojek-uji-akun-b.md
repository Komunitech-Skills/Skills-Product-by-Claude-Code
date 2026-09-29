# Contoh 4 (uji independen) — Freelancer, struk bensin & ojek

Diuji oleh penguji independen, 26 September 2026, folder sementara terpisah. Data fiktif.

## Skenario
"Arsipkan struk bensin SPBU 45 ribu tanggal 5 September, struk Gojek 22.500 tanggal 6 September buat ojek ke klien, dan struk GrabCar 35rb tanggal 7 September."

## Hasil (dari run aktual)
| File | Vendor | Nominal | Kategori | Asumsi |
|---|---|---|---|---|
| struk-spbu-1.jpg | SPBU Pertamina | Rp 45.000 | **Lain-lain** | Kategori tidak disebut |
| gojek-receipt.png | Gojek | Rp 22.500 | Transportasi | Ditebak dari nama vendor |
| grab-1.jpg | GrabCar | Rp 35.000 | Transportasi | Ditebak dari nama vendor |

Rekap bulan: `total_nominal: 102500`, per kategori Transportasi 2 nota Rp 57.500, Lain-lain 1 nota Rp 45.000.
**Verifikasi independen:** 45000 + 22500 + 35000 = 102.500 — cocok.

## Temuan
- **Struk SPBU tidak tertebak sebagai Transportasi**, meski jelas termasuk bensin. Kata kunci kategori `transportasi` di script hanya berisi `ongkir, kirim, bensin, bbm, tol, parkir, grab, gojek, gocar` — nama vendor nyata di nota biasanya "SPBU Pertamina"/"Shell"/"Pertamina", bukan kata "bensin"/"bbm" itu sendiri. Skenario ini secara eksplisit diminta menguji "struk bensin", dan hasilnya salah kategori (masuk Lain-lain, bukan Transportasi). **Dampak: sedang** — tidak salah data (nominal & tanggal tetap benar), tapi rekap per kategori jadi kurang akurat untuk freelancer yang sering catat BBM. Tidak fatal karena kategori tetap bisa dikoreksi manual dengan `--kategori transportasi`, dan agent (menurut SKILL.md) wajib menyampaikan baris "Asumsi" ke pengguna sehingga bisa dikoreksi saat pratinjau.
- Grab & Gojek (nama aplikasi ojek online, bukan kata "ojek" itu sendiri) berhasil ditebak lewat kata kunci vendor — konsisten.
