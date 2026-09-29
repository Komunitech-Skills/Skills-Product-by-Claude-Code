#!/usr/bin/env python3
"""Uji regresi fider.py dengan server Fider TIRUAN (perilaku dicocokkan dengan Fider v0.38.0 asli).

Jalankan:  python3 tests/uji_regresi.py   (Windows: python / py). Tanpa paket tambahan.
"""
import contextlib
import http.server
import io
import json
import os
import re
import sys
import tempfile
import threading
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import fider  # noqa: E402

KUNCI = "KUNCI-RAHASIA-UJI-1234567890"


class Tiruan(http.server.BaseHTTPRequestHandler):
    data = None
    log = None

    def log_message(self, *a):
        pass

    def _kirim(self, kode, obj, extra=None):
        b = json.dumps(obj).encode()
        self.send_response(kode)
        self.send_header("Content-Type", "application/json")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _tangani(self, m):
        D = self.data
        self.log.append((m, self.path))
        if self.headers.get("Authorization") != "Bearer " + KUNCI:
            return self._kirim(400, {"errors": [{"message": "API Key is invalid"}]})
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n)) if n else {}
        p = self.path.split("?")[0]
        if p == "/redirect":
            return self._kirim(302, {}, {"Location": "http://evil.example/"})
        if p == "/api/v1/tags" and m == "GET":
            return self._kirim(200, D["tags"])
        if p == "/api/v1/users":
            return self._kirim(403, {}) if D.get("collab") else self._kirim(200, {"users": []})
        if p == "/api/v1/posts" and m == "GET":
            return self._kirim(200, [x for x in D["posts"] if x["status"] != "duplicate"])
        if p == "/api/v1/posts" and m == "POST":
            if not body.get("title") or len(body["title"]) > 100:
                return self._kirim(400, {"errors": [{"field": "title", "message": "Title invalid"}]})
            no = len(D["posts"]) + 1
            D["posts"].append({"id": no, "number": no, "title": body["title"], "description": body.get("description", ""),
                               "createdAt": "2026-09-29T08:00:00Z", "votesCount": 1, "commentsCount": 0,
                               "status": "open", "tags": []})
            return self._kirim(200, {"id": no, "number": no})
        mm = re.match(r"^/api/v1/posts/(\d+)(/.*)?$", p)
        if mm:
            no, sisa = int(mm.group(1)), mm.group(2) or ""
            ps = [x for x in D["posts"] if x["number"] == no]
            if not ps:
                return self._kirim(404, {})
            ps = ps[0]
            if sisa == "" and m == "GET":
                return self._kirim(200, ps)
            if sisa == "/comments" and m == "GET":
                return self._kirim(200, [])
            if sisa == "/comments" and m == "POST":
                ps["commentsCount"] += 1
                D["komentar"].append(body["content"])
                return self._kirim(200, {"id": 1})
            if sisa == "/votes" and m == "GET":
                return self._kirim(403, {}) if D.get("collab") else self._kirim(
                    200, [{"createdAt": "2026-09-28T08:00:00Z"}] * ps["votesCount"])
            if sisa == "/votes" and m == "DELETE":
                ps["votesCount"] -= 1
                return self._kirim(200, {})
            if sisa == "/status" and m == "PUT":
                st = body.get("status")
                if st == "duplicate":
                    ps["status"] = "duplicate"
                    for x in D["posts"]:
                        if x["number"] == body["originalNumber"]:
                            x["votesCount"] += ps["votesCount"]
                else:  # Fider asli: status asing -> open, tetap 200
                    ps["status"] = st if st in fider.STATUS_SAH else "open"
                    ps["response"] = {"text": body.get("text", ""), "respondedAt": "2026-09-29T08:00:00Z"}
                return self._kirim(200, {})
            mt = re.match(r"^/tags/([a-z0-9-]+)$", sisa)
            if mt:
                if m == "POST":
                    ps["tags"].append(mt.group(1))
                else:
                    ps["tags"].remove(mt.group(1))
                return self._kirim(200, {})
        return self._kirim(404, {})

    def do_GET(self): self._tangani("GET")
    def do_POST(self): self._tangani("POST")
    def do_PUT(self): self._tangani("PUT")
    def do_DELETE(self): self._tangani("DELETE")


def pos(no, judul, suara=1, status="open", tags=None):
    return {"id": no, "number": no, "title": judul, "description": "", "createdAt": "2026-09-01T08:00:00Z",
            "votesCount": suara, "commentsCount": 0, "status": status, "tags": tags or []}


class Dasar(unittest.TestCase):
    def setUp(self):
        Tiruan.data = {"posts": [pos(1, "Tambah pembayaran QRIS", 5), pos(2, "Notifikasi WhatsApp pesanan", 3),
                                 pos(3, "Laporan bulanan PDF", 9, "planned")],
                       "tags": [{"id": 1, "name": "Pembayaran", "slug": "pembayaran", "color": "3B82F6", "isPublic": True}],
                       "komentar": []}
        Tiruan.log = []
        self.srv = http.server.HTTPServer(("127.0.0.1", 0), Tiruan)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"
        self.tmp = tempfile.mkdtemp()
        self.kf = os.path.join(self.tmp, "kunci.txt")
        with open(self.kf, "w") as f:
            f.write(KUNCI + "\n")
        os.chmod(self.kf, 0o600)

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()

    def jalan(self, *argv, kunci_file=None):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = fider.main(list(argv) + ["--url", self.url, "--kunci-file", kunci_file or self.kf])
        return rc, out.getvalue(), err.getvalue()

    def tulis(self, isi, nama="catatan.txt"):
        p = os.path.join(self.tmp, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write(isi)
        return p

    def penulisan(self):
        return [x for x in Tiruan.log if x[0] != "GET"]


class UjiBaca(Dasar):
    def test_cek_dan_kunci_tidak_bocor(self):
        rc, out, err = self.jalan("cek")
        self.assertEqual(rc, 0)
        self.assertIn("valid (tidak ditampilkan)", out)
        self.assertNotIn(KUNCI, out + err)

    def test_kunci_salah(self):
        salah = os.path.join(self.tmp, "salah.txt")
        with open(salah, "w") as f:
            f.write("kunci-lain\n")
        os.chmod(salah, 0o600)
        rc, out, err = self.jalan("cek", kunci_file=salah)
        self.assertEqual(rc, fider.K_KUNCI)
        self.assertIn("ditolak", err)
        self.assertNotIn("kunci-lain", err)

    def test_server_mati(self):
        self.srv.shutdown()
        rc, _, err = self.jalan("cek")
        self.assertEqual(rc, fider.K_JARINGAN)
        self.assertIn("GALAT", err)

    def test_daftar_urut_suara_dan_filter_status(self):
        rc, out, _ = self.jalan("daftar")
        self.assertEqual(out.splitlines()[0][:3], "#3 ")
        rc, out, _ = self.jalan("daftar", "--status", "rencana")
        self.assertEqual(len(out.strip().splitlines()), 1)
        rc, _, err = self.jalan("daftar", "--status", "ngawur")
        self.assertEqual(rc, fider.K_INPUT)

    def test_lihat_nomor_tidak_ada_dan_salah_format(self):
        self.assertEqual(self.jalan("lihat", "999")[0], fider.K_INPUT)
        self.assertEqual(self.jalan("lihat", "abc")[0], fider.K_INPUT)
        self.assertEqual(self.jalan("lihat", "../etc")[0], fider.K_INPUT)

    def test_ringkasan_mingguan_hitungan(self):
        Tiruan.data["posts"][0]["createdAt"] = "2999-01-01T00:00:00Z"  # "baru" (masa depan tetap >= awal)
        rc, out, _ = self.jalan("ringkasan-mingguan", "--top", "2")
        self.assertEqual(rc, 0)
        self.assertIn("3 pos aktif".replace("3 pos aktif", "Pos aktif"), out)
        self.assertIn("total 17 suara", out)
        self.assertIn("1. #3 Laporan bulanan PDF - 9 suara", out)
        self.assertIn("2. #1 Tambah pembayaran QRIS - 5 suara", out)
        rc, out, _ = self.jalan("ringkasan-mingguan", "--json")
        d = json.loads(out)
        self.assertEqual(d["total_suara"], 17)
        self.assertEqual(d["top"][0]["suara_baru"], 9)

    def test_ringkasan_tanpa_izin_suara(self):
        Tiruan.data["collab"] = True
        rc, out, _ = self.jalan("ringkasan-mingguan")
        self.assertEqual(rc, 0)
        self.assertIn("butuh peran Collaborator", out)

    def test_draf_balasan(self):
        rc, out, _ = self.jalan("draf-balasan", "1")
        self.assertIn("PERINGATAN", out)
        self.assertEqual(self.penulisan(), [])
        Tiruan.data["posts"][0]["status"] = "completed"
        rc, out, _ = self.jalan("draf-balasan", "1", "--gaya", "santai", "--catatan", "Sekarang ada di menu Bayar.")
        self.assertNotIn("PERINGATAN", out)
        self.assertIn("Halo Kak", out)
        self.assertIn("didukung 5 orang", out)
        self.assertEqual(self.penulisan(), [])


class UjiTulis(Dasar):
    def test_impor_pratinjau_tidak_menulis(self):
        p = self.tulis("- Bisa bayar pakai OVO\n- Tambah warna hitam\n")
        rc, out, _ = self.jalan("impor", p)
        self.assertEqual(rc, 0)
        self.assertIn("PRATINJAU", out)
        self.assertEqual(self.penulisan(), [])
        self.assertEqual(len(Tiruan.data["posts"]), 3)

    def test_impor_menulis_dengan_ya_dan_menyamarkan_pribadi(self):
        p = self.tulis("Ibu Rina (0812-3456-7890) minta cetak resi\n\nHubungi budi@contoh.id soal ongkir\n")
        rc, out, _ = self.jalan("impor", p, "--ya", "--sumber", "WhatsApp", "--hapus-suara-saya")
        self.assertEqual(rc, 0, out)
        semua = json.dumps(Tiruan.data["posts"], ensure_ascii=False)
        self.assertNotIn("0812", semua)
        self.assertNotIn("budi@", semua)
        self.assertIn("[nomor disembunyikan]", semua)
        self.assertEqual(Tiruan.data["posts"][3]["votesCount"], 0)
        self.assertEqual(len(Tiruan.data["posts"]), 5)

    def test_impor_lewati_duplikat(self):
        p = self.tulis("Tolong tambah pembayaran QRIS\n\nBisa bayar pakai OVO\n")
        rc, out, _ = self.jalan("impor", p, "--ya")
        self.assertIn("1 pos dibuat, 1 dilewati", out)
        rc, out, _ = self.jalan("impor", self.tulis("Tolong tambah pembayaran QRIS\n", "b.txt"), "--ya", "--tetap")
        self.assertIn("1 pos dibuat, 0 dilewati", out)

    def test_impor_judul_panjang_dan_json(self):
        panjang = "kata " * 60
        self.jalan("impor", self.tulis(panjang), "--ya")
        baru = Tiruan.data["posts"][-1]
        self.assertLessEqual(len(baru["title"]), 100)
        self.assertIn("kata", baru["description"])
        js = self.tulis(json.dumps([{"judul": "Diskon member", "uraian": "x", "tag": ["pembayaran"], "pelanggan": 4}]), "a.json")
        rc, out, _ = self.jalan("impor", js, "--ya")
        self.assertEqual(rc, 0, out)
        self.assertEqual(Tiruan.data["posts"][-1]["tags"], ["pembayaran"])
        self.assertIn("4 pelanggan", Tiruan.data["posts"][-1]["description"])

    def test_impor_input_buruk(self):
        self.assertEqual(self.jalan("impor", os.path.join(self.tmp, "tidak-ada.txt"))[0], fider.K_FILE)
        self.assertEqual(self.jalan("impor", self.tulis("   \n\n"))[0], fider.K_FILE)
        self.assertEqual(self.jalan("impor", self.tulis("{rusak", "x.json"))[0], fider.K_FILE)
        self.assertEqual(self.jalan("impor", self.tulis("[{\"uraian\":\"tanpa judul\"}]", "y.json"))[0], fider.K_FILE)
        biner = os.path.join(self.tmp, "b.txt")
        with open(biner, "wb") as f:
            f.write(b"\xff\xfe\x00\x81")
        self.assertEqual(self.jalan("impor", biner)[0], fider.K_FILE)
        banyak = self.tulis("\n\n".join(f"butir unik nomor {i} xq{i}" for i in range(60)), "banyak.txt")
        self.assertEqual(self.jalan("impor", banyak)[0], fider.K_INPUT)

    def test_status_pratinjau_lalu_tulis(self):
        rc, out, _ = self.jalan("status", "1", "dikerjakan")
        self.assertIn("PRATINJAU", out)
        self.assertEqual(Tiruan.data["posts"][0]["status"], "open")
        rc, out, _ = self.jalan("status", "1", "dikerjakan", "--catatan", "Mulai minggu ini", "--ya")
        self.assertEqual(Tiruan.data["posts"][0]["status"], "started")

    def test_status_asing_ditolak_lokal(self):
        rc, _, err = self.jalan("status", "1", "bogus", "--ya")
        self.assertEqual(rc, fider.K_INPUT)
        self.assertEqual(self.penulisan(), [])

    def test_gabung_dan_idempoten(self):
        rc, out, _ = self.jalan("gabung", "2", "1")
        self.assertIn("PRATINJAU", out)
        self.assertEqual(Tiruan.data["posts"][1]["status"], "open")
        self.jalan("gabung", "2", "1", "--ya")
        self.assertEqual(Tiruan.data["posts"][0]["votesCount"], 8)
        n = len(self.penulisan())
        rc, out, _ = self.jalan("gabung", "2", "1", "--ya")
        self.assertIn("sudah berstatus duplikat", out)
        self.assertEqual(len(self.penulisan()), n)
        self.assertEqual(self.jalan("gabung", "1", "1")[0], fider.K_INPUT)
        self.assertEqual(self.jalan("gabung", "3", "2")[0], fider.K_INPUT)  # induk sudah duplikat

    def test_tag_pasang_lepas_dan_tag_hilang(self):
        rc, out, _ = self.jalan("tag", "1", "pembayaran", "--ya")
        self.assertEqual(Tiruan.data["posts"][0]["tags"], ["pembayaran"])
        self.jalan("tag", "1", "pembayaran", "--lepas", "--ya")
        self.assertEqual(Tiruan.data["posts"][0]["tags"], [])
        rc, _, err = self.jalan("tag", "1", "tidak-ada", "--ya")
        self.assertEqual(rc, fider.K_INPUT)
        self.assertIn("tag-buat", err)

    def test_komentar_menyamarkan_nomor(self):
        self.jalan("komentar", "1", "--teks", "Sudah beres, telp 081234567890", "--ya")
        self.assertEqual(Tiruan.data["komentar"], ["Sudah beres, telp [nomor disembunyikan]"])
        self.assertEqual(self.jalan("komentar", "1", "--teks", "  ", "--ya")[0], fider.K_INPUT)

    def test_redirect_ditolak(self):
        k = fider.Klien(self.url, KUNCI)
        with self.assertRaises(fider.Gagal) as c:
            k.minta("GET", "/redirect")
        self.assertEqual(c.exception.kode, fider.K_JARINGAN)


class UjiUnit(unittest.TestCase):
    def test_samarkan_pribadi(self):
        t, n = fider.samarkan_pribadi("hub +62 812-3456-7890 / 08123456789 / a.b@x.co.id")
        self.assertEqual(n, 3)
        self.assertNotRegex(t, r"\d{6}")
        self.assertEqual(fider.samarkan_pribadi("harga Rp15.000 dan 3 pcs")[1], 0)

    def test_kemiripan(self):
        self.assertGreater(fider.kemiripan("Bayar pakai QRIS dong", "Tambah pembayaran QRIS"), 0.3)
        self.assertGreater(fider.kemiripan("Tambah pembayaran QRIS", "tolong tambah pembayaran QRIS"), 0.6)
        self.assertLess(fider.kemiripan("Warna hitam", "Ongkir ke luar Jawa"), 0.3)

    def test_periksa_url(self):
        fider.periksa_url("http://localhost:3000")
        fider.periksa_url("https://saran.tokosaya.id")
        for buruk in ("http://saran.tokosaya.id", "ftp://x", "https://user:pw@x.id", "localhost"):
            with self.assertRaises(fider.Gagal):
                fider.periksa_url(buruk)

    def test_samarkan_kunci(self):
        self.assertEqual(fider.samarkan("galat abc123 xyz", "abc123"), "galat *** xyz")

    def test_nomor_dan_slug(self):
        self.assertEqual(fider.nomor_valid("#12"), 12)
        self.assertEqual(fider.slug_tag("Fitur Baru!"), "fitur-baru")
        with self.assertRaises(fider.Gagal):
            fider.nomor_valid("1; DROP")


if __name__ == "__main__":
    unittest.main(verbosity=1)
