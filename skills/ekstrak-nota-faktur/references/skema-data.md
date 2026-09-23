# Skema data ekstraksi & aturan membaca dokumen

Contoh lengkap berisi 6 dokumen ada di `templates/contoh-input.json`.

## 1. Tiga jenis "kosong"

| Situasi | Tulis | Contoh |
|---|---|---|
| Kolom memang **tidak ada** di dokumen | `null` | Nota warung tanpa NPWP → `"npwp": null` |
| Kolom **ada tapi tidak terbaca** (buram, terlipat, tertutup jari, tinta luntur) | `"TIDAK_TERBACA"` | `"total": "TIDAK_TERBACA"` |
| Terbaca sebagian | `"TIDAK_TERBACA"` + tulis yang terlihat di `catatan` | `"catatan": "total terlihat '3?1.500'"` |

**Jangan menebak.** Jangan melengkapi digit yang kabur, jangan menghitung total sendiri lalu menuliskannya sebagai angka dokumen, jangan mengarang item. Angka hasil hitungan hanya boleh muncul sebagai "dihitung script", terpisah dari angka dokumen.

## 2. Kolom per dokumen

| Kunci | Isi | Catatan |
|---|---|---|
| `id` | Label pendek: `N1`, `F2`, atau nama file foto | Dipakai di rekap |
| `jenis` | `nota`, `struk`, `kuitansi`, `invoice`, `faktur_pajak`, `bukti_transfer`, `lainnya` | Lihat bagian 4 |
| `nomor` | Nomor nota/invoice/kuitansi/referensi transfer | Salin persis |
| `nsfp` | Kode & nomor seri faktur pajak | Hanya untuk faktur pajak. Salin persis termasuk titik |
| `tanggal` | `2026-09-01`, `01/09/2026`, atau `1 September 2026` | Tanggal di dokumen, bukan hari ini |
| `penjual` | `{nama, npwp, nitku, alamat, telepon}` | Di faktur: "Pengusaha Kena Pajak" = penjual |
| `pembeli` | `{nama, npwp, nitku, alamat}` | NPWP/NIK pembeli boleh kosong |
| `kategori` | Kategori pengeluaran (bagian 3) | Untuk rekap |
| `item` | Daftar `{nama, qty, satuan, harga_satuan, diskon, jumlah}` | `[]` bila dokumen hanya punya total |
| `subtotal` | Jumlah sebelum diskon/pajak | |
| `diskon` | Diskon total (rupiah) | |
| `dpp` | Dasar Pengenaan Pajak / Harga Jual | Faktur pajak selalu ada |
| `dpp_nilai_lain` | "DPP Nilai Lain" di faktur Coretax | Bila tercetak |
| `ppn` | Nominal PPN tertulis | |
| `jenis_ppn` | `umum` (barang/jasa biasa), `mewah`, `tidak_ada`, `dibebaskan`, `lainnya` | Kosongkan bila tidak jelas; script menganggap `umum` |
| `harga_termasuk_ppn` | `true` bila harga item sudah termasuk PPN (struk minimarket, restoran) | |
| `ppnbm` | Nominal PPnBM | Barang mewah |
| `pph`, `jenis_pph` | PPh yang dipotong, mis. `"PPh 23 (2%)"` | |
| `biaya_lain` | Ongkir, service charge, biaya admin yang **ditambahkan** | |
| `potongan_lain` | Uang muka, voucher, retur yang **dikurangkan** | |
| `meterai` | Nominal meterai **bila ditagihkan** ke pembeli | Bila hanya tertempel: `"ada_meterai": true` |
| `total` | Total yang harus dibayar/yang dibayar | |
| `terbilang` | Salin **persis** dari dokumen | Script membacanya jadi angka |
| `metode_bayar` | tunai, transfer BCA, QRIS, kartu, dll. | |
| `catatan` | Hal penting: bagian terbaca sebagian, cap "LUNAS", coretan | |
| `ikut_rekap` | `false` bila dokumen ini pembayaran atas nota lain | Default `false` untuk `bukti_transfer` |

Angka boleh ditulis gaya Indonesia (`"Rp 1.250.000"`, `"15.000,50"`, `"25.000,-"`) atau angka biasa. **Jangan** pakai format Inggris (`1,250,000.00`): script menolaknya supaya tidak salah baca.

## 3. Kategori pengeluaran (default)
Bahan baku · Bahan kemasan · Operasional · ATK & perlengkapan kantor · Transportasi & BBM · Makan & minum · Listrik, air & internet · Sewa · Jasa · Perbaikan & perawatan · Peralatan · Gaji & upah · Pemasaran · Lain-lain.
Pakai kategori milik pengguna bila ia menyebutkan. Bila ragu, pakai "Lain-lain" dan sebutkan.

## 4. Mengenali jenis dokumen
| Jenis | Ciri |
|---|---|
| `nota` | Tulisan tangan atau cetakan toko, daftar barang + total, jarang ada NPWP |
| `struk` | Cetakan kasir (thermal), sering ada baris "DPP" dan "PPN" dengan harga sudah termasuk PPN |
| `kuitansi` | "Sudah terima dari … Uang sejumlah … Untuk pembayaran …", ada terbilang, kadang meterai |
| `invoice` | "Invoice/Tagihan", nomor invoice, jatuh tempo, rekening tujuan |
| `faktur_pajak` | Judul "Faktur Pajak", ada "Kode dan Nomor Seri Faktur Pajak", NPWP penjual & pembeli, DPP, PPN, QR code |
| `bukti_transfer` | Screenshot m-banking/QRIS: nominal, tanggal, nomor referensi, rekening tujuan |

## 5. Tips foto
- Satu foto = satu dokumen. Bila satu foto berisi beberapa nota, beri id berbeda (`N1a`, `N1b`).
- Struk thermal yang pudar: angka 3/8, 1/7, 5/6, 0/8 sering tertukar. Bila ragu → `TIDAK_TERBACA`.
- Bila total terbaca tapi item tidak: isi total, `item: []`, sebut di catatan.
- Bila foto terpotong: tandai kolom yang terpotong sebagai `TIDAK_TERBACA`.
