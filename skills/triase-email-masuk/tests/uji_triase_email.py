#!/usr/bin/env python3
"""Uji regresi triase_email.py. Jalankan: python3 tests/uji_triase_email.py (Windows: python / py)."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path

RAKIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAKIT / "scripts"))
import triase_email as t  # noqa: E402

ACUAN = date(2026, 10, 6)


def csv_tmp(isi, nama="x.csv", mentah=None):
    d = tempfile.mkdtemp()
    p = os.path.join(d, nama)
    with open(p, "wb") as f:
        f.write(mentah if mentah is not None else isi.encode("utf-8"))
    return p


def jalan(path, *opsi):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        kode = t.main([path, *opsi])
    return kode, out.getvalue(), err.getvalue()


class TesAngka(unittest.TestCase):
    def test_nominal(self):
        self.assertEqual(t.cari_nominal("Rp 12.500.000 dan Rp1,5 juta serta 750rb"), [12500000, 1500000, 750000])
        self.assertEqual(t.cari_nominal("total IDR 2.000.000,00"), [2000000])
        self.assertEqual(t.cari_nominal("tanpa angka uang 2026"), [])

    def test_tanggal(self):
        tgl, rel = t.cari_tenggat("bayar paling lambat 15 Oktober 2026, atau besok jam 14.00", ACUAN)
        self.assertEqual(tgl, ["2026-10-15"])
        self.assertIn("besok", rel)
        tgl, _ = t.cari_tenggat("tenggat 31/10/2026 dan 2026-11-02, bukan 99 Foo", ACUAN)
        self.assertEqual(tgl, ["2026-10-31", "2026-11-02"])
        tgl, _ = t.cari_tenggat("30 Februari 2026", ACUAN)
        self.assertEqual(tgl, [])


class TesPhishing(unittest.TestCase):
    def test_nama_vs_domain(self):
        skor, alasan, _ = t.periksa_phishing("Layanan BCA", "cs@bca-secure.xyz", "", "Akun diblokir",
                                             "Segera verifikasi akun di https://bit.ly/abc123, masukkan PIN dan OTP.")
        self.assertGreaterEqual(skor, 6)
        self.assertTrue(any("bca" in a for a in alasan))

    def test_email_sah_tidak_dicurigai(self):
        skor, alasan, _ = t.periksa_phishing("Bu Rina", "rina@tokomaju.co.id", "", "Pesanan 12 pcs",
                                             "Mohon kirim penawaran, terima kasih. Info: https://tokomaju.co.id/katalog")
        self.assertLess(skor, 2)
        self.assertEqual(alasan, [])

    def test_ip_dan_balas_ke(self):
        skor, alasan, tl = t.periksa_phishing("Admin", "admin@vendor.co.id", "x@lain.com", "Invoice",
                                              "Bayar di http://192.168.4.5/bayar")
        self.assertTrue(any("balasan" in a for a in alasan))
        self.assertTrue(any("IP" in c for x in tl for c in x["catatan"]))


class TesEnd2End(unittest.TestCase):
    def test_csv_dan_urutan(self):
        isi = ("from,subject,date,body\n"
               '"Pak Budi <budi@klien.co.id>",Revisi,2026-10-05,"Mohon kabari segera, tenggat 7 Oktober 2026, Rp 25.000.000"\n'
               '"Toko Promo <promo@iklan.com>",Flash sale,2026-10-05,"Diskon 50% promo voucher. Berhenti berlangganan di sini"\n'
               '"Bank <x@bank-aman.top>",Akun diblokir,2026-10-05,"Klik tautan https://bit.ly/q dan masukkan OTP segera"\n')
        p = csv_tmp(isi)
        kode, out, _ = jalan(p, "--sekarang", "2026-10-06")
        self.assertEqual(kode, 0)
        lap = json.loads(out)
        kat = {e["id"]: e["kategori_dugaan"] for e in lap["email"]}
        self.assertEqual(kat["E3"], "phishing dicurigai")
        self.assertEqual(kat["E2"], "promosi/spam")
        self.assertIn(kat["E1"], ("mendesak", "perlu balasan", "tagihan/pembayaran"))
        self.assertEqual(lap["urutan_dugaan"][0], "E3")
        self.assertEqual(lap["email"][0]["nominal_rp"], [25000000])
        self.assertIn("UNTUK_AGENT_SAJA", lap)

    def test_folder_eml_dan_txt(self):
        d = tempfile.mkdtemp()
        Path(d, "a.eml").write_text("From: Sari <sari@mitra.id>\nSubject: Tagihan\nDate: Mon, 5 Oct 2026 09:00:00 +0700\n\n"
                                    "Invoice INV-7 Rp 3.200.000 jatuh tempo 10 Oktober 2026.", encoding="utf-8")
        Path(d, "b.txt").write_text("Halo, rapat besok jam 10.00 ya, mohon konfirmasi?", encoding="utf-8")
        Path(d, "c.png").write_bytes(b"\x89PNG")
        kode, out, _ = jalan(d, "--sekarang", "2026-10-06")
        self.assertEqual(kode, 0)
        lap = json.loads(out)
        self.assertEqual(lap["jumlah_email"], 2)
        self.assertEqual(lap["email"][0]["kategori_dugaan"], "tagihan/pembayaran")

    def test_mbox(self):
        p = csv_tmp("From a@b.c Mon Oct  5 09:00:00 2026\nFrom: A <a@b.co.id>\nSubject: Tanya\n\nBisa kirim katalog?\n", "x.mbox")
        kode, out, _ = jalan(p)
        self.assertEqual(kode, 0)
        self.assertEqual(json.loads(out)["jumlah_email"], 1)

    def test_ringkas_dan_keluar(self):
        p = csv_tmp("dari,subjek,tanggal,isi\nA <a@b.co.id>,Halo,2026-10-05,Mohon balas ya\n")
        kode, out, _ = jalan(p, "--format", "ringkas")
        self.assertEqual(kode, 0)
        self.assertIn("UNTUK AGENT SAJA", out)
        tujuan = os.path.join(tempfile.mkdtemp(), "laporan.json")
        kode, out, _ = jalan(p, "--keluar", tujuan)
        self.assertEqual(kode, 0)
        self.assertTrue(json.loads(Path(tujuan).read_text(encoding="utf-8"))["jumlah_email"] == 1)


class TesDataRusak(unittest.TestCase):
    def test_berkas_tidak_ada(self):
        kode, _, err = jalan("/tidak/ada/sama/sekali")
        self.assertEqual(kode, 1)
        self.assertIn("Gagal", err)

    def test_csv_kolom_salah(self):
        kode, _, err = jalan(csv_tmp("a,b\n1,2\n"))
        self.assertEqual(kode, 1)

    def test_biner_dan_kosong(self):
        kode, _, _ = jalan(csv_tmp("", mentah=b"\x00\x01\xff\xfe\x00"))
        self.assertEqual(kode, 1)
        kode, _, err = jalan(csv_tmp("", nama="kosong.csv"))
        self.assertEqual(kode, 1)

    def test_tanggal_acuan_salah(self):
        kode, _, err = jalan(csv_tmp("from,subject,date,body\nA,B,C,D\n"), "--sekarang", "besok")
        self.assertEqual(kode, 2)

    def test_baris_tanpa_isi(self):
        kode, out, _ = jalan(csv_tmp("from,subject,date,body\n,,,\n"))
        self.assertEqual(kode, 0)
        self.assertTrue(json.loads(out)["email"][0]["isi_kosong"])


if __name__ == "__main__":
    unittest.main()
