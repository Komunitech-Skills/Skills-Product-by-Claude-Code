#!/usr/bin/env python3
"""Rekap penjualan dari file CSV. Output: JSON ke stdout.

Hanya memakai library standar Python (3.8+).
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
from fractions import Fraction

VERSI = "1.2.7"

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
STATUS_BATAL_DEFAULT = ["batal", "dibatalkan", "cancel", "retur", "return", "refund", "gagal", "failed",
                        "pengembalian", "dikembalikan", "belum bayar", "belum dibayar", "unpaid",
                        "menunggu pembayaran", "kedaluwarsa", "expired"]

# Status yang mengandung kata di atas tetapi transaksinya TETAP sah (mis. "Pengembalian Ditolak")
PENGECUALIAN_STATUS = ["ditolak", "rejected", "dibatalkan pembatalannya"]

# Status yang dianggap sudah final (uang aman). Status lain yang tetap dihitung (mis. "Sedang Dikirim")
# ditandai "belum final" di ringkasan karena masih bisa batal/retur.
STATUS_FINAL = ["selesai", "completed", "complete", "diterima", "delivered"]

NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]  # date.weekday(): 0 = Senin
MIN_HARI_POLA = 14   # pola hari dalam minggu hanya bila periode >= 14 hari kalender

BULAN_PENDEK = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

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
    """Untuk tanggal angka a/b/tahun: 'dmy' (Indonesia) atau 'mdy' (AS). Kembalikan (urutan, ambigu)."""
    dmy_pasti = mdy_pasti = False
    for t in teks_tanggal:
        m = POLA_ANGKA_3.match(t.strip())
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12:
            dmy_pasti = True
        if b > 12:
            mdy_pasti = True
    if mdy_pasti and not dmy_pasti:
        return "mdy", False
    return "dmy", not dmy_pasti  # ambigu bila tidak ada bukti hari > 12


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
    """'1.250.000' valid; '15000.500' / '15.00' tidak (grup pertama 1–3 digit, sisanya tepat 3)."""
    grup = bagian_bulat.split(pemisah)
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def parse_angka(teks):
    """Angka format Indonesia/Inggris -> float, atau None bila tidak valid/meragukan.

    Mendukung: '15000', 'Rp 15.000', 'Rp. 25000', 'IDR 25.000', 'Rp 15.000,-',
    '15.000,50', '15,000.50', '1.250.000', '12,5'.
    Menolak (None) format ambigu: '15.000.00', '15000.500', notasi ilmiah '1.5E+06'.
    """
    if teks is None:
        return None
    s = str(teks).strip().lower()
    if not s:
        return None
    if re.fullmatch(r"\(.*\)", s):
        s = "-" + s[1:-1].strip()               # format akuntansi (15.000) = negatif
    if re.search(r"\d\s*e\s*[+-]?\s*\d", s):
        return None                               # notasi ilmiah dari Excel
    s = re.sub(r"\b(rp|idr)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)          # akhiran ',-' atau '.-'
    s = re.sub(r"[^\d,.\-]", "", s).strip(".,")
    if not s or s == "-":
        return None
    negatif = s.startswith("-")
    s = s.lstrip("-")
    if "-" in s:
        return None
    digit = sum(c.isdigit() for c in s)
    if "," in s and "." in s:
        # Pemisah desimal adalah yang muncul terakhir; sisanya wajib grup ribuan yang rapi
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
            s = bagian[0] + "." + bagian[1]       # '12,5' / '1.5' -> desimal
        elif _grup_ribuan_valid(s, pemisah):
            s = s.replace(pemisah, "")            # '15.000' / '1.250.000' -> ribuan
        else:
            return None                           # '15.000.00', '15000.500' -> ambigu
    try:
        nilai = float(s)
    except ValueError:
        return None
    # Pengaman: teks ber-4 digit atau lebih tapi hasil < 1 hampir pasti salah baca
    if digit >= 4 and 0 < nilai < 1:
        return None
    return -nilai if negatif else nilai


def rupiah(nilai):
    """Rupiah dibulatkan ke rupiah terdekat (setengah ke atas), pemisah ribuan titik: 'Rp 1.250.000'."""
    bulat = int(Decimal(str(nilai)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    tanda = "-" if bulat < 0 else ""
    return "Rp {}{:,}".format(tanda, abs(bulat)).replace(",", ".")


def tgl_id(iso):
    try:
        d = date.fromisoformat(iso)
    except ValueError:
        return iso
    return "{} {} {}".format(d.day, BULAN_PENDEK[d.month], d.year)


def tgl_hari(iso):
    """'Sabtu, 5 Sep 2026' (nama hari + tanggal). Bila bukan tanggal valid, dikembalikan apa adanya."""
    try:
        d = date.fromisoformat(iso)
    except ValueError:
        return iso
    return "{}, {}".format(NAMA_HARI[d.weekday()], tgl_id(iso))


def hitung_pola_hari(omzet_harian, awal, akhir):
    """Rata-rata omzet per hari dalam minggu = total omzet pada hari itu / jumlah kemunculan hari itu di periode
    (hari tanpa penjualan tetap dihitung sebagai kemunculan dengan omzet 0). None bila periode < 14 hari kalender.
    Perbandingan memakai pecahan eksak (tanpa galat float); seri disebut semua."""
    jumlah_hari = (akhir - awal).days + 1
    if jumlah_hari < MIN_HARI_POLA:
        return None
    muncul = [0] * 7
    for i in range(jumlah_hari):
        muncul[date.fromordinal(awal.toordinal() + i).weekday()] += 1
    total = [Fraction(0)] * 7
    for iso, v in omzet_harian.items():
        total[date.fromisoformat(iso).weekday()] += Fraction(str(round(v, 2)))
    rata = [total[i] / muncul[i] for i in range(7)]   # setiap hari muncul >= 2 kali bila periode >= 14 hari
    maks, mini = max(rata), min(rata)

    def rp(frac):
        return rupiah(Decimal(frac.numerator) / Decimal(frac.denominator))

    def sebut(nilai):
        return [{"hari": NAMA_HARI[i], "jumlah_kemunculan": muncul[i], "rata_rata_omzet": float(round(rata[i], 2)),
                 "total_omzet": float(total[i])} for i in range(7) if rata[i] == nilai]
    tinggi, rendah = sebut(maks), sebut(mini)
    dasar = ("rata-rata omzet per hari dalam minggu = total omzet pada hari itu dibagi jumlah hari itu di periode; "
             "hari tanpa penjualan dihitung Rp 0")
    if maks == mini:
        kalimat = ("Pola hari dalam minggu (omzet hari itu dibagi jumlah hari itu di periode; hari tanpa penjualan dihitung Rp 0): "
                   "sama untuk semua hari, {}.".format(rp(maks)))
    else:
        kalimat = ("Pola hari dalam minggu (omzet hari itu dibagi jumlah hari itu di periode; hari tanpa penjualan dihitung Rp 0): "
                   "tertinggi {} {}; terendah {} {}.".format(
                       gabung_daftar(x["hari"] for x in tinggi), rp(maks),
                       gabung_daftar(x["hari"] for x in rendah), rp(mini)))
    return {"dasar": dasar, "minimal_hari_kalender": MIN_HARI_POLA, "jumlah_hari_kalender": jumlah_hari,
            "per_hari": [{"hari": NAMA_HARI[i], "jumlah_kemunculan": muncul[i], "total_omzet": float(total[i]),
                          "rata_rata_omzet": float(round(rata[i], 2))} for i in range(7)],
            "tertinggi": tinggi, "terendah": rendah, "kalimat": kalimat}


def angka_qty(q):
    return str(int(q)) if float(q).is_integer() else ("%s" % round(q, 2)).replace(".", ",")


def persen_id(x):
    return ("%.1f" % x).replace(".", ",") + "%"


def gabung_daftar(item):
    item = list(item)
    if len(item) <= 1:
        return "".join(item)
    return ", ".join(item[:-1]) + " dan " + item[-1]


def susun_ringkasan(h, ada_status, satuan_pesanan):
    """Kalimat lengkap siap tempel ke grup tim. HANYA angka agregat: tanpa nama/nomor/alamat pembeli."""
    p = h["periode"]
    kal = []
    status_txt = ""
    if ada_status:
        status_txt = " (status yang dihitung: {})".format(gabung_daftar(
            [st for st, v in h["per_status"].items() if v["golongan"] == "dihitung"] or sorted(h["status_dihitung"])))
    kal.append("Rekap penjualan {} sampai {}: total omzet {} dari {} {}{}.".format(
        tgl_id(p["awal"]), tgl_id(p["akhir"]), rupiah(h["total_omzet"]),
        h["jumlah_pesanan_dihitung"], satuan_pesanan, status_txt))
    if ada_status and h["per_status"]:
        bagian = []
        for st, v in h["per_status"].items():
            teks = "{} {} {} senilai {}".format(st, v["jumlah_pesanan"], satuan_pesanan, rupiah(v["omzet"]))
            if v["baris_nilai_tak_terbaca"]:
                teks += " ({} baris nilainya tidak terbaca)".format(v["baris_nilai_tak_terbaca"])
            if v["golongan"] == "dibuang":
                teks += " (tidak masuk omzet)"
            elif not v["final"]:
                teks += " (sudah masuk omzet, belum final, bisa berubah bila batal/retur)"
            bagian.append(teks)
        kal.append("Rincian per status: " + "; ".join(bagian) + ".")
        if h["dibuang_per_tanggal"]:
            bagian = ["{} {} {} ({})".format(tgl_hari(x["tanggal"]), x["jumlah_pesanan"], satuan_pesanan, x["status"])
                      for x in h["dibuang_per_tanggal"]]
            kal.append("Pesanan yang tidak dihitung menurut tanggal pesanan: " + "; ".join(bagian) + ".")
        else:
            kal.append("Tidak ada pesanan batal/retur pada periode ini.")
    mode_pcs = h["satuan_jumlah_produk"] == "pcs"
    kunci_j, satuan_j = ("qty", "pcs") if mode_pcs else ("jumlah_baris", SATUAN_BARIS)
    top = h["produk_terlaris"][:3]
    if top:
        kal.append("Produk terlaris menurut omzet: " + gabung_daftar(
            "{} ({} {}, {})".format(x["produk"], angka_qty(x[kunci_j]), satuan_j, rupiah(x["omzet"])) for x in top) + ".")
    s = h["sorotan_produk"]
    tj = s["terlaris_qty"] if mode_pcs else s["terlaris_baris"]
    if tj:
        kal.append("{}: {} ({} {}{}).".format(
            "Paling banyak terjual menurut jumlah" if mode_pcs else "Paling sering tercatat",
            gabung_daftar(x["produk"] for x in tj), angka_qty(tj[0][kunci_j]), satuan_j,
            " masing-masing" if len(tj) > 1 else ""))
    if not mode_pcs:
        kal.append("Catatan: file tanpa kolom jumlah, jadi jumlah pcs yang terjual tidak diketahui.")
    kal.append("Omzet tertinggi pada {} ({}) dan terendah pada {} ({}).".format(
        tgl_hari(h["hari_terbaik"]["tanggal"]), rupiah(h["hari_terbaik"]["omzet"]),
        tgl_hari(h["hari_terendah"]["tanggal"]), rupiah(h["hari_terendah"]["omzet"])))
    t = h["hari_transaksi_terbanyak"]
    kal.append("Transaksi terbanyak: {} {} per hari, pada {}.".format(
        t["jumlah"], satuan_pesanan, gabung_daftar(tgl_hari(x) for x in t["semua_tanggal_seri"])))
    if h["pola_hari_dalam_minggu"]:
        kal.append(h["pola_hari_dalam_minggu"]["kalimat"])
    if h["baris_dilewati"]:
        kal.append("Catatan: {} baris tidak terbaca dan tidak dihitung.".format(h["baris_dilewati"]))
    return "RINGKASAN SIAP TEMPEL\n" + "\n".join(kal)


def teks_harga(x):
    """'Rp 35.000' atau 'rata-rata Rp 34.500' bila harga per pcs produk itu berbeda-beda antar baris."""
    if x["harga_per_pcs"] is None:
        return "-"
    return ("rata-rata " if x["harga_per_pcs_bervariasi"] else "") + rupiah(x["harga_per_pcs"])


SATUAN_BARIS = "baris transaksi"
CATATAN_TANPA_QTY = ("Tanpa kolom jumlah: jumlah pcs dan harga jual per pcs TIDAK diketahui; yang dihitung per "
                     "produk adalah jumlah baris transaksi (jumlah_baris), bukan pcs. Jangan menyebut pcs, harga per "
                     "pcs, atau terlaris menurut jumlah. Bila pengguna memastikan 1 baris = 1 pcs, jalankan ulang "
                     "dengan --satu-baris-satu-pcs.")
CATATAN_SATU_BARIS = "Tiap baris dihitung 1 pcs (dikonfirmasi pengguna lewat --satu-baris-satu-pcs)."


def susun_sorotan(produk, total, mode_pcs=True):
    """Sorotan produk untuk insight: SEMUA perbandingan dihitung di sini, bukan disimpulkan agent.

    `produk`: daftar dict per produk (semua produk, bukan hanya top). Seri (nilai sama) selalu ikut disebut.
    `mode_pcs` False = file tanpa kolom jumlah: yang dibandingkan jumlah BARIS transaksi, bukan pcs, dan tidak ada
    perbandingan harga per pcs.
    """
    def tanpa_detail(x, *kunci):
        return {k: x[k] for k in ("produk",) + kunci}

    kunci_j = "qty" if mode_pcs else "jumlah_baris"
    satuan = "pcs" if mode_pcs else SATUAN_BARIS
    sorotan = {"dari_jumlah_produk": len(produk), "satuan_jumlah": satuan, "terlaris_omzet": [], "terlaris_qty": [],
               "terlaris_omzet_dan_qty_sama": False if mode_pcs else None,
               "harga_per_pcs_termurah": [], "harga_per_pcs_termahal": []}
    if not mode_pcs:
        sorotan.update({"terlaris_baris": [], "terlaris_omzet_dan_baris_sama": False})
    fakta = []
    if not produk:
        return sorotan, fakta
    maks_omzet = max(x["omzet"] for x in produk)
    maks_j = max(x[kunci_j] for x in produk)
    top_o = [x for x in produk if x["omzet"] == maks_omzet]
    top_j = [x for x in produk if x[kunci_j] == maks_j]
    sama = {x["produk"] for x in top_o} == {x["produk"] for x in top_j}
    if mode_pcs:
        sorotan["terlaris_omzet"] = [tanpa_detail(x, "omzet", "persen_omzet", "qty", "peringkat_qty") for x in top_o]
        sorotan["terlaris_qty"] = [tanpa_detail(x, "qty", "omzet", "peringkat_omzet") for x in top_j]
        sorotan["terlaris_omzet_dan_qty_sama"] = sama
    else:
        sorotan["terlaris_omzet"] = [tanpa_detail(x, "omzet", "persen_omzet", "jumlah_baris") for x in top_o]
        sorotan["terlaris_baris"] = [tanpa_detail(x, "jumlah_baris", "omzet", "peringkat_omzet") for x in top_j]
        sorotan["terlaris_omzet_dan_baris_sama"] = sama

    nama = lambda daftar: gabung_daftar(x["produk"] for x in daftar)
    if len(top_o) == 1:
        fakta.append("Terlaris menurut omzet: {}, {} ({} dari omzet), {} {}.".format(
            top_o[0]["produk"], rupiah(maks_omzet), persen_id(top_o[0]["persen_omzet"]),
            angka_qty(top_o[0][kunci_j]), satuan))
    else:
        fakta.append("Terlaris menurut omzet (seri): {}, masing-masing {} ({} dari omzet).".format(
            gabung_daftar("{} ({} {})".format(x["produk"], angka_qty(x[kunci_j]), satuan) for x in top_o),
            rupiah(maks_omzet), persen_id(top_o[0]["persen_omzet"])))
    label = "Terlaris menurut jumlah" if mode_pcs else "Paling sering tercatat"
    ket = [] if mode_pcs else ["jumlah baris transaksi, bukan pcs"]
    if sama:
        fakta.append("{}{} juga {} ({} {}{}).".format(
            label, " (" + ket[0] + ")" if ket else "", nama(top_j), angka_qty(maks_j), satuan,
            " masing-masing" if len(top_j) > 1 else ""))
    else:
        if len(top_j) > 1:
            ket.append("seri")
        if len(top_j) == 1:
            rinci = "{}; peringkat {} menurut omzet dari {} produk".format(
                rupiah(top_j[0]["omzet"]), top_j[0]["peringkat_omzet"], len(produk))
        else:  # seri: tiap produk disebut lengkap, tanpa "1/3" yang bisa terbaca sebagai pecahan
            rinci = "; ".join("{} {}, peringkat {} menurut omzet".format(x["produk"], rupiah(x["omzet"]),
                                                                          x["peringkat_omzet"]) for x in top_j)
            rinci += "; dari {} produk".format(len(produk))
        fakta.append("{}{}: {}, {} {}{} ({}).".format(
            label, " (" + "; ".join(ket) + ")" if ket else "", nama(top_j), angka_qty(maks_j), satuan,
            " masing-masing" if len(top_j) > 1 else "", rinci))
    if not mode_pcs:
        fakta.append("File tanpa kolom jumlah: jumlah pcs dan harga jual per pcs tidak diketahui, jadi tidak ada "
                     "perbandingan harga per pcs.")
        return sorotan, fakta
    top_q = top_j
    if not sama:
        # Sah secara hitungan: qty A >= qty B dan omzet A < omzet B  =>  harga per pcs A < harga per pcs B.
        a, b = top_q[0], top_o[0]
        if len(top_q) == 1 and len(top_o) == 1 and a["harga_per_pcs"] is not None and b["harga_per_pcs"] is not None:
            fakta.append("{} paling banyak terjual ({} pcs) tetapi omzetnya di bawah {} ({} vs {}) karena harga jual "
                         "per pcs-nya lebih rendah ({} vs {}).".format(
                             a["produk"], angka_qty(a["qty"]), b["produk"], rupiah(a["omzet"]), rupiah(b["omzet"]),
                             teks_harga(a), teks_harga(b)))

    berharga = [x for x in produk if x["harga_per_pcs"] is not None]
    if len(berharga) >= 2:
        h_min = min(x["harga_per_pcs"] for x in berharga)
        h_maks = max(x["harga_per_pcs"] for x in berharga)
        if rupiah(h_min) != rupiah(h_maks):
            murah = [x for x in berharga if rupiah(x["harga_per_pcs"]) == rupiah(h_min)]
            mahal = [x for x in berharga if rupiah(x["harga_per_pcs"]) == rupiah(h_maks)]
            sorotan["harga_per_pcs_termurah"] = [tanpa_detail(x, "harga_per_pcs", "harga_per_pcs_bervariasi", "qty")
                                                 for x in murah]
            sorotan["harga_per_pcs_termahal"] = [tanpa_detail(x, "harga_per_pcs", "harga_per_pcs_bervariasi", "qty")
                                                 for x in mahal]
            fakta.append("Harga jual per pcs dari {} produk: termurah {}; termahal {}.".format(
                len(berharga), gabung_daftar("{} ({})".format(x["produk"], teks_harga(x)) for x in murah),
                gabung_daftar("{} ({})".format(x["produk"], teks_harga(x)) for x in mahal)))
    return sorotan, fakta


def susun_rekap_chat(h, ada_status, satuan_pesanan, top):
    """Rekap siap kirim di chat (Telegram/WA): teks polos tanpa judul Markdown/tabel, SATU rata-rata."""
    p = h["periode"]
    bar = ["Rekap penjualan {} – {}".format(tgl_id(p["awal"]), tgl_id(p["akhir"])), ""]
    dihitung = [(st, v) for st, v in h["per_status"].items() if v["golongan"] == "dihitung"]
    dibuang = [(st, v) for st, v in h["per_status"].items() if v["golongan"] == "dibuang"]
    if ada_status and len(dihitung) == 1:
        bar.append("Omzet: {} dari {} {} {}{}".format(
            rupiah(h["total_omzet"]), h["jumlah_pesanan_dihitung"], satuan_pesanan, dihitung[0][0],
            "" if dihitung[0][1]["final"] else " (belum final, bisa berubah bila batal/retur)"))
    else:
        bar.append("Omzet: {} dari {} {}".format(rupiah(h["total_omzet"]), h["jumlah_pesanan_dihitung"],
                                                 satuan_pesanan))
        if ada_status and dihitung:
            bar.append("Terdiri dari: " + "; ".join(
                "{} {} {} {}{}".format(st, v["jumlah_pesanan"], satuan_pesanan, rupiah(v["omzet"]),
                                       "" if v["final"] else " (belum final, bisa berubah bila batal/retur)")
                for st, v in dihitung))
    r = h["rata_rata_harian"]
    if r["jumlah_hari"] > 1:
        bar.append("Rata-rata per hari: {} (omzet dibagi {} hari kalender; {} hari ada penjualan)".format(
            rupiah(r["nilai"]), r["jumlah_hari"], p["jumlah_hari_ada_penjualan"]))
    if dibuang:
        bar.append("Tidak dihitung (batal/retur): " + "; ".join(
            "{} {} {} {}".format(st, v["jumlah_pesanan"], satuan_pesanan, rupiah(v["omzet"])) for st, v in dibuang))

    mode_pcs = h["satuan_jumlah_produk"] == "pcs"
    bar += ["", "Produk terlaris menurut omzet:"]
    for i, x in enumerate(h["produk_terlaris"][:top], 1):
        if not mode_pcs:   # tanpa kolom jumlah: jumlah baris, BUKAN pcs; harga per pcs tidak diketahui
            rinci = "{} {}".format(x["jumlah_baris"], SATUAN_BARIS)
        elif x["harga_per_pcs"] is None:
            rinci = "{} pcs".format(angka_qty(x["qty"]))
        elif x["harga_per_pcs_bervariasi"]:
            rinci = "{} pcs, rata-rata {}/pcs".format(angka_qty(x["qty"]), rupiah(x["harga_per_pcs"]))
        else:
            rinci = "{} pcs × {}".format(angka_qty(x["qty"]), rupiah(x["harga_per_pcs"]))
        bar.append("{}. {}: {} ({}), {}".format(i, x["produk"], rupiah(x["omzet"]), persen_id(x["persen_omzet"]), rinci))
    if h["jumlah_produk_unik"] > top:
        bar.append("(ditampilkan {} dari {} produk)".format(top, h["jumlah_produk_unik"]))
    s = h["sorotan_produk"]
    if mode_pcs:
        tj, kunci_j, label, sama = s["terlaris_qty"], "qty", "Terlaris menurut jumlah", s["terlaris_omzet_dan_qty_sama"]
    else:
        tj, kunci_j, label, sama = s["terlaris_baris"], "jumlah_baris", "Paling sering tercatat", \
            s["terlaris_omzet_dan_baris_sama"]
    if tj:
        jml = "{} {}{}".format(angka_qty(tj[0][kunci_j]), s["satuan_jumlah"], " masing-masing" if len(tj) > 1 else "")
        nama = gabung_daftar(x["produk"] for x in tj)
        bar.append("{} juga {} ({})".format(label, nama, jml) if sama else "{}: {}, {}".format(label, nama, jml))

    t = h["hari_transaksi_terbanyak"]
    bar += ["", "Hari paling ramai:",
            "Omzet tertinggi {} ({}); terendah {} ({})".format(
                tgl_hari(h["hari_terbaik"]["tanggal"]), rupiah(h["hari_terbaik"]["omzet"]),
                tgl_hari(h["hari_terendah"]["tanggal"]), rupiah(h["hari_terendah"]["omzet"])),
            "{} terbanyak: {} ({} {} per hari{})".format(
                "Pesanan" if satuan_pesanan == "pesanan" else "Transaksi",
                gabung_daftar(tgl_hari(x) for x in t["semua_tanggal_seri"]), t["jumlah"], satuan_pesanan,
                ", seri" if len(t["semua_tanggal_seri"]) > 1 else "")]
    if h["pola_hari_dalam_minggu"]:
        bar.append(h["pola_hari_dalam_minggu"]["kalimat"])

    catatan = []
    if not mode_pcs:
        catatan.append("file tanpa kolom jumlah, jadi jumlah pcs dan harga jual per pcs tidak diketahui "
                       "(yang dihitung jumlah baris transaksi per produk)")
    elif h["sorotan_produk"].get("catatan") == CATATAN_SATU_BARIS:
        catatan.append("tiap baris dihitung 1 pcs (sesuai konfirmasi Anda)")
    if h["baris_tanpa_jumlah"]:
        catatan.append("{} baris tanpa jumlah dihitung 1 pcs".format(h["baris_tanpa_jumlah"]))
    if h["baris_dilewati"]:
        catatan.append("{} baris tidak terbaca dan tidak dihitung ({})".format(
            h["baris_dilewati"], "; ".join("{}: {}".format(k, v) for k, v in h["alasan_dilewati"].items())))
    for utama, varian in h["nama_produk_digabung"].items():
        catatan.append("nama produk {} digabung menjadi \"{}\"".format(
            gabung_daftar('"{}"'.format(v) for v in varian), utama))
    catatan += h["peringatan_awam"]   # setiap isi 'peringatan', dalam bahasa awam
    if catatan:
        bar += ["", "Catatan data: " + "; ".join(catatan)]
    return "\n".join(bar)


def baca_csv(path):
    mentah = open(path, "rb").read()
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
    return list(csv.DictReader(io.StringIO(teks), dialect=dialek)), enc


def keluar_error(data):
    print(json.dumps(data, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Rekap penjualan dari CSV")
    p.add_argument("--versi", "--version", action="version", version="rekap.py " + VERSI)
    p.add_argument("file")
    p.add_argument("--kolom-tanggal", required=True)
    p.add_argument("--kolom-produk", required=True)
    p.add_argument("--kolom-qty")
    p.add_argument("--satu-baris-satu-pcs", action="store_true",
                   help="Tanpa kolom jumlah: anggap tiap baris = 1 pcs. Pakai HANYA bila pengguna sudah memastikannya; "
                        "tanpa opsi ini, file tanpa kolom jumlah dihitung per baris transaksi (bukan pcs).")
    grup = p.add_mutually_exclusive_group(required=True)
    grup.add_argument("--kolom-total", help="Total harga per baris")
    grup.add_argument("--kolom-harga", help="Harga satuan (dikali qty)")
    p.add_argument("--kolom-status", help="Kolom status pesanan (untuk membuang batal/retur)")
    p.add_argument("--kolom-pesanan",
                   help="Kolom nomor pesanan/transaksi (mis. 'No. Pesanan'); jumlah pesanan per hari dihitung unik. "
                        "Tanpa ini, jumlah transaksi = jumlah baris valid.")
    p.add_argument("--abaikan-status",
                   help="Kata status yang dibuang, pisahkan koma. MENGGANTI seluruh daftar bawaan: "
                        + ", ".join(STATUS_BATAL_DEFAULT))
    p.add_argument("--urutan-tanggal", choices=["auto", "dmy", "mdy"], default="auto",
                   help="Urutan tanggal angka: dmy (hari/bulan/tahun, Indonesia) atau mdy (AS)")
    p.add_argument("--top", type=int, default=5)
    a = p.parse_args()

    try:
        baris, encoding = baca_csv(a.file)
    except OSError as e:
        keluar_error({"error": f"Gagal membaca file: {e}"})

    if not baris:
        keluar_error({"error": "File kosong atau hanya berisi judul kolom"})

    kolom = list(baris[0].keys())
    wajib = [a.kolom_tanggal, a.kolom_produk, a.kolom_total or a.kolom_harga]
    wajib += [k for k in (a.kolom_qty, a.kolom_status, a.kolom_pesanan) if k]
    hilang = [k for k in wajib if k not in kolom]
    if hilang:
        keluar_error({"error": "Kolom tidak ditemukan", "hilang": hilang, "kolom_tersedia": kolom})

    abaikan = STATUS_BATAL_DEFAULT
    if a.abaikan_status:
        abaikan = [x.strip().lower() for x in a.abaikan_status.split(",") if x.strip()]

    if a.urutan_tanggal == "auto":
        urutan, ambigu = deteksi_urutan([r.get(a.kolom_tanggal) or "" for r in baris])
    else:
        urutan, ambigu = a.urutan_tanggal, False

    per_produk = defaultdict(lambda: {"qty": 0.0, "baris": 0, "omzet": 0.0, "harga_min": None, "harga_maks": None})
    nama_tampil = {}                 # kunci ternormalisasi -> nama pertama yang ditemui
    varian_nama = defaultdict(set)   # kunci -> semua ejaan asli
    status_dihitung = defaultdict(int)
    per_hari = defaultdict(float)
    baris_per_hari = defaultdict(int)
    pesanan_per_hari = defaultdict(set)
    dilewati = defaultdict(int)
    dibuang_status = defaultdict(int)
    total, n = 0.0, 0
    tanpa_jumlah = 0   # baris dihitung yang selisih kolom jumlahnya kosong (dihitung 1 pcs)

    # Per status (dihitung & dibuang): baris, pesanan unik, nilai. Dibuang per tanggal pesanan.
    per_status = {}
    dibuang_tgl = defaultdict(lambda: {"baris": 0, "pesanan": set(), "nilai": 0.0})
    pesanan_dihitung = set()

    def catat_status(st, golongan, no, nilai):
        d = per_status.setdefault(st, {"golongan": golongan, "baris": 0, "pesanan": set(), "omzet": 0.0,
                                       "baris_nilai_tak_terbaca": 0})
        d["baris"] += 1
        d["pesanan"].add(no)
        if nilai is None:
            d["baris_nilai_tak_terbaca"] += 1
        else:
            d["omzet"] += nilai

    for i, r in enumerate(baris):
        no = ((r.get(a.kolom_pesanan) or "").strip() if a.kolom_pesanan else "") or "(baris %d)" % (i + 2)
        tgl = parse_tanggal(r.get(a.kolom_tanggal), urutan)
        teks_qty = (r.get(a.kolom_qty) or "").strip() if a.kolom_qty else ""
        qty = parse_angka(teks_qty) if teks_qty else 1.0   # qty kosong dianggap 1
        if a.kolom_total:
            nilai = parse_angka(r.get(a.kolom_total))
        else:
            harga = parse_angka(r.get(a.kolom_harga))
            nilai = harga * qty if (harga is not None and qty is not None) else None
        if a.kolom_status:
            st = (r.get(a.kolom_status) or "").strip()
            st_kecil = st.lower()
            if any(k in st_kecil for k in abaikan) and not any(k in st_kecil for k in PENGECUALIAN_STATUS):
                dibuang_status[st] += 1
                catat_status(st, "dibuang", no, nilai)
                kunci_tgl = (tgl.isoformat() if tgl else "(tanggal tidak terbaca)", st)
                dibuang_tgl[kunci_tgl]["baris"] += 1
                dibuang_tgl[kunci_tgl]["pesanan"].add(no)
                dibuang_tgl[kunci_tgl]["nilai"] += nilai or 0.0
                continue
            status_dihitung[st or "(kosong)"] += 1
        if tgl is None:
            dilewati["tanggal tidak terbaca"] += 1
            continue
        if qty is None:
            dilewati["qty tidak valid"] += 1
            continue
        if nilai is None:
            dilewati["harga/total tidak valid atau meragukan"] += 1
            continue
        if a.kolom_status:
            catat_status(st or "(kosong)", "dihitung", no, nilai)
        pesanan_dihitung.add(no)
        if a.kolom_qty and not teks_qty:
            tanpa_jumlah += 1
        asli = " ".join((r.get(a.kolom_produk) or "").split()) or "(tanpa nama)"
        kunci = asli.casefold()
        nama_tampil.setdefault(kunci, asli)
        varian_nama[kunci].add(asli)
        produk = nama_tampil[kunci]
        pp = per_produk[produk]
        pp["qty"] += qty
        pp["baris"] += 1
        pp["omzet"] += nilai
        if qty > 0:
            hs = nilai / qty
            pp["harga_min"] = hs if pp["harga_min"] is None else min(pp["harga_min"], hs)
            pp["harga_maks"] = hs if pp["harga_maks"] is None else max(pp["harga_maks"], hs)
        per_hari[tgl.isoformat()] += nilai
        baris_per_hari[tgl.isoformat()] += 1
        pesanan_per_hari[tgl.isoformat()].add(no)
        total += nilai
        n += 1

    if n == 0:
        keluar_error({"error": "Tidak ada baris valid", "alasan": dict(dilewati),
                      "dibuang_karena_status": dict(dibuang_status)})

    # mode_pcs False = tanpa kolom jumlah dan tanpa konfirmasi 1 baris = 1 pcs: "qty" per produk hanya jumlah baris,
    # jadi harga per pcs, peringkat jumlah, dan terlaris menurut jumlah TIDAK dibuat (bisa salah bila 1 baris > 1 pcs).
    mode_pcs = bool(a.kolom_qty) or a.satu_baris_satu_pcs
    urut = sorted(per_produk.items(), key=lambda x: x[1]["omzet"], reverse=True)
    semua_produk = []
    for k, v in urut:
        semua_produk.append({
            "produk": k, "qty": round(v["qty"], 2), "jumlah_baris": v["baris"], "omzet": round(v["omzet"], 2),
            "persen_omzet": round(v["omzet"] / total * 100, 1) if total else 0,
            # Harga jual per pcs = omzet produk / jumlah terjual (BUKAN margin: data tidak memuat modal/HPP)
            "harga_per_pcs": (round(v["omzet"] / v["qty"], 2) if mode_pcs and v["qty"] > 0 and v["omzet"] > 0
                              else None),
            "harga_per_pcs_bervariasi": (mode_pcs and v["harga_min"] is not None
                                         and v["harga_maks"] - v["harga_min"] >= 1),
            "peringkat_omzet": 1 + sum(1 for _, w in urut if w["omzet"] > v["omzet"]),
            "peringkat_qty": 1 + sum(1 for _, w in urut if w["qty"] > v["qty"]) if mode_pcs else None,
        })
    urut_qty = sorted(semua_produk, key=lambda x: (-x["qty"], -x["omzet"])) if mode_pcs else []
    hari = sorted(per_hari.items())
    terbaik = max(hari, key=lambda x: x[1])
    terendah = min(hari, key=lambda x: x[1])
    if a.kolom_pesanan:
        transaksi_harian = {k: len(pesanan_per_hari[k]) for k, _ in hari}
        satuan_transaksi = "pesanan unik (kolom {})".format(a.kolom_pesanan)
    else:
        transaksi_harian = {k: baris_per_hari[k] for k, _ in hari}
        satuan_transaksi = "baris transaksi"
    maks_trx = max(transaksi_harian.values())
    tgl_maks_trx = [k for k, v in transaksi_harian.items() if v == maks_trx]
    awal, akhir = date.fromisoformat(hari[0][0]), date.fromisoformat(hari[-1][0])
    hari_kalender = (akhir - awal).days + 1

    peringatan = []
    peringatan_awam = []   # padanan tiap peringatan dalam bahasa sehari-hari, untuk "Catatan data" di rekap_chat
    if ambigu and any(POLA_ANGKA_3.match((r.get(a.kolom_tanggal) or "").strip()) for r in baris):
        peringatan.append("Urutan tanggal ambigu (tidak ada tanggal > 12); dianggap hari/bulan/tahun. "
                          "Konfirmasi ke pengguna; jika format AS, jalankan ulang dengan --urutan-tanggal mdy.")
        peringatan_awam.append("urutan tanggal di file belum pasti (semua tanggal bisa dibaca hari/bulan atau "
                               "bulan/hari), jadi dianggap hari/bulan/tahun seperti kebiasaan di Indonesia; mohon "
                               "dicek apakah benar")
    if encoding != "utf-8-sig":
        peringatan.append(f"File dibaca dengan encoding {encoding} (bukan UTF-8).")
        peringatan_awam.append("file ini disimpan dengan format huruf Excel lama, jadi huruf bertanda atau simbol "
                               "khusus pada nama produk mungkin tampil kurang tepat; angkanya tidak terpengaruh")

    hasil = {
        "periode": {"awal": hari[0][0], "akhir": hari[-1][0],
                    "jumlah_hari_kalender": hari_kalender, "jumlah_hari_ada_penjualan": len(hari)},
        "total_omzet": round(total, 2),
        "jumlah_baris_valid": n,
        "rata_rata_omzet_per_hari_kalender": round(total / hari_kalender, 2),
        "rata_rata_omzet_per_hari_berjualan": round(total / len(hari), 2),
        "rata_rata_harian": {"nilai": round(total / hari_kalender, 2), "dasar": "hari kalender",
                             "jumlah_hari": hari_kalender},
        "produk_terlaris": semua_produk[: a.top],
        "produk_terlaris_qty": [{k: x[k] for k in ("produk", "qty", "omzet", "harga_per_pcs", "peringkat_omzet")}
                                for x in urut_qty[: a.top]],
        "jumlah_produk_unik": len(per_produk),
        "hari_terbaik": {"tanggal": terbaik[0], "omzet": round(terbaik[1], 2)},
        "hari_terendah": {"tanggal": terendah[0], "omzet": round(terendah[1], 2)},
        "omzet_harian": {k: round(v, 2) for k, v in hari},
        "hari_transaksi_terbanyak": {"tanggal": tgl_maks_trx[0], "jumlah": maks_trx,
                                     "semua_tanggal_seri": tgl_maks_trx, "satuan": satuan_transaksi},
        "jumlah_transaksi_harian": transaksi_harian,
        "baris_dilewati": sum(dilewati.values()),
        "alasan_dilewati": dict(dilewati),
        "dibuang_karena_status": dict(dibuang_status),
        "status_dihitung": dict(status_dihitung),
        "nama_produk_digabung": {nama_tampil[k]: sorted(v) for k, v in varian_nama.items() if len(v) > 1},
        "urutan_tanggal_dipakai": urutan,
        "peringatan": peringatan,
        "peringatan_awam": peringatan_awam,
        "baris_tanpa_jumlah": tanpa_jumlah,
        "pola_hari_dalam_minggu": hitung_pola_hari(per_hari, awal, akhir),
    }

    hasil["jumlah_pesanan_dihitung"] = len(pesanan_dihitung)
    hasil["satuan_pesanan"] = "pesanan unik" if a.kolom_pesanan else "baris"
    hasil["per_status"] = {
        st: {"golongan": v["golongan"],
             "final": v["golongan"] == "dihitung" and any(k in st.lower() for k in STATUS_FINAL),
             "jumlah_baris": v["baris"],
             "jumlah_pesanan": len(v["pesanan"]),
             "omzet": round(v["omzet"], 2),
             "baris_nilai_tak_terbaca": v["baris_nilai_tak_terbaca"]}
        for st, v in sorted(per_status.items(), key=lambda x: (x[1]["golongan"] != "dihitung", -x[1]["omzet"]))
    }
    hasil["dibuang_per_tanggal"] = [
        {"tanggal": t, "status": st, "jumlah_baris": v["baris"], "jumlah_pesanan": len(v["pesanan"]),
         "nilai": round(v["nilai"], 2)}
        for (t, st), v in sorted(dibuang_tgl.items())
    ]
    # Nama hari untuk semua tanggal yang disebut di teks (pakai persis ini, jangan menebak hari sendiri)
    tgl_perlu = {hasil["hari_terbaik"]["tanggal"], hasil["hari_terendah"]["tanggal"], *tgl_maks_trx,
                 *(x["tanggal"] for x in hasil["dibuang_per_tanggal"])}
    hasil["tanggal_dengan_hari"] = {t: tgl_hari(t) for t in sorted(tgl_perlu)}
    hasil["satuan_jumlah_produk"] = "pcs" if mode_pcs else SATUAN_BARIS
    hasil["sorotan_produk"], hasil["fakta_produk"] = susun_sorotan(semua_produk, total, mode_pcs)
    if not a.kolom_qty:
        hasil["sorotan_produk"]["catatan"] = CATATAN_SATU_BARIS if mode_pcs else CATATAN_TANPA_QTY
    hasil["catatan_tanggal"] = ("Tanggal di dibuang_per_tanggal = isi kolom {} (biasanya tanggal pesanan dibuat), "
                                "bukan tanggal pembatalan.".format(a.kolom_tanggal))
    satuan = "pesanan" if a.kolom_pesanan else "baris transaksi"
    hasil["ringkasan_siap_tempel"] = susun_ringkasan(hasil, bool(a.kolom_status), satuan)
    hasil["rekap_chat"] = susun_rekap_chat(hasil, bool(a.kolom_status), satuan, a.top)
    hasil["versi_script"] = VERSI
    print(json.dumps(hasil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
