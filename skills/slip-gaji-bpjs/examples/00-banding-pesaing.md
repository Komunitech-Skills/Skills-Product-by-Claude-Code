# 00 — Uji banding pesaing: slip gaji + BPJS

Tanggal: 2026-09-23 · Penguji: agent penguji independen (simulasi, Claude Code)

## Pencarian
GitHub code search `filename:SKILL.md PPh 21 TER`, `SKILL.md BPJS payroll`, repo search `pph21 ter calculator`; kurasi internal `research/sources/kurasi-indonesian-business-agent-skills.md`; dicek juga anthropics/skills, VoltAgent/awesome-openclaw-skills, ClawHub/skills.sh, manairalabs/bicara-skills, alvinindra/bahasa-skills (tidak ada skill slip gaji Indonesia). Script pihak ketiga **tidak dijalankan**; logika dibaca lalu ditiru di Python penguji untuk membandingkan angka.

| Pesaing | URL | Lisensi |
|---|---|---|
| A. adamriofc/indonesian-business-agent-skills — `hr-id/skills/bpjs-calculator` + `engines/bpjs-calculator.js` (+ `tax-id/skills/pph21-calculator` untuk pajak) | https://github.com/adamriofc/indonesian-business-agent-skills | MIT |
| B. openaccountants/openaccountants — `agent-skills/id-payroll-pph21` (PPh 21 + BPJS) | https://github.com/openaccountants/openaccountants | AGPL-3.0 / OpenAccountants Guide License (tidak boleh disalin) |

## S1 dengan instruksi pesaing
Pesaing A tidak punya slip gaji, lembur, atau UMK; agent memakai `bpjs-calculator` (dasar = upah yang diberikan, tanpa batas bawah UMK) dan `pph21-calculator` (bruto = gaji yang diberikan; tabel TER B mereka keliru). Pesaing B memberi rumus & contoh, tanpa script; contohnya tidak memasukkan premi ke bruto.

| Karyawan | Angka | Skill kita | Pesaing A | Pesaing B (mengikuti contohnya) | Benar |
|---|---|---:|---:|---:|---:|
| Budi K/1 | PPh 21 | Rp 53.707 | Rp 51.711 | Rp 51.710 | Rp 53.707 |
| Budi | THP | Rp 6.521.091 | Rp 6.523.087 | Rp 6.523.088 | Rp 6.521.091 |
| Siti TK/0 | BPJS Kes 1% | Rp 53.968 | Rp 51.000 | Rp 51.000 | Rp 53.968 |
| Siti | PPh 21 | Rp 28.793 | Rp 13.750 | Rp 13.750 | Rp 28.793 |
| Dewi K/2 | PPh 21 | Rp 361.850 | Rp 231.069 (tabel B salah: 2%) | Rp 288.836 | Rp 361.850 |
| Dewi | THP | Rp 10.521.618 | Rp 10.652.399 | Rp 10.594.632 | Rp 10.521.618 |
| Semua | Slip siap cetak/CSV | Ya | Tidak | Tidak | — |

Uji massal skill kita: 3.000 slip acak (gaji, tunjangan tidak tetap, lembur hari kerja pecahan jam, lembur libur pola 5/6 hari, bonus, UMK, 5 tarif JKK, periode sebelum/sesudah kenaikan batas JP) dibandingkan dengan kalkulator payroll independen penguji: **0 selisih**. Pesaing A: tarif BPJS dan batas JP 2026 (Rp 11.086.300) benar, tetapi tanpa batas bawah UMK dan PPh 21-nya salah pada mayoritas kasus kategori B/C.

## Penilaian

| Kriteria | Skill kita | Pesaing A | Pesaing B |
|---|---|---|---|
| Kualitas output | 9 (slip MD/HTML/CSV) | 4 (JSON) | 5 (teks referensi) |
| Kesesuaian konteks Indonesia (lembur PP 35/2021, UMK, DTP, Desember) | 9 | 4 | 4 |
| Akurasi | 9 | 3 | 5 |
| Siap pakai | 9 | 3 (butuh Node.js) | 4 |

**Kesimpulan: skill kita menang telak.**

## Yang bisa dipelajari (ide)
- Pesaing A: aturan BPJS disimpan per periode berlaku (`effective_from/to`) sehingga periode lampau otomatis memakai batas JP lama — skill kita sudah punya `BATAS_JP` berperiode; bisa diperluas ke tarif lain (mis. diskon JKK padat karya bila diperpanjang).
- Pesaing A: menolak berjalan bila tanggal/aturan tidak ada ("fail-closed") — skill kita sudah melakukannya untuk batas JP; pertahankan pola ini untuk DTP (lihat cacat di HASIL-UJI).
