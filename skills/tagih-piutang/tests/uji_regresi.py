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

    def test_ringkasan_grup_tanpa_nama(self):
        f = os.path.join(self.dir, "piutang.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("pelanggan,no_invoice,nominal,jatuh_tempo,dibayar,no_wa\n"
                     "Toko A,INV-01,6300000,2026-09-05,,0812111\nCV B,INV-02,12500000,2026-08-24,2500000,0813222\n"
                     "UD C,INV-03,4000000,2026-10-30,,0814333\n")
        h = self.rekap(f)
        g = h["ringkasan_grup"]
        # pembanding independen: telat = 6.300.000 + 10.000.000; semua = + 4.000.000
        self.assertIn("Faktur belum lunas: 3, total Rp 20.300.000", g)
        self.assertIn("Sudah lewat jatuh tempo: 2 faktur, total Rp 16.300.000", g)
        self.assertIn("30 hari", g)
        for rahasia in ("Toko A", "CV B", "UD C", "INV-0", "081"):
            self.assertNotIn(rahasia, g)
        kode, out, err = self.jalan("--file", f, "--tanggal", TGL, "--format", "teks")
        self.assertEqual(kode, 0, err)
        blok = out.split("Ringkasan aman untuk grup", 1)[1].split("```")[1]
        self.assertEqual(blok.strip(), g)

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

    # ---- v1.0.4 (uji OpenClaw 2026-10-01): alias kolom, format angka ID, jadwal tahap berikutnya
    def test_alias_kolom_faktur(self):
        # Kolom seperti di uji OpenClaw 04 + kolom ekstra (tanggal_faktur, no_wa) yang harus diabaikan.
        f = os.path.join(self.dir, "piutang.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("no_faktur,pelanggan,tanggal_faktur,jatuh_tempo,nilai_faktur,sudah_dibayar,no_wa\n"
                     "INV-01,Toko A,2026-08-05,2026-09-05,\"6.300.000\",,0812\n"
                     "INV-02,CV B,2026-07-24,24 Agu 2026,Rp 12.500.000,\"2,5jt\",0813\n"
                     "INV-03,PT C,2026-08-01,2026-09-01,1000000,1000000,0814\n")
        h = self.rekap(f)
        self.cek_rekap(h)
        self.assertEqual(h["kolom_dipakai"]["no_invoice"], "no_faktur")
        self.assertEqual(h["kolom_dipakai"]["dibayar"], "sudah_dibayar")
        self.assertEqual(h["total_telat"], 16300000)
        self.assertEqual({x["no_invoice"] for x in h["daftar"]}, {"INV-01", "INV-02"})

    def test_alias_kolom_inggris_dan_kurung(self):
        f = os.path.join(self.dir, "ar.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("Customer;Invoice No;Amount (Rp);Due Date;Paid\n"
                     "Toko A;INV-01;6.300.000;05/09/2026;0\nCV B;INV-02;12.500.000;2026-08-24;2.500.000\n")
        self.cek_rekap(self.rekap(f))

    def test_kolom_sisa_saja(self):
        f = os.path.join(self.dir, "sisa.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("nama_pelanggan,jatuh_tempo,sisa_tagihan\nToko A,2026-09-05,6.300.000\nCV B,2026-08-24,10.000.000\n")
        h = self.rekap(f)
        self.cek_rekap(h)
        self.assertIn("sisa_tagihan", h["catatan_kolom"])

    def test_kolom_tidak_dikenal_pesan_jelas(self):
        f = os.path.join(self.dir, "aneh.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("siapa,berapa,kapan\nToko A,100,2026-09-05\n")
        kode, _, err = self.jalan("--file", f, "--tanggal", TGL)
        self.assertNotEqual(kode, 0)
        self.assertIn("nilai_faktur", err)
        self.assertIn("Kolom di file: siapa, berapa, kapan", err)

    def test_jadwal_hubungan_dekat_tidak_dua_hari(self):
        # Uji usaha-offline 05: tetangga, telat 6 hari, 1x diingatkan -> jangan naik tahap dalam 2 hari.
        kode, out, err = self.jalan("--nominal", "Rp 1.350.000", "--jatuh-tempo", "2026-09-25", "--tanggal",
                                    "2026-10-01", "--sudah-diingatkan", "1", "--hubungan", "dekat", "--format", "json")
        self.assertEqual(kode, 0, err)
        j = json.loads(out)["jadwal"]
        self.assertEqual(j["jeda_hari"], 14)
        self.assertEqual(j["tenggat_bayar"], "2026-10-15")
        self.assertEqual(j["kirim_berikutnya"], "2026-10-16")
        self.assertIn("ajak bicara langsung", j["kalimat"])

    def test_jadwal_bisnis_kalimat_jelas(self):
        # Uji konsultan 03: telat 21 hari, 2x diingatkan -> tenggat Kamis 8 Okt, tahap 6 Jumat 9 Okt.
        kode, out, err = self.jalan("--nominal", "12000000", "--jatuh-tempo", "2026-09-10", "--tanggal",
                                    "2026-10-01", "--sudah-diingatkan", "2", "--format", "json")
        self.assertEqual(kode, 0, err)
        j = json.loads(out)["jadwal"]
        self.assertEqual(j["kalimat"], "Tenggat bayar di pesan ini: Kamis, 8 Oktober 2026 (7 hari dari 1 Oktober 2026). "
                                       "Jika sampai tanggal itu belum ada pembayaran atau kabar, pada Jumat, 9 Oktober 2026 "
                                       "kirim tahap 6.")



CSV_BERANTAKAN = """no nota,pelanggan,total,sdh bayar,jatuh tempo,keterangan
BM-101,Pak Slamet (ruko),"Rp 18.750.000","Rp 5.000.000",12/08/2026,sudah WA 2x (3 Sep & 20 Sep) janji bayar 30 Sep tidak ditepati
BM-102,CV Karya Mandiri,"Rp 42.300.000",0,5 Sep 2026,belum pernah ditagih
BM-103,Bu Ratna,2.350.000,,28/09/2026,pelanggan lama
BM-104,Pak Dedi,"Rp 1.275.000","Rp 275.000",15/10/2026,belum jatuh tempo
BM-105,UD Maju Jaya,"Rp 9.600.000","Rp 9.600.000",30/08/2026,lunas
BM-106,Pak Haji Umar,"Rp 27.800.000","Rp 10.000.000",01/07/2026,diingatkan 3x; janji bayar tidak ditepati
BM-107,PT Bangun Persada,"Rp 61.500.000",0,9 Okt 2026,termin 2
BM-108,Bu Wati,640rb,0,20/08/2026,tetangga
BM-109,Pak Anton,"5,2jt","Rp 1.000.000",18/09/2026,sudah diingatkan 1x
BM-110,CV Sinar Baja,"Rp 14.000.000",0,13/10/2026,belum jatuh tempo
"""


class UjiKolomPembayaran(unittest.TestCase):
    """v1.0.7 (uji OpenClaw 2026-10-10): kolom 'sdh bayar' dulu diabaikan diam-diam sehingga nota lunas
    tampil telat 41 hari. Sekarang kolom pembayaran dikenali, dikurangkan, dan yang tak terbaca diberi peringatan."""

    TGL2 = "2026-10-10"

    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def tulis(self, isi, nama="p.csv"):
        f = os.path.join(self.dir, nama)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(isi)
        return f

    def jalan(self, f, fmt="json", *extra):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        p = subprocess.run([sys.executable, SCRIPT, "--file", f, "--tanggal", self.TGL2, "--format", fmt, *extra],
                           capture_output=True, text=True, env=env)
        return p.returncode, p.stdout, p.stderr

    def rekap(self, isi, nama="p.csv"):
        kode, out, err = self.jalan(self.tulis(isi, nama))
        self.assertEqual(kode, 0, err)
        return json.loads(out)

    def test_csv_berantakan_sdh_bayar_angka_independen(self):
        from decimal import Decimal as D
        from datetime import date as Tgl
        h = self.rekap(CSV_BERANTAKAN)
        # pembanding independen (Decimal, ditulis tangan dari data di atas): (no, total, dibayar, jatuh tempo)
        data = [("BM-101", D(18750000), D(5000000), Tgl(2026, 8, 12)), ("BM-102", D(42300000), D(0), Tgl(2026, 9, 5)),
                ("BM-103", D(2350000), D(0), Tgl(2026, 9, 28)), ("BM-104", D(1275000), D(275000), Tgl(2026, 10, 15)),
                ("BM-105", D(9600000), D(9600000), Tgl(2026, 8, 30)), ("BM-106", D(27800000), D(10000000), Tgl(2026, 7, 1)),
                ("BM-107", D(61500000), D(0), Tgl(2026, 10, 9)), ("BM-108", D(640000), D(0), Tgl(2026, 8, 20)),
                ("BM-109", D(5200000), D(1000000), Tgl(2026, 9, 18)), ("BM-110", D(14000000), D(0), Tgl(2026, 10, 13))]
        hari_ini = Tgl(2026, 10, 10)
        jt = {n: j for n, _, _, j in data}
        sisa = {n: t - b for n, t, b, _ in data if t - b > 0}
        telat = {n: s for n, s in sisa.items() if (hari_ini - jt[n]).days > 0}
        self.assertEqual(h["total_piutang"], int(sum(sisa.values())))
        self.assertEqual(h["total_piutang"], 157540000)
        self.assertEqual(h["total_telat"], int(sum(telat.values())))
        self.assertEqual(h["total_telat"], 142540000)
        self.assertEqual(h["jumlah_invoice_telat"], 7)
        d = {x["no_invoice"]: x for x in h["daftar"]}
        self.assertNotIn("BM-105", d)  # nota lunas tidak ditagih
        for n, s in sisa.items():
            self.assertEqual(d[n]["sisa"], int(s), n)
            self.assertEqual(d[n]["hari_terlambat"], (hari_ini - jt[n]).days, n)
        self.assertEqual(d["BM-106"]["hari_terlambat"], 101)
        self.assertEqual([x["no_invoice"] for x in h["lunas_dikecualikan"]], ["BM-105"])
        self.assertEqual(h["kolom_dipakai"]["dibayar"], "sdh bayar")

    def test_riwayat_pengingat_dari_keterangan(self):
        h = self.rekap(CSV_BERANTAKAN)
        d = {x["no_invoice"]: x for x in h["daftar"]}
        self.assertEqual(d["BM-106"]["sudah_diingatkan"], 3)
        self.assertEqual(d["BM-101"]["sudah_diingatkan"], 2)
        self.assertEqual(d["BM-109"]["sudah_diingatkan"], 1)
        self.assertEqual(d["BM-102"]["sudah_diingatkan"], 0)
        self.assertEqual(d["BM-106"]["tahap_kode"], 6)   # 101 hari + 3 pengingat -> somasi
        self.assertEqual(d["BM-102"]["tahap_kode"], 5)   # 35 hari, belum pernah ditagih -> maks tahap 5
        self.assertTrue(any("dibaca dari" in c for c in d["BM-106"]["catatan"]))

    def test_pengingat_kolom_eksplisit_menang(self):
        h = self.rekap("pelanggan,total,sdh bayar,jatuh tempo,sudah_diingatkan,keterangan\n"
                       "A,1000000,0,2026-09-01,1,sudah WA 5x\n")
        self.assertEqual(h["daftar"][0]["sudah_diingatkan"], 1)

    def test_variasi_judul_kolom_dibayar(self):
        judul = ["sdh bayar", "Sudah Dibayar", "DIBAYAR", "sudah_dibayar", "Sdh_Dibayar", "SDH-BAYAR", "Terbayar",
                 "Uang Muka", "DP", "Pembayaran (Rp)", "sudahDibayar", "Sudah Dibayár", "Dibayarkan", "Cicilan",
                 "Angsuran", "Paid", "Amount Paid"]
        for j in judul:
            with self.subTest(judul=j):
                h = self.rekap('pelanggan,total,"%s",jatuh tempo\nA,"Rp 1.000.000","Rp 400.000",2026-09-01\n' % j)
                self.assertEqual(h["daftar"][0]["sisa"], 600000)
                self.assertEqual(h["peringatan"], [])

    def test_beberapa_kolom_pembayaran_dijumlah(self):
        h = self.rekap('pelanggan,total,DP,Cicilan 1,Cicilan 2,jatuh tempo\nA,1000000,100000,200000,"Rp 50.000",2026-09-01\n')
        self.assertEqual(h["daftar"][0]["dibayar"], 350000)
        self.assertEqual(h["daftar"][0]["sisa"], 650000)

    def test_lunas_penuh_dikecualikan_dari_total(self):
        h = self.rekap("pelanggan,total,dibayar,jatuh tempo\nA,1000000,1000000,2026-09-01\nB,500000,100000,2026-09-01\n")
        self.assertEqual([x["pelanggan"] for x in h["daftar"]], ["B"])
        self.assertEqual(h["total_piutang"], 400000)
        self.assertEqual(h["lunas_dikecualikan"][0]["pelanggan"], "A")

    def test_kolom_lunas_ya_tidak_dan_status(self):
        h = self.rekap("Pelanggan,Total,Lunas?,Status Pembayaran,Jatuh Tempo\n"
                       "A,1000000,ya,,2026-09-01\nB,500000,,belum lunas,2026-09-01\n"
                       "C,700000,,Lunas,2026-09-01\nD,100000,,,2026-09-01\nE,200000,,Lunas sebagian,2026-09-01\n"
                       "F,300000,tidak,,2026-09-01\n")
        self.assertEqual(sorted(x["pelanggan"] for x in h["daftar"]), ["B", "D", "E", "F"])
        self.assertEqual(sorted(x["pelanggan"] for x in h["lunas_dikecualikan"]), ["A", "C"])
        self.assertEqual(h["total_piutang"], 500000 + 100000 + 200000 + 300000)

    def test_kolom_mirip_pembayaran_tak_dikenal_beri_peringatan(self):
        isi = "pelanggan,total,sdh transfer,jatuh tempo\nA,1000000,400000,2026-09-01\n"
        h = self.rekap(isi)
        self.assertEqual(len(h["peringatan"]), 1)
        self.assertIn("⚠️", h["peringatan"][0])
        self.assertIn("sdh transfer", h["peringatan"][0])
        self.assertIn("TIDAK dikurangkan", h["peringatan"][0])
        kode, out, err = self.jalan(self.tulis(isi), "teks")
        self.assertEqual(kode, 0, err)
        self.assertTrue(out.startswith("⚠️"), out[:80])

    def test_isi_pembayaran_tak_terbaca_beri_peringatan_dan_baris_tetap_ada(self):
        h = self.rekap('pelanggan,total,sudah dibayar,jatuh tempo\nA,1000000,"transfer 3 okt",2026-09-01\nB,500000,100000,2026-09-01\n')
        d = {x["pelanggan"]: x for x in h["daftar"]}
        self.assertEqual(d["A"]["sisa"], 1000000)  # tidak diam-diam dibuang
        self.assertEqual(d["B"]["sisa"], 400000)
        self.assertTrue(any("⚠️" in c and "tidak terbaca" in c for c in d["A"]["catatan"]))
        self.assertTrue(any("tidak terbaca" in w and "baris 2" in w for w in h["peringatan"]))

    def test_tanda_hubung_dan_kosong_dianggap_nol_tanpa_peringatan(self):
        h = self.rekap("pelanggan,total,dibayar,jatuh tempo\nA,1000000,-,2026-09-01\nB,500000,,2026-09-01\nC,300000,nihil,2026-09-01\n")
        self.assertEqual(h["peringatan"], [])
        self.assertEqual(h["total_piutang"], 1800000)

    def test_tanggal_bayar_terisi_tapi_sisa_masih_ada_diperingatkan(self):
        h = self.rekap("pelanggan,total,tgl bayar,jatuh tempo\nA,1000000,03/10/2026,2026-09-01\n")
        self.assertTrue(any("tgl bayar" in c for c in h["daftar"][0]["catatan"]))

    def test_bayar_melebihi_tagihan_dilewati_dengan_alasan(self):
        h = self.rekap("pelanggan,total,dibayar,jatuh tempo\nA,1000000,1500000,2026-09-01\nB,500000,0,2026-09-01\n")
        self.assertEqual([x["pelanggan"] for x in h["daftar"]], ["B"])
        self.assertEqual(h["baris_dilewati"][0]["baris"], 2)
        self.assertIn("melebihi", h["baris_dilewati"][0]["alasan"])

    def test_kolom_sisa_beda_dari_hitungan_diperingatkan(self):
        h = self.rekap("pelanggan,total,dibayar,sisa,jatuh tempo\nA,1000000,400000,700000,2026-09-01\n")
        self.assertEqual(h["daftar"][0]["sisa"], 600000)
        self.assertTrue(any("beda dari hitungan" in c for c in h["daftar"][0]["catatan"]))

    def test_keterangan_lunas_tapi_sisa_masih_ada_diperingatkan(self):
        h = self.rekap("pelanggan,total,jatuh tempo,keterangan\nA,1000000,2026-09-01,lunas\nB,500000,2026-09-01,belum lunas\n")
        d = {x["pelanggan"]: x for x in h["daftar"]}
        self.assertTrue(any("menyebut lunas" in c for c in d["A"]["catatan"]))
        self.assertFalse(any("menyebut lunas" in c for c in d["B"]["catatan"]))

    def test_tanpa_kolom_pembayaran_diberi_catatan(self):
        h = self.rekap("pelanggan,total,jatuh tempo\nA,1000000,2026-09-01\n")
        self.assertTrue(any("tidak ada kolom pembayaran" in w for w in h["peringatan"]))

    def test_xlsx_sdh_bayar(self):
        f = os.path.join(self.dir, "p.xlsx")
        buat_xlsx(f, [["pelanggan", "total", "sdh bayar", "jatuh tempo"], ["Toko A", 6300000, 300000, 46270]])
        kode, out, err = self.jalan(f, "json", "--sheet", "Piutang")
        self.assertEqual(kode, 0, err)
        self.assertEqual(json.loads(out)["daftar"][0]["sisa"], 6000000)

    def test_kolom_dibayar_lama_tetap_sama(self):
        h = self.rekap("pelanggan,no_invoice,nominal,jatuh_tempo,dibayar\nCV B,INV-02,12500000,2026-08-24,2500000\n")
        self.assertEqual(h["daftar"][0]["sisa"], 10000000)


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
