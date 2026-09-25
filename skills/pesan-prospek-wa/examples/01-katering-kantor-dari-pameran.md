# Skenario 01 (normal) — Katering kantor, kontak dari pameran → HRD perusahaan

> Uji independen Tahap 6 (2026-09-25). Penguji = agent terpisah dari pembuat skill, hanya membaca folder `pesan-prospek-wa/`. Script dijalankan dari salinan di scratchpad (bukan `.claude/skills`). Nama orang/usaha/nomor di bawah fiktif.

## Permintaan pengguna
> "Pak, saya Rudi, punya usaha katering 'Dapur Bu Ratna Catering' di Bekasi. Sabtu kemarin di Jakarta Food & Franchise Expo JIExpo saya tukeran kartu nama sama Bu Maya, HRD PT Sinar Logistik Nusantara di Cikarang. Dia cerita karyawannya (sekitar 120 orang) bosen sama menu kantin. Kami udah pegang makan siang 3 pabrik di Cikarang. Nomornya 0813-1234-5678. Tolong bikinin chat WA pertamanya, mau saya kirim besok jam 10 pagi."

## Langkah yang dijalankan agent
1. **Cek cakupan:** pesan pertama, satu prospek, belum pernah dihubungi → lanjut.
2. **Asal kontak:** pameran + tukar kartu nama langsung → sah (`references/dasar-hukum-wa.md` §1: kartu nama yang diberikan langsung).
3. **Pola pembuka:** #2 Pameran (`references/pola-pembuka.md`), dikaitkan ke hal yang benar-benar dibicarakan (menu kantin membosankan).
4. **Bukti:** hanya "3 pabrik di Cikarang" (diberikan pengguna). Tidak menambah testimoni/angka lain.
5. **Cek script** tiap varian (`cek --file ... --jam-kirim 10:00`). Varian 1 awal kena peringatan kalimat 29 kata → diperbaiki dulu sebelum ditampilkan (sesuai Langkah 6).
6. **Tautan wa.me** dibuat dari varian 2.

---

## Output ke pengguna

### Ringkasan konteks
Penerima: Bu Maya (HRD, PT Sinar Logistik Nusantara, Cikarang). Asal kontak: tukar kartu nama di Jakarta Food & Franchise Expo, JIExpo (Sabtu lalu). Ditawarkan: katering makan siang karyawan harian, menu berganti tiap minggu. B2B → sapaan "Bu".

### Varian 1 — Singkat
```
Selamat siang, Bu Maya. Saya Rudi dari Dapur Bu Ratna Catering, dapat kontak Ibu dari pameran Jakarta Food & Franchise Expo di JIExpo Sabtu lalu. Boleh saya kirim contoh menu makan siang karyawan? Boleh diabaikan bila belum relevan ya, Bu.
```
Hasil script: 239 karakter, 40 kata, asal kontak ✔, opsi keluar ✔, jam 10:00 wajar ✔ → **[OK]**

### Varian 2 — Sedang
```
Selamat siang, Bu Maya. Perkenalkan saya Rudi dari Dapur Bu Ratna Catering.
Saya dapat kontak Ibu dari pameran Jakarta Food & Franchise Expo di JIExpo Sabtu lalu, saat kita sempat mengobrol di booth kami.
Ibu sempat cerita karyawan mulai bosan dengan menu kantin, dan kami menyediakan katering makan siang harian dengan menu berganti tiap minggu.
Boleh saya kirim contoh menu 2 minggu beserta harganya? Mohon maaf mengganggu, dan boleh diabaikan bila tidak relevan, Bu.
```
Hasil script: 469 karakter, 74 kata, 4 baris, asal kontak ✔, opsi keluar ✔ → **[OK]**

### Varian 3 — Dengan nilai tambah
```
Selamat siang, Bu Maya. Saya Rudi dari Dapur Bu Ratna Catering, dapat kontak Ibu dari pameran Jakarta Food & Franchise Expo di JIExpo Sabtu lalu.
Waktu itu Ibu cerita karyawan PT Sinar Logistik Nusantara mulai bosan dengan menu kantin.
Kami menyiapkan makan siang harian untuk 3 pabrik di Cikarang, menu berganti tiap minggu dan diantar sebelum jam istirahat.
Kalau Ibu terbuka, boleh saya kirim contoh menu 2 minggu dan simulasi harga untuk 120 porsi?
Boleh diabaikan bila belum relevan, Bu. Terima kasih.
```
Hasil script: 506 karakter, 82 kata → **[PERIKSA DULU] 1 hal:** "Pesan 506 karakter — di atas 500, mungkin perlu scroll di layar HP. Masih boleh, tapi cek dulu." Penilaian agent: masih wajar untuk varian nilai tambah (hanya lewat 6 karakter); draf awal 602 karakter sudah dipangkas.

### Tautan WhatsApp (varian 2)
```
https://wa.me/6281312345678?text=Selamat%20siang%2C%20Bu%20Maya.%20Perkenalkan%20saya%20Rudi%20dari%20Dapur%20Bu%20Ratna%20Catering.%0ASaya%20dapat%20kontak%20Ibu%20dari%20pameran%20Jakarta%20Food%20%26%20Franchise%20Expo%20di%20JIExpo%20Sabtu%20lalu%2C%20saat%20kita%20sempat%20mengobrol%20di%20booth%20kami.%0AIbu%20sempat%20cerita%20karyawan%20mulai%20bosan%20dengan%20menu%20kantin%2C%20dan%20kami%20menyediakan%20katering%20makan%20siang%20harian%20dengan%20menu%20berganti%20tiap%20minggu.%0ABoleh%20saya%20kirim%20contoh%20menu%202%20minggu%20beserta%20harganya%3F%20Mohon%20maaf%20mengganggu%2C%20dan%20boleh%20diabaikan%20bila%20tidak%20relevan%2C%20Bu.
```
Klik tautan ini dari HP/WA Web, periksa teksnya, lalu **tekan kirim sendiri** (tidak dikirim otomatis). Verifikasi penguji: `urllib.parse.parse_qs` mengembalikan teks identik dengan varian 2.

### Saran jam kirim
Cikarang = WIB. Rencana jam 10.00 WIB sudah dalam rentang 08.00–20.00. Untuk HRD, hari kerja jam 09.00–11.00 atau 13.00–15.00 paling wajar; hindari jam istirahat 12.00–13.00.

### Checklist anti-blokir
- [x] Nomor dari kartu nama yang diberikan langsung (sah)
- [x] Menyebut asal kontak (pameran + waktu)
- [x] Ada opsi keluar sopan
- [ ] Pastikan foto profil & nama WA kamu jelas "Rudi – Dapur Bu Ratna Catering"
- [x] Tanpa link, tanpa huruf kapital berlebihan, tanpa emoji
- [ ] Satu pesan saja; kalau belum dibalas beberapa hari, pakai skill `follow-up-prospek`, jangan kirim variasi lain

### Asumsi
- Nama "Jakarta Food & Franchise Expo JIExpo" dan "Sabtu lalu" dipakai persis dari cerita pengguna.
- "Simulasi harga untuk 120 porsi" di varian 3 berasal dari angka 120 karyawan yang disebut pengguna; ganti bila tidak semua karyawan ikut.

---

## Catatan penguji
- Alur skill diikuti penuh; output lengkap sesuai "Format Output".
- Script berguna: menangkap kalimat 29 kata di draf awal V1 dan panjang V3.
- Temuan kecil: varian 3 mengikuti template hampir selalu > 500 karakter (terjadi juga di skenario 02 & 03) → peringatan jadi "rutin". Lihat HASIL-UJI.md.
