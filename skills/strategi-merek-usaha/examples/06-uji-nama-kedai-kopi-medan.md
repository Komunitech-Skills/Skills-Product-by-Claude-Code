# Uji 06 (normal 1): Nama kedai kopi di Medan

> Uji independen 2026-09-30 oleh penguji (bukan pembuat). Agent mengikuti SKILL.md Bagian A. Angka script dijalankan sungguhan dan diverifikasi ulang dengan implementasi penguji sendiri (hasil 10/10 sama).

**Input pengguna:** "Kasih nama buat kedai kopi saya di Medan, dekat kampus USU. Pembeli mahasiswa dan pekerja muda, harga Rp15-25 ribu. Pesaing yang saya tahu: Kopi Kenangan, Janji Jiwa, Kopi Kok Tong, Fore Coffee, Tomoro, Kopi Kita."

## Ringkasan (mode lengkap)
Kedai kopi harga mahasiswa di Padang Bulan/USU, Medan; kesan akrab dan bangga lokal Sumatera Utara.

**Asumsi:** gaya ramah, boleh unsur Batak/Melayu Deli, 2-4 suku kata, tanpa bahasa Inggris. Nilai `aman_makna`, `khas`, `relevan` = pendapat agent, bukan fakta.

## 10 opsi + alasan
| Nama | Alasan singkat |
|---|---|
| Kopi Horas | "Horas" salam khas Batak, langsung terasa Medan; tapi sangat banyak dipakai (khas rendah) |
| Kedai Tongkrong | Menggambarkan tempat nongkrong mahasiswa |
| Kopi Kesawan | Kesawan = kawasan kota lama Medan yang dikenal |
| Toba Seduh | Kopi + Danau Toba, citra Sumatera Utara |
| Kopi Sipirok | Sipirok = daerah penghasil kopi di Tapanuli Selatan |
| Seduh Deli | Deli = identitas Melayu Deli/Medan |
| Kopi Kita Medan | Dibuat sengaja mirip untuk uji; akan ditandai |
| Kopi Kenangan Medan | Opsi uji: menempel merek besar; akan ditandai |
| Lapo Kopi | "Lapo" akrab di Medan; **perlu ditanyakan ke penutur asli** karena lapo sering dikaitkan dengan lapo tuak (minuman beralkohol) |
| Ngopi Kuy | Gaul, tapi generik |

## Hasil script
`python3 scripts/skor_nama.py kopi.csv --merek "Kopi Kenangan, Janji Jiwa, Kopi Kok Tong, Fore Coffee, Tomoro, Kopi Kita"`
```
 #  Nama                      Skor  Huruf Suku  Status / catatan
 1  Seduh Deli                90.0      9    4  layak dicek
 2  Toba Seduh                90.0      9    4  layak dicek
 3  Kedai Tongkrong           83.0     14    4  layak dicek
 4  Kopi Horas                79.0      9    4  layak dicek
 5  Kopi Sipirok              79.0     11    5  layak dicek
 6  Lapo Kopi                 77.0      8    4  layak dicek
 7  Ngopi Kuy                 77.0      8    3  layak dicek
 8  Kopi Kesawan              76.0     11    5  layak dicek
 9  Kopi Kenangan Medan       56.0     17    7  TANDAI: terlalu mirip 'Kopi Kenangan'
10  Kopi Kita Medan           55.0     13    6  TANDAI: terlalu mirip 'Kopi Kita'
SETARA: 'Seduh Deli' dan 'Toba Seduh' selisih <= 5 poin.
```
Verifikasi tangan "Seduh Deli": (10x4 + 10x4 + 10x5 + 20x5 + 20x5 + 15x4 + 15x4) / 100 x 20 = 450/100 x 20 = **90,0** (cocok).

## 3 teratas
1. **Seduh Deli** (90) dan **Toba Seduh** (90): SETARA, putuskan lewat uji ucap 5 orang + cek ketersediaan. "Toba" sangat sering dipakai usaha lain di Sumut, kemungkinan banyak yang mirip di PDKI.
2. **Kedai Tongkrong** (83): panjang (14 huruf), tapi paling jelas "tempat nongkrong".
Nama yang ditandai (Kopi Kenangan Medan, Kopi Kita Medan) **tidak** direkomendasikan.

## Daftar cek (semua "belum dicek")
| Nama | Domain .id/.com | IG/TikTok | GrabFood/GoFood/Google Maps | PDKI kelas 30 (kopi) & 43 (kafe) |
|---|---|---|---|---|
| Seduh Deli | belum dicek | belum dicek | belum dicek | belum dicek |
| Toba Seduh | belum dicek | belum dicek | belum dicek | belum dicek |
| Kedai Tongkrong | belum dicek | belum dicek | belum dicek | belum dicek |

Cek PDKI: pdki-indonesia.dgip.go.id -> Merek -> cari nama persis + varian ("Seduh Deli", "Sedu Deli", "Seduhdeli"), lihat kelas 30 dan 43.

**Yang perlu kamu cek sendiri:** arti "Lapo" bagi pembeli sasaran; uji ucap 5 orang; domain/handle/PDKI.
**Disclaimer:** skor = alat bantu, bukan bukti nama tersedia atau aman secara hukum. Keputusan pendaftaran merek ada di DJKI/konsultan KI.

Mau saya buatkan tagline dan bio dari nama pilihanmu?

## Penilaian penguji
- Alur A1-A7 diikuti; 10 opsi, alasan per opsi, penanda "perlu penutur asli" untuk kata daerah, TANDAI bekerja, SETARA muncul, status "belum dicek" dipertahankan.
- Catatan: tabel kelas Nice di `references/cek-merek-pdki.md` memuat kelas 30 dan 43 dengan benar untuk kasus ini.
- Kekurangan kecil: script menilai "Kopi Horas" khas=2 hanya dari nilai manual; kemiripan ejaan tidak menangkap bahwa "Horas" sangat umum (sesuai batasan yang ditulis).
