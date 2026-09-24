# Pajak di kasir-lokal (v1.1.0) — berlaku per 24 September 2026

> Alat bantu catat, **bukan nasihat pajak**. Butir berlabel **BELUM TERVERIFIKASI** tidak boleh disampaikan sebagai kepastian; arahkan pengguna ke DJP (Kring Pajak 1500200 / pajak.go.id), Bapenda setempat, atau konsultan pajak.

## Pilihan mode pajak toko (`atur --pajak ...`)
| Mode | Untuk siapa | Yang terjadi di nota |
|---|---|---|
| `tanpa` (default) | Toko **bukan PKP** (mayoritas UMKM), atau usaha kuliner yang belum terdaftar/di bawah batas PBJT | Tidak ada baris pajak di struk. Omzet tetap tercatat untuk PPh final |
| `ppn-belum` + `--pkp ya` | PKP yang harga di daftarnya **belum** termasuk PPN | Pembeli membayar DPP + PPN |
| `ppn-termasuk` + `--pkp ya` | PKP yang harga di daftarnya **sudah** termasuk PPN | Total = harga; DPP & PPN dipisahkan di struk |

| `pbjt-belum` + `--tarif-pbjt N` | Restoran/kafe/warung makan/katering terdaftar PBJT; harga menu **belum** termasuk pajak | Pembeli membayar harga + PBJT (+ service charge bila ada) |
| `pbjt-termasuk` + `--tarif-pbjt N` | Sama, harga menu **sudah** termasuk PBJT | Total = harga; dasar & PBJT dipisahkan di struk |

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
- Kasir **tidak menghitung dan tidak mencetak** PPh final. Kasir hanya menyiapkan **omzet (peredaran bruto)** = uang diterima − PPN/PBJT (termasuk service charge), setelah retur/void.
- `rekap --bulan ...` menampilkan omzet bulan itu; `rekap --tahun 2026` menampilkan omzet per bulan + perintah siap pakai untuk skill `pph-final-umkm`.
- Sebelum menghitung, tanyakan: jenis wajib pajak (orang pribadi/badan) dan **omzet usaha lain** (marketplace, jasa, cabang lain) — PPh final dihitung dari omzet semua usaha. Orang pribadi: Rp 500 juta pertama setahun tidak kena (lihat `skills/pph-final-umkm/references/regulasi.md`).

## PBJT makanan/minuman — restoran, kafe, warung makan, katering (UU 1/2022 tentang HKPD)
Sumber utama: salinan resmi UU 1/2022 dari DJPK Kemenkeu — https://djpk.kemenkeu.go.id/wp-content/uploads/2022/01/Salinan-UU-Nomor-1-Tahun-2022.pdf (halaman: https://djpk.kemenkeu.go.id/?p=22499). Diverifikasi penguji independen 24 September 2026. Salinan JDIH BPK (https://peraturan.bpk.go.id/Details/195660/uu-no-1-tahun-2022) **perlu dicek manual** (diblokir saat uji).

| Pasal UU 1/2022 | Isi ringkas | Dipakai di kasir |
|---|---|---|
| Pasal 1 angka 42 | PBJT = pajak yang dibayar **konsumen akhir** atas konsumsi barang/jasa tertentu | PBJT ditambahkan/ditampilkan di nota pembeli |
| Pasal 1 angka 44–45 | Makanan/minuman = yang disediakan/dijual oleh **restoran** (langsung/tidak langsung/pesanan); restoran = fasilitas penyediaan makanan/minuman dengan bayaran | Pertanyaan jenis usaha di langkah A.1 |
| Pasal 4 ayat (2) huruf c | PBJT = pajak **kabupaten/kota** | Setor & lapor ke Bapenda, bukan DJP |
| Pasal 50 huruf a | Objek PBJT meliputi makanan dan/atau minuman | — |
| Pasal 51 ayat (1) | Restoran yang paling sedikit menyediakan meja, kursi, dan/atau peralatan makan-minum; jasa boga/katering | — |
| Pasal 51 ayat (2) | Dikecualikan antara lain: peredaran usaha **tidak melebihi batas di Perda**; toko swalayan yang tidak semata-mata menjual makanan/minuman; pabrik makanan/minuman; lounge bandara | Usaha di bawah batas → mode `tanpa` |
| Pasal 56 | Subjek = konsumen; **Wajib Pajak = penjual** (pemilik usaha memungut & menyetor) | Rekap menampilkan "PBJT dipungut" + pengingat setor |
| Pasal 57 ayat (1) | Dasar pengenaan = **jumlah yang dibayarkan konsumen** | Dasar = total setelah diskon; **tanpa** DPP 11/12 |
| Pasal 58 ayat (1), (4) | Tarif **paling tinggi 10%**, ditetapkan dengan Perda | `--tarif-pbjt` wajib diisi pengguna; > 10 ditolak |
| Pasal 59 | Pokok PBJT = dasar pengenaan × tarif | Rumus di bawah |
| Pasal 94 | Seluruh jenis & tarif pajak daerah ditetapkan dalam 1 Perda | Minta pengguna cek Perda/SKPD |
| Pasal 187 huruf b | Perda lama ("pajak restoran" UU 28/2009) berlaku paling lama 2 tahun sejak UU diundangkan (5 Januari 2022) | — |

**Hubungan dengan PPN:** makanan dan minuman yang disajikan di hotel, restoran, rumah makan, warung, dan sejenisnya (termasuk dibawa pulang dan katering) yang merupakan objek pajak daerah **tidak dikenai PPN** — Pasal 4A ayat (2) huruf c UU PPN s.t.d.t.d. UU HPP (DJP: https://www.pajak.go.id/en/node/81110). Karena itu script **menolak** menggabungkan PPN dan PBJT (`--tarif-pbjt` bersama `--pajak ppn-*`). Pengecualian (swalayan yang tidak semata-mata menjual makanan, pabrik, lounge bandara) bisa kena PPN (PMK 70/2020 menurut DDTC; teks PMK belum dicek) → arahkan ke konsultan.

**Rumus & pembulatan PBJT (keputusan desain, konsisten dengan standar PPN library):**
- Tarif r = tarif Perda ÷ 100 (boleh desimal, mis. 2,5%).
- `pbjt-belum`: dasar = total setelah diskon (+ service charge bila `--sc-kena-pajak ya`); **PBJT = floor(r × dasar)** — dibulatkan **ke bawah sekali** agar tidak pernah memungut melebihi tarif; total = dasar + PBJT (+ service charge bila tidak kena).
- `pbjt-termasuk`: dasar = rupiah bulat terbesar dengan dasar + floor(r × dasar) ≤ harga; sisa (Rp 0–1) ditampilkan.
- Retur/void: koreksi = PBJT(sisa sesudah) − PBJT(sisa sebelum).
- **Belum dicocokkan dengan sistem pajak daerah/Bapenda (e-SPTPD, tapping box, dsb.).** Bila Bapenda memakai cara pembulatan atau cara hitung lain (mis. per bulan dari omzet), ikuti Bapenda.
- Contoh tarif 10%: 45.900 → PBJT 4.590 → bayar 50.490. Termasuk PBJT 53.000 → dasar 48.182, PBJT 4.818.

**Service charge:** opsional (`--service-charge N`), dihitung dari total setelah diskon, dibulatkan ke rupiah terdekat, dan hanya untuk harga *belum* termasuk pajak. Apakah service charge termasuk dasar pengenaan PBJT **tidak ditentukan skill ini** — mengikuti Perda/arahan Bapenda setempat; pengguna wajib memilih `--sc-kena-pajak ya|tidak`. Service charge ikut dihitung sebagai omzet untuk PPh final.

**Yang tidak dilakukan kasir:** mendaftarkan wajib pajak daerah, membuat SSPD/kode bayar, melapor SPTPD, menghitung sanksi, menentukan batas omzet Perda. Arahkan ke Bapenda setempat.

## Disclaimer yang dicetak script
PBJT: "Dasar: UU 1/2022 (HKPD) Pasal 50 huruf a, 51, 56, 57 ayat (1), 58 ayat (1) & (4); tarif sesuai Perda daerah Anda (paling tinggi 10%); berlaku per 24 September 2026. Pembulatan belum dicocokkan dengan sistem pajak daerah/Bapenda. Alat bantu catat, bukan nasihat pajak; tanyakan Bapenda setempat."

PPN/PPh: "Dasar: UU HPP & PMK 131/2024 (PPN 12%, DPP nilai lain 11/12); PP 55/2022 jo. PP 20/2026 (PPh final 0,5%); berlaku per 24 September 2026. Pembulatan belum dicocokkan dengan Coretax. Alat bantu catat, bukan nasihat pajak; hubungi DJP (Kring Pajak 1500200) atau konsultan pajak."

## Sumber
- DJP — PPN 12% & DPP nilai lain: https://www.pajak.go.id/en/node/113453
- PMK 131/2024 (JDIH BPK): https://peraturan.bpk.go.id/Details/311485/pmk-no-131-tahun-2024
- DJP — PP 20/2026 (PPh final UMKM): https://www.pajak.go.id/en/node/119950
- UU 1/2022 HKPD (salinan resmi DJPK): https://djpk.kemenkeu.go.id/wp-content/uploads/2022/01/Salinan-UU-Nomor-1-Tahun-2022.pdf ; JDIH BPK https://peraturan.bpk.go.id/Details/195660/uu-no-1-tahun-2022 (perlu dicek manual)
- DJP — makanan/minuman objek pajak daerah bukan objek PPN: https://www.pajak.go.id/en/node/81110
