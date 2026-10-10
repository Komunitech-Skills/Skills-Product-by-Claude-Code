# Pra-cek konteks Telegram — skenario 01 (Bu Sri) — v1.0.1

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (independen)
- **Alat:** `run-uji-tg.sh` (VM Cursor, tanpa `unshare`); OpenClaw 2026.9.8; `--channel telegram` tanpa `--deliver`
- **HOME:** `pjw-tg-s1` (hanya skill `persiapan-jual-atau-wariskan-usaha` v1.0.1 dari repo)

## Pesan uji

Sama dengan skenario 01 di `00-openclaw-sebelum-sesudah.md` (warung Dapur Bu Sri, Semarang).

## Hasil

| Metrik | Nilai |
|---|---|
| Karakter jawaban | **8074** (~8158 byte) |
| Alat terpanggil | `read`, `ls`, `exec` (script nilai usaha) |
| Utuh di chat | **Ya** — 8 bagian (ringkasan, daftar periksa, rentang nilai, struktur, transisi 12 bln, dokumen, pertanyaan notaris/pajak, penutup + 3 tanya) |
| Terpotong / hanya tautan file | **Tidak** |
| Angka kunci | Nilai usaha Rp176.800.000–265.200.000; hasil bersih Rp122.960.000–206.940.000; kebutuhan 2 thn Rp192.000.000 |

## Verdik pra-cek

**LULUS** untuk tampilan Telegram / gelombang pilot — jawaban panjang tetap utuh di kanal chat; tidak perlu revisi skill khusus potongan Telegram untuk S1.

## Catatan

- Regresi script: `python3 tests/uji_regresi.py` → 15 OK (2026-10-10).
- Uji ulang penuh v1.0.1 (biaya sekali, beli-keluar mitra) = tugas **C5** terpisah.
