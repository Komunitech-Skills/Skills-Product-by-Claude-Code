#!/usr/bin/env python3
"""Analisis ekspor iklan mingguan (Meta/TikTok Ads/Shopee Ads/TikTok Shop Ads/Google Ads)
dan gabungan lintas-platform. Output JSON ke stdout (mode --json) atau teks siap kirim.

Hanya memakai library standar Python (3.8+). Lintas OS (Windows: pakai `python`/`py`).

Sumber nama kolom resmi per platform: lihat references/sumber-kolom.md di folder skill ini.
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

# --------------------------------------------------------------------------------------
# Parsing angka & tanggal (logika sama dengan skill rekap-penjualan-csv, dipakai ulang
# di sini karena tiap skill wajib berdiri sendiri / tanpa dependensi lintas-folder).
# --------------------------------------------------------------------------------------

BULAN = {
    "jan": 1, "januari": 1, "january": 1,
    "feb": 2, "februari": 2, "february": 2, "peb": 2, "pebruari": 2,
    "mar": 3, "maret": 3, "march": 3,
    "apr": 4, "april": 4,
    "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6,
    "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "nopember": 11,
    "des": 12, "desember": 12, "dec": 12, "december": 12,
}
POLA_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:[ T].*)?$")
POLA_ANGKA_3 = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})(?:[ T].*)?$")
POLA_NAMA_BULAN = re.compile(r"^(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{2}|\d{4})(?:[ T].*)?$")


def _tahun(t):
    t = int(t)
    return t + 2000 if t < 100 else t


def _buat_tanggal(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def deteksi_urutan(teks_tanggal):
    dmy_pasti = mdy_pasti = False
    for t in teks_tanggal:
        m = POLA_ANGKA_3.match((t or "").strip())
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12:
            dmy_pasti = True
        if b > 12:
            mdy_pasti = True
    if mdy_pasti and not dmy_pasti:
        return "mdy"
    return "dmy"


def parse_tanggal(teks, urutan="dmy"):
    teks = (teks or "").strip()
    if not teks:
        return None
    m = POLA_ISO.match(teks)
    if m:
        return _buat_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = POLA_ANGKA_3.match(teks)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), _tahun(m.group(3))
        d, bl = (a, b) if urutan == "dmy" else (b, a)
        return _buat_tanggal(y, bl, d)
    m = POLA_NAMA_BULAN.match(teks)
    if m:
        bl = BULAN.get(m.group(2).lower())
        if bl:
            return _buat_tanggal(_tahun(m.group(3)), bl, int(m.group(1)))
    return None


def _grup_ribuan_valid(bagian_bulat, pemisah):
    grup = bagian_bulat.split(pemisah)
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def parse_angka(teks):
    """Angka format Indonesia/Inggris -> float, atau None bila tidak valid/meragukan.

    Sama persis dengan `rekap-penjualan-csv/scripts/rekap.py::parse_angka` (lihat file itu
    untuk daftar contoh yang didukung/ditolak).
    """
    if teks is None:
        return None
    s = str(teks).strip().lower()
    if not s:
        return None
    if re.fullmatch(r"\(.*\)", s):
        s = "-" + s[1:-1].strip()
    if re.search(r"\d\s*e\s*[+-]?\s*\d", s):
        return None
    s = re.sub(r"\b(rp|idr|usd|sgd|myr|php|thb|vnd|eur|gbp|aud|jpy|cny)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)
    s = re.sub(r"[^\d,.\-]", "", s).strip(".,")
    if not s or s == "-":
        return None
    negatif = s.startswith("-")
    s = s.lstrip("-")
    if "-" in s:
        return None
    digit = sum(c.isdigit() for c in s)
    if "," in s and "." in s:
        desimal = "," if s.rfind(",") > s.rfind(".") else "."
        ribuan = "." if desimal == "," else ","
        bulat, _, pecahan = s.rpartition(desimal)
        if ribuan in pecahan or not _grup_ribuan_valid(bulat, ribuan):
            return None
        s = bulat.replace(ribuan, "") + "." + pecahan
    elif "," in s or "." in s:
        pemisah = "," if "," in s else "."
        bagian = s.split(pemisah)
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = bagian[0] + "." + bagian[1]
        elif _grup_ribuan_valid(s, pemisah):
            s = s.replace(pemisah, "")
        else:
            return None
    try:
        nilai = float(s)
    except ValueError:
        return None
    if digit >= 4 and 0 < nilai < 1:
        return None
    return -nilai if negatif else nilai


def baca_csv(path):
    mentah = open(path, "rb").read()
    if not mentah.strip():
        raise ValueError("File kosong")
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    contoh = teks[:4096]
    try:
        dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
    except csv.Error:
        dialek = csv.excel
    try:
        baris = list(csv.DictReader(io.StringIO(teks), dialect=dialek))
    except csv.Error as e:
        raise ValueError(f"File tidak bisa dibaca sebagai CSV ({e}). Pastikan file benar-benar hasil "
                          "ekspor CSV, bukan file rusak/format lain (mis. .xlsx yang diganti nama saja).")
    return baris, enc


# --------------------------------------------------------------------------------------
# Pembulatan (aturan eksplisit, sama untuk seluruh library — lihat SKILL.md § Rumus)
# --------------------------------------------------------------------------------------

def bulat_rupiah(x):
    """Ke rupiah bulat terdekat, 0,5 menjauhi nol."""
    if x is None:
        return None
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def bulat_satu_desimal(x):
    """1 desimal, 0,05 menjauhi nol (dipakai untuk persen & ROAS)."""
    if x is None:
        return None
    d = Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return float(d)


def fmt_rp(x):
    if x is None:
        return "-"
    n = bulat_rupiah(x)
    return "Rp " + f"{n:,}".replace(",", ".")


def fmt_rp_desimal(x, desimal=2):
    """Format Rupiah dengan desimal (mis. untuk kurs): ribuan '.', desimal ','."""
    teks = f"{x:,.{desimal}f}"
    bulat, _, pecahan = teks.partition(".")
    return "Rp " + bulat.replace(",", ".") + "," + pecahan


def fmt_persen(x):
    if x is None:
        return "-"
    v = bulat_satu_desimal(x)
    return f"{v:.1f}".replace(".", ",") + "%"


def fmt_angka(x):
    if x is None:
        return "-"
    if float(x).is_integer():
        return f"{int(x):,}".replace(",", ".")
    return f"{x:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")


def bagi(a, b):
    return a / b if b else None


# --------------------------------------------------------------------------------------
# Deteksi platform & pemetaan kolom
# --------------------------------------------------------------------------------------

# (peran -> (daftar substring yang harus ADA, daftar substring yang membuat kolom DITOLAK))
# Substring dicocokkan pada header yang sudah di-lower(). Urutan peran = prioritas penetapan
# saat satu header bisa "terlihat" cocok untuk lebih dari satu peran.
PERAN_UTAMA = [
    ("nama", (["campaign name", "nama kampanye", "nama iklan", "ad set name", "ad name",
               "campaign", "iklan"], [])),
    ("biaya", (["amount spent", "biaya bersih", "biaya", "net cost", "spend", "cost"],
               ["per", "roas", "value", "nilai", "%"])),
    ("nilai_hasil", (["purchase conversion value", "conversion value", "conv. value", "gmv",
                      "omzet penjualan", "pendapatan kotor", "total onsite value",
                      "nilai konversi"], ["per", "rate", "persen", "rasio", "%", "roas"])),
    ("hasil", (["results", "conversions", "conversion", "konversi", "pesanan", "purchases",
                "leads", "messaging conversations started", "messages"],
               ["cost", "biaya", "per", "value", "nilai", "rate", "ratio", "rasio", "roas", "%"])),
    ("klik", (["link clicks", "clicks (destination)", "clicks", "klik"],
              ["cost", "biaya", "cpc", "rate", "ctr", "tingkat", "per", "%", "through"])),
    ("tayangan", (["impressions", "impresi", "tayangan", "dilihat", "impr."],
                  ["cost", "biaya", "cpm", "per", "%", "frequency", "frekuensi"])),
    ("tanggal", (["date", "day", "tanggal", "tgl"], ["update", "created", "dibuat", "mulai", "selesai"])),
]
# Peran cadangan untuk "tayangan" bila kolom Impressions/Dilihat memang tidak ada di file
PERAN_TAYANGAN_CADANGAN = (["reach", "jangkauan"], ["cost", "biaya", "per", "%"])

# Penanda platform: (nama, [(substring, bobot), ...]). Substring khas satu platform (jarang
# dipakai platform lain) diberi bobot 2 supaya cukup sendirian; substring umum diberi bobot 1
# dan butuh ditemani penanda lain. Cocok bila total bobot >= AMBANG_FINGERPRINT.
AMBANG_FINGERPRINT = 2
FINGERPRINT_PLATFORM = [
    ("Meta Ads (Facebook/Instagram)", [("ad set name", 2), ("reach", 1), ("link clicks", 1),
                                        ("amount spent", 1)]),
    ("TikTok Shop Ads", [("gmv", 2), ("pendapatan kotor", 2), ("pesanan", 1)]),
    ("Shopee Ads", [("dilihat", 1), ("konversi (langsung)", 1), ("acos", 2), ("rasio konversi", 1)]),
    ("TikTok Ads Manager", [("clicks (destination)", 2), ("cpc (destination)", 2),
                            ("cost per conversion", 1)]),
    ("Google Ads", [("impr.", 2), ("avg. cpc", 1), ("cost / conv.", 1), ("conv. value", 1)]),
]

MATA_UANG_DIKENAL = {"IDR", "USD", "SGD", "MYR", "PHP", "THB", "VND", "EUR", "GBP", "AUD", "JPY", "CNY"}
POLA_MATA_UANG = re.compile(r"\(([A-Za-z]{3})\)")

KATA_BARIS_TOTAL = {"total", "grand total", "jumlah", "semua kampanye", "all campaigns",
                    "summary", "subtotal", "total keseluruhan", "keseluruhan", "grand-total"}


def _norm(h):
    return re.sub(r"\s+", " ", (h or "").strip().lower())


def deteksi_kolom(header, override):
    """Kembalikan (dict peran->nama_kolom_asli atau None, daftar_peringatan)."""
    norm = {h: _norm(h) for h in header}
    dipakai = set()
    hasil = {}
    peringatan = []

    # 1) override eksplisit dari pengguna/agent selalu menang
    for peran, kolom in override.items():
        if kolom:
            if kolom not in header:
                raise ValueError(f"Kolom '{kolom}' (untuk --kolom-{peran.replace('_', '-')}) "
                                  f"tidak ada di file. Kolom tersedia: {header}")
            hasil[peran] = kolom
            dipakai.add(kolom)

    # 2) deteksi otomatis untuk peran yang belum diisi manual
    for peran, (wajib_ada, dilarang) in PERAN_UTAMA:
        if peran in hasil:
            continue
        for h in header:
            if h in dipakai:
                continue
            n = norm[h]
            if any(k in n for k in wajib_ada) and not any(k in n for k in dilarang):
                hasil[peran] = h
                dipakai.add(h)
                break
        else:
            hasil[peran] = None

    # 3) cadangan tayangan -> reach
    if not hasil.get("tayangan"):
        wajib_ada, dilarang = PERAN_TAYANGAN_CADANGAN
        for h in header:
            if h in dipakai:
                continue
            n = norm[h]
            if any(k in n for k in wajib_ada) and not any(k in n for k in dilarang):
                hasil["tayangan"] = h
                dipakai.add(h)
                peringatan.append(
                    f"Kolom tayangan/impresi tidak ditemukan; memakai '{h}' (jangkauan/reach) "
                    "sebagai gantinya. CPM & CTR jadi perkiraan berbasis jangkauan, bukan tayangan asli.")
                break

    return hasil, peringatan


def deteksi_platform(header):
    norm = " | ".join(_norm(h) for h in header)
    cocok = []
    for nama, penanda in FINGERPRINT_PLATFORM:
        skor = sum(bobot for substr, bobot in penanda if substr in norm)
        if skor >= AMBANG_FINGERPRINT:
            cocok.append((skor, nama))
    if not cocok:
        return None
    cocok.sort(reverse=True)
    return cocok[0][1]


def deteksi_mata_uang(header):
    for h in header:
        m = POLA_MATA_UANG.search(h)
        if m and m.group(1).upper() in MATA_UANG_DIKENAL:
            return m.group(1).upper(), h
    return None, None


# --------------------------------------------------------------------------------------
# Analisis satu file (satu platform, satu minggu)
# --------------------------------------------------------------------------------------

def analisis_file(path, override, args):
    header0, _ = baca_csv(path)
    if not header0:
        raise ValueError("File kosong atau hanya berisi judul kolom")
    header = list(header0[0].keys())

    kolom, peringatan_kolom = deteksi_kolom(header, override)
    wajib = ["biaya", "tayangan", "klik", "hasil"]
    hilang = [k for k in wajib if not kolom.get(k)]
    if hilang:
        raise ValueError(
            "Kolom wajib tidak terdeteksi otomatis: " + ", ".join(hilang) + ". "
            "Beri tahu nama kolomnya lewat opsi --kolom-" +
            "/--kolom-".join(x.replace("_", "-") for x in hilang) +
            f". Kolom yang ada di file: {header}")

    platform_terdeteksi = args.platform or deteksi_platform(header) or "Tidak diketahui"

    mata_uang_terdeteksi, kolom_mata_uang = deteksi_mata_uang(
        [kolom["biaya"]] + ([kolom["nilai_hasil"]] if kolom.get("nilai_hasil") else []))
    catatan_mata_uang = []
    kurs = 1.0
    mata_uang_final = "IDR"
    if mata_uang_terdeteksi and mata_uang_terdeteksi != "IDR":
        if args.mata_uang == "IDR":
            catatan_mata_uang.append(
                f"Kolom '{kolom_mata_uang}' berlabel {mata_uang_terdeteksi}, tetapi dianggap IDR "
                "sesuai perintah eksplisit --mata-uang IDR.")
        elif args.kurs:
            kurs = args.kurs
            sumber_kurs = f", sumber: {args.kurs_sumber}" if args.kurs_sumber else ""
            tanggal_kurs = f" per {args.kurs_tanggal}" if args.kurs_tanggal else ""
            catatan_mata_uang.append(
                f"Nilai dikonversi dari {mata_uang_terdeteksi} ke IDR dengan kurs 1 {mata_uang_terdeteksi} "
                f"= {fmt_rp_desimal(kurs)}{tanggal_kurs}{sumber_kurs} (kurs diberikan pengguna, bukan realtime).")
        else:
            raise ValueError(
                f"File ini berlabel mata uang {mata_uang_terdeteksi}, bukan IDR. Skill ini menghitung "
                "dalam Rupiah dan TIDAK mengonversi diam-diam. Jalankan ulang dengan --kurs <angka> "
                f"(nilai tukar 1 {mata_uang_terdeteksi} ke Rupiah, boleh tambah --kurs-sumber/--kurs-tanggal) "
                "atau --mata-uang IDR bila label file keliru dan angkanya memang sudah Rupiah.")
    elif mata_uang_terdeteksi == "IDR":
        mata_uang_final = "IDR"
    else:
        catatan_mata_uang.append("Tidak ada label mata uang di file; diasumsikan IDR (Rupiah).")

    urutan = "dmy"
    if kolom.get("tanggal"):
        urutan = deteksi_urutan([r.get(kolom["tanggal"]) for r in header0])

    per_kampanye = defaultdict(lambda: {"biaya": 0.0, "tayangan": 0.0, "klik": 0.0,
                                        "hasil": 0.0, "nilai_hasil": 0.0})
    tanggal_terlihat = []
    baris_total_dilewati = 0
    dilewati = defaultdict(int)
    n_valid = 0

    for i, r in enumerate(header0, start=1):
        nama_baris = " ".join((r.get(kolom["nama"]) or f"Kampanye #{i}").split()) if kolom.get("nama") else f"Kampanye #{i}"
        if _norm(nama_baris) in KATA_BARIS_TOTAL:
            baris_total_dilewati += 1
            continue

        biaya = parse_angka(r.get(kolom["biaya"]))
        tayangan = parse_angka(r.get(kolom["tayangan"]))
        klik = parse_angka(r.get(kolom["klik"]))
        hasil_v = parse_angka(r.get(kolom["hasil"]))
        nilai_hasil = parse_angka(r.get(kolom["nilai_hasil"])) if kolom.get("nilai_hasil") else 0.0

        nilai_wajib = {"biaya": biaya, "tayangan": tayangan, "klik": klik, "hasil": hasil_v}
        kosong_semua = all(not (r.get(kolom[k]) or "").strip() for k in nilai_wajib)
        if kosong_semua:
            continue  # baris kosong (mis. baris pemisah di ekspor)
        tidak_valid = [k for k, v in nilai_wajib.items() if v is None]
        if tidak_valid:
            dilewati["angka tidak terbaca: " + ", ".join(tidak_valid)] += 1
            continue

        biaya *= kurs
        nilai_hasil = (nilai_hasil or 0.0) * kurs

        if kolom.get("tanggal"):
            tgl = parse_tanggal(r.get(kolom["tanggal"]), urutan)
            if tgl:
                tanggal_terlihat.append(tgl)

        k = per_kampanye[nama_baris]
        k["biaya"] += biaya
        k["tayangan"] += tayangan
        k["klik"] += klik
        k["hasil"] += hasil_v
        k["nilai_hasil"] += nilai_hasil or 0.0
        n_valid += 1

    if n_valid == 0:
        raise ValueError("Tidak ada baris data yang valid di file ini (semua kosong/rusak/baris total). "
                          f"Baris dilewati karena baris total: {baris_total_dilewati}. "
                          f"Alasan lain: {dict(dilewati)}")

    total = {"biaya": 0.0, "tayangan": 0.0, "klik": 0.0, "hasil": 0.0, "nilai_hasil": 0.0}
    daftar_kampanye = []
    for nama, v in per_kampanye.items():
        for kk in total:
            total[kk] += v[kk]
        cpc = bagi(v["biaya"], v["klik"])
        cpm = bagi(v["biaya"], v["tayangan"])
        cpm = cpm * 1000 if cpm is not None else None
        ctr = bagi(v["klik"], v["tayangan"])
        ctr = ctr * 100 if ctr is not None else None
        biaya_per_hasil = bagi(v["biaya"], v["hasil"])
        roas = bagi(v["nilai_hasil"], v["biaya"]) if kolom.get("nilai_hasil") else None
        daftar_kampanye.append({
            "nama": nama, "biaya": v["biaya"], "tayangan": v["tayangan"], "klik": v["klik"],
            "hasil": v["hasil"], "nilai_hasil": v["nilai_hasil"] if kolom.get("nilai_hasil") else None,
            "cpc": cpc, "cpm": cpm, "ctr_persen": ctr, "biaya_per_hasil": biaya_per_hasil, "roas": roas,
        })

    t_cpc = bagi(total["biaya"], total["klik"])
    t_cpm = bagi(total["biaya"], total["tayangan"])
    t_cpm = t_cpm * 1000 if t_cpm is not None else None
    t_ctr = bagi(total["klik"], total["tayangan"])
    t_ctr = t_ctr * 100 if t_ctr is not None else None
    t_bph = bagi(total["biaya"], total["hasil"])
    t_roas = bagi(total["nilai_hasil"], total["biaya"]) if kolom.get("nilai_hasil") else None

    periode = {"awal": None, "akhir": None, "label": args.periode or "(sesuai rentang tanggal file yang diunggah)"}
    if tanggal_terlihat:
        periode["awal"] = min(tanggal_terlihat).isoformat()
        periode["akhir"] = max(tanggal_terlihat).isoformat()
        if not args.periode:
            periode["label"] = f"{periode['awal']} s.d. {periode['akhir']}"

    # --- 3 terbaik & terburuk (berdasar biaya per hasil) ---
    ada_hasil = [k for k in daftar_kampanye if k["hasil"] > 0]
    tanpa_hasil = [k for k in daftar_kampanye if k["hasil"] == 0]
    terbaik = sorted(ada_hasil, key=lambda k: k["biaya_per_hasil"])[: args.top]
    terburuk = (sorted(tanpa_hasil, key=lambda k: -k["biaya"]) +
                sorted(ada_hasil, key=lambda k: -k["biaya_per_hasil"]))[: args.top]

    nama_hasil = args.nama_hasil or (kolom["hasil"] if kolom.get("hasil") else "hasil")

    # --- saran (berbasis angka, deterministik) ---
    saran = []
    avg_bph = bagi(sum(k["biaya"] for k in ada_hasil), sum(k["hasil"] for k in ada_hasil)) if ada_hasil else None
    for k in sorted(tanpa_hasil, key=lambda x: -x["biaya"]):
        if k["biaya"] >= 50000:
            saran.append(f"Tinjau/hentikan iklan '{k['nama']}': sudah menghabiskan {fmt_rp(k['biaya'])} "
                         f"tanpa {nama_hasil} sama sekali.")
    if avg_bph:
        for k in sorted(ada_hasil, key=lambda x: -x['biaya_per_hasil']):
            if k["biaya_per_hasil"] > 2 * avg_bph:
                kali = k["biaya_per_hasil"] / avg_bph
                saran.append(f"Tinjau/matikan iklan '{k['nama']}': biaya per {nama_hasil} "
                             f"{fmt_rp(k['biaya_per_hasil'])}, {fmt_satu_desimal_x(kali)} rata-rata "
                             f"({fmt_rp(avg_bph)}).")
        for k in sorted(ada_hasil, key=lambda x: x['biaya_per_hasil'])[:1]:
            if k["biaya_per_hasil"] <= 0.5 * avg_bph and len(ada_hasil) > 1:
                saran.append(f"Pertimbangkan naikkan anggaran iklan '{k['nama']}': biaya per {nama_hasil} "
                             f"{fmt_rp(k['biaya_per_hasil'])}, jauh di bawah rata-rata ({fmt_rp(avg_bph)}).")
    if t_roas is not None and t_roas < 1:
        saran.append(f"ROAS keseluruhan {fmt_satu_desimal_x(t_roas)} (di bawah 1x) — biaya iklan minggu ini "
                     f"lebih besar dari nilai {nama_hasil}/penjualan yang tercatat dari iklan.")
    if not saran:
        saran.append("Belum ada kampanye yang menonjol biaya-per-hasilnya minggu ini — performa relatif merata.")
    saran = saran[:5]

    return {
        "platform_terdeteksi": platform_terdeteksi,
        "mata_uang": mata_uang_final,
        "catatan_mata_uang": catatan_mata_uang,
        "periode": periode,
        "jumlah_kampanye": len(daftar_kampanye),
        "jumlah_baris_data_valid": n_valid,
        "baris_dilewati_baris_total": baris_total_dilewati,
        "baris_dilewati_lainnya": dict(dilewati),
        "kolom_dipakai": kolom,
        "nama_hasil": nama_hasil,
        "total": {**total, "cpc": t_cpc, "cpm": t_cpm, "ctr_persen": t_ctr,
                  "biaya_per_hasil": t_bph, "roas": t_roas},
        "per_kampanye": sorted(daftar_kampanye, key=lambda k: -k["biaya"]),
        "tiga_terbaik": terbaik,
        "tiga_terburuk": terburuk,
        "saran": saran,
        "peringatan": peringatan_kolom,
    }


def fmt_satu_desimal_x(v):
    return f"{bulat_satu_desimal(v):.1f}".replace(".", ",") + "x"


# --------------------------------------------------------------------------------------
# Perbandingan minggu ini vs minggu lalu
# --------------------------------------------------------------------------------------

def bandingkan_persen(sekarang, lalu):
    if lalu == 0:
        if sekarang == 0:
            return None, "sama-sama Rp 0"
        return None, f"naik dari Rp 0 (persen tidak dihitung)"
    p = (sekarang - lalu) / lalu * 100
    p = bulat_satu_desimal(p)
    if p == 0:
        return p, "tetap (0,0%)"
    arah = "naik" if p > 0 else "turun"
    return p, f"{arah} {fmt_persen(abs(p))}"


def bandingkan(hasil_sekarang, hasil_lalu):
    keluar = {}
    for metrik, label in [("biaya", "Biaya iklan"), ("hasil", "Hasil"),
                           ("biaya_per_hasil", "Biaya per hasil"), ("klik", "Klik"),
                           ("tayangan", "Tayangan")]:
        s = hasil_sekarang["total"].get(metrik)
        l = hasil_lalu["total"].get(metrik)
        if s is None or l is None:
            keluar[metrik] = {"sekarang": s, "lalu": l, "persen": None, "keterangan": "tidak dapat dibandingkan (- pada salah satu minggu)"}
            continue
        p, ket = bandingkan_persen(s, l)
        keluar[metrik] = {"sekarang": s, "lalu": l, "persen": p, "keterangan": ket, "label": label}
    return keluar


# --------------------------------------------------------------------------------------
# Susun teks laporan siap kirim
# --------------------------------------------------------------------------------------

def susun_teks(h, pembanding=None, omzet=None):
    L = []
    L.append(f"LAPORAN IKLAN MINGGUAN — {h['platform_terdeteksi']}")
    L.append(f"Periode: {h['periode']['label']}")
    L.append("")
    t = h["total"]
    L.append(f"Total belanja iklan: {fmt_rp(t['biaya'])}")
    L.append(f"Tayangan: {fmt_angka(t['tayangan'])} | Klik: {fmt_angka(t['klik'])} "
              f"| {h['nama_hasil'].capitalize()}: {fmt_angka(t['hasil'])}")
    L.append(f"CPC: {fmt_rp(t['cpc'])} | CPM: {fmt_rp(t['cpm'])} | CTR: {fmt_persen(t['ctr_persen'])}")
    L.append(f"Biaya per {h['nama_hasil']}: {fmt_rp(t['biaya_per_hasil'])}")
    if t.get("roas") is not None:
        L.append(f"ROAS: {fmt_satu_desimal_x(t['roas'])}")
    if omzet:
        L.append(f"Biaya iklan vs omzet: {fmt_persen(omzet['biaya_sebagai_persen_omzet'])} dari omzet "
                  f"{fmt_rp(omzet['omzet'])}")

    if pembanding:
        L.append("")
        L.append("VS MINGGU LALU")
        for metrik in ("biaya", "hasil", "biaya_per_hasil"):
            b = pembanding[metrik]
            label = b.get("label", metrik)
            if b["persen"] is None:
                L.append(f"{label}: {b['keterangan']}")
            else:
                nilai = fmt_rp(b["sekarang"]) if metrik != "hasil" else fmt_angka(b["sekarang"])
                L.append(f"{label}: {nilai} ({b['keterangan']} dari minggu lalu)")

    if h["tiga_terbaik"]:
        L.append("")
        L.append(f"3 TERBAIK (biaya per {h['nama_hasil']} termurah)")
        for i, k in enumerate(h["tiga_terbaik"], 1):
            L.append(f"{i}. {k['nama']}: {fmt_rp(k['biaya_per_hasil'])}/{h['nama_hasil']} "
                     f"({fmt_angka(k['hasil'])} {h['nama_hasil']}, {fmt_rp(k['biaya'])})")
    if h["tiga_terburuk"]:
        L.append("")
        L.append("3 PERLU PERHATIAN (biaya per hasil termahal / tanpa hasil)")
        for i, k in enumerate(h["tiga_terburuk"], 1):
            if k["hasil"] == 0:
                L.append(f"{i}. {k['nama']}: {fmt_rp(k['biaya'])} terpakai, 0 {h['nama_hasil']}")
            else:
                L.append(f"{i}. {k['nama']}: {fmt_rp(k['biaya_per_hasil'])}/{h['nama_hasil']} "
                         f"({fmt_angka(k['hasil'])} {h['nama_hasil']}, {fmt_rp(k['biaya'])})")

    L.append("")
    L.append("SARAN")
    for i, s in enumerate(h["saran"], 1):
        L.append(f"{i}. {s}")
    L.append("(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)")

    catatan = list(h.get("catatan_mata_uang", []))
    peringatan = list(h.get("peringatan", []))
    if h["baris_dilewati_baris_total"]:
        catatan.append(f"{h['baris_dilewati_baris_total']} baris 'Total/Jumlah' di file diabaikan agar tidak dihitung dua kali.")
    if h["baris_dilewati_lainnya"]:
        peringatan.append(f"Baris dilewati karena data tidak terbaca: {h['baris_dilewati_lainnya']}")
    if catatan:
        L.append("")
        L.append("Catatan: " + " ".join(catatan))
    if peringatan:
        L.append("")
        L.append("⚠️ " + " ".join(peringatan))
    return "\n".join(L)


# --------------------------------------------------------------------------------------
# Mode gabung (lintas platform)
# --------------------------------------------------------------------------------------

def gabung(daftar_json, omzet=None):
    total = {"biaya": 0.0, "tayangan": 0.0, "klik": 0.0, "hasil": 0.0, "nilai_hasil": 0.0}
    per_platform = []
    saran_semua = []
    peringatan_semua = []
    nama_hasil = None
    ada_nilai_hasil = False
    for h in daftar_json:
        t = h["total"]
        for k in total:
            total[k] += t.get(k) or 0.0
        if t.get("nilai_hasil"):
            ada_nilai_hasil = True
        per_platform.append({"platform": h["platform_terdeteksi"], "biaya": t["biaya"],
                              "hasil": t["hasil"], "biaya_per_hasil": t["biaya_per_hasil"],
                              "nama_hasil": h["nama_hasil"]})
        saran_semua.extend(f"[{h['platform_terdeteksi']}] {s}" for s in h["saran"])
        peringatan_semua.extend(h.get("peringatan", []))
        nama_hasil = nama_hasil or h["nama_hasil"]

    biaya_total = total["biaya"]
    for p in per_platform:
        p["persen_biaya"] = bulat_satu_desimal(p["biaya"] / biaya_total * 100) if biaya_total else None

    nama_hasil_beda = len({p["nama_hasil"] for p in per_platform}) > 1
    if nama_hasil_beda:
        peringatan_semua.append(
            "Platform-platform ini mengukur 'hasil' dengan nama/definisi berbeda ("
            + ", ".join(sorted({p['nama_hasil'] for p in per_platform}))
            + ") — total hasil, biaya-per-hasil, dan ROAS gabungan di bawah ini hanya perkiraan kasar "
              "lintas platform, bukan angka yang benar-benar setara. Baca rincian per platform di bawah "
              "untuk angka yang lebih akurat per jenis hasil.")

    t_cpc = bagi(total["biaya"], total["klik"])
    t_cpm = bagi(total["biaya"], total["tayangan"])
    t_cpm = t_cpm * 1000 if t_cpm is not None else None
    t_ctr = bagi(total["klik"], total["tayangan"])
    t_ctr = t_ctr * 100 if t_ctr is not None else None
    t_bph = bagi(total["biaya"], total["hasil"])
    t_roas = bagi(total["nilai_hasil"], total["biaya"]) if ada_nilai_hasil else None

    hasil_gabungan = {
        "platform_terdeteksi": " + ".join(sorted(set(p["platform"] for p in per_platform))),
        "mata_uang": "IDR",
        "total": {**total, "cpc": t_cpc, "cpm": t_cpm, "ctr_persen": t_ctr,
                  "biaya_per_hasil": t_bph, "roas": t_roas if ada_nilai_hasil else None},
        "per_platform": per_platform,
        "nama_hasil": nama_hasil or "hasil",
        "saran": saran_semua[:5] or ["Belum ada kampanye yang menonjol biaya-per-hasilnya minggu ini."],
        "peringatan": list(dict.fromkeys(peringatan_semua)),
    }
    return hasil_gabungan


def susun_teks_gabung(g, omzet=None):
    L = ["LAPORAN IKLAN MINGGUAN — GABUNGAN SEMUA PLATFORM", ""]
    t = g["total"]
    L.append(f"Total belanja iklan (semua platform): {fmt_rp(t['biaya'])}")
    for p in g["per_platform"]:
        L.append(f"- {p['platform']}: {fmt_rp(p['biaya'])} ({fmt_persen(p['persen_biaya'])} dari total), "
                 f"biaya per {p['nama_hasil']}: {fmt_rp(p['biaya_per_hasil'])}")
    L.append(f"Tayangan: {fmt_angka(t['tayangan'])} | Klik: {fmt_angka(t['klik'])} "
              f"| {g['nama_hasil'].capitalize()}: {fmt_angka(t['hasil'])}")
    L.append(f"CPC: {fmt_rp(t['cpc'])} | CPM: {fmt_rp(t['cpm'])} | CTR: {fmt_persen(t['ctr_persen'])}")
    L.append(f"Biaya per {g['nama_hasil']} (gabungan): {fmt_rp(t['biaya_per_hasil'])}")
    if t.get("roas") is not None:
        L.append(f"ROAS gabungan: {fmt_satu_desimal_x(t['roas'])}")
    if omzet:
        L.append(f"Biaya iklan vs omzet: {fmt_persen(omzet['biaya_sebagai_persen_omzet'])} dari omzet {fmt_rp(omzet['omzet'])}")
    L.append("")
    L.append("SARAN")
    for i, s in enumerate(g["saran"], 1):
        L.append(f"{i}. {s}")
    L.append("(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)")
    if g["peringatan"]:
        L.append("")
        L.append("⚠️ " + " ".join(g["peringatan"]))
    return "\n".join(L)


def sanitasi_sel_csv(nilai):
    """Cegah formula injection (CSV/Excel) bila nama kampanye dari file sumber diawali
    karakter pemicu formula ('=', '+', '-', '@', tab, CR). Diberi awalan kutip tunggal
    agar dibaca sebagai teks, bukan dieksekusi sebagai formula saat dibuka di Excel/Sheets.
    """
    s = str(nilai)
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + s
    return s


def tulis_csv_kampanye(path, daftar_kampanye, nama_hasil):
    kolom = ["nama", "biaya", "tayangan", "klik", "hasil", "nilai_hasil", "cpc", "cpm",
             "ctr_persen", "biaya_per_hasil", "roas"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["nama_kampanye", "biaya_rp", "tayangan", "klik", nama_hasil, "nilai_hasil_rp",
                    "cpc_rp", "cpm_rp", "ctr_persen", "biaya_per_" + nama_hasil.replace(" ", "_") + "_rp",
                    "roas_x"])
        for k in daftar_kampanye:
            w.writerow([
                sanitasi_sel_csv(k["nama"]),
                bulat_rupiah(k["biaya"]),
                fmt_angka(k["tayangan"]),
                fmt_angka(k["klik"]),
                fmt_angka(k["hasil"]),
                bulat_rupiah(k["nilai_hasil"]) if k.get("nilai_hasil") else "",
                bulat_rupiah(k["cpc"]) if k["cpc"] is not None else "",
                bulat_rupiah(k["cpm"]) if k["cpm"] is not None else "",
                bulat_satu_desimal(k["ctr_persen"]) if k["ctr_persen"] is not None else "",
                bulat_rupiah(k["biaya_per_hasil"]) if k["biaya_per_hasil"] is not None else "",
                bulat_satu_desimal(k["roas"]) if k.get("roas") is not None else "",
            ])


def hitung_omzet(total_biaya, omzet_teks):
    omzet = parse_angka(omzet_teks)
    if omzet is None:
        raise ValueError(f"Nilai --omzet '{omzet_teks}' tidak terbaca sebagai angka rupiah.")
    if omzet <= 0:
        raise ValueError("--omzet harus lebih besar dari 0.")
    return {"omzet": omzet, "biaya_sebagai_persen_omzet": bulat_satu_desimal(total_biaya / omzet * 100)}


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def buat_parser():
    p = argparse.ArgumentParser(description="Laporan iklan mingguan (Meta/TikTok/Shopee/Google Ads)")
    sub = p.add_subparsers(dest="mode", required=True)

    a = sub.add_parser("analisis", help="Analisis satu file ekspor iklan (satu platform, satu minggu)")
    a.add_argument("file")
    a.add_argument("--sebelumnya", help="File ekspor minggu sebelumnya (platform sama) untuk perbandingan")
    a.add_argument("--platform", help="Label platform manual bila deteksi otomatis meleset/kosong")
    a.add_argument("--kolom-nama")
    a.add_argument("--kolom-biaya")
    a.add_argument("--kolom-tayangan")
    a.add_argument("--kolom-klik")
    a.add_argument("--kolom-hasil")
    a.add_argument("--kolom-nilai-hasil")
    a.add_argument("--nama-hasil", help="Label hasil di laporan, mis. 'pesan WA', 'pembelian', 'leads'")
    a.add_argument("--mata-uang", choices=["IDR"], help="Paksa anggap file berlabel non-IDR sebagai IDR")
    a.add_argument("--kurs", type=float, help="Nilai tukar 1 satuan mata uang asing ke Rupiah")
    a.add_argument("--kurs-sumber")
    a.add_argument("--kurs-tanggal")
    a.add_argument("--periode", help="Label periode bila file tidak punya kolom tanggal")
    a.add_argument("--omzet", help="Omzet penjualan periode ini (untuk hitung biaya iklan sebagai % omzet)")
    a.add_argument("--top", type=int, default=3)
    a.add_argument("--json", action="store_true")
    a.add_argument("--csv-keluaran", help="Simpan rincian per kampanye sebagai file CSV (aman dibuka di Excel)")

    g = sub.add_parser("gabung", help="Gabungkan beberapa hasil --json 'analisis' (lintas platform)")
    g.add_argument("files", nargs="+", help="File JSON hasil 'analisis --json'")
    g.add_argument("--omzet")
    g.add_argument("--json", action="store_true")
    return p


def keluar_error(pesan):
    print(json.dumps({"error": pesan}, ensure_ascii=False), file=sys.stderr)
    sys.exit(2)


def jalankan_analisis(args):
    override = {"nama": args.kolom_nama, "biaya": args.kolom_biaya, "tayangan": args.kolom_tayangan,
                "klik": args.kolom_klik, "hasil": args.kolom_hasil, "nilai_hasil": args.kolom_nilai_hasil}
    try:
        hasil = analisis_file(args.file, override, args)
    except (ValueError, OSError) as e:
        keluar_error(str(e))
        return

    pembanding = None
    if args.sebelumnya:
        try:
            hasil_lalu = analisis_file(args.sebelumnya, override, args)
        except (ValueError, OSError) as e:
            keluar_error(f"Gagal membaca file minggu sebelumnya: {e}")
            return
        pembanding = bandingkan(hasil, hasil_lalu)
        if hasil["nama_hasil"] != hasil_lalu["nama_hasil"] or \
                hasil["platform_terdeteksi"] != hasil_lalu["platform_terdeteksi"]:
            hasil["peringatan"].append(
                f"File minggu ini ('{hasil['platform_terdeteksi']}', hasil='{hasil['nama_hasil']}') dan "
                f"minggu lalu ('{hasil_lalu['platform_terdeteksi']}', hasil='{hasil_lalu['nama_hasil']}') "
                "tampak berbeda platform/jenis hasil — perbandingan % di bawah ini mungkin tidak "
                "membandingkan hal yang sama. Pastikan kedua file dari platform yang sama.")

    omzet = None
    if args.omzet:
        try:
            omzet = hitung_omzet(hasil["total"]["biaya"], args.omzet)
        except ValueError as e:
            keluar_error(str(e))
            return

    hasil["pembanding_minggu_lalu"] = pembanding
    hasil["omzet"] = omzet
    hasil["teks"] = susun_teks(hasil, pembanding, omzet)

    if args.csv_keluaran:
        tulis_csv_kampanye(args.csv_keluaran, hasil["per_kampanye"], hasil["nama_hasil"])

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    else:
        print(hasil["teks"])


def jalankan_gabung(args):
    daftar = []
    for f in args.files:
        try:
            with open(f, encoding="utf-8") as fh:
                daftar.append(json.load(fh))
        except (OSError, json.JSONDecodeError) as e:
            keluar_error(f"Gagal membaca '{f}': jalankan dulu 'analisis --json' untuk tiap platform. ({e})")
            return
    g = gabung(daftar)
    omzet = None
    if args.omzet:
        try:
            omzet = hitung_omzet(g["total"]["biaya"], args.omzet)
        except ValueError as e:
            keluar_error(str(e))
            return
    g["omzet"] = omzet
    g["teks"] = susun_teks_gabung(g, omzet)
    if args.json:
        print(json.dumps(g, ensure_ascii=False, indent=2, default=str))
    else:
        print(g["teks"])


def main():
    args = buat_parser().parse_args()
    try:
        if args.mode == "analisis":
            jalankan_analisis(args)
        elif args.mode == "gabung":
            jalankan_gabung(args)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 - skill ini dipakai pengguna awam, jangan pernah traceback mentah
        keluar_error(f"Terjadi kesalahan tak terduga: {e}")


if __name__ == "__main__":
    main()
