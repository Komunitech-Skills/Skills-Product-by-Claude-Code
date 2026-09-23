#!/usr/bin/env python3
"""Validasi format semua skill, catalog.csv, dan bundles/. Keluar dengan kode 1 jika ada masalah.

Pakai `--skill <nama>` (bisa diulang) untuk memvalidasi skill tertentu saja, mis. saat
folder skill lain masih dalam pengerjaan.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CATALOG = ROOT / "catalog.csv"
BUNDLES_DIR = ROOT / "bundles"

KOLOM = ["nama", "kategori", "jalur", "sumber_url", "lisensi", "skor_kualitas", "tier_usulan",
         "harga_usulan_idr", "tier_final", "harga_final_idr", "versi", "platform_teruji",
         "status", "tanggal_update"]
JALUR = {"kurasi", "orisinal"}
TIER = {"gratis", "ecer", "vip"}
STATUS = {"ide", "draft", "uji", "lulus", "beta", "rilis", "ditolak", "arsip"}
STATUS_TANPA_FOLDER = {"ide", "ditolak"}
STATUS_SUDAH_UJI = {"lulus", "beta", "rilis"}

POLA_NAMA = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
POLA_VERSI = re.compile(r"^\d+\.\d+\.\d+$")
POLA_TANGGAL = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Pola yang tidak boleh ada di file skill: rahasia & fitur khusus satu platform
POLA_TERLARANG = [
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"), "mirip API key/token"),
    (re.compile(r"\{baseDir\}"), "placeholder {baseDir} khusus OpenClaw"),
    (re.compile(r"curl[^\n|]*\|\s*(ba)?sh"), "pola 'curl | sh'"),
]


def baca_frontmatter(path):
    """Kembalikan (dict frontmatter, sisa isi) atau raise ValueError."""
    teks = path.read_text(encoding="utf-8")
    if not teks.startswith("---\n"):
        raise ValueError("harus diawali frontmatter '---'")
    akhir = teks.find("\n---", 4)
    if akhir == -1:
        raise ValueError("frontmatter tidak ditutup dengan '---'")
    data = {}
    for no, baris in enumerate(teks[4:akhir].splitlines(), start=2):
        if not baris.strip():
            continue
        if ":" not in baris or baris.startswith((" ", "\t")):
            raise ValueError(f"baris {no}: gunakan format 'kunci: nilai' satu baris")
        kunci, nilai = baris.split(":", 1)
        data[kunci.strip()] = nilai.strip()
    return data, teks[akhir + 4:]


def validasi_skill(folder, status):
    n = folder.name
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return [f"{n}: SKILL.md tidak ada"]
    try:
        fm, isi = baca_frontmatter(skill_md)
    except ValueError as e:
        return [f"{n}/SKILL.md: {e}"]

    err = []
    if fm.get("name") != n:
        err.append(f"{n}: 'name' ({fm.get('name')!r}) harus sama dengan nama folder")
    if not POLA_NAMA.match(n) or len(n) > 64:
        err.append(f"{n}: nama folder hanya huruf kecil, angka, '-' dan maks. 64 karakter")
    lain = set(fm) - {"name", "description"}
    if lain:
        err.append(f"{n}: frontmatter hanya boleh 'name' dan 'description' (ada: {sorted(lain)})")
    desk = fm.get("description", "")
    if not 40 <= len(desk) <= 1024:
        err.append(f"{n}: 'description' harus 40–1024 karakter (sekarang {len(desk)})")
    if len(isi.strip()) < 300:
        err.append(f"{n}: isi SKILL.md terlalu sedikit")
    if len(isi.splitlines()) > 500:
        err.append(f"{n}: SKILL.md terlalu panjang (>500 baris); pindahkan detail ke references/")

    if not (folder / "README.md").is_file():
        err.append(f"{n}: README.md (panduan pembeli) tidak ada")
    if not ((folder / "ATTRIBUTION.md").is_file() or (folder / "LICENSE").is_file()):
        err.append(f"{n}: ATTRIBUTION.md atau LICENSE tidak ada")
    if status in STATUS_SUDAH_UJI:
        contoh = folder / "examples"
        if not contoh.is_dir() or not any(contoh.iterdir()):
            err.append(f"{n}: status '{status}' wajib punya hasil uji di examples/")

    for f in folder.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".py", ".txt", ".csv", ".json", ".sh"}:
            teks = f.read_text(encoding="utf-8", errors="ignore")
            for pola, alasan in POLA_TERLARANG:
                if pola.search(teks):
                    err.append(f"{n}: {f.relative_to(folder)} berisi {alasan}")
    return err


def baca_katalog():
    with CATALOG.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if r.fieldnames != KOLOM:
            raise ValueError(f"header harus persis: {','.join(KOLOM)}")
        return list(r)


def validasi_baris(b, no):
    err = []
    label = f"catalog.csv baris {no} ({b['nama'] or '?'})"
    if not POLA_NAMA.match(b["nama"]):
        err.append(f"{label}: 'nama' tidak valid")
    if b["jalur"] not in JALUR:
        err.append(f"{label}: 'jalur' harus {sorted(JALUR)}")
    if b["status"] not in STATUS:
        err.append(f"{label}: 'status' harus {sorted(STATUS)}")
    if b["tier_usulan"] not in TIER:
        err.append(f"{label}: 'tier_usulan' harus {sorted(TIER)}")
    if b["tier_final"] and b["tier_final"] not in TIER:
        err.append(f"{label}: 'tier_final' harus kosong atau {sorted(TIER)}")
    for k in ("harga_usulan_idr", "harga_final_idr"):
        if b[k] and not b[k].isdigit():
            err.append(f"{label}: '{k}' harus angka bulat tanpa titik (mis. 49000)")
    if b["skor_kualitas"] and not (b["skor_kualitas"].isdigit() and 1 <= int(b["skor_kualitas"]) <= 10):
        err.append(f"{label}: 'skor_kualitas' harus 1–10 atau kosong")
    if not POLA_VERSI.match(b["versi"]):
        err.append(f"{label}: 'versi' harus X.Y.Z")
    if not POLA_TANGGAL.match(b["tanggal_update"]):
        err.append(f"{label}: 'tanggal_update' harus YYYY-MM-DD")
    if b["jalur"] == "kurasi" and not (b["sumber_url"] and b["lisensi"]):
        err.append(f"{label}: skill kurasi wajib mengisi 'sumber_url' dan 'lisensi'")
    if b["status"] in STATUS_SUDAH_UJI:
        if not b["skor_kualitas"] or int(b["skor_kualitas"] or 0) < 7:
            err.append(f"{label}: status '{b['status']}' butuh skor_kualitas >= 7")
        if not b["platform_teruji"]:
            err.append(f"{label}: status '{b['status']}' butuh 'platform_teruji'")
    return err


def main():
    ap = argparse.ArgumentParser(description="Validasi skill & katalog")
    ap.add_argument("--skill", action="append", help="Hanya validasi skill ini (bisa diulang)")
    args = ap.parse_args()
    hanya = set(args.skill or [])
    errors = []
    try:
        katalog = baca_katalog()
    except (OSError, ValueError) as e:
        print(f"❌ catalog.csv: {e}")
        sys.exit(1)

    status = {}
    for no, b in enumerate(katalog, start=2):
        errors += validasi_baris(b, no)
        if b["nama"] in status:
            errors.append(f"catalog.csv: nama duplikat {b['nama']!r}")
        status[b["nama"]] = b["status"]

    folders = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []
    if hanya:
        tidak_ada = hanya - {f.name for f in folders}
        errors += [f"{n}: folder skills/{n} tidak ada" for n in sorted(tidak_ada)]
        folders = [f for f in folders if f.name in hanya]
    for f in folders:
        if f.name not in status:
            errors.append(f"{f.name}: ada di skills/ tapi tidak ada di catalog.csv")
            continue
        errors += validasi_skill(f, status[f.name])
    nama_folder = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()} if SKILLS_DIR.is_dir() else set()
    for nama, st in status.items():
        if st not in STATUS_TANPA_FOLDER and nama not in nama_folder:
            errors.append(f"catalog.csv: '{nama}' berstatus '{st}' tapi folder skills/{nama} tidak ada")

    for bundle in sorted(BUNDLES_DIR.glob("*.txt")) if BUNDLES_DIR.is_dir() else []:
        for s in bundle.read_text(encoding="utf-8").split():
            if s not in status:
                errors.append(f"bundles/{bundle.name}: skill '{s}' tidak ada di catalog.csv")

    if errors:
        print(f"❌ {len(errors)} masalah ditemukan:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"✅ {len(folders)} skill valid, {len(katalog)} baris katalog sesuai.")


if __name__ == "__main__":
    main()
