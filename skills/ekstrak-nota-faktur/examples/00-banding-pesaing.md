# 00 — Uji banding pesaing (S1 + titik uji S2)

## Sumber
- **Pesaing utama (skill sumber kurasi):** `invoice-extract-id`, github.com/manairalabs/bicara-skills (`skills/invoice-extract-id/SKILL.md` + `examples/faktur-pajak.md`, `examples/kwitansi-umkm.md`), lisensi **MIT**, v0.1.0 (commit `7de3633`, 2026-04-17; commit terbaru `f4c7843`, 2026-09-20, hanya README). Dibaca lewat raw.githubusercontent.com dan git clone baca-saja. **Tidak ada script yang dijalankan** (skill sumber memang tidak punya script, hanya merujuk paket npm `@manairalabs/id-locale`).
- Pencarian lain: `"faktur pajak" filename:SKILL.md` (8 hasil). `openaccountants/indonesia-vat` (AGPL-3.0) adalah skill SPT Masa PPN/klasifikasi transaksi, bukan ekstraksi nota; tidak sebanding. VoltAgent/awesome-openclaw-skills (kategori pdf-and-documents, productivity) hanya berisi generator invoice, bukan pembaca nota Indonesia. alvinindra/bahasa-skills tidak punya skill terkait.

## Output dengan instruksi pesaing (disimulasikan untuk S1)
Instruksi pesaing: output **JSON** per dokumen (skema camelCase bahasa Inggris), tiga cek (`sum(items) ≈ dpp`, `dpp × ppn.rate ≈ ppn.amount`, `dpp + ppn − pph + stampDuty ≈ totalDue`), tarif "11% sampai 2024, 12% mulai Jan 2025; bila dokumen menulis PPN 12%, percayai dokumen", "nota tulisan tangan: tetap isi kolom wajib, tandai keyakinan rendah di notes". Diringkas:

```json
[
 {"documentType":"receipt","documentNumber":"TRX-0903-0045","issueDate":"2026-09-03",
  "vendor":{"name":"Minimarket Sumber Rejeki Fiktif"},"items":[…3 item…],
  "dpp":107387,"ppn":{"rate":0.12,"amount":11813},"totalDue":119200,
  "notes":"Sum of items (119,200) does not match DPP (107,387). DPP × 12% = 12,886, differs from PPN 11,813."},
 {"documentType":"receipt","documentNumber":"0172","issueDate":"2026-09-05",
  "vendor":{"name":"Toko Bahan Kue Aneka Fiktif","npwp":null},"items":[…3 item…],
  "dpp":null,"ppn":{"rate":null,"amount":null},"totalDue":730500,"notes":"Handwritten receipt."},
 {"documentType":"invoice","documentNumber":"INV/SJT/2026/0911","issueDate":"2026-09-10",
  "vendor":{"name":"CV Sejuk Teknik Fiktif","npwp":"0001234567890000"},"items":[…2 item…],
  "dpp":1300000,"ppn":{"rate":0.12,"amount":143000},"totalDue":1443000,
  "amountInWords":"Satu juta empat ratus empat puluh tiga ribu rupiah",
  "notes":"PPN discrepancy: 1,300,000 × 12% = 156,000 but invoice shows 143,000."},
 {"documentType":"receipt","documentNumber":"017/KW/IX/26","issueDate":"2026-09-12",
  "vendor":{"name":"Persewaan Tenda Pak Budi (fiktif)"},"items":[],"totalDue":7500000,
  "amountInWords":"Tujuh juta lima ratus ribu rupiah","stampDuty":null,"notes":null}
]
```
Titik uji S2 (faktur PPN 12% penuh, `02-…md`): menurut aturan pesaing, `10.750.000 × 12% = 1.290.000 ✓`, sehingga **kelebihan PPN Rp 107.500 lolos**. Nomor seri 17 digit Coretax juga berisiko dianggap tidak valid karena pesaing menyebut "faktur pajak sah punya nomor seri 16 digit".

## Output dengan skill kita
Lihat `01-rekap-4-nota-toko-kue.md` dan `02-cek-faktur-pajak-ppn-12-penuh.md`.

## Penilaian

| Kriteria | Pesaing `invoice-extract-id` (MIT) | Skill kita `ekstrak-nota-faktur` |
|---|---|---|
| Kualitas | JSON rapi untuk developer/ERP. Tanpa tabel ringkas, rekap, atau CSV. | Tabel, daftar "yang perlu dicek", rekap, CSV Excel, dan JSON opsional |
| Konteks Indonesia | Baik (NPWP, PPh, terbilang, alamat RT/RW), tetapi **aturan PPN usang** (12% × DPP penuh) dan format faktur e-Faktur lama 16 digit | Aturan PMK 131/2024 (11/12), faktur Coretax 17 digit/NITKU, meterai UU 10/2020, tarif menurut tanggal |
| Akurasi | ❌ 2 alarm palsu di S1 (struk termasuk PPN, invoice 11/12). ❌ Kelebihan PPN di S2 tidak terdeteksi. ❌ Selisih nota tulisan tangan tidak dicek (cek memakai DPP yang kosong). ❌ Terbilang tidak dicek. | ✅ Semua benar, terverifikasi independen (PPN, terbilang 331/331 + 200 pembacaan acak, rekap) |
| Foto buram | "Tetap isi kolom wajib" → rawan menebak | `TIDAK_TERBACA` + catatan, tidak dijumlah (S3) |
| Siap pakai (awam) | Rendah (JSON bahasa Inggris) | Tinggi |

**Hasil: skill kita unggul jelas secara keseluruhan.** Pesaing kalah terutama pada akurasi pajak 2025+, yang merupakan inti "cek faktur".

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. Kolom **jatuh tempo** (`dueDate`) dan **rekening tujuan** (bank, nomor, nama pemilik). Keduanya berguna untuk jadwal bayar dan untuk mencegah penipuan "ganti rekening". Skema kita belum punya kolom rekening/jatuh tempo.
2. Jenis dokumen tambahan: **PO** dan **surat jalan (delivery order)**.
3. Alamat multi-baris (RT/RW, kelurahan, kecamatan) dipertahankan apa adanya.
4. Mode keluaran "JSON untuk impor ERP/akuntansi" dengan nama kolom stabil. Skill kita sudah punya `--format json`, dan ini bisa dipromosikan di README untuk pengguna teknis.
