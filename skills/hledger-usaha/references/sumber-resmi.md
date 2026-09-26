# Sumber resmi yang dipakai (diakses 26 September 2026)

- Situs resmi: https://hledger.org (instalasi: https://hledger.org/install.html; format jurnal: https://hledger.org/journal.html; aturan CSV: https://hledger.org/csv.html; hledger-web: https://hledger.org/hledger-web.html)
- Kode & rilis resmi: https://github.com/hledgerorg/hledger/releases (alamat lama `github.com/simonmichael/hledger` dialihkan ke sini)
- Versi yang diuji: **1.52.4** (rilis stabil terbaru saat diuji; berkas `hledger-linux-x64.tar.gz`, SHA-256 `f76a2e4088e162b7658e43077502569d5a6fdacd219b19bfb9aab6588b69643a`, cocok dengan digest di halaman rilis).
- Lisensi hledger: GPL-3.0-or-later. Tidak disertakan dalam paket skill.

Perilaku hledger 1.52.4 yang diandalkan skill (diuji langsung):
- `commodity Rp 1.000,` wajib memakai tanda desimal (tanpa koma → galat "Please include a decimal point or decimal comma").
- `account X  ; type: C` memberi golongan; sub-akun mewarisi golongan induk (terlihat di `ptags` JSON).
- `hledger print -O json`: jumlah di `aquantity.decimalMantissa` + `decimalPlaces` (dipakai skill, bukan `floatingPoint`).
- Aturan CSV: pola `if` tidak peka huruf besar/kecil secara bawaan; `(?i)` **ditolak**; `&` = DAN; blok yang lebih bawah menimpa `account2`; `include` di file rules didukung.
- `hledger-web` bawaan mendengarkan `127.0.0.1:5000`; `--allow=view` = hanya lihat.
- `-n`/`--no-conf` mengabaikan file konfigurasi pengguna (dipakai skill agar keluaran konsisten).
