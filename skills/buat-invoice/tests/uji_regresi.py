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
        self.assertIn("Lampirkan berkas ini ke chat untuk setiap dokumen (invoice maupun kuitansi)", out)
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


if __name__ == "__main__":
    unittest.main(verbosity=1)
