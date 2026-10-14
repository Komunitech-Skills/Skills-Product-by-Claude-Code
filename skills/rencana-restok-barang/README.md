# Tahu Kapan Restok, Berapa, ke Pemasok Mana

**Kirim catatan penjualan Anda, dapatkan daftar belanja siap kirim: barang yang harus dipesan sekarang, jumlahnya, perkiraan biayanya, dan draf WA ke pemasok.**

Diuji AI penguji independen di OpenClaw: 6,1 → 8,3 dari 10. Pembedanya: tanpa skill, AI menebak jumlah pesan dengan rumus yang berubah-ubah dan membuang lonjakan penjualan diam-diam; dengan skill, satu file penjualan langsung jadi daftar belanja per pemasok berisi jumlah per dus, tanggal pesan, Rupiah, dan draf WA siap kirim.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip hitung pendukung skill ini; tanpa Python skill tetap berjalan, AI menghitungnya langsung dan menunjukkan baris hitungannya, tetapi angkanya sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu barang mana yang akan kosong sebelum kiriman datang.** Bila stok habis lebih cepat daripada waktu kirim pemasok, barang itu ditaruh paling atas lengkap dengan perkiraan berapa hari kosong dan pilihan tindakannya.
- ✅ **Jumlah pesan dihitung, bukan dikira.** Dari penjualan nyata, tren 4 minggu terakhir, lama kiriman pemasok, isi per dus, dan minimal order, lengkap dengan perkiraan biaya dalam Rupiah.
- ✅ **Tiga kelompok jelas:** PESAN SEKARANG, PESAN MINGGU DEPAN (dengan tanggalnya), dan AMAN.
- ✅ **Daftar belanja per pemasok + draf WA siap kirim.** Anda tinggal membaca, mengisi nama toko, lalu mengirim sendiri.
- ✅ **Data berantakan tetap terbaca dan lonjakan tidak dibuang diam-diam.** Tanggal campur format dan nama barang yang beda tulis disamakan; penjualan sehari yang melonjak (promo atau borongan) ditandai lalu ditanyakan, dengan hasil "dengan" dan "tanpa" lonjakan. Modal yang tertahan di barang tidak laku dan stok berlebih ditampilkan dalam Rupiah.

## Cocok untuk siapa
- Pemilik toko kelontong/warung, toko fashion, toko perlengkapan bayi, dan kafe yang kulakan rutin.
- Seller Shopee, TikTok Shop, Tokopedia, dan toko online lain yang sering kehabisan barang laris atau menumpuk barang tidak laku.
- Admin pembelian yang menyiapkan daftar belanja mingguan ke beberapa pemasok.
- **Bukan untuk:** mencatat stok masuk/keluar dan stock opname (pakai skill Buku Stok; hasil ekspornya bisa langsung dipakai di sini), memilih pemasok termurah, atau membuat angka ramalan penjualan untuk pinjaman/investor tanpa data.

## Contoh sebelum & sesudah
Cuplikan dari uji, data fiktif (toko perlengkapan bayi online, file penjualan 90 hari, dua pemasok; versi 1.0.0 yang diuji).

**Sebelum (AI tanpa skill):**
```
Ketemu 1 data aneh: Sabun Cair Bayi 200ml tanggal 20/9 tercatat laku 65 pcs, padahal rata-rata
harian cuma ~5. Ini saya anggap salah input dan saya koreksi ke angka wajar (4) biar perhitungan nggak ngaco.
```

**Sesudah (dengan skill):**
```
Dari 12 barang: 4 pesan sekarang (±Rp9.799.000), 3 pesan minggu depan (±Rp3.351.000), 3 aman,
1 barang mati (modal tertahan Rp2.775.000), dan 1 barang datanya belum cukup.
| Barang | Stok | Laku/hari | Habis ± | Pesan | Nilai |
| Bedak Bayi 150g | 9 | 3,11 | 2 hari (16 Okt) | 49 pcs | Rp539.000 |
| Tisu Basah Bayi 50 lembar | 110 | 9,2 | 11 hari (25 Okt) | 132 pcs = 11 dus × 12 | Rp1.122.000 |
Catatan: Sabun Cair ada lonjakan 1 hari (20 Sep, terjual 65 vs biasanya ±4) — kemungkinan borongan
sekali. Dihitung tetap masuk, jadi angka ini agak konservatif ke atas. Beri tahu saya kalau itu memang
borongan, bisa dihitung ulang tanpa lonjakan itu.
Halo CV Grosir Bunda, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut: …
```

## Cara pakai
Ketik permintaan biasa ke AI agent Anda, lalu tempel tabel penjualan atau kirim file ekspornya:
- "Ini penjualan 3 bulan terakhir (file dari aplikasi kasir). Minggu ini saya harus kulakan apa saja dan berapa?"
- "Stok sekarang: kaos hitam M 35, tote 20. Konveksi kirim 5 hari, isi per dus 12. Kapan harus pesan?"
- "Barang apa yang numpuk? Berapa modal yang tertahan?"
- "Bulan depan Lebaran, biasanya penjualan naik 1,5 kali. Pesan berapa?"

**Data yang bisa dipakai:** tabel yang diketik di chat (per hari, per minggu, atau per bulan), file CSV atau Excel (.xlsx) dari aplikasi kasir, file pesanan yang Anda unduh sendiri dari pusat penjual marketplace, atau ekspor dari skill Buku Stok. Cukup tiga hal: tanggal, nama barang (atau kode/SKU), jumlah terjual. Stok sekarang, lama kiriman pemasok, harga beli, isi per dus, dan minimal order membuat hasilnya lebih tajam; yang belum ada diisi nilai standar (kiriman 7 hari) atau ditandai `[isian]`, lalu ditanyakan maksimal tiga hal di akhir.

## Instalasi singkat
Salin folder `rencana-restok-barang` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`). Hitungan berjalan di komputer Anda dengan Python standar; tidak perlu internet, akun, atau API key.

**Hasil uji (angka nyata):** uji OpenClaw otomatis oleh agen penguji independen, 14 Okt 2026, versi yang diuji 1.0.0, skor 1–10 (tanpa skill → dengan skill):
- Toko perlengkapan bayi online, file penjualan 90 hari (777 baris, tanggal campur format), stok 12 barang, dua pemasok: 7 → 8,5; dengan tampilan khusus chat Telegram: 6 → 8,5.
- Warung sembako, penjualan per minggu selama 8 minggu diketik di chat, stok dua barang belum dihitung: 6,5 → 7,5.
- Info minim ("stok tepung tinggal 20, sehari laku 3-5, kapan pesan?"): 7 → 8.
- Permintaan membuat angka proyeksi karangan untuk pinjaman, sekaligus pertanyaan restok yang sah: 4 → 9.
- Rata-rata **6,1 → 8,3**. File 777 baris menjadi rencana Rp9.799.000 untuk dipesan sekarang dan Rp3.351.000 minggu depan dalam sekitar 100 detik; 125 angka per barang dihitung ulang terpisah oleh penguji dan tidak ada yang berbeda. Pada tugas yang sama, dua skill publik lain mendapat nilai 5 dan 6,5; salah satunya menyarankan belanja Rp44,3 juta sekaligus.

**Status uji (jujur):** sejauh ini diuji otomatis oleh agen AI di OpenClaw (termasuk tampilan khusus chat Telegram tanpa mengirim pesan). Belum diuji di bot Telegram asli, belum diuji manusia, dan belum melalui program beta. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Catatan jujur dari uji: AI tanpa skill pun sudah cukup pandai di soal sehari-hari (menyatukan nama, menghitung Rupiah); pembeda terbesar ada di permintaan angka karangan (4 → 9) dan di tampilan Telegram. Lima temuan penguji diperbaiki di versi 1.0.1 (barang yang akan kosong sebelum kiriman datang kini disorot, tren dibandingkan dengan minggu-minggu sebelumnya, nama beda tulis disamakan, lonjakan dibandingkan, hitungan manual ditampilkan); perbaikan ini baru diuji dengan tes otomatis skrip, belum diuji ulang di OpenClaw. Karena aturan tren berubah, jumlah pesan barang yang sedang naik bisa lebih besar daripada angka uji di atas.

## FAQ
**Berapa lama data penjualan yang dibutuhkan?**
Minimal 2 minggu, dan paling bagus 2–3 bulan. Barang yang datanya kurang dari 2 minggu (misalnya barang baru) ditandai "data belum cukup" dan jumlah pesannya tidak dikarang. Anda tetap melihat laju penjualan sementaranya, dan bila barang itu akan habis sebelum kiriman datang, peringatannya ditaruh paling atas.

**Bisakah AI mengambil data langsung dari akun Shopee atau Tokopedia saya?**
Tidak. AI tidak masuk ke akun toko, tidak memakai kata sandi atau kode OTP, dan tidak mengambil data lewat scraping, karena berisiko akun dibatasi dan data login bocor. Unduh sendiri file pesanan dari menu ekspor di pusat penjual (nama menunya bisa berbeda), lalu kirim filenya.

**Seberapa tepat angkanya?**
Angka dihitung dengan rumus tetap dari penjualan Anda, bukan ditebak, tetapi tetap berupa perkiraan. Promo, barang viral, atau libur panjang bisa membuat penjualan berbeda dari biasanya. Cocokkan dengan stok fisik dan kesanggupan pemasok sebelum memesan. Bila ada lonjakan sehari, AI menunjukkan hasil dengan dan tanpa lonjakan itu lalu menanyakannya kepada Anda.

## Catatan
Alat bantu perencanaan stok, bukan nasihat keuangan dan bukan jaminan ketersediaan pemasok; keputusan belanja tetap di tangan Anda. Karya orisinal Komunitech. Nama marketplace dan aplikasi hanya disebut sebagai contoh sumber data dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan
Versi terkini: 1.0.1. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
