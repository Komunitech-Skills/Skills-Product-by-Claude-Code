#!/usr/bin/env python3
"""Uji regresi analisis-excel.

Fixture XLSX dibuat programatik dengan zipfile (tanpa openpyxl) agar tes tidak butuh paket apa pun.
Angka yang diharapkan dihitung ulang secara independen di tes (Fraction / penjumlahan manual),
bukan disalin dari keluaran script.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import csv
import json
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from datetime import date
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from xml.sax.saxutils import escape

SINI = Path(__file__).resolve().parent.parent
SCRIPT = SINI / "scripts" / "analisis.py"
sys.path.insert(0, str(SINI / "scripts"))
import analisis as modul  # noqa: E402


# ---------------------------------------------------------------------------
# Pembuat XLSX minimal (independen dari script)
# ---------------------------------------------------------------------------

NS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" ' \
     'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


def serial_excel(d):
    """Serial 1900 untuk tanggal >= 1 Mar 1900 (independen: hitung hari sejak 30 Des 1899)."""
    return (d - date(1899, 12, 30)).days


def kolom_huruf(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def buat_xlsx(path, sheets, date1904=False):
    """sheets: list dict {nama, baris: [[sel...]], gabung: ["A1:E1"], hidden, tanpa_ref}.

    Sel: None | str (shared string) | int/float/str-angka via ("n", "123.4") | ("tgl", serial)
    | ("tglc", serial) format kustom dd/mm/yyyy | ("f", "D6*5000", nilai_atau_None) | ("e", "#DIV/0!")
    | ("inline", "teks") | ("b", True).
    """
    shared, idx_shared = [], {}

    def si(t):
        if t not in idx_shared:
            idx_shared[t] = len(shared)
            shared.append(t)
        return idx_shared[t]

    sheet_xml = []
    for sh in sheets:
        rows_xml = []
        for ri, row in enumerate(sh["baris"], start=1):
            cells = []
            for ci, v in enumerate(row):
                if v is None:
                    continue
                ref = "" if sh.get("tanpa_ref") else ' r="{}{}"'.format(kolom_huruf(ci), ri)
                if isinstance(v, str):
                    cells.append('<c{} t="s"><v>{}</v></c>'.format(ref, si(v)))
                elif isinstance(v, (int, float)):
                    cells.append("<c{}><v>{}</v></c>".format(ref, v))
                elif v[0] == "n":
                    cells.append("<c{}><v>{}</v></c>".format(ref, v[1]))
                elif v[0] == "tgl":
                    cells.append('<c{} s="1"><v>{}</v></c>'.format(ref, v[1]))
                elif v[0] == "tglc":
                    cells.append('<c{} s="2"><v>{}</v></c>'.format(ref, v[1]))
                elif v[0] == "f":
                    isi = "<f>{}</f>".format(escape(v[1])) + ("<v>{}</v>".format(v[2]) if v[2] is not None else "")
                    cells.append("<c{}>{}</c>".format(ref, isi))
                elif v[0] == "e":
                    cells.append('<c{} t="e"><v>{}</v></c>'.format(ref, escape(v[1])))
                elif v[0] == "inline":
                    cells.append('<c{} t="inlineStr"><is><t>{}</t></is></c>'.format(ref, escape(v[1])))
                elif v[0] == "b":
                    cells.append('<c{} t="b"><v>{}</v></c>'.format(ref, 1 if v[1] else 0))
            rows_xml.append('<row r="{}">{}</row>'.format(ri, "".join(cells)))
        gab = ""
        if sh.get("gabung"):
            gab = '<mergeCells count="{}">{}</mergeCells>'.format(
                len(sh["gabung"]), "".join('<mergeCell ref="{}"/>'.format(g) for g in sh["gabung"]))
        sheet_xml.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                         '<worksheet {}><sheetData>{}</sheetData>{}</worksheet>'.format(NS, "".join(rows_xml), gab))
    wb = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook {}>{}<sheets>{}</sheets></workbook>'
          .format(NS, '<workbookPr date1904="1"/>' if date1904 else "<workbookPr/>",
                  "".join('<sheet name="{}" sheetId="{}" r:id="rId{}"{}/>'.format(
                      escape(sh["nama"]), i + 1, i + 1, ' state="hidden"' if sh.get("hidden") else "")
                      for i, sh in enumerate(sheets))))
    rels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships '
            'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{}</Relationships>'.format(
                "".join('<Relationship Id="rId{0}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        'relationships/worksheet" Target="worksheets/sheet{0}.xml"/>'.format(i + 1)
                        for i in range(len(sheets)))))
    sst = ('<?xml version="1.0" encoding="UTF-8"?><sst {} count="{}" uniqueCount="{}">{}</sst>'.format(
        NS, len(shared), len(shared),
        # satu string disimpan sebagai rich-text run + teks fonetik (harus diabaikan)
        "".join(("<si><r><t>{}</t></r><rPh sb=\"0\" eb=\"1\"><t>FONETIK</t></rPh></si>" if t == "Teh Manis"
                 else "<si><t xml:space=\"preserve\">{}</t></si>").format(escape(t)) for t in shared)))
    styles = ('<?xml version="1.0" encoding="UTF-8"?><styleSheet {}><numFmts count="1">'
              '<numFmt numFmtId="164" formatCode="dd/mm/yyyy;@"/></numFmts>'
              '<cellXfs count="3"><xf numFmtId="0"/><xf numFmtId="14"/><xf numFmtId="164"/></cellXfs>'
              '</styleSheet>'.format(NS))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types '
                   'xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", rels)
        z.writestr("xl/sharedStrings.xml", sst)
        z.writestr("xl/styles.xml", styles)
        for i, x in enumerate(sheet_xml):
            z.writestr("xl/worksheets/sheet{}.xml".format(i + 1), x)


def jalankan(*argv, cwd=None):
    r = subprocess.run([sys.executable, str(SCRIPT), *map(str, argv)], cwd=cwd, capture_output=True,
                       text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


def jalankan_json(test, *argv):
    code, out, err = jalankan(*argv, "--json")
    test.assertEqual(code, 0, err)
    test.assertNotIn("Traceback", err)
    return json.loads(out)


def D(x):
    return Decimal(str(x))


# Data penjualan fixture (dipakai beberapa tes). Nilai Total valid, dihitung independen:
T = {"r4": 30000, "r5": 15000, "r6": 15000, "r7": 60000, "r10": Fraction(250001, 2)}  # 125000,5


def sheet_penjualan():
    return {
        "nama": "Penjualan",
        "baris": [
            ["Laporan Penjualan Toko Maju — Agustus s.d. September 2026"],
            [],
            ["Tanggal", "Cabang", "Produk", "Qty", "Total"],
            [("tgl", serial_excel(date(2026, 8, 5))), "Bandung", "Kopi Susu", 2, 30000],
            [("tgl", serial_excel(date(2026, 8, 17))), None, " kopi  susu ", 1, 15000],
            [("tglc", serial_excel(date(2026, 9, 2))), None, "Teh Manis", 3, ("f", "D6*5000", 15000)],
            [("tgl", serial_excel(date(2026, 9, 10))), "Jakarta", "Kopi Susu", 4, 60000],
            [("tgl", serial_excel(date(2026, 9, 15))), "Jakarta", "Roti Bakar", 1, ("f", "D8*12000", None)],
            [("tgl", serial_excel(date(2026, 9, 20))), "Jakarta", "Teh Manis", 2, ("e", "#DIV/0!")],
            [("tgl", serial_excel(date(2026, 9, 25))), ("inline", "Bogor"), "Roti Bakar", 5, ("n", "125000.5")],
            ["Total", None, None, 18, ("f", "SUM(E4:E10)", "245000.5")],
        ],
        "gabung": ["A1:E1", "B4:B6"],
    }


def sheet_bug1900():
    return {"nama": "Bug1900", "tanpa_ref": True,
            "baris": [["Tanggal", "Nilai"],
                      [("tgl", 59), 1], [("tgl", 60), 2], [("tgl", 61), 3], [("tgl", 1), 4],
                      [("tgl", "45925.75"), 5]]}


class UjiXlsx(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.xlsx = self.dir / "toko.xlsx"
        buat_xlsx(self.xlsx, [sheet_penjualan(), sheet_bug1900(),
                              {"nama": "Arsip", "hidden": True, "baris": [["A", "B"], ["x", 1]]}])

    def tearDown(self):
        self.tmp.cleanup()

    def test_daftar_sheet(self):
        d = jalankan_json(self, "daftar", self.xlsx)
        nama = [r[1] for r in d["tabel"][0]["baris"]]
        self.assertEqual(nama, ["Penjualan", "Bug1900", "Arsip"])
        self.assertEqual(d["tabel"][0]["baris"][2][2], "tersembunyi")

    def test_header_baris_3_merge_formula_galat_total(self):
        d = jalankan_json(self, "pivot", self.xlsx, "--grup", "Cabang", "--nilai", "Total")
        self.assertEqual(d["baris_header"], 3)
        rows = {r[0]: Decimal(r[2]) for r in d["tabel"][0]["baris"]}
        # Bandung dari sel gabungan B4:B6 = r4 + r5 + r6
        self.assertEqual(rows["Bandung"], D(T["r4"] + T["r5"] + T["r6"]))
        self.assertEqual(rows["Jakarta"], D(T["r7"]))            # r8 rumus kosong, r9 galat -> tidak dihitung
        self.assertEqual(rows["Bogor"], Decimal("125000.5"))
        total = sum(T.values())
        self.assertEqual(rows["TOTAL"], Decimal(total.numerator) / Decimal(total.denominator))
        teks = " ".join(d["peringatan"])
        self.assertIn("rumus tanpa nilai tersimpan", teks)
        self.assertIn("E8", teks)
        self.assertIn("galat Excel", teks)
        self.assertIn("baris 11", teks)                         # baris Total dilewati
        self.assertIn("B4:B6", teks)                            # sel gabungan dilaporkan
        self.assertIn("3 sheet", teks)

    def test_kategori_digabung_dan_rich_text(self):
        d = jalankan_json(self, "pivot", self.xlsx, "--grup", "Produk", "--nilai", "Qty")
        rows = {r[0]: Decimal(r[2]) for r in d["tabel"][0]["baris"]}
        self.assertEqual(rows["Kopi Susu"], D(2 + 1 + 4))      # ' kopi  susu ' digabung
        self.assertEqual(rows["Teh Manis"], D(3 + 2))          # rich text + rPh diabaikan
        self.assertNotIn("FONETIK", json.dumps(d))

    def test_tren_bulan_dan_periode_tidak_penuh(self):
        d = jalankan_json(self, "tren", self.xlsx, "--nilai", "Total")
        rows = d["tabel"][0]["baris"]
        self.assertEqual([r[0] for r in rows], ["Agu 2026", "Sep 2026"])
        agu = D(T["r4"] + T["r5"])
        sep = Decimal(T["r6"] + T["r7"]) + Decimal("125000.5")
        self.assertEqual(Decimal(rows[0][2]), agu)
        self.assertEqual(Decimal(rows[1][2]), sep)
        # persen perubahan dihitung independen dengan Fraction
        p = (Fraction(sep) - Fraction(agu)) / Fraction(agu) * 100
        self.assertAlmostEqual(float(Decimal(rows[1][3])), float(p), places=9)
        self.assertTrue(any("Agu 2026 tidak penuh" in x for x in d["peringatan"]))
        self.assertTrue(any("Sep 2026 tidak penuh" in x for x in d["peringatan"]))

    def test_banding_periode(self):
        d = jalankan_json(self, "banding", self.xlsx, "--nilai", "Total", "--periode-a", "2026-08",
                          "--periode-b", "Sep 2026", "--grup", "Cabang")
        rows = {r[0]: r for r in d["tabel"][0]["baris"]}
        self.assertEqual(Decimal(rows["TOTAL"][1]), D(45000))
        self.assertEqual(Decimal(rows["TOTAL"][2]), Decimal("200000.5"))
        self.assertEqual(Decimal(rows["TOTAL"][3]), Decimal("155000.5"))
        self.assertIn("naik 344,4%", " ".join(d["temuan"]))    # 155000,5/45000 = 344,445%
        self.assertIsNone(rows["Bogor"][4])                    # dari 0 -> persen tidak dihitung

    def test_bug_1900_dan_tanpa_ref(self):
        d = jalankan_json(self, "ringkas", self.xlsx, "--sheet", "Bug1900")
        tgl = d["tabel"][1]["baris"][0]
        self.assertEqual(tgl[1], "1 Jan 1900")                  # serial 1
        self.assertEqual(tgl[2], "25 Sep 2025")                 # 45925,75 -> 25 Sep 2025 (jam diabaikan)
        self.assertTrue(any("29-Feb-1900" in x for x in d["peringatan"]))
        # unit: 59 -> 28 Feb 1900, 61 -> 1 Mar 1900
        self.assertEqual(modul.serial_ke_tanggal(Decimal(59)), date(1900, 2, 28))
        self.assertIsNone(modul.serial_ke_tanggal(Decimal(60)))
        self.assertEqual(modul.serial_ke_tanggal(Decimal(61)), date(1900, 3, 1))
        self.assertEqual(modul.serial_ke_tanggal(Decimal(serial_excel(date(2026, 9, 25)))), date(2026, 9, 25))
        self.assertEqual(modul.serial_ke_tanggal(Decimal(0), date1904=True), date(1904, 1, 1))

    def test_sheet_nomor_dan_tidak_ada(self):
        d = jalankan_json(self, "profil", self.xlsx, "--sheet", "2")
        self.assertIn("Bug1900", d["sumber"])
        code, out, err = jalankan("profil", self.xlsx, "--sheet", "Rekap")
        self.assertEqual(code, 2)
        self.assertIn("Sheet 'Rekap' tidak ada", err)
        self.assertIn("Penjualan", err)
        self.assertNotIn("Traceback", err)

    def test_kolom_tidak_ada(self):
        code, _o, err = jalankan("pivot", self.xlsx, "--grup", "Kota", "--nilai", "Total")
        self.assertEqual(code, 2)
        self.assertIn("Kolom grup 'Kota' tidak ada", err)
        self.assertIn("Cabang", err)

    def test_date1904_dan_noise_float(self):
        p = self.dir / "mac.xlsx"
        buat_xlsx(p, [{"nama": "S", "baris": [["Tgl", "Nilai"], [("tgl", 0), ("n", "0.1")],
                                              [("tgl", 1), ("n", "0.30000000000000004")]]}], date1904=True)
        d = jalankan_json(self, "ringkas", p)
        angka = d["tabel"][0]["baris"][0]
        self.assertEqual(Decimal(angka[2]), Decimal("0.4"))     # 0,1 + 0,3 tepat (Decimal, 15 digit)
        self.assertEqual(d["tabel"][1]["baris"][0][1], "1 Jan 1904")

    def test_xlsx_rusak(self):
        for nama, isi in [("rusak.xlsx", b"ini bukan excel sama sekali"),
                          ("lama.xls", b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 100)]:
            p = self.dir / nama
            p.write_bytes(isi)
            code, _o, err = jalankan("profil", p)
            self.assertEqual(code, 2, nama)
            self.assertNotIn("Traceback", err)
        p = self.dir / "zip.xlsx"
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("halo.txt", "x")
        code, _o, err = jalankan("profil", p)
        self.assertEqual(code, 2)
        self.assertIn("workbook.xml", err)
        p = self.dir / "potong.xlsx"
        p.write_bytes(self.xlsx.read_bytes()[:300])
        code, _o, err = jalankan("profil", p)
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)
        # XML sheet rusak
        p = self.dir / "xmlrusak.xlsx"
        buat_xlsx(p, [{"nama": "S", "baris": [["A"], [1]]}])
        with zipfile.ZipFile(p) as zin:
            isi = {n: zin.read(n) for n in zin.namelist()}
        isi["xl/worksheets/sheet1.xml"] = b"<worksheet><sheetData><row>"
        with zipfile.ZipFile(p, "w") as z:
            for n, b in isi.items():
                z.writestr(n, b)
        code, _o, err = jalankan("profil", p)
        self.assertEqual(code, 2)
        self.assertIn("rusak", err)


class UjiCsv(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def tulis(self, nama, teks, encoding="utf-8"):
        p = self.dir / nama
        p.write_bytes(teks.encode(encoding))
        return p

    def test_cp1252_titikkoma_format_indonesia(self):
        teks = ("Rekap Kas Toko Sembako Bu Tini\r\n"
                "Dicetak: 26/09/2026\r\n"
                "Tanggal;Kategori;Keterangan;Nominal\r\n"
                "25/09/2026;Belanja ;Beras 25 kg – Cianjur;Rp 1.234.567,89\r\n"
                "25 Sep 2026;belanja;Minyak;\"Rp 250.000\"\r\n"
                "2026-09-26;Gaji;Karyawan;Rp 2.500.000,-\r\n"
                "27/09/2026;GAJI;Bonus;(100.000)\r\n"
                "28/09/2026;Listrik;Token PLN;0,5\r\n"
                "Jumlah;;;Rp 3.884.568,39\r\n")
        p = self.tulis("kas.csv", teks, "cp1252")
        d = jalankan_json(self, "pivot", p, "--grup", "kategori", "--nilai", "nominal")
        rows = {r[0]: Decimal(r[2]) for r in d["tabel"][0]["baris"]}
        self.assertEqual(rows["belanja"] if "belanja" in rows else rows["Belanja"],
                         Decimal("1234567.89") + Decimal("250000"))
        gaji = [k for k in rows if k.lower() == "gaji"]
        self.assertEqual(len(gaji), 1)
        self.assertEqual(rows[gaji[0]], Decimal("2500000") - Decimal("100000"))
        self.assertEqual(rows["Listrik"], Decimal("0.5"))
        self.assertEqual(rows["TOTAL"], Decimal("1234567.89") + 250000 + 2500000 - 100000 + Decimal("0.5"))
        self.assertEqual(d["baris_header"], 3)
        teks_p = " ".join(d["peringatan"])
        self.assertIn("cp1252", teks_p)
        self.assertIn("baris 9", teks_p)                        # baris Jumlah dilewati

    def test_bom_tab_dan_tanggal_campur(self):
        teks = "﻿Tanggal\tProduk\tQty\n2026-09-25\tA\t1\n25 September 2026\tB\t2\n26/09/2026\tA\t3\n"
        p = self.tulis("tab.csv", teks)
        d = jalankan_json(self, "tren", p, "--nilai", "Qty", "--per", "hari")
        rows = d["tabel"][0]["baris"]
        self.assertEqual([r[0] for r in rows], ["25 Sep 2026", "26 Sep 2026"])
        self.assertEqual([Decimal(r[2]) for r in rows], [D(3), D(3)])

    def test_urutan_tanggal_ambigu(self):
        p = self.tulis("amb.csv", "Tgl,Nilai\n01/02/2026,1\n03/04/2026,2\n")
        d = jalankan_json(self, "tren", p, "--nilai", "Nilai")
        self.assertEqual(d["tabel"][0]["baris"][0][0], "Feb 2026")
        self.assertTrue(any("ambigu" in x for x in d["peringatan"]))
        d = jalankan_json(self, "tren", p, "--nilai", "Nilai", "--urutan-tanggal", "mdy")
        self.assertEqual(d["tabel"][0]["baris"][0][0], "Jan 2026")

    def test_profil_duplikat_outlier_sensitif(self):
        rows = ["Nama,No HP,Kota,Belanja"]
        nilai = [100000, 120000, 110000, 95000, 105000, 115000, 98000, 5000000]
        for i, v in enumerate(nilai):
            rows.append("Pelanggan {},08123456{:03d},Bandung,{}".format(i, i, v))
        rows.append(rows[1])  # duplikat
        p = self.tulis("pel.csv", "\n".join(rows) + "\n")
        d = jalankan_json(self, "profil", p)
        kol = {r[0]: r for r in d["tabel"][0]["baris"]}
        self.assertEqual(kol["No HP"][1], "kode")               # nol di depan -> kode, bukan angka
        self.assertIn("disembunyikan", kol["No HP"][7])
        self.assertEqual(d["duplikat"], 1)
        out = d["tabel"][1]["baris"][0]
        self.assertEqual(out[0], "Belanja")
        self.assertEqual(Decimal(out[2]), 1)
        self.assertIn("5.000.000", out[3])
        self.assertTrue(any("DATA PRIBADI" in x for x in d["peringatan"]))
        # batas outlier independen: QUARTILE.INC
        s = sorted(nilai + [nilai[0]])
        def q(p_):
            h = (len(s) - 1) * p_
            lo = int(h)
            return s[lo] + (s[lo + 1] - s[lo]) * (h - lo)
        q1, q3 = q(Fraction(1, 4)), q(Fraction(3, 4))
        atas = q3 + Fraction(3, 2) * (q3 - q1)
        self.assertIn(modul.fmt_uang(Decimal(atas.numerator) / Decimal(atas.denominator)), out[1])

    def test_top_pareto_dan_lainnya(self):
        rows = ["Produk,Omzet"] + ["P{},{}".format(i, v) for i, v in
                                    enumerate([500, 300, 100, 50, 30, 20], 1)]
        p = self.tulis("p.csv", "\n".join(rows))
        d = jalankan_json(self, "top", p, "--grup", "Produk", "--nilai", "Omzet", "--n", "3")
        t = d["tabel"][0]["baris"]
        self.assertEqual([r[1] for r in t[:3]], ["P1", "P2", "P3"])
        self.assertEqual(Decimal(t[1][5]), Decimal(800) / Decimal(1000) * 100)
        self.assertEqual(Decimal(t[3][3]), D(100))              # Lainnya = 50+30+20
        self.assertIn("P1, P2", " ".join(d["temuan"]))

    def test_pivot_silang_dan_rata(self):
        teks = "Bulan,Cabang,Produk,Nilai\n2026-09-01,A,x,10\n2026-09-02,A,y,20\n2026-09-03,B,x,30\n2026-09-04,B,x,50\n"
        p = self.tulis("s.csv", teks)
        d = jalankan_json(self, "pivot", p, "--grup", "Cabang", "--kolom-pivot", "Produk", "--nilai", "Nilai")
        t = {r[0]: r for r in d["tabel"][0]["baris"]}
        self.assertEqual(d["tabel"][0]["kolom"], ["Cabang", "x", "y", "Total"])
        self.assertEqual(Decimal(t["B"][1]), D(80))
        self.assertIsNone(t["B"][2])
        self.assertEqual(Decimal(t["TOTAL"][3]), D(110))
        d = jalankan_json(self, "pivot", p, "--grup", "Cabang", "--nilai", "Nilai", "--fungsi", "rata")
        t = {r[0]: r for r in d["tabel"][0]["baris"]}
        self.assertEqual(Decimal(t["B"][2]), D(40))
        self.assertEqual(Decimal(t["TOTAL"][2]), Decimal(110) / 4)

    def test_filter_dan_dari_sampai(self):
        teks = "Tanggal,Cabang,Nilai\n2026-07-31,A,1\n2026-08-01,A,2\n2026-08-31,B,4\n2026-09-01,A,8\n"
        p = self.tulis("f.csv", teks)
        d = jalankan_json(self, "ringkas", p, "--dari", "2026-08", "--sampai", "2026-08", "--filter", "cabang=a")
        self.assertEqual(Decimal(d["tabel"][0]["baris"][0][2]), D(2))

    def test_banding_dua_file(self):
        a = self.tulis("agustus.csv", "Produk,Omzet\nKopi,100\nTeh,50\nRoti,0\n")
        b = self.tulis("september.csv", "produk;omzet\nkopi;\"150\"\nTeh;25\nDonat;10\n")
        d = jalankan_json(self, "banding", a, "--file-b", b, "--nilai", "Omzet", "--grup", "Produk")
        t = {r[0]: r for r in d["tabel"][0]["baris"]}
        self.assertEqual(Decimal(t["Kopi"][4]), D(50))           # (150-100)/100
        self.assertEqual(Decimal(t["Teh"][4]), D(-50))
        self.assertEqual(Decimal(t["TOTAL"][1]), D(150))
        self.assertEqual(Decimal(t["TOTAL"][2]), D(185))
        self.assertIn("Donat", " ".join(d["temuan"]))

    def test_bersihkan_dan_formula_injection(self):
        teks = ("Tanggal;Pelanggan;Kategori;Harga\n"
                "25/09/2026;  Budi  ;Makanan ;Rp 1.500,50\n"
                "25 Sep 2026;=HYPERLINK(\"http://x\");makanan;2.000\n"
                "25 Sep 2026;=HYPERLINK(\"http://x\");makanan;2.000\n"
                "26/09/2026;Ani;MINUMAN;abc\n")
        p = self.tulis("kotor.csv", teks)
        keluar = self.dir / "bersih.csv"
        d = jalankan_json(self, "bersihkan", p, "--keluar", keluar, "--buang-duplikat")
        with open(keluar, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["Tanggal", "Pelanggan", "Kategori", "Harga"])
        self.assertEqual(rows[1], ["2026-09-25", "Budi", "makanan", "1500.5"])
        self.assertEqual(rows[2][1], "'=HYPERLINK(\"http://x\")")
        self.assertEqual(rows[2][3], "2000")
        self.assertEqual(len(rows), 4)                          # 1 duplikat dibuang
        self.assertEqual(rows[3][3], "abc")                     # nilai tidak valid dibiarkan
        self.assertTrue(any("tidak valid" in r[2] for r in d["tabel"][0]["baris"]))
        # --excel-id: ; dan koma desimal
        k2 = self.dir / "bersih-id.csv"
        jalankan_json(self, "bersihkan", p, "--keluar", k2, "--excel-id")
        isi = k2.read_text(encoding="utf-8-sig")
        self.assertIn("25/09/2026;Budi;makanan;1500,5", isi)
        # tidak menimpa file asli
        code, _o, err = jalankan("bersihkan", p, "--keluar", p)
        self.assertEqual(code, 2)

    def test_keluar_csv_hasil(self):
        p = self.tulis("k.csv", "Kat,Nilai\nA,1.000\nB,2.500\nA,500\n")
        out = self.dir / "hasil.csv"
        jalankan_json(self, "pivot", p, "--grup", "Kat", "--nilai", "Nilai", "--keluar", out)
        with open(out, encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[1][:3], ["B", "1", "2500"])
        self.assertEqual(rows[-1][0], "TOTAL")
        self.assertEqual(rows[-1][2], "4000")

    def test_markdown_default(self):
        p = self.tulis("m.csv", "Kat,Harga\nA,\"Rp 1.234.567\"\nB,1000\n")
        code, out, err = jalankan("pivot", p, "--grup", "Kat", "--nilai", "Harga")
        self.assertEqual(code, 0, err)
        self.assertIn("| A | 1 | Rp 1.234.567 | 99,9% |", out)
        self.assertIn("### Saran grafik", out)

    def test_input_buruk_tanpa_traceback(self):
        kasus = [
            ("kosong.csv", b""),
            ("spasi.csv", b"   \n\n"),
            ("biner.csv", b"\x00\x01\x02" * 50),
            ("header_saja.csv", b"A,B,C\n"),
        ]
        for nama, isi in kasus:
            p = self.dir / nama
            p.write_bytes(isi)
            code, _o, err = jalankan("profil", p)
            self.assertEqual(code, 2, nama)
            self.assertTrue(err.startswith("GAGAL:"), nama)
            self.assertNotIn("Traceback", err, nama)
        code, _o, err = jalankan("profil", self.dir / "tidak-ada.csv")
        self.assertEqual(code, 2)
        p = self.tulis("t.csv", "Kat,Nilai\nA,x\nB,y\n")
        code, _o, err = jalankan("pivot", p, "--grup", "Kat", "--nilai", "Nilai")
        self.assertEqual(code, 2)
        self.assertIn("--tipe", err)
        code, _o, err = jalankan("banding", p, "--nilai", "Nilai")
        self.assertEqual(code, 2)
        code, _o, err = jalankan("tren", p)
        self.assertEqual(code, 2)
        self.assertIn("tanggal", err)
        p2 = self.tulis("q.csv", 'A,B\n"tidak ditutup,1\n')
        code, _o, err = jalankan("profil", p2)
        self.assertIn(code, (0, 2))
        self.assertNotIn("Traceback", err)

    def test_desimal_tepat(self):
        p = self.tulis("d.csv", "Kat;Nilai\nA;0,1\nB;0,2\n")
        d = jalankan_json(self, "ringkas", p)
        self.assertEqual(Decimal(d["tabel"][0]["baris"][0][2]), Decimal("0.3"))


class UjiParseAngka(unittest.TestCase):
    def test_format(self):
        kasus = {
            "1.234.567,89": "1234567.89", "Rp 15.000": "15000", "Rp. 25000": "25000", "IDR 25.000": "25000",
            "Rp 15.000,-": "15000", "15,000.50": "15000.50", "(5.000)": "-5000", "-Rp 5.000": "-5000",
            "Rp -5.000": "-5000", "5.000-": "-5000", "0,5": "0.5", "12,5%": "12.5", "1 234 567": "1234567",
            " Rp 1.000 ": "1000", "15000": "15000", "1.250.000": "1250000",
        }
        for teks, harap in kasus.items():
            self.assertEqual(modul.parse_angka(teks), Decimal(harap), teks)
        for teks in ["1.5E+06", "15.000.00", "15000.500", "abc", "Rp", "1.2.3", "US$ 5", "12-5"]:
            self.assertIsNone(modul.parse_angka(teks), teks)
        self.assertEqual(modul.parse_angka("1,234", "id"), Decimal("1.234"))
        self.assertEqual(modul.parse_angka("1,234", "en"), Decimal("1234"))
        self.assertIsNone(modul.parse_angka("1,234.5", "id"))

    def test_tanggal(self):
        kasus = {"25/09/2026": date(2026, 9, 25), "25 Sep 2026": date(2026, 9, 25),
                 "2026-09-25": date(2026, 9, 25), "Kamis, 25 September 2026": date(2026, 9, 25),
                 "25-Sep-26": date(2026, 9, 25), "Sep 25, 2026": date(2026, 9, 25),
                 "2026-09-25 14:30:00": date(2026, 9, 25), "25.09.2026": date(2026, 9, 25),
                 "1 Agustus 2026": date(2026, 8, 1)}
        for teks, harap in kasus.items():
            self.assertEqual(modul.parse_tanggal(teks), harap, teks)
        for teks in ["31/02/2026", "kemarin", "2026"]:
            self.assertIsNone(modul.parse_tanggal(teks), teks)

    def test_periode_dan_format(self):
        self.assertEqual(modul.parse_periode("Q3 2026"), (date(2026, 7, 1), date(2026, 9, 30)))
        self.assertEqual(modul.parse_periode("2024-02"), (date(2024, 2, 1), date(2024, 2, 29)))
        self.assertEqual(modul.fmt_uang(Decimal("1234567.5")), "Rp 1.234.568")
        self.assertEqual(modul.fmt_angka(Decimal("-1234.5")), "-1.234,50")
        self.assertEqual(modul.fmt_persen(Decimal("91.65")), "91,7%")
        self.assertEqual(modul.huruf_kolom(27), "AB")
        self.assertEqual(modul.indeks_kolom("AB12"), (27, 12))


# ---------------------------------------------------------------------------
# v1.0.1 — regresi temuan uji independen (examples/HASIL-UJI.md) memakai fixture penguji
# ---------------------------------------------------------------------------

FIXTURE = SINI / "examples" / "buat_fixture_uji.py"


def angka(x):
    return None if x in (None, "") else Decimal(str(x))


class UjiTemuanV101(unittest.TestCase):
    """Fixture dari penguji independen (deterministik) + kunci jawaban yang dihitung tanpa script skill."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.fx = Path(cls.tmp.name)
        r = subprocess.run([sys.executable, str(FIXTURE), str(cls.fx)], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        cls.kunci = json.loads((cls.fx / "kunci-jawaban.json").read_text(encoding="utf-8"))
        cls.xlsx = cls.fx / "Penjualan 2026.xlsx"
        cls.lembur = cls.fx / "lembur-sep-2026.csv"
        cls.iuran = cls.fx / "iuran-komite.csv"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def pivot_map(self, d, kol_nilai=2):
        return {r[0]: angka(r[kol_nilai]) for r in d["tabel"][0]["baris"]}

    # -- pengunci angka skenario 01–03 (tidak boleh berubah) -------------
    def test_kunci_01_per_sheet_dan_banding(self):
        for q in ("Q2", "Q3"):
            d = jalankan_json(self, "pivot", self.xlsx, "--sheet", q, "--grup", "Kategori", "--nilai", "Total")
            m = self.pivot_map(d)
            harap = self.kunci["01"][q]
            self.assertEqual(m.pop("TOTAL"), D(harap["jumlah"]))
            self.assertEqual(m, {k: D(v) for k, v in harap["per_kategori"].items()})
        d = jalankan_json(self, "banding", self.xlsx, "--sheet", "Q2", "--file-b", self.xlsx, "--sheet-b", "Q3",
                          "--nilai", "Total")
        tot = d["tabel"][0]["baris"][-1]
        self.assertEqual(angka(tot[1]), D(self.kunci["01"]["Q2"]["jumlah"]))
        self.assertEqual(angka(tot[2]), D(self.kunci["01"]["Q3"]["jumlah"]))
        self.assertEqual(modul.fmt_persen(angka(tot[4])), "-28,8%")
        # temuan P3 #7: dua sheet dari file yang sama -> label = nama sheet
        self.assertEqual(d["tabel"][0]["kolom"][1:3], ["Q2", "Q3"])

    def test_kunci_02_lembur(self):
        k = self.kunci["02"]
        d = jalankan_json(self, "pivot", self.lembur, "--grup", "Divisi", "--nilai", "Jam Lembur")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["total_semua"]))
        self.assertEqual(m, {dv: D(v) for dv, v in k["total_per_divisi"].items()})
        d = jalankan_json(self, "pivot", self.lembur, "--grup", "Divisi", "--nilai", "Jam Lembur", "--fungsi", "rata")
        for dv, v in k["rata_per_baris_divisi"].items():
            self.assertEqual(round(self.pivot_map(d)[dv], 12), round(Decimal(v), 12), dv)
        d = jalankan_json(self, "top", self.lembur, "--grup", "Nama", "--nilai", "Jam Lembur", "--n", "5")
        got = [(r[1], angka(r[3])) for r in d["tabel"][0]["baris"][:5]]
        self.assertEqual(got, [(n, D(v)) for n, v in k["top5_total_karyawan"][:5]])

    def test_kunci_03_iuran(self):
        d = jalankan_json(self, "ringkas", self.iuran, "--kolom", "Nominal")
        row = d["tabel"][0]["baris"][0]
        self.assertEqual((angka(row[1]), angka(row[2])), (Decimal(89), D(self.kunci["03"]["mentah"]["jumlah"])))
        d = jalankan_json(self, "pivot", self.iuran, "--grup", "Bulan", "--nilai", "Nominal")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(self.kunci["03"]["mentah"]["jumlah"]))
        self.assertEqual(m, {b: D(v) for b, v in self.kunci["03"]["mentah"]["per_bulan"].items()})

    # -- P1-1: gabung beberapa sheet ------------------------------------
    def test_p1_sheet_semua_pivot_tren_ringkas(self):
        harap = self.kunci["01"]["semua"]
        for spec in ("semua", "Q1,Q2,Q3", "q1, Q2 ,Q3"):
            d = jalankan_json(self, "pivot", self.xlsx, "--sheet", spec, "--grup", "Kategori", "--nilai", "Total")
            m = self.pivot_map(d)
            self.assertEqual(m.pop("TOTAL"), D(harap["jumlah"]), spec)
            self.assertEqual(m, {k: D(v) for k, v in harap["per_kategori"].items()}, spec)
            self.assertEqual(d["jumlah_baris_data"], harap["baris"])
        teks = " ".join(d["peringatan"])
        for q in ("Q1", "Q2", "Q3"):                              # baris TOTAL dibuang per sheet
            self.assertRegex(teks, r"baris {}:\d+ \(rumus agregat \(E\d+: =SUM\(".format(q))
        self.assertEqual(len(d["baris_dikeluarkan"]), 3)
        self.assertEqual(d["kemungkinan_ringkasan"], [])
        self.assertIn("rumus tanpa nilai", teks)
        self.assertIn("gabungan sheet Q1 + Q2 + Q3", d["sumber"])
        d = jalankan_json(self, "pivot", self.xlsx, "--sheet", "semua", "--grup", "Sheet", "--nilai", "Total")
        m = self.pivot_map(d)
        for q in ("Q1", "Q2", "Q3"):
            self.assertEqual(m[q], D(self.kunci["01"][q]["jumlah"]))
        self.assertIn("Master Barang", " ".join(d["catatan"]))   # sheet tersembunyi tidak ikut
        for f in ("Penjualan 2026.xlsx", "Penjualan 2026 (1904).xlsx"):
            d = jalankan_json(self, "tren", self.fx / f, "--sheet", "semua", "--nilai", "Total")
            got = [angka(r[2]) for r in d["tabel"][0]["baris"]]
            self.assertEqual(got, [D(v) for v in harap["per_bulan"].values()], f)
        d = jalankan_json(self, "ringkas", self.xlsx, "--sheet", "semua", "--kolom", "Total")
        row = d["tabel"][0]["baris"][0]
        self.assertEqual([angka(x) for x in row[1:3]], [Decimal(harap["nilai_terisi"]), D(harap["jumlah"])])
        self.assertEqual(angka(row[4]), D(harap["median"]))
        self.assertEqual((angka(row[5]), angka(row[6])), (D(harap["min"]), D(harap["max"])))
        d = jalankan_json(self, "top", self.xlsx, "--sheet", "semua", "--nilai", "Total", "--n", "1")
        self.assertRegex(d["tabel"][0]["baris"][0][1], r"^Q[123]:\d+$")   # nomor baris Sheet:baris

    def test_p1_sheet_beda_kolom(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "cabang.xlsx"
            buat_xlsx(f, [
                {"nama": "Bogor", "baris": [["Tanggal", "Produk", "Total"],
                                            [("tgl", serial_excel(date(2026, 9, 1))), "Kopi", 10000],
                                            [("tgl", serial_excel(date(2026, 9, 2))), "Teh", 5000],
                                            ["TOTAL", None, 15000]]},
                {"nama": "Depok", "baris": [["Produk", "Tanggal", "Total", "Catatan"],
                                            ["kopi", ("tgl", serial_excel(date(2026, 9, 3))), 7000, "x"],
                                            ["Jumlah", None, 7000, None]]},
                {"nama": "Stok", "baris": [["Barang", "Gudang", "Sisa"], ["Kopi", "A", 3]]},
            ])
            d = jalankan_json(self, "pivot", f, "--sheet", "semua", "--grup", "Produk", "--nilai", "Total")
            m = self.pivot_map(d)
            self.assertEqual(m, {"Kopi": Decimal(17000), "Teh": Decimal(5000), "TOTAL": Decimal(22000)})
            teks = " ".join(d["peringatan"])
            self.assertIn("Sheet 'Stok' TIDAK digabung", teks)
            self.assertIn("kolom tambahan Catatan diabaikan", teks)
            code, _o, err = jalankan("pivot", f, "--sheet", "Bogor,Tidak Ada", "--grup", "Produk")
            self.assertEqual(code, 2)
            self.assertIn("Sheet 'Tidak Ada' tidak ada", err)

    # -- P1-2: CSV tanda kutip tak tertutup ------------------------------
    def test_p1_csv_kutip_tidak_tertutup(self):
        code, out, err = jalankan("ringkas", self.fx / "kutip-rusak.csv")
        self.assertEqual(code, 2)
        self.assertIn("GAGAL: CSV rusak", err)
        self.assertIn("baris 2", err)
        self.assertNotIn("Traceback", err)
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "tengah.csv"      # kutip dibuka di baris 3 dan baru "tertutup" di baris 5
            f.write_text('Nama,Nominal\nAni,5000\n"Budi,6000\nCici,7000\nDedi",8000\nEka,9000\n', encoding="utf-8")
            code, _o, err = jalankan("ringkas", f)
            self.assertEqual(code, 2)
            self.assertIn("baris 3 s.d. 5", err)
            f = Path(t) / "akhir.csv"       # kasus di HASIL-UJI: sisa file tertelan sampai akhir
            f.write_text('Nama,Nominal\nAni,5000\n"Budi,6000\nCici,7000\nDedi,8000\n', encoding="utf-8")
            code, _o, err = jalankan("ringkas", f)
            self.assertEqual(code, 2)
            self.assertIn("tanda kutip (\") di baris 3 tidak ditutup", err)
            f = Path(t) / "alamat.csv"      # teks multi-baris yang sah tetap terbaca (dengan peringatan)
            f.write_text('Nama,Alamat,Nominal\nAni,"Jl. Merdeka 5,\nBogor",5000\nBudi,Depok,6000\n', encoding="utf-8")
            d = jalankan_json(self, "ringkas", f, "--kolom", "Nominal")
            self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), Decimal(11000))
            self.assertIn("Baris 2 s.d. 3", " ".join(d["catatan"]))            # v1.0.4: info ringan

    # -- P2 -------------------------------------------------------------
    def test_p2_baris_vs_nilai_terisi(self):
        k = self.kunci["02"]
        d = jalankan_json(self, "pivot", self.lembur, "--grup", "Divisi", "--nilai", "Jam Lembur", "--fungsi", "rata")
        t = d["tabel"][0]
        self.assertEqual(t["kolom"][-1], "Nilai terisi")
        terisi = {r[0]: int(angka(r[-1])) for r in t["baris"]}
        self.assertEqual(terisi.pop("TOTAL"), k["baris"] - k["kosong"])
        self.assertEqual(terisi, k["baris_divisi"])
        self.assertEqual(sum(int(angka(r[1])) for r in t["baris"][:-1]), k["baris"])
        self.assertIn("3 baris tanpa nilai", " ".join(d["peringatan"]))
        d = jalankan_json(self, "pivot", self.xlsx, "--sheet", "Q2", "--grup", "Kategori", "--nilai", "Total")
        self.assertEqual(angka(d["tabel"][0]["baris"][-1][-1]), Decimal(self.kunci["01"]["Q2"]["nilai_terisi"]))
        d = jalankan_json(self, "top", self.lembur, "--grup", "Divisi", "--nilai", "Jam Lembur", "--n", "2")
        self.assertEqual(d["tabel"][0]["kolom"][-1], "Nilai terisi")
        # data tanpa sel kosong: tabel tidak berubah bentuk
        d = jalankan_json(self, "pivot", self.xlsx, "--sheet", "Q1", "--grup", "Kategori", "--nilai", "Total")
        self.assertNotIn("Nilai terisi", d["tabel"][0]["kolom"])

    def test_p2_privasi_disamarkan(self):
        code, out, _e = jalankan("top", self.lembur, "--grup", "NIK", "--nilai", "Jam Lembur", "--n", "3")
        self.assertEqual(code, 0)
        self.assertNotRegex(out, r"\d{16}")
        self.assertIn("3201•", out)
        self.assertIn("DISAMARKAN", out)
        code, out, _e = jalankan("top", self.lembur, "--grup", "NIK", "--nilai", "Jam Lembur", "--n", "3",
                                 "--tampilkan-pribadi")
        self.assertRegex(out, r"\d{16}")
        self.assertIn("--tampilkan-pribadi aktif", out)
        # pivot NIK: pengelompokan tetap per NIK lengkap (38 karyawan), hanya label yang disamarkan
        d = jalankan_json(self, "pivot", self.lembur, "--grup", "NIK", "--nilai", "Jam Lembur")
        self.assertEqual(len(d["tabel"][0]["baris"]) - 1, 38)
        self.assertEqual(angka(d["tabel"][0]["baris"][-1][2]), D(self.kunci["02"]["total_semua"]))
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "karyawan.csv"
            f.write_text("Nama,Kontak,Surel,Gaji Pokok\nAni,081234567890,ani@contoh.id,5000000\n"
                         "Budi,0857-1111-2222,budi@contoh.id,6500000\nCici,+6281399998888,cici@contoh.id,4000000\n",
                         encoding="utf-8")
            code, out, _e = jalankan("top", f, "--grup", "Kontak", "--nilai", "Gaji Pokok")
            self.assertNotIn("081234567890", out)
            self.assertIn("0812•", out)
            code, out, _e = jalankan("pivot", f, "--grup", "Surel", "--nilai", "Gaji Pokok")
            self.assertNotIn("ani@contoh.id", out)
            self.assertIn("a•••@contoh.id", out)
            code, out, _e = jalankan("top", f, "--grup", "Nama", "--nilai", "Gaji Pokok")
            self.assertIn("data SENSITIF", out)
            code, out, _e = jalankan("top", f, "--nilai", "Gaji Pokok")
            self.assertIn("data SENSITIF", out)
            self.assertNotIn("081234567890", out)
        self.assertEqual(modul.samarkan("3201005625752408"), "3201•••••••••408")

    def test_p2_kategori_spasi_dan_urutan_bulan(self):
        with tempfile.TemporaryDirectory() as t:
            bersih = Path(t) / "iuran-bersih.csv"
            code, _o, err = jalankan("bersihkan", self.iuran, "--buang-duplikat", "--keluar", bersih)
            self.assertEqual(code, 0, err)
            d = jalankan_json(self, "pivot", bersih, "--grup", "Kelas", "--nilai", "Nominal", "--kolom-pivot", "Bulan")
        t = d["tabel"][0]
        self.assertEqual(t["kolom"][1:4], ["Juli", "Agustus", "September"])   # kronologis, bukan abjad
        m = {r[0]: angka(r[-1]) for r in t["baris"]}
        harap = self.kunci["03"]["tanpa_duplikat_persis"]
        self.assertEqual(set(m), {"4A", "4B", "5A", "5B", "(kosong)", "TOTAL"})   # "4 A"/"4a" tidak memecah
        self.assertEqual(m["TOTAL"], D(harap["jumlah"]))
        # 1 baris kelas kosong (siswa 4B, Rp 50.000) dilaporkan terpisah sebagai (kosong)
        self.assertEqual(m["4B"] + m["(kosong)"], D(harap["per_kelas_asli"]["4B"]))
        for kls in ("4A", "5A", "5B"):
            self.assertEqual(m[kls], D(harap["per_kelas_asli"][kls]), kls)
        d = jalankan_json(self, "pivot", self.iuran, "--grup", "Kelas", "--nilai", "Nominal")
        teks = " ".join(d["peringatan"])
        self.assertIn("'4 A'", teks)
        self.assertIn("digabung", teks)
        d = jalankan_json(self, "ringkas", self.iuran, "--filter", "Kelas=4 A", "--kolom", "Nominal")
        self.assertIn("4 A", " ".join(d["catatan"]))
        self.assertGreater(angka(d["tabel"][0]["baris"][0][1]), 10)       # semua baris 4A ikut, bukan hanya "4 A"

    def test_p2_duplikat_di_pivot_dan_top(self):
        for argv in (("pivot", self.iuran, "--grup", "Kelas", "--nilai", "Nominal"),
                     ("top", self.iuran, "--grup", "Kelas", "--nilai", "Nominal"),
                     ("ringkas", self.iuran), ("tren", self.iuran, "--nilai", "Nominal")):
            d = jalankan_json(self, *argv)
            self.assertIn("3 baris persis sama", " ".join(d["peringatan"]), argv[0])
        d = jalankan_json(self, "pivot", self.lembur, "--grup", "Divisi", "--nilai", "Jam Lembur")
        self.assertIn("1 baris persis sama", " ".join(d["peringatan"]))

    def test_p3_persen_negatif_dan_dll(self):
        d = jalankan_json(self, "pivot", self.xlsx, "--sheet", "semua", "--grup", "Kategori", "--nilai", "Total")
        self.assertIn("ada nilai negatif", " ".join(d["catatan"]))
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "x.csv"
            f.write_text("Nama,Nominal\n" + "".join("N{},{}\n".format(i, v) for i, v in enumerate(
                ["1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000", "11000",
                 "12000", "13000", "14000", "15000", "16000", "17000", "18000", "19000",
                 "\"1,5jt\"", "2 juta", "abc", "x1", "y2"])), encoding="utf-8")
            d = jalankan_json(self, "ringkas", f, "--tipe", "Nominal=angka")
            self.assertIn("5 nilai tidak bisa dibaca", " ".join(d["peringatan"]))
            self.assertIn("dll.", " ".join(d["peringatan"]))
            g = Path(t) / "lebih.csv"
            g.write_text("Nama,Nominal\nAni,5000\nBudi,Rp 6,000\n", encoding="utf-8")
            code, _o, err = jalankan("profil", g)                            # v1.0.4: invarian jumlah kolom
            self.assertEqual(code, 2)
            self.assertIn("baris 3: 3 kolom terisi, padahal judul kolom hanya 2", err)
            d = jalankan_json(self, "profil", g, "--paksa")
            self.assertIn("PERINGATAN TEGAS (--paksa): 1 baris data", " ".join(d["peringatan"]))
        d = jalankan_json(self, "profil", self.fx / "semua-teks.csv")
        self.assertNotIn("Histogram", d["saran_grafik"])


FIXTURE_ULANG = SINI / "examples" / "buat_fixture_uji_ulang.py"


class UjiTemuanV102(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.1 (N1–N8) memakai fixture penguji ke-2 + kunci jawabannya."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.fx = Path(cls.tmp.name)
        r = subprocess.run([sys.executable, str(FIXTURE_ULANG), str(cls.fx)], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        cls.kunci = json.loads((cls.fx / "kunci-ulang.json").read_text(encoding="utf-8"))
        cls.kop = cls.fx / "Koperasi Maju Bersama 2026.xlsx"
        cls.mp = cls.fx / "pesanan-marketplace-sep.csv"
        cls.ang = cls.fx / "anggota-koperasi.csv"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def pivot_map(self, d, kol_nilai=2):
        return {r[0]: angka(r[kol_nilai]) for r in d["tabel"][0]["baris"]}

    # -- pengunci angka 3 file uji ulang (tidak boleh berubah) ------------
    def test_kunci_A_koperasi_daftar_sheet(self):
        k = self.kunci["A"]
        d = jalankan_json(self, "pivot", self.kop, "--sheet", "TW1,TW2,TW3,TW4", "--grup", "Sheet", "--nilai", "Jumlah")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["jumlah_semua"]))
        self.assertEqual(m, {"TW" + q: D(v) for q, v in k["jumlah_per_tw"].items()})
        d = jalankan_json(self, "pivot", self.kop, "--sheet", "TW1,TW2,TW3,TW4", "--grup", "Akun", "--nilai", "Jumlah")
        m = self.pivot_map(d)
        m.pop("TOTAL")
        self.assertEqual(m, {a: D(v) for a, v in k["per_akun"].items()})

    def test_kunci_B_marketplace(self):
        k = self.kunci["B"]
        d = jalankan_json(self, "pivot", self.mp, "--grup", "Kota", "--nilai", "Total Bayar")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["total"]))
        self.assertEqual(m, {a: D(v) for a, v in k["per_kota"].items()})
        self.assertEqual(d["jumlah_baris_data"], k["baris"])
        d = jalankan_json(self, "top", self.mp, "--grup", "Produk", "--nilai", "Total Bayar", "--n", "5")
        got = {r[1]: angka(r[3]) for r in d["tabel"][0]["baris"][:5]}
        self.assertEqual(got, {a: D(v) for a, v in k["per_produk"].items()})
        d = jalankan_json(self, "ringkas", self.mp, "--kolom", "Total Bayar", "--sampai", "15/09/2026")
        self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), D(k["sep1_15"]))
        d = jalankan_json(self, "ringkas", self.mp, "--kolom", "Total Bayar", "--dari", "16/09/2026")
        self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), D(k["sep16_30"]))

    def test_kunci_C_anggota(self):
        k = self.kunci["C"]
        d = jalankan_json(self, "pivot", self.ang, "--grup", "Golongan", "--nilai", "Simpanan Wajib")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["wajib_total_dengan_dup"]))
        self.assertEqual(m, {g: D(v) for g, v in k["per_gol_dengan_dup"].items()})

    # -- N1 (P1): CSV sah dengan alamat multi-baris berkoma ---------------
    def test_n1_alamat_multibaris_sah_terbaca(self):
        d = jalankan_json(self, "ringkas", self.fx / "alamat-sah.csv", "--kolom", "Nominal")
        self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), Decimal(6000))
        d = jalankan_json(self, "ringkas", self.mp, "--kolom", "Total Bayar")
        self.assertFalse([p for p in d["peringatan"] if "sel multi-baris" in p])   # v1.0.4: bukan peringatan
        teks = [p for p in d["catatan"] if "sel multi-baris" in p]
        self.assertEqual(len(teks), 1)                                   # N3: satu info gabungan
        self.assertIn("15 baris berisi sel multi-baris (15 sel", teks[0])  # B3 (v1.0.3): hitung baris & sel
        self.assertIn("Baris 5 s.d. 7 di Notepad = baris 5 di Excel", teks[0])
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "dua-kolom.csv"   # 2 kolom: baris alamat berkoma tidak mirip rekaman (kolom 2 angka)
            f.write_text('Alamat,Nominal\n"Jl. A, No. 1\nKel. B, Kec. C\nKota D, 12345",1000\nJl. E,2000\n',
                         encoding="utf-8")
            d = jalankan_json(self, "ringkas", f, "--kolom", "Nominal")
            self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), Decimal(3000))
            f = Path(t) / "titikkoma.csv"
            f.write_text('Nama;Alamat;Simpanan\nAni;"Jl. X; No. 2\nKel. Y; Kec. Z";1.250.000\nBudi;Depok;500.000\n',
                         encoding="utf-8")
            d = jalankan_json(self, "ringkas", f, "--kolom", "Simpanan")
            self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), Decimal(1750000))

    def test_n1_kutip_rusak_tetap_gagal_dan_paksa(self):
        code, _o, err = jalankan("ringkas", self.fx / "kutip-tengah.csv")
        self.assertEqual(code, 2)
        self.assertIn("baris 7", err)
        code, _o, err = jalankan("ringkas", self.fx / "kutip-tertutup-jauh.csv")
        self.assertEqual(code, 2)
        self.assertIn("baris 3 s.d. 5", err)
        self.assertIn("--paksa", err)
        code, _o, err = jalankan("ringkas", self.fx / "kutip-di-akhir.csv")
        self.assertEqual(code, 2)
        self.assertIn("baris 4", err)
        self.assertNotIn("4 s.d. 4", err)                                 # N8
        # --paksa: dibaca apa adanya + peringatan (kutip tertutup jauh)
        d = jalankan_json(self, "ringkas", self.fx / "kutip-tertutup-jauh.csv", "--paksa")
        self.assertIn("--paksa", " ".join(d["peringatan"]))
        # --paksa TIDAK menolong kutip yang tak tertutup sampai akhir file
        code, _o, err = jalankan("ringkas", self.fx / "kutip-di-akhir.csv", "--paksa")
        self.assertEqual(code, 2)
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "kolom-rusak.csv"   # sel multi-baris membuat rekaman punya 4 sel dari 3 kolom
            f.write_text('Nama,Kota,Nominal\nAni,"Bogor\nx",5000,9\nBudi,Depok,6000\nCici,Solo,7000\n',
                         encoding="utf-8")
            code, _o, err = jalankan("ringkas", f)
            self.assertEqual(code, 2)
            self.assertIn("--paksa", err)
            code, _o, err = jalankan("ringkas", f, "--paksa")
            self.assertEqual(code, 0, err)

    # -- N2 (P2): --sheet semua dengan sheet Ringkasan di depan ----------
    def test_n2_acuan_sheet_terbanyak_cocok(self):
        k = self.kunci["A"]
        d = jalankan_json(self, "pivot", self.kop, "--sheet", "semua", "--grup", "Jenis", "--nilai", "Jumlah")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["jumlah_semua"]))
        self.assertEqual(m, {j: D(v) for j, v in k["per_jenis"].items()})
        self.assertIn("gabungan sheet TW1 + TW2 + TW3 + TW4", d["sumber"])
        self.assertIn("Sheet 'Ringkasan' TIDAK digabung", " ".join(d["peringatan"]))
        # v1.0.3: 'Ringkasan' kini dilewati lebih awal sebagai sheet rekap (B2), jadi TW1 langsung jadi acuan.
        self.assertIn("tampak sheet REKAP/RINGKASAN", " ".join(d["peringatan"]))
        self.assertIn("Arsip 2025", " ".join(d["catatan"]))              # tersembunyi tetap tidak ikut
        d = jalankan_json(self, "pivot", self.kop, "--sheet", "semua", "--acuan", "TW3", "--grup", "Sheet",
                          "--nilai", "Jumlah")
        self.assertEqual(self.pivot_map(d)["TOTAL"], D(k["jumlah_semua"]))
        code, _o, err = jalankan("ringkas", self.kop, "--sheet", "semua", "--acuan", "Ringkasan")
        self.assertEqual(code, 0, err)
        code, _o, err = jalankan("ringkas", self.kop, "--sheet", "TW1,TW2", "--acuan", "TW3")
        self.assertEqual(code, 2)
        self.assertIn("--acuan", err)

    # -- N3–N8 (P3) ------------------------------------------------------
    def test_n4_judul_tanpa_jumlah_jumlah(self):
        code, out, _e = jalankan("pivot", self.kop, "--sheet", "semua", "--grup", "Sheet", "--nilai", "Jumlah")
        self.assertEqual(code, 0)
        self.assertNotIn("Jumlah Jumlah", out)
        self.assertNotIn("jumlah jumlah", out)
        self.assertIn("Total kolom Jumlah", out)
        self.assertEqual(modul.buat_judul_nilai("jumlah", "Total"), "Jumlah Total")

    def test_n5_email_tersamar_tidak_kembar(self):
        self.assertEqual(modul.samarkan("anggota01@contoh.id"), "a•••01@contoh.id")
        self.assertNotEqual(modul.samarkan("anggota01@contoh.id"), modul.samarkan("anggota04@contoh.id"))
        self.assertEqual(modul.samarkan("ani@contoh.id"), "a•••@contoh.id")
        code, out, _e = jalankan("top", self.ang, "--grup", "Email", "--nilai", "Simpanan Wajib", "--n", "3")
        self.assertNotIn("anggota", out.split("Perlu diperhatikan")[0].replace("anggota-koperasi", ""))

    def test_n6_uang_lembur_sensitif_dan_simpanan_uang(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "lembur.csv"
            f.write_text("Nama,Uang Lembur\nAni,150000\nBudi,200000\n", encoding="utf-8")
            code, out, _e = jalankan("top", f, "--grup", "Nama", "--nilai", "Uang Lembur")
            self.assertIn("data SENSITIF", out)
            self.assertIn("Rp 200.000", out)
        code, out, _e = jalankan("ringkas", self.ang, "--kolom", "Simpanan Wajib")
        self.assertIn("Rp 63.350.000", out)

    def test_n7_nama_sheet_berkoma(self):
        code, _o, err = jalankan("pivot", self.fx / "semua-beda.xlsx", "--sheet", "Satu,Jan, Feb", "--grup", "Nama")
        self.assertEqual(code, 2)
        self.assertIn("mengandung koma", err)
        self.assertIn('--sheet "1,5"', err)
        d = jalankan_json(self, "ringkas", self.fx / "semua-beda.xlsx", "--sheet", "1,5", "--kolom", "Nilai")
        self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), Decimal(13))


FIXTURE_V102 = SINI / "examples" / "buat_fixture_uji_v102.py"


class UjiTemuanV103(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.2 (B1–B4) memakai fixture penguji ke-3 + kunci jawabannya (kunci-baru.json)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.fx = Path(cls.tmp.name)
        r = subprocess.run([sys.executable, str(FIXTURE_V102), str(cls.fx)], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        cls.kunci = json.loads((cls.fx / "kunci-baru.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def pivot_map(self, d, kol_nilai=2):
        return {r[0]: angka(r[kol_nilai]) for r in d["tabel"][0]["baris"]}

    def total_kolom(self, d):
        return angka(d["tabel"][0]["baris"][0][2])

    # -- pengunci angka file v1.0.2 yang benar (tidak boleh berubah) -----
    def test_kunci_F1_marketplace(self):
        k = self.kunci["F1"]
        f = self.fx / "F1-ekspor-marketplace.csv"
        d = jalankan_json(self, "pivot", f, "--grup", "Kota", "--nilai", "Total Bayar")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["total_bayar"]))
        self.assertEqual(m, {a: D(v) for a, v in k["per_kota"].items()})
        self.assertEqual(d["jumlah_baris_data"], k["baris"])
        d = jalankan_json(self, "pivot", f, "--grup", "Produk", "--nilai", "Total Bayar")
        m = self.pivot_map(d)
        m.pop("TOTAL")
        self.assertEqual(m, {a: D(v) for a, v in k["per_produk"].items()})
        d = jalankan_json(self, "ringkas", f, "--kolom", "Jumlah")
        self.assertEqual(self.total_kolom(d), D(k["qty"]))
        self.assertNotIn("PERINGATAN TEGAS", " ".join(d["peringatan"]))

    def test_kunci_F2_rekap_wa(self):
        k = self.kunci["F2"]
        f = self.fx / "F2-rekap-wa.csv"
        d = jalankan_json(self, "pivot", f, "--grup", "Pelanggan", "--nilai", "Nominal")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["total"]))
        self.assertEqual(m, {a: D(v) for a, v in k["per_pelanggan"].items()})
        self.assertEqual(d["jumlah_baris_data"], k["baris"])
        d = jalankan_json(self, "banding", f, "--nilai", "Nominal", "--periode-a", "2026-08", "--periode-b", "2026-09")
        tot = d["tabel"][0]["baris"][-1]
        self.assertEqual((angka(tot[1]), angka(tot[2])), (D(k["agu"]), D(k["sep"])))

    def test_kunci_F4_sheet_semua(self):
        k = self.kunci["F4"]
        d = jalankan_json(self, "pivot", self.fx / "F4-biaya-4-bulan.xlsx", "--sheet", "semua", "--grup", "Kategori",
                          "--kolom-pivot", "Sheet", "--nilai", "Jumlah")
        t = d["tabel"][0]
        got = {r[0]: {b: angka(r[t["kolom"].index(b)]) for b in ("Jan", "Feb", "Mar", "Apr")}
               for r in t["baris"] if r[0] in k["pivot_kat_x_sheet"]}
        self.assertEqual(got, {a: {b: D(v) for b, v in x.items()} for a, x in k["pivot_kat_x_sheet"].items()})
        self.assertEqual(d["jumlah_baris_data"], k["baris"])

    def test_kunci_F5_sel_mirip_data_sah(self):
        k = self.kunci["F5"]
        d = jalankan_json(self, "ringkas", self.fx / "F5-rincian-mirip-data.csv", "--kolom", "Total")
        self.assertEqual(self.total_kolom(d), D(k["total"]))
        self.assertEqual(d["jumlah_baris_data"], k["baris"])
        self.assertNotIn("PERINGATAN TEGAS", " ".join(d["peringatan"]))

    # -- B1 (P2): kutip nyasar menelan tepat 1 baris data ----------------
    def test_b1_satu_baris_tertelan_gagal(self):
        f = self.fx / "F3b-rusak-satu-baris.csv"
        code, _o, err = jalankan("ringkas", f)
        self.assertEqual(code, 2)
        self.assertIn("baris 7 di Notepad tampak seperti baris data utuh", err)
        self.assertIn("tidak tertutup di baris 6", err)
        self.assertIn("1 baris data HILANG", err)
        # --paksa: tetap diproses, tetapi peringatan TEGAS + berapa baris mungkin hilang
        d = jalankan_json(self, "ringkas", f, "--paksa", "--kolom", "Total")
        w = " ".join(d["peringatan"])
        self.assertIn("PERINGATAN TEGAS", w)
        self.assertIn("1 baris data HILANG", w)
        self.assertNotIn("wajar bila memang disengaja", w)
        benar = sum(i * 1000 for i in range(1, 21))
        self.assertEqual(self.total_kolom(d), D(benar - 5000))       # apa adanya: nilai baris 5 tertelan

    def test_b1_rusak_lain_tetap_gagal(self):
        code, _o, err = jalankan("ringkas", self.fx / "F3-rusak-tertutup-jauh.csv")
        self.assertEqual(code, 2)
        self.assertIn("baris 6 s.d. 10", err)
        self.assertIn("4 baris data HILANG", err)
        for extra in ((), ("--paksa",)):
            code, _o, err = jalankan("ringkas", self.fx / "F3c-rusak-terbuka.csv", *extra)
            self.assertEqual(code, 2)
            self.assertIn("baris 11", err)

    def test_b1_hitungan_baris_fisik(self):
        with tempfile.TemporaryDirectory() as t:
            # titik koma + tanggal: baris tertelan terdeteksi dari tipe kolom tanggal & angka
            f = Path(t) / "tk.csv"
            baris = ["Tanggal;Nama;Nominal"] + ["{:02d}/09/2026;Budi {};{}.000".format(i, i, i) for i in range(1, 13)]
            baris[3] = '03/09/2026;"Budi 3;3.000'
            baris[4] = '04/09/2026;Budi 4";4.000'
            f.write_text("\n".join(baris) + "\n", encoding="utf-8")
            code, _o, err = jalankan("ringkas", f)
            self.assertEqual(code, 2)
            self.assertIn("baris 5 di Notepad", err)
            self.assertIn("File berisi 13 baris", err)
            # sel multi-baris sah di kolom yang biasanya satu baris: tidak ditolak, tapi disebut "tanda kutip nyasar"
            f = Path(t) / "lunak.csv"
            baris = ["No,Nama,Nominal"] + ["{},Ani {},{}".format(i, i, i * 100) for i in range(1, 13)]
            baris[5] = '5,"Ani 5\nlantai 2",500'
            f.write_text("\n".join(baris) + "\n", encoding="utf-8")
            d = jalankan_json(self, "ringkas", f, "--kolom", "Nominal")
            self.assertEqual(self.total_kolom(d), D(sum(i * 100 for i in range(1, 13))))
            self.assertIn("Kolom 'Nama' biasanya satu baris", " ".join(d["peringatan"]))
            self.assertIn("tanda kutip (\") nyasar", " ".join(d["peringatan"]))

    # -- B2 (P2): sheet rekap ikut digabung -> total dobel ---------------
    def test_b2_rekap_mirip_dilewati(self):
        k = self.kunci["F4"]
        f = self.fx / "F4b-rekap-mirip.xlsx"
        d = jalankan_json(self, "pivot", f, "--sheet", "semua", "--grup", "Sheet", "--nilai", "Jumlah")
        m = self.pivot_map(d)
        self.assertEqual(m.pop("TOTAL"), D(k["total"]))
        self.assertEqual(m, {b: D(v) for b, v in k["per_sheet"].items()})
        w = " ".join(d["peringatan"])
        self.assertIn("Sheet 'Rekap Kategori' TIDAK digabung: tampak sheet REKAP/RINGKASAN", w)
        self.assertIn('--sertakan "Rekap Kategori"', w)
        # --sertakan memaksa ikut -> total dobel, tetapi dengan PERINGATAN dobel hitung
        d = jalankan_json(self, "pivot", f, "--sheet", "semua", "--sertakan", "Rekap Kategori", "--grup", "Sheet",
                          "--nilai", "Jumlah")
        self.assertEqual(self.pivot_map(d)["TOTAL"], D(2 * k["total"]))
        w = " ".join(d["peringatan"])
        self.assertIn("tetap digabung karena diminta", w)
        self.assertIn("kemungkinan DOBEL HITUNG", w)
        code, _o, err = jalankan("ringkas", f, "--sheet", "semua", "--sertakan", "Tidak Ada")
        self.assertEqual(code, 2)

    def buat_bulanan(self, path, ekstra):
        kat = ["Bahan", "Gaji", "Sewa"]
        data, sheets = {}, []
        for m, bl in enumerate(["Jan", "Feb", "Mar"], 1):
            rs = [["{:02d}/{:02d}/2026".format(d_, m), kat[(d_ + m) % 3], (d_ * 7 + m) * 1000] for d_ in range(1, 13)]
            data[bl] = rs
            sheets.append({"nama": bl, "baris": [["Tanggal", "Kategori", "Jumlah"]] + rs})
        per_kat = {k2: sum(x[2] for b in data for x in data[b] if x[1] == k2) for k2 in kat}
        buat_xlsx(path, sheets + ekstra(data, per_kat))
        return sum(x[2] for b in data for x in data[b])

    def test_b2_isi_menduplikasi_total(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "isi.xlsx"   # nama netral, isinya = total per kategori (judul kolom sama persis)
            total = self.buat_bulanan(f, lambda data, pk: [{"nama": "Lembar4", "baris": [
                ["Tanggal", "Kategori", "Jumlah"]] + [["31/03/2026", k2, v] for k2, v in pk.items()]}])
            d = jalankan_json(self, "pivot", f, "--sheet", "semua", "--grup", "Sheet", "--nilai", "Jumlah")
            self.assertEqual(self.pivot_map(d)["TOTAL"], D(total))
            self.assertIn("Sheet 'Lembar4' TIDAK digabung", " ".join(d["peringatan"]))
            self.assertIn("jumlah gabungan sheet lain", " ".join(d["peringatan"]))
            # daftar eksplisit: tidak dilewati, tetapi diperingatkan (nama sheet + dobel hitung umum)
            d = jalankan_json(self, "pivot", f, "--sheet", "Jan,Feb,Mar,Lembar4", "--grup", "Sheet", "--nilai", "Jumlah")
            self.assertEqual(self.pivot_map(d)["TOTAL"], D(2 * total))
            w = " ".join(d["peringatan"])
            self.assertIn("Sheet 'Lembar4' yang Anda pilih tampak sheet REKAP/RINGKASAN", w)
            self.assertIn("kemungkinan DOBEL HITUNG", w)

    def test_b2_label_per_bulan(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "label.xlsx"  # sedikit baris berlabel bulan; angkanya target (tidak sama dengan total)
            total = self.buat_bulanan(f, lambda data, pk: [{"nama": "Lembar4", "baris": [
                ["Kategori", "Tanggal", "Jumlah"], ["Januari", "01/01/2026", 500000], ["Februari", "01/02/2026", 1],
                ["Maret", "01/03/2026", 7]]}])
            d = jalankan_json(self, "pivot", f, "--sheet", "semua", "--grup", "Sheet", "--nilai", "Jumlah")
            self.assertEqual(self.pivot_map(d)["TOTAL"], D(total))
            self.assertIn("berlabel periode", " ".join(d["peringatan"]))

    def test_b2_sheet_data_biasa_tetap_digabung(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "biasa.xlsx"
            total = self.buat_bulanan(f, lambda data, pk: [])
            d = jalankan_json(self, "pivot", f, "--sheet", "semua", "--grup", "Sheet", "--nilai", "Jumlah")
            self.assertEqual(self.pivot_map(d)["TOTAL"], D(total))
            w = " ".join(d["peringatan"])
            self.assertNotIn("REKAP", w)
            self.assertNotIn("DOBEL", w)

    # -- B3, B4 (P3): kata-kata --------------------------------------------
    def test_b3_hitung_baris_dan_sel(self):
        k = self.kunci["F1"]
        d = jalankan_json(self, "ringkas", self.fx / "F1-ekspor-marketplace.csv", "--kolom", "Total Bayar")
        w = [p for p in d["catatan"] if "sel multi-baris" in p]
        self.assertEqual(len(w), 1)
        self.assertIn("35 baris berisi sel multi-baris ({} sel".format(k["sel_multibaris"]), w[0])

    def test_b4_tanpa_kolom_kolom(self):
        code, _o, err = jalankan("pivot", self.fx / "F4-biaya-4-bulan.xlsx", "--sheet", "semua", "--acuan",
                                 "Ringkasan", "--grup", "Bulan", "--nilai", "Jumlah")
        self.assertEqual(code, 2)
        self.assertNotIn("Kolom kolom", err)
        self.assertIn("Kolom nilai 'Jumlah' tidak ada", err)
        code, _o, err = jalankan("pivot", self.fx / "F5-rincian-mirip-data.csv", "--grup", "Pelanggan",
                                 "--kolom-pivot", "Kota")
        self.assertIn("Kolom pivot 'Kota' tidak ada", err)


FIXTURE_V103 = SINI / "examples" / "buat_fixture_uji_v103.py"


class UjiInvarianV104(unittest.TestCase):
    """v1.0.4: INVARIAN JUMLAH KOLOM. Setiap file fixture SEMUA penguji (uji pertama, v1.0.1, v1.0.2, v1.0.3)
    diberi hasil yang diharapkan: a = angka benar (cocok kunci penguji), b = GAGAL tegas (kode 2) dengan jalan
    keluar yang jelas. Target: 0 angka salah diam-diam, 0 file sah ditolak."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        akar = Path(cls._tmp.name)
        cls.fx, cls.kunci = {}, {}
        for nama, gen, kunci in (("u1", FIXTURE, "kunci-jawaban.json"), ("u2", FIXTURE_ULANG, "kunci-ulang.json"),
                                 ("u3", FIXTURE_V102, "kunci-baru.json"), ("u4", FIXTURE_V103, "kunci-v103.json")):
            d = akar / nama
            r = subprocess.run([sys.executable, str(gen), str(d)], capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(r.stderr)
            cls.fx[nama] = d
            cls.kunci[nama] = json.loads((d / kunci).read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def total(self, f, kolom, *extra):
        d = jalankan_json(self, "ringkas", f, "--kolom", kolom, *extra)
        baris = d["tabel"][0]["baris"][0]
        return angka(baris[2]), int(angka(baris[1])), d

    def cek_a(self, f, kolom, total, terisi=None, *extra):
        t, n, d = self.total(f, kolom, *extra)
        self.assertEqual(t, D(total), f.name)
        if terisi is not None:
            self.assertEqual(n, terisi, f.name)
        self.assertNotIn("PERINGATAN TEGAS", " ".join(d["peringatan"]), f.name)
        return d

    def cek_b(self, f, *potongan, paksa="ok"):
        code, out, err = jalankan("ringkas", f)
        self.assertEqual(code, 2, "{}: {}".format(f.name, out[:300]))
        self.assertTrue(err.startswith("GAGAL:"), err)
        self.assertNotIn("Traceback", err)
        for p in potongan:
            self.assertIn(p, err, f.name)
        code, out, err2 = jalankan("ringkas", f, "--paksa", "--json")
        if paksa == "ok":      # jalan keluar ada, dan hasilnya memuat peringatan tegas (angka mungkin salah)
            self.assertEqual(code, 0, err2)
            self.assertIn("PERINGATAN TEGAS (--paksa)", " ".join(json.loads(out)["peringatan"]))
        else:                  # kutip tak tertutup sampai akhir file: tetap GAGAL
            self.assertEqual(code, 2, f.name)
        return err

    # -- file per file: fixture uji ulang v1.0.3 ---------------------------------------------------------
    def test_v103_C_csv(self):
        fx, k = self.fx["u4"], self.kunci["u4"]
        self.cek_b(fx / "C1-kutip-awal.csv", "baris 2 s.d. 3", "1 baris data HILANG")
        self.cek_b(fx / "C2-kutip-tengah.csv", "baris 11 s.d. 13", "2 baris data HILANG")
        self.cek_b(fx / "C3-kutip-akhir.csv", "baris 21 (baris terakhir file)", paksa="gagal")
        # C4 (dulu c-): dua baris kurang kolom akibat kutip nyasar -> invarian jumlah kolom
        err = self.cek_b(fx / "C4-alamat-sah-plus-nyasar.csv", "Jumlah kolom tidak cocok di 2 baris data",
                         "baris 18 (Notepad: baris 35): hanya 2 dari 4 kolom", "baris 19 (Notepad: baris 36)")
        self.assertIn("setiap baris harus punya 4 kolom", err)
        # C5 (dulu ditolak palsu): SAH, alamat 3 baris + "50%⏎sisa" -> terbaca tanpa --paksa, hanya info ringan
        d = self.cek_a(fx / "C5-sah-alamat-3-baris.csv", "Total", k["C5"]["total"], k["C5"]["baris"])
        self.assertFalse([p for p in d["peringatan"] if "rusak" in p or "HILANG" in p])
        self.assertIn("jumlah kolomnya sudah dicek cocok", " ".join(d["catatan"]))
        self.cek_a(fx / "C6-sah-satu-catatan-mirip-data.csv", "Jumlah", k["C6"]["total"], k["C6"]["baris"])
        self.cek_a(fx / "C7-sah-catatan-baris-baru.csv", "Jumlah", k["C7"]["total"], k["C7"]["baris"])
        # C8 (dulu c = angka salah diam-diam): baris 11 hanya 3 dari 4 kolom
        self.cek_b(fx / "C8-baris-kurang-sel.csv", "Jumlah kolom tidak cocok di 1 baris data",
                   "baris 11: hanya 3 dari 4 kolom")
        code, out, _e = jalankan("ringkas", fx / "C8-baris-kurang-sel.csv", "--paksa", "--json")
        w = " ".join(json.loads(out)["peringatan"])
        self.assertIn("1 baris data jumlah kolomnya tidak sama", w)
        self.assertIn("MUNGKIN SALAH", w)

    def test_v103_X_xlsx(self):
        fx, k = self.fx["u4"], self.kunci["u4"]
        s = ("--sheet", "semua")
        self.cek_a(fx / "X1-rekap-bernama-Sheet4.xlsx", "Jumlah", k["X1"]["total"], k["X1"]["baris"], *s)
        self.cek_a(fx / "X2-rekap-bernama-Okt.xlsx", "Jumlah", k["X2"]["total"], k["X2"]["baris"], *s)
        x3 = k["X3"]
        self.cek_a(fx / "X3-Rekap-berisi-data.xlsx", "Jumlah", x3["tanpa_sertakan"]["total"],
                   x3["tanpa_sertakan"]["baris"], *s)
        self.cek_a(fx / "X3-Rekap-berisi-data.xlsx", "Jumlah", x3["dengan_sertakan"]["total"],
                   x3["dengan_sertakan"]["baris"], *s, "--sertakan", "Rekap Des")
        self.cek_a(fx / "X4-satu-bulan-kosong.xlsx", "Jumlah", k["X4"]["total"], k["X4"]["baris"], *s)
        d = self.cek_a(fx / "X5-rekap-tidak-persis.xlsx", "Jumlah", k["X5"]["total"], k["X5"]["baris"], *s)
        w = " ".join(d["peringatan"])       # B8: tidak lagi "= 10.690.000 = jumlah gabungan"
        self.assertIn("10.690.000 ≈ jumlah gabungan", w)
        self.assertIn("(10.685.000), selisih 5.000", w)
        d = jalankan_json(self, "ringkas", fx / "X1-rekap-bernama-Sheet4.xlsx", *s)
        self.assertIn("10.685.000 = jumlah gabungan", " ".join(d["peringatan"]))

    def test_b9_tren_bulan_kosong_bukan_penurunan(self):
        f = self.fx["u4"] / "X4-satu-bulan-kosong.xlsx"
        d = jalankan_json(self, "tren", f, "--sheet", "semua", "--nilai", "Jumlah")
        rows = {r[0]: r for r in d["tabel"][0]["baris"]}
        self.assertIn(rows["Feb 2026"][3], (None, ""))
        self.assertIn(rows["Mar 2026"][3], (None, ""))
        t = " ".join(d["temuan"])
        self.assertNotIn("-100", t)
        self.assertNotIn("Penurunan terbesar: Feb", t)
        self.assertIn("Periode tanpa data (ditulis 0): Feb 2026", " ".join(d["catatan"]))

    # -- fixture v1.0.2 ------------------------------------------------------------------------------------
    def test_v102_F(self):
        fx, k = self.fx["u3"], self.kunci["u3"]
        self.cek_a(fx / "F1-ekspor-marketplace.csv", "Total Bayar", k["F1"]["total_bayar"], k["F1"]["baris"])
        self.cek_a(fx / "F2-rekap-wa.csv", "Nominal", k["F2"]["total"], k["F2"]["baris"])
        self.cek_b(fx / "F3-rusak-tertutup-jauh.csv", "baris 6 s.d. 10", "4 baris data HILANG")
        self.cek_b(fx / "F3b-rusak-satu-baris.csv", "baris 6 s.d. 7", "1 baris data HILANG")   # lolos invarian
        self.cek_b(fx / "F3c-rusak-terbuka.csv", "baris 11", paksa="gagal")
        self.cek_a(fx / "F4-biaya-4-bulan.xlsx", "Jumlah", k["F4"]["total"], k["F4"]["baris"], "--sheet", "semua")
        self.cek_a(fx / "F4b-rekap-mirip.xlsx", "Jumlah", k["F4"]["total"], k["F4"]["baris"], "--sheet", "semua")
        self.cek_a(fx / "F5-rincian-mirip-data.csv", "Total", k["F5"]["total"], k["F5"]["baris"])

    # -- fixture uji ulang v1.0.1 --------------------------------------------------------------------------
    def test_v101_ulang(self):
        fx, k = self.fx["u2"], self.kunci["u2"]
        self.cek_a(fx / "alamat-sah.csv", "Nominal", 6000, 3)
        self.cek_a(fx / "pesanan-marketplace-sep.csv", "Total Bayar", k["B"]["total"], k["B"]["baris"])
        self.cek_a(fx / "anggota-koperasi.csv", "Simpanan Wajib", k["C"]["wajib_total_dengan_dup"])
        self.cek_a(fx / "Koperasi Maju Bersama 2026.xlsx", "Jumlah", k["A"]["jumlah_semua"], None,
                   "--sheet", "semua")
        self.cek_b(fx / "kutip-tengah.csv", "baris 7", paksa="gagal")
        self.cek_b(fx / "kutip-di-akhir.csv", "baris 4", paksa="gagal")
        self.cek_b(fx / "kutip-tertutup-jauh.csv", "baris 3 s.d. 5", "2 baris data HILANG")

    # -- fixture uji pertama -------------------------------------------------------------------------------
    def test_uji_pertama(self):
        fx, k = self.fx["u1"], self.kunci["u1"]
        self.cek_a(fx / "Penjualan 2026.xlsx", "Total", k["01"]["semua"]["jumlah"], k["01"]["semua"]["nilai_terisi"],
                   "--sheet", "semua")
        self.cek_a(fx / "lembur-sep-2026.csv", "Jam Lembur", Decimal(k["02"]["total_semua"]))
        self.cek_a(fx / "iuran-komite.csv", "Nominal", k["03"]["mentah"]["jumlah"], k["03"]["mentah"]["terisi"])
        self.cek_b(fx / "kutip-rusak.csv", "CSV rusak", "baris 2", paksa="gagal")

    # -- pengunci angka lama: pivot/tren yang dulu sudah cocok kunci tidak boleh berubah ---------------------
    def test_pengunci_angka_lama(self):
        k1, k2, k3 = self.kunci["u1"], self.kunci["u2"], self.kunci["u3"]

        def peta(d):
            return {r[0]: angka(r[2]) for r in d["tabel"][0]["baris"]}
        d = jalankan_json(self, "pivot", self.fx["u1"] / "Penjualan 2026.xlsx", "--sheet", "semua",
                          "--grup", "Kategori", "--nilai", "Total")
        m = peta(d)
        self.assertEqual(m.pop("TOTAL"), D(k1["01"]["semua"]["jumlah"]))
        self.assertEqual(m, {a: D(b) for a, b in k1["01"]["semua"]["per_kategori"].items()})
        d = jalankan_json(self, "pivot", self.fx["u1"] / "lembur-sep-2026.csv", "--grup", "Divisi",
                          "--nilai", "Jam Lembur")
        m = peta(d)
        m.pop("TOTAL")
        self.assertEqual(m, {a: Decimal(b) for a, b in k1["02"]["total_per_divisi"].items()})
        d = jalankan_json(self, "pivot", self.fx["u2"] / "pesanan-marketplace-sep.csv", "--grup", "Kota",
                          "--nilai", "Total Bayar")
        m = peta(d)
        m.pop("TOTAL")
        self.assertEqual(m, {a: D(b) for a, b in k2["B"]["per_kota"].items()})
        d = jalankan_json(self, "pivot", self.fx["u3"] / "F1-ekspor-marketplace.csv", "--grup", "Kota",
                          "--nilai", "Total Bayar")
        m = peta(d)
        m.pop("TOTAL")
        self.assertEqual(m, {a: D(b) for a, b in k3["F1"]["per_kota"].items()})
        d = jalankan_json(self, "pivot", self.fx["u3"] / "F2-rekap-wa.csv", "--grup", "Pelanggan",
                          "--nilai", "Nominal")
        m = peta(d)
        m.pop("TOTAL")
        self.assertEqual(m, {a: D(b) for a, b in k3["F2"]["per_pelanggan"].items()})

    # -- invarian: kasus kecil yang mudah dijelaskan ---------------------------------------------------------
    def test_invarian_padding_dan_kolom_lebih(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "padding.csv"    # sel kosong berlebih di ujung kanan (padding Excel) = boleh
            f.write_text("Nama,Nominal\nAni,5000,,\nBudi,6000\nCici,,\n", encoding="utf-8")
            self.cek_a(f, "Nominal", 11000)
            f = Path(t) / "judul-berpadding.csv"   # judul ber-padding, data tanpa padding = boleh
            f.write_text("Nama;Nominal;;\nAni;5000\nBudi;6000;;\n", encoding="utf-8")
            self.cek_a(f, "Nominal", 11000)
            f = Path(t) / "kosong-tengah.csv"      # sel kosong di tengah tetap dihitung sebagai kolom
            f.write_text("Nama,Kota,Nominal\nAni,,5000\nBudi,Depok,6000\n", encoding="utf-8")
            self.cek_a(f, "Nominal", 11000)
            f = Path(t) / "lebih.csv"              # koma di dalam angka tanpa kutip -> 3 kolom terisi dari 2
            f.write_text("Nama,Nominal\nAni,5000\nBudi,6,000\n", encoding="utf-8")
            self.cek_b(f, "baris 3: 3 kolom terisi, padahal judul kolom hanya 2")
            f = Path(t) / "judul-baris3.csv"       # judul di baris 3: baris judul di atasnya tidak diperiksa
            f.write_text("LAPORAN KAS\nSeptember 2026\nTanggal;Uraian;Masuk\n01/09/2026;Saldo;100.000\n"
                         "02/09/2026;Jual;50.000\n", encoding="utf-8")
            self.cek_a(f, "Masuk", 150000)
            f = Path(t) / "kurang.csv"
            f.write_text("Tanggal;Uraian;Masuk\n01/09/2026;Saldo;100.000\n02/09/2026;50.000\n", encoding="utf-8")
            err = self.cek_b(f, "baris 3: hanya 2 dari 3 kolom", "02/09/2026 | 50.000")
            self.assertIn("--paksa", err)


FIXTURE_V104 = SINI / "examples" / "buat_fixture_uji_v104.py"


class UjiEksporV105(unittest.TestCase):
    """v1.0.5: BLOK RINGKASAN/CATATAN & BARIS KURANG KOLOM. Fixture penguji ke-5 (ekspor nyata Indonesia).
    Hasil diharapkan per file: a = angka & jumlah baris cocok kunci penguji TANPA --paksa, b = GAGAL tegas.
    Target: 0 salah diam-diam; semua file yang dinilai (d) 'wajar diharapkan terbaca' kini (a)."""

    total = UjiInvarianV104.total
    cek_a = UjiInvarianV104.cek_a
    cek_b = UjiInvarianV104.cek_b

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.fx = Path(cls._tmp.name) / "u5"
        r = subprocess.run([sys.executable, str(FIXTURE_V104), str(cls.fx)], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        cls.k = json.loads((cls.fx / "kunci-v104.json").read_text(encoding="utf-8"))
        cls.t = Path(cls._tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    alt = None   # diisi setelah definisi kelas (cek_alt)

    def a(self, nama, kolom, total, baris, *extra):
        d = self.cek_a(self.fx / nama, kolom, total, None, *extra)
        self.assertEqual(d["jumlah_baris_data"], baris, nama)
        return d

    def teks(self, d):
        return " ".join(d["peringatan"] + d["catatan"])

    # -- (d) di v1.0.4 -> kini (a) -----------------------------------------------------------------------
    def test_N1_shopee_total_dan_catatan_kaki(self):
        k = self.k["N1"]
        d = self.a("N1-shopee-judul-catatan-kaki.csv", "Total Pembayaran", k["total_pembayaran"], k["baris"])
        self.cek_a(self.fx / "N1-shopee-judul-catatan-kaki.csv", "Jumlah", k["qty"])
        t = self.teks(d)
        self.assertIn("BARIS DIKELUARKAN dari perhitungan (2 baris", t)
        self.assertEqual([x["alasan"] for x in d["baris_dikeluarkan"]],
                         ["baris ringkasan berlabel 'Total' di bawah tabel", "catatan di bawah tabel"])
        self.assertIn("Dicetak oleh", t)

    def test_N2_tokopedia_dua_baris_catatan(self):
        k = self.k["N2"]
        d = self.a("N2-tokopedia-rp-catatan-2-baris.csv", "Total Penjualan", k["total"], k["baris"])
        t = self.teks(d)
        self.assertIn("Catatan: data diambil", t)
        self.assertIn("Jumlah pesanan:", t)
        self.assertNotIn("tidak bisa dibaca sebagai tanggal", t)      # '15' tidak lagi jadi tanggal tidak valid

    def test_N4_bca_saldo_di_bawah(self):
        k = self.k["N4"]
        d = self.a("N4-bca-mutasi.csv", "Jumlah", k["jumlah_semua"], k["baris"])
        t = self.teks(d)
        for label in ("Saldo Awal", "Mutasi Kredit", "Mutasi Debet", "Saldo Akhir"):
            self.assertIn(label, t)
        d = jalankan_json(self, "pivot", self.fx / "N4-bca-mutasi.csv", "--grup", "Kolom E", "--nilai", "Jumlah")
        m = {r[0]: angka(r[2]) for r in d["tabel"][0]["baris"]}
        self.assertEqual(m, {"CR": D(k["kredit_CR"]), "DB": D(k["debet_DB"]), "TOTAL": D(k["jumlah_semua"])})

    def test_N8_kolom_catatan_opsional(self):
        k = self.k["N8"]
        d = self.a("N8-kolom-catatan-opsional.csv", "Jumlah", k["total"], k["baris"])
        self.assertIn("13 baris tidak punya sel untuk kolom paling kanan ('Catatan')", self.teks(d))

    # -- (c) di v1.0.4 -> kini (a) -----------------------------------------------------------------------
    def test_N11_sum_tanpa_label_dan_rata_rata(self):
        k = self.k["N11"]
        # v1.0.6: SUM tanpa label di CSV (tanpa rumus) = AMBIGU -> tetap dihitung + peringatan tegas + total alternatif
        d = self.alt(self.fx / "N11-excel-sum-tanpa-label.csv", "Jumlah", k["total"], k["baris"], [14])
        self.assertIn("baris ringkasan berlabel 'Rata-rata' di bawah tabel", self.teks(d))

    def test_N11_varian_label_di_kolom_mana_pun(self):
        f = self.t / "n11-varian.csv"
        f.write_text("Tanggal,Kategori,Keterangan,Jumlah\n01/09/2026,ATK,a,100000\n02/09/2026,ATK,b,200000\n"
                     "03/09/2026,Listrik,c,300000\n,,Total,600000\n,,Rata-rata,200000\n,,Min,100000\n"
                     ",,Maks,300000\n,,Grand Total,600000\n", encoding="utf-8")
        d = self.cek_a(f, "Jumlah", 600000, 3)
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [5, 6, 7, 8, 9])

    def test_subtotal_tanpa_label_di_tengah_dan_ekor(self):
        f = self.t / "subtotal-tanpa-label.csv"
        f.write_text("Tanggal,Kategori,Jumlah\n01/09/2026,ATK,100000\n02/09/2026,ATK,200000\n,,300000\n"
                     "03/09/2026,Listrik,300000\n04/09/2026,Listrik,50000\n,,350000\n,,650000\n,,162500\n"
                     ",,50000\n,,300000\n", encoding="utf-8")
        # v1.0.6: tanpa label & tanpa rumus = ambigu -> 6 kandidat, total alternatif = 650.000
        self.alt(f, "Jumlah", 650000, 4, [4, 7, 8, 9, 10, 11])
        # --pertahankan-total: semua baris dihitung apa adanya
        t, _n, _d = self.total(f, "Jumlah", "--pertahankan-total")
        self.assertEqual(t, D(100000 + 200000 + 300000 + 300000 + 50000 + 350000 + 650000 + 162500 + 50000 + 300000))

    def test_sum_tanpa_label_xlsx(self):
        f = self.t / "sum.xlsx"
        nilai = [125000, 80000, 42500, 310000]
        tot = sum(nilai)
        baris = [["Tanggal", "Uraian", "Jumlah"]]
        for i, v in enumerate(nilai):
            baris.append([("tgl", serial_excel(date(2026, 9, i + 1))), "Nota {}".format(i + 1), v])
        baris.append([None, None, ("f", "SUM(C2:C5)", tot)])
        baris.append([None, "Rata-rata", ("f", "AVERAGE(C2:C5)", tot / 4)])
        buat_xlsx(f, [{"nama": "Biaya", "baris": baris}])
        d = self.cek_a(f, "Jumlah", tot, 4)
        self.assertEqual([x["alasan"] for x in d["baris_dikeluarkan"]],
                         ["rumus agregat (C6: =SUM(C2:C5))", "rumus agregat (C7: =AVERAGE(C2:C5))"])

    def test_bukan_ringkasan_tetap_data(self):
        # satu kolom angka saja: 1 + 2 = 3 BUKAN baris jumlah (tidak ada kolom lain yang kosong)
        f = self.t / "satu-kolom.csv"
        f.write_text("Nominal\n1\n2\n3\n", encoding="utf-8")
        self.cek_a(f, "Nominal", 6, 3)
        # baris data terakhir tanpa angka tetapi bukan catatan -> tetap dihitung sebagai baris
        f = self.t / "akhir-tanpa-angka.csv"
        f.write_text("Tanggal,Nama,Nominal\n01/09/2026,Ani,5000\n02/09/2026,Budi,7000\n03/09/2026,Cici,\n",
                     encoding="utf-8")
        d = jalankan_json(self, "ringkas", f)
        self.assertEqual(d["jumlah_baris_data"], 3)
        # baris 'Saldo' biasa (bukan 'Saldo Awal') tetap data
        f = self.t / "saldo.csv"
        f.write_text("Tanggal;Uraian;Masuk\n01/09/2026;Saldo;100.000\n02/09/2026;Jual;50.000\n", encoding="utf-8")
        self.cek_a(f, "Masuk", 150000, 2)

    def test_saldo_awal_di_atas_tabel(self):
        f = self.t / "mutasi.csv"
        f.write_text("Tanggal,Keterangan,Debit,Kredit,Saldo\n01/09/2026,SALDO AWAL,,,1000000\n"
                     "02/09/2026,Transfer masuk,,250000,1250000\n03/09/2026,Tarik tunai,100000,,1150000\n"
                     ",Saldo Akhir,,,1150000\n", encoding="utf-8")
        d = jalankan_json(self, "ringkas", f)
        self.assertEqual(d["jumlah_baris_data"], 2)
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [2, 5])
        self.assertIn("di atas tabel", d["baris_dikeluarkan"][0]["alasan"])

    def test_N12_catatan_berpadding_tidak_jadi_data(self):
        k = self.k["N12"]
        d = self.a("N12-footer-berpadding.csv", "Penghasilan", k["total"], k["baris"])
        d = jalankan_json(self, "ringkas", self.fx / "N12-footer-berpadding.csv")
        self.assertIn("Data mencakup 3 Sep 2026 s.d. 21 Sep 2026", " ".join(d["temuan"]))   # bukan 30 Sep
        d = jalankan_json(self, "pivot", self.fx / "N12-footer-berpadding.csv", "--grup", "Produk",
                          "--nilai", "Penghasilan")
        self.assertNotIn("(kosong)", [r[0] for r in d["tabel"][0]["baris"]])

    # -- yang sudah (a)/(b) tetap -----------------------------------------------------------------------
    def test_N3_N5_N6_N7_N10_N13_tetap_benar(self):
        k = self.k
        self.cek_a(self.fx / "N3-tiktok-baris-deskripsi.csv", "Order Amount", k["N3"]["total"])
        self.cek_a(self.fx / "N3-tiktok-baris-deskripsi.csv", "Quantity", k["N3"]["qty"])
        d = self.cek_a(self.fx / "N5-mandiri-kolom-ganda.csv", "Debit", k["N5"]["debit"])
        self.cek_a(self.fx / "N5-mandiri-kolom-ganda.csv", "Credit", k["N5"]["credit"])
        self.a("N6-google-form.csv", "Jumlah Transfer", k["N6"]["total_valid"], k["N6"]["baris"])
        self.a("N7-excel-titikkoma-kolom-kosong.csv", "Total", k["N7"]["total"], k["N7"]["baris"])
        self.cek_a(self.fx / "N7-excel-titikkoma-kolom-kosong.csv", "Qty", k["N7"]["qty"])
        self.a("N10-kutip-inci-panggilan.csv", "Jumlah", k["N10"]["total"], k["N10"]["baris"])
        # v1.0.6: 'Subtotal' di tengah = ambigu -> peringatan tegas; ekor dikeluarkan; total alternatif = kunci
        d = self.alt(self.fx / "N13-subtotal-per-hari.csv", "Nominal", k["N13"]["total"], k["N13"]["baris"], [6, 11])
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [16])

    def test_B13_kolom_kode_dan_rp(self):
        d = jalankan_json(self, "profil", self.fx / "N5-mandiri-kolom-ganda.csv")
        tipe = {r[0]: r[1] for r in d["tabel"][0]["baris"]}
        self.assertNotEqual(tipe.get("Transaction Code"), "angka")
        d = jalankan_json(self, "ringkas", self.fx / "N5-mandiri-kolom-ganda.csv")
        nama = [r[0] for r in d["tabel"][0]["baris"]]
        self.assertNotIn("Transaction Code", nama)
        self.assertEqual(d["tabel"][0]["jenis_baris"], ["uang", "uang"])

    def test_N9_C8_sel_terlewat_tetap_gagal(self):
        err = self.cek_b(self.fx / "N9-sel-terlewat-tengah.csv", "baris 11: hanya 3 dari 4 kolom",
                         "masuk kolom 'Barang' yang biasanya teks", "sel kosong/terlewat di tengah baris",
                         "tanda kutip", "catatan di tengah tabel")
        self.assertIn("--paksa", err)
        # kolom paling kanan hilang tetapi kolom itu WAJIB (biasanya terisi) -> tetap GAGAL
        f = self.t / "kanan-wajib.csv"
        f.write_text("Tanggal,Nama,Jumlah\n01/09/2026,Ani,5000\n02/09/2026,Budi,6000\n03/09/2026,Cici\n"
                     "04/09/2026,Dodi,7000\n", encoding="utf-8")
        self.cek_b(f, "baris 4: hanya 2 dari 3 kolom", "kolom 'Jumlah' tidak ada, padahal biasanya terisi")
        # kolom opsional di kanan, tetapi sel yang ada bergeser (angka masuk kolom teks) -> tetap GAGAL
        f = self.t / "opsional-geser.csv"
        f.write_text("Tanggal,Nama,Jumlah,Catatan\n01/09/2026,Ani,5000\n02/09/2026,Budi,6000,lunas\n"
                     "03/09/2026,7000\n04/09/2026,Dodi,8000\n05/09/2026,Eka,9000\n", encoding="utf-8")
        self.cek_b(f, "baris 4: hanya 2 dari 4 kolom", "masuk kolom 'Nama' yang biasanya teks")
        # catatan kaki di TENGAH (ada baris data utuh sesudahnya) -> tetap GAGAL
        f = self.t / "catatan-tengah.csv"
        f.write_text("Tanggal,Nama,Jumlah\n01/09/2026,Ani,5000\nCatatan: sebagian belum lunas\n"
                     "02/09/2026,Budi,6000\n", encoding="utf-8")
        self.cek_b(f, "baris 3: hanya 1 dari 3 kolom")


# ---------------------------------------------------------------------------
# v1.0.6 — PRINSIP: buang otomatis HANYA bila tidak ambigu; selebihnya peringatan tegas + total alternatif
# ---------------------------------------------------------------------------

FIXTURE_V105 = SINI / "examples" / "buat_fixture_uji_v105.py"


def cek_waspada(test, f, kolom, kunci, baris, calon, kunci_di="tanpa", *extra):
    """Hasil (b) v1.0.6: baris kandidat TETAP dihitung, PERINGATAN TEGAS paling atas berisi nomor baris & saran
    --buang-baris, total alternatif DENGAN/TANPA baris itu; kunci penguji = salah satunya (kunci_di), dan
    --buang-baris <kandidat> memberi total TANPA."""
    d = jalankan_json(test, "ringkas", f, "--kolom", kolom, *extra)
    self_total = angka(d["tabel"][0]["baris"][0][2])
    test.assertEqual([x["baris"] for x in d["kemungkinan_ringkasan"]], calon, f.name)
    p0 = d["peringatan"][0]
    test.assertTrue(p0.startswith("PERINGATAN TEGAS — Kemungkinan baris ringkasan ikut terhitung ({} baris): baris"
                                  .format(len(calon))), p0)
    daftar = ",".join(map(str, calon))
    test.assertIn("Bila benar ringkasan, ulangi dengan --buang-baris {}.".format(daftar), p0)
    alt = {a["kolom"]: a for a in d["total_alternatif"]}
    test.assertIn(kolom, alt, f.name)
    test.assertEqual(angka(alt[kolom]["dengan"]), self_total)
    test.assertIn("DENGAN baris itu {} / TANPA {}baris itu {}".format(
        modul.fmt_angka(D(alt[kolom]["dengan"])), "SEMUA " if len(calon) > 1 else "",
        modul.fmt_angka(D(alt[kolom]["tanpa"]))), p0)
    test.assertEqual(angka(alt[kolom][kunci_di]), D(kunci), f.name)
    # jalan keluar: --buang-baris
    d2 = jalankan_json(test, "ringkas", f, "--kolom", kolom, "--buang-baris", daftar, *extra)
    test.assertEqual(angka(d2["tabel"][0]["baris"][0][2]), angka(alt[kolom]["tanpa"]), f.name)
    test.assertEqual(d2["kemungkinan_ringkasan"], [], f.name)
    test.assertNotIn("PERINGATAN TEGAS", " ".join(d2["peringatan"]))
    test.assertTrue(all(x["alasan"] == "diminta --buang-baris" for x in d2["baris_dikeluarkan"]
                        if x["baris"] in calon))
    if baris is not None:
        test.assertEqual(d["jumlah_baris_data"] - (len(calon) if kunci_di == "tanpa" else 0), baris, f.name)
    # Markdown: peringatan tegas tampil di ATAS tabel
    code, out, _err = jalankan("ringkas", f, "--kolom", kolom, *extra)
    test.assertEqual(code, 0)
    test.assertLess(out.index("PERINGATAN TEGAS"), out.index("| Kolom"))
    return d


UjiEksporV105.alt = lambda self, f, kolom, kunci, baris, calon: cek_waspada(self, f, kolom, kunci, baris, calon)


class UjiPrinsipV106(unittest.TestCase):
    """Fixture penguji ke-6 (uji ulang v1.0.5). Hasil per file: a = angka & baris cocok kunci tanpa peringatan tegas;
    b = kandidat tetap dihitung + PERINGATAN TEGAS + total alternatif (kunci = total DENGAN atau TANPA) + jalan keluar
    --buang-baris. Target: tidak ada (c) — tidak ada angka yang ikut/terbuang diam-diam."""

    total = UjiInvarianV104.total
    cek_a = UjiInvarianV104.cek_a

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.t = Path(cls._tmp.name)
        cls.fx = cls.t / "u6"
        r = subprocess.run([sys.executable, str(FIXTURE_V105), str(cls.fx)], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        cls.k = json.loads((cls.fx / "kunci-v105.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def a(self, nama, kolom, total, baris=None, dikeluarkan=()):
        d = self.cek_a(self.fx / nama, kolom, total)
        self.assertEqual(d["kemungkinan_ringkasan"], [], nama)
        if baris is not None:
            self.assertEqual(d["jumlah_baris_data"], baris, nama)
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], list(dikeluarkan), nama)
        return d

    def b(self, nama, kolom, kunci, baris, calon, kunci_di):
        return cek_waspada(self, self.fx / nama, kolom, kunci, baris, calon, kunci_di)

    # -- dulu (c) salah diam-diam -------------------------------------------------------------------------
    def test_R11_xlsx_rumus_sum_average_dikeluarkan_baris_polos_diwaspadai(self):
        k = self.k["R11"]
        d = self.b("R11-kas-sum-average.xlsx", "Biaya", k["total"], k["baris"], [6], "dengan")
        self.assertEqual([(x["baris"], x["alasan"]) for x in d["baris_dikeluarkan"]],
                         [(7, "rumus agregat (C7: =SUM(C2:C6))"), (8, "rumus agregat (C8: =AVERAGE(C2:C6))")])
        self.assertIn("2.140.000", " ".join(d["peringatan"]))              # B18: format rupiah, bukan 2140000.0000

    def test_R11_versi_csv_tanpa_rumus_diwaspadai(self):
        f = self.t / "r11.csv"
        f.write_text("Tanggal,Keterangan,Biaya\n2026-09-01,Gaji kurir,1500000\n,,1500000\n2026-09-02,Sewa gudang,"
                     "2000000\n2026-09-03,Bensin,350000\n,,5350000\n,,10700000\n,,2140000\n", encoding="utf-8")
        d = cek_waspada(self, f, "Biaya", 5350000, None, [6, 7, 8])
        alt = d["total_alternatif"][0]
        self.assertEqual(angka(alt["dengan"]), D(1500000 * 2 + 2000000 + 350000 + 5350000 + 10700000 + 2140000))
        # kunci penguji (10.700.000) = tanpa baris 7 & 8 saja
        d = jalankan_json(self, "ringkas", f, "--kolom", "Biaya", "--buang-baris", "7,8")
        self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), D(10700000))
        self.assertEqual([x["baris"] for x in d["kemungkinan_ringkasan"]], [6])

    def test_R10_subtotal_tanpa_label_termasuk_kelompok_1_baris(self):
        k = self.k["R10"]
        d = self.b("R10-subtotal-tanpa-label.csv", "Omzet", k["total"], k["baris"], [5, 7, 10], "tanpa")
        self.assertEqual(d["baris_dikeluarkan"], [])

    def test_R8d_catatan_berangka_dikeluarkan_dan_disebut(self):
        k = self.k["R8d"]
        d = self.a("R8d-catatan-berangka-3-sel.csv", "Nominal", k["total"], k["baris"], [9])
        self.assertEqual(d["baris_dikeluarkan"][0]["alasan"], "catatan di bawah tabel")
        self.assertIn("150000", d["baris_dikeluarkan"][0]["isi"])
        self.assertIn("--pertahankan-baris 9", d["peringatan"][0])
        t, _n, _d = self.total(self.fx / "R8d-catatan-berangka-3-sel.csv", "Nominal", "--pertahankan-baris", "9")
        self.assertEqual(t, D(k["total"] + 150000))

    # -- dulu (b-) data asli terbuang -----------------------------------------------------------------------
    def test_R6_R6b_R7_kategori_rata_rata_total(self):
        k = self.k
        self.a("R6-kategori-rata-rata.csv", "Bonus", k["R6"]["total"], k["R6"]["baris"])
        d = jalankan_json(self, "pivot", self.fx / "R6-kategori-rata-rata.csv", "--grup", "Penilaian", "--nilai", "Bonus")
        m = {r[0]: angka(r[2]) for r in d["tabel"][0]["baris"]}
        self.assertEqual(m["Rata-rata"], D(k["R6"]["per_penilaian"]["Rata-rata"]))
        self.a("R7-kerusakan-total.csv", "Nilai Klaim", k["R7"]["total"], k["R7"]["baris"])
        # label di sel teks PERTAMA -> kandidat (tetap dihitung), bukan dibuang
        self.b("R6b-penilaian-kolom-1.csv", "Bonus", k["R6b"]["total"], k["R6b"]["baris"], [3, 4], "dengan")

    def test_R3_R3c_R16_R5_data_kebetulan_sama_tetap_dihitung(self):
        k = self.k
        self.b("R3-kas-tanggal-sekali.csv", "Keluar", k["R3"]["total"], k["R3"]["baris"], [5, 9], "dengan")
        self.b("R3c-kas-akhir-sama-jumlah.csv", "Keluar", k["R3c"]["total"], k["R3c"]["baris"], [5], "dengan")
        d = self.b("R16-nilai-polos-sama-jumlah.xlsx", "Nilai", k["R16"]["total"], k["R16"]["baris"], [4], "dengan")
        self.assertNotIn("rumus", " ".join(x["alasan"] for x in d["kemungkinan_ringkasan"]))
        d = self.b("R5-produk-bernama-total.csv", "Harga", k["R5"]["total"], k["R5"]["baris"], [8, 9], "dengan")
        self.assertEqual(angka(d["total_alternatif"][0]["tanpa"]), D(k["R5"]["total_tanpa_baris_TOTAL_Jumlah"]))

    def test_R9_subtotal_berlabel(self):
        k = self.k["R9"]
        d = self.b("R9-subtotal-berlabel-kelompok-1-baris.csv", "Omzet", k["total"], k["baris"], [5, 7], "tanpa")
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [10, 11])       # ekor: Subtotal C + Grand Total

    # -- dulu (d) ditolak -----------------------------------------------------------------------------------
    def test_R8_R8c_catatan_kaki_berangka_terbaca(self):
        k = self.k
        self.a("R8-catatan-kaki-berangka.csv", "Nominal", k["R8"]["total"], k["R8"]["baris"], [9, 10])
        self.a("R8c-catatan-1-sel-berangka.csv", "Nominal", k["R8c"]["total"], k["R8c"]["baris"], [9, 10])

    # -- yang sudah (a) tetap (a) ---------------------------------------------------------------------------
    def test_a_tetap(self):
        k = self.k
        self.a("R1-bernomor-baris3-jumlah.csv", "Total", k["R1"]["total"], k["R1"]["baris"])
        self.a("R2-satu-kolom-nominal.csv", "Nominal", k["R2"]["total"], k["R2"]["baris"])
        self.a("R4-masuk-keluar-banyak-nol.csv", "Masuk", k["R4"]["masuk"], k["R4"]["baris"])
        self.a("R4-masuk-keluar-banyak-nol.csv", "Keluar", k["R4"]["keluar"], k["R4"]["baris"])
        self.a("R11b-sum-average-biasa.xlsx", "Biaya", k["R11b"]["total"], k["R11b"]["baris"], [5, 6])
        self.a("R12-bulan-angka.csv", "Penjualan", k["R12"]["total"], k["R12"]["baris"])
        self.a("R12b-bulan-angka-tanpa-tahun.csv", "Penjualan", k["R12b"]["total"], k["R12b"]["baris"])
        self.a("R13-waktu-pembeli-kosong.csv", "Bayar", k["R13"]["total"], k["R13"]["baris"])
        self.a("R14-iuran-baris-belum-lengkap.xlsx", "Iuran", k["R14"]["total"], k["R14"]["baris"])
        self.a("P1-shopee-nilai-berulang.csv", "Total Pembayaran", k["P1"]["total"], k["P1"]["baris"])
        self.a("P2-tokopedia-ringkasan-bawah.csv", "Total Penjualan", k["P2"]["total"], k["P2"]["baris"], [11, 12])
        self.a("P3-bca-keterangan-saldo-total.csv", "Jumlah", k["P3"]["jumlah"], k["P3"]["baris"], [12, 13, 14, 15])
        self.a("P4-google-form-donasi.csv", "Nominal Donasi", k["P4"]["total"], k["P4"]["baris"])

    # -- rumus XLSX: hanya agregat atas baris LAIN -------------------------------------------------------------
    def test_rumus_per_baris_dan_saldo_berjalan_bukan_ringkasan(self):
        f = self.t / "rumus.xlsx"
        baris = [["Tanggal", "Qty", "Harga", "Total", "Kumulatif"]]
        for i, (q, h) in enumerate([(2, 1000), (3, 2000), (1, 5000)]):
            r = i + 2
            baris.append([("tgl", serial_excel(date(2026, 9, i + 1))), q, h, ("f", "SUM(B{0}*C{0})".format(r), q * h),
                          ("f", "SUM($D$2:D{})".format(r), 0)])
        baris.append([None, None, None, ("f", "SUBTOTAL(9,D2:D4)", 13000)])
        buat_xlsx(f, [{"nama": "S", "baris": baris}])
        d = self.cek_a(f, "Total", 13000, 3)
        self.assertEqual([(x["baris"], x["alasan"]) for x in d["baris_dikeluarkan"]],
                         [(5, "rumus agregat (D5: =SUBTOTAL(9,D2:D4))")])
        self.assertTrue(modul._rumus_agregat_luar("_xlfn.AGGREGATE(9,6,C2:C9)", 10))
        self.assertTrue(modul._rumus_agregat_luar("ROUND(AVERAGE(C2:C9),0)", 10))
        self.assertFalse(modul._rumus_agregat_luar("SUMIF(A2:A9,\"x\",C2:C9)", 10))
        self.assertFalse(modul._rumus_agregat_luar("B10*C10", 10))
        # rumus bersama (shared): anak digeser dari induknya
        import xml.etree.ElementTree as ET
        bersama = {}
        induk = ET.fromstring('<f t="shared" si="0" ref="C7:D7">SUM(C2:C6)</f>')
        anak = ET.fromstring('<f t="shared" si="0"/>')
        self.assertEqual(modul._teks_rumus(induk, 7, bersama), "SUM(C2:C6)")
        self.assertEqual(modul._teks_rumus(anak, 8, bersama), "SUM(C3:C7)")

    # -- opsi --buang-baris / --pertahankan-baris ------------------------------------------------------------
    def test_opsi_baris(self):
        f = self.fx / "R10-subtotal-tanpa-label.csv"
        code, _o, err = jalankan("ringkas", f, "--buang-baris", "lima")
        self.assertEqual(code, 2)
        self.assertIn("GAGAL: --buang-baris berisi 'lima'", err)
        d = jalankan_json(self, "ringkas", f, "--buang-baris", "5", "--buang-baris", "99")
        self.assertEqual([x["baris"] for x in d["kemungkinan_ringkasan"]], [7, 10])
        self.assertIn("Nomor baris 99", " ".join(d["peringatan"]))
        d = jalankan_json(self, "ringkas", f, "--pertahankan-baris", "5,7,10")
        self.assertEqual(d["kemungkinan_ringkasan"], [])
        d = jalankan_json(self, "ringkas", self.fx / "P2-tokopedia-ringkasan-bawah.csv", "--pertahankan-baris", "12")
        # baris 12 dinyatakan data -> 'Total Penjualan' (baris 11) kini di TENGAH: tidak dibuang, jadi kandidat
        self.assertEqual(d["baris_dikeluarkan"], [])
        self.assertEqual([x["baris"] for x in d["kemungkinan_ringkasan"]], [11])
        self.assertEqual(d["jumlah_baris_data"], 7)

    def test_gabungan_sheet_nomor_baris_bersheet(self):
        f = self.t / "dua.xlsx"
        sh = []
        for nama, vals in (("A", [100, 200]), ("B", [300, 400])):
            b = [["Tanggal", "Uraian", "Nilai"]]
            for i, v in enumerate(vals):
                b.append([("tgl", serial_excel(date(2026, 9, i + 1))), "x{}".format(i), v])
            b.append([None, None, sum(vals)])
            b.append([("tgl", serial_excel(date(2026, 9, 5))), "y", 50])
            sh.append({"nama": nama, "baris": b})
        buat_xlsx(f, sh)
        d = jalankan_json(self, "ringkas", f, "--sheet", "semua", "--kolom", "Nilai")
        self.assertEqual([x["baris"] for x in d["kemungkinan_ringkasan"]], ["A:4", "B:4"])
        self.assertEqual(angka(d["total_alternatif"][0]["tanpa"]), D(1100))
        self.assertIn("--buang-baris A:4,B:4", d["peringatan"][0])
        d = jalankan_json(self, "ringkas", f, "--sheet", "semua", "--kolom", "Nilai", "--buang-baris", "A:4,B:4")
        self.assertEqual(angka(d["tabel"][0]["baris"][0][2]), D(1100))
        code, _o, err = jalankan("ringkas", f, "--sheet", "semua", "--buang-baris", "4")
        self.assertEqual(code, 2)
        self.assertIn("beserta sheetnya", err)


FIXTURE_V106 = SINI / "examples" / "buat_fixture_uji_v106.py"


class UjiPengamanV107(unittest.TestCase):
    """v1.0.7 — PENGAMAN UMUM (fixture penguji ke-7, uji ulang v1.0.6, + variasi tata letak). Target: tidak ada (c):
    setiap tata letak laporan yang tidak dikenali menjadi (b) peringatan tegas + total alternatif = kunci penguji,
    atau GAGAL jelas (tabel kedua)."""

    total = UjiInvarianV104.total
    cek_a = UjiInvarianV104.cek_a
    a = UjiPrinsipV106.a     # nama relatif ke folder fixture, atau Path absolut (file buatan tes)

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.t = Path(cls._tmp.name)
        cls.fx = cls.t / "u7"
        r = subprocess.run([sys.executable, str(FIXTURE_V106), str(cls.fx)], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        cls.k = json.loads((cls.fx / "kunci-v106.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def tulis(self, nama, teks):
        f = self.t / nama
        f.write_text(teks, encoding="utf-8")
        return f

    # -- (i) kata ringkasan di sel mana pun pada baris jarang (B19) ---------------------------------------
    def test_S12_data_subtotal_nilai_polos(self):
        k = self.k["S12"]
        d = cek_waspada(self, self.fx / "S12-data-subtotal-nilai-polos.csv", "Penjualan", k["total"], k["baris"],
                        [4, 6, 10], "tanpa")
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [11])
        self.assertIn("Jakarta Total", d["kemungkinan_ringkasan"][0]["alasan"])

    def test_B19_variasi_label_subtotal(self):
        kel = {"Jakarta": [3100000, 2750000], "Bandung": [1800000], "Surabaya": [2200000, 950000, 400000],
               "Medan": [100, 200]}
        label = {"Jakarta": "Total Jakarta", "Bandung": "Bandung Jumlah", "Surabaya": "Rekap Surabaya",
                 "Medan": None}
        t, calon = ["Kota,Sales,Penjualan"], []
        for kota, vals in kel.items():
            for i, v in enumerate(vals):
                t.append("{},S{},{}".format(kota, i + 1, v))
            t.append("{},,{}".format(label[kota] or kota, sum(vals)))     # Medan: tanpa kata ringkasan
            calon.append(len(t))
        t.append("Palu,S1,50")
        kunci = sum(sum(v) for v in kel.values()) + 50
        f = self.tulis("b19-variasi.csv", "\n".join(t) + "\n")
        d = cek_waspada(self, f, "Penjualan", kunci, None, calon, "tanpa")
        self.assertIn("jumlah 2 baris tepat di atasnya", d["kemungkinan_ringkasan"][-1]["alasan"])

    def test_B19_baris_lengkap_berkata_total_tetap_data(self):
        # nama produk/kategori yang MENGANDUNG kata ringkasan di baris lengkap = data (a)
        f = self.tulis("lengkap.csv", "Tanggal,Produk,Kategori,Harga\n2026-09-01,Paket Total Care,Rata-rata,150000\n"
                                      "2026-09-02,Saldo Kartu,Grand,50000\n2026-09-03,Kopi,Jumlah Besar,200000\n")
        self.a(f, "Harga", 400000, 3)

    # -- (iii) rincian pembayaran yang memecah total (B20) -------------------------------------------------
    def test_S3_ekspor_kasir_rincian_bayar(self):
        k = self.k["S3"]
        d = cek_waspada(self, self.fx / "S3-ekspor-kasir-tanpa-rumus.xlsx", "Total", k["total"], k["baris"],
                        [12, 13, 14], "tanpa")
        alt = {a["kolom"]: a for a in d["total_alternatif"]}
        self.assertEqual(angka(alt["Qty"]["tanpa"]), D(k["qty"]))
        self.assertIn("rincian baris 12", d["kemungkinan_ringkasan"][1]["alasan"])

    def test_B20_rincian_di_atas_total_ekor(self):
        f = self.tulis("kasir2.csv", "No,Item,Qty,Total\n1,Kopi,2,36000\n2,Roti,1,22000\n3,Teh,3,15000\n"
                                     "Tunai,,,40000\nQRIS,,,20000\nTransfer,,,13000\nTotal Penjualan,,6,73000\n")
        d = cek_waspada(self, f, "Total", 73000, 3, [5, 6, 7], "tanpa")
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [8])

    # -- tabel kedua & header berulang (B21, B23) ----------------------------------------------------------
    def test_S5_dua_tabel_gagal_jelas_dan_opsi_rentang(self):
        f = self.fx / "S5-dua-tabel.csv"
        k = self.k["S5"]
        code, _o, err = jalankan("ringkas", f)
        self.assertEqual(code, 2)
        for teks in ("LEBIH DARI SATU TABEL", "mulai baris 6", "--sampai-baris 5", "--mulai-baris 7"):
            self.assertIn(teks, err)
        t, n, d = self.total(f, "Nominal", "--sampai-baris", "5")
        self.assertEqual((t, d["jumlah_baris_data"]), (D(k["total_tabel1"]), k["baris_tabel1"]))
        self.assertEqual(self.total(f, "Qty", "--sampai-baris", "5")[0], D(6))
        t, n, d = self.total(f, "Nominal", "--mulai-baris", "7")
        self.assertEqual((t, n), (D(k["total_tabel2"]), 2))
        d = jalankan_json(self, "ringkas", f, "--paksa")
        self.assertTrue(d["peringatan"][0].startswith("PERINGATAN TEGAS (--paksa): File ini berisi LEBIH DARI SATU"))
        for salah in (["--mulai-baris", "0"], ["--mulai-baris", "7", "--sampai-baris", "5"]):
            self.assertEqual(jalankan("ringkas", f, *salah)[0], 2)

    def test_B21_tabel_kedua_sempit_dan_xlsx(self):
        f = self.tulis("dua2.csv", "Nama,Nominal\nAndi,100000\nBudi,200000\n\nBulan,Total\nJan,300000\nFeb,100000\n")
        code, _o, err = jalankan("ringkas", f)
        self.assertEqual(code, 2)
        self.assertIn("mulai baris 5", err)
        self.assertEqual(self.total(f, "Nominal", "--sampai-baris", "4")[0], D(300000))
        x = self.t / "dua.xlsx"
        buat_xlsx(x, [{"nama": "S", "baris": [["Tanggal", "Produk", "Qty", "Nominal"],
                                             [("tgl", serial_excel(date(2026, 9, 1))), "Kaos", 3, 225000],
                                             [("tgl", serial_excel(date(2026, 9, 2))), "Topi", 2, 90000], [],
                                             ["PENGELUARAN"], ["Tanggal", "Keterangan", "Nominal"],
                                             [("tgl", serial_excel(date(2026, 9, 1))), "Sewa", 500000]]}])
        code, _o, err = jalankan("ringkas", x)
        self.assertEqual(code, 2)
        self.assertIn("tabel kedua mulai baris 5", err)
        # teks biasa di kolom angka (bukan judul tabel) tidak memicu tabel kedua
        f = self.tulis("teks.csv", "Nama,Nominal\nAndi,100000\nBudi,belum bayar\nCici,200000\n")
        self.assertEqual(jalankan("ringkas", f)[0], 0)

    def test_S4_mutasi_multi_halaman(self):
        k = self.k["S4"]
        d = self.a("S4-mutasi-multi-halaman.csv", "Jumlah", k["jumlah"], k["baris"])
        self.assertIn("nomor halaman", " ".join(d["catatan"]))
        d = jalankan_json(self, "pivot", self.fx / "S4-mutasi-multi-halaman.csv", "--grup", "Jenis", "--nilai", "Jumlah")
        m = {r[0]: angka(r[2]) for r in d["tabel"][0]["baris"]}
        self.assertEqual((m["CR"], m["DB"]), (D(k["CR"]), D(k["DB"])))
        self.assertNotIn("(kosong)", m)

    def test_header_berulang_mirip(self):
        f = self.tulis("ulang.csv", "Tanggal,Keterangan,Jumlah,Jenis\n01/09/2026,A,100,CR\n02/09/2026,B,200,DB\n"
                                    "TANGGAL,KETERANGAN,JUMLAH,\n03/09/2026,C,300,CR\ntgl,Keterangan,Jumlah,Jenis\n"
                                    "04/09/2026,D,400,DB\nPage 2 of 2,,,\n")
        d = self.a(f, "Jumlah", 1000, 4)
        self.assertIn("(baris 4, 6)", " ".join(d["catatan"]))

    # -- B22: SUM daftar sel / penjumlahan sel tanpa label -------------------------------------------------
    def test_S1b_S1c_grand_total_rumus_daftar_sel(self):
        for nama in ("S1-subtotal-sum-berlabel.xlsx", "S1b-subtotal-sum-tanpa-label.xlsx",
                     "S1c-grandtotal-plus-tanpa-label.xlsx"):
            k = self.k[nama.split("-")[0]]
            self.a(nama, "Omzet", k["total"], k["baris"], [5, 9, 12, 13])

    # -- yang sudah (a)/(b) tetap -----------------------------------------------------------------------------
    def test_a_dan_b_lain_tetap(self):
        k = self.k
        self.a("S2-sum-mendatar-per-baris.xlsx", "Total", k["S2"]["total"], k["S2"]["baris"])
        self.a("S2-sum-mendatar-per-baris.xlsx", "Transport", k["S2"]["transport"], k["S2"]["baris"])
        self.a("S2b-rumus-kali-per-baris.xlsx", "Subtotal", k["S2b"]["total"], k["S2b"]["baris"], [7])
        self.a("S2b-rumus-kali-per-baris.xlsx", "Qty", k["S2b"]["qty"], k["S2b"]["baris"], [7])
        self.a("S2c-average-mendatar-nilai-siswa.xlsx", "UH1", k["S2c"]["jumlah_UH1"], k["S2c"]["baris"])
        self.a("S7-retur-negatif.csv", "Nilai", k["S7"]["nilai_bersih_bila_kurung_negatif"], k["S7"]["baris"])
        self.a("S8-duplikat-sah.csv", "Jumlah", k["S8"]["total"], k["S8"]["baris"])
        self.a("S9-total-di-atas-rumus.xlsx", "Biaya", k["S9"]["total"], k["S9"]["baris"], [2])
        self.a("S10-kebetulan-lalu-total.csv", "Nominal", k["S10"]["total"], k["S10"]["baris"], [5])
        self.a("S11-excel-data-subtotal.xlsx", "Penjualan", k["S11"]["total"], k["S11"]["baris"], [4, 6, 10, 11])
        for nama in ("S6-gaji-total-divisi.csv", "S6b-gaji-total-divisi-kolom1-tanpa-grand.csv"):
            kk = k[nama.split("-")[0]]
            cek_waspada(self, self.fx / nama, "Gaji Pokok", kk["gaji_pokok"], kk["baris"], [5, 7], "tanpa")
            cek_waspada(self, self.fx / nama, "Tunjangan", kk["tunjangan"], kk["baris"], [5, 7], "tanpa")

    # -- pesan dibatasi & profil menampilkan baris yang dipakai ---------------------------------------------
    def test_banyak_kandidat_pesan_dibatasi(self):
        t = ["Toko,Kasir,Omzet"]
        for g in range(40):
            t += ["T{},A,{}".format(g, 1000 + g), "T{},B,{}".format(g, 2000), "T{} Total,,{}".format(g, 3000 + g)]
        f = self.tulis("banyak.csv", "\n".join(t) + "\n")
        d = jalankan_json(self, "ringkas", f, "--kolom", "Omzet")
        self.assertEqual(len(d["kemungkinan_ringkasan"]), 40)
        p0 = d["peringatan"][0]
        self.assertIn("(40 baris)", p0)
        self.assertIn("dan 32 baris lainnya", p0)
        self.assertIn("(daftar lengkap di keluaran --json)", p0)
        self.assertLess(len(p0), 3000)
        alt = d["total_alternatif"][0]
        self.assertEqual(angka(alt["tanpa"]), D(sum(1000 + g + 2000 for g in range(40))))
        self.assertLessEqual(len(alt["tanpa_per_baris"]), modul.MAKS_KANDIDAT_TAMPIL)

    def test_profil_cek_baris_dipakai(self):
        f = self.fx / "S6-gaji-total-divisi.csv"
        d = jalankan_json(self, "profil", f)
        tb = {t["judul"].split(" (")[0]: t for t in d["tabel"]}
        cek = next(t for t in d["tabel"] if t["judul"].startswith("Cek sekilas"))
        self.assertEqual([r[0] for r in cek["baris"]], ["2", "3", "4", "5", "6", "7", "8", "9"])
        self.assertTrue(all(r[3] == "(disembunyikan)" for r in cek["baris"]))          # Gaji Pokok = data pribadi
        self.assertEqual([r[0] for r in tb["Baris DIKELUARKAN dari perhitungan"]["baris"]], ["10", "11"])
        self.assertEqual([r[0] for r in tb["Kemungkinan baris ringkasan"]["baris"]], ["5", "7"])
        # data besar: 5 pertama, penanda, 5 terakhir
        t = ["No,Nilai"] + ["{},{}".format(i, i * 10) for i in range(1, 31)]
        d = jalankan_json(self, "profil", self.tulis("30.csv", "\n".join(t) + "\n"))
        cek = next(t for t in d["tabel"] if t["judul"].startswith("Cek sekilas"))
        self.assertEqual([r[0] for r in cek["baris"]], ["2", "3", "4", "5", "6", "…", "27", "28", "29", "30", "31"])
        code, out, _e = jalankan("profil", f)
        self.assertIn("### Cek sekilas: baris data yang DIPAKAI", out)


FIXTURE_V107 = SINI / "examples" / "buat_fixture_uji_v107.py"


class UjiLengkapV108(unittest.TestCase):
    """v1.0.8 — fixture penguji ke-8 (uji ulang v1.0.7). Target: tidak ada (c) pada V1, V3, V4, V5, V6, V13
    (subtotal/total TERISI LENGKAP, pivot ringkas, tabel tanpa judul kolom); kontrol & ekspor rapi tetap (a)."""

    total = UjiInvarianV104.total
    cek_a = UjiInvarianV104.cek_a
    a = UjiPrinsipV106.a

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.t = Path(cls._tmp.name)
        cls.fx = cls.t / "u8"
        r = subprocess.run([sys.executable, str(FIXTURE_V107), str(cls.fx)], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        cls.k = json.loads((cls.fx / "kunci-v107.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def tulis(self, nama, teks):
        f = self.t / nama
        f.write_text(teks, encoding="utf-8")
        return f

    # -- B24: subtotal/total terisi lengkap -> kandidat + total alternatif = kunci -------------------------
    def test_V1_judul_kategori_dan_subtotal_lengkap(self):
        k = self.k["V1"]
        f = self.fx / "V1-stok-kategori-subtotal-lengkap.xlsx"
        d = cek_waspada(self, f, "Nilai Stok", k["nilai"], k["baris"], [5, 10, 14], "tanpa")
        cek_waspada(self, f, "Stok", k["stok"], k["baris"], [5, 10, 14], "tanpa")
        kel = {x["baris"]: x["alasan"] for x in d["baris_dikeluarkan"]}
        self.assertEqual(sorted(kel), [2, 6, 11, 15])                     # 3 judul kategori (B28) + TOTAL ekor
        self.assertIn("judul kelompok 'SEMEN'", kel[2])
        d = jalankan_json(self, "pivot", f, "--grup", "Satuan", "--nilai", "Nilai Stok", "--buang-baris", "5,10,14")
        self.assertNotIn("(kosong)", [r[0] for r in d["tabel"][0]["baris"]])

    def test_V4_jumlah_hadir_di_kolom_tanggal(self):
        k = self.k["V4"]
        d = cek_waspada(self, self.fx / "V4-absensi-jumlah-hadir.csv", "Jam Kerja", k["jam"], k["baris"],
                        [7, 13, 19], "tanpa")
        self.assertIn("Jumlah Hadir", d["kemungkinan_ringkasan"][0]["alasan"])

    def test_V5_total_jurnal_lengkap_di_ekor(self):
        k = self.k["V5"]
        f = self.fx / "V5-jurnal-umum-total-lengkap.csv"
        cek_waspada(self, f, "Debit", k["debit"], k["baris"], [12], "tanpa")
        cek_waspada(self, f, "Kredit", k["kredit"], k["baris"], [12], "tanpa")

    def test_V6_subtotal_cabang_dan_grand_total_lengkap(self):
        k = self.k["V6"]
        f = self.fx / "V6-cabang-subtotal-lengkap.csv"
        cek_waspada(self, f, "Omzet", k["omzet"], k["baris"], [5, 9, 12, 13], "tanpa")
        cek_waspada(self, f, "Qty", k["qty"], k["baris"], [5, 9, 12, 13], "tanpa")
        d = jalankan_json(self, "pivot", f, "--grup", "Cabang", "--nilai", "Omzet", "--buang-baris", "5,9,12,13")
        m = {r[0]: angka(r[2]) for r in d["tabel"][0]["baris"]}
        self.assertEqual(m.pop("TOTAL"), D(k["omzet"]))
        self.assertEqual(m, {c: D(v) for c, v in k["per_cabang"].items()})

    def test_B24_subtotal_tanpa_kata_dua_kolom(self):
        t = "Tanggal,Cabang,Produk,Qty,Omzet\n"
        blok = {"Bekasi": [(5, 750000), (6, 540000), (3, 270000)], "Bogor": [(4, 600000), (2, 180000), (7, 630000)]}
        calon, kunci = [], 0
        n = 1
        for c, it in blok.items():
            for q, o in it:
                t += "2026-09-0{},{},Kopi,{},{}\n".format(n % 9 + 1, c, q, o)
                n += 1
                kunci += o
            t += "2026-09-30,{},,{},{}\n".format(c, sum(q for q, _o in it), sum(o for _q, o in it))
            n += 1
            calon.append(n)
        t += "2026-09-04,Depok,Kopi,8,1200000\n"
        kunci += 1200000
        cek_waspada(self, self.tulis("b24.csv", t), "Omzet", kunci, None, calon, "tanpa")

    def test_B24_kebetulan_tetap_data(self):
        # baris lengkap yang kebetulan = jumlah 2 baris di atasnya: qty kecil (1 + 2 = 3) & kolom kembar tidak cukup
        self.a(self.tulis("k1.csv", "Tanggal,Produk,Qty,Total\n2026-09-01,A,10,100000\n2026-09-02,B,20,200000\n"
                                    "2026-09-03,C,30,300000\n2026-09-04,D,5,50000\n"), "Total", 650000, 4)
        self.a(self.tulis("k2.csv", "No Pesanan,Produk,Jumlah,Harga,Bayar\nA1,Jumlah Hemat,1,89000,89000\n"
                                    "A2,Jumlah Hemat,2,45000,45000\nA3,Jumlah Hemat,3,134000,134000\n"
                                    "A4,Kopi,1,20000,20000\n"), "Bayar", 288000, 4)
        # nama produk/kategori berkata Total/Jumlah di baris lengkap = data
        self.a(self.tulis("k3.csv", "Tanggal,Produk,Kategori,Harga\n2026-09-01,Paket Total Care,Rata-rata,150000\n"
                                    "2026-09-02,Saldo Kartu,Grand,50000\n2026-09-03,Kopi,Jumlah Besar,200000\n"),
               "Harga", 400000, 3)

    # -- B26: pivot bentuk ringkas ------------------------------------------------------------------------
    def test_V3_pivot_ringkas_subtotal_di_atas(self):
        k = self.k["V3"]
        d = cek_waspada(self, self.fx / "V3-pivot-ringkas-en.csv", "Sum of Amount", k["total"], k["baris_daun"],
                        [2, 5], "tanpa")
        self.assertIn("PivotTable", " ".join(d["catatan"]))
        f = self.tulis("piv2.csv", "Row Labels,Sum of Qty,Sum of Amount\nJawa,50,5000000\nKopi,30,3000000\n"
                                   "Teh,20,2000000\nSumatra,25,2500000\nKopi,15,1500000\nTeh,10,1000000\n"
                                   "Grand Total,75,7500000\n")
        cek_waspada(self, f, "Sum of Amount", 7500000, 4, [2, 5], "tanpa")
        cek_waspada(self, f, "Sum of Qty", 75, 4, [2, 5], "tanpa")

    def test_B26_pivot_ringkas_total_di_bawah(self):
        f = self.tulis("piv3.csv", "Row Labels,Sum of Amount\nJawa,\nKopi,3000000\nTeh,2000000\nJawa Total,5000000\n"
                                   "Sumatra,\nKopi,1500000\nTeh,1000000\nSumatra Total,2500000\n"
                                   "Grand Total,7500000\n")
        d = cek_waspada(self, f, "Sum of Amount", 7500000, 4, [5, 9], "tanpa")
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [2, 6, 10])

    def test_B26_tabel_biasa_tidak_dianggap_pivot(self):
        # tabel 1 kolom angka yang kebetulan sebagian bisa dijumlah tetapi TIDAK terbagi habis -> (a)
        self.a(self.tulis("bukan.csv", "Nama,Nominal\nAni,50000\nBudi,20000\nCici,30000\nDodi,10000\n"),
               "Nominal", 110000, 4)

    # -- B25: tabel tanpa judul kolom ---------------------------------------------------------------------
    def test_V13_tanpa_header(self):
        k = self.k["V13"]
        f = self.fx / "V13-tanpa-header.csv"
        t, n, d = self.total(f, "Kolom5")
        self.assertEqual((t, d["jumlah_baris_data"], d["baris_header"]), (D(k["total"]), k["baris"], 0))
        p = " ".join(d["peringatan"])
        self.assertIn("PERINGATAN TEGAS — Tabel ini tampaknya TIDAK punya baris judul kolom", p)
        self.assertIn("--baris-header 1", p)
        # pengguna menyatakan baris 1 = judul -> perilaku lama, tanpa peringatan
        t, n, d = self.total(f, "150000", "--baris-header", "1")
        self.assertEqual(n, k["baris"] - 1)
        self.assertNotIn("TIDAK punya baris judul", " ".join(d["peringatan"]))
        for opsi in (["--tanpa-header"], ["--baris-header", "0"], ["--header-baris", "0"]):
            t, n, d = self.total(f, "Kolom5", *opsi)
            self.assertEqual(t, D(k["total"]))
        code, _o, err = jalankan("ringkas", f, "--baris-header", "-1")
        self.assertEqual(code, 2)
        self.assertIn("--baris-header harus 0", err)
        d = jalankan_json(self, "profil", f)
        self.assertIn("TANPA baris judul kolom", " ".join(d["temuan"]))

    def test_B25_tanpa_header_tanpa_tanggal_dan_judul_angka_sah(self):
        f = self.tulis("nh.csv", "Bu Ani,Kue Lapis,2,150000\nPak Dedi,Bolu,1,85000\nBu Rina,Kue Lapis,3,225000\n")
        t, n, d = self.total(f, "Kolom4")
        self.assertEqual((t, n), (D(460000), 3))
        # judul kolom berupa tahun atau nomor soal = judul sah, bukan data
        self.a(self.tulis("th.csv", "Produk,2024,2025,2026\nBeras,1000,1200,1300\nGula,500,600,700\n"),
               "2025", 1800, 2)
        self.a(self.tulis("soal.csv", "Nama,1,2,3\nAyu,80,90,70\nBima,75,60,88\nCici,95,85,80\n"), "2", 235, 3)
        # judul tanggal di atas kolom angka (absensi melebar) = judul sah
        self.a(self.tulis("tgl.csv", "Nama,01/09/2026,02/09/2026\nAyu,8,7\nBima,6,8\n"), "01/09/2026", 14, 2)

    # -- yang sudah (a) tetap (a); P3 -----------------------------------------------------------------------
    def test_a_tetap_dan_p3(self):
        k = self.k
        self.a("V2-pivot-nilai-id.xlsx", "Sep", k["V2"]["sep"], k["V2"]["baris"], [6])
        self.a("V9-gobiz-transaksi.csv", "Pendapatan Bersih", k["V9"]["bersih"], k["V9"]["baris"])
        self.a("V10-grabmerchant-angka-inggris.csv", "Gross Sales (IDR)", k["V10"]["gross"], k["V10"]["baris"])
        self.a("V11-eropa-koma-desimal.csv", "Betrag", k["V11"]["betrag"], k["V11"]["baris"])
        self.a("V12-bulan-melebar.xlsx", "Des", k["V12"]["per_bulan"]["Des"], k["V12"]["baris"], [6])
        self.a("K1-kontrol-biaya.csv", "Nominal", k["K1"]["total"], k["K1"]["baris"])
        self.a("K2-kontrol-stok.xlsx", "Stok", k["K2"]["stok"], k["K2"]["baris"])
        self.a("K3-kontrol-nilai-siswa.csv", "Nilai", k["K3"]["jumlah"], k["K3"]["baris"])
        # V8: Masa Pajak / Tahun = periode (tidak dijumlah); PPN = kunci
        d = self.a("V8-coretax-faktur-keluaran.csv", "PPN", k["V8"]["ppn"], k["V8"]["baris"])
        d = jalankan_json(self, "ringkas", self.fx / "V8-coretax-faktur-keluaran.csv")
        kol = [r[0] for r in d["tabel"][0]["baris"]]
        self.assertNotIn("Masa Pajak", kol)
        self.assertNotIn("Tahun", kol)
        # V7: e-Faktur FK/LT/OF -> GAGAL dengan pesan khusus + jalan keluar yang benar
        f = self.fx / "V7-efaktur-fk-of.csv"
        code, _o, err = jalankan("ringkas", f)
        self.assertEqual(code, 2)
        self.assertIn("e-Faktur format lama", err)
        t, _n, _d = self.total(f, "JUMLAH_DPP", "--paksa", "--filter", "FK=FK")
        self.assertEqual(t, D(k["V7"]["dpp"]))


FIXTURE_V108 = SINI / "examples" / "buat_fixture_uji_v108.py"


class UjiSilangV109(unittest.TestCase):
    """v1.0.9 — fixture penguji ke-9 (uji ulang v1.0.8). B29 pivot ringkas dengan kelompok beranak tunggal,
    B31 pengaman silang Grand Total, B30 judul kolom tahun, B32 kolom nomor urut; W* lain tetap (a)/(b)."""

    total = UjiInvarianV104.total
    cek_a = UjiInvarianV104.cek_a
    a = UjiPrinsipV106.a

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.t = Path(cls._tmp.name)
        cls.fx = cls.t / "u9"
        r = subprocess.run([sys.executable, str(FIXTURE_V108), str(cls.fx)], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr)
        cls.k = json.loads((cls.fx / "kunci-v108.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def tulis(self, nama, teks):
        f = self.t / nama
        f.write_text(teks, encoding="utf-8")
        return f

    # -- B29 + B31: W8 pivot ringkas, kelompok Bogor hanya 1 anak ------------------------------------------
    def test_W8_pivot_ringkas_kelompok_beranak_tunggal(self):
        k = self.k["W8"]
        f = self.fx / "W8-pivot-ringkas-id.xlsx"
        d = cek_waspada(self, f, "Jumlah dari Omzet", k["omzet"], None, [2, 5, 7], "tanpa")
        cek_waspada(self, f, "Jumlah dari Qty", k["qty"], None, [2, 5, 7], "tanpa")
        self.assertEqual([x["baris"] for x in d["baris_dikeluarkan"]], [11])
        p0 = d["peringatan"][0]
        self.assertIn("PENGAMAN SILANG: baris 'Total Keseluruhan' di file (baris 11) = total TANPA baris kandidat", p0)
        self.assertIn("6.140.000", p0)
        cs = d["cek_silang_total"][0]
        self.assertEqual(cs["baris"], 11)
        self.assertEqual({c["status"] for c in cs["kolom"]}, {"cocok_tanpa"})
        # daun (produk) menurut --buang-baris = kunci; pivot tidak lagi mencampur
        d2 = jalankan_json(self, "ringkas", f, "--kolom", "Jumlah dari Omzet", "--buang-baris", "2,5,7")
        self.assertEqual(angka(d2["tabel"][0]["baris"][0][2]), D(k["omzet"]))
        self.assertIn("COCOK dengan baris 'Total Keseluruhan'", " ".join(d2["catatan"]))

    def test_B31_pengaman_silang_bila_deteksi_gagal(self):
        # deteksi dimatikan pengguna (--pertahankan-baris) -> total 2x Grand Total -> PERINGATAN TEGAS paling atas
        f = self.fx / "W8-pivot-ringkas-id.xlsx"
        d = jalankan_json(self, "ringkas", f, "--pertahankan-baris", "2,5,7")
        self.assertEqual(d["kemungkinan_ringkasan"], [])
        p0 = d["peringatan"][0]
        self.assertTrue(p0.startswith("PERINGATAN TEGAS — PENGAMAN SILANG: Total hitungan ≠ 'Total Keseluruhan'"), p0)
        self.assertIn("total hitungan 12.280.000 ≠ Total Keseluruhan di file 6.140.000 (tepat 2×", p0)
        self.assertIn("Total alternatif = angka 'Total Keseluruhan' di file", p0)
        # tata letak baru yang tidak dikenali: kelompok semua beranak tunggal + Grand Total
        f = self.tulis("tunggal.csv", "Row Labels,Sum of Omzet\nBekasi,500000\nKopi,500000\nBogor,300000\n"
                                      "Teh,300000\nGrand Total,800000\n")
        d = jalankan_json(self, "ringkas", f)
        self.assertIn("PERINGATAN TEGAS — PENGAMAN SILANG", d["peringatan"][0])
        self.assertIn("tepat 2×", d["peringatan"][0])
        # 3x (subtotal kelompok + subtotal wilayah ikut terhitung)
        f = self.tulis("tiga.csv", "Tanggal,Nama,Nominal\n01/09/2026,Ani,100\n02/09/2026,Budi,200\n,,300\n"
                                   ",,300\nTotal,,300\n")
        d = jalankan_json(self, "ringkas", f, "--pertahankan-baris", "4,5")
        self.assertIn("tepat 3×", " ".join(d["peringatan"]))
        # Total di file tidak sama (baris hilang) tanpa rasio bulat -> tetap TEGAS
        f = self.tulis("beda.csv", "Tanggal,Nama,Nominal\n01/09/2026,Ani,100000\n02/09/2026,Budi,250000\n"
                                   "03/09/2026,Cici,75000\nTotal,,500000\n")
        d = jalankan_json(self, "ringkas", f)
        self.assertIn("PERINGATAN TEGAS — PENGAMAN SILANG: Total hitungan ≠ 'Total' di file (baris 5): kolom "
                      "'Nominal': total hitungan 425.000 ≠ Total di file 500.000", d["peringatan"][0])

    def test_B31_cocok_menaikkan_keyakinan(self):
        f = self.tulis("cocok.csv", "Tanggal,Nama,Qty,Nominal\n01/09/2026,Ani,2,100000\n02/09/2026,Budi,3,250000\n"
                                    "03/09/2026,Cici,1,75000\nTotal,,6,425000\nRata-rata,,2,141667\n")
        d = self.cek_a(f, "Nominal", 425000, 3)
        c = " ".join(d["catatan"])
        self.assertIn("Pengaman silang: total hasil hitungan COCOK dengan baris 'Total' di file (baris 5)", c)
        self.assertNotIn("PENGAMAN SILANG", " ".join(d["peringatan"]))
        # invoice: Subtotal cocok, Grand Total = + PPN -> tidak ada peringatan palsu
        f = self.tulis("inv.csv", "Barang,Qty,Jumlah\nSemen,2,110000\nPasir,1,350000\nSubtotal,,460000\n"
                                  "Grand Total,,510600\n")
        d = jalankan_json(self, "ringkas", f)
        self.assertNotIn("PENGAMAN SILANG", " ".join(d["peringatan"]))

    def test_W6_W9_W10_subtotal_tetap_b_dengan_pengaman(self):
        k = self.k
        f = self.fx / "W6-subtotal-penuh-multikolom.csv"
        for kol, kunci in (("Qty", k["W6"]["qty"]), ("Omzet", k["W6"]["omzet"]), ("Laba", k["W6"]["laba"])):
            d = cek_waspada(self, f, kol, kunci, None, [5, 8, 12, 13], "tanpa")
        alt = {x["kolom"]: x for x in d["total_alternatif"]}
        self.assertEqual(angka(alt["HPP"]["tanpa"]), D(k["W6"]["hpp"]))
        self.assertIn("PENGAMAN SILANG: baris 'Total Semua Wilayah' di file (baris 13) = total TANPA", d["peringatan"][0])
        d = cek_waspada(self, self.fx / "W9-pivot-tabular.csv", "Sum of Omzet", k["W9"]["omzet"], None, [4, 6, 10],
                        "tanpa")
        self.assertIn("PENGAMAN SILANG: baris 'Grand Total' di file (baris 11) = total TANPA", d["peringatan"][0])
        cek_waspada(self, self.fx / "W10-pivot-ringkas-tanpa-kata-kunci.csv", "Penjualan", k["W10"]["total"], None,
                    [2, 6, 9], "tanpa")

    # -- B30, B32 ----------------------------------------------------------------------------------------
    def test_B30_judul_tahun_tanpa_pemisah_ribuan(self):
        k = self.k["W5b"]
        d = jalankan_json(self, "ringkas", self.fx / "W5b-header-tahun-numerik.xlsx")
        self.assertEqual([r[0] for r in d["tabel"][0]["baris"]], ["2023", "2024", "2025"])
        for th in ("2023", "2024", "2025"):
            self.a("W5b-header-tahun-numerik.xlsx", th, k[th], k["baris"])

    def test_B32_nomor_urut_tidak_dijumlah(self):
        k = self.k["W2"]
        d = jalankan_json(self, "ringkas", self.fx / "W2-tanpa-header-no-urut.csv")
        kol = [r[0] for r in d["tabel"][0]["baris"]]
        self.assertNotIn("Kolom1", kol)
        t, _n, _d = self.total(self.fx / "W2-tanpa-header-no-urut.csv", "Kolom6")
        self.assertEqual(t, D(k["total"]))
        t, _n, _d = self.total(self.fx / "W2-tanpa-header-no-urut.csv", "Kolom4")
        self.assertEqual(t, D(k["qty"]))
        f = self.tulis("pagar.csv", "#,Barang,Qty,Nominal\n1,Semen,2,110000\n2,Pasir,1,350000\n3,Besi,4,312000\n")
        d = jalankan_json(self, "ringkas", f)
        self.assertEqual([r[0] for r in d["tabel"][0]["baris"]], ["Qty", "Nominal"])
        # satu kolom 1,2,3 berjudul biasa tetap dijumlah
        self.cek_a(self.tulis("satu.csv", "Nominal\n1\n2\n3\n"), "Nominal", 6, 3)

    # -- W lain: (a) --------------------------------------------------------------------------------------
    def test_W_lain_tetap_a(self):
        k = self.k
        for nama, kol, kunci, baris in (
                ("W1-tanpa-header-teks-dulu.csv", "Kolom6", k["W1"]["total"], k["W1"]["baris"]),
                ("W3-tanpa-header-tanggal.xlsx", "Kolom3", k["W3"]["total"], k["W3"]["baris"])):
            t, n, d = self.total(self.fx / nama, kol)
            self.assertEqual((t, d["jumlah_baris_data"]), (D(kunci), baris), nama)
            self.assertIn("TIDAK punya baris judul kolom", d["peringatan"][0])
        self.a("W4-header-tahun.csv", "2024", k["W4"]["2024"], k["W4"]["baris"])
        self.a("W4-header-tahun.csv", "2025", k["W4"]["2025"], k["W4"]["baris"])
        for b in ("1", "7", "12"):
            self.a("W5-header-nomor-bulan.xlsx", b, k["W5"]["per_bulan"][b], k["W5"]["baris"])
        self.a("W7-kebetulan-x-plus-y.csv", "Total", k["W7"]["total"], k["W7"]["baris"])
        self.a("W7-kebetulan-x-plus-y.csv", "Qty", k["W7"]["qty"], k["W7"]["baris"])
        self.a("W7b-kebetulan-jumlah-blok.xlsx", "Nominal", k["W7b"]["nominal"], k["W7b"]["baris"])
        self.a("W11-kontrol-uang-saku.csv", "Jumlah", k["W11"]["total"], k["W11"]["baris"])
        self.a("W12-kontrol-stok-atk.xlsx", "Stok", k["W12"]["stok"], k["W12"]["baris"])
        self.a("W13-kontrol-nilai.csv", "Nilai Akhir", k["W13"]["total"], k["W13"]["baris"])

    def test_kinerja_50rb_baris(self):
        f = self.t / "besar.csv"
        with f.open("w", encoding="utf-8") as h:
            h.write("Tanggal,Nota,Kategori,Qty,Nominal\n")
            for i in range(50000):
                h.write("{:02d}/09/2026,NT-{:05d},K{},{},{}\n".format(i % 28 + 1, i, i % 7, i % 9 + 1, 1000 * (i % 97 + 1)))
            h.write("Total,,,,{}\n".format(sum(1000 * (i % 97 + 1) for i in range(50000))))
        t0 = time.perf_counter()
        d = self.cek_a(f, "Nominal", sum(1000 * (i % 97 + 1) for i in range(50000)), 50000)
        self.assertLess(time.perf_counter() - t0, 10)
        self.assertIn("COCOK", " ".join(d["catatan"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
