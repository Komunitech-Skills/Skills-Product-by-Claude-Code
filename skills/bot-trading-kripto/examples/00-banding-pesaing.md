# Uji banding pesaing (skenario normal 1: DCA mingguan BTC Rp500 ribu)

Penguji independen, 2026-09-29. Pesaing hanya **dibaca untuk dinilai** (dokumentasi resmi), tidak disalin,
tidak dipasang (butuh Docker/pip & kunci).

## Pesaing yang dicari
| Sumber | Kata kunci | Temuan |
|---|---|---|
| Freqtrade (GPL-3.0, ±55 rb bintang) | docs quickstart & configuration | https://www.freqtrade.io/en/stable/ , /configuration/ |
| Hummingbot (Apache-2.0, ±20 rb bintang) | docs (dirujuk di research/sources/bot-trading-2026-09-29.md) | Fokus market making; berat (Docker/conda), tidak dinilai rinci |
| ClawHub / skill OpenClaw | "crypto trading bot skill", "DCA grid binance skill" | `binance-spot-trader` (srikanthbellary, MIT, ±1,7 rb unduhan): "autonomous … LLM-powered market analysis", momentum/mean reversion/DCA; halaman katalog tanpa info batas risiko/paper/izin withdraw (https://clawbot.ai/skills/binance-spot-trader.html). Juga ada peringatan skill kripto berbahaya di ClawHub (opensourcemalware.com, "clawdbot-skills-ganked-your-crypto"). |

Skill ClawHub tersebut memberi **analisis pasar/sinyal oleh LLM** → bertentangan langsung dengan keputusan pemilik
2026-09-29 (tanpa sinyal) sehingga bukan pembanding yang setara; pembanding terkuat = **Freqtrade**.

## Skenario 1 dengan Freqtrade (menurut dokumentasi resmi)
Member harus: pasang Python ≥3.11 + Docker/pip + TA-Lib (docs "Installation Requirements", min. 2 GB RAM),
menulis strategi Python (DCA mingguan = strategi kustom / `adjust_trade_position`), mengisi `config.json`
(`dry_run: true` bawaan, `dry_run_wallet` bawaan 1000, `stake_amount`, `max_open_trades`, `stoploss` wajib),
kunci di `exchange.key/secret` atau env `FREQTRADE__EXCHANGE__KEY`. Indodax **tidak** tercantum di daftar bursa
yang didukung resmi Freqtrade (Binance, Bybit, OKX, Kraken, …).

## Penilaian berdampingan (1–5)
| Kriteria | Freqtrade | bot-trading-kripto | Catatan |
|---|---|---|---|
| Default simulasi | 5 (dry_run true) | 5 (paper; live bertahap) | seri |
| Backtest | 5 (lengkap, indikator, hyperopt) | 3 (candle harian, isi di harga tutup) | Freqtrade unggul |
| Batas risiko | 4 (stoploss, max_open_trades, plugin Protections) | 4 (5 batas wajib + tombol STOP; ada bypass jam mundur, lihat HASIL-UJI) | seri setelah perbaikan |
| Perlindungan kunci | 2 (docs konfigurasi tidak membahas izin withdraw) | 4 (tolak withdraw Binance, file 600 di luar repo, penyamar log; Indodax manual; redirect bocor key, lihat HASIL-UJI) | skill unggul |
| Bursa Indonesia (Indodax, PAKD OJK) | 1 (tidak didukung resmi) | 5 | skill unggul |
| Pajak Indonesia (PMK 50/2025) | 1 | 4 (jual benar; sisi swap USDT belum) | skill unggul |
| Kemudahan untuk awam | 1 (Docker, Python, tulis strategi) | 4 (kalimat biasa, Python standar) | skill unggul |
| Kepatuhan "tanpa sinyal" | 3 (netral, tapi komunitas strategi) | 5 | skill unggul |
| Kematangan & uji lapangan | 5 (sejak 2017, ribuan pengguna) | 2 (order bertanda tangan baru diuji di server tiruan) | Freqtrade unggul |

**Kesimpulan:** untuk target pembeli Komunitech (awam, Indodax, Rupiah, pajak lokal, tanpa sinyal), skill
**menang** di skenario 1. Freqtrade unggul di kedalaman backtest dan kematangan — sudah ditangani dengan benar oleh
`references/jalur-lanjutan-freqtrade.md` (dirujuk, tidak dibundel/disalin). Pelajaran yang layak ditulis ulang
dengan cara sendiri: (1) *protections* bergaya Freqtrade — jeda otomatis setelah N stop-loss beruntun;
(2) laporan backtest dengan jumlah hari/putaran bot aktif. Skill tidak kalah → aturan skor maks 6 tidak berlaku.
