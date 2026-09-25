#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hitung uang kompensasi akhir PKWT & ganti rugi pengakhiran dini (hanya library standar Python).

Dasar (dicek 2026-09-25, lihat references/dasar-hukum.md):
  - PP 35/2021 Pasal 15-17 : kompensasi bila masa kerja >= 1 bulan terus-menerus;
                             12 bulan = 1 x upah; kurang/lebih dari 12 bulan = masa kerja / 12 x upah.
                             Diakhiri lebih cepat: kompensasi dihitung dari jangka waktu yang sudah dijalani.
  - UU 13/2003 Pasal 62    : pihak yang mengakhiri PKWT sebelum waktunya membayar ganti rugi sebesar
                             upah sampai batas waktu berakhirnya jangka waktu perjanjian kerja.
  - Putusan MK 168/PUU-XXI/2023: total PKWT termasuk perpanjangan paling lama 5 tahun.

Cara hitung "bulan" (asumsi skill, tidak diatur rinci dalam aturan):
  - Tanggal mulai DAN tanggal akhir sama-sama dihitung sebagai hari kerja (inklusif).
    1 Jan 2026 s.d. 31 Des 2026 = 12 bulan tepat.
  - Masa kerja = bulan penuh + sisa hari; sisa hari dibagi jumlah hari di "bulan berjalan"
    (dari tanggal ulang bulanan terakhir ke tanggal ulang berikutnya). Satu-satunya metode sejak v1.0.2
    (opsi lama '--metode bulan-penuh' dihapus karena membuat dijalani + sisa != panjang kontrak).
  - Rupiah dibulatkan ke rupiah terdekat (setengah ke atas) di langkah akhir.
  - Sisa kontrak (ganti rugi Pasal 62) = panjang periode berjalan - masa dijalani di periode itu (v1.0.1),
    sehingga dijalani + sisa = panjang periode persis.

Contoh:
  python3 hitung_pkwt.py --periode "1 Januari 2026 s.d. 31 Desember 2026" --gaji-pokok 5jt --tunjangan-tetap 500rb
  python3 hitung_pkwt.py --periode "01/01/2025 s.d. 31/12/2025" --periode "01/01/2026 s.d. 30/06/2026" \
      --upah "Rp4.800.000" --berhenti "15/03/2026" --pihak-mengakhiri pengusaha --format json
Windows: ganti `python3` dengan `python` atau `py`.
"""
import argparse
import datetime
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

BATAS_BULAN_TOTAL = 60  # 5 tahun termasuk perpanjangan

NAMA_BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
              "Oktober", "November", "Desember"]
BULAN_ALIAS = {
    "januari": 1, "jan": 1, "january": 1,
    "februari": 2, "pebruari": 2, "feb": 2, "peb": 2, "february": 2,
    "maret": 3, "mar": 3, "march": 3,
    "april": 4, "apr": 4,
    "mei": 5, "may": 5,
    "juni": 6, "jun": 6, "june": 6,
    "juli": 7, "jul": 7, "july": 7,
    "agustus": 8, "agu": 8, "agt": 8, "ags": 8, "aug": 8, "august": 8,
    "september": 9, "sep": 9, "sept": 9,
    "oktober": 10, "okt": 10, "oct": 10, "october": 10,
    "november": 11, "nov": 11, "nop": 11, "nopember": 11,
    "desember": 12, "des": 12, "dec": 12, "december": 12,
}
PEMISAH_PERIODE = re.compile(r"\s+(?:s\.?\s?d\.?|s/d|sampai(?:\s+dengan)?|hingga|until|to)\s+|\s*\.\.\s*|\s+[-–—]\s+",
                             re.IGNORECASE)
_TGL_ANGKA = r"(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/\-.]\d{1,2}[/\-.]\d{4})"
PERIODE_RAPAT = re.compile(r"\s*(" + _TGL_ANGKA + r")\s*[-–—]\s*(" + _TGL_ANGKA + r")\s*")
BATAS_UPAH_JANGGAL = 500000  # upah bulanan di bawah ini hampir pasti salah ketik


class InputError(ValueError):
    pass


# ---------------------------------------------------------------- parsing
def parse_tanggal(teks, nama="tanggal"):
    s = str(teks or "").strip()
    if not s:
        raise InputError("{} kosong. Contoh format: 2026-01-01, 01/01/2026, atau 1 Januari 2026".format(nama))
    s_bersih = re.sub(r"^(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|ahad),?\s+", "", s, flags=re.I)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s_bersih)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})", s_bersih)
        if m:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        else:
            m = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", s_bersih)
            if not m:
                raise InputError("{}: '{}' tidak dikenali. Pakai 2026-01-01, 01/01/2026 (hari/bulan/tahun), "
                                 "atau 1 Januari 2026".format(nama, s))
            nb = m.group(2).lower()
            if nb not in BULAN_ALIAS:
                raise InputError("{}: nama bulan '{}' tidak dikenali".format(nama, m.group(2)))
            d, mo, y = int(m.group(1)), BULAN_ALIAS[nb], int(m.group(3))
    try:
        return datetime.date(y, mo, d)
    except ValueError:
        raise InputError("{}: tanggal '{}' tidak ada di kalender (cek hari/bulan)".format(nama, s))


def parse_rupiah(teks, nama="upah"):
    """'Rp5.000.000', '5jt', '5,5 juta', '500rb', '5000000', '5.000.000,00' -> int rupiah (>= 0)."""
    if teks is None:
        return None
    s = str(teks).strip().lower().replace(" ", "")
    if not s:
        return None
    if s.startswith("-") or s.startswith("rp-") or s.startswith("("):
        raise InputError("{}: nilai negatif '{}' tidak valid".format(nama, teks))
    s = s.replace("rp", "").replace("idr", "")
    s = re.sub(r"[.,]?-+$", "", s)  # akhiran umum "Rp 5.000.000,-" / "5.000.000.-"
    kali = 1
    for akhiran, faktor in (("juta", 10 ** 6), ("jt", 10 ** 6), ("ribu", 10 ** 3), ("rb", 10 ** 3), ("k", 10 ** 3)):
        if s.endswith(akhiran):
            s, kali = s[: -len(akhiran)], faktor
            break
    if not s or not re.fullmatch(r"[0-9.,]+", s):
        raise InputError("{}: '{}' bukan angka rupiah (contoh: Rp5.000.000, 5jt, 500rb)".format(nama, teks))
    if kali > 1:
        # 5,5jt / 5.5jt -> desimal
        s = s.replace(",", ".")
        if s.count(".") > 1:
            raise InputError("{}: '{}' membingungkan; tulis mis. 5,5jt atau 5500000".format(nama, teks))
        nilai = Decimal(s) * kali
    else:
        if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d{1,2})?", s):        # 5.000.000 atau 5.000.000,00
            s = s.replace(".", "").replace(",", ".")
        elif re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d{1,2})?", s):      # 5,000,000 (gaya Inggris)
            s = s.replace(",", "")
        elif re.fullmatch(r"\d+(,\d{1,2})?", s):
            s = s.replace(",", ".")
        elif not re.fullmatch(r"\d+(\.\d{1,2})?", s):
            raise InputError("{}: format '{}' tidak dikenali (contoh: 5.000.000 atau 5000000)".format(nama, teks))
        nilai = Decimal(s)
    return int(nilai.to_integral_value(rounding=ROUND_HALF_UP))


def parse_periode(teks, urutan):
    bagian = PEMISAH_PERIODE.split(str(teks).strip())
    if len(bagian) != 2:
        m = PERIODE_RAPAT.fullmatch(str(teks))  # "1/1/2026-31/12/2026" (tanpa spasi)
        if m:
            bagian = [m.group(1), m.group(2)]
    if len(bagian) != 2:
        raise InputError("periode ke-{} '{}': tulis 'TANGGAL_MULAI s.d. TANGGAL_AKHIR', "
                         "mis. '1 Januari 2026 s.d. 31 Desember 2026'".format(urutan, teks))
    mulai = parse_tanggal(bagian[0], "periode ke-{} (mulai)".format(urutan))
    akhir = parse_tanggal(bagian[1], "periode ke-{} (akhir)".format(urutan))
    if akhir < mulai:
        raise InputError("periode ke-{}: tanggal akhir ({}) lebih awal dari tanggal mulai ({}). "
                         "Mungkin tertukar?".format(urutan, fmt_tgl(akhir), fmt_tgl(mulai)))
    return mulai, akhir


# ---------------------------------------------------------------- tanggal & bulan
def hari_di_bulan(y, m):
    if m == 2:
        return 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28
    return 30 if m in (4, 6, 9, 11) else 31


def tambah_bulan(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    return datetime.date(y, m, min(d.day, hari_di_bulan(y, m)))


def masa(mulai, akhir):
    """Masa dari `mulai` s.d. `akhir` INKLUSIF -> (bulan_penuh, sisa_hari, hari_bulan_berjalan)."""
    batas = akhir + datetime.timedelta(days=1)
    n = (batas.year - mulai.year) * 12 + (batas.month - mulai.month)
    while n > 0 and tambah_bulan(mulai, n) > batas:
        n -= 1
    while tambah_bulan(mulai, n + 1) <= batas:
        n += 1
    jangkar = tambah_bulan(mulai, n)
    berikut = tambah_bulan(mulai, n + 1)
    return n, (batas - jangkar).days, (berikut - jangkar).days


def bulan_desimal(bp, sisa, hari_bln, metode="pecahan"):
    if sisa == 0:
        return Fraction(bp)
    return Fraction(bp) + Fraction(sisa, hari_bln)


def rupiah_bulat(frac):
    return int((Decimal(frac.numerator) / Decimal(frac.denominator)).to_integral_value(rounding=ROUND_HALF_UP))


def fmt_tgl(d):
    return "{} {} {}".format(d.day, NAMA_BULAN[d.month - 1], d.year)


def fmt_rp(n):
    return "Rp" + "{:,}".format(int(n)).replace(",", ".")


def fmt_masa(bp, sisa):
    if sisa:
        return "{} bulan {} hari".format(bp, sisa)
    return "{} bulan".format(bp)


def fmt_frac(f):
    return "{:.4f}".format(float(f)).rstrip("0").rstrip(".").replace(".", ",")


def _saran_upah(teks_asli, up):
    """Saran untuk upah janggal. '4,5' / '4.5' (angka < 1.000 berdesimal) -> kemungkinan juta (Rp4.500.000);
    '4.500' -> kemungkinan ribu (Rp4.500.000)."""
    s = str(teks_asli or "").strip().lower().replace(" ", "").replace("rp", "").replace("idr", "")
    m = re.fullmatch(r"(\d{1,3})(?:[.,](\d{1,2}))?", s)
    if m and (m.group(2) or int(m.group(1)) < 1000) and up < 1000:
        juta = Decimal(m.group(1) + "." + (m.group(2) or "0")) * 10 ** 6
        return " Mungkin maksudnya {} ({} juta)?".format(fmt_rp(int(juta)), s.replace(".", ","))
    if up < 100000:
        return " Mungkin maksudnya {}?".format(fmt_rp(up * 1000))
    return ""


# ---------------------------------------------------------------- inti
def hitung(periode_teks, upah=None, gaji_pokok=None, tunjangan_tetap=None, berhenti=None, pihak=None,
           metode="pecahan", upah_minimum=None, harian=False):
    peringatan = []
    if not periode_teks:
        raise InputError("minimal satu --periode wajib diisi")
    if metode == "bulan-penuh":
        raise InputError("opsi '--metode bulan-penuh' dihapus sejak v1.0.2: membuang sisa hari membuat masa "
                         "dijalani + sisa kontrak tidak sama dengan panjang kontrak. Jalankan tanpa --metode "
                         "(metode pecahan: bulan penuh + sisa hari / hari bulan berjalan).")
    if metode != "pecahan":
        raise InputError("metode hanya 'pecahan' (bawaan); hapus opsi --metode")

    # --- upah
    up = parse_rupiah(upah, "upah")
    gp = parse_rupiah(gaji_pokok, "gaji pokok")
    tt = parse_rupiah(tunjangan_tetap, "tunjangan tetap")
    if up is None and gp is None:
        raise InputError("isi --gaji-pokok (dan --tunjangan-tetap bila ada) atau --upah (upah 1 bulan)")
    if up is not None and gp is not None:
        raise InputError("pilih salah satu: --upah ATAU --gaji-pokok/--tunjangan-tetap, jangan keduanya")
    if up is None:
        tt = tt or 0
        up = gp + tt
        dasar_upah = "gaji pokok {} + tunjangan tetap {}".format(fmt_rp(gp), fmt_rp(tt))
        if up > 0 and Fraction(gp, up) < Fraction(3, 4):
            peringatan.append("Gaji pokok kurang dari 75% dari (gaji pokok + tunjangan tetap). UU 13/2003 Pasal 94 "
                              "mensyaratkan upah pokok paling sedikit 75%. Cek struktur upah.")
    else:
        dasar_upah = "upah 1 bulan (sudah termasuk tunjangan tetap) {}".format(fmt_rp(up))
        if tt:
            raise InputError("--tunjangan-tetap hanya dipakai bersama --gaji-pokok")
    if up <= 0:
        raise InputError("upah 1 bulan harus lebih dari Rp0")
    if up < BATAS_UPAH_JANGGAL:
        saran = _saran_upah(upah if upah is not None else gaji_pokok, up)
        peringatan.append("PERIKSA UPAH: upah 1 bulan tertulis {}, sangat kecil untuk upah bulanan; kemungkinan salah "
                          "ketik.{} Jika memang upah harian/per satuan, isi --upah dengan rata-rata upah per BULAN. "
                          "Angka di bawah dihitung dari {} apa adanya.".format(fmt_rp(up), saran, fmt_rp(up)))
    um = parse_rupiah(upah_minimum, "upah minimum")
    if um is not None and um > 0 and up < um:
        peringatan.append("Upah {} di bawah upah minimum yang Anda isi ({}). Dilarang membayar di bawah upah minimum "
                          "(kecuali usaha mikro/kecil dengan ketentuan khusus, lihat references/dasar-hukum.md)."
                          .format(fmt_rp(up), fmt_rp(um)))
    if harian:
        peringatan.append("PKWT harian lepas: dasar kompensasi memakai rata-rata upah per bulan (isi --upah dengan "
                          "rata-rata). Jika bekerja >= 21 hari/bulan selama 3 bulan berturut-turut atau lebih, "
                          "hubungan kerja demi hukum menjadi PKWTT (PP 35/2021 Pasal 10).")

    # --- periode
    daftar = [parse_periode(t, i + 1) for i, t in enumerate(periode_teks)]
    if daftar != sorted(daftar):
        daftar.sort()
        peringatan.append("Urutan periode diurutkan ulang berdasarkan tanggal mulai.")
    for (m1, a1), (m2, a2) in zip(daftar, daftar[1:]):
        if m2 <= a1:
            raise InputError("periode {} s.d. {} tumpang tindih dengan periode {} s.d. {}. Cek lagi tanggalnya."
                             .format(fmt_tgl(m1), fmt_tgl(a1), fmt_tgl(m2), fmt_tgl(a2)))
        jeda = (m2 - a1).days - 1
        if jeda > 0:
            peringatan.append("Ada jeda {} hari antara {} dan {}. Jika ini pembaruan kontrak (bukan perpanjangan), "
                              "tetap dihitung dalam batas total 5 tahun oleh skill ini (asumsi hati-hati)."
                              .format(jeda, fmt_tgl(a1), fmt_tgl(m2)))

    mulai_pertama, akhir_kontrak = daftar[0][0], daftar[-1][1]
    tb, ts, th = masa(mulai_pertama, akhir_kontrak)
    batas_5th = tambah_bulan(mulai_pertama, BATAS_BULAN_TOTAL) - datetime.timedelta(days=1)
    melebihi_5th = akhir_kontrak > batas_5th
    if melebihi_5th:
        peringatan.append("MELEBIHI BATAS: total PKWT termasuk perpanjangan {} (dari {} s.d. {}), lebih dari 5 tahun. "
                          "Paling lambat berakhir {} (Putusan MK 168/PUU-XXI/2023; PP 35/2021 Pasal 8). "
                          "PKWT yang tidak memenuhi syarat berisiko demi hukum menjadi PKWTT (karyawan tetap)."
                          .format(fmt_masa(tb, ts), fmt_tgl(mulai_pertama), fmt_tgl(akhir_kontrak), fmt_tgl(batas_5th)))
        peringatan.append("Angka kompensasi untuk masa setelah batas 5 tahun ({}) hanya ilustrasi hitungan, bukan "
                          "pengakuan bahwa kontrak itu sah.".format(fmt_tgl(batas_5th)))

    # --- pengakhiran dini
    tgl_berhenti = None
    if berhenti:
        tgl_berhenti = parse_tanggal(berhenti, "tanggal berhenti")
        if tgl_berhenti < mulai_pertama:
            raise InputError("tanggal berhenti ({}) lebih awal dari mulai kontrak ({})"
                             .format(fmt_tgl(tgl_berhenti), fmt_tgl(mulai_pertama)))
        if tgl_berhenti > akhir_kontrak:
            raise InputError("tanggal berhenti ({}) setelah kontrak berakhir ({}); itu bukan pengakhiran dini"
                             .format(fmt_tgl(tgl_berhenti), fmt_tgl(akhir_kontrak)))
        if tgl_berhenti == akhir_kontrak:
            tgl_berhenti = None
            peringatan.append("Tanggal berhenti sama dengan akhir kontrak: dihitung sebagai berakhir normal.")
        else:
            berjalan = [p for p in daftar if p[0] <= tgl_berhenti]
            if berjalan and tgl_berhenti > berjalan[-1][1]:
                raise InputError("tanggal berhenti {} jatuh di jeda antar-periode (tidak ada kontrak berjalan)"
                                 .format(fmt_tgl(tgl_berhenti)))
    if pihak and pihak not in ("pengusaha", "pekerja"):
        raise InputError("--pihak-mengakhiri harus 'pengusaha' atau 'pekerja'")
    if tgl_berhenti and not pihak:
        peringatan.append("Pihak yang mengakhiri belum diisi: arah ganti rugi (siapa membayar siapa) perlu dikonfirmasi.")

    # --- kompensasi per periode
    rincian = []
    total_komp = 0
    for i, (m, a) in enumerate(daftar, 1):
        if tgl_berhenti and m > tgl_berhenti:
            rincian.append({"periode": i, "mulai": m.isoformat(), "akhir_kontrak": a.isoformat(),
                            "dijalani_sampai": None, "masa_kerja": "tidak dijalani", "bulan": "0",
                            "berhak": False, "kompensasi": 0, "catatan": "Periode belum dimulai saat berhenti."})
            continue
        sampai = min(a, tgl_berhenti) if tgl_berhenti else a
        bp, sisa, hb = masa(m, sampai)
        bln = bulan_desimal(bp, sisa, hb, metode)
        berhak = bp >= 1
        if not berhak:
            komp, rumus = 0, "masa kerja < 1 bulan: belum berhak kompensasi (PP 35/2021 Pasal 15 ayat (3))"
        else:
            komp = rupiah_bulat(bln * up / 12)
            if bln == 12:
                rumus = "12 bulan: 1 x upah = {}".format(fmt_rp(up))
            else:
                rumus = "{} / 12 x {} = {}".format(fmt_frac(bln), fmt_rp(up), fmt_rp(komp))
        total_komp += komp
        rincian.append({"periode": i, "mulai": m.isoformat(), "akhir_kontrak": a.isoformat(),
                        "dijalani_sampai": sampai.isoformat(), "masa_kerja": fmt_masa(bp, sisa),
                        "bulan": fmt_frac(bln), "bulan_penuh": bp, "sisa_hari": sisa, "hari_bulan_berjalan": hb,
                        "berhak": berhak, "kompensasi": komp, "rumus": rumus})

    # --- periode berurutan tanpa jeda yang masing-masing < 1 bulan (PERLU REVIEW)
    rantai = []
    for r in rincian:
        if r["dijalani_sampai"] is None:
            continue
        m = datetime.date.fromisoformat(r["mulai"])
        if rantai and m == datetime.date.fromisoformat(rantai[-1][-1]["dijalani_sampai"]) + datetime.timedelta(days=1):
            rantai[-1].append(r)
        else:
            rantai.append([r])
    for grup in rantai:
        if len(grup) < 2 or all(r["berhak"] for r in grup):
            continue
        g_mulai = datetime.date.fromisoformat(grup[0]["mulai"])
        g_akhir = datetime.date.fromisoformat(grup[-1]["dijalani_sampai"])
        gbp, gsisa, ghb = masa(g_mulai, g_akhir)
        if gbp < 1:
            continue
        gbln = bulan_desimal(gbp, gsisa, ghb, metode)
        alt = rupiah_bulat(gbln * up / 12)
        per_periode = sum(r["kompensasi"] for r in grup)
        peringatan.append(
            "PERLU REVIEW (kompensasi Rp0 pada periode pendek): periode ke-{} s.d. ke-{} ({} s.d. {}) berurutan TANPA "
            "jeda. Ada periode yang masing-masing kurang dari 1 bulan sehingga script memberi Rp0 untuk periode itu, "
            "padahal masa kerja terus-menerus gabungannya {}. Dasar: PP 35/2021 Pasal 15 ayat (3), kompensasi "
            "diberikan kepada pekerja yang telah mempunyai masa kerja paling sedikit 1 bulan secara terus-menerus. "
            "Dua kemungkinan tafsir (skill tidak memutuskan): (a) dihitung per periode seperti tabel = {}; "
            "(b) periode berurutan tanpa jeda dijumlahkan sebagai satu masa kerja terus-menerus = {} / 12 x {} = {}. "
            "Konfirmasi ke Disnaker/konsultan hukum sebelum membayar."
            .format(grup[0]["periode"], grup[-1]["periode"], fmt_tgl(g_mulai), fmt_tgl(g_akhir), fmt_masa(gbp, gsisa),
                    fmt_rp(per_periode), fmt_frac(gbln), fmt_rp(up), fmt_rp(alt)))

    # --- ganti rugi Pasal 62
    ganti_rugi = None
    if tgl_berhenti:
        mulai_sisa = tgl_berhenti + datetime.timedelta(days=1)
        # sisa jangka waktu = sampai akhir periode yang sedang berjalan (perpanjangan yang belum dimulai
        # dicatat terpisah karena tafsirnya bisa berbeda)
        periode_jalan = [p for p in daftar if p[0] <= tgl_berhenti <= p[1]][0]
        hari_kalender = (periode_jalan[1] - tgl_berhenti).days
        # Sisa (bulan) = panjang periode berjalan - masa yang sudah dijalani di periode itu, keduanya dengan
        # metode pecahan yang sama, sehingga dijalani + sisa = panjang periode PERSIS (v1.0.1, temuan uji S1).
        tot_bln = bulan_desimal(*masa(periode_jalan[0], periode_jalan[1]), metode="pecahan")
        jln_bln = bulan_desimal(*masa(periode_jalan[0], tgl_berhenti), metode="pecahan")
        bln = tot_bln - jln_bln
        nilai = rupiah_bulat(bln * up)
        arah = {"pengusaha": "pengusaha membayar ke pekerja", "pekerja": "pekerja membayar ke pengusaha"}.get(
            pihak, "pihak yang mengakhiri membayar ke pihak lain")
        # Label = pecahan yang BENAR-BENAR dipakai (v1.0.2), bukan "X bulan Y hari" dari tanggal sisa
        # (yang bisa menghasilkan pecahan berbeda karena panjang bulan berjalan berbeda).
        if hari_kalender == 0:
            sisa_masa = "0 bulan (berhenti tepat di hari terakhir periode berjalan; tidak ada sisa)"
        elif bln.denominator == 1:
            sisa_masa = "{} bulan".format(fmt_frac(bln))
        else:
            sisa_masa = "{} bulan = panjang periode {} bulan - sudah dijalani {} bulan ({} hari kalender)".format(
                fmt_frac(bln), fmt_frac(tot_bln), fmt_frac(jln_bln), hari_kalender)
        ganti_rugi = {
            "sisa_dari": mulai_sisa.isoformat() if hari_kalender else None,
            "sisa_sampai": periode_jalan[1].isoformat() if hari_kalender else None,
            "sisa_hari_kalender": hari_kalender,
            "sisa_masa": sisa_masa, "bulan": fmt_frac(bln), "nilai": nilai, "arah": arah,
            "bulan_periode": fmt_frac(tot_bln), "bulan_dijalani_periode": fmt_frac(jln_bln),
            "bulan_pecahan": [bln.numerator, bln.denominator],
            "rumus": "({} - {}) = {} bulan x {} = {}".format(fmt_frac(tot_bln), fmt_frac(jln_bln), fmt_frac(bln),
                                                         fmt_rp(up), fmt_rp(nilai)),
            "catatan": ("Tidak berlaku bila berakhir karena pekerja meninggal, putusan pengadilan, selesainya "
                        "pekerjaan (PKWT berdasarkan selesainya pekerjaan), atau keadaan yang tercantum di PK/PP/PKB "
                        "(UU 13/2003 Pasal 61 & 62). Sisa (bulan) = panjang periode berjalan - masa yang sudah "
                        "dijalani di periode itu, sehingga dijalani + sisa = panjang kontrak persis."),
        }
        belum = [p for p in daftar if p[0] > tgl_berhenti]
        if belum:
            peringatan.append("Ada {} periode perpanjangan yang belum dimulai saat berhenti; skill tidak memasukkannya "
                              "ke ganti rugi. Minta pendapat Disnaker/konsultan bila dipersoalkan.".format(len(belum)))

    return {
        "upah_sebulan": up, "dasar_upah": dasar_upah, "metode_bulan": metode,
        "total_pkwt": {"mulai": mulai_pertama.isoformat(), "akhir": akhir_kontrak.isoformat(),
                       "masa": fmt_masa(tb, ts), "batas_akhir_5_tahun": batas_5th.isoformat(),
                       "melebihi_5_tahun": melebihi_5th},
        "rincian_kompensasi": rincian, "total_kompensasi": total_komp,
        "pengakhiran_dini": ({"tanggal_berhenti": tgl_berhenti.isoformat(), "pihak_mengakhiri": pihak or "belum diisi"}
                             if tgl_berhenti else None),
        "ganti_rugi_pasal_62": ganti_rugi, "peringatan": peringatan,
    }


# ---------------------------------------------------------------- output
def teks(h):
    b = []
    b.append("HITUNG KOMPENSASI AKHIR PKWT")
    b.append("Upah 1 bulan : {} ({})".format(fmt_rp(h["upah_sebulan"]), h["dasar_upah"]))
    t = h["total_pkwt"]
    b.append("Total PKWT   : {} s.d. {} = {} (batas 5 tahun: s.d. {}) {}".format(
        fmt_tgl(datetime.date.fromisoformat(t["mulai"])), fmt_tgl(datetime.date.fromisoformat(t["akhir"])), t["masa"],
        fmt_tgl(datetime.date.fromisoformat(t["batas_akhir_5_tahun"])),
        "MELEBIHI" if t["melebihi_5_tahun"] else "OK"))
    b.append("")
    b.append("| Periode | Kontrak | Dijalani | Masa kerja | Bulan | Rumus | Kompensasi |")
    b.append("|---|---|---|---|---|---|---|")
    for r in h["rincian_kompensasi"]:
        kontrak = "{} s.d. {}".format(fmt_tgl(datetime.date.fromisoformat(r["mulai"])),
                                       fmt_tgl(datetime.date.fromisoformat(r["akhir_kontrak"])))
        dijalani = fmt_tgl(datetime.date.fromisoformat(r["dijalani_sampai"])) if r["dijalani_sampai"] else "-"
        b.append("| {} | {} | s.d. {} | {} | {} | {} | {} |".format(
            r["periode"], kontrak, dijalani, r["masa_kerja"], r["bulan"], r.get("rumus", r.get("catatan", "")),
            fmt_rp(r["kompensasi"])))
    b.append("")
    b.append("TOTAL KOMPENSASI (dibayar pengusaha ke pekerja): {}".format(fmt_rp(h["total_kompensasi"])))
    g = h["ganti_rugi_pasal_62"]
    if g:
        b.append("")
        b.append("GANTI RUGI PENGAKHIRAN DINI (UU 13/2003 Pasal 62): {}".format(fmt_rp(g["nilai"])))
        if g["sisa_dari"]:
            b.append("  Sisa kontrak {} s.d. {} ({} hari kalender; hari hanya informasi)".format(
                fmt_tgl(datetime.date.fromisoformat(g["sisa_dari"])),
                fmt_tgl(datetime.date.fromisoformat(g["sisa_sampai"])), g["sisa_hari_kalender"]))
            b.append("  Sisa yang dipakai (panjang periode - sudah dijalani): {}".format(g["rumus"]))
        else:
            b.append("  Tidak ada sisa di periode berjalan: berhenti tepat di hari terakhir periode itu -> Rp0. "
                     "Perpanjangan yang belum dimulai tidak dihitung (lihat peringatan).")
        b.append("  Arah: {}".format(g["arah"]))
        b.append("  Catatan: {}".format(g["catatan"]))
    b.append("")
    b.append("Cara hitung bulan: tanggal mulai & akhir ikut dihitung; masa kerja = bulan penuh + sisa hari "
             "/ hari bulan berjalan (metode {}). Sisa kontrak = panjang periode - masa dijalani. Rupiah dibulatkan ke rupiah terdekat.".format(h["metode_bulan"]))
    if h["peringatan"]:
        b.append("")
        b.append("PERINGATAN:")
        for p in h["peringatan"]:
            b.append("- " + p)
    b.append("")
    b.append("Bukan nasihat hukum. Dasar: PP 35/2021 Pasal 15-17, UU 13/2003 Pasal 62 jo. UU 6/2023, Putusan MK "
             "168/PUU-XXI/2023 (dicek 25 September 2026). Konfirmasi ke Disnaker/konsultan hukum.")
    return "\n".join(b)


def buat_parser():
    p = argparse.ArgumentParser(description="Hitung kompensasi akhir PKWT & ganti rugi pengakhiran dini")
    p.add_argument("--periode", action="append", required=True,
                   help="'MULAI s.d. AKHIR' (ulangi untuk perpanjangan), mis. '1 Januari 2026 s.d. 31 Desember 2026'")
    p.add_argument("--gaji-pokok")
    p.add_argument("--tunjangan-tetap")
    p.add_argument("--upah", help="upah 1 bulan bila tidak dipisah (atau rata-rata upah untuk harian lepas)")
    p.add_argument("--berhenti", help="hari kerja terakhir bila kontrak diakhiri sebelum waktunya")
    p.add_argument("--pihak-mengakhiri", choices=["pengusaha", "pekerja"])
    p.add_argument("--metode", default="pecahan", help=argparse.SUPPRESS)  # 'bulan-penuh' dihapus v1.0.2
    p.add_argument("--upah-minimum", help="UMK/UMP yang berlaku (opsional, untuk peringatan)")
    p.add_argument("--harian", action="store_true", help="PKWT harian lepas")
    p.add_argument("--format", default="teks", choices=["teks", "json"])
    return p


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        h = hitung(args.periode, upah=args.upah, gaji_pokok=args.gaji_pokok, tunjangan_tetap=args.tunjangan_tetap,
                   berhenti=args.berhenti, pihak=args.pihak_mengakhiri, metode=args.metode,
                   upah_minimum=args.upah_minimum, harian=args.harian)
    except InputError as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        print(teks(h))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass
    sys.exit(main())
