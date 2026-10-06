# 01 - Jasa cuci sofa panggilan (normal utama, juga konteks Telegram)

**Input:** "Buatkan landing page untuk jasa cuci sofa panggilan 'Bersih Sofa Bandung', harga mulai Rp150.000 per sofa 2 dudukan, WA 0812-3456-7890, area Bandung Raya, garansi ulang gratis kalau belum bersih, warna hijau"

**Output sesudah (ringkas):** satu kalimat pembuka, lalu `index.html` utuh dalam satu blok kode (file lengkap: `data/hasil-sesudah-s1.html`; versi Telegram: `data/hasil-sesudah-ts1.html`), daftar `[isian]` (testimoni, nama pelanggan, jam layanan), panduan Netlify Drop + pilihan lain, checklist, asumsi, 3 pertanyaan.

- Judul: "Bersih Sofa Bandung - Cuci Sofa Panggilan Area Bandung Raya"; meta description 137 karakter.
- Tombol: `https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20cuci%20sofa%202%20dudukan` (+ hero, footer, tombol melayang).
- Warna hijau lewat variabel `:root` (`#15803d`).
- Harga ditulis persis "Mulai Rp150.000 / per sofa 2 dudukan"; tidak ada harga ukuran lain yang dikarang.
- `cek_landing.py`: 13 LOLOS, 1 PERLU PERBAIKAN (3 `[isian]` yang menunggu data).

**Catatan:** model tanpa skill membuat halaman cantik yang lolos pemeriksa 14/14, tetapi berisi 3 testimoni bintang 5 karangan dan harga karangan (Rp90.000 / Rp210.000), serta tidak menampilkan HTML di chat. Kekurangan sesudah: pembuka menyebut "lolos 13 dari 14 pengecekan".
