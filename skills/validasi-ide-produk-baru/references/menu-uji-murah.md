# Menu Uji Murah 7 Hari

Panduan memilih & menjalankan metode uji pasar murah sesuai kanal yang sudah dimiliki. Semua metode di bawah bisa dijalankan tanpa biaya iklan, tanpa produksi massal, dan selesai dalam 7 hari.

> **Aturan hitung (berlaku untuk semua metode):**
> - **Pesanan** (`--preorder`) = tindakan berkomitmen: pre-order yang **sudah transfer/DP/bayar**, order yang di-checkout di marketplace, barang titipan yang **laku terjual**, pesan ulang yang dibayar. Hanya ini yang masuk konversi, margin, dan balik modal.
> - **Minat** (`--minat`) = vote polling, like, emoji, komentar "mau", chat tanya harga, konfirmasi nama+jumlah tapi **belum bayar**, jawaban "ya mau beli rutin". Dicatat dan dilaporkan terpisah, **tidak pernah** dijumlahkan dengan pesanan.

## 1. Pre-order via broadcast/status WA
**Cocok kalau:** punya ≥30 kontak yang relevan dengan ide (bukan grup keluarga/arisan yang tidak relevan).

**Langkah:**
1. Kirim pesan (lihat `templates/pesan-uji-murah.md`) ke kontak yang relevan atau pasang di status WA selama beberapa hari.
2. Hitung "ditawari" = jumlah kontak yang dikirimi (broadcast) atau perkiraan jumlah yang melihat status (WA menunjukkan daftar pelihat status — hitung manual).
3. Hitung "pesanan" = jumlah yang **sudah transfer/DP**. Yang membalas "mau"/konfirmasi nama + jumlah tapi belum bayar dicatat sebagai **minat** (tagih DP sebelum tenggat supaya bisa naik jadi pesanan).
4. Beri tenggat jelas ("konfirmasi sebelum [tanggal]") supaya periode uji tidak molor.

## 2. Polling story Instagram
**Cocok kalau:** punya ≥100 follower aktif (rata-rata views story di atas 30–50 biasanya cukup untuk sinyal awal).

**Langkah:**
1. Posting story dengan stiker polling ("Mau beli kalau ada? Ya / Nanti dulu") + gambar produk/mock-up.
2. "Ditawari" = jumlah views/impressions story (Instagram Insights menunjukkan ini).
3. Vote "Ya" = **minat**, bukan pesanan (klik vote terlalu murah untuk jadi sinyal beli). Polling saja **tidak bisa** menghasilkan klasifikasi LULUS/GAGAL. Untuk mengubahnya jadi pesanan: DM pemilih "Ya" dengan tawaran PO + DP; yang transfer baru dihitung pesanan (kanal "DM dari polling", ditawari = jumlah yang di-DM).
4. Ulangi di beberapa story berbeda hari kalau follower tidak semuanya online bersamaan.

## 3. Lapak percobaan di marketplace (listing dulu, produksi setelah order/sistem PO)
**Cocok kalau:** sudah punya toko marketplace (Shopee/Tokopedia/dll.) atau gampang buka baru; produk bisa dijual sistem pre-order (PO) tanpa stok jadi.

**Langkah:**
1. Buat listing dengan judul & deskripsi jelas, tandai "PO — estimasi kirim X hari" agar tidak dianggap wanprestasi.
2. "Ditawari" = jumlah dilihat listing (marketplace biasanya menampilkan "dilihat X kali").
3. "Pesanan" = jumlah order yang **di-checkout/dibayar**. Chat yang hanya menanyakan harga/cara beli = minat.
4. Batasi kuota PO (mis. "khusus 10 pembeli pertama") supaya risiko produksi tetap kecil.

## 4. Sampel ke 10 pelanggan tetap
**Cocok kalau:** sudah punya ≥10 pelanggan langganan/reguler (untuk usaha yang sudah berjalan, bukan usaha baru dari nol).

**Langkah:**
1. Beri sampel gratis/harga khusus ke 10 pelanggan tetap, minta jawaban jujur: "kalau ini dijual rutin seharga [harga], mau beli lagi tidak?"
2. "Ditawari" = 10 (atau jumlah sampel yang dibagikan).
3. "Pesanan" = jumlah yang **langsung memesan ulang dan membayar** dalam 7 hari. Jawaban "ya, mau beli rutin" tanpa pesanan = minat (catat, tapi tidak masuk hitungan uang).
5. Catat alasan yang bilang "tidak" — ini paling berharga karena datang dari pelanggan yang sudah percaya ke usaha kita.

## 5. Titip di warung/reseller
**Cocok kalau:** ada warung/toko/reseller langganan yang mau dititipi tanpa biaya sewa rak besar.

**Langkah:**
1. Titipkan jumlah kecil (mis. 10–20 pcs) dengan sistem konsinyasi (bayar setelah laku) selama masa uji.
2. "Ditawari" = perkiraan jumlah pengunjung warung yang melihat produk selama periode uji (tanya pemilik warung perkiraan kasar, atau pakai jumlah stok yang dititip sebagai proksi kasar bila sulit dihitung — sebutkan ini sebagai perkiraan, bukan angka pasti).
3. "Pre-order/beli" = jumlah yang benar-benar laku terjual saat masa uji berakhir.
4. Cek ke pemilik warung di hari ke-7, bukan menunggu lebih lama (supaya tetap dalam jendela 7 hari).

## Kasus tambahan: kelas online Canva
Contoh kombinasi metode untuk jasa/produk digital (kelas online Canva):
- Hipotesis: "Kami percaya **pemilik UMKM yang jualan online tapi belum bisa desain sendiri** mau membayar **Rp99.000** untuk **kelas online Canva 2 sesi** karena bisa **bikin konten promosi sendiri tanpa sewa desainer**."
- Metode: pre-order via broadcast WA ke alumni pelatihan/komunitas UMKM sebelumnya + story polling IG.
- Ditawari: 35 (broadcast, hitung pesanan = yang sudah transfer) dan 150 views story (vote = minat, dilaporkan terpisah; tidak digabung dengan pesanan).
- Kriteria: karena ini produk harga menengah pertimbangan sedang, pakai ambang default (15%/8%).

## Menggabungkan beberapa metode
- **Pesanan boleh dijumlahkan** antar kanal yang sama-sama menghasilkan pesanan berkomitmen (mis. PO berbayar WA + checkout marketplace): total pesanan ÷ total ditawari di kanal-kanal itu.
- **Minat TIDAK PERNAH dijumlahkan dengan pesanan.** Kanal yang hanya menghasilkan minat (polling, like, komentar) dilaporkan di baris sendiri dan tidak ikut konversi, margin, atau balik modal.
- Selalu tampilkan konversi per kanal juga, supaya terlihat kanal mana yang paling efektif.
- Pakai mode `kanal` di `scripts/hitung_validasi.py` (lihat SKILL.md Langkah 5) — script yang memisahkan keduanya.

Contoh salah vs benar (keripik Rp18.000, HPP Rp9.500, biaya uji Rp60.000; WA 45 ditawari → 4 sudah transfer; polling IG 380 views → 52 vote "mau"):
- ❌ Salah: 56 pesanan dari 425 → margin 56 × Rp8.500 = Rp476.000 → "balik modal +Rp416.000".
- ✅ Benar: pesanan 4 dari 45 (8,9%); margin 4 × Rp8.500 = Rp34.000; selisih Rp34.000 − Rp60.000 = **−Rp26.000 (belum balik modal)**; 52 vote dilaporkan sebagai minat.
