#!/usr/bin/env python3
"""Uji regresi dolibarr.py memakai server Dolibarr TIRUAN (http.server standar).

Bentuk respons tiruan diambil dari respons ASLI Dolibarr 24.0.1 yang direkam di
tests/fixtures/dolibarr-24.0.1.json (bukan tebakan). Server tiruan juga mencatat setiap
permintaan sehingga uji bisa memastikan: perintah baca tidak pernah menulis, tidak ada
panggilan validasi/bayar/hapus, dan kunci API tidak pernah bocor ke keluaran/URL.

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
Tidak butuh internet, Dolibarr, atau paket tambahan.
"""
import copy
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.parse
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP = os.path.join(SINI, "..", "scripts", "dolibarr.py")
FIX = json.load(open(os.path.join(SINI, "fixtures", "dolibarr-24.0.1.json"), encoding="utf-8"))
KUNCI_TULIS = "kunciujiTULIS-0123456789abcdef"
KUNCI_BACA = "kunciujiBACA-0123456789abcdef"
TS_2026_09_24_WIB_SIANG = 1790226000  # 2026-09-24 12:00 WIB


def ts(tgl):
    """'2026-09-24' -> timestamp tengah malam WIB (seperti Dolibarr dengan PHP tz Asia/Jakarta)."""
    import datetime as dt
    y, m, d = map(int, tgl.split("-"))
    return int(dt.datetime(y, m, d, tzinfo=dt.timezone(dt.timedelta(hours=7))).timestamp())


def bulat2(d):
    return Decimal(d).quantize(Decimal("0.01"), ROUND_HALF_UP)


def s8(d):
    return "{:.8f}".format(Decimal(d))


class Keadaan:
    """Isi 'database' tiruan + mode galat."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.mode = set()
        self.versi = FIX["status"]["success"]["dolibarr_version"]
        self.log = []
        self.pelanggan = copy.deepcopy(FIX["thirdparties"])
        self.produk = copy.deepcopy(FIX["products_includestockdata"])
        self.invoice = copy.deepcopy(FIX["invoices_all"])
        self.next_tp = 100
        self.next_inv = 100


K = Keadaan()


def cocok_like(nilai, pola):
    pola = pola.strip("%").lower()
    return pola in str(nilai or "").lower()


def saring(daftar, sqlfilters, peta):
    """Tiru subset sqlfilters Dolibarr yang dipakai script: like (OR), in, =."""
    if not sqlfilters:
        return daftar
    if not re.fullmatch(r"[\w\s\.\(\):'%,=<>\-]+", sqlfilters):
        raise ValueError("sqlfilters tidak valid")
    hasil = []
    kondisi = re.findall(r"\(([\w\.]+):(like|in|=):([^()]*)\)", sqlfilters)
    for o in daftar:
        ok = False
        for kol, op, nilai in kondisi:
            v = o.get(peta.get(kol, kol.split(".")[-1]))
            nilai = nilai.strip("'")
            if op == "like" and cocok_like(v, nilai):
                ok = True
            elif op == "in" and str(v) in nilai.split(","):
                ok = True
            elif op == "=" and kol == "t.datef":
                ok = ok or (v and abs(int(v) - ts(nilai)) < 86400 and int(v) >= ts(nilai))
        if ok:
            hasil.append(o)
    return hasil


def properti(o, props):
    if not props:
        return o
    keep = props.split(",")
    return {k: v for k, v in o.items() if k in keep}


class Tiruan(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def kirim(self, kode, body, jenis="application/json"):
        data = body if isinstance(body, (bytes, str)) else json.dumps(body, indent=4)
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(kode)
        self.send_header("Content-Type", jenis)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def galat(self, kode, pesan):
        self.kirim(kode, {"error": {"code": kode, "message": pesan}, "debug": {"source": "tiruan"}})

    def handle_one(self, metode):
        u = urllib.parse.urlsplit(self.path)
        q = dict(urllib.parse.parse_qsl(u.query))
        panjang = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(panjang) or b"null") if panjang else None
        K.log.append({"metode": metode, "path": u.path, "query": q, "body": body,
                      "kunci": self.headers.get("DOLAPIKEY"), "url_mentah": self.path})
        if "redirect" in K.mode:
            self.send_response(302)
            self.send_header("Location", "http://127.0.0.1:{}/lain{}".format(self.server.server_port, self.path))
            self.end_headers()
            return
        m = re.match(r"^/dolibarr/api/index\.php/(.*)$", u.path)
        if not m:
            return self.kirim(404, "<html><body><h1>Not Found</h1></body></html>", "text/html")
        jalur = m.group(1)
        if "api_mati" in K.mode:
            return self.kirim(200, FIX["api_module_disabled_body_id"], "text/html; charset=UTF-8")
        kunci = self.headers.get("DOLAPIKEY")
        if kunci not in (KUNCI_TULIS, KUNCI_BACA):
            return self.kirim(401, FIX["error_401_body"])
        tulis = kunci == KUNCI_TULIS
        try:
            return self.rute(metode, jalur, q, body, tulis)
        except ValueError as e:
            return self.galat(400, str(e))

    def rute(self, metode, jalur, q, body, tulis):
        mati = {x.split(":", 1)[1] for x in K.mode if x.startswith("modul_mati:")}
        tolak = {x.split(":", 1)[1] for x in K.mode if x.startswith("403:")}
        root = jalur.split("/")[0]
        if root in mati:
            return self.kirim(501, FIX["error_501_body"], "text/html")
        if root in tolak:
            return self.kirim(403, FIX["error_403_body"])
        if metode == "GET" and jalur == "status":
            st = copy.deepcopy(FIX["status"])
            st["success"]["dolibarr_version"] = K.versi
            return self.kirim(200, st)
        if metode == "GET" and jalur == "users/info":
            if not tulis:
                return self.galat(403, "Forbidden: Not allowed")
            return self.kirim(200, FIX["users_info_tulis"])
        # ---- pihak ketiga
        if jalur == "thirdparties" and metode == "GET":
            d = saring(K.pelanggan, q.get("sqlfilters"), {"t.nom": "name", "t.rowid": "id", "t.phone": "phone",
                                                           "t.code_client": "code_client"})
            d = self.halaman(d, q)
            if not d:
                return self.kirim(404, FIX["error_404_thirdparties_empty_body"])
            return self.kirim(200, [properti(x, q.get("properties")) for x in d])
        m = re.fullmatch(r"thirdparties/(\d+)", jalur)
        if m and metode == "GET":
            for t in K.pelanggan:
                if t["id"] == m.group(1):
                    return self.kirim(200, t)
            return self.galat(404, "Not Found: Thirdparty not found")
        if jalur == "thirdparties" and metode == "POST":
            if not tulis:
                return self.kirim(403, FIX["error_403_body"])
            K.next_tp += 1
            t = {"id": str(K.next_tp), "name": body["name"], "name_alias": "", "status": "1", "client": "1",
                 "code_client": "CU2609-{:05d}".format(K.next_tp), "phone": body.get("phone"),
                 "email": body.get("email"), "town": body.get("town")}
            K.pelanggan.append(t)
            return self.kirim(200, K.next_tp)
        # ---- produk & gudang
        if jalur == "products" and metode == "GET":
            d = saring(K.produk, q.get("sqlfilters"), {"t.ref": "ref", "t.label": "label", "t.barcode": "barcode"})
            if q.get("mode") == "1":
                d = [p for p in d if p["type"] == "0"]
            d = self.halaman(d, q)
            if q.get("includestockdata") != "1":
                d = [dict(p, stock_warehouse=[], stock_theorique=None) for p in d]
            return self.kirim(200, [properti(x, q.get("properties")) for x in d])
        m = re.fullmatch(r"products/ref/(.+)", jalur)
        if m and metode == "GET":
            ref = urllib.parse.unquote(m.group(1))
            for p in K.produk:
                if p["ref"] == ref:
                    return self.kirim(200, p)
            return self.kirim(404, FIX["error_404_product_ref_body"])
        if jalur == "warehouses" and metode == "GET":
            return self.kirim(200, [{"id": "1", "label": "Gudang Utama", "statut": "1"}])
        # ---- invoice
        if jalur == "invoices" and metode == "GET":
            peta = {"draft": "0", "unpaid": "1", "paid": "2", "cancelled": "3"}
            d = K.invoice
            if q.get("status"):
                d = [i for i in d if i["statut"] == peta[q["status"]]]
            if q.get("thirdparty_ids"):
                d = [i for i in d if i["socid"] in q["thirdparty_ids"].split(",")]
            d = saring(d, q.get("sqlfilters"), {"t.datef": "date"})
            d = self.halaman(d, q)
            return self.kirim(200, [properti(x, q.get("properties")) for x in d])
        m = re.fullmatch(r"invoices/(\d+)", jalur)
        if m and metode == "GET":
            for i in K.invoice:
                if i["id"] == m.group(1):
                    return self.kirim(200, i)
            return self.galat(404, "Not Found: Invoice not found")
        if jalur == "invoices" and metode == "POST":
            if not tulis:
                return self.kirim(403, FIX["error_403_body"])
            K.next_inv += 1
            K.invoice.append({"id": str(K.next_inv), "ref": "(PROV{})".format(K.next_inv), "socid": str(body["socid"]),
                              "type": "0", "statut": "0", "status": "0", "paye": "0", "date": body["date"],
                              "date_lim_reglement": body.get("date_lim_reglement"), "total_ht": s8(0),
                              "total_tva": s8(0), "total_ttc": s8(0), "remaintopay": "0", "totalpaid": 0,
                              "multicurrency_code": "IDR", "note_private": body.get("note_private"), "lines": []})
            return self.kirim(200, K.next_inv)
        m = re.fullmatch(r"invoices/(\d+)/lines", jalur)
        if m and metode == "POST":
            if "gagal_baris_2" in K.mode and body["desc"] and len([i for i in K.invoice if i["id"] == m.group(1)][0]
                                                                    ["lines"]) == 1:
                return self.galat(400, "Bad Request: Unable to insert the new line. Check your inputs.")
            inv = [i for i in K.invoice if i["id"] == m.group(1)][0]
            # Cara hitung Dolibarr (price2num 'MT', 2 desimal, per baris, half-up)
            qty, pu, disk, tx = (Decimal(str(body[k])) for k in ("qty", "subprice", "remise_percent", "tva_tx"))
            ht = bulat2(qty * pu * (100 - disk) / 100)
            tva = bulat2(ht * tx / 100)
            inv["lines"].append({"desc": body["desc"], "qty": str(qty), "subprice": s8(pu), "tva_tx": str(tx),
                                 "remise_percent": str(disk), "total_ht": s8(ht), "total_tva": s8(tva),
                                 "total_ttc": s8(ht + tva), "fk_product": body.get("fk_product"),
                                 "product_type": str(body.get("product_type"))})
            for k in ("total_ht", "total_tva", "total_ttc"):
                inv[k] = s8(sum(Decimal(x[k]) for x in inv["lines"]))
            return self.kirim(200, len(inv["lines"]))
        return self.kirim(501, FIX["error_501_body"], "text/html")

    def halaman(self, d, q):
        lim = int(q.get("limit", 100))
        hal = int(q.get("page", 0))
        return d[hal * lim:(hal + 1) * lim]

    def do_GET(self):
        self.handle_one("GET")

    def do_POST(self):
        self.handle_one("POST")

    def do_PUT(self):
        self.handle_one("PUT")

    def do_DELETE(self):
        self.handle_one("DELETE")


def port_bebas():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class UjiDolibarr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Tiruan)
        cls.port = cls.srv.server_port
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.tmp = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        K.reset()

    def jalan(self, *argv, kunci=KUNCI_TULIS, url=None, env_tambah=None, masukan=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith("DOLIBARR")}
        env["HOME"] = self.tmp
        env["USERPROFILE"] = self.tmp
        if kunci:
            env["DOLIBARR_API_KEY"] = kunci
        env["DOLIBARR_URL"] = url or "http://127.0.0.1:{}/dolibarr".format(self.port)
        env.update(env_tambah or {})
        p = subprocess.run([sys.executable, SKRIP] + list(argv), capture_output=True, text=True, env=env,
                           input=masukan, timeout=60)
        for k in (KUNCI_TULIS, KUNCI_BACA):
            self.assertNotIn(k, p.stdout + p.stderr, "kunci API bocor ke keluaran")
        return p

    def tulis_dilakukan(self):
        return [x for x in K.log if x["metode"] != "GET"]

    def cek_tanpa_aksi_terlarang(self):
        for x in K.log:
            self.assertNotEqual(x["metode"], "DELETE")
            self.assertNotEqual(x["metode"], "PUT")
            self.assertNotRegex(x["path"], r"validate|payments|settopaid|sendbyemail|settodraft|reopen")
            self.assertNotIn("DOLAPIKEY", x["url_mentah"])

    # ---------------------------------------------------------- cek & galat koneksi
    def test_cek_normal(self):
        p = self.jalan("cek")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Versi Dolibarr: 24.0.1", p.stdout)
        self.assertIn("****cdef", p.stdout)
        self.assertIn("[x] buat/ubah draf invoice", p.stdout)
        self.assertIn("aktif, bisa dibaca", p.stdout)
        self.assertEqual(self.tulis_dilakukan(), [])
        self.assertTrue(all(x["kunci"] == KUNCI_TULIS for x in K.log), "header DOLAPIKEY harus dikirim")

    def test_cek_kunci_baca_tanpa_info_user(self):
        p = self.jalan("cek", kunci=KUNCI_BACA)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Hak diperkirakan dari uji baca", p.stdout)

    def test_cek_versi_belum_diuji(self):
        K.versi = "25.0.0"
        p = self.jalan("cek")
        self.assertIn("belum diuji", p.stdout)

    def test_kunci_salah_401(self):
        p = self.jalan("cek", kunci="kunci-salah-sekali-123")
        self.assertEqual(p.returncode, 5)
        self.assertIn("401", p.stderr)
        self.assertNotIn("kunci-salah-sekali-123", p.stdout + p.stderr)

    def test_dolibarr_mati(self):
        p = self.jalan("stok", url="http://127.0.0.1:{}/dolibarr".format(port_bebas()))
        self.assertEqual(p.returncode, 3)
        self.assertIn("tidak bisa dihubungi", p.stderr)
        self.assertIn("DoliWamp", p.stderr)

    def test_modul_api_belum_aktif(self):
        K.mode.add("api_mati")
        p = self.jalan("cek")
        self.assertEqual(p.returncode, 4)
        self.assertIn("API / Web services", p.stderr)

    def test_modul_invoice_belum_aktif_501(self):
        K.mode.add("modul_mati:invoices")
        p = self.jalan("cek")
        self.assertEqual(p.returncode, 0)
        self.assertIn("Nota/Invoice pelanggan: BELUM AKTIF", p.stdout)
        p = self.jalan("piutang")
        self.assertEqual(p.returncode, 4)

    def test_url_salah_404_html(self):
        p = self.jalan("stok", url="http://127.0.0.1:{}/bukan-dolibarr".format(self.port))
        self.assertEqual(p.returncode, 2)
        self.assertIn("DOLIBARR_URL", p.stderr)

    def test_redirect_ditolak_kunci_tidak_diteruskan(self):
        K.mode.add("redirect")
        p = self.jalan("stok")
        self.assertEqual(p.returncode, 6)
        self.assertIn("mengalihkan", p.stderr)
        self.assertEqual([x for x in K.log if x["path"].startswith("/lain")], [])

    def test_json_galat(self):
        K.mode.add("api_mati")
        p = self.jalan("cek", "--json")
        d = json.loads(p.stdout)
        self.assertFalse(d["ok"])
        self.assertEqual(d["kode_keluar"], 4)

    # ---------------------------------------------------------- keamanan URL & kunci
    def test_url_luar_ditolak_tanpa_izin(self):
        p = self.jalan("cek", url="http://192.168.1.20/dolibarr")
        self.assertEqual(p.returncode, 2)
        self.assertIn("bukan komputer ini", p.stderr)
        self.assertEqual(K.log, [])

    def test_url_internet_http_ditolak_walau_diizinkan(self):
        p = self.jalan("cek", "--izinkan-url-luar", url="http://erp.contoh.co.id/dolibarr")
        self.assertEqual(p.returncode, 2)
        self.assertIn("https", p.stderr)

    def test_url_lan_http_diizinkan_dengan_peringatan(self):
        p = self.jalan("cek", "--izinkan-url-luar", url="http://192.168.255.254:9/dolibarr")
        self.assertEqual(p.returncode, 3)  # lolos validasi, lalu gagal konek (tidak ada server)

    def test_url_dengan_sandi_ditolak(self):
        p = self.jalan("cek", url="http://admin:rahasia@localhost/dolibarr")
        self.assertEqual(p.returncode, 2)
        self.assertNotIn("rahasia", p.stdout + p.stderr.replace("sandi", ""))

    def test_tanpa_kunci(self):
        p = self.jalan("cek", kunci=None)
        self.assertEqual(p.returncode, 5)
        self.assertIn("simpan-kunci", p.stderr)

    @unittest.skipIf(os.name == "nt", "izin file POSIX")
    def test_simpan_kunci_dan_izin_file(self):
        p = self.jalan("simpan-kunci", kunci=None, masukan=KUNCI_TULIS + "\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        path = os.path.join(self.tmp, ".komunitech", "dolibarr-kunci.txt")
        self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
        p = self.jalan("cek", kunci=None)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("dari file", p.stdout)
        os.chmod(path, 0o644)
        p = self.jalan("cek", kunci=None)
        self.assertEqual(p.returncode, 5)
        self.assertIn("chmod 600", p.stderr)
        os.remove(path)

    def test_kunci_tidak_ada_di_json(self):
        p = self.jalan("cek", "--json")
        d = json.loads(p.stdout)
        self.assertTrue(d["ok"])
        self.assertEqual(d["kunci"], "****cdef")

    # ---------------------------------------------------------- pelanggan
    def test_cari_pelanggan(self):
        p = self.jalan("pelanggan", "cari", "maju")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("ID 1: CV Maju Jaya", p.stdout)
        self.assertNotIn("Sinar", p.stdout)

    def test_cari_pelanggan_kosong_404_jadi_daftar_kosong(self):
        p = self.jalan("pelanggan", "cari", "zzz')(drop")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Tidak ada pelanggan", p.stdout)
        filt = [x["query"].get("sqlfilters", "") for x in K.log if x["path"].endswith("thirdparties")][0]
        self.assertNotIn("')(", filt.replace("%')", "").replace("('", ""))

    def test_tambah_pelanggan_pratinjau_tidak_menulis(self):
        p = self.jalan("pelanggan", "tambah", "--nama", "Warung Bu Sari", "--telepon", "0812-3456-7890")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("PRATINJAU", p.stdout)
        self.assertIn("081234567890", p.stdout)
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_tambah_pelanggan_ya(self):
        p = self.jalan("pelanggan", "tambah", "--nama", "Warung Bu Sari", "--kota", "Solo", "--ya")
        self.assertEqual(p.returncode, 0, p.stderr)
        tulis = self.tulis_dilakukan()
        self.assertEqual(len(tulis), 1)
        self.assertEqual(tulis[0]["body"]["name"], "Warung Bu Sari")
        self.assertEqual(tulis[0]["body"]["client"], 1)
        self.assertEqual(tulis[0]["body"]["code_client"], "auto")
        self.assertIn("TERSIMPAN: ID 101", p.stdout)

    def test_tambah_pelanggan_nama_mirip_ditahan(self):
        p = self.jalan("pelanggan", "tambah", "--nama", "Maju Jaya", "--ya")
        self.assertEqual(p.returncode, 0)
        self.assertIn("nama mirip", p.stdout)
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_tambah_pelanggan_input_buruk(self):
        self.assertEqual(self.jalan("pelanggan", "tambah", "--nama", "X", "--ya").returncode, 2)
        self.assertEqual(self.jalan("pelanggan", "tambah", "--nama", "Budi", "--telepon", "12").returncode, 2)
        self.assertEqual(self.jalan("pelanggan", "tambah", "--nama", "Budi", "--email", "bukan-email").returncode, 2)
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_kunci_baca_tidak_bisa_menulis(self):
        p = self.jalan("pelanggan", "tambah", "--nama", "Warung Baru Sekali", "--ya", kunci=KUNCI_BACA)
        self.assertEqual(p.returncode, 5)
        self.assertIn("403", p.stderr)

    # ---------------------------------------------------------- invoice
    ITEM = ["--item", "@KPI-250|3", "--item", "Gula Aren 1kg|2|32.500", "--item", "Ongkos kirim|1|12345"]

    def test_invoice_pratinjau_tidak_menulis(self):
        p = self.jalan("invoice", "buat", "--pelanggan", "2", *self.ITEM)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("PRATINJAU DRAF INVOICE", p.stdout)
        self.assertIn("DPP (jumlah harga sebelum pajak): Rp 332.345", p.stdout)
        self.assertIn("PPN: Rp 36.557 (dari Rp 36.557,95 dibulatkan ke bawah)", p.stdout)
        self.assertIn("TOTAL: Rp 368.902", p.stdout)
        self.assertIn("DPP nilai lain 11/12 (informasi faktur): Rp 304.649,58", p.stdout)
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_invoice_ya_draf_dan_banding(self):
        p = self.jalan("invoice", "buat", "--pelanggan", "2", *self.ITEM, "--ya", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        d = json.loads(p.stdout)
        self.assertTrue(d["dibuat"])
        self.assertEqual(d["status_dolibarr"], "0")
        self.assertEqual(d["hitungan"]["ppn"], 36557)
        self.assertEqual(d["dolibarr"]["ppn"], 36557.95)
        self.assertEqual(d["beda"], {"ppn": 0.95, "total": 0.95})
        tulis = self.tulis_dilakukan()
        self.assertEqual([x["path"].split("index.php/")[1] for x in tulis],
                         ["invoices", "invoices/101/lines", "invoices/101/lines", "invoices/101/lines"])
        kepala = tulis[0]["body"]
        self.assertEqual(kepala["socid"], 2)
        self.assertNotIn("lines", kepala)
        self.assertEqual(tulis[1]["body"]["fk_product"], 1)
        self.assertEqual(tulis[1]["body"]["subprice"], "85000.00000000")
        self.assertEqual(tulis[1]["body"]["tva_tx"], "11")
        self.assertEqual(tulis[2]["body"]["subprice"], "32500")
        self.cek_tanpa_aksi_terlarang()

    def test_invoice_ya_teks_beda(self):
        p = self.jalan("invoice", "buat", "--pelanggan", "2", *self.ITEM, "--ya")
        self.assertIn("TERSIMPAN SEBAGAI DRAF: (PROV101)", p.stdout)
        self.assertIn("BEDA dengan hitungan Komunitech: PPN +Rp 0,95; TOTAL +Rp 0,95", p.stdout)
        self.assertIn("Coretax", p.stdout)

    def test_invoice_cocok(self):
        p = self.jalan("invoice", "buat", "--pelanggan", "1", "--item", "Jasa desain|1|1.000.000", "--jasa", "--ya")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("COCOK", p.stdout)
        self.assertEqual(self.tulis_dilakukan()[1]["body"]["product_type"], 1)

    def test_invoice_dobel_ditahan(self):
        self.jalan("invoice", "buat", "--pelanggan", "2", *self.ITEM, "--ya")
        n = len(self.tulis_dilakukan())
        p = self.jalan("invoice", "buat", "--pelanggan", "2", *self.ITEM, "--ya")
        self.assertIn("DIBATALKAN", p.stdout)
        self.assertEqual(len(self.tulis_dilakukan()), n)
        p = self.jalan("invoice", "buat", "--pelanggan", "2", *self.ITEM, "--ya", "--tetap-buat")
        self.assertIn("(PROV102)", p.stdout)

    def test_invoice_tanggal_jam_siang_wib(self):
        self.jalan("invoice", "buat", "--pelanggan", "1", "--item", "A|1|1000", "--tanggal", "2026-09-24",
                   "--jatuh-tempo", "30", "--ya")
        kepala = self.tulis_dilakukan()[0]["body"]
        self.assertEqual(kepala["date"], TS_2026_09_24_WIB_SIANG)
        self.assertEqual(kepala["date_lim_reglement"], TS_2026_09_24_WIB_SIANG + 30 * 86400)

    def test_invoice_mewah_dan_diskon(self):
        p = self.jalan("invoice", "buat", "--pelanggan", "1", "--item", "Tas kulit|2|1.250.000|10",
                       "--item", "Dompet|3|333333", "--ppn", "mewah", "--json")
        d = json.loads(p.stdout)
        # Verifikasi independen: 2x1.250.000x90% = 2.250.000; 3x333.333 = 999.999; DPP 3.249.999
        self.assertEqual(d["hitungan"]["dpp"], 3249999)
        self.assertEqual(d["hitungan"]["ppn"], int((Decimal(3249999) * Decimal("0.12")).quantize(1, ROUND_FLOOR)))
        self.assertEqual(d["hitungan"]["ppn"], 389999)
        self.assertIsNone(d["hitungan"]["dpp_nilai_lain"])

    def test_invoice_diskon_pembulatan_baris(self):
        p = self.jalan("invoice", "buat", "--pelanggan", "1", "--item", "Kain|3|10.333|7,5", "--json")
        d = json.loads(p.stdout)
        # 3 x 10.333 x 92,5% = 28.674,075 -> Rp 28.674 (terdekat); PPN floor(28.674 x 11%) = 3.154
        self.assertEqual(d["items"][0]["total_baris"], 28674)
        self.assertEqual(d["hitungan"]["ppn"], 3154)

    def test_invoice_tanpa_ppn(self):
        p = self.jalan("invoice", "buat", "--pelanggan", "1", "--item", "Kue|10|5000", "--ppn", "tanpa", "--json")
        d = json.loads(p.stdout)
        self.assertEqual(d["hitungan"]["ppn"], 0)
        self.assertEqual(d["hitungan"]["total"], 50000)

    def test_invoice_input_buruk(self):
        kasus = [["--pelanggan", "1"], ["--pelanggan", "1", "--item", "Kopi|dua|1000"],
                 ["--pelanggan", "1", "--item", "Kopi|1"], ["--pelanggan", "1", "--item", "Kopi|0|1000"],
                 ["--pelanggan", "1", "--item", "Kopi|1|-5"], ["--pelanggan", "1", "--item", "Kopi|1|1000|150"],
                 ["--pelanggan", "abc", "--item", "Kopi|1|1000"], ["--pelanggan", "999", "--item", "Kopi|1|1000"],
                 ["--pelanggan", "1", "--item", "@TIDAKADA|1"], ["--pelanggan", "1", "--item", "A|1|1", "--tanggal", "besok lusa"]]
        for k in kasus:
            p = self.jalan("invoice", "buat", *k, "--ya")
            self.assertEqual(p.returncode, 2, "{} -> {} {}".format(k, p.returncode, p.stderr))
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_invoice_baris_gagal_dilaporkan_tanpa_hapus(self):
        K.mode.add("gagal_baris_2")
        p = self.jalan("invoice", "buat", "--pelanggan", "2", *self.ITEM, "--ya")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("baris 2 gagal", p.stdout)
        self.cek_tanpa_aksi_terlarang()

    # ---------------------------------------------------------- piutang
    def test_piutang_umur(self):
        p = self.jalan("piutang", "--per-tanggal", "2026-09-24", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        d = json.loads(p.stdout)
        # Dari data asli: IN2606-0003 sisa 1.387.000 (tempo 1/7, lewat 85), IN2608-0001 749.250 (lewat 23),
        # IN2609-0005 334.110 (lewat 1), IN2609-0004 108.225 (belum). IN2609-0002 sisa 0 -> catatan.
        self.assertEqual(d["jumlah"], 4)
        self.assertEqual(d["total"], 1387000 + 749250 + 334110 + 108225)
        self.assertEqual(d["umur"]["lewat 61-90 hari"]["nilai"], 1387000)
        self.assertEqual(d["umur"]["lewat 1-30 hari"]["jumlah"], 2)
        self.assertEqual(d["umur"]["belum jatuh tempo"]["nilai"], 108225)
        self.assertEqual(d["invoice"][0]["ref"], "IN2606-0003")
        self.assertEqual(d["invoice"][0]["hari_lewat"], 85)
        self.assertTrue(any("IN2609-0002" in c for c in d["catatan"]))
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_piutang_samarkan_dan_nota_kredit(self):
        K.invoice.append({"id": "90", "ref": "AV2609-0001", "socid": "1", "type": "2", "statut": "1",
                          "date": ts("2026-09-20"), "date_lim_reglement": ts("2026-09-20"),
                          "total_ttc": "-50000.00000000", "remaintopay": "-50000", "totalpaid": 0})
        p = self.jalan("piutang", "--per-tanggal", "2026-09-24", "--samarkan")
        self.assertIn("T.S.A.", p.stdout)
        self.assertNotIn("Sinar", p.stdout)
        self.assertNotIn("AV2609", p.stdout)

    def test_piutang_kosong(self):
        K.invoice = []
        p = self.jalan("piutang")
        self.assertEqual(p.returncode, 0)
        self.assertIn("Tidak ada invoice tervalidasi yang belum lunas", p.stdout)

    # ---------------------------------------------------------- stok
    def test_stok_menipis(self):
        K.produk.append({"id": "9", "ref": "SUSU", "label": "Susu UHT", "type": "0", "status": "1",
                         "stock_reel": -3, "seuil_stock_alerte": "5", "desiredstock": "0"})
        K.produk.append({"id": "10", "ref": "PAS", "label": "Pas batas", "type": "0", "status": "1",
                         "stock_reel": 10, "seuil_stock_alerte": "10", "desiredstock": None})
        K.produk.append({"id": "11", "ref": "NOB", "label": "Tanpa batas", "type": "0", "status": "1",
                         "stock_reel": 4, "seuil_stock_alerte": None, "desiredstock": None})
        p = self.jalan("stok", "--menipis", "--json")
        d = json.loads(p.stdout)
        status = {x["ref"]: x["status"] for x in d["produk"]}
        self.assertEqual(status, {"SUSU": "MINUS", "CUP-12": "HABIS", "KPI-250": "MENIPIS"})
        saran = {x["ref"]: x["saran_beli"] for x in d["produk"]}
        self.assertEqual(saran, {"SUSU": 8, "CUP-12": 20, "KPI-250": 23})  # ke stok ideal bila ada, else minimum
        self.assertEqual(d["tanpa_batas_minimum"], 1)
        self.assertNotIn("JSA-INST", p.stdout)  # jasa tidak punya stok
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_stok_cari_dan_kosong(self):
        p = self.jalan("stok", "gula")
        self.assertIn("GLA-1KG Gula Aren 1kg: stok 40 (min 5) aman", p.stdout)
        K.produk = []
        p = self.jalan("stok")
        self.assertEqual(p.returncode, 0)
        self.assertIn("Belum ada produk", p.stdout)

    # ---------------------------------------------------------- laporan harian
    def test_laporan_harian(self):
        p = self.jalan("laporan-harian", "--tanggal", "2026-09-24", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        d = json.loads(p.stdout)
        pj = d["bagian"]["penjualan"]
        # Data asli tanggal 24/9: IN2609-0002 (368.902,95) + IN2609-0004 (108.225); draf (PROV) tidak dihitung
        self.assertEqual(pj["nota"], 2)
        self.assertEqual(Decimal(str(pj["total"])), Decimal("477127.95"))
        self.assertEqual(d["bagian"]["piutang"]["terlambat"], 3)
        self.assertEqual(d["bagian"]["stok"]["perlu_perhatian"], 2)
        self.assertNotIn("Sinar", d["teks"])  # laporan terjadwal tanpa nama pelanggan
        self.assertNotIn("Maju", d["teks"])
        self.assertEqual(self.tulis_dilakukan(), [])

    def test_laporan_harian_persen_dan_draf(self):
        K.invoice.append({"id": "91", "ref": "IN2609-0099", "socid": "1", "type": "0", "statut": "2",
                          "date": ts("2026-09-23"), "total_ht": "300000", "total_tva": "33000",
                          "total_ttc": "333000", "remaintopay": "0"})
        K.invoice.append({"id": "92", "ref": "(PROV92)", "socid": "1", "type": "0", "statut": "0",
                          "date": ts("2026-09-24"), "total_ht": "1", "total_tva": "0", "total_ttc": "1"})
        p = self.jalan("laporan-harian", "--tanggal", "2026-09-24")
        # (477.127,95 - 333.000) / 333.000 x 100 = 43,28... -> 43,3%
        self.assertIn("vs kemarin: Rp 333.000 -> naik 43,3%", p.stdout)
        self.assertIn("1 draf invoice", p.stdout)

    def test_laporan_harian_sebagian_gagal(self):
        K.mode.add("403:products")
        p = self.jalan("laporan-harian", "--tanggal", "2026-09-24")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("STOK\nTidak bisa dibaca", p.stdout)
        self.assertIn("PENJUALAN", p.stdout)

    def test_laporan_zona_salah(self):
        self.assertEqual(self.jalan("laporan-harian", "--tz", "Europe/London").returncode, 2)

    # ---------------------------------------------------------- statis
    def test_statis_tidak_ada_perintah_berbahaya(self):
        src = open(SKRIP, encoding="utf-8").read()
        self.assertNotIn('"DELETE"', src)
        self.assertNotIn('"PUT"', src)
        for kata in ("/validate", "/payments", "settopaid", "sendbyemail", "paymentsdistributed"):
            self.assertNotIn(kata, src)
        self.assertNotRegex(src, r"^\s*(import|from)\s+(requests|httpx|urllib3)", "hanya pustaka standar")

    def test_bantuan(self):
        p = self.jalan("--help")
        self.assertEqual(p.returncode, 0)
        p = self.jalan()
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
