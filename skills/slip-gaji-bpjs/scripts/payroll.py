#!/usr/bin/env python3
"""Payroll bulanan Indonesia: slip gaji per karyawan + rekap, dengan BPJS, lembur, dan PPh 21 TER.

Dasar (status per 2026-09-23, rincian di references/regulasi.md):
- BPJS Kesehatan: 5% (4% perusahaan, 1% karyawan), batas atas upah Rp12.000.000, batas bawah UMK
  (Perpres 82/2018 jo. Perpres 64/2020 Pasal 30 & 32).
- BPJS Ketenagakerjaan: JHT 3,7% + 2%; JKK 0,24–1,74% (perusahaan); JKM 0,30% (perusahaan);
  JP 2% + 1% dengan batas upah JP (Rp10.547.400 s.d. Feb 2026; Rp11.086.300 mulai Maret 2026).
  Dasar iuran = upah pokok + tunjangan tetap (PP 44/2015 Pasal 19).
- Lembur: PP 35/2021 Pasal 26, 31–32 (1/173 upah sebulan; hari kerja jam ke-1 1,5x, berikutnya 2x).
- PPh 21: PP 58/2023 & PMK 168/2023 (TER; Desember/bulan berhenti dihitung ulang), PMK 105/2025 (DTP 2026).

Contoh:
  python3 payroll.py --data karyawan.csv --periode 2026-09 --perusahaan "CV Maju" --umk 5.396.761 --jkk 0,24
  python3 payroll.py --nama Budi --ptkp K/1 --gaji-pokok 6jt --tunjangan-tetap 1jt --periode 2026-09

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Keluar dengan kode 2 bila input salah.
"""
import argparse
import csv
import html
import io
import json
import os
import re
import sys
import tempfile
from decimal import Decimal

import ter_core as tc

# ---------------------------------------------------------------- konstanta aturan
KES_PERUSAHAAN = Decimal(4)
KES_KARYAWAN = Decimal(1)
BATAS_KES = Decimal(12000000)
JHT_PERUSAHAAN = Decimal("3.7")
JHT_KARYAWAN = Decimal(2)
JKM = Decimal("0.3")
JP_PERUSAHAAN = Decimal(2)
JP_KARYAWAN = Decimal(1)
JKK_RESMI = [Decimal("0.24"), Decimal("0.54"), Decimal("0.89"), Decimal("1.27"), Decimal("1.74")]
JKK_DEFAULT = Decimal("0.24")
# Batas upah JP: (mulai 'YYYY-MM', sampai 'YYYY-MM', nilai)
BATAS_JP = [
    ("2025-03", "2026-02", Decimal(10547400)),
    ("2026-03", "2027-02", Decimal(11086300)),
]
PEMBAGI_LEMBUR = Decimal(173)
MAKS_LEMBUR_HARI_KERJA = Decimal(4)
# Lembur hari istirahat/libur resmi: daftar (jumlah jam, pengali)
TIER_LIBUR = {
    "5": [(8, 2), (1, 3), (3, 4)],      # 5 hari kerja/40 jam: jam 1–8 2x, jam 9 3x, jam 10–12 4x
    "6": [(7, 2), (1, 3), (3, 4)],      # 6 hari kerja/40 jam: jam 1–7 2x, jam 8 3x, jam 9–11 4x
    "6p": [(5, 2), (1, 3), (3, 4)],     # 6 hari kerja, libur resmi jatuh di hari kerja terpendek
}

DISCLAIMER = ("Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Perpres 64/2020 (BPJS Kesehatan), PP 44/2015 & "
              "PP 45/2015 & PP 46/2015 (BPJS Ketenagakerjaan), PP 35/2021 (lembur), PP 58/2023 & PMK 168/2023 "
              "(PPh 21 TER), PMK 105/2025 (DTP), berlaku per 23 September 2026. Untuk kasus khusus hubungi BPJS, "
              "Disnaker, Kring Pajak 1500200, atau konsultan.")

ALIAS = {
    "nama_karyawan": "nama", "karyawan": "nama", "status_ptkp": "ptkp", "ptkp_status": "ptkp",
    "gaji": "gaji_pokok", "upah_pokok": "gaji_pokok", "tunjangan": "tunjangan_tetap",
    "tunj_tetap": "tunjangan_tetap", "tunj_tidak_tetap": "tunjangan_tidak_tetap",
    "tunjangan_tidak_tetap_(transport/makan)": "tunjangan_tidak_tetap", "id": "nik", "no_karyawan": "nik",
    "nip": "nik", "posisi": "jabatan", "lembur": "lembur_rp", "potongan": "potongan_lain", "kasbon": "potongan_lain",
    "jkk": "jkk_persen",
}
YA = {"ya", "y", "yes", "true", "1", "iya"}
TIDAK = {"tidak", "t", "no", "n", "false", "0", "tdk", "gak", "nggak"}


class InputError(Exception):
    pass


def angka(nilai, nama, default=None):
    if nilai is None or str(nilai).strip() == "":
        if default is None:
            raise InputError("{} wajib diisi".format(nama))
        return default
    try:
        return tc.parse_angka(nilai, nama)
    except ValueError as e:
        raise InputError(str(e))


def ya_tidak(nilai, nama, default):
    if nilai is None or str(nilai).strip() == "":
        return default
    s = str(nilai).strip().lower()
    if s in YA:
        return True
    if s in TIDAK:
        return False
    raise InputError("{}: isi 'ya' atau 'tidak' (bukan '{}')".format(nama, nilai))


def persen(d, dasar):
    return tc.bulat_terdekat(Decimal(dasar) * Decimal(d) / 100)


def batas_jp(periode, override):
    if override is not None:
        return angka(override, "--batas-jp")
    for mulai, sampai, nilai in BATAS_JP:
        if mulai <= periode <= sampai:
            return nilai
    raise InputError("Batas upah Jaminan Pensiun untuk periode {} belum tercatat di skill ini (diketahui: Maret 2025 "
                     "s.d. Februari 2027). Cek pengumuman BPJS Ketenagakerjaan lalu isi --batas-jp.".format(periode))


# ---------------------------------------------------------------- lembur
def _daftar_jam(teks, nama):
    if teks is None or str(teks).strip() == "":
        return []
    bagian = [b for b in re.split(r"[+;/|\s]+", str(teks).strip()) if b]
    hasil = []
    for b in bagian:
        pendek = b.lower().endswith("p")
        nilai = b[:-1] if pendek else b
        try:
            jam = tc.parse_angka(nilai, nama)
        except ValueError:
            raise InputError("{}: '{}' bukan jumlah jam. Tulis jam per hari dipisah '+', mis. 2+3+1".format(nama, b))
        if jam <= 0:
            raise InputError("{}: jam lembur harus lebih dari 0".format(nama))
        hasil.append((jam, pendek))
    return hasil


def hitung_lembur(dasar_upah, jam_kerja, jam_libur, hari_kerja, peringatan, label):
    """Kembalikan (total_lembur_dibulatkan, rincian). dasar_upah = upah sebulan dasar lembur."""
    sejam = Decimal(dasar_upah) / PEMBAGI_LEMBUR
    total = Decimal(0)
    rincian = []
    for i, (jam, pendek) in enumerate(jam_kerja, start=1):
        if pendek:
            raise InputError("{}: akhiran 'p' hanya untuk lembur hari libur".format(label))
        if jam > MAKS_LEMBUR_HARI_KERJA:
            peringatan.append("{}: lembur hari kerja ke-{} = {} jam, melebihi batas 4 jam/hari (PP 35/2021 Pasal 26)."
                              .format(label, i, tc.format_persen(jam).rstrip("%")))
        pengali = Decimal("1.5") * min(jam, Decimal(1)) + Decimal(2) * max(jam - 1, Decimal(0))
        total += pengali * sejam
        rincian.append({"jenis": "hari kerja", "jam": jam, "jam_setara": pengali})
    for i, (jam, pendek) in enumerate(jam_libur, start=1):
        kunci = str(hari_kerja) + ("p" if pendek else "")
        if kunci not in TIER_LIBUR:
            raise InputError("{}: akhiran 'p' (libur resmi di hari kerja terpendek) hanya untuk pola 6 hari kerja"
                             .format(label))
        tier = TIER_LIBUR[kunci]
        maks = sum(t[0] for t in tier)
        if jam > maks:
            raise InputError("{}: lembur hari libur ke-{} = {} jam, melebihi {} jam yang diatur PP 35/2021 Pasal 31 "
                             "untuk pola ini".format(label, i, jam, maks))
        sisa, pengali = jam, Decimal(0)
        for n, kali in tier:
            pakai = min(sisa, Decimal(n))
            pengali += pakai * kali
            sisa -= pakai
            if sisa <= 0:
                break
        total += pengali * sejam
        rincian.append({"jenis": "hari libur", "jam": jam, "jam_setara": pengali})
    return tc.bulat_terdekat(total), sejam, rincian


# ---------------------------------------------------------------- hitung satu karyawan
def hitung_karyawan(r, cfg):
    label = r.get("nama") or "baris {}".format(r.get("_baris", "?"))
    if not r.get("nama"):
        raise InputError("{}: kolom 'nama' kosong".format(label))
    peringatan = []
    ptkp = tc.normalisasi_ptkp(r.get("ptkp"))
    kat = tc.kategori_ter(ptkp)
    pokok = angka(r.get("gaji_pokok"), label + ": gaji_pokok")
    tetap = angka(r.get("tunjangan_tetap"), label + ": tunjangan_tetap", Decimal(0))
    tidak_tetap = angka(r.get("tunjangan_tidak_tetap"), label + ": tunjangan_tidak_tetap", Decimal(0))
    bonus = angka(r.get("bonus"), label + ": bonus", Decimal(0)) + angka(r.get("thr"), label + ": thr", Decimal(0))
    pot_lain = angka(r.get("potongan_lain"), label + ": potongan_lain", Decimal(0))
    zakat = angka(r.get("zakat"), label + ": zakat", Decimal(0))
    jkk_p = angka(r.get("jkk_persen"), label + ": jkk_persen", cfg["jkk"])
    ikut_kes = ya_tidak(r.get("ikut_bpjs_kesehatan"), label + ": ikut_bpjs_kesehatan", True)
    ikut_tk = ya_tidak(r.get("ikut_bpjs_tk"), label + ": ikut_bpjs_tk", True)
    ikut_jp = ya_tidak(r.get("ikut_jp"), label + ": ikut_jp", True) and ikut_tk
    dtp = ya_tidak(r.get("dtp"), label + ": dtp", False)
    berhenti = ya_tidak(r.get("berhenti"), label + ": berhenti", False)
    if pokok <= 0:
        raise InputError("{}: gaji_pokok harus lebih dari 0".format(label))

    upah_tetap = pokok + tetap
    if tetap > 0 and pokok < upah_tetap * Decimal("0.75"):
        peringatan.append("{}: gaji pokok kurang dari 75% dari (gaji pokok + tunjangan tetap) — cek PP 36/2021 "
                          "Pasal 7 ayat (2).".format(label))
    if cfg["umk"] is not None and upah_tetap < cfg["umk"]:
        peringatan.append("{}: gaji pokok + tunjangan tetap {} di bawah UMK yang Anda isi ({}). Pastikan tidak "
                          "melanggar ketentuan upah minimum (usaha mikro/kecil punya aturan tersendiri)."
                          .format(label, tc.format_rp(upah_tetap), tc.format_rp(cfg["umk"])))

    # lembur
    jam_kerja = _daftar_jam(r.get("lembur_hari_kerja"), label + ": lembur_hari_kerja")
    jam_libur = _daftar_jam(r.get("lembur_hari_libur"), label + ": lembur_hari_libur")
    lembur_manual = r.get("lembur_rp")
    lembur_info = None
    if (jam_kerja or jam_libur) and lembur_manual not in (None, ""):
        raise InputError("{}: isi jam lembur ATAU lembur_rp, jangan keduanya".format(label))
    if jam_kerja or jam_libur:
        total_upah = upah_tetap + tidak_tetap
        dasar_lembur = upah_tetap
        if tidak_tetap > 0 and upah_tetap < total_upah * Decimal("0.75"):
            dasar_lembur = total_upah * Decimal("0.75")     # PP 35/2021 Pasal 32 ayat (4)
        lembur, sejam, rincian = hitung_lembur(dasar_lembur, jam_kerja, jam_libur, cfg["hari_kerja"], peringatan,
                                               label)
        total_kerja = sum((j for j, _ in jam_kerja), Decimal(0))
        if total_kerja > 18 * 5:
            peringatan.append("{}: total lembur hari kerja {} jam sebulan — cek batas 18 jam/minggu.".format(
                label, total_kerja))
        lembur_info = {"dasar_upah": dasar_lembur, "upah_sejam": sejam, "rincian": rincian}
    else:
        lembur = angka(lembur_manual, label + ": lembur_rp", Decimal(0))

    # BPJS
    dasar_kes = angka(r.get("dasar_bpjs_kesehatan"), label + ": dasar_bpjs_kesehatan", upah_tetap)
    if cfg["umk"] is not None and dasar_kes < cfg["umk"]:
        dasar_kes = cfg["umk"]
    dasar_kes = min(dasar_kes, BATAS_KES)
    dasar_jp = min(upah_tetap, cfg["batas_jp"])
    iur = {
        "kes_perusahaan": persen(KES_PERUSAHAAN, dasar_kes) if ikut_kes else Decimal(0),
        "kes_karyawan": persen(KES_KARYAWAN, dasar_kes) if ikut_kes else Decimal(0),
        "jht_perusahaan": persen(JHT_PERUSAHAAN, upah_tetap) if ikut_tk else Decimal(0),
        "jht_karyawan": persen(JHT_KARYAWAN, upah_tetap) if ikut_tk else Decimal(0),
        "jkk": persen(jkk_p, upah_tetap) if ikut_tk else Decimal(0),
        "jkm": persen(JKM, upah_tetap) if ikut_tk else Decimal(0),
        "jp_perusahaan": persen(JP_PERUSAHAAN, dasar_jp) if ikut_jp else Decimal(0),
        "jp_karyawan": persen(JP_KARYAWAN, dasar_jp) if ikut_jp else Decimal(0),
    }
    if ikut_tk and jkk_p not in JKK_RESMI:
        peringatan.append("{}: tarif JKK {} bukan salah satu tarif PP 44/2015 (0,24/0,54/0,89/1,27/1,74%). Pastikan "
                          "sesuai penetapan BPJS Ketenagakerjaan.".format(label, tc.format_persen(jkk_p)))

    penghasilan = pokok + tetap + tidak_tetap + lembur + bonus
    bruto_pajak = penghasilan + iur["jkk"] + iur["jkm"] + iur["kes_perusahaan"]
    iuran_pengurang = iur["jht_karyawan"] + iur["jp_karyawan"]

    # PPh 21
    bulan = cfg["bulan"]
    masa_terakhir = berhenti or bulan == 12
    pph_info = {"kategori": kat, "bruto": bruto_pajak, "masa_terakhir": masa_terakhir}
    if masa_terakhir:
        wajib = ["bruto_sd_bulan_lalu", "pph21_sd_bulan_lalu"]
        kurang = [k for k in wajib if r.get(k) in (None, "")]
        if kurang:
            raise InputError("{}: bulan ini Masa Pajak Terakhir ({}). PPh 21 wajib dihitung ulang setahun, jadi isi "
                             "kolom {} (total bruto pajak & PPh 21 Januari s.d. bulan lalu)."
                             .format(label, "berhenti bekerja" if berhenti else "Desember", ", ".join(kurang)))
        bruto_lalu = angka(r.get("bruto_sd_bulan_lalu"), label + ": bruto_sd_bulan_lalu")
        pph_lalu = angka(r.get("pph21_sd_bulan_lalu"), label + ": pph21_sd_bulan_lalu")
        if r.get("iuran_sd_bulan_lalu") in (None, "") and ikut_tk and bulan > 1:
            peringatan.append("{}: kolom iuran_sd_bulan_lalu (JHT+JP karyawan Jan s.d. bulan lalu) kosong, dianggap 0 "
                              "— PPh 21 bisa terlalu besar.".format(label))
        iuran_lalu = angka(r.get("iuran_sd_bulan_lalu"), label + ": iuran_sd_bulan_lalu", Decimal(0))
        zakat_lalu = angka(r.get("zakat_sd_bulan_lalu"), label + ": zakat_sd_bulan_lalu", Decimal(0))
        if r.get("jumlah_bulan_kerja") not in (None, ""):
            n_d = angka(r.get("jumlah_bulan_kerja"), label + ": jumlah_bulan_kerja")
        elif r.get("bulan_mulai") not in (None, ""):
            n_d = Decimal(bulan) - angka(r.get("bulan_mulai"), label + ": bulan_mulai") + 1
        else:
            raise InputError("{}: bulan ini Masa Pajak Terakhir — isi kolom jumlah_bulan_kerja (jumlah bulan bekerja "
                             "tahun ini, termasuk bulan ini) atau bulan_mulai (1 bila bekerja sejak Januari). Batas "
                             "biaya jabatan = Rp 500.000 × jumlah bulan, jadi angka ini memengaruhi PPh 21."
                             .format(label))
        if n_d != n_d.to_integral_value() or not 1 <= n_d <= bulan:
            raise InputError("{}: jumlah bulan bekerja harus bilangan bulat 1–{} (dari jumlah_bulan_kerja/bulan_mulai)"
                             .format(label, bulan))
        n = int(n_d)
        mt = tc.hitung_masa_terakhir(bruto_lalu + bruto_pajak, iuran_lalu + iuran_pengurang, zakat_lalu + zakat, n,
                                     ptkp, pph_lalu)
        pph = mt["pph_masa_terakhir"]
        pph_info.update({"metode": "Hitung ulang setahun (Pasal 17)", "tarif": None, "detail": mt})
    else:
        pph, tarif = tc.pph_ter_bulanan(bruto_pajak, kat)
        pph_info.update({"metode": "TER bulanan", "tarif": tarif})

    if dtp:
        if r.get("bruto_tetap_januari") not in (None, ""):
            bruto_tetap = angka(r.get("bruto_tetap_januari"), label + ": bruto_tetap_januari")
        else:
            bruto_tetap = upah_tetap
            peringatan.append("{}: kolom bruto_tetap_januari kosong — syarat DTP dicek memakai gaji pokok + tunjangan "
                              "tetap bulan ini ({}). Syarat resmi memakai bruto tetap & teratur Januari 2026 atau bulan "
                              "pertama kerja.".format(label, tc.format_rp(upah_tetap)))
        ok, alasan = tc.cek_syarat_dtp(cfg["tahun"], bruto_tetap)
        if not ok:
            dtp = False
            peringatan.append("{}: TIDAK memenuhi syarat PPh 21 DTP — {}. PPh 21 dipotong & disetor normal."
                              .format(label, alasan))
    pph_dipotong = max(pph, Decimal(0))
    dtp_tunai = pph_dipotong if dtp else Decimal(0)
    pengembalian = -pph if (pph < 0 and not dtp) else Decimal(0)
    if pph < 0 and dtp:
        peringatan.append("{}: kelebihan PPh 21 DTP {} tidak dikembalikan (PMK 105/2025 Pasal 5 ayat 5).".format(
            label, tc.format_rp(-pph)))
    if pph < 0 and not dtp:
        peringatan.append("{}: PPh 21 lebih potong {} dikembalikan ke karyawan di slip ini.".format(
            label, tc.format_rp(-pph)))

    potongan = {
        "BPJS Kesehatan 1%": iur["kes_karyawan"],
        "BPJS TK - JHT 2%": iur["jht_karyawan"],
        "BPJS TK - JP 1%": iur["jp_karyawan"],
        "PPh 21": pph_dipotong,
        "Zakat": zakat,
        "Potongan lain": pot_lain,
    }
    pendapatan = {
        "Gaji pokok": pokok,
        "Tunjangan tetap": tetap,
        "Tunjangan tidak tetap": tidak_tetap,
        "Lembur": lembur,
        "Bonus/THR": bonus,
        "PPh 21 DTP dibayar tunai": dtp_tunai,
        "Pengembalian kelebihan PPh 21": pengembalian,
    }
    total_pendapatan = sum(pendapatan.values(), Decimal(0))
    total_potongan = sum(potongan.values(), Decimal(0))
    thp = total_pendapatan - total_potongan
    if thp < 0:
        peringatan.append("{}: take home pay negatif — cek potongan lain/kasbon.".format(label))
    iuran_perusahaan = iur["kes_perusahaan"] + iur["jht_perusahaan"] + iur["jkk"] + iur["jkm"] + iur["jp_perusahaan"]
    biaya = penghasilan + iuran_perusahaan
    return {
        "nama": r.get("nama"), "nik": r.get("nik", ""), "jabatan": r.get("jabatan", ""), "ptkp": ptkp,
        "upah_tetap": upah_tetap, "dasar_bpjs_kesehatan": dasar_kes if ikut_kes else Decimal(0),
        "dasar_jp": dasar_jp if ikut_jp else Decimal(0), "jkk_persen": jkk_p,
        "pendapatan": pendapatan, "potongan": potongan, "iuran": iur, "lembur": lembur_info,
        "total_pendapatan": total_pendapatan, "total_potongan": total_potongan, "take_home_pay": thp,
        "iuran_perusahaan": iuran_perusahaan, "biaya_perusahaan": biaya, "pph": pph, "pph_info": pph_info,
        "dtp": dtp, "pph_disetor": Decimal(0) if dtp else pph_dipotong, "peringatan": peringatan,
    }


# ---------------------------------------------------------------- input
def norm_kolom(k):
    k = (k or "").strip().lower().replace(" ", "_").replace("-", "_")
    return ALIAS.get(k, k)


def baca_csv(path):
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except OSError as e:
        raise InputError("File '{}' tidak bisa dibaca: {}".format(path, e.strerror))
    teks = None
    for enc in ("utf-8-sig", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if not teks or not teks.strip():
        raise InputError("File CSV kosong")
    try:
        dialek = csv.Sniffer().sniff(teks[:4096], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    rd = csv.DictReader(io.StringIO(teks), dialect=dialek)
    if not rd.fieldnames:
        raise InputError("File CSV tanpa header")
    kolom = [norm_kolom(f) for f in rd.fieldnames]
    for wajib in ("nama", "ptkp", "gaji_pokok"):
        if wajib not in kolom:
            raise InputError("CSV wajib punya kolom '{}' (ditemukan: {})".format(wajib, ", ".join(rd.fieldnames)))
    baris = []
    for i, row in enumerate(rd, start=2):
        d = {norm_kolom(k): (v or "").strip() for k, v in row.items() if k is not None}
        if not any(d.values()):
            continue
        d["_baris"] = i
        baris.append(d)
    if not baris:
        raise InputError("CSV tidak berisi data karyawan")
    return baris


# ---------------------------------------------------------------- output
def nama_periode(cfg):
    return "{} {}".format(tc.NAMA_BULAN[cfg["bulan"] - 1], cfg["tahun"])


def slip_md(h, cfg):
    o = ["# SLIP GAJI — {}".format(cfg["perusahaan"] or "(nama perusahaan)"),
         "**Periode:** {}  ".format(nama_periode(cfg)),
         "**Nama:** {}{}{}  ".format(h["nama"], " · " + h["jabatan"] if h["jabatan"] else "",
                                     " · ID " + h["nik"] if h["nik"] else ""),
         "**Status PTKP:** {}".format(h["ptkp"]), "",
         "| Pendapatan | Jumlah |", "|---|---:|"]
    for k, v in h["pendapatan"].items():
        if v or k in ("Gaji pokok",):
            o.append("| {} | {} |".format(k, tc.format_rp(v)))
    o += ["| **Total pendapatan** | **{}** |".format(tc.format_rp(h["total_pendapatan"])), "",
          "| Potongan | Jumlah |", "|---|---:|"]
    for k, v in h["potongan"].items():
        if v:
            o.append("| {} | {} |".format(k, tc.format_rp(v)))
    o += ["| **Total potongan** | **{}** |".format(tc.format_rp(h["total_potongan"])), "",
          "### TAKE HOME PAY: {}".format(tc.format_rp(h["take_home_pay"])), ""]
    i = h["iuran"]
    o.append("_Ditanggung perusahaan (tidak memotong gaji): BPJS Kesehatan 4% {}, JHT 3,7% {}, JKK {} {}, JKM 0,3% {}, "
             "JP 2% {}._".format(tc.format_rp(i["kes_perusahaan"]), tc.format_rp(i["jht_perusahaan"]),
                                 tc.format_persen(h["jkk_persen"]), tc.format_rp(i["jkk"]), tc.format_rp(i["jkm"]),
                                 tc.format_rp(i["jp_perusahaan"])))
    p = h["pph_info"]
    if p["masa_terakhir"]:
        o.append("_PPh 21: dihitung ulang setahun (Masa Pajak Terakhir); PPh setahun {} − sudah dipotong {}._".format(
            tc.format_rp(p["detail"]["pph_terutang"]), tc.format_rp(p["detail"]["pph_sudah_dipotong"])))
    else:
        o.append("_PPh 21: TER kategori {} {} × penghasilan bruto pajak {} (termasuk premi JKK, JKM, BPJS Kesehatan "
                 "perusahaan)._".format(p["kategori"], tc.format_persen(p["tarif"]), tc.format_rp(p["bruto"])))
    if h["dtp"]:
        o.append("_PPh 21 Ditanggung Pemerintah (PMK 105/2025) dibayarkan tunai; tidak mengurangi gaji._")
    if h["lembur"]:
        setara = sum((x["jam_setara"] for x in h["lembur"]["rincian"]), Decimal(0))
        o.append("_Lembur: upah sejam = 1/173 × {} = {}; {} jam setara × upah sejam = {}._".format(
            tc.format_rp(h["lembur"]["dasar_upah"]), tc.format_rp(h["lembur"]["upah_sejam"], True),
            tc.format_persen(setara).rstrip("%"), tc.format_rp(h["pendapatan"]["Lembur"])))
    return "\n".join(o)


CSS = """body{font-family:Arial,Helvetica,sans-serif;color:#111;background:#fff;margin:0;padding:16px}
.slip{max-width:720px;margin:0 auto 32px;border:1px solid #999;padding:20px;page-break-after:always}
h1{font-size:18px;margin:0 0 4px}h2{font-size:15px;margin:16px 0 6px}
table{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:8px}
td,th{padding:4px 6px;border-bottom:1px solid #ddd;text-align:left}td.n,th.n{text-align:right}
.thp{font-size:17px;font-weight:bold;border:2px solid #111;padding:8px;margin:12px 0}
.kecil{font-size:11px;color:#444}.info td{border:none;padding:1px 6px}
@media print{body{padding:0}.slip{border:none;margin:0}}"""


def slip_html(h, cfg):
    e = html.escape
    rp = tc.format_rp
    b = ['<div class="slip">', "<h1>SLIP GAJI — {}</h1>".format(e(cfg["perusahaan"] or "(nama perusahaan)")),
         '<table class="info"><tr><td>Periode</td><td>{}</td></tr><tr><td>Nama</td><td>{}</td></tr>'.format(
             e(nama_periode(cfg)), e(h["nama"]))]
    if h["jabatan"]:
        b.append("<tr><td>Jabatan</td><td>{}</td></tr>".format(e(h["jabatan"])))
    if h["nik"]:
        b.append("<tr><td>ID</td><td>{}</td></tr>".format(e(h["nik"])))
    b.append("<tr><td>Status PTKP</td><td>{}</td></tr></table>".format(e(h["ptkp"])))
    b.append('<h2>Pendapatan</h2><table>')
    for k, v in h["pendapatan"].items():
        if v or k == "Gaji pokok":
            b.append('<tr><td>{}</td><td class="n">{}</td></tr>'.format(e(k), rp(v)))
    b.append('<tr><th>Total pendapatan</th><th class="n">{}</th></tr></table>'.format(rp(h["total_pendapatan"])))
    b.append('<h2>Potongan</h2><table>')
    for k, v in h["potongan"].items():
        if v:
            b.append('<tr><td>{}</td><td class="n">{}</td></tr>'.format(e(k), rp(v)))
    b.append('<tr><th>Total potongan</th><th class="n">{}</th></tr></table>'.format(rp(h["total_potongan"])))
    b.append('<div class="thp">TAKE HOME PAY: {}</div>'.format(rp(h["take_home_pay"])))
    i = h["iuran"]
    b.append('<p class="kecil">Ditanggung perusahaan (tidak memotong gaji): BPJS Kesehatan 4% {}, JHT 3,7% {}, JKK {} {}, '
             'JKM 0,3% {}, JP 2% {}.</p>'.format(rp(i["kes_perusahaan"]), rp(i["jht_perusahaan"]),
                                               e(tc.format_persen(h["jkk_persen"])), rp(i["jkk"]), rp(i["jkm"]),
                                               rp(i["jp_perusahaan"])))
    if h["dtp"]:
        b.append('<p class="kecil">PPh 21 Ditanggung Pemerintah (PMK 105/2025) dibayarkan tunai.</p>')
    b.append('<table class="info" style="margin-top:24px"><tr><td>Diterima oleh,<br><br><br>{}</td>'
             '<td class="n">Disetujui oleh,<br><br><br>________________</td></tr></table>'.format(e(h["nama"])))
    b.append('<p class="kecil">{}</p></div>'.format(e(DISCLAIMER)))
    return "\n".join(b)


KOLOM_REKAP = ["nama", "nik", "jabatan", "ptkp", "gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap", "lembur",
               "bonus_thr", "total_pendapatan", "bpjs_kes_karyawan", "jht_karyawan", "jp_karyawan", "pph21_dipotong",
               "pph21_dtp_tunai", "pengembalian_pph21", "zakat", "potongan_lain", "take_home_pay",
               "bpjs_kes_perusahaan", "jht_perusahaan", "jkk", "jkm", "jp_perusahaan", "biaya_total_perusahaan",
               "bruto_pajak", "pph21_disetor"]


def baris_rekap(h):
    p, q, i = h["pendapatan"], h["potongan"], h["iuran"]
    nilai = [h["nama"], h["nik"], h["jabatan"], h["ptkp"], p["Gaji pokok"], p["Tunjangan tetap"],
             p["Tunjangan tidak tetap"], p["Lembur"], p["Bonus/THR"], h["total_pendapatan"], q["BPJS Kesehatan 1%"],
             q["BPJS TK - JHT 2%"], q["BPJS TK - JP 1%"], q["PPh 21"], p["PPh 21 DTP dibayar tunai"],
             p["Pengembalian kelebihan PPh 21"], q["Zakat"], q["Potongan lain"], h["take_home_pay"],
             i["kes_perusahaan"], i["jht_perusahaan"], i["jkk"], i["jkm"], i["jp_perusahaan"], h["biaya_perusahaan"],
             h["pph_info"]["bruto"], h["pph_disetor"]]
    return [tc.angka_json(v) if isinstance(v, Decimal) else v for v in nilai]


def total_rekap(hasil):
    t = {}
    for k in ("total_pendapatan", "take_home_pay", "biaya_perusahaan", "pph_disetor", "iuran_perusahaan"):
        t[k] = sum((h[k] for h in hasil), Decimal(0))
    t["iuran_bpjs_kes"] = sum((h["iuran"]["kes_perusahaan"] + h["iuran"]["kes_karyawan"] for h in hasil), Decimal(0))
    t["iuran_bpjs_tk"] = sum((h["iuran"][k] for h in hasil for k in ("jht_perusahaan", "jht_karyawan", "jkk", "jkm",
                                                                     "jp_perusahaan", "jp_karyawan")), Decimal(0))
    t["dtp_tunai"] = sum((h["pendapatan"]["PPh 21 DTP dibayar tunai"] for h in hasil), Decimal(0))
    return t


def peringatan_folder_sementara(path):
    """Beri PERINGATAN (stderr) bila path keluaran ada di folder sementara sistem. Tidak memblokir."""
    try:
        target = os.path.realpath(path)
        akar = {tempfile.gettempdir(), "/tmp", "/var/tmp"}
        for k in ("TEMP", "TMP", "TMPDIR"):
            if os.environ.get(k):
                akar.add(os.environ[k])
        for a in akar:
            a = os.path.realpath(a)
            if target == a or target.startswith(a.rstrip(os.sep) + os.sep):
                print("PERINGATAN: file keluaran ditulis di folder sementara ({}). Data gaji bersifat pribadi; "
                      "folder sementara bisa dibaca pengguna lain dan terhapus otomatis. Simpan di folder kerja "
                      "yang disepakati.".format(target), file=sys.stderr)
                return True
    except (OSError, ValueError):
        pass
    return False


def tulis_output(hasil, cfg, folder):
    peringatan_folder_sementara(folder)
    os.makedirs(folder, exist_ok=True)
    kode = "{}-{:02d}".format(cfg["tahun"], cfg["bulan"])
    md_path = os.path.join(folder, "slip-gaji-{}.md".format(kode))
    html_path = os.path.join(folder, "slip-gaji-{}.html".format(kode))
    csv_path = os.path.join(folder, "rekap-payroll-{}.csv".format(kode))
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(slip_md(h, cfg) for h in hasil))
        f.write("\n\n_{}_\n".format(DISCLAIMER))
    with open(html_path, "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html lang="id"><head><meta charset="utf-8"><title>Slip Gaji {}</title>'
                '<meta name="viewport" content="width=device-width,initial-scale=1"><style>{}</style></head><body>\n'
                .format(html.escape(nama_periode(cfg)), CSS))
        f.write("\n".join(slip_html(h, cfg) for h in hasil))
        f.write("\n</body></html>\n")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=cfg["pemisah_csv"])
        w.writerow(KOLOM_REKAP)
        for h in hasil:
            w.writerow(baris_rekap(h))
    return {"markdown": md_path, "html": html_path, "csv": csv_path}


def ringkasan_teks(hasil, cfg, file, total):
    o = ["**Rekap payroll {} — {}** ({} karyawan)".format(nama_periode(cfg), cfg["perusahaan"] or "-", len(hasil)), "",
         "| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |",
         "|---|---:|---:|---:|---:|---:|"]
    for h in hasil:
        o.append("| {} | {} | {} | {} | {} | {} |".format(
            h["nama"], tc.format_rp(h["total_pendapatan"]), tc.format_rp(h["total_potongan"]),
            tc.format_rp(h["pph"]) + (" (DTP)" if h["dtp"] else ""), tc.format_rp(h["take_home_pay"]),
            tc.format_rp(h["biaya_perusahaan"])))
    o += ["| **Total** | **{}** | | | **{}** | **{}** |".format(
        tc.format_rp(total["total_pendapatan"]), tc.format_rp(total["take_home_pay"]),
        tc.format_rp(total["biaya_perusahaan"])), "",
        "- Setor BPJS Kesehatan (4% + 1%): {}".format(tc.format_rp(total["iuran_bpjs_kes"])),
        "- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): {}".format(tc.format_rp(total["iuran_bpjs_tk"])),
        "- Setor PPh 21 (tanpa DTP): {}".format(tc.format_rp(total["pph_disetor"]))]
    if total["dtp_tunai"]:
        o.append("- PPh 21 DTP dibayar tunai ke karyawan: {}".format(tc.format_rp(total["dtp_tunai"])))
    o.append("- Batas upah JP dipakai: {} · JKK default {} · UMK: {}".format(
        tc.format_rp(cfg["batas_jp"]), tc.format_persen(cfg["jkk"]),
        tc.format_rp(cfg["umk"]) if cfg["umk"] is not None else "tidak diisi (cek UMK dilewati)"))
    o += ["", "File: " + ", ".join(file.values())]
    pr = [p for h in hasil for p in h["peringatan"]] + cfg["peringatan"]
    if pr:
        o += ["", "⚠️ Peringatan:"] + ["- " + p for p in pr]
    o += ["", "Pembulatan: iuran BPJS & lembur ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan "
          "dengan Coretax/aplikasi BPJS; bila berbeda, ikuti sistem resmi).", "", "_" + DISCLAIMER + "_"]
    return "\n".join(o)


def ke_json(obj):
    if isinstance(obj, Decimal):
        return tc.angka_json(obj)
    if isinstance(obj, dict):
        return {k: ke_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [ke_json(v) for v in obj]
    return obj


# ---------------------------------------------------------------- main
def buat_parser():
    p = argparse.ArgumentParser(description="Slip gaji + BPJS + PPh 21 TER (Indonesia)")
    p.add_argument("--data", help="CSV karyawan (kolom wajib: nama, ptkp, gaji_pokok)")
    p.add_argument("--periode", required=True, help="Periode gaji YYYY-MM, mis. 2026-09")
    p.add_argument("--perusahaan", default="", help="Nama perusahaan di slip")
    p.add_argument("--umk", help="UMK/UMP yang berlaku (isi sendiri dari SK Gubernur)")
    p.add_argument("--jkk", help="Tarif JKK perusahaan dalam persen (default 0,24)")
    p.add_argument("--hari-kerja", choices=["5", "6"], default="5", help="Pola hari kerja per minggu (untuk lembur libur)")
    p.add_argument("--batas-jp", help="Batas upah Jaminan Pensiun (default otomatis sesuai periode)")
    p.add_argument("--out", help="Folder output (default: ./payroll-YYYY-MM)")
    p.add_argument("--pemisah-csv", choices=[";", ","], default=";", help="Pemisah kolom CSV rekap (default ';' untuk Excel Indonesia)")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    # satu karyawan tanpa CSV
    for k in ("nama", "ptkp", "gaji-pokok", "tunjangan-tetap", "tunjangan-tidak-tetap", "lembur-hari-kerja",
              "lembur-hari-libur", "lembur-rp", "bonus", "potongan-lain", "zakat", "jabatan", "nik", "dtp",
              "bruto-tetap-januari", "bulan-mulai",
              "ikut-jp", "berhenti", "bruto-sd-bulan-lalu", "pph21-sd-bulan-lalu", "iuran-sd-bulan-lalu",
              "jumlah-bulan-kerja"):
        p.add_argument("--" + k)
    return p


def jalankan(args):
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", args.periode.strip())
    if not m or not 1 <= int(m.group(2)) <= 12:
        raise InputError("--periode harus berformat YYYY-MM, mis. 2026-09")
    tahun, bulan = int(m.group(1)), int(m.group(2))
    periode = "{}-{:02d}".format(tahun, bulan)
    cfg = {"tahun": tahun, "bulan": bulan, "perusahaan": args.perusahaan,
           "umk": angka(args.umk, "--umk") if args.umk else None,
           "jkk": angka(args.jkk, "--jkk") if args.jkk else JKK_DEFAULT,
           "hari_kerja": args.hari_kerja, "batas_jp": batas_jp(periode, args.batas_jp),
           "pemisah_csv": args.pemisah_csv, "peringatan": []}
    if not args.jkk:
        cfg["peringatan"].append("Tarif JKK belum diisi: dipakai 0,24% (risiko sangat rendah, mis. kantor). Ganti "
                                 "dengan tarif di sertifikat/penetapan BPJS Ketenagakerjaan perusahaan Anda.")
    if cfg["umk"] is None:
        cfg["peringatan"].append("UMK tidak diisi, jadi cek upah minimum dan batas bawah iuran BPJS Kesehatan dilewati.")
    if args.data:
        rows = baca_csv(args.data)
    else:
        if not (args.nama and args.ptkp and args.gaji_pokok):
            raise InputError("Isi --data karyawan.csv, atau untuk satu orang: --nama, --ptkp, --gaji-pokok")
        rows = [{k.replace("-", "_"): getattr(args, k.replace("-", "_")) for k in (
            "nama", "ptkp", "gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap", "lembur_hari_kerja",
            "lembur_hari_libur", "lembur_rp", "bonus", "potongan_lain", "zakat", "jabatan", "nik", "dtp",
            "bruto_tetap_januari", "bulan_mulai", "ikut_jp",
            "berhenti", "bruto_sd_bulan_lalu", "pph21_sd_bulan_lalu", "iuran_sd_bulan_lalu", "jumlah_bulan_kerja")}]
        rows = [{k: (v if v is not None else "") for k, v in rows[0].items()}]
    hasil, galat = [], []
    for r in rows:
        try:
            hasil.append(hitung_karyawan(r, cfg))
        except (InputError, ValueError) as e:
            galat.append(str(e) if str(e).startswith(r.get("nama") or "\0") else "{}: {}".format(
                r.get("nama") or "baris {}".format(r.get("_baris", "?")), e))
    return hasil, galat, cfg


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        hasil, galat, cfg = jalankan(args)
    except (InputError, ValueError) as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    if galat:
        print("ERROR: data berikut harus diperbaiki dulu (tidak ada file yang dibuat):", file=sys.stderr)
        for g in galat:
            print("- " + g, file=sys.stderr)
        return 2
    folder = args.out or "payroll-{}-{:02d}".format(cfg["tahun"], cfg["bulan"])
    file = tulis_output(hasil, cfg, folder)
    total = total_rekap(hasil)
    if args.format == "json":
        print(json.dumps(ke_json({"periode": nama_periode(cfg), "karyawan": hasil, "total": total, "file": file,
                                  "peringatan_umum": cfg["peringatan"], "batas_jp": cfg["batas_jp"]}),
                         ensure_ascii=False, indent=2))
    else:
        print(ringkasan_teks(hasil, cfg, file, total))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
