# Hasil Uji – caption-sosmed-umkm

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md di folder ini (tanpa script)
- **Metode:** 5 skenario dijalankan dengan berperan sebagai agent yang memuat SKILL.md. Panjang caption dicek dengan penghitung kata Python (hashtag tidak dihitung). Contoh ada di `01-…md` s.d. `05-…md`.

## Audit keamanan
Tidak ada script, tidak ada panggilan jaringan, tidak ada perintah destruktif, tidak ada pembacaan kredensial. Tidak ditemukan teks yang berupa prompt injection. Aturan anti-klaim palsu (halal/BPOM/medis) dan larangan menjelekkan pesaing sudah ada. **Aman.**

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 01 | IG keripik, input lengkap | Baik. Hook, CTA, dan campuran hashtag sesuai. Draf pertama 2 dari 3 variasi di bawah 80 kata dan harus diperpanjang. |
| 02 | FB wedang uwuh, pengguna minta klaim kesehatan | Baik. Klaim ditolak dengan sopan. Aturan di SKILL.md ambigu soal klaim yang diberikan pengguna. |
| 03 | TikTok laundry, permintaan singkat/malas | Baik. Asumsi disebutkan, format TikTok (1–3 kalimat, 3–5 hashtag, teks overlay) terpenuhi. |
| 04 | WA Status "jual sambal", input kurang | Baik. Bertanya sekali dengan daftar singkat. Batas "kapan tanya dan kapan pakai asumsi" belum diatur. |
| 05 | Balas review bintang 1 + menyindir | Diarahkan dengan benar, tapi karena penilaian umum agent. SKILL.md tidak punya aturan di luar cakupan. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 7 | Platform dan kata kunci jelas. Kata "copywriting" dan "teks promosi" terlalu luas, dan tidak ada batasan kapan skill TIDAK dipakai. |
| Kemudahan awam | 9 | Cukup satu kalimat. Pertanyaan dan asumsi dalam bahasa sehari-hari. README jelas. |
| Kualitas output | 8 | 3 gaya benar-benar berbeda, terasa lokal, CTA tegas, ada tips posting. |
| Akurasi (angka/fakta) | 8 | Harga dan promo diambil persis dari input, tidak ada klaim karangan. Minus: batas panjang per platform mudah terlewat (lihat cacat R1). |
| Penanganan input kurang | 7 | Alurnya ada (tanya sekali atau pakai asumsi), tapi ambang keputusannya tidak ditentukan. |
| Penanganan di luar cakupan | 5 | Tidak ada instruksi sama sekali. Hasil baik di uji ini bergantung pada kecerdasan agent. |
| Keamanan | 10 | Tidak ada risiko teknis. Pagar klaim sudah ada. |

## SKOR AKHIR: 7 / 10 → **LULUS** (dengan revisi kecil yang disarankan)

Tidak ada cacat berat. Output siap pakai untuk pembeli awam. Poin terlemah adalah tidak adanya batas cakupan dan satu aturan klaim yang ambigu. Keduanya murah diperbaiki dan sebaiknya diperbaiki sebelum rilis.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- **S1 – Tidak ada bagian "di luar cakupan"** (SKILL.md, bagian *Aturan & batasan*, dan `description` di frontmatter). Kata "copywriting / teks promosi" bisa memicu skill untuk balasan ulasan, deskripsi produk marketplace, naskah video, dan lainnya.
  *Saran:* tambahkan poin: "Di luar cakupan: balasan ulasan/komplain, deskripsi produk marketplace yang panjang, naskah video/iklan berbayar, serta promosi produk ilegal atau berisiko (judi, pinjol ilegal, obat keras, rokok/vape, investasi 'pasti untung'). Jelaskan singkat bahwa ini bukan fungsi skill ini, lalu tawarkan bantuan umum atau caption yang relevan. Jangan memaksakan format 3 variasi." Tambahkan juga di akhir `description`: "Bukan untuk membalas ulasan atau menulis deskripsi produk panjang."
- **S2 – Aturan klaim kesehatan ambigu** (SKILL.md, *Aturan & batasan*, poin ke-5: "**Jangan** membuat klaim yang tidak diberikan pengguna … dan jangan membuat klaim kesehatan/medis"). Tidak jelas apakah klaim kesehatan yang *diminta pengguna* juga dilarang (skenario 02).
  *Saran:* pecah menjadi dua poin: (a) "Jangan menambah klaim yang tidak diberikan pengguna (halal, BPOM, organik, terlaris, dll.)." (b) "Jangan menulis klaim kesehatan/medis/menyembuhkan/menurunkan berat badan **walaupun diminta pengguna**. Jelaskan alasannya dalam satu kalimat, lalu fokus ke rasa, manfaat praktis, dan suasana."
- **S3 – Ambang "tanya dulu" dan "pakai asumsi" tidak ditentukan** (SKILL.md, *Alur kerja* langkah 1, kalimat terakhir).
  *Saran:* "Jika **produk** belum jelas, atau untuk WA Status **harga/cara order** belum ada, tanyakan dulu (satu pesan, maks. 4 poin). Selain itu langsung tulis dengan asumsi wajar, cantumkan daftar asumsi di atas caption, dan pakai placeholder `[nomor WA]` / `[harga]` untuk data yang kosong."

### Ringan
- **R1 – Panjang kata tidak dicek sendiri.** Pada uji ini, draf pertama variasi IG (77 dan 68 kata) dan FB (49 kata) di bawah batas minimum di tabel platform. *Saran:* di *Alur kerja* tambahkan langkah "Sebelum mengirim, cek panjang tiap variasi terhadap tabel (hashtag tidak dihitung)". Tulis juga di tabel bahwa hashtag tidak dihitung.
- **R2 – Aturan emoji "maks. 1 per kalimat"** tidak jelas untuk daftar poin (✅). *Saran:* "maks. 1 emoji per kalimat atau per poin; total maks. ±6 per caption."
- **R3 – Format output tidak punya tempat untuk daftar asumsi dan teks overlay TikTok**, padahal langkah 1 dan tabel TikTok memintanya. *Saran:* tambahkan baris opsional `Asumsi: …` sebelum Variasi A dan `🎬 Teks overlay: …` untuk TikTok di blok *Format output*.
- **R4 – README merujuk `CARA-INSTAL.md` dan `LISENSI.txt`** (README *Instalasi singkat*; ATTRIBUTION.md) yang tidak ada di folder skill. Pastikan kedua file ikut dalam paket rilis.

## Uji A/B
- **Tanggal:** 2026-09-23 — ditambahkan oleh agent penguji independen (simulasi, Claude Code) karena uji A/B baru diwajibkan setelah uji awal. Isi di atas tidak diubah.
- **Berkas:** `00-pembanding-tanpa-skill.md` (input S1 yang sama persis, dikerjakan tanpa membaca skill apa pun, lalu dibandingkan dengan `01-instagram-keripik-mahasiswa.md`).
- **Hasil tanpa skill:** 1 caption, 62 kata (di bawah rentang IG 80–150), baris pertama berupa judul kapital (bukan hook), ±12 emoji, dan memuat
  **klaim yang tidak diberikan pengguna** ("dibuat dari singkong pilihan", "diolah secara higienis") serta **urgensi palsu** ("Stok terbatas, buruan sebelum kehabisan!").
- **Hasil dengan skill:** 3 variasi gaya berbeda dengan hook nyata, 81–82 kata, emoji terkendali, tanpa klaim/urgensi karangan, plus tips posting.
- **Setara:** harga, paket, cara order, dan campuran hashtag sama-sama benar.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik**, terutama pada kejujuran klaim dan pilihan variasi. Selisihnya lebih kecil daripada skill yang
  memakai script (tidak ada perhitungan angka), tetapi nyata dan relevan bagi pembeli awam. Tidak ada cacat berat "skill tidak memberi nilai tambah".
- **Dampak ke skor:** **tidak perlu diturunkan** — SKOR AKHIR tetap **7 / 10 → LULUS**.
