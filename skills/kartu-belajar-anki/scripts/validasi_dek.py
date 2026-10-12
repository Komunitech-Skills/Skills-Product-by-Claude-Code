#!/usr/bin/env python3
"""Validasi berkas TSV kartu untuk impor Anki (tab-separated)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CLOZE_RE = re.compile(r"\{\{c\d+::.+?\}\}", re.DOTALL)
MAX_FIELD = 8000


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validasi deck TSV untuk Anki")
    p.add_argument("--input", required=True, help="Path berkas .tsv")
    return p.parse_args()


def validate_line(line: str, lineno: int) -> list[str]:
    err: list[str] = []
    if line.startswith("#"):
        return err
    if not line.strip():
        return err
    if "\t" not in line:
        err.append(f"Baris {lineno}: pemisah harus tab (\\t), bukan koma saja")
        return err
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 2:
        err.append(f"Baris {lineno}: minimal 2 kolom (depan, belakang)")
        return err
    front, back = parts[0], parts[1]
    for i, field in enumerate(parts[:3]):
        if len(field) > MAX_FIELD:
            err.append(f"Baris {lineno}: kolom {i + 1} terlalu panjang (>{MAX_FIELD})")
        if "\r" in field:
            err.append(f"Baris {lineno}: kolom {i + 1} mengandung carriage return")
    if "{{c" in front and not CLOZE_RE.search(front):
        err.append(f"Baris {lineno}: cloze tidak lengkap (harus {{c1::teks}})")
    if not front.strip():
        err.append(f"Baris {lineno}: kolom depan kosong")
    is_cloze = "{{c" in front
    if not is_cloze and not back.strip():
        err.append(f"Baris {lineno}: kolom belakang kosong (bukan cloze)")
    if len(parts) > 3:
        err.append(f"Baris {lineno}: maksimal 3 kolom (depan, belakang, tag)")
    if len(parts) == 3 and parts[2] and " " in parts[2].strip():
        err.append(f"Baris {lineno}: tag sebaiknya satu token tanpa spasi (pakai -)")
    return err


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    if not path.is_file():
        print(json.dumps({"ok": False, "error": "berkas tidak ditemukan"}))
        return 1
    errors: list[str] = []
    count = 0
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.startswith("#") or not line.strip():
            continue
        errors.extend(validate_line(line, lineno))
        count += 1
    out = {"ok": not errors, "jumlah_kartu": count, "errors": errors}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
