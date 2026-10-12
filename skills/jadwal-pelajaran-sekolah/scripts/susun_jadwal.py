#!/usr/bin/env python3
"""Penjadwalan greedy tanpa bentrok guru/kelas."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from validasi_input import validasi  # noqa: E402


def slot_list(data: dict) -> list[tuple[str, int]]:
    hari = data.get("hari") or ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    jam = int(data.get("jam_per_hari") or 6)
    kurang = int(data.get("jumat_kurangi_slot") or 0)
    slots: list[tuple[str, int]] = []
    for d in hari:
        n = jam
        if d == "Jumat" and kurang:
            n = max(1, jam - kurang)
        for j in range(1, n + 1):
            slots.append((d, j))
    return slots


def susun(data: dict) -> dict:
    ok, errors, meta = validasi(data)
    if not ok:
        return {"ok": False, "errors": errors, "penempatan": [], "belum_terpenuhi": []}

    slots = slot_list(data)
    kegiatan = []
    for k in data.get("kegiatan") or []:
        kegiatan.append(
            {
                "guru": str(k["guru"]).strip(),
                "kelas": str(k["kelas"]).strip(),
                "mapel": str(k["mapel"]).strip(),
                "jp": int(k["jp"]),
                "sisa": int(k["jp"]),
            }
        )
    kegiatan.sort(key=lambda x: (-x["jp"], x["guru"], x["kelas"]))

    guru_busy: set[tuple[str, int, str]] = set()
    kelas_busy: set[tuple[str, int, str]] = set()
    penempatan: list[dict] = []

    si = 0
    for act in kegiatan:
        placed = 0
        attempts = 0
        while act["sisa"] > 0 and attempts < len(slots) * 3:
            h, j = slots[si % len(slots)]
            si += 1
            attempts += 1
            gkey = (h, j, act["guru"])
            ckey = (h, j, act["kelas"])
            if gkey in guru_busy or ckey in kelas_busy:
                continue
            guru_busy.add(gkey)
            kelas_busy.add(ckey)
            penempatan.append(
                {
                    "hari": h,
                    "jam": j,
                    "guru": act["guru"],
                    "kelas": act["kelas"],
                    "mapel": act["mapel"],
                }
            )
            act["sisa"] -= 1
            placed += 1
        if act["sisa"] > 0:
            pass

    belum = [
        {
            "guru": a["guru"],
            "kelas": a["kelas"],
            "mapel": a["mapel"],
            "jp_belum": a["sisa"],
        }
        for a in kegiatan
        if a["sisa"] > 0
    ]
    jp_terjadwal = sum(int(k["jp"]) for k in data.get("kegiatan") or []) - sum(
        b["jp_belum"] for b in belum
    )
    bentrok = _cek_bentrok_internal(penempatan)
    return {
        "ok": not bentrok,
        "jp_terjadwal": jp_terjadwal,
        "jp_total_diminta": meta["jp_total_diminta"],
        "kapasitas_slot": meta["kapasitas_slot"],
        "penempatan": sorted(penempatan, key=lambda x: (x["kelas"], x["hari"], x["jam"])),
        "belum_terpenuhi": belum,
        "bentrok": bentrok,
    }


def _cek_bentrok_internal(penempatan: list[dict]) -> bool:
    guru_seen: set[tuple[str, int, str]] = set()
    kelas_seen: set[tuple[str, int, str]] = set()
    for p in penempatan:
        g = (p["hari"], p["jam"], p["guru"])
        c = (p["hari"], p["jam"], p["kelas"])
        if g in guru_seen or c in kelas_seen:
            return True
        guru_seen.add(g)
        kelas_seen.add(c)
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.json).read_text(encoding="utf-8"))
    out = susun(data)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") and not out.get("belum_terpenuhi") else (1 if out.get("bentrok") else 0)


if __name__ == "__main__":
    sys.exit(main())
