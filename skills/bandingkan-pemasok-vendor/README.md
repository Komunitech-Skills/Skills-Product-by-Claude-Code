# Pilih Pemasok Paling Untung, Bukan Paling Murah

**Tempel penawaran dari beberapa pemasok, dapatkan total biaya sampai di tempat, pilihan terbaik beserta alasannya, dan pesan WA siap kirim untuk menawar atau menanyakan yang belum jelas.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor; langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk hitungan yang tepat; tanpa Python skill tetap berjalan, AI menghitung langsung tetapi angkanya sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu uang yang benar-benar keluar**, bukan cuma harga satuan: harga grosir bertingkat, minimal order, isi per dus, ongkir, PPN, dan biaya lain dihitung untuk jumlah yang Anda butuhkan.
- ✅ **Tidak tertipu harga "belum PPN"**: pemasok yang sudah PKP (memungut PPN) dan yang belum dibandingkan setara; bila usaha Anda sendiri PKP, PPN yang bisa dikreditkan ikut diperhitungkan.
- ✅ **Pilihan terbaik dengan alasan jelas**: nilai gabungan biaya, kecepatan kirim, termin bayar (DP/tempo/COD), kualitas, dan fleksibilitas minimal order; bobotnya bisa Anda ubah sesuai prioritas.
- ✅ **Tahu kapan pilihan berubah**: bila jumlah beli jadi 2 kali, bila pemasok termurah telat, atau bila pesanan dibagi ke dua pemasok supaya tidak bergantung pada satu pemasok.
- ✅ **Pesan WA siap kirim** untuk menanyakan ongkir/PPN/garansi dan menawar secara sopan, tanpa klaim palsu.

## Cocok untuk siapa
- Pemilik kafe, resto, toko online, konveksi, percetakan, bengkel, dan usaha yang rutin membeli bahan baku, kemasan, atau barang dagangan.
- Admin pembelian dan staf kantor yang harus menyiapkan perbandingan penawaran untuk atasan.
- Reseller/dropshipper yang memilih pemasok grosir.
- **Bukan untuk:** mencatat stok (skill Buku Stok, `buku-stok`), menentukan kapan pesan ulang (`rencana-restok-barang`), atau membuat penawaran harga ke pelanggan Anda (`surat-penawaran-harga`).

## Contoh sebelum & sesudah
**Sebelum:** tiga penawaran kemasan di WA: Rp4.500, Rp4.300 (minimal 500 pcs), Rp4.650. Kelihatannya yang Rp4.300 paling murah.

**Sesudah:** akan diisi dari hasil uji.

## Cara pakai
Tempel penawaran (boleh langsung dari chat WA pemasok) lalu tulis misalnya:
- "Saya butuh 300 pcs dalam 2 minggu. Ini 3 penawaran, mana yang paling untung?"
- "Supplier A PKP harga belum PPN, B non-PKP. Bandingkan untuk 50 kg per minggu."
- "Bandingkan lagi, tapi utamakan pengiriman cepat dan tempo bayar."

Tidak perlu lengkap. Data yang belum ada (misalnya ongkir) ditandai `[isian]`, dan AI bertanya paling banyak tiga hal di akhir. Format rapi (opsional) ada di `templates/format-penawaran.md`.

## Instalasi singkat
Salin folder `bandingkan-pemasok-vendor` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputer Anda.

**Status uji (jujur):** belum diuji di platform mana pun; hasil uji akan dicantumkan di sini setelah pengujian.

## FAQ
**Apakah AI memilihkan pemasok yang paling murah?**
Belum tentu. Yang paling murah harga satuannya bisa jadi paling mahal setelah ongkir, PPN, atau minimal order dihitung, atau terlambat dari tanggal yang Anda butuhkan. AI memberi pilihan terbaik menurut prioritas Anda beserta alasannya; keputusan tetap di tangan Anda.

**Bisa dibuatkan penawaran pembanding supaya pengajuan ke atasan atau tender kelihatan lengkap?**
Tidak. Penawaran pembanding harus asli dari pemasok sungguhan. Sebagai gantinya AI menyiapkan pesan permintaan penawaran tertulis ke 2-3 pemasok, lalu membandingkan semuanya dengan jujur. Begitu pula permintaan fee pribadi dari pemasok atau mengambil harga lewat login akun marketplace: ditolak, tetapi perbandingan dari data asli tetap dikerjakan.

**Apakah perhitungan PPN-nya pasti sama dengan faktur?**
PPN dihitung dengan aturan yang berlaku untuk barang biasa (efektif 11% dari harga sebelum PPN) dan dibulatkan ke bawah. Pembulatan bisa berbeda beberapa rupiah dengan faktur resmi; bila berbeda, ikuti faktur. Untuk barang mewah, impor, atau kasus pajak khusus, tanyakan ke konsultan pajak.

> **Catatan penting:** alat bantu keputusan pembelian, bukan nasihat pajak atau hukum. Angka hanya dihitung dari penawaran yang Anda berikan; pastikan harga, PPN, ongkir, dan syarat tertulis di penawaran resmi atau faktur pemasok. Merek dan nama usaha di contoh fiktif.

## Riwayat perubahan

Versi terkini: **1.0.0**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
