# 02 — "bikinin dong", pakai angka contoh (bandingkan Tokopedia & TikTok Shop)

**Skenario:** S2 — permintaan singkat/malas. Pengguna tidak tahu biaya platform dan minta pakai angka contoh.

**Input pengguna (persis):**
> bikinin dong harga jual tumbler modal 45rb buat di tokped sama tiktok. aku ga tau biaya adminnya, pake angka contoh aja dulu

**Yang dilakukan agent:** menyalin `templates/platform-contoh.json` ke folder kerja sebagai `platform.json`, mengganti `modal` menjadi 45.000, memakai baris Tokopedia & TikTok Shop saja (target default margin 20%).
```bash
python3 <folder-skill>/scripts/harga_marketplace.py --config platform.json
```

## Output

> ⚠️ **SEMUA PERSENTASE BIAYA DI BAWAH ADALAH ANGKA CONTOH**, bukan tarif resmi Tokopedia/TikTok Shop. Biaya asli berbeda per kategori, jenis toko, program, dan sering berubah. Cek angka terbaru di Seller Center kamu, lalu minta saya hitung ulang.

## Perbandingan harga per platform

| Platform | Harga minimal (impas) | Harga rekomendasi | Laba/barang | Margin |
|---|---:|---:|---:|---:|
| Tokopedia (contoh - cek Seller Center) | Rp 51.686 | Rp 67.000 | Rp 13.630 | 20,34% |
| TikTok Shop (contoh - cek Seller Center) | Rp 52.926 | Rp 68.500 | Rp 13.242 | 20,35% |

### Tokopedia (contoh - cek Seller Center) - target margin 20% dari harga setelah voucher
- Harga minimal agar tidak rugi: **Rp 51.686**
- Harga tepat sesuai target: Rp 66.667
- **Harga rekomendasi (dibulatkan ke atas kelipatan Rp 500): Rp 67.000**

Rincian pada harga rekomendasi:

| Komponen | Nilai |
|---|---:|
| Harga tayang | Rp 67.000 |
| Biaya admin/komisi (6,5%) | -Rp 4.355 |
| Biaya layanan/program ongkir (4%) | -Rp 2.680 |
| Biaya per pesanan (dibagi 1 barang) | -Rp 1.000 |
| PPh 22 marketplace (0,5%) | -Rp 335 |
| **Uang diterima dari marketplace** | **Rp 58.630** |
| Modal/HPP | -Rp 45.000 |
| **Laba bersih per barang** | **Rp 13.630** |
| Margin (laba / harga setelah voucher) | 20,34% |
| Markup (laba / modal) | 30,29% |

### TikTok Shop (contoh - cek Seller Center) - target margin 20% dari harga setelah voucher
- Harga minimal agar tidak rugi: **Rp 52.926**
- Harga tepat sesuai target: Rp 68.157
- **Harga rekomendasi (dibulatkan ke atas kelipatan Rp 500): Rp 68.500**

Rincian pada harga rekomendasi:

| Komponen | Nilai |
|---|---:|
| Harga tayang | Rp 68.500 |
| Voucher toko | -Rp 3.425 |
| Harga setelah voucher | Rp 65.075 |
| Biaya admin/komisi (7%) | -Rp 4.555 |
| Biaya layanan/program ongkir (3%) | -Rp 1.952 |
| PPh 22 marketplace (0,5%) | -Rp 325 |
| **Uang diterima dari marketplace** | **Rp 58.242** |
| Modal/HPP | -Rp 45.000 |
| **Laba bersih per barang** | **Rp 13.242** |
| Margin (laba / harga setelah voucher) | 20,35% |
| Markup (laba / modal) | 29,43% |

**Catatan & asumsi**
- Persentase biaya platform berasal dari input Anda. Cek angka terbaru di Seller Center masing-masing (berbeda per kategori & program, dan bisa berubah).
- Biaya persen dan PPh 22 dihitung dari harga setelah voucher toko. Jika platform Anda memakai dasar lain, hasil bisa sedikit berbeda.
- Biaya dihitung tanpa pembulatan; angka di tabel dibulatkan ke rupiah terdekat.
- PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke marketplace; hitung ulang dengan --pph22 tidak. PPh 22 ini bukan pajak baru; cara memperhitungkannya dengan PPh final Anda, tanyakan ke DJP/konsultan.
- Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.

**Asumsi yang dipakai:** target margin 20% dari harga setelah voucher (kamu belum menyebut target); modal Rp45.000 sudah termasuk kemasan; TikTok Shop contoh memakai voucher toko 5% maks Rp5.000. Status TikTok Shop sebagai pemungut PPh 22 **belum terverifikasi** — PPh 22 tetap dimasukkan sebagai perhitungan aman (konservatif).

💡 Saran: dengan angka contoh ini harga Tokopedia dan TikTok Shop hanya selisih Rp1.500; voucher 5% di TikTok Shop "memakan" Rp3.425 per barang. Setelah dapat angka asli dari Seller Center, bandingkan lagi.

## Catatan penguji
- Label "contoh — cek Seller Center" muncul di nama platform (dari template) dan agent menambahkan peringatan tebal di atas. Sesuai aturan "jangan mengarang persentase".
- **Kurang:** catatan script tetap berbunyi "Persentase biaya platform berasal dari input Anda" padahal dari template contoh — kontradiktif; agent harus menambal dengan peringatan manual.
- **Kurang:** script memotong PPh 22 untuk TikTok Shop tanpa catatan, padahal referensi menandai TikTok Shop BELUM TERVERIFIKASI sebagai pemungut; agent menambahkan kalimatnya sendiri.
- Angka dicek independen: TikTok S = 45.000 ÷ 0,695 = 64.748,2; P = S ÷ 0,95 = 68.156,0 → Rp68.157 → Rp68.500. Tokopedia 45.000 ÷ 0,675 = 66.666,7 → Rp66.667 → Rp67.000. Benar.
