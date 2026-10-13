# Hitung Modal & Harga Jual yang Pas

**Dari resep dan daftar belanja, langsung dapat modal sebenarnya per produk (HPP), harga jual ideal, dan target penjualan minimal.**

*Diuji AI penguji independen: 8 → 8,5 dari 10 (selisih kecil karena hitungan modal tanpa skill juga benar; nilai tambahnya tabel titik impas atau BEP per pilihan harga yang dihitung skrip).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ HPP (harga pokok, yaitu modal sebenarnya per produk) dihitung rinci: bahan, tenaga kerja, biaya tak langsung seperti sewa dan gas (overhead), kemasan, sampai penyusutan alat — sebaik data yang Anda isi
- ✅ Konversi satuan otomatis: beli 1 kg pakai 250 g, kain per yard dipakai per meter, lusin, kodi
- ✅ Harga jual dari target margin atau markup, lengkap penjelasan bedanya
- ✅ BEP (titik impas): tahu berapa produk minimal harus terjual per bulan agar tidak rugi
- ✅ Cocok untuk makanan, fashion, kerajinan, dan jasa

## Cocok untuk siapa
- Pelaku usaha kuliner rumahan, katering, dan kue
- Konveksi, penjahit, dan brand fashion lokal
- Pengrajin, serta penyedia jasa (desainer, fotografer, jasa servis) yang ingin tarif tidak asal tebak

## Contoh sebelum & sesudah
**Sebelum:** "Modal brownies kira-kira 30 ribuan lah, jual 50 ribu." Ternyata upah, gas, box, dan oven belum dihitung.

**Sesudah (cukup ketik):** "Mau hitung modal keripik pisang balado. Sekali produksi: pisang 10 kg (8 ribu/kg), minyak 2 liter (19 ribu/liter), bumbu balado 250 gram (beli 1 kg 60 ribu). Jadinya 40 bungkus. … Sebulan produksi 480 bungkus. Mau margin 35%, jual berapa?"

*Cuplikan hasil nyata dari `examples/01-keripik-pisang-margin-35.md` (tabel rincian per bahan dipotong):*
```
**Ringkasan HPP per bungkus**

- Bahan baku: Rp 3.325
- Tenaga kerja: Rp 1.250
- Overhead: Rp 1.525
- Kemasan: Rp 850
- **HPP per bungkus: Rp 6.950**
…
- **Harga rekomendasi: Rp 11.000** -> laba Rp 4.050 per bungkus (margin 36,82%, markup 58,27%)
…
- **BEP: 114 bungkus per bulan** (tepatnya 113,21), atau omzet **Rp 1.245.284** per bulan
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Hitung HPP kemeja: kain 1,6 meter (beli 45 ribu per yard), kancing 7 biji, ongkos jahit 35 ribu."
- "Tarif jasa foto produk saya per sesi berapa kalau mau markup 100%?"
- "Harga jual saya 65 ribu, masih untung? Berapa BEP-nya?"

## Instalasi singkat
Salin folder `hitung-hpp` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, dua sumber yang terpisah.
- **Uji OpenClaw, 1 Oktober 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario es kopi): skor tanpa skill 8 → dengan skill 7 pada uji pertama (skill kalah), lalu 8,5 setelah perbaikan v1.0.4. Selisih akhir hanya +0,5: hitungan modal tanpa skill juga benar; yang ditambahkan skill adalah tabel titik impas (BEP) per pilihan harga dari skrip.
- **Uji simulasi agent, 23 September 2026** (`examples/00-pembanding-tanpa-skill.md`, resep keripik pisang balado dengan target margin 35%): agent tanpa skill menukar margin dengan markup, sehingga harga Rp9.500 (margin sebenarnya hanya sekitar 26,8%) dan tanpa BEP. Dengan skill harga Rp11.000 (margin 36,82%) dan BEP 114 bungkus per bulan. Selisihnya Rp1.500 per bungkus, sekitar Rp720.000 per bulan pada 480 bungkus.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Hasil uji di bot Telegram ada di bagian berikut.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 2–3, 2026-10-02 (skenario usaha-offline). Versi yang diuji tidak tercatat di catatan gelombang (versi repo saat itu: 1.0.4, sama dengan versi terkini).
- Tanpa skill: https://t.me/c/4407409583/518/520 — skor tidak dicatat di gelombang itu
- Dengan skill: https://t.me/c/4407409583/235/533 — skor tidak dicatat di gelombang itu
Verdik gelombang: tidak dicatat di gelombang itu — DENGAN HPP Rp6.950, harga Rp11.000 (margin 36,82%), titik impas 114 bungkus/bln, cocok dengan contoh teruji; TANPA HPP Rp6.950 benar tetapi memberi dua pilihan harga (Rp10.700 / Rp9.400) dan bertanya definisi margin.

## FAQ
**Apa bedanya margin dan markup?**
Margin dihitung dari harga jual, markup dari modal. Modal Rp70.000 dijual Rp100.000: margin 30%, markup 42,86%. Skill menampilkan keduanya supaya tidak tertukar.

**Bahan saya pakai sendok, bukan gram. Bisa?**
Takaran sendok berbeda-beda, jadi skill meminta Anda menimbang sekali (gram/ml) supaya hitungannya akurat. Atau samakan satuan beli dan pakai, misalnya beli 1 sachet, pakai 1 sachet.

**Setelah dapat HPP, bagaimana harga di marketplace?**
Pakai HPP ini sebagai modal di skill Komunitech lain, `harga-jual-marketplace` (menghitung harga jual di marketplace), untuk menghitung potongan admin, gratis ongkir, dan PPh 22 (pajak yang dipungut marketplace).

> **Catatan penting:** alat bantu hitung harga pokok dan harga jual, bukan nasihat keuangan atau pajak dan bukan laporan keuangan resmi. Hasil hanya sebaik data yang Anda isi; biaya yang belum dimasukkan (mis. upah pemilik) tidak ikut terhitung dan disebut sebagai asumsi. Pajak (PPN/PPh) tidak dihitung di sini.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
