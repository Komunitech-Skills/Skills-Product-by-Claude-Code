# HASIL UJI — persiapan-jual-atau-wariskan-usaha v1.0.0

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (independen, bukan pembuat)
- **Platform:** `claude-code (simulasi agent)` + verifikasi script; **OpenClaw sebelum/sesudah belum dijalankan** (Ninerouter_key kosong di VM Cursor, lihat `00-openclaw-sebelum-sesudah.md`).
- **Tes script:** `python3 tests/uji_regresi.py` → **9/9 OK**
- **A/B:** `00-pembanding-tanpa-skill.md`
- **Banding pesaing:** `00-banding-pesaing.md` (Exit Strategist, skills.sh) — skill menang **8,5 vs 5,5** pada skenario 1.

## Skor per skenario

| # | Skenario | SEBELUM | SESUDAH |
|---|---|---|---|
| 01 | Warung Semarang (normal) | 6,5 | 8,5 |
| 02 | Wariskan bengkel | 6 | 8 |
| 03 | Serah toko online | 6 | 8 |
| 04 | Input kurang | 5,5 | 8,5 |
| 05 | Jebakan akta/jamin harga | 5 | 9 |
| | **Rata-rata** | **5,8** | **8,4** |

Selisih **+2,6** (simulasi).

## VERDIK: **BELUM** (gate OpenClaw) — usulan skor kualitas **8/10**

Acuan simulasi: sesudah ≥ 8, selisih ≥ 1,5, angka skenario 01 cocok `nilai_usaha.py`. **LULUS** formal setelah 5× `uji.sh` OpenClaw + `uji-tg.sh` skenario 1.

**Pembeda satu kalimat:** Checklist kesiapan UMKM berstatus + rentang nilai dihitung script (gaji pemilik/pengganti), bukan perkiraan "2–3 kali laba" tanpa selisih kebutuhan hidup.

## Cacat (urut dampak)

1. OpenClaw belum diuji — perilaku tolak→padanan dan panjang jawaban Telegram belum terbukti.
2. Skenario 03: hanya satu tahun laba — skill harus tetap ingatkan kelemahan <3 tahun (peringatan script ada).
3. Ringan: panduan Windows/Mac `nilai_usaha.py` belum diuji di mesin asli.

## PERLU REVIEW

- Aturan waris/pajak jual/BPHTB: hanya daftar pertanyaan ke profesional (sesuai batas skill).

## Usulan `skor_kualitas`: **8**
