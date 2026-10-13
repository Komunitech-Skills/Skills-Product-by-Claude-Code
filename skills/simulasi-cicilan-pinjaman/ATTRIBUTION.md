# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Definisi fungsi keuangan PMT dan RATE serta dua nilai kasus uji diturunkan dari **numpy-financial**. Kode tidak disalin: semua rumus ditulis ulang dalam Python standar (`decimal`), tanpa numpy, dan RATE dicari dengan bisection (bukan metode Newton milik sumber). Sisanya karya orisinal Komunitech.

## Sumber
- **Repo:** [numpy/numpy-financial](https://github.com/numpy/numpy-financial) — pembuat: NumPy Developers (organisasi NumPy).
- **Lisensi:** BSD-3-Clause, "Copyright (c) 2005-2019, NumPy Developers." Teks lengkap disalin tanpa perubahan di `LICENSE-BSD`.
- **Commit acuan:** `90e1ed1b090363de1c2ad7a42771b18b738f20bb` (HEAD `main`, 2026-10-05; audit di catatan riset internal kurator (tidak disertakan dalam paket) repo Komunitech).

## Bagian yang diturunkan (tunduk pada BSD-3-Clause, lihat `LICENSE-BSD`)
1. Persamaan PMT akhir periode termasuk kasus bunga 0, dengan konvensi tanda numpy-financial (fungsi `pmt` di `scripts/cicilan.py`).
2. Definisi RATE = bunga per periode yang menyeimbangkan nilai pinjaman dan pembayaran (fungsi `rate`).
3. Nilai harapan kasus uji `pmt(8%/12, 60, 15000) = −304,145914` dan `pmt(7,5%/12, 180, 200000) = −1854,02472` di `tests/uji_regresi.py` bagian **A**, ditulis ulang tanpa numpy/pytest.

Pemberitahuan wajib BSD-3: nama NumPy Developers dan kontributornya **tidak** dipakai untuk mendukung atau mempromosikan skill ini.

## Audit lisensi & keamanan (Tahap 2–3)
Sumber yang sama dengan `kelayakan-investasi-usaha`: dibaca sebagai teks, tidak di-clone, tidak di-install, tidak dijalankan. Tidak ada akses jaringan, berkas, subprocess, `eval`/`exec`, kredensial, atau kode ter-obfuscate. **Lolos audit.** Script skill ini hanya memakai Python standar.

## Nilai tambah Komunitech (orisinal)
- Bunga flat vs efektif/anuitas dengan jadwal angsuran rupiah (pembulatan per baris, selisih di cicilan terakhir ditampilkan), harga + DP (rupiah/persen).
- Bunga efektif setara per tahun termasuk biaya di muka (tunai / dipotong saat cair / ditambahkan ke pinjaman) dan biaya bulanan; total harga lewat kredit vs tunai.
- KPR bunga bertahap (fixed lalu floating), hitung balik bunga dari cicilan, pinjaman harian (pinjol) dengan peringatan batas yang dicatat, ilustrasi denda, cicilan & pinjaman maksimal aman dari penghasilan.
- Pembacaan angka Indonesia (`25jt`, `1,5jt`, `750rb`, `3th`, `14hari`), pesan galat jelas, `SKILL.md`, `README.md`, `references/`, dan tes B–K.
- Semua data contoh fiktif.

Penggunaan tunduk pada `LISENSI.txt` dalam paket pembelian, ditambah ketentuan BSD-3-Clause untuk bagian yang disebut di atas.
