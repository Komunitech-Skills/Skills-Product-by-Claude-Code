# Siapkan Usaha Anda Siap Dijual atau Diwariskan

**Dari "usaha ini kira-kira dihargai berapa?" sampai rencana serah terima 12 bulan, tanpa janji palsu dan tanpa tebakan angka pasar.**

## Manfaat
- Daftar periksa kesiapan: pembukuan, SOP, ketergantungan pada Anda, aset, utang, kontrak, izin, pelanggan dan pemasok kunci.
- Rentang nilai usaha yang dihitung dari angka dan asumsi Anda sendiri, lengkap dengan rumus dan peringatan (bukan harga pasti).
- Rencana transisi 3-12 bulan per bulan, bisa langsung dikerjakan.
- Daftar dokumen untuk calon pembeli/penerus dan daftar pertanyaan siap bawa ke notaris dan konsultan pajak.
- Jujur soal batas: tidak membuat akta, wasiat, atau pembagian waris, dan tidak menghitung pajak.

## Cocok untuk siapa
Pemilik warung, toko, kafe, bengkel, jasa, atau toko online yang ingin menjual, mewariskan ke anak, atau menyerahkan ke karyawan; pemilik yang mendekati pensiun.

## Contoh sebelum/sesudah
Uji OpenClaw 2026-10-10 (5 skenario, `examples/HASIL-UJI.md`): rata-rata **6,1 tanpa skill → 8,7 dengan skill**.

Kasus warung makan Bu Sri (laba 2023-2025 Rp96 juta/Rp118 juta/Rp134 juta, sisa KUR Rp45 juta, kebutuhan pensiun Rp8 juta/bulan selama 2 tahun):
- **Tanpa skill:** memakai rata-rata tertimbang buatan sendiri dan menyimpulkan "realistis laku di kisaran 190-280 jt" seolah angka pasar; persiapan hanya berupa saran singkat, tanpa daftar periksa berstatus, rencana transisi per bulan, atau daftar pertanyaan notaris/konsultan pajak.
- **Dengan skill (v1.0.1):** laba disesuaikan dengan gaji manajer pengganti, potongan karena resep masih di kepala pemilik, lalu dipisah jelas: nilai usaha Rp176.800.000 s/d Rp265.200.000, setelah biaya 5% Rp167.960.000 s/d Rp251.940.000, **hasil bersih ke Bu Sri setelah melunasi KUR Rp122.960.000 s/d Rp206.940.000**, dibanding kebutuhan Rp192.000.000: bisa kurang Rp69.040.000 di harga rendah. Plus daftar periksa, rencana transisi, dan pertanyaan untuk notaris/konsultan pajak.

## Instalasi singkat
Salin folder ini ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Cara pakai:** cukup ketik, misalnya: "Saya mau oper kafe saya tahun depan, bantu siapkan." Data yang kurang ditanyakan sekali, dan angka yang belum Anda berikan tidak dikarang.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 13, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1099/1171 — skor 7
- Dengan skill: https://t.me/c/4407409583/1100/1176 — skor 7,5
Verdik gelombang: BELUM — Tanpa skill ringkas dan tegas bahwa Rp500 juta di atas kisaran wajar; dengan skill lebih lengkap (daftar periksa, rencana 12 bulan, dokumen untuk pembeli, pertanyaan ke notaris) tetapi panjang dan ada kalimat koreksi diri, sehingga selisih belum mencapai acuan 1,5.

## FAQ
**Apakah ini menggantikan notaris?** Tidak. Skill menyiapkan bahan dan pertanyaan; akta dan keputusan hukum tetap lewat notaris.
**Angka nilai usaha dari mana?** Dari laba, aset, dan kelipatan yang Anda berikan. Tanpa kelipatan dari Anda, hasil diberi label contoh hitungan, bukan angka pasar.
**Datanya ke mana?** Tetap di percakapan dan komputer Anda; skill tidak mengirim apa pun.

> **Catatan penting:** hasil berupa rentang hitungan dari angka dan asumsi Anda, bukan penilaian (appraisal) resmi, bukan nasihat hukum, pajak, atau keuangan. Akta, wasiat, pembagian waris, dan pajak tetap lewat notaris, konsultan pajak, atau penilai berizin.

## Riwayat versi
- **1.0.1 (2026-10-10):** biaya sekali jalan (mis. renovasi) kini dicatat per tahun kejadiannya, tidak lagi menaikkan semua tahun; utang dihitung sekali dan terlihat "hasil bersih ke pemilik setelah utang"; jalur beli/lepas bagian sekutu (porsi); daftar pertanyaan notaris/pajak ditambah (persetujuan pasangan, hak ahli waris lain, karyawan, SKB waris, PPN aset) beserta dasar aturan dan tanggal cek.
- **1.0.0 (2026-10-09):** rilis awal.
