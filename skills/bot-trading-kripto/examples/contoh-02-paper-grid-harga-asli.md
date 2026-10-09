# Contoh 02 — Paper trading grid BTC/IDR dengan harga ASLI Indodax (2026-09-29)

> Dijalankan pembuat skill. Harga diambil langsung dari API publik Indodax saat itu (bukan angka karangan). Order DISIMULASIKAN (mode paper). Konfigurasi: `templates/konfigurasi-grid.json` (contoh format).

```
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json
Bot kripto [SIMULASI - bukan uang asli] btc_idr
BELI 0.00016568 BTC @ Rp1.505.899.000 | bayar Rp249.996 (fee Rp499)
  Aturan Anda: grid: harga di pita level 4 (Rp1.500.000.000 s.d. Rp1.525.000.000)
Ringkasan bot: kas Rp1.750.004, koin 0.00016568 BTC, nilai total Rp1.999.501 (harga Rp1.505.899.000), untung/rugi terealisasi Rp0.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]

$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --openclaw   # putaran berikut, harga masih di pita yang sama
NO_REPLY
[kode keluar 0]

$ python3 scripts/berhenti.py --konfigurasi bot/konfigurasi.json --status
Bot btc_idr mode paper | strategi grid
Status: aktif
Kas bot Rp1.750.004 | koin 0.00016568 BTC | modal terpakai Rp249.996 | untung/rugi terealisasi Rp0
Total fee Rp499 | PPh Rp0 | transaksi 1 | putaran 2

$ cat bot/transaksi.csv
waktu,mode,bursa,pasangan,sisi,jumlah_koin,harga,bruto,fee,pajak_pph,bersih,realized_pl,alasan,order_id,sumber_angka,catatan
2026-09-29T16:17:11+07:00,paper,indodax,btc_idr,beli,0.00016568,1505899000,249497,499,0,249996,,grid: harga di pita level 4 (Rp1.500.000.000 s.d. Rp1.525.000.000),SIM-c9fbdff63a,simulasi,

$ python3 scripts/hitung_pajak_biaya.py --transaksi bot/transaksi.csv
{
  "status": "ok",
  "per_bulan": {
    "2026-09": {
      "jumlah_jual": 0,
      "nilai_jual_idr": 0,
      "pph_idr": 0,
      "fee_idr": 499,
      "nilai_beli_idr": 249497
    }
  },
  "baris_bermasalah": [],
  "catatan": "Dasar: PMK 50/2025 (berlaku 1 Agustus 2025), dicek 2026-09-29 di pajak.go.id. Pembulatan belum dicocokkan dengan Coretax. Ini alat bantu hitung, bukan nasihat pajak -- konfirmasi ke konsultan pajak/DJP."
}

$ python3 scripts/hitung_pajak_biaya.py --nilai-jual 15000000 --pajak domestik --fee-persen 0.2
{
  "status": "ok",
  "nilai_jual": 15000000,
  "tarif_pph_persen": "0.2100",
  "pph": 31500,
  "fee": 30000,
  "diterima_bersih": 14938500,
  "catatan": "Dasar: PMK 50/2025 (berlaku 1 Agustus 2025), dicek 2026-09-29 di pajak.go.id. Pembulatan belum dicocokkan dengan Coretax. Ini alat bantu hitung, bukan nasihat pajak -- konfirmasi ke konsultan pajak/DJP."
}
```

Cek manual: PPh 0,21% × Rp15.000.000 = Rp31.500; fee 0,2% = Rp30.000; bersih Rp14.938.500 (sama).
