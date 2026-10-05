# numpy/numpy-financial — audit & ATM untuk `kelayakan-investasi-usaha` (2026-10-05)

| Kolom | Isi |
|---|---|
| Nama | numpy-financial |
| URL | https://github.com/numpy/numpy-financial |
| Pembuat | NumPy Developers (organisasi NumPy) |
| Bukti pemakaian | 411★ / 103 fork; pengganti resmi fungsi finansial NumPy (NEP-32); dirawat (commit 4–5 Okt 2026) — lihat `kurasi-bsd-cc-2026-10-05.md` #1 |
| Commit dibaca | `90e1ed1b090363de1c2ad7a42771b18b738f20bb` (HEAD `main`, via `git ls-remote`, 2026-10-05) |
| Lisensi | **BSD-3-Clause** — `LICENSE.txt` dibaca langsung dari raw.githubusercontent.com; "Copyright (c) 2005-2019, NumPy Developers." |
| Keputusan | **Diterima (kurasi/ATM)** → `skills/kelayakan-investasi-usaha` v1.0.0, status `uji` |

## Cara ambil
Teks diunduh sebagai teks biasa (`curl` ke raw.githubusercontent.com, disimpan sementara di memori/`/dev/shm`, lalu dihapus). Tidak di-clone, tidak di-install, **tidak ada kode sumber yang dijalankan**.

File dibaca: `LICENSE.txt`, `numpy_financial/_financial.py` (1.415 baris; fokus `npv`, `irr`, `_irr_default_selection`, `pmt`), `numpy_financial/_cfinancial.pyx` (loop `npv`, `nper`), `numpy_financial/tests/test_financial.py` (885 baris; `TestNpv`, `TestPmt`, `TestIrr`).

## Audit keamanan (Tahap 3)
- Impor `_financial.py`: `collections.abc`, `decimal`, `typing`, `numpy`, `numpy.typing`, `numpy._typing`, `numpy_financial._cfinancial`. `_cfinancial.pyx`: `libc.math`, `cython`. Tes: `math`, `warnings`, `decimal`, `numpy`, `pytest`, `hypothesis`.
- Tidak ada jaringan, akses berkas, subprocess, `eval`/`exec`, pembacaan kredensial, `curl | sh`, atau kode ter-obfuscate. Tidak ada prompt injection (bukan skill agent).
- Hasil: **lolos**. Skill Komunitech tidak memakai satu baris kode pun dari sumber; hanya definisi/konvensi dan nilai kasus uji.

## Yang diambil (turunan BSD-3, diatribusikan di `ATTRIBUTION.md` + `LICENSE-BSD`)
1. Konvensi arus kas: indeks 0 = investasi (negatif), NPV dijumlah dari t = 0.
2. Definisi IRR (NPV = 0), "tidak ada solusi" bila semua arus kas bertanda sama, aturan pilih akar bila banyak (akar ≥ 0 terkecil; semua negatif → paling dekat nol).
3. Persamaan PMT (akhir periode, kasus bunga 0).
4. Nilai harapan kasus uji: npv 5% → 122,89; npv 8% → 3065,22267; pmt(8%/12, 60, 15000) → −304,145914; pmt(7,5%/12, 180, 200000) → −1854,02472; irr untuk 8 deret (0,0524 · −0,0955 · 0,28095 · −0,0833 · 0,06206 · 0,0886 · trailing zeros · gh-44 1,00426); gh-39 → 0,12; IRR(1,2,3) tidak ada.

## Yang TIDAK diambil
Kode numpy/Cython, `np.roots` (diganti pemindaian + bisection), MIRR/NPER/RATE/IPMT/PPMT/FV/PV, broadcast array, uji fuzz `hypothesis`, kasus gh-15 (IRR ≈ −99,99999%, di luar rentang bisnis −99%…1000%).

## Catatan pembeda vs sumber (nilai tambah)
Sumber = pustaka fungsi untuk programmer (butuh numpy). Skill = alur keputusan UMKM: omzet/biaya variabel/tetap per bulan, nilai sisa garis lurus, pajak sebagai persen (PPh final/PPh badan), payback biasa & terdiskonto, PI, BEP akuntansi & ekonomi, sensitivitas & batas aman, kesimpulan layak/kurang layak/tidak layak, mode uang bersih minimal, pembacaan angka Indonesia, contoh lokal, disclaimer.

## Pesaing yang perlu dicek penguji (Tahap 6.5)
Belum dicari oleh pembuat. Kata kunci usulan: "investment feasibility skill", "capital budgeting NPV IRR SKILL.md", "payback period calculator agent skill", ClawHub "npv", skills.sh "financial analysis".
