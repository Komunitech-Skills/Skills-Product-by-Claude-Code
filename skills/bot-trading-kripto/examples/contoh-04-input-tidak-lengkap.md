# Contoh 04 — Input tidak lengkap / salah (keluaran script asli)

> Dijalankan pembuat skill 2026-09-29. Menunjukkan bahwa bot **menolak jalan** (tanpa order apa
> pun) bila batas risiko tidak lengkap atau input meragukan, dengan pesan Bahasa Indonesia.

## Percakapan yang diharapkan
**Member:** "Bikin bot beli BTC Rp100 ribu tiap minggu di Indodax ya."

**Agent (satu pesan, bernomor):**
> Siap. Sebelum bot dibuat (mulai di mode SIMULASI, tanpa uang asli), saya perlu batas pengaman
> yang Anda tentukan sendiri:
> 1. Modal maksimal total untuk bot ini (Rp)?
> 2. Stop-loss: jual semua & berhenti kalau harga turun berapa % dari harga rata-rata beli?
> 3. Rugi maksimal per hari (Rp) sebelum bot berhenti?
> 4. Jual semua kalau untung berapa %? (boleh kosong)
> 5. Notifikasi ke Telegram lewat OpenClaw? (ya/tidak)
> Angka-angka ini keputusan Anda; saya tidak menyarankan angka tertentu.

## Keluaran script
```
$ python3 scripts/jalankan_bot.py --konfigurasi tanpa-batas.json
Bot kripto: konfigurasi bermasalah, TIDAK ada order dijalankan.
'batas_risiko' WAJIB diisi: modal_maks_per_order, modal_maks_total, stop_loss_persen, rugi_harian_maks, order_terbuka_maks. Bot tidak mau jalan tanpa batas risiko.
[kode keluar 1]

$ python3 scripts/jalankan_bot.py --konfigurasi float.json
Bot kripto: konfigurasi bermasalah, TIDAK ada order dijalankan.
'strategi.nominal_per_beli' tulis sebagai teks, mis. "100000.0" (pakai tanda kutip) supaya presisi terjaga.
[kode keluar 1]

$ python3 scripts/jalankan_bot.py --konfigurasi binance-live.json
Bot kripto: konfigurasi bermasalah, TIDAK ada order dijalankan.
Mode live di Binance global ditolak: Binance global tidak tercantum di daftar PAKD berizin OJK (cek ojk.go.id) dan PPh-nya 1%. Pakai Indodax (PAKD berizin) untuk live, atau tambahkan "saya_paham_binance_bukan_pakd_ojk": true bila Anda tetap memilihnya dengan sadar.
[kode keluar 1]

$ python3 scripts/backtest.py --konfigurasi templates/konfigurasi-dca.json --csv rusak.csv --keluaran teks
Error: Data valid hanya 1 baris; butuh minimal 2. Baris rusak: 3 (harga 'abc' bukan angka)
[kode keluar 1]

$ python3 scripts/hitung_pajak_biaya.py --nilai-jual lima-juta
{"status": "error", "pesan": "nilai jual 'lima-juta' bukan angka"}
[kode keluar 1]
```
