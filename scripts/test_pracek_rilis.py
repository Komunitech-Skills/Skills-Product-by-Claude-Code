#!/usr/bin/env python3
"""Tes pracek_rilis.py pada repo tiruan sementara. Jalankan: python3 scripts/test_pracek_rilis.py"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pracek_rilis as pr  # noqa: E402

KOLOM = "nama,kategori,jalur,sumber_url,lisensi,skor_kualitas,tier_usulan,harga_usulan_idr,tier_final,harga_final_idr,versi,platform_teruji,status,tanggal_update"


def buat_skill(root: Path, nama: str, *, lengkap: bool = True, deskripsi: str | None = None, teks_tambahan: str = ""):
    d = root / "skills" / nama
    (d / "examples").mkdir(parents=True)
    desk = deskripsi or f"Membantu pemilik usaha menyusun {nama} dengan cepat; pakai saat diminta {nama} (ID/EN)."
    (d / "SKILL.md").write_text(f"---\nname: {nama}\ndescription: {desk}\n---\n# {nama}\n{teks_tambahan}\n", encoding="utf-8")
    if lengkap:
        (d / "README.md").write_text(f"# Judul {nama}\n\n**Hasil uji (angka nyata):** 7 → 9.\n\nSebelum/sesudah.\n\n## Instalasi\n\n## FAQ\n", encoding="utf-8")
        for n in ("HASIL-UJI.md", "00-pembanding-tanpa-skill.md", "01-a.md", "02-b.md", "03-c.md"):
            (d / "examples" / n).write_text("x\n", encoding="utf-8")
        (d / "LICENSE").write_text("MIT\n", encoding="utf-8")
    return d


def buat_repo(tmp: str):
    root = Path(tmp)
    (root / "koordinasi").mkdir()
    (root / "promosi").mkdir()
    baris = [
        KOLOM,
        "bagus,Keuangan,orisinal,,Proprietary,8,ecer,49000,ecer,49000,1.0.2,openclaw,beta,2026-10-01",
        "cacat,Marketing,kurasi,,MIT,6,ecer,,,,1.0,,beta,2026-10-01",
        "tunda,HR,orisinal,,Proprietary,8,ecer,49000,,,1.0.0,openclaw,beta,2026-10-01",
        "lama,HR,orisinal,,Proprietary,8,ecer,49000,,,1.0.0,openclaw,arsip,2026-10-01",
    ]
    (root / "catalog.csv").write_text("\n".join(baris) + "\n", encoding="utf-8")
    (root / "koordinasi" / "beta-tunda.txt").write_text("# komentar\ntunda # alasan\n", encoding="utf-8")
    (root / "promosi" / "sebelum-sesudah.jsonl").write_text(json.dumps({"nama": "bagus", "judul_jualan": "Judul bagus"}) + "\n", encoding="utf-8")
    buat_skill(root, "bagus")
    cacat = buat_skill(root, "cacat", lengkap=False, deskripsi="pendek", teks_tambahan="lihat `lama` dan {baseDir}")
    (cacat / "README.md").write_text("tanpa judul\n", encoding="utf-8")
    (cacat / "scripts").mkdir()
    (cacat / "scripts" / "rusak.py").write_text("def x(:\n", encoding="utf-8")
    (cacat / "examples" / "catatan.txt").write_text("token 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi\n", encoding="utf-8")
    buat_skill(root, "tunda")
    buat_skill(root, "lama")
    return root


class TesPracek(unittest.TestCase):
    def test_skill_lengkap_tanpa_celah_dan_tunda_dilewati(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = buat_repo(tmp)
            h = pr.periksa(root)
            self.assertEqual(h["calon"], ["bagus", "cacat"])
            self.assertEqual(h["ditunda"], ["tunda"])
            self.assertNotIn("bagus", h["celah"])
            h2 = pr.periksa(root, abaikan_tunda=True)
            self.assertIn("tunda", h2["calon"])
            self.assertIn("PROMO: tanpa baris promosi jsonl", h2["celah"]["tunda"])

    def test_skill_cacat_semua_jenis_terdeteksi(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = buat_repo(tmp)
            c = pr.periksa(root)["celah"]["cacat"]
            jenis = {x.split(":", 1)[0] for x in c}
            self.assertEqual(jenis, {"SKILL", "README", "EX", "LIS", "KAT", "PROMO", "PY", "RAHASIA"})
            self.assertTrue(any("merujuk skill arsip lama" in x for x in c))
            self.assertTrue(any("placeholder" in x for x in c))
            self.assertTrue(any("kurasi tanpa sumber_url" in x for x in c))
            self.assertTrue(any("skor 6 < 7" in x for x in c))
            self.assertTrue(any("bukan X.Y.Z" in x for x in c))
            self.assertTrue(any("rusak.py gagal kompilasi" in x for x in c))
            self.assertTrue(any("RAHASIA" in x for x in c))

    def test_h1_tidak_sama_dengan_judul_promosi(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = buat_repo(tmp)
            p = root / "skills" / "bagus" / "README.md"
            p.write_text(p.read_text(encoding="utf-8").replace("# Judul bagus", "# Judul Lain"), encoding="utf-8")
            c = pr.periksa(root)["celah"]["bagus"]
            self.assertEqual(len(c), 1)
            self.assertIn("H1 ≠ judul_jualan", c[0])

    def test_main_kode_keluar_dan_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = buat_repo(tmp)
            self.assertEqual(pr.main(["--root", str(root), "--skill", "bagus"]), 0)
            self.assertEqual(pr.main(["--root", str(root)]), 1)
            # hanya peringatan PROMO (tunda, lengkap tetapi tanpa baris promosi) → kode keluar 0
            self.assertEqual(pr.main(["--root", str(root), "--abaikan-tunda", "--skill", "tunda"]), 0)
            self.assertEqual(pr.periksa(root, abaikan_tunda=True, skill={"tunda"})["penghalang"], [])
            self.assertEqual(pr.main(["--root", str(Path(tmp) / "kosong")]), 2)
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                pr.main(["--root", str(root), "--json", "--skill", "cacat"])
            d = json.loads(buf.getvalue())
            self.assertIn("cacat", d["celah"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
