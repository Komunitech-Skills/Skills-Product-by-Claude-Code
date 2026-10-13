# Uji OpenClaw SEBELUM vs SESUDAH: gaji-umkm

**Sumber (ada di paket VIP):** `solusi-vip/usaha-offline/UJI-OPENCLAW.md` (tabel skor skenario 02, bagian "Cacat per skill", "Cuplikan jualan" dan "Uji ulang 2026-10-01 (keuangan)") dengan rincian per skenario di `solusi-vip/usaha-offline/uji-openclaw/02-gaji-bpjs.md` dan `02-gaji-bpjs-ulang.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.5 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang = 1.0.6. Versi di katalog saat ini: 1.0.11.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Usaha Offline (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill usaha-offline (24 skill, termasuk `gaji-umkm`). Pesan identik. Agent SESUDAH bertanya balik sekali pada uji pertama; jawaban member ("Andi masuk 1 Maret 2022, Sari 1 Januari 2024. Belum pernah pakai, bikinin aja.") sama pada kedua putaran.
- Uji ulang hanya mengulang sisi SESUDAH; skor SEBELUM dipakai ulang dari uji pertama. Angka dihitung ulang penguji dengan Python (BPJS Kesehatan 4%/1%, JHT 3,7%/2%, JKK 0,24%, JKM 0,3%, JP 2%/1%, lembur PP 35/2021, PPh 21 TER PMK 168/2023).

**Pesan member (skenario 02):** "Tolong hitungin gaji september 2 karyawan warung makan saya di Solo. Andi: gapok 2,8jt + uang makan tetap 300rb, status nikah anak 1, lembur 3 hari masing2 2 jam (hari kerja biasa). Sari: gapok 2,65jt, belum nikah, ga lembur. Dua2nya ikut BPJS Kesehatan & BPJS TK (JHT, JKK, JKM, JP). Yg ditransfer ke masing2 berapa, saya nyetor BPJS berapa total, PPh 21 nya ada ga?"

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 02 Gaji September + BPJS + PPh 21, 2 karyawan warung, uji pertama | ±1.0.5 | 8 | 8 | Angka kedua sisi sama persis dan benar (transfer Andi Rp3.164.150, Sari Rp2.544.000, setor BPJS Rp818.800, PPh 21 Rp0); dengan skill data tersimpan di database lokal dengan tawaran slip dan CSV transfer, serta jujur bahwa UMK belum dicek, tetapi butuh satu giliran tambahan (menanyakan tanggal masuk) sedangkan tanpa skill langsung tuntas dan menulis "di atas UMK Solo" tanpa angka. |
| 02, uji ulang (hanya sisi SESUDAH) | 1.0.6 | 8 (dari uji pertama) | 9 | Angka lengkap keluar di giliran 1 dengan asumsi tanggal masuk disebut, UMK/JKK/tanggal masuk dalam satu pesan, database dibuat hanya setelah member setuju. |
| **Rata-rata skenario ini** (skenario tunggal) | | **8** | **8** (uji pertama, seri) → **9** (1.0.6) | Selisih 0 pada uji pertama, +1 pada uji ulang. |

Rata-rata seluruh solusi usaha-offline (5 skenario, skill berbeda) di uji pertama: 7,8 → 7,8. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS uji ulang (skor 9, 1.0.6).** Pada uji pertama hasilnya seri (8 vs 8).

## Catatan jujur
- Angka sama-sama benar di kedua sisi, jadi pembeda bukan ketepatan satu jawaban. Sumber menilai keunggulan ada pada hal yang tidak terlihat dalam satu jawaban: data tersimpan lokal untuk bulan depan, slip dan file transfer, dasar aturan, dan tidak mengklaim UMK tanpa data.
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Sisa kecil pada uji ulang: kalimat "dua hal" lalu tiga butir. UMK Solo 2026 belum diisi sehingga cek batas upah dilewati (agent meminta angkanya).
- Versi 1.0.7 sampai 1.0.11 (antara lain mesin hitung disinkronkan, rujukan upah harian lepas, PPh 21 DTP PMK 105/2025) tidak diuji ulang di skenario ini.
- Satu skenario saja (dua karyawan tetap, tanpa karyawan masuk/keluar tahun berjalan).

## Cuplikan dari sumber (uji pertama)
Dengan skill, data Andi dan Sari tersimpan di komputer pemilik; hasil hitung sama persis dengan hitungan independen (transfer Rp3.164.150 dan Rp2.544.000, setor BPJS Rp818.800), lalu skill menawarkan: "bilang saja 'kunci' — saya buatkan slip gaji per orang dan file transfer CSV-nya."
