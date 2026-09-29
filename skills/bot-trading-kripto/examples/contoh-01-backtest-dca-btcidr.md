# Contoh 01 — Backtest DCA mingguan BTC/IDR pada data asli Indodax (setahun)

> Dibuat pembuat skill (bukan penguji independen), 2026-09-29. Data: `tests/data/btcidr-harian-2025-2026.csv`, diunduh dari API publik Indodax (`scripts/ambil_candle.py`) pada 2026-09-29. Konfigurasi: `templates/konfigurasi-dca.json` (angka hanya contoh format, BUKAN anjuran).

**Permintaan member:** "Backtest aturan saya: beli BTC Rp100 ribu tiap minggu, modal maksimal Rp2 juta, jual semua kalau untung 30%, stop-loss 25%, rugi harian maks Rp300 ribu."

```
$ python3 scripts/backtest.py --konfigurasi bot/konfigurasi.json --csv tests/data/btcidr-harian-2025-2026.csv --keluaran teks
UJI MUNDUR (backtest) btc_idr - strategi dca - 2025-09-29 s.d. 2026-09-29 (366 baris)
Modal bot: Rp2.000.000 -> akhir Rp1.344.864 (-32.76%)
Untung/rugi terealisasi: -Rp655.136 | koin tersisa 0 BTC
Transaksi: 20 | total fee Rp6.300 | PPh Rp2.624
Penurunan terdalam (drawdown): 33.02%
Bot berhenti: STOP-LOSS: harga Rp1.063.498.000 sudah 25% atau lebih di bawah harga rata-rata beli Rp1.616.605.684. Posisi dijual & bot berhenti.
Pembanding faktual beli sekali & tahan: Rp1.575.171 (-21.24%)
Catatan: Hasil masa lalu tidak menjamin hasil masa depan.
Catatan: Order diasumsikan terisi di harga penutupan tiap baris; slippage & likuiditas tidak dimodelkan.
Catatan: Pembanding 'beli sekali & tahan' hanya fakta historis, bukan rekomendasi.
Catatan: PMK 50/2025 (berlaku 1 Agustus 2025): PPh 22 final 0,21% (PAKD dalam negeri) / 1% (platform luar negeri) dari nilai jual, dipungut dari penjual. Dicek 2026-09-29 di pajak.go.id. Pembulatan belum dicocokkan dengan Coretax.
```

**Cuplikan transaksi (JSON `transaksi`)** — 3 pertama & 2 terakhir:
```
{"waktu": "2025-09-29", "sisi": "beli", "harga": "1908238000", "jumlah_koin": "0.00005229", "bersih": "99982", "fee": "200", "pph": "0", "realized_pl": "", "alasan": "DCA terjadwal tiap 168 jam"}
{"waktu": "2025-10-06", "sisi": "beli", "harga": "2066398000", "jumlah_koin": "0.00004829", "bersih": "99986", "fee": "200", "pph": "0", "realized_pl": "", "alasan": "DCA terjadwal tiap 168 jam"}
{"waktu": "2025-10-13", "sisi": "beli", "harga": "1921600000", "jumlah_koin": "0.00005193", "bersih": "99989", "fee": "200", "pph": "0", "realized_pl": "", "alasan": "DCA terjadwal tiap 168 jam"}
{"waktu": "2026-02-02", "sisi": "beli", "harga": "1327739000", "jumlah_koin": "0.00007516", "bersih": "99993", "fee": "200", "pph": "0", "realized_pl": "", "alasan": "DCA terjadwal tiap 168 jam"}
{"waktu": "2026-02-05", "sisi": "jual", "harga": "1063498000", "jumlah_koin": "0.0011752", "bersih": "1244699", "fee": "2500", "pph": "2624", "realized_pl": "-655136", "alasan": "stop-loss global"}
```

**Cek angka manual (jual stop-loss 2026-02-05):** 0,0011752 BTC × Rp1.063.498.000 = Rp1.249.822,85 → bruto Rp1.249.823;
fee 0,2% = Rp2.499,65 → Rp2.500; PPh 0,21% = Rp2.624,63 → dibulatkan ke bawah Rp2.624;
bersih = 1.249.823 − 2.500 − 2.624 = **Rp1.244.699** (sama dengan script).

**Cara agent menyampaikan (sesuai SKILL.md):** angka di atas apa adanya + catatan keterbatasan.
Agent TIDAK menyimpulkan "strategi ini buruk/bagus" dan TIDAK mengusulkan angka stop-loss lain.
Bila member ingin mencoba variasi, member yang menyebut angkanya.
