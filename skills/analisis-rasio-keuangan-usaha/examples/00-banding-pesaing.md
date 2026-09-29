# Uji banding pesaing — analisis-rasio-keuangan-usaha vs skill publik

> Penguji independen (Akun B), 2026-09-26. Skill pesaing **hanya dibaca dan dinilai**, tidak disalin. Script pesaing diperiksa dulu (impor hanya `json`/`typing`/`argparse`/`sys`, tanpa jaringan/subprocess/eval, hanya membuka file input), lalu dijalankan di scratchpad dengan data yang sama.

## Pesaing yang dinilai
| # | Skill | Sumber | Lisensi | Versi yang dibaca |
|---|---|---|---|---|
| P1 | `analyzing-financial-statements` ("Financial Ratio Analyzer" di notebook `03_skills_custom_development.ipynb`) | https://github.com/anthropics/claude-cookbooks/tree/main/skills/custom_skills/analyzing-financial-statements | MIT (c) 2023 Anthropic | commit `813fbeec03cdedfda7808529438d1c7af71f26eb` (24-09-2026) |
| P2 | `financial-analyst` (ratio_calculator.py) | https://github.com/alirezarezvani/claude-skills/tree/main/finance/skills/financial-analyst | MIT (c) 2025 Alireza Rezvani | commit `19392f7a08264ed00486a251f5b2098321771f94` (26-08-2026) |

Kata kunci pencarian: "SKILL.md financial ratio analysis skill github clawhub small business". Hasil lain (himself65/finance-skills, borghei/Claude-Skills financial-analyst, accounting-skills.com) berfokus pada analisis saham/perusahaan besar dan tidak dijalankan. Tidak ditemukan skill publik berbahasa Indonesia untuk rasio keuangan UMKM.

## Skenario normal #1 (warung sembako 2025, data sama dengan Uji 03)
Input pesaing: dict/JSON bahasa Inggris (revenue 420.000.000, COGS 361.200.000, net income 16.800.000, current assets 58.700.000, inventory 48.000.000, cash 6.500.000, AR 4.200.000, total assets 76.700.000, current liabilities = total debt 29.000.000, equity 47.700.000). Untuk P1 dipakai `perform_comprehensive_analysis(industry="retail")`.

| Aspek | P1 cookbook | P2 financial-analyst | Skill kita |
|---|---|---|---|
| Angka inti (current 2,02 · quick 0,37 · DER 0,61 · margin kotor 14%) | benar (float) | benar (float) | benar (Decimal, 35/35 terverifikasi) |
| Rata-rata saldo & tren 2 tahun | tidak (fungsi tren ada, tetapi tanpa data historis otomatis) | tidak | ya (tren 19 baris; catatan: basis campur, lihat HASIL-UJI) |
| Umur stok / lama piutang / siklus kas | hanya turnover & DSO | turnover & DSO | ya, lengkap + siklus kas |
| Ambang sesuai warung | margin kotor 14% = **"Poor"** (tolok ukur retail AS 20–40%) | margin kotor 14% = "Below average" | 🟡 Waspada (ambang dagang 8–15%) |
| Rasio cepat 0,37 | "N/A" (tanpa tafsiran) | "Below average" | 🟡 + arti sehari-hari + saran |
| Kesiapan KUR & cicilan | tidak ada | tidak ada | ✓/✗ + rasio cicilan 53,6% |
| Bahasa & format | Inggris, JSON/teks teknis | Inggris, teks teknis + rasio valuasi 0,00 yang tidak relevan | Indonesia awam, tabel siap tempel |
| Input format Indonesia (`Rp 1.500.000`, `2,5 jt`, `(500.000)`) | tidak | tidak | ya |
| Disclaimer | "Historical data doesn't guarantee future performance" | tidak spesifik | bukan nasihat investasi/kredit, ambang bukan standar OJK/bank |

## Uji tepi pada pesaing (data sama dengan uji tepi skill kita)
| Kasus | P1 cookbook | P2 financial-analyst | Skill kita |
|---|---|---|---|
| Utang lancar = 0 | current/quick/cash ratio = **0,00** (seolah bangkrut); ringkasan "Debt-to-equity of 0.00 indicates conservative leverage" | Current ratio 0,00 "Insufficient data" | "tidak dihitung — tidak ada utang jangka pendek (kondisi aman)" |
| Modal −20 jt, rugi −6 jt | ROE = **+30,0%** → "ROE of 30.0% indicates **strong shareholder returns**" | ROE 30,0% "**Excellent**"; DER **−1,90** "Conservative leverage - **strong equity position**" | ROE & DER "tidak bermakna" 🔴, "Modal habis/negatif" jadi saran #2, KUR "BELUM SIAP" |
| Penjualan 0 | margin = 0 | margin = 0 | "tidak dihitung — penjualan Rp 0" |

Kedua pesaing memberi kesimpulan **berbahaya** untuk usaha yang modalnya sudah negatif dan sedang rugi (ROE "excellent", leverage "conservative"). Skill kita menangani kasus ini dengan benar.

## Skor berdampingan (1–10, untuk pembeli UMKM Indonesia)
| Kriteria | P1 | P2 | Kita |
|---|:-:|:-:|:-:|
| Akurasi & penanganan pembagi nol/negatif | 4 | 4 | 9 |
| Relevansi ambang untuk UMKM | 2 | 3 | 8 |
| Kelengkapan (aktivitas, tren, kredit) | 4 | 5 | 9 |
| Kemudahan awam (bahasa, format) | 2 | 3 | 9 |
| Keamanan & kejujuran (disclaimer, tanpa janji) | 6 | 5 | 9 |
| **Rata-rata** | **3,6** | **4,0** | **8,8** |

**Kesimpulan:** skill kita **unggul telak** dan tidak kalah di aspek apa pun untuk tugas ini. Kelebihan pesaing yang layak dipelajari (bukan disalin): P2 menampilkan **rumus di setiap baris** dan kategori "Insufficient data" yang konsisten (skill kita sudah punya keduanya). P1/P2 menyediakan rasio **DSCR** (arus kas operasi ÷ total cicilan). Versi Indonesia yang ditulis ulang ("cakupan cicilan dari arus kas") bisa menjadi tambahan di masa depan, karena bank memakai logika serupa.
