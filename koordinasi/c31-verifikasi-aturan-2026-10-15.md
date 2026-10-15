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
