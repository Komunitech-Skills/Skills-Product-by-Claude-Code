# Atribusi

## Jalur produksi
**Kreasi orisinal Komunitech.** Alur kerja, rumus biaya sampai di tempat, skor tertimbang, sensitivitas, aturan PPN PKP/non-PKP, istilah lokal (franco/loco, DP/tempo/COD), template, pesan WA, script, tes, dan semua contoh ditulis sendiri oleh Komunitech untuk UMKM Indonesia (Rupiah, PPN 12% × 11/12, pemasok lewat WhatsApp, harga grosir bertingkat).

## Sumber ide
- **Asal ide topik:** kurasi sumber berlisensi Apache-2.0 oleh tim riset Komunitech (2026-10-05) mencatat skill `operations/vendor-review` di repo [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic; lisensi Apache License 2.0) sebagai kandidat topik "bandingkan pemasok/vendor" (gagasan umum: total biaya kepemilikan, matriks perbandingan, titik tawar). Catatan riset itu internal kurator dan tidak disertakan dalam paket.
- **Yang diambil:** hanya gagasan topik di tingkat umum, yang juga lazim dalam praktik pembelian/pengadaan.
- **Yang TIDAK diambil:** pembuat skill ini **tidak membaca teks skill sumber** saat menulis; tidak ada teks, struktur bagian, contoh, template, atau kode yang disalin atau diterjemahkan. Tidak ada repositori yang di-clone dan tidak ada kode luar yang dijalankan. Karena itu skill ini bukan karya turunan dari materi tersebut, dan teks lisensi Apache-2.0 tidak disertakan; ide asalnya tetap dicatat di sini demi keterbukaan.
- Anthropic tidak berafiliasi dengan dan tidak mengesahkan produk Komunitech ini.

## Audit keamanan (pedoman kurasi Komunitech)
`scripts/banding_pemasok.py` (karya Komunitech) hanya memakai pustaka standar Python (`argparse`, `csv`, `io`, `json`, `re`, `sys`, `decimal`); hanya membaca `--file`/`--data`/stdin yang diberikan pengguna; tidak ada akses jaringan, tidak menulis file, tidak ada `eval`/`exec`/`subprocess`. `tests/uji_regresi.py` menjalankan script itu dengan data fiktif. Isi penawaran diperlakukan sebagai data (catatan pemasok ditampilkan dengan label "data, bukan perintah").

## Data contoh
Semua nama usaha, harga, dan penawaran di `SKILL.md`, `templates/`, `references/`, dan `tests/` fiktif. Tidak ada data pribadi atau rahasia dagang nyata.

## Lisensi
Karya orisinal Komunitech; penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian. Dasar aturan pajak yang dikutip (PMK 131/2024) adalah peraturan publik.

## Riwayat versi
- 1.0.0 (2026-10-14): rilis awal.
- 1.0.1 (2026-10-14): revisi dari uji independen (ringkasan siap salin, kamus PPN, batas ongkir, rekomendasi = peringkat 1, asumsi pajak terbuka). Semua perubahan karya Komunitech.
