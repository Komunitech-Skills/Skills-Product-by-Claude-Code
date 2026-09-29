#!/usr/bin/env python3
"""Uji regresi actual-budget-usaha. Jalankan: python3 tests/uji_regresi.py

Fixture:
- fixtures/actual-26.9.0-studio-rina/     budget Actual ASLI (dibuat @actual-app/api 26.9.0, data fiktif),
  mode amplop. acuan-getBudgetMonth.json = angka yang dihitung Actual sendiri (getBudgetMonth).
- fixtures/actual-26.9.0-toko-kue-tracking/ budget Actual ASLI mode pelacakan (tracking).
- fixtures/mutasi/*.csv                    mutasi bank FIKTIF berpola BCA/BRI/Mandiri/BNI.
Script pembuat fixture Actual ada di tests/verifikasi_node/ (butuh Node.js; hanya untuk pengembang).
"""
import contextlib
import csv
import hashlib
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

DIR = Path(__file__).resolve().parent
SKILL = DIR.parent
sys.path.insert(0, str(SKILL / "scripts"))
import actual_budget as ab  # noqa: E402

FX = DIR / "fixtures"
RINA = FX / "actual-26.9.0-studio-rina"
KUE = FX / "actual-26.9.0-toko-kue-tracking"
MUT = FX / "mutasi"


def jalan(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        kode = ab.main([str(x) for x in argv])
    return kode, out.getvalue(), err.getvalue()


def loosely_parse_amount(s):
    """Port uji dari looselyParseAmount Actual 26.9.0 (packages/loot-core/src/shared/util.ts, MIT,
    Copyright James Long). Dipakai hanya untuk memastikan kolom Amount hasil skill dibaca benar."""
    s = s.strip()
    if s.startswith("(") and s.endswith(")"):
        s = s.replace("(", "-", 1).replace(")", "", 1)
    m = re.search(r"[.,]([^.,]{4,9}|[^.,]{1,2})$", s)
    ex = lambda v: re.sub(r"[^0-9-]", "", v)
    if not m:
        return Decimal(ex(s))
    return Decimal(ex(s[:m.start()]) + "." + ex(s[m.start() + 1:]))


def baca_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def baca_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class TmpMixin:
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="uji-actual-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class UjiAngka(unittest.TestCase):
    def test_01_format_rupiah(self):
        self.assertEqual(ab.rp(Decimal("1500000")), "Rp 1.500.000")
        self.assertEqual(ab.rp(Decimal("149999.5")), "Rp 149.999,50")
        self.assertEqual(ab.rp(Decimal("-200000")), "-Rp 200.000")
        self.assertEqual(ab.rp(Decimal("0")), "Rp 0")

    def test_02_angka_gaya_indonesia(self):
        self.assertEqual(ab.parse_nominal("1.500.000,00", "koma")[0], Decimal("1500000"))
        self.assertEqual(ab.parse_nominal("Rp 1.250.000,-", "koma")[0], Decimal("1250000"))
        self.assertEqual(ab.parse_nominal("12.345,67", "koma")[0], Decimal("12345.67"))

    def test_03_angka_gaya_inggris_dan_penanda(self):
        self.assertEqual(ab.parse_nominal("1,500,000.00", "titik"), (Decimal("1500000.00"), None))
        self.assertEqual(ab.parse_nominal("1,500,000.00 CR", "titik"), (Decimal("1500000.00"), "CR"))
        self.assertEqual(ab.parse_nominal("(25,000)", "titik")[0], Decimal("-25000"))
        self.assertEqual(ab.parse_nominal("150000-", None)[0], Decimal("-150000"))

    def test_04_angka_ambigu_ditolak(self):
        self.assertEqual(ab.parse_nominal("1.500", None)[0], Decimal("1500"))  # ribuan, Rupiah tanpa sen
        with self.assertRaises(ValueError):
            ab.parse_nominal("12,5", None)
        with self.assertRaises(ValueError):
            ab.parse_nominal("1.50.000", "koma")
        with self.assertRaises(ValueError):
            ab.parse_nominal("10,123", "koma")  # 3 angka di belakang koma desimal

    def test_05_tanggal(self):
        f = lambda t, tahun=None: ab.rakit_tanggal(ab.pecah_tanggal(t), "dm", tahun).isoformat()
        self.assertEqual(f("01/09/2026"), "2026-09-01")
        self.assertEqual(f("2026-09-02 10:21:33"), "2026-09-02")
        self.assertEqual(f("01 Sep 2026"), "2026-09-01")
        self.assertEqual(f("17 Agustus 2026"), "2026-08-17")
        self.assertEqual(f("5-Okt-26"), "2026-10-05")
        self.assertEqual(f("'01/09", 2026), "2026-09-01")
        with self.assertRaises(ab.Gagal):
            f("01/09")

    def test_06_parse_bulan(self):
        import datetime as dt
        h = dt.date(2026, 9, 26)
        self.assertEqual(ab.parse_bulan("2026-09", h), 202609)
        self.assertEqual(ab.parse_bulan("09/2026", h), 202609)
        self.assertEqual(ab.parse_bulan("September 2026", h), 202609)
        self.assertEqual(ab.parse_bulan("lalu", dt.date(2026, 1, 5)), 202512)
        with self.assertRaises(ab.Gagal):
            ab.parse_bulan("bulan depan kayaknya", h)


class UjiKonversi(TmpMixin, unittest.TestCase):
    def konversi(self, nama, *opsi):
        out = self.tmp / (nama + "-actual.csv")
        kode, teks, err = jalan("konversi", MUT / (nama + "-sep-2026.csv"), "--keluaran", out, "--json", *opsi)
        data = json.loads(teks) if kode == 0 else None
        rows = baca_csv(out) if kode == 0 else None
        return kode, data, rows, err

    def test_07_bca_tanpa_tahun_minta_tahun(self):
        kode, _, _, err = self.konversi("bca")
        self.assertEqual(kode, 2)
        self.assertIn("--tahun", err)

    def test_08_bca_lengkap(self):
        kode, d, rows, _ = self.konversi("bca", "--tahun", "2026")
        self.assertEqual(kode, 0)
        self.assertEqual(d["baris_terbaca"], 13)
        self.assertEqual(Decimal(d["total_masuk"]), Decimal("10262345.67"))
        self.assertEqual(Decimal(d["total_keluar"]), Decimal("8019969.13"))
        self.assertTrue(d["cek_saldo"]["cocok"])
        self.assertEqual(Decimal(d["cek_saldo"]["saldo_akhir"]), Decimal("7242376.54"))
        alasan = " ".join(x["alasan"] for x in d["dilewati"])
        self.assertIn("PENDING", alasan)
        self.assertIn("ringkasan", alasan)
        self.assertEqual(d["deteksi"]["desimal"], "titik")
        self.assertTrue(all(not r["Notes"].startswith("'") for r in rows))

    def test_09_bri_kolom_debet_kredit(self):
        kode, d, rows, _ = self.konversi("bri")
        self.assertEqual(kode, 0)
        self.assertEqual(d["baris_terbaca"], 6)
        self.assertEqual(Decimal(d["total_masuk"]), Decimal("4500000"))
        self.assertEqual(Decimal(d["total_keluar"]), Decimal("832500"))
        self.assertTrue(d["cek_saldo"]["cocok"])
        self.assertEqual(rows[0]["Date"], "2026-09-02")

    def test_10_mandiri_titik_koma_format_indonesia(self):
        kode, d, rows, _ = self.konversi("mandiri")
        self.assertEqual(kode, 0)
        self.assertEqual(d["deteksi"]["pemisah"], "titik koma")
        self.assertEqual(d["deteksi"]["desimal"], "koma")
        self.assertEqual(Decimal(d["total_masuk"]), Decimal("12000000"))
        self.assertEqual(Decimal(d["total_keluar"]), Decimal("2779000"))
        self.assertTrue(d["cek_saldo"]["cocok"])

    def test_11_bni_kolom_tipe_db_cr(self):
        kode, d, rows, _ = self.konversi("bni")
        self.assertEqual(kode, 0)
        self.assertEqual([r["Amount"] for r in rows], ["3000000", "-2500000", "-25000", "-1000000"])
        self.assertTrue(d["cek_saldo"]["cocok"])

    def test_12_kategori_usulan_dan_pindah_dana(self):
        kode, d, rows, _ = self.konversi("bca", "--tahun", "2026")
        per = {r["Notes"]: r["Category"] for r in rows}
        self.assertEqual(per["TRSF E-BANKING DB 0309/FTFVA/WS95051 70001/PLN PRABAYAR"], "Listrik & Air")
        self.assertEqual(per["KARTU DEBIT TELKOMSEL 8801"], "Internet & Pulsa")
        self.assertEqual(per["TARIKAN ATM 10/09 ATM BCA"], "")          # pindah dana: tanpa kategori
        self.assertEqual(per["TRSF E-BANKING CR 2009/FTSCY/WS95031 2000000.00 BUDI SANTOSO"], "Pendapatan Usaha")
        ragu = {x["keterangan"]: x["alasan"] for x in d["ragu"]}
        self.assertIn("TRANSFER", ragu["TARIKAN ATM 10/09 ATM BCA"])
        self.assertIn("marketplace", ragu["KARTU DEBIT TOKOPEDIA"])

    def test_13_peta_pengguna_menang(self):
        peta = self.tmp / "peta.csv"
        peta.write_text("kata_kunci,kategori,arah\nTOKOPEDIA,Bahan Baku,keluar\n", encoding="utf-8")
        kode, d, rows, _ = self.konversi("bca", "--tahun", "2026", "--peta", peta)
        self.assertEqual({r["Notes"]: r["Category"] for r in rows}["KARTU DEBIT TOKOPEDIA"], "Bahan Baku")

    def test_14_nama_kategori_dicocokkan_ke_budget(self):
        peta = self.tmp / "peta.csv"
        peta.write_text("FACEBK,iklan,keluar\n", encoding="utf-8")  # huruf kecil -> dibetulkan jadi 'Iklan'
        kode, d, rows, _ = self.konversi("bca", "--tahun", "2026", "--peta", peta, "--db", RINA)
        per = {r["Notes"]: r["Category"] for r in rows}
        self.assertEqual(per["TRSF E-BANKING DB 1309/FTSCY/WS95031 3200000.00 FACEBK ADS META"], "Iklan")
        # 'Listrik & Air' tidak ada di budget fixture -> dikosongkan + masuk daftar ragu
        self.assertEqual(per["TRSF E-BANKING DB 0309/FTFVA/WS95051 70001/PLN PRABAYAR"], "")
        self.assertTrue(any("belum ada di budget" in x["alasan"] for x in d["ragu"]))
        self.assertTrue(d["kategori_dicek_ke_budget"])

    def test_15_kolom_amount_dibaca_benar_oleh_actual(self):
        kode, d, rows, _ = self.konversi("bca", "--tahun", "2026")
        self.assertEqual(list(rows[0].keys()), ["Date", "Payee", "Notes", "Category", "Amount"])
        total = sum(loosely_parse_amount(r["Amount"]) for r in rows)
        self.assertEqual(total, Decimal("10262345.67") - Decimal("8019969.13"))
        for r in rows:
            self.assertRegex(r["Date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_16_tidak_menimpa_tanpa_izin(self):
        out = self.tmp / "hasil.csv"
        out.write_text("isi lama", encoding="utf-8")
        kode, _, err = jalan("konversi", MUT / "bri-sep-2026.csv", "--keluaran", out)
        self.assertEqual(kode, 2)
        self.assertIn("sudah ada", err)
        self.assertEqual(out.read_text(encoding="utf-8"), "isi lama")
        kode, _, _ = jalan("konversi", MUT / "bri-sep-2026.csv", "--keluaran", out, "--timpa")
        self.assertEqual(kode, 0)

    def test_17_excel_pdf_dan_file_hilang(self):
        x = self.tmp / "mutasi.xlsx"
        x.write_bytes(b"PK\x03\x04isi-zip")
        kode, _, err = jalan("konversi", x)
        self.assertEqual(kode, 2)
        self.assertIn("Excel", err)
        p = self.tmp / "mutasi.csv"
        p.write_bytes(b"%PDF-1.7 isi")
        kode, _, err = jalan("konversi", p)
        self.assertIn("PDF", err)
        kode, _, err = jalan("konversi", self.tmp / "tidak-ada.csv")
        self.assertEqual(kode, 3)

    def test_18_format_angka_campur_ditolak(self):
        p = self.tmp / "campur.csv"
        p.write_text("Tanggal,Keterangan,Debet,Kredit,Saldo\n01/09/2026,A,\"1.500.000,00\",,\"1.000,00\"\n"
                     "02/09/2026,B,\"1,500,000.00\",,\"2,000.00\"\n", encoding="utf-8")
        kode, _, err = jalan("konversi", p, "--keluaran", self.tmp / "o.csv")
        self.assertEqual(kode, 2)
        self.assertIn("--desimal", err)

    def test_19_baris_kembar_ditandai(self):
        kode, d, rows, _ = self.konversi("mandiri")
        grab = [x for x in d["ragu"] if "GRAB" in x["keterangan"]]
        self.assertEqual(len(grab), 2)
        self.assertIn("dobel", grab[0]["alasan"])
        self.assertEqual(len(rows), 7)  # tetap ditulis; pengguna yang memutuskan

    def test_20_lintas_tahun_desember_januari(self):
        p = self.tmp / "bca-des.csv"
        p.write_text("Tanggal Transaksi,Keterangan,Cabang,Jumlah,,Saldo\n"
                     "'30/12,'BIAYA ADM,'0000,\"10,000.00\",DB,\"990,000.00\"\n"
                     "'02/01,'SETORAN TUNAI,'0000,\"500,000.00\",CR,\"1,490,000.00\"\n", encoding="utf-8")
        out = self.tmp / "o.csv"
        kode, teks, _ = jalan("konversi", p, "--tahun", "2027", "--keluaran", out, "--json")
        self.assertEqual(kode, 0)
        rows = baca_csv(out)
        self.assertEqual([r["Date"] for r in rows], ["2026-12-30", "2027-01-02"])

    def test_21_teks_mutasi_hanya_data(self):
        kode, d, rows, _ = self.konversi("bni")
        r = [x for x in rows if "IGNORE" in x["Notes"]][0]
        self.assertEqual(r["Category"], "")
        self.assertEqual(r["Amount"], "-25000")

    def test_22_tanpa_penanda_masuk_keluar(self):
        p = self.tmp / "polos.csv"
        p.write_text("Tanggal,Keterangan,Jumlah\n01/09/2026,Transfer X,150000\n", encoding="utf-8")
        kode, _, err = jalan("konversi", p, "--keluaran", self.tmp / "o.csv")
        self.assertEqual(kode, 2)
        self.assertIn("penanda", err)


class UjiRingkasan(TmpMixin, unittest.TestCase):
    def test_23_cocok_dengan_hitungan_actual_amplop(self):
        acuan = baca_json(RINA / "acuan-getBudgetMonth.json")["bulan"]
        con, _ = ab.buka_db(RINA)
        for bulan, a in acuan.items():
            if bulan == "2026-10":
                continue
            h = ab.hitung_bulan(con, int(bulan.replace("-", "")))
            per = {x["kategori"]: x for x in h["kategori"]}
            for nama, v in a["kategori"].items():
                self.assertEqual(per[nama]["sisa"], v["balance"], (bulan, nama, "sisa"))
                self.assertEqual(per[nama]["anggaran"], v["budgeted"], (bulan, nama, "anggaran"))
                self.assertEqual(-per[nama]["terpakai"], v["spent"], (bulan, nama, "terpakai"))
            self.assertEqual(h["siap_dianggarkan"], a["toBudget"], bulan)
            self.assertEqual(h["total_anggaran"], -a["totalBudgeted"], bulan)
            self.assertEqual(h["total_pemasukan"], a["totalIncome"], bulan)
            self.assertEqual(h["overspent_lalu"], a["lastMonthOverspent"], bulan)
        con.close()

    def test_24_bulan_tanpa_transaksi_membawa_minus(self):
        acuan = baca_json(RINA / "acuan-getBudgetMonth.json")["bulan"]
        con, _ = ab.buka_db(RINA)
        h = ab.hitung_bulan(con, 202610)
        con.close()
        self.assertEqual(h["siap_dianggarkan"], acuan["2026-10"]["toBudget"])
        self.assertFalse(h["ada_transaksi"])

    def test_25_cocok_dengan_hitungan_actual_tracking(self):
        acuan = baca_json(KUE / "acuan-getBudgetMonth.json")["bulan"]
        con, _ = ab.buka_db(KUE)
        for bulan, a in acuan.items():
            h = ab.hitung_bulan(con, int(bulan.replace("-", "")))
            self.assertEqual(h["jenis"], "tracking")
            per = {x["kategori"]: x for x in h["kategori"]}
            for nama, v in a["kategori"].items():
                self.assertEqual(per[nama]["sisa"], v["balance"], (bulan, nama))
            self.assertIsNone(h["siap_dianggarkan"])
        con.close()

    def test_26_teks_ringkasan_jebol_terbesar_tanpa_kategori(self):
        kode, teks, _ = jalan("ringkasan", "--db", RINA, "--bulan", "September 2026")
        self.assertEqual(kode, 0)
        self.assertIn("- Iklan: minus Rp 1.100.000", teks)
        self.assertIn("- Pajak: minus Rp 200.000", teks)
        self.assertIn("Siap dianggarkan (To Budget): Rp 1.010.000", teks)
        self.assertIn("1. 13 Sep - Meta Ads - Rp 3.200.000 (Iklan)", teks)
        self.assertIn("Belanja Rumah: sisa Rp 149.999,50", teks)
        self.assertIn("1 transaksi belum berkategori (bersih Rp 275.000 keluar)", teks)
        self.assertNotIn("Salah Input", teks)            # transaksi terhapus tidak ikut
        self.assertNotIn("Ojek Online", teks)            # kategori terhapus -> digabung ke Transportasi

    def test_27_json_ringkasan(self):
        kode, teks, _ = jalan("ringkasan", "--db", RINA, "--bulan", "2026-09", "--json", "--top", "3")
        d = json.loads(teks)
        self.assertEqual(d["jebol"], ["Iklan", "Pajak"])
        self.assertEqual(Decimal(d["siap_dianggarkan"]), Decimal("1010000"))
        self.assertEqual(len(d["terbesar"]), 3)
        self.assertEqual(d["terbesar"][0]["tanggal"], "2026-09-13")

    def test_28_read_only_file_tidak_berubah(self):
        salin = self.tmp / "budget"
        shutil.copytree(RINA, salin)
        db = salin / "db.sqlite"
        sebelum = (hashlib.sha256(db.read_bytes()).hexdigest(), db.stat().st_mtime_ns)
        for argv in (("cek", "--db", salin), ("kategori", "--db", salin), ("ringkasan", "--db", salin)):
            self.assertEqual(jalan(*argv)[0], 0)
        self.assertEqual((hashlib.sha256(db.read_bytes()).hexdigest(), db.stat().st_mtime_ns), sebelum)
        self.assertEqual(sorted(p.name for p in salin.iterdir()), ["acuan-getBudgetMonth.json", "db.sqlite",
                                                                     "metadata.json"])

    def test_29_db_terkunci_pesan_awam(self):
        salin = self.tmp / "budget"
        shutil.copytree(RINA, salin)
        kunci = sqlite3.connect(str(salin / "db.sqlite"), isolation_level=None)
        kunci.execute("BEGIN EXCLUSIVE")
        try:
            kode, _, err = jalan("ringkasan", "--db", salin)
        finally:
            kunci.execute("ROLLBACK")
            kunci.close()
        self.assertEqual(kode, 4)
        self.assertIn("coba", err.lower())

    def test_30_bukan_budget_actual_zip_dan_hilang(self):
        lain = self.tmp / "lain.sqlite"
        c = sqlite3.connect(str(lain))
        c.execute("CREATE TABLE barang (id INTEGER)")
        c.commit()
        c.close()
        kode, _, err = jalan("cek", "--db", lain)
        self.assertEqual(kode, 4)
        self.assertIn("tidak dikenali", err)
        z = self.tmp / "My-Finances.zip"
        z.write_bytes(b"PK\x03\x04")
        self.assertEqual(jalan("cek", "--db", z)[0], 2)
        self.assertEqual(jalan("cek", "--db", self.tmp / "tidak-ada")[0], 3)
        teks = self.tmp / "teks.sqlite"
        teks.write_text("bukan database", encoding="utf-8")
        self.assertEqual(jalan("cek", "--db", teks)[0], 4)

    def test_31_cari_dan_folder_budget(self):
        data = self.tmp / "Actual"
        shutil.copytree(RINA, data / "Studio-Rina-abc123")
        kode, teks, _ = jalan("cari", "--folder", data)
        self.assertEqual(kode, 0)
        self.assertIn("Studio Rina (fiktif)", teks)
        kode, teks, _ = jalan("cek", "--db", data)   # folder data berisi satu budget -> dipilih otomatis
        self.assertEqual(kode, 0)
        shutil.copytree(RINA, data / "Budget-Kedua")
        kode, _, err = jalan("cek", "--db", data)
        self.assertEqual(kode, 2)
        self.assertIn("lebih dari satu", err)
        kode, _, _ = jalan("cari", "--folder", self.tmp / "kosong")
        self.assertEqual(kode, 3)

    def test_32_daftar_kategori(self):
        kode, teks, _ = jalan("kategori", "--db", RINA, "--json")
        d = json.loads(teks)
        nama = [x["kategori"] for x in d]
        self.assertIn("Iklan", nama)
        self.assertNotIn("Ojek Online", nama)
        self.assertTrue([x for x in d if x["kategori"] == "Arsip Lama"][0]["disembunyikan"])



class UjiV101(TmpMixin, unittest.TestCase):
    """Perbaikan v1.0.1 dari uji independen (examples/HASIL-UJI.md temuan 1-4, 6)."""

    def budget_dengan_hold(self):
        salin = self.tmp / "budget"
        shutil.copytree(RINA, salin)
        c = sqlite3.connect(str(salin / "db.sqlite"))
        c.execute("INSERT INTO zero_budget_months (id, buffered) VALUES ('2026-09', 100000000)")
        c.commit()
        c.close()
        return salin

    def test_33_dana_ditahan_tampil_di_teks(self):
        b = self.budget_dengan_hold()
        kode, teks, _ = jalan("ringkasan", "--db", b, "--bulan", "2026-09")
        self.assertEqual(kode, 0)
        self.assertIn("Siap dianggarkan (To Budget): Rp 10.000", teks)
        self.assertIn("Ditahan untuk bulan depan (Hold): Rp 1.000.000", teks)
        kode, teks, _ = jalan("ringkasan", "--db", b, "--bulan", "2026-10")
        self.assertIn("ditahan bulan lalu dan masuk ke bulan ini: Rp 1.000.000", teks)
        # tanpa hold: baris tidak muncul, To Budget tetap seperti Actual
        kode, teks, _ = jalan("ringkasan", "--db", RINA, "--bulan", "2026-09")
        self.assertNotIn("Ditahan", teks)

    def test_34_hold_mengikuti_rumus_to_budget(self):
        b = self.budget_dengan_hold()
        con, _ = ab.buka_db(b)
        sep, okt = ab.hitung_bulan(con, 202609), ab.hitung_bulan(con, 202610)
        con.close()
        self.assertEqual(sep["siap_dianggarkan"], 101000000 - 100000000)
        self.assertEqual(okt["siap_dianggarkan"], -9000000)  # sama dengan tanpa hold (dana dipindah, tidak hilang)
        self.assertEqual(sep["ditahan"], 100000000)

    def tulis(self, isi):
        p = self.tmp / "mutasi.csv"
        p.write_text(isi, encoding="utf-8")
        out = self.tmp / "hasil.csv"
        kode, teks, err = jalan("konversi", p, "--keluaran", out, "--json", "--timpa")
        self.assertEqual(kode, 0, err)
        return json.loads(teks), baca_csv(out)

    def test_35_setoran_penjualan_bukan_pindah_dana(self):
        d, rows = self.tulis("Tanggal,Keterangan,Debet,Kredit,Saldo\n"
                             "01/09/2026,SETORAN PENJUALAN QRIS,,\"850.000,00\",\"850.000,00\"\n"
                             "02/09/2026,SETORAN TUNAI,,\"500.000,00\",\"1.350.000,00\"\n"
                             "03/09/2026,TARIK TUNAI ATM,\"200.000,00\",,\"1.150.000,00\"\n")
        kat = {r["Notes"]: r["Category"] for r in rows}
        self.assertEqual(kat["SETORAN PENJUALAN QRIS"], "Pendapatan Usaha")
        self.assertEqual(kat["SETORAN TUNAI"], "")
        ragu = {x["keterangan"]: x["alasan"] for x in d["ragu"]}
        self.assertNotIn("SETORAN PENJUALAN QRIS", ragu)
        self.assertIn("HASIL JUALAN", ragu["SETORAN TUNAI"])
        self.assertNotIn("PINDAH DANA", ragu["SETORAN TUNAI"])
        self.assertIn("PINDAH DANA", ragu["TARIK TUNAI ATM"])

    def test_36_payee_transfer_bernama(self):
        kode, teks, _ = jalan("ringkasan", "--db", RINA, "--bulan", "2026-09", "--top", "12")
        self.assertIn("Transfer ke Tabungan Pajak - Rp 600.000 (Pajak)", teks)
        self.assertNotIn("(tanpa payee)", teks)

    def test_37_koma_satu_digit_dibaca_desimal_indonesia_dan_ditandai(self):
        d, rows = self.tulis("Tanggal,Keterangan,Debet,Kredit\n01/09/2026,BIAYA MATERAI,\"12,5\",\n"
                             "02/09/2026,TRANSFER DARI ANI,,\"1.000.000\"\n")
        self.assertEqual(d["deteksi"]["desimal"], "koma")
        self.assertEqual(rows[0]["Amount"], "-12.50")
        self.assertEqual(rows[1]["Amount"], "1000000")
        self.assertTrue(any("sangat kecil" in x["alasan"] for x in d["ragu"]))

    def test_38_rujukan_kas_umkm_dan_versi(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        readme = (SKILL / "README.md").read_text(encoding="utf-8")
        self.assertIn("kas-umkm", skill.split("---")[1])   # di description
        self.assertIn("Kas UMKM", readme)
        self.assertEqual(ab.VERSI, "1.0.1")
        fmt = (SKILL / "references" / "format-bank.md").read_text(encoding="utf-8")
        self.assertIn("`12,5` = Rp 12,50", fmt)



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "actual_budget.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["konversi", os.path.join(t, "m.csv"), "--timp"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60, cwd=t)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "m-actual.csv")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main(verbosity=1)
