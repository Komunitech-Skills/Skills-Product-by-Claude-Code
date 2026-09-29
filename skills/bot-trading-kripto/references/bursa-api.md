# Endpoint bursa yang dipakai & status uji (2026-09-29)

**T** = dipanggil sungguhan dari lingkungan uji. **M** = diuji terhadap server tiruan lokal
(`tests/mock_bursa.py`) yang meniru contoh respons di dokumentasi resmi. **S** = belum diuji.

## Indodax — docs: https://github.com/btcid/indodax-official-api-docs
| Fungsi | Endpoint | Status |
|---|---|---|
| Harga | `GET /api/ticker/{btcidr}` → `ticker.last` | T |
| Aturan pasangan | `GET /api/pairs` → `trade_min_base_currency`, `is_maintenance` | T |
| Candle harian | `GET /tradingview/history_v2?symbol=BTCIDR&tf=1D&from&to` | T |
| Tanda tangan | `POST /tapi`, header `Key`, `Sign` = HMAC-SHA512(body, secret); `timestamp` + `recvWindow` | vektor docs cocok (T), M |
| getInfo / openOrders / trade (market) / cancelOrder | `method=...` | M |
| Demo | `https://demo-indodax.com` (disebut di docs) | S — minta login (Cloudflare Access) dari lingkungan uji |
Catatan: order beli market memakai `idr`; jual memakai jumlah koin (`btc=` dst.). Respons `trade`
di docs hanya mencontohkan `receive_btc`, `spend_rp`, `fee`, `remain_rp`, `order_id`; bila rincian
isi tidak ada, bot mencatat angka ESTIMASI.

## Binance Spot — docs: https://github.com/binance/binance-spot-api-docs (testnet/rest-api.md)
| Fungsi | Endpoint | Status |
|---|---|---|
| Harga (paper/live) | `GET https://data-api.binance.vision/api/v3/ticker/price` | T |
| Aturan simbol | `GET /api/v3/exchangeInfo` → `LOT_SIZE.stepSize`, `NOTIONAL.minNotional` | T (data-api) |
| Candle | `GET /api/v3/klines?interval=1d` | T (data-api) |
| Testnet | `https://testnet.binance.vision/api` | S — HTTP 451 "restricted location" dari lingkungan uji |
| Tanda tangan | HMAC-SHA256(query+body) hex → `signature`, header `X-MBX-APIKEY` | vektor docs cocok (T), M |
| Waktu server | `GET /api/v3/time` | M |
| Akun | `GET /api/v3/account` (`canTrade`) | M |
| Izin kunci (live) | `GET /sapi/v1/account/apiRestrictions` (`enableWithdrawals`, …) | M |
| Order | `POST /api/v3/order` `type=MARKET`, BUY `quoteOrderQty`, SELL `quantity`, `newOrderRespType=FULL` | M |
| Order terbuka / batalkan | `GET` / `DELETE /api/v3/openOrders` | M |
Keamanan: kunci hanya dikirim ke host resmi di atas. `--url-uji` hanya menerima localhost.
