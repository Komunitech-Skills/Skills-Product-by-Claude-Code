#!/usr/bin/env python3
"""Uji regresi fider.py dengan server Fider TIRUAN (perilaku dicocokkan dengan Fider v0.38.0 asli).

Jalankan:  python3 tests/uji_regresi.py   (Windows: python / py). Tanpa paket tambahan.
"""
import contextlib
import datetime as dt
import http.server
import io
import json
import os
import re
import subprocess
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
                    200, [{"createdAt": (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")}] * ps["votesCount"])  # selalu "minggu ini"
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

    def test_impor_tahan_mirip_dan_tetap_per_butir(self):
        p = self.tulis("Tolong tambah pembayaran QRIS\n\nBisa bayar pakai OVO\n")
        rc, out, _ = self.jalan("impor", p, "--ya")
        self.assertIn("1 pos dibuat, 1 ditahan", out)
        rc, out, _ = self.jalan("impor", self.tulis("Tolong tambah pembayaran QRIS\n", "b.txt"), "--ya")
        self.assertIn("0 pos dibuat, 1 ditahan", out)
        rc, out, _ = self.jalan("impor", self.tulis("Tolong tambah pembayaran QRIS\n", "c.txt"), "--ya", "--tetap", "1")
        self.assertIn("1 pos dibuat, 0 ditahan", out)
        rc, out, _ = self.jalan("impor", self.tulis("Tolong tambah pembayaran QRIS\n", "d.txt"), "--ya", "--tetap", "9")
        self.assertEqual(rc, fider.K_INPUT)

    def test_impor_gopay_tidak_dianggap_duplikat_qris(self):
        p = self.tulis("Tambah pembayaran GoPay\n\nTambah pembayaran ShopeePay\n")
        rc, out, _ = self.jalan("impor", p)
        self.assertEqual(out.count("[BUAT  ]"), 2, out)
        self.assertNotIn("MIRIP", out)

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

    def test_impor_sumber_disamarkan(self):
        p = self.tulis("Tambah warna hitam\n")
        rc, out, _ = self.jalan("impor", p, "--sumber", "WA dari 0812-3456-7890", "--ya")
        self.assertEqual(rc, 0, out)
        self.assertNotIn("3456", json.dumps(Tiruan.data["posts"]))
        self.assertNotIn("3456", out)
        rc, out, _ = self.jalan("impor", self.tulis("Tambah ukuran besar\n", "b.txt"), "--sumber", "WA 0812-3456-7890")
        self.assertNotIn("3456", out)
        self.assertIn("[nomor disembunyikan]", out)

    def test_impor_pelanggan_negatif_dan_tidak_wajar_ditolak(self):
        for nilai in ("-5", "0", "99999999999999999999", "true", "\"abc\"", "1.5e400"):
            p = self.tulis('[{"judul":"Tambah warna hitam","pelanggan":%s}]' % nilai, "n.json")
            rc, _, err = self.jalan("impor", p, "--ya")
            self.assertEqual(rc, fider.K_FILE, nilai)
            self.assertIn("pelanggan", err)
        self.assertEqual(len(Tiruan.data["posts"]), 3)
        p = self.tulis('[{"judul":"Tambah warna hitam","pelanggan":3}]', "ok.json")
        self.assertEqual(self.jalan("impor", p, "--ya")[0], 0)

    def test_judul_pos_lama_disamarkan_saat_ditampilkan(self):
        Tiruan.data["posts"].append(pos(4, "Rina 0812-3456-7890 minta resi", 2))
        Tiruan.data["posts"].append(pos(5, "Hubungi (+62) 812 9999 8888 soal ongkir", 1))
        for perintah in (("daftar",), ("daftar", "--json"), ("lihat", "4"), ("ringkasan-mingguan",), ("draf-balasan", "4"),
                         ("cari", "resi")):
            rc, out, _ = self.jalan(*perintah)
            self.assertEqual(rc, 0, perintah)
            self.assertNotIn("3456", out, perintah)
            self.assertNotIn("9999", out, perintah)
        rc, out, _ = self.jalan("gabung", "4", "1")
        self.assertNotIn("3456", out)

    def test_url_rusak_gagal_bersih(self):
        for buruk in ("http://[::1]evil", "http://[::1", "http://localhost:abc", "http:// localhost", "https://[x"):
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = fider.main(["cek", "--url", buruk, "--kunci-file", self.kf])
            self.assertEqual(rc, fider.K_INPUT, buruk)
            self.assertIn("GALAT", err.getvalue())

    def test_status_tolak_catatan_sepele_ditolak(self):
        for c in ("-", "ok", "  ", "tidak", "12345"):
            rc, _, _ = self.jalan("status", "1", "ditolak", "--catatan", c, "--ya")
            self.assertEqual(rc, fider.K_INPUT, c)
        self.assertEqual(Tiruan.data["posts"][0]["status"], "open")
        rc, _, _ = self.jalan("status", "1", "ditolak", "--catatan", "Belum sesuai rencana produk kami", "--ya")
        self.assertEqual(rc, 0)

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


class UjiKeamananTambahan(Dasar):
    def test_singkatan_opsi_ditolak_dan_tidak_menulis(self):
        for singkat in ("--y", "--ya-"):
            with self.assertRaises(SystemExit) as c:
                with contextlib.redirect_stderr(io.StringIO()):
                    fider.main(["status", "1", "dikerjakan", singkat, "--url", self.url, "--kunci-file", self.kf])
            self.assertEqual(c.exception.code, 2)
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                fider.main(["gabung", "2", "1", "--yaa", "--url", self.url, "--kunci-file", self.kf])
        with self.assertRaises(SystemExit):  # singkatan opsi lain juga ditolak
            with contextlib.redirect_stderr(io.StringIO()):
                fider.main(["cek", "--js", "--url", self.url, "--kunci-file", self.kf])
        self.assertEqual(self.penulisan(), [])
        self.assertEqual(Tiruan.data["posts"][0]["status"], "open")

    def test_semua_parser_allow_abbrev_false(self):
        ap = fider.buat_parser()
        self.assertFalse(ap.allow_abbrev)
        for sp in ap._subparsers._group_actions[0].choices.values():
            self.assertFalse(sp.allow_abbrev)

    def test_url_http_ke_nama_host_menyerupai_ip_ditolak(self):
        for u in ("http://10.contoh.com", "http://192.168.evil.com"):
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = fider.main(["cek", "--url", u, "--kunci-file", self.kf])
            self.assertEqual(rc, fider.K_INPUT)
            self.assertIn("HTTPS", err.getvalue())

    def test_impor_berkas_kunci_ditolak_dan_tidak_tercetak(self):
        rc, out, err = self.jalan("impor", self.kf)
        self.assertEqual(rc, fider.K_FILE)
        self.assertNotIn(KUNCI, out + err)
        rc, out, err = self.jalan("impor", self.tulis("Usul baru\n\nkunci saya " + KUNCI + "\n"))
        self.assertEqual(rc, fider.K_FILE)
        self.assertNotIn(KUNCI, out + err)

    def test_butir_kosong_dibuang_dan_uraian_dibatasi(self):
        p = self.tulis("- \n- Bisa cetak label\n-\n")
        rc, out, _ = self.jalan("impor", p)
        self.assertEqual(rc, 0)
        self.assertIn("1. [BUAT  ] Bisa cetak label", out)
        self.assertEqual(self.jalan("impor", self.tulis("-\n\n*\n", "k.txt"))[0], fider.K_FILE)
        besar = self.tulis("Judul wajar\n" + "x" * 6000, "besar.txt")
        self.jalan("impor", besar, "--ya")
        self.assertLessEqual(len(Tiruan.data["posts"][-1]["description"]), 5000)

    def test_catatan_status_dan_gabung_disamarkan_dan_ditolak_wajib_alasan(self):
        rc, _, err = self.jalan("status", "1", "ditolak", "--ya")
        self.assertEqual(rc, fider.K_INPUT)
        self.assertEqual(self.penulisan(), [])
        rc, out, _ = self.jalan("status", "1", "ditolak", "--catatan", "Hubungi 08123456789 atau 021-5551234", "--ya")
        self.assertEqual(rc, 0, out)
        self.assertEqual(Tiruan.data["posts"][0]["response"]["text"], "Hubungi [nomor disembunyikan] atau [nomor disembunyikan]")

    def test_gabung_pratinjau_memuat_peringatan(self):
        rc, out, _ = self.jalan("gabung", "3", "1")
        self.assertIn("PERIKSA", out)
        self.assertIn("hampir tidak mirip", out)

    def test_draf_menyesuaikan_status(self):
        Tiruan.data["posts"][0]["status"] = "started"
        Tiruan.data["posts"][0]["title"] = "Bayar QRIS minta 4 orang"
        rc, out, _ = self.jalan("draf-balasan", "1")
        self.assertNotIn("selesai kami", out)
        self.assertNotIn("Selamat siang", out)
        self.assertIn("sedang dalam pengerjaan", out)
        rc, out, _ = self.jalan("draf-balasan", "1", "--topik", "pembayaran QRIS")
        self.assertIn("\"pembayaran QRIS\"", out)
        self.assertNotIn("4 orang", out)

    def test_galat_fider_diterjemahkan(self):
        Tiruan.data["posts"][0]["title"] = "x"

        class E:
            code = 400
            def read(self):
                return json.dumps({"errors": [{"message": "This has already been posted before"}]}).encode()
        with self.assertRaises(fider.Gagal) as c:
            fider.Klien(self.url, KUNCI)._galat_http(E(), "/x")
        self.assertIn("sudah ada", str(c.exception))

    def test_cek_tidak_menyebut_pasti_administrator(self):
        rc, out, _ = self.jalan("cek")
        self.assertIn("tidak dapat dipastikan", out)


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
        for lokal in ("http://127.0.0.1:3000", "http://127.5.6.7", "http://[::1]:3000", "http://10.1.2.3:3000",
                      "http://192.168.1.20", "http://172.16.0.5", "http://172.31.255.1"):
            fider.periksa_url(lokal)
        fider.periksa_url("https://saran.tokosaya.id")
        for buruk in ("http://saran.tokosaya.id", "ftp://x", "https://user:pw@x.id", "localhost",
                      "http://10.contoh.com", "http://192.168.evil.com", "http://172.16.evil.id", "http://127.evil.com",
                      "http://8.8.8.8", "http://172.32.0.1", "http://192.169.1.1", "http://foo.local", "http://localhost.evil.com"):
            with self.assertRaises(fider.Gagal):
                fider.periksa_url(buruk)

    def test_kemiripan_sinonim_dan_beda_permintaan(self):
        self.assertGreaterEqual(fider.kemiripan("Bayar QRIS", "Tambah pembayaran QRIS"), fider.AMBANG_MIRIP)
        self.assertGreaterEqual(fider.kemiripan("Notif WA pesanan", "Notifikasi WhatsApp pesanan"), fider.AMBANG_MIRIP)
        self.assertLess(fider.kemiripan("Tambah pembayaran GoPay", "Tambah pembayaran QRIS"), fider.AMBANG_MIRIP)
        self.assertLess(fider.kemiripan("Tambah pembayaran ShopeePay", "Tambah pembayaran QRIS"), fider.AMBANG_MIRIP)
        self.assertLess(fider.kemiripan("Notifikasi email", "Notifikasi WA"), fider.AMBANG_MIRIP)

    def test_samarkan_telepon_rumah(self):
        for t in ("telp 021-5551234", "kantor (0274) 555123 ya", "+62 21 5551234", "021 555 1234", "0274-512345", "+62-21-5551234"):
            h, n = fider.samarkan_pribadi(t)
            self.assertEqual(n, 1, t)
            self.assertNotRegex(h, r"\d{5}", t)
        for aman in ("harga Rp15.000 dan 3 pcs", "tanggal 2026-09-29", "Rp 1.021.555.000", "pesanan 12 buah 2 warna"):
            self.assertEqual(fider.samarkan_pribadi(aman)[1], 0, aman)

    def test_samarkan_format_telepon_tambahan(self):
        for x in ("(+62) 812 3456 7890", "+62-812-3456-7890", "0812.3456.7890", "62812345678901", "0812 3456 7890",
                  "0 8 1 2 3 4 5 6 7 8 9 0", "62 21 5551234", "kontak0812-3456-7890", "0812 - 3456 - 7890",
                  "0812\u20133456\u20137890", "0812/3456/7890", "tel:+622155512", "0896 1234 5678 9",
                  "hub 0812-3456-7890."):
            h, n = fider.samarkan_pribadi(x)
            self.assertGreaterEqual(n, 1, x)
            self.assertNotRegex(h, r"\d{4}", x)
        for aman in ("Rp 1.021.555.000", "tanggal 01/09/2026 pukul 10", "buka 08.00-17.00", "stok 0812", "rek 1234567890",
                     "NPWP 01.234.567.8-901.000", "Rp 1.500.000 dan 12 buah"):
            self.assertEqual(fider.samarkan_pribadi(aman)[1], 0, aman)
        self.assertEqual(fider.samarkan_pribadi("2026-09-29 0812345678")[0], "2026-09-29 [nomor disembunyikan]")
        self.assertEqual(fider.samarkan_pribadi("hub 0812-3456-7890 15 pcs")[0], "hub [nomor disembunyikan] 15 pcs")

    def test_samarkan_nama_orang(self):
        t, n = fider.samarkan_pribadi("Pak Hendra minta QRIS, hubungi Bu Sari Wulandari di 0812-3456-7890")
        self.assertNotIn("Hendra", t)
        self.assertNotIn("Sari", t)
        self.assertNotIn("0812", t)
        self.assertEqual(n, 3)
        self.assertIn("[nama disembunyikan] minta QRIS", t)
        t2, n2 = fider.samarkan_pribadi("Tambah pembayaran QRIS untuk toko")
        self.assertEqual((t2, n2), ("Tambah pembayaran QRIS untuk toko", 0))

    def test_impor_pratinjau_menandai_nama_disamarkan(self):
        butir = [{"judul": "Pak Hendra minta bayar QRIS", "uraian": "Kak Rina bilang kurirnya lambat", "tag": []}]
        r = fider.siapkan_impor(butir, "WA", [], set())[0]
        self.assertNotIn("Hendra", r["judul"] + r["uraian"])
        self.assertNotIn("Rina", r["judul"] + r["uraian"])
        self.assertEqual(r["disamarkan"], 2)

    def test_samarkan_kunci(self):
        self.assertEqual(fider.samarkan("galat abc123 xyz", "abc123"), "galat *** xyz")

    def test_nomor_dan_slug(self):
        self.assertEqual(fider.nomor_valid("#12"), 12)
        self.assertEqual(fider.slug_tag("Fitur Baru!"), "fitur-baru")
        with self.assertRaises(fider.Gagal):
            fider.nomor_valid("1; DROP")

class UjiAturanBalasan(unittest.TestCase):
    def setUp(self):
        d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.skill = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read()
        self.readme = open(os.path.join(d, "README.md"), encoding="utf-8").read()
        self.ex = open(os.path.join(d, "examples", "00-openclaw-sebelum-sesudah.md"), encoding="utf-8").read()

    def test_aturan_seorang_pelanggan(self):
        self.assertIn("seorang pelanggan", self.skill)
        self.assertIn("JANGAN mengulang nama", self.skill)

    def test_aturan_tanpa_persen_karangan(self):
        self.assertNotIn("kemiripan 100%", self.readme)
        self.assertNotIn("100% mirip", self.readme)
        self.assertNotIn("100% mirip", self.readme)

    def test_aturan_tanpa_bold_dan_impor_di_chat(self):
        self.assertIn("kata \"impor\"", self.skill)
        self.assertIn("`**`", self.skill)

    def test_contoh_sesudah_tanpa_nama(self):
        # transkrip uji lama direkam apa adanya; yang dijaga: catatan jujur ada di awal berkas
        self.assertIn("tidak disunting", self.ex[:1200])

    def test_tanpa_perintah_terminal_untuk_pengguna(self):
        self.assertNotIn("ketik sendiri", self.skill)
        self.assertNotIn("minta pengguna menjalankan", self.skill)
        self.assertNotIn("satu perintah yang memang harus diketik", self.skill)

    def test_pratinjau_script_tanpa_impor_dan_persen(self):
        src = open(fider.__file__, encoding="utf-8").read()
        self.assertNotIn("RENCANA IMPOR", src)
        self.assertNotIn("m['skor'] * 100", src)
        self.assertIn("disusun ulang", self.skill)

    def test_penomoran_aturan_berurutan(self):
        import re
        nomor = [int(n) for n in re.findall(r"^(\d+)\. \*\*", self.skill.split("## Kapan digunakan")[0], re.M)]
        self.assertEqual(nomor, sorted(nomor))

    def test_jumlah_uji_di_dokumen_sinkron(self):
        import re
        src = open(__file__, encoding="utf-8").read()
        n = len(re.findall(r"^    def test_", src, re.M))
        self.assertIn("%d uji regresi" % n, self.skill)

    def test_readme_tanpa_impor_di_contoh(self):
        blok = self.readme.split("```")[1]
        self.assertNotIn("IMPOR", blok)

    def test_batasan_tanpa_aturan_lama_galat_apa_adanya(self):
        self.assertNotIn("ditulis apa adanya ke pengguna", self.skill)
        self.assertNotIn("Jangan meminta `simpan-kunci`", self.skill)
        self.assertNotIn("Hanya bila script menjawab `GALAT` kunci belum ada (kode 3)", self.skill)
        self.assertIn("UNTUK AGEN SAJA", self.skill)
        self.assertIn("kunci ditolak", self.skill.lower())

    def test_galat_kunci_tanpa_perintah_untuk_pengguna(self):
        src = open(fider.__file__, encoding="utf-8").read()
        self.assertNotIn("Jalankan SENDIRI", src)
        env = {k: v for k, v in os.environ.items() if not k.startswith("FIDER_")}
        env["HOME"] = env["USERPROFILE"] = self.tmp_kosong()
        r = subprocess.run([sys.executable, fider.__file__, "daftar", "--url", "http://127.0.0.1:9"],
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, fider.K_KUNCI)
        self.assertIn("UNTUK AGEN SAJA", r.stderr)

    def tmp_kosong(self):
        import tempfile
        return tempfile.mkdtemp()

    def test_pratinjau_terlihat_tanpa_opsi_teknis(self):
        for baris in (fider.PRATINJAU + "\n" + "x").splitlines():
            if "--" in baris:
                self.assertIn("UNTUK AGEN SAJA", baris)

    def test_contoh_pratinjau_tanpa_nama_pelanggan(self):
        import re, glob
        d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pola = re.compile(r"\b(Pak|Bu|Ibu|Bapak|Kak|Mas|Mbak)\s+[A-Z][a-z]+")
        self.assertIsNone(pola.search(self.readme), pola.search(self.readme))
        for f in glob.glob(os.path.join(d, "examples", "*.md")):
            t = open(f, encoding="utf-8").read()
            if "FORMAT LAMA" in t[:600] or "tidak disunting" in t[:1200]:
                continue
            m = pola.search(t)
            self.assertIsNone(m, (f, m and m.group(0)))

    def test_skill_ringkas_dan_versi_sinkron(self):
        self.assertLess(len(self.skill.splitlines()), 300)
        self.assertIn("Versi " + fider.VERSI, self.skill)
        self.assertIn("**" + fider.VERSI + "**", self.readme)

    def test_ringkasan_diminta_tidak_ditunda(self):
        a = self.skill
        self.assertIn("Ringkasan yang diminta tidak boleh ditunda", a)
        self.assertIn("balasan PERTAMA", a)
        self.assertIn("5 teratas", a)
        self.assertIn("total suara", a)
        self.assertIn("Jangan menjanjikan", a)

    def test_ringkasan_angka_dari_script_bukan_kemungkinan(self):
        self.assertIn("bukan dikira-kira", self.skill)
        self.assertIn('tanpa kata "kemungkinan"', self.skill)

    def test_ringkasan_tetap_patuh_aturan_privasi(self):
        i = self.skill.index("10. **Ringkasan")
        r = self.skill[i:self.skill.index("\n", i)]
        for k in ("tanpa nama pelanggan", "tanpa persen karangan", "tanpa `**`", "tanpa kata \"impor\"", "tanpa perintah terminal"):
            self.assertIn(k, r)

    def test_tak_ada_aturan_lama_yang_menunda_ringkasan(self):
        a = self.skill
        self.assertNotIn("ringkasan menyusul", a.replace("Jangan menjanjikan \"ringkasannya menyusul\"", ""))
        self.assertIn("aturan 10", a)  # bagian C merujuk aturan baru
        self.assertIn("ringkasan (bagian C) lebih dulu", a)  # bagian A

    def test_script_ringkasan_memuat_angka_yang_diminta(self):
        # angka yang harus dilaporkan agent berasal dari keluaran script
        src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "fider.py"), encoding="utf-8").read()
        for k in ("total {angka(total_suara)} suara", "TOP {len(top)} SUARA TERBANYAK", "minggu ini)"):
            self.assertIn(k, src)


if __name__ == "__main__":
    unittest.main(verbosity=1)
