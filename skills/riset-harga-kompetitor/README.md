# Cek Harga Pesaing, Pasang Harga Tetap Untung

**Tempel link atau screenshot produk pesaing, dapatkan harga pasaran dan harga jual yang disarankan tanpa merusak margin.**

*Diuji AI penguji independen di OpenClaw (16 Oktober 2026, versi 1.0.5, satu skenario kopi gayo 250 gr, lokal dan konteks Telegram): tanpa skill 5 → dengan skill 8,0 dari 10. Lulus tipis: skor tanpa skill dibatasi karena dua salah hitung persen untung dan jumlah harga coret; semua angka dengan skill cocok dengan hitungan independen (median Rp53.125, harga minimum tetap untung Rp46.297). Uji simulasi Claude Code sebelumnya: 8,5 dari 10.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tabel pembanding rapi: harga, harga coret, promo, rating, terjual, lokasi tiap pesaing
- ✅ Adil walau ukurannya beda: 200 gr, 1/2 kg, 1 kg, paket "2 x 250 gr" atau "isi 2 @250gr" disetarakan ke ukuran produk Anda (plus harga per 100 g/ml/pcs); harga yang janggal (jauh dari pasaran) dipisahkan dan ditanyakan dulu agar tidak merusak hitungan
- ✅ Tahu posisi harga Anda: termurah, tengah, atau termahal dibanding pasar (harga terendah, harga tengah/median, tertinggi)
- ✅ Harga minimum dihitung dari modal + biaya marketplace + target untung, jadi rekomendasi dijaga **tidak di bawah batas untung** yang dihitung dari angka yang Anda berikan (modal atau biaya yang keliru tetap bisa membuat hasilnya meleset)
- ✅ Peringatan jelas kalau harga pasaran sudah di bawah batas untung Anda, plus ide promo & bundling (paket gabungan) dari pesaing

## Cocok untuk siapa
- Penjual online di Shopee, Tokopedia, TikTok Shop, Lazada, atau website sendiri
- UMKM makanan/minuman, fesyen, kosmetik, kerajinan yang mau meluncurkan produk baru
- Reseller yang bingung kenapa tokonya sepi padahal "harga sudah murah"

## Contoh sebelum & sesudah
**Sebelum:** Buka 8 tab satu per satu, catat harga di kertas, bingung karena ada yang 200 gr, 500 gr, dan 1 kg. Akhirnya pasang Rp65.000 "biar untung", ternyata paling mahal sepasar.

**Sesudah (cukup ketik):** "Cek harga kopi gayo 250 gr di link-link ini. Modal saya 32 ribu, jual di Shopee admin 8%, gratis ongkir 4%. Sekarang saya jual 65 ribu."
→ Hasilnya (dipotong): 6 pesaing dibandingkan pada ukuran setara 250 g.
```
| Terendah | Kuartil bawah (P25) | Median (tengah) | Kuartil atas (P75) | Tertinggi |
|---|---|---|---|---|
| Rp 49.900 | Rp 50.588 | **Rp 54.375** | Rp 57.188 | Rp 62.000 |

- Harga kamu sekarang **Rp 65.000**: lebih murah dari 0 pesaing, sama dengan 0, lebih mahal dari 6 (posisi sekitar persentil 100). Laba Rp 23.625 per barang (margin 36,35%).
- Pesaing paling laris: Warung Kopi Kita (sekitar 2.300 terjual) di harga setara Rp 49.900.
…
| **Harga minimum sesuai target margin** | **Rp 49.260** |
…
- **Rentang harga: Rp 50.588 - Rp 57.188** (dasar: P25 - P75, titik median pasar)
- Titik rekomendasi: **Rp 54.375** (laba Rp 14.328 per barang, margin 26,35%)
- Harga cantik terdekat (masih di dalam rentang): **Rp 53.900** (laba Rp 13.913, margin 25,81%)
```
(Contoh dengan data fiktif dari `examples/contoh-pembuat-kopi-gayo.md`, dipotong. Rentang P25–P75 adalah kisaran harga tempat separuh pesaing berada; "persentil 100" berarti harga Anda lebih mahal dari semua pesaing; "harga cantik" adalah harga berakhiran angka menarik, mis. Rp53.900.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Harga pasaran keripik singkong 250 gr berapa? Ini link-link pesaing saya."
- "Saya tempel screenshot 5 toko pesaing, harga saya 45 ribu kemahalan nggak? Modal 27 ribu."
- "Mau jual serum 20 ml, modal 38 ribu, target untung 30%. Bandingkan dengan produk-produk ini."

Kalau link Shopee/Tokopedia tidak bisa dibuka AI (sering diblokir), cukup tempel teks halamannya atau kirim screenshot. Skill ini tidak memakai akun/login marketplace Anda.

## Instalasi singkat
Salin folder `riset-harga-kompetitor` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Tidak perlu API key, akun, atau instalasi tambahan (hitungan memakai Python bawaan; tanpa Python pun tetap bisa dengan hitung manual).

**Hasil uji (angka nyata):**
- **Uji sebelum/sesudah OpenClaw, 16 Oktober 2026 (versi 1.0.5)** (`examples/00-openclaw-sebelum-sesudah.md`): satu skenario (8 baris pesaing dengan 1 duplikat, modal Rp30.000, biaya Shopee, target untung 20 %), tanpa skill **5** → dengan skill **8,5** lokal dan **7,5** di konteks Telegram (rata-rata 8,0). Tanpa skill: persen untung salah hitung (ditulis 45–53 %, benar 47,5–56,3 %), jumlah pesaing berharga coret salah (4, benar 3), dan menyarankan harga coret fiktif. Dengan skill: semua harga disetarakan ke 250 gr, duplikat dibuang, median Rp53.125, harga minimum tetap untung Rp46.297, harga cantik Rp52.900; semua cocok dengan hitungan independen. Catatan jujur: kelulusan bergantung pada aturan skor maksimal 5 untuk jawaban bersalah angka; tanpa aturan itu selisihnya sekitar 1 poin. Versi Telegram membuang catatan rentang harga satu pesaing.
- Uji lama: uji Claude Code simulasi agent, skor **8,5/10** (LULUS; uji ulang independen terakhir pada v1.0.3). Hitungan dicocokkan ulang dengan hitungan independen: **117** angka pada uji awal dan **388** angka pada uji ulang v1.0.1, semuanya **0 selisih**. Contoh kopi Gayo di atas (median Rp54.375, rekomendasi Rp50.588–Rp57.188, harga cantik Rp53.900, laba Rp13.913) adalah hasil skrip pada data fiktif dari pembuat skill, bukan uji independen. Di OpenClaw: uji platform otomatis oleh agent, 6 dari 6 butir lulus (`examples/UJI-PLATFORM.md`); uji sebelum/sesudah OpenClaw dengan skor belum dilakukan. Sumber: `examples/HASIL-UJI.md`, `examples/06-uji-ulang-v1.0.1.md`, `examples/UJI-PLATFORM.md`.

**Status uji (jujur):** versi 1.0.5 diuji sebelum/sesudah oleh penguji AI independen di OpenClaw 2026.10.2 pada 16 Oktober 2026 (lulus tipis, satu skenario; lihat Hasil uji); sebelumnya diuji Claude Code (simulasi agent) dan di OpenClaw (uji platform otomatis oleh agent + muat CLI). Codex dan Cursor belum uji platform asli. Skill tidak login atau mengambil data marketplace secara massal; link sering diblokir → tempel teks/screenshot. Pada uji pengambilan data dari web, hanya 1 dari 3 halaman publik yang terbaca (satu halaman Shopee kosong, satu situs error 503), jadi jangan mengandalkan pengambilan otomatis dari marketplace.

## FAQ
**Apakah AI bisa otomatis mengambil harga dari Shopee/Tokopedia?**
Kalau AI agent Anda punya fitur membuka halaman web, ia akan mencoba membuka link publik satu per satu (maks. ±20). Banyak marketplace memblokir akses seperti ini; kalau begitu, AI akan minta Anda menempel teks atau screenshot. Skill ini sengaja tidak login, tidak melewati blokir, dan tidak memantau harga terjadwal, mengikuti aturan situs dan kebijakan Komunitech.

**Kenapa harga rekomendasinya bisa lebih mahal dari pasaran?**
Karena rekomendasi dijaga tidak di bawah harga minimum (modal + biaya + target untung). Kalau pasaran memang lebih murah, Anda akan dapat PERHATIAN beserta pilihan: tekan modal, buat paket/bundling, ganti ukuran, atau tonjolkan keunggulan, daripada ikut perang harga lalu rugi.

**Saya belum tahu modal saya, bisa tetap dipakai?**
Bisa. Tanpa modal, Anda tetap dapat tabel pesaing dan harga pasaran (terendah, median, tertinggi). Rekomendasi harga jual baru muncul setelah modal diisi, supaya tidak menyarankan harga yang bikin rugi.

**Biaya marketplace saya belum tahu, bagaimana?**
Bisa dianggap 0% dulu (jualan langsung) dan AI akan menyebut asumsi itu. Untuk angka potongan Shopee/Tokopedia/TikTok Shop yang rinci, pakai skill Komunitech lain untuk harga jual di marketplace (`harga-jual-marketplace`); untuk menghitung modal per produk (HPP), pakai skill hitung modal (`hitung-hpp`).

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
