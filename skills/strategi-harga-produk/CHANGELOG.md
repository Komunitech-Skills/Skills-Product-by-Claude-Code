# Riwayat perubahan — strategi-harga-produk

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **1.0.9 (2026-10-03)** — dari uji ulang OpenClaw 1.0.8: AI sempat mengisi sendiri baris tabel ("~40,2%", "15%+"). Kini hitungan mencetak tabel siap salin: harga promo + margin promo + status untuk setiap harga cantik (`cantik --diskon`), harga normal minimal agar bisa diskon X% (`margin --diskon-target`), dan tabel rentang diskon di ringkasan. AI wajib menyalin tabel utuh, tanpa angka perkiraan.
- **1.0.8 (2026-10-03)** — dari uji ulang OpenClaw 1.0.7: hitungan PPN kini menampilkan terpisah margin bila harga "dibagi 1,12" (keliru), bila PPN tidak dipisah (keliru), dan margin yang benar — agar AI tidak tertukar. Dari harga lantai, AI tegas tidak menawarkan diskon dan menyebut harga normal minimal agar ada ruang diskon 5%/10%; contoh harga cantik yang aman dicetak hitungan sehingga AI tidak mengarang "misal" harga.
- **1.0.7 (2026-10-03)** — dari uji OpenClaw 1.0.6: AI sempat menulis "diskon maksimal 9%" sendiri padahal hitungan menunjukkan tidak ada ruang diskon. Kini setiap hitungan mencetak **ringkasan siap tempel** (harga, laba, margin, status, diskon maksimal, konflik reseller/agen) dan AI wajib menyalinnya apa adanya — tidak boleh menulis angka harga/diskon yang tidak dihitung. Tambahan: rentang aman harga khusus reseller/agen selama promo, pembanding volume promo marketplace terhadap jual langsung, dan peringatan bila margin terlihat besar karena PPN lupa dipisah.
