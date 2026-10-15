# Dasar aturan PPN untuk SPH — berlaku per 2026-09-23 (bagian bea meterai dicek ulang 2026-10-15)

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

## Bea meterai (UU No. 10 Tahun 2020 tentang Bea Meterai)
- SPH pada umumnya bukan dokumen yang wajib bermeterai.
- **Objek (Pasal 3 ayat (2)):** huruf a menyebut «surat perjanjian, surat keterangan, surat pernyataan, atau surat lainnya yang sejenis, beserta rangkapnya» **tanpa batas nilai**; ambang **lebih dari Rp5.000.000** hanya ada di huruf g, yaitu dokumen yang menyebut **penerimaan uang** atau pengakuan bahwa utang **telah dilunasi/diperhitungkan** (mis. kuitansi/tanda terima pelunasan).
- **Tarif (Pasal 5):** «Dokumen sebagaimana dimaksud dalam Pasal 3 dikenai Bea Meterai dengan tarif tetap sebesar Rp10.000,00 (sepuluh ribu rupiah).»
- **Saat terutang (Pasal 8 ayat (1) huruf a):** untuk surat perjanjian, saat dokumen **dibubuhi tanda tangan**.
- Jika SPH ditandatangani kedua pihak sebagai kesepakatan (menjadi perjanjian), sarankan pengguna memakai meterai / skill `perjanjian-sederhana`.
- Dibaca langsung dari teks resmi (salinan) UU 10/2020 di pajak.go.id, diakses 2026-10-15 (tautan di bagian Sumber).

## Sumber
- https://www.pajak.go.id/en/node/113453
- https://peraturan.bpk.go.id/Details/311485/pmk-no-131-tahun-2024
- https://news.ddtc.co.id/berita/nasional/1812992/tak-berubah-tarif-ppn-12-tetap-berlaku-untuk-barang-mewah-di-2026
- https://pajak.go.id/en/node/115238 (Coretax & faktur)
- https://www.pajak.go.id/sites/default/files/2020-11/UU%20Nomor%2010%20Tahun%202020%20tentang%20Bea%20Materai.pdf (UU 10/2020 tentang Bea Meterai, teks resmi; Pasal 3, 5, 8; diakses 2026-10-15)
