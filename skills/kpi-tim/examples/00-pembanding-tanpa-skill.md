# Uji A/B — tanpa skill vs dengan skill (skenario 01, toko retail 5 orang)

> Penguji independen, 2026-09-29. "Tanpa skill" = jawaban agent umum tanpa SKILL.md, disimulasikan
> penguji dengan pendekatan yang lazim dipakai (dan dihitung ulang dengan Python agar angkanya
> mencerminkan metode itu, bukan salah hitung). Data sama dengan `01-toko-retail-5-orang.md`.

## Tanpa skill (pendekatan umum)
Agent umum biasanya: capaian naik = realisasi ÷ target; capaian turun = **target ÷ realisasi**;
**tanpa batas atas**; realisasi 0 untuk KPI turun ditangani ad hoc; data kosong dianggap 0 atau
diabaikan diam-diam; tidak ada status berbasis ambang; tidak ada tren; output berupa tabel Markdown.

| Orang | Skor tanpa skill | Masalah |
|---|---|---|
| Wulan | 122,1 | Void 0 kali → target÷0 tak terdefinisi, diberi "200%"; tanpa batas, satu KPI mendongkrak skor |
| Rudi | 71,3 | Kehadiran belum diisi → dianggap 0% → Rudi tampak 🔴 padahal datanya telat |
| Fajar | 103,2 | Salah kirim 2 vs 3 → 150%; menutupi "item stok habis" 9 vs 5 dan akurasi stok di bawah ambang |
| Nadia | 110,1 | |
| Bayu | 125,0 | Leads 158% tanpa batas; CPL 15.000/12.000 = 125% |

Tidak ada: file Excel siap impor, lembar petunjuk, validasi bobot, status ambang, tren vs Agustus,
peringatan data kosong, mode tanpa nama, bahan 1:1, catatan etika.

## Dengan skill
| Orang | Skor | Keterangan |
|---|---|---|
| Wulan | 🟢 106,1 ▲18,4 | void 0 → (2−0/2)=200% → dibatasi 120% |
| Rudi | ⚪ belum lengkap | tidak ikut rata-rata divisi; disebut KPI yang kosong |
| Fajar | 🟡 91,9 ▲5,7 | "perlu perhatian: Item stok habis 20,0%"; akurasi 96,8 < ambang 97 → 🔴 |
| Nadia | 🟢 106,1 ▲20,1 | |
| Bayu | 🟢 112,4 ▲27,7 | leads dibatasi 120%; CPL (2−0,8)=120% |

Plus: `rencana-kpi.xlsx` + CSV, validasi (`cek`), laporan siap Telegram, tren, 1:1 per orang, `--tanpa-nama`.
Semua angka lulus verifikasi independen (90 nilai, 0 selisih).

## Kesimpulan
Dengan skill **jelas lebih baik**: tanpa skill, Fajar tampak "tercapai" (103,2) padahal dua KPI mutu
bermasalah, dan Rudi dirugikan karena data telat. Skill memberi aturan eksplisit (rumus turun, batas
120%, mode data kosong) yang membuat hasil adil dan dapat diulang. Bahan "sebelum/sesudah" README valid.
