#!/usr/bin/env python3
"""Uji regresi pantau.py memakai server Uptime Kuma TIRUAN (http.server standar).

`tests/fixtures/uptime-kuma-2.5.5-status-page.json` dan `-heartbeat.json` adalah respons
API yang direkam APA ADANYA dari **Uptime Kuma 2.5.5 ASLI** (rilis resmi dari GitHub,
dijalankan sungguhan oleh Komunitech di sandbox pada 2026-09-26 - lihat
`research/sources/uptime-kuma-2026-09-26.md`). `skenario2-*.json` adalah data buatan tangan
Komunitech (ditandai jelas di dalam filenya) untuk menguji jalur kode lain (status AKTIF,
ping, sertifikat SSL hampir habis) yang tidak muncul di rekaman asli.

Sebagian uji memanggil fungsi Python langsung dan sebagian menjalankan pantau.py sebagai
proses terpisah lewat server tiruan (uji ujung-ke-ujung argparse + HTTP + SSL). Tidak
butuh internet.

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
"""
import importlib.util
import json
import os
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP = os.path.join(SINI, "..", "scripts", "pantau.py")
FIXDIR = os.path.join(SINI, "fixtures")
PY = sys.executable

spec = importlib.util.spec_from_file_location("pantau_mod", SKRIP)
pantau = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pantau)


def muat(nama):
    with open(os.path.join(FIXDIR, nama), encoding="utf-8") as f:
        return json.load(f)


REKAM_STATUS = muat("uptime-kuma-2.5.5-status-page.json")
REKAM_HEARTBEAT = muat("uptime-kuma-2.5.5-heartbeat.json")
SK2_STATUS = muat("skenario2-status-page.json")
SK2_HEARTBEAT = muat("skenario2-heartbeat.json")


# ============================================================ server Uptime Kuma tiruan

class HandlerTiruan(BaseHTTPRequestHandler):
    # Peta slug -> (config_json, heartbeat_json). Diisi lewat kelas turunan/functools.
    HALAMAN = {}

    def log_message(self, *a):
        pass  # diamkan log http.server bawaan

    def _kirim_json(self, kode, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(kode)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parts = self.path.split("?")[0].strip("/").split("/")
        # /api/status-page/<slug>  atau  /api/status-page/heartbeat/<slug>
        if len(parts) == 3 and parts[0] == "api" and parts[1] == "status-page":
            slug = parts[2]
            if slug not in self.HALAMAN:
                self._kirim_json(404, {"status": "fail", "msg": "Status Page Not Found"})
                return
            cfg, _ = self.HALAMAN[slug]
            self._kirim_json(200, cfg)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "status-page" and parts[2] == "heartbeat":
            slug = parts[3]
            if slug not in self.HALAMAN:
                self._kirim_json(404, {"status": "fail", "msg": "Status Page Not Found"})
                return
            _, hb = self.HALAMAN[slug]
            self._kirim_json(200, hb)
            return
        if parts == ["bukan-json"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html>halaman biasa, bukan API</html>")
            return
        self._kirim_json(404, {"status": "fail", "msg": "Not Found"})


def jalankan_server_tiruan(halaman):
    kelas = type("Handler", (HandlerTiruan,), {"HALAMAN": halaman})
    srv = ThreadingHTTPServer(("127.0.0.1", 0), kelas)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv


def jalankan_pantau(argv, timeout=15):
    r = subprocess.run([PY, SKRIP] + argv, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


# ============================================================ 1. urai_alamat & parser URL

class TesUraiAlamat(unittest.TestCase):
    class NS:
        def __init__(self, **kw):
            self.status_url = kw.get("status_url")
            self.url = kw.get("url")
            self.slug = kw.get("slug")

    def test_status_url_lengkap(self):
        base, slug = pantau.urai_alamat(self.NS(status_url="http://127.0.0.1:3001/status/toko-saya"))
        self.assertEqual(base, "http://127.0.0.1:3001")
        self.assertEqual(slug, "toko-saya")

    def test_status_url_dengan_slash_akhir(self):
        base, slug = pantau.urai_alamat(self.NS(status_url="http://127.0.0.1:3001/status/toko-saya/"))
        self.assertEqual(slug, "toko-saya")

    def test_url_dan_slug_terpisah(self):
        base, slug = pantau.urai_alamat(self.NS(url="http://127.0.0.1:3001/", slug="toko-saya"))
        self.assertEqual(base, "http://127.0.0.1:3001")
        self.assertEqual(slug, "toko-saya")

    def test_status_url_bentuk_salah(self):
        with self.assertRaises(pantau.Gagal):
            pantau.urai_alamat(self.NS(status_url="bukan-url-sama-sekali"))

    def test_tanpa_apa_apa(self):
        with self.assertRaises(pantau.Gagal):
            pantau.urai_alamat(self.NS())


# ============================================================ 2. urai_waktu_kuma

class TesUraiWaktu(unittest.TestCase):
    def test_dengan_mikrodetik(self):
        w = pantau.urai_waktu_kuma("2026-09-26 08:10:00.500")
        self.assertEqual(w.year, 2026)
        self.assertEqual(w.tzinfo, timezone.utc)

    def test_tanpa_mikrodetik(self):
        w = pantau.urai_waktu_kuma("2026-09-26 08:10:00")
        self.assertEqual(w.second, 0)

    def test_format_tidak_dikenali(self):
        with self.assertRaises(pantau.Gagal):
            pantau.urai_waktu_kuma("26/09/2026 08:10")


# ============================================================ 3. hitung_downtime_jendela

class TesHitungDowntime(unittest.TestCase):
    def test_kosong(self):
        menit, mulai, akhir, jumlah = pantau.hitung_downtime_jendela([], datetime.now(timezone.utc))
        self.assertEqual(menit, 0.0)
        self.assertIsNone(mulai)
        self.assertEqual(jumlah, 0)

    def test_semua_aktif(self):
        beats = [{"status": pantau.UP, "time": "2026-09-26 08:00:00"},
                  {"status": pantau.UP, "time": "2026-09-26 08:05:00"}]
        menit, mulai, akhir, jumlah = pantau.hitung_downtime_jendela(beats, datetime.now(timezone.utc))
        self.assertEqual(menit, 0.0)
        self.assertEqual(jumlah, 0)

    def test_satu_turun_di_tengah(self):
        beats = [{"status": pantau.UP, "time": "2026-09-26 08:00:00"},
                  {"status": pantau.DOWN, "time": "2026-09-26 08:05:00"},
                  {"status": pantau.UP, "time": "2026-09-26 08:12:00"}]
        menit, mulai, akhir, jumlah = pantau.hitung_downtime_jendela(beats, datetime.now(timezone.utc))
        self.assertAlmostEqual(menit, 7.0, places=3)
        self.assertEqual(jumlah, 1)

    def test_masih_turun_sampai_sekarang(self):
        sekarang = datetime(2026, 9, 26, 8, 20, 0, tzinfo=timezone.utc)
        beats = [{"status": pantau.DOWN, "time": "2026-09-26 08:10:00"}]
        menit, mulai, akhir, jumlah = pantau.hitung_downtime_jendela(beats, sekarang)
        self.assertAlmostEqual(menit, 10.0, places=3)

    def test_dua_kali_turun(self):
        beats = [{"status": pantau.DOWN, "time": "2026-09-26 08:00:00"},
                  {"status": pantau.UP, "time": "2026-09-26 08:02:00"},
                  {"status": pantau.DOWN, "time": "2026-09-26 08:10:00"},
                  {"status": pantau.UP, "time": "2026-09-26 08:13:00"}]
        menit, mulai, akhir, jumlah = pantau.hitung_downtime_jendela(beats, datetime.now(timezone.utc))
        self.assertAlmostEqual(menit, 5.0, places=3)
        self.assertEqual(jumlah, 2)


# ============================================================ 4. perintah 'cek' (ujung-ke-ujung)

class TesCmdCek(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = jalankan_server_tiruan({
            "toko-saya": (REKAM_STATUS, REKAM_HEARTBEAT),
            "toko-scenario2": (SK2_STATUS, SK2_HEARTBEAT),
        })
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def test_normal_rekam_asli(self):
        kode, out, err = jalankan_pantau(["cek", "--status-url", f"{self.base}/status/toko-saya", "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertTrue(data["ok"])
        self.assertEqual(data["judul"], "Toko Saya")
        self.assertEqual(data["jumlah_monitor"], 2)

    def test_slug_salah(self):
        kode, out, err = jalankan_pantau(["cek", "--status-url", f"{self.base}/status/tidak-ada"])
        self.assertEqual(kode, 4)
        self.assertIn("tidak ditemukan", err)

    def test_server_tidak_bisa_dihubungi(self):
        kode, out, err = jalankan_pantau(["cek", "--status-url", "http://127.0.0.1:1/status/x", "--timeout", "2"])
        self.assertEqual(kode, 4)
        self.assertIn("tidak bisa dihubungi", err)

    def test_respons_bukan_json(self):
        kode, out, err = jalankan_pantau(["cek", "--url", self.base, "--slug", "x"])
        # slug "x" tidak ada di HALAMAN -> 404 json rapi, bukan "bukan-json"; pastikan tetap galat rapi
        self.assertEqual(kode, 4)
        self.assertIn("GALAT:", err)

    def test_url_dan_slug_terpisah(self):
        kode, out, err = jalankan_pantau(["cek", "--url", self.base, "--slug", "toko-scenario2", "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["jumlah_monitor"], 2)
        self.assertTrue(data["sertifikat_ssl_ditampilkan"])


# ============================================================ 5. perintah 'ringkasan'

class TesCmdRingkasan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = jalankan_server_tiruan({
            "toko-saya": (REKAM_STATUS, REKAM_HEARTBEAT),
            "toko-scenario2": (SK2_STATUS, SK2_HEARTBEAT),
        })
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.log = os.path.join(self.tmpdir, "log.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_rekam_asli_kedua_monitor_turun(self):
        kode, out, err = jalankan_pantau(["ringkasan", "--status-url", f"{self.base}/status/toko-saya",
                                            "--log", self.log, "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        nama = {m["nama"]: m for m in data["monitor"]}
        self.assertEqual(nama["Website Toko"]["status"], "TURUN")
        self.assertEqual(nama["Halaman Checkout"]["status"], "TURUN")

    def test_skenario2_status_dan_ssl(self):
        kode, out, err = jalankan_pantau(["ringkasan", "--status-url", f"{self.base}/status/toko-scenario2",
                                            "--log", self.log, "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        nama = {m["nama"]: m for m in data["monitor"]}
        self.assertEqual(nama["Toko Online"]["status"], "AKTIF")  # heartbeat terakhir UP
        self.assertEqual(nama["Toko Online"]["sisa_hari_ssl"], 9)
        self.assertEqual(nama["Toko Online"]["uptime_24_jam_persen"], 95.0)
        self.assertEqual(nama["WA Katalog"]["jendela_jumlah_turun"], 0)

    def test_downtime_jendela_dihitung_dari_heartbeat(self):
        kode, out, err = jalankan_pantau(["ringkasan", "--status-url", f"{self.base}/status/toko-scenario2",
                                            "--log", self.log, "--json"])
        data = json.loads(out)
        nama = {m["nama"]: m for m in data["monitor"]}
        # id 10: turun 08:10-08:20 (2 titik turun berurutan -> 5 + 5 = 10 menit; lihat fixture)
        self.assertEqual(nama["Toko Online"]["jendela_jumlah_turun"], 2)
        self.assertAlmostEqual(nama["Toko Online"]["jendela_menit_turun"], 10.0, places=3)

    def test_log_tertulis(self):
        jalankan_pantau(["ringkasan", "--status-url", f"{self.base}/status/toko-scenario2", "--log", self.log])
        self.assertTrue(os.path.isfile(self.log))
        with open(self.log, encoding="utf-8") as f:
            baris = [json.loads(l) for l in f if l.strip()]
        self.assertEqual(len(baris), 2)  # 2 monitor
        self.assertIn("monitor_nama", baris[0])

    def test_tanpa_log_tidak_menulis_file(self):
        jalankan_pantau(["ringkasan", "--status-url", f"{self.base}/status/toko-scenario2",
                          "--log", self.log, "--tanpa-log"])
        self.assertFalse(os.path.isfile(self.log))

    def test_grup_kosong(self):
        cfg_kosong = {**SK2_STATUS, "publicGroupList": []}
        srv2 = jalankan_server_tiruan({"kosong": (cfg_kosong, {"heartbeatList": {}, "uptimeList": {}})})
        base2 = f"http://127.0.0.1:{srv2.server_address[1]}"
        try:
            kode, out, err = jalankan_pantau(["ringkasan", "--status-url", f"{base2}/status/kosong",
                                                "--log", self.log])
            self.assertEqual(kode, 4)
            self.assertIn("belum berisi monitor", err)
        finally:
            srv2.shutdown()


# ============================================================ 6. perintah 'mingguan' (log lokal)

class TesCmdMingguan(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.log = os.path.join(self.tmpdir, "log.jsonl")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def tulis(self, *baris):
        with open(self.log, "w", encoding="utf-8") as f:
            for b in baris:
                f.write(json.dumps(b) + "\n")

    def test_belum_ada_log(self):
        kode, out, err = jalankan_pantau(["mingguan", "--log", self.log])
        self.assertEqual(kode, 4)
        self.assertIn("Belum ada data", err)

    def test_semua_di_luar_jendela_hari(self):
        lama = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        self.tulis({"ts": lama, "base": "b", "slug": "s", "monitor_id": 1, "monitor_nama": "A",
                    "status_kode": 1, "uptime_24_jam_persen": 100, "ping_ms": 10, "sisa_hari_ssl": None})
        kode, out, err = jalankan_pantau(["mingguan", "--log", self.log])
        self.assertEqual(kode, 4)
        self.assertIn("hari terakhir", err)

    def test_agregasi_rata_rata_dan_turun(self):
        sekarang = datetime.now(timezone.utc)
        self.tulis(
            {"ts": (sekarang - timedelta(hours=2)).isoformat(), "base": "b", "slug": "s", "monitor_id": 1,
             "monitor_nama": "Toko A", "status_kode": 1, "uptime_24_jam_persen": 100.0, "ping_ms": 50, "sisa_hari_ssl": 30},
            {"ts": (sekarang - timedelta(hours=1)).isoformat(), "base": "b", "slug": "s", "monitor_id": 1,
             "monitor_nama": "Toko A", "status_kode": 0, "uptime_24_jam_persen": 80.0, "ping_ms": None, "sisa_hari_ssl": 29},
        )
        kode, out, err = jalankan_pantau(["mingguan", "--log", self.log, "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        m = data["monitor"][0]
        self.assertEqual(m["jumlah_observasi"], 2)
        self.assertAlmostEqual(m["rata_rata_uptime_24_jam_persen"], 90.0, places=3)
        self.assertEqual(m["jumlah_observasi_turun"], 1)
        self.assertEqual(m["sisa_hari_ssl_terakhir"], 29)

    def test_baris_rusak_diabaikan_bukan_gagal(self):
        sekarang = datetime.now(timezone.utc)
        with open(self.log, "w", encoding="utf-8") as f:
            f.write("{ini bukan json valid\n")
            f.write(json.dumps({"ts": sekarang.isoformat(), "base": "b", "slug": "s", "monitor_id": 1,
                                  "monitor_nama": "Toko A", "status_kode": 1, "uptime_24_jam_persen": 100.0,
                                  "ping_ms": 1, "sisa_hari_ssl": None}) + "\n")
        kode, out, err = jalankan_pantau(["mingguan", "--log", self.log, "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["baris_log_rusak_diabaikan"], 1)
        self.assertEqual(data["jumlah_observasi_total"], 1)

    def test_hari_bisa_diatur(self):
        sekarang = datetime.now(timezone.utc)
        self.tulis({"ts": (sekarang - timedelta(hours=20)).isoformat(), "base": "b", "slug": "s",
                    "monitor_id": 1, "monitor_nama": "A", "status_kode": 1, "uptime_24_jam_persen": 100.0,
                    "ping_ms": 1, "sisa_hari_ssl": None})
        kode, out, err = jalankan_pantau(["mingguan", "--log", self.log, "--hari", "1", "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["jumlah_observasi_total"], 1)


# ============================================================ 7. perintah 'cek-cepat' (tanpa Uptime Kuma)

class HandlerHTTPSederhana(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/lambat":
            import time
            time.sleep(2)
        if self.path == "/error-server":
            self.send_response(500)
            self.end_headers()
            return
        if self.path == "/tidak-ada":
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")


class TesCmdCekCepatHTTP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = HTTPServer(("127.0.0.1", 0), HandlerHTTPSederhana)
        cls.port = cls.srv.server_address[1]
        cls.t = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.t.start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def test_200_ok(self):
        kode, out, err = jalankan_pantau(["cek-cepat", f"http://127.0.0.1:{self.port}/", "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["kode_http"], 200)
        self.assertEqual(data["kategori"], "OK")
        self.assertIsNone(data["ssl"])

    def test_404(self):
        kode, out, err = jalankan_pantau(["cek-cepat", f"http://127.0.0.1:{self.port}/tidak-ada", "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["kode_http"], 404)
        self.assertIn("KLIEN", data["kategori"])

    def test_500(self):
        kode, out, err = jalankan_pantau(["cek-cepat", f"http://127.0.0.1:{self.port}/error-server", "--json"])
        data = json.loads(out)
        self.assertEqual(data["kode_http"], 500)
        self.assertIn("SERVER", data["kategori"])

    def test_timeout(self):
        kode, out, err = jalankan_pantau(["cek-cepat", f"http://127.0.0.1:{self.port}/lambat",
                                            "--timeout", "1"], timeout=10)
        self.assertEqual(kode, 4)
        self.assertIn("timeout" if "timeout" in err.lower() else "tunggu", err.lower())

    def test_koneksi_ditolak(self):
        kode, out, err = jalankan_pantau(["cek-cepat", "http://127.0.0.1:1/", "--timeout", "2"])
        self.assertEqual(kode, 4)

    def test_url_tanpa_skema_ditambah_https(self):
        # domain tak ada -> harus gagal jelas, bukan crash python
        kode, out, err = jalankan_pantau(["cek-cepat", "domain-tidak-ada.invalid.contoh", "--timeout", "3"])
        self.assertEqual(kode, 4)
        self.assertIn("GALAT:", err)

    def test_url_kosong_setelah_skema(self):
        kode, out, err = jalankan_pantau(["cek-cepat", "https://"])
        self.assertEqual(kode, 2)


class TesCmdCekCepatSSL(unittest.TestCase):
    """SSL nyata pakai sertifikat self-signed (dibuat lewat openssl, hanya untuk uji)."""

    @classmethod
    def setUpClass(cls):
        if shutil.which("openssl") is None:
            raise unittest.SkipTest("openssl tidak ada di PATH, lewati uji SSL")
        cls.tmpdir = tempfile.mkdtemp()
        cls.keyfile = os.path.join(cls.tmpdir, "key.pem")
        cls.certfile = os.path.join(cls.tmpdir, "cert.pem")
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", cls.keyfile,
            "-out", cls.certfile, "-days", "30", "-nodes", "-subj", "/CN=127.0.0.1",
        ], check=True, capture_output=True)

        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cls.certfile, cls.keyfile)
        cls.srv = HTTPServer(("127.0.0.1", 0), HandlerHTTPSederhana)
        cls.srv.socket = ctx.wrap_socket(cls.srv.socket, server_side=True)
        cls.port = cls.srv.server_address[1]
        cls.t = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.t.start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def test_https_sertifikat_self_signed_tidak_terpercaya_tapi_sisa_hari_tetap_terbaca(self):
        kode, out, err = jalankan_pantau(["cek-cepat", f"https://127.0.0.1:{self.port}/", "--json"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["kode_http"], 200)
        self.assertIsNotNone(data["ssl"])
        self.assertFalse(data["ssl"]["valid"])
        self.assertEqual(data["ssl"]["sisa_hari"], 29)  # dibuat -days 30, cek hari yang sama


if __name__ == "__main__":
    unittest.main(verbosity=2)
