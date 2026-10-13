# Riwayat perubahan — proses-pesanan-wa

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.1 (2026-10-06)
- Revisi dari uji OpenClaw (skor 5,5 naik ke 8,4): nota ditulis utuh untuk setiap pesanan, juga di Telegram/chat (tidak boleh "sama format di atas"); bila lebih dari 5 pesanan, nota digabung dalam satu blok tetapi tetap lengkap per pesanan.
- Template pesan "pesanan dikirim + resi" selalu disertakan. Item dengan varian atau produk yang tidak ada di katalog tidak masuk label, serah-terima, dan total; total sementara ditampilkan untuk item yang pasti dan varian itu ditanyakan ke pelanggan lewat draf.
- Sapaan mengikuti yang dipakai pelanggan/pemilik (Bu/Pak/Kak); paket yang belum lunas (non-COD) tidak masuk daftar serah-terima kurir tetapi ditulis di "menunggu pembayaran". Berkas kerja sementara berisi HP atau alamat dihapus setelah hasil diberikan.
- Script `rekap_pesanan.py` memberi peringatan bila harga dari chat tidak terbaca atau tidak wajar (dipakai harga katalog bila ada, selain itu ditandai belum diketahui).

## Catatan revisi 1.0.0 (2026-10-06)
- Rilis awal.
