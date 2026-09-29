#!/usr/bin/env python3
"""Adapter bursa untuk bot-trading-kripto (Python standar: urllib + hmac).

- Kertas (paper)  : harga dari API publik bursa, order DISIMULASIKAN (tanpa kunci).
- Binance Spot    : testnet (https://testnet.binance.vision) atau live (https://api.binance.com).
                    Tanda tangan HMAC-SHA256 atas query string (docs resmi Binance spot).
- Indodax         : live (https://indodax.com) atau demo (https://demo-indodax.com, status S).
                    Tanda tangan HMAC-SHA512 atas body (docs resmi btcid/indodax-official-api-docs).

KEAMANAN
- Kunci dibaca HANYA dari file milik member (di luar folder skill & di luar repo git,
  izin file 600 di macOS/Linux) atau dari variabel lingkungan yang member set sendiri.
- Kunci tidak pernah dicetak/ditulis ke log (objek Kunci menyembunyikan isinya; log lewat Penyamar).
- URL dasar tidak bisa diarahkan ke server lain kecuali localhost (untuk tes/mock) --
  supaya kunci tidak bisa "dibelokkan" ke server asing lewat konfigurasi.
- Pengalihan (redirect HTTP 3xx) TIDAK diikuti untuk permintaan bertanda tangan (yang membawa
  header Key/Sign/X-MBX-APIKEY): urllib bawaan akan menyalin header itu ke host tujuan. Permintaan
  publik hanya boleh dialihkan ke host & skema yang sama. Selain itu -> gagal dengan pesan jelas.
- Tidak ada pemanggilan metode keluarga withdraw/transfer sama sekali (termasuk yang baca-saja
  seperti withdrawFee Indodax) -- keputusan kurator 2026-09-29.
"""

import hashlib
import hmac
import json
import os
import stat
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from decimal import Decimal

from inti import D, NOL, bulat_bawah, bulat_uang, bulat_pajak, simulasi_isi

HEADER_RAHASIA = ("key", "sign", "x-mbx-apikey")

BATAS_WAKTU = 15
ENV_KUNCI, ENV_SECRET = "KOMUNITECH_BOT_API_KEY", "KOMUNITECH_BOT_API_SECRET"
URL = {
    ("binance", "live"): "https://api.binance.com",
    ("binance", "testnet"): "https://testnet.binance.vision",
    ("binance", "publik"): "https://data-api.binance.vision",
    ("indodax", "live"): "https://indodax.com",
    ("indodax", "testnet"): "https://demo-indodax.com",
    ("indodax", "publik"): "https://indodax.com",
}


class ErrorBursa(Exception):
    """Bursa menjawab jelas dengan penolakan/error. Pesan Bahasa Indonesia."""


class StatusTidakPasti(Exception):
    """Order mungkin terkirim tapi jawabannya tidak diterima (timeout/putus). Bot WAJIB berhenti
    dan member mengecek manual di aplikasi bursa."""


class ErrorKunci(Exception):
    pass


# ---------------------------------------------------------------------------- kunci

class Kunci:
    __slots__ = ("_k", "_s", "sumber")

    def __init__(self, k, s, sumber):
        self._k, self._s, self.sumber = k, s, sumber

    def __repr__(self):
        return f"<Kunci dari {self.sumber}, isi disembunyikan>"

    __str__ = __repr__

    def rahasia(self):
        return (self._k, self._s)


def _di_dalam_repo_git(path):
    d = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        induk = os.path.dirname(d)
        if induk == d:
            return None
        d = induk


def muat_kunci(cfg, folder_skill):
    """Baca kunci milik member. Pesan error TIDAK pernah memuat isi kunci."""
    spec = cfg.get("kunci") or {}
    if spec.get("env") is True:
        k, s = os.environ.get(ENV_KUNCI, ""), os.environ.get(ENV_SECRET, "")
        if not k or not s:
            raise ErrorKunci(f"Variabel lingkungan {ENV_KUNCI} / {ENV_SECRET} belum diset. "
                             "Set sendiri di mesin Anda (lihat references/keamanan-kunci-api.md).")
        return Kunci(k.strip(), s.strip(), "variabel lingkungan")
    path = os.path.abspath(os.path.expanduser(str(spec.get("file", ""))))
    if not os.path.isfile(path):
        raise ErrorKunci(f"File kunci '{path}' tidak ada. Buat sendiri mengikuti references/keamanan-kunci-api.md.")
    if os.path.commonpath([path, os.path.abspath(folder_skill)]) == os.path.abspath(folder_skill):
        raise ErrorKunci("File kunci berada DI DALAM folder skill. Pindahkan ke luar (mis. ~/.komunitech/kunci-bot.json).")
    repo = _di_dalam_repo_git(path)
    if repo:
        raise ErrorKunci(f"File kunci berada di dalam repo git ({repo}). Risiko ter-commit/bocor. "
                         "Pindahkan ke luar repo (mis. ~/.komunitech/kunci-bot.json).")
    if os.name == "posix":
        mode = stat.S_IMODE(os.stat(path).st_mode)
        if mode & 0o077:
            raise ErrorKunci(f"Izin file kunci terlalu terbuka ({oct(mode)}). Jalankan: chmod 600 \"{path}\"")
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        k, s = str(data["api_key"]).strip(), str(data["api_secret"]).strip()
    except (json.JSONDecodeError, KeyError, TypeError):
        raise ErrorKunci("File kunci harus JSON berisi \"api_key\" dan \"api_secret\" (isi tidak ditampilkan).")
    if not k or not s:
        raise ErrorKunci("api_key/api_secret di file kunci kosong.")
    return Kunci(k, s, "file milik member")


# ---------------------------------------------------------------------------- http

def _periksa_url_uji(url):
    if url is None:
        return None
    host = urllib.parse.urlparse(url).hostname
    if host not in ("127.0.0.1", "localhost"):
        raise ValueError("url uji hanya boleh localhost/127.0.0.1 (demi keamanan kunci).")
    return url.rstrip("/")


class _Dialihkan(Exception):
    def __init__(self, kode, asal, tujuan):
        super().__init__(kode, asal, tujuan)
        self.kode, self.asal, self.tujuan = kode, asal, tujuan


class _PenjagaRedirect(urllib.request.HTTPRedirectHandler):
    """Bertanda tangan: redirect apa pun ditolak. Publik: hanya host & skema yang sama."""

    def __init__(self, bertanda):
        super().__init__()
        self.bertanda = bertanda

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        asal = urllib.parse.urlparse(req.full_url)
        tujuan = urllib.parse.urlparse(urllib.parse.urljoin(req.full_url, newurl))
        if self.bertanda or (asal.scheme, asal.hostname, asal.port) != (tujuan.scheme, tujuan.hostname, tujuan.port):
            try:
                fp.close()
            except Exception:  # noqa: BLE001
                pass
            raise _Dialihkan(code, asal.hostname, tujuan.hostname or "?")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _http(metode, url, header=None, body=None, order=False):
    data = body.encode() if isinstance(body, str) else body
    header = header or {}
    bertanda = any(k.lower() in HEADER_RAHASIA for k in header)
    req = urllib.request.Request(url, data=data, method=metode, headers=header)
    req.add_header("User-Agent", "komunitech-bot-trading-kripto/1.0.3")
    pembuka = urllib.request.build_opener(_PenjagaRedirect(bertanda))
    try:
        with pembuka.open(req, timeout=BATAS_WAKTU) as r:
            isi = r.read().decode("utf-8", "replace")
    except _Dialihkan as e:
        pesan = (f"Bursa mengalihkan permintaan (HTTP {e.kode}) dari {e.asal} ke {e.tujuan}. Demi keamanan, "
                 + ("permintaan bertanda tangan TIDAK diikuti dan kunci API TIDAK dikirim ke alamat lain. "
                    if bertanda else "pengalihan ke host lain tidak diikuti. ")
                 + "Kemungkinan situs sedang maintenance/butuh login atau alamat API berubah; cek pengumuman bursa.")
        if order:
            raise StatusTidakPasti(pesan + " Order tidak dikirim ulang; cek aplikasi bursa untuk memastikan.")
        raise ErrorBursa(pesan)
    except urllib.error.HTTPError as e:
        isi = e.read().decode("utf-8", "replace")
        try:
            j = json.loads(isi)
        except json.JSONDecodeError:
            j = {"msg": isi[:200]}
        pesan = j.get("msg") or j.get("error") or j.get("message") or str(j)[:200]
        kode = j.get("code") or j.get("error_code") or ""
        if e.code == 451 or "restricted location" in str(pesan):
            raise ErrorBursa(f"Bursa menolak akses dari lokasi/IP ini (HTTP {e.code}).")
        raise ErrorBursa(f"Bursa menolak (HTTP {e.code}, kode {kode}): {pesan}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        if order:
            raise StatusTidakPasti(f"Tidak ada jawaban bursa saat mengirim order ({type(e).__name__}). "
                                   "Order MUNGKIN sudah masuk -- cek manual di aplikasi bursa.")
        raise ErrorBursa(f"Gagal menghubungi bursa: {type(e).__name__}: {getattr(e, 'reason', e)}")
    try:
        return json.loads(isi)
    except json.JSONDecodeError:
        if order:
            raise StatusTidakPasti("Jawaban bursa atas order tidak bisa dibaca. Cek manual di aplikasi bursa.")
        raise ErrorBursa("Jawaban bursa bukan JSON (mungkin halaman blokir/maintenance).")


def harga_valid(nilai):
    """Harga dari API wajib angka > 0 (harga 0/rusak -> tidak ada order)."""
    try:
        x = D(str(nilai))
    except Exception:  # noqa: BLE001
        raise ErrorBursa(f"Harga dari bursa tidak terbaca ({str(nilai)[:30]!r}). Tidak ada order.")
    if not x.is_finite() or x <= 0:
        raise ErrorBursa(f"Harga dari bursa tidak wajar ({str(nilai)[:30]}). Tidak ada order.")
    return x


# ---------------------------------------------------------------------------- binance

class Binance:
    def __init__(self, cfg, mode, kunci=None, url_uji=None):
        self.cfg, self.mode, self.kunci = cfg, mode, kunci
        uji = _periksa_url_uji(url_uji)
        self.url = uji or URL[("binance", "live" if mode == "live" else "testnet")]
        # paper memakai data pasar publik mainnet; testnet memakai harga testnet sendiri
        self.url_publik = uji or (URL[("binance", "publik")] if mode in ("paper", "live") else self.url)
        self.selisih_waktu = 0

    def _publik(self, path, params=None):
        q = ("?" + urllib.parse.urlencode(params)) if params else ""
        return _http("GET", self.url_publik + path + q)

    def harga(self):
        j = self._publik("/api/v3/ticker/price", {"symbol": self.cfg["pasangan"]})
        return harga_valid(j["price"])

    def aturan_simbol(self):
        j = self._publik("/api/v3/exchangeInfo", {"symbol": self.cfg["pasangan"]})
        s = j["symbols"][0]
        out = {"status": s.get("status")}
        for f in s.get("filters", []):
            if f["filterType"] == "LOT_SIZE":
                out["langkah_jumlah"] = D(f["stepSize"])
            if f["filterType"] in ("NOTIONAL", "MIN_NOTIONAL"):
                out["min_nilai_order"] = D(f.get("minNotional", "0"))
        return out

    def sinkron_waktu(self):
        j = _http("GET", self.url + "/api/v3/time")
        self.selisih_waktu = int(j["serverTime"]) - int(time.time() * 1000)

    @staticmethod
    def tanda_tangan(secret, query):
        return hmac.new(secret.encode(), query.encode(), hashlib.sha256).hexdigest()

    def _bertanda(self, metode, path, params=None, order=False):
        if not self.kunci:
            raise ErrorKunci("Kunci belum dimuat.")
        k, s = self.kunci.rahasia()
        p = dict(params or {})
        p["timestamp"] = int(time.time() * 1000) + self.selisih_waktu
        p["recvWindow"] = 5000
        q = urllib.parse.urlencode(p)
        q += "&signature=" + self.tanda_tangan(s, q)
        return _http(metode, f"{self.url}{path}?{q}", {"X-MBX-APIKEY": k}, order=order)

    def cek_izin_kunci(self):
        """Live: WAJIB lolos (tanpa withdraw, spot trading aktif). Testnet: tidak ada endpoint izin."""
        if self.mode == "testnet":
            akun = self._bertanda("GET", "/api/v3/account", {"omitZeroBalances": "true"})
            return {"lolos": bool(akun.get("canTrade")), "dicek_otomatis": False,
                    "catatan": "Testnet tidak menyediakan endpoint izin kunci; dana testnet bukan uang asli."}
        j = self._bertanda("GET", "/sapi/v1/account/apiRestrictions")
        masalah = []
        if j.get("enableWithdrawals"):
            masalah.append("kunci PUNYA izin withdraw (tarik dana) -- WAJIB dimatikan")
        if not j.get("enableSpotAndMarginTrading"):
            masalah.append("izin Spot Trading belum aktif")
        for k in ("enableMargin", "enableFutures", "enableInternalTransfer", "permitsUniversalTransfer"):
            if j.get(k):
                masalah.append(f"izin {k} aktif -- matikan, bot hanya butuh spot")
        return {"lolos": not masalah, "dicek_otomatis": True, "masalah": masalah,
                "ip_dibatasi": bool(j.get("ipRestrict")),
                "catatan": "" if j.get("ipRestrict") else "Disarankan batasi IP kunci ke IP mesin bot."}

    def jumlah_order_terbuka(self):
        return len(self._bertanda("GET", "/api/v3/openOrders", {"symbol": self.cfg["pasangan"]}))

    def saldo_koin(self):
        """Saldo koin (free + locked) di akun -- baca-saja (GET /api/v3/account). Untuk rekonsiliasi
        paparan live terhadap modal_maks_total."""
        akun = self._bertanda("GET", "/api/v3/account", {"omitZeroBalances": "true"})
        for b in akun.get("balances", []):
            if str(b.get("asset", "")).upper() == self.cfg["koin"]:
                return D(str(b.get("free", "0"))) + D(str(b.get("locked", "0")))
        return NOL

    def order_pasar(self, sisi, nilai_kutipan=None, jumlah_koin=None, langkah=D("0.00000001")):
        p = {"symbol": self.cfg["pasangan"], "type": "MARKET", "newOrderRespType": "FULL",
             "newClientOrderId": "kt-" + uuid.uuid4().hex[:20]}
        if sisi == "beli":
            # kutipan kripto (USDT dll.) = swap -> PPh sisi beli; sisihkan supaya total <= nilai order
            t = self.cfg["_d"].get("tarif_pph_beli", NOL)
            p.update(side="BUY", quoteOrderQty=format(bulat_bawah(nilai_kutipan / (D("1") + t), D("0.01")), "f"))
        else:
            p.update(side="SELL", quantity=format(bulat_bawah(jumlah_koin, langkah).normalize(), "f"))
        j = self._bertanda("POST", "/api/v3/order", p, order=True)
        return self._isi_dari_respons(sisi, j)

    def _isi_dari_respons(self, sisi, j):
        kut, koin = self.cfg["kutipan"], self.cfg["koin"]
        eq, cq = D(str(j.get("executedQty", "0"))), D(str(j.get("cummulativeQuoteQty", "0")))
        if eq <= 0:
            raise ErrorBursa(f"Order tidak terisi (status {j.get('status')}).")
        harga = cq / eq
        kom_kut = kom_koin = kom_lain = NOL
        for f in j.get("fills", []):
            c = D(str(f.get("commission", "0")))
            if f.get("commissionAsset") == kut:
                kom_kut += c
            elif f.get("commissionAsset") == koin:
                kom_koin += c
            else:
                kom_lain += c
        fee = bulat_uang(kom_kut + kom_koin * harga, kut)
        if sisi == "beli":
            pajak = bulat_pajak(cq * self.cfg["_d"].get("tarif_pph_beli", NOL), kut)
            isi = {"sisi": "beli", "harga": harga, "jumlah": eq - kom_koin, "bruto": cq, "fee": fee,
                   "pajak": pajak, "bersih": cq + kom_kut + pajak}
        else:
            pajak = bulat_pajak(cq * self.cfg["_d"]["tarif_pph"], kut)
            isi = {"sisi": "jual", "harga": harga, "jumlah": eq, "bruto": cq, "fee": fee,
                   "pajak": pajak, "bersih": cq - kom_kut - pajak}
        isi.update(order_id=j.get("orderId"), sumber_angka="bursa",
                   catatan=("komisi dibayar aset lain (mis. BNB), tidak masuk hitungan" if kom_lain else ""))
        return isi

    def batalkan_semua(self):
        try:
            j = self._bertanda("DELETE", "/api/v3/openOrders", {"symbol": self.cfg["pasangan"]})
            return len(j) if isinstance(j, list) else 0
        except ErrorBursa as e:
            if "-2011" in str(e) or "Unknown order" in str(e):
                return 0
            raise


# ---------------------------------------------------------------------------- indodax

class Indodax:
    def __init__(self, cfg, mode, kunci=None, url_uji=None):
        self.cfg, self.mode, self.kunci = cfg, mode, kunci
        uji = _periksa_url_uji(url_uji)
        self.url = uji or URL[("indodax", "live" if mode in ("live", "paper") else "testnet")]
        self.id_pasangan = cfg["pasangan"].replace("_", "")
        self.koin = cfg["koin"].lower()

    def harga(self):
        j = _http("GET", f"{self.url}/api/ticker/{self.id_pasangan}")
        return harga_valid(j["ticker"]["last"])

    def aturan_simbol(self):
        daftar = _http("GET", f"{self.url}/api/pairs")
        for p in daftar:
            if p.get("id") == self.id_pasangan:
                return {"status": "maintenance" if p.get("is_maintenance") or p.get("is_market_suspended") else "TRADING",
                        "min_nilai_order": D(str(p.get("trade_min_base_currency", "10000"))),
                        "langkah_jumlah": D("0.00000001")}
        raise ErrorBursa(f"Pasangan {self.cfg['pasangan']} tidak ditemukan di Indodax.")

    @staticmethod
    def tanda_tangan(secret, body):
        return hmac.new(secret.encode(), body.encode(), hashlib.sha512).hexdigest()

    def _tapi(self, metode, params=None, order=False):
        if not self.kunci:
            raise ErrorKunci("Kunci belum dimuat.")
        k, s = self.kunci.rahasia()
        p = {"method": metode, "timestamp": int(time.time() * 1000), "recvWindow": 5000}
        p.update(params or {})
        body = urllib.parse.urlencode(p)
        j = _http("POST", self.url + "/tapi",
                  {"Key": k, "Sign": self.tanda_tangan(s, body),
                   "Content-Type": "application/x-www-form-urlencoded"}, body, order=order)
        if str(j.get("success")) != "1":
            raise ErrorBursa(f"Indodax menolak ({j.get('error_code', '')}): {j.get('error', j)}")
        return j["return"]

    def cek_izin_kunci(self):
        self._tapi("getInfo")  # membuktikan kunci valid; TIDAK menampilkan izin
        # Keputusan kurator 2026-09-29: TIDAK memanggil metode keluarga withdraw apa pun (termasuk
        # withdrawFee yang baca-saja) walau bisa dipakai menebak izin. Izin dicek MANUAL oleh member
        # lewat daftar periksa wajib + flag --saya-sudah-cek-tanpa-withdraw di siapkan_live.py.
        return {"lolos": None, "dicek_otomatis": False,
                "catatan": ("Izin withdraw Indodax TIDAK diperiksa otomatis (skill sengaja tidak memanggil "
                            "metode withdraw apa pun). Buka Indodax > Pengaturan API, pastikan izin 'withdraw' "
                            "TIDAK dicentang, lalu selesaikan daftar periksa di siapkan_live.py "
                            "(--saya-sudah-cek-tanpa-withdraw). Lihat references/keamanan-kunci-api.md.")}

    def saldo_koin(self):
        """Saldo koin (tersedia + ditahan order) dari getInfo -- baca-saja."""
        r = self._tapi("getInfo")
        total = NOL
        for kunci in ("balance", "balance_hold"):
            v = (r.get(kunci) or {}).get(self.koin)
            if v not in (None, ""):
                total += D(str(v))
        return total

    def jumlah_order_terbuka(self):
        r = self._tapi("openOrders", {"pair": self.cfg["pasangan"]})
        o = r.get("orders") or []
        return len(o) if isinstance(o, list) else sum(len(v) for v in o.values())

    def order_pasar(self, sisi, nilai_kutipan=None, jumlah_koin=None, langkah=D("0.00000001")):
        p = {"pair": self.cfg["pasangan"], "order_type": "market",
             "client_order_id": "kt-" + uuid.uuid4().hex[:20]}
        if sisi == "beli":
            p.update(type="buy", idr=str(int(bulat_bawah(nilai_kutipan, D("1")))))
        else:
            p.update(type="sell")
            p[self.koin] = format(bulat_bawah(jumlah_koin, langkah).normalize(), "f")
        r = self._tapi("trade", p, order=True)
        return self._isi_dari_respons(sisi, r, nilai_kutipan, jumlah_koin)

    def _isi_dari_respons(self, sisi, r, nilai_kutipan, jumlah_koin):
        """Pakai angka dari respons bila ada; selain itu tandai 'estimasi' (dicocokkan manual
        dengan riwayat transaksi Indodax)."""
        fee = D(str(r.get("fee", "0") or "0"))
        oid = r.get("order_id")
        if sisi == "beli" and f"receive_{self.koin}" in r and D(str(r.get("spend_rp", "0") or "0")) > 0:
            jumlah, spend = D(str(r[f"receive_{self.koin}"])), D(str(r["spend_rp"]))
            return {"sisi": "beli", "harga": spend / jumlah if jumlah else NOL, "jumlah": jumlah,
                    "bruto": spend, "fee": fee, "pajak": NOL, "bersih": spend + fee,
                    "order_id": oid, "sumber_angka": "bursa", "catatan": ""}
        if sisi == "jual" and "receive_rp" in r and f"sold_{self.koin}" in r:
            jumlah, terima = D(str(r[f"sold_{self.koin}"])), D(str(r["receive_rp"]))
            pajak = bulat_pajak(terima * self.cfg["_d"]["tarif_pph"], "IDR")
            return {"sisi": "jual", "harga": terima / jumlah if jumlah else NOL, "jumlah": jumlah,
                    "bruto": terima, "fee": fee, "pajak": pajak, "bersih": terima - fee - pajak,
                    "order_id": oid, "sumber_angka": "bursa+estimasi_pajak", "catatan": ""}
        harga = self.harga()
        isi = simulasi_isi(self.cfg, sisi, harga, nilai_kutipan, jumlah_koin)
        if isi is None:
            raise ErrorBursa("Order terkirim tetapi jumlahnya tidak bisa dihitung. Cek manual di Indodax.")
        isi.update(order_id=oid, sumber_angka="estimasi",
                   catatan="Respons Indodax tidak memuat angka isi lengkap; angka ESTIMASI, cocokkan dengan riwayat Indodax.")
        return isi

    def batalkan_semua(self):
        r = self._tapi("openOrders", {"pair": self.cfg["pasangan"]})
        n = 0
        for o in r.get("orders") or []:
            self._tapi("cancelOrder", {"pair": self.cfg["pasangan"], "order_id": o["order_id"], "type": o["type"]})
            n += 1
        return n


# ---------------------------------------------------------------------------- kertas

class Kertas:
    """Paper trading: harga asli dari API publik (atau --harga manual), order disimulasikan."""

    def __init__(self, cfg, harga_manual=None, url_uji=None):
        self.cfg = cfg
        self.harga_manual = harga_manual
        self.sumber = (Binance if cfg["bursa"] == "binance" else Indodax)(cfg, "paper", None, url_uji)

    def harga(self):
        return self.harga_manual if self.harga_manual is not None else self.sumber.harga()

    def aturan_simbol(self):
        if self.harga_manual is not None:
            return {}
        try:
            return self.sumber.aturan_simbol()
        except (ErrorBursa, KeyError, IndexError):
            return {}

    def cek_izin_kunci(self):
        return {"lolos": True, "dicek_otomatis": False, "catatan": "Mode simulasi tidak memakai kunci."}

    def jumlah_order_terbuka(self):
        return 0

    def order_pasar(self, sisi, nilai_kutipan=None, jumlah_koin=None, langkah=None):
        isi = simulasi_isi(self.cfg, sisi, self.harga(), nilai_kutipan, jumlah_koin)
        if isi is None:
            raise ErrorBursa("Jumlah order 0 setelah pembulatan lot.")
        isi.update(order_id="SIM-" + uuid.uuid4().hex[:10], sumber_angka="simulasi", catatan="")
        return isi

    def batalkan_semua(self):
        return 0


def buat_adapter(cfg, kunci=None, harga_manual=None, url_uji=None):
    if cfg["mode"] == "paper":
        return Kertas(cfg, harga_manual, url_uji)
    kelas = Binance if cfg["bursa"] == "binance" else Indodax
    return kelas(cfg, cfg["mode"], kunci, url_uji)
