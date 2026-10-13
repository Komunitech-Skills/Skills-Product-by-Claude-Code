# Aplikasi Stok Tanpa Langganan, Dijalankan AI

**Pengganti aplikasi stok berbayar: cukup chat ke AI agent, data stok tetap di laptop kamu sendiri.**

## Manfaat
- ✅ **Hemat biaya bulanan.** Perkiraan hemat **±Rp250 rb–800 rb per bulan** (±Rp3–9,6 jt per tahun) dibanding aplikasi kasir/stok atau omnichannel berbayar. Menurut riset harga publik kami (23 Sep 2026, bisa berubah): Majoo Rp249–999 rb, Moka Rp299–799 rb, Jubelio mulai Rp799 rb per bulan (minimal 6 bulan). Bayar sekali, tanpa langganan.
- ✅ **Stok terpotong dari file pesanan Shopee, TikTok Shop, dan Tokopedia.** Pesanan batal, retur, dan belum bayar diabaikan otomatis. Pesanan yang sama tidak akan terpotong dua kali. Pesanan yang batal setelah diimpor dikembalikan stoknya.
- ✅ **Daftar ambil barang (picking) per rak + urutan tempel resi.** Siap dicetak, jadi packing lebih cepat dan jarang salah kirim.
- ✅ **HPP rata-rata dihitung otomatis.** Harga kulakan naik-turun dan ongkir kulakan ikut masuk ke modal per barang. Nilai persediaan selalu terlihat.
- ✅ **Stock opname rapi.** Masukkan hasil hitung fisik, lalu selisih dan nilai rupiahnya keluar, lengkap dengan alasan. Laporan stok menipis, barang tidak laku, dan laporan harian bisa dikirim otomatis ke Telegram lewat OpenClaw.

## Cocok untuk siapa
- Seller Shopee/TikTok Shop/Tokopedia yang masih mencatat stok di Excel atau buku, atau sering kelebihan jual (oversell)
- Toko offline, grosir, dan reseller dengan puluhan sampai ribuan SKU
- Pemilik usaha yang tidak mau data stoknya disimpan di server pihak lain

## Contoh sebelum & sesudah
**Sebelum:** Setiap malam kamu mengunduh pesanan Shopee, mencocokkan satu per satu ke Excel stok, lalu menulis daftar barang yang harus diambil. Pesanan batal sering lupa dikembalikan. Stok di Excel tidak pernah sama dengan stok di rak, dan kamu tidak tahu modal yang tertahan di barang tidak laku.

**Sesudah (cukup ketik):** "Ini file pesanan Shopee hari ini, potong stoknya dan buatkan daftar ambil barang."
→ AI menunjukkan ringkasan: 4 pesanan baru, 1 batal dan 1 belum bayar diabaikan, stok yang akan berkurang per SKU. Setelah kamu balas "ya", stok tersimpan (backup otomatis dibuat), lalu keluar daftar ambil per rak dan urutan resi siap cetak.

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.1.6), skor 1-10 dari agen penguji independen: tanpa skill 6 → dengan skill 8,5.
- Tugas: catat stok kaos dan tote bag, lalu barang datang "kaos hitam M 50 pcs harga 34 ribu, ongkir 25 ribu". Tanpa skill, angka benar tetapi hanya jadi catatan teks di memori AI tanpa konfirmasi, dan untuk sinkron Shopee AI menawarkan menyimpan kredensial. Dengan skill: buku stok sungguhan di komputermu, stok 24 → 74 dan HPP rata-rata Rp 35.000 → Rp 34.662 (ongkir ikut masuk modal), tersimpan setelah kamu balas "ya". Permintaan menempel email dan password Seller Center ditolak.
- Jujur: hitungan HPP benar di kedua sisi. Bedanya sistem stok yang bisa dipakai ulang (backup, laporan stok menipis, potong stok dari file pesanan).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Catat stok toko saya" (kirim daftar barang dari Excel, atau ketik saja)
- "Barang datang: kaos hitam M 50 pcs, harga 34 ribu, ongkir 25 ribu"
- "Potong stok dari file pesanan TikTok ini, lalu buatkan picking list"
- "Mau stock opname: kaos hitam M ada 22, tote bag 41"
- "Barang apa saja yang hampir habis? Yang tidak laku 60 hari berapa modalnya?"
- "Kirim laporan stok ke Telegram saya setiap jam 9 malam" (OpenClaw)

Setiap perubahan data selalu ditunjukkan dulu dan baru disimpan setelah kamu setuju.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- Data tersimpan di satu file `KomunitechData/stok.db` di folder pengguna komputermu (lokasi bisa diganti). Backup otomatis ada di folder `backup-stok/` di sebelahnya. Salin folder ini ke flashdisk/Google Drive secara berkala.

## Instalasi singkat
Salin folder `buku-stok` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: perintah jadwalnya sudah dicocokkan dengan OpenClaw asli, tetapi pengiriman sungguhan ke bot Telegram belum kami uji untuk skill ini.

## FAQ
**Apakah stok di Shopee/TikTok ikut berubah otomatis?**
Tidak. Alat ini membaca file pesanan yang kamu unduh dari Seller Center. Alat ini tidak login ke marketplace dan tidak mengubah stok di sana. Stok di marketplace tetap kamu perbarui sendiri, dan laporan stok bisa diekspor ke Excel untuk membantu. Jika kamu butuh sinkron otomatis banyak toko secara real-time, layanan omnichannel berbayar tetap pilihan yang tepat.

**Kalau laptop rusak, datanya hilang?**
Semua data ada dalam satu file. Setiap impor, opname, dan pemulihan membuat backup bertanggal secara otomatis, dan kamu bisa minta "backup stok sekarang" kapan saja. Simpan salinan folder `KomunitechData` di tempat lain (flashdisk/cloud milikmu). Untuk memulihkan, cukup bilang "pulihkan stok dari backup kemarin".

**Apakah ini bisa menggantikan pembukuan/akuntansi?**
Tidak. Buku Stok fokus pada stok, HPP, dan nilai persediaan. Laba di laporan harian hanya perkiraan kasar (omzet dikurangi HPP, belum termasuk biaya admin, ongkir, dan iklan). Untuk laporan keuangan, pakai skill `laporan-keuangan-emkm`.

## Catatan revisi 1.1.6 (2026-10-01)
- Uji OpenClaw 2026-10-01: perubahan HPP baru muncul setelah barang masuk tersimpan. Kini konfirmasi pertama barang masuk selalu menampilkan "HPP Rp lama → Rp baru" (dari pratinjau script; saat mulai dari nol, dihitung dengan rumus HPP yang ditulis lalu dicocokkan dengan script sebelum disimpan).
