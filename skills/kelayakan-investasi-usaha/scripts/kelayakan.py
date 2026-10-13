#!/usr/bin/env python3
"""Kelayakan investasi usaha kecil-menengah: payback, payback terdiskonto, NPV, IRR,
profitability index (PI), BEP tahunan, dan analisis sensitivitas.

Hanya library standar Python 3.8+. Tidak ada akses jaringan, tidak membaca/menulis file
(kecuali --output-json bila diminta).

Konvensi (ditulis ulang dari definisi numpy-financial, BSD-3-Clause, lihat ATTRIBUTION.md):
  * Arus kas periode 0 = investasi awal, bertanda NEGATIF; periode 1..n = arus kas bersih
    akhir tahun ke-1..n (positif = uang masuk).
  * NPV  = sum_{t=0..n} CF_t / (1 + r)^t
  * IRR  = r yang membuat NPV = 0. Dicari dengan pemindaian + bisection (kokoh, tanpa numpy).
           Tidak ada IRR bila semua arus kas bertanda sama. Bila ada beberapa akar, dipilih
           akar >= 0 terkecil; bila semua negatif, akar yang paling dekat ke nol.
  * PMT  = cicilan tetap: -(fv + pv(1+r)^n) / ((1+r)^n - 1) * r   (r = 0 -> -(fv+pv)/n)
           Dipakai untuk "biaya modal tahunan setara" pada BEP ekonomi.
  * PI   = nilai kini arus kas tahun 1..n / investasi awal.

Pembulatan: nominal rupiah per baris dibulatkan ke rupiah terdekat (0,5 ke atas); pajak
dibulatkan ke bawah (tidak pernah melebihi tarif). Hasil adalah alat bantu, bukan nasihat keuangan.
"""
import argparse
import json
import re
import sys
from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

getcontext().prec = 40
VERSI = "1.0.5"
DISKONTO_DEFAULT = Decimal("12")
DISKONTO_KETAT = Decimal("20")
LABEL_MANFAAT = {"omzet": "Omzet", "penghematan": "Penghematan", "pemasukan": "Pemasukan tambahan"}
ASAL_DISKONTO = ("bunga KUR Mikro/Kecil sektor produksi 6% efektif/tahun (acuan Permenko Perekonomian "
                 "No. 1 Tahun 2026 Pasal 37 & 44, berlaku 13 Januari 2026; konfirmasi ke bank penyalur) + "
                 "tambahan risiko usaha 6%")
SENS_DEFAULT = "omzet-10;omzet-20;biaya+10"
LABEL_AGENT = "[UNTUK AGENT SAJA - jangan disalin apa adanya; sampaikan dengan bahasa awam, tanpa menyebut script/file/proses]"
DISCLAIMER = ("Bukan nasihat keuangan. Hasil sepenuhnya tergantung asumsi (omzet, biaya, umur, tingkat "
              "diskonto); angka nyata bisa berbeda. Tidak ada jaminan untung.")


class Galat(Exception):
    def __init__(self, pesan, saran=""):
        super().__init__(pesan)
        self.pesan, self.saran = pesan, saran


# ---------------------------------------------------------------- parsing
PENGALI = {"rb": 10**3, "ribu": 10**3, "k": 10**3, "jt": 10**6, "juta": 10**6,
           "m": 10**9, "miliar": 10**9, "milyar": 10**9, "t": 10**12, "triliun": 10**12}


def periode_dari(teks):
    s = teks.lower()
    if re.search(r"(/|per\s*|se)\s*(bln|bulan)\b", s):
        return "bulan"
    if re.search(r"(/|per\s*|se)\s*(thn|tahun|th)\b", s):
        return "tahun"
    return None


def parse_rupiah(teks, nama):
    """'Rp 45.000.000' | '45jt' | '1,5 juta' | '150rb' | '(5jt)' | 'minus 5jt' | '9jt/bulan' -> (Decimal, periode)."""
    if teks is None:
        return None, None
    asli = str(teks)
    s = asli.strip().lower()
    periode = periode_dari(s)
    s = re.sub(r"(/|per\s*|se)\s*(bln|bulan|thn|tahun|th)\b", "", s)
    s = re.sub(r"^\s*(rp|idr)\.?\s*", "", s).strip()
    negatif = False
    if s.startswith("(") and s.endswith(")"):
        negatif, s = True, s[1:-1].strip()
    m = re.match(r"^(minus|min|-)\s*", s)
    if m:
        negatif, s = True, s[m.end():]
    s = s.replace(" ", "")
    m = re.fullmatch(r"([0-9][0-9.,]*)(rb|ribu|k|jt|juta|m|miliar|milyar|t|triliun)?", s)
    if not m:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca",
                    "Tulis seperti 45000000, 45.000.000, 45jt, 1,5jt, atau 150rb.")
    num, suf = m.group(1).strip(".,"), m.group(2)
    if "," in num and "." in num:
        num = num.replace(".", "").replace(",", ".") if num.rfind(",") > num.rfind(".") else num.replace(",", "")
    elif "," in num:
        b = num.split(",")
        if len(b) > 2:
            num = num.replace(",", "")
        elif len(b[1]) == 3 and not suf:
            raise Galat(f"{nama}: '{asli}' ambigu (koma bisa ribuan atau desimal)",
                        "Tulis 45.000 atau 45rb untuk empat puluh lima ribu.")
        else:
            num = num.replace(",", ".")
    elif "." in num:
        b = num.split(".")
        if len(b) > 2 or len(b[1]) == 3:
            num = num.replace(".", "")
    try:
        v = Decimal(num) * Decimal(PENGALI[suf] if suf else 1)
    except InvalidOperation:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca", "Contoh: 45jt")
    return (-v if negatif else v), periode


def parse_persen(teks, nama):
    if teks is None:
        return None, None
    s = str(teks).strip().lower()
    periode = periode_dari(s)
    s = re.sub(r"(/|per\s*|se)\s*(bln|bulan|thn|tahun|th)\b", "", s)
    s = s.replace("%", "").replace("persen", "").replace("efektif", "").strip().replace(",", ".")
    try:
        v = Decimal(s)
    except InvalidOperation:
        raise Galat(f"{nama}: persen '{teks}' tidak terbaca", "Contoh: 12 atau 12% atau 0,5%")
    return v, periode


def pecah_daftar(teks):
    s = str(teks).strip()
    if ";" in s or "\n" in s:
        return [x.strip() for x in re.split(r"[;\n]", s) if x.strip()]
    if re.search(r"[a-z)]\s*,\s*[-(0-9rm]", s.lower()):
        return [x.strip() for x in s.split(",") if x.strip()]
    if re.search(r"\d\s+\d", s) and not re.search(r"\d\.\d{3}", s):
        raise Galat("daftar angka dipisah spasi", "Pisahkan tiap tahun dengan titik koma, mis. \"15jt;18jt;20jt\".")
    return [s]


def daftar_rupiah(teks, nama, n=None):
    """Kembalikan list Decimal per TAHUN (nilai /bulan dikali 12) + catatan."""
    catatan = []
    nilai = []
    for i, bagian in enumerate(pecah_daftar(teks), start=1):
        v, per = parse_rupiah(bagian, f"{nama} ke-{i}")
        if per == "bulan":
            v *= 12
            catatan.append(f"{nama} ke-{i} ditulis per bulan, dikali 12 menjadi per tahun.")
        nilai.append(v)
    if n and len(nilai) == 1:
        nilai = nilai * n
    return nilai, catatan


def bulat(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def bawah(x):
    return int(Decimal(x).to_integral_value(rounding=ROUND_FLOOR))


def rp(n):
    n = int(n)
    return ("-" if n < 0 else "") + "Rp" + f"{abs(n):,}".replace(",", ".")


def pct(x, d=2):
    if x is None:
        return "-"
    return f"{x:.{d}f}".replace(".", ",") + "%"


# ---------------------------------------------------------------- rumus inti
def npv(rate, values):
    """NPV dengan arus kas dimulai di t = 0 (konvensi numpy-financial)."""
    r = Decimal(str(rate))
    if r <= -1:
        raise ValueError("tingkat diskonto harus > -100%")
    total = Decimal(0)
    faktor = Decimal(1)
    for v in values:
        total += Decimal(str(v)) / faktor
        faktor *= (1 + r)
    return total


def pmt(rate, nper, pv, fv=0):
    """Cicilan tetap akhir periode (konvensi numpy-financial: hasil negatif untuk pv positif)."""
    r, n, pv, fv = Decimal(str(rate)), int(nper), Decimal(str(pv)), Decimal(str(fv))
    if n <= 0:
        raise ValueError("nper harus > 0")
    if r == 0:
        return -(fv + pv) / n
    temp = (1 + r) ** n
    return -(fv + pv * temp) * r / (temp - 1)


def _npv_float(r, vals):
    total, f = 0.0, 1.0
    for v in vals:
        total += v / f
        f *= (1.0 + r)
    return total


def irr_semua(values, lo=-0.99, hi=10.0):
    """Semua akar NPV=0 di rentang [-99%, 1000%] (pemindaian + bisection)."""
    vals = [float(v) for v in values]
    if all(v >= 0 for v in vals) or all(v <= 0 for v in vals):
        return []
    grid = [lo + i * 0.0025 for i in range(int((1.0 - lo) / 0.0025) + 1)]
    grid += [1.0 + i * 0.01 for i in range(1, int((hi - 1.0) / 0.01) + 1)]
    akar = []
    r0, f0 = grid[0], _npv_float(grid[0], vals)
    if f0 == 0:
        akar.append(r0)
    for r1 in grid[1:]:
        f1 = _npv_float(r1, vals)
        if f1 == 0:
            akar.append(r1)
        elif f0 != 0 and (f0 < 0) != (f1 < 0):
            a, b, fa = r0, r1, f0
            for _ in range(200):
                mid = (a + b) / 2
                fm = _npv_float(mid, vals)
                if fm == 0 or (b - a) < 1e-15:
                    a = b = mid
                    break
                if (fa < 0) == (fm < 0):
                    a, fa = mid, fm
                else:
                    b = mid
            akar.append((a + b) / 2)
        r0, f0 = r1, f1
    unik = []
    for x in sorted(akar):
        if not unik or abs(x - unik[-1]) > 1e-9:
            unik.append(x)
    return unik


def irr(values):
    """IRR (desimal, mis. 0.28 = 28%) atau None bila tidak ada."""
    akar = irr_semua(values)
    if not akar:
        return None
    pos = [x for x in akar if x >= 0]
    return min(pos) if pos else max(akar)


def payback(arus, investasi):
    """arus = list arus kas tahun 1..n. Kembalikan tahun (Decimal) saat kumulatif >= investasi, atau None."""
    sisa = Decimal(investasi)
    for t, cf in enumerate(arus, start=1):
        cf = Decimal(cf)
        if cf > 0 and cf >= sisa:
            return Decimal(t - 1) + (sisa / cf if sisa > 0 else Decimal(0))
        sisa -= cf
    return None


def teks_tahun(th):
    if th is None:
        return "tidak balik modal dalam masa proyek"
    bln = bulat(Decimal(th) * 12)
    t, b = divmod(bln, 12)
    if t == 0:
        return f"{b} bulan"
    return f"{t} tahun" + (f" {b} bulan" if b else "")


# ---------------------------------------------------------------- model
def bangun(p, f_omzet=Decimal(1), f_biaya=Decimal(1), f_arus=Decimal(1), omzet_rata=None):
    """Bangun tabel arus kas tahunan untuk skenario tertentu."""
    n = p["tahun"]
    baris = []
    for t in range(1, n + 1):
        dep = p["penyusutan"][t - 1]
        b = {"tahun": t, "penyusutan": bulat(dep)}
        if p["mode"] == "omzet":
            omzet = bulat((omzet_rata if omzet_rata is not None else p["omzet"][t - 1]) * f_omzet)
            var = bulat(omzet * p["v"] * f_biaya)
            tetap = bulat(p["tetap"][t - 1] * f_biaya)
            laba_tunai = omzet - var - tetap
            if p["pajak"] > 0 and p["dasar_pajak"] == "omzet":
                pajak = bawah(Decimal(max(omzet, 0)) * p["pajak"] / 100)
            elif p["pajak"] > 0:
                pajak = bawah(Decimal(max(laba_tunai - b["penyusutan"], 0)) * p["pajak"] / 100)
            else:
                pajak = 0
            b.update({"omzet": omzet, "biaya_variabel": var, "biaya_tetap": tetap,
                      "laba_sebelum_pajak": laba_tunai - b["penyusutan"], "pajak": pajak})
            cf = laba_tunai - pajak
        else:
            pre = bulat(p["arus"][t - 1] * f_arus)
            pajak = bawah(Decimal(max(pre - b["penyusutan"], 0)) * p["pajak"] / 100) if p["pajak"] > 0 else 0
            b.update({"arus_kas_sebelum_pajak": pre, "pajak": pajak})
            cf = pre - pajak
        b["arus_kas_operasional"] = cf
        b["nilai_sisa"] = bulat(p["nilai_sisa"]) if t == n else 0
        b["arus_kas_bersih"] = cf + b["nilai_sisa"]
        baris.append(b)
    return baris


def hitung(p, baris):
    r = p["diskonto"] / 100
    inv = p["investasi"]
    nilai = [-inv] + [Decimal(b["arus_kas_bersih"]) for b in baris]
    hasil_npv = npv(r, nilai)
    kum, kum_pv, faktor = -inv, -inv, Decimal(1)
    pv_operasional = []
    for b in baris:
        faktor *= (1 + r)
        pv = Decimal(b["arus_kas_bersih"]) / faktor
        kum += b["arus_kas_bersih"]
        kum_pv += pv
        b["kumulatif"] = bulat(kum)
        b["nilai_kini"] = bulat(pv)
        b["nilai_kini_kumulatif"] = bulat(kum_pv)
        pv_operasional.append(Decimal(b["arus_kas_operasional"]) / faktor)
    akar = irr_semua(nilai)
    nilai_irr = irr(nilai)
    pb = payback([b["arus_kas_operasional"] for b in baris], inv)
    pbd = payback(pv_operasional, inv)
    pv_masuk = sum(Decimal(b["arus_kas_bersih"]) / (1 + r) ** b["tahun"] for b in baris)
    return {
        "npv": bulat(hasil_npv),
        "irr_persen": None if nilai_irr is None else round(nilai_irr * 100, 2),
        "irr_jumlah_akar": len(akar),
        "irr_semua_akar_persen": [round(x * 100, 2) for x in akar],
        "pi": float((pv_masuk / inv).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        "payback_tahun": None if pb is None else float(pb.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        "payback_teks": teks_tahun(pb),
        "payback_diskonto_tahun": None if pbd is None else float(pbd.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
        "payback_diskonto_teks": teks_tahun(pbd),
        "_npv_dec": hasil_npv,
    }


def npv_skenario(p, **kw):
    baris = bangun(p, **kw)
    nilai = [-p["investasi"]] + [Decimal(b["arus_kas_bersih"]) for b in baris]
    return npv(p["diskonto"] / 100, nilai)


def cari_faktor(fungsi, lo, hi, iterasi=80):
    """Cari x di [lo, hi] dengan fungsi(x) = 0 (fungsi monoton). None bila tanda tidak berubah."""
    flo, fhi = fungsi(lo), fungsi(hi)
    if flo == 0:
        return lo
    if (flo < 0) == (fhi < 0):
        return None
    for _ in range(iterasi):
        mid = (lo + hi) / 2
        fm = fungsi(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def bep(p):
    """BEP tahunan (mode omzet, memakai biaya tahun ke-1)."""
    v, F, dep = p["v"], p["tetap"][0], p["penyusutan"][0]
    t_omzet = p["pajak"] / 100 if (p["pajak"] > 0 and p["dasar_pajak"] == "omzet") else Decimal(0)
    marjin = 1 - v - t_omzet
    out = {}
    if marjin <= 0:
        out["bep_akuntansi_omzet_per_tahun"] = None
        out["bep_ekonomi_omzet_per_tahun"] = None
        out["bep_catatan"] = "Biaya variabel + pajak omzet >= 100% omzet: impas tidak pernah tercapai."
        return out
    akt = (F + dep) / marjin
    out["bep_akuntansi_omzet_per_tahun"] = bulat(akt)
    out["bep_akuntansi_omzet_per_bulan"] = bulat(akt / 12)
    r = p["diskonto"] / 100
    n = p["tahun"]
    pv_sisa = p["nilai_sisa"] / (1 + r) ** n
    out["biaya_modal_tahunan_setara"] = bulat(-pmt(r, n, p["investasi"] - pv_sisa))
    fungsi = lambda s: npv_skenario(p, omzet_rata=Decimal(s))
    atas = Decimal(10) * (p["investasi"] + F * n + 1) / marjin
    eko = cari_faktor(fungsi, Decimal(0), atas)
    out["bep_ekonomi_omzet_per_tahun"] = None if eko is None else bulat(eko)
    out["bep_ekonomi_omzet_per_bulan"] = None if eko is None else bulat(eko / 12)
    return out


def parse_sens(teks, mode):
    hasil = []
    for bagian in pecah_daftar(teks or SENS_DEFAULT):
        m = re.fullmatch(r"\s*(omzet|penghematan|pemasukan|biaya|arus|arus-kas)\s*([+-])\s*(\d+(?:[.,]\d+)?)\s*%?\s*", bagian.lower())
        if not m:
            raise Galat(f"skenario sensitivitas '{bagian}' tidak terbaca", "Contoh: \"omzet-10;omzet-20;biaya+10\" (omzet = penghematan/pemasukan)")
        jenis = "arus" if m.group(1).startswith("arus") else m.group(1)
        if jenis in ("penghematan", "pemasukan"):
            jenis = "omzet"
        besar = Decimal(m.group(3).replace(",", ".")) * (1 if m.group(2) == "+" else -1)
        if mode == "arus" and jenis == "omzet":
            jenis = "arus"
        if mode == "arus" and jenis == "biaya":
            continue
        hasil.append((jenis, besar))
    return hasil


# ---------------------------------------------------------------- utama
def siapkan(a):
    catatan, peringatan, asumsi = [], [], []
    if a.investasi is None:
        raise Galat("investasi awal belum diisi", "Isi --investasi, mis. 45jt.")
    inv, _ = parse_rupiah(a.investasi, "investasi")
    if inv <= 0:
        raise Galat("investasi harus lebih dari 0", "Isi nilai pembelian/biaya awal, mis. 45jt.")
    if a.arus_kas and (a.omzet or a.biaya or a.biaya_variabel or a.hpp_persen):
        raise Galat("pakai --arus-kas ATAU --omzet/--biaya, jangan keduanya",
                    "--arus-kas = uang bersih masuk per tahun; --omzet + --biaya = rinciannya.")
    if not a.arus_kas and not a.omzet:
        raise Galat("arus kas belum diisi", "Isi --arus-kas per tahun, atau --omzet dan --biaya.")
    n_arg = a.tahun
    if n_arg is not None and not 1 <= n_arg <= 30:
        raise Galat("--tahun harus 1 sampai 30", "Masa proyek dalam tahun, mis. 5.")
    p = {"investasi": inv, "pajak": Decimal(0), "dasar_pajak": a.dasar_pajak, "jenis": a.jenis}
    if a.arus_kas and a.jenis != "omzet":
        raise Galat("--jenis hanya untuk --omzet", "Dengan --arus-kas, angka sudah berupa uang bersih per tahun.")

    if a.arus_kas:
        p["mode"] = "arus"
        arus, c = daftar_rupiah(a.arus_kas, "arus kas", n_arg)
        catatan += c
        if n_arg and len(arus) != n_arg:
            raise Galat(f"jumlah arus kas ({len(arus)}) tidak sama dengan --tahun ({n_arg})",
                        "Isi satu angka (dipakai tiap tahun) atau satu angka per tahun.")
        p["arus"], p["tahun"] = arus, len(arus)
    else:
        p["mode"] = "omzet"
        lbl = LABEL_MANFAAT[a.jenis].lower()
        omzet, c = daftar_rupiah(a.omzet, lbl, None)
        catatan += c
        n = n_arg or (len(omzet) if len(omzet) > 1 else 5)
        if n_arg is None and len(omzet) == 1:
            asumsi.append("Masa proyek 5 tahun (default).")
        if len(omzet) == 1:
            naik = parse_persen(a.kenaikan_omzet, "kenaikan omzet")[0] if a.kenaikan_omzet else Decimal(0)
            omzet = [omzet[0] * (1 + naik / 100) ** t for t in range(n)]
            if naik:
                asumsi.append(f"{lbl.capitalize()} naik {pct(naik, 1)} per tahun.")
        if len(omzet) != n:
            raise Galat(f"jumlah omzet ({len(omzet)}) tidak sama dengan --tahun ({n})",
                        "Isi satu angka omzet atau satu angka per tahun.")
        if any(x < 0 for x in omzet):
            raise Galat("omzet tidak boleh negatif", "Periksa angka omzet.")
        tetap, c = daftar_rupiah(a.biaya or "0", "biaya tetap", None)
        catatan += c
        if len(tetap) == 1:
            naikb = parse_persen(a.kenaikan_biaya, "kenaikan biaya")[0] if a.kenaikan_biaya else Decimal(0)
            tetap = [tetap[0] * (1 + naikb / 100) ** t for t in range(n)]
            if naikb:
                asumsi.append(f"Biaya tetap naik {pct(naikb, 1)} per tahun.")
        if len(tetap) != n:
            raise Galat(f"jumlah biaya ({len(tetap)}) tidak sama dengan masa proyek ({n})", "Isi satu angka biaya.")
        if any(x < 0 for x in tetap):
            raise Galat("biaya tidak boleh negatif", "Periksa angka biaya.")
        v = Decimal(0)
        if a.hpp_persen and a.biaya_variabel:
            raise Galat("pakai --hpp-persen ATAU --biaya-variabel", "Pilih salah satu.")
        if a.hpp_persen:
            v = parse_persen(a.hpp_persen, "biaya variabel")[0] / 100
        elif a.biaya_variabel:
            bv, c = daftar_rupiah(a.biaya_variabel, "biaya variabel", None)
            catatan += c
            if omzet[0] <= 0:
                raise Galat("omzet tahun 1 = 0, biaya variabel tidak bisa dijadikan persen", "Isi --hpp-persen.")
            v = bv[0] / omzet[0]
            catatan.append(f"Biaya variabel dianggap {pct(v * 100)} dari omzet (ikut naik-turun dengan omzet).")
        if not 0 <= v < 1:
            raise Galat("biaya variabel harus 0% sampai di bawah 100% omzet", "Periksa --hpp-persen.")
        if not a.biaya_variabel and not a.hpp_persen and a.biaya:
            asumsi.append(f"Semua biaya dianggap tetap (tidak ikut turun saat {lbl} turun) - perkiraan hati-hati.")
        p.update({"omzet": omzet, "tetap": tetap, "v": v, "tahun": n})

    n = p["tahun"]
    # diskonto
    if a.diskonto is None:
        d = DISKONTO_DEFAULT
        p["sumber_diskonto"] = "default"
        asumsi.append(f"Tingkat diskonto 12%/tahun (default): {ASAL_DISKONTO}. Ganti dengan bunga pinjaman "
                      "Anda sendiri atau hasil minimal yang Anda harapkan.")
    else:
        d, per = parse_persen(a.diskonto, "diskonto")
        p["sumber_diskonto"] = "pengguna"
        if per == "bulan":
            d *= 12
            catatan.append("Tingkat diskonto ditulis per bulan, dikali 12 menjadi per tahun.")
    if not Decimal(0) <= d <= Decimal(100):
        raise Galat("tingkat diskonto harus 0% sampai 100% per tahun", "Mis. 12.")
    p["diskonto"] = d
    if d < 6:
        peringatan.append("Tingkat diskonto di bawah 6%/tahun (bunga KUR produksi menurut Permenko Perekonomian "
                          "No. 1 Tahun 2026 Pasal 37 & 44, berlaku 13 Januari 2026; konfirmasi ke bank penyalur) "
                          "- hasil bisa terlalu optimis.")
    if d > 30:
        peringatan.append("Tingkat diskonto di atas 30%/tahun - pastikan memang disengaja.")

    # pajak
    if a.pajak_persen is not None:
        pj = parse_persen(a.pajak_persen, "pajak")[0]
        if not Decimal(0) <= pj <= Decimal(50):
            raise Galat("pajak harus 0% sampai 50%", "PPh final UMKM 0,5 (dari omzet) atau PPh badan 22 (dari laba).")
        if pj > 0 and p["mode"] == "arus" and a.dasar_pajak == "omzet":
            raise Galat("pajak dari omzet butuh angka omzet",
                        "Pakai --omzet/--biaya, atau --dasar-pajak laba bila pajaknya dari laba.")
        if pj > 0 and a.jenis == "penghematan" and a.dasar_pajak == "omzet":
            raise Galat("pajak dari omzet tidak berlaku untuk penghematan (penghematan bukan omzet)",
                        "Hapus --pajak-persen, atau pakai --dasar-pajak laba bila usaha membayar PPh dari laba.")
        p["pajak"] = pj
        if pj > 0:
            asumsi.append(f"Pajak {pct(pj, 1)} dari {'omzet (seperti PPh final UMKM)' if a.dasar_pajak == 'omzet' else 'laba setelah penyusutan (seperti PPh badan)'}; tanpa kompensasi rugi.")
    else:
        asumsi.append("Pajak belum dihitung (bisa ditambahkan sebagai persen).")

    # penyusutan & nilai sisa
    umur = a.umur_ekonomis if a.umur_ekonomis is not None else n
    if not 1 <= umur <= 50:
        raise Galat("umur ekonomis harus 1 sampai 50 tahun", "Mis. mesin 5, mobil 8.")
    # Satu angka nilai sisa (--nilai-sisa = --nilai-residu): perkiraan harga jual kembali di akhir masa proyek.
    # Bila diisi, penyusutan garis lurus = (investasi - nilai sisa) / masa pakai dalam proyek, sehingga
    # nilai buku di akhir = nilai sisa. Bila kosong: residu 0, nilai sisa = nilai buku garis lurus.
    pakai = min(n, umur)
    if a.nilai_sisa is not None:
        ns = parse_rupiah(a.nilai_sisa, "nilai sisa")[0]
        if ns < 0:
            raise Galat("nilai sisa tidak boleh negatif", "Isi 0 bila tidak ada nilai jual kembali.")
        if ns > inv:
            peringatan.append("Nilai sisa lebih besar dari investasi - pastikan masuk akal (penyusutan dianggap 0).")
        residu = min(ns, inv)
        dep_th = (inv - residu) / pakai
        p["nilai_sisa"] = ns
        p["sumber_nilai_sisa"] = "pengguna"
        asumsi.append(f"Nilai sisa (perkiraan harga jual kembali) di akhir tahun ke-{n}: {rp(bulat(ns))}; "
                      f"penyusutan rata {rp(bulat(dep_th))}/tahun selama {pakai} tahun.")
    else:
        residu = Decimal(0)
        dep_th = inv / umur
        p["nilai_sisa"] = inv - dep_th * pakai
        p["sumber_nilai_sisa"] = "garis lurus"
        asumsi.append(f"Nilai sisa = nilai buku garis lurus (umur ekonomis {umur} tahun, nilai akhir Rp0): "
                      f"{rp(bulat(p['nilai_sisa']))} di akhir tahun ke-{n}.")
    p["penyusutan"] = [dep_th if t <= pakai else Decimal(0) for t in range(1, n + 1)]
    if n > umur:
        peringatan.append(f"Masa proyek ({n} th) lebih lama dari umur ekonomis ({umur} th): alat mungkin perlu diganti.")
    if n > 10:
        peringatan.append("Proyeksi lebih dari 10 tahun sangat tidak pasti.")
    p.update({"umur": umur, "residu": residu, "penyusutan_per_tahun": dep_th})
    return p, catatan, peringatan, asumsi


def cari_minimal(a):
    """Tanpa data omzet/arus kas: hitung arus kas bersih minimal agar balik modal & layak."""
    if a.investasi is None:
        raise Galat("investasi awal belum diisi", "Isi --investasi, mis. 85jt.")
    inv, _ = parse_rupiah(a.investasi, "investasi")
    if inv <= 0:
        raise Galat("investasi harus lebih dari 0", "Isi nilai pembelian/biaya awal.")
    n = a.tahun or 5
    if not 1 <= n <= 30:
        raise Galat("--tahun harus 1 sampai 30", "Mis. 5.")
    asumsi = []
    if a.tahun is None:
        asumsi.append("Masa proyek 5 tahun (default).")
    if a.diskonto is None:
        d = DISKONTO_DEFAULT
        asumsi.append(f"Tingkat diskonto 12%/tahun (default): {ASAL_DISKONTO}. Bisa diubah.")
    else:
        d, per = parse_persen(a.diskonto, "diskonto")
        d = d * 12 if per == "bulan" else d
    if not Decimal(0) <= d <= Decimal(100):
        raise Galat("tingkat diskonto harus 0% sampai 100% per tahun", "Mis. 12.")
    ns = parse_rupiah(a.nilai_sisa, "nilai sisa")[0] if a.nilai_sisa else Decimal(0)
    if ns < 0:
        raise Galat("nilai sisa tidak boleh negatif", "Isi 0 bila tidak ada.")
    asumsi.append(f"Nilai jual kembali di akhir: {rp(bulat(ns))}.")
    r = d / 100
    tahunan = -pmt(r, n, inv - ns / (1 + r) ** n)
    x = {
        "versi": VERSI, "mode": "cari-minimal",
        "input": {"investasi": bulat(inv), "masa_proyek_tahun": n, "diskonto_persen": float(d), "nilai_sisa": bulat(ns)},
        "hasil": {
            "arus_kas_minimal_layak_per_tahun": bulat(tahunan),
            "arus_kas_minimal_layak_per_bulan": bulat(tahunan / 12),
            "arus_kas_minimal_balik_modal_per_tahun": bulat(inv / n),
            "arus_kas_minimal_balik_modal_per_bulan": bulat(inv / n / 12),
        },
        "asumsi": asumsi, "disclaimer": DISCLAIMER,
    }
    h = x["hasil"]
    x["ringkasan_untuk_agent"] = "\n".join([
        LABEL_AGENT,
        f"Investasi {rp(bulat(inv))}, masa {n} tahun, diskonto {pct(d, 1)}.",
        f"Uang bersih minimal agar LAYAK (NPV = 0): {rp(h['arus_kas_minimal_layak_per_tahun'])}/tahun = {rp(h['arus_kas_minimal_layak_per_bulan'])}/bulan.",
        f"Uang bersih minimal agar sekadar balik modal dalam {n} tahun (tanpa nilai waktu uang): {rp(h['arus_kas_minimal_balik_modal_per_bulan'])}/bulan.",
        "Uang bersih = tambahan omzet - bahan baku - biaya operasional - pajak (atau penghematan bersih).",
        "Asumsi:"] + ["  - " + s for s in asumsi] + [DISCLAIMER])
    return x


def jalankan(a):
    if a.cari_minimal:
        return cari_minimal(a)
    p, catatan, peringatan, asumsi = siapkan(a)
    lbl = LABEL_MANFAAT[p["jenis"]]
    baris = bangun(p)
    h = hitung(p, baris)
    npv_dec = h.pop("_npv_dec")
    if p["mode"] == "omzet":
        h.update(bep(p))
        if p["pajak"] > 0 and p["dasar_pajak"] == "omzet" and p["omzet"][0] > Decimal("4800000000"):
            peringatan.append("Omzet di atas Rp4,8 miliar/tahun: PPh final 0,5% UMKM (PP 55/2022) tidak berlaku.")
        if baris[0]["arus_kas_operasional"] < 0:
            peringatan.append("Arus kas tahun pertama negatif: siapkan dana cadangan untuk menutup kekurangan.")
    else:
        if any(b["arus_kas_operasional"] < 0 for b in baris):
            peringatan.append("Ada tahun dengan arus kas negatif: siapkan dana cadangan.")
    if h["irr_jumlah_akar"] > 1:
        peringatan.append("IRR punya lebih dari satu jawaban (arus kas berganti tanda beberapa kali); "
                          "pakai NPV sebagai patokan utama.")

    # NPV uji ketat 20% (informasi; tidak mengubah status)
    if p["diskonto"] < DISKONTO_KETAT:
        nilai = [-p["investasi"]] + [Decimal(b["arus_kas_bersih"]) for b in baris]
        h["npv_uji_ketat"] = bulat(npv(DISKONTO_KETAT / 100, nilai))
        h["diskonto_uji_ketat_persen"] = float(DISKONTO_KETAT)
    else:
        h["npv_uji_ketat"] = None
        h["diskonto_uji_ketat_persen"] = None

    # batas aman
    if p["mode"] == "omzet":
        f_turun = cari_faktor(lambda x: npv_skenario(p, f_omzet=Decimal(x)), Decimal(0), Decimal(1)) if npv_dec > 0 else None
        f_naik_b = cari_faktor(lambda x: npv_skenario(p, f_biaya=Decimal(x)), Decimal(1), Decimal(20)) if npv_dec > 0 else None
        f_perlu = cari_faktor(lambda x: npv_skenario(p, f_omzet=Decimal(x)), Decimal(1), Decimal(20)) if npv_dec < 0 else None
    else:
        f_turun = cari_faktor(lambda x: npv_skenario(p, f_arus=Decimal(x)), Decimal(0), Decimal(1)) if npv_dec > 0 else None
        f_naik_b = None
        f_perlu = cari_faktor(lambda x: npv_skenario(p, f_arus=Decimal(x)), Decimal(1), Decimal(20)) if npv_dec < 0 else None
    h["batas_penurunan_persen"] = None if f_turun is None else float(((1 - f_turun) * 100).quantize(Decimal("0.1")))
    h["batas_penurunan_dasar"] = lbl.lower() if p["mode"] == "omzet" else "arus kas"
    h["batas_kenaikan_biaya_persen"] = None if f_naik_b is None else float(((f_naik_b - 1) * 100).quantize(Decimal("0.1")))
    h["kenaikan_diperlukan_persen"] = None if f_perlu is None else float(((f_perlu - 1) * 100).quantize(Decimal("0.1")))
    h["penyusutan_per_tahun"] = bulat(p["penyusutan_per_tahun"])
    h["nilai_sisa"] = bulat(p["nilai_sisa"])

    # sensitivitas
    sens = []
    for jenis, besar in parse_sens(a.sensitivitas, p["mode"]):
        f = 1 + besar / 100
        if f < 0:
            raise Galat("skenario sensitivitas lebih dari -100%", "Mis. omzet-20.")
        kw = {"omzet": {"f_omzet": f}, "biaya": {"f_biaya": f}, "arus": {"f_arus": f}}[jenis]
        bs = bangun(p, **kw)
        hs = hitung(p, bs)
        hs.pop("_npv_dec")
        label = {"omzet": lbl, "biaya": "Biaya", "arus": "Arus kas"}[jenis]
        angka = format(besar, "f")
        angka = angka.rstrip("0").rstrip(".") if "." in angka else angka
        sens.append({"skenario": f"{label} {'+' if besar > 0 else ''}{angka.replace('.', ',')}%",
                     "jenis": jenis, "perubahan_persen": float(besar), "npv": hs["npv"],
                     "irr_persen": hs["irr_persen"], "payback_teks": hs["payback_teks"],
                     "tetap_layak": hs["npv"] >= 0})

    # kesimpulan
    alasan, syarat = [], []
    diskonto_txt = pct(p["diskonto"], 1)
    if h["irr_persen"] is None:
        irr_txt = "lebih dari 1000%" if h["npv"] > 0 else "tidak ada"
        if h["npv"] > 0:
            h["irr_catatan"] = "IRR di atas 1000% per tahun (di luar rentang pencarian)."
    else:
        irr_txt = pct(h["irr_persen"])
    kritis = [s for s in sens if s["perubahan_persen"] in (-10.0, 10.0)]
    if h["npv"] < 0:
        status = "TIDAK LAYAK"
        alasan.append(f"NPV minus {rp(-h['npv'])}: hasilnya belum menutup modal ditambah hasil minimal {diskonto_txt}/tahun.")
        if h["irr_persen"] is None:
            alasan.append("IRR tidak ada: uang yang kembali tidak pernah menutup modal.")
        else:
            alasan.append(f"IRR {irr_txt} di bawah tingkat diskonto {diskonto_txt}.")
        alasan.append(f"Balik modal: {h['payback_teks']}.")
        if h["kenaikan_diperlukan_persen"] is not None:
            syarat.append(f"{h['batas_penurunan_dasar'].capitalize()} perlu sekitar {pct(h['kenaikan_diperlukan_persen'], 1)} lebih tinggi dari perkiraan agar impas (NPV = 0).")
        if h.get("bep_ekonomi_omzet_per_bulan"):
            syarat.append(f"{lbl} minimal agar layak: sekitar {rp(h['bep_ekonomi_omzet_per_bulan'])}/bulan (bila sama tiap tahun).")
        syarat.append("Atau tekan nilai investasi (beli bekas/sewa dulu) atau biaya tetap.")
    else:
        rapuh = [s for s in kritis if not s["tetap_layak"]]
        if h["payback_tahun"] is None:
            status = "KURANG LAYAK"
            alasan.append("NPV tidak negatif hanya karena nilai jual kembali di akhir; dari operasional tidak balik modal dalam masa proyek.")
        elif rapuh:
            status = "KURANG LAYAK"
            alasan.append(f"NPV positif {rp(h['npv'])} tetapi tipis: " + ", ".join(s["skenario"].lower() for s in rapuh)
                          + " sudah membuat NPV negatif.")
        elif h["npv"] == 0:
            status = "KURANG LAYAK"
            alasan.append("NPV tepat nol: hanya impas dengan hasil minimal yang diminta.")
        else:
            status = "LAYAK"
            alasan.append(f"NPV positif {rp(h['npv'])} pada diskonto {diskonto_txt}; IRR {irr_txt} di atas {diskonto_txt}.")
            alasan.append(f"Balik modal {h['payback_teks']} (terdiskonto {h['payback_diskonto_teks']}) dari masa proyek {p['tahun']} tahun.")
        if h["payback_diskonto_tahun"] is not None or h["nilai_sisa"] <= 0:
            pass
        elif status != "LAYAK":
            alasan.append(f"NPV positif juga bergantung pada nilai jual kembali di akhir ({rp(h['nilai_sisa'])}).")
        else:
            status = "KURANG LAYAK"
            alasan[:] = [f"NPV positif {rp(h['npv'])}, tetapi hanya berkat nilai jual kembali di akhir "
                         f"({rp(h['nilai_sisa'])}); setelah memperhitungkan nilai waktu uang, arus kas operasional "
                         f"belum balik modal dalam {p['tahun']} tahun."]
        if status != "LAYAK":
            alasan.append(f"IRR {irr_txt} dibanding diskonto {diskonto_txt}; balik modal {h['payback_teks']}.")
        if h["batas_penurunan_persen"] is not None:
            syarat.append(f"{h['batas_penurunan_dasar'].capitalize()} tidak turun lebih dari {pct(h['batas_penurunan_persen'], 1)} dari perkiraan.")
        if h["batas_kenaikan_biaya_persen"] is not None:
            syarat.append(f"Biaya tidak naik lebih dari {pct(h['batas_kenaikan_biaya_persen'], 1)}.")
        if p["mode"] == "omzet" and h.get("bep_ekonomi_omzet_per_bulan"):
            syarat.append(f"{lbl} minimal sekitar {rp(h['bep_ekonomi_omzet_per_bulan'])}/bulan (bila sama tiap tahun).")

    hasil = {
        "versi": VERSI,
        "mode": p["mode"],
        "input": {
            "investasi": bulat(p["investasi"]), "masa_proyek_tahun": p["tahun"],
            "diskonto_persen": float(p["diskonto"]), "sumber_diskonto": p["sumber_diskonto"],
            "pajak_persen": float(p["pajak"]), "dasar_pajak": p["dasar_pajak"] if p["pajak"] > 0 else None,
            "umur_ekonomis_tahun": p["umur"], "nilai_residu": bulat(p["residu"]),
            "sumber_nilai_sisa": p["sumber_nilai_sisa"],
            "jenis_manfaat": p["jenis"] if p["mode"] == "omzet" else None,
            "label_manfaat": lbl if p["mode"] == "omzet" else None,
            "biaya_variabel_persen_omzet": float((p["v"] * 100).quantize(Decimal("0.01"))) if p["mode"] == "omzet" else None,
        },
        "tabel_arus_kas": baris,
        "hasil": h,
        "sensitivitas": sens,
        "kesimpulan": {"status": status, "alasan": alasan, "syarat": syarat},
        "asumsi": asumsi,
        "catatan": catatan,
        "peringatan": peringatan,
        "disclaimer": DISCLAIMER,
    }
    hasil["ringkasan_untuk_agent"] = ringkasan(hasil)
    return hasil


def ringkasan(x):
    h, i, k = x["hasil"], x["input"], x["kesimpulan"]
    L = [LABEL_AGENT,
         f"Investasi {rp(i['investasi'])}, masa {i['masa_proyek_tahun']} tahun, diskonto {pct(i['diskonto_persen'], 1)} ({i['sumber_diskonto']}).",
         f"KESIMPULAN: {k['status']}"]
    L += ["  - " + s for s in k["alasan"]]
    L.append(f"NPV {rp(h['npv'])} (diskonto {pct(i['diskonto_persen'], 1)}) | IRR {'tidak ada' if h['irr_persen'] is None else pct(h['irr_persen'])} | PI {str(h['pi']).replace('.', ',')}")
    if h.get("npv_uji_ketat") is not None:
        L.append(f"NPV uji ketat (diskonto {pct(h['diskonto_uji_ketat_persen'], 1)}): {rp(h['npv_uji_ketat'])} -> "
                 f"{'tetap positif' if h['npv_uji_ketat'] >= 0 else 'negatif'}. Arti: bila hasil minimal yang diminta "
                 f"dinaikkan ke 20%/tahun (bunga lebih mahal atau risiko lebih besar), rencana "
                 f"{'masih menutup modal plus hasil itu' if h['npv_uji_ketat'] >= 0 else 'tidak lagi menutupnya'} (informasi, tidak mengubah kesimpulan).")
    L.append(f"Balik modal {h['payback_teks']} | terdiskonto {h['payback_diskonto_teks']}")
    if x["mode"] == "omzet":
        lbl = i["label_manfaat"]
        if h.get("bep_akuntansi_omzet_per_tahun") is not None:
            L.append(f"{lbl} impas (laba pembukuan = 0): {rp(h['bep_akuntansi_omzet_per_tahun'])}/tahun = {rp(h['bep_akuntansi_omzet_per_bulan'])}/bulan")
        if h.get("bep_ekonomi_omzet_per_tahun") is not None:
            L.append(f"{lbl} minimal agar layak (NPV = 0, sama tiap tahun): {rp(h['bep_ekonomi_omzet_per_tahun'])}/tahun = {rp(h['bep_ekonomi_omzet_per_bulan'])}/bulan")
    L.append("Arus kas per tahun (arus kas bersih | kumulatif):")
    for b in x["tabel_arus_kas"]:
        extra = f" (termasuk nilai sisa {rp(b['nilai_sisa'])})" if b["nilai_sisa"] else ""
        L.append(f"  Tahun {b['tahun']}: {rp(b['arus_kas_bersih'])}{extra} | {rp(b['kumulatif'])}")
    if x["sensitivitas"]:
        L.append("Sensitivitas (NPV | IRR):")
        for s in x["sensitivitas"]:
            L.append(f"  {s['skenario']}: {rp(s['npv'])} | {'tidak ada' if s['irr_persen'] is None else pct(s['irr_persen'])} -> {'tetap layak' if s['tetap_layak'] else 'NPV negatif'}")
    if k["syarat"]:
        L.append("Syarat/batas aman:")
        L += ["  - " + s for s in k["syarat"]]
    for judul, isi in (("Asumsi", x["asumsi"]), ("Catatan", x["catatan"]), ("Peringatan", x["peringatan"])):
        if isi:
            L.append(judul + ":")
            L += ["  - " + s for s in isi]
    L.append(x["disclaimer"])
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Kelayakan investasi usaha: payback, NPV, IRR, PI, BEP, sensitivitas.")
    ap.add_argument("--investasi", help="Investasi awal, mis. 45jt")
    ap.add_argument("--arus-kas", help="Arus kas bersih per tahun: satu angka (dipakai tiap tahun) atau '15jt;18jt;20jt'. Boleh '/bulan'.")
    ap.add_argument("--omzet", help="Omzet tambahan per tahun (atau '/bulan'), satu angka atau daftar per tahun")
    ap.add_argument("--biaya", help="Biaya tetap tunai per tahun (gaji, sewa, listrik, servis), boleh '/bulan'")
    ap.add_argument("--hpp-persen", help="Biaya variabel (bahan baku, kemasan, komisi) dalam %% omzet")
    ap.add_argument("--biaya-variabel", help="Biaya variabel tahun 1 dalam rupiah (diubah ke %% omzet)")
    ap.add_argument("--kenaikan-omzet", help="Kenaikan omzet per tahun dalam %% (default 0)")
    ap.add_argument("--kenaikan-biaya", help="Kenaikan biaya tetap per tahun dalam %% (default 0)")
    ap.add_argument("--tahun", type=int, help="Masa proyek (tahun). Default 5 untuk mode omzet")
    ap.add_argument("--diskonto", help="Tingkat diskonto %%/tahun (default 12)")
    ap.add_argument("--nilai-sisa", "--nilai-residu", dest="nilai_sisa",
                    help="Perkiraan harga jual kembali di akhir masa proyek (dua nama opsi ini sama persis). "
                         "Kosong = nilai buku garis lurus dengan nilai akhir Rp0")
    ap.add_argument("--umur-ekonomis", type=int, help="Umur ekonomis aset (tahun) untuk penyusutan garis lurus. Default = masa proyek")
    ap.add_argument("--pajak-persen", help="Pajak dalam %%: 0,5 (PPh final UMKM, dari omzet) atau 22 (PPh badan, dari laba)")
    ap.add_argument("--dasar-pajak", choices=["omzet", "laba"], default="omzet", help="Dasar pajak (default omzet)")
    ap.add_argument("--sensitivitas", nargs="?", const=SENS_DEFAULT, default=SENS_DEFAULT,
                    help="Skenario, default 'omzet-10;omzet-20;biaya+10'")
    ap.add_argument("--cari-minimal", action="store_true",
                    help="Belum ada data omzet/arus kas: hitung uang bersih minimal per bulan/tahun agar layak")
    ap.add_argument("--jenis", choices=["omzet", "penghematan", "pemasukan"], default="omzet",
                    help="Arti angka --omzet: omzet (default), penghematan (beli vs sewa/maklon), "
                         "atau pemasukan (pemasukan tambahan, mis. sewa alat)")
    ap.add_argument("--format", choices=["json", "teks"], default="json")
    a = ap.parse_args(argv)
    try:
        hasil = jalankan(a)
    except Galat as e:
        print(json.dumps({"error": e.pesan, "saran": e.saran}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    if a.format == "teks":
        print(hasil["ringkasan_untuk_agent"])
    else:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
