#!/usr/bin/env python3
"""Server TIRUAN lokal (127.0.0.1) yang meniru respons TERDOKUMENTASI Binance Spot API &
Indodax Trade API, untuk menguji endpoint bertanda tangan TANPA akun/kunci asli.

Bentuk respons disalin dari contoh di dokumentasi resmi (dibaca 2026-09-29):
- https://github.com/binance/binance-spot-api-docs/blob/master/testnet/rest-api.md
- https://developers.binance.com/docs/wallet/account/api-key-permission
- https://github.com/btcid/indodax-official-api-docs/blob/master/Private-RestAPI.md
Ini BUKAN bursa sungguhan: pengisian order disederhanakan (market terisi penuh di harga tiruan).

Kunci uji = contoh kunci PUBLIK dari dokumentasi resmi masing-masing bursa (bukan milik siapa pun).
"""

import hashlib
import hmac
import json
import threading
import time
import urllib.parse
from decimal import Decimal, ROUND_DOWN
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BINANCE_KEY = "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A"
BINANCE_SECRET = "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
INDODAX_KEY = "AEDHIGAT-QATEGWOX-OPCSCPQX-2E00B1L7-VJBXXKMA"
INDODAX_SECRET = "f60617a68fcce028f0a90bc9eb765d17379eb548cc935c01a7ee3186eecf870e9b68f27a31bcfe8d"


class Kondisi:
    def __init__(self):
        self.harga_btcusdt = Decimal("60000")
        self.harga_btcidr = Decimal("1500000000")
        self.withdraw_aktif = False
        self.order_terbuka = 0
        self.nilai_order_terbuka = Decimal("50")   # nilai kutipan (USDT / rupiah) tiap order BELI terbuka tiruan
        self.jeda_order = 0.0          # detik jeda sebelum order terisi (uji balapan proses paralel)
        self.kunci = threading.Lock()  # server tiruan berutas banyak: saldo diperbarui atomik
        self.putus_saat_order = False
        self.tolak_order = None
        self.saldo_btc = Decimal("0")   # saldo BTC akun tiruan (bertambah saat order beli terisi)
        self.gagal_saldo = False        # bila True, endpoint saldo menjawab error (uji rekonsiliasi)
        self.alihkan_ke = None      # URL dasar: bila diisi, SEMUA permintaan dijawab 302 ke sana (uji M1)
        self.permintaan = []   # (metode, path, header, query, body) -- untuk diperiksa tes
        self.order = []


def _dec(x):
    return format(Decimal(x).normalize(), "f")


class Handler(BaseHTTPRequestHandler):
    kondisi = None

    def log_message(self, *a):
        pass

    def _kirim(self, kode, obj):
        b = json.dumps(obj).encode()
        self.send_response(kode)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _proses(self, metode):
        k = self.kondisi
        u = urllib.parse.urlparse(self.path)
        panjang = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(panjang).decode() if panjang else ""
        k.permintaan.append((metode, u.path, dict(self.headers), u.query, body))
        if k.alihkan_ke:
            self.send_response(302)
            self.send_header("Location", k.alihkan_ke + self.path)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        q = dict(urllib.parse.parse_qsl(u.query))
        if u.path.startswith("/api/v3") or u.path.startswith("/sapi"):
            return self._binance(metode, u, q, body)
        if u.path == "/tapi":
            return self._indodax_tapi(body)
        if u.path == "/api/ticker/btcidr":
            return self._kirim(200, {"ticker": {"last": str(k.harga_btcidr), "buy": str(k.harga_btcidr),
                                                "sell": str(k.harga_btcidr), "server_time": int(time.time())}})
        if u.path == "/api/pairs":
            return self._kirim(200, [{"id": "btcidr", "trade_min_base_currency": 10000, "is_maintenance": 0,
                                      "is_market_suspended": 0, "trade_fee_percent_taker": 0.2}])
        return self._kirim(404, {"msg": "tidak ada"})

    # ------------------------------------------------------------------ binance
    def _binance(self, metode, u, q, body):
        k = self.kondisi
        p = u.path
        if p == "/api/v3/time":
            return self._kirim(200, {"serverTime": int(time.time() * 1000)})
        if p == "/api/v3/ticker/price":
            return self._kirim(200, {"symbol": q.get("symbol"), "price": _dec(k.harga_btcusdt)})
        if p == "/api/v3/exchangeInfo":
            return self._kirim(200, {"symbols": [{"symbol": "BTCUSDT", "status": "TRADING", "filters": [
                {"filterType": "PRICE_FILTER", "tickSize": "0.01000000"},
                {"filterType": "LOT_SIZE", "minQty": "0.00001000", "stepSize": "0.00001000"},
                {"filterType": "NOTIONAL", "minNotional": "5.00000000"}]}]})
        # --- endpoint bertanda tangan
        if self.headers.get("X-MBX-APIKEY") != BINANCE_KEY:
            return self._kirim(401, {"code": -2015, "msg": "Invalid API-key, IP, or permissions for action."})
        raw = u.query
        if "&signature=" not in raw:
            return self._kirim(400, {"code": -1102, "msg": "Mandatory parameter 'signature' was not sent."})
        payload, sig = raw.rsplit("&signature=", 1)
        benar = hmac.new(BINANCE_SECRET.encode(), (payload + body).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, benar):
            return self._kirim(400, {"code": -1022, "msg": "Signature for this request is not valid."})
        if abs(int(q.get("timestamp", 0)) - int(time.time() * 1000)) > int(q.get("recvWindow", 5000)):
            return self._kirim(400, {"code": -1021, "msg": "Timestamp for this request is outside of the recvWindow."})
        if p == "/sapi/v1/account/apiRestrictions":
            return self._kirim(200, {"ipRestrict": False, "createTime": 1623840271000, "enableReading": True,
                                     "enableWithdrawals": k.withdraw_aktif, "enableInternalTransfer": False,
                                     "enableMargin": False, "enableFutures": False, "permitsUniversalTransfer": False,
                                     "enableVanillaOptions": False, "enableFixApiTrade": False,
                                     "enableFixReadOnly": True, "enableSpotAndMarginTrading": True,
                                     "enablePortfolioMarginTrading": False})
        if p == "/api/v3/account":
            if k.gagal_saldo:
                return self._kirim(500, {"code": -1000, "msg": "An unknown error occurred."})
            return self._kirim(200, {"canTrade": True, "canWithdraw": True, "canDeposit": True, "accountType": "SPOT",
                                     "balances": [{"asset": "USDT", "free": "10000.00000000", "locked": "0.00000000"},
                                                  {"asset": "BTC", "free": _dec(k.saldo_btc), "locked": "0"}],
                                     "permissions": ["SPOT"]})
        if p == "/api/v3/openOrders" and metode == "GET":
            # order BELI limit terbuka: 0,001 BTC x harga -> nilai_order_terbuka USDT tertahan
            harga_o = k.nilai_order_terbuka / Decimal("0.001")
            return self._kirim(200, [{"symbol": "BTCUSDT", "orderId": i, "status": "NEW", "side": "BUY", "type": "LIMIT",
                                      "price": _dec(harga_o), "origQty": "0.00100000", "executedQty": "0.00000000",
                                      "cummulativeQuoteQty": "0.00000000", "origQuoteOrderQty": "0.00000000"}
                                     for i in range(k.order_terbuka)])
        if p == "/api/v3/openOrders" and metode == "DELETE":
            n, k.order_terbuka = k.order_terbuka, 0
            if n == 0:
                return self._kirim(400, {"code": -2011, "msg": "Unknown order sent."})
            return self._kirim(200, [{"symbol": "BTCUSDT", "orderId": i, "status": "CANCELED"} for i in range(n)])
        if p == "/api/v3/order" and metode == "POST":
            if k.putus_saat_order:
                self.close_connection = True
                self.connection.shutdown(2)
                return
            if k.tolak_order:
                return self._kirim(400, {"code": -2010, "msg": k.tolak_order})
            if k.jeda_order:
                time.sleep(k.jeda_order)
            harga = k.harga_btcusdt
            langkah = Decimal("0.00001")
            if q["side"] == "BUY":
                eq = (Decimal(q["quoteOrderQty"]) / harga / langkah).to_integral_value(ROUND_DOWN) * langkah
                kom, aset = (eq * Decimal("0.001")).quantize(Decimal("0.00000001")), "BTC"
            else:
                eq = Decimal(q["quantity"])
                kom, aset = (eq * harga * Decimal("0.001")).quantize(Decimal("0.00000001")), "USDT"
            cq = eq * harga
            with k.kunci:
                k.saldo_btc += (eq - kom) if q["side"] == "BUY" else -eq
            resp = {"symbol": "BTCUSDT", "orderId": 28 + len(k.order), "orderListId": -1,
                    "clientOrderId": q.get("newClientOrderId"), "transactTime": int(time.time() * 1000),
                    "price": "0.00000000", "origQty": _dec(eq), "executedQty": _dec(eq),
                    "cummulativeQuoteQty": _dec(cq), "status": "FILLED", "timeInForce": "GTC", "type": "MARKET",
                    "side": q["side"], "fills": [{"price": _dec(harga), "qty": _dec(eq), "commission": _dec(kom),
                                                  "commissionAsset": aset, "tradeId": 56}]}
            k.order.append(resp)
            return self._kirim(200, resp)
        return self._kirim(404, {"code": -1, "msg": "tidak ditiru"})

    # ------------------------------------------------------------------ indodax
    def _indodax_tapi(self, body):
        k = self.kondisi
        if self.headers.get("Key") != INDODAX_KEY:
            return self._kirim(200, {"success": 0, "error": "Invalid credentials. API not found or session has expired.",
                                     "error_code": "invalid_credentials"})
        benar = hmac.new(INDODAX_SECRET.encode(), body.encode(), hashlib.sha512).hexdigest()
        if not hmac.compare_digest(self.headers.get("Sign", ""), benar):
            return self._kirim(200, {"success": 0, "error": "Invalid credentials. Bad sign.", "error_code": "invalid_credentials"})
        p = dict(urllib.parse.parse_qsl(body))
        m = p.get("method")
        if m == "getInfo":
            return self._kirim(200, {"success": 1, "return": {"server_time": int(time.time()),
                                                              "balance": {"idr": 5000000, "btc": _dec(k.saldo_btc)},
                                                              "balance_hold": {"idr": 0, "btc": "0.00000000"}}})
        if m == "openOrders":
            return self._kirim(200, {"success": 1, "return": {"orders": [
                {"order_id": str(170 + i), "type": "buy", "order_type": "limit", "price": "1400000000",
                 "order_idr": _dec(k.nilai_order_terbuka), "remain_idr": _dec(k.nilai_order_terbuka)}
                for i in range(k.order_terbuka)]}})
        if m == "cancelOrder":
            k.order_terbuka = max(0, k.order_terbuka - 1)
            return self._kirim(200, {"success": 1, "return": {"order_id": int(p["order_id"]), "type": p["type"], "pair": p["pair"]}})
        if m == "trade":
            if k.putus_saat_order:
                self.close_connection = True
                self.connection.shutdown(2)
                return
            # bentuk respons persis contoh docs (receive_btc, spend_rp, fee, remain_rp, order_id)
            if p["type"] == "buy":
                idr = Decimal(p["idr"])
                fee = (idr * Decimal("0.002")).quantize(Decimal("1"))
                btc = ((idr - fee) / k.harga_btcidr).quantize(Decimal("0.00000001"), ROUND_DOWN)
                ret = {"receive_btc": _dec(btc), "spend_rp": int(idr - fee), "fee": int(fee), "remain_rp": 0}
                if k.jeda_order:
                    time.sleep(k.jeda_order)
                with k.kunci:
                    k.saldo_btc += btc
            else:
                ret = {"receive_btc": "0.00000000", "spend_rp": 0, "fee": 0, "remain_rp": 0}
            ret.update(order_id=59632813 + len(k.order), client_order_id=p.get("client_order_id"))
            k.order.append(ret)
            return self._kirim(200, {"success": 1, "return": ret})
        return self._kirim(200, {"success": 0, "error": "method tidak ditiru", "error_code": "invalid_method"})

    def do_GET(self):
        self._proses("GET")

    def do_POST(self):
        self._proses("POST")

    def do_DELETE(self):
        self._proses("DELETE")


def jalankan():
    """Mulai server di port acak. Kembalikan (url, kondisi, server)."""
    kondisi = Kondisi()
    kelas = type("H", (Handler,), {"kondisi": kondisi})
    srv = ThreadingHTTPServer(("127.0.0.1", 0), kelas)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}", kondisi, srv


if __name__ == "__main__":
    url, _, srv = jalankan()
    print(f"Server tiruan jalan di {url} (Ctrl+C untuk berhenti)")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        srv.shutdown()
