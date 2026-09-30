#!/usr/bin/env python3
"""Uji regresi odoo.py memakai server Odoo TIRUAN (tests/server_tiruan.py, Python standar).

PENTING (jujur): server tiruan meniru BENTUK API eksternal resmi Odoo (XML-RPC /xmlrpc/2 dan
JSON-2 /json/2) menurut dokumentasi resmi; ia BUKAN Odoo sungguhan dan belum dicocokkan dengan
rekaman respons Odoo asli. Angka penting dihitung ulang di sini secara independen dari data
tiruan (bukan disalin dari keluaran script).

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
"""
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

SINI = os.path.dirname(os.path.abspath(__file__))
SKRIP = os.path.join(SINI, "..", "scripts", "odoo.py")
PY = sys.executable
sys.path.insert(0, SINI)
import server_tiruan as st  # noqa: E402

spec = importlib.util.spec_from_file_location("odoo_mod", SKRIP)
od = importlib.util.module_from_spec(spec)
spec.loader.exec_module(od)

SEMUA_KUNCI = list(st.KUNCI) + ["salah-kunci-1234567890"]
KELUARAN = []   # semua stdout+stderr untuk uji "kunci tidak pernah tercetak"
TGL = "2026-09-30"


def jalan(port, *argv, kunci=st.KUNCI_BACA, home=None, env_tambah=None, masukan=None, db=True, login="baca"):
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("ODOO_") or k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            env.pop(k)
    env["HOME"] = home or tempfile.mkdtemp()
    env["USERPROFILE"] = env["HOME"]
    if kunci:
        env["ODOO_API_KEY"] = kunci
    if port:
        env["ODOO_URL"] = "http://127.0.0.1:{}".format(port)
    if db:
        env["ODOO_DB"] = st.DB
    if login:
        env["ODOO_LOGIN"] = {"baca": "bot-laporan@tokomaju.test", "jual": "bot-penjualan@tokomaju.test",
                             "admin": "admin@tokomaju.test",
                             "sendiri": "bot-own@tokomaju.test"}.get(login, login)
    env.update(env_tambah or {})
    p = subprocess.run([PY, SKRIP] + list(argv), capture_output=True, text=True, env=env, input=masukan, timeout=60)
    KELUARAN.append(p.stdout + p.stderr)
    return p.returncode, p.stdout, p.stderr


class Server:
    def __init__(self, versi=19, mode=None):
        self.srv, self.t = st.buat_server(versi, mode)
        self.port = self.srv.server_address[1]

    def tutup(self):
        self.srv.shutdown()
        self.srv.server_close()


# ============================================================ perhitungan independen dari data tiruan
def harapan_penjualan(data, awal_utc, akhir_utc):
    so = [s for s in data["sale.order"] if s["state"] in ("sale", "done") and awal_utc <= s["date_order"] < akhir_utc
          and s["currency_id"][1] == "IDR"]
    return len(so), sum(Decimal(str(s["amount_total"])) for s in so)


def harapan_piutang_lampau(data, per):
    """Hitung ulang independen: faktur terbit <= per, sisa per tanggal = sisa kini + pelunasan setelah per."""
    baris_ke_faktur = {b["id"]: b["move_id"][0] for b in data["account.move.line"]}
    tambah = {}
    for pr in data["account.partial.reconcile"]:
        if pr["max_date"] > per:
            fid = baris_ke_faktur[pr["debit_move_id"][0]]
            tambah[fid] = tambah.get(fid, Decimal(0)) + Decimal(str(pr["amount"]))
    hasil = {}
    for f in data["account.move"]:
        if f["move_type"] == "out_invoice" and f["state"] == "posted" and f["invoice_date"] <= per:
            sisa = Decimal(str(f["amount_residual_signed"])) + tambah.get(f["id"], Decimal(0))
            if sisa > 0:
                hasil[f["name"]] = sisa
    return hasil


def harapan_piutang(data, per):
    import datetime as dt
    hasil = []
    for f in data["account.move"]:
        if f["move_type"] == "out_invoice" and f["state"] == "posted" and f["payment_state"] in ("not_paid", "partial") \
                and f["amount_residual_signed"] > 0:
            hari = (dt.date.fromisoformat(per) - dt.date.fromisoformat(f["invoice_date_due"])).days
            hasil.append((f["name"], Decimal(str(f["amount_residual_signed"])), hari))
    return hasil


# ============================================================ unit
class UjiFungsi(unittest.TestCase):
    def test_format_rupiah_dan_angka(self):
        self.assertEqual(od.format_rp(Decimal("1917352.95")), "Rp 1.917.352,95")
        self.assertEqual(od.format_rp(Decimal("-49950")), "-Rp 49.950")
        self.assertEqual(od.format_rp(Decimal("0.005")), "Rp 0,01")
        self.assertEqual(od.format_angka(Decimal("2.5")), "2,5")
        self.assertEqual(od.format_angka(Decimal("1200")), "1.200")
        self.assertEqual(od.format_angka(Decimal("-2")), "-2")

    def test_angka_indonesia(self):
        self.assertEqual(od.angka_id("85.000", "harga"), Decimal(85000))
        self.assertEqual(od.angka_id("2,5", "jumlah"), Decimal("2.5"))
        self.assertEqual(od.angka_id("Rp 1.250.000", "harga"), Decimal(1250000))
        for buruk in ("62,500", "-3", "tiga", "1.2.3", "1e5"):
            with self.assertRaises(od.Gagal):
                od.angka_id(buruk, "harga")
        with self.assertRaises(od.Gagal):
            od.angka_id("2000000", "jumlah", od.BATAS_JUMLAH)

    def test_uang_float_odoo(self):
        self.assertEqual(od.uang(0.1 + 0.2), Decimal("0.30"))
        self.assertEqual(od.uang(False), Decimal("0.00"))

    def test_hitung_quotation_standar_pembulatan(self):
        items = [{"qty": Decimal(3), "harga": Decimal(45000), "diskon": Decimal(0)},
                 {"qty": Decimal(2), "harga": Decimal(32500), "diskon": Decimal(0)},
                 {"qty": Decimal(1), "harga": Decimal(132345), "diskon": Decimal(0)}]
        h = od.hitung_quotation(items, "umum")
        self.assertEqual(h["dpp"], Decimal(332345))
        self.assertEqual(h["ppn"], Decimal(36557))          # 36.557,95 dibulatkan ke BAWAH sekali
        self.assertEqual(od.hitung_quotation(items, "mewah")["ppn"], Decimal(39881))   # 39.881,4 -> 39.881
        self.assertEqual(od.hitung_quotation(items, "tanpa")["ppn"], Decimal(0))
        d = od.hitung_quotation([{"qty": Decimal(3), "harga": Decimal(33333), "diskon": Decimal("7.5")}], "umum")
        self.assertEqual(d["dpp"], Decimal(92499))          # 92.499,075 -> terdekat

    def test_inisial_dan_samaran(self):
        self.assertEqual(od.inisial("Hotel Melati Indah"), "H.M.I.")
        self.assertEqual(od.inisial("CV Maju Jaya, Budi"), "C.M.J.")
        self.assertEqual(od.inisial(""), "?")
        self.assertEqual(od.samarkan_hp("+62 812-3456-7890"), "0812****890")
        self.assertEqual(od.samarkan_email("budi.s@contoh.test"), "b***@contoh.test")
        self.assertEqual(od.samarkan_kunci(st.KUNCI_BACA), "****5e3f")

    def test_rentang_utc_zona(self):
        import datetime as dt
        self.assertEqual(od.rentang_utc(dt.date(2026, 9, 30), 7), ("2026-09-29 17:00:00", "2026-09-30 17:00:00"))
        self.assertEqual(od.rentang_utc(dt.date(2026, 9, 30), 8)[0], "2026-09-29 16:00:00")

    def test_umur_piutang_batas(self):
        self.assertEqual(od.kelompok_umur(0), "belum jatuh tempo")
        self.assertEqual(od.kelompok_umur(30), "1-30 hari")
        self.assertEqual(od.kelompok_umur(31), "31-60 hari")
        self.assertEqual(od.kelompok_umur(91), ">90 hari")

    def test_allowlist_host(self):
        self.assertTrue(od.cek_url("http://localhost:8069", [])[2])
        self.assertEqual(od.cek_url("https://tokosaya.odoo.com/odoo", [])[0], "https://tokosaya.odoo.com")
        for buruk, izin in (("http://tokosaya.odoo.com", []), ("https://tokosaya.odoo.com.jahat.test", []),
                            ("https://odoo.com", []), ("https://erp.tokosaya.id", []),
                            ("http://erp.tokosaya.id", ["erp.tokosaya.id"]), ("https://u:p@localhost", []),
                            ("ftp://localhost", []), ("https://erp.tokosaya.id/?x=1", ["erp.tokosaya.id"])):
            with self.assertRaises(od.Gagal, msg=buruk):
                od.cek_url(buruk, izin)
        self.assertEqual(od.cek_url("https://ERP.tokosaya.id", ["erp.tokosaya.id"])[1], "erp.tokosaya.id")
        _, _, tanpa_proxy, cat = od.cek_url("http://192.168.1.20:8069", ["192.168.1.20"])
        self.assertTrue(tanpa_proxy)
        self.assertIn("PERINGATAN", cat[0])

    def test_daftar_izin_metode_tanpa_hapus(self):
        semua = set(od.METODE_BACA) | {m for _, m in od.METODE_TULIS}
        for terlarang in ("unlink", "write", "action_confirm", "action_post", "action_quotation_send",
                          "button_validate", "message_post"):
            self.assertNotIn(terlarang, semua)
        api = od.Odoo("http://127.0.0.1:9", "db", "x", "kunci-uji-12345678", "xmlrpc")
        api.protokol = "xmlrpc"
        with self.assertRaises(od.Gagal) as c:
            api.panggil("sale.order", "unlink", [1])
        self.assertIn("tidak diizinkan", c.exception.pesan)
        with self.assertRaises(od.Gagal):
            api.panggil("res.partner", "create", vals_list=[{}])   # create hanya untuk sale.order

    def test_versi_saas(self):
        self.assertEqual(od.Odoo.angka_mayor(["saas~19", 1, 0, "final", 0, ""]), 19)
        self.assertEqual(od.Odoo.angka_mayor([17, 0, 0, "final", 0, ""]), 17)


# ============================================================ integrasi (server tiruan)
class UjiIntegrasi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = {v: Server(v) for v in (16, 17, 18, 19)}

    @classmethod
    def tearDownClass(cls):
        for s in cls.s.values():
            s.tutup()

    def test_cek_semua_versi(self):
        for v, s in self.s.items():
            k, out, err = jalan(s.port, "cek")
            self.assertEqual(k, 0, err)
            self.assertIn("Versi Odoo: {}.0".format(v), out)
            self.assertIn("JSON-2" if v >= 19 else "XML-RPC", out)
            self.assertIn("diuji ke Odoo Community 18 & 19 asli", out)
            self.assertNotIn("belum diuji ke server Odoo asli", out)
            self.assertIn("- Pesanan penjualan: SEMUA data", out)
            self.assertNotIn("PERINGATAN DATA SEBAGIAN", out)

    def test_cek_admin_diberi_risiko(self):
        k, out, _ = jalan(self.s[19].port, "cek", kunci=st.KUNCI_ADMIN, login="admin")
        self.assertEqual(k, 0)
        self.assertIn("RISIKO", out)
        k, out, _ = jalan(self.s[19].port, "cek")
        self.assertNotIn("RISIKO", out)

    def test_penjualan_angka_independen_dan_zona(self):
        n, total = harapan_penjualan(self.s[19].t.data, "2026-09-29 17:00:00", "2026-09-30 17:00:00")
        self.assertEqual((n, total), (3, Decimal("1917352.95")))
        for v in (16, 17, 18, 19):
            k, out, err = jalan(self.s[v].port, "penjualan", "--tanggal", TGL, "--json")
            self.assertEqual(k, 0, err)
            d = json.loads(out)
            self.assertEqual(d["pesanan"]["jumlah"], n, v)
            self.assertEqual(Decimal(str(d["pesanan"]["total"])), total, v)
            self.assertEqual(d["pesanan"]["mata_uang_lain"][0]["nomor"], "S00106")
        # 1 Okt WIB: S00107 (17.30 UTC tgl 30) masuk; WITA: batas 16.00 UTC
        k, out, _ = jalan(self.s[19].port, "penjualan", "--tanggal", "2026-10-01", "--json")
        self.assertEqual(json.loads(out)["pesanan"]["jumlah"], 1)
        k, out, _ = jalan(self.s[19].port, "penjualan", "--tanggal", TGL, "--tz", "WITA", "--json")
        n2, t2 = harapan_penjualan(self.s[19].t.data, "2026-09-29 16:00:00", "2026-09-30 16:00:00")
        self.assertEqual(Decimal(str(json.loads(out)["pesanan"]["total"])), t2)

    def test_penjualan_teks_faktur_dan_persen(self):
        k, out, _ = jalan(self.s[17].port, "penjualan", "--tanggal", TGL)
        self.assertEqual(k, 0)
        # faktur 30 Sep: 368.902,95 + 1.398.600 - 49.950 (nota kredit)
        self.assertIn("Rp 1.717.552,95", out)
        # kemarin 999.000 + 499.500 = 1.498.500; (1.917.352,95 - 1.498.500)/1.498.500 = 27,95% -> 28
        self.assertIn("Kemarin: Rp 1.498.500 (+28,0%)", out)
        self.assertIn("JANGAN dijumlahkan", out)
        self.assertNotIn("Hotel Melati", out)       # tanpa --rinci tidak ada nama
        k, out, _ = jalan(self.s[17].port, "penjualan", "--tanggal", TGL, "--rinci", "--samarkan")
        self.assertIn("S00103 H.M.I.", out)

    def test_piutang_independen(self):
        har = harapan_piutang(self.s[19].t.data, TGL)
        for v in (17, 19):
            k, out, err = jalan(self.s[v].port, "piutang", "--per-tanggal", TGL, "--json")
            self.assertEqual(k, 0, err)
            d = json.loads(out)
            self.assertEqual(d["jumlah"], len(har))
            self.assertEqual(Decimal(str(d["total"])), sum(x[1] for x in har))
            nomor = [f["nomor"] for f in d["faktur"]]
            for tidak in ("INV/2026/00193", "INV/2026/00194", "INV/2026/00195"):   # in_payment, lunas, draf
                self.assertNotIn(tidak, nomor)
            self.assertEqual(d["umur"][">90 hari"]["jumlah"], sum(1 for x in har if x[2] > 90))
            self.assertEqual(d["faktur"][0]["hari_lewat"], 103)
        k, out, _ = jalan(self.s[19].port, "piutang", "--per-tanggal", TGL, "--samarkan")
        for r in self.s[19].t.data["res.partner"]:
            self.assertNotIn(r["name"], out)
        self.assertIn("nota kredit belum dipakai, Rp 49.950", out)

    def test_stok_menipis_versi_16_sampai_19(self):
        hasil = {}
        for v, s in self.s.items():
            k, out, err = jalan(s.port, "stok-menipis", "--json")
            self.assertEqual(k, 0, err)
            d = json.loads(out)
            hasil[v] = [(x["produk_id"], x["status"], x["saran_pesan"]) for x in d["perhatian"]]
            self.assertEqual([x["produk_id"] for x in d["habis_tanpa_aturan"]], [29])   # jasa (26) tidak ikut
        self.assertEqual(hasil[17], [(24, "MINUS", 26), (23, "HABIS", 50), (22, "MENIPIS", 2),
                                     (21, "PERKIRAAN DI BAWAH MINIMUM", 104)])
        self.assertTrue(all(h == hasil[17] for h in hasil.values()))

    def test_cari_pelanggan_hp_dan_samaran(self):
        for q, harap in (("+62 812-3456-7890", 3), ("081311112222", 8), ("maju", 3), ("sinarabadi", 9)):
            k, out, _ = jalan(self.s[19].port, "pelanggan", "cari", q, "--json")
            self.assertEqual(k, 0)
            ids = [h["id"] for h in json.loads(out)["hasil"]]
            self.assertIn(harap, ids, q)
        k, out, _ = jalan(self.s[17].port, "pelanggan", "cari", "0857 9999 0001")
        self.assertIn("ID 9", out)
        self.assertNotIn("0857-9999-0001", out)
        self.assertNotIn("order@sinarabadi.test", out)

    def test_produk_cari(self):
        k, out, _ = jalan(self.s[18].port, "produk", "cari", "kopi")
        self.assertEqual(k, 0)
        self.assertIn("#21 [KP-250] Kopi Robusta Bubuk 250g: harga jual Rp 45.000, stok 120", out)

    def test_laporan_harian_tersamar_dan_pendek(self):
        for v in (17, 19):
            k, out, err = jalan(self.s[v].port, "laporan-harian", "--tanggal", TGL)
            self.assertEqual(k, 0, err)
            self.assertLessEqual(len(out), od.MAKS_TELEGRAM + 1)
            for r in self.s[v].t.data["res.partner"]:
                self.assertNotIn(r["name"], out)
                if r.get("phone"):
                    self.assertNotIn(r["phone"], out)
            self.assertIn("INV/2026/00170 (H.M.I.) sisa Rp 5.661.000, lewat 103 hari", out)
            self.assertIn("Pesanan terkonfirmasi: 3, total Rp 1.917.352,95", out)

    def test_quotation_pratinjau_tidak_menulis(self):
        s = self.s[17]
        n0 = len(s.t.data["sale.order"])
        k, out, _ = jalan(s.port, "quotation", "buat", "--pelanggan", "3", "--item", "KP-250|3",
                          "--item", "Gula Aren|2|32.500", kunci=st.KUNCI_JUAL, login="jual")
        self.assertEqual(k, 0)
        self.assertIn("PRATINJAU", out)
        self.assertIn("Belum disimpan", out)
        self.assertEqual(len(s.t.data["sale.order"]), n0)
        self.assertNotIn(("sale.order", "create"), s.t.log)


class UjiTulis(unittest.TestCase):
    def setUp(self):
        self.s = None

    def tearDown(self):
        if self.s:
            self.s.tutup()

    def buat(self, v=19, pelanggan="3", extra=(), kunci=st.KUNCI_JUAL, mode=None, **kw):
        if self.s is None:
            self.s = Server(v, mode)
        argv = ["quotation", "buat", "--pelanggan", pelanggan, "--item", "KP-250|3", "--item", "GA-1KG|2|32500",
                "--item", "#25|1|132345"] + list(extra)
        return jalan(self.s.port, *argv, kunci=kunci, login="jual", **kw)

    def draf_ai(self):
        return [s for s in self.s.t.data["sale.order"] if "Komunitech" in str(s.get("origin"))]

    def test_ya_membuat_satu_draf_dan_cocok_lalu_tahan_dobel(self):
        for v in (17, 19):
            self.s = None
            k, out, err = self.buat(v, extra=["--ya"])
            self.assertEqual(k, 0, err)
            self.assertEqual(len(self.draf_ai()), 1)
            self.assertEqual(self.draf_ai()[0]["state"], "draft")
            self.assertIn("Sebelum pajak: COCOK", out)
            self.assertIn("Pajak: COCOK", out)       # 36.557,95 (Odoo tiruan) vs 36.557 (standar) < Rp 1
            k, out, _ = self.buat(v, extra=["--ya"])
            self.assertEqual(k, 7)
            self.assertEqual(len(self.draf_ai()), 1)
            k, out, _ = self.buat(v, extra=["--ya", "--tetap-buat"])
            self.assertEqual(k, 0)
            self.assertEqual(len(self.draf_ai()), 2)
            self.s.tutup()
        self.s = None

    def test_baris_draf_dikirim_benar(self):
        k, out, err = self.buat(19, extra=["--ya", "--berlaku", "7"])
        self.assertEqual(k, 0, err)
        so = self.draf_ai()[0]
        import datetime as dt
        berlaku = dt.date.fromisoformat(so["validity_date"])
        self.assertIn((berlaku - od.hari_ini(7)).days, (7,))
        baris = [b for b in self.s.t.data["sale.order.line"] if b["order_id"][0] == so["id"]]
        self.assertEqual([(b["product_id"][0], b["product_uom_qty"], b["price_unit"]) for b in baris],
                         [(21, 3.0, 45000.0), (22, 2.0, 32500.0), (25, 1.0, 132345.0)])

    def test_kunci_baca_tidak_bisa_membuat(self):
        k, out, err = self.buat(19, extra=["--ya"], kunci=st.KUNCI_BACA)
        self.assertEqual(k, 5, out + err)
        self.assertEqual(self.draf_ai(), [])
        self.s.tutup()
        self.s = Server(17)
        k, out, err = jalan(self.s.port, "quotation", "buat", "--pelanggan", "3", "--item", "KP-250|1", "--ya")
        self.assertEqual(k, 5, out + err)

    def test_timeout_saat_menulis_kode_8_dan_cek_ulang(self):
        k, out, err = self.buat(19, extra=["--ya", "--timeout", "1"], mode=["timeout_create"])
        self.assertEqual(k, 8, out + err)
        self.assertIn("BELUM PASTI TERBUAT", out)
        self.assertIn("SUDAH ADA", out)
        self.assertEqual(len(self.draf_ai()), 1)
        self.assertEqual(self.s.t.log.count(("sale.order", "create")), 1)   # tidak diulang otomatis

    def test_galat_500_saat_menulis_kode_8(self):
        for v in (17, 19):
            self.s = None
            k, out, err = self.buat(v, extra=["--ya"], mode=["error500_create"])
            self.assertEqual(k, 8, out + err)
            self.assertIn("belum terlihat", out)
            self.s.tutup()
        self.s = None

    def test_item_ambigu_dan_tidak_ada(self):
        self.s = Server(19)
        k, _, err = jalan(self.s.port, "quotation", "buat", "--pelanggan", "3", "--item", "kopi|1", kunci=st.KUNCI_JUAL)
        self.assertEqual(k, 7)
        self.assertIn("#28", err)
        k, _, err = jalan(self.s.port, "quotation", "buat", "--pelanggan", "3", "--item", "ZZZ|1", kunci=st.KUNCI_JUAL)
        self.assertEqual(k, 2)
        k, _, err = jalan(self.s.port, "quotation", "buat", "--pelanggan", "999", "--item", "KP-250|1",
                          kunci=st.KUNCI_JUAL)
        self.assertEqual(k, 2)
        self.assertIn("tidak ditemukan", err)
        k, _, err = jalan(self.s.port, "quotation", "buat", "--pelanggan", "3", kunci=st.KUNCI_JUAL)
        self.assertEqual(k, 2)
        k, _, err = jalan(self.s.port, "quotation", "buat", "--pelanggan", "3", "--item", "KP-250|0",
                          kunci=st.KUNCI_JUAL)
        self.assertEqual(k, 2)


class UjiGalatDanKeamanan(unittest.TestCase):
    def test_server_mati(self):
        k, _, err = jalan(1, "cek")
        self.assertEqual(k, 3)
        self.assertIn("tidak bisa dihubungi", err)

    def test_kunci_salah_kedua_protokol(self):
        for v in (17, 19):
            s = Server(v)
            try:
                k, _, err = jalan(s.port, "cek", kunci="salah-kunci-1234567890")
                self.assertEqual(k, 5, err)
                s.t.kunci_kedaluwarsa.add(st.KUNCI_BACA)
                k, _, err = jalan(s.port, "laporan-harian", kunci=st.KUNCI_BACA)
                self.assertEqual(k, 5, err)
            finally:
                s.tutup()

    def test_redirect_ditolak(self):
        s = Server(19, ["redirect"])
        try:
            k, out, err = jalan(s.port, "cek")
            self.assertEqual(k, 2)
            self.assertIn("Kunci API tidak dikirim ulang", err)
        finally:
            s.tutup()

    def test_xmlrpc_dihapus_sarankan_json2(self):
        s = Server(17, ["xmlrpc_hilang"])
        try:
            k, _, err = jalan(s.port, "cek")
            self.assertEqual(k, 4)
            k, _, err = jalan(s.port, "cek", "--protokol", "xmlrpc")
            self.assertEqual(k, 4)
            self.assertIn("--protokol json2", err)
        finally:
            s.tutup()
        s = Server(19, ["xmlrpc_hilang"])
        try:
            k, out, err = jalan(s.port, "cek")     # otomatis -> json2, tetap jalan
            self.assertEqual(k, 0, err)
        finally:
            s.tutup()

    def test_json2_dipaksa_di_odoo_17(self):
        s = Server(17)
        try:
            k, _, err = jalan(s.port, "cek", "--protokol", "json2")
            self.assertEqual(k, 4)
            self.assertIn("Odoo 19", err)
        finally:
            s.tutup()

    def test_bukan_odoo(self):
        s = Server(19, ["bukan_odoo"])
        try:
            k, _, err = jalan(s.port, "cek")
            self.assertEqual(k, 4, err)
        finally:
            s.tutup()

    def test_tanpa_modul_stok_tidak_ada_habis_palsu(self):
        s = Server(19, ["tanpa_stok"])
        try:
            k, _, err = jalan(s.port, "stok-menipis")
            self.assertEqual(k, 4)
            self.assertIn("TIDAK dinilai", err)
            k, out, err = jalan(s.port, "laporan-harian", "--tanggal", TGL)
            self.assertEqual(k, 0, err)
            self.assertNotIn("HABIS", out)
            self.assertIn("Tidak bisa dibaca", out)
        finally:
            s.tutup()

    def test_laporan_semua_bagian_gagal_kode_bukan_0(self):
        s = Server(19, ["tolak_semua"])
        try:
            k, out, err = jalan(s.port, "laporan-harian")
            self.assertEqual(k, 5, out + err)
        finally:
            s.tutup()

    def test_xmlrpc_tanpa_db_atau_login(self):
        s = Server(17)
        try:
            k, _, err = jalan(s.port, "cek", db=False)
            self.assertEqual(k, 2)
            self.assertIn("database", err)
            k, _, err = jalan(s.port, "cek", login=None)
            self.assertEqual(k, 2)
        finally:
            s.tutup()

    def test_host_tidak_diizinkan_dan_atur(self):
        home = tempfile.mkdtemp()
        k, _, err = jalan(None, "cek", "--url", "https://erp.tokosaya.test", home=home)
        self.assertEqual(k, 2)
        self.assertIn("--izinkan-host", err)
        k, out, _ = jalan(None, "atur", "--url", "https://erp.tokosaya.test", "--izinkan-host", home=home, kunci=None)
        self.assertEqual(k, 0)
        with open(os.path.join(home, ".komunitech", "odoo.json"), encoding="utf-8") as f:
            konf = json.load(f)
        self.assertEqual(konf["host_diizinkan"], ["erp.tokosaya.test"])
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(os.stat(os.path.join(home, ".komunitech", "odoo.json")).st_mode), 0o600)
        k, out, _ = jalan(None, "atur", "--url", "https://tokosaya.odoo.com", home=tempfile.mkdtemp(), kunci=None)
        self.assertIn("db: tokosaya", out)

    def test_konfig_berisi_kunci_diabaikan_dan_tidak_dicetak(self):
        s = Server(19)
        home = tempfile.mkdtemp()
        os.makedirs(os.path.join(home, ".komunitech"))
        with open(os.path.join(home, ".komunitech", "odoo.json"), "w") as f:
            json.dump({"url": "http://127.0.0.1:{}".format(s.port), "api_key": st.KUNCI_ADMIN}, f)
        try:
            k, out, err = jalan(None, "cek", home=home)
            self.assertEqual(k, 0, err)
            self.assertIn("DIABAIKAN", err)
            self.assertNotIn(st.KUNCI_ADMIN, out + err)
            self.assertIn("Bot Laporan", out)     # kunci dari ENV yang dipakai, bukan dari konfigurasi
        finally:
            s.tutup()

    def test_file_kunci_izin_dan_simpan_kunci(self):
        if os.name == "nt":
            self.skipTest("izin file POSIX")
        home = tempfile.mkdtemp()
        k, out, err = jalan(None, "simpan-kunci", kunci=None, home=home, masukan=st.KUNCI_BACA + "\n")
        self.assertEqual(k, 0, err)
        path = os.path.join(home, ".komunitech", "odoo-kunci.txt")
        self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)
        self.assertNotIn(st.KUNCI_BACA, out + err)
        k, _, err = jalan(None, "simpan-kunci", kunci=None, home=home, masukan="kunci-lain-123456789\n")
        self.assertEqual(k, 2)
        with open(path, encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), st.KUNCI_BACA)
        s = Server(19)
        try:
            k, out, _ = jalan(s.port, "cek", kunci=None, home=home)
            self.assertEqual(k, 0)
            os.chmod(path, 0o644)
            k, _, err = jalan(s.port, "cek", kunci=None, home=home)
            self.assertEqual(k, 5)
            self.assertIn("chmod 600", err)
            k, _, err = jalan(s.port, "cek", "--kunci-file", os.path.join(home, "tidak-ada.txt"), kunci=None, home=home)
            self.assertEqual(k, 5)
        finally:
            s.tutup()

    def test_kunci_rusak(self):
        k, _, err = jalan(8069, "cek", kunci="abc def ghi jkl mno")
        self.assertEqual(k, 5)
        self.assertIn("spasi", err)

    def test_singkatan_flag_ditolak(self):
        home = tempfile.mkdtemp()
        for argv in (["simpan-kunci", "--y"], ["quotation", "buat", "--pelanggan", "3", "--item", "KP-250|1", "--y"],
                     ["quotation", "buat", "--pelanggan", "3", "--item", "KP-250|1", "--ya", "--tetap"],
                     ["piutang", "--samar"], ["cek", "--time", "3"], ["atur", "--izin"]):
            k, out, err = jalan(1, *argv, home=home, masukan="kunci-uji-123456789\n")
            self.assertEqual(k, 2, argv)
            self.assertIn("unrecognized arguments", out + err, argv)
        self.assertFalse(os.path.exists(os.path.join(home, ".komunitech")))

    def test_kunci_tidak_pernah_tercetak(self):
        s = Server(19)
        try:
            for argv in (["cek", "--json"], ["laporan-harian"], ["piutang", "--json"]):
                jalan(s.port, *argv, kunci=st.KUNCI_ADMIN, login="admin")
        finally:
            s.tutup()
        semua = "\n".join(KELUARAN)
        self.assertTrue(semua)
        for kunci in SEMUA_KUNCI:
            self.assertNotIn(kunci, semua)

    def test_tidak_ada_panggilan_hapus_di_kode(self):
        with open(SKRIP, encoding="utf-8") as f:
            kode = f.read()
        badan = kode.split('"""', 2)[2]      # lewati docstring modul
        for kata in ('"unlink"', "'unlink'", '"write"', "action_confirm", "action_post", "database/drop", "/jsonrpc"):
            self.assertNotIn(kata, badan)


# ============================================================ perbaikan 1.0.1 (temuan penguji Odoo asli 18 & 19)
class UjiPerbaikan101(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = {v: Server(v) for v in (17, 19)}

    @classmethod
    def tearDownClass(cls):
        for s in cls.s.values():
            s.tutup()

    def own(self, v, *argv):
        return jalan(self.s[v].port, *argv, kunci=st.KUNCI_SENDIRI, login="sendiri")

    def test_own_documents_penjualan_tidak_diam_diam(self):
        for v in (17, 19):
            k, out, err = self.own(v, "penjualan", "--tanggal", TGL)
            self.assertEqual(k, 9, out + err)
            self.assertIn("PERINGATAN DATA SEBAGIAN", out)
            self.assertIn("Own Documents", out)
            self.assertIn("Jumlah pesanan: 1", out)          # hanya S00102 milik bot-own
            k, out, err = self.own(v, "penjualan", "--tanggal", TGL, "--terima-sebagian", "--json")
            self.assertEqual(k, 0, err)
            d = json.loads(out)
            self.assertTrue(d["data_sebagian"])
            self.assertTrue(d["peringatan"])
            self.assertEqual(Decimal(str(d["pesanan"]["total"])), Decimal("149850"))

    def test_own_documents_cek_dan_laporan(self):
        k, out, err = self.own(19, "cek")
        self.assertEqual(k, 0, err)
        self.assertIn("- Pesanan penjualan: HANYA milik pengguna API ini", out)
        self.assertIn("PERINGATAN DATA SEBAGIAN", out)
        k, out, err = self.own(19, "laporan-harian", "--tanggal", TGL)
        self.assertEqual(k, 9, out + err)
        self.assertTrue(out.splitlines()[2].startswith("PERINGATAN DATA SEBAGIAN"), out)
        k, out, err = self.own(17, "piutang", "--per-tanggal", TGL)
        self.assertEqual(k, 9, out + err)
        self.assertIn("INV/2026/00190", out)
        self.assertNotIn("INV/2026/00170", out)

    def test_hak_penuh_tanpa_peringatan(self):
        for argv in (["penjualan", "--tanggal", TGL], ["laporan-harian", "--tanggal", TGL],
                     ["piutang", "--per-tanggal", TGL]):
            k, out, err = jalan(self.s[19].port, *argv)
            self.assertEqual(k, 0, out + err)
            self.assertNotIn("PERINGATAN", out)

    def test_has_group_tidak_ada_tidak_memblokir(self):
        s = Server(19, ["tanpa_has_group"])
        try:
            k, out, err = jalan(s.port, "cek")
            self.assertEqual(k, 0, err)
            self.assertIn("tidak bisa dipastikan", out)
            k, out, err = jalan(s.port, "penjualan", "--tanggal", TGL)
            self.assertEqual(k, 0, err)
        finally:
            s.tutup()

    def test_has_group_hanya_untuk_res_users(self):
        api = od.Odoo("http://127.0.0.1:9", "db", "x", "kunci-uji-12345678", "xmlrpc")
        api.protokol = "xmlrpc"
        with self.assertRaises(od.Gagal) as c:
            api.panggil("sale.order", "has_group", [1], group_ext_id="base.group_user")
        self.assertIn("tidak diizinkan", c.exception.pesan)

    def test_piutang_per_tanggal_lampau(self):
        data = self.s[19].t.data
        for per, total, jumlah in (("2026-09-25", Decimal("9756900"), 6), ("2026-08-15", Decimal("9268500"), 3)):
            har = harapan_piutang_lampau(data, per)
            self.assertEqual((sum(har.values()), len(har)), (total, jumlah), per)
            for v in (17, 19):
                k, out, err = jalan(self.s[v].port, "piutang", "--per-tanggal", per, "--json")
                self.assertEqual(k, 0, out + err)
                d = json.loads(out)
                self.assertEqual(Decimal(str(d["total"])), total, (v, per))
                self.assertEqual({f["nomor"]: Decimal(str(f["sisa"])) for f in d["faktur"]}, har, (v, per))
        k, out, _ = jalan(self.s[19].port, "piutang", "--per-tanggal", "2026-08-15")
        self.assertNotIn("INV/2026/00190", out)                 # terbit 10 Sep: belum ada per 15 Agu
        self.assertIn("INV/2026/00185", out)                    # dibayar 1 Sep: per 15 Agu masih penuh
        self.assertNotIn("dibayar sebagian", out)
        self.assertIn("pelunasan bertanggal setelah 2026-08-15", out)
        k, out, _ = jalan(self.s[19].port, "piutang", "--per-tanggal", "2026-09-25")
        self.assertIn("INV/2026/00193", out)                    # lunas 28 Sep: per 25 Sep masih terbuka
        self.assertNotIn("INV/2026/00194", out)                 # lunas 20 Sep
        self.assertNotIn("nota kredit belum dipakai", out)      # RINV 30 Sep belum terbit

    def test_piutang_lampau_tanpa_hak_pelunasan_kode_9(self):
        k, out, err = self.own(19, "piutang", "--per-tanggal", "2026-09-25")
        self.assertEqual(k, 9, out + err)
        self.assertIn("pelunasan setelah 2026-09-25 tidak bisa dibaca", out)

    def test_stok_masuk_terjadwal_diterangkan(self):
        k, out, _ = jalan(self.s[19].port, "stok-menipis")
        self.assertIn("Gelas Kertas 12oz (isi 50): stok 0 (HABIS), perkiraan 50, min 20, maks 100 -> saran pesan 50 "
                      "(sudah ada barang masuk terjadwal 50)", out)

    def test_env_host_diizinkan_tidak_lagi_membuka_host(self):
        k, _, err = jalan(None, "cek", "--url", "https://erp.tokosaya.test",
                          env_tambah={"ODOO_HOST_DIIZINKAN": "erp.tokosaya.test"})
        self.assertEqual(k, 2)
        self.assertIn("--izinkan-host", err)


if __name__ == "__main__":
    unittest.main(verbosity=1)
