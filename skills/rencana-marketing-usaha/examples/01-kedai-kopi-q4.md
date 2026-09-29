# Contoh: Rencana Marketing Q4 — Kedai Kopi Senja (FIKTIF)

> Contoh buatan Komunitech dengan usaha fiktif. Angka konversi adalah **asumsi**; angka anggaran/CAC/ROAS/corong di bawah adalah keluaran nyata `scripts/alokasi_anggaran.py`.

**Permintaan pengguna:** "Bikin rencana marketing Oktober-Desember buat kedai kopi saya di Bandung. Budget Rp 6 juta, target 200 pesanan online per bulan."

**Asumsi (karena pengguna tidak menyebut):** menu andalan Es Kopi Susu Rp 25.000, HPP Rp 9.000, potongan aplikasi pesan-antar 20% (isi sendiri dari dasbor), kemasan Rp 1.000/pesanan, pembelian ulang rata-rata 1x per pelanggan dalam kuartal, pemilik + 1 barista, 5 jam/minggu untuk marketing. Pesanan online sekarang: 120/bulan (data dari pemilik).

## 0. Ringkasan
- Tujuan: pesanan online 120 -> 200 per bulan pada 31 Desember (dicatat di rekap penjualan).
- Segmen: pekerja kantor radius 3 km, usia 22-35, beli kopi saat gajian dan jam istirahat.
- Kanal utama: WhatsApp pelanggan lama, Instagram/Reels + Google Maps, iklan Meta kecil, kolaborasi kantor.
- Anggaran Rp 6.000.000 (10% cadangan eksperimen).
- CAC titik impas Rp 10.000, CAC target Rp 7.000; ROAS target 3,57.
- Minggu ini: rapikan Google Maps, catat sumber pelanggan, kumpulkan 30 nomor pelanggan yang pernah chat.

## 1. Kondisi sekarang
| Hal | Kondisi |
|---|---|
| Omzet online | 120 pesanan/bulan (aplikasi pesan-antar + WA) |
| Margin per pesanan | dihitung di bagian 8 |
| Pelanggan lama | ~85 nomor WA pernah chat (DATA: perlu dirapikan) |
| Kanal jalan | Instagram 2x/minggu tanpa jadwal; Maps belum diisi jam & menu |
| Tenaga | 5 jam/minggu |

## 2. Tujuan SMART
| Tujuan | Awal | Target | Tenggat | Ukur |
|---|---|---|---|---|
| Pesanan online/bulan | 120 | 200 | 31 Des | Rekap pesanan |
| Pelanggan beli ulang dalam 60 hari | belum tercatat | 25% | 31 Des | Catatan nomor WA |
| Ulasan Google baru | 12 | 40 | 31 Des | Google Business |

## 3. Target pasar
Pekerja kantor sekitar Jl. contoh (fiktif). Masalah: butuh kopi enak cepat saat istirahat dan sore, mau harga jelas. Momen beli: jam 09-10 dan 14-15, hari gajian. Ada di Instagram, WA grup kantor, Google Maps.

## 4. Pesan kunci
"Kopi susu asli, sampai di meja kantor Anda dalam 20 menit." Bukti: foto proses, ulasan Google, rating aplikasi. Ajakan: "Chat WA untuk paket kantor min. 5 gelas gratis antar."

## 5. Kanal
| Kanal | Peran | Alasan | Jam/minggu |
|---|---|---|---|
| WA & loyalitas | Beli lagi | murah, konversi tertinggi | 1,5 |
| Konten IG/Reels + foto | Kenal | pekerja kantor aktif di IG | 2 |
| Google Maps | Kenal + Tertarik | cari "kopi dekat saya" | 0,5 |
| Iklan Meta radius 3 km | Kenal | uji kecil, hanya bila CAC < impas | 0,5 |
| Kolaborasi kantor | Beli | paket kantor, order besar | 0,5 |

## 6. Kalender (ringkas)
| Tanggal | Momen | Kegiatan |
|---|---|---|
| Minggu 1-2 Okt | Persiapan | Isi profil Maps, kumpulkan nomor, mulai catat sumber pelanggan, uji iklan Rp 50.000/hari |
| 25 Okt | Gajian | Promo "tanggal muda": paket 3 gelas (cek margin di `promo-kalender`) |
| 10-11 Nov | 10.10/11.11 | Voucher toko di aplikasi pesan-antar; hanya bila margin promo aman |
| 25 Nov | Gajian + Hari Guru | Paket hadiah guru/kantor |
| 1-12 Des | 12.12 Harbolnas | Voucher + konten "kopi sore" |
| 15-24 Des | Natal & akhir tahun | Paket hampers kopi, pre-order 20 Des |
| 26-31 Des | Evaluasi | Ucapan terima kasih via WA, hitung hasil |

Jadwal posting harian: `kalender-konten-30hari`.

## 7. Anggaran (keluaran script)
```
ANGGARAN Rp 6.000.000 untuk 3 bulan
- Meta Ads: Rp 1.350.000 total (22.5% dari anggaran), ~Rp 450.000/bulan
- WA & loyalitas: Rp 1.080.000 total (18.0% dari anggaran), ~Rp 360.000/bulan
- Konten & foto: Rp 1.350.000 total (22.5% dari anggaran), ~Rp 450.000/bulan
- Google Maps: Rp 540.000 total (9.0% dari anggaran), ~Rp 180.000/bulan
- Kolaborasi kantor: Rp 1.080.000 total (18.0% dari anggaran), ~Rp 360.000/bulan
- Cadangan eksperimen (10%): Rp 600.000
Cek: jumlah semua = anggaran (OK). Sisa pembulatan Rp diserap kanal dengan sisa terbesar.
```

## 8. Target angka (keluaran script, iklan Meta Rp 1.350.000 = alokasi Meta Ads)
```
Harga jual Rp 25.000 | HPP Rp 9.000 | biaya platform Rp 5.000 | biaya/pesanan Rp 1.000
Margin kontribusi per pesanan: Rp 10.000 (40.0%)  STATUS: AMAN
- CAC titik impas (pesanan pertama): Rp 10.000
- ROAS titik impas: 2.50
- CAC impas termasuk pembelian ulang: Rp 20.000
- CAC target: Rp 7.000
- ROAS target: 3.58
- Pesanan dari iklan: 192
- Omzet dari iklan: Rp 4.800.000
```
Artinya: dengan margin sekitar Rp 10.000 per gelas, biaya iklan untuk mendapat 1 pesanan tidak boleh lebih dari Rp 10.000 (impas) dan idealnya Rp 7.000 (sisa laba Rp 3.000). Karena pelanggan beli ulang rata-rata 1x, batas impas efektif Rp 20.000 — tetap pakai target lebih ketat sampai data 4 minggu ada.

Corong untuk 600 pesanan/kuartal (asumsi konversi; ganti dengan data setelah 2 minggu):
```
Target 600 pesanan -> perlu 457334 di awal corong (Jangkauan)
- Jangkauan -> Klik: konversi 1.5% -> butuh 457334 untuk dapat 6860
- Klik -> Chat/Order: konversi 25% -> butuh 6860 untuk dapat 1715
- Chat/Order -> Pesanan: konversi 35% -> butuh 1715 untuk dapat 600
```

## 9. KPI & rutinitas
| Tahap | KPI | Target Q4 | Dicek |
|---|---|---|---|
| Kenal | Penelusuran Maps / jangkauan Reels | +50% | Mingguan |
| Tertarik | Chat WA masuk | 100/bulan | Mingguan |
| Beli | Pesanan online, CAC iklan | 200/bulan, CAC <= 7.000 | Mingguan |
| Beli lagi | % beli ulang 60 hari | 25% | Bulanan |
| Rekomendasi | Ulasan Google baru | 40 | Bulanan |
Aturan hentikan: iklan Meta dihentikan bila 4 minggu berturut-turut CAC > Rp 10.000.

## 10. Risiko & rencana B
| Risiko | Tanda | Tindakan |
|---|---|---|
| Iklan tidak menghasilkan | CAC > 10.000 selama 4 minggu | Pindahkan dana ke kolaborasi kantor & WA |
| Kapasitas barista penuh saat 12.12 | Waktu antar > 30 menit | Batasi voucher per hari |

## 11. Keputusan terbuka
- Persentase potongan aplikasi sebenarnya (ganti asumsi 20%).
- Apakah pembelian ulang benar 1x (cek rekap 60 hari).

## 12. Langkah minggu ini
1. Lengkapi Google Business Profile (jam, menu, 10 foto). 2. Kumpulkan dan catat 30 nomor WA pelanggan lama. 3. Pasang catatan "tahu kami dari mana?" di kasir dan chat.

*Rencana ini alat bantu; target adalah tujuan, bukan jaminan hasil.*
