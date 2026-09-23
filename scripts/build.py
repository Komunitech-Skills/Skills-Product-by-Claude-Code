#!/usr/bin/env python3
"""Buat paket ZIP ber-watermark untuk pembeli ecer atau member VIP.

Contoh:
  python3 scripts/build.py --pembeli "Budi <budi@contoh.com>" --skill caption-sosmed-umkm
  python3 scripts/build.py --pembeli "Member VIP #0123" --vip
"""
import argparse
import csv
import hashlib
import json
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


def main():
    p = argparse.ArgumentParser(description="Build paket skill untuk pembeli")
    p.add_argument("--pembeli", required=True, help="Nama/email/ID member pembeli")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--skill", action="append", help="ID skill (paket ecer), bisa diulang")
    target.add_argument("--vip", action="store_true", help="Semua skill (paket VIP)")
    p.add_argument("--izinkan-draft", action="store_true",
                   help="Ikutkan skill berstatus draft (hanya untuk uji coba)")
    a = p.parse_args()

    # Validasi dulu supaya paket yang terkirim selalu bersih
    if subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")]).returncode != 0:
        sys.exit("Build dibatalkan: perbaiki masalah validasi dulu.")

    katalog = {s["id"]: s for s in json.loads((ROOT / "catalog.json").read_text("utf-8"))["skills"]}

    if a.vip:
        pilihan = [s for s in katalog.values() if s["status"] != "arsip"]
        jenis = "VIP"
    else:
        pilihan = []
        for sid in dict.fromkeys(a.skill):
            if sid not in katalog:
                sys.exit(f"Skill '{sid}' tidak ada di katalog.")
            if not katalog[sid]["tersedia_ecer"]:
                sys.exit(f"Skill '{sid}' tidak dijual ecer (khusus VIP).")
            if katalog[sid]["status"] == "arsip":
                sys.exit(f"Skill '{sid}' sudah diarsipkan.")
            pilihan.append(katalog[sid])
        jenis = "ECER"

    draft = [s["id"] for s in pilihan if s["status"] == "draft"]
    if draft and not a.izinkan_draft:
        if a.vip:
            print(f"ℹ️  Skill draft dilewati: {', '.join(draft)}")
            pilihan = [s for s in pilihan if s["status"] != "draft"]
        else:
            sys.exit(f"Skill masih draft: {', '.join(draft)}. Pakai --izinkan-draft untuk uji coba.")
    if not pilihan:
        sys.exit("Tidak ada skill untuk dipaketkan.")

    waktu = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    kode = buat_kode_lisensi(a.pembeli, waktu)
    watermark = (f"<!-- Lisensi Komunitech: {kode} | Pemegang: {a.pembeli} | {waktu} | "
                 f"Dilarang menyebarluaskan. -->")

    DIST.mkdir(exist_ok=True)
    nama_zip = f"komunitech-{jenis.lower()}-{slug(a.pembeli)}-{kode[4:].replace('-', '').lower()}.zip"
    path_zip = DIST / nama_zip
    lisensi = (ROOT / "LICENSE").read_text("utf-8")

    with zipfile.ZipFile(path_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for s in pilihan:
            folder = ROOT / "skills" / s["id"]
            for f in sorted(folder.rglob("*")):
                if not f.is_file() or DIABAIKAN & set(f.relative_to(folder).parts):
                    continue
                arc = f"{s['id']}/{f.relative_to(folder).as_posix()}"
                if f.name == "SKILL.md":
                    z.writestr(arc, sisipkan_watermark(f.read_text("utf-8"), watermark))
                else:
                    z.write(f, arc)
        daftar = "\n".join(f"  - {s['id']} v{s['versi']}" for s in pilihan)
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
        w.writerow([kode, a.pembeli, jenis, waktu,
                    ";".join(f"{s['id']}@{s['versi']}" for s in pilihan), nama_zip])

    print(f"✅ Paket {jenis} dibuat: {path_zip.relative_to(ROOT)}")
    print(f"   Kode lisensi: {kode}")
    print(f"   Skill: {', '.join(s['id'] for s in pilihan)}")


if __name__ == "__main__":
    main()
