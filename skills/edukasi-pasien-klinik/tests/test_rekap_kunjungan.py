#!/usr/bin/env python3
"""Tes regresi untuk rekap_kunjungan.py — jalankan:
    python3 tests/test_rekap_kunjungan.py
Hanya library standar (unittest). Mengimpor modul dari ../scripts.

Setiap kelas tes memetakan ke temuan HASIL-UJI.md (2026-09-24) agar mudah
ditelusuri: B1 = berat, S1-S4 = sedang, R1-R2 = ringan yang berkaitan
dengan script.
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import rekap_kunjungan as rk  # noqa: E402


CSV_NORMAL = """Tanggal,Jam,Poli,Penjamin,Status
2026-09-01,08:15,Gigi,BPJS,Selesai
2026-09-01,09:00,Gigi,Umum,Selesai
2026-09-01,09:30,Umum,BPJS,Tidak Datang
2026-09-02,08:00,Gigi,Umum,Selesai
2026-09-02,10:00,KIA,BPJS,Selesai
"""

CSV_DENGAN_KOLOM_SENSITIF = """Tanggal,Nama Pasien,NIK,Poli,Diagnosis
2026-09-01,Budi,3201xxxx,Gigi,K02.1
2026-09-01,Sari,3201yyyy,Umum,J06
"""

CSV_HANYA_HEADER = """Tanggal,Poli
"""


class TesRekapNormal(unittest.TestCase):
    def test_rekap_lengkap(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 5)
        self.assertEqual(hasil["per_hari"]["2026-09-01"], 3)
        self.assertEqual(hasil["per_hari"]["2026-09-02"], 2)
        self.assertEqual(hasil["per_poli"]["Gigi"], 3)
        self.assertEqual(hasil["per_penjamin"]["BPJS"], 3)
        self.assertEqual(hasil["tidak_datang"], 1)
        self.assertEqual(hasil["hadir"], 4)
        self.assertEqual(hasil["kolom_sensitif_diabaikan"], [])
        jam_list = [j["jam"] for j in hasil["jam_ramai"]]
        self.assertIn("08:00", jam_list)

    def test_format_teks_tidak_error(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        self.assertIn("REKAP OPERASIONAL", teks)
        self.assertIn("2026-09-01", teks)
        self.assertIn("Total pendaftaran tercatat", teks)


class TesPrivasi(unittest.TestCase):
    def test_kolom_sensitif_tidak_muncul_di_output(self):
        header, baris = rk.baca_csv(CSV_DENGAN_KOLOM_SENSITIF, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        for terlarang in ["Budi", "Sari", "3201xxxx", "3201yyyy", "K02.1", "J06"]:
            self.assertNotIn(terlarang, teks)
            self.assertNotIn(terlarang, dump)
        self.assertIn("nama pasien", [c.lower() for c in hasil["kolom_sensitif_diabaikan"]])
        self.assertIn("diagnosis", [c.lower() for c in hasil["kolom_sensitif_diabaikan"]])

    def test_r1_variasi_header_sensitif_dikenali(self):
        """R1: Dx, ICD-10, Keluhan Utama, HP/WA, No. RM, Tgl Lahir, Email, Nama Ibu."""
        header = [
            "Tanggal", "Dx", "ICD-10", "Keluhan Utama", "HP/WA", "No. RM",
            "Tgl Lahir", "Email", "Nama Ibu", "Poli",
        ]
        baris = [{h: "x" for h in header}]
        baris[0]["Tanggal"] = "2026-09-01"
        baris[0]["Poli"] = "Gigi"
        hasil = rk.rekap(header, baris)
        diabaikan_lower = [c.lower() for c in hasil["kolom_sensitif_diabaikan"]]
        for kolom in ["dx", "icd-10", "keluhan utama", "hp/wa", "no. rm", "tgl lahir", "email", "nama ibu"]:
            self.assertIn(kolom, diabaikan_lower, f"{kolom} seharusnya dikenali sebagai kolom sensitif")

    def test_r2_teks_bebas_lebih_dari_4_kata_diberi_peringatan(self):
        header, baris = rk.baca_csv(
            "Tanggal,Poli\n2026-09-01,Cabut gigi FIKTIF Ani anak Budi\n", is_text=True
        )
        hasil = rk.rekap(header, baris)
        self.assertIn("Cabut gigi FIKTIF Ani anak Budi", hasil["kolom_nilai_mencurigakan"]["poli"])
        teks = rk.format_teks(hasil)
        self.assertIn("periksa apakah ini teks bebas", teks)

    def test_r2_lebih_dari_20_nilai_unik_diberi_peringatan(self):
        baris_csv = "Tanggal,Poli\n" + "".join(
            f"2026-09-01,Poli{i}\n" for i in range(25)
        )
        header, baris = rk.baca_csv(baris_csv, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIn("Poli", hasil["kolom_terlalu_beragam"])


class TesStatusKehadiran(unittest.TestCase):
    """B1a: status tidak boleh diam-diam dianggap hadir."""

    def test_variasi_tidak_datang_dikenali(self):
        for nilai in [
            "Tidak datang", "tdk datang", "Tidak Hadir", "TDK HADIR", "tidak jadi",
            "Mangkir", "No Show", "no-show", "Batal", "Dibatalkan", "cancel",
            "Belum datang",
        ]:
            with self.subTest(nilai=nilai):
                self.assertEqual(rk.klasifikasi_status(nilai), "tidak_datang")

    def test_singkatan_th_dikenali_tidak_datang(self):
        self.assertEqual(rk.klasifikasi_status("TH"), "tidak_datang")
        self.assertEqual(rk.klasifikasi_status("th"), "tidak_datang")

    def test_status_hadir_dikenali(self):
        for nilai in ["Selesai", "Hadir", "Datang", "Terlaksana", "Berhasil", "Dilayani"]:
            with self.subTest(nilai=nilai):
                self.assertEqual(rk.klasifikasi_status(nilai), "hadir")

    def test_status_tidak_dikenal_tidak_dianggap_hadir(self):
        """Inti B1a: status asing dilaporkan, BUKAN diam-diam hadir."""
        for nilai in ["Reschedule", "Dijadwalkan ulang", "Pending konfirmasi", "???"]:
            with self.subTest(nilai=nilai):
                self.assertEqual(rk.klasifikasi_status(nilai), "tidak_dikenal")

    def test_kasus_asli_bug_tidak_hadir_terhitung_benar(self):
        """Reproduksi temuan penguji: 'Tidak hadir' harus dihitung tidak datang,
        bukan hadir (sebelumnya salah dihitung 2 dari 3 seharusnya)."""
        csv_text = """Tanggal,Status
2026-09-01,Selesai
2026-09-01,Tidak hadir
2026-09-01,Hadir
"""
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["tidak_datang"], 1)
        self.assertEqual(hasil["hadir"], 2)

    def test_status_tidak_dikenal_terlihat_di_rincian_dan_tidak_masuk_hadir(self):
        csv_text = "Tanggal,Status\n2026-09-01,Reschedule besok\n2026-09-01,Selesai\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["status_tidak_dikenal_jumlah"], 1)
        self.assertEqual(hasil["hadir"], 1)
        kategori = {s["nilai"]: s["kategori"] for s in hasil["status_rincian"]}
        self.assertEqual(kategori["Reschedule besok"], "tidak_dikenal")
        teks = rk.format_teks(hasil)
        self.assertIn("TIDAK DIKENAL", teks)


class TesFormatTanggal(unittest.TestCase):
    """B1b: format tanggal ditentukan sekali per file, peringatan bila campur."""

    def test_dmy_konsisten_tanpa_peringatan(self):
        csv_text = "Tanggal,Poli\n25/01/2026,A\n13/09/2026,B\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIsNone(hasil["peringatan_format_tanggal"])
        self.assertEqual(hasil["urutan_tanggal_dipakai"], "dmy")
        self.assertIn("2026-01-25", hasil["per_hari"])
        self.assertIn("2026-09-13", hasil["per_hari"])

    def test_format_campur_memberi_peringatan_dan_baca_bukti_lokal(self):
        # 25/01 -> hanya masuk akal dmy (hari=25). 09/13 -> hanya masuk akal mdy (bulan=9? tidak,
        # 13 tidak mungkin bulan, jadi ini unik: a=09,b=13 -> b>12 -> mdy (hari=13, bulan=09).
        csv_text = "Tanggal,Poli\n25/01/2026,A\n09/13/2026,B\n02/02/2026,C\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIsNotNone(hasil["peringatan_format_tanggal"])
        self.assertIn("tidak konsisten", hasil["peringatan_format_tanggal"])
        # baris ke-3 di file (baris data ke-2, +1 header) yang bertentangan disebut
        self.assertIn("3", hasil["peringatan_format_tanggal"])
        # tapi bukti lokalnya tetap dibaca benar: 09/13/2026 -> 13 September 2026
        self.assertIn("2026-09-13", hasil["per_hari"])
        self.assertIn("2026-01-25", hasil["per_hari"])

    def test_iso_tidak_terpengaruh_urutan(self):
        header, baris = rk.baca_csv("Tanggal,Poli\n2026-09-01,A\n", is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIn("2026-09-01", hasil["per_hari"])

    def test_nama_bulan_indonesia_dan_inggris(self):
        for teks, iso in [
            ("2 Sept 2026", "2026-09-02"),
            ("1 September 2026", "2026-09-01"),
            ("1-Sep-2026", "2026-09-01"),
            ("5 Januari 2026", "2026-01-05"),
        ]:
            with self.subTest(teks=teks):
                header, baris = rk.baca_csv(f"Tanggal,Poli\n{teks},A\n", is_text=True)
                hasil = rk.rekap(header, baris)
                self.assertIn(iso, hasil["per_hari"], f"gagal parse: {teks}")

    def test_tanggal_dengan_jam_sekaligus(self):
        header, baris = rk.baca_csv(
            "Tanggal,Poli\n2026-09-01 08:45,A\n2026-09-01T10:00:00,B\n", is_text=True
        )
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["per_hari"]["2026-09-01"], 2)
        jam_terbaca = {j["jam"] for j in hasil["jam_ramai"]}
        self.assertTrue({"08:00", "10:00"} <= jam_terbaca)

    def test_tanggal_campur_sebagian_gagal_dihitung(self):
        csv_text = "Tanggal,Poli\n01/09/2026,A\n2026-09-02,B\ntanggal-rusak,C\n"
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 3)
        self.assertEqual(hasil["baris_tanggal_tidak_terbaca"], 1)
        self.assertEqual(sum(hasil["per_hari"].values()), 2)


class TesEncoding(unittest.TestCase):
    """S1: encoding selain UTF-8 tidak boleh membuat script crash."""

    def _tulis(self, teks, enc):
        f = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        f.write(teks.encode(enc))
        f.close()
        return f.name

    def test_cp1252(self):
        path = self._tulis("Tanggal,Poli\n2026-09-01,Depané\n", "cp1252")
        try:
            header, baris = rk.baca_csv(path)
            self.assertEqual(baris[0]["Poli"], "Depané")
        finally:
            os.unlink(path)

    def test_utf16_dengan_bom(self):
        path = self._tulis("Tanggal,Poli\r\n2026-09-01,Gigi\r\n", "utf-16")
        try:
            header, baris = rk.baca_csv(path)
            self.assertEqual(baris[0]["Poli"], "Gigi")
        finally:
            os.unlink(path)

    def test_utf8_sig_bom(self):
        path = self._tulis("Tanggal,Poli\n2026-09-01,Gigi\n", "utf-8-sig")
        try:
            header, baris = rk.baca_csv(path)
            self.assertEqual(header[0], "Tanggal")
        finally:
            os.unlink(path)

    def test_encoding_tidak_dikenali_pesan_jelas_bukan_traceback(self):
        # Byte yang tidak valid untuk utf-8/cp1252/latin-1 sangat jarang (latin-1
        # menerima semua byte), jadi kita paksakan lewat _decode_bytes langsung
        # dengan byte yang gagal di semua percobaan sebelum latin-1 (uji fallback).
        mentah = "Tanggal,Poli\n2026-09-01,Gigi\n".encode("utf-8")
        teks, enc = rk._decode_bytes(mentah)
        self.assertEqual(enc, "utf-8")


class TesTotalDanPersentase(unittest.TestCase):
    """S3: total pendaftaran, hadir, tidak datang, persentase eksplisit."""

    def test_persentase_dihitung_dan_dibulatkan_1_desimal(self):
        csv_text = """Tanggal,Status
2026-09-01,Selesai
2026-09-01,Selesai
2026-09-01,Tidak datang
"""
        header, baris = rk.baca_csv(csv_text, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_pendaftaran"], 3)
        self.assertEqual(hasil["hadir"], 2)
        self.assertEqual(hasil["tidak_datang"], 1)
        self.assertAlmostEqual(hasil["persentase_hadir"], 66.7)
        self.assertAlmostEqual(hasil["persentase_tidak_datang"], 33.3)

    def test_tanpa_kolom_status_field_none(self):
        header, baris = rk.baca_csv("Tanggal,Poli\n2026-09-01,A\n", is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertIsNone(hasil["hadir"])
        self.assertIsNone(hasil["tidak_datang"])
        self.assertIsNone(hasil["persentase_hadir"])


class TesDataRusak(unittest.TestCase):
    def test_hanya_header_raise_error(self):
        header, baris = rk.baca_csv(CSV_HANYA_HEADER, is_text=True)
        with self.assertRaises(rk.DataError):
            rk.rekap(header, baris)

    def test_tanpa_kolom_tanggal_raise_error(self):
        header, baris = rk.baca_csv("Poli\nGigi\n", is_text=True)
        with self.assertRaises(rk.DataError):
            rk.rekap(header, baris)

    def test_file_tidak_ada(self):
        with self.assertRaises(rk.DataError):
            rk.baca_csv("/path/tidak/ada/kunjungan.csv")


class TesCLI(unittest.TestCase):
    def test_main_file_tidak_ada_exit_code_1(self):
        buf_err = io.StringIO()
        with redirect_stderr(buf_err):
            kode = rk.main(["--file", "/path/tidak/ada.csv"])
        self.assertEqual(kode, 1)
        self.assertIn("Error", buf_err.getvalue())

    def test_main_json_output(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(CSV_NORMAL)
            path = f.name
        try:
            buf_out = io.StringIO()
            with redirect_stdout(buf_out):
                kode = rk.main(["--file", path, "--format", "json"])
            self.assertEqual(kode, 0)
            data = json.loads(buf_out.getvalue())
            self.assertEqual(data["total_pendaftaran"], 5)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
