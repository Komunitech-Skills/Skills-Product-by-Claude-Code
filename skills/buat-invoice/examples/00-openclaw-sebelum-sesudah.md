# Uji OpenClaw SEBELUM vs SESUDAH: buat-invoice

**Sumber (ada di paket VIP):** `solusi-vip/konsultan/UJI-OPENCLAW.md` (tabel skor skenario 01, bagian "Cacat per skill", "Uji ulang 2026-10-01 (keuangan)" dan "putaran 2") dengan rincian per skenario di `solusi-vip/konsultan/uji-openclaw/01-invoice-ppn-pph23.md`, `01-invoice-ppn-pph23-ulang.md`, dan `01-invoice-ppn-pph23-ulang2.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.2 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang 1 = 1.0.3, uji ulang 2 = 1.0.4. Versi di katalog saat ini: 1.0.4.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); tiap uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Konsultan (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill solusi konsultan (25 skill, termasuk `buat-invoice`). Pesan member identik di kedua sisi; data fiktif.
- Uji ulang hanya mengulang sisi SESUDAH dengan pesan yang sama; skor SEBELUM dipakai ulang dari uji pertama.
- Angka dihitung ulang penguji dengan Python (PPN 12% × DPP nilai lain 11/12 sesuai PMK 131/2024, dibulatkan ke bawah; PPh 23 2% dari bruto).

**Pesan member (skenario 01):** "Halo, tolong bikinin invoice buat PT Sinar Abadi Logistik ya. Jasa konsultasi pajak bulan September Rp 8.750.000, sama pendampingan pemeriksaan pajak 2 hari @ Rp 2.375.000. Saya sudah PKP (CV Arta Konsulindo). Mereka biasanya potong PPh 23. Jatuh tempo 14 hari. Rekening BCA 1234567890 a.n. CV Arta Konsulindo."

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 01 Invoice jasa konsultan PKP + PPN + PPh 23, uji pertama | ±1.0.2 | 7 | 8 | Dengan skill: PPN 12% × DPP nilai lain 11/12, terbilang, HTML siap cetak, catatan faktur pajak/meterai, tetapi PPh 23 (Rp270.000) dan neto (Rp14.715.000) tidak dihitung; tanpa skill menghitungnya tetapi memakai label "PPN 11%" dan menjalankan `find /` ke seluruh disk. |
| 01, uji ulang 1 (hanya sisi SESUDAH) | 1.0.3 | 7 (dari uji pertama) | 8 | PPh 23 dan neto kini dihitung script dan invoice utuh tampil di chat, tetapi agent bertanya dulu "PPN 11%" padahal data lengkap (satu giliran tambahan). |
| 01, uji ulang 2 (hanya sisi SESUDAH) | 1.0.4 | 7 (dari uji pertama) | 9 | Invoice langsung jadi di giliran 1 dengan PPN 12% × DPP nilai lain 11/12 dan asumsi disebut, plus PPh 23 Rp270.000 dan estimasi diterima bersih Rp14.715.000 dari script. |
| **Rata-rata skenario ini** (skenario tunggal) | | **7** | **8** (uji pertama) → **9** (1.0.4) | Selisih +1 pada uji pertama, +2 pada uji ulang terakhir. |

Rata-rata seluruh solusi konsultan (5 skenario, skill berbeda) di uji pertama: 6,8 → 7,8. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS pada uji ulang 2 (skor 9, 1.0.4).** Pada uji pertama keunggulan skill tipis (8 vs 7).

Angka invoice benar semua pada uji ulang 2: subtotal Rp13.500.000, DPP nilai lain Rp12.375.000, PPN Rp1.485.000, total Rp14.985.000, PPh 23 Rp270.000, diterima bersih Rp14.715.000, jatuh tempo 15 Okt 2026.

## Catatan jujur
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Pada uji pertama, model tanpa skill justru lebih baik menjawab inti pertanyaan (PPh 23 dan neto); skill versi awal tidak menangani PPh 23. Celah ini ditutup di versi berikutnya.
- Lampiran file HTML ke chat Telegram tidak dapat dinilai di mode lokal (tanpa kanal); sumber hanya mencatat path file disebut.
- Pada uji ulang, argumen tool call tidak dapat diaudit (hanya nama tool), jadi pencarian `find /` tidak bisa dipastikan hilang.
- Satu skenario saja; belum menguji invoice non-PKP, termin, atau PPh 23 tanpa NPWP (4%) di OpenClaw.

## Cuplikan dari sumber (sebelum/sesudah)
- Tanpa skill: "PPN 11%".
- Dengan skill: "DPP nilai lain (11/12): Rp 12.375.000 · PPN 12%: Rp 1.485.000 … Invoice ini bukan faktur pajak, faktur pajak keluaran tetap dibuat di Coretax."
