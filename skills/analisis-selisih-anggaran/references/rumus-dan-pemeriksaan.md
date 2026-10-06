# Rumus & daftar pemeriksaan penyebab selisih

Dimuat bila perlu. Isi ini untuk agent; sampaikan ke pengguna dengan bahasa awam.

## 1. Rumus (semua dihitung `scripts/selisih.py`, Decimal)
| Ukuran | Rumus | Arti untuk pemilik |
|---|---|---|
| Selisih | realisasi − anggaran | berapa rupiah meleset |
| Persen | selisih ÷ anggaran × 100 (anggaran 0 → "tidak dianggarkan") | seberapa jauh dari rencana |
| Arah | pendapatan: + = menguntungkan; biaya: + = merugikan | dampaknya ke laba |
| Dampak ke laba | pendapatan: +selisih; biaya: −selisih | dipakai di jembatan laba |
| Efek volume (penjualan) | (unit realisasi − unit anggaran) × harga rata-rata anggaran | karena jual lebih banyak/sedikit |
| Efek harga (penjualan) | selisih − efek volume = (harga realisasi − harga anggaran) × unit realisasi | karena harga jual/diskon berubah |
| Efek volume total | (total unit realisasi − total unit anggaran) × harga rata-rata anggaran semua produk | jual lebih banyak secara keseluruhan |
| Efek bauran | jumlah efek volume per produk − efek volume total | yang laku lebih banyak produk murah/mahal |
| Efek jumlah/pemakaian (biaya) | (kuantitas realisasi − kuantitas anggaran) × harga satuan anggaran | jam lembur/bahan/orang lebih banyak |
| Efek harga satuan (biaya) | selisih − efek pemakaian | tarif/harga beli naik |
| Anggaran disesuaikan (biaya variabel) | anggaran × (unit terjual realisasi ÷ unit anggaran) | wajar naik karena penjualan naik |
| Material | \|selisih\| ≥ Rp500.000 **atau** \|persen\| ≥ 5% (bisa diubah, `--aturan dan`) | layak dibahas |

Pembulatan: rupiah terdekat; komponen terakhir dihitung sebagai sisa sehingga komponen selalu menjumlah persis ke total selisih.

**Urutan prioritas pembahasan:** rupiah terbesar dulu → persen sangat besar (bisa salah catat) → arah tak terduga (biaya turun drastis, penjualan naik padahal sepi) → pos yang baru meleset bulan ini → pos yang meleset berbulan-bulan (anggaran mungkin tidak realistis).

**Ciri penjelasan yang baik:** menyebut pos dan angkanya, membedakan harga vs jumlah, menyebut apakah sekali saja atau berlanjut, dan ada tindakan. Hindari: "biaya naik karena biaya naik", "faktor waktu" tanpa menyebut apa yang bergeser, "lain-lain" untuk selisih besar, hanya membahas pos terbesar dan melupakan pos yang saling menutup.

## 2. Pemeriksaan per pos (tulis sebagai pertanyaan, bukan tuduhan)
| Pos | Bila merugikan, yang perlu dicek |
|---|---|
| Penjualan / omzet | Jumlah transaksi atau nilai per transaksi yang turun? Ada hari tutup, cuaca, libur, pesaing baru, stok kosong, menu/produk habis? Diskon/promo lebih besar dari rencana? Penjualan belum tercatat (kasir, transfer, marketplace yang belum cair)? |
| HPP / bahan baku | Harga beli dari pemasok naik (cek nota)? Porsi/resep sesuai standar? Bahan terbuang/kedaluwarsa? Stok opname akhir bulan sudah dihitung? Pembelian stok untuk bulan depan ikut tercatat? |
| Gaji & lembur | Jumlah orang bertambah (karyawan baru, pengganti)? Jam lembur naik karena pesanan naik, ada yang absen, atau jadwal shift kurang pas? Tarif lembur/UMK baru? Ada THR/bonus yang jatuh di bulan ini? |
| Sewa | Ada kenaikan kontrak, denda, atau sewa tambahan (gudang, stand)? Dibayar per tahun lalu dicatat sekaligus? |
| Listrik, air, gas | Tarif naik? Alat baru (freezer, mesin, AC)? Jam buka lebih panjang? Tagihan dua bulan tercatat di satu bulan? Ada kebocoran/alat rusak? |
| Iklan & promosi | Ada kampanye di luar rencana? Anggaran harian iklan marketplace/Meta naik otomatis? Berapa penjualan yang datang dari iklan itu (biaya iklan ÷ penjualan dari iklan)? |
| Ongkir / subsidi ongkir | Program gratis ongkir ikut serta? Banyak kiriman ke luar pulau? Kurir/tarif berganti? Retur ongkos kirim balik? |
| Komisi marketplace / ojol | Persentase biaya layanan/komisi platform berubah? Ikut program (gratis ongkir, cashback) yang menambah potongan? Porsi penjualan lewat aplikasi naik? |
| Kemasan | Harga kemasan naik? Ganti jenis kemasan? Kemasan rusak/terbuang? |
| Transport / BBM | Rute lebih jauh, order lebih banyak, harga BBM naik, kendaraan sering servis? |
| Pos tidak dianggarkan | Pengeluaran sekali saja (perbaikan, denda) atau rutin yang lupa dianggarkan? |
| Pos menguntungkan besar | Benar hemat, atau tagihannya belum masuk / bergeser ke bulan depan? |

## 3. Tindakan yang lazim (pilih yang sesuai angka)
- Tetapkan batas (mis. anggaran iklan harian, maksimal jam lembur per minggu) dan siapa yang menyetujui bila lewat.
- Cek resep/porsi standar dan catat bahan terbuang selama 2 minggu.
- Bandingkan harga 2-3 pemasok untuk bahan yang naik.
- Jadwal ulang shift berdasarkan jam ramai sebelum menambah lembur.
- Ukur hasil iklan per kampanye; hentikan yang tidak membawa penjualan.
- Revisi anggaran pos yang terbukti tidak realistis (ditulis sebagai revisi anggaran berikutnya, realisasi tetap apa adanya).
- Pantau ulang bulan depan: pos material diberi target angka.
