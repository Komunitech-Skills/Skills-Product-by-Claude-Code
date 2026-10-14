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

## Progress C30

| # | Skill | Status run |
|---|---|---|
| 1 | kasir-lokal | ✅ verifikasi run 23:30 UTC |
| 2 | laporan-keuangan-emkm | ✅ verifikasi run 23:30 UTC |
| 3 | pengingat-pasien-klinik + edukasi-pasien-klinik | belum |
| 4 | cek-privasi-openclaw | belum |
| 5 | rekonsiliasi-bank | belum |
| 6 | kelayakan-investasi-usaha | belum |
