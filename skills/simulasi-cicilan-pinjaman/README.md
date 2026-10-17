# Tahu Harga Asli Cicilan Sebelum Tanda Tangan

**"Bunganya cuma 0,8% sebulan" — sebenarnya berapa? Hitung cicilan, total bunga, dan bunga efektif dalam satu kalimat.**

Diuji AI penguji independen di OpenClaw: 6,5 → 8,75 dari 10 (rata-rata 4 skenario; tanpa skill tidak menjelaskan bahwa bunga flat 0,8% sebulan setara ±17,25% per tahun, dengan skill hal itu terlihat, ±20,97% bila biaya admin ikut dihitung).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Cicilan per bulan, total bayar, total bunga, dan **total harga lewat kredit vs harga tunai** — langsung jelas
- ✅ **Bunga efektif setara per tahun** (bunga yang dihitung dari sisa utang) yang sudah memasukkan biaya admin, provisi (biaya pencairan), dan asuransi, sehingga penawaran bunga "flat" (dihitung dari pokok awal terus) dan efektif bisa dibandingkan dengan adil
- ✅ Jadwal angsuran (pokok, bunga, sisa utang) dan perbandingan flat vs anuitas (cicilan tetap dengan bunga dari sisa utang) dalam rupiah
- ✅ Cocok untuk motor, mobil, HP, KPR (kredit rumah, termasuk bunga tetap yang kemudian mengambang), leasing (kredit lewat perusahaan pembiayaan), koperasi, KTA (pinjaman tanpa agunan), paylater (bayar nanti), sampai pinjaman harian
- ✅ **Batas cicilan yang masih aman** dari gaji bersih Anda (patokan hati-hati maks. 30% gaji, asumsi yang bisa diubah, bukan aturan resmi semua lembaga), plus peringatan bila cicilan terasa berat; angkanya dihitung lewat skrip, bukan dikira

## Cocok untuk siapa
- Karyawan, ibu rumah tangga, dan pelaku usaha yang mau ambil kredit motor, HP, mobil, atau rumah
- Siapa saja yang bingung membandingkan dua penawaran kredit
- Staf penjualan dealer/koperasi yang ingin membuat simulasi dan brosur kredit yang transparan

## Contoh sebelum & sesudah
**Sebelum:** "Motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan flat, admin 1 juta." AI biasa menjawab cicilan Rp715.556 per bulan dan bilang "aman" — tanpa memberi tahu berapa mahal sebenarnya.

**Sesudah:** cicilan yang sama, ditambah fakta yang biasanya tidak terlihat. Cuplikan keluaran uji (v1.0.1, dipotong; `examples/01-motor-flat-admin-gaji.md`):

> **Simulasi cicilan motor — Rp25.000.000, 36 bulan**
> Cicilan: **Rp715.556/bulan** (36 kali, terakhir Rp715.540) · Total bayar Rp25.760.000 · Total bunga Rp5.760.000
> Bunga 0,8%/bulan flat = **efektif setara ±17,25%/tahun**; dengan biaya admin **±20,97%/tahun** …
>
> | Hal | Angka |
> |---|---|
> | Harga tunai / DP | Rp25.000.000 / Rp5.000.000 |
> | Pokok pinjaman | Rp20.000.000 |
> | Biaya di muka | Rp1.000.000 (admin) |
> | Total biaya pinjaman | Rp6.760.000 |
> | Total harga lewat kredit | Rp31.760.000 (lebih mahal Rp6.760.000 = 27,0% dari tunai) |

Hasil lengkapnya juga memuat perbandingan dengan anuitas dan batas cicilan aman dari gaji (patokan asumsi, bisa diubah).

## Cara pakai
Ketik permintaan biasa ke AI agent Anda, misalnya:
- "Motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan. Cicilannya berapa? Mahal nggak?"
- "Pinjam 30 juta, cicilannya 1,5 juta selama 24 bulan. Bunganya sebenarnya berapa persen?"
- "Gaji bersih 6 juta, sudah ada cicilan 500 ribu. Maksimal aman cicil berapa?"

## Instalasi singkat
Salin folder `simulasi-cicilan-pinjaman` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputer Anda.

**Hasil uji (angka nyata):** uji OpenClaw otomatis oleh agen AI, 6 Okt 2026 (v1.0.1; versi terkini 1.0.4), skor 1–10 penguji independen: rata-rata tanpa skill **6,5** → dengan skill **8,75** (lulus acuan kami). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Hasil di bot Telegram asli ada di bagian "Bukti uji di bot Telegram" di bawah.

**Status uji (jujur):** sudah diuji di OpenClaw (sebelum/sesudah, otomatis oleh agen AI, bukan oleh manusia) dan di bot Telegram asli. Cursor: pemasangan folder, skrip, dan tes regresi diuji 14 Okt 2026 dan berjalan, tetapi skill termuat otomatis di Cursor belum terbukti. Claude Code dan Codex belum diuji langsung (format skill-nya sama). Bukan nasihat keuangan atau rekomendasi lembaga pembiayaan.

## Bukti uji di bot Telegram

Uji terakhir: 12 Okt 2026, versi 1.0.1, di bot OpenClaw asli (grup uji internal Komunitech). Pesan yang sama dikirim dua kali, sekali tanpa skill dan sekali dengan skill: motor Rp25.000.000, DP 20%, 3 tahun, "bunga cuma 0,8% per bulan flat" ditambah admin Rp1.000.000, gaji Rp6.000.000 dengan cicilan HP Rp800.000; kredit HP Rp8.000.000 "flat 2% per bulan" selama 12 bulan; dan permintaan dibuatkan teks promo "bunga 0%" dari brosur dealer yang punya biaya admin dan asuransi wajib. Skor 1-10 dari penilai independen: tanpa skill **6** → dengan skill **8,5**, selisih **+2,5**: **lulus acuan kami** (dengan skill minimal 8 dan selisih minimal 1,5).

Bedanya yang terasa: hanya versi dengan skill yang menunjukkan bahwa bunga 0,8% flat per bulan setara sekitar 17,25% per tahun (sekitar 20,97% dengan biaya admin) dan bahwa motornya jadi Rp31.760.000 atau 27% lebih mahal dari tunai; versi ini juga langsung membuatkan brosur "bunga 0%" versi jujur berisi rincian biaya. Tanpa skill hanya menyebut cicilan Rp715.556, memberi contoh singkat brosur jujur lalu bertanya dulu, dan menaksir bunga kredit HP "kira-kira 44-45%" setahun, padahal hitungannya sekitar 41,7%.

Catatan jujur: tabel di jawaban ini tampil sebagai teks bergaris di Telegram, bukan tabel rapi. Perubahan sesudah uji ini (versi 1.0.2 sampai 1.0.4: aturan sumber angka, teks netral untuk bunga ilustrasi, dan dasar aturan batas biaya pinjaman daring; rumus cicilan tidak berubah) belum diuji ulang di bot Telegram. Uji lain: uji OpenClaw otomatis 6 Okt 2026, 6,5 → 8,75 (lihat di atas).

## FAQ
**Apakah angkanya sama persis dengan tabel dari bank/leasing?**
Rumusnya standar dan dibulatkan per rupiah, tetapi tiap lembaga bisa memakai pembulatan dan biaya yang berbeda. Pakai hasil ini untuk memahami dan membandingkan; angka final tetap dari tabel angsuran resmi.

**Apa bedanya bunga flat dan efektif?**
Flat menghitung bunga dari pinjaman awal sampai lunas; efektif menghitung dari sisa utang. Pada angka yang sama, flat jauh lebih mahal — misalnya flat 0,8% per bulan setara bunga efektif sekitar 17% per tahun.

**Bisa menyarankan bank atau aplikasi pinjaman yang paling murah?**
Skill ini tidak menyebut atau merekomendasikan merek bank maupun aplikasi pinjaman. Kirimkan angka dari penawaran yang Anda terima, dan AI akan membandingkannya dengan bunga efektif setara dan total biaya.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
