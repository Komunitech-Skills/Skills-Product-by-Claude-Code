# Uji OpenClaw SEBELUM vs SESUDAH: arus-kas-13minggu

**Sumber (ada di paket VIP):** `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` (tabel skor skenario 05, bagian "Cacat per skill", "Cuplikan jualan" dan "Uji ulang ke-3 2026-10-01") dengan rincian per skenario di `solusi-vip/kantor-manajemen/uji-openclaw/05-arus-kas-13-minggu-info-kurang.md` dan `05-arus-kas-13-minggu-ulang3.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.2 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang = 1.0.3. Versi di katalog saat ini: 1.0.3.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen ke-3 untuk paket kantor-manajemen (satu-satunya uji ulang skill ini).

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Kantor & Manajemen (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home `kosong-kantor-manajemen` (tanpa skill). **SESUDAH** = home `sol-kantor-manajemen` (17 skill paket terpasang); uji ulang di home `sol3-kantor-manajemen` dari skill terbaru repo. Kedua home dibuat ulang bersih sebelum skenario; pesan dan jawaban lanjutan identik.
- Skenario "info kurang lalu dilengkapi": member hanya memberi saldo awal, agent bertanya sekali, member menjawab satu kali (sama di kedua sisi).
- Uji ulang hanya mengulang sisi SESUDAH; skor SEBELUM dipakai ulang dari uji pertama. Saldo mingguan, total, dan simulasi dihitung ulang penguji dengan Python.

**Pesan member (skenario 05, giliran 1):** "bikinin proyeksi arus kas 13 minggu dong. saya takut kas ga cukup buat gaji akhir bulan. saldo kas sekarang sekitar 380 juta" (giliran 2: data pemasukan Rp210 jt per minggu (minggu 1-2 hanya Rp150 jt), gaji Rp420 jt tiap tanggal 25, supplier Rp130 jt per minggu, sewa Rp75 jt tanggal 5, cicilan Rp62 jt tanggal 15, batas aman Rp100 jt, mulai Senin 5 Oktober).

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 05 Arus kas 13 minggu, info kurang lalu dilengkapi, uji pertama | ±1.0.2 | 7,5 | 8,5 | Tabel 13 minggu benar di kedua sisi, tetapi dengan skill ada status per minggu terhadap batas aman, defisit struktural dihitung (-Rp751 jt), opsi tindakan disimulasikan dengan angka (termasuk bukti "geser termin supplier hanya menunda") dan file CSV, sedangkan narasi salah menaruh cicilan Rp62 jt di minggu 12 (seharusnya minggu 11) dan BPJS/PPh 21 tak disebut sebagai asumsi. |
| 05, uji ulang (hanya sisi SESUDAH) | 1.0.3 | 7,5 (dari uji pertama) | 9 | Kedua cacat hilang: minggu kritis dikutip dari rincian script ("minggu 3 ... Gaji Rp 420.000.000 dan bahan baku Rp 130.000.000 ... total keluar Rp 550.000.000") dan "Belum termasuk pajak/BPJS" ditulis di Asumsi. |
| **Rata-rata skenario ini** (skenario tunggal) | | **7,5** | **8,5** (uji pertama) → **9** (1.0.3) | Selisih +1 pada uji pertama, +1,5 pada uji ulang. |

Rata-rata seluruh solusi kantor-manajemen (5 skenario, skill berbeda) di uji pertama: 7,0 → 8,3; setelah uji ulang ke-3 sisi SESUDAH 8,9. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS uji ulang ke-3 (skor 9, 1.0.3).** Semua angka (13 saldo mingguan, total masuk Rp2.610 jt, keluar Rp3.361 jt, kebutuhan dana Rp451 jt / Rp551 jt dari batas aman, simulasi opsi) cocok dengan hitungan independen dan `proyeksi_kas.py`.

## Catatan jujur
- Model tanpa skill sudah kuat: tabel 13 minggu benar tanpa script dan menyimpulkan "kas jebol sebelum gaji 25 Okt". Pembeda ada di simulasi opsi berangka, file Excel/CSV, dan status per minggu, bukan di tabel dasarnya.
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Pada uji ulang, argumen tool call tidak dibaca; `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan (tidak terlihat). Sisa kecil: opsi 4 tidak menyebut saldo terendah selama periode (-Rp191 jt minggu 12) yang dicetak script; tetap benar.
- Satu skenario saja; skenario tanpa piutang besar, THR, atau pajak/BPJS belum diuji di OpenClaw.

## Cuplikan dari sumber (uji pertama)
- Tanpa skill: "Nego termin bayar supplier: geser dari mingguan ke 2-mingguan ..." (tanpa hitungan).
- Dengan skill: "Naikkan pemasukan ±Rp 60 juta/minggu → saldo terendah naik dari -Rp 451.000.000 menjadi +Rp 123.000.000 ... Negosiasi termin ... INI HANYA MENUNDA ... saldo tetap minus Rp 371.000.000."
