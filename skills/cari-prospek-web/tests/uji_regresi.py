#!/usr/bin/env python3
"""Uji regresi saring_prospek.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import saring_prospek as s  # noqa: E402

CSV = """Nama Usaha,Kota,Bidang,Website,Telepon,Sumber URL,Catatan
PT Bersih Jaya Contoh,Surabaya,cleaning service gedung,https://www.bersihjaya.example,(031) 555-0101,https://bersihjaya.example/kontak,melayani kantor
Bersih Jaya Contoh,Surabaya,cleaning service,bersihjaya.example,,,
CV Rapi Selalu,Sidoarjo,laundry,,0812-3456-7890,https://direktori.example/rapi,
UD Tanpa Bukti,Surabaya,cleaning service kantor,,info@contoh.example,,
"""


def tmp(isi, mentah=None):
    p = os.path.join(tempfile.mkdtemp(), "p.csv")
    with open(p, "wb") as f:
        f.write(mentah if mentah is not None else isi.encode("utf-8"))
    return p


def jalan(*arg):
    o, e = io.StringIO(), io.StringIO()
    with redirect_stdout(o), redirect_stderr(e):
        kode = s.main(list(arg))
    return kode, o.getvalue(), e.getvalue()


class Uji(unittest.TestCase):
    def test_dedup_nama_mirip_dan_domain(self):
        rows = s.baca_csv(tmp(CSV))
        hasil, dobel = s.saring(rows, ["cleaning"], "surabaya")
        self.assertEqual(len(hasil), 3)
        self.assertEqual(len(dobel), 1)
        bj = [d for d in hasil if "Bersih" in d["nama"]][0]
        self.assertTrue(bj["sumber"])  # sumber baris asli dipertahankan

    def test_dedup_domain_sama_nama_beda(self):
        rows = [
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Alfa", "website": "http://www.x.example/a"},
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Omega Lain", "website": "x.example"},
        ]
        hasil, dobel = s.saring(rows, [])
        self.assertEqual((len(hasil), len(dobel)), (1, 1))

    def test_tanpa_sumber_ditandai_dan_skor_dibatasi(self):
        hasil, _ = s.saring(s.baca_csv(tmp(CSV)), ["cleaning", "kantor"], "surabaya")
        ud = [d for d in hasil if d["nama"].startswith("UD")][0]
        self.assertIn("TANPA SUMBER", ud["periksa"])
        self.assertLessEqual(ud["skor"], 30)

    def test_urutan_skor_dan_hp_ditandai(self):
        hasil, _ = s.saring(s.baca_csv(tmp(CSV)), ["cleaning"], "surabaya")
        self.assertEqual(hasil[0]["nama"], "PT Bersih Jaya Contoh")
        rapi = [d for d in hasil if "Rapi" in d["nama"]][0]
        self.assertIn("nomor HP", rapi["periksa"])
        self.assertTrue(all(0 <= d["skor"] <= 100 for d in hasil))

    def test_nilai_belum_terverifikasi_dianggap_tanpa_sumber(self):
        d = dict.fromkeys(s.KOLOM, "")
        d["sumber"] = "[belum terverifikasi]"
        self.assertFalse(s.punya_sumber(d))

    def test_kolom_bebas_dan_titik_koma(self):
        kode, out, _ = jalan(tmp("usaha;kota;url sumber\nToko A;Bali;https://a.example/x\n"), "--icp", "toko")
        self.assertEqual(kode, 0)
        self.assertIn("Toko A", out)

    def test_berkas_rusak_dan_kosong(self):
        self.assertEqual(jalan(tmp("", mentah=b""))[0], 2)
        self.assertEqual(jalan(tmp("a,b\n1,2\n"))[0], 2)  # tanpa kolom nama
        self.assertEqual(jalan(tmp("", mentah=b"\xff\xfe\x00bad\x80"))[0], 2)
        self.assertEqual(jalan("/tidak/ada.csv")[0], 2)

    def test_maks_dan_keluar(self):
        p = os.path.join(tempfile.mkdtemp(), "k.csv")
        kode, out, _ = jalan(tmp(CSV), "--maks", "1", "--keluar", p)
        self.assertEqual(kode, 0)
        self.assertEqual(len(out.strip().splitlines()), 2)
        self.assertTrue(os.path.exists(p))


if __name__ == "__main__":
    unittest.main()
