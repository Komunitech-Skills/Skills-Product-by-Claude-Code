# Ratusan Ulasan Jadi Laporan Satu Halaman

**Tempel ulasan atau kirim file ekspor, langsung tahu apa yang harus diperbaiki duluan dan apa yang bisa dijadikan konten.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Sebaran bintang, rata-rata, dan persen ulasan positif/negatif dihitung pasti, bukan dikira-kira
- ✅ Keluhan & pujian teratas lengkap dengan jumlah dan contoh kutipan asli, tanpa nama pembeli
- ✅ Paham bahasa ulasan orang Indonesia: "brg", "bgt", "gk sesuai", "mantul", "fast respon", "packing rapi"
- ✅ Daftar prioritas perbaikan yang jelas: masalah apa, buktinya apa, siapa mengerjakan apa, dan cara mengukur hasilnya
- ✅ Ide konten testimoni dari pujian pelanggan, siap dipakai tanpa melanggar privasi

## Cocok untuk siapa
- Seller Shopee, Tokopedia, TikTok Shop yang ulasannya sudah puluhan sampai ribuan
- Pemilik kafe, resto, salon, atau klinik yang ingin merangkum ulasan Google Maps
- Tim produk/marketing yang butuh bahan rapat evaluasi bulanan

## Contoh sebelum & sesudah
**Sebelum:** Membaca 300 ulasan satu per satu, lalu hanya ingat yang paling pedas. Rapat tim berakhir dengan "kayaknya banyak yang komplain soal pengiriman".

**Sesudah (cukup ketik):** "Analisis ulasan di file ulasan-september.csv, apa yang harus saya benahi dulu?"
→ Laporan berisi sebaran bintang, 5 keluhan teratas (mis. "kemasan bocor: 18 ulasan, rata-rata 1,8★" + kutipan), pujian teratas, tabel prioritas perbaikan dengan ukuran keberhasilan, dan 3–5 ide konten dari pujian.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Rangkum ulasan-ulasan ini, keluhan terbanyak apa?" (lalu tempel ulasannya)
- "Analisis file review-toko.csv, bandingkan per produk"
- "Dari ulasan bintang 5 ini, bikinin ide konten testimoni"

Tips: kalau menempel ulasan, tulis satu ulasan per baris dengan bintang di depan, misalnya `5 | barang bagus, packing rapi`.

## Instalasi singkat
Salin folder `analisis-ulasan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Apakah nama pembeli ikut muncul di laporan?**
Tidak. Kolom nama/username diabaikan, dan nomor HP, email, nomor pesanan, serta sapaan nama di dalam ulasan disamarkan otomatis.

**Ulasan saya banyak pakai bahasa gaul dan singkatan. Tetap terbaca?**
Ya. Sekitar 300 singkatan umum sudah dikenali. Kata khas usahamu bisa ditambahkan, dan ulasan yang belum dikenali tetap dibaca AI agent sebelum laporan dibuat.

**Perlu Python?**
Disarankan (gratis, biasanya sudah ada di Mac/Linux). Tanpa Python, AI agent tetap bisa menghitung manual dan akan memberi tahu bahwa hasilnya belum diverifikasi script.
