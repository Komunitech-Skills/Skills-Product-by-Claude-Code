---
name: harga-jual-marketplace
description: Menghitung harga jual minimal (balik modal) dan harga rekomendasi di Shopee, Tokopedia, TikTok Shop, dll. agar target margin/laba tercapai setelah biaya admin, gratis ongkir, pembayaran, biaya per pesanan, voucher toko, dan PPh 22 marketplace 0,5%; plus mode kebalikan (harga jual ke untung bersih) dan perbandingan antar-platform. Gunakan saat pengguna tanya "harga jual di Shopee berapa biar untung", "potongan marketplace", "untung bersih per produk", atau marketplace pricing, seller fee calculator. Menghitung HPP/modal pakai hitung-hpp; menulis deskripsi produk pakai listing-marketplace.
---

# Harga Jual Marketplace

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menjawab pertanyaan penjual online: "Berapa harga yang harus saya pasang supaya setelah semua potongan marketplace saya tetap untung sesuai target?" — dan sebaliknya, "Kalau saya jual segini, untung bersih saya berapa?"

## Kapan digunakan
- Menentukan harga tayang produk baru di Shopee/Tokopedia/TikTok Shop/Lazada/dll.
- Mengecek apakah harga sekarang masih untung setelah biaya admin naik atau ikut program gratis ongkir.
- Membandingkan harga ideal di beberapa platform sekaligus.
- Menghitung dampak voucher toko terhadap laba.

## Kapan TIDAK digunakan
- Menghitung modal/HPP dari resep atau bahan → skill `hitung-hpp` dulu, lalu hasilnya dipakai di sini.
- Menulis judul/deskripsi produk → skill `listing-marketplace`.
- PPh final UMKM bulanan → skill `pph-final-umkm`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Modal/HPP per barang (termasuk kemasan) | Ya | — (tanyakan; tawarkan skill `hitung-hpp`) |
| Biaya admin/komisi (%) per platform | Ya | — (minta pengguna cek Seller Center) |
| Biaya layanan / program gratis ongkir / cashback (%) + batas maksimum (Rp) | Tidak | 0 (tanyakan apakah ikut program) |
| Biaya pembayaran/transaksi (%) | Tidak | 0 |
| Biaya tetap per pesanan (Rp) & rata-rata barang per pesanan | Tidak | 0 & 1 |
| Voucher toko (% atau Rp, + maks.) | Tidak | Tidak ada |
| Status PPh 22: sudah menyerahkan surat pernyataan/SKB? | Tidak | Belum → PPh 22 0,5% dipotong |
| Target: margin %, laba Rp per barang, atau markup % | Tidak | Margin 20% dari harga setelah voucher (sebut asumsinya) |
| Harga jual saat ini (untuk mode cek) | Tidak | — |

**Jangan mengarang persentase biaya platform.** Angka berbeda per kategori, program, dan waktu. Minta pengguna mengisi dari Seller Center. Jika pengguna hanya ingin gambaran, boleh pakai angka di `templates/platform-contoh.json` tetapi **wajib** diberi label "contoh — cek angka terbaru di Seller Center". Template itu berisi `"angka_contoh": true`, sehingga script mencetak peringatan **ANGKA CONTOH** di baris pertama; peringatan itu wajib ikut ditampilkan ke pengguna. Saat membuat file JSON dengan angka asli pengguna, hapus kunci `angka_contoh`.

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan).

## Langkah kerja
1. Kumpulkan modal dan biaya tiap platform. Satu platform → pakai argumen; beberapa platform → buat file JSON seperti `templates/platform-contoh.json` di folder kerja pengguna.
2. Jalankan script (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   # Cari harga (target margin 20%)
   python3 <folder-skill-ini>/scripts/harga_marketplace.py --platform "Shopee" --modal 35.000 \
     --admin 8 --layanan 4 --maks-layanan 10.000 --per-pesanan 1.250 --target-margin 20
   # Cek laba dari harga yang sudah ada (mode kebalikan)
   python3 <folder-skill-ini>/scripts/harga_marketplace.py --platform "Shopee" --modal 35.000 \
     --admin 8 --layanan 4 --harga-jual 59.900
   # Bandingkan beberapa platform
   python3 <folder-skill-ini>/scripts/harga_marketplace.py --config platform.json
   ```
   Opsi lain: `--pembayaran`, `--iklan` (%), `--voucher 10%` / `--voucher 5000`, `--maks-voucher`, `--qty-per-pesanan`, `--biaya-lain` (Rp/barang), `--target-laba`, `--target-markup`, `--pph22 tidak`, `--bulatkan 1000` (kelipatan pembulatan, default 500), `--format json`.
3. Sajikan hasil: harga minimal, harga rekomendasi, dan tabel rincian dari script **apa adanya**. Tambahkan 1–2 saran praktis berbasis angka (mis. "voucher 10% menurunkan laba Rp3.500/barang").
4. Selalu sertakan catatan asumsi dari script (dasar biaya, sumber persentase, PPh 22).
5. **Fallback tanpa Python:** hitung manual dengan rumus di bawah dan beri tahu bahwa hasil dihitung manual.

## Rumus (untuk hitung manual)
Notasi per barang: P = harga tayang, V = voucher toko, S = P − V (harga setelah voucher), M = modal, F = biaya per pesanan ÷ barang per pesanan, L = biaya lain, a/l/b/i = persen admin/layanan/pembayaran/iklan, t = 0,5% PPh 22 (0 bila dikecualikan).
```
potongan persen   = S × (a + l + b + i)       ← tiap komponen dibatasi "maks" bila ada
PPh 22            = S × 0,5%
uang diterima     = S − potongan persen − F − PPh 22
laba bersih       = uang diterima − M − L
margin            = laba ÷ S      markup = laba ÷ M
```
Tanpa batas maksimum dan tanpa voucher (S = P), harga yang memenuhi target:
```
Balik modal     : P = (M + F + L) ÷ (1 − a − l − b − i − t)
Target margin m : P = (M + F + L) ÷ (1 − a − l − b − i − t − m)
Target laba Rp  : P = (M + F + L + laba) ÷ (1 − a − l − b − i − t)
Voucher Rp V    : hitung S dengan rumus di atas, lalu P = S + V
Voucher persen v: P = S ÷ (1 − v)
```
Bulatkan harga **ke atas** ke rupiah penuh, lalu ke atas ke kelipatan pembulatan (default Rp500). Jika ada batas maksimum biaya, hitung ulang laba pada harga hasil dengan rumus rincian. Contoh: M = 35.000, a = 8%, l = 4%, b = 1,5%, F = 1.250, t = 0,5%, m = 20% → P = 36.250 ÷ 0,66 = 54.924,24 → Rp 54.925 → rekomendasi Rp 55.000 (laba Rp 11.050, margin 20,09%).

## Format output
```
### <Platform> - target <margin/laba/markup>
- Harga minimal agar tidak rugi: **Rp ...**
- **Harga rekomendasi: Rp ...**
| Komponen | Nilai |  ← rincian potongan, uang diterima, modal, laba, margin, markup
(Perbandingan antar-platform bila lebih dari satu)
**Catatan & asumsi** (sumber persentase, dasar biaya, PPh 22, berlaku per, disclaimer)
💡 Saran: <1–2 saran berbasis angka>
```

## Contoh
**Input pengguna:** "Modal kaos 35 ribu. Di Shopee admin 8%, gratis ongkir 4% maks 10 ribu, biaya proses 1.250 per pesanan, pembayaran 1,5%. Mau margin 20%, harga jualnya berapa?"

**Output (dipersingkat, dari script):**
```
### Shopee - target margin 20% dari harga setelah voucher
- Harga minimal agar tidak rugi: **Rp 42.152**
- **Harga rekomendasi (dibulatkan ke atas kelipatan Rp 500): Rp 55.000**

| Harga tayang | Rp 55.000 |
| Biaya admin/komisi (8%) | -Rp 4.400 |
| Biaya layanan/program ongkir (4%) | -Rp 2.200 |
| Biaya pembayaran/transaksi (1,5%) | -Rp 825 |
| Biaya per pesanan (dibagi 1 barang) | -Rp 1.250 |
| PPh 22 marketplace (0,5%) | -Rp 275 |
| **Uang diterima dari marketplace** | **Rp 46.050** |
| **Laba bersih per barang** | **Rp 11.050** (margin 20,09%) |

💡 Jika sudah menyerahkan surat pernyataan omzet ≤ Rp500 juta ke Shopee, hitung ulang tanpa PPh 22 (--pph22 tidak).
```

## Checklist sebelum mengirim hasil
- [ ] Persentase biaya berasal dari pengguna, atau diberi label "contoh — cek Seller Center".
- [ ] Asumsi dasar biaya (harga setelah voucher) dan target default disebut.
- [ ] PPh 22 0,5% disertakan (atau dijelaskan kenapa tidak) + catatan pengecualian OP omzet ≤ Rp500 juta dengan surat pernyataan.
- [ ] Harga rekomendasi dibulatkan ke atas dan laba pada harga itu ditampilkan.
- [ ] Format Rupiah `Rp 1.250.000`; disclaimer + tanggal berlaku ada.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila modal kosong/bukan angka, persen ≥ 100, voucher persen ≥ 100%, qty per pesanan bukan bilangan bulat, atau total persen biaya + target margin ≥ 100% (target mustahil). Jelaskan dan minta angka yang benar.
- Hitungan per barang; ongkir yang dibayar pembeli, subsidi platform, koin/cashback yang ditanggung platform, dan biaya iklan per klik tidak dimodelkan (masukkan sebagai `--iklan` % atau `--biaya-lain` bila perlu).
- Dasar biaya tiap platform bisa berbeda (mis. sebelum/sesudah voucher). Bila pengguna tahu dasar yang dipakai platformnya berbeda, sampaikan bahwa hasil bisa bergeser sedikit.
- PPh 22 marketplace: dasar aturan & status di `references/regulasi.md`. Jangan menyatakan pasti TikTok Shop sudah ditunjuk sebagai pemungut.
