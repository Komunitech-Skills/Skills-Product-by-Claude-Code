# Atribusi

## Jalur produksi
Kreasi orisinal Komunitech lewat **tulis ulang bersih** (disetujui pemilik 2026-10-06). Agen pembuat hanya membaca daftar ide ringkas di catatan riset internal kurator (tidak disertakan dalam paket); tidak membaca atau menyalin dokumen sumber. Lisensi: Proprietary Komunitech; tunduk LISENSI.txt paket.

## Sumber ide
Konsep umum keamanan pangan (zona suhu bahaya, kontaminasi silang, kebersihan karyawan, FIFO, pencatatan) yang merupakan pengetahuan ilmiah umum. Tidak ada teks sumber yang disalin. Aturan Indonesia hanya disebut nama; PERLU REVIEW.

## Audit keamanan
`scripts/cek_log_suhu.py` hanya memakai pustaka standar Python, membaca CSV yang diberikan pengguna, tanpa jaringan, tanpa eval/exec/subprocess. Data di `tests/` fiktif.

## Riwayat versi
- 1.0.0 (2026-10-06): rilis awal (status uji).
- 1.0.1 (2026-10-06): perbaikan script log suhu (lihat SKILL.md).
- 1.0.2 (2026-10-12): verifikasi fakta ke sumber resmi (WHO Five Keys 2006, FDA Food Code 2022, USDA FSIS, Peraturan BPOM 31/2018 jo. 20/2021, UU 33/2014 & PP 42/2024, BPJPH 2026); URL di `references/`. Angka/aturan hanya ditulis ulang, tidak ada teks sumber yang disalin.
