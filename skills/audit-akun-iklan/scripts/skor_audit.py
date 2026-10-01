#!/usr/bin/env python3
"""Skor kesehatan akun iklan (0-100), prioritas perbaikan, dan rencana 7 hari.

Bagian dari skill `audit-akun-iklan` (Komunitech). Hanya Python standar, semua angka
memakai Decimal. Metode skor diadaptasi dari claude-ads (MIT, lihat ATTRIBUTION.md):
status lulus/gagal/tidak_tahu/tidak_berlaku, bobot keparahan, bobot kategori yang
dinormalkan ulang, dan cakupan bukti. Daftar cek & bobot ada di file CSV di folder ini.

Perintah:
  daftar      [--platform meta,shopee] [--format teks|csv]
  templat     --platform meta,shopee [--keluar jawaban.csv]
  hitung      JAWABAN.csv|.json [--belanja meta=3jt ...] [--mulai 2026-09-28] [--usaha NAMA] [--json]
  roas-impas  --harga 150rb --modal 80rb [--biaya-persen 10] [--biaya-lain 3000] [--roas-aktual 2,3 ...] [--json]

Windows: ganti `python3` dengan `python` atau `py`.
Kode keluar: 0 berhasil, 2 input bermasalah (pesan di stderr).
"""
import argparse
import csv
import io
import json
import re
import sys
from datetime import date, timedelta
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation
from pathlib import Path

SINI = Path(__file__).resolve().parent
FILE_CEK = SINI / "daftar_cek.csv"
FILE_BOBOT = SINI / "bobot_kategori.csv"

PLATFORM = {
    "meta": "Meta Ads (Facebook/Instagram)",
    "tiktok": "TikTok Ads Manager",
    "google": "Google Ads",
    "shopee": "Shopee Ads (juga iklan pencarian marketplace lain)",
    "tiktokshop": "Iklan TikTok Shop / Tokopedia",
}
ALIAS_PLATFORM = {
    "meta": "meta", "facebook": "meta", "fb": "meta", "instagram": "meta", "ig": "meta",
    "tiktok": "tiktok", "tiktokads": "tiktok", "tiktok-ads": "tiktok",
    "google": "google", "googleads": "google", "google-ads": "google",
    "shopee": "shopee", "shopeeads": "shopee", "marketplace": "shopee",
    "tiktokshop": "tiktokshop", "tiktok-shop": "tiktokshop", "tokopedia": "tiktokshop",
    "topads": "tiktokshop", "tiktok-gmvmax": "tiktokshop", "tiktokshop-gmvmax": "tiktokshop",
    "shopee-gmvmax": "shopee", "gmvmax-shopee": "shopee",
}
KATEGORI = {
    "pelacakan": "Pelacakan & konversi",
    "struktur": "Struktur & akses akun",
    "audiens": "Target & audiens",
    "anggaran": "Anggaran & bidding",
    "materi": "Materi iklan",
    "tujuan_halaman": "Halaman tujuan / etalase",
    "frekuensi": "Frekuensi & kelelahan materi",
    "pengecualian": "Pengecualian",
}
BOBOT_KEPARAHAN = {"kritis": Decimal(5), "tinggi": Decimal(3), "sedang": Decimal(1)}
NILAI_KEMUDAHAN = {"mudah": 3, "sedang": 2, "sulit": 1}
BEBAN_HARI = {"mudah": 1, "sedang": 2, "sulit": 3}   # kapasitas 3 unit per hari
KAPASITAS_HARI = 3
HARI_PERBAIKAN = 5
KREDIT = {"lulus": Decimal(1), "sebagian": Decimal("0.5"), "gagal": Decimal(0)}
STATUS_DIKETAHUI = set(KREDIT)
SINONIM_STATUS = {
    "lulus": "lulus", "ya": "lulus", "y": "lulus", "ok": "lulus", "oke": "lulus", "sudah": "lulus",
    "pass": "lulus", "yes": "lulus", "aman": "lulus", "beres": "lulus",
    "gagal": "gagal", "tidak": "gagal", "belum": "gagal", "fail": "gagal", "no": "gagal",
    "sebagian": "sebagian", "partial": "sebagian", "setengah": "sebagian", "kadang": "sebagian",
    "tidak_tahu": "tidak_tahu", "tidaktahu": "tidak_tahu", "tidak tahu": "tidak_tahu", "?": "tidak_tahu",
    "unknown": "tidak_tahu", "": "tidak_tahu", "ragu": "tidak_tahu", "belum dicek": "tidak_tahu",
    "tidak_berlaku": "tidak_berlaku", "tidak berlaku": "tidak_berlaku", "na": "tidak_berlaku",
    "n/a": "tidak_berlaku", "-": "tidak_berlaku", "tidak relevan": "tidak_berlaku",
}
NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
NAMA_BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
SATU_DESIMAL = Decimal("0.1")
VERSI = "1.0.5"
# Cek anggaran yang TIDAK boleh dikerjakan (menaikkan anggaran) sebelum cek batas-untungnya beres.
PRASYARAT = {"T08": "T09", "S07": "S06", "TS05": "TS04"}
BATAS_RASIO_BERLAKU = Decimal("0.5")   # bila < 50% bobot cek berlaku -> maksimal "sementara"


class InputSalah(Exception):
    """Input pengguna tidak bisa diproses; pesan ditujukan ke orang awam."""


# ---------------------------------------------------------------- data ---
def muat_cek():
    with FILE_CEK.open(newline="", encoding="utf-8") as f:
        daftar = list(csv.DictReader(f))
    return {c["id"]: c for c in daftar}, [c["id"] for c in daftar]


def muat_bobot():
    bobot = {}
    with FILE_BOBOT.open(newline="", encoding="utf-8") as f:
        for b in csv.DictReader(f):
            bobot.setdefault(b["platform"], {})[b["kategori"]] = Decimal(b["bobot"])
    return bobot


def periksa_data():
    """Kembalikan daftar masalah konsistensi data cek & bobot (dipakai tes)."""
    cek, urutan = muat_cek()
    bobot = muat_bobot()
    masalah = []
    if len(cek) != len(urutan):
        masalah.append("ID cek ganda")
    for p, kat in bobot.items():
        if sum(kat.values()) != 100:
            masalah.append(f"bobot {p} = {sum(kat.values())}, harus 100")
    for c in cek.values():
        if c["platform"] not in PLATFORM:
            masalah.append(f"{c['id']}: platform {c['platform']}")
        if c["kategori"] not in KATEGORI:
            masalah.append(f"{c['id']}: kategori {c['kategori']}")
        if c["keparahan"] not in BOBOT_KEPARAHAN:
            masalah.append(f"{c['id']}: keparahan {c['keparahan']}")
        if c["kemudahan"] not in NILAI_KEMUDAHAN:
            masalah.append(f"{c['id']}: kemudahan {c['kemudahan']}")
        if c["kategori"] not in bobot.get(c["platform"], {}):
            masalah.append(f"{c['id']}: kategori tanpa bobot")
    for p, kat in bobot.items():
        for k in kat:
            if not any(c["platform"] == p and c["kategori"] == k for c in cek.values()):
                masalah.append(f"bobot {p}/{k} tanpa cek")
    return masalah


# -------------------------------------------------------------- angka ---
def angka(teks, nama="angka"):
    """'150rb', 'Rp 1,5 jt', '3.000.000', '2,5' -> Decimal. Tolak negatif & kosong."""
    s = str(teks).strip().lower().replace("rp", "").replace(" ", "").replace("%", "")
    if not s:
        raise InputSalah(f"{nama} kosong")
    kali = Decimal(1)
    for akhiran, k in (("juta", 10**6), ("jt", 10**6), ("ribu", 10**3), ("rb", 10**3), ("k", 10**3)):
        if s.endswith(akhiran):
            s, kali = s[: -len(akhiran)], Decimal(k)
            break
    if kali != 1:
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    elif re.fullmatch(r"\d{1,3}(,\d{3})+", s):
        s = s.replace(",", "")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+,\d+", s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        nilai = Decimal(s) * kali
    except InvalidOperation:
        raise InputSalah(f"{nama} tidak terbaca sebagai angka: {teks!r}")
    if not nilai.is_finite():
        raise InputSalah(f"{nama} tidak valid: {teks!r}")
    if nilai < 0:
        raise InputSalah(f"{nama} tidak boleh negatif: {teks!r}")
    return nilai


def satu_desimal(d):
    return d.quantize(SATU_DESIMAL, rounding=ROUND_HALF_UP)


def fmt(d):
    """Decimal -> '62,5' (koma desimal Indonesia)."""
    return str(satu_desimal(d)).replace(".", ",")


def rupiah(d):
    n = int(d.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    return "Rp " + f"{n:,}".replace(",", ".")


def label_skor(skor):
    if skor >= 85:
        return "Sehat"
    if skor >= 70:
        return "Cukup, ada yang perlu dibenahi"
    if skor >= 50:
        return "Perlu perbaikan"
    return "Kritis"


def label_platform(x):
    """Label mutu untuk hasil platform/gabungan; None bila bukti belum cukup."""
    if x.get("status") == "bukti_kurang" or x.get("skor") is None:
        return "Bukti belum cukup"
    lab = label_skor(x["skor"])
    if x.get("batas_label") and lab == "Sehat":
        lab = "Cukup, ada yang perlu dibenahi (dibatasi: ada cek kritis ditandai tidak berlaku)"
    return lab


def status_cakupan(cak):
    if cak >= 80:
        return "final"
    if cak >= 60:
        return "sementara"
    return "bukti_kurang"


# -------------------------------------------------------------- input ---
def normal_status(teks):
    s = re.sub(r"\s+", " ", str(teks or "").strip().lower())
    for calon in (s, s.replace("_", " "), s.replace(" ", "_"), s.replace("-", " ")):
        if calon in SINONIM_STATUS:
            return SINONIM_STATUS[calon]
    return None


# Pola kredensial yang tidak boleh ikut tercetak di laporan (password/OTP/token/kartu).
_LABEL_KUAT = (r"(?:kata\s*sandi|sandi|password|passwd|pwd|kode\s*otp|otp|kode\s*verifikasi|kode\s*akses|"
               r"access[\s_-]*token|token\s*akses|api[\s_-]*key|kunci\s*api)")
_LABEL_LEMAH = r"(?:pass|pin|token|secret)"   # wajib diikuti ':' atau '=' (hindari "pin lokasi", "token iklan")
_POLA_RAHASIA = [
    # "password: Klinik#2026", "password nya Klinik#2026", "otp 123456", "pin=1234"
    re.compile(r"(?i)\b(" + _LABEL_KUAT + r")\b(\s*(?:[:=]|adalah|nya)?\s*)([^\s,;]+)"),
    re.compile(r"(?i)\b(" + _LABEL_LEMAH + r")\b(\s*[:=]\s*)([^\s,;]+)"),
    # token Meta (EAA...), kunci gaya sk-/ghp_/AIza, JWT
    re.compile(r"\b(EAA[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,}|"
               r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b"),
    # nomor kartu 13-19 digit (boleh dipisah spasi/tanda hubung, bukan titik ribuan rupiah)
    re.compile(r"(?<![\d.,])(?:\d[ -]?){12,18}\d(?![\d.,])"),
]
SAMARAN = "[DISAMARKAN]"


def samarkan_kredensial(teks):
    """Ganti password/OTP/token/nomor kartu dengan [DISAMARKAN]. Kembalikan (teks, jumlah_samaran)."""
    if not teks:
        return teks, 0
    n = 0
    hasil = teks

    def ganti_label(mo):
        nonlocal n
        nilai = mo.group(3)
        if nilai == SAMARAN:
            return mo.group(0)
        if not re.search(r"[:=]", mo.group(2)) and nilai.isalpha():
            return mo.group(0)   # "OTP belum aktif", "password lama" = kalimat biasa, bukan rahasia
        n += 1
        return mo.group(1) + mo.group(2) + SAMARAN

    def ganti_utuh(mo):
        nonlocal n
        n += 1
        return SAMARAN

    for pola in _POLA_RAHASIA[:2]:
        hasil = pola.sub(ganti_label, hasil)
    for pola in _POLA_RAHASIA[2:]:
        hasil = pola.sub(ganti_utuh, hasil)
    return hasil, n


def baca_jawaban(path):
    """Kembalikan (dict id->(status, catatan), dict belanja dari file, list peringatan)."""
    p = Path(path)
    if not p.is_file():
        raise InputSalah(f"file jawaban tidak ditemukan: {path}")
    if p.suffix.lower() in (".xlsx", ".xls"):
        raise InputSalah("file Excel tidak didukung; buka di Excel/Google Sheets lalu Simpan sebagai CSV")
    teks = p.read_bytes().decode("utf-8-sig", errors="replace")
    if not teks.strip():
        raise InputSalah("file jawaban kosong")
    jawaban, belanja, peringatan = {}, {}, []
    mentah = []
    if p.suffix.lower() == ".json" or teks.lstrip().startswith("{"):
        try:
            data = json.loads(teks)
        except json.JSONDecodeError as e:
            raise InputSalah(f"JSON rusak: {e}")
        if not isinstance(data, dict):
            raise InputSalah("JSON harus berupa objek {\"jawaban\": {...}}")
        isi = data.get("jawaban", data.get("cek", data))
        belanja = data.get("belanja", {}) if isinstance(data.get("belanja", {}), dict) else {}
        if not isinstance(isi, dict):
            raise InputSalah("bagian 'jawaban' harus berupa objek id -> status")
        for k, v in isi.items():
            if k in ("belanja", "usaha"):
                continue
            if isinstance(v, dict):
                mentah.append((k, v.get("status", ""), v.get("catatan", "")))
            else:
                mentah.append((k, v, ""))
    else:
        baris1 = teks.splitlines()[0]
        pemisah = ";" if baris1.count(";") > baris1.count(",") else ","
        r = csv.DictReader(io.StringIO(teks), delimiter=pemisah)
        kolom = {(c or "").strip().lower(): c for c in (r.fieldnames or [])}
        if "id" not in kolom or "status" not in kolom:
            raise InputSalah("CSV jawaban wajib punya kolom 'id' dan 'status' "
                             f"(kolom yang ada: {', '.join(kolom) or '-'}). Buat dengan perintah templat.")
        for b in r:
            cat = b.get(kolom["catatan"], "") if "catatan" in kolom else ""
            lebih = b.get(None)
            if lebih:   # catatan berisi koma tanpa tanda kutip -> sambung lagi, jangan hilang
                cat = ",".join([cat or ""] + [x for x in lebih if x is not None])
            mentah.append((b.get(kolom["id"]), b.get(kolom["status"]), cat))
    for id_, st, cat in mentah:
        id_ = (id_ or "").strip().upper()
        if not id_:
            continue
        s = normal_status(st)
        if s is None:
            peringatan.append(f"{id_}: status {st!r} tidak dikenal -> dianggap tidak_tahu")
            s = "tidak_tahu"
        if id_ in jawaban and jawaban[id_][0] != s:
            raise InputSalah(f"{id_} dijawab dua kali dengan status berbeda "
                             f"({jawaban[id_][0]} vs {s}); pilih salah satu")
        cat, n_samar = samarkan_kredensial((cat or "").strip())
        if n_samar:
            peringatan.append(f"{id_}: catatan berisi password/OTP/token/nomor kartu -> disamarkan. "
                              "Minta pemilik segera ganti password & aktifkan verifikasi 2 langkah.")
        jawaban[id_] = (s, cat)
    if not jawaban:
        raise InputSalah("tidak ada baris jawaban berisi id")
    return jawaban, belanja, peringatan


def parse_belanja(pasangan, dari_file):
    hasil = {}
    for k, v in dari_file.items():
        pk = ALIAS_PLATFORM.get(str(k).strip().lower())
        if not pk:
            raise InputSalah(f"platform belanja tidak dikenal: {k}")
        hasil[pk] = angka(v, f"belanja {k}")
    for item in pasangan or []:
        if "=" not in item:
            raise InputSalah(f"format --belanja harus platform=angka, mis. meta=3jt (dapat {item!r})")
        k, v = item.split("=", 1)
        pk = ALIAS_PLATFORM.get(k.strip().lower())
        if not pk:
            raise InputSalah(f"platform belanja tidak dikenal: {k}")
        hasil[pk] = angka(v, f"belanja {k}")
    return hasil


# ------------------------------------------------------------- hitung ---
def skor_platform(statuses, cek_platform, bobot_kat):
    """statuses: id->status. Kembalikan dict skor (Decimal penuh, belum dibulatkan)."""
    per_kat = {}
    for c in cek_platform:
        st = statuses[c["id"]]
        k = per_kat.setdefault(c["kategori"], {"lulus_w": Decimal(0), "diketahui_w": Decimal(0),
                                                "berlaku_w": Decimal(0)})
        if st == "tidak_berlaku":
            continue
        w = BOBOT_KEPARAHAN[c["keparahan"]]
        k["berlaku_w"] += w
        if st in STATUS_DIKETAHUI:
            k["diketahui_w"] += w
            k["lulus_w"] += w * KREDIT[st]
    total_w = Decimal(0)
    jumlah = Decimal(0)
    kategori = {}
    for nama, k in per_kat.items():
        skor = (Decimal(100) * k["lulus_w"] / k["diketahui_w"]) if k["diketahui_w"] else None
        kategori[nama] = {"skor": skor, "bobot": bobot_kat[nama], **k}
        if skor is not None:
            total_w += bobot_kat[nama]
            jumlah += skor * bobot_kat[nama]
    berlaku = sum((k["berlaku_w"] for k in per_kat.values()), Decimal(0))
    diketahui = sum((k["diketahui_w"] for k in per_kat.values()), Decimal(0))
    skor = (jumlah / total_w) if total_w else None
    cakupan = (Decimal(100) * diketahui / berlaku) if berlaku else None
    return {"skor": skor, "cakupan": cakupan, "kategori": kategori}


def hitung(jawaban, belanja=None, mulai=None, usaha=""):
    cek, urutan = muat_cek()
    bobot = muat_bobot()
    peringatan = []
    tak_dikenal = sorted(i for i in jawaban if i not in cek)
    if tak_dikenal:
        peringatan.append("ID tidak dikenal dilewati: " + ", ".join(tak_dikenal))
    platform_dipakai = [p for p in PLATFORM if any(i in cek and cek[i]["platform"] == p for i in jawaban)]
    if not platform_dipakai:
        raise InputSalah("tidak ada ID cek yang dikenal; buat file jawaban dengan perintah templat")
    belanja = belanja or {}
    for p in belanja:
        if p not in platform_dipakai:
            peringatan.append(f"belanja {PLATFORM[p]} diberikan tapi platform itu tidak diaudit -> diabaikan")

    hasil_platform = {}
    prioritas, cek_dulu = [], []
    for p in platform_dipakai:
        cek_p = [cek[i] for i in urutan if cek[i]["platform"] == p]
        statuses = {}
        belum = 0
        na_tanpa_syarat, kritis_na = [], []
        for c in cek_p:
            if c["id"] in jawaban:
                st = jawaban[c["id"]][0]
                if st == "tidak_berlaku" and not c["tidak_berlaku_jika"].strip():
                    na_tanpa_syarat.append(c["id"])
                    st = "tidak_tahu"
                elif st == "tidak_berlaku" and c["keparahan"] == "kritis":
                    kritis_na.append(c["id"])
                statuses[c["id"]] = st
            else:
                statuses[c["id"]] = "tidak_tahu"
                belum += 1
        if belum:
            peringatan.append(f"{PLATFORM[p]}: {belum} cek belum dijawab -> dihitung 'tidak_tahu'")
        if na_tanpa_syarat:
            peringatan.append(f"{PLATFORM[p]}: {', '.join(na_tanpa_syarat)} ditandai tidak_berlaku padahal cek "
                              "ini selalu berlaku -> dihitung 'tidak_tahu'; isi lulus/gagal/sebagian dengan bukti")
        if kritis_na:
            peringatan.append(f"{PLATFORM[p]}: cek KRITIS {', '.join(kritis_na)} ditandai tidak_berlaku -> "
                              "pastikan syarat 'tidak berlaku jika' benar-benar terpenuhi; label maksimal 'Cukup'")
        s = skor_platform(statuses, cek_p, bobot[p])
        st_cak = status_cakupan(s["cakupan"]) if s["cakupan"] is not None else "tidak_berlaku"
        if s["skor"] is None and st_cak != "tidak_berlaku":
            st_cak = "bukti_kurang"
        total_w = sum((BOBOT_KEPARAHAN[c["keparahan"]] for c in cek_p), Decimal(0))
        berlaku_w = sum((BOBOT_KEPARAHAN[c["keparahan"]] for c in cek_p
                         if statuses[c["id"]] != "tidak_berlaku"), Decimal(0))
        if st_cak == "final" and berlaku_w / total_w < BATAS_RASIO_BERLAKU:
            st_cak = "sementara"
            peringatan.append(f"{PLATFORM[p]}: lebih dari separuh bobot cek ditandai tidak_berlaku -> "
                              "status maksimal 'sementara'")
        if belanja.get(p) == 0:
            peringatan.append(f"belanja {PLATFORM[p]} = 0 -> platform ini tidak berbobot di skor gabungan")
        hasil_platform[p] = {"nama": PLATFORM[p], **s, "status": st_cak,
                             "batas_label": bool(kritis_na),
                             "belanja": belanja.get(p), "jumlah_cek": len(cek_p)}
        for c in cek_p:
            st = statuses[c["id"]]
            catatan = jawaban.get(c["id"], ("", ""))[1]
            if st in ("gagal", "sebagian"):
                uji = dict(statuses)
                uji[c["id"]] = "lulus"
                baru = skor_platform(uji, cek_p, bobot[p])["skor"]
                naik = baru - s["skor"] if s["skor"] is not None else Decimal(0)
                nilai = int(BOBOT_KEPARAHAN[c["keparahan"]]) * NILAI_KEMUDAHAN[c["kemudahan"]]
                prioritas.append({**c, "status": st, "catatan": catatan, "prioritas": nilai, "naik": naik})
            elif st == "tidak_tahu" and c["keparahan"] == "kritis":
                cek_dulu.append({**c, "status": st, "catatan": catatan})

    urut_p = {p: n for n, p in enumerate(PLATFORM)}
    prioritas.sort(key=lambda x: (-x["prioritas"], -x["naik"], -BOBOT_KEPARAHAN[x["keparahan"]],
                                  urut_p[x["platform"]], x["id"]))
    # Jangan menaikkan anggaran sebelum batas untung beres: pindahkan cek anggaran ke belakang prasyaratnya.
    for anak, induk in PRASYARAT.items():
        ids = [x["id"] for x in prioritas]
        if anak in ids and induk in ids:
            peringatan.append(f"{anak} dikerjakan setelah {induk}: jangan menaikkan anggaran selama "
                              f"biaya per hasil/ROAS masih di bawah batas untung ({induk})")
            if ids.index(anak) < ids.index(induk):
                item = prioritas.pop(ids.index(anak))
                prioritas.insert([x["id"] for x in prioritas].index(induk) + 1, item)

    # gabungan: hanya platform yang skornya layak (bukan bukti_kurang)
    layak = [p for p, h in hasil_platform.items() if h["status"] in ("final", "sementara")]
    gabungan = {"skor": None, "status": "bukti_kurang", "cara_bobot": None, "dikeluarkan": []}
    gabungan["dikeluarkan"] = [p for p in hasil_platform if p not in layak]
    if layak:
        pakai_belanja = all(p in belanja for p in layak) and sum(belanja[p] for p in layak) > 0
        if pakai_belanja:
            total = sum(belanja[p] for p in layak)
            porsi = {p: belanja[p] / total for p in layak}
            gabungan["cara_bobot"] = "porsi belanja"
        else:
            porsi = {p: Decimal(1) / Decimal(len(layak)) for p in layak}
            gabungan["cara_bobot"] = "rata (belanja tidak lengkap)" if len(layak) > 1 else "satu platform"
        gabungan["porsi"] = porsi
        gabungan["skor"] = sum(hasil_platform[p]["skor"] * porsi[p] for p in layak)
        sementara = (any(hasil_platform[p]["status"] == "sementara" for p in layak)
                     or gabungan["dikeluarkan"]
                     or (len(layak) > 1 and not pakai_belanja))
        gabungan["status"] = "sementara" if sementara else "final"
        gabungan["batas_label"] = any(hasil_platform[p]["batas_label"] for p in layak)

    rencana = susun_rencana(cek_dulu, prioritas, mulai)
    return {"usaha": usaha, "platform": hasil_platform, "gabungan": gabungan,
            "prioritas": prioritas, "cek_dulu": cek_dulu, "rencana": rencana,
            "peringatan": peringatan}


def susun_rencana(cek_dulu, prioritas, mulai=None):
    antre = [("cek", c, 1) for c in cek_dulu] + [("perbaiki", c, BEBAN_HARI[c["kemudahan"]])
                                                 for c in prioritas]
    hari = {d: [] for d in range(1, HARI_PERBAIKAN + 1)}
    sisa = []
    d, pakai = 1, 0
    for jenis, c, beban in antre:
        if d <= HARI_PERBAIKAN and pakai + beban > KAPASITAS_HARI and pakai > 0:
            d, pakai = d + 1, 0
        if d > HARI_PERBAIKAN:
            sisa.append((jenis, c))
            continue
        hari[d].append((jenis, c))
        pakai += beban
    hasil = []
    for n in range(1, 8):
        tgl = (mulai + timedelta(days=n - 1)) if mulai else None
        label = f"Hari {n}"
        if tgl:
            label += f" ({NAMA_HARI[tgl.weekday()]}, {tgl.day} {NAMA_BULAN[tgl.month - 1]} {tgl.year})"
        if n <= HARI_PERBAIKAN:
            tugas = []
            for jenis, c in hari[n]:
                if jenis == "cek":
                    tugas.append(f"CEK DULU [{c['id']}] {c['judul']} - kumpulkan bukti: {c['bukti']}")
                else:
                    tugas.append(f"PERBAIKI [{c['id']}] {c['judul']} - {c['perbaikan']}")
            if not tugas:
                tugas.append("Tidak ada tugas baru; pantau hasil harian dan catat perubahan.")
        elif n == 6:
            tugas = ["Jangan ubah pengaturan besar; biarkan iklan belajar setelah perbaikan. "
                     "Catat biaya & hasil harian."]
        else:
            tugas = ["Ekspor data iklan 7 hari lalu buat laporan dengan skill laporan-iklan-mingguan; "
                     "audit ulang cek yang sudah diperbaiki dan bandingkan skornya."]
        hasil.append({"hari": n, "label": label, "tugas": tugas})
    return {"hari": hasil, "antrean_berikutnya": [f"[{c['id']}] {c['judul']}" for _, c in sisa]}


# ------------------------------------------------------------- keluaran ---
def teks_laporan(h):
    o = []
    judul = "AUDIT KESEHATAN AKUN IKLAN" + (f" - {h['usaha']}" if h["usaha"] else "")
    o += [judul, "=" * len(judul)]
    g = h["gabungan"]
    if g["skor"] is not None:
        o.append(f"Skor gabungan: {fmt(g['skor'])} / 100 ({label_platform(g)}) - "
                 f"{'FINAL' if g['status'] == 'final' else 'SEMENTARA'}; bobot: {g['cara_bobot']}")
    else:
        o.append("Skor gabungan: BELUM BISA DIBERIKAN - bukti kurang dari 60%. "
                 "Lengkapi jawaban cek bertanda 'tidak_tahu' dulu.")
    if g["dikeluarkan"]:
        o.append("Tidak ikut skor gabungan (bukti < 60%): "
                 + ", ".join(PLATFORM[p] for p in g["dikeluarkan"]))
    o.append("")
    o.append("PER PLATFORM")
    for p, x in h["platform"].items():
        if x["skor"] is None:
            o.append(f"- {x['nama']}: belum ada skor (semua cek belum diketahui/tidak berlaku)")
            continue
        cak = fmt(x["cakupan"]) + "%" if x["cakupan"] is not None else "-"
        if x["status"] == "bukti_kurang":
            o.append(f"- {x['nama']}: BUKTI BELUM CUKUP (bukti {cak}, perlu minimal 60%) - skor & label "
                     "tidak diberikan; lengkapi cek bertanda tidak_tahu dulu")
            continue
        tanda = {"final": "final", "sementara": "sementara", "bukti_kurang": "BUKTI KURANG - jangan dijadikan nilai akun"}[x["status"]]
        bel = f"; belanja {rupiah(x['belanja'])}" if x["belanja"] is not None else ""
        o.append(f"- {x['nama']}: {fmt(x['skor'])}/100 ({label_platform(x)}); bukti {cak} ({tanda}){bel}")
        for k in KATEGORI:
            if k in x["kategori"]:
                kk = x["kategori"][k]
                nilai = fmt(kk["skor"]) if kk["skor"] is not None else "belum tahu"
                o.append(f"    {KATEGORI[k]}: {nilai} (bobot {kk['bobot']})")
    o.append("")
    o.append("PRIORITAS PERBAIKAN (dampak x kemudahan; skor tertinggi dikerjakan dulu)")
    if not h["prioritas"]:
        o.append("- Tidak ada cek yang gagal. Pertahankan & audit ulang bulan depan.")
    for n, c in enumerate(h["prioritas"][:10], 1):
        o.append(f"{n}. [{c['id']}] {c['judul']} - {PLATFORM[c['platform']].split(' (')[0]}; "
                 f"{c['keparahan']}, {c['kemudahan']}; prioritas {c['prioritas']}; "
                 f"skor platform naik +{fmt(c['naik'])} bila beres"
                 + (" (status: sebagian)" if c["status"] == "sebagian" else ""))
        o.append(f"   Perbaikan: {c['perbaikan']}")
        if c["catatan"]:
            o.append(f"   Catatan audit: {c['catatan']}")
    if len(h["prioritas"]) > 10:
        o.append(f"   ...dan {len(h['prioritas']) - 10} perbaikan lain (lihat --json atau antrean).")
    if h["cek_dulu"]:
        o.append("")
        o.append("CEK DULU (keparahan kritis tapi belum ada bukti)")
        for c in h["cek_dulu"]:
            o.append(f"- [{c['id']}] {c['judul']} - bukti: {c['bukti']}")
    o.append("")
    o.append("RENCANA 7 HARI (maks. kira-kira 1-2 jam kerja per hari)")
    for d in h["rencana"]["hari"]:
        o.append(d["label"] + ":")
        for t in d["tugas"]:
            o.append(f"  - {t}")
    if h["rencana"]["antrean_berikutnya"]:
        o.append("Antrean minggu berikutnya: " + "; ".join(h["rencana"]["antrean_berikutnya"]))
    if h["peringatan"]:
        o.append("")
        o.append("CATATAN")
        for w in h["peringatan"]:
            o.append(f"- {w}")
    o.append("")
    o.append("Aturan aman: ubah anggaran paling banyak 20% per 2-3 hari dan jangan ubah banyak hal "
             "sekaligus di satu kampanye. Skor ini alat bantu prioritas, bukan jaminan hasil iklan.")
    return "\n".join(o)


def ke_json(h):
    def d(x):
        return None if x is None else str(satu_desimal(x))
    out = {"versi": VERSI, "usaha": h["usaha"], "gabungan": {
        "skor": d(h["gabungan"]["skor"]), "status": h["gabungan"]["status"],
        "label": label_platform(h["gabungan"]),
        "cara_bobot": h["gabungan"]["cara_bobot"], "dikeluarkan": h["gabungan"]["dikeluarkan"],
        "porsi": {p: str(v.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
                  for p, v in h["gabungan"].get("porsi", {}).items()}},
        "platform": {}, "prioritas": [], "cek_dulu": [c["id"] for c in h["cek_dulu"]],
        "rencana": h["rencana"], "peringatan": h["peringatan"]}
    for p, x in h["platform"].items():
        kurang = x["status"] == "bukti_kurang"
        out["platform"][p] = {"nama": x["nama"], "skor": None if kurang else d(x["skor"]),
                              "skor_indikatif": d(x["skor"]) if kurang else None,
                              "label": label_platform(x), "cakupan_bukti": d(x["cakupan"]),
                              "status": x["status"],
                              "belanja": None if x["belanja"] is None else str(x["belanja"].quantize(Decimal(1), rounding=ROUND_HALF_UP)),
                              "kategori": {k: {"skor": d(v["skor"]), "bobot": str(v["bobot"])}
                                           for k, v in x["kategori"].items()}}
    for c in h["prioritas"]:
        out["prioritas"].append({"id": c["id"], "platform": c["platform"], "judul": c["judul"],
                                 "status": c["status"], "keparahan": c["keparahan"],
                                 "kemudahan": c["kemudahan"], "prioritas": c["prioritas"],
                                 "naik_skor": d(c["naik"]), "perbaikan": c["perbaikan"]})
    return json.dumps(out, ensure_ascii=False, indent=2)


def roas_impas(harga, modal, persen=Decimal(0), lain=Decimal(0)):
    if harga <= 0:
        raise InputSalah("harga jual harus lebih dari 0")
    if persen >= 100:
        raise InputSalah("persen biaya platform harus di bawah 100")
    biaya_platform = (harga * persen / 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    laba_mentah = harga - modal - biaya_platform - lain
    if laba_mentah <= 0:
        raise InputSalah(f"produk ini sudah rugi/impas sebelum iklan (laba kotor {rupiah(laba_mentah)} per pesanan); "
                         "jangan diiklankan sebelum harga/modal dibenahi")
    # Dibulatkan KE BAWAH (konservatif): batas biaya iklan tidak boleh lebih besar dari laba sebenarnya.
    laba = laba_mentah.quantize(Decimal(1), rounding=ROUND_FLOOR)
    if laba < 1:
        raise InputSalah(f"laba kotor per pesanan kurang dari Rp1 ({laba_mentah} rupiah); ROAS impas tidak masuk "
                         "akal untuk iklan. Periksa angka harga/modal/biaya, atau benahi harga dulu")
    roas = (harga / laba).quantize(Decimal("0.01"), rounding=ROUND_CEILING)
    return {"harga": harga, "modal": modal, "biaya_platform": biaya_platform, "biaya_lain": lain,
            "laba_kotor": laba, "biaya_iklan_maks_per_pesanan": laba, "roas_impas": roas}


def banding_roas(r, daftar_roas):
    """Bandingkan tiap ROAS (aktual/target) yang disebut pengguna dengan titik impas.
    Status dihitung persis (tanpa pembulatan): biaya iklan per pesanan = harga / ROAS;
    lebih besar dari laba kotor = RUGI, sama = IMPAS, lebih kecil = UNTUNG.
    Nominal ditampilkan dibulatkan ke rupiah terdekat."""
    hasil = []
    for x in daftar_roas:
        if x <= 0:
            raise InputSalah("ROAS aktual/target harus lebih dari 0")
        biaya = r["harga"] / x
        selisih = r["laba_kotor"] - biaya
        st = "RUGI" if selisih < 0 else ("IMPAS" if selisih == 0 else "UNTUNG")
        hasil.append({"roas": x, "status": st,
                      "biaya_iklan_per_pesanan": biaya.quantize(Decimal(1), rounding=ROUND_HALF_UP),
                      "laba_setelah_iklan_per_pesanan": selisih.quantize(Decimal(1), rounding=ROUND_HALF_UP)})
    return hasil


# ---------------------------------------------------------------- CLI ---
def pilih_platform(teks):
    if not teks:
        return list(PLATFORM)
    hasil = []
    for t in teks.split(","):
        k = ALIAS_PLATFORM.get(t.strip().lower())
        if not k:
            petunjuk = (" GMV Max ada di Shopee dan TikTok Shop: tulis shopee atau tiktokshop."
                        if "gmv" in t.lower() else "")
            raise InputSalah(f"platform tidak dikenal: {t!r}. Pilihan: {', '.join(PLATFORM)}.{petunjuk}")
        if k not in hasil:
            hasil.append(k)
    return hasil


def main(argv=None):
    ap = argparse.ArgumentParser(description=f"Skor audit kesehatan akun iklan (Komunitech) v{VERSI}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("daftar", help="tampilkan daftar cek")
    a.add_argument("--platform")
    a.add_argument("--format", choices=["teks", "csv"], default="teks")
    a = sub.add_parser("templat", help="buat CSV jawaban kosong")
    a.add_argument("--platform", required=True)
    a.add_argument("--keluar")
    a = sub.add_parser("hitung", help="hitung skor dari file jawaban")
    a.add_argument("jawaban")
    a.add_argument("--belanja", action="append", help="platform=angka, mis. meta=3jt (bisa diulang)")
    a.add_argument("--mulai", help="tanggal mulai rencana 7 hari, YYYY-MM-DD")
    a.add_argument("--usaha", default="")
    a.add_argument("--json", action="store_true")
    a = sub.add_parser("roas-impas", help="hitung ROAS/ROI impas & biaya iklan maks per pesanan")
    a.add_argument("--harga", required=True)
    a.add_argument("--modal", required=True)
    a.add_argument("--biaya-persen", default="0", help="persen biaya admin/layanan/komisi, mis. 10 atau 10,5")
    a.add_argument("--biaya-lain", default="0", help="biaya lain per pesanan (kemas, dll.)")
    a.add_argument("--roas-aktual", action="append", default=[],
                   help="ROAS aktual/target yang disebut pengguna, mis. 2,3 (bisa diulang); dicetak RUGI/IMPAS/UNTUNG")
    a.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.cmd in ("daftar", "templat"):
            cek, urutan = muat_cek()
            plat = pilih_platform(args.platform)
            baris = [cek[i] for i in urutan if cek[i]["platform"] in plat]
            if args.cmd == "templat" or args.format == "csv":
                buf = io.StringIO()
                w = csv.writer(buf, lineterminator="\n")
                if args.cmd == "templat":
                    w.writerow(["id", "status", "catatan", "platform", "judul", "lulus_jika", "bukti"])
                    for c in baris:
                        w.writerow([c["id"], "", "", c["platform"], c["judul"], c["lulus_jika"], c["bukti"]])
                else:
                    w.writerow(list(baris[0].keys()))
                    for c in baris:
                        w.writerow(list(c.values()))
                if getattr(args, "keluar", None):
                    Path(args.keluar).write_text(buf.getvalue(), encoding="utf-8")
                    print(f"Templat {len(baris)} cek ditulis ke {args.keluar}. Isi kolom status: "
                          "lulus / gagal / sebagian / tidak_tahu / tidak_berlaku")
                else:
                    sys.stdout.write(buf.getvalue())
            else:
                for p in plat:
                    print(f"\n## {PLATFORM[p]}")
                    for c in baris:
                        if c["platform"] == p:
                            print(f"[{c['id']}] {c['judul']} ({KATEGORI[c['kategori']]}; {c['keparahan']}; {c['kemudahan']})")
                            print(f"   Lulus jika: {c['lulus_jika']}")
                            print(f"   Bukti: {c['bukti']}")
                            if c["tidak_berlaku_jika"]:
                                print(f"   Tidak berlaku jika: {c['tidak_berlaku_jika']}")
            return 0
        if args.cmd == "hitung":
            jawaban, bel_file, peringatan = baca_jawaban(args.jawaban)
            belanja = parse_belanja(args.belanja, bel_file)
            mulai = None
            if args.mulai:
                try:
                    mulai = date.fromisoformat(args.mulai)
                except ValueError:
                    raise InputSalah(f"--mulai harus YYYY-MM-DD, dapat {args.mulai!r}")
            usaha, n_samar = samarkan_kredensial(args.usaha)
            if n_samar:
                peringatan.append("--usaha berisi password/OTP/token -> disamarkan")
            h = hitung(jawaban, belanja, mulai, usaha)
            h["peringatan"] = peringatan + h["peringatan"]
            print(ke_json(h) if args.json else teks_laporan(h))
            return 0
        if args.cmd == "roas-impas":
            r = roas_impas(angka(args.harga, "harga"), angka(args.modal, "modal"),
                           angka(args.biaya_persen, "biaya persen"), angka(args.biaya_lain, "biaya lain"))
            banding = banding_roas(r, [angka(x, "ROAS aktual") for x in args.roas_aktual])
            if args.json:
                out = {k: str(v) for k, v in r.items()}
                out["banding_roas"] = [{k: str(v) for k, v in b.items()} for b in banding]
                print(json.dumps(out, ensure_ascii=False, indent=2))
            else:
                print(f"Harga jual            : {rupiah(r['harga'])}")
                print(f"Modal (HPP)           : {rupiah(r['modal'])}")
                print(f"Biaya platform        : {rupiah(r['biaya_platform'])}")
                print(f"Biaya lain            : {rupiah(r['biaya_lain'])}")
                print(f"Laba kotor/pesanan    : {rupiah(r['laba_kotor'])}")
                print(f"Biaya iklan maks/pesanan (impas): {rupiah(r['biaya_iklan_maks_per_pesanan'])}")
                print(f"ROAS/ROI impas        : {str(r['roas_impas']).replace('.', ',')} "
                      "(di bawah angka ini iklan rugi; dibulatkan ke atas)")
                for b in banding:
                    lr = b["laba_setelah_iklan_per_pesanan"]
                    if b["status"] == "IMPAS":
                        ket = "laba Rp 0"
                    elif b["status"] == "UNTUNG":
                        ket = f"laba ±{rupiah(lr)}" if lr > 0 else "laba < Rp 1"
                    else:
                        ket = f"rugi ±{rupiah(-lr)}" if lr < 0 else "rugi < Rp 1"
                    print(f"ROAS {str(b['roas']).replace('.', ',')} vs impas "
                          f"{str(r['roas_impas']).replace('.', ',')}: {b['status']} "
                          f"(biaya iklan ±{rupiah(b['biaya_iklan_per_pesanan'])}/pesanan, {ket} per pesanan)")
            return 0
    except InputSalah as e:
        print(f"Input bermasalah: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
