# Hasil Uji — listing-marketplace

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/batas-platform.md`, `scripts/cek_listing.py`
- **Metode:** 5 skenario (01–05) + uji A/B (00), berperan sebagai agent yang memuat SKILL.md. Script dijalankan sungguhan di `/tmp/uji-listing-marketplace/`;
  panjang judul/deskripsi dihitung ulang dengan python terpisah (`len` dan unit UTF-16).

## Audit keamanan
- Script hanya memakai `argparse, json, re, sys`. Tidak ada akses jaringan, subprocess, penulisan/penghapusan file, atau pembacaan kredensial.
  Hanya membaca file teks yang diberikan.
- SKILL.md/references: tidak ada prompt injection. Penolakan barang KW/terlarang dan klaim tanpa bukti tertulis jelas. **Aman.**

## Verifikasi angka & aturan (independen)
- Panjang: 80/57/68 (S1), 83/65 (S2), 45 (S3), deskripsi 1.173/462/759/755 — semua cocok dengan hitungan independen. Emoji dihitung 2 (UTF-16):
  "Sambal 🌶️ Pedas" = 15 karakter → dihitung 16 (aman, lebih ketat) ✔.
- Batas: Shopee 100/3.000, Tokopedia 70/2.000, TikTok Shop 25–100/2.000 — **semuanya dilabeli "batas aman, bukan batas resmi — cek batas terbaru di
  Seller Center"** di references, di output script, dan di format output SKILL.md ✔. `--batas-judul` & `--batas-deskripsi` bekerja; nilai 0 ditolak ✔.
- Deteksi kontak: nomor `0812-0000-1234`, `www.…com`, `@akun`, email → **GAGAL** ✔. Judul 83 karakter di Tokopedia → GAGAL "pangkas 13" ✔.
  Judul kurang dari 25 karakter di TikTok Shop → GAGAL ✔. Platform tidak dikenal, judul kosong → ditangani ✔.
- **Tidak tertangkap:** "Order via WA ya kak" (tanpa nomor), "turunkan kolesterol", "meningkatkan imun", "aman untuk ibu hamil". Judul
  "Sepatu Nike Air Jordan KW Super Grade Ori Original Mirip Adidas Samba" → status **LULUS** (hanya CEK). Barcode "0812345678901" → dianggap nomor HP (false positive).

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Judul/deskripsi/SEO marketplace, Indonesia & Inggris, batas dengan caption jelas. |
| Kemudahan awam | 8 | Satu kalimat cukup; output siap tempel per platform. Istilah "kata kunci ekor panjang" sedikit teknis tapi dijelaskan lewat contoh. |
| Kualitas output | 9 | Judul per platform, deskripsi terstruktur, `[isi: …]` untuk data kosong. A/B: jelas lebih baik. |
| Akurasi (angka/fakta) | 9 | Panjang teks akurat; tidak ada klaim karangan di 3 skenario normal; batas diberi label. |
| Penanganan input kurang | 8 | S4 tanya sekali; S3 lanjut dengan `[isi]`. Aturan "spesifikasi wajib" vs "lanjut cepat" sedikit ambigu. |
| Penanganan di luar cakupan | 9 | S5 menolak KW dengan alasan & alternatif; S2 menolak klaim halal/diet. |
| Keamanan | 9 | Tidak ada risiko teknis. Pagar klaim di script belum lengkap (lihat S1–S2). |

## SKOR AKHIR: 8 / 10 → **LULUS**

Tidak ada cacat berat. Aturan "tidak mengarang klaim" dan label "cek batas terbaru" dipatuhi di semua skenario; uji A/B menunjukkan
nilai tambah besar (tanpa skill: judul 141 karakter dan 5 klaim karangan). Kelemahan ada di jaring pengaman script yang terlalu longgar untuk
barang tiruan dan klaim kesehatan — saat ini penolakan bergantung pada agent.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- **S1 — Indikasi barang tiruan hanya berstatus CEK, listing tetap "LULUS"** (`cek_listing.py` baris 52 di `POLA_BERISIKO`; status lulus dihitung
  hanya dari GAGAL, baris 163). *Saran:* pindahkan pola `kw|replika|grade\s?ori|mirip\s+<merek>` ke daftar yang menghasilkan **GAGAL**
  ("indikasi barang tiruan — marketplace melarang"), dan biarkan "original" tetap CEK.
- **S2 — Daftar klaim kesehatan terlalu sempit** (baris 48–49). Tidak menangkap "menurunkan/turunkan kolesterol", "meningkatkan imun/daya tahan tubuh",
  "mencegah", "aman untuk ibu hamil/bayi", "herbal", "melangsingkan", "menghilangkan jerawat". *Saran:* perluas pola, mis.
  `\b(?:menurunkan|turunkan|meningkatkan|mencegah|menghilangkan|melangsingkan)\b.{0,20}\b(?:kolesterol|gula darah|imun|daya tahan|jerawat|berat badan|asam urat)\b`
  dan `\baman\s+untuk\s+(?:ibu\s+hamil|bayi|anak)\b` → CEK dengan alasan "klaim kesehatan butuh bukti/izin".

### Ringan
- **R1 — Ajakan "via WA/order WA/DM" tanpa nomor tidak tertangkap** (baris 42 hanya `chat wa|hubungi wa|whats app|dm ig`). *Saran:* tambah `\b(?:via|order|pesan|lewat)\s+(?:wa|whatsapp|dm|ig)\b`.
- **R2 — False positive:** "Original" sebagai nama varian rasa → CEK klaim keaslian; barcode 13 digit berawalan 08 → GAGAL nomor HP. *Saran:* untuk
  "original" tambahkan pengecualian bila diikuti/didahului "rasa|varian|/"; untuk nomor HP batasi panjang 10–13 digit dan abaikan bila didahului "barcode|EAN|SKU".
- **R3 — Cek kata kunci mencari frasa persis** (baris 147) sehingga "gamis katun rayon" dilaporkan "tidak ada" walau semua katanya ada di judul.
  *Saran:* tampilkan juga status "semua kata ada (tidak berurutan)".
- **R4 — Ambiguitas input wajib:** tabel Input menandai spesifikasi "Ya — tanyakan", tetapi paragraf di bawahnya membolehkan lanjut dengan `[isi]`.
  *Saran:* "Produk tidak jelas → tanya. Produk jelas tapi spesifikasi minim → lanjut dengan `[isi]` dan daftar yang perlu dilengkapi."
- **R5 — README merujuk `CARA-INSTAL.md`, ATTRIBUTION merujuk `LISENSI.txt`** yang tidak ada di folder skill; pastikan ikut paket rilis.

## Uji A/B
Lihat `00-pembanding-tanpa-skill.md`. Tanpa skill: satu judul 141 karakter untuk semua platform (gagal batas di ketiganya), 5 klaim karangan
("premium", "tidak menerawang", "wudhu friendly", "jahitan kuat", "terbaru 2026"), hashtag di deskripsi. Dengan skill: 3 judul sesuai batas,
teks polos, tanpa klaim karangan. **Skill jelas memberi nilai tambah.**
