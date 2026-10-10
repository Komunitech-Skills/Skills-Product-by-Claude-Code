# Hasil uji OpenClaw: persiapan-jual-atau-wariskan-usaha v1.0.1

- **Tanggal:** 2026-10-10
- **Penguji:** Akun C (agent independen, bukan pembuat revisi 1.0.1)
- **Platform:** openclaw (uji otomatis agent), OpenClaw 2026.9.8, model router claude-sonnet-5
- **Rincian:** `00-openclaw-sebelum-sesudah-v1.0.1-2026-10-10.md`
- **Fokus revisi:** `--biaya-sekali TAHUN=NOMINAL`, utang sekali di kedua metode, `--porsi` beli-keluar mitra

## Skor per skenario

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1. Warung bakso, renovasi 2024 Rp12 jt (biaya-sekali per tahun) | 6,5 | 9,0 |
| 2. CV Mitra Teknik, beli 40% bagian Yanto | 6,0 | 9,0 |
| 3. Laundry Surabaya tanpa angka | 5,0 | 8,0 |
| 4. Jebakan akta + pasti laku Rp500 jt | 5,5 | 8,5 |
| **Rata-rata** | **6,0** | **8,6** |

**VERDIK uji OpenClaw: LULUS** (sesudah 8,6 ≥ 8; selisih +2,6 ≥ 1,5; angka S1–S2 diverifikasi independen, cocok).

## Konteks Telegram (skenario 1 SESUDAH)

- `run-uji-tg.sh`: **9539** karakter, jawaban utuh di chat (tidak terpotong / tidak dialih ke file).
- Tool: read, ls, exec (script nilai_usaha).

## Pembeda terkuat (promosi)

Revisi **biaya sekali per tahun** memperbaiki over-valuasi Rp28 jt pada kasus warung bakso, sambil tetap memberi checklist 8 bagian + hitung script + langkah beli-keluar mitra dengan porsi eksplisit.

## PERLU REVIEW

- Aturan waris/pajak/NIB di `references/dasar-aturan.md` belum dicek ke naskah resmi (catatan pembuat v1.0.1).

## Catatan jujur

- S3 SESUDAH tidak memanggil script (wajar, data kosong); tetap memberi kerangka + asumsi berlabel.
- S4 masih memakai placeholder `[isian]` karena jenis toko tidak disebut — sesuai skill.
