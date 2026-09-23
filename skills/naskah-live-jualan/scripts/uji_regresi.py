#!/usr/bin/env python3
"""Uji regresi hitung_promo.py & susun_segmen.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import unittest

DIR = os.path.dirname(os.path.abspath(__file__))


def jalan(script, *arg):
    r = subprocess.run([sys.executable, os.path.join(DIR, script)] + list(arg) + ["--json"],
                       capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout) if r.returncode == 0 else None)


class UjiPromo(unittest.TestCase):
    def test_format_angka(self):
        for teks, harap in (("1.500rb", 1500000), ("1,5jt", 1500000), ("1.5jt", 1500000), ("Rp 89.000", 89000),
                            ("89rb", 89000), ("89000", 89000)):
            r, h = jalan("hitung_promo.py", "--harga-normal", teks, "--harga-live", "1")
            self.assertEqual(h["harga_normal"], harap, teks)

    def test_bundling_sama_dengan_harga_live_diberi_peringatan(self):
        r, h = jalan("hitung_promo.py", "--harga-normal", "90000", "--harga-live", "75000", "--bundling", "2=150000")
        self.assertTrue(any("sama dengan" in p for p in h["peringatan"]))
        self.assertFalse(h["bundling"][0]["lebih_hemat_dari_harga_live"])

    def test_pembulatan_jujur(self):
        r, h = jalan("hitung_promo.py", "--harga-normal", "89000", "--diskon-persen", "12,5", "--bulatkan", "1000")
        self.assertEqual(h["harga_live"], 78000)          # 77.875 dibulatkan ke atas
        self.assertEqual(h["persen_hemat_boleh_diucapkan"], 12)  # 12,36% dibulatkan ke bawah
        self.assertNotIn("±", h["kalimat_live"])

    def test_input_rusak(self):
        for arg in (["--harga-normal", "abc", "--harga-live", "1"], ["--harga-normal", "89000", "--harga-live", "99000"],
                    ["--harga-normal", "89000", "--diskon-persen", "100"], ["--harga-normal", "89000", "--bundling", "1=5"]):
            r, _ = jalan("hitung_promo.py", *arg)
            self.assertEqual(r.returncode, 1, arg)


class UjiSegmen(unittest.TestCase):
    def cek(self, durasi, produk):
        r, h = jalan("susun_segmen.py", "--durasi", str(durasi), "--produk", produk)
        self.assertEqual(r.returncode, 0, r.stderr)
        seg = h["segmen"]
        self.assertEqual(seg[-1]["selesai_menit"], durasi)
        for a, b in zip(seg, seg[1:]):
            self.assertEqual(a["selesai_menit"], b["mulai_menit"])
        self.assertEqual({s["produk"] for s in seg if s["produk"] != "-"}, set(produk.split(",")))
        return seg

    def test_rekap_tiap_15_menit(self):
        for d in (45, 60, 90, 120):
            seg = self.cek(d, "A,B,C")
            titik = [s["mulai_menit"] for s in seg
                     if s["segmen"].startswith(("Pembukaan", "Rekap", "Tanya-jawab bebas", "Penutup"))]
            self.assertLessEqual(max(b - a for a, b in zip(titik, titik[1:])), 17, (d, titik))

    def test_semua_produk_kebagian_saat_waktu_mepet(self):
        self.cek(26, "A,B,C")
        self.cek(27, "A,B,C")

    def test_durasi_terlalu_pendek_ditolak(self):
        r, _ = jalan("susun_segmen.py", "--durasi", "20", "--produk", "A,B,C")
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
