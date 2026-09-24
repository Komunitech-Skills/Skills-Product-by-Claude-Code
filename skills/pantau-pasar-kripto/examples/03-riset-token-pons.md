# 03 — Riset proyek token yang sedang ramai: Pons (PONS)

**Skenario:** S3 normal. Token dipilih penguji dari daftar *trending* CoinGecko (`/search/trending`, 24 Sep 2026 ±07:45 WIB): **Pons (PONS)**, token launchpad di Robinhood Chain yang naik tajam sejak Juli 2026.

## Input pengguna (persis)
> bikinin riset koin PONS dong, lagi rame banget di grup. saya mau tau faktanya aja

## Output (mengikuti SKILL.md Langkah C + references/checklist-riset.md)

**Riset fakta: Pons (PONS)** — disusun 24 Sep 2026, 07:50 WIB. Hanya fakta bersumber; kolom tanpa sumber ditulis "tidak ditemukan / perlu dicek".

**1. Tim & organisasi**
- Entitas yang tercantum: "© 2026 Pons Labs, LLC" (docs.ponsfamily.com). Negara/tempat pendaftaran badan usaha: **tidak ditemukan / perlu dicek**.
- Nama pendiri/tim: **tidak ditemukan** di situs resmi maupun dokumentasi (tim praktis anonim bagi publik).
- Bukan produk resmi Robinhood; berjalan di Robinhood Chain (layer-2 yang diluncurkan Robinhood 1 Juli 2026 menurut Decrypt).

**2. Tokenomics**
- Suplai maksimum 1.000.000.000 PONS; suplai beredar ±684,3 juta; total ±684,2 juta (CoinGecko, data 24 Sep 2026 07:45 WIB).
- Mekanisme: sebagian pendapatan biaya dipakai *buyback-and-burn* (Decrypt: "about 80% of Pons's revenue funds an automatic buyback-and-burn"; ±29% suplai sudah dibakar per 3 Sep 2026). Untuk token yang diluncurkan lewat platform, biaya dibagi "creator 70% · protocol 30%" (docs).
- Alokasi awal (tim/investor/komunitas) & jadwal vesting: **tidak ditemukan / perlu dicek** (tidak ada di situs & docs yang dibaca).

**3. Audit kontrak & keamanan**
- Laporan audit firma keamanan: **tidak ditemukan** di situs, docs, maupun artikel Decrypt. Ini fakta penting: belum ada audit publik yang bisa dirujuk.
- Kontrak di Robinhood Chain: `0x39dbed3a2bd333467115de45665cc57f813c4571` (explorer: robinhoodchain.blockscout.com, dari CoinGecko).
- Riwayat exploit: **tidak ditemukan / perlu dicek**.

**4. Likuiditas & perdagangan** (CoinGecko, 24 Sep 2026 07:45 WIB)
- Harga US$0,6395 (±Rp 11.420); perubahan 24 jam −8,62%; 7 hari +11,44%.
- Kapitalisasi ±US$437,6 juta; volume 24 jam ±US$99,8 juta.
- Riwayat: terendah US$0,0033 (17 Jul 2026), tertinggi US$0,971 (5 Sep 2026) — naik ±290 kali dalam 7 minggu, lalu turun ±34% dari puncak.
- Tempat perdagangan: DEX di Robinhood Chain (Uniswap, Ramses, dll.) dan exchange luar negeri (Bybit, OKX, Gate, MEXC, Crypto.com, dll.). **Tidak ada di Indodax** (dicek: `indodax.com/api/pairs` 484 pasangan, tidak ada PONS; `ticker/ponsidr` → "Invalid Pair").

**5. Status legal di Indonesia**
- Sejak 10 Jan 2025 pengawasan aset kripto di OJK (UU 4/2023 P2SK, PP 49/2024, POJK 27/2024 — siaran pers OJK). Per siaran pers OJK 4 Agustus 2026 ada **dua** bursa: CFX dan ICEX, masing-masing punya Daftar Aset Keuangan Digital (DAKD); pedagang berizin hanya boleh memperdagangkan aset dalam daftar.
- Apakah PONS ada di DAKD CFX/ICEX: **belum bisa dipastikan** (daftar CFX berbentuk 130 halaman/PDF pindaian, tidak terbaca otomatis di sesi ini). **Perlu dicek** di cfx.co.id → Daftar Aset Kripto, dan di daftar ICEX, atau tanyakan ke exchange berizin OJK Anda.
- Fakta terverifikasi: PONS tidak tersedia di Indodax (exchange berizin) saat dicek.

**6. Perhatian (edukasi, bukan sinyal)**
- Kenaikan ratusan kali dalam hitungan minggu dan grup yang "ramai" adalah pola yang juga terlihat pada aset yang kemudian turun tajam; situs Pons sendiri menulis: "Tokens can be volatile or lose all value."
- Tim tidak disebut namanya dan tidak ditemukan audit publik.
- Decrypt mencatat estimasi kapitalisasi bervariasi (US$392–576 juta), "a reminder of how thin and fast-moving the token's on-chain liquidity still is."
- Kalau ajakan di grup memuat janji untung pasti, tekanan "buruan sebelum terbang", atau ajakan beli bareng pada jam tertentu — itu ciri klasik skema pump; laporkan ke OJK (157) bila ada penawaran investasi.

```
Sumber yang dipakai:
- https://api.coingecko.com/api/v3/coins/pons (data 2026-09-24T00:45:40Z) & /search/trending
- https://ponsfamily.com/ · https://docs.ponsfamily.com/
- https://finance.yahoo.com/markets/crypto/articles/pons-robinhood-chain-meme-coin-204604745.html (Decrypt, 3 Sep 2026)
- https://indodax.com/api/pairs · https://indodax.com/api/ticker/ponsidr
- https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/RDKB-Juli-2026.aspx (SP 147/DKPU/OJK/VIII/2026)
- https://www.cfx.co.id/id/products-and-services/crypto-asset-list
Kolom yang belum bisa diverifikasi: negara badan usaha, nama tim, alokasi & vesting awal, audit, riwayat exploit, status DAKD CFX/ICEX.
Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.
```

## Catatan penguji
- Setiap klaim di atas dicek ke sumbernya (WebFetch/curl). Tidak ada kesimpulan beli/jual/tahan maupun target harga. ✅
- Checklist bekerja baik: kolom kosong ditulis jujur, tanda risiko disampaikan netral.
- **Kelemahan referensi:** `checklist-riset.md` §5 dan `regulasi.md` §2 menyebut daftar aset "ditetapkan Bursa (CFX)" seolah hanya satu bursa. Per siaran pers OJK 4 Agustus 2026 ada dua bursa (CFX & ICEX) dengan DAKD masing-masing — agent di atas menambahkan ini dari pencarian, bukan dari skill.
- Skill tidak memberi cara praktis mengecek DAKD (daftar CFX 130 halaman / PDF pindaian); sebaiknya beri langkah manual yang jelas untuk awam.
