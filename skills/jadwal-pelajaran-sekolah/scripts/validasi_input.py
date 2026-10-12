#!/usr/bin/env python3
"""Validasi JSON kebutuhan jadwal sekolah."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _parse_int(field: str, raw, lo: int | None, hi: int | None) -> tuple[int | None, str | None]:
    if raw is None or raw == "":
        return None, f"{field} wajib angka bulat"
    if isinstance(raw, bool):
        return None, f"{field} bukan angka bulat"
    if isinstance(raw, float) and not raw.is_integer():
        return None, f"{field} harus bilangan bulat (pecahan ditolak)"
    try:
        v = int(raw)
    except (TypeError, ValueError):
        return None, f"{field} bukan angka bulat"
    if lo is not None and v < lo:
        return None, f"{field} minimal {lo}"
    if hi is not None and v > hi:
        return None, f"{field} maksimal {hi}"
    return v, None


def validasi(data: dict) -> tuple[bool, list[str], dict]:
    errors: list[str] = []
    hari = data.get("hari") or ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    if not isinstance(hari, list) or not hari:
        errors.append("hari harus daftar non-kosong")
        hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

    jam, err = _parse_int("jam_per_hari", data.get("jam_per_hari", 6), 1, 12)
    if err:
        errors.append(err)
        jam = 6

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
        jp, jerr = _parse_int(f"kegiatan[{i}].jp", k.get("jp"), 1, None)
        if jerr:
            errors.append(jerr)
            jp = 0
        jp_total += jp

    jk_raw = data.get("jumat_kurangi_slot", 0)
    jumat_pendek, jerr = _parse_int("jumat_kurangi_slot", jk_raw, 0, jam or 12)
    if jerr:
        errors.append(jerr)
        jumat_pendek = 0
    elif jam is not None and jumat_pendek > jam:
        errors.append("jumat_kurangi_slot tidak valid")

    ketersediaan = data.get("ketersediaan_guru") or {}
    if ketersediaan and not isinstance(ketersediaan, dict):
        errors.append("ketersediaan_guru harus objek {nama_guru: [hari,...]}")

    slot_per_hari = {d: jam or 6 for d in hari}
    if "Jumat" in hari and jumat_pendek:
        slot_per_hari["Jumat"] = max(1, (jam or 6) - jumat_pendek)
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
    path = Path(args.json)
    if not path.is_file():
        print(json.dumps({"ok": False, "errors": ["berkas JSON tidak ditemukan"]}, ensure_ascii=False))
        return 1
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(
            json.dumps(
                {"ok": False, "errors": [f"JSON tidak valid: {e.msg} (baris {e.lineno})"]},
                ensure_ascii=False,
            )
        )
        return 1
    except OSError as e:
        print(json.dumps({"ok": False, "errors": [f"tidak bisa membaca berkas: {e}"]}, ensure_ascii=False))
        return 1
    if not isinstance(data, dict):
        print(json.dumps({"ok": False, "errors": ["akar JSON harus objek"]}, ensure_ascii=False))
        return 1
    ok, errors, meta = validasi(data)
    out = {"ok": ok, "errors": errors, **meta}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
