#!/usr/bin/env python3
"""Ekspor penempatan ke CSV siap salin; tidak menghasilkan .fet valid (gunakan FET manual)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from susun_jadwal import susun  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--output", required=True, help="Path berkas CSV keluaran")
    args = ap.parse_args()
    path = Path(args.json)
    if not path.is_file():
        print(json.dumps({"ok": False, "errors": ["berkas JSON tidak ditemukan"]}, ensure_ascii=False))
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "errors": [f"JSON tidak valid: {e.msg}"]}, ensure_ascii=False))
        return 1
    hasil = susun(data)
    if hasil.get("errors"):
        print(json.dumps({"ok": False, "errors": hasil["errors"]}, ensure_ascii=False))
        return 1
    out_path = Path(args.output)
    if out_path.suffix.lower() != ".csv":
        out_path = out_path.with_suffix(".csv")
    lines = ["hari;jam;kelas;mapel;guru;ruang"]
    for p in hasil.get("penempatan") or []:
        lines.append(
            f"{p['hari']};{p['jam']};{p['kelas']};{p['mapel']};{p['guru']};{p.get('ruang') or ''}"
        )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    out = {
        "ok": hasil.get("ok", False),
        "csv": out_path.name,
        "jp_terjadwal": hasil.get("jp_terjadwal"),
        "catatan": "CSV siap impor manual; file .fet asli harus dibuat di aplikasi FET (panduan references/panduan-fet.md).",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if hasil.get("ok") and not hasil.get("bentrok") else 1


if __name__ == "__main__":
    sys.exit(main())
