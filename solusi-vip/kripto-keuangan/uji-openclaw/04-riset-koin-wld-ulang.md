# Uji ULANG 04 — Catatan riset koin Worldcoin (WLD)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member · home `sol2-kripto-keuangan` (6 skill paket; `atur-keuangan-pribadi` 1.0.5, `pantau-pasar-kripto` 1.0.5), **direset bersih sebelum skenario**. Pesan, jawaban lanjutan, dan data file identik dengan uji asal.

Pembanding: [04-riset-koin-wld.md](04-riset-koin-wld.md) (SESUDAH lama 8.5).

## Pesan member

> kak temen kantor ngajak beli koin Worldcoin (WLD), katanya bakal booming soalnya yg bikin bos OpenAI. sebelum ikut2an saya mau riset dulu. tolong bikinin catatan riset singkat soal koin ini ya, apa aja yg perlu saya cek, boleh dibeli di indonesia gak

## Tool yang dipakai

read, tool_search, web_fetch, tool_call, exec (daftar dari JSON hasil).

## Balasan utuh (3.069 karakter)

> Udah saya riset — fakta-fakta penting soal Worldcoin (WLD), **belum ada kesimpulan beli/jual** ya, itu tetap keputusan kamu sendiri:
>
> **1. Siapa di baliknya**
> Proyek "World" (dulu nama "Worldcoin"), didirikan 2019 oleh Sam Altman (chairman, juga CEO OpenAI), Max Novendstern, dan Alex Blania (CEO harian). Dikembangkan perusahaan swasta **Tools for Humanity** (AS & Jerman). Jadi benar, Sam Altman terlibat — tapi ini proyek terpisah dari OpenAI, bukan produk resmi OpenAI.
> Sumber: en.wikipedia.org/wiki/Worldcoin, world.org
>
> **2. Cara kerja**
> User scan mata/wajah lewat alat "Orb" buat verifikasi "proof of humanity" (World ID), lalu dapat WLD gratis sebagai insentif. WLD juga dipakai untuk governance.
>
> **3. Tokenomics**
> Total/max supply 10 miliar WLD. Yang sudah beredar sekarang ±3,96 miliar (~40%) — artinya ±60% suplai lain *belum* beredar, berpotensi jadi tekanan jual di masa depan kalau di-unlock. 10% token dijatahkan ke investor, 11,1% ke karyawan (saat peluncuran).
> Sumber: api.coingecko.com (data 1 Okt 2026), Wikipedia.
>
> **4. Harga & volatilitas (data CoinGecko, 1 Okt 2026 07:10 WIB)**
> Harga ±US$0,54 (≈Rp9.700-an), market cap ±US$2,14 miliar (ranking ~#53). ATH US$11,74 (Mar 2024) — sekarang sudah turun ~95% dari ATH itu. 1 tahun terakhir -56%, tapi 30 hari terakhir +46%, 24 jam terakhir +9% — volatilitas sangat tinggi.
>
> **5. Audit kontrak**
> Tidak ditemukan tautan laporan audit keamanan publik yang bisa saya verifikasi langsung di sesi ini — **perlu dicek sendiri** ke dokumentasi resmi/whitepaper.
>
> **6. Isu privasi & regulasi global**
> World ID (scan biometrik-nya, bukan token-nya) sempat diselidiki/dibatasi otoritas privasi di Prancis, UK, Jerman, Korsel, Kenya, Spanyol, Portugal; Hong Kong memutuskan ada pelanggaran; Filipina kena cease-and-desist (Okt 2025); Thailand diperintah hentikan (Nov 2025) — semua soal pengumpulan data biometrik, bukan larangan trading WLD.
>
> **7. Status di Indonesia**
> WLD/IDR tersedia di **Indodax** (PAKD berizin OJK): saat dicek, harga ±Rp9.700, volume 24 jam ±88 ribu WLD (±Rp853 juta) — likuiditas domestiknya relatif kecil. Komdigi (dulu Kominfo) sempat **menghentikan sementara operasi World ID/Orb** di Indonesia Mei 2025 karena keluhan publik — itu soal verifikasi biometriknya, bukan larangan jual-beli token WLD. Status WLD di daftar resmi DAKD bursa CFX/ICEX belum saya pastikan langsung ke situsnya — **perlu dicek sendiri** ke cfx.co.id/ICEX atau daftar PAKD di ojk.go.id.
>
> **Perhatian:** bukan ciri skema Ponzi klasik (nggak ada janji imbal hasil tetap), tapi fakta penting: harga sudah jatuh jauh dari ATH, dan ±60% suplai token belum beredar — ini fakta tokenomics, bukan sinyal baik/buruk, tapi layak dipikirkan.
>
> Konteks umum: trading kripto di Indonesia diawasi OJK (POJK 27/2024, diubah POJK 23/2025); transaksi di PAKD domestik berizin kena PPh final 0,21%.
>
> Mau rincian lengkap per bagian checklist (tim, likuiditas detail, dll), atau dibantu bikin kolom pantau harga WLD juga? Bisa saya kirim/simpan ke file.
>
> Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.
## Verifikasi independen penguji (14:16 WIB; CoinGecko `coins/worldcoin-wld` `last_updated` 07:14 UTC = 14:14 WIB; Indodax `wldidr`)

| Klaim balasan | Data penguji | |
|---|---|---|
| ±US$0,54, ±Rp9.700 | US$0,5381; CoinGecko Rp9.663; Indodax last Rp9.699 | ✅ (Rupiah dari Indodax, USD dari CoinGecko — tidak disebut) |
| Beredar ±3,96 M dari 10 M (~40%) | 3.956.398.868 / 10.000.000.000 | ✅ |
| Market cap ±US$2,14 M, rank ~#53 | US$2,129 M, #53 | ✅ |
| ATH US$11,74 (Mar 2024), −95% dari ATH | 11,74 (9 Mar 2024); 0,538/11,74 = −95,4% | ✅ |
| 1 th −56%, 30 hr +46%, 24 jam +9% | −56,7% / +45,7% / +8,9% (USD) | ✅ |
| Indodax vol ±88 rb WLD (±Rp853 jt) | 88.108 WLD / Rp852.952.462 | ✅ |
| **"data CoinGecko, 1 Okt 2026 07:10 WIB"** | data diambil ±14:10 WIB; 07:10 adalah jam **UTC** | ❌ jam salah 7 jam |
| **"10% token dijatahkan ke investor, 11,1% ke karyawan (saat peluncuran)"** | Angka ini dari Wikipedia (rencana awal 2021–22). Alokasi resmi saat peluncuran 2023: komunitas 75%, investor TFH 13,5%, tim awal 9,8%, cadangan TFH 1,7% ([world.org](https://world.org/blog/foundational-topics/the-circulating-supply-of-worldcoin-wld-an-explainer)) | ❌ usang, label "saat peluncuran" keliru |

## Cacat lama

| Cacat lama | Hilang? | Bukti |
|---|---|---|
| Terlalu panjang (±6.600 karakter) | **sebagian** | 3.069 karakter — turun >50%, masih di atas target 2.500; menawarkan rincian lengkap ("Mau rincian lengkap per bagian checklist…"). |
| Sumber berupa nama domain, bukan tautan | **tidak** | *"Sumber: en.wikipedia.org/wiki/Worldcoin, world.org"*, *"Sumber: api.coingecko.com"*; bagian privasi global, Komdigi, dan regulasi **tanpa sumber sama sekali** (uji lama masih menyebut Jakarta Globe/Antara). Tidak ada satu pun `https://`. |

## Regresi / temuan baru

1. **Jam data salah** (07:10 WIB, seharusnya ±14:10 WIB) — melanggar janji "sumber + waktu"; member bisa mengira data basi 7 jam. Di skenario 01 jam benar, jadi konversi zona waktu tidak konsisten.
2. **Alokasi token usang muncul lagi** (10% / 11,1%) — kesalahan yang di uji lama hanya ada di sisi TANPA skill; versi lama dengan skill jujur menulis "tidak saya verifikasi".
3. Positif: tetap tanpa kesimpulan beli/jual, jujur soal audit dan status DAKD yang belum diverifikasi, menyebut OJK (POJK 27/2024 jo. POJK 23/2025) dan PPh 0,21%, disclaimer ada, klarifikasi "bukan produk OpenAI" tepat.

## Nilai

| | Sesudah lama | Ulang 1.0.5 |
|---|---|---|
| Skor (1–10) | 8.5 | **7.5** |

Lebih ringkas (perbaikan nyata untuk chat), tetapi tautan sumber tetap tidak ada (malah sumber berkurang), jam data salah, dan satu fakta tokenomics usang kembali. Saran: di bagian riset (Langkah C) wajibkan blok "Sumber" berisi URL lengkap per klaim (minimal tim, tokenomics, harga, legal Indonesia); konversi jam dari `last_updated` ke WIB (UTC+7) secara eksplisit (atau lewat script); untuk alokasi token wajib sumber resmi proyek, bukan Wikipedia — bila tidak dibuka, tulis "belum diverifikasi".
