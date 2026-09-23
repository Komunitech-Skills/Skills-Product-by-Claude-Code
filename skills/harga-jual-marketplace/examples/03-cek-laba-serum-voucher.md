# 03 — Cek laba dari harga yang sudah dipasang (dengan voucher toko)

**Skenario:** S3 — permintaan normal, mode kebalikan. Penjual sudah menyerahkan surat pernyataan (tanpa PPh 22) dan memasang voucher toko.

**Input pengguna (persis):**
> Aku jual serum di Shopee harga 89.900, modal 52 ribu. Admin 10%, layanan 5% maks 10rb, biaya proses 1.250. Aku pasang voucher toko potongan 10rb. Omzet setahun masih 200an juta dan udah kirim surat pernyataan jadi ga kena PPh 22. Masih untung ga sih?

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/harga_marketplace.py --platform Shopee --modal 52.000 --admin 10 --layanan 5 --maks-layanan 10.000 --per-pesanan 1.250 --voucher 10.000 --pph22 tidak --harga-jual 89.900
```

## Output

### Shopee - cek harga Rp 89.900

| Komponen | Nilai |
|---|---:|
| Harga tayang | Rp 89.900 |
| Voucher toko | -Rp 10.000 |
| Harga setelah voucher | Rp 79.900 |
| Biaya admin/komisi (10%) | -Rp 7.990 |
| Biaya layanan/program ongkir (5%) | -Rp 3.995 |
| Biaya per pesanan (dibagi 1 barang) | -Rp 1.250 |
| **Uang diterima dari marketplace** | **Rp 66.665** |
| Modal/HPP | -Rp 52.000 |
| **Laba bersih per barang** | **Rp 14.665** |
| Margin (laba / harga setelah voucher) | 18,35% |
| Markup (laba / modal) | 28,2% |

**Catatan & asumsi**
- Persentase biaya platform berasal dari input Anda. Cek angka terbaru di Seller Center masing-masing (berbeda per kategori & program, dan bisa berubah).
- Biaya persen dan PPh 22 dihitung dari harga setelah voucher toko. Jika platform Anda memakai dasar lain, hasil bisa sedikit berbeda.
- Biaya dihitung tanpa pembulatan; angka di tabel dibulatkan ke rupiah terdekat.
- PPh 22 marketplace tidak dipotong (dianggap sudah menyerahkan surat pernyataan/SKB). Pastikan status ini benar di Seller Center.
- Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.

**Jawaban singkat:** Masih untung, **Rp14.665 per botol** (margin 18,35% dari harga setelah voucher).

💡 Saran:
- Voucher Rp10.000 menurunkan laba dari **Rp23.165 menjadi Rp14.665** (turun Rp8.500 per botol, karena biaya persen ikut turun sedikit). Pertimbangkan voucher dengan minimal belanja atau batas kuota.
- Kalau ingin tetap margin minimal 15% dengan voucher yang sama, harga tayang terendahnya **Rp86.500**; harga impasnya Rp72.648.

## Catatan penguji
- Dicek independen: dasar 79.900; admin 7.990; layanan 3.995 (di bawah maks); proses 1.250 → diterima 66.665 → laba 14.665. Tanpa voucher (dijalankan terpisah) laba 23.165. Benar.
- PPh 22 tidak dipotong dan output mengingatkan untuk memastikan status di Seller Center. Bagus.
- Saran berbasis angka (dua perhitungan tambahan dijalankan agent dengan script) sesuai langkah 3 SKILL.md.
