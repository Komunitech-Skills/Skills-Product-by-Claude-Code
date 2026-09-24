# 02 — Jurnal trading 12 transaksi → P/L FIFO (diverifikasi independen)

**Skenario:** S2 normal. Member menempel jurnal campuran format angka (Rp, titik ribuan, koma desimal, huruf kecil `btc`), beli bertahap, jual sebagian, biaya exchange, 3 koin.

## Input pengguna (persis)
> rapikan jurnal trading saya dong, hitung untung ruginya. ini file kripto/JURNAL.csv

```csv
tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat
2026-01-10,BTC,beli,0.005,"Rp 1.380.000.000",20.700,DCA bulan 1,,
2026-02-10,BTC,beli,0.004,1.420.000.000,"17.040",DCA bulan 2,,
2026-03-10,btc,beli,0.006,1350000000,24300,DCA bulan 3,2026-09-01,"cek lagi rencana DCA setelah 6 bulan"
2026-03-20,ETH,beli,0.5,"52.000.000",7.800,beli setelah baca roadmap,,
2026-04-02,SOL,beli,10,2.450.000,"36.750",coba diversifikasi kecil,2026-10-01,"tinjau kalau porsi SOL sudah terasa terlalu besar buat saya"
2026-04-15,ETH,beli,0.3,48.500.000,"4.365",tambah posisi,,
2026-05-05,BTC,jual,0.006,1.610.000.000,"29.946",ambil sebagian untung,,
2026-06-01,SOL,beli,5,"2.100.000",15.750,tambah,,
2026-06-20,ETH,jual,0.6,"55.250.000,50",9.945,butuh dana usaha,,
2026-07-15,SOL,jual,12,"2.300.000",41.400,kurangi,,
2026-08-18,BTC,jual,0.005,1.490.000.000,"22.350",,,
2026-09-05,BTC,beli,0.002,1505000000,6.020,DCA lanjut,,
```

## Output (mengikuti SKILL.md Langkah D)
Perintah: `python3 scripts/hitung_pl_jurnal.py --jurnal kripto/JURNAL.csv --hari-ini 2026-09-24` → exit 0, 12 baris terhitung, **0 baris bermasalah**.

**Untung/rugi yang sudah terealisasi (FIFO, sudah termasuk biaya beli & jual)**

| Tgl jual | Koin | Jumlah | Hasil jual bersih | Modal (FIFO) | Untung/Rugi | % |
|---|---|---|---|---|---|---|
| 05-05-2026 | BTC | 0,006 | Rp 9.630.054 | Rp 8.344.960 | **+Rp 1.285.094** | +15,40% |
| 20-06-2026 | ETH | 0,6 | Rp 33.140.055 | Rp 30.859.255 | **+Rp 2.280.800** | +7,39% |
| 15-07-2026 | SOL | 12 | Rp 27.558.600 | Rp 28.743.050 | **−Rp 1.184.450** | −4,12% |
| 18-08-2026 | BTC | 0,005 | Rp 7.427.650 | Rp 6.980.880 | **+Rp 446.770** | +6,40% |
| | | | | **Total** | **+Rp 2.828.214** | |

**Posisi yang masih dipegang (rata-rata harga perolehan termasuk biaya beli)**
| Koin | Sisa | Rata-rata perolehan | Lot |
|---|---|---|---|
| BTC | 0,006 | Rp 1.405.370.000 | 2 |
| ETH | 0,2 | Rp 48.514.550 | 1 |
| SOL | 3 | Rp 2.103.150 | 1 |

**Pengingat yang Anda tulis sendiri & sudah jatuh tempo**
- BTC (ditulis 10-03-2026, jatuh tempo 01-09-2026): "cek lagi rencana DCA setelah 6 bulan"

Catatan: jual BTC 05-05 memakai lot 10-01 (0,005) + sebagian lot 10-02 (0,001), sesuai urutan FIFO. Pengingat SOL (01-10-2026) belum jatuh tempo.

Angka dari yang Anda catat sendiri. Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

## Verifikasi independen (penguji)
Script terpisah memakai `fractions.Fraction` (FIFO dengan biaya beli dibebankan proporsional per lot, biaya jual dikurangkan dari hasil jual):
```
2026-05-05 BTC proceeds 9630054.0  cost 8344960.0  pl 1285094.0  pct 15.3996
2026-06-20 ETH proceeds 33140055.3 cost 30859255.0 pl 2280800.3  pct 7.391
2026-07-15 SOL proceeds 27558600.0 cost 28743050.0 pl -1184450.0 pct -4.1208
2026-08-18 BTC proceeds 7427650.0  cost 6980880.0  pl 446770.0   pct 6.3999
total 2828214.3
BTC 0.006 1405370000.0 | ETH 0.2 48514550.0 | SOL 3.0 2103150.0
```
**Semua angka cocok** (selisih hanya pembulatan ke rupiah terdekat). Parsing "20.700"→20.700, "7.800"→7.800, "6.020"→6.020, "55.250.000,50"→55.250.000,5 benar.

## Uji data rusak (hitung_pl_jurnal.py)
| Kasus | Hasil | Nilai |
|---|---|---|
| `jumlah_koin` "0,005" (format ID) | baris ditolak: `could not convert string to float: '0,005'` | ⚠️ pesan Inggris teknis; harga boleh format ID tapi jumlah tidak |
| biaya "abc", tanggal 2026-13-40, aksi "tahan", jumlah −1, harga "1,5 M" | masing-masing masuk `baris_bermasalah`, baris lain tetap dihitung | ✅ |
| Jual 1 ETH tanpa beli | ditandai "melebihi stok", tapi tetap muncul baris realized berisi 0 | ⚠️ kecil |
| Jual 0,02 BTC, stok 0,01 | P/L dihitung untuk 0,01 (biaya jual diprorata), kekurangan dilaporkan | ✅ |
| File kosong 0 byte | exit 1, pesan "File jurnal **tidak ditemukan**" | ⚠️ pesan salah |
| Header saja | exit 1 "Jurnal kosong" | ✅ |
| CSV pemisah `;` (default Excel lokal Indonesia) | exit 1 "kolom wajib hilang: tanggal, koin, …" | ⚠️ membingungkan awam |
| File ANSI/cp1252 | exit 1 JSON "codec can't decode" | ✅ (tidak crash) |
| `--hari-ini 24-09-2026` | **traceback** Python | ⚠️ |

## Catatan penguji
- Hitungan FIFO benar dan konsisten; format hasil jelas; pengingat dikutip persis tanpa opini — sesuai batas skill.
- Permintaan "untung/rugi **bulan ini**" tidak didukung langsung script (tidak ada filter periode) — agent harus menjumlah sendiri dari `realized_per_koin`, padahal SKILL.md melarang "hitung ulang manual".
- PPh final 0,21% yang dipungut exchange (PMK 50/2025) tidak disebut — member tidak diberi tahu apakah kolom `biaya` sebaiknya memasukkan PPh.
