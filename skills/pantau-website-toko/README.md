# Pantau Website Toko: Tahu Duluan Sebelum Pelanggan yang Mengeluh

**Ketik "cek website saya masih hidup nggak", "SSL toko saya kapan habis?", atau "ringkas status website hari ini" — AI Anda langsung membacanya lewat Uptime Kuma (gratis, jalan di komputer sendiri) atau, tanpa pasang apa pun, cek sekali langsung ke alamat website Anda.** (SSL = sertifikat keamanan yang menampilkan gembok di browser.)

*Diuji AI penguji independen di OpenClaw: 3,0 → 8,7 dari 10 (pembeda: menolak memantau situs saingan dan tidak menjanjikan pemasangan alert yang tidak bisa dilakukan, sementara AI biasa siap "memasang automation"; ringkasan status memakai server Uptime Kuma tiruan).*

> Komunitech **tidak berafiliasi** dengan proyek Uptime Kuma. Uptime Kuma adalah software open-source (MIT) milik Louis Lam & komunitasnya; skill dan panduan ini adalah karya orisinal Komunitech untuk mempermudah pemakaiannya bagi pemilik usaha Indonesia.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan (opsional): Uptime Kuma (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu duluan, bukan dari komplain pelanggan.** Website/checkout/link WA mati ("down") biasanya baru ketahuan saat pelanggan sudah kesal — dengan Uptime Kuma + notifikasi Telegram, Anda bisa tahu dalam hitungan menit sesuai jarak pengecekan yang Anda atur (notifikasi Telegram belum diuji langsung).
- ✅ **Bukan cuma "hidup/mati".** Ringkasan menyebut uptime 24 jam (persentase waktu website hidup), berapa lama mati, dan sisa hari sertifikat SSL — angkanya dibaca dari Uptime Kuma dan dihitung skrip, bukan kira-kira. SSL kedaluwarsa berarti browser pelanggan menampilkan peringatan "Not Secure" yang menakuti calon pembeli.
- ✅ **Bisa mulai TANPA pasang apa pun.** Belum sempat pasang Uptime Kuma? Ketik "cek website saya" dan AI melakukan satu kali pengecekan (status HTTP, yaitu kode jawaban website seperti 200 = normal; waktu respons; sisa hari SSL) ke alamat Anda.
- ✅ **Daftar hal yang layak dipantau untuk toko online.** Bukan cuma beranda — halaman checkout, domain & SSL, link WA/katalog, form pesanan; daftarnya ada di panduan pemasangan.
- ✅ **Tanpa biaya langganan.** Uptime Kuma gratis, jalan di komputer/mini PC/server sewaan (VPS) milik Anda sendiri — bukan langganan layanan pemantau berbayar seperti UptimeRobot atau Pingdom.
- ✅ **Laporan otomatis ke Telegram** (lewat notifikasi bawaan Uptime Kuma saat website mati, atau jadwal ringkasan harian/mingguan lewat OpenClaw; keduanya belum diuji langsung).

## Cocok untuk siapa
- Pemilik toko online, landing page produk, atau link bio jualan (Shopee/Tokopedia + website sendiri, WA Business) yang belum punya cara tahu kalau situsnya down.
- UMKM yang checkout/form pesanannya lewat halaman/tools terpisah dari website utama — sering luput dipantau.
- Yang ingin mulai **gratis dan cepat** (cek sekali tanpa instalasi) sebelum memutuskan pasang pemantauan terus-menerus.

**Kurang cocok:** butuh pemantauan performa mendalam atau uji beban (di luar cakupan — ini murni hidup/mati + waktu respons + SSL); memantau website milik orang lain (skill ini menolak, hanya untuk situs milik/dikelola pengguna sendiri); belum punya komputer/mini PC/VPS yang bisa menyala terus untuk pemantauan berkelanjutan (cek sekali tetap bisa dipakai sesekali tanpa syarat itu).

## Contoh sebelum & sesudah
**Sebelum:** buka website manual dari HP untuk cek masih hidup, atau — lebih sering — baru sadar website mati setelah pelanggan chat WA "kak websitenya error". SSL kedaluwarsa ketahuan setelah calon pembeli screenshot peringatan "Not Secure" di browser mereka.

**Sesudah (dengan Uptime Kuma terpasang, cukup ketik):** *"Mas, Uptime Kuma toko aku udah dipasang sama teknisi, alamat status page nya http://127.0.0.1:3001/status/toko-kita . Tolong ringkasin dong kondisi website toko hari ini, ada yang down nggak, terus SSL nya kapan habis?"*
```
Udah aku cek status page toko-nya (Toko Scenario2) barusan, jam 15:08 WIB. Ini ringkasannya:

**1. Toko Online** (halaman utama)
- Sekarang: AKTIF ✅, respons 240 ms (normal)
- Uptime 24 jam terakhir: 95,0%
- Ada 1 kejadian TURUN di jendela data yang terbaca (26 Sep, 15:10–15:20 WIB), total 10 menit mati. Catatan: ini bukan rangkuman sehari penuh, cuma beberapa jam terakhir yang kebaca sistemnya.
- **SSL: tinggal 9 hari lagi** ⚠️ **SEGERA PERPANJANG** — ini yang paling perlu diperhatikan, kalau habis nanti pelanggan bisa lihat peringatan "Not Secure" di browser mereka.

**2. WA Katalog**
- Sekarang: AKTIF ✅, respons 82 ms
- Uptime 24 jam: 100% — bersih, gak ada yang down
- SSL: masih aman, 120 hari lagi
…
```
(Jawaban asli AI saat diuji di OpenClaw dengan server Uptime Kuma tiruan berisi data fiktif; dipotong. "Respons" = waktu website menjawab; "uptime" = persentase waktu website hidup.)

**Sesudah (belum pasang apa-apa, cukup ketik):** *"Cek website saya masih hidup nggak: https://tokosaya.contoh"*
```
CEK CEPAT: https://tokosaya.contoh
HTTP    : 200 (OK)
Respons : 86.7 ms
SSL     : 25 hari lagi (kedaluwarsa 2026-10-21)
```
(Contoh bentuk keluaran dengan alamat fiktif; angka hanya ilustrasi.)

## Cara pakai
Cukup ketik permintaan biasa ke AI agent Anda:
- "Cek website saya masih hidup nggak?"
- "SSL toko saya kapan habis?"
- "Ringkas status website hari ini" / "gimana status minggu ini?"
- "Tolong pasangkan pemantau website saya" (akan diarahkan ke panduan pasang)
- "Kirim ringkasan status website ke Telegram saya tiap pagi" (lewat OpenClaw; jadwal otomatis belum diuji langsung)

## Instalasi singkat
1. **Pilih jalur:** langsung pakai cek cepat (`cek-cepat`; tidak perlu instalasi apa pun, tapi harus diminta manual), atau pasang **Uptime Kuma** untuk pemantauan terus-menerus + notifikasi Telegram otomatis — ikuti `docs/panduan-uptime-kuma.md` di paket (±20–30 menit), atau **jasa setup Komunitech**.
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

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.9), skor 1–10: tanpa skill **3,0** → dengan skill **8,7** (LULUS). Jebakan pantau situs saingan tiap 5 detik: DENGAN skill, AI menolak dan mengarahkan cek sekali situs milik sendiri atau memandu Anda memasang Uptime Kuma sendiri; ringkasan uptime/SSL pada data contoh benar. Catatan jujur: uji OpenClaw memakai server Uptime Kuma tiruan; Uptime Kuma 2.5.5 asli diuji terpisah oleh penguji lain (`examples/HASIL-UJI.md`). Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-03; muat CLI) dan Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Notifikasi Telegram dari Uptime Kuma dan jadwal ringkasan otomatis belum diuji langsung. Software Uptime Kuma (MIT) — panduan `docs/panduan-uptime-kuma.md`; tidak berafiliasi dengan Louis Lam/Uptime Kuma.

## FAQ
**Apakah data website saya dikirim ke server Komunitech atau pihak lain?**
Tidak. Script ini hanya menghubungi Uptime Kuma **milik Anda sendiri** (biasanya di komputer yang sama, alamat `127.0.0.1`) atau website Anda sendiri langsung. Tidak ada data yang dikirim ke Komunitech; ringkasan hanya sampai ke Telegram bila Anda sendiri mengatur jadwal laporan ke Telegram.

**Bisakah saya pakai ini untuk memantau website kompetitor atau klien tanpa izin?**
Tidak — skill ini sengaja **menolak** dipakai untuk situs yang bukan milik/dikelola Anda sendiri, dan cek cepat tidak boleh dijadwalkan berulang cepat ke situs siapa pun (itu bisa dianggap membebani server orang lain).

**Saya belum punya komputer yang menyala 24 jam untuk Uptime Kuma, apa saya bisa mulai sekarang?**
Bisa — pakai cek cepat kapan saja tanpa instalasi apa pun. Untuk pemantauan otomatis terus-menerus (dengan notifikasi Telegram saat website mati), Uptime Kuma butuh komputer/mini PC/VPS yang menyala saat itu terjadi — lihat opsi mini PC murah atau jasa setup Komunitech di `docs/panduan-uptime-kuma.md`.

## Riwayat perubahan

Versi terkini: **1.0.9**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
