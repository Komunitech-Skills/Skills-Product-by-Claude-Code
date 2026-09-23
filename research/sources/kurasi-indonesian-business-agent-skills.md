# Kurasi: adamriofc/indonesian-business-agent-skills

Tanggal tinjau: 2026-09-23 · Peninjau: agent kurator · Status: **menunggu keputusan koordinator/pemilik**

## 1. Identitas

| Item | Isi |
|---|---|
| Nama | Indonesian Business Agent Skills: 88 skill dalam 6 plugin (`legal-id`, `tax-id`, `hr-id`, `finance-id`, `marketing-id`, `strategic-id`) + 39 "engine" Node.js + rule JSON |
| URL | https://github.com/adamriofc/indonesian-business-agent-skills |
| Ditemukan lewat | Pencarian GitHub `topic:agent-skills indonesia` |
| Pembuat | adamriofc |
| Update terakhir | 2026-08-16 (dibuat 2026-08-09; `package.json` v6.16.3). Sekitar 30 commit dalam 13–16 Agustus 2026. |
| **Lisensi (file LICENSE dibaca langsung)** | **MIT**, "Copyright (c) 2026 adamriofc". `package.json` juga `"license": "MIT"`. |
| Popularitas | 1 bintang, 0 fork |

### Ringkasan isi
- **tax-id (16):** pph21-calculator (TER PMK 168/2023), pph21-grossup, pph23-26, pph-final-umkm (PP 20/2026), pph-badan, ppn-ppnbm-advanced (DPP nilai lain 11/12), efaktur-helper, laporan-keuangan-psak, transfer pricing, tax planning, dan lain-lain.
- **hr-id (13):** bpjs-calculator, thr-calculator, phk-calculator/phk-advanced-matrix (PP 35/2021), pkwt/pkwtt checker, surat-peringatan, sop-perusahaan, struktur-skala-upah, interview.
- **legal-id (9):** contract-reviewer, nda-indonesia, somasi-draft-id, spk-generator, oss-kbli-navigator, pdp-compliance, haki-trademark-check.
- **marketing-id (27):** whatsapp-broadcast, shopee-live-script, tokopedia-seo-optimizer, tiktok-shop-affiliate, margin-pricing-calculator, cs-komplain-handler, dan lain-lain.
- **finance-id (15) dan strategic-id (10):** rasio keuangan, arus kas, BEP, NPV/IRR, Porter, BCG, VRIO, dan lain-lain.
- `engines/rules/*.json`: tarif berversi dengan tanggal berlaku dan sumber (pph21, bpjs, umkm, marketplace, btki). `tests/golden/` berisi 27 file kasus uji, plus PROVENANCE.md (tautan ke peraturan).

## 2. Audit keamanan (Tahap 3)

Metode: repo di-clone dangkal ke scratchpad di luar repo, **dibaca saja**, dan tidak ada `npm install`/`node` yang dijalankan.

| Pemeriksaan | Hasil |
|---|---|
| Dependensi | `package-lock.json` tanpa paket pihak ketiga (0 `resolved`). Engine memakai Node murni. |
| Jaringan | **Hanya di script pengembang** `scripts/benchmark.js` dan `scripts/llm-benchmark-eval.js`: memanggil endpoint LLM (`/chat/completions`) memakai `LLM_BENCH_KEY` / `LLM_EVAL_KEY` dari env, dan hanya jika diset. Tidak dipanggil oleh skill. **Jangan ikut disalin.** |
| Eksekusi perintah | `scripts/validate-release.js` dan `generate-release-manifest.js` memakai `execSync` untuk `git`, `npm audit`, dan `bash scripts/sha256sums.sh`. Ini alat rilis internal, bukan bagian skill. **Jangan ikut disalin.** |
| Engine (`engines/*.js`) | Tidak ada `fetch`, `child_process`, `eval`, atau akses `homedir`/SSH/env yang mencurigakan. |
| Kredensial / API key tertanam | Tidak ada. |
| Prompt injection | Tidak ada di SKILL.md. Teks "Ignore all previous instructions" hanya ada di `fixtures/adversarial/` sebagai **data uji** ketahanan terhadap injeksi. |
| Karakter tersembunyi | Tidak ada. |
| Catatan izin | Semua 88 SKILL.md memuat `allowed-tools: bash` dan 33 di antaranya menyuruh agent menjalankan `engines/*.js`. Ini tidak jahat, tetapi melanggar standar kita (Python standar saja, frontmatter hanya `name` dan `description`). |

**Hasil: LULUS**, dengan syarat folder `scripts/`, `.github/`, dan konfigurasi benchmark tidak dipakai.

## 3. Penilaian

- **Kualitas SKILL.md: 5/10.** Berbahasa Inggris, bernada teknis/korporat, banyak frontmatter non-standar (`argument-hint`, `risk_level`, `capability`, dan lain-lain), serta boilerplate "Trust Envelope" yang disalin ke semua skill (THR pun mencontohkan kerangka PPh 21). Isi per skill tipis (43–105 baris). Bergantung pada Node. Tidak cocok untuk pembeli awam.
- **Kualitas data/logika: 7/10 (perlu verifikasi).** Rule berversi dan bertanggal sejalan dengan riset kita:
  - PPN 12% dengan DPP nilai lain 11/12 = efektif 11% (cocok dengan PMK 131/2024).
  - UMKM: PP 20/2026 berlaku 2026-04-22, subjek OP/PT perorangan/koperasi, ambang Rp500 juta, batas Rp4,8 M (cocok dengan `regulasi-2026-09-23.md`).
  - BPJS: JP cap bertahap 2024/2025/2026, tarif JHT/JP/JKK/JKM/Kesehatan cocok.
  - PPh 21: kategori TER A/B/C dan tarif Pasal 17 benar.
- **Tanda bahaya mutu:**
  1. README sendiri mengakui "Independent external domain validation ... still pending".
  2. Dibangun sangat cepat (v6.16.3 dalam kurang dari 1 minggu, 88 skill). Kemungkinan besar dihasilkan AI secara massal.
  3. Sumber batas upah JP 2026 tidak konsisten: ID `SE B/3307/022026`, tetapi tautannya berjudul `B/1226/022026` dan berupa mirror HubSpot pihak ketiga.
  4. Tarif komisi marketplace (`MKPL-FEE-2024`, "Infinity") hampir pasti sudah berubah.
- **Tumpang tindih dengan katalog kita:** `hitung-ppn` ↔ ppn-ppnbm; `pph-final-umkm` ↔ pph-final-umkm; `surat-peringatan-karyawan` ↔ surat-peringatan; `sop-writer` ↔ sop-perusahaan; `broadcast-wa` ↔ whatsapp-broadcast; `naskah-live-jualan` ↔ shopee-live-script; `harga-jual-marketplace` ↔ margin-pricing-calculator; `laporan-keuangan-emkm` ↔ laporan-keuangan-psak; `balas-chat-cs` ↔ cs-komplain-handler; `perjanjian-sederhana` ↔ nda/spk.
- **Mengisi celah backlog kita:** kalkulator **PPh 21 TER, BPJS, THR, pesangon/PHK, PKWT**; draf somasi dan NDA; navigator KBLI/OSS; checklist UU PDP.

**Keputusan: KURASI SELEKTIF (lisensi MIT mengizinkan komersial).** Yang diambil hanya **logika hitung, tabel tarif berversi, dan kasus uji emas** sebagai bahan skill kalkulator kita. SKILL.md-nya **tidak** dijual apa adanya.

## 4. Usulan nilai tambah (skill turunan)

Prioritas: `hitung-thr`, `hitung-bpjs`, `hitung-pesangon`, `hitung-pph21` (tabel TER), dan pembaruan `hitung-ppn`/`pph-final-umkm` kita.
1. **Port ke Python standar** (`scripts/*.py`, lintas OS, tanpa paket), dengan antarmuka tanya-jawab bahasa awam dan output slip/tabel siap cetak.
2. **Verifikasi independen setiap angka** terhadap dokumen resmi (PMK 168/2023 lampiran TER, PP 35/2021, Permenaker 6/2016, SE BPJS TK batas upah JP 2026, PP 20/2026) sebelum dipakai. Golden test mereka menjadi pembanding tambahan, bukan sumber kebenaran.
3. Konteks lokal: UMP/UMK tidak di-hardcode (arahkan ke SK Gubernur), contoh kasus warung/toko/klinik, dan disclaimer pajak/ketenagakerjaan dengan tanggal berlaku.
4. Buang frontmatter non-standar, `allowed-tools: bash`, "Trust Envelope" korporat, dan ketergantungan Node.
5. Legal (somasi, NDA, SPK): **inspirasi struktur saja**. Tulis ulang dengan template berbahasa Indonesia dan dasar hukum yang diverifikasi, plus arahan ke advokat.
6. Usulan tier: kalkulator HR/pajak sebagai **ECER** atau "Paket Admin Kantor/HR". PPh 21 dan pesangon kandidat **VIP**.

## 5. Kewajiban lisensi jika dipakai
- Sertakan teks MIT asli (Copyright (c) 2026 adamriofc) dan atribusi di `ATTRIBUTION.md` skill turunan. Sebutkan file/tabel mana yang diadaptasi.
- Catat `jalur=kurasi`, `lisensi=MIT`, `sumber_url` repo ini di `catalog.csv`.
