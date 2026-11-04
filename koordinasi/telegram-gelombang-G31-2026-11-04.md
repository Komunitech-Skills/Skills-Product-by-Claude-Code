# Gelombang Telegram G31 — 2026-11-04 (bot kedua @KTclaude2bot, Akun B)

Uji formal ulang `kasir-lokal` 1.1.13 dan `absensi-lokal` 1.0.11 setelah `channels.telegram.streaming.mode = off` (keputusan 124/126). Grup uji, topik baru 2373–2376, 8 pesan (4 pembuka + 4 balasan "ya"), database dan workspace direset antar sisi (`g28/pasang.sh`), sisi TANPA dengan `skills: []` dan folder skill dipindah. Pra-cek konteks Telegram sebelum kirim: kasir 7/7, absensi 7/7 butir. Pesan identik dengan G28/G29 (Warung Kopi Mbak Sri fiktif; mesin fingerprint September, 3 karyawan, fiktif).

## Skor (dua penilai Opus independen; pemeriksa kedua menghitung ulang dari data mentah sebelum membuka kunci)
| Skill | Versi | Topik (TANPA/DENGAN) | Penilai 1 | Pemeriksa kedua | Verdik |
|---|---|---|---|---|---|
| kasir-lokal | 1.1.13 | 2373 / 2374 | 5 → 9 (+4,0) | 6 → 9 (+3,0) | **LULUS** |
| absensi-lokal | 1.0.11 | 2375 / 2376 | 7 → 9 (+2,0) | 7 → 9 (+2,0) | **LULUS** |

Acuan: DENGAN ≥ 8, selisih ≥ 1,5, tanpa salah angka kunci, tanpa kebocoran sisi DENGAN. Semua terpenuhi.

## Angka (dihitung ulang independen dengan python3 -I)
- Kasir: subtotal 39.000, diskon 10% 3.900, total 35.100, kembalian 64.900 (cocok di balasan DENGAN).
- Absensi: telat Andi 3× (66 mnt), Joko 3× (75 mnt; 17/09 masuk 08.08 masih toleransi), Sari 0×; Andi 25/09 tanpa tap pulang; 14/09 kosong untuk ketiganya, Sari juga 21 dan 22/09; 121 catatan tersimpan (Andi 41, Sari 38, Joko 42). Kedua kunci.json benar.

## Kebocoran monolog (tujuan uji ini)
- Sisi DENGAN: tidak ada, di kedua skill; tiap topik tepat 2 balasan bot.
- Sisi TANPA kasir: ada satu pesan terpisah ("Tidak ada tindakan yang perlu diambil — ini cuma konfirmasi 'ya' dari user…") dan jalur `transaksi.csv`; itu perilaku bot tanpa skill, justru bagian dari pembeda. Sisi TANPA absensi: ringan ("web search lagi gak tersedia"), menyatu dengan jawaban.
- Total sejak `streaming.mode: off`: kasir-lokal DENGAN 4 run sah (G30b, G30c ×2, G31), absensi-lokal DENGAN 1 run, 0 kebocoran. Sebelumnya G28/G29 bocor.

## Catatan jujur
- Sisi TANPA kasir **TERKONTAMINASI** (aturan 115): bot membuka salinan skill di folder uji pra-cek (`homes/pc28-kasir-lokal`). Nilai TANPA tetap dipakai; kontaminasi hanya mempersempit selisih. Sisi TANPA absensi BERSIH.
- Kekurangan kecil sisi DENGAN absensi: 14/09 disebut dua kali, kalimat setelah simpan tidak persis format SKILL.md. Kasir: struk 32 kolom benar; tampil sebagai blok kode tidak bisa dipastikan dari log.
- n kecil per skill (1 gelombang formal); kebocoran acak, jadi pantau di beta/produksi.
- Member VIP memakai OpenClaw dengan default mode `progress`: saran `streaming.mode: off` untuk panduan setup (teks saja).

## Pembeda (bahasa awam)
- Kasir: tanpa skill, penjualan langsung dicatat diam-diam ke file dan bot "ngomong sendiri"; dengan skill, pemilik melihat dulu menu, pengaturan toko dan struk, lalu cukup balas "ya" sekali.
- Absensi: tanpa skill, hanya daftar telat dan bolong; dengan skill, rekap lengkap (hadir sekian dari 22 hari, total menit telat, jam kerja, hari yang perlu dicek) dan cukup sekali "ya" untuk menyimpan.
