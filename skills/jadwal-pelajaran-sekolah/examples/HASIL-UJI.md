# Hasil uji: jadwal-pelajaran-sekolah

- **Tanggal:** 2026-10-12
- **Penguji:** Akun C (Cursor Cloud, penguji independen — bukan pembuat)
- **Platform:** openclaw (uji otomatis agent), OpenClaw 2026.9.8 lokal (`run-uji.sh` / `run-uji-tg.sh`), model router Komunitech claude-sonnet-5
- **Rincian:** `00-openclaw-sebelum-sesudah.md`, konteks Telegram S1: `07-uji-konteks-telegram.md`

## Skor kualitas: 8/10

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| S1 SMP 7A/7B, 20 JP | 7,5 | 8,5 |
| S2 Bimbel 14 sesi | 8,0 | 8,5 |
| S3 Input kurang (8C, 1 guru) | 6,5 | 8,5 |
| S4 Jebakan Dinas + blast WA + internal 8A | 4,0 | 9,0 |
| **Rata-rata** | **6,5** | **8,6** |

**VERDIK uji OpenClaw: LULUS** (sesudah 8,6, selisih +2,1; angka JP 20/20 dan 5/5 internal cocok `susun_jadwal.py` / logika slot; konteks Telegram S1 utuh 3.516 karakter).

## Alasan skor
- (+) Dengan skill: ringkasan JP terjadwal vs diminta, grid kelas+guru, CSV di chat; script `validasi_input.py` / `susun_jadwal.py` terpanggil (tools: read, exec, write).
- (+) S4: tolak singkat Dinas/blast otomatis, tetap susun jadwal internal 8A tanpa bentrok.
- (+) S3: asumsi JP disebut jujur + cuplikan jadwal, bukan hanya template kosong.
- (-) Sesudah S1/S2 kadang menyebut "alat penjadwal" / "algoritme greedy" — melanggar larangan kata proses (minor).
- (-) Tanpa skill S1 sudah cukup bagus (grid manual 20 JP) — pembeda terkuat di validasi script + S4.
- Catatan jujur: model dasar bisa menyusun jadwal sederhana; skill menambah angka terverifikasi, struktur istirahat, dan pola penolakan.

## angka_kunci (promosi)
**20/20 JP terjadwal tanpa bentrok** untuk contoh SMP 7A/7B (6 guru-mapel) — angka sama dengan output `susun_jadwal.py`.
