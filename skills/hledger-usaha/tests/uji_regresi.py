#!/usr/bin/env python3
"""Uji regresi hledger_usaha.py.

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)

Tanpa hledger: semua uji pembaca bawaan jalan; uji yang butuh hledger dilewati (SKIP).
Dengan hledger (di PATH atau ENV HLEDGER=/path/hledger): angka laporan dicocokkan dengan
`hledger is/bs/bal -O json` (verifikasi independen), aturan bank diuji silang, dan pemulihan file
saat `hledger check` gagal diuji dengan pembungkus hledger palsu.
"""
import csv
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

SINI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(SINI)
SKRIP = os.path.join(SKILL, "scripts", "hledger_usaha.py")
DATA = os.path.join(SINI, "data")
EMKM = os.path.join(SKILL, "..", "laporan-keuangan-emkm", "scripts", "laporan_emkm.py")
HLEDGER = os.environ.get("HLEDGER") or shutil.which("hledger")

sys.path.insert(0, os.path.join(SKILL, "scripts"))
import hledger_usaha as hu  # noqa: E402


def jalan(*arg, mesin="bawaan", hledger=None, masukan=None):
    cmd = [sys.executable, SKRIP] + list(arg)
    if arg and arg[0] not in ("--versi",):
        cmd += ["--mesin", mesin]
        if hledger:
            cmd += ["--hledger", hledger]
    env = dict(os.environ)
    env.pop("LEDGER_FILE", None)
    if mesin == "bawaan":
        env.pop("HLEDGER", None)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env, input=masukan)
    return r.returncode, r.stdout, r.stderr


def isi(path):
    with open(path, "rb") as f:
        return f.read()


class Dasar(unittest.TestCase):
    MESIN = "bawaan"

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji-hledger-usaha-")
        self.j = os.path.join(self.tmp, "Pembukuan", "usaha.journal")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_(self, *arg, **kw):
        kw.setdefault("mesin", self.MESIN)
        if kw["mesin"] != "bawaan":
            kw.setdefault("hledger", HLEDGER)
        return jalan(*arg, **kw)

    def buku_september(self):
        k, o, e = self.run_("init", "--jurnal", self.j, "--nama", "Kopi Sari", "--bank", "BCA")
        self.assertEqual(k, 0, e)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--jenis", "saldo-awal", "--tanggal", "2026-08-31",
                            "--posting", "Aset:Kas=2.000.000", "--posting", "Aset:Bank:BCA=10.000.000",
                            "--posting", "Aset:Persediaan=3.000.000", "--posting", "Utang:Bank=-5.000.000", "--ya")
        self.assertEqual(k, 0, e)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--batch", os.path.join(DATA, "batch-september.json"), "--ya")
        self.assertEqual(k, 0, e)
        k, o, e = self.run_("stok-akhir", "--jurnal", self.j, "--tanggal", "2026-09-30", "--nilai", "2.700.000", "--ya")
        self.assertEqual(k, 0, e)


# ------------------------------------------------------------------ angka

class UjiAngka(unittest.TestCase):
    def test_nominal_sah(self):
        kasus = {"150000": 150000, "150.000": 150000, "Rp 1.500.000": 1500000, "1,5jt": 1500000,
                 "1,5 juta": 1500000, "150rb": 150000, "2 miliar": 2000000000, "Rp 1.250,50": Decimal("1250.50"),
                 "1.000.000,-": 1000000, "750rb": 750000, "1,500,000": 1500000, "12,5": Decimal("12.5")}
        for t, harap in kasus.items():
            self.assertEqual(hu.parse_nominal(t), Decimal(harap), t)

    def test_nominal_ditolak(self):
        for t in ("62,500", "1.5", "1.50", "abc", "", "-5000", "5m", "1,234.50", "1.000,505", "2000000000000",
                  "1..000"):
            with self.assertRaises(hu.Gagal, msg=t):
                hu.parse_nominal(t)
        self.assertEqual(hu.parse_nominal("-5.000", boleh_negatif=True), Decimal(-5000))

    def test_format_rupiah(self):
        self.assertEqual(hu.rp(Decimal("1500000")), "Rp 1.500.000")
        self.assertEqual(hu.rp(Decimal("-1234.56")), "-Rp 1.234,56")
        self.assertEqual(hu.rp(Decimal("0.5")), "Rp 0,50")
        self.assertEqual(hu.rp(Decimal("100"), tanda_plus=True), "+Rp 100")

    def test_tanggal(self):
        self.assertEqual(hu.parse_tanggal("25/09/2026").isoformat(), "2026-09-25")
        self.assertEqual(hu.parse_tanggal("1 Okt 2026").isoformat(), "2026-10-01")
        self.assertEqual(hu.parse_tanggal("01/10", tahun_default=2026).isoformat(), "2026-10-01")
        for t in ("31/02/2026", "besok lusa", "2026-13-01"):
            with self.assertRaises(hu.Gagal, msg=t):
                hu.parse_tanggal(t)
        self.assertEqual(hu.parse_bulan("September 2026")[1].isoformat(), "2026-09-30")
        self.assertEqual(hu.parse_bulan("02/2028")[1].isoformat(), "2028-02-29")

    def test_bagi_proporsional_tanpa_sisa(self):
        h = hu.bagi_proporsional(Decimal("100"), [Decimal(1), Decimal(1), Decimal(1)])
        self.assertEqual(sum(h), Decimal(100))


# ------------------------------------------------------------------ pembaca jurnal

class UjiPembaca(unittest.TestCase):
    def baca(self, teks):
        return hu.parse_jurnal(teks)

    def test_template_valid(self):
        with open(hu.TEMPLATE_JURNAL, encoding="utf-8") as f:
            j = self.baca(f.read())
        self.assertEqual(j.gol("Aset:Bank:BCA"), "kas")
        self.assertEqual(j.gol("HPP:Pembelian"), "hpp")
        self.assertEqual(j.gol("Beban:Gaji"), "beban")
        self.assertEqual(j.gol("Utang:Usaha:Toko A"), "utang")
        self.assertEqual(j.gol("Modal:Prive"), "modal")

    def test_tidak_seimbang(self):
        with self.assertRaises(hu.Gagal) as c:
            self.baca("decimal-mark ,\n2026-09-01 x\n    Aset:Kas  Rp 100\n    Modal  -Rp 90\n")
        self.assertIn("tidak seimbang", str(c.exception))
        self.assertIn("baris 2", str(c.exception))

    def test_directive_asing_minta_hledger(self):
        with self.assertRaises(hu.Gagal) as c:
            self.baca("decimal-mark ,\ninclude lain.journal\n")
        self.assertIn("hledger", str(c.exception))
        self.assertEqual(c.exception.kode, hu.K_JURNAL)

    def test_saldo_assertion(self):
        dasar = "decimal-mark ,\n2026-09-01 a\n    Aset:Kas  Rp 1.000,50\n    Modal\n"
        self.baca(dasar + "2026-09-02 b\n    Aset:Kas  Rp 0 = Rp 1.000,50\n    Modal  Rp 0\n")
        with self.assertRaises(hu.Gagal) as c:
            self.baca(dasar + "2026-09-02 b\n    Aset:Kas  Rp 0 = Rp 999\n    Modal  Rp 0\n")
        self.assertIn("pengecekan saldo gagal", str(c.exception))

    def test_crlf_dan_komentar(self):
        t = "decimal-mark ,\r\n; komentar\r\n2026-09-01 * (01) Jual ; pihak:Bu Sari\r\n    Aset:Kas    Rp 5.000 ; x\r\n" \
            "    Pendapatan:Penjualan\r\n"
        j = self.baca(t)
        self.assertEqual(j.txns[0].postings[1][1], Decimal(-5000))
        self.assertEqual(j.txns[0].tags.get("pihak"), "Bu Sari")

    def test_tanpa_rp_dan_mata_uang_lain(self):
        with self.assertRaises(hu.Gagal):
            self.baca("decimal-mark ,\n2026-09-01 x\n    Aset:Kas  100\n    Modal\n")
        with self.assertRaises(hu.Gagal):
            self.baca("decimal-mark ,\ncommodity USD 1.000,00\n")
        with self.assertRaises(hu.Gagal):
            self.baca("decimal-mark ,\n2026-09-01 x\n    Aset:Kas  Rp 1 @ USD 2\n    Modal\n")

    def test_tanggal_mustahil(self):
        with self.assertRaises(hu.Gagal):
            self.baca("decimal-mark ,\n2026-02-30 x\n    Aset:Kas  Rp 1\n    Modal\n")


# ------------------------------------------------------------------ alur bawaan (tanpa hledger)

class UjiAlurBawaan(Dasar):
    MESIN = "bawaan"

    def test_init_tidak_menimpa(self):
        self.assertEqual(self.run_("init", "--jurnal", self.j, "--nama", "A")[0], 0)
        sebelum = isi(self.j)
        k, o, e = self.run_("init", "--jurnal", self.j, "--nama", "B")
        self.assertEqual(k, 2)
        self.assertIn("sudah ada", e)
        self.assertEqual(isi(self.j), sebelum)

    def test_pratinjau_tidak_menulis_lalu_simpan(self):
        self.run_("init", "--jurnal", self.j)
        sebelum = isi(self.j)
        arg = ["catat", "--jurnal", self.j, "--jenis", "jual", "--nominal", "75rb", "--via", "kas",
               "--tanggal", "2026-09-01", "--ket", "Jual kopi; 3 cup | meja 2"]
        k, o, e = self.run_(*arg)
        self.assertEqual(k, 0, e)
        self.assertIn("BELUM disimpan", o)
        self.assertEqual(isi(self.j), sebelum)
        k, o, e = self.run_(*(arg + ["--ya"]))
        self.assertEqual(k, 0, e)
        teks = isi(self.j).decode()
        self.assertIn("2026-09-01 Jual kopi, 3 cup / meja 2", teks)   # ; dan | dinetralkan
        self.assertIn("Rp 75.000", teks)
        # dobel ditolak
        k, o, e = self.run_(*(arg + ["--ya"]))
        self.assertEqual(k, 7)
        self.assertIn("KEMUNGKINAN DOBEL", o)
        self.assertEqual(self.run_(*(arg + ["--ya", "--tetap-catat"]))[0], 0)

    def test_salah_ketik_akun(self):
        self.run_("init", "--jurnal", self.j)
        sebelum = isi(self.j)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--jenis", "beban", "--nominal", "10000", "--via", "kas",
                            "--akun", "Beban:Listrik Air Internt", "--ya")
        self.assertEqual(k, 2)
        self.assertIn("Beban:Listrik Air Internet", e)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--jenis", "beban", "--nominal", "10000", "--via", "kas",
                            "--akun", "Aset:Kas", "--ya")
        self.assertEqual(k, 2)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--jenis", "bebas", "--ket", "x", "--posting",
                            "Harta:Kas=5", "--posting", "Aset:Kas", "--akun-baru", "--ya")
        self.assertEqual(k, 2)
        self.assertIn("akun utama", e)
        self.assertEqual(isi(self.j), sebelum)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--jenis", "beban", "--nominal", "10000", "--via", "kas",
                            "--akun", "Beban:Kebersihan", "--akun-baru", "--ya")
        self.assertEqual(k, 0, e)
        self.assertIn("account Beban:Kebersihan", isi(self.j).decode())

    def test_input_buruk(self):
        self.run_("init", "--jurnal", self.j)
        sebelum = isi(self.j)
        for arg, kata in ((["--jenis", "jual", "--nominal", "62,500", "--via", "kas"], "ambigu"),
                          (["--jenis", "jual", "--nominal", "-5000", "--via", "kas"], "negatif"),
                          (["--jenis", "jual", "--nominal", "5000"], "--via belum diisi"),
                          (["--jenis", "terbang", "--nominal", "5000"], "tidak dikenal"),
                          (["--jenis", "jual", "--nominal", "5000", "--via", "kas", "--tanggal", "31/02/2026"],
                           "kalender"),
                          (["--jenis", "bebas", "--ket", "x", "--posting", "Aset:Kas=5", "--posting",
                            "Modal:Setoran=-4"], "tidak seimbang"),
                          (["--jenis", "transfer", "--nominal", "5", "--dari", "kas", "--ke", "kas"], "sama")):
            k, o, e = self.run_("catat", "--jurnal", self.j, "--ya", *arg)
            self.assertEqual(k, 2, arg)
            self.assertIn(kata, e, arg)
        self.assertEqual(isi(self.j), sebelum)
        # batch dengan satu entri rusak: tidak ada yang tertulis
        p = os.path.join(self.tmp, "b.json")
        with open(p, "w") as f:
            json.dump([{"jenis": "jual", "nominal": "5000", "via": "kas"},
                       {"jenis": "jual", "nominal": "lima ribu", "via": "kas"}], f)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--batch", p, "--ya")
        self.assertEqual(k, 2)
        self.assertIn("Transaksi ke-2", e)
        self.assertEqual(isi(self.j), sebelum)
        with open(p, "w") as f:
            f.write("{rusak")
        self.assertEqual(self.run_("catat", "--jurnal", self.j, "--batch", p, "--ya")[0], 2)

    def test_jurnal_tidak_ada(self):
        k, o, e = self.run_("laba-rugi", "--jurnal", os.path.join(self.tmp, "tidak-ada.journal"))
        self.assertEqual(k, 3)
        self.assertIn("init", e)

    def test_jurnal_rusak_tidak_ditulisi(self):
        self.run_("init", "--jurnal", self.j)
        with open(self.j, "a", encoding="utf-8") as f:
            f.write("\n2026-09-01 rusak\n    Aset:Kas  Rp 100\n    Modal:Setoran  -Rp 90\n")
        sebelum = isi(self.j)
        k, o, e = self.run_("catat", "--jurnal", self.j, "--jenis", "jual", "--nominal", "1000", "--via", "kas", "--ya")
        self.assertEqual(k, 4)
        self.assertIn("tidak seimbang", e)
        self.assertEqual(isi(self.j), sebelum)

    def test_laporan_september(self):
        self.buku_september()
        k, o, e = self.run_("bulanan", "--jurnal", self.j, "--bulan", "2026-09", "--json")
        self.assertEqual(k, 0, e)
        d = json.loads(o)
        lr, n, ak = d["laba_rugi"], d["neraca"], d["arus_kas"]
        self.assertEqual(lr["total_pendapatan"], 8800000)
        self.assertEqual(lr["total_hpp"], 3800000)   # 2jt + 1,5jt + penyesuaian stok 300rb
        self.assertEqual(lr["total_beban"], 3400000)
        self.assertEqual(lr["laba_bersih"], 1600000)
        self.assertEqual(n["total_aset"], 17200000)
        self.assertEqual(n["total_utang"], 6100000)
        self.assertEqual(n["total_modal"], 11100000)
        self.assertEqual(n["selisih"], 0)
        self.assertEqual(ak["kas_awal"], 12000000)
        self.assertEqual(ak["kas_akhir"], 10000000)
        self.assertTrue(ak["cocok"])
        self.assertEqual(ak["operasi"]["neto"], 3400000)
        self.assertEqual(ak["investasi"]["neto"], -4500000)
        self.assertEqual(ak["pendanaan"]["neto"], -900000)
        self.assertIn("LABA BERSIH: Rp 1.600.000 (18,2% dari pendapatan)", d["teks"])
        # transfer kas->bank tidak dihitung masuk/keluar
        self.assertNotIn("Aset:Kas", json.dumps(ak["operasi"]))

    def test_saldo_nyata(self):
        self.buku_september()
        k, o, e = self.run_("saldo", "--jurnal", self.j, "--tanggal", "2026-09-30", "--nyata", "Aset:Kas=1.400.000")
        self.assertEqual(k, 0, e)
        self.assertIn("COCOK", o)
        k, o, e = self.run_("saldo", "--jurnal", self.j, "--tanggal", "2026-09-30", "--nyata", "Aset:Kas=1.350.000")
        self.assertEqual(k, 1)
        self.assertIn("SELISIH Rp 50.000 (catatan lebih besar", o)
        k, o, e = self.run_("saldo", "--jurnal", self.j, "Aset:Kass")
        self.assertEqual(k, 2)
        self.assertIn("Aset:Kas", e)

    def test_stok_akhir_sama(self):
        self.buku_september()
        k, o, e = self.run_("stok-akhir", "--jurnal", self.j, "--tanggal", "2026-09-30", "--nilai", "2.700.000")
        self.assertEqual(k, 0)
        self.assertIn("Sudah sama", o)

    def test_impor_bank_bca(self):
        self.buku_september()
        m = os.path.join(DATA, "mutasi-bca-okt.csv")
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, m)
        self.assertEqual(k, 2)
        self.assertIn("--tahun", e)
        sebelum = isi(self.j)
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, m, "--tahun", "2026")
        self.assertEqual(k, 0, e)
        self.assertEqual(isi(self.j), sebelum)
        self.assertIn("Terbaca 12 transaksi", o)
        self.assertIn("Uang masuk Rp 3.891.734,56 | uang keluar Rp 8.800.500", o)
        self.assertIn("3 transaksi belum dikelompokkan", o)
        self.assertIn("COCOK. Setelah impor", o)
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, m, "--tahun", "2026", "--tetapkan", "99=HPP:Pembelian")
        self.assertEqual(k, 2)
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, m, "--tahun", "2026", "--tetapkan", "10=HPP:Pembelian",
                            "--ya")
        self.assertEqual(k, 0, e)
        k, o, e = self.run_("saldo", "--jurnal", self.j, "--tanggal", "2026-10-31", "--nyata",
                            "Aset:Bank:BCA=3.691.234,56")
        self.assertEqual(k, 0, o + e)
        # impor ulang: semua dilewati
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, m, "--tahun", "2026", "--ya")
        self.assertIn("12 sudah pernah diimpor", o)
        self.assertIn("Tidak ada transaksi baru", o)
        # tarik tunai = pindah dana (kas), bukan beban
        j = hu.parse_jurnal(isi(self.j).decode())
        tarik = [t for t in j.txns if "TARIKAN ATM" in t.ket][0]
        self.assertIn("Aset:Kas", [a for a, _ in tarik.postings])

    def test_impor_bank_rusak(self):
        self.run_("init", "--jurnal", self.j, "--bank", "Mandiri")
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, os.path.join(DATA, "mutasi-mandiri-rusak.csv"))
        self.assertEqual(k, 0, e)
        self.assertIn("Terbaca 3 transaksi", o)
        self.assertIn("tanggal tidak dikenali: tanggal-rusak", o)
        self.assertIn("nominal 0/kosong", o)
        self.assertIn("masuk dan keluar sekaligus", o)
        self.assertIn("tidak konsisten", o)
        self.assertIn("Aset:Kas", o)          # setor tunai
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, os.path.join(DATA, "mutasi-tanpa-dk.csv"))
        self.assertEqual(k, 2)
        self.assertIn("CR/DB", e)
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, os.path.join(DATA, "mutasi-excel.xlsx"))
        self.assertEqual(k, 2)
        self.assertIn("Excel", e)
        kosong = os.path.join(self.tmp, "kosong.csv")
        open(kosong, "w").close()
        self.assertEqual(self.run_("impor-bank", "--jurnal", self.j, kosong)[0], 2)

    def test_tambah_aturan(self):
        self.run_("init", "--jurnal", self.j, "--bank", "BCA")
        aturan = os.path.join(os.path.dirname(self.j), "aturan-bank.rules")
        sebelum = isi(aturan)
        k, o, e = self.run_("tambah-aturan", "--jurnal", self.j, "--kata", "AB", "--akun", "HPP:Pembelian")
        self.assertEqual(k, 2)
        k, o, e = self.run_("tambah-aturan", "--jurnal", self.j, "--kata", "ROASTERY (GAYO)", "--akun",
                            "HPP:Pembelian", "--arah", "keluar")
        self.assertEqual(k, 0)
        self.assertEqual(isi(aturan), sebelum)
        self.run_("tambah-aturan", "--jurnal", self.j, "--kata", "ROASTERY (GAYO)", "--akun", "HPP:Pembelian",
                  "--arah", "keluar", "--ya")
        self.assertIn("ROASTERY \\(GAYO\\)", isi(aturan).decode())
        blok = hu.baca_aturan(aturan)
        r = {"tanggal": hu.parse_tanggal("2026-10-01"), "ket": "TRF ROASTERY (GAYO) OKT", "masuk": Decimal(0),
             "keluar": Decimal(5), "saldo": None, "ref": "x"}
        self.assertEqual(hu.kelompokkan(blok, r), "HPP:Pembelian")
        r["masuk"], r["keluar"] = Decimal(5), Decimal(0)
        self.assertEqual(hu.kelompokkan(blok, r), "Pendapatan:Belum Dikelompokkan")

    def test_ekspor_emkm(self):
        self.buku_september()
        out = os.path.join(self.tmp, "kas.csv")
        k, o, e = self.run_("ekspor-emkm", "--jurnal", self.j, "--bulan", "2026-09", "--keluar", out, "--json")
        self.assertEqual(k, 0, e)
        d = json.loads(o)
        with open(out, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 10)
        kode = {r["Keterangan"]: r["Kategori"] for r in rows}
        self.assertEqual(kode["Prive (ambil untuk pribadi)"], "prive")
        self.assertEqual(kode["Grinder kopi"], "aset_tetap")
        self.assertEqual(kode["Angsuran pinjaman (Bunga)"], "beban_keuangan")
        self.assertEqual(kode["Angsuran pinjaman (Bank)"], "bayar_pinjaman")
        self.assertEqual(d["saldo"]["persediaan-akhir"], 2700000)
        self.assertEqual(d["saldo"]["utang-usaha-akhir"], 1500000)
        self.assertEqual(self.run_("ekspor-emkm", "--jurnal", self.j, "--bulan", "2026-09", "--keluar", out)[0], 2)
        if not os.path.isfile(EMKM):
            self.skipTest("skill laporan-keuangan-emkm tidak ada di sebelah skill ini")
        arg = [sys.executable, EMKM, out, "--format", "json", "--periode-awal", "2026-09-01", "--periode-akhir",
               "2026-09-30"]
        for kunci, v in d["saldo"].items():
            arg += ["--" + kunci, str(v)]
        r = subprocess.run(arg, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        teks = r.stdout
        self.assertIn("1600000", teks.replace(".", ""))   # laba bersih sama dengan hledger-usaha
        self.assertIn("17200000", teks.replace(".", ""))  # total aset sama

    def test_backup(self):
        self.buku_september()
        k, o, e = self.run_("backup", "--jurnal", self.j)
        self.assertEqual(k, 0, e)
        salinan = [x for x in os.listdir(os.path.join(os.path.dirname(self.j), "backup"))]
        self.assertEqual(len(salinan), 2)
        jr = [x for x in salinan if x.endswith(".journal")][0]
        self.assertEqual(isi(os.path.join(os.path.dirname(self.j), "backup", jr)), isi(self.j))

    def test_cek_tanpa_jurnal(self):
        k, o, e = self.run_("cek", "--jurnal", self.j)
        self.assertEqual(k, 3)
        self.assertIn("BELUM ADA", o)


# ------------------------------------------------------------------ dengan hledger asli

@unittest.skipUnless(HLEDGER, "hledger tidak terpasang (set ENV HLEDGER=/path/hledger)")
class UjiHledgerAsli(Dasar):
    MESIN = "hledger"

    def hl(self, *arg):
        r = subprocess.run([HLEDGER, "-n", "-f", self.j] + list(arg), capture_output=True, text=True,
                           encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    @staticmethod
    def angka_json(am):
        tot = Decimal(0)
        for a in am:
            q = a["aquantity"]
            tot += Decimal(q["decimalMantissa"]).scaleb(-q["decimalPlaces"])
        return tot

    def test_template_lulus_check_strict(self):
        self.run_("init", "--jurnal", self.j)
        self.hl("check", "accounts")

    def test_laporan_sama_dengan_hledger(self):
        self.buku_september()
        self.hl("check", "accounts")
        k, o, e = self.run_("bulanan", "--jurnal", self.j, "--bulan", "2026-09", "--json")
        self.assertEqual(k, 0, e)
        d = json.loads(o)
        self.assertIn("Uji silang pembaca bawaan: COCOK", d["catatan"])
        # laba rugi: bandingkan dengan `hledger is -O json` (verifikasi independen)
        isj = json.loads(self.hl("is", "-p", "2026-09", "-O", "json"))
        laba_hl = self.angka_json(isj["cbrTotals"]["prrTotal"])
        self.assertEqual(Decimal(d["laba_rugi"]["laba_bersih"]), laba_hl)
        # total aset & utang: `hledger bs -O json`
        bs = json.loads(self.hl("bs", "-e", "2026-10-01", "-O", "json"))
        sub = {s[0]: self.angka_json(s[1]["prTotals"]["prrTotal"]) for s in bs["cbrSubreports"]}
        aset = [v for k2, v in sub.items() if "sset" in k2][0]
        utang = [v for k2, v in sub.items() if "iabil" in k2][0]
        self.assertEqual(Decimal(d["neraca"]["total_aset"]), aset)
        self.assertEqual(Decimal(d["neraca"]["total_utang"]), utang)
        # perubahan kas: `hledger cf`
        cf = json.loads(self.hl("cf", "-p", "2026-09", "-O", "json"))
        self.assertEqual(Decimal(d["arus_kas"]["perubahan_kas"]), self.angka_json(cf["cbrTotals"]["prrTotal"]))

    def test_impor_bank_uji_silang(self):
        self.buku_september()
        k, o, e = self.run_("impor-bank", "--jurnal", self.j, os.path.join(DATA, "mutasi-bca-okt.csv"), "--tahun",
                            "2026", "--ya")
        self.assertEqual(k, 0, e)
        self.assertIn("Uji silang aturan dengan hledger: COCOK (12 baris)", o)
        bal = self.hl("bal", "Aset:Bank:BCA", "-e", "2026-11-01", "-O", "json")
        self.assertEqual(self.angka_json(json.loads(bal)[1]), Decimal("3691234.56"))
        # file mutasi rapi + aturan bisa dibaca hledger langsung
        self.hl("check")

    def test_pulihkan_bila_hledger_check_gagal(self):
        self.buku_september()
        palsu = os.path.join(self.tmp, "hledger-palsu.py")
        with open(palsu, "w") as f:
            f.write("#!{}\nimport os, sys\nif 'check' in sys.argv:\n    sys.stderr.write('hledger: Error: uji\\n')\n"
                    "    sys.exit(1)\nos.execv({!r}, [{!r}] + sys.argv[1:])\n".format(sys.executable, HLEDGER, HLEDGER))
        os.chmod(palsu, os.stat(palsu).st_mode | stat.S_IEXEC)
        sebelum = isi(self.j)
        k, o, e = jalan("catat", "--jurnal", self.j, "--jenis", "jual", "--nominal", "1000", "--via", "kas", "--ya",
                        mesin="hledger", hledger=palsu)
        self.assertEqual(k, 6, o + e)
        self.assertIn("dikembalikan seperti semula", e)
        self.assertEqual(isi(self.j), sebelum)

    def test_jurnal_rusak_dilaporkan_hledger(self):
        self.run_("init", "--jurnal", self.j)
        with open(self.j, "a", encoding="utf-8") as f:
            f.write("\n2026-09-01 rusak\n    Aset:Kas  Rp 100\n    Modal:Setoran  -Rp 90\n")
        k, o, e = self.run_("laba-rugi", "--jurnal", self.j)
        self.assertEqual(k, 4)
        self.assertIn("hledger menolak", e)


if __name__ == "__main__":
    unittest.main(verbosity=1)
