#!/usr/bin/env python3
"""Regresi validasi_input.py dan susun_jadwal.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return p.returncode, p.stdout + p.stderr


def test_valid_ok() -> None:
    data = {
        "hari": ["Senin", "Selasa"],
        "jam_per_hari": 4,
        "kegiatan": [
            {"guru": "Bu Ana", "kelas": "7A", "mapel": "Matematika", "jp": 2},
            {"guru": "Pak Ben", "kelas": "7A", "mapel": "IPA", "jp": 2},
        ],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "validasi_input.py"), "--json", path])
    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] and body["jp_total_diminta"] == 4


def test_valid_guru_kosong() -> None:
    data = {"kegiatan": [{"guru": "", "kelas": "7A", "mapel": "MTK", "jp": 1}]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "validasi_input.py"), "--json", path])
    assert code == 1, out


def test_valid_jp_pecahan() -> None:
    data = {"kegiatan": [{"guru": "Bu Ana", "kelas": "7A", "mapel": "MTK", "jp": 2.5}]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    code, _ = run(["python3", str(SCRIPTS / "validasi_input.py"), "--json", path])
    assert code == 1


def test_valid_jam_bukan_angka() -> None:
    data = {
        "jam_per_hari": "enam",
        "kegiatan": [{"guru": "Bu Ana", "kelas": "7A", "mapel": "MTK", "jp": 1}],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    code, _ = run(["python3", str(SCRIPTS / "validasi_input.py"), "--json", path])
    assert code == 1


def test_susun_tanpa_bentrok() -> None:
    data = {
        "hari": ["Senin", "Selasa", "Rabu"],
        "jam_per_hari": 3,
        "kegiatan": [
            {"guru": "Bu Ana", "kelas": "7A", "mapel": "Matematika", "jp": 3},
            {"guru": "Pak Ben", "kelas": "7B", "mapel": "IPA", "jp": 3},
        ],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "susun_jadwal.py"), "--json", path])
    assert code == 0, out
    body = json.loads(out)
    assert body["jp_terjadwal"] == 6
    assert not body["bentrok"]
    assert body["belum_terpenuhi"] == []


def test_susun_kapasitas_kurang() -> None:
    data = {
        "hari": ["Senin"],
        "jam_per_hari": 2,
        "kegiatan": [{"guru": "Bu Ana", "kelas": "7A", "mapel": "MTK", "jp": 5}],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "susun_jadwal.py"), "--json", path])
    body = json.loads(out)
    assert body["jp_terjadwal"] == 2
    assert body["belum_terpenuhi"][0]["jp_belum"] == 3
    assert code == 2


def test_ketersediaan_guru() -> None:
    data = {
        "hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
        "jam_per_hari": 4,
        "ketersediaan_guru": {"Pak Budi": ["Selasa", "Kamis"]},
        "kegiatan": [{"guru": "Pak Budi", "kelas": "8A", "mapel": "IPA", "jp": 4, "ruang": "Lab IPA"}],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "susun_jadwal.py"), "--json", path])
    assert code == 0, out
    body = json.loads(out)
    assert body["jp_terjadwal"] == 4
    for p in body["penempatan"]:
        assert p["hari"] in ("Selasa", "Kamis")


def test_maks_dua_jp_per_hari_per_mapel() -> None:
    data = {
        "hari": ["Senin", "Selasa", "Rabu"],
        "jam_per_hari": 6,
        "kegiatan": [{"guru": "Bu Ana", "kelas": "7A", "mapel": "Matematika", "jp": 6}],
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = f.name
    _, out = run(["python3", str(SCRIPTS / "susun_jadwal.py"), "--json", path])
    body = json.loads(out)
    from collections import Counter

    per_day = Counter((p["kelas"], p["mapel"], p["hari"]) for p in body["penempatan"])
    assert all(v <= 2 for v in per_day.values())


def main() -> int:
    test_valid_ok()
    test_valid_guru_kosong()
    test_valid_jp_pecahan()
    test_valid_jam_bukan_angka()
    test_susun_tanpa_bentrok()
    test_susun_kapasitas_kurang()
    test_ketersediaan_guru()
    test_maks_dua_jp_per_hari_per_mapel()
    print("OK: 8 tes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
