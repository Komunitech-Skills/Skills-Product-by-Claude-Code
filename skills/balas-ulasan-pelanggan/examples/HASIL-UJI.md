# Hasil Uji — balas-ulasan-pelanggan

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/pola-balasan.md`, `scripts/cek_balasan.py`
- **Metode:** 5 skenario (01–05) + uji A/B (00), berperan sebagai agent yang memuat SKILL.md. Script dijalankan sungguhan di
  `/tmp/uji-balas-ulasan-pelanggan/` untuk setiap balasan publik; panjang teks dihitung ulang dengan python terpisah.

## Audit keamanan
- Script hanya memakai `argparse, json, re, sys`. Tidak ada akses jaringan, subprocess, penulisan/penghapusan file, atau pembacaan kredensial.
- SKILL.md/references: tidak ada prompt injection. Larangan imbalan untuk ubah ulasan, pembukaan data pembeli, dan ajakan keluar platform eksplisit. **Aman.**

## Verifikasi (independen)
- Panjang balasan: 358, 175 (S1); 496, 249 (S2); 175, 218, 295 (S3); 311 (S5) — cocok dengan hitungan independen.
- Deteksi yang benar: nomor HP, email, `INV/…`, kode resi `JP1234567890`, deretan angka ≥ 10 digit, "Jl./No. 5/RT 03", "WA" di marketplace (GAGAL),
  "ubah bintang", "bintang 5 … voucher" (GAGAL), "seharusnya kakak baca deskripsi", "pembeli lain tidak", janji "pasti/dijamin/100%" (CEK),
  tidak ada terima kasih/maaf/eskalasi (SARAN), platform tidak dikenal & teks kosong (ERROR) ✔.
- **Tidak tertangkap / salah:** nama lengkap pembeli ("Kak Rina Wulandari") dan kutipan isi chat pribadi di balasan publik → tidak terdeteksi;
  alamat toko sendiri "Jalan Sudirman" → **GAGAL** (false positive); kalimat empatik "pengalaman yang seharusnya Kakak dapat" → CEK defensif (false positive).

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Ulasan/review/bintang 1/Google review, batas dengan balas-chat-cs jelas. |
| Kemudahan awam | 9 | Cukup tempel ulasan; output siap tempel + catatan urutan kirim yang praktis. |
| Kualitas output | 9 | Tenang, spesifik, tidak defensif; pesan chat pribadi berguna. A/B: jelas lebih baik. |
| Akurasi (angka/fakta) | 9 | Tidak mengarang fakta toko atau kompensasi; panjang akurat. |
| Penanganan input kurang | 9 | S4 tanya sekali + jalan cepat; S3 langsung kerja dengan asumsi aman. |
| Penanganan di luar cakupan | 9 | S5 menolak ulasan palsu & pembukaan data, memberi alternatif sah. |
| Keamanan | 8 | Tidak ada risiko teknis; pemeriksa data pribadi belum menangkap nama lengkap & kutipan chat. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Tidak ada cacat berat. Di semua skenario agent menghasilkan balasan yang aman dan siap tempel; uji A/B menunjukkan nilai tambah besar (tanpa skill:
ajakan ke WA + permintaan ubah rating + alasan karangan). Kelemahan hanya pada ketelitian script pemeriksa (beberapa false positive/negative).

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- **S1 — Kutipan isi chat dan nama lengkap pembeli tidak terdeteksi** (`cek_balasan.py`, `POLA_DATA` baris 32–41). Balasan
  "Kak Rina Wulandari, … Kakak sendiri bilang 'gpp kak telat dikit'" hanya GAGAL karena nomor pesanan; tanpa nomor, draf itu akan LULUS.
  *Saran:* tambahkan CEK untuk (a) teks dalam tanda kutip setelah kata "bilang|chat|pesan|katanya" (`(?:bilang|chat|katanya|menulis)\s*[:,]?\s*["'“‘]`),
  dan (b) sapaan + dua kata berhuruf kapital (`\b(?:Kak|Bu|Pak|Mbak|Mas)\s+[A-Z][a-z]+\s+[A-Z][a-z]+`) → "kemungkinan nama lengkap pembeli".

### Ringan
- **R1 — False positive alamat:** kata umum "jalan"/"Jalan" (mis. "jalan-jalan", alamat toko sendiri) langsung **GAGAL** (baris 38). *Saran:* wajibkan pola
  alamat berisi nama/nomor (`\b(?:jl\.?|jalan)\s+[A-Z][\w.]+(?:\s+no\.?\s*\d+)?`) dan turunkan ke CEK bila tanpa nomor.
- **R2 — False positive defensif:** `\bseharusnya\s+(?:kakak|anda…)` menandai kalimat empatik "pengalaman yang seharusnya Kakak dapat" (S1).
  *Saran:* kecualikan bila didahului "yang" atau diikuti "dapat|terima|alami".
- **R3 — Pola `\bwa\b` dan `\bline\b`** dapat mengenai kata lain (mis. "line produksi"). *Saran:* batasi ke "wa\s*(?:ke|di|:|\d)" atau "whatsapp".
- **R4 — Banyak ulasan sekaligus menghasilkan output panjang** (1 utama + 1 alternatif per ulasan). *Saran:* SKILL.md langkah 5: "Untuk ≥ 3 ulasan, alternatif opsional."
- **R5 — README merujuk `CARA-INSTAL.md`, ATTRIBUTION merujuk `LISENSI.txt`** yang tidak ada di folder skill; pastikan ikut paket rilis.

## Uji A/B
Lihat `00-pembanding-tanpa-skill.md`. Tanpa skill: mengarahkan ke WhatsApp dengan nomor (dilarang di marketplace), meminta pembeli mengubah rating
(melanggar kebijakan ulasan), mengarang alasan "lonjakan pesanan", dan menjanjikan kompensasi di publik. Dengan skill: semua itu dihindari, plus pesan
chat pribadi dan urutan kirim. **Skill jelas memberi nilai tambah.**
