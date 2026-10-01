# Uji ulang 2 — Harga jual Shopee target untung 25% (harga-jual-marketplace 1.0.4)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal asli (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech`. Home `sol2-toko-online` direset lewat script reset tepat sebelum skenario (tidak ada file data yang perlu dibuat ulang; semua data ada di pesan). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama dan uji ulang 1 ([01-harga-jual-shopee.md](01-harga-jual-shopee.md), [01-harga-jual-shopee-ulang.md](01-harga-jual-shopee-ulang.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python dan script skill dijalankan ulang oleh penguji. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran). Keluaran mentah: `hasil/ulang4-*.txt`.

## Cacat sisa dari uji ulang 1 (versi 1.0.3)
Narasi model menyebut Rp62.900 "di bawah target" padahal margin 25,10% (≥ 25%).

## Pesan member
> kak aku jual tumbler stainless modal 38rb udh sm packing, mau jual di shopee. admin 8% , ikut gratis ongkir xtra 4% maks 10rb, biaya proses 1250 per pesanan. mau untung 25% brp harga jualnya ya

Alat: `read, exec`. Skill terpakai.

## Balasan (utuh)
> ### Shopee - modal 38.000, target margin 25%
>
> - Harga minimal biar gak rugi: **Rp 44.858**
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
> | Modal/HPP | -Rp 38.000 |
> | **Laba bersih** | **Rp 15.875** (margin 25,2%, markup 41,8%) |
>
> Status: **memenuhi target margin 25%** (hasil hitung script, bukan taksiran).
>
> 💡 Saran:
> - Rp 63.000 udah "pas" psikologis-ish. Kalau mau coba harga lebih "nanggung" kayak Rp 62.900, bisa aku hitung ulang labanya biar ketahuan masih kena target atau turun dikit.
> - Gratis ongkir 4% itu udah kena maksimal Rp10rb? Di harga Rp63.000, 4% = Rp2.520, masih di bawah batas Rp10rb, jadi aman dipakai apa adanya.
>
> **Catatan & asumsi**
> - Persentase biaya platform berasal dari input Anda. Cek angka terbaru di Seller Center masing-masing (berbeda per kategori & program, dan bisa berubah).
> - Biaya persen dan PPh 22 dihitung dari harga setelah voucher toko. Jika platform Anda memakai dasar lain, hasil bisa sedikit berbeda.
> - Biaya dihitung tanpa pembulatan; angka di tabel dibulatkan ke rupiah terdekat.
> - PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke marketplace; hitung ulang dengan --pph22 tidak. PPh 22 ini bukan pajak baru; cara memperhitungkannya dengan PPh final Anda, tanyakan ke DJP/konsultan.
> - Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.

## Verifikasi independen
Python: (38.000 + 1.250) ÷ (1 − 0,08 − 0,04 − 0,005 − 0,25) = **62.800** → kelipatan Rp500 ke atas **63.000** ✔. Balik modal 39.250 ÷ 0,875 = 44.857,14 → **44.858** ✔. Di Rp63.000: admin 5.040, ongkir 2.520 (< batas 10.000) ✔, PPh 22 315, diterima 53.875, laba 15.875, margin 25,198% → 25,2%, markup 41,78% ✔. Script dijalankan ulang penguji: *"Status target pada harga rekomendasi: MEMENUHI target margin 25% …"* ✔. Pembanding (tidak diklaim di balasan): Rp62.900 → margin 25,10% MEMENUHI; Rp59.900 → 21,97% DI BAWAH.

## Penilaian
- **Cacat sisa hilang: YA.** Tidak ada lagi klaim untung/rugi harga lain tanpa script. Status dikutip dari script: *"Status: **memenuhi target margin 25%** (hasil hitung script, bukan taksiran)."* Untuk Rp62.900 agent menawarkan: *"bisa aku hitung ulang labanya biar ketahuan masih kena target atau turun dikit"* (tidak menilai sendiri).
- **Regresi (kecil, jargon):** karena blok catatan disalin kata per kata, teks perintah script ikut sampai ke member awam: *"hitung ulang dengan --pph22 tidak."* Sumbernya teks catatan di `harga_marketplace.py` sendiri (uji ulang 1 memparafrasekannya jadi "hitung ulang tanpa PPh 22 kalau sudah daftar"). Saran: ubah teks script menjadi "minta hitung ulang tanpa PPh 22". Catatan kecil lain: Rp63.000 disebut "pas psikologis-ish" (opini, tidak salah).
- **Skor: 8,5/10** (uji ulang 1: 8,5). Kebenaran angka naik, tetapi satu jargon CLI masuk ke chat. **LULUS** (dengan saran perbaikan teks catatan script).
