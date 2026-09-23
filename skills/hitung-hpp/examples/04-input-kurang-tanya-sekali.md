# 04 — Input kurang: daftar bahan tanpa harga & takaran

**Skenario:** S4 — input tidak lengkap. Harga beli, isi kemasan, takaran pakai, dan hasil per resep tidak ada.

**Input pengguna (persis):**
> HPP brownies saya berapa ya? bahannya tepung, gula, telur, coklat, mentega

## Output (bertanya sekali)

Siap saya hitungkan. Supaya HPP-nya akurat, saya perlu beberapa data (boleh dijawab singkat):

1. **Untuk tiap bahan**: harga beli, isi kemasan, dan jumlah yang dipakai per resep. Contoh: *"tepung beli 1 kg 14rb, pakai 250 g; telur 30rb isi 16, pakai 6 butir"*. Kalau takarannya pakai sendok, timbang sekali dalam gram ya — sendok tidak bisa dikonversi akurat.
2. **1 resep jadi berapa** loyang/potong?
3. **Kemasan** per loyang (box, stiker) dan harganya?
4. **Biaya lain**: upah (kalau ada yang dibayar), gas per resep, listrik/sewa per bulan, oven (harga & perkiraan umur pakai)? Kalau tidak ada, saya anggap Rp0 dan saya sebutkan bahwa upah Anda sendiri belum dihitung.
5. **Sebulan produksi berapa loyang**, dan mau untung berapa persen (margin)? Kalau belum tahu, saya tampilkan pilihan margin 20/30/40/50%.

## Catatan penguji
- Bertanya sekali, tepat 5 pertanyaan bernomor, dengan contoh format jawaban yang ramah awam. Sesuai SKILL.md.
- Sudah mengantisipasi masalah sendok/cangkir (batasan script: satuan "sdm" ditolak) — bagus.
- Tidak menebak harga bahan (benar; harga bahan berbeda per daerah).
