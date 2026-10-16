#!/usr/bin/env python3
"""Pra-cek rilis: periksa kelengkapan skill calon rilis SEBELUM `scripts/rilis_batch.py --terapkan`.

Hanya membaca. Memeriksa, per skill berstatus `beta` (default) yang tidak ada di koordinasi/beta-tunda.txt:
  SKILL   frontmatter hanya name+description, name = nama folder, description 40–1024 karakter,
          tanpa placeholder khusus platform ({baseDir}, metadata.openclaw), SKILL.md ≤ 400 baris,
          tidak merujuk skill berstatus arsip
  README  ada H1, blok "Hasil uji", bagian instalasi, FAQ, kata "sebelum" (sebelum/sesudah),
          H1 sama persis dengan judul_jualan di promosi/sebelum-sesudah.jsonl bila barisnya ada,
          tidak merujuk skill arsip
  EX      folder examples/ berisi HASIL-UJI.md, berkas 00-* (pembanding / sebelum-sesudah), ≥ 3 contoh 01–05
  LIS     LICENSE / LICENSE.md / LICENSE.txt / ATTRIBUTION.md ada (wajib untuk jalur kurasi)
  KAT     sumber_url terisi untuk kurasi, platform_teruji terisi, skor_kualitas ≥ 7, versi X.Y.Z,
          tier & harga usulan terisi, tier_final berbayar punya harga_final
  PROMO   ada baris di promosi/sebelum-sesudah.jsonl (PERINGATAN saja: tidak menghalangi rilis,
          skill tanpa bukti sebelum/sesudah tetap bisa rilis tetapi tidak tampil di halaman promosi)
  PY      semua *.py di folder skill bisa dikompilasi
  RAHASIA pola token bot Telegram / kunci API di berkas teks (termasuk README)
  ENC     berkas teks bukan UTF-8

Pakai:
    python3 scripts/pracek_rilis.py                 # semua calon rilis (status beta, di luar beta-tunda)
    python3 scripts/pracek_rilis.py --status rilis  # audit ulang skill yang sudah rilis
    python3 scripts/pracek_rilis.py --skill a,b     # hanya skill tertentu
    python3 scripts/pracek_rilis.py --json          # keluaran JSON (untuk skrip lain)
Kode keluar 0 bila tanpa celah penghalang (peringatan PROMO tidak dihitung), 1 bila ada celah penghalang, 2 bila galat input.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"\b\d{9,10}:[A-Za-z0-9_-]{35}\b|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}")
EKS_TEKS = {".md", ".py", ".txt", ".csv", ".json"}
LISENSI = ("LICENSE", "LICENSE.md", "LICENSE.txt", "ATTRIBUTION.md")
PERINGATAN = {"PROMO"}  # jenis celah yang hanya diperingatkan, tidak menghalangi rilis


def baca_katalog(root: Path) -> list[dict]:
    with open(root / "catalog.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def baca_tunda(root: Path) -> set[str]:
    p = root / "koordinasi" / "beta-tunda.txt"
    if not p.exists():
        return set()
    hasil = set()
    for ln in p.read_text(encoding="utf-8").splitlines():
        ln = ln.split("#", 1)[0].strip()
        if ln:
            hasil.add(ln)
    return hasil


def baca_jsonl(root: Path) -> dict[str, dict]:
    p = root / "promosi" / "sebelum-sesudah.jsonl"
    if not p.exists():
        return {}
    hasil = {}
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            d = json.loads(ln)
            hasil[d["nama"]] = d
    return hasil


def rujuk_arsip(teks: str, arsip: set[str], diri: str) -> list[str]:
    return sorted(a for a in arsip if a != diri and re.search(rf"`{re.escape(a)}`|\b{re.escape(a)}\b", teks))


def periksa_skill(root: Path, r: dict, arsip: set[str], jsonl: dict[str, dict]) -> list[str]:
    """Kembalikan daftar celah 'JENIS: keterangan' untuk satu baris katalog."""
    s = r["nama"]
    d = root / "skills" / s
    celah: list[str] = []
    add = lambda k, m: celah.append(f"{k}: {m}")  # noqa: E731

    sk = d / "SKILL.md"
    if not sk.exists():
        add("SKILL", "SKILL.md tidak ada")
        return celah
    t = sk.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        add("SKILL", "frontmatter tidak ada")
    else:
        fm = m.group(1)
        keys = [ln.split(":")[0].strip() for ln in fm.splitlines() if ln and not ln.startswith(" ")]
        if set(keys) != {"name", "description"}:
            add("SKILL", f"frontmatter field {keys} (harus hanya name & description)")
        nm = re.search(r"^name:\s*(.+)$", fm, re.M)
        if not nm or nm.group(1).strip() != s:
            add("SKILL", "name ≠ nama folder")
        ds = re.search(r"^description:\s*(.+)$", fm, re.M)
        if not ds or not (40 <= len(ds.group(1)) <= 1024):
            add("SKILL", "description kosong, terlalu pendek (< 40), atau terlalu panjang (> 1024)")
    if "{baseDir}" in t or "metadata.openclaw" in t:
        add("SKILL", "placeholder/field khusus platform")
    if len(t.splitlines()) > 400:
        add("SKILL", f"{len(t.splitlines())} baris (> 400)")
    for a in rujuk_arsip(t, arsip, s):
        add("SKILL", f"merujuk skill arsip {a}")

    rd = d / "README.md"
    if not rd.exists():
        add("README", "README.md tidak ada")
    else:
        u = rd.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", u, re.M)
        if not h1:
            add("README", "tanpa H1")
        elif s in jsonl and jsonl[s].get("judul_jualan", "").strip() != h1.group(1).strip():
            add("README", f"H1 ≠ judul_jualan jsonl ({h1.group(1).strip()[:40]!r} vs {jsonl[s].get('judul_jualan', '')[:40]!r})")
        if not re.search(r"hasil uji", u, re.I):
            add("README", 'tanpa blok "Hasil uji"')
        if not re.search(r"instalasi", u, re.I):
            add("README", "tanpa bagian instalasi")
        if not re.search(r"\bFAQ\b|Pertanyaan (yang )?sering", u, re.I):
            add("README", "tanpa FAQ")
        if not re.search(r"sebelum", u, re.I):
            add("README", "tanpa sebelum/sesudah")
        for a in rujuk_arsip(u, arsip, s):
            add("README", f"merujuk skill arsip {a}")

    ex = d / "examples"
    if not ex.is_dir():
        add("EX", "folder examples tidak ada")
    else:
        names = {p.name for p in ex.iterdir()}
        if "HASIL-UJI.md" not in names:
            add("EX", "HASIL-UJI.md tidak ada")
        if not any(n.startswith("00-") for n in names):
            add("EX", "tanpa berkas 00- (pembanding / sebelum-sesudah)")
        if len([n for n in names if re.match(r"0[1-5]", n)]) < 3:
            add("EX", "contoh skenario 01–05 kurang dari 3")

    if not any((d / nama).exists() for nama in LISENSI):
        add("LIS", "tanpa LICENSE/ATTRIBUTION.md" + (" (jalur kurasi!)" if r.get("jalur") == "kurasi" else ""))

    if r.get("jalur") == "kurasi" and not r.get("sumber_url", "").strip():
        add("KAT", "kurasi tanpa sumber_url")
    if not r.get("platform_teruji", "").strip():
        add("KAT", "platform_teruji kosong")
    try:
        if float(r.get("skor_kualitas", "").replace(",", ".")) < 7:
            add("KAT", f"skor {r['skor_kualitas']} < 7")
    except ValueError:
        add("KAT", f"skor tidak valid {r.get('skor_kualitas')!r}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", r.get("versi", "")):
        add("KAT", f"versi {r.get('versi')!r} bukan X.Y.Z")
    if not r.get("tier_usulan") or not r.get("harga_usulan_idr"):
        add("KAT", "tier/harga usulan kosong")
    if r.get("tier_final") and r["tier_final"] != "gratis" and not r.get("harga_final_idr"):
        add("KAT", "tier_final berbayar tanpa harga_final")

    if s not in jsonl:
        add("PROMO", "tanpa baris promosi jsonl")

    for p in sorted(d.rglob("*.py")):
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
        except Exception as e:  # noqa: BLE001
            add("PY", f"{p.relative_to(d)} gagal kompilasi: {type(e).__name__}")
    for p in sorted(d.rglob("*")):
        if p.is_file() and p.suffix in EKS_TEKS and p.stat().st_size < 2_000_000:
            try:
                x = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                add("ENC", f"{p.relative_to(d)} bukan UTF-8")
                continue
            if TOKEN.search(x):
                add("RAHASIA", f"{p.relative_to(d)} memuat pola token/kunci")
    return celah


def periksa(root: Path, status: str = "beta", skill: set[str] | None = None, abaikan_tunda: bool = False) -> dict:
    kat = baca_katalog(root)
    tunda = set() if abaikan_tunda else baca_tunda(root)
    arsip = {r["nama"] for r in kat if r["status"] == "arsip"}
    jsonl = baca_jsonl(root)
    calon = [r for r in kat if r["status"] == status and r["nama"] not in tunda and (not skill or r["nama"] in skill)]
    celah = {}
    for r in calon:
        c = periksa_skill(root, r, arsip, jsonl)
        if c:
            celah[r["nama"]] = c
    per_jenis: dict[str, int] = {}
    for L in celah.values():
        for m in L:
            k = m.split(":", 1)[0]
            per_jenis[k] = per_jenis.get(k, 0) + 1
    penghalang = {s: [m for m in L if m.split(":", 1)[0] not in PERINGATAN] for s, L in celah.items()}
    penghalang = {s: L for s, L in penghalang.items() if L}
    return {"status": status, "calon": [r["nama"] for r in calon], "ditunda": sorted(tunda), "celah": celah,
            "per_jenis": per_jenis, "penghalang": sorted(penghalang)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Pra-cek kelengkapan skill calon rilis (hanya membaca).")
    ap.add_argument("--status", default="beta", help="status katalog yang diperiksa (default: beta)")
    ap.add_argument("--skill", help="batasi ke nama skill tertentu, dipisah koma")
    ap.add_argument("--abaikan-tunda", action="store_true", help="ikut periksa skill di koordinasi/beta-tunda.txt")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    ap.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    root = Path(a.root)
    if not (root / "catalog.csv").exists():
        print(f"catalog.csv tidak ditemukan di {root}", file=sys.stderr)
        return 2
    skill = {x.strip() for x in a.skill.split(",") if x.strip()} if a.skill else None
    h = periksa(root, a.status, skill, a.abaikan_tunda)
    if a.json:
        print(json.dumps(h, ensure_ascii=False, indent=1))
    else:
        print(f"calon ({h['status']}): {len(h['calon'])} | ditunda: {len(h['ditunda'])} | skill dengan celah: {len(h['celah'])}")
        if h["per_jenis"]:
            print("per jenis:", ", ".join(f"{k}={v}" for k, v in sorted(h["per_jenis"].items())))
        for s in sorted(h["celah"]):
            print(f"- {s}: " + " | ".join(h["celah"][s]))
        if h["penghalang"]:
            print(f"❌ {len(h['penghalang'])} skill punya celah penghalang — perbaiki sebelum rilis_batch.py --terapkan")
        elif h["celah"]:
            print("⚠️ hanya peringatan (tidak menghalangi rilis)")
        else:
            print("✅ tanpa celah")
    return 1 if h["penghalang"] else 0


if __name__ == "__main__":
    sys.exit(main())
