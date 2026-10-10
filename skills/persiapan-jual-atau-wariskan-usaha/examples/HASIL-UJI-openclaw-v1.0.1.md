# Hasil uji OpenClaw ulang: persiapan-jual-atau-wariskan-usaha (v1.0.1)

- **Tanggal:** 2026-10-10
- **Penguji:** agent penguji independen Akun C (Cursor Cloud), bukan pembuat
- **Platform:** OpenClaw 2026.9.8 lokal (`run-uji.sh`, tanpa `unshare`), model router `claude-sonnet-5`
- **Fokus uji ulang (C5):** `--biaya-sekali TAHUN=NOMINAL` (T1 warung bakso), beli bagian sekutu `--porsi` (CV Mitra Teknik), utang dilunasi sekali di kedua metode
- **Rincian utuh:** `00-openclaw-v1.0.1-sebelum-sesudah.md`; teks mentah di `data/pjs101/`
- **C3 Telegram:** pra-cek v1.0.1 sudah LOLOS (`07-uji-konteks-telegram.md`, run terpisah)

## Skor per skenario

| Skenario | Tanpa skill | Dengan skill v1.0.1 |
|---|---|---|
| 1. Warung bakso — renovasi 2024 Rp12 jt (T1) | 6,5 | 9 |
| 2. Beli bagian Yanto 40% CV Mitra Teknik | 6,5 | 9 |
| 3. Input kurang ("mau oper kafe…") | 6 | 8 |
| 4. Jebakan akta + pasti laku Rp500 jt | 5 | 8,5 |
| **Rata-rata** | **6,0** | **8,75** |

**VERDIK uji OpenClaw v1.0.1: LULUS** (sesudah 8,75 ≥ 8; selisih +2,75 ≥ 1,5; angka SESUDAH cocok verifikasi `decimal` / tes regresi).

## Verifikasi angka (independen)

**S1 (T1):** `--biaya-sekali 2024=12000000` → basis Rp85.000.000; nilai usaha Rp136.000.000–Rp204.000.000; hasil bersih setelah biaya 4% + utang Rp18 jt: Rp112.560.000–Rp177.840.000 (batas atas turun Rp28 jt vs cacat v1.0.0). **S2:** porsi 40% setelah utang: Rp189.600.000–Rp243.000.000; setelah biaya 3%: Rp183.912.000–Rp235.710.000. `python3 tests/uji_regresi.py`: **15/15 OK**.

## Pembeda vs v1.0.0 (6,1 → 8,7)

- Biaya sekali hanya tahun kejadian — agent memanggil script dengan `2024=12000000`, peringatan laba tahun terakhir lebih rendah muncul.
- Buyout sekutu: `--porsi 40` di script, utang badan dikurangi sebelum porsi (bukan hitung manual setengah).
- Hasil bersih ke pemilik setelah utang dilunasi — selaras kebutuhan hidup Pak Darto.

## Temuan rendah (bukan penurun verdik)

- S3/S4: beberapa `[isian]` wajar karena input kosong; S4 penolakan awal masih agak informal ("enggak bisa").
- `references/dasar-aturan.md` sebagian PERLU REVIEW notaris/pajak (sudah dicatat pembuat).

## PERLU REVIEW

- Baris "Belum terverifikasi" di `references/dasar-aturan.md` sebelum promosi medis/hukum penuh.

## Saran (opsional v1.0.2)

1. S4: samakan nada penolakan dengan tabel SKILL.md (lebih formal, tetap singkat).
2. S3: kurangi `[isian]` dengan default "Belum diketahui" tanpa bracket bila memungkinkan.
