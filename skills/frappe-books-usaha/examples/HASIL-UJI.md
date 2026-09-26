# HASIL UJI — frappe-books-usaha v1.0.0 (penguji independen Akun B, 26 Sep 2026)

## Skor: **5/10 — REVISI, jangan rilis** (uji ulang oleh penguji independen setelah perbaikan)

**Alasan:** Semua laporan baca benar dan terbukti pada file `.books.db` **asli**. Tetapi jalur impor CSV, fitur jual kedua,
gagal di aplikasi asli: CSV transaksi ditolak Import Wizard, dan akun penjualan/utang otomatis salah pada bagan akun Indonesia
asli. Selain itu `--keluar` bisa menimpa file database. Uji A/B dan banding pesaing dimenangkan skill untuk laporan
(`00-*`), tetapi temuan tinggi mengunci skor di bawah 7.

## Cara uji (yang benar-benar dilakukan)
- **Aplikasi asli:** unduh `Frappe-Books-v0.36.0-linux-x86_64.AppImage` dari GitHub releases frappe/books. SHA-512 cocok dengan
  `latest-linux.yml` rilis v0.36.0 (`nFHZaPXph+L6...fqBXmg==`). Dijalankan headless (Xvfb, jaringan keluar diblokir lewat proxy
  palsu, `TZ=Asia/Jakarta`). Lewat Chrome DevTools Protocol lokal dibuat 1 demo bawaan (Flo's Clothes, INR) + 4 perusahaan
  Indonesia (IDR, bagan akun "Indonesia - Chart of Accounts") dengan transaksi fiktif lewat mesin aplikasi itu sendiri
  (invoice, pembayaran sebagian, batal, retur, draf, stok, jurnal, pajak). Kode sumber tag v0.36.0 (commit `2f028f42`, cocok dengan
  `references/sumber-resmi.md`) dikloning untuk membaca skema & Import Wizard. Semua di scratchpad penguji; tidak ada yang masuk repo.
- **Skema:** tabel/kolom di `SKEMA_WAJIB` semuanya ada di file asli (Indonesia & demo India). Fixture pembuat (17 tabel) cocok untuk
  kolom yang dipakai, kecuali `Party`: file asli punya `gstin/gstType`, **tanpa `taxId`**.
- **Tes bawaan:** `python3 tests/uji_regresi.py` → 29 tes OK. `python3 scripts/validate.py --skill frappe-books-usaha` → valid.
- **Tidak dijalankan:** `uji_openclaw.sh` (sesuai instruksi). Uji platform agen sungguhan belum; skenario 06/07 bagian respons agen = simulasi penguji.

## Ringkasan skenario
| # | File | Hasil |
|---|---|---|
| A/B | `00-pembanding-tanpa-skill.md` | Skill Rp 564.000 benar; pendekatan SQL umum Rp 518.000–608.000 salah |
| Pesaing | `00-banding-pesaing.md` | Tidak ada pesaing khusus Frappe Books desktop; SQL generik kalah |
| 1 | `03-toko-kopi-uji-akun-b.md` | Laporan cocok; batas hari WIB/WITA/WIT benar; `cek` salah baca Inventory; retur vs laba-rugi |
| 2 | `04-sembako-piutang-uji-akun-b.md` | Umur piutang/utang (tempo 14 & 30) cocok 100% |
| 3 | `05-servis-ac-ppn-impor-uji-akun-b.md` | PPN floor sekali benar; **impor transaksi ditolak**; **akun salah** |
| 4 | `06-input-tidak-lengkap-uji-akun-b.md` | Lulus (tanya sekali); lokasi `~/Frappe Books` tidak terdeteksi |
| 5 | `07-luar-cakupan-uji-akun-b.md` | Menolak ubah DB & e-Faktur; **`--keluar` bisa menimpa .books.db** |

## Verifikasi angka independen (Decimal, kode penguji sendiri, dari data mentah file asli)
Penjualan/pembelian per bulan, sisa bayar, umur piutang/utang, laba rugi dari buku besar (`reverted=0`), stok, PPN 12% × DPP 11/12
dibulatkan ke bawah sekali, mode harga termasuk PPN (DPP terbesar dengan DPP + PPN ≤ harga): **semua cocok** dengan keluaran skill.
Konversi UTC → WIB/WITA/WIT diuji di 4 titik batas (23:45, 23:50, 00:10, 00:30) — benar.

## Data rusak
| Kasus | Hasil |
|---|---|
| DB tidak ada / 0 byte / teks / acak / terpotong / SQLite lain | kode 3, pesan awam jelas |
| DB dikunci EXCLUSIVE proses lain | kode 3 "sedang dikunci", timeout 5 detik |
| DB sedang dibuka aplikasi Frappe Books | terbaca normal, file tidak berubah |
| CSV cp1252 (`é`, `¼`), pemisah `;` | terbaca benar |
| Angka: `Rp 85.000,-`, `85.000,50`, `1,5jt`, `1.5jt`, `1,5 jt`, `85.000.000`, `1.250.000,00` | benar |
| `85,000`, `dua ratus`, `€ 5`, `-5000` | ditolak dengan alasan per baris (kode 5) |
| Koma tak berkutip di CSV koma | ditolak + saran pakai `;` |
| Tanggal `31/02/2026`, `09/27/2026`, nota beda tanggal, qty negatif, pelanggan/barang belum ada | ditolak per baris |
| CSV berisi byte `0x81` (tidak valid di cp1252 maupun UTF-8) | **galat tak terduga (UnboundLocalError)**, kode 1 — aman tapi tidak ramah |
| `--keluar` = file `.books.db` | **database tertimpa CSV** |

## Temuan
### TINGGI
1. **CSV transaksi ditolak Import Wizard asli** — "Required fields not selected: Number Series". Tambahkan kolom
   `SalesInvoice.numberSeries`/`PurchaseInvoice.numberSeries` (nilai `SINV-`/`PINV-`); sudah dicoba penguji → 2 draf masuk,
   total cocok dengan pratinjau skill. Koreksi juga `references/import-wizard.md`.
2. **Akun otomatis salah di bagan akun Indonesia asli.** Nama akun asli bernomor (`Penjualan - 4110.000`, `Pendapatan Service - 4310.000`,
   `Hutang Dagang Dalam Negeri - 2111.001`, sumber: `src/setup/createCOA.ts#getAccountName`). `csv-barang` memilih
   **`Pendapatan Bunga Bank - 4410.000`** untuk barang & jasa; `csv-transaksi --jenis pembelian` akan memilih `HUtang Dagang Biaya Kirim
   Luar Negeri - 2111.004`. Cocokkan dengan awalan nama/`accountNumber`, atau wajibkan konfirmasi akun sebelum LOLOS. Perbarui fixture
   agar memakai nama akun asli.
3. **`--keluar` dapat menimpa file `.books.db`** (terbukti pada salinan). Bertentangan dengan janji keamanan SKILL.md. Tolak path yang
   sama dengan `--db`, berakhiran `.db`, atau file SQLite yang sudah ada.

### SEDANG
4. `cek`/`info_usaha` membaca centang SingleValue sebagai `'1'`/`'true'`, padahal file asli menyimpan `'1.0'`/`'0.0'` → Inventory aktif
   dilaporkan "tidak aktif", dan `csv-barang` memberi peringatan palsu.
5. Retur: Frappe Books v0.36.0 memposting retur penjualan dengan tanda yang membuat akun Penjualan di buku besar **naik** (Rp 608.000 vs
   Rp 564.000 di `penjualan`). `laba-rugi` mengikuti buku besar (sama dengan P&L Frappe) tanpa penjelasan. Tambahkan catatan otomatis bila
   ada retur di periode, dan uji dengan data asli.
6. NPWP (`Party.taxId`) diabaikan diam-diam oleh Import Wizard pada perusahaan uji (skema punya `gstin`, bukan `taxId`). Cek kolom yang
   ada di tabel `Party` dan beri peringatan bila NPWP tidak bisa diimpor.

### RENDAH
7. CSV dengan byte tak valid cp1252 → `UnboundLocalError` (galat umum, kode 1). Tangani dengan pesan "simpan ulang sebagai CSV UTF-8".
8. Lokasi bawaan tidak lengkap: `~/Frappe Books` (Linux tanpa XDG Documents, terbukti di aplikasi asli) dan Documents di OneDrive (Windows) tidak dicari.
9. Dokumen menyebut satuan `Jam/Hari` dan lokasi `Toko`; file asli (UI bahasa Inggris) berisi `Hour/Day` dan `Stores`.
10. `--samarkan` pada nama berkurung → "W. B. S. (.".
11. "Sudah dibayar" = total bersih − sisa; saat ada retur belum dikembalikan, angka ini ≠ uang yang diterima. Pertimbangkan label "lunas/terbayar (bersih)".
12. Klaim di SKILL.md/README "belum diuji dengan file buatan aplikasi sungguhan" kini bisa diperbarui (laporan baca sudah terbukti), tetapi
    klaim Import Wizard harus tetap "belum lolos" sampai temuan 1–2 diperbaiki.

## Keamanan (audit)
Read-only `mode=ro` + `query_only` terbukti (SHA-256 file sama di semua perintah baca, termasuk saat aplikasi terbuka). Tidak ada akses jaringan,
kredensial, subprocess, eval/exec, SQL tulis. Satu-satunya jalur merusak adalah temuan 3.

## Rekomendasi
Perbaiki temuan 1–4 (+6, 7), perbarui fixture dari file asli (nama akun bernomor, centang `'1.0'`, retur bertanda terbalik, `Party` tanpa
`taxId`), tambah tes regresi untuk tiap temuan, lalu uji ulang impor penuh (Party → Item → Sales/Purchase Invoice) di Import Wizard asli.
`platform_teruji` tetap hanya uji simulasi agent; belum ada uji di OpenClaw/Codex/Claude Code/Cursor sungguhan.
