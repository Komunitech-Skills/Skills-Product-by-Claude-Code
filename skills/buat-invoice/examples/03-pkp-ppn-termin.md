# 03 — Invoice PKP dengan PPN 12% (DPP nilai lain) dan termin 40-30-30

**Skenario:** S3 — permintaan normal: penjual PKP, diskon total, PPN, jadwal termin.

**Input pengguna (persis):**
> Kami PT Solusi Digital Fiktif (PKP, NPWP 00.000.000.0-000.000, Jl. Teknologi No. 8 Bandung). Tolong buat invoice ke CV Mitra Contoh (Jl. Niaga No. 3 Cimahi) untuk pengembangan aplikasi kasir 45 juta dan pelatihan 2 sesi @1,25 juta, kasih diskon 2,5 juta, pakai PPN. Pembayaran termin 40% tgl 7 Oktober, 30% tgl 16 November, 30% tgl 15 Desember. Nomor INV/SDF/2026/09/0021. Rekening Mandiri 000-00-0000000-0. TTD Andi Contoh, Direktur.

**Yang dilakukan agent:** menyusun `invoice-kasir.json`, lalu:
```bash
python3 <folder-skill>/scripts/buat_invoice.py --file invoice-kasir.json --html invoice-kasir.html
```
<details><summary>Isi invoice-kasir.json</summary>

```json
{
  "jenis_dokumen": "invoice",
  "nomor": "INV/SDF/2026/09/0021",
  "tanggal": "2026-09-23",
  "jatuh_tempo": "2026-10-07",
  "penjual": {"nama": "PT Solusi Digital Fiktif", "alamat": "Jl. Teknologi No. 8, Bandung", "email": "tagihan@solusidigital-fiktif.id", "npwp": "00.000.000.0-000.000", "pkp": true},
  "pembeli": {"nama": "CV Mitra Contoh", "alamat": "Jl. Niaga No. 3, Cimahi"},
  "items": [
    {"nama": "Pengembangan aplikasi kasir (web + Android)", "qty": 1, "satuan": "proyek", "harga": "45.000.000"},
    {"nama": "Pelatihan pengguna", "qty": 2, "satuan": "sesi", "harga": "1.250.000"}
  ],
  "diskon": "2.500.000",
  "ppn": {"aktif": true, "jenis": "umum"},
  "termin": [
    {"nama": "Termin 1 (DP)", "persen": 40, "jatuh_tempo": "2026-10-07"},
    {"nama": "Termin 2 (UAT)", "persen": 30, "jatuh_tempo": "2026-11-16"},
    {"nama": "Termin 3 (Go-live)", "persen": 30, "jatuh_tempo": "2026-12-15"}
  ],
  "rekening": [{"bank": "Mandiri", "nomor": "000-00-0000000-0", "atas_nama": "PT Solusi Digital Fiktif"}],
  "catatan": "Pembayaran per termin sesuai jadwal. Faktur pajak diterbitkan terpisah melalui Coretax.",
  "tanda_tangan": {"nama": "Andi Contoh", "jabatan": "Direktur", "kota": "Bandung"}
}
```
</details>

## Output

# INVOICE

**No.:** INV/SDF/2026/09/0021  
**Tanggal:** 23 September 2026  
**Jatuh tempo:** 7 Oktober 2026  
**Status:** BELUM DIBAYAR

**Dari:**  
**PT Solusi Digital Fiktif**  
Jl. Teknologi No. 8, Bandung  
tagihan@solusidigital-fiktif.id  
NPWP: 00.000.000.0-000.000

**Kepada:**  
**CV Mitra Contoh**  
Jl. Niaga No. 3, Cimahi

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Pengembangan aplikasi kasir (web + Android) | 1 proyek | Rp 45.000.000 | - | Rp 45.000.000 |
| 2 | Pelatihan pengguna | 2 sesi | Rp 1.250.000 | - | Rp 2.500.000 |

| | |
|---|---:|
| Subtotal | Rp 47.500.000 |
| Diskon | -Rp 2.500.000 |
| DPP | Rp 45.000.000 |
| DPP nilai lain (11/12) | Rp 41.250.000 |
| PPN 12% | Rp 4.950.000 |
| **TOTAL** | **Rp 49.950.000** |

Terbilang: _Empat Puluh Sembilan Juta Sembilan Ratus Lima Puluh Ribu Rupiah_

**Jadwal pembayaran**

| Termin | Persen | Jumlah | Jatuh tempo |
|---|---:|---:|---|
| Termin 1 (DP) | 40% | Rp 19.980.000 | 7 Oktober 2026 |
| Termin 2 (UAT) | 30% | Rp 14.985.000 | 16 November 2026 |
| Termin 3 (Go-live) | 30% | Rp 14.985.000 | 15 Desember 2026 |

**Pembayaran ke:**
- Mandiri 000-00-0000000-0 a.n. PT Solusi Digital Fiktif

**Catatan:** Pembayaran per termin sesuai jadwal. Faktur pajak diterbitkan terpisah melalui Coretax.

Bandung, 23 September 2026


**Andi Contoh**
Direktur

---
Info untuk penjual (jangan ikut dikirim):
- Bea meterai: Tidak perlu meterai: dokumen tidak menyatakan penerimaan uang di atas Rp5.000.000. Catatan: kuitansi/bukti lunas untuk pembayaran lebih dari Rp5.000.000 nanti wajib bermeterai Rp10.000.
- PPN dihitung dengan DPP nilai lain 11/12 (PMK 131/2024, berlaku per 2026-09-23), dibulatkan ke bawah. Invoice ini bukan faktur pajak; buat faktur pajak di Coretax.
- Pembulatan: jumlah baris & diskon dibulatkan ke rupiah terdekat.
- Versi HTML siap cetak disimpan di: invoice-kasir.html

**Catatan untuk Anda:**
- PPN dihitung 12% × DPP nilai lain (11/12 × Rp45.000.000) = **Rp4.950.000** (efektif 11%). Invoice ini **bukan faktur pajak**; buat faktur pajak di Coretax. Untuk tagihan bertermin, pastikan saat penerbitan faktur per termin sesuai ketentuan — tanyakan ke konsultan pajak Anda bila ragu.
- Tidak perlu meterai di invoice ini, tetapi kuitansi tiap termin (semuanya > Rp5 juta) wajib bermeterai Rp10.000.

## Catatan penguji
- Angka dicek independen: subtotal 47.500.000 − diskon 2.500.000 = DPP 45.000.000; DPP nilai lain 41.250.000; PPN 4.950.000 (floor 11%); total 49.950.000; termin 19.980.000 + 14.985.000 + 14.985.000 = 49.950.000. Benar.
- PPN hanya aktif karena `pkp: true`; peringatan NPWP tidak muncul karena NPWP diisi. Bagus.
- Catatan faktur per termin ditambahkan agent (tidak ada di script) — wajar.
