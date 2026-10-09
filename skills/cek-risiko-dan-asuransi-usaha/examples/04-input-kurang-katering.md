# 04 — Input tidak lengkap: katering, tanpa angka

**Pesan:**
> sy usaha katering rumahan, perlu asuransi apa aja? dana darurat brp?

**Perilaku yang diharapkan:** kerjakan dulu dengan asumsi, tanya maks 3 di akhir, dana darurat `[isian]` (biaya tetap tidak diberikan), jangan mengarang nilai aset.

**Output SESUDAH (ringkas):**
> Asumsi: katering di rumah (bukan ruko), kota besar, 2 karyawan, status BPJS belum diketahui; nilai alat & stok `[isian: nilai aset]`.
>
> Tabel 7 risiko: Pelanggan keracunan pesanan besar (2×5 = 10 TINGGI, Ya pertimbangkan, langkah: sampel makanan disimpan 2×24 jam, catat bahan & suhu); Kebakaran dapur gas (2×5 = 10 TINGGI, Ya pertimbangkan); Pemilik/juru masak utama sakit saat pesanan besar (3×3 = 9 SEDANG, Tidak perlu, langkah: resep tertulis, 1 cadangan); Karyawan cedera (3×3 = 9 SEDANG, BPJS); Pemasok bahan naik harga/telat (3×2 = 6 SEDANG); Pembayaran DP palsu/batal (3×2 = 6 SEDANG); Kendaraan antar kecelakaan (2×3 = 6 SEDANG).
>
> Dana darurat: target = biaya tetap per bulan × 3 = **[isian: biaya tetap per bulan] × 3**. Contoh rumus: bila biaya tetap Rp6.000.000, target Rp18.000.000 (contoh, bukan data Anda).
>
> Perlindungan umum: tanggung gugat produk/umum, kebakaran/isi rumah usaha, kendaraan, BPJS. Disclaimer.
> Pertanyaan (3): 1) Biaya tetap per bulan (gaji, listrik/gas, cicilan, sewa)? 2) Kas cadangan sekarang? 3) Berapa karyawan dan sudah ikut BPJS?

**Verifikasi:** skor 10,10,9,9,6,6,6 cocok dengan rumus; contoh 6.000.000×3 = 18.000.000 benar dan ditandai contoh.

**Catatan:** perilaku sesuai brief (kerja dulu, 3 pertanyaan, tidak mengarang). Model dasar tanpa skill cenderung menjawab "dana darurat 3–6 bulan pengeluaran" tanpa tabel dan menanyakan banyak hal sekaligus.

**Skor: SEBELUM 6 · SESUDAH 8,5.**
