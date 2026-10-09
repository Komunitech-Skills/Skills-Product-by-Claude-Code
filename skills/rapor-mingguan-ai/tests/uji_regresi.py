#!/usr/bin/env python3
"""Uji regresi rapor.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

RAKIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAKIT / "scripts"))
import rapor as r  # noqa: E402


def jalan(isi, *opsi, nama="x.txt", mentah=None):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, nama)
        with open(path, "wb") as f:
            f.write(mentah if mentah is not None else isi.encode("utf-8"))
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            kode = r.main([path, "--json", *opsi])
        return kode, out.getvalue(), err.getvalue()


def blok(i, pel, bot, gagal):
    return "---\nid: %s\nPelanggan: %s\nBot: %s\n#gagal: %s\n" % (i, pel, bot, gagal)


class Uji(unittest.TestCase):
    def test_hitung_dasar(self):
        teks = "".join(blok("A%d" % i, "tanya", "jawab", "lolos") for i in range(8)) + blok("B1", "x", "y", "konteks") + blok("B2", "x", "y", "lupa, panjang") + "---\n"
        k, out, _ = jalan(teks)
        self.assertEqual(k, 0)
        h = json.loads(out)
        self.assertEqual(h["dinilai"], 10)
        self.assertEqual(h["lolos_persen"]["konteks"], 80.0)
        self.assertEqual(h["lolos_persen"]["panjang"], 90.0)
        self.assertEqual(h["percakapan_bersih"], 8)
        self.assertEqual(h["tiga_kesalahan_teratas"][0]["kode"], "konteks")

    def test_kritis_membatasi_nilai_umum(self):
        teks = "".join(blok("A%d" % i, "t", "j", "lolos") for i in range(19)) + blok("Z", "t", "j", "bocor")
        h = json.loads(jalan(teks)[1])
        self.assertEqual(h["lolos_persen"]["bocor"], 95.0)
        self.assertEqual(h["nilai_umum"], "C")
        self.assertEqual(h["kena_kriteria_kritis"], ["bocor"])

    def test_predikat(self):
        self.assertEqual(r.predikat(90, False), "A")
        self.assertEqual(r.predikat(89.9, False), "B")
        self.assertEqual(r.predikat(59, False), "D")
        self.assertEqual(r.predikat(99, True), "B")
        self.assertEqual(r.predikat(100, True), "A")
        self.assertEqual(r.predikat(80, True), "D")

    def test_tren_dari_string_dan_json(self):
        teks = "".join(blok("A%d" % i, "t", "j", "lolos") for i in range(9)) + blok("B", "t", "j", "nada")
        h = json.loads(jalan(teks, "--lama", "nada=95,fakta=100%")[1])
        nada = [k for k in h["kriteria"] if k["kode"] == "nada"][0]
        self.assertEqual(nada["selisih_poin"], -5.0)
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "lama.json")
            with open(p, "w") as f:
                json.dump({"lolos_persen": {"nada": 50}}, f)
            h2 = json.loads(jalan(teks, "--lama", p)[1])
            self.assertEqual([k for k in h2["kriteria"] if k["kode"] == "nada"][0]["selisih_poin"], 40.0)

    def test_samarkan(self):
        s = r.samarkan("Hubungi Bu Rina di 0812-3456-7788 atau rina@mail.com, resi 1234567890123456", ["Wulan"])
        self.assertNotIn("3456", s)
        self.assertNotIn("rina@mail.com", s)
        self.assertNotIn("Rina", s)
        self.assertIn("0812-xxxx-7788", s)
        self.assertNotIn("1234567890123456", s)
        self.assertEqual(r.samarkan("halo Wulan", ["Wulan"]), "halo [nama]")

    def test_contoh_rapor_tersamar(self):
        teks = blok("A", "Saya Bu Rina 0812-3456-7788 tanya", "ok", "fakta") + "---\n"
        out = jalan(teks)[1]
        self.assertNotIn("3456", out)
        self.assertNotIn("Rina", out)

    def test_dugaan_mekanis(self):
        c = {"turn": [["pelanggan", "ada diskon?"], ["bot", "Pasti dijamin! Lihat file json di /home/x. Hubungi 0812-1111-2222"]]}
        d = r.dugaan(c, 700)
        self.assertEqual(set(d), {"janji", "teknis", "bocor"})
        c2 = {"turn": [["pelanggan", "nomor saya 0812-1111-2222"], ["bot", "Baik, saya catat 0812-1111-2222"]]}
        self.assertNotIn("bocor", r.dugaan(c2, 700))
        self.assertIn("panjang", r.dugaan({"turn": [["bot", "x" * 800]]}, 700))
        self.assertNotIn("teknis", r.dugaan({"turn": [["bot", "Sesi konsultasi 60 menit, log kunjungan"]]}, 700))

    def test_belum_dinilai_tidak_dihitung(self):
        teks = blok("A", "t", "j", "lolos") + "---\nid: B\nPelanggan: t\nBot: Pasti sembuh!\n---\n"
        h = json.loads(jalan(teks)[1])
        self.assertEqual(h["dinilai"], 1)
        self.assertEqual(h["belum_dinilai"], 1)
        self.assertTrue(h["dugaan_pada_yang_belum_dinilai"])
        self.assertTrue(any("indikatif" in p for p in h["peringatan"]))

    def test_kode_tak_dikenal(self):
        h = json.loads(jalan(blok("A", "t", "j", "ngaco, nada"))[1])
        self.assertEqual(h["kriteria"][4]["gagal"], 1)
        self.assertTrue(any("tidak dikenal" in p for p in h["peringatan"]))

    def test_csv_digabung_per_id(self):
        csvt = "id,pelanggan,bot,gagal\nA,halo,hai,lolos\nA,harga?,ya,konteks\nB,x,y,\n"
        k, out, _ = jalan(csvt, nama="x.csv")
        h = json.loads(out)
        self.assertEqual(h["percakapan_total"], 2)
        self.assertEqual(h["dinilai"], 1)

    def test_csv_peran_pesan(self):
        csvt = "id,peran,pesan,gagal\nA,Pelanggan,halo,\nA,Bot,hai,nada\n"
        h = json.loads(jalan(csvt, nama="x.csv")[1])
        self.assertEqual(h["kriteria"][4]["gagal"], 1)

    def test_berkas_buruk(self):
        self.assertEqual(jalan("", mentah=b"")[0], 2)
        self.assertEqual(jalan("   \n\n")[0], 2)
        self.assertEqual(jalan("", mentah=b"\xff\xfe\x00\x01garbage")[0] in (0, 2), True)
        k, _, err = jalan("bebas tanpa pemisah")
        self.assertEqual(k, 0)
        k2 = r.main(["/tidak/ada.txt"])
        self.assertEqual(k2, 2)

    def test_blok_agent_ada_penanda(self):
        out = io.StringIO()
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "a.txt")
            with open(p, "w") as f:
                f.write(blok("A", "t", "j", "lolos"))
            with redirect_stdout(out):
                r.main([p])
        self.assertIn("UNTUK AGENT SAJA", out.getvalue())

    def test_nol_dinilai(self):
        h = json.loads(jalan("---\nPelanggan: a\nBot: b\n---\n")[1])
        self.assertEqual(h["dinilai"], 0)
        self.assertIsNone(h["nilai_umum"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
