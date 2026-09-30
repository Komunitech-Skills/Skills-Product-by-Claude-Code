#!/usr/bin/env python3
"""Server Odoo TIRUAN (Python standar) untuk uji regresi & contoh skill odoo-usaha.

BUKAN Odoo sungguhan. Meniru BENTUK antarmuka API eksternal resmi Odoo sesuai dokumentasi
(dicek 30 Sep 2026, lihat research/sources/odoo-2026-09-30.md):
- POST /xmlrpc/2/common  : version(), authenticate(db, login, kunci, {})
- POST /xmlrpc/2/object  : execute_kw(db, uid, kunci, model, metode, args, kw)
  Galat = XML-RPC Fault dengan kode seperti Odoo /xmlrpc/2: 1 galat aplikasi (traceback),
  2 UserError/peringatan, 3 Access Denied (login), 4 AccessError (hak).
- POST /json/2/<model>/<metode> (hanya versi >= 19), header Authorization: bearer <kunci>;
  galat = JSON {name, message, arguments, context, debug} + status 401/403/404/422/500.
- GET /web/version (hanya versi >= 19): {"version_info": [...], "version": "19.0"}.
Semua data FIKTIF. Perhitungan pajak tiruan: 11% efektif per baris (PPN 12% x DPP 11/12),
dibulatkan 2 desimal per baris - hanya pendekatan, bukan perilaku pasti Odoo.

Jalankan manual (untuk contoh):  python3 tests/server_tiruan.py --port 8069 --versi 19
Mode gangguan: --mode timeout_create | error500_create | redirect | xmlrpc_hilang | tanpa_stok | bukan_odoo |
tolak_semua
"""
import argparse
import copy
import json
import re
import threading
import time
import xmlrpc.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB = "tokomaju"
KUNCI = {
    "kt-baca-4f1c9a7e2b6d8c0a5e3f": {"uid": 6, "login": "bot-laporan@tokomaju.test", "peran": "baca"},
    "kt-jual-9b2e7c4a1f8d6e0b3a5c": {"uid": 7, "login": "bot-penjualan@tokomaju.test", "peran": "jual"},
    "kt-admin-2a7f9c1e5b3d8a6c4e0f": {"uid": 2, "login": "admin@tokomaju.test", "peran": "admin"},
}
KUNCI_BACA, KUNCI_JUAL, KUNCI_ADMIN = list(KUNCI)


def data_awal(versi):
    idr, usd = [12, "IDR"], [2, "USD"]
    p = {
        3: "CV Maju Jaya", 8: "Warung Bu Sari", 9: "Toko Bangunan Sinar Abadi", 10: "PT Kopi Nusantara Sejahtera",
        11: "Budi Santoso", 12: "Hotel Melati Indah", 13: "Sari Roti Mandiri",
    }
    partner = [
        {"id": 3, "name": p[3], "email": "admin@majujaya.test", "phone": "0812-3456-7890", "mobile": False,
         "city": "Solo"},
        {"id": 8, "name": p[8], "email": False, "phone": "+62 813 1111 2222", "mobile": False, "city": "Klaten"},
        {"id": 9, "name": p[9], "email": "order@sinarabadi.test", "phone": "0274-555123", "mobile": "0857-9999-0001",
         "city": "Yogyakarta"},
        {"id": 10, "name": p[10], "email": "keuangan@kopinusantara.test", "phone": False, "mobile": False,
         "city": "Jakarta"},
        {"id": 11, "name": p[11], "email": "budi.s@contoh.test", "phone": "0821-7777-6543", "mobile": False,
         "city": "Solo"},
        {"id": 12, "name": p[12], "email": False, "phone": "0271-888777", "mobile": False, "city": "Surakarta"},
        {"id": 13, "name": p[13], "email": False, "phone": "0812-0000-1111", "mobile": False, "city": "Sukoharjo"},
    ]
    if versi >= 19:
        for r in partner:
            r.pop("mobile")
    produk = [
        # id, kode, nama, harga, jenis, stok, perkiraan, sale_ok
        (21, "KP-250", "Kopi Robusta Bubuk 250g", 45000, True, 120, 96, True),
        (22, "GA-1KG", "Gula Aren Cair 1kg", 32500, True, 8, 8, True),
        (23, "CUP-12", "Gelas Kertas 12oz (isi 50)", 27500, True, 0, 50, True),
        (24, "SRP-VNL", "Sirup Vanila 750ml", 68000, True, -2, -2, True),
        (25, "KP-1KG", "Kopi Arabika Gayo 1kg", 210000, True, 14, 4, True),
        (26, "JS-ANTAR", "Ongkos Antar Dalam Kota", 15000, False, 0, 0, True),
        (27, "MSN-01", "Mesin Espresso Bekas (aset)", 7500000, True, 1, 1, False),
        (28, "KP-250-D", "Kopi Robusta Bubuk 250g (Decaf)", 52000, True, 30, 30, True),
        (29, "SDT-KYU", "Sendok Kayu (isi 100)", 12500, True, 0, 0, True),
    ]
    produk_rec = []
    for pid, kode, nama, harga, stok_ok, qa, va, sale_ok in produk:
        r = {"id": pid, "default_code": kode, "name": nama, "display_name": "[{}] {}".format(kode, nama),
             "list_price": float(harga), "sale_ok": sale_ok, "barcode": False, "qty_available": float(qa),
             "virtual_available": float(va), "uom_id": [1, "Unit"]}
        if versi >= 18:
            r["type"] = "consu" if stok_ok else "service"
            r["is_storable"] = stok_ok
        else:
            r["type"] = "product" if stok_ok else "service"
        if not stok_ok:
            r["qty_available"] = r["virtual_available"] = 0.0
        produk_rec.append(r)
    nama_p = {r["id"]: r["display_name"] for r in produk_rec}
    orderpoint = [
        {"id": 1, "product_id": [21, nama_p[21]], "location_id": [8, "WH/Stok"], "product_min_qty": 100.0,
         "product_max_qty": 200.0, "qty_on_hand": 120.0, "qty_forecast": 96.0},
        {"id": 2, "product_id": [22, nama_p[22]], "location_id": [8, "WH/Stok"], "product_min_qty": 10.0,
         "product_max_qty": 0.0, "qty_on_hand": 8.0, "qty_forecast": 8.0},
        {"id": 3, "product_id": [23, nama_p[23]], "location_id": [8, "WH/Stok"], "product_min_qty": 20.0,
         "product_max_qty": 100.0, "qty_on_hand": 0.0, "qty_forecast": 50.0},
        {"id": 4, "product_id": [24, nama_p[24]], "location_id": [8, "WH/Stok"], "product_min_qty": 6.0,
         "product_max_qty": 24.0, "qty_on_hand": -2.0, "qty_forecast": -2.0},
        {"id": 5, "product_id": [28, nama_p[28]], "location_id": [8, "WH/Stok"], "product_min_qty": 10.0,
         "product_max_qty": 40.0, "qty_on_hand": 30.0, "qty_forecast": 30.0},
    ]

    def so(i, nama, pid, tgl, state, dpp, tax, cur=None, origin=False):
        return {"id": i, "name": nama, "partner_id": [pid, p[pid]], "date_order": tgl, "state": state,
                "amount_untaxed": dpp, "amount_tax": tax, "amount_total": round(dpp + tax, 2),
                "currency_id": cur or idr, "origin": origin, "create_date": tgl, "validity_date": False}
    pesanan = [
        # 30 Sep 2026 WIB = 2026-09-29 17:00:00 .. 2026-09-30 17:00:00 UTC
        so(101, "S00101", 3, "2026-09-29 18:30:00", "sale", 332345.0, 36557.95),   # 01.30 WIB tgl 30
        so(102, "S00102", 8, "2026-09-30 02:15:00", "sale", 135000.0, 14850.0),
        so(103, "S00103", 12, "2026-09-30 07:40:00", "sale", 1260000.0, 138600.0),
        so(104, "S00104", 9, "2026-09-30 09:05:00", "draft", 500000.0, 55000.0),    # draf: tidak dihitung
        so(105, "S00105", 11, "2026-09-30 10:00:00", "cancel", 90000.0, 9900.0),    # batal
        so(106, "S00106", 10, "2026-09-30 11:20:00", "sale", 1000.0, 0.0, usd),      # USD: tidak dijumlah
        so(107, "S00107", 13, "2026-09-30 17:30:00", "sale", 45000.0, 4950.0),      # 00.30 WIB tgl 1 Okt
        # 29 Sep 2026 WIB
        so(95, "S00095", 3, "2026-09-29 03:00:00", "sale", 900000.0, 99000.0),
        so(96, "S00096", 11, "2026-09-29 08:00:00", "sale", 450000.0, 49500.0),
    ]
    if versi <= 16:
        pesanan[2]["state"] = "done"
    baris = [
        {"id": 1001, "order_id": [101, "S00101"], "product_id": [21, nama_p[21]], "product_uom_qty": 3.0,
         "price_unit": 45000.0, "discount": 0.0, "price_subtotal": 135000.0},
        {"id": 1002, "order_id": [101, "S00101"], "product_id": [22, nama_p[22]], "product_uom_qty": 2.0,
         "price_unit": 32500.0, "discount": 0.0, "price_subtotal": 65000.0},
        {"id": 1003, "order_id": [101, "S00101"], "product_id": [25, nama_p[25]], "product_uom_qty": 1.0,
         "price_unit": 132345.0, "discount": 0.0, "price_subtotal": 132345.0},
        {"id": 1004, "order_id": [102, "S00102"], "product_id": [21, nama_p[21]], "product_uom_qty": 3.0,
         "price_unit": 45000.0, "discount": 0.0, "price_subtotal": 135000.0},
        {"id": 1005, "order_id": [103, "S00103"], "product_id": [25, nama_p[25]], "product_uom_qty": 6.0,
         "price_unit": 210000.0, "discount": 0.0, "price_subtotal": 1260000.0},
        {"id": 1006, "order_id": [95, "S00095"], "product_id": [25, nama_p[25]], "product_uom_qty": 4.0,
         "price_unit": 225000.0, "discount": 0.0, "price_subtotal": 900000.0},
    ]

    def fk(i, nama, pid, jenis, tgl, due, dpp, tax, sisa, state="posted", bayar="not_paid"):
        tanda = -1 if jenis == "out_refund" else 1
        return {"id": i, "name": nama, "partner_id": [pid, p[pid]], "move_type": jenis, "state": state,
                "invoice_date": tgl, "invoice_date_due": due, "amount_untaxed_signed": tanda * dpp,
                "amount_tax_signed": tanda * tax, "amount_total_signed": tanda * round(dpp + tax, 2),
                "amount_residual_signed": tanda * sisa, "payment_state": bayar, "currency_id": idr}
    faktur = [
        fk(201, "INV/2026/00201", 3, "out_invoice", "2026-09-30", "2026-10-14", 332345.0, 36557.95, 368902.95),
        fk(202, "INV/2026/00202", 12, "out_invoice", "2026-09-30", "2026-10-30", 1260000.0, 138600.0, 1398600.0),
        fk(203, "RINV/2026/00007", 8, "out_refund", "2026-09-30", "2026-09-30", 45000.0, 4950.0, 49950.0),
        fk(180, "INV/2026/00180", 9, "out_invoice", "2026-07-01", "2026-07-06", 1250000.0, 137500.0, 1387500.0),
        fk(185, "INV/2026/00185", 10, "out_invoice", "2026-08-10", "2026-08-24", 2000000.0, 220000.0, 1110000.0,
           bayar="partial"),
        fk(190, "INV/2026/00190", 11, "out_invoice", "2026-09-10", "2026-09-17", 450000.0, 49500.0, 499500.0),
        fk(192, "INV/2026/00192", 3, "out_invoice", "2026-09-20", "2026-10-04", 900000.0, 99000.0, 999000.0),
        fk(193, "INV/2026/00193", 13, "out_invoice", "2026-09-15", "2026-09-29", 90000.0, 9900.0, 0.0,
           bayar="in_payment"),
        fk(194, "INV/2026/00194", 12, "out_invoice", "2026-09-01", "2026-09-15", 300000.0, 33000.0, 0.0, bayar="paid"),
        fk(195, "INV/2026/00195", 9, "out_invoice", "2026-09-29", "2026-10-29", 700000.0, 77000.0, 777000.0,
           state="draft"),
        fk(170, "INV/2026/00170", 12, "out_invoice", "2026-05-20", "2026-06-19", 5100000.0, 561000.0, 5661000.0),
    ]
    user = [{"id": 2, "name": "Administrator", "login": "admin@tokomaju.test", "share": False,
             "company_id": [1, "Toko Maju Kopi"]},
            {"id": 6, "name": "Bot Laporan", "login": "bot-laporan@tokomaju.test", "share": False,
             "company_id": [1, "Toko Maju Kopi"]},
            {"id": 7, "name": "Bot Penjualan", "login": "bot-penjualan@tokomaju.test", "share": False,
             "company_id": [1, "Toko Maju Kopi"]}]
    return {
        "res.partner": partner, "product.product": produk_rec, "stock.warehouse.orderpoint": orderpoint,
        "sale.order": pesanan, "sale.order.line": baris, "account.move": faktur, "res.users": user,
        "res.company": [{"id": 1, "name": "Toko Maju Kopi", "currency_id": idr}],
        "ir.config_parameter": [{"id": 1, "key": "web.base.url", "value": "http://localhost:8069"}],
    }


class Tiruan:
    def __init__(self, versi=19, mode=None):
        self.versi = versi
        self.mode = set(mode or [])
        self.data = data_awal(versi)
        self.log = []          # (protokol, model, metode)
        self.header = []       # header Authorization / body mentah untuk uji "kunci tidak bocor"
        self.kunci_kedaluwarsa = set()
        self.kunci_lambat_detik = 3.0
        self.kunci = threading.Lock()

    # ------------------------------------------------------------ domain
    def cocok(self, r, domain):
        stack = []
        for term in reversed(domain or []):
            if term == "|":
                a, b = stack.pop(), stack.pop()
                stack.append(a or b)
            elif term == "&":
                a, b = stack.pop(), stack.pop()
                stack.append(a and b)
            elif term == "!":
                stack.append(not stack.pop())
            else:
                stack.append(self.term(r, term))
        return all(stack)

    def term(self, r, term):
        f, op, v = term
        if f not in r and f != "id":
            raise ValueError("Invalid field {!r} in leaf {!r}".format(f, tuple(term)))
        x = r.get(f)
        if isinstance(x, list) and len(x) == 2 and isinstance(x[0], int):
            x = x[0]
        if op == "=":
            return x == v
        if op == "!=":
            return x != v
        if op == "in":
            return x in v
        if op == "not in":
            return x not in v
        if op in ("ilike", "=ilike"):
            if x in (False, None):
                return False
            pola = str(v).lower().replace("%", "")
            return (pola in str(x).lower()) if op == "ilike" else str(x).lower() == pola
        a, b = x, v
        if isinstance(a, str) and isinstance(b, str):
            pass
        return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]

    def model(self, nama):
        if "tanpa_stok" in self.mode and nama in ("stock.warehouse.orderpoint",):
            raise KeyError(nama)
        if nama not in self.data:
            raise KeyError(nama)
        return self.data[nama]

    def fields_get(self, model):
        recs = self.model(model)
        f = {"id": {"type": "integer"}}
        for r in recs:
            for k, v in r.items():
                f.setdefault(k, {"type": "many2one" if isinstance(v, list) else type(v).__name__})
        if model == "product.product" and "tanpa_stok" in self.mode:
            f.pop("qty_available", None)
            f.pop("virtual_available", None)
        return f

    def pilih(self, r, fields, model):
        semua = self.fields_get(model)
        out = {"id": r["id"]}
        for f in fields or [k for k in r]:
            if f not in semua:
                raise ValueError("Invalid field {!r} on model {!r}".format(f, model))
            out[f] = copy.deepcopy(r.get(f, False))
        return out

    # ------------------------------------------------------------ eksekusi
    def jalankan(self, user, model, metode, ids=None, kw=None):
        kw = kw or {}
        self.log.append((model, metode))
        if "tolak_semua" in self.mode and model not in ("res.users", "res.company") and metode != "fields_get":
            raise PermissionError("You are not allowed to access '{}' records.".format(model))
        if model == "ir.config_parameter" and user["peran"] != "admin":
            raise PermissionError("You are not allowed to access 'System Parameter' (ir.config_parameter) records.")
        if metode == "context_get":
            return {"lang": "id_ID", "tz": "Asia/Jakarta", "uid": user["uid"]}
        recs = self.model(model)
        if metode == "fields_get":
            return self.fields_get(model)
        if metode == "search_count":
            return sum(1 for r in recs if self.cocok(r, kw.get("domain") or []))
        if metode == "search_read":
            hasil = [r for r in recs if self.cocok(r, kw.get("domain") or [])]
            order = kw.get("order")
            if order:
                f, _, arah = order.partition(" ")
                hasil.sort(key=lambda r: (r.get(f) is False, str(r.get(f))), reverse=arah.strip().lower() == "desc")
            off, lim = int(kw.get("offset") or 0), kw.get("limit")
            hasil = hasil[off: off + lim] if lim else hasil[off:]
            return [self.pilih(r, kw.get("fields"), model) for r in hasil]
        if metode == "read":
            ada = {r["id"]: r for r in recs}
            if any(i not in ada for i in ids):
                raise LookupError("Record does not exist or has been deleted.")
            return [self.pilih(ada[i], kw.get("fields"), model) for i in ids]
        if metode == "create" and model == "sale.order":
            if user["peran"] == "baca":
                raise PermissionError("You are not allowed to create 'Sales Order' (sale.order) records.")
            return [self.buat_so(v) for v in kw["vals_list"]]
        if metode in ("unlink", "write", "action_confirm", "action_post"):
            raise AssertionError("SKILL TIDAK BOLEH MEMANGGIL " + metode)
        raise AttributeError("The method '{}' does not exist on the model '{}'".format(metode, model))

    def buat_so(self, v):
        with self.kunci:
            so = self.data["sale.order"]
            baru = max(r["id"] for r in so) + 1
            pid = v["partner_id"]
            pel = [r for r in self.data["res.partner"] if r["id"] == pid]
            if not pel:
                raise LookupError("Record does not exist or has been deleted.")
            dpp = pajak = 0.0
            produk = {r["id"]: r for r in self.data["product.product"]}
            for _, _, ln in v.get("order_line") or []:
                sub = round(ln["product_uom_qty"] * ln["price_unit"] * (1 - ln.get("discount", 0) / 100.0), 2)
                dpp += sub
                pajak += round(sub * 0.11, 2)
                self.data["sale.order.line"].append({
                    "id": 5000 + len(self.data["sale.order.line"]), "order_id": [baru, "S%05d" % baru],
                    "product_id": [ln["product_id"], produk[ln["product_id"]]["display_name"]],
                    "product_uom_qty": ln["product_uom_qty"], "price_unit": ln["price_unit"],
                    "discount": ln.get("discount", 0.0), "price_subtotal": sub})
            so.append({"id": baru, "name": "S%05d" % baru, "partner_id": [pid, pel[0]["name"]],
                       "date_order": "2026-09-30 03:00:00", "state": "draft", "amount_untaxed": round(dpp, 2),
                       "amount_tax": round(pajak, 2), "amount_total": round(dpp + pajak, 2),
                       "currency_id": [12, "IDR"], "origin": v.get("origin", False),
                       "create_date": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                       "validity_date": v.get("validity_date", False)})
            return baru


def buat_handler(t):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def kirim(self, status, isi, ctype="application/json", header=None):
            raw = isi if isinstance(isi, bytes) else isi.encode("utf-8")
            self.send_response(status)
            for k, v in (header or {}).items():
                self.send_header(k, v)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            try:
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def gangguan_umum(self):
            if "redirect" in t.mode:
                self.kirim(303, "", "text/html", {"Location": "https://login.contoh-lain.test/web/login"})
                return True
            if "bukan_odoo" in t.mode:
                self.kirim(200, "<html><body>Selamat datang di router</body></html>", "text/html")
                return True
            return False

        def do_GET(self):
            t.header.append(dict(self.headers))
            if self.gangguan_umum():
                return
            if self.path == "/web/version" and t.versi >= 19:
                self.kirim(200, json.dumps({"version_info": [t.versi, 0, 0, "final", 0, ""],
                                            "version": "{}.0".format(t.versi)}))
            else:
                self.kirim(404, "<html><title>404: Not Found</title></html>", "text/html")

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(n)
            t.header.append(dict(self.headers))
            if self.gangguan_umum():
                return
            if self.path.startswith("/xmlrpc/2/"):
                if "xmlrpc_hilang" in t.mode:
                    self.kirim(404, "<html><title>404: Not Found</title></html>", "text/html")
                    return
                return self.xmlrpc(self.path.rsplit("/", 1)[1], body)
            m = re.fullmatch(r"/json/2/([a-z_.]+)/([a-z_]+)", self.path)
            if m and t.versi >= 19:
                return self.json2(m.group(1), m.group(2), body)
            self.kirim(404, "<html><title>404: Not Found</title></html>", "text/html")

        # -------------------------------------------------- XML-RPC
        def fault(self, kode, teks):
            self.kirim(200, xmlrpc.client.dumps(xmlrpc.client.Fault(kode, teks), methodresponse=True), "text/xml")

        def xmlrpc(self, layanan, body):
            params, metode = xmlrpc.client.loads(body, use_builtin_types=True)
            if layanan == "common":
                if metode == "version":
                    hasil = {"server_version": "{}.0".format(t.versi),
                             "server_version_info": [t.versi, 0, 0, "final", 0, ""], "server_serie": "{}.0".format(t.versi),
                             "protocol_version": 1}
                elif metode == "authenticate":
                    db, login, kunci, _ = params
                    u = KUNCI.get(kunci)
                    ok = db == DB and u and u["login"] == login and kunci not in t.kunci_kedaluwarsa
                    hasil = u["uid"] if ok else False
                else:
                    return self.fault(1, "Traceback...\nNameError: method {} not found".format(metode))
                return self.kirim(200, xmlrpc.client.dumps((hasil,), methodresponse=True, allow_none=False), "text/xml")
            if layanan != "object" or metode != "execute_kw":
                return self.fault(1, "Traceback...\nNameError: service not found")
            db, uid, kunci, model, met, args, kw = (list(params) + [{}])[:7]
            u = KUNCI.get(kunci)
            if db != DB or not u or u["uid"] != uid or kunci in t.kunci_kedaluwarsa:
                return self.fault(3, "Access Denied")
            ids = None
            if met in ("read",):
                ids = args[0] if args else kw.pop("ids", [])
            if met == "create":
                kw = {"vals_list": args[0] if isinstance(args[0], list) else [args[0]]}
            status = self.gangguan_tulis(model, met)
            if status == "500":
                return self.kirim(500, "<html><title>500 Internal Server Error</title></html>", "text/html")
            try:
                hasil = t.jalankan(u, model, met, ids, kw)
            except KeyError as e:
                return self.fault(2, "Object {} doesn't exist".format(e.args[0]))
            except PermissionError as e:
                return self.fault(4, str(e))
            except LookupError as e:
                return self.fault(2, str(e))
            except (ValueError, AttributeError) as e:
                return self.fault(1, "Traceback (most recent call last):\n  File \"odoo/service/model.py\"\n{}: {}"
                                  .format(type(e).__name__, e))
            if status == "lambat":
                time.sleep(t.kunci_lambat_detik)
            self.kirim(200, xmlrpc.client.dumps((hasil,), methodresponse=True, allow_none=False), "text/xml")

        def gangguan_tulis(self, model, met):
            if met == "create" and "error500_create" in t.mode:
                t.jalankan(KUNCI[KUNCI_JUAL], model, met, None, {"vals_list": []})  # dicatat, tidak membuat
                return "500"
            if met == "create" and "timeout_create" in t.mode:
                return "lambat"
            return None

        # -------------------------------------------------- JSON-2
        def jgalat(self, status, nama, pesan):
            self.kirim(status, json.dumps({"name": nama, "message": pesan, "arguments": [pesan], "context": {},
                                           "debug": "Traceback (most recent call last): ..."}))

        def json2(self, model, met, body):
            auth = self.headers.get("Authorization") or ""
            kunci = auth[7:] if auth.lower().startswith("bearer ") else ""
            u = KUNCI.get(kunci)
            if not u or kunci in t.kunci_kedaluwarsa:
                return self.jgalat(401, "werkzeug.exceptions.Unauthorized", "Invalid apikey")
            dbh = self.headers.get("X-Odoo-Database")
            if dbh and dbh != DB:
                return self.jgalat(404, "werkzeug.exceptions.NotFound", "database not found")
            try:
                data = json.loads(body or b"{}")
            except ValueError:
                return self.jgalat(400, "werkzeug.exceptions.BadRequest", "bad json")
            ids = data.pop("ids", None)
            data.pop("context", None)
            status = self.gangguan_tulis(model, met)
            if status == "500":
                return self.jgalat(500, "builtins.Exception", "Internal Server Error")
            try:
                hasil = t.jalankan(u, model, met, ids, data)
            except KeyError as e:
                return self.jgalat(404, "werkzeug.exceptions.NotFound", "Model {} not found".format(e.args[0]))
            except PermissionError as e:
                return self.jgalat(403, "odoo.exceptions.AccessError", str(e))
            except LookupError as e:
                return self.jgalat(422, "odoo.exceptions.MissingError", str(e))
            except AttributeError as e:
                return self.jgalat(404, "werkzeug.exceptions.NotFound", str(e))
            except ValueError as e:
                return self.jgalat(422, "builtins.ValueError", str(e))
            if status == "lambat":
                time.sleep(t.kunci_lambat_detik)
            self.kirim(200, json.dumps(hasil))
    return H


def buat_server(versi=19, mode=None, port=0):
    t = Tiruan(versi, mode)
    srv = ThreadingHTTPServer(("127.0.0.1", port), buat_handler(t))
    srv.daemon_threads = True
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    return srv, t


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Server Odoo TIRUAN untuk uji (bukan Odoo sungguhan)")
    ap.add_argument("--port", type=int, default=8069)
    ap.add_argument("--versi", type=int, default=19)
    ap.add_argument("--mode", action="append", default=[])
    a = ap.parse_args()
    srv, _ = buat_server(a.versi, a.mode, a.port)
    print("Server Odoo tiruan {} di http://127.0.0.1:{} (Ctrl+C untuk berhenti)".format(a.versi, a.port), flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        srv.shutdown()
