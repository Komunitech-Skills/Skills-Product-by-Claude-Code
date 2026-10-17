#!/usr/bin/env python3
"""Uji regresi gaji-umkm. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Prinsip: gaji-umkm tidak punya rumus sendiri. Tes ini memastikan
  1. file mesin/ identik byte-per-byte dengan script asli skill slip-gaji-bpjs, pph21-ter, hitung-thr (bila repo ada);
  2. hasil hitung massal SAMA PERSIS dengan menjalankan script asli langsung, untuk banyak kasus acak
     (masukan untuk script asli disusun oleh tes ini sendiri, bukan oleh gaji.py);
  3. Desember & karyawan keluar/masuk tengah bulan mengikuti aturan skill sumber (Masa Pajak Terakhir, bulan_mulai),
     dicek dengan pph21-ter asli dan hitungan Pasal 17 manual;
  4. data rusak ditolak tanpa mengubah database; kunci periode, revisi, penyamaran NIK/rekening, backup/restore.
Semua data fiktif.
"""
import contextlib
import hashlib
import io
import json
import os
import random
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, ROUND_FLOOR

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
sys.dont_write_bytecode = True
import gaji as G  # noqa: E402

REPO_SKILLS = os.path.dirname(AKAR)
ASLI = {
    "payroll.py": os.path.join(REPO_SKILLS, "slip-gaji-bpjs", "scripts", "payroll.py"),
    "pph21.py": os.path.join(REPO_SKILLS, "pph21-ter", "scripts", "pph21.py"),
    "thr.py": os.path.join(REPO_SKILLS, "hitung-thr", "scripts", "thr.py"),
    "ter_core.py": os.path.join(REPO_SKILLS, "slip-gaji-bpjs", "scripts", "ter_core.py"),
    "ter_tabel.json": os.path.join(REPO_SKILLS, "slip-gaji-bpjs", "scripts", "ter_tabel.json"),
}
ADA_ASLI = all(os.path.isfile(p) for p in ASLI.values())
NIK = "3201010101019999"
REK = "1234509876"


def jalankan_asli(script, argv):
    """Script ASLI dari skill sumber (bila repo ada), selain itu salinan mesin/."""
    path = ASLI[script] if ADA_ASLI else os.path.join(AKAR, "scripts", "mesin", script)
    p = subprocess.run([sys.executable, path] + argv, capture_output=True, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if p.returncode != 0:
        raise AssertionError("script asli %s gagal: %s" % (script, p.stderr.decode("utf-8", "replace")))
    return json.loads(p.stdout.decode("utf-8"))


class Dasar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "gaji.db")
        self.ok("init", "--nama-usaha", "CV Uji Fiktif", "--ya")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def cli(self, *argv, hari_ini="2026-09-26"):
        argv = list(argv)
        # opsi umum ditaruh setelah sub-perintah (karyawan <aksi> punya 2 kata)
        argv += ["--db", self.db, "--json", "--hari-ini", hari_ini]
        buf, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            try:
                kode = G.main(argv)
            except SystemExit as e:
                kode = e.code
        teks = buf.getvalue()
        return kode, (json.loads(teks) if teks.strip() else {}), teks

    def ok(self, *argv, **kw):
        kode, out, _ = self.cli(*argv, **kw)
        self.assertEqual(kode, 0, out)
        self.assertTrue(out.get("ok"), out)
        return out

    def gagal(self, *argv, **kw):
        kode, out, _ = self.cli(*argv, **kw)
        self.assertEqual(kode, 1, out)
        self.assertFalse(out["ok"])
        return out

    def tambah(self, nama, *opsi):
        return self.ok("karyawan", "tambah", "--nama", nama, *opsi, "--ya")["karyawan"]

    def file(self, nama, isi):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write(isi)
        return p

    def jumlah(self, sql):
        c = sqlite3.connect(self.db)
        try:
            return c.execute(sql).fetchone()[0]
        finally:
            c.close()

    def hasil(self, bulan):
        out = self.ok("hitung", "--bulan", bulan)
        return {k["kode"]: k for k in out["karyawan"]}, out


# --------------------------------------------------------------------------- mesin identik
class UjiMesin(unittest.TestCase):
    def test_sumber_json_cocok(self):
        m = G.cek_mesin()
        for nama, info in m["file"].items():
            with open(os.path.join(AKAR, "scripts", "mesin", nama), "rb") as f:
                self.assertEqual(hashlib.sha256(f.read()).hexdigest(), info["sha256"], nama)

    @unittest.skipUnless(ADA_ASLI, "repo skill sumber tidak ada (instalasi pembeli)")
    def test_identik_dengan_skill_sumber(self):
        for nama, asli in ASLI.items():
            with open(asli, "rb") as a, open(os.path.join(AKAR, "scripts", "mesin", nama), "rb") as b:
                self.assertEqual(a.read(), b.read(), "mesin/%s berbeda dari %s" % (nama, asli))

    def test_mesin_diubah_ditolak(self):
        tmp = tempfile.mkdtemp()
        try:
            salinan = os.path.join(tmp, "mesin")
            shutil.copytree(os.path.join(AKAR, "scripts", "mesin"), salinan)
            with open(os.path.join(salinan, "ter_tabel.json"), "a", encoding="utf-8") as f:
                f.write(" ")
            lama = G.MESIN
            G.MESIN = G.Path(salinan)
            try:
                with self.assertRaises(G.Gagal) as c:
                    G.cek_mesin()
                self.assertIn("berbeda dari salinan resmi", c.exception.pesan)
            finally:
                G.MESIN = lama
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- pencocokan angka massal
PTKP = ["TK/0", "TK/1", "TK/2", "TK/3", "K/0", "K/1", "K/2", "K/3"]


def acak_karyawan(rng, i):
    gp = rng.choice([2_900_000, 3_600_000, 4_250_000, 5_000_000, 7_500_000, 9_800_000, 12_500_000, 16_000_000,
                     rng.randrange(2_500_000, 30_000_000, 1000)])
    tt = rng.choice([0, 0, 250_000, 600_000, 1_500_000])
    ttt = rng.choice([0, 0, 300_000, 900_000, 4_000_000])
    bpjs = rng.choice(["kes,tk,jp", "kes,tk,jp", "kes,tk", "kes", "tidak"])
    hk = rng.choice([5, 6])
    jkk = rng.choice(["", "0,24", "0,54", "0,89", "1,27", "1,74"])
    lk = rng.choice(["", "", "2", "1,5+3", "4+4+2", "0,5"])
    ll = rng.choice(["", "", "5", "8+3", "7p" if hk == 6 else "10"])
    return {"nama": "Uji %02d" % i, "ptkp": rng.choice(PTKP), "gaji_pokok": gp, "tunjangan_tetap": tt,
            "tunjangan_tidak_tetap": ttt, "bpjs": bpjs, "hari_kerja": hk, "jkk": jkk, "lembur_hari_kerja": lk,
            "lembur_hari_libur": ll, "bonus": rng.choice([0, 0, 500_000, 2_000_000]),
            "potongan_lain": rng.choice([0, 0, 150_000]), "zakat": rng.choice([0, 0, 125_000])}


class UjiPencocokan(Dasar):
    def _cocokkan(self, bulan, spek, cfg_asli):
        for s in spek:
            opsi = ["--ptkp", s["ptkp"], "--gaji-pokok", str(s["gaji_pokok"]), "--tunjangan-tetap",
                    str(s["tunjangan_tetap"]), "--tunjangan-tidak-tetap", str(s["tunjangan_tidak_tetap"]),
                    "--bpjs", s["bpjs"], "--hari-kerja", str(s["hari_kerja"]), "--masuk", "2020-01-01",
                    "--zakat", str(s["zakat"])]
            if s["jkk"]:
                opsi += ["--jkk", s["jkk"]]
            if "kes" not in s["bpjs"] or "tk" not in s["bpjs"]:
                opsi += ["--ya-saya-paham"]          # v1.0.1: tanpa BPJS butuh persetujuan khusus
            s["kode"] = self.tambah(s["nama"], *opsi)["kode"]
            isi = []
            for k in ("lembur_hari_kerja", "lembur_hari_libur", "bonus", "potongan_lain"):
                if s[k]:
                    isi += ["--" + k.replace("_", "-"), str(s[k])]
            if isi:
                self.ok("isi", "--bulan", bulan, "--karyawan", s["kode"], *isi)
        hasil, _ = self.hasil(bulan)
        # jalankan script ASLI per orang dengan argumen yang disusun tes ini sendiri
        for s in spek:
            bp = s["bpjs"]
            f = self.file("asli-%s.csv" % s["kode"],
                          "nama;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;lembur_hari_kerja;"
                          "lembur_hari_libur;bonus;potongan_lain;zakat;jkk_persen;ikut_bpjs_kesehatan;ikut_bpjs_tk;"
                          "ikut_jp\n%s;%s;%d;%d;%d;%s;%s;%d;%d;%d;%s;%s;%s;%s\n" % (
                              s["nama"], s["ptkp"], s["gaji_pokok"], s["tunjangan_tetap"], s["tunjangan_tidak_tetap"],
                              s["lembur_hari_kerja"], s["lembur_hari_libur"], s["bonus"], s["potongan_lain"], s["zakat"],
                              s["jkk"], "ya" if "kes" in bp else "tidak", "ya" if "tk" in bp else "tidak",
                              "ya" if "jp" in bp else "tidak"))
            asli = jalankan_asli("payroll.py", ["--data", f, "--periode", bulan, "--format", "json", "--out",
                                                os.path.join(self.dir, "o"), "--hari-kerja", str(s["hari_kerja"])]
                                 + cfg_asli)["karyawan"][0]
            kita = hasil[s["kode"]]["payroll"]
            for kunci in ("pendapatan", "potongan", "iuran", "total_pendapatan", "total_potongan", "take_home_pay",
                          "iuran_perusahaan", "biaya_perusahaan", "pph", "pph_disetor", "upah_tetap"):
                self.assertEqual(kita[kunci], asli[kunci], "%s %s %s" % (bulan, s["nama"], kunci))
            self.assertEqual(kita["pph_info"]["bruto"], asli["pph_info"]["bruto"])
        return hasil

    def test_massal_acak_cocok_dengan_slip_gaji_bpjs(self):
        rng = random.Random(20260926)
        self.ok("atur", "--umk", "3.450.000", "--jkk", "0,54")
        n = 0
        for bulan in ("2026-02", "2026-03", "2026-09"):      # batas JP berganti Maret 2026
            spek = [acak_karyawan(rng, n + i) for i in range(20)]
            n += 20
            for s in spek:
                s["nama"] = "Uji %s %02d" % (bulan, spek.index(s))
            hasil = self._cocokkan(bulan, spek, ["--umk", "3450000", "--jkk", "0.54"])
            # total perusahaan = jumlah per karyawan
            tot = G.total_perusahaan([{"payroll": h["payroll"], "potongan_tidak_masuk": 0,
                                       "potongan_lain_saja": h["potongan_lain_saja"]} for h in hasil.values()])
            out = self.ok("rekap", "--bulan", bulan)
            for k in ("take_home_pay", "setor_pph21", "setor_bpjs_kesehatan", "setor_bpjs_ketenagakerjaan",
                      "biaya_perusahaan"):
                self.assertEqual(Decimal(str(out["total"][k])), tot[k], k)
            # hanya karyawan bulan ini + bulan sebelumnya yang masih aktif ikut dihitung
            self.assertEqual(out["total"]["jumlah_karyawan"], n)

    def test_angka_contoh_manual(self):
        # Contoh SKILL.md slip-gaji-bpjs: Budi K/1, pokok 5 jt, tunj. tetap 500 rb, uang makan 600 rb,
        # lembur 2+3 jam hari kerja + 8 jam libur, kasbon 100 rb, UMK 5.396.761, JKK 0,54% -> THP Rp 6.521.091.
        self.ok("atur", "--umk", "5.396.761", "--jkk", "0,54")
        k = self.tambah("Budi", "--ptkp", "K/1", "--gaji-pokok", "5jt", "--tunjangan-tetap", "500rb",
                        "--tunjangan-tidak-tetap", "600rb", "--masuk", "2021-01-04")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "Budi", "--lembur-hari-kerja", "2+3",
                "--lembur-hari-libur", "8", "--kasbon", "100rb")
        h, _ = self.hasil("2026-09")
        p = h[k["kode"]]["payroll"]
        self.assertEqual(p["pendapatan"]["Lembur"], 794798)
        self.assertEqual(p["pph"], 53707)
        self.assertEqual(p["take_home_pay"], 6521091)
        self.assertEqual(p["biaya_perusahaan"], 7474498)


# --------------------------------------------------------------------------- Desember, keluar/masuk tengah bulan
def pasal17(pkp):
    lap = [(60_000_000, 5), (250_000_000, 15), (500_000_000, 25), (5_000_000_000, 30), (None, 35)]
    sisa, bawah, pajak = pkp, 0, Decimal(0)
    for atas, t in lap:
        porsi = sisa if atas is None else min(sisa, atas - bawah)
        if porsi <= 0:
            break
        pajak += Decimal(porsi) * t / 100
        sisa -= porsi
        bawah = atas or bawah
    return pajak.to_integral_value(rounding=ROUND_FLOOR)


class UjiSetahun(Dasar):
    def setUp(self):
        super().setUp()
        self.ok("atur", "--jkk", "0,24")

    def jalankan_bulan(self, dari, sampai, tahun=2026):
        for b in range(dari, sampai + 1):
            kode = "%d-%02d" % (tahun, b)
            self.ok("hitung", "--bulan", kode)
            self.ok("final", "--bulan", kode, "--ya")

    def test_desember_cocok_pph21_ter_dan_pasal17_manual(self):
        a = self.tambah("Ani", "--ptkp", "K/0", "--gaji-pokok", "9,5jt", "--tunjangan-tetap", "1jt",
                        "--masuk", "2018-05-02", "--nik", NIK, "--rekening", REK)["kode"]
        b = self.tambah("Bayu", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2026-04-20")["kode"]
        c = self.tambah("Citra", "--ptkp", "K/3", "--gaji-pokok", "22jt", "--tunjangan-tetap", "3jt",
                        "--bpjs", "kes,tk", "--masuk", "2016-01-01")["kode"]
        self.ok("isi", "--bulan", "2026-03", "--karyawan", a, "--bonus", "10jt")
        self.gagal("isi", "--bulan", "2026-03", "--karyawan", b, "--bonus", "1jt")   # Bayu belum masuk
        self.jalankan_bulan(1, 11)
        self.ok("isi", "--bulan", "2026-12", "--karyawan", c, "--bonus", "25jt")
        h, _ = self.hasil("2026-12")
        # Bayu: bulan mulai April (masuk 20/4 = bulan April dihitung satu bulan penuh)
        self.assertEqual(h[b]["masa_terakhir"]["bulan_mulai"], 4)
        self.assertEqual(h[b]["payroll"]["pph_info"]["detail"]["biaya_jabatan_maks"], 500000 * 9)
        self.ok("final", "--bulan", "2026-12", "--ya")
        out = self.ok("pph21-tahunan", "--tahun", "2026")
        self.assertFalse(out["ada_selisih"], out)
        self.assertEqual(len(out["karyawan"]), 3)
        # hitung manual Pasal 17 untuk Ani dari data tersimpan
        c_ = sqlite3.connect(self.db)
        rows = [json.loads(r[0]) for r in c_.execute(
            "SELECT h.data FROM hasil h JOIN periode p ON p.id=h.periode_id AND p.revisi=h.revisi "
            "JOIN karyawan k ON k.id=h.karyawan_id WHERE k.kode=?", (a,))]
        c_.close()
        bruto = sum(Decimal(str(r["payroll"]["pph_info"]["bruto"])) for r in rows)
        iuran = sum(Decimal(str(r["payroll"]["iuran"]["jht_karyawan"])) + Decimal(str(r["payroll"]["iuran"]["jp_karyawan"]))
                    for r in rows)
        bj = min(bruto * 5 / 100, Decimal(6_000_000))
        pkp = int(((bruto - bj - iuran - 58_500_000) / 1000).to_integral_value(rounding=ROUND_FLOOR) * 1000)
        pph_setahun = pasal17(pkp)
        total = sum(Decimal(str(r["payroll"]["pph"])) for r in rows)
        self.assertEqual(total, pph_setahun)
        # angka Desember sama dengan payroll.py ASLI yang diberi total Jan-Nov oleh tes ini
        ani = [r for r in rows]
        lalu = [r for r in ani if r["payroll"]["pph_info"]["masa_terakhir"] is False]
        f = self.file("des.csv", "nama;ptkp;gaji_pokok;tunjangan_tetap;jkk_persen;bruto_sd_bulan_lalu;pph21_sd_bulan_lalu;"
                      "iuran_sd_bulan_lalu;bulan_mulai\nAni;K/0;9500000;1000000;0.24;%s;%s;%s;1\n" % (
                          sum(Decimal(str(r["payroll"]["pph_info"]["bruto"])) for r in lalu),
                          sum(Decimal(str(r["payroll"]["pph"])) for r in lalu),
                          sum(Decimal(str(r["payroll"]["iuran"]["jht_karyawan"])) +
                              Decimal(str(r["payroll"]["iuran"]["jp_karyawan"])) for r in lalu)))
        asli = jalankan_asli("payroll.py", ["--data", f, "--periode", "2026-12", "--format", "json", "--out",
                                            os.path.join(self.dir, "o")])["karyawan"][0]
        self.assertEqual(h[a]["payroll"]["pph"], asli["pph"])
        self.assertEqual(h[a]["payroll"]["take_home_pay"], asli["take_home_pay"])

    def test_keluar_tengah_bulan(self):
        j = self.tambah("Joko", "--ptkp", "K/2", "--gaji-pokok", "8jt", "--masuk", "2026-01-05")["kode"]
        self.tambah("Lina", "--ptkp", "TK/0", "--gaji-pokok", "5jt", "--masuk", "2025-06-01")
        self.jalankan_bulan(1, 10)
        self.ok("karyawan", "keluar", "--karyawan", "Joko", "--tanggal", "2026-11-14", "--ya")
        h, out = self.hasil("2026-11")
        self.assertTrue(h[j]["berhenti"])
        self.assertTrue(h[j]["payroll"]["pph_info"]["masa_terakhir"])
        self.assertEqual(h[j]["masa_terakhir"]["alasan"], "berhenti bekerja")
        self.assertEqual(h[j]["payroll"]["pendapatan"]["Gaji pokok"], 8000000)       # tidak diprorata otomatis
        self.assertTrue(any("keluar 14/11/2026" in p and "PENUH" in p for p in out["peringatan_hitung"]))
        # gaji dibayar sesuai perjanjian kerja (diisi pengguna) -> dipakai sebagai gaji pokok bulan itu
        self.ok("isi", "--bulan", "2026-11", "--karyawan", j, "--gaji-pokok-dibayar", "3.733.333")
        h, _ = self.hasil("2026-11")
        self.assertEqual(h[j]["payroll"]["pendapatan"]["Gaji pokok"], 3733333)
        lalu = h[j]["masa_terakhir"]
        f = self.file("k.csv", "nama;ptkp;gaji_pokok;jkk_persen;berhenti;bruto_sd_bulan_lalu;pph21_sd_bulan_lalu;"
                      "iuran_sd_bulan_lalu;bulan_mulai\nJoko;K/2;3733333;0.24;ya;%s;%s;%s;1\n" % (
                          lalu["bruto_sd_bulan_lalu"], lalu["pph21_sd_bulan_lalu"], lalu["iuran_sd_bulan_lalu"]))
        asli = jalankan_asli("payroll.py", ["--data", f, "--periode", "2026-11", "--format", "json", "--out",
                                            os.path.join(self.dir, "o")])["karyawan"][0]
        self.assertEqual(h[j]["payroll"]["pph"], asli["pph"])
        self.assertEqual(h[j]["payroll"]["take_home_pay"], asli["take_home_pay"])
        self.ok("final", "--bulan", "2026-11", "--ya")
        h12, _ = self.hasil("2026-12")
        self.assertNotIn(j, h12)                                        # tidak ikut bulan setelah keluar
        self.gagal("isi", "--bulan", "2026-12", "--karyawan", j, "--bonus", "1")
        self.ok("final", "--bulan", "2026-12", "--ya")
        out = self.ok("pph21-tahunan", "--tahun", "2026")
        self.assertFalse(out["ada_selisih"], out)

    def test_masuk_tengah_bulan(self):
        d = self.tambah("Dewi", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2026-10-15")["kode"]
        self.tambah("Eko", "--ptkp", "TK/0", "--gaji-pokok", "5jt", "--masuk", "2024-01-01")
        h9, _ = self.hasil("2026-09")
        self.assertNotIn(d, h9)
        h, out = self.hasil("2026-10")
        self.assertTrue(h[d]["masuk_tengah_bulan"])
        self.assertTrue(any("Dewi" in p and "PENUH" in p for p in out["peringatan_hitung"]))
        self.ok("isi", "--bulan", "2026-10", "--karyawan", d, "--gaji-pokok-dibayar", "3,3jt")
        h, out = self.hasil("2026-10")
        self.assertEqual(h[d]["payroll"]["pendapatan"]["Gaji pokok"], 3300000)
        self.assertFalse(any("Dewi" in p and "PENUH" in p for p in out["peringatan_hitung"]))

    def test_masa_terakhir_butuh_data_lengkap_dan_saldo_awal(self):
        e = self.tambah("Eko", "--ptkp", "K/1", "--gaji-pokok", "12jt", "--masuk", "2020-01-01")["kode"]
        out = self.gagal("hitung", "--bulan", "2026-12")
        # v1.0.13: semua karyawan tertunda -> gagal dengan daftar data yang dibutuhkan (bahasa awam)
        self.assertIn("total Januari–November 2026", out["error"])
        self.assertEqual([t["kode"] for t in out["tertunda"]], [e])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM hasil"), 0)
        self.ok("saldo-awal", "--karyawan", e, "--tahun", "2026", "--sampai-bulan", "10", "--bruto", "130.000.000",
                "--pph21", "2.500.000", "--iuran", "3.000.000")
        out = self.gagal("hitung", "--bulan", "2026-12")
        self.assertIn("November 2026", out["error"])
        self.jalankan_bulan(11, 11)
        h, _ = self.hasil("2026-12")
        mt = h[e]["masa_terakhir"]
        self.assertEqual(mt["bulan_mulai"], 1)
        nov = self.ok("rekap", "--bulan", "2026-11")["karyawan"][0]
        self.assertEqual(Decimal(str(mt["pph21_sd_bulan_lalu"])), 2_500_000 + Decimal(str(nov["pph21"])))
        self.ok("final", "--bulan", "2026-12", "--ya")
        self.assertFalse(self.ok("pph21-tahunan", "--tahun", "2026")["ada_selisih"])
        self.gagal("saldo-awal", "--karyawan", e, "--tahun", "2026", "--sampai-bulan", "12", "--bruto", "1")

    def test_revisi_bulan_lalu_mengubah_desember(self):
        self.tambah("Fani", "--ptkp", "TK/0", "--gaji-pokok", "11jt", "--masuk", "2019-01-01")
        self.jalankan_bulan(1, 12)
        sebelum = self.ok("rekap", "--bulan", "2026-12")["karyawan"][0]["pph21"]
        out = self.ok("revisi", "--bulan", "2026-06", "--alasan", "bonus Juni terlewat", "--ya")
        self.assertTrue(any("2026-12" in p for p in out["peringatan"]))
        self.ok("isi", "--bulan", "2026-06", "--karyawan", "Fani", "--bonus", "20jt")
        self.ok("hitung", "--bulan", "2026-06")
        self.ok("final", "--bulan", "2026-06", "--ya")
        self.ok("revisi", "--bulan", "2026-12", "--alasan", "ikut revisi Juni", "--ya")
        self.ok("hitung", "--bulan", "2026-12")
        out = self.ok("final", "--bulan", "2026-12", "--ya")
        self.assertNotEqual(out["selisih"], [])
        self.assertNotEqual(self.ok("rekap", "--bulan", "2026-12")["karyawan"][0]["pph21"], sebelum)
        self.assertFalse(self.ok("pph21-tahunan", "--tahun", "2026")["ada_selisih"])


# --------------------------------------------------------------------------- THR
class UjiDTP(Dasar):
    def test_slip_dtp_dipotong_lalu_dibayar_tunai(self):
        # PMK 105/2025 Pasal 2 ayat 1, Pasal 5, Lampiran B (cek 2026-10-05): PPh 21 dipotong, DTP tunai nilai sama,
        # gaji bersih tidak berkurang karena pajak (bukan gaji + DTP), setoran bagian DTP Rp 0
        k = self.tambah("Rina", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2020-01-01", "--dtp", "ya",
                        "--bruto-tetap-januari", "6jt")["kode"]
        h, _ = self.hasil("2026-09")
        p = h[k]["payroll"]
        self.assertTrue(p["dtp"])
        pph = p["potongan"]["PPh 21"]
        self.assertGreater(pph, 0)
        self.assertEqual(p["pendapatan"]["PPh 21 DTP dibayar tunai"], pph)
        self.assertEqual(p["pph_disetor"], 0)
        i = p["iuran"]
        self.assertEqual(p["take_home_pay"], 6000000 - i["kes_karyawan"] - i["jht_karyawan"] - i["jp_karyawan"])
        slip = self.ok("slip", "--bulan", "2026-09", "--karyawan", "Rina", "--keluar", self.dir)["teks"]
        self.assertIn("tetap dipotong", slip)
        self.assertIn("Setoran PPh 21 ke negara untuk karyawan ini: Rp 0", slip)

    def test_total_dtp_dipotong_vs_disetor_dipisah(self):
        # v1.0.11: total.pph21_dipotong = yang DIPOTONG (termasuk DTP); pph21_dtp & pph21_disetor_ke_negara terpisah
        self.tambah("Rina", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2020-01-01", "--dtp", "ya",
                    "--bruto-tetap-januari", "6jt")
        self.tambah("Andi", "--ptkp", "K/1", "--gaji-pokok", "9jt", "--masuk", "2022-01-01")
        h, out = self.hasil("2026-09")
        tot = out["total"]
        dipotong = sum(Decimal(str(x["payroll"]["potongan"]["PPh 21"])) for x in h.values())
        dtp = sum(Decimal(str(x["payroll"]["pendapatan"]["PPh 21 DTP dibayar tunai"])) for x in h.values())
        setor = sum(Decimal(str(x["payroll"]["pph_disetor"])) for x in h.values())
        self.assertGreater(dtp, 0)
        self.assertGreater(setor, 0)
        self.assertEqual(Decimal(str(tot["pph21_dipotong"])), dipotong)
        self.assertEqual(Decimal(str(tot["pph21_dtp"])), dtp)
        self.assertEqual(Decimal(str(tot["pph21_disetor_ke_negara"])), setor)
        self.assertEqual(Decimal(str(tot["setor_pph21"])), setor)
        self.assertEqual(dipotong, dtp + setor)
        self.assertIn("PPh 21 dipotong dari gaji bulan ini: %s (termasuk DTP %s" % (G.rp(dipotong), G.rp(dtp)), out["teks"])
        self.assertIn("- Setor PPh 21 ke negara: %s" % G.rp(setor), out["teks"])


class UjiTHR(Dasar):
    def test_thr_cocok_hitung_thr(self):
        self.tambah("Gita", "--ptkp", "TK/0", "--gaji-pokok", "5jt", "--tunjangan-tetap", "500rb", "--masuk", "2019-07-01")
        self.tambah("Hadi", "--ptkp", "K/1", "--gaji-pokok", "4,8jt", "--jenis", "kontrak", "--masuk", "2026-06-15")
        self.tambah("Iwan", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk", "2027-02-20")
        prev = self.ok("thr", "--bulan", "2027-03", "--hari-raya", "2027-03-10", "--nama-hari-raya", "Idul Fitri",
                       hari_ini="2027-02-25")
        self.assertTrue(prev["perlu_konfirmasi"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM isian WHERE kolom='thr'"), 0)
        self.ok("thr", "--bulan", "2027-03", "--hari-raya", "2027-03-10", "--nama-hari-raya", "Idul Fitri", "--ya",
                hari_ini="2027-02-25")
        f = self.file("thr.csv", "nama;jenis;ptkp;gaji_pokok;tunjangan_tetap;tanggal_mulai\n"
                      "Gita;tetap;TK/0;5000000;500000;2019-07-01\nHadi;kontrak;K/1;4800000;;2026-06-15\n"
                      "Iwan;tetap;TK/0;4000000;;2027-02-20\n")
        asli = {k["nama"]: k["thr"] for k in jalankan_asli("thr.py", ["--data", f, "--hari-raya", "2027-03-10",
                                                                       "--format", "json", "--hari-ini", "2027-02-25"])
                ["karyawan"]}
        self.ok("atur", "--batas-jp", "11.086.300")
        h, _ = self.hasil("2027-03")
        by = {x["nama"]: x for x in h.values()}
        self.assertEqual(by["Gita"]["payroll"]["pendapatan"]["Bonus/THR"], asli["Gita"])
        self.assertEqual(by["Hadi"]["payroll"]["pendapatan"]["Bonus/THR"], asli["Hadi"])
        self.assertEqual(asli["Iwan"], 0)
        self.assertEqual(by["Iwan"]["payroll"]["pendapatan"]["Bonus/THR"], 0)

    def test_thr_bulan_salah(self):
        self.tambah("Gita", "--ptkp", "TK/0", "--gaji-pokok", "5jt", "--masuk", "2019-07-01")
        out = self.gagal("thr", "--bulan", "2027-02", "--hari-raya", "2027-03-10", "--ya", hari_ini="2027-02-01")
        self.assertIn("tidak berada di periode", out["error"])


# --------------------------------------------------------------------------- data rusak & pratinjau
class UjiDataRusak(Dasar):
    def test_impor_karyawan_semua_atau_tidak_sama_sekali(self):
        f = self.file("k.csv", "nama;ptkp;gaji_pokok;masuk;nik;rekening\n"
                               "Andi;K/1;5.000.000;2024-01-02;;\n"
                               "Budi;K/4;4jt;2024-01-02;;\n"
                               "Cici;TK/0;-3jt;2024-01-02;;\n"
                               "Dodo;TK/0;1,250,000.50;2024-01-02;;\n"
                               "Euis;TK/0;4jt;31/02/2024;;\n"
                               "Fajar;TK/0;4jt;2024-01-02;320101010101;\n"
                               "Gina;TK/0;4jt;2024-01-02;;1,23457E+12\n")
        out = self.gagal("karyawan", "impor", f, "--ya")
        self.assertEqual(len(out["galat"]), 6, out)
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 0)

    def test_file_tidak_valid(self):
        self.gagal("karyawan", "impor", self.file("kosong.csv", ""))
        self.gagal("karyawan", "impor", self.file("judul.csv", "nama;ptkp;gaji_pokok;masuk\n"))
        self.gagal("karyawan", "impor", self.file("kolom.csv", "nama;gaji\nA;1\n"))
        p = os.path.join(self.dir, "x.xlsx")
        with open(p, "wb") as f:
            f.write(b"PK\x03\x04isi")
        self.assertIn("Excel", self.gagal("karyawan", "impor", p)["error"])
        self.gagal("karyawan", "impor", os.path.join(self.dir, "tidak-ada.csv"))

    def test_pratinjau_tidak_menyimpan(self):
        out = self.ok("karyawan", "tambah", "--nama", "A", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk", "2024-01-01")
        self.assertTrue(out["perlu_konfirmasi"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 0)

    def test_karyawan_tanpa_data_wajib(self):
        self.assertIn("--masuk", self.gagal("karyawan", "tambah", "--nama", "A", "--ptkp", "TK/0", "--gaji-pokok",
                                            "4jt", "--ya")["error"])
        self.gagal("karyawan", "tambah", "--nama", "A", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk",
                   "2024-01-01", "--bpjs", "jp", "--ya")
        self.gagal("karyawan", "tambah", "--nama", "A", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk",
                   "2024-01-01", "--jenis", "harian", "--ya")
        self.gagal("karyawan", "tambah", "--nama", "A", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk",
                   "2024-01-01", "--jkk", "15", "--ya")
        self.tambah("A", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk", "2024-01-01", "--nik", NIK)
        self.gagal("karyawan", "tambah", "--nama", "B", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk",
                   "2024-01-01", "--nik", NIK, "--ya")

    def test_isian_rusak(self):
        self.tambah("Andi", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk", "2024-01-01")
        self.gagal("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--lembur-hari-kerja", "dua jam")
        self.gagal("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--lembur-hari-kerja", "3p")
        self.gagal("isi", "--bulan", "2026-13", "--karyawan", "Andi", "--bonus", "1")
        self.gagal("isi", "--bulan", "2026-09", "--karyawan", "Siapa", "--bonus", "1")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--lembur-rp", "200rb")
        self.gagal("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--lembur-hari-kerja", "2")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--lembur-rp", "-", "--lembur-hari-kerja", "2")
        # lembur hari libur melebihi tangga PP 35/2021 -> mesin slip-gaji-bpjs menolak, tidak ada hasil tersimpan
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--lembur-hari-libur", "13")
        out = self.gagal("hitung", "--bulan", "2026-09")
        # v1.0.13: baris yang ditolak mesin menjadi 'tertunda' per karyawan (pesan awam); di sini semua tertunda
        self.assertIn("melebihi 12 jam", out["error"])
        self.assertEqual([t["kode"] for t in out["tertunda"]], ["K001"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM hasil"), 0)

    def test_nama_dengan_koma_dan_titik_koma(self):
        k = self.tambah("Budi, S.E.; \"Jr\"", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--jabatan", "Staf, Gudang",
                        "--masuk", "2024-01-01", "--jkk", "0,89")["kode"]
        self.ok("isi", "--bulan", "2026-09", "--karyawan", k, "--lembur-hari-kerja", "1,5+2")
        h, _ = self.hasil("2026-09")
        self.assertEqual(h[k]["nama"], 'Budi, S.E.; "Jr"')
        self.assertEqual(h[k]["payroll"]["jkk_persen"], "0.89")
        self.assertEqual(h[k]["payroll"]["pendapatan"]["Lembur"],
                         int((Decimal("6") * 4_000_000 / 173).to_integral_value(rounding="ROUND_HALF_UP")))

    def test_nama_kembar_dan_cli_salah(self):
        self.tambah("Sari", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk", "2024-01-01")
        self.tambah("Sari", "--ptkp", "K/0", "--gaji-pokok", "5jt", "--masuk", "2024-01-01")
        out = self.gagal("isi", "--bulan", "2026-09", "--karyawan", "Sari", "--bonus", "1")
        self.assertEqual(len(out["pilihan"]), 2)
        kode, _, _ = self.cli("hitung")
        self.assertEqual(kode, 2)

    def test_database_bukan_milik_aplikasi(self):
        lain = os.path.join(self.dir, "lain.db")
        c = sqlite3.connect(lain)
        c.execute("CREATE TABLE x(a)")
        c.commit()
        c.close()
        kode, out, _ = self.cli("info")
        self.assertEqual(kode, 0)
        self.db = lain
        self.assertIn("bukan database gaji-umkm", self.gagal("karyawan", "daftar")["error"])


# --------------------------------------------------------------------------- absensi-lokal
class UjiAbsensi(Dasar):
    def setUp(self):
        super().setUp()
        self.tambah("Andi", "--ptkp", "K/1", "--gaji-pokok", "5jt", "--tunjangan-tetap", "500rb", "--masuk",
                    "2023-01-01", "--kode-absensi", "A01", "--hari-kerja", "6")
        self.tambah("Sari", "--ptkp", "TK/0", "--gaji-pokok", "4,5jt", "--masuk", "2023-01-01")
        self.csv = self.file("abs.csv",
                             "nama;jabatan;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;lembur_hari_kerja;"
                             "lembur_hari_libur;kode_absensi;hari_hadir;hari_alpa;terlambat_menit\n"
                             "Andi (nama di mesin);;;5000000;500000;;2+1,5;8+6p;A01;24;0;6\n"
                             "Sari;;;4500000;;;;;A02;19;2;0\n")

    def test_impor_lembur_tanpa_potongan_otomatis(self):
        prev = self.ok("impor-absensi", self.csv, "--bulan", "2026-09")
        self.assertTrue(prev["perlu_konfirmasi"])
        out = self.ok("impor-absensi", self.csv, "--bulan", "2026-09", "--ya")
        self.assertTrue(any("TIDAK dipotong otomatis" in p for p in out["peringatan"]))
        h, _ = self.hasil("2026-09")
        andi = [x for x in h.values() if x["nama"] == "Andi"][0]
        # (1,5+2) + (1,5+2x0,5) + libur pola 6: 7x2+1x3 = 17 ; libur hari terpendek 6 jam: 5x2+1x3 = 13 -> 36 jam setara
        self.assertEqual(andi["payroll"]["pendapatan"]["Lembur"], int((Decimal(36) * 5_500_000 / 173)
                                                                      .to_integral_value(rounding="ROUND_HALF_UP")))
        sari = [x for x in h.values() if x["nama"] == "Sari"][0]
        self.assertEqual(sari["potongan_tidak_masuk"], 0)

    def test_potongan_alpa_hanya_dengan_dasar(self):
        self.gagal("atur", "--potongan-per-hari-alpa", "150rb")
        self.ok("atur", "--potongan-per-hari-alpa", "150rb", "--dasar-potongan", "Peraturan Perusahaan Pasal 12")
        self.ok("impor-absensi", self.csv, "--bulan", "2026-09", "--ya")
        h, _ = self.hasil("2026-09")
        sari = [x for x in h.values() if x["nama"] == "Sari"][0]
        self.assertEqual(sari["potongan_tidak_masuk"], 300000)
        self.assertEqual(sari["payroll"]["potongan"]["Potongan lain"], 300000)
        slip = self.ok("slip", "--bulan", "2026-09", "--karyawan", "Sari", "--keluar", self.dir)["teks"]
        self.assertIn("Potongan tidak masuk | Rp 300.000", slip)

    def test_nama_tidak_dikenal(self):
        f = self.file("abs2.csv", "nama;lembur_hari_kerja;lembur_hari_libur;hari_alpa\nBudi;2;;0\n")
        self.assertIn("tidak ada di data gaji", self.gagal("impor-absensi", f, "--bulan", "2026-09", "--ya")["error"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM isian"), 0)

    @unittest.skipUnless(os.path.isfile(os.path.join(REPO_SKILLS, "absensi-lokal", "scripts", "absensi.py")),
                         "absensi-lokal tidak ada")
    def test_file_asli_absensi_lokal(self):
        ab = os.path.join(REPO_SKILLS, "absensi-lokal", "scripts", "absensi.py")
        adb = os.path.join(self.dir, "absensi.db")

        def a(*argv):
            p = subprocess.run([sys.executable, ab] + list(argv) + ["--db", adb, "--json", "--sekarang",
                                                                    "2026-09-30 23:00"], capture_output=True)
            self.assertEqual(p.returncode, 0, p.stdout.decode() + p.stderr.decode())
        a("init", "--ya")
        a("karyawan", "tambah", "--kode", "A01", "--nama", "Andi", "--gaji-pokok", "5jt", "--tunjangan-tetap", "500rb",
          "--ya")
        a("lembur", "--karyawan", "Andi", "--tanggal", "2026-09-22", "--jam", "3", "--catatan", "perintah pemilik", "--ya")
        csv_gaji = os.path.join(self.dir, "lembur-gaji.csv")
        a("rekap", "--bulan", "2026-09", "--csv-gaji", csv_gaji)
        self.ok("karyawan", "ubah", "--karyawan", "Andi", "--hari-kerja", "5", "--ya")
        self.ok("impor-absensi", csv_gaji, "--bulan", "2026-09", "--ya")
        h, _ = self.hasil("2026-09")
        andi = [x for x in h.values() if x["nama"] == "Andi"][0]
        self.assertEqual(andi["payroll"]["pendapatan"]["Lembur"], int((Decimal("5.5") * 5_500_000 / 173)
                                                                      .to_integral_value(rounding="ROUND_HALF_UP")))


# --------------------------------------------------------------------------- kunci, revisi, penyamaran
class UjiKunciDanPrivasi(Dasar):
    def setUp(self):
        super().setUp()
        self.k = self.tambah("Andi", "--ptkp", "K/1", "--gaji-pokok", "6jt", "--masuk", "2022-01-01", "--nik", NIK,
                             "--bank", "BCA", "--rekening", REK)["kode"]
        self.tambah("Tanpa Rek", "--ptkp", "TK/0", "--gaji-pokok", "4jt", "--masuk", "2022-01-01")

    def test_final_mengunci_dan_revisi_tercatat(self):
        self.ok("hitung", "--bulan", "2026-09")
        self.gagal("transfer", "--bulan", "2026-09", "--keluar", self.dir)            # draf belum boleh transfer
        self.ok("karyawan", "ubah", "--karyawan", "Andi", "--gaji-pokok", "6,5jt", "--ya")
        self.assertIn("berubah sejak", self.gagal("final", "--bulan", "2026-09", "--ya")["error"])
        self.ok("hitung", "--bulan", "2026-09")
        self.ok("final", "--bulan", "2026-09")                                           # pratinjau
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM periode WHERE status='final'"), 0)
        self.ok("final", "--bulan", "2026-09", "--ya")
        for argv in (["isi", "--bulan", "2026-09", "--karyawan", "Andi", "--bonus", "1"],
                     ["hitung", "--bulan", "2026-09"], ["final", "--bulan", "2026-09", "--ya"]):
            self.assertTrue(self.gagal(*argv).get("terkunci", True))
        self.gagal("revisi", "--bulan", "2026-09", "--alasan", "x", "--ya")               # alasan terlalu pendek
        self.ok("revisi", "--bulan", "2026-09", "--alasan", "bonus Andi terlewat", "--ya")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--bonus", "1jt")
        self.ok("hitung", "--bulan", "2026-09")
        out = self.ok("final", "--bulan", "2026-09", "--ya")
        self.assertEqual(out["selisih"][0]["kode"], self.k)
        self.assertEqual(self.jumlah("SELECT COUNT(DISTINCT revisi) FROM hasil"), 2)   # hasil lama tetap ada
        per = self.ok("periode")["periode"][0]
        self.assertEqual(per["revisi_log"][0]["alasan"], "bonus Andi terlewat")
        self.assertTrue(per["revisi_log"][0]["difinalkan"])
        tr = self.ok("transfer", "--bulan", "2026-09", "--keluar", self.dir, "--rekening-lengkap")
        with open(tr["file"], encoding="utf-8-sig") as f:
            isi = f.read()
        selisih = out["selisih"][0]["rincian"]["gaji_bersih"]["selisih"]
        self.assertIn(";%s;" % selisih, isi)
        self.assertEqual(tr["jumlah"], 1)

    def test_nik_dan_rekening_disamarkan(self):
        keluaran = []
        for argv in (["karyawan", "daftar"], ["hitung", "--bulan", "2026-09"], ["rekap", "--bulan", "2026-09"],
                     ["slip", "--bulan", "2026-09", "--keluar", self.dir], ["final", "--bulan", "2026-09", "--ya"],
                     ["transfer", "--bulan", "2026-09", "--keluar", self.dir], ["pengingat", "--rentang", "30"],
                     ["karyawan", "ubah", "--karyawan", "Andi", "--rekening", "5555566666", "--ya"]):
            kode, out, teks = self.cli(*argv)
            self.assertEqual(kode, 0, out)
            keluaran.append(teks)
            for f in (out.get("file") or []) if isinstance(out.get("file"), list) else [out.get("file")] if out.get(
                    "file") else []:
                with open(f, encoding="utf-8-sig") as fh:
                    keluaran.append(fh.read())
        semua = "\n".join(keluaran)
        for rahasia in (NIK, REK, "5555566666"):
            self.assertNotIn(rahasia, semua)
        self.assertIn("************9999", semua)
        self.assertIn("******9876", semua)
        # --rekening-lengkap: nomor lengkap hanya di file, tidak di keluaran perintah
        kode, out, teks = self.cli("transfer", "--bulan", "2026-09", "--keluar", self.dir, "--rekening-lengkap")
        self.assertNotIn("5555566666", teks)
        with open(out["file"], encoding="utf-8-sig") as f:
            self.assertIn("5555566666", f.read())
        self.assertTrue(any("Belum ada nomor rekening" in p for p in out["peringatan"]))

    def test_pengingat_geser_akhir_pekan_tanpa_nama(self):
        self.ok("hitung", "--bulan", "2026-10")
        self.ok("final", "--bulan", "2026-10", "--ya")
        out = self.ok("pengingat", "--rentang", "14", hari_ini="2026-11-08")
        teks = out["teks"]
        self.assertIn("Sen 16/11/2026: Batas setor PPh 21 masa Oktober 2026", teks)   # 15/11/2026 = Minggu
        self.assertIn("Sel 10/11/2026: Batas setor iuran BPJS Kesehatan", teks)
        self.assertIn("Jum 20/11/2026: Batas lapor SPT Masa PPh 21", teks)
        self.assertNotIn("Andi", teks)
        tot = self.ok("rekap", "--bulan", "2026-10")["total"]
        self.assertIn(G.rp(tot["setor_pph21"]), teks)


# --------------------------------------------------------------------------- backup & restore
class UjiBackup(Dasar):
    def test_restore_aman(self):
        self.tambah("Andi", "--ptkp", "K/1", "--gaji-pokok", "6jt", "--masuk", "2022-01-01")
        b = self.ok("backup", "--label", "uji")["backup"]
        self.tambah("Budi", "--ptkp", "K/1", "--gaji-pokok", "6jt", "--masuk", "2022-01-01")
        self.assertTrue(self.ok("restore", "--dari", b)["perlu_konfirmasi"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 2)
        out = self.ok("restore", "--dari", b, "--ya")
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 1)
        self.assertTrue(os.path.isfile(out["backup"]))                 # database sebelum restore disimpan
        # database rusak -> dipindah (tidak dihapus), cadangan dipasang
        with open(self.db, "wb") as f:
            f.write(b"bukan database" * 100)
        self.assertIn("rusak", self.gagal("karyawan", "daftar")["error"].lower())
        out = self.ok("restore", "--dari", b, "--ya")
        self.assertIn("rusak-gaji-", out["backup"])
        self.assertTrue(os.path.isfile(out["backup"]))
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 1)
        # cadangan palsu ditolak
        palsu = self.file("palsu.db", "")
        c = sqlite3.connect(palsu)
        c.execute("CREATE TABLE meta(kunci, nilai)")
        c.commit()
        c.close()
        self.gagal("restore", "--dari", palsu, "--ya")
        self.gagal("restore", "--dari", os.path.join(self.dir, "tidak-ada.db"), "--ya")

    def test_init_tidak_menimpa(self):
        self.tambah("Andi", "--ptkp", "K/1", "--gaji-pokok", "6jt", "--masuk", "2022-01-01")
        self.gagal("init", "--ya")
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 1)


# --------------------------------------------------------------------------- v1.0.1: temuan penguji Akun B
class UjiV101(Dasar):
    def test_pagar_tanpa_bpjs_butuh_persetujuan_khusus(self):
        e = self.tambah("Eka", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2022-01-01")["kode"]
        # pratinjau: boleh, tapi diberi peringatan + tanda perlu persetujuan khusus
        out = self.ok("karyawan", "ubah", "--karyawan", e, "--bpjs", "tidak")
        self.assertTrue(out["perlu_persetujuan_khusus"])
        self.assertIn("PERLU PERSETUJUAN KHUSUS", out["teks"])
        self.assertIn("UU 24/2011 Pasal 15", out["teks"])
        # --ya saja: ditolak, database tidak berubah
        out = self.gagal("karyawan", "ubah", "--karyawan", e, "--bpjs", "tidak", "--ya")
        self.assertIn("--ya-saya-paham", out["error"])
        self.assertEqual(out["masalah_kepatuhan"], ["tanpa_bpjs_kesehatan", "tanpa_bpjs_ketenagakerjaan"])
        self.assertEqual(self.jumlah("SELECT ikut_kes FROM karyawan WHERE kode='%s'" % e), 1)
        # dengan persetujuan khusus: tersimpan + tercatat di log (audit)
        out = self.ok("karyawan", "ubah", "--karyawan", e, "--bpjs", "tidak", "--ya", "--ya-saya-paham",
                      "--alasan-khusus", "iuran dibayar induk perusahaan")
        self.assertEqual(out["konfirmasi_kepatuhan"]["masalah"], ["tanpa_bpjs_kesehatan", "tanpa_bpjs_ketenagakerjaan"])
        self.assertIn("PERSETUJUAN KHUSUS", out["teks"])
        c = sqlite3.connect(self.db)
        log = c.execute("SELECT ringkasan FROM log WHERE perintah='karyawan ubah' ORDER BY id DESC").fetchone()[0]
        c.close()
        self.assertIn("konfirmasi_kepatuhan", log)
        self.assertIn("iuran dibayar induk perusahaan", log)
        # tiap bulan hitung tetap mengingatkan
        _, out = self.hasil("2026-09")
        self.assertTrue(any("Eka: TIDAK didaftarkan BPJS Kesehatan" in p for p in out["peringatan_hitung"]))
        # perubahan lain pada karyawan yang sudah disetujui tidak meminta persetujuan ulang
        self.ok("karyawan", "ubah", "--karyawan", e, "--jabatan", "Kasir", "--ya")

    def test_pagar_dasar_bpjs_kesehatan_di_bawah_upah(self):
        self.ok("atur", "--umk", "5.396.761")
        c = self.tambah("Citra", "--ptkp", "K/0", "--gaji-pokok", "9jt", "--tunjangan-tetap", "1jt",
                        "--masuk", "2021-01-01")["kode"]
        out = self.gagal("karyawan", "ubah", "--karyawan", c, "--dasar-bpjs-kesehatan", "5.396.761", "--ya")
        self.assertIn("Rp 10.000.000", out["error"])
        self.assertEqual(out["masalah_kepatuhan"], ["dasar_bpjs_kesehatan_rendah"])
        # dasar = upah sebenarnya (atau di atas batas 12 jt) tidak perlu persetujuan
        self.ok("karyawan", "ubah", "--karyawan", c, "--dasar-bpjs-kesehatan", "10jt", "--ya")
        g = self.tambah("Gilang", "--ptkp", "TK/0", "--gaji-pokok", "20jt", "--dasar-bpjs-kesehatan", "12jt",
                        "--masuk", "2021-01-01")["kode"]
        self.gagal("karyawan", "ubah", "--karyawan", g, "--dasar-bpjs-kesehatan", "11jt", "--ya")
        # tambah & impor baru juga dipagari
        self.gagal("karyawan", "tambah", "--nama", "Hadi", "--ptkp", "TK/0", "--gaji-pokok", "8jt", "--masuk",
                   "2024-01-01", "--jenis", "kontrak", "--bpjs", "tidak", "--ya")
        f = self.file("k.csv", "nama;ptkp;gaji_pokok;masuk;bpjs\nIka;TK/0;6000000;2024-01-01;tidak\n"
                               "Jaka;TK/0;6000000;2024-01-01;kes,tk,jp\n")
        out = self.gagal("karyawan", "impor", f, "--ya")
        self.assertIn("baris 2", out["error"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 2)
        self.assertTrue(self.ok("karyawan", "impor", f)["perlu_persetujuan_khusus"])
        self.assertEqual(self.ok("karyawan", "impor", f, "--ya", "--ya-saya-paham")["jumlah"], 2)
        # JP saja tidak diikuti (usaha mikro/kecil belum wajib JP) -> tidak dipagari
        self.ok("karyawan", "ubah", "--karyawan", "Jaka", "--bpjs", "kes,tk", "--ya")

    def test_setor_pph21_dikurangi_kelebihan_dikembalikan(self):
        # Lina: gaji besar Jan-Nov lalu turun drastis di Desember -> lebih potong di Masa Pajak Terakhir
        l = self.tambah("Lina", "--ptkp", "TK/0", "--gaji-pokok", "30jt", "--masuk", "2020-01-01")["kode"]
        m = self.tambah("Mira", "--ptkp", "TK/0", "--gaji-pokok", "8jt", "--masuk", "2020-01-01")["kode"]
        for b in range(1, 12):
            kode = "2026-%02d" % b
            self.ok("isi", "--bulan", kode, "--karyawan", l, "--bonus", "40jt" if b == 3 else "-")
            self.ok("hitung", "--bulan", kode)
            self.ok("final", "--bulan", kode, "--ya")
        self.ok("karyawan", "keluar", "--karyawan", l, "--tanggal", "2026-12-31", "--ya")
        # v1.0.2: keluar 31/12 = bulan penuh; gaji pokok turun ke 1 jt butuh persetujuan khusus (dasar BPJS turun)
        self.ok("isi", "--bulan", "2026-12", "--karyawan", l, "--gaji-pokok-dibayar", "1jt", "--ya-saya-paham",
                "--alasan-khusus", "data uji fiktif: gaji Desember dipotong sesuai PK")
        h, out = self.hasil("2026-12")
        kembali = Decimal(str(h[l]["payroll"]["pendapatan"]["Pengembalian kelebihan PPh 21"]))
        self.assertGreater(kembali, 0)
        dipotong = sum(Decimal(str(x["payroll"]["pph_disetor"])) for x in h.values())   # tanpa DTP: = dipotong
        tot = out["total"]
        self.assertEqual(Decimal(str(tot["pph21_dipotong"])), dipotong)
        self.assertEqual(Decimal(str(tot["pph21_dtp"])), Decimal(0))
        self.assertEqual(tot["pph21_disetor_ke_negara"], tot["setor_pph21"])
        self.assertEqual(Decimal(str(tot["pengembalian_pph21"])), kembali)
        self.assertEqual(Decimal(str(tot["setor_pph21"])), max(dipotong - kembali, Decimal(0)))
        self.assertEqual(Decimal(str(tot["lebih_bayar_pph21"])), max(kembali - dipotong, Decimal(0)))
        teks = out["teks"]
        self.assertIn("PPh 21 dipotong bulan ini: %s" % G.rp(dipotong), teks)
        self.assertIn("Kelebihan PPh 21 dikembalikan ke karyawan", teks)
        self.assertIn("Perkiraan setor PPh 21: %s" % G.rp(max(dipotong - kembali, Decimal(0))), teks)
        self.assertIn("konsultan", teks)
        self.assertIn("Coretax", teks)
        if kembali > dipotong:
            self.assertIn("Lebih bayar PPh 21", teks)
        # rekap tahun & pengingat memakai perkiraan setor yang sama
        self.ok("final", "--bulan", "2026-12", "--ya")
        rk = self.ok("rekap", "--bulan", "2026-12")["total"]
        self.assertEqual(Decimal(str(rk["setor_pph21"])), max(dipotong - kembali, Decimal(0)))
        self.assertIn("Perkiraan setor PPh 21", self.ok("rekap", "--tahun", "2026")["teks"])

    def test_setor_pph21_tanpa_kelebihan_tetap_satu_baris(self):
        self.tambah("Andi", "--ptkp", "K/1", "--gaji-pokok", "9jt", "--masuk", "2022-01-01")
        _, out = self.hasil("2026-09")
        self.assertEqual(out["total"]["setor_pph21"], out["total"]["pph21_dipotong"])
        self.assertIn("- Setor PPh 21: ", out["teks"])
        self.assertNotIn("Perkiraan setor", out["teks"])

    def test_total_lama_v100_dilengkapi(self):
        t = G.lengkapi_total({"setor_pph21": Decimal(4018864), "pengembalian_pph21": Decimal(931100)})
        self.assertEqual(t["pph21_dipotong"], Decimal(4018864))
        self.assertEqual(t["setor_pph21"], Decimal(3087764))           # angka neto temuan penguji (September)
        t = G.lengkapi_total({"setor_pph21": Decimal(100), "pengembalian_pph21": Decimal(250)})
        self.assertEqual((t["setor_pph21"], t["lebih_bayar_pph21"]), (Decimal(0), Decimal(150)))

    def test_total_lama_v1010_dtp_diubah_ke_arti_baru(self):
        # total tersimpan <= 1.0.10: pph21_dipotong berisi jumlah DISETOR (tanpa DTP)
        t = G.lengkapi_total({"pph21_dipotong": Decimal(300000), "pph21_dtp_tunai": Decimal(45000),
                              "setor_pph21": Decimal(300000), "pengembalian_pph21": Decimal(0)})
        self.assertEqual((t["pph21_dipotong"], t["pph21_dtp"], t["pph21_disetor_ke_negara"], t["setor_pph21"]),
                         (Decimal(345000), Decimal(45000), Decimal(300000), Decimal(300000)))
        # idempoten: dipanggil ulang pada total baru tidak menambah DTP lagi
        self.assertEqual(G.lengkapi_total(t)["pph21_dipotong"], Decimal(345000))

    def test_pengingat_jp_tidak_digeser_jht_digeser(self):
        self.tambah("Andi", "--ptkp", "K/1", "--gaji-pokok", "6jt", "--masuk", "2022-01-01")
        self.ok("hitung", "--bulan", "2026-10")
        self.ok("final", "--bulan", "2026-10", "--ya")
        teks = self.ok("pengingat", "--rentang", "14", hari_ini="2026-11-08")["teks"]   # 15/11/2026 = Minggu
        self.assertIn("Min 15/11/2026: Batas setor iuran JP (Jaminan Pensiun) masa Oktober 2026", teks)
        self.assertIn("PP 45/2015 Pasal 30 ayat (3)", teks)
        self.assertIn("Sen 16/11/2026: Batas setor iuran JHT, JKK, JKM masa Oktober 2026", teks)
        self.assertIn("PP 46/2015 Pasal 19", teks)
        self.assertNotIn("Sen 16/11/2026: Batas setor iuran JP", teks)
        # tanggal 15 hari kerja -> satu baris gabungan
        self.ok("hitung", "--bulan", "2026-09")
        teks = self.ok("pengingat", "--rentang", "20", hari_ini="2026-10-01")["teks"]   # 15/10/2026 = Kamis
        self.assertIn("Kam 15/10/2026: Batas setor iuran BPJS Ketenagakerjaan masa September 2026 (JHT, JKK, JKM, JP",
                      teks)

    def test_peringatan_umk_prorata_dibedakan(self):
        self.ok("atur", "--umk", "5.396.761")
        k = self.tambah("Kiki", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2026-09-15")["kode"]
        self.ok("isi", "--bulan", "2026-09", "--karyawan", k, "--gaji-pokok-dibayar", "3,2jt")
        _, out = self.hasil("2026-09")
        umk = [p for p in out["peringatan_hitung"] if "di bawah UMK" in p]
        self.assertTrue(umk)
        self.assertTrue(all("prorata" in p for p in umk))


# --------------------------------------------------------------------------- v1.0.2: temuan uji ulang v1.0.1 (Akun B)
class UjiV102(Dasar):
    def test_isi_gaji_pokok_dibayar_bulan_penuh_dipagari(self):
        e = self.tambah("Eka", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2022-01-01")["kode"]
        _, out = self.hasil("2026-09")
        iuran_penuh = out["karyawan"][0]["payroll"]["iuran"]
        arg = ["isi", "--bulan", "2026-09", "--karyawan", e, "--gaji-pokok-dibayar", "5jt", "--bonus", "10jt"]
        # tanpa persetujuan khusus: ditolak (isi menyimpan langsung, jadi tanpa flag selalu ditolak), DB tidak berubah
        for tambahan in ([], ["--ya"]):
            out = self.gagal(*(arg + tambahan))
            self.assertEqual(out["masalah_kepatuhan"], ["dasar_bpjs_turun_bulan_penuh"])
            self.assertIn("--ya-saya-paham", out["error"])
            self.assertIn("sebulan penuh", out["error"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM isian"), 0)
        # dengan persetujuan khusus: tersimpan + tercatat di log
        out = self.ok(*(arg + ["--ya-saya-paham", "--alasan-khusus", "cuti di luar tanggungan 20 hari sesuai PK"]))
        self.assertEqual(out["konfirmasi_kepatuhan"]["masalah"], ["dasar_bpjs_turun_bulan_penuh"])
        c = sqlite3.connect(self.db)
        log = c.execute("SELECT ringkasan FROM log WHERE perintah='isi' ORDER BY id DESC").fetchone()[0]
        c.close()
        self.assertIn("konfirmasi_kepatuhan", log)
        self.assertIn("cuti di luar tanggungan", log)
        # hitung memakai dasar 5 jt dan tetap mengingatkan; iuran diverifikasi Decimal (dibulatkan ke rupiah)
        _, out = self.hasil("2026-09")
        self.assertTrue(any("Eka: gaji pokok + tunjangan tetap" in p and "sebulan penuh" in p
                            for p in out["peringatan_hitung"]))
        iuran = out["karyawan"][0]["payroll"]["iuran"]
        dasar, dasar_penuh = Decimal(5000000), Decimal(15000000)
        r = lambda x: x.quantize(Decimal(1))                                   # noqa: E731
        self.assertEqual(Decimal(iuran["kes_perusahaan"]), r(dasar * Decimal("0.04")))           # 200.000
        self.assertEqual(Decimal(iuran["jht_perusahaan"]), r(dasar * Decimal("0.037")))          # 185.000
        self.assertEqual(Decimal(iuran["jkk"]), r(dasar * Decimal("0.0024")))                    # 12.000
        self.assertEqual(Decimal(iuran["jkm"]), r(dasar * Decimal("0.003")))                     # 15.000
        self.assertEqual(Decimal(iuran_penuh["kes_perusahaan"]), r(min(dasar_penuh, Decimal(12000000)) *
                                                                   Decimal("0.04")))              # 480.000
        self.assertEqual(Decimal(iuran_penuh["jht_perusahaan"]), r(dasar_penuh * Decimal("0.037")))  # 555.000

    def test_isi_tanpa_penurunan_atau_bulan_masuk_tidak_dipagari(self):
        e = self.tambah("Eka", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2022-01-01")["kode"]
        self.ok("isi", "--bulan", "2026-09", "--karyawan", e, "--bonus", "1jt")               # bukan gaji pokok
        out = self.ok("isi", "--bulan", "2026-09", "--karyawan", e, "--gaji-pokok-dibayar", "15jt")  # tidak turun
        self.assertFalse(out["perlu_persetujuan_khusus"])
        k = self.tambah("Kiki", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2026-09-15")["kode"]
        out = self.ok("isi", "--bulan", "2026-09", "--karyawan", k, "--gaji-pokok-dibayar", "3,2jt")  # prorata masuk
        self.assertFalse(out["perlu_persetujuan_khusus"])
        l = self.tambah("Lina", "--ptkp", "TK/0", "--gaji-pokok", "8jt", "--masuk", "2020-01-01")["kode"]
        self.ok("karyawan", "keluar", "--karyawan", l, "--tanggal", "2026-09-14", "--ya")
        out = self.ok("isi", "--bulan", "2026-09", "--karyawan", l, "--gaji-pokok-dibayar", "3,7jt")  # prorata keluar
        self.assertFalse(out["perlu_persetujuan_khusus"])

    def test_isi_file_gaji_pokok_turun_dipagari(self):
        self.tambah("Eka", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2022-01-01")
        f = self.file("komp.csv", "nama;gaji_pokok;bonus\nEka;5000000;10000000\n")
        out = self.ok("isi", "--bulan", "2026-09", "--file", f)                           # pratinjau
        self.assertTrue(out["perlu_persetujuan_khusus"])
        self.assertIn("--ya-saya-paham", out["langkah_berikut"][0])                    # instruksi khusus agent
        self.assertNotIn("--ya", out["teks"])                                           # teks pemilik polos
        self.assertIn("perlu persetujuan khusus pemilik", out["teks"])
        out = self.gagal("isi", "--bulan", "2026-09", "--file", f, "--ya")
        self.assertEqual(out["masalah_kepatuhan"], ["dasar_bpjs_turun_bulan_penuh:K001"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM isian"), 0)
        self.ok("isi", "--bulan", "2026-09", "--file", f, "--ya", "--ya-saya-paham", "--alasan-khusus", "uji")
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM isian"), 2)

    def test_teks_pratinjau_persetujuan_khusus_menyebut_flag(self):
        e = self.tambah("Eka", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2022-01-01")["kode"]
        out = self.ok("karyawan", "ubah", "--karyawan", e, "--bpjs", "tidak")
        self.assertTrue(out["perlu_persetujuan_khusus"])
        penutup = out["teks"].rsplit("\n\n", 1)[-1]
        self.assertIn("perlu persetujuan khusus pemilik", penutup)
        self.assertNotIn("--ya", out["teks"])                                           # v1.0.13: teks pemilik polos
        self.assertIn("--ya --ya-saya-paham", out["langkah_berikut"][0])                # flag hanya untuk agent
        # pratinjau biasa: teks pemilik "balas simpan", perintah simpan di langkah_berikut
        out = self.ok("karyawan", "ubah", "--karyawan", e, "--jabatan", "Kasir")
        self.assertTrue(out["teks"].endswith('Sudah benar? Balas "simpan" untuk menyimpan.'))
        self.assertNotIn("Jalankan perintah", out["teks"])
        self.assertEqual(out["langkah_berikut"][0], G.LANGKAH_SIMPAN)



# --------------------------------------------------------------------------- v1.0.13: temuan bot Telegram gelombang 21
G21_CSV = (
    "kode;nama;jabatan;jenis;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;bpjs;jkk;hari_kerja;masuk;bank;"
    "rekening\n"
    "K01;Andi Fiktif;Kepala Gudang;tetap;K/1;6.500.000;750.000;400.000;kes,tk,jp;0,54;6;2019-03-01;BCA;0000000001\n"
    "K02;Budi Fiktif;Sopir;tetap;K/2;5.400.000;300.000;500.000;kes,tk,jp;0,54;6;2020-06-15;BRI;0000000002\n"
    "K03;Citra Fiktif;Kasir;tetap;TK/0;5.400.000;;300.000;kes,tk,jp;0,54;6;2021-01-10;BCA;0000000003\n"
    "K04;Dewi Fiktif;Admin;tetap;TK/0;5.600.000;250.000;;kes,tk,jp;0,54;6;2021-09-01;Mandiri;0000000004\n"
    "K05;Eko Fiktif;Staf Gudang;kontrak;K/0;5.400.000;;350.000;kes,tk;0,54;6;2024-02-01;BRI;0000000005\n"
    "K06;Fajar Fiktif;Staf Gudang;kontrak;TK/0;5.400.000;;350.000;kes,tk;0,54;6;2024-02-01;BRI;0000000006\n"
    "K07;Gita Fiktif;Marketing;tetap;TK/0;6.000.000;500.000;;kes,tk,jp;0,54;6;2022-04-18;BCA;0000000007\n"
    "K08;Hadi Fiktif;Teknisi;tetap;K/3;7.000.000;600.000;;kes,tk,jp;0,54;6;2018-11-05;Mandiri;0000000008\n"
    "K09;Indah Fiktif;Staf Produksi;tetap;TK/0;5.400.000;;300.000;kes,tk,jp;0,54;6;2023-03-13;BCA;0000000009\n"
    "K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;kes,tk;0,54;6;2025-01-06;BRI;0000000010\n"
    "K11;Kiki Fiktif;Staf Produksi;kontrak;TK/0;5.400.000;;;kes,tk;0,54;6;2026-09-15;BCA;0000000011\n"
    "K12;Lina Fiktif;Supervisor;tetap;K/0;10.000.000;1.000.000;;kes,tk,jp;0,54;6;2017-08-01;Mandiri;0000000012\n")
UMK_G21 = Decimal(5396761)
# saldo awal Lina Jan-Agu (fiktif, konsisten dengan 8 bulan gaji penuh: bruto pajak 11.532.400/bulan, TER A 3,5%;
# iuran JHT 2% 8 x 220.000 + JP 1% dengan batas upah JP 10.547.400 (Jan-Feb) / 11.086.300 (Mar-Agu) = 2.630.948)
SALDO_LINA = ("92.259.200", "3.229.072", "2.630.948")


def _r(x):
    return Decimal(x).quantize(Decimal(1), rounding="ROUND_HALF_UP")


def bpjs_independen(baris):
    """Hitung ulang setoran BPJS tanpa mesin (Decimal, per komponen dibulatkan ke rupiah terdekat).
    baris: [(gaji_pokok, tunjangan_tetap, ikut_jp)]"""
    kes = tk = Decimal(0)
    for gp, tt, jp in baris:
        upah = Decimal(gp) + Decimal(tt)
        dk = min(max(upah, UMK_G21), Decimal(12000000))
        kes += _r(dk * 4 / 100) + _r(dk * 1 / 100)
        tk += _r(upah * Decimal("3.7") / 100) + _r(upah * 2 / 100) + _r(upah * Decimal("0.54") / 100) + \
            _r(upah * Decimal("0.3") / 100)
        if jp:
            dj = min(upah, Decimal(11086300))
            tk += _r(dj * 2 / 100) + _r(dj * 1 / 100)
    return kes, tk


class UjiV1013(Dasar):
    """Satu karyawan yang datanya kurang tidak boleh menahan karyawan lain (gelombang 21, 16-10-2026)."""

    def siapkan_g21(self):
        self.ok("atur", "--umk", "5.396.761", "--jkk", "0,54", "--tanggal-gajian", "25")
        self.ok("karyawan", "impor", self.file("g21.csv", G21_CSV), "--ya")
        self.ok("karyawan", "keluar", "--karyawan", "Lina", "--tanggal", "2026-09-14", "--ya")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "Andi", "--bonus", "500rb", "--kasbon", "250rb")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "Indah", "--lembur-hari-kerja", "2+3")

    def asli_11(self):
        """payroll.py ASLI (slip-gaji-bpjs) untuk 11 karyawan lengkap; baris disusun tes ini sendiri."""
        kol = "nama;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;bonus;potongan_lain;lembur_hari_kerja;ikut_jp"
        data = [("Andi Fiktif", "K/1", 6500000, 750000, 400000, 500000, 250000, "", "ya"),
                ("Budi Fiktif", "K/2", 5400000, 300000, 500000, "", "", "", "ya"),
                ("Citra Fiktif", "TK/0", 5400000, 0, 300000, "", "", "", "ya"),
                ("Dewi Fiktif", "TK/0", 5600000, 250000, 0, "", "", "", "ya"),
                ("Eko Fiktif", "K/0", 5400000, 0, 350000, "", "", "", "tidak"),
                ("Fajar Fiktif", "TK/0", 5400000, 0, 350000, "", "", "", "tidak"),
                ("Gita Fiktif", "TK/0", 6000000, 500000, 0, "", "", "", "ya"),
                ("Hadi Fiktif", "K/3", 7000000, 600000, 0, "", "", "", "ya"),
                ("Indah Fiktif", "TK/0", 5400000, 0, 300000, "", "", "2+3", "ya"),
                ("Joko Fiktif", "K/1", 5400000, 0, 300000, "", "", "", "tidak"),
                ("Kiki Fiktif", "TK/0", 5400000, 0, 0, "", "", "", "tidak")]
        f = self.file("asli11.csv", kol + "\n" + "".join(";".join(str(x) for x in r) + "\n" for r in data))
        out = jalankan_asli("payroll.py", ["--data", f, "--periode", "2026-09", "--hari-kerja", "6", "--umk",
                                           "5396761", "--jkk", "0.54", "--format", "json", "--out",
                                           os.path.join(self.dir, "o11")])
        return {k["nama"]: k for k in out["karyawan"]}, [(r[2], r[3], r[8] == "ya") for r in data]

    def cocokkan(self, hasil, asli):
        for kd, h in hasil.items():
            a = asli[h["nama"]]
            for kol in ("take_home_pay", "pph", "biaya_perusahaan", "total_pendapatan", "total_potongan"):
                self.assertEqual(Decimal(str(h["payroll"][kol])), Decimal(str(a[kol])), (h["nama"], kol))
            for kol, v in a["iuran"].items():
                self.assertEqual(Decimal(str(h["payroll"]["iuran"][kol])), Decimal(str(v)), (h["nama"], kol))

    def teks_bersih(self, teks):
        self.assertNotIn("gaji.py", teks)
        self.assertNotRegex(teks, r"--[a-z]")
        self.assertNotIn("script", teks)
        self.assertNotRegex(teks, r"\b[a-z]+_[a-z]+\b")                       # nama kolom teknis

    def test_g21_satu_tertunda_tidak_menahan_yang_lain(self):
        self.siapkan_g21()
        h, out = self.hasil("2026-09")
        # 11 karyawan lengkap dihitung, Lina (keluar, tanpa data Jan-Agu) tertunda - tidak menahan yang lain
        self.assertEqual(len(h), 11)
        self.assertNotIn("K12", h)
        self.assertEqual([t["kode"] for t in out["tertunda"]], ["K12"])
        self.assertTrue(out["tertunda"][0]["bisa_pph_sementara"])
        self.assertFalse(out["bisa_final"])
        asli, baris = self.asli_11()
        self.cocokkan(h, asli)
        kes, tk = bpjs_independen(baris)
        t = out["total"]
        self.assertEqual((Decimal(str(t["setor_bpjs_kesehatan"])), Decimal(str(t["setor_bpjs_ketenagakerjaan"]))),
                         (kes, tk))
        self.assertEqual((kes, tk), (Decimal(3265000), Decimal(5581620)))   # acuan penilai G21 dikurangi Lina
        self.assertEqual(Decimal(str(t["setor_pph21"])), sum(Decimal(str(a["pph"])) for a in asli.values()))
        self.assertEqual(Decimal(str(h["K09"]["payroll"]["pendapatan"]["Lembur"])),
                         _r(Decimal(5400000) / 173 * 9))                        # 280.925
        teks = out["teks"]
        for frasa in ("11 karyawan dihitung, 1 tertunda", "BELUM termasuk yang tertunda: Lina Fiktif",
                      "TERTUNDA - belum dihitung", "Januari–Agustus 2026", "(a) kirim angka itu", "(b) hitung",
                      "1721-A1", "belum bisa dikunci"):
            self.assertIn(frasa, teks)
        self.teks_bersih(teks)
        self.assertTrue(any("Kiki Fiktif masuk 15/09/2026" in p and "PENUH" in p and "Rp 2.880.000" in p
                            for p in out["peringatan_hitung"]))
        self.assertTrue(any("--pph-sementara" in x for x in out["langkah_berikut"]))
        # tidak bisa dikunci selama ada yang tertunda; slip draf 11 orang tetap bisa
        g = self.gagal("final", "--bulan", "2026-09", "--ya")
        self.assertIn("belum bisa dikunci", g["error"])
        self.assertEqual(g["tertunda"], ["K12"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM periode WHERE status='final'"), 0)
        self.assertEqual(len(self.ok("slip", "--bulan", "2026-09", "--keluar", self.dir)["file"]), 11)
        self.assertIn("tertunda", self.gagal("slip", "--bulan", "2026-09", "--karyawan", "Lina")["error"])
        self.assertIn("1 tertunda", self.ok("periode")["teks"])
        # pilihan (a): data Jan-Agu dikirim -> Lina dihitung ulang setahun, periode bisa dikunci
        self.ok("saldo-awal", "--karyawan", "Lina", "--tahun", "2026", "--sampai-bulan", "8", "--bruto",
                SALDO_LINA[0], "--pph21", SALDO_LINA[1], "--iuran", SALDO_LINA[2])
        h, out = self.hasil("2026-09")
        self.assertEqual(len(h), 12)
        self.assertEqual(out["tertunda"], [])
        self.assertTrue(out["bisa_final"])
        lina = h["K12"]
        self.assertTrue(lina["payroll"]["pph_info"]["masa_terakhir"])
        f = self.file("lina.csv", "nama;ptkp;gaji_pokok;tunjangan_tetap;jkk_persen;berhenti;bruto_sd_bulan_lalu;"
                      "pph21_sd_bulan_lalu;iuran_sd_bulan_lalu;bulan_mulai\n"
                      "Lina Fiktif;K/0;10000000;1000000;0.54;ya;92259200;3229072;2630948;1\n")
        a = jalankan_asli("payroll.py", ["--data", f, "--periode", "2026-09", "--hari-kerja", "6", "--umk", "5396761",
                                         "--format", "json", "--out", os.path.join(self.dir, "ol")])["karyawan"][0]
        self.assertEqual(lina["payroll"]["pph"], a["pph"])
        self.assertEqual(Decimal(str(a["pph"])), Decimal(-1337572))             # hitung manual Pasal 17 (contoh 08)
        self.assertEqual(lina["payroll"]["take_home_pay"], a["take_home_pay"])
        t = out["total"]
        self.assertEqual((Decimal(str(t["setor_bpjs_kesehatan"])), Decimal(str(t["setor_bpjs_ketenagakerjaan"]))),
                         (Decimal(3815000), Decimal(6631020)))                  # acuan penilai G21 (12 orang)
        self.ok("final", "--bulan", "2026-09", "--ya")

    def test_pph_sementara_pilihan_b(self):
        self.siapkan_g21()
        h, out = self.hasil_opsi("2026-09", "--pph-sementara")
        self.assertEqual(len(h), 12)
        self.assertEqual(out["tertunda"], [])
        self.assertEqual(out["pph_sementara"], ["K12"])
        lina = h["K12"]
        self.assertTrue(lina["pph_sementara"])
        self.assertIsNone(lina["masa_terakhir"])
        self.assertFalse(lina["payroll"]["pph_info"]["masa_terakhir"])
        f = self.file("lina-ter.csv", "nama;ptkp;gaji_pokok;tunjangan_tetap;jkk_persen\n"
                      "Lina Fiktif;K/0;10000000;1000000;0.54\n")
        a = jalankan_asli("payroll.py", ["--data", f, "--periode", "2026-09", "--hari-kerja", "6", "--umk", "5396761",
                                         "--format", "json", "--out", os.path.join(self.dir, "olt")])["karyawan"][0]
        self.assertEqual(lina["payroll"]["pph"], a["pph"])                       # TER bulanan (403.634)
        self.assertEqual(Decimal(str(a["pph"])), Decimal(403634))
        asli, _ = self.asli_11()
        self.assertEqual(Decimal(str(out["total"]["setor_pph21"])),
                         sum(Decimal(str(x["pph"])) for x in asli.values()) + Decimal(403634))
        for frasa in ("403.634 (sementara)", "BELUM FINAL", "1721-A1", "SEMENTARA untuk Lina Fiktif"):
            self.assertIn(frasa, out["teks"])
        self.teks_bersih(out["teks"])
        self.assertIn("PPh 21 masih SEMENTARA", self.gagal("final", "--bulan", "2026-09", "--ya")["error"])
        slip = self.ok("slip", "--bulan", "2026-09", "--karyawan", "Lina", "--keluar", self.dir)["teks"]
        self.assertIn("PPh 21 SEMENTARA", slip)
        # tanpa flag kembali tertunda (angka sementara tidak menempel)
        h, out = self.hasil("2026-09")
        self.assertEqual([t["kode"] for t in out["tertunda"]], ["K12"])

    def hasil_opsi(self, bulan, *opsi):
        out = self.ok("hitung", "--bulan", bulan, *opsi)
        return {k["kode"]: k for k in out["karyawan"]}, out

    def test_desember_tanpa_data_tidak_bisa_sementara(self):
        a = self.tambah("Ani", "--ptkp", "TK/0", "--gaji-pokok", "8jt", "--masuk", "2020-01-01")["kode"]
        b = self.tambah("Bayu", "--ptkp", "K/1", "--gaji-pokok", "9jt", "--masuk", "2020-01-01")["kode"]
        self.ok("saldo-awal", "--karyawan", a, "--tahun", "2026", "--sampai-bulan", "11", "--bruto", "90jt",
                "--pph21", "1jt", "--iuran", "2.640.000")
        h, out = self.hasil_opsi("2026-12", "--pph-sementara")
        self.assertEqual(list(h), [a])
        self.assertEqual([t["kode"] for t in out["tertunda"]], [b])
        self.assertFalse(out["tertunda"][0]["bisa_pph_sementara"])
        self.assertEqual(out["pph_sementara"], [])
        self.assertTrue(out["tertunda"][0]["sementara_diabaikan"])
        self.assertIn("Pilihan angka sementara tidak berlaku untuk Desember", out["teks"])

    def test_baris_ditolak_mesin_tidak_menahan_lain(self):
        self.tambah("Ani", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2020-01-01")
        b = self.tambah("Bayu", "--ptkp", "K/1", "--gaji-pokok", "7jt", "--masuk", "2020-01-01")["kode"]
        self.tambah("Cici", "--ptkp", "K/0", "--gaji-pokok", "5jt", "--masuk", "2020-01-01")
        # 13 jam lembur hari libur (pola 5 hari, maks. 12 jam PP 35/2021) lolos isian tetapi ditolak mesin
        self.ok("isi", "--bulan", "2026-09", "--karyawan", b, "--lembur-hari-libur", "13")
        h, out = self.hasil("2026-09")
        self.assertEqual(len(h), 2)
        self.assertEqual([t["kode"] for t in out["tertunda"]], [b])
        self.assertIn("data perlu diperbaiki", out["tertunda"][0]["teks"])
        self.assertIn("melebihi", out["tertunda"][0]["teks"])
        self.assertNotIn("Bayu: Bayu", out["tertunda"][0]["teks"])
        self.assertIn("data perlu diperbaiki", self.gagal("final", "--bulan", "2026-09", "--ya")["error"])
        self.ok("isi", "--bulan", "2026-09", "--karyawan", b, "--lembur-hari-libur", "8")
        h, out = self.hasil("2026-09")
        self.assertEqual((len(h), out["tertunda"]), (3, []))
        # galat umum mesin (batas upah JP periode belum tercatat) tetap satu pesan, bukan 'tertunda' per orang
        out = self.gagal("hitung", "--bulan", "2027-04")
        self.assertIn("Batas upah Jaminan Pensiun", out["error"])
        self.assertNotIn("tertunda", out)

    def test_prorata_kalender_dan_kembali_penuh(self):
        k = self.tambah("Kiki", "--ptkp", "TK/0", "--gaji-pokok", "5,4jt", "--masuk", "2026-09-15")["kode"]
        l = self.tambah("Lina", "--ptkp", "K/0", "--gaji-pokok", "10jt", "--tunjangan-tetap", "1jt",
                        "--masuk", "2017-08-01")["kode"]
        m = self.tambah("Mira", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2026-09-10")["kode"]
        n = self.tambah("Nana", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2020-01-01")["kode"]
        self.ok("karyawan", "keluar", "--karyawan", l, "--tanggal", "2026-09-14", "--ya")
        self.ok("karyawan", "keluar", "--karyawan", n, "--tanggal", "2026-09-30", "--ya")   # hari terakhir = penuh
        self.ok("saldo-awal", "--karyawan", l, "--tahun", "2026", "--sampai-bulan", "8", "--bruto", SALDO_LINA[0],
                "--pph21", SALDO_LINA[1], "--iuran", SALDO_LINA[2])
        self.ok("saldo-awal", "--karyawan", n, "--tahun", "2026", "--sampai-bulan", "8", "--bruto", "50jt",
                "--pph21", "1jt", "--iuran", "1,44jt")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", m, "--gaji-pokok-dibayar", "4,2jt")   # nominal pemilik
        h, out = self.hasil_opsi("2026-09", "--prorata", "kalender")
        gp = lambda x: Decimal(str(h[x]["payroll"]["pendapatan"]["Gaji pokok"]))           # noqa: E731
        tt = lambda x: Decimal(str(h[x]["payroll"]["pendapatan"]["Tunjangan tetap"]))      # noqa: E731
        self.assertEqual(gp(k), _r(Decimal(5400000) * 16 / 30))       # 2.880.000 (15-30 Sep = 16 hari)
        self.assertEqual(gp(l), _r(Decimal(10000000) * 14 / 30))      # 4.666.667 (1-14 Sep = 14 hari)
        self.assertEqual(tt(l), _r(Decimal(1000000) * 14 / 30))       # 466.667
        self.assertEqual(gp(m), Decimal(4200000))                     # nominal pemilik tidak ditimpa
        self.assertEqual(gp(n), Decimal(6000000))                     # keluar hari terakhir bulan = penuh
        self.assertEqual(sorted(x["kode"] for x in out["prorata_diterapkan"]), sorted([k, l]))
        self.assertTrue(any("Kiki: gaji diprorata hari kalender" in p and "5.400.000 × 16 ÷ 30" in p
                            for p in out["peringatan_hitung"]))
        h, out = self.hasil_opsi("2026-09", "--prorata", "penuh")
        self.assertEqual((gp(k), gp(l), gp(m)), (Decimal(5400000), Decimal(10000000), Decimal(4200000)))
        self.assertEqual(sorted(x["kode"] for x in out["saran_prorata"]), sorted([k, l]))

    def test_hitung_cepat_tanpa_database(self):
        f = self.file("g21.csv", G21_CSV)
        dasar = ["hitung-cepat", "--data", f, "--bulan", "2026-09", "--umk", "Rp 5.396.761", "--jkk", "0,54",
                 "--isi", "Andi: bonus=500rb; kasbon=250rb", "--isi", "Indah: lembur-hari-kerja=2+3",
                 "--masuk", "Kiki=2026-09-15", "--keluar", "Lina=2026-09-14"]
        out = self.ok(*dasar)
        self.assertEqual((out["mode"], out["disimpan"]), ("pratinjau", False))
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM karyawan"), 0)      # database tidak disentuh
        h = {k["kode"]: k for k in out["karyawan"]}
        self.assertEqual(len(h), 11)
        self.assertEqual([t["kode"] for t in out["tertunda"]], ["K12"])
        asli, baris = self.asli_11()
        self.cocokkan(h, asli)
        t = out["total"]
        self.assertEqual((Decimal(str(t["setor_bpjs_kesehatan"])), Decimal(str(t["setor_bpjs_ketenagakerjaan"]))),
                         bpjs_independen(baris))
        self.assertIn("PRATINJAU (hitung cepat, belum disimpan)", out["teks"])
        self.assertIs(out["bisa_final"], False)
        self.assertIn("balas \"simpan\"", out["teks"])
        self.teks_bersih(out["teks"])
        # pilihan (a) langsung lewat --saldo-awal: 12 orang, Lina dihitung ulang setahun
        out = self.ok(*(dasar + ["--saldo-awal", "Lina: bruto=%s; pph21=%s; iuran=%s" % SALDO_LINA,
                                 "--folder-slip", os.path.join(self.dir, "slip")]))
        self.assertEqual((len(out["karyawan"]), out["tertunda"]), (12, []))
        lina = [k for k in out["karyawan"] if k["kode"] == "K12"][0]
        self.assertTrue(lina["payroll"]["pph_info"]["masa_terakhir"])
        self.assertEqual(len(out["file_slip"]), 12)
        with open(out["file_slip"][0], encoding="utf-8") as fh:
            self.assertIn("PRATINJAU", fh.read())
        # kolom masuk tidak ada -> asumsi disebut, tetap dihitung
        tanpa = self.file("tanpa-masuk.csv", "nama;ptkp;gaji_pokok\nAni Fiktif;TK/0;6jt\nBayu Fiktif;K/1;7jt\n")
        out = self.ok("hitung-cepat", "--data", tanpa, "--bulan", "2026-09", "--keluar", "Bayu=2026-08-31")
        self.assertEqual(len(out["karyawan"]), 1)
        self.assertTrue(any("di luar September 2026: Bayu Fiktif" in a for a in out["asumsi"]))
        self.assertTrue(any("semua karyawan (2)" in a and "tidak ada di data" in a for a in out["asumsi"]))
        self.assertTrue(any("UMK" in a for a in out["asumsi"]))
        # input rusak ditolak dengan pesan jelas
        self.assertIn("NAMA: kolom=nilai", self.gagal("hitung-cepat", "--data", f, "--bulan", "2026-09",
                                                      "--isi", "Andi bonus 500rb")["error"])
        g = self.gagal("hitung-cepat", "--data", f, "--bulan", "2026-09", "--isi", "Zaki: bonus=1jt")["error"]
        self.assertIn("tidak ada di daftar karyawan. Nama yang ada: Andi Fiktif, Budi Fiktif", g)
        self.assertNotIn("gaji.py", g)
        self.assertIn("tidak dikenal", self.gagal("hitung-cepat", "--data", f, "--bulan", "2026-09",
                                                  "--isi", "Andi: insentif=1jt")["error"])


class UjiV1013Pemeriksa(Dasar):
    """Temuan pemeriksa independen atas draf 1.0.13 (17-10-2026)."""

    def cepat(self, *opsi, data=G21_CSV, ok=True):
        f = self.file("g21c.csv", data)
        argv = ["hitung-cepat", "--data", f, "--bulan", "2026-09", "--umk", "5.396.761", "--jkk", "0,54"] + list(opsi)
        return self.ok(*argv) if ok else self.gagal(*argv)

    # 1. pagar dasar BPJS / kepesertaan BPJS juga berlaku di hitung-cepat
    def test_hitung_cepat_pagar_bpjs(self):
        out = self.cepat("--isi", "Andi: gaji-pokok-dibayar=3jt; bonus=4jt")
        h = {k["kode"]: k for k in out["karyawan"]}
        self.assertNotIn("K01", h)                                          # Andi tidak dihitung tanpa persetujuan
        self.assertEqual(len(h), 11)                                        # yang lain tetap dihitung
        self.assertEqual(out["masalah_kepatuhan"], ["K01:dasar_bpjs_turun_bulan_penuh"])
        self.assertTrue(out["perlu_persetujuan_khusus"])
        andi = [t for t in out["tertunda"] if t["kode"] == "K01"][0]
        self.assertIn("perlu persetujuan khusus pemilik", andi["teks"])
        self.assertIn("Rp 3.750.000", andi["teks"])
        self.assertNotIn("Disimpan dengan persetujuan", out["teks"])
        self.assertNotIn("tercatat di log", out["teks"])
        # dengan persetujuan khusus pemilik: dihitung, kalimatnya jujur (belum disimpan)
        out = self.cepat("--isi", "Andi: gaji-pokok-dibayar=3jt; bonus=4jt", "--ya-saya-paham", "--alasan-khusus",
                         "cuti di luar tanggungan sesuai PK")
        self.assertIn("K01", {k["kode"] for k in out["karyawan"]})
        self.assertFalse(out["perlu_persetujuan_khusus"])
        self.assertEqual(out["konfirmasi_kepatuhan"]["karyawan"], ["K01"])
        self.assertIn("Dipakai atas persetujuan khusus pemilik; belum disimpan", out["teks"])
        self.assertNotIn("Disimpan dengan persetujuan", out["teks"])
        # karyawan tanpa BPJS di file: ditunda tanpa persetujuan (sama dengan impor database)
        data = G21_CSV.replace("K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;kes,tk;",
                               "K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;tidak;")
        out = self.cepat(data=data)
        self.assertIn("K10", [t["kode"] for t in out["tertunda"]])
        self.assertEqual(out["masalah_kepatuhan"], ["K10:tanpa_bpjs_kesehatan", "K10:tanpa_bpjs_ketenagakerjaan"])
        out = self.cepat("--ya-saya-paham", data=data)
        self.assertIn("K10", {k["kode"] for k in out["karyawan"]})
        self.assertIn("Tidak didaftarkan BPJS: Joko Fiktif (Kesehatan & Ketenagakerjaan)", out["teks"])

    def test_kalimat_persetujuan_database_jujur(self):
        e = self.tambah("Eka", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2022-01-01")["kode"]
        self.ok("isi", "--bulan", "2026-09", "--karyawan", e, "--gaji-pokok-dibayar", "5jt", "--ya-saya-paham",
                "--alasan-khusus", "cuti di luar tanggungan sesuai PK")
        _, out = self.hasil("2026-09")
        self.assertTrue(any("Disimpan dengan persetujuan khusus pemilik, tercatat di log" in p
                            for p in out["peringatan_hitung"]))
        # isian lama tanpa catatan persetujuan (mis. disimpan versi lama tanpa pagar) -> tidak diklaim disetujui
        f = self.tambah("Fani", "--ptkp", "TK/0", "--gaji-pokok", "15jt", "--masuk", "2022-01-01")
        c = sqlite3.connect(self.db)
        pid = c.execute("SELECT id FROM periode WHERE kode='2026-09'").fetchone()[0]
        c.execute("INSERT INTO isian VALUES (?,?,?,?,?)", (pid, c.execute("SELECT id FROM karyawan WHERE kode=?",
                                                                           (f["kode"],)).fetchone()[0],
                                                          "gaji_pokok", "5000000", ""))
        c.commit()
        c.close()
        _, out = self.hasil("2026-09")
        fani = [p for p in out["peringatan_hitung"] if p.startswith("Fani:") and "sebulan penuh" in p]
        self.assertTrue(fani and "Tidak ada catatan persetujuan khusus" in fani[0], fani)

    # 2. bulan terlewat setelah aplikasi dipakai: sarankan hitung & kunci bulan itu, bukan jumlah manual
    def test_bulan_terlewat_disarankan_hitung_dan_kunci(self):
        e = self.tambah("Eko", "--ptkp", "K/1", "--gaji-pokok", "12jt", "--masuk", "2020-01-01")["kode"]
        s_ = self.tambah("Sri", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2021-01-01")["kode"]
        self.ok("saldo-awal", "--karyawan", e, "--tahun", "2026", "--sampai-bulan", "8", "--bruto", "100jt",
                "--pph21", "2jt", "--iuran", "2,9jt")
        self.ok("saldo-awal", "--karyawan", s_, "--tahun", "2026", "--sampai-bulan", "8", "--bruto", "50jt",
                "--pph21", "0", "--iuran", "1,4jt")
        for b in ("2026-09", "2026-10"):
            self.ok("hitung", "--bulan", b)
            self.ok("final", "--bulan", b, "--ya")
        out = self.gagal("hitung", "--bulan", "2026-12")                   # November terlewat
        self.assertIn("Gaji November 2026 belum dihitung & dikunci di aplikasi ini", out["error"])
        self.assertNotIn("total Januari–November", out["error"])
        self.assertIn("(2 karyawan, Desember)", out["error"])                # digabung, bukan 2 paragraf
        langkah = out["tertunda"][0]["langkah_agent"]
        self.assertIn("hitung --bulan 2026-11", langkah)
        self.assertIn("final --bulan 2026-11 (pratinjau, lalu --ya)", langkah)
        self.assertFalse(any(x.startswith("saldo-awal") for x in langkah))
        self.ok("hitung", "--bulan", "2026-11")
        self.ok("final", "--bulan", "2026-11", "--ya")
        h, out = self.hasil("2026-12")
        self.assertEqual((len(h), out["tertunda"]), (2, []))

    def test_bulan_sebelum_aplikasi_tetap_minta_total(self):
        self.tambah("Eko", "--ptkp", "K/1", "--gaji-pokok", "12jt", "--masuk", "2020-01-01")
        self.ok("hitung", "--bulan", "2026-10")
        self.ok("final", "--bulan", "2026-10", "--ya")
        self.ok("karyawan", "keluar", "--karyawan", "Eko", "--tanggal", "2026-11-14", "--ya")
        out = self.gagal("hitung", "--bulan", "2026-11")["tertunda"][0]     # Jan-Sep sebelum aplikasi dipakai
        self.assertEqual(out["rentang_data"], "Januari–September 2026")
        self.assertIn("Butuh total Januari–September 2026", out["teks"])
        self.assertIn("saldo-awal --karyawan K001 --tahun 2026 --sampai-bulan 9 --bruto <1> --pph21 <2> --iuran <3>",
                      out["langkah_agent"])

    # 3a. peringatan teknis mesin (JKK neto PP 6/2025) satu kalimat awam; disclaimer tanpa 'script', sebut PP 6/2025
    def test_peringatan_jkk_neto_digabung_dan_awam(self):
        minimal = ("nama;ptkp;gaji_pokok;tunjangan_tetap\n" + "".join(
            "Orang%02d Fiktif;TK/0;%d;\n" % (i, 5400000 + i * 100000) for i in range(1, 13)))
        out = self.ok("hitung-cepat", "--data", self.file("min.csv", minimal), "--bulan", "2026-09", "--umk",
                      "5.396.761", "--jkk", "0,40")
        teks = out["teks"]
        self.assertEqual(teks.count("tarif JKK 0,4%"), 1)
        self.assertIn("Semua karyawan (12): tarif JKK 0,4%", teks)
        self.assertEqual(sum("tarif JKK 0,4%" in p for p in out["peringatan_hitung"]), 12)   # JSON tetap rinci
        for kata in ("jkk_persen", "--jkk", "script"):
            self.assertNotIn(kata, teks)
        self.assertLessEqual(len(teks), 3800)
        self.assertIn("PP 6/2025", G.DISCLAIMER)
        self.assertNotIn("script", G.DISCLAIMER)

    # 5. panjang teks varian realistis 12 orang <= 3.800 karakter (muat satu pesan Telegram 4.096)
    def test_panjang_teks_varian_realistis(self):
        dasar = ["--isi", "Andi: bonus=500rb; kasbon=250rb", "--isi", "Indah: lembur-hari-kerja=2+3",
                 "--masuk", "Kiki=2026-09-15", "--keluar", "Lina=2026-09-14"]
        saldo = ["--saldo-awal", "Lina: bruto=%s; pph21=%s; iuran=%s" % SALDO_LINA]
        varian = {"default": [], "saldo": saldo, "prorata": ["--prorata", "kalender"],
                  "sementara": ["--pph-sementara"], "sementara+prorata": ["--pph-sementara", "--prorata", "kalender"],
                  "saldo+prorata": saldo + ["--prorata", "kalender"],
                  "pagar": ["--isi", "Andi: gaji-pokok-dibayar=3jt; bonus=4jt"]}
        for nama, opsi in varian.items():
            out = self.cepat(*(dasar + opsi))
            self.assertLessEqual(len(out["teks"]), 3800, (nama, len(out["teks"])))
            self.teks_bersih(out["teks"])
        out = self.cepat(*dasar)
        t = out["total"]
        self.assertEqual([t[k] for k in ("take_home_pay", "setor_bpjs_kesehatan", "setor_bpjs_ketenagakerjaan",
                                         "setor_pph21")], [65412866, 3265000, 5581620, 522059])
        # alur database ala examples/01 (12 orang, tanpa BPJS, di bawah UMK, prorata, Masa Pajak Terakhir)
        self.ok("atur", "--umk", "5.396.761", "--jkk", "0,54")
        self.ok("karyawan", "impor", self.file("ex01.csv", EX01_CSV), "--ya", "--ya-saya-paham", "--alasan-khusus",
                "uji fiktif")
        for a in (["K01", "--bonus", "500rb", "--kasbon", "250rb"], ["K09", "--lembur-hari-kerja", "2+3"],
                  ["K11", "--gaji-pokok-dibayar", "4.266.667"]):
            self.ok("isi", "--bulan", "2026-09", "--karyawan", *a)
        self.ok("karyawan", "keluar", "--karyawan", "K12", "--tanggal", "2026-09-14", "--ya")
        self.ok("isi", "--bulan", "2026-09", "--karyawan", "K12", "--gaji-pokok-dibayar", "4.666.667")
        for _ in range(2):
            out = self.ok("hitung", "--bulan", "2026-09")
            self.assertLessEqual(len(out["teks"]), 3800, len(out["teks"]))
            self.teks_bersih(out["teks"])
            self.ok("saldo-awal", "--karyawan", "K12", "--tahun", "2026", "--sampai-bulan", "8", "--bruto",
                    "83.872.000", "--pph21", "2.096.800", "--iuran", "2.400.000")
        self.assertEqual(out["tertunda"], [])

    teks_bersih = UjiV1013.teks_bersih

    # 6. nominal gaji terakhir sudah diisi -> jangan tanya penuh/prorata lagi
    def test_tertunda_tidak_tanya_prorata_bila_sudah_diisi(self):
        out = self.cepat("--keluar", "Lina=2026-09-14")
        lina = [t for t in out["tertunda"] if t["kode"] == "K12"][0]
        self.assertIn("penuh atau prorata", lina["teks"])
        out = self.cepat("--keluar", "Lina=2026-09-14", "--isi", "Lina: gaji-pokok-dibayar=4.666.667")
        lina = [t for t in out["tertunda"] if t["kode"] == "K12"][0]
        self.assertNotIn("penuh atau prorata", lina["teks"])
        self.assertNotIn("penuh atau prorata", out["teks"])

    def test_desember_satu_catatan_dan_nama_ganda(self):
        out = self.gagal("hitung-cepat", "--data", self.file("d.csv", G21_CSV), "--bulan", "2026-12",
                         "--pph-sementara")
        self.assertEqual(out["error"].count("Pilihan angka sementara tidak berlaku untuk Desember"), 1)
        self.assertEqual(out["error"].count("adalah Masa Pajak Terakhir"), 2)  # 11 orang digabung + Kiki (Sep-Nov)
        self.assertLess(len(out["error"]), 1500)
        ganda = "nama;ptkp;gaji_pokok\nAndi Fiktif;TK/0;5jt\nAndi Fiktif;K/1;6jt\nAndika Fiktif;TK/0;5,5jt\n"
        out = self.ok("hitung-cepat", "--data", self.file("g.csv", ganda), "--bulan", "2026-09")
        self.assertTrue(any("Nama ganda di data: Andi Fiktif (K001, K002)" in a for a in out["asumsi"]))
        self.assertIn("kolom masuk WAJIB", out["langkah_berikut"][0])


EX01_CSV = (
    "kode;nama;jabatan;jenis;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;bpjs;jkk;hari_kerja;masuk;nik;bank;"
    "rekening;atas_nama\n"
    "K01;Andi Fiktif;Kepala Gudang;tetap;K/1;6.000.000;750.000;400.000;kes,tk,jp;;5;2019-03-01;3201010101010001;BCA;"
    "1234567890;Andi Fiktif\n"
    "K02;Budi Fiktif;Sopir;tetap;TK/0;4.000.000;;;kes,tk,jp;;5;2020-06-15;;;;\n"
    "K03;Citra Fiktif;Manajer;tetap;K/3;12.000.000;1.000.000;;kes,tk,jp;;5;2018-01-02;;;;\n"
    "K04;Dedi Fiktif;Admin;tetap;TK/2;9.000.000;500.000;;kes,tk,jp;;5;2021-09-01;;;;\n"
    "K05;Eka Fiktif;Staf;tetap;K/0;15.000.000;;;kes,tk,jp;;5;2020-02-01;;;;\n"
    "K06;Fajar Fiktif;Teknisi;tetap;K/2;5.500.000;;;kes,tk;0,89;5;2022-04-18;;BRI;002101000123456;Fajar Fiktif\n"
    "K07;Gita Fiktif;Marketing;tetap;TK/1;7.000.000;300.000;;kes;;5;2022-08-01;;;;\n"
    "K08;Hadi Fiktif;Direktur;tetap;TK/3;20.000.000;2.000.000;;kes,tk,jp;;5;2017-05-05;;;;\n"
    "K09;Indah Fiktif;Produksi;tetap;K/1;5.400.000;;;kes,tk,jp;;5;2023-03-13;;;;\n"
    "K10;Joko Fiktif;Sopir;kontrak;K/2;3.800.000;;;tidak;;5;2025-01-06;;;;\n"
    "K11;Kiki Fiktif;Produksi;kontrak;TK/0;8.000.000;;;kes,tk,jp;;5;2026-09-15;;;;\n"
    "K12;Lina Fiktif;Supervisor;tetap;K/0;10.000.000;;;kes,tk,jp;;5;2017-08-01;;;;\n")


# --------------------------------------------------------------------------- v1.0.13 putaran 3: pemeriksa ulang (17-10-2026)
MIN_G21 = "nama;ptkp;gaji_pokok\n" + "".join(
    "%s;%s;%s\n" % (b.split(";")[1], b.split(";")[4], b.split(";")[5]) for b in G21_CSV.splitlines()[1:])
SALDO_LINA_OPSI = ["--saldo-awal", "Lina: bruto=%s; pph21=%s; iuran=%s" % SALDO_LINA]
DASAR_G21 = ["--isi", "Andi: bonus=500rb; kasbon=250rb", "--isi", "Indah: lembur-hari-kerja=2+3",
             "--masuk", "Kiki=2026-09-15", "--keluar", "Lina=2026-09-14"]
PAGAR_G21 = ["--isi", "Andi: gaji-pokok-dibayar=3jt; bonus=4jt", "--isi", "Indah: lembur-hari-kerja=2+3",
             "--masuk", "Kiki=2026-09-15", "--keluar", "Lina=2026-09-14"]
SETUJU = ["--ya-saya-paham", "--alasan-khusus",
          "cuti di luar tanggungan 12 hari sesuai perjanjian kerja pasal 7, disetujui pemilik"]
PRORATA = ["--prorata", "kalender"]


class UjiV1013Putaran3(Dasar):
    """Temuan pemeriksa ulang (lensa perilaku) atas 1.0.13: panjang pesan Telegram, klaim JKK palsu, kolom komponen
    asing, catatan iuran prorata, bulan terlewat setelah saldo awal, prorata satu komponen, Desember + pagar."""

    teks_bersih = UjiV1013.teks_bersih

    def bersih_ketat(self, teks):
        self.teks_bersih(teks)
        for kata in ("slip-gaji-bpjs", "pph21-ter", "hitung-thr", "database", "kolom", "jkk_persen", ".csv"):
            self.assertNotIn(kata, teks)

    def cepat(self, data, *opsi):
        f = self.file("data-%d.csv" % (abs(hash(data)) % 10 ** 8), data)
        return self.ok("hitung-cepat", "--data", f, "--bulan", "2026-09", *opsi)

    # HEAVY 1: semua varian realistis 12 karyawan muat SATU pesan Telegram (<= 3.800 dari batas 4.096)
    def test_panjang_teks_semua_varian_satu_pesan(self):
        umk = ["--umk", "5.396.761"]
        mini = umk + ["--jkk", "0,40"] + DASAR_G21
        g21 = umk + ["--jkk", "0,54"]
        bpjs_tidak = G21_CSV.replace(";kes,tk,jp;0,54;6;2022-04-18;", ";kes;0,54;6;2022-04-18;").replace(
            "K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;kes,tk;",
            "K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;tidak;")
        jkk040 = G21_CSV.replace(";0,54;", ";0,40;")
        varian = [
            # jalur Langkah A.0: CSV minimal nama;ptkp;gaji_pokok
            ("min", MIN_G21, mini),
            ("min+saldo", MIN_G21, mini + SALDO_LINA_OPSI),
            ("min+prorata", MIN_G21, mini + PRORATA),
            ("min+saldo+prorata", MIN_G21, mini + SALDO_LINA_OPSI + PRORATA),
            ("min+sementara", MIN_G21, mini + ["--pph-sementara"]),
            ("min+sementara+prorata", MIN_G21, mini + ["--pph-sementara"] + PRORATA),
            ("min jkk 0,54+saldo+prorata", MIN_G21, umk + ["--jkk", "0,54"] + DASAR_G21 + SALDO_LINA_OPSI + PRORATA),
            ("min tanpa jkk+saldo+prorata", MIN_G21, umk + DASAR_G21 + SALDO_LINA_OPSI + PRORATA),
            # file G21 lengkap
            ("g21", G21_CSV, g21 + DASAR_G21),
            ("g21+saldo", G21_CSV, g21 + DASAR_G21 + SALDO_LINA_OPSI),
            ("g21+prorata", G21_CSV, g21 + DASAR_G21 + PRORATA),
            ("g21+saldo+prorata", G21_CSV, g21 + DASAR_G21 + SALDO_LINA_OPSI + PRORATA),
            ("g21+sementara", G21_CSV, g21 + DASAR_G21 + ["--pph-sementara"]),
            ("g21+sementara+prorata", G21_CSV, g21 + DASAR_G21 + ["--pph-sementara"] + PRORATA),
            ("g21 tanpa jkk", G21_CSV, umk + DASAR_G21),
            ("g21 tanpa jkk+saldo+prorata", G21_CSV, umk + DASAR_G21 + SALDO_LINA_OPSI + PRORATA),
            ("g21 jkk 0,40 per baris", jkk040, umk + DASAR_G21),
            ("g21 dua tanpa BPJS", bpjs_tidak, umk + DASAR_G21),
            # pagar dasar BPJS turun (dengan/tanpa persetujuan khusus)
            ("pagar", G21_CSV, g21 + PAGAR_G21),
            ("pagar+saldo+prorata", G21_CSV, g21 + PAGAR_G21 + SALDO_LINA_OPSI + PRORATA),
            ("setuju+alasan", G21_CSV, g21 + PAGAR_G21 + SETUJU),
            ("setuju (alasan singkat)", G21_CSV, g21 + PAGAR_G21 + ["--ya-saya-paham", "--alasan-khusus", "uji"]),
            ("setuju+prorata", G21_CSV, g21 + PAGAR_G21 + ["--ya-saya-paham", "--alasan-khusus", "uji"] + PRORATA),
            ("setuju+saldo+prorata", G21_CSV, g21 + PAGAR_G21 + SETUJU + SALDO_LINA_OPSI + PRORATA),
            ("setuju+sementara+prorata", G21_CSV, g21 + PAGAR_G21 + SETUJU + ["--pph-sementara"] + PRORATA),
        ]
        panjang = {}
        for nama, data, opsi in varian:
            out = self.cepat(data, *opsi)
            panjang[nama] = len(out["teks"])
            self.assertLessEqual(len(out["teks"]), G.BATAS_PESAN, (nama, len(out["teks"])))
            self.assertNotIn("teks_bagian", out, nama)
            self.bersih_ketat(out["teks"])
        self.assertLessEqual(max(panjang.values()), 3800, panjang)
        # penyebab utama dulu: 11 nama tanpa tanggal masuk tidak lagi didaftar satu per satu
        out = self.cepat(MIN_G21, *(mini + SALDO_LINA_OPSI))
        self.assertIn("Tanggal masuk 11 karyawan (semua kecuali Kiki Fiktif) tidak ada di data", out["teks"])
        self.assertNotIn("Andi Fiktif, Budi Fiktif, Citra Fiktif", out["teks"])
        # kelebihan PPh 21 Lina disebut sekali (baris setoran), tidak diulang di "Perlu diperhatikan"
        kembali = G.rp(Decimal(str(out["total"]["pengembalian_pph21"])))
        self.assertEqual(len(re.findall(r"(?<![\d.])%s(?![\d])" % re.escape(kembali[3:]), out["teks"])), 2)  # tabel+baris
        self.assertIn("dikembalikan ke karyawan (Lina Fiktif, sudah di gaji bersih): %s" % kembali, out["teks"])
        self.assertNotIn("lebih potong", out["teks"])
        # persetujuan khusus + dasar BPJS turun: satu kalimat, alasan ikut, tetap jujur "belum disimpan"
        out = self.cepat(G21_CSV, *(g21 + PAGAR_G21 + SETUJU))
        self.assertEqual(out["teks"].count("persetujuan khusus pemilik"), 1)
        self.assertIn("belum disimpan, dicatat saat disimpan. Alasan: cuti di luar tanggungan 12 hari", out["teks"])

    def test_teks_panjang_dibagi_aman(self):
        """Usaha besar (45 karyawan): teks tidak muat satu pesan -> teks_bagian, tiap bagian <= 3.800, tidak ada isi
        yang hilang, judul kolom tabel diulang di bagian berikutnya."""
        data = "nama;ptkp;gaji_pokok;tunjangan_tetap;masuk\n" + "".join(
            "Karyawan Nomor %02d Fiktif Panjang;TK/0;%d;250000;2020-01-01\n" % (i, 5400000 + i * 37000)
            for i in range(1, 46))
        out = self.cepat(data, "--umk", "5.396.761", "--jkk", "0,54", "--keluar",
                         "Karyawan Nomor 07 Fiktif Panjang=2026-09-10")
        self.assertGreater(len(out["teks"]), G.BATAS_PESAN)
        bagian = out["teks_bagian"]
        self.assertGreaterEqual(len(bagian), 2)
        self.assertTrue(all(len(b) <= G.BATAS_PESAN for b in bagian), [len(b) for b in bagian])
        gabung = "\n".join(bagian)
        self.assertTrue(all(baris in gabung for baris in out["teks"].split("\n")))
        self.assertTrue(bagian[1].startswith("| Kode | Nama |"))               # lanjutan tabel tetap berjudul
        self.assertIn("| Kode | Nama |", bagian[0])                            # judul rekap tidak sendirian
        self.assertTrue(bagian[-1].rstrip().endswith("tersimpan di komputer ini."))
        # fungsi pemotong: teks pendek tidak diubah; baris sangat panjang dipotong di spasi
        self.assertEqual(G.bagi_teks("pendek"), ["pendek"])
        b = G.bagi_teks("A" * 100 + "\n\n" + "kata " * 1200, 1000)
        self.assertTrue(all(len(x) <= 1000 for x in b))
        self.assertEqual("".join(b).replace(" ", "").replace("\n", ""), "A" * 100 + "kata" * 1200)

    # HEAVY 2: tarif JKK per baris di data -> tidak ada klaim "dipakai 0,24%" (hitung-cepat & database)
    def test_jkk_per_baris_tanpa_tarif_umum(self):
        out = self.cepat(G21_CSV, "--umk", "5.396.761", *DASAR_G21)
        t = out["teks"]
        self.assertNotIn("0,24%", t)
        self.assertNotIn("belum diisi", t)
        self.assertNotIn("belum disebut", t)
        self.assertIn("Tarif JKK dari data karyawan: 0,54%.", t)
        upah = sum(Decimal(str(k["payroll"]["pendapatan"]["Gaji pokok"])) + Decimal(str(
            k["payroll"]["pendapatan"]["Tunjangan tetap"])) for k in out["karyawan"])
        self.assertEqual(Decimal(str(out["total"]["jkk"])), sum(
            (_r((Decimal(str(k["payroll"]["pendapatan"]["Gaji pokok"])) + Decimal(str(
                k["payroll"]["pendapatan"]["Tunjangan tetap"]))) * Decimal("0.54") / 100) for k in out["karyawan"]),
            Decimal(0)))
        self.assertGreater(upah, 0)
        # tarif 0,40 per baris: hanya peringatan porsi JKK murni + tarif yang dipakai, tidak ada kalimat bertentangan
        t = self.cepat(G21_CSV.replace(";0,54;", ";0,40;"), "--umk", "5.396.761", *DASAR_G21)["teks"]
        self.assertNotIn("0,24%", t)
        self.assertIn("tarif JKK 0,4%", t)
        self.assertIn("Tarif JKK dari data karyawan: 0,4%.", t)
        # campuran per baris
        campur = "".join(b.replace(";0,54;", ";0,24;") if i % 2 else b for i, b in enumerate(
            G21_CSV.splitlines(True)))
        t = self.cepat(campur, "--umk", "5.396.761")["teks"]
        self.assertIn("Tarif JKK dari data karyawan: 0,24% (6 karyawan), 0,54% (6 karyawan).", t)
        # sebagian kosong: asumsi hanya menyebut yang kosong
        sebagian = "nama;ptkp;gaji_pokok;jkk\nAni Fiktif;TK/0;6jt;0,54\nBayu Fiktif;K/1;7jt;\n"
        out = self.cepat(sebagian)
        self.assertTrue(any(a.startswith("Tarif JKK dari data karyawan: 0,54% (Ani Fiktif); belum diisi untuk Bayu "
                                         "Fiktif: dipakai 0,24% (risiko sangat rendah)") for a in out["asumsi"]),
                        out["asumsi"])                                                 # sama dengan alur database
        self.assertEqual(out["teks"].count("0,24%"), 1)
        # hanya karyawan yang DIHITUNG yang dihitung (yang tertunda tidak ikut disebut memakai 0,24%)
        data = "".join(b if i < 7 else b.replace(";0,54;", ";;") for i, b in enumerate(G21_CSV.splitlines(True)))
        out = self.cepat(data, "--umk", "5.396.761", "--keluar", "Lina=2026-09-14")
        self.assertIn("Tarif JKK dari data karyawan: 0,54% (6 karyawan); belum diisi untuk 5 karyawan: dipakai 0,24%",
                      out["teks"])
        self.assertEqual(Decimal(str(out["total"]["jkk"])), Decimal(261720))
        # semua kosong & tanpa tarif umum: kalimat lama tetap (memang benar 0,24%)
        out = self.cepat("nama;ptkp;gaji_pokok\nAni Fiktif;TK/0;6jt\n")
        self.assertTrue(any(a.startswith("Tarif JKK belum disebut: dipakai 0,24%") for a in out["asumsi"]))
        # alur database: atur tanpa --jkk, impor dengan kolom jkk -> sama
        self.ok("atur", "--umk", "5.396.761")
        self.ok("karyawan", "impor", self.file("g21.csv", G21_CSV), "--ya")
        h, out = self.hasil("2026-08")
        self.assertNotIn("belum diisi", out["teks"])
        self.assertNotIn("0,24%", out["teks"])
        self.assertIn("Tarif JKK dari data karyawan: 0,54%.", out["teks"])
        self.assertFalse(any(p.startswith(G.JKK_BELUM) for p in out["peringatan_hitung"]))
        # database tanpa tarif di data & tanpa tarif umum -> peringatan mesin tetap (benar)
        self.tambah("Zaki", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2020-01-01")
        _, out = self.hasil("2026-08")
        self.assertIn("Tarif JKK dari data karyawan: 0,54% (11 karyawan); belum diisi untuk Zaki: dipakai 0,24%",
                      out["teks"])

    # LIGHT a: kolom komponen asing tidak lagi diam-diam diabaikan; nama kolom 'dibayar' dikenali
    def test_komponen_kolom_tidak_dikenal_dan_alias(self):
        f = self.file("g21.csv", G21_CSV)
        umum = ["hitung-cepat", "--data", f, "--bulan", "2026-09", "--umk", "5.396.761", "--jkk", "0,54"]
        out = self.ok(*umum, "--komponen", self.file("k1.csv", "nama;gaji_pokok_dibayar;bonus\nAndi Fiktif;3jt;4jt\n"))
        self.assertIn("K01:dasar_bpjs_turun_bulan_penuh", out["masalah_kepatuhan"])      # pagar tetap bekerja
        self.assertIn("K01", [t["kode"] for t in out["tertunda"]])
        self.assertEqual(out["kolom_tidak_dikenal"], [])
        out = self.ok(*umum, "--komponen", self.file("k2.csv", "no;nama;insentif_harian;bonus\n1;Andi Fiktif;100rb;1jt\n"))
        self.assertEqual(out["kolom_tidak_dikenal"], ["insentif_harian"])
        self.assertIn('Isian "insentif harian" di daftar komponen tidak dikenali, jadi TIDAK dihitung', out["teks"])
        self.bersih_ketat(out["teks"])
        andi = [k for k in out["karyawan"] if k["kode"] == "K01"][0]
        self.assertEqual(Decimal(str(andi["payroll"]["pendapatan"]["Bonus/THR"])), Decimal(1000000))
        # alur database (isi --file): diberi peringatan, bukan diam
        self.ok("karyawan", "impor", f, "--ya")
        out = self.ok("isi", "--bulan", "2026-09", "--file", self.file("k3.csv", "nama;bonus;uang_lelah\nBudi;1jt;50rb\n"))
        self.assertEqual(out["kolom_tidak_dikenal"], ["uang_lelah"])
        self.assertIn('Isian "uang lelah" di daftar komponen tidak dikenali', out["teks"])
        self.assertFalse(out["perlu_persetujuan_khusus"])

    # LIGHT b: catatan iuran prorata sesuai cara mesin (BPJS Kesehatan minimal UMK)
    def test_catatan_iuran_prorata_akurat(self):
        out = self.cepat(G21_CSV, "--umk", "5.396.761", "--jkk", "0,54", *(DASAR_G21 + SALDO_LINA_OPSI + PRORATA))
        self.assertIn("Iuran BPJS ikut angka prorata, tetapi dasar BPJS Kesehatan minimal UMK", out["teks"])
        kiki = [k for k in out["karyawan"] if k["kode"] == "K11"][0]["payroll"]["iuran"]
        self.assertEqual(Decimal(str(kiki["kes_karyawan"])), _r(UMK_G21 / 100))           # dasar = UMK, bukan prorata
        self.assertEqual(Decimal(str(kiki["jht_karyawan"])), _r(Decimal(2880000) * 2 / 100))  # JHT ikut prorata
        # gaji penuh Kiki & Lina >= UMK: tidak ada peringatan UMK palsu di teks pemilik (JSON tetap rinci)
        self.assertNotIn("di bawah UMK", out["teks"])
        self.assertTrue(any("tidak di bawah UMK" in p for p in out["peringatan_hitung"]))
        out = self.cepat(G21_CSV, "--jkk", "0,54", *(DASAR_G21 + SALDO_LINA_OPSI + PRORATA))     # tanpa UMK
        self.assertIn("Iuran BPJS Kesehatan & Ketenagakerjaan ikut angka prorata", out["teks"])
        kiki = [k for k in out["karyawan"] if k["kode"] == "K11"][0]["payroll"]["iuran"]
        self.assertEqual(Decimal(str(kiki["kes_karyawan"])), Decimal(28800))                # 1% x 2.880.000
        # gaji penuh di bawah UMK tetap diperingatkan, dengan angka gaji penuhnya
        out = self.cepat(G21_CSV.replace("K11;Kiki Fiktif;Staf Produksi;kontrak;TK/0;5.400.000",
                                         "K11;Kiki Fiktif;Staf Produksi;kontrak;TK/0;5.000.000"),
                         "--umk", "5.396.761", "--jkk", "0,54", *(DASAR_G21 + SALDO_LINA_OPSI + PRORATA))
        self.assertIn("sebulan penuh di bawah UMK yang Anda isi (Rp 5.396.761): Kiki Fiktif (Rp 5.000.000)",
                      out["teks"])

    # LIGHT c: saldo awal s.d. Agustus, September tidak dihitung, aplikasi mulai Oktober -> dua pilihan
    def test_bulan_terlewat_setelah_saldo_awal(self):
        e = self.tambah("Eko", "--ptkp", "K/1", "--gaji-pokok", "12jt", "--masuk", "2020-01-01")["kode"]
        s_ = self.tambah("Sri", "--ptkp", "TK/0", "--gaji-pokok", "6jt", "--masuk", "2021-01-01")["kode"]
        for k, b, p, i in ((e, "100jt", "2jt", "2,9jt"), (s_, "50jt", "0", "1,4jt")):
            self.ok("saldo-awal", "--karyawan", k, "--tahun", "2026", "--sampai-bulan", "8", "--bruto", b,
                    "--pph21", p, "--iuran", i)
        self.ok("hitung", "--bulan", "2026-10")
        self.ok("final", "--bulan", "2026-10", "--ya")
        self.ok("karyawan", "keluar", "--karyawan", e, "--tanggal", "2026-11-14", "--ya")
        out = self.ok("hitung", "--bulan", "2026-11")
        t = out["tertunda"][0]
        self.assertIn("Gaji September 2026 belum dihitung & dikunci di aplikasi ini: hitung dan kunci dulu bulan itu "
                      "(bila gajinya dibayar di luar aplikasi, kirim totalnya Januari–September 2026 sebagai saldo "
                      "awal)", t["teks"])
        self.assertNotIn("Butuh total Januari–September", t["teks"])
        self.assertIn("hitung --bulan 2026-09", t["langkah_agent"])
        self.assertTrue(any("saldo-awal --karyawan %s --tahun 2026 --sampai-bulan 9" % e in x
                            for x in t["langkah_agent"]))
        self.teks_bersih(out["teks"])

    # LIGHT d: hanya satu komponen 'dibayar' diisi -> konsisten, disebut dalam satu kalimat
    def test_prorata_satu_komponen(self):
        g21 = ["--umk", "5.396.761", "--jkk", "0,54", "--keluar", "Lina=2026-09-14"]
        out = self.cepat(G21_CSV, *(g21 + SALDO_LINA_OPSI + ["--isi", "Lina: gaji-pokok-dibayar=4.666.667"]))
        self.assertIn("Lina Fiktif: gaji pokok bulan ini diisi Rp 4.666.667; tunjangan tetap Rp 1.000.000 tetap "
                      "dihitung penuh.", out["teks"])
        self.assertNotIn("Lina Fiktif (keluar", out["teks"].split("Perlu diperhatikan")[1])
        out = self.cepat(G21_CSV, *(g21 + ["--isi", "Lina: tunjangan-tetap-dibayar=466.667"]))
        self.assertNotIn("penuh atau prorata", out["teks"])                 # tidak ditanya lagi
        out = self.cepat(G21_CSV, *(g21 + SALDO_LINA_OPSI + ["--isi", "Lina: tunjangan-tetap-dibayar=466.667"]))
        self.assertIn("Lina Fiktif: tunjangan tetap bulan ini diisi Rp 466.667; gaji pokok Rp 10.000.000 tetap "
                      "dihitung penuh.", out["teks"])
        penuh = [b for b in out["teks"].split("\n") if "gaji dihitung PENUH" in b]
        self.assertFalse(any("Lina" in b for b in penuh), penuh)           # tidak ada pertanyaan ganda untuk Lina

    # LIGHT e: disclaimer tanpa nama skill bertanda hubung; Desember + pagar ditanya sekali
    def test_disclaimer_dan_desember_pagar_satu_pesan(self):
        for kata in ("slip-gaji-bpjs", "pph21-ter", "hitung-thr"):
            self.assertNotIn(kata, G.DISCLAIMER)
        self.assertIn("mesin hitung gaji, PPh 21 dan THR Komunitech", G.DISCLAIMER)
        out = self.gagal("hitung-cepat", "--data", self.file("d.csv", G21_CSV), "--bulan", "2026-12",
                         "--isi", "Andi: gaji-pokok-dibayar=3jt; bonus=4jt")
        andi = [x for x in out["error"].split("\n") if x.startswith("- Andi Fiktif")][0]
        self.assertIn("perlu persetujuan khusus pemilik", andi)
        self.assertIn("Selain itu, data Masa Pajak Terakhir-nya juga belum ada (sama dengan Budi Fiktif dkk.)", andi)
        t = [x for x in out["tertunda"] if x["kode"] == "K01"][0]
        self.assertTrue(any("saldo-awal --karyawan K01 --tahun 2026 --sampai-bulan 11" in x for x in t["langkah_agent"]))
        self.assertEqual(len(t["data_dibutuhkan"]), 2)
        # dua karyawan perlu persetujuan khusus: kalimat dasar hukum cukup sekali
        data = G21_CSV.replace(";kes,tk,jp;0,54;6;2022-04-18;", ";kes;0,54;6;2022-04-18;").replace(
            "K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;kes,tk;",
            "K10;Joko Fiktif;Staf Produksi;kontrak;K/1;5.400.000;;300.000;tidak;")
        teks = self.cepat(data, "--umk", "5.396.761", "--jkk", "0,54")["teks"]
        self.assertEqual(teks.count("UU 24/2011 Pasal 15"), 1)
        self.assertIn("Untuk Gita Fiktif, Joko Fiktif: Wajib BPJS dengan upah sebenarnya", teks)


class UjiV1013Putaran4(Dasar):
    """Temuan pemeriksa ulang putaran 3 (17-10-2026): kolom komponen asing di isi --file bukan masalah kepatuhan,
    teks pratinjau tanpa instruksi agent, pemotong teks tidak meninggalkan judul/penutup sendirian."""

    teks_bersih = UjiV1013.teks_bersih

    def siapkan(self):
        self.ok("atur", "--umk", "5.396.761", "--jkk", "0,54")
        self.ok("karyawan", "impor", self.file("g21.csv", G21_CSV), "--ya")

    def test_isi_file_kolom_asing_bukan_persetujuan_khusus(self):
        self.siapkan()
        f = self.file("a.csv", "nama;bonus;uang_makan_harian;insentif_toko\nAndi Fiktif;1jt;300rb;200rb\n")
        out = self.ok("isi", "--bulan", "2026-09", "--file", f)                                  # pratinjau
        self.assertFalse(out["perlu_persetujuan_khusus"])
        self.assertNotIn("masalah_kepatuhan", out)
        self.assertEqual(out["kolom_tidak_dikenal"], ["uang_makan_harian", "insentif_toko"])
        t = out["teks"]
        for kata in ("PERSETUJUAN KHUSUS", "BELUM BISA", "persetujuan khusus"):
            self.assertNotIn(kata, t)
        self.assertIn('Isian "uang makan harian" dan "insentif toko" di daftar komponen tidak dikenali, jadi TIDAK '
                      'dihitung. Bila itu bagian gaji, sebutkan masuk tunjangan tidak tetap', t)
        self.teks_bersih(t)
        self.assertEqual(out["langkah_berikut"], [G.LANGKAH_SIMPAN])
        out = self.ok("isi", "--bulan", "2026-09", "--file", f, "--ya")                          # --ya biasa cukup
        self.assertEqual(out["mode"], "tersimpan")
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM isian"), 1)                          # hanya bonus
        self.teks_bersih(out["teks"])
        self.assertNotIn(self.dir, out["teks"])                                                 # tanpa jalur file
        # penurunan dasar BPJS sungguhan (bulan penuh) tetap memicu persetujuan khusus, kolom asing atau tidak
        g = self.file("b.csv", "nama;gaji_pokok_dibayar;uang_lelah\nBudi Fiktif;3jt;50rb\n")
        out = self.ok("isi", "--bulan", "2026-09", "--file", g)
        self.assertTrue(out["perlu_persetujuan_khusus"])
        self.assertIn("PERLU PERSETUJUAN KHUSUS", out["teks"])
        self.assertIn("--ya-saya-paham", out["langkah_berikut"][0])
        self.assertNotIn("--", out["teks"])
        out = self.gagal("isi", "--bulan", "2026-09", "--file", g, "--ya")
        self.assertEqual(out["masalah_kepatuhan"], ["dasar_bpjs_turun_bulan_penuh:K02"])
        self.assertEqual(self.jumlah("SELECT COUNT(*) FROM isian"), 1)                          # tidak tersimpan

    def test_teks_pratinjau_tanpa_instruksi_agent(self):
        d = tempfile.mkdtemp()
        try:
            db2 = os.path.join(d, "baru.db")
            kode, out, _ = self.cli("init", "--nama-usaha", "Toko Fiktif")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                G.main(["init", "--db", db2, "--json", "--nama-usaha", "Toko Fiktif"])
            out = json.loads(buf.getvalue())
            self.assertEqual(out["mode"], "pratinjau")
            self.assertNotIn(d, out["teks"])
            self.assertNotIn("--", out["teks"])
            self.assertEqual(out["langkah_berikut"], [G.LANGKAH_SIMPAN])
        finally:
            shutil.rmtree(d, ignore_errors=True)
        self.siapkan()
        cek = []
        cek.append(self.ok("karyawan", "impor", self.file("x.csv", "nama;ptkp;gaji_pokok;masuk\nZaki Fiktif;TK/0;6jt;"
                                                                    "2024-01-01\n")))
        cek.append(self.ok("karyawan", "keluar", "--karyawan", "Lina", "--tanggal", "2026-09-14"))
        isi = self.ok("isi", "--bulan", "2026-08", "--karyawan", "Andi", "--bonus", "500rb")
        self.assertEqual(isi["langkah_berikut"], ["hitung --bulan 2026-08"])
        cek.append(isi)
        self.ok("hitung", "--bulan", "2026-08")
        fin = self.ok("final", "--bulan", "2026-08")
        self.assertTrue(fin["teks"].endswith('Balas "kunci" - setelah dikunci, angka bulan ini hanya bisa diubah lewat '
                                             'revisi tercatat.'))
        cek.append(fin)
        cek.append(self.ok("final", "--bulan", "2026-08", "--ya"))
        tr = self.ok("transfer", "--bulan", "2026-08", "--keluar", self.dir)
        self.assertTrue(any("--rekening-lengkap" in x for x in tr["langkah_berikut"]))
        for out in (tr, self.ok("slip", "--bulan", "2026-08", "--keluar", self.dir)):
            self.assertNotIn(self.dir, out["teks"])                                     # tanpa jalur folder/file
            self.assertNotRegex(out["teks"], r"--[a-z]")
        rev = self.ok("revisi", "--bulan", "2026-08", "--alasan", "uji revisi fiktif")
        self.assertIn("final --bulan 2026-08 (pratinjau, lalu --ya)", rev["langkah_berikut"])
        cek.append(rev)
        for out in cek:
            self.teks_bersih(out["teks"])
            for kata in ("Jalankan perintah", "gaji.py", self.dir, ".db"):
                self.assertNotIn(kata, out["teks"])
            if out["mode"] == "pratinjau":
                self.assertEqual(out["langkah_berikut"][0], G.LANGKAH_SIMPAN)

    def test_pemotong_judul_dan_penutup_tidak_sendirian(self):
        judul = "REKAP GAJI SEPTEMBER 2026 - Toko\nStatus: DRAF | 40 karyawan"
        tabel = "| Kode | Nama | Gaji |\n|---|---|---:|\n" + "\n".join("| K%03d | Orang %03d | 5.000.000 |" % (i, i)
                                                                      for i in range(114))
        self.assertLess(len(tabel), G.BATAS_PESAN)
        self.assertGreater(len(judul) + 2 + len(tabel), G.BATAS_PESAN)        # tabel muat sendiri, tidak bersama judul
        teks = judul + "\n\n" + tabel + "\n\nYang harus dibayar:\n- Transfer: Rp 1\n\n_" + "x" * 500 + "_\n\nBalas simpan."
        b = G.bagi_teks(teks)
        self.assertTrue(b[0].startswith(judul + "\n\n| Kode | Nama | Gaji |"))  # judul tetap bersama tabel
        self.assertTrue(all(len(x) <= G.BATAS_PESAN for x in b))
        self.assertIn("Yang harus dibayar", b[-1])                            # pesan terakhir bukan hanya penutup
        gab = "\n".join(b)
        self.assertTrue(all(baris in gab for baris in teks.split("\n")))
        # bagian terakhir tidak hanya kalimat penutup: disclaimer ikut pindah ke pesan terakhir
        teks2 = "A" * 3500 + "\n\n" + "B" * 250 + "\n\n" + "_" + "d" * 500 + "_\n\nBalas simpan."
        b = G.bagi_teks(teks2)
        self.assertEqual([len(x) for x in b], [3500, 769])                   # bagian pendek dipindah ke pesan akhir
        self.assertTrue(b[-1].startswith("B") and b[-1].endswith("Balas simpan."))
        # kasus nyata: CSV minimal + pagar BPJS (jalur Langkah A.0) -> 2 pesan seimbang, tidak ada isi hilang
        out = self.ok("hitung-cepat", "--data", self.file("min.csv", MIN_G21), "--bulan", "2026-09", "--umk",
                      "5.396.761", "--jkk", "0,40", *PAGAR_G21)
        b = out["teks_bagian"]
        self.assertEqual(len(b), 2)
        self.assertTrue(b[0].startswith("REKAP GAJI") and "| **Total** |" in b[0])
        self.assertTrue(b[1].rstrip().endswith("tersimpan di komputer ini."))
        self.assertTrue(all(G.BATAS_PESAN // 4 <= len(x) <= G.BATAS_PESAN for x in b), [len(x) for x in b])
        gab = "\n".join(b)
        self.assertTrue(all(baris in gab for baris in out["teks"].split("\n")))


class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "gaji.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["init", "--db", os.path.join(t, "a.db"), "--y"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "a.db")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main(verbosity=1)
