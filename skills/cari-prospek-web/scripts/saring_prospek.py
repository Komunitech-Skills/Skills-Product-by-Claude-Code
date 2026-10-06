#!/usr/bin/env python3
"""Saring daftar prospek: dedup, tandai tanpa sumber, skor cocok 0-100.

Pakai:  python3 saring_prospek.py prospek.csv --icp "cleaning service,kantor,surabaya"
        (Windows: python atau py)  Opsi: --keluar hasil.csv  --kota Surabaya  --maks 20
Python standar saja. Hanya membaca berkas yang diberikan; tidak ada akses jaringan.
Kolom bebas (huruf besar/kecil tidak berpengaruh): nama, kota, jenis, website, kontak, sumber, tanggal, catatan.
"""
import argparse
import csv
import io
import re
import sys
from difflib import SequenceMatcher
from urllib.parse import urlparse

ALIAS = {
    "nama": ["nama", "nama usaha", "usaha", "perusahaan", "name", "company"],
    "kota": ["kota", "wilayah", "lokasi", "city"],
    "jenis": ["jenis", "bidang", "kategori", "type", "industri"],
    "website": ["website", "situs", "url", "web", "domain"],
    "kontak": ["kontak", "telepon", "telp", "email", "wa", "phone", "contact"],
    "sumber": ["sumber", "sumber url", "url sumber", "source", "link sumber"],
    "tanggal": ["tanggal", "tanggal cek", "tgl", "date"],
    "catatan": ["catatan", "alasan", "alasan cocok", "note", "notes"],
}
KOLOM = ["nama", "kota", "jenis", "website", "kontak", "sumber", "tanggal", "catatan"]
BELUM = "[belum terverifikasi]"
BADAN = {"pt", "cv", "ud", "pd", "tbk", "persero", "koperasi", "toko", "the"}
RE_HP = re.compile(r"(?<!\d)(?:\+?62|0)\s?-?8\d[\d\s\-]{6,12}")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
GRATIS_MAIL = ("gmail.", "yahoo.", "hotmail.", "outlook.", "icloud.", "ymail.")


def baca_teks(path):
    with open(path, "rb") as f:
        mentah = f.read()
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return mentah.decode(enc)
        except UnicodeError:
            continue
    return mentah.decode("utf-8", "replace")


def petakan(header):
    peta = {}
    for i, h in enumerate(header):
        k = re.sub(r"\s+", " ", (h or "").strip().lower())
        for baku, daftar in ALIAS.items():
            if k in daftar and baku not in peta:
                peta[baku] = i
    return peta


def baca_csv(path):
    teks = baca_teks(path)
    if not teks.strip():
        raise ValueError("berkas kosong")
    try:
        dialek = csv.Sniffer().sniff(teks[:2000], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    baris = [r for r in csv.reader(io.StringIO(teks), dialek) if any(c.strip() for c in r)]
    peta = petakan(baris[0])
    if "nama" not in peta:
        raise ValueError("kolom nama usaha tidak ditemukan (judul kolom: nama/usaha/perusahaan)")
    hasil = []
    for r in baris[1:]:
        d = {k: (r[peta[k]].strip() if k in peta and peta[k] < len(r) else "") for k in KOLOM}
        if d["nama"]:
            hasil.append(d)
    return hasil


def inti_nama(nama):
    kata = re.findall(r"[a-z0-9]+", nama.lower())
    kata = [k for k in kata if k not in BADAN]
    return " ".join(kata)


def domain(url):
    u = (url or "").strip().lower()
    if not u:
        return ""
    if "://" not in u:
        u = "http://" + u
    h = urlparse(u).netloc.split(":")[0]
    return h[4:] if h.startswith("www.") else h


def mirip(a, b):
    if not a or not b:
        return False
    return a == b or SequenceMatcher(None, a, b).ratio() >= 0.88


def punya_sumber(d):
    s = d["sumber"].strip().lower()
    return bool(s) and BELUM not in s and s not in ("-", "n/a", "tidak ada", "?")


def peringatan_kontak(kontak):
    """Tandai kontak yang patut dicek: HP (bisa pribadi) atau email gratisan."""
    cat = []
    if RE_HP.search(kontak):
        cat.append("nomor HP: pastikan nomor bisnis yang dipublikasikan situs resmi, bukan pribadi")
    for m in RE_EMAIL.findall(kontak):
        if m.lower().split("@")[-1].startswith(GRATIS_MAIL):
            cat.append("email gratisan: cek apakah email bisnis resmi")
            break
    return cat


def skor(d, kata, kota):
    teks = " ".join([d["nama"], d["jenis"], d["catatan"], d["kota"], d["website"]]).lower()
    if kata:
        cocok = sum(1 for k in kata if k in teks)
        s = 55.0 * cocok / len(kata)
    else:
        s = 27.5
    if kota:
        s += 15 if kota in (d["kota"] + " " + d["catatan"]).lower() else 0
    else:
        s += 7.5
    s += 10 if domain(d["website"]) else 0
    s += 10 if d["kontak"].strip() and BELUM not in d["kontak"] else 0
    s += 10 if punya_sumber(d) else 0
    if not punya_sumber(d):
        s = min(s, 30)
    return int(round(min(s, 100)))


def saring(rows, kata, kota=""):
    kata = [k.strip().lower() for k in kata if k.strip()]
    kota = kota.strip().lower()
    unik, dobel = [], []
    for d in rows:
        inti, dom = inti_nama(d["nama"]), domain(d["website"])
        ada = None
        for u in unik:
            if (dom and dom == u["_dom"]) or mirip(inti, u["_inti"]):
                ada = u
                break
        if ada is not None:
            dobel.append((d["nama"], ada["nama"]))
            for k in KOLOM:  # lengkapi sel kosong pada baris yang dipertahankan
                if not ada[k] and d[k]:
                    ada[k] = d[k]
            continue
        d = dict(d, _inti=inti, _dom=dom)
        unik.append(d)
    for d in unik:
        d["skor"] = skor(d, kata, kota)
        c = []
        if not punya_sumber(d):
            c.append("TANPA SUMBER: " + BELUM)
        c += peringatan_kontak(d["kontak"])
        d["periksa"] = "; ".join(c)
    unik.sort(key=lambda x: (-x["skor"], x["nama"].lower()))
    return unik, dobel


def main(argv=None):
    ap = argparse.ArgumentParser(description="Saring & skor daftar prospek")
    ap.add_argument("berkas")
    ap.add_argument("--icp", default="", help="kata kunci profil ideal, pisah koma")
    ap.add_argument("--kota", default="", help="kota/wilayah target")
    ap.add_argument("--maks", type=int, default=0, help="batasi jumlah baris keluaran")
    ap.add_argument("--keluar", default="", help="simpan CSV hasil ke berkas ini")
    a = ap.parse_args(argv)
    try:
        rows = baca_csv(a.berkas)
    except (OSError, ValueError, csv.Error) as e:
        print("GAGAL: %s" % e, file=sys.stderr)
        return 2
    if not rows:
        print("GAGAL: tidak ada baris prospek", file=sys.stderr)
        return 2
    hasil, dobel = saring(rows, a.icp.split(","), a.kota)
    tampil = hasil[: a.maks] if a.maks > 0 else hasil
    kolom = KOLOM + ["skor", "periksa"]
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(kolom)
    for d in tampil:
        w.writerow([d[k] for k in kolom])
    if a.keluar:
        with open(a.keluar, "w", encoding="utf-8", newline="") as f:
            f.write(out.getvalue())
    sys.stdout.write(out.getvalue())
    tanpa = sum(1 for d in hasil if not punya_sumber(d))
    print("\nRINGKASAN: %d baris masuk, %d unik, %d duplikat dibuang, %d tanpa sumber, %d perlu dicek kontaknya"
          % (len(rows), len(hasil), len(dobel), tanpa, sum(1 for d in hasil if "nomor HP" in d["periksa"] or "email gratisan" in d["periksa"])),
          file=sys.stderr)
    for dup, asli in dobel:
        print("DUPLIKAT: '%s' sama dengan '%s'" % (dup, asli), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
