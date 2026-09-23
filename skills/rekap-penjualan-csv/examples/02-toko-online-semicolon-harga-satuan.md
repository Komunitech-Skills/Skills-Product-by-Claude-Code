# Contoh 02 – Toko online busana muslim, pemisah titik koma, harga satuan

## Skenario
S2, permintaan normal. Ekspor pesanan toko online sebulan: pemisah `;`, tanggal+jam `2026-08-01 12:27`, harga satuan berformat Indonesia dengan desimal (`68.500,00`). Tidak ada kolom total, jadi dipakai `--kolom-harga`.

## Input pengguna
```
Min, ini laporan pesanan toko online aku bulan Agustus. Tolong rekapin omzetnya berapa, produk mana yang paling nyumbang, sama kasih saran buat bulan depan dong.
```
Cuplikan file:
```
No. Pesanan;Waktu Pesanan Dibuat;Nama Produk;Jumlah;Harga Satuan
260900001;2026-08-01 12:27;Hijab Segi Empat Voal;2;35.000,00
260900002;2026-08-01 19:29;Khimar Syari Jersey;1;68.500,00
```

## Output

## Rekap Penjualan 1 – 30 Agustus 2026

**Total omzet:** Rp 13.899.100
**Jumlah transaksi (baris):** 88
**Rata-rata omzet per hari:** Rp 463.303 (30 hari, semuanya ada penjualan)

> Catatan: file berakhir di 30 Agustus. Tanggal 31 Agustus tidak ada di data. Omzet dihitung dari *Harga Satuan × Jumlah* dan belum dikurangi diskon, ongkir, atau potongan biaya marketplace.

### 5 Produk Terlaris (omzet)
| # | Produk | Qty | Omzet | % |
|---|---|---|---|---|
| 1 | Gamis Katun Rayon Motif Bunga | 46 | Rp 6.670.000 | 48,0% |
| 2 | Mukena Travel Parasut | 29 | Rp 3.767.100 | 27,1% |
| 3 | Khimar Syari Jersey | 27 | Rp 1.849.500 | 13,3% |
| 4 | Hijab Segi Empat Voal | 35 | Rp 1.225.000 | 8,8% |
| 5 | Bros Mutiara | 31 | Rp 387.500 | 2,8% |

### Tren harian
Hari terbaik: Sabtu, 29 Agustus 2026 (Rp 1.328.200). Hari terendah: Jumat, 7 Agustus 2026 (Rp 12.500).

Rata-rata omzet Sabtu–Minggu Rp 519.150 per hari, sedangkan Senin–Jumat Rp 435.380 per hari. Tiga hari tertinggi: 29 Agustus (Rp 1.328.200), 10 Agustus (Rp 1.015.000), dan 30 Agustus (Rp 958.400).

### Insight
1. **Gamis Katun Rayon Motif Bunga menyumbang hampir setengah omzet (48,0%).** Ini produk andalan, jadi jangan sampai kehabisan stok. Tambah 1–2 motif baru untuk bulan depan. Di sisi lain, ketergantungan pada satu produk berisiko, jadi Mukena Travel (27,1%) layak didorong sebagai andalan kedua.
2. **Hijab Voal dan Bros laku banyak tapi omzetnya kecil.** Hijab 35 pcs (qty terbanyak ke-2) hanya 8,8% omzet, dan Bros 31 pcs hanya 2,8%. Jadikan keduanya pelengkap: misalnya paket "Gamis + Hijab Voal" atau "gratis/diskon Bros untuk pembelian Gamis", supaya nilai per pesanan naik.
3. **Akhir pekan lebih ramai.** Rata-rata Sabtu–Minggu sekitar 19% lebih tinggi dari hari kerja, dan hari terbaik jatuh di Sabtu 29 Agustus. Jadwalkan live, voucher, atau posting produk baru di Jumat malam sampai Minggu.

## Catatan penguji
- Perintah: `python3 <skill>/scripts/rekap.py toko-agustus.csv --kolom-tanggal "Waktu Pesanan Dibuat" --kolom-produk "Nama Produk" --kolom-qty "Jumlah" --kolom-harga "Harga Satuan"`. Delimiter `;` dan format `68.500,00` terdeteksi otomatis dengan benar.
- **Verifikasi independen:** dihitung ulang dengan Python terpisah (parser sendiri untuk `68.500,00`). Total Rp 13.899.100, 88 baris, top-5, dan hari terbaik/terendah **cocok 100%**.
- Bagus: `--kolom-harga` (harga × qty) bekerja. Tanggal dengan jam terbaca.
- Kurang (sedang): SKILL.md menyebut ekspor Shopee/Tokopedia, tetapi script **tidak bisa menyaring status pesanan** (Batal/Dikembalikan). Pada ekspor marketplace asli, pesanan batal akan ikut terhitung sebagai omzet tanpa peringatan. File uji ini sengaja tidak memuat kolom status.
- Catatan: "sekitar 19%" adalah angka turunan (519.150 ÷ 435.380).
