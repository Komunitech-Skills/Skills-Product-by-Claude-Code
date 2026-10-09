# 02 — Toko online hijab, kuartal, unit & harga (efek harga/volume/bauran)

> Contoh pembuat skill (v1.0.0). Angka dari `scripts/selisih.py --file examples/data/02-toko-hijab-q3.csv --periode "Kuartal 3 2026 (Jul-Sep)" --format teks`; diverifikasi ulang terpisah di `tests/uji_selisih.py` kasus D1–D7 (efek volume total 170 × Rp97.500 = Rp16.575.000; bauran −Rp8.925.000; harga −Rp16.200.000; jumlah = −Rp8.550.000).

## Pesan pengguna
"Toko hijab saya di Shopee & TikTok Shop, rekap Q3 (file CSV terlampir). Pashmina laku banyak tapi kok laba malah turun 26 juta?"

## Contoh balasan chat
**Rekap Kuartal 3 2026: laba Rp109.400.000 vs rencana Rp135.360.000 (−Rp25.960.000, −19,2%)**
Penjualan kurang Rp8,55 jt (−1,8%) walau jumlah barang terjual justru naik (4.800 → 4.970 pcs); biaya naik Rp17,41 jt (+5,2%), terbesar iklan marketplace.

| Pos | Selisih | Keterangan |
|---|---|---|
| Penjualan pashmina | +Rp29.050.000 (+14,2%) | menguntungkan; laku 550 pcs lebih banyak, harga turun |
| Penjualan gamis | −Rp19.600.000 (−13,3%) | merugikan; 80 pcs lebih sedikit |
| Penjualan bergo instan | −Rp18.000.000 (−15,4%) | merugikan; 300 pcs lebih sedikit |
| Iklan marketplace | +Rp8.500.000 (+47,2%) | merugikan |
| HPP | +Rp7.200.000 (+3,1%) | wajar: ikut naik karena barang terjual lebih banyak |
| Komisi marketplace | +Rp3.910.000 (+10,4%) | merugikan |
| Subsidi ongkir | −Rp2.900.000 (−32,2%) | menguntungkan (biaya turun) |
| Kemasan | +Rp700.000 (+9,7%) | merugikan |
| **Laba** | **−Rp25.960.000 (−19,2%)** | margin 28,9% → 23,8% |

**Kenapa angkanya begitu (penjualan −Rp8.550.000)**
- **Jual lebih banyak:** +Rp16.575.000 (170 pcs ekstra dengan harga rata-rata rencana).
- **Bauran bergeser ke produk murah:** −Rp8.925.000 (pashmina Rp85 rb naik, gamis Rp245 rb dan bergo turun).
- **Harga jual turun:** −Rp16.200.000, hampir semuanya dari pashmina (Rp85.000 → Rp79.000 per pcs = −Rp17.700.000; bergo +Rp1.500.000).
- Biaya variabel setelah disesuaikan jumlah barang terjual (+3,5%): HPP malah hemat Rp1.087.500; komisi marketplace tetap lebih Rp2.584.000 (+6,7%); kemasan lebih Rp445.000 (+6,0%). Ini perkiraan kasar karena campuran produk bergeser.

**Yang perlu dicek**
1. Pashmina: harga turun Rp6.000/pcs karena voucher toko, flash sale, atau ikut program gratis ongkir/cashback? Apakah penjualan ekstra datang dari potongan itu?
2. Gamis & bergo: stok/ukuran sempat kosong? Foto/ulasan produk bermasalah? Iklan dialihkan ke pashmina?
3. Iklan +Rp8,5 jt: berapa penjualan dari iklan per produk (biaya iklan ÷ penjualan dari iklan)?
4. Komisi marketplace: persentase biaya layanan/program yang diikuti berubah di kuartal ini?

**Tindakan kuartal depan**
- Hitung ulang harga promo pashmina: pastikan setelah komisi, iklan, dan HPP masih ada laba per pcs.
- Geser sebagian anggaran iklan ke gamis (nilai per pcs paling besar) dengan batas harian.
- Tinjau program marketplace yang menambah potongan; pertahankan hanya yang menambah laba, bukan hanya omzet.
- Revisi anggaran Q4 dengan harga jual dan campuran produk yang lebih realistis (tetap ditulis sebagai rencana baru).

**Pesan untuk tim (siap kirim)**
> Rekap Q3: barang terjual naik (4.970 pcs, rencana 4.800) tapi laba Rp109,4 jt, kurang Rp25,96 jt.
> Penyebab utama: harga pashmina turun Rp6 rb/pcs, gamis & bergo kurang laku, iklan +Rp8,5 jt.
> Tolong admin iklan kirim laporan biaya vs penjualan per produk, dan admin toko cek stok/ukuran gamis yang sempat kosong — sebelum Senin.

**Asumsi:** ambang 5% atau Rp500 rb; HPP, komisi, kemasan dianggap ikut jumlah barang terjual; harga rata-rata = nilai ÷ pcs (voucher & diskon masuk efek harga).
Catatan: analisis untuk manajemen, bukan audit/nasihat keuangan; penyebab perlu dicek ke nota, rekening, dan catatan stok.

Pertanyaan: berapa HPP per pcs tiap produk? Dengan itu saya bisa hitung laba per produk, bukan hanya penjualan.
