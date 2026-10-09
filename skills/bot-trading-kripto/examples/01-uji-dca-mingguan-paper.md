# Uji 01 — Normal: DCA mingguan BTC Rp500 ribu, mode paper

Penguji independen (Tahap 6), 2026-09-29. Skill diuji dari salinan di scratchpad (bukan folder repo).
Agent disimulasikan oleh penguji dengan mengikuti SKILL.md. Tanpa uang/kunci asli.

## Permintaan member
> "Bikin bot DCA: beli BTC Rp500 ribu tiap minggu di Indodax, mode simulasi dulu."

## Respons agent (simulasi, mengikuti SKILL.md "Input — tanya SEKALI")
Batas risiko tidak disebut → wajib ditanyakan (SKILL.md: satu-satunya hal yang tidak boleh diisi diam-diam):

> Siap, saya siapkan dalam **mode simulasi (paper)**, tanpa uang asli. Satu hal wajib sebelum mulai — batas pengaman Anda:
> 1. Modal maksimal total untuk bot ini (Rp)?
> 2. Stop-loss: turun berapa % dari harga rata-rata beli, bot jual semua & berhenti?
> 3. Rugi maksimal per hari (Rp) sebelum bot berhenti?
> 4. Order terbuka maksimal (bila ragu: 1)?
> 5. Fee: saya pakai asumsi Indodax 0,2% kecuali Anda punya angka lain. Notifikasi Telegram: ya/tidak?

Jawaban member (simulasi): modal total Rp6 juta, stop-loss 20%, rugi harian Rp1 juta, order terbuka 1, fee 0,2%.

Ringkasan yang ditunjukkan agent sebelum jalan: Aturan Anda = beli Rp500.000 tiap 168 jam di btc_idr ·
Batas pengaman = per order Rp500.000, total Rp6.000.000, stop-loss 20%, rugi harian Rp1.000.000, order terbuka 1 ·
Asumsi = fee 0,2%, PPh jual 0,21% (PMK 50/2025). Member: "ya".

## Eksekusi (script skill, harga ASLI Indodax untuk putaran pertama)
```
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json
Bot kripto [SIMULASI - bukan uang asli] btc_idr
BELI 0.00033196 BTC @ Rp1.503.159.000 | bayar Rp499.987 (fee Rp998)
  Aturan Anda: DCA terjadwal tiap 168 jam
Ringkasan bot: kas Rp5.500.013, koin 0.00033196 BTC, nilai total Rp5.999.002 (harga Rp1.503.159.000), untung/rugi terealisasi Rp0.
Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, ...
[kode keluar 2]
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json      # putaran berikut, belum 168 jam
NO_REPLY
[kode keluar 0]
```
Lalu 12 minggu disimulasikan dengan `--harga`/`--sekarang` (hanya boleh di mode paper; harga contoh buatan penguji):
11 pembelian lagi, lalu putaran ke-13 (modal terpakai Rp5.999.905 + Rp500.000 > Rp6.000.000):
```
BOT BERHENTI. Alasan: BATAS MODAL TOTAL: modal terpakai Rp5.999.905 + order Rp500.000 > Rp6.000.000. Bot berhenti membeli.
Tidak ada order baru sampai Anda meninjau dan melanjutkan (berhenti.py --lanjutkan).
[kode keluar 3]
```
Status akhir (`berhenti.py --status`): kas Rp95 | koin 0.00410994 BTC | modal terpakai Rp5.999.905 | fee Rp11.976 | 12 transaksi.

Catatan perilaku: tick 2026-10-06 09:00 tidak membeli karena beli pertama 2026-09-29 16:21 + 168 jam belum lewat
(jadwal DCA bergeser mengikuti jam beli pertama; benar sesuai spesifikasi "≥ interval_jam sejak beli terakhir").

## Verifikasi angka independen (Decimal, `uji_batas.py` penguji)
Rumus penguji: jumlah = ⌊(500.000/1,002)/harga⌋ ke 0,00000001; bruto = bulat(jumlah×harga); fee = bulat(jumlah×harga×0,2%); bayar = bruto+fee ≤ 500.000.
**12/12 transaksi cocok** (jumlah koin, bruto, fee, bayar). Contoh: @1.503.159.000 → 0,00033196 BTC, bruto 498.989, fee 998, bayar 499.987.

## Penilaian
| Kriteria | Hasil |
|---|---|
| Batas risiko ditanyakan, tidak diisi diam-diam | Ya |
| Default paper, label [SIMULASI] | Ya |
| Angka dari script, cocok independen | 12/12 |
| Disclaimer di setiap pesan | Ya |
| Batas modal total menghentikan bot dengan alasan jelas | Ya |
| Temuan | Tidak ada di skenario ini (lihat HASIL-UJI untuk temuan lapisan risiko) |
