# Foto Nota Jadi Tabel Excel, Sudah Dicek

**Kirim foto nota, struk, atau faktur pajak. Dapat tabel rapi, hitungan yang sudah dicek, dan rekap pengeluaran.**

*Diuji AI penguji independen di OpenClaw: 6,0 → 9,0 dari 10 (pembedanya: PPN 12% penuh pada invoice jasa cetak ketahuan, padahal AI tanpa skill menyatakan "sesuai"; digit yang buram ditandai TIDAK TERBACA, bukan ditebak).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak perlu mengetik ulang nota satu per satu. Hasilnya tabel dan file CSV (tabel sederhana yang bisa dibuka di Excel) yang bisa langsung ditempel ke Excel atau Google Sheets
- ✅ Hitungan dicek otomatis: harga × jumlah, subtotal, PPN, total, sampai terbilang. Selisih hitungan ditandai
- ✅ Sesuai aturan PPN yang berlaku per 23 September 2026 (12% dihitung dari "DPP nilai lain", yaitu 11/12 dari harga sebelum PPN). Faktur yang menagih PPN terlalu besar ditandai sebagai peringatan
- ✅ Foto buram tidak ditebak. Kolom yang tidak terbaca ditandai jelas supaya Anda cek sendiri
- ✅ Banyak nota sekaligus jadi rekap pengeluaran per kategori, per toko, dan per bulan

## Cocok untuk siapa
- Pemilik usaha yang tiap bulan menumpuk nota belanja bahan dan operasional
- Admin keuangan yang harus menginput nota dan faktur pajak supplier ke spreadsheet
- Karyawan yang mengurus reimburse, dan freelancer yang mencatat pengeluaran

## Contoh sebelum & sesudah
**Sebelum:** Mengetik puluhan nota ke Excel satu per satu memakan waktu lama. Kesalahan PPN di faktur supplier sering lolos karena tidak ada yang menghitung ulang.

**Sesudah (cukup ketik):** "Mbak/Mas, tolong cek 2 faktur pajak dari PT Kemas Jaya ini. PPN-nya udah bener belum? Yang satu faktur bulan ini, satunya faktur lama Desember 2024 yang baru ketemu di laci. [2 PDF terlampir]"

*Cuplikan dari uji simulasi Claude Code (data fiktif), `examples/02-cek-faktur-pajak-ppn-12-penuh.md`; sisa temuan, rekap pengeluaran, dan CSV dipotong:*
```
**Hasil baca & cek 2 dokumen**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| F1 | 15-09-2026 | PT Kemas Jaya Fiktif | Faktur pajak | Rp 12.040.000 | ⚠️ Perlu dicek |
| F2 | 18-12-2024 | PT Kemas Jaya Fiktif | Faktur pajak | Rp 5.550.000 | ⚠️ Perlu dicek (hanya format NPWP) |

**Yang perlu Anda cek**
- **F1: PPN ditulis Rp 1.290.000, yaitu 12% × DPP penuh Rp 10.750.000.** Tarif 12% penuh hanya untuk barang mewah. Untuk kardus dan lakban (barang biasa), aturan sejak 2025 adalah 12% × DPP nilai lain (11/12 × DPP), jadi **PPN seharusnya Rp 1.182.500** (efektif 11%).
  - Kelebihan PPN: Rp 1.290.000 − Rp 1.182.500 = **Rp 107.500**. Jumlah yang seharusnya dibayar: Rp 10.750.000 + Rp 1.182.500 = **Rp 11.932.500** (di faktur tertulis Rp 12.040.000).
…
```

## Cara pakai
Setelah terpasang, kirim foto atau teks dokumen ke AI agent Anda, lalu ketik permintaan biasa, misalnya:
- "Ketik ulang nota-nota ini ke tabel Excel."
- "Cek faktur pajak dari supplier ini, PPN-nya sudah benar?"
- "Rekap pengeluaran bulan September dari foto-foto struk ini, per kategori."
- "Buatkan CSV pakai pemisah titik koma."

## Instalasi singkat
Salin folder `ekstrak-nota-faktur` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, di OpenClaw (uji otomatis agent, 1 Oktober 2026; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill. Invoice jasa cetak dengan "PPN 12% = Rp 180.000" atas harga sebelum PPN (DPP) Rp 1.500.000 dinyatakan sesuai oleh agent tanpa skill; dengan skill ditemukan PPN seharusnya Rp 165.000 (total Rp 1.665.000, kelebihan Rp 15.000). Pada faktur yang fotonya buram ("92?.000"), tanpa skill AI menyodorkan "tebakan paling masuk akal" untuk digit itu (dengan catatan agar dicocokkan); dengan skill digit tidak ditebak: ditandai TIDAK TERBACA, lalu dibandingkan dengan hasil hitung yang diberi label "dihitung, bukan dibaca".

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama). Pada uji OpenClaw, isi nota diketik di chat; membaca foto sungguhan belum diuji langsung.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "Kak tolong rekap nota belanja toko kue aku ke Excel ya, sekalian cek hitungannya bener ga: 1) Toko Bahan Kue Sari, 03/09/2026, tunai — Tepung terigu 10 kg x 13.500 = 135.000; Gula pasir 5 kg x 17.000 = 85.000; Mentega 2 kg x…". Tanpa skill skor **4,5** → dengan skill skor **7,5** (selisih +3, belum lulus acuan kami: skor dengan skill di bawah 8). Hanya DENGAN yang menangkap PPN invoice CV Cetak Kilat dihitung 12% penuh (untuk jasa biasa seharusnya Rp165.000, kelebihan tagih Rp15.000) dan menyarankan bertanya ke penjual sebelum bayar; TANPA menyatakan invoice "sudah cocok semua" dan berkas Excel-nya berisi rumus yang salah, tetapi DENGAN tidak melampirkan berkas Excel yang diminta. Catatan jujur: Hitungan dengan skill benar semua (termasuk PPN jasa 12% × 11/12 = Rp165.000, kelebihan tagih Rp15.000), tetapi di bot Telegram berkas Excel yang diminta tidak dilampirkan, hanya disebut tersimpan di folder kerja, sehingga skor dengan skill 7,5. Tanpa skill, invoice yang kelebihan PPN dinyatakan "cocok semua" dan berkas Excel-nya berisi rumus yang salah (satu selisih −37.500 bertanda cocok, total Rp2.024.000 yang seharusnya Rp2.061.500). Kekurangan dengan skill ada pada cara menyerahkan berkas di kanal chat, bukan pada hitungan; sedang diperbaiki dan akan diuji ulang. Uji internal (lokal, berkas di folder kerja wajar): 5,5–6 → 9.

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "Kak tolong rekap nota belanja toko kue aku ke Excel ya, sekalian cek hitungannya bener ga: 1) Toko Bahan Kue Sari, 03/09/2026, tunai — Tepung terigu 10 kg x 13.500 = 135.000; Gula pasir 5 kg x 17.000 = 85.000; Mentega 2 kg x…". Tanpa skill skor **4,5** → dengan skill skor **8,5** (selisih +4, lulus acuan kami). AI biasa menyatakan invoice CV Cetak Kilat "sudah cocok semua" dan file Excel-nya berisi rumus yang salah, sedangkan dengan skill bot menemukan PPN jasa cetak seharusnya Rp165.000 (bukan Rp180.000, kelebihan tagih Rp15.000) dan menyarankan bertanya ke penjual sebelum bayar, sambil langsung mengirim file rekapnya di chat. Salah angka yang ditemukan penilai: TANPA: menulis "Invoice CV Cetak Kilat sudah cocok semua" padahal PPN Rp180.000 = 12% × DPP penuh. Untuk jasa biasa (PMK 131/2024) PPN = 12% × 11/12 × Rp1.500.000 = Rp165.000, total Rp1.665.000, sehingga ada kelebihan tagih Rp15.000.; TANPA (isi berkas Rekap_Nota_Toko_Kue_Sep2026.xlsx): sel selisih Nota 2 berisi =I11−I12 dan merujuk sel kosong, jadi tampil −37.500 di samping "✓ COCOK". Di sheet Ringkasan, Total Hasil Cek Minimarket Berkah merujuk I11 (kosong) sehingga 0, dan total hasil cek menjadi Rp2.024.000 padahal seharusnya Rp2.061.500. Sheet faktur juga menyatakan "✓ SEMUA HITUNGAN COCOK" dengan PPN = DPP × 12%.. Catatan jujur: File rekap yang dikirim berformat CSV (bisa dibuka di Excel), bukan .xlsx. Isinya satu baris per nota tanpa rincian barang, dan karena memakai pemisah titik koma, kolomnya bisa menumpuk jadi satu di Excel berbahasa Inggris atau aplikasi di HP. Kategori pengeluaran ditebak dari isi nota dan sebaiknya disesuaikan dengan pembukuan sendiri.

## FAQ
**AI agent saya harus bisa membaca foto?**
Ya, untuk foto dibutuhkan AI agent yang bisa melihat gambar (kebanyakan agent sekarang bisa). Jika tidak, Anda bisa menempelkan teks nota atau hasil scan PDF.

**Kalau fotonya buram, apakah angkanya dikira-kira?**
Seharusnya tidak. Dalam uji, angka yang tidak terbaca ditulis "TIDAK TERBACA" dan tidak ikut dijumlah. Anda akan diberi tahu bagian mana yang perlu dicek atau difoto ulang.

**Apakah skill ini bisa memastikan faktur pajak asli?**
Belum bisa. Skill ini mengecek hitungan dan format nomor, lalu memberi peringatan bila ada yang janggal. Keaslian faktur tetap dicek lewat Coretax (sistem pajak online milik DJP) atau QR code resmi, dan untuk urusan pengkreditan PPN (mengurangi PPN yang harus disetor dengan PPN dari supplier) atau SPT (laporan pajak tahunan) silakan hubungi konsultan pajak atau Kring Pajak 1500200.

> **Catatan penting:** alat bantu mengetik ulang dan mengecek hitungan, bukan nasihat pajak. Dasar aturan PPN (berlaku per 23 September 2026): UU HPP dan PMK 131/2024, yaitu PPN 12% × DPP nilai lain 11/12 untuk barang/jasa non-mewah dan 12% dari harga penuh hanya untuk barang mewah. Pembulatan belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax. Format NPWP, NITKU (nomor identitas tempat kegiatan usaha), dan nomor faktur hanya diperiksa sebagai peringatan (belum diverifikasi dari dokumen resmi), dan skill tidak memutuskan PPN bisa dikreditkan. Kepastian: Kring Pajak 1500200 atau konsultan pajak.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
