# Uji 07 - Normal 2: Bengkel motor, Rp1,5 juta/bulan, tujuan leads WhatsApp

Penguji independen, 2026-09-30, simulasi agent mengikuti SKILL.md v1.0.0.

## Permintaan
"Bengkel motor saya di Depok, mau iklan Rp1,5jt sebulan supaya banyak yang chat WA untuk servis. Rata-rata sekali servis + ganti part Rp250rb, untung bersih dari itu kira-kira 35%. Dari 10 yang chat biasanya 3 datang. Pakai IG sama Google."

## Perintah & keluaran script
```
python3 scripts/alokasi_anggaran.py --anggaran 1,5jt --tujuan leads --aov 250rb --margin 35% --closing 30% --kanal meta,google
```
```
# Rencana Alokasi Anggaran Iklan - Rp1.500.000 / bulan
Tujuan: **leads** | 4 minggu x 7 hari = 28 hari tayang (sisa hari bulan dipakai evaluasi tanpa menambah anggaran).

## Target dari margin (batas impas, bukan prediksi)
- Harga rata-rata per pesanan: Rp250.000; margin kotor 35% -> laba kotor per pesanan Rp87.500
- **Titik impas ROAS = 1/margin = 2,86x** (di bawah ini iklan merugi); CPA impas Rp87.500
- **Target aman** (sisakan 30% laba kotor): CPA maks Rp61.250, ROAS minimal 4,09x
- Leads (closing 30%): biaya per lead impas Rp26.250, target maks Rp18.375
- Agar anggaran bulan ini sekadar impas dibutuhkan minimal 18 pesanan (= omzet Rp4.500.000); ini syarat impas, BUKAN perkiraan hasil.

## Anggaran per kanal
| Kanal | Anggaran | % | Aman 70% | Uji 30% |
|---|---:|---:|---:|---:|
| Meta (IG/FB) | Rp1.500.000 | 100,0% | Rp1.050.000 | Rp450.000 |
| **Total** | **Rp1.500.000** | 100% | | |

## Rencana per minggu
| Kanal | Minggu 1 | Minggu 2 | Minggu 3 | Minggu 4 | Jumlah |
|---|---:|---:|---:|---:|---:|
| Meta (IG/FB) | Rp375.000 | Rp375.000 | Rp375.000 | Rp375.000 | Rp1.500.000 |
| **Total** | **Rp375.000** | **Rp375.000** | **Rp375.000** | **Rp375.000** | **Rp1.500.000** |

## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)
| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |
|---|---:|---:|---:|
| Meta (IG/FB) | Rp53.571 | Rp25.000 | 2 |

Kanal tidak dipakai: Google Ads (bagian anggarannya di bawah batas uji).
Sisa pembulatan: Rp0. Total tetap sama dengan anggaran.

Angka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.
```
Karena Google Ads terbuang (bagian 1.500.000 x 30/85 = 529.412 < 28 x 25.000 = 700.000), agent menjelaskan dengan bahasa awam dan - sesuai langkah 5 - tidak mengubah angka. Penguji juga menjalankan alternatif `--kanal google` (100% Google, 2 iklan aktif maks, angka target identik) untuk pembanding.

## Dokumen agent (ringkas)
- **Angka kunci:** laba kotor per servis Rp87.500; biaya per chat WA impas Rp26.250, target maks Rp18.375; CPA (per servis) impas Rp87.500, target Rp61.250; minimal 18 servis dari iklan agar Rp1,5jt impas.
- **Pilar (3 pilar, usaha kecil, 3 konten/minggu):** (1) Tips perawatan motor harian (awareness): "5 tanda kampas rem harus ganti", "Oli matic ganti tiap berapa km?", "Suara tek-tek di mesin, bahaya?", "Cara cek tekanan ban tanpa alat", "Motor susah hidup pagi hari: 3 penyebab". (2) Proses & kejujuran bengkel (pertimbangan): video servis CVT, "part asli vs KW: cara bedakan", "harga jasa kami terpampang", "mekanik kami", "garansi servis 7 hari". (3) Jadwal & penawaran (beli, <=30%): "slot kosong Sabtu ini" (asli), "paket servis gajian", "antar-jemput area X", "booking lewat WA", "ulasan Google asli".
- **Anggaran:** tabel script disalin. Iklan Meta tujuan "pesan WhatsApp", radius dekat bengkel; 2 iklan aktif maks.
- **Kanal tidak dipakai:** Google Ads - uangnya terlalu tipis dibagi dua; agent menyarankan: perkuat Google Business Profile (gratis, ulasan & foto) sekarang; bila ingin Google Ads, pilih salah satu saja (jalankan ulang `--kanal google`).
- **Aturan keputusan:** catat "tahu dari mana?" di WA; hitung biaya per chat mingguan terhadap Rp26.250.
- **Kepatuhan:** tanpa janji "pasti awet", harga di iklan harus sesuai; tanpa data nomor pelanggan di dokumen.

## Verifikasi independen
- Leads bobot meta 55 + google 30: Google 529.411,8 < 700.000 -> dibuang, sisa 1 kanal = 100% Meta 1.500.000. OK.
- Per minggu 375.000 x 4. Uji 450.000 / aman 1.050.000. Rata-rata harian 1.500.000/28 = 53.571,4 -> 53.571. Iklan maks 375.000 // 175.000 = 2. OK.
- Laba 250.000 x 35% = 87.500; ROAS impas 1/0,35 = 2,857 -> 2,86; target 1/0,245 = 4,082 -> 4,09; CPA target 61.250; CPL impas 87.500 x 30% = 26.250; target 18.375; pesanan 1.500.000/87.500 = 17,14 -> 18. OK.

**Penilaian:** angka benar. Temuan: untuk jasa lokal, `references/kanal-iklan-indonesia.md` menyebut Google "kuat untuk jasa lokal dengan niat beli tinggi", tetapi bobot tetap script (Meta 55 / Google 30) membuat Google yang terbuang. Agent perlu inisiatif menawarkan varian Google-saja; SKILL.md tidak menyuruhnya secara eksplisit.
