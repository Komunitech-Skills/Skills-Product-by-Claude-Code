#!/usr/bin/env python3
"""Uji regresi pantau-pasar-kripto -- SEPENUHNYA OFFLINE (tanpa jaringan).

Jalankan: python3 tests/uji_regresi.py
(atau: python3 -m unittest tests/uji_regresi.py -v)

cek_ambang.py hanya diuji lewat mode --harga-file (tidak pernah memanggil ambil_harga_online).
hitung_pl_jurnal.py diuji lewat file CSV sementara.
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


def jalankan_jurnal(args):
    cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "hitung_pl_jurnal.py")] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def tulis_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


class UjiFungsiMurniCekAmbang(unittest.TestCase):
    """Uji fungsi kalkulasi murni (tanpa file/proses) -- cepat, tanpa I/O."""

    def test_01_bulat_setengah_ke_atas_rupiah(self):
        self.assertEqual(cek_ambang.bulat_setengah_ke_atas(1500000.5), 1500001)
        self.assertEqual(cek_ambang.bulat_setengah_ke_atas(1500000.4), 1500000)

    def test_02_bulat_setengah_ke_atas_negatif(self):
        # nilai negatif tetap konsisten (menjauhi nol pada .5)
        self.assertEqual(cek_ambang.bulat_setengah_ke_atas(-2.5, 0), -3)

    def test_03_format_rupiah_pemisah_ribuan(self):
        self.assertEqual(cek_ambang.format_rupiah(1500000000), "Rp 1.500.000.000")

    def test_04_format_rupiah_negatif(self):
        self.assertEqual(cek_ambang.format_rupiah(-50000), "-Rp 50.000")

    def test_05_format_persen_naik(self):
        self.assertEqual(cek_ambang.format_persen(5.256), "+5.26%")

    def test_06_format_persen_turun(self):
        self.assertEqual(cek_ambang.format_persen(-5.2), "-5.20%")

    def test_07_hitung_persen_perubahan_naik(self):
        persen = cek_ambang.hitung_persen_perubahan(1100, 1000)
        self.assertAlmostEqual(persen, 10.0)

    def test_08_hitung_persen_perubahan_turun(self):
        persen = cek_ambang.hitung_persen_perubahan(800, 1000)
        self.assertAlmostEqual(persen, -20.0)

    def test_09_hitung_persen_perubahan_tanpa_acuan(self):
        self.assertIsNone(cek_ambang.hitung_persen_perubahan(1000, None))
        self.assertIsNone(cek_ambang.hitung_persen_perubahan(1000, 0))

    def test_10_evaluasi_ambang_turun_terlewati(self):
        cfg = {"ambang_turun_persen": 5}
        terlewati, detail = cek_ambang.evaluasi_ambang(cfg, 950, -6.0)
        self.assertTrue(terlewati)
        self.assertIn("Turun", detail[0])

    def test_11_evaluasi_ambang_naik_terlewati(self):
        cfg = {"ambang_naik_persen": 5}
        terlewati, detail = cek_ambang.evaluasi_ambang(cfg, 1100, 7.5)
        self.assertTrue(terlewati)

    def test_12_evaluasi_ambang_tidak_terlewati(self):
        cfg = {"ambang_naik_persen": 5, "ambang_turun_persen": 5}
        terlewati, detail = cek_ambang.evaluasi_ambang(cfg, 1020, 2.0)
        self.assertFalse(terlewati)
        self.assertEqual(detail, [])

    def test_13_evaluasi_ambang_harga_absolut_atas(self):
        cfg = {"ambang_harga_di_atas": 1000}
        terlewati, detail = cek_ambang.evaluasi_ambang(cfg, 1000, None)
        self.assertTrue(terlewati)

    def test_14_evaluasi_ambang_harga_absolut_bawah(self):
        cfg = {"ambang_harga_di_bawah": 500}
        terlewati, detail = cek_ambang.evaluasi_ambang(cfg, 400, None)
        self.assertTrue(terlewati)

    def test_15_evaluasi_ambang_persen_tanpa_dasar_pembanding(self):
        cfg = {"ambang_turun_persen": 5}
        terlewati, detail = cek_ambang.evaluasi_ambang(cfg, 900, None)
        self.assertFalse(terlewati)
        self.assertTrue(any("tidak ada dasar pembanding" in d.lower() for d in detail))


class UjiProsesCekAmbangViaCLI(unittest.TestCase):
    """Uji end-to-end lewat CLI, --harga-file (tanpa jaringan), skenario Rp & USD."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji_kripto_")
        self.cfg_path = os.path.join(self.tmp, "konfigurasi.json")
        self.state_path = os.path.join(self.tmp, "state.json")
        self.harga_path = os.path.join(self.tmp, "harga.json")
        tulis_json(self.state_path, {})

    def test_16_ambang_turun_idr_terpicu_exit_2(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 5},
        ]})
        tulis_json(self.harga_path, {
            "bitcoin_idr": {"harga": 1400000000, "perubahan_24jam_persen": -7.0,
                             "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        data = json.loads(out)
        self.assertTrue(data["ambang_terlewati"])
        self.assertIn("Rp 1.400.000.000", data["koin"][0]["harga_format"])

    def test_17_ambang_naik_usd_terpicu(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "ETH", "coingecko_id": "ethereum", "mata_uang": "usd", "ambang_naik_persen": 5},
        ]})
        tulis_json(self.harga_path, {
            "ethereum_usd": {"harga": 2700.0, "perubahan_24jam_persen": 8.1,
                              "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        data = json.loads(out)
        self.assertIn("US$", data["koin"][0]["harga_format"])

    def test_18_tidak_ada_ambang_terlewati_exit_0(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr",
             "ambang_naik_persen": 10, "ambang_turun_persen": 10},
        ]})
        tulis_json(self.harga_path, {
            "bitcoin_idr": {"harga": 1500000000, "perubahan_24jam_persen": 1.0,
                             "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 0, err)

    def test_19_sumber_gagal_tanpa_cache_exit_3_tanpa_mengarang_harga(self):
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
        self.assertIsNone(data["koin"][0]["harga"])  # tidak boleh mengarang angka

    def test_20_sumber_gagal_dengan_cache_pakai_data_basi(self):
        tulis_json(self.state_path, {
            "solana_usd": {"harga_terakhir": 150.0, "jam_data_terakhir": "2026-09-20T07:00:00+07:00",
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
        self.assertEqual(kode, 0, err)  # ambang tidak terpicu, tapi tetap sukses (bukan gagal_total)
        data = json.loads(out)
        self.assertEqual(data["koin"][0]["status"], "cache")
        self.assertTrue(any("DATA BASI" in p for p in data["koin"][0]["peringatan"]))
        self.assertTrue(any("lebih tua dari batas" in p for p in data["koin"][0]["peringatan"]))

    def test_21_state_json_rusak_exit_1(self):
        with open(self.state_path, "w", encoding="utf-8") as f:
            f.write("{ini bukan json valid")
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "mata_uang": "idr", "ambang_turun_persen": 5}]})
        tulis_json(self.harga_path, {"btc_idr": {"harga": 1, "perubahan_24jam_persen": 0,
                                                   "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "x"}})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertEqual(data["status"], "error")

    def test_22_konfigurasi_json_rusak_exit_1(self):
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            f.write("{bukan json")
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path if False else self.harga_path,
        ])
        self.assertEqual(kode, 1)

    def test_23_konfigurasi_tanpa_ambang_sama_sekali_exit_1(self):
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "mata_uang": "idr"}]})
        tulis_json(self.harga_path, {})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertIn("ambang", data["pesan"].lower())

    def test_24_konfigurasi_mata_uang_tidak_valid_exit_1(self):
        tulis_json(self.cfg_path, {"koin": [{"kode": "BTC", "mata_uang": "eur", "ambang_turun_persen": 5}]})
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)

    def test_25_file_konfigurasi_tidak_ada_exit_1(self):
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", os.path.join(self.tmp, "tidak-ada.json"),
            "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 1)

    def test_26_harga_acuan_member_dipakai_untuk_persen(self):
        # Sumber tanpa 24h change (indodax) TAPI harga_acuan diisi member -> persen tetap bisa dihitung
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "mata_uang": "idr", "sumber": "indodax", "indodax_pair": "btcidr",
             "harga_acuan": 2000000000, "ambang_turun_persen": 15},
        ]})
        tulis_json(self.harga_path, {
            "btc_idr": {"harga": 1600000000, "perubahan_24jam_persen": None,
                        "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "indodax"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
        ])
        self.assertEqual(kode, 2, err)
        data = json.loads(out)
        self.assertAlmostEqual(data["koin"][0]["persen_vs_acuan"], -20.0)

    def test_27_mode_keluaran_teks_singkat(self):
        tulis_json(self.cfg_path, {"koin": [
            {"kode": "BTC", "coingecko_id": "bitcoin", "mata_uang": "idr", "ambang_turun_persen": 50},
        ]})
        tulis_json(self.harga_path, {
            "bitcoin_idr": {"harga": 1500000000, "perubahan_24jam_persen": 0,
                             "jam_data": "2026-09-24T07:00:00+07:00", "sumber": "coingecko"},
        })
        kode, out, err = jalankan_cek_ambang([
            "--konfigurasi", self.cfg_path, "--state", self.state_path, "--harga-file", self.harga_path,
            "--keluaran", "teks",
        ])
        self.assertEqual(kode, 0, err)
        self.assertNotIn("{", out.strip()[:1])
        self.assertIn("BTC", out)


class UjiJurnalPL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji_jurnal_")
        self.csv_path = os.path.join(self.tmp, "JURNAL.csv")

    def _tulis_csv(self, isi):
        with open(self.csv_path, "w", encoding="utf-8", newline="") as f:
            f.write(isi)

    def test_28_parse_angka_id_format_indonesia(self):
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("Rp 1.500.000"), 1500000.0)
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("1.500.000,50"), 1500000.50)
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("1500000"), 1500000.0)
        self.assertAlmostEqual(hitung_pl_jurnal.parse_angka_id("15000,5"), 15000.5)

    def test_29_parse_angka_id_kosong_error(self):
        with self.assertRaises(ValueError):
            hitung_pl_jurnal.parse_angka_id("")
        with self.assertRaises(ValueError):
            hitung_pl_jurnal.parse_angka_id(None)

    def test_30_fifo_untung_termasuk_biaya(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,10000,,,\n"
            "2026-02-01,BTC,jual,1,1200000,12000,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        r = data["realized_per_koin"]["BTC"][0]
        # cost basis = 1*(1.000.000+10.000) = 1.010.000 ; proceeds = 1*1.200.000 - 12.000 = 1.188.000
        self.assertEqual(r["cost_basis"], 1010000)
        self.assertEqual(r["proceeds"], 1188000)
        self.assertEqual(r["pl"], 178000)
        self.assertEqual(data["total_realized_pl"], 178000)

    def test_31_fifo_dua_lot_beli_beda_harga(self):
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
        # ambil 1 dari lot pertama (1.000.000) + 0.5 dari lot kedua (2.000.000) = 1.000.000 + 1.000.000 = 2.000.000
        self.assertEqual(r["cost_basis"], 2000000)
        self.assertEqual(data["posisi_tersisa"]["BTC"]["jumlah_tersisa"], 0.5)

    def test_32_jual_melebihi_stok_dicatat_bermasalah(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,jual,1,1000000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)
        self.assertIn("melebihi stok", data["baris_bermasalah"][0]["alasan"])

    def test_33_baris_rusak_aksi_tidak_valid_tetap_lanjut(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,0,,,\n"
            "2026-02-01,BTC,tukar,1,1000000,0,,,\n"  # aksi rusak
            "2026-03-01,BTC,jual,1,1200000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)
        self.assertIn("aksi", data["baris_bermasalah"][0]["alasan"])
        # baris beli & jual yang valid tetap dihitung
        self.assertEqual(data["total_realized_pl"], 200000)

    def test_34_angka_rusak_tidak_menghentikan_baris_lain(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,satu,1000000,0,,,\n"  # jumlah_koin rusak
            "2026-02-01,ETH,beli,1,2000000,0,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)
        self.assertIn("ETH", data["posisi_tersisa"])

    def test_35_kolom_wajib_hilang_exit_1(self):
        self._tulis_csv("tanggal,koin,aksi,jumlah_koin\n2026-01-01,BTC,beli,1\n")
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 1)
        data = json.loads(out)
        self.assertEqual(data["status"], "error")

    def test_36_file_tidak_ada_exit_1(self):
        kode, out, err = jalankan_jurnal(["--jurnal", os.path.join(self.tmp, "hilang.csv"),
                                           "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 1)

    def test_37_file_kosong_exit_1(self):
        self._tulis_csv("")
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 1)

    def test_38_tinjau_ulang_belum_jatuh_tempo_tidak_muncul(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,0,rencana,2099-01-01,masih jauh\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(data["tinjau_ulang_jatuh_tempo"], [])

    def test_39_tinjau_ulang_jatuh_tempo_hari_ini_muncul(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,0,rencana awal,2026-09-24,cek harga sekarang\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["tinjau_ulang_jatuh_tempo"]), 1)
        self.assertEqual(data["tinjau_ulang_jatuh_tempo"][0]["syarat"], "cek harga sekarang")

    def test_40_biaya_negatif_dicatat_bermasalah(self):
        self._tulis_csv(
            "tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat\n"
            "2026-01-01,BTC,beli,1,1000000,-500,,,\n"
        )
        kode, out, err = jalankan_jurnal(["--jurnal", self.csv_path, "--hari-ini", "2026-09-24"])
        self.assertEqual(kode, 0, err)
        data = json.loads(out)
        self.assertEqual(len(data["baris_bermasalah"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
