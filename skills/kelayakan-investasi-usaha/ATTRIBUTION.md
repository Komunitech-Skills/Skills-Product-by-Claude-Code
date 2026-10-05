# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Definisi dan konvensi fungsi keuangan (NPV, IRR, PMT) serta sebagian kasus uji diturunkan dari **numpy-financial**. Kode tidak disalin: semua rumus ditulis ulang dalam Python standar (`decimal` + `float`), tanpa numpy, dengan cara pencarian IRR yang berbeda (pemindaian + bisection, bukan akar polinomial). Sisanya karya orisinal Komunitech.

## Sumber
- **Repo:** [numpy/numpy-financial](https://github.com/numpy/numpy-financial) — pembuat: NumPy Developers (organisasi NumPy).
- **Lisensi:** BSD-3-Clause, "Copyright (c) 2005-2019, NumPy Developers." Teks lengkap disalin tanpa perubahan di `LICENSE-BSD` (diambil dari `LICENSE.txt` repo sumber).
- **Commit yang dibaca:** `90e1ed1b090363de1c2ad7a42771b18b738f20bb` (HEAD cabang `main`, 2026-10-05).
- **File yang dibaca:** `LICENSE.txt`, `numpy_financial/_financial.py` (docstring & definisi `npv`, `irr`, `pmt`), `numpy_financial/_cfinancial.pyx` (loop `npv`), `numpy_financial/tests/test_financial.py` (kelas `TestNpv`, `TestPmt`, `TestIrr`).

## Bagian yang diturunkan (tunduk pada BSD-3-Clause, lihat `LICENSE-BSD`)
1. Konvensi arus kas: periode 0 = investasi awal bertanda negatif; NPV dijumlahkan mulai t = 0 (`scripts/kelayakan.py` fungsi `npv`).
2. Definisi IRR = tingkat yang membuat NPV = 0, "tidak ada IRR" bila semua arus kas bertanda sama, dan pemilihan akar bila ada lebih dari satu (akar ≥ 0 terkecil; bila semua negatif, yang paling dekat nol) — fungsi `irr`, `irr_semua`.
3. Persamaan PMT akhir periode termasuk kasus bunga 0 — fungsi `pmt` (dipakai untuk "biaya modal tahunan setara" dan uang bersih minimal).
4. Kasus uji di `tests/uji_kelayakan.py` bagian **A** (nilai harapan NPV/IRR/PMT dari dokumentasi & tes numpy-financial, termasuk kasus isu gh-39 dan gh-44), ditulis ulang tanpa numpy/pytest.

Pemberitahuan wajib BSD-3: nama NumPy Developers dan kontributornya **tidak** dipakai untuk mendukung atau mempromosikan skill ini.

## Audit lisensi & keamanan (Tahap 2–3)
- `LICENSE.txt` dibaca langsung (BSD-3-Clause standar, tiga klausul). Mengizinkan modifikasi dan penjualan turunan dengan menyertakan pemberitahuan hak cipta, syarat, dan penafian.
- File sumber **dibaca, tidak dijalankan**, tidak di-clone, tidak di-install (diambil sebagai teks dari `raw.githubusercontent.com`). `_financial.py` hanya mengimpor `numpy`, `decimal`, `typing`, `collections.abc`, dan modul Cython internal `_cfinancial`; `_cfinancial.pyx` hanya `libc.math` & `cython`. Tidak ada akses jaringan, berkas, subprocess, `eval`/`exec`, kredensial, atau kode ter-obfuscate. Tes memakai `pytest`/`hypothesis` (tidak dipakai).
- Kesimpulan: **lolos audit**. Script skill ini tidak membutuhkan paket apa pun di luar Python standar.

## Nilai tambah Komunitech (orisinal)
- Model kelayakan untuk UMKM Indonesia: omzet/biaya variabel/biaya tetap per bulan atau tahun, investasi penghematan, nilai sisa garis lurus, pajak sebagai persen (PPh final 0,5% dari omzet atau PPh badan dari laba), pertumbuhan omzet/biaya.
- Payback biasa & terdiskonto, PI, BEP akuntansi & ekonomi, sensitivitas, batas aman, dan kesimpulan **layak / kurang layak / tidak layak** dengan alasan & syarat.
- Mode `--cari-minimal` untuk input tidak lengkap; pembacaan angka Indonesia (`45jt`, `1,5jt`, `Rp45.000.000`, `6jt/bulan`); pesan galat yang jelas.
- `SKILL.md`, `README.md`, `references/`, `examples/`, dan tes B–H.

Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian, ditambah ketentuan BSD-3-Clause untuk bagian yang disebut di atas.
