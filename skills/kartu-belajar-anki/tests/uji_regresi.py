#!/usr/bin/env python3
"""Regresi validasi_dek.py dan rencana_belajar.py."""
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
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as f:
        f.write("#notetype:Basic\n")
        f.write("Apa FIFO?\tFirst In First Out\tsop-gudang\n")
        f.write("#notetype:Cloze\n")
        f.write("{{c1::FEFO}} dipakai untuk barang kedaluwarsa.\t\tsop-gudang\n")
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "validasi_dek.py"), "--input", path])
    assert code == 0, out
    data = json.loads(out)
    assert data["ok"] and data["jumlah_kartu"] == 2


def test_valid_mixed_without_header() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as f:
        f.write("Apa FIFO?\tFirst In First Out\tsop-gudang\n")
        f.write("{{c1::FEFO}} dipakai.\t\tsop-gudang\n")
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "validasi_dek.py"), "--input", path])
    assert code == 1, out
    data = json.loads(out)
    assert not data["ok"]
    assert any("Campuran" in e for e in data["errors"])


def test_valid_empty() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as f:
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "validasi_dek.py"), "--input", path])
    assert code == 1, out
    data = json.loads(out)
    assert not data["ok"]


def test_rencana_menit_nol() -> None:
    code, out = run(
        [
            "python3",
            str(SCRIPTS / "rencana_belajar.py"),
            "--kartu",
            "10",
            "--menit",
            "0",
            "--baru-per-hari",
            "5",
        ]
    )
    assert code == 0, out
    data = json.loads(out)
    assert data["ok"] and data["peringatan"]


def test_valid_bad_tab() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as f:
        f.write("hanya satu kolom\n")
        path = f.name
    code, out = run(["python3", str(SCRIPTS / "validasi_dek.py"), "--input", path])
    assert code == 1, out
    data = json.loads(out)
    assert not data["ok"] and data["errors"]


def test_rencana() -> None:
    code, out = run(
        [
            "python3",
            str(SCRIPTS / "rencana_belajar.py"),
            "--kartu",
            "30",
            "--menit",
            "20",
            "--baru-per-hari",
            "15",
        ]
    )
    assert code == 0, out
    data = json.loads(out)
    assert data["ok"] and data["hari_selesai_kartu_baru"] == 2


def main() -> int:
    test_valid_ok()
    test_valid_bad_tab()
    test_valid_mixed_without_header()
    test_valid_empty()
    test_rencana()
    test_rencana_menit_nol()
    print("OK: 6 tes regresi kartu-belajar-anki")
    return 0


if __name__ == "__main__":
    sys.exit(main())
