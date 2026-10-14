# Tahu Kapan Restok, Berapa, ke Pemasok Mana

**Kirim catatan penjualan Anda, dapatkan daftar belanja siap kirim: barang yang harus dipesan sekarang, jumlahnya, perkiraan biayanya, dan draf WA ke pemasok.**

> **Status uji (jujur):** versi 1.0.0, belum diuji penguji independen maupun di OpenClaw. Hasil uji akan ditambahkan di sini.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip hitung pendukung skill ini; tanpa Python skill tetap berjalan, AI menghitungnya langsung tetapi angkanya sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tidak kehabisan barang laris.** Tiap barang diberi "titik pesan ulang" (stok berapa saatnya pesan) yang memperhitungkan lama kiriman pemasok dan naik-turunnya penjualan. Barang yang bisa kosong sebelum kiriman datang langsung disorot.
- ✅ **Jumlah pesan yang pas, bukan kira-kira.** Dihitung dari penjualan nyata, tren 4 minggu terakhir, isi per dus, dan minimal order pemasok, lengkap dengan perkiraan biaya dalam Rupiah.
- ✅ **Tiga kelompok jelas:** PESAN SEKARANG, PESAN MINGGU DEPAN (dengan tanggalnya), dan AMAN.
- ✅ **Daftar belanja per pemasok + draf WA siap kirim.** Anda tinggal membaca, mengisi nama toko, lalu mengirim sendiri.
- ✅ **Modal yang tertahan terlihat.** Barang yang 60 hari tidak laku dan stok berlebih ditampilkan beserta nilai modalnya dan saran (paket bundling dengan barang laris, diskon bertahap, tanya tukar ke pemasok).

## Cocok untuk siapa
- Pemilik toko kelontong/warung, toko fashion, toko perlengkapan, apotek non-resep, dan kafe yang kulakan rutin.
- Seller Shopee, TikTok Shop, Tokopedia, dan toko online lain yang sering kehabisan barang laris atau menumpuk barang tidak laku.
- Admin pembelian yang menyiapkan daftar belanja mingguan ke beberapa pemasok.
- **Bukan untuk:** mencatat stok masuk/keluar dan stock opname (pakai skill Buku Stok; hasil ekspornya bisa langsung dipakai di sini), memilih pemasok termurah, atau membuat angka ramalan penjualan untuk pinjaman/investor tanpa data.

## Contoh sebelum & sesudah
Akan diisi dari hasil uji.

## Cara pakai
Ketik permintaan biasa ke AI agent Anda, lalu tempel tabel penjualan atau kirim file ekspornya:
- "Ini penjualan 3 bulan terakhir (file dari aplikasi kasir). Minggu ini saya harus kulakan apa saja dan berapa?"
- "Stok sekarang: kaos hitam M 35, tote 20. Konveksi kirim 5 hari, isi per dus 12. Kapan harus pesan?"
- "Barang apa yang numpuk? Berapa modal yang tertahan?"
- "Bulan depan Lebaran, biasanya penjualan naik 1,5 kali. Pesan berapa?"

**Data yang bisa dipakai:** tabel yang diketik di chat, file CSV atau Excel (.xlsx) dari aplikasi kasir, file pesanan yang Anda unduh sendiri dari pusat penjual marketplace, atau ekspor dari skill Buku Stok. Cukup tiga kolom: tanggal, nama barang (atau kode/SKU), jumlah terjual. Stok sekarang, lama kiriman pemasok, harga beli, isi per dus, dan minimal order membuat hasilnya lebih tajam; yang belum ada diisi nilai standar (kiriman 7 hari) atau ditandai `[isian]`, lalu ditanyakan maksimal tiga hal di akhir.

## Instalasi singkat
Salin folder `rencana-restok-barang` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`). Hitungan berjalan di komputer Anda dengan Python standar; tidak perlu internet, akun, atau API key.

## FAQ
**Berapa lama data penjualan yang dibutuhkan?**
Minimal 2 minggu; paling bagus 2–3 bulan. Barang yang datanya kurang dari 2 minggu (misalnya barang baru) ditandai "data belum cukup" dan jumlah pesannya tidak dikarang. Anda tetap melihat laju penjualan sementaranya.

**Bisakah AI mengambil data langsung dari akun Shopee/Tokopedia saya?**
Tidak. AI tidak masuk ke akun toko, tidak memakai kata sandi atau kode OTP, dan tidak mengambil data lewat scraping, karena berisiko akun dibatasi dan data login bocor. Unduh sendiri file pesanan dari menu ekspor di pusat penjual (nama menunya bisa berbeda), lalu kirim filenya.

**Seberapa tepat angkanya?**
Angka dihitung dengan rumus tetap dari penjualan Anda, bukan ditebak. Tetapi tetap perkiraan: promo, barang viral, atau libur panjang bisa membuat penjualan berbeda dari biasanya. Cocokkan dengan stok fisik dan kesanggupan pemasok sebelum memesan. Bila ada lonjakan sekali (misalnya pesanan borongan), AI akan menanyakannya dulu.

## Catatan
Alat bantu perencanaan stok, bukan nasihat keuangan dan bukan jaminan ketersediaan pemasok; keputusan belanja tetap di tangan Anda. Karya orisinal Komunitech. Nama marketplace dan aplikasi hanya disebut sebagai contoh sumber data dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan
Versi terkini: **1.0.0**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
