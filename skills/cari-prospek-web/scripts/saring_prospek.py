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
    "website": ["website", "situs", "web", "domain", "url"],
    "kontak": ["kontak", "telepon", "telp", "email", "wa", "phone", "contact"],
    "sumber": ["sumber", "sumber url", "url sumber", "source", "link sumber", "tautan", "link", "maps",
               "tautan halaman (maps/situs)", "url"],
    "tanggal": ["tanggal", "tanggal cek", "tgl", "date"],
    "catatan": ["catatan", "alasan", "alasan cocok", "note", "notes"],
}
KOLOM = ["nama", "kota", "jenis", "website", "kontak", "sumber", "tanggal", "catatan"]
BELUM = "[belum terverifikasi]"
BADAN = {"pt", "cv", "ud", "pd", "tbk", "persero", "koperasi", "toko", "the"}
RE_HP = re.compile(r"(?<!\d)(?:\+?62|0)\s?-?8\d[\d\s\-]{6,12}")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RE_NO_DUMMY = re.compile(r"\bno\.?\s*(?:123|1234|12|1)\b(?!\d)", re.I)
DOMAIN_MAIL_DUMMY = ("domain.com", "email.com", "mail.com", "test.com", "contoh.com", "yourdomain.com", "company.com")
# Platform bersama: bukan bukti "situs yang sama" antar usaha.
PLATFORM = ("google.com", "maps.google.com", "maps.app.goo.gl", "goo.gl", "g.page", "instagram.com",
            "facebook.com", "fb.com", "tokopedia.com", "shopee.co.id", "linktr.ee", "wa.me", "tiktok.com")
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


def baca_csv(path, peringatan=None):
    """Baca CSV. Baris tidak rata ditoleransi; tiap baris bermasalah dicatat ke daftar `peringatan`."""
    if peringatan is None:
        peringatan = []
    teks = baca_teks(path)
    if not teks.strip():
        raise ValueError("berkas kosong, belum ada isinya")
    judul = teks.lstrip().splitlines()[0]
    pemisah = max(",;\t", key=lambda c: judul.count(c))
    dialek = csv.excel_tab if pemisah == "\t" else csv.excel
    if pemisah == ";":
        class dialek(csv.excel):  # noqa: N801
            delimiter = ";"
    baris = [r for r in csv.reader(io.StringIO(teks), dialek) if any(c.strip() for c in r)]
    peta = petakan(baris[0])
    if "nama" not in peta:
        raise ValueError("kolom nama usaha tidak ditemukan; beri judul kolom 'nama' atau 'usaha' atau 'perusahaan' di baris pertama")
    if "sumber" not in peta:  # kolom 'url' bisa dipakai sebagai sumber bila belum ada kolom sumber lain
        for i, h in enumerate(baris[0]):
            if re.sub(r"\s+", " ", h.strip().lower()) in ALIAS["sumber"]:
                peta["sumber"] = i
                break
    n = len(baris[0])
    hasil = []
    for no, r in enumerate(baris[1:], start=2):
        if len(r) < n:
            peringatan.append("baris %d hanya punya %d kolom dari %d; kolom yang kurang dianggap kosong" % (no, len(r), n))
            r = r + [""] * (n - len(r))
        elif len(r) > n:
            peringatan.append("baris %d kelebihan kolom (%d dari %d); kelebihannya digabung ke kolom terakhir" % (no, len(r), n))
            sep = dialek.delimiter if dialek.delimiter else ","
            r = r[:n - 1] + [(sep + " ").join(r[n - 1:])]
        d = {k: (r[peta[k]].strip() if k in peta else "") for k in KOLOM}
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


def kunci_domain(url):
    """Domain untuk dedup 'situs sama'; kosong bila platform bersama (maps, IG, FB, marketplace, dll)."""
    d = domain(url)
    if not d:
        return ""
    if any(d == p or d.endswith("." + p) for p in PLATFORM):
        return ""
    return d


def digit_dummy(teks):
    """True bila ada nomor telepon dengan pola deret/berulang (placeholder)."""
    for m in re.finditer(r"\+?\d[\d\s\-().]{6,}\d", teks):
        dg = re.sub(r"\D", "", m.group())
        if len(dg) < 7:
            continue
        for i in range(len(dg) - 5):
            w = dg[i:i + 6]
            sel = {int(w[j + 1]) - int(w[j]) for j in range(5)}
            if sel in ({1}, {-1}, {0}):
                return True
    return False


def dummy(d):
    """Alasan bila baris tampak placeholder/contoh, bukan kontak nyata; kosong bila wajar."""
    alasan = []
    gabung = " ".join([d["kontak"], d["catatan"], d["nama"], d["website"], d["sumber"]])
    if digit_dummy(d["kontak"]):
        alasan.append("nomor berderet/berulang")
    if RE_NO_DUMMY.search(gabung):
        alasan.append("alamat 'No. 123'")
    for m in RE_EMAIL.findall(gabung):
        dm = m.lower().split("@")[-1]
        if dm in DOMAIN_MAIL_DUMMY or dm.startswith("example.") or dm == "example":
            alasan.append("email contoh")
            break
    if "lorem" in gabung.lower() or "ipsum" in gabung.lower():
        alasan.append("teks Lorem")
    return ", ".join(alasan)


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
    s += 10 if kunci_domain(d["website"]) else 0
    s += 10 if d["kontak"].strip() and BELUM not in d["kontak"] else 0
    s += 10 if punya_sumber(d) else 0
    if not punya_sumber(d):
        s = min(s, 30)
    if dummy(d):
        return 0
    return int(round(min(s, 100)))


def saring(rows, kata, kota=""):
    kata = [k.strip().lower() for k in kata if k.strip()]
    kota = kota.strip().lower()
    unik, dobel = [], []
    for d in rows:
        inti, dom = inti_nama(d["nama"]), kunci_domain(d["website"])
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
        dm = dummy(d)
        if dm:
            c.append("DUMMY? [contoh/dummy, bukan kontak nyata] (%s)" % dm)
        if not punya_sumber(d):
            c.append("TANPA SUMBER: " + BELUM)
        if not dm:
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
    peringatan = []
    try:
        rows = baca_csv(a.berkas, peringatan)
    except FileNotFoundError:
        print("GAGAL: berkas '%s' tidak ditemukan; periksa nama dan lokasinya" % a.berkas, file=sys.stderr)
        return 2
    except OSError as e:
        print("GAGAL: berkas tidak bisa dibuka (%s)" % e.strerror, file=sys.stderr)
        return 2
    except (ValueError, csv.Error) as e:
        print("GAGAL: %s" % e, file=sys.stderr)
        return 2
    for w_ in peringatan:
        print("PERINGATAN: " + w_, file=sys.stderr)
    if not rows:
        print("GAGAL: tidak ada baris usaha yang bisa dibaca; pastikan ada isi di bawah judul kolom", file=sys.stderr)
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
    print("\nRINGKASAN: %d baris masuk, %d unik, %d duplikat dibuang, %d tanpa sumber, %d perlu dicek kontaknya, %d tampak dummy"
          % (len(rows), len(hasil), len(dobel), tanpa, sum(1 for d in hasil if "nomor HP" in d["periksa"] or "email gratisan" in d["periksa"]), sum(1 for d in hasil if "DUMMY?" in d["periksa"])),
          file=sys.stderr)
    for dup, asli in dobel:
        print("DUPLIKAT: '%s' sama dengan '%s'" % (dup, asli), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
