---
name: katalog-reseller
description: Menyusun program mitra untuk produsen/brand UMKM — daftar harga bertingkat dropshipper/reseller/agen per jumlah beli (dihitung script dari HPP atau harga eceran), cek untung tersisa untuk mitra dengan peringatan bila tipis, S&K kemitraan (minimal order, bayar, retur, harga minimum, foto), dan pesan rekrut jujur tanpa skema piramida. Gunakan saat diminta price list reseller/agen, buka dropshipper, reseller program, tier pricing. Harga marketplace pakai harga-jual-marketplace.
---

# Katalog & Program Reseller

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu produsen/pemilik brand membuka jaringan mitra yang **sehat**: harga bertingkat yang tetap menguntungkan produsen, untung mitra yang cukup untuk bertahan (tanpa terpaksa banting harga), aturan main yang jelas, dan ajakan rekrut yang jujur — tanpa bonus rekrut berjenjang.

## Kapan digunakan
- "Bikinin daftar harga reseller & agen untuk produk saya", "harga dropship berapa yang pas?"
- Menyusun syarat & ketentuan reseller (minimal order, retur, larangan banting harga, penggunaan foto).
- Membuat pesan/caption ajakan jadi reseller.
- Mengecek apakah struktur harga mitra yang sudah ada masih masuk akal.

## Kapan TIDAK digunakan
- Menentukan harga jual di marketplace & potongan platform → `harga-jual-marketplace`; HPP dari bahan → `hitung-hpp`.
- Penawaran harga resmi ke satu klien B2B → `surat-penawaran-harga`; proposal kerja sama dengan perusahaan/toko → `proposal-kerjasama`.
- Perjanjian kemitraan bertanda tangan → `perjanjian-sederhana`.
- **Skema bonus rekrut berjenjang/MLM/"passive income dari downline"** → tolak dengan sopan (lihat Batasan).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Produk + HPP/modal per unit | Ya | — (tanyakan; belum tahu → tawarkan `hitung-hpp`) |
| Harga eceran anjuran ke konsumen | Tidak | Diusulkan script dari tier termahal agar mitra tier itu dapat 20% **bersih** setelah biaya jual & ongkir (sebut sebagai usulan) |
| Tier: nama, minimal beli, diskon dari eceran (atau target margin produsen) | Tidak | Contoh: Dropshipper 1 pcs, Reseller 12 pcs, Agen 60 pcs; diskon 20/25/35% (mode eceran) atau margin produsen 45/35/25% (mode HPP) |
| Mitra jualan di marketplace? perkiraan % potongan | Tidak | 0% (script mengingatkan untung bersih mitra lebih kecil) |
| Batas diskon ke konsumen yang masih diizinkan | Tidak | 0% (harga minimum = harga eceran) |
| Ongkir ke mitra, pembayaran, retur, wilayah | Tidak | Mitra tanggung ongkir; lunas sebelum kirim; retur hanya cacat/salah kirim 3 hari dengan video unboxing |
| Nama brand & kanal rekrut (WA/IG/TikTok) | Tidak | "<nama brand>"; versi WA + caption |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, pakai default dan tulis asumsinya.

## Langkah kerja
1. **Pilih mode hitung.** Sudah punya harga eceran → mode `diskon` (harga mitra = eceran × (1 − diskon)). Belum punya harga eceran atau ingin menjamin margin produsen → mode `margin` (harga mitra = modal ÷ (1 − target margin)).
2. **Jalankan script** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_tier.py --produk "Serum 20ml" --hpp 28.000 --eceran 89.000 \
     --tier "Dropshipper:1:15" --tier "Reseller:12:25" --tier "Agen:60:35" \
     --biaya-jual-mitra 10 --maks-diskon-konsumen 5
   python3 <folder-skill-ini>/scripts/hitung_tier.py --produk "Kopi 250g" --hpp 32.000 --mode margin \
     --tier "Dropshipper:1:45" --tier "Reseller:12:35" --tier "Agen:60:25"
   # banyak produk: --config produk.json (contoh: templates/produk-contoh.json / .csv)
   # daftar harga untuk dibagikan ke mitra (tanpa HPP & margin produsen): --csv-keluar daftar-harga-mitra.csv
   ```
   Opsi lain: `--biaya-produsen` (packing/label per unit), `--ongkir-ke-mitra` (Rp/unit; otomatis **tidak** dikenakan ke tier yang namanya mengandung "drop", karena dropshipper tidak menerima kiriman stok), `--min-margin-mitra 15`, `--min-margin-dropship 10`, `--min-margin-produsen 15`, `--bulatkan 100`, `--format json`. Tier boleh punya batas sendiri: `"Agen:60:35:20"`.
3. **Baca status & peringatan.** Jangan menyajikan tier berstatus `PRODUSEN RUGI`, `MITRA RUGI`, atau `HARGA MITRA ≥ ECERAN` sebagai final. Untuk `MARGIN MITRA TIPIS` / `RUGI DI HARGA MINIMUM` / selisih tier terlalu kecil: jalankan ulang dengan usulan perbaikan (diskon tier lebih besar, harga eceran lebih tinggi, tier dikurangi) dan tampilkan perbandingannya.
4. **Susun dokumen** dengan format di bawah: tabel internal (dengan margin produsen) **terpisah** dari daftar harga untuk mitra (tanpa HPP/margin produsen).
5. **Syarat & ketentuan** dari `references/syarat-kemitraan.md`; harga minimum ditulis sebagai "anjuran" + konsekuensi kebijakan kemitraan (bukan denda) sesuai `references/regulasi.md`.
6. **Pesan rekrut** dari `templates/pesan-rekrut.md` memakai contoh untung dari script (dengan "±" dan "jika terjual di harga eceran").
7. **Fallback tanpa Python:** hitung manual dengan rumus di bawah, tunjukkan langkahnya, dan tulis "dihitung manual, belum diverifikasi script".

## Rumus (untuk hitung manual)
M = HPP + biaya produsen per unit, E = harga eceran anjuran, d = diskon tier, m = target margin produsen, f = % biaya jual mitra, O = ongkir ke mitra per unit.
```
Mode diskon : harga mitra = E × (1 − d)          → bulatkan KE BAWAH ke kelipatan Rp 100
Mode margin : harga mitra = M ÷ (1 − m)          → bulatkan KE ATAS ke kelipatan Rp 100
Margin produsen   = (harga mitra − M) ÷ harga mitra
Untung mitra/unit = E − harga mitra − E×f − O     (% = ÷ E; O = 0 untuk dropshipper)
Harga minimum     = E × (1 − maks diskon konsumen) → bulatkan ke bawah ke kelipatan Rp 100
Eceran usulan     = (harga tier termahal + O) ÷ (1 − target untung mitra − f) → bulatkan KE ATAS ke Rp 1.000
(O = 0 untuk dropshipper)
Contoh untung paket = untung mitra/unit × minimal beli
```
Contoh: E = Rp 89.000, d = 25% → Rp 66.750 → Rp 66.700; f = 10% → untung mitra Rp 89.000 − 66.700 − 8.900 = Rp 13.400 (15,1%); HPP Rp 28.000 → margin produsen Rp 38.700 (58,0%).

## Format output
```
# Program Mitra <brand>

## 1. Struktur harga (INTERNAL — jangan dibagikan)
| Produk | Tier | Min. beli | Harga mitra | Diskon | Margin produsen | Untung mitra/unit | Status |
+ peringatan script & perbaikan yang disarankan (dengan angka hasil hitung ulang)

## 2. Daftar harga mitra (siap kirim)
| Produk | Harga eceran anjuran | Dropshipper (1 pcs) | Reseller (≥12) | Agen (≥60) |
Harga minimum anjuran; contoh modal & untung per paket minimal.

## 3. Syarat & ketentuan kemitraan (siap tempel, bernomor)

## 4. Pesan ajakan rekrut
WA broadcast • caption IG/TikTok • status singkat

**Asumsi & catatan:** mode hitung, pembulatan, % biaya jual mitra (sumber), dasar aturan (per 23 Sep 2026), disclaimer.
```

## Contoh
**Input pengguna:** "Saya produksi serum, modal 28 ribu, jual eceran 89 ribu. Mau buka dropshipper, reseller min 12, agen min 60. Kebanyakan reseller jualan di Shopee."

**Output (dipersingkat):**
```
| Tier | Min. beli | Harga mitra | Diskon | Margin produsen | Untung mitra/unit* | Status |
| Dropshipper | 1 | Rp 75.600 | 15,1% | Rp 47.600 (63,0%) | Rp 4.500 (5,1%) | ⚠️ MARGIN MITRA TIPIS |
| Reseller | 12 | Rp 66.700 | 25,1% | Rp 38.700 (58,0%) | Rp 13.400 (15,1%) | ✅ |
| Agen | 60 | Rp 57.800 | 35,1% | Rp 29.800 (51,6%) | Rp 22.300 (25,1%) | ✅ |
*setelah perkiraan potongan marketplace 10% (contoh — cek Seller Center mitra)
Saran: naikkan diskon dropshipper ke 22% → harga Rp 69.400, untung dropshipper Rp 10.700 (12,0%).
Pesan WA: "...Reseller beli 12 pcs (modal ±Rp 800.400), jika semua terjual di harga eceran, untung ±Rp 160.800..."
```

## Checklist sebelum mengirim hasil
- [ ] Semua harga & untung berasal dari script (atau hitung manual yang disebut); tidak ada tier rugi yang disajikan final.
- [ ] Tabel internal (HPP, margin produsen) terpisah dari daftar harga untuk mitra.
- [ ] Tier ditentukan dari jumlah beli sendiri; **tidak ada** bonus rekrut, biaya pendaftaran berbayar, atau komisi downline.
- [ ] "Larangan banting harga" ditulis sebagai harga minimum anjuran + konsekuensi kebijakan, bukan denda.
- [ ] Pesan rekrut memakai "±" & "jika terjual di harga eceran"; tanpa "pasti untung"/"passive income"; ada opt-out.
- [ ] Tidak ada klaim produk (BPOM, halal, manfaat) yang tidak diberikan pengguna.
- [ ] % biaya jual mitra diberi label sumber/contoh; format Rupiah `Rp 1.250.000`; disclaimer ada.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila HPP kosong/≤ 0, format tier salah (`Nama:min_beli:nilai`), persen di luar 0–100, nama tier kembar, atau mode diskon tanpa harga eceran. Jelaskan dan minta data yang benar.
- **Skema piramida dilarang** (UU 7/2014 Pasal 9, ancaman pidana Pasal 105). Jika pengguna meminta bonus dari merekrut/downline/biaya pendaftaran sebagai sumber untung: tolak bagian itu, jelaskan singkat, tawarkan alternatif sah (diskon volume, bonus barang untuk pembelian sendiri, komisi afiliasi satu tingkat dari penjualan produk nyata). MLM resmi butuh izin penjualan langsung dan di luar cakupan skill.
- Penetapan harga jual kembali bisa bermasalah secara hukum persaingan usaha untuk usaha yang lebih besar (UU 5/1999 Pasal 8; usaha kecil dikecualikan Pasal 50 huruf h) — lihat `references/regulasi.md`, sarankan konsultasi hukum untuk jaringan besar.
- Hitungan per unit; biaya iklan mitra, retur, dan pajak mitra tidak dimodelkan. Ini alat bantu, bukan nasihat hukum/pajak.
