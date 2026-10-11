# Uji OpenClaw sebelum/sesudah — persiapan-jual-atau-wariskan-usaha **v1.0.1** (fokus perbaikan)

- **Tanggal:** 2026-10-10 (UTC ~22:15)
- **Penguji:** Akun C (independen, bukan pembuat v1.0.1)
- **Cara uji:** OpenClaw 2026.9.8, model router `claude-sonnet-5`, `SCRATCHPAD=$HOME/komunitech-uji`, `mk-home.sh` + `run-uji.sh` (tanpa `unshare`, VM Cursor)
- **Tes script:** `python3 tests/uji_regresi.py` → 15 tes OK
- **Verifikasi angka:** Python/Decimal — warung bakso S1 dan buyout CV S3 cocok output script v1.0.1

Fokus run ini: cacat **T1** (`--biaya-sekali` per tahun) dan **S4** (jalur sekutu + `--porsi`), sesuai tugas C5 papan.

---

## Skenario A — warung bakso Pak Darto (renovasi 2024 Rp12 jt)

**Pesan:** (sama `examples/01-jual-warung-bakso.md`)

### SEBELUM — skor **6,5/10**

Normalisasi manual benar (78/103/85 jt), tapi basis pakai rata-rata ~89 jt (bukan basis hati-hati Rp85 jt); rentang setelah diskon 20% ≈ Rp142–214 jt tanpa baris utang/hasil bersih terstruktur; tidak ada daftar periksa 8 bagian.

### SESUDAH — skor **9/10**

Agent memanggil `nilai_usaha.py` dengan `--biaya-sekali 2024=12000000`. **Batas atas nilai usaha Rp204.000.000** (bukan Rp232.000.000 v1.0.0). Hasil bersih ke pemilik Rp112.560.000–177.840.000 setelah utang Rp18 jt + biaya 4%; peringatan laba 2025 turun; struktur 8 bagian lengkap. Skill/script terpakai: ya (`read`, `exec`).

<details><summary>Cuplikan SESUDAH (angka kunci)</summary>

- Laba disesuaikan: 78 / 103 (+12 renovasi 2024) / 85 jt → basis **Rp85.000.000**
- Nilai 100%: **Rp136.000.000 s/d Rp204.000.000**
- Hasil bersih ke Bapak: **Rp112.560.000 s/d Rp177.840.000** vs kebutuhan Rp108 jt

</details>

---

## Skenario B — beli bagian sekutu CV 40% (Rudi/Yanto)

**Pesan:** (sama `examples/03-buyout-mitra-cv.md`)

### SEBELUM — skor **5,5/10**

Saran generik kelipatan laba; tidak ada porsi 40%, utang badan usaha, atau akta perubahan CV.

### SESUDAH — skor **9/10**

Langkah 5a skill + script `--porsi 40 --utang-ikut` (implisit): nilai 100% Rp534–667,5 jt; **harga bagian 40% Rp189.600.000–243.000.000**; setelah biaya 3% **Rp183.912.000–235.710.000** ke Yanto. Utang leasing dijelaskan tetap di CV. Skill/script terpakai: ya.

<details><summary>Cuplikan SESUDAH (angka kunci)</summary>

- Porsi Yanto 40%: **Rp189.600.000 s/d Rp243.000.000**
- Setelah biaya 3%: **Rp183.912.000 s/d Rp235.710.000**

</details>

---

## Ringkasan gate (2 skenario)

| Skenario | SEBELUM | SESUDAH | Selisih |
|---|---|---|---|
| A warung + biaya sekali | 6,5 | 9,0 | +2,5 |
| B buyout sekutu 40% | 5,5 | 9,0 | +3,5 |
| **Rata-rata** | **6,0** | **9,0** | **+3,0** |

Acuan LULUS (subset): sesudah ≥ 8 dan selisih ≥ 1,5 — **terpenuhi** untuk kedua skenario fokus v1.0.1.
