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


if __name__ == "__main__":
    unittest.main(verbosity=1)
