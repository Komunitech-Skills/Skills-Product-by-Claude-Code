# Skenario 01: Meta Ads, 6 iklan, hasil = pesan WA, minggu ini vs minggu lalu

- **Penguji:** agent penguji independen (simulasi, Claude Code), 2026-09-25. Bukan pembuat skill.
- **Usaha fiktif:** katering rumahan yang beriklan "klik ke WhatsApp" di Facebook/Instagram.
- **Permintaan pengguna:** "Ini ekspor Meta Ads minggu ini sama minggu lalu, hasilnya itu chat WA. Tolong buatin laporannya."
- **Nama kolom:** mengikuti ekspor Ads Manager level iklan: `Reporting starts`, `Reporting ends`, `Ad name`, `Results`, `Result indicator`, `Reach`, `Impressions`, `Cost per results`, `Amount spent (IDR)`, `Link clicks`, `CPC (cost per link click) (IDR)`, `CTR (link click-through rate)`. Nama ini sama dengan `references/sumber-kolom.md`.
- **Yang realistis di file ini:** iklan yang **tidak menghasilkan chat** punya sel `Results` dan `Cost per results` **kosong**, bukan `0`. Ads Manager menampilkan "—" untuk metrik tanpa nilai, dan sel ekspornya kosong. Perilaku ini berdasarkan pengalaman penguji dengan ekspor Meta. Belum dicocokkan dengan file ekspor asli, jadi pemilik perlu memastikannya dengan satu ekspor nyata.

## Input `meta_ini.csv` (14–20 Sep 2026)
```csv
Reporting starts,Reporting ends,Ad name,Ad delivery,Attribution setting,Results,Result indicator,Reach,Impressions,Cost per results,Amount spent (IDR),Link clicks,CPC (cost per link click) (IDR),CTR (link click-through rate),Ends
2026-09-14,2026-09-20,Video Testimoni - Paket Harian,active,7-day click or 1-day view,62,actions:onsite_conversion.messaging_conversation_started_7d,41250,68420,20090.32,1245600,1083,1150.14,1.582870,Ongoing
2026-09-14,2026-09-20,Carousel Menu Mingguan,active,7-day click or 1-day view,38,actions:onsite_conversion.messaging_conversation_started_7d,30110,52300,25959.21,986450,702,1405.20,1.342256,Ongoing
2026-09-14,2026-09-20,Promo Gratis Ongkir - Story,active,7-day click or 1-day view,21,actions:onsite_conversion.messaging_conversation_started_7d,25400,47810,38680.95,812300,655,1240.15,1.370006,Ongoing
2026-09-14,2026-09-20,Retargeting Pengunjung IG,active,7-day click or 1-day view,,actions:onsite_conversion.messaging_conversation_started_7d,9800,18760,,356900,212,1683.49,1.130064,Ongoing
2026-09-14,2026-09-20,Foto Produk Nasi Box,active,7-day click or 1-day view,4,actions:onsite_conversion.messaging_conversation_started_7d,15300,22150,124687.50,498750,188,2652.93,0.848758,Ongoing
2026-09-14,2026-09-20,Lookalike Pelanggan,active,7-day click or 1-day view,17,actions:onsite_conversion.messaging_conversation_started_7d,20040,31990,23657.65,402180,377,1066.79,1.178493,Ongoing
```
`meta_lalu.csv` (7–13 Sep) punya kolom yang sama. Isinya (iklan: hasil / tayangan / biaya / klik): Video 55/61.200/1.150.000/990; Carousel 40/50.100/900.000/690; Promo 18/45.000/790.000/600; Retargeting 2/17.000/300.000/190; Foto 6/21.000/450.000/170; Lookalike 12/29.000/380.000/330.

## A. Ekspor apa adanya (sel `Results` kosong)
```bash
python3 scripts/laporan_iklan.py analisis meta_ini.csv --sebelumnya meta_lalu.csv --nama-hasil "pesan WA"
```
Output (apa adanya, rc=0):
```
LAPORAN IKLAN MINGGUAN — Meta Ads (Facebook/Instagram)
Periode: (sesuai rentang tanggal file yang diunggah)

Total belanja iklan: Rp 3.945.280
Tayangan: 222.670 | Klik: 3.005 | Pesan wa: 142
CPC: Rp 1.313 | CPM: Rp 17.718 | CTR: 1,3%
Biaya per pesan WA: Rp 27.784

VS MINGGU LALU
Biaya iklan: Rp 3.945.280 (turun 0,6% dari minggu lalu)
Hasil: 142 (naik 6,8% dari minggu lalu)
Biaya per hasil: Rp 27.784 (turun 6,9% dari minggu lalu)

3 TERBAIK (biaya per pesan WA termurah)
1. Video Testimoni - Paket Harian: Rp 20.090/pesan WA (62 pesan WA, Rp 1.245.600)
2. Lookalike Pelanggan: Rp 23.658/pesan WA (17 pesan WA, Rp 402.180)
3. Carousel Menu Mingguan: Rp 25.959/pesan WA (38 pesan WA, Rp 986.450)

3 PERLU PERHATIAN (biaya per hasil termahal / tanpa hasil)
1. Foto Produk Nasi Box: Rp 124.688/pesan WA (4 pesan WA, Rp 498.750)
2. Promo Gratis Ongkir - Story: Rp 38.681/pesan WA (21 pesan WA, Rp 812.300)
3. Carousel Menu Mingguan: Rp 25.959/pesan WA (38 pesan WA, Rp 986.450)

SARAN
1. Tinjau/matikan iklan 'Foto Produk Nasi Box': biaya per pesan WA Rp 124.688, 4,5x rata-rata (Rp 27.784).
(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)

⚠️ Baris dilewati karena data tidak terbaca: {'angka tidak terbaca: hasil': 1}
```

### Verifikasi independen (Fraction/Decimal, tanpa kode skill; sel kosong = 0)
| Angka | Skill | Benar | Status |
|---|---|---|---|
| Total belanja | Rp 3.945.280 | **Rp 4.302.180** | ❌ kurang Rp 356.900 (iklan Retargeting dibuang) |
| Tayangan / klik | 222.670 / 3.005 | 241.430 / 3.217 | ❌ |
| CPC / CPM | Rp 1.313 / Rp 17.718 | Rp 1.337 / Rp 17.820 | ❌ |
| Biaya per pesan WA | Rp 27.784 | **Rp 30.297** | ❌ |
| Biaya vs minggu lalu (Rp 3.970.000) | **turun 0,6%** | **naik 8,4%** | ❌ **arah terbalik** |
| Biaya per hasil vs minggu lalu (Rp 29.850) | **turun 6,9%** | **naik 1,5%** | ❌ **arah terbalik** |
| Pesan WA 142 vs 133 | naik 6,8% | naik 6,8% | ✅ |
| Iklan 0 chat yang menghabiskan Rp 356.900 | **tidak muncul** di PERLU PERHATIAN maupun SARAN | harus jadi saran no. 1 | ❌ |

Aritmetika script konsisten dengan baris yang dipakainya. Hasil hitung ulang tanpa baris Retargeting sama persis dengan angka skill. Yang salah adalah **aturan pembacaan**: `parse_angka("")` → `None`, lalu seluruh baris dibuang (`scripts/laporan_iklan.py:420-423`). Peringatan yang muncul berupa `dict` Python mentah, sulit dipahami pengguna awam, dan tidak menyebut iklan mana yang dibuang maupun berapa biayanya.

## B. File yang sama dengan sel kosong diisi `0` (menguji aritmetika)
```bash
python3 scripts/laporan_iklan.py analisis meta_ini_nol.csv --sebelumnya meta_lalu.csv --nama-hasil "pesan WA" --csv-keluaran rincian.csv
```
```
Total belanja iklan: Rp 4.302.180
Tayangan: 241.430 | Klik: 3.217 | Pesan wa: 142
CPC: Rp 1.337 | CPM: Rp 17.820 | CTR: 1,3%
Biaya per pesan WA: Rp 30.297

VS MINGGU LALU
Biaya iklan: Rp 4.302.180 (naik 8,4% dari minggu lalu)
Hasil: 142 (naik 6,8% dari minggu lalu)
Biaya per hasil: Rp 30.297 (naik 1,5% dari minggu lalu)

3 TERBAIK (biaya per pesan WA termurah)
1. Video Testimoni - Paket Harian: Rp 20.090/pesan WA (62 pesan WA, Rp 1.245.600)
2. Lookalike Pelanggan: Rp 23.658/pesan WA (17 pesan WA, Rp 402.180)
3. Carousel Menu Mingguan: Rp 25.959/pesan WA (38 pesan WA, Rp 986.450)

3 PERLU PERHATIAN (biaya per hasil termahal / tanpa hasil)
1. Retargeting Pengunjung IG: Rp 356.900 terpakai, 0 pesan WA
2. Foto Produk Nasi Box: Rp 124.688/pesan WA (4 pesan WA, Rp 498.750)
3. Promo Gratis Ongkir - Story: Rp 38.681/pesan WA (21 pesan WA, Rp 812.300)

SARAN
1. Tinjau/hentikan iklan 'Retargeting Pengunjung IG': sudah menghabiskan Rp 356.900 tanpa pesan WA sama sekali.
2. Tinjau/matikan iklan 'Foto Produk Nasi Box': biaya per pesan WA Rp 124.688, 4,5x rata-rata (Rp 27.784).
```
**Verifikasi:** semua angka total, persen, dan saran **0 beda** dengan hitung ulang independen. `rincian.csv` berisi 6 iklan × (biaya, CPC, CPM, CTR, biaya per hasil), juga **0 beda**. Kolom turunan di file (`Cost per results`, `CPC`, `CTR`) tidak dipakai; semua metrik dihitung dari total. Sebagai contoh, rata-rata kolom `Cost per results` = Rp 46.615, sedangkan angka yang benar = Rp 30.297, dan skill memakai yang benar.

## Catatan lain dari skenario ini
- `Periode` tidak terisi walaupun file punya `Reporting starts`/`Reporting ends` (peran tanggal hanya mencari "date/day/tanggal/tgl", `:243`).
- Label "Pesan wa" (`.capitalize()` mengubah "WA" menjadi "wa", `:582`).
- "Carousel Menu Mingguan" muncul sekaligus di **3 TERBAIK** dan **3 PERLU PERHATIAN** (varian A). Di contoh pembuat sendiri, "Promo Lebaran - Kaos" juga muncul di keduanya.
- Saran "matikan" untuk iklan dengan **4 chat** tidak disertai catatan bahwa sampelnya kecil.
- "Rata-rata (Rp 27.784)" di saran berbeda dengan "Biaya per pesan WA Rp 30.297" di atasnya, karena rata-rata saran tidak menghitung iklan tanpa hasil. Pembaca awam bisa bingung.

**Hasil skenario: GAGAL** untuk ekspor apa adanya (angka utama dan arah perbandingan salah). Varian B **lulus** (angka 100% cocok).
