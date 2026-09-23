# Pemetaan Kategori & Kata Kunci

Script mengklasifikasi setiap transaksi dengan urutan:
1. `--tetapkan BARIS=KODE` dari pengguna (paling kuat).
2. Kolom **Kategori** di file (jika ada), dicocokkan ke kode/label/kata kunci.
3. Kata kunci di **Keterangan**. Kata kunci kustom (`--pemetaan`) dicek sebelum kata kunci bawaan.
4. Tidak cocok → masuk daftar **"Transaksi belum terklasifikasi"** (dihitung sementara sebagai pemasukan/pengeluaran lain-lain dan status laporan menjadi SEMENTARA).

Setiap kategori punya arah (uang masuk/keluar). Kata kunci hanya berlaku untuk arah yang sesuai, jadi "bayar bon" (keluar) = bayar utang pemasok, sedangkan "bayar bon" (masuk) = pelanggan melunasi piutang.
Kata kunci ≤ 3 huruf dicocokkan sebagai kata utuh (mis. `air`, `kur`, `dp`); yang lebih panjang dicocokkan di awal kata (`gaji` cocok dengan "gajian").

Lihat daftar lengkap kata kunci terkini dengan:
```bash
python3 <folder-skill-ini>/scripts/laporan_emkm.py --daftar-kategori
```

## Kode kategori & perlakuan

| Kode | Arah | Masuk laporan sebagai | Contoh kata kunci |
|---|---|---|---|
| `pendapatan_usaha` | masuk | Pendapatan usaha | penjualan, jual, omzet, pesanan, shopee, qris, dp, jasa |
| `retur_penjualan` | keluar | Pengurang pendapatan | retur, refund, pengembalian dana |
| `pendapatan_lain` | masuk | Pendapatan lain-lain | bunga tabungan, jasa giro, cashback, hadiah, bantuan |
| `penjualan_aset` | masuk | Pendapatan lain-lain (+ peringatan nilai buku) | jual aset, jual peralatan, rongsok |
| `pembelian_bahan` | keluar | Pembelian → Beban pokok penjualan | bahan, kulakan, stok, tepung, telur, kain, supplier |
| `beban_gaji` | keluar | Beban usaha | gaji, upah, lembur, THR, karyawan, tukang |
| `beban_sewa` | keluar | Beban usaha | sewa, kontrakan, ruko, kios, lapak |
| `beban_utilitas` | keluar | Beban usaha | listrik, PLN, token, air, PDAM, gas, internet, pulsa |
| `beban_transportasi` | keluar | Beban usaha | bensin, ongkir, ekspedisi, JNE, gosend, parkir |
| `beban_pemasaran` | keluar | Beban usaha | iklan, ads, promosi, endorse, brosur |
| `beban_admin_penjualan` | keluar | Beban usaha | admin shopee, biaya layanan, komisi, MDR |
| `beban_perlengkapan` | keluar | Beban usaha | kemasan, plastik, kardus, ATK, stiker, cup |
| `beban_perawatan` | keluar | Beban usaha | servis, perbaikan, oli, sparepart |
| `beban_pajak_lain` | keluar | Beban usaha (pajak daerah) | PB1/PBJT/pajak restoran (+ ditanyakan), PBB, retribusi, pajak kendaraan, meterai |
| `beban_lain` | keluar | Beban usaha | iuran, keamanan, sampah, langganan aplikasi, asuransi |
| `beban_keuangan` | keluar | Beban keuangan | bunga pinjaman, admin bank, biaya transfer |
| `beban_pajak_penghasilan` | keluar | Beban pajak penghasilan | PPh, pajak UMKM, pajak final, "pajak" |
| `prive` | keluar | Pengurang modal (BUKAN beban) | prive, pribadi, rumah tangga, SPP, gaji pemilik, keluarga |
| `setoran_modal` | masuk | Tambahan modal | modal, setoran pemilik, uang pribadi, tabungan pribadi |
| `pinjaman_diterima` | masuk | Utang bank/pinjaman naik | pinjaman, KUR, pencairan kredit, utang |
| `bayar_pinjaman` | keluar | Utang bank/pinjaman turun | cicilan, angsuran, bayar utang, kredit |
| `bayar_utang_usaha` | keluar | Utang pemasok turun | bayar supplier, bayar bon, bayar tempo, utang dagang |
| `terima_piutang` | masuk | Piutang turun | piutang, pelunasan bon, bayar tempo, tagihan pelanggan |
| `aset_tetap` | keluar | Aset tetap naik | mesin, etalase, kulkas, oven, laptop, motor, renovasi |
| `transfer_internal` | dua arah | Pindah dana antar kas/rekening sendiri | setor tunai, tarik tunai, pindah buku |
| `titipan_pajak` | dua arah | Utang pajak daerah (neraca). Masuk = PB1/PBJT dipungut dari pembeli, keluar = penyetoran. Bukan pendapatan/beban. Hanya lewat `--tetapkan` atau pemetaan. | (tidak otomatis) |
| `piutang_lain` | dua arah | Kasbon karyawan/piutang lain (aset); keluar = kasbon diberikan, masuk = pelunasan/potong kasbon | kasbon, pinjaman karyawan, potong kasbon |

**Kategori baru:** di file pemetaan boleh membuat kode baru berawalan `beban_` (menjadi beban usaha) atau `pendapatan_` (menjadi pendapatan usaha).

## Contoh file pemetaan (`--pemetaan pemetaan.json`)
```json
{
  "pembelian_bahan": ["deterjen", "pewangi"],
  "prive": ["kasih ke adik", "arisan keluarga"],
  "beban_iuran_lingkungan": {"label": "Iuran lingkungan", "kata": ["pak rt", "iuran rt"]}
}
```

## Prioritas penting
- Kata kerja pembelian barang dagangan (`kulakan`, `kulak`, `restock`, `stok`, `untuk dijual`, `air mineral`) dicek **sebelum** utilitas, sehingga "kulakan gas melon" = pembelian barang dagangan, bukan beban gas.
- `iuran`, `keamanan`, `kebersihan`, `sampah` dicek **sebelum** kata `pasar`, sehingga "iuran kebersihan pasar" = beban lain, bukan pembelian bahan.
- `bpjs` = beban gaji. `kasbon` dicek sebelum kata `pinjaman`.

## Kasus yang sengaja ditanyakan, bukan ditebak
- **Angsuran/cicilan pinjaman**: porsi bunga vs pokok (script menanyakan otomatis; jawab dengan `--bunga BARIS=NOMINAL`).
- **PB1/PBJT**: bila dipungut terpisah dari pembeli, tetapkan `titipan_pajak` untuk pemungutan & penyetorannya; bila sudah termasuk penjualan, tetapkan `beban_pajak_lain`. Pertanyaan tertutup setelah baris itu di-`--tetapkan`.
- "Transfer", "kirim", "ambil ATM" tanpa keterangan lain.
- "PPN", "zakat" (usaha atau pribadi?), "arisan", "belanja dapur rumah" (bila tidak jelas pribadi).
- "Cicilan" motor/HP: script memperlakukannya sebagai pembayaran pinjaman; jika itu barang pribadi → minta pengguna menetapkan `prive`.
- Pembelian aset kecil (mis. rak Rp 50.000) otomatis masuk aset tetap bila kata kuncinya cocok; jika pengguna ingin langsung dibebankan, tetapkan ke `beban_perlengkapan`.
