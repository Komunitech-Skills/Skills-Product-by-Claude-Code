# Dasar aturan PPN untuk SPH — berlaku per 2026-09-23

> Ringkasan untuk keperluan menyusun penawaran harga. Bukan nasihat pajak. Aturan bisa berubah; cek pajak.go.id atau konsultan pajak sebelum dipakai untuk kasus khusus.

## Siapa yang boleh mencantumkan PPN
- Hanya **Pengusaha Kena Pajak (PKP)** yang boleh memungut PPN dan membuat faktur pajak.
- Usaha yang belum dikukuhkan sebagai PKP **tidak boleh** menagih PPN kepada pembeli. Di SPH cukup tulis "Harga tidak dikenakan PPN".
- Batas pengusaha kecil (wajib PKP bila omzet melewati) Rp4,8 miliar/tahun — ketentuan lama, belum dicek ulang pada riset 2026-09-23; jangan dipakai sebagai kepastian.

## Tarif & DPP (UU HPP jo. PMK 131/2024)
| Jenis | Rumus | Efektif |
|---|---|---|
| Barang/jasa **non-mewah** (umum) | PPN = 12% × DPP nilai lain; DPP nilai lain = 11/12 × harga jual | 11% dari harga jual |
| Barang **mewah** (kena PPnBM) | PPN = 12% × harga jual | 12% (PPnBM dihitung terpisah) |
| Barang/jasa yang punya DPP nilai lain / besaran tertentu tersendiri | Ikuti aturan khususnya | — (di luar cakupan skill) |

Harga sudah termasuk PPN (non-mewah): DPP = rupiah bulat terbesar sehingga DPP + PPN ≤ harga (≈ harga ÷ 1,11); sisa Rp 0–1 ditampilkan sebagai selisih pembulatan.

**Pembulatan (standar library Komunitech):** PPN dihitung persis dari DPP lalu dibulatkan **ke bawah** sekali (tidak memungut melebihi tarif); nominal lain ke rupiah terdekat. Belum dicocokkan dengan Coretax — faktur resmi bisa berbeda Rp 1.

## Faktur pajak
- Faktur pajak dibuat PKP melalui Coretax / e-Faktur Desktop / H2H (KEP-54/PJ/2025). SPH **bukan** faktur pajak.

## Bea meterai
- SPH pada umumnya bukan dokumen yang wajib bermeterai.
- Bea meterai Rp10.000 (UU 10/2020 Pasal 3): **surat perjanjian/pernyataan** dikenai meterai **berapa pun nilainya**; ambang **> Rp5.000.000** hanya berlaku untuk dokumen yang menyebut **penerimaan uang** atau pernyataan bahwa utang **telah dilunasi** (mis. kuitansi/tanda terima pelunasan).
- Jika SPH ditandatangani kedua pihak sebagai kesepakatan (menjadi perjanjian), sarankan pengguna memakai meterai / skill `perjanjian-sederhana`.
- Dicek per 2026-09-23. Sumber ringkasan: https://www.online-pajak.com/pajak/materai-10000/ *(teks resmi UU 10/2020 Pasal 3 belum dibaca langsung — perlu review)*

## Sumber
- https://www.pajak.go.id/en/node/113453
- https://peraturan.bpk.go.id/Details/311485/pmk-no-131-tahun-2024
- https://news.ddtc.co.id/berita/nasional/1812992/tak-berubah-tarif-ppn-12-tetap-berlaku-untuk-barang-mewah-di-2026
- https://pajak.go.id/en/node/115238 (Coretax & faktur)
- https://www.online-pajak.com/pajak/materai-10000/ (bea meterai)
