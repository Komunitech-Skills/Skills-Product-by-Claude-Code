#!/usr/bin/env python3
"""Uji regresi vikunja.py memakai server Vikunja TIRUAN (http.server standar).

Bentuk data tiruan (proyek, tugas, token, pesan galat 401/404) diambil dari
tests/fixtures/vikunja-2.6.0.json, yang direkam dari Vikunja 2.6.0 ASLI (binary resmi,
checksum SHA-256 cocok) yang benar-benar dijalankan Komunitech — bukan tebakan.

Sebagian uji memanggil fungsi Python langsung (parser tanggal, dari-teks, validasi URL) dan
sebagian menjalankan vikunja.py sebagai proses terpisah lewat server tiruan (uji ujung-ke-ujung
argparse + HTTP). Tidak butuh internet atau Vikunja sungguhan.

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
"""
import datetime as dt
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP = os.path.join(SINI, "..", "scripts", "vikunja.py")
FIX = json.load(open(os.path.join(SINI, "fixtures", "vikunja-2.6.0.json"), encoding="utf-8"))
PY = sys.executable

spec = importlib.util.spec_from_file_location("vikunja_mod", SKRIP)
vikunja = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vikunja)

HARI_ACUAN = dt.date(2026, 9, 26)  # Sabtu, sesuai tanggal riset/uji


# ============================================================ 1. parser tanggal Indonesia

class TesTanggal(unittest.TestCase):
    def cocok(self, teks):
        return vikunja.cocok_tanggal_kata(teks, HARI_ACUAN)

    def test_hari_ini(self):
        self.assertEqual(self.cocok("hari ini"), HARI_ACUAN)

    def test_besok(self):
        self.assertEqual(self.cocok("besok"), HARI_ACUAN + dt.timedelta(days=1))

    def test_lusa(self):
        self.assertEqual(self.cocok("lusa"), HARI_ACUAN + dt.timedelta(days=2))

    def test_n_hari_lagi(self):
        self.assertEqual(self.cocok("3 hari lagi"), HARI_ACUAN + dt.timedelta(days=3))

    def test_minggu_depan(self):
        self.assertEqual(self.cocok("minggu depan"), HARI_ACUAN + dt.timedelta(days=7))

    def test_nama_hari_terdekat(self):
        # 26 Sep 2026 = Sabtu (weekday 5). Jumat (4) terdekat -> +6 hari (2 Okt).
        self.assertEqual(self.cocok("Jumat"), dt.date(2026, 10, 2))

    def test_nama_hari_hari_ini_sendiri(self):
        # Sabtu disebut, acuan juga Sabtu -> hari ini juga (delta 0).
        self.assertEqual(self.cocok("Sabtu"), HARI_ACUAN)

    def test_nama_hari_depan(self):
        # 'Jumat depan' melewati Jumat terdekat (2 Okt) -> Jumat pekan sesudahnya (9 Okt).
        self.assertEqual(self.cocok("Jumat depan"), dt.date(2026, 10, 9))

    def test_tanggal_slash_tanpa_tahun(self):
        self.assertEqual(self.cocok("25/10"), dt.date(2026, 10, 25))

    def test_tanggal_slash_dengan_tahun(self):
        self.assertEqual(self.cocok("25/10/2027"), dt.date(2027, 10, 25))

    def test_tanggal_slash_tahun_sudah_lewat_lompat_tahun_depan(self):
        # 1/1 tanpa tahun, acuan 26 Sep -> dianggap 1 Jan tahun depan (bukan tahun ini yang sudah lewat)
        self.assertEqual(self.cocok("1/1"), dt.date(2027, 1, 1))

    def test_nama_bulan_indonesia(self):
        self.assertEqual(self.cocok("25 Oktober 2026"), dt.date(2026, 10, 25))

    def test_nama_bulan_tanpa_tahun(self):
        self.assertEqual(self.cocok("5 Desember"), dt.date(2026, 12, 5))

    def test_iso_yyyy_mm_dd(self):
        self.assertEqual(self.cocok("2026-10-25"), dt.date(2026, 10, 25))

    def test_tidak_dikenal(self):
        self.assertIsNone(self.cocok("entah kapan lah"))

    def test_parse_tenggat_dengan_jam(self):
        iso, tgl = vikunja.parse_tenggat("besok jam 14:00", HARI_ACUAN, "WIB")
        self.assertEqual(tgl, HARI_ACUAN + dt.timedelta(days=1))
        # 14:00 WIB = 07:00 UTC
        self.assertEqual(iso, "2026-09-27T07:00:00Z")

    def test_parse_tenggat_default_jam_17(self):
        iso, _ = vikunja.parse_tenggat("besok", HARI_ACUAN, "WIB")
        self.assertEqual(iso, "2026-09-27T10:00:00Z")

    def test_parse_tenggat_gagal(self):
        with self.assertRaises(vikunja.Gagal) as c:
            vikunja.parse_tenggat("kapan-kapan", HARI_ACUAN, "WIB")
        self.assertEqual(c.exception.kode, vikunja.K_INPUT)

    def test_tanggal_tidak_valid_dilewati(self):
        # 31 Februari tidak ada -> dianggap tidak cocok, bukan error/crash
        self.assertIsNone(self.cocok("31/2"))


# ============================================================ 2. dari-teks (draf lokal)

class TesDariTeks(unittest.TestCase):
    def test_pola_nama_titik_dua(self):
        draf, _ = vikunja.urai_dari_teks("- Budi: follow up ke supplier bata sebelum Jumat", HARI_ACUAN)
        self.assertEqual(len(draf), 1)
        self.assertEqual(draf[0]["ke"], "Budi")
        self.assertEqual(draf[0]["tenggat"], "2026-10-02")

    def test_baris_tanpa_pic(self):
        draf, _ = vikunja.urai_dari_teks("- Beli semen 50 sak", HARI_ACUAN)
        self.assertIsNone(draf[0]["ke"])
        self.assertEqual(draf[0]["judul"], "Beli semen 50 sak")

    def test_kata_label_pic_di_awal_terdeteksi(self):
        # v1.0.2: "PIC: Nama <tugas>" di awal baris sekarang dikenali via label eksplisit,
        # bukan lagi dianggap "Nama: tugas" biasa (yang mengecualikan kata "pic").
        draf, _ = vikunja.urai_dari_teks("- PIC: Andi kirim penawaran", HARI_ACUAN)
        self.assertEqual(draf[0]["ke"], "Andi")
        self.assertEqual(draf[0]["judul"], "kirim penawaran")

    def test_label_pic_di_akhir_baris_terdeteksi(self):
        draf, _ = vikunja.urai_dari_teks("- Follow up klien ABC PIC: Budi", HARI_ACUAN)
        self.assertEqual(draf[0]["ke"], "Budi")
        self.assertEqual(draf[0]["judul"], "Follow up klien ABC")

    def test_label_pic_dua_kata(self):
        draf, _ = vikunja.urai_dari_teks("- Kirim invoice ke supplier PIC: Siti Aminah", HARI_ACUAN)
        self.assertEqual(draf[0]["ke"], "Siti Aminah")
        self.assertEqual(draf[0]["judul"], "Kirim invoice ke supplier")

    def test_tanpa_label_pic_tetap_tanpa_ke(self):
        draf, _ = vikunja.urai_dari_teks("- Beli semen 50 sak", HARI_ACUAN)
        self.assertIsNone(draf[0]["ke"])

    def test_baris_diabaikan_dihitung(self):
        teks = "Notulen rapat\n- Budi: telepon supplier\nCatatan tambahan tanpa bullet"
        draf, diabaikan = vikunja.urai_dari_teks(teks, HARI_ACUAN)
        self.assertEqual(len(draf), 1)
        self.assertEqual(diabaikan, 2)

    def test_penomoran_dan_bintang(self):
        teks = "1. Rina: kirim invoice\n* cek stok cat"
        draf, _ = vikunja.urai_dari_teks(teks, HARI_ACUAN)
        self.assertEqual(len(draf), 2)

    def test_kata_mendesak_jadi_prioritas_4(self):
        draf, _ = vikunja.urai_dari_teks("- Andi: kirim penawaran urgent ke klien", HARI_ACUAN)
        self.assertEqual(draf[0]["prioritas"], 4)

    def test_anggota_dikenal_2_kata(self):
        draf, _ = vikunja.urai_dari_teks("- Siti Aminah: follow up klien", HARI_ACUAN, anggota_dikenal=["Siti Aminah"])
        self.assertEqual(draf[0]["ke"], "Siti Aminah")

    def test_teks_kosong_tanpa_bullet(self):
        draf, diabaikan = vikunja.urai_dari_teks("cuma teks biasa tanpa bullet", HARI_ACUAN)
        self.assertEqual(draf, [])
        self.assertEqual(diabaikan, 1)

    def test_v103_kata_header_inggris_bukan_pic(self):
        # temuan uji ulang v1.0.2: "TOPIC:" dulu terbaca PIC "TOPIC" dan terhapus dari judul
        for kata in ("TOPIC", "INFO", "UPDATE", "STATUS", "NOTE", "AGENDA", "SUBJECT", "Next Step", "Action Items",
                     "FYI", "Reminder", "Summary", "Topik", "Perihal", "Update", "RE"):
            baris = "- %s: bahas rencana marketing minggu depan" % kata
            draf, _ = vikunja.urai_dari_teks(baris, HARI_ACUAN)
            self.assertIsNone(draf[0]["ke"], kata)
            self.assertEqual(draf[0]["judul"], "%s: bahas rencana marketing minggu depan" % kata, kata)

    def test_v103_nama_asli_tetap_terbaca(self):
        for baris, nama in (("- Budi: follow up supplier", "Budi"), ("- Siti Aminah: kirim invoice", "Siti Aminah"),
                            ("- ANDI: cek stok gudang", "ANDI"), ("- Status: cek laporan PIC: Rina", "Rina"),
                            ("- UPDATE - kirim revisi desain PIC: Maya", "Maya")):
            draf, _ = vikunja.urai_dari_teks(baris, HARI_ACUAN)
            self.assertEqual(draf[0]["ke"], nama, baris)
        # anggota yang dikenal menang atas daftar kata header (orang bernama "Tim")
        draf, _ = vikunja.urai_dari_teks("- Tim: siapkan materi", HARI_ACUAN)
        self.assertIsNone(draf[0]["ke"])
        draf, _ = vikunja.urai_dari_teks("- Tim: siapkan materi", HARI_ACUAN, anggota_dikenal=["Tim"])
        self.assertEqual(draf[0]["ke"], "Tim")


# ============================================================ 3. validasi URL (keamanan)

class TesValidasiURL(unittest.TestCase):
    class A:
        def __init__(self, url, jauh=False):
            self.url, self.izinkan_jarak_jauh = url, jauh

    def test_localhost_diizinkan(self):
        vikunja.periksa_url("http://127.0.0.1:3456", False)  # tidak melempar

    def test_domain_publik_ditolak_tanpa_flag(self):
        with self.assertRaises(vikunja.Gagal) as c:
            vikunja.periksa_url("http://vikunja.contoh.com", False)
        self.assertEqual(c.exception.kode, vikunja.K_INPUT)

    def test_domain_publik_http_ditolak_walau_izin(self):
        with self.assertRaises(vikunja.Gagal):
            vikunja.periksa_url("http://vikunja.contoh.com", True)

    def test_domain_publik_https_dengan_izin_diterima(self):
        vikunja.periksa_url("https://vikunja.contoh.com", True)

    def test_jaringan_kantor_http_dengan_izin_diterima(self):
        vikunja.periksa_url("http://192.168.1.50:3456", True)

    def test_jaringan_kantor_tanpa_izin_ditolak(self):
        with self.assertRaises(vikunja.Gagal):
            vikunja.periksa_url("http://192.168.1.50:3456", False)


# ============================================================ 4. simpan-kunci & file token

class TesKunci(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "kunci.txt")

    def jalankan(self, argv, masukan=None, env=None):
        e = dict(os.environ)
        e.pop("VIKUNJA_TOKEN", None)
        e.pop("VIKUNJA_TOKEN_FILE", None)
        if env:
            e.update(env)
        return subprocess.run([PY, SKRIP] + argv, input=masukan, capture_output=True, text=True, env=e)

    def test_tolak_token_tanpa_prefiks(self):
        r = self.jalankan(["simpan-kunci", "--kunci-file", self.path], masukan="bukantoken\n")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("tk_", r.stderr)

    def test_simpan_dan_baca_kembali(self):
        r = self.jalankan(["simpan-kunci", "--kunci-file", self.path], masukan="tk_abc123\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(self.path) as f:
            self.assertEqual(f.read().strip(), "tk_abc123")
        mode = oct(os.stat(self.path).st_mode)[-3:]
        self.assertEqual(mode, "600")

    def test_tolak_timpa_tanpa_ya(self):
        self.jalankan(["simpan-kunci", "--kunci-file", self.path], masukan="tk_abc123\n")
        r = self.jalankan(["simpan-kunci", "--kunci-file", self.path], masukan="tk_lainlagi\n")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("sudah ada", r.stderr)
        with open(self.path) as f:
            self.assertEqual(f.read().strip(), "tk_abc123")

    def test_timpa_dengan_ya(self):
        self.jalankan(["simpan-kunci", "--kunci-file", self.path], masukan="tk_abc123\n")
        r = self.jalankan(["simpan-kunci", "--kunci-file", self.path, "--ya"], masukan="tk_baru456\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(self.path) as f:
            self.assertEqual(f.read().strip(), "tk_baru456")

    def test_token_tidak_pernah_dicetak(self):
        r = self.jalankan(["simpan-kunci", "--kunci-file", self.path], masukan="tk_rahasiasekali\n")
        self.assertNotIn("tk_rahasiasekali", r.stdout)
        self.assertNotIn("tk_rahasiasekali", r.stderr)

    def test_kunci_file_tidak_ada(self):
        r = self.jalankan(["cek", "--url", "http://127.0.0.1:1", "--kunci-file", "/tidak/ada/kunci.txt"])
        self.assertNotEqual(r.returncode, 0)


# ============================================================ 5. server tiruan + CLI ujung-ke-ujung

def _terapkan_filter(tugas, filt):
    """Tiruan SEDERHANA bahasa filter Vikunja, cukup untuk klausa yang dibuat vikunja.py sendiri:
    'done = false', 'due_date >= X', 'due_date < X', digabung dengan '&&'. due_date kosong
    (belum diisi, '0001-01-01...') dianggap NULL -> tidak pernah cocok pada perbandingan due_date
    (meniru semantik NULL SQL, sama seperti Vikunja asli)."""
    if not filt:
        return list(tugas)
    klausa = [k.strip() for k in filt.split("&&")]
    hasil = []
    for t in tugas:
        cocok = True
        for k in klausa:
            m = re.match(r"^(done|due_date)\s*(>=|<=|<|>|=)\s*(.+)$", k)
            if not m:
                continue
            field, op, nilai = m.group(1), m.group(2), m.group(3).strip()
            if field == "done":
                if (t["done"]) != (nilai == "true"):
                    cocok = False
            else:
                dd = t.get("due_date", "0001-01-01T00:00:00Z")
                if dd.startswith("0001-01-01"):
                    cocok = False
                elif op == "<" and not (dd < nilai):
                    cocok = False
                elif op == ">=" and not (dd >= nilai):
                    cocok = False
                elif op == "<=" and not (dd <= nilai):
                    cocok = False
                elif op == ">" and not (dd > nilai):
                    cocok = False
            if not cocok:
                break
        if cocok:
            hasil.append(t)
    return hasil


class Tiruan(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _kirim(self, kode, obj, headers=None):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(kode)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _token(self):
        h = self.headers.get("Authorization", "")
        return h[len("Bearer "):] if h.startswith("Bearer ") else None

    def _izin(self, grup, aksi):
        tok = self._token()
        S = self.server.keadaan
        if tok is None or tok not in S.token_izin:
            return False
        return aksi in S.token_izin[tok].get(grup, [])

    def _tolak(self):
        self._kirim(401, FIX["galat_401"])

    def do_GET(self):
        S = self.server.keadaan
        path, _, qs = self.path.partition("?")
        q = {k: v[0] for k, v in urllib.parse.parse_qs(qs).items()} if qs else {}
        if path == "/api/v1/info":
            return self._kirim(200, FIX["info"])
        if path == "/api/v1/tunda":  # simulasi timeout untuk uji koneksi
            time.sleep(2)
            return self._kirim(200, {})
        if path == "/api/v1/projects":
            if not self._izin("projects", "read_all"):
                return self._tolak()
            return self._kirim(200, S.proyek, {"X-Pagination-Total-Pages": "1"})
        if path.startswith("/api/v1/projects/") and path.endswith("/tasks"):
            if not self._izin("tasks", "read_all"):
                return self._tolak()
            pid = int(path.split("/")[4])
            data = _terapkan_filter([t for t in S.tugas if t["project_id"] == pid], q.get("filter", ""))
            return self._kirim(200, data, {"X-Pagination-Total-Pages": "1"})
        if path.startswith("/api/v1/projects/") and path.endswith("/projectusers"):
            if not self._izin("projects", "projectusers"):
                return self._tolak()
            s = q.get("s", "").lower()
            data = [u for u in S.pengguna if s in u["username"].lower()]
            return self._kirim(200, data)
        if path == "/api/v1/tasks":
            if not self._izin("tasks", "read_all"):
                return self._tolak()
            data = _terapkan_filter(S.tugas, q.get("filter", ""))
            s = q.get("s", "")
            if s:
                data = [t for t in data if s.lower() in t["title"].lower()]
            return self._kirim(200, data, {"X-Pagination-Total-Pages": "1"})
        if path.startswith("/api/v1/tasks/"):
            if not self._izin("tasks", "read_one"):
                return self._tolak()
            tid = int(path.rsplit("/", 1)[-1])
            for t in S.tugas:
                if t["id"] == tid:
                    return self._kirim(200, t)
            return self._kirim(404, FIX["galat_404_task"])
        self._kirim(404, {"message": "unknown route"})

    def do_PUT(self):
        S = self.server.keadaan
        panjang = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(panjang) or b"{}")
        path = self.path
        if path.startswith("/api/v1/projects/") and path.endswith("/tasks"):
            if not self._izin("tasks", "create"):
                return self._tolak()
            if "GALAT500" in body.get("title", ""):
                return self._kirim(500, {"message": "internal error tiruan"})
            if "TUNDATULIS" in body.get("title", ""):
                time.sleep(2)
                return self._kirim(200, {})
            pid = int(path.split("/")[4])
            S.penghitung += 1
            t = {"id": S.penghitung, "title": body["title"], "done": False,
                 "due_date": body.get("due_date", "0001-01-01T00:00:00Z"),
                 "priority": body.get("priority", 0), "project_id": pid, "assignees": []}
            S.tugas.append(t)
            return self._kirim(201, t)
        if path.startswith("/api/v1/tasks/") and path.endswith("/assignees"):
            if not self._izin("tasks_assignees", "create"):
                return self._tolak()
            tid = int(path.split("/")[4])
            for t in S.tugas:
                if t["id"] == tid:
                    t["assignees"].append({"id": body["user_id"], "username": "diketahui"})
                    return self._kirim(201, {"user_id": body["user_id"]})
            return self._kirim(404, FIX["galat_404_task"])
        self._kirim(404, {"message": "unknown route"})

    def do_POST(self):
        S = self.server.keadaan
        panjang = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(panjang) or b"{}")
        path = self.path
        if path.startswith("/api/v1/tasks/"):
            if not self._izin("tasks", "update"):
                return self._tolak()
            tid = int(path.rsplit("/", 1)[-1])
            for t in S.tugas:
                if t["id"] == tid:
                    if body.get("done"):
                        t["done"] = True
                        t["done_at"] = "2026-09-26T10:00:00Z"
                    return self._kirim(200, t)
            return self._kirim(404, FIX["galat_404_task"])
        self._kirim(404, {"message": "unknown route"})


class Keadaan:
    def __init__(self):
        self.reset()

    def reset(self):
        # Margin lebar (bukan pas 'besok'/'seminggu lalu') supaya uji tidak rapuh terhadap lamanya
        # proses berjalan (batas hari nyata bisa terlewati di tengah sesi uji yang panjang).
        hari_ini = dt.datetime.now(dt.timezone.utc).date()
        besok = vikunja.ke_iso_utc(hari_ini + dt.timedelta(days=3), 12, 0, "WIB")
        seminggu_lalu = vikunja.ke_iso_utc(hari_ini - dt.timedelta(days=10), 12, 0, "WIB")
        self.proyek = [dict(FIX["proyek_inbox"]), dict(FIX["proyek"])]
        self.tugas = [
            {"id": 1, "title": "Beli semen 50 sak", "done": False,
             "due_date": besok, "priority": 3, "project_id": 2, "assignees": []},
            {"id": 2, "title": "Tagih pelanggan telat", "done": False,
             "due_date": seminggu_lalu, "priority": 0, "project_id": 2,
             "assignees": [{"id": 1, "username": "budi"}]},
        ]
        self.pengguna = [{"id": 1, "username": "budi"}, {"id": 2, "username": "siti"}]
        self.penghitung = 2
        self.token_izin = {
            "tk_bacasajarahasia1": {"projects": ["read_all", "read_one"], "tasks": ["read_all", "read_one"]},
            "tk_tulisrahasia12345": {"projects": ["read_all", "read_one", "projectusers"],
                                     "tasks": ["read_all", "read_one", "create", "update"],
                                     "tasks_assignees": ["create", "read_all"]},
            # Temuan Akun B (2026-09-26): token dengan Tasks lengkap TAPI TANPA kelompok
            # 'tasks_assignees' -> penugasan (--ke) harus gagal dengan pesan yang menyebut
            # kelompok itu secara eksplisit, bukan pesan 401 generik.
            "tk_tanpaassignees1234": {"projects": ["read_all", "read_one", "projectusers"],
                                       "tasks": ["read_all", "read_one", "create", "update"]},
        }


class TesUjungKeUjung(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Tiruan)
        cls.srv.keadaan = Keadaan()
        cls.port = cls.srv.server_address[1]
        cls.url = f"http://127.0.0.1:{cls.port}"
        cls.t = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.t.start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        self.srv.keadaan.reset()

    def jalankan(self, argv, token="tk_tulisrahasia12345", tambahan_env=None):
        env = dict(os.environ)
        env["VIKUNJA_URL"] = self.url
        env["VIKUNJA_TOKEN"] = token
        if tambahan_env:
            env.update(tambahan_env)
        return subprocess.run([PY, SKRIP] + argv, capture_output=True, text=True, env=env, timeout=10)

    def test_cek_berhasil(self):
        r = self.jalankan(["cek"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("v2.6.0", r.stdout)
        self.assertIn("tk_tul****2345", r.stdout)  # token tersamar, bukan token asli
        self.assertNotIn("tk_tulisrahasia12345", r.stdout)

    def test_cek_token_salah(self):
        r = self.jalankan(["cek"], token="tk_ngasalsekaliinipanjang")
        self.assertNotEqual(r.returncode, 0)

    def test_daftar_proyek(self):
        r = self.jalankan(["daftar-proyek"])
        self.assertIn("Toko Bangunan Sinar Jaya", r.stdout)
        self.assertIn("Inbox", r.stdout)

    def test_terlambat(self):
        r = self.jalankan(["terlambat"])
        self.assertIn("Tagih pelanggan telat", r.stdout)
        self.assertNotIn("Beli semen", r.stdout)  # itu due besok siang, bukan terlambat

    def test_hari_ini_kosong_jika_bukan_hari_ini(self):
        # fixture due_date pakai tanggal tetap; di lingkungan uji nyata tanggal berbeda -> boleh kosong
        r = self.jalankan(["hari-ini"])
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_tambah_pratinjau_tidak_menulis(self):
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "Tugas uji"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Belum disimpan", r.stdout)
        self.assertEqual(len(self.srv.keadaan.tugas), 2)  # tidak bertambah

    def test_tambah_ya_menulis(self):
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "Tugas uji", "--ya"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("TERSIMPAN", r.stdout)
        self.assertEqual(len(self.srv.keadaan.tugas), 3)

    def test_tambah_token_baca_saja_ditolak(self):
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "Tugas uji", "--ya"], token="tk_bacasajarahasia1")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("401", r.stderr)
        self.assertEqual(len(self.srv.keadaan.tugas), 2)

    def test_tambah_proyek_tidak_ditemukan(self):
        r = self.jalankan(["tambah", "--proyek", "TidakAda", "--judul", "x"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("tidak ditemukan", r.stderr)

    def test_tambah_dengan_ke_berhasil_assign(self):
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "Tugas ditugaskan", "--ke", "budi", "--ya"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(any(t["assignees"] for t in self.srv.keadaan.tugas if t["title"] == "Tugas ditugaskan"))

    def test_tambah_ke_tidak_ditemukan_tugas_tetap_tersimpan(self):
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "Tugas x", "--ke", "entahsiapa", "--ya"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("GAGAL menugaskan", r.stderr)
        self.assertTrue(any(t["title"] == "Tugas x" for t in self.srv.keadaan.tugas))

    def test_tambah_ke_tanpa_izin_tasks_assignees_pesan_jelas(self):
        # Regresi Temuan #1 Akun B: token punya Tasks lengkap tapi tidak dicentang kelompok
        # terpisah 'Tasks Assignees' -> Vikunja balas 401 ("token tidak valid", bukan 403).
        # Tugas tetap tersimpan; pesan galat harus menyebut 'Tasks Assignees' secara eksplisit
        # supaya pengguna tidak salah kira token/username-nya yang salah.
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "Tugas tanpa izin assign", "--ke", "budi", "--ya"],
                           token="tk_tanpaassignees1234")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("GAGAL menugaskan", r.stderr)
        self.assertIn("Tasks Assignees", r.stderr)
        self.assertTrue(any(t["title"] == "Tugas tanpa izin assign" for t in self.srv.keadaan.tugas))
        self.assertFalse(any(t["assignees"] for t in self.srv.keadaan.tugas
                              if t["title"] == "Tugas tanpa izin assign"))

    def test_hari_ini_dan_terlambat_menyebut_catatan_tumpang_tindih(self):
        # Regresi Temuan #2 Akun B: dokumentasikan (bukan sembunyikan) bahwa tugas due hari ini
        # yang jamnya sudah lewat bisa muncul di hari-ini MAUPUN terlambat sekaligus.
        r1 = self.jalankan(["hari-ini"])
        self.assertEqual(r1.returncode, 0, r1.stderr)
        self.assertIn("MAUPUN", r1.stdout)
        r2 = self.jalankan(["terlambat"])
        self.assertEqual(r2.returncode, 0, r2.stderr)
        self.assertIn("MAUPUN", r2.stdout)

    def test_selesai_menandai(self):
        r = self.jalankan(["selesai", "--id", "1", "--ya"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(self.srv.keadaan.tugas[0]["done"])

    def test_selesai_sudah_selesai(self):
        self.srv.keadaan.tugas[0]["done"] = True
        r = self.jalankan(["selesai", "--id", "1"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("sudah SELESAI", r.stdout)

    def test_selesai_id_tidak_ada(self):
        r = self.jalankan(["selesai", "--id", "999", "--ya"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("404", r.stderr)

    def test_ringkasan_kelompok_per_anggota(self):
        r = self.jalankan(["ringkasan"])
        self.assertIn("budi (1 tugas)", r.stdout)
        self.assertIn("BELUM ADA PIC", r.stdout)

    def test_cari(self):
        r = self.jalankan(["cari", "semen"])
        self.assertIn("Beli semen 50 sak", r.stdout)

    def test_galat_500_saat_tulis_kode_8(self):
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "GALAT500", "--ya"])
        self.assertEqual(r.returncode, vikunja.K_TAKPASTI)
        self.assertIn("MUNGKIN sudah masuk sebagian", r.stderr)

    def test_timeout_saat_tulis_kode_8(self):
        # server tiruan menunda 2 detik; --timeout 0.5 harus memicu timeout urllib yang ditangani
        # sebagai 'TAKPASTI' (mungkin sudah tersimpan sebagian), bukan crash tak tertangani.
        r = self.jalankan(["tambah", "--proyek", "2", "--judul", "TUNDATULIS", "--ya", "--timeout", "0.5"])
        self.assertEqual(r.returncode, vikunja.K_TAKPASTI, r.stderr)
        self.assertIn("timeout", r.stderr.lower())

    def test_opsi_timeout_tidak_mengganggu_permintaan_cepat(self):
        r = self.jalankan(["daftar-proyek", "--timeout", "5"])
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_json_output(self):
        r = self.jalankan(["daftar-proyek", "--json"])
        data = json.loads(r.stdout)
        self.assertEqual(len(data["proyek"]), 2)

    def test_batch_tambah(self):
        batch = [
            {"judul": "Batch 1", "proyek": "2"},
            {"judul": "Batch 2", "proyek": "2", "tenggat": "besok"},
        ]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(batch, f)
            path = f.name
        try:
            r = self.jalankan(["tambah", "--batch", path, "--ya"])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("TERSIMPAN 2 TUGAS", r.stdout)
        finally:
            os.unlink(path)

    def test_batch_kosong_ditolak(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump([], f)
            path = f.name
        try:
            r = self.jalankan(["tambah", "--batch", path, "--ya"])
            self.assertNotEqual(r.returncode, 0)
        finally:
            os.unlink(path)

    def test_dari_teks_tidak_memanggil_jaringan(self):
        # sengaja pakai VIKUNJA_URL yang tidak ada servernya -> harus tetap sukses (tidak konek)
        env = dict(os.environ)
        env["VIKUNJA_URL"] = "http://127.0.0.1:1"
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run(
                [PY, SKRIP, "dari-teks", "--teks", "- Budi: telepon supplier", "--keluaran",
                 os.path.join(d, "draf.json")],
                capture_output=True, text=True, env=env, timeout=10, cwd=d,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(os.path.join(d, "draf.json")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
