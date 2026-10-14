# Tahu Kapan Restok, Berapa, ke Pemasok Mana

**Kirim catatan penjualan Anda, dapatkan daftar belanja siap kirim: barang yang harus dipesan sekarang, jumlahnya, perkiraan biayanya, dan draf WA ke pemasok.**

Diuji AI penguji independen di OpenClaw: 6,1 → 8,7 dari 10. Pembedanya: tanpa skill, AI menebak jumlah pesan dengan rumus yang berubah-ubah dan membuang lonjakan penjualan diam-diam; dengan skill, satu file penjualan langsung jadi daftar belanja per pemasok (jumlah per dus, tanggal pesan, Rupiah, draf WA) dengan barang yang akan kosong sebelum kiriman datang di paling atas.

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
Cuplikan dari uji, data fiktif (toko perlengkapan bayi online, file penjualan 90 hari, dua pemasok; versi 1.0.1).

**Sebelum (AI tanpa skill):**
```
Ketemu 1 data aneh: Sabun Cair Bayi 200ml tanggal 20/9 tercatat laku 65 pcs, padahal rata-rata
harian cuma ~5. Ini saya anggap salah input dan saya koreksi ke angka wajar (4) biar perhitungan nggak ngaco.
```

**Sesudah (dengan skill):**
```
Dari 12 barang: 4 dipesan sekarang (±Rp10.879.000), 3 minggu depan (±Rp3.351.000), 3 aman,
1 barang mati (modal nganggur Rp2.775.000), dan 3 barang berisiko kosong sebelum kiriman tiba.
⚠️ AKAN KOSONG SEBELUM BARANG DATANG — urus duluan
- Bedak Bayi 150g: stok 9, habis ±2 hari, CV Grosir Bunda kirim 3 hari → bisa kosong ±1 hari. Pesan hari ini.
- Botol Susu Anti Kolik 250ml: stok 38, habis ±8 hari, PT Ceria 10 hari → bisa kosong ±2 hari. Pesan hari ini.
| Barang | Stok | Laku/hari | Habis ± | Pesan | Nilai |
| Tisu Basah Bayi 50 lembar | 110 | 9,2 (stabil) | 11 hari (25 Okt) | 132 pcs = 11 dus | Rp1.122.000 |
Catatan Sabun Cair: ada lonjakan 20 Sep (terjual 65, biasanya ±4). Hitungan di atas termasuk lonjakan itu —
tanpa lonjakan tren-nya stabil dan barang ini sebetulnya AMAN, bukan minggu depan. Kalau 20 Sep itu
borongan/promo sekali, saya bisa hitung ulang tanpa lonjakan tersebut.
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

**Hasil uji (angka nyata):** uji OpenClaw otomatis oleh agen penguji independen, 14 Okt 2026, skor 1–10 (tanpa skill → dengan skill versi 1.0.1):
- Toko perlengkapan bayi online, file penjualan 90 hari (777 baris, tanggal campur format), stok 12 barang, dua pemasok: 7 → 9; dengan tampilan khusus chat Telegram: 6 → 8,5.
- Warung sembako, penjualan per minggu selama 8 minggu diketik di chat, stok dua barang belum dihitung: 6,5 → 9.
- Info minim ("stok tepung tinggal 20, sehari laku 3-5, kapan pesan?"): 7 → 8 (diuji pada versi 1.0.0).
- Permintaan membuat angka proyeksi karangan untuk pinjaman, sekaligus pertanyaan restok yang sah: 4 → 9 (diuji pada versi 1.0.0).
- Rata-rata **6,1 → 8,7**. File 777 baris menjadi rencana Rp10.879.000 untuk dipesan sekarang dan Rp3.351.000 minggu depan dalam sekitar 100 detik, dengan 3 barang ditandai akan kosong ±1–4 hari sebelum pesanan datang. Penguji menghitung ulang 182 angka secara terpisah: 180 cocok (dua sisanya berasal dari satu selisih pembulatan, diperbaiki di versi 1.0.2). Pada tugas yang sama, dua skill publik lain mendapat nilai 5 dan 6,5; salah satunya menyarankan belanja Rp44,3 juta sekaligus.

**Status uji (jujur):** diuji otomatis oleh agen AI di OpenClaw (termasuk tampilan khusus chat Telegram tanpa mengirim pesan). Versi 1.0.0 mendapat rata-rata 8,3; versi 1.0.1 mendapat 8,7 dari uji ulang terbatas (hanya dua skenario pertama diulang; dua skenario lain memakai nilai versi 1.0.0). Dua ketidaktepatan kecil dari uji ulang, yaitu hari habis satu barang tertulis ±139 padahal tepat 140 dan kalimat "dibatasi 2×" untuk barang yang tidak kena batas, diperbaiki di versi 1.0.2 tanpa uji ulang OpenClaw (baru tes otomatis skrip). Versi 1.0.2 sudah dicoba sekali di bot Telegram asli untuk kasus warung sembako (lihat bagian di bawah); belum diuji manusia dan belum melalui program beta. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Catatan jujur: AI tanpa skill pun sudah cukup pandai di soal sehari-hari (menyatukan nama, menghitung Rupiah); pembeda terbesar ada di permintaan angka karangan (4 → 9), data mingguan dengan tren naik (6,5 → 9), dan penanda barang yang akan kosong sebelum kiriman datang.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 14 Okt 2026) dengan pesan yang sama: penjualan mingguan warung sembako selama 8 minggu diketik di chat, stok tiga barang, grosir antar 2-3 hari.

- **Uji pertama (versi 1.0.2):** tanpa skill skor **7** → dengan skill skor **8** (selisih 1,0: belum memenuhi acuan kami, yaitu selisih minimal 1,5). Dengan skill, jumlah pesan keluar pasti dan semuanya cocok dengan hitung ulang terpisah: beras 47 karung (habis ±2 hari, 16 Okt, berisiko kosong ±1 hari sebelum kiriman datang), minyak goreng 82 botol (lakunya naik 27%), dan gula 75 kg dipesan sekitar 15 Okt. Tanpa skill, AI juga sudah menghitung sisa hari stok dengan benar dan menandai beras sebagai darurat, tetapi jumlah pesannya hanya kisaran (±38-40 karung, ±65-70 botol, ±50 kg). Kekurangannya: draf WA ke grosir tidak muncul, dan judul "pesan minggu depan" untuk gula sebenarnya berarti pesan besok.
- **Uji ulang setelah perbaikan (versi 1.0.3):** skor **4**, BELUM lulus. Perbaikan tampilannya berhasil: draf WA siap kirim muncul, dan setiap barang diberi baris hitungan ("stok target − stok = pesan"). Namun kali ini AI membaca angka mingguan sebagai penjualan satu hari, sehingga jumlah pesan terlalu besar: beras 75 karung (seharusnya 47), minyak 115 botol (seharusnya 82), gula 105 kg (seharusnya 75). Gula juga ditulis "turun 20%" padahal stabil. Hitungan dengan data yang dibaca benar di versi 1.0.3 tetap menghasilkan 47 / 82 / 75.

Catatan jujur: kesalahan membaca data mingguan ini sudah dicatat untuk diperbaiki. Sampai perbaikannya diuji ulang, bila Anda memberi total per minggu, sebutkan "per minggu" dan pastikan jawabannya menulis laku per hari sekitar total seminggu dibagi 7 (contoh: beras 22 karung/minggu ≈ 3,1 per hari). Bila angkanya jauh berbeda, minta dihitung ulang.

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
Versi terkini: 1.0.3. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
