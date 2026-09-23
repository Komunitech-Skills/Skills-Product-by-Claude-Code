#!/usr/bin/env python3
"""Validasi format semua skill dan kesesuaiannya dengan catalog.json."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CATALOG = ROOT / "catalog.json"

POLA_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
POLA_VERSI = re.compile(r"^\d+\.\d+\.\d+$")
STATUS_VALID = {"draft", "rilis", "arsip"}
KOLOM_KATALOG = {
    "id": str, "nama": str, "ringkasan": str, "kategori": str, "versi": str,
    "status": str, "tersedia_ecer": bool, "harga_ecer": int, "vip_eksklusif": bool,
    "platform": list,
}


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


def validasi_skill(folder):
    err = []
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return [f"{folder.name}: SKILL.md tidak ada"]
    try:
        fm, isi = baca_frontmatter(skill_md)
    except ValueError as e:
        return [f"{folder.name}/SKILL.md: {e}"]

    nama = fm.get("name", "")
    if nama != folder.name:
        err.append(f"{folder.name}: 'name' ({nama!r}) harus sama dengan nama folder")
    if not POLA_ID.match(folder.name):
        err.append(f"{folder.name}: nama folder hanya boleh huruf kecil, angka, dan '-'")
    desk = fm.get("description", "")
    if len(desk) < 40:
        err.append(f"{folder.name}: 'description' terlalu pendek (min. 40 karakter)")
    if len(desk) > 1024:
        err.append(f"{folder.name}: 'description' terlalu panjang (maks. 1024 karakter)")
    if "metadata" in fm:
        try:
            meta = json.loads(fm["metadata"])
            if not isinstance(meta, dict):
                raise ValueError
        except ValueError:
            err.append(f"{folder.name}: 'metadata' harus JSON objek dalam satu baris")
    if len(isi.strip()) < 100:
        err.append(f"{folder.name}: isi SKILL.md terlalu sedikit")
    return err


def validasi_katalog(folder_skill):
    err = []
    try:
        katalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [f"catalog.json: {e}"]

    ids = []
    for i, s in enumerate(katalog.get("skills", [])):
        label = s.get("id", f"#{i}")
        for kunci, tipe in KOLOM_KATALOG.items():
            if kunci not in s:
                err.append(f"catalog.json [{label}]: kolom '{kunci}' tidak ada")
            elif not isinstance(s[kunci], tipe) or (tipe is int and isinstance(s[kunci], bool)):
                err.append(f"catalog.json [{label}]: '{kunci}' harus bertipe {tipe.__name__}")
        if not POLA_VERSI.match(str(s.get("versi", ""))):
            err.append(f"catalog.json [{label}]: 'versi' harus format X.Y.Z")
        if s.get("status") not in STATUS_VALID:
            err.append(f"catalog.json [{label}]: 'status' harus salah satu {sorted(STATUS_VALID)}")
        if s.get("vip_eksklusif") and s.get("tersedia_ecer"):
            err.append(f"catalog.json [{label}]: skill vip_eksklusif tidak boleh tersedia_ecer")
        ids.append(s.get("id"))

    duplikat = {x for x in ids if ids.count(x) > 1}
    for d in sorted(duplikat, key=str):
        err.append(f"catalog.json: id duplikat {d!r}")
    for d in sorted(set(folder_skill) - set(ids)):
        err.append(f"catalog.json: skill '{d}' ada di folder skills/ tapi tidak ada di katalog")
    for d in sorted(set(ids) - set(folder_skill), key=str):
        err.append(f"catalog.json: skill '{d}' ada di katalog tapi foldernya tidak ada")
    return err


def main():
    folders = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []
    errors = []
    for f in folders:
        errors += validasi_skill(f)
    errors += validasi_katalog([f.name for f in folders])

    if errors:
        print(f"❌ {len(errors)} masalah ditemukan:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"✅ {len(folders)} skill valid, katalog sesuai.")


if __name__ == "__main__":
    main()
