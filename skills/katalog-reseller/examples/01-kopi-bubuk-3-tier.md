# 01 — Program mitra kopi bubuk: dropshipper, reseller, agen (S1, normal)

## Skenario
Roastery kecil ingin membuka mitra. Ia sudah punya harga eceran. Resellernya kebanyakan berjualan di marketplace, dan ongkir dari roastery ke reseller ditanggung reseller.

## Input pengguna
> Aku roasting kopi bubuk robusta 250 gr, modal 32rb + kemasan & label 2rb, jual eceran 79rb. Mau buka dropshipper, reseller min 10, agen min 50. Rencananya diskon 15%, 25%, 35%. Reseller2 biasanya jualan di Shopee/TikTok, potongannya katanya sekitar 10%. Ongkir ke reseller rata2 1.500/bungkus mereka yang tanggung. Boleh diskon ke konsumen maks 5%. Bikinin price list, S&K, sama pesan rekrutnya ya.

## Langkah agent (mengikuti SKILL.md)
1. Mode `diskon`, karena harga eceran sudah ada.
2. `hitung_tier.py --hpp 32.000 --biaya-produsen 2.000 --eceran 79.000 --tier "Dropshipper:1:15" --tier "Reseller:10:25" --tier "Agen:50:35" --biaya-jual-mitra 10 --ongkir-ke-mitra 1.500 --maks-diskon-konsumen 5`
3. Status: Dropshipper **MARGIN MITRA TIPIS + RUGI DI HARGA MINIMUM**, Reseller **TIPIS**. Sesuai langkah 3, agent menjalankan ulang dengan usulan perbaikan: Dropshipper 20%, Reseller 30%, Agen 38%.
4. Dropshipper tidak menerima kiriman stok, jadi dihitung ulang **tanpa** ongkir ke mitra (run terpisah).
5. `--csv-keluar daftar-harga-mitra.csv` untuk versi yang dibagikan ke mitra.

## Output

# Program Mitra Kopi Robusta 250 g

## 1. Struktur harga (INTERNAL — jangan dibagikan)
**Usulan awal pengguna (15/25/35%)**
| Tier | Min. beli | Harga mitra | Diskon | Margin produsen | Untung mitra/unit* | Status |
|---|---|---|---|---|---|---|
| Dropshipper | 1 | Rp 67.100 | 15,1% | Rp 33.100 (49,3%) | Rp 2.500 (3,2%)** | ⚠️ TIPIS, rugi bila dijual di harga minimum (−Rp 1.100) |
| Reseller | 10 | Rp 59.200 | 25,1% | Rp 25.200 (42,6%) | Rp 10.400 (13,2%) | ⚠️ TIPIS (< 15%) |
| Agen | 50 | Rp 51.300 | 35,1% | Rp 17.300 (33,7%) | Rp 18.300 (23,2%) | ✅ |

**Usulan perbaikan (dihitung ulang script), direkomendasikan**
| Tier | Min. beli | Harga mitra | Diskon | Margin produsen | Untung mitra/unit* | Untung di harga min. Rp 75.000 | Status |
|---|---|---|---|---|---|---|---|
| Dropshipper | 1 | **Rp 63.200** | 20,0% | Rp 29.200 (46,2%) | Rp 7.900 (10,0%) | Rp 4.300 | ✅ |
| Reseller | 10 | **Rp 55.300** | 30,0% | Rp 21.300 (38,5%) | Rp 14.300 (18,1%) | Rp 10.700 | ✅ |
| Agen | 50 | **Rp 48.900** | 38,1% | Rp 14.900 (30,5%) | Rp 20.700 (26,2%) | Rp 17.100 | ✅ |
\*Setelah perkiraan potongan marketplace 10% (angka dari reseller, **contoh**; cek Seller Center masing-masing) dan ongkir ke mitra Rp 1.500/unit (reseller & agen).
\*\*Di run pertama, dropshipper ikut dikurangi ongkir Rp 1.500 oleh script. Tanpa ongkir pun untungnya hanya Rp 4.000 (5,1%), tetap tipis.

**Kenapa diperbaiki:** dengan diskon 15%, dropshipper hanya untung Rp 2.500–4.000 per bungkus setelah potongan marketplace. Mitra seperti ini biasanya cepat berhenti atau banting harga. Margin kamu tetap sehat di semua tier (terendah 30,5% di agen).

## 2. Daftar harga mitra (siap kirim)
| Produk | Harga eceran anjuran | Dropshipper (1 pcs) | Reseller (≥ 10 pcs) | Agen (≥ 50 pcs) |
|---|---|---|---|---|
| Kopi Robusta 250 g | Rp 79.000 | Rp 63.200 | Rp 55.300 | Rp 48.900 |
- Harga minimum anjuran untuk iklan/etalase online: **Rp 75.000**.
- Contoh reseller: beli 10 pcs = modal Rp 553.000. Jika semua terjual di harga eceran, untung ±Rp 143.000 (setelah potongan marketplace ±10% dan ongkir).
- Contoh agen: beli 50 pcs = modal Rp 2.445.000. Jika semua terjual di harga eceran, untung ±Rp 1.035.000.
- Contoh dropshipper: tanpa stok. Per pesanan untung ±Rp 7.900 bila dijual Rp 79.000 di marketplace.

## 3. Syarat & ketentuan kemitraan (siap tempel)
**SYARAT & KETENTUAN MITRA KOPI <NAMA BRAND>** (berlaku mulai [isi: tanggal berlaku])
1. Dropshipper tidak menyimpan stok. Pesanan dikirim langsung dari kami atas nama toko mitra, minimal 1 pcs.
2. Reseller: minimal 10 pcs per pembelian ([isi: boleh campur varian atau tidak]). Agen: minimal 50 pcs per pembelian.
3. Tier ditentukan dari jumlah pembelian dalam satu transaksi. **Tidak ada biaya pendaftaran. Tidak ada bonus dari merekrut mitra lain.**
4. Perubahan harga diinformasikan paling lambat [isi: jumlah] hari sebelumnya.
5. Pembayaran lunas sebelum barang dikirim, ke rekening atas nama usaha kami. Kami tidak pernah meminta transfer ke rekening pribadi lain.
6. Pesanan yang dibayar sebelum pukul [isi: jam] dikirim di [isi: hari kerja yang sama / hari kerja berikutnya]. Ongkir ke reseller/agen ditanggung mitra.
7. Untuk dropship: nama pengirim memakai nama toko mitra; invoice tanpa harga mitra.
8. Retur/tukar untuk kemasan bocor/rusak atau salah kirim maksimal [isi: jumlah] hari setelah diterima, dengan [isi: bukti yang diminta, mis. video pembukaan paket]. Kopi yang tidak laku [isi: boleh diretur/ditukar atau tidak, dan batasnya].
9. Harga eceran anjuran Rp 79.000. Harga minimum anjuran untuk iklan/etalase online Rp 75.000. Tujuannya menjaga citra produk dan agar semua mitra tetap untung. Mitra yang berulang kali memasang harga di bawah harga minimum anjuran akan diingatkan, lalu disesuaikan tiernya, lalu dihentikan kerja samanya. **Tidak ada denda uang.**
10. Mitra boleh memakai foto & materi resmi kami untuk menjual produk asli kami. Dilarang mengubah klaim, memakai untuk produk lain, atau menjual produk tiruan dengan merek kami.
11. Mitra hanya menyampaikan klaim yang tertulis di kemasan/materi resmi. Tidak boleh menambah klaim kesehatan.
12. Nama toko mitra tidak boleh menyerupai toko resmi kami.
13. Data konsumen hanya dipakai untuk memproses pesanan dan tidak dibagikan ke pihak lain.
14. Kerja sama dapat diakhiri salah satu pihak dengan pemberitahuan [isi: jumlah] hari; pesanan yang sudah dibayar tetap diproses.

## 4. Pesan ajakan rekrut
**WA broadcast** (hanya ke kontak yang pernah berinteraksi/setuju)
> Halo Kak, Kopi <brand> sedang membuka kesempatan jadi **mitra** 🙌
> 📦 Produk: Kopi Robusta bubuk 250 g
> 💰 Harga mitra mulai Rp 48.900/pcs (harga eceran anjuran Rp 79.000)
> 🧾 Pilihan: Dropshipper (tanpa stok, mulai 1 pcs) • Reseller (min. 10 pcs, modal ±Rp 553.000) • Agen (min. 50 pcs)
> 📈 Contoh: Reseller beli 10 pcs, jika semua terjual di harga eceran, untung ±Rp 143.000 (sudah dipotong perkiraan biaya marketplace & ongkir).
> ✅ Gratis pendaftaran • [isi: layanan pendukung yang benar-benar ada, mis. foto & materi promosi, retur kemasan rusak]
> Mau daftar harga lengkap & syaratnya? Balas **MITRA** ya, Kak.
> _(Tidak ingin menerima info seperti ini lagi? Balas STOP.)_

**Caption IG/TikTok**
> Mau jualan kopi tanpa roasting sendiri? ☕
> Harga mitra mulai Rp 48.900, eceran anjuran Rp 79.000. Bisa dropship tanpa stok, reseller mulai 10 pcs, atau agen 50 pcs. [isi: layanan pendukung yang benar-benar ada, mis. foto & materi promosi].
> Contoh jujur: reseller 10 pcs, jika semua terjual di harga eceran, untung ±Rp 143.000.
> DM "MITRA" untuk daftar harga. Tanpa biaya pendaftaran.

**Status singkat**
> Dibuka: mitra Kopi <brand>. Mulai 1 pcs (dropship). Untung ±Rp 7.900/pcs di harga eceran. DM "MITRA".

**Asumsi & catatan:** mode diskon dari harga eceran; harga tier dibulatkan ke **bawah** ke Rp 100 (diskon mitra tidak pernah lebih kecil dari yang dijanjikan); harga minimum dibulatkan ke bawah. Potongan marketplace 10% adalah perkiraan dari pengguna, jadi cek Seller Center mitra. Harga minimum ditulis sebagai anjuran + kebijakan kemitraan, bukan denda (lihat UU 5/1999 Pasal 8 & pengecualian usaha kecil Pasal 50 huruf h). Per 23 September 2026; bukan nasihat hukum/pajak. Tanggal berlaku, batas waktu (pemberitahuan harga, jam potong kirim, retur/tukar, pengakhiran kerja sama), kebijakan tukar kopi tidak laku, dan layanan pendukung (foto & materi promosi, retur kemasan rusak) tidak diberikan pengguna, jadi ditulis `[isi: ...]` (asumsi, ganti dengan data Anda; hapus bila tidak berlaku). Syarat nomor 5, 7, 9, 10–13 adalah usulan standar dari template.

## Catatan penguji
- **Verifikasi independen:** 300 kombinasi acak (mode diskon & margin, biaya produsen, biaya jual 0–15%, ongkir, maks. diskon konsumen, eceran diturunkan script) dihitung ulang dengan python terpisah (pecahan eksak): harga tier, arah pembulatan (diskon → ke bawah, margin → ke atas, eceran usulan → ke atas ke Rp 1.000), margin produsen, untung mitra di eceran & di harga minimum → **cocok 300/300**.
- Cek manual contoh ini: 79.000 × 0,62 = 48.980 → Rp 48.900 ✓; untung agen 79.000 − 48.900 − 7.900 − 1.500 = 20.700 ✓; 20.700 × 50 = 1.035.000 ✓.
- **Kelemahan:** `--ongkir-ke-mitra` dikurangkan juga dari tier Dropshipper, padahal dropshipper tidak menerima kiriman stok. Agent harus menjalankan ulang terpisah (lihat HASIL-UJI).
