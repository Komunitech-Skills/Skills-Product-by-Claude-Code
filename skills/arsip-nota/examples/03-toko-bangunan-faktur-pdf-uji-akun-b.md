# Contoh 3 (uji independen) — Toko bangunan, faktur PDF supplier

Diuji oleh penguji independen, 26 September 2026, di folder sementara terpisah dari sesi pembuat skill. Data fiktif.

## Skenario
"Arsipkan faktur semen dari CV Sumber Bangunan Jaya tanggal 12 September, Rp 12.500.000, sama invoice cat dari Toko Cat Warna Indah tanggal sama, 3 juta, kategori peralatan."

File sumber: `Faktur-Supplier-Semen-Sept.pdf`, `INV-2026-0912.pdf` (nama file asli tidak dipakai untuk arsip — dibentuk ulang dari data).

## Perintah & hasil (JSON asli dari run)
```bash
python3 scripts/arsip.py tambah --file "Faktur-Supplier-Semen-Sept.pdf" --tanggal 12/09/2026 \
  --vendor "CV Sumber Bangunan Jaya" --nominal "12.500.000" --jenis faktur --ya --json
```
```json
{
  "ok": true, "mode": "tersimpan", "id": 1,
  "nominal": 12500000, "kategori": "lain-lain", "jenis_dokumen": "faktur",
  "file_tujuan": ".../arsip/2026/09/2026-09-12_CV-Sumber-Bangunan-Jaya_12500000.pdf",
  "asumsi": ["Kategori tidak disebut, dipakai 'Lain-lain'."]
}
```
```bash
python3 scripts/arsip.py tambah --file "INV-2026-0912.pdf" --tanggal 12/09/2026 \
  --vendor "Toko Cat Warna Indah" --nominal "3jt" --jenis invoice --kategori peralatan --ya --json
```
```json
{"ok": true, "mode": "tersimpan", "id": 2, "nominal": 3000000, "kategori": "peralatan"}
```

Rekap bulan 09/2026: `total_nominal: 15500000`, `jumlah_nota: 2`.
**Verifikasi independen:** 12.500.000 + 3.000.000 = 15.500.000 — cocok.

## Temuan
- Nominal format Indonesia dengan titik ribuan ("12.500.000") dan singkatan ("3jt") pada dokumen bernilai besar (PDF faktur toko bangunan) diparser tepat, sesuai standar pembulatan CLAUDE.md (di sini tidak ada pecahan, tidak ada pembulatan).
- Vendor "CV Sumber Bangunan Jaya" tidak tertangkap kata kunci kategori manapun (termasuk `bahan-baku`) → jatuh ke "Lain-lain". Ini **bukan bug**, tapi kesenjangan kamus kata kunci: usaha toko bangunan (semen, cat, bata, paku) tidak terwakili di `KATEGORI` (kata kunci saat ini condong ke usaha kuliner/sembako). Dicatat sebagai temuan sedang di `HASIL-UJI.md`.
- Ekstensi `.pdf` diarsipkan dengan benar (termasuk daftar `EKSTENSI_DIKENAL`), tanpa peringatan.
