# Format input penawaran pemasok

Pengguna tidak wajib memakai format ini; tempelan chat WA apa adanya sudah cukup. Format ini untuk (1) pengguna yang ingin merapikan sendiri, dan (2) agent yang menyusun data sebelum dihitung. Semua contoh fiktif.

## 1. Cara cepat (ketik bebas, satu baris per pemasok)
```
Butuh: 300 pcs, harus tiba dalam 14 hari. Usaha saya bukan PKP.
- CV Kemasan Prima: Rp4.500/pcs, 250+ Rp4.200, 500+ Rp3.900, min 100, ongkir 85rb, PKP harga belum PPN, kirim 5-7 hari, DP 50% sisanya saat barang datang. Sampel bagus.
- UD Sumber Plastik: Rp4.300/pcs, minimal 500, gratis ongkir, bukan PKP, kirim 3 hari, tempo 30 hari.
- Toko Grosir Abadi: Rp4.650/pcs, kirim 2 minggu, COD.
```

## 2. Tabel (Excel/Google Sheets → salin, atau CSV dengan `;`)
Judul kolom bebas huruf besar/kecil. Kolom yang tidak ada boleh dihapus.

| Kolom | Isi | Contoh |
|---|---|---|
| nama | Nama pemasok | CV Kemasan Prima |
| harga | Harga satuan dasar | 4.500 / Rp4.500/pcs / 4,5rb |
| tingkat harga | Harga grosir bertingkat, dipisah `;` atau `\|` | `250: 4.200; 500: 3.900` atau `200: 5%` |
| isi kemasan | Bila harga ditulis per dus/pak: jumlah unit per dus | 24 |
| moq | Minimal order (unit; atau dus bila isi kemasan diisi) | 100 |
| kelipatan | Harus kelipatan berapa | 50 |
| min belanja | Minimal belanja dalam rupiah | 1jt |
| diskon | Diskon persen (`5%`) atau rupiah (`Rp25.000`) | 5% |
| ongkir | Rupiah, `franco`/`gratis`, atau `loco`/`ambil sendiri` | 85rb |
| ongkir ditagih pemasok | `tidak` bila ongkir dibayar langsung ke ekspedisi | ya |
| pkp | Status pemasok: `ya`/`PKP` atau `tidak`/`non-PKP` | PKP |
| harga termasuk ppn | `ya`/`sudah` atau `belum` | belum |
| biaya lain | Biaya lain yang ditagih pemasok (packing kayu, setup cetak) | 50rb |
| biaya sendiri | Biaya yang Anda keluarkan sendiri (ambil barang, bongkar) | 30rb |
| lead time | Hari sampai barang tiba (`3-5 hari`, `2 minggu`, `5 hari kerja`) | 5-7 hari |
| termin | `COD`, `tempo 30 hari`, `DP 50% sisa H+30`, `bayar di muka` | DP 50% |
| kualitas | Penilaian Anda 1-5 (sampel, pengalaman, garansi) | 4 |
| garansi | Garansi/retur yang dijanjikan | retur cacat 7 hari |
| catatan | Hal lain ("harga bisa berubah", "harga sampel") | harga berlaku s.d. 31 Okt |

Contoh CSV siap pakai: `templates/contoh-penawaran.csv`.

## 3. JSON (untuk agent)
```json
{
  "kebutuhan": {"qty": 300, "satuan": "pcs", "butuh_dalam_hari": 14, "pembeli_pkp": false,
                "bobot": {"biaya": 40, "lead_time": 20, "termin": 15, "kualitas": 15, "moq": 10}},
  "pemasok": [
    {"nama": "CV Kemasan Prima", "harga_satuan": "4.500", "tingkat_harga": "250: 4.200; 500: 3.900",
     "moq": 100, "ongkir": "85rb", "pkp": "ya", "harga_termasuk_ppn": "belum", "lead_time": "5-7 hari",
     "termin": "DP 50%, pelunasan saat barang tiba", "nilai_kualitas": 4, "catatan": "sampel bagus"},
    {"nama": "UD Sumber Plastik", "harga_satuan": 4300, "moq": 500, "ongkir": "franco", "pkp": "tidak",
     "lead_time": 3, "termin": "tempo 30 hari", "nilai_kualitas": 3}
  ]
}
```
Kunci lain yang dikenali: `isi_kemasan`, `kelipatan`, `min_belanja`, `diskon_persen`, `diskon_rp`, `ongkir_per_unit`, `ongkir_ditagih_pemasok`, `biaya_lain`, `biaya_luar`, `dp_persen`, `tempo_hari`, `garansi`, `catatan`. Kebutuhan juga bisa lewat opsi baris perintah (`--qty`, `--butuh-hari`, `--pembeli-pkp`, `--bobot`).

## 4. Daftar yang sebaiknya diminta ke setiap pemasok
Agar penawaran bisa dibandingkan setara, minta tertulis:
1. Harga satuan + harga grosir per jumlah, dan **berlaku sampai tanggal berapa**.
2. Minimal order, kelipatan/isi per dus.
3. Ongkir ke alamat Anda (atau franco/loco), dan siapa yang menagih ongkir.
4. Status PKP; harga sudah atau belum termasuk PPN; bisa terbit faktur pajak atau tidak.
5. Lama produksi/kirim sampai barang tiba.
6. Termin bayar (DP, tempo, COD) dan rekening atas nama usaha.
7. Garansi/retur barang cacat, dan apakah barang produksi sama persis dengan sampel.
