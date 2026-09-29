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
# --- revisi 1.0.1 ---
# F1: ide besar di urutan teratas tidak boleh mengunci tahap
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\nBesar,1500,1,100,15\nSedang,40,1,100,4\nKecil,10,1,100,2\n"), "rice")
p.beri_tahap(h, "rice", D(10))
cek("F1 Besar(15),Sedang(4),Kecil(2) kap 10 -> Nanti,Sekarang,Sekarang",
    [(x["nama"], x["tahap"]) for x in h] == [("Besar", "Nanti"), ("Sedang", "Sekarang"), ("Kecil", "Sekarang")], h)
cek("F1 catatan ide > kapasitas", "lebih besar dari kapasitas" in h[0]["catatan"], h[0])
# F1: ide yang tidak muat di Sekarang dilewati, ide kecil sesudahnya tetap masuk; sisanya ke Berikutnya
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\nA,120,1,100,6\nB,90,1,100,5\nC,40,1,100,4\nD,9,1,100,9\n"), "rice")
p.beri_tahap(h, "rice", D(10))
cek("F1 lewati & lanjut: A,C Sekarang; B Berikutnya; D Nanti",
    [x["tahap"] for x in h] == ["Sekarang", "Berikutnya", "Sekarang", "Nanti"], [(x["nama"], x["tahap"]) for x in h])
# F2: keyakinan pecahan ditolak dengan pesan jelas
h, g = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\nTas,300,1,\"0,9\",2\nKotak,100,1,0.8,1\nSatu,10,1,1,1\nPersen,10,1,\"0,9%\",1\nNol,10,1,0,1\n"), "rice")
cek("F2 0,9 / 0.8 / 1 ditolak", sorted(n for _, n, _ in g) == ["Kotak", "Satu", "Tas"], g)
cek("F2 pesan 'maksudnya 90%?'", any("maksudnya 90%?" in a for _, _, a in g), g)
cek("F2 pesan 'maksudnya 80%?'", any("maksudnya 80%?" in a for _, _, a in g), g)
cek("F2 0,9% eksplisit & 0 tetap diterima", sorted(x["nama"] for x in h) == ["Nol", "Persen"], h)
# F6: 10,000 ambigu ditolak; 10,000,000 dan 10.000 diterima; 0,250 tetap desimal
h, g = p.proses(p.baca_csv("nama;jangkauan;dampak;keyakinan;usaha\nAmbigu;10,000;1;100;1\nJuta;10,000,000;1;100;1\nTitik;10.000;1;100;1\nDes;10;0,250;100;1\n"), "rice")
cek("F6 10,000 ditolak (ambigu)", [n for _, n, _ in g] == ["Ambigu"] and "ambigu" in g[0][2], g)
skor = {x["nama"]: x["skor"] for x in h}
cek("F6 10,000,000 / 10.000 / 0,250", skor == {"Juta": D(10000000), "Titik": D(10000), "Des": D("2.5")}, skor)
# F6: judul kolom Inggris diterima
h, g = p.proses(p.baca_csv("Name,Reach,Impact,Confidence,Effort\nE,100,1,50,1\n"), "rice")
cek("F6 judul Inggris", not g and h[0]["skor"] == D(50), (h, g))
# F6: n=4 -> 2/1/1 ; seri ikut tahap atas
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\n" + "\n".join(f"I{i},{i*10},1,100,1" for i in range(1, 5))), "rice")
p.beri_tahap(h, "rice")
cek("F6 4 ide: 2/1/1", [x["tahap"] for x in h] == ["Sekarang", "Sekarang", "Berikutnya", "Nanti"], [x["tahap"] for x in h])
h, _ = p.proses(p.baca_csv("nama,jangkauan,dampak,keyakinan,usaha\nA,30,1,100,1\nB,20,1,100,1\nC,20,1,100,1\n"), "rice")
p.beri_tahap(h, "rice")
cek("F6 skor seri satu tahap", [x["tahap"] for x in h] == ["Sekarang", "Berikutnya", "Berikutnya"], [x["tahap"] for x in h])
# F6: kolom hilang -> pesan jelas
f5 = tulis("judul-salah.csv", "produk,reach,dampak,yakin,usaha\nA,1,1,50,1\n")
rc, out, err = jalan("--metode", "rice", "--csv", f5)
cek("F6 kolom wajib hilang kode 2 + nama kolom", rc == 2 and "kolom wajib tidak ditemukan: nama, keyakinan" in err, (rc, err))
# F6: --kapasitas pada ICE -> peringatan
f6 = tulis("ice.csv", "nama,dampak,keyakinan,kemudahan\nA,5,5,5\n")
rc, out, err = jalan("--metode", "ice", "--csv", f6, "--kapasitas", "10")
cek("F6 ICE + kapasitas diberi peringatan", rc == 0 and "PERINGATAN" in out and "PERINGATAN" in err, (rc, out, err))
rc, out, _ = jalan("--metode", "ice", "--csv", f6, "--kapasitas", "10", "--json")
cek("F6 ICE + kapasitas json peringatan", rc == 0 and json.loads(out)["peringatan"], out)
# B10: nilai lebih banyak dari judul kolom -> baris ditolak, bukan skor 0
f7 = tulis("kolom-lebih.csv", "nama,reach,dampak,keyakinan,usaha\nTas kertas,300,1,0,9,2\nB,100,2,80,1\n")
rc, out, err = jalan("--metode", "rice", "--csv", f7)
cek("B10 baris kelebihan nilai ditolak", "lebih banyak dari judul kolom" in out + err and "Tas kertas" in out + err, (rc, out, err))
cek("cek Fraction manual A", F(1000) * 2 * F(8, 10) / 10 == 160)

print(f"\n{N[0] - len(GAGAL)}/{N[0]} lulus")
sys.exit(1 if GAGAL else 0)
