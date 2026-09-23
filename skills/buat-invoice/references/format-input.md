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
| `pembayaran[]` | Uang yang **sudah diterima**: `tanggal`, `jumlah`, `keterangan` (mis. "DP") | kosong; kuitansi tanpa pembayaran = lunas penuh |
| `termin[]` | Jadwal: `nama`, `persen` **atau** `jumlah`, `jatuh_tempo` | kosong |
| `rekening[]` | `bank`, `nomor`, `atas_nama` (tampil bila masih ada sisa tagihan) | kosong |
| `catatan` | Syarat/ucapan | kosong |
| `tanda_tangan` | `nama`, `jabatan`, `kota` | nama penjual |

## Penomoran otomatis
Urutan prioritas: `nomor` di JSON → `--nomor-terakhir` (angka terakhir +1, nol di depan dipertahankan) → `--counter-file` (urut per prefix/tahun/bulan, file diperbarui) → `PREFIX/TAHUN/BULAN/0001` dengan pengingat.
