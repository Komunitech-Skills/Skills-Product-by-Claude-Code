#!/usr/bin/env python3
"""Uji regresi scripts/skor_audit.py (audit-akun-iklan).

Angka pembanding dihitung ulang dengan cara terpisah (pecahan Fraction, bukan fungsi script)
supaya kesalahan rumus di script ketahuan.

Jalankan: python3 tests/uji_skor_audit.py   (Windows: python / py)
"""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
SCRIPT = SINI / "scripts" / "skor_audit.py"
sys.path.insert(0, str(SINI / "scripts"))
import skor_audit as m  # noqa: E402

W = {"kritis": 5, "tinggi": 3, "sedang": 1}
KR = {"lulus": Fraction(1), "sebagian": Fraction(1, 2), "gagal": Fraction(0)}


def jalan(*argv):
    r = subprocess.run([sys.executable, str(SCRIPT), *argv], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def skor_manual(platform, status):
    """Hitung ulang skor platform secara independen dengan Fraction."""
    cek = list(csv.DictReader((SINI / "scripts" / "daftar_cek.csv").read_text(encoding="utf-8").splitlines()))
    bobot = {b["kategori"]: Fraction(b["bobot"]) for b in
             csv.DictReader((SINI / "scripts" / "bobot_kategori.csv").read_text(encoding="utf-8").splitlines())
             if b["platform"] == platform}
    kat = {}
    berlaku = diketahui = Fraction(0)
    for c in cek:
        if c["platform"] != platform:
            continue
        st = status.get(c["id"], "tidak_tahu")
        if st == "tidak_berlaku":
            continue
        w = W[c["keparahan"]]
        berlaku += w
        if st in KR:
            diketahui += w
            a = kat.setdefault(c["kategori"], [Fraction(0), Fraction(0)])
            a[0] += w * KR[st]
            a[1] += w
    total = sum(bobot[k] for k in kat)
    skor = sum(100 * a[0] / a[1] * bobot[k] for k, a in kat.items()) / total
    return skor, 100 * diketahui / berlaku


def bulat1(fr):
    return Decimal(fr.numerator) / Decimal(fr.denominator)


class UjiData(unittest.TestCase):
    def test_01_data_konsisten(self):
        self.assertEqual(m.periksa_data(), [])

    def test_02_bobot_tiap_platform_100(self):
        for p, k in m.muat_bobot().items():
            self.assertEqual(sum(k.values()), 100, p)

    def test_03_semua_platform_punya_cek(self):
        cek, _ = m.muat_cek()
        for p in m.PLATFORM:
            self.assertGreaterEqual(sum(1 for c in cek.values() if c["platform"] == p), 10, p)

    def test_04_tanpa_pola_berbahaya_di_script(self):
        teks = SCRIPT.read_text(encoding="utf-8")
        for kata in ("urllib", "requests", "socket", "subprocess", "os.system", "eval(", "exec("):
            self.assertNotIn(kata, teks)


class UjiSkor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def tulis(self, nama, baris, header=("id", "status", "catatan"), pemisah=","):
        p = self.dir / nama
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=pemisah)
            w.writerow(header)
            w.writerows(baris)
        return p

    def test_05_contoh_shopee_cocok_hitung_manual(self):
        p = SINI / "examples" / "01-jawaban-toko-fashion-shopee.csv"
        jw, _, _ = m.baca_jawaban(p)
        h = m.hitung(jw)
        skor, cak = skor_manual("shopee", {k: v[0] for k, v in jw.items()})
        self.assertEqual(m.satu_desimal(h["platform"]["shopee"]["skor"]), m.satu_desimal(bulat1(skor)))
        self.assertEqual(m.satu_desimal(h["platform"]["shopee"]["cakupan"]), m.satu_desimal(bulat1(cak)))
        self.assertEqual(str(m.satu_desimal(h["platform"]["shopee"]["skor"])), "41.3")

    def test_06_contoh_meta_dan_google_cocok_manual(self):
        for nama, plat in (("02-jawaban-klinik-kecantikan-meta.csv", "meta"),
                           ("03-jawaban-kursus-online-google.csv", "google")):
            jw, _, _ = m.baca_jawaban(SINI / "examples" / nama)
            h = m.hitung(jw)
            skor, cak = skor_manual(plat, {k: v[0] for k, v in jw.items()})
            self.assertEqual(m.satu_desimal(h["platform"][plat]["skor"]), m.satu_desimal(bulat1(skor)), nama)
            self.assertEqual(m.satu_desimal(h["platform"][plat]["cakupan"]), m.satu_desimal(bulat1(cak)), nama)

    def test_07_semua_lulus_100(self):
        cek, _ = m.muat_cek()
        jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == "tiktok"}
        h = m.hitung(jw)
        self.assertEqual(h["platform"]["tiktok"]["skor"], 100)
        self.assertEqual(h["platform"]["tiktok"]["status"], "final")
        self.assertEqual(h["prioritas"], [])

    def test_08_semua_gagal_0_dan_prioritas_urut(self):
        cek, _ = m.muat_cek()
        jw = {i: ("gagal", "") for i, c in cek.items() if c["platform"] == "meta"}
        h = m.hitung(jw)
        self.assertEqual(h["platform"]["meta"]["skor"], 0)
        nilai = [x["prioritas"] for x in h["prioritas"]]
        self.assertEqual(nilai, sorted(nilai, reverse=True))
        self.assertEqual(h["prioritas"][0]["prioritas"], 15)   # kritis x mudah

    def test_09_sebagian_setengah_kredit(self):
        # G02 kritis & G03 tinggi di pelacakan; lainnya tidak_berlaku kecuali satu kategori
        cek, _ = m.muat_cek()
        jw = {i: ("tidak_berlaku", "") for i, c in cek.items() if c["platform"] == "google"}
        jw["G02"] = ("sebagian", "")
        h = m.hitung(jw)
        self.assertEqual(h["platform"]["google"]["skor"], 50)

    def test_10_tidak_tahu_menurunkan_cakupan_bukan_skor(self):
        cek, _ = m.muat_cek()
        ids = [i for i, c in cek.items() if c["platform"] == "shopee"]
        jw = {i: ("lulus", "") for i in ids}
        jw[ids[0]] = ("tidak_tahu", "")
        h = m.hitung(jw)
        self.assertEqual(h["platform"]["shopee"]["skor"], 100)
        self.assertLess(h["platform"]["shopee"]["cakupan"], 100)

    def test_11_bukti_kurang_tidak_ikut_gabungan(self):
        cek, _ = m.muat_cek()
        jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == "meta"}
        jw["S01"] = ("gagal", "")          # shopee hanya 1 cek terjawab -> bukti kurang
        h = m.hitung(jw)
        self.assertEqual(h["platform"]["shopee"]["status"], "bukti_kurang")
        self.assertIn("shopee", h["gabungan"]["dikeluarkan"])
        self.assertEqual(h["gabungan"]["skor"], 100)
        self.assertEqual(h["gabungan"]["status"], "sementara")

    def test_12_gabungan_bobot_belanja(self):
        cek, _ = m.muat_cek()
        jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == "meta"}
        jw.update({i: ("gagal", "") for i, c in cek.items() if c["platform"] == "shopee"})
        h = m.hitung(jw, {"meta": Decimal(3000000), "shopee": Decimal(1000000)})
        self.assertEqual(h["gabungan"]["skor"], 75)     # 100 x 0,75 + 0 x 0,25
        self.assertEqual(h["gabungan"]["cara_bobot"], "porsi belanja")
        self.assertEqual(h["gabungan"]["status"], "final")

    def test_13_gabungan_rata_bila_belanja_kurang(self):
        cek, _ = m.muat_cek()
        jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == "meta"}
        jw.update({i: ("gagal", "") for i, c in cek.items() if c["platform"] == "shopee"})
        h = m.hitung(jw, {"meta": Decimal(3000000)})
        self.assertEqual(h["gabungan"]["skor"], 50)
        self.assertEqual(h["gabungan"]["status"], "sementara")

    def test_14_naik_skor_tepat(self):
        cek, _ = m.muat_cek()
        ids = [i for i, c in cek.items() if c["platform"] == "shopee"]
        jw = {i: ("lulus", "") for i in ids}
        jw["S14"] = ("gagal", "")   # satu-satunya cek pengecualian (bobot kategori 10)
        h = m.hitung(jw)
        self.assertEqual(h["platform"]["shopee"]["skor"], 90)
        self.assertEqual(h["prioritas"][0]["naik"], 10)

    def test_15_cek_dulu_kritis_tidak_tahu_masuk_hari_1(self):
        cek, _ = m.muat_cek()
        jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == "google"}
        jw["G01"] = ("tidak_tahu", "")
        h = m.hitung(jw, mulai=date(2026, 9, 28))
        self.assertEqual([c["id"] for c in h["cek_dulu"]], ["G01"])
        self.assertIn("G01", h["rencana"]["hari"][0]["tugas"][0])
        self.assertIn("Senin, 28 Sep 2026", h["rencana"]["hari"][0]["label"])

    def test_16_rencana_kapasitas_dan_antrean(self):
        cek, _ = m.muat_cek()
        jw = {i: ("gagal", "") for i in cek}          # semua platform gagal -> banyak tugas
        h = m.hitung(jw)
        beban = {"mudah": 1, "sedang": 2, "sulit": 3}
        idx = {c["id"]: c for c in cek.values()}
        for d in h["rencana"]["hari"][:5]:
            total = 0
            for t in d["tugas"]:
                i = t.split("[")[1].split("]")[0]
                total += beban[idx[i]["kemudahan"]]
            self.assertLessEqual(total, 3)
        self.assertTrue(h["rencana"]["antrean_berikutnya"])
        self.assertEqual(len(h["rencana"]["hari"]), 7)

    def test_17_sinonim_status(self):
        for teks, harap in (("Ya", "lulus"), ("BELUM", "gagal"), ("tidak tahu", "tidak_tahu"),
                            ("n/a", "tidak_berlaku"), ("-", "tidak_berlaku"), ("", "tidak_tahu"),
                            ("Sebagian", "sebagian"), ("tidak-berlaku", "tidak_berlaku")):
            self.assertEqual(m.normal_status(teks), harap, teks)

    def test_18_csv_titik_koma_dan_bom(self):
        p = self.dir / "j.csv"
        p.write_bytes("﻿id;status;catatan\nM01;ya;\nM02;belum;x\n".encode("utf-8"))
        jw, _, _ = m.baca_jawaban(p)
        self.assertEqual(jw["M01"][0], "lulus")
        self.assertEqual(jw["M02"][0], "gagal")

    def test_19_catatan_berkoma_tanpa_kutip_tidak_hilang(self):
        p = self.dir / "j.csv"
        p.write_text("id,status,catatan\nS06,gagal,ROAS 2, impas 2,92\n", encoding="utf-8")
        jw, _, _ = m.baca_jawaban(p)
        self.assertEqual(jw["S06"][1], "ROAS 2, impas 2,92")

    def test_20_jawaban_ganda_bertentangan_ditolak(self):
        p = self.tulis("j.csv", [["M01", "lulus", ""], ["M01", "gagal", ""]])
        code, _, err = jalan("hitung", str(p))
        self.assertEqual(code, 2)
        self.assertIn("dua kali", err)

    def test_21_file_rusak_kosong_xlsx(self):
        kosong = self.dir / "k.csv"
        kosong.write_text("", encoding="utf-8")
        self.assertEqual(jalan("hitung", str(kosong))[0], 2)
        salah = self.tulis("s.csv", [["a", "b"]], header=("nama", "nilai"))
        code, _, err = jalan("hitung", str(salah))
        self.assertEqual(code, 2)
        self.assertIn("'id' dan 'status'", err)
        x = self.dir / "a.xlsx"
        x.write_bytes(b"PK\x03\x04")
        code, _, err = jalan("hitung", str(x))
        self.assertEqual(code, 2)
        self.assertIn("CSV", err)
        self.assertEqual(jalan("hitung", str(self.dir / "tidakada.csv"))[0], 2)

    def test_22_id_tidak_dikenal_dan_status_aneh(self):
        p = self.tulis("j.csv", [["X99", "lulus", ""], ["M01", "mungkin", ""]])
        code, out, _ = jalan("hitung", str(p))
        self.assertEqual(code, 0)
        self.assertIn("X99", out)
        self.assertIn("tidak dikenal", out)
        p2 = self.tulis("j2.csv", [["X99", "lulus", ""]])
        self.assertEqual(jalan("hitung", str(p2))[0], 2)

    def test_23_json_input_dan_output(self):
        p = self.dir / "j.json"
        p.write_text(json.dumps({"jawaban": {"S01": "lulus", "S02": {"status": "gagal", "catatan": "a"}},
                                 "belanja": {"shopee": "1,5jt"}}), encoding="utf-8")
        code, out, err = jalan("hitung", str(p), "--json")
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["platform"]["shopee"]["belanja"], "1500000")
        self.assertEqual(d["platform"]["shopee"]["status"], "bukti_kurang")
        rusak = self.dir / "r.json"
        rusak.write_text("{rusak", encoding="utf-8")
        self.assertEqual(jalan("hitung", str(rusak))[0], 2)

    def test_24_belanja_salah(self):
        p = self.tulis("j.csv", [["M01", "lulus", ""]])
        self.assertEqual(jalan("hitung", str(p), "--belanja", "meta=-5")[0], 2)
        self.assertEqual(jalan("hitung", str(p), "--belanja", "friendster=5")[0], 2)
        self.assertEqual(jalan("hitung", str(p), "--belanja", "meta")[0], 2)
        self.assertEqual(jalan("hitung", str(p), "--mulai", "28-09-2026")[0], 2)


class UjiAngka(unittest.TestCase):
    def test_25_parse_angka_indonesia(self):
        for teks, harap in (("150rb", 150000), ("Rp 1,5 jt", 1500000), ("3.000.000", 3000000),
                            ("1,250,000", 1250000), ("1.234,5", Decimal("1234.5")), ("10,5", Decimal("10.5")),
                            ("2 juta", 2000000), ("750k", 750000)):
            self.assertEqual(m.angka(teks), Decimal(harap), teks)
        for buruk in ("", "abc", "-100", "NaN"):
            with self.assertRaises(m.InputSalah):
                m.angka(buruk)

    def test_26_roas_impas_dihitung_independen(self):
        r = m.roas_impas(Decimal(149000), Decimal(78000), Decimal(12), Decimal(2000))
        biaya = Fraction(149000 * 12, 100)            # 17880 persis
        laba = 149000 - 78000 - biaya - 2000          # 51120
        self.assertEqual(r["laba_kotor"], Decimal(int(laba)))
        roas = Fraction(149000) / laba                # 2,9147 -> dibulatkan ke atas 2,92
        self.assertEqual(r["roas_impas"], Decimal("2.92"))
        self.assertGreaterEqual(Fraction(str(r["roas_impas"])), roas)

    def test_27_roas_impas_rugi_dan_cli(self):
        with self.assertRaises(m.InputSalah):
            m.roas_impas(Decimal(100000), Decimal(95000), Decimal(10))
        code, out, _ = jalan("roas-impas", "--harga", "150rb", "--modal", "80rb", "--biaya-persen", "10,5",
                             "--biaya-lain", "2.500")
        self.assertEqual(code, 0)
        self.assertIn("Rp 51.750", out)
        self.assertIn("2,90", out)
        self.assertEqual(jalan("roas-impas", "--harga", "0", "--modal", "1")[0], 2)
        self.assertEqual(jalan("roas-impas", "--harga", "1000", "--modal", "1", "--biaya-persen", "100")[0], 2)

    def test_28_templat_dan_daftar(self):
        code, out, _ = jalan("templat", "--platform", "tokopedia")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("id,status,catatan"))
        self.assertIn("TS01", out)
        self.assertNotIn("M01", out)
        code, out, _ = jalan("daftar", "--platform", "google")
        self.assertIn("[G15]", out)
        self.assertEqual(jalan("daftar", "--platform", "friendster")[0], 2)

    def test_29_label_skor_batas(self):
        self.assertEqual(m.label_skor(Decimal(85)), "Sehat")
        self.assertEqual(m.label_skor(Decimal("84.99")), "Cukup, ada yang perlu dibenahi")
        self.assertEqual(m.label_skor(Decimal(50)), "Perlu perbaikan")
        self.assertEqual(m.label_skor(Decimal("49.9")), "Kritis")
        self.assertEqual(m.status_cakupan(Decimal(80)), "final")
        self.assertEqual(m.status_cakupan(Decimal("79.99")), "sementara")
        self.assertEqual(m.status_cakupan(Decimal("59.9")), "bukti_kurang")


if __name__ == "__main__":
    unittest.main(verbosity=1)
