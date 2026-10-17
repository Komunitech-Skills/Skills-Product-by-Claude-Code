# Ratusan Ulasan Jadi Laporan Satu Halaman

**Tempel ulasan atau kirim file ekspor (file ulasan yang diunduh dari marketplace), langsung tahu apa yang harus diperbaiki duluan dan apa yang bisa dijadikan konten.**

Diuji AI penguji independen di OpenClaw: 7,0 → 8,25 dari 10 (persentase keluhan dan pujian serta prioritas perbaikan terukur, username pembeli disamarkan; tanpa skill wawasannya benar tetapi tanpa sebaran dan username ikut bocor).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Sebaran bintang, rata-rata, dan persen ulasan positif/negatif dihitung dengan skrip (program hitung kecil), bukan dikira-kira
- ✅ Keluhan & pujian teratas lengkap dengan jumlah dan contoh kutipan asli, tanpa nama pembeli
- ✅ Paham bahasa ulasan orang Indonesia: "brg", "bgt", "gk sesuai", "mantul", "fast respon", "packing rapi"
- ✅ Daftar prioritas perbaikan yang jelas: masalah apa, buktinya apa, siapa mengerjakan apa, dan cara mengukur hasilnya
- ✅ Ide konten testimoni dari pujian pelanggan, dengan nama pembeli disamarkan (periksa lagi sebelum diposting)

## Cocok untuk siapa
- Seller Shopee, Tokopedia, TikTok Shop yang ulasannya sudah puluhan sampai ribuan
- Pemilik kafe, resto, salon, atau klinik yang ingin merangkum ulasan Google Maps
- Tim produk/marketing yang butuh bahan rapat evaluasi bulanan

## Contoh sebelum & sesudah
**Sebelum:** Membaca 300 ulasan satu per satu, lalu hanya ingat yang paling pedas. Rapat tim berakhir dengan "kayaknya banyak yang komplain soal pengiriman".

**Sesudah (cukup ketik):** "Ini ulasan toko aku 3 bulan terakhir dari Shopee, filenya ulasan.csv. Keluhan paling banyak apa sih? Terus apa yang harus aku benahi duluan?" (CSV = file tabel yang bisa dibuka di Excel/Google Sheets)

Cuplikan laporan (data fiktif: 160 ulasan; hasil uji simulasi agent di Claude Code, bukan dari uji OpenClaw; dipotong dari `examples/01-toko-kaos-160-ulasan-csv.md`):
> ## Ringkasan cepat
> - Rata-rata **3,88★**. 67,5% ulasan positif (4–5★) dan **18,8% negatif (1–2★)**. Rata-rata turun tiap bulan: Juli 4,07 → Agustus 3,84 → September 3,71.
> - Keluhan paling merusak bintang adalah **pengiriman atau proses kirim lambat**: 15 ulasan (9,4%), rata-rata 2,07★. Dari 15 itu, 7 menyebut "pesanan diproses lama, 5 hari baru dikirim", jadi penyebabnya ada di **proses toko**, bukan hanya kurir.
> - Pujian terbanyak: **ukuran pas** (33 ulasan), **sesuai foto** (31) dan **pengiriman cepat** (30). Ini bahan konten testimoni.
> - **Tindakan paling penting minggu ini:** tetapkan jam potong kirim (pesanan yang masuk sebelum 15.00 dikirim hari itu juga) dan tulis estimasi proses di deskripsi produk dan balasan chat otomatis.
>
> …
>
> | Prioritas | Masalah | Bukti | Tindakan konkret | Ukuran keberhasilan |
> |---|---|---|---|---|
> | **Segera (minggu ini)** | Pesanan lama diproses | 15 ulasan, rata-rata 2,07★; 7 menyebut "5 hari baru dikirim" | Pemilik menetapkan jam potong 15.00. Admin memasang estimasi proses di deskripsi dan balasan otomatis. Pesanan dicek setiap pagi dan sore | Waktu proses ≤ 1 hari kerja; keluhan pengiriman < 5% ulasan bulan depan |

Laporan lengkapnya juga memuat sebaran bintang, keluhan dan pujian teratas dengan kutipan tanpa nama, serta ide konten dari pujian.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Rangkum ulasan-ulasan ini, keluhan terbanyak apa?" (lalu tempel ulasannya)
- "Analisis file review-toko.csv (file tabel dari Excel/Google Sheets), bandingkan per produk"
- "Dari ulasan bintang 5 ini, bikinin ide konten testimoni"

Tips: kalau menempel ulasan, tulis satu ulasan per baris dengan bintang di depan, misalnya `5 | barang bagus, packing rapi`.

## Instalasi singkat
Salin folder `analisis-ulasan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (folder kerja bersih terpisah untuk tiap skenario), 1 Okt 2026 (v1.0.3), skor 1–10 penguji independen, rata-rata 2 skenario: tanpa skill **7,0** → dengan skill **8,25** (LULUS). Pada skenario utama (40 ulasan Shopee) skornya 6 → 8,5; pada skenario permintaan ulasan palsu skill tidak termuat dan hasilnya setara tanpa skill (8 vs 8). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dengan skill: persentase keluhan/pujian, prioritas terukur, username disamarkan; tanpa skill: wawasan benar tapi tanpa sebaran dan membocorkan username.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung. Semua uji memakai file ulasan contoh (data fiktif), belum dengan ekspor asli dari tiap marketplace. Pada uji OpenClaw v1.0.3, ulasan bernada sindiran (mis. "mantap, 2 minggu baru sampai") sempat tidak terhitung sebagai keluhan pengiriman, jadi tetap baca ringkasan keluhan dengan teliti.

## FAQ
**Apakah nama pembeli ikut muncul di laporan?**
Seharusnya tidak. Kolom nama/username diabaikan, dan nomor HP, email, nomor pesanan, serta sapaan nama di dalam ulasan disamarkan otomatis. Tetap periksa laporan sebelum dibagikan atau diposting.

**Ulasan saya banyak pakai bahasa gaul dan singkatan. Tetap terbaca?**
Umumnya terbaca. Sekitar 300 singkatan umum sudah dikenali. Kata khas usaha Anda bisa ditambahkan, dan ulasan yang belum dikenali tetap dibaca AI agent sebelum laporan dibuat.

**Perlu Python?**
Disarankan (gratis, biasanya sudah ada di Mac/Linux). Tanpa Python, AI agent tetap bisa menghitung manual dan akan memberi tahu bahwa hasilnya belum diverifikasi script.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
