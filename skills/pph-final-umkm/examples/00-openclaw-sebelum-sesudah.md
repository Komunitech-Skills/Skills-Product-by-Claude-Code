# Uji OpenClaw SEBELUM vs SESUDAH: pph-final-umkm

**Sumber (ada di paket VIP):** `solusi-vip/usaha-offline/UJI-OPENCLAW.md` (tabel skor skenario 03, bagian "Cacat per skill" dan "Uji ulang 2026-10-01 (keuangan)") dengan rincian per skenario di `solusi-vip/usaha-offline/uji-openclaw/03-pph-final-umkm.md` dan `03-pph-final-umkm-ulang.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.2 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang = 1.0.3. Versi di katalog saat ini: 1.0.3.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Usaha Offline (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill usaha-offline (24 skill, termasuk `pph-final-umkm`). Pesan member identik; data fiktif.
- Uji ulang hanya mengulang sisi SESUDAH; skor SEBELUM dipakai ulang dari uji pertama.
- Angka dihitung ulang penguji dengan Python dan dicek terhadap PP 55/2022 dan PMK 81/2024.

**Pesan member (skenario 03):** "Saya punya warung makan, atas nama pribadi, NPWP dari 2021. Omzet 2026: Jan 48jt, Feb 45jt, Mar 52jt, Apr 70jt, Mei 55jt, Jun 50jt, Jul 53jt, Agu 58jt, Sep 61jt. Okt kira2 60jt. Pajak 0,5% nya tiap bulan berapa dan setornya kapan? Ada yg telat ga?"

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 03 PPh Final 0,5% orang pribadi, batas Rp500 juta, uji pertama | ±1.0.2 | 8 | 7 | Angka sama-sama benar (Jan-Sep Rp0; Okt (552-500) juta × 0,5% = Rp260.000), tetapi tanpa skill menyebut 15 Nov 2026 jatuh hari Minggu dan batas 7 tahun (s.d. 2027), sedangkan dengan skill (tabel ringkas, plus catatan bahwa batas Rp500 juta berlaku untuk gabungan semua usaha) melewatkan keduanya. |
| 03, uji ulang (hanya sisi SESUDAH) | 1.0.3 | 8 (dari uji pertama) | 9 | Keduanya kini muncul: "16 Nov 2026 (15 Nov jatuh Minggu, jadi mundur ke Senin)" dan tarif 0,5% berlaku s.d. 2027 menurut PP 55/2022, dengan catatan PP 20/2026 "belum saya verifikasi", ditambah tabel per bulan. |
| **Rata-rata skenario ini** (skenario tunggal) | | **8** | **7** (uji pertama) → **9** (1.0.3) | Selisih -1 pada uji pertama (tanpa skill menang), +1 pada uji ulang. |

Rata-rata seluruh solusi usaha-offline (5 skenario, skill berbeda) di uji pertama: 7,8 → 7,8. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS uji ulang (skor 9, 1.0.3).** Pada uji pertama, skenario ini dimenangkan sisi SEBELUM (8 vs 7).

## Catatan jujur
- Selisih akhir +1 poin; pembeda utama adalah tabel per bulan dengan tanggal setor yang digeser ke hari kerja (PMK 81/2024) dan sikap jujur soal batas 7 tahun yang mungkin berubah, bukan angka pajaknya (kedua sisi sama-sama benar).
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Klaim "PP 20/2026 mengubah batas" ditandai belum terverifikasi (butir PERLU REVIEW di catatan internal kurator, tidak disertakan dalam paket). Disclaimer "bukan nasihat pajak" tidak muncul eksplisit di balasan uji ulang (ada rujukan Kring Pajak 1500200).
- Argumen tool call tidak dapat diaudit pada uji ulang (hanya nama tool). Satu skenario saja (orang pribadi, NPWP 2021); badan usaha dan PP 20/2026 belum diuji di OpenClaw.
