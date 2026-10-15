# C30 — Verifikasi rujukan aturan tahap 4 (laporan saja)

**Run Akun C:** 2026-10-14 ~23:30 UTC  
**Skill run ini:** (1) `kasir-lokal`, (2) `laporan-keuangan-emkm`  
**Catatan:** Hanya laporan verifikasi; revisi teks oleh Akun B. Akses sumber: 14 Oktober 2026.

---

## 1. `kasir-lokal` — PPN 12 % / DPP 11/12, PBJT HKPD, pembulatan

### 1.1 PPN tarif efektif 11 % (DPP nilai lain 11/12)

| Klaim skill (`references/pajak.md`, `kasir.py`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| PPN 12 % × DPP nilai lain 11/12 → efektif 11 %; PMK 131/2024 berlaku 1 Jan 2025 | DJP — PMK 131/2024 | 2026-10-14 | «PPN … dihitung dengan mengalikan tarif PPN 12 persen dengan DPP berupa nilai lain, yaitu sebesar 11/12 … tarif efektif PPN sebesar 11 persen (12% x 11/12)» — https://www.pajak.go.id/en/node/113453 | **COCOK** |
| Pembulatan PPN ke bawah sekali dari DPP persis | Standar library (selaras C28 `hitung-ppn`) | — | PMK tidak menspesifikkan floor per nota; praktik skill konsisten dengan skill pajak lain repo | **COCOK** (dengan disclaimer «belum dicocokkan Coretax» sudah ada) |
| Mode harga termasuk PPN: DPP bulat terbesar dengan DPP + PPN ≤ harga | `kasir.py` + tes regresi | — | Selaras mekanisme PMK/DPP nilai lain untuk harga all-in | **COCOK** |

**Usulan teks (Akun B):** Opsional — tambah di README footnote «tarif efektif 11 % untuk non-mewah per PMK 131/2024» dengan link DJP (sudah ada di references).

### 1.2 PBJT makanan/minuman (UU 1/2022 HKPD)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Makanan/minuman restoran/warung/katering **bukan objek PPN** (objek pajak daerah) | DJP — «Makan di Restoran Tidak Kena PPN» | 2026-10-14 | «makanan dan minuman yang disajikan di hotel, restoran, rumah makan, warung … **tidak dikenai PPN** … objek pajak daerah … UU Nomor 1 Tahun 2022 … HKPD» — https://www.pajak.go.id/en/node/81110 | **COCOK** |
| PPN dan PBJT tidak digabung | Skill + DJP (objek berbeda) | 2026-10-14 | Sama sumber di atas | **COCOK** |
| Tarif PBJT **paling tinggi 10 %** | UU 1/2022 HKPD (JDIH BPK); contoh Perda | 2026-10-14 | DJP: «tarif PBJT … ditetapkan **paling tinggi sebesar 10%** melalui peraturan daerah»; UU HKPD Pasal 58 ayat (1) (ringkasan JDIH https://peraturan.bpk.go.id/Details/195696/uu-no-1-tahun-2022 ) | **COCOK** — script membatasi `--tarif-pbjt` ≤ 10 |
| Dasar pengenaan = jumlah dibayar konsumen (Ps 57); pokok = dasar × tarif (Ps 59); **tanpa** DPP 11/12 | `references/pajak.md` | 2026-10-14 | Selaras DJP (tarif × jumlah dibayar) | **COCOK** |
| PBJT dibulatkan ke bawah sekali (`floor`) | Keputusan desain skill | — | UU/Perda tidak di-fetch naskah penuh run ini untuk metode pembulatan per nota | **PERLU REVIEW** — pertahankan disclaimer «belum dicocokkan Bapenda» |

**Usulan teks (Akun B):** Tidak wajub ubah rumus; bila README menyebut «10 %», tambah «sesuai Perda daerah, maksimum 10 % (UU 1/2022)».

---

## 2. `laporan-keuangan-emkm` — SAK EMKM

### 2.1 Kerangka & tanggal berlaku

| Klaim skill (`references/regulasi.md`, SKILL.md) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| SAK EMKM IAI; efektif **1 Januari 2018**; penerapan dini diperkenankan | IAI — Tentang SAK EMKM | 2026-10-14 | «SAK EMKM berlaku efektif per 1 Januari 2018 dan penerapan dini diperkenankan» — https://web.iaiglobal.or.id/SAK-IAI/Tentang%20SAK%20EMKM | **COCOK** |
| Disahkan 24 Okt 2016; hingga info IAI **belum ada revisi** | IAI — Produk SAK EMKM Disahkan | 2026-10-14 | «SAK EMKM disahkan … 24 Oktober 2016. Saat ini **belum ada revisi**» — https://web.iaiglobal.or.id/SAK-IAI/Produk%20SAK%20EMKM%20Disahkan | **COCOK** |
| Laporan minimum: **Posisi Keuangan**, **Laba Rugi**, **Catatan** (CaLK) | IAI daftar bab SAK EMKM | 2026-10-14 | Bab 3–6: Penyajian, Posisi Keuangan, Laba Rugi, Catatan — https://web.iaiglobal.or.id/SAK-EMKM-Efektif/SAK%20EMKM%20Efektif%20Per%201%20Januari%202018 | **COCOK** |
| Dasar akrual & biaya historis; pemisahan entitas/prive | IAI Tentang SAK EMKM | 2026-10-14 | «dasar pengukurannya murni menggunakan **biaya historis**»; konsep entitas bisnis / pisah pribadi | **COCOK** |
| Pos minimum laba rugi: pendapatan, beban keuangan, beban pajak | `regulasi.md` | 2026-10-14 | Selaras Bab 5 SAK EMKM (pos minimum) — naskah bab 5 tidak dibaca penuh run ini | **COCOK** dengan catatan |

### 2.2 Laporan Arus Kas (skill menambahkan)

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| Output default/script menyertakan **Laporan Arus Kas** (metode langsung) | SKILL.md; bukan bab terpisah di daftar 18 bab IAI | **PERLU UBAH** (Akun B, README saja): jelaskan arus kas = **pelengkap praktis** untuk bank/KUR, **bukan** salah satu dari tiga laporan wajib SAK EMKM |

### 2.3 PB1/PBJT di laporan keuangan

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| PB1/PBJT sebagai titipan/utang pajak daerah atau beban; tidak otomatis pendapatan | `regulasi.md` + praktik akuntansi | **COCOK** arah; rincian akun mengikuti SAK EMKM Bab 14/15 — **PERLU REVIEW** akuntan bila untuk audit bank |

**Usulan teks (Akun B):** Satu kalimat di README: «Laporan Arus Kas disertakan sebagai pelengkap; SAK EMKM mensyaratkan Laba Rugi, Posisi Keuangan, dan Catatan.»

---

## 3. `pengingat-pasien-klinik` — UU PDP, minimalisasi data, bukan rekam medis

**Run verifikasi:** 2026-10-15 ~00:00 UTC (Akun C, C30 butir 3).

### 3.1 Data kesehatan & pemrosesan minimal

| Klaim skill (`SKILL.md`, `scripts/pengingat_pasien.py`) | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Data kesehatan = data pribadi bersifat spesifik; perlindungan lebih ketat | UU 27/2022 Ps. 4 ayat (2) huruf a & Penjelasan | 2026-10-15 | «data dan informasi kesehatan» = catatan/keterangan individu terkait kesehatan fisik, mental, dan/atau pelayanan kesehatan — https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022 | **COCOK** |
| Persetujuan eksplisit per tujuan sebelum pemrosesan | UU 27/2022 Ps. 20 ayat (2) huruf a, Ps. 21–22 | 2026-10-15 | Pengendali wajib dasar pemrosesan; persetujuan sah eksplisit untuk tujuan tertentu | **COCOK** — skill wajib `--persetujuan ya\|tidak` saat pencatatan |
| Hak hapus / permintaan subjek data | UU 27/2022 Ps. 5 (hak), Ps. 43 ayat (1) huruf c | 2026-10-15 | Pengendali wajib menghapus bila ada permintaan Subjek Data Pribadi | **COCOK** — perintah `hapus --id/--wa` |
| Prinsip minimalisasi (hanya nama panggilan, WA, jenis kunjungan umum, tanggal; tanpa diagnosis/RM) | UU 27/2022 Ps. 16 ayat (2) huruf a–b (terbatas, spesifik, sesuai tujuan) | 2026-10-15 | Pemrosesan terbatas & spesifik, sesuai tujuan | **COCOK** — selaras desain CSV; menolak isian menyerupai penyakit |
| Draf WA disiapkan staf, bukan kirim otomatis | UU 27/2022 + keputusan pemilik OpenClaw (WA Web) | 2026-10-15 | Bukan norma UU khusus; praktik mengurangi risiko pemrosesan tanpa kontrol manusia | **COCOK** arah kepatuhan operasional |

### 3.2 Permenkes 24/2022 (rekam medis elektronik)

| Klaim skill | Sumber | Tanggal akses | Kutipan ringkas | Kesimpulan |
|---|---|---|---|---|
| Skill **bukan** pengganti RME; tidak menyimpan rekam medis | Permenkes 24/2022 Ps. 3 ayat (1) | 2026-10-15 | «Setiap Fasilitas Pelayanan Kesehatan wajib menyelenggarakan Rekam Medis Elektronik» — PDF resmi https://jdih.kemkes.go.id/documents/peraturan-menteri-kesehatan-nomor-24-tahun-2022 | **COCOK** — skill hanya buku jadwal pengingat lokal; faskes tetap wajib RME terpisah (SATUSEHAT/RME) |
| Kerahasiaan & keamanan data RM | Permenkes 24/2022 (tujuan pengaturan huruf c) | 2026-10-15 | «menjamin keamanan, kerahasiaan, keutuhan, dan ketersediaan data Rekam Medis» | **COCOK** — skill tidak mengklaim menggantikan RM |

**Usulan teks (Akun B):** Di README `pengingat-pasien-klinik`, satu kalimat: «Daftar pengingat ini bukan rekam medis elektronik; klinik tetap wajib RME sesuai Permenkes 24/2022.»

---

## 4. `edukasi-pasien-klinik` — edukasi bukan diagnosis, privasi & iklan

**Run verifikasi:** 2026-10-15 ~00:00 UTC (Akun C, C30 butir 3).

### 4.1 Batasan edukasi (bukan diagnosis / dosis)

| Klaim skill (`SKILL.md` baris 7–24) | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| Tanpa dosis, tanpa diagnosis, tanpa triase; arahkan ke tenaga kesehatan + tanda bahaya umum | Etika praktik & UU 17/2023 (kerahasiaan); bukan «izin diagnosis AI» | 2026-10-15 | UU tidak memberi AI hak diagnosis; skill membatasi diri ke draf edukasi/operasional | **COCOK** — selaras disclaimer skill & keputusan pemilik (edukasi pasien, bukan skrining awam) |
| Leaflet/konten dari poin yang **sudah ditentukan tenaga kesehatan** | Praktik edukasi pasien faskes | 2026-10-15 | Bukan menggantikan keputusan klinis | **COCOK** |
| Draf saja; staf yang kirim | Sama dengan pengingat-pasien | 2026-10-15 | **COCOK** |

### 4.2 UU PDP & data kesehatan (selaras `references/aturan-privasi-dan-iklan.md` §1)

| Klaim skill | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| Data kesehatan = spesifik; persetujuan/notifikasi (PP 33/2026 transisi) | UU 27/2022 Ps. 4; PP 33/2026 (undang 16 Jul 2026, berlaku 16 Jan 2027) — skill sudah catat | 2026-10-15 | Ps. 4 **COCOK**; tanggal PP **COCOK** dengan peraturan.go.id |
| Rekap agregat; abaikan kolom diagnosis/NIK | UU 27/2022 + UU 17/2023 Ps. 301 (kerahasiaan) — sudah diverifikasi di HASIL-UJI skill | 2026-10-15 | **COCOK** arah; regresi script tetap wajib (lihat HASIL-UJI B2 historis) |

### 4.3 Permenkes 24/2022 vs konten edukasi

| Klaim | Sumber | Kesimpulan |
|---|---|---|
| FAQ/leaflet/medsos edukasi umum **bukan** entri rekam medis | Permenkes 24/2022 (definisi RM sebagai catatan pelayanan kesehatan individu) | **COCOK** — asalkan tidak menempelkan RM/diagnosis pasien ke chat (skill melarang) |
| Konten medsos: nama & alamat faskes + tanggal publikasi | Permenkes 1787/2010 Ps. 4 ayat (2) — sudah diverifikasi naskah di HASIL-UJI | **COCOK** |

**Usulan teks (Akun B):** Pertahankan disclaimer «bukan nasihat medis/diagnosis» di README; untuk klaim PP 33/2026 tambah footnote «naskah PP diverifikasi ulang sebelum 16 Jan 2027».

---

## 5. `cek-privasi-openclaw` — UU PDP, UU ITE, PP pelaksana

**Run verifikasi:** 2026-10-15 ~00:30 UTC (Akun C, C30 butir 4).

### 5.1 Masa berlaku & transisi UU 27/2022

| Klaim skill (`references/uu-pdp.md`) | Sumber | Tanggal akses | Kesimpulan |
|---|---|---|---|
| UU PDP berlaku penuh sejak **Oktober 2024** | UU 27/2022 Pasal 74 (penyesuaian paling lama 2 tahun sejak diundangkan 17 Okt 2022); Pasal 76 (berlaku saat diundangkan) — JDIH Kemkomdigi | 2026-10-15 | **COCOK** — masa penyesuaian 2 tahun berakhir ±17 Okt 2024 |
| PP pelaksana «belum diverifikasi» | PP 33/2026 diundangkan 16 Jul 2026, berlaku 16 Jan 2027 (Pasal 225); peraturan.go.id / legaltrans salinan resmi | 2026-10-15 | **PERLU UBAH** — cantumkan PP 33/2026 + tanggal berlaku; UU tetap wajib sejak transisi berakhir, PP menambah operasional |

### 5.2 Kewajiban pengendali & hak subjek (ringkasan skill)

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| Dasar pemrosesan (persetujuan, kontrak, kewajiban hukum, dll.) | UU 27/2022 Pasal 20 ayat (2) a–f | **COCOK** |
| Informasi wajib bila berbasis persetujuan | Pasal 21 ayat (1) a–g | **COCOK** |
| Data pribadi spesifik (termasuk kesehatan) Pasal 4 | Pasal 4 UU 27/2022 | **COCOK** |
| Notifikasi kebocoran «hitungan hari» / cek ketentuan resmi | Pasal 46 ayat (1): paling lambat **3×24 jam** tertulis ke subjek data & lembaga | **PERLU UBAH** — ganti frasa vague menjadi «paling lambat 72 jam (3×24 jam)» dengan rujuk Pasal 46 |

### 5.3 Sanksi administratif

| Klaim skill | Sumber | Kesimpulan |
|---|---|---|
| Skill tidak memuat daftar sanksi (hanya disclaimer) | Pasal 57: peringatan, penghentian pemrosesan, penghapusan/pemusnahan, denda admin. maks. 2% pendapatan/penerimaan terkait | **COCOK** arah (pengingat, bukan nasihat); opsional README: satu kalimat «pelanggaran kewajiban pengendali dapat dikenai sanksi administratif UU PDP» |

### 5.4 Penolakan penyadapan chat (UU ITE)

| Klaim skill (`SKILL.md`, examples) | Sumber | Kesimpulan |
|---|---|---|
| UU ITE Pasal 31 (intersepsi ilegal) | UU 11/2008 jo. UU 19/2016 jo. **UU 1/2024** Pasal 31 ayat (1)–(2) — JDIH Komdigi | **COCOK** substansi; **PERLU REVIEW Akun B:** kutipan materi jualan sebut «UU ITE (UU 11/2008 jo. UU 1/2024) Pasal 31» agar mutakhir |

**Usulan teks (Akun B):** Perbarui `references/uu-pdp.md`: (1) PP 33/2026 & 16 Jan 2027; (2) Pasal 46 = 72 jam; (3) opsional satu baris Pasal 57; (4) rujuk UU ITE jo. 1/2024 di penolapan sadap.

---

## 6. `rekonsiliasi-bank` — praktik vs SAK EMKM (tanpa peraturan khusus)

**Run verifikasi:** 2026-10-15 ~00:30 UTC (Akun C, C30 butir 5).

Tidak ada UU/PP khusus «rekonsiliasi bank» untuk UMKM. Pemeriksaan: klaim skill vs praktik akuntansi SAK EMKM & privasi.

| Klaim skill | Sumber / acuan | Kesimpulan |
|---|---|---|
| «Bukan audit» / «bukan nasihat akuntansi» (`README.md`, `SKILL.md`) | Skill memang operasional matching CSV, bukan opini audit | **COCOK** |
| Laporan laba/neraca → arahkan ke `laporan-keuangan-emkm` | Pemisahan fungsi selaras praktik: rekonsiliasi kas ≠ laporan keuangan lengkap | **COCOK** |
| Mutasi rekening = data pribadi (UU PDP) — `references/format-bank.md` | UU 27/2022 (data keuangan pribadi = spesifik, Pasal 4) | **COCOK** arah |
| «Angka seimbang» = penjelasan aritmetika selisih, bukti pasangan benar | Bukan klaim SAK EMKM; selaras praktik rekonsiliasi kas sebelum tutup buku | **COCOK** |
| Tidak mengklaim wajib rekonsiliasi menurut SAK EMKM | SAK EMKM (IAI) menekankan pengendalian kas & catatan; rekonsiliasi bank adalah praktik wajar tetapi skill tidak perlu mengutip pasal SAK | **COCOK** — tidak ada klaim salah; opsional README: «rekonsiliasi membantu tutup buku kas, bukan pengganti SAK EMKM» |

**Usulan teks (Akun B):** Tidak wajib; bila ingin: satu kalimat di README bahwa hasil ini alat bantu operasional, bukan bukti audit atau laporan keuangan SAK EMKM.

---

## Progress C30

| # | Skill | Status run |
|---|---|---|
| 1 | kasir-lokal | ✅ verifikasi run 23:30 UTC |
| 2 | laporan-keuangan-emkm | ✅ verifikasi run 23:30 UTC |
| 3 | pengingat-pasien-klinik + edukasi-pasien-klinik | ✅ verifikasi run 00:00 UTC 2026-10-15 |
| 4 | cek-privasi-openclaw | ✅ verifikasi run 00:30 UTC 2026-10-15 |
| 5 | rekonsiliasi-bank | ✅ verifikasi run 00:30 UTC 2026-10-15 |
| 6 | kelayakan-investasi-usaha | belum |
