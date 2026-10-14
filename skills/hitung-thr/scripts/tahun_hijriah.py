#!/usr/bin/env python3
"""Perkiraan tanggal Hijriah dari tanggal Masehi (kalender Hijriah tabular/aritmetika).

Dipakai hitung-thr agar tahun Hijriah hari raya (mis. "Idul Fitri 1448 H") DIHITUNG, bukan ditebak.
Kalender tabular bisa berbeda 1-2 hari dari penetapan resmi (rukyat/hisab Kemenag), jadi TANGGAL Hijriah
hanya perkiraan. Untuk hari raya yang jatuh di tengah tahun Hijriah (Idul Fitri = Syawal, Idul Adha = Zulhijah)
tahun Hijriahnya aman; bila tanggal dekat pergantian tahun (Zulhijah akhir/Muharam awal), script memberi peringatan.

Contoh:
  python3 tahun_hijriah.py 2027-03-10
  python3 tahun_hijriah.py 2027-03-10 --format json
  python3 tahun_hijriah.py 2027-03-20 --cek idul-fitri   # cek tanggal Lebaran dari pengguna (v1.0.5)
  python3 tahun_hijriah.py 2026-10-14 --berikutnya idul-fitri   # perkiraan Lebaran berikutnya (v1.0.10)

--cek idul-fitri|idul-adha: membandingkan tanggal dari pengguna dengan perkiraan 1 Syawal / 10 Zulhijah
(kalender tabular). Bila selisih > 2 hari, script mencetak PERINGATAN berisi perkiraan tanggal hari raya
dan batas bayar THR H-7 menurut perkiraan itu (tanggal resmi tetap menunggu penetapan pemerintah/SKB).

--berikutnya idul-fitri|idul-adha (v1.0.10): perkiraan hari raya pertama yang jatuh PADA/SESUDAH tanggal yang
diberikan (biasanya tanggal hari ini), plus batas bayar H-7. Dipakai bila pengguna tidak menyebut hari raya:
THR dihitung dulu dengan tanggal ini sebagai ASUMSI yang disebut, lalu tanggal pastinya ditanyakan di akhir.

Hanya library standar Python 3.8+. Keluar dengan kode 2 bila input salah.
"""
import argparse
import datetime
import json
import math
import sys

EPOCH_ISLAM = 1948439.5  # JD 1 Muharam 1 H (kalender tabular, epoch sipil 16 Juli 622 M Julian)
BULAN = ["Muharam", "Safar", "Rabiulawal", "Rabiulakhir", "Jumadilawal", "Jumadilakhir", "Rajab", "Syakban",
         "Ramadan", "Syawal", "Zulkaidah", "Zulhijah"]


def jd_dari_masehi(t):
    """Julian Day (tengah malam, .5) dari tanggal Gregorian."""
    y, m, d = t.year, t.month, t.day
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5


def jd_dari_hijriah(y, m, d):
    return d + math.ceil(29.5 * (m - 1)) + (y - 1) * 354 + math.floor((3 + 11 * y) / 30) + EPOCH_ISLAM - 1


def ke_hijriah(t):
    """(tahun, bulan, hari) Hijriah tabular untuk tanggal Masehi t."""
    jd = math.floor(jd_dari_masehi(t)) + 0.5
    y = math.floor((30 * (jd - EPOCH_ISLAM) + 10646) / 10631)
    m = min(12, math.ceil((jd - (29 + jd_dari_hijriah(y, 1, 1))) / 29.5) + 1)
    d = int(jd - jd_dari_hijriah(y, m, 1)) + 1
    return int(y), int(m), d


def hasil(t):
    y, m, d = ke_hijriah(t)
    dekat_pergantian = (m == 12 and d >= 25) or (m == 1 and d <= 5)
    out = {"masehi": t.isoformat(), "tahun_hijriah": y, "bulan_hijriah": BULAN[m - 1], "hari_hijriah": d,
           "teks": "{} {} {} H (perkiraan kalender tabular)".format(d, BULAN[m - 1], y),
           "label_tahun": "{} H".format(y), "tahun_pasti": not dekat_pergantian,
           "catatan": "Tanggal Hijriah tabular bisa berbeda 1-2 hari dari penetapan resmi Kemenag."}
    if dekat_pergantian:
        out["catatan"] += (" Tanggal ini dekat pergantian tahun Hijriah, jadi tahunnya bisa {} atau {} H - "
                           "jangan cantumkan tahun Hijriah tanpa cek kalender resmi.".format(y - 1 if m == 1 else y,
                                                                                         y if m == 1 else y + 1))
    return out


HARI_RAYA = {"idul-fitri": ("Idul Fitri", 10, 1), "idul-adha": ("Idul Adha", 12, 10)}
TOLERANSI_HARI = 2


def masehi_dari_jd(jd):
    return datetime.date(1970, 1, 1) + datetime.timedelta(days=int(math.floor(jd + 0.5) - 2440588))


def cek_hari_raya(t, jenis):
    """Bandingkan tanggal t (dari pengguna) dengan perkiraan tabular Idul Fitri/Idul Adha terdekat."""
    nama, bln, hari = HARI_RAYA[jenis]
    y = ke_hijriah(t)[0]
    calon = [masehi_dari_jd(jd_dari_hijriah(th, bln, hari)) for th in (y - 1, y, y + 1)]
    perkiraan = min(calon, key=lambda c: abs((c - t).days))
    selisih = (t - perkiraan).days
    sesuai = abs(selisih) <= TOLERANSI_HARI
    out = {"hari_raya": nama, "tanggal_pengguna": t.isoformat(), "perkiraan": perkiraan.isoformat(),
           "tahun_hijriah": ke_hijriah(perkiraan)[0], "selisih_hari": selisih, "sesuai": sesuai,
           "batas_bayar_h7_perkiraan": (perkiraan - datetime.timedelta(days=7)).isoformat()}
    if not sesuai:
        h = hasil(t)
        out["peringatan"] = (
            "PERINGATAN: {} = {} {} {} H, bukan {} ({}). {} {} H diperkirakan {} (kalender tabular, "
            "selisih {} hari dari tanggal yang disebut). Tanggal resmi menunggu penetapan pemerintah/SKB libur "
            "nasional. Bila memakai perkiraan ini, batas bayar THR (H-7) = {}.".format(
                t.isoformat(), h["hari_hijriah"], h["bulan_hijriah"], h["tahun_hijriah"],
                "1 Syawal" if jenis == "idul-fitri" else "10 Zulhijah", nama, nama, out["tahun_hijriah"],
                perkiraan.isoformat(), abs(selisih), out["batas_bayar_h7_perkiraan"]))
    return out


def hari_raya_berikutnya(t, jenis):
    """Perkiraan Idul Fitri/Idul Adha (kalender tabular) pertama yang jatuh pada/sesudah tanggal t."""
    nama, bln, hari = HARI_RAYA[jenis]
    y = ke_hijriah(t)[0]
    tgl = masehi_dari_jd(jd_dari_hijriah(y, bln, hari))
    if tgl < t:
        tgl = masehi_dari_jd(jd_dari_hijriah(y + 1, bln, hari))
    h = hasil(tgl)
    return {"hari_raya": nama, "sejak": t.isoformat(), "perkiraan": tgl.isoformat(),
            "tahun_hijriah": h["tahun_hijriah"], "tahun_pasti": h["tahun_pasti"],
            "nama_hari_raya": "{} {}".format(nama, h["label_tahun"] if h["tahun_pasti"] else tgl.year),
            "batas_bayar_h7_perkiraan": (tgl - datetime.timedelta(days=7)).isoformat(),
            "catatan": ("Perkiraan kalender tabular, bisa berbeda 1-2 hari dari penetapan resmi. Tanggal resmi "
                        "menunggu penetapan pemerintah/SKB libur nasional: tulis sebagai ASUMSI di balasan.")}


def main(argv=None):
    p = argparse.ArgumentParser(description="Perkiraan tanggal & tahun Hijriah dari tanggal Masehi.")
    p.add_argument("tanggal", help="Tanggal Masehi YYYY-MM-DD, mis. 2027-03-10")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    p.add_argument("--cek", choices=sorted(HARI_RAYA), help="Cek apakah tanggal ini cocok dengan perkiraan hari raya")
    p.add_argument("--berikutnya", choices=sorted(HARI_RAYA),
                   help="Perkiraan hari raya pertama pada/sesudah tanggal ini (mis. tanggal hari ini) + batas H-7")
    a = p.parse_args(argv)
    try:
        t = datetime.date.fromisoformat(a.tanggal.strip())
    except ValueError:
        print("ERROR: tanggal '{}' tidak valid (pakai format 2027-03-10)".format(a.tanggal), file=sys.stderr)
        return 2
    if not 1900 <= t.year <= 2200:
        print("ERROR: tahun {} di luar rentang 1900-2200".format(t.year), file=sys.stderr)
        return 2
    if a.berikutnya:
        b = hari_raya_berikutnya(t, a.berikutnya)
        if a.format == "json":
            print(json.dumps(b, ensure_ascii=False, indent=2))
        else:
            print("{} berikutnya sejak {} (perkiraan): {}".format(b["hari_raya"], b["sejak"], b["perkiraan"]))
            print("Nama hari raya untuk hitungan: {}".format(b["nama_hari_raya"]))
            print("Batas bayar THR (H-7) menurut perkiraan ini: {}".format(b["batas_bayar_h7_perkiraan"]))
            print("Catatan: " + b["catatan"])
        return 0
    h = hasil(t)
    if a.cek:
        h["cek_hari_raya"] = cek_hari_raya(t, a.cek)
    if a.format == "json":
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        print("{} = {}".format(h["masehi"], h["teks"]))
        print("Tahun Hijriah untuk nama hari raya: {}{}".format(
            h["label_tahun"], "" if h["tahun_pasti"] else " (BELUM PASTI - lihat catatan)"))
        print("Catatan: " + h["catatan"])
        c = h.get("cek_hari_raya")
        if c:
            if c["sesuai"]:
                print("Cek {}: COCOK dengan perkiraan {} (selisih {} hari).".format(
                    c["hari_raya"], c["perkiraan"], abs(c["selisih_hari"])))
            else:
                print(c["peringatan"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
