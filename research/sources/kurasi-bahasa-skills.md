# Kurasi: alvinindra/bahasa-skills

Tanggal tinjau: 2026-09-23 · Peninjau: agent kurator · Status: **menunggu keputusan koordinator/pemilik**

## 1. Identitas

| Item | Isi |
|---|---|
| Nama | bahasa-skills (router `bahasa-skills` + 5 skill: `bahasa-inti`, `bahasa-marketing`, `bahasa-website`, `bahasa-seo`, `bahasa-peneliti`) |
| URL | https://github.com/alvinindra/bahasa-skills |
| Pembuat | Alvin Indra (alvinindra) |
| Update terakhir | 2026-08-02 (6 commit, semuanya 2026-08-02). `plugin.json` versi 1.2.0. |
| **Lisensi** | **TIDAK ADA.** Tidak ada file LICENSE/COPYING di pohon repo. `plugin.json` dan `marketplace.json` tidak punya field lisensi. README tidak menyebut lisensi. Sidebar GitHub juga tidak menampilkan lisensi. |
| Popularitas | 3 bintang |

Isi: SKILL.md router (51 baris), 5 SKILL.md kategori (95–114 baris), 11 file `references/` (kata baku, EYD V, frasa terlarang, padanan istilah, copywriting, media sosial, UX writing, halaman situs, SEO on-page, riset kata kunci, kalimat akademik, sitasi), `sumber/` (bibliografi berlabel mutu sumber), `CONTOH.md` (perbandingan tanpa/dengan skill), `.claude-plugin/`. Total sekitar 2.240 baris Markdown.

### Ringkasan isi
Paket menulis bahasa Indonesia "bebas AI slop". Isinya: protokol tiga langkah, empat keputusan awal (pembaca, ragam, medium, pesan), "Sepuluh Larangan Keras" (pembuka klise, penutup ritual, paralelisme negatif, tripel kosong, kosakata slop seperti *hiruk pikuk*, dan lain-lain), kewajiban (spesifik, verba kuat, satu sapaan), Pemeriksaan Wajib, lalu aturan per kategori. Contoh: aturan sapaan Anda/kamu/lo, larangan superlatif tanpa bukti (Etika Pariwara Indonesia), dan microcopy tombol.

## 2. Audit keamanan (Tahap 3)

| Pemeriksaan | Hasil |
|---|---|
| Script | Tidak ada. Murni Markdown dan JSON manifest plugin. |
| Jaringan / kredensial / `curl \| bash` / obfuscation | Tidak ada. Sekitar 150 URL hanya daftar pustaka di `sumber/`, tanpa perintah mengambil URL. |
| Prompt injection | Tidak ada perintah jahat. **Catatan:** deskripsi router dan `bahasa-inti` sangat agresif ("WAJIB dipakai pada SETIAP tugas menulis ... apa pun bentuknya"). Ini bukan injeksi berbahaya, tetapi membuat skill merebut semua tugas berbahasa Indonesia dan bisa bentrok dengan skill kita (caption, surat, broadcast). Jangan tiru pola pemicu ini. |
| Karakter tersembunyi | Tidak ada (dipindai). |
| Data pribadi / API key | Tidak ada. |

**Hasil: LULUS** (catatan: pemicu terlalu agresif).

## 3. Penilaian

- **Kualitas: 8/10.** Aturannya spesifik dan berbasis sumber (Ivan Lanin/Narabahasa, EYD V, KBBI, Etika Pariwara), contohnya konkret, dan ada perbandingan sebelum/sesudah. Termasuk yang terbaik di antara paket bahasa Indonesia yang ditinjau.
- **Tumpang tindih:** menyentuh semua skill tulis kita (`caption-sosmed-umkm`, `kalender-konten-30hari`, `broadcast-wa`, `listing-marketplace`, `surat-resmi`, `proposal-kerjasama`, `balas-ulasan-pelanggan`). Paket ini bukan pesaing langsung karena bersifat lapisan gaya, tetapi berpotensi menjadi "standar mutu bahasa" untuk semua skill kita.
- **Keputusan: INSPIRASI SAJA (tulis ulang dari nol).**
  Alasan: tanpa file lisensi, hak cipta penuh ada pada penulis dan tidak ada izin yang diberikan. Sesuai aturan CLAUDE.md, repo ini dilarang disalin atau dijual ulang.

## 4. Cara memakai sebagai inspirasi (aman)

1. Yang boleh diambil adalah **gagasan dan fakta**, bukan susunan kalimat. Contohnya: kaidah EYD V dan KBBI (aturan resmi), konsep "ragam lima tingkat" (Martin Joos, dipopulerkan Ivan Lanin), prinsip "satu materi satu sapaan", dan larangan superlatif tanpa bukti (Etika Pariwara Indonesia).
2. Tulis rujukan internal kita sendiri, misalnya `templates/` atau `references/gaya-bahasa.md` bersama untuk skill tulis, langsung dari sumber primer (ejaan.kemendikdasmen.go.id, KBBI, EPI). Jangan membuka file alvinindra saat menulis agar tidak terjadi penyalinan tak sengaja.
3. Alternatif berlisensi MIT yang bisa dikurasi resmi untuk kebutuhan yang sama: `ardianryan/eyd-v` (MIT) dan `fathurwithyou/indonesia-eyd-writing-skill` (MIT). Keduanya belum diaudit penuh di sesi ini; hanya lisensinya yang diperiksa.
4. Opsi lain: pemilik menghubungi penulis dan meminta lisensi (misalnya MIT). Jika lisensi diberikan, status bisa ditinjau ulang menjadi KURASI.

## 5. Temuan terkait
Repo `pataanggs/indonesian-writing-skills` (MIT) mengaku "ditulis ulang dari nol" dari repo ini, tetapi ditemukan **82 baris panjang identik kata per kata** dengan repo ini. Lihat `kurasi-indonesian-writing-skills.md`.
