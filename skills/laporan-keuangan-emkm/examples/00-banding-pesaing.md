# 00 — Uji banding pesaing (S1)

## Pencarian yang dilakukan (2026-09-23)
| Sumber | Kata kunci / cara | Hasil |
|---|---|---|
| GitHub (web search) | `SKILL.md "financial statements" balance sheet income statement`, `laporan keuangan SAK EMKM skill` | openaccountant/skills, borghei/Claude-Skills (financial-analyst), insight68/Skills (finance-reconcile, audit), GAJETOso/financeskills (IFRS/GAAP) |
| github.com/adamriofc/indonesian-business-agent-skills (sudah dikurasi di `research/sources/kurasi-indonesian-business-agent-skills.md`) | clone read-only, cari `laporan`, `keuangan`, `psak` | **`tax-id/skills/laporan-keuangan-psak/SKILL.md`**, satu-satunya pesaing berbahasa/berkonteks Indonesia yang ditemukan |
| github.com/VoltAgent/awesome-openclaw-skills | grep `accounting`, `bookkeep`, `financial statement`, `indonesia` | accounting-workflows (Yunani), accountsos (UK), bookkeeping-basics (umum). Tidak ada yang untuk Indonesia/SAK EMKM |
| github.com/anthropics/skills | daftar skill | Tidak ada skill laporan keuangan (hanya xlsx/pdf/docx umum) |
| manairalabs/bicara-skills, alvinindra/bahasa-skills | daftar skill | Hanya bahasa/penulisan/WA/invoice-extract. Tidak ada laporan keuangan |
| ClawHub / skills.sh | lewat daftar VoltAgent & web search | Tidak ditemukan skill SAK EMKM |

Pesaing yang dibandingkan:
1. **adamriofc — `laporan-keuangan-psak`**, https://github.com/adamriofc/indonesian-business-agent-skills/blob/main/tax-id/skills/laporan-keuangan-psak/SKILL.md, lisensi **MIT** (file LICENSE dibaca). Pesaing utama: sama-sama menyebut SAK EMKM.
2. **openaccountant — `profit-loss`**, https://github.com/openaccountant/skills/blob/main/business/profit-loss/SKILL.md, lisensi **MIT**. Hanya laba rugi, konteks AS (dolar, bank Chase/Amex), basis kas. Dicatat sebagai pembanding sekunder.

Tidak ada script pihak ketiga yang dijalankan. Isi pesaing tidak disalin ke skill kita.

## Isi pesaing utama (ringkas)
`laporan-keuangan-psak` hanya ±25 baris: daftar standar (SAK EMKM/SAK EP), struktur output (Laba Rugi: pendapatan, HPP, laba kotor, beban operasional, laba usaha, pajak, laba bersih; Neraca: aset lancar/tidak lancar, liabilitas jangka pendek/panjang, ekuitas; CALK: kebijakan akuntansi & jadwal penyusutan). Input yang diminta adalah *trial balance* (neraca saldo). Tidak ada script (meski frontmatter menyebut `deterministic: true`), tidak ada aturan prive, tidak ada langkah bertanya, tidak ada disclaimer, tidak ada contoh.

## S1 dijalankan dengan instruksi pesaing
Penguji berperan sebagai agent yang memuat `laporan-keuangan-psak` dengan permintaan S1 yang sama. Karena pengguna memberi buku kas (bukan neraca saldo), agent mengelompokkan sendiri transaksinya. Instruksi pesaing tidak mengatur transaksi ambigu, jadi agent menebak. Angka hasilnya sama dengan agent tanpa skill (lihat `00-pembanding-tanpa-skill.md`), tetapi disusun dengan struktur pesaing:

> **LAPORAN LABA RUGI — Katering Dapur Sehati, periode 1 Januari – 31 Maret 2026 (SAK EMKM)**
>
> | Pos | Rp |
> |---|---:|
> | Pendapatan | 36.150.000 |
> | HPP | (11.900.000) |
> | Laba kotor | 24.250.000 |
> | Beban operasional (gaji 14.400.000; sewa 4.500.000; utilitas 3.150.000; kemasan 1.550.000; lain-lain 1.610.000; penyusutan 1.265.625) | (26.475.625) |
> | Laba (rugi) usaha | (2.225.625) |
> | Beban pajak (PPh final) | (156.500) |
> | **Laba (rugi) bersih** | **(2.382.125)** |
>
> **LAPORAN POSISI KEUANGAN per 31 Maret 2026**
>
> | Aset lancar | Rp | Liabilitas jangka pendek | Rp |
> |---|---:|---|---:|
> | Kas | 14.691.833 | Utang usaha | 600.000 |
> | Piutang usaha | 2.000.000 | Utang KUR jatuh tempo ≤ 12 bulan | 22.708.333 |
> | Piutang karyawan | 300.000 | **Ekuitas** | |
> | Persediaan | 1.650.000 | Modal | 22.400.000 |
> | **Aset tidak lancar** | | Rugi berjalan | (2.382.125) |
> | Peralatan (neto) | 18.984.375 | Prive | (5.700.000) |
> | **Total aset** | **37.626.208** | **Total liabilitas & ekuitas** | **37.626.208** |
>
> **CALK:** Kebijakan akuntansi signifikan: basis akrual, biaya historis. Jadwal penyusutan: peralatan lama 12.000.000/4 th → 750.000; kompor 1.450.000 → 90.625; freezer 6.800.000 → 425.000 (garis lurus, 3 bulan).

## Tabel penilaian (1–10)
| Kriteria | Skill kita (`laporan-keuangan-emkm`) | Pesaing (`laporan-keuangan-psak`) |
|---|---|---|
| Kualitas output | 9: tiga laporan SAK EMKM + tren + asumsi + "Perlu dicek" + ringkasan awam + saran | 6: struktur rapi (lancar/tidak lancar), tetapi tanpa ringkasan awam, asumsi, atau daftar yang perlu dicek |
| Kesesuaian konteks Indonesia | 9: prive, KUR, PPh final, format Rupiah, bahasa awam, tanggal "5 Januari 2026" | 6: menyebut SAK EMKM, tetapi instruksinya berbahasa Inggris, tidak menyinggung prive/KUR/PPh final |
| Akurasi | 8: script terverifikasi; ambigu ditanyakan; penyusutan per bulan beli (celah: bunga KUR, kulakan gas) | 5: tergantung agent; zakat pribadi ditebak jadi beban; penyusutan freezer terlalu besar; tidak ada cek seimbang otomatis |
| Siap pakai untuk awam | 9: satu kalimat + file cukup; pertanyaan maksimal 5; disclaimer | 4: meminta *trial balance* (awam tidak punya); tanpa disclaimer |
| **Keseluruhan** | **Menang** | Kalah |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Pemisahan lancar / tidak lancar** di Laporan Posisi Keuangan, termasuk "bagian utang KUR yang jatuh tempo dalam 12 bulan". Bank sering melihat ini untuk rasio likuiditas.
2. **Jadwal penyusutan per aset di CaLK** (nama aset, tanggal beli, harga, umur, penyusutan periode ini). Skill kita hanya menampilkan total.
3. (Dari openaccountant `profit-loss`) tampilkan **margin kotor dan margin bersih** sebagai baris eksplisit di laba rugi, serta panduan "tanpa agent" berupa rumus spreadsheet. Ini bisa menjadi fallback yang ramah untuk pembeli yang tidak punya Python.
