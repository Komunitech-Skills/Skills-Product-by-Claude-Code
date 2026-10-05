#!/usr/bin/env python3
"""rapikan.py - merapikan tabel CSV/TSV berantakan (daftar pelanggan, produk, penjualan).

Hanya library standar Python 3.8+. Lintas OS. Di Windows pakai `python` atau `py`.

Yang dikerjakan (tanpa menghapus data diam-diam):
  - Nama/produk/kota: spasi, huruf besar-kecil dirapikan. Nama mirip DITANDAI sebagai kelompok
    (keputusan di tangan pengguna), kecuali --gabungkan-otomatis.
  - Nomor HP -> 628xxxxxxxxxx.   - Tanggal -> YYYY-MM-DD.   - Rupiah -> bilangan bulat.
  - Duplikat persis & mirip DITANDAI (kolom _catatan / _grup_duplikat), kecuali --buang-duplikat-persis
    (itu pun ditulis ke berkas dibuang-duplikat.csv, tidak hilang).
  - Sel yang tidak bisa diperbaiki dibiarkan APA ADANYA dan dilaporkan beserta alasannya.

Ide kelompok nama mirip (kunci sidik jari / n-gram / kemiripan teks) terinspirasi konsep
"cluster and edit" di OpenRefine (BSD-3-Clause); kode ini ditulis ulang sendiri dan tidak
menyalin kode OpenRefine.

Keluaran: <folder-keluar>/<nama>-bersih.csv, laporan.json, dan ringkasan teks di layar
(diawali BLOK ANGKA TETAP yang disalin apa adanya ke balasan, lalu bagian UNTUK AGENT SAJA).
"""
import argparse
import csv
import io
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict, defaultdict
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from difflib import SequenceMatcher

VERSI = "1.0.1"

# --------------------------------------------------------------------------- umum

PLACEHOLDER_KOSONG = {"", "-", "--", "---", "n/a", "na", "n.a", "null", "none", "nil", "tidak ada",
                      "tdk ada", "kosong", "(kosong)", "?", "#n/a", "tidak tahu", "unknown"}
KARAKTER_ANEH = dict.fromkeys(map(ord, "​‌‍⁠﻿"), None)


def bersihkan_spasi(s):
    """Hapus karakter tak terlihat, ubah spasi aneh jadi spasi biasa, rapatkan spasi ganda."""
    s = s.translate(KARAKTER_ANEH).replace(" ", " ").replace(" ", " ").replace("\t", " ")
    s = re.sub(r"[\r\n]+", " ", s)
    return re.sub(r" {2,}", " ", s).strip()


def daftar_baris(nomor, batas=12):
    """[3, 5, 9] -> 'baris 3, 5, 9' (dipotong bila panjang)."""
    nomor = list(nomor)
    if len(nomor) <= min(batas, 3):
        teks = " & ".join(str(x) for x in nomor) if len(nomor) == 2 else ", ".join(str(x) for x in nomor)
    else:
        teks = ", ".join(str(x) for x in nomor[:batas])
        if len(nomor) > batas:
            teks += " dan {} baris lain".format(len(nomor) - batas)
    return "baris " + teks


def hilangkan_aksen(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


# --------------------------------------------------------------------------- baca berkas

def baca_teks(path):
    with open(path, "rb") as f:
        data = f.read()
    if b"\x00" in data[:4096]:
        raise ValueError("Berkas ini bukan teks CSV (tampak berkas biner, mungkin .xlsx). "
                         "Simpan dulu sebagai CSV dari Excel/Google Sheets.")
    for enc in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1"), "latin-1"


def deteksi_pemisah(teks):
    sampel = "\n".join(teks.splitlines()[:30])
    kandidat = [",", ";", "\t", "|"]
    try:
        d = csv.Sniffer().sniff(sampel, delimiters="".join(kandidat)).delimiter
        if d in kandidat:
            return d
    except csv.Error:
        pass
    baris = [b for b in teks.splitlines()[:30] if b.strip()]
    if not baris:
        return ","
    skor = {k: sum(b.count(k) for b in baris) for k in kandidat}
    terbaik = max(kandidat, key=lambda k: skor[k])
    return terbaik if skor[terbaik] > 0 else ","


# --------------------------------------------------------------------------- nomor HP

RE_ILMIAH = re.compile(r"^\d(\.\d+)?[eE]\+?\d+$")


def _satu_hp(teks):
    """Kembalikan (hasil, jenis, alasan_gagal). jenis: 'hp' | 'tetap'."""
    s = teks.strip()
    if RE_ILMIAH.match(s.replace(",", ".")):
        return None, None, "nomor berubah jadi notasi ilmiah oleh Excel (digitnya sudah hilang); ekspor ulang dengan kolom bertipe teks"
    s = re.sub(r"\.0+$", "", s)  # 812345678901.0 (angka float dari Excel)
    punya_plus = s.lstrip().startswith("+")
    s = re.sub(r"\(\s*0\s*\)", "", s)  # +62 (0) 812
    huruf = re.findall(r"[A-Za-z]", re.sub(r"(?i)\b(ext|x|wa|hp|telp|tlp)\b\.?", "", s))
    if huruf:
        return None, None, "ada huruf di dalam nomor"
    d = re.sub(r"\D", "", s)
    if not d:
        return None, None, "tidak ada angka"
    if d.startswith("0062"):
        d = d[2:]
    if d.startswith("62"):
        sisa = d[2:]
        if sisa.startswith("0"):
            sisa = sisa[1:]
    elif d.startswith("0"):
        sisa = d[1:]
    elif d.startswith("8"):  # nol depan hilang karena Excel
        sisa = d
    elif punya_plus:
        return None, None, "tampaknya nomor luar negeri (bukan +62)"
    else:
        return None, None, "awalan nomor tidak dikenali (bukan 08..., 62..., atau +62...)"
    if not sisa:
        return None, None, "nomor terlalu pendek"
    if sisa.startswith("80"):  # 0800/0804: bebas pulsa / layanan, bukan nomor HP
        return "62" + sisa, "tetap", None
    if sisa.startswith("8"):
        if not 9 <= len(sisa) <= 12:
            return None, None, "panjang nomor HP tidak wajar ({} angka setelah 0/62; wajar 9-12)".format(len(sisa))
        return "62" + sisa, "hp", None
    if 7 <= len(sisa) <= 11:
        return "62" + sisa, "tetap", None
    return None, None, "panjang nomor tidak wajar"


def _hp_terbaca(nilai):
    a = analisis_hp(nilai)
    return bool(a["hp"] or a["tetap"])


def analisis_hp(nilai):
    """Pisahkan isi satu sel HP. Mengembalikan dict:
    hp (nomor seluler pertama, 628..., atau None), tetap (telepon rumah/kantor, ditulis 0..., bukan WA),
    lain (nomor seluler tambahan), jumlah (banyak nomor di sel), tak_terbaca (bagian yang gagal),
    gagal (alasan bila tidak ada satu pun nomor yang bisa dipakai)."""
    bagian = [b for b in re.split(r"[/;,&]|\bdan\b|\batau\b", nilai) if re.search(r"\d", b)]
    hasil = {"hp": None, "tetap": [], "lain": [], "jumlah": len(bagian), "tak_terbaca": [], "gagal": None}
    if not bagian:
        hasil["gagal"] = "tidak ada angka"
        return hasil
    alasan_pertama = None
    for b in bagian:
        h, jenis, alasan = _satu_hp(b)
        if h is None:
            alasan_pertama = alasan_pertama or alasan
            hasil["tak_terbaca"].append(b.strip())
        elif jenis == "tetap":
            n = "0" + h[2:]
            if n not in hasil["tetap"]:
                hasil["tetap"].append(n)
        elif hasil["hp"] is None:
            hasil["hp"] = h
        elif h != hasil["hp"] and h not in hasil["lain"]:
            hasil["lain"].append(h)
    if hasil["hp"] is None and not hasil["tetap"]:
        hasil["gagal"] = alasan_pertama
    return hasil


# --------------------------------------------------------------------------- tanggal

BULAN = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "may": 5, "jun": 6, "jul": 7, "agu": 8,
         "agt": 8, "aug": 8, "sep": 9, "okt": 10, "oct": 10, "nov": 11, "des": 12, "dec": 12}
HARI = r"(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|ahad|mon|tue|wed|thu|fri|sat|sun)[a-z']*\.?,?"
RE_JAM = re.compile(r"(?i)(?:[T\s]+(?:pukul|jam)\s*)?[T\s]+\d{1,2}[:.]\d{2}(?::\d{2})?(?:\.\d+)?\s*(?:am|pm|wib|wita|wit|z)?\s*$")
RE_JAM2 = re.compile(r"(?i)\s+(?:pukul|jam)\s+\d{1,2}[:.]\d{2}.*$")


def _tgl_valid(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def _tahun(t):
    n = int(t)
    if len(t) <= 2:
        return 2000 + n if n <= 69 else 1900 + n
    return n


def normalisasi_tanggal(nilai, urutan="dmy"):
    """-> (iso|None, info dict). info: ambigu(bool), dibalik(bool), jam_dibuang(bool), serial(bool), alasan."""
    info = {"ambigu": False, "dibalik": False, "jam_dibuang": False, "serial": False, "alasan": None}
    s = bersihkan_spasi(nilai)
    if not s:
        info["alasan"] = "kosong"
        return None, info
    if re.fullmatch(r"\d{5}(\.\d+)?", s):  # nomor seri tanggal Excel
        n = int(float(s))
        if 25569 <= n <= 73050:
            info["serial"] = True
            return (date(1899, 12, 30) + timedelta(days=n)).isoformat(), info
    t = s
    if RE_JAM.search(t) and re.search(r"\d", RE_JAM.sub("", t)):
        t = RE_JAM.sub("", t).strip()
        info["jam_dibuang"] = True
    elif RE_JAM2.search(t):
        t = RE_JAM2.sub("", t).strip()
        info["jam_dibuang"] = True
    t = re.sub(r"(?i)^\s*" + HARI + r"\s*", "", t).strip()
    t = t.rstrip(".,")
    # 20261005
    m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})", t)
    if m:
        d = _tgl_valid(int(m[1]), int(m[2]), int(m[3]))
        if d and 1990 <= d.year <= 2100:
            return d.isoformat(), info
    # angka dengan pemisah
    m = re.fullmatch(r"(\d{1,4})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{1,4})", t)
    if m:
        a, b, c = m[1], m[2], m[3]
        if len(a) == 4:  # y-m-d
            d = _tgl_valid(int(a), int(b), int(c))
            if d:
                return d.isoformat(), info
            d2 = _tgl_valid(int(a), int(c), int(b))
            if d2:
                info["dibalik"] = True
                return d2.isoformat(), info
            info["alasan"] = "tanggal tidak ada di kalender"
            return None, info
        if len(c) not in (2, 4) or len(a) > 2:
            info["alasan"] = "format tanggal tidak dikenali"
            return None, info
        y = _tahun(c)
        x1, x2 = int(a), int(b)
        hari_bulan = _tgl_valid(y, x2, x1)   # dd/mm
        bulan_hari = _tgl_valid(y, x1, x2)   # mm/dd
        pilih_pertama, pilih_kedua = (hari_bulan, bulan_hari) if urutan == "dmy" else (bulan_hari, hari_bulan)
        if pilih_pertama and pilih_kedua and x1 != x2:
            info["ambigu"] = True
        if pilih_pertama:
            return pilih_pertama.isoformat(), info
        if pilih_kedua:
            info["dibalik"] = True
            return pilih_kedua.isoformat(), info
        info["alasan"] = "tanggal tidak ada di kalender (mis. 31 Februari)"
        return None, info
    # dengan nama bulan: "5 Okt 2026", "5-Okt-26", "Okt 5, 2026", "5 Oktober 2026"
    low = t.lower().replace(",", " ")
    m = re.fullmatch(r"(\d{1,2})[\s\-./]*([a-z]{3,9})[\s\-./']*(\d{2,4})", low)
    if m:
        hh, bln, th = m[1], m[2], m[3]
    else:
        m = re.fullmatch(r"([a-z]{3,9})[\s\-./]*(\d{1,2})(?:st|nd|rd|th)?[\s\-./']*(\d{2,4})", low)
        if m:
            bln, hh, th = m[1], m[2], m[3]
        else:
            info["alasan"] = "format tanggal tidak dikenali"
            return None, info
    nb = BULAN.get(bln[:3])
    if not nb or len(th) not in (2, 4):
        info["alasan"] = "nama bulan atau tahun tidak dikenali"
        return None, info
    d = _tgl_valid(_tahun(th), nb, int(hh))
    if not d:
        info["alasan"] = "tanggal tidak ada di kalender (mis. 31 Februari)"
        return None, info
    return d.isoformat(), info


def tentukan_urutan(nilai_list, paksa=None):
    """Urutan tanggal kolom: bukti dari nilai yang tidak ambigu. -> (urutan, peringatan|None)."""
    if paksa:
        return paksa, None
    dmy = mdy = 0
    for v in nilai_list:
        m = re.fullmatch(r"\s*(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{2,4})(?:[T\s].*)?", v or "")
        if m:
            a, b = int(m[1]), int(m[2])
            if a > 12 and b <= 12:
                dmy += 1
            elif b > 12 and a <= 12:
                mdy += 1
    if mdy and not dmy:
        return "mdy", "Bukti dari {} tanggal: urutan bulan/hari (gaya AS); seluruh kolom dibaca bulan/hari.".format(mdy)
    if dmy and mdy:
        return "dmy", "Kolom tanggal bercampur: {} tanggal jelas hari/bulan dan {} jelas bulan/hari. Tanggal ambigu dibaca hari/bulan.".format(dmy, mdy)
    return "dmy", None


# --------------------------------------------------------------------------- rupiah

SATUAN = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("jt", 10 ** 6), ("ribu", 10 ** 3),
          ("rb", 10 ** 3), ("k", 10 ** 3)]


def normalisasi_rupiah(nilai):
    """-> (int|None, info). info: pembulatan(bool), ambigu(bool), gratis(bool), alasan."""
    info = {"pembulatan": False, "ambigu": False, "gratis": False, "alasan": None}
    s = bersihkan_spasi(nilai)
    low = s.lower()
    if low in ("gratis", "free", "bonus"):
        info["gratis"] = True
        return 0, info
    neg = False
    if re.fullmatch(r"\(.*\)", low):
        neg, low = True, low[1:-1].strip()
    low = re.sub(r"^(idr|rp)\s*\.?\s*", "", low)
    low = re.sub(r"[,.]-+$", "", low).strip()   # "15.000,-"
    low = low.rstrip(",.-").strip()
    if low.startswith("-"):
        neg, low = True, low[1:].strip()
    kali = 1
    m = re.fullmatch(r"(.*?)\s*(miliar|milyar|juta|jt|ribu|rb|k)", low)
    if m:
        low = m[1].strip()
        kali = dict(SATUAN)[m[2]]
        suffix = True
    else:
        suffix = False
    if not low or not re.fullmatch(r"[0-9.,]+", low):
        info["alasan"] = "bukan angka rupiah yang dikenali"
        return None, info
    if re.search(r"[.,]{2}", low) or low[0] in ".,":
        info["alasan"] = "format angka tidak wajar"
        return None, info
    # tentukan pemisah desimal / ribuan
    if "," in low and "." in low:
        # pemisah yang muncul terakhir = desimal; yang lain = ribuan
        akhir = max(low.rfind(","), low.rfind("."))
        sep = low[akhir]
        lain = "." if sep == "," else ","
        belakang = low[akhir + 1:]
        depan = low[:akhir]
        if sep in depan or not re.fullmatch(r"\d{1,3}(%s\d{3})*" % re.escape(lain), depan):
            info["alasan"] = "pemisah ribuan tidak konsisten"
            return None, info
        if not belakang.isdigit() or (len(belakang) > 2 and not suffix):
            info["alasan"] = "format angka meragukan"
            return None, info
        angka = Decimal(depan.replace(lain, "") + "." + belakang)
    elif "." in low or "," in low:
        sep = "." if "." in low else ","
        bagian = low.split(sep)
        if len(bagian) > 2:
            # banyak pemisah: harus ribuan (grup 3 digit)
            if not re.fullmatch(r"\d{1,3}(%s\d{3})+" % re.escape(sep), low):
                info["alasan"] = "pemisah ribuan tidak konsisten"
                return None, info
            angka = Decimal(low.replace(sep, ""))
        else:
            belakang = bagian[1]
            if suffix:
                angka = Decimal(bagian[0] + "." + belakang)       # 1,5jt / 1.5jt
            elif len(belakang) == 3 and 1 <= len(bagian[0]) <= 3:
                angka = Decimal(bagian[0] + belakang)             # 1.500 -> 1500 (ribuan)
                if sep == ",":
                    info["ambigu"] = True                         # 1,500: ribuan gaya AS atau 1,5?
            elif len(belakang) in (1, 2):
                angka = Decimal(bagian[0] + "." + belakang)       # 15000,50
            else:
                info["alasan"] = "format angka meragukan"
                return None, info
    else:
        angka = Decimal(low)
    angka = angka * kali
    bulat = int(angka.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    if angka != bulat:
        info["pembulatan"] = True
    return (-bulat if neg else bulat), info


# --------------------------------------------------------------------------- nama

HURUF_BESAR_TETAP = {"PT", "CV", "UD", "TB", "TK", "RS", "RSU", "SD", "SMP", "SMA", "SMK", "II", "III", "IV", "KUR", "UMKM", "WA", "HP", "RT", "RW"}
KATA_KECIL = {"dan", "bin", "binti", "van", "de", "der", "al", "el", "di", "ke", "dari", "untuk", "dengan", "&"}
SAPAAN = {"bpk", "bapak", "pak", "ibu", "bu", "kak", "kakak", "mas", "mbak", "mba", "sdr", "sdri", "saudara", "saudari",
          "hj", "haji", "hajjah", "dr", "drs", "dra", "ir", "prof", "ust", "ustadz", "ustadzah"}
BADAN = {"pt", "cv", "ud", "tb", "toko", "tk", "kios", "warung", "wr"}
LIPAT = {"muh": "muhammad", "moh": "muhammad", "mhd": "muhammad", "muhd": "muhammad", "mohd": "muhammad",
         "muhamad": "muhammad", "mohamad": "muhammad", "mohammad": "muhammad", "mochammad": "muhammad",
         "moch": "muhammad",
         "jl": "jalan", "jln": "jalan", "ds": "desa", "kab": "kabupaten", "kec": "kecamatan",
         "yogya": "yogyakarta", "jogja": "yogyakarta", "jkt": "jakarta", "sby": "surabaya", "bdg": "bandung",
         "smg": "semarang", "mdn": "medan", "mks": "makassar", "plg": "palembang"}


def rapikan_nama(nilai):
    s = bersihkan_spasi(nilai)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"([,;:])(?=\S)", r"\1 ", s)
    s = re.sub(r"^[\s,.;:\-]+|[\s,;:\-]+$", "", s)
    token = s.split(" ")
    hasil = []
    for i, t in enumerate(token):
        hasil.append(_kapital_token(t, i == 0))
    return " ".join(hasil)


def _kapital_token(t, pertama):
    inti = re.sub(r"[^\w]", "", t, flags=re.UNICODE)
    if not inti:
        return t
    if inti.upper() in HURUF_BESAR_TETAP and (t.isupper() or t.islower()):
        return t.upper()
    if not pertama and t.lower() in KATA_KECIL and (t.islower() or t.isupper()):
        return t.lower()
    if re.search(r"\d", t):
        return t   # 5kg, 250ml, A4: biarkan
    if t.islower() or t.isupper():
        return re.sub(r"[A-Za-zÀ-ÿ]+", lambda m: m[0][:1].upper() + m[0][1:].lower(), t)
    return t   # huruf campur (iPhone, McDonald): biarkan


def token_kunci(nilai):
    s = hilangkan_aksen(nilai).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    out = []
    for t in s.split():
        if t in SAPAAN or t in BADAN:
            continue
        out.append(LIPAT.get(t, t))
    return out


def kunci_sidik_jari(nilai):
    """Kunci urutan-bebas: kata unik diurutkan (menangkap 'Santoso Budi' = 'Budi Santoso')."""
    return " ".join(sorted(set(token_kunci(nilai))))


def kunci_ngram(nilai, n=2):
    s = "".join(token_kunci(nilai))
    s = re.sub(r"\W", "", s)
    g = sorted(set(s[i:i + n] for i in range(len(s) - n + 1)))
    return "".join(g)


def angka_dalam(nilai):
    return tuple(re.findall(r"\d+", nilai))


class UnionFind:
    def __init__(self):
        self.p = {}

    def cari(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def gabung(self, a, b):
        self.p[self.cari(a)] = self.cari(b)


def kelompok_mirip(hitung, ambang):
    """hitung: Counter nilai_rapi -> jumlah. Kembalikan list kelompok: (metode, [nilai...])."""
    nilai = [v for v in hitung if token_kunci(v)]
    uf = UnionFind()
    metode = {}
    # 1) kunci sama (sidik jari, lalu n-gram)
    for fn, nama in ((kunci_sidik_jari, "kata sama (urutan/sapaan/singkatan beda)"),
                     (kunci_ngram, "huruf hampir sama (spasi/ejaan)")):
        grup = defaultdict(list)
        for v in nilai:
            k = fn(v)
            if k:
                grup[k].append(v)
        for isi in grup.values():
            if len(isi) > 1:
                for v in isi[1:]:
                    if angka_dalam(v) == angka_dalam(isi[0]):
                        uf.gabung(isi[0], v)
                        metode.setdefault(v, nama)
                        metode.setdefault(isi[0], nama)
    # 2) kemiripan teks (difflib) antar kunci unik
    kunci = {v: " ".join(token_kunci(v)) for v in nilai}
    urut = sorted(nilai, key=lambda v: kunci[v])
    blok = defaultdict(list)
    for v in urut:
        blok[kunci[v][:1]].append(v)
    for isi in blok.values():
        if len(isi) > 1500:   # batasi biaya pada kolom sangat beragam
            isi = isi[:1500]
        for i in range(len(isi)):
            a = kunci[isi[i]]
            if len(a) < 5:
                continue
            for j in range(i + 1, len(isi)):
                b = kunci[isi[j]]
                if len(b) < 5 or abs(len(a) - len(b)) > 3:
                    continue
                if angka_dalam(isi[i]) != angka_dalam(isi[j]):
                    continue
                if uf.cari(isi[i]) == uf.cari(isi[j]):
                    continue
                sm = SequenceMatcher(None, a, b, autojunk=False)
                if sm.real_quick_ratio() >= ambang and sm.quick_ratio() >= ambang and sm.ratio() >= ambang:
                    uf.gabung(isi[i], isi[j])
                    metode.setdefault(isi[i], "ejaan mirip (kemungkinan salah ketik)")
                    metode.setdefault(isi[j], "ejaan mirip (kemungkinan salah ketik)")
    anggota = defaultdict(list)
    for v in nilai:
        anggota[uf.cari(v)].append(v)
    hasil = []
    for isi in anggota.values():
        if len(isi) > 1:
            m = [metode[v] for v in isi if v in metode]
            hasil.append((Counter(m).most_common(1)[0][0] if m else "mirip", isi))
    return hasil


def usulan_kanonik(isi, hitung):
    """Paling sering muncul; seri -> yang punya sapaan paling sedikit, lalu terpanjang."""
    return sorted(isi, key=lambda v: (-hitung[v], len([t for t in v.lower().split() if t.strip(".") in SAPAAN]), -len(v), v))[0]


# --------------------------------------------------------------------------- deteksi kolom

POLA_HEADER = {
    "hp": re.compile(r"(?i)\b(hp|h\.p|telepon|telpon|telp|tlp|phone|mobile|whatsapp|wa|no\.? ?wa|kontak|handphone|nomor)\b"),
    "tanggal": re.compile(r"(?i)(tanggal|tgl|date|waktu|dibuat|created|jatuh tempo|kunjungan)"),
    "rupiah": re.compile(r"(?i)(harga|total|nominal|omzet|price|amount|ongkir|subtotal|diskon|biaya|bayar|saldo|gaji|nilai|\brp\b|rupiah|tagihan|piutang|hutang|utang)"),
    "nama": re.compile(r"(?i)(nama|name|pelanggan|customer|pembeli|penerima|produk|product|barang|item|kota|city|kabupaten|alamat kota|toko|supplier|pemasok)"),
}


def deteksi_kolom(header, baris_data):
    hasil = {"hp": [], "tanggal": [], "rupiah": [], "nama": []}
    alasan = {}
    n_data = max(1, len(baris_data))
    terpakai = set()
    for idx, nm in enumerate(header):
        isi = [r[idx] for r in baris_data if idx < len(r) and bersihkan_spasi(r[idx])]
        if len(isi) < max(1, int(0.3 * n_data)):
            continue
        # HP
        by_header = bool(POLA_HEADER["hp"].search(nm)) and not re.search(r"(?i)nomor (pesanan|order|resi|invoice|faktur)|no\.? ?(pesanan|order|resi|invoice|faktur)", nm)
        awalan_hp = ("08", "62", "00", "81", "82", "83", "85", "87", "88", "89")
        awalan_telp = awalan_hp + ("02", "03", "04", "05", "06", "07")   # kolom bernama HP/telp boleh berisi telepon rumah
        ok_hp = sum(1 for v in isi if _hp_terbaca(v) and re.sub(r"\D", "", v)[:2] in awalan_hp or v.strip().startswith("+62")) / len(isi)
        ok_telp = sum(1 for v in isi if _hp_terbaca(v) and re.sub(r"\D", "", v)[:2] in awalan_telp or v.strip().startswith("+62")) / len(isi)
        if (by_header and ok_telp >= 0.4) or ok_hp >= 0.8:
            hasil["hp"].append(nm)
            alasan[nm] = "hp (nama kolom/isi)"
            terpakai.add(idx)
            continue
        # tanggal
        by_header = bool(POLA_HEADER["tanggal"].search(nm))
        ok_tgl = sum(1 for v in isi if normalisasi_tanggal(v)[0]) / len(isi)
        mengandung_huruf_bulan = sum(1 for v in isi if re.search(r"(?i)[a-z]{3}", v)) / len(isi)
        if (by_header and ok_tgl >= 0.4) or (ok_tgl >= 0.8 and not all(re.fullmatch(r"\d{5,}", v.strip()) for v in isi)):
            hasil["tanggal"].append(nm)
            alasan[nm] = "tanggal (nama kolom/isi)"
            terpakai.add(idx)
            continue
        # rupiah
        by_header = bool(POLA_HEADER["rupiah"].search(nm))
        ada_tanda = sum(1 for v in isi if re.search(r"(?i)\brp\b|rp\.?\s*\d|\d\s*(rb|ribu|jt|juta|k)\b|^\d{1,3}(\.\d{3})+(,\d+)?$", v.strip())) / len(isi)
        ok_rp = sum(1 for v in isi if normalisasi_rupiah(v)[0] is not None) / len(isi)
        if (by_header and ok_rp >= 0.4) or (ada_tanda >= 0.5 and ok_rp >= 0.8):
            hasil["rupiah"].append(nm)
            alasan[nm] = "rupiah (nama kolom/isi)"
            terpakai.add(idx)
            continue
        # nama
        if POLA_HEADER["nama"].search(nm):
            teks = sum(1 for v in isi if re.search(r"[A-Za-z]{2}", v)) / len(isi)
            if teks >= 0.6:
                hasil["nama"].append(nm)
                alasan[nm] = "nama (nama kolom)"
    return hasil, alasan


def cocokkan_kolom(spesifikasi, header):
    if not spesifikasi:
        return []
    out = []
    peta = {h.strip().lower(): h for h in header}
    for bagian in re.split(r"\s*[|;]\s*|,(?=\s*\S)", spesifikasi):
        b = bagian.strip()
        if not b:
            continue
        if b.lower() in peta:
            out.append(peta[b.lower()])
        else:
            raise ValueError("Kolom '{}' tidak ditemukan. Kolom yang ada: {}".format(b, ", ".join(header)))
    return out


# --------------------------------------------------------------------------- inti

class Laporan:
    def __init__(self):
        self.perbaikan = Counter()
        self.contoh = defaultdict(list)
        self.gagal = []
        self.peringatan = []
        self.dibuang = []
        self.ambigu_tanggal = []
        self.telepon_rumah = []
        self.hp_ganda = []
        self.nama_sel_berubah = 0

    def catat(self, jenis, baris, kolom, sebelum, sesudah):
        self.perbaikan[jenis] += 1
        if len(self.contoh[jenis]) < 6:
            self.contoh[jenis].append({"baris": baris, "kolom": kolom, "sebelum": sebelum, "sesudah": sesudah})


def proses(path, opsi):
    teks, enc = baca_teks(path)
    pemisah = opsi.pemisah or deteksi_pemisah(teks)
    rows = list(csv.reader(io.StringIO(teks, newline=""), delimiter=pemisah))
    rows = [r for r in rows]
    # lewati baris kosong di awal
    awal = 0   # baris kosong di awal file tetap dihitung agar nomor baris = nomor baris di spreadsheet
    while rows and not any(c.strip() for c in rows[0]):
        rows.pop(0)
        awal += 1
    if not rows:
        raise ValueError("Berkas kosong: tidak ada baris judul maupun data.")
    header = [bersihkan_spasi(h) or "kolom_{}".format(i + 1) for i, h in enumerate(rows[0])]
    # judul kembar
    seen = Counter()
    for i, h in enumerate(header):
        seen[h] += 1
        if seen[h] > 1:
            header[i] = "{}_{}".format(h, seen[h])
    lap = Laporan()
    if len(header) == 1 and len(rows) > 1 and re.search(r"[;\t|]", rows[0][0]):
        lap.peringatan.append("Hanya terbaca 1 kolom; pemisah kolom mungkin bukan koma. Coba --pemisah ';' atau --pemisah tab.")
    n = len(header)
    data = []  # (nomor_baris, [cells])
    kosong = 0
    for i, r in enumerate(rows[1:], start=2 + awal):
        if not any(c.strip() for c in r):
            kosong += 1
            lap.dibuang.append({"baris": i, "alasan": "baris kosong"})
            continue
        norm = [bersihkan_spasi(c) for c in r]
        if [c.lower() for c in norm[:n]] == [h.lower() for h in header] and len(set(norm)) > 1:
            lap.dibuang.append({"baris": i, "alasan": "baris judul muncul lagi (file gabungan)"})
            continue
        data.append((i, r))
    # bentuk baris + catatan struktur
    tabel = []   # dict(baris, sel[list], asli[list], catatan[list])
    kelebihan = False
    for i, r in data:
        catatan = []
        sel = list(r)
        if len(sel) < n:
            catatan.append("kolom kurang ({} dari {})".format(len(sel), n))
            lap.gagal.append({"baris": i, "kolom": "(struktur)", "nilai": "", "alasan": "jumlah kolom kurang ({} dari {}); dilengkapi kosong".format(len(sel), n)})
            sel += [""] * (n - len(sel))
        elif len(sel) > n:
            extra = [c for c in sel[n:] if c.strip()]
            if extra:
                kelebihan = True
                catatan.append("kolom berlebih ({} dari {}); sisa disimpan di _kelebihan".format(len(sel), n))
                lap.gagal.append({"baris": i, "kolom": "(struktur)", "nilai": " | ".join(extra)[:80], "alasan": "jumlah kolom berlebih; kemungkinan koma/pemisah di dalam isi sel yang tidak diberi tanda kutip"})
            sel_ekstra = sel[n:]
            sel = sel[:n]
        else:
            sel_ekstra = []
        tabel.append({"baris": i, "sel": sel, "asli": list(sel), "catatan": catatan,
                      "ekstra": sel_ekstra if len(r) > n else [], "telepon_rumah": [], "nomor_lain": []})

    # spasi
    for t in tabel:
        for ci in range(n):
            b = bersihkan_spasi(t["sel"][ci])
            if b != t["sel"][ci]:
                lap.catat("spasi_dirapikan", t["baris"], header[ci], t["sel"][ci], b)
            t["sel"][ci] = b

    # kolom
    isi_data = [t["sel"] for t in tabel]
    otomatis, alasan_det = deteksi_kolom(header, isi_data)
    peta = {}
    for kunci, arg in (("nama", opsi.kolom_nama), ("hp", opsi.kolom_hp), ("tanggal", opsi.kolom_tanggal), ("rupiah", opsi.kolom_rupiah)):
        if arg is not None:
            peta[kunci] = cocokkan_kolom(arg, header)
            if arg.strip().lower() in ("-", "tidak", "none"):
                peta[kunci] = []
        else:
            peta[kunci] = list(otomatis[kunci])
    # satu kolom satu peran
    dipakai = set()
    for kunci in ("hp", "tanggal", "rupiah", "nama"):
        peta[kunci] = [c for c in peta[kunci] if c not in dipakai]
        dipakai.update(peta[kunci])
    deteksi = {k: {"kolom": v, "cara": "diberikan pengguna" if getattr(opsi, "kolom_" + k) is not None else "dideteksi otomatis"} for k, v in peta.items()}
    idx = {h: i for i, h in enumerate(header)}

    sel_kosong = Counter()
    # placeholder -> kosong
    for t in tabel:
        for kunci in peta:
            for nm in peta[kunci]:
                ci = idx[nm]
                v = t["sel"][ci]
                if v.lower() in PLACEHOLDER_KOSONG:
                    if v != "":
                        lap.catat("placeholder_jadi_kosong", t["baris"], nm, v, "")
                    t["sel"][ci] = ""
                if t["sel"][ci] == "":
                    sel_kosong[nm] += 1

    # HP
    for nm in peta["hp"]:
        ci = idx[nm]
        banyak = []
        rumah = []
        for t in tabel:
            v = t["sel"][ci]
            if not v:
                continue
            asli = t["asli"][ci]
            a = analisis_hp(v)
            if a["gagal"]:
                lap.gagal.append({"baris": t["baris"], "kolom": nm, "nilai": v, "isi_asli": asli, "alasan": a["gagal"]})
                t["catatan"].append("{}: {}".format(nm, a["gagal"]))
                continue
            if a["jumlah"] > 1:
                banyak.append(t["baris"])
                lap.hp_ganda.append({"baris": t["baris"], "kolom": nm, "isi_asli": asli, "dipakai_sebagai_hp": a["hp"],
                                     "nomor_seluler_lain": a["lain"], "telepon_rumah": a["tetap"], "bagian_tidak_terbaca": a["tak_terbaca"]})
                if a["hp"]:
                    t["catatan"].append("{}: ada lebih dari satu nomor (asli: {}); dipakai nomor seluler pertama{}".format(
                        nm, asli, ("; nomor lain dicatat: " + ", ".join(a["lain"])) if a["lain"] else ""))
                if a["tak_terbaca"]:
                    t["catatan"].append("{}: bagian yang tidak terbaca dibiarkan: {}".format(nm, ", ".join(a["tak_terbaca"])))
            if a["tetap"]:
                rumah.append(t["baris"])
                lap.telepon_rumah.append({"baris": t["baris"], "kolom": nm, "isi_asli": asli, "nomor": a["tetap"],
                                          "kolom_hp_dikosongkan": a["hp"] is None})
                t["telepon_rumah"].extend(a["tetap"])
                t["catatan"].append("{}: telepon rumah/kantor {}, bukan WhatsApp; dipindah ke kolom _telepon_rumah{}".format(
                    nm, ", ".join(a["tetap"]), "; kolom HP dikosongkan" if a["hp"] is None else ""))
            if a["lain"]:
                t["nomor_lain"].extend(a["lain"])
            hasil = a["hp"] or ""
            if hasil and hasil != v:
                lap.catat("hp_format", t["baris"], nm, v, hasil)
            t["sel"][ci] = hasil
        if banyak:
            lap.peringatan.append("Kolom {}: {} sel berisi lebih dari satu nomor ({}); nomor seluler pertama dipakai sebagai HP, yang lain dicatat.".format(nm, len(banyak), daftar_baris(banyak)))
        if rumah:
            lap.peringatan.append("Kolom {}: {} sel berisi telepon rumah/kantor ({}); bukan WhatsApp, dipisah ke kolom _telepon_rumah dan tidak ikut di kolom HP.".format(nm, len(rumah), daftar_baris(rumah)))

    # tanggal
    for nm in peta["tanggal"]:
        ci = idx[nm]
        urutan, warn = tentukan_urutan([t["sel"][ci] for t in tabel], opsi.urutan_tanggal)
        if warn:
            lap.peringatan.append("Kolom {}: {}".format(nm, warn))
        ambigu_n = dibalik_n = jam_n = serial_n = 0
        b_dibalik = []
        b_jam = []
        for t in tabel:
            v = t["sel"][ci]
            if not v:
                continue
            iso, info = normalisasi_tanggal(v, urutan)
            if iso is None:
                alasan = info["alasan"]
                lap.gagal.append({"baris": t["baris"], "kolom": nm, "nilai": v, "isi_asli": t["asli"][ci], "alasan": alasan})
                t["catatan"].append("{}: {}".format(nm, alasan))
                continue
            if info["ambigu"]:
                ambigu_n += 1
                lap.ambigu_tanggal.append({"baris": t["baris"], "kolom": nm, "nilai": v, "isi_asli": t["asli"][ci], "dibaca_sebagai": iso})
                t["catatan"].append("{}: tanggal ambigu ({}), dibaca {}".format(nm, v, "hari/bulan" if urutan == "dmy" else "bulan/hari"))
            if info["dibalik"]:
                dibalik_n += 1
                b_dibalik.append(t["baris"])
                t["catatan"].append("{}: urutan hari/bulan dibalik agar tanggal valid ({})".format(nm, v))
            jam_n += info["jam_dibuang"]
            if info["jam_dibuang"]:
                b_jam.append(t["baris"])
            serial_n += info["serial"]
            if iso != v:
                lap.catat("tanggal_format", t["baris"], nm, v, iso)
            t["sel"][ci] = iso
        if ambigu_n:
            lap.peringatan.append("Kolom {}: {} tanggal ambigu (bisa hari/bulan atau bulan/hari), dibaca {} ({}).".format(
                nm, ambigu_n, "hari/bulan (cara Indonesia)" if urutan == "dmy" else "bulan/hari",
                daftar_baris([a["baris"] for a in lap.ambigu_tanggal if a["kolom"] == nm])))
        if dibalik_n:
            lap.peringatan.append("Kolom {}: {} tanggal hanya valid bila urutannya dibalik, sudah dibalik ({}).".format(nm, dibalik_n, daftar_baris(b_dibalik)))
        if jam_n:
            lap.peringatan.append("Kolom {}: jam pada {} tanggal dibuang (hanya tanggal disimpan; {}).".format(nm, jam_n, daftar_baris(b_jam)))
        if serial_n:
            lap.peringatan.append("Kolom {}: {} tanggal berupa nomor seri Excel dikonversi.".format(nm, serial_n))

    # rupiah
    for nm in peta["rupiah"]:
        ci = idx[nm]
        pemb = amb = gr = 0
        b_pemb = []
        b_amb = []
        b_gr = []
        for t in tabel:
            v = t["sel"][ci]
            if not v:
                continue
            nilai, info = normalisasi_rupiah(v)
            if nilai is None:
                lap.gagal.append({"baris": t["baris"], "kolom": nm, "nilai": v, "isi_asli": t["asli"][ci], "alasan": info["alasan"]})
                t["catatan"].append("{}: {}".format(nm, info["alasan"]))
                continue
            if info["pembulatan"]:
                pemb += 1
                b_pemb.append(t["baris"])
                t["catatan"].append("{}: dibulatkan ke rupiah terdekat (asli {})".format(nm, v))
            if info["ambigu"]:
                amb += 1
                b_amb.append(t["baris"])
                t["catatan"].append("{}: '{}' dibaca sebagai {} (bisa juga 1,5 gaya desimal)".format(nm, v, nilai))
            gr += info["gratis"]
            if info["gratis"]:
                b_gr.append(t["baris"])
            if str(nilai) != v:
                lap.catat("rupiah_format", t["baris"], nm, v, str(nilai))
            t["sel"][ci] = str(nilai)
        if pemb:
            lap.peringatan.append("Kolom {}: {} nilai mengandung sen/desimal dan dibulatkan ke rupiah terdekat ({}).".format(nm, pemb, daftar_baris(b_pemb)))
        if amb:
            lap.peringatan.append("Kolom {}: {} nilai seperti '1,500' dibaca sebagai ribuan (1500), bukan 1,5 ({}).".format(nm, amb, daftar_baris(b_amb)))
        if gr:
            lap.peringatan.append("Kolom {}: {} nilai 'gratis' dicatat sebagai 0 ({}).".format(nm, gr, daftar_baris(b_gr)))

    # nama
    kelompok_semua = []
    gabung_pilihan = set(opsi.gabung_kelompok or [])
    if opsi.nama_baku:
        gabung_pilihan.update(opsi.nama_baku)
    for nm in peta["nama"]:
        ci = idx[nm]
        for t in tabel:
            v = t["sel"][ci]
            if not v:
                continue
            baru = rapikan_nama(v)
            if baru != t["asli"][ci]:
                lap.nama_sel_berubah += 1
            if baru != v:
                lap.catat("nama_dirapikan", t["baris"], nm, v, baru)
            t["sel"][ci] = baru
        hitung = Counter(t["sel"][ci] for t in tabel if t["sel"][ci])
        baris_per_nilai = defaultdict(list)
        for t in tabel:
            if t["sel"][ci]:
                baris_per_nilai[t["sel"][ci]].append(t["baris"])
        grup = kelompok_mirip(hitung, opsi.ambang_mirip)
        grup.sort(key=lambda g: -sum(hitung[v] for v in g[1]))
        for k, (metode, isi) in enumerate(grup, start=1):
            kanon = usulan_kanonik(isi, hitung)
            entri = {"kolom": nm, "no": len(kelompok_semua) + 1, "alasan_mirip": metode, "usulan_nama_baku": kanon,
                     "isi": [{"nilai": v, "jumlah": hitung[v],
                              "baris": baris_per_nilai[v][:12]} for v in sorted(isi, key=lambda x: -hitung[x])],
                     "digabung": False}
            if opsi.nama_baku and entri["no"] in opsi.nama_baku:
                kanon = entri["usulan_nama_baku"] = opsi.nama_baku[entri["no"]]
            if opsi.gabungkan_otomatis or entri["no"] in gabung_pilihan:
                for t in tabel:
                    if t["sel"][ci] in isi and t["sel"][ci] != kanon:
                        lap.catat("nama_digabung_otomatis", t["baris"], nm, t["sel"][ci], kanon)
                        t["sel"][ci] = kanon
                entri["digabung"] = True
            else:
                for t in tabel:
                    if t["sel"][ci] in isi:
                        t["catatan"].append("{}: nama mirip kelompok #{} (usulan: {})".format(nm, entri["no"], kanon))
            kelompok_semua.append(entri)

    # jenis tabel & duplikat
    jenis = opsi.jenis
    if jenis == "auto":
        jenis = "transaksi" if (peta["tanggal"] or peta["rupiah"]) else "daftar"
    duplikat = {"persis": [], "nomor_hp_sama": [], "hp_sama_nama_beda": []}

    def label(t):
        if peta["nama"]:
            v = t["sel"][idx[peta["nama"][0]]]
            if v:
                return v
        return next((c for c in t["sel"] if c), "")

    def isi_asli(t):
        return {"baris": t["baris"], "isi_asli": [c.strip() for c in t["asli"] if c.strip()]}

    kunci_persis = OrderedDict()
    # kolom nomor urut (No, #, ID yang semuanya beda) tidak ikut dibandingkan
    abaikan_dup = set()
    for i, h in enumerate(header):
        if re.fullmatch(r"(?i)(no\.?|nomor|nomor urut|no urut|urut|#|id)", h):
            nilai_i = [t["sel"][i] for t in tabel if t["sel"][i]]
            if len(set(nilai_i)) == len(nilai_i):
                abaikan_dup.add(i)
    for t in tabel:
        kp = (tuple("" if i in abaikan_dup else c for i, c in enumerate(t["sel"])) + tuple(t["ekstra"])
              + tuple(t["telepon_rumah"]) + tuple(t["nomor_lain"]))
        if not any(kp):
            continue
        kunci_persis.setdefault(kp, []).append(t)
    grup_id = 0
    t_dibuang = []
    for kp, daftar in kunci_persis.items():
        if len(daftar) > 1:
            grup_id += 1
            duplikat["persis"].append({"grup": grup_id, "baris": [t["baris"] for t in daftar], "label": label(daftar[0]),
                                       "isi_asli_per_baris": [isi_asli(t) for t in daftar], "contoh": {header[i]: kp[i] for i in range(min(n, len(kp))) if kp[i]}})
            for t in daftar:
                t["grup"] = "P{}".format(grup_id)
                t["catatan"].append("duplikat persis (grup P{}, baris {})".format(grup_id, ", ".join(str(x["baris"]) for x in daftar)))
            if opsi.buang_duplikat_persis:
                for t in daftar[1:]:
                    t["dibuang"] = True
                    t_dibuang.append(t)
    # nomor HP sama tapi nama (setelah dirapikan) beda: petunjuk orang yang sama
    if peta["nama"] and peta["hp"]:
        ci_n = idx[peta["nama"][0]]
        for nm in peta["hp"]:
            ci = idx[nm]
            per_hp = defaultdict(list)
            for t in tabel:
                if re.fullmatch(r"628\d{8,11}", t["sel"][ci]) and t["sel"][ci_n]:
                    per_hp[t["sel"][ci]].append(t)
            for hp, daftar in per_hp.items():
                nama_beda = sorted({t["sel"][ci_n] for t in daftar})
                if len(nama_beda) > 1:
                    duplikat["hp_sama_nama_beda"].append({
                        "hp": hp, "nama": nama_beda, "baris": [t["baris"] for t in daftar],
                        "isi_asli_per_baris": [{"baris": t["baris"], "nama_asli": t["asli"][ci_n], "hp_asli": t["asli"][ci]} for t in daftar]})
                    for t in daftar:
                        t["catatan"].append("nomor HP ini juga dipakai nama lain: " + ", ".join(x for x in nama_beda if x != t["sel"][ci_n]))
    if jenis == "daftar":
        for nm in peta["hp"]:
            ci = idx[nm]
            per_hp = defaultdict(list)
            for t in tabel:
                if t["sel"][ci] and re.fullmatch(r"628\d{8,11}", t["sel"][ci]) and "grup" not in t:
                    per_hp[t["sel"][ci]].append(t)
            for hp, daftar in per_hp.items():
                if len(daftar) > 1:
                    grup_id += 1
                    duplikat["nomor_hp_sama"].append({"grup": grup_id, "hp": hp, "baris": [t["baris"] for t in daftar],
                                                       "nama": [t["sel"][idx[peta["nama"][0]]] for t in daftar] if peta["nama"] else [],
                                                       "isi_asli_per_baris": [{"baris": t["baris"], "hp_asli": t["asli"][ci]} for t in daftar]})
                    for t in daftar:
                        t["grup"] = "H{}".format(grup_id)
                        t["catatan"].append("nomor HP sama dengan baris {} (grup H{})".format(", ".join(str(x["baris"]) for x in daftar if x is not t), grup_id))
    else:
        # transaksi: pelanggan beli berulang itu wajar. Hanya duplikat persis yang ditandai.
        pass
    for t in t_dibuang:
        lap.dibuang.append({"baris": t["baris"], "alasan": "duplikat persis (--buang-duplikat-persis); disimpan di dibuang-duplikat.csv"})

    # baris yang hanya berisi nomor urut
    for t in tabel:
        if abaikan_dup and not any(c for i, c in enumerate(t["sel"]) if i not in abaikan_dup):
            t["catatan"].append("baris hampir kosong (hanya nomor urut)")
            lap.gagal.append({"baris": t["baris"], "kolom": "(struktur)", "nilai": "", "alasan": "baris hampir kosong: hanya berisi nomor urut"})

    # kolom kosong
    kolom_kosong = [h for i, h in enumerate(header) if not any(t["sel"][i] for t in tabel)]
    buang_kolom = set(kolom_kosong) if opsi.buang_kolom_kosong else set()

    return {"enc": enc, "pemisah": pemisah, "header": header, "tabel": tabel, "lap": lap, "deteksi": deteksi,
            "alasan_det": alasan_det, "kelompok": kelompok_semua, "duplikat": duplikat, "jenis": jenis,
            "kosong": kosong, "kolom_kosong": kolom_kosong, "buang_kolom": buang_kolom, "kelebihan": kelebihan,
            "sel_kosong": sel_kosong, "jumlah_data": len(data), "idx": idx, "peta": peta, "t_dibuang": t_dibuang}


def tulis_hasil(path, hasil, opsi):
    folder = opsi.keluar or os.path.join(os.path.dirname(os.path.abspath(path)), "hasil-rapikan")
    os.makedirs(folder, exist_ok=True)
    dasar = os.path.splitext(os.path.basename(path))[0]
    berkas = os.path.join(folder, dasar + "-bersih.csv")
    header = [h for h in hasil["header"] if h not in hasil["buang_kolom"]]
    keep = [i for i, h in enumerate(hasil["header"]) if h not in hasil["buang_kolom"]]
    ada_grup = any("grup" in t for t in hasil["tabel"])
    kolom_hp = set(hasil["peta"]["hp"])
    ada_rumah = any(t["telepon_rumah"] for t in hasil["tabel"])
    ekstra = (["_catatan"] + (["_telepon_rumah"] if ada_rumah else []) + (["_grup_duplikat"] if ada_grup else [])
              + (["_kelebihan"] if hasil["kelebihan"] else []))

    def baris_csv(t):
        out = []
        for i in keep:
            v = t["sel"][i]
            if opsi.hp_untuk_excel and hasil["header"][i] in kolom_hp and re.fullmatch(r"\d{9,15}", v):
                v = '="{}"'.format(v)
            out.append(v)
        out.append("; ".join(t["catatan"]))
        if ada_rumah:
            rumah = list(t["telepon_rumah"])
            if opsi.hp_untuk_excel:
                rumah = ['="{}"'.format(x) for x in rumah]
            out.append(" / ".join(rumah))
        if ada_grup:
            out.append(t.get("grup", ""))
        if hasil["kelebihan"]:
            out.append(" | ".join(t["ekstra"]))
        return out

    with open(berkas, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header + ekstra)
        for t in hasil["tabel"]:
            if t.get("dibuang"):
                continue
            w.writerow(baris_csv(t))
    berkas_dibuang = None
    if hasil["t_dibuang"]:
        berkas_dibuang = os.path.join(folder, "dibuang-duplikat.csv")
        with open(berkas_dibuang, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["_baris_asal"] + header)
            for t in hasil["t_dibuang"]:
                w.writerow([t["baris"]] + [t["sel"][i] for i in keep])
    return folder, berkas, berkas_dibuang


def susun_laporan(path, hasil, berkas, berkas_dibuang, opsi):
    lap = hasil["lap"]
    keluar = len(hasil["tabel"]) - len(hasil["t_dibuang"])
    baris_bermasalah = len({g["baris"] for g in lap.gagal if isinstance(g["baris"], int)})
    ambil = lambda k: lap.perbaikan.get(k, 0)
    rap = {
        "spasi_dirapikan": ambil("spasi_dirapikan"), "nama_dirapikan": ambil("nama_dirapikan"),
        "hp_format": ambil("hp_format"), "tanggal_format": ambil("tanggal_format"),
        "rupiah_format": ambil("rupiah_format"), "placeholder_jadi_kosong": ambil("placeholder_jadi_kosong"),
        "nama_digabung_otomatis": ambil("nama_digabung_otomatis"),
        "nama_sel_berubah": lap.nama_sel_berubah,
    }
    laporan = {
        "versi_alat": VERSI,
        "file_masuk": os.path.basename(path),
        "file_bersih": os.path.basename(berkas),
        "file_dibuang_duplikat": os.path.basename(berkas_dibuang) if berkas_dibuang else None,
        "pemisah": {",": "koma", ";": "titik koma", "\t": "tab", "|": "garis tegak"}.get(hasil["pemisah"], hasil["pemisah"]),
        "encoding": hasil["enc"],
        "jenis_tabel": hasil["jenis"],
        "jumlah_baris_data_masuk": hasil["jumlah_data"] + hasil["kosong"] + sum(1 for d in lap.dibuang if "judul" in d["alasan"]),
        "jumlah_baris_data_isi": hasil["jumlah_data"],
        "jumlah_baris_keluar": keluar,
        "kolom": hasil["header"],
        "deteksi_kolom": hasil["deteksi"],
        "perbaikan": rap,
        "contoh_perbaikan": {k: v for k, v in lap.contoh.items()},
        "duplikat": hasil["duplikat"],
        "kelompok_nama_mirip": hasil["kelompok"],
        "tidak_bisa_diperbaiki": lap.gagal,
        "tanggal_ambigu": lap.ambigu_tanggal,
        "telepon_rumah": lap.telepon_rumah,
        "hp_ganda": lap.hp_ganda,
        "baris_dibuang": lap.dibuang,
        "sel_kosong": dict(hasil["sel_kosong"]),
        "kolom_kosong_semua": hasil["kolom_kosong"],
        "peringatan": lap.peringatan,
        "jumlah_baris_bermasalah": baris_bermasalah,
    }
    laporan["blok_angka_tetap"] = blok_angka(laporan)
    return laporan


def _label_baris(nomor):
    return daftar_baris(nomor, 15)


def blok_angka(l):
    """Daftar baris siap salin ke balasan. Semua angka & nomor baris dihitung di sini, bukan oleh agent.
    Butir yang berisi daftar baris ditulis sebagai sub-butir (satu item per baris teks)."""
    rap = l["perbaikan"]
    dup = l["duplikat"]
    kol = {k: v["kolom"] for k, v in l["deteksi_kolom"].items()}
    o = []

    def butir(judul, items=(), batas=15):
        o.append("- " + judul)
        items = list(items)
        for it in items[:batas]:
            o.append("  - " + it)
        if len(items) > batas:
            o.append("  - ... dan {} lainnya (daftar lengkap di kolom _catatan file bersih)".format(len(items) - batas))

    kosong_dibuang = [d for d in l["baris_dibuang"] if "duplikat" not in d["alasan"]]
    buang = len(l["baris_dibuang"]) - len(kosong_dibuang)
    kalimat = "Selesai dirapikan: {} baris data".format(l["jumlah_baris_data_isi"])
    if kosong_dibuang:
        kalimat += " (+{} baris kosong/judul berulang tidak dihitung)".format(len(kosong_dibuang))
    kalimat += "; di file bersih: {} baris".format(l["jumlah_baris_keluar"])
    kalimat += ", {} baris duplikat persis dibuang atas permintaan".format(buang) if buang else ", tidak ada baris yang dihapus"
    o.append(kalimat + ".")
    if kol.get("hp"):
        butir("Nomor HP diseragamkan ke format 62: {}".format(rap["hp_format"]))
        butir("Telepon rumah/kantor (bukan WhatsApp; dipisah ke kolom _telepon_rumah, tidak ada di kolom HP): {} sel".format(len(l["telepon_rumah"])),
              ['{} "{}"'.format(_label_baris([x["baris"]]), x["isi_asli"]) for x in l["telepon_rumah"]])
        butir("Sel berisi lebih dari satu nomor: {} sel".format(len(l["hp_ganda"])), [
            '{} "{}" -> dipakai sebagai HP: {}{}'.format(
                _label_baris([x["baris"]]), x["isi_asli"], x["dipakai_sebagai_hp"] or "tidak ada (tidak ada nomor seluler)",
                "; nomor lain dicatat: " + ", ".join(x["nomor_seluler_lain"]) if x["nomor_seluler_lain"] else "")
            for x in l["hp_ganda"]])
    if kol.get("tanggal"):
        butir("Tanggal diseragamkan ke YYYY-MM-DD: {}".format(rap["tanggal_format"]))
        if l["tanggal_ambigu"]:
            butir("Tanggal ambigu (bisa hari/bulan atau bulan/hari; dibaca hari/bulan kecuali ada bukti lain): {} -> {}".format(
                len(l["tanggal_ambigu"]), _label_baris([a["baris"] for a in l["tanggal_ambigu"]])))
    if kol.get("rupiah"):
        butir("Nominal rupiah jadi angka: {}".format(rap["rupiah_format"]))
    if kol.get("nama"):
        butir("Nama/produk/kota dirapikan huruf dan spasinya: {}".format(rap["nama_sel_berubah"]))
    butir("Baris kembar persis (semua kolom sama): {} grup".format(len(dup["persis"])),
          ['{} ({})'.format(_label_baris(g["baris"]), g["label"]) for g in dup["persis"]])
    if kol.get("hp") and kol.get("nama"):
        butir("Nomor HP sama tetapi nama beda (belum tentu orang yang sama, TIDAK digabung): {} kelompok".format(len(dup["hp_sama_nama_beda"])),
              ['{} ({})'.format(_label_baris(g["baris"]), " / ".join(g["nama"])) for g in dup["hp_sama_nama_beda"]])
    if dup["nomor_hp_sama"]:
        butir("Nomor HP sama, tetapi isi lain juga ada yang beda (bukan kembar persis): {} kelompok".format(len(dup["nomor_hp_sama"])),
              [_label_baris(g["baris"]) for g in dup["nomor_hp_sama"]])
    menunggu = [k for k in l["kelompok_nama_mirip"] if not k["digabung"]]
    sudah = [k for k in l["kelompok_nama_mirip"] if k["digabung"]]
    if sudah:
        butir("Nama yang sudah digabung atas persetujuan pengguna: {} kelompok ({} sel diganti)".format(len(sudah), rap["nama_digabung_otomatis"]),
              ['no. {} -> "{}"'.format(k["no"], k["usulan_nama_baku"]) for k in sudah])
    if menunggu:
        butir("Nama mirip yang menunggu keputusan: {} kelompok".format(len(menunggu)), [
            "no. {}: ".format(k["no"]) + " / ".join('"{}" ({})'.format(i["nilai"], _label_baris(i["baris"])) for i in k["isi"])
            for k in menunggu])
    gagal = sorted(l["tidak_bisa_diperbaiki"], key=lambda g: g["baris"])
    butir("Sel tidak bisa diperbaiki (dibiarkan apa adanya): {} sel di {} baris".format(len(gagal), l["jumlah_baris_bermasalah"]), [
        'baris {}{}{}: {}'.format(g["baris"], "" if g["kolom"] == "(struktur)" else " kolom " + g["kolom"],
                                  ' "{}"'.format(g["isi_asli"]) if g.get("isi_asli") else "", g["alasan"])
        for g in gagal])
    return o


def ringkasan_teks(l):
    o = []
    o.append("=== BLOK ANGKA TETAP: salin apa adanya ke balasan sebagai daftar. Angka dan nomor baris di sini SUDAH DIHITUNG; jangan dihitung ulang, jangan diganti nomor baris dari kolom 'No'. ===")
    o.extend(l["blok_angka_tetap"])
    o.append("=== AKHIR BLOK ANGKA TETAP ===")
    o.append("")
    o.append("UNTUK AGENT SAJA -- rincian tambahan. Jangan tempel mentah ke pengguna; tulis ulang dengan bahasa biasa tanpa kata script/path/JSON.")
    o.append("File: {} | pemisah: {} | encoding: {} | jenis: {}".format(l["file_masuk"], l["pemisah"], l["encoding"], l["jenis_tabel"]))
    o.append("Baris data: {} terisi, {} keluar di file bersih; dibuang: {} (kosong/judul berulang/duplikat yang diminta dibuang)".format(
        l["jumlah_baris_data_isi"], l["jumlah_baris_keluar"], len(l["baris_dibuang"])))
    for k, v in l["deteksi_kolom"].items():
        o.append("Kolom {}: {} ({})".format(k, ", ".join(v["kolom"]) or "tidak ada", v["cara"]))
    o.append("Diperbaiki: " + ", ".join("{}={}".format(k, v) for k, v in l["perbaikan"].items()))
    o.append("Duplikat persis: {} grup | HP sama (daftar): {} grup | HP sama nama beda: {} | kelompok nama mirip: {}".format(
        len(l["duplikat"]["persis"]), len(l["duplikat"]["nomor_hp_sama"]), len(l["duplikat"]["hp_sama_nama_beda"]), len(l["kelompok_nama_mirip"])))
    o.append("Tidak bisa diperbaiki: {} sel di {} baris".format(len(l["tidak_bisa_diperbaiki"]), l["jumlah_baris_bermasalah"]))
    if l["tanggal_ambigu"]:
        o.append("Tanggal ambigu: {}".format(len(l["tanggal_ambigu"])))
    for p in l["peringatan"]:
        o.append("PERINGATAN: " + p)
    if l["kolom_kosong_semua"]:
        o.append("Kolom kosong semua: " + ", ".join(l["kolom_kosong_semua"]))
    o.append("Berkas hasil: {} dan laporan.json di folder hasil.".format(l["file_bersih"]))
    return "\n".join(o)


def _daftar_int(v):
    try:
        return [int(x) for x in v.split(",") if x.strip()]
    except ValueError:
        raise argparse.ArgumentTypeError("harus daftar angka dipisah koma, mis. 1,3")


def _nama_baku(v):
    no, sep, nama = v.partition("=")
    if not sep or not no.strip().isdigit() or not nama.strip():
        raise argparse.ArgumentTypeError('harus berbentuk NOMOR=NAMA, mis. 1=Budi Santoso')
    return (int(no), rapikan_nama(nama))


def buat_parser():
    p = argparse.ArgumentParser(description="Rapikan data CSV/TSV berantakan (nama, HP, tanggal, rupiah, duplikat).")
    p.add_argument("berkas", help="file CSV/TSV masukan")
    p.add_argument("--kolom-nama", help="kolom nama/produk/kota; pisahkan beberapa kolom dengan '|' atau ';' (default: deteksi otomatis; '-' = tidak ada)")
    p.add_argument("--kolom-hp", help="kolom nomor HP (default: otomatis)")
    p.add_argument("--kolom-tanggal", help="kolom tanggal (default: otomatis)")
    p.add_argument("--kolom-rupiah", help="kolom harga/total rupiah (default: otomatis)")
    p.add_argument("--urutan-tanggal", choices=["dmy", "mdy"], help="paksa urutan tanggal ambigu: dmy=hari/bulan (default), mdy=bulan/hari")
    p.add_argument("--jenis", choices=["auto", "daftar", "transaksi"], default="auto",
                   help="daftar = 1 baris 1 pelanggan/produk (nomor HP sama ditandai); transaksi = pelanggan boleh muncul berulang")
    p.add_argument("--pemisah", help="paksa pemisah kolom (',' ';' atau tab)")
    p.add_argument("--ambang-mirip", type=float, default=0.86, help="batas kemiripan nama 0-1 (default 0.86)")
    p.add_argument("--gabungkan-otomatis", action="store_true", help="gabungkan nama mirip ke nama baku usulan (hanya bila pengguna setuju)")
    p.add_argument("--gabung-kelompok", type=_daftar_int, help="gabungkan hanya kelompok nama bernomor ini (mis. 1,3); nomor dari laporan sebelumnya")
    p.add_argument("--nama-baku", action="append", type=_nama_baku, metavar='NOMOR=NAMA', help='pakai nama baku pilihan pengguna untuk kelompok itu, mis. --nama-baku "1=Budi Santoso" (otomatis menggabungkan)')
    p.add_argument("--buang-duplikat-persis", action="store_true", help="buang duplikat persis dari file bersih (disimpan di dibuang-duplikat.csv)")
    p.add_argument("--buang-kolom-kosong", action="store_true", help="buang kolom yang kosong semua")
    p.add_argument("--hp-untuk-excel", action="store_true", help='tulis HP sebagai ="628..." agar Excel tidak mengubahnya jadi 6,28E+11')
    p.add_argument("--keluar", help="folder hasil (default: hasil-rapikan di sebelah file masukan)")
    return p


def main(argv=None):
    opsi = buat_parser().parse_args(argv)
    opsi.nama_baku = dict(opsi.nama_baku) if opsi.nama_baku else None
    if sys.stdout.encoding and sys.stdout.encoding.lower().replace("-", "") != "utf8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if not os.path.isfile(opsi.berkas):
        print("GAGAL: berkas tidak ditemukan: {}".format(opsi.berkas), file=sys.stderr)
        return 2
    if not 0 < opsi.ambang_mirip <= 1:
        print("GAGAL: --ambang-mirip harus di antara 0 dan 1", file=sys.stderr)
        return 2
    try:
        hasil = proses(opsi.berkas, opsi)
    except ValueError as e:
        print("GAGAL: {}".format(e), file=sys.stderr)
        return 2
    folder, berkas, berkas_dibuang = tulis_hasil(opsi.berkas, hasil, opsi)
    laporan = susun_laporan(opsi.berkas, hasil, berkas, berkas_dibuang, opsi)
    laporan["ringkasan_teks"] = ringkasan_teks(laporan)
    with open(os.path.join(folder, "laporan.json"), "w", encoding="utf-8") as f:
        json.dump(laporan, f, ensure_ascii=False, indent=2)
    print(laporan["ringkasan_teks"])
    print("Folder hasil: " + folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
