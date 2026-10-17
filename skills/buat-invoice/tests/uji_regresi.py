#!/usr/bin/env python3
"""Uji regresi buat-invoice. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Fokus: penomoran (nomor baru = nomor terakhir + 1, aturan ganti bulan/tahun) dan data yang tidak diberikan
(kota, penanda tangan) tidak pernah dikarang -> placeholder [isi ...].
Angka invoice contoh (templates/contoh-invoice.json), dihitung manual:
  100 x 65.000 = 6.500.000; diskon 5% = 325.000 -> 6.175.000; + desain 500.000 = 6.675.000
  + ongkir 75.000 = 6.750.000; DP 3.000.000 -> sisa 3.750.000.
"""
import contextlib
import copy
import datetime
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
sys.dont_write_bytecode = True
import buat_invoice as B  # noqa: E402

with open(os.path.join(AKAR, "templates", "contoh-invoice.json"), encoding="utf-8") as _f:
    CONTOH = json.load(_f)

D = datetime.date


class UjiNomor(unittest.TestCase):
    def n(self, terakhir, tgl=None, lanjut=False):
        return B.nomor_berikutnya(terakhir, tgl, lanjut)[0]

    def test_bulan_sama_plus_satu(self):
        # kasus uji OpenClaw: terakhir 0012 -> baru 0013 (bukan 0012 dobel)
        self.assertEqual(self.n("INV/2026/09/0012", D(2026, 9, 29)), "INV/2026/09/0013")
        self.assertEqual(self.n("INV/2026/09/0007", D(2026, 9, 1)), "INV/2026/09/0008")

    def test_tanpa_tanggal_plus_satu(self):
        self.assertEqual(self.n("INV/2026/09/0012"), "INV/2026/09/0013")
        self.assertEqual(self.n("INV-0099"), "INV-0100")
        self.assertEqual(self.n("12"), "13")

    def test_nol_depan_dan_melebar(self):
        self.assertEqual(self.n("INV/2026/09/0009", D(2026, 9, 5)), "INV/2026/09/0010")
        self.assertEqual(self.n("INV/2026/09/9999", D(2026, 9, 5)), "INV/2026/09/10000")

    def test_ganti_bulan_mulai_satu(self):
        baru, ket = B.nomor_berikutnya("INV/2026/09/0012", D(2026, 10, 2))
        self.assertEqual(baru, "INV/2026/10/0001")
        self.assertIn("Periode berganti", ket)
        self.assertIn("--urut-lanjut", ket)

    def test_ganti_bulan_urut_lanjut(self):
        self.assertEqual(self.n("INV/2026/09/0012", D(2026, 10, 2), True), "INV/2026/10/0013")

    def test_ganti_tahun(self):
        self.assertEqual(self.n("INV/2026/12/0045", D(2027, 1, 3)), "INV/2027/01/0001")
        self.assertEqual(self.n("INV-2026-0045", D(2027, 1, 3)), "INV-2027-0001")
        self.assertEqual(self.n("INV-2026-0045", D(2026, 11, 3)), "INV-2026-0046")  # nomor tahunan, bulan tak berpengaruh

    def test_format_romawi_urut_di_depan(self):
        # tahun paling kanan TIDAK boleh ikut dinaikkan (bug lama: 2026 -> 2027)
        self.assertEqual(self.n("012/INV/IX/2026", D(2026, 9, 29)), "013/INV/IX/2026")
        self.assertEqual(self.n("012/INV/IX/2026", D(2026, 10, 1)), "001/INV/X/2026")
        self.assertEqual(self.n("012/INV/IX/2026"), "013/INV/IX/2026")

    def test_tanggal_mundur_error(self):
        with self.assertRaises(ValueError):
            B.nomor_berikutnya("INV/2026/09/0012", D(2026, 8, 31))

    def test_tanpa_angka_error(self):
        for s in ("INV/ABC", "", "2026"):
            with self.assertRaises(ValueError):
                B.nomor_berikutnya(s, D(2026, 9, 1))


class UjiCLI(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def jalan(self, data, *argv):
        f = os.path.join(self.dir, "inv.json")
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = B.main(["--file", f] + list(argv))
        return kode, out.getvalue(), err.getvalue()

    def test_contoh_angka_dan_nomor(self):
        kode, out, _ = self.jalan(CONTOH, "--nomor-terakhir", "INV/2026/09/0012")
        self.assertEqual(kode, 0)
        self.assertIn("**No.:** INV/2026/09/0013", out)
        self.assertIn("Nomor terakhir dibaca: INV/2026/09/0012 -> nomor baru: INV/2026/09/0013", out)
        self.assertIn("Rp 6.750.000", out)
        self.assertIn("Rp 3.750.000", out)
        self.assertIn("Bandung, 23 September 2026", out)
        self.assertNotIn("[isi", out)

    def test_json_nomor(self):
        kode, out, _ = self.jalan(CONTOH, "--nomor-terakhir", "INV/2026/08/0030", "--format", "json")
        self.assertEqual(kode, 0)
        h = json.loads(out)
        self.assertEqual(h["nomor"], "INV/2026/09/0001")
        self.assertIn("Periode berganti", h["keterangan_nomor"])
        self.assertEqual(h["perlu_diisi"], [])

    def test_nomor_mundur_exit2(self):
        kode, _, err = self.jalan(CONTOH, "--nomor-terakhir", "INV/2026/10/0003")
        self.assertEqual(kode, 2)
        self.assertIn("tidak boleh mundur", err)

    def test_kota_dan_penanda_tangan_tidak_dikarang(self):
        d = copy.deepcopy(CONTOH)
        d["tanda_tangan"] = {}
        html_path = os.path.join(self.dir, "inv.html")
        kode, out, _ = self.jalan(d, "--html", html_path)
        self.assertEqual(kode, 0)
        self.assertIn("[isi kota], 23 September 2026", out)
        self.assertIn("**[isi nama penanda tangan]**", out)
        self.assertIn("PERLU DIISI: kota, nama penanda tangan", out)
        with open(html_path, encoding="utf-8") as fh:
            isi = fh.read()
        self.assertIn("[isi kota], 23 September 2026", isi)
        self.assertIn("[isi nama penanda tangan]", isi)
        for karangan in ("Jakarta, 23", "Rina"):
            self.assertNotIn(karangan, out)

    def test_tanpa_tanda_tangan_sama_sekali(self):
        d = copy.deepcopy(CONTOH)
        del d["tanda_tangan"]
        kode, out, _ = self.jalan(d, "--format", "json")
        self.assertEqual(kode, 0)
        self.assertEqual(json.loads(out)["perlu_diisi"], ["kota", "nama penanda tangan"])

    def test_nomor_manual_menang(self):
        d = copy.deepcopy(CONTOH)
        d["nomor"] = "INV/2026/09/0050"
        kode, out, _ = self.jalan(d, "--nomor-terakhir", "INV/2026/09/0012")
        self.assertEqual(kode, 0)
        self.assertIn("**No.:** INV/2026/09/0050", out)


class UjiNomorTidakDobel(unittest.TestCase):
    """v1.0.5: dua pembuatan berturut-turut tidak boleh menghasilkan nomor yang sama (temuan uji platform:
    nomor invoice dobel). --counter-file mencatat nomor yang sudah dibuat + nama pembeli."""

    setUp, tearDown, jalan = UjiCLI.setUp, UjiCLI.tearDown, UjiCLI.jalan

    def data(self, pembeli):
        d = copy.deepcopy(CONTOH)
        d["pembeli"] = {"nama": pembeli}
        return d

    def no(self, out):
        return json.loads(out)["nomor"]

    def test_dua_kali_berantai_tanpa_counter(self):
        k1, o1, _ = self.jalan(self.data("PT A Fiktif"), "--nomor-terakhir", "INV/2026/09/0012", "--format", "json")
        k2, o2, _ = self.jalan(self.data("PT B Fiktif"), "--nomor-terakhir", self.no(o1), "--format", "json")
        self.assertEqual((k1, k2), (0, 0))
        self.assertEqual((self.no(o1), self.no(o2)), ("INV/2026/09/0013", "INV/2026/09/0014"))

    def test_nomor_terakhir_sama_dua_kali_dengan_counter(self):
        # agent menyalin lagi "nomor terakhir 0012" dari pesan pengguna untuk invoice kedua
        c = os.path.join(self.dir, "nomor-invoice.json")
        o1 = self.jalan(self.data("PT A Fiktif"), "--nomor-terakhir", "INV/2026/09/0012", "--counter-file", c,
                        "--format", "json")[1]
        k2, o2, _ = self.jalan(self.data("PT B Fiktif"), "--nomor-terakhir", "INV/2026/09/0012", "--counter-file",
                               c, "--format", "json")
        self.assertEqual(k2, 0)
        self.assertEqual((self.no(o1), self.no(o2)), ("INV/2026/09/0013", "INV/2026/09/0014"))
        self.assertTrue(any("sudah dipakai untuk PT A Fiktif" in w for w in json.loads(o2)["peringatan"]))
        # mode counter saja melanjutkan, tidak mengulang dari 0001
        o3 = self.jalan(self.data("PT C Fiktif"), "--counter-file", c, "--format", "json")[1]
        self.assertEqual(self.no(o3), "INV/2026/09/0015")
        with open(c, encoding="utf-8") as fh:
            self.assertEqual(sorted(json.load(fh)["terbit"]),
                             ["INV/2026/09/0013", "INV/2026/09/0014", "INV/2026/09/0015"])

    def test_counter_saja_dua_kali_hari_sama(self):
        c = os.path.join(self.dir, "nomor-invoice.json")
        n1 = self.no(self.jalan(self.data("PT A Fiktif"), "--counter-file", c, "--format", "json")[1])
        n2 = self.no(self.jalan(self.data("PT A Fiktif"), "--counter-file", c, "--format", "json")[1])
        self.assertEqual((n1, n2), ("INV/2026/09/0001", "INV/2026/09/0002"))

    def test_revisi_pembeli_sama_nomor_tetap(self):
        c = os.path.join(self.dir, "nomor-invoice.json")
        argv = ("--nomor-terakhir", "INV/2026/09/0012", "--counter-file", c, "--format", "json")
        n1 = self.no(self.jalan(self.data("PT A Fiktif"), *argv)[1])
        o2 = self.jalan(self.data("PT A Fiktif"), *argv)[1]
        self.assertEqual((n1, self.no(o2)), ("INV/2026/09/0013", "INV/2026/09/0013"))
        self.assertTrue(any("dianggap revisi" in w for w in json.loads(o2)["peringatan"]))

    def test_folder_kerja_berbeda_file_counter_sama(self):
        c = os.path.join(self.dir, "nomor-invoice.json")
        asal = os.getcwd()
        hasil = []
        try:
            for i, pembeli in enumerate(("PT A Fiktif", "PT B Fiktif")):
                sub = os.path.join(self.dir, "kerja{}".format(i))
                os.mkdir(sub)
                os.chdir(sub)
                hasil.append(self.no(self.jalan(self.data(pembeli), "--nomor-terakhir", "INV/2026/09/0012",
                                                "--counter-file", c, "--format", "json")[1]))
        finally:
            os.chdir(asal)
        self.assertEqual(hasil, ["INV/2026/09/0013", "INV/2026/09/0014"])

    def test_nomor_manual_bentrok_ditolak(self):
        c = os.path.join(self.dir, "nomor-invoice.json")
        self.jalan(self.data("PT A Fiktif"), "--nomor-terakhir", "INV/2026/09/0012", "--counter-file", c)
        d = self.data("PT B Fiktif")
        d["nomor"] = "INV/2026/09/0013"
        kode, _, err = self.jalan(d, "--counter-file", c)
        self.assertEqual(kode, 2)
        self.assertIn("tidak boleh dobel", err)

    def test_file_counter_rusak(self):
        c = os.path.join(self.dir, "nomor-invoice.json")
        with open(c, "w", encoding="utf-8") as fh:
            fh.write('{"terbit": [1]}')
        self.assertEqual(self.jalan(self.data("PT A Fiktif"), "--counter-file", c)[0], 2)


class UjiNamaBerkasDanRekening(unittest.TestCase):
    """v1.0.6 (uji OpenClaw 2026-10-14): nama berkas HTML harus sama dengan nomor yang tampil di chat
    (invoice-INV-013.html vs 001/INV/X/2026), dan 'a.n.' rekening tidak boleh ditebak."""

    setUp, tearDown, jalan = UjiCLI.setUp, UjiCLI.tearDown, UjiCLI.jalan

    def data_oktober(self):
        d = copy.deepcopy(CONTOH)
        d["tanggal"] = "2026-10-02"
        d["pembayaran"] = []
        return d

    def test_nama_aman_dari_nomor(self):
        self.assertEqual(B.nama_berkas_dari_nomor("001/INV/X/2026"), "001-INV-X-2026")
        self.assertEqual(B.nama_berkas_dari_nomor("INV/2026/10/0013"), "INV-2026-10-0013")
        self.assertEqual(B.nama_berkas_dari_nomor("KWT\\2026/10/0004"), "KWT-2026-10-0004")
        self.assertEqual(B.nama_berkas_dari_nomor("///"), "tanpa-nomor")

    def test_placeholder_nomor_romawi_ganti_bulan(self):
        # nomor terakhir 012/INV/IX/2026 + tanggal Oktober -> 001/INV/X/2026; berkas HARUS bernama dari nomor itu
        pola = os.path.join(self.dir, "invoice-{nomor}.html")
        kode, out, _ = self.jalan(self.data_oktober(), "--nomor-terakhir", "012/INV/IX/2026", "--html", pola,
                                  "--format", "json")
        self.assertEqual(kode, 0)
        h = json.loads(out)
        self.assertEqual(h["nomor"], "001/INV/X/2026")
        harapan = os.path.join(self.dir, "invoice-001-INV-X-2026.html")
        self.assertEqual(h["html_disimpan_ke"], harapan)
        self.assertTrue(os.path.isfile(harapan))
        with open(harapan, encoding="utf-8") as fh:
            self.assertIn("001/INV/X/2026", fh.read())
        self.assertNotIn("012", os.path.basename(harapan))      # tidak mengulang nomor terakhir pengguna

    def test_folder_nama_otomatis_invoice_dan_kuitansi(self):
        kode, out, _ = self.jalan(self.data_oktober(), "--nomor-terakhir", "INV/2026/10/0012", "--html", self.dir)
        self.assertEqual(kode, 0)
        self.assertTrue(os.path.isfile(os.path.join(self.dir, "invoice-INV-2026-10-0013.html")))
        self.assertIn("invoice-INV-2026-10-0013.html", out)
        d = self.data_oktober()
        d["jenis_dokumen"], d["prefix"] = "kuitansi", "KWT"
        d["pembayaran"] = [{"tanggal": "2026-10-02", "jumlah": "7.500.000", "keterangan": "DP"}]
        kode, out, _ = self.jalan(d, "--nomor-terakhir", "KWT/2026/10/0003", "--html", self.dir + os.sep)
        self.assertEqual(kode, 0)
        self.assertTrue(os.path.isfile(os.path.join(self.dir, "kuitansi-KWT-2026-10-0004.html")))
        # v1.0.8: catatan lampiran berlaku untuk invoice maupun kuitansi (kalimatnya diperbarui)
        self.assertIn("untuk invoice maupun kuitansi. Urutan: lampirkan berkas di baris BERKAS", out)
        self.assertIn("kirim file", out)

    def test_path_biasa_tetap_dipakai_apa_adanya(self):
        f = os.path.join(self.dir, "invoice-saya.html")
        self.assertEqual(self.jalan(CONTOH, "--html", f)[0], 0)
        self.assertTrue(os.path.isfile(f))

    def test_peringatan_nomor_sama_dengan_nomor_terakhir(self):
        d = copy.deepcopy(CONTOH)
        d["nomor"] = "INV/2026/09/0012"
        kode, out, _ = self.jalan(d, "--nomor-terakhir", "INV/2026/09/0012", "--format", "json")
        self.assertEqual(kode, 0)
        self.assertTrue(any("sama dengan nomor terakhir" in w for w in json.loads(out)["peringatan"]))

    def test_rekening_tanpa_atas_nama_tidak_ditebak(self):
        d = copy.deepcopy(CONTOH)
        d["rekening"] = [{"bank": "BRI", "nomor": "0000000001"}]
        f = os.path.join(self.dir, "inv.html")
        kode, out, _ = self.jalan(d, "--html", f)
        self.assertEqual(kode, 0)
        self.assertIn("- BRI 0000000001\n", out)
        self.assertNotIn("a.n.", out)
        with open(f, encoding="utf-8") as fh:
            isi = fh.read()
        self.assertIn("BRI 0000000001", isi)
        self.assertNotIn("a.n.", isi)
        # atas nama diberikan pengguna -> tetap tampil
        d["rekening"][0]["atas_nama"] = "Nama Fiktif"
        self.assertIn("BRI 0000000001 a.n. Nama Fiktif", self.jalan(d)[1])

    def test_penanda_tangan_tidak_diambil_dari_rekening(self):
        # script tidak pernah mengisi penanda tangan dari data lain (rekening/penjual): tetap placeholder
        d = copy.deepcopy(CONTOH)
        d["tanda_tangan"] = {}
        d["rekening"] = [{"bank": "BCA", "nomor": "0000000002", "atas_nama": "Rini Fiktif"}]
        kode, out, _ = self.jalan(d)
        self.assertEqual(kode, 0)
        self.assertIn("**[isi nama penanda tangan]**", out)
        self.assertNotIn("**Rini Fiktif**", out)


class UjiPPh23(unittest.TestCase):
    """v1.0.3 (uji OpenClaw 2026-10-01): PPh 23 jasa 2% sebagai info, total tagihan tidak berubah.
    Skenario: 8.750.000 + 2 x 2.375.000 = 13.500.000; PPN 12% x 11/12 x 13.500.000 = 1.485.000 -> total 14.985.000;
    PPh 23 = 2% x 13.500.000 = 270.000 -> estimasi diterima bersih 14.985.000 - 270.000 = 14.715.000."""

    DATA = {"tanggal": "2026-10-01", "jatuh_tempo_hari": 14,
            "penjual": {"nama": "CV Uji Konsultan", "pkp": True, "npwp": "0000000000000000"},
            "pembeli": {"nama": "PT Klien Uji"},
            "items": [{"nama": "Jasa konsultasi", "qty": 1, "harga": "8.750.000"},
                      {"nama": "Pendampingan", "qty": 2, "satuan": "hari", "harga": "2.375.000"}],
            "ppn": True, "pph23": True}

    setUp, tearDown, jalan = UjiCLI.setUp, UjiCLI.tearDown, UjiCLI.jalan

    def test_skenario_konsultan(self):
        kode, out, _ = self.jalan(self.DATA, "--format", "json")
        self.assertEqual(kode, 0)
        h = json.loads(out)
        self.assertEqual(h["total"], 14985000)
        self.assertEqual(h["pph23"]["pph23"], 270000)
        self.assertEqual(h["pph23"]["estimasi_diterima_bersih"], 14715000)
        self.assertEqual(h["sisa"], 14985000)          # total tagihan tidak dikurangi PPh 23
        kode, out, _ = self.jalan(self.DATA)
        self.assertIn("2% x Rp 13.500.000 = Rp 270.000", out)
        self.assertIn("Estimasi diterima bersih: Rp 14.715.000", out)
        self.assertIn("**TOTAL** | **Rp 14.985.000**", out)

    def test_tanpa_npwp_dan_dasar_manual_dan_pembulatan(self):
        d = copy.deepcopy(self.DATA)
        d["pph23"] = {"tanpa_npwp": True}
        h = json.loads(self.jalan(d, "--format", "json")[1])
        self.assertEqual(h["pph23"]["pph23"], 540000)     # 4% x 13.500.000
        d["pph23"] = {"dasar": "1.234.567"}
        h = json.loads(self.jalan(d, "--format", "json")[1])
        self.assertEqual(h["pph23"]["pph23"], 24691)      # 2% x 1.234.567 = 24.691,34 -> ke bawah
        d["pph23"] = {"dasar": "99.000.000"}
        self.assertEqual(self.jalan(d)[0], 2)             # dasar melebihi nilai sebelum PPN
        d["pph23"] = {"tarif": "0"}
        self.assertEqual(self.jalan(d)[0], 2)

    def test_tidak_aktif_dan_kuitansi(self):
        d = copy.deepcopy(self.DATA)
        d["pph23"] = False
        h = json.loads(self.jalan(d, "--format", "json")[1])
        self.assertIsNone(h["pph23"])
        d["pph23"], d["jenis_dokumen"] = True, "kuitansi"
        self.assertEqual(self.jalan(d)[0], 2)

    def test_html_memuat_info_pph23(self):
        f = os.path.join(self.dir, "inv.html")
        self.assertEqual(self.jalan(self.DATA, "--html", f)[0], 0)
        with open(f, encoding="utf-8") as fh:
            self.assertIn("Estimasi diterima bersih: Rp 14.715.000", fh.read())


class UjiBerkasAbsolutDanMeterai(unittest.TestCase):
    """v1.0.7 (uji ulang OpenClaw 2026-10-14): (a) script mencetak baris 'BERKAS: <path absolut>' supaya agent tidak
    menyusun path sendiri (path salah ketik -> lampiran gagal); (b) kalimat meterai dihitung dari angka:
    sisa Rp5.075.000 = DI ATAS Rp5 juta (bukan 'di bawah')."""

    setUp, tearDown, jalan = UjiCLI.setUp, UjiCLI.tearDown, UjiCLI.jalan

    def data_catering(self):
        # skenario uji 1.0.6: total 8.075.000, DP 3.000.000 -> sisa 5.075.000
        d = copy.deepcopy(CONTOH)
        d["tanggal"] = "2026-10-14"
        d["items"] = [{"nama": "Nasi box", "qty": 150, "satuan": "box", "harga": "32.500"},
                      {"nama": "Snack box", "qty": 150, "satuan": "box", "harga": "15.000", "diskon": "10%"},
                      {"nama": "Air mineral", "qty": 300, "satuan": "botol", "harga": "3.500"}]
        d["ongkir"] = "125.000"
        d["pembayaran"] = [{"tanggal": "2026-10-10", "jumlah": "3.000.000", "keterangan": "DP"}]
        return d

    def baris_berkas(self, out):
        baris = [x for x in out.splitlines() if x.startswith("BERKAS: ")]
        self.assertEqual(len(baris), 1)
        return baris[0][len("BERKAS: "):]

    def test_baris_berkas_absolut_invoice(self):
        cwd = os.getcwd()
        os.chdir(self.dir)
        try:
            # path RELATIF diberikan; baris BERKAS harus tetap absolut dan menunjuk berkas yang ada
            kode, out, _ = self.jalan(self.data_catering(), "--nomor-terakhir", "INV/2026/10/0007",
                                      "--html", "invoice-{nomor}.html")
        finally:
            os.chdir(cwd)
        self.assertEqual(kode, 0)
        path = self.baris_berkas(out)
        self.assertTrue(os.path.isabs(path))
        self.assertEqual(os.path.basename(path), "invoice-INV-2026-10-0008.html")
        self.assertTrue(os.path.isfile(path))
        self.assertIn("jangan menyusun atau menebak path", out)

    def test_baris_berkas_absolut_kuitansi_dan_json(self):
        d = self.data_catering()
        d["jenis_dokumen"], d["prefix"] = "kuitansi", "KWT"
        d["pembayaran"] = [{"tanggal": "2026-10-14", "jumlah": "7.500.000", "keterangan": "DP"}]
        kode, out, _ = self.jalan(d, "--nomor-terakhir", "KWT/2026/10/0003", "--html", self.dir)
        self.assertEqual(kode, 0)
        path = self.baris_berkas(out)
        self.assertTrue(os.path.isabs(path) and os.path.isfile(path))
        self.assertEqual(os.path.basename(path), "kuitansi-KWT-2026-10-0004.html")
        kode, out, _ = self.jalan(d, "--nomor-terakhir", "KWT/2026/10/0003", "--html", self.dir, "--format", "json")
        self.assertTrue(os.path.isabs(json.loads(out)["html_disimpan_ke"]))

    def test_tanpa_html_tanpa_baris_berkas(self):
        kode, out, _ = self.jalan(CONTOH)
        self.assertEqual(kode, 0)
        self.assertNotIn("BERKAS:", out)

    def test_meterai_sisa_5075000_di_atas_batas(self):
        kode, out, _ = self.jalan(self.data_catering(), "--nomor-terakhir", "INV/2026/10/0007", "--format", "json")
        self.assertEqual(kode, 0)
        h = json.loads(out)
        self.assertEqual(int(h["total"]), 8075000)
        self.assertEqual(int(h["sisa"]), 5075000)
        m = h["meterai"]
        self.assertFalse(m["wajib"])                        # DP 3 juta: invoice ini sendiri tidak wajib meterai
        self.assertIn("Sisa tagihan Rp 5.075.000 di atas Rp5.000.000", m["pesan"])
        self.assertIn("wajib bermeterai Rp10.000", m["pesan"])
        self.assertNotIn("di bawah", m["pesan"])
        self.assertNotIn("tidak lebih dari", m["pesan"])

    def test_meterai_sisa_pas_5jt_dan_di_bawah_tidak_wajib(self):
        d = self.data_catering()
        d["pembayaran"] = [{"tanggal": "2026-10-10", "jumlah": "3.075.000", "keterangan": "DP"}]   # sisa 5.000.000 pas
        pesan = json.loads(self.jalan(d, "--format", "json")[1])["meterai"]["pesan"]
        self.assertIn("Sisa tagihan Rp 5.000.000 tidak lebih dari Rp5.000.000", pesan)
        self.assertIn("tidak wajib meterai", pesan)
        d["pembayaran"] = [{"tanggal": "2026-10-10", "jumlah": "4.000.000", "keterangan": "DP"}]   # sisa 4.075.000
        pesan = json.loads(self.jalan(d, "--format", "json")[1])["meterai"]["pesan"]
        self.assertIn("Sisa tagihan Rp 4.075.000 tidak lebih dari Rp5.000.000", pesan)

    def test_meterai_dp_di_atas_5jt_wajib_dan_sisa_dinilai(self):
        d = self.data_catering()
        d["pembayaran"] = [{"tanggal": "2026-10-14", "jumlah": "5.000.001", "keterangan": "DP"}]
        m = json.loads(self.jalan(d, "--format", "json")[1])["meterai"]
        self.assertTrue(m["wajib"])
        self.assertIn("di atas Rp5.000.000", m["pesan"])
        self.assertIn("Sisa tagihan Rp 3.074.999 tidak lebih dari Rp5.000.000", m["pesan"])

    def test_meterai_total_kecil_tanpa_catatan_sisa(self):
        pesan = json.loads(self.jalan(CONTOH, "--format", "json")[1])["meterai"]["pesan"]   # total 6,75 jt, sisa 3,75 jt
        self.assertIn("Sisa tagihan Rp 3.750.000 tidak lebih dari Rp5.000.000", pesan)
        d = copy.deepcopy(CONTOH)
        d["items"], d["ongkir"], d["pembayaran"] = [{"nama": "Kaos", "qty": 10, "harga": "100.000"}], "", []
        pesan = json.loads(self.jalan(d, "--format", "json")[1])["meterai"]["pesan"]       # total 1 juta
        self.assertNotIn("Sisa tagihan", pesan)

    def test_meterai_termin_dinilai_per_termin(self):
        d = self.data_catering()
        d["pembayaran"] = []
        d["termin"] = [{"nama": "DP", "persen": 30, "jatuh_tempo": "2026-10-14"},
                       {"nama": "Pelunasan", "persen": 70, "jatuh_tempo": "2026-11-14"}]
        pesan = json.loads(self.jalan(d, "--format", "json")[1])["meterai"]["pesan"]
        # total 8.075.000: DP 30% = 2.422.500 (tidak lebih dari 5 juta), pelunasan 5.652.500 (di atas 5 juta)
        self.assertIn("DP Rp 2.422.500 (tidak lebih dari Rp5.000.000: tidak wajib meterai)", pesan)
        self.assertIn("Pelunasan Rp 5.652.500 (di atas Rp5.000.000: wajib bermeterai Rp10.000)", pesan)



class UjiBerkasTeksDanBalasanAkhir(unittest.TestCase):
    """v1.0.8 (uji bot Telegram asli G24, 17 Okt 2026): (a) bot asli hanya mengirim BALASAN TERAKHIR giliran, jadi
    invoice yang ditulis sebelum pemanggilan alat tidak sampai; (b) kanal chat OpenClaw menolak berkas HTML hasil
    script ('hostReadCapability permits only validated plain-text documents ...') tetapi menerima .txt teks biasa.
    Script kini bisa menulis versi teks (--txt -> baris 'BERKAS TEKS: <path absolut>') dengan angka yang sama persis.
    Skenario G24: 150 x 32.500 = 4.875.000; 150 x 15.000 = 2.250.000 - 10% (225.000) = 2.025.000;
    300 x 3.500 = 1.050.000; subtotal 7.950.000 + ongkir 125.000 = TOTAL 8.075.000; DP 3.000.000 -> sisa 5.075.000."""

    setUp, tearDown, jalan = UjiCLI.setUp, UjiCLI.tearDown, UjiCLI.jalan

    def data_g24(self):
        return {"jenis_dokumen": "invoice", "prefix": "INV", "tanggal": "2026-10-17", "jatuh_tempo_hari": 7,
                "penjual": {"nama": "Dapur Bu Rini Catering", "pkp": False},
                "pembeli": {"nama": "PT Kencana Fiktif Mandiri"},
                "items": [{"nama": "Nasi box ayam bakar", "qty": 150, "satuan": "box", "harga": "32.500"},
                          {"nama": "Snack box", "qty": 150, "satuan": "box", "harga": "15.000", "diskon": "10%"},
                          {"nama": "Air mineral botol", "qty": 300, "satuan": "botol", "harga": "3.500"}],
                "ongkir": "125.000", "ppn": False,
                "pembayaran": [{"tanggal": "2026-10-10", "jumlah": "3.000.000", "keterangan": "DP"}],
                "rekening": [{"bank": "Mandiri", "nomor": "1230009876543", "atas_nama": "Rini Kusumawati"}]}

    def baris(self, out, awalan):
        b = [x[len(awalan):] for x in out.splitlines() if x.startswith(awalan)]
        self.assertEqual(len(b), 1, awalan)
        self.assertTrue(os.path.isabs(b[0]) and os.path.isfile(b[0]), b[0])
        return b[0]

    def baca(self, path):
        with open(path, "rb") as fh:
            return fh.read()

    def lolos_teks_biasa(self, path, data):
        """Cermin aturan kanal chat OpenClaw untuk dokumen teks lokal: akhiran .txt, UTF-8 valid, >95% karakter
        tercetak (tab/baris baru dihitung tercetak)."""
        self.assertTrue(path.endswith(".txt"))
        teks = data.decode("utf-8")   # strict: gagal bila bukan UTF-8 valid
        tercetak = sum(1 for c in teks if c in "\t\n\r" or (ord(c) >= 32 and not 127 <= ord(c) <= 159))
        self.assertGreater(tercetak / len(teks), 0.95)
        self.assertNotIn("\x00", teks)
        return teks

    def test_g24_angka_nomor_dan_isi_lengkap(self):
        kode, out, _ = self.jalan(self.data_g24(), "--nomor-terakhir", "INV/2026/10/0007",
                                  "--counter-file", os.path.join(self.dir, "nomor-invoice.json"),
                                  "--html", os.path.join(self.dir, "invoice-{nomor}.html"),
                                  "--txt", os.path.join(self.dir, "invoice-{nomor}.txt"))
        self.assertEqual(kode, 0)
        self.assertEqual(os.path.basename(self.baris(out, "BERKAS: ")), "invoice-INV-2026-10-0008.html")
        path = self.baris(out, "BERKAS TEKS: ")
        self.assertEqual(os.path.basename(path), "invoice-INV-2026-10-0008.txt")
        teks = self.lolos_teks_biasa(path, self.baca(path))
        for wajib in ("INVOICE", "No.: INV/2026/10/0008", "Tanggal: 17 Oktober 2026", "Jatuh tempo: 24 Oktober 2026",
                      "Status: SEBAGIAN DIBAYAR", "Dari: Dapur Bu Rini Catering", "Kepada: PT Kencana Fiktif Mandiri",
                      "1. Nasi box ayam bakar: 150 box x Rp 32.500 = Rp 4.875.000",
                      "2. Snack box: 150 box x Rp 15.000 = Rp 2.250.000, diskon Rp 225.000 (10%), jumlah Rp 2.025.000",
                      "3. Air mineral botol: 300 botol x Rp 3.500 = Rp 1.050.000",
                      "Subtotal: Rp 7.950.000", "Ongkos kirim: Rp 125.000", "TOTAL: Rp 8.075.000",
                      "Sudah dibayar - DP (10 Oktober 2026): -Rp 3.000.000", "SISA TAGIHAN: Rp 5.075.000",
                      "Terbilang: Lima Juta Tujuh Puluh Lima Ribu Rupiah",
                      "- Mandiri 1230009876543 a.n. Rini Kusumawati",
                      "[isi kota], 17 Oktober 2026", "[isi nama penanda tangan]"):
            self.assertIn(wajib, teks)
        for dilarang in ("PPN", "**", "|", "Info untuk penjual", "BERKAS", "nomor-invoice.json", "_Lima"):
            self.assertNotIn(dilarang, teks)
        self.assertTrue(teks.endswith("Dapur Bu Rini Catering\n"))
        h = json.loads(self.jalan(self.data_g24(), "--nomor-terakhir", "INV/2026/10/0007", "--format", "json")[1])
        self.assertEqual((h["nomor"], int(h["total"]), int(h["dibayar"]), int(h["sisa"]), h["ppn"]),
                         ("INV/2026/10/0008", 8075000, 3000000, 5075000, None))

    def test_angka_teks_sama_dengan_markdown(self):
        """Tidak ada angka baru di versi teks kecuali nilai bruto baris berdiskon (qty x harga dari hitung())."""
        for data in (self.data_g24(), CONTOH, UjiPPh23.DATA):
            d = copy.deepcopy(data)
            if d is not CONTOH and d.get("ppn"):
                d["termin"] = [{"nama": "DP", "persen": 30, "jatuh_tempo": "2026-10-05"},
                               {"nama": "Pelunasan", "persen": 70, "jatuh_tempo": "2026-10-20"}]
            f = os.path.join(self.dir, "x.txt")
            kode, out, _ = self.jalan(d, "--txt", f)
            self.assertEqual(kode, 0)
            dokumen = out.split("\n---\n")[0]
            teks = self.baca(f).decode("utf-8")
            rp = r"Rp [0-9.,]*[0-9]"
            di_md, di_teks = set(re.findall(rp, dokumen)), set(re.findall(rp, teks))
            self.assertLessEqual(di_md, di_teks)
            h = json.loads(self.jalan(d, "--format", "json")[1])
            bruto = {B.format_rp(B.Decimal(str(b["bruto"]))) for b in h["baris"] if B.Decimal(str(b["diskon"]))}
            self.assertLessEqual(di_teks - di_md, bruto)

    def test_pkp_termin_pph23_dan_meterai_di_teks(self):
        d = copy.deepcopy(UjiPPh23.DATA)
        d["termin"] = [{"nama": "DP", "persen": 30, "jatuh_tempo": "2026-10-05"},
                       {"nama": "Pelunasan", "persen": 70, "jatuh_tempo": "2026-10-20"}]
        d["tanda_tangan"] = {"nama": "Sari Uji", "jabatan": "Direktur", "kota": "Bandung"}
        f = os.path.join(self.dir, "pkp.txt")
        self.assertEqual(self.jalan(d, "--txt", f)[0], 0)
        teks = self.lolos_teks_biasa(f, self.baca(f))
        for wajib in ("DPP: Rp 13.500.000", "DPP nilai lain (11/12): Rp 12.375.000", "PPN 12%: Rp 1.485.000",
                      "TOTAL: Rp 14.985.000", "Info PPh 23 (dipotong & disetor oleh PT Klien Uji",
                      "Estimasi diterima bersih: Rp 14.715.000", "Jadwal pembayaran:",
                      "- DP (30%): Rp 4.495.500, jatuh tempo 5 Oktober 2026",
                      "- Pelunasan (70%): Rp 10.489.500, jatuh tempo 20 Oktober 2026",
                      "Bandung, 1 Oktober 2026", "Sari Uji\nDirektur\nCV Uji Konsultan"):
            self.assertIn(wajib, teks)
        self.assertNotIn("PPN 11%", teks)

    def test_kuitansi_dp_teks_folder_dan_meterai(self):
        d = copy.deepcopy(CONTOH)
        d.update({"jenis_dokumen": "kuitansi", "prefix": "KWT", "tanggal": "2026-10-14", "ongkir": "",
                  "items": [{"nama": "Seragam batik", "qty": 60, "satuan": "pcs", "harga": "285.000"}],
                  "pembayaran": [{"tanggal": "2026-10-14", "jumlah": "7.500.000", "keterangan": "DP"}]})
        kode, out, _ = self.jalan(d, "--nomor-terakhir", "KWT/2026/10/0003", "--html", self.dir, "--txt", self.dir)
        self.assertEqual(kode, 0)
        self.assertEqual(os.path.basename(self.baris(out, "BERKAS: ")), "kuitansi-KWT-2026-10-0004.html")
        path = self.baris(out, "BERKAS TEKS: ")
        self.assertEqual(os.path.basename(path), "kuitansi-KWT-2026-10-0004.txt")
        teks = self.lolos_teks_biasa(path, self.baca(path))
        for wajib in ("KUITANSI", "No.: KWT/2026/10/0004", "Telah terima dari: PT Pelanggan Contoh",
                      "Uang sejumlah: Rp 7.500.000", "Terbilang: Tujuh Juta Lima Ratus Ribu Rupiah",
                      "Sisa yang belum dibayar: Rp 9.600.000 dari total Rp 17.100.000", "[ Meterai Rp10.000 ]"):
            self.assertIn(wajib, teks)
        self.assertEqual(teks.count("Terbilang:"), 1)   # satu terbilang saja: uang yang diterima

    def test_akhiran_txt_dipaksa_dan_json(self):
        kode, out, _ = self.jalan(CONTOH, "--txt", os.path.join(self.dir, "inv-teks"))
        self.assertEqual(kode, 0)
        self.assertTrue(self.baris(out, "BERKAS TEKS: ").endswith("inv-teks.txt"))
        self.assertNotIn("BERKAS: ", out)
        h = json.loads(self.jalan(CONTOH, "--txt", os.path.join(self.dir, "a.txt"), "--format", "json")[1])
        self.assertTrue(os.path.isabs(h["txt_disimpan_ke"]) and h["txt_disimpan_ke"].endswith("a.txt"))
        self.assertIsNone(h["html_disimpan_ke"])

    def test_tanpa_txt_tidak_ada_baris_berkas_teks(self):
        kode, out, _ = self.jalan(CONTOH, "--html", os.path.join(self.dir, "a.html"))
        self.assertEqual(kode, 0)
        self.assertNotIn("BERKAS TEKS", out)
        self.assertIn("balasan terakhir berisi dokumen LENGKAP", out)
        self.assertIsNone(json.loads(self.jalan(CONTOH, "--format", "json")[1])["txt_disimpan_ke"])

    def test_catatan_urutan_lampir_lalu_balasan_terakhir(self):
        kode, out, _ = self.jalan(CONTOH, "--html", os.path.join(self.dir, "a.html"),
                                  "--txt", os.path.join(self.dir, "a.txt"))
        catatan = [x for x in out.splitlines() if x.startswith("- Berkas dibuat")][0]
        self.assertLess(catatan.index("baris BERKAS (siap cetak) SEKALI"), catatan.index("bila gagal, lampirkan "
                                                                                        "berkas di baris BERKAS TEKS"))
        self.assertLess(catatan.index("BERKAS TEKS"), catatan.index("SESUDAH itu tulis balasan terakhir"))
        self.assertIn("jangan mengulang dengan opsi lain", catatan)
        self.assertIn("tanpa kata HTML, path, sistem, error", catatan)
        baris = out.splitlines()
        self.assertTrue(baris[-2].startswith("BERKAS: ") and baris[-1].startswith("BERKAS TEKS: "))

    def test_teks_pengguna_satu_baris_tanpa_escape_markdown(self):
        d = copy.deepcopy(CONTOH)
        d["pembeli"]["nama"] = "PT Maju_Jaya *Abadi*"
        d["catatan"] = "Baris satu\nbaris dua"
        f = os.path.join(self.dir, "x.txt")
        self.assertEqual(self.jalan(d, "--txt", f)[0], 0)
        teks = self.baca(f).decode("utf-8")
        self.assertIn("Kepada: PT Maju_Jaya *Abadi*", teks)
        self.assertIn("Catatan: Baris satu baris dua", teks)
        self.assertNotIn("\\", teks)

    def test_html_pph23_tanpa_escape_markdown(self):
        """Cacat lama (temuan pemeriksa 1.0.8): nama pembeli ber-_ atau * tampil 'PT Maju\\_Jaya' di HTML."""
        d = copy.deepcopy(UjiPPh23.DATA)
        d["pembeli"]["nama"] = "PT Maju_Jaya *Abadi* <b>"
        f = os.path.join(self.dir, "pph.html")
        kode, out, _ = self.jalan(d, "--html", f)
        self.assertEqual(kode, 0)
        with open(f, encoding="utf-8") as fh:
            isi = fh.read()
        self.assertIn("dipotong &amp; disetor oleh PT Maju_Jaya *Abadi* &lt;b&gt;, tidak mengurangi", isi)
        self.assertNotIn("\\", isi)
        self.assertNotIn("<b>,", isi)
        self.assertIn("oleh PT Maju\\_Jaya \\*Abadi\\* \\<b\\>, tidak", out)   # Markdown tetap di-escape

    def test_txt_sama_dengan_html_ditolak_tanpa_menulis(self):
        c = os.path.join(self.dir, "nomor-invoice.json")
        f = os.path.join(self.dir, "sama.txt")
        kode, out, err = self.jalan(CONTOH, "--html", f, "--txt", f, "--counter-file", c)
        self.assertEqual(kode, 2)
        self.assertIn("menunjuk berkas yang sama", err)
        self.assertFalse(os.path.exists(f))
        self.assertFalse(os.path.exists(c))   # file pencatat nomor juga tidak ditulis

    def test_txt_berakhiran_html_diganti_bukan_ditambah(self):
        kode, out, _ = self.jalan(self.data_g24(), "--nomor-terakhir", "INV/2026/10/0007",
                                  "--html", os.path.join(self.dir, "invoice-{nomor}.html"),
                                  "--txt", os.path.join(self.dir, "invoice-{nomor}.html"))
        self.assertEqual(kode, 0)
        self.assertEqual(os.path.basename(self.baris(out, "BERKAS: ")), "invoice-INV-2026-10-0008.html")
        self.assertEqual(os.path.basename(self.baris(out, "BERKAS TEKS: ")), "invoice-INV-2026-10-0008.txt")
        self.assertTrue(self.baca(self.baris(out, "BERKAS: ")).startswith(b"<!DOCTYPE html>"))   # HTML utuh
        kode, out, _ = self.jalan(CONTOH, "--txt", os.path.join(self.dir, "b.HTM"))
        self.assertTrue(self.baris(out, "BERKAS TEKS: ").endswith("b.txt"))

    def test_folder_baru_berakhiran_garis_miring_dibuat(self):
        baru = os.path.join(self.dir, "baru", "invoice") + os.sep
        kode, out, _ = self.jalan(self.data_g24(), "--nomor-terakhir", "INV/2026/10/0007", "--html", baru,
                                  "--txt", baru)
        self.assertEqual(kode, 0)
        self.assertEqual(self.baris(out, "BERKAS: "), os.path.join(os.path.abspath(baru),
                                                                   "invoice-INV-2026-10-0008.html"))
        self.assertEqual(self.baris(out, "BERKAS TEKS: "), os.path.join(os.path.abspath(baru),
                                                                        "invoice-INV-2026-10-0008.txt"))

    def test_folder_induk_tidak_ada_gagal_sebelum_menulis_html(self):
        html = os.path.join(self.dir, "ada.html")
        kode, out, err = self.jalan(CONTOH, "--html", html, "--txt", os.path.join(self.dir, "tidak-ada", "x.txt"))
        self.assertEqual(kode, 2)
        self.assertIn("tidak ada", err)
        self.assertFalse(os.path.exists(html))   # HTML tidak tertulis setengah jalan
        kode, out, err = self.jalan(CONTOH, "--html", os.path.join(self.dir, "tidak-ada", "x.html"))
        self.assertEqual(kode, 2)

    def test_kirim_file_jangan_jalankan_ulang_script(self):
        """Balasan 'kirim file': menjalankan ulang dengan --nomor-terakhir = nomor baru diam-diam menaikkan nomor
        (0009); yang benar memakai berkas yang sudah ada, atau nomor yang sama di kolom 'nomor' (revisi)."""
        c = os.path.join(self.dir, "nomor-invoice.json")
        argv = ("--counter-file", c, "--html", os.path.join(self.dir, "invoice-{nomor}.html"),
                "--txt", os.path.join(self.dir, "invoice-{nomor}.txt"))
        kode, out, _ = self.jalan(self.data_g24(), "--nomor-terakhir", "INV/2026/10/0007", *argv)
        self.assertIn("JANGAN jalankan script lagi", out)
        self.assertIn("**No.:** INV/2026/10/0008", self.jalan(self.data_g24(), "--nomor-terakhir",
                                                              "INV/2026/10/0007", *argv)[1])   # revisi, tetap 0008
        salah = self.jalan(self.data_g24(), "--nomor-terakhir", "INV/2026/10/0008", *argv)[1]
        self.assertIn("**No.:** INV/2026/10/0009", salah)                                       # bukti risiko
        d = self.data_g24()
        d["nomor"] = "INV/2026/10/0008"
        benar = self.jalan(d, *argv)[1]
        self.assertIn("**No.:** INV/2026/10/0008", benar)
        self.assertIn("dianggap revisi", benar)

    def test_catatan_lampiran_media_dan_lokasi_counter_terminal_saja(self):
        c = os.path.join(self.dir, "nomor-invoice.json")
        out = self.jalan(CONTOH, "--counter-file", c, "--txt", os.path.join(self.dir, "a.txt"))[1]
        self.assertIn("MEDIA:<path>), lampirkan HANYA berkas di baris BERKAS TEKS", out)
        self.assertIn("lokasi berikut hanya untuk terminal/IDE: " + os.path.abspath(c), out)
        self.assertIn("'nomor terakhir sudah dicatat'", out)
        dokumen = out.split("\n---\n")[0]
        self.assertNotIn(self.dir, dokumen)   # path tidak pernah masuk bagian dokumen untuk pembeli
        out = self.jalan(CONTOH, "--html", os.path.join(self.dir, "a.html"))[1]
        self.assertNotIn("MEDIA:", out)       # tanpa versi teks: tidak menyarankan baris MEDIA untuk HTML

    def test_versi_dan_aturan_balasan_di_skill(self):
        with open(os.path.join(AKAR, "CHANGELOG.md"), encoding="utf-8") as fh:
            self.assertIn("## Catatan revisi {} ".format(B.VERSI), fh.read())
        with open(os.path.join(AKAR, "SKILL.md"), encoding="utf-8") as fh:
            skill = fh.read()
        self.assertLess(len(skill.splitlines()), 300)
        self.assertIn("**Aturan balasan", skill)
        self.assertIn("balasan terakhir", skill)
        self.assertIn("BERKAS TEKS:", skill)
        for wajib in ("MEDIA:<path>", "jangan menjalankan script lagi", "<dokumen>", "**bila ada**",
                      "Versi teks <dokumen> saya lampirkan di pesan ini"):
            self.assertIn(wajib, skill)
        self.assertNotIn("dipersingkat", skill)


if __name__ == "__main__":
    unittest.main(verbosity=1)
