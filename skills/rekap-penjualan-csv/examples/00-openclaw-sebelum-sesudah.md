# Uji OpenClaw SEBELUM vs SESUDAH: rekap-penjualan-csv

**Sumber (ada di paket VIP):** `solusi-vip/toko-online/UJI-OPENCLAW.md` (tabel skor skenario 02, bagian "Cacat per skill" dan "Uji ulang 2026-10-01") dengan rincian per skenario di `solusi-vip/toko-online/uji-openclaw/02-rekap-penjualan-csv.md` dan `02-rekap-penjualan-csv-ulang.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.2.2 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang = 1.2.3. Versi di katalog saat ini: 1.2.5.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Toko Online (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home `kosong-toko-online` (folder skill kosong). **SESUDAH** = home `sol-toko-online` (paket skill Toko Online + skill tambahan VIP). Pesan identik di kedua sisi.
- File uji fiktif `penjualan-september.csv` (72 baris gaya ekspor Shopee: 66 Selesai, 4 Batal, 2 Pengembalian Dana; tanpa nama atau nomor pembeli) disalin identik ke kedua workspace.
- Uji ulang hanya mengulang sisi SESUDAH; skor SEBELUM dipakai ulang dari uji pertama. Angka dihitung ulang penguji dengan Python (`csv`), terpisah dari script skill.

**Pesan member (skenario 02):** "td aku udh taro file penjualan-september.csv di folder kerja (export dr shopee). tolong rekapin dong omzet sebulan brp, produk paling laku apa, sama hari paling rame kapan"

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 02 Rekap penjualan sebulan dari CSV Shopee, uji pertama | ±1.2.2 | 7,5 | 8,5 | Kedua sisi benar (omzet Rp3.038.000 dari 66 pesanan Selesai, Batal dan Pengembalian Dana dibuang); dengan skill menambah persentase kontribusi, rata-rata harian (kalender Rp101.267, hari berjualan Rp108.500) dan 3 insight, tetapi "hari paling rame" hanya dijawab dari omzet, sedangkan tanpa skill menjawab dari omzet dan jumlah pesanan. |
| 02, uji ulang (hanya sisi SESUDAH) | 1.2.3 | 7,5 (dari uji pertama) | 9 | "Transaksi terbanyak: 1 & 5 September, sama-sama 5 pesanan unik" (benar) kini muncul, ditambah catatan data (6 baris dibuang, tidak ada baris error). |
| **Rata-rata skenario ini** (skenario tunggal) | | **7,5** | **8,5** (uji pertama) → **9** (1.2.3) | Selisih +1 pada uji pertama, +1,5 pada uji ulang. |

Rata-rata seluruh solusi toko-online (5 skenario, skill berbeda) di uji pertama: 6,4 → 8,4. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS uji ulang (skor 9, 1.2.3).** Semua angka cocok dengan hitungan independen.

## Catatan jujur
- Sumber menegaskan selisihnya kecil: model tanpa skill sudah hampir sama tepat angkanya, jadi skenario ini **tidak boleh dijual sebagai pembeda besar**. Pembeda utamanya kelengkapan dan konsistensi format, bukan ketepatan angka.
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Versi 1.2.4 dan 1.2.5 (2 Okt 2026: omzet per status, ringkasan siap tempel, opt-in promo, larangan broadcast) hasil uji gabungan paket toko-online (catatan internal kurator, tidak disertakan dalam paket, bagian 11), bukan uji per-skill; skor gabungan itu bukan skor skill ini.
- Balasan uji ulang menyapa member "Sol": artefak nama home uji, bukan perilaku skill.
- Satu skenario, satu file contoh; belum menguji format ekspor lain (Tokopedia, kasir kedai) atau angka berformat campur di OpenClaw.
