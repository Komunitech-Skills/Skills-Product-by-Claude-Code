# Pajak di kasir-lokal — berlaku per 24 September 2026

> Alat bantu catat, **bukan nasihat pajak**. Butir berlabel **BELUM TERVERIFIKASI** tidak boleh disampaikan sebagai kepastian; arahkan pengguna ke DJP (Kring Pajak 1500200 / pajak.go.id), Bapenda setempat, atau konsultan pajak.

## Pilihan mode pajak toko (`atur --pajak ...`)
| Mode | Untuk siapa | Yang terjadi di nota |
|---|---|---|
| `tanpa` (default) | Toko **bukan PKP** (mayoritas UMKM), atau usaha yang pajaknya bukan PPN | Tidak ada baris pajak di struk. Omzet tetap tercatat untuk PPh final |
| `ppn-belum` + `--pkp ya` | PKP yang harga di daftarnya **belum** termasuk PPN | Pembeli membayar DPP + PPN |
| `ppn-termasuk` + `--pkp ya` | PKP yang harga di daftarnya **sudah** termasuk PPN | Total = harga; DPP & PPN dipisahkan di struk |

Script **menolak** mode PPN tanpa `--pkp ya`: pengusaha yang belum dikukuhkan PKP tidak boleh memungut PPN atau mencantumkannya di struk.

## PPN (UU HPP; PMK 131/2024, berlaku 1 Januari 2025)
| Hal | Ketentuan | Status |
|---|---|---|
| Tarif | 12% | Terverifikasi (lihat `skills/hitung-ppn/references/regulasi.md`) |
| Barang/jasa non-mewah | PPN = 12% × DPP nilai lain, DPP nilai lain = 11/12 × harga jual → efektif 11% | Terverifikasi |
| Barang mewah (PPnBM) | 12% × harga penuh | **Tidak didukung** kasir ini (arahkan ke `hitung-ppn`/konsultan) |
| Yang boleh memungut | Hanya PKP; faktur pajak dibuat di Coretax | Terverifikasi |

**Rumus & pembulatan (standar library Komunitech, sama persis dengan skill `hitung-ppn`):**
- PPN dihitung **per nota** dari DPP persis: `PPN = floor(11% × DPP)` (dibulatkan ke bawah sekali, tidak pernah melebihi tarif). 11% × DPP identik dengan 12% × 11/12 × DPP, jadi tidak ada pembulatan berantai.
- Harga belum termasuk PPN: `DPP = total setelah diskon`; `bayar = DPP + PPN`.
- Harga sudah termasuk PPN (T): `DPP` = rupiah bulat terbesar dengan `DPP + floor(11% × DPP) ≤ T`; `sisa = T − DPP − PPN` (Rp 0–1) ditampilkan sebagai selisih pembulatan.
- DPP nilai lain (11/12 × DPP) ditampilkan 2 desimal sebagai informasi.
- Retur/void: `koreksi = pajak(sisa sesudah) − pajak(sisa sebelum)`, jadi retur penuh mengembalikan PPN persis ke Rp 0.
- **Belum dicocokkan dengan Coretax.** Bila faktur di Coretax berbeda Rp 1, ikuti Coretax.
- Diuji otomatis: untuk ratusan nilai, DPP/PPN kasir = hasil `hitung_ppn.py` (tes `test_08`).

Contoh: harga termasuk PPN Rp 53.000 → DPP Rp 47.748, DPP nilai lain Rp 43.769, PPN Rp 5.252 (47.748 + 5.252 = 53.000).

**Struk bukan faktur pajak.** Struk mencetak "Struk ini bukan faktur pajak" di mode PPN.

## PPh final UMKM 0,5% (PP 55/2022 jo. PP 20/2026)
- Kasir **tidak menghitung dan tidak mencetak** PPh final. Kasir hanya menyiapkan **omzet (peredaran bruto)** = uang diterima − PPN, setelah retur/void.
- `rekap --bulan ...` menampilkan omzet bulan itu; `rekap --tahun 2026` menampilkan omzet per bulan + perintah siap pakai untuk skill `pph-final-umkm`.
- Sebelum menghitung, tanyakan: jenis wajib pajak (orang pribadi/badan) dan **omzet usaha lain** (marketplace, jasa, cabang lain) — PPh final dihitung dari omzet semua usaha. Orang pribadi: Rp 500 juta pertama setahun tidak kena (lihat `skills/pph-final-umkm/references/regulasi.md`).

## Warung makan, kafe, restoran — PBJT (pajak daerah)
- Makanan/minuman yang disajikan restoran/kafe/warung makan umumnya **bukan objek PPN**, melainkan **Pajak Barang dan Jasa Tertentu (PBJT) makanan/minuman** milik pemerintah kabupaten/kota (UU 1/2022 tentang HKPD; tarif ditetapkan Perda, paling tinggi 10%). **BELUM TERVERIFIKASI** di riset repo ini; batas omzet & tarif berbeda per daerah.
- Kasir versi 1.0.0 **belum** punya mode PBJT. Untuk usaha makanan/minuman: pakai mode `tanpa`, jangan memakai mode PPN untuk "pajak resto", dan arahkan pemilik ke Bapenda setempat. (Usulan fitur versi berikutnya.)

## Disclaimer yang dicetak script
"Dasar: UU HPP & PMK 131/2024 (PPN 12%, DPP nilai lain 11/12); PP 55/2022 jo. PP 20/2026 (PPh final 0,5%); berlaku per 24 September 2026. Pembulatan belum dicocokkan dengan Coretax. Alat bantu catat, bukan nasihat pajak; hubungi DJP (Kring Pajak 1500200) atau konsultan pajak."

## Sumber
- DJP — PPN 12% & DPP nilai lain: https://www.pajak.go.id/en/node/113453
- PMK 131/2024 (JDIH BPK): https://peraturan.bpk.go.id/Details/311485/pmk-no-131-tahun-2024
- DJP — PP 20/2026 (PPh final UMKM): https://www.pajak.go.id/en/node/119950
- UU 1/2022 HKPD: cari "UU Nomor 1 Tahun 2022" di https://peraturan.bpk.go.id (PBJT; alamat halaman belum diverifikasi, perlu dicek ulang)
