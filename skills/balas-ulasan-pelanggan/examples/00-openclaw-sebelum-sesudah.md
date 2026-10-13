# Uji OpenClaw SEBELUM vs SESUDAH — balas-ulasan-pelanggan

Sumber: `solusi-vip/klinik/UJI-OPENCLAW.md` (rincian: `solusi-vip/klinik/uji-openclaw/04-balas-ulasan-bintang-1.md`, `04-balas-ulasan-bintang-1-ulang.md`, `04-balas-ulasan-ulang3.md`) dan `solusi-vip/toko-online/UJI-OPENCLAW.md` (rincian: `solusi-vip/toko-online/uji-openclaw/03-balas-ulasan-bintang-1.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.3); uji ulang ke-2 = 1.0.3; uji ulang ke-3 = 1.0.4 (versi katalog saat ini 1.0.5). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home OpenClaw tanpa skill; SESUDAH = home dengan paket skill solusi VIP (toko online / klinik). Pesan member identik di kedua sisi; sesi baru per sisi.
- Panjang balasan dihitung ulang penguji dengan Python; pemakaian skill dilihat dari alat yang dipakai agent (membaca SKILL.md, menjalankan `cek_balasan.py`).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| A | Toko online: ulasan Shopee bintang 1 (telat kirim, warna beda, admin lambat) | 6 | 8,5 | tidak diuji ulang | Tanpa skill balasan 924 karakter (lewat batas aman 500), mengarang "sesuai SLA" dan bernada membantah; dengan skill 469 karakter tercek script, dua versi plus pesan chat pribadi, tidak defensif. |
| B | Klinik: ulasan Google Maps bintang 1 (antre lama, resepsionis jutek, dokter buru-buru) | 5 | 8 | 8,5 (ulang ke-2, v1.0.3) dan 8,5 (ulang ke-3, v1.0.4) | Tanpa skill mencari "login akun password" di memori dan menawarkan posting otomatis lewat login browser serta menyinggung perawatan anak di ruang publik; dengan skill dua versi plus pesan pribadi dicek script, tanpa posting otomatis (setelah revisi: tanpa menyebut anak/pemeriksaan di balasan publik). |
| | **Rata-rata** (dihitung dari dua skenario di atas; sumber hanya memberi angka per skenario) | **5,5** | **8,25** | 8,5 (memakai angka uji ulang untuk skenario B) | |

## Verdik
- Skenario B: **LULUS uji ulang ke-3** (cacat privasi pasien hilang dan terbukti oleh `cek_balasan.py --faskes`); tetap **PERLU REVIEW tenaga medis/kepatuhan** sebelum rilis (kata sumber).
- Skenario A: sumber mencatat "tidak ada cacat berarti".

## Catatan jujur
- Hanya 2 skenario di OpenClaw (bukan 5 skenario Tahap 6); skenario A tidak diuji ulang.
- Cacat uji pertama (klinik): balasan publik menulis "saat periksa gigi putra/putri Bapak" sehingga mengonfirmasi perawatan pasien di ruang publik. Hilang pada uji ulang ke-2 dan ke-3.
- Sisa temuan uji ulang ke-3: balasan publik masih menulis "Masukan ini sudah kami bahas bersama tim" tanpa konfirmasi pemilik, dan kata "pasien" dipakai umum ("kejelasan informasi yang diberikan ke pasien"). Satu dari 9 panggilan alat gagal (hasil akhir tetap lulus cek). README skill mencatat perbaikan klaim tindakan di 1.0.5; tidak ada catatan uji ulang OpenClaw untuk 1.0.5 di sumber.
- Skenario A: balasan publik memuat komitmen ("kami pakai untuk perbaiki hasil fotonya", "sedang membenahi respon tim CS"); agent sendiri mengingatkan pemilik agar tidak jadi janji kosong.
- Sisi tanpa skill sebenarnya sudah menulis draf yang cukup baik pada skenario B; pembeda terbesar ada di kepatuhan (tidak membuka detail perawatan, tidak menawarkan posting otomatis), bukan di kalimat balasan.
