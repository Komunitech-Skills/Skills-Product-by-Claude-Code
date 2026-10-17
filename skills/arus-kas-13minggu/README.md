# Tahu Kapan Kas Menipis, Sebelum Terlambat

**Perkiraan (proyeksi) kas 13 minggu ke depan, lengkap dengan tanda bahaya dan jalan keluarnya — cukup ceritakan pemasukan dan pengeluaran Anda.**

*Uji ulang sebelum/sesudah di OpenClaw (16 Oktober 2026, versi 1.0.5): rata-rata tanpa skill 6,75 → dengan skill 8,4 dari 10, lulus. Tabel 13 minggu cocok 100% dengan hitungan ulang independen, setiap pilihan tindakan disertai angkanya, dan kasus toko sembako yang dulu habis waktu kini selesai dalam 4 menit.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tahu **minggu ke berapa** uang usaha diperkirakan kurang dan berapa kurangnya (dari angka yang Anda berikan)
- ✅ Tanggal gajian, sewa, cicilan, dan pajak otomatis ditempatkan di minggu yang benar
- ✅ 3–5 jalan keluar konkret (tagih lebih cepat, atur termin supplier, tunda belanja, pinjaman) **beserta hitungan dampaknya**, dibandingkan berdampingan
- ✅ File tabel (CSV) siap buka di Excel/Google Sheets untuk dipantau tiap minggu
- ✅ Angka dihitung script, bukan dikira-kira

## Cocok untuk siapa
- Pemilik UMKM yang sering deg-degan menjelang tanggal gajian atau jatuh tempo supplier
- Usaha dengan pelanggan yang membayar belakangan (termin/tempo)
- Admin keuangan yang diminta atasan membuat rencana kas 3 bulan

## Contoh sebelum & sesudah
**Sebelum:** "Kayaknya aman sih…" — lalu tiba-tiba kas habis tepat saat gajian karena pembayaran pelanggan baru masuk minggu depannya.

**Sesudah (cukup ketik):** "bikinin dong proyeksi kas 13 minggu. kas 8jt, omzet seminggu 5jt, belanja stok kaos polos+tinta 3,5jt/minggu, gaji 2 org 5jt tiap tgl 1, sewa kios 2,5jt tiap tgl 10, iklan IG 1jt tiap 2 minggu, minggu ke 11 mau beli mesin press 7,5jt"

*Cuplikan hasil nyata dari `examples/03-bikinin-dong-sablon-kaos-minus.md` (minggu lain, opsi tindakan, dan file Excel dipotong):*
```
## Proyeksi Kas 13 Minggu (28 Sep – 27 Des 2026)
Saldo awal Rp 8.000.000 · Batas aman Rp 6.346.154 (asumsi: rata-rata pengeluaran 1 minggu)

| Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
|---|---|---:|---:|---:|---|
| 5 | 26 Okt – 1 Nov | Rp 5.000.000 | Rp 9.500.000 | Rp 0 | 🟡 Di bawah batas |
| 7 | 9 – 15 Nov | Rp 5.000.000 | Rp 7.000.000 | -Rp 500.000 | 🔴 NEGATIF |
| 11 | 7 – 13 Des | Rp 5.000.000 | Rp 14.500.000 | -Rp 11.500.000 | 🔴 NEGATIF |
…
### Kesimpulan
- **Titik paling kritis: minggu 11 (7–13 Des), saldo −Rp 11.500.000.** Penyebabnya mesin press Rp 7.500.000 dibeli saat kas sudah minus (setelah gajian 1 Des), bersamaan dengan sewa kios 10 Des, belanja stok, dan iklan.
- **Kas pertama kali minus di minggu 7 (9–15 Nov), −Rp 500.000**, karena sewa kios jatuh di minggu itu. Minggu 5 (gajian 1 Nov) kas tepat habis, Rp 0.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan proyeksi arus kas 13 minggu dari data ini: …"
- "Uang usaha saya cukup nggak buat bayar THR bulan depan?"
- "Kalau saya beli mesin 25 juta bulan depan, kas saya aman?"

## Instalasi singkat
Salin folder `arus-kas-13minggu` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10.
- **Uji ulang di OpenClaw, 16 Oktober 2026 (versi 1.0.5):** tiga skenario dijalankan ulang (usaha kue, CSV CV dengan tanda `;` berlebih, toko sembako yang bertanya soal menunda pajak/gaji atau pinjol); skor skenario lain dipakai ulang dari 14 Oktober. Rata-rata tanpa skill 6,75 → dengan skill **8,4** (selisih +1,65), **lulus**, tanpa salah angka: tiga tabel 13 minggu dan 15 pilihan tindakan cocok 100% dengan hitungan independen. Ketiga temuan 14 Oktober hilang: kasus sembako selesai 236 detik (dulu habis waktu), pilihan "percepat piutang" menyebut DP dan pelunasan yang digeser, CSV dengan `;` berlebih terbaca. Untuk kasus sembako, AI tanpa skill tidak menghasilkan jawaban dalam tiga percobaan. Catatan jujur: satu kalimat narasi kurang tepat ("seminggu" seharusnya dua minggu), syarat pinjaman di kasus sembako ditulis tanpa label asumsi, dan jawaban kasus kue memakan 8 menit.
- **Uji sebelum/sesudah OpenClaw, 14 Oktober 2026 (versi 1.0.4)** (`examples/00-openclaw-sebelum-sesudah.md`, 5 skenario fiktif: usaha kue, CV dengan file CSV, bengkel yang menimbang order besar, laundry dengan info kurang, toko sembako yang bertanya soal menunda pajak/gaji atau pinjol): rata-rata **6,75 tanpa skill → 8,5 dengan skill** pada 4 skenario yang bisa dinilai. Tabel 13 minggu cocok 100% dengan hitungan ulang independen; contoh beda: tanpa skill satu jawaban menyimpulkan "kas aman, tidak pernah minus" karena gajian terlewat, padahal minggu ke-3 minus Rp700.000. Skenario toko sembako **tidak bisa dinilai**: dengan skill, AI menghitung terlalu banyak simulasi terpisah dan habis waktu sebelum menjawab. Penguji juga mencatat waktu jawab yang lama (sampai lebih dari 10 menit) dan satu kesalahan baca file CSV.
- **Versi 1.0.5** memperbaiki temuan itu: semua pilihan tindakan dihitung dalam satu kali jalan (lebih cepat), setiap pilihan menyebut persis pos mana yang digeser, dan file CSV dengan tanda `;` berlebih kini terbaca. Versi 1.0.5 lulus uji ulang 16 Oktober 2026 (butir pertama).
- **Uji OpenClaw, 1 Oktober 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario: saldo awal Rp380 juta, info dilengkapi setelah ditanya sekali): skor tanpa skill 7,5 → dengan skill 8,5 pada uji pertama, lalu 9 setelah perbaikan v1.0.3.
- **Uji simulasi agent (perbandingan tanpa dan dengan skill), 23 September 2026** (`examples/00-pembanding-tanpa-skill.md`, usaha katering dengan kas Rp 35 juta): jawaban tanpa skill per bulan: "aman, saldo terendah sekitar Rp 14,9 juta". Padahal di minggu ke-6 (2–8 November) saldo tinggal Rp 6.300.000 karena freezer, sewa, dan bahan jatuh di minggu yang sama. Dengan skill titik kritis itu ketemu, lengkap dengan 5 opsi tindakan berangka; saldo 13 minggu cocok dengan hitungan independen (13 dari 13 minggu).

**Status uji (jujur):** versi 1.0.5 lulus uji ulang penguji AI independen di OpenClaw 2026.10.2 pada 16 Oktober 2026 (6,75 → 8,4; tiga skenario diuji ulang, dua dipakai ulang dari 14 Oktober; tanpa salah angka). Uji dengan pengaturan seperti bot Telegram (bukan bot sungguhan) terakhir pada versi 1.0.4 (14 Oktober). Belum diuji manusia dan belum melalui program beta; Claude Code (simulasi agent) versi lama; Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Saya tidak punya data rapi, hanya perkiraan. Bisa?**
Bisa. Cukup jawab beberapa pertanyaan singkat dari AI (saldo sekarang, penjualan per minggu, pengeluaran rutin). Perkiraan kasar pun sudah sangat membantu, lalu perbarui tiap minggu.

**Apakah butuh Python?**
Sebaiknya ada (gratis, biasanya sudah ada di Mac/Linux; di Windows pasang dari python.org) agar angka dihitung pasti. Jika tidak ada, AI tetap menghitung manual langkah demi langkah dan memberi tahu Anda.

**Apakah data keuangan saya dikirim ke internet?**
Script berjalan di komputer Anda sendiri tanpa internet. Isi percakapan tetap dibaca oleh AI agent yang Anda pakai.

> **Catatan penting:** proyeksi dari angka dan jadwal yang Anda berikan, bukan ramalan, bukan jaminan, dan bukan nasihat keuangan profesional. Pos yang belum Anda sebut (mis. iuran BPJS atau pajak gaji PPh 21) ditulis "Belum termasuk", dan kewajiban yang jatuh setelah minggu ke-13 diperingatkan terpisah. Untuk keputusan besar (PHK, jual aset, restrukturisasi utang) diskusikan dengan akuntan atau konsultan.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
