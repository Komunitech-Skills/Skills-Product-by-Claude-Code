# Rumus (untuk hitung manual bila script tidak bisa dijalankan)

Notasi: P = harga jual, C = HPP/biaya variabel per unit, f = potongan % dari harga (admin marketplace dll.), m = margin, k = markup, F = biaya tetap per bulan.

| Hitungan | Rumus | Pembulatan |
|---|---|---|
| Laba per unit | P × (1 − f) − C | rupiah terdekat |
| Margin | laba ÷ P | 2 desimal persen |
| Markup | laba ÷ C | 2 desimal persen |
| Margin → markup | m ÷ (1 − m) | |
| Markup → margin | k ÷ (1 + k) | |
| Harga dari target margin | C ÷ (1 − f − m) | **ke atas** ke rupiah |
| Harga dari target markup | C × (1 + k) ÷ (1 − f) | **ke atas** ke rupiah |
| BEP unit | F ÷ (P × (1 − f) − C) | **ke atas** ke unit |
| Unit untuk target laba L | (F + L) ÷ (P × (1 − f) − C) | ke atas |
| Batas aman | (penjualan − BEP) ÷ penjualan | |
| Harga promo (diskon d) | P × (1 − d) | rupiah terdekat |
| Beli X gratis Y | harga efektif = P × X ÷ (X + Y) | tidak dibulatkan |
| Kenaikan penjualan agar laba sama | laba normal ÷ laba promo − 1 | volume ke atas |
| Diskon maksimal | 1 − (harga lantai ÷ P) | |
| Volume impas saat ubah harga | volume × laba lama ÷ laba baru | ke atas |
| Elastisitas (ESTIMASI) | volume baru ≈ volume × (1 + e × perubahan harga) | unit terdekat |
| PPN non-mewah (PKP) | 11% × DPP (= 12% × 11/12 × DPP) | **ke bawah** sekali |
| DPP dari harga termasuk PPN T | DPP bulat terbesar dengan DPP + PPN(DPP) ≤ T; sisa ditampilkan | |
| Laba PKP (harga tayang T termasuk PPN) | DPP(T) − f × T − C; margin = laba ÷ DPP(T) | |
| Harga tayang minimum PKP untuk margin m | DPP terkecil dengan DPP − f × (DPP + PPN) − C ≥ m × DPP, lalu T = DPP + PPN(DPP) | DPP bulat, PPN ke bawah |
| Untung reseller | harga eceran anjuran (= harga toko) − harga beli reseller; persen = ÷ harga anjuran | |

Contoh PKP: HPP paket Rp95.500, margin 40% → DPP 95.500 ÷ 0,6 = 159.166,67 → 159.167; PPN ⌊17.508,37⌋ = 17.508 → harga tayang **Rp176.675** (bukan Rp176.700).

Contoh cek cepat: C = Rp11.500, target margin 40%, tanpa potongan → P = 11.500 ÷ 0,6 = 19.166,67 → **Rp19.167**.

Tulis "dihitung manual" di jawaban bila memakai rumus ini tanpa script.
