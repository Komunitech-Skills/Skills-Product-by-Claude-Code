#!/usr/bin/env python3
"""Uji regresi listmonk.py memakai server listmonk TIRUAN (stdlib). Jalankan: python3 tests/uji_regresi.py
Tidak butuh listmonk sungguhan; uji nyata terhadap listmonk 6.2.0 ada di examples/uji-pembuat/."""
import contextlib
import io
import json
import os
import sys
import tempfile
import threading
import unittest
import zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import listmonk as lm  # noqa: E402

TOKEN = "RAHASIA-TOKEN-UJI-1234567890"
STATE = {}


def reset():
    STATE.clear()
    STATE.update(
        lists={1: {"id": 1, "name": "Pelanggan", "type": "private", "optin": "double", "subscriber_count": 3},
               2: {"id": 2, "name": "Umum", "type": "public", "optin": "single", "subscriber_count": 4}},
        subs=[{"id": 1, "email": "a@example.test", "name": "A", "lists": {1: "confirmed"}},
              {"id": 2, "email": "b@example.test", "name": "B", "lists": {1: "confirmed", 2: "unconfirmed"}},
              {"id": 3, "email": "c@example.test", "name": "C", "lists": {1: "unconfirmed"}},
              {"id": 4, "email": "d@example.test", "name": "D", "lists": {2: "confirmed"}}],
        camp={"id": 7, "name": "Promo", "subject": "Halo {{ .Subscriber.FirstName }}", "status": "draft",
              "body": "<p>Hai. Hubungi WhatsApp 0812. {{ UnsubscribeURL }}</p>", "content_type": "html",
              "template_id": 1, "lists": [{"id": 1}], "from_email": "T <t@example.test>", "sent": 10, "to_send": 10,
              "views": 4, "clicks": 2, "bounces": 1, "type": "regular", "messenger": "email",
              "created_at": "2026-09-01T00:00:00Z"},
        calls=[], tests=[], imports=[])


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _out(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _auth(self):
        if self.headers.get("Authorization") != f"token agen:{TOKEN}":
            self._out({"message": "invalid API credentials"}, 403)
            return False
        return True

    def _handle(self, metode):
        from urllib.parse import urlparse, parse_qs
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b""
        if not self._auth():
            return
        p = u.path
        STATE["calls"].append((metode, p, q))
        if p == "/api/lists" and metode == "GET":
            return self._out({"data": {"results": list(STATE["lists"].values()), "total": 2}})
        if p == "/api/campaigns" and metode == "GET":
            return self._out({"data": {"results": [STATE["camp"]], "total": 1}})
        if p == "/api/subscribers" and metode == "GET":
            res = STATE["subs"]
            if "list_id" in q:
                lid = int(q["list_id"])
                res = [s for s in res if lid in s["lists"] and (not q.get("subscription_status") or s["lists"][lid] == q["subscription_status"])]
            if "search" in q:
                res = [s for s in res if q["search"].lower() in s["email"]]
            return self._out({"data": {"results": res[: int(q.get("per_page", 20))], "total": len(res), "per_page": 20, "page": 1}})
        if p == "/api/subscribers" and metode == "POST":
            d = json.loads(raw)
            STATE["subs"].append({"id": 99, "email": d["email"], "name": d["name"], "lists": {}})
            return self._out({"data": {"id": 99}})
        if p.startswith("/api/subscribers/") and metode == "DELETE":
            return self._out({"data": True})
        if p == "/api/import/subscribers" and metode == "POST":
            STATE["imports"].append(raw)
            return self._out({"data": {"status": "importing"}})
        if p == "/api/import/subscribers" and metode == "GET":
            return self._out({"data": {"status": "finished", "imported": 3, "total": 3}})
        if p == "/api/campaigns/7" and metode == "GET":
            return self._out({"data": STATE["camp"]})
        if p == "/api/templates/1":
            return self._out({"data": {"body": "<html>{{ UnsubscribeURL }}</html>"}})
        if p == "/api/campaigns/7/test":
            STATE["tests"].append(json.loads(raw))
            return self._out({"data": True})
        if p == "/api/campaigns/7/status":
            STATE["camp"]["status"] = json.loads(raw)["status"]
            return self._out({"data": STATE["camp"]})
        if p == "/api/campaigns/7" and metode == "PUT":
            STATE["camp"]["send_at"] = json.loads(raw)["send_at"]
            return self._out({"data": STATE["camp"]})
        if p == "/api/campaigns/analytics/links":
            return self._out({"data": [{"url": "https://wa.me/62", "count": 2}]})
        if p.startswith("/api/subscribers/") and p.endswith("/optin"):
            return self._out({"data": True})
        return self._out({"message": "tidak ada"}, 404)

    do_GET = lambda s: s._handle("GET")
    do_POST = lambda s: s._handle("POST")
    do_PUT = lambda s: s._handle("PUT")
    do_DELETE = lambda s: s._handle("DELETE")


def jalankan(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            kode = lm.main(list(argv))
        except SystemExit as e:  # argparse: pemakaian salah -> kode 2
            kode = e.code
    return kode, out.getvalue(), err.getvalue()


def buat_xlsx(path, baris):
    def sel(ref, v):
        return f'<c r="{ref}" t="inlineStr"><is><t>{v}</t></is></c>'
    rows = ""
    for i, b in enumerate(baris, 1):
        rows += f'<row r="{i}">' + "".join(sel(f"{chr(65 + j)}{i}", v) for j, v in enumerate(b) if v != "") + "</row>"
    x = ('<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
         f"<sheetData>{rows}</sheetData></worksheet>")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/worksheets/sheet1.xml", x)


class Uji(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.srv.server_port}"
        cls.tmp = tempfile.mkdtemp()
        lm.DIR_KONFIG = cls.tmp
        lm.F_UJI = os.path.join(cls.tmp, "uji.json")
        lm.F_ALAMAT_UJI = os.path.join(cls.tmp, "alamat-uji.txt")
        lm.F_LOG_IMPOR = os.path.join(cls.tmp, "log-impor.jsonl")
        lm.F_ALAMAT = os.path.join(cls.tmp, "alamat.txt")
        lm.F_AKUN = os.path.join(cls.tmp, "akun.txt")
        lm.F_TOKEN = os.path.join(cls.tmp, "token.txt")
        os.environ["LISTMONK_URL"] = cls.url
        os.environ["LISTMONK_USER"] = "agen"
        os.environ["LISTMONK_TOKEN"] = TOKEN

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        reset()
        for f in (lm.F_UJI, lm.F_LOG_IMPOR):
            if os.path.exists(f):
                os.remove(f)
        with open(lm.F_ALAMAT_UJI, "w") as f:  # alamat uji milik pemilik (didaftarkan manusia)
            f.write("saya@example.test\ns@example.test\n")

    # ---- berkas kontak
    def _csv(self, isi):
        p = os.path.join(self.tmp, "k.csv")
        open(p, "w", encoding="utf-8").write(isi)
        return p

    def test_csv_titik_koma_bom_duplikat_typo_izin(self):
        p = self._csv("﻿Nama;Email;Kota;Setuju\nSari;sari@x.id;Bdg;ya\nAndi;ANDI@x.id;Solo;ya\nDobel;andi@x.id;Solo;ya\n"
                      "Tin;tin@gmial.com;Tgl;ya\nRudi;rudi.x.id;M;ya\nDewi;dewi@x.id;D;tidak\n;;;\n=cmd|x;evil@x.id;J;ya\n")
        h = lm.analisis_kontak(lm.baca_baris_kontak(p))
        self.assertEqual([d["email"] for d in h["ok"]], ["sari@x.id", "andi@x.id", "tin@gmial.com", "evil@x.id"])
        self.assertEqual(len(h["duplikat"]), 1)
        self.assertEqual(len(h["tidak_valid"]), 1)
        self.assertEqual(len(h["tanpa_izin"]), 1)
        self.assertEqual(len(h["mencurigakan"]), 1)
        self.assertEqual(h["kosong"], 1)
        self.assertEqual(h["ok"][3]["name"], "cmd|x")  # '=' di depan dibuang
        self.assertEqual(h["formula_dibersihkan"], 1)
        self.assertEqual(h["ok"][0]["attributes"], {"Kota": "Bdg"})

    def test_csv_tanpa_header_dan_tanpa_email(self):
        h = lm.analisis_kontak(lm.baca_baris_kontak(self._csv("a@x.id,Ani\nb@x.id,Bo\n")))
        self.assertEqual(len(h["ok"]), 2)
        with self.assertRaises(lm.Galat):
            lm.analisis_kontak(lm.baca_baris_kontak(self._csv("nama,kota\nA,B\n")))

    def test_nama_kosong_diturunkan_dari_email(self):
        h = lm.analisis_kontak(lm.baca_baris_kontak(self._csv("email,nama\nsari.dewi@x.id,\n")))
        self.assertEqual(h["ok"][0]["name"], "Sari Dewi")

    def test_xlsx(self):
        p = os.path.join(self.tmp, "k.xlsx")
        buat_xlsx(p, [["Nama", "Email"], ["Sari", "sari@x.id"], ["Bo", "bo@x.id"]])
        h = lm.analisis_kontak(lm.baca_baris_kontak(p))
        self.assertEqual(len(h["ok"]), 2)

    def test_berkas_rusak(self):
        p = os.path.join(self.tmp, "rusak.xlsx")
        open(p, "wb").write(b"bukan zip")
        with self.assertRaises(lm.Galat):
            lm.baca_baris_kontak(p)
        with self.assertRaises(lm.Galat):
            lm.baca_baris_kontak(os.path.join(self.tmp, "tidak-ada.csv"))
        self.assertEqual(jalankan("periksa-kontak", os.path.join(self.tmp, "tidak-ada.csv"))[0], 3)

    # ---- impor
    def test_impor_ditolak_tanpa_izin_atau_daftar_beli(self):
        p = self._csv("email\na@x.id\n")
        self.assertEqual(jalankan("impor", p, "--list", "1", "--ya")[0], 6)
        k, _, e = jalankan("impor", p, "--list", "1", "--sumber-persetujuan", "hasil beli database", "--saya-punya-izin", "--ya")
        self.assertEqual(k, 6)
        self.assertEqual(STATE["imports"], [])
        k, _, _ = jalankan("impor", p, "--list", "1", "--sumber-persetujuan", "hasil scraping IG", "--saya-punya-izin", "--ya")
        self.assertEqual(k, 6)

    def test_impor_butuh_ya_lalu_unconfirmed(self):
        p = self._csv("email,nama\na@x.id,Ani\n")
        args = ["impor", p, "--list", "1", "--sumber-persetujuan", "formulir toko", "--saya-punya-izin"]
        self.assertEqual(jalankan(*args)[0], 6)
        self.assertEqual(STATE["imports"], [])
        k, o, _ = jalankan(*args, "--ya")
        self.assertEqual(k, 0)
        self.assertIn(b'"unconfirmed"', STATE["imports"][0])
        self.assertIn("kirim-optin", o)

    def test_kirim_optin_gerbang(self):
        self.assertEqual(jalankan("kirim-optin", "--list", "1")[0], 6)
        self.assertEqual(jalankan("kirim-optin", "--list", "1", "--ya", "--konfirmasi-penerima", "5")[0], 6)
        self.assertEqual(jalankan("kirim-optin", "--list", "1", "--ya", "--konfirmasi-penerima", "1")[0], 0)
        self.assertEqual(jalankan("kirim-optin", "--list", "2")[0], 2)  # single opt-in

    # ---- kampanye
    def test_kirim_gerbang_bertahap(self):
        k, o, _ = jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")
        self.assertEqual(k, 6)  # belum uji-kirim
        self.assertNotEqual(STATE["camp"]["status"], "running")
        self.assertEqual(jalankan("uji-kirim", "7", "--ke", "Saya@Example.test")[0], 0)
        self.assertEqual(STATE["tests"][0]["subscribers"], ["saya@example.test"])
        k, o, _ = jalankan("kirim", "7")
        self.assertEqual(k, 6)
        self.assertIn("2 penerima", o)  # double opt-in: hanya yang confirmed (a, b)
        self.assertEqual(STATE["camp"]["status"], "draft")
        self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "3")[0], 6)
        self.assertEqual(STATE["camp"]["status"], "draft")
        self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")[0], 0)
        self.assertEqual(STATE["camp"]["status"], "running")

    def test_isi_berubah_setelah_uji_wajib_uji_ulang(self):
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        STATE["camp"]["body"] += " <p>diubah</p>"
        self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")[0], 6)

    def test_tanpa_tautan_berhenti_ditolak(self):
        STATE["camp"]["body"] = "<p>Hai</p>"
        STATE["camp"]["template_id"] = 99  # template tak ada -> tidak ada UnsubscribeURL
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        k, o, _ = jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")
        self.assertEqual(k, 6)
        self.assertIn("berhenti berlangganan", o)

    def test_daftar_gabungan_single_optin_hitung_semua(self):
        STATE["camp"]["lists"] = [{"id": 2}]
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        _, o, _ = jalankan("kirim", "7")
        self.assertIn("2 penerima", o)  # d confirmed + b unconfirmed (single opt-in)

    def test_penerima_nol_ditolak(self):
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        STATE["subs"] = []
        self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "0")[0], 6)

    def test_jadwal(self):
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        self.assertEqual(jalankan("jadwal", "7", "--waktu", "2020-01-01 09:00", "--ya", "--konfirmasi-penerima", "2")[0], 2)
        self.assertEqual(jalankan("jadwal", "7", "--waktu", "salah")[0], 2)
        k, _, _ = jalankan("jadwal", "7", "--waktu", "2099-01-01 09:00", "--tz", "WITA", "--ya", "--konfirmasi-penerima", "2")
        self.assertEqual(k, 0)
        self.assertEqual(STATE["camp"]["send_at"], "2099-01-01T09:00:00+08:00")
        self.assertEqual(STATE["camp"]["status"], "scheduled")

    def test_batalkan_jadwal_kembali_ke_draf(self):
        STATE["camp"]["status"] = "scheduled"
        self.assertEqual(jalankan("batalkan", "7")[0], 6)
        self.assertEqual(jalankan("batalkan", "7", "--ya")[0], 0)
        self.assertEqual(STATE["camp"]["status"], "draft")

    def test_statistik(self):
        k, o, _ = jalankan("statistik", "7", "--tautan")
        self.assertEqual(k, 0)
        self.assertIn("40,0%", o)   # 4/10 dibuka
        self.assertIn("20,0%", o)   # 2/10 klik
        self.assertIn("https://wa.me/62", o)

    def test_hapus_pelanggan(self):
        self.assertEqual(jalankan("hapus-pelanggan", "--email", "a@example.test")[0], 6)
        self.assertEqual(jalankan("hapus-pelanggan", "--email", "a@example.test", "--ya")[0], 0)
        self.assertEqual(jalankan("hapus-pelanggan", "--email", "tidak@ada.id")[0], 7)

    # ---- keamanan
    def test_token_tidak_pernah_tercetak(self):
        semua = ""
        for a in (["cek"], ["daftar-list"], ["statistik", "7"], ["kirim", "7"], ["daftar-pelanggan", "--list", "1", "--contoh", "3"]):
            _, o, e = jalankan(*a)
            semua += o + e
        self.assertNotIn(TOKEN, semua)
        os.environ["LISTMONK_TOKEN"] = "salah"
        try:
            k, o, e = jalankan("daftar-list")
            self.assertEqual(k, 5)
            self.assertNotIn("salah", o + e.replace("salah ", ""))
        finally:
            os.environ["LISTMONK_TOKEN"] = TOKEN

    def test_alamat_internet_wajib_https_dan_izin(self):
        self.assertEqual(jalankan("cek", "--url", "http://contoh.com")[0], 2)
        self.assertEqual(jalankan("cek", "--url", "https://contoh.com")[0], 2)

    def test_server_mati_dan_tanpa_akun(self):
        self.assertEqual(jalankan("cek", "--url", "http://127.0.0.1:1")[0], 4)
        u, t = os.environ.pop("LISTMONK_USER"), os.environ.pop("LISTMONK_TOKEN")
        try:
            self.assertEqual(jalankan("cek")[0], 3)
        finally:
            os.environ["LISTMONK_USER"], os.environ["LISTMONK_TOKEN"] = u, t

    def test_redirect_tidak_diikuti(self):
        class R(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                self.send_response(302)
                self.send_header("Location", "http://127.0.0.1:1/x")
                self.end_headers()
        s = HTTPServer(("127.0.0.1", 0), R)
        threading.Thread(target=s.serve_forever, daemon=True).start()
        try:
            self.assertEqual(jalankan("cek", "--url", f"http://127.0.0.1:{s.server_port}")[0], 4)
        finally:
            s.shutdown()

    def test_lint_subjek_spam(self):
        STATE["camp"]["subject"] = "PROMO GILA GILAAN HARI INI SAJA!!!"
        _, o, _ = jalankan("periksa-kampanye", "7")
        self.assertIn("HURUF BESAR", o)
        self.assertIn("tanda seru", o)

    def test_parse_waktu(self):
        self.assertEqual(lm.parse_waktu("2026-10-05 09:00", "WIB").isoformat(), "2026-10-05T09:00:00+07:00")
        self.assertEqual(lm.parse_waktu("2026-10-05 9:30", "WIT").isoformat(), "2026-10-05T09:30:00+09:00")

    # ================= REGRESI 1.0.1 =================
    # -- P1.1 gerbang uji-kirim
    def test_tanpa_uji_tidak_ada_lagi(self):
        for cmd in ("kirim", "jadwal"):
            extra = ["--waktu", "2099-01-01 09:00"] if cmd == "jadwal" else []
            k, _, e = jalankan(cmd, "7", *extra, "--tanpa-uji", "--ya", "--konfirmasi-penerima", "2")
            self.assertEqual(k, 2)  # argumen tak dikenal
        self.assertNotEqual(STATE["camp"]["status"], "running")

    def test_singkatan_opsi_ditolak(self):
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        k, _, e = jalankan("kirim", "7", "--y", "--konfirmasi-penerima", "2")
        self.assertEqual(k, 2)
        self.assertNotEqual(STATE["camp"]["status"], "running")
        k, _, _ = jalankan("kirim", "7", "--ya", "--konfirmasi-p", "2")
        self.assertEqual(k, 2)
        k, _, _ = jalankan("impor", "x.csv", "--li", "1")
        self.assertEqual(k, 2)
        self.assertEqual(STATE["camp"]["status"], "draft")

    def test_gerbang_uji_semua_jalur_tanpa_uji(self):
        self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")[0], 6)
        self.assertEqual(jalankan("jadwal", "7", "--waktu", "2099-01-01 09:00", "--ya", "--konfirmasi-penerima", "2")[0], 6)
        self.assertEqual(STATE["camp"]["status"], "draft")

    def test_catatan_uji_kunci_id_dan_sidik_isi(self):
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        d = lm.muat_uji()
        (kunci, nilai), = d.items()
        self.assertTrue(kunci.endswith("#7"))
        self.assertEqual(len(nilai["sidik"]), 16)
        self.assertNotIn("s@example.test", json.dumps(d))  # alamat disamarkan
        for ubah in ("subject", "body", "from_email"):
            with self.subTest(ubah=ubah):
                asli = STATE["camp"][ubah]
                STATE["camp"][ubah] = asli + " x"
                self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")[0], 6)
                STATE["camp"][ubah] = asli
        self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")[0], 0)

    def test_uji_di_kampanye_lain_tidak_berlaku(self):
        jalankan("uji-kirim", "7", "--ke", "s@example.test")
        d = lm.muat_uji()
        kunci = list(d)[0]
        d[kunci.replace("#7", "#8")] = d.pop(kunci)
        with open(lm.F_UJI, "w") as f:
            json.dump(d, f)
        self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")[0], 6)

    # -- P1.2 penerima uji-kirim
    def test_uji_kirim_hanya_alamat_terdaftar(self):
        k, _, e = jalankan("uji-kirim", "7", "--ke", "korban@orang.test")
        self.assertEqual(k, 6)
        self.assertEqual(STATE["tests"], [])
        self.assertFalse(any(m == "POST" and p == "/api/subscribers" for m, p, _ in STATE["calls"]))  # tak buat pelanggan asing
        self.assertEqual(lm.muat_uji(), {})

    def test_uji_kirim_tanpa_daftar_alamat_ditolak(self):
        os.remove(lm.F_ALAMAT_UJI)
        self.assertEqual(jalankan("uji-kirim", "7", "--ke", "saya@example.test")[0], 6)
        self.assertEqual(STATE["tests"], [])

    def test_uji_kirim_alamat_tunggal_default_dan_maks_tiga(self):
        open(lm.F_ALAMAT_UJI, "w").write("a1@example.test\na2@example.test\na3@example.test\na4@example.test\n")
        self.assertEqual(len(lm.muat_alamat_uji()), 3)
        self.assertEqual(jalankan("uji-kirim", "7")[0], 2)  # banyak alamat: harus sebut satu
        self.assertEqual(jalankan("uji-kirim", "7", "--ke", "a4@example.test")[0], 6)  # di luar 3 pertama
        open(lm.F_ALAMAT_UJI, "w").write("satu@example.test\n")
        self.assertEqual(jalankan("uji-kirim", "7")[0], 0)
        self.assertEqual(STATE["tests"][0]["subscribers"], ["satu@example.test"])

    def test_simpan_alamat_uji_butuh_terminal(self):
        # stdin uji bukan terminal -> agent tidak bisa menambah alamat
        self.assertEqual(jalankan("simpan-alamat-uji", "--email", "x@orang.test")[0], 3)
        self.assertNotIn("x@orang.test", open(lm.F_ALAMAT_UJI).read())

    # -- P1.3 tautan berhenti
    def test_tautan_berhenti_dalam_komentar_tidak_dihitung(self):
        for body in ("<p>Hai WA 0812</p><!-- {{ UnsubscribeURL }} -->",
                     "<p>Hai</p><!--\n<a href=\"{{ UnsubscribeURL }}\">berhenti</a>\n-->",
                     "<p>Hai</p>{{/* {{ UnsubscribeURL }} */}}",
                     "<p>UnsubscribeURL</p>"):
            with self.subTest(body=body):
                STATE["camp"]["body"] = body
                STATE["camp"]["template_id"] = 99
                self.assertEqual(jalankan("uji-kirim", "7", "--ke", "s@example.test")[0], 6)
                self.assertEqual(STATE["tests"], [])
                self.assertEqual(jalankan("kirim", "7", "--ya", "--konfirmasi-penerima", "2")[0], 6)
                self.assertEqual(jalankan("periksa-kampanye", "7")[0], 6)

    def test_tautan_berhenti_valid_di_isi_atau_template(self):
        self.assertTrue(lm.punya_tautan_berhenti('<a href="{{ UnsubscribeURL }}">x</a>'))
        self.assertTrue(lm.punya_tautan_berhenti("<!-- catatan --><a href=\"{{UnsubscribeURL}}\">x</a>"))
        self.assertFalse(lm.punya_tautan_berhenti(""))
        # template bawaan (mock) memuat tag di luar komentar, isi tidak
        STATE["camp"]["body"] = "<p>Hai WA 0812</p>"
        self.assertEqual(jalankan("uji-kirim", "7", "--ke", "s@example.test")[0], 0)

    def test_komentar_di_template_tidak_dihitung(self):
        self.assertFalse(lm.punya_tautan_berhenti("<html><!-- {{ UnsubscribeURL }} --></html>"))

    # -- P1.4 sumber persetujuan
    def _impor(self, sumber, *extra, isi="email\na@x.id\n"):
        return jalankan("impor", self._csv(isi), "--list", "1", "--sumber-persetujuan", sumber, "--saya-punya-izin",
                        "--ya", *extra)

    def test_sumber_terlarang_ditolak_semua_variasi(self):
        buruk = ["grup WA komunitas", "Grup Whatsapp alumni", "dari vendor", "Vendor data", "hasil beli", "dibeli dari toko data",
                 "database orang", "database pelanggan", "hasil scrape IG", "Scraping marketplace", "dapat dari teman",
                 "dikasih teman", "Dapet dari teman kantor", "b3li database", "s c r a p e", "beli", "B E L I putus",
                 "Tokopedia buyer list", "followers Instagram", "sewa list", "data bocor", "lupa dari mana", "tidak tahu",
                 "formulir website tapi juga hasil beli", "WA group"]
        for sb in buruk:
            with self.subTest(sumber=sb):
                STATE["imports"].clear()
                k, _, _ = self._impor(sb)
                self.assertEqual(k, 6, sb)
                self.assertEqual(STATE["imports"], [])

    def test_sumber_terlarang_tidak_bisa_dielak_konfirmasi(self):
        k, _, _ = self._impor("grup WA", "--pengguna-konfirmasi-setuju", "semua orang sudah setuju kok")
        self.assertEqual(k, 6)
        k, _, _ = self._impor("apa saja", "--pengguna-konfirmasi-setuju", "dapat dari teman saya")
        self.assertEqual(k, 6)
        self.assertEqual(STATE["imports"], [])

    def test_sumber_sah_diterima(self):
        for sb in ("Formulir pendaftaran di website toko", "Kotak opt-in tidak tercentang saat checkout",
                   "persetujuan tertulis (tanda tangan) di kasir", "Rekaman persetujuan lisan pelanggan"):
            with self.subTest(sumber=sb):
                STATE["imports"].clear()
                self.assertEqual(self._impor(sb)[0], 0, sb)
                self.assertEqual(len(STATE["imports"]), 1)

    def test_checkout_tanpa_opt_in_bukan_persetujuan(self):
        self.assertEqual(lm.klasifikasi_sumber("pembeli checkout"), "tak_dikenal")
        self.assertEqual(lm.klasifikasi_sumber("pembeli toko saya"), "tak_dikenal")

    def test_sumber_tak_dikenal_wajib_konfirmasi_dan_dicatat(self):
        k, _, e = self._impor("pelanggan lama toko")
        self.assertEqual(k, 6)
        self.assertEqual(STATE["imports"], [])
        k, _, _ = self._impor("pelanggan lama toko", "--pengguna-konfirmasi-setuju", "ya")  # terlalu pendek
        self.assertEqual(k, 6)
        k, _, _ = self._impor("pelanggan lama toko", "--pengguna-konfirmasi-setuju",
                              "Ya, mereka isi buku tamu dan tulis setuju dikirimi email")
        self.assertEqual(k, 0)
        self.assertEqual(len(STATE["imports"]), 1)
        log = [json.loads(x) for x in open(lm.F_LOG_IMPOR, encoding="utf-8")]
        diimpor = [x for x in log if x["hasil"] == "diimpor"]
        self.assertEqual(len(diimpor), 1)
        self.assertIn("buku tamu", diimpor[0]["konfirmasi_pengguna"])
        self.assertEqual(diimpor[0]["klasifikasi"], "tak_dikenal")
        self.assertNotIn("a@x.id", open(lm.F_LOG_IMPOR, encoding="utf-8").read())  # log tanpa kontak

    def test_penolakan_juga_dicatat(self):
        self._impor("hasil beli")
        log = [json.loads(x) for x in open(lm.F_LOG_IMPOR, encoding="utf-8")]
        self.assertEqual(log[-1]["hasil"], "ditolak-sumber-terlarang")

    def test_sudah_terkonfirmasi_butuh_sumber_sah(self):
        k, _, _ = self._impor("pelanggan lama toko", "--pengguna-konfirmasi-setuju", "Ya, mereka setuju tertulis di buku",
                              "--sudah-terkonfirmasi")
        self.assertEqual(k, 6)
        k, _, _ = self._impor("Formulir website toko", "--sudah-terkonfirmasi")
        self.assertEqual(k, 0)
        self.assertIn(b'"confirmed"', STATE["imports"][0])

    def test_nama_berkas_terlarang_ditolak(self):
        p = os.path.join(self.tmp, "hasil-beli-database.csv")
        open(p, "w").write("email\na@x.id\n")
        k, _, _ = jalankan("impor", p, "--list", "1", "--sumber-persetujuan", "Formulir website", "--saya-punya-izin", "--ya")
        self.assertEqual(k, 6)

    def test_kolom_sumber_terlarang_di_berkas(self):
        p = self._csv("email,sumber\na@x.id,formulir web\nb@x.id,grup WA alumni\n")
        k, o, _ = jalankan("impor", p, "--list", "1", "--sumber-persetujuan", "Formulir website", "--saya-punya-izin", "--ya")
        self.assertEqual(k, 6)
        self.assertEqual(STATE["imports"], [])

    # -- P2
    def test_kolom_setuju_kosong_dianggap_tidak_setuju(self):
        h = lm.analisis_kontak(lm.baca_baris_kontak(self._csv(
            "email,setuju\na@x.id,ya\nb@x.id,\nc@x.id,mungkin\nd@x.id,Ya\ne@x.id,tidak\n")))
        self.assertEqual([d["email"] for d in h["ok"]], ["a@x.id", "d@x.id"])
        self.assertEqual(len(h["tanpa_izin"]), 3)
        self.assertEqual(h["izin_kosong"], 1)

    def test_tanpa_kolom_setuju_tetap_masuk(self):
        h = lm.analisis_kontak(lm.baca_baris_kontak(self._csv("email\na@x.id\n")))
        self.assertEqual(len(h["ok"]), 1)

    def test_bersihkan_awalan_rumus_nama_dan_atribut(self):
        h = lm.analisis_kontak(lm.baca_baris_kontak(self._csv(
            'email,nama,kota\na@x.id,"=+@-HYPERLINK(x)","@SUM(1)"\nb@x.id,Bo,Solo\n')))
        self.assertEqual(h["ok"][0]["name"], "HYPERLINK(x)")
        self.assertEqual(h["ok"][0]["attributes"]["kota"], "SUM(1)")
        self.assertEqual(h["formula_dibersihkan"], 2)
        self.assertEqual(h["ok"][1]["name"], "Bo")

    def test_impor_beri_catatan_berhenti_diblokir(self):
        _, o, _ = self._impor("Formulir website")
        self.assertIn("TIDAK dihidupkan lagi", o)

    def test_xlsx_xml_rusak_pesan_ramah(self):
        p = os.path.join(self.tmp, "rusak2.xlsx")
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("xl/worksheets/sheet1.xml", "<worksheet><sheetData><row>")
        with self.assertRaises(lm.Galat):
            lm.baca_baris_kontak(p)
        self.assertEqual(jalankan("periksa-kontak", p)[0], 3)
        p2 = os.path.join(self.tmp, "rusak3.xlsx")
        with zipfile.ZipFile(p2, "w") as z:
            z.writestr("xl/worksheets/sheet1.xml", "<worksheet/>")
            z.writestr("xl/sharedStrings.xml", "<sst><si>")
        self.assertEqual(jalankan("periksa-kontak", p2)[0], 3)

    def test_404_tanpa_pesan_dikira_bukan_listmonk(self):
        class N(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
        s = HTTPServer(("127.0.0.1", 0), N)
        threading.Thread(target=s.serve_forever, daemon=True).start()
        try:
            k, _, e = jalankan("cek", "--url", f"http://127.0.0.1:{s.server_port}")
            self.assertEqual(k, 7)
            self.assertIn("BUKAN server listmonk", e)
        finally:
            s.shutdown()

    def test_tidak_ada_traceback_mentah(self):
        orig = lm.cmd_cek
        try:
            def rusak(a):
                raise RuntimeError("boom " + TOKEN)
            lm.cmd_cek = rusak
            p = lm.buat_parser()
            k, _, e = 0, "", ""
            import unittest.mock as um
            with um.patch.object(lm, "buat_parser", lambda: um.Mock(parse_args=lambda argv: um.Mock(f=rusak))):
                k, o, e = jalankan("cek")
            self.assertEqual(k, 1)
            self.assertNotIn("Traceback", e)
            self.assertNotIn(TOKEN, e)
        finally:
            lm.cmd_cek = orig

    def test_token_tidak_tercetak_di_alur_baru(self):
        semua = ""
        for a in (["uji-kirim", "7", "--ke", "s@example.test"], ["kirim", "7"], ["uji-kirim", "7", "--ke", "asing@x.test"]):
            _, o, e = jalankan(*a)
            semua += o + e
        _, o, e = self._impor("hasil beli")
        semua += o + e + open(lm.F_LOG_IMPOR, encoding="utf-8").read()
        self.assertNotIn(TOKEN, semua)

    def test_versi(self):
        self.assertEqual(lm.VERSI, "1.0.1")


if __name__ == "__main__":
    unittest.main(verbosity=1)
