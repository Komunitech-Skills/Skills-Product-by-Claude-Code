# Contoh 02 - Kafe, awareness menjelang 12.12, Rp3 juta

**Permintaan:** "Kafe saya baru buka, mau lebih dikenal di kota. Anggaran Rp3 juta, minggu terakhir (promo 12.12) mau lebih besar. Fokus IG dan TikTok saja."

**Perintah script** (tujuan awareness tidak memerlukan harga/margin; bobot minggu 1 1 1 2):
```
python3 scripts/alokasi_anggaran.py --anggaran 3jt --tujuan awareness --kanal meta,tiktok --bobot-minggu 1 1 1 2
```

## Keluaran script (nyata)
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
| Meta (IG/FB) | Rp300.000 | Rp300.000 | Rp300.000 | Rp600.000 | Rp1.500.000 |
| TikTok Ads | Rp300.000 | Rp300.000 | Rp300.000 | Rp600.000 | Rp1.500.000 |
| **Total** | **Rp600.000** | **Rp600.000** | **Rp600.000** | **Rp1.200.000** | **Rp3.000.000** |

## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)
| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |
|---|---:|---:|---:|
| Meta (IG/FB) | Rp53.571 | Rp25.000 | 1 |
| TikTok Ads | Rp53.571 | Rp30.000 | 1 |

Sisa pembulatan: Rp0. Total tetap sama dengan anggaran.

## Catatan
- Tanpa --aov/--margin: rencana awareness tidak menghitung CPA/ROAS (memang bukan tolok ukurnya).

Angka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.

## Catatan untuk pemilik
- Tujuan awareness: ukur dengan jangkauan, kunjungan profil, dan pertanyaan "buka jam berapa?", bukan ROAS. Tidak ada janji jumlah pengunjung.
- Pilar: proses barista, menu baru, jawab "halal? porsi? colokan?", cerita pelanggan. Promosi 12.12 hanya di minggu ke-4 (maks +-30% konten).
- Minggu 4 berbobot 2 karena momen 12.12; naikkan bertahap, jangan mendadak (maks +20% per langkah bila berjalan).
- Musik: pakai audio yang diizinkan untuk iklan komersial.
