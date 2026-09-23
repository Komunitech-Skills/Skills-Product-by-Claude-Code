# 00 — Uji banding pesaing (S1)

## Pencarian (23 Sep 2026)
- Kata kunci GitHub code search: `"13-week cash flow" filename:SKILL.md` (130 hasil), `"cash flow forecast" filename:SKILL.md` (868 hasil), `"arus kas" filename:SKILL.md` (9 hasil).
- Sumber dicek: github.com/anthropics/knowledge-work-plugins, github.com/VoltAgent/awesome-openclaw-skills (kategori productivity, pdf-and-documents, shopping, marketing: tidak ada skill cash flow), manairalabs/bicara-skills (hanya `invoice-extract-id` dan `wa-reply-id`), alvinindra/bahasa-skills (skill bahasa saja), edorabma9304/Claude-Skill-by-Ozolab-Indonesia (`skills/finance`: laporan arus kas historis operasi/investasi/pendanaan, bukan proyeksi mingguan).
- Pesaing paling sebanding:
  1. **`cash-flow-forecaster`**, github.com/OneWave-AI/claude-skills (`cash-flow-forecaster/SKILL.md`), lisensi **MIT**. Proyeksi 13 minggu mingguan dengan tanda CRUNCH dan tuas tindakan beserta nominal. **Dipakai untuk simulasi S1.**
  2. `cash-flow-forecast`, github.com/mohitagw15856/pm-claude-skills, MIT. Kerangka 13 minggu dan contoh angka placeholder.
  3. `cash-flow-snapshot`, github.com/anthropics/knowledge-work-plugins (small-business), Apache-2.0. Jendela 30/60/90 hari dengan pita keyakinan, bergantung pada konektor ledger (QuickBooks/Xero/dll.), output XLSX.
- Dibaca lewat raw.githubusercontent.com. Tidak ada script pihak ketiga yang dijalankan dan tidak ada isi yang disalin.

## Output dengan instruksi pesaing (`cash-flow-forecaster`, disimulasikan)
Instruksinya: tetapkan baseline dan tanggal as-of, jadwalkan pos yang pasti, tandai minggu di bawah "minimum comfort" sebagai `CRUNCH` (tanya pengguna; default 1 siklus gaji), jadikan crunch pertama sebagai headline, lalu beri tuas "konkret dengan nominal". Tidak ada script, jadi agent menghitung sendiri (di sini dianggap teliti; angka sama dengan hitungan independen).

```
13-WEEK CASH FORECAST — as of 23 Sep 2026 (opening cash Rp 35.000.000, user-stated)
Minimum comfort: Rp 15.000.000 (default: one payroll cycle — please confirm)

HEADLINE: first CRUNCH week = week 6 (2–8 Nov), ending cash Rp 6.300.000

Wk | Begin        | In          | Out         | End          | Flag
1  | 35.000.000   | 15.000.000  | 24.500.000  | 25.500.000   |
2  | 25.500.000   | 15.000.000  | 16.500.000  | 24.000.000   |
3  | 24.000.000   | 15.000.000  | 12.700.000  | 26.300.000   |
4  | 26.300.000   | 15.000.000  | 12.000.000  | 29.300.000   |
5  | 29.300.000   | 15.000.000  | 24.500.000  | 19.800.000   |
6  | 19.800.000   | 15.000.000  | 28.500.000  |  6.300.000   | CRUNCH
7  |  6.300.000   | 15.000.000  | 12.700.000  |  8.600.000   | CRUNCH
8  |  8.600.000   | 39.000.000  | 12.000.000  | 35.600.000   |
9  | 35.600.000   | 15.000.000  | 24.500.000  | 26.100.000   |
10 | 26.100.000   | 15.000.000  | 16.500.000  | 24.600.000   |
11 | 24.600.000   | 15.000.000  |  9.500.000  | 30.100.000   |
12 | 30.100.000   | 15.000.000  | 30.200.000  | 14.900.000   | CRUNCH
13 | 14.900.000   | 15.000.000  |  9.500.000  | 20.400.000   |

ESTIMATE lines: weekly sales Rp 15.000.000 and utilities Rp 2.500.000 (user averages).
Levers:
- Chase PT Arunika Fiktif (Rp 24.000.000) to pay by week 6 → week 6 ends ~Rp 30.300.000.
- Slide the freezer (Rp 12.000.000) to week 10 → week 6 ends Rp 18.300.000.
- Ask food supplier for 2-week terms → +Rp 9.500.000 buffer in crunch weeks (payable still due).
- Owner draw pause / credit line: not enough info.
File: cash-flow-13wk.csv
```

## Output dengan skill kita
Lihat `01-katering-cek-aman-3-bulan.md`.

## Penilaian

| Kriteria | Pesaing (`cash-flow-forecaster`, MIT) | Skill kita (`arus-kas-13minggu`) |
|---|---|---|
| Kualitas analisis | Baik: mingguan, headline crunch, tuas bernominal | Baik: sama, ditambah 5 opsi berangka hasil hitung ulang, peringatan pos setelah minggu 13, dan masalah struktural |
| Kesesuaian konteks Indonesia | Rendah: bahasa Inggris, tanpa format Rupiah/Excel Indonesia, tanpa pola "tanggal gajian", THR, pinjol, KUR | Tinggi: bahasa awam, `Rp 1.250.000`, CSV `;` + BOM, `tgl:25` dan akhir bulan, rujukan KUR/pinjol ilegal, contoh kalimat negosiasi |
| Akurasi | Bergantung pada ketelitian agent menghitung manual (tidak ada script). Penempatan tanggal bulanan ke minggu rawan salah. | Deterministik lewat script dan terverifikasi independen. Ada kelemahan: tebakan "kritis" dan simulasi "gabungan" yang bisa menyesatkan (lihat HASIL-UJI). |
| Siap pakai | Butuh agent yang mahir. Output teknis. | Langsung dipakai pemilik UMKM, dengan file Excel |
| Keunggulan pesaing | Pola bayar historis ("pelanggan net-30 yang bayar hari ke-55 diproyeksikan hari ke-55"), pos ESTIMATE dijumlah terpisah, forecast vs aktual tiap minggu, larangan memasukkan pemasukan yang belum pasti | Sebagian ada (asumsi disebut, perbarui tiap minggu), tetapi tidak sekuat itu |

Pesaing lain: `cash-flow-snapshot` (Anthropic) kuat untuk bisnis yang memakai ledger online (pita keyakinan dari variasi keterlambatan bayar, XLSX 3 sheet). Namun skill itu bersifat 30/60/90 hari (bukan mingguan), butuh konektor, dan tidak berbahasa Indonesia. `cash-flow-forecast` (mohitagw15856) hanya berupa kerangka dan placeholder tanpa perhitungan.

**Hasil: skill kita unggul secara keseluruhan** untuk pembeli sasaran (UMKM Indonesia, awam). Selisihnya terutama pada konteks lokal, script deterministik, dan kesiapan pakai. Kualitas analitis inti pesaing MIT setara bila agentnya teliti.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Pemasukan belum pasti dipisah**: tandai baris `pasti`/`perkiraan` dan tampilkan saldo "hanya yang pasti" di samping saldo total. Contohnya, di S2 kenaikan kas sepenuhnya bergantung pada 1 piutang.
2. **Kebiasaan bayar pelanggan**: tanyakan "biasanya telat berapa hari?" dan tempatkan piutang pada minggu realistis, bukan tanggal jatuh tempo.
3. **Forecast vs aktual mingguan**: panduan "roll forward" (geser 1 minggu, isi angka aktual, laporkan selisih terbesar), bisa sebagai bagian "Perbarui tiap minggu".
4. **Rentang ketidakpastian** (dari Anthropic): skenario pesimis sederhana (penjualan −20%) otomatis di script, bukan hanya saran di SKILL.md.
