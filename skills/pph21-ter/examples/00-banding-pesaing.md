# 00 — Uji banding pesaing: PPh 21 TER

Tanggal: 2026-09-23 · Penguji: agent penguji independen (simulasi, Claude Code)

## Pencarian
- GitHub code search `filename:SKILL.md PPh 21 TER` (1.392 hasil, disaring yang relevan), repo search `pph21 ter calculator`, kurasi internal (riset internal kurator, tidak disertakan dalam paket).
- Juga dicek sesuai brief: github.com/anthropics/skills, VoltAgent/awesome-openclaw-skills, ClawHub/skills.sh, manairalabs/bicara-skills, alvinindra/bahasa-skills → tidak ada skill PPh 21/payroll Indonesia.
- Pesaing relevan yang ditemukan dan dibaca (tidak ada script pihak ketiga yang dijalankan; logika mesin mereka dibaca lalu ditiru di Python penguji hanya untuk membandingkan angka):

| Pesaing | URL | Lisensi | Sinyal |
|---|---|---|---|
| A. adamriofc/indonesian-business-agent-skills — `tax-id/skills/pph21-calculator` + `engines/pph21-calculator.js` + `engines/rules/pph21.json` | https://github.com/adamriofc/indonesian-business-agent-skills | MIT | 1 bintang, dibuat Agustus 2026 |
| B. openaccountants/openaccountants — `agent-skills/id-payroll-pph21/SKILL.md` | https://github.com/openaccountants/openaccountants | AGPL-3.0 (kode) / OpenAccountants Guide License (konten) — **tidak boleh disalin ke produk kita** | "source-cited draft", belum direview konsultan |

## S1 dijalankan dengan instruksi pesaing
Permintaan: K/1, gaji Rp 12 jt, THR Rp 12 jt di Maret, iuran JHT+JP Rp 360 rb/bulan, PPh 21 setahun 2026.

| Bulan | Skill kita (`pph21-ter`) | Pesaing A (adamriofc) | Pesaing B (openaccountants) | Benar (kalkulator independen dari PDF resmi) |
|---|---:|---:|---:|---:|
| Jan–Feb, Apr–Nov | Rp 360.000 (TER B 3%) | Rp 240.000 (tabel B mereka: 2%) | Rp 360.000 (tabel B parsial benar di rentang ini) | Rp 360.000 |
| Maret (24 jt) | Rp 2.160.000 (9%) | Rp 1.680.000 (7%) | Rp 2.160.000 | Rp 2.160.000 |
| Desember | Rp 642.000 | Rp 2.322.000 | Rp 642.000* | Rp 642.000 |
| Setahun | Rp 6.402.000 | Rp 6.402.000 | Rp 6.402.000* | Rp 6.402.000 |

\*Pesaing B hanya bila agent memakai iuran Rp 360 rb yang disebut pengguna; contoh resmi di SKILL.md mereka sendiri hanya mengurangkan JP (bukan JHT) dan tidak memasukkan premi JKK/JKM/BPJS Kes ke bruto — pada contoh mereka (TK/0, Rp 10 jt) mereka menulis PPh bulanan Rp 200.000 dan Desember Rp 740.000, padahal yang benar (bruto termasuk premi Rp 10.484.000, TER 2,5%) Rp 262.100/bulan dan Desember Rp 448.100.

## Uji akurasi massal (sama untuk semua)
- Tabel TER pesaing A dibandingkan dengan tabel yang penguji urai sendiri dari PDF PP 58/2023: **kategori A sama, kategori B salah (34 baris vs 40 resmi), kategori C salah (37 vs 41)**. Pada 5.000 kasus bulanan acak, PPh 21 pesaing A berbeda dari yang benar pada **3.119 kasus (62%)**; khusus kategori B/C gaji Rp 5–30 jt: **2.225 dari 3.000 (74%) salah**. Desember pesaing A dipaksa ≥ 0 (tidak ada pengembalian lebih potong), biaya jabatan selalu maks Rp 6 jt (tidak ada pegawai baru/berhenti), tidak ada TER harian dan DTP.
  - Contoh resmi PMK 168 Tuan B (mulai September): benar lebih potong Rp 2.975.000 → pesaing A Rp 0. Tuan D (berhenti Agustus): benar lebih potong Rp 3.620.000 → pesaing A tidak punya mode berhenti kerja.
- Pesaing B: tabel hanya "selected rates" (tidak lengkap di atas Rp 27,7 jt untuk B), batas JP masih Rp 10.547.400 (lama), menyarankan **"Mid-year joiner: pro-rate PTKP"** — bertentangan dengan PMK 168 Lampiran I.2 angka 6a (PTKP penuh, tidak disetahunkan), dan tanpa script.
- Skill kita: 0 selisih dari ±15.000 kasus acak + 500 CSV + semua contoh resmi PMK 168/2023 & PMK 105/2025 (lihat HASIL-UJI.md).

## Penilaian

| Kriteria | Skill kita | Pesaing A | Pesaing B |
|---|---|---|---|
| Kualitas output (siap pakai, format) | 9 | 5 (JSON "trust envelope", bahasa Inggris) | 6 (referensi panjang, tanpa script) |
| Kesesuaian konteks Indonesia (bahasa, awam, DTP 2026, harian, resign) | 9 | 4 | 4 |
| Akurasi | 10 | 2 (tabel B/C salah) | 5 (bruto & pegawai baru keliru) |
| Siap pakai untuk pembeli awam | 9 | 3 (butuh Node.js, `allowed-tools: bash`) | 4 |

**Kesimpulan: skill kita menang telak.**

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- Pesaing A: tarif disimpan berversi dengan tanggal berlaku (`effective_from/to`) dan hash integritas — ide bagus untuk memudahkan pembaruan tahunan (mis. batas JP) dan menolak berjalan bila tabel rusak. Skill kita sudah punya uji hash tabel di test; bisa ditambah pemilihan aturan otomatis berdasarkan tanggal.
- Pesaing A: menandai hasil berisiko tinggi dengan "perlu review manusia" — kita bisa menambahkan satu baris tegas di output Desember/berhenti kerja.
- Pesaing B: tabel kata kunci klasifikasi penghasilan (bonus, THR, lembur, natura) — ide untuk bagian FAQ "apa saja yang masuk bruto".
