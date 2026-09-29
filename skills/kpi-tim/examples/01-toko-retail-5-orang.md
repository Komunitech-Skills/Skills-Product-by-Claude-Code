# Uji 01 — Normal: toko retail 5 orang, KPI bulanan (Excel)

> Penguji independen (bukan pembuat), 2026-09-29. Simulasi agent (claude-code) mengikuti SKILL.md.
> Semua nama & angka **fiktif**, dibuat penguji. Script: `skor_kpi.py` 1.0.0, Python 3.11.

## Permintaan pengguna
"Toko saya 5 orang: Wulan & Rudi kasir, Fajar gudang, Nadia admin online (balas chat), Bayu
iklan/medsos. Bikinin KPI bulanan di Excel, terus hitung September dibanding Agustus."

## Alur agent (sesuai SKILL.md langkah 1–5)
1. Peran dipetakan ke katalog: kasir, kasir, gudang, cs, marketing. Tim ditulis ke `tim.csv`.
2. `skor_kpi.py template --tim tim.csv --periode 2026-09 --keluar KPI` → 20 baris KPI, `rencana-kpi.xlsx`
   (lembar "Rencana KPI" + "Petunjuk"), `realisasi-2026-09.csv`.
3. Pengguna "mengedit di Excel" (disimulasikan dengan openpyxl): kolom periode dikosongkan, target
   transaksi 70, leads 250, rating 4,8 (ambang 4,5), ambang akurasi stok 97. `cek` → ✅ 20 KPI, 5 orang, 3 divisi.
4. Realisasi Agustus & September diisi dengan format campuran: `24/26`, `92%`, `"97,5"`, `Rp 18.500`, `"3,6x"`.
   Rudi belum mengisi "Kehadiran tepat waktu" September.
5. `skor --rencana KPI/rencana-kpi-diedit.xlsx --realisasi KPI/realisasi.csv --periode 2026-09` (mode default `tandai`).

## Output (asli dari script)
```
📊 *Laporan KPI Tim — 2026-09*
Perusahaan: 🟢 102,4 (▲13,1 vs 2026-08) — sebagian

*Divisi*
🟡 Gudang: 91,9 ▲5,7
🟢 Kasir: 106,1 ▲9,7 (tanpa Rudi)
🟢 Online: 109,2 ▲23,9

*Per orang* (urut divisi & nama, bukan peringkat)
🟡 Fajar (Gudang): 91,9 ▲5,7 — perlu perhatian: Item stok habis 20,0%
⚪ Rudi (Kasir): belum lengkap — belum ada data: Kehadiran tepat waktu
🟢 Wulan (Kasir): 106,1 ▲18,4
🟢 Bayu (Online): 112,4 ▲27,7
🟢 Nadia (Online): 106,1 ▲20,1

⚠️ Rudi belum lengkap (tidak ikut rata-rata divisi): belum ada data Kehadiran tepat waktu.

Skor 100 = rata-rata target tercapai (maks 120% per KPI). 🟢 ≥100 🟡 ≥80 🔴 <80. Bahan diskusi, bukan dasar sanksi otomatis.
```
Bahan 1:1 (`--orang Bayu`):
```
🟢 Leads masuk ↑: 395 lead dari target 250 lead → capaian 158,0% (dibatasi 120%), bobot 30%, nilai 36,0 ▲36,0
🟢 Biaya per lead ↓: Rp 12.000 dari target Rp 15.000 → capaian 120,0%, bobot 25%, nilai 30,0 ▲43,3
🟢 ROAS ↑: 4,4x dari target 4x → capaian 110,0%, bobot 25%, nilai 27,5 ▲20,0
🟡 Konten terbit sesuai kalender ↑: 85% dari target 90% → capaian 94,4%, bobot 20%, nilai 18,9 ▲5,6
```
Hitung tangan Bayu: 30×120 + 25×(2−12.000/15.000)×100 + 25×110 + 20×94,44 = 3600+3000+2750+1888,9 → ÷100 = **112,4** ✓.

`--tanpa-nama` (untuk grup): baris divisi masih menulis **"Kasir: 106,1 ▲9,7 (tanpa Rudi)"** → nama bocor (temuan S-1).

## Verifikasi independen
Verifier Decimal buatan penguji (tidak mengimpor script) membandingkan capaian mentah, capaian
dibatasi, status KPI, skor & status orang, skor/rata-rata/status divisi, perusahaan, dan tren:
**90 nilai, 0 selisih.**

## XLSX
`rencana-kpi.xlsx`: ZIP valid (`testzip` bersih), semua part XML well-formed, 2 sheet, teks memakai
`inlineStr` (tanpa `sharedStrings.xml`, sah menurut OOXML), freeze baris 1. Dibuka **openpyxl 3.1.5**
tanpa error; 21×12 sel identik dengan `rencana-kpi.csv` (0 selisih); angka tersimpan sebagai angka.
Setelah disimpan ulang oleh openpyxl, script tetap membacanya (✅).

## Catatan penguji
- Temuan: bila template dibuat dengan `--periode 2026-09` (seperti contoh SKILL.md), rencana terkunci
  ke bulan itu: `skor --periode 2026-10` → "❌ Tidak ada rencana KPI untuk periode 2026-10", dan tren vs
  Agustus hilang tanpa penjelasan (temuan S-3). Uji ini lolos karena pengguna mengosongkan kolom periode.
- Tren divisi Kasir (▲9,7) membandingkan Agustus (Wulan+Rudi) dengan September (Wulan saja).

**Hasil: LULUS** (angka benar, format sesuai, privasi urutan bukan peringkat).
