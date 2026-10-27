#!/usr/bin/env python3
"""Uji regresi scripts/pantau_cron.py (parsing cron, jatuh tempo, toleransi, status, zona, input rusak).

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(AKAR, "scripts", "pantau_cron.py")
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import pantau_cron as pc  # noqa: E402

D = dt.datetime


def jalan(folder, *args):
    env = dict(os.environ)
    env.pop("PANTAU_CRON_DIR", None)
    p = subprocess.run([sys.executable, SCRIPT, args[0], "--folder", folder] + list(args[1:]),
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout, p.stderr


class Dasar(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.f = self._t.name

    def tearDown(self):
        self._t.cleanup()

    def tambah(self, nama, jadwal, saat="2026-10-01T08:00+07:00", *ekstra):
        c, o, e = jalan(self.f, "tambah", nama, "--jadwal", jadwal, "--sekarang", saat, *ekstra)
        self.assertEqual(c, 0, e)

    def ping(self, nama, saat):
        c, o, e = jalan(self.f, "ping", nama, "--sekarang", saat)
        self.assertEqual(c, 0, e)

    def cek_json(self, saat, *ekstra):
        c, o, e = jalan(self.f, "cek", "--json", "--tanpa-catat", "--sekarang", saat, *ekstra)
        self.assertEqual(c, 0, e)
        return {j["nama"]: j for j in json.loads(o)["jobs"]}


class ParsingCron(unittest.TestCase):
    def test_bintang_langkah_daftar_rentang(self):
        s = pc.parse_cron("*/15 8-10,20 * * *")
        self.assertEqual(s["menit"], [0, 15, 30, 45])
        self.assertEqual(s["jam"], [8, 9, 10, 20])
        s = pc.parse_cron("0 9-17/4 * * *")
        self.assertEqual(s["jam"], [9, 13, 17])
        self.assertEqual(pc.parse_cron("10/20 * * * *")["menit"], [10, 30, 50])

    def test_hari_minggu_7_sama_dengan_0_dan_nama(self):
        self.assertEqual(pc.parse_cron("0 7 * * 7")["hari"], {0})
        self.assertEqual(pc.parse_cron("0 7 * * 5-7")["hari"], {5, 6, 0})
        self.assertEqual(pc.parse_cron("0 7 * * mon-fri")["hari"], {1, 2, 3, 4, 5})
        self.assertEqual(pc.parse_cron("@daily")["jam"], [0])

    def test_cron_rusak_ditolak(self):
        for buruk in ("", "   ", "* * * *", "* * * * * *", "61 * * * *", "* 24 * * *", "0 0 0 * *", "0 0 * 13 *",
                      "*/0 * * * *", "5-1 * * * *", "a b c d e", "0,,5 * * * *", None, 5):
            with self.assertRaises(pc.GalatPantau, msg=repr(buruk)):
                pc.parse_cron(buruk)


class JatuhTempo(unittest.TestCase):
    def test_lintas_tengah_malam(self):
        s = pc.parse_cron("30 23 * * *")
        self.assertEqual(pc.sebelumnya(s, D(2026, 10, 13, 0, 10)), D(2026, 10, 12, 23, 30))
        self.assertEqual(pc.berikutnya(s, D(2026, 10, 12, 23, 30)), D(2026, 10, 13, 23, 30))
        self.assertEqual(pc.berikutnya(s, D(2026, 10, 12, 23, 31)), D(2026, 10, 13, 23, 30))

    def test_lintas_akhir_bulan_dan_tahun(self):
        s = pc.parse_cron("0 0 1 * *")
        self.assertEqual(pc.sebelumnya(s, D(2026, 3, 1, 0, 0), inklusif=False), D(2026, 2, 1, 0, 0))
        self.assertEqual(pc.berikutnya(s, D(2026, 12, 31, 23, 59)), D(2027, 1, 1, 0, 0))
        s31 = pc.parse_cron("0 0 31 * *")
        self.assertEqual(pc.sebelumnya(s31, D(2026, 3, 15, 12, 0)), D(2026, 1, 31, 0, 0))   # Februari tak punya tgl 31
        self.assertEqual(pc.berikutnya(s31, D(2026, 4, 1, 0, 0)), D(2026, 5, 31, 0, 0))

    def test_29_februari_dan_jadwal_mustahil(self):
        s = pc.parse_cron("0 0 29 2 *")
        self.assertEqual(pc.sebelumnya(s, D(2026, 6, 1)), D(2024, 2, 29, 0, 0))
        self.assertEqual(pc.berikutnya(s, D(2026, 6, 1)), D(2028, 2, 29, 0, 0))
        with self.assertRaises(pc.GalatPantau):
            pc.berikutnya(pc.parse_cron("0 0 31 2 *"), D(2026, 1, 1))

    def test_hari_minggu_dan_aturan_atau(self):
        senin = pc.parse_cron("0 7 * * 1")     # 12 Okt 2026 = Senin
        self.assertEqual(pc.sebelumnya(senin, D(2026, 10, 15, 12, 0)), D(2026, 10, 12, 7, 0))
        self.assertEqual(pc.berikutnya(senin, D(2026, 10, 12, 7, 0)), D(2026, 10, 19, 7, 0))
        atau = pc.parse_cron("0 0 13 * 5")     # tanggal 13 ATAU hari Jumat
        self.assertEqual(pc.berikutnya(atau, D(2026, 10, 12, 0, 0)), D(2026, 10, 13, 0, 0))   # tgl 13 (Selasa)
        self.assertEqual(pc.berikutnya(atau, D(2026, 10, 13, 0, 0)), D(2026, 10, 16, 0, 0))   # Jumat
        dan = pc.parse_cron("0 0 */2 * 1")     # kolom diawali * -> DAN
        self.assertEqual(pc.berikutnya(dan, D(2026, 10, 1, 0, 0)), D(2026, 10, 5, 0, 0))      # Senin & tgl ganjil


class StatusDanToleransi(Dasar):
    def test_ok_setelah_ping_dan_batas_toleransi(self):
        self.tambah("harian", "0 21 * * *", "2026-10-01T08:00+07:00")
        self.ping("harian", "2026-10-11T21:02+07:00")
        # tepat di batas toleransi (21:30) belum dianggap telat; 21:31 baru TERLAMBAT
        self.assertEqual(self.cek_json("2026-10-12T21:30+07:00")["harian"]["status"], "OK")
        j = self.cek_json("2026-10-12T21:31+07:00")["harian"]
        self.assertEqual((j["status"], j["terlewat"], j["lewat_menit"]), ("TERLAMBAT", 1, 31))

    def test_pulih_bila_ping_telat_akhirnya_datang(self):
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-11T21:01+07:00")
        self.assertEqual(self.cek_json("2026-10-12T23:00+07:00")["harian"]["status"], "TERLAMBAT")
        self.ping("harian", "2026-10-12T23:05+07:00")
        self.assertEqual(self.cek_json("2026-10-12T23:10+07:00")["harian"]["status"], "OK")

    def test_hilang_bila_dua_jadwal_terlewat_atau_tak_pernah_ping(self):
        self.tambah("harian", "0 21 * * *", "2026-10-01T08:00+07:00")
        self.ping("harian", "2026-10-09T21:01+07:00")
        j = self.cek_json("2026-10-12T21:40+07:00")["harian"]    # 10, 11, 12 Okt terlewat
        self.assertEqual((j["status"], j["terlewat"]), ("HILANG", 3))
        self.tambah("baru", "0 8 * * *", "2026-10-01T07:00+07:00")
        j = self.cek_json("2026-10-01T08:45+07:00")["baru"]
        self.assertEqual((j["status"], j["ping_terakhir"], j["terlewat"]), ("HILANG", None, 1))

    def test_job_baru_menunggu_jadwal_pertama(self):
        self.tambah("harian", "0 21 * * *", "2026-10-12T21:00:30+07:00")   # jadwal 21.00 sudah lewat sebelum didaftarkan
        j = self.cek_json("2026-10-12T22:00+07:00")["harian"]
        self.assertEqual((j["status"], j["menunggu_jadwal_pertama"]), ("OK", True))
        self.assertEqual(self.cek_json("2026-10-13T21:31+07:00")["harian"]["status"], "HILANG")

    def test_job_lama_tidak_disebut_baru_dan_tanggal_daftar_tampil(self):
        # Job terdaftar 12 Okt, jadwal pertamanya belum tiba pada 16 Okt: jangan disebut "baru didaftarkan".
        self.tambah("mingguan", "0 2 * * 0", "2026-10-12T10:37+07:00")
        c, o, e = jalan(self.f, "cek", "--tanpa-catat", "--sekarang", "2026-10-16T22:00+07:00")
        self.assertEqual(c, 0, e)
        self.assertNotIn("baru didaftarkan", o)
        self.assertIn("terdaftar sejak 12 Okt 10.37 WIB", o)
        c, o, e = jalan(self.f, "daftar", "--sekarang", "2026-10-16T22:00+07:00")
        self.assertIn("terdaftar sejak 12 Okt 10.37 WIB", o)
        self.assertTrue(o.isascii())

    def test_ganti_memulai_ulang_hitungan_terlewat(self):
        self.tambah("harian", "0 21 * * *", "2026-10-12T10:00+07:00")
        self.assertEqual(self.cek_json("2026-10-16T22:00+07:00")["harian"]["terlewat"], 5)
        self.tambah("harian", "0 21 * * *", "2026-10-16T21:50+07:00", "--ganti", "--mulai-ulang")
        j = self.cek_json("2026-10-16T22:00+07:00")["harian"]
        self.assertEqual((j["status"], j["terlewat"]), ("OK", 0))

    def test_ping_sebelum_jadwal_tidak_menutupi_jadwal(self):
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-12T14:00+07:00")    # uji manual siang hari
        j = self.cek_json("2026-10-12T21:40+07:00")["harian"]
        self.assertEqual((j["status"], j["terlewat"]), ("TERLAMBAT", 1))     # jadwal 21.00 hari itu tetap belum dipenuhi

    def test_lintas_tengah_malam_status(self):
        self.tambah("malam", "30 23 * * *")
        self.ping("malam", "2026-10-11T23:31+07:00")
        j = self.cek_json("2026-10-13T00:10+07:00")["malam"]      # 12 Okt 23.30 + 30 mnt toleransi sudah lewat
        self.assertEqual((j["status"], j["lewat_menit"]), ("TERLAMBAT", 40))
        self.assertTrue(j["jadwal_jatuh_tempo_lokal"].startswith("12 Okt 23.30"))

    def test_job_rapat_toleransi_default_separuh_jarak(self):
        c, o, e = jalan(self.f, "tambah", "tiap10", "--jadwal", "*/10 * * * *", "--sekarang", "2026-10-01T08:00+07:00")
        self.assertEqual(c, 0, e)
        self.assertIn("toleransi 5 menit", o)
        c, o, e = jalan(self.f, "tambah", "tiap10b", "--jadwal", "*/10 * * * *", "--toleransi", "20",
                        "--sekarang", "2026-10-01T08:00+07:00")
        self.assertIn("Peringatan", o)

    def test_semua_ok_dan_laporan_ringkas(self):
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-12T21:01+07:00")
        c, o, e = jalan(self.f, "cek", "--hanya-masalah", "--sekarang", "2026-10-12T22:00+07:00")
        self.assertEqual((c, o.strip()), (0, "SEMUA_OK"))
        c, o, e = jalan(self.f, "cek", "--sekarang", "2026-10-12T22:00+07:00")
        self.assertIn("Semua 1 job aman.", o)
        self.assertTrue(o.isascii())

    def test_laporan_pisah_bermasalah_dan_ok(self):
        self.tambah("laporan-harian", "0 21 * * *")
        self.tambah("tagih-piutang", "45 7 * * 1-5")
        self.tambah("backup-data", "0 2 * * 0")
        self.ping("laporan-harian", "2026-10-11T21:03+07:00")
        self.ping("tagih-piutang", "2026-10-12T07:46+07:00")
        c, o, e = jalan(self.f, "cek", "--tanpa-catat", "--sekarang", "2026-10-12T21:40+07:00")
        self.assertIn("BERMASALAH (2 dari 3):", o)
        self.assertIn("OK (1):", o)
        self.assertNotIn("job bermasalah", o)
        baris = o.splitlines()
        i_masalah = baris.index("BERMASALAH (2 dari 3):")
        i_ok = baris.index("OK (1):")
        self.assertLess(i_masalah, i_ok)
        antara = baris[i_masalah + 1:i_ok]
        self.assertEqual(len(antara), 2)
        self.assertTrue(any(b.startswith("- HILANG backup-data") for b in antara))
        self.assertTrue(any(b.startswith("- TERLAMBAT laporan-harian") for b in antara))
        sesudah_ok = baris[i_ok + 1:]
        self.assertEqual(len(sesudah_ok), 1)
        self.assertTrue(sesudah_ok[0].startswith("- tagih-piutang:"))
        # tidak ada job OK di blok bermasalah, tidak ada job bermasalah di blok OK
        self.assertFalse(any("tagih-piutang" in b for b in antara))
        self.assertTrue(o.isascii())

    def test_laporan_hanya_masalah_pisah_blok_ok(self):
        self.tambah("harian", "0 21 * * *")
        self.tambah("pagi", "45 7 * * *")
        self.ping("harian", "2026-10-11T21:03+07:00")
        self.ping("pagi", "2026-10-12T07:46+07:00")
        c, o, e = jalan(self.f, "cek", "--hanya-masalah", "--tanpa-catat", "--sekarang", "2026-10-12T21:40+07:00")
        baris = o.splitlines()
        self.assertEqual(baris[1], "BERMASALAH (1 dari 2):")
        self.assertTrue(baris[2].startswith("- TERLAMBAT harian"))
        self.assertEqual(baris[3], "OK (1): pagi")

    def test_laporan_semua_aman_tetap_ada_blok_ok(self):
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-12T21:01+07:00")
        c, o, e = jalan(self.f, "cek", "--sekarang", "2026-10-12T22:00+07:00")
        self.assertNotIn("BERMASALAH", o)
        self.assertIn("OK (1):", o)


class ZonaWaktu(Dasar):
    def test_wita_dan_wit_memakai_jam_setempat(self):
        self.tambah("wita", "0 22 * * *", "2026-10-01T08:00+07:00", "--zona", "WITA")
        self.ping("wita", "2026-10-12T21:30+07:00")      # = 22.30 WITA, setelah jadwal 22.00
        self.assertEqual(self.cek_json("2026-10-12T22:00+07:00")["wita"]["status"], "OK")   # 23.00 WITA, 22.00 sudah dipenuhi
        self.tambah("wit", "0 23 * * *", "2026-10-01T08:00+07:00", "--zona", "Asia/Jayapura")
        j = self.cek_json("2026-10-12T21:40+07:00")["wit"]       # 23.40 WIT -> jadwal 23.00 WIT terlewat
        self.assertEqual((j["zona"], j["status"], j["lewat_menit"]), ("WIT", "HILANG", 40))

    def test_zona_tak_dikenal_ditolak(self):
        c, o, e = jalan(self.f, "tambah", "x", "--jam", "21.00", "--zona", "Mars/Olympus")
        self.assertEqual(c, 1)
        self.assertIn("Zona", e)
        with self.assertRaises(pc.GalatPantau):
            pc.baca_waktu_utc("kemarin sore")


class AlarmDanInputRusak(Dasar):
    def test_alarm_tidak_diulang_lalu_pulih(self):
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-11T21:01+07:00")
        c, o1, _ = jalan(self.f, "cek", "--hanya-masalah", "--sekarang", "2026-10-12T22:00+07:00")
        self.assertTrue(o1.startswith("PANTAU CRON"))
        c, o2, _ = jalan(self.f, "cek", "--hanya-masalah", "--sekarang", "2026-10-12T23:00+07:00")    # 1 jam kemudian
        self.assertEqual(o2.strip(), "SUDAH_DIKABARKAN")
        c, o3, _ = jalan(self.f, "cek", "--hanya-masalah", "--sekarang", "2026-10-13T05:00+07:00")    # > 6 jam: ingatkan lagi
        self.assertTrue(o3.startswith("PANTAU CRON"))
        self.ping("harian", "2026-10-13T05:10+07:00")
        c, o4, _ = jalan(self.f, "cek", "--hanya-masalah", "--sekarang", "2026-10-13T05:20+07:00")
        self.assertIn("PULIH harian", o4)
        c, o5, _ = jalan(self.f, "cek", "--hanya-masalah", "--sekarang", "2026-10-13T06:20+07:00")
        self.assertEqual(o5.strip(), "SEMUA_OK")

    def test_mode_openclaw_senyap_saat_tenang(self):
        self.assertEqual(jalan(self.f, "cek", "--openclaw")[1].strip(), "NO_REPLY")      # belum ada job
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-12T21:01+07:00")
        self.assertEqual(jalan(self.f, "cek", "--openclaw", "--sekarang", "2026-10-12T22:00+07:00")[1].strip(), "NO_REPLY")
        c, o, e = jalan(self.f, "cek", "--openclaw", "--kode-keluar", "--sekarang", "2026-10-14T22:00+07:00")
        self.assertEqual(c, 0)
        self.assertTrue(o.startswith("PANTAU CRON"))
        self.assertEqual(jalan(self.f, "cek", "--openclaw", "--sekarang", "2026-10-14T22:30+07:00")[1].strip(), "NO_REPLY")

    def test_kode_keluar_dan_belum_ada_job(self):
        c, o, e = jalan(self.f, "cek", "--hanya-masalah")
        self.assertEqual((c, o.strip()), (0, "BELUM_ADA_JOB"))
        self.tambah("harian", "0 21 * * *")
        c, o, e = jalan(self.f, "cek", "--kode-keluar", "--sekarang", "2026-10-02T21:40+07:00")
        self.assertEqual(c, 2)

    def test_berkas_rusak_tidak_ditimpa(self):
        os.makedirs(self.f, exist_ok=True)
        with open(os.path.join(self.f, "jobs.json"), "w") as fh:
            fh.write("{bukan json")
        c, o, e = jalan(self.f, "tambah", "x", "--jam", "21.00")
        self.assertEqual(c, 1)
        self.assertIn("rusak", e)
        with open(os.path.join(self.f, "jobs.json")) as fh:
            self.assertEqual(fh.read(), "{bukan json")

    def test_baris_ping_rusak_dilewati_dan_input_aneh(self):
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-11T21:01+07:00")
        with open(os.path.join(self.f, "ping", "harian.log"), "a") as fh:
            fh.write("sampah tanpa tanggal\n\t\n2026-13-45T99:99:99Z\tx\n")
        j = self.cek_json("2026-10-12T21:10+07:00")["harian"]
        self.assertEqual(j["status"], "OK")
        for args in (["ping", "tidak-ada"], ["tambah", "!!!", "--jam", "21.00"], ["tambah", "a", "--jam", "25.99"],
                     ["tambah", "a"], ["tambah", "a", "--jam", "21.00", "--toleransi", "0"],
                     ["tambah", "a", "--jadwal", "* * * *"], ["riwayat", "tidak-ada"], ["hapus", "tidak-ada"]):
            c, o, e = jalan(self.f, *args)
            self.assertEqual(c, 1, args)
            self.assertTrue(e.startswith("GALAT:"), args)

    def test_tambah_ganda_dan_hapus(self):
        self.tambah("harian", "0 21 * * *")
        c, o, e = jalan(self.f, "tambah", "harian", "--jam", "22.00")
        self.assertEqual(c, 1)
        c, o, e = jalan(self.f, "tambah", "harian", "--jam", "22.00", "--ganti")
        self.assertEqual(c, 0, e)
        c, o, e = jalan(self.f, "hapus", "harian")
        self.assertEqual(c, 0, e)
        self.assertEqual(jalan(self.f, "cek", "--hanya-masalah")[1].strip(), "BELUM_ADA_JOB")

    def test_riwayat_menandai_di_luar_toleransi(self):
        self.tambah("harian", "0 21 * * *")
        self.ping("harian", "2026-10-11T21:05+07:00")
        self.ping("harian", "2026-10-12T23:00+07:00")
        c, o, e = jalan(self.f, "riwayat", "harian", "--json")
        r = json.loads(o)["riwayat"]
        self.assertEqual([x["dalam_toleransi"] for x in r], [False, True])    # terbaru dulu
        self.assertEqual(r[0]["selisih_menit"], 120)

    def test_nama_job_dinormalkan(self):
        self.assertEqual(pc.slug("Laporan Harian 21.00"), "laporan-harian-21-00")
        self.assertEqual(pc.slug("Piutang_Pagi"), "piutang-pagi")
        with self.assertRaises(pc.GalatPantau):
            pc.slug("???")
        self.assertNotIn("/", pc.slug("../../etc/passwd"))


class LayananLuar(Dasar):
    def test_ping_layanan_luar_milik_pengguna_tanpa_bocor_url(self):
        dipanggil = []

        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                dipanggil.append(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")

            def log_message(self, *a):
                pass

        srv = HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            self.tambah("harian", "0 21 * * *")
            url = "http://127.0.0.1:%d/ping/rahasia-uji" % srv.server_port
            with open(os.path.join(self.f, "healthchecks.json"), "w") as fh:
                json.dump({"harian": url}, fh)
            c, o, e = jalan(self.f, "ping", "harian")
            self.assertEqual(c, 0, e)
            self.assertEqual(dipanggil, ["/ping/rahasia-uji"])
            self.assertNotIn("rahasia-uji", o + e)
            jalan(self.f, "ping", "harian", "--tanpa-luar")
            self.assertEqual(len(dipanggil), 1)
        finally:
            srv.shutdown()
            srv.server_close()

    def test_layanan_luar_mati_tidak_menggagalkan_job(self):
        self.tambah("harian", "0 21 * * *")
        with open(os.path.join(self.f, "healthchecks.json"), "w") as fh:
            json.dump({"harian": "http://127.0.0.1:9/ping/x"}, fh)
        c, o, e = jalan(self.f, "ping", "harian")
        self.assertEqual(c, 0)
        self.assertIn("Peringatan", e)
        self.assertEqual(len(pc.baca_ping(self.f, "harian")), 1)


class GantiMenyimpanRiwayat(Dasar):
    """1.0.6 (a)/(d): --ganti tidak menghapus riwayat; hitungan lama tetap bila jadwal & zona sama."""

    def test_ganti_jadwal_sama_mempertahankan_hitungan_dan_riwayat(self):
        self.tambah("harian", "0 21 * * *", "2026-10-12T10:00+07:00")
        self.ping("harian", "2026-10-13T21:01+07:00")
        c, o, e = jalan(self.f, "tambah", "harian", "--jadwal", "0 21 * * *", "--toleransi", "45", "--ganti",
                        "--sekarang", "2026-10-16T21:50+07:00")
        self.assertEqual(c, 0, e)
        self.assertIn("dipertahankan", o)
        self.assertNotIn("mulai ulang", o.lower())
        j = self.cek_json("2026-10-16T22:00+07:00")["harian"]
        self.assertEqual((j["status"], j["terlewat"], j["toleransi_menit"]), ("HILANG", 3, 45))
        self.assertEqual(len(pc.baca_ping(self.f, "harian")), 1)
        self.assertIn("12 Okt 10.00 WIB", j["terdaftar_lokal"])

    def test_ganti_jadwal_berbeda_mulai_dari_sekarang_riwayat_tetap(self):
        self.tambah("harian", "0 21 * * *", "2026-10-12T10:00+07:00")
        self.ping("harian", "2026-10-13T21:01+07:00")
        self.tambah("harian", "0 22 * * *", "2026-10-16T22:30+07:00", "--ganti")
        j = self.cek_json("2026-10-16T22:40+07:00")["harian"]
        self.assertEqual((j["status"], j["terlewat"]), ("OK", 0))
        self.assertEqual(len(pc.baca_ping(self.f, "harian")), 1)

    def test_mulai_ulang_tanpa_job_lama_ditolak(self):
        c, o, e = jalan(self.f, "tambah", "baru", "--jam", "21.00", "--ganti", "--mulai-ulang")
        self.assertEqual(c, 1)
        self.assertTrue(e.startswith("GALAT:"))


class BungkusJobPerintah(Dasar):
    """1.0.6 (b)/(h): argv lama utuh dengan kutip yang benar; --buang mengembalikan persis; script pemilik tak disentuh."""

    ARGV = [sys.executable, "-c", "import sys; print(\"isi 'laporan' $HOME\"); sys.exit(int(sys.argv[1]))", "0", "--",
            "--folder", "a b"]

    def bungkus(self, argv, *ekstra):
        c, o, e = jalan(self.f, "bungkus", "lap", "--argv-lama", json.dumps(argv), *ekstra)
        self.assertEqual(c, 0, e)
        return o.strip(), e

    def test_argv_lama_utuh_dan_dikembalikan_persis(self):
        self.tambah("lap", "0 21 * * *")
        baru, _ = self.bungkus(self.ARGV)
        baru = json.loads(baru)
        self.assertEqual(baru[baru.index("--") + 1:], self.ARGV)
        self.assertIn("jalankan", baru)
        c, o, e = jalan(self.f, "bungkus", "--buang", "--argv-lama", json.dumps(baru))
        self.assertEqual(c, 0, e)
        self.assertEqual(json.loads(o), self.ARGV)

    def test_perintah_edit_berkutip_benar(self):
        import shlex
        self.tambah("lap", "0 21 * * *")
        o, _ = self.bungkus(self.ARGV, "--id", "id 1")
        bagian = shlex.split(o)
        self.assertEqual(bagian[:4], ["openclaw", "automations", "edit", "id 1"])
        self.assertEqual(bagian[4], "--command-argv")
        argv = json.loads(bagian[5])
        self.assertEqual(argv[argv.index("--") + 1:], self.ARGV)

    def _jalan_bungkus(self, kode):
        argv = list(self.ARGV)
        argv[3] = str(kode)
        baru, _ = self.bungkus(argv)
        return subprocess.run(json.loads(baru), capture_output=True, text=True, encoding="utf-8")

    def test_jalankan_meneruskan_keluaran_dan_ping_hanya_bila_sukses(self):
        self.tambah("lap", "0 21 * * *")
        p = self._jalan_bungkus(0)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "isi 'laporan' $HOME")       # keluaran job utuh, tanpa catatan pantauan
        self.assertEqual(p.stderr, "")                                  # 1.0.6 putaran 2: sukses = diam total
        self.assertEqual(len(pc.baca_ping(self.f, "lap")), 1)
        p = self._jalan_bungkus(3)
        self.assertEqual(p.returncode, 3)
        self.assertEqual(len(pc.baca_ping(self.f, "lap")), 1)

    def test_jalankan_dimatikan_sinyal_kode_128_plus(self):
        if os.name == "nt":
            self.skipTest("sinyal POSIX")
        self.tambah("lap", "0 21 * * *")
        baru, _ = self.bungkus([sys.executable, "-c", "import os, signal; os.kill(os.getpid(), signal.SIGTERM)"])
        p = subprocess.run(json.loads(baru), capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(p.returncode, 128 + 15)
        self.assertEqual(pc.baca_ping(self.f, "lap"), [])

    def test_jalankan_job_tidak_terdaftar_peringatan_saja(self):
        baru, _ = self.bungkus([sys.executable, "-c", "print('ok')"])
        p = subprocess.run(json.loads(baru), capture_output=True, text=True, encoding="utf-8")
        self.assertEqual((p.returncode, p.stdout.strip()), (0, "ok"))
        self.assertIn("Peringatan pantauan", p.stderr)

    def test_perintah_tidak_ada_tidak_ping(self):
        self.tambah("lap", "0 21 * * *")
        baru, _ = self.bungkus(["/tidak/ada/program-xyz"])
        p = subprocess.run(json.loads(baru), capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(p.returncode, 127)
        self.assertEqual(pc.baca_ping(self.f, "lap"), [])

    def test_tidak_dibungkus_dua_kali_dan_ping_pemilik_tidak_disentuh(self):
        self.tambah("lap", "0 21 * * *")
        baru, _ = self.bungkus(["python3", "/rumah/lap.py"])
        lagi, e = self.bungkus(json.loads(baru))
        self.assertEqual(json.loads(lagi), json.loads(baru))
        self.assertIn("tidak dibungkus dua kali", e)
        milik = ["sh", "-c", "python3 /rumah/lap.py && python3 /x/scripts/pantau_cron.py ping lap"]
        for args in (["bungkus", "--buang"], ["bungkus", "lap"]):
            c, o, e = jalan(self.f, *(args + ["--argv-lama", json.dumps(milik)]))
            self.assertEqual(c, 1, args)
            self.assertEqual(o, "")

    def test_argv_rusak_ditolak(self):
        for buruk in ("bukan json", "[]", '["a", 1]', '{"a": 1}', '[""]'):
            c, o, e = jalan(self.f, "bungkus", "lap", "--argv-lama", buruk)
            self.assertEqual(c, 1, buruk)
            self.assertTrue(e.startswith("GALAT:"), buruk)


class TerimaLaporTanpaPengawasan(Dasar):
    """1.0.6 putaran 2 (h): berhenti memantau job yang ping-nya ada di perintah buatan pemilik."""

    def test_hapus_biasa_membuat_ping_galat(self):
        self.tambah("backup", "0 2 * * 0")
        self.assertEqual(jalan(self.f, "hapus", "backup")[0], 0)
        c, o, e = jalan(self.f, "ping", "backup")
        self.assertEqual(c, 1)
        self.assertIn("belum terdaftar", e)

    def test_terima_lapor_ping_kode_0_tidak_dicatat_dan_tidak_diawasi(self):
        self.tambah("backup", "0 2 * * 0", "2026-10-01T08:00+07:00")
        self.tambah("piutang", "45 7 * * 1-5", "2026-10-01T08:00+07:00")
        self.ping("backup", "2026-10-04T02:01+07:00")
        c, o, e = jalan(self.f, "hapus", "backup", "--terima-lapor")
        self.assertEqual(c, 0, e)
        self.assertIn("tidak diawasi lagi", o)
        c, o, e = jalan(self.f, "ping", "backup", "--sekarang", "2026-10-11T02:01+07:00")
        self.assertEqual((c, e), (0, ""))
        self.assertEqual(len(pc.baca_ping(self.f, "backup")), 1)     # riwayat lama tetap, ping baru tak dicatat
        jobs = self.cek_json("2026-10-30T09:00+07:00")
        self.assertNotIn("backup", jobs)                            # tidak pernah HILANG/TERLAMBAT lagi
        self.assertIn("piutang", jobs)
        c, o, e = jalan(self.f, "daftar", "--json")
        self.assertEqual(json.loads(o)["tidak_diawasi"], ["backup"])
        c, o, e = jalan(self.f, "cek", "--openclaw", "--sekarang", "2026-10-30T09:00+07:00")
        self.assertNotIn("backup", o)

    def test_terima_lapor_lewat_bungkus_jalankan_tetap_kode_0(self):
        self.tambah("lap", "0 21 * * *")
        c, baru, e = jalan(self.f, "bungkus", "lap", "--argv-lama", json.dumps([sys.executable, "-c", "print(1)"]))
        self.assertEqual(jalan(self.f, "hapus", "lap", "--terima-lapor")[0], 0)
        p = subprocess.run(json.loads(baru), capture_output=True, text=True, encoding="utf-8")
        self.assertEqual((p.returncode, p.stderr), (0, ""))

    def test_diawasi_lagi_dengan_tambah(self):
        self.tambah("backup", "0 2 * * 0")
        jalan(self.f, "hapus", "backup", "--terima-lapor")
        self.tambah("backup", "0 2 * * 0", "2026-10-20T08:00+07:00")   # tanpa --ganti
        self.ping("backup", "2026-10-25T02:01+07:00")
        self.assertEqual(len(pc.baca_ping(self.f, "backup")), 1)
        self.assertIn("backup", self.cek_json("2026-10-25T03:00+07:00"))

    def test_ping_job_dilepas_diam_total(self):
        """1.0.6 putaran 3: ping job yang dilepas tidak mencetak apa pun (keluaran job perintah bisa ke chat)."""
        self.tambah("backup", "0 2 * * 0")
        jalan(self.f, "hapus", "backup", "--terima-lapor")
        self.assertEqual(jalan(self.f, "ping", "backup", "--sekarang", "2026-10-11T02:01+07:00"), (0, "", ""))

    def test_tambah_ulang_ganti_sesudah_dilepas_tanpa_hilang_palsu(self):
        """1.0.6 putaran 3: urutan persis temuan; --ganti dengan jadwal sama tidak memakai `dibuat` lama."""
        c, o, e = jalan(self.f, "tambah", "lap", "--jam", "21.00", "--sekarang", "2026-10-01T10:00+07:00")
        self.assertEqual(c, 0, e)
        self.ping("lap", "2026-10-01T21:05+07:00")
        self.assertEqual(jalan(self.f, "hapus", "lap", "--terima-lapor")[0], 0)
        self.ping("lap", "2026-10-05T21:05+07:00")
        c, o, e = jalan(self.f, "tambah", "lap", "--jam", "21.00", "--ganti", "--sekarang", "2026-10-10T10:00+07:00")
        self.assertEqual(c, 0, e)
        self.assertNotIn("Riwayat dan hitungan lama dipertahankan", o)
        self.assertIn("hitungan terlewat dimulai dari sekarang", o)
        self.assertEqual(len(pc.baca_ping(self.f, "lap")), 1)        # riwayat lama tetap
        for saat in ("2026-10-10T10:00+07:00", "2026-10-10T21:20+07:00"):
            j = self.cek_json(saat)["lap"]
            self.assertNotIn(j["status"], ("HILANG", "TERLAMBAT"), (saat, j))
        c, o, e = jalan(self.f, "cek", "--openclaw", "--tanpa-catat", "--sekarang", "2026-10-10T10:00+07:00")
        self.assertNotIn("HILANG", o)
        self.assertEqual(self.cek_json("2026-10-11T22:00+07:00")["lap"]["status"], "HILANG")   # pengawasan hidup lagi

    def test_terima_lapor_job_tidak_ada_galat(self):
        c, o, e = jalan(self.f, "hapus", "tidak-ada", "--terima-lapor")
        self.assertEqual(c, 1)
        self.assertTrue(e.startswith("GALAT:"))


class Versi(unittest.TestCase):
    def test_versi_sama_di_semua_tempat(self):
        def baca(*b):
            with open(os.path.join(AKAR, *b), encoding="utf-8") as fh:
                return fh.read()
        self.assertEqual(pc.VERSI, "1.0.6")
        p = subprocess.run([sys.executable, SCRIPT, "--versi"], capture_output=True, text=True)
        self.assertEqual(p.stdout.strip(), pc.VERSI)
        self.assertIn("_Versi skill: %s_" % pc.VERSI, baca("SKILL.md"))
        self.assertIn("Versi terkini: **%s**" % pc.VERSI, baca("README.md"))
        import re
        self.assertEqual(re.search(r"## Catatan revisi (\S+)", baca("CHANGELOG.md")).group(1), pc.VERSI)


class KonsistensiTeksPetunjuk(unittest.TestCase):
    """Teks "Aturan penutup" yang ditambahkan ke prompt jadwal harus sama di SKILL.md dan references,
    aman dipakai di --message "...", dan teks lama (penyebab isi laporan hilang) tidak boleh kembali."""

    @staticmethod
    def _baca(*bagian):
        with open(os.path.join(AKAR, *bagian), encoding="utf-8") as fh:
            return fh.read()

    def _teks_penutup(self, isi):
        import re
        m = re.search(r"Aturan penutup \(wajib\):.*?(?=`\n|\"\n)", isi, re.S)
        self.assertIsNotNone(m, "teks Aturan penutup tidak ditemukan")
        return m.group(0)

    def test_teks_penutup_sama_di_skill_dan_references(self):
        sk = self._teks_penutup(self._baca("SKILL.md"))
        ref = self._teks_penutup(self._baca("references", "openclaw-jadwal.md")).replace("laporan-harian", "<nama>")
        self.assertEqual(sk, ref)

    def test_teks_penutup_aman_dan_lengkap(self):
        t = self._teks_penutup(self._baca("SKILL.md"))
        for karakter in ['"', "$", "`", "!"]:
            self.assertNotIn(karakter, t)
        self.assertNotIn("\n", t)
        for kata in ["jangan menulis laporan sebagai teks dulu", "diam-diam", "balasan akhir",
                     "LENGKAP", "pesan terakhir", "pantau_cron.py ping <nama>", "sudah final"]:
            self.assertIn(kata, t)

    def test_teks_lama_tidak_ada_di_petunjuk_aktif(self):
        lama = "dan pesan sudah terkirim: jalankan perintah"
        for bagian in (("SKILL.md",), ("references", "openclaw-jadwal.md")):
            isi = self._baca(*bagian)
            # boleh disebut hanya sebagai kutipan "teks lama yang harus diganti"
            for baris in isi.splitlines():
                if lama in baris:
                    self.assertTrue("GANTI" in baris or "Teks lama" in baris or "versi sebelumnya" in baris,
                                    "teks lama dipakai sebagai petunjuk: " + baris[:80])

    def test_rencana_wajib_menyebut_uji_jalan_sekali(self):
        isi = self._baca("SKILL.md")
        self.assertIn("Setelah Anda balas ya, tiap jadwal saya jalankan sekali untuk uji", isi)
        self.assertIn("mau saya hapus", isi)

    KALIMAT_TAK_TERBACA = "Daftar jadwal OpenClaw Anda tidak terbaca utuh, jadi saya tidak mengubah apa pun."

    def test_c_kalimat_daftar_tak_terbaca_seragam(self):
        sk = self._baca("SKILL.md")
        ref = self._baca("references", "openclaw-jadwal.md")
        self.assertIn(self.KALIMAT_TAK_TERBACA, sk)
        bag1b = ref.split("## 1b.", 1)[1].split("\n## ", 1)[0]
        self.assertIn(self.KALIMAT_TAK_TERBACA, bag1b)
        for isi in (sk, ref):   # tidak ada variasi lain dari kalimat itu
            self.assertEqual(isi.count("tidak terbaca utuh, jadi"), isi.count(self.KALIMAT_TAK_TERBACA))

    def test_a_f_pengawas_lama_dikenali_dan_label_berbeda(self):
        sk = self._baca("SKILL.md")
        for frasa in ("Pengawas yang SUDAH ada di daftar jadwal OpenClaw", "topik lain lagi", "pakai yang lama",
                      "pindahkan ke obrolan ini", "tidak pernah ditambah dobel", "--mulai-ulang"):
            self.assertIn(frasa, sk)
        self.assertIn("topik lain lagi", self._baca("references", "openclaw-jadwal.md"))

    def test_b_job_perintah_lewat_bungkus(self):
        for bagian in (("SKILL.md",), ("references", "openclaw-jadwal.md")):
            isi = self._baca(*bagian)
            self.assertIn("bungkus", isi)
            self.assertIn("UTUH", isi)
        self.assertNotIn("tambahkan `ping` sebagai perintah terakhir di script", self._baca("SKILL.md"))

    def test_a2_pengawas_dobel_dirapikan(self):
        sk = self._baca("SKILL.md")
        for frasa in ("**Ada set ke obrolan ini DAN set lain**", "bawaan **rapikan**", "**biarkan**",
                      "  - rapikan: \"pakai pengawas yang sudah ada di obrolan ini", "Rapikan/lengkapi: sesudah set di obrolan ini terlihat utuh",
                      "Balas ya = pakai yang di obrolan ini dan hapus yang ke <label>", "pakai yang lama, rapikan, atau biarkan"):
            self.assertIn(frasa, sk)
        self.assertNotIn("set yang sudah mengarah ke obrolan ini dipakai; bila tidak ada", sk)
        self.assertIn("rapikan", self._baca("references", "openclaw-jadwal.md").split("## 1b.", 1)[1].split("\n## ", 1)[0])

    def test_d2_pc4_bawaan_rapikan_bukan_pindah(self):
        pc4 = self._baca("examples", "HASIL-UJI.md").split("Harapan uji ulang PC4", 1)[1]
        self.assertIn("**rapikan**", pc4)
        self.assertNotIn("bawaan \"ya\" = pindah", pc4)
        self.assertNotIn("set baru terpasang", pc4)
        self.assertIn("tidak ada pengawas baru yang dipasang", pc4)

    def test_ganti_jadwal_berbeda_tidak_diklaim_hitungan_tetap(self):
        sk = self._baca("SKILL.md")
        self.assertNotIn("bila jadwal/toleransi berbeda cukup", sk)
        self.assertIn("Jadwal atau zona berbeda -> `tambah <nama> --jadwal \"<jadwal baru>\" --ganti`: script otomatis memulai", sk)

    def test_g2_tidak_ada_tiga_pertanyaan_wajib(self):
        sk = self._baca("SKILL.md")
        self.assertNotIn("tiga pertanyaan)", sk)
        self.assertNotIn("bila tiga pertanyaan tidak dijawab", sk)

    def test_h2_berhenti_memantau_perintah_pemilik_terima_lapor(self):
        sk = self._baca("SKILL.md")
        self.assertIn("`hapus <nama> --terima-lapor` (BUKAN `hapus <nama>` biasa", sk)
        self.assertNotIn("Tanpa pengawas, langkah itu tidak mengirim kabar apa pun", sk)
        self.assertIn("--terima-lapor", self._baca("references", "openclaw-jadwal.md"))
        ex = self._baca("examples", "05-berhenti-memantau-dan-jawaban-tidak.md")
        self.assertNotIn("Tanpa pengawas", ex)
        b = ex.split("## B.", 1)[1].split("## C.", 1)[0]
        self.assertIn("--terima-lapor", b)
        self.assertLess(b.index("Backup mingguan"), b.index("**Pemilik:** ya"))   # disebut di rencananya sendiri

    def test_d_harapan_pc4_sesuai_skill(self):
        h = self._baca("examples", "HASIL-UJI.md")
        self.assertIn("Harapan uji ulang PC4", h)
        pc4 = h.split("Harapan uji ulang PC4", 1)[1]
        for baris in pc4.splitlines():
            if "mulai ulang" in baris:
                self.assertIn("tidak ada", baris, baris[:80])
        self.assertIn("JANGAN menulis kalimat \"hitungannya saya mulai ulang\"", self._baca("SKILL.md"))

    def test_e_baris_uji_peringatan_bersyarat_dan_varian_tujuan(self):
        sk = self._baca("SKILL.md")
        self.assertIn("baris ini HANYA bila pengawas dipasang baru, dipindah, atau diubah", sk)
        self.assertIn("- Tujuan kabar: SATU varian saja:", sk)
        self.assertIn("pakai yang lama: \"tetap ke <label>", sk)
        self.assertIn("(pakai yang lama: \"Tujuan kabar saat ini: tetap ke <label>", sk)

    def test_g_penutup_tidak_menanyakan_yang_sudah_disebut(self):
        sk = self._baca("SKILL.md")
        self.assertNotIn("Tepat tiga pertanyaan", sk)
        self.assertIn("Paling banyak tiga pertanyaan", sk)
        self.assertIn("SUDAH disebut pemilik DIHAPUS", sk)
        self.assertIn("Tidak ada pertanyaan lagi; balas ya untuk mulai.", sk)

    def test_h_berhenti_memantau(self):
        sk = self._baca("SKILL.md")
        self.assertIn("JANGAN PERNAH mengubah berkas script/perintah milik pemilik", sk)
        self.assertIn("baca ulang daftar jadwal SEBELUM menulis \"sudah dihapus\"", sk)
        self.assertIn("bungkus --buang", sk)
        ex = self._baca("examples", "05-berhenti-memantau-dan-jawaban-tidak.md")
        self.assertIn("**Pemilik:** tidak", ex)
        self.assertIn("tidak ada yang saya ubah", ex)

    def test_p3_mode_terblokir_tanpa_daftar_lokal_saat_tak_terbaca(self):
        sk = self._baca("SKILL.md")
        mt = sk.split("## Mode terblokir", 1)[1].split("\n## ", 1)[0]
        self.assertNotIn("Pekerjaan lokal tetap jalan (daftar job", mt)   # aturan lama tanpa pengecualian
        self.assertIn("Pekerjaan lokal tetap jalan HANYA untuk galat izin", mt)
        self.assertIn("daftar tidak terbaca utuh atau galat bukan soal izin -> TIDAK ada pendaftaran lokal sama sekali", mt)
        bag1b = self._baca("references", "openclaw-jadwal.md").split("## 1b.", 1)[1].split("\n## ", 1)[0]
        self.assertIn("jangan mendaftarkan apa pun ke pantauan lokal", bag1b)

    def test_p3_uji_alarm_selalu_hapus_riwayat(self):
        for isi in (self._baca("SKILL.md"), self._baca("references", "openclaw-jadwal.md")):
            self.assertEqual(isi.count("hapus uji-alarm"), isi.count("hapus uji-alarm --hapus-riwayat"))

    def test_p3_set_pengawas_tidak_utuh(self):
        sk = self._baca("SKILL.md")
        for frasa in ("**Set tidak utuh**", "Bawaan **lengkapi**", "  - lengkapi: \"", "Pengawas belum lengkap:",
                      "Rapikan/lengkapi: sesudah set di obrolan ini terlihat utuh"):
            self.assertIn(frasa, sk)
        self.assertIn("set tidak utuh", self._baca("references", "openclaw-jadwal.md").split("## 1b.", 1)[1].split("\n## ", 1)[0])

    def test_p3_aturan_ganti_jadwal_berubah_dan_job_dilepas(self):
        sk = self._baca("SKILL.md")
        ref = self._baca("references", "openclaw-jadwal.md")
        for isi in (sk, ref):
            self.assertNotRegex(isi, r"(jadwal|Jadwal)[^.\n]{0,20}toleransi berbeda[^.\n]{0,40}--ganti[^.\n]{0,60}hitungan (lama )?tetap")
        self.assertIn("Jadwal atau zona berubah -> script otomatis memulai hitungan dari sekarang", ref)
        self.assertIn("**tidak diawasi** (pernah dilepas dengan `hapus --terima-lapor`)", sk)
        self.assertIn("didaftarkan lagi -> hitungan selalu dimulai dari sekarang", ref)
        self.assertIn("tidak dicatat, dan tidak mengirim kabar apa pun", sk)   # kalimat ke pemilik tetap benar (ping diam)

    def test_i_galat_lain_baca_ulang_sebelum_daftar_lokal(self):
        sk = self._baca("SKILL.md")
        self.assertIn("baca ulang (5c) dulu, sebelum mendaftarkan lokal (5a)", sk)
        self.assertIn("a. **Catat ke pantauan lokal**", sk)
        self.assertIn("c. **Baca ulang**", sk)
        self.assertIn("(SKILL.md 5c) DULU, sebelum mendaftarkan lokal (5a)", self._baca("references", "openclaw-jadwal.md"))

    def test_skill_ringkas_dan_frontmatter(self):
        sk = self._baca("SKILL.md")
        self.assertLess(len(sk.splitlines()), 300)
        fm = sk.split("---", 2)[1]
        self.assertEqual([b.split(":", 1)[0] for b in fm.strip().splitlines()], ["name", "description"])

    def test_larangan_membuka_catatan_harian(self):
        for bagian in (("SKILL.md",), ("references", "openclaw-jadwal.md")):
            isi = self._baca(*bagian)
            self.assertIn("MEMORY.md", isi)
            self.assertIn("DILARANG membuka folder catatan harian", isi)


if __name__ == "__main__":
    unittest.main(verbosity=1)
