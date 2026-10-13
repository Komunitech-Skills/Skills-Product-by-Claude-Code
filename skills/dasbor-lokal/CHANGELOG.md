# Riwayat perubahan — dasbor-lokal

Catatan teknis per versi.

## Catatan revisi 1.0.4 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.3 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).
- Uji ulang akhir: skor 9/10.

## Catatan revisi 1.0.2 (2026-09-29)
- Alat ke-7 ditambahkan: `kpi-tim` (database `kpi.db` dari `skor_kpi.py ekspor-db`) dengan 5 query siap pakai: `perusahaan-tren`, `divisi-terbaru`, `orang-terbaru`, `tren-orang`, `kpi-merah`. Blok `kpi` ditambahkan di `templates/metadata.yml`.
- Skor per orang adalah data pribadi karyawan: dasbor tetap hanya di `127.0.0.1` dan disarankan memakai `--anonim` di `ekspor-db` bila layar dilihat orang lain. Uji regresi 25/25.

## Catatan revisi 1.0.1 (2026-09-28)
- Revisi temuan rendah: di mode teks, angka bulat dari kolom desimal SQLite (mis. stok) ditampilkan `25`, bukan `25.0`; nilai pecahan asli (`25.5`) dan kolom Rupiah tidak berubah. Uji regresi 22/22.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): dasbor lokal hanya-baca di atas database SQLite alat Komunitech (buku-stok, kasir-lokal, crm-wa, absensi-lokal, buku-piutang, kas-umkm). Menemukan file database, menjalankan query siap pakai, dan menyiapkan perintah Datasette read-only/immutable di `127.0.0.1`; `scripts/dasbor.py` menjadi jalur cadangan tanpa Datasette.
