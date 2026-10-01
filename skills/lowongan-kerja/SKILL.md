---
name: lowongan-kerja
description: Membuat iklan lowongan kerja (loker) siap posting untuk JobStreet, LinkedIn, Glints, Instagram, dan grup WhatsApp, lengkap dengan tanggung jawab, kualifikasi wajib vs nilai plus, benefit, cara melamar, versi pendek IG/WA, dan pertanyaan screening, serta cek syarat diskriminatif (usia, gender, agama, penampilan). Gunakan saat pengguna minta buat loker, info lowongan, rekrut karyawan, atau job posting, job description, hiring ad, job vacancy.
---

# Lowongan Kerja Siap Posting

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah kebutuhan rekrutmen pemilik usaha ("butuh admin online shop, gaji UMR") menjadi iklan lowongan yang jelas, menarik pelamar yang tepat, bebas syarat diskriminatif, dan langsung bisa diposting di beberapa kanal sekaligus.

## Kapan digunakan
- Pengguna minta dibuatkan loker / iklan lowongan / job posting / job description untuk dipublikasikan.
- Pengguna ingin versi pendek loker untuk Instagram, status/grup WhatsApp, atau Facebook grup loker.
- Pengguna minta pertanyaan screening untuk menyaring pelamar.
- Pengguna minta mengecek atau merapikan loker yang sudah ada.

## Kapan TIDAK digunakan
- Membuat surat peringatan karyawan → pakai skill `surat-peringatan-karyawan`.
- Surat penawaran kerja / kontrak kerja (PKWT/PKWTT) → pakai `perjanjian-sederhana` dan sarankan cek ahli hukum.
- Surat resmi umum (undangan, keterangan kerja) → pakai `surat-resmi`.
- SOP kerja untuk karyawan yang sudah diterima → pakai `sop-writer`.
- Menghitung gaji, PPh 21, atau BPJS → di luar cakupan; minta pengguna memakai kalkulator resmi atau konsultan.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Posisi / jabatan | Ya | — (tanyakan) |
| Nama usaha & bidang usaha | Ya | — (tanyakan; boleh "Rahasia/Confidential" jika pengguna minta) |
| Lokasi kerja (kota, WFO/hybrid/remote) | Ya | — (tanyakan) |
| Tugas utama sehari-hari | Tidak | Disusun dari posisi yang umum; tandai "(sesuaikan)" |
| Status kerja (tetap/kontrak/magang/freelance/part-time) | Tidak | `[isi status kerja]` (jangan diasumsikan) |
| Jam & hari kerja | Tidak | "[isi jam kerja]" |
| Gaji / rentang gaji | Tidak | Tidak dicantumkan; sarankan mencantumkan rentang (pelamar lebih banyak) |
| Benefit | Tidak | Hanya yang disebut pengguna. Jangan mengarang BPJS/bonus |
| Cara melamar & batas waktu | Tidak | "[isi email/nomor WA]", batas waktu 14 hari dari hari ini |
| Kanal posting | Tidak | Semua: versi lengkap + versi IG + versi WA |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan (maks 5 pertanyaan bernomor). Jika pengguna ingin cepat, buat dengan placeholder `[isi ...]` dan sebutkan asumsinya di akhir.

## Langkah kerja
1. **Pahami posisi.** Tentukan level (staf/senior/supervisor), jenis pekerjaan, dan 5–8 tugas nyata. Jika pengguna hanya menyebut nama posisi, pakai daftar tugas umum dari `references/contoh-posisi.md` dan tandai "(sesuaikan)".
2. **Saring syarat diskriminatif** (wajib, sebelum menulis). Periksa setiap syarat dari pengguna terhadap `references/anti-diskriminasi.md`:
   - Syarat usia, jenis kelamin, agama, suku, status pernikahan, tinggi/berat badan, "berpenampilan menarik", warna kulit, disabilitas → **jangan dicantumkan** kecuali ada alasan pekerjaan yang nyata dan bisa dijelaskan.
   - Jika pengguna memintanya, tetap buat lowongan **tanpa** syarat itu, lalu beri kotak **⚠️ Catatan** berisi: syarat mana yang dihapus, alasan singkat (SE Menaker M/6/HK.04/V/2025 & prinsip kesempatan kerja yang sama), dan alternatif kalimat yang berfokus pada kemampuan (mis. "berpenampilan menarik" → "rapi dan sopan dalam melayani pelanggan").
   - Jika pengguna bersikeras dan ada alasan pekerjaan yang sah (mis. usia minimal 18 tahun karena aturan kerja; kemampuan mengangkat 20 kg untuk gudang), tulis sebagai syarat kemampuan, bukan ciri pribadi.
2b. **Cek gaji vs UMK** (wajib bila gaji dan kota/kabupaten disebut, termasuk saat mengecek loker lama): skill tidak punya tabel UMK, jadi jangan menebak angka. Tambahkan kotak **⚠️ Cek gaji vs UMK** dari `references/anti-diskriminasi.md` (bagian "Gaji vs upah minimum") dengan `[isi: UMK]`, minta pengguna mengecek UMK tahun berjalan di Disnaker/pemprov setempat, dan sebut pengecualian usaha mikro/kecil (PP 36/2021). Bila pengguna memberi angka UMK resmi, bandingkan langsung; bila gaji di bawahnya, beri peringatan tegas. Pada format cek loker, masukkan sebagai baris di tabel "0) Hasil cek loker".
3. **Pisahkan kualifikasi** menjadi **Wajib** (maks 6 butir, benar-benar dibutuhkan hari pertama) dan **Nilai plus** (maks 4 butir). Syarat yang bisa dilatih dalam 1–2 minggu pindahkan ke nilai plus.
4. **Tulis versi lengkap** (JobStreet/LinkedIn/Glints) mengikuti format output. Judul posisi pakai nama yang umum dicari pelamar (mis. "Admin Online Shop", bukan "Customer Happiness Hero"); boleh tambahkan padanan Inggris dalam kurung.
5. **Tulis versi pendek**:
   - Instagram: caption ≤ 120 kata + teks untuk desain feed (judul, 3 poin, cara melamar) + 5–8 hashtag loker lokal (#lokerjakarta, #lokersurabaya, dsb. sesuai kota).
   - WhatsApp grup: ≤ 80 kata, tanpa hashtag, format *tebal* WA pakai `*...*`.
6. **Buat 5–7 pertanyaan screening** yang terkait langsung dengan tugas (pengalaman, tes kecil, ketersediaan, ekspektasi gaji). Jangan menanyakan agama, status pernikahan, rencana hamil, atau hal pribadi yang tidak relevan.
7. **Tambahkan pengingat anti-penipuan** di akhir iklan: "Proses rekrutmen tidak dipungut biaya apa pun."
8. Periksa dengan checklist, lalu tawarkan revisi (nada lebih santai/formal, bahasa Inggris untuk LinkedIn).

## Format output
Untuk permintaan **cek/rapikan loker yang sudah ada**, awali dengan bagian 0, lalu lanjutkan bagian 1–4 berisi versi yang sudah dirapikan:
```
## 0) Hasil cek loker
| Di loker lama | Masalah | Diganti menjadi |
|---|---|---|
| "Wanita, maks 25 th" | Syarat diskriminatif (SE Menaker M/6/HK.04/V/2025) | Dihapus; diganti "Ramah dan teliti" |
| "Biaya seragam Rp 150.000" | Pola penipuan: pelamar diminta bayar | Dihapus; tambah "tidak dipungut biaya" |
Ringkasan: [n] masalah ditemukan. [1 kalimat saran utama]
```
Untuk permintaan membuat loker baru:
```
## 1) Versi lengkap (JobStreet / LinkedIn / Glints)
**[Judul Posisi]** — [Nama Usaha] | [Kota] ([WFO/Hybrid/Remote]) | [Status kerja]

**Tentang kami**
[1–2 kalimat usaha]

**Yang akan kamu kerjakan**
- ...

**Kualifikasi wajib**
- ...

**Nilai plus**
- ...

**Yang kamu dapatkan**
- Gaji: [rentang atau "dibicarakan saat interview"]
- ...

**Cara melamar**
Kirim [CV / portofolio] ke [email/WA] dengan subjek "[Posisi] - [Nama]" paling lambat [tanggal].
Proses rekrutmen tidak dipungut biaya apa pun.
Data lamaran hanya digunakan untuk proses rekrutmen [Nama Usaha]. (opsional)

## 2) Versi Instagram
Teks desain feed: ...
Caption: ...
Hashtag: ...

## 3) Versi grup WhatsApp
...

## 4) Pertanyaan screening
1. ...

⚠️ Catatan (hanya jika ada syarat yang dihapus/diubah): ...
Asumsi: ...
```

## Contoh
**Input pengguna:** "Buatin loker admin olshop buat toko hijab aku di Bandung, cewek, maks 25 tahun, good looking, gaji UMR, kirim CV ke WA 0812-xxxx"

**Output (ringkas):**
```
## 1) Versi lengkap
**Admin Online Shop** — [Nama Toko] Hijab | Bandung (WFO) | [isi status kerja]

**Yang akan kamu kerjakan**
- Membalas chat pembeli di Shopee, TikTok Shop, dan WhatsApp
- Input pesanan dan cek stok harian
- Menyiapkan resi dan koordinasi dengan tim packing
- Membuat rekap penjualan mingguan sederhana
- Mengunggah produk baru (foto, judul, deskripsi)

**Kualifikasi wajib**
- Terbiasa memakai aplikasi Shopee Seller / TikTok Shop atau cepat belajar
- Bisa Microsoft Excel/Google Sheets dasar
- Ramah, sabar, dan rapi dalam melayani pelanggan
- Siap bekerja di Bandung sesuai jam kerja toko

**Nilai plus**
- Pengalaman admin online shop, terutama fashion muslim
- Bisa edit foto produk sederhana (Canva/CapCut)

**Yang kamu dapatkan**
- Gaji sesuai UMK Kota Bandung [isi angka]
...
⚠️ Catatan: Syarat "cewek", "maks 25 tahun", dan "good looking" tidak kami cantumkan.
Kementerian Ketenagakerjaan melalui SE M/6/HK.04/V/2025 melarang syarat diskriminatif
seperti batas usia, penampilan menarik, dan jenis kelamin yang tidak berkaitan dengan
pekerjaan. Sebagai gantinya kami menulis kemampuan yang benar-benar dibutuhkan
("ramah, sabar, rapi"). Jika posisi ini memang harus perempuan (mis. fitting langsung
dengan pelanggan perempuan), jelaskan alasannya agar bisa ditulis sebagai kebutuhan kerja.
```

Contoh lebih lengkap (kurir, barista, staf gudang, sales) ada di `references/contoh-posisi.md`.

## Checklist sebelum mengirim hasil
- [ ] Tidak ada syarat usia, gender, agama, suku, status nikah, fisik, atau "good looking" tanpa alasan kerja yang nyata.
- [ ] Jika ada syarat yang dihapus, kotak ⚠️ Catatan ada dan menjelaskan alternatifnya.
- [ ] Kualifikasi wajib ≤ 6 butir dan benar-benar dibutuhkan; sisanya di nilai plus.
- [ ] Benefit hanya yang disebut pengguna; angka gaji/UMK tidak dikarang (pakai `[isi angka]`).
- [ ] Bila gaji & kota disebut: kotak **⚠️ Cek gaji vs UMK** ada (dengan `[isi: UMK]` bila angka resmi belum diketahui).
- [ ] Ada cara melamar, batas waktu, dan kalimat "tidak dipungut biaya".
- [ ] Versi IG ≤ 120 kata, versi WA ≤ 80 kata, format tebal WA memakai `*...*`.
- [ ] Jika versi IG/WA masih memuat `[isi ...]`, tulis peringatan tebal tepat di atas bloknya: **⚠️ Isi dulu bagian [isi ...] sebelum dikirim.** Lebih baik lagi: hapus baris yang belum ada datanya dari versi IG/WA.
- [ ] Untuk permintaan cek loker: bagian "0) Hasil cek loker" ada dan setiap masalah punya penggantinya.
- [ ] Pertanyaan screening tidak menanyakan hal pribadi yang tidak relevan.

## Batasan & penanganan error
- **Angka UMR/UMK tidak boleh dikarang.** Nilainya berbeda per kota dan berubah tiap tahun; minta pengguna mengisi atau tulis "[isi: UMK]". Tetapi **selalu ingatkan** pengguna untuk membandingkan gaji dengan UMK (langkah 2b).
- Jangan menjanjikan benefit (BPJS, THR, bonus, jenjang karier) yang tidak disebut pengguna. Boleh diberi saran: "Jika ada BPJS, sebutkan: pelamar lebih tertarik."
- Jika pengguna meminta syarat yang jelas melanggar hukum atau merendahkan (mis. "bukan dari suku X", "belum menikah dan tidak akan hamil"), tolak syarat itu dengan sopan, jelaskan singkat, dan tetap berikan lowongan yang layak.
- Jika lowongan terlihat seperti modus penipuan (pelamar diminta bayar biaya seragam/pelatihan), beri peringatan dan jangan tulis syarat pembayaran.
- Data pelamar (CV, nomor HP) adalah data pribadi: sarankan hanya dipakai untuk rekrutmen dan dihapus bila tidak lolos (UU PDP). Lihat `references/anti-diskriminasi.md`.
- Dasar aturan dan tanggal berlaku ada di `references/anti-diskriminasi.md`. Ini bukan nasihat hukum; untuk sengketa rekrutmen, konsultasikan ke Disnaker atau ahli hukum ketenagakerjaan.
