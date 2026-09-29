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
        self.assertEqual(n_kos - n_lain, 3)  # cek izin + label T-28 + foto listing T-3

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

    # ---- regresi v1.0.1 ----
    def _cari(self, b, teks):
        return [r for r in b if teks in r["tugas"]]

    def test_soft_launch_kirim_dulu_baru_tanya(self):
        # T0 2026-11-14: kirim pre-order soft launch T-10 = 2026-11-04; umpan balik T-5 = 2026-11-09.
        b = J.bangun(date(2026, 11, 14), "pangan")
        kirim = self._cari(b, "Kirim pre-order soft launch")[0]
        tanya = self._cari(b, "tanya 10 pembeli")[0]
        self.assertEqual(kirim["tanggal"], "2026-11-04")
        self.assertEqual(tanya["tanggal"], "2026-11-09")
        self.assertLess(kirim["tanggal"], tanya["tanggal"])
        self.assertGreater(tanya["tanggal"], self._cari(b, "Buka soft launch")[0]["tanggal"])

    def test_hari_ini_default_hari_ini(self):
        # tanpa --hari-ini: tanggal sudah lewat harus tetap diperingatkan (default date.today()).
        k, out, _ = jalan("--tanggal", "2020-01-01")
        self.assertEqual(k, 0)
        self.assertIn("sudah lewat", out)
        besok = date.today().replace(year=date.today().year + 1)
        k, out, _ = jalan("--tanggal", besok.isoformat())
        self.assertNotIn("sudah lewat", out)
        k, out, _ = jalan("--tanggal", "2026-11-14", "--hari-ini", "2026-11-01")
        self.assertIn("13 hari", out)

    def test_kosmetik_label_t28_dan_foto_t3(self):
        b = J.bangun(date(2026, 11, 14), "kosmetik")
        lab = [r for r in b if r["bidang"] == "Label"]
        self.assertEqual(sorted(r["t"] for r in lab), ["T-28", "T-3"])
        self.assertTrue(all("BPOM" in r["tugas"] for r in lab))

    def test_tahun_data_libur_seluruh_rentang(self):
        # T0 2027-12-20 -> T+30 = 2028-01-19: 2028 tanpa data, harus diperingatkan walau T0 tahun 2027.
        w = J.peringatan(date(2027, 12, 20))
        self.assertTrue(any("2028" in x and "belum ada" in x for x in w))
        # T0 2027-01-10 -> T-30 = 2026-12-11: dua-duanya ada datanya, tanpa peringatan tahun.
        w = J.peringatan(date(2027, 1, 10))
        self.assertFalse(any("belum ada" in x for x in w))
        # T0 2026-01-10 -> T-30 tahun 2025 tanpa data.
        w = J.peringatan(date(2026, 1, 10))
        self.assertTrue(any("2025" in x and "belum ada" in x for x in w))

    def test_stok_rumus_termasuk_preorder(self):
        b = J.bangun(date(2026, 11, 14), "lain")
        st = self._cari(b, "Hitung stok awal")[0]
        self.assertIn("pre-order soft launch + perkiraan pesanan minggu 1) x 1,3", st["tugas"])
        # contoh angka: (40 + 16) x 1,3 = 72,8 -> 73
        self.assertEqual(int(-(-(40 + 16) * 13 // 10)), 73)

    def test_peringatan_lebaran(self):
        # Idulfitri 2026: 20-24 Maret. T0 16 Mar (T+7 menyentuh) dan T0 1 Apr (T-7 = 25 Mar, masih arus balik).
        self.assertTrue(any("Lebaran" in x for x in J.peringatan(date(2026, 3, 16))))
        self.assertTrue(any("Lebaran" in x for x in J.peringatan(date(2026, 3, 30))))
        self.assertTrue(any("Idulfitri 2027" in x for x in J.peringatan(date(2027, 3, 5))))
        self.assertFalse(any("Lebaran" in x for x in J.peringatan(date(2026, 11, 14))))
        self.assertFalse(any("Lebaran" in x for x in J.peringatan(date(2026, 5, 20))))

    def test_md_label_t_per_baris(self):
        k, out, _ = jalan("--tanggal", "2026-11-14", "--jenis", "pangan", "--hari-ini", "2026-09-29")
        baris = [l for l in out.splitlines() if l.startswith("- [ ]")]
        self.assertEqual(len(baris), len(J.bangun(date(2026, 11, 14), "pangan")))
        self.assertTrue(all(l.startswith("- [ ] **T") for l in baris))
        # bazar T-5 digeser ke Jumat 2026-11-06? tetap berlabel T-5 (bukan label tugas lain)
        bazar = [l for l in baris if "konfirmasi stan" in l][0]
        self.assertIn("**T-5**", bazar)

    def test_jenis_jasa_tanpa_stok_kemasan_kirim(self):
        b = J.bangun(date(2026, 11, 14), "jasa")
        gabung = " ".join(r["tugas"] + " " + r["bidang"] for r in b).lower()
        for kata in ("pemasok", "uji coba kirim", "kirim semua pesanan", "pengemasan", "kemasan pengiriman", "stok fisik", "hitung stok"):
            self.assertNotIn(kata, gabung, kata)
        self.assertFalse([r for r in b if r["fase"] == "Stok & operasional" and r["bidang"] != "Kapasitas"])
        self.assertTrue(self._cari(b, "kapasitas layanan"))
        self.assertTrue(self._cari(b, "klien percobaan"))
        self.assertLess(len(b), len(J.bangun(date(2026, 11, 14), "lain")))
        k, out, _ = jalan("--tanggal", "2026-11-14", "--jenis", "jasa", "--hari-ini", "2026-09-29")
        self.assertEqual(k, 0)

    def test_data_libur_2027_tidak_bertanda_review(self):
        with open(os.path.join(AKAR, "scripts", "jadwal_peluncuran.py"), encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("PERLU REVIEW", src)
        self.assertEqual(len([k for k in J.LIBUR if k.startswith("2027")]), 26)


if __name__ == "__main__":
    unittest.main()
