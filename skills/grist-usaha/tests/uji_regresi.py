#!/usr/bin/env python3
"""Uji regresi grist.py.

Dua cara uji, sesuai dua cara kerja skill (lihat docstring scripts/grist.py):

1. **Baca file .grist (SQLite) read-only** — diuji dengan file TIRUAN yang skemanya disusun
   sama persis dengan kode sumber resmi grist-core v1.7.19 (lihat tests/fixtures/buat_fixture.py
   untuk rincian & sumbernya), termasuk file RUSAK dan file SQLite tanpa metadata Grist.
2. **REST API** — diuji dengan server HTTP TIRUAN (`http.server` standar) yang meniru bentuk
   respons `/api/orgs`, `/api/orgs/:oid/workspaces`, `/api/docs/:docId/tables`, dan
   `/api/docs/:docId/tables/:tableId/records` PERSIS seperti dibaca dari
   `app/gen-server/ApiServer.ts` & `app/server/lib/DocApi.ts` resmi (lihat
   research/sources/grist-2026-09-26.md). **Belum diuji terhadap server Grist yang sungguhan
   menyala** — dicatat apa adanya di README.md skill ini.

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
Tidak butuh internet, Grist, Docker, atau paket tambahan (hanya pustaka standar Python 3.8+).
"""
import csv
import json
import os
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP_DIR = os.path.join(SINI, "..", "scripts")
SKRIP = os.path.join(SKRIP_DIR, "grist.py")
sys.path.insert(0, SKRIP_DIR)
sys.path.insert(0, os.path.join(SINI, "fixtures"))
import grist  # noqa: E402  (import setelah sys.path diatur - modul skill yang diuji)
import buat_fixture  # noqa: E402

KUNCI_UJI = "kunciuji-abcdef0123456789"


# ============================================================================
# 1. Fungsi murni (dipanggil langsung, tanpa subprocess - cepat & presisi)
# ============================================================================

class TestBersihkanAngka(unittest.TestCase):
    def cek(self, teks, harap):
        hasil = grist._bersihkan_angka(teks)
        if harap is None:
            self.assertIsNone(hasil, f"{teks!r} seharusnya BUKAN angka")
        else:
            self.assertAlmostEqual(hasil, harap, msg=f"{teks!r}")

    def test_format_rupiah_ribuan_titik_desimal_koma(self):
        self.cek("Rp 1.234.567,89", 1234567.89)
        self.cek("1.234.567,89", 1234567.89)

    def test_format_polos_titik_desimal(self):
        self.cek("1234567.89", 1234567.89)
        self.cek("12500.5", 12500.5)

    def test_ribuan_titik_tanpa_desimal(self):
        self.cek("1.234.567", 1234567)
        self.cek("1.234", 1234)

    def test_koma_sebagai_desimal_pendek(self):
        self.cek("32,5", 32.5)
        self.cek("100,00", 100.0)

    def test_koma_sebagai_ribuan_panjang(self):
        self.cek("1,234", 1234)

    def test_bukan_angka(self):
        self.cek("Kopi Robusta", None)
        self.cek("", None)
        self.cek("08123456789 (WA)", None)

    def test_rp_dengan_spasi_dan_titik(self):
        self.cek("Rp. 50.000", 50000)


class TestBersihkanHeader(unittest.TestCase):
    def test_spasi_jadi_camelcase(self):
        self.assertEqual(grist._bersihkan_header("Nama Pelanggan"), "NamaPelanggan")

    def test_karakter_aneh_dibuang(self):
        self.assertEqual(grist._bersihkan_header("Harga (Rp)"), "HargaRp")
        self.assertEqual(grist._bersihkan_header("No. HP/WA"), "NoHpWa")

    def test_diakritik_dilucuti(self):
        self.assertEqual(grist._bersihkan_header("Nomor Rési"), "NomorResi")

    def test_kosong_jadi_kolom(self):
        self.assertEqual(grist._bersihkan_header("   "), "Kolom")

    def test_diawali_angka_diberi_awalan_k(self):
        self.assertEqual(grist._bersihkan_header("2025 Target"), "K2025Target")


class TestMasker(unittest.TestCase):
    def test_hanya_4_terakhir_tampil(self):
        self.assertEqual(grist.masker("abcdefgh1234"), "********1234")

    def test_kunci_kosong(self):
        self.assertEqual(grist.masker(""), "(kosong)")

    def test_tidak_pernah_ada_kunci_utuh_di_kode_uji_ini(self):
        # Jaga-jaga: pastikan fungsi tidak pernah mengembalikan string yang sama persis dengan input.
        k = "kuncirahasiasangat-panjang-sekali"
        self.assertNotEqual(grist.masker(k), k)


class TestAlamatServer(unittest.TestCase):
    def setUp(self):
        os.environ.pop("GRIST_ALLOW_REMOTE", None)

    def test_default_localhost(self):
        self.assertEqual(grist.ambil_base_url(None), "http://localhost:8484")

    def test_localhost_eksplisit_ok(self):
        self.assertEqual(grist.ambil_base_url("http://127.0.0.1:9999"), "http://127.0.0.1:9999")

    def test_alamat_luar_tanpa_izin_ditolak(self):
        with self.assertRaises(grist.Gagal):
            grist.ambil_base_url("http://grist.contoh-kantor.com")

    def test_alamat_internet_izin_tanpa_https_ditolak(self):
        os.environ["GRIST_ALLOW_REMOTE"] = "1"
        with self.assertRaises(grist.Gagal):
            grist.ambil_base_url("http://grist.contoh-kantor.com")

    def test_alamat_internet_izin_dengan_https_diterima(self):
        os.environ["GRIST_ALLOW_REMOTE"] = "1"
        self.assertEqual(grist.ambil_base_url("https://grist.contoh-kantor.com"),
                          "https://grist.contoh-kantor.com")

    def test_alamat_lan_izin_tanpa_https_diterima(self):
        os.environ["GRIST_ALLOW_REMOTE"] = "1"
        self.assertEqual(grist.ambil_base_url("http://192.168.1.50:8484"), "http://192.168.1.50:8484")

    def tearDown(self):
        os.environ.pop("GRIST_ALLOW_REMOTE", None)


class TestCariDokumen(unittest.TestCase):
    """cari_dokumen() dipanggil langsung dengan panggil_grist DITEMPEL (monkeypatch) supaya
    tidak butuh server sungguhan untuk menguji logika pencocokan nama."""

    DAFTAR_ORG = [{"id": 1, "name": "Personal", "domain": "docs"}]
    DAFTAR_WS = [{"id": 10, "name": "Home", "docs": [
        {"id": "docABC123", "name": "Data Usaha Saya"},
        {"id": "docXYZ789", "name": "Data Usaha Cabang"},
    ]}]

    def setUp(self):
        self._asli = grist.panggil_grist

        def tiruan(base_url, kunci, path, method="GET", body=None, timeout=30):
            if path == "/api/orgs":
                return self.DAFTAR_ORG
            if path == "/api/orgs/1/workspaces":
                return self.DAFTAR_WS
            raise AssertionError(f"path tak terduga: {path}")

        grist.panggil_grist = tiruan

    def tearDown(self):
        grist.panggil_grist = self._asli

    def test_docid_persis(self):
        self.assertEqual(grist.cari_dokumen("http://x", "k", "docABC123"), "docABC123")

    def test_nama_persis_cocok_satu(self):
        self.assertEqual(grist.cari_dokumen("http://x", "k", "Data Usaha Saya"), "docABC123")

    def test_nama_sebagian_ambigu(self):
        with self.assertRaises(grist.Gagal) as c:
            grist.cari_dokumen("http://x", "k", "usaha")
        self.assertIn("Ada 2 dokumen", str(c.exception))

    def test_nama_tidak_ketemu(self):
        with self.assertRaises(grist.Gagal) as c:
            grist.cari_dokumen("http://x", "k", "tidak ada begini")
        self.assertIn("tidak ditemukan", str(c.exception))


# ============================================================================
# 2. Baca file .grist (SQLite) read-only — file TIRUAN & file RUSAK
# ============================================================================

class TestBacaSqlite(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.doc = buat_fixture.buat_dokumen_contoh(Path(self.tmp.name) / "contoh.grist")

    def tearDown(self):
        self.tmp.cleanup()

    def jalan(self, *args):
        return subprocess.run([sys.executable, SKRIP, *args], capture_output=True, text=True)

    def test_daftar_tabel(self):
        p = self.jalan("daftar-tabel", str(self.doc), "--json")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("Pelanggan", p.stdout)
        self.assertIn("Stok", p.stdout)
        baris_json = [l for l in p.stdout.splitlines() if l.startswith("[")][0]
        data = json.loads(baris_json)
        self.assertEqual({d["tabel"] for d in data}, {"Pelanggan", "Stok"})

    def test_ringkasan_pelanggan(self):
        p = self.jalan("ringkasan", str(self.doc), "Pelanggan", "--json")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        baris_json = [l for l in p.stdout.splitlines() if l.startswith("{")][0]
        data = json.loads(baris_json)
        self.assertEqual(data["jumlah_baris"], 3)
        kolom_rumus = [c["id"] for c in data["kolom"] if c["rumus"]]
        self.assertEqual(kolom_rumus, ["TeleponRapi"])
        self.assertIn("Toko Maju Jaya", [b["Nama"] for b in data["contoh"]])

    def test_ringkasan_stok_status_menipis_dan_habis(self):
        p = self.jalan("ringkasan", str(self.doc), "Stok", "--json")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        baris_json = [l for l in p.stdout.splitlines() if l.startswith("{")][0]
        data = json.loads(baris_json)
        status = {b["Nama"]: b["Status"] for b in data["contoh"]}
        self.assertEqual(status["Gula Aren 1kg"], "MENIPIS")
        self.assertEqual(status["Cup Kertas 12oz"], "HABIS")
        self.assertEqual(status["Kopi Robusta 1kg"], "AMAN")

    def test_ekspor_csv(self):
        keluaran = Path(self.tmp.name) / "pelanggan.csv"
        p = self.jalan("ekspor-csv", str(self.doc), "Pelanggan", "--keluaran", str(keluaran))
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with keluaran.open(encoding="utf-8") as f:
            baris = list(csv.DictReader(f))
        self.assertEqual(len(baris), 3)
        self.assertEqual(baris[0]["Nama"], "Toko Maju Jaya")
        self.assertEqual(baris[1]["TeleponRapi"], "6281311112222")

    def test_tabel_tidak_ada(self):
        p = self.jalan("ringkasan", str(self.doc), "TidakAda")
        self.assertEqual(p.returncode, 2)
        self.assertIn("tidak ada", p.stdout + p.stderr)
        self.assertIn("Pelanggan", p.stdout + p.stderr)  # menyebut tabel yang memang ada

    def test_file_tidak_ditemukan(self):
        p = self.jalan("daftar-tabel", str(Path(self.tmp.name) / "tidak-ada.grist"))
        self.assertEqual(p.returncode, 2)
        self.assertIn("tidak ditemukan", p.stdout + p.stderr)

    def test_file_rusak_bukan_sqlite(self):
        rusak = buat_fixture.buat_file_rusak(Path(self.tmp.name) / "rusak.grist")
        p = self.jalan("daftar-tabel", str(rusak))
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("tidak bisa dibuka", p.stdout + p.stderr)

    def test_file_sqlite_tanpa_metadata_grist(self):
        aneh = buat_fixture.buat_file_sqlite_tanpa_metadata_grist(Path(self.tmp.name) / "bukan-grist.grist")
        p = self.jalan("daftar-tabel", str(aneh))
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("_grist_Tables", p.stdout + p.stderr)

    def test_file_kosong(self):
        kosong = Path(self.tmp.name) / "kosong.grist"
        kosong.write_bytes(b"")
        p = self.jalan("daftar-tabel", str(kosong))
        self.assertNotEqual(p.returncode, 0)

    def test_benar_benar_read_only_tidak_menulis(self):
        ukuran_sebelum = self.doc.stat().st_size
        self.jalan("ringkasan", str(self.doc), "Pelanggan")
        self.jalan("ekspor-csv", str(self.doc), "Stok", "--keluaran", str(Path(self.tmp.name) / "x.csv"))
        self.assertEqual(self.doc.stat().st_size, ukuran_sebelum, "file .grist berubah ukuran - seharusnya read-only")
        # Coba tulis langsung lewat fungsi internal skill: harus DITOLAK oleh PRAGMA query_only.
        con = grist._buka_ro(self.doc)
        try:
            with self.assertRaises(Exception):
                con.execute('INSERT INTO "Pelanggan" (Nama) VALUES (?)', ("Harus gagal",))
        finally:
            con.close()


# ============================================================================
# 3. REST API lewat server Grist TIRUAN (belum diuji ke server Grist sungguhan)
# ============================================================================

class ServerGristTiruan(BaseHTTPRequestHandler):
    orgs = [{"id": 1, "name": "Personal", "domain": "docs"}]
    docs = {"docABC123": {"nama": "Data Usaha Saya"}}
    tabel = {}   # docId -> {tableId: [colId, ...]}
    records = {}  # (docId, tableId) -> list of fields dict

    def _kirim(self, kode, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(kode)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _sah(self):
        auth = self.headers.get("Authorization", "")
        if auth != f"Bearer {KUNCI_UJI}":
            self._kirim(401, {"error": "Bad request: no access key"})
            return False
        return True

    def log_message(self, *a):  # bungkam log server tiruan
        pass

    def do_GET(self):
        if not self._sah():
            return
        u = urllib.parse.urlparse(self.path)
        if u.path == "/api/orgs":
            return self._kirim(200, self.orgs)
        if u.path == "/api/orgs/1/workspaces":
            docs = [{"id": did, "name": d["nama"]} for did, d in self.docs.items()]
            return self._kirim(200, [{"id": 10, "name": "Home", "docs": docs}])
        self._kirim(404, {"error": "not found"})

    def do_POST(self):
        if not self._sah():
            return
        panjang = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(panjang) or b"{}")
        u = urllib.parse.urlparse(self.path)
        bagian = u.path.strip("/").split("/")
        # /api/docs/<docId>/tables
        if len(bagian) == 4 and bagian[:3] == ["api", "docs", bagian[2]] and bagian[3] == "tables":
            doc_id = bagian[2]
            if doc_id not in self.docs:
                return self._kirim(404, {"error": f"document not found: {doc_id}"})
            hasil = []
            for t in body.get("tables", []):
                tid = t["id"]
                self.tabel.setdefault(doc_id, {})[tid] = [c["id"] for c in t.get("columns", [])]
                self.records[(doc_id, tid)] = []
                hasil.append({"id": tid})
            return self._kirim(200, {"tables": hasil})
        # /api/docs/<docId>/tables/<tableId>/records
        if len(bagian) == 6 and bagian[:3] == ["api", "docs", bagian[2]] and bagian[3] == "tables" and bagian[5] == "records":
            doc_id, table_id = bagian[2], bagian[4]
            if doc_id not in self.docs:
                return self._kirim(404, {"error": f"document not found: {doc_id}"})
            if table_id not in self.tabel.get(doc_id, {}):
                return self._kirim(404, {"error": f"table not found: {table_id}"})
            recs = self.records[(doc_id, table_id)]
            hasil = []
            for r in body.get("records", []):
                rid = len(recs) + 1
                recs.append(r["fields"])
                hasil.append({"id": rid, "fields": r["fields"]})
            return self._kirim(200, {"records": hasil})
        self._kirim(404, {"error": "not found"})


class TestApiServerTiruan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), ServerGristTiruan)
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=5)

    def setUp(self):
        ServerGristTiruan.tabel = {}
        ServerGristTiruan.records = {}
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.home.mkdir()
        kunci_dir = self.home / ".komunitech"
        kunci_dir.mkdir()
        (kunci_dir / "grist-kunci.txt").write_text(KUNCI_UJI + "\n", encoding="utf-8")
        os.chmod(kunci_dir / "grist-kunci.txt", 0o600)

    def tearDown(self):
        self.tmp.cleanup()

    def jalan(self, *args):
        env = os.environ.copy()
        env["HOME"] = str(self.home)
        env["GRIST_URL"] = self.base_url
        env.pop("GRIST_API_KEY", None)
        env.pop("GRIST_API_KEY_FILE", None)
        return subprocess.run([sys.executable, SKRIP, *args], capture_output=True, text=True, env=env)

    def test_cek_daftar_dokumen(self):
        p = self.jalan("cek")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("Data Usaha Saya", p.stdout)
        self.assertIn("docABC123", p.stdout)
        self.assertNotIn(KUNCI_UJI, p.stdout)  # kunci tidak boleh tercetak utuh

    def test_cek_kunci_salah(self):
        (self.home / ".komunitech" / "grist-kunci.txt").write_text("kunci-salah-sekali\n", encoding="utf-8")
        os.chmod(self.home / ".komunitech" / "grist-kunci.txt", 0o600)
        p = self.jalan("cek")
        self.assertEqual(p.returncode, 5, p.stdout + p.stderr)  # 401 -> kode 5 (lihat tabel error SKILL.md)
        self.assertIn("401", p.stdout + p.stderr)
        self.assertNotIn("Data Usaha Saya", p.stdout)
        self.assertNotIn("kunci-salah-sekali", p.stdout + p.stderr)

    def test_buat_tabel_pratinjau_tanpa_ya(self):
        p = self.jalan("buat-tabel", "pelanggan", "--dokumen", "Data Usaha Saya")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("PRATINJAU", p.stdout)
        self.assertIn("Belum dibuat", p.stdout)
        self.assertEqual(ServerGristTiruan.tabel, {})  # belum benar-benar memanggil API tulis

    def test_buat_tabel_dengan_ya(self):
        p = self.jalan("buat-tabel", "stok", "--dokumen", "docABC123", "--ya")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("BERHASIL", p.stdout)
        self.assertIn("Stok", ServerGristTiruan.tabel.get("docABC123", {}))

    def test_impor_csv_pratinjau_dan_ya(self):
        csv_path = Path(self.tmp.name) / "pelanggan.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Nama", "Kota"])
            w.writerow(["Toko Baru", "Solo"])
            w.writerow(["Toko Lama", "Semarang"])
        # Tabel harus sudah ada dulu (dibuat lewat API tiruan langsung, meniru 'sudah dibuat sebelumnya').
        ServerGristTiruan.tabel["docABC123"] = {"Pelanggan": ["Nama", "Kota"]}
        ServerGristTiruan.records[("docABC123", "Pelanggan")] = []

        p = self.jalan("impor-csv", str(csv_path), "--dokumen", "docABC123", "--tabel", "Pelanggan")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("PRATINJAU", p.stdout)
        self.assertEqual(ServerGristTiruan.records[("docABC123", "Pelanggan")], [])

        p = self.jalan("impor-csv", str(csv_path), "--dokumen", "docABC123", "--tabel", "Pelanggan", "--ya")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("BERHASIL: 2 baris", p.stdout)
        self.assertEqual(len(ServerGristTiruan.records[("docABC123", "Pelanggan")]), 2)

    def test_impor_csv_nama_kolom_tidak_sah_ditolak_sebelum_kirim(self):
        csv_path = Path(self.tmp.name) / "buruk.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Nama Pelanggan", "Kota"])  # ada spasi - tidak sah untuk Grist
            w.writerow(["Toko Baru", "Solo"])
        p = self.jalan("impor-csv", str(csv_path), "--dokumen", "docABC123", "--tabel", "Pelanggan", "--ya")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("bersihkan-csv", p.stdout + p.stderr)

    def test_dokumen_tidak_ditemukan(self):
        p = self.jalan("buat-tabel", "pelanggan", "--dokumen", "Tidak Ada Sama Sekali", "--ya")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("tidak ditemukan", p.stdout + p.stderr)


# ============================================================================
# 4. simpan-kunci: izin file & penolakan menimpa
# ============================================================================

class TestSimpanKunci(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def jalan(self, teks_kunci, *args):
        env = os.environ.copy()
        env["HOME"] = self.tmp.name
        p = subprocess.run([sys.executable, SKRIP, "simpan-kunci", *args],
                            input=teks_kunci, capture_output=True, text=True, env=env)
        return p

    def test_simpan_baru(self):
        p = self.jalan("kunciasliku-1234\n")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        f = Path(self.tmp.name) / ".komunitech" / "grist-kunci.txt"
        self.assertTrue(f.is_file())
        self.assertEqual(f.read_text(encoding="utf-8").strip(), "kunciasliku-1234")
        izin = stat.S_IMODE(f.stat().st_mode)
        self.assertEqual(izin, 0o600)
        self.assertNotIn("kunciasliku-1234", p.stdout)  # tidak dicetak utuh

    def test_tolak_menimpa_tanpa_ya(self):
        self.jalan("kunci-lama-1\n")
        p = self.jalan("kunci-baru-2\n")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("sudah ada", p.stdout + p.stderr)
        f = Path(self.tmp.name) / ".komunitech" / "grist-kunci.txt"
        self.assertEqual(f.read_text(encoding="utf-8").strip(), "kunci-lama-1")

    def test_timpa_dengan_ya(self):
        self.jalan("kunci-lama-1\n")
        p = self.jalan("kunci-baru-2\n", "--ya")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        f = Path(self.tmp.name) / ".komunitech" / "grist-kunci.txt"
        self.assertEqual(f.read_text(encoding="utf-8").strip(), "kunci-baru-2")

    def test_kunci_kosong_ditolak(self):
        p = self.jalan("\n")
        self.assertNotEqual(p.returncode, 0)

    def test_izin_file_longgar_ditolak_saat_dipakai(self):
        self.jalan("kunciasliku-1234\n")
        f = Path(self.tmp.name) / ".komunitech" / "grist-kunci.txt"
        os.chmod(f, 0o644)
        env = os.environ.copy()
        env["HOME"] = self.tmp.name
        p = subprocess.run([sys.executable, SKRIP, "daftar-tabel", "/tmp/tidak-relevan.grist"],
                            capture_output=True, text=True, env=env)
        # daftar-tabel tidak butuh kunci sama sekali, jadi harus tetap gagal karena FILE .grist,
        # bukan karena kunci. Uji izin longgar dilakukan lewat 'cek' yang memang membaca kunci.
        p2 = subprocess.run([sys.executable, SKRIP, "cek", "--url", "http://127.0.0.1:1"],
                             capture_output=True, text=True, env=env)
        self.assertIn("izin", (p2.stdout + p2.stderr).lower())


# ============================================================================
# 5. Statis: tidak ada pola berbahaya di dalam script
# ============================================================================

class TestStatis(unittest.TestCase):
    def test_tidak_ada_perintah_berbahaya(self):
        with open(SKRIP, encoding="utf-8") as f:
            src = f.read()
        for pola in ("os.system(", "subprocess.", "eval(", "exec(", "curl ", "rm -rf"):
            self.assertNotIn(pola, src, f"pola berbahaya ditemukan: {pola!r}")
        self.assertNotRegex(src, r"^\s*(import|from)\s+(requests|httpx|urllib3)\b", "hanya pustaka standar")

    def test_bantuan_dan_tanpa_argumen(self):
        p = subprocess.run([sys.executable, SKRIP, "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        p = subprocess.run([sys.executable, SKRIP], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)

    def test_pola_daftar_dan_tampilkan(self):
        p = subprocess.run([sys.executable, SKRIP, "pola", "daftar"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        for nama in ("pelanggan", "pesanan", "stok", "jadwal-konten"):
            self.assertIn(nama, p.stdout)
        p = subprocess.run([sys.executable, SKRIP, "pola", "tampilkan", "stok"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("rumus_sisa_stok", p.stdout)
        p = subprocess.run([sys.executable, SKRIP, "pola", "tampilkan", "tidak-ada"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)  # argparse choices


if __name__ == "__main__":
    unittest.main(verbosity=1)
