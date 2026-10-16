#!/usr/bin/env python3
"""Bangun promosi/SEBELUM-SESUDAH.md dari promosi/sebelum-sesudah.jsonl (SSOT).

Skill tampil di daftar promosi bila: verdik terakhir LULUS, skor sesudah >= 8,
selisih >= 1,5 (keputusan pemilik 2026-10-03), DAN — bila skill sudah pernah diuji sebelum/sesudah
di bot Telegram asli — hasil terakhirnya (`telegram_terakhir`, keputusan otomatis 100, 2026-10-16)
bukan BELUM. Kolom `label` (mis. "Belum direview tenaga medis") ditampilkan di kartu.
Skrip juga menyelaraskan kolom turunan di jsonl: `selisih` dan `lolos_promosi` (= tampil).
Pakai: python3 scripts/promosi_sebelum_sesudah.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
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


def tampil(r):
    t = tg_terakhir(r)
    return lulus_internal(r) and not (t and t.get("verdik_aturan") == "BELUM")


def alasan_sembunyi(r):
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


def kalimat_telegram(t):
    """Satu–dua kalimat awam tentang uji terakhir di bot Telegram asli."""
    if not t:
        return ""
    tgl = tanggal_id(t.get("tanggal", ""))
    pemb = (t.get("pembeda_awam") or "").strip()
    if pemb and not pemb.endswith((".", "!", "?")):
        pemb += "."
    v = t.get("verdik_aturan")
    if v == "LOLOS":
        k = f"Diuji juga di bot Telegram sungguhan ({tgl}): skor {angka(t['skor_tanpa'])} menjadi {angka(t['skor_dengan'])}."
    elif v == "BELUM":
        k = (f"Pada uji di bot Telegram sungguhan ({tgl}) hasilnya {angka(t['skor_tanpa'])} menjadi "
             f"{angka(t['skor_dengan'])}, belum memenuhi acuan kami.")
    else:
        k = f"Diuji juga di bot Telegram sungguhan ({tgl}), tanpa skor angka."
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
    ok = [r for r in rows if tampil(r)]
    lain = [r for r in rows if not tampil(r)]
    L = ["# Sebelum vs sesudah pakai skill Komunitech", "",
         "Berkas ini DIBUAT OTOMATIS dari `promosi/sebelum-sesudah.jsonl` (SSOT) oleh "
         "`scripts/promosi_sebelum_sesudah.py`. Jangan diedit manual; perbarui data lalu jalankan ulang.", "",
         f"Cara uji & arti skor: lihat [CARA-UJI.md](CARA-UJI.md). Ditampilkan: verdik LULUS, skor dengan skill ≥ {angka(MIN_SESUDAH)}, "
         f"selisih ≥ {angka(MIN_SELISIH)}, dan bila sudah diuji di bot Telegram asli, hasil terakhirnya memenuhi acuan yang sama. "
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
            L.append(f"- **Di bot Telegram sungguhan:** {kalimat_telegram(tg_terakhir(r))}")
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
             "tg": kalimat_telegram(tg_terakhir(r))} for r in ok]
    tanggal = max([r["tanggal_uji"] for r in ok] + [tg_terakhir(r)["tanggal"] for r in ok if tg_terakhir(r)])
    html = TPL.read_text(encoding="utf-8").replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    HTML.write_text(html.replace("__TANGGAL__", tanggal_id(tanggal)), encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(ok)} tampil, {len(lain)} tidak")


if __name__ == "__main__":
    main()
