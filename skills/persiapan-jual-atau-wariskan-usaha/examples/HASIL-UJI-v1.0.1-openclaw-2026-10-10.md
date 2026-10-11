# HASIL UJI — persiapan-jual-atau-wariskan-usaha **1.0.1** (OpenClaw, fokus perbaikan)

- Tanggal: 2026-10-10
- Penguji: Akun C (independen)
- Platform: `openclaw (uji otomatis agent)` — OpenClaw 2026.9.8, router `claude-sonnet-5`
- Cakupan: 6 skenario OpenClaw v1.0.1 (A–B `00-openclaw-v1.0.1-sebelum-sesudah.md`; C–D `08-openclaw-v1.0.1-skenario-2-3.md`; E–F `09-openclaw-v1.0.1-skenario-4-5.md`).
- Tes script: 15/15 OK (`tests/uji_regresi.py`)
- Detail transkrip: `00-openclaw-v1.0.1-sebelum-sesudah.md`

## Skor per skenario (OpenClaw)

| # | Skenario | SEBELUM | SESUDAH |
|---|---|---|---|
| A | Warung bakso, renovasi 2024 (T1) | 6,5 | 9,0 |
| B | Beli bagian sekutu 40% (S4) | 5,5 | 9,0 |
| C | Wariskan bengkel cat | 6,5 | 9,0 |
| D | Laundry tanpa angka | 5,5 | 8,5 |
| E | Jebakan akta + pasti laku 500 jt | 5,0 | 8,5 |
| F | Jual 30% saham bengkel las | 6,5 | 9,0 |
| | **Rata-rata (6 skenario v1.0.1)** | **5,92** | **8,83** |

Selisih rata-rata +2,92. Uji penuh v1.0.0 tetap di `HASIL-UJI.md` (LULUS 6,1→8,7).

## VERDIK (perbaikan v1.0.1): **LULUS**

Skor kualitas usulan untuk revisi: **9/10** (cacat T1 & S4 dari uji isi agent 2026-10-09 teratasi pada skenario fokus).

## Pembeda (satu kalimat)

Renovasi Rp12 jt hanya menaikkan laba 2024 → batas atas warung turun **Rp28 jt**; buyout sekutu kini pakai **porsi 40%** dan utang badan usaha sebelum bagi hasil (Rp183,9–235,7 jt ke Yanto).

## Cacat tersisa (ringan)

- S1 subset masih output panjang (~10 rb karakter); pra-cek Telegram v1.0.1 sudah OK di run terpisah (C3, branch `cursor/uji-persiapan-jual-tg-8b42`).
- `references/dasar-aturan.md` sebagian PERLU REVIEW (situs instansi).

## PERLU REVIEW

- Aturan waris/pajak: arahkan ke notaris/konsultan pajak (tidak diverifikasi ke naskah resmi di sesi ini).
