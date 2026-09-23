# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "SKILL.md discount strategy", "promo calendar skill", "ecommerce promotion margin skill", "Black Friday discount skill", "rencana promo harbolnas skill".
- Sumber dicek: github.com/anthropics/skills (tidak ada skill promo), github.com/manairalabs/bicara-skills & github.com/alvinindra/bahasa-skills (tidak ada skill promo; `bahasa-marketing` hanya soal copywriting), github.com/VoltAgent/awesome-openclaw-skills (yang ada hanya pengirim pesan promo/webhook dan pencari kupon, bukan perencana promo), skills.sh (hasil pencarian web), github.com/mardab96/ecommerce-claude-skills (`promo-discount-impact-review-ecommerce`, **evaluasi pasca-promo**, MIT).
- **Pesaing paling sebanding untuk perencanaan:** `discount-marketing-strategy`, dari github.com/kostja94/marketing-skills, path `skills/strategies/commercial/pricing/discount-marketing/SKILL.md`, **lisensi MIT**, v1.1.1. Pembanding kedua: `promo-discount-impact-review-ecommerce` (mardab96, MIT). Script `promo_impact.py` miliknya **tidak dijalankan**.
- Isi pesaing tidak disalin.

## Output dengan instruksi pesaing (disimulasikan, input S1)
Instruksi `discount-marketing-strategy`: identifikasi tipe produk, tujuan, tipe diskon, dan batasan (margin); pilih struktur kupon (persen/fixed/BOGO/free shipping); strategi musiman (contoh BFCM: "10–25% sering lebih baik dari potongan dalam"); output berisi tipe diskon, kampanye, pendekatan kode, dan *financial guardrails*.

> **Discount type:** Untuk e-commerce skincare, diskon 10–25% sering lebih efektif daripada potongan dalam. 40% berisiko menarik pembeli yang sensitif harga dan merusak persepsi harga.
> **Campaign (11.11):** mulai teaser ±1 minggu sebelumnya; gunakan countdown dan persen diskon yang menonjol; promosikan lewat email/sosmed/iklan.
> **Redeem code:** kode voucher unik per kanal (IG, TikTok) untuk melacak; minimum belanja untuk voucher; pertimbangkan free shipping dengan minimum order.
> **Bundle/BOGO:** "Buy 2 serum" untuk menaikkan nilai keranjang.
> **Financial guardrails:** pastikan margin cukup setelah diskon dan biaya platform; hitung LTV:CAC.

(Pesaing tidak menghitung angka apa pun, tidak punya linimasa bertanggal, dan tidak mengenal Shopee Seller Center, harga coret, atau aturan Indonesia. Pesaing kedua (mardab96) hanya menilai promo **setelah** berjalan, dari data harian.)

## Output dengan skill kita
Lihat `01-skincare-1111-shopee.md`.

## Penilaian
| Kriteria | Pesaing (`discount-marketing-strategy`) | Skill kita (`promo-kalender`) |
|---|---|---|
| Kualitas rencana | Kerangka strategi umum (SaaS-sentris: LTD, AppSumo) | Rencana lengkap 7 bagian untuk UMKM |
| Akurasi angka | Tidak ada hitungan | Script terverifikasi 300/300 kombinasi; diskon maksimal, target unit, laba bersih |
| Konteks Indonesia | Tidak ada (BFCM, email marketing) | 9.9–12.12, gajian, Ramadan-Lebaran (label perkiraan), Seller Center, UU 8/1999, UGB |
| Kepatuhan | "Genuine scarcity" disebut, tapi menyarankan countdown | Harga coret jujur, kuota & jam, larangan hitung mundur palsu, undian perlu izin |
| Siap pakai | Perlu diolah lagi | S&K & linimasa siap tempel |
| **Keseluruhan** | – | **Skill kita menang telak** |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Kode voucher unik per kanal** (IG vs TikTok vs WA) untuk mengukur kanal mana yang menghasilkan. Ini bisa masuk bagian "Ukuran evaluasi".
2. **Risiko "melatih pembeli menunggu promo"** (dari pesaing mardab96): tambahkan satu baris peringatan bila pengguna diskon besar setiap bulan, dan cek penjualan harga normal sebelum/sesudah.
3. **Cek penurunan penjualan setelah promo (pull-forward)** pada evaluasi H+7: bandingkan 7 hari setelah promo dengan 7 hari normal.
4. **Pisahkan kenaikan karena iklan vs karena diskon** saat evaluasi, bila anggaran iklan dinaikkan bersamaan.
