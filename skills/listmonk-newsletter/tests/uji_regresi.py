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
        kode = lm.main(list(argv))
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
        if os.path.exists(lm.F_UJI):
            os.remove(lm.F_UJI)

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
        _, o, _ = jalankan("kirim", "7", "--tanpa-uji")
        self.assertIn("2 penerima", o)  # d confirmed + b unconfirmed (single opt-in)

    def test_penerima_nol_ditolak(self):
        STATE["subs"] = []
        self.assertEqual(jalankan("kirim", "7", "--tanpa-uji", "--ya", "--konfirmasi-penerima", "0")[0], 6)

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


if __name__ == "__main__":
    unittest.main(verbosity=1)
