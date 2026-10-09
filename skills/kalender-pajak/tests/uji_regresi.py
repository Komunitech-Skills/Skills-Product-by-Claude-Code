#!/usr/bin/env python3
"""Uji regresi kalender-pajak. Python standar saja.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)

Tanggal patokan pergeseran yang DIKONFIRMASI sumber luar (dicek 2026-09-25):
- SPT Masa PPh 21/Unifikasi masa Feb 2026: 20 Mar 2026 -> 25 Mar 2026 (libur & cuti Idulfitri) - DDTC/Kring Pajak.
- Setor PPh masa Apr 2026: 15 Mei 2026 (cuti bersama) -> 18 Mei 2026 - DDTC.
- PPN masa Apr 2026: 31 Mei 2026 (Minggu, Waisak) -> 1 Jun (Pancasila) -> 2 Jun 2026 - DDTC.
- v1.0.1: batas unggah faktur pajak keluaran tgl 20 bulan berikutnya (PER-11/PJ/2025 Ps. 44 ayat 1),
  tidak bergeser (sumber sekunder, PERLU REVIEW).
- v1.0.2: tenggat tidak bergeser yang jatuh di hari libur menyebut hari kerja sebelumnya;
  file --libur pengguna dilabeli "data libur dari pengguna" dan tidak mematikan peringatan.
- v1.0.3: SPT Tahunan (PMK 81/2024 Ps. 169) TIDAK bergeser meski hari libur - satu tanggal saja, tanpa
  "kemungkinan tanggal bergeser" (Ps. 173(1) hanya untuk Ps. 171 & 172; dicocokkan naskah resmi 2026-09-26).
"""
import csv
import datetime as dt
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
SCRIPT = SINI / "scripts" / "kalender_pajak.py"
sys.path.insert(0, str(SINI / "scripts"))
import kalender_pajak as kp  # noqa: E402

STAMP = dt.datetime(2026, 9, 25, 1, 2, 3, tzinfo=dt.timezone.utc)


def jalan(*argv):
    data, _ = kp.jalankan([str(a) for a in argv], sekarang_utc=STAMP)
    return data.decode("utf-8")


def acara_json(*argv):
    return json.loads(jalan(*argv, "--format", "json"))["acara"]


def cari(acara, kewajiban, jenis, masa):
    hasil = [e for e in acara if e["kewajiban"] == kewajiban and e["jenis"] == jenis and e["masa"] == masa]
    assert len(hasil) == 1, (kewajiban, jenis, masa, hasil)
    return hasil[0]


class UjiPergeseran(unittest.TestCase):
    def setUp(self):
        self.a26 = acara_json("--profil", "pemberi-kerja,pemotong,badan-pkp,op-umkm", "--tahun", "2026")

    def test_tanpa_geser(self):
        e = cari(self.a26, "pph21", "setor", "Sep 2026")
        self.assertEqual(e["tanggal"], "2026-10-15")
        self.assertEqual(e["bergeser_karena"], [])

    def test_minggu(self):
        e = cari(self.a26, "pph21", "setor", "Feb 2026")  # 15 Mar 2026 Minggu
        self.assertEqual((e["tanggal_normal"], e["tanggal"]), ("2026-03-15", "2026-03-16"))

    def test_sabtu_minggu_libur_17_agustus(self):
        e = cari(self.a26, "pph21", "setor", "Jul 2026")  # 15 Agu Sab, 16 Min, 17 libur
        self.assertEqual(e["tanggal"], "2026-08-18")
        self.assertEqual(len(e["bergeser_karena"]), 3)

    def test_cuti_bersama_imlek(self):
        e = cari(self.a26, "unifikasi", "setor", "Jan 2026")  # 15 Min, 16 cuti, 17 Imlek
        self.assertEqual(e["tanggal"], "2026-02-18")
        self.assertTrue(any("Cuti bersama" in x for x in e["bergeser_karena"]))

    def test_lebaran_2026_dikonfirmasi_ddtc(self):
        for k in ("pph21", "unifikasi"):
            e = cari(self.a26, k, "lapor", "Feb 2026")
            self.assertEqual(e["tanggal"], "2026-03-25", k)

    def test_cuti_bersama_mei_2026_dikonfirmasi_ddtc(self):
        e = cari(self.a26, "pph-final-umkm", "setor", "Apr 2026")
        self.assertEqual(e["tanggal"], "2026-05-18")

    def test_libur_beruntun_mei_2027(self):
        a = acara_json("--profil", "pph25", "--tahun", "2027", "--bulan-mulai", "5", "--jumlah-bulan", "1")
        e = cari(a, "pph25", "setor", "Apr 2027")  # 15 Sab .. 20 Waisak -> 21 Jumat
        self.assertEqual(e["tanggal"], "2027-05-21")
        self.assertEqual(len(e["bergeser_karena"]), 6)

    def test_hasil_selalu_hari_kerja(self):
        libur, _ = kp.muat_libur()
        a = acara_json("--profil", "pemberi-kerja,pemotong,badan-pkp,op-umkm", "--tahun", "2026",
                       "--jumlah-bulan", "24")
        for e in a:
            if e["jenis"] in ("tahunan", "unggah"):  # sengaja tidak digeser
                continue
            t = dt.date.fromisoformat(e["tanggal"])
            self.assertLess(t.weekday(), 5, e)
            self.assertNotIn(t, libur, e)


class UjiAkhirBulan(unittest.TestCase):
    def test_ppn_februari_biasa_dan_kabisat(self):
        a = acara_json("--profil", "ppn", "--tahun", "2027", "--bulan-mulai", "2", "--jumlah-bulan", "2")
        e = cari(a, "ppn", "setor+lapor", "Jan 2027")  # 28 Feb 2027 Minggu -> 1 Mar
        self.assertEqual((e["tanggal_normal"], e["tanggal"]), ("2027-02-28", "2027-03-01"))
        # 2028 kabisat: 29 Feb 2028 Selasa (tanpa data libur 2028 -> peringatan)
        d = json.loads(jalan("--profil", "ppn", "--tahun", "2028", "--bulan-mulai", "2", "--jumlah-bulan", "1",
                             "--format", "json"))
        e = cari(d["acara"], "ppn", "setor+lapor", "Jan 2028")
        self.assertEqual(e["tanggal_normal"], "2028-02-29")
        self.assertIn("2028", d["peringatan"])

    def test_ppn_30_hari(self):
        a = acara_json("--profil", "ppn", "--tahun", "2026", "--bulan-mulai", "9", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "ppn", "setor+lapor", "Agu 2026")["tanggal"], "2026-09-30")

    def test_desember_ke_tahun_berikutnya(self):
        a = acara_json("--profil", "pemberi-kerja,ppn", "--tahun", "2027", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "pph21", "setor", "Des 2026")["tanggal"], "2027-01-15")
        self.assertEqual(cari(a, "pph21", "lapor", "Des 2026")["tanggal"], "2027-01-20")
        # masa Nov 2026 PPN: 31 Des 2026 Kamis -> tetap
        a2 = acara_json("--profil", "ppn", "--tahun", "2026", "--bulan-mulai", "12", "--jumlah-bulan", "1")
        self.assertEqual(cari(a2, "ppn", "setor+lapor", "Nov 2026")["tanggal"], "2026-12-31")

    def test_desember_2027_lintas_tahun_ke_2028(self):
        # PPN masa Nov 2027: 31 Des 2027 Jumat (hari kerja). Masa Des 2027 PPh 21 setor 15 Jan 2028 Sabtu -> 17 Jan
        a = acara_json("--profil", "pph21", "--tahun", "2028", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "pph21", "setor", "Des 2027")["tanggal"], "2028-01-17")


class UjiTahunan(unittest.TestCase):
    def test_spt_op_tidak_bergeser(self):
        a = acara_json("--profil", "spt-op", "--tahun", "2027")
        e = cari(a, "spt-op", "tahunan", "Tahun pajak 2026")
        self.assertEqual(e["tanggal"], "2027-03-31")

    def test_spt_badan_akhir_april(self):
        a = acara_json("--profil", "spt-badan", "--tahun", "2027")
        self.assertEqual(cari(a, "spt-badan", "tahunan", "Tahun pajak 2026")["tanggal"], "2027-04-30")

    def test_bukti_a1_hari_libur_ditandai(self):
        md = jalan("--profil", "bukti-a1", "--tahun", "2026", "--jumlah-bulan", "1")
        self.assertIn("Sabtu, 31 Januari 2026", md)
        self.assertIn("TIDAK bergeser", md)


class UjiHariIni(unittest.TestCase):
    def test_14_hari(self):
        md = jalan("--profil", "badan-pkp,pemberi-kerja", "--hari-ini", "2026-10-10")
        self.assertIn("5 hari lagi", md)  # 15 Okt
        self.assertIn("10 hari lagi", md)  # 20 Okt
        self.assertNotIn("Nov 2026", md)

    def test_hari_ini_dan_besok(self):
        md = jalan("--profil", "pph21", "--hari-ini", "2026-10-14", "--rentang", "1")
        self.assertIn("besok", md)
        md = jalan("--profil", "pph21", "--hari-ini", "2026-10-15", "--rentang", "1")
        self.assertIn("HARI INI", md)

    def test_kosong(self):
        md = jalan("--profil", "spt-op", "--hari-ini", "2026-09-25")
        self.assertIn("Tidak ada tenggat", md)


class UjiIcs(unittest.TestCase):
    def setUp(self):
        self.teks = jalan("--profil", "badan-pkp,pemberi-kerja,pemotong", "--tahun", "2026", "--format", "ics")

    def test_crlf_dan_panjang_baris(self):
        raw = self.teks.encode("utf-8")
        self.assertTrue(raw.endswith(b"\r\n"))
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        for baris in raw.split(b"\r\n"):
            self.assertLessEqual(len(baris), 75)
            baris.decode("utf-8")  # lipatan tidak memotong karakter multi-byte

    def urai(self):
        lines = self.teks.split("\r\n")
        gabung = []
        for l in lines:
            if l.startswith(" ") and gabung:
                gabung[-1] += l[1:]
            elif l:
                gabung.append(l)
        return gabung

    def test_struktur(self):
        g = self.urai()
        self.assertEqual(g[0], "BEGIN:VCALENDAR")
        self.assertEqual(g[-1], "END:VCALENDAR")
        self.assertIn("VERSION:2.0", g)
        self.assertTrue(any(x.startswith("PRODID:") for x in g))
        self.assertEqual(g.count("BEGIN:VEVENT"), g.count("END:VEVENT"))
        self.assertEqual(g.count("BEGIN:VALARM"), 2 * g.count("BEGIN:VEVENT"))
        self.assertIn("TRIGGER:-P2DT15H", g)
        self.assertIn("TRIGGER:-PT15H", g)
        uids = [x for x in g if x.startswith("UID:")]
        self.assertEqual(len(uids), len(set(uids)))
        self.assertEqual(len(uids), g.count("BEGIN:VEVENT"))
        for x in g:
            if x.startswith(("DTSTART", "DTEND")):
                self.assertRegex(x, r"^DT(START|END);VALUE=DATE:\d{8}$")
            if x.startswith("DTSTAMP:"):
                self.assertEqual(x, "DTSTAMP:20260925T010203Z")

    def test_dtend_hari_berikut(self):
        g = self.urai()
        mulai = [x.split(":")[1] for x in g if x.startswith("DTSTART")]
        akhir = [x.split(":")[1] for x in g if x.startswith("DTEND")]
        for s, e in zip(mulai, akhir):
            d0 = dt.datetime.strptime(s, "%Y%m%d").date()
            self.assertEqual(dt.datetime.strptime(e, "%Y%m%d").date(), d0 + dt.timedelta(days=1))

    def test_escape(self):
        self.assertEqual(kp.ics_escape("a,b;c\\d\ne"), "a\\,b\\;c\\\\d\\ne")
        g = self.urai()
        for x in g:
            if x.startswith(("SUMMARY:", "DESCRIPTION:")):
                isi = x.split(":", 1)[1]
                # koma/titik koma harus ter-escape
                self.assertIsNone(re.search(r"(?<!\\)[,;]", isi.replace("\\\\", "")), x)

    def test_uid_stabil(self):
        lain = jalan("--profil", "badan-pkp,pemberi-kerja,pemotong", "--tahun", "2026", "--format", "ics")
        uid1 = [x for x in self.urai() if x.startswith("UID:")]
        uid2 = [x for x in lain.split("\r\n") if x.startswith("UID:")]
        self.assertEqual(uid1, uid2)
        # masa yang sama dari rentang berbeda -> UID sama (impor ulang tidak dobel)
        sebagian = jalan("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1",
                         "--format", "ics")
        u = [x for x in sebagian.split("\r\n") if x.startswith("UID:")]
        self.assertTrue(set(u) <= set(uid1))

    def test_lipat_utf8(self):
        panjang = "DESCRIPTION:" + "é" * 100
        hasil = kp.ics_lipat(panjang)
        for b in hasil.split("\r\n"):
            self.assertLessEqual(len(b.encode("utf-8")), 75)
        self.assertEqual(hasil.replace("\r\n ", ""), panjang)


class UjiCsvDanInputBuruk(unittest.TestCase):
    def test_csv(self):
        teks = jalan("--profil", "op-umkm", "--tahun", "2026", "--format", "csv")
        rows = list(csv.DictReader(io.StringIO(teks)))
        self.assertEqual(rows[0]["tanggal"], "2026-01-15")
        self.assertIn("keterangan_geser", rows[0])

    def cli(self, *argv):
        return subprocess.run([sys.executable, str(SCRIPT)] + list(argv), stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    def test_input_buruk_tanpa_traceback(self):
        kasus = [["--profil", "toko-kue"], ["--profil", "op-umkm", "--bulan-mulai", "13"],
                 ["--profil", "op-umkm", "--bulan-mulai", "nol"], ["--profil", "op-umkm", "--tahun", "1999"],
                 ["--profil", "op-umkm", "--hari-ini", "31-12-2026"], ["--profil", "op-umkm", "--format", "pdf"],
                 [], ["--profil", "op-umkm", "--jumlah-bulan", "0"], ["--opsi-ngawur"],
                 ["--profil", "op-umkm", "--libur", "tidak-ada.csv"]]
        for k in kasus:
            p = self.cli(*k)
            self.assertEqual(p.returncode, 2, k)
            err = p.stderr.decode("utf-8")
            self.assertIn("ERROR:", err, k)
            self.assertNotIn("Traceback", err, k)

    def test_file_libur_rusak(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "rusak.csv"
            f.write_text("tanggal,jenis\n2028-13-40,libur\n", encoding="utf-8")
            p = self.cli("--profil", "op-umkm", "--libur", str(f))
            self.assertEqual(p.returncode, 2)
            self.assertIn("baris 2", p.stderr.decode("utf-8"))

    def test_file_libur_tambahan_dipakai(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "libur-2028.csv"
            f.write_text("tanggal,jenis,keterangan\n2028-02-15,libur,Contoh libur\n", encoding="utf-8")
            a = json.loads(jalan("--profil", "pph21", "--tahun", "2028", "--bulan-mulai", "2",
                                 "--jumlah-bulan", "1", "--libur", str(f), "--format", "json"))
            e = cari(a["acara"], "pph21", "setor", "Jan 2028")
            self.assertEqual(e["tanggal"], "2028-02-16")
            # v1.0.2: file pengguna TIDAK mematikan peringatan tahun tanpa data resmi
            self.assertIn("2028", a["peringatan"])
            self.assertIn("data libur dari pengguna", a["peringatan"])

    def test_tahun_tanpa_data_peringatan_stderr(self):
        p = self.cli("--profil", "op-umkm", "--tahun", "2029", "--format", "ics")
        self.assertEqual(p.returncode, 0)
        self.assertIn("2029", p.stderr.decode("utf-8"))

    def test_keluar_file(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "pajak.ics"
            p = self.cli("--profil", "op-umkm", "--tahun", "2026", "--format", "ics", "--keluar", str(f))
            self.assertEqual(p.returncode, 0)
            self.assertTrue(f.read_bytes().startswith(b"BEGIN:VCALENDAR\r\n"))

    def test_nama_bulan(self):
        a = acara_json("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "Oktober", "--jumlah-bulan", "1")
        self.assertEqual(cari(a, "pph21", "setor", "Sep 2026")["tanggal"], "2026-10-15")

    def test_daftar_profil(self):
        p = self.cli("--daftar-profil")
        self.assertEqual(p.returncode, 0)
        self.assertIn("badan-pkp", p.stdout.decode("utf-8"))

    def test_data_libur_lengkap(self):
        libur, tahun = kp.muat_libur()
        self.assertEqual(tahun, {2026, 2027})
        n26 = [t for t in libur if t.year == 2026]
        n27 = [t for t in libur if t.year == 2027]
        self.assertEqual(len(n26), 17 + 8)
        self.assertEqual(len(n27), 18 + 8)



class UjiRevisi101(unittest.TestCase):
    """Regresi temuan penguji (examples/HASIL-UJI.md) untuk v1.0.1."""

    def test_tanggal_lama_tidak_berubah(self):
        a = acara_json("--profil", "pemberi-kerja,pemotong,badan-pkp,op-umkm", "--tahun", "2026")
        self.assertEqual(cari(a, "pph21", "lapor", "Feb 2026")["tanggal"], "2026-03-25")
        self.assertEqual(cari(a, "unifikasi", "lapor", "Feb 2026")["tanggal"], "2026-03-25")
        self.assertEqual(cari(a, "pph-final-umkm", "setor", "Apr 2026")["tanggal"], "2026-05-18")
        self.assertEqual(cari(a, "ppn", "setor+lapor", "Apr 2026")["tanggal"], "2026-06-02")
        self.assertEqual(cari(a, "ppn", "setor+lapor", "Sep 2026")["tanggal"], "2026-11-02")
        self.assertEqual(cari(a, "spt-badan", "tahunan", "Tahun pajak 2025")["tanggal"], "2026-04-30")
        self.assertEqual(cari(a, "spt-op", "tahunan", "Tahun pajak 2025")["tanggal"], "2026-03-31")

    # P1 - batas unggah faktur pajak keluaran
    def test_p1_unggah_faktur_tgl_20_semua_profil_pkp(self):
        for prof in ("badan-pkp", "pkp", "ppn", "op-umkm,pkp"):
            a = acara_json("--profil", prof, "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1")
            e = cari(a, "ppn", "unggah", "Sep 2026")
            self.assertEqual(e["tanggal"], "2026-10-20", prof)
            self.assertIn("faktur pajak keluaran", e["kegiatan"])

    def test_p1_unggah_faktur_tidak_ada_di_profil_non_pkp(self):
        a = acara_json("--profil", "op-umkm,pemberi-kerja,pemotong,badan-umum", "--tahun", "2026")
        self.assertFalse([e for e in a if e["jenis"] == "unggah"])

    def test_p1_unggah_faktur_tidak_bergeser_saat_libur(self):
        a = acara_json("--profil", "badan-pkp", "--tahun", "2026", "--bulan-mulai", "3", "--jumlah-bulan", "1")
        e = cari(a, "ppn", "unggah", "Feb 2026")  # 20 Mar 2026 cuti bersama Idulfitri
        self.assertEqual(e["tanggal"], "2026-03-20")
        self.assertEqual(e["bergeser_karena"], [])
        self.assertIn("Idulfitri", e["libur_tidak_bergeser"])
        self.assertIn("TIDAK bergeser", e["keterangan"])
        # 20 Des 2026 Minggu -> tetap 20 Des, ditandai
        a = acara_json("--profil", "pkp", "--tahun", "2026", "--bulan-mulai", "12", "--jumlah-bulan", "1")
        e = cari(a, "ppn", "unggah", "Nov 2026")
        self.assertEqual((e["tanggal"], e["libur_tidak_bergeser"]), ("2026-12-20", "Minggu"))

    def test_p1_catatan_dasar_dan_perlu_review(self):
        md = jalan("--profil", "badan-pkp", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1")
        self.assertIn("UNGGAH faktur pajak keluaran bulan Sep 2026", md)
        self.assertIn("PER-11/PJ/2025", md)
        self.assertIn("PERLU REVIEW", md)

    def test_p1_unggah_di_ics_dan_hari_ini(self):
        md = jalan("--profil", "badan-pkp", "--hari-ini", "2026-10-15", "--rentang", "7")
        self.assertIn("UNGGAH faktur", md)
        ics = jalan("--profil", "pkp", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1",
                    "--format", "ics")
        self.assertIn("UNGGAH faktur", ics.replace("\r\n ", ""))

    # P2 - klaim pengingat & impor ulang
    def test_p2_catatan_google_calendar_saat_simpan_ics(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.ics"
            out, _ = kp.jalankan(["--profil", "op-umkm", "--tahun", "2026", "--format", "ics", "--keluar", str(f)],
                                 sekarang_utc=STAMP)
            teks = out.decode("utf-8")
            self.assertIn("Google Calendar", teks)
            self.assertIn("--acara-pengingat", teks)
            self.assertIn("duplikat", teks)
        _, per = kp.jalankan(["--profil", "op-umkm", "--tahun", "2026", "--format", "ics"], sekarang_utc=STAMP)
        self.assertIn("Google Calendar", per)

    def urai(self, teks):
        g = []
        for l in teks.split("\r\n"):
            if l.startswith(" ") and g:
                g[-1] += l[1:]
            elif l:
                g.append(l)
        return g

    def test_p2_acara_pengingat_terpisah(self):
        dasar = self.urai(jalan("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "10",
                                "--jumlah-bulan", "1", "--format", "ics"))
        g = self.urai(jalan("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1",
                            "--format", "ics", "--acara-pengingat"))
        n0 = dasar.count("BEGIN:VEVENT")
        self.assertEqual(g.count("BEGIN:VEVENT"), 3 * n0)
        self.assertEqual(g.count("BEGIN:VALARM"), 2 * n0)  # VALARM tetap hanya di acara tenggat
        uids = [x for x in g if x.startswith("UID:")]
        self.assertEqual(len(uids), len(set(uids)))
        # setor PPh 21 masa Sep 2026 = 15 Okt 2026 -> pengingat 12 Okt & 14 Okt
        mulai = [x for x in g if x.startswith("DTSTART")]
        self.assertIn("DTSTART;VALUE=DATE:20261012", mulai)
        self.assertIn("DTSTART;VALUE=DATE:20261014", mulai)
        self.assertTrue(any(x.startswith("SUMMARY:Pengingat H-3 pajak") for x in g))
        self.assertTrue(any(x.startswith("SUMMARY:Pengingat H-1 pajak") for x in g))
        for x in g:
            if x.startswith("SUMMARY:"):
                self.assertIsNone(re.search(r"(?<!\\)[,;]", x.split(":", 1)[1].replace("\\\\", "")), x)
        # UID pengingat stabil antar-run
        g2 = self.urai(jalan("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1",
                             "--format", "ics", "--acara-pengingat"))
        self.assertEqual(uids, [x for x in g2 if x.startswith("UID:")])
        for baris in jalan("--profil", "pph21", "--tahun", "2026", "--format", "ics",
                           "--acara-pengingat").encode("utf-8").split(b"\r\n"):
            self.assertLessEqual(len(baris), 75)

    def test_p2_acara_pengingat_hanya_ics(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "--profil", "op-umkm", "--acara-pengingat"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(p.returncode, 2)
        self.assertIn("ERROR:", p.stderr.decode("utf-8"))
        self.assertNotIn("Traceback", p.stderr.decode("utf-8"))

    def test_p2_prodid_versi(self):
        ics = jalan("--profil", "op-umkm", "--tahun", "2026", "--format", "ics")
        self.assertIn("PRODID:-//Komunitech//kalender-pajak %s//ID" % kp.VERSI, ics)
        self.assertEqual(kp.VERSI, "1.0.7")

    # P3 - CSV libur berkoma
    def test_p3_keterangan_berkoma_tanpa_kutip_tidak_terpotong(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "libur-2028.csv"
            f.write_text("tanggal,jenis,keterangan\n2028-02-15,libur,Uji, dengan koma\n"
                         '2028-03-15,libur,"Kutip, juga koma"\n', encoding="utf-8")
            libur, tahun = kp.muat_libur([str(f)])
            self.assertEqual(libur[dt.date(2028, 2, 15)], "Uji, dengan koma")
            self.assertEqual(libur[dt.date(2028, 3, 15)], "Kutip, juga koma")
            a = json.loads(jalan("--profil", "pph21", "--tahun", "2028", "--bulan-mulai", "2",
                                 "--jumlah-bulan", "1", "--libur", str(f), "--format", "json"))
            e = cari(a["acara"], "pph21", "setor", "Jan 2028")
            self.assertEqual(e["tanggal"], "2028-02-16")
            self.assertIn("Uji, dengan koma", e["bergeser_karena"][0])

    # P3 - tenggat berikutnya di mode --hari-ini
    def test_p3_hari_ini_kosong_sebut_tenggat_berikutnya(self):
        md = jalan("--profil", "spt-op", "--hari-ini", "2026-09-25")
        self.assertIn("Tidak ada tenggat", md)
        self.assertIn("Tenggat berikutnya", md)
        self.assertIn("Rabu, 31 Maret 2027", md)
        self.assertIn("LAPOR SPT Tahunan PPh Orang Pribadi tahun pajak 2026", md)
        d = json.loads(jalan("--profil", "pph21", "--hari-ini", "2026-10-21", "--rentang", "7", "--format", "json"))
        self.assertEqual(d["acara"], [])
        self.assertEqual(d["tenggat_berikutnya"][0]["tanggal"], "2026-11-16")

    def test_p3_hari_ini_tenggat_berikutnya_bergeser(self):
        md = jalan("--profil", "pph21", "--hari-ini", "2026-10-21", "--rentang", "7")
        self.assertIn("Senin, 16 November 2026", md)
        self.assertIn("26 hari lagi", md)

    # P3 - label alasan geser menampilkan hari & libur
    def test_p3_label_sabtu_dan_hari_raya(self):
        a = acara_json("--profil", "pph21", "--tahun", "2026", "--bulan-mulai", "3", "--jumlah-bulan", "1")
        e = cari(a, "pph21", "lapor", "Feb 2026")
        self.assertEqual(e["tanggal"], "2026-03-25")
        self.assertIn("21 Mar: Sabtu & Idulfitri 1447 H", e["bergeser_karena"])
        self.assertIn("22 Mar: Minggu & Idulfitri 1447 H", e["bergeser_karena"])
        self.assertIn("20 Mar: Cuti bersama Idulfitri 1447 H", e["bergeser_karena"])
        a = acara_json("--profil", "ppn", "--tahun", "2026", "--bulan-mulai", "6", "--jumlah-bulan", "1")
        e = cari(a, "ppn", "setor+lapor", "Apr 2026")
        self.assertEqual(e["bergeser_karena"][0], "31 Mei: Minggu & Hari Raya Waisak 2570 BE")

    # P3 - cakupan periode & sumber data libur
    def test_p3_cakupan_dan_sumber_libur(self):
        md = jalan("--profil", "badan-pkp,pemberi-kerja", "--tahun", "2027")
        self.assertIn("Cakupan: tenggat yang **jatuh**", md)
        self.assertIn("masa pajak Desember 2027", md)
        self.assertIn("tahun pajak 2027", md)
        self.assertIn("Data libur: SKB 3 Menteri", md)
        self.assertIn("libur-nasional-2027.csv", md)
        ck = jalan("--profil", "op-umkm", "--tahun", "2026", "--format", "checklist")
        self.assertIn("Cakupan:", ck)
        self.assertIn("Data libur:", ck)
        hi = jalan("--profil", "op-umkm", "--hari-ini", "2026-10-01")
        self.assertIn("Data libur:", hi)

    def test_p3_catatan_perpanjangan_spt_2025(self):
        a = acara_json("--profil", "spt-op", "--tahun", "2026")
        e = cari(a, "spt-op", "tahunan", "Tahun pajak 2025")
        self.assertEqual(e["tanggal"], "2026-03-31")
        self.assertIn("KEP-55/PJ/2026", e["keterangan"])
        # Regresi v1.0.6: KEP-55 BUKAN perpanjangan - jatuh tempo tetap, hanya sanksi dihapus s.d. 30 Apr 2026.
        self.assertIn("jatuh tempo tetap 31 Mar 2026", e["keterangan"])
        self.assertIn("menghapus sanksi", e["keterangan"])
        self.assertIn("30 Apr 2026", e["keterangan"])
        self.assertNotIn("diperpanjang", e["keterangan"])
        # Badan TP 2025: tanggal tetap 30 Apr 2026, catatan KEP-71 (bukan KEP-55)
        b = acara_json("--profil", "badan-umum", "--tahun", "2026")
        eb = cari(b, "spt-badan", "tahunan", "Tahun pajak 2025")
        self.assertEqual(eb["tanggal"], "2026-04-30")
        self.assertIn("KEP-71/PJ/2026", eb["keterangan"])
        self.assertNotIn("KEP-55", eb["keterangan"])
        self.assertIn("jatuh tempo tetap", eb["keterangan"])
        # Tahun pajak lain tidak diberi catatan kebijakan khusus
        e26 = cari(acara_json("--profil", "spt-op", "--tahun", "2027"), "spt-op", "tahunan", "Tahun pajak 2026")
        self.assertNotIn("KEP-", e26["keterangan"])
        # Teks skill & referensi tidak lagi menyebut KEP-55 sebagai perpanjangan/pengunduran
        for f in (SINI / "SKILL.md", SINI / "references" / "aturan-tenggat.md", SCRIPT):
            t = f.read_text(encoding="utf-8")
            self.assertNotIn("diundur ke 30 April 2026", t)
            self.assertNotIn("KEP-55/PJ/2026 → 30 Apr", t)
            self.assertNotIn("diperpanjang DJP sampai 30 Apr 2026", t)

    # Aturan yang diverifikasi ulang
    def test_aturan_pph25_dan_pasal(self):
        md = jalan("--profil", "pph25", "--tahun", "2026", "--jumlah-bulan", "1")
        self.assertIn("tgl 20", md)
        self.assertIn("Ps. 171", md)
        src = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("Ps. 94 dst.", src)
        skill = (SINI / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Ps. 100", skill)
        self.assertNotIn("Ps. 94 dst.", skill)


class UjiRevisi102(unittest.TestCase):
    """Regresi temuan P3 examples/06-uji-ulang-v1.0.1.md untuk v1.0.2."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def berkas(self, nama, isi):
        f = self.d / nama
        f.write_text(isi, encoding="utf-8")
        return str(f)

    def test_tanggal_lama_tidak_berubah(self):
        a = acara_json("--profil", "badan-pkp,pemberi-kerja,pemotong,op-umkm", "--tahun", "2026",
                       "--bulan-mulai", "10", "--jumlah-bulan", "15")
        self.assertEqual(len(a), 123)  # sama dengan hitungan independen 06-uji-ulang
        self.assertEqual(cari(a, "ppn", "unggah", "Apr 2027")["tanggal"], "2027-05-20")
        self.assertEqual(cari(a, "spt-op", "tahunan", "Tahun pajak 2026")["tanggal"], "2027-03-31")
        self.assertEqual(cari(a, "spt-badan", "tahunan", "Tahun pajak 2026")["tanggal"], "2027-04-30")
        self.assertEqual(cari(a, "pph21", "setor", "Apr 2027")["tanggal"], "2027-05-21")

    # (1) SPT Tahunan di hari libur: satu tanggal, tidak bergeser (Ps. 169), saran lapor lebih awal
    def test_1_spt_op_hari_libur_satu_tanggal(self):
        f = self.berkas("libur-2029.csv", "tanggal,jenis,keterangan\n2029-03-30,libur,Wafat Yesus Kristus\n")
        a = json.loads(jalan("--profil", "spt-op", "--tahun", "2029", "--jumlah-bulan", "4", "--libur", f,
                             "--format", "json"))["acara"]
        e = cari(a, "spt-op", "tahunan", "Tahun pajak 2028")
        self.assertEqual(e["tanggal"], "2029-03-31")  # Sabtu, tidak digeser
        self.assertEqual(e["saran_hari_kerja_sebelumnya"], "2029-03-29")
        self.assertNotIn("kemungkinan_tanggal_bergeser", e)
        self.assertIn("TIDAK bergeser", e["keterangan"])
        self.assertIn("tidak bergeser meski hari libur (PMK 81/2024 Ps. 169); lapor lebih awal", e["keterangan"])
        self.assertNotIn("Ps. 173", e["keterangan"])
        self.assertNotIn("PERLU REVIEW", e["keterangan"])
        self.assertNotIn("2 April 2029", e["keterangan"])

    def test_1_spt_badan_hari_libur_beruntun(self):
        f = self.berkas("libur-2028.csv", "tanggal,jenis,keterangan\n2028-05-01,libur,Hari Buruh\n")
        a = acara_json("--profil", "spt-badan", "--tahun", "2028", "--jumlah-bulan", "5", "--libur", f)
        e = cari(a, "spt-badan", "tahunan", "Tahun pajak 2027")
        self.assertEqual(e["tanggal"], "2028-04-30")  # Minggu
        self.assertEqual(e["saran_hari_kerja_sebelumnya"], "2028-04-28")
        self.assertNotIn("kemungkinan_tanggal_bergeser", e)
        self.assertIn("PMK 81/2024 Ps. 169", e["keterangan"])
        self.assertNotIn("2 Mei 2028", e["keterangan"])

    def test_1_spt_hari_kerja_tanpa_catatan(self):
        a = acara_json("--profil", "spt-op,spt-badan", "--tahun", "2027")
        for e in a:
            self.assertNotIn("kemungkinan_tanggal_bergeser", e)
            self.assertIsNone(e["saran_hari_kerja_sebelumnya"])
            self.assertEqual(e["keterangan"], "-")

    def test_1_tidak_ada_kemungkinan_geser_sama_sekali(self):
        a = acara_json("--profil", "badan-pkp,pemberi-kerja", "--tahun", "2026", "--jumlah-bulan", "24")
        for e in a:
            self.assertNotIn("kemungkinan_tanggal_bergeser", e, e["kegiatan"])
            self.assertNotIn("kemungkinan lain", e["keterangan"], e["kegiatan"])

    # (2) unggah faktur di hari libur: sebut hari kerja sebelumnya, tanggal resmi tetap
    def test_2_unggah_20_mei_2027_saran_14_mei(self):
        a = acara_json("--profil", "pkp", "--tahun", "2027", "--bulan-mulai", "5", "--jumlah-bulan", "1")
        e = cari(a, "ppn", "unggah", "Apr 2027")
        self.assertEqual(e["tanggal"], "2027-05-20")
        self.assertEqual(e["tanggal_normal"], "2027-05-20")
        self.assertEqual(e["saran_hari_kerja_sebelumnya"], "2027-05-14")
        self.assertIn("Jumat, 14 Mei 2027", e["keterangan"])
        self.assertNotIn("kemungkinan_tanggal_bergeser", e)
        md = jalan("--profil", "pkp", "--tahun", "2027", "--bulan-mulai", "5", "--jumlah-bulan", "1")
        self.assertIn("Jumat, 14 Mei 2027", md)

    def test_2_unggah_lain_di_hari_libur(self):
        harap = {("2026", "3", "Feb 2026"): "2026-03-17",   # 20 Mar cuti Idulfitri, 19 Nyepi, 18 cuti Nyepi
                 ("2026", "12", "Nov 2026"): "2026-12-18",  # 20 Des Minggu
                 ("2027", "2", "Jan 2027"): "2027-02-19",   # 20 Feb Sabtu
                 ("2027", "3", "Feb 2027"): "2027-03-19",   # 20 Mar Sabtu
                 ("2027", "6", "Mei 2027"): "2027-06-18",   # 20 Jun Minggu
                 ("2027", "11", "Okt 2027"): "2027-11-19"}  # 20 Nov Sabtu
        for (th, bl, masa), tgl in harap.items():
            a = acara_json("--profil", "pkp", "--tahun", th, "--bulan-mulai", bl, "--jumlah-bulan", "1")
            e = cari(a, "ppn", "unggah", masa)
            self.assertEqual(e["saran_hari_kerja_sebelumnya"], tgl, masa)
            self.assertEqual(e["tanggal"][8:], "20", masa)

    def test_2_bukti_a1_saran_hari_kerja(self):
        a = acara_json("--profil", "bukti-a1", "--tahun", "2026", "--jumlah-bulan", "1")
        self.assertEqual(a[0]["tanggal"], "2026-01-31")
        self.assertEqual(a[0]["saran_hari_kerja_sebelumnya"], "2026-01-30")

    # (3) file libur pengguna
    def test_3_label_data_libur_pengguna_bukan_skb(self):
        f = self.berkas("libur-2028.csv", "tanggal,jenis,keterangan\n2028-02-15,libur,Contoh\n")
        md = jalan("--profil", "pph21", "--tahun", "2028", "--bulan-mulai", "2", "--jumlah-bulan", "1",
                   "--libur", f)
        baris = [x for x in md.splitlines() if x.startswith("Data libur:")][0]
        self.assertNotIn("SKB 3 Menteri libur nasional & cuti bersama 2026, 2027, 2028", baris)
        self.assertIn("data libur dari pengguna", baris)
        self.assertIn("libur-2028.csv", baris)
        self.assertIn("PERINGATAN", md)
        d = json.loads(jalan("--profil", "pph21", "--tahun", "2028", "--libur", f, "--format", "json"))
        self.assertNotIn("2028 (", d["sumber_libur"].split(";")[0])
        self.assertIn("data libur dari pengguna", d["sumber_libur"])

    def test_3_peringatan_tetap_saat_file_pengguna(self):
        f = self.berkas("l.csv", "tanggal,jenis,keterangan\n2028-02-15,libur,Contoh\n")
        p = subprocess.run([sys.executable, str(SCRIPT), "--profil", "op-umkm", "--tahun", "2028",
                            "--format", "ics", "--libur", f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(p.returncode, 0)
        err = p.stderr.decode("utf-8")
        self.assertIn("PERINGATAN", err)
        self.assertIn("2028", err)
        self.assertIn("data libur dari pengguna", err)

    def test_3_file_pengguna_untuk_tahun_resmi_tidak_ubah_label_resmi(self):
        f = self.berkas("tambah.csv", "tanggal,jenis,keterangan\n2027-10-15,libur,Libur daerah\n")
        d = json.loads(jalan("--profil", "pph21", "--tahun", "2027", "--libur", f, "--format", "json"))
        self.assertIsNone(d["peringatan"])
        self.assertTrue(d["sumber_libur"].startswith("SKB 3 Menteri libur nasional & cuti bersama 2026, 2027"))
        self.assertEqual(cari(d["acara"], "pph21", "setor", "Sep 2027")["tanggal"], "2027-10-18")

    def test_ics_catatan_tidak_menyarankan_opsi_yang_sudah_dipakai(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.ics"
            out, _ = kp.jalankan(["--profil", "op-umkm", "--tahun", "2026", "--format", "ics",
                                  "--acara-pengingat", "--keluar", str(f)], sekarang_utc=STAMP)
            self.assertNotIn("--acara-pengingat", out.decode("utf-8"))
            self.assertIn("Google Calendar", out.decode("utf-8"))


class UjiRevisi107(unittest.TestCase):
    """v1.0.7 (uji OpenClaw 2026-10-01): kapan omzet kumulatif OP melewati Rp500 juta dihitung script,
    bukan ditebak model; rujukan skill lain bersyarat ("bila terpasang")."""

    def test_omzet_setahun_600jt_lewat_november(self):
        # 600 jt / 12 = 50 jt/bln; kumulatif Okt = 500 jt (belum MELEWATI) -> Nov 550 jt -> setor pertama 15 Des 2026 (Selasa)
        d = json.loads(jalan("--profil", "op-umkm", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1",
                             "--omzet-setahun", "600jt", "--format", "json"))["omzet_lewat_500jt"]
        self.assertEqual(d["bulan_lewat"], 11)
        self.assertEqual(d["kumulatif_sebelum"], 500000000)
        self.assertEqual(d["omzet_kena_bulan_lewat"], 50000000)
        self.assertEqual(d["setor_pertama"], "2026-12-15")

    def test_omzet_bulanan_lewat_oktober_geser_minggu(self):
        # kumulatif s.d. Sep 492 jt; Okt +60 jt = 552 jt -> kena 52 jt; 15 Nov 2026 Minggu -> Senin 16 Nov
        out = jalan("--profil", "op-umkm", "--tahun", "2026", "--bulan-mulai", "10", "--jumlah-bulan", "1",
                    "--omzet-bulanan", "48jt,45jt,52jt,70jt,55jt,50jt,53jt,58jt,61jt,60jt")
        self.assertIn("melewati Rp500 juta pada **Oktober 2026**", out)
        self.assertIn("Rp 52.000.000", out)
        self.assertIn("Senin, 16 November 2026", out)

    def test_belum_lewat(self):
        out = jalan("--profil", "op-umkm", "--tahun", "2026", "--omzet-bulanan", "100jt;100jt;100jt")
        self.assertIn("belum melewati Rp500 juta (sisa Rp 200.000.000)", out)

    def test_omzet_ditolak_untuk_badan_dan_input_rusak(self):
        for argv in (["--profil", "badan-umkm", "--omzet-setahun", "600jt"],
                     ["--profil", "badan-pkp", "--omzet-setahun", "600jt"],
                     ["--profil", "op-umkm", "--omzet-setahun", "enam ratus"],
                     ["--profil", "op-umkm", "--omzet-bulanan", ";".join(["10jt"] * 13)]):
            with self.assertRaises(kp.InputSalah):
                kp.jalankan(argv, sekarang_utc=STAMP)

    def test_rujukan_skill_bersyarat_dan_tanpa_kap_karangan(self):
        out = jalan("--profil", "op-umkm,pemberi-kerja,pkp", "--tahun", "2026", "--format", "checklist")
        self.assertIn("hitung-ppn bila terpasang", out)
        self.assertIn("pph-final-umkm (bila terpasang)", jalan("--profil", "op-umkm", "--tahun", "2026"))
        self.assertNotIn("411125", out)
        self.assertNotIn("411128", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
