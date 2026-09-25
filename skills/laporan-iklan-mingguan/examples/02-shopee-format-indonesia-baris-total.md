# Skenario 02: Shopee Ads, angka format Indonesia + baris Total di akhir

- **Penguji:** agent penguji independen (simulasi, Claude Code), 2026-09-25.
- **Usaha fiktif:** toko hijab di Shopee dengan 5 iklan (1 Iklan Toko tanpa pesanan, 1 iklan dijeda dengan ROAS di bawah 1).
- **Permintaan:** "Ini download data Iklan Shopee minggu 14–20 Sep. Omzet toko 25 juta. Buatin laporan iklannya, hasilnya pesanan."
- **Kolom:** mengikuti "Download Data" Iklanku (Bahasa Indonesia): `Urutan, Nama Iklan, Status, Jenis Iklan, …, Dilihat, Jumlah Klik, Persentase Klik, Konversi, Konversi Langsung, …, Biaya per Konversi, …, Omzet Penjualan, Penjualan Langsung (GMV Langsung), Biaya, …, ACOS, ACOS Langsung`. Angka memakai format `"Rp1.234.567"`, `"2,50%"`, `"Rp446.294,5"`. Catatan: ekspor asli Shopee biasanya diawali beberapa baris info toko/periode sebelum baris judul kolom. Baris itu sudah dihapus di sini, dan kasusnya dibahas di skenario 04.

## Input (ringkas; kolom lain seperti di atas)
```csv
Urutan,Nama Iklan,Status,Jenis Iklan,…,Dilihat,Jumlah Klik,Persentase Klik,Konversi,…,Omzet Penjualan,…,Biaya,…
1,Hijab Voal Motif - Pencarian,Berjalan,Iklan Produk,…,"48.215","1.206","2,50%",38,…,"Rp3.895.000",…,"Rp960.000",…
2,Gamis Katun Premium,Berjalan,Iklan Produk,…,"22.930","641","2,80%",12,…,"Rp2.868.000",…,"Rp750.000",…
3,Toko - Iklan Toko,Berjalan,Iklan Toko,…,"15.404","2","0,01%",0,…,"Rp0",…,"Rp100.001",…
4,Pashmina Ceruty,Berjalan,Iklan Produk,…,"61.772","1.877","3,04%",25,…,"Rp1.620.000",…,"Rp446.294,5",…
5,Bundling Mukena Anak,Dijeda,Iklan Produk,…,"3.120","58","1,86%",1,…,"Rp189.000",…,"Rp212.340",…
<baris total>,"151.441","3.784","2,50%",76,…,"Rp8.572.000",…,"Rp2.468.635,5",…
```
File lengkap (28 kolom) dibuat penguji. Angka `Rp100.001` (CPC Rp 50.000,5) dan `Rp446.294,5` sengaja dipilih untuk menguji pembulatan 0,5 menjauhi nol.

## Varian A: "Total" di kolom `Nama Iklan`
```bash
python3 scripts/laporan_iklan.py analisis shopee.csv --nama-hasil pesanan --periode "14-20 Sep 2026" --omzet 25000000 --csv-keluaran rincian.csv
```
```
LAPORAN IKLAN MINGGUAN — Shopee Ads
Periode: 14-20 Sep 2026

Total belanja iklan: Rp 2.468.636
Tayangan: 151.441 | Klik: 3.784 | Pesanan: 76
CPC: Rp 652 | CPM: Rp 16.301 | CTR: 2,5%
Biaya per pesanan: Rp 32.482
ROAS: 3,5x
Biaya iklan vs omzet: 9,9% dari omzet Rp 25.000.000

3 TERBAIK (biaya per pesanan termurah)
1. Pashmina Ceruty: Rp 17.852/pesanan (25 pesanan, Rp 446.295)
2. Hijab Voal Motif - Pencarian: Rp 25.263/pesanan (38 pesanan, Rp 960.000)
3. Gamis Katun Premium: Rp 62.500/pesanan (12 pesanan, Rp 750.000)

3 PERLU PERHATIAN (biaya per hasil termahal / tanpa hasil)
1. Toko - Iklan Toko: Rp 100.001 terpakai, 0 pesanan
2. Bundling Mukena Anak: Rp 212.340/pesanan (1 pesanan, Rp 212.340)
3. Gamis Katun Premium: Rp 62.500/pesanan (12 pesanan, Rp 750.000)

SARAN
1. Tinjau/hentikan iklan 'Toko - Iklan Toko': sudah menghabiskan Rp 100.001 tanpa pesanan sama sekali.
2. Tinjau/matikan iklan 'Bundling Mukena Anak': biaya per pesanan Rp 212.340, 6,8x rata-rata (Rp 31.166).
3. Tinjau/matikan iklan 'Gamis Katun Premium': biaya per pesanan Rp 62.500, 2,0x rata-rata (Rp 31.166).
(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)

Catatan: Tidak ada label mata uang di file; diasumsikan IDR (Rupiah). 1 baris 'Total/Jumlah' di file diabaikan agar tidak dihitung dua kali.
```
**Verifikasi independen:** total biaya 2.468.635,5 → Rp 2.468.636 (0,5 dibulatkan ke atas), CPC 652, CPM 16.301, CTR 2,5%, biaya/pesanan 32.482, ROAS 8.572.000 ÷ 2.468.635,5 = 3,47 → **3,5x**, biaya vs omzet **9,9%**, rata-rata saran 31.166, 6,8x, 2,0x (2,005): **0 beda**. `rincian.csv` per iklan (biaya, CPC termasuk 50.000,5 → **50.001**, CPM, CTR, biaya/pesanan, ROAS): **0 beda**. Baris total **tidak** ikut dihitung. Metrik dihitung dari total kolom, bukan dari rata-rata `Persentase Klik`.

Cacat tampilan: **"Gamis Katun Premium" muncul di 3 TERBAIK no. 3, di PERLU PERHATIAN no. 3, dan disarankan "Tinjau/matikan"** dalam laporan yang sama. Ini membingungkan, karena dengan 5 iklan, daftar terbaik dan terburuk bertumpuk (`:480-484`).

## Varian B: "Total" di kolom pertama (`Urutan`), `Nama Iklan` kosong
Baris total yang sama, hanya pindah kolom (`Total,,,,…`):
```
Total belanja iklan: Rp 4.937.271
Tayangan: 302.882 | Klik: 7.568 | Pesanan: 152
…
Biaya iklan vs omzet: 19,7% dari omzet Rp 25.000.000

3 TERBAIK (biaya per pesanan termurah)
1. Pashmina Ceruty: …
2. Hijab Voal Motif - Pencarian: …
3. Kampanye #6: Rp 32.482/pesanan (76 pesanan, Rp 2.468.636)
```
**❌ Dihitung dua kali.** Biaya, klik, pesanan, dan % omzet menjadi **2×**, dan baris total tampil sebagai iklan "Kampanye #6" di 3 TERBAIK. Tidak ada peringatan. Penyebabnya, pengenalan baris total hanya memeriksa kolom nama (`:405-408`).

## Varian C: label total lain (di kolom `Nama Iklan`)
| Label | Dilewati? | Total biaya |
|---|---|---|
| `Total`, `TOTAL`, `Grand Total` | ya | Rp 2.468.636 ✅ |
| `Total:` | **tidak** | Rp 4.937.271 ❌ |
| `Total (5 iklan)` | **tidak** | Rp 4.937.271 ❌ |
| `Total: Account` (gaya Google Ads) | **tidak** | Rp 4.937.271 ❌ |
| `Jumlah Total` | **tidak** | Rp 4.937.271 ❌ |

Pengenalan memakai kecocokan persis dengan himpunan kata (`:265-266`), bukan awalan "total"/"jumlah".

**Hasil skenario:** varian A **lulus** (angka 100% cocok, dengan cacat tampilan terbaik/terburuk). Varian B/C **gagal** (baris total dihitung dua kali tanpa peringatan).
