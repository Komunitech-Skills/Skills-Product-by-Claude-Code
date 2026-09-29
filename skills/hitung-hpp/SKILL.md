---
name: hitung-hpp
description: Menghitung HPP (harga pokok produksi/modal) per unit untuk produk makanan, fashion, kerajinan, maupun jasa dari resep/BOM dengan konversi satuan (beli 1 kg pakai 250 g, yard ke meter, lusin/kodi), tenaga kerja, overhead, kemasan, dan penyusutan alat, lalu menentukan harga jual dari target margin atau markup dan titik impas (BEP unit & rupiah). Gunakan saat pengguna tanya "modal per pcs berapa", "HPP resep", "harga jual yang pas", "BEP", atau cost of goods sold, unit cost, break-even, pricing. Potongan marketplace pakai harga-jual-marketplace.
---

# Hitung HPP, Harga Jual & BEP

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah daftar bahan dan biaya usaha menjadi **HPP per unit yang akurat**, harga jual yang sesuai target, dan jumlah penjualan minimal per bulan agar tidak rugi (BEP) — lengkap dengan rincian yang bisa dicek ulang.

## Kapan digunakan
- "Modal brownies per loyang berapa? Tepung beli 1 kg Rp14.000, pakai 250 g..."
- "Kemeja saya butuh 1,6 m kain (beli per yard), ongkos jahit 35 ribu. HPP dan harga jualnya?"
- "Jasa desain logo: 6 jam kerja, langganan software 400 ribu/bulan. Tarif yang pas?"
- "Harga jual saya 65 ribu, masih untung? BEP-nya berapa per bulan?"

## Kapan TIDAK digunakan
- Harga tayang setelah potongan marketplace → skill `harga-jual-marketplace` (pakai HPP dari sini sebagai modal).
- Laporan laba rugi/neraca → skill `laporan-keuangan-emkm`.
- Penawaran harga ke klien → skill `surat-penawaran-harga`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Bahan: harga beli, isi kemasan beli + satuan, jumlah dipakai + satuan | Ya (produk) | — (tanyakan) |
| Hasil per 1x produksi/resep (batch) | Ya | 1 unit |
| Tenaga kerja (per unit/batch/bulan, atau upah per jam × jam) | Tidak | 0 — sebutkan bahwa upah pemilik belum dihitung |
| Overhead (gas, listrik, sewa…) per unit/batch/bulan | Tidak | 0 |
| Kemasan per unit | Tidak | 0 |
| Alat (harga, umur pakai bulan, nilai sisa) | Tidak | Tidak ada penyusutan |
| Produksi/penjualan per bulan | Wajib bila ada biaya per bulan/alat | — (tanyakan) |
| Biaya tetap lain di luar produksi (admin, internet, marketing) | Tidak | 0 |
| Target margin % **atau** markup %, atau harga jual saat ini | Tidak | Tampilkan pilihan margin 20/30/40/50% |
| Susut/bahan terbuang % | Tidak | 0 |

Jasa: 1 unit = 1 proyek/sesi; isi tenaga kerja (jam × tarif) dan overhead bulanan. Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan).

## Langkah kerja
1. Susun data ke file JSON di folder kerja pengguna, mengikuti `templates/contoh-hpp.json` (format lengkap: `references/format-input.md`). CSV sederhana juga bisa: `templates/contoh-hpp.csv`.
2. Jalankan script (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_hpp.py --file hpp-brownies.json
   python3 <folder-skill-ini>/scripts/hitung_hpp.py --file bahan.csv --hasil-per-batch 16 --produksi-per-bulan 400 --margin 40
   ```
   Opsi: `--margin` / `--markup` (pilih satu), `--harga-jual`, `--bulatkan 1000`, `--susut 5`, `--satuan-produk pcs`, `--format json`.
3. Tampilkan tabel rincian, ringkasan HPP, harga jual, dan BEP dari script **apa adanya**.
4. Jelaskan singkat beda **margin vs markup** bila pengguna menyebut salah satunya, lalu beri 2–3 saran berbasis angka (mis. komponen biaya terbesar, dampak kenaikan harga bahan).
5. Jika ada asumsi (upah pemilik belum dihitung — script otomatis memberi catatan bila tidak ada data tenaga kerja; produksi per bulan diperkirakan), sebutkan di akhir. "Laba kotor" = harga − HPP, belum dikurangi biaya tetap lain di luar HPP.
6. **Fallback tanpa Python:** hitung manual dengan rumus di bawah, tunjukkan tiap langkah, beri tahu bahwa hasil dihitung manual.

## Rumus (untuk hitung manual)
```
Bahan per batch      = harga beli ÷ (isi beli dalam satuan pakai) × jumlah pakai × (1 + susut%)
                       konversi: 1 kg = 1.000 g; 1 ons = 100 g; 1 l = 1.000 ml; 1 m = 100 cm;
                       1 yard = 91,44 cm; 1 lusin = 12; 1 kodi = 20; 1 gross = 144; 1 rim = 500 lembar
Biaya per unit       = biaya per unit | biaya per batch ÷ hasil per batch | biaya per bulan ÷ produksi per bulan
Penyusutan per bulan = (harga alat − nilai sisa) ÷ umur (bulan)       → lalu ÷ produksi per bulan
HPP per unit         = bahan + tenaga kerja + overhead + kemasan + penyusutan (semua per unit)

Harga dari MARGIN m  = HPP ÷ (1 − m)        (margin = laba ÷ harga jual)
Harga dari MARKUP k  = HPP × (1 + k)        (markup = laba ÷ HPP)
  margin m setara markup m ÷ (1 − m); markup k setara margin k ÷ (1 + k)
Harga rekomendasi    = dibulatkan KE ATAS ke kelipatan Rp500 (bisa diubah)

Biaya variabel/unit  = komponen per unit & per batch
Biaya tetap/bulan    = biaya per bulan dalam HPP + penyusutan + biaya tetap lain
BEP unit             = biaya tetap ÷ (harga jual − biaya variabel/unit), dibulatkan ke atas
BEP rupiah           = biaya tetap ÷ ((harga jual − biaya variabel/unit) ÷ harga jual)
```
Pembulatan: rincian ditampilkan 2 desimal; harga rekomendasi dan BEP dibulatkan ke atas agar tidak meremehkan biaya.

## Format output
```
## HPP <produk> (per <satuan>)
| Kategori | Komponen | Cara hitung | Biaya | Per <satuan> |
**Ringkasan HPP** (per kategori, HPP, biaya variabel vs tetap)
**Harga jual** (rumus + harga rekomendasi + laba, margin, markup)  ← atau tabel pilihan margin
**BEP per bulan** (biaya tetap, margin kontribusi, BEP unit & rupiah, % dari rencana produksi)
**Catatan & asumsi**
💡 Saran: <2–3 poin berbasis angka>
```

## Contoh
**Input pengguna:** "Brownies 1 resep jadi 2 loyang. Tepung 1 kg 14 rb pakai 250 g, gula 1 kg 18 rb pakai 300 g, telur 30 rb isi 16 pakai 6, coklat 250 g 25 rb pakai 200 g, mentega 200 g 12 rb pakai 150 g. Upah 15 rb/jam, 2 jam per resep. Gas 5 rb per resep, listrik 150 rb/bulan. Box 250 rb isi 100, stiker 500. Oven 3,6 jt umur 3 tahun. Internet 300 rb/bulan. Produksi 120 loyang/bulan, mau margin 40%."

**Output (dari `templates/contoh-hpp.json`, dipersingkat):**
```
- Bahan baku: Rp 24.575 | Tenaga kerja: Rp 15.000 | Overhead: Rp 3.750 | Kemasan: Rp 3.000 | Penyusutan: Rp 833,33
- **HPP per loyang: Rp 47.158,33** (variabel Rp 45.075 + tetap dialokasikan Rp 2.083,33)
- Target margin 40% -> harga = HPP / (1 - 40%) = Rp 78.597,22 (setara markup 66,67%)
- **Harga rekomendasi: Rp 79.000** -> laba kotor Rp 31.841,67 per loyang (margin 40,31%; belum dikurangi biaya tetap lain)
- Biaya tetap bulanan Rp 550.000; margin kontribusi Rp 33.925/loyang
- **BEP: 17 loyang per bulan**, atau omzet **Rp 1.280.767** per bulan (13,51% dari rencana produksi)
💡 Dark chocolate (Rp 10.000/loyang) adalah bahan termahal; harga naik 10% menambah HPP Rp 1.000.
```

## Checklist sebelum mengirim hasil
- [ ] Satuan beli & pakai sudah dikonversi dengan benar (atau pengguna diminta menyamakan satuan).
- [ ] Biaya per bulan dan penyusutan dibagi produksi per bulan; biaya tetap tidak dihitung ganda di BEP.
- [ ] Margin dan markup tidak tertukar; keduanya ditampilkan setaranya.
- [ ] Harga rekomendasi dibulatkan ke atas; laba & margin pada harga itu ditampilkan.
- [ ] Asumsi (upah pemilik, produksi per bulan) disebut. Format Rupiah `Rp 1.250.000`.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila: satuan tidak dikenal (mis. sdm, sachet berbeda), satuan beda jenis (liter ke gram), `pakai` kosong, biaya negatif, `produksi_per_bulan` kosong padahal ada biaya bulanan/alat, margin ≥ 100%, margin dan markup diisi bersamaan, atau JSON/CSV rusak. Sampaikan dengan bahasa sederhana dan minta data yang dibutuhkan.
- Sendok/cangkir tidak dikonversi otomatis; minta pengguna menimbang (gram/ml) atau menyamakan satuan beli dan pakai.
- HPP bergantung pada produksi per bulan; bila penjualan nyata lebih rendah, HPP per unit naik — ingatkan pengguna.
- Bukan perhitungan pajak dan bukan laporan keuangan resmi.
