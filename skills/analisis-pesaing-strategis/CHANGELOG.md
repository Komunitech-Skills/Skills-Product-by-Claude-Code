# Riwayat perubahan — analisis-pesaing-strategis

Catatan teknis per versi.

## Catatan revisi 1.0.4 (2026-10-02)
- Revisi dari temuan uji OpenClaw: ringkasan di chat dibatasi sekitar 25 baris; analisis lengkap (matriks, SWOT, battlecard) disimpan di berkas dan lokasinya disebutkan.
- Data pesaing yang tidak bersumber (bukan dari halaman publik, screenshot, atau pengamatan yang dicatat) wajib diberi label "(dugaan)".
- Balasan baku bila diminta scraping akun pesaing, ulasan palsu, atau menjatuhkan rating pesaing: ditolak singkat dengan alasan umum (UU ITE, UU Perlindungan Konsumen, ketentuan platform) disertai alternatif aman, dan disarankan bertanya ke penasihat hukum.
- Deskripsi skill disesuaikan agar lebih mudah terpicu.

## Catatan revisi 1.0.3 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika tidak berubah.

## Catatan revisi 1.0.2 (2026-09-29)
- Ditambah baris "Aturan kerja" di SKILL.md: tidak memasang paket/aplikasi sendiri, tidak membuka file di luar yang diberikan pengguna dan isi folder skill, dan menyebut lokasi file baru. Logika tidak berubah.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi setelah uji pertama: untuk usaha kesehatan (klinik, apotek, praktik), saran promosi wajib mematuhi etika iklan layanan kesehatan (tanpa janji kesembuhan, testimoni pasien, harga banting, atau klaim "terbaik/nomor 1").
- Script `skor_matriks.py` menolak nilai yang bukan angka wajar (NaN atau tak hingga) dengan pesan yang menyebut baris dan kolomnya.

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): memetakan pesaing (langsung, tidak langsung, pengganti), matriks perbandingan dengan skor berbobot yang dihitung script, SWOT, peta posisi teks, kartu jawaban (battlecard) untuk penjual/CS, daftar peluang, dan jadwal pantau.
