# Template Daftar Utang

Isi semua utang, termasuk paylater dan pinjaman keluarga. Lalu salin tiap baris ke format script:
`--utang "Nama;Sisa saldo;Bunga;Cicilan minimum;jenis"`

| Nama | Jenis (kk/kta/paylater/pinjol/kpr/motor/mobil/keluarga/lain) | Sisa saldo | Bunga (angka + per th/bln/hari) | Flat atau efektif? | Cicilan minimum | Jatuh tempo tgl | Terdaftar OJK? (pinjol) |
|---|---|---:|---|---|---:|---|---|
| | | Rp | | | Rp | | |
| | | Rp | | | Rp | | |
| | | Rp | | | Rp | | |

Uang ekstra per bulan di atas semua cicilan minimum: Rp__________

Catatan:
- Bunga **flat** (leasing motor/mobil, sebagian KTA/koperasi) → ubah dulu ke efektif: `python3 scripts/keuangan.py konversi-flat --pokok ... --bunga-flat ... --tenor ...` (atau `--cicilan` dari kontrak).
- Pinjol: cek legalitas di ojk.go.id, Kontak OJK 157, atau WA 081-157-157-157.
- Sisa saldo kartu kredit = tagihan penuh terakhir (bukan pembayaran minimum).
