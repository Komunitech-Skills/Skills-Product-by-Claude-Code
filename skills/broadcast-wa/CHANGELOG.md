# Riwayat perubahan — broadcast-wa

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.12 (2026-10-13)
- Rujukan UU PDP ditulis lengkap: UU 27/2022 tentang Pelindungan Data Pribadi (tanpa perubahan cara kerja).

## Catatan revisi 1.0.11 (2026-10-13)
- Rujukan ke skill arsip diganti: `caption-sosmed-umkm`, `kalender-konten-30hari` diganti `konten-mingguan` (SKILL.md, bagian Kapan TIDAK digunakan).

## Catatan revisi 1.0.10 (2026-10-03)
- ATURAN WAJIB baru: draf teks pada jalur penolakan (tanpa file kontak) juga wajib lolos `cek_fakta.py`; klaim/urgensi karangan ("Hari ini ada promo", "Khusus hari ini", "sebelum kehabisan") dilarang.
- `cek_fakta.py` menambah deteksi "hari ini ada promo", "promo hari ini", "mumpung promo"; tes regresi ditambah.

## Catatan revisi 1.0.9 (2026-10-01)
- Cek fakta kini **otomatis di dalam perintah utama** (`siapkan_broadcast.py`) dan tidak bisa dilewati: klaim yang tidak disebut pemilik ("Khusus hari ini", "sebelum kehabisan", "promo terakhir", "buruan", "jangan sampai ketinggalan", "waktu terbatas", "stok terbatas", dst.) membuat script **GAGAL** dan tidak menghasilkan file siap kirim, dengan atau tanpa `--fakta-file`.
- Daftar frasa urgensi di `cek_fakta.py` diperluas; tes regresi ditambah.

## Catatan revisi 1.0.8 (2026-10-01)
- Kolom **Sapaan/Panggilan** di file kontak kini dipakai ("Bu Siti", "Pak Fajar"), tidak lagi diganti "Kak".
- Versi daftar siaran (tanpa nama) dipisah jelas dan ditolak bila masuk ke daftar kirim personal.
- Pemeriksaan anti-karang: klaim seperti "stok terbatas", "terlaris", "halal" ditolak bila tidak disebut pemilik (`--fakta-file`).
- Kolom "Setuju Promo" dikenali otomatis sebagai kolom persetujuan.
