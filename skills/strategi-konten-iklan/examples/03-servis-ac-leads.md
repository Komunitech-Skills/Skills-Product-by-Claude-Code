# Contoh 03 - Jasa servis AC (leads), Rp8 juta

**Permintaan:** "Servis AC di Bekasi. Anggaran Rp8 juta. Nilai rata-rata satu order Rp600.000, margin 45%. Dari 10 orang yang chat WA, sekitar 3 jadi pesan."

**Perintah script:**
```
python3 scripts/alokasi_anggaran.py --anggaran 8jt --tujuan leads --aov 600rb --margin 45% --closing 30%
```

## Keluaran script (nyata)
# Rencana Alokasi Anggaran Iklan - Rp8.000.000 / bulan
Tujuan: **leads** | 4 minggu x 7 hari = 28 hari tayang (sisa hari bulan dipakai evaluasi tanpa menambah anggaran).

## Target dari margin (batas impas, bukan prediksi)
- Harga rata-rata per pesanan: Rp600.000; margin kotor 45% -> laba kotor per pesanan Rp270.000
- **Titik impas ROAS = 1/margin = 2,23x** (di bawah ini iklan merugi); CPA impas Rp270.000
- **Target aman** (sisakan 30% laba kotor): CPA maks Rp189.000, ROAS minimal 3,18x
- Leads (closing 30%): biaya per lead impas Rp81.000, target maks Rp56.700
- Agar anggaran bulan ini sekadar impas dibutuhkan minimal 30 pesanan (= omzet Rp18.000.000); ini syarat impas, BUKAN perkiraan hasil.

## Anggaran per kanal
| Kanal | Anggaran | % | Aman 70% | Uji 30% |
|---|---:|---:|---:|---:|
| Meta (IG/FB) | Rp4.400.000 | 55,0% | Rp3.080.000 | Rp1.320.000 |
| TikTok Ads | Rp1.200.000 | 15,0% | Rp840.000 | Rp360.000 |
| Google Ads | Rp2.400.000 | 30,0% | Rp1.680.000 | Rp720.000 |
| **Total** | **Rp8.000.000** | 100% | | |

## Rencana per minggu
| Kanal | Minggu 1 | Minggu 2 | Minggu 3 | Minggu 4 | Jumlah |
|---|---:|---:|---:|---:|---:|
| Meta (IG/FB) | Rp1.100.000 | Rp1.100.000 | Rp1.100.000 | Rp1.100.000 | Rp4.400.000 |
| TikTok Ads | Rp300.000 | Rp300.000 | Rp300.000 | Rp300.000 | Rp1.200.000 |
| Google Ads | Rp600.000 | Rp600.000 | Rp600.000 | Rp600.000 | Rp2.400.000 |
| **Total** | **Rp2.000.000** | **Rp2.000.000** | **Rp2.000.000** | **Rp2.000.000** | **Rp8.000.000** |

## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)
| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |
|---|---:|---:|---:|
| Meta (IG/FB) | Rp157.143 | Rp25.000 | 6 |
| TikTok Ads | Rp42.857 | Rp30.000 | 1 |
| Google Ads | Rp85.714 | Rp25.000 | 3 |

Kanal tidak dipakai: Shopee Ads (kurang cocok untuk tujuan ini); TikTok Shop Ads (kurang cocok untuk tujuan ini).
Sisa pembulatan: Rp0. Total tetap sama dengan anggaran.

Angka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.

## Catatan untuk pemilik
- Untuk leads yang dihitung adalah **biaya per calon pembeli (chat WA)**, bukan biaya per pesanan: laba kotor per order Rp270.000 x closing 30% = biaya per lead impas Rp81.000; target aman Rp56.700.
- Shopee & TikTok Shop tidak dipakai (bukan kanal leads jasa lokal). Google Ads (pencarian "servis AC Bekasi") + profil Google Bisnis biasanya paling dekat dengan niat beli; Meta untuk menjaring yang belum mencari.
- Catat setiap chat: "tahu dari mana?" dan jadi/tidak, supaya angka closing 30% dikoreksi dari data sendiri.
