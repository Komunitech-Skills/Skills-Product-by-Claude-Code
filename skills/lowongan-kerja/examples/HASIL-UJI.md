# Hasil Uji – lowongan-kerja

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/anti-diskriminasi.md`, `references/contoh-posisi.md` (tidak ada script)
- **Metode:** 5 skenario dijalankan dengan berperan sebagai agent yang memuat SKILL.md dan mengikuti langkahnya persis, ditambah 1 uji A/B (S1 tanpa skill). Hitungan kata versi IG/WA diukur dengan `wc -w`. Tanggal batas lamaran (14 hari dari 23 September 2026 = Rabu, 7 Oktober 2026) dicek dengan Python.

## Audit keamanan
Tidak ada script, perintah shell, akses jaringan, atau pembacaan kredensial. SKILL.md dan file referensi tidak memuat instruksi tersembunyi atau prompt injection. Skill justru menambah perlindungan: menolak syarat diskriminatif, memperingatkan modus penipuan (biaya seragam/pelatihan), dan mengingatkan soal data pribadi pelamar (UU 27/2022 tentang PDP). **Aman.**

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B: S1 tanpa skill | Tanpa skill, syarat diskriminatif ikut tercantum, benefit dikarang, dan KTP diminta sejak melamar. Dengan skill **jauh lebih baik**. |
| 01 | Admin keuangan + 4 syarat diskriminatif | Sangat baik. Semua syarat dihapus dengan dasar aturan dan pengganti, ada 3 versi kanal, screening relevan. |
| 02 | "bikinin dong" kurir, WA saja | Baik. Menghormati permintaan satu kanal. Placeholder jam kerja ada di teks siap-kirim. |
| 03 | Cek loker lama (usia, tinggi, belum menikah, bayar seragam) | Sangat baik. Semua masalah dan pola penipuan terdeteksi. Format "hasil cek" adalah inisiatif agent. |
| 04 | "buatin loker sales ya" | Sangat baik. Bertanya sekali (5 pertanyaan) dan menawarkan opsi cepat. |
| 05 | Kontrak PKWT + PPh 21 | Baik. Diarahkan ke `perjanjian-sederhana` dan kalkulator/konsultan, tanpa angka pajak. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci ID/EN lengkap (loker, lowongan, job posting, hiring ad), kanal disebut, batas cakupan jelas. |
| Kemudahan awam | 9 | Satu kalimat sudah cukup. Hasil siap tempel per kanal. Placeholder `[isi ...]` bisa terlewat oleh pengguna awam. |
| Kualitas output | 9 | Tugas konkret, wajib vs nilai plus, screening yang relevan, batas panjang IG/WA dipatuhi. |
| Akurasi (angka/fakta) | 9 | Dasar aturan (SE Menaker M/6/HK.04/V/2025, UU 13/2003, UU 8/2016, UU 27/2022 tentang PDP) bertanggal dan bersumber. UMK dan benefit tidak dikarang. |
| Penanganan input kurang | 9 | Tanya sekali (≤ 5), atau placeholder + asumsi. |
| Penanganan di luar cakupan | 8 | Pengarahan jelas. Belum ada fallback bila skill tujuan tidak terpasang. |
| Keamanan | 10 | Tanpa script. Aktif mencegah diskriminasi, penipuan, dan penyalahgunaan data. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Skill ini memberi nilai tambah yang nyata dan terukur dibanding agent biasa (lihat uji A/B). Tanpa skill, lowongan untuk pengguna awam berisi syarat yang dilarang Kemnaker dan benefit karangan. Dengan skill, hasilnya patuh aturan, siap diposting di 3 kanal, dan dilengkapi alat screening. Tidak ada cacat berat atau sedang. Beberapa cacat ringan di bawah ini bisa diperbaiki untuk mencapai 9.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
- **R1 – Format output tidak punya bagian untuk permintaan "cek loker"** (SKILL.md, *Kapan digunakan* butir 4 vs *Format output*). Agent harus berimprovisasi (contoh 03). *Saran:* tambahkan di awal Format output: `## 0) Hasil cek (khusus permintaan cek/rapikan loker)` berisi tabel `Di loker lama | Masalah | Diganti menjadi`, lalu versi yang dirapikan.
- **R2 – Placeholder di teks siap-kirim** (Format output & langkah 5). `[isi jam kerja]`/`[isi angka UMK]` bisa ikut terkirim ke grup WA. *Saran:* tambahkan ke Checklist: "Jika masih ada `[isi ...]` di versi IG/WA, tulis peringatan tebal tepat di atas blok: **Isi dulu bagian [isi ...] sebelum dikirim.**"
- **R3 – Pengarahan ke skill lain tanpa fallback** (SKILL.md, *Kapan TIDAK digunakan*). `perjanjian-sederhana`, `surat-resmi`, dan lainnya belum tentu dibeli pengguna. *Saran:* tambahkan "Jika skill tersebut tidak terpasang, jelaskan singkat bahwa permintaan di luar cakupan dan sarankan ahli hukum/konsultan yang relevan."
- **R4 – Tidak ada saran untuk syarat pendidikan yang terlalu tinggi** (langkah 3). Contoh 01 mempertahankan "S1 Akuntansi" tanpa catatan. *Saran:* pada langkah 3 tambahkan: "Jika syarat pendidikan tampak lebih tinggi dari kebutuhan tugas, sarankan alternatif (mis. 'D3/S1 Akuntansi atau pengalaman setara') tanpa memaksakan."
- **R5 – Kalimat privasi data tidak ada di Format output**, hanya di `references/anti-diskriminasi.md`. *Saran:* tambahkan baris opsional "Data lamaran hanya digunakan untuk proses rekrutmen [Nama Usaha]." di bagian *Cara melamar* pada Format output.
- **R6 – README merujuk `CARA-INSTAL.md`** dan ATTRIBUTION merujuk `LISENSI.txt`, dan keduanya tidak ada di folder skill. Pastikan keduanya ikut dalam paket rilis (build).
