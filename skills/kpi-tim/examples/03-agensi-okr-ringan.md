# Uji 03 — Normal: agensi kreatif, OKR ringan (tengah & akhir kuartal)

> Penguji independen, 2026-09-29. Simulasi agent (claude-code). Data fiktif buatan penguji.

## Permintaan pengguna
"Agensi desain saya di Bandung mau pakai OKR kuartal 4, tidak usah KPI ribet. Ini tabelnya, cek
progres sekarang (sudah setengah kuartal)."

## Data `okr.csv` (8 baris)
- Tim Kreatif: 3 KR, termasuk KR **menurun** (revisi/proyek 4 → 2, sekarang 3,2), skor kepuasan
  7,5 → 9 (8,1), dan KR berbentuk progres langsung `60%`.
- Tim Akun: klien retainer 6 → 10 (sekarang **11**, melampaui), nilai retainer Rp 45.000.000 → 70.000.000
  (52.500.000), proposal upsell 0 → 12 (3).
- Owner: 1 KR saja (memicu saran 2–4 KR).
- 1 baris periode 2026-Q3 (harus diabaikan).

## Output `okr --periode 2026-Q4 --jalan 0,5`
```
🎯 *OKR — 2026-Q4* (waktu berjalan 0,50)
🟡 Tim Kreatif — Klien puas dengan hasil pertama: 0,47
   🟡 Rata-rata revisi per proyek (turun): 0,40
   🟡 Skor kepuasan klien (1-10): 0,40
   🟢 Template brief baru dipakai semua proyek: 0,60
🟢 Tim Akun — Pendapatan berulang naik: 0,52
   🟢 Klien retainer aktif: 1,00
   🔴 Nilai retainer per bulan (Rp): 0,30
   🔴 Proposal upsell terkirim: 0,25
🔴 Owner — Agensi dikenal di Bandung: 0,33
   🔴 Artikel studi kasus terbit: 0,33
⚠️ OKR baris 5 (Klien retainer aktif): melampaui target (1,25), progres dibatasi 1,0.
⚠️ Objective 'Agensi dikenal di Bandung' punya 1 key result. Saran OKR ringan: 2-4 key result.
Progres 0-1,0. 🟢 ≥ waktu berjalan, 🟡 ≥ 70% dari itu, 🔴 di bawahnya.
```
Akhir periode (tanpa `--jalan`): status memakai 🟢 ≥0,7 🟡 ≥0,4 🔴 <0,4 → Tim Akun 0,52 menjadi 🟡;
catatan "OKR tidak untuk menilai gaji" tampil.

## Verifikasi independen
Hitung ulang Decimal: revisi (3,2−4)/(2−4)=0,40; kepuasan (8,1−7,5)/1,5=0,40; objective
(0,4+0,4+0,6)/3=0,4667→0,47; retainer min(1,25;1)=1; nilai (52,5−45)/25=0,30; upsell 0,25 →
0,5167→0,52; Owner 2/6=0,33. Status tengah kuartal (≥0,5 hijau, ≥0,35 kuning). **3 objective,
0 selisih.** Baris Q3 diabaikan ✓. Nomor baris di peringatan sesuai baris file ✓.

## Catatan penguji
- KR menurun dihitung benar tanpa kolom arah (rumus (sekarang−awal)/(target−awal)).
- Agent menjelaskan: OKR untuk arah & fokus, tidak masuk skor KPI/gaji (sesuai SKILL.md §6).

**Hasil: LULUS.**
