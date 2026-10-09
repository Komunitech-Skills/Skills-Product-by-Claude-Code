# Contoh 4: Input tidak lengkap

**Input:** "Bikinin nama bisnis dong."
**Jawaban agent (satu pesan, tanpa mengarang):**
> Siap! Biar namanya pas, jawab singkat ya:
> 1. Jual apa (produk/jasa)? 2. Siapa pembelinya dan di kota mana? 3. Kesan nama: kalem, gaul, daerah, atau Inggris? 4. Ada kata yang wajib atau harus dihindari? 5. Merek/pesaing yang kamu tahu (5-10 nama) supaya saya periksa kemiripannya?
> Kalau mau cepat, balas "cepat" dan saya buatkan 10 opsi dengan asumsi: usaha kecil online, gaya ramah, Bahasa Indonesia, 2-3 suku kata. Kemiripan dengan merek lain akan tertulis "belum diperiksa".

**Bila pengguna membalas "cepat" tanpa produk:** agent tetap meminta jenis produk/jasa dalam satu kalimat, karena nama tanpa produk tidak bisa dinilai kolom `relevan`.
**Data rusak (script):** CSV berisi `khas` = 9 -> `GAGAL: baris 2: 'khas' harus bilangan bulat 1-5, bukan '9'`; agent memperbaiki baris itu dan menjalankan ulang.
