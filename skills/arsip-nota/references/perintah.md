# Referensi perintah arsip.py

Path relatif terhadap folder skill ini. Windows: ganti `python3` dengan `python`/`py`.
`--json` dan `--db` bisa dipakai di semua perintah (dari argumen bersama).

| Perintah | Fungsi | Opsi utama |
|---|---|---|
| `init` | Buat indeks arsip baru | `--folder-arsip PATH`, `--mulai-baru`, `--ya` |
| `info` | Ringkasan indeks (jumlah nota, total, folder arsip) | - |
| `tambah` | Arsipkan satu file nota ke indeks | `--file`, `--tanggal`, `--vendor`, `--nominal`, `--kategori`, `--jenis`, `--catatan`, `--folder-arsip`, `--pindah`, `--izinkan-duplikat`, `--ya` |
| `cari` | Cari nota | `--vendor`, `--kategori`, `--dari`/`--sampai`, `--nominal-min`/`--nominal-max`, `--cari` |
| `rekap` | Rekap per kategori/vendor | `--bulan`/`--tahun`/`--dari`+`--sampai`, `--kategori`, `--csv` |
| `duplikat` | Cari nota yang kemungkinan dobel | - |
| `ekspor` | Ekspor CSV siap impor `kas-umkm` | `--bulan`/`--tahun`/`--dari`+`--sampai`, `--csv` (wajib) |
| `backup` | Cadangkan/lihat cadangan indeks | `--daftar` |
| `restore` | Pulihkan indeks dari cadangan | `--dari FILE`, `--ya` |

## Kategori
`bahan-baku`, `operasional`, `peralatan`, `jasa`, `transportasi`, `listrik-air`, `sewa`, `pajak`, `lain-lain`.
Tidak diisi → ditebak dari nama vendor/catatan (kata kunci sederhana); tidak cocok → `lain-lain`, ditandai sebagai
asumsi. Ini bukan pos akuntansi resmi; saat `ekspor` ke `kas-umkm`, dipetakan ke kategori kas-umkm:
`bahan-baku`/`peralatan` → `beli-stok`, `sewa` → `sewa`, `listrik-air` → `listrik-air`, `pajak` → `pajak`,
sisanya (`operasional`, `jasa`, `transportasi`, `lain-lain`) → `lain-lain`.

## Jenis dokumen
`nota` (default), `struk`, `kuitansi`, `invoice`, `faktur`, `bukti-transfer`.

## Nama file & folder arsip
`<folder-arsip>/<tahun>/<bulan 2 digit>/<YYYY-MM-DD>_<vendor-aman>_<nominal>.<ekstensi asli>`
- Vendor "diamankan": spasi → `-`, karakter yang tidak diizinkan di nama file Windows (`< > : " / \ | ? *`) dan
  karakter kontrol dihapus, dipotong maks. 40 karakter, nama yang bentrok dengan nama perangkat Windows
  (`CON`, `PRN`, `AUX`, `NUL`, `COM1`-`COM9`, `LPT1`-`LPT9`) diberi awalan `_`.
- Nominal ditulis tanpa titik ribuan, dibulatkan ke rupiah terdekat.
- Nama file yang sudah ada di tujuan (kebetulan sama) diberi akhiran `-2`, `-3`, dst. — tidak pernah menimpa.

## Nominal
Boleh ditulis `150000`, `150rb`, `Rp1.250.000`, `4,5jt`, `1jt 250rb`. Bukan bilangan bulat (mis. `150000.50`)
dibulatkan ke rupiah terdekat (0,5 ke atas) dan diberi peringatan.

## Tanggal
`20/09/2026`, `2026-09-20`, `20 Sep 2026`, `hari ini`, `kemarin`, `3 hari lalu`. **Ditolak**: tanpa tahun, tahun
2 angka, urutan bulan/hari (format Amerika), tanggal masa depan, tanggal sebelum tahun 2000.

## Deteksi duplikat
- **Persis** (`tambah`, `duplikat`): hash SHA-256 isi file sama persis → dianggap file yang sama, `tambah` meminta
  `--izinkan-duplikat` untuk tetap mengarsipkannya.
- **Kemungkinan dobel** (`duplikat`): tanggal + vendor + nominal sama tapi file berbeda (mis. difoto dua kali
  dengan pencahayaan berbeda) — ditampilkan sebagai peringatan, bukan ditolak; pengguna yang memeriksa.

## Kode keluar & JSON
`0` berhasil (termasuk pratinjau), `1` gagal (`error`, plus penanda seperti `belum_ada`, `rusak`, `perlu_izin`),
`2` perintah salah tulis.

## Uji regresi
`python3 tests/uji_regresi.py` (dari folder skill ini).
