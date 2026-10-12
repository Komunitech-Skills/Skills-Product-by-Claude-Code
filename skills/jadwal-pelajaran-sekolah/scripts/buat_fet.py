#!/usr/bin/env python3
"""Ekspor penempatan ke CSV siap FET/manual; stub XML petunjuk (bukan file FET penuh)."""
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
    ap.add_argument("--output", required=True, help="Prefix path tanpa ekstensi")
    args = ap.parse_args()
    data = json.loads(Path(args.json).read_text(encoding="utf-8"))
    hasil = susun(data)
    base = Path(args.output)
    csv_path = base.with_suffix(".csv")
    lines = ["hari;jam;kelas;mapel;guru"]
    for p in hasil.get("penempatan") or []:
        lines.append(
            f"{p['hari']};{p['jam']};{p['kelas']};{p['mapel']};{p['guru']}"
        )
    csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    stub = base.with_suffix(".fet.txt")
    stub.write_text(
        "Berkas ini bukan .fet valid — gunakan CSV di impor manual atau buat .fet di FET "
        "(lihat references/panduan-fet.md). Software FET: AGPL, unduh dari situs resmi lalescu.ro.\n",
        encoding="utf-8",
    )
    out = {
        "ok": hasil.get("ok", False),
        "csv": str(csv_path.name),
        "catatan_fet": str(stub.name),
        "jp_terjadwal": hasil.get("jp_terjadwal"),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if hasil.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
