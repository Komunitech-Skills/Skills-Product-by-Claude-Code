# Pantau Website Toko: Tahu Duluan Sebelum Pelanggan yang Mengeluh

**Ketik "cek website saya masih hidup nggak", "SSL toko saya kapan habis?", atau "ringkas status website hari ini" — AI Anda langsung membacanya lewat Uptime Kuma (gratis, jalan di komputer sendiri) atau, tanpa pasang apa pun, cek sekali langsung ke alamat website Anda.**

> Komunitech **tidak berafiliasi** dengan proyek Uptime Kuma. Uptime Kuma adalah software open-source (MIT) milik Louis Lam & komunitasnya; skill dan panduan ini adalah karya orisinal Komunitech untuk mempermudah pemakaiannya bagi pemilik usaha Indonesia.

## Manfaat
- ✅ **Tahu duluan, bukan dari komplain pelanggan.** Website/checkout/link WA down biasanya baru ketahuan saat pelanggan sudah kesal — dengan Uptime Kuma + notifikasi Telegram, Anda tahu dalam hitungan menit.
- ✅ **Bukan cuma "hidup/mati".** Ringkasan menyebut uptime 24 jam, berapa lama down, dan sisa hari sertifikat SSL — dihitung dari data asli, bukan kira-kira. SSL kedaluwarsa berarti browser pelanggan menampilkan peringatan "Not Secure" yang menakuti calon pembeli.
- ✅ **Bisa mulai TANPA pasang apa pun.** Belum sempat pasang Uptime Kuma? Ketik "cek website saya" dan AI langsung melakukan satu kali pengecekan (status HTTP, waktu respons, sisa hari SSL) ke alamat Anda.
- ✅ **Daftar monitor yang memang penting untuk toko online.** Bukan cuma beranda — halaman checkout, domain & SSL, link WA/katalog, form pesanan, semua ada di panduan pasangnya.
- ✅ **Tanpa biaya bulanan.** Uptime Kuma gratis selamanya, jalan di komputer/mini PC/VPS Anda sendiri — bukan langganan UptimeRobot/Pingdom Pro.
- ✅ **Laporan otomatis ke Telegram** (lewat notifikasi bawaan Uptime Kuma saat down, atau jadwal ringkasan harian/mingguan lewat OpenClaw).

## Cocok untuk siapa
- Pemilik toko online, landing page produk, atau link bio jualan (Shopee/Tokopedia + website sendiri, WA Business) yang belum punya cara tahu kalau situsnya down.
- UMKM yang checkout/form pesanannya lewat halaman/tools terpisah dari website utama — sering luput dipantau.
- Yang ingin mulai **gratis dan cepat** (mode `cek-cepat` tanpa instalasi) sebelum memutuskan pasang pemantauan terus-menerus.

**Kurang cocok:** butuh pemantauan performa mendalam/load testing (di luar cakupan — ini murni hidup/mati + respons + SSL); memantau website milik orang lain (skill ini menolak, hanya untuk situs milik/dikelola pengguna sendiri); belum punya komputer/mini PC/VPS yang bisa menyala terus untuk pemantauan berkelanjutan (mode `cek-cepat` tetap bisa dipakai sesekali tanpa syarat itu).

## Contoh sebelum & sesudah
**Sebelum:** buka website manual dari HP untuk cek masih hidup, atau — lebih sering — baru sadar down setelah pelanggan chat WA "kak websitenya error". SSL kedaluwarsa ketahuan setelah calon pembeli screenshot peringatan "Not Secure" di browser mereka.

**Sesudah (dengan Uptime Kuma terpasang, cukup ketik):** *"Ringkas status website toko saya"*
```
RINGKASAN STATUS - Toko Saya (toko-saya)
Diperiksa: 2026-09-26T09:00:12+00:00 UTC
------------------------------------------------------------
[OK] Toko Online  (grup: Utama)
     Status sekarang : AKTIF, ping 210 ms
     Uptime 24 jam   : 95.0% (dihitung Uptime Kuma sendiri)
     Terlihat TURUN dalam 5 cek terakhir yang terbaca (08:00-08:20 UTC): 2x, total 10.0 menit
     Sertifikat SSL  : 9 hari lagi  <-- SEGERA PERPANJANG
```
(Contoh nyata dari uji dengan Uptime Kuma 2.5.5 asli + data uji Komunitech, lihat `examples/`.)

**Sesudah (belum pasang apa-apa, cukup ketik):** *"Cek website saya masih hidup nggak: https://tokosaya.contoh"*
```
CEK CEPAT: https://tokosaya.contoh
HTTP    : 200 (OK)
Respons : 86.7 ms
SSL     : 25 hari lagi (kedaluwarsa 2026-10-21)
```

## Cara pakai
Cukup ketik permintaan biasa ke AI agent Anda:
- "Cek website saya masih hidup nggak?"
- "SSL toko saya kapan habis?"
- "Ringkas status website hari ini" / "gimana status minggu ini?"
- "Tolong pasangkan pemantau website saya" (akan diarahkan ke panduan pasang)
- "Kirim ringkasan status website ke Telegram saya tiap pagi" (lewat OpenClaw)

## Instalasi singkat
1. **Pilih jalur:** langsung pakai `cek-cepat` (tidak perlu instalasi apa pun, tapi harus diminta manual), atau pasang **Uptime Kuma** untuk pemantauan terus-menerus + notifikasi Telegram otomatis — ikuti `docs/panduan-uptime-kuma.md` di paket (±20–30 menit), atau **jasa setup Komunitech**.
2. Salin folder `pantau-website-toko` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Rincian & verifikasi lokasi instalasi ada di `docs/instalasi.md`.)

3. Bila memakai Uptime Kuma: catat alamat status page Anda (bentuk `http://ALAMAT:PORT/status/NAMA-SLUG`, dari `docs/panduan-uptime-kuma.md` §5) — tidak ada token/API key yang perlu disiapkan.
4. Coba: "Cek website saya masih hidup nggak?" atau "Ringkas status website toko saya."

## Catatan revisi 1.0.8 (2026-10-03)

- `description` kini memuat batas keras (tidak memasang Uptime Kuma/alert, tidak mengecek situs pesaing, termasuk cek sekali) beserta kata pemicu, karena model sering menjawab tanpa membuka SKILL.md; ditambah "ATURAN WAJIB" di awal SKILL.md.

## Catatan revisi 1.0.7 (2026-10-01)

- Kata pemicu ditambah di description ("kabari ke WA kalau web down", "pasang alert website", "pantau/cek website saingan atau kompetitor") agar skill terbaca pada permintaan jebakan; uji ulang putaran 2 menunjukkan agent tidak membaca SKILL.md di skenario itu.

## Catatan revisi 1.0.6 (2026-10-01)
- Batas layanan dipertegas di bagian paling awal skill dan di deskripsinya: AI tidak memasang Uptime Kuma, monitor, maupun alert WA/notifikasi — dipasang Anda sendiri (dipandu) atau lewat jasa setup Komunitech; notifikasi resmi lewat Telegram.
- Kalimat baku penolakan untuk permintaan memantau website pesaing/orang lain, tanpa tawaran cek terjadwal ke situs mereka.
- Contoh balasan yang benar ditambahkan di `examples/10-contoh-balasan-pantau-saingan-dan-minta-pasang.md`.

## Catatan revisi 1.0.5 (2026-10-01)
- Ringkasan kini menghitung **kejadian** down (beberapa cek gagal berurutan = 1 kejadian) lengkap dengan jam mulai–selesai (WIB) dan durasinya — tidak lagi "turun 5x" yang membingungkan.
- Angka menit & persen disampaikan persis seperti hasil script.
- Batas layanan diperjelas: AI tidak memasang Uptime Kuma atau notifikasi untuk Anda; pemasangan dilakukan sendiri (dipandu) atau lewat jasa setup Komunitech. Notifikasi resmi lewat Telegram; WhatsApp hanya dengan nomor terpisah sesuai kebijakan Komunitech.

## FAQ
**Apakah data website saya dikirim ke server Komunitech atau pihak lain?**
Tidak. Script ini hanya menghubungi Uptime Kuma **milik Anda sendiri** (biasanya `127.0.0.1`) atau website Anda sendiri langsung. Tidak ada data yang dikirim ke Komunitech, kecuali Anda sendiri mengatur jadwal laporan ke Telegram.

**Bisakah saya pakai ini untuk memantau website kompetitor atau klien tanpa izin?**
Tidak — skill ini sengaja **menolak** dipakai untuk situs yang bukan milik/dikelola Anda sendiri, dan `cek-cepat` tidak boleh dijadwalkan berulang cepat ke situs siapa pun (itu bisa dianggap membebani server orang lain).

**Saya belum punya komputer yang menyala 24 jam untuk Uptime Kuma, apa saya bisa mulai sekarang?**
Bisa — pakai `cek-cepat` kapan saja tanpa instalasi apa pun. Untuk pemantauan otomatis terus-menerus (dengan notifikasi Telegram saat down), Uptime Kuma butuh komputer/mini PC/VPS yang menyala saat itu terjadi — lihat opsi mini PC murah atau jasa setup Komunitech di `docs/panduan-uptime-kuma.md`.
