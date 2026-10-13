> **Sumber keluaran:** penguji independen Akun B, 2026-10-13, Claude Code (simulasi agent), data fiktif; menggantikan contoh lama yang memuat angka tanpa sumber.

# Contoh 01 — Deskripsi Produk Marketplace (Sepatu Lari), mode Perbaiki

## Input pengguna
"Perbaiki deskripsi produk sepatu lari ini biar nggak kelihatan AI banget:

Di era digital ini, belanja online menjadi kebiasaan banyak orang. Sepatu lari kami tidak hanya nyaman, tetapi juga stylish untuk dipakai sehari-hari. Solusi terbaik nomor satu untuk kamu yang aktif! Bahan breathable, ringan, dan tahan lama menjadi kunci kenyamanan kaki seharian. Tak bisa dipungkiri, kualitas sol karetnya sangat penting untuk cengkeraman di jalan. Yuk simak detail produk selengkapnya! Semoga bermanfaat dan selamat berbelanja! 🔥🔥✨"

## Output

✏️ Tulisan hasil perbaikan:

> Sepatu lari kami nyaman dan stylish untuk dipakai sehari-hari. Cocok buat kamu yang aktif. Bahannya breathable, ringan, dan tahan lama, jadi kaki enak dipakai seharian. Sol karetnya menjaga cengkeraman di jalan. Ada pertanyaan soal produk? Chat kami ya.

**Yang diubah:**
- Pembuka basa-basi ("Di era digital ini, belanja online menjadi kebiasaan banyak orang") → dihapus, langsung masuk ke produk.
- Kontras biner palsu ("tidak hanya nyaman, tetapi juga stylish") → "nyaman dan stylish". Isinya sama, tanpa struktur "tidak hanya... tetapi juga".
- Klaim superlatif tanpa bukti ("Solusi terbaik nomor satu") → dihapus karena tidak ada data pendukung di draf Anda. Yang dipertahankan hanya sasaran pembelinya: "Cocok buat kamu yang aktif".
- "Menjadi kunci" → label kepentingannya dibuang, tiga sifat bahan (breathable, ringan, tahan lama) tetap dan disambung ke manfaat dari draf Anda sendiri: kaki enak dipakai seharian.
- "Tak bisa dipungkiri... sangat penting untuk" → jadi kalimat fakta langsung: "Sol karetnya menjaga cengkeraman di jalan."
- Ajakan generik ("Yuk simak...") dan penutup klise ("Semoga bermanfaat dan selamat berbelanja!") → diganti satu ajakan netral: "Ada pertanyaan soal produk? Chat kami ya."
- Emoji berderet (🔥🔥✨) → dihapus. Ini deskripsi produk, jadi dibuat fokus ke fakta.

Yang sengaja tidak saya tambahkan: harga, ukuran, warna, stok, atau janji pengiriman, karena tidak ada di draf Anda. Klaim "tahan lama" dan "cengkeraman di jalan" berasal dari draf Anda, jadi pastikan memang sesuai kenyataan produknya.

Kalau mau deskripsinya lebih lengkap, kirim ukuran yang tersedia, pilihan warna, dan detail bahan sol, nanti saya masukkan persis seperti yang Anda tulis.

## Catatan penguji
- **Mode:** Perbaiki. Pengguna menempel draf dan meminta diperbaiki (tabel Input SKILL.md). Konteks: deskripsi produk marketplace, sesuai ucapan pengguna.
- **Skrip `scripts/cek_pola.py`** (dijalankan langsung, tidak diedit): draf **49/100**, 10 kemunculan dari 8 pola berbeda (kutipan "Tak bisa dipungkiri..." dan "Solusi terbaik nomor satu..." terhitung dua kali karena dua frasa berbeda cocok di kalimat yang sama, jadi skor sedikit lebih rendah dari jumlah pola sebenarnya). Hasil perbaikan **100/100**, tidak ada pola tersisa. Skor ini heuristik pencocokan kata, bukan "persen AI".
- **Cek fakta per kata (Langkah kerja #4):** semua isi hasil perbaikan ada di draf asli: nyaman, stylish, sehari-hari, kamu yang aktif, breathable, ringan, tahan lama, kaki seharian, sol karet, cengkeraman di jalan. Satu-satunya tambahan adalah ajakan netral "Chat kami ya" (setara "hubungi kami" yang dibolehkan SKILL.md).
- **Jumlah kalimat inti dipertahankan:** draf 7 kalimat; 2 kalimat murni basa-basi dihapus (pembuka dan penutup), 5 kalimat sisanya jadi 5 kalimat.
- **Tiga-serangkai "breathable, ringan, dan tahan lama" tidak dibuang**, karena ketiganya fakta konkret dari draf, bukan kata sifat generik yang diulang di banyak kalimat (pola #6). Skrip juga tidak menandainya.
- **Sengaja TIDAK diklaim karena tidak bersumber:** ukuran, warna, harga, stok, kecepatan kirim, jenis permukaan jalan, manfaat tambahan produk ("tidak bikin kaki panas" dan sejenisnya), kebiasaan atau aturan platform tentang emoji di kolom deskripsi, serta efek ke penjualan atau peringkat pencarian. Tulisan juga tidak dijanjikan "lolos detektor AI".
- **Hal yang tidak bisa diverifikasi penguji:** apakah sepatu itu benar breathable, tahan lama, dan cengkeramannya baik. Itu klaim dari pengguna (fiktif di contoh ini) dan sudah diingatkan di Output agar dicocokkan dengan produk aslinya.
