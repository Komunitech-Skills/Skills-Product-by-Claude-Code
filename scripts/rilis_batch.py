#!/usr/bin/env python3
"""Rilis batch (keputusan otomatis 62): skill berstatus `beta` naik ke `rilis`.

Aturan keputusan 62: pada 20 Okt 2026 semua skill `beta` di catalog.csv yang TIDAK menerima
masukan negatif tester naik ke `rilis`. Skill yang masih perlu ditahan ditulis di
`koordinasi/beta-tunda.txt` (satu nama per baris, komentar dengan `#`); skill itu tetap `beta`.

Pemakaian (default DRY-RUN, tidak menulis apa pun):

    python3 scripts/rilis_batch.py                      # ringkasan saja
    python3 scripts/rilis_batch.py --cek                # periksa prasyarat + validate.py, tanpa menulis
    python3 scripts/rilis_batch.py --terapkan           # tulis perubahan (lalu validate.py; batal bila gagal)
    python3 scripts/rilis_batch.py --terapkan --tanggal 2026-10-20
    python3 scripts/rilis_batch.py --hanya nama1,nama2  # batasi ke skill tertentu

Di Windows, pakai `python` atau `py` sebagai pengganti `python3`.
Hanya Python standar. Tidak melakukan git commit.
"""
import argparse
import csv
import datetime
import io
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TANGGAL_RENCANA = "2026-10-20"  # tanggal rilis batch menurut keputusan otomatis 62
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
KOLOM_WAJIB = {"nama", "status", "tanggal_update", "versi"}
SKOR_MINIMAL = 7  # sama dengan validate.py untuk status lulus/beta/rilis


class GalatInput(Exception):
    """Kesalahan pemakaian atau data masukan (kode keluar 2)."""


# ---------------------------------------------------------------- baca/tulis catalog

def baca_katalog(path):
    """Kembalikan (daftar kolom, daftar baris dict, teks asli)."""
    teks = path.read_bytes().decode("utf-8")
    r = csv.DictReader(io.StringIO(teks, newline=""))
    kolom = r.fieldnames or []
    kurang = KOLOM_WAJIB - set(kolom)
    if kurang:
        raise GalatInput(f"{path.name}: kolom wajib tidak ada: {sorted(kurang)}")
    return kolom, list(r), teks


def serialisasi(kolom, baris):
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=kolom, lineterminator="\n")
    w.writeheader()
    w.writerows(baris)
    return buf.getvalue()


def baca_tunda(path):
    """Nama skill dari berkas daftar tunda (kosong bila berkas tidak ada)."""
    if not path.is_file():
        return []
    nama = []
    for baris in path.read_text(encoding="utf-8").splitlines():
        baris = baris.split("#", 1)[0].strip()
        if baris:
            nama.append(baris)
    return nama


def tanggal_valid(teks):
    try:
        datetime.datetime.strptime(teks, "%Y-%m-%d")
    except ValueError:
        raise GalatInput(f"--tanggal harus format YYYY-MM-DD yang valid (diberikan: {teks!r})")
    return teks


def tanggal_indonesia(iso):
    d = datetime.datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


# ---------------------------------------------------------------- perencanaan

def susun_rencana(baris, tunda, hanya, folder_skills):
    """Kelompokkan skill beta: naik / tunda / folder_tidak_ada / di_luar_hanya."""
    nama_katalog = {b["nama"] for b in baris}
    beta = [b["nama"] for b in baris if b["status"] == "beta"]
    rencana = {"beta": beta, "naik": [], "tunda": [], "tanpa_folder": [], "di_luar_hanya": [],
               "peringatan": []}
    for n in tunda:
        if n not in nama_katalog:
            rencana["peringatan"].append(f"daftar tunda: '{n}' tidak ada di catalog.csv")
        elif n not in beta:
            rencana["peringatan"].append(f"daftar tunda: '{n}' bukan berstatus beta (diabaikan)")
    if hanya is not None:
        asing = [n for n in hanya if n not in nama_katalog]
        if asing:
            raise GalatInput(f"--hanya: tidak ada di catalog.csv: {', '.join(asing)}")
        for n in hanya:
            if n not in beta:
                rencana["peringatan"].append(f"--hanya: '{n}' bukan berstatus beta (dilewati)")
    for n in beta:
        if hanya is not None and n not in hanya:
            rencana["di_luar_hanya"].append(n)
        elif n in tunda:
            rencana["tunda"].append(n)
        elif not (folder_skills / n).is_dir():
            rencana["tanpa_folder"].append(n)
        else:
            rencana["naik"].append(n)
    return rencana


def cetak_ringkasan(rencana, judul, tanggal, folder_skills):
    naik = rencana["naik"]
    sudah = [n for n in naik if (folder_skills / n / "examples" / "MASUKAN-BETA.md").exists()]
    print(f"== Rilis batch (keputusan otomatis 62) — {judul} ==")
    print(f"Tanggal efektif       : {tanggal}")
    print(f"Skill beta di katalog : {len(rencana['beta'])}")
    if rencana["di_luar_hanya"]:
        print(f"Di luar --hanya       : {len(rencana['di_luar_hanya'])}")
    print(f"Akan naik ke rilis    : {len(naik)}")
    print(f"Dilewati (daftar tunda): {len(rencana['tunda'])}")
    if rencana["tanpa_folder"]:
        print(f"Dilewati (folder tidak ada): {len(rencana['tanpa_folder'])}")
    print(f"MASUKAN-BETA.md       : {len(naik) - len(sudah)} akan dibuat, {len(sudah)} sudah ada (tidak ditimpa)")
    if naik:
        print("\nAkan naik ke rilis:")
        for n in naik:
            print(f"  - {n}")
    if rencana["tunda"]:
        print("\nDilewati (tetap beta, ada di koordinasi/beta-tunda.txt):")
        for n in rencana["tunda"]:
            print(f"  - {n}")
    if rencana["tanpa_folder"]:
        print("\nDilewati (folder skills/<nama> tidak ada):")
        for n in rencana["tanpa_folder"]:
            print(f"  - {n}")
    for p in rencana["peringatan"]:
        print(f"PERINGATAN: {p}")


# ---------------------------------------------------------------- prasyarat (--cek)

def periksa_prasyarat(baris, naik, folder_skills):
    """Daftar masalah untuk skill yang akan naik (syarat yang sama dengan validate.py)."""
    per_nama = {b["nama"]: b for b in baris}
    masalah = []
    for n in naik:
        b = per_nama[n]
        folder = folder_skills / n
        if not (folder / "SKILL.md").is_file():
            masalah.append(f"{n}: SKILL.md tidak ada")
        contoh = folder / "examples"
        if not contoh.is_dir() or not any(contoh.iterdir()):
            masalah.append(f"{n}: examples/ kosong atau tidak ada")
        skor = b.get("skor_kualitas", "")
        if not skor.isdigit() or int(skor) < SKOR_MINIMAL:
            masalah.append(f"{n}: skor_kualitas {skor!r} < {SKOR_MINIMAL}")
        if not b.get("platform_teruji"):
            masalah.append(f"{n}: platform_teruji kosong")
    return masalah


# ---------------------------------------------------------------- penerapan

def isi_masukan_beta(nama, versi, tanggal):
    return (
        f"# Masukan beta — {nama}\n"
        "\n"
        f"- **Versi yang diuji:** {versi}\n"
        "- **Masa beta:** 13–19 Oktober 2026\n"
        f"- **Masukan tester:** tidak ada masukan negatif yang diterima sampai {tanggal_indonesia(tanggal)}.\n"
        "- **Keputusan:** status rilis (keputusan kurator 62).\n"
    )


def jalankan_validate(root):
    skrip = root / "scripts" / "validate.py"
    hasil = subprocess.run([sys.executable, str(skrip)], cwd=str(root),
                           capture_output=True, text=True)
    return hasil.returncode, (hasil.stdout + hasil.stderr).strip()


def terapkan(root, path_katalog, kolom, baris, teks_asli, naik, tanggal):
    """Tulis perubahan; kembalikan (berhasil, daftar berkas MASUKAN yang dibuat)."""
    skrip_validate = root / "scripts" / "validate.py"
    if not skrip_validate.is_file():
        raise GalatInput(f"{skrip_validate} tidak ditemukan; --terapkan butuh validate.py untuk verifikasi")
    if serialisasi(kolom, baris) != teks_asli:
        raise GalatInput("catalog.csv tidak identik setelah dibaca-tulis ulang tanpa perubahan "
                         "(format akan berubah); dibatalkan, tidak ada yang ditulis")

    waktu = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    cadangan = path_katalog.with_name(f"{path_katalog.name}.bak-{waktu}")
    cadangan.write_bytes(path_katalog.read_bytes())
    print(f"Cadangan catalog: {cadangan.name}")

    dibuat = []
    try:
        naik_set = set(naik)
        for b in baris:
            if b["nama"] in naik_set:
                versi = b["versi"]
                b["status"] = "rilis"
                b["tanggal_update"] = tanggal
                target = root / "skills" / b["nama"] / "examples" / "MASUKAN-BETA.md"
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(isi_masukan_beta(b["nama"], versi, tanggal), encoding="utf-8")
                    dibuat.append(target)
        sementara = path_katalog.with_name(path_katalog.name + ".tmp")
        sementara.write_bytes(serialisasi(kolom, baris).encode("utf-8"))
        os.replace(sementara, path_katalog)
        kode, keluaran = jalankan_validate(root)
    except BaseException:
        pulihkan(path_katalog, cadangan, dibuat)
        raise
    if kode != 0:
        print("validate.py GAGAL; perubahan dibatalkan:")
        print(keluaran)
        pulihkan(path_katalog, cadangan, dibuat)
        print(f"catalog.csv dipulihkan dari {cadangan.name}; {len(dibuat)} berkas MASUKAN-BETA.md baru dihapus.")
        return False, []
    print(keluaran.splitlines()[-1] if keluaran else "validate.py lolos")
    return True, dibuat


def pulihkan(path_katalog, cadangan, dibuat):
    path_katalog.write_bytes(cadangan.read_bytes())
    for f in dibuat:
        try:
            f.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------- main

def buat_parser():
    ap = argparse.ArgumentParser(
        description="Naikkan skill beta ke rilis (keputusan otomatis 62). Default: dry-run.")
    ap.add_argument("--terapkan", action="store_true",
                    help="tulis perubahan ke catalog.csv + MASUKAN-BETA.md, lalu jalankan validate.py")
    ap.add_argument("--cek", action="store_true",
                    help="hanya validasi prasyarat + validate.py, tanpa menulis")
    ap.add_argument("--hanya", help="batasi ke nama skill tertentu, dipisah koma")
    ap.add_argument("--tanggal", help="paksa tanggal_update (YYYY-MM-DD); default hari ini")
    ap.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)  # untuk tes
    return ap


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        return _main(args)
    except GalatInput as e:
        print(f"GALAT: {e}", file=sys.stderr)
        return 2


def _main(args):
    if args.terapkan and args.cek:
        raise GalatInput("--terapkan dan --cek tidak bisa dipakai bersamaan")
    root = Path(args.root).resolve()
    tanggal = tanggal_valid(args.tanggal) if args.tanggal else datetime.date.today().isoformat()
    hanya = None
    if args.hanya is not None:
        hanya = [n.strip() for n in args.hanya.split(",") if n.strip()]
        if not hanya:
            raise GalatInput("--hanya kosong")
    path_katalog = root / "catalog.csv"
    if not path_katalog.is_file():
        raise GalatInput(f"{path_katalog} tidak ditemukan")
    folder_skills = root / "skills"

    kolom, baris, teks_asli = baca_katalog(path_katalog)
    tunda = baca_tunda(root / "koordinasi" / "beta-tunda.txt")
    rencana = susun_rencana(baris, tunda, hanya, folder_skills)
    mode = "TERAPKAN" if args.terapkan else ("CEK" if args.cek else "DRY-RUN, tidak ada yang ditulis")
    cetak_ringkasan(rencana, mode, tanggal, folder_skills)
    if tanggal < TANGGAL_RENCANA:
        print(f"\nCATATAN: jadwal keputusan 62 adalah {TANGGAL_RENCANA}; tanggal efektif {tanggal} lebih awal. "
              "Pastikan tidak ada pembatalan ('batal 62') di koordinasi/keputusan-otomatis.md.")

    if args.cek:
        masalah = periksa_prasyarat(baris, rencana["naik"], folder_skills)
        kode, keluaran = jalankan_validate(root) if (root / "scripts" / "validate.py").is_file() else (
            1, "scripts/validate.py tidak ditemukan")
        print("\n-- Hasil cek --")
        for m in masalah:
            print(f"MASALAH: {m}")
        print(f"validate.py (kondisi saat ini): {'lolos' if kode == 0 else 'GAGAL'}")
        if kode != 0:
            print(keluaran)
        ok = not masalah and kode == 0
        print("Cek: OK, siap --terapkan." if ok else "Cek: ADA MASALAH.")
        return 0 if ok else 1

    if not args.terapkan:
        print("\nDRY-RUN: tidak ada berkas diubah. Tambahkan --terapkan untuk menulis.")
        return 0

    if not rencana["naik"]:
        print("\nTidak ada skill yang perlu dinaikkan; tidak ada yang ditulis.")
        return 0
    berhasil, dibuat = terapkan(root, path_katalog, kolom, baris, teks_asli, rencana["naik"], tanggal)
    if not berhasil:
        return 1
    print(f"\nSELESAI: {len(rencana['naik'])} skill beta → rilis (tanggal_update {tanggal}); "
          f"{len(dibuat)} MASUKAN-BETA.md dibuat. Belum di-commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
