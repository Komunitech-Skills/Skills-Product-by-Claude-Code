# 00 — Uji A/B: S1 tanpa skill vs dengan skill

**Input (sama dengan S1):** kopi robusta 250 g, modal Rp 32.000 + kemasan Rp 2.000, eceran Rp 79.000, dropshipper/reseller min. 10/agen min. 50 dengan diskon 15/25/35%, reseller jualan di Shopee/TikTok (potongan ±10%), ongkir ke reseller Rp 1.500/bungkus, diskon ke konsumen maks. 5%. Minta price list, S&K, dan pesan rekrut.

## A. Tanpa skill (agent umum)
> **Price List Reseller Kopi Robusta 250 g**
> | Tier | Min. order | Diskon | Harga |
> |---|---|---|---|
> | Dropshipper | 1 pcs | 15% | Rp 67.150 |
> | Reseller | 10 pcs | 25% | Rp 59.250 |
> | Agen | 50 pcs | 35% | Rp 51.350 |
>
> Keuntungan reseller: Rp 79.000 − Rp 59.250 = Rp 19.750 per bungkus (25%). Keuntungan kamu per bungkus di tier agen: Rp 51.350 − Rp 34.000 = Rp 17.350. **Semua tier aman.**
>
> **Syarat & Ketentuan:**
> 1. Minimal order sesuai tier.
> 2. Pembayaran di muka.
> 3. Harga jual minimal Rp 75.000. Pelanggaran akan dikenakan sanksi tegas.
> 4. Retur hanya untuk barang rusak.
>
> **Pesan rekrut:** "Yuk jadi reseller kopi kami! Untung sampai 35% per bungkus, modal kecil, cocok buat penghasilan tambahan! Daftar sekarang!"

## B. Dengan skill `katalog-reseller`
Lihat `01-kopi-bubuk-3-tier.md`.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Harga tier | Rp 67.150 dll. (tidak dibulatkan) | Dibulatkan ke bawah ke Rp 100, sehingga diskon mitra tidak pernah kurang dari janji |
| Untung mitra | Rp 19.750 (25%). **Salah**, karena mengabaikan potongan marketplace 10% & ongkir Rp 1.500 yang **disebut pengguna** | Rp 10.400 (13,2%) → ditandai TIPIS dan diperbaiki menjadi Rp 14.300 (18,1%) |
| Dropshipper | "Aman" | Untung hanya Rp 2.500–4.000, dan **rugi** bila dijual di harga minimum. Diperbaiki ke diskon 20% |
| Harga minimum | Disebut, dengan "sanksi tegas" yang kabur | Rp 75.000 anjuran + konsekuensi kebijakan bertahap, tanpa denda; dasar UU 5/1999 |
| Pemisahan data | Margin produsen dicampur ke daftar untuk mitra | Tabel internal terpisah + CSV siap kirim tanpa HPP |
| S&K | 4 butir | 14 butir (dropship, pembayaran aman, retur, foto/merek/klaim, data konsumen, penghentian) |
| Pesan rekrut | "Untung sampai 35%": **menyesatkan** (diskon ≠ untung), tanpa opt-out | Contoh untung jujur "±Rp 143.000 jika semua terjual di harga eceran", gratis pendaftaran, opt-out STOP |
| Anti-piramida | Tidak dibahas | Tegas: tanpa biaya daftar & bonus rekrut |

## Penilaian
Skill **jelas lebih baik**. Kesalahan utama agent tanpa skill adalah menyatakan "semua tier aman" dan menjanjikan "untung sampai 35%", padahal setelah potongan marketplace dan ongkir, untung dropshipper hanya ±3%. Justru itu masalah yang ingin dicegah pengguna. Skill memberi angka bersih, perbaikan terukur, dan dokumen yang patuh hukum.
