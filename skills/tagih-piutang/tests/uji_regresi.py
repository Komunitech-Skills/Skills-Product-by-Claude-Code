#!/usr/bin/env python3
"""Uji regresi tagih-piutang. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Fokus: rekap dari CSV dan dari .xlsx yang dibaca TANPA paket tambahan (zipfile + xml saja), format yang
tidak didukung meminta CSV (bukan menginstal paket), serta hitungan satu tagihan.
Angka dihitung manual (tanggal hitung 2026-09-23):
  Toko A: 6.300.000, jatuh tempo 2026-09-05 -> terlambat 18 hari, sisa 6.300.000
  CV B  : 12.500.000 - 2.500.000 = 10.000.000, jatuh tempo 2026-08-24 -> terlambat 30 hari
  Total piutang = 16.300.000.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(AKAR, "scripts", "hitung_telat.py")
TGL = "2026-09-23"


def buat_xlsx(path, baris, pakai_shared=True, nama_sheet="Piutang"):
    """Buat .xlsx minimal (sheet1) dengan library standar. Angka ditulis sebagai sel angka,
    tanggal sebagai serial Excel (angka) agar pembacaan serial ikut diuji."""
    shared, sel_xml = [], []
    for r, b in enumerate(baris, 1):
        sel = []
        for c, v in enumerate(b):
            ref = "{}{}".format(chr(65 + c), r)
            if isinstance(v, (int, float)):
                sel.append('<c r="{}"><v>{}</v></c>'.format(ref, v))
            elif pakai_shared:
                shared.append(v)
                sel.append('<c r="{}" t="s"><v>{}</v></c>'.format(ref, len(shared) - 1))
            else:
                sel.append('<c r="{}" t="inlineStr"><is><t>{}</t></is></c>'.format(ref, v))
        sel_xml.append('<row r="{}">{}</row>'.format(r, "".join(sel)))
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("xl/workbook.xml",
                   '<workbook {} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                   '<sheets><sheet name="Catatan" sheetId="2" r:id="rId2"/><sheet name="{}" sheetId="1" r:id="rId1"/>'
                   '</sheets></workbook>'.format(ns, nama_sheet))
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
                   '<Relationship Id="rId2" Target="worksheets/sheet2.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", "<worksheet {}><sheetData>{}</sheetData></worksheet>"
                   .format(ns, "".join(sel_xml)))
        z.writestr("xl/worksheets/sheet2.xml", '<worksheet {}><sheetData><row r="1"><c r="A1" t="inlineStr">'
                   '<is><t>catatan saja</t></is></c></row></sheetData></worksheet>'.format(ns))
        if pakai_shared:
            z.writestr("xl/sharedStrings.xml", "<sst {}>{}</sst>".format(
                ns, "".join("<si><t>{}</t></si>".format(s) for s in shared)))


KEPALA = ["pelanggan", "no_invoice", "nominal", "jatuh_tempo", "dibayar"]
# serial Excel: 2026-09-05 = 46270, 2026-08-24 = 46258
DATA_XLSX = [KEPALA, ["Toko A", "INV-01", 6300000, 46270, 0], ["CV B", "INV-02", 12500000, 46258, 2500000]]


class Uji(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def jalan(self, *argv):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        p = subprocess.run([sys.executable, SCRIPT] + list(argv), capture_output=True, text=True, env=env)
        return p.returncode, p.stdout, p.stderr

    def rekap(self, path, *extra):
        kode, out, err = self.jalan("--file", path, "--tanggal", TGL, "--format", "json", *extra)
        self.assertEqual(kode, 0, err)
        return json.loads(out)

    def cek_rekap(self, h):
        self.assertEqual(h["total_piutang"], 16300000)
        d = {x["pelanggan"]: x for x in h["daftar"]}
        self.assertEqual(d["Toko A"]["hari_terlambat"], 18)
        self.assertEqual(d["Toko A"]["jatuh_tempo"], "2026-09-05")
        self.assertEqual(d["CV B"]["sisa"], 10000000)
        self.assertEqual(d["CV B"]["hari_terlambat"], 30)
        self.assertEqual(h["baris_dilewati"], [])

    def test_csv(self):
        f = os.path.join(self.dir, "piutang.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("pelanggan,no_invoice,nominal,jatuh_tempo,dibayar\n"
                     "Toko A,INV-01,6300000,2026-09-05,\nCV B,INV-02,\"Rp 12.500.000\",24/08/2026,2500000\n")
        self.cek_rekap(self.rekap(f))

    def test_xlsx_shared_strings(self):
        f = os.path.join(self.dir, "piutang.xlsx")
        buat_xlsx(f, DATA_XLSX)
        self.cek_rekap(self.rekap(f, "--sheet", "piutang"))

    def test_xlsx_inline_dan_tanpa_ekstensi(self):
        f = os.path.join(self.dir, "piutang_tanpa_ekstensi")
        buat_xlsx(f, DATA_XLSX, pakai_shared=False)
        self.cek_rekap(self.rekap(f, "--sheet", "Piutang"))

    def test_xlsx_sheet_tidak_ada(self):
        f = os.path.join(self.dir, "piutang.xlsx")
        buat_xlsx(f, DATA_XLSX)
        kode, _, err = self.jalan("--file", f, "--sheet", "Juli", "--tanggal", TGL)
        self.assertNotEqual(kode, 0)
        self.assertIn("Sheet yang tersedia: Catatan, Piutang", err)

    def test_xlsx_rusak_minta_csv(self):
        f = os.path.join(self.dir, "rusak.xlsx")
        with open(f, "wb") as fh:
            fh.write(b"bukan zip")
        kode, _, err = self.jalan("--file", f, "--tanggal", TGL)
        self.assertNotEqual(kode, 0)
        self.assertIn("CSV UTF-8", err)

    def test_xls_lama_minta_csv_tanpa_instal(self):
        f = os.path.join(self.dir, "lama.xls")
        with open(f, "wb") as fh:
            fh.write(b"\xd0\xcf\x11\xe0")
        kode, _, err = self.jalan("--file", f, "--tanggal", TGL)
        self.assertNotEqual(kode, 0)
        self.assertIn("CSV UTF-8", err)
        self.assertIn("paket tidak boleh diinstal", err)

    def test_script_tanpa_paket_luar(self):
        with open(SCRIPT, encoding="utf-8") as fh:
            isi = fh.read()
        for terlarang in ("import openpyxl", "import pandas", "pip install", "subprocess"):
            self.assertNotIn(terlarang, isi)

    def test_satu_tagihan_denda(self):
        # 10.000.000 x 0,1% x (30 - 3) hari = 270.000
        kode, out, err = self.jalan("--nominal", "Rp 12.500.000", "--dibayar", "Rp 2.500.000",
                                    "--jatuh-tempo", "2026-08-24", "--tanggal", TGL, "--sudah-diingatkan", "2",
                                    "--denda-persen", "0,1", "--denda-per", "hari", "--tenggang", "3",
                                    "--denda-maks", "5%", "--dasar-denda", "PO", "--format", "json")
        self.assertEqual(kode, 0, err)
        h = json.loads(out)
        self.assertEqual(h["denda"], 270000)
        self.assertEqual(h["total_ditagih"], 10270000)



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "hitung_telat.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["--nominal", "1000", "--jatuh-tempo", "2026-01-01", "--tanggal", "2026-02-01", "--konfirmasi-denda"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60, cwd=t)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
