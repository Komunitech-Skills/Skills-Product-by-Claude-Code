#!/usr/bin/env python3
"""Validasi JSON kebutuhan jadwal sekolah."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validasi(data: dict) -> tuple[bool, list[str], dict]:
    errors: list[str] = []
    hari = data.get("hari") or ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    if not isinstance(hari, list) or not hari:
        errors.append("hari harus daftar non-kosong")
        hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    jam = int(data.get("jam_per_hari") or 6)
    if jam < 1 or jam > 12:
        errors.append("jam_per_hari harus 1–12")
    kegiatan = data.get("kegiatan") or []
    if not isinstance(kegiatan, list) or not kegiatan:
        errors.append("kegiatan wajib berisi minimal 1 baris")
    jp_total = 0
    for i, k in enumerate(kegiatan):
        if not isinstance(k, dict):
            errors.append(f"kegiatan[{i}] bukan objek")
            continue
        for fld in ("guru", "kelas", "mapel"):
            if not str(k.get(fld) or "").strip():
                errors.append(f"kegiatan[{i}] {fld} kosong")
        try:
            jp = int(k.get("jp") or 0)
        except (TypeError, ValueError):
            jp = 0
            errors.append(f"kegiatan[{i}] jp bukan angka")
        if jp < 1:
            errors.append(f"kegiatan[{i}] jp minimal 1")
        jp_total += max(jp, 0)
    jumat_pendek = int(data.get("jumat_kurangi_slot") or 0)
    if jumat_pendek < 0 or jumat_pendek > jam:
        errors.append("jumat_kurangi_slot tidak valid")
    slot_per_hari = {d: jam for d in hari}
    if "Jumat" in hari and jumat_pendek:
        slot_per_hari["Jumat"] = max(1, jam - jumat_pendek)
    kapasitas = sum(slot_per_hari.values())
    meta = {
        "jp_total_diminta": jp_total,
        "kapasitas_slot": kapasitas,
        "jumlah_kegiatan": len(kegiatan),
    }
    ok = not errors
    return ok, errors, meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, help="Berkas JSON input")
    args = ap.parse_args()
    raw = Path(args.json).read_text(encoding="utf-8")
    data = json.loads(raw)
    ok, errors, meta = validasi(data)
    out = {"ok": ok, "errors": errors, **meta}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
