# Pilihan Isi per Jenis Usaha

Dipakai agent untuk **menyarankan** isi yang lazim, lalu **dikonfirmasi** ke pengguna. Jangan menulis nama penyedia (kurir, payment gateway, cloud) yang tidak disebut pengguna — pakai `[isi: ...]` dan beri contoh di tanda kurung.

## 1. Toko online (website sendiri: WooCommerce/Shopify/landing page + checkout)
- **Data umum:** nama, no. WA/HP, email, alamat kirim, riwayat pesanan, bukti transfer; data otomatis (IP, perangkat, cookie).
- **Penerima umum:** kurir/agregator ongkir, payment gateway, penyedia hosting/toko online, email marketing, piksel iklan (Meta/Google/TikTok).
- **Transfer LN:** hampir pasti ada bila memakai Shopify, Google, Meta, Mailchimp, Cloudflare → pakai opsi 5(a).
- **Cookie/piksel:** wajib bagian 10. Tawarkan banner persetujuan cookie non-esensial.
- **PSE:** website yang melayani transaksi mungkin wajib daftar PSE Lingkup Privat → sarankan cek pse.komdigi.go.id.

## 2. Penjual marketplace (Shopee, Tokopedia/TikTok Shop, Lazada, dll.)
- Marketplace punya kebijakan privasi sendiri untuk data di platformnya. Kebijakan usaha diperlukan bila penjual **menyimpan/memakai data di luar platform** (mis. menyalin nomor pembeli ke WA, spreadsheet, grup reseller, promo ulang).
- Ingatkan: memakai data pembeli marketplace untuk promo di luar platform bisa melanggar ketentuan marketplace dan butuh dasar sah/persetujuan.

## 3. Akun WhatsApp Business / jualan lewat chat
- **Data:** nama profil, nomor WA, isi chat, alamat, bukti transfer, label pelanggan, katalog pesanan.
- **Penerima:** Meta/WhatsApp (server di luar Indonesia), kurir, bank/e-wallet, **AI agent/chatbot** bila memakai (sebutkan jujur bahwa balasan dapat dibantu AI).
- Pakai template "B" di `templates/pemberitahuan-persetujuan.md` sebagai pesan salam. Tanpa broadcast/blast ke nomor yang tidak setuju.
- Kebijakan privasi bisa ditaruh di tautan (Google Docs/Notion/website) dan dicantumkan di profil bisnis.

## 4. Aplikasi (Android/iOS/web app)
- **Data:** akun (email, no. HP, kata sandi ter-hash), data perangkat, lokasi (bila perlu), izin kamera/kontak/galeri, data penggunaan, notifikasi push, log crash.
- **Wajib tambahan:** jelaskan setiap **izin perangkat** dan alasannya; cara **hapus akun** (toko aplikasi umumnya mensyaratkan); SDK pihak ketiga (analytics, crash reporting, iklan).
- Hindari "mengakses semua data di perangkat Anda" (minimisasi).
- Bila ada fitur untuk anak → bagian data anak + persetujuan orang tua. Pertimbangkan konsultan hukum.

## 5. Klinik / praktik kesehatan / jasa kecantikan / psikolog / apotek
- **Data spesifik:** keluhan, diagnosis, riwayat alergi, hasil lab, foto sebelum/sesudah, resep → **data pribadi spesifik** (Ps. 4 ayat (2)).
- Wajib: persetujuan eksplisit terpisah (template D), akses terbatas, tidak untuk promosi tanpa persetujuan terpisah, foto tanpa wajah bila untuk konten.
- Masa simpan rekam medis mengikuti aturan kesehatan (Permenkes 24/2022 Ps. 39 menyebut ≥ 25 tahun untuk RME — cocokkan dengan aturan terbaru).
- Pertimbangkan DPO bila pemrosesan skala besar (Ps. 53 + Putusan MK 151/PUU-XXII/2024) dan DPIA (Ps. 34). **Sarankan konsultan hukum kesehatan.**
- Skill ini tidak membuat informed consent tindakan medis.

## 6. Jasa lain (kursus/les, event organizer, travel, properti, jasa keuangan kecil, HR/rekrutmen)
- **Kursus/les anak:** data anak → persetujuan orang tua/wali; foto kegiatan butuh izin terpisah.
- **Travel/umrah:** paspor, KTP, data kesehatan (vaksin) → data spesifik & transfer LN (maskapai, hotel luar negeri) → persetujuan.
- **Rekrutmen:** CV, riwayat pendidikan, gaji → masa simpan pelamar yang tidak diterima (mis. 6–12 bulan, dengan persetujuan bila disimpan untuk lowongan berikutnya).
- **Koperasi/simpan pinjam/jasa keuangan:** data keuangan = spesifik; ada aturan OJK/sektor → **rujuk konsultan hukum**, skill hanya membuat draf awal.

## Masa simpan: saran default (tandai sebagai saran, konfirmasi ke pengguna)
| Data | Saran | Dasar |
|---|---|---|
| Catatan transaksi/faktur | 10 tahun | UU KUP Ps. 28 ayat (11) |
| Chat CS tanpa transaksi | 1 tahun sejak chat terakhir | kebijakan usaha (minimisasi) |
| Daftar promo/newsletter | sampai persetujuan ditarik | UU PDP Ps. 40 |
| Data pelamar tidak diterima | 6–12 bulan | kebijakan usaha |
| Rekam medis | ikuti aturan kesehatan (≥ 25 th untuk RME fasyankes) | Permenkes 24/2022 Ps. 39 — PERLU REVIEW |
| Log website/analitik | 12–26 bulan (ikuti pengaturan penyedia) | kebijakan usaha |
