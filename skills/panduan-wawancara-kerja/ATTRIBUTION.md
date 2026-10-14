# Atribusi

## Jalur produksi
**Kreasi orisinal Komunitech, dengan asal ide dari hasil kurasi.** Isi skill ini (kompetensi, bank pertanyaan, tes praktik, rubrik, kartu skor, aturan pertanyaan terlarang, script hitung skor, tes, templat, contoh data) ditulis sendiri oleh Komunitech dari pengetahuan umum tentang wawancara terstruktur dan dari praktik rekrutmen usaha kecil di Indonesia, untuk pasar Indonesia (Rupiah, UMKM, WhatsApp, UU 13/2003, SE Menaker M/6/HK.04/V/2025, UU 27/2022).

## Asal ide
- **Repo:** [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic), lisensi Apache License 2.0.
- **Skill sumber ide:** `human-resources/interview-prep` (skill ringkas untuk menyusun wawancara terstruktur), tercatat pada kurasi internal Komunitech tanggal 2026-10-05.
- **Ide yang dipakai (gagasan umum, bukan teks):** wawancara terstruktur mengikuti urutan kompetensi, bank pertanyaan, rubrik skor berjangkar perilaku, lalu pembahasan (debrief) setelah wawancara.
- **Yang tidak dilakukan:** pembuat skill ini **tidak membaca teks skill sumber** saat menulis dan **tidak menyalin** kalimat, contoh, templat, atau kode apa pun darinya. Tidak ada repositori yang di-clone dan tidak ada kode luar yang dijalankan. Karena tidak ada materi sumber yang disalin atau diadaptasi, tidak ada berkas `LICENSE-APACHE` atau pernyataan perubahan Apache-2.0 yang perlu disertakan; asal ide dicatat di sini untuk penelusuran. Bila kelak ada bagian yang diadaptasi dari teks sumber, versi berikutnya wajib menyertakan teks lisensi Apache-2.0 dan pernyataan perubahan.

## Dasar aturan yang diringkas
Ringkasan di `references/aturan-pertanyaan.md` merujuk ke UU 13/2003 tentang Ketenagakerjaan, UU 6/2023 (Cipta Kerja), UU 8/2016 tentang Penyandang Disabilitas, UU 27/2022 tentang Pelindungan Data Pribadi, dan SE Menaker M/6/HK.04/V/2025 tentang larangan diskriminasi dalam rekrutmen. Peraturan perundang-undangan bukan karya yang dilindungi hak cipta; ringkasannya ditulis sendiri. Tautan sumber resmi diambil dari referensi yang sudah ada di pustaka Komunitech (skill `lowongan-kerja` dan `seleksi-cv-pelamar`). Bagian yang bertanda PERLU REVIEW belum dicocokkan ke naskah resmi pasal per pasal.

## Audit keamanan (pedoman kurasi Komunitech)
`scripts/skor_wawancara.py` (karya Komunitech) hanya memakai pustaka standar Python (`argparse`, `json`, `sys`, `decimal`, `fractions`, `pathlib`); hanya membaca berkas JSON yang diberikan pengguna, tidak ada akses jaringan, tidak ada `eval`/`exec`/`subprocess`, tidak menulis atau mengubah berkas apa pun, menolak berkas lebih dari 2 MB, dan menganggap semua teks di dalam data sebagai data biasa. Semua nama, skor, angka, dan skenario di `templates/`, `references/`, dan `tests/` fiktif; kemiripan dengan orang atau usaha nyata tidak disengaja. Tidak ada API key, token, atau data pribadi.

## Merek pihak ketiga
QRIS, WhatsApp, Instagram, Excel, Canva, CapCut, Shopee, dan nama sejenis hanya disebut sebagai contoh alat atau kanal kerja. Tidak berafiliasi dengan merek mana pun. Anthropic tidak berafiliasi dengan dan tidak mengesahkan produk Komunitech ini.

## Lisensi
Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian.

## Riwayat versi
- 1.0.0 (2026-10-14): rilis awal (status draf).
- 1.0.1 (2026-10-14): perbaikan dari temuan uji independen; tidak ada materi pihak ketiga yang ditambahkan.
