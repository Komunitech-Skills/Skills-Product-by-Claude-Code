# Aturan Promo & Diskon yang Menjaga Margin

Dimuat saat langkah 5 SKILL.md. Karya orisinal Komunitech.

## 1. Rumus kunci (dihitung script `diskon`)
- Laba per unit normal = harga × (1 − potongan%) − HPP
- Laba per unit promo = harga promo × (1 − potongan%) − HPP
- **Kenaikan penjualan yang dibutuhkan** = laba normal ÷ laba promo − 1

Tabel cepat (tanpa potongan marketplace): berapa % penjualan harus naik agar laba kotor sama.

| Margin normal → / Diskon ↓ | 30% | 40% | 50% | 60% |
|---|---|---|---|---|
| 10% | 50% | 33% | 25% | 20% |
| 20% | 200% | 100% | 67% | 50% |
| 30% | tidak mungkin (0 laba) | 300% | 150% | 100% |

(Rumus: diskon ÷ (margin − diskon). Contoh margin 40%, diskon 20% → 0,2 ÷ 0,2 = 100%, penjualan harus 2×.)

## 2. Aturan umum
1. **Tentukan batas diskon maksimal sebelum promo** (`diskon ... --margin-min 30` → "diskon maksimal"). Tidak ada promo di bawah batas itu, termasuk saat ditumpuk dengan voucher marketplace.
2. **Promo harus punya tujuan & ukuran:** mis. "menarik 50 pelanggan baru", "menghabiskan 200 pcs stok mendekati kedaluwarsa". Tanpa tujuan, promo hanya memotong laba dari pembeli yang toh akan membeli.
3. **Batasi waktu dan/atau kuota** (3 hari, 100 pcs pertama, khusus Jumat). Promo terus-menerus membuat harga normal terlihat mahal.
4. **Lebih baik tambah nilai daripada potong harga:** bonus kecil (topping, cookies mini, gratis ongkir area dekat, kartu ucapan) sering lebih murah bagi Anda daripada diskon dengan nilai sama di mata pembeli. Hitung bonus sebagai tambahan HPP.
5. **Beli X gratis Y** = diskon efektif Y ÷ (X+Y). Beli 2 gratis 1 = diskon 33,33%, bukan "cuma satu barang". Cek dengan `--beli-gratis 2:1`.
6. **Diskon bertingkat per jumlah** (beli 3 hemat 10%) lebih aman dari diskon semua produk karena menaikkan jumlah belanja.
7. **Tumpukan promo:** jumlahkan semua potongan (voucher toko + diskon produk + gratis ongkir yang Anda tanggung) sebelum dicek.
8. **Jangan pakai harga coret palsu.** Harga "sebelum diskon" harus harga yang benar-benar berlaku sebelumnya (UU 8/1999 Perlindungan Konsumen melarang informasi harga yang menyesatkan). Bila ingin memakai harga coret di kemudian hari, harga normal itu harus **sungguh berlaku secara wajar** (dipajang dan bisa dibeli siapa saja di harga itu dalam periode yang wajar, bukan formalitas beberapa jam/hari hanya supaya ada angka untuk dicoret). Simpan bukti harga lama (tangkapan layar katalog, nota). Bila ragu, pakai framing jujur tanpa harga coret ("Harga Spesial Lebaran").
9. **Stop-loss promo:** tetapkan tanda berhenti (mis. setelah 3 hari penjualan tidak naik minimal separuh dari kebutuhan) dan kembalikan harga normal.
10. Promo **TIDAK DISARANKAN** bila: laba promo ≤ 0, kenaikan penjualan yang dibutuhkan > 100%, atau kapasitas produksi tidak cukup untuk volume yang dibutuhkan.

## 3. Kalender promo khas Indonesia (ringkas)
Tanggal kembar (9.9, 10.10, 11.11, 12.12, Harbolnas 12.12), gajian (25–5), Ramadan & Lebaran (hampers, kue kering), Natal/Tahun Baru, Imlek, Hari Ibu (22 Des), musim wisuda/sekolah. Rincian kalender → skill **promo-kalender**.

## 4. Diskon reseller vs diskon konsumen
- Diskon reseller = harga tetap (tangga), bukan promo; jangan diubah-ubah tiap minggu.
- Saat promo konsumen, beri tahu reseller lebih dulu dan pertimbangkan subsidi agar mereka tidak kalah harga dari toko Anda sendiri.
- **Konflik kanal:** harga promo konsumen **tidak boleh ≤ harga beli reseller/agen** (mis. agen beli Rp26.250 lalu flash sale konsumen juga Rp26.250). Cek dengan `diskon ... --harga-reseller Agen:26250` atau `tangga ... --harga-promo 26250`. Solusi: kecilkan diskon, kuota/maks beli per pembeli, promo varian tertentu saja, atau harga khusus reseller selama promo.
- **Potongan marketplace saat event** (11.11, 12.12, Harbolnas, flash sale) hampir tidak pernah 0%: hitung dengan `--kanal marketplace --biaya-persen <total>`; bila belum tahu angkanya, tanyakan atau pakai asumsi yang disebut jelas.
- Tetapkan **harga eceran anjuran** dan larangan banting harga di bawahnya dalam syarat reseller.
