# Atribusi

## Jalur produksi
**Kreasi orisinal Komunitech.** Template HTML/CSS, aturan isi, script `scripts/cek_landing.py`, tes, dan panduan tayang ditulis sendiri oleh Komunitech. Tidak ada teks, kode, atau template dari proyek lain yang disalin.

## Sumber fakta eksternal
Langkah tayang dicocokkan dengan dokumentasi resmi (diperiksa 2026-10-06): docs.netlify.com (Netlify Drop), docs.github.com (GitHub Pages), developers.cloudflare.com (Pages Direct Upload). Antarmuka mereka bisa berubah; ditandai PERLU REVIEW di panduan.

## Audit keamanan
`scripts/cek_landing.py`: Python standar (`re`, `sys`, `os`, `html.parser`), hanya membaca file yang diberikan, tanpa jaringan, tanpa `eval`/`exec`/`subprocess`, tidak menulis file. Data contoh di tes fiktif.

## Merek pihak ketiga
Netlify, GitHub, Cloudflare, WhatsApp, cPanel hanya disebut sebagai nama layanan. Tidak berafiliasi.

## Riwayat versi
- 1.0.0 (2026-10-06): rilis awal (status uji).
