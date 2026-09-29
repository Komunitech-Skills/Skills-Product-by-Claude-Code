#!/usr/bin/env python3
"""Uji regresi umami.py memakai server Umami TIRUAN (http.server standar).

Jawaban server tiruan diputar ulang dari tests/fixtures/umami-3.4.0.json, yang DIREKAM (tests/rekam_fixture.py)
dari Umami 3.4.0 ASLI (image resmi, PostgreSQL 15, 127.0.0.1) berisi kunjungan fiktif tests/isi_data_fiktif.py.
Kunci rekaman = 'METODE path?query' persis seperti dikirim script, per peran kunci: 'baca' (akun view-only
anggota tim), 'admin' (melihat 2 website), 'lain' (kunci salah), 'tanpa' (tanpa kunci, heartbeat).

Angka penting dibandingkan dengan hitungan INDEPENDEN dari daftar kunjungan fiktif (isi_data_fiktif.harapan),
bukan disalin dari keluaran script. Tidak butuh internet atau Umami sungguhan.

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
"""
import argparse
import csv
import importlib.util
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP = os.path.join(SINI, "..", "scripts", "umami.py")
FIX = json.load(open(os.path.join(SINI, "fixtures", "umami-3.4.0.json"), encoding="utf-8"))["rekaman"]
PY = sys.executable
SEKARANG = "2026-09-29T16:00"


def muat(nama, path):
    spec = importlib.util.spec_from_file_location(nama, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


um = muat("umami_mod", SKRIP)
data = muat("isi_data_fiktif", os.path.join(SINI, "isi_data_fiktif.py"))

KUNCI_BACA = "umami_UjiBaca00000000000000000000000000"
KUNCI_ADMIN = "umami_UjiAdmin0000000000000000000000000"
JWT_SESI = "jwt-sesi-uji"
PERAN = {KUNCI_BACA: "baca", KUNCI_ADMIN: "admin", JWT_SESI: "baca"}
SITUS_BATIK = "9a6ec2d7-668a-4e66-a2ea-85c6484bc2e2"


class Tiruan:
    def __init__(self):
        self.diterima = []
        self.timpa = {}
        self.login_2fa = False
        self.kosong = False  # True: rentang tanpa rekaman dijawab kosong (website tanpa data di rentang itu)


def buat_handler(t):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _jawab(self, status, body, jenis="application/json"):
            raw = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", jenis)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _layani(self):
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n)) if n else None
            auth = self.headers.get("Authorization") or ""
            tok = auth[7:] if auth.startswith("Bearer ") else ""
            peran = PERAN.get(tok, "lain" if tok else "tanpa")
            key = f"{self.command} {self.path}"
            t.diterima.append((self.command, self.path, peran, auth))
            if key in t.timpa:
                status, isi = t.timpa[key]
                return self._jawab(status, isi, "text/html" if isinstance(isi, bytes) else "application/json")
            if key == "POST /api/auth/login":
                if body == {"username": "agen-baca", "password": "sandi-benar-uji"}:
                    if t.login_2fa:
                        return self._jawab(200, {"requiresTwoFactor": True, "partialToken": "x"})
                    return self._jawab(200, {"token": JWT_SESI, "user": {"username": "agen-baca"}})
                return self._jawab(401, {"error": {"message": "Unauthorized", "code": "incorrect-username-password"}})
            rek = FIX.get(peran, {})
            if key in rek:
                status, isi = rek[key]
                return self._jawab(status, isi)
            if t.kosong and peran == "baca" and self.command == "GET" and "/websites/" in key and "startAt=" in key:
                if "/stats?" in key:
                    return self._jawab(200, {"pageviews": 0, "visitors": 0, "visits": 0, "bounces": 0, "totaltime": 0})
                return self._jawab(200, [])
            if peran == "lain":
                return self._jawab(401, {"error": {"message": "Unauthorized", "status": 401}})
            return self._jawab(599, {"error": f"TIDAK ADA REKAMAN: {peran} {key}"})

        do_GET = do_POST = _layani

    return H


class DasarServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = Tiruan()
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), buat_handler(cls.t))
        cls.url = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.home = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        self.t.timpa.clear()
        self.t.diterima.clear()
        self.t.login_2fa = False
        self.t.kosong = False

    def jalan(self, *arg, kunci=KUNCI_BACA, env_tambah=None, url=True, sekarang=True, cwd=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith("UMAMI_")}
        env["HOME"] = self.home
        env["USERPROFILE"] = self.home
        if kunci:
            env["UMAMI_API_KEY"] = kunci
        env.update(env_tambah or {})
        cmd = [PY, SKRIP, *arg]
        if url:
            cmd += ["--url", self.url]
        if sekarang and arg and arg[0] not in ("cek", "situs", "simpan-kunci", "simpan-alamat"):
            cmd += ["--sekarang", SEKARANG]
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60, cwd=cwd or self.home)
        return p.returncode, p.stdout, p.stderr

    def json_(self, *arg, **kw):
        kode, out, err = self.jalan(*arg, "--json", **kw)
        self.assertEqual(kode, 0, err)
        return json.loads(out)


# ============================================================ fungsi murni


class UjiFungsi(unittest.TestCase):
    def test_format_angka(self):
        self.assertEqual(um.ribuan(1234567), "1.234.567")
        self.assertEqual(um.desimal(27.2727), "27,3")
        self.assertEqual(um.desimal(25.0), "25")
        self.assertEqual(um.persen(3, 11), "27,3%")
        self.assertEqual(um.persen(1, 0), "-")
        self.assertEqual(um.durasi(48), "48 dtk")
        self.assertEqual(um.durasi(97), "1 mnt 37 dtk")
        self.assertEqual(um.durasi(120), "2 mnt")
        self.assertEqual(um.durasi(3725), "1 jam 2 mnt")
        self.assertEqual(um.perubahan(11, 4), "naik 7 (+175%)")
        self.assertEqual(um.perubahan(2, 4), "turun 2 (-50%)")
        self.assertEqual(um.perubahan(3, 0), "baru")
        self.assertEqual(um.perubahan(5, 5), "sama")
        self.assertEqual(um.angka("11"), 11)
        self.assertEqual(um.angka(None), 0)

    def _r(self, periode=None, dari=None, sampai=None, sekarang=SEKARANG):
        return um.rentang(argparse.Namespace(tz="WIB", sekarang=sekarang, periode=periode, dari=dari, sampai=sampai))

    def test_rentang_minggu(self):
        r = self._r("minggu-lalu")
        self.assertEqual(r["awal"].isoformat(), "2026-09-21T00:00:00+07:00")
        self.assertEqual(r["akhir"].isoformat(), "2026-09-28T00:00:00+07:00")
        self.assertEqual(r["b_awal"].isoformat(), "2026-09-14T00:00:00+07:00")
        r = self._r("minggu-ini")
        self.assertEqual(r["awal"].isoformat(), "2026-09-28T00:00:00+07:00")
        self.assertEqual(r["b_akhir"].isoformat(), "2026-09-22T16:00:00+07:00")  # sama panjang s.d. jam sama
        # Senin pagi: minggu-lalu = Senin-Minggu sebelumnya penuh
        r = self._r("minggu-lalu", sekarang="2026-09-28T08:00")
        self.assertEqual((r["awal"].date().isoformat(), r["akhir"].date().isoformat()), ("2026-09-21", "2026-09-28"))

    def test_rentang_bulan_dan_manual(self):
        r = self._r("bulan-lalu")
        self.assertEqual((r["awal"].date().isoformat(), r["akhir"].date().isoformat()), ("2026-08-01", "2026-09-01"))
        self.assertEqual(r["b_awal"].date().isoformat(), "2026-07-01")
        r = self._r("bulan-ini", sekarang="2026-03-31T10:00")
        self.assertEqual(r["b_akhir"].isoformat(), "2026-02-28T10:00:00+07:00")  # tanggal 31 -> 28 Feb
        r = self._r(dari="2026-09-21", sampai="2026-09-27")
        self.assertEqual(r["akhir"].isoformat(), "2026-09-28T00:00:00+07:00")  # --sampai inklusif
        self.assertEqual(r["b_awal"].isoformat(), "2026-09-14T00:00:00+07:00")
        q = um.query_rentang(r)
        self.assertEqual(q["endAt"] - q["startAt"], 7 * 86400000 - 1)
        self.assertEqual(q["timezone"], "Asia/Jakarta")
        for salah in [dict(dari="2026-09-30", sampai="2026-09-01"), dict(dari="2026-13-01", sampai="2026-12-01"),
                      dict(dari="2026-09-01", sampai=None)]:
            with self.assertRaises(um.Gagal):
                self._r(**salah)

    def test_periksa_url(self):
        um.periksa_url("http://localhost:3000", False)
        um.periksa_url("http://127.0.0.1:3000", False)
        um.periksa_url("http://192.168.1.10:3000", False)
        um.periksa_url("https://analitik.tokosaya.id", True)
        for url, publik in [("http://analitik.tokosaya.id", True), ("https://analitik.tokosaya.id", False),
                            ("ftp://localhost", True), ("http://localhost:3000/login", True),
                            ("http://localhost:3000/api", True)]:
            with self.assertRaises(um.Gagal, msg=url):
                um.periksa_url(url, publik)

    def test_csv_aman_dan_samaran(self):
        self.assertEqual(um.aman_csv("=HYPERLINK(1)"), "'=HYPERLINK(1)")
        self.assertEqual(um.aman_csv("-promo"), "'-promo")
        self.assertEqual(um.aman_csv("/produk"), "/produk")
        self.assertEqual(um.samarkan("umami_AbCdEf0000000000000000000000WXYZ"), "umami_Ab****WXYZ")
        self.assertEqual(um.samarkan("sandi-rahasia"), "(sandi, disembunyikan)")


# ============================================================ perintah lewat server tiruan


class UjiPerintah(DasarServer):
    H_MINGGU_LALU = data.harapan("2026-09-21", "2026-09-27")
    H_SEBELUM = data.harapan("2026-09-14", "2026-09-20")

    def test_ringkasan_minggu_lalu_cocok_hitungan_independen(self):
        j = self.json_("ringkasan", "--periode", "minggu-lalu")
        h, hb = self.H_MINGGU_LALU, self.H_SEBELUM
        s = j["statistik"]
        self.assertEqual((s["pengunjung"], s["kunjungan"], s["tayangan"], s["bounce"], s["total_detik"]),
                         (h["pengunjung"], h["kunjungan"], h["tayangan"], h["bounce"], h["total_detik"]))
        self.assertEqual(s["bounce_persen"], round(h["bounce"] * 100 / h["kunjungan"], 1))
        self.assertEqual(s["rata_detik"], h["total_detik"] // h["kunjungan"])
        b = j["pembanding"]
        self.assertEqual((b["pengunjung"], b["kunjungan"], b["tayangan"], b["bounce"]),
                         (hb["pengunjung"], hb["kunjungan"], hb["tayangan"], hb["bounce"]))
        self.assertIn("11   (sebelumnya 4; naik 7 (+175%))", j["teks"])
        self.assertIn("Bounce rate           : 25%", j["teks"])
        self.assertIn("48 dtk per kunjungan", j["teks"])

    def test_semua_periode_berjalan(self):
        for p in um.PERIODE:
            kode, out, err = self.jalan("ringkasan", "--periode", p)
            self.assertEqual(kode, 0, f"{p}: {err}")
        kode, out, err = self.jalan("ringkasan", "--dari", "2026-09-21", "--sampai", "2026-09-27")
        self.assertEqual(kode, 0, err)
        self.assertIn("21 Sep 2026 - 27 Sep 2026", out)

    def test_hari_ini_dan_kemarin_cocok(self):
        j = self.json_("ringkasan", "--periode", "kemarin")
        h = data.harapan("2026-09-28", "2026-09-28")
        self.assertEqual((j["statistik"]["pengunjung"], j["statistik"]["tayangan"], j["statistik"]["total_detik"]),
                         (h["pengunjung"], h["tayangan"], h["total_detik"]))

    def test_halaman_teratas(self):
        j = self.json_("halaman", "--periode", "minggu-lalu")
        pengunjung = {d["nama"]: d["pengunjung"] for d in j["halaman"]}
        self.assertEqual(pengunjung, self.H_MINGGU_LALU["halaman"])
        tay = {d["nama"]: d["tayangan"] for d in j["halaman"]}
        self.assertEqual(tay["/"], 11)
        self.assertEqual(sum(tay.values()), self.H_MINGGU_LALU["tayangan"])
        self.assertEqual(j["halaman"][0]["nama"], "/")
        kode, out, _ = self.jalan("halaman", "--jenis", "masuk", "--periode", "minggu-lalu")
        self.assertEqual(kode, 0)
        self.assertIn("HALAMAN MASUK", out)

    def test_sumber(self):
        j = self.json_("sumber", "--periode", "minggu-lalu")
        self.assertEqual({d["nama"]: d["pengunjung"] for d in j["referrer"]}, self.H_MINGGU_LALU["referrer"])
        kanal = {d["nama"]: d["kunjungan"] for d in j["kanal"]}
        self.assertEqual(kanal, {"organicSocial": 6, "direct": 4, "organicSearch": 2})
        self.assertEqual(sum(kanal.values()), self.H_MINGGU_LALU["kunjungan"])
        self.assertIn("WhatsApp", j["teks"])

    def test_utm(self):
        j = self.json_("utm", "--periode", "minggu-lalu")
        self.assertEqual({d["nama"]: d["pengunjung"] for d in j["utm"]["utmSource"]}, self.H_MINGGU_LALU["utm_source"])
        self.assertEqual({d["nama"]: d["pengunjung"] for d in j["utm"]["utmCampaign"]},
                         self.H_MINGGU_LALU["utm_campaign"])
        j = self.json_("utm", "--periode", "minggu-ini")
        self.assertIn("reseller-okt", {d["nama"] for d in j["utm"]["utmCampaign"]})

    def test_pengunjung(self):
        j = self.json_("pengunjung", "--periode", "minggu-lalu", "--semua")
        h = self.H_MINGGU_LALU
        dev = {d["nama"]: d["jumlah"] for d in j["pengunjung"]["device"]}
        self.assertEqual(dev, {"mobile": h["perangkat"]["android"] + h["perangkat"]["iphone"],
                               "desktop": h["perangkat"]["windows"], "tablet": h["perangkat"]["tablet"]})
        self.assertEqual({d["nama"]: d["jumlah"] for d in j["pengunjung"]["city"]}, h["kota"])
        self.assertEqual({d["nama"]: d["jumlah"] for d in j["pengunjung"]["country"]}, h["negara"])
        self.assertIn("HP", j["teks"])
        self.assertIn("Kuala Lumpur, Malaysia", j["teks"])
        # urutan tetap: seri diurutkan nama
        kota = [d["nama"] for d in j["pengunjung"]["city"]]
        self.assertEqual(kota[:2], ["Jakarta", "Surabaya"])

    def test_konversi(self):
        j = self.json_("konversi", "--periode", "minggu-lalu")
        self.assertEqual({d["nama"]: d["tayangan"] for d in j["event"]}, self.H_MINGGU_LALU["event"])
        self.assertIn("27,3%", j["teks"])  # 3 dari 11 pengunjung klik WA
        nilai = [r for r in j["rincian"] if r["properti"] == "nilai"][0]
        self.assertEqual(nilai["jumlah_total"], 25000 + 22000)
        self.assertIn("Rp47.000", j["teks"])
        self.assertIn("BUKAN omzet resmi", j["teks"])

    def test_banding_minggu_ini(self):
        j = self.json_("banding")
        h = data.harapan("2026-09-28", "2026-09-29")
        self.assertEqual((j["statistik"]["pengunjung"], j["statistik"]["tayangan"]), (h["pengunjung"], h["tayangan"]))
        # pembanding = Senin 21 Sep 00.00 s.d. Selasa 22 Sep 16.00 (sama panjang): hanya kunjungan A & E
        self.assertEqual((j["pembanding"]["pengunjung"], j["pembanding"]["tayangan"]), (2, 5))
        self.assertIn("pukul 16.00 (sama panjang)", j["teks"])
        self.assertIn("naik 5 (+250%)", j["teks"])

    def test_laporan_mingguan(self):
        kode, out, err = self.jalan("laporan-mingguan")
        self.assertEqual(kode, 0, err)
        self.assertLess(len(out), 4096)  # batas satu pesan Telegram
        for frasa in ("minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026", "klik-wa: 3x oleh 3 pengunjung (27,3%)",
                      "1. / - 11 tayangan, 10 pengunjung", "kampanye promo-gajian-sep: 7", "Perangkat: HP 73%"):
            self.assertIn(frasa, out)

    def test_ekspor_csv(self):
        with tempfile.TemporaryDirectory() as d:
            kode, out, err = self.jalan("ekspor-csv", "--periode", "minggu-lalu", "--keluaran", "a.csv", cwd=d)
            self.assertEqual(kode, 0, err)
            with open(os.path.join(d, "a.csv"), encoding="utf-8-sig") as f:
                baris = list(csv.reader(f, delimiter=";"))
        self.assertTrue(baris[0][0].startswith("# Umami"))
        self.assertEqual(baris[1][:3], ["bagian", "nama", "pengunjung"])
        tot = [b for b in baris if b[0] == "ringkasan"][0]
        self.assertEqual(tot[2:8], ["11", "12", "23", "3", "25,0", "48"])
        harian = [b for b in baris if b[0] == "harian"]
        self.assertEqual(len(harian), 7)
        self.assertEqual(sum(int(b[4]) for b in harian), 23)
        hal = [b for b in baris if b[0] == "halaman" and b[1] == "/"][0]
        self.assertEqual(hal[5:8], ["", "", ""])  # bounce per halaman tidak diisi (Umami 3.4.0 memberi 0 palsu)
        self.assertIn(["kanal", "Media sosial", "6", "6", "8", "3", "50,0", "11"], baris)

    def test_tautan_pelacak(self):
        kode, out, err = self.jalan("tautan", "--sekarang", "2026-09-29T17:00", sekarang=False)
        self.assertEqual(kode, 0, err)
        j = self.json_("tautan", "--sekarang", "2026-09-29T17:00", sekarang=False)
        t = j["tautan"][0]
        # 3 klik nyata ke https://<umami>/q/wa-busri-bio dari 3 HP fiktif ber-referer Instagram
        self.assertEqual((t["nama"], t["klik"], t["pengunjung"], t["klik_sebelumnya"]), ("WA order (bio IG)", 3, 3, 0))
        self.assertEqual(t["referrer"], [{"nama": "l.instagram.com", "jumlah": 3}])
        self.assertIn("l.instagram.com (3)", out)

    def test_cek_tidak_membocorkan_kunci(self):
        kode, out, err = self.jalan("cek")
        self.assertEqual(kode, 0, err)
        self.assertNotIn(KUNCI_BACA, out + err)
        self.assertIn("umami_Uj****0000", out)
        self.assertIn("view-only", out)
        self.assertIn("Usaha Bu Sri", out)
        j = self.json_("cek")
        self.assertNotIn("token", json.dumps(j))
        self.assertNotIn("accessCode", json.dumps(j))

    def test_admin_dua_situs(self):
        kode, out, err = self.jalan("ringkasan", kunci=KUNCI_ADMIN)
        self.assertEqual(kode, 7)
        self.assertIn("Toko Batik Laras", err)
        kode, out, err = self.jalan("ringkasan", "--situs", "batik", "--periode", "30hari", kunci=KUNCI_ADMIN)
        self.assertEqual(kode, 0, err)
        self.assertIn("Toko Batik Laras", out)

    def test_situs_tidak_ada(self):
        kode, out, err = self.jalan("ringkasan", "--situs", "batik")
        self.assertEqual(kode, 2)
        self.assertIn("tidak ditemukan", err)

    def test_kunci_salah(self):
        kode, out, err = self.jalan("ringkasan", kunci="umami_salahsalahsalahsalahsalahsalah12")
        self.assertEqual(kode, 5)
        self.assertIn("kunci API salah", err)
        self.assertNotIn("umami_salahsalah", err)

    def test_401_tanpa_akses_website(self):
        k = um.Klien(argparse.Namespace(url=self.url, timeout=10, kunci_file=None))
        os.environ["UMAMI_API_KEY"] = KUNCI_BACA
        try:
            with self.assertRaises(um.Gagal) as c:
                k.get(f"/websites/{SITUS_BATIK}/stats", {"startAt": 1789923600000, "endAt": 1790528399999,
                                                        "timezone": "Asia/Jakarta"})
        finally:
            del os.environ["UMAMI_API_KEY"]
        self.assertEqual(c.exception.kode, 5)
        self.assertIn("TIDAK PUNYA AKSES", str(c.exception))

    def test_login_sandi(self):
        env = {"UMAMI_USERNAME": "agen-baca", "UMAMI_PASSWORD": "sandi-benar-uji"}
        kode, out, err = self.jalan("ringkasan", "--periode", "minggu-lalu", kunci=None, env_tambah=env)
        self.assertEqual(kode, 0, err)
        self.assertIn("Pengunjung unik       : 11", out)
        self.assertNotIn("sandi-benar-uji", out + err)
        env["UMAMI_PASSWORD"] = "salah"
        kode, out, err = self.jalan("ringkasan", kunci=None, env_tambah=env)
        self.assertEqual(kode, 5)
        self.t.login_2fa = True
        env["UMAMI_PASSWORD"] = "sandi-benar-uji"
        kode, out, err = self.jalan("ringkasan", kunci=None, env_tambah=env)
        self.assertEqual(kode, 5)
        self.assertIn("2FA", err)
        kode, out, err = self.jalan("ringkasan", kunci=None, env_tambah={"UMAMI_PASSWORD": "x"})
        self.assertEqual(kode, 2)
        self.assertIn("UMAMI_USERNAME", err)

    def test_galat_server(self):
        kunci = [k for k in FIX["baca"] if "82bc6b1f-3021-4699-bd48-bd3acd2c86e9/stats?startAt=1789923600000&endAt=1790528399999&" in k][0]  # minggu-lalu
        self.t.timpa[kunci] = (500, {"error": "x"})
        kode, out, err = self.jalan("ringkasan", "--periode", "minggu-lalu")
        self.assertEqual(kode, 4)
        self.assertIn("galat server (500)", err)
        self.t.timpa.clear()
        self.t.timpa["GET /api/heartbeat"] = (200, b"<html>bukan umami</html>")
        kode, out, err = self.jalan("cek")
        self.assertEqual(kode, 4)
        self.assertIn("bukan JSON", err)

    def test_proxy_env_diabaikan_untuk_lokal(self):
        env = {"HTTP_PROXY": "http://127.0.0.1:9", "http_proxy": "http://127.0.0.1:9", "NO_PROXY": "", "no_proxy": ""}
        kode, out, err = self.jalan("ringkasan", "--periode", "minggu-lalu", env_tambah=env)
        self.assertEqual(kode, 0, err)

    def test_alamat_publik(self):
        kode, _, err = self.jalan("cek", url=False, env_tambah={"UMAMI_URL": "http://analitik.tokosaya.id"})
        self.assertEqual(kode, 2)
        self.assertIn("wajib HTTPS", err)
        kode, _, err = self.jalan("cek", "--url", "https://analitik.tokosaya.id", url=False)
        self.assertEqual(kode, 2)
        self.assertIn("--izinkan-jarak-jauh", err)


class UjiRevisi101(DasarServer):
    """Regresi revisi 1.0.1 (perbaikan dari HASIL-UJI 1.0.0)."""

    def test_rata_rata_lama_dijelaskan_dan_konsisten_dengan_umami(self):
        for perintah in ("ringkasan", "banding", "laporan-mingguan"):
            kode, out, err = self.jalan(perintah, "--periode", "minggu-lalu")
            self.assertEqual(kode, 0, err)
            self.assertIn("mengikuti hitungan Umami", out, perintah)
        j = self.json_("ringkasan", "--periode", "minggu-lalu")
        # angka yang tampil = total lama / kunjungan (dibulatkan ke bawah), sama dengan Umami
        self.assertEqual(j["statistik"]["rata_detik"], j["statistik"]["total_detik"] // j["statistik"]["kunjungan"])

    def test_periode_tak_dikenal_pesan_indonesia(self):
        kode, out, err = self.jalan("ringkasan", "--periode", "tahun-lalu")
        self.assertEqual(kode, 2)
        self.assertIn("Periode tidak dikenal: tahun-lalu", err)
        self.assertIn("minggu-lalu", err)
        self.assertNotIn("invalid choice", err)
        self.assertNotIn("usage:", err)
        kode, out, err = self.jalan("ringkasan", "--tz", "XYZ")
        self.assertEqual(kode, 2)
        self.assertIn("Zona waktu tidak dikenal", err)

    def _kosong(self, semua):
        """Jalankan ringkasan rentang kosong; 'semua' = jawaban stats sepanjang waktu (None = tidak ada rekaman)."""
        args = ("ringkasan", "--dari", "2020-01-01", "--sampai", "2020-01-07")
        self.t.kosong = True
        kode, out, err = self.jalan(*args)
        self.assertEqual(kode, 0, err)
        if semua is not None:
            path = [p for (_, p, _, _) in self.t.diterima if "/stats?startAt=0&" in p][0]
            self.t.timpa["GET " + path] = (500, {"error": "x"}) if semua == "gagal" else (200, semua)
            kode, out, err = self.jalan(*args)
            self.assertEqual(kode, 0, err)
        return out

    def test_rentang_kosong_membedakan_kode_pelacak(self):
        ada = {"pageviews": 23, "visitors": 11, "visits": 12, "bounces": 3, "totaltime": 500}
        nol = {"pageviews": 0, "visitors": 0, "visits": 0, "bounces": 0, "totaltime": 0}
        out = self._kosong(ada)
        self.assertIn("punya data di periode lain", out)
        self.assertNotIn("cek kode pelacak", out)
        self.t.timpa.clear()
        out = self._kosong(nol)
        self.assertIn("belum pernah mencatat pengunjung", out)
        self.assertIn("cek kode pelacak", out)
        self.t.timpa.clear()
        out = self._kosong("gagal")  # cek data sepanjang waktu gagal -> pesan netral, tidak menyesatkan
        self.assertIn("Belum ada pengunjung tercatat pada periode ini.", out)
        self.assertNotIn("cek kode pelacak", out)

    def test_konversi_hari_hanya_event_diberi_catatan(self):
        args = ("konversi", "--periode", "minggu-lalu")
        kode, out, err = self.jalan(*args)
        self.assertEqual(kode, 0, err)
        self.assertNotIn("0 pengunjung unik", out)
        path = [p for (_, p, _, _) in self.t.diterima if "/stats?" in p][0]
        self.t.timpa["GET " + path] = (200, {"pageviews": 0, "visitors": 0, "visits": 0, "bounces": 0, "totaltime": 0})
        kode, out, err = self.jalan(*args)
        self.assertEqual(kode, 0, err)
        self.assertIn("0 pengunjung unik", out)
        self.assertIn("tidak bisa dihitung", out)

    def test_versi(self):
        self.assertEqual(um.VERSI, "1.0.1")


class UjiPengalihan(unittest.TestCase):
    def test_tidak_ikut_redirect(self):
        tujuan = []

        class Tujuan(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                tujuan.append(self.headers.get("Authorization"))
                self.send_response(200)
                self.end_headers()

        s2 = ThreadingHTTPServer(("127.0.0.1", 0), Tujuan)
        threading.Thread(target=s2.serve_forever, daemon=True).start()
        port2 = s2.server_address[1]

        class Alih(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                self.send_response(302)
                self.send_header("Location", f"http://127.0.0.1:{port2}{self.path}")
                self.end_headers()

        s1 = ThreadingHTTPServer(("127.0.0.1", 0), Alih)
        threading.Thread(target=s1.serve_forever, daemon=True).start()
        env = {k: v for k, v in os.environ.items() if not k.startswith("UMAMI_")}
        env["UMAMI_API_KEY"] = KUNCI_BACA
        p = subprocess.run([PY, SKRIP, "ringkasan", "--url", f"http://127.0.0.1:{s1.server_address[1]}"],
                           capture_output=True, text=True, env=env, timeout=30)
        s1.shutdown()
        s2.shutdown()
        self.assertEqual(p.returncode, 4)
        self.assertIn("TIDAK mengikuti pengalihan", p.stderr)
        self.assertEqual(tujuan, [])  # kunci tidak pernah sampai ke alamat tujuan pengalihan


class UjiSimpanKunci(unittest.TestCase):
    def test_simpan_kunci(self):
        with tempfile.TemporaryDirectory() as home:
            env = {k: v for k, v in os.environ.items() if not k.startswith("UMAMI_")}
            env["HOME"] = env["USERPROFILE"] = home
            p = subprocess.run([PY, SKRIP, "simpan-kunci"], input=KUNCI_BACA + "\n", capture_output=True, text=True,
                               env=env, timeout=30)
            self.assertEqual(p.returncode, 0, p.stderr)
            path = os.path.join(home, ".komunitech", "umami-kunci.txt")
            with open(path, encoding="utf-8") as f:
                self.assertEqual(f.read().strip(), KUNCI_BACA)
            self.assertNotIn(KUNCI_BACA, p.stdout + p.stderr.replace("Tempel kunci", ""))
            if os.name != "nt":
                self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)
            p = subprocess.run([PY, SKRIP, "simpan-kunci"], input="umami_lain\n", capture_output=True, text=True,
                               env=env, timeout=30)
            self.assertEqual(p.returncode, 3)
            p = subprocess.run([PY, SKRIP, "simpan-kunci"], input="ada spasi\n", capture_output=True, text=True,
                               env=env, timeout=30)
            self.assertEqual(p.returncode, 3)  # file sudah ada -> tolak dulu sebelum membaca



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "umami.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["simpan-kunci", "--kunci-file", os.path.join(t, "k.txt"), "--y"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "k.txt")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main(verbosity=1)
