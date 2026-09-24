# 01 — Pantau BTC, ETH, SOL + ambang % & Rp + ringkasan pagi (data NYATA)

**Skenario:** S1 normal. Member VIP (pemakai OpenClaw) ingin dipantau 3 koin dengan ambang persen dan ambang harga Rupiah, plus ringkasan pagi berita bersumber. Diuji 2026-09-24 ±07:37–07:45 WIB dengan jaringan sungguhan (CoinGecko + Indodax), lalu dengan `--harga-file`.

## Input pengguna (persis)
> tolong pantau BTC, ETH sama SOL ya. kabarin kalau turun 5% atau naik 8%. terus BTC kalau di bawah 1,45 M, ETH kalau tembus 55 juta, SOL kalau di bawah 2,1 juta kabarin juga. tiap jam 7 pagi kirim ringkasan harga + berita ke telegram saya

## Output (mengikuti SKILL.md Langkah A → B)

**Pesan 1 — konfirmasi terjemahan (Langkah A.1)**

Siap. Sebagian sudah jelas, sisanya saya pakai default (bisa diubah kapan saja):
- Persen dihitung dari **perubahan 24 jam** (Anda tidak menyebut harga beli sebagai acuan).
- Kata kunci berita: nama koin saja (bitcoin, ethereum, solana).
- Ringkasan pagi 07:00 WIB via Telegram.

`kripto/PANTAU.md`
| Koin | Ambang naik | Ambang turun | Harga acuan | Kata kunci berita | Jam ringkasan pagi |
|---|---|---|---|---|---|
| BTC | 8% | 5% | (kosong — 24 jam terakhir) · di bawah Rp 1.450.000.000 | bitcoin | 07:00 WIB |
| ETH | 8% | 5% | (kosong) · di atas Rp 55.000.000 | ethereum | 07:00 WIB |
| SOL | 8% | 5% | (kosong) · di bawah Rp 2.100.000 | solana | 07:00 WIB |

`kripto/konfigurasi.json`
```json
{"koin":[
 {"kode":"BTC","coingecko_id":"bitcoin","mata_uang":"idr","ambang_naik_persen":8,"ambang_turun_persen":5,"ambang_harga_di_bawah":1450000000},
 {"kode":"ETH","coingecko_id":"ethereum","mata_uang":"idr","ambang_naik_persen":8,"ambang_turun_persen":5,"ambang_harga_di_atas":55000000},
 {"kode":"SOL","coingecko_id":"solana","mata_uang":"idr","ambang_naik_persen":8,"ambang_turun_persen":5,"ambang_harga_di_bawah":2100000}
]}
```
Sudah benar? (ya / ubah …)

**Pesan 2 — hasil cek pertama (member menjawab "ya")**

Perintah: `python3 scripts/cek_ambang.py --konfigurasi kripto/konfigurasi.json --state kripto/state.json` → **exit 2** (ada ambang terlewati).

```
Pantau harga kripto -- 24 Sep 2026 07:41 WIB
- BTC: Rp 1.505.467.218 (-2.52% / 24 jam)
- ETH: Rp 47.945.407 (-2.78% / 24 jam)
- SOL: Rp 2.056.215 (-3.22% / 24 jam)
  >> AMBANG TERLEWATI: Harga sudah <= ambang bawah 2100000.
Sumber & jam data ada di rincian JSON. Informasi, bukan nasihat investasi.
```
Sumber: CoinGecko `simple/price`, jam data 24 Sep 2026 07:39:30 WIB (usia ±2 menit).
Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

**Pesan 3 — contoh ringkasan pagi (Langkah B)**

☀️ **Ringkasan kripto — Kamis, 24 Sep 2026, 07:41 WIB**

**Harga (CoinGecko, data 07:39 WIB)**
- BTC: Rp 1.505.467.218 (−2,52% / 24 jam)
- ETH: Rp 47.945.407 (−2,78% / 24 jam)
- SOL: Rp 2.056.215 (−3,22% / 24 jam) — **ambang Anda terlewati: di bawah Rp 2.100.000**
- Pembanding pasar lokal Indodax (07:37 WIB): BTC Rp 1.506.509.000 · ETH Rp 47.876.000 · SOL Rp 2.052.042

**Berita (3 teratas, bertautan sumber asli)**
1. *CoinDesk, 23 Sep 2026* — Bitcoin naik ±10,9% sepanjang September; bila bertahan, ini tiga bulan naik berturut-turut, pola yang terakhir terjadi pada 2012. Artikel juga mencatat arus masuk ETF spot > US$5,5 miliar sejak Agustus. https://www.coindesk.com/markets/2026/09/23/bitcoin-s-on-a-streak-it-hasn-t-hit-since-2012
2. *Yahoo Finance, 23 Sep 2026* — BTC dibuka US$86.195 dan ETH US$2.753 (dekat level tertinggi 8 bulan), bersamaan dengan rencana pertemuan Trump–Xi di Washington. https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-september-23-2026-crypto-prices-open-near-8-month-highs-is-the-crypto-winter-over-113908671.html
3. *Pluang (dari Blockonomi), 22 Sep 2026* — SOL sempat menyentuh US$117,23 pada 21 Sep (tertinggi sejak Januari 2026); ±US$18 juta posisi short terlikuidasi dalam 24 jam. https://pluang.com/en/news-feed/solana-sol-melonjak-lebih-dari-117-dolar-dengan-liquidasi-paksa-18-juta-dolar

**Kalender peristiwa:** tidak ada yang ditemukan dengan sumber jelas hari ini (tidak ditulis).

Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

**Pesan 4 — jadwal (Langkah E)**
Saya siap membuat 2 jadwal OpenClaw: (1) ringkasan pagi 07:00 WIB, (2) cek ambang tiap jam. Keduanya dikirim ke Telegram Anda (ID chat: 0000000000 — fiktif). Komputer/mesin harus menyala saat jam jadwal. Lanjut? (ya/tidak)

## Uji `--harga-file` (offline, deterministik)
File harga: BTC Rp 1.420.000.000 (−5,7%), ETH Rp 52.000.000 (+8,4%), SOL Rp 2.050.000 (−1,0%) → exit **2**:
```
- BTC: Rp 1.420.000.000 (-5.70% / 24 jam)
  >> AMBANG TERLEWATI: Turun -5.70% (ambang turun 5%).
  >> AMBANG TERLEWATI: Harga sudah <= ambang bawah 1450000000.
- ETH: Rp 52.000.000 (+8.40% / 24 jam)
  >> AMBANG TERLEWATI: Naik +8.40% (ambang naik 8%).
- SOL: Rp 2.050.000 (-1.00% / 24 jam)
  >> AMBANG TERLEWATI: Harga sudah <= ambang bawah 2100000.
```
Semua pemicu benar (dicek manual: −5,7 ≤ −5; 8,4 ≥ 8; 1,42 M ≤ 1,45 M; 2,05 jt ≤ 2,1 jt).

## Catatan penguji
- **Verifikasi harga nyata:** tepat setelah script jalan, endpoint yang sama di-`curl` manual: `bitcoin.idr=1505467218`, `ethereum.idr=47945407`, `solana.idr=2056215`, `last_updated_at=1790210370` (= 07:39:30 WIB) — **identik** dengan keluaran script. Indodax `ticker/btcidr` `last=1506509000` identik dengan keluaran script (sumber indodax).
- **Rate limit nyata:** pada percobaan pertama, SOL gagal total (`HTTP 429`) karena script memanggil CoinGecko **satu permintaan per koin** (3 permintaan + retry). Script jujur (tidak mengarang, exit 3), tetapi percobaan kedua ETH jatuh ke **cache** dan ambang persennya diam-diam **tidak dicek** (cache tidak menyimpan perubahan 24 jam), sementara `pesan_singkat` tetap berbunyi "Tidak ada ambang yang terlewati saat ini" dan hanya memberi tanda ⚠️ tanpa kata "DATA BASI".
- `pesan_singkat` **tidak memuat sumber & jam data** ("ada di rincian JSON"), padahal SKILL.md "Format output" mewajibkannya dan jadwal otomatis mengirim `pesan_singkat` apa adanya. Di contoh di atas agent menambahkannya manual.
- Format angka campur: persen pakai titik ("-2.52%"), ambang harga tidak diformat ("2100000").
- Berita: artikel Pluang asli memuat "level resistance US$120/125/130" — agent sengaja membuangnya, tetapi SKILL.md Langkah B **tidak** menyuruh membuang target/level harga dari berita (lihat HASIL-UJI).
