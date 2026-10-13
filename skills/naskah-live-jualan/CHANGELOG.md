# Riwayat perubahan — naskah-live-jualan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.7 (2026-10-05)
- Judul tabel kini hanya "Angka promo"; semua label proses internal dihapus dari format dan contoh. Pemeriksaan internal memakai file sementara yang dihapus dan tidak pernah disebut. Klaim "paling banyak diambil"/"stok terbatas"/"laris" dilarang kecuali Anda yang memberi datanya.

## Catatan revisi 1.0.6 (2026-10-05)
- Balasan langsung dimulai dengan naskah. Hasil pemeriksaan internal (mis. "lulus cek-silang, 0 GAGAL") tidak lagi ikut tampil; masalah yang perlu Anda lengkapi disebut dengan bahasa biasa.

## Catatan revisi 1.0.5 (2026-10-01)
- Langkah wajib baru: AI menulis dulu "Fakta dari pengguna" (hanya yang Anda sebut), lalu setiap klaim di naskah harus bisa ditelusuri ke daftar itu.
- Script baru `scripts/cek_fakta.py` mencocokkan naskah dengan pesan Anda: jam live yang tidak Anda sebut, asal produk yang dikarang ("diambil dari Pekanbaru" padahal Anda hanya bilang *kirim* dari Pekanbaru), ukuran/isi, manfaat kesehatan, reputasi, dan urgensi palsu ditandai GAGAL dan wajib diperbaiki.
- Tanpa jam mulai, rundown memakai "menit 0–3" (atau [isi: jam mulai]) — tidak lagi memakai jam 19:00 diam-diam.

## Catatan revisi 1.0.4 (2026-10-01)
- Persen diskon dan harga akhir dijaga konsisten: bila harga dibulatkan, yang diucapkan adalah persen sebenarnya atau "hemat RpX". Contoh Pashmina diperbaiki.
- Detail produk yang tidak Anda berikan ditulis [isi: ...] atau arahan aksi, tidak dikarang.
- Jam mulai yang tidak diberikan memakai menit relatif dan dicatat di Asumsi.
