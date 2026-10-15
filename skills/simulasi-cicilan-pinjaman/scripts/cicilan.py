#!/usr/bin/env python3
"""Simulasi cicilan pinjaman: flat vs efektif/anuitas, bunga efektif setara (termasuk biaya),
jadwal angsuran, pinjaman harian (pinjol), denda, dan cicilan maksimal aman.

Hanya Python standar (3.8+), tanpa jaringan. Windows: `python` atau `py`.

Definisi (ditulis ulang dari konvensi numpy-financial, BSD-3-Clause; lihat ATTRIBUTION.md):
  pmt(r, n, pv)  = -(pv*(1+r)^n) * r / ((1+r)^n - 1)          r = 0 -> -pv/n
  rate(n, pmt, pv) = r yang membuat pv*(1+r)^n + pmt*((1+r)^n - 1)/r = 0  (dicari dengan bisection)
Rumus lain:
  Flat     : bunga/bulan = pokok x bunga_bulanan ; pokok/bulan = pokok / n
  Anuitas  : cicilan = pokok x r / (1 - (1+r)^-n) ; bunga bulan k = sisa x r ; pokok = cicilan - bunga
  Bunga efektif setara (EIR) : i bulanan yang membuat
      uang_diterima_bersih = sum( pembayaran_k / (1+i)^k ),  k = 1..n
      uang_diterima_bersih = pokok - biaya di muka ; pembayaran_k = cicilan_k + biaya bulanan
      Ditampilkan sebagai i x 12 (per tahun, cara bank menyebut bunga efektif)
      dan (1+i)^12 - 1 (per tahun majemuk).
  Pinjaman harian (tenor dalam hari, dibayar sekali di akhir):
      bunga = pokok x bunga_harian x hari ; biaya per tahun = (kembali/diterima - 1) x 365/hari
      Pembanding batas OJK (cara hitung SEOJK No. 19/SEOJK.06/2025 Romawi XIV angka 3):
      manfaat ekonomi per hari = (bunga + biaya) / nilai pinjaman di perjanjian / hari
Pembulatan: rupiah ke terdekat (0,5 ke atas) per baris; selisih pembulatan ditaruh di cicilan
terakhir agar total pokok tepat sama dengan pinjaman, dan selisihnya ditampilkan.
"""
import argparse
import json
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

getcontext().prec = 50
D = Decimal
NOL, SATU, SERATUS = D(0), D(1), D(100)

# Batas maksimum manfaat ekonomi pinjaman daring (LPBBTI) menurut SEOJK No. 19/SEOJK.06/2025
# Romawi XIV angka 2-3 (ditetapkan dan berlaku 31 Juli 2025; mencabut SEOJK No. 19/SEOJK.06/2023).
# Persen per hari kalender dari nilai pendanaan yang tercantum dalam perjanjian. Manfaat ekonomi =
# bunga/margin + biaya administrasi/komisi/fee platform + biaya lain, selain denda keterlambatan,
# biaya tanda tangan elektronik bersertifikat, dan pajak. OJK dapat mengevaluasi batas ini secara
# berkala (Romawi XIV angka 7) - hanya untuk peringatan; selalu minta pengguna cek aturan OJK terbaru.
BATAS_PINJOL_HARIAN = {
    "konsumtif": {"sd_6_bulan": D("0.3"), "di_atas_6_bulan": D("0.2")},
    "produktif_sd_50jt": {"sd_6_bulan": D("0.275"), "di_atas_6_bulan": D("0.1")},
    "produktif_di_atas_50jt": {"sd_6_bulan": D("0.1"), "di_atas_6_bulan": D("0.1")},
}
NILAI_PRODUKTIF_KECIL = D(50_000_000)  # produktif: nilai pendanaan paling tinggi Rp50.000.000
# Asumsi: "tenor sampai dengan 6 bulan" = sampai 180 hari (1 bulan = 30 hari, seperti simulasi di SEOJK
# yang sama: tenor 5 bulan = 150 hari, 7 bulan = 210 hari). Tenor 181-184 hari diberi catatan asumsi.
TENOR_6_BULAN_HARI = 180
TENOR_6_BULAN_KALENDER_MAKS_HARI = 184
RUJUKAN_PINJOL = ("SEOJK No. 19/SEOJK.06/2025 Romawi XIV angka 3, berlaku sejak 31 Juli 2025 "
                  "(SEOJK No. 19/SEOJK.06/2023 sudah dicabut): konsumtif 0,3%/hari untuk tenor sampai 6 bulan "
                  "dan 0,2%/hari untuk tenor di atas 6 bulan; produktif dengan nilai pinjaman paling tinggi "
                  "Rp50 juta 0,275%/hari (tenor sampai 6 bulan) dan 0,1%/hari (tenor di atas 6 bulan); produktif "
                  "di atas Rp50 juta 0,1%/hari; dihitung per hari kalender dari nilai pinjaman di perjanjian "
                  "- cek aturan OJK terbaru di ojk.go.id")
RUJUKAN_PINJOL_SINGKAT = "SEOJK No. 19/SEOJK.06/2025 Romawi XIV angka 3, berlaku sejak 31 Juli 2025"


def batas_pinjol(jenis, nilai, hari):
    """Batas manfaat ekonomi (persen per hari) + keterangan golongan, menurut BATAS_PINJOL_HARIAN."""
    pendek = hari <= TENOR_6_BULAN_HARI
    kunci_tenor = "sd_6_bulan" if pendek else "di_atas_6_bulan"
    teks_tenor = "tenor sampai 6 bulan" if pendek else "tenor di atas 6 bulan"
    if jenis == "konsumtif":
        return BATAS_PINJOL_HARIAN["konsumtif"][kunci_tenor], f"konsumtif, {teks_tenor}"
    if nilai <= NILAI_PRODUKTIF_KECIL:
        return (BATAS_PINJOL_HARIAN["produktif_sd_50jt"][kunci_tenor],
                f"produktif dengan nilai pinjaman paling tinggi Rp50 juta, {teks_tenor}")
    return (BATAS_PINJOL_HARIAN["produktif_di_atas_50jt"][kunci_tenor],
            "produktif dengan nilai pinjaman di atas Rp50 juta, semua tenor")


# Bunga ilustrasi bila bunga belum diketahui (bunga ilustrasi, bukan acuan pasar dan bukan data lembaga tertentu).
ILUSTRASI = {
    "hp": ("kredit HP/elektronik lewat pembiayaan atau paylater, dihitung flat",
           "1,5%/bulan flat;2%/bulan flat;3%/bulan flat"),
    "motor": ("kredit motor, dihitung flat", "0,8%/bulan flat;1,2%/bulan flat;1,5%/bulan flat"),
    "kpr": ("KPR, efektif/anuitas", "5%/tahun efektif;8%/tahun efektif;12%/tahun efektif"),
}

PENGALI = {"rb": 10**3, "ribu": 10**3, "k": 10**3, "jt": 10**6, "juta": 10**6,
           "m": 10**9, "miliar": 10**9, "milyar": 10**9, "t": 10**12, "triliun": 10**12}


class Galat(Exception):
    def __init__(self, pesan, saran=""):
        super().__init__(pesan)
        self.pesan, self.saran = pesan, saran


# ------------------------------------------------------------------ pembacaan angka
def bulat(x):
    return D(x).quantize(SATU, rounding=ROUND_HALF_UP)


def periode_dari(s):
    s = s.lower()
    if re.search(r"(/|per\s*|se)\s*(hari|hr)\b|harian", s):
        return "hari"
    if re.search(r"(/|per\s*|se)\s*(bln|bulan|bl)\b|bulanan", s):
        return "bulan"
    if re.search(r"(/|per\s*|se)\s*(thn|tahun|th)\b|tahunan|p\.?a\.?\b", s):
        return "tahun"
    return None


def _angka(num, suf, asli, nama):
    num = num.strip(".,")
    if "," in num and "." in num:
        if len(re.split(r"[.,]", num)[-1]) == 3:
            raise Galat(f"{nama}: '{asli}' ambigu (titik dan koma bercampur)", "Tulis 10.000.000 atau 10jt.")
        num = num.replace(".", "").replace(",", ".") if num.rfind(",") > num.rfind(".") else num.replace(",", "")
    elif "," in num:
        b = num.split(",")
        if len(b) > 2:
            num = num.replace(",", "")
        elif len(b[1]) == 3 and not suf:
            raise Galat(f"{nama}: '{asli}' ambigu (koma bisa ribuan atau desimal)",
                        "Tulis 25.000.000 atau 25jt.")
        else:
            num = num.replace(",", ".")
    elif "." in num:
        b = num.split(".")
        if len(b) > 2 or len(b[1]) == 3:
            num = num.replace(".", "")
    try:
        return D(num) * D(PENGALI[suf] if suf else 1)
    except InvalidOperation:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca", "Contoh: 25jt, 1,5jt, 750rb, 25.000.000")


def parse_rupiah(teks, nama, boleh_persen=False):
    """'Rp25.000.000' | '25jt' | '1,5 juta' | '750rb' -> Decimal. Bila boleh_persen: '20%' -> ('%', 20)."""
    if teks is None:
        return None
    asli = str(teks)
    s = asli.strip().lower()
    s = re.sub(r"(/|per\s*|se)\s*(bln|bulan|thn|tahun|th|hari)\b", "", s)
    s = re.sub(r"^\s*(rp|idr)\.?\s*", "", s).replace(" ", "")
    if boleh_persen and s.endswith("%"):
        return ("%", _angka(s[:-1], None, asli, nama))
    if s.startswith("-") or s.startswith("minus"):
        raise Galat(f"{nama}: tidak boleh negatif ('{asli}')", "Tulis angka positif.")
    m = re.fullmatch(r"([0-9][0-9.,]*)(rb|ribu|k|jt|juta|m|miliar|milyar|t|triliun)?", s)
    if not m:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca", "Contoh: 25jt, 1,5jt, 750rb, 25.000.000")
    return _angka(m.group(1), m.group(2), asli, nama)


def parse_persen(teks, nama):
    """'0,8%/bulan' | '9,6% per tahun' | '0,3% per hari' | '12' -> (Decimal persen, periode|None)."""
    if teks is None:
        return None, None
    s = str(teks).strip().lower()
    per = periode_dari(s)
    s = re.sub(r"(/|per\s*|se)\s*(hari|hr|bln|bulan|bl|thn|tahun|th)\b", "", s)
    s = re.sub(r"harian|bulanan|tahunan|p\.?a\.?|persen|%|flat|efektif|anuitas", "", s).strip().replace(" ", "")
    s = s.replace(",", ".")
    try:
        v = D(s)
    except InvalidOperation:
        raise Galat(f"{nama}: '{teks}' tidak terbaca", "Contoh: 0,8%/bulan, 9,6%/tahun, 0,3%/hari")
    if v < 0:
        raise Galat(f"{nama}: tidak boleh negatif", "Tulis 0 bila tanpa bunga.")
    return v, per


def parse_tenor(teks):
    """'36' | '36 bulan' | '3 tahun' | '3th' | '14 hari' -> (jumlah, satuan 'bulan'|'hari')."""
    s = str(teks).strip().lower().replace(" ", "")
    m = re.fullmatch(r"([0-9]+(?:[.,][0-9]+)?)(bulan|bln|bl|b|tahun|thn|th|t|hari|hr|h|minggu|mg)?", s)
    if not m:
        raise Galat(f"tenor '{teks}' tidak terbaca", "Contoh: 36 (bulan), 3th, 14hari")
    v = D(m.group(1).replace(",", "."))
    sat = m.group(2) or "bulan"
    if sat in ("tahun", "thn", "th", "t"):
        v, sat = v * 12, "bulan"
    elif sat in ("minggu", "mg"):
        v, sat = v * 7, "hari"
    elif sat in ("hari", "hr", "h"):
        sat = "hari"
    else:
        sat = "bulan"
    if v != v.to_integral_value() or v <= 0:
        raise Galat(f"tenor '{teks}' harus bilangan bulat > 0", "Contoh: 36 bulan atau 3 tahun.")
    n = int(v)
    if sat == "bulan" and n > 480:
        raise Galat("tenor lebih dari 40 tahun", "Periksa lagi tenornya (dalam bulan atau tahun?).")
    if sat == "hari" and n > 3650:
        raise Galat("tenor harian terlalu panjang", "Untuk tenor lebih dari setahun, tulis dalam bulan.")
    return n, sat


# ------------------------------------------------------------------ fungsi keuangan dasar
def pmt(rate, nper, pv, fv=0):
    """Konvensi numpy-financial (akhir periode): hasil negatif untuk pv positif."""
    r, n, pv, fv = D(str(rate)), int(nper), D(str(pv)), D(str(fv))
    if r == 0:
        return -(pv + fv) / n
    f = (SATU + r) ** n
    return -(pv * f + fv) * r / (f - SATU)


def pv_anuitas(rate, nper, cicilan):
    r = D(str(rate))
    if r == 0:
        return D(str(cicilan)) * nper
    return D(str(cicilan)) * (SATU - (SATU + r) ** (-nper)) / r


def _cari_akar(f, lo, hi, iterasi=300):
    flo = f(lo)
    if flo == 0:
        return lo
    fhi = f(hi)
    if (flo > 0) == (fhi > 0):
        return None
    for _ in range(iterasi):
        mid = (lo + hi) / 2
        fm = f(mid)
        if fm == 0 or (hi - lo) < D("1e-30"):
            return mid
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def rate(nper, pmt_, pv, fv=0):
    """Bunga per periode (bisection) agar pv*(1+r)^n + pmt*((1+r)^n-1)/r + fv = 0."""
    n, p, v, f = int(nper), D(str(pmt_)), D(str(pv)), D(str(fv))

    def g(r):
        if r == 0:
            return v + p * n + f
        q = (SATU + r) ** n
        return v * q + p * (q - SATU) / r + f
    return _cari_akar(g, D("-0.99"), D("10"))


def irr_periode(arus):
    """i per periode agar sum(arus_t / (1+i)^t) = 0. arus[0] = uang diterima (positif)."""
    arus = [D(str(a)) for a in arus]

    def g(i):
        return sum(a / (SATU + i) ** t for t, a in enumerate(arus))
    return _cari_akar(g, D("-0.99"), D("10"))


# ------------------------------------------------------------------ jadwal
def jadwal_flat(pokok, r_bulan, n):
    bunga = bulat(pokok * r_bulan)
    pk = bulat(pokok / n)
    rows, sisa = [], pokok
    for k in range(1, n + 1):
        p = sisa if k == n else pk
        sisa -= p
        rows.append({"bulan": k, "cicilan": p + bunga, "pokok": p, "bunga": bunga, "sisa": sisa})
    return rows


def jadwal_anuitas(pokok, tahap, cicilan_tetap=None):
    """tahap = [(r_bulan, jumlah_bulan), ...]. Cicilan dihitung ulang di awal tiap tahap dari sisa pokok."""
    n_total = sum(b for _, b in tahap)
    rows, sisa, k = [], pokok, 0
    for r, b in tahap:
        sisa_bulan = n_total - k
        cic = cicilan_tetap if cicilan_tetap is not None else bulat(-pmt(r, sisa_bulan, sisa))
        for _ in range(b):
            k += 1
            bunga = bulat(sisa * r)
            p = cic - bunga
            if k == n_total or p > sisa:
                p = sisa
            if p < 0:
                raise Galat("cicilan lebih kecil dari bunga bulanan (pinjaman tidak pernah lunas)",
                            "Periksa angka cicilan, bunga, atau pokok.")
            sisa -= p
            rows.append({"bulan": k, "cicilan": p + bunga, "pokok": p, "bunga": bunga, "sisa": sisa})
    return rows


def cicilan_tahap(rows, tahap):
    out, k = [], 0
    for r, b in tahap:
        out.append({"bulan": f"{k + 1}-{k + b}", "bunga_per_tahun_persen": r * 12 * SERATUS, "cicilan": rows[k]["cicilan"]})
        k += b
    return out


def ringkas_tahunan(rows, tahap=None):
    mulai = {}
    if tahap and len(tahap) > 1:
        k = 0
        for r, b in tahap:
            if k > 0:
                mulai[k + 1] = (r, rows[k]["cicilan"])
            k += b
    out = []
    for awal in range(0, len(rows), 12):
        blok = rows[awal:awal + 12]
        cat = [f"mulai bulan ke-{bln}: bunga {pct(r * 12 * SERATUS)}/tahun, cicilan {rp(c)}"
               for bln, (r, c) in mulai.items() if blok[0]["bulan"] <= bln <= blok[-1]["bulan"]]
        out.append({"catatan": "; ".join(cat) or None, "tahun": awal // 12 + 1, "bulan": f"{blok[0]['bulan']}-{blok[-1]['bulan']}",
                    "cicilan_per_bulan": sorted({r["cicilan"] for r in blok}),
                    "pokok_dibayar": sum(r["pokok"] for r in blok),
                    "bunga_dibayar": sum(r["bunga"] for r in blok), "sisa_akhir": blok[-1]["sisa"]})
    return out


def eir(diterima, rows, biaya_bulanan=NOL):
    arus = [diterima] + [-(r["cicilan"] + biaya_bulanan) for r in rows]
    i = irr_periode(arus)
    if i is None:
        return None
    return {"bulanan_persen": i * SERATUS, "per_tahun_persen": i * 12 * SERATUS,
            "per_tahun_majemuk_persen": ((SATU + i) ** 12 - SATU) * SERATUS}


# ------------------------------------------------------------------ format
def rp(x):
    x = bulat(x)
    s = f"{abs(int(x)):,}".replace(",", ".")
    return ("-Rp" if x < 0 else "Rp") + s


def pct(x, d=2):
    if x is None:
        return "-"
    q = D(x).quantize(D(1).scaleb(-d), rounding=ROUND_HALF_UP)
    return f"{q}".replace(".", ",") + "%"


def jsonable(o):
    if isinstance(o, Decimal):
        return int(o) if o == o.to_integral_value() else round(float(o), 6)
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    return o


# ------------------------------------------------------------------ inti
def hitung(a):
    asumsi, peringatan = [], []
    # --- pokok
    harga = parse_rupiah(a.harga, "harga") if a.harga else None
    if a.pokok:
        pokok = parse_rupiah(a.pokok, "pokok pinjaman")
        dp = NOL
    elif harga is not None:
        dpv = parse_rupiah(a.dp, "DP", boleh_persen=True) if a.dp else NOL
        if isinstance(dpv, tuple):
            if dpv[1] >= 100:
                raise Galat("DP 100% atau lebih: tidak ada yang perlu dicicil", "Periksa persen DP.")
            dp = bulat(harga * dpv[1] / SERATUS)
            asumsi.append(f"DP {pct(dpv[1], 1)} dari harga {rp(harga)} = {rp(dp)}.")
        else:
            dp = dpv
        pokok = harga - dp
        if not a.dp:
            asumsi.append("DP tidak disebut, dianggap Rp0.")
    else:
        if a.penghasilan:
            pokok = None
            dp = NOL
        else:
            raise Galat("pokok pinjaman atau harga belum diisi", "Isi --pokok 20jt atau --harga 25jt --dp 5jt.")
    if pokok is not None and pokok <= 0:
        raise Galat("pokok pinjaman harus lebih dari 0 (DP sama dengan/lebih besar dari harga?)",
                    "Periksa harga dan DP.")

    hasil = {"input_terbaca": {}, "asumsi": asumsi, "peringatan": peringatan}
    kemampuan = None
    if a.penghasilan:
        kemampuan = hitung_kemampuan(a)
        hasil["kemampuan_bayar"] = kemampuan

    if pokok is None:
        if kemampuan is None:
            raise Galat("data belum cukup", "Isi pokok/harga, tenor, dan bunga atau cicilan.")
        hasil["mode"] = "kemampuan_saja"
        return hasil

    if not a.tenor:
        raise Galat("tenor belum diisi", "Contoh: --tenor 36 (bulan) atau --tenor 3th atau --tenor 14hari.")
    n, satuan = parse_tenor(a.tenor)

    # --- biaya
    def biaya(teks, nama):
        if not teks:
            return NOL
        v = parse_rupiah(teks, nama, boleh_persen=True)
        if isinstance(v, tuple):
            return bulat(pokok * v[1] / SERATUS)
        return v
    b_admin = biaya(a.admin, "biaya admin")
    b_provisi = biaya(a.provisi, "provisi")
    b_asuransi = biaya(a.asuransi, "asuransi")
    b_lain = biaya(a.biaya_lain, "biaya lain")
    biaya_muka = b_admin + b_provisi + b_asuransi + b_lain
    biaya_bulanan = parse_rupiah(a.biaya_bulanan, "biaya bulanan") if a.biaya_bulanan else NOL
    if biaya_muka >= pokok:
        raise Galat("biaya di muka sama dengan/lebih besar dari pinjaman", "Periksa biaya admin/provisi/asuransi.")
    cara = a.cara_biaya
    pokok_dicicil = pokok + biaya_muka if cara == "masuk-pinjaman" else pokok
    diterima = pokok - biaya_muka if cara in ("potong", "tunai") else pokok
    hasil["input_terbaca"] = {"harga": harga, "dp": dp, "pokok_pinjaman": pokok, "tenor": n, "satuan_tenor": satuan,
                              "biaya_di_muka": {"admin": b_admin, "provisi": b_provisi, "asuransi": b_asuransi,
                                                "lain": b_lain, "total": biaya_muka, "cara": cara},
                              "biaya_bulanan": biaya_bulanan, "pokok_yang_dicicil": pokok_dicicil}
    if biaya_muka > 0:
        teks_cara = {"potong": "dipotong dari uang yang cair", "tunai": "dibayar tunai di muka",
                     "masuk-pinjaman": "ditambahkan ke pinjaman (ikut dicicil dan berbunga)"}[cara]
        asumsi.append(f"Biaya di muka {rp(biaya_muka)} {teks_cara}.")

    if satuan == "hari":
        hasil.update(hitung_harian(a, pokok_dicicil, diterima, n, asumsi, peringatan))
        hasil["mode"] = "harian"
        tambah_denda(a, hasil, hasil["ringkasan"]["total_kembali"], asumsi)
        return hasil

    # --- bunga bulanan
    jenis = a.jenis
    tahap = None
    cicilan_input = parse_rupiah(a.cicilan, "cicilan") if a.cicilan else None
    if a.bunga_tahap:
        if jenis == "flat":
            raise Galat("bunga bertahap hanya untuk bunga efektif/anuitas (mis. KPR fixed lalu floating)",
                        "Hapus --jenis flat atau --bunga-tahap.")
        jenis = "efektif"
        tahap, terpakai = [], 0
        bagian = [x.strip() for x in a.bunga_tahap.split(";") if x.strip()]
        for idx, bg in enumerate(bagian):
            m = re.fullmatch(r"(.+?)\s*[x×@]\s*([0-9]+)\s*(bulan|bln|th|tahun|thn)?", bg)
            if m:
                bp, per = parse_persen(m.group(1), "bunga tahap")
                bln = int(m.group(2)) * (12 if m.group(3) in ("th", "tahun", "thn") else 1)
            elif idx == len(bagian) - 1:
                bp, per = parse_persen(bg, "bunga tahap")
                bln = n - terpakai
            else:
                raise Galat(f"tahap bunga '{bg}' tidak terbaca", "Contoh: \"5%x36;11%\" (5% 36 bulan, lalu 11% sisanya)")
            if bln <= 0:
                raise Galat("jumlah bulan tahap bunga melebihi tenor", "Periksa tenor dan lama masa fixed.")
            r = bp / SERATUS / (1 if per == "bulan" else 12)
            tahap.append((r, bln))
            terpakai += bln
        if terpakai != n:
            raise Galat(f"jumlah bulan tahap bunga ({terpakai}) tidak sama dengan tenor ({n})",
                        "Tahap terakhir boleh tanpa jumlah bulan, mis. \"5%x36;11%\".")
        r_bulan = tahap[0][0]
        asumsi.append("Bunga efektif setara pada bunga bertahap = rata-rata sepanjang tenor.")
        asumsi.append("Bunga bertahap: " + "; ".join(f"{pct(r * 12 * SERATUS)}/tahun selama {b} bulan" for r, b in tahap)
                      + ". Cicilan dihitung ulang di awal tiap tahap dari sisa pokok. Bunga tahap berikutnya "
                        "(floating) hanyalah perkiraan; angka sebenarnya ditentukan bank saat itu.")
    elif a.bunga is not None:
        bp, per = parse_persen(a.bunga, "bunga")
        if per == "hari":
            r_bulan = bp / SERATUS * 30
            asumsi.append(f"Bunga {pct(bp, 3)} per hari dihitung 30 hari per bulan = {pct(bp * 30)} per bulan.")
        elif per == "bulan":
            r_bulan = bp / SERATUS
        else:
            if per is None:
                asumsi.append(f"Bunga {pct(bp)} dianggap per tahun (tidak disebut per bulan/per tahun).")
            r_bulan = bp / SERATUS / 12
    elif cicilan_input is not None:
        r_bulan = None
    else:
        raise Galat("bunga atau cicilan per bulan belum diisi",
                    "Isi --bunga 0,8%/bulan --jenis flat, atau --cicilan 1,2jt bila hanya tahu cicilannya.")

    if jenis is None and r_bulan is not None:
        jenis = "efektif"
        asumsi.append("Jenis bunga tidak disebut, dianggap efektif/anuitas (cicilan tetap). Bila ternyata flat, "
                      "cicilan lebih besar - lihat perbandingan.")

    # --- jadwal utama
    if r_bulan is None:
        # Hanya tahu cicilan: cari bunga efektif per bulan (bisection)
        r_bulan = rate(n, -cicilan_input, pokok_dicicil)
        if r_bulan is None:
            raise Galat("cicilan x tenor tidak masuk akal terhadap pokok", "Periksa angka cicilan, tenor, dan pokok.")
        if cicilan_input * n < pokok_dicicil:
            raise Galat("total cicilan lebih kecil dari pokok (tidak mungkin)", "Periksa angka cicilan dan tenor.")
        jenis = "dari_cicilan"
        rows = jadwal_anuitas(pokok_dicicil, [(r_bulan, n)], cicilan_tetap=cicilan_input)
        asumsi.append("Bunga tidak disebut: dihitung balik dari cicilan, tenor, dan pokok (cicilan sama tiap bulan).")
    elif jenis == "flat":
        rows = jadwal_flat(pokok_dicicil, r_bulan, n)
    else:
        rows = jadwal_anuitas(pokok_dicicil, tahap or [(r_bulan, n)])

    total_cicilan = sum(r["cicilan"] for r in rows)
    total_bunga = sum(r["bunga"] for r in rows)
    cicilan_normal = rows[0]["cicilan"]
    selisih_akhir = rows[-1]["cicilan"] - (rows[-2]["cicilan"] if len(rows) > 1 else rows[-1]["cicilan"])
    total_biaya_bulanan = biaya_bulanan * n
    total_dibayar = total_cicilan + total_biaya_bulanan + (biaya_muka if cara == "tunai" else NOL)
    biaya_total_pinjaman = total_cicilan + total_biaya_bulanan - diterima
    e = eir(diterima, rows, biaya_bulanan)
    e_tanpa_biaya = eir(pokok_dicicil, rows)

    ringkasan = {
        "jenis_bunga": jenis,
        "bunga_bulanan_persen": r_bulan * SERATUS,
        "bunga_tahunan_tertulis_persen": r_bulan * 12 * SERATUS,
        "cicilan_per_bulan": cicilan_normal,
        "cicilan_terakhir": rows[-1]["cicilan"],
        "selisih_pembulatan_cicilan_terakhir": selisih_akhir if not tahap else None,
        "cicilan_per_tahap": cicilan_tahap(rows, tahap) if tahap else None,
        "biaya_bulanan": biaya_bulanan,
        "dibayar_per_bulan": cicilan_normal + biaya_bulanan,
        "total_cicilan": total_cicilan,
        "total_bunga": total_bunga,
        "biaya_di_muka": biaya_muka,
        "uang_diterima_bersih": diterima,
        "total_biaya_pinjaman": biaya_total_pinjaman,
        "total_dibayar_dari_kantong": total_dibayar,
        "bunga_efektif_setara_tanpa_biaya": e_tanpa_biaya,
        "bunga_efektif_setara_dengan_biaya": e,
    }
    if harga is not None:
        kepemilikan = dp + total_dibayar
        ringkasan["total_harga_kredit"] = kepemilikan
        ringkasan["lebih_mahal_dari_tunai"] = kepemilikan - harga
        ringkasan["lebih_mahal_dari_tunai_persen"] = (kepemilikan - harga) / harga * SERATUS
    hasil["ringkasan"] = ringkasan
    hasil["mode"] = "bulanan"

    # --- perbandingan flat vs anuitas pada angka yang sama
    if not tahap:
        f_rows = jadwal_flat(pokok_dicicil, r_bulan, n)
        a_rows = jadwal_anuitas(pokok_dicicil, [(r_bulan, n)])
        f_tot = sum(r["bunga"] for r in f_rows)
        a_tot = sum(r["bunga"] for r in a_rows)
        flat_setara = (total_cicilan - pokok_dicicil) / (pokok_dicicil * n) * SERATUS
        hasil["perbandingan"] = {
            "angka_bunga_per_tahun_persen": r_bulan * 12 * SERATUS,
            "flat": {"cicilan": f_rows[0]["cicilan"], "total_bunga": f_tot,
                     "bunga_efektif_setara_per_tahun_persen": eir(pokok_dicicil, f_rows)["per_tahun_persen"]},
            "anuitas": {"cicilan": a_rows[0]["cicilan"], "total_bunga": a_tot,
                        "bunga_efektif_setara_per_tahun_persen": r_bulan * 12 * SERATUS},
            "selisih_total_bunga_flat_minus_anuitas": f_tot - a_tot,
            "bunga_flat_setara_dari_cicilan_ini": {"per_bulan_persen": flat_setara, "per_tahun_persen": flat_setara * 12},
        }

    if a.jadwal_lengkap or n <= 12:
        hasil["jadwal"] = rows
    else:
        hasil["jadwal_awal"] = rows[:3]
        hasil["jadwal_akhir"] = rows[-2:]
        hasil["jadwal_per_tahun"] = ringkas_tahunan(rows, tahap)

    # --- peringatan (netral)
    if jenis == "flat" and e_tanpa_biaya:
        peringatan.append(f"Bunga flat {pct(r_bulan * SERATUS)}/bulan ({pct(r_bulan * 12 * SERATUS)}/tahun) setara bunga "
                          f"efektif ±{pct(e_tanpa_biaya['per_tahun_persen'], 1)}/tahun, karena bunga dihitung dari "
                          f"pokok awal walau utang sudah berkurang.")
    if biaya_muka > 0 and e and e_tanpa_biaya:
        naik = e["per_tahun_persen"] - e_tanpa_biaya["per_tahun_persen"]
        peringatan.append(f"Biaya di muka {rp(biaya_muka)} menaikkan bunga efektif setara dari "
                          f"{pct(e_tanpa_biaya['per_tahun_persen'], 1)} menjadi {pct(e['per_tahun_persen'], 1)}/tahun "
                          f"(+{pct(naik, 1)}).")
    if cara == "potong" and biaya_muka > 0:
        peringatan.append(f"Uang yang benar-benar diterima {rp(diterima)}, bukan {rp(pokok)}, tetapi cicilan dihitung dari "
                          f"{rp(pokok_dicicil)}.")
    if cara == "masuk-pinjaman" and biaya_muka > 0:
        peringatan.append(f"Biaya {rp(biaya_muka)} ikut dicicil sehingga ikut berbunga.")
    if biaya_bulanan > 0:
        peringatan.append(f"Ada biaya bulanan {rp(biaya_bulanan)} di luar cicilan; total yang keluar per bulan "
                          f"{rp(cicilan_normal + biaya_bulanan)}.")
    if tahap and len(tahap) > 1:
        peringatan.append("Cicilan berubah saat bunga tahap berikutnya berlaku: "
                          + " -> ".join(rp(t["cicilan"]) for t in cicilan_tahap(rows, tahap)) + " per bulan.")
    if jenis == "dari_cicilan" and e_tanpa_biaya:
        fs = hasil["perbandingan"]["bunga_flat_setara_dari_cicilan_ini"]
        peringatan.append(f"Dari cicilan {rp(cicilan_input)} x {n} bulan: bunga efektif ±{pct(e_tanpa_biaya['per_tahun_persen'], 1)}"
                          f"/tahun, atau bila ditulis cara flat ±{pct(fs['per_bulan_persen'])}/bulan.")

    tambah_denda(a, hasil, cicilan_normal, asumsi)

    if kemampuan:
        dibayar = cicilan_normal + biaya_bulanan
        lain = kemampuan["cicilan_lain"]
        rasio = (dibayar + lain) / kemampuan["penghasilan_bersih"] * SERATUS
        status = "AMAN" if rasio <= kemampuan["batas_persen"] else ("WASPADA" if rasio <= kemampuan["batas_atas_persen"] else "BERAT")
        kemampuan["cicilan_ini_per_bulan"] = dibayar
        kemampuan["rasio_semua_cicilan_persen"] = rasio
        kemampuan["status"] = status
        cm = kemampuan["cicilan_maksimal_aman"]
        if cm > 0 and not tahap:
            per_bulan_cm = cm - biaya_bulanan
            if per_bulan_cm > 0:
                if jenis == "flat":
                    pk_maks = per_bulan_cm / (SATU / n + r_bulan)
                else:
                    pk_maks = pv_anuitas(r_bulan, n, per_bulan_cm)
                kemampuan["pinjaman_maksimal_aman_dengan_bunga_tenor_ini"] = bulat(pk_maks)
    return hasil


def hitung_kemampuan(a):
    gaji = parse_rupiah(a.penghasilan, "penghasilan bersih")
    if gaji <= 0:
        raise Galat("penghasilan bersih harus lebih dari 0", "Contoh: --penghasilan 6jt")
    lain = parse_rupiah(a.cicilan_lain, "cicilan lain") if a.cicilan_lain else NOL
    batas = D(str(a.batas).replace(",", "."))
    batas_atas = D(str(a.batas_atas).replace(",", "."))
    if not (0 < batas <= batas_atas < 100):
        raise Galat("batas rasio cicilan tidak masuk akal", "Contoh: --batas 30 --batas-atas 35")
    return {"penghasilan_bersih": gaji, "cicilan_lain": lain, "batas_persen": batas, "batas_atas_persen": batas_atas,
            "cicilan_maksimal_aman": max(NOL, bulat(gaji * batas / SERATUS) - lain),
            "cicilan_maksimal_batas_atas": max(NOL, bulat(gaji * batas_atas / SERATUS) - lain),
            "catatan": f"Patokan hati-hati (bukan aturan resmi): semua cicilan maks. {pct(batas, 0)}-{pct(batas_atas, 0)} dari penghasilan bersih "
                       f"(asumsi; bisa disesuaikan dengan kebutuhan rumah tangga)."}


def hitung_harian(a, pokok, diterima, hari, asumsi, peringatan):
    if a.bunga is None:
        raise Galat("bunga per hari belum diisi untuk pinjaman harian", "Contoh: --bunga 0,3%/hari")
    bp, per = parse_persen(a.bunga, "bunga")
    if per == "bulan":
        bp_h = bp / 30
        asumsi.append(f"Bunga {pct(bp)} per bulan dihitung per hari = /30.")
    elif per == "tahun":
        bp_h = bp / 365
        asumsi.append(f"Bunga {pct(bp)} per tahun dihitung per hari = /365.")
    else:
        bp_h = bp
        if per is None:
            asumsi.append("Bunga dianggap per hari (tenor dalam hari).")
    bunga = bulat(pokok * bp_h / SERATUS * hari)
    kembali = pokok + bunga
    biaya = kembali - diterima
    per_hari = biaya / diterima / hari * SERATUS
    tahun_sederhana = biaya / diterima * D(365) / hari * SERATUS
    majemuk = ((kembali / diterima) ** (D(365) / hari) - SATU) * SERATUS
    asumsi.append("Dibayar sekali di akhir tenor (bunga sederhana per hari).")
    ring = {"bunga_per_hari_persen": bp_h, "bunga_total": bunga, "total_kembali": kembali,
            "uang_diterima_bersih": diterima, "total_biaya_pinjaman": biaya,
            "biaya_total_per_hari_persen": per_hari, "setara_per_bulan_persen": per_hari * 30,
            "setara_per_tahun_persen": tahun_sederhana, "setara_per_tahun_majemuk_persen": majemuk}
    # Pembanding batas OJK: (bunga + biaya) per hari dari nilai pinjaman di perjanjian (bukan dari uang diterima).
    me_per_hari = biaya / pokok / hari * SERATUS
    jenis_pinjol = a.jenis_pinjol or "konsumtif"
    if not a.jenis_pinjol:
        asumsi.append("Jenis pinjaman daring dianggap konsumtif; bila untuk modal usaha (produktif), batas OJK-nya berbeda.")
    batas, golongan = batas_pinjol(jenis_pinjol, pokok, hari)
    ring["manfaat_ekonomi_per_hari_persen"] = me_per_hari
    ring["batas_tercatat_per_hari_persen"] = batas
    ring["golongan_batas"] = golongan
    ring["rujukan_batas"] = RUJUKAN_PINJOL
    asumsi.append(f"Batas OJK dipilih untuk pinjaman daring {golongan}: tenor {hari} hari (6 bulan dihitung 180 hari), "
                  f"nilai pinjaman di perjanjian {rp(pokok)}; semua biaya yang dimasukkan dihitung sebagai manfaat ekonomi "
                  f"(denda keterlambatan, biaya tanda tangan elektronik bersertifikat, dan pajak tidak termasuk).")
    if TENOR_6_BULAN_HARI < hari <= TENOR_6_BULAN_KALENDER_MAKS_HARI:
        b_pendek, _ = batas_pinjol(jenis_pinjol, pokok, TENOR_6_BULAN_HARI)
        asumsi.append(f"Tenor {hari} hari dianggap di atas 6 bulan (6 bulan = 180 hari). Bila perjanjian menyebut tenornya "
                      f"6 bulan, batas yang berlaku adalah batas tenor sampai 6 bulan ({pct(b_pendek, 3)}/hari).")
    peringatan.append(f"Biaya total {rp(biaya)} untuk {hari} hari = {pct(per_hari, 3)} per hari dari uang yang diterima "
                      f"(setara ±{pct(tahun_sederhana, 0)} per tahun).")
    if me_per_hari > batas:
        peringatan.append(f"Bunga + biaya = {pct(me_per_hari, 3)} per hari dari nilai pinjaman {rp(pokok)}, di atas "
                          f"{pct(batas, 3)}/hari, batas pinjaman daring {golongan} ({RUJUKAN_PINJOL_SINGKAT}); "
                          f"cek aturan OJK terbaru dan legalitas penyelenggara di ojk.go.id / Kontak OJK 157.")
    if diterima < pokok:
        peringatan.append(f"Uang cair {rp(diterima)} tetapi yang harus dikembalikan dihitung dari {rp(pokok)}.")
    return {"ringkasan": ring}


def tambah_denda(a, hasil, dasar, asumsi):
    if not a.denda:
        return
    telat = int(a.telat)
    if telat <= 0:
        raise Galat("jumlah hari telat harus > 0", "Contoh: --telat 10")
    s = str(a.denda).strip().lower()
    if "%" in s or "persen" in s:
        bp, per = parse_persen(s, "denda")
        if per == "bulan":
            bp = bp / 30
        denda = bulat(dasar * bp / SERATUS * telat)
        dasar_t = f"{pct(bp, 3)} per hari x {rp(dasar)} x {telat} hari"
    else:
        v = parse_rupiah(s, "denda")
        denda = v * telat
        dasar_t = f"{rp(v)} per hari x {telat} hari"
    hasil["denda_ilustrasi"] = {"hari_telat": telat, "denda": denda, "rumus": dasar_t}
    asumsi.append("Denda dihitung dari tunggakan satu cicilan (ilustrasi; cek cara hitung di perjanjian).")


def bandingkan_bunga(a, hasil):
    """Tabel cicilan pada beberapa angka bunga efektif (ilustrasi bila bunga belum diketahui)."""
    pokok = hasil["input_terbaca"].get("pokok_yang_dicicil")
    n = hasil["input_terbaca"].get("tenor")
    if not pokok or hasil["input_terbaca"].get("satuan_tenor") != "bulan":
        raise Galat("--bandingkan-bunga butuh pokok dan tenor dalam bulan", "Contoh: --pokok 20jt --tenor 24")
    out = []
    for t in [x for x in a.bandingkan_bunga.split(";") if x.strip()]:
        flat = "flat" in t.lower()
        bp, per = parse_persen(t, "bandingkan bunga")
        r = bp / SERATUS / (1 if per == "bulan" else 12)
        if flat:
            rows = jadwal_flat(pokok, r, n)
            cic, tb = rows[0]["cicilan"], sum(x["bunga"] for x in rows)
            ef = eir(pokok, rows)["per_tahun_persen"]
        else:
            cic = bulat(-pmt(r, n, pokok))
            tb, ef = cic * n - pokok, r * 12 * SERATUS
        out.append({"jenis": "flat" if flat else "efektif", "bunga_per_bulan_persen": r * SERATUS,
                    "bunga_per_tahun_persen": r * 12 * SERATUS, "bunga_efektif_per_tahun_persen": ef,
                    "cicilan": cic, "total_bunga": tb})
    return out


# ------------------------------------------------------------------ teks
def teks(h):
    L = []
    it, rg = h.get("input_terbaca", {}), h.get("ringkasan")
    if h["mode"] == "harian":
        L.append(f"Pinjaman {rp(it['pokok_pinjaman'])}, {it['tenor']} hari, dibayar sekali di akhir")
        L.append(f"  Pinjaman bersih setelah biaya di muka : {rp(rg['uang_diterima_bersih'])}")
        L.append(f"  Bunga                    : {pct(rg['bunga_per_hari_persen'], 3)}/hari = {rp(rg['bunga_total'])}")
        L.append(f"  Total dikembalikan       : {rp(rg['total_kembali'])}")
        L.append(f"  Total biaya pinjaman     : {rp(rg['total_biaya_pinjaman'])}")
        L.append(f"  Biaya per hari (bersih)  : {pct(rg['biaya_total_per_hari_persen'], 3)}  ~ {pct(rg['setara_per_bulan_persen'], 1)}/bulan"
                 f"  ~ {pct(rg['setara_per_tahun_persen'], 0)}/tahun")
        L.append(f"  Cara hitung OJK          : {pct(rg['manfaat_ekonomi_per_hari_persen'], 3)}/hari dari nilai pinjaman; "
                 f"batas {pct(rg['batas_tercatat_per_hari_persen'], 3)}/hari ({rg['golongan_batas']})")
    elif h["mode"] == "bulanan":
        jen = {"flat": "flat", "efektif": "efektif/anuitas", "dari_cicilan": "dihitung balik dari cicilan"}[rg["jenis_bunga"]]
        L.append(f"Pinjaman {rp(it['pokok_pinjaman'])}, tenor {it['tenor']} bulan, bunga {jen} "
                 f"{pct(rg['bunga_bulanan_persen'], 3)}/bulan ({pct(rg['bunga_tahunan_tertulis_persen'])}/tahun)")
        if it.get("harga") is not None:
            L.append(f"  Harga {rp(it['harga'])}, DP {rp(it['dp'])}")
        if rg.get("cicilan_per_tahap"):
            for t in rg["cicilan_per_tahap"]:
                L.append(f"  Cicilan bulan {t['bulan']:<10} : {rp(t['cicilan'])} (bunga {pct(t['bunga_per_tahun_persen'])}/tahun)")
        else:
            L.append(f"  Cicilan per bulan        : {rp(rg['cicilan_per_bulan'])}"
                     + (f" (cicilan terakhir {rp(rg['cicilan_terakhir'])})" if rg['cicilan_terakhir'] != rg['cicilan_per_bulan'] else ""))
        if rg["biaya_bulanan"]:
            L.append(f"  + biaya bulanan          : {rp(rg['biaya_bulanan'])} -> {rp(rg['dibayar_per_bulan'])}/bulan")
        L.append(f"  Total cicilan            : {rp(rg['total_cicilan'])}")
        L.append(f"  Total bunga              : {rp(rg['total_bunga'])}")
        if rg["biaya_di_muka"]:
            L.append(f"  Biaya di muka            : {rp(rg['biaya_di_muka'])}")
        L.append(f"  Pinjaman bersih setelah biaya di muka : {rp(rg['uang_diterima_bersih'])}")
        L.append(f"  Total biaya pinjaman     : {rp(rg['total_biaya_pinjaman'])} (bunga + semua biaya)")
        e0, e1 = rg["bunga_efektif_setara_tanpa_biaya"], rg["bunga_efektif_setara_dengan_biaya"]
        if e0:
            L.append(f"  Bunga efektif setara     : {pct(e0['per_tahun_persen'])}/tahun (tanpa biaya)")
        if e1 and rg["biaya_di_muka"] + rg["biaya_bulanan"] > 0:
            L.append(f"  Termasuk semua biaya     : {pct(e1['per_tahun_persen'])}/tahun (majemuk {pct(e1['per_tahun_majemuk_persen'])})")
        if "total_harga_kredit" in rg:
            L.append(f"  Total harga lewat kredit : {rp(rg['total_harga_kredit'])} (lebih mahal {rp(rg['lebih_mahal_dari_tunai'])} "
                     f"= {pct(rg['lebih_mahal_dari_tunai_persen'], 1)} dari harga tunai)")
        if rg.get("selisih_pembulatan_cicilan_terakhir"):
            L.append(f"  Selisih pembulatan       : {rp(rg['selisih_pembulatan_cicilan_terakhir'])} di cicilan terakhir")
        pb = h.get("perbandingan")
        if pb and rg["jenis_bunga"] == "dari_cicilan":
            fs = pb["bunga_flat_setara_dari_cicilan_ini"]
            L.append(f"  Bila ditulis cara flat   : {pct(fs['per_bulan_persen'], 3)}/bulan ({pct(fs['per_tahun_persen'])}/tahun)")
        elif pb:
            L.append(f"Perbandingan pada angka {pct(pb['angka_bunga_per_tahun_persen'])}/tahun:")
            L.append(f"  Flat    : cicilan {rp(pb['flat']['cicilan'])}, total bunga {rp(pb['flat']['total_bunga'])}, "
                     f"setara efektif {pct(pb['flat']['bunga_efektif_setara_per_tahun_persen'])}/tahun")
            L.append(f"  Anuitas : cicilan {rp(pb['anuitas']['cicilan'])}, total bunga {rp(pb['anuitas']['total_bunga'])}")
            L.append(f"  Selisih total bunga      : {rp(pb['selisih_total_bunga_flat_minus_anuitas'])}")
        rows = h.get("jadwal")
        if rows:
            L.append("Jadwal (bulan | cicilan | pokok | bunga | sisa):")
            for r in rows:
                L.append(f"  {r['bulan']:>3} | {rp(r['cicilan'])} | {rp(r['pokok'])} | {rp(r['bunga'])} | {rp(r['sisa'])}")
        else:
            L.append("Ringkasan per tahun (tahun | pokok dibayar | bunga dibayar | sisa akhir):")
            for r in h["jadwal_per_tahun"]:
                L.append(f"  {r['tahun']:>2} | {rp(r['pokok_dibayar'])} | {rp(r['bunga_dibayar'])} | {rp(r['sisa_akhir'])}"
                         + (f"  ({r['catatan']})" if r.get("catatan") else ""))
    if h.get("bandingkan_bunga"):
        L.append("Cicilan pada beberapa angka bunga (ilustrasi, bukan tawaran"
                 + (f"; {h['ilustrasi_untuk']}; bunga ilustrasi, bukan acuan pasar - masukkan bunga dari penawaran Anda"
                    if h.get("ilustrasi_untuk") else "") + "):")
        for r in h["bandingkan_bunga"]:
            label = (f"flat {pct(r['bunga_per_bulan_persen'], 2)}/bulan" if r["jenis"] == "flat"
                     else f"efektif {pct(r['bunga_per_tahun_persen'], 1)}/tahun")
            L.append(f"  {label} -> {rp(r['cicilan'])}/bulan, total bunga {rp(r['total_bunga'])}, "
                     f"bunga efektif setara {pct(r['bunga_efektif_per_tahun_persen'], 1)}/tahun")
    if h.get("denda_ilustrasi"):
        d = h["denda_ilustrasi"]
        L.append(f"Denda telat {d['hari_telat']} hari: {rp(d['denda'])} ({d['rumus']})")
    k = h.get("kemampuan_bayar")
    if k:
        L.append(f"Kemampuan bayar (penghasilan bersih {rp(k['penghasilan_bersih'])}, cicilan lain {rp(k['cicilan_lain'])}):")
        L.append(f"  Cicilan maksimal aman    : {rp(k['cicilan_maksimal_aman'])} ({pct(k['batas_persen'], 0)}); "
                 f"batas atas {rp(k['cicilan_maksimal_batas_atas'])} ({pct(k['batas_atas_persen'], 0)})")
        if "rasio_semua_cicilan_persen" in k:
            L.append(f"  Rasio semua cicilan      : {pct(k['rasio_semua_cicilan_persen'], 1)} -> {k['status']}")
        if "pinjaman_maksimal_aman_dengan_bunga_tenor_ini" in k:
            L.append(f"  Pinjaman maksimal aman   : {rp(k['pinjaman_maksimal_aman_dengan_bunga_tenor_ini'])} (bunga & tenor sama)")
    for x in h.get("peringatan", []):
        L.append("! " + x)
    for x in h.get("asumsi", []):
        L.append("Asumsi: " + x)
    L.append("Simulasi, bukan penawaran atau nasihat keuangan; angka final mengikuti tabel angsuran resmi lembaga pembiayaan.")
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="Simulasi cicilan pinjaman (flat/efektif/anuitas/harian) dengan bunga efektif setara.")
    p.add_argument("--harga", help="harga barang (pakai bersama --dp)")
    p.add_argument("--dp", help="uang muka: rupiah (5jt) atau persen (20%%)")
    p.add_argument("--pokok", help="pokok pinjaman langsung (mengabaikan harga/DP)")
    p.add_argument("--tenor", help="36 | 3th | 14hari | 2minggu")
    p.add_argument("--bunga", help="0,8%%/bulan | 9,6%%/tahun | 0,3%%/hari (tanpa satuan = per tahun)")
    p.add_argument("--jenis", choices=["flat", "efektif", "anuitas"], help="jenis bunga (anuitas = efektif)")
    p.add_argument("--bunga-tahap", help="bunga bertahap efektif, mis. \"5%%x36;11%%\" (KPR fixed lalu floating)")
    p.add_argument("--cicilan", help="cicilan per bulan yang diketahui (bunga dihitung balik)")
    p.add_argument("--admin", help="biaya admin di muka (rupiah atau %% pokok)")
    p.add_argument("--provisi", help="provisi di muka (rupiah atau %% pokok)")
    p.add_argument("--asuransi", help="asuransi dibayar di muka (rupiah atau %% pokok)")
    p.add_argument("--biaya-lain", help="biaya di muka lain (notaris, materai, survei)")
    p.add_argument("--biaya-bulanan", help="biaya tetap per bulan di luar cicilan (mis. asuransi bulanan)")
    p.add_argument("--cara-biaya", choices=["tunai", "potong", "masuk-pinjaman"], default="tunai",
                   help="biaya di muka: dibayar tunai (default), dipotong dari pencairan, atau ditambahkan ke pinjaman")
    p.add_argument("--jenis-pinjol", choices=["konsumtif", "produktif"],
                   help="jenis pinjaman daring untuk memilih batas OJK (default konsumtif, dicatat sebagai asumsi; "
                        "tenor & nilai pinjaman dipilih otomatis)")
    p.add_argument("--denda", help="denda telat: 0,1%%/hari dari tunggakan, atau rupiah per hari")
    p.add_argument("--telat", default="7", help="hari telat untuk ilustrasi denda (default 7)")
    p.add_argument("--penghasilan", help="penghasilan bersih per bulan (untuk cicilan maksimal aman)")
    p.add_argument("--cicilan-lain", help="cicilan lain yang sedang berjalan per bulan")
    p.add_argument("--batas", default="30", help="batas aman rasio cicilan (%% penghasilan bersih), default 30")
    p.add_argument("--batas-atas", default="35", help="batas atas rasio cicilan, default 35")
    p.add_argument("--bandingkan-bunga", help="ilustrasi cicilan pada beberapa bunga efektif, mis. \"10;15;20\"")
    p.add_argument("--ilustrasi", choices=sorted(ILUSTRASI), help="bunga belum diketahui: bunga ilustrasi per jenis kredit (bukan acuan pasar)")
    p.add_argument("--jadwal-lengkap", action="store_true", help="tampilkan semua baris jadwal")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    a = p.parse_args(argv)
    if a.jenis == "anuitas":
        a.jenis = "efektif"
    ilu = None
    if a.ilustrasi and not a.bandingkan_bunga:
        ilu, a.bandingkan_bunga = ILUSTRASI[a.ilustrasi]
    try:
        if a.bandingkan_bunga and not (a.bunga or a.cicilan or a.bunga_tahap):
            # Mode ilustrasi: pokok + tenor saja
            pokok = parse_rupiah(a.pokok, "pokok") if a.pokok else None
            if pokok is None and a.harga:
                h0 = hitung_pokok_saja(a)
                pokok = h0
            if pokok is None or not a.tenor:
                raise Galat("--bandingkan-bunga butuh pokok/harga dan tenor", "Contoh: --pokok 20jt --tenor 24 --bandingkan-bunga \"10;15;20\"")
            n, sat = parse_tenor(a.tenor)
            if sat != "bulan":
                raise Galat("--bandingkan-bunga hanya untuk tenor bulanan", "Contoh: --tenor 24")
            h = {"mode": "ilustrasi", "input_terbaca": {"pokok_yang_dicicil": pokok, "pokok_pinjaman": pokok, "tenor": n,
                                                        "satuan_tenor": "bulan"},
                 "asumsi": ["Bunga belum diketahui: angka bunga di tabel adalah bunga ilustrasi, bukan acuan pasar dan bukan "
                            "tawaran lembaga mana pun; masukkan bunga dari penawaran Anda untuk hasil sebenarnya."],
                 "peringatan": []}
            if a.penghasilan:
                h["kemampuan_bayar"] = hitung_kemampuan(a)
        else:
            h = hitung(a)
        if a.bandingkan_bunga:
            h["bandingkan_bunga"] = bandingkan_bunga(a, h)
            if ilu:
                h["ilustrasi_untuk"] = ilu
    except Galat as g:
        print(json.dumps({"error": g.pesan, "saran": g.saran}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    h["disclaimer"] = ("Simulasi, bukan penawaran atau nasihat keuangan. Angka final mengikuti tabel angsuran resmi "
                       "lembaga pembiayaan; bank/leasing bisa memakai pembulatan dan biaya berbeda.")
    if a.format == "teks":
        print(teks(h))
    else:
        print(json.dumps(jsonable(h), ensure_ascii=False, indent=2))
    return 0


def hitung_pokok_saja(a):
    harga = parse_rupiah(a.harga, "harga")
    dpv = parse_rupiah(a.dp, "DP", boleh_persen=True) if a.dp else NOL
    dp = bulat(harga * dpv[1] / SERATUS) if isinstance(dpv, tuple) else dpv
    if harga - dp <= 0:
        raise Galat("DP sama dengan/lebih besar dari harga", "Periksa harga dan DP.")
    return harga - dp


if __name__ == "__main__":
    sys.exit(main())
