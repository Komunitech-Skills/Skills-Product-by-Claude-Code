# 02 — Promo hampers kue kering Lebaran 2027, jualan lewat WA (S2, normal)

## Skenario
Usaha kue kering rumahan menjual hampers lewat WhatsApp dan Instagram, bukan marketplace, sehingga tidak ada potongan platform. Ingin merencanakan promo Ramadan–Lebaran tahun depan. Tanggal Lebaran 2027 belum resmi.

## Input pengguna
> Kak tolong bikinin rencana promo lebaran tahun depan buat hampers kue kering aku. Hampers isi 3 toples harganya 285rb, modal 168rb. Jualnya lewat WA & IG aja. Tahun lalu kejual 40 hampers tanpa promo. Aku kepikiran: potongan 20rb + gratis ongkir (rata2 ongkir 15rb) + bonus kartu ucapan & pita (7.500). Atau voucher 25rb min belanja 500rb? Budget konten 600rb. Target 150 hampers.

## Langkah agent
1. Lebaran berubah tiap tahun. Script menolak `--momen lebaran` tanpa tanggal, jadi dipakai perkiraan 10 Maret 2027 dari `references/momen-promo.md` dengan label **perkiraan**: `cek_promo.py jadwal --momen "Lebaran 2027 (perkiraan)" --tanggal 2027-03-10`.
2. Margin dicek untuk tiga opsi: (a) potongan Rp 20.000 + subsidi ongkir + hadiah, (b) voucher Rp 25.000 min. belanja Rp 500.000 untuk 1 hampers, (c) voucher yang sama untuk pesanan 2 hampers (`--item-per-pesanan 2`). Biaya platform 0%, karena jualan lewat WA.

## Output

# Rencana Promo Ramadan–Lebaran 2027 — Hampers Kue Kering
**Periode promo:** Rabu, 17 Februari 2027 (buka pre-order) s.d. Minggu, 28 Februari 2027 (batas kirim antarkota) *(tanggal perkiraan, cek SKB 3 Menteri/sidang isbat Kemenag)*  |  **Tujuan:** 150 hampers terjual, laba terjaga  |  **Anggaran konten:** Rp 600.000

## 1. Mekanisme (hasil cek margin)
| Opsi | Harga efektif/hampers | Laba/hampers (normal Rp 117.000 →) | Margin | Status |
|---|---|---|---|---|
| A. Potongan Rp 20.000 + gratis ongkir Rp 15.000 + kartu & pita Rp 7.500 | Rp 265.000 | Rp 74.500 | 28,1% | ✅ AMAN |
| B. Voucher Rp 25.000 min. belanja Rp 500.000, beli 1 hampers | Rp 285.000 (voucher **tidak terpakai**) | Rp 109.500 | – | ⚠️ tidak menarik bagi pembeli 1 hampers |
| C. Voucher Rp 25.000 min. belanja Rp 500.000, beli 2 hampers + gratis ongkir + kartu | Rp 272.500 | Rp 89.500 | 32,8% | ✅ AMAN |

**Rekomendasi:** gabungkan A untuk pembeli 1 hampers dan C untuk pembeli banyak (kantor, keluarga besar). Voucher C cocok untuk menaikkan jumlah hampers per pesanan, bukan untuk pembeli satuan.
Diskon maksimal agar tidak rugi (opsi A, dengan ongkir & kartu): **33,1%** (harga impas Rp 190.500).

## 2. Hitungan kampanye (opsi A, dari script)
- Target 150 hampers: dibayar pembeli Rp 39.750.000, laba sebelum anggaran Rp 11.175.000, anggaran konten Rp 600.000 → **laba bersih Rp 10.575.000**.
- Tahun lalu tanpa promo: 40 hampers × Rp 117.000 = Rp 4.680.000.
- Agar laba sama dengan tahun lalu, cukup **63 hampers** (1,57x). Anggaran konten tertutup setelah **9 hampers**.
- Kapasitas produksi harus dicek dulu: 150 hampers = 450 toples dalam ±3 minggu.

## 3. Linimasa (dari script; Lebaran = perkiraan Rabu, 10 Maret 2027)
| Hari | Tanggal | Fase | Kegiatan |
|---|---|---|---|
| H-30 | Senin, 8 Februari 2027 | Persiapan besar | Beli bahan & toples untuk 150 hampers; tetapkan batas pre-order (mis. 120 hampers antarkota + 30 dalam kota) |
| H-21 | Rabu, 17 Februari 2027 | Pre-order & pemanasan | Buka pre-order; foto hampers (skill `foto-produk-brief`) |
| H-14 | Rabu, 24 Februari 2027 | THR mulai cair | Promo utama; pengingat ke kantor/instansi |
| H-10 | Minggu, 28 Februari 2027 | Batas kirim antarkota | Tanyakan jadwal operasional kurir yang dipakai, jangan menebak; umumkan batas pesan |
| H-7 | Rabu, 3 Maret 2027 | Puncak | Pengingat terakhir; dalam kota lewat kurir instan |
| H-3 | Minggu, 7 Maret 2027 | Last call dalam kota | Ambil sendiri / kurir instan saja |
| H | Rabu, 10 Maret 2027 | Hari Raya | Ucapan tanpa jualan |
| H+3 | Sabtu, 13 Maret 2027 | Buka kembali | Balas chat tertunda |
| H+14 | Rabu, 24 Maret 2027 | Evaluasi | Target vs realisasi, sisa bahan |
*Seluruh tanggal bergeser bila pemerintah menetapkan tanggal Idulfitri berbeda. Jalankan ulang script dengan tanggal resmi.*

## 4. Materi & kanal
Status WA & IG: proses baking (video 15 detik), isi hampers, testimoni tahun lalu (dengan izin). Broadcast hanya ke pelanggan yang pernah memesan/setuju (skill `broadcast-wa`), dengan pilihan berhenti.

## 5. Kesiapan operasional
Bahan & toples dibeli sebelum harga naik jelang Ramadan; kardus hampers + bubble wrap; jadwal baking per hari; rekap pesanan di satu tabel.

## 6. Syarat & ketentuan (siap tempel)
1. Pre-order dibuka Rabu, 17 Februari 2027 s.d. Minggu, 28 Februari 2027 (antarkota) / Minggu, 7 Maret 2027 (dalam kota), atau sampai kuota 150 hampers terpenuhi.
2. Harga hampers Rp 285.000; selama promo potongan Rp 20.000 menjadi Rp 265.000, gratis ongkir s.d. Rp 15.000 (kelebihan ongkir dibayar pembeli), dan bonus kartu ucapan + pita.
3. Voucher Rp 25.000 untuk pembelian min. Rp 500.000 (min. 2 hampers) dalam satu pesanan. Tidak dapat digabung dengan potongan Rp 20.000.
4. Pembayaran lunas saat pemesanan melalui transfer ke rekening atas nama usaha.
5. Pengiriman sesuai jadwal kurir. Keterlambatan karena libur kurir diinformasikan sebelum pesanan dibayar.

**Asumsi & catatan:** biaya platform 0% (jualan langsung via WA/IG). Tanggal Idulfitri 1448 H **perkiraan, belum terverifikasi**. THR umumnya cair paling lambat H-7 (cek surat edaran Kemnaker tahun berjalan). Harga normal Rp 285.000 harus harga yang memang berlaku. Ini alat bantu perencanaan, bukan jaminan hasil.

## Catatan penguji
- Hitungan dicek manual: A = 265.000 − 15.000 − 168.000 − 7.500 = 74.500 ✓; C = 570.000 − 25.000 − 15.000 − 2×175.500 = 179.000 → 89.500/hampers ✓; impas A = 168.000 + 7.500 + 15.000 = 190.500 → 1 − 190.500/285.000 = 33,16% → 33,1% (dibulatkan ke bawah) ✓.
- Nama hari: 8 Feb 2027 Senin, 10 Mar 2027 Rabu ✓ (dicek `datetime`).
- Bagus: script menolak Lebaran tanpa tanggal, memberi label perkiraan, dan memperingatkan bila voucher tidak terpakai karena di bawah min. belanja.
- Kurang: opsi voucher di tabel ringkasan tidak menunjukkan persen hemat bila `item-per-pesanan` diubah, sehingga agent harus menjelaskannya. Fase pola Lebaran H-14 "THR mulai cair" terasa generik.
