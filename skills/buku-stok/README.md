# Aplikasi Stok Tanpa Langganan, Dijalankan AI

**Pengganti aplikasi stok berbayar: cukup chat ke AI agent, data stok disimpan di laptop Anda sendiri.**

Diuji AI penguji independen di OpenClaw: 6 → 8,5 dari 10 (tanpa skill, stok hanya jadi catatan teks di memori AI dan AI menawarkan menyimpan login marketplace; dengan skill, buku stok sungguhan di komputer dengan cadangan, dan login ditolak). Hitungan modal per barang benar di kedua sisi.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Hemat biaya bulanan.** Perkiraan hemat **±Rp250 rb–800 rb per bulan** (±Rp3–9,6 jt per tahun) dibanding aplikasi kasir/stok atau omnichannel (pengelola banyak toko online sekaligus) berbayar. Menurut riset harga publik kami (23 Sep 2026, bisa berubah): Majoo Rp249–999 rb, Moka Rp299–799 rb, Jubelio mulai Rp799 rb per bulan (minimal 6 bulan). Bayar sekali, tanpa langganan.
- ✅ **Stok terpotong dari file pesanan Shopee, TikTok Shop, dan Tokopedia.** Pesanan batal, retur, dan belum bayar diabaikan otomatis. Pesanan yang sama dikenali, jadi tidak terpotong dua kali saat file diimpor ulang. Pesanan yang batal setelah diimpor dikembalikan stoknya.
- ✅ **Daftar ambil barang (picking) per rak + urutan tempel resi.** Siap dicetak, untuk membantu packing lebih cepat dan mengurangi salah kirim.
- ✅ **HPP (modal per barang) rata-rata dihitung otomatis.** Harga kulakan naik-turun dan ongkir kulakan ikut masuk ke modal per barang. Nilai persediaan bisa dilihat kapan saja.
- ✅ **Stock opname (hitung fisik stok) rapi.** Masukkan hasil hitung fisik, lalu selisih dan nilai rupiahnya keluar, lengkap dengan alasan. Laporan stok menipis, barang tidak laku, dan laporan harian bisa dijadwalkan ke Telegram lewat OpenClaw (yang sudah diuji terjadwal di bot Telegram uji pada 13 Okt 2026: laporan harian).

## Cocok untuk siapa
- Seller Shopee/TikTok Shop/Tokopedia yang masih mencatat stok di Excel atau buku, atau sering kelebihan jual (oversell)
- Toko offline, grosir, dan reseller dengan puluhan sampai ribuan SKU
- Pemilik usaha yang tidak mau data stoknya disimpan di server pihak lain

## Contoh sebelum & sesudah
**Sebelum:** Setiap malam Anda mengunduh pesanan Shopee, mencocokkan satu per satu ke Excel stok, lalu menulis daftar barang yang harus diambil. Pesanan batal sering lupa dikembalikan. Stok di Excel jarang sama dengan stok di rak, dan Anda tidak tahu modal yang tertahan di barang tidak laku.

**Sesudah (cukup ketik):** "Ini file pesanan Shopee hari ini (shopee-hari1.csv), potong stoknya dan buatkan daftar ambil barang ya"
→ AI menunjukkan ringkasan dulu (belum menyimpan). Setelah Anda balas "ya", stok tersimpan (backup otomatis dibuat), lalu keluar daftar ambil per rak dan urutan resi siap cetak. Cuplikan nyata dari uji simulasi agen penguji (keluaran asli skrip, data fiktif; SKU = kode barang):
```
Saya akan mencatat (belum disimpan):
…
Pesanan baru yang memotong stok: 4
Tidak dihitung: 1 batal, 1 pengembalian, 1 belum bayar

Stok yang akan berkurang (total 9 barang):
- KAOS-PT-M Kaos Putih M: -3 (stok 30 -> 27)
- KAOS-HT-M Kaos Hitam M: -2 (stok 24 -> 22)
…
Simpan? Balas "ya" untuk menyimpan.
```
Setelah "ya":
```
DAFTAR AMBIL BARANG — 2 pesanan, 6 barang
A. Ambil di rak (urut lokasi)
[Rak A1]  [ ] KAOS-HT-M  Kaos Polos Cotton 30s - Hitam M  x 2 pcs (1 pesanan)
[Rak A2]  [ ] KAOS-PT-M  Kaos Polos Cotton 30s - Putih M  x 3 pcs (1 pesanan)
…
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Catat stok toko saya" (kirim daftar barang dari Excel, atau ketik saja)
- "Barang datang: kaos hitam M 50 pcs, harga 34 ribu, ongkir 25 ribu"
- "Potong stok dari file pesanan TikTok ini, lalu buatkan daftar ambil barang (picking list)"
- "Mau stock opname: kaos hitam M ada 22, tote bag 41"
- "Barang apa saja yang hampir habis? Yang tidak laku 60 hari berapa modalnya?"
- "Kirim laporan stok ke Telegram saya setiap jam 9 malam" (OpenClaw; jadwal ke Telegram diuji 13 Okt 2026)

Perubahan data ditunjukkan dulu dan baru disimpan setelah Anda setuju.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- Data tersimpan di satu file `KomunitechData/stok.db` di folder pengguna komputer Anda (lokasi bisa diganti). Backup otomatis ada di folder `backup-stok/` di sebelahnya. Salin folder ini ke flashdisk/Google Drive secara berkala.

## Instalasi singkat
Salin folder `buku-stok` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## Hasil uji (jujur)

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.1.6), skor 1-10 dari agen penguji independen: tanpa skill 6 → dengan skill 8,5.
- Tugas: catat stok kaos dan tote bag, lalu barang datang "kaos hitam M 50 pcs harga 34 ribu, ongkir 25 ribu". Tanpa skill, angka benar tetapi hanya jadi catatan teks di memori AI tanpa konfirmasi, dan untuk sinkron Shopee AI menawarkan menyimpan kredensial (data login). Dengan skill: buku stok sungguhan di komputer Anda, stok 24 → 74 dan HPP rata-rata Rp 35.000 → Rp 34.662 (ongkir ikut masuk modal), tersimpan setelah Anda balas "ya". Permintaan menempel email dan password Seller Center ditolak.
- Jujur: hitungan HPP benar di kedua sisi. Bedanya sistem stok yang bisa dipakai ulang (backup, laporan stok menipis, potong stok dari file pesanan).

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. File pesanan marketplace yang dipakai uji adalah tiruan yang meniru format ekspor Seller Center; nama kolom TikTok Shop versi Indonesia belum dicocokkan dengan file ekspor asli (AI selalu menampilkan kolom yang dipakai supaya Anda cek dulu). Jadwal laporan harian ke Telegram: diuji di bot Telegram uji pada 13 Okt 2026 (jadwal sekali jalan 5 menit ke depan; pesan tiba tepat waktu dan angka omzet, HPP, serta nilai persediaan cocok dengan hitungan terpisah; lihat `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`).

## FAQ
**Apakah stok di Shopee/TikTok ikut berubah otomatis?**
Tidak. Alat ini membaca file pesanan yang Anda unduh dari Seller Center. Alat ini tidak login ke marketplace dan tidak mengubah stok di sana. Stok di marketplace tetap Anda perbarui sendiri, dan laporan stok bisa diekspor ke Excel untuk membantu. Jika Anda butuh sinkron otomatis banyak toko secara real-time, layanan omnichannel berbayar tetap pilihan yang tepat.

**Kalau laptop rusak, datanya hilang?**
Semua data ada dalam satu file. Setiap impor, opname, dan pemulihan membuat backup bertanggal secara otomatis, dan Anda bisa minta "backup stok sekarang" kapan saja. Simpan salinan folder `KomunitechData` di tempat lain (flashdisk/cloud milik Anda). Untuk memulihkan, cukup bilang "pulihkan stok dari backup kemarin".

**Apakah ini bisa menggantikan pembukuan/akuntansi?**
Tidak. Buku Stok fokus pada stok, HPP, dan nilai persediaan. Laba di laporan harian hanya perkiraan kasar (omzet dikurangi HPP, belum termasuk biaya admin, ongkir, dan iklan). Untuk laporan keuangan, pakai skill `laporan-keuangan-emkm` (menyusun laba rugi dan neraca sederhana dari catatan kas).

## Riwayat perubahan

Versi terkini: **1.1.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
