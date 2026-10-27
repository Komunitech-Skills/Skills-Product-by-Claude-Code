#!/usr/bin/env python3
"""Uji regresi rapor.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import json
import os
import sys
import tempfile
import unittest
from decimal import ROUND_HALF_UP, Decimal
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
        self.assertIn("[nomor]", s)
        self.assertNotIn("7788", s)  # 1.0.3: 4 digit akhir juga ditutup
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
                harap = Decimal(100 * c["lolos"]) / Decimal(n)
                self.assertEqual(c["lolos_persen"], float(harap.quantize(Decimal("0.1"), ROUND_HALF_UP)))

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
        self.assertEqual(r.VERSI, "1.0.3")
        self.assertIn("1.0.3", (RAKIT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn("**1.0.3**", (RAKIT / "README.md").read_text(encoding="utf-8"))
        _, h, _ = jalan_nilai("P1=lolos")
        self.assertEqual(h["versi"], "1.0.3")


class UjiFormatRingkas(unittest.TestCase):
    """Contoh format ringkas untuk chat (Telegram): <= 3.000 karakter, tabel <= 3 kolom, tanpa nama skill.
    1.0.3: contoh memakai data 02 (persen berbeda-beda) dan lolos cek_balasan."""

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
        _, h, _ = jalan_nilai(MATRIKS_02, "--tahap", "bulan2+", "--lama-jawaban", LAMA_02)
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
        self.assertRegex(b, r"(?<![\d.,])7 dari 12(?!\d|[.,]\d)")  # angka utuh, bukan "17 dari 120"
        self.assertIn("nilai umum **%s**" % h["nilai_umum"], b)
        self.assertIn(h["baris_tren"], b)
        self.assertGreater(len(set(h["lolos_persen"].values())), 1)  # contoh tidak lagi "semua 90%"

    def test_contoh_lolos_cek_balasan(self):
        _, h, _ = jalan_nilai(MATRIKS_02, "--tahap", "bulan2+", "--lama-jawaban", LAMA_02)
        cs = r.parse_teks((RAKIT / "examples/data/02-klinik-bulan2.txt").read_text(encoding="utf-8"), set(), [])
        nomor = [m.group(0) for c in cs for _, t in c["turn"] for m in r.RE_HP.finditer(t)]
        self.assertEqual(r.cek_balasan(self.ambil("balasan pertama"), h, r.nama_terdeteksi(cs), nomor), [])


MATRIKS_02 = ("P1=lolos; P2=lolos; P3=fakta,janji; P4=lolos; P5=fakta,janji; P6=lolos; P7=lolos; P8=konteks; "
              "P9=lolos; P10=lolos; P11=bocor; P12=teknis")
LAMA_02 = ("Rapor minggu lalu: fakta 100%, nyambung 90%, ingat konteks 85%, panjang 95%, nada 90%, janji 100%, "
           "data pribadi 100%, teknis 90%.")


def draf_baik(h, ekstra=""):
    """Draf minimal yang benar untuk hitungan h; tes menyisipkan satu kesalahan lewat ekstra."""
    pendek = {"fakta": "Fakta", "nyambung": "Nyambung", "konteks": "Konteks", "panjang": "Panjang", "nada": "Nada",
              "janji": "Janji", "bocor": "Data pribadi", "teknis": "Kata teknis"}
    baris = ["**Rapor bot minggu ini:** %d percakapan dinilai, %d dari %d bersih." % (h["dinilai"], h["percakapan_bersih"], h["dinilai"]),
             "", "| Kriteria | Lolos | Nilai |", "|---|---|---|"]
    for c in h["kriteria"]:
        baris.append("| %s | %s (%d/%d) | %s |" % (pendek[c["kode"]], r.persen_id(c["lolos_persen"]), c["lolos"], c["dinilai"], c["nilai"]))
    baris += ["", h["baris_tren"], "", ekstra, "", "Mau rincian per percakapan dan cara cek tiap PR? Balas 'rinci'."]
    return "\n".join(baris)


class Uji103(unittest.TestCase):
    """1.0.3: aturan pra-cek Telegram dijadikan pemeriksaan draf + regresi per aturan."""

    def setUp(self):
        _, self.h, _ = jalan_nilai(MATRIKS_02, "--lama-jawaban", LAMA_02)

    def masalah(self, ekstra="", teks=None, nama=("Sari", "Rina"), nomor=("0813-1111-2222",)):
        return r.cek_balasan(teks if teks is not None else draf_baik(self.h, ekstra), self.h, nama, nomor)

    def test_draf_baik_lolos(self):
        self.assertEqual(self.masalah(), [])

    # Aturan 1: tanpa nama/inisial pelanggan di mana pun, termasuk pertanyaan & asumsi.
    def test_nama_di_pertanyaan_ditolak(self):
        m = self.masalah("**Asumsi:** minggu 2-4. Pertanyaan: (1) Apakah pesanan Sari sudah dikirim?")
        self.assertTrue(any("Sari" in x for x in m), m)

    def test_nama_di_asumsi_huruf_kecil_ditolak(self):
        self.assertTrue(self.masalah("**Asumsi:** keluhan rina dianggap selesai."))

    def test_inisial_dan_sapaan_ditolak(self):
        self.assertTrue(any("inisial" in x for x in self.masalah("Pertanyaan: (1) Kak S. sudah dihubungi?")))
        self.assertTrue(any("sapaan" in x for x in self.masalah("Pertanyaan: (1) Bu Hartini mau refund?", nama=())))

    def test_pelanggan_di_p_nomor_boleh(self):
        self.assertEqual(self.masalah("Pertanyaan: (1) Pelanggan di P3 sudah dihubungi staf?"), [])

    # Aturan 3: a/n (atas nama).
    def test_atas_nama_disamarkan_dan_ditolak_di_draf(self):
        self.assertEqual(r.samarkan("transfer a/n Budi Santoso, atau a.n. Rina; atas nama: Dewi"),
                         "transfer a/n [nama], atau a.n. [nama]; atas nama [nama]")
        self.assertTrue(any("a/n" in x for x in self.masalah("Rekening a/n Joko belum dicek.", nama=())))
        self.assertEqual(self.masalah("Tulis 'a/n [nama]' saja."), [])
        self.assertEqual(r.bersih_nama("a/n Budi Santoso"), "Budi Santoso")
        cs = r.parse_teks("Pelanggan (Sari, 0813-1111-2222): transfer a/n Joko Widodo sudah\nBot: ok\n", set(), [])
        nama = r.nama_terdeteksi(cs)
        for n in ("Sari", "Joko", "Widodo"):
            self.assertIn(n, nama)

    def test_kode_berisi_nama_dibuang(self):
        k, h, _ = jalan_nilai("P1 (Sari)=fakta; P2 a/n Budi=lolos")
        self.assertEqual(k, 0)
        self.assertEqual([c["gagal_di"] for c in h["kriteria"] if c["kode"] == "fakta"][0], ["P1"])
        self.assertNotIn("Sari", json.dumps(h))
        self.assertNotIn("Budi", json.dumps(h))

    # Aturan 2: tabel <= 3 kolom, baris pemisah benar.
    def test_tabel_salah_ditolak(self):
        t = draf_baik(self.h)
        self.assertTrue(self.masalah(teks=t.replace("|---|---|---|\n", "")))
        self.assertTrue(self.masalah(teks=t.replace("|---|---|---|", "|---|---|")))
        self.assertTrue(self.masalah(teks=t.replace("|---|---|---|", "|--|--|--|")))
        self.assertTrue(self.masalah(teks=t.replace("| Kriteria | Lolos | Nilai |\n|---|---|---|",
                                                    "| Kriteria | Lolos | Nilai | Tren |\n|---|---|---|---|")))
        dua = t.replace("| Nada |", "|---|---|---|\n| Nada |")
        self.assertTrue(any("pemisah ganda" in x for x in self.masalah(teks=dua)))

    # Aturan 3 (lanjutan): --lama-jawaban.
    def test_lama_jawaban_berbagai_bentuk(self):
        self.assertEqual(r.baca_lama_teks(LAMA_02), {"fakta": 100.0, "nyambung": 90.0, "konteks": 85.0, "panjang": 95.0,
                                                     "nada": 90.0, "janji": 100.0, "bocor": 100.0, "teknis": 90.0})
        tabel = "| Fakta | 83,3% (10/12) | D |\n| Data pribadi | 91,7% (11/12) | C |\n| Kata teknis | 75% (9/12) | C |"
        self.assertEqual(r.baca_lama_teks(tabel), {"fakta": 83.3, "bocor": 91.7, "teknis": 75.0})
        self.assertEqual(r.baca_lama_teks("- Fakta: 80% (8/10), D\n- Ingat konteks: 70%"), {"fakta": 80.0, "konteks": 70.0})
        # baris tren diutamakan; 'P3' dan 'turun 16,7 poin' tidak terbaca sebagai persen
        teks = ("Fakta salah (P3): turun 16,7 poin\n| Fakta | 50% (5/10) | D |\n" + self.h["baris_tren"])
        self.assertEqual(r.baca_lama_teks(teks), self.h["lolos_persen"])
        self.assertEqual(r.baca_lama_teks("fakta=80; nada: 90"), {"fakta": 80.0, "nada": 90.0})
        p = []
        self.assertEqual(r.baca_lama_teks("minggu lalu bagus", p), {})
        self.assertTrue(p)

    def test_lama_jawaban_sama_dengan_lama(self):
        _, a, _ = jalan_nilai(MATRIKS_02, "--lama-jawaban", LAMA_02)
        _, b, _ = jalan_nilai(MATRIKS_02, "--lama", "fakta=100,nyambung=90,konteks=85,panjang=95,nada=90,janji=100,bocor=100,teknis=90")
        self.assertEqual([c.get("selisih_poin") for c in a["kriteria"]], [c.get("selisih_poin") for c in b["kriteria"]])
        _, c, _ = jalan_nilai(MATRIKS_02, "--lama-jawaban", LAMA_02, "--lama", "fakta=50")
        self.assertEqual(c["kriteria"][0]["lama_persen"], 50.0)
        self.assertTrue(any("dua kali" in x for x in c["peringatan"]))

    def test_tren_putar_balik(self):
        # baris tren minggu ini ditempel minggu depan -> selisih 0 semua bila data sama
        _, h2, _ = jalan_nilai(MATRIKS_02, "--lama-jawaban", "rapor lalu...\n" + self.h["baris_tren"])
        self.assertTrue(all(c["selisih_poin"] == 0 for c in h2["kriteria"]))

    def test_lama_jawaban_stdin(self):
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            lama_stdin = sys.stdin
            sys.stdin = io.StringIO(LAMA_02)
            try:
                kode = r.main(["--nilai", MATRIKS_02, "--lama-jawaban", "-", "--json"])
            finally:
                sys.stdin = lama_stdin
        self.assertEqual(kode, 0)
        self.assertTrue(json.loads(out.getvalue())["ada_rapor_lama"])

    # Aturan 4: cepat untuk 1.000+ percakapan.
    def test_kinerja_1000_lebih(self):
        import random
        import time
        acak = random.Random(3)
        nilai = "; ".join("P%d=%s" % (i, ",".join(k for k in r.KRITERIA if acak.random() < 0.1) or "lolos") for i in range(1, 2001))
        teks = "".join(blok("P%d" % i, "Saya Kak Sari%d 0813-1111-%04d, pesanan a/n Budi belum sampai" % (i, i),
                            "Pasti dijamin sampai hari ini juga " * 20, "lolos") for i in range(1500))
        mulai = time.perf_counter()
        k1, h1, _ = jalan_nilai(nilai)
        k2, out, _ = jalan(teks)
        draf = draf_baik(h1, "Catatan: " + "kalimat biasa. " * 200)
        r.cek_balasan(draf, h1, ["Sari%d" % i for i in range(1500)], ["0813-1111-%04d" % i for i in range(1500)])
        lama = time.perf_counter() - mulai
        self.assertEqual((k1, k2), (0, 0))
        self.assertEqual(h1["dinilai"], 2000)
        self.assertEqual(json.loads(out)["dinilai"], 1500)
        self.assertLess(lama, 10.0)
        teks_blok = io.StringIO()
        with redirect_stdout(teks_blok):
            r.main(["--nilai", nilai])
        self.assertIn("lainnya)", teks_blok.getvalue())  # daftar 'gagal di' diringkas

    # Aturan 5: panjang, penutup, tanpa kata proses, tanpa digit nomor.
    def test_panjang_dan_penutup(self):
        self.assertTrue(any("panjang" in x for x in self.masalah("isi " * 1000)))
        self.assertTrue(any("rinci" in x for x in self.masalah(teks=draf_baik(self.h) + "\nTerima kasih.")))

    def test_kata_proses_ditolak(self):
        for kata in ("Dihitung dengan skrip.", "lihat rapor.py", "berkas /home/user/x", "tempel ke AGENTS.md",
                     "jalankan --nilai", "pakai cek-privasi-openclaw", "hasil exec tool"):
            self.assertTrue(self.masalah(kata), kata)

    def test_digit_nomor_ditolak(self):
        for x in ("nomor 0813-1111-2222", "nomor 0813-xxxx-2222", "akhiran 2222 bocor", "+62 813 1111 2222",
                  "nomor xxxx-2222"):
            self.assertTrue(self.masalah(x), x)
        self.assertEqual(self.masalah("Jam buka 08.00-21.00, ongkir gratis min. Rp200.000."), [])

    # Aturan 6: baris tren wajib & sama dengan hitungan.
    def test_baris_tren_wajib(self):
        t = draf_baik(self.h)
        self.assertTrue(any("Angka tren" in x for x in self.masalah(teks=t.replace(self.h["baris_tren"], ""))))
        salah = t.replace(self.h["baris_tren"], self.h["baris_tren"].replace("fakta 83,3%", "fakta 90%"))
        self.assertTrue(any("baris tren" in x for x in self.masalah(teks=salah)))
        self.assertTrue(self.h["baris_tren"].startswith(r.TANDA_TREN + ": fakta "))
        out = io.StringIO()
        with redirect_stdout(out):
            r.main(["--nilai", "P1=lolos"])
        self.assertIn("Angka tren (tempel minggu depan): fakta 100%", out.getvalue())

    # Aturan 7: persen mengikuti data, bukan "semua 90%".
    def test_semua_90_ditolak_bila_data_beda(self):
        t = draf_baik(self.h)
        import re
        semua90 = re.sub(r"\| (\d+(?:,\d)?)% \((\d+)/12\)", "| 90% (9/10)", t)
        m = self.masalah(teks=semua90)
        self.assertTrue(any("sama persen" in x for x in m), m)
        self.assertTrue(any("fakta tertulis 90%" in x for x in m), m)
        kurang = "\n".join(b for b in t.splitlines() if not b.startswith("| Nada"))
        self.assertTrue(any("belum tertulis: nada" in x for x in self.masalah(teks=kurang)))
        self.assertTrue(any("bersih" in x for x in self.masalah(teks=t.replace("7 dari 12", "8 dari 12"))))

    def test_cli_cek_balasan(self):
        with tempfile.TemporaryDirectory() as d:
            baik, buruk = os.path.join(d, "a.txt"), os.path.join(d, "b.txt")
            Path(baik).write_text(draf_baik(self.h), encoding="utf-8")
            Path(buruk).write_text(draf_baik(self.h, "Pertanyaan: Sari sudah transfer?"), encoding="utf-8")
            for path, kode_harap in ((baik, 0), (buruk, 1)):
                out = io.StringIO()
                with redirect_stdout(out), redirect_stderr(io.StringIO()):
                    kode = r.main(["--nilai", MATRIKS_02, "--lama-jawaban", LAMA_02, "--samarkan-nama", "Sari",
                                   "--cek-balasan", path])
                self.assertEqual(kode, kode_harap, out.getvalue())
            # nama terbaca otomatis dari berkas percakapan walau angka dari --nilai
            data = os.path.join(d, "p.txt")
            Path(data).write_text("---\nPelanggan (Sari, 0813-1111-2222): halo\nBot: halo\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(r.main([data, "--nilai", MATRIKS_02, "--lama-jawaban", LAMA_02, "--cek-balasan", buruk]), 1)
                self.assertEqual(r.main(["--nilai", "P1=lolos", "--cek-balasan", os.path.join(d, "tidak-ada.txt")]), 2)


class Uji103b(unittest.TestCase):
    """1.0.3 putaran 2: temuan pemeriksa independen, satu tes per temuan."""

    def setUp(self):
        _, self.h, _ = jalan_nilai(MATRIKS_02, "--lama-jawaban", LAMA_02)

    def masalah(self, ekstra="", teks=None, nama=(), nomor=(), angka=()):
        return r.cek_balasan(teks if teks is not None else draf_baik(self.h, ekstra), self.h, nama, nomor, angka)

    # Temuan 1: hitungan ditulis sebelum persen; label bermakna gagal.
    def test_lama_hitungan_sebelum_persen(self):
        _, h, _ = jalan_nilai("P1=lolos; P2=fakta", "--lama-jawaban", "Fakta: 10 dari 12 (83,3%)")
        fakta = h["kriteria"][0]
        self.assertEqual(fakta["lama_persen"], 83.3)
        self.assertEqual(fakta["selisih_poin"], -33.3)
        self.assertEqual(r.baca_lama_teks("Konteks: 11/12 (91,7%)"), {"konteks": 91.7})
        self.assertEqual(r.baca_lama_teks("Fakta: 10 dari 12"), {"fakta": 83.3})
        self.assertEqual(r.baca_lama_teks("Tidak nyambung: 2 percakapan (P2, P4); nyambung 83,3%"), {"nyambung": 83.3})
        self.assertEqual(r.baca_lama_teks("Nyambung naik dari 90% ke 100%"), {"nyambung": 100.0})
        # baris blok hitungan sendiri ("lolos 10 dari 12 (83,3%) | ... target 90% ...")
        out = io.StringIO()
        with redirect_stdout(out):
            r.main(["--nilai", MATRIKS_02])
        self.assertEqual(r.baca_lama_teks(out.getvalue().split("--- JSON ---")[0]), self.h["lolos_persen"])

    def test_lama_label_gagal_tidak_dipakai(self):
        p = []
        self.assertEqual(r.baca_lama_teks("Fakta salah: 16,7% percakapan", p), {})
        self.assertTrue(any("bermakna gagal" in x for x in p), p)
        p = []
        self.assertEqual(r.baca_lama_teks("Tidak janji berlebihan 83,3%; janji berlebihan 16,7%", p), {"janji": 83.3})
        self.assertTrue(any("bermakna gagal" in x for x in p))

    # Temuan 2: teks tambahan panjang di kode P; nama masuk pemeriksaan draf.
    def test_kode_p_dengan_nama_panjang(self):
        k, h, _ = jalan_nilai("P1=lolos; P2 (Ibu Sari Wulandari)=fakta; P3 (Sari)=janji")
        self.assertEqual(k, 0)
        self.assertEqual(h["dinilai"], 3)
        self.assertEqual(h["lolos_persen"]["fakta"], 66.7)
        self.assertNotIn("Wulandari", json.dumps(h))
        self.assertNotIn("Sari", json.dumps(h))
        nama = []
        r.parse_nilai("P2 (Ibu Sari Wulandari)=fakta; P4 (H.)=lolos; P5 a/n Budi Santoso: nada", [], nama)
        for n in ("Sari Wulandari", "Sari", "Wulandari", "H.", "Budi Santoso"):
            self.assertIn(n, nama)

    def test_nama_dari_kode_p_dicek_di_draf(self):
        with tempfile.TemporaryDirectory() as d:
            draf = os.path.join(d, "d.txt")
            Path(draf).write_text(draf_baik(self.h, "Pertanyaan: Sari sudah dihubungi?"), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                kode = r.main(["--nilai", MATRIKS_02.replace("P3=", "P3 (Sari)="), "--cek-balasan", draf])
            self.assertEqual(kode, 1)

    # Temuan 3: nama tanpa sapaan / inisial di depan kode P, tanpa berkas.
    def test_nama_tersirat_dan_inisial_p(self):
        self.assertTrue(any("Hendra" in x for x in self.masalah("Pertanyaan: (1) Apakah Hendra jadi pindah Kamis?")))
        self.assertTrue(any("inisial" in x for x in self.masalah("Pertanyaan: (1) Apakah H. (P4) jadi pindah?")))
        self.assertTrue(any("Hendra" in x for x in self.masalah("Asumsi: keluhan Hendra (P4) selesai.")))
        self.assertTrue(any("inisial" in x for x in self.masalah("Pertanyaan: H. sudah bayar?", nama=("H.",))))
        for aman in ("Pertanyaan: (1) Apakah Anda punya daftar harga resmi?", "Apakah Senin tetap buka?",
                     "Nilai umum C. Pelanggan di P4 belum dihubungi."):
            self.assertEqual(self.masalah(aman, nama=("C.",)), [], aman)

    # Temuan 4: positif palsu rekening usaha & persen di kalimat ringkasan.
    def test_rekening_usaha_dan_ringkasan_tidak_ditolak(self):
        self.assertEqual(self.masalah("PR: sebut 'Rekening a/n Klinik Senyum Sehat'."), [])
        self.assertEqual(self.masalah("PR: transfer ke Rekening BCA 1234567890."), [])
        self.assertEqual(self.masalah("Nyambung naik dari 90% ke 100% dibanding minggu lalu."), [])
        # rekening yang berasal dari pesan pelanggan tetap ditolak; nomor HP tetap ditolak
        self.assertTrue(self.masalah("Rekening BCA 1234567890 milik P3.", angka=("1234567890",)))
        self.assertTrue(self.masalah("Rekening 081311112222."))
        self.assertTrue(self.masalah("Rekening a/n Joko belum dicek."))
        # persen salah di baris tabel/butir tetap tertangkap
        self.assertTrue(any("fakta tertulis" in x for x in self.masalah("- Fakta: 90% (9/10), A")))

    # Temuan 5: percakapan bersih dicocokkan sebagai angka utuh.
    def test_bersih_bukan_substring(self):
        t = draf_baik(self.h).replace("7 dari 12", "17 dari 120")
        self.assertTrue(any("bersih" in x for x in self.masalah(teks=t)))

    # Temuan 6: pembulatan setengah ke atas, sama dengan hitung manual.
    def test_pembulatan_setengah_ke_atas(self):
        _, h, _ = jalan_nilai("; ".join("P%d=%s" % (i, "nada" if i <= 3 else "lolos") for i in range(1, 17)))
        self.assertEqual(h["lolos_persen"]["nada"], 81.3)  # 13/16 = 81,25
        self.assertEqual(r.bulat1(-16.75), -16.8)
        import random
        acak = random.Random(11)
        for _ in range(3000):
            n = acak.randint(1, 400)
            a = acak.randint(0, n)
            harap = (Decimal(100 * a) / Decimal(n)).quantize(Decimal("0.1"), ROUND_HALF_UP)
            self.assertEqual(r.persen(a, n), float(harap), (a, n))

    # Temuan 7: checklist tidak bertentangan dengan baris tren wajib.
    def test_checklist_tren_selaras(self):
        sk = (RAKIT / "SKILL.md").read_text(encoding="utf-8")
        self.assertFalse("Tren hanya ada bila rapor lama diberikan;" in sk)
        self.assertIn("tetap selalu ada", sk)
        self.assertLess(len(sk.splitlines()), 300)



class Uji103c(unittest.TestCase):
    """1.0.3 putaran 3: temuan pemeriksa independen berikutnya, satu tes per temuan."""

    def setUp(self):
        _, self.h, _ = jalan_nilai(MATRIKS_02, "--lama-jawaban", LAMA_02)

    def masalah(self, teks, nama=()):
        return r.cek_balasan(teks, self.h, nama, ())

    def ganti_ringkasan(self, kalimat):
        baris = draf_baik(self.h).splitlines()
        baris[0] = kalimat
        return "\n".join(baris)

    # Temuan sedang: "x dari n" diikuti titik/koma tidak boleh dianggap belum tertulis.
    def test_bersih_diikuti_titik_atau_koma(self):
        for kal in ("**Rapor:** percakapan bersih 7 dari 12, nilai umum C.",
                    "**Rapor:** 12 percakapan dinilai, percakapan bersih 7 dari 12.",
                    "**Rapor:** bersih 7 dari 12 percakapan."):
            self.assertFalse(any("bersih" in x for x in self.masalah(self.ganti_ringkasan(kal))), kal)
        for salah in ("**Rapor:** bersih 7 dari 12,5 persen.", "**Rapor:** bersih 17 dari 120.",
                      "**Rapor:** bersih 7 dari 120.", "**Rapor:** bersih 1,7 dari 12."):
            self.assertTrue(any("bersih" in x for x in self.masalah(self.ganti_ringkasan(salah))), salah)

    def test_rapor_lama_hitungan_diikuti_tanda_baca(self):
        self.assertEqual(r.baca_lama_teks("Fakta: 10 dari 12."), {"fakta": 83.3})
        self.assertEqual(r.baca_lama_teks("Konteks: 1 dari 2, nada: 1 dari 2 percakapan."), {"konteks": 50.0, "nada": 50.0})
        self.assertEqual(r.baca_lama_teks("Fakta: 1 dari 2."), {"fakta": 50.0})
        self.assertEqual(r.baca_lama_teks("Fakta: 1 dari 2,"), {"fakta": 50.0})
        self.assertEqual(r.baca_lama_teks("Fakta: 1 dari 2 percakapan."), {"fakta": 50.0})
        self.assertEqual(r.baca_lama_teks("Fakta = 90."), {"fakta": 90.0})
        # desimal tetap tidak dipotong jadi hitungan
        self.assertEqual(r.baca_lama_teks("Fakta: 1 dari 2,5 jam"), {}, )
        self.assertTrue(r.RE_HITUNGAN.search("1 dari 2."))
        self.assertTrue(r.RE_HITUNGAN.search("1 dari 2,"))
        self.assertIsNone(r.RE_HITUNGAN.search("1 dari 2.5"))

    # Temuan ringan: nama marketplace/layanan bukan nama pelanggan.
    def test_merek_bukan_nama(self):
        for kal in ("Apakah Shopee sudah mengirim?", "Keluhan Tokopedia (P4) soal ongkir.", "pesanan Lazada telat",
                    "Apakah Gojek bisa antar?", "pelanggan Grab menunggu", "Apakah Bpjs diterima?"):
            self.assertEqual(self.masalah(draf_baik(self.h, kal)), [], kal)
        cs = r.parse_teks("---\nPelanggan: pesanan Shopee saya belum datang, dengan Gojek bisa?\nBot: bisa\n", set(), [])
        self.assertEqual(r.nama_terdeteksi(cs), [])
        # nama sungguhan tetap tertangkap
        self.assertTrue(self.masalah(draf_baik(self.h, "Apakah Hendra jadi datang?")))

    # Temuan ringan: nama tanpa sapaan ("Kak, ini Yuni", "dengan Dimas") terbaca otomatis dari tempelan.
    def test_nama_ini_dan_dengan(self):
        cs = r.parse_teks("---\nPelanggan: Kak, ini Yuni mau tanya stok\nBot: halo\n---\n"
                          "Pelanggan: Saya bicara dengan Dimas kemarin\nBot: baik\n", set(), [])
        nama = r.nama_terdeteksi(cs)
        self.assertIn("Yuni", nama)
        self.assertIn("Dimas", nama)
        self.assertTrue(any("Yuni" in x for x in self.masalah(draf_baik(self.h, "Catatan: Yuni minta stok."), nama)))
        self.assertNotIn("Harga", r.nama_terdeteksi(r.parse_teks("---\nPelanggan: ini Harga berapa\nBot: x\n", set(), [])))

    # Temuan ringan: --nilai dari stdin ('-') dan berkas ('@berkas'), untuk daftar sangat panjang.
    def test_nilai_stdin_dan_berkas(self):
        besar = "; ".join("P%d=%s" % (i, "nada" if i % 4 == 0 else "lolos") for i in range(1, 12001))
        self.assertGreater(len(besar.encode()), 131072)
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "nilai.txt")
            Path(f).write_text(besar, encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out), redirect_stderr(io.StringIO()):
                self.assertEqual(r.main(["--nilai", "@" + f, "--json"]), 0)
            h = json.loads(out.getvalue())
            self.assertEqual(h["dinilai"], 12000)
            self.assertEqual(h["lolos_persen"]["nada"], 75.0)
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(r.main(["--nilai", "@" + os.path.join(d, "tidak-ada.txt")]), 2)
        lama_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO("P1=lolos\nP2=fakta\n")
            out = io.StringIO()
            with redirect_stdout(out), redirect_stderr(io.StringIO()):
                self.assertEqual(r.main(["--nilai", "-", "--json"]), 0)
            self.assertEqual(json.loads(out.getvalue())["lolos_persen"]["fakta"], 50.0)
            sys.stdin = io.StringIO("")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(r.main(["--nilai", "-", "--cek-balasan", "-"]), 2)
        finally:
            sys.stdin = lama_stdin
        self.assertIn("--nilai @", (RAKIT / "SKILL.md").read_text(encoding="utf-8"))

    # Temuan ringan: aturan/dokumen usang yang bertentangan.
    def test_aturan_usang_hilang(self):
        import re
        ref = (RAKIT / "references/rubrik-dan-tahap.md").read_text(encoding="utf-8")
        sk = (RAKIT / "SKILL.md").read_text(encoding="utf-8")
        readme = (RAKIT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("pelanggan A", ref)
        self.assertIn("pelanggan di P3", ref)
        self.assertIn("pelanggan di P3", sk)
        self.assertNotIn("pelanggan A", sk)
        self.assertEqual(len(re.findall(r"versi terkini", readme.split("Versi terkini:")[0])), 1)
        self.assertIn("v1.0.3 (versi terkini", readme)
        self.assertLess(len(sk.splitlines()), 300)
        for nama in ("02-klinik-bulan2-rapor-lama.md", "03-konsultan-minggu1.md"):
            teks = (RAKIT / "examples" / nama).read_text(encoding="utf-8")
            if re.search(r"^\|([^|]*\|){4,}\s*$", teks, re.M):
                self.assertIn("FORMAT LAMA", teks, nama)
            self.assertNotIn("cek-privasi-openclaw", teks, nama)

    def test_contoh_01_format_terkini(self):
        teks = (RAKIT / "examples/01-skincare-minggu2.md").read_text(encoding="utf-8")
        b = teks.split("<!-- awal balasan pertama -->", 1)[1].split("<!-- akhir balasan pertama -->", 1)[0].strip()
        data = (RAKIT / "examples/data/01-skincare-minggu2.txt").read_text(encoding="utf-8")
        cs = r.parse_teks(data, set(), [])
        h = r.hitung(cs, "minggu2-4", {}, 700, [], [])
        nomor = [m.group(0) for c in cs for _, t in c["turn"] for m in r.RE_HP.finditer(t)]
        self.assertEqual(r.cek_balasan(b, h, r.nama_terdeteksi(cs), nomor), [])
        self.assertTrue(h["semua_kriteria_sama_persen"])
        self.assertIn("kebetulan sama persen", b)
        self.assertIn("jangan menyalin angka dari contoh ini", teks)
        self.assertNotIn("cek-privasi-openclaw", teks)

if __name__ == "__main__":
    unittest.main(verbosity=1)
