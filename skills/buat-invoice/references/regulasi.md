# Dasar Aturan Invoice — berlaku per 23 September 2026

> Ringkasan untuk alat bantu, bukan nasihat hukum/pajak.

## Bea Meterai (UU 10/2020)
| Hal | Ketentuan | Status |
|---|---|---|
| Tarif | Tunggal **Rp10.000** (meterai tempel atau e-meterai) | Terverifikasi |
| Dokumen yang menyatakan **penerimaan uang** / pengakuan utang | Wajib bila nilainya **> Rp5.000.000** (tepat Rp5.000.000 tidak wajib) | Terverifikasi |
| Surat perjanjian & akta | Wajib berapa pun nilainya | Terverifikasi (di luar cakupan skill) |
| Invoice yang hanya menagih (belum ada uang diterima) | Skill menganggap tidak menyatakan penerimaan uang → tidak ditandai wajib | Interpretasi skill; kasus ragu → konsultan |

## PPN pada invoice
- Hanya **PKP** yang boleh memungut PPN. Tarif 12% × DPP nilai lain 11/12 (non-mewah, efektif 11%); 12% × harga untuk barang mewah (UU HPP, PMK 131/2024).
- Logika hitung sama persis dengan skill `hitung-ppn` (`scripts/hitung_ppn.py` disalin apa adanya). PPN dibulatkan ke bawah ke rupiah penuh.
- Ongkir yang ditagihkan penjual dianggap bagian dari DPP (default). Bila ongkir hanya penggantian biaya yang ditagih terpisah, pengguna bisa mengatur `ongkir_kena_ppn: false`. **Perlakuan ongkir perlu dikonfirmasi ke konsultan untuk kasus spesifik.**
- Invoice bukan faktur pajak. Faktur pajak dibuat PKP lewat Coretax / e-Faktur Desktop / H2H (KEP-54/PJ/2025).

## Sumber
- Bea meterai Rp10.000: https://www.online-pajak.com/pajak/materai-10000/
- DJP — PPN 12% & DPP nilai lain: https://www.pajak.go.id/en/node/113453
- PMK 131/2024: https://peraturan.bpk.go.id/Details/311485/pmk-no-131-tahun-2024
- DJP — Coretax & faktur: https://pajak.go.id/en/node/115238
