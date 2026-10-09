# Atribusi

## Jalur produksi
**Karya orisinal Komunitech** (jalur "tulis ulang bersih"). Alur kerja, skala nilai, aturan respons, tabel, template, script, tes, dan semua contoh ditulis sendiri untuk pasar Indonesia (Rupiah, BPJS, konteks OJK, risiko banjir/gempa lokal).

## Sumber ide
Ide umum (peta risiko, skor kemungkinan x dampak, empat respons terhadap risiko, dana darurat usaha, pertanyaan ke agen) terinspirasi materi pendidikan publik pemerintah AS. Tidak ada teks, struktur, contoh, atau kode yang disalin; pembuat skill tidak membaca materi aslinya.

## Keamanan
`scripts/cek_risiko.py` memakai pustaka standar saja (`argparse`, `json`, `sys`); hanya membaca berkas JSON yang diberikan, tanpa jaringan, tanpa `eval`/`exec`/`subprocess`. Data contoh fiktif. Tunduk pada `LISENSI.txt` paket.

## Riwayat versi
- 1.0.0 (2026-10-09): rilis awal (status draft).
- 1.0.1 (2026-10-09): parser angka ketat (desimal/ambigu ditolak), nama biaya dobel ditolak, kategori tidak bisa diasuransikan, aturan jarang-tapi-berat, cicilan menabung.
