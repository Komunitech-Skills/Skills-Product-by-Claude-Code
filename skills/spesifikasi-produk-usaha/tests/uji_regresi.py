#!/usr/bin/env python3
"""Uji regresi scripts/prioritas.py (Python standar). Jalankan: python3 tests/uji_regresi.py
Angka harapan dihitung manual dengan Fraction, bukan dengan fungsi script."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from decimal import Decimal as D
from fractions import Fraction as F

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(SINI, "..", "scripts", "prioritas.py")
spec = importlib.util.spec_from_file_location("prioritas", SCRIPT)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
TMP = tempfile.mkdtemp(prefix="uji-prio-")
GAGAL, N = [], [0]


def cek(nama, ok, info=""):
    N[0] += 1
    print(("OK    " if ok else "GAGAL ") + nama + ("" if ok else " -> " + str(info)))
    if not ok:
        GAGAL.append(nama)


def tulis(nama, isi):
    path = os.path.join(TMP, nama)
    with open(path, "w", encoding="utf-8") as f:
        f.write(isi)
    return path


def jalan(*arg):
    r = subprocess.run([sys.executable, SCRIPT, *arg], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


# RICE manual: A 1000*2*0.8/10=160 ; B 500*1*1/2=250 ; C 200*3*0.5/6=50
rice = "nama,jangkauan,dampak,keyakinan,usaha\nA,1000,2,80%,10\nB,500,1,100,2\nC,200,3,50,6\n"
h, g = p.proses(p.baca_csv(rice), "rice")
cek("rice urutan B,A,C", [x["nama"] for x in h] == ["B", "A", "C"])
cek("rice skor B=250", h[0]["skor"] == D(250), h[0]["skor"])
cek("rice skor A=160", h[1]["skor"] == D(160))
cek("rice skor C=50", h[2]["skor"] == D(50))
cek("tanpa galat", g == [])
# presisi: 1/3 tidak jadi float
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\nX,1,1,100,3\n"), "rice")
cek("presisi Decimal 1/3", p.fmt(h[0]["skor"]) == "0,33", p.fmt(h[0]["skor"]))
cek("pembulatan 0,125 -> 0,13", p.fmt(D("0.125")) == "0,13")
cek("format ribuan", p.fmt(D("12345.6")) == "12.345,60", p.fmt(D("12345.6")))
# koma desimal & titik-koma
h, g = p.proses(p.baca_csv("nama;jangkauan;dampak;keyakinan;usaha\nY;1.500;0,5;80;3\n"), "rice")
cek("titik-koma & 1.500 & 0,5", not g and h[0]["skor"] == D(1500) * D("0.5") * D("0.8") / 3, (h, g))
# ICE manual: 8*7*6=336 ; 9*5*5=225
h, g = p.proses(p.baca_csv("nama,dampak,keyakinan,kemudahan\nP,8,7,6\nQ,9,5,5\n"), "ice")
cek("ice skor", [x["skor"] for x in h] == [D(336), D(225)])
# data rusak
rusak = ("nama,jangkauan,dampak,keyakinan,usaha\nNol,100,1,80,0\nHuruf,abc,1,80,2\nNegatif,-5,1,80,2\n"
         "Yakin,10,1,150,2\nKosong,10,1,,2\nOk,10,1,100,1\n,1,1,1,1\n")
h, g = p.proses(p.baca_csv(rusak), "rice")
cek("hanya Ok dihitung", [x["nama"] for x in h] == ["Ok"], h)
cek("5 galat dilaporkan + 1 tanpa nama", len(g) == 6, g)
cek("usaha nol ditolak", any("dibagi nol" in a for _, _, a in g))
h, g = p.proses(p.baca_csv("nama,dampak,keyakinan,kemudahan\nZ,11,5,5\nNaN,nan,5,5\n"), "ice")
cek("ice di luar 1-10 & NaN ditolak", not h and len(g) == 2, g)
# seri: usaha lebih kecil dulu
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\nBesar,100,1,100,10\nKecil,10,1,100,1\n"), "rice")
cek("seri skor 10: usaha kecil dulu", [x["nama"] for x in h] == ["Kecil", "Besar"], h)
# tahap sepertiga
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\n" + "\n".join(f"I{i},{i*10},1,100,1" for i in range(1, 7))), "rice")
p.beri_tahap(h, "rice")
cek("6 item: 2/2/2", [x["tahap"] for x in h] == ["Sekarang"] * 2 + ["Berikutnya"] * 2 + ["Nanti"] * 2)
# kapasitas: usaha 5,5,5,5 ; kapasitas 10 -> 2 Sekarang, 2 Berikutnya
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\nA,40,1,100,5\nB,30,1,100,5\nC,20,1,100,5\nD,10,1,100,5\nE,5,1,100,5\n"), "rice")
p.beri_tahap(h, "rice", D(10))
cek("kapasitas 10", [x["tahap"] for x in h] == ["Sekarang", "Sekarang", "Berikutnya", "Berikutnya", "Nanti"], [x["tahap"] for x in h])
# CLI
f = tulis("ide.csv", rice)
rc, out, _ = jalan("--metode", "rice", "--csv", f)
cek("CLI kode 0 & tabel", rc == 0 and "| 1 | B | 250,00 | Sekarang |" in out, out)
rc, out, _ = jalan("--metode", "rice", "--csv", f, "--json")
cek("CLI json valid", rc == 0 and json.loads(out)["hasil"][0]["skor"] == "250.00", out)
f2 = tulis("rusak.csv", rusak)
rc, out, _ = jalan("--metode", "rice", "--csv", f2)
cek("CLI rusak kode 1 + pesan", rc == 1 and "TIDAK DIHITUNG" in out, (rc, out))
rc, out, err = jalan("--metode", "rice", "--csv", os.path.join(TMP, "tidak-ada.csv"))
cek("CLI file hilang kode 2", rc == 2 and "GAGAL" in err)
rc, _, err = jalan("--metode", "rice", "--csv", f, "--kapasitas", "0")
cek("kapasitas 0 ditolak", rc == 2, err)
f3 = tulis("kosong.csv", "")
rc, _, err = jalan("--metode", "rice", "--csv", f3)
cek("file kosong kode 2", rc == 2, err)
f4 = tulis("bom.csv", "﻿nama,dampak,keyakinan,kemudahan\nA,5,5,5\n")
rc, out, _ = jalan("--metode", "ice", "--csv", f4)
cek("BOM diterima", rc == 0 and "125,00" in out, out)
cek("cek Fraction manual A", F(1000) * 2 * F(8, 10) / 10 == 160)

print(f"\n{N[0] - len(GAGAL)}/{N[0]} lulus")
sys.exit(1 if GAGAL else 0)
