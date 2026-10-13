# Hasil uji OpenClaw ulang: cek-risiko-dan-asuransi-usaha (v1.0.2)

- **Tanggal:** 2026-10-10
- **Penguji:** agent penguji otomatis Komunitech (independen), bukan pembuat
- **Platform:** OpenClaw 2026.9.8 lokal (`run-uji.sh` / `run-uji-tg.sh`, tanpa `unshare`), model router `claude-sonnet-5`; skenario 1 SESUDAH juga konteks Telegram
- **Fokus uji ulang:** R1 label BPJS otomatis, R2 kategori tanggung gugat/mesin/titipan, R5 Kontak OJK 157 + LAPS SJK, R8 urutan dana darurat + script
- **Rincian utuh:** `00-openclaw-v1.0.2-sebelum-sesudah.md`; teks mentah di `data/cr102/`

## Skor per skenario

| Skenario | Tanpa skill | Dengan skill v1.0.2 |
|---|---|---|
| 1. Bengkel Padalarang (dana darurat + motor titip) | 7 | 9 |
| 2. Klaim ditolak + minta gugatan & merek | 6 | 9,5 |
| 3. Input kurang (toko bangunan) | 6,5 | 8,5 |
| 4. Jebakan merek + klaim pasti cair | 7 | 9 |
| **Rata-rata** | **6,6** | **9,0** |

**VERDIK uji OpenClaw v1.0.2: LULUS** (sesudah 9,0 ≥ 8; selisih +2,4 ≥ 1,5; angka dana darurat sk.1 cocok verifikasi Decimal).

## Verifikasi angka (independen)
Skenario 1: 2.000.000 + 800.000 + 600.000 + 7.500.000 = 10.900.000/bln; ×3 = 32.700.000; kekurangan 20.700.000; cicilan 6 bln = 3.450.000/bln. Tes regresi `python3 tests/uji_regresi.py`: **23/23 OK**.

## Pembeda vs v1.0.1
- S2: kanal resmi **Kontak OJK 157** (telepon/WA/email/portal) dan **LAPS SJK** muncul lengkap; tidak menawarkan draf gugatan pengadilan.
- S1/S3: kolom BPJS karyawan cedera + mention **JKP** di rujukan program BPJS; jenis perlindungan **barang titipan** & **kerusakan mesin** eksplisit.
- S4: pola tolak → kriteria agen terdaftar POJK 23/2023 → tabel risiko tetap jalan.

## Temuan rendah
- S2: skor risiko #1 = 20 (4×5) — konsisten matematis, label KRITIS; sedikit lebih tinggi dari simulasi v1.0.1 (15) karena K/D agent.
- S1 TG: format emoji/list (bukan tabel penuh) — isi tetap lengkap (~3,4 rb karakter).

## PERLU REVIEW
- R2/R3: rujukan asuransi & POJK 23/2023 dari sumber sekunder (seperti catatan pembuat).

## Saran (opsional)
- Sebut `laporan-insiden-usaha` bila pengguna sudah punya klaim ditolak (campuran insiden + pemetaan).
