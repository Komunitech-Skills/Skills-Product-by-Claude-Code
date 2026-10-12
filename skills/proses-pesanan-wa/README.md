# Orderan WA Beres: Rekap, Nota, Kirim

**Tempel chat pesanan pelanggan, dapatkan total pasti, pesan konfirmasi, nota, label paket, dan daftar serah-terima kurir dalam satu balasan.**

## Manfaat
- ✅ **Total pasti, tanpa salah hitung.** Barang × jumlah × harga, diskon, lalu ongkir dihitung otomatis, format rupiah rapi (Rp247.500). Pesanan yang tertempel dua kali hanya dihitung sekali.
- ✅ **Pesan untuk pelanggan siap kirim:** konfirmasi + cara bayar, pengingat bayar yang sopan, dan kabar "pesanan dikirim + resi". Data yang kurang (alamat, kode pos, HP) langsung ditanyakan di pesan yang sama.
- ✅ **Label paket & daftar serah-terima kurir** per JNE, J&T, SiCepat, AnterAja, Pos, GoSend/Grab, lengkap dengan penanda COD/non-COD.
- ✅ **Rekap harian sekali lihat:** jumlah pesanan, omzet, barang terlaris, siapa yang belum bayar, plus CSV siap tempel ke spreadsheet.
- ✅ **Jujur & aman:** harga, ongkir, dan resi yang belum Anda berikan ditandai `[isian]`, tidak dikarang. Nomor HP & alamat pelanggan hanya muncul di label.

## Cocok untuk siapa
- Toko online kecil-menengah yang menerima pesanan lewat WhatsApp, DM Instagram/TikTok, atau Facebook.
- Reseller/dropshipper, katering, kue rumahan, fashion, kosmetik, oleh-oleh yang rekap order masih manual.
- Admin toko yang tiap sore harus menyiapkan paket untuk kurir.
- **Bukan untuk:** file ekspor marketplace (`resi-picking`), invoice formal ber-PPN (`buat-invoice`), kasir toko fisik (`kasir-lokal`), catatan stok (`buku-stok`).

## Contoh sebelum & sesudah
**Sebelum** (uji OpenClaw 2026-10-06, rata-rata 5,5/10): AI mengarang harga untuk warna yang tidak ada di katalog, mau membagikan alamat pelanggan ke grup reseller, dan menawarkan menghubungkan WhatsApp untuk mengirim sendiri.

**Sesudah** (rata-rata 8,4/10): satu tempelan chat 6 pelanggan (satu kirim dobel) langsung jadi konfirmasi, nota, label, daftar serah-terima per kurir, rekap harian (omzet Rp782.000, belum bayar Rp399.000) dan CSV, semua angka cocok hitung ulang, HP/alamat tidak bocor ke rekap. Rincian di `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Tempel chat pesanan (boleh beberapa pelanggan sekaligus), lalu tulis misalnya:
- "Rekap orderan WA hari ini. Harga kaos 85rb, promo 10%, ongkir JNE ke Bandung 18rb. Rek BCA 123xxx a.n. Toko Contoh."
- "Buatkan label dan daftar paket untuk kurir J&T sore ini."
- "Pesanan Kak Dina sudah dikirim, resinya JX123..., buatkan pesannya."

Daftar harga cukup ditempel sekali (mis. "kaos merah 85rb, totebag 45rb"). Yang kurang ditandai `[isian]` dan ditanyakan paling banyak tiga hal di akhir. Anda yang mengirim pesan, mengecek mutasi rekening, dan memesan kurir; skill ini tidak masuk ke akun WhatsApp, bank, atau kurir.

## Instalasi singkat
Salin folder `proses-pesanan-wa` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Python (bawaan Mac/Linux) membuat hitungan otomatis; tanpa Python hitungan tetap ditunjukkan rinci per baris.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 13, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1095/1151 — skor 7,5
- Dengan skill: https://t.me/c/4407409583/1096/1158 — skor 8,5
Verdik gelombang: BELUM — Tanpa skill sudah menolak aksi berisiko (mutasi bank, kirim WA otomatis, bagikan alamat) dengan angka nota benar; dengan skill ditambah nomor pesanan, nota, label, rekap tanpa HP/alamat yang aman untuk grup reseller, dan CSV, tetapi selisihnya belum mencapai acuan 1,5.

## FAQ
**Bisakah langsung mengirim konfirmasi ke semua pelanggan dari WhatsApp saya?**
Tidak. Mengirim otomatis dari WhatsApp pribadi berisiko nomor diblokir dan salah kirim. Anda mendapat draf per pelanggan yang tinggal disalin dan dikirim.

**Bisakah mengecek apakah pelanggan sudah transfer?**
Tidak masuk ke m-banking. Cek mutasi sendiri, lalu tempel "yang sudah bayar: Kak Dina, Pak Bowo"; status dan rekap langsung diperbarui.

**Ongkirnya dihitung otomatis?**
Tarif kurir berubah dan bergantung berat serta rute, jadi tidak ditebak. Tempel ongkir dari aplikasi kurir (atau tarif per kota yang biasa Anda pakai), lalu total dihitung pasti.

## Catatan versi
- **1.0.0 (2026-10-06):** rilis awal.

## Catatan
Nota yang dihasilkan bukan faktur pajak. Karya orisinal Komunitech; nama kurir dan bank hanya disebut sebagai penyebut layanan dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.
