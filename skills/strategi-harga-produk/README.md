# Harga Tepat, Laku, dan Tetap Untung

**Tentukan harga eceran, reseller, paket, dan promo dengan hitungan pasti, bukan feeling.**

## Manfaat
- ✅ Harga yang disarankan **tidak pernah di bawah batas untung** Anda (dihitung dari modal + potongan + margin minimum)
- ✅ Daftar harga reseller/grosir/agen siap kirim ke WA, lengkap untung Anda dan untung reseller per level (harga anjuran reseller selalu sama dengan harga toko)
- ✅ Tahu dulu sebelum promo: "diskon 20% berarti penjualan harus naik 51% agar untung sama", plus alternatif promo yang lebih aman
- ✅ Paket hemat & hampers dicek: pembeli hemat berapa, Anda untung berapa
- ✅ Rencana naik harga saat bahan naik: berapa pelanggan boleh berkurang sebelum rugi, plus teks pengumuman yang sopan

## Cocok untuk siapa
- Pemilik toko roti/kue, katering, kedai, F&B rumahan
- Produsen & brand kecil yang mulai membuka reseller, grosir, atau agen
- Penjual online dan offline yang ingin merancang paket, harga cantik, atau promo tanggal kembar
- Penyedia jasa (desain, foto, les) yang ingin menyusun paket Hemat/Favorit/Premium

## Contoh sebelum & sesudah
**Sebelum:** "Mau promo diskon 20% biar rame." Setelah sebulan, toko ramai tapi uang di akhir bulan malah berkurang. Harga reseller ditentukan kira-kira, agen dapat harga yang ternyata hampir tidak untung.

**Sesudah (cukup ketik):** "Roti sobek saya jual 28 ribu, modal 11.500, sewa+gaji 6,5 juta, laku 600 sebulan. Mau buka reseller dan promo 20%."
→ Titik impas 394 pcs/bulan. Tangga harga Rp28.000 / Rp24.000 (≥10) / Rp21.000 (≥50) / Rp18.000 (≥200), semua di atas margin minimum. Diskon 20% butuh penjualan naik **51,38%** (600 → 909 pcs) — disarankan diganti "beli 5 gratis 1" khusus Jumat dengan kuota. Plus teks daftar harga reseller siap tempel.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Harga bolu pandan saya enaknya berapa? Modal 19 ribu."
- "Bikinin harga reseller, grosir, agen untuk kopi susu literan saya, modal 22 ribu, jual 45 ribu."
- "Diskon 30% untuk 11.11 masih untung nggak? Modal 40rb, harga 89.900, jual di Shopee."
- "Hampers isi 3 toples, enaknya dijual berapa?"
- "Bahan naik, mending naik harga ke 29.900 atau 31.000?"

Hasilnya selalu memuat asumsi yang dipakai, tabel angka, aturan promo, dan langkah minggu ini. Hasil simulasi "kalau harga naik, penjualan turun berapa" diberi label **perkiraan**.

Lebih lengkap bila dipakai bersama skill Komunitech lain: **hitung-hpp** (menghitung modal dari resep), **harga-jual-marketplace** (potongan Shopee/Tokopedia/TikTok Shop), **riset-harga-kompetitor** (harga pasar pesaing).

## Instalasi singkat
Salin folder `strategi-harga-produk` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` di dalam paket. Tidak perlu API key, akun, atau instalasi tambahan. Hitungan memakai Python bawaan; bila Python tidak tersedia, AI menghitung manual dengan rumus yang ditampilkan.

## FAQ
**Apa bedanya margin dan markup? Saya bilang "untung 50%".**
Margin = untung dibagi harga jual; markup = untung dibagi modal. Modal Rp10.000 dijual Rp15.000 itu markup 50% tapi margin hanya 33,33%. Skill ini selalu menampilkan keduanya dan akan bertanya bila maksud Anda belum jelas.

**Apakah skill ini bisa memastikan penjualan tidak turun kalau saya naik harga?**
Tidak ada yang bisa memastikan. Yang pasti dihitung: berapa penjualan boleh turun sebelum untung Anda lebih kecil dari sekarang. Perkiraan pada tiga tingkat kepekaan pembeli diberi label "perkiraan", dan skill menyarankan uji kecil dulu.

**Usaha saya PKP, bagaimana dengan PPN?**
Untung dihitung dari harga sebelum PPN. Bila ingin harga tayang cantik yang sudah termasuk PPN (mis. Rp49.900), skill menghitung DPP dan PPN-nya (tarif 12% × DPP nilai lain 11/12, dibulatkan ke bawah), margin dari DPP, dan harga tayang minimum termasuk PPN — untuk harga satuan, reseller, paket, promo, dan harga cantik. Pembulatan belum dicocokkan dengan Coretax; untuk faktur resmi ikuti Coretax atau konsultan pajak. Bila bukan PKP, Anda tidak boleh memungut PPN.

## Riwayat versi
- **1.0.8 (2026-10-03)** — dari uji ulang OpenClaw 1.0.7: hitungan PPN kini menampilkan terpisah margin bila harga "dibagi 1,12" (keliru), bila PPN tidak dipisah (keliru), dan margin yang benar — agar AI tidak tertukar. Dari harga lantai, AI tegas tidak menawarkan diskon dan menyebut harga normal minimal agar ada ruang diskon 5%/10%; contoh harga cantik yang aman dicetak hitungan sehingga AI tidak mengarang "misal" harga.
- **1.0.7 (2026-10-03)** — dari uji OpenClaw 1.0.6: AI sempat menulis "diskon maksimal 9%" sendiri padahal hitungan menunjukkan tidak ada ruang diskon. Kini setiap hitungan mencetak **ringkasan siap tempel** (harga, laba, margin, status, diskon maksimal, konflik reseller/agen) dan AI wajib menyalinnya apa adanya — tidak boleh menulis angka harga/diskon yang tidak dihitung. Tambahan: rentang aman harga khusus reseller/agen selama promo, pembanding volume promo marketplace terhadap jual langsung, dan peringatan bila margin terlihat besar karena PPN lupa dipisah.
