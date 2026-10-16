#!/usr/bin/env python3
"""Uji regresi rapor.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

RAKIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAKIT / "scripts"))
import rapor as r  # noqa: E402


def jalan(isi, *opsi, nama="x.txt", mentah=None):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, nama)
        with open(path, "wb") as f:
            f.write(mentah if mentah is not None else isi.encode("utf-8"))
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            kode = r.main([path, "--json", *opsi])
        return kode, out.getvalue(), err.getvalue()


def blok(i, pel, bot, gagal):
    return "---\nid: %s\nPelanggan: %s\nBot: %s\n#gagal: %s\n" % (i, pel, bot, gagal)


class Uji(unittest.TestCase):
    def test_hitung_dasar(self):
        teks = "".join(blok("A%d" % i, "tanya", "jawab", "lolos") for i in range(8)) + blok("B1", "x", "y", "konteks") + blok("B2", "x", "y", "lupa, panjang") + "---\n"
        k, out, _ = jalan(teks)
        self.assertEqual(k, 0)
        h = json.loads(out)
        self.assertEqual(h["dinilai"], 10)
        self.assertEqual(h["lolos_persen"]["konteks"], 80.0)
        self.assertEqual(h["lolos_persen"]["panjang"], 90.0)
        self.assertEqual(h["percakapan_bersih"], 8)
        self.assertEqual(h["tiga_kesalahan_teratas"][0]["kode"], "konteks")

    def test_kritis_membatasi_nilai_umum(self):
        teks = "".join(blok("A%d" % i, "t", "j", "lolos") for i in range(19)) + blok("Z", "t", "j", "bocor")
        h = json.loads(jalan(teks)[1])
        self.assertEqual(h["lolos_persen"]["bocor"], 95.0)
        self.assertEqual(h["nilai_umum"], "C")
        self.assertEqual(h["kena_kriteria_kritis"], ["bocor"])

    def test_predikat(self):
        self.assertEqual(r.predikat(90, False), "A")
        self.assertEqual(r.predikat(89.9, False), "B")
        self.assertEqual(r.predikat(59, False), "D")
        self.assertEqual(r.predikat(99, True), "B")
        self.assertEqual(r.predikat(100, True), "A")
        self.assertEqual(r.predikat(80, True), "D")

    def test_tren_dari_string_dan_json(self):
        teks = "".join(blok("A%d" % i, "t", "j", "lolos") for i in range(9)) + blok("B", "t", "j", "nada")
        h = json.loads(jalan(teks, "--lama", "nada=95,fakta=100%")[1])
        nada = [k for k in h["kriteria"] if k["kode"] == "nada"][0]
        self.assertEqual(nada["selisih_poin"], -5.0)
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "lama.json")
            with open(p, "w") as f:
                json.dump({"lolos_persen": {"nada": 50}}, f)
            h2 = json.loads(jalan(teks, "--lama", p)[1])
            self.assertEqual([k for k in h2["kriteria"] if k["kode"] == "nada"][0]["selisih_poin"], 40.0)

    def test_samarkan(self):
        s = r.samarkan("Hubungi Bu Rina di 0812-3456-7788 atau rina@mail.com, resi 1234567890123456", ["Wulan"])
        self.assertNotIn("3456", s)
        self.assertNotIn("rina@mail.com", s)
        self.assertNotIn("Rina", s)
        self.assertIn("0812-xxxx-7788", s)
        self.assertNotIn("1234567890123456", s)
        self.assertEqual(r.samarkan("halo Wulan", ["Wulan"]), "halo [nama]")

    def test_contoh_rapor_tersamar(self):
        teks = blok("A", "Saya Bu Rina 0812-3456-7788 tanya", "ok", "fakta") + "---\n"
        out = jalan(teks)[1]
        self.assertNotIn("3456", out)
        self.assertNotIn("Rina", out)

    def test_dugaan_mekanis(self):
        c = {"turn": [["pelanggan", "ada diskon?"], ["bot", "Pasti dijamin! Lihat file json di /home/x. Hubungi 0812-1111-2222"]]}
        d = r.dugaan(c, 700)
        self.assertEqual(set(d), {"janji", "teknis", "bocor"})
        c2 = {"turn": [["pelanggan", "nomor saya 0812-1111-2222"], ["bot", "Baik, saya catat 0812-1111-2222"]]}
        self.assertNotIn("bocor", r.dugaan(c2, 700))
        self.assertIn("panjang", r.dugaan({"turn": [["bot", "x" * 800]]}, 700))
        self.assertNotIn("teknis", r.dugaan({"turn": [["bot", "Sesi konsultasi 60 menit, log kunjungan"]]}, 700))

    def test_belum_dinilai_tidak_dihitung(self):
        teks = blok("A", "t", "j", "lolos") + "---\nid: B\nPelanggan: t\nBot: Pasti sembuh!\n---\n"
        h = json.loads(jalan(teks)[1])
        self.assertEqual(h["dinilai"], 1)
        self.assertEqual(h["belum_dinilai"], 1)
        self.assertTrue(h["dugaan_pada_yang_belum_dinilai"])
        self.assertTrue(any("indikatif" in p for p in h["peringatan"]))

    def test_kode_tak_dikenal(self):
        h = json.loads(jalan(blok("A", "t", "j", "ngaco, nada"))[1])
        self.assertEqual(h["kriteria"][4]["gagal"], 1)
        self.assertTrue(any("tidak dikenal" in p for p in h["peringatan"]))

    def test_csv_digabung_per_id(self):
        csvt = "id,pelanggan,bot,gagal\nA,halo,hai,lolos\nA,harga?,ya,konteks\nB,x,y,\n"
        k, out, _ = jalan(csvt, nama="x.csv")
        h = json.loads(out)
        self.assertEqual(h["percakapan_total"], 2)
        self.assertEqual(h["dinilai"], 1)

    def test_csv_peran_pesan(self):
        csvt = "id,peran,pesan,gagal\nA,Pelanggan,halo,\nA,Bot,hai,nada\n"
        h = json.loads(jalan(csvt, nama="x.csv")[1])
        self.assertEqual(h["kriteria"][4]["gagal"], 1)

    def test_berkas_buruk(self):
        self.assertEqual(jalan("", mentah=b"")[0], 2)
        self.assertEqual(jalan("   \n\n")[0], 2)
        self.assertEqual(jalan("", mentah=b"\xff\xfe\x00\x01garbage")[0] in (0, 2), True)
        k, _, err = jalan("bebas tanpa pemisah")
        self.assertEqual(k, 0)
        k2 = r.main(["/tidak/ada.txt"])
        self.assertEqual(k2, 2)

    def test_blok_agent_ada_penanda(self):
        out = io.StringIO()
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "a.txt")
            with open(p, "w") as f:
                f.write(blok("A", "t", "j", "lolos"))
            with redirect_stdout(out):
                r.main([p])
        self.assertIn("UNTUK AGENT SAJA", out.getvalue())

    def test_nol_dinilai(self):
        h = json.loads(jalan("---\nPelanggan: a\nBot: b\n---\n")[1])
        self.assertEqual(h["dinilai"], 0)
        self.assertIsNone(h["nilai_umum"])


def jalan_nilai(nilai, *opsi):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        kode = r.main(["--nilai", nilai, "--json", *opsi])
    return kode, (json.loads(out.getvalue()) if kode == 0 else None), err.getvalue()


MATRIKS_01 = "P1=lolos; P2=nyambung,panjang; P3=janji,fakta; P4=teknis; P5=konteks; P6=bocor; P7=nada; P8=lolos; P9=lolos; P10=lolos"


class UjiPerKriteria(unittest.TestCase):
    """1.0.2: angka per kriteria dan percakapan bersih wajib dari daftar penilaian per percakapan."""

    def test_data_contoh_01_semua_90_dan_bersih_4(self):
        # Data contoh 01: tiap kriteria gagal tepat di 1 percakapan (berbeda-beda) -> 8 x 90% memang benar;
        # bersih = P1, P8, P9, P10 = 4 (pra-cek Telegram 1.0.1 menulis 5: salah).
        k, h, _ = jalan_nilai(MATRIKS_01)
        self.assertEqual(k, 0)
        self.assertEqual(set(h["lolos_persen"].values()), {90.0})
        self.assertEqual(h["percakapan_bersih"], 4)
        self.assertTrue(h["konsistensi"]["ok"])
        self.assertTrue(h["semua_kriteria_sama_persen"])
        self.assertEqual({c["kode"]: c["gagal_di"] for c in h["kriteria"]}["nyambung"], ["P2"])

    def test_nilai_sama_dengan_berkas(self):
        h_berkas = json.loads(jalan((RAKIT / "examples/data/01-skincare-minggu2.txt").read_text(encoding="utf-8"))[1])
        _, h_nilai, _ = jalan_nilai(MATRIKS_01)
        self.assertEqual(h_berkas["lolos_persen"], h_nilai["lolos_persen"])
        self.assertEqual(h_berkas["percakapan_bersih"], h_nilai["percakapan_bersih"])
        self.assertEqual(h_berkas["nilai_umum"], h_nilai["nilai_umum"])

    def test_kegagalan_beragam_persen_berbeda(self):
        nilai = ("P1=lolos; P2=fakta,nada; P3=nada; P4=lolos; P5=konteks,nada; P6=panjang; "
                 "P7=nada; P8=lolos; P9=teknis; P10=lolos")
        _, h, _ = jalan_nilai(nilai)
        lp = h["lolos_persen"]
        self.assertEqual(lp["nada"], 60.0)
        self.assertEqual(lp["fakta"], 90.0)
        self.assertEqual(lp["nyambung"], 100.0)
        self.assertEqual(lp["konteks"], 90.0)
        self.assertEqual(h["percakapan_bersih"], 4)
        self.assertLessEqual(h["percakapan_bersih"], min(c["lolos"] for c in h["kriteria"]))
        self.assertFalse(h["semua_kriteria_sama_persen"])
        self.assertEqual([c for c in h["kriteria"] if c["kode"] == "nada"][0]["nilai"], "C")

    def test_bersih_tidak_pernah_melebihi_lolos_terendah(self):
        import random
        acak = random.Random(7)
        for _ in range(200):
            n = acak.randint(1, 25)
            butir = []
            for i in range(n):
                g = [k for k in r.KRITERIA if acak.random() < 0.15]
                butir.append("P%d=%s" % (i + 1, ",".join(g) or "lolos"))
            _, h, _ = jalan_nilai("; ".join(butir))
            self.assertTrue(h["konsistensi"]["ok"], h["konsistensi"])
            self.assertLessEqual(h["percakapan_bersih"], min(c["lolos"] for c in h["kriteria"]))
            for c in h["kriteria"]:
                self.assertEqual(c["lolos"] + c["gagal"], n)
                self.assertEqual(c["lolos_persen"], round(100.0 * c["lolos"] / n, 1))

    def test_cek_konsistensi_menangkap_angka_salah(self):
        matriks = [[], ["nyambung", "panjang"], ["janji", "fakta"], ["teknis"], ["konteks"], ["bocor"], ["nada"], [], [], []]
        gagal = {k: 1 for k in r.KRITERIA}
        self.assertEqual(r.cek_konsistensi(10, gagal, 4, matriks), [])
        # Kesalahan pra-cek 1.0.1: "5 dari 10 bersih" padahal daftar penilaian memberi 4.
        self.assertTrue(r.cek_konsistensi(10, gagal, 5, matriks))
        # Bersih melebihi lolos terendah: mustahil.
        self.assertTrue(any("lolos terendah" in m for m in r.cek_konsistensi(10, gagal, 10)))
        # Semua kriteria ditulis 90% padahal nada gagal di 3 percakapan.
        matriks2 = [[], ["nada"], ["nada"], ["nada"], [], [], [], [], [], []]
        self.assertTrue(r.cek_konsistensi(10, {"nada": 1}, 7, matriks2))
        # Tidak bersih lebih banyak dari total kesalahan.
        self.assertTrue(r.cek_konsistensi(10, {"nada": 1, "fakta": 1}, 5))
        self.assertEqual(r.cek_konsistensi(0, {}, 0), [])

    def test_penilaian_buruk_tidak_dihitung_lolos(self):
        k, h, _ = jalan_nilai("P1=lolos; P2=ngaco; P3=; P4=?; tanpa sama dengan; P5=Data pribadi")
        self.assertEqual(k, 0)
        self.assertEqual(h["dinilai"], 2)
        self.assertEqual(h["percakapan_bersih"], 1)
        self.assertEqual(h["lolos_persen"]["bocor"], 50.0)
        teks = " ".join(h["peringatan"])
        self.assertIn("P2", teks)
        self.assertIn("P3", teks)
        self.assertIn("tanpa '='", teks)

    def test_nilai_kosong_dan_tanpa_masukan(self):
        self.assertEqual(jalan_nilai(" ; ")[0], 2)
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(r.main([]), 2)

    def test_blok_agent_angka_siap_salin(self):
        out = io.StringIO()
        with redirect_stdout(out):
            r.main(["--nilai", MATRIKS_01, "--lama", "fakta=100,nada=85"])
        t = out.getvalue()
        self.assertIn("4 dari 10 (40%)", t)
        self.assertIn("lolos 9 dari 10 (90%)", t)
        self.assertIn("cek konsistensi: OK", t)
        self.assertIn("turun 10 poin", t)
        self.assertIn("naik 5 poin", t)
        self.assertIn("kalimat penjelas", t)
        self.assertEqual(r.persen_id(83.3), "83,3%")
        self.assertEqual(r.persen_id(90.0), "90%")

    def test_versi(self):
        self.assertEqual(r.VERSI, "1.0.2")
        self.assertIn("1.0.2", (RAKIT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn("**1.0.2**", (RAKIT / "README.md").read_text(encoding="utf-8"))


class UjiFormatRingkas(unittest.TestCase):
    """1.0.2: contoh format ringkas untuk chat (Telegram) <= 3.000 karakter, tabel <= 3 kolom, tanpa nama skill."""

    def ambil(self, tanda):
        teks = (RAKIT / "examples/06-format-ringkas-chat.md").read_text(encoding="utf-8")
        awal, akhir = "<!-- awal %s -->" % tanda, "<!-- akhir %s -->" % tanda
        self.assertIn(awal, teks)
        return teks.split(awal, 1)[1].split(akhir, 1)[0].strip()

    def test_panjang_dan_bentuk(self):
        import re
        for tanda in ("balasan pertama", "balasan rinci"):
            b = self.ambil(tanda)
            self.assertLessEqual(len(b), 3000, tanda)
            for baris in b.splitlines():
                if baris.strip().startswith("|"):
                    self.assertLessEqual(baris.strip().strip("|").count("|"), 2, baris)
            self.assertIsNone(re.search(r"\b[a-z]+(?:-[a-z0-9]+){2,}\b", b), tanda)
            for kata in ("script", "skrip", "python", ".py", "json", "/home", "--nilai"):
                self.assertNotIn(kata, b.lower())
        self.assertIn("Balas 'rinci'", self.ambil("balasan pertama"))

    def test_angka_contoh_sama_dengan_hitungan(self):
        import re
        _, h, _ = jalan_nilai(MATRIKS_01)
        pendek = {"Fakta": "fakta", "Nyambung": "nyambung", "Konteks": "konteks", "Panjang": "panjang",
                  "Nada": "nada", "Janji": "janji", "Data pribadi": "bocor", "Kata teknis": "teknis"}
        per = {c["kode"]: c for c in h["kriteria"]}
        b = self.ambil("balasan pertama")
        ketemu = 0
        for baris in b.splitlines():
            m = re.match(r"^\|\s*([^|]+?)\s*\|\s*([\d,]+)% \((\d+)/(\d+)\)\s*\|\s*([A-D])\s*\|$", baris.strip())
            if m and m.group(1) in pendek:
                c = per[pendek[m.group(1)]]
                self.assertEqual(float(m.group(2).replace(",", ".")), c["lolos_persen"])
                self.assertEqual((int(m.group(3)), int(m.group(4))), (c["lolos"], c["dinilai"]))
                self.assertEqual(m.group(5), c["nilai"])
                ketemu += 1
        self.assertEqual(ketemu, 8)
        self.assertIn("4 dari 10", b)
        self.assertIn("nilai umum **%s**" % h["nilai_umum"], b)


if __name__ == "__main__":
    unittest.main(verbosity=1)
