# Tahu Kenapa Laba Meleset dari Rencana

**Tempel anggaran vs realisasi, dapatkan penyebab selisih per pos, apa yang perlu dicek, dan pesan siap kirim ke tim, dengan angka yang dihitung langsung dari data Anda.**

Diuji AI penguji independen di OpenClaw: 5,75 → 8,5 dari 10 (selisih dipecah "karena harga" atau "karena jumlah", dan permintaan menggeser angka untuk investor ditolak).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Rekap 1 layar:** laba meleset berapa, pos mana penyebab terbesarnya, urut dari rupiah terbesar
- ✅ Bedakan **"karena harga" atau "karena jumlah"**: penjualan dipecah jadi efek harga, jumlah terjual, dan campuran produk; lembur/bahan dipecah jadi efek tarif vs jam/pemakaian
- ✅ Arah dinilai sesuai jenis pos: pendapatan naik = bagus, biaya naik = merugikan; biaya bahan (HPP)/komisi disesuaikan dengan naik-turunnya penjualan, jadi tahu mana kenaikan yang wajar
- ✅ Daftar **yang perlu dicek** (sebagai pertanyaan, bukan tuduhan) + tindakan bulan depan
- ✅ **Pesan WA/Telegram singkat ke tim** siap kirim, tanpa menyalahkan siapa pun

## Cocok untuk siapa
- Pemilik kafe, resto, toko online, laundry, bengkel, jasa kebersihan, konveksi yang punya anggaran bulanan/kuartalan
- Manajer toko/cabang dan admin keuangan yang menyiapkan bahan rapat bulanan
- Pendamping UMKM dan konsultan yang membantu klien membaca laporan

## Contoh sebelum & sesudah
**Sebelum:** "Laba Juli turun 6 juta, kayaknya karena sepi." Tidak jelas pos mana, berapa, dan apa yang harus dibenahi.

**Sesudah (cukup tempel tabel atau ketik):** "Anggaran penjualan minuman 62 jt realisasi 57,4 jt, makanan 18 jt jadi 21,3 jt, HPP 24 jt jadi 25,9 jt, iklan 1,5 jt jadi 3,2 jt, ... kok laba turun?"
Cuplikan keluarannya (contoh dengan data fiktif, dari `examples/01-kafe-bulanan-8-pos.md`; HPP = modal bahan yang terpakai):

```
**Rekap Juli 2026: laba Rp23.750.000 vs rencana Rp30.000.000 (−Rp6.250.000, −20,8%)**
Pendapatan hanya kurang Rp1,3 jt (−1,6%), tapi biaya naik Rp4,95 jt (+9,9%). Penyebab terbesar: penjualan minuman turun Rp4,6 jt (sebagian tertutup makanan +Rp3,3 jt), lalu HPP bahan +Rp1,9 jt dan iklan +Rp1,7 jt.

| Pos | Selisih | Keterangan |
|---|---|---|
| Penjualan minuman | −Rp4.600.000 (−7,4%) | merugikan; terbesar |
| Penjualan makanan | +Rp3.300.000 (+18,3%) | menguntungkan |
| HPP bahan baku | +Rp1.900.000 (+7,9%) | merugikan; padahal penjualan turun |
| Iklan & promosi | +Rp1.700.000 (+113,3%) | merugikan; lebih dari 2× rencana |
…
| **Laba** | **−Rp6.250.000 (−20,8%)** | margin 37,5% → 30,2% |
```

Disusul penjelasan HPP, 5 hal yang perlu dicek (dalam bentuk pertanyaan), 4 tindakan bulan depan, dan pesan 3 baris untuk tim.

Contoh lain di `examples/`: toko hijab online per kuartal (barang terjual naik tapi laba turun karena harga pashmina turun dan campuran produk bergeser ke yang murah) dan jasa kebersihan (lembur naik Rp7,1 jt: Rp6,5 jt karena jam, Rp615 rb karena tarif).

## Cara pakai
Ketik permintaan biasa ke AI agent Anda, misalnya:
- "Ini anggaran vs realisasi bulan ini, kenapa biaya over budget?" (tempel tabel atau lampirkan file ekspor dari Excel/aplikasi kasir)
- "Penjualan naik tapi untung turun, salahnya di mana? Ini unit dan harga tiap produk."
- "Lembur bengkak, karena jamnya atau tarifnya?"

Tabel cukup berisi kolom pos, anggaran, realisasi. Kalau ada jumlah unit/harga atau jam lembur, hasilnya lebih tajam.

## Instalasi singkat
Salin folder `analisis-selisih-anggaran` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`). Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputer Anda.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent (v1.0.1), skor 1–10: tanpa skill **5,75** → dengan skill **8,5** (LULUS). Dua skenario: anggaran kafe 8 pos (juga di konteks Telegram) dan permintaan menggeser angka agar laporan investor tampak sesuai target; angka dicocokkan hitung ulang independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Angka di bagian "Bukti uji di bot Telegram" di bawah dari uji bot asli terpisah.

**Status uji (jujur):** diuji OpenClaw (uji otomatis agent) dan bot Telegram asli (selisih kecil di bot asli). Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), 2026-10-12.
- Tanpa skill: skor **7,5** — angka sudah benar dan menolak memoles laporan investor.
- Dengan skill: skor **8** — ditambah tabel selisih per pos, penyesuaian volume, daftar tindakan, pesan siap kirim ke tim. Verdik: BELUM (selisih skor < 1,5).

## FAQ
**Apakah AI akan memastikan siapa/apa penyebab selisihnya?**
Tidak. Angka hanya menunjukkan di mana dan berapa selisihnya, dan apakah karena harga atau jumlah. Penyebab pastinya ditulis sebagai daftar pemeriksaan yang Anda cek ke nota, rekening, dan catatan stok. AI tidak menuduh karyawan atau pemasok.

**Apa arti "material"?**
Selisih yang layak dibahas. Default-nya selisih minimal Rp500 ribu atau 5% dari anggaran. Anda bisa mengubahnya, misalnya Rp1 juta dan 10% untuk usaha yang lebih besar.

**Bisa dipakai untuk membuat laporan ke investor terlihat sesuai target?**
Tidak. Skill ini menolak mengubah atau menggeser angka realisasi. Sebagai gantinya ia membantu menyusun penjelasan jujur + rencana perbaikan berangka, yang justru lebih dipercaya investor dan bank.

> **Catatan penting:** alat bantu membaca laporan, bukan nasihat akuntansi, pajak, atau keuangan. Angka hanya dihitung dari data yang Anda berikan dan tidak diaudit; keputusan besar (investasi, pinjaman, laporan ke investor/bank) sebaiknya dibahas dengan akuntan Anda.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
