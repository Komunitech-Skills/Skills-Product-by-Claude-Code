# HASIL UJI ULANG — spt-tahunan-op

## Uji ulang 1.0.1 (2026-09-30)

Penguji independen (bukan pembuat). Salinan skill diuji di scratchpad (`uji-spt-101/`), bukan di `.claude/skills/`. Input semuanya baru (bukan dari contoh 01–10). Simulasi agent + jalankan script langsung.

### Ringkasan
- Tes bawaan: **43/43 OK** (`python3 scripts/test_spt_op.py`). `python3 scripts/validate.py --skill spt-tahunan-op` → ✅ valid.
- Temuan 1.0.0 no. 1–6: **semua diperbaiki**. Tidak ada regresi angka.

### 1. Tenggat TP 2025 (temuan 1.0.0 #1) — ✅ diperbaiki
- Sumber resmi DJP (pajak.go.id/en/node/119611): *"Jatuh tempo formal … tahun pajak 2025 dan pembayaran PPh Pasal 29 tetap 31 Maret 2026"*; *"KEP-55/2026 bukan memindahkan jatuh tempo menjadi 30 April 2026"*; sanksi denda/bunga dihapus bila lapor/bayar s.d. 30 April 2026. Teks skill (SKILL.md, references/regulasi.md, script) kini sesuai.
- `grep -rni "diperpanjang"` seluruh folder: tidak ada di SKILL.md, README, references, script (selain `assertNotIn` di tes). Sisa kata hanya di catatan historis `HASIL-UJI.md`, `00-pembanding-tanpa-skill.md` (sudah diberi anotasi koreksi v1.0.1) dan `06-uji-...md` (log uji 1.0.0) — wajar.
- Status script (`--status TK/0 --a1 100jt 2.000.000`, TP 2025):

| `--hari-ini` | Keterangan batas | Peringatan telat |
|---|---|---|
| 2026-03-15 | 31 Maret 2026 (jatuh tempo formal tetap) + info KEP-55 | tidak ada ✔ |
| 2026-04-15 | "JATUH TEMPO SUDAH LEWAT (masih masa bebas sanksi s.d. 2026-04-30)" | tidak ada ✔ |
| 2026-05-05 | "JATUH TEMPO SUDAH LEWAT" | ada: masa bebas sanksi berakhir, denda Rp100.000, bunga ✔ |

### 2. Saran cek A1 ke HRD, 1 pemberi kerja (temuan #2) — ✅ diperbaiki
| Kasus | Hasil | Peringatan "CEK ULANG … HRD" |
|---|---|---|
| TK/0, A1 neto 100 jt, PPh 21 2.000.000 | KB Rp300.000 | muncul ✔ |
| K/0, A1 neto 120 jt, PPh 21 5.000.000 | LB Rp1.775.000 (dicek manual) | muncul ✔ |
| TK/0, A1 neto 100 jt, PPh 21 2.300.000 | NIHIL | tidak muncul ✔ |
| 2 A1 / A1 + NPPN / K/I | KB | tidak muncul ✔ (sesuai desain) |
| `--a1-bruto` 1 kantor | KB | muncul + saran minta angka neto ✔ |
| 1 A1 + `--zakat` atau `--pph25` | KB | **tidak muncul** (lihat temuan R1) |
SKILL.md Langkah 3 juga menginstruksikan agent menjelaskan dengan bahasa awam dan tidak langsung menyuruh bayar ✔.

### 3. Pesan error ramah (temuan #3–5) — ✅ diperbaiki
| Input | Hasil |
|---|---|
| `--a1 -10jt 0`, `--a1 10jt -5` | kode 2, "angka tidak boleh negatif (-10jt). Isi dengan angka positif, mis. 5jt…" ✔ (bukan lagi error argparse) |
| `--zakat -1jt`, `--pph23 -500rb` | pesan sama, tidak lagi menyebut "rugi usaha" ✔ |
| `5,054 miliar`, `5,054miliar` | diterima = Rp5.054.000.000 ✔ |
| `5,054M`, `5M`, `2,5M` | kode 2, "ambigu (M = juta atau miliar?)" + contoh benar ✔ |

### 4. PPh final 0,5% vs pekerjaan bebas (temuan #6) — ✅ diperbaiki
- Catatan muncul saat ada `--omzet-final`; SKILL.md Input & Rumus menjelaskan beda jalur; daftar profesi sesuai.
- Cek kewajaran baru: omzet 800 jt, PPh final 4 jt → "0,5% × (800 jt − 500 jt) = Rp1.500.000, sedangkan yang Anda isi Rp4.000.000 …" ✔.
- Dasar hukum (web): PP 20/2026 mempertahankan omzet s.d. Rp500 jt OP tidak kena & batas Rp4,8 M (pajak.go.id/en/node/119950). Pengecualian pekerjaan bebas di **Ps. 56 ayat (3)–(4)** PP 55/2022 s.t.d.d. PP 20/2026 dan Ps. 57 ayat (2) (perseroan perorangan) — sumber sekunder (taxcenterpknstan.com/pp-20-2026, opini.kemenkeu.go.id); naskah PP belum dibuka langsung. Skill menyebut "Pasal 56" → konsisten.

### 5. Hitung ulang independen (3 kasus baru, kalkulator Python terpisah)
| # | Input | Script | Independen |
|---|---|---|---|
| A | K/I/3, 2 A1: 180 jt (PPh 21 8 jt) + 95 jt (2 jt) | PTKP 126 jt; PKP 149.000.000; PPh 16.350.000; **KB 6.350.000** | sama ✔ |
| B | TK/1, A1 200 jt (20 jt) + NPPN 180.834.998 × 60% (=108.500.999) + PPh 23 1 jt → PKP **tepat Rp250 jt** (dari 250.000.999, bulat ke bawah) | PPh 31.500.000 (3 jt + 28,5 jt); **KB 10.500.000**; PPh 25 2026 Rp875.000 | sama ✔ |
| C | K/2, A1 bruto 240 jt, 12 bln, iuran 4,8 jt (biaya jabatan dibatasi 6 jt), zakat 6 jt, omzet final 800 jt/PPh final 1,5 jt | neto 223.200.000; PKP 155.700.000; PPh 17.355.000; **KB 5.355.000**; omzet final tidak masuk Ps. 17 | sama ✔ |

Regresi: kasus 06 (K/2, KB 375.000), 07 (KB 3.075.000), K/I/3 neto 300 jt (PPh 20.100.000), pembulatan PKP 60.000.999 → 60.000.000 — tidak berubah ✔. JSON kasus 06 kini membawa 2 peringatan (A1 tunggal + batas lewat) sesuai.

### 6. Temuan baru
**Tinggi/Sedang:** tidak ada.

**Rendah**
- **R1.** Peringatan A1 tunggal dimatikan bila ada `--zakat` atau `--pph21-lain/22/23/25`. Untuk 1 A1 + zakat mandiri saja, hasil KB justru makin janggal (zakat seharusnya mendorong ke LB), jadi saran cek HRD tetap relevan. Usul: izinkan cek bila hanya zakat yang ditambahkan (untuk KB). Tidak memengaruhi angka.
- **R2.** Pada `--hari-ini` sebelum 31 Maret tidak ada penanda "belum lewat / sisa N hari" — cukup, hanya kosmetik.

### 7. Skor: **9/10** — LULUS
Alasan: seluruh 6 temuan 1.0.0 diperbaiki dan terverifikasi dengan input baru; teks KEP-55 kini persis sesuai sumber DJP; 3 kasus baru (termasuk K/I/3 dan PKP tepat Rp250 jt) cocok dengan hitungan independen; tidak ada regresi; 43 tes lulus. Belum 10 karena R1 dan beberapa dasar hukum baru diverifikasi lewat sumber sekunder.

### 8. PERLU REVIEW
- Naskah PP 20/2026 Ps. 56 ayat (3)–(4) (pengecualian pekerjaan bebas) — baru dicek lewat sumber sekunder.
- Naskah KEP-55/PJ/2026 sendiri (dicek via siaran/artikel DJP, bukan PDF KEP).
- Aturan tenggat bila 31 Maret jatuh pada hari libur (PMK 81/2024 Ps. 173?) — masih ditandai di skill.
- Nomor pasal NPPN (Ps. 463 PMK 81/2024 s.t.d.t.d. PMK 1/2026 vs Ps. 450), PTKP istri digabung & zakat (PP 60/2010) — belum dibuka naskahnya (bawaan 1.0.0).
- Domain pajak: review konsultan pajak terdaftar sebelum rilis; pembulatan belum dicocokkan dengan Coretax.
- `platform_teruji`: tetap hanya `claude-code (simulasi agent)`.
