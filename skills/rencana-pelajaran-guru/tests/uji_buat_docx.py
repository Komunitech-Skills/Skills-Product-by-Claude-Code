#!/usr/bin/env python3
"""Tes scripts/buat_docx.py (Python standar). Jalankan: python3 tests/uji_buat_docx.py"""
import os, subprocess, sys, tempfile, zipfile
from xml.dom import minidom

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(AKAR, "scripts", "buat_docx.py")
CONTOH = os.path.join(AKAR, "examples", "06-contoh-masukan-docx.md")


def jalan(*a):
    return subprocess.run([sys.executable, SCRIPT, *a], capture_output=True, text=True)


def main():
    gagal = 0
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "x.docx")
        r = jalan(CONTOH, out)
        ok = r.returncode == 0 and zipfile.is_zipfile(out)
        print("contoh -> docx:", "LULUS" if ok else "GAGAL", r.stdout.strip(), r.stderr.strip())
        gagal += not ok
        if ok:
            z = zipfile.ZipFile(out)
            for n in ("[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/styles.xml"):
                try:
                    minidom.parseString(z.read(n))
                except Exception as e:
                    print("XML tidak valid", n, e); gagal += 1
            xml = z.read("word/document.xml").decode()
            for kata, nama in [("Kunci Jawaban (untuk guru)", "judul kunci"), ("w:tbl", "tabel"),
                               ('w:br w:type="page"', "halaman baru"), ("Heading1", "heading"),
                               ("&amp;", "escape &")]:
                c = kata in xml
                print(" ada", nama, ":", "LULUS" if c else "GAGAL"); gagal += not c
            # kunci hanya setelah penanda halaman baru
            awal = xml.index('w:br w:type="page"')
            c = "Jawaban: " not in xml[:awal]
            print(" lembar siswa tanpa jawaban:", "LULUS" if c else "GAGAL"); gagal += not c
        # input buruk
        for args, nama in [((os.path.join(d, "tidak-ada.md"), out), "file tidak ada"),
                           (("a.md",), "argumen kurang"),
                           ((CONTOH, os.path.join(d, "x.txt")), "ekstensi salah")]:
            r = jalan(*args)
            c = r.returncode == 1 and "Traceback" not in r.stderr
            print("input buruk", nama, ":", "LULUS" if c else "GAGAL"); gagal += not c
        kosong = os.path.join(d, "k.md"); open(kosong, "w").close()
        r = jalan(kosong, out)
        c = r.returncode == 1 and "Traceback" not in r.stderr
        print("input buruk file kosong:", "LULUS" if c else "GAGAL"); gagal += not c
    print("TOTAL GAGAL:", gagal)
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
