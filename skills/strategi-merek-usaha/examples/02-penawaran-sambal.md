# Contoh 2: Rumusan penawaran sambal cobek

**Input pengguna:** "Sambal cobek 180 g Rp38.000, modal Rp17.000, jual di Shopee (potongan 8% menurut pusat penjual saya) dan WA. Mau bikin penawaran yang bikin orang beli lagi. Bonus boleh stiker (modal Rp500) dan kartu resep (Rp800). Batch berikutnya 50 botol, kirim tiap Senin dan Kamis."

**Tuas terlemah (perkiraan):** keyakinan ("takut basi/tidak tahan lama") dan kerepotan ongkir. Perbaikan: garansi ganti rusak + bonus kartu resep.

**Hitungan** (`python3 scripts/hitung_penawaran.py --harga 38000 --hpp 17000 --platform 8 --bonus "Stiker=500;Kartu resep=800" --refund 2 --margin-minimal 25`):
```
Harga tayang        : Rp38.000
Potongan platform   : -Rp3.040
HPP                 : -Rp17.000
Bonus Stiker        : -Rp500 (biaya modal)
Bonus Kartu resep   : -Rp800 (biaya modal)
Perkiraan refund 2% : -Rp760
LABA per unit       : Rp15.900 (margin 41.8%)
Ruang biaya bonus maksimum agar margin >= 25%: Rp7.700 per unit; memenuhi.
```
Versi B, diskon 15% tanpa bonus lain (`--diskon 15` dengan bonus yang sama): harga tayang Rp32.300, laba Rp10.770 (margin 33,3%). Versi A (bonus, harga penuh) lebih menguntungkan Rp5.130 per botol. Rekomendasi: versi A.

**Penawaran:**
- Inti: Sambal Cobek 180 g (isi: [isi: bahan dan masa simpan sesuai label]).
- Bonus: kartu resep (3 resep) + stiker.
- Garansi: botol bocor/pecah atau salah kirim? Kirim ulang gratis, kirim video buka paket maks. 2 hari setelah terima.
- Batas nyata: 50 botol batch ini; pesanan ditutup saat 50 botol habis; batch berikutnya [isi: tanggal].
- Nama: "Paket Sarapan Pedas".

**WhatsApp** (untuk pelanggan yang pernah beli):
> Halo Kak, sambal cobek batch baru sudah jadi. Paket Sarapan Pedas: sambal 180 g + kartu resep + stiker, Rp38.000. Batch ini 50 botol, kirim Senin/Kamis. Kalau botol bocor atau salah kirim, kami kirim ulang gratis (video buka paket maksimal 2 hari). Mau dipesan? Balas "MAU". Balas STOP kalau tidak mau dikabari lagi.

**Ceklis kepatuhan:** angka stok diperbarui tiap terjual; bonus benar-benar dikirim; tidak ada klaim "tahan sekian bulan" kecuali sudah diuji; izin PIRT/halal: [isi nomor bila ada] dan cek aturan BPOM.
