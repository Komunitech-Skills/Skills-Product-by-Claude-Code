# 00 — Uji banding pesaing: hitung THR

Tanggal: 2026-09-23 · Penguji: agent penguji independen (simulasi, Claude Code)

## Pencarian
- GitHub code search `filename:SKILL.md "Tunjangan Hari Raya"` (3 hasil: openaccountants — hanya menyebut THR sebagai penghasilan kena PPh 21; rancapoly/vault — benchmarking kompensasi, tidak relevan), `filename:SKILL.md PPh 21 TER`, kurasi internal `research/sources/kurasi-indonesian-business-agent-skills.md`.
- Dicek juga anthropics/skills, VoltAgent/awesome-openclaw-skills, ClawHub/skills.sh, manairalabs/bicara-skills, alvinindra/bahasa-skills: tidak ada skill THR.
- Pesaing relevan: **adamriofc/indonesian-business-agent-skills — `hr-id/skills/thr-calculator` + `engines/thr-calculator.js`** — https://github.com/adamriofc/indonesian-business-agent-skills — lisensi **MIT**. Script tidak dijalankan; logikanya (47 baris) dibaca dan ditiru di Python penguji.

## S1 dengan instruksi pesaing
Mesin pesaing hanya menerima `gaji_pokok, tunjangan_tetap, masa_kerja_bulan` (masa kerja harus dihitung sendiri oleh agent/pengguna). Tidak ada harian lepas, satuan hasil, PHK ≤ 30 hari, PKWT berakhir, tanggal batas bayar, PPh 21, atau pengumuman.

| Karyawan | Skill kita | Pesaing A (mengikuti instruksinya) | Benar |
|---|---:|---:|---:|
| Budi (tetap, 92 bln) | Rp 5.500.000 | Rp 5.500.000 | Rp 5.500.000 |
| Rina (kontrak, 8 bln) | Rp 3.200.000 | Rp 3.200.000 **bila** agent menghitung 8 bulan dengan benar (mesin tidak menghitung dari tanggal) | Rp 3.200.000 |
| Joko (harian lepas) | Rp 3.008.333 (rata-rata 12 bulan) | Tidak didukung — agent harus mengisi "gaji pokok" sendiri; rumus rata-rata harian lepas tidak ada di instruksi | Rp 3.008.333 |
| Wati (PHK 18 hari sebelum Lebaran) | Rp 5.200.000 + dasar Pasal 7 | Tidak ada aturan PHK; hasil tergantung tebakan agent | Rp 5.200.000 |
| Batas bayar | Rabu, 3 Maret 2027 | Hanya teks "at least 7 days prior" | 3 Maret 2027 |
| PPh 21 atas THR | Budi Rp 286.500, Rina Rp 120.000 | Tidak ada | sama dengan skill kita |
| Pengumuman karyawan | Ada | Tidak ada | — |

Akurasi rumus inti (≥ 12 bulan = 1 bulan upah; proporsional masa kerja/12) sama-sama benar. Uji massal skill kita: 3.000 kasus acak (tetap/kontrak/harian/satuan, masa kerja 0–26 bulan dan sekitar 12 bulan, PHK 1–60 hari sebelum hari raya, PPh 21 dengan/tanpa bruto bulan bayar) dibanding kalkulator independen penguji: **0 selisih** (di luar dua cacat berat yang dicatat di HASIL-UJI: PPh THR pegawai yang sudah berhenti, dan DTP tanpa cek).

## Penilaian

| Kriteria | Skill kita | Pesaing A |
|---|---|---|
| Kualitas output | 9 (tabel, catatan per orang, pengumuman, CSV) | 3 (JSON angka tunggal) |
| Kesesuaian konteks Indonesia | 9 (harian lepas, PKWT/PKWTT, PHK, H-7, SE 2026, bahasa awam) | 4 |
| Akurasi | 7 (THR benar; PPh pegawai berhenti & DTP bermasalah) | 6 (rumus inti benar, cakupan sangat sempit, tanpa PPh) |
| Siap pakai | 9 | 3 (butuh Node.js, masa kerja dihitung manual) |

**Kesimpulan: skill kita menang secara keseluruhan.**

## Yang bisa dipelajari (ide)
- Pesaing A menyatakan tegas "tidak dipakai untuk keputusan PHK tanpa pendamping" di metadata `not_for` — ide untuk mempertegas batas cakupan di awal output bila ada kasus PHK.
- Pesaing A memisahkan hasil "statutory minimum" dari kebijakan perusahaan — skill kita sudah punya `thr_minimum` vs `thr`; tampilkan keduanya di tabel bila berbeda.
