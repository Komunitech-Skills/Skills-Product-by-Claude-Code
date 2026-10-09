# Template nota ringkas (non-PPN, siap tempel di chat)

Nota ini bukti pesanan sederhana, **bukan** faktur pajak. Untuk invoice formal (perusahaan, termin, PPN/PKP, kuitansi, meterai) pakai skill `buat-invoice`.

```
NOTA PESANAN — [nama toko]
No.     : [kode pesanan]
Tanggal : [tanggal]
Kepada  : [nama panggilan pelanggan]

[nama barang] x[qty] @[harga]   [total baris]
...
Subtotal                 [subtotal]
Diskon [label]          -[diskon]
Ongkir [kurir]           [ongkir]
TOTAL                    [total]
Status : [LUNAS / BELUM BAYAR (sisa [sisa]) / COD]
Bayar ke: [bank] [no rek] a.n. [nama]

Terima kasih sudah berbelanja 🙏
```
Angka disalin persis dari rekap. Harga atau ongkir yang belum diketahui: `[isian: ...]`, dan baris TOTAL ditulis `[isian: total]`.
