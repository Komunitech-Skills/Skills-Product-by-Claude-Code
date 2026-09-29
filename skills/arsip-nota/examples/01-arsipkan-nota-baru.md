# Contoh 1 - Mengarsipkan nota baru (dua file sekaligus)

Data nyata dari hasil `scripts/arsip.py` (dijalankan di folder sementara, 26 September 2026).

## Percakapan

**Pengguna:** "Arsipkan dua nota ini: IMG_20260920_1.jpg dari Toko Sembako Bu Yati tanggal 20 September, 150 ribu.
Terus WhatsApp-Image-2026-09-22.jpeg dari Toko C Elektronik tanggal 22 September, 50 ribu, buat beli kabel."

**Agent:** (belum ada indeks arsip di komputer ini)

```bash
python3 scripts/arsip.py init --ya --json
```
```json
{"ok": true, "mode": "tersimpan", "db": ".../data/arsip.db", "folder_arsip": ".../data/arsip"}
```

Lanjut, pratinjau nota pertama:
```bash
python3 scripts/arsip.py tambah --file "in/IMG_20260920_1.jpg" --tanggal 20/09/2026 \
  --vendor "Toko Sembako Bu Yati" --nominal 150000 --json
```
```json
{
  "ok": true,
  "mode": "pratinjau",
  "perlu_konfirmasi": true,
  "tanggal": "2026-09-20",
  "vendor": "Toko Sembako Bu Yati",
  "nominal": 150000,
  "kategori": "bahan-baku",
  "jenis_dokumen": "nota",
  "file_sumber": "in/IMG_20260920_1.jpg",
  "file_tujuan": "data/arsip/2026/09/2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg",
  "aksi": "disalin",
  "hash_sha256": "08bed2ae3b52fc9fa213bfb69c23751941bb298a2e886057f9215aaba44f70f3",
  "peringatan": [],
  "asumsi": ["Kategori 'Bahan baku' ditebak dari nama vendor/catatan."]
}
```

**Agent ke pengguna:**
> Saya akan arsipkan (belum disimpan, file asli belum disalin):
> 1. IMG_20260920_1.jpg → `2026/09/2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg` — 20/09/2026, Rp 150.000, kategori Bahan baku (ditebak dari nama vendor)
> 2. WhatsApp-Image-2026-09-22.jpeg → `2026/09/2026-09-22_Toko-C-Elektronik_50000.jpeg` — 22/09/2026, Rp 50.000, kategori Peralatan (ditebak dari nama vendor), catatan "beli kabel"
>
> File asli tetap ada di tempatnya (mode salin). Simpan? Balas "ya".

**Pengguna:** "ya"

```bash
python3 scripts/arsip.py tambah --file "in/IMG_20260920_1.jpg" --tanggal 20/09/2026 \
  --vendor "Toko Sembako Bu Yati" --nominal 150000 --ya --json
python3 scripts/arsip.py tambah --file "in/WhatsApp-Image-2026-09-22.jpeg" --tanggal 22/09/2026 \
  --vendor "Toko C Elektronik" --nominal 50rb --catatan "beli kabel" --ya --json
```
```json
{
  "ok": true, "mode": "tersimpan", "id": 1, "tanggal": "2026-09-20", "vendor": "Toko Sembako Bu Yati",
  "nominal": 150000, "kategori": "bahan-baku", "jenis_dokumen": "nota",
  "file_tujuan": "data/arsip/2026/09/2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg", "aksi": "disalin",
  "hash_sha256": "08bed2ae3b52fc9fa213bfb69c23751941bb298a2e886057f9215aaba44f70f3", "peringatan": [], "asumsi": [...],
  "backup": "data/backup-arsip/arsip-20260926-154034-harian.db"
}
```

**Agent:**
> Sudah tersimpan, 2 nota. File asli masih ada di folder aslinya (disalin, bukan dipindah). Cadangan indeks
> otomatis dibuat: `backup-arsip/arsip-20260926-154034-harian.db`.

## Catatan
- Nominal `50rb` diproses lewat parser satuan (`SATUAN_NOMINAL`), menjadi Rp 50.000.
- Kategori ditebak dari nama vendor ("Elektronik" → Peralatan); pengguna bisa mengoreksi dengan `--kategori` pada
  perintah ulang bila tidak sesuai (catatan lama tidak dihapus, cukup arsipkan ulang dengan kategori benar dan
  `--izinkan-duplikat` bila filenya sama).
