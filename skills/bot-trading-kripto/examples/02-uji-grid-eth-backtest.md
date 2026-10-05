# Uji 02 — Normal: grid ETH, backtest pada data sintetis + data publik

Penguji independen, 2026-09-29. Tanpa uang/kunci asli.

## Permintaan member
> "Pasang grid ETH antara Rp42 juta dan Rp58 juta, 8 tingkat, Rp500 ribu per tingkat. Modal total Rp4 juta,
> stop-loss 15%, rugi harian maks Rp1 juta, order terbuka 2. Backtest dulu."

Agent (simulasi): semua batas risiko sudah disebut → tidak perlu bertanya. Konfigurasi dari
`templates/konfigurasi-grid.json` (mode paper, `eth_idr`, fee asumsi Indodax 0,2% — disebut sebagai asumsi).
Validasi script: 8 × Rp500.000 = Rp4.000.000 ≤ modal total → lolos.

## Data
1. **Sintetis milik penguji** (`gen_sintetis.py`, deterministik): 150 hari ETH/IDR berosilasi Rp42–58 jt, lalu jatuh
   tajam mulai hari ke-130; ditambah 4 baris rusak (tanggal 2026-13-45, harga `abc`, harga `-5`, baris kosong).
2. **Publik**: `scripts/ambil_candle.py --bursa indodax --pasangan eth_idr --hari 180` → 181 baris
   (2026-04-02 s.d. 2026-09-29), dipanggil sungguhan hari ini.

## Hasil script (apa adanya)
```
UJI MUNDUR (backtest) eth_idr - strategi grid - 2026-01-01 s.d. 2026-05-30 (150 baris)   [SINTETIS]
Modal bot: Rp4.000.000 -> akhir Rp3.482.101 (-12.95%)
Untung/rugi terealisasi: -Rp517.899 | koin tersisa 0 ETH
Transaksi: 14 | total fee Rp18.980 | PPh Rp9.449
Penurunan terdalam (drawdown): 14.24%
Bot berhenti: STOP-LOSS: harga Rp42.897.000 sudah 15% atau lebih di bawah harga rata-rata beli Rp51.033.189. Posisi dijual & bot berhenti.
Pembanding faktual beli sekali & tahan: Rp2.307.385 (-42.32%)
Baris CSV dilewati: 4 (lihat keluaran JSON)
Catatan: Hasil masa lalu tidak menjamin hasil masa depan. ... slippage & likuiditas tidak dimodelkan. ... PMK 50/2025 ...

UJI MUNDUR (backtest) eth_idr - strategi grid - 2026-04-02 s.d. 2026-09-29 (181 baris)   [PUBLIK INDODAX]
Modal bot: Rp4.000.000 -> akhir Rp4.103.529 (2.59%)
Untung/rugi terealisasi: Rp103.065 | koin tersisa 0.01018205 ETH
Transaksi: 17 | total fee Rp17.235 | PPh Rp8.659
Penurunan terdalam (drawdown): 0.92%
Bot berhenti: tidak
Pembanding faktual beli sekali & tahan: Rp5.532.794 (38.32%)
```
Keempat baris rusak dilaporkan per nomor baris dengan alasan (JSON `baris_rusak`), proses tidak berhenti.

Respons agent (simulasi): menyajikan angka di atas apa adanya + catatan keterbatasan; **tidak** menyimpulkan
"grid bagus/buruk" dan tidak mengusulkan rentang lain (SKILL.md Langkah B.3). Pembanding beli-tahan disebut
"fakta historis, bukan rekomendasi".

## Verifikasi independen
- **Level grid** (penguji): langkah (58−42)/8 = Rp2 jt → 42, 44, …, 58 jt. Uji batas (`uji_batas.py`):
  beli tepat di Rp44.000.000 (pita [44,46)) ✔; Rp45.999.999 tidak memicu ✔; Rp46.000.000 memicu jual slot 1 lalu beli
  slot 2 ✔; di bawah harga_bawah dan tepat di harga_atas tidak membeli ✔.
- **Mesin independen** (`verif_independen.py`, ditulis dari `references/strategi-dan-konfigurasi.md`, tidak
  mengimpor `inti.py`): grid sintetis 14/14 transaksi, grid publik 17/17 transaksi cocok (jumlah koin, fee, PPh,
  bersih, untung/rugi, kas/koin/fee/PPh akhir). Bersama 5 konfigurasi lain (DCA+TP BTC setahun, TP/SL, rebalancing
  BTCUSDT PPh 1%, DCA harian ETH ×2): **110 transaksi, 0 selisih**.
- **Stop-loss global** di data sintetis: rata-rata tertimbang Rp51.033.189 × 0,85 = Rp43.378.211 ≥ Rp42.897.000 → terpicu ✔.
  PPh jual SL: bruto = bersih 2.929.934 + fee 5.884 + PPh 6.178 = 2.941.996; ⌊2.941.996 × 0,21%⌋ = ⌊6.178,19⌋ = Rp6.178 ✔;
  fee = bulat(2.941.996 × 0,2%) = Rp5.884 ✔.

## Catatan untuk pembuat (LOW, UX)
- Di data sintetis, stop-loss global 15% (dari rata-rata semua slot) terpicu **di dalam** rentang grid
  (Rp42,9 jt > harga_bawah Rp42 jt). Sesuai aturan, tetapi member grid mungkin tidak menyadarinya → ringkasan
  konfigurasi sebaiknya memberi peringatan bila `rata-rata × (1−SL%)` bisa jatuh di atas `harga_bawah`.
- Untung/rugi per jual grid memakai rata-rata tertimbang **seluruh** posisi, bukan harga beli slot itu:
  data publik 2026-09-24 slot dibeli Rp47.890.000 dijual Rp48.223.000 tetapi tercatat **rugi Rp5.357**. Metode
  terdokumentasi (references), total tetap benar, tetapi membingungkan pemakai grid → sebutkan di pesan.
