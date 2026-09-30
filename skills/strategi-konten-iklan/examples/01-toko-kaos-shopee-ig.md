# Contoh 01 - Toko kaos lokal, Shopee + Instagram, Rp5 juta

**Permintaan:** "Saya jual kaos sablon, anggaran iklan Rp5 juta sebulan. Harga rata-rata Rp150.000, margin 40%. Saya punya toko Shopee dan Instagram. Tolong bagi anggarannya dan bikin strategi kontennya."

**Perintah script:**
```
python3 scripts/alokasi_anggaran.py --anggaran 5jt --aov 150rb --margin 40% --kanal meta,shopee
```

## Keluaran script (nyata)
# Rencana Alokasi Anggaran Iklan - Rp5.000.000 / bulan
Tujuan: **penjualan** | 4 minggu x 7 hari = 28 hari tayang (sisa hari bulan dipakai evaluasi tanpa menambah anggaran).

## Target dari margin (batas impas, bukan prediksi)
- Harga rata-rata per pesanan: Rp150.000; margin kotor 40% -> laba kotor per pesanan Rp60.000
- **Titik impas ROAS = 1/margin = 2,50x** (di bawah ini iklan merugi); CPA impas Rp60.000
- **Target aman** (sisakan 30% laba kotor): CPA maks Rp42.000, ROAS minimal 3,58x
- Agar anggaran bulan ini sekadar impas dibutuhkan minimal 84 pesanan (= omzet Rp12.600.000); ini syarat impas, BUKAN perkiraan hasil.

## Anggaran per kanal
| Kanal | Anggaran | % | Aman 70% | Uji 30% |
|---|---:|---:|---:|---:|
| Meta (IG/FB) | Rp3.181.818 | 63,6% | Rp2.227.273 | Rp954.545 |
| Shopee Ads | Rp1.818.182 | 36,4% | Rp1.272.727 | Rp545.455 |
| **Total** | **Rp5.000.000** | 100% | | |

## Rencana per minggu
| Kanal | Minggu 1 | Minggu 2 | Minggu 3 | Minggu 4 | Jumlah |
|---|---:|---:|---:|---:|---:|
| Meta (IG/FB) | Rp795.453 | Rp795.455 | Rp795.455 | Rp795.455 | Rp3.181.818 |
| Shopee Ads | Rp454.544 | Rp454.546 | Rp454.546 | Rp454.546 | Rp1.818.182 |
| **Total** | **Rp1.249.997** | **Rp1.250.001** | **Rp1.250.001** | **Rp1.250.001** | **Rp5.000.000** |

## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)
| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |
|---|---:|---:|---:|
| Meta (IG/FB) | Rp113.636 | Rp25.000 | 4 |
| Shopee Ads | Rp64.935 | Rp10.000 | 6 |

Sisa pembulatan: Meta (IG/FB) antar minggu -Rp2; Shopee Ads antar minggu -Rp2. Total tetap sama dengan anggaran.

Angka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.

## Dokumen yang disampaikan ke pemilik (ringkas)
**Asumsi:** tujuan penjualan; TikTok/Google tidak dipakai karena pemilik hanya punya IG + Shopee; margin sudah setelah biaya admin Shopee.

**Pilar konten (4):**
| Pilar | Tahap | 3 sudut pesan | Format | Judul contoh |
|---|---|---|---|---|
| Padu padan & tips | Awareness | praktis, hemat, cocok tiap hari | Reels 15-20 detik | "3 cara pakai kaos polos ke kantor", "Kaos sablon awet: jangan salah cuci" |
| Proses sablon | Awareness-pertimbangan | buatan sendiri, detail, rapi | Video proses | "Dari desain sampai dikirim: 1 hari di studio kami" |
| Ulasan asli | Pertimbangan | ukuran pas, bahan adem, pengiriman cepat | Carousel foto ulasan (izin pembeli) | "Ulasan pembeli minggu ini" |
| Jawab keberatan + penawaran | Beli | ukuran, retur, bundling | Foto + tabel ukuran | "Tabel ukuran S-XXL", "Beli 3 lebih hemat" (harga asli, maks 30% konten) |

**Anggaran:** ikuti tabel di atas. Meta Rp3,18 jt (Rp954.545 untuk uji kreatif), Shopee Rp1,82 jt. Kanal Shopee sebaiknya dipakai setelah judul, foto, dan ulasan produk dibereskan.

**Angka kunci:** laba kotor Rp60.000/pesanan; iklan merugi di bawah ROAS 2,50x; target aman 3,58x; CPA maksimal Rp42.000. Untuk sekadar impas bulan ini perlu minimal 84 pesanan (Rp12,6 jt omzet) - ini syarat, bukan perkiraan hasil.

**3 langkah hari ini:** (1) foto 5 ulasan asli dengan izin; (2) rapikan judul & foto 3 kaos terlaris di Shopee; (3) buat 3 versi Reels dengan sudut pesan berbeda untuk minggu 1.
