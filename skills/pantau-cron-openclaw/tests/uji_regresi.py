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
        self.tambah("harian", "0 21 * * *", "2026-10-16T21:50+07:00", "--ganti")
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

    def test_larangan_membuka_catatan_harian(self):
        for bagian in (("SKILL.md",), ("references", "openclaw-jadwal.md")):
            isi = self._baca(*bagian)
            self.assertIn("MEMORY.md", isi)
            self.assertIn("DILARANG membuka folder catatan harian", isi)


if __name__ == "__main__":
    unittest.main(verbosity=1)
