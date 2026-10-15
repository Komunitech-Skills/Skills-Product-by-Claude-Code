# C31 — Verifikasi rujukan aturan tahap 5 (laporan saja)

**Run Akun C:** 2026-10-15 ~01:30 UTC  
**Skill run ini:** (1) `tender-checklist`, (2) `persiapan-jual-atau-wariskan-usaha`  
**Catatan:** Hanya laporan verifikasi; revisi teks oleh Akun B. Akses sumber: 15 Oktober 2026.

---

## 1. `tender-checklist` — Perpres PBJ, LPSE, SIKaP

### 1.1 Hierarki Perpres 16/2018 jo. 12/2021 jo. 46/2025

| Klaim skill (`references/dasar-aturan.md`, SKILL.md) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Perpres 46/2025 = perubahan kedua atas Perpres 16/2018; berlaku sejak diundangkan | JDIH BPK | 2026-10-15 | «Peraturan Presiden … Nomor 46 Tahun 2025 … Perubahan Kedua atas Peraturan Presiden Nomor 16 Tahun 2018 … Tanggal Pengundangan 30 April 2025 … Tanggal Berlaku 30 April 2025 … Mengubah … PERPRES No. 12 Tahun 2021 … PERPRES No. 16 Tahun 2018» — https://peraturan.bpk.go.id/Details/318647/perpres-no-46-tahun-2025 | **COCOK** |
| Pengadaan barang/jasa pemerintah = proses identifikasi kebutuhan s.d. serah terima | Metadata BPK (abstrak Perpres 46/2025) | 2026-10-15 | Abstrak JDIH BPK menyebut definisi yang sama dengan skill | **COCOK** |
| Jaminan penawaran hanya konstruksi/terintegrasi (Perpres 46/2025); jaminan pelaksanaan kontrak > Rp200 jt | Skill v1.0.4 + naskah konsolidasi LKPP (sudah dicocokkan 2026-09-26) | 2026-10-15 | BPK mengonfirmasi 46/2025 mengubah 16/2018; rincian Pasal 30–33 tidak dibaca ulang penuh run ini | **COCOK** (selaras verifikasi sebelumnya; **PERLU REVIEW** bila naskah konsolidasi LKPP tidak bisa diunduh dari VM) |
| Paket UMK s.d. Rp15 M (Pasal 65); pengadaan langsung batas konstruksi Rp400 jt | Skill + sumber sekunder | 2026-10-15 | Perpres 46/2025 abstrak BPK; angka spesifik Pasal 38/65 tidak dikutip ulang dari PDF | **COCOK** arah (sudah ada naskah konsolidasi 2026-09-26 di skill) |

**Usulan teks (Akun B):** Tambah di README footnote «Perpres 46/2025 berlaku 30 April 2025 (JDIH BPK)» bila belum ada; pertahankan disclaimer «pasal Perpres dicek ke naskah konsolidasi LKPP».

### 1.2 SPSE (portal tender)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Tender lewat **SPSE** per LPSE; versi yang terlihat **SPSE 4.5** | eProc LKPP + spse.inaproc.id | 2026-10-15 | Daftar LPSE menampilkan «VERSI SPSE 4.5u20240923» — https://eproc.lkpp.go.id/lpse/ ; paket 2026 di https://spse.inaproc.id/nasional dan LPSE instansi (mis. kemkes) memuat label «spse 4.5» pada tender/pengadaan langsung | **COCOK** — portal aktif **spse.inaproc.id** (bukan hanya domain lama) |
| Login SPSE 4.5 memakai **TOTP** | Pengumuman LPSE Papua Barat Prov | 2026-10-15 | «SPSE Versi 4.5 Membutuhkan TOTP untuk login» — https://spse.inaproc.id/papuabaratprov/pengumuman/1144641 | **PERLU UBAH** (README/panduan pembeli): sebut TOTP/2FA bila skill menyebut «login SPSE» generik |

**Usulan teks (Akun B):** Satu kalimat di README: «Akses tender resmi lewat LPSE masing-masing di ekosistem INAPROC (spse.inaproc.id); versi 4.5 wajib TOTP.»

### 1.3 SIKaP (kualifikasi & kinerja penyedia)

| Klaim skill (registrasi penyedia, kualifikasi) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Penyedia terdaftar / data kualifikasi di ekosistem LKPP | SIKaP resmi | 2026-10-15 | «Aplikasi yang merupakan subsistem dari SPSE … mengelola data kualifikasi Pelaku Usaha dan riwayat kinerja Penyedia» — https://sikap.inaproc.id/ | **COCOK** |
| URL akses SIKaP | LKPP (pengumuman migrasi) | 2026-10-15 | «mulai tanggal **15 Desember 2025** … Akses SIKaP melalui laman: **sikap.inaproc.id**» — https://sikap.lkpp.go.id/ | **PERLU UBAH** bila README masih menyebut hanya `sikap.lkpp.go.id` tanpa `sikap.inaproc.id` |
| Akun terintegrasi INAPROC SSO | Pusat Bantuan INAPROC | 2026-10-15 | «Akun INAPROC menggunakan sistem Single Sign-On … SPSE (coming soon), SiKAP (coming soon)» — artikel 2025; praktik 2026-10-15: login SIKaP di sikap.inaproc.id aktif | **COCOK** arah migrasi ke INAPROC |

**Usulan teks (Akun B):** Ganti tautan lama ke `sikap.inaproc.id`; catat migrasi 15 Des 2025 di catatan kaki materi jualan.

---

## 2. `persiapan-jual-atau-wariskan-usaha` — PPh pengalihan, hibah/waris, notaris

### 2.1 Objek & pengecualian PPh (jual usaha vs waris/hibah)

| Klaim skill (`references/dasar-aturan.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Keuntungan pengalihan harta = objek PPh (Pasal 4 ayat (1) huruf d) | DJP — Objek PPh | 2026-10-15 | «keuntungan karena penjualan atau karena pengalihan harta» termasuk objek; pengecualian hibah/waris di ayat (3) — https://www.pajak.go.id/id/objek-pph | **COCOK** |
| **Warisan** bukan objek PPh | DJP — Objek PPh | 2026-10-15 | «Yang dikecualikan … **3. warisan**» — sumber sama | **COCOK** |
| Hibah ke keluarga sedarah lurus satu derajat (dan entitas tertentu) dikecualikan bila tidak ada hubungan usaha/pekerjaan/kepemilikan/penguasaan | DJP — Objek PPh + PMK 90 (rujukan artikel DJP) | 2026-10-15 | Pengecualian huruf a angka 2 UU PPh; artikel DJP «Bantuan atau Sumbangan, serta Harta Hibahan…» menjelaskan syarat hubungan antar pihak | **COCOK** — skill sudah menegaskan hibah ke anak sulung **wajib** konfirmasi notaris & ahli waris lain |
| Warisan belum terbagi dapat jadi subjek pajak pengganti bila menghasilkan | Artikel DJP (warisan) | 2026-10-15 | «warisan yang belum terbagi menjadi … subjek pajak pengganti» — https://www.pajak.go.id/index.php/id/artikel/menakar-pajak-atas-warisan-sri-ningsih | **COCOK** — selaras peringatan skill soal laba usaha sebelum dibagi |

**Usulan teks (Akun B):** Di `dasar-aturan.md` baris 5: ubah status «Sekunder» untuk Pasal 4 ayat (3) waris/hibah menjadi **Resmi (DJP objek-pph, 2026-10-15)**.

### 2.2 PPh final pengalihan tanah/bangunan (jual aset usaha)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| PPh final atas pengalihan hak tanah/bangunan (tarif umum **2,5%** nilai bruto); di bawah ambang tertentu dikecualikan | PP 34/2016 JDIH BPK | 2026-10-15 | Pasal 2: «**2,5%** … dari jumlah bruto nilai pengalihan hak atas tanah dan/atau bangunan» (selain RSS/Rumah Sederhana oleh WP usaha pokok pengalih) — https://peraturan.bpk.go.id/Details/5755/pp-no-34-tahun-2016 ; PDF https://peraturan.bpk.go.id/Download/27464/PP%20Nomor%2034%20Tahun%202016.pdf | **COCOK** |
| Pengalihan melalui hibah/waris termasuk dalam definisi pengalihan (PPh final TB) tetapi warisan dikecualikan dari objek PPh umum (UU PPh) | PP 34/2016 Pasal 1 | 2026-10-15 | «… melalui penjualan, … **hibah, waris**, atau cara lain …» — PDF sama | **COCOK** — skill memisahkan PPh final TB vs pengecualian waris (SKB) dengan benar |
| Warisan: pengalihan TB **bukan objek PPh**; SKB / PMK 81/2024 (skill) | Keterangan Tertulis DJP KT-16/2025 (sudah dirujuk skill 10-10-2026) | 2026-10-15 | Skill merujuk PDF resmi pajak.go.id; run ini tidak membuka ulang PDF | **COCOK** (mengandalkan verifikasi 10-10-2026 + konsistensi DJP objek-pph) |

**Usulan teks (Akun B):** Pastikan README menyebut PP 34/2016 + SKB warisan (PMK 81/2024 / PER-8/PJ/2025) dengan tanggal cek; jangan janji «tanpa pajak» untuk jual aset operasional PKP (PPN Pasal 16D tetap terpisah).

### 2.3 PPN aktiva & BPHTB

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| PKP: penyerahan aktiva yang semula tidak untuk dijual kena PPN (UU PPN / artikel DJP) | Artikel DJP «jual aktiva tetap» (opini pegawai, 2022) | **PERLU REVIEW** — arah benar; usulkan kutip Pasal 16D UU HPP dari JDIH |
| BPHTB = pajak daerah; tetap pada perolehan warisan | UU 1/2022 HKPD (rujukan skill) | **COCOK** arah; tarif per Perda tidak diverifikasi run ini |

### 2.4 Akta notaris / PPAT (jual & waris)

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| Hibah/wasiat/akta waris **wajib** lewat notaris; skill tidak memberi prosedur detail | Praktik hukum umum; UU 2/2021 tentang Jabatan Notaris (tidak dibuka penuh run ini) | **COCOK** — skill hanya daftar pertanyaan ke notaris, bukan prosedur palsu |
| Perubahan sekutu CV / saham PT (Pasal 57 UU 40/2007) | pasal.id (sekunder di skill) | **PERLU REVIEW** — UU 40/2007 jo. UU 6/2023 Cipta Kerja; Akun B cocokkan naskah resmi |

**Usulan teks (Akun B):** Tidak ubah alur skill; perkuat disclaimer «akta hibah/waris dan balik nama tanah = notaris/PPAT, bukan output skill».

---

## Ringkasan run

| Skill | Hasil singkat |
|---|---|
| `tender-checklist` | Perpres 46/2025 **COCOK** (BPK); SPSE 4.5 + **spse.inaproc.id COCOK**; SIKaP → **sikap.inaproc.id** (migrasi 15 Des 2025); TOTP login **PERLU UBAH** di README |
| `persiapan-jual-atau-wariskan-usaha` | Waris/hibah Pasal 4 ayat (3) **COCOK** (DJP); PP 34/2016 **COCOK** metadata; warisan belum terbagi **COCOK**; PPN aktiva & UU 40/2007 **PERLU REVIEW** |

**Progress C31:** 2/6 skill (tender-checklist, persiapan-jual-atau-wariskan-usaha).  
**Router model:** smoke OpenClaw gateway → **HTTP 530** (~96 s, Ninerouter) → **C24 G18 tidak dilanjutkan**; pesan 2–10 `msgs-g18.json` belum terkirim.

**Run berikutnya:** smoke router → G18 bila HTTP 200; else C31 skill (3–4) `proposal-kerjasama` + `tagih-piutang` (atau `perjanjian-kerja` bila ada).

---

## 3. `proposal-kerjasama` — KUHPerdata Pasal 1320 & bea meterai UU 10/2020

### 3.1 Syarat sah perjanjian (Pasal 1320 KUHPerdata)

| Klaim skill (`SKILL.md`, kerangka) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Setelah mitra setuju, tuangkan perjanjian tertulis; skill `perjanjian-sederhana` | Pasal 1320 + 1338 KUHPerdata (Wikisource) | 2026-10-15 | «Supaya terjadi persetujuan yang sah, perlu dipenuhi empat syarat; 1. kesepakatan … 2. kecakapan … 3. suatu pokok persoalan tertentu; 4. suatu sebab yang tidak terlarang.» — https://id.wikisource.org/wiki/Halaman:KUHPerdata.pdf/236 | **COCOK** — proposal bukan kontrak, tetapi anjuran perjanjian tertulis selaras syarat sah bila nanti diikat |
| Empat syarat: kesepakatan, kecakapan, hal tertentu, sebab halal | Halo JPN Kejaksaan RI (2025-88JP) | 2026-10-15 | Ringkasan Pasal 1320: syarat subjektif (1–2) → dapat dibatalkan; objektif (3–4) → batal demi hukum bila tidak terpenuhi | **COCOK** |
| Pasal 1321: persetujuan karena kekhilafan/paksaan/penipuan tidak berkekuatan | Wikisource KUHPerdata hal. 236 | 2026-10-15 | «Tiada suatu persetujuan pun mempunyai kekuatan jika diberikan karena kekhilafan atau diperoleh dengan paksaan atau penipuan.» | **COCOK** — skill menolak skema piramida/penipuan (kerangka reseller) |

**Usulan teks (Akun B):** Di README pembeli, satu kalimat: «Proposal ini bukan kontrak; bila disepakati, perjanjian tertulis harus memenuhi syarat sah Pasal 1320 KUHPerdata (kesepakatan, kecakapan, objek jelas, causa halal).» Opsional rujuk `perjanjian-sederhana`.

### 3.2 Bea meterai perjanjian (UU 10/2020)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Perjanjian tertulis kena bea meterai **Rp10.000** (UU 10/2020) | UU 10/2020 (JDIH Kemenkeu / pajak.go.id PDF) Pasal 3 ayat (2) huruf a, Pasal 4 | 2026-10-15 | «surat perjanjian, surat keterangan, surat pernyataan, atau surat lainnya yang sejenis, beserta rangkapnya»; «tarif tetap sebesar Rp10.000,00» — https://www.pajak.go.id/sites/default/files/2020-11/UU%20Nomor%2010%20Tahun%202020%20tentang%20Bea%20Materai.pdf | **COCOK** |
| Ambang > Rp5 jt hanya untuk kuitansi/pelunasan utang, bukan semua perjanjian | UU 10/2020 Pasal 3 ayat (2) huruf g | 2026-10-15 | Objek huruf g: dokumen > Rp5 jt yang «menyebutkan penerimaan uang» atau «pengakuan … utang … dilunasi» | **COCOK** — selaras catatan skill `tagih-piutang` & contoh proposal (meterai untuk perjanjian, bukan kuitansi) |
| Saat terutang: dibubuhi tanda tangan (surat perjanjian) | DJP — halaman Bea Meterai | 2026-10-15 | Pasal 8 UU 10/2020: saat terutang untuk surat perjanjian = saat dokumen dibubuhi tanda tangan — https://www.pajak.go.id/id/bea-meterai | **COCOK** |

**Usulan teks (Akun B):** Pertahankan kalimat meterai Rp10.000; tambah opsional «e-meterai atau meterai tempel» dan tautan pajak.go.id/bea-meterai.

---

## 4. `tagih-piutang` — wanprestasi, somasi, UU 8/1999 (konsumen)

### 4.1 Lalai, somasi, bunga moratoir (KUHPerdata)

| Klaim skill (`references/regulasi.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Pasal 1238: lalai setelah surat perintah/akta sejenis atau lewat waktu perjanjian | Wikisource / BPK Bali (tulisan somasi) | 2026-10-15 | «Si berutang adalah lalai, apabila ia dengan surat perintah atau dengan sebuah akta sejenis itu telah dinyatakan lalai, atau demi perikatannya sendiri … lewatnya waktu yg ditentukan.» | **COCOK** |
| Pasal 1243: ganti rugi/biaya/bunga setelah lalai | Halo JPN (2025-5XQB) | 2026-10-15 | «Penggantian biaya, kerugian dan bunga … mulai diwajibkan, bila debitur, walaupun telah dinyatakan lalai, tetap lalai …» | **COCOK** |
| Pasal 1250: bunga moratoir 6%/tahun untuk utang uang (skill tidak hitung) | Skill + doktrin (sumber sekunder di skill) | 2026-10-15 | Run ini tidak membuka PDF KUHPerdata Pasal 1250 penuh | **COCOK** arah; **PERLU REVIEW Akun B:** kutip Pasal 1250 dari naskah resmi |
| Somasi tidak selalu mutlak bila perjanjian sudah menetapkan akibat lalai | Marinews MA + LBH Pengayoman | 2026-10-15 | Yurisprudensi: gugatan/surat teguran dapat dianggap somasi; somasi wajib bervariasi menurut perjanjian | **PERLU UBAH** (ringan): di `regulasi.md` §1 tambah satu kalimat «bila perjanjian/invoice sudah menetapkan jatuh tempo & akibat lalai, somasi terpisah bisa tidak wajib — advokat menilai» |

### 4.2 Penagihan & UU 8/1999 Perlindungan Konsumen

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Utang dagang = perdata; jangan ancam pidana hanya karena telat bayar | UU 8/1999 fokus pelaku usaha → konsumen (BPK PDF) | 2026-10-15 | UU 8/1999 melindungi **konsumen** dari pelaku usaha (Pasal 4, 19, 45), bukan debitur B2B | **COCOK** — skill sudah bedakan utang usaha vs ancaman pidana |
| Klausula baku merugikan konsumen (denda/penagihan sepihak) batal demi hukum | UU 8/1999 Pasal 18 ayat (1)–(3) (BPK PDF) | 2026-10-15 | Larangan klausula baku huruf a–h; ayat (3): «dinyatakan batal demi hukum» | **COCOK** — skill: denda hanya bila disepakati tertulis; relevan bila **pembeli = konsumen** |
| Penagihan ke pihak ketiga / publikasi nama = risiko UU ITE & PDP | UU 8/1999 + skill §2 | 2026-10-15 | Pasal 18 tidak menggantikan larangan pencemaran/ancaman (UU ITE) | **COCOK** |
| Gugatan sederhana wanprestasi maks Rp500 jt (PERMA 2/2015 jo. 4/2019) | Skill (perlu review) | 2026-10-15 | Run ini tidak verifikasi PERMA terbaru 2026 | **PERLU REVIEW** — Akun B cek PERMA MA & batas nilai gugatan sederhana |

**Usulan teks (Akun B):** Tambah di README §FAQ: «Jika yang berutang adalah konsumen (B2C), klausula penagihan harus patuh UU 8/1999 Pasal 18; penagihan B2B umumnya KUHPerdata wanprestasi.»

---

## Ringkasan run 2026-10-15 ~02:00 UTC

| Skill | Hasil singkat |
|---|---|
| `proposal-kerjasama` | Pasal 1320 **COCOK**; UU 10/2020 meterai Rp10.000 untuk surat perjanjian **COCOK** |
| `tagih-piutang` | Pasal 1238/1243 **COCOK**; UU 8/1999 Pasal 18 relevan B2C **COCOK**; somasi mutlak & PERMA 500 jt **PERLU REVIEW/UBAH** ringan |

**Progress C31:** 4/6 skill (`proposal-kerjasama`, `tagih-piutang` ditambah pada tender-checklist, persiapan-jual-atau-wariskan-usaha).  
**Router model:** smoke OpenClaw `./oc.sh agent --local` → **HTTP 530** (~86 s, Ninerouter Error 1016) → **C24 G18 tidak dilanjutkan**; pesan 2–10 `msgs-g18.json` belum terkirim.

**Run berikutnya:** smoke router → G18 bila HTTP 200; else C31 skill (5–6) `surat-penawaran-harga` + `checklist-keamanan-pangan-usaha`.

---

## 5. `surat-penawaran-harga` — PPN 12 % / DPP 11/12, PKP, masa berlaku penawaran

### 5.1 Tarif PPN & DPP nilai lain (PMK 131/2024)

| Klaim skill (`references/regulasi.md`, SKILL.md) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| PKP saja boleh memungut PPN & faktur | UU PPN jo. UU HPP (umum); DJP | 2026-10-15 | PMK 131/2024 mengatur tarif & DPP; faktur lewat Coretax (KEP-54/PJ/2025) | **COCOK** |
| Non-mewah: PPN = 12 % × DPP nilai lain 11/12 → efektif 11 % | PMK 131/2024 (JDIH BPK) + artikel DJP | 2026-10-15 | «tarif efektif … selain barang mewah adalah 11 persen»; «12% x 11/12» — https://www.pajak.go.id/id/node/113453 ; PMK berlaku **1 Januari 2025** — https://peraturan.bpk.go.id/Details/311485/pmk-no-131-tahun-2024 | **COCOK** |
| Barang mewah (PPnBM): 12 % × harga jual | PMK 131/2024 Pasal 2 ayat (2)–(3) (ringkasan DJP) | 2026-10-15 | DJP: tarif 12 % × harga jual untuk BKP mewah | **COCOK** |
| Pembulatan PPN ke bawah dari DPP | Standar library (belum Coretax) | 2026-10-15 | — | **COCOK** arah; disclaimer skill sudah ada |
| Ambang PKP Rp4,8 M/tahun | Skill (belum dicek ulang) | 2026-10-15 | Run ini tidak verifikasi angka terbaru 2026 | **PERLU REVIEW Akun B** — cek PMK/UU HPP ambang usaha kecil |

### 5.2 Masa berlaku penawaran & meterai SPH

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| Default masa berlaku penawaran **14 hari** | Praktik bisnis / default skill, bukan aturan | **COCOK** sebagai default (bukan klaim hukum); README boleh tetap sebut «bisa disesuaikan» |
| SPH umumnya **bukan** faktur pajak | PMK/Coretax (faktur terpisah) | **COCOK** |
| Bea meterai: perjanjian Rp10.000 (UU 10/2020); ambang > Rp5 jt untuk kuitansi/pelunasan | Sudah diverifikasi C31 §3 (proposal-kerjasama) | **COCOK** — skill `regulasi.md` selaras; catatan «UU 10/2020 belum dibaca langsung» di regulasi.md **PERLU UBAH** ke **COCOK** (sudah dicek run C31 sebelumnya) |

**Usulan teks (Akun B):** Di `references/regulasi.md` baris PKP: tandai verifikasi PMK 131 + DJP 2026-10-15; perbarui footnote meterai ke sumber resmi UU 10/2020 (BPK/DJP).

---

## 6. `checklist-keamanan-pangan-usaha` — PP 86/2019, Perka BPOM, Permenkes, halal

### 6.1 Perizinan & SPP-IRT / PIRT

| Klaim skill (`references/perizinan-indonesia.md`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| PIRT / SPP-IRT untuk pangan olahan IRTP kemasan eceran | PP 86/2019 Pasal 35 (JDIH PDF) | 2026-10-15 | IRTP wajib sertifikat produksi dari bupati/wali kota | **COCOK** |
| Nama & pedoman terbaru **SPP-IRT** | Peraturan BPOM No. 4 Tahun 2024 | 2026-10-15 | «Perizinan … berupa **SPP-IRT**»; pengecualian umur simpan <7 hari, pangan siap saji, bahan belum olah — https://peraturan.bpk.go.id/Read/341095/ | **PERLU UBAH** ringan: README/references sebut **SPP-IRT** selain singkatan PIRT; catat Per BPOM 4/2024 |
| SLHS + pelatihan penjamah (jasa boga/katering) | Permenkes 2/2023 | 2026-10-15 | Permenkes 2/2023 **mencabut** Permenkes **1096/2011** jasa boga — https://peraturan.bpk.go.id/Details/245563 | **COCOK** — skill sudah pakai Permenkes 2/2023; pastikan output agent tidak menyebut 1096/2011 |
| Label + alergen Peraturan BPOM 31/2018 jo. 20/2021 | Metadata BPK (skill) | 2026-10-15 | Run ini tidak buka PDF penuh | **COCOK** arah (sudah di references); **PERLU REVIEW** naskah Pasal 49 ayat (3) |

### 6.2 Halal (PP 42/2024)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Produk masuk/beredar wajib sertifikat halal (kecuali bahan haram → label tidak halal) | PP 42/2024 (JDIH BPK abstrak) | 2026-10-15 | «Produk … wajib bersertifikat halal»; menggantikan PP 39/2021; berlaku **17 Oktober 2024** | **COCOK** |
| UMK: penahapan wajib halal (skill: **18 Oktober 2026**) | PP 42/2024 + rilis BPJPH 2026 (skill) | 2026-10-15 | Abstrak PP 42 tidak memuat tanggal tahapan UMK; skill merujuk BPJPH 2026 — **PERLU REVIEW** kutip pasal PP 42/UU 33 jo. Cipta Kerja untuk tanggal pasti |

### 6.3 Suhu & bahan (FDA/WHO — bukan PP 86)

| Klaim skill (`references/batas-suhu-dan-bahan-rawan.md`) | Sumber | Kesimpulan |
|---|---|---|
| Batas suhu mengacu FDA/WHO/USDA, bukan PP 86/2019 | Sumber asing resmi (skill) | **COCOK** — PP 86 tidak mengatur suhu internal; skill sudah label PERLU REVIEW untuk aturan Indonesia lebih rinci |

**Usulan teks (Akun B):** Tambah satu baris di `perizinan-indonesia.md`: «SPP-IRT = Per BPOM 4/2024, mengacu PP 86/2019»; cek apakah PP 1/2026 mengubah PP 86 (metadata BPK ada — **PERLU REVIEW** sebelum rilis batch).

---

## Ringkasan run 2026-10-15 ~02:30 UTC

| Skill | Hasil singkat |
|---|---|
| `surat-penawaran-harga` | PMK 131 + DJP **COCOK** (11/12, efektif 11 %); PKP/meterai **COCOK**; ambang PKP **PERLU REVIEW** |
| `checklist-keamanan-pangan-usaha` | PP 86/2019 + Per BPOM 4/2024 SPP-IRT **COCOK**; Permenkes 2/2023 cabut 1096 **COCOK**; halal PP 42 **COCOK**; tanggal UMK halal **PERLU REVIEW** |

**Progress C31:** **6/6 selesai** (tender-checklist … checklist-keamanan-pangan-usaha).  
**Router model:** smoke `./oc.sh agent --local` → **HTTP 530** (~94 s, Error 1016) → **C24 G18 tidak dilanjutkan**; pesan 2–10 `msgs-g18.json` belum terkirim.

**Run berikutnya:** smoke router → **G18** bila HTTP 200; bila masih 530, tidak ada backlog C25–C31 — tunggu router / tugas baru di papan.
