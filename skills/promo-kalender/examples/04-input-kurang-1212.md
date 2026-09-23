# 04 — "Diskon berapa yang aman buat 12.12?" tanpa angka (S4, input tidak lengkap)

## Input pengguna
> mau ikut 12.12 nih, diskon berapa persen ya yg aman?

## Output
Siap, aku bantu hitung diskon yang aman untuk 12.12 (Sabtu, 12 Desember 2026). Supaya angkanya pasti (bukan kira-kira), aku perlu jawaban untuk 5 hal ini:

1. **Produk apa** yang mau dipromokan, dan **harga jual normalnya** (harga yang berlaku sekarang)?
2. **Modal/HPP per unit**, sudah termasuk kemasan. Kalau belum tahu, bisa dihitung dulu dengan skill `hitung-hpp`.
3. **Jualan di mana?** Kalau di marketplace, berapa total potongannya (%) dan biaya per pesanan? Lihat di *rincian penghasilan* satu pesanan di Seller Center. Aku tidak memakai angka tebakan karena tarif beda per kategori dan sering berubah.
4. **Biasanya laku berapa** per minggu? (untuk menghitung target agar laba tidak turun)
5. **Ada rencana gratis ongkir, voucher, atau budget iklan?** (boleh dikosongkan)

Kalau mau cepat, cukup jawab nomor 1–3. Sisanya aku isi dengan default (tanpa subsidi ongkir, tanpa anggaran) dan aku sebutkan asumsinya.

Setelah itu kamu dapat: tabel diskon/bundling/voucher dengan laba per unit dan status AMAN/TIPIS/RUGI, **diskon maksimal sebelum rugi**, target unit, linimasa 28 November–19 Desember 2026, dan S&K promo siap tempel.

## Catatan penguji
- Bertanya sekali, maksimal 5 pertanyaan bernomor, dengan jalur cepat (jawab 3 wajib saja). Sesuai SKILL.md.
- Tidak mengarang tarif marketplace dan mengarahkan ke Seller Center.
- Tanggal dicek: 12 Des 2026 = Sabtu; H-14 = Sabtu, 28 November 2026; H+7 = Sabtu, 19 Desember 2026 (sesuai `cek_promo.py jadwal --momen 12.12 --dari 2026-09-23`) ✓.
