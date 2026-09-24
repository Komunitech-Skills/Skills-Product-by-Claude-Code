# 02 — Toko bangunan PKP: PPN harga belum/sudah termasuk, barang per kg/meter pecahan, rekap bulanan + omzet untuk PPh final

**Skenario:** "TB Maju Jaya" (fiktif, Bekasi) sudah PKP, printer 80 mm. Diuji dua kali dengan data identik: (A) harga di daftar **belum** termasuk PPN, (B) harga **sudah** termasuk PPN. Barang dijual per sak, kg, meter, pail, m3. DB uji: `/tmp/uji-kasir-lokal/b/ppn-belum.db` dan `ppn-termasuk.db`.

**Input pengguna (awal):**
> bikinin kasir buat toko bangunan saya, TB Maju Jaya, Jl. Contoh Raya 2 Bekasi, NPWP 00.000.000.0-000.000. kami udah PKP, harga di daftar belum termasuk PPN. printer 80mm. daftar barang terlampir

`produk.csv` (pemisah koma, harga dalam tanda kutip):
```
Kode,Nama,Varian,Harga,Satuan,Stok
SMN50,Semen Tiga Roda,50 kg,"68.500",sak,
PKU5,Paku Kayu,5 cm,"24.750",kg,
KWB,Kawat Bendrat,,"27.300",kg,
PPA,Pipa PVC,1/2 inch,"9.800",meter,
KBL2,Kabel NYM,2x1.5,"11.450",meter,
CAT5,Cat Tembok,5 kg,"139.900",pail,
PSR,Pasir Beton,,"285.000",m3,
```

## Output

### Pengaturan (pratinjau → "ya")
```
Toko: TB Maju Jaya (fiktif) | Pajak: PPN 12% (harga produk belum termasuk PPN) | Stok: tidak dilacak | Kertas struk: 80 mm
Produk baru: 7 | baris rusak: 0
```
Pengaman: tanpa `--pkp ya` script menolak: *"PPN hanya boleh dipungut oleh Pengusaha Kena Pajak (PKP). Jika toko sudah PKP, tambahkan --pkp ya. Jika belum PKP, pakai --pajak tanpa (jangan cantumkan PPN di struk)."*

### Transaksi — mode A: harga BELUM termasuk PPN
| Pesan | Rincian | DPP | PPN (11% × DPP, dibulatkan ke bawah) | Total |
|---|---|---:|---:|---:|
| 10 semen, 1,5 kg paku, 2,25 kg kawat bendrat, bayar tunai 1jt | 685.000 + 37.125 + 61.425 | 783.550 | 86.190 | **869.740** (kembalian 130.260) |
| 12,5 meter pipa pvc, 7,75 meter kabel nym diskon 5%, bayar transfer | 122.500 + (88.738 − 4.437) | 206.801 | 22.748 | **229.549** |
| 2 cat tembok diskon 10%+5%, 1 pasir beton, diskon 3%, bayar qris | (279.800 − 40.571) + 285.000 − 15.727 | 508.502 | 55.935 | **564.437** |
| setengah kg paku, 1 semen, bayar pas | 12.375 + 68.500 | 80.875 | 8.896 | **89.771** |
| 3,333 kg paku, bayar tunai 100rb (15/09) | 82.492 | 82.492 | 9.074 | **91.566** (kembalian 8.434) |
| 20 semen, bayar transfer (20/08) | 1.370.000 | 1.370.000 | 150.700 | **1.520.700** |

Contoh pratinjau lengkap:
```
Nota N-260902-0001 | 02/09/2026 08:10
1. Semen Tiga Roda 50 kg (SMN50) 10 x Rp 68.500 = Rp 685.000
2. Paku Kayu 5 cm (PKU5) 1,5 x Rp 24.750 = Rp 37.125
3. Kawat Bendrat (KWB) 2,25 x Rp 27.300 = Rp 61.425
Subtotal: Rp 783.550
DPP: Rp 783.550 | DPP nilai lain 11/12: Rp 718.254,17 | PPN 12%: Rp 86.190
TOTAL: Rp 869.740
Bayar: Tunai Rp 1.000.000 | Kembalian: Rp 130.260
Catatan: 'semen' dibaca sebagai Semen Tiga Roda 50 kg (SMN50)
```

### Transaksi — mode B: harga SUDAH termasuk PPN (data sama)
| Nota | Total (= harga) | DPP (rupiah bulat terbesar, DPP+PPN ≤ harga) | PPN | Kembalian |
|---|---:|---:|---:|---:|
| N-260902-0001 | 783.550 | 705.901 | 77.649 | 216.450 |
| N-260902-0002 | 206.801 | 186.308 | 20.493 | 0 |
| N-260902-0004 | 508.502 | 458.110 | 50.392 | 0 |
| N-260902-0003 | 80.875 | 72.861 | 8.014 | 0 |
| N-260915-0001 | 82.492 | 74.318 | 8.174 | 17.508 |
| N-260820-0001 | 1.370.000 | 1.234.235 | 135.765 | 0 |

Struk 80 mm (mode B, render Chromium: PDF 80,1 mm, tidak terpotong; gambar 58 mm: `struk-58mm-ppn-termasuk.png`, 80 mm mode A: `struk-80mm-ppn-belum.png`):
```
             TB MAJU JAYA (FIKTIF)
           Jl. Contoh Raya 2, Bekasi
           NPWP 00.000.000.0-000.000
------------------------------------------------
No                                 N-260902-0003
Tgl                             02/09/2026 11:00
------------------------------------------------
Paku Kayu 5 cm
  0,5 kg x 24.750                         12.375
Semen Tiga Roda 50 kg
  1 sak x 68.500                          68.500
------------------------------------------------
Subtotal                                  80.875
TOTAL                                  Rp 80.875
Tunai                                     80.875
------------------------------------------------
Harga sudah termasuk PPN
DPP                                       72.861
DPP nilai lain 11/12                   66.789,25
PPN 12%                                    8.014
------------------------------------------------
         Struk ini bukan faktur pajak.
                  Terima kasih
```

### Retur pecahan dengan koreksi PPN
> kawat bendrat nota pertama kelebihan ambil 0,75 kg, balikin tunai

Percobaan pertama `--item "0,75 kg kawat bendrat"` **ditolak** ("Barang '0,75 kg kawat bendrat' tidak ada di nota…") — kata satuan "kg" tidak dibuang di perintah retur. Diulang `--item "0,75 kawat bendrat"`:
```
RETUR R-260902-0001 atas nota N-260902-0001 | 02/09/2026 15:00      (mode A)
Alasan: kelebihan ambil
- Kawat Bendrat (KWB) 0,75 x | nilai -Rp 20.475
Koreksi PPN: -Rp 2.252 | koreksi DPP: -Rp 20.475
Uang dikembalikan: Tunai Rp 22.727
```
Mode B: nilai −20.475, koreksi DPP −18.446, PPN −2.029, uang kembali Rp 20.475. Retur sisa 1,5 kg: mode A −45.455 (PPN −4.505), mode B −40.950 (PPN −4.059). Setelah seluruh kawat diretur, PPN nota = PPN(722.125) persis.

### Rekap bulanan (mode A, setelah retur)
`rekap --bulan 2026-09` (dipotong):
```
REKAP KASIR SEPTEMBER 2026
TB Maju Jaya (fiktif)
Nota jual: 5 | retur 2
...
PPN terpungut   : Rp 176.086
Omzet tanpa PPN : Rp 1.600.795
...
Catatan PPh final UMKM: omzet (peredaran bruto, tanpa PPN) periode ini Rp 1.600.795. Hitung PPh final 0,5% dengan skill pph-final-umkm (bergantung omzet kumulatif setahun dari SEMUA usaha dan status wajib pajak; orang pribadi: Rp500 juta pertama setahun tidak kena).

_Dasar: UU HPP & PMK 131/2024 (PPN 12%, DPP nilai lain 11/12); PP 55/2022 jo. PP 20/2026 (PPh final 0,5%); berlaku per 24 September 2026. Pembulatan belum dicocokkan dengan Coretax. Alat bantu catat, bukan nasihat pajak; hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
```
Mode B: PPN Rp 158.634, omzet tanpa PPN Rp 1.442.161.

### Rekap tahunan → skill pph-final-umkm
`rekap --tahun 2026` memberi perintah siap pakai; agent bertanya dulu *"Usaha atas nama pribadi atau badan? Ada omzet dari usaha lain tahun ini?"* (jawab: pribadi, tidak ada), lalu menjalankan skill `pph-final-umkm` sungguhan:
```
python3 <folder-pph-final-umkm>/scripts/pph_final.py --jenis op --tahun 2026 --bulan-awal 8 --omzet 1370000 1600795
```
(Skill pph-final-umkm dijalankan penguji dengan data yang sama: Agustus Rp 1.370.000, September omzet kumulatif masih di bawah Rp 500 juta → PPh final Rp 0, disertai catatan & batas setor.)

## Catatan penguji
- **Bagus:** PPN kedua mode cocok 100% dengan perhitungan independen dan dengan `skills/hitung-ppn/scripts/hitung_ppn.py` (48 nilai × 2 mode, 0 beda). DPP persis → dibulatkan ke bawah sekali; mode termasuk memberi DPP terbesar dengan DPP+PPN ≤ harga (sisa 0 di semua contoh). Diskon nota mengurangi DPP (benar). Koreksi PPN retur = PPN(sisa sebelum) − PPN(sisa sesudah). Disclaimer & dasar aturan tercetak. Mode PPN tanpa PKP ditolak.
- **Kurang (SEDANG):** kata satuan milik produk tidak dikenali di pesanan: `2 sak semen`, `2 pail cat tembok`, `semen 2 sak` ditolak "tidak dikenal" (hanya "pcs/buah/porsi/…" dan satuan timbang yang dibuang). Retur tidak membuang satuan sama sekali (`0,75 kg kawat bendrat` ditolak). Pasir per **m3** tidak bisa dijual pecahan (`0,5 m3` ditolak: m3/m2 tidak ada di daftar satuan pecahan) — padahal lazim di toko bangunan.
- **Ringan:** struk mode "belum termasuk" tidak mencetak DPP nilai lain (teks chat mencetaknya) — tidak salah, hanya tidak konsisten.
</content>
</invoke>
