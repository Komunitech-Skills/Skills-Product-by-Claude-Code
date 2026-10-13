#!/usr/bin/env python3
"""Tes rilis_batch.py pada salinan sementara (catalog + folder skill tiruan). Tidak menyentuh repo nyata.

Jalankan: python3 scripts/test_rilis_batch.py   (atau: python3 -m unittest discover -s scripts)
"""
import contextlib
import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rilis_batch  # noqa: E402

KOLOM = ["nama", "kategori", "jalur", "sumber_url", "lisensi", "skor_kualitas", "tier_usulan",
         "harga_usulan_idr", "tier_final", "harga_final_idr", "versi", "platform_teruji",
         "status", "tanggal_update"]


def baris(nama, status, versi="1.0.0"):
    return {"nama": nama, "kategori": "Uji", "jalur": "orisinal", "sumber_url": "", "lisensi": "",
            "skor_kualitas": "8", "tier_usulan": "ecer", "harga_usulan_idr": "99000",
            "tier_final": "ecer", "harga_final_idr": "99000", "versi": versi,
            # koma + tanda kutip supaya penulisan ulang CSV ikut diuji
            "platform_teruji": 'openclaw (uji "otomatis", agent)', "status": status,
            "tanggal_update": "2026-10-01"}


VALIDATE_LOLOS = "import sys\nprint('✅ validate tiruan lolos')\nsys.exit(0)\n"
VALIDATE_GAGAL = "import sys\nprint('❌ validate tiruan gagal')\nsys.exit(1)\n"


class TesRilisBatch(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.rows = [baris("skill-a", "beta", "1.2.3"), baris("skill-b", "beta"),
                     baris("skill-c", "beta"), baris("skill-d", "lulus"), baris("skill-e", "rilis")]
        for r in self.rows:
            contoh = self.root / "skills" / r["nama"] / "examples"
            contoh.mkdir(parents=True)
            (contoh / "01-uji.md").write_text("contoh", encoding="utf-8")
            (self.root / "skills" / r["nama"] / "SKILL.md").write_text("x", encoding="utf-8")
        self.tulis_katalog(self.rows)
        (self.root / "koordinasi").mkdir()
        (self.root / "scripts").mkdir()
        self.set_validate(VALIDATE_LOLOS)

    # -- bantu
    def tulis_katalog(self, rows):
        with (self.root / "catalog.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=KOLOM, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)

    def set_validate(self, isi):
        (self.root / "scripts" / "validate.py").write_text(isi, encoding="utf-8")

    def jalankan(self, *argumen):
        keluar, galat = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(keluar), contextlib.redirect_stderr(galat):
            kode = rilis_batch.main(["--root", str(self.root), *argumen])
        return kode, keluar.getvalue() + galat.getvalue()

    def katalog(self):
        with (self.root / "catalog.csv").open(newline="", encoding="utf-8") as f:
            return {r["nama"]: r for r in csv.DictReader(f)}

    def masukan(self, nama):
        return self.root / "skills" / nama / "examples" / "MASUKAN-BETA.md"

    def cadangan(self):
        return list(self.root.glob("catalog.csv.bak-*"))

    # -- tes
    def test_dry_run_tidak_menulis(self):
        sebelum = (self.root / "catalog.csv").read_bytes()
        kode, out = self.jalankan()
        self.assertEqual(kode, 0)
        self.assertEqual((self.root / "catalog.csv").read_bytes(), sebelum)
        self.assertFalse(self.masukan("skill-a").exists())
        self.assertEqual(self.cadangan(), [])
        self.assertIn("Skill beta di katalog : 3", out)
        self.assertIn("Akan naik ke rilis    : 3", out)
        self.assertIn("DRY-RUN", out)
        for n in ("skill-a", "skill-b", "skill-c"):
            self.assertIn(f"  - {n}", out)
        self.assertNotIn("skill-d", out)  # status lulus tidak disentuh

    def test_terapkan_mengubah_status_dan_tanggal(self):
        kode, out = self.jalankan("--terapkan", "--tanggal", "2026-10-20")
        self.assertEqual(kode, 0, out)
        kat = self.katalog()
        for n in ("skill-a", "skill-b", "skill-c"):
            self.assertEqual(kat[n]["status"], "rilis")
            self.assertEqual(kat[n]["tanggal_update"], "2026-10-20")
        # yang bukan beta tidak berubah, kolom lain utuh
        self.assertEqual(kat["skill-d"]["status"], "lulus")
        self.assertEqual(kat["skill-d"]["tanggal_update"], "2026-10-01")
        self.assertEqual(kat["skill-e"]["tanggal_update"], "2026-10-01")
        self.assertEqual(kat["skill-a"]["platform_teruji"], 'openclaw (uji "otomatis", agent)')
        self.assertEqual(kat["skill-a"]["versi"], "1.2.3")
        # format file: LF, tanpa CRLF, baris yang tidak berubah identik
        mentah = (self.root / "catalog.csv").read_bytes()
        self.assertNotIn(b"\r", mentah)
        self.assertTrue(mentah.endswith(b"\n"))
        self.assertEqual(len(self.cadangan()), 1)

    def test_daftar_tunda_dihormati(self):
        (self.root / "koordinasi" / "beta-tunda.txt").write_text(
            "# skill yang ditahan\nskill-b  # ada keluhan tester\n\nskill-tidak-ada\nskill-d\n",
            encoding="utf-8")
        kode, out = self.jalankan("--terapkan", "--tanggal", "2026-10-20")
        self.assertEqual(kode, 0, out)
        kat = self.katalog()
        self.assertEqual(kat["skill-b"]["status"], "beta")
        self.assertEqual(kat["skill-b"]["tanggal_update"], "2026-10-01")
        self.assertFalse(self.masukan("skill-b").exists())
        self.assertEqual(kat["skill-a"]["status"], "rilis")
        self.assertEqual(kat["skill-c"]["status"], "rilis")
        self.assertIn("Dilewati (daftar tunda): 1", out)
        self.assertIn("'skill-tidak-ada' tidak ada di catalog.csv", out)
        self.assertIn("'skill-d' bukan berstatus beta", out)

    def test_masukan_beta_dibuat_sekali_dan_tidak_ditimpa(self):
        ada = self.masukan("skill-a")
        ada.write_text("masukan asli tester", encoding="utf-8")
        kode, out = self.jalankan("--terapkan", "--tanggal", "2026-10-20")
        self.assertEqual(kode, 0, out)
        self.assertEqual(ada.read_text(encoding="utf-8"), "masukan asli tester")
        baru = self.masukan("skill-b").read_text(encoding="utf-8")
        self.assertIn("# Masukan beta — skill-b", baru)
        self.assertIn("13–19 Oktober 2026", baru)
        self.assertIn("tidak ada masukan negatif yang diterima sampai 20 Oktober 2026", baru)
        self.assertIn("status rilis (keputusan kurator 62)", baru)
        # jalankan lagi: tidak ada beta tersisa, berkas yang sudah dibuat tidak berubah
        isi_b = self.masukan("skill-b").read_text(encoding="utf-8")
        kode, out = self.jalankan("--terapkan", "--tanggal", "2026-10-21")
        self.assertEqual(kode, 0, out)
        self.assertIn("Tidak ada skill yang perlu dinaikkan", out)
        self.assertEqual(self.masukan("skill-b").read_text(encoding="utf-8"), isi_b)
        self.assertEqual(self.katalog()["skill-b"]["tanggal_update"], "2026-10-20")

    def test_hanya_membatasi(self):
        kode, out = self.jalankan("--terapkan", "--tanggal", "2026-10-20", "--hanya", "skill-c")
        self.assertEqual(kode, 0, out)
        kat = self.katalog()
        self.assertEqual(kat["skill-c"]["status"], "rilis")
        self.assertEqual(kat["skill-a"]["status"], "beta")
        self.assertEqual(kat["skill-b"]["status"], "beta")
        self.assertTrue(self.masukan("skill-c").exists())
        self.assertFalse(self.masukan("skill-a").exists())

    def test_hanya_nama_tidak_dikenal_ditolak(self):
        sebelum = (self.root / "catalog.csv").read_bytes()
        kode, out = self.jalankan("--terapkan", "--hanya", "skill-typo")
        self.assertEqual(kode, 2)
        self.assertIn("skill-typo", out)
        self.assertEqual((self.root / "catalog.csv").read_bytes(), sebelum)

    def test_cek_tidak_menulis_dan_mendeteksi_masalah(self):
        sebelum = (self.root / "catalog.csv").read_bytes()
        kode, out = self.jalankan("--cek")
        self.assertEqual(kode, 0, out)
        self.assertIn("Cek: OK", out)
        # buat masalah: examples skill-b dikosongkan
        (self.root / "skills" / "skill-b" / "examples" / "01-uji.md").unlink()
        kode, out = self.jalankan("--cek")
        self.assertEqual(kode, 1)
        self.assertIn("skill-b: examples/ kosong", out)
        self.assertEqual((self.root / "catalog.csv").read_bytes(), sebelum)
        self.assertEqual(self.cadangan(), [])
        self.assertFalse(self.masukan("skill-a").exists())

    def test_validate_gagal_membatalkan(self):
        self.set_validate(VALIDATE_GAGAL)
        sebelum = (self.root / "catalog.csv").read_bytes()
        kode, out = self.jalankan("--terapkan", "--tanggal", "2026-10-20")
        self.assertEqual(kode, 1)
        self.assertIn("dibatalkan", out)
        self.assertEqual((self.root / "catalog.csv").read_bytes(), sebelum)
        for n in ("skill-a", "skill-b", "skill-c"):
            self.assertFalse(self.masukan(n).exists())

    def test_tanggal_tidak_valid(self):
        kode, out = self.jalankan("--terapkan", "--tanggal", "20-10-2026")
        self.assertEqual(kode, 2)
        self.assertIn("YYYY-MM-DD", out)

    def test_skill_tanpa_folder_dilewati(self):
        import shutil
        shutil.rmtree(self.root / "skills" / "skill-c")
        kode, out = self.jalankan("--terapkan", "--tanggal", "2026-10-20")
        self.assertEqual(kode, 0, out)
        self.assertEqual(self.katalog()["skill-c"]["status"], "beta")
        self.assertEqual(self.katalog()["skill-a"]["status"], "rilis")
        self.assertFalse((self.root / "skills" / "skill-c").exists())


if __name__ == "__main__":
    unittest.main()
