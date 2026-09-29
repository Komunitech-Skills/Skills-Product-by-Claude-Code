#!/usr/bin/env python3
"""Uji regresi laporan-klien-konsultan.

Mencakup: catat pekerjaan (normal, default status, jam koma, validasi status/jam/klien),
susun laporan (mingguan/bulanan/kustom, jam per proyek, dedup kendala/butuh_dari_klien,
rencana manual vs turunan, periode kosong, klien tidak ada), deteksi data sensitif (exit 3,
tidak memblokir output), dan keamanan CSV (formula injection).

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
SCRIPT = SINI / "scripts" / "laporan_klien.py"

sys.path.insert(0, str(SINI / "scripts"))
import laporan_klien as modul  # noqa: E402


def jalankan(*argv, cwd):
    r = subprocess.run([sys.executable, str(SCRIPT), *argv], cwd=cwd,
                        capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


class UjiCatat(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_catat_normal_membuat_file_dan_baris(self):
        code, out, err = jalankan("catat", "--klien", "PT Maju", "--proyek", "Pembukuan",
                                   "--pekerjaan", "Rekonsiliasi bank", "--jam", "2.5",
                                   "--status", "selesai", "--tanggal", "2026-09-22", "--json",
                                   cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertTrue(d["file_baru_dibuat"])
        self.assertEqual(d["dicatat"]["jam"], 2.5)
        self.assertEqual(d["dicatat"]["status"], "selesai")
        self.assertTrue((self.dir / "log-kerja-klien.csv").exists())

    def test_status_default_berjalan(self):
        code, out, err = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", "C",
                                   "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["dicatat"]["status"], "berjalan")

    def test_jam_koma_indonesia(self):
        code, out, _ = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", "C",
                                 "--jam", "1,5", "--json", cwd=self.dir)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["dicatat"]["jam"], 1.5)

    def test_status_alias_dikenali(self):
        code, out, _ = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", "C",
                                 "--status", "done", "--json", cwd=self.dir)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["dicatat"]["status"], "selesai")

    def test_status_tidak_valid_ditolak(self):
        code, out, err = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", "C",
                                   "--status", "ngasal", cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("tidak dikenali", err)

    def test_jam_bukan_angka_ditolak(self):
        code, _, err = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", "C",
                                 "--jam", "abc", cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("bukan angka", err)

    def test_jam_negatif_ditolak(self):
        code, _, err = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", "C",
                                 "--jam", "-1", cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("negatif", err)

    def test_jam_lebih_24_ditolak(self):
        code, _, err = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", "C",
                                 "--jam", "30", cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("24 jam", err)

    def test_klien_kosong_ditolak(self):
        code, _, err = jalankan("catat", "--klien", "  ", "--proyek", "B", "--pekerjaan", "C",
                                 cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("--klien wajib diisi", err)

    def test_pekerjaan_kosong_ditolak(self):
        code, _, err = jalankan("catat", "--klien", "A", "--proyek", "B", "--pekerjaan", " ",
                                 cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("--pekerjaan wajib diisi", err)

    def test_deteksi_data_sensitif_exit_3_tapi_tetap_tercatat(self):
        code, out, err = jalankan("catat", "--klien", "A", "--proyek", "B",
                                   "--pekerjaan", "Hubungi klien di 0812-3456-7890",
                                   cwd=self.dir)
        self.assertEqual(code, 3)
        self.assertIn("nomor HP/telepon", err)
        isi = (self.dir / "log-kerja-klien.csv").read_text(encoding="utf-8")
        self.assertIn("0812-3456-7890", isi)  # tetap tercatat, hanya diberi peringatan

    def test_formula_injection_dicegah(self):
        code, _, _ = jalankan("catat", "--klien", "A", "--proyek", "B",
                               "--pekerjaan", "=SUM(A1:A9)", cwd=self.dir)
        self.assertEqual(code, 0)
        with (self.dir / "log-kerja-klien.csv").open(newline="", encoding="utf-8") as f:
            baris = list(csv.DictReader(f))
        self.assertEqual(baris[0]["pekerjaan"], "'=SUM(A1:A9)")


class UjiLaporan(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.file = self.dir / "log.csv"
        with self.file.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(modul.KOLOM)
            w.writerow(["2026-09-22", "PT Maju", "Pembukuan", "Rekonsiliasi bank", "2.5",
                        "selesai", "", ""])
            w.writerow(["2026-09-23", "PT Maju", "Pembukuan", "Susun SPT PPN", "1.5",
                        "berjalan", "", "Faktur pajak masukan belum dikirim"])
            w.writerow(["2026-09-24", "PT Maju", "Konsultasi", "Diskusi PPh Badan", "",
                        "terkendala", "Menunggu laporan laba rugi Q3", ""])
            # duplikat kendala & butuh, harus di-dedup di laporan
            w.writerow(["2026-09-25", "PT Maju", "Konsultasi", "Follow up laba rugi", "1",
                        "terkendala", "Menunggu laporan laba rugi Q3", ""])
            w.writerow(["2026-08-10", "PT Maju", "Pembukuan", "Kerjaan bulan lalu", "3",
                        "selesai", "", ""])
            w.writerow(["2026-09-23", "CV Lain", "Website", "Desain landing page", "4",
                        "selesai", "", ""])

    def tearDown(self):
        self.tmp.cleanup()

    def test_laporan_minggu_kustom_hitung_benar(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--dari", "2026-09-21", "--sampai", "2026-09-27", "--json",
                                   cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["jumlah_entri"], 4)
        self.assertEqual(len(d["selesai"]), 1)
        self.assertEqual(len(d["berjalan"]), 1)
        self.assertEqual(len(d["terkendala"]), 2)
        self.assertAlmostEqual(d["total_jam"], 5.0)  # 2.5+1.5+1 (satu entri tanpa jam)
        self.assertEqual(d["entri_tanpa_jam"], 1)
        self.assertEqual(d["jam_per_proyek"]["Pembukuan"], 4.0)
        self.assertEqual(d["jam_per_proyek"]["Konsultasi"], 1.0)
        # dedup: kendala yang sama 2x hanya muncul sekali
        self.assertEqual(d["kendala"], ["Menunggu laporan laba rugi Q3"])
        self.assertEqual(d["butuh_dari_klien"], ["Faktur pajak masukan belum dikirim"])
        self.assertIn("PT Maju", d["teks_email"])
        self.assertIn("*Laporan Progres", d["teks_wa"])
        self.assertIn("# Laporan Progres", d["markdown"])

    def test_periode_minggu_ini_alias_mingguan(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--periode", "mingguan", "--tanggal-acuan", "2026-09-26",
                                   "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["periode"]["awal"], "2026-09-21")
        self.assertEqual(d["periode"]["akhir"], "2026-09-27")

    def test_periode_bulan_lalu(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--periode", "bulan-lalu", "--tanggal-acuan", "2026-09-26",
                                   "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["periode"]["awal"], "2026-08-01")
        self.assertEqual(d["periode"]["akhir"], "2026-08-31")
        self.assertEqual(d["jumlah_entri"], 1)

    def test_rencana_diturunkan_dari_berjalan_jika_tidak_diberi(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--dari", "2026-09-21", "--sampai", "2026-09-27", "--json",
                                   cwd=self.dir)
        d = json.loads(out)
        self.assertEqual(d["rencana_berikutnya"], ["Lanjutkan: Susun SPT PPN (Pembukuan)"])

    def test_rencana_manual_dipakai_bukan_turunan(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--dari", "2026-09-21", "--sampai", "2026-09-27",
                                   "--rencana", "Kirim draf SPT", "--rencana", "Follow up faktur",
                                   "--json", cwd=self.dir)
        d = json.loads(out)
        self.assertEqual(d["rencana_berikutnya"], ["Kirim draf SPT", "Follow up faktur"])

    def test_periode_kosong_tidak_mengarang_isi(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--dari", "2026-01-01", "--sampai", "2026-01-31", "--json",
                                   cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["jumlah_entri"], 0)
        self.assertEqual(d["selesai"], [])
        self.assertTrue(any("Tidak ada catatan pekerjaan" in c for c in d["catatan"]))

    def test_klien_tidak_ada_di_log(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "Tidak Ada PT",
                                   cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("Tidak ada catatan untuk klien", err)
        self.assertIn("PT Maju", err)  # menyebut klien yang memang tercatat

    def test_klien_lain_tidak_tercampur(self):
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "CV Lain",
                                   "--dari", "2026-09-21", "--sampai", "2026-09-27", "--json",
                                   cwd=self.dir)
        d = json.loads(out)
        self.assertEqual(d["jumlah_entri"], 1)
        self.assertEqual(d["selesai"], ["Desain landing page"])

    def test_deteksi_sensitif_di_laporan_exit_3(self):
        with self.file.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["2026-09-25", "PT Maju", "Legal", "Hubungi 0812-1111-2222",
                                     "1", "berjalan", "", ""])
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--dari", "2026-09-21", "--sampai", "2026-09-27", "--json",
                                   cwd=self.dir)
        self.assertEqual(code, 3)
        d = json.loads(out)
        self.assertTrue(any("nomor HP" in p for p in d["peringatan"]))
        self.assertIn("PT Maju", d["teks_email"])  # draf tetap dihasilkan, bukan diblokir

    def test_dari_tanpa_sampai_ditolak(self):
        code, _, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                 "--dari", "2026-09-01", cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("--dari dan --sampai", err)

    def test_file_tidak_ada(self):
        code, _, err = jalankan("--file", str(self.dir / "tidak-ada.csv"), "laporan",
                                 "--klien", "PT Maju", cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("tidak ditemukan", err)

    def test_file_0_byte_ditolak_dengan_pesan_jelas(self):
        kosong = self.dir / "kosong-0-byte.csv"
        kosong.write_bytes(b"")
        code, _, err = jalankan("--file", str(kosong), "laporan", "--klien", "PT Maju", cwd=self.dir)
        self.assertEqual(code, 1)
        self.assertIn("0 byte", err)
        self.assertIn("init", err)


class UjiFungsiInternal(unittest.TestCase):
    def test_rentang_minggu_ini_senin_minggu(self):
        label, a, b = modul.rentang_periode("minggu-ini", date(2026, 9, 26))  # Sabtu
        self.assertEqual((a, b), (date(2026, 9, 21), date(2026, 9, 27)))

    def test_rentang_bulan_ini_kabisat(self):
        label, a, b = modul.rentang_periode("bulan-ini", date(2028, 2, 15))
        self.assertEqual((a, b), (date(2028, 2, 1), date(2028, 2, 29)))

    def test_format_jam_bulat_dan_desimal(self):
        self.assertEqual(modul.format_jam(2.0), "2 jam")
        self.assertEqual(modul.format_jam(2.5), "2,5 jam")
        self.assertEqual(modul.format_jam(None), "-")

    def test_deteksi_sensitif_tidak_salah_kena_kata_biasa(self):
        temuan = []
        modul.deteksi_sensitif("Desain unik untuk klinik gigi", "kolom", temuan)
        self.assertEqual(temuan, [])



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import os
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "laporan_klien.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["init", "--pak"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60, cwd=t)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "log-kerja-klien.csv")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main()
