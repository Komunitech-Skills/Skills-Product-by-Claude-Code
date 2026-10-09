# Sumber: Google Technical Writing One & Two (2026-10-05)

| Item | Isi |
|---|---|
| Nama | Technical Writing One; Technical Writing Two (kursus penulisan teknis) |
| URL | https://developers.google.com/tech-writing (halaman `/one` dan `/two`) |
| Pembuat | Google (tim Technical Writing, developers.google.com) |
| Pembaruan terakhir | Halaman *Two*: 2025-08-21 UTC (unit baru "Using LLMs") |
| Lisensi | **CC BY 4.0** untuk konten halaman; contoh kode Apache-2.0 (tidak dipakai). Kalimat lisensi dibaca langsung di halaman *One* dan *Two* |
| Sinyal bukti | Pembuat resmi vendor besar; kursus dipakai luas & dirawat; materi dirujuk dalam dokumentasi pengembang (sinyal ringkas dari riset `kurasi-bsd-cc-2026-10-05.md`: C, K, I, U) |
| Keputusan | **Diterima** (ATM, CC BY 4.0). Hanya PRINSIP yang diambil dan ditulis ulang dalam Bahasa Indonesia; contoh/latihan kursus tidak disalin |
| Hasil | `skills/sunting-tulisan-jelas` v1.0.0 (status `uji`), tier_usulan `ecer` Rp59.000 |

## Yang dibaca
Halaman ringkasan unit *One* (kata, kalimat aktif, kalimat jelas, kalimat pendek, daftar & tabel, paragraf, audiens, dokumen, tanda baca, Markdown) dan *Two* (sunting mandiri, mengorganisasi dokumen besar, ilustrasi, contoh kode, LLM) melalui pengambil halaman teks.

## Audit keamanan (Tahap 3)
- Hanya teks halaman yang dibaca; tidak ada skrip/kode dijalankan, tidak ada repositori di-clone.
- Tidak ditemukan instruksi tersembunyi, perintah unduh-jalankan, atau pengiriman data ke luar. **Lolos.**

## Yang diambil (prinsip, ditulis ulang)
Pembaca & tujuan dulu; satu kalimat satu gagasan; kalimat aktif/pelaku jelas; kata konkret; istilah konsisten & singkatan dijelaskan; daftar bernomor vs butir; paragraf pendek dengan kalimat pembuka; sunting mandiri; struktur dokumen panjang.

## Nilai tambah Komunitech
Kaidah kalimat Indonesia (pasif "di-" yang wajar vs menyembunyikan pelaku); daftar kata pengisi/bertele/jargon/kabur Indonesia; tulisan usaha (email klien, pengumuman karyawan, deskripsi produk, WA); aturan "tidak mengubah fakta" + pencocokan angka/tanggal otomatis; ukuran keterbacaan (`ukur_keterbacaan.py`, stdlib, 9 uji); contoh Indonesia baru; pola "kerjakan dulu, tanya di akhir".

## Bedanya dengan skill sendiri
`tulisan-tanpa-kesan-ai` menghilangkan pola ciri AI; `surat-resmi` memformat surat; `sop-writer` menyusun SOP. Skill ini menyunting tulisan kerja apa pun demi kejelasan.
