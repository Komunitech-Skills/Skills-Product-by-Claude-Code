# Orderan WA Beres: Rekap, Nota, Kirim

**Tempel chat pesanan pelanggan, dapatkan total yang dihitung rinci, pesan konfirmasi, nota, label paket, dan daftar serah-terima kurir dalam satu balasan.**

Diuji AI penguji independen di OpenClaw: 5,5 → 8,4 dari 10 (semua angka rupiah cocok dengan hitung ulang independen; pembedanya: tanpa skill AI mengarang harga untuk warna yang tidak ada dan mau membagikan alamat pelanggan ke grup reseller, dengan skill harga dan resi yang belum Anda beri ditandai, tidak dikarang).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Total dihitung, bukan dikira.** Barang × jumlah × harga, diskon, lalu ongkir dihitung otomatis, format rupiah rapi (Rp247.500). Pesanan yang tertempel dua kali hanya dihitung sekali.
- ✅ **Pesan untuk pelanggan siap kirim:** konfirmasi + cara bayar, pengingat bayar yang sopan, dan kabar "pesanan dikirim + resi". Data yang kurang (alamat, kode pos, HP) langsung ditanyakan di pesan yang sama.
- ✅ **Label paket & daftar serah-terima kurir** per JNE, J&T, SiCepat, AnterAja, Pos, GoSend/Grab, lengkap dengan penanda COD (bayar di tempat) atau bukan.
- ✅ **Rekap harian sekali lihat:** jumlah pesanan, omzet, barang terlaris, siapa yang belum bayar, plus tabel CSV (teks yang bisa ditempel ke Excel/Google Sheets).
- ✅ **Jujur dan menjaga privasi:** harga, ongkir, dan resi yang belum Anda berikan ditandai `[isian]`, tidak dikarang. Nomor HP & alamat pelanggan hanya dimasukkan ke label, tidak ke rekap harian atau CSV.

## Cocok untuk siapa
- Toko online kecil-menengah yang menerima pesanan lewat WhatsApp, DM Instagram/TikTok, atau Facebook.
- Reseller/dropshipper, katering, kue rumahan, fashion, kosmetik, oleh-oleh yang rekap order masih manual.
- Admin toko yang tiap sore harus menyiapkan paket untuk kurir.
- **Bukan untuk:** file ekspor marketplace (skill Picking List & Urutan Resi, `resi-picking`), invoice formal ber-PPN (skill Invoice & Kuitansi, `buat-invoice`), kasir toko fisik (skill Kasir Lokal, `kasir-lokal`), catatan stok (skill Buku Stok, `buku-stok`).

## Contoh sebelum & sesudah
**Sebelum** (uji OpenClaw tanpa skill, 2026-10-06): AI mengarang harga untuk warna yang tidak ada di katalog, mau membagikan alamat pelanggan ke grup reseller, dan menawarkan menghubungkan WhatsApp untuk mengirim sendiri.

**Sesudah:** satu tempelan chat 6 pelanggan (satu kirim dobel) langsung jadi konfirmasi, nota, label, daftar serah-terima per kurir, rekap harian (omzet Rp782.000, belum bayar Rp399.000) dan tabel CSV; semua angka cocok dengan hitung ulang, HP/alamat tidak masuk rekap. Cuplikan salah satu pesan konfirmasi (dipotong; hasil asli uji OpenClaw otomatis, 6 Okt 2026, data fiktif, dari `examples/01-normal-6-pelanggan.md`):

```
Halo Kak Rina, terima kasih sudah order di Nayla Hijab 🙏
Pesanan yang tadi pagi sudah kami terima ya, tidak perlu dikirim ulang 😊

20261006-01
• Pashmina Ceruty Babydoll Mocca x2 = Rp90.000
• Pashmina Ceruty Babydoll Dusty Pink x1 = Rp45.000
• Bros Mutiara x3 = Rp30.000
Subtotal: Rp165.000
Ongkir JNE REG: Rp12.000
*Total: Rp177.000*

Pembayaran via transfer ke:
BCA 1234567890 a.n. Nayla Putri
Mohon transfer sesuai total, lalu kirim bukti transfernya di chat ini ya, Kak.
…
```

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

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 6 Okt 2026 (v1.0.0), penguji independen: rata-rata nilai 5,5 tanpa skill menjadi 8,4 dengan skill (skala 10), dari empat skenario (lima kali uji): tempelan chat 6 pelanggan (dijalankan dua kali: biasa dan dengan pengaturan seperti bot Telegram), diskon + DP + pengingat bayar, pesan kurang lengkap, dan jebakan (kirim otomatis dari WA, cek m-banking, bagikan alamat ke reseller). Semua angka rupiah di jawaban dengan skill dicocokkan dengan hitung ulang independen. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Pada uji dengan pengaturan Telegram (5,5 → 7,5), nota pesanan ke-2 dan seterusnya sempat disingkat "sama format di atas"; ini diperbaiki di v1.0.1. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

## Bukti uji di bot Telegram

Diuji di bot Telegram uji (bot OpenClaw asli di grup uji internal Komunitech), 12 Okt 2026, satu skenario dengan topik lain, pesan yang sama tanpa skill lalu dengan skill:
- Tanpa skill: skor 7,5
- Dengan skill: skor 8,5
Selisihnya tipis (+1,0). Tanpa skill AI sudah menolak aksi berisiko (cek mutasi bank, kirim WA otomatis, bagikan alamat) dengan angka nota yang benar. Dengan skill ditambah nomor pesanan, nota, label, rekap tanpa nomor HP/alamat yang aman untuk grup reseller, dan CSV. Jadi di bot Telegram keunggulan skill ini lebih kecil daripada angka uji OpenClaw di atas.

## FAQ
**Bisakah langsung mengirim konfirmasi ke semua pelanggan dari WhatsApp saya?**
Tidak. Mengirim otomatis dari WhatsApp pribadi berisiko nomor diblokir dan salah kirim. Anda mendapat draf per pelanggan yang tinggal disalin dan dikirim.

**Bisakah mengecek apakah pelanggan sudah transfer?**
Tidak masuk ke m-banking. Cek mutasi sendiri, lalu tempel "yang sudah bayar: Kak Dina, Pak Bowo"; status dan rekap langsung diperbarui.

**Ongkirnya dihitung otomatis?**
Tarif kurir berubah dan bergantung berat serta rute, jadi tidak ditebak. Tempel ongkir dari aplikasi kurir (atau tarif per kota yang biasa Anda pakai), lalu total dihitung rinci per baris.

## Catatan
Nota yang dihasilkan bukan faktur pajak. Karya orisinal Komunitech; nama kurir dan bank hanya disebut sebagai penyebut layanan dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
