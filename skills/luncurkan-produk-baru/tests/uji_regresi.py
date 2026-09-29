#!/usr/bin/env python3
"""Uji jadwal_peluncuran.py. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py).
Tanggal diverifikasi dengan kalender manual (dicek di komentar)."""
import contextlib, io, json, os, sys, unittest
from datetime import date

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import jadwal_peluncuran as J  # noqa: E402


def jalan(*argv):
    buf = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
        k = J.main(list(argv))
    return k, buf.getvalue(), err.getvalue()


class Uji(unittest.TestCase):
    def test_t0_dan_rentang(self):
        # 2026-11-14 = Sabtu. T-30 = 2026-10-15 (Kamis), T+30 = 2026-12-14 (Senin).
        b = J.bangun(date(2026, 11, 14), "lain")
        tg = [r["tanggal"] for r in b]
        self.assertEqual(min(tg), "2026-10-15")
        self.assertEqual(max(tg), "2026-12-14")
        self.assertTrue(any(r["t"] == "T0" for r in b))

    def test_geser_hari_kerja_mundur(self):
        # T-2 (stok fisik, hari kerja) = 2026-11-12 Kamis: tidak digeser.
        # T-3 legal-label bukan hari kerja. T-10 = 2026-11-04 Rabu ok.
        # Untuk T0 Senin 2026-11-16: T-2 = Sabtu 11-14 -> mundur ke Jumat 11-13.
        b = J.bangun(date(2026, 11, 16), "lain")
        r = [x for x in b if x["bidang"] == "Stok" and "Stok fisik" in x["tugas"]][0]
        self.assertEqual(r["tanggal"], "2026-11-13")
        self.assertIn("digeser dari 2026-11-14", r["catatan"])

    def test_geser_maju_pasca(self):
        # T0 = Jumat 2026-05-29 ; T+1 kirim = Sabtu 05-30 -> Minggu 05-31 (Waisak) -> Senin 06-01 (Pancasila) -> Selasa 06-02.
        b = J.bangun(date(2026, 5, 29), "lain")
        r = [x for x in b if x["t"] == "T+1" and x["bidang"] == "Kirim"][0]
        self.assertEqual(r["tanggal"], "2026-06-02")

    def test_libur_tambahan_dan_konten_tidak_digeser(self):
        b = J.bangun(date(2026, 11, 14), "lain", {"2026-11-13": "tutup"})
        r = [x for x in b if x["tugas"].startswith("Kirim semua")][0]  # T+1 = Minggu 11-15 -> Senin 11-16
        self.assertEqual(r["tanggal"], "2026-11-16")
        k = [x for x in b if x["t"] == "T0" and x["bidang"] == "Semua kanal"][0]
        self.assertEqual(k["tanggal"], "2026-11-14")  # konten tidak digeser

    def test_jenis_pangan_menambah_legalitas(self):
        n_lain = len(J.bangun(date(2026, 11, 14), "lain"))
        n_pangan = len(J.bangun(date(2026, 11, 14), "pangan"))
        n_kos = len(J.bangun(date(2026, 11, 14), "kosmetik"))
        self.assertEqual(n_pangan - n_lain, 3)  # 3 tugas khusus pangan
        self.assertEqual(n_kos - n_lain, 1)

    def test_peringatan(self):
        w = J.peringatan(date(2026, 11, 11))
        self.assertTrue(any("11.11" in x for x in w))
        w = J.peringatan(date(2026, 12, 25))
        self.assertTrue(any("Natal" in x for x in w))
        w = J.peringatan(date(2030, 3, 3))
        self.assertTrue(any("belum ada" in x for x in w))
        w = J.peringatan(date(2026, 11, 14), date(2026, 11, 1))
        self.assertTrue(any("13 hari" in x for x in w))

    def test_lewat(self):
        b = J.bangun(date(2026, 11, 14), "lain", None, date(2026, 11, 1))
        self.assertTrue(any("LEWAT" in r["catatan"] for r in b))

    def test_input_rusak(self):
        for arg in ("2026-13-40", "besok", "14/11/2026", ""):
            k, out, err = jalan("--tanggal", arg)
            self.assertEqual(k, 2, arg)
            self.assertIn("Galat", err)
        k, _, err = jalan("--tanggal", "2026-11-14", "--libur-tambahan", "xx")
        self.assertEqual(k, 2)

    def test_format(self):
        k, out, _ = jalan("--tanggal", "2026-11-14", "--format", "json", "--produk", "Sambal")
        d = json.loads(out)
        self.assertEqual(d["t0"], "2026-11-14")
        k, out, _ = jalan("--tanggal", "2026-11-14", "--format", "csv")
        self.assertTrue(out.startswith("tanggal,hari,t,fase"))
        k, out, _ = jalan("--tanggal", "2026-11-14")
        self.assertIn("- [ ]", out)
        self.assertIn("Sabtu, 2026-11-14", out)

    def test_data_libur_konsisten(self):
        # 2026-08-17 Senin; semua kunci berformat sah
        for k in J.LIBUR:
            date.fromisoformat(k)
        self.assertEqual(date(2026, 8, 17).weekday(), 0)
        self.assertEqual(len([k for k in J.LIBUR if k.startswith("2026")]), 25)


if __name__ == "__main__":
    unittest.main()
