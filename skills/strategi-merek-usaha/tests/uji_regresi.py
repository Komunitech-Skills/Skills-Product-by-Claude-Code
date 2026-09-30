#!/usr/bin/env python3
"""Uji skor_nama.py & hitung_penawaran.py. Jalankan: python3 tests/uji_regresi.py (Windows: py tests/uji_regresi.py).
Angka diverifikasi dengan hitungan tangan (dicek di komentar)."""
import contextlib, io, os, sys, tempfile, unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import skor_nama as N  # noqa: E402
import hitung_penawaran as H  # noqa: E402


def jalan(mod, *argv):
    o, e = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e):
        k = mod.main(list(argv))
    return k, o.getvalue(), e.getvalue()


def tulis(isi, akhiran=".csv", mode="w", enc="utf-8"):
    f = tempfile.NamedTemporaryFile(mode, suffix=akhiran, delete=False, encoding=None if "b" in mode else enc)
    f.write(isi)
    f.close()
    return f.name


class UjiNama(unittest.TestCase):
    def test_suku_kata(self):
        # sam-bal=2, nu-sa=2 ; pu-lau=2 (au diftong akhir) ; ku-at... tiap vokal 1 -> 2 ; KPK (tanpa vokal) = 3
        self.assertEqual(N.suku_kata("Sambal Nusa"), 4)
        self.assertEqual(N.suku_kata("Pulau"), 2)
        self.assertEqual(N.suku_kata("Kuat"), 2)
        self.assertEqual(N.suku_kata("KPK"), 3)
        self.assertEqual(N.suku_kata("Santai"), 2)  # san-tai
        self.assertEqual(N.suku_kata("123"), 0)

    def test_panjang_dan_ejaan(self):
        self.assertEqual(N.skor_panjang(8), 5)
        self.assertEqual(N.skor_panjang(9), 4)
        self.assertEqual(N.skor_panjang(16), 1)
        self.assertEqual(N.skor_ejaan("Kopi Kita")[0], 5)
        self.assertEqual(N.skor_ejaan("Kopi 99")[0], 3)      # angka -2
        self.assertEqual(N.skor_ejaan("Xylo")[0], 3)         # q/x -1 dan 'xyl' 3 konsonan -1
        self.assertEqual(N.skor_ejaan("Bangsa")[0], 5)       # ng bukan kluster

    def test_kemiripan(self):
        s, m, r = N.kemiripan("Indomi", ["Indomie"])
        self.assertEqual(s, 1)  # ratio 2*6/13=0.923
        self.assertEqual(m, "Indomie")
        s2, _, _ = N.kemiripan("Warung Bintang", ["Indomie"])
        self.assertEqual(s2, 5)
        s3, _, _ = N.kemiripan("Kopi Kenangan Senja", ["Kopi Kenangan"])
        self.assertEqual(s3, 1)  # mengandung merek

    def test_skor_total_tangan(self):
        # nama "Kopi Kita": huruf=8 ->5 ; suku ko-pi-ki-ta=4 ->4 ; ejaan 5 ; tanpa merek kemiripan 3
        # manual 4,4,4. Bobot awal: (10*5+10*4+10*5+20*3+20*4+15*4+15*4)/100*20 = 400/100*20 = 80.0
        f = tulis("nama,aman_makna,khas,relevan\nKopi Kita,4,4,4\n")
        k, o, e = jalan(N, f, "--format", "json")
        self.assertEqual(k, 0)
        import json
        self.assertEqual(json.loads(o)["hasil"][0]["skor"], 80.0)

    def test_bobot_kustom(self):
        # hanya khas dan relevan berbobot 1: (4+2)/2*20 = 60
        f = tulis("nama,khas,relevan\nKopi Kita,4,2\n")
        k, o, _ = jalan(N, f, "--bobot", "panjang=0,suku_kata=0,ejaan=0,kemiripan=0,aman_makna=0,khas=1,relevan=1", "--format", "json")
        import json
        self.assertEqual(k, 0)
        self.assertEqual(json.loads(o)["hasil"][0]["skor"], 60.0)

    def test_tandai_makna_dan_mirip(self):
        f = tulis("nama,aman_makna\nBaguz,1\nKopi Kita,5\n")
        k, o, _ = jalan(N, f)
        self.assertIn("TANDAI: arti/konotasi negatif", o)
        self.assertIn("Teratas yang layak dicek: 'Kopi Kita'", o)

    def test_seri(self):
        f = tulis("nama,aman_makna,khas,relevan\nKopi Kita,4,4,4\nTeh Kita,4,4,4\n")
        k, o, _ = jalan(N, f)
        self.assertIn("SETARA", o)

    def test_merek_file_dan_bom(self):
        m = tulis("﻿Indomie\nKopi Kenangan\n", ".txt")
        f = tulis("﻿nama\nKopi Kenangan Baru\n")
        k, o, _ = jalan(N, f, "--merek-file", m)
        self.assertEqual(k, 0)
        self.assertIn("TANDAI: terlalu mirip", o)

    def test_data_rusak(self):
        casos = [
            ("", "kosong"), ("judul\nA\n", "kolom 'nama'"), ("nama\n", "tidak berisi nama"),
            ("nama,khas\nA,9\n", "1-5"), ("nama,khas\nA,abc\n", "bukan angka"), ("nama,khas\nA,2.5\n", "1-5"),
            ("nama\nKopi Kita\nkopi  kita\n", "nama ganda"), ("nama,foo\nA,1\n", "tidak dikenal"),
            ("nama,khas\n,3\n", "nama kosong"), ("nama\nA,b,c\n", "tanda kutip"),
        ]
        for isi, kata in casos:
            k, _, e = jalan(N, tulis(isi))
            self.assertEqual(k, 2, isi)
            self.assertIn(kata, e, isi)

    def test_argumen_rusak(self):
        f = tulis("nama\nKopi Kita\n")
        self.assertEqual(jalan(N, f, "--bobot", "khas=abc")[0], 2)
        self.assertEqual(jalan(N, f, "--bobot", "xyz=1")[0], 2)
        self.assertEqual(jalan(N, f, "--bobot", "khas=-1")[0], 2)
        self.assertEqual(jalan(N, f, "--bobot", "panjang=0,suku_kata=0,ejaan=0,kemiripan=0,aman_makna=0,khas=0,relevan=0")[0], 2)
        self.assertEqual(jalan(N, f, "--bobot", "khas=nan")[0], 2)
        self.assertEqual(jalan(N, "/tidak/ada.csv")[0], 2)
        self.assertEqual(jalan(N)[0], 2)
        self.assertEqual(jalan(N, f, "--merek-file", "/tidak/ada.txt")[0], 2)

    def test_tanpa_singkatan_opsi(self):
        # allow_abbrev=False: --bob tidak boleh dianggap --bobot
        f = tulis("nama\nKopi Kita\n")
        k, _, _ = jalan(N, f, "--bob", "khas=1")
        self.assertEqual(k, 2)

    def test_file_biner(self):
        f = tulis(b"\xff\xfe\x00bad", ".csv", "wb")
        self.assertEqual(jalan(N, f)[0], 2)

    def test_hitung(self):
        k, o, _ = jalan(N, "--hitung", "Sambal Nusa")
        self.assertEqual(k, 0)
        self.assertIn("suku kata: 4", o)


class UjiPenawaran(unittest.TestCase):
    def test_hitungan_tangan(self):
        # harga 45.000, diskon 10% -> 40.500 ; platform 8% -> 3.240 ; hpp 22.000 ; bonus 500+800=1.300 ; refund 3% -> 1.215
        # laba = 40.500-3.240-22.000-1.300-1.215 = 12.745 ; margin = 31.47% -> 31.5
        r = H.hitung(45000, 22000, 10, 8, [("a", 500), ("b", 800)], 3, 20)
        self.assertEqual(r["harga_tayang"], 40500)
        self.assertEqual(r["laba_per_unit"], 12745)
        self.assertEqual(r["margin_persen"], 31.5)
        # ruang bonus: (40.500-3.240-22.000-1.215)=14.045 ; minus 20% x 40.500 = 8.100 -> 5.945
        self.assertEqual(r["ruang_bonus_maks"], 5945)
        self.assertTrue(r["memenuhi_margin_minimal"])

    def test_pembulatan(self):
        # 999 x (1-0.15) = 849.15 -> 849 ; platform 7% = 59.43 -> 59
        r = H.hitung(999, 500, 15, 7)
        self.assertEqual(r["harga_tayang"], 849)
        self.assertEqual(r["biaya_platform"], 59)
        self.assertEqual(H.bulat(2.5), 3)

    def test_rugi_dan_peringatan(self):
        k, o, _ = jalan(H, "--harga", "30000", "--hpp", "25000", "--diskon", "20", "--platform", "10")
        # tayang 24.000 ; fee 2.400 ; laba = 24.000-2.400-25.000 = -3.400
        self.assertEqual(k, 0)
        self.assertIn("-Rp3.400", o)
        self.assertIn("RUGI", o)

    def test_input_rusak(self):
        for arg in (["--harga", "0", "--hpp", "1"], ["--harga", "-5", "--hpp", "1"], ["--harga", "abc", "--hpp", "1"],
                    ["--harga", "100", "--hpp", "1", "--diskon", "100"], ["--harga", "100", "--hpp", "1", "--diskon", "120"],
                    ["--harga", "100", "--hpp", "1", "--bonus", "tanpa-biaya"], ["--harga", "100", "--hpp", "1", "--bonus", "A=xx"],
                    ["--harga", "100", "--hpp", "1", "--bonus", "A=-5"], ["--harga", "nan", "--hpp", "1"],
                    ["--harga", "100", "--hpp", "-1"], ["--hpp", "1"], ["--harga", "100", "--hpp", "1", "--platfor", "5"],
                    ["--harga", "100", "--hpp", "1", "--margin-minimal", "100"]):
            self.assertEqual(jalan(H, *arg)[0], 2, arg)


if __name__ == "__main__":
    unittest.main(verbosity=1)
