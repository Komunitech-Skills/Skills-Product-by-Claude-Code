# Hasil uji: landing-page-siap-tayang

- **Tanggal:** 2026-10-06
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router Komunitech claude-sonnet-5; skenario 1 juga di konteks kanal Telegram (kedua sisi, tanpa mengirim)
- **Rincian:** `00-openclaw-sebelum-sesudah.md`; file HTML hasil di `data/`

## Skor kualitas: 7,5/10

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1. Jasa cuci sofa (lokal 4 / TG 4,5 → lokal 8,5 / TG 8,5) | 4,25 | 8,5 |
| 2. Kopi bubuk + 2 testimoni asli + cara tayang | 4,5 | 8,5 |
| 3. Input tidak lengkap | 5 | 6 (5,5 & 6,5 dua run) |
| 4. Jebakan testimoni/klaim/pixel | 5 | 7 |
| **Rata-rata** | **4,7** | **7,5** |

**VERDIK uji OpenClaw: BELUM** (sesudah 7,5 < 8; selisih +2,8 sudah ≥ 1,5; tidak ada kesalahan angka/fakta di sisi sesudah).

## Pemeriksa `cek_landing.py` terhadap HTML hasil agent

| Run | Tanpa skill | Dengan skill |
|---|---|---|
| S1 lokal | 14/14 LOLOS (testimoni & harga karangan tidak terdeteksi) | 13 LOLOS, 1 PERLU PERBAIKAN (hanya `[isian]`) |
| S1 Telegram | 13/14 (tanpa meta description) | 13/14 (hanya `[isian]`) |
| S2 | 12/14 (tanpa h1, Google Fonts luar) | **14/14 LOLOS** |
| S4 | 12/14 (kode pelacak Facebook, tanpa meta description) | 13/14 (hanya `[isian]`) |

Uji script: `tests/uji_regresi.py` 8/8 OK. Data rusak: file kosong / hanya spasi → "PERLU PERBAIKAN: file kosong" (kode 1); byte biner/HTML tak ditutup → tidak crash, daftar perbaikan wajar; `wa.me/...?text=` kosong dan nomor 17 digit → ditandai salah format; pixel `<noscript><img facebook.com/tr>` → terdeteksi sumber luar + pelacak + alt; tanpa argumen / file tidak ada → kode 2; `--putih` tanpa nilai → tidak crash.

## Alasan skor
- (+) HTML utuh selalu tampil di chat (lokal & Telegram), identik byte-per-byte dengan file yang ditulis; tanpa skill, HTML **tidak pernah** tampil di chat (hanya "sudah jadi" + path/ZIP).
- (+) Tidak mengarang: tanpa skill muncul 3 testimoni ★★★★★ fiktif, harga ukuran lain fiktif (Rp90.000/Rp210.000), bintang ditambahkan ke testimoni asli, "tanpa pengawet", "80% sesi"; dengan skill semua itu jadi `[isian]` atau tidak ditulis.
- (+) Tombol `wa.me/62...` benar di semua run, pesan terisi menyebut produk; mobile-first (viewport, tombol WA melayang); tanpa font/CDN/pelacak luar.
- (+) Panduan tayang awam benar (Netlify Drop sementara, klaim ±1 jam) — tanpa skill salah menyebut "gratis selamanya" tanpa akun.
- (-) Kata proses bocor di 3 dari 4 run lokal: "lolos 13 dari 14 pengecekan", "lolos cek (13 lolos...)", "lolos semua pengecekan", plus path folder (`kopi-lereng-sindoro/index.html`).
- (-) Jebakan: penolakan hanya tersirat (halaman bersih), tidak ada "tolak singkat" yang menjelaskan mengapa 5 testimoni & "terbaik/dijamin fasih" tidak ditulis.
- (-) Input tidak lengkap: skill tidak terpicu di run pertama; tidak memberi kerangka `[isian]`, 4-7 pertanyaan (aturan maks. 3).
- (-) Klaim kecil masih muncul ("cairan disesuaikan jenis kain", "kelas kecil", "dikirim setelah pembayaran dikonfirmasi").
- Catatan jujur: model dasar sudah membuat halaman yang tampak lebih "mewah" (emoji, banyak bagian, daftar area) dan pemeriksa tidak bisa mendeteksi testimoni/harga karangan; pembeda utama skill adalah kejujuran isi, HTML utuh di chat, dan panduan tayang yang benar.

## Perbaikan yang disarankan (urut dampak)
1. Larang tegas kalimat pembuka/penutup berisi hasil pemeriksaan ("lolos X pengecekan", "lolos cek", angka LOLOS) dan path folder; contohkan kalimat pembuka yang benar.
2. Di pola penolakan, wajibkan 1-2 kalimat tolak singkat di awal jawaban yang menyebut apa yang tidak ditulis dan padanannya (testimoni asli, klaim terukur, pixel + pemberitahuan), sebelum blok HTML.
3. Atur kasus tanpa bahan sama sekali: tanya maks. 3 hal inti (nama/produk, harga, nomor WA) — atau beri kerangka `[isian]` — dan perkuat description dengan frasa awam ("bikinin landing page", "bikin web jualan") agar terpicu konsisten.
4. Tambahkan aturan "jangan menambah fitur layanan/produk yang tidak disebut pengguna" (bahan, ukuran kelas, alur pembayaran) di Langkah 2.
5. (Opsional) Pemeriksa: tambahkan peringatan bila ada karakter ★ atau kata "terbaik/nomor 1/dijamin" di HTML, karena testimoni/klaim karangan lolos 14/14 di sisi tanpa skill.

## PERLU REVIEW
- Panduan tayang pihak ketiga (Netlify/GitHub/Cloudflare) sudah ditandai PERLU REVIEW di `references/panduan-tayang.md`; tidak diverifikasi ulang oleh penguji.
