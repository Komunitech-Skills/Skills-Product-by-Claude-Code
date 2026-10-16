# Uji OpenClaw SEBELUM vs SESUDAH — promo-kalender

Sumber (ada di paket VIP): `solusi-vip/toko-online/UJI-OPENCLAW.md` (rincian: `solusi-vip/toko-online/uji-openclaw/05-promo-1111-cek-margin.md` dan `05-promo-1111-cek-margin-ulang.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.3); uji ulang = 1.0.3 (versi katalog saat ini 1.0.4; 1.0.4 belum diuji ulang di OpenClaw). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Toko Online (21 skill). Pesan member identik; sesi baru per sisi.
- Pesan member: diskon 30% serum 11.11, harga normal Rp89.000, modal Rp41.000, potongan Shopee sekitar 12% + Rp1.250 per pesanan, biasanya laku 60 botol sebulan, minta rencana promo.
- Semua angka dihitung ulang penguji dengan Python (laba = harga - 12% x harga - 1.250 - 41.000).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang, v1.0.3) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Promo 11.11 diskon 30%: masih untung? + rencana | 6,5 | 8 | 8,5 | Tanpa skill target "173 botol" membandingkan promo 1-3 hari dengan laba sebulan penuh, memakai klaim pasar tanpa dasar (lonjakan 2-4x) dan tanpa syarat & ketentuan; dengan skill jawaban "masih untung", batas diskon maksimal 46%, target 6 botol untuk promo 1 hari, linimasa bertanggal, dan S&K dengan isian `[isi: ...]` untuk hal yang tidak diberikan pemilik. |
| | **Rata-rata** (satu skenario) | **6,5** | **8** | **8,5** | |

## Verdik
**LULUS uji ulang** (kata sumber: "ketiganya LULUS uji ulang"; cuplikan jualan "layak").

## Catatan jujur
- Satu skenario saja di OpenClaw.
- Cacat uji pertama sisi dengan skill: periode promo tidak konsisten (target dihitung 3 hari, linimasa dan S&K 1 hari) dan S&K memuat janji "Dikirim maks 2 hari kerja" yang tidak diberikan pemilik. Kedua cacat hilang pada uji ulang.
- Regresi kecil pada uji ulang: opsi bundling 2 botol (laba per botol Rp24.375) dan peringatan harga coret palsu tidak muncul lagi, begitu pula pengingat "cek potongan di Seller Center"; jawaban jadi sedikit lebih tipis. Tidak ada angka salah.
- PPh 22 marketplace 0,5% tidak dimasukkan di kedua sisi karena member menyebut potongan "kira-kira 12%"; bila belum termasuk, laba diskon 30% turun menjadi Rp12.263 (hitungan penguji).
- Angka dasar benar di kedua sisi (laba normal Rp36.070; diskon 30% menjadi Rp62.300 dengan laba Rp12.574). Kekurangan sisi tanpa skill ada di kerangka (target 173 botol salah periode), klaim tanpa dasar, dan tidak adanya S&K; bukan di hitungan per botol.
