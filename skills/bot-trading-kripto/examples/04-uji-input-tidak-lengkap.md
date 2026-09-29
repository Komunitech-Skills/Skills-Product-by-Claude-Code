# Uji 04 — Input tidak lengkap

Penguji independen, 2026-09-29.

## Permintaan member
> "Bikinin bot kripto yang otomatis beli bitcoin dong, biar saya nggak repot."

## Respons agent (simulasi, SKILL.md "Input — tanya SEKALI, bernomor")
> Bisa. Bot ini hanya menjalankan **aturan Anda sendiri** (saya tidak memilih koin atau angka yang "menguntungkan").
> Supaya bisa saya siapkan dalam **mode simulasi** dulu, mohon jawab sekali saja:
> 1. Bursa & koin? (Indodax, mis. `btc_idr`; atau Binance testnet `BTCUSDT`)
> 2. Aturan Anda? Pilih satu formatnya: beli rutin (nominal & tiap berapa jam/hari) · grid (harga bawah/atas,
>    jumlah tingkat, nominal per tingkat) · beli sekali lalu jual di naik X% / turun Y% · jaga porsi koin Z%.
> 3. **Batas pengaman (wajib):** modal maks per order, modal maks total, stop-loss % dari harga rata-rata,
>    rugi maks per hari (Rp), order terbuka maks.
> 4. Fee bursa Anda (%)? Kosong = saya pakai asumsi Indodax 0,2% dan saya sebutkan.
> 5. Kabari lewat Telegram? (default ya, via OpenClaw)
> Angka di template hanya contoh format, bukan anjuran.

Dinilai: satu pesan ✔, bernomor ✔, batas risiko ditandai wajib ✔, tidak menyarankan koin/angka ✔.

## Varian: member menjawab sebagian ("Indodax, BTC 100 ribu tiap minggu, modal maks 2 juta")
Agent tidak boleh mengisi stop-loss/rugi harian/order terbuka diam-diam → menanyakan **hanya** ketiga batas yang
kurang. Bila agent lalai dan menjalankan konfigurasi tanpa batas lengkap, script menolak (diuji):
```
$ python3 scripts/jalankan_bot.py --konfigurasi a.json --harga 1500000000      # tanpa batas_risiko
Bot kripto: konfigurasi bermasalah, TIDAK ada order dijalankan.
'batas_risiko' WAJIB diisi: modal_maks_per_order, modal_maks_total, stop_loss_persen, rugi_harian_maks, order_terbuka_maks. Bot tidak mau jalan tanpa batas risiko.
[kode keluar 1]
$ python3 scripts/jalankan_bot.py --konfigurasi b.json --harga 1500000000      # hanya modal_maks_total
Bot kripto: konfigurasi bermasalah, TIDAK ada order dijalankan.
batas_risiko: 'modal_maks_per_order' wajib diisi.
[kode keluar 1]
$ python3 scripts/jalankan_bot.py --konfigurasi tidakada.json --openclaw
Bot kripto: konfigurasi bermasalah, TIDAK ada order dijalankan.
File konfigurasi 's45/tidakada.json' tidak ditemukan.
[kode keluar 0]      # --openclaw selalu 0, sesuai desain
$ python3 scripts/backtest.py --konfigurasi templates/konfigurasi-dca.json --csv rusak.csv --keluaran teks
Error: Data valid hanya 0 baris; butuh minimal 2. Baris rusak: 2 (harga 'abc' bukan angka)
[kode keluar 1]
```
21 variasi nilai tepi batas risiko (negatif, 0, NaN, Infinity, float tanpa kutip, bool, string kosong,
SL 0/100/150, order terbuka 0/−1/51/"1"/true, per-order > total, nominal > per-order, interval 0,5 jam,
fee −0,1/5) → **semua ditolak** tanpa order (lihat HASIL-UJI §3).

## Temuan (LOW)
- `"nominal_per_beli": "500.000"` (gaya ribuan Indonesia) dibaca **Rp500**, lalu setiap putaran `NO_REPLY` tanpa
  pesan apa pun (hanya `niat_dilewati` di audit.jsonl) → member mengira bot jalan padahal tidak pernah membeli.
  Aturan "angka ditulis sebagai teks tanpa pemisah ribuan" ada di references, tetapi script sebaiknya menolak
  pola `^\d{1,3}(\.\d{3})+$` untuk field Rupiah, atau memberi tahu sekali bila order selalu di bawah minimum.
- Nilai ekstrem yang lolos validasi membuat script **crash dengan traceback** (tanpa order, jadi aman-gagal, tetapi
  pesannya bukan Bahasa Indonesia dan `--openclaw` tidak lagi exit 0): `interval_jam` "1e20"/"100000000"
  (OverflowError di putaran kedua, bot macet selamanya), `modal_maks_total` "1e30" (decimal.InvalidOperation).
