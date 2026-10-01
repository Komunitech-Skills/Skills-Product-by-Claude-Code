# Uji ulang 01 — Harga jual Shopee target untung 25% (harga-jual-marketplace 1.0.3)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech` (jawaban dilayani `claude-sonnet-5`). Home baru `sol2-toko-online` (paket skill solusi, dibuat ulang lewat script reset sebelum skenario). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama ([01-harga-jual-shopee.md](01-harga-jual-shopee.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran).

## Pesan member
> kak aku jual tumbler stainless modal 38rb udh sm packing, mau jual di shopee. admin 8% , ikut gratis ongkir xtra 4% maks 10rb, biaya proses 1250 per pesanan. mau untung 25% brp harga jualnya ya

Alat: `read, exec` (18 dtk). Skill terpakai.

## Balasan (utuh)
> ### Shopee – target margin 25%
>
> - Harga minimal biar ga rugi: **Rp 44.858**
> - **Harga rekomendasi: Rp 63.000**
>
> | Komponen | Nilai |
> |---|---:|
> | Harga tayang | Rp 63.000 |
> | Admin (8%) | -Rp 5.040 |
> | Gratis ongkir xtra (4%) | -Rp 2.520 |
> | Biaya proses/pesanan | -Rp 1.250 |
> | PPh 22 marketplace (0,5%) | -Rp 315 |
> | **Uang diterima** | **Rp 53.875** |
> | Modal | -Rp 38.000 |
> | **Laba bersih** | **Rp 15.875** (margin 25,2%, markup 41,78%) |
>
> **Catatan & asumsi**
> - Persentase biaya platform berasal dari input kamu — cek lagi angka terbaru di Seller Center (beda per kategori/program, bisa berubah).
> - Biaya persen & PPh 22 dihitung dari harga setelah voucher toko (di sini belum ada voucher, jadi sama dengan harga tayang).
> - PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke marketplace; hitung ulang tanpa PPh 22 kalau sudah daftar.
> - Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.
>
> 💡 Rp 63.000 udah pas kelipatan Rp500 dan laba sedikit di atas target (25,2% vs 25% yang diminta), aman buat dipasang. Kalau mau psikologis Rp 62.900 atau Rp 59.900, laba/marginnya bakal turun sedikit di bawah target — mau aku hitungin juga?

## Verifikasi independen
Target dengan PPh 22: 39.250 ÷ (1 − 0,08 − 0,04 − 0,005 − 0,25) = **62.800** → kelipatan Rp500 ke atas **63.000** ✔. Balik modal 39.250 ÷ 0,875 = 44.857,14 → **44.858** ✔. Di Rp63.000: admin 5.040, ongkir 2.520, PPh 22 315, diterima 53.875, laba 15.875, margin 25,20%, markup 41,78% ✔. Batas ongkir 10rb tidak tercapai ✔.

Cek klaim tambahan: *"Kalau mau psikologis Rp 62.900 … laba/marginnya bakal turun sedikit di bawah target"* — **salah untuk Rp62.900**: laba 15.787,50, margin **25,10%** (masih di atas 25%, karena harga target persis 62.800). Untuk Rp59.900 benar di bawah target.

## Penilaian
- **Cacat lama hilang: YA.** Blok catatan kini disalin utuh: *"PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026) … Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak."*
- **Regresi/temuan baru (kecil):** narasi model di luar script menyatakan Rp62.900 di bawah target (salah, margin 25,1%). Model menawarkan menghitung ulang, jadi risikonya rendah.
- **Skor: 8,5/10** (uji pertama SESUDAH: 8,5). Kekurangan lama hilang, tetapi muncul satu klaim angka salah dari model. Saran: "jangan menyatakan untung/rugi harga lain sebelum dihitung script (`--harga`)".
