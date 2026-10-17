#!/usr/bin/env python3
"""Bangun promosi/SEBELUM-SESUDAH.md dari promosi/sebelum-sesudah.jsonl (SSOT).

Skill tampil di daftar promosi bila: verdik terakhir LULUS, skor sesudah >= 8,
selisih >= 1,5 (keputusan pemilik 2026-10-03), DAN — bila skill sudah pernah diuji sebelum/sesudah
di bot Telegram asli — hasil terakhirnya (`telegram_terakhir`, keputusan otomatis 100, 2026-10-16)
bukan BELUM (TIDAK-DINILAI = uji bot lama tanpa skor tetap tampil, kalimat kartu menyebut "tanpa skor angka";
bila versi yang diuji di bot lebih lama dari versi catalog.csv atau tidak tercatat, kalimat kartu menyebutnya),
DAN baris tidak punya kolom `tahan` ({"alasan": "...", "sejak": "YYYY-MM-DD"}: kartu ditahan sementara,
mis. versi yang dijual perlu diuji ulang; alasannya tampil di tabel internal "Tidak ditampilkan").
Kolom `label` (mis. "Belum direview tenaga medis") ditampilkan di kartu.
Skrip juga menyelaraskan kolom turunan di jsonl: `selisih` dan `lolos_promosi` (= tampil).
Pakai: python3 scripts/promosi_sebelum_sesudah.py
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "catalog.csv"
SRC = ROOT / "promosi" / "sebelum-sesudah.jsonl"
OUT = ROOT / "promosi" / "SEBELUM-SESUDAH.md"
TPL = ROOT / "promosi" / "template-halaman.html"
HTML = ROOT / "promosi" / "halaman-sebelum-sesudah.html"
MIN_SESUDAH, MIN_SELISIH = 8.0, 1.5


def angka(x):
    return f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")


BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def tanggal_id(iso):
    try:
        y, m, d = str(iso)[:10].split("-")
        return f"{int(d)} {BULAN[int(m) - 1]} {y}"
    except Exception:
        return str(iso)


def tg_terakhir(r):
    """Uji sebelum/sesudah terakhir di bot Telegram asli (dict) atau None."""
    t = r.get("telegram_terakhir")
    return t if isinstance(t, dict) and t.get("ada") else None


def lulus_internal(r):
    return (str(r.get("verdik_terakhir", "")).upper().startswith("LULUS")
            and r["skor_sesudah"] >= MIN_SESUDAH
            and r["skor_sesudah"] - r["skor_sebelum"] >= MIN_SELISIH)


def ditahan(r):
    """Kolom opsional `tahan` = {"alasan": ..., "sejak": ...}: kartu ditahan sementara (transparan)."""
    return bool(r.get("tahan"))


def tampil(r):
    if ditahan(r):
        return False
    t = tg_terakhir(r)
    return lulus_internal(r) and not (t and t.get("verdik_aturan") == "BELUM")


def alasan_sembunyi(r):
    if ditahan(r):
        th = r["tahan"]
        alasan = th.get("alasan", "") if isinstance(th, dict) else str(th)
        return f"ditahan: {alasan}".strip()
    if not str(r.get("verdik_terakhir", "")).upper().startswith("LULUS"):
        return "belum lulus"
    if r["skor_sesudah"] < MIN_SESUDAH:
        return "skor sesudah < 8"
    if r["skor_sesudah"] - r["skor_sebelum"] < MIN_SELISIH:
        return "selisih < 1,5"
    t = tg_terakhir(r)
    if t and t.get("verdik_aturan") == "BELUM":
        return f"uji di bot Telegram asli belum lulus ({angka(t['skor_tanpa'])} → {angka(t['skor_dengan'])}, {tanggal_id(t['tanggal'])})"
    return "-"


def versi_katalog():
    """{nama: versi} dari catalog.csv (hanya dibaca) — untuk menandai uji bot dengan versi lama."""
    try:
        with CAT.open(encoding="utf-8", newline="") as f:
            return {r["nama"]: (r.get("versi") or "").strip() for r in csv.DictReader(f)}
    except Exception:
        return {}


def _versi(s):
    m = re.fullmatch(r"\s*(\d+)\.(\d+)\.(\d+)\s*", str(s or ""))
    return tuple(int(x) for x in m.groups()) if m else None


def ket_versi(t, versi_jual):
    """Keterangan awam bila bot diuji dengan versi lebih lama dari yang dijual / versinya tidak tercatat."""
    vd, vj = _versi(t.get("versi_diuji")), _versi(versi_jual)
    if vd is None:
        return "versi yang diuji tidak tercatat"
    if vj and vd < vj:
        return "versi lebih lama dari yang dijual"
    return ""


def kalimat_telegram(t, versi_jual=""):
    """Satu–dua kalimat awam tentang uji terakhir di bot Telegram asli."""
    if not t:
        return ""
    tgl = tanggal_id(t.get("tanggal", ""))
    kv = ket_versi(t, versi_jual)
    waktu = f"{tgl} ({kv})" if kv else tgl
    pemb = (t.get("pembeda_awam") or "").strip()
    if pemb and not pemb.endswith((".", "!", "?")):
        pemb += "."
    v = t.get("verdik_aturan")
    if v == "LOLOS":
        k = f"Uji {waktu}: skor {angka(t['skor_tanpa'])} menjadi {angka(t['skor_dengan'])}."
    elif v == "BELUM":
        k = (f"Uji {waktu}: skor {angka(t['skor_tanpa'])} menjadi "
             f"{angka(t['skor_dengan'])}, belum memenuhi acuan kami.")
    else:
        k = f"Uji {waktu}: uji ini hanya mencatat perbedaannya, tanpa skor angka."
    return (k + " " + pemb).strip()


def main():
    rows = [json.loads(l) for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
    berubah = False
    for r in rows:
        sel = round(r["skor_sesudah"] - r["skor_sebelum"], 2)
        lp = tampil(r)
        if r.get("selisih") != sel or r.get("lolos_promosi") != lp:
            berubah = True
        r["selisih"], r["lolos_promosi"] = sel, lp
    if berubah:  # kolom turunan diselaraskan di SSOT (urutan baris tetap)
        SRC.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    rows.sort(key=lambda r: (-r["selisih"], -r["skor_sesudah"], r["nama"]))
    vk = versi_katalog()
    ok = [r for r in rows if tampil(r)]
    lain = [r for r in rows if not tampil(r)]
    L = ["# Sebelum vs sesudah pakai skill Komunitech", "",
         "Berkas ini DIBUAT OTOMATIS dari `promosi/sebelum-sesudah.jsonl` (SSOT) oleh "
         "`scripts/promosi_sebelum_sesudah.py`. Jangan diedit manual; perbarui data lalu jalankan ulang.", "",
         f"Cara uji & arti skor: lihat [CARA-UJI.md](CARA-UJI.md). Ditampilkan: verdik LULUS, skor dengan skill ≥ {angka(MIN_SESUDAH)}, "
         f"selisih ≥ {angka(MIN_SELISIH)}, uji terakhirnya di bot Telegram asli (bila ada) tidak gagal, dan kartu tidak sedang ditahan "
         f"(uji bot lama tanpa skor angka tetap tampil dan disebut \"tanpa skor angka\"). "
         f"Jumlah: **{len(ok)} skill** dari {len(rows)} yang diuji; "
         f"{sum(1 for r in ok if tg_terakhir(r))} di antaranya juga teruji di bot Telegram asli.", "",
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
        if r.get("label"):
            L.append(f"- **Keterangan:** {r['label']}")
        if tg_terakhir(r):
            L.append(f"- **Di bot Telegram sungguhan:** {kalimat_telegram(tg_terakhir(r), vk.get(r['nama'], ''))}")
        if r.get("catatan_jujur"):
            L.append(f"- **Catatan jujur:** {r['catatan_jujur']}")
        L.append("")
    L += ["## Tidak ditampilkan (internal)", "",
          "| Skill | Tanpa → Dengan | Verdik | Alasan |", "|---|---|---|---|"]
    for r in lain:
        alasan = alasan_sembunyi(r)
        L.append(f"| `{r['nama']}` | {angka(r['skor_sebelum'])} → {angka(r['skor_sesudah'])} | {r.get('verdik_terakhir','')} | {alasan} |")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    data = [{"judul": r["judul_jualan"] or r["nama"], "kat": r["kategori"], "b": r["skor_sebelum"],
             "a": r["skor_sesudah"], "tugas": r["tugas"], "tanpa": r["tanpa_skill"], "dengan": r["dengan_skill"],
             "angka": r.get("angka_kunci", ""), "catatan": r.get("catatan_jujur", ""), "label": r.get("label", ""),
             "tg": kalimat_telegram(tg_terakhir(r), vk.get(r["nama"], ""))} for r in ok]
    tanggal = max([r["tanggal_uji"] for r in ok] + [tg_terakhir(r)["tanggal"] for r in ok if tg_terakhir(r)])
    html = TPL.read_text(encoding="utf-8").replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    HTML.write_text(html.replace("__TANGGAL__", tanggal_id(tanggal)), encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(ok)} tampil, {len(lain)} tidak")


if __name__ == "__main__":
    main()
