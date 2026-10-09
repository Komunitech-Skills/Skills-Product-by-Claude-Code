# 01 - Jasa cuci sofa panggilan (normal utama, juga konteks Telegram)

**Input:** "Buatkan landing page untuk jasa cuci sofa panggilan 'Bersih Sofa Bandung', harga mulai Rp150.000 per sofa 2 dudukan, WA 0812-3456-7890, area Bandung Raya, garansi ulang gratis kalau belum bersih, warna hijau"

**Output sesudah (ringkas):** satu kalimat pembuka, lalu `index.html` utuh dalam satu blok kode (file lengkap: `data/hasil-sesudah-s1.html`; versi Telegram: `data/hasil-sesudah-ts1.html`), daftar `[isian]` (testimoni, nama pelanggan, jam layanan), panduan Netlify Drop + pilihan lain, checklist, asumsi, 3 pertanyaan.

- Judul: "Bersih Sofa Bandung - Cuci Sofa Panggilan Area Bandung Raya"; meta description 137 karakter.
- Tombol: `https://wa.me/6281234567890?text=Halo%2C%20saya%20mau%20pesan%20cuci%20sofa%202%20dudukan` (+ hero, footer, tombol melayang).
- Warna hijau lewat variabel `:root` (`#15803d`).
- Harga ditulis persis "Mulai Rp150.000 / per sofa 2 dudukan"; tidak ada harga ukuran lain yang dikarang.
- `cek_landing.py`: 13 LOLOS, 1 PERLU PERBAIKAN (3 `[isian]` yang menunggu data).

**Catatan:** model tanpa skill membuat halaman cantik yang lolos pemeriksa 14/14, tetapi berisi 3 testimoni bintang 5 karangan dan harga karangan (Rp90.000 / Rp210.000), serta tidak menampilkan HTML di chat. Kekurangan sesudah: pembuka menyebut "lolos 13 dari 14 pengecekan".

## Uji ulang 1.0.1 (2026-10-06)
**Output sesudah:** pembuka "Ini halaman untuk Bersih Sofa Bandung, siap disalin dan ditayangkan." lalu `index.html` utuh (file: `data/hasil-sesudah-v101-s1.html`; Telegram: `data/hasil-sesudah-v101-ts1.html`), daftar `[isian]`, Netlify Drop + alternatif + CNAME, checklist, asumsi, 3 pertanyaan.
- Tidak ada lagi "lolos X dari 14 pengecekan" atau path; pemeriksa: 14 lolos, 1 PERLU PERBAIKAN (hanya `[isian]`).
- WA `6281234567890` (4 tautan) & "Mulai Rp150.000" benar; tidak ada harga/testimoni karangan.
- Nilai: lokal 8,5 (sisa: "disimpan di workspace", "tanpa biaya tersembunyi"), Telegram 9.
