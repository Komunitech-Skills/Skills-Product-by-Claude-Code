# 03 — Normal: toko online baju dari rumah + banding 2 penawaran polis

**Pesan:**
> jualan baju di shopee & tokped dr rumah jogja, stok kira2 60jt di kamar belakang (pernah bocor pas hujan). sendirian + 1 admin 2,5jt. internet+listrik 600rb, cicilan 1jt. tabungan 15jt. penjualan rame pas lebaran doang. ada 2 penawaran: A premi 1,2jt/thn pertanggungan 60jt own risk 10%, banjir gak termasuk. B premi 1,8jt/thn pertanggungan 75jt own risk 1jt, banjir termasuk. bagusan mana?

**Data risiko:** `data/03-toko-online-jogja.json`. Dana: 6 bulan (usaha musiman, sesuai default skill), biaya Rp4.100.000.

**Output SESUDAH (ringkas):**
> | No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Akun marketplace dibekukan | 3 | 4 | 12 TINGGI | Patuhi aturan toko, buka kanal kedua (WA katalog/toko lain), simpan daftar pelanggan sendiri | Ya, pertimbangkan |
> | 2 | Banjir/bocor merusak stok (±Rp60 jt) | 2 | 4 | 8 SEDANG | Stok di rak/kontainer plastik tertutup, perbaiki atap | Ya, pertimbangkan |
> | 3 | Pemilik sakit (satu-satunya pengelola) | 2 | 4 | 8 SEDANG | Ajari admin proses kirim & balas chat | Ya, pertimbangkan |
> | 4 | Paket hilang/rusak di ekspedisi | 4 | 2 | 8 SEDANG | Video unboxing/packing, asuransi pengiriman per paket mahal | Tidak perlu |
> | 5 | Penipuan retur/bukti transfer palsu | 4 | 2 | 8 SEDANG | Cek mutasi, video packing | Tidak perlu |
> | 6 | Pencurian stok | 2 | 3 | 6 SEDANG | Kunci kamar stok, stok opname bulanan | Tidak perlu |
> | 7 | Kebakaran rumah-gudang | 1 | 5 | 5 SEDANG | APAR kecil, colokan tidak bertumpuk | Ya, pertimbangkan |
>
> Dana darurat 6 bulan: Rp4.100.000/bln → target **Rp24.600.000**; kas Rp15.000.000 (±3,7 bln); kekurangan **Rp9.600.000** → 12 bulan Rp800.000/bln (lebih ringan bila disisihkan saat ramai Lebaran).
>
> Banding netral (tanpa memilih "terbaik"):
> | | Penawaran A | Penawaran B |
> |---|---|---|
> | Premi/tahun | Rp1.200.000 | Rp1.800.000 |
> | Nilai pertanggungan | Rp60.000.000 | Rp75.000.000 |
> | Biaya sendiri | 10% kerugian | Rp1.000.000 per kejadian |
> | Banjir | Tidak termasuk | Termasuk |
> | Contoh: stok rusak Rp20 jt karena bocor/banjir | Tidak dijamin (banjir dikecualikan; bocor atap cek definisi) | Ganti ±Rp19 jt bila syarat terpenuhi |
> | Contoh: kebakaran rugi Rp60 jt | Ganti Rp54 jt (60 jt − 10%) | Ganti Rp59 jt |
> Yang perlu ditanyakan: definisi "banjir" vs "air hujan/bocor", apakah stok berpindah-pindah tetap dijamin, batas klaim per tahun, izin OJK. Selisih premi Rp600.000/tahun.

**Verifikasi:** skor 12,8,8,8,8,6,5 cocok; 2.500.000+600.000+1.000.000 = 4.100.000; ×6 = 24.600.000; −15.000.000 = 9.600.000; /12 = 800.000; 60 jt × 90% = 54 jt; 20 jt − 1 jt = 19 jt; 60 jt − 1 jt = 59 jt; 1,8 − 1,2 = 0,6 jt. Cocok. Contoh klaim dihitung agent, bukan script (tidak ada fungsi banding polis).

**Catatan:** Baris 1 "Akun marketplace dibekukan → Perlu asuransi: Ya, pertimbangkan" **salah secara isi**: tidak ada asuransi umum untuk akun marketplace dibekukan; ini akibat aturan numerik script (dampak ≥ 4, kemungkinan ≤ 3 → alihkan) dan perintah SKILL "ikuti kolom hasil script" (cacat B2). Pada uji ini penguji mencatatnya apa adanya karena SKILL melarang mengubah hasil script. Opsi `--dana` (kerugian_rp vs dana darurat) ada di script tetapi tidak disebut di langkah kerja, sehingga `kerugian_rp` praktis tidak terpakai.

**Skor: SEBELUM 6,5 · SESUDAH 7.**
