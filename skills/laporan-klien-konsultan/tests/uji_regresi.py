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
        self.assertIn("tidak dikenali", err)

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

    def test_rencana_tanpa_data_jadi_isian_bukan_ulang_judul(self):
        # 1.0.5: tidak lagi "Lanjutkan: <judul>" (mekanis); wajib isian [isi: ...] + catatan
        code, out, err = jalankan("--file", str(self.file), "laporan", "--klien", "PT Maju",
                                   "--dari", "2026-09-21", "--sampai", "2026-09-27", "--json",
                                   cwd=self.dir)
        d = json.loads(out)
        self.assertEqual(len(d["rencana_berikutnya"]), 3)  # 1 berjalan + 2 terkendala
        self.assertTrue(all(r.startswith("[isi: ") for r in d["rencana_berikutnya"]))
        self.assertFalse(any("Lanjutkan" in r for r in d["rencana_berikutnya"]))
        self.assertEqual(d["rencana_perlu_diisi"], 3)
        self.assertTrue(any("isian [isi: ...]" in c for c in d["catatan"]))

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


DATA = SINI / "tests" / "data"


class UjiRevisi105(unittest.TestCase):
    """Regresi temuan uji OpenClaw 2026-10-01 (solusi-vip/konsultan, skenario 04)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def lapor(self, path, klien="PT Sentosa Makmur", *extra):
        code, out, err = jalankan("--file", str(path), "laporan", "--klien", klien,
                                   "--dari", "2026-09-22", "--sampai", "2026-09-26",
                                   *extra, "--json", cwd=self.dir)
        return code, (json.loads(out) if out.strip() else None), err

    # --- file contoh skenario 04 (CSV milik member, format awam) ---
    def test_file_member_skenario_04_terbaca_dan_total_persis(self):
        code, d, err = self.lapor(DATA / "catatan-kerja.csv")
        self.assertEqual(code, 0, err)
        self.assertEqual(d["jumlah_entri"], 5)  # 19 & 29 Sep + CV Lancar Abadi dikecualikan
        self.assertEqual(len(d["selesai"]), 2)
        self.assertEqual(len(d["berjalan"]), 3)
        self.assertEqual(d["total_jam"], 9.75)
        self.assertEqual(d["total_jam_teks"], "9,75 jam (9 jam 45 menit)")
        jam_item = [r["jam"] for r in d["rincian"]]
        self.assertEqual(sorted(jam_item), [1.0, 1.5, 1.5, 2.5, 3.25])  # "90 menit" -> 1,5
        self.assertEqual(round(sum(jam_item), 2), d["total_jam"])
        self.assertIn("3,25 jam", d["teks_wa"])
        self.assertNotIn("3,2 jam", d["teks_wa"])
        self.assertNotIn("9,8 jam", d["teks_wa"])
        self.assertEqual(d["butuh_dari_klien"], ["nunggu data stok opname dari klien"])
        self.assertIn("klien minta tambah alur retur", d["teks_wa"])  # keterangan ikut tampil

    def test_total_sama_dengan_jumlah_item_yang_tampil(self):
        import re as _re
        code, d, err = self.lapor(DATA / "catatan-kerja.csv")
        tampil = _re.findall(r"\((\d+(?:,\d+)?) jam\)", d["teks_wa"])
        jumlah = sum(float(x.replace(",", ".")) for x in tampil)
        self.assertAlmostEqual(jumlah, d["total_jam"], places=9)
        self.assertIn(f"Total jam tercatat: {d['total_jam_teks']}", d["teks_wa"])

    def test_tidak_ada_kata_periode_ganda(self):
        code, d, err = self.lapor(DATA / "catatan-kerja.csv")
        for teks in (d["teks_email"], d["teks_wa"], d["markdown"], d["ringkasan"]):
            self.assertNotRegex(teks.lower(), r"periode\s+periode")
            self.assertNotIn("kustom", teks.lower())

    def test_rencana_dari_kolom_file_member(self):
        f = self.dir / "dengan-rencana.csv"
        f.write_text("Tanggal,Klien,Kegiatan,Durasi,Status,Rencana\n"
                     "22/09/2026,PT A,Draft SOP,2 jam,berjalan,Kirim draf SOP ke klien Senin 29/9\n"
                     "23/09/2026,PT A,Audit stok,1 jam,berjalan,\n", encoding="utf-8")
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 0, err)
        self.assertEqual(d["rencana_berikutnya"][0], "Kirim draf SOP ke klien Senin 29/9")
        self.assertEqual(d["rencana_berikutnya"][1],
                         '[isi: langkah berikutnya untuk "Audit stok" + target tanggal]')

    # --- pembacaan toleran ---
    def test_titik_koma_desimal_koma_cp1252(self):
        f = self.dir / "excel-indo.csv"
        f.write_bytes("Tgl;Client;Aktivitas;Jam;Status;Catatan\n"
                      "22-09-2026;PT A;Rapat café;2,5;Selesai;\n"
                      "23 Sep 2026;PT A;Laporan;1:15;on progress;\n".encode("cp1252"))
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 0, err)
        self.assertEqual(d["total_jam"], 3.75)
        self.assertIn("café", d["teks_wa"])
        self.assertTrue(any("Windows-1252" in c for c in d["catatan"]))

    def test_bom_utf8_dan_header_inggris(self):
        f = self.dir / "en.csv"
        f.write_bytes("\ufeffDate,Client,Project,Task,Hours,Status,Notes\n"
                      "2026-09-22,PT A,Web,Landing page,\"1,25\",done,\n".encode("utf-8"))
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 0, err)
        self.assertEqual(d["total_jam"], 1.25)
        self.assertEqual(d["selesai"], ["Landing page"])

    def test_utf16_tab_dari_excel(self):
        f = self.dir / "u16.csv"
        f.write_bytes("Tanggal\tKlien\tPekerjaan\tDurasi\n22/09/2026\tPT A\tRapat\t45 menit\n"
                      .encode("utf-16"))
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 0, err)
        self.assertEqual(d["total_jam"], 0.75)

    def test_tanpa_kolom_klien_dianggap_satu_klien_dengan_catatan(self):
        f = self.dir / "satu-klien.csv"
        f.write_text("Tanggal,Pekerjaan,Durasi\n22/09/2026,Rapat,1 jam 30 menit\n", encoding="utf-8")
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 0, err)
        self.assertEqual(d["total_jam"], 1.5)
        self.assertTrue(any("tidak punya kolom Klien" in c for c in d["catatan"]))

    def test_koma_desimal_tanpa_kutip_pesan_jelas(self):
        f = self.dir / "rusak.csv"
        f.write_text("Tanggal,Klien,Kerjaan,Durasi\n22/09/2026,PT A,Rapat,2,5 jam\n", encoding="utf-8")
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 1)
        self.assertIn("Baris 2", err)
        self.assertIn("tanda kutip", err)

    def test_kolom_wajib_tidak_ada_pesan_jelas(self):
        f = self.dir / "aneh.csv"
        f.write_text("Kolom1,Kolom2\nx,y\n", encoding="utf-8")
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 1)
        self.assertIn("tidak punya kolom wajib", err)
        self.assertIn("Header yang terbaca", err)

    def test_durasi_tidak_dikenali_sebut_baris(self):
        f = self.dir / "durasi.csv"
        f.write_text("Tanggal,Klien,Kerjaan,Durasi\n22/09/2026,PT A,Rapat,sebentar\n", encoding="utf-8")
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 1)
        self.assertIn("Baris 2", err)
        self.assertIn("90 menit", err)

    def test_log_lama_skema_skill_tetap_terbaca(self):
        f = self.dir / "log-kerja-klien.csv"
        jalankan("--file", str(f), "catat", "--klien", "PT A", "--proyek", "P", "--pekerjaan",
                 "Kerja", "--jam", "3,25", "--tanggal", "2026-09-22", cwd=self.dir)
        code, d, err = self.lapor(f, "PT A")
        self.assertEqual(code, 0, err)
        self.assertEqual(d["total_jam"], 3.25)


class UjiFungsiInternal(unittest.TestCase):
    def test_parse_jam_format_awam(self):
        kasus = {"2": 2.0, "2,5": 2.5, "2.5": 2.5, "2,5 jam": 2.5, "90 menit": 1.5,
                 "1 jam 30 menit": 1.5, "1:30": 1.5, "2h": 2.0, "45m": 0.75, "100 menit": 1.67,
                 "3,25 jam": 3.25, "2 Jam": 2.0, "": None}
        for teks, harap in kasus.items():
            self.assertEqual(modul.parse_jam(teks), harap, teks)

    def test_format_jam_dua_desimal_tanpa_pembulatan_ulang(self):
        self.assertEqual(modul.format_jam(3.25), "3,25 jam")
        self.assertEqual(modul.format_jam(9.75), "9,75 jam")
        self.assertEqual(modul.format_jam(1.67), "1,67 jam")
        self.assertEqual(modul.format_jam_menit(9.75), "9,75 jam (9 jam 45 menit)")
        self.assertEqual(modul.format_jam_menit(0.5), "0,5 jam (30 menit)")
        self.assertEqual(modul.format_jam_menit(1.67), "1,67 jam")

    def test_jumlah_jam_persis(self):
        self.assertEqual(modul.jumlah_jam([1.67, 1.67, 1.67]), 5.01)
        self.assertEqual(modul.jumlah_jam([0.1, 0.2]), 0.3)

    def test_tanggal_format_indonesia(self):
        self.assertEqual(modul.baca_tanggal("22/09/2026"), date(2026, 9, 22))
        self.assertEqual(modul.baca_tanggal("22 Sep 2026"), date(2026, 9, 22))
        self.assertEqual(modul.baca_tanggal("22 Agustus 2026"), date(2026, 8, 22))
        self.assertEqual(modul.baca_tanggal("2026-09-22 00:00:00"), date(2026, 9, 22))

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
