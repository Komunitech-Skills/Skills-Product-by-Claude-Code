#!/usr/bin/env python3
"""Uji scripts/pdf_cadangan.py (jalur cadangan tanpa Stirling-PDF).

Bagian A - deteksi & pemilihan alat memakai PATH buatan (alat palsu), jadi selalu bisa
           dijalankan tanpa memasang apa pun.
Bagian B - operasi sungguhan dengan qpdf/Ghostscript BILA sudah terpasang di komputer
           penguji (dilewati dengan keterangan bila tidak ada). Hasil diverifikasi
           independen dengan `qpdf --show-npages` / `--show-encryption`.

Jalankan: python3 uji_cadangan.py   (keluar 0 bila semua lulus)
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SINI = Path(__file__).resolve().parent
SCRIPT = SINI.parent / "scripts" / "pdf_cadangan.py"
sys.path.insert(0, str(SCRIPT.parent))
sys.dont_write_bytecode = True
import pdf_cadangan as pc  # noqa: E402

PDF_MINIMAL = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 300]>>endobj\n"
    b"trailer<</Size 4/Root 1 0 R>>\n%%EOF"
)

lulus = gagal = 0


def cek(nama, kondisi, ket=""):
    global lulus, gagal
    if kondisi:
        lulus += 1
        print(f"lulus [{nama}]")
    else:
        gagal += 1
        print(f"GAGAL [{nama}] {ket}")


def jalankan(args, env_path=None, cwd=None):
    env = dict(os.environ)
    if env_path is not None:
        env["PATH"] = env_path
    r = subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True,
                       encoding="utf-8", env=env, cwd=cwd)
    return r.returncode, r.stdout, r.stderr


def buat_alat_palsu(folder, nama):
    """Alat palsu (POSIX, skrip Python): menyalin PDF pertama ke argumen setelah 'output'
    dan mencatat argumen yang diterima (bukti dipanggil tanpa shell, argumen utuh)."""
    p = folder / nama
    p.write_text(
        f"#!{sys.executable}\n"
        "import shutil, sys, pathlib\n"
        "a = sys.argv[1:]\n"
        "src = next(x for x in a if x.endswith('.pdf'))\n"
        "out = pathlib.Path(a[a.index('output') + 1])\n"
        "(out.parent / ('argumen-' + pathlib.Path(sys.argv[0]).name + '.txt')).write_text(' '.join(a))\n"
        "shutil.copy(src, out)\n", encoding="utf-8")
    p.chmod(0o755)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="uji-pdf-cadangan-"))
    try:
        a, b = tmp / "nota-a.pdf", tmp / "nota-b.pdf"
        a.write_bytes(PDF_MINIMAL)
        b.write_bytes(PDF_MINIMAL)

        # ---------------- Bagian A: deteksi & fallback ----------------
        kosong = tmp / "path-kosong"
        kosong.mkdir()
        cek("deteksi-tanpa-alat", pc.cari_alat(str(kosong)) == {})
        rc, out, err = jalankan(["alat"], env_path=str(kosong))
        cek("alat-tanpa-alat-tidak-memasang", rc == 0 and "tidak ada alat PDF lokal" in out
            and "Jangan memasang" in out, f"out={out!r}")
        rc, out, err = jalankan(["gabung", str(a), str(b)], env_path=str(kosong), cwd=str(tmp))
        cek("gabung-tanpa-alat-pesan-jelas", rc == 1 and "TIDAK memasang" in err
            and "references/pasang-stirling.md" in err and "Traceback" not in err, f"err={err!r}")

        cek("prioritas-kompres-gs-dulu", pc.pilih_alat("kompres", {"qpdf": "q", "gs": "g"}) == "gs")
        cek("prioritas-gabung-qpdf-dulu", pc.pilih_alat("gabung", {"qpdf": "q", "pdftk": "p", "gs": "g"}) == "qpdf")
        cek("fallback-kunci-ke-pdftk", pc.pilih_alat("kunci", {"pdftk": "p", "gs": "g"}) == "pdftk")
        try:
            pc.pilih_alat("kunci", {"gs": "g"})
            cek("kunci-hanya-gs-ditolak", False, "seharusnya Gagal")
        except pc.Gagal:
            cek("kunci-hanya-gs-ditolak", True)
        try:
            pc.parse_rentang("3-1")
            cek("rentang-terbalik-ditolak", False)
        except pc.Gagal:
            cek("rentang-terbalik-ditolak", True)
        cek("rentang-ganda", pc.parse_rentang("1,3,5-9") == [(1, 1), (3, 3), (5, 9)])

        if os.name == "posix":
            palsu = tmp / "path-pdftk"
            palsu.mkdir()
            buat_alat_palsu(palsu, "pdftk")
            cek("deteksi-pdftk-palsu", set(pc.cari_alat(str(palsu))) == {"pdftk"})
            rc, out, err = jalankan(["gabung", str(a), str(b)], env_path=str(palsu), cwd=str(tmp))
            hasil = tmp / "nota-a-gabungan.pdf"
            argumen = (tmp / "argumen-pdftk.txt").read_text() if (tmp / "argumen-pdftk.txt").exists() else ""
            cek("gabung-via-pdftk-tanpa-shell", rc == 0 and "via pdftk" in out and hasil.is_file()
                and "cat output" in argumen, f"rc={rc} out={out!r} err={err!r} arg={argumen!r}")
            rc, out, err = jalankan(["kompres", str(a)], env_path=str(palsu), cwd=str(tmp))
            cek("kompres-tanpa-gs-qpdf-ditolak", rc == 1 and "gs, qpdf" in err, f"err={err!r}")
        else:
            print("lewati [alat-palsu] (hanya POSIX)")

        # Input buruk
        bukan = tmp / "foto.pdf"
        bukan.write_bytes(b"\xff\xd8\xff\xe0 bukan pdf")
        rc, out, err = jalankan(["putar", str(bukan), "--derajat", "90"], cwd=str(tmp))
        cek("bukan-pdf-ditolak", rc == 1 and "Bukan file PDF" in err, f"err={err!r}")
        rc, out, err = jalankan(["gabung", str(a), str(b), "--keluaran", str(a)], cwd=str(tmp))
        cek("tidak-menimpa-asli", rc == 1 and a.read_bytes() == PDF_MINIMAL, f"rc={rc} err={err!r}")
        rc, out, err = jalankan(["gabung", str(tmp / "hilang.pdf"), str(b)], cwd=str(tmp))
        cek("file-tidak-ada", rc == 1 and "tidak ditemukan" in err, f"err={err!r}")

        # ---------------- Bagian B: alat sungguhan ----------------
        alat = pc.cari_alat()
        qpdf = alat.get("qpdf")
        if qpdf:
            rc, out, err = jalankan(["gabung", str(a), str(b), str(a), "--keluaran", str(tmp / "g3.pdf"),
                                     "--alat", "qpdf"], cwd=str(tmp))
            n = subprocess.run([qpdf, "--show-npages", str(tmp / "g3.pdf")], capture_output=True, text=True).stdout.strip()
            cek("qpdf-gabung-3-halaman", rc == 0 and n == "3", f"rc={rc} n={n!r} err={err!r}")

            rc, out, err = jalankan(["kunci", str(a), "--sandi", "Rina0926"], cwd=str(tmp))
            kunci = tmp / "nota-a-terkunci.pdf"
            enk = subprocess.run([qpdf, "--password=Rina0926", "--show-encryption", str(kunci)],
                                 capture_output=True, text=True).stdout
            salah = subprocess.run([qpdf, "--password=salah", "--check", str(kunci)], capture_output=True, text=True)
            cek("qpdf-kunci-aes256", rc == 0 and "R = 6" in enk and salah.returncode != 0,
                f"rc={rc} enk={enk!r} err={err!r}")
            rc, out, err = jalankan(["buka-kunci", str(kunci), "--sandi", "salah"], cwd=str(tmp))
            cek("qpdf-sandi-salah-pesan-ramah", rc == 1 and "kata sandi" in err.lower(), f"err={err!r}")
            rc, out, err = jalankan(["buka-kunci", str(kunci), "--sandi", "Rina0926"], cwd=str(tmp))
            enk2 = subprocess.run([qpdf, "--show-encryption", str(tmp / "nota-a-terkunci-terbuka.pdf")],
                                  capture_output=True, text=True).stdout
            cek("qpdf-buka-kunci", rc == 0 and "not encrypted" in enk2, f"rc={rc} enk={enk2!r}")

            rc, out, err = jalankan(["pisah-rentang", str(tmp / "g3.pdf"), "--halaman", "2-3"], cwd=str(tmp))
            n = subprocess.run([qpdf, "--show-npages", str(tmp / "g3-hal-2-3.pdf")], capture_output=True, text=True).stdout.strip()
            cek("qpdf-pisah-rentang", rc == 0 and n == "2", f"rc={rc} n={n!r} err={err!r}")
            rc, out, err = jalankan(["pisah-rentang", str(tmp / "g3.pdf"), "--halaman", "7-9"], cwd=str(tmp))
            cek("qpdf-halaman-melebihi", rc == 1 and "melebihi jumlah halaman" in err, f"err={err!r}")
            rc, out, err = jalankan(["putar", str(a), "--derajat", "90"], cwd=str(tmp))
            cek("qpdf-putar", rc == 0 and (tmp / "nota-a-putar90.pdf").is_file(), f"err={err!r}")
            rc, out, err = jalankan(["pisah-halaman", str(tmp / "g3.pdf")], cwd=str(tmp))
            cek("qpdf-pisah-halaman", rc == 0 and len(list((tmp / "g3-per-halaman").glob("*.pdf"))) == 3, f"err={err!r}")
        else:
            print("lewati [qpdf-*] (qpdf tidak terpasang di komputer penguji)")

        gs = alat.get("gs")
        if gs:
            rc, out, err = jalankan(["gabung", str(a), str(b), "--keluaran", str(tmp / "gs-gab.pdf"), "--alat", "gs"],
                                    cwd=str(tmp))
            cek("gs-gabung", rc == 0 and (tmp / "gs-gab.pdf").read_bytes().startswith(b"%PDF"), f"err={err!r}")
            rc, out, err = jalankan(["kompres", str(a), "--alat", "gs"], cwd=str(tmp))
            # PDF minimal tidak bisa dikecilkan: hasil harus dibuang dengan pesan jujur, bukan klaim "berhasil".
            cek("gs-kompres-jujur-bila-tidak-mengecil", rc == 0 and (
                ("Tidak bisa dikecilkan" in out and not (tmp / "nota-a-kompres.pdf").exists())
                or "Berhasil dikompres" in out), f"out={out!r} err={err!r}")
        else:
            print("lewati [gs-*] (Ghostscript tidak terpasang di komputer penguji)")

        rc, out, err = jalankan(["--help"])
        cek("versi-di-bantuan", rc == 0 and f"v{pc.VERSI}" in out, f"out={out!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{lulus}/{lulus + gagal} skenario lulus.")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
