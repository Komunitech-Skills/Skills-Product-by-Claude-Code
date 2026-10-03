#!/usr/bin/env python3
"""Bangun promosi/SEBELUM-SESUDAH.md dari promosi/sebelum-sesudah.jsonl (SSOT).

Skill tampil di daftar promosi bila: verdik terakhir LULUS, skor sesudah >= 8,
selisih >= 1,5 (keputusan pemilik 2026-10-03), dan tidak sedang ditunda (mis. PERLU REVIEW).
Pakai: python3 scripts/promosi_sebelum_sesudah.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "promosi" / "sebelum-sesudah.jsonl"
OUT = ROOT / "promosi" / "SEBELUM-SESUDAH.md"
MIN_SESUDAH, MIN_SELISIH = 8.0, 1.5


def angka(x):
    return f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def tampil(r):
    return (str(r.get("verdik_terakhir", "")).upper().startswith("LULUS")
            and r["skor_sesudah"] >= MIN_SESUDAH
            and r["skor_sesudah"] - r["skor_sebelum"] >= MIN_SELISIH
            and not r.get("tunda_promosi"))


def main():
    rows = [json.loads(l) for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
    for r in rows:
        r["selisih"] = round(r["skor_sesudah"] - r["skor_sebelum"], 2)
    rows.sort(key=lambda r: (-r["selisih"], -r["skor_sesudah"], r["nama"]))
    ok = [r for r in rows if tampil(r)]
    lain = [r for r in rows if not tampil(r)]
    L = ["# Sebelum vs sesudah pakai skill Komunitech", "",
         "Berkas ini DIBUAT OTOMATIS dari `promosi/sebelum-sesudah.jsonl` (SSOT) oleh "
         "`scripts/promosi_sebelum_sesudah.py`. Jangan diedit manual; perbarui data lalu jalankan ulang.", "",
         f"Cara uji & arti skor: lihat [CARA-UJI.md](CARA-UJI.md). Ditampilkan: verdik LULUS, skor dengan skill ≥ {angka(MIN_SESUDAH)}, "
         f"selisih ≥ {angka(MIN_SELISIH)}. Jumlah: **{len(ok)} skill** dari {len(rows)} yang diuji.", "",
         "## Ringkasan (urut selisih terbesar)", "",
         "| # | Skill | Kategori | Tanpa → Dengan skill | Selisih |", "|---|---|---|---|---|"]
    for i, r in enumerate(ok, 1):
        L.append(f"| {i} | {r['judul_jualan'] or r['nama']} (`{r['nama']}`) | {r['kategori']} | "
                 f"{angka(r['skor_sebelum'])} → {angka(r['skor_sesudah'])} | +{angka(r['selisih'])} |")
    L += ["", "## Rincian per skill", ""]
    for r in ok:
        L += [f"### {r['judul_jualan'] or r['nama']} — {angka(r['skor_sebelum'])} → {angka(r['skor_sesudah'])}",
              f"`{r['nama']}` · {r['kategori']} · versi {r['versi_teruji']} · diuji {r['tanggal_uji']}", "",
              f"- **Permintaan:** {r['tugas']}",
              f"- **Tanpa skill:** {r['tanpa_skill']}",
              f"- **Dengan skill:** {r['dengan_skill']}"]
        if r.get("angka_kunci"):
            L.append(f"- **Angka kunci:** {r['angka_kunci']}")
        if r.get("catatan_jujur"):
            L.append(f"- **Catatan jujur:** {r['catatan_jujur']}")
        L.append("")
    L += ["## Tidak ditampilkan (internal)", "",
          "| Skill | Tanpa → Dengan | Verdik | Alasan |", "|---|---|---|---|"]
    for r in lain:
        alasan = r.get("tunda_promosi") or (
            "belum lulus" if not str(r.get("verdik_terakhir", "")).upper().startswith("LULUS")
            else "skor sesudah < 8" if r["skor_sesudah"] < MIN_SESUDAH else "selisih < 1,5")
        L.append(f"| `{r['nama']}` | {angka(r['skor_sebelum'])} → {angka(r['skor_sesudah'])} | {r.get('verdik_terakhir','')} | {alasan} |")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(ok)} tampil, {len(lain)} tidak")


if __name__ == "__main__":
    main()
