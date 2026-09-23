# 02 — Konveksi hijab: 3 produk, harga dari modal (mode margin), 2 produk belum punya harga eceran (S2, normal)

## Skenario
Produsen hijab ingin menjamin margin kotor tiap tier (reseller 40%, agen 30%, distributor 22%). Dua produk belum punya harga eceran. Resellernya berjualan di marketplace dengan potongan ±8%.

## Input pengguna
> Aku konveksi hijab. Modal: voal motif 24.500, pashmina ceruty 19.000, bergo instan jersey 31.000 (bergo udah aku jual eceran 65rb). Aku mau untung minimal: dari reseller (min 6 pcs) 40%, agen (min 30) 30%, distributor (min 120) 22%. Harga eceran voal & pashmina belum ada, tolong sekalian diusulin. Reseller rata2 jualan di Shopee, potongannya kira2 8%.

## Langkah agent
1. Mode `margin` lewat `--config hijab.json` (tier global, biaya jual mitra 8%). Voal & pashmina tanpa `eceran`, jadi script mengusulkan harga eceran.
2. Run pertama: harga eceran usulan (target untung mitra default 20%) menghasilkan status **MARGIN MITRA TIPIS** untuk tier Reseller di ketiga produk (12,5–13,3%). Penyebabnya: harga eceran diturunkan **sebelum** dipotong biaya marketplace 8%.
3. Run ulang dengan `--target-margin-mitra 28`. Voal & pashmina menjadi AMAN. Bergo (eceran sudah ditetapkan Rp 65.000) tetap tipis, jadi dihitung opsi eceran Rp 69.000.

## Output

# Program Mitra Hijab <brand>

## 1. Struktur harga (INTERNAL)
| Produk | Tier | Min. beli | Harga mitra | Margin produsen | Untung mitra/unit* | Status |
|---|---|---|---|---|---|---|
| Hijab Voal Motif (eceran usulan **Rp 57.000**) | Reseller | 6 | Rp 40.900 | Rp 16.400 (40,1%) | Rp 11.540 (20,2%) | ✅ |
| | Agen | 30 | Rp 35.000 | Rp 10.500 (30,0%) | Rp 17.440 (30,6%) | ✅ |
| | Distributor | 120 | Rp 31.500 | Rp 7.000 (22,2%) | Rp 20.940 (36,7%) | ✅ |
| Pashmina Ceruty (eceran usulan **Rp 45.000**) | Reseller | 6 | Rp 31.700 | Rp 12.700 (40,1%) | Rp 9.700 (21,6%) | ✅ |
| | Agen | 30 | Rp 27.200 | Rp 8.200 (30,1%) | Rp 14.200 (31,6%) | ✅ |
| | Distributor | 120 | Rp 24.400 | Rp 5.400 (22,1%) | Rp 17.000 (37,8%) | ✅ |
| Bergo Instan Jersey (eceran **Rp 65.000**, sekarang) | Reseller | 6 | Rp 51.700 | Rp 20.700 (40,0%) | Rp 8.100 (12,5%) | ⚠️ TIPIS |
| | Agen | 30 | Rp 44.300 | Rp 13.300 (30,0%) | Rp 15.500 (23,8%) | ✅ |
| | Distributor | 120 | Rp 39.800 | Rp 8.800 (22,1%) | Rp 20.000 (30,8%) | ✅ |
\*Setelah perkiraan potongan marketplace 8% (angka dari pengguna, contoh; cek Seller Center mitra).

**Perbaikan untuk bergo** (dihitung ulang script): naikkan eceran anjuran ke **Rp 69.000**. Untung reseller menjadi Rp 11.780 (17,1%, AMAN), agen Rp 19.180, distributor Rp 23.680. Harga mitra tetap sama. Kalau harga Rp 65.000 tidak mau diubah, pilihannya adalah menurunkan target margin reseller kamu (mis. 35% → harga reseller ±Rp 47.700). Ini perlu dicek ulang dengan script sebelum dipakai.

**Catatan harga eceran usulan:** Rp 57.000 dan Rp 45.000 adalah **usulan** agar reseller untung ±20% bersih setelah potongan marketplace. Bandingkan dulu dengan harga hijab serupa di pasaran (skill `harga-jual-marketplace`).

## 2. Daftar harga mitra (siap kirim)
| Produk | Eceran anjuran | Reseller (≥ 6) | Agen (≥ 30) | Distributor (≥ 120) |
|---|---|---|---|---|
| Hijab Voal Motif | Rp 57.000 | Rp 40.900 | Rp 35.000 | Rp 31.500 |
| Pashmina Ceruty | Rp 45.000 | Rp 31.700 | Rp 27.200 | Rp 24.400 |
| Bergo Instan Jersey | Rp 69.000 | Rp 51.700 | Rp 44.300 | Rp 39.800 |
Harga minimum anjuran = harga eceran anjuran (tidak ada ruang diskon ke konsumen yang ditetapkan). Tier boleh campur produk & warna <sesuaikan>.
Contoh reseller voal: beli 6 pcs = modal Rp 245.400. Jika semua terjual di harga eceran, untung ±Rp 69.240 (setelah potongan marketplace ±8%).

## 3. S&K kemitraan
Memakai 14 butir yang sama dengan contoh 01 (jenis mitra, tanpa biaya pendaftaran & tanpa bonus rekrut, pembayaran lunas, retur cacat/salah kirim 3 hari dengan video, harga minimum anjuran + teguran → penyesuaian tier → penghentian, **tanpa denda**, izin foto, data konsumen). Minimal order disesuaikan: 6 / 30 / 120 pcs.

## 4. Pesan rekrut (WA)
> Halo Kak, <brand> hijab sedang membuka kesempatan jadi **mitra** 🙌
> 📦 Produk: hijab voal motif, pashmina ceruty, bergo instan jersey
> 💰 Harga mitra mulai Rp 24.400/pcs (eceran anjuran mulai Rp 45.000)
> 🧾 Reseller min. 6 pcs (boleh campur) • Agen min. 30 pcs • Distributor min. 120 pcs
> 📈 Contoh: reseller 6 voal, jika semua terjual di harga eceran, untung ±Rp 69.240 (sudah dipotong perkiraan biaya marketplace).
> ✅ Gratis pendaftaran • foto katalog disediakan • retur untuk barang cacat
> Balas **MITRA** untuk daftar harga lengkap. _(Balas STOP bila tidak ingin menerima info ini.)_

**Asumsi:** mode margin, dengan harga mitra dibulatkan **ke atas** ke Rp 100 (margin kamu tidak pernah di bawah target). Harga eceran usulan dibulatkan ke atas ke Rp 1.000. Tidak ada biaya produsen tambahan & ongkir ke mitra (bisa diisi). Per 23 September 2026.

## Catatan penguji
- Cek manual: 24.500 ÷ 0,6 = 40.833 → Rp 40.900 (ke atas) ✓; eceran usulan 40.900 ÷ 0,72 = 56.806 → Rp 57.000 ✓; untung 57.000 − 40.900 − 4.560 = 11.540 ✓.
- **Cacat desain (sedang):** harga eceran usulan dihitung dari `--target-margin-mitra` **tanpa** memperhitungkan `--biaya-jual-mitra` dan ongkir. Di run pertama, script mengusulkan harga yang langsung dinilainya sendiri sebagai TIPIS. Agent harus menaikkan target secara manual.
