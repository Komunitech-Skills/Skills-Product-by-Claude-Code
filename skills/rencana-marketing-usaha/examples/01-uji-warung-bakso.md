# Uji 01 — Skenario normal: warung bakso, anggaran Rp 3 juta/bulan

> Uji simulasi oleh agent penguji independen (Claude Code, bukan pembuat skill), 2026-09-29. Usaha fiktif. Angka anggaran/CAC/ROAS/corong adalah **keluaran nyata** `scripts/alokasi_anggaran.py`, diverifikasi ulang secara independen (lihat `HASIL-UJI.md`).

**Permintaan pengguna:**
"Saya punya warung bakso di Bekasi Timur, rame siang aja, malam sepi. Budget promosi 3 juta sebulan. Tolong bikinin rencana marketing 3 bulan ke depan (Okt-Des). Harga rata-rata sekali makan 20 ribu, modal bahan sekitar 9 ribu, bungkus plastik/kotak sekitar seribu. Ada GoFood juga, potongannya 20%. Kerja berdua sama istri."

**Perilaku agent:** semua info wajib sudah ada (usaha, harga, HPP, periode, anggaran); tujuan belum eksplisit -> agent mengusulkan satu tujuan dan menandainya untuk konfirmasi (sesuai tabel Input), tanpa bertanya ulang.

---

# Rencana Marketing Bakso Mas Parto — Oktober-Desember 2026

Disusun: 29 Sep 2026 | Pemilik rencana: Pemilik & istri | **Asumsi:** nota rata-rata Rp 20.000, HPP Rp 9.000, kemasan Rp 1.000/nota (dirata-rata dine-in & bungkus), potongan GoFood 20% (cek di dasbor GoBiz), omzet sekarang ± Rp 45 juta/bulan (≈ 75 nota/hari, perkiraan pemilik), pembelian ulang rata-rata 1,5x per pelanggan baru dalam 3 bulan (asumsi, ganti dengan data), tenaga 5 jam/minggu untuk marketing. **Tujuan diusulkan — mohon konfirmasi.**

## 0. Ringkasan
- Tujuan: tambah omzet Rp 12 juta/bulan (Rp 36 juta sekuartal ≈ 1.800 nota tambahan), terutama **jam malam 17.00-21.00**, per 31 Des 2026.
- Segmen: keluarga & pekerja pulang kantor radius 3 km (perumahan sekitar), makan malam/bungkus.
- Kanal utama (3): Google Maps, WhatsApp pelanggan lama + kartu stempel, iklan Meta/IG radius 3 km (+ konten TikTok/IG sebagai pendukung).
- Anggaran Rp 9.000.000 (Rp 3 jt x 3 bulan), cadangan eksperimen Rp 900.000.
- CAC titik impas Rp 10.000 per pelanggan baru (nota pertama), CAC target Rp 8.000, ROAS target 2,50. GoFood: impas Rp 6.000, ROAS impas 3,34 -> iklan GoFood hanya uji kecil.
- Minggu ini: rapikan Google Maps, cetak kartu stempel "10 mangkuk gratis 1", mulai catat "tahu kami dari mana?".

## 1. Kondisi sekarang
| Hal | Kondisi | Data |
|---|---|---|
| Omzet per bulan | ± Rp 45 juta, ramai siang, sepi malam | Perkiraan pemilik (DATA BELUM ADA per jam) |
| Produk andalan & margin | Bakso urat + es teh, margin kontribusi Rp 10.000/nota (50%) | Dihitung script |
| Pelanggan lama | Banyak langganan siang, nomor WA belum dicatat | DATA BELUM ADA |
| Kanal yang sudah jalan | GoFood, papan nama | — |
| Tenaga | Pemilik + istri, 5 jam/minggu | Asumsi |

## 2. Tujuan SMART
| Tujuan | Awal | Target | Tenggat | Cara ukur |
|---|---|---|---|---|
| Nota malam (17-21) per hari | belum dicatat (catat minggu 1) | +20 nota/hari | 31 Des | Buku kasir / aplikasi kasir, kolom jam |
| Omzet per bulan | ± Rp 45 jt | Rp 57 jt | Des 2026 | Rekap harian |
| Ulasan Google baru | cek jumlah sekarang | +60 ulasan asli | 31 Des | Google Business Profile |

## 3. Target pasar
Segmen prioritas: keluarga muda & pekerja pulang kantor di perumahan radius 3 km. Masalah: bingung makan malam praktis, hangat, harga jelas. Momen beli: 17.30-20.00, musim hujan (Okt-Des), tanggal gajian. Ada di: Google Maps ("bakso dekat saya"), grup WA perumahan, Instagram/TikTok lokal, GoFood.

## 4. Pesan kunci
Janji: **"Bakso urat hangat, kuah kaldu sapi asli, siap dalam 5 menit — enak buat makan malam keluarga."** Bukti: foto/video kuah direbus sejak pagi, ulasan Google asli, "sudah jualan sejak 2015" (isi sesuai fakta). Ajakan: "Chat WA untuk pesan bungkus, ambil tanpa antre."
Catatan klaim: jangan menulis "paling enak se-Bekasi" atau "100% tanpa pengawet" kecuali bisa dibuktikan.

## 5. Kanal
| Kanal | Peran di corong | Alasan | Pemilik | Jam/minggu |
|---|---|---|---|---|
| Google Maps & foto | Kenal + Tertarik | Pencari "bakso dekat saya" sudah siap makan | Istri | 0,5 |
| WA & kartu stempel | Beli lagi + Rekomendasi | Murah, pelanggan siang diajak datang malam | Istri | 1,5 |
| Iklan Meta/IG radius 3 km (jam 16-19) | Kenal | Uji kecil, ukur dengan kupon "MALAM" | Pemilik | 1 |
| Konten TikTok/IG (pendukung) | Kenal | Video 15 detik proses bakso; bahan iklan | Pemilik | 2 |
| GoFood | Beli | Sudah jalan; promo hanya bila margin aman | — | — |

## 6. Kalender
| Minggu / tanggal | Momen | Kegiatan | Kanal | PJ |
|---|---|---|---|---|
| 1-7 Okt | Persiapan | Isi Maps (jam, menu, 10 foto), cetak kartu stempel & QR ulasan, mulai catat sumber pelanggan & jam | Maps, kasir | Istri |
| 8-24 Okt | Musim hujan mulai | Iklan radius Rp 35.000/hari jam 16-19, konten "hujan-hujan enaknya bakso" | Meta, TikTok | Pemilik |
| 25 Okt-3 Nov | Gajian | "Paket keluarga 4 mangkuk" (cek margin di `promo-kalender`) | WA status, iklan | Pemilik |
| Nov | Evaluasi bulan 1 | Bandingkan CAC iklan vs Rp 10.000; pindahkan dana bila perlu | — | Pemilik |
| 25 Nov-3 Des | Gajian | Pengingat WA ke pelanggan yang pernah chat | WA | Istri |
| 20-31 Des | Libur sekolah & tahun baru | Pre-order bakso frozen/paket malam tahun baru (bila kapasitas ada) | WA, IG | Berdua |
Tanggal momen dicek per 29 Sep 2026; pastikan ulang jadwal promo GoFood di GoBiz. Jadwal posting dan tulis konten mingguan -> `konten-mingguan`.

## 7. Anggaran (keluaran script)
```
ANGGARAN Rp 9.000.000 untuk 3 bulan
- Iklan Meta-IG radius 3 km: Rp 3.240.000 total (36.0% dari anggaran), ~Rp 1.080.000/bulan
- Konten TikTok-IG: Rp 2.025.000 total (22.5% dari anggaran), ~Rp 675.000/bulan
- WA & kartu stempel: Rp 1.620.000 total (18.0% dari anggaran), ~Rp 540.000/bulan
- Google Maps & foto: Rp 1.215.000 total (13.5% dari anggaran), ~Rp 405.000/bulan
- Cadangan eksperimen (10%): Rp 900.000
Cek: jumlah semua = anggaran (OK). Sisa pembulatan Rp diserap kanal dengan sisa terbesar.
```
Isi dana non-iklan: cetak kartu stempel & QR, stiker kemasan, foto menu, hadiah mangkuk gratis (biaya HPP), bensin antar lokal.

## 8. Target angka (keluaran script)
> **Disegarkan ke v1.0.7 (2026-10-16):** blok di bawah adalah keluaran ulang `scripts/alokasi_anggaran.py target --harga-jual 20000 --hpp 9000 --biaya-platform 0 --biaya-per-pesanan 1000 --laba-target-per-pesanan 2000 --pembelian-ulang 1.5 --anggaran-iklan 3240000 --target-omzet 36000000`. Label lama "Pesanan dari iklan: 405" kini "Minimal pelanggan agar sesuai target (…): 405", ditambah baris "Titik impas iklan: 324" dan "Batas atas anggaran iklan, sesuai target laba: Rp 14.400.000". Angka lain sama dengan uji 2026-09-29.
```
Harga jual Rp 20.000 | HPP Rp 9.000 | biaya platform Rp 0 | biaya/pesanan Rp 1.000
Margin kontribusi per pesanan: Rp 10.000 (50.0%)  STATUS: AMAN
- CAC titik impas (pesanan pertama): Rp 10.000
- ROAS titik impas: 2.00
- CAC impas termasuk pembelian ulang: Rp 25.000
- CAC target: Rp 8.000
- ROAS target: 2.50
- Titik impas iklan (pelanggan agar biaya iklan tertutup margin, tanpa laba target; bukan perkiraan): 324
- Minimal pelanggan agar sesuai target (biaya iklan maks. Rp 8.000/pelanggan, laba Rp 2.000/pelanggan; bukan perkiraan): 405
- Omzet bila jumlah pelanggan sesuai target tercapai (bukan perkiraan): Rp 8.100.000
- Jumlah pesanan yang dibutuhkan untuk target omzet: 1800
- Batas atas anggaran iklan, impas (hanya bila SEMUA pesanan dari iklan; bukan saran belanja): Rp 18.000.000
- Batas atas anggaran iklan, sesuai target laba (hanya bila SEMUA pesanan dari iklan; bukan saran belanja): Rp 14.400.000
Cara baca: titik impas = batas agar iklan tidak rugi; angka 'sesuai target' = syarat agar laba target tercapai. Keduanya syarat, BUKAN perkiraan hasil iklan.
Kalau 'tanpa iklan' sebagian pesanan tetap datang (organik), iklan cukup menutup sisanya: kurangi pesanan_dibutuhkan dengan perkiraan pesanan organik.
```
GoFood (potongan 20%): margin Rp 6.000, CAC impas Rp 6.000, ROAS impas 3,34 -> iklan/voucher GoFood jauh lebih sempit; utamakan pesan WA ambil sendiri.

Artinya: iklan Rp 3,24 juta **balik modal bila menghasilkan 324 pelanggan baru** (titik impas iklan), dan **minimal harus menghasilkan 405 pelanggan baru** agar sesuai target laba (biaya iklan maks. Rp 8.000/pelanggan). Iklan sendiri tidak akan menutup 1.800 nota; sisanya dari pelanggan lama yang datang malam (kartu stempel, WA) dan Maps.

Corong iklan untuk 360 pelanggan baru sekuartal (**asumsi, ganti dengan data Anda**):
```
Target 360 pesanan -> perlu 300000 di awal corong (Jangkauan)
- Jangkauan -> Klik: konversi 1.5% -> butuh 300000 untuk dapat 4500
- Klik -> Chat/Kunjungan: konversi 20% -> butuh 4500 untuk dapat 900
- Chat/Kunjungan -> Pembeli: konversi 40% -> butuh 900 untuk dapat 360
```

## 9. KPI & rutinitas pantau
| Tahap | KPI | Target | Sumber | Dicek | Aturan hentikan/ubah |
|---|---|---|---|---|---|
| Kenal | Penelusuran & tampilan Maps | +50% | Google Business | Mingguan | — |
| Tertarik | Chat WA pesan bungkus | 10/hari | WA Business | Mingguan | — |
| Beli | Nota malam, kupon "MALAM" terpakai, CAC | +20 nota/hari, CAC ≤ Rp 8.000 | Kasir | Mingguan (10 menit, Senin) | Iklan dihentikan bila 4 minggu CAC > Rp 10.000 |
| Beli lagi | Kartu stempel aktif | 150 kartu | Hitung kartu | Bulanan | — |
| Rekomendasi | Ulasan Google baru | +60 | Google | Bulanan | — |

## 10. Risiko & rencana B
| Risiko | Tanda | Tindakan |
|---|---|---|
| Iklan tidak menghasilkan | Kupon MALAM < 5/hari setelah 3 minggu | Pindah dana ke WA/kartu stempel & kolaborasi warung kopi/pos ronda |
| Dapur kewalahan jam 18-19 | Tunggu > 15 menit | Siapkan bakso siap rebus, batasi paket promo |
| Hujan deras = sepi dine-in | Nota dine-in turun | Dorong pesan WA ambil/antar lokal |

## 11. Keputusan terbuka
- Konfirmasi tujuan +Rp 12 juta/bulan (usulan agent).
- Angka potongan GoFood sebenarnya; berapa nota dari GoFood.
- Apakah bisa antar sendiri radius 2 km.

## 12. Langkah minggu ini
1. Lengkapi Google Maps (jam buka malam, menu + harga, 10 foto). 2. Cetak 300 kartu stempel + QR ulasan di meja. 3. Tambah kolom "jam" & "tahu dari mana" di buku kasir.

*Rencana ini alat bantu; target adalah tujuan, bukan jaminan hasil.*

---

## Penilaian penguji
- Semua 12 bagian template terisi; asumsi di atas; tujuan usulan diberi label konfirmasi. ✔
- Angka dari script, cocok dengan verifikasi independen (0 selisih). ✔
- GoFood margin dihitung terpisah — wawasan nyata yang tidak ada di jawaban generik. ✔
- Kanal utama 3 + pendukung, sesuai aturan "maksimal 3". ✔ (Catatan: `examples/01-kedai-kopi-q4.md` bawaan memakai 5 kanal setara — lihat temuan.)
- Label script "Pesanan dari iklan: 405" harus ditafsirkan agent sebagai **minimal**, bukan perkiraan (agent melakukannya; lihat temuan M1). *(Catatan 2026-10-16: sejak v1.0.7 label script sudah "Minimal pelanggan agar sesuai target (…)" + baris "Titik impas iklan: 324"; blok bagian 8 di atas sudah disegarkan. Penilaian penguji ini tetap penilaian uji 2026-09-29.)*
