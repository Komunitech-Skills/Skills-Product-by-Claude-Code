#!/usr/bin/env python3
"""Uji otomatis thr.py. Jalankan: python3 test_thr.py"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal as D

FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FOLDER)
import ter_core as tc  # noqa: E402
import thr  # noqa: E402

SHA256_TABEL = "26edfe89bda74169a5280317da194cec3194e8c48c661a8e6860ff8b48d5da72"
SUMBER_REPO = os.path.normpath(os.path.join(FOLDER, "..", "..", "..", "research", "sources", "pph21-ter-tabel.json"))
CORE_SKILL1 = os.path.normpath(os.path.join(FOLDER, "..", "..", "pph21-ter", "scripts", "ter_core.py"))


def cfg(hari_raya="2027-03-10", bayar=None):
    hr = datetime.date.fromisoformat(hari_raya)
    batas = hr - datetime.timedelta(days=7)
    b = datetime.date.fromisoformat(bayar) if bayar else batas
    return {"hari_raya": hr, "batas_bayar": batas, "tanggal_bayar": b, "bulan_bayar": b.month,
            "nama_hari_raya": "Idul Fitri", "perusahaan": "PT Uji", "peringatan": []}


def orang(**kw):
    r = {"nama": "Uji", "jenis": "tetap", "gaji_pokok": "5jt", "tanggal_mulai": "2020-01-01"}
    r.update(kw)
    return r


class TestTabel(unittest.TestCase):
    def test_hash(self):
        with open(tc.FILE_TABEL, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA256_TABEL)

    def test_sama_dengan_sumber(self):
        if not os.path.exists(SUMBER_REPO):
            self.skipTest("sumber riset tidak ada (paket pembeli)")
        with open(SUMBER_REPO, encoding="utf-8") as a, open(tc.FILE_TABEL, encoding="utf-8") as b:
            self.assertEqual(json.load(a), json.load(b))

    def test_core_identik(self):
        if not os.path.exists(CORE_SKILL1):
            self.skipTest("skill pph21-ter tidak berdampingan")
        with open(CORE_SKILL1, "rb") as a, open(os.path.join(FOLDER, "ter_core.py"), "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_contoh_resmi_ter(self):
        self.assertEqual(tc.pph_ter_bulanan(D(10000000), "A")[0], 200000)   # PP 58/2023 K/0
        self.assertEqual(tc.pph_ter_bulanan(D(15500000), "A")[0], 1085000)  # PMK 168/2023


class TestMasaKerja(unittest.TestCase):
    def test_bulan_penuh_inklusif(self):
        f = datetime.date.fromisoformat
        self.assertEqual(thr.bulan_penuh(f("2026-03-11"), f("2027-03-10")), 12)   # regresi uji independen
        self.assertEqual(thr.bulan_penuh(f("2026-03-12"), f("2027-03-10")), 11)
        self.assertEqual(thr.bulan_penuh(f("2026-03-10"), f("2027-03-10")), 12)
        self.assertEqual(thr.bulan_penuh(f("2027-01-01"), f("2027-01-31")), 1)
        self.assertEqual(thr.bulan_penuh(f("2027-01-01"), f("2027-01-30")), 0)
        self.assertEqual(thr.bulan_penuh(f("2027-01-31"), f("2027-02-27")), 1)   # akhir bulan: 31 Jan -> 28 Feb
        self.assertEqual(thr.bulan_penuh(f("2027-01-31"), f("2027-02-26")), 0)
        self.assertEqual(thr.bulan_penuh(f("2027-02-11"), f("2027-03-10")), 1)
        self.assertEqual(thr.bulan_penuh(f("2027-02-12"), f("2027-03-10")), 0)

    def test_11_vs_12_bulan(self):
        h11 = thr.hitung_karyawan(orang(gaji_pokok="6jt", tanggal_mulai="2026-03-12"), cfg())
        h12 = thr.hitung_karyawan(orang(gaji_pokok="6jt", tanggal_mulai="2026-03-11"), cfg())
        self.assertEqual((h11["masa_kerja_bulan"], h11["thr"]), (11, 5500000))
        self.assertEqual((h12["masa_kerja_bulan"], h12["thr"]), (12, 6000000))
        self.assertTrue(any("kurang 1 hari" in p for p in h11["peringatan"]))   # peringatan kasus tepi
        h = thr.hitung_karyawan(orang(gaji_pokok="6jt", tanggal_mulai="2026-03-20"), cfg())
        self.assertFalse(any("kurang" in p and "hari lagi" in p for p in h["peringatan"]))

    def test_kurang_1_bulan(self):
        h = thr.hitung_karyawan(orang(tanggal_mulai="2027-02-20"), cfg())
        self.assertFalse(h["berhak"])
        self.assertEqual(h["thr"], 0)

    def test_proporsional_dan_pembulatan(self):
        h = thr.hitung_karyawan(orang(gaji_pokok="5.000.000", tunjangan_tetap="555.555", masa_kerja_bulan="7"),
                                cfg())
        self.assertEqual(h["thr"], tc.bulat_terdekat(D(7) / 12 * D(5555555)))
        self.assertEqual(h["thr"], 3240740)

    def test_komponen_upah(self):
        h = thr.hitung_karyawan(orang(gaji_pokok="5jt", tunjangan_tetap="750rb"), cfg())
        self.assertEqual(h["thr"], 5750000)


class TestJenis(unittest.TestCase):
    def test_harian_12_bulan_rata2(self):
        upah = "+".join(["3jt"] * 11 + ["4,2jt"] + ["9jt"])     # 13 data: yang dipakai 12 terakhir
        h = thr.hitung_karyawan(orang(jenis="harian", gaji_pokok="", upah_bulanan=upah, tanggal_mulai="2025-01-01"),
                                cfg())
        self.assertEqual(h["upah_sebulan"], (D(3000000) * 10 + D(4200000) + D(9000000)) / 12)
        self.assertEqual(h["thr"], 3600000)

    def test_harian_kurang_12(self):
        h = thr.hitung_karyawan(orang(jenis="harian", gaji_pokok="", upah_bulanan="3jt+2jt+4jt",
                                      tanggal_mulai="2026-12-01"), cfg())
        self.assertEqual(h["masa_kerja_bulan"], 3)
        self.assertEqual(h["thr"], 750000)                          # 3/12 x rata-rata 3 jt

    def test_pkwt_berakhir_sebelum_hari_raya(self):
        h = thr.hitung_karyawan(orang(jenis="kontrak", tanggal_berhenti="2027-03-01"), cfg())
        self.assertFalse(h["berhak"])

    def test_pkwtt_phk_30_hari(self):
        h = thr.hitung_karyawan(orang(tanggal_berhenti="2027-02-08"), cfg())   # 30 hari sebelum
        self.assertTrue(h["berhak"])
        h = thr.hitung_karyawan(orang(tanggal_berhenti="2027-02-07"), cfg())   # 31 hari
        self.assertFalse(h["berhak"])

    def test_kebijakan_lebih_besar(self):
        h = thr.hitung_karyawan(orang(thr_kebijakan="7,5jt"), cfg())
        self.assertEqual(h["thr"], 7500000)
        h = thr.hitung_karyawan(orang(thr_kebijakan="1jt"), cfg())
        self.assertEqual(h["thr"], 5000000)
        self.assertTrue(h["peringatan"])


class TestPPh(unittest.TestCase):
    def test_pph_thr_ter(self):
        # K/0 gaji 10 jt: tanpa THR 2% = 200.000; dengan THR 10 jt -> bruto 20 jt -> TER A 9% = 1.800.000
        h = thr.hitung_karyawan(orang(ptkp="K/0", gaji_pokok="10jt", bruto_bulan_bayar="10jt"), cfg())
        p = h["pph21"]
        self.assertEqual(p["pph_tanpa_thr"], 200000)
        self.assertEqual(p["tarif_dengan_thr"], 9)
        self.assertEqual(p["pph_dengan_thr"], 1800000)
        self.assertEqual(p["tambahan_pph_thr"], 1600000)
        self.assertEqual(h["thr_setelah_pph"], 8400000)

    def test_pph_k3_kategori_c(self):
        h = thr.hitung_karyawan(orang(ptkp="K/3", gaji_pokok="5jt", bruto_bulan_bayar="5jt"), cfg())
        self.assertEqual(h["pph21"]["kategori"], "C")
        self.assertEqual(h["pph21"]["pph_tanpa_thr"], 0)

    def test_desember_tidak_pakai_ter(self):
        h = thr.hitung_karyawan(orang(ptkp="TK/0"), cfg("2026-12-25"))
        self.assertFalse(h["pph21"]["dihitung"])
        self.assertTrue(any("Masa Pajak Terakhir" in x for x in h["peringatan"]))

    def test_mantan_pegawai_pasal17(self):
        # regresi uji independen: PHK 20 Feb 2027 (<=30 hari), THR dibayar 3 Mar 2027 -> 5% x 20 jt
        h = thr.hitung_karyawan(orang(ptkp="TK/0", gaji_pokok="20jt", tanggal_berhenti="2027-02-20"), cfg())
        self.assertTrue(h["berhak"])
        self.assertEqual(h["thr"], 20000000)
        self.assertEqual(h["pph21"]["metode"], "mantan_pegawai")
        self.assertEqual(h["pph21"]["tambahan_pph_thr"], 1000000)
        self.assertEqual(h["thr_setelah_pph"], 19000000)
        # contoh resmi Tuan O (PMK 168/2023): mantan pegawai, jasa produksi 60 jt -> Rp3.000.000
        self.assertEqual(tc.bulat_bawah(tc.pasal17(D(60000000))[0]), 3000000)
        # THR besar: lapisan progresif 5% & 15%
        h = thr.hitung_karyawan(orang(ptkp="TK/0", gaji_pokok="80jt", tanggal_berhenti="2027-02-20"), cfg())
        self.assertEqual(h["pph21"]["tambahan_pph_thr"], 3000000 + 3000000)

    def test_berhenti_bulan_sama_dengan_bayar(self):
        h = thr.hitung_karyawan(orang(ptkp="TK/0", tanggal_berhenti="2027-03-01"), cfg())
        self.assertFalse(h["pph21"]["dihitung"])

    def test_dtp_ditolak_tahun_2027(self):
        # regresi uji independen: THR Maret 2027 -> bukan masa 2026
        h = thr.hitung_karyawan(orang(ptkp="TK/0", gaji_pokok="8jt", bruto_bulan_bayar="8jt", dtp="ya"), cfg())
        self.assertFalse(h["pph21"]["dtp"])
        self.assertLess(h["thr_setelah_pph"], h["thr"])

    def test_dtp_ditolak_di_atas_10jt(self):
        h = thr.hitung_karyawan(orang(ptkp="TK/0", gaji_pokok="20jt", bruto_bulan_bayar="20jt", dtp="ya"),
                                cfg("2026-06-20"))
        self.assertFalse(h["pph21"]["dtp"])
        self.assertTrue(any("TIDAK memenuhi" in p for p in h["peringatan"]))

    def test_dtp(self):
        h = thr.hitung_karyawan(orang(ptkp="TK/0", gaji_pokok="8jt", bruto_bulan_bayar="8jt", dtp="ya"),
                                cfg("2026-06-20"))
        self.assertTrue(h["pph21"]["dtp"])
        self.assertEqual(h["thr_setelah_pph"], h["thr"])
        # PMK 105/2025 Pasal 2 ayat 1, Pasal 5, Lampiran B (cek 2026-10-05): PPh tetap dipotong lalu DTP dibayar
        # tunai -> THR diterima = THR (bukan THR + DTP); setoran bagian DTP Rp 0
        tambahan = h["pph21"]["tambahan_pph_thr"]
        self.assertGreater(tambahan, 0)
        c = cfg("2026-06-20")
        total = {"thr": h["thr"], "pph": tambahan, "diterima": h["thr_setelah_pph"]}
        teks = thr.teks_hasil([h], c, total, None)
        self.assertIn("{} tetap dipotong, lalu {} dibayar tunai kembali".format(
            tc.format_rp(tambahan), tc.format_rp(tambahan)), teks)
        self.assertIn("setoran PPh 21 ke negara untuk bagian ini Rp 0", teks)
        self.assertNotIn(tc.format_rp(h["thr"] + tambahan), teks)


class TestRusak(unittest.TestCase):
    def cek(self, r):
        with self.assertRaises((thr.InputError, ValueError)):
            thr.hitung_karyawan(r, cfg())

    def test_rusak(self):
        self.cek(orang(gaji_pokok="abc"))
        self.cek(orang(tanggal_mulai="31-31-2026"))
        self.cek(orang(tanggal_mulai="2026-12-01", tanggal_berhenti="2026-11-01"))   # mulai setelah berhenti
        self.cek(orang(tanggal_mulai="", masa_kerja_bulan=""))
        self.cek(orang(jenis="magang"))
        self.cek(orang(jenis="harian", upah_bulanan=""))
        self.cek(orang(ptkp="K/7"))
        self.cek(orang(nama=""))

    def test_cli(self):
        r = subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "2027-03-10",
                            "--nama", "Budi", "--gaji-pokok", "6jt", "--mulai", "2026-06-10", "--format", "json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["batas_bayar"], "2027-03-03")
        self.assertEqual(d["karyawan"][0]["thr"], 4500000)          # 9/12 x 6 jt
        r = subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "10 Maret",
                            "--nama", "Budi", "--gaji-pokok", "6jt", "--mulai", "2026-06-10"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("ERROR", r.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "thr.csv")
            r = subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "2027-03-10",
                                "--nama", "Budi", "--gaji-pokok", "6jt", "--mulai", "2026-06-10", "--tanggal-bayar",
                                "2027-03-05", "--csv", out], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            self.assertIn("denda 5%", r.stdout)
            self.assertTrue(os.path.exists(out))


class TestPeringatanTemp(unittest.TestCase):
    def test_fungsi(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(thr.peringatan_folder_sementara(os.path.join(tmp, "x")))
        self.assertFalse(thr.peringatan_folder_sementara(os.path.expanduser("~")))

    def test_cli_tetap_menulis_dan_memperingatkan(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "2027-03-10", "--nama", "Budi", "--gaji-pokok", "6jt", "--mulai", "2026-06-10", "--tanggal-bayar", "2027-03-05", "--csv", os.path.join(tmp, "thr.csv")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("PERINGATAN", r.stderr)
            self.assertIn("folder sementara", r.stderr)
            self.assertTrue(os.path.exists(os.path.join(tmp, "thr.csv")))


class TesTahunHijriah(unittest.TestCase):
    """v1.0.4: tahun Hijriah hari raya dihitung, bukan ditebak (temuan uji: Maret 2027 ditulis 1449 H)."""

    def test_idul_fitri_dan_adha_dikenal(self):
        import tahun_hijriah as th
        # Idul Fitri resmi: 10 Apr 2024 = 1445 H, 31 Mar 2025 = 1446 H, 21 Mar 2026 = 1447 H, 10 Mar 2027 = 1448 H
        for tgl, tahun in (("2024-04-10", 1445), ("2025-03-31", 1446), ("2026-03-21", 1447), ("2027-03-10", 1448)):
            y, m, _ = th.ke_hijriah(datetime.date.fromisoformat(tgl))
            self.assertEqual((y, m), (tahun, 10), tgl)
        y, m, d = th.ke_hijriah(datetime.date(2026, 5, 27))   # Iduladha 1447 H
        self.assertEqual((y, m, d), (1447, 12, 10))
        self.assertNotEqual(th.ke_hijriah(datetime.date(2027, 3, 10))[0], 1449)

    def test_dekat_pergantian_tahun_tidak_pasti(self):
        import tahun_hijriah as th
        self.assertFalse(th.hasil(datetime.date(2026, 6, 16))["tahun_pasti"])
        self.assertTrue(th.hasil(datetime.date(2027, 3, 10))["tahun_pasti"])

    def test_cli(self):
        p = subprocess.run([sys.executable, os.path.join(FOLDER, "tahun_hijriah.py"), "2027-03-10"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0)
        self.assertIn("1448 H", p.stdout)
        p = subprocess.run([sys.executable, os.path.join(FOLDER, "tahun_hijriah.py"), "10-03-2027"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 2)


class TesCekTanggalLebaran(unittest.TestCase):
    """v1.0.5 (uji OpenClaw ulang 2026-10-01): pengguna menyebut Lebaran 20 Maret 2027 (= 11 Syawal 1448 H)."""

    def test_tanggal_keliru_diperingatkan(self):
        import tahun_hijriah as th
        c = th.cek_hari_raya(datetime.date(2027, 3, 20), "idul-fitri")
        self.assertFalse(c["sesuai"])
        self.assertEqual(c["perkiraan"], "2027-03-10")
        self.assertEqual(c["batas_bayar_h7_perkiraan"], "2027-03-03")
        self.assertEqual(c["selisih_hari"], 10)
        self.assertIn("11 Syawal 1448 H", c["peringatan"])

    def test_toleransi_dua_hari(self):
        import tahun_hijriah as th
        for tgl, sesuai in (("2027-03-08", True), ("2027-03-12", True), ("2027-03-13", False), ("2027-03-07", False)):
            self.assertEqual(th.cek_hari_raya(datetime.date.fromisoformat(tgl), "idul-fitri")["sesuai"], sesuai, tgl)
        # Lebaran resmi 2024-2026 lolos cek
        for tgl in ("2024-04-10", "2025-03-31", "2026-03-21"):
            self.assertTrue(th.cek_hari_raya(datetime.date.fromisoformat(tgl), "idul-fitri")["sesuai"], tgl)

    def test_idul_adha(self):
        import tahun_hijriah as th
        self.assertTrue(th.cek_hari_raya(datetime.date(2026, 5, 27), "idul-adha")["sesuai"])
        c = th.cek_hari_raya(datetime.date(2026, 6, 10), "idul-adha")
        self.assertFalse(c["sesuai"])
        self.assertEqual(c["perkiraan"], "2026-05-27")

    def test_cli_cek(self):
        s = os.path.join(FOLDER, "tahun_hijriah.py")
        p = subprocess.run([sys.executable, s, "2027-03-20", "--cek", "idul-fitri"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0)
        self.assertIn("PERINGATAN", p.stdout)
        self.assertIn("2027-03-03", p.stdout)
        p = subprocess.run([sys.executable, s, "2027-03-10", "--cek", "idul-fitri"], capture_output=True, text=True, timeout=60)
        self.assertNotIn("PERINGATAN", p.stdout)
        self.assertIn("COCOK", p.stdout)


class TesPrivasiDanTanggalMasaDepan(unittest.TestCase):
    """v1.0.6 (uji OpenClaw 2026-10-02): nominal per orang bocor ke pengumuman grup; tanggal masuk masa depan lolos."""

    CSV = ("nama;gaji_sebulan;tanggal_masuk\nAndi;Rp 5.500.000;01/07/2019\nSari;Rp 4.000.000;01/03/2026\n"
           "Yohanes;Rp 6.200.000;10/11/2026\nBaru;5jt;05/01/2027\n")

    def jalan(self, *extra):
        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, "k.csv")
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(self.CSV)
            return subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "2026-12-25",
                                   "--nama-hari-raya", "Natal 2026", "--data", f, "--hari-ini", "2026-10-02"] +
                                  list(extra), capture_output=True, text=True, timeout=60)

    def test_masa_depan_diperingatkan(self):
        c = cfg("2026-12-25")
        c["hari_ini"] = datetime.date(2026, 10, 2)
        h = thr.hitung_karyawan(orang(tanggal_mulai="2026-11-10", gaji_pokok="6,2jt"), c)
        self.assertEqual(h["thr"], 516667)
        self.assertTrue(any("MASA DEPAN" in x for x in h["peringatan"]))
        h = thr.hitung_karyawan(orang(tanggal_mulai="2026-03-01", gaji_pokok="4jt"), c)
        self.assertFalse(any("MASA DEPAN" in x for x in h["peringatan"]))
        self.assertEqual(h["thr"], 3000000)

    def test_mulai_setelah_hari_raya_tidak_berhak_dan_diperingatkan(self):
        h = thr.hitung_karyawan(orang(tanggal_mulai="2028-01-01"), cfg())
        self.assertFalse(h["berhak"])
        self.assertEqual(h["thr"], 0)
        self.assertIn("setelah hari raya", h["alasan"])
        self.assertTrue(any("SETELAH tanggal hari raya" in x for x in h["peringatan"]))

    def test_format_pengumuman_tanpa_nama_dan_nominal(self):
        r = self.jalan("--format", "pengumuman")
        self.assertEqual(r.returncode, 0, r.stderr)
        for kata in ("Andi", "Sari", "Yohanes", "5.500.000", "3.000.000", "516.667", "Rp "):
            self.assertNotIn(kata, r.stdout, kata)
        self.assertIn("PRIBADI", r.stdout)
        self.assertIn("18 Desember 2026", r.stdout)
        self.assertIn("peringatan", r.stderr)

    def test_teks_dua_blok_terpisah(self):
        r = self.jalan()
        self.assertEqual(r.returncode, 0, r.stderr)
        a = r.stdout.index("KHUSUS PEMILIK/HR")
        b = r.stdout.index("TEKS GRUP")
        self.assertLess(a, b)
        grup = r.stdout[b:]
        for kata in ("Andi", "Sari", "5.500.000", "516.667"):
            self.assertNotIn(kata, grup, kata)
        self.assertIn("MASA DEPAN", r.stdout[:b])
        self.assertNotIn("— -", r.stdout)

    def test_json_pengumuman_bersih(self):
        r = self.jalan("--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertNotIn("Sari", d["pengumuman"])
        self.assertIn("privasi", d)
        self.assertEqual([k["thr"] for k in d["karyawan"]], [5500000, 3000000, 516667, 0])


if __name__ == "__main__":
    unittest.main(verbosity=1)
