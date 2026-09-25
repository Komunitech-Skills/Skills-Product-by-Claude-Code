# Skenario 03 (normal) — Konsultan pajak freelancer, referral teman, bahasa formal, beda zona waktu

> Uji independen Tahap 6 (2026-09-25). Nama & nomor fiktif.

## Permintaan pengguna
> "Saya Dewi Anggraini, konsultan pajak independen di Jakarta, bersertifikat Brevet A & B. Teman saya Pak Hendra Wijaya merekomendasikan saya ke Pak Surya, pemilik CV Surya Bahari (distributor di Makassar), katanya lagi cari pendamping pajak bulanan dan SPT Tahunan badan menjelang Coretax. Pak Hendra sudah izinkan namanya disebut. Nomor Pak Surya 62 811-4455-6677. Tolong buatkan pesan WA pembuka yang formal. Rencananya saya kirim malam ini jam 19.30."

## Langkah yang dijalankan agent
1. Cakupan: pesan pertama, referral → lanjut.
2. Asal kontak: referral dengan izin eksplisit menyebut nama (sesuai pola #1 & larangan "mengaku direkomendasikan tanpa izin" di `dasar-hukum-wa.md` §2) → sah.
3. Nada formal: "Bapak", "berkenan", tanpa "ya/Kak".
4. Domain pajak: pesan murni perkenalan jasa; tidak menjanjikan hasil pajak, tidak memberi hitungan/nasihat.
5. **Zona waktu:** penerima di Makassar = **WITA (WIB+1)**. 19.30 WIB = **20.30 WITA** → di luar 08.00–20.00 setempat. Agent pertama memasukkan `--jam-kirim 19.30` → script menolak: `format --jam-kirim harus HH:MM (24 jam), diberi '19.30'` (format titik khas Indonesia tidak diterima — temuan B4). Lalu dijalankan `--jam-kirim 20:30` (jam setempat penerima) → peringatan "di luar rentang wajar". Script sendiri tidak tahu zona waktu; konversi dilakukan agent.
6. Script menandai **PPN, SPT** sebagai "kata huruf kapital semua (terkesan teriak)" → false positive; singkatan pajak wajar di pesan konsultan pajak (temuan B3).

---

## Output ke pengguna

### Ringkasan konteks
Penerima: Bapak Surya, pemilik CV Surya Bahari (Makassar, **WITA**). Asal kontak: rekomendasi Bapak Hendra Wijaya (sudah mengizinkan namanya disebut). Ditawarkan: pendampingan pajak bulanan & SPT Tahunan badan.

### Varian 1 — Singkat
```
Selamat siang, Bapak Surya. Saya Dewi Anggraini, konsultan pajak independen, mendapat nomor Bapak dari Bapak Hendra Wijaya atas rekomendasi beliau. Apakah Bapak berkenan saya kirimkan ringkasan layanan pendampingan pajak untuk CV? Mohon maaf bila mengganggu, pesan ini boleh diabaikan bila belum relevan.
```
Script (jam 09:30 WITA): 304 karakter, 42 kata, asal kontak ✔, opsi keluar ✔ → **[OK]**

### Varian 2 — Sedang
```
Selamat siang, Bapak Surya. Perkenalkan, saya Dewi Anggraini, konsultan pajak independen di Jakarta.
Saya mendapat nomor Bapak dari Bapak Hendra Wijaya, yang menyampaikan bahwa CV Surya Bahari sedang mencari pendamping untuk urusan pajak bulanan dan SPT Tahunan badan.
Saya membantu pelaporan PPN, PPh, dan SPT untuk usaha distribusi skala menengah.
Apakah Bapak berkenan saya kirimkan ringkasan layanan dan biayanya? Mohon maaf bila mengganggu, dan boleh diabaikan bila belum relevan.
```
Script: 485 karakter, 69 kata → **[PERIKSA DULU]** "Kata huruf kapital semua terdeteksi: PPN, SPT". Penilaian manual agent: ini singkatan resmi perpajakan, bukan teriakan — aman dibiarkan.

### Varian 3 — Dengan nilai tambah
```
Selamat siang, Bapak Surya. Saya Dewi Anggraini, konsultan pajak independen di Jakarta, mendapat nomor Bapak dari Bapak Hendra Wijaya.
Beliau menyampaikan CV Surya Bahari sedang mencari pendamping pajak bulanan menjelang pelaporan lewat Coretax.
Saya bersertifikat Brevet A dan B, dan saat ini mendampingi pelaporan PPN serta PPh beberapa usaha distribusi, termasuk dari luar Jawa secara daring.
Bila Bapak berkenan, saya dapat mengirimkan ringkasan layanan dan kisaran biaya terlebih dahulu.
Mohon maaf bila mengganggu, pesan ini boleh diabaikan bila belum relevan. Terima kasih atas waktunya.
```
Script: 594 karakter, 84 kata → **[PERIKSA DULU]** panjang > 500; kapital "PPN". Penilaian: panjang masih wajar untuk jasa profesional formal; singkatan aman.
⚠️ Kalimat "mendampingi … usaha distribusi, termasuk dari luar Jawa secara daring" **harus benar**; hapus bila Ibu belum pernah punya klien seperti itu (skill melarang mengarang bukti).

### Tautan WhatsApp (varian 1)
```
https://wa.me/6281144556677?text=Selamat%20siang%2C%20Bapak%20Surya.%20Saya%20Dewi%20Anggraini%2C%20konsultan%20pajak%20independen%2C%20mendapat%20nomor%20Bapak%20dari%20Bapak%20Hendra%20Wijaya%20atas%20rekomendasi%20beliau.%20Apakah%20Bapak%20berkenan%20saya%20kirimkan%20ringkasan%20layanan%20pendampingan%20pajak%20untuk%20CV%3F%20Mohon%20maaf%20bila%20mengganggu%2C%20pesan%20ini%20boleh%20diabaikan%20bila%20belum%20relevan.
```
Nomor `62 811-4455-6677` → `6281144556677` (diverifikasi manual).

### Saran jam kirim
**Jangan kirim jam 19.30 WIB malam ini** — itu 20.30 WITA di Makassar, sudah lewat batas wajar 20.00 waktu setempat penerima. Kirim besok **08.30–11.00 WIB (09.30–12.00 WITA)** di jam kerja.

### Checklist anti-blokir
- [x] Referral dengan izin eksplisit
- [x] Nama perekomendasi & identitas pengirim jelas
- [x] Opsi keluar sopan, tanpa link/emoji
- [ ] Kabari Pak Hendra bahwa Ibu sudah menghubungi Pak Surya (sopan & menambah kepercayaan)
- [ ] Jika belum dibalas → `follow-up-prospek`, bukan kirim ulang

### Asumsi
- Pesan ini perkenalan jasa, **bukan nasihat pajak**; jangan menjanjikan penghematan pajak di pesan pertama.
