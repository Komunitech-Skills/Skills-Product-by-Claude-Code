# Tahu Kenapa Laba Meleset dari Rencana

**Tempel anggaran vs realisasi, dapatkan penyebab selisih per pos, apa yang perlu dicek, dan pesan siap kirim ke tim, dengan angka yang dihitung pasti.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Rekap 1 layar:** laba meleset berapa, pos mana penyebab terbesarnya, urut dari rupiah terbesar
- ✅ Bedakan **"karena harga" atau "karena jumlah"**: penjualan dipecah jadi efek harga, volume, dan campuran produk; lembur/bahan dipecah jadi efek tarif vs jam/pemakaian
- ✅ Arah selalu benar: pendapatan naik = bagus, biaya naik = merugikan; biaya bahan/komisi disesuaikan dengan naik-turunnya penjualan, jadi tahu mana kenaikan yang wajar
- ✅ Daftar **yang perlu dicek** (sebagai pertanyaan, bukan tuduhan) + tindakan bulan depan
- ✅ **Pesan WA/Telegram singkat ke tim** siap kirim, tanpa menyalahkan siapa pun

## Cocok untuk siapa
- Pemilik kafe, resto, toko online, laundry, bengkel, jasa kebersihan, konveksi yang punya anggaran bulanan/kuartalan
- Manajer toko/cabang dan admin keuangan yang menyiapkan bahan rapat bulanan
- Pendamping UMKM dan konsultan yang membantu klien membaca laporan

## Contoh sebelum & sesudah
**Sebelum:** "Laba Juli turun 6 juta, kayaknya karena sepi." Tidak jelas pos mana, berapa, dan apa yang harus dibenahi.

**Sesudah (cukup tempel tabel atau ketik):** "Anggaran penjualan minuman 62 jt realisasi 57,4 jt, makanan 18 jt jadi 21,3 jt, HPP 24 jt jadi 25,9 jt, iklan 1,5 jt jadi 3,2 jt, ... kok laba turun?"
→ **Laba Rp23.750.000 vs rencana Rp30.000.000 (−20,8%).** Penyebab terbesar: minuman −Rp4,6 jt, bahan +Rp1,9 jt (padahal penjualan turun, jadi kelebihan wajarnya Rp2,29 jt), iklan +Rp1,7 jt (+113%). Lalu 5 hal yang perlu dicek, 4 tindakan, dan pesan 3 baris untuk tim.

Contoh lain di `examples/`: toko hijab online per kuartal (barang terjual naik tapi laba turun karena harga pashmina turun dan campuran produk bergeser ke yang murah) dan jasa kebersihan (lembur naik Rp7,1 jt: Rp6,5 jt karena jam, Rp615 rb karena tarif).

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 5,75 tanpa skill menjadi 8,5 dengan skill (skala 10). Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Ketik permintaan biasa ke AI agent kamu, misalnya:
- "Ini anggaran vs realisasi bulan ini, kenapa biaya over budget?" (tempel tabel atau lampirkan CSV/ekspor Excel)
- "Penjualan naik tapi untung turun, salahnya di mana? Ini unit dan harga tiap produk."
- "Lembur bengkak, karena jamnya atau tarifnya?"

Tabel cukup berisi kolom pos, anggaran, realisasi. Kalau ada jumlah unit/harga atau jam lembur, hasilnya lebih tajam.

## Instalasi singkat
Salin folder `analisis-selisih-anggaran` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`). Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputermu.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 13, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1097/1166 — skor 7,5
- Dengan skill: https://t.me/c/4407409583/1098/1168 — skor 8
Verdik gelombang: BELUM — Tanpa skill sudah benar angkanya dan menolak memoles laporan investor; dengan skill ditambah tabel selisih per pos berpersen, penyesuaian volume, daftar tindakan, dan pesan siap kirim ke tim, tetapi selisihnya belum mencapai acuan 1,5.

## FAQ
**Apakah AI akan memastikan siapa/apa penyebab selisihnya?**
Tidak. Angka hanya menunjukkan di mana dan berapa selisihnya, dan apakah karena harga atau jumlah. Penyebab pastinya ditulis sebagai daftar pemeriksaan yang kamu cek ke nota, rekening, dan catatan stok. AI tidak menuduh karyawan atau pemasok.

**Apa arti "material"?**
Selisih yang layak dibahas. Default-nya selisih minimal Rp500 ribu atau 5% dari anggaran. Kamu bisa mengubahnya, misalnya Rp1 juta dan 10% untuk usaha yang lebih besar.

**Bisa dipakai untuk membuat laporan ke investor terlihat sesuai target?**
Tidak. Skill ini menolak mengubah atau menggeser angka realisasi. Sebagai gantinya ia membantu menyusun penjelasan jujur + rencana perbaikan berangka, yang justru lebih dipercaya investor dan bank.

> **Catatan penting:** alat bantu membaca laporan, bukan nasihat akuntansi, pajak, atau keuangan. Angka hanya dihitung dari data yang Anda berikan dan tidak diaudit; keputusan besar (investasi, pinjaman, laporan ke investor/bank) sebaiknya dibahas dengan akuntan Anda.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
