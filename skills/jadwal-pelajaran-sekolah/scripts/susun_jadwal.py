#!/usr/bin/env python3
"""Penjadwalan backtracking tanpa bentrok; maks 2 JP mapel sama per hari per kelas."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
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


def _guru_hari_ok(guru: str, hari: str, ketersediaan: dict) -> bool:
    if not ketersediaan:
        return True
    allowed = ketersediaan.get(guru)
    if allowed is None:
        return True
    if not isinstance(allowed, list):
        return True
    return hari in allowed


def _can_place(
    h: str,
    j: int,
    act: dict,
    penempatan: list[dict],
    ketersediaan: dict,
    max_per_day: int,
) -> bool:
    guru, kelas, mapel = act["guru"], act["kelas"], act["mapel"]
    ruang = (act.get("ruang") or "").strip()

    if not _guru_hari_ok(guru, h, ketersediaan):
        return False

    for p in penempatan:
        if p["hari"] == h and p["jam"] == j:
            if p["guru"] == guru or p["kelas"] == kelas:
                return False
            pr = (p.get("ruang") or "").strip()
            if ruang and pr == ruang:
                return False

    same_day = sum(
        1 for p in penempatan if p["kelas"] == kelas and p["mapel"] == mapel and p["hari"] == h
    )
    if same_day >= max_per_day:
        return False
    return True


def _backtrack(
    acts: list[dict],
    idx: int,
    slots: list[tuple[str, int]],
    penempatan: list[dict],
    ketersediaan: dict,
    max_per_day: int,
) -> bool:
    if idx >= len(acts):
        return True
    act = acts[idx]
    if act["sisa"] == 0:
        return _backtrack(acts, idx + 1, slots, penempatan, ketersediaan, max_per_day)
    for h, j in slots:
        if not _can_place(h, j, act, penempatan, ketersediaan, max_per_day):
            continue
        penempatan.append(
            {
                "hari": h,
                "jam": j,
                "guru": act["guru"],
                "kelas": act["kelas"],
                "mapel": act["mapel"],
                "ruang": act.get("ruang") or "",
            }
        )
        act["sisa"] -= 1
        if _backtrack(acts, idx, slots, penempatan, ketersediaan, max_per_day):
            return True
        act["sisa"] += 1
        penempatan.pop()
    return _backtrack(acts, idx + 1, slots, penempatan, ketersediaan, max_per_day)


def susun(data: dict, max_jp_mapel_per_hari: int = 2) -> dict:
    ok, errors, meta = validasi(data)
    if not ok:
        return {"ok": False, "errors": errors, "penempatan": [], "belum_terpenuhi": []}

    slots = slot_list(data)
    ketersediaan = data.get("ketersediaan_guru") or {}
    if not isinstance(ketersediaan, dict):
        ketersediaan = {}

    kegiatan = []
    for k in data.get("kegiatan") or []:
        kegiatan.append(
            {
                "guru": str(k["guru"]).strip(),
                "kelas": str(k["kelas"]).strip(),
                "mapel": str(k["mapel"]).strip(),
                "jp": int(k["jp"]),
                "sisa": int(k["jp"]),
                "ruang": str(k.get("ruang") or "").strip(),
            }
        )
    kegiatan.sort(key=lambda x: (-x["jp"], x["guru"], x["kelas"]))

    penempatan: list[dict] = []
    _backtrack(kegiatan, 0, slots, penempatan, ketersediaan, max_jp_mapel_per_hari)

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
    ruang_seen: dict[tuple[str, int], str] = {}
    per_day: dict[tuple[str, str, str], int] = defaultdict(int)
    for p in penempatan:
        g = (p["hari"], p["jam"], p["guru"])
        c = (p["hari"], p["jam"], p["kelas"])
        if g in guru_seen or c in kelas_seen:
            return True
        guru_seen.add(g)
        kelas_seen.add(c)
        ruang = (p.get("ruang") or "").strip()
        if ruang:
            key = (p["hari"], p["jam"])
            if key in ruang_seen and ruang_seen[key] != ruang:
                return True
            ruang_seen[key] = ruang
        per_day[(p["kelas"], p["mapel"], p["hari"])] += 1
        if per_day[(p["kelas"], p["mapel"], p["hari"])] > 2:
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    args = ap.parse_args()
    path = Path(args.json)
    if not path.is_file():
        print(json.dumps({"ok": False, "errors": ["berkas JSON tidak ditemukan"]}, ensure_ascii=False))
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(
            json.dumps(
                {"ok": False, "errors": [f"JSON tidak valid: {e.msg}"]},
                ensure_ascii=False,
            )
        )
        return 1
    out = susun(data)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not out.get("ok") and out.get("errors"):
        return 1
    if out.get("bentrok"):
        return 1
    if out.get("belum_terpenuhi"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
