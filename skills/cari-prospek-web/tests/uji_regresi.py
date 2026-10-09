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
CV Rapi Selalu,Sidoarjo,laundry,,0813-5521-9047,https://direktori.example/rapi,
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

    def test_dummy_ditandai_dan_tanpa_skor(self):
        csvd = ("nama,kota,jenis,kontak,sumber,catatan\n"
                "Toko Satu,Bali,toko,0812 3456 7890,https://a.example/x,\n"
                "Toko Dua,Bali,toko,0812 7654 3210,https://b.example/x,\n"
                "Toko Tiga,Bali,toko,info@email.com,https://c.example/x,Jl. Mawar No. 123\n"
                "Toko Empat,Bali,toko,(0361) 555-0188,https://d.example/x,Lorem ipsum\n"
                "Toko Lima,Bali,toko,0821 4417 9035,https://e.example/x,\n")
        hasil, _ = s.saring(s.baca_csv(tmp(csvd)), ["toko"], "bali")
        per = {d["nama"]: d for d in hasil}
        for n in ("Toko Satu", "Toko Dua", "Toko Tiga", "Toko Empat"):
            self.assertIn("DUMMY?", per[n]["periksa"], n)
            self.assertEqual(per[n]["skor"], 0, n)
        self.assertNotIn("DUMMY?", per["Toko Lima"]["periksa"])
        self.assertGreater(per["Toko Lima"]["skor"], 0)

    def test_no_alamat_wajar_tidak_ditandai_dummy(self):
        for alamat, dummy in (("Jl. Mawar No. 1", False), ("Jl. Melati No. 12", False), ("Jl. Kenanga No. 45A", False),
                              ("Jl. Anggrek No. 123", True), ("Jl. Dahlia No. 12345", True), ("Jl. Tulip No. 000", True)):
            d = {**dict.fromkeys(s.KOLOM, ""), "nama": "Toko X", "catatan": alamat, "kontak": "(031) 555-0188"}
            self.assertEqual(bool(s.dummy(d)), dummy, alamat)

    def test_platform_bersama_bukan_kunci_dedup(self):
        rows = [
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Alfa Sejahtera", "website": "https://www.instagram.com/alfa"},
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Omega Lestari", "website": "https://instagram.com/omega"},
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Beta Makmur", "website": "https://www.google.com/maps/place/beta"},
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Gamma Abadi", "website": "https://maps.app.goo.gl/xyz"},
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Delta Utama", "website": "https://wa.me/6281200000000"},
            {**dict.fromkeys(s.KOLOM, ""), "nama": "Sigma Prima", "website": "https://wa.me/6281200000001"},
        ]
        hasil, dobel = s.saring(rows, [])
        self.assertEqual((len(hasil), len(dobel)), (6, 0))
        self.assertEqual(s.kunci_domain("https://linktr.ee/x"), "")
        self.assertEqual(s.kunci_domain("https://www.kopi.example/a"), "kopi.example")

    def test_alias_kolom_sumber(self):
        for h in ("tautan", "link", "maps", "Tautan Halaman (Maps/Situs)", "url"):
            rows = s.baca_csv(tmp("nama,kota,%s\nToko A,Bali,https://a.example/x\n" % h))
            self.assertEqual(rows[0]["sumber"], "https://a.example/x", h)

    def test_baris_tidak_rata_ditoleransi(self):
        p = tmp("nama;kota;sumber\nToko A;Bandung;https://a.example\nToko B;Bandung\nToko C;Bandung;https://c.example;sisa;lagi\n")
        pr = []
        rows = s.baca_csv(p, pr)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["sumber"], "")
        self.assertIn("https://c.example", rows[2]["sumber"])
        self.assertEqual(len(pr), 2)
        kode, out, err = jalan(p)
        self.assertEqual(kode, 0)
        self.assertIn("PERINGATAN: baris 3", err)
        self.assertIn("PERINGATAN: baris 4", err)

    def test_pesan_galat_bahasa_indonesia(self):
        kode, _, err = jalan("/tidak/ada.csv")
        self.assertEqual(kode, 2)
        self.assertIn("tidak ditemukan", err)
        _, _, err = jalan(tmp("a,b\n1,2\n"))
        self.assertIn("kolom nama usaha", err)

    def test_maks_dan_keluar(self):
        p = os.path.join(tempfile.mkdtemp(), "k.csv")
        kode, out, _ = jalan(tmp(CSV), "--maks", "1", "--keluar", p)
        self.assertEqual(kode, 0)
        self.assertEqual(len(out.strip().splitlines()), 2)
        self.assertTrue(os.path.exists(p))


if __name__ == "__main__":
    unittest.main()
