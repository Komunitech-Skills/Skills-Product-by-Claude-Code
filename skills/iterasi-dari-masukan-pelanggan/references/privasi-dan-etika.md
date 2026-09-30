# Privasi & etika data masukan
- Yang disamarkan otomatis oleh script: nama pengirim chat (tanpa ikut menyamarkan sapaan "kak"), nomor HP & telepon rumah, email, tautan,
  @akun, nomor pesanan/resi/kode panjang, alamat jalan/gang/perumahan/blok/RT-RW, plat nomor, "a.n. Nama", "Saya/nama saya Nama",
  sapaan+nama ("kak Budi", "mba Sari Lestari", "makasih kak rina"). Kolom nama/username/email/no. pesanan di CSV tidak pernah dicetak
  atau disimpan; isinya hanya dipakai di memori untuk mengenali baris ganda.
- Plat nomor = kode wilayah Indonesia + 1-4 angka + 1-3 huruf dengan spasi konsisten ("B 1234 XYZ", "B1234XYZ"); kode model produk
  ("Sony A7 III", "Galaxy S23 FE") dibiarkan. Kata sifat sesudah sapaan ("Mas telaten", "kak sigap") bukan nama; kata sifat yang lazim
  jadi nama (Bagus, Indah ...) bisa lolos tanpa disamarkan - baca ulang kutipannya.
- Tidak sempurna: nama tanpa sapaan di tengah kalimat, nama tempat kerja, foto/gambar, tanda tangan bisa lolos. Agent WAJIB membaca
  ulang kutipan sebelum masuk laporan dan menyamarkan sisa yang ketemu.
- Ekspor chat WhatsApp: minta izin bila chat grup berisi pelanggan lain; pakai hanya chat usaha (bukan chat pribadi).
- Simpan file mentah (chat asli) di komputer pemilik, hapus setelah dianalisis bila tidak perlu. Jangan unggah ke layanan lain.
- Hanya `--simpan-anonim` yang aman dibagikan ke tim; file mentah tidak.
- Jangan hubungi pelanggan lewat nomor yang diambil dari ekspor untuk promosi. Tindak lanjut hanya untuk masukan yang mereka kirim sendiri,
  dan pengiriman dilakukan manusia.
- Ulasan/komentar publik: analisis untuk perbaikan sendiri; jangan mengumpulkan data lewat login browser atau scraping.
