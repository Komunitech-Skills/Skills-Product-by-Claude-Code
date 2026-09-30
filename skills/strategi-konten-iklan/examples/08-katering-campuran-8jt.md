# Uji 08 - Normal 3: Katering, Rp8 juta/bulan, campuran awareness + penjualan

Penguji independen, 2026-09-30, simulasi agent mengikuti SKILL.md v1.0.0.

## Permintaan
"Katering nasi kotak & tumpeng di Surabaya. Budget iklan Rp8 juta bulan depan. Saya mau orang kenal dulu (baru buka cabang) tapi juga tetap ada pesanan. Rata-rata pesanan Rp450.000, margin 30%. Pakai IG, TikTok, Google. Minggu 3-4 banyak acara kantor akhir tahun."

## Penanganan tujuan campuran
Script hanya menerima satu `--tujuan`. SKILL.md tidak memberi aturan untuk tujuan campuran. Agent memutuskan sendiri membagi 3jt awareness + 5jt penjualan (asumsi disebut di dokumen) dan menjalankan script dua kali. Pembanding: satu kali `--tujuan penjualan --anggaran 8jt` (lihat bawah).

### Run A - awareness Rp3jt
```
python3 scripts/alokasi_anggaran.py --anggaran 3jt --tujuan awareness --kanal meta,tiktok,google --bobot-minggu 1 1 2 2 --kategori kuliner
```
```
# Rencana Alokasi Anggaran Iklan - Rp3.000.000 / bulan
Tujuan: **awareness** | 4 minggu x 7 hari = 28 hari tayang (sisa hari bulan dipakai evaluasi tanpa menambah anggaran).

## Anggaran per kanal
| Kanal | Anggaran | % | Aman 70% | Uji 30% |
|---|---:|---:|---:|---:|
| Meta (IG/FB) | Rp1.500.000 | 50,0% | Rp1.050.000 | Rp450.000 |
| TikTok Ads | Rp1.500.000 | 50,0% | Rp1.050.000 | Rp450.000 |
| **Total** | **Rp3.000.000** | 100% | | |

## Rencana per minggu
| Kanal | Minggu 1 | Minggu 2 | Minggu 3 | Minggu 4 | Jumlah |
|---|---:|---:|---:|---:|---:|
| Meta (IG/FB) | Rp250.000 | Rp250.000 | Rp500.000 | Rp500.000 | Rp1.500.000 |
| TikTok Ads | Rp250.000 | Rp250.000 | Rp500.000 | Rp500.000 | Rp1.500.000 |
| **Total** | **Rp500.000** | **Rp500.000** | **Rp1.000.000** | **Rp1.000.000** | **Rp3.000.000** |

## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)
| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |
|---|---:|---:|---:|
| Meta (IG/FB) | Rp53.571 | Rp25.000 | 1 |
| TikTok Ads | Rp53.571 | Rp30.000 | 1 |

Kanal tidak dipakai: Google Ads (bagian anggarannya di bawah batas uji).
Sisa pembulatan: Rp0. Total tetap sama dengan anggaran.

## Catatan
- Kategori 'kuliner': cek dulu apakah termasuk kategori terbatas di kebijakan iklan resmi tiap platform.
- Tanpa --aov/--margin: rencana awareness tidak menghitung CPA/ROAS (memang bukan tolok ukurnya).

Angka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.
```
### Run B - penjualan Rp5jt
```
python3 scripts/alokasi_anggaran.py --anggaran 5jt --tujuan penjualan --aov 450rb --margin 30% --kanal meta,tiktok,google --bobot-minggu 1 1 2 2 --kategori kuliner
```
```
# Rencana Alokasi Anggaran Iklan - Rp5.000.000 / bulan
Tujuan: **penjualan** | 4 minggu x 7 hari = 28 hari tayang (sisa hari bulan dipakai evaluasi tanpa menambah anggaran).

## Target dari margin (batas impas, bukan prediksi)
- Harga rata-rata per pesanan: Rp450.000; margin kotor 30% -> laba kotor per pesanan Rp135.000
- **Titik impas ROAS = 1/margin = 3,34x** (di bawah ini iklan merugi); CPA impas Rp135.000
- **Target aman** (sisakan 30% laba kotor): CPA maks Rp94.500, ROAS minimal 4,77x
- Agar anggaran bulan ini sekadar impas dibutuhkan minimal 38 pesanan (= omzet Rp17.100.000); ini syarat impas, BUKAN perkiraan hasil.

## Anggaran per kanal
| Kanal | Anggaran | % | Aman 70% | Uji 30% |
|---|---:|---:|---:|---:|
| Meta (IG/FB) | Rp2.692.307 | 53,8% | Rp1.884.615 | Rp807.692 |
| TikTok Ads | Rp1.538.462 | 30,8% | Rp1.076.923 | Rp461.539 |
| Google Ads | Rp769.231 | 15,4% | Rp538.462 | Rp230.769 |
| **Total** | **Rp5.000.000** | 100% | | |

## Rencana per minggu
| Kanal | Minggu 1 | Minggu 2 | Minggu 3 | Minggu 4 | Jumlah |
|---|---:|---:|---:|---:|---:|
| Meta (IG/FB) | Rp448.718 | Rp448.718 | Rp897.435 | Rp897.436 | Rp2.692.307 |
| TikTok Ads | Rp256.410 | Rp256.410 | Rp512.821 | Rp512.821 | Rp1.538.462 |
| Google Ads | Rp128.205 | Rp128.205 | Rp256.411 | Rp256.410 | Rp769.231 |
| **Total** | **Rp833.333** | **Rp833.333** | **Rp1.666.667** | **Rp1.666.667** | **Rp5.000.000** |

## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)
| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |
|---|---:|---:|---:|
| Meta (IG/FB) | Rp96.154 | Rp25.000 | 2 |
| TikTok Ads | Rp54.945 | Rp30.000 | 1 |
| Google Ads | Rp27.473 | Rp25.000 | 0 - DI BAWAH BATAS (cukup untuk 30 hari tayang 1 iklan) |

Sisa pembulatan: antar kanal -Rp1 (ditambahkan ke Meta (IG/FB)); Meta (IG/FB) antar minggu -Rp1; Google Ads antar minggu Rp1. Total tetap sama dengan anggaran.

## Catatan
- Kategori 'kuliner': cek dulu apakah termasuk kategori terbatas di kebijakan iklan resmi tiap platform.

Angka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.
```
### Pembanding - penjualan penuh Rp8jt (lihat hasil di laporan penguji)
Meta Rp4.307.693 / TikTok Rp2.461.538 / Google Rp1.230.769; 60 pesanan minimal impas; semua kanal >= 1 iklan aktif.

## Gabungan yang disusun agent (dijumlah tangan dari dua keluaran script - penguji memverifikasi)
| Kanal | Awareness | Penjualan | Total |
|---|---:|---:|---:|
| Meta | 1.500.000 | 2.692.307 | 4.192.307 |
| TikTok | 1.500.000 | 1.538.462 | 3.038.462 |
| Google | 0 | 769.231 | 769.231 |
| Total | 3.000.000 | 5.000.000 | 8.000.000 |
Pesanan minimal impas dihitung hanya atas bagian penjualan (38 pesanan untuk Rp5jt); agent menyebut bahwa uang awareness Rp3jt tidak diukur dengan ROAS.

## Pilar konten (5 pilar, ada admin)
Dapur & kebersihan (awareness), menu & porsi asli (pertimbangan), ulasan acara kantor (pertimbangan), jawab keberatan "halal? minimal order? ongkir? bisa DP?" (beli), paket akhir tahun & tumpeng (beli, <=30%). Tiap pilar 5 judul, mis. "Dari jam 3 pagi: cara kami masak 500 kotak", "Isi nasi kotak Rp35rb kami, ditimbang", "Minimal order & area antar Surabaya".

## Verifikasi independen
- Run A: bobot awareness meta 40 / tiktok 40 / google 10; Google 3.000.000 x 10/90 = 333.333 < 700.000 -> dibuang; Meta & TikTok 1.500.000. Per minggu 1:1:2:2 = 250.000/250.000/500.000/500.000. Iklan maks Meta 250.000 // 175.000 = 1, TikTok 250.000 // 210.000 = 1. OK.
- Run B: 5.000.000 x 35/65 = 2.692.307,7 -> 2.692.308; x20/65 = 1.538.461,5 -> 1.538.462; x10/65 = 769.230,8 -> 769.231; jumlah 5.000.001 -> sisa -1 ke Meta = 2.692.307. OK. Pesanan 5.000.000/135.000 = 37,04 -> 38. OK.
- **Temuan (bug konsistensi):** Google Ads Rp769.231 lolos saringan kanal (dicek terhadap total sebulan 28 x 25.000 = 700.000) padahal minggu 1-2 hanya Rp128.205 < 7 x 25.000 = 175.000, sehingga tabel batas uji menulis "0 - DI BAWAH BATAS (cukup untuk 30 hari tayang 1 iklan)". Tidak ada catatan "Anggaran DI BAWAH batas uji" di bagian Catatan, dan "30 hari" melebihi 28 hari tayang rencana. Angka total tetap benar; yang salah adalah logika kelayakan kanal saat bobot minggu tidak rata.

**Penilaian:** agent bisa menangani campuran, tetapi dengan improvisasi (pembagian 3/5 tidak berdasar aturan skill, penjumlahan gabungan dikerjakan tangan - bertentangan dengan prinsip "angka dari script").
