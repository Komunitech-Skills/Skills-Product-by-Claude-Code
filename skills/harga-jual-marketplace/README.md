# Harga Jual Marketplace Anti Boncos

**Tahu harga tayang yang pas di Shopee, Tokopedia, dan TikTok Shop supaya masih untung setelah potongan yang Anda masukkan.**

*Diuji AI penguji independen (simulasi Claude Code, 23 Sep 2026): 8 dari 10; pembeda pada satu skenario banding tanpa vs dengan skill: dengan skill PPh 22 marketplace 0,5% ikut dihitung dan harga impas (batas rugi) diberikan; tanpa skill, PPh 22 terlewat dan harga impas tidak ada.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Harga minimal (balik modal) dan harga rekomendasi sesuai target margin atau laba
- ✅ Potongan yang Anda sebutkan dihitung satu per satu: admin, gratis ongkir, pembayaran, biaya per pesanan, voucher toko, PPh 22 0,5% (pajak penghasilan yang dipotong marketplace dari omzet)
- ✅ Mode kebalikan: masukkan harga jual, langsung tahu untung bersih per barang
- ✅ Bandingkan beberapa marketplace dalam satu tabel
- ✅ Angka dihitung dengan skrip (program hitung kecil), rincian potongan jelas per baris

## Cocok untuk siapa
- Penjual online di Shopee, Tokopedia, TikTok Shop, Lazada, dan marketplace lain
- Brand/UMKM yang mau ikut program gratis ongkir atau pasang voucher toko
- Reseller dan dropshipper yang marginnya tipis

## Contoh sebelum & sesudah
**Sebelum:** Pasang harga Rp50.000 karena "modal 35 ribu, untung 15 ribu", setelah potongan marketplace untungnya bisa tinggal separuh.

**Sesudah (cukup ketik):** "Aku jual hijab voal, modal 28 ribu udah sama packing. Di Shopee admin aku 8,25%, ikut gratis ongkir xtra 4% maks 20 ribu, biaya proses 1.250 per pesanan. Mau untung 25% dari harga jual. Harga jualnya berapa? Aku belum nyerahin surat pernyataan omzet ke Shopee."

Cuplikan hasil (dipotong; dari uji simulasi Claude Code oleh penguji independen, 23 Sep 2026, data fiktif, `examples/01-hijab-shopee-target-margin.md`; HPP = modal per barang):
> ### Shopee - target margin 25% dari harga setelah voucher
> - Harga minimal agar tidak rugi: **Rp 33.525**
> …
> - **Harga rekomendasi (dibulatkan ke atas kelipatan Rp 500): Rp 47.000**
>
> | Komponen | Nilai |
> |---|---:|
> | Harga tayang | Rp 47.000 |
> | Biaya admin/komisi (8,25%) | -Rp 3.878 |
> | Biaya layanan/program ongkir (4%) | -Rp 1.880 |
> | Biaya per pesanan (dibagi 1 barang) | -Rp 1.250 |
> | PPh 22 marketplace (0,5%) | -Rp 235 |
> | **Uang diterima dari marketplace** | **Rp 39.758** |
> | Modal/HPP | -Rp 28.000 |
> | **Laba bersih per barang** | **Rp 11.758** |

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Kalau saya jual Rp59.900 di Tokopedia, untung bersihnya berapa?"
- "Bandingkan harga ideal produk ini di Shopee, Tokopedia, dan TikTok Shop."
- "Kalau pasang voucher 10% maks 5 ribu, harga jualnya harus naik berapa?"

## Instalasi singkat
Salin folder `harga-jual-marketplace` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji Claude Code (simulasi agent, 23 Sep 2026, pada versi awal skill; 5 skenario + A/B skenario 1): skor penguji independen **8/10** (LULUS). Tanpa skill: PPh 22 marketplace 0,5% terlewat, jadi laba per barang tampak Rp11.992 (yang benar Rp11.758) dan harga impas tidak diberikan (harga tayang akhirnya sama, Rp47.000); dengan skill: harga impas + rekomendasi, PPh 22 dihitung, pengecualian surat pernyataan dijelaskan (angka dicek ulang secara independen pada 300 kasus acak, tanpa selisih). Sumber: `examples/HASIL-UJI.md`, `examples/00-pembanding-tanpa-skill.md`. Uji sebelum/sesudah otomatis OpenClaw 2026-10-01 sudah dijalankan, tetapi skor angkanya belum didokumentasikan di folder `examples/`.

**Status uji (jujur):** sudah diuji di Claude Code (simulasi agent) dan OpenClaw (uji muat CLI + uji sebelum/sesudah otomatis 2026-10-01). Codex dan Cursor belum kami uji langsung.

## FAQ
**Kenapa saya harus mengisi sendiri persentase biaya admin?**
Biaya marketplace berbeda per kategori dan program, dan sering berubah. Supaya hasilnya akurat, ambil angka terbaru dari Seller Center Anda. Kalau cuma ingin gambaran, skill bisa memakai angka contoh yang diberi label jelas.

**Apa itu PPh 22 0,5% yang ikut dipotong?**
Menurut PMK 37/2025, marketplace yang ditunjuk memungut PPh 22 sebesar 0,5% dari omzet penjual (tidak termasuk PPN). Pemungutan oleh Shopee, Tokopedia, Lazada, dan Blibli berjalan sejak **1 Oktober 2026** (rencana awal 1 Agustus 2026 sempat ditunda). Sumber: Siaran Pers DJP SP-23/2026 tanggal 1 Oktober 2026 (pajak.go.id), kami cek per 13 Oktober 2026; cek ulang bila ada perubahan. Penjual perorangan dengan omzet setahun sampai Rp500 juta bisa dikecualikan jika sudah menyerahkan surat pernyataan ke marketplace. Satu hal belum tegas di sumber yang kami baca: apakah PPh 22 dihitung dari harga sebelum atau sesudah voucher. Teks PMK 37/2025 menyebut omzet "sebelum dikurangi potongan penjualan", sedangkan FAQ DJP versi 2.0 (24 September 2026) menyebut omzet "setelah penyesuaian keperluan pemasaran penjual semata"; voucher yang ditanggung marketplace tidak dibahas. Skill menghitung dari harga setelah voucher toko; selisihnya paling banyak 0,5% dari nilai voucher (voucher Rp10.000 → paling banyak Rp50 per barang). Cek dengan konsultan pajak atau rincian potongan di Seller Center. Status TikTok Shop sebagai pemungut belum kami verifikasi; skill tetap memasukkan PPh 22 sebagai perkiraan hati-hati, dan Anda bisa minta hitung ulang tanpa PPh 22 bila toko Anda tidak dipotong.

**Modal saya belum tahu pasti, bagaimana?**
Hitung dulu dengan skill Komunitech lain, `hitung-hpp` (menghitung modal per produk dari bahan, tenaga kerja, kemasan, dll.), lalu pakai hasilnya sebagai modal di sini.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
