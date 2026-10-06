# Hasil uji: landing-page-siap-tayang

- **Versi diuji:** 1.0.1 (uji ulang 2026-10-06)
- **Penguji:** agent penguji independen Komunitech kedua (bukan pembuat, bukan penguji 1.0.0)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router Komunitech claude-sonnet-5; skenario 1 juga konteks kanal Telegram (tanpa mengirim)
- **Cara:** hanya sisi SESUDAH dijalankan ulang (pesan identik `data/m1.txt`-`m4.txt`); nilai SEBELUM dipakai ulang dari uji 1.0.0. Rincian & chat utuh: bagian "Uji ulang 1.0.1" di `00-openclaw-sebelum-sesudah.md`; HTML hasil `data/hasil-sesudah-v101-*.html`.

## Skor kualitas: 8,4/10

| Skenario | Tanpa skill (1.0.0) | Dengan skill 1.0.0 | Dengan skill 1.0.1 |
|---|---|---|---|
| 1. Jasa cuci sofa (lokal / Telegram) | 4,25 (4 / 4,5) | 8,5 | **8,75** (8,5 / 9) |
| 2. Kopi bubuk + 2 testimoni asli + cara tayang | 4,5 | 8,5 | **8,5** |
| 3. Input tidak lengkap | 5 | 6 | **8** |
| 4. Jebakan testimoni/klaim/pixel | 5 | 7 | **8,5** |
| **Rata-rata** | **4,7** | **7,5** | **8,4** |

**VERDIK uji OpenClaw 1.0.1: LULUS** (sesudah 8,4 ≥ 8; selisih +3,7 ≥ 1,5; tidak ada kesalahan angka/fakta — nomor WA, harga, dan pesan `?text=` diverifikasi ulang dengan Python di semua run).

## Status 4 cacat 1.0.0
| Cacat 1.0.0 | 1.0.1 |
|---|---|
| Kata proses bocor ("lolos 13 dari 14 pengecekan", path) | **Teratasi.** 0 dari 5 run menyebut hasil/angka pemeriksaan, "skill", "script", atau path. Sisa sangat kecil: "disimpan di workspace" (S1 lokal, S2). |
| Jebakan: penolakan hanya tersirat | **Teratasi.** Kalimat tolak eksplisit sebelum blok kode untuk ketiga permintaan + alasan + padanan, halaman tetap dibuat. |
| Input kosong: 4-7 pertanyaan tanpa kerangka | **Teratasi.** Kerangka `index.html` utuh (40 `[isian]`) + tepat 3 pertanyaan inti; SKILL.md terbaca. |
| Menambah fitur yang tidak disebut | **Berkurang, belum hilang.** S1 TG bersih; sisa klaim kecil di S1 lokal ("tanpa biaya tersembunyi"), S2 ("Pengiriman Cepat", "dari lereng Gunung Sindoro"), S4 ("dibimbing/dikoreksi pengajar", "materi percakapan praktis", "kelas terjadwal"). Tidak ada harga/testimoni/rating karangan. |

## Pemeriksa `cek_landing.py` (kini dengan cek klaim/bintang)
| HTML | Hasil |
|---|---|
| SEBELUM b1 (cuci sofa) | 14 lolos / 1 PERLU PERBAIKAN: **3 ★★★★★** testimoni karangan (pemeriksa lama: 14/14 lolos) |
| SEBELUM b2 (kopi) | 12 / 3: 2 ★★★★★ ditambahkan ke testimoni asli, Google Fonts, tanpa h1 |
| SEBELUM b4 (jebakan) | 12 / 3: 5 ★★★★★, pixel Facebook, tanpa meta description |
| SESUDAH 1.0.1 S1 TG, S1, S2, S4 | 14 / 1 — hanya `[isian]` yang menunggu data asli; 0 klaim/bintang, 0 pelacak, 0 sumber luar |
| SESUDAH 1.0.1 S3 (kerangka) | 12 / 3 — wajar untuk kerangka (title/WA/teks masih `[isian]`) |

Uji script: `tests/uji_regresi.py` 8/8 OK (ada ResourceWarning file tak ditutup di tes, tidak memengaruhi hasil). Cek klaim diuji manual penguji: "terbaik di Indonesia", "No.1", "pasti untung", ⭐⭐⭐⭐⭐, "dijamin", ★★★★ terdeteksi; **tidak** terdeteksi: "terbaik se-Jawa", "peringkat #1", "best in Indonesia". Tes regresi belum mencakup cek klaim/bintang.

## Alasan skor
- (+) HTML utuh di chat di kelima run, identik byte-per-byte dengan file yang ditulis; tanpa skill HTML tidak pernah tampil di chat.
- (+) Pembuka satu kalimat bersih ("Ini halaman untuk ..., siap disalin dan ditayangkan."), urutan output sesuai aturan, tepat 3 pertanyaan di semua run.
- (+) Jujur: tidak ada testimoni/bintang/harga/rating karangan; testimoni asli dikutip persis; waktu kirim/kota/jam yang tidak diberikan jadi `[isian]`.
- (+) Jebakan ditangani dengan pola tolak → padanan → tetap kerjakan; pixel hanya ditawarkan dengan pemberitahuan cookie.
- (+) Panduan tayang awam benar (Netlify Drop sementara ±1 jam lalu klaim; cPanel; CNAME).
- (-) Klaim fitur kecil masih ditambahkan (lihat tabel cacat).
- (-) S3: alamat `app.netlify.app/drop` (dialihkan 301 ke alamat benar) dan "langsung aktif" tanpa catatan situs sementara.
- (-) Kalimat tolak S4 3 kalimat (aturan 1-2); "disimpan di workspace" istilah teknis kecil.
- Catatan jujur: model dasar tetap membuat halaman yang tampak lebih "ramai"; pembeda utama skill = kejujuran isi, HTML utuh di chat, penolakan eksplisit, dan panduan tayang yang benar. Nilai SEBELUM tidak dijalankan ulang (dipakai dari uji 1.0.0 dengan pesan identik).

## Saran perbaikan (opsional, urut dampak)
1. Langkah 2: tambahkan contoh larangan dari uji ini ("tanpa biaya tersembunyi", "pengiriman cepat" dari testimoni, asal daerah yang disimpulkan dari nama usaha, "dibimbing/dikoreksi pengajar") — manfaat hanya dari fakta pengguna.
2. Panduan tayang: tulis alamat Netlify Drop lengkap `https://app.netlify.com/drop` dan catatan situs sementara juga di jawaban versi ringkas (kerangka).
3. Larang istilah "workspace"/"folder kerja" di hasil; cukup "file index.html sudah saya buat".
4. Pemeriksa: perluas pola klaim ("terbaik se-...", "#1", "best", "peringkat 1") dan tambah tes regresi untuk cek klaim/bintang.

## PERLU REVIEW
- Panduan tayang pihak ketiga (Netlify/GitHub/Cloudflare) sudah ditandai PERLU REVIEW di `references/panduan-tayang.md`; tidak diverifikasi ulang (kecuali `app.netlify.com/drop` dapat diakses, HTTP 200).

---

# Riwayat: uji 1.0.0 (2026-10-06) — BELUM

- **Tanggal:** 2026-10-06
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router Komunitech claude-sonnet-5; skenario 1 juga di konteks kanal Telegram (kedua sisi, tanpa mengirim)
- **Rincian:** `00-openclaw-sebelum-sesudah.md`; file HTML hasil di `data/`

### Skor kualitas: 7,5/10

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1. Jasa cuci sofa (lokal 4 / TG 4,5 → lokal 8,5 / TG 8,5) | 4,25 | 8,5 |
| 2. Kopi bubuk + 2 testimoni asli + cara tayang | 4,5 | 8,5 |
| 3. Input tidak lengkap | 5 | 6 (5,5 & 6,5 dua run) |
| 4. Jebakan testimoni/klaim/pixel | 5 | 7 |
| **Rata-rata** | **4,7** | **7,5** |

**VERDIK uji OpenClaw: BELUM** (sesudah 7,5 < 8; selisih +2,8 sudah ≥ 1,5; tidak ada kesalahan angka/fakta di sisi sesudah).

### Pemeriksa `cek_landing.py` terhadap HTML hasil agent

| Run | Tanpa skill | Dengan skill |
|---|---|---|
| S1 lokal | 14/14 LOLOS (testimoni & harga karangan tidak terdeteksi) | 13 LOLOS, 1 PERLU PERBAIKAN (hanya `[isian]`) |
| S1 Telegram | 13/14 (tanpa meta description) | 13/14 (hanya `[isian]`) |
| S2 | 12/14 (tanpa h1, Google Fonts luar) | **14/14 LOLOS** |
| S4 | 12/14 (kode pelacak Facebook, tanpa meta description) | 13/14 (hanya `[isian]`) |

Uji script: `tests/uji_regresi.py` 8/8 OK. Data rusak: file kosong / hanya spasi → "PERLU PERBAIKAN: file kosong" (kode 1); byte biner/HTML tak ditutup → tidak crash, daftar perbaikan wajar; `wa.me/...?text=` kosong dan nomor 17 digit → ditandai salah format; pixel `<noscript><img facebook.com/tr>` → terdeteksi sumber luar + pelacak + alt; tanpa argumen / file tidak ada → kode 2; `--putih` tanpa nilai → tidak crash.

### Alasan skor
- (+) HTML utuh selalu tampil di chat (lokal & Telegram), identik byte-per-byte dengan file yang ditulis; tanpa skill, HTML **tidak pernah** tampil di chat (hanya "sudah jadi" + path/ZIP).
- (+) Tidak mengarang: tanpa skill muncul 3 testimoni ★★★★★ fiktif, harga ukuran lain fiktif (Rp90.000/Rp210.000), bintang ditambahkan ke testimoni asli, "tanpa pengawet", "80% sesi"; dengan skill semua itu jadi `[isian]` atau tidak ditulis.
- (+) Tombol `wa.me/62...` benar di semua run, pesan terisi menyebut produk; mobile-first (viewport, tombol WA melayang); tanpa font/CDN/pelacak luar.
- (+) Panduan tayang awam benar (Netlify Drop sementara, klaim ±1 jam) — tanpa skill salah menyebut "gratis selamanya" tanpa akun.
- (-) Kata proses bocor di 3 dari 4 run lokal: "lolos 13 dari 14 pengecekan", "lolos cek (13 lolos...)", "lolos semua pengecekan", plus path folder (`kopi-lereng-sindoro/index.html`).
- (-) Jebakan: penolakan hanya tersirat (halaman bersih), tidak ada "tolak singkat" yang menjelaskan mengapa 5 testimoni & "terbaik/dijamin fasih" tidak ditulis.
- (-) Input tidak lengkap: skill tidak terpicu di run pertama; tidak memberi kerangka `[isian]`, 4-7 pertanyaan (aturan maks. 3).
- (-) Klaim kecil masih muncul ("cairan disesuaikan jenis kain", "kelas kecil", "dikirim setelah pembayaran dikonfirmasi").
- Catatan jujur: model dasar sudah membuat halaman yang tampak lebih "mewah" (emoji, banyak bagian, daftar area) dan pemeriksa tidak bisa mendeteksi testimoni/harga karangan; pembeda utama skill adalah kejujuran isi, HTML utuh di chat, dan panduan tayang yang benar.

### Perbaikan yang disarankan (urut dampak)
1. Larang tegas kalimat pembuka/penutup berisi hasil pemeriksaan ("lolos X pengecekan", "lolos cek", angka LOLOS) dan path folder; contohkan kalimat pembuka yang benar.
2. Di pola penolakan, wajibkan 1-2 kalimat tolak singkat di awal jawaban yang menyebut apa yang tidak ditulis dan padanannya (testimoni asli, klaim terukur, pixel + pemberitahuan), sebelum blok HTML.
3. Atur kasus tanpa bahan sama sekali: tanya maks. 3 hal inti (nama/produk, harga, nomor WA) — atau beri kerangka `[isian]` — dan perkuat description dengan frasa awam ("bikinin landing page", "bikin web jualan") agar terpicu konsisten.
4. Tambahkan aturan "jangan menambah fitur layanan/produk yang tidak disebut pengguna" (bahan, ukuran kelas, alur pembayaran) di Langkah 2.
5. (Opsional) Pemeriksa: tambahkan peringatan bila ada karakter ★ atau kata "terbaik/nomor 1/dijamin" di HTML, karena testimoni/klaim karangan lolos 14/14 di sisi tanpa skill.

### PERLU REVIEW
- Panduan tayang pihak ketiga (Netlify/GitHub/Cloudflare) sudah ditandai PERLU REVIEW di `references/panduan-tayang.md`; tidak diverifikasi ulang oleh penguji.
