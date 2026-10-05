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

## Pajak yang disebut skill (v1.0.1, dicek 26 September 2026)
- **PPh Pasal 23 atas jasa:** 2% dari jumlah bruto (jasa teknik, manajemen, konsultan, dan jasa lain), tarif 100% lebih tinggi bila penerima tidak memiliki NPWP — halaman DJP "Pemotongan Pajak Penghasilan - Pasal 23": https://www.pajak.go.id/en/node/35004 (dasar UU 36/2008 Pasal 23; jenis jasa lain: PMK 141/PMK.03/2015, https://jdih.kemenkeu.go.id/dok/141-pmk-03-2015). Skill tidak menghitung kewajiban PPh 23; hanya mencatat potongan sesuai bukti potong. Pembulatan belum dicocokkan dengan Coretax.
- **Larangan pembukuan ganda:** UU KUP (UU 28/2007) Pasal 28 ayat (3) — pembukuan/pencatatan diselenggarakan dengan iktikad baik dan mencerminkan keadaan usaha yang sebenarnya; Pasal 39 ayat (1) huruf d (SPT/keterangan isinya tidak benar) dan huruf f (memperlihatkan pembukuan palsu/tidak menggambarkan keadaan sebenarnya). Naskah dibaca dari https://learning.hukumonline.com/wp-content/uploads/2021/07/UU-No.-28-Tahun-2007.pdf.
