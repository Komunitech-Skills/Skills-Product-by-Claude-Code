#!/usr/bin/env python3
"""Uji regresi inventree.py memakai server InvenTree TIRUAN (http.server standar).

Jawaban server tiruan diputar ulang dari tests/fixtures/inventree-1.5.6.json, yang DIREKAM dari
InvenTree 1.5.6 (API 530) ASLI yang dijalankan Komunitech di 127.0.0.1 dengan data fiktif
(lihat examples/uji-pembuat/). Kunci rekaman = 'METODE path?query' persis seperti dikirim script,
per akun: 'baca' (grup Agen Baca), 'gudang' (grup Agen Gudang), 'lain' (tanpa/ salah token).

Sebagian uji memanggil fungsi Python langsung (angka Indonesia, URL, CSV, lembar opname) dan
sebagian menjalankan inventree.py sebagai proses terpisah lewat server tiruan (argparse + HTTP).
Tidak butuh internet atau InvenTree sungguhan. Angka penting dihitung ulang secara independen
dari data rekaman (bukan disalin dari keluaran script).

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
"""
import csv
import importlib.util
import io
import json
import math
import os
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP = os.path.join(SINI, "..", "scripts", "inventree.py")
FIX = json.load(open(os.path.join(SINI, "fixtures", "inventree-1.5.6.json"), encoding="utf-8"))["rekaman"]
PY = sys.executable

spec = importlib.util.spec_from_file_location("inventree_mod", SKRIP)
inv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inv)

TOKEN_BACA = "inv-ujibaca0000000000000000000000000000000000-20270929"
TOKEN_GUDANG = "inv-ujigudang00000000000000000000000000000000-20270929"
PERAN = {TOKEN_BACA: "baca", TOKEN_GUDANG: "gudang"}


# ============================================================ server tiruan

class Tiruan:
    def __init__(self):
        self.diterima = []      # (metode, path, peran, body)
        self.timpa = {}         # key -> (status, body) untuk semua peran
        self.tunda = {}         # key -> detik
        self.bukan_inventree = False


def buat_handler(t):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _jawab(self, status, body, header=None):
            raw = json.dumps(body).encode("utf-8")
            self.send_response(status)
            for k, v in (header or {}).items():
                self.send_header(k, v)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            try:
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass  # klien sudah menyerah (uji timeout)

        def _layani(self):
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n)) if n else None
            auth = self.headers.get("Authorization") or ""
            token = auth[6:] if auth.startswith("Token ") else ""
            peran = PERAN.get(token, "lain")
            key = f"{self.command} {self.path}"
            t.diterima.append((self.command, self.path, peran, body))
            if key in t.tunda:
                time.sleep(t.tunda[key])
            if t.bukan_inventree:
                return self._jawab(200, {"halo": "bukan inventree"})
            if key in t.timpa:
                return self._jawab(*t.timpa[key])
            if self.path.startswith("/api/part/?search=banyak"):
                return self._halaman_banyak()
            if token and peran == "lain" and self.path != "/api/":
                return self._jawab(401, {"detail": "Invalid token."})
            rek = FIX.get(key, {})
            r = rek.get(peran) or (rek.get("lain") if self.path == "/api/" else None)
            if r is None:
                return self._jawab(404, {"detail": "Tidak ada di rekaman tiruan: " + key})
            return self._jawab(r["status"], r["body"])

        def _halaman_banyak(self):
            import urllib.parse
            q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.path).query))
            off, lim = int(q["offset"]), int(q["limit"])
            semua = [{"pk": i, "name": f"Baut M{i}", "IPN": f"BT-{i:03d}", "category_name": "Baut", "units": "",
                      "total_in_stock": i, "minimum_stock": 0} for i in range(1, 151)]
            return self._jawab(200, {"count": 150, "next": None, "previous": None, "results": semua[off:off + lim]})

        do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = _layani
    return H


class DasarServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = Tiruan()
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), buat_handler(cls.t))
        cls.url = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.tmp = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        self.t.diterima.clear()
        self.t.timpa.clear()
        self.t.tunda.clear()
        self.t.bukan_inventree = False

    def jalan(self, *argv, token=TOKEN_BACA, env_tambah=None, cwd=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith("INVENTREE_")
               and k.lower() not in ("http_proxy", "https_proxy", "all_proxy", "no_proxy")}
        env["HOME"] = self.tmp
        env["USERPROFILE"] = self.tmp
        env["INVENTREE_API_HOST"] = self.url
        if token:
            env["INVENTREE_API_TOKEN"] = token
        env.update(env_tambah or {})
        p = subprocess.run([PY, SKRIP] + list(argv), capture_output=True, text=True, env=env,
                           cwd=cwd or self.tmp, timeout=60)
        return p.returncode, p.stdout, p.stderr

    def tulis(self):
        return [d for d in self.t.diterima if d[0] != "GET"]


# ============================================================ 1. angka gaya Indonesia

class TesAngka(unittest.TestCase):
    def test_baca_angka(self):
        kasus = {"12,5": "12.5", "1.200": "1200", "1.200,5": "1200.5", "1,200.5": "1200.5", "12.5": "12.5",
                 "1.5": "1.5", "1200": "1200", " 57 ": "57", "0,05": "0.05", "1.234.567": "1234567"}
        for teks, harap in kasus.items():
            self.assertEqual(inv.baca_angka_pengguna(teks), Decimal(harap), teks)

    def test_baca_angka_salah(self):
        for teks in ("", "abc", "12kg", "1..2,,3x"):
            with self.assertRaises(ValueError, msg=teks):
                inv.baca_angka_pengguna(teks)

    def test_fmt(self):
        self.assertEqual(inv.fmt(Decimal("1200")), "1.200")
        self.assertEqual(inv.fmt(Decimal("12.50")), "12,5")
        self.assertEqual(inv.fmt(Decimal("1234567.25")), "1.234.567,25")
        self.assertEqual(inv.fmt(Decimal("-0.5")), "-0,5")
        self.assertEqual(inv.fmt(90.0), "90")
        self.assertEqual(inv.fmt(Decimal("1E+2")), "100")

    def test_desimal_tanpa_galat_biner(self):
        # 0.1 + 0.2 float = 0.30000000000000004; lewat str -> Decimal persis
        self.assertEqual(inv.ke_desimal(0.1) + inv.ke_desimal(0.2), Decimal("0.3"))

    def test_dec_json(self):
        self.assertEqual(inv.dec(Decimal("90.0")), "90")
        self.assertIsNone(inv.dec(None))


# ============================================================ 2. keamanan URL & CSV

class TesUrlCsv(unittest.TestCase):
    def test_url_lokal_boleh(self):
        for u in ("http://localhost", "http://127.0.0.1:8000", "http://inventree.localhost", "http://[::1]:8000"):
            inv.periksa_url(u, False)

    def test_url_internet_ditolak(self):
        with self.assertRaises(inv.Gagal):
            inv.periksa_url("https://gudang.contoh.com", False)
        with self.assertRaises(inv.Gagal):
            inv.periksa_url("http://gudang.contoh.com", True)  # izin ada, tapi tanpa HTTPS
        inv.periksa_url("https://gudang.contoh.com", True)

    def test_url_kantor_http_dengan_izin(self):
        inv.periksa_url("http://192.168.1.10:8000", True)
        with self.assertRaises(inv.Gagal):
            inv.periksa_url("http://192.168.1.10:8000", False)

    def test_url_skema_aneh(self):
        with self.assertRaises(inv.Gagal):
            inv.periksa_url("ftp://127.0.0.1", False)
        with self.assertRaises(inv.Gagal):
            inv.periksa_url("127.0.0.1:8000", False)

    def test_csv_anti_rumus(self):
        self.assertEqual(inv._aman_csv("=HYPERLINK(\"x\")"), "'=HYPERLINK(\"x\")")
        self.assertEqual(inv._aman_csv("@SUM(A1)"), "'@SUM(A1)")
        self.assertEqual(inv._aman_csv("-5"), "-5")
        self.assertEqual(inv._aman_csv("12,5"), "12,5")

    def test_urai_baris_terima(self):
        self.assertEqual(inv.urai_baris_terima("BB-001=150; minyak=40"),
                         [("BB-001", Decimal(150)), ("minyak", Decimal(40))])
        self.assertEqual(inv.urai_baris_terima("BB-001=1.000, BB-002=12,5"),
                         [("BB-001", Decimal(1000)), ("BB-002", Decimal("12.5"))])
        for salah in ("BB-001", "BB-001=0", "BB-001=abc", " "):
            with self.assertRaises(inv.Gagal, msg=salah):
                inv.urai_baris_terima(salah)


# ============================================================ 3. lembar opname

class TesLembarOpname(unittest.TestCase):
    def buat(self, isi):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8-sig")
        f.write(isi)
        f.close()
        return f.name

    def test_titik_koma_dan_kosong_dilewati(self):
        p = self.buat("id_stok;kode;nama;lokasi;batch;satuan;stok_sistem;stok_fisik;catatan\n"
                      "5;BB-003;Bumbu;Rak A;B1;kg;12,5;12,5;\n3;BB-002;Minyak;Rak A;M1;L;18;;\n1;BB-001;Singkong;Rak A;S;kg;60;57;\n")
        isi, lewati, salah = inv.baca_lembar_opname(p)
        self.assertEqual([x["id"] for x in isi], [5, 1])
        self.assertEqual(isi[0]["fisik"], Decimal("12.5"))
        self.assertEqual(len(lewati), 1)
        self.assertEqual(salah, [])

    def test_koma_biasa(self):
        p = self.buat("id_stok,stok_sistem,stok_fisik\n7,10,9\n")
        isi, _, _ = inv.baca_lembar_opname(p)
        self.assertEqual(isi[0]["fisik"], Decimal(9))

    def test_negatif_ganda_dan_salah(self):
        p = self.buat("id_stok;stok_sistem;stok_fisik\n1;5;-1\n2;5;lima\n3;5;4\n3;5;4\n")
        _, _, salah = inv.baca_lembar_opname(p)
        teks = " ".join(salah)
        self.assertIn("negatif", teks)
        self.assertIn("bukan angka", teks)
        self.assertIn("lebih dari sekali", teks)

    def test_kolom_wajib(self):
        p = self.buat("kode;jumlah\nBB-001;5\n")
        with self.assertRaises(inv.Gagal) as c:
            inv.baca_lembar_opname(p)
        self.assertEqual(c.exception.kode, inv.K_FILE)

    def test_file_tidak_ada(self):
        with self.assertRaises(inv.Gagal):
            inv.baca_lembar_opname("/tidak/ada.csv")


# ============================================================ 4. token

class TesToken(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()

    def jalan(self, *argv, masukan="", env_tambah=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith("INVENTREE_")}
        env["HOME"] = self.home
        env["USERPROFILE"] = self.home
        env.update(env_tambah or {})
        return subprocess.run([PY, SKRIP] + list(argv), input=masukan, capture_output=True, text=True, env=env,
                              timeout=30)

    def test_simpan_kunci_aman(self):
        rahasia = "inv-abcdef0123456789abcdef0123456789abcdef01-20270929"
        p = self.jalan("simpan-kunci", masukan=rahasia + "\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        path = os.path.join(self.home, ".komunitech", "inventree-kunci.txt")
        with open(path) as fh:
            self.assertEqual(fh.read().strip(), rahasia)
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)
        self.assertNotIn(rahasia, p.stdout + p.stderr)
        p2 = self.jalan("simpan-kunci", masukan=rahasia + "\n")
        self.assertEqual(p2.returncode, inv.K_FILE)  # tidak menimpa tanpa --ya

    def test_simpan_kunci_tolak_bentuk_aneh(self):
        p = self.jalan("simpan-kunci", masukan="Bearer salah\n")
        self.assertEqual(p.returncode, inv.K_INPUT)
        p = self.jalan("simpan-kunci", masukan="tk_vikunjabukaninventree\n")
        self.assertEqual(p.returncode, inv.K_INPUT)

    def test_urutan_token(self):
        f = os.path.join(self.home, "kunci2.txt")
        with open(f, "w") as fh:
            fh.write("inv-darifile\n")
        os.chmod(f, 0o600)

        class A:
            kunci_file = f
        os.environ["INVENTREE_API_TOKEN"] = "inv-darienv"
        try:
            self.assertEqual(inv.ambil_token(A), "inv-darifile")
            A.kunci_file = None
            self.assertEqual(inv.ambil_token(A), "inv-darienv")
        finally:
            del os.environ["INVENTREE_API_TOKEN"]

    def test_samarkan(self):
        s = inv.samarkan("inv-abcdef0123456789-20270929")
        self.assertTrue(s.startswith("inv-ab") and s.endswith("0929") and "****" in s)
        self.assertNotIn("0123456789", s)


# ============================================================ 5. perintah baca lewat server tiruan

def bom_rekaman(part):
    return FIX[f"GET /api/bom/?part={part}&sub_part_detail=true&limit=100&offset=0"]["baca" if part == 7 else "gudang"]["body"]["results"]


class TesBaca(DasarServer):
    def test_cek_baca(self):
        k, out, err = self.jalan("cek")
        self.assertEqual(k, 0, err)
        self.assertIn("Versi server: 1.5.6 (API 530)", out)
        self.assertIn("opname (tulis): tidak", out)
        self.assertNotIn(TOKEN_BACA, out + err)
        self.assertIn("inv-uj****0929", out)

    def test_cek_gudang_peringatan_tulis(self):
        k, out, _ = self.jalan("cek", token=TOKEN_GUDANG)
        self.assertEqual(k, 0)
        self.assertIn("BISA MENULIS", out)

    def test_cek_bukan_inventree(self):
        self.t.bukan_inventree = True
        k, _, err = self.jalan("cek")
        self.assertEqual(k, inv.K_KONEKSI)
        self.assertIn("bukan InvenTree", err)

    def test_cari(self):
        k, out, _ = self.jalan("cari", "keripik")
        self.assertEqual(k, 0)
        self.assertIn("Jumlah: 2", out)
        self.assertIn("Keripik Singkong Original 250g [PJ-002] | Produk Jadi | stok 90 (min 150) - DI BAWAH MINIMUM", out)

    def test_stok_total_dan_batch(self):
        k, out, _ = self.jalan("stok", "BB-001")
        self.assertEqual(k, 0)
        items = FIX["GET /api/stock/?in_stock=true&location_detail=true&part_detail=true&part=1&limit=100&offset=0"]["baca"]["body"]["results"]
        total = sum(Decimal(str(i["quantity"])) for i in items)
        self.assertEqual(total, Decimal(85))
        self.assertIn(f"Total: {inv.fmt(total)} kg (2 item stok)", out)
        self.assertIn("60 kg (batch SK-2609)", out)

    def test_stok_ambigu(self):
        k, _, err = self.jalan("stok", "singkong")
        self.assertEqual(k, inv.K_GANDA)
        self.assertIn("cocok dengan 3 barang", err)

    def test_stok_404(self):
        k, _, err = self.jalan("stok", "#999")
        self.assertEqual(k, inv.K_KONEKSI)
        self.assertIn("404", err)

    def test_lokasi(self):
        k, out, _ = self.jalan("lokasi")
        self.assertEqual(k, 0)
        self.assertIn("Gudang Utama/Rak A (4 item stok)", out)
        k, out, _ = self.jalan("lokasi", "Rak A")
        self.assertIn("Bumbu Balado [BB-003]: 12,5 kg", out)

    def test_stok_menipis_hitung_independen(self):
        k, out, _ = self.jalan("stok-menipis", "--json")
        self.assertEqual(k, 0)
        data = json.loads(out)
        rek = FIX["GET /api/part/?low_stock=true&active=true&limit=100&offset=0"]["baca"]["body"]["results"]
        self.assertEqual(data["jumlah"], len(rek))
        for p in rek:
            harap = max(Decimal(str(p["minimum_stock"])) - Decimal(str(p["total_in_stock"])) -
                        Decimal(str(p["ordering"])) - Decimal(str(p["building"])), Decimal(0))
            baris = [b for b in data["barang"] if b["id"] == p["pk"]][0]
            self.assertEqual(Decimal(baris["saran"]), harap, p["name"])
        teks = self.jalan("stok-menipis")[1]
        self.assertIn("Keripik Singkong Original 250g [PJ-002]: stok 90, minimum 150, kurang 60 (perlu diproduksi lagi min. 60)", teks)
        self.assertIn("dibutuhkan produksi/penjualan terbuka 30 kg", teks)  # BO-0001 100 unit x 0,3 kg

    def test_po_terbuka(self):
        k, out, _ = self.jalan("po-terbuka")
        self.assertEqual(k, 0)
        self.assertIn("PO-0001 | CV Tani Makmur (fiktif) | Sudah dipesan", out)
        self.assertIn("Singkong Kupas [BB-001]: dipesan 200, diterima 0, sisa 200 kg", out)
        self.assertIn("Standing Pouch 250g [KM-001]: dipesan 1.000", out)

    def test_bom_maks_independen(self):
        k, out, _ = self.jalan("bom", "PJ-001")
        self.assertEqual(k, 0)
        harap = min(math.floor(Decimal(str(b["available_stock"])) / Decimal(str(b["quantity"]))) for b in bom_rekaman(7))
        self.assertEqual(harap, 283)  # 85 kg / 0,3 kg
        self.assertIn(f"Maksimal bisa diproduksi dari stok sekarang: {harap} unit", out)
        self.assertIn("Bumbu Balado [BB-003]: 0,02 kg (stok tersedia 12,5 kg; cukup untuk 625 unit)", out)

    def test_produksi_kebutuhan(self):
        k, out, _ = self.jalan("produksi-ringkas", "--produk", "PJ-001", "--jumlah", "300")
        self.assertEqual(k, 0)
        self.assertIn("Singkong Kupas [BB-001]: butuh 90 kg, tersedia 85 -> KURANG 5 kg", out)
        self.assertIn("Label Stiker Sumber Rasa [KM-002]: butuh 300, tersedia 300 -> CUKUP", out)
        self.assertIn("BAHAN BELUM CUKUP", out)

    def test_produksi_input_kurang(self):
        self.assertEqual(self.jalan("produksi-ringkas", "--produk", "PJ-001")[0], inv.K_INPUT)
        self.assertEqual(self.jalan("produksi-ringkas", "--produk", "PJ-001", "--jumlah", "-3")[0], inv.K_INPUT)
        self.assertEqual(self.jalan("produksi-ringkas", "--produk", "PJ-001", "--jumlah", "banyak")[0], inv.K_INPUT)

    def test_bom_bukan_rakitan(self):
        k, _, err = self.jalan("bom", "BB-001")
        self.assertEqual(k, inv.K_INPUT)
        self.assertIn("bukan produk rakitan", err)

    def test_produksi_terbuka(self):
        k, out, _ = self.jalan("produksi-ringkas")
        self.assertIn("BO-0001 Keripik Singkong Balado 250g: 0/100 selesai | Menunggu | target 1 Okt 2026", out)

    def test_laporan_harian_hanya_baca(self):
        k, out, _ = self.jalan("laporan-harian")
        self.assertEqual(k, 0)
        self.assertIn("STOK MENIPIS (di bawah minimum): 4 barang", out)
        self.assertIn("PO TERBUKA: 2 (0 terlambat)", out)
        self.assertEqual(self.tulis(), [])

    def test_ekspor_csv(self):
        f = os.path.join(self.tmp, "e.csv")
        k, out, _ = self.jalan("ekspor-csv", "--keluaran", f)
        self.assertEqual(k, 0)
        with open(f, encoding="utf-8-sig") as fh:
            baris = list(csv.reader(fh, delimiter=";"))
        rek = FIX["GET /api/stock/?in_stock=true&location_detail=true&part_detail=true&limit=100&offset=0"]["baca"]["body"]["results"]
        self.assertEqual(len(baris) - 1, len(rek))
        self.assertIn(["5", "BB-003", "Bumbu Balado", "Gudang Utama/Rak A", "BL-0901", "12,5", "kg", "", "OK", ""], baris)
        f2 = os.path.join(self.tmp, "b.csv")
        self.jalan("ekspor-csv", "--jenis", "barang", "--pemisah", "koma", "--keluaran", f2)
        with open(f2, encoding="utf-8-sig") as fh:
            b2 = list(csv.reader(fh))
        self.assertEqual(b2[0][:3], ["kode", "nama", "kategori"])
        self.assertTrue(any(r[0] == "BB-003" and r[4] == "12.5" for r in b2))

    def test_halaman_banyak(self):
        k, out, _ = self.jalan("cari", "banyak", "--json", "--maks", "500")
        self.assertEqual(k, 0)
        self.assertEqual(json.loads(out)["jumlah"], 150)

    def test_json_valid(self):
        for argv in (["cari", "keripik"], ["po-terbuka"], ["bom", "PJ-001"], ["laporan-harian"]):
            k, out, _ = self.jalan(*argv, "--json")
            self.assertEqual(k, 0)
            self.assertIn("teks", json.loads(out))


# ============================================================ 6. galat koneksi & hak akses

class TesGalat(DasarServer):
    def test_401(self):
        k, _, err = self.jalan("stok-menipis", token="inv-salahsalahsalah0000")
        self.assertEqual(k, inv.K_AUTH)
        self.assertIn("401", err)

    def test_403_baca_saja_tidak_bisa_menulis(self):
        f = os.path.join(self.tmp, "o403.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("id_stok;stok_sistem;stok_fisik\n5;12,5;12\n")
        k, _, err = self.jalan("opname", "--file", f, "--ya")
        self.assertEqual(k, inv.K_AUTH)
        self.assertIn("403", err)

    def test_server_mati(self):
        k, _, err = self.jalan("cari", "x", "--url", "http://127.0.0.1:9")
        self.assertEqual(k, inv.K_KONEKSI)
        self.assertIn("Tidak bisa menghubungi", err)

    def test_timeout_baca(self):
        key = "GET /api/part/?search=keripik&active=true&limit=100&offset=0"
        self.t.tunda[key] = 2
        k, _, err = self.jalan("cari", "keripik", "--timeout", "0.5")
        self.assertEqual(k, inv.K_KONEKSI)

    def test_jarak_jauh_tanpa_panggil(self):
        k, _, err = self.jalan("cari", "x", "--url", "http://gudang.contoh.com")
        self.assertEqual(k, inv.K_INPUT)
        self.assertEqual(self.t.diterima, [])

    def test_tanpa_token(self):
        k, _, err = self.jalan("cari", "x", token=None)
        self.assertEqual(k, inv.K_FILE)
        self.assertIn("simpan-kunci", err)

    def test_kedaluwarsa_format_salah(self):
        k, _, _ = self.jalan("terima-barang", "--po", "PO-0001", "--semua", "--kedaluwarsa", "6/10/2026",
                             token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)


# ============================================================ 7. opname (tulis)

class TesOpname(DasarServer):
    # Rekaman 'gudang' untuk /api/stock/{1,3,5}/ = keadaan SESUDAH opname (57 / 17,5 / 12,5).
    def lembar(self, nama, isi):
        f = os.path.join(self.tmp, nama)
        with open(f, "w", encoding="utf-8-sig") as fh:
            fh.write(isi)
        return f

    def test_draf(self):
        f = os.path.join(self.tmp, "draf.csv")
        k, out, _ = self.jalan("opname-draf", "--lokasi", "Rak A", "--keluaran", f)
        self.assertEqual(k, 0)
        with open(f, encoding="utf-8-sig") as fh:
            baris = list(csv.reader(fh, delimiter=";"))
        self.assertEqual(baris[0], inv.KOLOM_OPNAME)
        self.assertEqual(len(baris), 5)
        self.assertTrue(all(r[7] == "" for r in baris[1:]))
        self.assertEqual(self.tulis(), [])

    def test_pratinjau_tidak_menulis(self):
        f = self.lembar("p.csv", "id_stok;nama;satuan;stok_sistem;stok_fisik\n1;Singkong;kg;57;55\n5;Bumbu;kg;12,5;12,5\n")
        k, out, _ = self.jalan("opname", "--file", f, token=TOKEN_GUDANG)
        self.assertEqual(k, 0)
        self.assertIn("sistem 57 kg, fisik 55 kg -> KURANG 2 kg", out)
        self.assertIn("1 item selisih, 1 item sama", out)
        self.assertIn("Belum disimpan", out)
        self.assertEqual(self.tulis(), [])

    def test_simpan_dengan_ya(self):
        f = self.lembar("y.csv", "id_stok;nama;stok_sistem;stok_fisik\n1;Singkong;57;55\n3;Minyak;17,5;17,5\n")
        k, out, err = self.jalan("opname", "--file", f, "--catatan", "akhir bulan", "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, 0, err)
        tulis = self.tulis()
        self.assertEqual(len(tulis), 1)
        metode, path, _, body = tulis[0]
        self.assertEqual((metode, path), ("POST", "/api/stock/count/"))
        self.assertEqual(body["items"], [{"pk": 1, "quantity": "55"}, {"pk": 3, "quantity": "17.5"}])
        self.assertIn("akhir bulan", body["notes"])
        self.assertIn("TERSIMPAN", out)

    def test_berubah_sejak_draf_berhenti(self):
        f = self.lembar("b.csv", "id_stok;nama;stok_sistem;stok_fisik\n1;Singkong;60;57\n")
        k, out, _ = self.jalan("opname", "--file", f, "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)
        self.assertIn("BERUBAH", out)
        self.assertEqual(self.tulis(), [])

    def test_lembar_rusak_tidak_ada_yang_dikirim(self):
        f = self.lembar("r.csv", "id_stok;stok_sistem;stok_fisik\n1;57;lima puluh\n")
        k, _, err = self.jalan("opname", "--file", f, "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)
        self.assertEqual(self.t.diterima, [])

    def test_item_hilang_404(self):
        f = self.lembar("h.csv", "id_stok;stok_sistem;stok_fisik\n4242;5;5\n")
        k, _, err = self.jalan("opname", "--file", f, token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)
        self.assertIn("sudah tidak ada", err)

    def test_galat_500_saat_tulis(self):
        self.t.timpa["POST /api/stock/count/"] = (500, {"detail": "err"})
        f = self.lembar("e.csv", "id_stok;stok_sistem;stok_fisik\n5;12,5;12\n")
        k, _, err = self.jalan("opname", "--file", f, "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_TAKPASTI)
        self.assertIn("JANGAN ulangi", err)
        self.assertEqual(len(self.tulis()), 1)  # tidak mengulang sendiri

    def test_timeout_saat_tulis(self):
        self.t.tunda["POST /api/stock/count/"] = 2
        f = self.lembar("t.csv", "id_stok;stok_sistem;stok_fisik\n5;12,5;12\n")
        k, _, err = self.jalan("opname", "--file", f, "--ya", "--timeout", "0.7", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_TAKPASTI)
        self.assertIn("TIDAK PASTI", err)
        self.assertEqual(len(self.tulis()), 1)

    def test_400_dari_server(self):
        self.t.timpa["POST /api/stock/count/"] = (400, {"items": [{"quantity": ["Ensure this value is greater than or equal to 0."]}]})
        f = self.lembar("q.csv", "id_stok;stok_sistem;stok_fisik\n5;12,5;12\n")
        k, _, err = self.jalan("opname", "--file", f, "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_TULIS)
        self.assertIn("menolak data (400)", err)


# ============================================================ 8. terima barang (tulis)

class TesTerima(DasarServer):
    # Rekaman 'gudang' baris PO-0001 = keadaan SESUDAH terima 150 kg singkong + 40 L minyak (sisa: singkong 50).
    def test_perlu_baris(self):
        k, _, err = self.jalan("terima-barang", "--po", "PO-0001", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)

    def test_melebihi_sisa(self):
        k, _, err = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "BB-001=60", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)
        self.assertIn("melebihi sisa pesanan 50", err)

    def test_baris_sudah_lengkap(self):
        k, _, err = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "minyak=1", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)
        self.assertIn("tidak ada di baris terbuka", err)

    def test_pratinjau(self):
        k, out, _ = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "BB-001=50", "--batch", "SK-3009",
                               token=TOKEN_GUDANG)
        self.assertEqual(k, 0)
        self.assertIn("Masuk ke lokasi: Gudang Utama/Rak A", out)
        self.assertIn("Singkong Kupas [BB-001]: terima 50 kg (sisa pesanan 50)", out)
        self.assertEqual(self.tulis(), [])

    def test_simpan(self):
        k, out, err = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "BB-001=50", "--batch", "SK-3009",
                                 "--kedaluwarsa", "2026-10-07", "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, 0, err)
        tulis = self.tulis()
        self.assertEqual(len(tulis), 1)
        _, path, _, body = tulis[0]
        self.assertEqual(path, "/api/order/po/1/receive/")
        self.assertEqual(body, {"items": [{"line_item": 1, "quantity": "50", "status": 10, "batch_code": "SK-3009",
                                           "expiry_date": "2026-10-07"}], "location": 2})

    def test_status_po_bukan_placed(self):
        key = "GET /api/order/po/?search=PO-0001&limit=100&offset=0"
        rek = json.loads(json.dumps(FIX[key]["gudang"]["body"]))
        rek["results"][0]["status"] = 30
        self.t.timpa[key] = (200, rek)
        k, _, err = self.jalan("terima-barang", "--po", "PO-0001", "--semua", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)
        self.assertIn("Sudah dipesan", err)



# ============================================================ 9. v1.0.1: pencocokan baris PO, redirect, proxy, catatan

class Penangkap:
    """Server kedua yang mencatat setiap permintaan (termasuk header Authorization) yang SAMPAI kepadanya."""

    def __init__(self):
        self.masuk = []
        tangkap = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _catat(self):
                tangkap.masuk.append((self.command, self.path, self.headers.get("Authorization"),
                                      self.headers.get("Proxy-Authorization")))
                raw = b'{"server": "InvenTree", "version": "palsu"}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            do_GET = do_POST = do_CONNECT = _catat

        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def tutup(self):
        self.srv.shutdown()
        self.srv.server_close()


def baris_po_tiruan(daftar):
    """daftar: [(pk_baris, pk_barang, IPN, nama, sku, pesan, diterima, kemasan)] -> jawaban po-line bergaya 1.5.6."""
    hasil = []
    for pk, part, ipn, nama, sku, pesan, terima, kemasan in daftar:
        hasil.append({"pk": pk, "order": 1, "part": 100 + pk, "quantity": pesan, "received": terima, "sku": sku,
                      "destination": None, "internal_part": part, "internal_part_name": nama,
                      "part_detail": {"pk": part, "IPN": ipn, "name": nama, "units": "", "trackable": False},
                      "supplier_part_detail": {"pk": 100 + pk, "SKU": sku, "pack_quantity_native": kemasan}})
    return {"count": len(hasil), "next": None, "previous": None, "results": hasil}


KEY_BARIS_PO1 = "GET /api/order/po-line/?order=1&part_detail=true&limit=100&offset=0"


class TesV101(DasarServer):
    def pasang_baris(self):
        self.t.timpa[KEY_BARIS_PO1] = (200, baris_po_tiruan([
            (1, 51, "PK-05", "Paku 5 cm", "SUP-P5", 10, 0, 1),
            (2, 52, "PK-05B", "Paku 5 cm Beton", "SUP-P5B", 10, 0, 1),
            (3, 53, "RL-09", "Rol Kabel", "SUP-RL", 2, 0, 6),
        ]))

    def test_ipn_persis_menang_atas_awalan(self):
        self.pasang_baris()
        k, out, err = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "PK-05=4", token=TOKEN_GUDANG)
        self.assertEqual(k, 0, err)
        self.assertIn("Paku 5 cm [PK-05]: terima 4", out)
        self.assertNotIn("PK-05B", out)
        k, out, _ = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "pk-05b=3", token=TOKEN_GUDANG)
        self.assertIn("Paku 5 cm Beton [PK-05B]: terima 3", out)

    def test_nama_persis_menang_dan_simpan_baris_benar(self):
        self.pasang_baris()
        k, out, err = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "Paku 5 cm=2", "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, 0, err)
        self.assertEqual(self.tulis()[0][3]["items"][0]["line_item"], 1)

    def test_id_barang_dan_sku(self):
        self.pasang_baris()
        k, out, _ = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "#52=1; SUP-P5=1", token=TOKEN_GUDANG)
        self.assertEqual(k, 0)
        self.assertIn("[PK-05B]: terima 1", out)
        self.assertIn("[PK-05]: terima 1", out)

    def test_potongan_ambigu_tetap_ditanya(self):
        self.pasang_baris()
        k, _, err = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "paku=1", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_GANDA)
        self.assertIn("SKU pemasok SUP-P5B", err)
        self.assertEqual(self.tulis(), [])

    def test_baris_sama_dua_kali_ditolak(self):
        self.pasang_baris()
        k, _, err = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "PK-05=1; #51=1", token=TOKEN_GUDANG)
        self.assertEqual(k, inv.K_INPUT)
        self.assertIn("lebih dari sekali", err)

    def test_kemasan_pemasok_ditampilkan(self):
        self.pasang_baris()
        k, out, _ = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "RL-09=1", token=TOKEN_GUDANG)
        self.assertIn("terima 1 kemasan pemasok (= 6 stok)", out)
        k, out, _ = self.jalan("terima-barang", "--po", "PO-0001", "--baris", "RL-09=1", "--ya", token=TOKEN_GUDANG)
        self.assertIn("+1 kemasan pemasok = +6 stok", out)

    def test_redirect_tidak_diikuti_token_tidak_bocor(self):
        tangkap = Penangkap()
        try:
            key = "GET /api/part/?search=keripik&active=true&limit=100&offset=0"
            self.t.timpa[key] = (302, {}, {"Location": tangkap.url + "/api/part/?search=keripik"})
            k, _, err = self.jalan("cari", "keripik")
            self.assertEqual(k, inv.K_KONEKSI)
            self.assertIn("mengalihkan", err)
            self.assertEqual(tangkap.masuk, [])  # tidak ada permintaan (apalagi token) ke alamat tujuan redirect
            self.t.timpa["POST /api/stock/count/"] = (307, {}, {"Location": tangkap.url + "/api/stock/count/"})
            f = os.path.join(self.tmp, "r307.csv")
            with open(f, "w", encoding="utf-8") as fh:
                fh.write("id_stok;stok_sistem;stok_fisik\n5;12,5;12\n")
            k, _, err = self.jalan("opname", "--file", f, "--ya", token=TOKEN_GUDANG)
            self.assertEqual(k, inv.K_KONEKSI)
            self.assertEqual(tangkap.masuk, [])
        finally:
            tangkap.tutup()

    def test_proxy_env_diabaikan_untuk_localhost(self):
        proxy = Penangkap()
        try:
            env = {"HTTP_PROXY": proxy.url, "http_proxy": proxy.url, "HTTPS_PROXY": proxy.url,
                   "https_proxy": proxy.url, "ALL_PROXY": proxy.url}
            k, out, err = self.jalan("cari", "keripik", env_tambah=env)
            self.assertEqual(k, 0, err)
            self.assertIn("Jumlah: 2", out)
            self.assertEqual(proxy.masuk, [])  # token tidak pernah lewat proxy
            self.assertTrue(any(d[2] == "baca" for d in self.t.diterima))  # langsung ke server lokal
        finally:
            proxy.tutup()

    def test_opener_lokal_tanpa_proxy_internet_pakai_proxy(self):
        lama = os.environ.get("HTTPS_PROXY")
        os.environ["HTTPS_PROXY"] = "http://proxy.kantor.contoh:3128"
        try:
            def proxies(url):
                op = inv.buat_opener(url)
                # ProxyHandler({}) tidak didaftarkan urllib sama sekali (tanpa metode *_open) = tanpa proxy.
                ph = [h for h in op.handlers if isinstance(h, inv.urllib.request.ProxyHandler)]
                self.assertTrue(any(isinstance(h, inv._TolakPengalihan) for h in op.handlers))
                return ph[0].proxies if ph else {}
            self.assertEqual(proxies("http://localhost"), {})
            self.assertEqual(proxies("http://192.168.1.10:8000"), {})
            self.assertIn("https", proxies("https://gudang.contoh.com"))
        finally:
            if lama is None:
                del os.environ["HTTPS_PROXY"]
            else:
                os.environ["HTTPS_PROXY"] = lama

    def test_catatan_per_baris_ikut_dikirim(self):
        f = os.path.join(self.tmp, "cat.csv")
        with open(f, "w", encoding="utf-8-sig") as fh:
            fh.write("id_stok;nama;stok_sistem;stok_fisik;catatan\n3;Minyak;17,5;17;1 jeriken bocor\n1;Singkong;57;57;\n")
        k, out, _ = self.jalan("opname", "--file", f, token=TOKEN_GUDANG)
        self.assertIn("| catatan: 1 jeriken bocor", out)
        k, out, err = self.jalan("opname", "--file", f, "--ya", token=TOKEN_GUDANG)
        self.assertEqual(k, 0, err)
        notes = self.tulis()[0][3]["notes"]
        self.assertIn("id 3 (Minyak): 1 jeriken bocor", notes)
        self.assertLessEqual(len(notes), 512)

    def test_catatan_panjang_dipotong(self):
        import datetime as _dt
        isi = [{"id": i, "nama": "Barang", "kode": "", "catatan": "x" * 80} for i in range(20)]
        teks = inv.susun_catatan_opname(_dt.date(2026, 9, 29), "akhir bulan", isi)
        self.assertLessEqual(len(teks), 512)
        self.assertTrue(teks.endswith("(terpotong)"))

    def test_produksi_menunggu_ikut_dihitung(self):
        key = "GET /api/part/?low_stock=true&active=true&limit=100&offset=0"
        rek = json.loads(json.dumps(FIX[key]["baca"]["body"]))
        for p in rek["results"]:
            if p["IPN"] == "PJ-002":
                p["scheduled_to_build"] = 40.0   # BO Pending 40 unit, building masih 0
        self.t.timpa[key] = (200, rek)
        k, out, _ = self.jalan("stok-menipis")
        self.assertIn("dalam perintah produksi terbuka 40", out)
        self.assertIn("perlu diproduksi lagi min. 20", out)  # 150 - 90 - 0 - 40

    def test_folder_kunci_700(self):
        if os.name == "nt":
            self.skipTest("izin POSIX")
        home = tempfile.mkdtemp()
        env = {k: v for k, v in os.environ.items() if not k.startswith("INVENTREE_")}
        env["HOME"] = home
        p = subprocess.run([PY, SKRIP, "simpan-kunci"], input="inv-abc123abc123abc123\n", capture_output=True,
                           text=True, env=env, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(stat.S_IMODE(os.stat(os.path.join(home, ".komunitech")).st_mode), 0o700)

    def test_peringatan_lan_sekali(self):
        k, _, err = self.jalan("cari", "x", "--url", "http://192.168.254.254:9", "--izinkan-jarak-jauh",
                               "--timeout", "0.5")
        self.assertEqual(err.count("PERINGATAN"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
