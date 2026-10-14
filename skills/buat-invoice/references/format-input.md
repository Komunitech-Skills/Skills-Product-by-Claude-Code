# Format Input `buat_invoice.py` (JSON)

Angka boleh gaya Indonesia (`"65.000"`, `"1,5jt"`, `"Rp 3.000.000"`). Diskon: `"5%"` atau nominal `"50.000"`. Tanggal: `2026-09-23` atau `23/09/2026`.

| Kunci | Isi | Default |
|---|---|---|
| `jenis_dokumen` | `invoice` atau `kuitansi` | invoice |
| `nomor` | Nomor manual (mengalahkan penomoran otomatis) | otomatis |
| `prefix` | Awalan nomor | INV (invoice) / KWT (kuitansi) |
| `tanggal` | Tanggal dokumen | hari ini |
| `jatuh_tempo` / `jatuh_tempo_hari` | Tanggal jatuh tempo / jumlah hari dari tanggal dokumen | 14 hari (hanya invoice yang belum lunas) |
| `penjual` | `nama` (wajib), `alamat`, `telepon`, `email`, `npwp`, `pkp` (true/false) | pkp false |
| `pembeli` | `nama` (wajib), `alamat`, `telepon`, `email` | — |
| `items[]` | `nama` (wajib), `qty` (default 1), `satuan`, `harga` (wajib), `diskon` | — |
| `diskon` | Diskon total sebelum ongkir & PPN | 0 |
| `ongkir` | Ongkos kirim | 0 |
| `ppn` | `false`, `true`, atau `{"aktif": true, "jenis": "umum"/"mewah", "ongkir_kena_ppn": true}` | false |
| `pph23` | `false`, `true` (jasa 2%), atau `{"aktif": true, "tanpa_npwp": true}` (4%), `{"dasar": "5.000.000"}` (nilai jasa saja bila ada barang), `{"tarif": 2}`. Hanya info: menampilkan PPh 23 yang dipotong pembeli & estimasi diterima bersih; **total tagihan tidak berubah**. Hanya untuk invoice (v1.0.3) | false |
| `pembayaran[]` | Uang yang **sudah diterima**: `tanggal`, `jumlah`, `keterangan` (mis. "DP") | kosong; kuitansi tanpa pembayaran = lunas penuh |
| `termin[]` | Jadwal: `nama`, `persen` **atau** `jumlah`, `jatuh_tempo` | kosong |
| `rekening[]` | `bank`, `nomor`, `atas_nama` (tampil bila masih ada sisa tagihan). `atas_nama` hanya bila pengguna menyebutnya; kosong -> "a.n." tidak ditulis (v1.0.6) | kosong |
| `catatan` | Syarat/ucapan | kosong |
| `tanda_tangan` | `nama`, `jabatan`, `kota` — hanya dari pengguna, jangan dikarang atau ditebak dari nama pemilik rekening/nama usaha | `[isi kota]`, `[isi nama penanda tangan]` + baris PERLU DIISI |

## Penomoran otomatis
Urutan prioritas: `nomor` di JSON → `--nomor-terakhir` (angka urut terakhir +1, nol di depan dipertahankan; bila bulan/tahun tanggal dokumen lebih baru dari nomor terakhir → periode diganti dan urut mulai 0001, atau dilanjutkan dengan `--urut-lanjut`; tanggal lebih lama → ditolak; format `INV/2026/09/0012`, `012/INV/IX/2026`, `INV-2026-0012` dikenali) → `--counter-file` (urut per prefix/tahun/bulan, file diperbarui) → `PREFIX/TAHUN/BULAN/0001` dengan pengingat.

**Cegah nomor dobel (v1.0.5):** bila `--counter-file` diberikan (boleh bersama `nomor`/`--nomor-terakhir`), file itu menyimpan `"terbit": {nomor: nama pembeli}` dan counter per bulan. Nomor hasil otomatis yang sudah dipakai pembeli lain dinaikkan ke nomor berikutnya yang belum dipakai (dengan PERHATIAN); nomor yang sama untuk pembeli yang sama dianggap revisi (tetap); `nomor` manual yang sudah dipakai pembeli lain → error. Pakai path file yang sama setiap kali (path relatif dibaca dari folder kerja saat script dijalankan).

## Nama berkas HTML (v1.0.6)
`--html invoice-{nomor}.html` mengganti `{nomor}` dengan nomor dokumen yang dicetak (karakter selain huruf/angka/titik/garis bawah, termasuk `/`, menjadi `-`): `001/INV/X/2026` -> `invoice-001-INV-X-2026.html`. `--html <folder>` (folder yang sudah ada, atau berakhir `/`) memberi nama `invoice-<nomor>.html` / `kuitansi-<nomor>.html` otomatis. Path tanpa `{nomor}` dan bukan folder dipakai apa adanya. Setelah menulis berkas, script mencetak **path absolut**-nya pada baris tersendiri `BERKAS: /path/absolut/invoice-001-INV-X-2026.html` (v1.0.7; juga di `--format json` pada `html_disimpan_ke`). Itu path yang dipakai untuk melampirkan berkas ke chat, tanpa disusun ulang.
