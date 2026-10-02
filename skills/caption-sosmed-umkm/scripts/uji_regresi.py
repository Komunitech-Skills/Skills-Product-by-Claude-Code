#!/usr/bin/env python3
"""Uji regresi cek_caption.py & cek_fakta.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import os
import subprocess
import sys
import unittest

DIR = os.path.dirname(os.path.abspath(__file__))
FAKTA = "keripik singkong pedas level 1-5, 200 gram, Rp15.000 per bungkus, 3 bungkus Rp40.000, target mahasiswa Jogja, order WA 0812-2233-4455 atau DM"
IG_BAIK = "**Variasi A – Storytelling**\n" + " ".join(["Ngemil sambil nugas di kos itu enak banget kalau camilannya renyah"] * 1) + \
    " dan pedasnya bisa kamu pilih sendiri dari level 1 sampai 5 sesuai nyali. " + \
    "Keripik singkong pedas ukuran 200 gram cuma Rp15.000 per bungkus, atau ambil 3 bungkus Rp40.000 untuk dibagi bareng teman kos. " + \
    "Cocok menemani begadang, rapat kelompok, sampai nobar akhir pekan di Jogja. Pilih levelmu, lalu pesan lewat WA 0812-2233-4455 atau DM kami sekarang. Siapa tahu levelmu naik terus. Ajak teman sekelas, sekamar, dan sekelompok supaya ngemilnya makin seru. Jangan lupa siapkan minum dingin di samping kamu.\n" \
    "#keripiksingkong #camilanpedas #mahasiswajogja #jajananjogja #umkmjogja\n"


def jalan(script, *arg):
    r = subprocess.run([sys.executable, os.path.join(DIR, script)] + list(arg), capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout + r.stderr


def tiga(teks):
    return "\n".join(teks.replace("Variasi A – Storytelling", n) for n in
                     ("Variasi A – Storytelling", "Variasi B – Langsung jualan", "Variasi C – Santai"))


class UjiCaption(unittest.TestCase):
    def test_lulus(self):
        kode, out = jalan("cek_caption.py", "--platform", "ig", "--teks", tiga(IG_BAIK), "--fakta", FAKTA)
        self.assertEqual(kode, 0, out)
        self.assertIn("HASIL: LULUS", out)

    def test_ig_tanpa_hashtag_gagal(self):
        t = tiga(IG_BAIK.split("#keripik")[0])
        kode, out = jalan("cek_caption.py", "--platform", "ig", "--teks", t, "--fakta", FAKTA)
        self.assertEqual(kode, 2)
        self.assertIn("0 hashtag", out)

    def test_terlalu_pendek_gagal(self):
        t = "**Variasi A – Storytelling**\nKeripik pedas Rp15.000, order WA 0812-2233-4455.\n#a #b #c #d\n"
        kode, out = jalan("cek_caption.py", "--platform", "ig", "--teks", t, "--fakta", FAKTA)
        self.assertEqual(kode, 2)
        self.assertIn("wajib 80-150", out)

    def test_hashtag_tidak_dihitung_sebagai_kata(self):
        kode, out = jalan("cek_caption.py", "--platform", "ig", "--teks", IG_BAIK, "--fakta", FAKTA)
        self.assertRegex(out, r"Variasi A – Storytelling: \d+ kata, 5 hashtag")

    def test_klaim_kesehatan_halus_gagal(self):
        for kalimat in ("Bantu redakan perut kembung setiap hari", "Cocok diminum pas asam lambung naik",
                        "Obat alami pengganti obat", "Menurunkan gula darah", "Detox harian", "Menjaga imun tubuh"):
            kode, out = jalan("cek_fakta.py", "--teks", kalimat, "--fakta", "jamu kunyit asam botol 250 ml Rp12.000")
            self.assertEqual(kode, 2, kalimat + "\n" + out)

    def test_klaim_karangan_gagal(self):
        for kalimat in ("Tanpa pengawet dan 100% alami", "Stok terbatas, siap antar!", "Dulu aku juga sering begadang",
                        "Sudah BPOM dan halal", "Gratis ongkir seluruh Jogja"):
            kode, out = jalan("cek_fakta.py", "--teks", kalimat, "--fakta", FAKTA)
            self.assertEqual(kode, 2, kalimat + "\n" + out)

    def test_kelangkaan_dan_pengiriman_karangan_gagal(self):
        for kalimat in ("Stok terbatas tiap hari", "Stoknya terbatas banget", "Pesan sekarang sebelum kehabisan!",
                        "Promo hari ini saja", "Tunggu keripiknya nyampe ya", "Siap antar ke kosmu",
                        "Order lewat DM, secepatnya kami proses"):
            kode, out = jalan("cek_fakta.py", "--teks", kalimat, "--fakta", FAKTA)
            self.assertEqual(kode, 2, kalimat + "\n" + out)

    def test_kelangkaan_disebut_pengguna_lulus(self):
        kode, out = jalan("cek_fakta.py", "--teks", "Stok terbatas, pesan sebelum kehabisan.",
                          "--fakta", FAKTA + ", stok terbatas, sebelum kehabisan")
        self.assertEqual(kode, 0, out)

    def test_fb_di_bawah_50_kata_gagal(self):
        t = "**Variasi C – Santai**\n" + " ".join(["kata"] * 46) + "\n"
        kode, out = jalan("cek_caption.py", "--platform", "fb", "--teks", t, "--fakta", FAKTA)
        self.assertEqual(kode, 2, out)
        self.assertIn("wajib 50-120", out)

    def test_aman_dan_placeholder_lulus(self):
        kode, out = jalan("cek_fakta.py", "--teks", "Segar diminum dingin sore hari. Bahan: [isi: bahan]. Teman santai keluarga.",
                          "--fakta", "jamu kunyit asam botol 250 ml")
        self.assertEqual(kode, 0, out)

    def test_penolakan_klaim_tidak_ditandai(self):
        kode, out = jalan("cek_fakta.py", "--teks", "Catatan: klaim menyembuhkan atau obat alami tidak ditulis.", "--fakta", FAKTA)
        self.assertEqual(kode, 0, out)

    def test_input_rusak(self):
        for arg in (["--platform", "ig"], ["--platform", "xx", "--teks", "a", "--fakta", "b"],
                    ["--platform", "ig", "--teks-file", "/tidak/ada.md", "--fakta", "b"],
                    ["--platform", "ig", "--teks", "tanpa variasi", "--fakta", " "]):
            kode, _ = jalan("cek_caption.py", *arg)
            self.assertIn(kode, (1, 2), arg)
        kode, _ = jalan("cek_caption.py", "--platform", "ig", "--teks", "tanpa variasi", "--fakta", FAKTA)
        self.assertEqual(kode, 2)


if __name__ == "__main__":
    unittest.main()
