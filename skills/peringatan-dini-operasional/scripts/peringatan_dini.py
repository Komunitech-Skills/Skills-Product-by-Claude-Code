#!/usr/bin/env python3
"""Peringatan dini operasional harian -- Komunitech (Proprietary). Python standar saja.

Membaca log harian (CSV / TSV / titik-koma / tabel tempel ber-garis tegak "|" / .xlsx)
berisi kolom tanggal + angka operasional (output, reject, stok, pemakaian bahan,
penjualan, keluhan, telat kirim, absensi, dll.), lalu menghitung statistik sederhana
dan menandai peringatan dini 🔴/🟠/🟡 beserta alasannya dalam bahasa sehari-hari.

Pemakaian (Windows: ganti python3 dengan python atau py):
  python3 peringatan_dini.py log.csv                      # laporan teks siap kirim
  python3 peringatan_dini.py log.csv --format json        # detail angka (untuk agent)
  python3 peringatan_dini.py - < tabel.txt                # tabel ditempel lewat stdin
Opsi penting:
  --target kolom=nilai        target (maks untuk metrik "naik=buruk", min untuk "turun=buruk")
  --arah kolom=naik|turun|dua naik = makin besar makin buruk; turun = makin kecil makin buruk
  --stok STOK:PAKAI           pasangan kolom stok akhir & pemakaian harian
  --lead-time N | kolom=N     berapa hari pemasok butuh mengirim (default 2)
  --abaikan-tanggal A,B       tanggal khusus (libur nasional, event) tidak dipakai sama sekali
  --tanggal YYYY-MM-DD        tanggal laporan (default: tanggal terakhir di data)
  --duplikat terakhir|jumlah  kalau satu tanggal muncul >1 baris (default terakhir)
  --urutan-tanggal dmy|mdy    01/09/2026 = 1 Sep (dmy, default) atau 9 Jan (mdy)
Baris yang kolom tanggalnya berisi "TARGET" dibaca sebagai target tiap kolom.
Baris yang diawali "#" diabaikan (komentar).

Rumus (semua Decimal, presisi 28 digit, dibulatkan hanya saat ditampilkan):
  rata-rata 7   = rata-rata 7 angka tercatat terakhir (termasuk hari laporan)
  garis dasar   = maks. 28 angka tercatat SEBELUM hari laporan; pencilan |z|>3 dibuang sekali
  sigma (σ)     = simpangan baku sampel (n-1) garis dasar; z = (nilai hari ini - rata) / σ
  batas kendali = rata ± 2σ (waspada) dan ± 3σ (bahaya); butuh >= 14 angka garis dasar
  tren          = kemiringan regresi linear (kuadrat terkecil) atas angka dalam 7 hari
                  kalender terakhir, x = selisih hari kalender; butuh >= 5 angka; R² dilaporkan
  hari yang sama= rata-rata nilai pada hari yang sama 1-4 minggu lalu (butuh >= 2 minggu)
  sisa stok     = stok akhir / rata-rata pemakaian 7 angka terakhir (dibulatkan ke bawah 1 desimal)
Kode keluar: 0 = berhasil, 2 = input tidak bisa dibaca.
"""
import argparse
import csv
import json
import math
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal as D, InvalidOperation, getcontext

getcontext().prec = 28

VERSI = "1.0.1"
MIN_RATA7 = 7
MIN_TREN = 5
MIN_SIGMA = 14
MIN_HARI_SAMA = 2
MIN_RATA_PERSEN = D(5)  # aturan persen (banding hari yang sama) hanya bila rata-ratanya >= 5
JENDELA_DASAR = 28
HARI_TREN = 7
R2_MIN_PROYEKSI = D("0.5")
HARI_PROYEKSI = 7
# Peluang ekor satu sisi (setara 2σ / 3σ / 4σ pada distribusi normal)
P2 = 0.02275
P3 = 0.00135
P4 = 0.0000317
EFEK_RELATIF = D("0.03")        # selisih minimal 3% dari rata-rata agar σ kecil tidak memicu alarm
MAKS_LAMBDA_HITUNGAN = D(20)    # angka bulat dengan rata-rata < 20/hari -> model hitungan (Poisson)
MIN_DASAR_HITUNGAN = 7

HARI_ID = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
HARI_PANJANG = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN_ID = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
BULAN = {"jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "february": 2, "peb": 2,
         "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
         "jun": 6, "juni": 6, "june": 6, "jul": 7, "juli": 7, "july": 7, "agu": 8, "agt": 8,
         "agus": 8, "agustus": 8, "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
         "okt": 10, "oktober": 10, "oct": 10, "october": 10, "nov": 11, "nop": 11, "november": 11,
         "nopember": 11, "des": 12, "desember": 12, "dec": 12, "december": 12}
KOSONG = {"", "-", "–", "—", "n/a", "na", "null", "none", "libur", "tutup", "off", "kosong", "?"}

KATA_NAIK_BURUK = ("reject", "cacat", "rusak", "gagal", "retur", "keluhan", "komplain", "complain",
                   "telat", "terlambat", "late", "tidak_hadir", "absen", "izin", "sakit", "mangkir",
                   "downtime", "mesin_mati", "breakdown", "waste", "buang", "terbuang", "void",
                   "batal", "refund", "lembur", "kecelakaan", "susut", "sisa_produk", "tidak_laku")
KATA_TURUN_BURUK = ("output", "produksi", "hasil", "penjualan", "omzet", "omset", "transaksi",
                    "hadir", "kehadiran", "pengunjung", "order", "pesanan", "terkirim", "tepat_waktu", "sales",
                    "pendapatan", "terjual", "pengiriman")
KATA_KEJADIAN = ("kecelakaan", "k3", "cedera", "luka", "insiden", "kebakaran", "keracunan",
                 "near_miss", "nyaris_celaka", "hampir_celaka")
KATA_UANG = ("rp", "rupiah", "omzet", "omset", "nilai", "biaya", "pendapatan", "idr")
KATA_TANGGAL = ("tanggal", "tgl", "date")
KATA_CATATAN = ("catatan", "keterangan", "ket", "note", "notes", "kejadian")
KATA_STOK = ("stok", "stock", "persediaan")
KATA_PAKAI = ("pakai", "pemakaian", "terpakai", "usage", "keluar")

WARNA = {3: "🔴", 2: "🟠", 1: "🟡", 0: "✅"}
NAMA_LEVEL = {3: "merah", 2: "oranye", 1: "kuning", 0: "normal"}


class InputError(Exception):
    pass


# ----------------------------------------------------------------------------- parsing
def normalisasi(teks):
    return re.sub(r"[^a-z0-9]+", "_", str(teks).lower()).strip("_")


def _cek_ribuan(kelompok):
    return all(len(k) == 3 and k.isdigit() for k in kelompok[1:]) and kelompok[0].isdigit() \
        and 1 <= len(kelompok[0]) <= 3


def parse_angka(nilai, ambigu=None):
    """Teks angka gaya Indonesia -> Decimal. None = kosong/libur. InputError = tidak terbaca.

    "1.250" -> 1250, "1,5" -> 1.5, "1,2rb" -> 1200, "Rp 1.250.000" -> 1250000, "2,5%" -> 2.5,
    "1.250,5" -> 1250.5, "1,250.5" -> 1250.5, "1.2jt" -> 1200000, "1.250rb" -> 1250000.
    "1,250" (koma + tepat 3 angka) ditafsirkan ribuan (1250) dan dicatat di `ambigu`.
    """
    if nilai is None:
        return None
    if isinstance(nilai, D):
        return nilai
    if isinstance(nilai, int) and not isinstance(nilai, bool):
        return D(nilai)
    if isinstance(nilai, float):
        return D(repr(nilai))
    asli = str(nilai)
    s = asli.strip().lower().replace(" ", " ")
    if s in KOSONG:
        return None
    s = re.sub(r"^(rp\.?|idr)\s*", "", s)
    s = s.replace(" ", "")
    s = re.sub(r",-$", "", s)
    s = s.rstrip("%")
    kali = D(1)
    m = re.search(r"(rb|ribu|k|jt|juta)$", s)
    if m:
        kali = D(1000) if m.group(1) in ("rb", "ribu", "k") else D(1000000)
        s = s[:m.start()]
    tanda = ""
    if s and s[0] in "+-":
        tanda, s = s[0], s[1:]
    if not s or not re.fullmatch(r"[0-9.,]+", s) or not re.search(r"\d", s):
        raise InputError(f"angka tidak terbaca: {asli!r}")
    if "." in s and "," in s:
        des = "." if s.rfind(".") > s.rfind(",") else ","
        rib = "," if des == "." else "."
        bulat, pecahan = s.rsplit(des, 1)
        if des in bulat or not pecahan.isdigit() or not _cek_ribuan(bulat.split(rib)):
            raise InputError(f"angka tidak terbaca: {asli!r}")
        s = bulat.replace(rib, "") + "." + pecahan
    elif "." in s or "," in s:
        sep = "." if "." in s else ","
        bag = s.split(sep)
        if len(bag) > 2:
            if not _cek_ribuan(bag):
                raise InputError(f"angka tidak terbaca: {asli!r}")
            s = "".join(bag)
        else:
            a, b = bag
            if not b.isdigit() or (a and not a.isdigit()):
                raise InputError(f"angka tidak terbaca: {asli!r}")
            ribuan = len(b) == 3 and a and a[0] != "0" and len(a) <= 3
            if sep == "," and kali != 1:
                ribuan = False
            if ribuan:
                s = a + b
                if sep == "," and ambigu is not None:
                    ambigu.append(asli)
            else:
                s = (a or "0") + "." + b
    try:
        return D(tanda + s) * kali
    except InvalidOperation:
        raise InputError(f"angka tidak terbaca: {asli!r}")


def parse_tanggal(nilai, urutan="dmy"):
    if isinstance(nilai, datetime):
        return nilai.date()
    if isinstance(nilai, date):
        return nilai
    if isinstance(nilai, (D, int, float)) and not isinstance(nilai, bool):
        serial = D(str(nilai))
        if 20000 <= serial <= 80000:  # nomor seri tanggal Excel
            return date(1899, 12, 30) + timedelta(days=int(serial))
        raise InputError(f"tanggal tidak terbaca: {nilai!r}")
    s = str(nilai).strip().lower()
    s = re.sub(r"^[a-z']+,?\s+(?=\d)", "", s)  # "Senin, 1 Sep 2026" / "sen 01/09/2026"
    try:
        m = re.match(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:[ t].*)?$", s)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.match(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})(?:\s.*)?$", s)
        if m:
            a, b, th = int(m.group(1)), int(m.group(2)), int(m.group(3))
            th = th + 2000 if th < 100 else th
            return date(th, b, a) if urutan == "dmy" else date(th, a, b)
        m = re.match(r"^(\d{1,2})[\s-]+([a-z]+)\.?[\s-]+(\d{2}|\d{4})$", s)
        if m and m.group(2) in BULAN:
            th = int(m.group(3))
            th = th + 2000 if th < 100 else th
            return date(th, BULAN[m.group(2)], int(m.group(1)))
    except ValueError:
        pass
    raise InputError(f"tanggal tidak terbaca: {nilai!r}")


def baca_teks(teks):
    baris = [b for b in teks.splitlines() if b.strip() and not b.lstrip().startswith("#")]
    if not baris:
        raise InputError("file/tabel kosong")
    if baris[0].strip().startswith("|"):
        hasil = []
        for b in baris:
            sel = [c.strip() for c in b.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in sel if c):
                continue
            hasil.append(sel)
        return hasil
    kepala = baris[0]
    hitung = {d: kepala.count(d) for d in ("\t", ";", "|", ",")}
    delim = max(hitung, key=lambda d: hitung[d]) if max(hitung.values()) > 0 else ","
    return [[c.strip() for c in r] for r in csv.reader(baris, delimiter=delim)]


def baca_xlsx(path):
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rel_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    try:
        z = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as e:
        raise InputError(f"file Excel tidak bisa dibuka ({e}); simpan ulang sebagai CSV")
    with z:
        nama = set(z.namelist())
        teks_bersama = []
        if "xl/sharedStrings.xml" in nama:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(ns + "si"):
                teks_bersama.append("".join(t.text or "" for t in si.iter(ns + "t")))
        lembar = "xl/worksheets/sheet1.xml"
        try:
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            s1 = wb.find(f"{ns}sheets/{ns}sheet")
            rid = s1.get(rel_ns + "id")
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")):
                if r.get("Id") == rid:
                    t = r.get("Target")
                    lembar = t.lstrip("/") if t.startswith("/") else "xl/" + t
        except (KeyError, AttributeError, ET.ParseError):
            pass
        if lembar not in nama:
            raise InputError("lembar pertama file Excel tidak ditemukan; simpan ulang sebagai CSV")
        hasil = []
        for row in ET.fromstring(z.read(lembar)).iter(ns + "row"):
            sel = {}
            urut = 0
            for c in row.findall(ns + "c"):
                ref = c.get("r")
                if ref:
                    huruf = re.match(r"[A-Z]+", ref).group(0)
                    urut = 0
                    for h in huruf:
                        urut = urut * 26 + (ord(h) - 64)
                    urut -= 1
                t = c.get("t")
                v = c.find(ns + "v")
                if t == "s" and v is not None:
                    isi = teks_bersama[int(v.text)]
                elif t == "inlineStr":
                    isi = "".join(x.text or "" for x in c.iter(ns + "t"))
                elif v is None or v.text is None:
                    isi = ""
                elif t in (None, "n"):
                    try:
                        isi = D(v.text)
                    except InvalidOperation:
                        isi = v.text
                else:
                    isi = v.text
                sel[urut] = isi
                urut += 1
            if sel:
                hasil.append([sel.get(i, "") for i in range(max(sel) + 1)])
    hasil = [r for r in hasil if any(str(x).strip() for x in r)]
    if hasil and str(hasil[0][0]).strip().startswith("#"):
        hasil = [r for r in hasil if not str(r[0]).strip().startswith("#")]
    return hasil


def baca_tabel(path):
    if path == "-":
        return baca_teks(sys.stdin.read())
    low = path.lower()
    if low.endswith((".xlsx", ".xlsm")):
        return baca_xlsx(path)
    if low.endswith(".xls"):
        raise InputError("format .xls lama belum didukung; di Excel pilih File > Save As > CSV atau .xlsx")
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except OSError as e:
        raise InputError(f"file tidak bisa dibuka: {e}")
    if mentah[:2] == b"PK":
        return baca_xlsx(path)
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return baca_teks(mentah.decode(enc))
        except UnicodeDecodeError:
            continue
    raise InputError("encoding file tidak dikenali; simpan ulang sebagai CSV UTF-8")


# ----------------------------------------------------------------------------- struktur data
SATUAN = {"pcs": "pcs", "kg": "kg", "gr": "gr", "g": "g", "rp": "Rp", "idr": "Rp", "liter": "liter",
          "ltr": "liter", "l": "liter", "pack": "pack", "box": "box", "dus": "dus", "orang": "orang",
          "jam": "jam", "menit": "menit", "persen": "%", "pct": "%", "unit": "unit", "porsi": "porsi",
          "m": "m", "meter": "m", "cm": "cm", "lembar": "lembar", "roll": "roll", "karung": "karung",
          "sak": "sak", "botol": "botol"}


def label_cantik(h):
    """'stok_tepung_kg' -> 'Stok tepung (kg)'; judul yang sudah berspasi dibiarkan."""
    h = str(h).strip()
    if "_" in h and " " not in h:
        bag = [b for b in h.split("_") if b]
        satuan = SATUAN.get(bag[-1].lower()) if len(bag) > 1 else None
        h = " ".join(bag[:-1] if satuan else bag) + (f" ({satuan})" if satuan else "")
    return h[:1].upper() + h[1:]


def cocok(nama_norm, kata):
    bagian = nama_norm.split("_")
    for k in kata:
        if "_" in k:
            if k in nama_norm:
                return True
        elif any(b == k or b.startswith(k) for b in bagian):
            return True
    return False


def tebak_arah(nama_norm):
    if cocok(nama_norm, KATA_NAIK_BURUK):
        return "naik"
    if cocok(nama_norm, KATA_TURUN_BURUK):
        return "turun"
    return "dua"


def susun_data(tabel, args, catatan):
    if len(tabel) < 2:
        raise InputError("tabel hanya berisi judul kolom, belum ada baris data")
    kepala = [str(h).strip() for h in tabel[0]]
    norm = [normalisasi(h) or f"kolom_{i + 1}" for i, h in enumerate(kepala)]
    idx_tgl = next((i for i, n in enumerate(norm) if cocok(n, KATA_TANGGAL)), None)
    if idx_tgl is None:
        idx_tgl = 0
        catatan.append(f"Kolom tanggal tidak berjudul 'tanggal'; kolom pertama ({kepala[0]!r}) dipakai sebagai tanggal.")
    abaikan = set()
    for t in args.abaikan_tanggal or []:
        for bag in t.split(","):
            if bag.strip():
                abaikan.add(parse_tanggal(bag.strip(), args.urutan_tanggal))

    target_baris = {}
    per_tanggal = {}
    dilewati = []
    duplikat = []
    lebih_panjang = 0
    for no, r in enumerate(tabel[1:], start=2):
        r = list(r)
        if len(r) > len(kepala):
            if any(str(x).strip() for x in r[len(kepala):]):
                lebih_panjang += 1
            r = r[:len(kepala)]
        r += [""] * (len(kepala) - len(r))
        sel_tgl = r[idx_tgl]
        if str(sel_tgl).strip().lower() in ("target", "sasaran", "batas"):
            target_baris = {i: r[i] for i in range(len(r)) if i != idx_tgl}
            continue
        if not str(sel_tgl).strip():
            dilewati.append(f"baris {no}: tanggal kosong")
            continue
        try:
            tgl = parse_tanggal(sel_tgl, args.urutan_tanggal)
        except InputError as e:
            dilewati.append(f"baris {no}: {e}")
            continue
        if tgl in abaikan:
            continue
        if tgl in per_tanggal:
            duplikat.append(tgl)
            if args.duplikat == "jumlah":
                per_tanggal[tgl].append((no, r))
            else:
                per_tanggal[tgl] = [(no, r)]
        else:
            per_tanggal[tgl] = [(no, r)]
    if lebih_panjang:
        catatan.append(f"{lebih_panjang} baris punya sel lebih banyak dari judul kolom (kemungkinan koma di dalam angka tanpa tanda kutip); sel lebihnya diabaikan -- cek file.")
    saran_mdy = args.urutan_tanggal == "dmy" and any(
        re.search(r"'\d{1,2}[-/.](1[3-9]|2\d|3[01])[-/.]\d{2,4}", d) for d in dilewati)
    if saran_mdy:
        catatan.append("Beberapa tanggal tampaknya format bulan/hari (AS), mis. 09/13/2026. Jalankan ulang dengan --urutan-tanggal mdy.")
    if not per_tanggal:
        raise InputError("tidak ada baris dengan tanggal yang terbaca. " + "; ".join(dilewati[:3])
                         + (" -- tampaknya format bulan/hari (AS): coba --urutan-tanggal mdy" if saran_mdy else ""))

    # kolom angka vs teks
    kolom = []
    ambigu = []
    sel_rusak = []
    for i, h in enumerate(kepala):
        if i == idx_tgl:
            continue
        nilai = {}
        terbaca = gagal = 0
        rusak_kolom = []
        for tgl, isi in per_tanggal.items():
            total = None
            ada = False
            for no, r in isi:
                try:
                    v = parse_angka(r[i], ambigu)
                except InputError:
                    gagal += 1
                    rusak_kolom.append(f"{h} baris {no}: {r[i]!r}")
                    continue
                if v is None:
                    continue
                if v < 0:
                    rusak_kolom.append(f"{h} baris {no}: nilai negatif {r[i]!r} diabaikan")
                    continue
                ada = True
                terbaca += 1
                total = v if total is None else total + v
            if ada:
                nilai[tgl] = total
        kosong_semua = terbaca == 0 and gagal == 0
        if terbaca and terbaca >= 0.6 * (terbaca + gagal):
            sel_rusak.extend(rusak_kolom)
            kolom.append({"kolom": norm[i], "label": label_cantik(h), "indeks": i, "nilai": nilai})
        elif cocok(norm[i], KATA_CATATAN):
            teks = {tgl: " / ".join(str(r[i]).strip() for _, r in isi if str(r[i]).strip())
                    for tgl, isi in per_tanggal.items()}
            kolom.append({"kolom": norm[i], "label": h, "indeks": i, "teks": teks})
        elif not kosong_semua and terbaca == 0:
            catatan.append(f"Kolom teks {h!r} diabaikan dan tidak pernah dikutip di laporan (bisa berisi nama orang).")
        elif kosong_semua:
            catatan.append(f"Kolom {h!r} kosong semua, diabaikan.")
        else:
            catatan.append(f"Kolom {h!r} campuran angka & teks ({terbaca} angka, {gagal} tidak terbaca), diabaikan -- rapikan dulu bila ingin dianalisis.")
    if not any("nilai" in k for k in kolom):
        raise InputError("tidak ada kolom angka yang terbaca selain tanggal (log belum diisi, atau angkanya tertulis sebagai teks)")

    targets = {}
    for k in kolom:
        if "nilai" in k and k["indeks"] in target_baris:
            try:
                t = parse_angka(target_baris[k["indeks"]])
            except InputError:
                catatan.append(f"Target kolom {k['label']!r} tidak terbaca: {target_baris[k['indeks']]!r}")
                t = None
            if t is not None:
                targets[k["kolom"]] = t
    return {"kolom": kolom, "tanggal": sorted(per_tanggal), "dilewati": dilewati,
            "duplikat": sorted(set(duplikat)), "ambigu": ambigu, "sel_rusak": sel_rusak,
            "targets": targets, "abaikan": sorted(abaikan)}


# ----------------------------------------------------------------------------- statistik
def rata(xs):
    return sum(xs, D(0)) / len(xs)


def sd_sampel(xs):
    if len(xs) < 2:
        return None
    m = rata(xs)
    return (sum(((x - m) ** 2 for x in xs), D(0)) / (len(xs) - 1)).sqrt()


def regresi(titik):
    """titik = [(x_hari, y)] -> (kemiringan per hari, R²) atau (None, None)."""
    n = len(titik)
    if n < 2:
        return None, None
    mx = rata([D(x) for x, _ in titik])
    my = rata([y for _, y in titik])
    sxx = sum(((D(x) - mx) ** 2 for x, _ in titik), D(0))
    sxy = sum(((D(x) - mx) * (y - my) for x, y in titik), D(0))
    syy = sum(((y - my) ** 2 for _, y in titik), D(0))
    if sxx == 0:
        return None, None
    b = sxy / sxx
    r2 = (sxy * sxy) / (sxx * syy) if syy != 0 else D(0)
    return b, r2


def garis_dasar(titik):
    """titik = [(tanggal, nilai)] sebelum hari laporan -> dict statistik garis dasar."""
    nilai = [v for _, v in titik]
    hasil = {"n": len(nilai), "pencilan_diabaikan": []}
    if len(nilai) < 2:
        return hasil
    m, s = rata(nilai), sd_sampel(nilai)
    if len(nilai) >= MIN_SIGMA and s and s > 0:
        bersih = [(t, v) for t, v in titik if abs(v - m) / s <= 3]
        if len(bersih) < len(titik) and sd_sampel([v for _, v in bersih]):
            hasil["pencilan_diabaikan"] = [t.isoformat() for t, v in titik if abs(v - m) / s > 3]
            nilai = [v for _, v in bersih]
            m, s = rata(nilai), sd_sampel(nilai)
    hasil.update({"n": len(nilai), "rata": m, "sd": s})
    return hasil


def beruntun(titik, arah):
    """Jumlah kenaikan (arah='naik') / penurunan berturut-turut yang berakhir di titik terakhir."""
    k = 0
    for i in range(len(titik) - 1, 0, -1):
        (t0, a), (t1, b) = titik[i - 1], titik[i]
        if (t1 - t0).days > 3:
            break
        if (arah == "naik" and b > a) or (arah == "turun" and b < a):
            k += 1
        else:
            break
    return k


def sisi_beruntun(titik, m, arah):
    """Berapa angka terakhir berturut-turut berada di sisi buruk rata-rata garis dasar."""
    k = 0
    for _, v in reversed(titik):
        if (arah == "naik" and v > m) or (arah == "turun" and v < m):
            k += 1
        else:
            break
    return k


# ----------------------------------------------------------------------------- format
def fmt_angka(x, uang=False, des=2):
    if x is None:
        return "-"
    if uang:
        q = D(x).quantize(D(1), rounding=ROUND_HALF_UP)
        return "Rp " + f"{int(q):,}".replace(",", ".")
    q = D(x).quantize(D(1).scaleb(-des), rounding=ROUND_HALF_UP)
    tanda = "-" if q < 0 else ""
    q = abs(q)
    bulat = int(q)
    pecahan = str(q - bulat)[2:].rstrip("0") if q != bulat else ""
    s = f"{bulat:,}".replace(",", ".")
    return tanda + s + ("," + pecahan if pecahan else "")


def fmt_satu(x):
    """Selalu 1 angka desimal dengan koma: 7 -> '7,0', 6.79 -> '6,8'."""
    return str(D(x).quantize(D("0.1"), rounding=ROUND_HALF_UP)).replace(".", ",")


def fmt_tgl(t, panjang=False):
    return f"{HARI_ID[t.weekday()]}, {t.day} {BULAN_ID[t.month - 1]}" + (f" {t.year}" if panjang else "")


def bulat(x, des=2):
    return None if x is None else str(D(x).quantize(D(1).scaleb(-des), rounding=ROUND_HALF_UP))


# ----------------------------------------------------------------------------- evaluasi metrik
def ekor_normal(z):
    """P(Z >= z) untuk normal baku (satu sisi)."""
    return 0.5 * math.erfc(float(z) / math.sqrt(2))


def ekor_poisson(x, lam, arah):
    """arah 'naik': P(X >= x); 'turun': P(X <= x), X ~ Poisson(lam). Dihitung langsung per suku."""
    lam, x = float(lam), int(x)
    if lam <= 0:
        return 0.0 if (arah == "naik" and x > 0) else 1.0

    def pmf(k):
        return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))
    if arah == "naik":
        if x <= 0:
            return 1.0
        total, k = 0.0, x
        while True:
            suku = pmf(k)
            total += suku
            if k > lam and suku < 1e-18:
                break
            k += 1
        return min(1.0, total)
    return min(1.0, sum(pmf(k) for k in range(0, max(x, -1) + 1)))


def peluang_teks(p):
    if p <= 0.0001:
        return "sangat jarang terjadi kebetulan (< 1 dari 10.000 hari)"
    n = 1 / p
    bulat_n = int(round(n, -1)) if n >= 20 else int(round(n))
    return f"peluang kebetulan ±1 dari {fmt_angka(bulat_n)} hari"


def level_dari_peluang(p, efek, p_lalu):
    """p = peluang hari ini; efek = level maksimum yang diizinkan besar selisih;
    p_lalu = peluang 2 angka sebelumnya (hanya yang efeknya juga cukup), terbaru dulu."""
    lv = 0
    kemarin = p_lalu[0] if p_lalu else 1.0
    if p <= P2:
        lv = 1
    if p <= P3 or (p <= P2 and any(q <= P2 for q in p_lalu[:2])):
        lv = 2
    if p <= P4 or (p <= P3 and kemarin <= P2):
        lv = 3
    return min(lv, efek)


def evaluasi_metrik(k, arah, target, tgl_lap, uang, kejadian=False):
    titik = sorted(k["nilai"].items())
    h = {"kolom": k["kolom"], "label": k["label"], "arah": arah, "uang": uang, "n": len(titik),
         "target": target, "level": 0, "alasan": [], "butuh_data": []}
    if k.get("sumber"):
        h["sumber"] = k["sumber"]
    if not titik:
        h["butuh_data"].append("belum ada angka")
        return h
    t_akhir, v_akhir = titik[-1]
    h["terbaru"] = {"tanggal": t_akhir.isoformat(), "nilai": v_akhir}
    if t_akhir != tgl_lap:
        h["tidak_diisi_hari_ini"] = True
        return h
    lvl = [0]

    def naikkan(level, teks):
        lvl[0] = max(lvl[0], level)
        h["alasan"].append((level, teks))

    kata_buruk = {"naik": ("naik", "di atas"), "turun": ("turun", "di bawah")}

    if len(titik) >= 2:
        h["sebelumnya"] = {"tanggal": titik[-2][0].isoformat(), "nilai": titik[-2][1]}

    # rata-rata 7
    if len(titik) >= MIN_RATA7:
        h["rata7"] = rata([v for _, v in titik[-7:]])
        if len(titik) >= 2 * MIN_RATA7:
            h["rata7_sebelumnya"] = rata([v for _, v in titik[-14:-7]])
            if h["rata7_sebelumnya"] != 0:
                h["perubahan7_persen"] = (h["rata7"] - h["rata7_sebelumnya"]) / h["rata7_sebelumnya"] * 100
    else:
        h["butuh_data"].append(f"rata-rata 7 hari butuh {MIN_RATA7} hari (ada {len(titik)})")

    # garis dasar & sigma (untuk JSON & model normal)
    jendela_dasar = titik[:-1][-JENDELA_DASAR:]
    dasar = garis_dasar(jendela_dasar)
    h["dasar"] = dasar
    z = None
    if dasar["n"] >= MIN_SIGMA and dasar.get("sd"):
        m, s = dasar["rata"], dasar["sd"]
        dasar.update({"batas_atas_2": m + 2 * s, "batas_atas_3": m + 3 * s,
                      "batas_bawah_2": max(D(0), m - 2 * s), "batas_bawah_3": max(D(0), m - 3 * s)})
        z = (v_akhir - m) / s
        h["z"] = z

    # pilih model
    mentah = [v for _, v in jendela_dasar]
    semua_bulat = all(v == v.to_integral_value() for v in mentah + [v_akhir])
    if kejadian:
        model = "kejadian"
    elif len(mentah) >= MIN_DASAR_HITUNGAN and semua_bulat and rata(mentah) < MAKS_LAMBDA_HITUNGAN:
        model = "hitungan"
    elif dasar["n"] >= MIN_SIGMA and dasar.get("sd"):
        model = "normal"
    elif dasar["n"] >= MIN_DASAR_HITUNGAN and dasar.get("sd") == 0:
        model = "konstan"
    else:
        model = None
        h["butuh_data"].append(f"batas kendali (σ) butuh {MIN_SIGMA} hari sebelum hari ini (ada {dasar['n']})")
    h["model"] = model
    if model == "hitungan":
        lam = rata(mentah)
        h["hitungan"] = {"n": len(mentah), "lambda": lam, "maks_sebelumnya": max(mentah),
                         "sd": sd_sampel(mentah)}

    # tren
    awal = tgl_lap - timedelta(days=HARI_TREN - 1)
    jendela = [(t, v) for t, v in titik if t >= awal]
    if len(jendela) >= MIN_TREN:
        b, r2 = regresi([((t - awal).days, v) for t, v in jendela])
        if b is not None:
            h["tren"] = {"n": len(jendela), "kemiringan_per_hari": b, "r2": r2}
    else:
        h["butuh_data"].append(f"tren butuh {MIN_TREN} angka dalam 7 hari terakhir (ada {len(jendela)})")

    # hari yang sama 1-4 minggu lalu
    peta = dict(titik)
    sama = [peta[tgl_lap - timedelta(days=7 * w)] for w in range(1, 5) if tgl_lap - timedelta(days=7 * w) in peta]
    if len(sama) >= MIN_HARI_SAMA:
        rs = rata(sama)
        h["hari_sama"] = {"n": len(sama), "rata": rs,
                          "selisih_persen": (v_akhir - rs) / rs * 100 if rs != 0 else None}
    else:
        h["butuh_data"].append(f"banding hari {HARI_PANJANG[tgl_lap.weekday()]} butuh {MIN_HARI_SAMA} minggu sebelumnya (ada {len(sama)})")

    h["naik_beruntun"] = beruntun(titik, "naik")
    h["turun_beruntun"] = beruntun(titik, "turun")

    # kejadian (K3, kecelakaan): setiap kejadian = merah
    if model == "kejadian":
        if v_akhir > 0:
            naikkan(3, f"{fmt_angka(v_akhir)} kejadian hari ini -- setiap kejadian wajib ditindaklanjuti & dicatat hari ini")

    def basis_untuk(i):
        """Garis dasar untuk angka ke-i dari belakang (1 = hari ini), dari angka SEBELUM angka itu."""
        if i == 1:
            return {"dasar": dasar, "mentah": mentah}
        jd = titik[:-i][-JENDELA_DASAR:]
        return {"dasar": garis_dasar(jd), "mentah": [v for _, v in jd]}

    def sinyal(v, a, basis):
        """-> (peluang ekor ke arah buruk, level maksimum yang diizinkan besar selisih)."""
        tanda = D(1) if a == "naik" else D(-1)
        dasar_b, mentah_b = basis["dasar"], basis["mentah"]
        if model == "normal":
            if dasar_b["n"] < MIN_SIGMA or not dasar_b.get("sd"):
                return 1.0, 0
            m, s = dasar_b["rata"], dasar_b["sd"]
            zz = (v - m) / s * tanda
            if zz <= 0:
                return 1.0, 0
            rel_ok = m == 0 or abs(v - m) / abs(m) >= EFEK_RELATIF
            return ekor_normal(zz), (3 if rel_ok else 0)
        if model == "hitungan":
            if len(mentah_b) < MIN_DASAR_HITUNGAN:
                return 1.0, 0
            lam = rata(mentah_b)
            lam_ef = max(lam, D("0.5") / len(mentah_b))
            selisih = (v - lam_ef) * tanda
            if selisih <= 0:
                return 1.0, 0
            p = ekor_poisson(v, lam_ef, a)
            sd = sd_sampel(mentah_b)
            if sd and sd > 0 and len(mentah_b) >= MIN_SIGMA:
                p = max(p, ekor_normal((v - lam) / sd * tanda))
            efek = 3 if selisih >= D("2.5") else (2 if selisih >= D("1.5") else (1 if selisih >= 1 else 0))
            return p, efek
        return 1.0, 0

    arah_cek = [arah] if arah in ("naik", "turun") else ["naik", "turun"]
    for a in arah_cek:
        if model == "kejadian":
            break
        kata, posisi = kata_buruk[a]
        tanda = D(1) if a == "naik" else D(-1)
        pusat = None
        if model in ("normal", "hitungan"):
            p, efek = sinyal(v_akhir, a, basis_untuk(1))
            p_lalu = []
            for i in (2, 3):
                if len(titik) > i and (titik[-i + 1][0] - titik[-i][0]).days <= 3:
                    pl, el = sinyal(titik[-i][1], a, basis_untuk(i))
                    p_lalu.append(pl if el >= 1 else 1.0)
                else:
                    break
            lv = level_dari_peluang(p, efek, p_lalu)
            h.setdefault("peluang", {})[a] = p
            bertahan = p <= P2 and any(q <= P2 for q in p_lalu[:2])
            ekor = " (2 dari 3 hari terakhir)" if bertahan else ""
            if model == "normal":
                pusat, sref = dasar["rata"], dasar["sd"]
                if lv:
                    zz = abs(z)
                    batas = " -- lewat batas bahaya 3σ" if zz >= 3 else (" -- lewat batas waspada 2σ" if zz >= 2 else "")
                    naikkan(lv, f"{fmt_satu(zz)}σ {posisi} rata-rata {dasar['n']} hari sebelumnya ({fmt_angka(pusat, uang)}){batas}{ekor}")
            else:
                pusat = h["hitungan"]["lambda"]
                sref = pusat.sqrt() if pusat > 0 else D(1)
                biasa = "biasanya 0" if pusat == 0 else f"biasanya ±{fmt_angka(pusat, des=1)}/hari"
                if lv:
                    naikkan(lv, f"{biasa} ({len(mentah)} hari sebelumnya), hari ini {fmt_angka(v_akhir)} -- {peluang_teks(p)}{ekor}")
                if (a == "naik" and pusat < 1 and v_akhir > h["hitungan"]["maks_sebelumnya"]
                        and v_akhir - pusat >= 1 and lv == 0):
                    naikkan(1, f"biasanya hampir selalu 0; hari ini {fmt_angka(v_akhir)} -- tertinggi dalam {len(mentah)} hari tercatat")
            # pola bergeser
            k7 = sisi_beruntun(titik, pusat, a)
            if k7 >= 7:
                rk = rata([v for _, v in titik[-k7:]])
                cukup = abs(rk - pusat) >= max(EFEK_RELATIF * abs(pusat), sref / 2)
                if cukup:
                    naikkan(2 if k7 >= 9 else 1, f"{k7} hari tercatat berturut-turut {posisi} rata-rata -- pola bergeser, bukan kebetulan sehari")
        elif model == "konstan":
            m = dasar["rata"]
            d = (v_akhir - m) * tanda
            if d > 0:
                rel = d / abs(m) if m != 0 else D(1)
                lv = 3 if rel >= D("0.5") else (2 if rel >= D("0.2") else (1 if rel >= D("0.05") else 0))
                if lv:
                    naikkan(lv, f"biasanya selalu {fmt_angka(m, uang)} ({dasar['n']} hari), hari ini {kata} {fmt_angka(rel * 100, des=0)}%")
            pusat = m
        # beruntun (hanya bila hari ini memang di sisi buruk rata-rata)
        kb = h["naik_beruntun"] if a == "naik" else h["turun_beruntun"]
        sisi_buruk = pusat is None or (v_akhir - pusat) * tanda > 0
        if sisi_buruk and kb >= 5:
            naikkan(2 if arah != "dua" else 1, f"{kata} {kb} hari berturut-turut")
        elif sisi_buruk and kb >= 3 and arah != "dua":
            naikkan(1, f"{kata} {kb} hari berturut-turut")
        # hari yang sama (hanya kuning; butuh selisih bermakna)
        hs = h.get("hari_sama")
        if hs and hs["selisih_persen"] is not None and arah != "dua" and hs["rata"] >= MIN_RATA_PERSEN:
            pr = hs["selisih_persen"] * tanda
            if model == "normal":
                sref_hs = dasar["sd"]
            elif model == "hitungan":
                sref_hs = hs["rata"].sqrt()
            else:
                sref_hs = None
            cukup = (abs(v_akhir - hs["rata"]) >= 2 * sref_hs) if sref_hs else pr >= 35
            if pr >= 25 and cukup:
                label_hari = HARI_PANJANG[tgl_lap.weekday()]
                naikkan(1, f"{fmt_angka(abs(hs['selisih_persen']), des=0)}% {posisi} rata-rata hari {label_hari} {hs['n']} minggu terakhir ({fmt_angka(hs['rata'], uang)})")

    # target
    if target is not None and arah in ("naik", "turun"):
        buruk = (lambda v: v > target) if arah == "naik" else (lambda v: v < target)
        langgar7 = sum(1 for _, v in titik[-7:] if buruk(v))
        info = {"selisih": v_akhir - target, "langgar_7": langgar7, "n_7": len(titik[-7:])}
        if target != 0:
            info["selisih_persen"] = (v_akhir - target) / target * 100
        h["target_info"] = info
        jenis = "maks" if arah == "naik" else "min"
        kata_gagal = "melewati target" if arah == "naik" else "di bawah target"
        if buruk(v_akhir):
            if target != 0:
                rel = abs(info["selisih_persen"])
                lv = 3 if rel >= 50 else (2 if rel >= 10 else 1)
                persen = f" ({'+' if arah == 'naik' else '-'}{fmt_angka(rel, des=0)}%)"
            else:
                lv, persen = 2, ""
            if langgar7 >= 3:
                lv = max(lv, 2)
            naikkan(lv, f"{kata_gagal} {jenis} {fmt_angka(target, uang)}{persen}"
                    + (f"; {langgar7} dari {info['n_7']} hari terakhir {kata_gagal}" if langgar7 >= 2 else ""))
        elif langgar7 >= 3:
            naikkan(1, f"{langgar7} dari {info['n_7']} hari terakhir {kata_gagal} {jenis} {fmt_angka(target, uang)}")
        tr = h.get("tren")
        if not buruk(v_akhir) and tr and tr["r2"] >= R2_MIN_PROYEKSI:
            b = tr["kemiringan_per_hari"]
            if (arah == "naik" and b > 0) or (arah == "turun" and b < 0):
                sisa_hari = (target - v_akhir) / b
                if 0 < sisa_hari <= HARI_PROYEKSI:
                    n_hari = int(sisa_hari.to_integral_value(rounding="ROUND_CEILING"))
                    h["proyeksi_hari_ke_target"] = sisa_hari
                    naikkan(1, f"kalau tren 7 hari terakhir berlanjut, kira-kira ±{n_hari} hari lagi melewati target {jenis} {fmt_angka(target, uang)} (perkiraan kasar)")
    elif target is not None:
        h["butuh_data"].append("target diabaikan karena arah metrik belum jelas (isi --arah)")

    h["alasan"].sort(key=lambda x: -x[0])
    h["level"] = lvl[0]
    return h


def evaluasi_stok(ks, kp, tgl_lap, lead):
    stok = sorted(ks["nilai"].items())
    h = {"jenis": "stok", "kolom": ks["kolom"], "label": ks["label"], "lead_time": lead, "level": 0,
         "alasan": [], "butuh_data": []}
    if not stok or stok[-1][0] != tgl_lap:
        h["tidak_diisi_hari_ini"] = True
        return h
    t_akhir, sisa = stok[-1]
    h["stok_akhir"] = sisa
    if sisa == 0:
        h["level"] = 3
        h["sisa_hari"] = D(0)
        h["perkiraan_habis"] = t_akhir.isoformat()
        h["alasan"].append((3, f"stok HABIS (0) per {fmt_tgl(t_akhir)}; pemasok butuh {lead} hari -- pesan HARI INI"))
        return h
    pakai = []
    if kp is not None:
        pakai = [v for t, v in sorted(kp["nilai"].items()) if t <= tgl_lap][-7:]
        h["kolom_pakai"] = kp["kolom"]
        h["sumber_pemakaian"] = "kolom pemakaian"
    else:
        turun = []
        for (t0, a), (t1, b) in zip(stok, stok[1:]):
            if b < a and (t1 - t0).days == 1:
                turun.append(a - b)
        pakai = turun[-7:]
        h["sumber_pemakaian"] = "perkiraan dari penurunan stok harian (hari restok diabaikan)"
    if len(pakai) < 3:
        h["butuh_data"].append(f"sisa hari stok butuh >= 3 hari data pemakaian (ada {len(pakai)})")
        return h
    rp = rata(pakai)
    h["rata_pakai"] = rp
    h["n_pakai"] = len(pakai)
    if rp <= 0:
        h["butuh_data"].append("pemakaian rata-rata 0, sisa hari belum bisa dihitung")
        return h
    hari = (sisa / rp).quantize(D("0.1"), rounding=ROUND_FLOOR)
    h["sisa_hari"] = hari
    # stok = sisa AKHIR hari laporan. Hari penuh terakhir = +floor(sisa/pakai); mulai kurang = +ceil.
    tepat = sisa / rp
    penuh = int(tepat.to_integral_value(rounding=ROUND_FLOOR))
    kurang = int(tepat.to_integral_value(rounding="ROUND_CEILING"))
    t_kurang = t_akhir + timedelta(days=max(1, kurang))
    h["cukup_sampai"] = (t_akhir + timedelta(days=penuh)).isoformat() if penuh >= 1 else None
    h["perkiraan_habis"] = t_kurang.isoformat()
    besok = t_akhir + timedelta(days=1)
    if penuh < 1:
        kapan = f"TIDAK cukup untuk besok -> habis besok ({fmt_tgl(besok)})"
    elif penuh == 1 and kurang == 1:
        kapan = f"cukup sampai besok ({fmt_tgl(besok)}) saja"
    else:
        kapan = f"cukup sampai {fmt_tgl(t_akhir + timedelta(days=penuh))}" + \
                (f", mulai kurang {fmt_tgl(t_kurang)}" if kurang != penuh else "")
    teks = (f"sisa {fmt_angka(sisa)} = ±{fmt_angka(hari, des=1)} hari pemakaian (rata-rata {fmt_angka(rp)}/hari)"
            f" -> {kapan}; pemasok butuh {lead} hari")
    if hari <= lead:
        h["level"] = 3
        teks += " -- pesan HARI INI"
        kosong = D(lead) - tepat
        if kosong > 0:
            h["perkiraan_kosong_hari"] = kosong.quantize(D("0.1"), rounding=ROUND_HALF_UP)
            teks += (f"; walau dipesan hari ini (datang ±{fmt_tgl(t_akhir + timedelta(days=lead))}),"
                     f" kemungkinan kosong ±{fmt_satu(kosong)} hari")
    elif hari <= 2 * lead:
        h["level"] = 2
        teks += " -- siapkan pesanan"
    elif hari <= 3 * lead:
        h["level"] = 1
    h["alasan"].append((h["level"], teks))
    return h


# ----------------------------------------------------------------------------- pertanyaan akar masalah
PERTANYAAN = [
    (("reject", "cacat", "rusak", "gagal", "susut", "waste", "buang", "terbuang"), [
        "Material: ada bahan baku batch/pemasok baru, atau bahan disimpan terlalu lama?",
        "Mesin: suhu/setting mesin (oven, mixer, sealer) berubah, baru diservis, atau sempat rusak?",
        "Manusia & metode: operator baru/ganti shift? resep, SOP, atau ukuran batch berubah?"]),
    (("keluhan", "komplain", "complain", "retur", "refund"), [
        "Keluhannya soal apa? Kelompokkan: rasa/kualitas, kemasan, telat, pelayanan.",
        "Datang dari satu produk/cabang/kanal (WA, marketplace) tertentu?",
        "Mulai naik sejak kapan, dan bersamaan dengan perubahan apa (bahan, kurir, harga)?"]),
    (("telat", "terlambat", "late"), [
        "Kurir/armada: ada kendaraan rusak, kurir kurang, atau ganti ekspedisi?",
        "Pesanan menumpuk di jam tertentu? Jam potong (cut-off) masih dipatuhi?",
        "Barang siap tepat waktu dari produksi/gudang, atau sudah telat sejak packing?"]),
    (("absen", "izin", "sakit", "tidak_hadir", "mangkir"), [
        "Terpusat di satu bagian/shift atau hari tertentu (mis. Senin, setelah gajian)?",
        "Ada penyakit musiman, masalah transportasi, atau lembur berlebihan minggu ini?",
        "Pekerjaan siapa yang terganggu, dan ada cadangan orangnya?"]),
    (("downtime", "mesin_mati", "breakdown", "mesin_rusak"), [
        "Mesin mana yang berhenti, berapa lama, dan apa gejalanya sebelum berhenti?",
        "Jadwal perawatan/servis terakhir kapan? Ada suku cadang yang aus?",
        "Berhentinya karena mesin, listrik/angin/air, atau menunggu bahan/operator?"]),
    (("kecelakaan", "k3", "cedera", "luka", "insiden", "kebakaran", "keracunan", "near_miss"), [
        "Korban sudah ditangani? Area/alat penyebab sudah diamankan agar tidak terulang hari ini?",
        "Apa yang terjadi persis (tempat, jam, alat, APD dipakai atau tidak) -- catat tanpa menyalahkan orang.",
        "Ada kejadian nyaris celaka serupa sebelumnya yang belum ditindaklanjuti?"]),
    (("output", "produksi", "hasil"), [
        "Mesin sempat berhenti/rusak? Berapa jam?",
        "Bahan baku sempat kurang atau telat datang?",
        "Jumlah orang di lini produksi cukup hari itu?"]),
    (("penjualan", "omzet", "omset", "transaksi", "pesanan", "order", "pengunjung", "sales", "pendapatan"), [
        "Ada perubahan harga, promo pesaing, atau produk kosong di etalase/marketplace?",
        "Hari libur, cuaca, atau acara lokal yang memengaruhi pembeli?",
        "Turunnya merata di semua produk/kanal, atau hanya satu?"]),
    (("stok", "stock", "persediaan"), [
        "Kapan terakhir pesan ke pemasok, dan berapa hari biasanya barang datang?",
        "Pemakaian naik karena produksi/reject naik, atau ada selisih (hilang/rusak)?",
        "Ada pemasok cadangan bila pemasok utama telat?"]),
]
PERTANYAAN_UMUM = [
    "Apa yang berubah dibanding minggu lalu (orang, bahan, mesin, cara kerja, pelanggan)?",
    "Mulai sejak tanggal berapa, dan terjadi di bagian/shift mana?",
    "Angka ini dicatat dengan cara yang sama seperti biasanya?"]


def pertanyaan_untuk(nama_norm):
    for kata, daftar in PERTANYAAN:
        if cocok(nama_norm, kata):
            return daftar
    return PERTANYAAN_UMUM


# ----------------------------------------------------------------------------- utama
def analisis(tabel, args):
    catatan = []
    data = susun_data(tabel, args, catatan)
    semua_tgl = data["tanggal"]
    tgl_lap = parse_tanggal(args.tanggal) if args.tanggal else semua_tgl[-1]
    # buang data setelah tanggal laporan
    for k in data["kolom"]:
        if "nilai" in k:
            k["nilai"] = {t: v for t, v in k["nilai"].items() if t <= tgl_lap}
    ada_angka = set()
    for k in data["kolom"]:
        if "nilai" in k:
            ada_angka.update(k["nilai"])
    tgl_dipakai = [t for t in semua_tgl if t <= tgl_lap and t in ada_angka]
    if not tgl_dipakai:
        raise InputError(f"tidak ada data pada/sebelum tanggal laporan {tgl_lap.isoformat()}")

    arah_manual, target_manual, lead_manual = {}, {}, {}
    for a in args.arah or []:
        kol, _, val = a.partition("=")
        if val not in ("naik", "turun", "dua"):
            raise InputError(f"--arah {a!r}: pakai naik, turun, atau dua")
        arah_manual[normalisasi(kol)] = val
    for a in args.target or []:
        kol, _, val = a.partition("=")
        target_manual[normalisasi(kol)] = parse_angka(val)
    lead_umum = 2
    for a in args.lead_time or []:
        kol, _, val = a.rpartition("=")
        if not val.strip().isdigit():
            raise InputError(f"--lead-time {a!r}: isi jumlah hari bulat, mis. 3 atau stok_tepung_kg=3")
        if kol:
            lead_manual[normalisasi(kol)] = int(val)
        else:
            lead_umum = int(val)
    targets = dict(data["targets"])
    targets.update(target_manual)

    angka = {k["kolom"]: k for k in data["kolom"] if "nilai" in k}
    teks_kolom = [k for k in data["kolom"] if "teks" in k]

    # pasangan stok
    pasangan = []
    for p in args.stok or []:
        s, _, u = p.partition(":")
        s, u = normalisasi(s), normalisasi(u) if u else None
        if s not in angka or (u and u not in angka):
            raise InputError(f"--stok {p!r}: kolom tidak ditemukan. Kolom angka: {', '.join(angka)}")
        pasangan.append((s, u))
    if not args.stok:
        kol_stok = [n for n in angka if cocok(n, KATA_STOK)]
        kol_pakai = [n for n in angka if cocok(n, KATA_PAKAI)]

        def ekor(n, kata):
            return "_".join(b for b in n.split("_") if not any(b.startswith(k) for k in kata))
        for s in kol_stok:
            u = next((p for p in kol_pakai if ekor(p, KATA_PAKAI) == ekor(s, KATA_STOK)), None)
            if u is None and len(kol_stok) == 1 and len(kol_pakai) == 1:
                u = kol_pakai[0]
            pasangan.append((s, u))
    kol_khusus = {s for s, _ in pasangan} | {u for _, u in pasangan if u}

    # rasio reject otomatis
    if not args.tanpa_rasio:
        rj = next((n for n in angka if n not in kol_khusus and cocok(n, ("reject", "cacat", "rusak", "gagal"))), None)
        out = next((n for n in angka if n not in kol_khusus and cocok(n, ("output", "produksi", "hasil"))
                    and not cocok(n, KATA_NAIK_BURUK)), None)
        if rj and out and "persen_reject" not in angka:
            nilai = {t: angka[rj]["nilai"][t] / angka[out]["nilai"][t] * 100
                     for t in angka[rj]["nilai"] if angka[out]["nilai"].get(t)}
            if nilai:
                angka["persen_reject"] = {"kolom": "persen_reject", "label": "% reject", "sumber": [rj, out],
                                          "nilai": nilai, "turunan": True}
                catatan.append(f"Ditambahkan metrik turunan '% reject' = {angka[rj]['label']} ÷ {angka[out]['label']} × 100 (supaya kenaikan reject karena produksi naik tidak disalahartikan).")

    kol_kejadian = set()
    for a in args.kejadian or []:
        for bag in a.split(","):
            if bag.strip():
                if normalisasi(bag) not in angka:
                    raise InputError(f"--kejadian {bag!r}: kolom tidak ditemukan. Kolom angka: {', '.join(angka)}")
                kol_kejadian.add(normalisasi(bag))
    metrik = []
    for n, k in angka.items():
        if n in kol_khusus:
            continue
        kejadian = n in kol_kejadian or cocok(n, KATA_KEJADIAN)
        arah = arah_manual.get(n) or ("naik" if n == "persen_reject" or kejadian else tebak_arah(n))
        uang = cocok(n, KATA_UANG)
        metrik.append(evaluasi_metrik(k, arah, targets.get(n), tgl_lap, uang, kejadian and arah == "naik"))
    for s, u in pasangan:
        metrik.append(evaluasi_stok(angka[s], angka.get(u) if u else None, tgl_lap,
                                    lead_manual.get(s, lead_umum)))

    # kualitas data
    rentang = (tgl_dipakai[0], max(tgl_lap, tgl_dipakai[-1]))
    semua_hari = [rentang[0] + timedelta(days=i) for i in range((rentang[1] - rentang[0]).days + 1)]
    ada = set(tgl_dipakai)
    hari_kosong = [t for t in semua_hari if t not in ada]
    kualitas = {
        "hari_tercatat": len(tgl_dipakai), "hari_kalender": len(semua_hari),
        "hari_kosong": [t.isoformat() for t in hari_kosong],
        "baris_dilewati": data["dilewati"], "tanggal_duplikat": [t.isoformat() for t in data["duplikat"]],
        "angka_ambigu": data["ambigu"], "sel_rusak": data["sel_rusak"],
        "tanggal_diabaikan": [t.isoformat() for t in data["abaikan"]],
        "tidak_diisi_hari_ini": [m["label"] for m in metrik if m.get("tidak_diisi_hari_ini")],
    }
    if data["duplikat"]:
        catatan.append(f"{len(data['duplikat'])} tanggal muncul lebih dari sekali; dipakai "
                       + ("jumlah semua baris" if args.duplikat == "jumlah" else "baris terakhir") + ".")
    if data["ambigu"]:
        catatan.append(f"{len(data['ambigu'])} angka seperti {data['ambigu'][0]!r} dibaca sebagai ribuan (koma = pemisah ribuan). Kalau maksudnya desimal, tulis dengan 1-2 angka di belakang koma.")

    catatan_hari_ini = []
    for k in teks_kolom:
        isi = k["teks"].get(tgl_lap, "")
        if isi and not re.fullmatch(r"[\d\s.,:/-]*", isi):
            catatan_hari_ini.append(isi)

    peringatan = sorted([m for m in metrik if m["level"] > 0],
                        key=lambda m: (-m["level"], -abs(m.get("z") or 0)))
    normal = [m for m in metrik if m["level"] == 0 and not m.get("tidak_diisi_hari_ini")
              and (m.get("terbaru") or m.get("sisa_hari") is not None)]
    hasil = {
        "versi": VERSI, "tanggal_laporan": tgl_lap.isoformat(),
        "periode": {"awal": rentang[0].isoformat(), "akhir": rentang[1].isoformat()},
        "data_sedikit": len(tgl_dipakai) < MIN_SIGMA + 1,
        "ringkas": {NAMA_LEVEL[l]: sum(1 for m in metrik if m["level"] == l) for l in (3, 2, 1)},
        "metrik": metrik, "kualitas_data": kualitas, "catatan": catatan,
        "catatan_hari_ini": catatan_hari_ini, "sertakan_catatan": bool(args.sertakan_catatan),
    }
    hasil["ringkas"]["normal"] = len(normal)
    hasil["belum_diisi"] = not any(not m.get("tidak_diisi_hari_ini") for m in metrik)
    hasil["laporan_teks"] = susun_laporan(hasil, peringatan, normal, args.nama_usaha)
    return hasil


def susun_laporan(h, peringatan, normal, nama_usaha):
    tgl = date.fromisoformat(h["tanggal_laporan"])
    aw = date.fromisoformat(h["periode"]["awal"])
    kd = h["kualitas_data"]
    L = []
    if h.get("belum_diisi"):
        terakhir = max((date.fromisoformat(m["terbaru"]["tanggal"]) for m in h["metrik"] if m.get("terbaru")),
                       default=None)
        L.append("⬜ LOG HARIAN BELUM DIISI")
        L.append((f"{nama_usaha} — " if nama_usaha else "") + fmt_tgl(tgl, True))
        L.append("Belum ada angka untuk tanggal ini, jadi belum bisa dicek. Tidak ada angka yang ditebak."
                 + (f" Data terakhir: {fmt_tgl(terakhir, True)}." if terakhir else ""))
        return "\n".join(L)
    judul = "🚨 PERINGATAN DINI OPERASIONAL" if peringatan else "✅ PERINGATAN DINI OPERASIONAL"
    L.append(judul)
    L.append((f"{nama_usaha} — " if nama_usaha else "") + fmt_tgl(tgl, True))
    L.append(f"Data {aw.day} {BULAN_ID[aw.month - 1]}–{tgl.day} {BULAN_ID[tgl.month - 1]} ({kd['hari_tercatat']} hari tercatat)")
    r = h["ringkas"]
    L.append(f"Ringkas: {r['merah']} 🔴 · {r['oranye']} 🟠 · {r['kuning']} 🟡 · {r['normal']} normal")
    if h["data_sedikit"]:
        n = kd["hari_tercatat"]
        kurang = [f"batas kendali (σ) butuh ≥{MIN_SIGMA + 1} hari"]
        if n < MIN_TREN:
            kurang.append(f"tren ≥{MIN_TREN} hari")
        if n < 7 * MIN_HARI_SAMA + 1:
            kurang.append(f"banding hari yang sama ≥{7 * MIN_HARI_SAMA + 1} hari")
        L.append(f"⚠️ Data baru {n} hari: " + ", ".join(kurang) + ". Peringatan di bawah masih terbatas.")
    L.append("")
    tampil = peringatan[:6]
    for m in tampil:
        if m.get("jenis") == "stok":
            L.append(f"{WARNA[m['level']]} {m['label']}: {m['alasan'][0][1]}")
            continue
        nilai = fmt_angka(m["terbaru"]["nilai"], m["uang"])
        extra = ""
        if m.get("sebelumnya"):
            ts = date.fromisoformat(m["sebelumnya"]["tanggal"])
            kapan = "kemarin" if (tgl - ts).days == 1 else f"sebelumnya {fmt_tgl(ts)}"
            extra = f" ({kapan} {fmt_angka(m['sebelumnya']['nilai'], m['uang'])})"
        L.append(f"{WARNA[m['level']]} {m['label']}: {nilai} hari ini{extra}")
        alasan = [t for _, t in m["alasan"]]
        L.append("   " + "; ".join(alasan[:3]) + ".")
    if len(peringatan) > len(tampil):
        L.append(f"(+{len(peringatan) - len(tampil)} peringatan lain, lihat detail)")
    if not peringatan:
        L.append("Tidak ada tanda bahaya dari angka hari ini.")
    parah = [m for m in peringatan if m["level"] >= 2 and m.get("jenis") != "stok"]
    turunan = {s for m in parah if m["kolom"] == "persen_reject" for s in m.get("sumber", [])}
    parah = [m for m in parah if not (m["kolom"] == "persen_reject" and turunan & {x["kolom"] for x in parah})]
    if len(parah) >= 2:
        L.append(f"🔗 {parah[0]['label']} dan {parah[1]['label']} memburuk bersamaan — cek apakah penyebabnya sama (belum tentu berkaitan).")
    if normal:
        L.append("✅ Normal: " + ", ".join(m["label"] for m in normal))
    if kd["tidak_diisi_hari_ini"]:
        L.append("⬜ Belum diisi hari ini: " + ", ".join(kd["tidak_diisi_hari_ini"]))
    belum_hitung = [m["label"] for m in h["metrik"] if m.get("jenis") == "stok" and m["level"] == 0
                    and m.get("sisa_hari") is None and not m.get("tidak_diisi_hari_ini")]
    if belum_hitung:
        L.append("⬜ Sisa stok belum bisa dihitung (pemakaian kurang/0): " + ", ".join(belum_hitung))
    if h["catatan_hari_ini"] and h.get("sertakan_catatan"):
        L.append("📝 Catatan hari ini: " + " | ".join(f'"{c}"' for c in h["catatan_hari_ini"]))
    if peringatan:
        L.append("")
        L.append("❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):")
        dipakai = []
        for m in peringatan:
            daftar = pertanyaan_untuk(m["kolom"])
            if daftar in dipakai:
                continue
            dipakai.append(daftar)
            L.append(f"{m['label']}:")
            for q in daftar:
                L.append(f" • {q}")
            if len(dipakai) == 2:
                break
        m0 = peringatan[0]
        kata = "memburuk"
        if m0.get("jenis") != "stok":
            kata = "naik" if m0["arah"] == "naik" else ("turun" if m0["arah"] == "turun" else "berubah")
        L.append(f"5 kenapa: Kenapa {m0['label']} {kata}? → karena … → kenapa itu terjadi? → … (ulang sampai ketemu hal yang bisa diperbaiki).")
        L.append("Kalau sudah ada kerugian/komplain pelanggan: susun laporan insiden (skill laporan-insiden-usaha).")
    L.append("")
    info = []
    if kd["hari_kosong"]:
        contoh = ", ".join(fmt_tgl(date.fromisoformat(t)) for t in kd["hari_kosong"][:3])
        info.append(f"{len(kd['hari_kosong'])} hari kosong ({contoh}{'…' if len(kd['hari_kosong']) > 3 else ''}) tidak diisi tebakan")
    if kd["baris_dilewati"]:
        info.append(f"{len(kd['baris_dilewati'])} baris dilewati (tanggal tidak terbaca)")
    if kd["sel_rusak"]:
        info.append(f"{len(kd['sel_rusak'])} sel angka tidak terbaca/negatif diabaikan")
    if kd["tanggal_duplikat"]:
        info.append(f"{len(kd['tanggal_duplikat'])} tanggal dobel (baris terakhir dipakai, kecuali --duplikat jumlah)")
    if kd["angka_ambigu"]:
        info.append(f"{len(kd['angka_ambigu'])} angka seperti {kd['angka_ambigu'][0]} dibaca ribuan")
    peng = [m for m in h["metrik"] if m.get("dasar", {}).get("pencilan_diabaikan")]
    if peng:
        info.append(f"{sum(len(m['dasar']['pencilan_diabaikan']) for m in peng)} angka ekstrem lama tidak dipakai di rata-rata")
    if info:
        L.append("ℹ️ Data: " + "; ".join(info) + ".")
    L.append("Catatan: ini peringatan statistik (tanda untuk dicek), bukan kepastian masalah atau ramalan pasti.")
    return "\n".join(L)


def ke_json(o):
    if isinstance(o, D):
        return bulat(o, 4)
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    if isinstance(o, tuple):
        return list(o)
    raise TypeError(type(o))


def rapikan(o):
    if isinstance(o, dict):
        return {k: rapikan(v) for k, v in o.items() if k != "nilai" or not isinstance(v, dict)}
    if isinstance(o, list):
        return [rapikan(v) for v in o]
    if isinstance(o, tuple):
        return {"level": o[0], "teks": o[1]} if len(o) == 2 and isinstance(o[0], int) else list(o)
    return o


def buat_parser():
    p = argparse.ArgumentParser(description="Peringatan dini operasional harian (Komunitech)")
    p.add_argument("file", help="CSV/TSV/.xlsx log harian, atau '-' untuk tabel dari stdin")
    p.add_argument("--format", choices=("teks", "json"), default="teks")
    p.add_argument("--target", action="append", help="kolom=nilai (bisa diulang)")
    p.add_argument("--arah", action="append", help="kolom=naik|turun|dua (bisa diulang)")
    p.add_argument("--stok", action="append", help="KOLOM_STOK[:KOLOM_PAKAI] (bisa diulang)")
    p.add_argument("--lead-time", action="append", help="N hari (semua stok) atau kolom_stok=N")
    p.add_argument("--abaikan-tanggal", action="append", help="YYYY-MM-DD[,YYYY-MM-DD]")
    p.add_argument("--tanggal", help="tanggal laporan YYYY-MM-DD (default: tanggal terakhir di data)")
    p.add_argument("--duplikat", choices=("terakhir", "jumlah"), default="terakhir")
    p.add_argument("--urutan-tanggal", choices=("dmy", "mdy"), default="dmy")
    p.add_argument("--nama-usaha", default="")
    p.add_argument("--tanpa-rasio", action="store_true", help="jangan tambah metrik %% reject otomatis")
    p.add_argument("--kejadian", action="append",
                   help="kolom kejadian kritis (mis. kecelakaan kerja): setiap angka > 0 = merah")
    p.add_argument("--sertakan-catatan", action="store_true",
                   help="kutip kolom catatan/keterangan di laporan teks (PERHATIAN: bisa berisi nama orang)")
    return p


def main(argv=None):
    a = buat_parser().parse_args(argv)
    try:
        hasil = analisis(baca_tabel(a.file), a)
    except (InputError, ValueError) as e:
        pesan = {"galat": str(e)}
        if a.format == "json":
            print(json.dumps(pesan, ensure_ascii=False, indent=2))
        else:
            print(f"GALAT: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps(rapikan(hasil), ensure_ascii=False, indent=2, default=ke_json))
    else:
        print(hasil["laporan_teks"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
