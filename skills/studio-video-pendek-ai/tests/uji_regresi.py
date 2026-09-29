#!/usr/bin/env python3
"""Uji regresi durasi_naskah.py. Jalankan: python3 tests/uji_regresi.py (Windows: py tests/uji_regresi.py)

Angka acuan dihitung manual: detik = kata / wpm x 60 + jeda; +0,3 dtk antar adegan (bukan setelah adegan terakhir).
"""
import contextlib
import io
import json
import os
import sys
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import durasi_naskah as d  # noqa: E402


def jalan(*args, stdin=None):
    out, err = io.StringIO(), io.StringIO()
    lama = sys.stdin
    if stdin is not None:
        sys.stdin = io.StringIO(stdin)
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = d.main(list(args))
    finally:
        sys.stdin = lama
    return kode, out.getvalue(), err.getvalue()


class Uji(unittest.TestCase):
    def test_hitung_kata(self):
        self.assertEqual(d.hitung_kata("Es kopi susu gula aren"), 5)
        self.assertEqual(d.hitung_kata("Cuma Rp15.000, murah-meriah!"), 3)

    def test_satu_adegan_150wpm(self):
        # 25 kata / 150 x 60 = 10,0 dtk
        teks = " ".join(["kata"] * 25)
        r, total = d.estimasi([("A", teks)], wpm=150)
        self.assertEqual(total, 10.0)

    def test_dua_adegan_dengan_jeda(self):
        # A: 15 kata = 6,0 + jeda 1,5 + 0,3 = 7,8 ; B: 10 kata = 4,0 -> total 11,8
        a = " ".join(["kata"] * 15) + " [jeda 1,5]"
        b = " ".join(["kata"] * 10)
        r, total = d.estimasi([("A", a), ("B", b)], wpm=150)
        self.assertEqual(r[0]["detik"], 7.8)
        self.assertEqual(total, 11.8)

    def test_jeda_default_setengah_detik(self):
        r, total = d.estimasi([("A", "[jeda]")], wpm=150)
        self.assertEqual(total, 0.5)
        self.assertEqual(r[0]["kata"], 0)

    def test_wpm_dapat_diatur(self):
        r, total = d.estimasi([("A", " ".join(["kata"] * 30))], wpm=180)
        self.assertEqual(total, 10.0)  # 30/180*60

    def test_peringatan_melebihi_target(self):
        teks = " ".join(["kata"] * 100)  # 40 dtk
        kode, out, _ = jalan("--teks", teks, "--target", "30")
        self.assertEqual(kode, 0)
        self.assertIn("MELEBIHI", out)
        self.assertIn("PERINGATAN", out)
        kode, _, _ = jalan("--teks", teks, "--target", "30", "--strict")
        self.assertEqual(kode, 1)

    def test_pas_dan_json(self):
        teks = " ".join(["kata"] * 70)  # 28 dtk
        kode, out, _ = jalan("--teks", teks, "--target", "30", "--json")
        data = json.loads(out)
        self.assertEqual(kode, 0)
        self.assertEqual(data["total_dtk"], 28.0)
        self.assertEqual(data["status"], "PAS")

    def test_stdin_label_dan_komentar(self):
        kode, out, _ = jalan("-", stdin="# catatan\nHook | Kopi ini bikin melek\n\nCTA | Klik keranjang kuning\n")
        self.assertEqual(kode, 0)
        self.assertIn("Hook", out)
        self.assertIn("CTA", out)

    def test_input_rusak(self):
        for args, stdin in [(("--teks", "   "), None), (("-",), "\n\n# saja\n"),
                            (("--teks", "a", "--wpm", "0"), None), (("--teks", "a", "--target", "-5"), None),
                            (("tidak_ada.txt",), None), ((), None)]:
            kode, _, err = jalan(*args, stdin=stdin)
            self.assertEqual(kode, 2, args)
            self.assertIn("Error", err)

    def test_wpm_nol_di_fungsi(self):
        with self.assertRaises(ValueError):
            d.estimasi([("A", "halo")], wpm=0)

    def test_v101_adegan_emoji_diperingatkan(self):
        kode, out, _ = jalan("--teks", "Hook | \U0001F600\U0001F525;;CTA | Klik keranjang kuning")
        self.assertEqual(kode, 0)
        self.assertIn("PERINGATAN: Adegan 'Hook'", out)
        self.assertNotIn("Adegan 'CTA' tidak punya", out)
        kode, out, _ = jalan("--teks", "Hook | \U0001F600;;B | halo", "--json")
        data = json.loads(out)
        self.assertEqual(len(data["peringatan"]), 1)
        self.assertEqual(data["adegan"][0]["kata"], 0)

    def test_v101_jeda_saja_tidak_diperingatkan(self):
        p = []
        d.estimasi([("A", "[jeda 2]")], peringatan=p)
        self.assertEqual(p, [])

    def test_v101_wpm_ekstrem(self):
        kode, _, err = jalan("--teks", "a b c", "--wpm", "5000")
        self.assertEqual(kode, 2)
        self.assertIn("tidak masuk akal", err)
        kode, _, err = jalan("--teks", "a b c", "--wpm", "10")
        self.assertEqual(kode, 2)
        kode, out, _ = jalan("--teks", "a b c", "--wpm", "300")     # di luar wajar tapi masih diterima
        self.assertEqual(kode, 0)
        self.assertIn("di luar kisaran wajar", out)
        kode, out, _ = jalan("--teks", "a b c", "--wpm", "150")
        self.assertNotIn("di luar kisaran wajar", out)

    def test_v101_jeda_bukan_angka(self):
        p = []
        r, total = d.estimasi([("A", "halo [jeda abc] dunia")], peringatan=p)
        self.assertEqual(r[0]["kata"], 2)                # "jeda abc" tidak dihitung sebagai kata
        self.assertEqual(r[0]["jeda_dtk"], 0.5)          # jeda bawaan
        self.assertEqual(len(p), 1)
        self.assertIn("[jeda abc]", p[0])
        r, _ = d.estimasi([("A", "x [jeda 1,5] y [JEDA] z")])
        self.assertEqual(r[0]["jeda_dtk"], 2.0)

    def test_v101_tabel_angka_besar_tidak_melebur(self):
        _, out, _ = jalan("--teks", "a [jeda 40000] b")
        baris = [b for b in out.splitlines() if b.startswith("Adegan 1")][0]
        self.assertEqual(baris.split()[-3:], ["2", "40000.0", "40000.8"])

    def test_v101_pesan_kependekan_tidak_menakutkan(self):
        _, out, _ = jalan("--teks", " ".join(["kata"] * 20), "--target", "45")
        self.assertIn("KEPENDEKAN", out)
        self.assertIn("wajar bila ada bagian visual tanpa suara", out)

    def test_v101_json_punya_peringatan_kosong(self):
        _, out, _ = jalan("--teks", " ".join(["kata"] * 10), "--json")
        self.assertEqual(json.loads(out)["peringatan"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
