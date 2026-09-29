---
name: positioning-persona-usaha
description: Menyusun persona pelanggan, segmentasi-targeting-positioning (STP), kebutuhan pelanggan (JTBD), value proposition canvas, pernyataan positioning + pilihan tagline, pembeda dari pesaing, dan message house untuk UMKM/usaha Indonesia, lengkap dengan skor segmen lewat script dan teks siap tempel ke bio, listing, dan caption. Pakai saat pengguna bilang "siapa target pasar saya", "bikin persona", "positioning brand", "kenapa orang harus beli di saya", "bedain dari kompetitor", "value proposition", "tagline", "STP", customer persona, market segmentation, brand positioning, differentiation, message house.
---

# Positioning & Persona Usaha

## Tujuan
Mengubah "jualan ke semua orang" menjadi pilihan yang jelas: **siapa** yang dilayani duluan, **kenapa** mereka beli di kamu, dan **kalimat apa** yang dipakai di bio, listing, caption, dan chat WhatsApp. Hasil langsung siap tempel, bukan teori.

## Kapan digunakan
- "Target pasar produk saya siapa sih?" / "Bikinkan persona pelanggan untuk toko hijab saya."
- "Brand saya mirip banyak toko lain, gimana biar beda?"
- "Buatkan positioning dan tagline untuk jasa katering saya."
- "Aku punya data ulasan/daftar prospek, tolong simpulkan segmen dan pesan yang cocok."
- Persiapan sebelum bikin konten, iklan, atau rencana marketing.

## Kapan TIDAK digunakan
- Mencari daftar calon pelanggan B2B dan skor prospek -> `riset-calon-pelanggan`.
- Membaca banyak ulasan/keluhan untuk mencari tema -> `analisis-ulasan` (hasilnya boleh dijadikan bahan skill ini).
- Menghitung harga jual/HPP -> `hitung-hpp`, `harga-jual-marketplace`.
- Menulis halaman jualan lengkap -> `copy-landing-page`; caption harian -> `caption-sosmed-umkm`.
- Riset harga pesaing -> `riset-harga-kompetitor`. Validasi ide produk yang belum ada -> `validasi-ide-produk-baru`.
- Klaim kesehatan/medis, hukum, atau data pribadi konsumen yang identitasnya nyata: tidak diproses di sini (lihat Batasan).

## Input
| Info | Wajib? | Bila tidak diberikan |
|---|---|---|
| Produk/jasa + harga kasar | Ya | Tanyakan |
| Nama usaha (boleh belum ada) | Tidak | Pakai "[Nama Usaha]" |
| Pelanggan sekarang / yang paling sering beli | Tidak | Buat hipotesis, tandai "perlu dicek" |
| Kota/daerah, kanal jual (WA, Shopee/Tokopedia, TikTok Shop, IG, toko fisik) | Tidak | Asumsikan online + WA, sebutkan asumsinya |
| Pesaing utama (2-3 nama/akun) | Tidak | Minta; bila tidak ada, buat peta pesaing umum dan tandai "perlu dicek" |
| Bahan data: ulasan, chat pelanggan, hasil `analisis-ulasan` / `riset-calon-pelanggan` | Tidak | Pakai bila ada (Langkah 1) |

**Aturan tanya:** kalau info wajib kurang, tanyakan **sekali** dalam satu pesan berupa daftar singkat (maks. 5 pertanyaan). Kalau pengguna ingin cepat, langsung kerjakan dengan default dan tulis asumsinya di bagian "Asumsi".

## Langkah kerja
Kerjakan berurutan; jangan lompat. Detail template ada di `references/`.

### 1. Kumpulkan bahan (jangan mengarang)
- Ambil fakta dari pengguna. Bila ada keluaran `analisis-ulasan` (keluhan/pujian teratas, kalimat asli pelanggan) atau `riset-calon-pelanggan` (profil pelanggan ideal, daftar prospek), pakai itu dan sebut sumbernya.
- Pisahkan tegas: **FAKTA** (dari pengguna/data) vs **HIPOTESIS** (tebakan wajar). Angka ukuran pasar/penduduk **tidak dikarang**; tulis "perkiraan kasar" atau minta pengguna mengecek (mis. data BPS, Google Maps, jumlah pengikut).
- Kosakata pelanggan lebih berharga dari kata-kata indah: kumpulkan frasa asli ("bahannya adem", "nggak nerawang", "ongkirnya mahal").

### 2. Segmentasi (S dalam STP)
- Bagi pembeli potensial jadi **3-5 segmen** yang berbeda kebutuhannya (bukan sekadar beda usia). Dimensi yang dipakai UMKM: situasi/momen beli, kebutuhan utama, daya beli (rentang Rupiah per pembelian), kanal, kota/daerah, kebiasaan bayar (COD/transfer/e-wallet/paylater). Lihat `references/stp-umkm.md`.
- Beri nama segmen yang mudah diingat, mis. "Karyawati muda kantoran", "Ibu muda pengajian".

### 3. Targeting (T) dengan skor
- Nilai tiap segmen 1-5 pada 7 kriteria: ukuran, daya beli, kebutuhan mendesak, jangkauan kanal, kecocokan produk, persaingan, kemampuan melayani. Penilaian = perkiraan; jelaskan alasan tiap angka satu kalimat.
- **Hitung lewat script** (bukan dikira-kira): buat CSV dari `templates/segmen.csv`, lalu
  `python3 scripts/skor_segmen.py segmen.csv` (Windows: `python` atau `py`). Bobot bisa diubah: `--bobot "daya_beli=30"`.
- Bila script tidak bisa dijalankan, hitung manual: skor = jumlah(bobot x nilai) / jumlah bobot x 20. Bobot awal: ukuran 15, daya beli 20, kebutuhan 20, kanal 15, kecocokan 15, persaingan 10, kemampuan melayani 5.
- Pilih **1 segmen utama** (maks. 2). Skor >= 75 utama, 60-74 kandidat (uji kecil dulu), < 60 tunda. Katakan jelas: "untuk 90 hari ke depan fokus ke segmen X; segmen lain tetap boleh beli tapi tidak dikejar."

### 4. Persona (untuk segmen terpilih)
- Buat **1 persona utama** (opsional 1 pendamping) memakai `references/persona-indonesia.md`: nama fiktif + usia, kota/daerah, pekerjaan, penghasilan kasar & daya beli per pembelian, kebiasaan digital (WA, marketplace, TikTok, IG), cara bayar, bahasa/gaya bicara, pemicu beli, keberatan, siapa yang memengaruhi (suami, teman pengajian, grup WA, ulasan), kutipan khas.
- Wajib ada **satu wawasan tak terduga** (perilaku yang tidak jelas dari demografi) dan **anti-persona** (siapa yang bukan target).
- Persona adalah **tokoh rekaan dari pola**, bukan orang sungguhan. Jangan memasukkan nama, nomor, atau foto pelanggan nyata.

### 5. JTBD dan Value Proposition Canvas
- Rumus JTBD: "Ketika [situasi], aku ingin [kemajuan yang dicari], supaya [hasil yang diharapkan]." Tulis 1 tugas fungsional + 1 emosional + 1 sosial.
- Canvas (`references/kanvas-nilai-dan-pesan.md`): sisi pelanggan (tugas, kerepotan/pain, harapan/gain) dan sisi usaha (produk/layanan, pereda kerepotan, pencipta manfaat). Beri tanda mana yang **benar-benar dijanjikan dan bisa dibuktikan**.
- Tambah **Empat Gaya** peralihan: dorongan (yang bikin tak puas dengan yang lama), tarikan (yang menarik ke kita), kebiasaan (yang bikin bertahan), kecemasan (yang bikin ragu, mis. "takut ukurannya tidak pas", "takut barang tidak sampai").
- Ringkas dalam 6 bagian: Untuk siapa - Masalah/tugas - Kondisi sebelum - Cara kami - Kondisi sesudah - Alternatif lain.

### 6. Pembeda dari pesaing
- Petakan 3-5 alternatif: pesaing langsung (toko sejenis), tidak langsung (produk berbeda, kebutuhan sama), dan **"tidak beli apa-apa / cara lama"** (jahit sendiri, beli di pasar, minta teman).
- Tabel: klaim mereka - celah - klaim kita - bukti yang kita punya. Pembeda yang sah = spesifik, dirasakan pelanggan, dan bisa dibuktikan (foto, ulasan, proses, garansi). "Kualitas terbaik" dan "harga murah" bukan pembeda.
- Jangan menyerang/menyebut nama pesaing di materi publik; beri saran versi aman ("bukan seperti umumnya toko yang ...").

### 7. Pernyataan positioning + tagline
- Rumus: "Untuk [segmen] yang [kebutuhan], [Nama] adalah [kategori] yang [manfaat utama], karena [alasan percaya/bukti]. Berbeda dengan [alternatif], kami [pembeda]."
- Beri **2 versi**: internal (lengkap) dan publik (1 kalimat, tanpa menyebut pesaing).
- **5 opsi tagline** (maks. 8 kata, bahasa sehari-hari, tanpa klaim yang tak bisa dibuktikan) + 1 rekomendasi dengan alasan. Beri versi bio Instagram/TikTok (<= 150 karakter; hitung, jangan dikira).

### 8. Message house
- Atap: pesan utama (1 kalimat). 3 pilar pesan (masing-masing: klaim, bukti, contoh kalimat). Fondasi: bukti/aset (ulasan asli, foto proses, sertifikat, garansi). Tambah **penanganan 3 keberatan** dan **kata yang dipakai / dihindari**.
- Sertakan **teks siap tempel**: bio IG/TikTok, judul + 3 poin listing marketplace, 1 caption, 1 sapaan balasan WhatsApp untuk pelanggan baru. Detail: `references/kanvas-nilai-dan-pesan.md`.

### 9. Langkah uji cepat 7 hari
- Beri 3 uji murah untuk memeriksa hipotesis: tanya 5 pelanggan lama lewat WA (pertanyaan disediakan di referensi), uji 2 versi tagline di status/story, cek 10 pertanyaan chat masuk. Tulis apa yang harus terjadi supaya positioning dipertahankan atau diubah.

## Format output
Gunakan bagian bernomor ini (boleh dipangkas jika pengguna minta ringkas, tapi urutan tetap):
```
# Positioning & Persona — <nama usaha>
## Ringkasan 5 baris   (segmen utama, persona, positioning, tagline terpilih, langkah pertama)
## 1. Bahan & asumsi   (FAKTA / HIPOTESIS / perlu dicek)
## 2. Segmen & skor    (tabel segmen + skor dari script + alasan)
## 3. Persona utama    (kartu persona + anti-persona)
## 4. Kebutuhan (JTBD) & Value Proposition
## 5. Pembeda vs pesaing (tabel)
## 6. Positioning & tagline
## 7. Message house + teks siap tempel
## 8. Uji 7 hari & pengingat
```
Selalu tutup dengan: ceklis klaim (Batasan), asumsi, dan "apa yang perlu kamu cek sendiri".

## Contoh singkat
Input: "Toko hijab lokal, Bandung, harga Rp 89-189 ribu, jual lewat Shopee dan WA, pesaing banyak."
Keluaran ringkas:
- Segmen utama: **Karyawati muda kantoran** (skor 82/100). Persona: "Sinta, 27, admin di Bandung, ..." 
- Positioning: "Untuk perempuan berhijab yang bekerja dan sering keringetan, [Nama] adalah hijab yang adem dan tidak nerawang, karena bahannya diuji dipakai seharian; berbeda dengan hijab fashion yang cantik di foto tapi gerah."
- Tagline pilihan: "Adem dipakai seharian." Contoh lengkap: `examples/01-toko-hijab-stp-persona-lengkap.md`.

## Batasan & penanganan error
- **Bukan riset pasar.** Segmen, skor, dan persona = hipotesis terstruktur dari info pengguna. Katakan itu; sarankan uji 7 hari. Jangan menyebut angka ukuran pasar tanpa sumber.
- **Tidak mengarang bukti:** jangan menulis testimoni, rating, jumlah pelanggan, penghargaan, atau sertifikat (halal/BPOM/SNI) yang tidak dipunyai pengguna. Beri placeholder `[isi: ...]`.
- **Klaim berisiko** (kesehatan, "menyembuhkan", "pasti langsing", "100% aman", "termurah se-Indonesia", "BPOM" tanpa nomor): tolak/ganti versi yang sah dan bisa dibuktikan. Ingat UU Perlindungan Konsumen (iklan tidak boleh menyesatkan). Produk pangan/kosmetik/obat: arahkan pengguna mengecek aturan BPOM dan sertifikasi halal.
- **Bukan nasihat hukum/merek:** cek nama/tagline di pangkalan data merek DJKI sebelum dipakai jangka panjang.
- **Data pribadi:** bila pengguna menempelkan chat/ulasan berisi nama & nomor, ringkas polanya saja; jangan menyalin identitas ke persona.
- **Stereotip:** persona menggambarkan situasi dan kebutuhan, bukan menilai suku/agama/kelompok. Hindari generalisasi seperti "orang daerah pasti ...".
- Input terlalu tipis ("jualan baju"): tanyakan sekali (5 pertanyaan), atau kerjakan versi cepat dengan asumsi eksplisit.
- Skill ini tidak menggantikan uji lapangan; hasil terbaik muncul setelah 5 percakapan nyata dengan pelanggan.
- Script gagal/tak ada Python: hitung manual dengan rumus di Langkah 3; kesalahan CSV dijelaskan pesan "GAGAL: ..." (perbaiki barisnya, jalankan ulang).
