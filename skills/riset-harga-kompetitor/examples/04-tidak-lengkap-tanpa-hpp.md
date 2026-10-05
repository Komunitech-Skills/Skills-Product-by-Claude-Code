# Uji 04 (input tidak lengkap) - tanpa HPP

**Input pengguna:**
> Harga pasaran kopi gayo bubuk 250 gr berapa ya? Ini 5 toko pesaing: [teks tempelan 5 produk, ukuran 200 g - 500 g].

## Perilaku agent (mengikuti SKILL.md)
Data pesaing ada, HPP tidak ada, biaya marketplace tidak ada. SKILL.md: "tanyakan sekali dalam satu pesan bernomor (maks. 5)" dan "jangan mengarang HPP".

Percobaan menjalankan script tanpa HPP:
```
ERROR: HPP/modal per barang belum diisi. Tanyakan ke pengguna (atau hitung dengan skill hitung-hpp).
(exit code 2)
```

Balasan agent:
> Data 5 pesaing sudah saya catat. Supaya saya bisa kasih harga yang tetap untung, saya perlu 4 info singkat:
> 1. Modal (HPP) per bungkus 250 gr, sudah termasuk kemasan? (Kalau belum tahu, saya bisa bantu hitung dengan skill `hitung-hpp`.)
> 2. Jualan di mana? Kalau di Shopee/Tokopedia/TikTok Shop, berapa persen biaya admin, gratis ongkir, dan biaya proses per pesanan? (Kalau tidak diisi, saya anggap 0% = jualan langsung.)
> 3. Target untung berapa persen dari harga jual? (Default 20%.)
> 4. Harga jual kamu sekarang berapa? (Opsional.)

## Catatan penguji
- Sesuai aturan: tidak mengarang HPP, pertanyaan sekali, bernomor, ≤ 5, default disebut. ✓
- **Celah (T5):** pertanyaan pengguna murni "harga pasaran berapa". Script menolak jalan tanpa HPP sehingga ringkasan pasar (terendah/P25/median/P75, per 100 g) yang sebenarnya sudah bisa dijawab **tertunda**. Setelah HPP diisi (uji: `--hpp 30.000`), ringkasan pasar keluar: terendah Rp 48.000, P25 Rp 53.125, median Rp 54.750, P75 Rp 54.900, tertinggi Rp 80.000 (setara 250 g, 5 pesaing). Usul: mode "pasar saja" bila HPP kosong (statistik & tabel ditampilkan, bagian batas harga/rekomendasi diganti pertanyaan HPP).
- Perilaku error lain yang diuji: `--hpp 0`, `--hpp abc`, biaya+margin ≥ 100%, ukuran "sebungkus", `--biaya-persen 120`, file tidak ada, `--tanggal kemarin`, `--harga-kita 49,9` -> semuanya `ERROR:` jelas, exit 2. ✓

**Penilaian skenario:** lulus (aman), dengan usulan perbaikan UX.
