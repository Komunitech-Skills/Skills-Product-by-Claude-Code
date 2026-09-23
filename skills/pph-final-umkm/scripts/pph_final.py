#!/usr/bin/env python3
"""Hitung PPh Final UMKM 0,5% per bulan + pelacak omzet kumulatif setahun.

Dasar: PP 55/2022 sebagaimana diubah PP 20/2026 (ditetapkan 22 April 2026). Status per 2026-09-23.
- Wajib Pajak orang pribadi (OP): omzet s.d. Rp500.000.000 setahun TIDAK dikenai pajak.
  Pajak 0,5% hanya atas bagian omzet yang melewati Rp500 juta (bulan saat melewati dihitung proporsional).
- Badan (PT perorangan, koperasi, dll.): 0,5% x seluruh omzet bulan itu (tanpa pembebasan Rp500 juta).
- PPh 22 marketplace (PMK 37/2025) hanya DICATAT sebagai informasi, tidak dikurangkan otomatis.

Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 pph_final.py --jenis op --tahun 2026 --omzet 45jt 60jt 80jt 120jt 150jt 90jt
  python3 pph_final.py --jenis badan --file omzet.csv --format json
"""
import argparse
import csv
import datetime
import json
import re
import sys
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

TANGGAL_ATURAN = "2026-09-23"
DASAR_ATURAN = "PP 55/2022 jo. PP 20/2026 (PPh Final UMKM 0,5%); PMK 37/2025 (PPh 22 marketplace)"
TARIF = Decimal("0.005")
BATAS_BEBAS_OP = Decimal(500000000)
BATAS_OMZET_UMKM = Decimal(4800000000)

NAMA_BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
              "September", "Oktober", "November", "Desember"]
ALIAS_BULAN = {
    "jan": 1, "feb": 2, "peb": 2, "mar": 3, "apr": 4, "mei": 5, "may": 5, "jun": 6, "jul": 7,
    "agu": 8, "agt": 8, "ags": 8, "aug": 8, "sep": 9, "okt": 10, "oct": 10, "nov": 11, "nop": 11,
    "des": 12, "dec": 12,
}


# ---------------------------------------------------------------- angka & format
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3), ("m", 10 ** 9)]


def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise ValueError("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                         "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))


def parse_angka(nilai, nama="angka"):
    """Baca angka format Indonesia: 'Rp 15.000', '15.000,50', '1,5 jt', '4,8 M', '15000'."""
    if isinstance(nilai, bool) or nilai is None:
        raise ValueError("{}: nilai kosong atau tidak valid".format(nama))
    if isinstance(nilai, Decimal):
        return nilai
    if isinstance(nilai, int):
        return Decimal(nilai)
    if isinstance(nilai, float):
        return Decimal(str(nilai))
    asli = str(nilai)
    s = asli.strip().lower().replace("\u00a0", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    if s.endswith("%"):
        s = s[:-1]
    pengali = 1
    for akhiran, kali in _PENGALI:
        if s.endswith(akhiran):
            s, pengali = s[: -len(akhiran)], kali
            break
    negatif = s.startswith("-")
    if negatif:
        s = s[1:]
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    if "," in s and "." in s:
        if s.rfind(",") < s.rfind("."):
            raise ValueError("{}: '{}' memakai format Inggris. Tulis dengan titik untuk ribuan dan koma "
                             "untuk desimal, mis. 1.250.000,50".format(nama, asli))
        utuh, _, desimal = s.rpartition(",")
        _cek_ribuan(utuh.split("."), asli, nama)
        s = utuh.replace(".", "") + "." + desimal
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2:
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(".", "")
    try:
        d = Decimal(s) * pengali
    except InvalidOperation:
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    return -d if negatif else d


def format_rp(d, desimal=False):
    d = Decimal(d).quantize(Decimal("0.01") if desimal else Decimal(1), ROUND_HALF_UP)
    neg = d < 0
    d = abs(d)
    teks = "{:,}".format(int(d)).replace(",", ".")
    if desimal:
        pecahan = "{:.2f}".format(d).split(".")[1]
        if pecahan != "00":
            teks += "," + pecahan
    return ("-" if neg else "") + "Rp " + teks


def ke_json(d):
    if isinstance(d, Decimal):
        return int(d) if d == d.to_integral_value() else float(d.quantize(Decimal("0.01"), ROUND_HALF_UP))
    raise TypeError(str(type(d)))


# ---------------------------------------------------------------- input
def parse_bulan(teks):
    s = str(teks).strip().lower()
    if re.fullmatch(r"\d{1,2}", s):
        b = int(s)
    else:
        m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})", s) or re.fullmatch(r"(\d{1,2})[-/.](\d{4})", s)
        if m:
            a, c = m.groups()
            b = int(c) if len(a) == 4 else int(a)
        else:
            b = ALIAS_BULAN.get(s[:3])
            if b is None:
                raise ValueError("bulan '{}' tidak dikenali (pakai 1-12 atau nama bulan, mis. 'Januari')"
                                 .format(teks))
    if not 1 <= b <= 12:
        raise ValueError("bulan '{}' di luar 1-12".format(teks))
    return b


def cari_kolom(header, kata):
    for i, h in enumerate(header):
        h2 = re.sub(r"[^a-z0-9]", "", h.lower())
        if any(k in h2 for k in kata):
            return i
    return None


def baca_file(path):
    """CSV (bulan;omzet;pph22) atau JSON [{bulan, omzet, pph22}] -> list (bulan, omzet, pph22)."""
    try:
        with open(path, encoding="utf-8-sig", newline="") as f:
            isi = f.read()
    except OSError as e:
        raise ValueError("file '{}' tidak bisa dibaca: {}".format(path, e.strerror or e))
    if not isi.strip():
        raise ValueError("file '{}' kosong".format(path))
    data = []
    if path.lower().endswith(".json"):
        try:
            obj = json.loads(isi)
        except json.JSONDecodeError as e:
            raise ValueError("JSON tidak valid (baris {}): {}".format(e.lineno, e.msg))
        if isinstance(obj, dict):
            obj = obj.get("bulan") or obj.get("data") or []
        if not isinstance(obj, list):
            raise ValueError("JSON harus berupa daftar: [{\"bulan\": 1, \"omzet\": 45000000}, ...]")
        for i, r in enumerate(obj, 1):
            if not isinstance(r, dict) or "bulan" not in r or "omzet" not in r:
                raise ValueError("data ke-{} wajib punya 'bulan' dan 'omzet'".format(i))
            data.append((parse_bulan(r["bulan"]), parse_angka(r["omzet"], "omzet data ke-{}".format(i)),
                         parse_angka(r.get("pph22", 0) or 0, "pph22 data ke-{}".format(i))))
        return data
    try:
        dialek = csv.Sniffer().sniff(isi[:2048], delimiters=";,\t|")
    except csv.Error:
        dialek = csv.excel
    baris = [r for r in csv.reader(isi.splitlines(), dialek) if any(c.strip() for c in r)]
    header = baris[0]
    ib = cari_kolom(header, ["bulan", "month", "periode", "masa"])
    io = cari_kolom(header, ["omzet", "omset", "peredaran", "penjualan", "bruto", "revenue", "sales"])
    ip = cari_kolom(header, ["pph22", "pph", "marketplace", "dipungut"])
    if ib is None or io is None:
        raise ValueError("CSV wajib punya kolom 'bulan' dan 'omzet' di baris pertama (header). "
                         "Contoh: bulan;omzet;pph22")
    for no, r in enumerate(baris[1:], 2):
        if len(r) <= max(ib, io):
            raise ValueError("baris {} CSV tidak lengkap: {}".format(no, r))
        pph = r[ip] if ip is not None and ip < len(r) and r[ip].strip() else "0"
        data.append((parse_bulan(r[ib]), parse_angka(r[io], "omzet baris {}".format(no)),
                     parse_angka(pph, "pph22 baris {}".format(no))))
    return data


# ---------------------------------------------------------------- perhitungan
def batas_setor(tahun, bulan):
    """Tanggal 15 bulan berikutnya."""
    if bulan == 12:
        return datetime.date(tahun + 1, 1, 15)
    return datetime.date(tahun, bulan + 1, 15)


def hitung(data, jenis, tahun, omzet_sebelumnya=Decimal(0), hari_ini=None):
    if not data:
        raise ValueError("belum ada data omzet")
    if len(data) > 12:
        raise ValueError("maksimal 12 bulan dalam satu tahun pajak")
    dilihat = set()
    for b, o, p in data:
        if b in dilihat:
            raise ValueError("bulan {} diisi lebih dari sekali".format(NAMA_BULAN[b - 1]))
        dilihat.add(b)
        if o < 0:
            raise ValueError("omzet {} tidak boleh negatif".format(NAMA_BULAN[b - 1]))
        if p < 0:
            raise ValueError("PPh 22 {} tidak boleh negatif".format(NAMA_BULAN[b - 1]))
    if omzet_sebelumnya < 0:
        raise ValueError("omzet sebelumnya tidak boleh negatif")
    data = sorted(data)
    kumulatif = omzet_sebelumnya
    rows = []
    catatan = []
    bulan_lewat_500 = None
    bulan_lewat_48 = None
    if jenis == "op" and omzet_sebelumnya >= BATAS_BEBAS_OP:
        bulan_lewat_500 = "sebelum periode ini"
    for b, omzet, pph22 in data:
        sebelum = kumulatif
        kumulatif = sebelum + omzet
        if jenis == "op":
            # Hanya bagian omzet di atas Rp500 juta (kumulatif setahun) yang kena pajak
            kena = max(kumulatif - max(sebelum, BATAS_BEBAS_OP), Decimal(0))
        else:
            kena = omzet
        pph = (kena * TARIF).quantize(Decimal(1), ROUND_FLOOR)
        ket = []
        if jenis == "op" and sebelum <= BATAS_BEBAS_OP < kumulatif:
            bulan_lewat_500 = NAMA_BULAN[b - 1]
            ket.append("melewati Rp500 juta; hanya {} yang kena pajak".format(format_rp(kena, True)))
        elif jenis == "op" and kumulatif <= BATAS_BEBAS_OP:
            ket.append("masih dalam Rp500 juta bebas")
        if sebelum <= BATAS_OMZET_UMKM < kumulatif:
            bulan_lewat_48 = NAMA_BULAN[b - 1]
            ket.append("omzet setahun melewati Rp4,8 M")
        rows.append({
            "bulan": b,
            "nama_bulan": NAMA_BULAN[b - 1],
            "omzet": omzet,
            "omzet_kumulatif": kumulatif,
            "omzet_kena_pajak": kena,
            "pph_final": pph,
            "pph22_marketplace_info": pph22,
            "setor_paling_lambat": batas_setor(tahun, b).isoformat(),
            "batas_setor_sudah_lewat": bool(hari_ini and pph > 0 and batas_setor(tahun, b) < hari_ini),
            "keterangan": "; ".join(ket),
        })

    total_omzet = sum((r["omzet"] for r in rows), Decimal(0))
    total_pph = sum((r["pph_final"] for r in rows), Decimal(0))
    total_pph22 = sum((r["pph22_marketplace_info"] for r in rows), Decimal(0))
    sisa_bebas = max(BATAS_BEBAS_OP - kumulatif, Decimal(0)) if jenis == "op" else None

    bulan_ada = [r["bulan"] for r in rows]
    if bulan_ada[0] > 1 and omzet_sebelumnya == 0:
        catatan.append("Data mulai {}. Omzet bulan sebelumnya di tahun {} dianggap Rp 0; jika ada, isi "
                       "--omzet-sebelumnya agar batas Rp500 juta dihitung benar.".format(
                           NAMA_BULAN[bulan_ada[0] - 1], tahun))
    celah = [NAMA_BULAN[x - 1] for x in range(bulan_ada[0], bulan_ada[-1] + 1) if x not in bulan_ada]
    if celah:
        catatan.append("Bulan tanpa data dianggap omzet Rp 0: {}.".format(", ".join(celah)))
    if bulan_lewat_48:
        catatan.append("Omzet kumulatif melewati Rp4,8 miliar pada {}. Menurut ketentuan PP 55/2022, tarif 0,5% "
                       "umumnya masih dipakai sampai akhir tahun pajak ini dan mulai tahun berikutnya memakai tarif "
                       "umum (pembukuan). Pastikan ke DJP/konsultan pajak.".format(bulan_lewat_48))
    elif kumulatif > BATAS_OMZET_UMKM * Decimal("0.8"):
        catatan.append("Omzet kumulatif sudah di atas 80% dari batas Rp4,8 miliar. Siapkan pembukuan bila "
                       "batas terlewati.")
    lewat = [r["nama_bulan"] for r in rows if r["batas_setor_sudah_lewat"]]
    if lewat:
        catatan.append("Batas setor untuk {} sudah lewat per {}. Jika belum disetor, segera setor dan cek ke DJP "
                       "kemungkinan sanksi administrasi atas keterlambatan.".format(", ".join(lewat),
                                                                                  hari_ini.isoformat()))
    if total_pph22 > 0:
        catatan.append("PPh 22 marketplace yang tercatat ({}) hanya informasi. DJP menyebut pungutan ini bukan pajak "
                       "baru dan dapat diperhitungkan, tetapi cara memperhitungkannya dengan PPh final Anda perlu "
                       "dicek ke DJP/konsultan. Angka PPh final di atas BELUM dikurangi PPh 22.".format(
                           format_rp(total_pph22)))
    return {
        "jenis_wp": jenis,
        "tahun": tahun,
        "omzet_sebelumnya": omzet_sebelumnya,
        "bulan": rows,
        "ringkasan": {
            "total_omzet_periode": total_omzet,
            "omzet_kumulatif_tahun": kumulatif,
            "total_pph_final": total_pph,
            "total_pph22_marketplace_info": total_pph22,
            "sisa_omzet_bebas_pajak": sisa_bebas,
            "bulan_mulai_kena_pajak": bulan_lewat_500,
            "bulan_melewati_4_8_miliar": bulan_lewat_48,
        },
        "catatan": catatan,
    }


CATATAN_TETAP = [
    "Tarif 0,5% dihitung dari OMZET (peredaran bruto), bukan dari laba.",
    "Pembulatan: PPh tiap bulan dibulatkan ke bawah ke rupiah penuh (pecahan rupiah dibuang); belum dicocokkan "
    "dengan Coretax - bila berbeda, ikuti Coretax.",
    "Batas setor tercantum = tanggal 15 bulan berikutnya (ketentuan umum PMK 81/2024); cek DJP bila jatuh di hari libur.",
    "PP 20/2026: ketentuan masa transisi untuk CV/firma/PT dan batas jangka waktu pemakaian tarif 0,5% belum "
    "kami verifikasi. Cek pajak.go.id atau Kring Pajak 1500200 sebelum mengambil keputusan.",
    "Tidak berlaku untuk penghasilan dari jasa pekerjaan bebas (mis. dokter, notaris, konsultan) dan penghasilan "
    "lain yang dikecualikan PP 55/2022.",
]


def catatan_jenis(jenis, jenis_badan):
    c = []
    if jenis == "op":
        c.append("Orang pribadi: omzet s.d. Rp500 juta setahun tidak dikenai PPh final. Batas ini untuk total "
                 "omzet SEMUA usaha Anda dalam setahun.")
    else:
        c.append("Badan: 0,5% x seluruh omzet, tanpa pembebasan Rp500 juta.")
        if jenis_badan in ("cv", "firma", "pt"):
            c.append("PP 20/2026 mengeluarkan {} dari skema PPh final 0,5% dengan masa transisi yang belum kami "
                     "verifikasi. Hasil ini hanya simulasi; pastikan ke DJP/konsultan apakah usaha Anda masih "
                     "boleh memakai tarif 0,5%.".format(LABEL_BADAN[jenis_badan]))
    return c


# ---------------------------------------------------------------- output
LABEL_BADAN = {"pt-perorangan": "PT perorangan", "koperasi": "Koperasi", "cv": "CV", "firma": "Firma",
               "pt": "PT", "lainnya": "lainnya"}

def teks_markdown(h, jenis_badan):
    r = h["ringkasan"]
    label = "Orang pribadi" if h["jenis_wp"] == "op" else "Badan" + (
        " ({})".format(LABEL_BADAN[jenis_badan]) if jenis_badan else "")
    out = ["## PPh Final UMKM 0,5% - Tahun {} ({})".format(h["tahun"], label), ""]
    if h["omzet_sebelumnya"]:
        out.append("Omzet sebelum periode ini: {}".format(format_rp(h["omzet_sebelumnya"])))
        out.append("")
    out.append("| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) "
               "| Setor paling lambat | Keterangan |")
    out.append("|---|---:|---:|---:|---:|---:|---|---|")
    for b in h["bulan"]:
        out.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            b["nama_bulan"], format_rp(b["omzet"], True), format_rp(b["omzet_kumulatif"], True),
            format_rp(b["omzet_kena_pajak"], True), format_rp(b["pph_final"]),
            format_rp(b["pph22_marketplace_info"]) if b["pph22_marketplace_info"] else "-",
            b["setor_paling_lambat"] + (" (SUDAH LEWAT)" if b["batas_setor_sudah_lewat"] else ""),
            b["keterangan"] or "-"))
    out.append("| **Total** | **{}** | | | **{}** | {} | | |".format(
        format_rp(r["total_omzet_periode"], True), format_rp(r["total_pph_final"]),
        format_rp(r["total_pph22_marketplace_info"]) if r["total_pph22_marketplace_info"] else "-"))
    out.append("")
    out.append("**Ringkasan**")
    out.append("- Omzet kumulatif tahun {}: {}".format(h["tahun"], format_rp(r["omzet_kumulatif_tahun"], True)))
    out.append("- Total PPh final periode ini: {}".format(format_rp(r["total_pph_final"])))
    if h["jenis_wp"] == "op":
        if r["sisa_omzet_bebas_pajak"] > 0:
            out.append("- Sisa omzet bebas pajak tahun ini: {}".format(format_rp(r["sisa_omzet_bebas_pajak"], True)))
        elif r["bulan_mulai_kena_pajak"]:
            out.append("- Batas Rp500 juta bebas pajak sudah terlewati ({}).".format(r["bulan_mulai_kena_pajak"]))
        else:
            out.append("- Omzet tepat mencapai batas Rp500 juta: belum ada omzet yang kena pajak, tetapi mulai rupiah "
                       "berikutnya seluruh omzet kena 0,5%.")
    out.append("- Sisa ruang sebelum batas Rp4,8 miliar: {}".format(
        format_rp(max(BATAS_OMZET_UMKM - r["omzet_kumulatif_tahun"], Decimal(0)), True)))
    out.append("")
    out.append("**Catatan penting**")
    for c in h["catatan"]:
        out.append("- " + c)
    out.append("")
    out.append("_Dasar: {}. Berlaku per {}. Ini alat bantu hitung, bukan nasihat pajak. Untuk kepastian, hubungi "
               "DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak._".format(DASAR_ATURAN, TANGGAL_ATURAN))
    return "\n".join(out)


class ParserID(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen tidak valid ({}).\nLihat bantuan: python3 pph_final.py --help\n"
                         .format(message))
        sys.exit(2)


def main(argv=None):
    p = ParserID(description="PPh Final UMKM 0,5% per bulan + pelacak omzet kumulatif setahun.")
    p.add_argument("--jenis", choices=["op", "badan"], default="op",
                   help="'op' = orang pribadi (default, bebas Rp500 juta pertama); 'badan' = PT perorangan, koperasi, dll.")
    p.add_argument("--jenis-badan", choices=["pt-perorangan", "koperasi", "cv", "firma", "pt", "lainnya"],
                   help="Opsional, untuk catatan khusus badan.")
    p.add_argument("--tahun", type=int, default=datetime.date.today().year, help="Tahun pajak")
    p.add_argument("--omzet", nargs="+", help="Omzet per bulan berurutan, mis. 45jt 60jt 'Rp 80.000.000'")
    p.add_argument("--bulan-awal", default="1", help="Bulan untuk nilai --omzet pertama (default 1 = Januari)")
    p.add_argument("--pph22", nargs="+", help="PPh 22 marketplace yang sudah dipotong per bulan (urutan sama dengan --omzet)")
    p.add_argument("--file", help="CSV (kolom bulan;omzet;pph22) atau JSON sebagai ganti --omzet")
    p.add_argument("--omzet-sebelumnya", default="0",
                   help="Omzet kumulatif tahun ini SEBELUM bulan pertama data (default 0)")
    p.add_argument("--hari-ini", help="Tanggal acuan untuk menandai batas setor yang sudah lewat (YYYY-MM-DD, default hari ini)")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    a = p.parse_args(argv)

    try:
        if a.jenis == "op" and a.jenis_badan:
            raise ValueError("--jenis-badan hanya untuk --jenis badan")
        if not 2000 <= a.tahun <= 2100:
            raise ValueError("tahun {} tidak masuk akal".format(a.tahun))
        if a.file and a.omzet:
            raise ValueError("pakai salah satu: --omzet atau --file")
        if a.file:
            data = baca_file(a.file)
        elif a.omzet:
            awal = parse_bulan(a.bulan_awal)
            if awal + len(a.omzet) - 1 > 12:
                raise ValueError("{} nilai omzet mulai {} melewati Desember".format(len(a.omzet), NAMA_BULAN[awal - 1]))
            pph22 = a.pph22 or []
            if len(pph22) > len(a.omzet):
                raise ValueError("jumlah nilai --pph22 lebih banyak dari --omzet")
            data = []
            for i, o in enumerate(a.omzet):
                b = awal + i
                data.append((b, parse_angka(o, "omzet " + NAMA_BULAN[b - 1]),
                             parse_angka(pph22[i], "pph22 " + NAMA_BULAN[b - 1]) if i < len(pph22) else Decimal(0)))
        else:
            raise ValueError("isi omzet dengan --omzet atau --file")
        try:
            hari_ini = (datetime.datetime.strptime(a.hari_ini.strip(), "%Y-%m-%d").date() if a.hari_ini
                        else datetime.date.today())
        except ValueError:
            raise ValueError("--hari-ini '{}' tidak valid (pakai format 2026-09-23)".format(a.hari_ini))
        hasil = hitung(data, a.jenis, a.tahun, parse_angka(a.omzet_sebelumnya, "omzet sebelumnya"), hari_ini)
        hasil["hari_ini"] = hari_ini.isoformat()
    except ValueError as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        return 2

    hasil["catatan"] = catatan_jenis(a.jenis, a.jenis_badan) + hasil["catatan"] + CATATAN_TETAP
    hasil["dasar_aturan"] = DASAR_ATURAN
    hasil["berlaku_per"] = TANGGAL_ATURAN
    hasil["disclaimer"] = ("Alat bantu hitung, bukan nasihat pajak. Konfirmasi ke DJP (Kring Pajak 1500200) "
                           "atau konsultan pajak.")
    if a.format == "json":
        hasil["jenis_badan"] = a.jenis_badan
        print(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2))
    else:
        print(teks_markdown(hasil, a.jenis_badan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
