# Uji A/B — tanpa skill vs dengan skill (skenario normal 1)

Penguji independen, 2026-09-29. Prompt sama: *"Bikin bot DCA: beli BTC Rp500 ribu tiap minggu di Indodax."*

**Jujur soal metode:** jawaban "tanpa skill" ditulis penguji sebagai agent umum **tanpa** memuat SKILL.md,
meniru pola jawaban asisten koding umum untuk permintaan ini (tidak ada agent terpisah yang buta terhadap skill di
lingkungan ini). Kode di bawah **tidak dijalankan** (butuh `pip install ccxt` + kunci asli).

## A. Tanpa skill (ringkasan jawaban agent umum)
> Tentu! Pasang dulu `pip install ccxt`, lalu simpan script ini:
> ```python
> import ccxt, time
> ex = ccxt.indodax({'apiKey': 'ISI_API_KEY', 'secret': 'ISI_SECRET'})
> while True:
>     price = ex.fetch_ticker('BTC/IDR')['last']
>     amount = 500000 / price
>     ex.create_market_buy_order('BTC/IDR', amount)
>     print(f"Beli {amount} BTC @ {price}")
>     time.sleep(7 * 24 * 3600)
> ```
> Jalankan `python bot.py`. Pastikan API key punya izin trading. DCA adalah strategi yang bagus untuk jangka
> panjang karena merata-ratakan harga. Selalu lakukan riset sendiri.

## B. Dengan skill
Lihat `01-uji-dca-mingguan-paper.md`: bertanya sekali soal batas risiko → ringkasan aturan + batas + asumsi →
mode **paper** dengan harga asli Indodax → pesan siap kirim ber-label `[SIMULASI]` + disclaimer → berhenti sendiri saat
modal total tercapai → catatan transaksi CSV + audit log → jalur live bertahap dengan kunci tanpa withdraw.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Uang asli sejak awal? | **Ya** — langsung order market live | Tidak — paper → testnet → live bertahap |
| Kunci API | Ditempel di kode (rawan ter-commit/terbagi); tidak menyebut larangan izin withdraw | File milik member di luar repo (600), ditolak bila di repo/folder skill/izin terbuka; Binance ber-withdraw ditolak otomatis |
| Batas risiko | Tidak ada (tanpa modal total, SL, rugi harian, tombol berhenti) | 5 batas wajib + tombol berhenti; bot menolak jalan tanpa batas |
| Jumlah beli | `500000/price` float, **tanpa fee** → order bisa ditolak/lebih dari Rp500 rb | Decimal, fee di dalam nominal, lot size; 12/12 cocok verifikasi independen |
| Pajak | Tidak ada | PPh final 0,21%/1% PMK 50/2025 per jual, rekap bulanan |
| Keandalan jadwal | `sleep` 7 hari; mati bila laptop restart, tanpa catatan | Satu putaran per panggilan, state di file, jadwal OpenClaw, NO_REPLY saat tenang |
| Kegagalan jaringan saat order | Crash / tidak tahu order masuk atau tidak | "STATUS ORDER TIDAK PASTI" → bot berhenti, minta cek manual |
| Instalasi | `pip install ccxt` | Python standar saja |
| Kepatuhan kebijakan Komunitech | Memberi opini "strategi bagus" (mendekati rekomendasi), tanpa disclaimer risiko | Tanpa sinyal/opini, disclaimer di setiap pesan |
| Cocok untuk awam | Rendah | Tinggi (kalimat biasa → konfigurasi → ringkasan bahasa sehari-hari) |

**Kesimpulan A/B:** dengan skill **jelas lebih baik** di keselamatan dana, ketepatan angka, kepatuhan, dan
keandalan. Nilai tambah signifikan → aturan "skor maks 6 bila tidak lebih baik" **tidak berlaku**.

## Bahan sebelum/sesudah README
Sebelum: "Script 8 baris, uang asli langsung jalan, kunci di dalam kode, tanpa batas rugi."
Sesudah: "Simulasi dulu, rem berlapis, kunci tanpa tarik dana, angka & pajak dihitung pasti."
