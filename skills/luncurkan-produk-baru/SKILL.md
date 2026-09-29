---
name: luncurkan-produk-baru
description: Menyusun rencana peluncuran produk baru UMKM Indonesia (makanan, fashion, kriya, jasa) lengkap dengan jadwal bertanggal T-30 sampai T+30, teaser, daftar tunggu WA/Google Form, soft launch, grand launch, kanal (IG, TikTok, marketplace, grup WA, bazar, KOL mikro), runbook hari-H, kesiapan stok, aturan promo, ukuran hasil, dan pengingat label halal/BPOM/PIRT. Pakai saat pengguna bilang "mau luncurkan produk baru", "launching", "soft launch", "pre-order", "jadwal peluncuran", "product launch plan", "go-to-market" untuk produk usaha.
---

# Luncurkan Produk Baru

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah "saya mau launching produk" menjadi **rencana peluncuran satu paket yang siap dijalankan**: tujuan berangka, kanal terpilih, jadwal bertanggal (hari libur sudah diperhitungkan), teks siap tempel, stok yang dihitung, hari-H per jam, dan cara mengukur hasilnya.

## Kapan digunakan
- Produk fisik/jasa baru (atau varian besar baru) yang akan dijual ke publik lewat WA, IG, TikTok, marketplace, bazar.
- Ingin daftar tunggu, pre-order, soft launch, lalu launching resmi.
- Butuh daftar tugas bertanggal dari tanggal peluncuran yang sudah ditentukan.

## Kapan TIDAK digunakan
- Belum tahu produk apa yang dijual atau apakah laku: pakai `validasi-ide-produk-baru` atau `brainstorming-ide-usaha` dulu.
- Hanya ingin caption/iklan/listing satu kali: pakai `caption-sosmed-umkm`, `listing-marketplace`, `copy-landing-page`.
- Peluncuran perangkat lunak/aplikasi/startup (Product Hunt dst.): di luar cakupan.
- Butuh keputusan hukum/izin: skill ini hanya pengingat (lihat `references/legalitas-label.md`).

## Input (tanyakan SEKALI, dalam satu pesan)
Wajib: (1) produk & harga normal, (2) tanggal peluncuran yang diinginkan (atau "secepatnya"), (3) jenis: makanan/minuman, kosmetik, atau lain, (4) kanal yang sudah dimiliki (jumlah kontak WA, pengikut IG/TikTok, toko marketplace), (5) anggaran promo+iklan.
Opsional: stok awal & kapan barang tiba, foto/aset yang ada, target pesanan.
Bila pengguna ingin cepat: pakai default (jenis "lain", anggaran Rp 0 = hanya kanal gratis, tanggal = 35 hari dari hari ini) dan **sebutkan asumsinya** di awal jawaban.

## Langkah kerja

### 1. Gerbang kesiapan (2 menit)
Cek tiga hal di `references/runbook-hari-h.md` bagian A: satu janji jelas, sudah dicoba orang luar, kemasan/label utuh. Jika belum: sarankan soft launch kecil, bukan menunda tanpa batas dan bukan menambah fitur terus.

### 2. Tetapkan target dan angka dasar
- Target pesanan minggu 1 dari **daftar tunggu x 15-25%** (patokan awal, tandai sebagai asumsi) atau dari hasil soft launch bila ada.
- Harga & margin: hitung lewat `hitung-hpp` dan `harga-jual-marketplace` (biaya admin, ongkir, voucher). **Jangan menebak margin.**
- Stok awal = perkiraan pesanan minggu 1 x 1,3; titik pesan ulang = waktu tunggu pemasok x penjualan harian (contoh di runbook bagian B). Hitung dengan angka, tampilkan rumusnya.

### 3. Pilih 2-4 kanal
Pakai tabel dan skor 0-3 di `references/kanal-checklist.md`. Susun menurut milik/sewa/pinjam; daftar tunggu WA/formulir selalu menjadi kanal "milik" utama. Tiap kanal diberi satu kode/tautan pelacak.

### 4. Fase peluncuran
| Fase | Kira-kira | Isi | Keluaran |
|------|-----------|-----|----------|
| Pra-peluncuran / teaser | T-30 s.d. T-15 | janji produk, aset foto/video, formulir daftar tunggu, teaser 1-2, pesan ke tim pertama | daftar tunggu berjalan |
| Soft launch | T-14 s.d. T-7 | pre-order terbatas 30-50 unit untuk daftar tunggu; kumpulkan masukan 10 pembeli | perbaikan listing/label/kemasan |
| Persiapan akhir | T-7 s.d. T-1 | promo diputuskan, stok fisik, uji kirim, listing terjadwal, Go/No-Go H-1 | keputusan Go/No-Go |
| Grand launch | T0 | runbook per jam (bagian F) | angka hari-1 |
| Pasca-peluncuran | T+1 s.d. T+30 | kirim cepat, ulasan, bukti sosial, restok, akhiri promo jujur, tinjauan 30 hari | pelajaran + keputusan lanjut |

### 5. Jadwal bertanggal (dihitung script, bukan ditebak)
Jalankan (Windows: `python` atau `py`):
```
python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-14 --produk "Nama Produk" --jenis pangan
```
Pilihan: `--jenis pangan|kosmetik|lain`, `--hari-ini TTTT-BB-HH` (tandai tugas yang sudah lewat), `--libur-tambahan 2026-11-20,...`, `--format md|csv|json`. Script memakai Python standar, tanpa instalasi. Tugas pemasok/cetak/izin digeser ke hari kerja terdekat (mundur sebelum peluncuran, maju sesudahnya); konten tidak digeser tetapi diberi catatan bila jatuh di libur. Script juga memperingatkan: tanggal peluncuran di hari libur, dekat tanggal kembar (9.9/10.10/11.11/12.12), waktu tersisa <30 hari, dan tahun tanpa data libur (hanya 2026-2027 tersedia; libur di luar itu perlu dicek manual).
Bila script tidak bisa dijalankan: buat jadwal manual dengan pola T-30, T-25, T-21, T-14, T-7, T-3, T-1, T0, T+1, T+3, T+7, T+14, T+30 dan geser tugas pemasok dari Sabtu/Minggu/libur. Katakan bahwa daftar libur belum diperiksa.
Tanggal libur adalah SKB 3 Menteri 2026/2027 (data 2027 perlu ditinjau ulang terhadap lampiran resmi); selalu cocokkan pengumuman terbaru.

### 6. Teks siap tempel
Buat langsung (bukan saran umum), bahasa santai sopan, sesuai kanal yang dipilih:
- Pesan WA pribadi ke tim pertama; pesan pendaftar daftar tunggu (pembuka soft launch, pengingat H-1, pengumuman hari-H).
- 3 teaser IG/TikTok + posting hari-H (bisa dilanjutkan dengan `caption-sosmed-umkm`).
- Pesan ke KOL mikro (isi kesepakatan: konten, tanggal, tautan, tanda iklan).
- Balasan cepat: harga, ongkir, kedaluwarsa, izin/halal, cara simpan, retur.
Contoh format: `examples/02-pesan-siap-tempel.md`.

### 7. Promo
Terapkan `references/aturan-promo.md`: hitung margin di harga promo terendah, batasi waktu/jumlah, satu mekanisme utama, harga coret jujur.

### 8. Ukur dan tinjau
Catat 5 angka per hari selama T0-T+7 (kunjungan, chat, pesanan, omzet, stok sisa), lalu tinjauan hari 3, 7, 30 di `templates/rencana-peluncuran.md`. Iklan berbayar: laporan mingguan lewat `laporan-iklan-mingguan`. Target tim/karyawan bila ada: `kpi-tim`. Keputusan per kanal: lanjut / ubah / stop berdasarkan biaya per pesanan vs margin.

### 9. Pengingat legalitas & label
Untuk makanan/minuman/kosmetik selalu sisipkan pengingat NIB, PIRT/BPOM, halal, dan kecocokan label dengan listing (`references/legalitas-label.md`) dengan tautan situs resmi (oss.go.id, halal.go.id, cekbpom.pom.go.id). Ini pengingat, bukan keputusan; arahkan ke dinas/BPOM/BPJPH atau konsultan.

## Format output (urut tetap)
1. **Asumsi** (bila ada default yang dipakai).
2. **Ringkasan** 5 baris: produk, tanggal T0, kanal terpilih, target, anggaran.
3. **Kesiapan & angka**: hasil gerbang, stok (dengan rumus), margin promo.
4. **Jadwal bertanggal** (keluaran script apa adanya, dirapikan bila perlu).
5. **Teks siap tempel**.
6. **Runbook hari-H** (ringkas dari bagian F) dan **Go/No-Go H-1**.
7. **Pengukuran** dan **Pengingat legalitas**.
8. **3 langkah pertama yang bisa dikerjakan hari ini.**

## Contoh
Input: "Saya mau launching sambal botol baru tgl 14 Nov, stok 150 botol, kontak WA 120, IG 800 pengikut, anggaran promo 500 ribu."
Ringkas: jenis pangan; kanal terpilih WA daftar tunggu + IG + marketplace; jadwal 42 tugas T-30 = 15 Okt; peringatan bila T-30 sudah lewat. Lengkap: `examples/01-jadwal-sambal-botol.md` (keluaran nyata script).

## Batasan & penanganan error
- Tanggal salah format / tidak ada: script keluar dengan pesan "Galat" dan kode 2; minta pengguna menulis ulang TTTT-BB-HH.
- Tanggal peluncuran kurang dari 30 hari: jangan menolak; tandai tugas LEWAT, padatkan (gabungkan teaser, soft launch minimal 5 pembeli), dan katakan risiko terpangkasnya.
- Angka tidak diberikan: tanya sekali; bila tetap tidak ada, pakai patokan dan tandai "asumsi, ganti dengan angka nyata".
- Tidak mengirim pesan massal, tidak menjanjikan hasil penjualan, tidak membuat ulasan/testimoni palsu, tidak menyatakan produk halal/berizin/aman: hanya mengingatkan pengecekan.
- Di luar cakupan (validasi ide, pajak usaha, izin hukum, aplikasi/SaaS): arahkan ke skill lain atau profesional.
- Bukan nasihat hukum atau keuangan. Angka perkiraan (15-25%, x1,3) adalah patokan awal dan bukan jaminan.
