# 01 — Hijab di Shopee, target margin 25%

**Skenario:** S1 — permintaan normal. Penjual memberi modal dan biaya platform dari Seller Center-nya sendiri.

**Input pengguna (persis):**
> Aku jual hijab voal, modal 28 ribu udah sama packing. Di Shopee admin aku 8,25%, ikut gratis ongkir xtra 4% maks 20 ribu, biaya proses 1.250 per pesanan. Mau untung 25% dari harga jual. Harga jualnya berapa? Aku belum nyerahin surat pernyataan omzet ke Shopee.

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/harga_marketplace.py --platform "Shopee" --modal 28.000 --admin "8,25" --layanan 4 --maks-layanan 20.000 --per-pesanan 1.250 --target-margin 25
```

## Output

### Shopee - target margin 25% dari harga setelah voucher
- Harga minimal agar tidak rugi: **Rp 33.525**
- Harga tepat sesuai target: Rp 46.988
- **Harga rekomendasi (dibulatkan ke atas kelipatan Rp 500): Rp 47.000**

Rincian pada harga rekomendasi:

| Komponen | Nilai |
|---|---:|
| Harga tayang | Rp 47.000 |
| Biaya admin/komisi (8,25%) | -Rp 3.878 |
| Biaya layanan/program ongkir (4%) | -Rp 1.880 |
| Biaya per pesanan (dibagi 1 barang) | -Rp 1.250 |
| PPh 22 marketplace (0,5%) | -Rp 235 |
| **Uang diterima dari marketplace** | **Rp 39.758** |
| Modal/HPP | -Rp 28.000 |
| **Laba bersih per barang** | **Rp 11.758** |
| Margin (laba / harga setelah voucher) | 25,02% |
| Markup (laba / modal) | 41,99% |

**Catatan & asumsi**
- Persentase biaya platform berasal dari input Anda. Cek angka terbaru di Seller Center masing-masing (berbeda per kategori & program, dan bisa berubah).
- Biaya persen dan PPh 22 dihitung dari harga setelah voucher toko. Jika platform Anda memakai dasar lain, hasil bisa sedikit berbeda.
- Biaya dihitung tanpa pembulatan; angka di tabel dibulatkan ke rupiah terdekat.
- PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke marketplace; hitung ulang dengan --pph22 tidak. PPh 22 ini bukan pajak baru; cara memperhitungkannya dengan PPh final Anda, tanyakan ke DJP/konsultan.
- Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.

💡 Saran:
- Pasang **Rp 47.000**: setelah semua potongan kamu terima Rp 39.758 dan untung bersih **Rp 11.758 per hijab** (margin 25,02%). Di bawah **Rp 33.525** kamu rugi.
- Omzet kamu kalau setahun masih ≤ Rp500 juta dan jualan atas nama pribadi, kamu bisa menyerahkan **surat pernyataan** ke Shopee supaya PPh 22 0,5% (Rp235 per hijab di harga ini) tidak dipotong. Setelah itu minta saya hitung ulang tanpa PPh 22.

## Catatan penguji
- Semua persentase berasal dari pengguna — tidak ada angka karangan. Asumsi dasar biaya (harga setelah voucher) tercantum.
- Angka dicek independen (Fraction): impas 29.250 ÷ 0,8725 = 33.524,4 → Rp33.525; target 29.250 ÷ 0,6225 = 46.987,95 → Rp46.988 → dibulatkan Rp47.000; laba 11.757,50 (tampil Rp11.758). Benar.
- PPh 22 dan pengecualiannya dijelaskan jujur (bersyarat surat pernyataan, OP, omzet ≤ Rp500 juta).
