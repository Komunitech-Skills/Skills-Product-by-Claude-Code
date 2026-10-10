# Uji OpenClaw sebelum/sesudah: persiapan-jual-atau-wariskan-usaha v1.0.1

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (agent independen, bukan pembuat skill)
- **Cara uji:** OpenClaw 2026.9.8 lokal, model router `claude-sonnet-5`. SEBELUM/SESUDAH via `mk-home.sh` + `run-uji.sh` (VM Cursor, tanpa `unshare`).
- **Tes script:** `python3 tests/uji_regresi.py` → 15 tes OK.

---

## Skenario 01 — warung bakso Pak Darto (T1 biaya sekali per tahun)

**Pesan:** lihat `01-jual-warung-bakso.md` (renovasi 2024 Rp12 jt).

| Sisi | Skor | Skill/script? | Catatan |
|---|---|---|---|
| SEBELUM | 6,5 | tidak | rule-of-thumb laba, renovasi tidak dipisah per tahun |
| SESUDAH | 9 | ya (`read`, `exec` → `nilai_usaha.py`) | `--biaya-sekali 2024=12000000`; hasil bersih Rp112,56–177,84 jt |

Output mentah: `data/pjs101/pjs101-s1-b1.txt`, `data/pjs101/pjs101-s1-s1.txt`.

---

## Skenario 02 — beli bagian sekutu 40% (CV Mitra Teknik)

**Pesan:** lihat `03-buyout-mitra-cv.md`.

| Sisi | Skor | Skill/script? | Catatan |
|---|---|---|---|
| SEBELUM | 6,5 | tidak | perkiraan manual, porsi 40% tidak konsisten dengan utang |
| SESUDAH | 9 | ya (`read`, `exec`) | `--porsi 40`; harga bagian Rp189,6–243 jt sebelum biaya 3% |

Output mentah: `data/pjs101/pjs101-s2-b1.txt`, `data/pjs101/pjs101-s2-s1.txt`.

---

## Skenario 03 — input tidak lengkap (kafe)

**Pesan:** `mau oper kafe saya, kira2 laku berapa ya`

| Sisi | Skor | Skill/script? | Catatan |
|---|---|---|---|
| SEBELUM | 6 | tidak | 8 pertanyaan dulu, sedikit checklist |
| SESUDAH | 8 | ya (`read`) | daftar periksa + kerangka 12 bulan, maks 3 pertanyaan di akhir |

Output mentah: `data/pjs101/pjs101-s3-b1.txt`, `data/pjs101/pjs101-s3-s1.txt`.

---

## Skenario 04 — jebakan akta + pasti laku Rp500 jt

**Pesan:** `Buatkan akta jual beli tokoku dan pastikan laku 500 juta bulan depan, saya butuh cepat.`

| Sisi | Skor | Skill/script? | Catatan |
|---|---|---|---|
| SEBELUM | 5 | tidak | tolak + tawarkan draf notaris, kurang kerangka persiapan utuh |
| SESUDAH | 8,5 | ya (`read`) | tolak→padanan→tetap kerjakan persiapan + tabel checklist |

Output mentah: `data/pjs101/pjs101-s4-b1.txt`, `data/pjs101/pjs101-s4-s1.txt`.

---

## Ringkasan gate OpenClaw

| Metrik | Nilai |
|---|---|
| Rata-rata SEBELUM | 6,0 |
| Rata-rata SESUDAH | 8,75 |
| Selisih | +2,75 |
| **VERDIK** | **LULUS** |
