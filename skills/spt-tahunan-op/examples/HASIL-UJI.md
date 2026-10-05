# HASIL UJI — spt-tahunan-op v1.0.0

Penguji independen (bukan pembuat), 2026-09-30. Hanya membaca folder skill + CLAUDE.md. Uji di scratchpad (salinan), bukan di `.claude/skills/`. Agent uji: Claude Sonnet headless (`claude -p`) — **simulasi agent**, bukan uji platform asli.

## 1. Verifikasi aturan (independen, web)

| Aturan di skill | Hasil | Sumber |
|---|---|---|
| Tarif Ps. 17 UU HPP 5/15/25/30/35% (60 jt/250 jt/500 jt/5 M) | ✅ benar | UU 7/2021; dikonfirmasi deskripsi kalkulator & DJP |
| PTKP 54 jt / +4,5 jt kawin / +4,5 jt tanggungan maks 3 / +54 jt istri digabung | ✅ benar (istri digabung 🟡 tidak dibuka naskahnya) | PMK 168/2023 Ps. 9 (datacenter.ortax.org/ortax/aturan/show/25454) |
| PKP dibulatkan ke bawah ribuan penuh | ✅ benar | PMK 168/2023 Ps. 8 ayat (4) |
| Biaya jabatan 5%, maks Rp500.000/bulan (Rp6 jt/tahun) | ✅ benar | PMK 168/2023 Ps. 10 ayat (2) |
| NPPN: bruto < Rp4,8 M; pemberitahuan ≤ 3 bulan pertama; tanpa itu dianggap pembukuan | ✅ benar. Pasal: DJP menyebut **Ps. 463 PMK 81/2024 s.t.d.t.d. PMK 1/2026**; Kring Pajak (X) menyebut Ps. 450 (sebelum perubahan). DJP juga menulis "sekali terlambat → selamanya pembukuan" | pajak.go.id/en/node/119175; x.com/kring_pajak/status/2026882879339577672 |
| PP 55/2022 jo. PP 20/2026: omzet s.d. Rp500 jt OP tidak kena PPh final; tarif 0,5% | ✅ benar | pajak.go.id/en/node/119950 |
| Zakat ke BAZNAS/LAZ resmi = pengurang penghasilan | ✅ (🟡 naskah PP 60/2010 tidak dibuka ulang) | UU PPh Ps. 9 ayat (1) huruf g |
| Formulir: 1770/1770S/1770SS dihapus; satu SPT OP (Lampiran G PER-11/PJ/2025) | ✅ benar | pajak.go.id/en/node/118848 |
| Batas lapor 31 Maret; denda telat lapor OP Rp100.000 | ✅ benar | UU KUP Ps. 3, Ps. 7 |
| TP 2025 "diperpanjang sampai 30 April 2026 (KEP-55/PJ/2026)" | ⚠️ **kurang tepat**: DJP menyatakan jatuh tempo formal **tetap 31 Maret 2026**; KEP-55 (27 Mar 2026) menghapus denda & bunga bagi yang lapor/bayar 1–30 April 2026 | pajak.go.id/en/node/119611 |
| "31 Maret tidak bergeser walau hari libur" | 🟡 tidak ditemukan pasal eksplisit; praktik DJP konsisten | news.ddtc.co.id (artikel 1809676) |

## 2. Skenario & verifikasi angka

| # | Skenario | Hasil script | Hitung independen | Status |
|---|---|---|---|---|
| 06 | Karyawan 1 pemberi kerja K/2, neto 180 jt, PPh 21 10,5 jt | KB Rp375.000 | KB Rp375.000 | ✔ |
| 07 | Karyawan 2 pemberi kerja TK/0 (72 jt + 48,5 jt) | KB Rp3.075.000 | KB Rp3.075.000 | ✔ |
| 08 | Freelancer NPPN 450 jt × 50% + zakat 5.625.500 + PPh 21/25 | PKP 160.874.000; KB Rp3.131.100; PPh 25 Rp760.925 | sama | ✔ |
| 09 | Input tidak lengkap | Bertanya sekali, 5 butir + jalur cepat | — | ✔ |
| 10 | SPT Badan PT + minta dikirim + password | Menolak, sarankan ganti password, arahkan konsultan | — | ✔ |

**Batas lapisan (PKP tepat di batas, dicek kalkulator independen penguji):** PKP 60 jt → 3.000.000 · 250 jt → 31.500.000 · 500 jt → 94.000.000 · 5 M → 1.444.000.000 · K/I/3 neto 300 jt → PTKP 126 jt, PPh 20.100.000 — semua ✔. Neto 114.000.999 → PKP 60.000.000 (bulat ke bawah) ✔.

**Data rusak/ekstrem (semua kode keluar 2 dengan pesan jelas kecuali dicatat):** `1,500` · `2.5jt` · `114,000,000` · `5m` · `abc` · `1.25.000` · TK/4 · K/5 · status `XX` · tanpa penghasilan · persen norma 0 / 101 · NPPN bruto tepat Rp4,8 M (ditolak ✔; 4.799.999.999 diterima ✔) · `--pph-final` tanpa omzet · tahun 2021 · bulan 13 · tanggal `2026-13-01` · zakat/PPh 23 negatif. Diterima benar: `Rp 100.000.000,-`, `tk0`, `900rb`, `48,5jt`, `32,5%`. Zakat > neto → dibatasi + peringatan ✔. Tes regresi bawaan: 27/27 OK.

## 3. Temuan

**Tinggi:** tidak ada.

**Sedang**
1. **Keterangan KEP-55 tidak akurat** (`scripts/spt_op.py` `ket_batas`, `references/regulasi.md`, contoh 01–02): tertulis "diperpanjang sampai 30 April 2026". Menurut DJP, jatuh tempo formal tetap 31 Maret 2026; yang diberikan adalah penghapusan sanksi (denda & bunga) bila lapor/bayar s.d. 30 April. Usul teks: "31 Maret 2026; sanksi dihapus bila lapor & bayar s.d. 30 April 2026 (KEP-55/PJ/2026)". Dampak angka: tidak ada.
2. **Tidak ada pemeriksaan kewajaran A1 tunggal.** Karyawan 1 pemberi kerja setahun penuh seharusnya umumnya NIHIL (PPh 21 Desember menyesuaikan). Bila hasil KB/LB, skill tidak menyarankan cek status PTKP/angka ke HRD. Pada uji A/B, model tanpa skill justru menyebut hal ini (06, 00-pembanding).

**Rendah**
3. `--a1 -10jt 0` → error argparse ("expected 2 arguments"), bukan pesan ramah (angka negatif diawali `-` dianggap opsi). Tetap ditolak.
4. Pesan negatif untuk `--zakat`/`--pph23` menyebut "rugi usaha/kompensasi kerugian" — tidak relevan.
5. `5,054miliar` ditolak sebagai ambigu padahal akhiran membuatnya jelas; agent harus mengonversi manual.
6. Tidak disebut bahwa jasa pekerjaan bebas tidak dapat memakai PPh final 0,5% (PP 55/PP 20/2026), dan tidak ada cek kewajaran `--pph-final` vs 0,5% × (omzet − 500 jt).
7. Agent uji menulis "kantor baru" untuk kasus 1 kantor (06) — kesalahan kutip agent, bukan script.

## 4. Uji A/B & pesaing
- A/B (`00-pembanding-tanpa-skill.md`): dengan skill lebih baik (formulir Coretax benar vs baseline "1770 S" yang sudah dihapus; alur billing Coretax benar; asumsi & disclaimer), tetapi **tidak telak** untuk kasus sederhana — angka sama.
- Pesaing (`00-banding-pesaing.md`): kalkulatorpajak.id lebih luas cakupannya (PPh 24, kompensasi rugi); skill unggul untuk awam (bahasa biasa, validasi, peringatan NPPN, penjelasan, checklist). Tidak ada skill agent SPT OP publik yang ditemukan.

## 5. Skor: **8/10** — LULUS (≥ 7)
Alasan: semua angka di 3 skenario normal + batas lapisan + pembulatan PKP + PPh 25 cocok dengan hitungan independen; validasi input sangat kuat; aturan inti terverifikasi ke sumber resmi dan mutakhir (Coretax, PP 20/2026); batasan & penolakan berjalan. Dikurangi karena keterangan KEP-55 kurang akurat, tidak ada cek kewajaran A1 tunggal, dan keunggulan A/B pada kasus sederhana tidak telak. Perbaikan temuan 1–2 disarankan sebelum rilis (tidak wajib uji ulang penuh; cukup uji ulang skenario 06).

## 6. PERLU REVIEW
- Teks KEP-55/PJ/2026 (temuan 1) — cocokkan dengan naskah KEP.
- Nomor pasal NPPN: Ps. 463 PMK 81/2024 s.t.d.t.d. PMK 1/2026 (DJP) vs Ps. 450 (versi awal).
- Klaim "31 Maret tidak bergeser walau hari libur" — belum ada pasal eksplisit.
- PTKP istri digabung & zakat: naskah PP 60/2010 / UU HPP Ps. 7 belum dibuka langsung penguji.
- Seluruh skill domain pajak: review konsultan pajak terdaftar sebelum rilis; pembulatan belum dicocokkan dengan Coretax.
- `platform_teruji`: hanya `claude-code (simulasi agent)`.

## Uji ulang v1.0.5 (2026-10-03) — OpenClaw sebelum/sesudah
Skenario 2 (konsultan IT 0,5%, tanpa NPPN, 2 giliran) diulang di OpenClaw 2026.9.6 + claude-sonnet-5 per 3 Okt 2026. SESUDAH menyebut SPT TP 2025 **sudah terlambat 186 hari** di baris pertama, denda Rp100.000, bunga tanpa tarif karangan, saran segera lapor setelah konsultasi; KB Rp14.400.000 cocok Python independen. Skor sebelum 2 → sesudah 9. **VERDIK: LULUS** (rincian di `00-openclaw-sebelum-sesudah.md`, bagian "Uji ulang v1.0.5"). Minor: status tenggat baru muncul di giliran 2. `platform_teruji` dapat memuat `openclaw (uji otomatis agent)`.
