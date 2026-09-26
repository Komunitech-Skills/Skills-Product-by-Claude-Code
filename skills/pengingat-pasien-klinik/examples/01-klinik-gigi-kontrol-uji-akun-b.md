# Uji independen Akun B — Skenario 1 (normal): klinik gigi, kontrol behel

Hari acuan: 26 September 2026 (Sabtu). Dijalankan di scratchpad terpisah, database CSV fiktif.

## Perintah
```
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 --json tambah \
  --nama "Bu Sari" --wa "0812-0000-1111" --jenis "kontrol gigi" --tanggal "10 hari lagi" --persetujuan ya
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 --json daftar --kapan h-3
```

## Keluaran nyata
```
{"ok": true, "mode": "tersimpan", "id": "1", "teks": "Tersimpan #1: Bu Sari | Kontrol gigi | 6 Okt 2026 | persetujuan: ya", "peringatan": []}
{"ok": true, "mode": "baca", "kelompok": {"terlambat": 0, "hari_ini": 0, "h1": 0, "h3": 0}, "teks": "Tidak ada jadwal pada kategori ini."}
```
Catatan: pada 26 Sep, H-3 dari 6 Okt belum jatuh (H-3 = 3 Okt). Ini **benar** — dibuktikan lagi
di skenario 3 dengan kombinasi tanggal yang memang jatuh di kategori aktif.

## Verifikasi independen (Python `datetime`, bukan dari skill)
```python
from datetime import date, timedelta
acuan = date(2026, 9, 26)
target = acuan + timedelta(days=10)      # 2026-10-06 -> cocok dengan "6 Okt 2026"
h3 = target - timedelta(days=3)          # 2026-10-03 -> H-3 belum jatuh pada 26 Sep
```
Hasil manual **cocok persis** dengan keluaran script.

## Hasil
LULUS. Nama, WA, jenis kunjungan (bukan diagnosis — "kontrol gigi" adalah jenis kunjungan umum),
dan tanggal tersimpan benar. Tidak ada kolom diagnosis di CSV (diperiksa header:
`id,nama_panggilan,wa,jenis,tanggal,status,persetujuan,dibuat,diingatkan_pada,catatan`).
