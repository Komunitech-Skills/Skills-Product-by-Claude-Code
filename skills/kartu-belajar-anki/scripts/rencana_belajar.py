#!/usr/bin/env python3
"""Rencana belajar sederhana untuk deck kartu (Anki-style new cards per day)."""
from __future__ import annotations

import argparse
import json
import math
import sys


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Hitung rencana belajar harian")
    p.add_argument("--kartu", type=int, required=True, help="Jumlah kartu total")
    p.add_argument("--menit", type=int, default=20, help="Menit belajar per hari")
    p.add_argument("--baru-per-hari", type=int, default=15, help="Kartu baru maks per hari")
    p.add_argument("--menit-per-kartu-baru", type=float, default=1.2, help="Estimasi menit per kartu baru")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.kartu < 1:
        print(json.dumps({"ok": False, "error": "kartu minimal 1"}))
        return 1
    warnings: list[str] = []
    if args.menit <= 0:
        warnings.append(
            "Menit belajar 0 — rencana hanya perkiraan; set minimal 10–20 menit per hari agar realistis"
        )
    menit_efektif = max(1, args.menit)
    baru = max(1, min(args.baru_per_hari, args.kartu))
    kapasitas = max(1, int(menit_efektif / args.menit_per_kartu_baru))
    if kapasitas < baru:
        baru = kapasitas
    hari_baru = int(math.ceil(args.kartu / baru))
    out = {
        "ok": True,
        "jumlah_kartu": args.kartu,
        "kartu_baru_per_hari": baru,
        "hari_selesai_kartu_baru": hari_baru,
        "menit_per_hari_disarankan": args.menit,
        "peringatan": warnings,
        "catatan": (
            f"Hari 1–{hari_baru}: pelajari {baru} kartu baru per hari; "
            f"setelah hari 1, sisihkan ±5–10 menit review kartu kemarin (Anki otomatis bila dipakai). "
            f"Perkiraan total kartu baru selesai dalam {hari_baru} hari belajar."
        ),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
