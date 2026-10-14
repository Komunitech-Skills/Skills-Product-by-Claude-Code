# Rumus biaya, skor, dan sensitivitas (dipakai `scripts/banding_pemasok.py`)

Semua perhitungan memakai `Decimal` (tanpa pembulatan berantai). Rupiah dibulatkan ke rupiah terdekat (0,5 ke atas), kecuali PPN (ke bawah sekali).

## 1. Biaya sampai di tempat (landed cost)
1. **Jumlah beli** = maks(kebutuhan, MOQ efektif) → dibulatkan ke atas ke kelipatan/isi dus → dinaikkan per kelipatan sampai minimal belanja (Rp) terpenuhi. MOQ efektif juga mencakup tingkat harga terendah bila pemasok tidak menyebut harga di bawahnya.
2. **Harga berlaku** = harga tingkat tertinggi yang jumlah minimalnya ≤ jumlah beli (berlaku untuk semua unit). Tingkat berbentuk persen = harga dasar × (1 − persen).
3. **Subtotal** = harga berlaku × jumlah beli. **Diskon** = subtotal × diskon% + diskon Rp (maks. subtotal).
4. **Tagihan pemasok** = subtotal − diskon + ongkir yang ditagih pemasok + biaya lain dari pemasok.
5. **PPN** (pemasok PKP, non-mewah) = 11% × DPP (= 12% × 11/12), dibulatkan ke bawah.
   - Harga belum termasuk PPN: DPP = tagihan; bayar ke pemasok = tagihan + PPN.
   - Harga termasuk PPN: DPP = rupiah bulat terbesar dengan DPP + PPN ≤ tagihan; sisa (biasanya Rp0-1) ditampilkan.
   - Status PKP tidak jelas: tanpa PPN, tetapi **potensi PPN** (11% × tagihan) dilaporkan sebagai `[isian]`.
6. **Total bayar** = bayar ke pemasok + ongkir ke ekspedisi + biaya yang dikeluarkan sendiri.
7. **Biaya pembanding** = total bayar − PPN yang bisa dikreditkan (hanya bila pembeli PKP dan pemasok PKP). Opsi bunga modal *b*% per bulan: − manfaat tempo (bayar ke pemasok × (1 − DP%) × b × tempo/30) + biaya dana DP (bayar ke pemasok × DP% × b × lead time/30).
8. **Per unit** = biaya pembanding ÷ **kebutuhan** (stok sisa karena MOQ tidak dianggap bernilai: sikap hati-hati untuk kas UMKM). **Per unit dibeli** = biaya ÷ jumlah beli, disebut sebagai pembanding "bila sisa pasti terpakai". **Modal tertahan** = per unit dibeli × unit sisa.
9. **Selisih vs termurah** = biaya − biaya termurah (Rp) dan ÷ biaya termurah × 100 (%, 1 desimal).

## 2. Skor tertimbang (0-100 per kriteria)
| Kriteria | Bobot default | Rumus | Alasan |
|---|---|---|---|
| Biaya | 40 | 100 × biaya termurah ÷ biaya pemasok | Rasio, bukan min-max: beda 3% hanya mengurangi ±3 poin, tidak dibesar-besarkan |
| Lead time | 20 | 100 × (hari tercepat + 1) ÷ (hari pemasok + 1); **0 bila melewati tenggat**; 50 bila belum diketahui | +1 agar "kirim hari ini" (0 hari) tetap terhitung |
| Termin | 15 | 50 + hari bayar rata-rata × 50/30, dibatasi 0-100 | Tunai saat terima = 50, tempo 30 hari = 100, bayar di muka < 50 |
| Kualitas/rekam jejak | 15 | nilai 1-5 × 20 (belum dinilai = 3 → 60) | Dari penilaian pengguna, bukan tebakan |
| Fleksibilitas/MOQ | 10 | 100 × kebutuhan ÷ jumlah beli | Beli tepat sesuai kebutuhan = 100 |

- Hari bayar rata-rata = −DP% × lead time + (1 − DP%) × tempo (DP dibayar saat pesan, sebelum barang tiba).
- **Skor total** = Σ(bobot × skor) ÷ Σ bobot. Bobot boleh diubah dan tidak harus berjumlah 100 (dinormalisasi). Bobot yang tidak disebut tetap default.
- **Peringkat** = pemasok yang tepat waktu lebih dulu (skor total 1 desimal tertinggi; seri → lebih murah → nama), lalu pemasok yang melewati tenggat dengan aturan yang sama.
- **Rekomendasi = peringkat 1** (selalu sama dengan tabel). Bila semua melewati tenggat, skor tertinggi + catatan untuk minta percepatan. Beda < 2 poin dengan urutan kedua → "hampir seri".

Contoh bobot alternatif yang wajar: barang untuk acara bertanggal (lead time 40, biaya 30, termin 10, kualitas 15, MOQ 5); bahan makanan/kosmetik (kualitas 30, biaya 35, lead 15, termin 10, MOQ 10); kas sedang seret (termin 30, biaya 35, lead 15, kualitas 15, MOQ 5).

## 3. Sensitivitas
1. **Jumlah 2×:** semua dihitung ulang untuk kebutuhan × 2 (tingkat harga & MOQ bisa membalik urutan).
2. **Pemasok termurah yang tepat waktu telat** (default 7 hari, `--telat-hari`; termurah yang sudah melewati tenggat tidak dipakai sebagai subjek): lead time + hari telat → skor & rekomendasi dihitung ulang; dilaporkan apakah melewati tenggat. Penghematan vs termurah kedua dihitung; bila kerugian per hari telat diketahui (`--biaya-telat-per-hari`, mis. penjualan hilang), **hari impas** = penghematan ÷ kerugian per hari (dibulatkan ke bawah).
3. **Bagi pesanan** (default 70/30, `--bagi`): rekomendasi mendapat 70% kebutuhan, cadangan 30% (dipilih dari calon lain yang total gabungannya paling murah; MOQ & tingkat harga tetap berlaku untuk tiap bagian; ongkir tetap dihitung penuh di masing-masing). Dilaporkan "lebih MAHAL/lebih MURAH Rp… daripada membeli semua dari [rekomendasi]" (tanpa tanda +/−).

## 4. Ringkasan siap salin (sejak 1.0.1)
Hasil `--format teks` memuat blok **RINGKASAN SIAP SALIN**: kalimat utuh bersubjek yang wajib disalin agent apa adanya.
- Setiap selisih ditulis "A lebih MURAH Rp… daripada B" atau "A lebih MAHAL Rp… (x%) daripada B". Persen hanya pada "lebih MAHAL" dan selalu terhadap yang lebih murah, sama dengan kolom tabel "selisih vs termurah".
- Isi: peringkat; rekomendasi (= peringkat 1); rekomendasi vs termurah (dan vs termurah yang tepat waktu bila termurah telat); jumlah 2×; termurah yang tepat waktu telat (default 7 hari); bagi pesanan; batas ongkir/biaya ambil; skenario status PKP belum jelas; asumsi pajak; pilihan pengguna (`--pilihan`).
- **Batas ongkir (ongkir impas):** untuk pemasok yang ongkirnya belum diketahui, dicari ongkir sekali kirim terbesar (rupiah bulat, pencarian biner memakai hitungan penuh termasuk PPN bila pemasok PKP) sehingga biayanya tidak lebih mahal daripada pemasok lain termurah yang tepat waktu. Ditampilkan juga per satuan (batas ÷ jumlah) sebagai aturan umum. Sama untuk biaya ambil sendiri (loco).
- **Skenario status PKP belum jelas:** pemasok itu dihitung ulang sebagai PKP dengan harga belum termasuk PPN; dilaporkan total baru, perbandingan dengan pesaing terdekat yang tepat waktu, dan apakah rekomendasi berubah (beserta kriteria yang membuatnya berubah).
- **Termurah sementara:** termurah yang ongkir/biaya ambil/status PPN-nya belum pasti diberi label ini di tabel dan ringkasan.

## 5. Data rusak
- Penawaran tanpa harga terbaca, angka negatif, DP > 100%, nilai kolom `ppn` di luar kamus, tingkat harga tidak terbaca, atau MOQ/ongkir "per dus" tanpa isi per dus → **dilewati** (dilaporkan dengan alasan dan saran); penawaran lain tetap dihitung.
- Jumlah kebutuhan kosong/0, semua penawaran rusak, data kosong, JSON rusak, bobot tidak dikenal/semuanya nol → **kode keluar 2** dengan `error` + `saran`.
- Satuan baku diubah otomatis: 1 lusin = 12, 1 kodi = 20, 1 gross = 144 (kecuali satuan kebutuhan memang lusin/kodi). Ongkir "Rp500/pcs" atau "15rb/dus" dibaca per unit/per kemasan, bukan sekali kirim.
- Kolom kosong (ongkir, lead time, termin, PKP) → tidak gagal; diberi default yang disebut di asumsi dan masuk daftar `[isian]`.
