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
        p = SINI / "examples" / "uji-pembuat-01-jawaban-toko-fashion-shopee.csv"
        jw, _, _ = m.baca_jawaban(p)
        h = m.hitung(jw)
        skor, cak = skor_manual("shopee", {k: v[0] for k, v in jw.items()})
        self.assertEqual(m.satu_desimal(h["platform"]["shopee"]["skor"]), m.satu_desimal(bulat1(skor)))
        self.assertEqual(m.satu_desimal(h["platform"]["shopee"]["cakupan"]), m.satu_desimal(bulat1(cak)))
        self.assertEqual(str(m.satu_desimal(h["platform"]["shopee"]["skor"])), "41.3")

    def test_06_contoh_meta_dan_google_cocok_manual(self):
        for nama, plat in (("uji-pembuat-02-jawaban-klinik-kecantikan-meta.csv", "meta"),
                           ("uji-pembuat-03-jawaban-kursus-online-google.csv", "google")):
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


class UjiRevisi101(unittest.TestCase):
    """Regresi dari uji independen v1.0.0 (examples/HASIL-UJI.md)."""

    def test_30_roas_laba_sangat_kecil_tidak_crash(self):
        code, out, err = jalan("roas-impas", "--harga", "100000", "--modal", "99999,6")
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)
        self.assertIn("kurang dari Rp1", err)

    def test_31_roas_laba_dibulatkan_ke_bawah(self):
        with self.assertRaises(m.InputSalah):   # laba 0,5 -> ke bawah 0 -> ditolak (dulu naik jadi 1)
            m.roas_impas(Decimal(100000), Decimal(60000), Decimal("33.3333"), Decimal("6666.5"))
        r = m.roas_impas(Decimal(100000), Decimal("50000.7"), Decimal(0), Decimal(0))
        self.assertEqual(r["laba_kotor"], Decimal(49999))        # 49.999,3 -> 49.999
        self.assertEqual(r["roas_impas"], Decimal("2.01"))       # 2,00004 -> ke atas

    def test_32_tidak_berlaku_tanpa_syarat_jadi_tidak_tahu(self):
        cek, _ = m.muat_cek()
        jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == "meta"}
        jw["M04"] = ("tidak_berlaku", "")      # akses akun selalu berlaku
        h = m.hitung(jw)
        self.assertTrue(any("M04" in w and "selalu berlaku" in w for w in h["peringatan"]))
        self.assertIn("M04", [c["id"] for c in h["cek_dulu"]])
        self.assertLess(h["platform"]["meta"]["cakupan"], 100)

    def test_33_kritis_tidak_berlaku_batasi_label(self):
        cek, _ = m.muat_cek()
        jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == "meta"}
        jw["M01"] = ("tidak_berlaku", "")      # kritis, syaratnya ada (iklan ke WA)
        h = m.hitung(jw)
        x = h["platform"]["meta"]
        self.assertEqual(x["skor"], 100)
        self.assertNotEqual(m.label_platform(x), "Sehat")
        self.assertNotEqual(m.label_platform(h["gabungan"]), "Sehat")
        self.assertTrue(any("KRITIS" in w and "M01" in w for w in h["peringatan"]))
        code, out, _ = jalan_jawaban(jw)
        self.assertNotIn("(Sehat)", out)

    def test_34_banyak_tidak_berlaku_maksimal_sementara(self):
        cek, _ = m.muat_cek()
        jw = {i: (("tidak_berlaku" if c["tidak_berlaku_jika"] else "lulus"), "")
              for i, c in cek.items() if c["platform"] == "meta"}
        # Semua syarat tidak_berlaku Meta dipakai: sisa bobot berlaku 41/62 = 66% -> masih final
        self.assertEqual(m.hitung(jw)["platform"]["meta"]["status"], "final")
        lama = m.BATAS_RASIO_BERLAKU
        try:
            m.BATAS_RASIO_BERLAKU = Decimal("0.7")   # simulasikan rasio di bawah batas
            h = m.hitung(jw)
        finally:
            m.BATAS_RASIO_BERLAKU = lama
        self.assertEqual(h["platform"]["meta"]["status"], "sementara")
        self.assertTrue(any("separuh" in w for w in h["peringatan"]))

    def test_35_bukti_kurang_tanpa_label_mutu(self):
        jw = {"S01": ("gagal", ""), "S02": ("lulus", "")}
        h = m.hitung(jw)
        x = h["platform"]["shopee"]
        self.assertEqual(x["status"], "bukti_kurang")
        self.assertEqual(m.label_platform(x), "Bukti belum cukup")
        code, out, _ = jalan_jawaban(jw)
        self.assertIn("BUKTI BELUM CUKUP", out)
        for lab in ("(Sehat)", "(Kritis)", "(Perlu perbaikan)", "(Cukup"):
            self.assertNotIn(lab, out)
        code, out, _ = jalan_jawaban(jw, "--json")
        d = json.loads(out)
        self.assertIsNone(d["platform"]["shopee"]["skor"])
        self.assertEqual(d["platform"]["shopee"]["label"], "Bukti belum cukup")
        self.assertEqual(d["versi"], "1.0.1")

    def test_36_anggaran_tidak_dinaikkan_sebelum_batas_untung(self):
        cek, _ = m.muat_cek()
        for plat, anak, induk in (("shopee", "S07", "S06"), ("tiktok", "T08", "T09"),
                                  ("tiktokshop", "TS05", "TS04")):
            jw = {i: ("lulus", "") for i, c in cek.items() if c["platform"] == plat}
            jw[anak] = ("gagal", "")
            jw[induk] = ("sebagian", "")
            h = m.hitung(jw)
            ids = [x["id"] for x in h["prioritas"]]
            self.assertLess(ids.index(induk), ids.index(anak), plat)
            self.assertTrue(any(anak in w and induk in w for w in h["peringatan"]))

    def test_37_fakta_platform_diperbarui(self):
        cek, _ = m.muat_cek()
        for i in ("M22", "T18"):
            self.assertEqual(cek[i]["kategori"], "pelacakan")
            self.assertIn("event_id", cek[i]["lulus_jika"])
            self.assertTrue(cek[i]["tidak_berlaku_jika"])
        self.assertNotIn("pilih orang yang tinggal di lokasi", cek["M08"]["perbaikan"])
        self.assertIn("baru-baru ini", cek["M08"]["perbaikan"])
        for i in ("G15", "G16"):
            self.assertIn("Performance Max", cek[i]["tidak_berlaku_jika"])
            self.assertIn("Performance Max", cek[i]["lulus_jika"])
        self.assertIn("10x", cek["T08"]["lulus_jika"])
        self.assertIn("T09", cek["T08"]["perbaikan"])
        self.assertIn("jangan perluas lokasi", cek["M18"]["perbaikan"])

    def test_38_alias_gmvmax(self):
        code, _, err = jalan("templat", "--platform", "gmvmax")
        self.assertEqual(code, 2)
        self.assertIn("shopee atau tiktokshop", err)
        code, out, _ = jalan("templat", "--platform", "shopee-gmvmax")
        self.assertEqual(code, 0)
        self.assertIn("S01", out)

    def test_39_banding_roas_aktual_vs_impas(self):
        # Kasus uji OpenClaw 2026-10-01: ROAS 2,3 dari pengguna di bawah impas 2,66 -> RUGI
        r = m.roas_impas(Decimal(189000), Decimal(95000), Decimal(12))
        self.assertEqual(r["roas_impas"], Decimal("2.66"))
        b = {x["roas"]: x for x in m.banding_roas(r, [Decimal("2.3"), Decimal("2"), Decimal("2.65"), Decimal("3")])}
        self.assertEqual(b[Decimal("2.3")]["status"], "RUGI")
        # independen: 189000/2,3 = 82173,91 -> 82174; laba 71320 - 82173,91 = -10853,91 -> -10854
        self.assertEqual(b[Decimal("2.3")]["biaya_iklan_per_pesanan"], Decimal(82174))
        self.assertEqual(b[Decimal("2.3")]["laba_setelah_iklan_per_pesanan"], Decimal(-10854))
        self.assertEqual(b[Decimal("2")]["laba_setelah_iklan_per_pesanan"], Decimal(-23180))
        self.assertEqual(b[Decimal("2.65")]["status"], "RUGI")   # 189000/2,65 = 71320,75 > 71320
        self.assertEqual(b[Decimal("3")]["status"], "UNTUNG")
        r2 = m.roas_impas(Decimal(100000), Decimal(50000))
        self.assertEqual(m.banding_roas(r2, [Decimal(2)])[0]["status"], "IMPAS")
        code, out, _ = jalan("roas-impas", "--harga", "189rb", "--modal", "95rb", "--biaya-persen", "12",
                             "--roas-aktual", "2,3")
        self.assertEqual(code, 0)
        self.assertIn("ROAS 2,3 vs impas 2,66: RUGI", out)
        self.assertEqual(jalan("roas-impas", "--harga", "189rb", "--modal", "95rb", "--roas-aktual", "0")[0], 2)


def jalan_jawaban(jw, *extra):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "j.csv"
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "status", "catatan"])
            for k, (s, c) in jw.items():
                w.writerow([k, s, c])
        return jalan("hitung", str(p), *extra)


if __name__ == "__main__":
    unittest.main(verbosity=1)
