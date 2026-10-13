# Uji OpenClaw SEBELUM vs SESUDAH — surat-penawaran-harga

## Uji ulang v1.0.5 (2026-10-13, penguji independen)

**Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`). Home bersih per sisi dan sesi baru. SEBELUM = tanpa skill; SESUDAH = hanya skill ini (v1.0.5), bukan paket. Agent dijalankan terisolasi (repo dan folder lain tidak terlihat). Tanggal sistem agent: 14 Okt 2026 (WIB). Pada percobaan pertama, giliran 1 sisi SESUDAH gagal karena router mengembalikan panggilan alat rusak ("incomplete or malformed tool call"). Giliran itu diulang sekali dengan home bersih dan berhasil.

**Skenario (pesan identik, dua giliran, data fiktif):** sama persis dengan uji 2026-10-01. Giliran 1: surat penawaran ke CV Berkah Jaya Bakery untuk desain logo + brand guideline Rp7,5 jt dan 12 template feed IG @Rp150rb, diskon 10% dari total, freelancer belum PKP, DP 50%, berlaku 14 hari. Giliran 2: kota Bandung, nomor WA, "PIC nggak tahu", rekening, pengerjaan 14 hari kerja setelah DP, "sisanya pakai default aja, langsung jadiin".

**Verifikasi angka (Python Decimal, independen):** subtotal Rp9.300.000; diskon 10% Rp930.000; total Rp8.370.000; DP dan pelunasan masing-masing Rp4.185.000; penjual bukan PKP sehingga PPN Rp0 (aturan pembulatan PPN tidak berlaku); berlaku 14 hari dari tanggal surat 14 Okt 2026, yaitu sampai 28 Okt 2026; terbilang "Delapan Juta Tiga Ratus Tujuh Puluh Ribu Rupiah". **Di kedua sisi semua angka benar.**

| Sisi | Skor | Alasan |
|---|---|---|
| SEBELUM (tanpa skill) | 6 | Angka benar dan surat formal cukup rapi, tetapi isi surat hanya disimpan sebagai file di workspace; chat cuma berisi ringkasan angka. Kota "Jakarta" dikarang di giliran 1, dan surat menulis "Harga di atas belum termasuk PPN karena … Non-PKP" (menyiratkan PPN akan menyusul). Tidak ada terbilang dan tidak ada teks WA. |
| SESUDAH (v1.0.5) | 8,5 | Di kedua giliran, chat memuat surat lengkap dan teks WA siap kirim (9 baris, tanpa klaim lampiran). Angka berasal dari script, ada terbilang, kalimat "Harga final; penjual bukan PKP sehingga tidak memungut PPN", dan sapaan "Bapak/Ibu Pimpinan". Perbaikan v1.0.5 terbukti: giliran 1 menulis `[isi: kota]` dan memuat daftar asumsi, lalu giliran 2 memakai Bandung dari member. Minus: kop menambah kata "DESIGN" pada nama penjual (nama usaha tidak diberikan); giliran 2 menambah syarat default (file diserahkan setelah pelunasan) tanpa daftar asumsi; agent sempat mencari folder skill dengan `find /` (dilarang SKILL.md) karena alat baca skill tidak tersedia. |
| **Selisih** | **+2,5** | |

**Verdik: LULUS** (sesudah 8,5 ≥ 8 dan selisih 2,5 ≥ 1,5).

**Pembeda (hanya muncul saat skill aktif):** surat lengkap dan teks WA langsung tampil di chat, dengan kalimat bukan-PKP yang benar dan kota yang tidak ditebak (`[isi: kota]`). Tanpa skill, surat hanya berupa file, kotanya "Jakarta" hasil karangan, dan tertulis "belum termasuk PPN".

Cuplikan jawaban (giliran 1):
> **SEBELUM (chat):** Surat penawaran sudah jadi. Ringkasan perhitungan: … **Total: Rp 8.370.000** (belum PPN, Non-PKP) … File tersimpan di workspace:
> **SEBELUM (isi file):** Jakarta, 14 Oktober 2026
> **SEBELUM (isi file):** - Harga di atas belum termasuk PPN karena penyedia jasa bukan Pengusaha Kena Pajak (Non-PKP).
>
> **SESUDAH:** [isi: kota], 14 Oktober 2026
> **SESUDAH:** | **TOTAL** | **Rp 8.370.000** |
> **SESUDAH:** Terbilang: *Delapan Juta Tiga Ratus Tujuh Puluh Ribu Rupiah*
> **SESUDAH:** 1. Harga final; penjual bukan PKP sehingga tidak memungut PPN.
> **SESUDAH:** 2. Penawaran berlaku sampai 28 Oktober 2026 (14 hari sejak tanggal surat).
> **SESUDAH (teks WA):** Total: *Rp 8.370.000* (tanpa PPN, bukan PKP)
> **SESUDAH (teks WA):** Surat penawaran resminya menyusul ya, Bapak/Ibu. …
> **SESUDAH (asumsi):** - Kota surat belum disebut → `[isi: kota]`.

---

## Riwayat — uji 2026-10-01 (sebelum uji ulang di atas)

Sumber (ada di paket VIP): `solusi-vip/konsultan/UJI-OPENCLAW.md` (rincian: `solusi-vip/konsultan/uji-openclaw/02-surat-penawaran-harga.md`, `02-surat-penawaran-harga-ulang.md`, `02-surat-penawaran-harga-ulang3.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.3); uji ulang ke-2 = 1.0.3; uji ulang ke-3 = 1.0.4 (versi katalog saat ini 1.0.5). Penguji: agent penguji independen (bukan pembuat skill).

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
