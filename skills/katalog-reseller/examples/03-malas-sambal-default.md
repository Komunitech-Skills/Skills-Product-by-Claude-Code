# 03 — "bikinin price list reseller dong" sambal botol (S3, singkat/malas)

## Input pengguna
> bikinin price list reseller dong, sambal bawang 150ml modal 12rb jual 25rb

## Langkah agent
Info wajib (produk, HPP) ada. Tier tidak disebut, jadi dipakai **default contoh** script (Dropshipper 1 pcs 15%, Reseller 12 pcs 25%, Agen 60 pcs 35%). Biaya jual mitra tidak disebut, jadi 0%, dan agent menambahkan simulasi 10% sebagai pembanding karena reseller sambal sering berjualan di marketplace.
`hitung_tier.py --produk "Sambal Bawang 150 ml" --hpp 12.000 --eceran 25.000` (lalu sekali lagi dengan `--biaya-jual-mitra 10`).

## Output

# Price List Mitra — Sambal Bawang 150 ml

## Daftar harga (siap kirim ke calon mitra)
| Tier | Minimal beli | Harga mitra/botol | Harga eceran anjuran | Contoh untung* |
|---|---|---|---|---|
| Dropshipper | 1 botol | Rp 21.200 | Rp 25.000 | ±Rp 3.800/botol |
| Reseller | 12 botol | Rp 18.700 | Rp 25.000 | 12 botol (modal Rp 224.400) → ±Rp 75.600 |
| Agen | 60 botol | Rp 16.200 | Rp 25.000 | 60 botol (modal Rp 972.000) → ±Rp 528.000 |
\*Jika semua terjual di harga eceran, dijual langsung (WA/offline), belum termasuk ongkir.

## Catatan untuk kamu (internal)
- Margin kamu per botol: dropshipper Rp 9.200 (43,4%), reseller Rp 6.700 (35,8%), agen Rp 4.200 (25,9%). Semua masih di atas batas aman 15%.
- ⚠️ **Kalau mitra jualan di Shopee/TikTok (potongan ±10%)**, untung dropshipper tinggal **Rp 1.300/botol (5,2%)**. Itu terlalu tipis dan memancing banting harga. Untung reseller Rp 3.800 (15,2%), agen Rp 6.300 (25,2%). Kalau banyak mitramu berjualan online, naikkan diskon dropshipper ke 22% (harga Rp 19.500, untung Rp 3.000 atau 12% setelah potongan 10%). Diskon 25% tidak bisa dipakai karena akan sama dengan harga reseller. Pilihan lain: buka reseller & agen saja.
- Tier di atas adalah **contoh default**. Minimal beli dan persen diskon bisa disesuaikan.

**Syarat singkat:** tanpa biaya pendaftaran, tanpa bonus merekrut, bayar lunas sebelum kirim, retur untuk botol bocor/pecah maksimal 3 hari dengan video unboxing, harga eceran anjuran Rp 25.000 (bila dijual jauh di bawahnya: teguran, lalu penyesuaian tier, **tanpa denda**). Mau aku lengkapi dengan S&K lengkap dan pesan ajakan WA?

## Catatan penguji
- Hitungan dicek: 25.000 × 0,85 = 21.250 → Rp 21.200 (ke bawah) ✓; 25.000 × 0,65 = 16.250 → Rp 16.200 ✓. Dengan biaya 10%: 25.000 − 21.200 − 2.500 = 1.300 ✓ (dijalankan script: "MARGIN MITRA TIPIS").
- Default + asumsi disebut, sesuai SKILL.md. Permintaan malas dijawab ringkas dengan tawaran lanjutan, tidak dipaksa laporan 4 bagian penuh.
