# Uji OpenClaw SEBELUM vs SESUDAH — notulen-rapat

Sumber (ada di paket VIP): `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` (rincian: `solusi-vip/kantor-manajemen/uji-openclaw/01-notulen-rapat-catatan-berantakan.md` dan `01-notulen-rapat-ulang3.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.3); uji ulang ke-3 = 1.0.3 (versi katalog saat ini 1.0.4). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Kantor & Manajemen. Kedua home dibuat ulang bersih sebelum skenario.
- Pesan member: catatan rapat mingguan 1/10 yang berantakan (peserta, "sales sept 2,1M target 2,5M", "jumat depan", "sebelum rabu", "besok", "forklift 2 rusak", rapat berikutnya "kamis depan").
- Kalender dicek penguji dengan Python (1 Okt 2026 = Kamis).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang ke-3, v1.0.3) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Notulen dari catatan rapat berantakan (tanggal relatif, satuan angka) | 6 | 8,5 | 9 | Tanpa skill "2,1M" ditulis Rp2.100.000, tanggal relatif tidak dikonversi, dan satu tugas dikarang; dengan skill tanggal dihitung script ("Sebelum Rabu, 7 Oktober 2026"), satuan "M" ditandai untuk dikonfirmasi, dan ada ringkasan siap tempel ke grup. |
| | **Rata-rata** (satu skenario) | **6** | **8,5** | **9** | |

## Verdik
**LULUS uji ulang ke-3** (9). Sumber menempatkan skenario ini sebagai salah satu pembeda nyata paket Kantor & Manajemen (tanggal relatif dikonversi pasti).

## Catatan jujur
- Satu skenario saja di OpenClaw; sisi tanpa skill tidak diulang pada uji ulang.
- Cacat uji pertama sisi dengan skill yang hilang pada uji ulang ke-3: script tidak mengenali "sebelum rabu"; "forklift 2 rusak" ditafsirkan 2 unit (kesalahan yang sama juga terjadi di sisi tanpa skill); tawaran "Mau saya tanyakan ke Tono dulu?".
- Temuan uji ulang ke-3: muncul tugas tambahan "Proses sewa forklift sementara - Hendra" yang tidak ada di catatan (ditandai peringatan "belum ada tenggat", tetapi melampaui catatan); sel tenggat Tono menulis 9 Okt padahal ditandai ambigu; "harga palet maksimal Rp85.000" ditaruh di bagian Keputusan (tafsir ringan). README skill mencatat perbaikan tugas tambahan di 1.0.4; tidak ada catatan uji ulang OpenClaw untuk 1.0.4 di sumber.
- Uji pertama: satuan "M" juga ditandai ambigu oleh sisi dengan skill (aman, tetapi agak berlebihan).
