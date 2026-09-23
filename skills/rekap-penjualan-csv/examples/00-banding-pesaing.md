# Banding Pesaing – rekap-penjualan-csv (uji ulang v1.2.0)

## Pencarian
- **Kata kunci:** `filename:SKILL.md sales csv` (GitHub code search), "SKILL.md sales report CSV analysis skill claude openclaw revenue top products" (web), "rekap penjualan", "laporan penjualan".
- **Sumber yang diperiksa:** GitHub code search (21.088 hasil `SKILL.md` + sales/csv; 15 teratas diperiksa judulnya), web search, `manairalabs/bicara-skills` (README: hanya `invoice-extract-id` dan `wa-reply-id`, tidak ada rekap penjualan), `alvinindra/bahasa-skills` (skill gaya bahasa, tidak relevan). API GitHub untuk `anthropics/skills` diblokir di sesi ini, tetapi repo itu dikenal hanya punya skill `xlsx` umum (bukan rekap penjualan CSV), jadi tidak diuji. Situs awesome-openclaw-skills/ClawHub/skills.sh tidak diperiksa terpisah. Web search mengarah ke pesaing yang sama di katalog mcpservers.org.
- **Kandidat yang dibaca:**
  - `modbender/skill-library-mcp` → `data/sales/SKILL.md`: skill CRM/pipeline/outreach, **tidak relevan** (bukan analisis file penjualan).
  - **`coffeefuelbump/csv-data-summarizer-claude-skill`** → `SKILL.md` v2.1.0. Skill publik paling dikenal untuk menganalisis CSV, termasuk yang secara eksplisit menyebut "Sales/E-commerce data: time-series trends, revenue analysis, product performance". **Pesaing yang dipilih.**
    - URL: https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill (SKILL.md dibaca lewat raw.githubusercontent.com, 2026-09-23)
    - Lisensi: **MIT** (badge & bagian License di README; file `LICENSE` tidak ditemukan di cabang `main`)
    - Ketergantungan: pandas ≥ 2.0, matplotlib, seaborn. Script `analyze.py` **tidak dijalankan** sesuai brief. Penguji berperan sebagai agent yang mengikuti instruksi SKILL.md pesaing, dengan kode pandas yang ditulis sendiri (`/tmp/uji-rekap-penjualan-csv/pesaing/sim_pesaing.py`).

## Ringkas instruksi pesaing (parafrase, bukan salinan)
Langsung analisis tanpa bertanya apa pun. Muat CSV ke pandas, kenali tipe kolom, lalu pilih analisis sesuai jenis data. Tampilkan ikhtisar dataset, statistik ringkas (mean/std/kuartil), data kosong, grafik yang relevan, dan insight. Kolom tanggal dikenali dari nama kolom yang mengandung "date". Dilarang menawarkan pilihan atau bertanya.

## Skenario S1 (sama dengan contoh 01)
```
Halo, ini file export kasir kedai kopi aku 2 minggu pertama September (kasir-kopi-sept.csv). Tolong direkap ya, mau tau menu mana yang paling laku sama hari apa yang paling rame.
```

### A. Dengan skill pesaing (csv-data-summarizer)
Proses agent: `pd.read_csv` → 127 × 4. Tipe kolom: `Tanggal` teks, `Produk` teks, `Qty` int, `Total` teks (berisi "Rp 60.000"). **Kolom tanggal tidak terdeteksi** karena namanya tidak mengandung "date", jadi menurut aturan pesaing tidak ada plot deret waktu. Agent "beradaptasi" untuk data sales: membersihkan `Total` dengan membuang karakter non-digit.

> **Saya langsung menganalisis data ini secara menyeluruh.**
>
> **Ikhtisar dataset**
> - 127 baris × 4 kolom (1 kolom numerik: Qty; 3 kolom teks)
> - Tidak ada nilai kosong (0%)
>
> **Statistik ringkas**
> - Qty per transaksi: rata-rata 2,5 (std 1,12; min 1; median 2; maks 4)
> - Nilai per transaksi: rata-rata Rp 40.031,50 (std Rp 21.507,82)
> - Total pendapatan: Rp 5.084.000
>
> **Performa produk (pendapatan)**
> | Produk | Pendapatan |
> |---|---|
> | Matcha Latte | 1.320.000 |
> | Es Kopi Susu Gula Aren | 1.134.000 |
> | Roti Bakar Coklat | 848.000 |
> | Americano | 645.000 |
> | Pisang Goreng | 432.000 |
>
> **Harian:** tertinggi 07/09/2026 (549.000), terendah 14/09/2026 (214.000).
>
> **Insight**
> - Matcha Latte adalah produk dengan pendapatan tertinggi.
> - Distribusi Qty cenderung terkumpul di 2–3 item per transaksi.
> - Terdapat variasi pendapatan harian yang cukup besar.
>
> *(Terlampir: histogram Qty, diagram batang pendapatan per produk)*

### B. Dengan skill kita (rekap-penjualan-csv v1.2.0)
Lihat output lengkap di `01-kasir-kedai-kopi-2-minggu.md`. Ringkasnya: total Rp 5.084.000, 127 baris, rata-rata per hari kalender vs hari berjualan, tabel 5 terlaris dengan Qty + Omzet + %, hari terbaik/terendah dengan nama hari (Senin, 7 Sept / Senin, 14 Sept), perbandingan minggu 1 vs 2 (+5,4%), dan 3 insight yang bisa langsung dijalankan (stok matcha, paket minuman + roti bakar, cek penyebab Senin 14 Sept turun).

### Verifikasi angka
Angka pada kedua versi untuk file S1 **sama dan benar** (total, top-5, hari terbaik/terendah), karena file S1 rapi (`Rp 60.000`, tanpa desimal). Simulasi pesaing pada file uji lain (cara pembersihan yang sama, "ambil digit"):
| File | Pesaing (simulasi) | Skill kita v1.2.0 | Benar |
|---|---|---|---|
| 02 `35.000,00` (harga satuan berdesimal koma) | Rp 1.389.910.000 (100×) | Rp 13.899.100 | Rp 13.899.100 |
| 06 ekspor Shopee + status | Rp 10.793.000 (tanpa instruksi menyaring batal/retur) | Rp 9.006.000 + daftar status dihitung/dibuang | Rp 9.006.000 |
| 07 CSV ANSI dari Excel | `pd.read_csv` gagal: `UnicodeDecodeError` (agent harus memperbaiki sendiri) | terbaca + peringatan encoding | Rp 2.538.500 |
| 08 `15.000.00`, `1.5E+06`, `16000.500` | ditebak diam-diam (`1.5E+06` → 1.506; `15.000.00` → 1.500.000; `16000.500` → 16.000.500) | dilewati + dilaporkan | dilewati |

## Tabel penilaian (S1 + ketahanan data nyata)
| Aspek | Pesaing (csv-data-summarizer) | Skill kita | Catatan |
|---|---|---|---|
| Kualitas laporan | 6 | 9 | Pesaing memberi statistik (std, kuartil) yang tidak berguna bagi pemilik kedai; insight generik. Skill kita menjawab langsung "menu paling laku" dan "hari paling ramai". |
| Kesesuaian konteks Indonesia | 3 | 10 | Pesaing: kolom "Tanggal" tidak dikenali, format rupiah tidak diatur, status marketplace ID tidak dikenal. Skill kita: `Rp 15.000,-`, `1.500.000,50`, ANSI Excel, tanggal "14 Sept 2026", status "Pengembalian Barang/Dana". |
| Akurasi | 6 (S1 benar; salah besar pada 3 dari 4 file lain) | 10 (semua file cocok verifikasi independen) | — |
| Siap pakai | 6 (butuh pandas + matplotlib + seaborn; ada grafik) | 8 (Python standar saja; belum ada grafik) | Satu-satunya keunggulan jelas pesaing: grafik otomatis. |
| **Keseluruhan** | **5** | **9** | **Skill kita menang.** |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Grafik opsional.** Tren harian dan batang omzet per produk sangat membantu pemilik usaha awam. Pertimbangkan opsi `--grafik` (misalnya SVG sederhana tanpa library tambahan) atau instruksi agar agent menawarkan grafik bila lingkungannya mendukung.
2. **Ringkasan kualitas data di awal** (jumlah baris, kolom kosong). Skill kita sudah melaporkan baris dilewati. Satu baris "kualitas data: 127/127 baris terbaca" di awal laporan bisa menambah kepercayaan.
3. **Sikap "langsung kerjakan"** cocok untuk file rapi. Skill kita sudah begitu, dan tetap bertanya bila ada ambiguitas (urutan tanggal, kolom harga hilang). Ini lebih aman daripada larangan bertanya mutlak dari pesaing.
