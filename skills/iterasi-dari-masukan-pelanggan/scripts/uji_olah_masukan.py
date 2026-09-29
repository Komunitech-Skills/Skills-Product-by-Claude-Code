#!/usr/bin/env python3
"""Uji otomatis olah_masukan.py (Python standar). Jalankan: python3 scripts/uji_olah_masukan.py"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import olah_masukan as om  # noqa: E402


class Opsi:
    staf_list = []
    kolom_teks = kolom_bintang = kolom_tanggal = None
    contoh = 3
    min_bulan = 5


def tulis(dir_, nama, isi):
    p = os.path.join(dir_, nama)
    with open(p, "w", encoding="utf-8") as f:
        f.write(isi)
    return p


class UjiSamarkan(unittest.TestCase):
    def test_hp_email_tautan_akun(self):
        t = om.samarkan("Hubungi 0812-3456-7890 atau +62 857 1234 5678, email a.b@x.co.id, lihat https://x.id/p?1 @budi_s")
        for bocor in ("0812", "857", "a.b@", "https", "@budi"):
            self.assertNotIn(bocor, t)
        self.assertIn("[hp]", t)

    def test_nomor_pesanan_dan_kode(self):
        t = om.samarkan("No pesanan INV/2026/0912 dan resi JP1234567890 sudah sampai")
        self.assertNotIn("1234567890", t)
        self.assertNotIn("0912", t)

    def test_kata_pesanan_biasa_tidak_hilang(self):
        self.assertIn("salah", om.samarkan("Pesanan salah kirim"))

    def test_harga_tidak_disamarkan(self):
        self.assertIn("25.000", om.samarkan("Harganya Rp 25.000 saja"))

    def test_sapaan_nama_tapi_bukan_admin(self):
        self.assertEqual(om.samarkan("Terima kasih kak Budi"), "Terima kasih kak [nama]")
        self.assertIn("kak Admin", om.samarkan("Halo kak Admin"))

    def test_nama_pengirim(self):
        self.assertNotIn("Wulandari", om.samarkan("Kata Sari Wulandari enak", ["Sari Wulandari", "Sari"]))

    def test_alamat(self):
        self.assertNotIn("Melati", om.samarkan("Kirim ke Jl. Melati No 5, Bekasi"))


class UjiSentimenTema(unittest.TestCase):
    def setUp(self):
        self.tema, self.pos, self.neg = om.buat_tema(None)

    def hasil(self, teks, bintang=None):
        return om.analisis_item(teks, bintang, self.tema, self.pos, self.neg)

    def test_negasi(self):
        sent, t = self.hasil("rasanya tidak enak")
        self.assertEqual(sent, "negatif")
        self.assertIn("keluhan", t["rasa"])
        sent, t = self.hasil("pengiriman tidak telat")
        self.assertIn("pujian", t["pengiriman"])

    def test_klausa_campuran(self):
        sent, t = self.hasil("rasa enak banget tapi pengiriman telat")
        self.assertIn("pujian", t["rasa"])
        self.assertIn("keluhan", t["pengiriman"])
        self.assertNotIn("keluhan", t["rasa"])

    def test_slang(self):
        sent, t = self.hasil("brg gk sesuai foto, packing bgt jelek")
        self.assertIn("keluhan", t["kemasan"])

    def test_bintang_rendah_tanpa_kata_negatif(self):
        sent, t = self.hasil("pengiriman kemarin sore", bintang=1)
        self.assertEqual(sent, "negatif")
        self.assertIn("keluhan", t["pengiriman"])

    def test_saran(self):
        _, t = self.hasil("semoga ada menu vegetarian")
        self.assertIn("saran", t["varian_menu"])

    def test_tema_kustom(self):
        tema, pos, neg = om.buat_tema({"tema": [{"id": "parkir", "label": "Parkir", "kata": ["parkir"], "dampak": 2}],
                                        "kata_negatif": ["sempit"]})
        _, t = om.analisis_item("parkirnya sempit", None, tema, pos, neg)
        self.assertIn("keluhan", t["parkir"])


class UjiTanggal(unittest.TestCase):
    def test_format(self):
        self.assertEqual(om.bulan_dari("12/09/2026"), "2026-09")
        self.assertEqual(om.bulan_dari("2026-08-03"), "2026-08")
        self.assertEqual(om.bulan_dari("5 Okt 2026"), "2026-10")
        self.assertEqual(om.bulan_dari("3/1/26"), "2026-01")
        self.assertIsNone(om.bulan_dari("kemarin"))
        self.assertIsNone(om.bulan_dari(""))


class UjiBerkas(unittest.TestCase):
    def jalankan(self, spes, **kw):
        o = Opsi()
        for k, v in kw.items():
            setattr(o, k, v)
        item, tema, dibuang, _ = om.olah(spes, o)
        return item, om.ringkas(item, tema, dibuang, o), dibuang

    def test_wa_staf_sistem_media_dan_nama(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "c.txt", "[02/09/2026 09.14.05] Budi Santoso: Pesanan datang telat sekali\n"
                                   "dan nasinya dingin\n"
                                   "[02/09/2026 09.20.11] Admin Toko: Maaf ya Pak Budi Santoso\n"
                                   "[02/09/2026 09.25.11] Budi Santoso: <Media tidak disertakan>\n"
                                   "02/09/2026 09.30 - Pesan dan panggilan terenkripsi end-to-end\n"
                                   "[03/09/2026 10.00.00] Sari: Rasanya enak, Budi Santoso juga suka\n")
            item, r, dibuang = self.jalankan([p + "=WA"], staf_list=["admin"])
            self.assertEqual(len(item), 2)
            semua = " ".join(i["teks"] for i in item)
            self.assertNotIn("Budi", semua)
            self.assertIn("dingin", item[0]["teks"])  # baris lanjutan tergabung
            self.assertEqual(dibuang["pesan staf"], 1)
            self.assertGreaterEqual(dibuang["pesan sistem/media"], 1)

    def test_csv_kolom_nama_tidak_dibaca_dan_duplikat(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "u.csv", "Nama Pembeli,Rating,Tanggal,Ulasan\nRini Hartati,1,2026-09-01,Telat banget kurirnya\n"
                                   "Lain,1,2026-09-02,telat banget kurirnya!\nX,5,2026-09-03,Enak dan rapi\n")
            item, r, dibuang = self.jalankan([p + "=Shopee"])
            self.assertEqual(len(item), 2)
            self.assertEqual(dibuang.get("duplikat"), 1)
            self.assertNotIn("Rini", json.dumps(r, ensure_ascii=False))
            self.assertEqual(item[0]["bintang"], 1)

    def test_csv_tanpa_kolom_teks_dikenali_untuk_survei(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "s.csv", "Tanggal,Apa yang perlu diperbaiki?\n2026-09-01,Pengiriman sering telat\n2026-09-02,Kemasan bocor\n")
            item, r, _ = self.jalankan([p + "=Survei"])
            self.assertEqual(len(item), 2)

    def test_teks_bintang_dan_data_rusak(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.txt", "5 | enak banget\n★★ nasi dingin\n\n\n??\n")
            item, r, _ = self.jalankan([p + "=IG"])
            self.assertEqual([i["bintang"] for i in item], [5, 2])
            k = tulis(d, "kosong.txt", "")
            self.assertEqual(self.jalankan([k])[0], [])

    def test_hitungan_dan_tren(self):
        with tempfile.TemporaryDirectory() as d:
            baris = ["Tanggal,Rating,Ulasan"]
            for i in range(10):
                baris.append("2026-08-%02d,1,Kurir telat parah nomor %d" % (i + 1, i))
            for i in range(10):
                baris.append("2026-09-%02d,%d,%s nomor %d" % (i + 1, 1 if i < 2 else 5, "Kurir telat parah" if i < 2 else "Enak dan rapi", i + 50))
            p = tulis(d, "t.csv", "\n".join(baris))
            item, r, _ = self.jalankan([p + "=Shopee"])
            self.assertEqual(r["total_masukan"], 20)
            peng = [t for t in r["tema"] if t["id"] == "pengiriman"][0]
            self.assertEqual(peng["keluhan"], 12)
            self.assertEqual(peng["skor"], 12 * 3)
            self.assertEqual(peng["arah_tren"], "turun")
            self.assertEqual(peng["selisih_persen_poin"], -80.0)
            self.assertEqual(r["sentimen"], {"positif": 8, "netral": 0, "negatif": 12})

    def test_tren_data_kurang(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.csv", "Tanggal,Ulasan\n2026-08-01,Kurir telat\n2026-09-01,Kurir telat lagi\n")
            _, r, _ = self.jalankan([p])
            self.assertEqual(r["tema"][0]["arah_tren"], "data kurang")

    def test_cli_json_dan_simpan_anonim(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.txt", "Kak Budi, pesanan telat, telp 08123456789\nEnak banget rasanya\n")
            out = os.path.join(d, "anon.csv")
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = om.main([p, "--format", "json", "--simpan-anonim", out])
            self.assertEqual(rc, 0)
            json.loads(buf.getvalue())
            with open(out, encoding="utf-8") as f:
                isi = f.read()
            self.assertNotIn("08123456789", isi)
            self.assertNotIn("Budi", isi)


if __name__ == "__main__":
    unittest.main(verbosity=1)
