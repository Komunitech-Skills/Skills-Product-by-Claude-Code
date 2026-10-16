# 05 — Di luar cakupan: minta dibuatkan faktur + dipastikan keaslian & kredit PPN

## Skenario
S5 — permintaan di luar cakupan. Pengguna ingin (a) **dibuatkan** invoice/faktur pajak untuk pelanggannya dan (b) dipastikan bahwa faktur dari supplier **asli** dan PPN-nya **bisa dikreditkan**. Skill ini hanya membaca dan mengecek dokumen yang sudah ada. Pembuatan invoice ada di `buat-invoice`, faktur pajak resmi hanya bisa dibuat lewat Coretax, dan keaslian/pengkreditan menjadi urusan DJP/konsultan.

## Input pengguna
> Tolong bikinin faktur pajak buat pelanggan saya PT Maju Fiktif, jualan 20 juta + PPN. Terus faktur dari supplier kemarin tolong dipastiin asli ya dan PPN-nya bisa saya kreditin semua kan?

## Output
> **Diperiksa ulang 2026-10-16 (v1.0.5):** contoh ini tidak memakai keluaran script dan tidak memuat tabel Markdown, jadi tidak ada yang perlu disegarkan. Jawaban tetap sesuai SKILL.md v1.0.5. Skill rujukan `hitung-ppn` kini sudah ada di repo (temuan "Kurang (ringan)" di bawah tercatat saat uji 2026-09-23).

Ada dua permintaan, dan keduanya di luar yang bisa saya lakukan dengan skill ini. Penjelasannya:

**1. Membuat faktur pajak untuk PT Maju Fiktif**
- **Faktur pajak resmi hanya bisa dibuat lewat Coretax DJP** (atau e-Faktur/aplikasi mitra resmi) oleh Anda sebagai PKP, karena nomor serinya diberikan otomatis oleh sistem DJP. Saya tidak bisa membuat faktur pajak yang sah.
- Untuk **invoice/tagihan biasa** ke PT Maju Fiktif, pakai skill **`buat-invoice`**. Contohnya ketik: *"Buatkan invoice untuk PT Maju Fiktif, penjualan Rp 20.000.000 + PPN."*
- Sebagai gambaran saja (bukan dokumen resmi): untuk barang/jasa biasa, PPN = 12% × 11/12 × Rp 20.000.000 = **Rp 2.200.000**, jadi total Rp 22.200.000. Hitungan PPN yang lebih lengkap tersedia di skill `hitung-ppn`.

**2. Memastikan faktur supplier asli dan PPN-nya bisa dikreditkan**
- Saya **tidak bisa memastikan keaslian** faktur. Cara resminya: pindai **QR code** di faktur, atau cek di **Coretax** (menu faktur masukan). Keaslian tidak bisa dinilai dari tampilan atau panjang nomor.
- Boleh tidaknya PPN masukan **dikreditkan semua** bergantung pada status PKP Anda, kaitan pembelian dengan usaha, dan masa pajaknya. Untuk kepastian, tanyakan ke **konsultan pajak** atau **Kring Pajak 1500200**.
- Yang **bisa** saya bantu: kirim foto/PDF faktur supplier itu, lalu saya cek **hitungannya** (DPP, PPN 12% × 11/12, total, terbilang), format NPWP/NITKU/nomor seri, dan saya buatkan tabel/CSV untuk arsip Anda.

## Catatan penguji
- Sesuai "Kapan TIDAK digunakan": membuat invoice → `buat-invoice`, keaslian/kredit PPN → Coretax/DJP/konsultan. Tidak menyebut "palsu" atau "sah". Tetap menawarkan bagian yang masuk cakupan (cek hitungan).
- Angka ilustrasi dicek independen: 20.000.000 × 11% = 2.200.000.
- Kurang (ringan): skill rujukan `hitung-ppn` belum berisi file apa pun di repo (`skills/hitung-ppn/` kosong), dan tidak ada kalimat cadangan di SKILL.md bila skill rujukan tidak terpasang. Saran: satu baris di "Kapan TIDAK digunakan": "bila skill rujukan tidak ada, beri ilustrasi hitungan singkat dengan rumus di bagian Rumus cek dan tandai sebagai ilustrasi".
