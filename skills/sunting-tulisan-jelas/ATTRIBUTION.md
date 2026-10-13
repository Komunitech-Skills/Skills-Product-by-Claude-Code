# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengambil prinsip-prinsip menulis jelas yang terbukti dari kursus resmi Google, lalu menulis ulang seluruhnya dalam Bahasa Indonesia untuk tulisan kerja usaha Indonesia, dengan contoh karangan baru dan script pengukur yang ditulis sendiri oleh Komunitech.

## Sumber: Google Technical Writing One & Two (CC BY 4.0)
- **Karya:** *Technical Writing One* dan *Technical Writing Two*, kursus teknik penulisan oleh **Google**. Tautan: https://developers.google.com/tech-writing (halaman: https://developers.google.com/tech-writing/one dan https://developers.google.com/tech-writing/two).
- **Lisensi:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Pernyataan di halaman sumber (dibaca 2026-10-05): "Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License." Halaman *Two* tercatat terakhir diperbarui 2025-08-21 UTC. Contoh kode berlisensi Apache-2.0 **tidak dipakai**.
- **Pernyataan perubahan (diubah/diadaptasi):** prinsip-prinsip berikut **diadaptasi dan ditulis ulang** oleh Komunitech dalam Bahasa Indonesia: menetapkan pembaca dan tujuan; satu kalimat satu gagasan dan cara memecah kalimat panjang; kalimat aktif dan pelaku yang jelas; kata konkret; konsistensi istilah dan penjelasan singkatan; daftar bernomor vs butir; paragraf pendek dengan kalimat pembuka; menyunting diri sendiri dan menyusun dokumen panjang. Dari sana ditambahkan: penyesuaian pada kaidah kalimat Bahasa Indonesia (pasif "di-" yang wajar vs yang menyembunyikan pelaku), daftar kata pengisi/bertele/jargon/kabur Indonesia, pesan WhatsApp dan tulisan usaha, aturan "tidak mengubah fakta", pengukuran keterbacaan (`scripts/ukur_keterbacaan.py`), dan semua contoh. **Contoh, latihan, dan kalimat kursus Google tidak disalin.**
- **Tidak ada dukungan dari Google.** Google tidak berafiliasi dengan, tidak mengesahkan, dan tidak mendukung skill ini. "Google" hanya disebut sebagai asal prinsip.
- Hasil adaptasi ada di `references/prinsip-sunting.md` dan ringkasannya di `SKILL.md`; bagian itu dapat dipakai ulang dengan atribusi ini.

## Audit keamanan (pedoman kurasi Komunitech), 2026-10-05
- Hanya halaman kursus (teks) yang dibaca lewat pengambil halaman. **Tidak ada repositori yang di-clone dan tidak ada kode sumber dari sumber yang dijalankan.**
- Diperiksa pada halaman yang dibaca: instruksi tersembunyi untuk agent, perintah unduh-dan-jalankan, pengiriman data ke luar, kredensial tertanam. **Nihil**; isinya hanya materi ajar.
- `scripts/ukur_keterbacaan.py` (karya Komunitech) memakai pustaka standar saja (`argparse`, `re`, `json`, `collections`, `pathlib`); tidak ada akses jaringan, tidak ada `eval`/`exec`/`subprocess` (kecuali `tests/uji_ukur.py` yang menjalankan script itu sendiri), tidak menulis berkas, hanya membaca berkas teks yang diberikan pengguna dan `references/kata-pengisi-jargon.txt`.
- Kesimpulan: **lolos audit**.

## Pembagian lisensi
- `references/prinsip-sunting.md` dan bagian langkah kerja di `SKILL.md` yang menyangkut prinsip menulis: adaptasi materi CC BY 4.0 Google.
- Semua bagian lain (`scripts/`, `tests/`, `examples/`, `references/kata-pengisi-jargon.txt`, `README.md`): karya orisinal Komunitech. Nama, perusahaan, dan data di `examples/` fiktif.

Penggunaan keseluruhan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, kecuali bagian CC BY di atas.

## Riwayat versi
- 1.0.0 (2026-10-05): rilis awal.
