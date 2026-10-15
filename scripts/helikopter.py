#!/usr/bin/env python3
"""Laporan helikopter: pelacak pekerjaan terbuka per skill + pengirim laporan ke grup uji.

Permintaan pemilik 2026-10-15: "setiap 10 skill sudah selesai, report helikopter view
dan berapa lagi yang belum selesai ke grup" (keputusan otomatis no. 88).

Berkas (semua di-commit, tanpa data pribadi):
- koordinasi/helikopter-status.csv  : satu baris per pekerjaan terbuka
      kolom: skill,jenis,keterangan,status,tanggal_selesai,bukti
      jenis : rujukan | uji-ulang | telegram | lain
      status: buka | selesai
- koordinasi/helikopter-laporan.md  : catatan laporan yang sudah terkirim (tabel)

Skill "tuntas" = semua barisnya berstatus selesai.
Laporan dikirim bila skill tuntas bertambah >= AMBANG (10) sejak laporan terakhir, atau --paksa.

Pakai:
  python3 scripts/helikopter.py                                   # status + pratinjau pesan, tanpa kirim
  python3 scripts/helikopter.py --tutup <skill> <jenis> "<bukti>"  # tandai pekerjaan selesai (hari ini, UTC)
  python3 scripts/helikopter.py --buka  <skill> <jenis> "<alasan>" # buka kembali pekerjaan
  python3 scripts/helikopter.py --tambah <skill> <jenis> "<keterangan>"
  python3 scripts/helikopter.py --kirim [--paksa] [--catatan "teks penghambat/kabar"]
Kirim butuh env tester_bot_token (bot penguji) -> grup uji, topik 242, tag pemilik.
Token tidak pernah dicetak atau disimpan.
"""
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "koordinasi" / "helikopter-status.csv"
LAPORAN = ROOT / "koordinasi" / "helikopter-laporan.md"
KATALOG = ROOT / "catalog.csv"

CHAT_ID = -1004407409583          # grup uji Komunitech (bukan grup member)
TOPIK = 242                       # topik "Ringkasan uji"
TAG = "@nikioktarian"
AMBANG = 10
BATAS_TELEGRAM = 4096
KOLOM = ["skill", "jenis", "keterangan", "status", "tanggal_selesai", "bukti"]
JENIS = ("rujukan", "uji-ulang", "telegram", "lain")
LABEL = {
    "rujukan": "Rujukan aturan belum diterapkan",
    "uji-ulang": "Uji ulang sebelum/sesudah",
    "telegram": "Belum tampil di bot Telegram",
    "lain": "Pekerjaan lain",
}
KEPALA_LAPORAN = (
    "# Laporan helikopter (otomatis tiap 10 skill tuntas)\n\n"
    "Dibuat oleh `scripts/helikopter.py` atas permintaan pemilik 2026-10-15 (keputusan otomatis no. 88). "
    "Satu baris per laporan yang terkirim ke grup uji topik 242. "
    "Kolom *skill tuntas baru* = skill yang tuntas sejak laporan sebelumnya; "
    "gabungan kolom ini pada semua baris = daftar skill yang sudah dilaporkan tuntas.\n\n"
    "| no | tanggal (UTC) | tuntas total | sisa skill | skill tuntas baru | catatan |\n"
    "|---|---|---|---|---|---|\n"
)


def sekarang():
    return datetime.now(timezone.utc)


# ---------- status ----------
def baca_status(path=STATUS):
    if not Path(path).exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        baris = list(csv.DictReader(f))
    for b in baris:
        if b["jenis"] not in JENIS:
            raise ValueError(f"jenis tidak dikenal: {b['jenis']} ({b['skill']})")
        if b["status"] not in ("buka", "selesai"):
            raise ValueError(f"status tidak dikenal: {b['status']} ({b['skill']})")
    return baris


def tulis_status(baris, path=STATUS):
    baris = sorted(baris, key=lambda b: (b["skill"], JENIS.index(b["jenis"]), b["keterangan"]))
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=KOLOM, lineterminator="\n")
        w.writeheader()
        for b in baris:
            w.writerow({k: b.get(k, "") for k in KOLOM})


def ringkas(baris):
    """Kembalikan {skill: [baris]}, daftar tuntas, daftar sisa, dan jumlah skill terbuka per jenis."""
    per_skill = {}
    for b in baris:
        per_skill.setdefault(b["skill"], []).append(b)
    tuntas = sorted(s for s, it in per_skill.items() if all(i["status"] == "selesai" for i in it))
    sisa = sorted(s for s in per_skill if s not in tuntas)
    per_jenis = {j: sorted({b["skill"] for b in baris if b["jenis"] == j and b["status"] == "buka"}) for j in JENIS}
    return {"per_skill": per_skill, "tuntas": tuntas, "sisa": sisa, "per_jenis": per_jenis,
            "item_buka": sum(1 for b in baris if b["status"] == "buka")}


def tutup(baris, skill, jenis, bukti, tanggal=None):
    cocok = [b for b in baris if b["skill"] == skill and b["jenis"] == jenis]
    if not cocok:
        raise KeyError(f"tidak ada pekerjaan {jenis} untuk skill {skill}")
    for b in cocok:
        b["status"] = "selesai"
        b["tanggal_selesai"] = tanggal or sekarang().strftime("%Y-%m-%d")
        b["bukti"] = bukti
    return len(cocok)


def buka(baris, skill, jenis, alasan):
    cocok = [b for b in baris if b["skill"] == skill and b["jenis"] == jenis]
    if not cocok:
        raise KeyError(f"tidak ada pekerjaan {jenis} untuk skill {skill}")
    for b in cocok:
        b["status"] = "buka"
        b["tanggal_selesai"] = ""
        b["bukti"] = alasan
    return len(cocok)


def tambah(baris, skill, jenis, keterangan):
    if jenis not in JENIS:
        raise ValueError(f"jenis harus salah satu dari {JENIS}")
    if any(b["skill"] == skill and b["jenis"] == jenis and b["keterangan"] == keterangan for b in baris):
        return False
    baris.append({"skill": skill, "jenis": jenis, "keterangan": keterangan,
                  "status": "buka", "tanggal_selesai": "", "bukti": ""})
    return True


# ---------- laporan ----------
def baca_laporan(path=LAPORAN):
    """Baca tabel laporan -> list dict(no, tanggal, tuntas, sisa, baru[list], catatan)."""
    if not Path(path).exists():
        return []
    hasil = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|"):
            continue
        sel = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(sel) < 6 or not sel[0].isdigit():
            continue
        hasil.append({"no": int(sel[0]), "tanggal": sel[1], "tuntas": int(sel[2]), "sisa": int(sel[3]),
                      "baru": [s for s in (x.strip() for x in sel[4].split(",")) if s and s != "—"],
                      "catatan": sel[5]})
    return hasil


def sudah_dilaporkan(laporan):
    s = set()
    for l in laporan:
        s.update(l["baru"])
    return s


def skill_baru(ringkasan, laporan):
    return [s for s in ringkasan["tuntas"] if s not in sudah_dilaporkan(laporan)]


def perlu_kirim(ringkasan, laporan, ambang=AMBANG):
    baru = skill_baru(ringkasan, laporan)
    return len(baru) >= ambang, baru


def catat_laporan(nomor, tanggal, ringkasan, baru, catatan, path=LAPORAN):
    p = Path(path)
    teks = p.read_text(encoding="utf-8") if p.exists() else KEPALA_LAPORAN
    if not teks.endswith("\n"):
        teks += "\n"
    teks += (f"| {nomor} | {tanggal} | {len(ringkasan['tuntas'])} | {len(ringkasan['sisa'])} | "
             f"{', '.join(baru) if baru else '—'} | {catatan.replace('|', '/') or '—'} |\n")
    p.write_text(teks, encoding="utf-8")


# ---------- pesan ----------
def katalog_ringkas(path=KATALOG):
    if not Path(path).exists():
        return ""
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    hitung = {}
    for r in rows:
        hitung[r["status"]] = hitung.get(r["status"], 0) + 1
    urut = ["rilis", "beta", "lulus", "uji", "draft", "ide", "arsip", "ditolak"]
    bagian = [f"{hitung[s]} {s}" for s in urut if s in hitung]
    bagian += [f"{n} {s}" for s, n in sorted(hitung.items()) if s not in urut]
    return f"{len(rows)} skill = " + ", ".join(bagian)


def _daftar(nama, maks_panjang):
    teks = ", ".join(nama)
    if len(teks) <= maks_panjang:
        return teks
    ambil, panjang = [], 0
    for n in nama:
        if panjang + len(n) + 2 > maks_panjang - 12:
            break
        ambil.append(n)
        panjang += len(n) + 2
    return ", ".join(ambil) + f", +{len(nama) - len(ambil)} lagi"


def _tanggal_id(dt):
    bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    return f"{dt.day} {bulan[dt.month - 1]} {dt.year}, {dt:%H:%M} UTC"


def susun_pesan(ringkasan, laporan, nomor, baru, dt=None, katalog="", catatan=""):
    dt = dt or sekarang()
    total = len(ringkasan["tuntas"]) + len(ringkasan["sisa"])
    sebelumnya = laporan[-1] if laporan else None
    acuan = f" sejak laporan #{sebelumnya['no']} ({sebelumnya['tanggal'][:10]})" if sebelumnya else ""
    baris = [
        f"{TAG} LAPORAN HELIKOPTER #{nomor} — {_tanggal_id(dt)}",
        "Otomatis tiap 10 skill tuntas (keputusan otomatis no. 88). "
        "Skill tuntas = semua pekerjaan terbuka untuknya selesai (rujukan aturan, uji ulang, tampil di bot Telegram).",
        "",
        f"TUNTAS: {len(baru)} skill baru{acuan} — total {len(ringkasan['tuntas'])} dari {total} skill antrean",
    ]
    for s in baru[:AMBANG + 5]:
        bukti = [b["bukti"] for b in ringkasan["per_skill"][s] if b["bukti"]]
        baris.append(f"- {s}" + (f" — {bukti[-1]}" if bukti else ""))
    if len(baru) > AMBANG + 5:
        baris.append(f"- +{len(baru) - AMBANG - 5} skill lagi (lihat koordinasi/helikopter-laporan.md)")
    baris += ["", f"BELUM TUNTAS: {len(ringkasan['sisa'])} skill ({ringkasan['item_buka']} pekerjaan)"]
    for j in JENIS:
        nama = ringkasan["per_jenis"][j]
        if nama:
            baris.append(f"- {LABEL[j]}: {len(nama)} skill ({_daftar(nama, 600)})")
    baris.append("(satu skill bisa punya lebih dari satu pekerjaan)")
    if katalog:
        baris += ["", f"KATALOG: {katalog}."]
    if catatan:
        baris.append(f"CATATAN: {catatan}")
    pesan = "\n".join(baris)
    if len(pesan) > BATAS_TELEGRAM:
        pesan = pesan[:BATAS_TELEGRAM - 20].rstrip() + "\n(…dipotong)"
    return pesan


def kirim_telegram(teks, chat_id=CHAT_ID, topik=TOPIK):
    tok = os.environ.get("tester_bot_token")
    if not tok:
        raise RuntimeError("env tester_bot_token tidak ada; laporan tidak dikirim")
    data = urllib.parse.urlencode({"chat_id": chat_id, "message_thread_id": topik, "text": teks,
                                   "disable_web_page_preview": "true"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}") | {"http": e.code}


# ---------- CLI ----------
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    catatan = ""
    if "--catatan" in argv:
        i = argv.index("--catatan")
        catatan = argv[i + 1]
        del argv[i:i + 2]
    paksa = "--paksa" in argv
    argv = [a for a in argv if a != "--paksa"]

    baris = baca_status()
    if argv and argv[0] in ("--tutup", "--buka", "--tambah"):
        if len(argv) != 4:
            print(f"pakai: {argv[0]} <skill> <jenis> \"<teks>\"", file=sys.stderr)
            return 2
        fungsi = {"--tutup": tutup, "--buka": buka, "--tambah": tambah}[argv[0]]
        try:
            hasil = fungsi(baris, argv[1], argv[2], argv[3])
        except (KeyError, ValueError) as e:
            print(f"GAGAL: {e}", file=sys.stderr)
            return 2
        tulis_status(baris)
        print(f"{argv[0][2:]}: {argv[1]} {argv[2]} -> {hasil}")
        baris = baca_status()

    r = ringkas(baris)
    laporan = baca_laporan()
    kirim, baru = perlu_kirim(r, laporan)
    nomor = (laporan[-1]["no"] + 1) if laporan else 0
    pesan = susun_pesan(r, laporan, nomor, baru, katalog=katalog_ringkas(), catatan=catatan)
    print(f"skill antrean: {len(r['tuntas']) + len(r['sisa'])} | tuntas: {len(r['tuntas'])} | "
          f"sisa: {len(r['sisa'])} | pekerjaan buka: {r['item_buka']} | tuntas baru sejak laporan: {len(baru)} "
          f"| ambang {AMBANG}: {'KIRIM' if kirim else 'belum'}")
    if "--kirim" not in argv:
        print("--- pratinjau pesan ---")
        print(pesan)
        return 0
    if not (kirim or paksa):
        print("belum waktunya kirim (pakai --paksa untuk memaksa)")
        return 0
    hasil = kirim_telegram(pesan)
    if not hasil.get("ok"):
        print(f"GAGAL kirim: {hasil.get('description', hasil)}", file=sys.stderr)
        return 1
    tanggal = sekarang().strftime("%Y-%m-%d %H:%M")
    catat_laporan(nomor, tanggal, r, baru, catatan or ("laporan awal" if nomor == 0 else ""))
    print(f"terkirim: laporan #{nomor} ke topik {TOPIK} (message_id {hasil['result'].get('message_id')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
