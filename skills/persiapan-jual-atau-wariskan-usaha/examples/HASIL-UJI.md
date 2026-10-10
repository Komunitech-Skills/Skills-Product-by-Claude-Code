# HASIL UJI — persiapan-jual-atau-wariskan-usaha 1.0.0

- Tanggal: 2026-10-10
- Penguji: Akun C (independen, bukan pembuat)
- Platform: `openclaw (uji otomatis agent)` — OpenClaw 2026.9.8, model router `claude-sonnet-5`
- Tes script: `python3 tests/uji_regresi.py` → 9 tes OK
- Verifikasi angka: Python independen — Bu Sri & jual 30% saham cocok script

## Skor per skenario (OpenClaw)
| # | Skenario | SEBELUM | SESUDAH |
|---|---|---|---|
| 01 | Warung Bu Sri (normal + A/B) | 6,5 | 9 |
| 02 | Wariskan bengkel cat | 7 | 8,5 |
| 03 | Jual laundry, input kurang | 5,5 | 8,5 |
| 04 | Jebakan akta + pasti laku 500 jt | 5 | 8,5 |
| 05 | Jual 30% saham bengkel las | 6,5 | 9 |
| | **Rata-rata** | **6,1** | **8,7** |

Selisih +2,6. Banding pesaing: tidak ada skill publik setara; prompt generik ≈5,5 vs skill 9 pada skenario 1 (`00-banding-pesaing.md`).

## VERDIK: **LULUS** — skor kualitas **9/10**

## Pembeda (satu kalimat)
Tanpa skill laba warung Bu Sri dihitung mentah (±Rp187–281 jt bersih); dengan skill penyesuaian gaji manajer + potongan ketergantungan → **Rp96,9–251,9 jt** dan terlihat kebutuhan pensiun Rp192 jt bisa kurang **Rp95,1 jt** di harga rendah.

## Cacat per keparahan
**Sedang**
- S1: output sangat panjang (~9,5 rb karakter) — di Telegram mungkin perlu ringkasan dulu (uji konteks Telegram belum dijalankan).

**Ringan**
- S2: gaji pemilik "dicampur" belum dihitung ulang ke angka pasti (skill minta data di akhir).
- S4: sebelum skill menolak akta tapi hampir tidak menyiapkan checklist.

## Alasan (+/−)
+ Struktur output 8 bagian konsisten; script `nilai_usaha.py` dipakai; tolak→padanan→tetap kerjakan (S4).
+ Daftar periksa berstatus, rencana transisi per bulan, pertanyaan notaris/pajak.
+ Tidak menjanjikan harga/laku; kelipatan selalu asumsi pengguna.
− Panjang jawaban skenario 1; wariskan (S2) belum hitung nilai (laba ada tapi kelipatan tidak diberikan — sesuai aturan).

## Catatan jujur
Satu model/router untuk kedua sisi; selisih nyata terutama dari struktur + hitungan script.

## PERLU REVIEW
- Aturan waris/pajak/BPHTB/NIB pengalihan: arahkan ke notaris/konsultan pajak (sudah di skill); tidak diverifikasi ke naskah resmi di sesi ini.

## Usulan skor_kualitas catalog
**9**
