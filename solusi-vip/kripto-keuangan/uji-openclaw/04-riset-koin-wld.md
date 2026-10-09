# Uji OpenClaw 04 — Catatan riset koin (Worldcoin/WLD) sebelum ikut ajakan teman

Tanggal: 2026-10-01 (Asia/Jakarta) · Agent: OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member. SEBELUM = home `kosong-kripto-keuangan` (tanpa skill), SESUDAH = home `sol-kripto-keuangan` (6 skill paket). Kedua home dibuat ulang bersih sebelum skenario ini.

## Pesan member (identik di kedua sisi)

> kak temen kantor ngajak beli koin Worldcoin (WLD), katanya bakal booming soalnya yg bikin bos OpenAI. sebelum ikut2an saya mau riset dulu. tolong bikinin catatan riset singkat soal koin ini ya, apa aja yg perlu saya cek, boleh dibeli di indonesia gak

## Tool yang dipakai

- SEBELUM: `web_fetch` Wikipedia, world.org, Indodax, berita (±16 panggilan tool).
- SESUDAH: membaca `pantau-pasar-kripto/SKILL.md`, `references/checklist-riset.md`, `references/regulasi.md`; `web_fetch` Wikipedia/world.org/whitepaper, API CoinGecko & ticker Indodax, mencoba cfx.co.id & ojk.go.id (gagal diakses otomatis, dan **dilaporkan jujur**).

## SEBELUM (tanpa skill) — balasan utuh

> Oke, ini hasil riset cepatnya. Saya korek dari Wikipedia, web resmi World, Indodax, dan berita CNBC Indonesia/Bing News hari ini.
>
> ## 📋 Apa itu Worldcoin (WLD)
>
> - Proyek dari **Tools for Humanity**, didirikan 2019 oleh **Sam Altman** (CEO OpenAI, di sini jadi *chairman*), Max Novendstern, dan Alex Blania (CEO). Ini proyek terpisah dari OpenAI — bukan "produk OpenAI", cuma Altman jadi salah satu pendiri & bosnya.
> - Produk utamanya: alat **"Orb"** (scan bola mata/iris) buat bikin **World ID** — identitas digital buat membuktikan "saya manusia asli, bukan bot AI". Token **WLD** adalah "hadiah" buat orang yang scan mata + mata uang di ekosistemnya (jalan di jaringan Layer-2 Ethereum, namanya World Chain).
> - Rebranding dari "Worldcoin" jadi "World Network" di Oktober 2024.
> - September 2025: ~33 juta pengguna World App, 15 juta yang sudah terverifikasi (scan mata).
>
> ## ⚠️ Yang bikin was-was (sudah ada track record)
>
> **Masalah privasi/regulasi di banyak negara** — ini bukan isu kecil, tapi berulang di banyak yurisdiksi:
> - Diselidiki/dihentikan sementara: Prancis, Inggris, Jerman (Bavaria), Korea Selatan, Spanyol, Portugal, Hong Kong, Kenya, India, Brasil
> - **Oktober 2025**: Filipina keluarkan *cease and desist* resmi — dianggap melanggar UU Privasi Data, konsennya dianggap tidak sah karena "dibayar" buat scan biometrik
> - **November 2025**: Thailand perintahkan hentikan scan iris & hapus data 1,2 juta orang
> - Pola yang terlihat: pemerintah berulang kali mempermasalahkan cara mereka kumpulkan data biometrik & insentif uang buat scan mata
>
> **Tokenomics — rawan tekanan jual:**
> - Dari total suplai, porsi besar dipegang investor & tim (10% buat investor awal, 11,1% buat karyawan/kontributor)
> - Berita terbaru (dalam beberapa bulan ke belakang): token unlock besar (100 juta+ WLD) bikin harga turun karena pasokan membanjir
> - Harga sangat fluktuatif: sempat anjlok dari puncak 2024, rebound ke sekitar $0,35–0,50 belakangan ini — volatil banget, bukan aset yang "pasti naik"
>
> ## 🇮🇩 Soal legal di Indonesia — ini bagian penting, dua hal beda
>
> 1. **World ID / aplikasi Orb (layanan scan mata)**: **Mei 2025, Kementerian Komdigi (dulu Kominfo) SUDAH membekukan/suspend operasinya** di Indonesia karena laporan masyarakat soal aktivitas mencurigakan + data iris wajib dihapus. ❌ Layanan "scan mata dapat duit" ini statusnya bermasalah di RI.
> 2. **Token WLD sebagai aset kripto untuk diperdagangkan**: beda urusan. Saya cek, **WLD/IDR memang ada sebagai pair trading di Indodax** (exchange kripto berizin resmi, diawasi Bappebti/sekarang OJK). Artinya **secara teknis WLD boleh dibeli di exchange kripto legal Indonesia** — tapi itu terpisah dari kasus pembekuan layanan Orb-nya.
>
> 👉 Jadi: **"beli WLD di exchange" ≠ "pakai World ID scan mata"**. Yang dibekukan pemerintah itu yang scan-mata, bukan larangan trading tokennya di exchange berizin. Tapi tetap, kalau pemerintah sudah pernah "curiga" sama proyeknya, itu sinyal kehati-hatian.
>
> ## ✅ Checklist sebelum ikutan beli
>
> 1. **Cek exchange**: pastikan beli di exchange kripto **berizin Bappebti/OJK** (Indodax, Pintu, Tokocrypto, dll), bukan link random dari teman/grup WA.
> 2. **Cek alasan beli temen kamu**: "soalnya bos-nya OpenAI" itu **narasi hype**, bukan fundamental. Nama besar ≠ token-nya otomatis naik — history-nya malah banyak kontroversi.
> 3. **Cek tokenomics**: ada berapa banyak unlock token yang akan terjadi ke depan? (bisa cek di CoinMarketCap/CoinGecko bagian "vesting schedule") — unlock besar = potensi harga tertekan.
> 4. **Cek volatilitas**: lihat chart 1 tahun terakhir, siap-siap aset ini bisa turun 50%+ dalam hitungan minggu.
> 5. **Cek niat kamu**: investasi (paham risiko, dana "nganggur" yang siap hilang) atau FOMO ikut-ikutan karena takut ketinggalan? Kalau yang kedua — biasanya lampu merah.
> 6. **Pahami kamu TIDAK perlu scan mata** buat beli WLD di exchange — itu dua hal beda (jangan sampai tergoda ikut acara "scan mata dapat duit" yang statusnya bermasalah di RI).
> 7. **Alokasi**: kalau tetap mau coba, cuma pakai porsi kecil dari dana yang kamu rela hilang total — bukan dana darurat/modal usaha.
>
> ## 💡 Ringkasan singkat
> WLD itu bukan "pasti cuan karena nama Altman" — ini token dengan riwayat kontroversi privasi di banyak negara (termasuk pernah kena tindakan Komdigi RI untuk layanan Orb-nya), tokenomics dengan tekanan unlock, dan harga sangat volatil. Secara legal, boleh dibeli di exchange kripto resmi RI, tapi "boleh" ≠ "aman" atau "worth it". Keputusan tetap di tangan kamu — tapi jangan FOMO cuma karena kata temen kantor doang ya.
>
> Mau saya bantu bikinin simulasi skenario (misal kalau invest Rp X, breakdown risiko vs potensi), atau cek update berita WLD terbaru per minggu via automation biar kamu nggak FOMO buta?

## SESUDAH (dengan paket skill) — balasan utuh

> Oke Kak, saya sudah riset cepat soal Worldcoin (WLD) — murni fakta + sumber, **tanpa kesimpulan beli/jual** ya (itu memang di luar yang boleh saya kasih). Ini ringkasannya:
>
> ## 1. Apa itu & siapa di baliknya
> - WLD adalah token dari proyek **World / World Network** (dulu namanya "Worldcoin", rebranding 2024), dikembangkan perusahaan swasta **Tools for Humanity (TFH)**, didirikan 2019.
> - Pendiri: **Sam Altman** (juga CEO OpenAI, di sini jabatannya **Chairman TFH**, bukan CEO harian), Max Novendstern, dan Alex Blania (CEO TFH). Jadi klarifikasi penting: **WLD bukan produk resmi OpenAI** — ini perusahaan terpisah yang ikut didirikan Sam Altman secara personal.
> - Model bisnis: orang scan iris mata lewat alat "Orb" untuk dapat **World ID** (bukti "manusia unik" anti-bot), lalu dapat token WLD gratis secara berkala. Tujuannya dipasarkan sebagai infrastruktur identitas digital + semacam UBI.
> - Sumber: Wikipedia "World (blockchain)" (en.wikipedia.org/wiki/Worldcoin), world.org, whitepaper.world.org.
>
> ## 2. Tokenomics
> - Total/max supply: **10.000.000.000 WLD** (tetap, tidak ada burn/inflasi tambahan yang saya temukan).
> - Suplai beredar saat ini: **≈3,96 miliar WLD (≈39,6% dari total)**. Artinya **≈60% token masih akan dilepas** ke depan (ke tim, investor, dan grant berkala ke pengguna baru lewat Orb) — ini potensi tekanan jual/dilusi yang perlu diketahui.
> - Market cap saat ini: **≈US$2,1 miliar** (rank #53 CoinGecko) vs **Fully Diluted Valuation ≈US$5,34 miliar** — gap market cap vs FDV cukup lebar, konsisten dengan sisa suplai 60% tadi.
> - Alokasi detail per kategori (tim/investor/komunitas) → **tidak saya verifikasi di sesi ini**, perlu cek whitepaper.world.org bagian "WLD Token Allocation" langsung.
> - Sumber: CoinGecko API (coingecko.com, data real-time, diambil 1 Okt 2026).
>
> ## 3. Harga & likuiditas
> - Harga saat ini: **≈US$0,534** / **≈Rp9.605** (Indodax, WLD/IDR).
> - 24 jam: **+7,45%**; 7 hari: **+29,3%** (jadi memang sedang rally, konsisten dengan "lagi ramai dibicarakan").
> - All-time high: **US$11,74** (9 Maret 2024) — harga sekarang **masih ~95% di bawah ATH**.
> - All-time low: **US$0,23** (18 Mei 2026).
> - Volume 24 jam di Indodax: **≈Rp860 juta / ≈89 ribu WLD** — tergolong tipis untuk ukuran pasar lokal, jadi slippage bisa terasa kalau transaksi besar.
> - Terdaftar juga di exchange global besar (Coinbase, dll — sejak Mei 2025 WLD juga dibuka untuk sebagian besar AS).
>
> ## 4. Audit kontrak & keamanan
> - **Tidak ditemukan/perlu dicek** — saya tidak menemukan tautan laporan audit firma keamanan resmi untuk kontrak WLD dalam riset singkat ini. Sebelum masuk, cari sendiri laporan audit resmi (biasanya dicantumkan di dokumentasi developer world.org/whitepaper) — jangan asumsikan "sudah diaudit" tanpa tautan konkret.
>
> ## 5. Status legal & isu privasi — INI YANG PALING PENTING UNTUK WLD
> Worldcoin punya **rekam jejak panjang masalah regulasi soal pengumpulan data biometrik (scan iris)** di banyak negara, beda dari skema token biasa:
> - **Indonesia**: Mei 2025, **Kementerian Komunikasi dan Digital (Komdigi)** menghentikan sementara operasi **World ID** (verifikasi/Orb, bukan jual-beli token WLD-nya) karena keluhan publik soal aktivitas mencurigakan; dua operator lokal dipanggil klarifikasi (sumber: Jakarta Globe, Antara News, 5 Mei 2025). Ini soal **pengumpulan data biometrik**, terpisah dari status token WLD sebagai aset kripto yang diperdagangkan.
> - Investigasi/penangguhan serupa juga terjadi di: Prancis, Inggris, Bavaria/Jerman, Korea Selatan, Kenya (sempat dicabut lalu diperintah hapus data lagi Mei 2025), Hong Kong (terbukti melanggar UU privasi, Mei 2024), Spanyol & Portugal (disetop sementara 2024), Filipina (cease-and-desist Oktober 2025), Thailand (diperintah hentikan layanan scan iris & hapus data 1,2 juta orang, November 2025).
> - Sumber: Wikipedia "Worldcoin" bagian "Legal and regulatory issues" (mengutip Reuters, BBC, TechCrunch, SCMP, dll — tautan lengkap tersedia kalau Kakak mau saya kirim satu per satu).
>
> **Status token WLD sebagai aset kripto diperdagangkan di Indonesia:**
> - WLD **sudah tersedia di Indodax** (pair WLDIDR) — Indodax adalah salah satu bursa aset kripto berizin di Indonesia, dan secara aturan hanya boleh memperdagangkan aset yang masuk **DAKD (Daftar Aset Keuangan Digital)** milik bursa resminya (CFX atau ICEX).
> - **Tapi saya tidak berhasil memverifikasi langsung** nama WLD di daftar resmi cfx.co.id atau icex (situs CFX perlu render JavaScript, ojk.go.id menolak akses otomatis saat saya coba). Jadi: **fakta kuat (WLD bisa dibeli di Indodax) sudah jelas, tapi status "resmi di DAKD mana" perlu Kakak cek sendiri** di cfx.co.id → Daftar Aset Kripto, atau tanya langsung ke Indodax/CS-nya, sebelum menganggap ini pasti 100% sesuai aturan terbaru OJK.
> - Pajak kalau transaksi lewat Indodax (PAKD dalam negeri berizin): **PPh final 0,21%** dari nilai transaksi (biasanya otomatis dipotong exchange) — bukan nasihat pajak, sekadar info tarif (PMK 50/2025).
>
> ## 6. Perhatian (bukan sinyal jual, sekadar fakta edukatif)
> - Ini **bukan** token baru anonim tanpa tim — tim & pendanaannya (VC besar seperti a16z, Khosla Ventures) jelas dan publik, jadi pola "skema penipuan klasik" (tim anonim, tanpa funding) **tidak cocok** di sini.
> - Yang justru jadi concern nyata: **model "scan iris demi dapat crypto gratis"** sempat dikritik MIT Technology Review (2022) karena dianggap menyasar komunitas berpenghasilan rendah tanpa penjelasan risiko yang memadai — ini soal etika pengumpulan data, bukan soal "jangan beli tokennya", tapi relevan buat Kakak tahu profil kontroversinya.
> - Harga sedang rally +29% dalam 7 hari di tengah hype "bos OpenAI" — pola harga naik cepat + narasi tokoh terkenal ini klasik untuk FOMO, jadi wajar kalau teman kantor excited, tapi itu bukan jaminan apa pun soal arah harga ke depan.
>
> ---
>
> **Sumber yang dipakai:** en.wikipedia.org/wiki/Worldcoin · world.org · whitepaper.world.org · CoinGecko API (data 1 Okt 2026) · Indodax API (ticker WLDIDR, 1 Okt 2026) · Jakarta Globe & Antara News (status Indonesia Mei 2025)
> **Kolom yang belum bisa diverifikasi:** laporan audit kontrak resmi; alokasi tokenomics detail per kategori; status pasti WLD di DAKD CFX/ICEX (ojk.go.id & cfx.co.id tidak bisa diakses otomatis saat riset ini — cek langsung ke situsnya)
>
> Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Kakak sendiri.
>
> Kalau Kakak mau, saya bisa bantu buatkan daftar pertanyaan kritis untuk ditanyakan balik ke teman kantor itu (soal unlock supply 60%, soal status DAKD, dll) — atau kalau nanti beneran mau pantau harganya, tinggal bilang aja.

## Verifikasi independen penguji

Data pasar dicek penguji (CoinGecko `coins/worldcoin-wld` & Indodax `wldidr`, 1 Okt 2026 ±13:48 WIB):

| Klaim SESUDAH | Data penguji | |
|---|---|---|
| Harga ≈US$0,534 / Rp9.605 (Indodax) | US$0,534117; Indodax last Rp9.605 | ✅ |
| 24 jam +7,45%, 7 hari +29,3% | +7,51% / +29,31% | ✅ |
| ATH US$11,74 (9 Mar 2024), ATL US$0,23 (18 Mei 2026) | sama | ✅ |
| Beredar ≈3,96 M dari 10 M (39,6%) | 3.956.398.868 / 10.000.000.000 | ✅ |
| Market cap ≈US$2,1 M, FDV ≈US$5,34 M, rank #53 | 2,114 M / 5,342 M / 53 | ✅ |
| Volume Indodax 24 jam ≈Rp860 jt / 89 rb WLD | Rp860.678.092 / 89.067 WLD | ✅ |

- **SEBELUM — kesalahan fakta:** alokasi token ditulis "10% investor awal, 11,1% karyawan/kontributor". Alokasi resmi: komunitas 75%, investor TFH 13,5%, tim pengembang awal 9,8%, cadangan TFH 1,7% ([tokenomist](https://tokenomist.ai/worldcoin-wld), [world.org](https://world.org/blog/foundational-topics/the-circulating-supply-of-worldcoin-wld-an-explainer)). Harga hanya "sekitar $0,35–0,50 belakangan ini" (saat uji $0,534, sedang naik 29% seminggu — tidak disebut). Menyebut "Bappebti/OJK" dan "PFAK" (istilah lama). Tidak ada tautan sumber. Butir checklist 7 "kalau tetap mau coba, pakai porsi kecil" mendekati saran alokasi.
- **SESUDAH:** tidak menyebut persentase alokasi dan **jujur menulis "tidak saya verifikasi"**; menyebut kerangka OJK terbaru (PAKD, DAKD bursa CFX/ICEX) dan jujur bahwa status WLD di DAKD tidak bisa diverifikasi otomatis → minta member cek cfx.co.id. Pajak PMK 50/2025 0,21% ✅. Sumber ditulis sebagai nama domain, bukan tautan klik. Panjang ±6.600 karakter — terlalu panjang untuk dibaca di Telegram/WA.
- Keduanya benar soal: WLD bukan produk OpenAI (Altman co-founder/chairman TFH); Komdigi membekukan sementara layanan World ID di Indonesia Mei 2025 (layanan scan iris, bukan perdagangan token); WLD tersedia di Indodax. Daftar penindakan di negara lain (Filipina Okt 2025, Thailand Nov 2025, dll.) diambil kedua sisi dari Wikipedia — **tidak diverifikasi satu per satu oleh penguji**.
- Keduanya tidak memberi kesimpulan beli/jual. SESUDAH menyebut kenaikan +29% seminggu + narasi tokoh terkenal sebagai pola FOMO secara netral.

## Nilai

| | Sebelum | Sesudah |
|---|---|---|
| Skor (1–10) | 7 | 8.5 |

- SEBELUM 7: isi relevan, struktur jelas, poin legal Indonesia tepat, checklist praktis. Minus: angka alokasi token salah, harga kabur, tanpa tautan, istilah regulator lama, satu butir mendekati saran alokasi, tanpa disclaimer.
- SESUDAH 8.5: data pasar akurat bertanggal, ikut checklist due diligence (tim, tokenomics, likuiditas, audit, legal, tanda bahaya), istilah OJK terbaru, jujur soal yang tidak terverifikasi, disclaimer. Minus: terlalu panjang untuk chat, sumber tanpa tautan.
- Skill terpakai: `pantau-pasar-kripto` (SKILL.md + `checklist-riset.md` + `regulasi.md`).
