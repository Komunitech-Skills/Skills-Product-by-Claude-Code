# Uji 02 — Normal: pabrik kecil 12 orang, 3 divisi, KPI "makin rendah makin baik", batas capaian

> Penguji independen, 2026-09-29. Simulasi agent (claude-code). Data fiktif buatan penguji.

## Permintaan pengguna
"Pabrik konveksi saya: 5 operator + 1 supervisor produksi, 3 orang QC & gudang, 3 kurir. Reject dan
keterlambatan makin kecil makin bagus. Output operator jangan lebih dari 110% dihitungnya. Pengiriman
dinilai per divisi juga. Hitung September, file dari Excel (pakai titik koma)."

## Data
- `rencana.csv` dengan pemisah `;` (gaya Excel Indonesia), angka `4.000`, `20.000`, `2.500`.
- 43 KPI: Output produksi (naik, `maks_capai` 110), Tingkat reject % (turun, ambang 3), Kecelakaan kerja
  (turun, **target 0**), Keterlambatan order (turun, ambang 4), Keterlambatan serah ke ekspedisi
  (turun, `maks_capai` 150), Salah kirim (turun, target 0), Keterlambatan rata-rata kurir (turun,
  `maks_capai` 100), + **KPI divisi** Pengiriman (tepat waktu 60%, Biaya BBM/paket Rp, turun, 40%).
- Data kosong September: Citra (Kecelakaan kerja, 15%), Joni (Akurasi stok, 40%), Mira (2 KPI, 80%).
- Kasus ekstrem: Bambang reject 5% (target 2 → mentah −50% → 0), 1 kecelakaan (→ 0%);
  Hartono keterlambatan 0 vs target 2 (→ 200% → dibatasi 120); Kurnia serah telat 12 jam vs 4 (→ −100% → 0).

`cek` → ✅ 43 KPI, 12 orang, 3 divisi + 8 catatan "nol kejadian" untuk target 0.

## Output mode default `tandai`
```
📊 *Laporan KPI Tim — 2026-09*
Perusahaan: 🟡 91,1 (▼0,9 vs 2026-08) — sebagian

*Divisi*
🟢 Pengiriman: 102,7 ▲8,8
🟡 Produksi: 93,6 ▲1,0 (tanpa Citra)
🔴 QC & Gudang: 77,1 ▼12,6 (tanpa Joni)

*Per orang* (urut divisi & nama, bukan peringkat)
🟢 Lukman (Pengiriman): 107,1 ▲2,6
⚪ Mira (Pengiriman): belum lengkap — belum ada data: Pengiriman tepat waktu, Paket gagal kirim
🟡 Nando (Pengiriman): 92,1 ▼8,4 — perlu perhatian: Paket gagal kirim 83,3%
🟢 Agus (Produksi): 109,9 ▲18,7
🔴 Bambang (Produksi): 55,2 ▼48,9 — perlu perhatian: Kecelakaan kerja 0,0%
⚪ Citra (Produksi): belum lengkap — belum ada data: Kecelakaan kerja
🟢 Dedi (Produksi): 107,1 ▲4,4
🟡 Eka (Produksi): 96,8 ▼3,4 — perlu perhatian: Tingkat reject 90,0%
🟡 Hartono (Produksi): 98,9 ▲19,0 — perlu perhatian: Reject lini 75,0%
🟢 Indah (QC & Gudang): 115,2 ▲22,9
⚪ Joni (QC & Gudang): belum lengkap — belum ada data: Akurasi stok
🔴 Kurnia (QC & Gudang): 39,0 ▼60,2 — perlu perhatian: Keterlambatan serah ke ekspedisi -100,0%
...
```

## Mode eksplisit
- `--data-kosong bobot-ulang`: Citra 81,8 "(dihitung dari 85% bobot)", Joni 75,0 "(dari 60% bobot)",
  Mira tetap ⚪ (20% < 50%). Perusahaan 90,2. **Catatan:** Mira tidak masuk daftar ⚠️ dan perusahaan
  tidak ditandai "sebagian" di mode ini (temuan R-2).
- `--data-kosong nol`: Mira 🔴 16,0; perusahaan 86,2; peringatan "KPI tanpa data dihitung 0%" muncul.
  "Perlu perhatian" Mira menunjuk KPI berdata (80%), bukan KPI kosong yang membuat skornya 16 (R-3).
- `--bobot-divisi "Produksi=50,QC & Gudang=25,Pengiriman=25"` dan `--cap 110` juga diuji.

## Verifikasi independen (verifier Decimal penguji)
| Run | Nilai dibandingkan | Selisih |
|---|---|---|
| tandai | 174 | 0 |
| bobot-ulang | 174 | 0 |
| nol | 174 | 0 |
| --bobot-divisi | 174 | 0 |
| --cap 110 + bobot-ulang | 174 | 0 |

Termasuk: rumus turun (2 − r/t), aturan nol kejadian, `maks_capai` per KPI (110/150/100), batas
bawah 0, ambang kuning/merah dua arah, KPI divisi menggantikan rata-rata individu, tren orang/divisi/perusahaan.

## Catatan penguji
- 1:1 Kurnia menulis "capaian -100,0%": benar sebagai angka mentah, tetapi membingungkan pemilik awam
  karena aturan menyebut batas bawah 0% (R-1).
- `--tanpa-nama --json` masih memuat `belum_lengkap: ["Mira"]`, dst. (S-1).

**Hasil: LULUS** (0 selisih; arah turun, batas, dan data kosong ditangani eksplisit).
