# Uji konteks Telegram — skenario 1 (warung Bu Sri)

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (independen)
- **Skill:** persiapan-jual-atau-wariskan-usaha **v1.0.1**
- **Cara:** `mk-home.sh` + `run-uji-tg.sh` (OpenClaw 2026.9.8, `--channel telegram` tanpa `--deliver`; VM Cursor tanpa `unshare`)
- **Pesan uji:** sama dengan skenario 01 di `00-openclaw-sebelum-sesudah.md` (warung Dapur Bu Sri, pensiun, laba 2023–2025, KUR, kelipatan 2–3x, dll.)

## Hasil

| Sisi | Karakter | Skill/script terpakai? | Utuh di chat? |
|---|---|---|---|
| SEBELUM (tanpa skill) | 3.095 | tidak | ya — jawaban ringkas rule-of-thumb |
| SESUDAH (dengan skill) | 10.254 | ya (`read`, `exec` → `nilai_usaha.py`) | **ya** — struktur 8 bagian lengkap, tanpa tawaran "kirim file" |

## Verifikasi singkat (SESUDAH, TG)

- Rentang nilai usaha Rp176.800.000–Rp265.200.000; hasil bersih setelah KUR Rp122.960.000–Rp206.940.000 — selaras dengan uji lokal v1.0.0/1.0.1.
- Daftar periksa, rencana transisi, pertanyaan notaris/pajak ada; penutup maks 3 pertanyaan lanjutan.
- Tidak ada pemotongan mid-message yang terlihat; tidak beralih ke lampiran file.

## Verdik pra-cek Telegram

**LOLOS** — jawaban panjang skenario 1 aman untuk calon gelombang tampilan; tidak perlu revisi khusus kanal Telegram (cacat "mungkin perlu ringkasan" di HASIL-UJI v1.0.0 **ditutup**).

## Output mentah

- `examples/data/pjs-tg-b1-01-sebelum.txt`
- `examples/data/pjs-tg-s1-01-sesudah.txt`
