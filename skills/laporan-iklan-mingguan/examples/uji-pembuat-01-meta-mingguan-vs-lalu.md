# Contoh 01 — Meta Ads, minggu ini vs minggu lalu + omzet

> Dijalankan sendiri oleh pembuat skill saat pengembangan (bukan uji independen Tahap 6
> `CLAUDE.md` — itu perlu agent/sesi terpisah yang belum dilakukan untuk skill ini). Disertakan
> agar pembeli/reviewer bisa melihat contoh nyata input → output sebelum memakainya.

## Skenario
Toko baju online beriklan di Meta (Facebook/Instagram) untuk 3 kampanye. Pemilik mengekspor CSV
minggu ini dan minggu lalu dari Ads Manager, dan tahu omzet toko minggu ini Rp 20.000.000 (dari
`rekap-penjualan-csv`).

## Input: `meta_minggu_ini.csv`
```csv
Campaign name,Ad set name,Ad name,Amount spent (IDR),Impressions,Reach,Link clicks,CTR (link click-through rate),CPC (cost per link click) (IDR),"CPM (cost per 1,000 impressions) (IDR)",Results,Cost per results (IDR),Purchases,Purchase conversion value,Website purchase ROAS (return on ad spend)
Promo Lebaran - Kaos,AS1,Ad1,1500000,80000,60000,900,1.13,1666.67,18750,45,33333.33,20,4500000,3.0
Retargeting - Semua Produk,AS2,Ad2,800000,40000,35000,300,0.75,2666.67,20000,0,0,0,0,0
Prospek Baru - Tas,AS3,Ad3,600000,30000,28000,200,0.67,3000,20000,5,120000,3,900000,1.5
Total,,,2900000,150000,,1400,,,,,,,,
```
(Kolom `CPC (cost per link click)`, `CPM (cost per 1,000 impressions)`, `Cost per results`,
`Website purchase ROAS` sengaja disertakan untuk membuktikan script **tidak** memakai kolom
turunan ini secara langsung — semua dihitung ulang dari `Amount spent`/`Impressions`/
`Link clicks`/`Results`/`Purchase conversion value`, dan baris `Total` dilewati.)

## Input: `meta_minggu_lalu.csv`
```csv
Campaign name,Ad set name,Ad name,Amount spent (IDR),Impressions,Reach,Link clicks,Results,Purchases,Purchase conversion value
Promo Lebaran - Kaos,AS1,Ad1,1200000,70000,55000,700,40,18,3800000
Retargeting - Semua Produk,AS2,Ad2,750000,38000,33000,280,2,1,150000
Prospek Baru - Tas,AS3,Ad3,500000,25000,23000,180,4,2,600000
```

## Perintah
```bash
python3 scripts/laporan_iklan.py analisis meta_minggu_ini.csv \
  --sebelumnya meta_minggu_lalu.csv --omzet 20000000
```

## Output (apa adanya dari script, v1.0.1)
```
LAPORAN IKLAN MINGGUAN — Meta Ads (Facebook/Instagram)
Periode: (tidak ada kolom tanggal di file; sebutkan periodenya)

Total belanja iklan: Rp 2.900.000
Tayangan: 150.000 | Klik: 1.400 | Results: 50
CPC: Rp 2.071 | CPM: Rp 19.333 | CTR: 0,9%
Biaya per Results: Rp 58.000
ROAS: 1,9x
Biaya iklan vs omzet: 14,5% dari omzet Rp 20.000.000

VS MINGGU LALU
Biaya iklan: Rp 2.900.000 (naik 18,4% dari minggu lalu Rp 2.450.000)
Hasil: 50 (naik 8,7% dari minggu lalu 46)
Biaya per hasil: Rp 58.000 (naik 8,9% dari minggu lalu Rp 53.261)

TERBAIK (biaya per Results termurah)
1. Promo Lebaran - Kaos: Rp 33.333/Results (45 Results, Rp 1.500.000)

PERLU PERHATIAN (tanpa hasil / biaya per hasil termahal)
1. Retargeting - Semua Produk: Rp 800.000 terpakai, 0 Results
2. Prospek Baru - Tas: Rp 120.000/Results (5 Results, Rp 600.000)

SARAN
1. Tinjau/hentikan iklan 'Retargeting - Semua Produk': sudah menghabiskan Rp 800.000 tanpa Results sama sekali.
2. Tinjau/matikan iklan 'Prospek Baru - Tas': biaya per Results Rp 120.000, 2,1x rata-rata semua iklan (Rp 58.000).
(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)

Catatan:
- 1 baris total/ringkasan ('Total') diabaikan agar tidak dihitung dua kali.
- Biaya iklan diambil dari file ekspor. Tagihan platform ke akun Indonesia bisa ditambah PPN (cek invoice/faktur platform), jadi persentase terhadap omzet bisa sedikit lebih tinggi.
- Kolom dibaca: nama='Campaign name', biaya='Amount spent (IDR)', tayangan='Impressions', klik='Link clicks', hasil='Results', nilai='Purchase conversion value'.
```

## Verifikasi angka manual (independen dari script)
- Total biaya = 1.500.000 + 800.000 + 600.000 = **2.900.000** ✓ (baris `Total` yang mencantumkan
  2.900.000 di file TIDAK dipakai — angka ini hasil jumlah baris kampanye, kebetulan sama, yang
  membuktikan baris Total memang dilewati bukan malah dijumlah dua kali jadi 5.800.000).
- Total hasil = 45 + 0 + 5 = **50** ✓ (kolom `Results`, bukan `Cost per results`).
- Biaya per hasil = 2.900.000 ÷ 50 = **58.000** ✓.
- ROAS = (4.500.000 + 0 + 900.000) ÷ 2.900.000 = 5.400.000 ÷ 2.900.000 = 1,862... → **1,9x** ✓
  (dibulatkan 1 desimal, aturan 0,05 menjauhi nol).
- Biaya minggu lalu = 1.200.000 + 750.000 + 500.000 = 2.450.000. Kenaikan biaya =
  (2.900.000 − 2.450.000) ÷ 2.450.000 × 100 = 18,367...% → **18,4%** ✓.
- Hasil minggu lalu = 40 + 2 + 4 = 46. Kenaikan hasil = (50 − 46) ÷ 46 × 100 = 8,695...% →
  **8,7%** ✓.
- Biaya iklan vs omzet = 2.900.000 ÷ 20.000.000 × 100 = **14,5%** ✓.
- Biaya per hasil minggu lalu = 2.450.000 ÷ 46 = 53.260,87 → **Rp 53.261**; kenaikan
  (58.000 − 53.260,87) ÷ 53.260,87 × 100 = 8,898...% → **8,9%** ✓.
- Saran #2 (v1.0.1): pembanding = biaya per hasil **semua iklan** (angka yang sama dengan baris
  "Biaya per Results" di atas) = 58.000. Prospek Baru 120.000 ÷ 58.000 = 2,068... → **2,1×
  rata-rata** ✓. (v1.0.0 memakai rata-rata iklan ber-hasil saja, Rp 42.000, yang berbeda dari
  angka di atasnya dan membingungkan; lihat R5 di `HASIL-UJI.md`.)
- Daftar TERBAIK hanya berisi Promo Lebaran; v1.0.1 tidak lagi menaruh iklan yang sama di TERBAIK
  dan PERLU PERHATIAN sekaligus (S2).

Semua angka di atas dihitung ulang manual dan cocok dengan keluaran script — tidak ada angka yang
diperkirakan/dikarang.

## Catatan
- Karena tidak ada kolom tanggal di file contoh ini, `Periode` menampilkan label default. Ekspor
  Ads Manager sungguhan biasanya sudah mencantumkan rentang tanggal yang dipilih saat mengunduh;
  bila filenya punya kolom tanggal (harian per kampanye), script mengelompokkan otomatis per
  kampanye dan mendeteksi rentang tanggalnya (lihat `SKILL.md`).
- Uji lebih lengkap (per platform lain, format angka campur, mata uang asing, file rusak, gabung
  lintas platform, formula injection, serta regresi semua temuan uji independen v1.0.0) ada di
  `tests/uji_regresi.py`: 49 tes, semua lulus (`python3 tests/uji_regresi.py`).
