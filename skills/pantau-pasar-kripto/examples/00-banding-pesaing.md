# 00 — Uji banding pesaing

Dicari 2026-09-24 (hanya DIBACA, tidak ada script pihak ketiga yang dijalankan, tidak ada teks yang disalin ke skill kita).

## Pencarian
- ClawHub API `clawhub.ai/api/v1/search`: "crypto price alert", "crypto portfolio", "crypto trading journal", "bitcoin", "crypto", "crypto trading bot", "binance trade", "indodax".
- Web: "clawhub crypto price alert skill SKILL.md", awesome-openclaw-skills (VoltAgent), skills.sh/clawskills.sh.
- Hasil "indodax" & "crypto trading journal": **tidak ada** skill yang relevan. Tidak ditemukan skill berbahasa Indonesia.

## Pesaing terpilih (paling populer & relevan)
| Skill | URL | Popularitas | Lisensi | Catatan |
|---|---|---|---|---|
| **portfolio-watcher** (clawd-team / jhillin8) | clawhub.ai/jhillin8/skills/portfolio-watcher | 10.201 unduhan, 309 instal, 7 ★ | tidak dicantumkan | SKILL.md hanya contoh kalimat; tidak ada script, sumber data, atau langkah kerja. |
| **Crypto Market** (manifoldor/crypto) | clawhub.ai/manifoldor/skills/crypto | 4.790 unduhan, 142 instal, 17 ★ | MIT-0 | Script CCXT (`pip install ccxt`), default Binance, alert above/below/%, pasangan USDT. |

Pesaing lain yang dicatat (tidak dibandingkan, **berisiko**): `srikanthbellary/binance-spot-trader` (5.071 unduhan, "Autonomous Binance spot trading bot" — **auto-trading, butuh API key**), `katrina-jpg/crypto-trading-bot` (8.404 unduhan, pembuatan bot auto-trade + API CEX/DEX), `june-kris/binance-trade-hunter` ("pump detection, one-click trading"), `vamzi/alpaca` (menempatkan order). Semua bertentangan dengan keputusan pemilik (tanpa auto-trading).

## Skenario 01 dijalankan dengan instruksi pesaing (berperan sebagai agent)
**portfolio-watcher:** agent hanya bisa "tell Clawd what you own" + "Alert me if AAPL hits $200". Tidak ada mekanisme penjadwalan, sumber data, atau aturan jika gagal; ambang persen 24 jam & Rupiah tidak dijelaskan. Output realistis: "Oke, saya akan kabari kalau BTC di bawah Rp 1,45 M" — **janji tanpa mekanisme** (tidak ada proses yang benar-benar memantau). Berita: tidak dicakup. Tips menyebut "Ask 'portfolio allocation'" (pie chart, bukan saran).
**Crypto Market:** `alert-add BTC/USDT below …` dalam **USDT**, bukan Rupiah; tidak ada IDR/Indodax; harus `pip install ccxt`; `alert-check` harus dijalankan manual/cron; tidak ada notifikasi Telegram bawaan, tidak ada disclaimer, tidak ada ringkasan berita, tidak ada penanganan data basi/cache. Contoh skenario memakai istilah "support/resistance", "breaks previous high" (nuansa sinyal trading).

## Penilaian (1–5)
| Kriteria | pantau-pasar-kripto (kita) | portfolio-watcher | Crypto Market (CCXT) |
|---|---|---|---|
| Kualitas output skenario 01 | 4 | 1 | 3 |
| Konteks Indonesia (Rp, Indodax, OJK, WIB, bahasa) | 5 | 1 | 1 |
| Akurasi & kejujuran data | 4 (diverifikasi; celah cache/429) | 1 (tanpa sumber) | 3 (data exchange nyata) |
| Siap pakai awam (tanpa install) | 4 | 3 | 2 (pip + CLI) |
| Keamanan & batas etika | 5 | 3 | 3 |
| **Total** | **22** | 9 | 12 |

**Skill kita menang jelas.**

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- Crypto Market: menyimpan alert sebagai daftar dengan **ID & status (monitoring/terpicu)** → ide untuk kita: simpan status "sudah dikabari" per ambang di `state.json` supaya notifikasi tidak berulang tiap jam.
- Crypto Market: sekali panggil untuk banyak pasangan / pilihan bursa → ide: **satu permintaan CoinGecko untuk semua koin** (`ids=a,b,c`) agar tidak kena rate limit 429 (terbukti terjadi di uji kita).
- portfolio-watcher: input bahasa natural "saya punya 0,5 BTC di harga X" langsung jadi catatan → ide: agent bisa menambah baris jurnal dari kalimat biasa (dengan konfirmasi).
