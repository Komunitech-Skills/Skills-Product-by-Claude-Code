#!/usr/bin/env python3
"""Buat paket ZIP ber-watermark untuk pembeli ecer, bundle, atau member VIP.

Contoh:
  python3 scripts/build.py --pembeli "Budi <budi@contoh.com>" --skill caption-sosmed-umkm
  python3 scripts/build.py --pembeli "Budi <budi@contoh.com>" --bundle paket-toko-online
  python3 scripts/build.py --pembeli "Member VIP #0123" --vip

Hanya skill berstatus 'rilis' yang dipaketkan. --beta mengikutkan status 'beta' (untuk beta tester);
--izinkan-draft untuk uji coba internal.
"""
import argparse
import csv
import hashlib
import re
import secrets
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DIABAIKAN = {"__pycache__", ".DS_Store", "Thumbs.db"}


def buat_kode_lisensi(pembeli, waktu):
    acak = secrets.token_hex(8)
    h = hashlib.sha256(f"{pembeli}|{waktu}|{acak}".encode()).hexdigest().upper()
    return f"KMT-{h[:4]}-{h[4:8]}-{h[8:12]}"


def sisipkan_watermark(teks_skill, baris_watermark):
    """Sisipkan komentar HTML tepat setelah frontmatter SKILL.md."""
    akhir = teks_skill.find("\n---", 4)
    posisi = teks_skill.find("\n", akhir + 1) + 1
    return teks_skill[:posisi] + baris_watermark + "\n" + teks_skill[posisi:]


def slug(teks):
    return re.sub(r"[^a-z0-9]+", "-", teks.lower()).strip("-")[:40] or "pembeli"


def gagal(pesan):
    sys.exit(f"❌ {pesan}")


def pilih_skill(a, katalog):
    if a.vip:
        return [b for b in katalog.values() if b["status"] not in {"ide", "ditolak", "arsip"}], "VIP"

    if a.bundle:
        path = ROOT / "bundles" / f"{a.bundle}.txt"
        if not path.is_file():
            gagal(f"Bundle '{a.bundle}' tidak ada di bundles/.")
        nama, jenis = path.read_text(encoding="utf-8").split(), "BUNDLE"
    else:
        nama, jenis = list(dict.fromkeys(a.skill)), "ECER"

    hasil = []
    for n in nama:
        b = katalog.get(n)
        if b is None:
            gagal(f"Skill '{n}' tidak ada di catalog.csv.")
        if b["status"] in {"ide", "ditolak", "arsip"}:
            gagal(f"Skill '{n}' berstatus '{b['status']}', tidak bisa dijual.")
        tier = b["tier_final"]
        if not tier and not (a.izinkan_draft or a.beta):
            gagal(f"Skill '{n}' belum punya tier_final dari pemilik.")
        if tier == "vip":
            gagal(f"Skill '{n}' eksklusif VIP, tidak dijual ecer/bundle.")
        hasil.append(b)
    return hasil, jenis


def main():
    p = argparse.ArgumentParser(description="Build paket skill untuk pembeli")
    p.add_argument("--pembeli", required=True, help="Nama/email/ID member pembeli")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--skill", action="append", help="Nama skill (paket ecer), bisa diulang")
    target.add_argument("--bundle", help="Nama bundle di bundles/<nama>.txt")
    target.add_argument("--vip", action="store_true", help="Semua skill (paket VIP)")
    p.add_argument("--beta", action="store_true",
                   help="Ikutkan skill berstatus 'beta' (paket untuk beta tester)")
    p.add_argument("--izinkan-draft", action="store_true",
                   help="Ikutkan skill yang belum 'rilis' / belum ada tier_final (HANYA untuk uji coba)")
    a = p.parse_args()

    # Validasi dulu supaya paket yang terkirim selalu bersih
    if subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")]).returncode != 0:
        gagal("Build dibatalkan: perbaiki masalah validasi dulu.")

    with (ROOT / "catalog.csv").open(newline="", encoding="utf-8") as f:
        katalog = {b["nama"]: b for b in csv.DictReader(f)}

    pilihan, jenis = pilih_skill(a, katalog)
    boleh = {"rilis", "beta"} if a.beta else {"rilis"}
    belum_rilis = [b["nama"] for b in pilihan if b["status"] not in boleh]
    if belum_rilis and not a.izinkan_draft:
        if a.vip:
            print(f"ℹ️  Dilewati (belum rilis): {', '.join(belum_rilis)}")
            pilihan = [b for b in pilihan if b["status"] in boleh]
        else:
            gagal(f"Belum rilis: {', '.join(belum_rilis)}. Pakai --izinkan-draft untuk uji coba.")
    if not pilihan:
        gagal("Tidak ada skill untuk dipaketkan.")

    waktu = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    kode = buat_kode_lisensi(a.pembeli, waktu)
    watermark = (f"<!-- Lisensi Komunitech: {kode} | Pemegang: {a.pembeli} | {waktu} | "
                 f"Dilarang menyebarluaskan. -->")

    DIST.mkdir(exist_ok=True)
    label = a.bundle if a.bundle else jenis.lower()
    nama_zip = f"komunitech-{label}-{slug(a.pembeli)}-{kode[4:].replace('-', '').lower()}.zip"
    path_zip = DIST / nama_zip
    lisensi = (ROOT / "LICENSE").read_text("utf-8")
    instalasi = ROOT / "docs" / "instalasi.md"

    with zipfile.ZipFile(path_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for b in pilihan:
            folder = ROOT / "skills" / b["nama"]
            for f in sorted(folder.rglob("*")):
                if not f.is_file() or DIABAIKAN & set(f.relative_to(folder).parts):
                    continue
                arc = f"{b['nama']}/{f.relative_to(folder).as_posix()}"
                if f.name == "SKILL.md" and f.parent == folder:
                    z.writestr(arc, sisipkan_watermark(f.read_text("utf-8"), watermark))
                else:
                    z.write(f, arc)
        if instalasi.is_file():
            z.write(instalasi, "CARA-INSTAL.md")
        daftar = "\n".join(f"  - {b['nama']} v{b['versi']}" for b in pilihan)
        z.writestr("LISENSI.txt",
                   f"Kode lisensi : {kode}\nPemegang     : {a.pembeli}\nJenis        : {jenis}\n"
                   f"Tanggal      : {waktu}\nSkill:\n{daftar}\n\n{'=' * 60}\n\n{lisensi}")

    # Catat lisensi untuk pelacakan (dist/ tidak di-commit)
    log = DIST / "lisensi.csv"
    baru = not log.exists()
    with log.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if baru:
            w.writerow(["kode", "pembeli", "jenis", "waktu", "skill", "file"])
        w.writerow([kode, a.pembeli, label, waktu,
                    ";".join(f"{b['nama']}@{b['versi']}" for b in pilihan), nama_zip])

    print(f"✅ Paket {jenis} dibuat: {path_zip.relative_to(ROOT)}")
    print(f"   Kode lisensi: {kode}")
    print(f"   Skill: {', '.join(b['nama'] for b in pilihan)}")


if __name__ == "__main__":
    main()
