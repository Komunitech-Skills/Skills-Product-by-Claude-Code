#!/usr/bin/env python3
"""Bersihkan draf kasar & deteksi jenis dokumen (Python standar)."""
from __future__ import annotations

import argparse
import re
import sys

_META = re.compile(
    r"^(tentu!|baik!|berikut (ini )?|sure!|here'?s|as an ai)[^\n]*$",
    re.I | re.M,
)
_BLANK3 = re.compile(r"\n{3,}")

_KATA = {
    "notulen": ("notulen", "rapat", "meeting", "mom", "agenda rapat", "tindak lanjut"),
    "laporan": ("laporan", "rekap", "evaluasi", "temuan", "bulanan", "triwulan"),
    "surat": ("surat", "yth", "dengan hormat", "permohonan", "undangan", "pemberitahuan"),
    "proposal": ("proposal", "penawaran kerja sama", "kemitraan", "sponsorship"),
    "memo": ("memo", "pengumuman internal", "kepada seluruh", "kepada staf"),
}


def bersihkan(teks: str) -> str:
    t = teks.replace("\r\n", "\n").strip()
    t = _META.sub("", t)
    t = _BLANK3.sub("\n\n", t)
    lines = []
    for line in t.split("\n"):
        s = line.strip()
        if s.startswith("- ") and not s.startswith("- [ ]"):
            lines.append(s)
        else:
            lines.append(line.rstrip())
    return "\n".join(lines).strip()


def deteksi_jenis(teks: str) -> str:
    low = teks.lower()
    skor = {k: 0 for k in _KATA}
    for jenis, kata in _KATA.items():
        for k in kata:
            if k in low:
                skor[jenis] += 1
    best = max(skor, key=skor.get)
    if skor[best] == 0:
        return "umum"
    return best


def main() -> int:
    p = argparse.ArgumentParser(description="Rapikan draf & deteksi jenis dokumen")
    p.add_argument("--jenis", default="auto", choices=["auto", *list(_KATA.keys()), "umum"])
    p.add_argument("--stdin", action="store_true")
    p.add_argument("file", nargs="?")
    args = p.parse_args()
    if args.stdin:
        raw = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                raw = f.read()
        except OSError as e:
            print(f"GAGAL: {e}", file=sys.stderr)
            return 1
    else:
        print("GAGAL: beri file atau --stdin", file=sys.stderr)
        return 1
    if not raw.strip():
        print("GAGAL: draf kosong", file=sys.stderr)
        return 1
    bersih = bersihkan(raw)
    jenis = deteksi_jenis(bersih) if args.jenis == "auto" else args.jenis
    print(f"JENIS: {jenis}")
    print("---")
    print(bersih)
    return 0


if __name__ == "__main__":
    sys.exit(main())
