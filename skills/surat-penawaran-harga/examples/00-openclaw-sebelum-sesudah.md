# Uji OpenClaw SEBELUM vs SESUDAH — surat-penawaran-harga

Sumber: `solusi-vip/konsultan/UJI-OPENCLAW.md` (rincian: `solusi-vip/konsultan/uji-openclaw/02-surat-penawaran-harga.md`, `02-surat-penawaran-harga-ulang.md`, `02-surat-penawaran-harga-ulang3.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.3); uji ulang ke-2 = 1.0.3; uji ulang ke-3 = 1.0.4 (versi katalog saat ini 1.0.5). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Konsultan & Freelancer (25 skill). Pesan member identik di kedua sisi, dua giliran (giliran 2 menjawab pertanyaan agent).
- Pesan member: surat penawaran ke CV Berkah Jaya Bakery untuk jasa desain logo + brand guideline Rp7,5 juta dan 12 template feed IG @Rp150.000, diskon 10% dari total, freelancer belum PKP, DP 50%, berlaku 14 hari.
- Angka dihitung ulang penguji dengan Python.

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Surat penawaran jasa desain, non-PKP, diskon 10%, DP 50% | 7 | 8 | 7,5 (ulang ke-2, v1.0.3) dan 8 (ulang ke-3, v1.0.4) | Tanpa skill angka benar tetapi menulis "harga belum termasuk PPN" (menyiratkan PPN bisa ditambah) dan memasang paket PDF lewat `pip install` tanpa izin member; dengan skill surat lengkap plus teks WA, terbilang, syarat revisi, daftar asumsi, dan "tidak dikenakan PPN (bukan PKP)". |
| | **Rata-rata** (satu skenario) | **7** | **8** | **8** (angka uji ulang terakhir) | |

## Verdik
- Uji ulang ke-2 (1.0.3): **BELUM** (cacat lama hilang tetapi muncul regresi format).
- Uji ulang ke-3 (1.0.4): **LULUS untuk cacat yang dilaporkan, dengan 1 regresi yang perlu patch kecil** (kata sumber).

## Catatan jujur
- Sumber pada uji pertama: angka sama-sama benar dan "selisih kecil; jujurnya ini bukan kemenangan telak". Selisih 1,0 pada uji pertama dan uji ulang terakhir.
- Cacat uji pertama sisi dengan skill: teks WA menulis "Surat penawaran resmi (PDF) terlampir" padahal tidak ada file. Hilang pada uji ulang.
- Regresi uji ulang ke-2: surat hanya disimpan ke file di workspace (member Telegram tidak bisa membukanya) dan teks WA baru dibuat setelah diminta (penguji menambah giliran 3), `[Nama PIC]` muncul padahal member menjawab "PIC nggak tahu", dan teks WA menulis "(belum kena PPN)". Semuanya hilang pada uji ulang ke-3.
- Regresi uji ulang ke-3: giliran 1 menulis kota "Jakarta" yang tidak pernah disebut member dan tidak masuk daftar asumsi; giliran 2 menambah syarat default ("maks 2x revisi minor", format file) tanpa daftar asumsi. README skill mencatat perbaikan kota di 1.0.5; tidak ada catatan uji ulang OpenClaw untuk 1.0.5 di sumber.
- Angka benar di semua putaran: subtotal Rp9.300.000, diskon Rp930.000, total Rp8.370.000, DP/pelunasan Rp4.185.000, berlaku sampai 15 Okt 2026.
- Hanya satu skenario surat di OpenClaw.
