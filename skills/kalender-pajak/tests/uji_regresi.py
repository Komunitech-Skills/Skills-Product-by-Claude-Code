#!/usr/bin/env python3
"""Uji regresi kalender-pajak. Python standar saja.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)

Tanggal patokan pergeseran yang DIKONFIRMASI sumber luar (dicek 2026-09-25):
- SPT Masa PPh 21/Unifikasi masa Feb 2026: 20 Mar 2026 -> 25 Mar 2026 (libur & cuti Idulfitri) - DDTC/Kring Pajak.
- Setor PPh masa Apr 2026: 15 Mei 2026 (cuti bersama) -> 18 Mei 2026 - DDTC.
"""
import csv
import datetime as dt
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
SCRIPT = SINI / "scripts" / "kalender_pajak.py"
sys.path.insert(0, str(SINI / "scripts"))
import kalender_pajak as kp  # noqa: E402

STAMP = dt.datetime(2026, 9, 25, 1, 2, 3, tzinfo=dt.timezone.utc)


def jalan(*argv):
    data, _ = kp.jalankan([str(a) for a in argv], sekarang_utc=STAMP)
    return data.decode("utf-8")


def acara_json(*argv):
    return json.loads(jalan(*argv, "--format", "json"))["acara"]


def cari(acara, kewajiban, jenis, masa):
    hasil = [e for e in acara if e["kewajiban"] == kewajiban and e["jenis"] == jenis and e["masa"] == masa]
    assert len(hasil) == 1, (kewajiban, jenis, masa, hasil)
    return hasil[0]


class UjiPergeseran(unittest.TestCase):
    def setUp(self):
        self.a26 = acara_json("--profil", "pemberi-kerja,pemotong,badan-pkp,op-umkm", "--tahun", "2026")

    def test_tanpa_geser(self):
        e = cari(self.a26, "pph21", "setor", "Sep 2026")
        self.assertEqual(e["tanggal"], "2026-10-15")
        self.assertEqual(e["bergeser_karena"], [])

    def test_minggu(self):
        e = cari(self.a26, "pph21", "setor", "Feb 2026")  # 15 Mar 2026 Minggu
        self.assertEqual((e["tanggal_normal"], e["tanggal"]), ("2026-03-15", "2026-03-16"))

    def test_sabtu_minggu_libur_17_agustus(self):
        e = cari(self.a26, "pph21", "setor", "Jul 2026")  # 15 Agu Sab, 16 Min, 17 libur
        self.assertEqual(e["tanggal"], "2026-08-18")
        self.assertEqual(len(e["bergeser_karena"]), 3)

    def test_cuti_bersama_imlek(self):
        e = cari(self.a26, "unifikasi", "setor", "Jan 2026")  # 15 Min, 16 cuti, 17 Imlek
        self.assertEqual(e["tanggal"], "2026-02-18")
        self.assertTrue(any("Cuti bersama" in x for x in e["bergeser_karena"]))

    def test_lebaran_2026_dikonfirmasi_ddtc(self):
        for k in ("pph21", "unifikasi"):
            e = cari(self.a26, k, "lapor", "Feb 2026")
            self.assertEqual(e["tanggal"], "2026-03-25", k)

    def test_cuti_bersama_mei_2026_dikonfirmasi_ddtc(self):
        e = cari(self.a26, "pph-final-umkm", "setor", "Apr 2026")
        self.assertEqual(e["tanggal"], "2026-05-18")

    def test_libur_beruntun_mei_2027(self):
        a = acara_json("--profil", "pph25", "--tahun", "2027", "--bulan-mulai", "5", "--jumlah-bulan", "1")
        e = cari(a, "pph25", "setor", "Apr 2027")  # 15 Sab .. 20 Waisak -> 21 Jumat
        self.assertEqual(e["tanggal"], "2027-05-21")
        self.assertEqual(len(e["bergeser_karena"]), 6)

    def test_hasil_selalu_hari_kerja(self):
        libur, _ = kp.muat_libur()
        a = acara_json("--profil", "pemberi-kerja,pemotong,badan-pkp,op-umkm", "--tahun", "2026",
                       "--jumlah-bulan", "24")
        for e in a:
            if e["jenis"] == "tahunan":
                continue
            t = dt.date.fromisoformat(e["tanggal"])
            self.assertLess(t.weekday(), 5, e)
            self.assertNotIn(t, libur, e)


class UjiAkhirBulan(unittest.TestCase):
    def test_ppn_februari_biasa_dan_kabisat(self):
        a = acara_json("--profil", "ppn", "--tahun", "2027", "--bulan-mulai", "2", "--jumlah-bulan", "2")
        e = cari(a, "ppn", "setor+lapor", "Jan 2027")  # 28 Feb 2027 Minggu -> 1 Mar
        self.assertEqual((e["tanggal_normal"], e["tanggal"]), ("2027-02-28", "2027-03-01"))
        # 2028 kabisat: 29 Feb 2028 Selasa (tanpa data libur 2028 -> peringatan)
        d = json.loads(jalan("--profil", "ppn", "--tahun", "2028", "--bulan-mulai", "2", "--jumlah-bulan", "1",
                             "--format", "json"))
        e = cari(d["acara"], "ppn", "setor+lapor", "Jan 2028")
        self.assertEqual(e["tanggal_normal"], "2028-02-29")
        self.assertIn("2028", d["peringatan"])

    def test_ppn_30_hari(self):
        a = acara_json("--profil", "ppn", "--tahun", "2026", "--bulan-mulai", "9", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "ppn", "setor+lapor", "Agu 2026")["tanggal"], "2026-09-30")

    def test_desember_ke_tahun_berikutnya(self):
        a = acara_json("--profil", "pemberi-kerja,ppn", "--tahun", "2027", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "pph21", "setor", "Des 2026")["tanggal"], "2027-01-15")
        self.assertEqual(cari(a, "pph21", "lapor", "Des 2026")["tanggal"], "2027-01-20")
        # masa Nov 2026 PPN: 31 Des 2026 Kamis -> tetap
        a2 = acara_json("--profil", "ppn", "--tahun", "2026", "--bulan-mulai", "12", "--jumlah-bulan", "1")
        self.assertEqual(cari(a2, "ppn", "setor+lapor", "Nov 2026")["tanggal"], "2026-12-31")

    def test_desember_2027_lintas_tahun_ke_2028(self):
        # PPN masa Nov 2027: 31 Des 2027 Jumat (hari kerja). Masa Des 2027 PPh 21 setor 15 Jan 2028 Sabtu -> 17 Jan
        a = acara_json("--profil", "pph21", "--tahun", "2028", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "pph21", "setor", "Des 2027")["tanggal"], "2028-01-17")


class UjiTahunan(unittest.TestCase):
    def test_spt_op_tidak_bergeser(self):
        a = acara_json("--profil", "spt-op", "--tahun", "2027")
        e = cari(a, "spt-op", "tahunan", "Tahun pajak 2026")
        self.assertEqual(e["tanggal"], "2027-03-31")

    def test_spt_badan_akhir_april(self):
        a = acara_json("--profil", "spt-badan", "--tahun", "2027")
        self.assertEqual(cari(a, "spt-badan", "tahunan", "Tahun pajak 2026")["tanggal"], "2027-04-30")

    def test_bukti_a1_hari_libur_ditandai(self):
        md = jalan("--profil", "bukti-a1", "--tahun", "2026", "--jumlah-bulan", "1")
        self.assertIn("Sabtu, 31 Januari 2026", md)
        self.assertIn("TIDAK bergeser", md)


class UjiHariIni(unittest.TestCase):
    def test_14_hari(self):
        md = jalan("--profil", "badan-pkp,pemberi-kerja", "--hari-ini", "2026-10-10")
        self.assertIn("5 hari lagi", md)  # 15 Okt
        self.assertIn("10 hari lagi", md)  # 20 Okt
        self.assertNotIn("Nov 2026", md)

    def test_hari_ini_dan_besok(self):
        md = jalan("--profil", "pph21", "--hari-ini", "2026-10-14", "--rentang", "1")
        self.assertIn("besok", md)
        md = jalan("--profil", "pph21", "--hari-ini", "2026-10-15", "--rentang", "1")
        self.assertIn("HARI INI", md)

    def test_kosong(self):
        md = jalan("--profil", "spt-op", "--hari-ini", "2026-09-25")
        self.assertIn("Tidak ada tenggat", md)


class UjiIcs(unittest.TestCase):
    def setUp(self):
        self.teks = jalan("--profil", "badan-pkp,pemberi-kerja,pemotong", "--tahun", "2026", "--format", "ics")

    def test_crlf_dan_panjang_baris(self):
        raw = self.teks.encode("utf-8")
        self.assertTrue(raw.endswith(b"\r\n"))
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        for baris in raw.split(b"\r\n"):
            self.assertLessEqual(len(baris), 75)
            baris.decode("utf-8")  # lipatan tidak memotong karakter multi-byte

    def urai(self):
        lines = self.teks.split("\r\n")
        gabung = []
        for l in lines:
            if l.startswith(" ") and gabung:
                gabung[-1] += l[1:]
            elif l:
                gabung.append(l)
        return gabung

    def test_struktur(self):
        g = self.urai()
        self.assertEqual(g[0], "BEGIN:VCALENDAR")
        self.assertEqual(g[-1], "END:VCALENDAR")
        self.assertIn("VERSION:2.0", g)
        self.assertTrue(any(x.startswith("PRODID:") for x in g))
        self.assertEqual(g.count("BEGIN:VEVENT"), g.count("END:VEVENT"))
        self.assertEqual(g.count("BEGIN:VALARM"), 2 * g.count("BEGIN:VEVENT"))
        self.assertIn("TRIGGER:-P2DT15H", g)
        self.assertIn("TRIGGER:-PT15H", g)
        uids = [x for x in g if x.startswith("UID:")]
        self.assertEqual(len(uids), len(set(uids)))
        self.assertEqual(len(uids), g.count("BEGIN:VEVENT"))
        for x in g:
            if x.startswith(("DTSTART", "DTEND")):
                self.assertRegex(x, r"^DT(START|END);VALUE=DATE:\d{8}$")
            if x.startswith("DTSTAMP:"):
                self.assertEqual(x, "DTSTAMP:20260925T010203Z")

    def test_dtend_hari_berikut(self):
        g = self.urai()
        mulai = [x.split(":")[1] for x in g if x.startswith("DTSTART")]
        akhir = [x.split(":")[1] for x in g if x.startswith("DTEND")]
        for s, e in zip(mulai, akhir):
            d0 = dt.datetime.strptime(s, "%Y%m%d").date()
            self.assertEqual(dt.datetime.strptime(e, "%Y%m%d").date(), d0 + dt.timedelta(days=1))

    def test_escape(self):
        self.assertEqual(kp.ics_escape("a,b;c\\d\ne"), "a\\,b\\;c\\\\d\\ne")
        g = self.urai()
        for x in g:
            if x.startswith(("SUMMARY:", "DESCRIPTION:")):
                isi = x.split(":", 1)[1]
                # koma/titik koma harus ter-escape
                self.assertIsNone(re.search(r"(?<!\\)[,;]", isi.replace("\\\\", "")), x)

    def test_uid_stabil(self):
        lain = jalan("--profil", "badan-pkp,pemberi-kerja,pemotong", "--tahun", "2026", "--format", "ics")
        uid1 = [x for x in self.urai() if x.startswith("UID:")]
        uid2 = [x for x in lain.split("\r\n") if x.startswith("UID:")]
        self.assertEqual(uid1, uid2)
        # masa yang sama dari rentang berbeda -> UID sama (impor ulang tidak dobel)
        sebagian = jalan("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1",
                         "--format", "ics")
        u = [x for x in sebagian.split("\r\n") if x.startswith("UID:")]
        self.assertTrue(set(u) <= set(uid1))

    def test_lipat_utf8(self):
        panjang = "DESCRIPTION:" + "é" * 100
        hasil = kp.ics_lipat(panjang)
        for b in hasil.split("\r\n"):
            self.assertLessEqual(len(b.encode("utf-8")), 75)
        self.assertEqual(hasil.replace("\r\n ", ""), panjang)


class UjiCsvDanInputBuruk(unittest.TestCase):
    def test_csv(self):
        teks = jalan("--profil", "op-umkm", "--tahun", "2026", "--format", "csv")
        rows = list(csv.DictReader(io.StringIO(teks)))
        self.assertEqual(rows[0]["tanggal"], "2026-01-15")
        self.assertIn("keterangan_geser", rows[0])

    def cli(self, *argv):
        return subprocess.run([sys.executable, str(SCRIPT)] + list(argv), stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    def test_input_buruk_tanpa_traceback(self):
        kasus = [["--profil", "toko-kue"], ["--profil", "op-umkm", "--bulan-mulai", "13"],
                 ["--profil", "op-umkm", "--bulan-mulai", "nol"], ["--profil", "op-umkm", "--tahun", "1999"],
                 ["--profil", "op-umkm", "--hari-ini", "31-12-2026"], ["--profil", "op-umkm", "--format", "pdf"],
                 [], ["--profil", "op-umkm", "--jumlah-bulan", "0"], ["--opsi-ngawur"],
                 ["--profil", "op-umkm", "--libur", "tidak-ada.csv"]]
        for k in kasus:
            p = self.cli(*k)
            self.assertEqual(p.returncode, 2, k)
            err = p.stderr.decode("utf-8")
            self.assertIn("ERROR:", err, k)
            self.assertNotIn("Traceback", err, k)

    def test_file_libur_rusak(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "rusak.csv"
            f.write_text("tanggal,jenis\n2028-13-40,libur\n", encoding="utf-8")
            p = self.cli("--profil", "op-umkm", "--libur", str(f))
            self.assertEqual(p.returncode, 2)
            self.assertIn("baris 2", p.stderr.decode("utf-8"))

    def test_file_libur_tambahan_dipakai(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "libur-2028.csv"
            f.write_text("tanggal,jenis,keterangan\n2028-02-15,libur,Contoh libur\n", encoding="utf-8")
            a = json.loads(jalan("--profil", "pph21", "--tahun", "2028", "--bulan-mulai", "2",
                                 "--jumlah-bulan", "1", "--libur", str(f), "--format", "json"))
            e = cari(a["acara"], "pph21", "setor", "Jan 2028")
            self.assertEqual(e["tanggal"], "2028-02-16")
            self.assertIsNone(a["peringatan"])

    def test_tahun_tanpa_data_peringatan_stderr(self):
        p = self.cli("--profil", "op-umkm", "--tahun", "2029", "--format", "ics")
        self.assertEqual(p.returncode, 0)
        self.assertIn("2029", p.stderr.decode("utf-8"))

    def test_keluar_file(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "pajak.ics"
            p = self.cli("--profil", "op-umkm", "--tahun", "2026", "--format", "ics", "--keluar", str(f))
            self.assertEqual(p.returncode, 0)
            self.assertTrue(f.read_bytes().startswith(b"BEGIN:VCALENDAR\r\n"))

    def test_nama_bulan(self):
        a = acara_json("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "Oktober", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "pph21", "setor", "Sep 2026")["tanggal"], "2026-10-15")

    def test_daftar_profil(self):
        p = self.cli("--daftar-profil")
        self.assertEqual(p.returncode, 0)
        self.assertIn("badan-pkp", p.stdout.decode("utf-8"))

    def test_data_libur_lengkap(self):
        libur, tahun = kp.muat_libur()
        self.assertEqual(tahun, {2026, 2027})
        n26 = [t for t in libur if t.year == 2026]
        n27 = [t for t in libur if t.year == 2027]
        self.assertEqual(len(n26), 17 + 8)
        self.assertEqual(len(n27), 18 + 8)


if __name__ == "__main__":
    unittest.main(verbosity=1)
