"""Tes: python3 tests/uji_skor_matriks.py"""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import skor_matriks as m


class T(unittest.TestCase):
    def test_skor_manual(self):
        toko, k = m.parse("kriteria,bobot,Kita,A\nHarga,30,3,4\nMutu,70,4,2\n")
        h, _, _ = m.hitung(toko, k)
        self.assertEqual(h["Kita"]["skor"], round((30*3+70*4)/100, 2))  # 3.7
        self.assertEqual(h["A"]["skor"], 2.6)

    def test_kosong_dinormalkan(self):
        toko, k = m.parse("kriteria,bobot,Kita,A\nHarga,50,3,\nMutu,50,4,2\n")
        h, _, _ = m.hitung(toko, k)
        self.assertEqual(h["A"]["skor"], 2.0)
        self.assertEqual(h["A"]["cakupan_persen"], 50)
        self.assertEqual(h["A"]["kosong"], ["Harga"])

    def test_koma_desimal_dan_titik_koma(self):
        toko, k = m.parse("kriteria;bobot;Kita;A\nHarga;10;3,5;2\n")
        self.assertEqual(k[0]["nilai"]["Kita"], 3.5)

    def test_data_rusak(self):
        for buruk in ["kriteria,bobot,Kita,A\nH,10,6,2\n", "kriteria,bobot,Kita,A\nH,abc,3,2\n",
                      "kriteria,bobot,Kita,A\nH,10,x,2\n", "a,b,c\n1,2,3\n", "",
                      "kriteria,bobot,Kita,kita\nH,10,3,2\n", "kriteria,bobot,Kita,A\nH,0,3,2\n"]:
            with self.assertRaises(m.MatriksError, msg=buruk):
                m.parse(buruk)

    def test_unggul_tertinggal(self):
        toko, k = m.parse("kriteria,bobot,Kita,A,B\nHarga,50,2,4,4\nMutu,50,5,3,3\n")
        _, u, t = m.hitung(toko, k)
        self.assertEqual(u[0]["kriteria"], "Mutu"); self.assertEqual(u[0]["selisih_vs_rata_pesaing"], 2)
        self.assertEqual(t[0]["kriteria"], "Harga"); self.assertEqual(t[0]["selisih_vs_rata_pesaing"], -2)

    def test_peta_dan_sumbu_salah(self):
        toko, k = m.parse("kriteria,bobot,Kita,A\nHarga,50,2,4\nMutu,50,5,3\n")
        self.assertIn("0", m.peta(toko, k, "Harga", "Mutu"))
        with self.assertRaises(m.MatriksError):
            m.peta(toko, k, "Nggak ada", "Mutu")

    def test_cli(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write("kriteria,bobot,Kita,A\nHarga,10,3,2\n")
        self.assertEqual(m.main([f.name]), 0)
        self.assertEqual(m.main(["/tidak/ada.csv"]), 2)
        os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
