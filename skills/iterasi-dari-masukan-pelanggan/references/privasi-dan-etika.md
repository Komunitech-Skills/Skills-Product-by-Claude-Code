# Privasi & etika data masukan
- Yang disamarkan otomatis oleh script: nama pengirim chat, nomor HP, email, tautan, @akun, nomor pesanan/resi/kode panjang, alamat jalan,
  sapaan+nama ("kak Budi"). Kolom nama/username/email di CSV tidak pernah dibaca.
- Tidak sempurna: nama tanpa sapaan di tengah kalimat, nama tempat kerja, foto/gambar, tanda tangan bisa lolos. Agent WAJIB membaca
  ulang kutipan sebelum masuk laporan dan menyamarkan sisa yang ketemu.
- Ekspor chat WhatsApp: minta izin bila chat grup berisi pelanggan lain; pakai hanya chat usaha (bukan chat pribadi).
- Simpan file mentah (chat asli) di komputer pemilik, hapus setelah dianalisis bila tidak perlu. Jangan unggah ke layanan lain.
- Hanya `--simpan-anonim` yang aman dibagikan ke tim; file mentah tidak.
- Jangan hubungi pelanggan lewat nomor yang diambil dari ekspor untuk promosi. Tindak lanjut hanya untuk masukan yang mereka kirim sendiri,
  dan pengiriman dilakukan manusia.
- Ulasan/komentar publik: analisis untuk perbaikan sendiri; jangan mengumpulkan data lewat login browser atau scraping.
