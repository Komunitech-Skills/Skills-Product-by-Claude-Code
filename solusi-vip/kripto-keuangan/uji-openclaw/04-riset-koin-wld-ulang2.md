# Uji ULANG ke-2 — 04 Riset koin Worldcoin (WLD)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen putaran ke-2 (bukan pembuat, tidak mengubah skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member · home `sol2-kripto-keuangan` (6 skill paket; `atur-keuangan-pribadi` **1.0.6**, `pantau-pasar-kripto` **1.0.6**, isi folder identik dengan repo), **direset bersih (`reset2-kripto.sh`) sebelum tiap sesi**. Pesan, jawaban lanjutan, dan data file identik dengan uji asal.

Pembanding: [04-riset-koin-wld.md](04-riset-koin-wld.md) (8.5), [04-riset-koin-wld-ulang.md](04-riset-koin-wld-ulang.md) (1.0.5: 7.5).

## Pesan member

> kak temen kantor ngajak beli koin Worldcoin (WLD), katanya bakal booming soalnya yg bikin bos OpenAI. sebelum ikut2an saya mau riset dulu. tolong bikinin catatan riset singkat soal koin ini ya, apa aja yg perlu saya cek, boleh dibeli di indonesia gak

Tool: read, tool_search, web_fetch, tool_call, exec.

## Balasan utuh (2.620 karakter)

> Udah aku riset — bukan kesimpulan beli/jual, cuma fakta + sumber biar kakak yang putuskan sendiri. Ini versi ringkas dulu, kalau mau versi lengkap tiap bagian checklist tinggal bilang.
>
> **Harga & pasar** (CoinGecko, data 14:45 WIB 1 Okt 2026 — https://api.coingecko.com/api/v3/coins/worldcoin-wld):
> • WLD ≈ US$0,524 / Rp9.421 — market cap rank #53 (~US$2,07 M)
> • 24 jam +4,5%, 7 hari +26%, tapi 1 tahun -57,8% dan -95,5% dari ATH (US$11,74, Mar 2024)
> • Supply: max/total 10 miliar WLD (sudah fix, bukan inflasi tak terbatas), yang beredar baru ~3,96 M (39,6%) — artinya market cap baru 40% dari nilai full-diluted, jadi masih ada ~6,6 M token belum beredar yang berpotensi menekan harga saat di-unlock.
>
> **Terdaftar di Indonesia**: ada pair WLD/IDR aktif di Indodax, harga Rp9.457 (14:49 WIB — https://indodax.com/api/ticker/wldidr). Tapi status WLD di **DAKD resmi CFX/ICEX** (daftar aset berizin OJK) belum berhasil saya cek langsung — situsnya https://www.cfx.co.id perlu dibuka manual (render JavaScript, gagal diakses otomatis). Sebelum beli, cek dulu: (1) platform yang dipakai benar PAKD berizin OJK, (2) WLD ada di DAKD-nya.
>
> **Tim/organisasi**: entitas resmi di baliknya tercantum di Terms & Conditions — World Foundation (Cayman Islands), World Assets Limited (BVI), World Chain LLC (Cayman) — https://world.org/legal/user-terms-and-conditions. Whitepaper resmi ada, tunduk kerangka MiCA Uni Eropa — https://whitepaper.world.org/
>
> **Audit kontrak**: tidak ditemukan laporan audit resmi WLD dari pencarian ini — perlu dicek. Catatan penting: ada halaman CertiK berjudul "WorldCoin (**WDC**)" bukan WLD — ticker beda, jangan disamakan sebelum diverifikasi ulang (bisa jadi token lain).
>
> **Tokenomics (alokasi tim/investor/komunitas)**: belum bisa saya cek dari sumber resmi terbaru — halaman blog alokasi world.org tidak bisa diakses saat riset ini. Perlu dicek manual.
>
> **Perhatian**: tidak saya temukan tanda klasik skema penipuan (janji imbal hasil tetap, tekanan buru-buru, dll) — ini proyek besar dengan tim diketahui publik & whitepaper resmi, bukan token anonim baru. Tapi harga sangat volatil (1 tahun -58%) — risiko fluktuasi tinggi tetap ada di luar soal legitimasi proyek.
>
> Sumber lengkap: https://api.coingecko.com/api/v3/coins/worldcoin-wld · https://indodax.com/api/ticker/wldidr · https://world.org/legal/user-terms-and-conditions · https://whitepaper.world.org/
> Kolom belum terverifikasi: audit kontrak resmi, alokasi token tim/investor/komunitas, status WLD di DAKD CFX & ICEX.
>
> Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

## Verifikasi independen penguji (14:52 WIB; CoinGecko `coins/worldcoin-wld` `last_updated` 07:49:40 UTC = 14:49 WIB; Indodax `wldidr`)

| Klaim balasan | Data penguji | |
|---|---|---|
| "data 14:45 WIB" | tarikan agent beberapa menit sebelum penguji; UTC→WIB benar | ✅ (cacat jam 7 jam hilang) |
| US$0,524 / Rp9.421 | US$0,5232 / Rp9.399 | ✅ |
| Rank #53, mcap ±US$2,07 M | #53, US$2,071 M | ✅ |
| 24 jam +4,5%, 7 hari +26%, 1 th −57,8% | +4,0% / +25,9% / −57,9% | ✅ |
| −95,5% dari ATH US$11,74 (Mar 2024) | 0,5232/11,74 − 1 = −95,5%; ATH 9 Mar 2024 | ✅ |
| Beredar ±3,96 M (39,6%), max 10 M | 3.956.400.032 / 10.000.000.000 | ✅ |
| **"masih ada ~6,6 M token belum beredar"** | 10 M − 3,96 M = **6,04 M** | ❌ salah hitung (±0,56 M) |
| Indodax Rp9.457 (14:49 WIB) | last Rp9.457 | ✅ |
| Entitas: World Foundation (Cayman), World Assets Ltd (BVI), World Chain LLC | tautan world.org/legal… HTTP 200 | ✅ (tidak dibaca rinci penguji) |
| Whitepaper resmi | whitepaper.world.org HTTP 200 | ✅ |

## Cacat sisa putaran 1

| Cacat sisa | Hilang? | Bukti |
|---|---|---|
| Sumber hanya nama domain, tanpa `https://` | **ya** | blok *"Sumber lengkap: https://api.coingecko.com/api/v3/coins/worldcoin-wld · https://indodax.com/api/ticker/wldidr · https://world.org/legal/user-terms-and-conditions · https://whitepaper.world.org/"* (2 di antaranya URL API JSON — benar tapi kurang ramah awam) |
| Jam data "07:10 WIB" (UTC dikira WIB) | **ya** | *"data 14:45 WIB 1 Okt 2026"* |
| Alokasi token usang 10%/11,1% | **ya** | *"Tokenomics (alokasi tim/investor/komunitas): belum bisa saya cek dari sumber resmi terbaru … Perlu dicek manual."* |
| Panjang di atas 2.500 karakter | **ya (hampir)** | 2.620 karakter, menawarkan versi lengkap |

## Regresi / temuan baru

1. **Klaim teman "yang bikin bos OpenAI" tidak dijawab.** Uji asal dan ulang 1.0.5 sama-sama meluruskan: Sam Altman salah satu pendiri, tetapi proyek ini milik Tools for Humanity, bukan produk OpenAI. Kali ini tidak disinggung sama sekali, padahal itu alasan utama ajakan teman member.
2. **"Boleh dibeli di Indonesia" kurang lengkap:** penghentian sementara layanan World ID/Orb oleh Komdigi (Mei 2025) — isu privasi biometrik yang relevan untuk orang Indonesia — tidak lagi disebut; POJK 27/2024 dan PPh 0,21% juga tidak disebut (ulang 1.0.5 menyebutnya). Yang tersisa: WLD/IDR ada di Indodax + ajakan cek PAKD/DAKD (benar dan jujur).
3. Salah hitung token belum beredar (6,6 M, seharusnya ±6,04 M) — tidak mengubah kesimpulan, tetapi angka keliru.
4. Positif: jujur menulis "belum terverifikasi" untuk audit, tokenomics, dan DAKD; waspada ticker CertiK "WDC" ≠ WLD; tanpa kesimpulan beli/jual; disclaimer ada.

## Nilai

| | Asal | Ulang 1.0.5 | **Ulang ke-2 1.0.6** |
|---|---|---|---|
| Skor | 8.5 | 7.5 | **7.5** |

Keempat cacat sisa beres (URL lengkap, jam WIB benar, tokenomics tidak dikarang, ringkas). Skor tidak naik karena isi yang paling dibutuhkan member hilang: klaim "bikinan bos OpenAI" tidak diluruskan dan konteks Indonesia (Komdigi, OJK, pajak) menipis, plus satu salah hitung. Saran: checklist riset wajib memuat baris "klaim yang beredar (dari pesan member) → fakta + sumber" dan baris "konteks Indonesia: OJK/DAKD, regulator lain (Komdigi), pajak".
