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
        self.assertIn("Januari 2026 (belum ada)", out["error"])
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
        self.assertIn("payroll.py", out["error"])
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
        dipotong = sum(Decimal(str(x["payroll"]["pph_disetor"])) for x in h.values())
        tot = out["total"]
        self.assertEqual(Decimal(str(tot["pph21_dipotong"])), dipotong)
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
        self.assertIn("--ya-saya-paham", out["teks"])
        self.assertNotIn("Simpan? Jalankan perintah yang sama + --ya setelah", out["teks"])
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
        self.assertIn("--ya --ya-saya-paham", penutup)
        self.assertNotIn("Simpan? Jalankan perintah yang sama + --ya setelah", out["teks"])
        # pratinjau biasa tetap memakai kalimat baku
        out = self.ok("karyawan", "ubah", "--karyawan", e, "--jabatan", "Kasir")
        self.assertIn("Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.", out["teks"])



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
