#!/usr/bin/env python3
"""Uji regresi cek_risiko.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import cek_risiko as c  # noqa: E402


def jalan(*arg):
    o, e = io.StringIO(), io.StringIO()
    with redirect_stdout(o), redirect_stderr(e):
        k = c.main(list(arg))
    return k, o.getvalue(), e.getvalue()


def tmp_json(obj, mentah=None):
    p = os.path.join(tempfile.mkdtemp(), "r.json")
    with open(p, "w", encoding="utf-8") as f:
        f.write(mentah if mentah is not None else json.dumps(obj))
    return p


class Tes(unittest.TestCase):
    def test_skor_dan_tingkat(self):
        h = c.hitung_risiko([{"nama": "A", "kemungkinan": 2, "dampak": 5},
                             {"nama": "B", "kemungkinan": 5, "dampak": 3},
                             {"nama": "C", "kemungkinan": 1, "dampak": 2}])
        self.assertEqual([(x["nama"], x["skor"], x["tingkat"]) for x in h],
                         [("B", 15, "KRITIS"), ("A", 10, "TINGGI"), ("C", 2, "RENDAH")])

    def test_batas_tingkat(self):
        self.assertEqual([c.tingkat(s) for s in (1, 4, 5, 9, 10, 14, 15, 25)],
                         ["RENDAH", "RENDAH", "SEDANG", "SEDANG", "TINGGI", "TINGGI", "KRITIS", "KRITIS"])

    def test_respons(self):
        self.assertEqual(c.respons(2, 2, 4)[1], "Tidak")
        self.assertEqual(c.respons(1, 4, 4)[1], "Ya, pertimbangkan")  # jarang tapi berat
        self.assertEqual(c.respons(2, 5, 10)[1], "Ya, pertimbangkan")
        self.assertEqual(c.respons(4, 5, 20)[1], "Ya, setelah dikurangi")
        self.assertEqual(c.respons(4, 3, 12)[1], "Tidak perlu")
        # kerugian melebihi dana darurat -> dianggap besar
        self.assertEqual(c.respons(2, 3, 6, 50_000_000, 20_000_000)[1], "Ya, pertimbangkan")
        self.assertEqual(c.respons(2, 3, 6, 10_000_000, 20_000_000)[1], "Tidak perlu")

    def test_dana(self):
        o = c.hitung_dana({"sewa": 3_000_000, "gaji": 8_500_000, "listrik": 750_000}, 3, 10_000_000)
        self.assertEqual(o["biaya_tetap_bulanan"], 12_250_000)
        self.assertEqual(o["target"], 36_750_000)
        self.assertEqual(o["kekurangan"], 26_750_000)
        self.assertEqual(o["tercukupi_bulan"], 0.8)
        self.assertEqual(c.hitung_dana({"a": 1}, 6, 99)["kekurangan"], 0)

    def test_parse_biaya(self):
        self.assertEqual(c.parse_biaya("Sewa=3.000.000, Gaji=8500000"), {"Sewa": 3000000, "Gaji": 8500000})
        with self.assertRaises(ValueError):
            c.parse_biaya("Sewa=abc")
        with self.assertRaises(ValueError):
            c.parse_biaya("Sewa")

    def test_rp(self):
        self.assertEqual(c.rp(1250000), "Rp1.250.000")
        self.assertEqual(c.rp(0), "Rp0")

    def test_data_rusak(self):
        for bad in ([{"nama": "A", "kemungkinan": 0, "dampak": 3}],
                    [{"nama": "A", "kemungkinan": 6, "dampak": 3}],
                    [{"nama": "A", "kemungkinan": "tinggi", "dampak": 3}],
                    [{"nama": "", "kemungkinan": 1, "dampak": 1}],
                    [{"nama": "A", "kemungkinan": True, "dampak": 1}],
                    [{"nama": "A", "kemungkinan": 1, "dampak": 1, "kerugian_rp": -5}],
                    [], "bukan list"):
            with self.assertRaises(ValueError):
                c.hitung_risiko(bad)
        with self.assertRaises(ValueError):
            c.hitung_dana({"a": -1}, 3)
        with self.assertRaises(ValueError):
            c.hitung_dana({}, 3)
        with self.assertRaises(ValueError):
            c.hitung_dana({"a": 1}, 0)

    def test_cli(self):
        k, o, _ = jalan("risiko", tmp_json([{"nama": "Kebakaran", "kemungkinan": 2, "dampak": 5}]))
        self.assertEqual(k, 0)
        self.assertIn("| 1 | Kebakaran | 2 | 5 | 10 | TINGGI |", o)
        k, o, _ = jalan("dana", "--biaya", "Sewa=2000000,Gaji=4000000", "--bulan", "6", "--kas", "10000000")
        self.assertEqual(k, 0)
        self.assertIn("Rp6.000.000", o)
        self.assertIn("Rp36.000.000", o)
        self.assertIn("Kekurangan: Rp26.000.000", o)

    def test_biaya_dobel_ditolak(self):
        with self.assertRaises(ValueError) as e:
            c.parse_biaya("Gaji=1000000,gaji=2000000")
        self.assertIn("dobel", str(e.exception))
        k, _, err = jalan("dana", "--biaya", "Gaji=1000000,Gaji=2000000")
        self.assertEqual(k, 2)
        self.assertIn("dobel", err)

    def test_parse_angka(self):
        self.assertEqual(c.parse_angka("3000000"), 3000000)
        self.assertEqual(c.parse_angka("3.000.000"), 3000000)
        self.assertEqual(c.parse_angka("Rp 3.000.000"), 3000000)
        self.assertEqual(c.parse_angka("0"), 0)
        for bad in ("3000000.00", "3.5", "3,5", "3,000,000", "3.00", "1.2345", "abc", "", "-5"):
            with self.assertRaises(ValueError):
                c.parse_angka(bad)
        with self.assertRaises(ValueError):
            c.parse_biaya("Sewa=3000000.00")

    def test_tidak_bisa_diasuransikan(self):
        h = c.hitung_risiko([
            {"nama": "Akun marketplace dibekukan", "kemungkinan": 2, "dampak": 4, "bisa_diasuransikan": False},
            {"nama": "Kebakaran", "kemungkinan": 2, "dampak": 5}])
        d = {x["nama"]: x for x in h}
        self.assertNotIn("Ya", d["Akun marketplace dibekukan"]["perlu_asuransi"])
        self.assertIn("mitigasi lain", d["Akun marketplace dibekukan"]["perlu_asuransi"])
        self.assertEqual(d["Kebakaran"]["perlu_asuransi"], "Ya, pertimbangkan")
        with self.assertRaises(ValueError):
            c.hitung_risiko([{"nama": "A", "kemungkinan": 1, "dampak": 1, "bisa_diasuransikan": "tidak"}])

    def test_jarang_tapi_berat_bukan_terima(self):
        h = c.hitung_risiko([{"nama": "Gempa", "kemungkinan": 1, "dampak": 4}])[0]
        self.assertEqual(h["skor"], 4)
        self.assertEqual(h["perlu_asuransi"], "Ya, pertimbangkan")
        h = c.hitung_risiko([{"nama": "X", "kemungkinan": 1, "dampak": 2, "kerugian_rp": 50000000}], 10000000)[0]
        self.assertEqual(h["perlu_asuransi"], "Ya, pertimbangkan")
        h = c.hitung_risiko([{"nama": "X", "kemungkinan": 1, "dampak": 2}])[0]
        self.assertEqual(h["perlu_asuransi"], "Tidak")

    def test_cicilan(self):
        o = c.hitung_dana({"a": 6_000_000}, 3, 10_000_000, 6)
        self.assertEqual(o["kekurangan"], 8_000_000)
        self.assertEqual(o["cicilan"], 1_333_334)  # dibulatkan ke atas
        k, out, _ = jalan("dana", "--biaya", "a=6.000.000", "--bulan", "3", "--kas", "10.000.000", "--cicil", "6")
        self.assertEqual(k, 0)
        self.assertIn("Cicilan menabung: Rp1.333.334 per bulan selama 6 bulan", out)
        self.assertIn("cukup 1,7 bulan", out)
        with self.assertRaises(ValueError):
            c.hitung_dana({"a": 1}, 3, None, 6)
        with self.assertRaises(ValueError):
            c.hitung_dana({"a": 1}, 3, 5, 0)

    def test_pesan_indonesia_dan_nol(self):
        k, _, err = jalan("dana", "--biaya", "a=1000", "--kas", "5000000.50")
        self.assertEqual(k, 2)
        self.assertIn("tidak jelas", err)
        k, out, _ = jalan("dana", "--biaya", "a=0", "--kas", "100")
        self.assertEqual(k, 0)
        self.assertNotIn("None", out)

    def test_cli_dana_opsi(self):
        j = tmp_json([{"nama": "X", "kemungkinan": 2, "dampak": 3, "kerugian_rp": 50000000}])
        k, out, _ = jalan("risiko", j, "--dana", "10.000.000")
        self.assertIn("Ya, pertimbangkan", out)

    def test_cli_berkas_rusak(self):
        k, _, e = jalan("risiko", tmp_json(None, "{rusak"))
        self.assertEqual(k, 2)
        self.assertIn("tidak valid", e)
        k, _, e = jalan("risiko", "/tidak/ada.json")
        self.assertEqual(k, 2)

    # ---- v1.0.2 ----
    def test_bpjs_otomatis_dan_eksplisit(self):
        h = {x["nama"]: x for x in c.hitung_risiko([
            {"nama": "Pegawai cedera angkat karung", "kemungkinan": 2, "dampak": 2},
            {"nama": "Karyawan cedera kerja", "kemungkinan": 3, "dampak": 3},
            {"nama": "Insiden di gudang", "kemungkinan": 2, "dampak": 4, "kategori": "bpjs"},
            {"nama": "Pelanggan terpeleset dan cedera", "kemungkinan": 2, "dampak": 4},
            {"nama": "Pemilik sakit", "kemungkinan": 2, "dampak": 3},
            {"nama": "Mekanik senior keluar/sakit", "kemungkinan": 3, "dampak": 4},
            {"nama": "Karyawan cedera (diubah)", "kemungkinan": 2, "dampak": 2, "kategori": "umum"},
        ])}
        for n in ("Pegawai cedera angkat karung", "Karyawan cedera kerja", "Insiden di gudang"):
            self.assertTrue(h[n]["bpjs"], n)
            self.assertEqual(h[n]["perlu_asuransi"], c.LABEL_BPJS)
            self.assertIn("BPJS", h[n]["respons"])
            self.assertNotIn(h[n]["perlu_asuransi"], ("Tidak", "Tidak perlu"))
        for n in ("Pelanggan terpeleset dan cedera", "Pemilik sakit",
                  "Mekanik senior keluar/sakit", "Karyawan cedera (diubah)"):
            self.assertFalse(h[n]["bpjs"], n)
            self.assertNotEqual(h[n]["perlu_asuransi"], c.LABEL_BPJS)
        with self.assertRaises(ValueError):
            c.hitung_risiko([{"nama": "A", "kemungkinan": 1, "dampak": 1, "kategori": "lain"}])

    def test_bpjs_menang_atas_tidak_bisa_diasuransikan_dan_cli(self):
        j = tmp_json([{"nama": "Kasir cedera", "kemungkinan": 1, "dampak": 1, "bisa_diasuransikan": False}])
        k, o, _ = jalan("risiko", j)
        self.assertEqual(k, 0)
        self.assertIn("BPJS: kewajiban pemberi kerja", o)
        self.assertNotIn("| Terima", o)

    def test_nama_dengan_pipa_tidak_merusak_tabel(self):
        k, o, _ = jalan("risiko", tmp_json([{"nama": "Listrik | padam\nlama", "kemungkinan": 3, "dampak": 2}]))
        baris = [b for b in o.splitlines() if b.startswith("| 1 |")]
        self.assertEqual(len(baris), 1)
        self.assertEqual(baris[0].count("|"), 9)
        self.assertIn("Listrik / padam lama", baris[0])

    def test_cukup_bulan_bulat_setengah_ke_atas(self):
        self.assertEqual(c.hitung_dana({"a": 5_000_000}, 3, 1_250_000)["tercukupi_bulan"], 0.3)  # 0,25 -> 0,3
        self.assertEqual(c.hitung_dana({"a": 3_000_000}, 3, 5_000_000)["tercukupi_bulan"], 1.7)
        self.assertEqual(c.hitung_dana({"a": 3_000_000}, 3, 0)["tercukupi_bulan"], 0.0)
        k, out, _ = jalan("dana", "--biaya", "a=5000000", "--kas", "1250000")
        self.assertIn("cukup 0,3 bulan", out)

    def test_kas_cukup_tanpa_cicilan_nol(self):
        k, out, _ = jalan("dana", "--biaya", "a=1000000", "--bulan", "3", "--kas", "5000000", "--cicil", "6")
        self.assertEqual(k, 0)
        self.assertNotIn("Cicilan menabung: Rp0", out)
        self.assertIn("tidak perlu cicilan", out)

    def test_nama_biaya_kosong_dan_koma_desimal(self):
        for bad in ("=3000000", " =5"):
            with self.assertRaises(ValueError) as e:
                c.parse_biaya(bad)
            self.assertIn("kosong", str(e.exception))
        with self.assertRaises(ValueError) as e:
            c.parse_biaya("Sewa=3.000.000,00")
        self.assertIn("koma", str(e.exception))
        k, _, err = jalan("dana", "--biaya", "Sewa=3.000.000,00")
        self.assertEqual(k, 2)
        self.assertIn("koma", err)

    def test_json_dengan_bom(self):
        p = os.path.join(tempfile.mkdtemp(), "bom.json")
        with open(p, "wb") as f:
            f.write(b"\xef\xbb\xbf" + json.dumps([{"nama": "Kebakaran", "kemungkinan": 2, "dampak": 5}]).encode())
        k, o, _ = jalan("risiko", p)
        self.assertEqual(k, 0)
        self.assertIn("Kebakaran", o)


    # ---- v1.0.3: tampilan chat ----
    def _data_chat(self, n=9):
        return [{"nama": f"Risiko {i}", "kemungkinan": 1 + i % 5, "dampak": 1 + (i * 2) % 5} for i in range(n)]

    def test_chat_tanpa_tabel_dan_ringkasan_tiga_teratas(self):
        j = tmp_json(self._data_chat(6))
        k, o, _ = jalan("risiko", j, "--tampilan", "chat")
        self.assertEqual(k, 0)
        self.assertNotIn("|", o)
        self.assertNotIn("---", o)
        self.assertTrue(o.startswith("Tiga prioritas teratas:"))
        # ringkasan memuat tiga risiko skor tertinggi sama dengan urutan tabel
        h = c.hitung_risiko(self._data_chat(6))
        ringkas = o.split("Rincian per risiko:")[0]
        for i, r in enumerate(h[:3], 1):
            self.assertIn(f"{i}. {r['nama']} \u00b7 {r['tingkat']} (skor {r['skor']})", ringkas)
        self.assertNotIn(h[3]["nama"], ringkas)
        # tiap risiko ada keenam butir: nama, tingkat, dampak, langkah, perlindungan, prioritas
        for kata in ("Dampak kira-kira:", "Langkah pencegahan:", "Perlindungan/asuransi:", "Prioritas:"):
            self.assertEqual(o.count(kata), 6, kata)

    def test_chat_angka_sama_dengan_tabel_dan_pesan_dibagi(self):
        data = self._data_chat(9)
        j = tmp_json(data)
        _, tabel, _ = jalan("risiko", j)
        _, chat, _ = jalan("risiko", j, "--tampilan", "chat")
        for r in c.hitung_risiko(data):
            self.assertIn(f"skor {r['skor']} = kemungkinan {r['kemungkinan']} x dampak {r['dampak']}", chat)
            self.assertIn(r["perlu_asuransi"], chat)
            self.assertIn(r["respons"], chat)
        self.assertEqual(chat.count("<<< PESAN BERIKUTNYA"), 2)  # 9 blok = 4 + 4 + 1
        for bagian in chat.split(c.PENANDA_PESAN):
            self.assertLess(len(bagian), 3000)
        # 4 blok atau kurang: tidak ada penanda
        _, kecil, _ = jalan("risiko", tmp_json(self._data_chat(4)), "--tampilan", "chat")
        self.assertNotIn("PESAN BERIKUTNYA", kecil)

    def test_chat_kerugian_rupiah_dan_bpjs_dan_istilah(self):
        j = tmp_json([{"nama": "Kebakaran", "kemungkinan": 2, "dampak": 5, "kerugian_rp": 80000000},
                      {"nama": "Karyawan cedera kerja", "kemungkinan": 3, "dampak": 3}])
        k, o, _ = jalan("risiko", j, "--tampilan", "chat")
        self.assertIn("perkiraan rugi Rp80.000.000", o)
        self.assertIn("BPJS: kewajiban pemberi kerja", o)
        self.assertIn("JKK/jaminan kecelakaan kerja", o)  # istilah dijelaskan
        self.assertIn("setara sekitar 1 bulan biaya tetap", o)

    def test_chat_input_rusak_tetap_ditolak_jelas(self):
        k, _, e = jalan("risiko", tmp_json([{"nama": "A", "kemungkinan": 9, "dampak": 1}]), "--tampilan", "chat")
        self.assertEqual(k, 2)
        self.assertIn("tidak valid", e)
        with self.assertRaises(SystemExit):
            with redirect_stderr(io.StringIO()):
                c.main(["risiko", "x.json", "--tampilan", "lain"])


if __name__ == "__main__":
    unittest.main()
