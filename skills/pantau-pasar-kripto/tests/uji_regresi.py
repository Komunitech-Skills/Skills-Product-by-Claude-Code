#!/usr/bin/env python3
"""Uji regresi pantau-pasar-kripto v1.0.1 -- SEPENUHNYA OFFLINE (tanpa jaringan).

Jalankan: python3 tests/uji_regresi.py
(atau: python3 -m unittest tests/uji_regresi.py -v)

cek_ambang.py hanya diuji lewat mode --harga-file (tidak pernah memanggil fungsi yang
melakukan permintaan jaringan sungguhan). hitung_pl_jurnal.py diuji lewat file CSV
sementara. Mencakup temuan uji independen v1.0.0 (lihat examples/HASIL-UJI.md): B-1
(wrapper cek_dan_lapor.py), S-1..S-6, R-1..R-6.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import cek_ambang  # noqa: E402
import hitung_pl_jurnal  # noqa: E402


def jalankan_cek_ambang(args):
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "cek_ambang.py")] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def jalankan_wrapper(args):
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "cek_dan_lapor.py")] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def jalankan_jurnal(args):
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "hitung_pl_jurnal.py")] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def tulis_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def tulis_teks(path, teks, encoding="utf-8"):
    with open(path, "w", encoding=encoding, newline="") as f:
        f.write(teks)


# ---------------------------------------------------------------------------
# Fungsi murni cek_ambang.py
# ---------------------------------------------------------------------------

class UjiFungsiMurniCekAmbang(unittest.TestCase):

    def test_01_bulat_setengah_ke_atas_rupiah(self):
        self.assertEqual(cek_ambang.bulat_setengah_ke_atas(1500000.5), 1500001)
        self.assertEqual(cek_ambang.bulat_setengah_ke_atas(1500000.4), 1500000)

    def test_02_bulat_setengah_ke_atas_negatif(self):
        self.assertEqual(cek_ambang.bulat_setengah_ke_atas(-2.5, 0), -3)

    def test_03_format_rupiah_pemisah_ribuan(self):
        self.assertEqual(cek_ambang.format_rupiah(1500000000), "Rp 1.500.000.000")

    def test_04_format_rupiah_negatif(self):
        self.assertEqual(cek_ambang.format_rupiah(-50000), "-Rp 50.000")

    def test_05_format_persen_pakai_koma_R4(self):
        self.assertEqual(cek_ambang.format_persen(5.256), "+5,26%")
        self.assertEqual(cek_ambang.format_persen(-5.2), "-5,20%")

    def test_06_format_usd_pakai_koma_desimal(self):
        self.assertEqual(cek_ambang.format_usd(2650.5), "US$ 2.650,50")

    def test_07_format_angka_ringkas(self):
        self.assertEqual(cek_ambang.format_angka_ringkas(5.0), "5")
        self.assertEqual(cek_ambang.format_angka_ringkas(5.5), "5,5")

    def test_08_hitung_persen_perubahan_naik(self):
        self.assertAlmostEqual(cek_ambang.hitung_persen_perubahan(1100, 1000), 10.0)

    def test_09_hitung_persen_perubahan_turun(self):
        self.assertAlmostEqual(cek_ambang.hitung_persen_perubahan(800, 1000), -20.0)

    def test_10_hitung_persen_perubahan_tanpa_acuan(self):
        self.assertIsNone(cek_ambang.hitung_persen_perubahan(1000, None))
        self.assertIsNone(cek_ambang.hitung_persen_perubahan(1000, 0))

    def test_11_evaluasi_ambang_turun_terlewati(self):
        cfg = {"ambang_turun_persen": 5}
        terlewati, detail, tidak_bisa = cek_ambang.evaluasi_ambang(cfg, 950, -6.0, "IDR")
        self.assertTrue(terlewati)
        self.assertIn("Turun", detail[0])
        self.assertEqual(tidak_bisa, [])

    def test_12_evaluasi_ambang_naik_terlewati(self):
        cfg = {"ambang_naik_persen": 5}
        terlewati, detail, _ = cek_ambang.evaluasi_ambang(cfg, 1100, 7.5, "IDR")
        self.assertTrue(terlewati)

    def test_13_evaluasi_ambang_tidak_terlewati(self):
        cfg = {"ambang_naik_persen": 5, "ambang_turun_persen": 5}
        terlewati, detail, tidak_bisa = cek_ambang.evaluasi_ambang(cfg, 1020, 2.0, "IDR")
        self.assertFalse(terlewati)
        self.assertEqual(detail, [])
        self.assertEqual(tidak_bisa, [])

    def test_14_evaluasi_ambang_harga_absolut_atas_terformat_S1(self):
        cfg = {"ambang_harga_di_atas": 1000000}
        terlewati, detail, _ = cek_ambang.evaluasi_ambang(cfg, 1000000, None, "IDR")
        self.assertTrue(terlewati)
        self.assertIn("Rp 1.000.000", detail[0])  # R-4: ambang diformat Rupiah, bukan angka mentah

    def test_15_evaluasi_ambang_harga_absolut_bawah(self):
        cfg = {"ambang_harga_di_bawah": 500}
        terlewati, detail, _ = cek_ambang.evaluasi_ambang(cfg, 400, None, "USD")
        self.assertTrue(terlewati)
        self.assertIn("US$", detail[0])

    def test_16_evaluasi_ambang_persen_tanpa_dasar_pembanding_S1(self):
        cfg = {"ambang_turun_persen": 5}
        terlewati, detail, tidak_bisa = cek_ambang.evaluasi_ambang(cfg, 900, None, "IDR")
        self.assertFalse(terlewati)
        self.assertEqual(detail, [])
        self.assertTrue(any("tidak ada dasar pembanding" in t for t in tidak_bisa))

    def test_17_parse_angka_konfigurasi_persen_teks_R2(self):
        self.assertEqual(cek_ambang._parse_angka_konfigurasi("5%", "x"), 5.0)

    def test_18_parse_angka_konfigurasi_format_id_R2(self):
        self.assertEqual(cek_ambang._parse_angka_konfigurasi("1.450.000.000", "x"), 1450000000.0)
        self.assertEqual(cek_ambang._parse_angka_konfigurasi("1.450.000,50", "x"), 1450000.50)

    def test_19_parse_angka_konfigurasi_nol_ditolak_R2(self):
        with self.assertRaises(cek_ambang.KesalahanInput):
            cek_ambang._parse_angka_konfigurasi(0, "x")
        with self.assertRaises(cek_ambang.KesalahanInput):
            cek_ambang._parse_angka_konfigurasi(-5, "x")

    def test_20_parse_angka_konfigurasi_bukan_angka(self):
        with self.assertRaises(cek_ambang.KesalahanInput):
            cek_ambang._parse_angka_konfigurasi("abc", "x")

    def test_21_kunci_koin_menyertakan_sumber_R3(self):
        koin_cg = {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr"}
        koin_id = {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "sumber": "indodax",
                   "indodax_pair": "btcidr"}
        self.assertNotEqual(cek_ambang.kunci_koin(koin_cg), cek_ambang.kunci_koin(koin_id))

    def test_22_tunggu_retry_429_pakai_retry_after_S2(self):
        self.assertEqual(cek_ambang._tunggu_retry_429("3", 0), 3.0)

    def test_23_tunggu_retry_429_fallback_backoff(self):
        self.assertEqual(cek_ambang._tunggu_retry_429(None, 0), 1.0)
        self.assertEqual(cek_ambang._tunggu_retry_429("bukan-angka", 1), 2.0)

    def test_24_tunggu_retry_429_dibatasi_15_detik(self):
        self.assertEqual(cek_ambang._tunggu_retry_429("999", 0), 15.0)

    def test_25_perbarui_status_notifikasi_baru_terpicu_S3(self):
        import datetime as dt
        notif = {}
        sekarang = dt.datetime(2026, 9, 24, 7, 0, tzinfo=cek_ambang.WIB)
        lapor = cek_ambang.perbarui_status_notifikasi(notif, "btc#0", True, sekarang, 6.0)
        self.assertTrue(lapor)

    def test_26_perbarui_status_notifikasi_diredam_S3(self):
        import datetime as dt
        notif = {"btc#0": {"terlewati": True, "pada": "2026-09-24T07:00:00+07:00"}}
        sekarang = dt.datetime(2026, 9, 24, 8, 0, tzinfo=cek_ambang.WIB)  # +1 jam, < jeda 6 jam
        lapor = cek_ambang.perbarui_status_notifikasi(notif, "btc#0", True, sekarang, 6.0)
        self.assertFalse(lapor)

    def test_27_perbarui_status_notifikasi_lapor_ulang_setelah_jeda_S3(self):
        import datetime as dt
        notif = {"btc#0": {"terlewati": True, "pada": "2026-09-24T07:00:00+07:00"}}
        sekarang = dt.datetime(2026, 9, 24, 14, 0, tzinfo=cek_ambang.WIB)  # +7 jam, > jeda 6 jam
        lapor = cek_ambang.perbarui_status_notifikasi(notif, "btc#0", True, sekarang, 6.0)
        self.assertTrue(lapor)

    def test_28_perbarui_status_notifikasi_reset_saat_pulih_S3(self):
        import datetime as dt
        notif = {"btc#0": {"terlewati": True, "pada": "2026-09-24T07:00:00+07:00"}}
        sekarang = dt.datetime(2026, 9, 24, 7, 30, tzinfo=cek_ambang.WIB)
        lapor = cek_ambang.perbarui_status_notifikasi(notif, "btc#0", False, sekarang, 6.0)
        self.assertFalse(lapor)
        self.assertFalse(notif["btc#0"]["terlewati"])
        # Kondisi terpicu lagi segera setelah pulih -> harus lapor lagi (bukan diredam)
        lapor2 = cek_ambang.perbarui_status_notifikasi(notif, "btc#0", True, sekarang, 6.0)
        self.assertTrue(lapor2)


# ---------------------------------------------------------------------------
# CLI end-to-end cek_ambang.py (--harga-file, offline)
# ---------------------------------------------------------------------------

class UjiProsesCekAmbangViaCLI(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji_kripto_")
        self.cfg_path = os.path.join(self.tmp, "konfigurasi.json")
        self.state_path = os.path.join(self.tmp, "state.json")
        self.harga_path = os.path.join(self.tmp, "harga.json")
        tulis_json(self.state_path, {})

    def test_29_ambang_turun_idr_terpicu_exit_2(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 5},
        ]})
        tulis_json(self.harga_path, {
            "bitcoin_idr_coingecko": {"harga": 1400000000, "perubahan_24jam_persen": -7.0,
                                       "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        data = json.loads(out)
        self.assertTrue(data["perlu_lapor_sekarang"])
        self.assertIn("Rp 1.400.000.000", data["koin"][0]["harga_format"])

    def test_30_ambang_naik_usd_terpicu(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "ETH", "coingecko_id": "ethereum", "mata_uang": "usd", "ambang_naik_persen": 5},
        ]})
        tulis_json(self.harga_path, {
            "ethereum_usd_coingecko": {"harga": 2700.0, "perubahan_24jam_persen": 8.1,
                                        "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        data = json.loads(out)
        self.assertIn("US$", data["koin"][0]["harga_format"])

    def test_31_tidak_ada_ambang_terlewati_exit_0(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr",
             "ambang_naik_persen": 10, "ambang_turun_persen": 10},
        ]})
        tulis_json(self.harga_path, {
            "bitcoin_idr_coingecko": {"harga": 1500000000, "perubahan_24jam_persen": 1.0,
                                       "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 0, err)

    def test_32_sumber_gagal_tanpa_cache_exit_3_tanpa_mengarang_harga(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "SOL", "coingecko_id": "solana", "mata_uang": "usd", "ambang_turun_persen": 10},
        ]})
        tulis_json(self.harga_path, {})  # SOL tidak ada -> simulasi gagal
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 3, err)
        data = json.loads(out)
        self.assertEqual(data["koin"][0]["status"], "gagal_total")
        self.assertIsNone(data["koin"][0]["harga"])
        self.assertIn("TIDAK BISA DICEK", data["pesan_singkat"])  # S-1: bukan didiamkan

    def test_33_sumber_gagal_dengan_cache_pakai_data_basi(self):
        tulis_json(self.state_path, {
            "solana_usd_coingecko": {"harga_terakhir": 150.0, "jam_data_terakhir": "2026-09-20T07:00:00+07:00",
                                      "sumber_terakhir": "coingecko"},
        })
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "SOL", "coingecko_id": "solana", "mata_uang": "usd", "ambang_turun_persen": 50},
        ]})
        tulis_json(self.harga_path, {})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
            "--usia-basi-jam", "6",
        ])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["koin"][0]["status"], "cache")
        self.assertTrue(any("DATA BASI" in p for p in data["koin"][0]["peringatan"]))
        self.assertTrue(any("lebih tua dari batas" in p for p in data["koin"][0]["peringatan"]))
        # S-1: pesan_singkat wajib memuat sumber & jam data
        self.assertIn("sumber:", data["pesan_singkat"])
        self.assertIn("data jam", data["pesan_singkat"])

    def test_34_state_json_rusak_tidak_lagi_exit_1_R3(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            f.write("{ini bukan json valid")
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "coingecko_id": "bitcoin",
                                              "mata_uang": "idr", "ambang_turun_persen": 5}]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1500000000, "perubahan_24jam_persen": 0,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 0, err)  # dulu exit 1 (semua pemantauan berhenti) -- sekarang tetap jalan
        data = json.loads(out)
        self.assertTrue(any("dicadangkan" in p for p in data["peringatan_global"]))
        cadangan = [f for f in os.listdir(self.tmp) if f.startswith("state.json.rusak-")]
        self.assertEqual(len(cadangan), 1)

    def test_35_konfigurasi_json_rusak_exit_1(self):
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            f.write("{bukan json")
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)

    def test_36_konfigurasi_tanpa_ambang_sama_sekali_exit_1(self):
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "mata_uang": "idr"}]})
        tulis_json(self.harga_path, {})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertIn("ambang", data["pesan"].lower())

    def test_37_konfigurasi_mata_uang_tidak_valid_exit_1(self):
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "mata_uang": "eur", "ambang_turun_persen": 5}]})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)

    def test_38_ambang_nol_ditolak_exit_1_R2(self):
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "coingecko_id": "bitcoin",
                                              "mata_uang": "idr", "ambang_turun_persen": 0}]})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertIn("lebih besar dari 0", data["pesan"])

    def test_39_ambang_teks_persen_tidak_traceback_R2(self):
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "coingecko_id": "bitcoin",
                                              "mata_uang": "idr", "ambang_turun_persen": "5%"}]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1400000000, "perubahan_24jam_persen": -8,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        self.assertEqual(err, "")  # tidak ada traceback ke stderr

    def test_40_harga_acuan_format_id_dipakai_untuk_persen(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr",
             "harga_acuan": "1.450.000.000", "ambang_turun_persen": 10},
        ]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1200000000, "perubahan_24jam_persen": -1,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        data = json.loads(out)
        self.assertAlmostEqual(data["koin"][0]["persen_vs_acuan"], -17.24137931034483, places=4)

    def test_41_mode_keluaran_teks_singkat(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 50},
        ]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1500000000, "perubahan_24jam_persen": 0,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
            "--keluaran", "teks",
        ])
        self.assertEqual(kode, 0, err)
        self.assertNotEqual(out.strip()[:1], "{")
        self.assertIn("BTC", out)

    def test_42_data_hidup_tapi_basi_diberi_peringatan_R1(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_naik_persen": 50},
        ]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1500000000, "perubahan_24jam_persen": 0,
            "jam_data": "2026-09-20T07:00:00+07:00", "sumber": "coingecko"}})  # ~96 jam lalu
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        data = json.loads(out)
        self.assertEqual(data["koin"][0]["status"], "hidup")
        self.assertTrue(any("sudah berumur" in p for p in data["koin"][0]["peringatan"]))

    def test_43_gagal_total_dan_ambang_terlewati_bersamaan_dilaporkan_keduanya_S1(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 5},
            {"kode": "SOL", "coingecko_id": "solana", "mata_uang": "usd", "ambang_turun_persen": 5},
        ]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1400000000, "perubahan_24jam_persen": -8,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)  # perlu_lapor menang atas gagal_total di exit code
        data = json.loads(out)
        self.assertTrue(data["ambang_terlewati"])
        self.assertTrue(data["ada_koin_gagal_total"])
        self.assertIn("BTC", data["pesan_singkat"])
        self.assertIn("SOL", data["pesan_singkat"])
        self.assertIn("TIDAK BISA DICEK", data["pesan_singkat"])

    def test_44_anti_spam_diredam_lalu_lapor_ulang_setelah_jeda_S3(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 5},
        ]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1400000000, "perubahan_24jam_persen": -8,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        # Panggilan pertama: baru terpicu -> exit 2
        kode1, _, _ = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode1, 2)
        # Panggilan kedua, kondisi & waktu sama -> sudah dilaporkan, diredam -> exit 0
        kode2, out2, _ = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode2, 0)
        data2 = json.loads(out2)
        self.assertTrue(data2["koin"][0]["ambang_terlewati"])
        self.assertFalse(data2["koin"][0]["perlu_lapor"])

    def test_45_anti_spam_reset_setelah_pulih_S3(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 5},
        ]})
        harga_turun = os.path.join(self.tmp, "turun.json")
        harga_normal = os.path.join(self.tmp, "normal.json")
        tulis_json(harga_turun, {"bitcoin_idr_coingecko": {
            "harga": 1400000000, "perubahan_24jam_persen": -8,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        tulis_json(harga_normal, {"bitcoin_idr_coingecko": {
            "harga": 1500000000, "perubahan_24jam_persen": 0,
            "jam_data": "2026-09-24T08:00:00+07:00", "sumber": "coingecko"}})
        kode1, _, _ = jalankan_cek_ambang(["--konfigurasi", self.cfg_path, "--state", self.state_path,
                                            "--harga-file", harga_turun])
        self.assertEqual(kode1, 2)
        kode2, _, _ = jalankan_cek_ambang(["--konfigurasi", self.cfg_path, "--state", self.state_path,
                                            "--harga-file", harga_normal])
        self.assertEqual(kode2, 0)  # pulih
        kode3, _, _ = jalankan_cek_ambang(["--konfigurasi", self.cfg_path, "--state", self.state_path,
                                            "--harga-file", harga_turun])
        self.assertEqual(kode3, 2)  # terpicu lagi -> harus lapor lagi, bukan diredam

    def test_46_dua_entri_koin_sama_tidak_saling_meredam_R3(self):
        # Dua aturan berbeda untuk BTC/IDR/CoinGecko yang sama (berbagi cache harga, TAPI
        # status notifikasi terpisah per entri -- lihat kk_notif indeks di proses_koin).
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 5},
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_harga_di_bawah": 1450000000},
        ]})
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1400000000, "perubahan_24jam_persen": -8,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        data = json.loads(out)
        self.assertTrue(data["koin"][0]["perlu_lapor"])
        self.assertTrue(data["koin"][1]["perlu_lapor"])  # keduanya baru, bukan saling meredam


class UjiWrapperCekDanLapor(unittest.TestCase):
    """B-1: wrapper --command yang terbukti bekerja di Gateway uji."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji_wrapper_")
        self.cfg_path = os.path.join(self.tmp, "konfigurasi.json")
        self.state_path = os.path.join(self.tmp, "state.json")
        self.harga_path = os.path.join(self.tmp, "harga.json")
        tulis_json(self.state_path, {})
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 5},
        ]})

    def test_47_wrapper_no_reply_saat_tenang(self):
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1500000000, "perubahan_24jam_persen": 0,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_wrapper([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 0)  # SELALU exit 0
        self.assertEqual(out.strip(), "NO_REPLY")

    def test_48_wrapper_cetak_pesan_saat_ambang_terlewati(self):
        tulis_json(self.harga_path, {"bitcoin_idr_coingecko": {
            "harga": 1400000000, "perubahan_24jam_persen": -8,
            "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"}})
        kode, out, err = jalankan_wrapper([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 0)  # SELALU exit 0, walau cek_ambang.py exit 2
        self.assertIn("AMBANG TERLEWATI", out)
        self.assertNotEqual(out.strip(), "NO_REPLY")

    def test_49_wrapper_selalu_exit_0_walau_gagal_total(self):
        tulis_json(self.harga_path, {})  # BTC gagal -> cek_ambang.py exit 3
        kode, out, err = jalankan_wrapper([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 0)
        self.assertIn("TIDAK BISA DICEK", out)

    def test_50_wrapper_selalu_exit_0_walau_error_konfigurasi(self):
        tulis_json(self.cfg_path, {"koin": []})  # konfigurasi tidak valid -> exit 1
        kode, out, err = jalankan_wrapper([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 0)


# ---------------------------------------------------------------------------
# hitung_pl_jurnal.py
# ---------------------------------------------------------------------------

class UjiJurnalPL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji_jurnal_")
        self.csv_path = os.path.join(self.tmp, "JURNAL.csv")

    def _tulis_csv(self, isi, encoding="utf-8"):
        tulis_teks(self.csv_path, isi, encoding=encoding)

    def test_51_parse_angka_id_format_indonesia(self):
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("Rp 1.500.000"), 1500000.0)
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("1.500.000,50"), 1500000.50)
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("1500000"), 1500000.0)
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("15000,5"), 15000.5)

    def test_52_parse_angka_id_kosong_pesan_indonesia(self):
        with self.assertRaises(ValueError) as cm:
            hitung_pl_jurnal.parse_angka_id("")
        self.assertIn("kosong", str(cm.exception))

    def test_53_parse_jumlah_koin_titik_S6(self):
        self.assertAlmostEqual(hitung_pl_jurnal.parse_jumlah_koin("0.005"), 0.005)

    def test_54_parse_jumlah_koin_koma_S6(self):
        self.assertAlmostEqual(hitung_pl_jurnal.parse_jumlah_koin("0,005"), 0.005)

    def test_55_parse_jumlah_koin_titik_dan_koma_ditolak_jelas(self):
        with self.assertRaises(ValueError) as cm:
            hitung_pl_jurnal.parse_jumlah_koin("1.234,5")
        self.assertIn("koma dan titik sekaligus", str(cm.exception))

    def test_56_fifo_untung_termasuk_biaya(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,10000,,,\n"
            "2026-02-01,BTC,jual,1,1200000,12000,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        r = data["realized_per_koin"]["BTC"][0]
        self.assertEqual(r["cost_basis"], 1010000)
        self.assertEqual(r["proceeds"], 1188000)
        self.assertEqual(r["pl"], 178000)
        self.assertEqual(data["total_realized_pl"], 178000)

    def test_57_fifo_dua_lot_beli_beda_harga(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,0,,,\n"
            "2026-02-01,BTC,beli,1,2000000,0,,,\n"
            "2026-03-01,BTC,jual,1.5,3000000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        r = data["realized_per_koin"]["BTC"][0]
        self.assertEqual(r["cost_basis"], 2000000)
        self.assertEqual(data["posisi_tersisa"]["BTC"]["jumlah_tersisa"], 0.5)

    def test_58_jual_melebihi_stok_dicatat_bermasalah_partial(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,0.5,1000000,0,,,\n"
            "2026-02-01,BTC,jual,1,1200000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)
        self.assertIn("melebihi stok", data["baris_bermasalah"][0]["alasan"])
        self.assertEqual(len(data["realized_per_koin"]["BTC"]), 1)  # tetap ada utk bagian yg terpenuhi

    def test_59_jual_tanpa_lot_sama_sekali_tidak_bikin_realized_nol_R5(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,jual,1,1000000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)
        self.assertEqual(data["realized_per_koin"], {})  # bukan {"BTC": [{"pl": 0, ...}]}

    def test_60_baris_rusak_aksi_tidak_valid_tetap_lanjut(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,0,,,\n"
            "2026-02-01,BTC,tukar,1,1000000,0,,,\n"
            "2026-03-01,BTC,jual,1,1200000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)
        self.assertIn("aksi", data["baris_bermasalah"][0]["alasan"])
        self.assertEqual(data["total_realized_pl"], 200000)

    def test_61_angka_rusak_pesan_indonesia_tidak_menghentikan_baris_lain(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,satu,1000000,0,,,\n"
            "2026-02-01,ETH,beli,1,2000000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)
        self.assertIn("bukan angka", data["baris_bermasalah"][0]["alasan"])
        self.assertIn("ETH", data["posisi_tersisa"])

    def test_62_kolom_wajib_hilang_exit_1(self):
        self._tulis_csv("tanggal,koin,aksi,jumlah_koin\n2026-01-01,BTC,beli,1\n")
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertEqual(data["status"], "error")

    def test_63_file_tidak_ada_exit_1(self):
        kode, out, err = jalankan_jurnal(["--jurnal", os.path.join(self.tmp, "hilang.csv"),
                                           "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertIn("tidak ditemukan", data["pesan"])

    def test_64_file_0_byte_pesan_jelas_bukan_tidak_ditemukan_R5(self):
        self._tulis_csv("")
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertIn("kosong", data["pesan"])
        self.assertNotIn("tidak ditemukan", data["pesan"])  # file ADA, cuma isinya kosong

    def test_65_header_saja_tanpa_transaksi_bukan_error_R5(self):
        self._tulis_csv("tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya\n")
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["jumlah_baris_dihitung"], 0)

    def test_66_csv_pemisah_titik_koma_S6(self):
        self._tulis_csv(
            "tanggal;koin;aksi;jumlah_koin;harga_satuan;biaya\n"
            "2026-01-10;BTC;beli;0,005;1.380.000.000;20.700\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["jumlah_baris_dihitung"], 1)
        self.assertAlmostEqual(data["posisi_tersisa"]["BTC"]["jumlah_tersisa"], 0.005)

    def test_67_csv_dengan_bom_utf8(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya\n"
            "2026-01-10,BTC,beli,0.01,1000000,0\n",
            encoding="utf-8-sig",
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["jumlah_baris_dihitung"], 1)

    def test_68_encoding_bukan_utf8_tidak_menggagalkan_file(self):
        with open(self.csv_path, "wb") as f:
            f.write(
                b"tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana\n"
                b"2026-01-10,BTC,beli,0.005,1380000000,0,caf\xe9 rencana\n"
            )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["jumlah_baris_dihitung"], 1)
        self.assertTrue(any("UTF-8" in p for p in data["peringatan_global"]))

    def test_69_hari_ini_rusak_tidak_traceback(self):
        self._tulis_csv("tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya\n2026-01-01,BTC,beli,1,1000000,0\n")
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "bukan-tanggal"])
        self.assertEqual(kode, 1)
        self.assertEqual(err, "")
        data = json.loads(out)
        self.assertIn("--hari-ini", data["pesan"])

    def test_70_tinjau_ulang_belum_jatuh_tempo_tidak_muncul(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,0,rencana,2099-01-01,masih jauh\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["tinjau_ulang_jatuh_tempo"], [])

    def test_71_tinjau_ulang_jatuh_tempo_hari_ini_muncul(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,0,rencana awal,2026-09-24,cek harga sekarang\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["tinjau_ulang_jatuh_tempo"]), 1)
        self.assertEqual(data["tinjau_ulang_jatuh_tempo"][0]["syarat"], "cek harga sekarang")

    def test_72_biaya_negatif_dicatat_bermasalah(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,-500,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)

    def test_73_filter_periode_bulan_ini(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya\n"
            "2026-01-01,BTC,beli,1,1000000,0\n"
            "2026-01-15,BTC,jual,0.5,1200000,0\n"
            "2026-09-10,BTC,jual,0.5,1500000,0\n"
        )
        kode, out, err = jalankan_jurnal([
            "--jurnal", self.csv_path, "--hari-ini", "2026-09-24", "--periode", "bulan-ini",
        ])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["realized_per_koin"]["BTC"]), 1)
        self.assertEqual(data["realized_per_koin"]["BTC"][0]["tanggal"], "2026-09-10")
        self.assertEqual(data["total_realized_pl"], 250000)
        # FIFO/posisi tetap utuh, tidak terpengaruh filter
        self.assertNotIn("BTC", data["posisi_tersisa"])  # habis terjual semua (0.5+0.5=1)

    def test_74_filter_dari_sampai_eksplisit(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya\n"
            "2026-01-01,BTC,beli,2,1000000,0\n"
            "2026-03-01,BTC,jual,1,1100000,0\n"
            "2026-08-01,BTC,jual,1,1300000,0\n"
        )
        kode, out, err = jalankan_jurnal([
            "--jurnal", self.csv_path, "--hari-ini", "2026-09-24",
            "--dari", "2026-07-01", "--sampai", "2026-08-31",
        ])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["realized_per_koin"]["BTC"]), 1)
        self.assertEqual(data["realized_per_koin"]["BTC"][0]["tanggal"], "2026-08-01")

    def test_75_dari_setelah_sampai_ditolak(self):
        self._tulis_csv("tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya\n2026-01-01,BTC,beli,1,1000000,0\n")
        kode, out, err = jalankan_jurnal([
            "--jurnal", self.csv_path, "--dari", "2026-09-01", "--sampai", "2026-01-01",
        ])
        self.assertEqual(kode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
