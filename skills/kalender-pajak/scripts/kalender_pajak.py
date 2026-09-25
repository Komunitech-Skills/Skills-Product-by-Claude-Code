#!/usr/bin/env python3
"""Kalender tenggat SETOR & LAPOR pajak Indonesia (PMK 81/2024) per profil wajib pajak.

Hanya JADWAL, bukan menghitung besaran pajak. Python standar saja, lintas OS.

Contoh (Windows: ganti python3 dengan python atau py):
  python3 kalender_pajak.py --profil op-umkm,pemberi-kerja --tahun 2026
  python3 kalender_pajak.py --profil badan-pkp --tahun 2026 --bulan-mulai 10 --format ics --keluar pajak.ics
  python3 kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --hari-ini 2026-09-25
  python3 kalender_pajak.py --daftar-profil

Keluar kode 0 = sukses, 2 = input salah (pesan 'ERROR: ...', tanpa traceback).
"""
import argparse
import calendar
import csv
import datetime as dt
import hashlib
import io
import json
import re
import sys
from pathlib import Path

SINI = Path(__file__).resolve().parent
REF = SINI.parent / "references"
TANGGAL_CEK = "2026-09-25"
TAHUN_MIN, TAHUN_MAKS = 2025, 2100

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# ---------------------------------------------------------------------------
# Aturan (sumber & status verifikasi: references/aturan-tenggat.md)
# setor/lapor: 15 / 20 = tanggal itu bulan berikutnya; "akhir" = hari terakhir bulan berikutnya;
# None = tidak ada acara terpisah.
# ---------------------------------------------------------------------------
KEWAJIBAN_MASA = {
    "pph-final-umkm": {
        "pajak": "PPh Final UMKM 0,5% (PP 55/2022)",
        "setor": 15, "lapor": None,
        "catatan": "Setor yang tervalidasi dianggap sudah lapor SPT Masa (PMK 81/2024). "
                   "Hanya bila ada PPh terutang: orang pribadi tidak setor selama omzet kumulatif "
                   "setahun masih <= Rp500 juta. Besarannya: skill pph-final-umkm.",
    },
    "pph21": {
        "pajak": "PPh 21/26 (pemberi kerja)",
        "setor": 15, "lapor": 20, "nama_spt": "SPT Masa PPh 21/26",
        "catatan": "Besarannya: skill pph21-ter. Bukti potong dibuat di Coretax.",
    },
    "unifikasi": {
        "pajak": "PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai)",
        "setor": 15, "lapor": 20, "nama_spt": "SPT Masa PPh Unifikasi",
        "catatan": "Untuk pemotong/pemungut, mis. potong PPh 23 jasa atau PPh 4(2) sewa.",
    },
    "ppn": {
        "pajak": "PPN (PKP)",
        "setor": "akhir", "lapor": "akhir", "nama_spt": "SPT Masa PPN",
        "catatan": "Setor paling lambat akhir bulan berikutnya DAN sebelum SPT Masa PPN dikirim. "
                   "PKP tetap lapor walau nihil. Besarannya: skill hitung-ppn.",
    },
    "pph25": {
        "pajak": "PPh 25 (angsuran bulanan)",
        "setor": 15, "lapor": None,
        "catatan": "Setor yang tervalidasi dianggap sudah lapor SPT Masa PPh 25 (PERLU REVIEW). "
                   "Angsuran nihil tidak perlu setor.",
    },
}

KEWAJIBAN_TAHUNAN = {
    "spt-op": {
        "pajak": "SPT Tahunan PPh Orang Pribadi",
        "bulan_ke": 3,
        "judul": "LAPOR SPT Tahunan PPh Orang Pribadi",
        "catatan": "Paling lambat 3 bulan setelah akhir tahun pajak. Kurang bayar (PPh 29) dilunasi "
                   "SEBELUM SPT dikirim. Tenggat SPT Tahunan TIDAK bergeser walau jatuh di hari libur.",
    },
    "spt-badan": {
        "pajak": "SPT Tahunan PPh Badan",
        "bulan_ke": 4,
        "judul": "LAPOR SPT Tahunan PPh Badan",
        "catatan": "Paling lambat akhir bulan ke-4 setelah akhir tahun buku (dianggap tahun buku "
                   "Januari-Desember). Kurang bayar (PPh 29) dilunasi SEBELUM SPT dikirim. Tidak bergeser "
                   "walau jatuh di hari libur.",
    },
    "bukti-a1": {
        "pajak": "Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1)",
        "bulan_ke": 1,
        "judul": "BERIKAN bukti potong BPA1 ke karyawan",
        "catatan": "Paling lama 1 bulan setelah masa pajak terakhir (PER-2/PJ/2024). Karyawan butuh ini "
                   "untuk SPT Tahunan. Tanggal ditampilkan tanpa pergeseran (PERLU REVIEW).",
    },
}

PROFIL = {
    "op-umkm": (["pph-final-umkm", "spt-op"],
                "Orang pribadi usaha, PPh final 0,5% (PP 55/2022)"),
    "op-karyawan": (["spt-op"], "Orang pribadi karyawan/pekerja tanpa usaha"),
    "op-pembukuan": (["pph25", "spt-op"],
                     "Orang pribadi usaha/pekerjaan bebas dengan tarif umum (pembukuan/norma)"),
    "badan-umkm": (["pph-final-umkm", "spt-badan"],
                   "PT perorangan/koperasi yang memakai PPh final 0,5%"),
    "badan-umum": (["pph25", "spt-badan"], "Badan dengan tarif umum, bukan PKP"),
    "badan-pkp": (["ppn", "pph25", "spt-badan"], "Badan PKP (memungut PPN), tarif umum"),
    "pkp": (["ppn"], "Tambahan: sudah dikukuhkan PKP (untuk orang pribadi/badan UMKM yang PKP)"),
    "pemberi-kerja": (["pph21", "bukti-a1"], "Tambahan: punya karyawan (memotong PPh 21)"),
    "pemotong": (["unifikasi"], "Tambahan: memotong PPh 23/4(2)/15/22/26 (mis. bayar jasa, sewa)"),
}

SEMUA_KEWAJIBAN = list(KEWAJIBAN_MASA) + list(KEWAJIBAN_TAHUNAN)

DISCLAIMER = (
    "Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, "
    "PER-2/PJ/2024, SKB 3 Menteri libur nasional & cuti bersama; dicek " + TANGGAL_CEK +
    " dari sumber sekunder (naskah resmi belum dibaca langsung). DJP kadang memundurkan tenggat lewat "
    "pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). "
    "Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. "
    "Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)."
)


class InputSalah(Exception):
    pass


# ---------------------------------------------------------------------------
# Data libur
# ---------------------------------------------------------------------------
def muat_libur(ekstra=None):
    """Kembalikan (dict tanggal -> keterangan, set tahun yang punya data)."""
    libur, tahun_ada = {}, set()
    berkas = sorted(REF.glob("libur-nasional-*.csv")) + [Path(p) for p in (ekstra or [])]
    for f in berkas:
        if not f.is_file():
            raise InputSalah("file libur '%s' tidak ditemukan" % f)
        try:
            with f.open(newline="", encoding="utf-8-sig") as h:
                r = csv.DictReader(h)
                if not r.fieldnames or "tanggal" not in r.fieldnames:
                    raise InputSalah("file libur '%s' harus punya kolom 'tanggal' (dan opsional "
                                     "'jenis','keterangan')" % f.name)
                for no, b in enumerate(r, start=2):
                    try:
                        t = dt.date.fromisoformat((b.get("tanggal") or "").strip())
                    except ValueError:
                        raise InputSalah("file libur '%s' baris %d: tanggal '%s' bukan format "
                                         "YYYY-MM-DD" % (f.name, no, b.get("tanggal")))
                    jenis = (b.get("jenis") or "libur").strip()
                    ket = (b.get("keterangan") or "").strip() or "hari libur"
                    libur[t] = ("cuti bersama: " if jenis == "cuti" and not ket.lower().startswith("cuti")
                                else "") + ket
                    tahun_ada.add(t.year)
        except UnicodeDecodeError:
            raise InputSalah("file libur '%s' bukan teks UTF-8" % f.name)
    return libur, tahun_ada


def hari_libur(t, libur):
    if t.weekday() == 5:
        return "Sabtu"
    if t.weekday() == 6:
        return "Minggu"
    return libur.get(t)


def geser(t, libur, tahun_ada, kurang):
    """Geser ke hari kerja berikutnya. Kembalikan (tanggal akhir, [alasan]).
    Tahun tanpa data libur yang dilewati dicatat ke `kurang`."""
    alasan = []
    while True:
        if t.year not in tahun_ada:
            kurang.add(t.year)
        a = hari_libur(t, libur)
        if not a:
            return t, alasan
        alasan.append("%s %s" % (fmt_pendek(t), a))
        t += dt.timedelta(days=1)


# ---------------------------------------------------------------------------
# Tanggal
# ---------------------------------------------------------------------------
def bulan_berikut(th, bl, n=1):
    i = th * 12 + (bl - 1) + n
    return i // 12, i % 12 + 1


def tgl_aturan(th, bl, aturan):
    if aturan == "akhir":
        return dt.date(th, bl, calendar.monthrange(th, bl)[1])
    return dt.date(th, bl, aturan)


def fmt_pendek(t):
    return "%d %s" % (t.day, BLN[t.month - 1])


def fmt_panjang(t):
    return "%s, %d %s %d" % (HARI[t.weekday()], t.day, BULAN[t.month - 1], t.year)


# ---------------------------------------------------------------------------
# Susun acara
# ---------------------------------------------------------------------------
def urai_profil(teks_list):
    kewajiban, profil_dipakai = [], []
    for teks in teks_list:
        for p in re.split(r"[,\s;]+", teks.strip().lower()):
            if not p:
                continue
            if p in PROFIL:
                profil_dipakai.append(p)
                kewajiban += PROFIL[p][0]
            elif p in SEMUA_KEWAJIBAN:
                profil_dipakai.append(p)
                kewajiban.append(p)
            else:
                raise InputSalah("profil/kewajiban '%s' tidak dikenal. Pilihan profil: %s. "
                                 "Pilihan kewajiban: %s. Lihat --daftar-profil."
                                 % (p, ", ".join(PROFIL), ", ".join(SEMUA_KEWAJIBAN)))
    if not kewajiban:
        raise InputSalah("isi --profil, mis. --profil op-umkm atau --profil badan-pkp,pemberi-kerja")
    unik = []
    for k in kewajiban:
        if k not in unik:
            unik.append(k)
    return profil_dipakai, unik


def uid(*bagian):
    h = hashlib.sha1("|".join(str(b) for b in bagian).encode("utf-8")).hexdigest()[:20]
    return "%s@kalender-pajak.komunitech" % h


def buat_acara(kewajiban, awal, akhir, libur, tahun_ada):
    """Acara dengan tanggal akhir (sesudah geser) di [awal, akhir]."""
    acara, kurang = [], set()

    def tambah(kode, jenis, judul, pajak, masa_label, normal, bisa_geser, catatan):
        cek, libur_tetap = set(), None
        if bisa_geser:
            final, alasan = geser(normal, libur, tahun_ada, cek)
        else:
            final, alasan = normal, []
            if normal.year not in tahun_ada:
                cek.add(normal.year)
            libur_tetap = hari_libur(normal, libur)
        if awal <= final <= akhir:
            kurang.update(cek)
            acara.append({
                "tanggal": final, "tanggal_normal": normal, "kode": kode, "jenis": jenis,
                "judul": judul, "pajak": pajak, "masa": masa_label, "alasan_geser": alasan,
                "bisa_geser": bisa_geser, "catatan": catatan, "libur_tetap": libur_tetap,
                "uid": uid(kode, jenis, masa_label),
            })

    # masa pajak yang mungkin tenggatnya jatuh di rentang (mundur 3 bulan cukup: geser maks. beberapa hari)
    th, bl = bulan_berikut(awal.year, awal.month, -3)
    while (th, bl) <= (akhir.year, akhir.month):
        masa_label = "%s %d" % (BLN[bl - 1], th)
        nth, nbl = bulan_berikut(th, bl)
        for k in kewajiban:
            a = KEWAJIBAN_MASA.get(k)
            if not a:
                continue
            ts = tgl_aturan(nth, nbl, a["setor"])
            tl = tgl_aturan(nth, nbl, a["lapor"]) if a["lapor"] is not None else None
            if tl is not None and tl == ts:
                tambah(k, "setor+lapor", "SETOR & LAPOR %s masa %s" % (a["nama_spt"].replace("SPT Masa ", ""), masa_label),
                       a["pajak"], masa_label, ts, True, a["catatan"])
            else:
                tambah(k, "setor", "SETOR %s masa %s" % (a["pajak"], masa_label), a["pajak"],
                       masa_label, ts, True, a["catatan"])
                if tl is not None:
                    tambah(k, "lapor", "LAPOR %s masa %s" % (a["nama_spt"], masa_label), a["pajak"],
                           masa_label, tl, True, a["catatan"])
        th, bl = nth, nbl

    for k in kewajiban:
        a = KEWAJIBAN_TAHUNAN.get(k)
        if not a:
            continue
        for tp in range(awal.year - 2, akhir.year + 1):
            yth, ybl = bulan_berikut(tp, 12, a["bulan_ke"])
            normal = tgl_aturan(yth, ybl, "akhir")
            tambah(k, "tahunan", "%s tahun pajak %d" % (a["judul"], tp), a["pajak"],
                   "Tahun pajak %d" % tp, normal, False, a["catatan"])

    urut = {k: i for i, k in enumerate(SEMUA_KEWAJIBAN)}
    jenis_urut = {"setor": 0, "setor+lapor": 1, "lapor": 2, "tahunan": 3}
    acara.sort(key=lambda e: (e["tanggal"], jenis_urut[e["jenis"]], urut[e["kode"]]))
    return acara, kurang


# ---------------------------------------------------------------------------
# Keluaran
# ---------------------------------------------------------------------------
def ket_geser(e):
    if e.get("libur_tetap"):
        return "jatuh pada hari libur (%s) dan TIDAK bergeser - selesaikan hari kerja sebelumnya" % e["libur_tetap"]
    if not e["alasan_geser"]:
        return "-"
    return "bergeser dari %s (%s)" % (fmt_pendek(e["tanggal_normal"]), "; ".join(e["alasan_geser"]))


def pesan_kurang(kurang, tahun_ada):
    if not kurang:
        return None
    return ("PERINGATAN: data libur nasional/cuti bersama tahun %s belum ada (tersedia: %s). "
            "Untuk tahun itu hanya Sabtu/Minggu yang diperhitungkan - tanggal bisa kurang tepat. "
            "Cek SKB 3 Menteri tahun tersebut dan tambahkan file references/libur-nasional-<tahun>.csv "
            "atau pakai --libur <file.csv>." % (", ".join(str(t) for t in sorted(kurang)),
                                               ", ".join(str(t) for t in sorted(tahun_ada)) or "-"))


def keluaran_md(acara, info):
    o = []
    o.append("## Kalender Pajak %s - %s" % (info["judul_rentang"], info["label_profil"]))
    o.append("")
    o.append("Kewajiban: %s" % ", ".join(info["kewajiban_nama"]))
    if info["peringatan"]:
        o += ["", "> **%s**" % info["peringatan"]]
    o.append("")
    if not acara:
        o.append("_Tidak ada tenggat dalam rentang ini._")
    else:
        o.append("| Tanggal | Kegiatan | Keterangan |")
        o.append("|---|---|---|")
        for e in acara:
            o.append("| %s | %s | %s |" % (fmt_panjang(e["tanggal"]), e["judul"], ket_geser(e)))
    o += ["", "**Catatan per kewajiban**"]
    for k in info["kewajiban"]:
        a = KEWAJIBAN_MASA.get(k) or KEWAJIBAN_TAHUNAN[k]
        o.append("- %s: %s" % (a["pajak"], a["catatan"]))
    o += ["", "**Aturan pergeseran:** tenggat setor & lapor bulanan yang jatuh pada Sabtu, Minggu, "
              "libur nasional, atau cuti bersama bergeser ke hari kerja berikutnya (PMK 81/2024). "
              "Tenggat SPT Tahunan tidak bergeser. Sebaiknya setor/lapor 2-3 hari sebelum tenggat.",
          "", "_%s_" % DISCLAIMER]
    return "\n".join(o) + "\n"


def keluaran_checklist(acara, info):
    o = ["## Checklist Pajak Bulanan - %s" % info["label_profil"], ""]
    if info["peringatan"]:
        o += ["> **%s**" % info["peringatan"], ""]
    bulan_ini = None
    for e in acara:
        kunci = (e["tanggal"].year, e["tanggal"].month)
        if kunci != bulan_ini:
            bulan_ini = kunci
            o += ["", "### %s %d" % (BULAN[kunci[1] - 1], kunci[0])]
        tambahan = " (%s)" % ket_geser(e) if ket_geser(e) != "-" else ""
        o.append("- [ ] **%s %s** - %s%s" % (HARI[e["tanggal"].weekday()][:3], fmt_pendek(e["tanggal"]),
                                               e["judul"], tambahan))
    if not acara:
        o.append("_Tidak ada tenggat dalam rentang ini._")
    o += ["", "Sebelum setor: siapkan angka (skill pph-final-umkm / pph21-ter / hitung-ppn), buat kode "
              "billing di Coretax, bayar, simpan bukti penerimaan negara (BPN/NTPN).",
          "", "_%s_" % DISCLAIMER]
    return "\n".join(o) + "\n"


def keluaran_hari_ini(acara, info, hari_ini, rentang):
    o = ["## Tenggat pajak %d hari ke depan (%s s.d. %s) - %s" % (
        rentang, fmt_panjang(hari_ini), fmt_panjang(hari_ini + dt.timedelta(days=rentang)),
        info["label_profil"]), ""]
    if info["peringatan"]:
        o += ["> **%s**" % info["peringatan"], ""]
    if not acara:
        o.append("Tidak ada tenggat dalam %d hari ke depan." % rentang)
    else:
        o.append("| Sisa | Tanggal | Kegiatan | Keterangan |")
        o.append("|---|---|---|---|")
        for e in acara:
            sisa = (e["tanggal"] - hari_ini).days
            label = "HARI INI" if sisa == 0 else ("besok" if sisa == 1 else "%d hari lagi" % sisa)
            o.append("| %s | %s | %s | %s |" % (label, fmt_panjang(e["tanggal"]), e["judul"], ket_geser(e)))
    o += ["", "_%s_" % DISCLAIMER]
    return "\n".join(o) + "\n"


def keluaran_csv(acara):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["tanggal", "hari", "kegiatan", "jenis", "kewajiban", "pajak", "masa", "tanggal_normal",
                "keterangan_geser", "catatan"])
    for e in acara:
        w.writerow([e["tanggal"].isoformat(), HARI[e["tanggal"].weekday()], e["judul"], e["jenis"], e["kode"],
                    e["pajak"], e["masa"], e["tanggal_normal"].isoformat(),
                    ket_geser(e) if ket_geser(e) != "-" else "", e["catatan"]])
    return buf.getvalue()


def keluaran_json(acara, info):
    return json.dumps({
        "profil": info["profil"], "kewajiban": info["kewajiban"], "rentang": info["rentang"],
        "peringatan": info["peringatan"], "tanggal_cek_aturan": TANGGAL_CEK,
        "acara": [{
            "tanggal": e["tanggal"].isoformat(), "tanggal_normal": e["tanggal_normal"].isoformat(),
            "kegiatan": e["judul"], "jenis": e["jenis"], "kewajiban": e["kode"], "masa": e["masa"],
            "bergeser_karena": e["alasan_geser"], "libur_tidak_bergeser": e["libur_tetap"],
            "catatan": e["catatan"], "uid": e["uid"],
        } for e in acara],
        "disclaimer": DISCLAIMER,
    }, ensure_ascii=False, indent=2) + "\n"


def ics_escape(teks):
    return (teks.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
            .replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n"))


def ics_lipat(baris):
    """Lipat baris > 75 oktet (RFC 5545 3.1) tanpa memotong karakter UTF-8."""
    hasil, sekarang, batas = [], "", 75
    for ch in baris:
        if len((sekarang + ch).encode("utf-8")) > batas:
            hasil.append(sekarang)
            sekarang, batas = " " + ch, 75
        else:
            sekarang += ch
    hasil.append(sekarang)
    return "\r\n".join(hasil)


def keluaran_ics(acara, info, sekarang_utc):
    stamp = sekarang_utc.strftime("%Y%m%dT%H%M%SZ")
    b = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Komunitech//kalender-pajak 1.0.0//ID",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:" + ics_escape("Kalender Pajak - " + info["label_profil"]),
         "X-WR-TIMEZONE:Asia/Jakarta"]
    for e in acara:
        desk = "%s\nMasa: %s\n%s\n%s\nTenggat normal: %s\n\n%s" % (
            e["judul"], e["masa"], e["catatan"],
            ("Keterangan: " + ket_geser(e)) if ket_geser(e) != "-" else "Tidak bergeser.",
            fmt_panjang(e["tanggal_normal"]), DISCLAIMER)
        b += ["BEGIN:VEVENT", "UID:" + e["uid"], "DTSTAMP:" + stamp,
              "DTSTART;VALUE=DATE:" + e["tanggal"].strftime("%Y%m%d"),
              "DTEND;VALUE=DATE:" + (e["tanggal"] + dt.timedelta(days=1)).strftime("%Y%m%d"),
              "SUMMARY:" + ics_escape("Pajak: " + e["judul"]),
              "DESCRIPTION:" + ics_escape(desk),
              "CATEGORIES:" + ics_escape("Pajak"),
              "TRANSP:TRANSPARENT"]
        # Pengingat H-3 & H-1 pukul 09.00 waktu perangkat (acara sepanjang hari mulai 00.00)
        for trig, label in (("-P2DT15H", "3 hari lagi"), ("-PT15H", "besok")):
            b += ["BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:" + trig,
                  "DESCRIPTION:" + ics_escape("%s: %s" % (label, e["judul"])), "END:VALARM"]
        b.append("END:VEVENT")
    b.append("END:VCALENDAR")
    return "\r\n".join(ics_lipat(x) for x in b) + "\r\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def daftar_profil():
    o = ["Profil (boleh digabung dengan koma, mis. badan-pkp,pemberi-kerja,pemotong):"]
    for k, (kw, ket) in PROFIL.items():
        o.append("  %-14s %s  -> %s" % (k, ket, ", ".join(kw)))
    o.append("Kewajiban tunggal juga boleh dipakai langsung: " + ", ".join(SEMUA_KEWAJIBAN))
    return "\n".join(o) + "\n"


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise InputSalah("argumen tidak valid: %s. Lihat --help." % message)


def angka(teks, nama, bawah, atas):
    try:
        n = int(str(teks).strip())
    except ValueError:
        raise InputSalah("%s harus angka bulat, bukan '%s'" % (nama, teks))
    if not bawah <= n <= atas:
        raise InputSalah("%s harus %d-%d (sekarang %d)" % (nama, bawah, atas, n))
    return n


def nama_bulan(teks):
    """Terima 10, 'Okt', 'oktober', 'Oct'."""
    t = str(teks).strip().lower()
    for i, (panjang, pendek) in enumerate(zip(BULAN, BLN), start=1):
        if t in (panjang.lower(), pendek.lower()) or (len(t) >= 3 and panjang.lower().startswith(t)):
            return i
    lain = {"may": 5, "aug": 8, "oct": 10, "dec": 12, "agt": 8, "ags": 8}
    return lain.get(t, teks)


def jalankan(argv, sekarang_utc=None):
    p = Parser(description="Kalender tenggat setor & lapor pajak Indonesia (PMK 81/2024).")
    p.add_argument("--profil", action="append", default=[],
                   help="profil/kewajiban, dipisah koma. Lihat --daftar-profil")
    p.add_argument("--tahun", help="tahun awal kalender (default: tahun ini)")
    p.add_argument("--bulan-mulai", default="1", help="bulan awal kalender 1-12 (default 1)")
    p.add_argument("--jumlah-bulan", default="12", help="panjang kalender 1-24 bulan (default 12)")
    p.add_argument("--hari-ini", help="YYYY-MM-DD: tampilkan tenggat N hari ke depan dari tanggal ini "
                                      "('hari-ini' = tanggal komputer)")
    p.add_argument("--rentang", default="14", help="N hari untuk --hari-ini (1-90, default 14)")
    p.add_argument("--format", default="md", help="md | checklist | csv | ics | json")
    p.add_argument("--keluar", help="simpan ke file ini (disarankan untuk ics)")
    p.add_argument("--libur", action="append", default=[], help="file CSV libur tambahan (kolom tanggal,jenis,keterangan)")
    p.add_argument("--daftar-profil", action="store_true", help="tampilkan daftar profil lalu keluar")
    a = p.parse_args(argv)

    if a.daftar_profil:
        return daftar_profil().encode("utf-8"), None

    fmt = a.format.strip().lower()
    if fmt not in ("md", "checklist", "csv", "ics", "json"):
        raise InputSalah("format '%s' tidak dikenal; pilih md, checklist, csv, ics, atau json" % a.format)
    profil, kewajiban = urai_profil(a.profil)
    libur, tahun_ada = muat_libur(a.libur)
    sekarang_utc = sekarang_utc or dt.datetime.now(dt.timezone.utc)

    if a.hari_ini:
        if a.hari_ini.strip().lower() in ("hari-ini", "sekarang", "today"):
            hari_ini = dt.date.today()
        else:
            try:
                hari_ini = dt.date.fromisoformat(a.hari_ini.strip())
            except ValueError:
                raise InputSalah("--hari-ini harus tanggal YYYY-MM-DD (mis. 2026-09-25), bukan '%s'" % a.hari_ini)
        if not TAHUN_MIN <= hari_ini.year <= TAHUN_MAKS:
            raise InputSalah("tahun harus %d-%d" % (TAHUN_MIN, TAHUN_MAKS))
        rentang = angka(a.rentang, "--rentang", 1, 90)
        awal, akhir = hari_ini, hari_ini + dt.timedelta(days=rentang)
        judul = "%s s.d. %s" % (awal.isoformat(), akhir.isoformat())
    else:
        tahun = angka(a.tahun or dt.date.today().year, "--tahun", TAHUN_MIN, TAHUN_MAKS)
        bm = angka(nama_bulan(a.bulan_mulai), "--bulan-mulai", 1, 12)
        jb = angka(a.jumlah_bulan, "--jumlah-bulan", 1, 24)
        awal = dt.date(tahun, bm, 1)
        ath, abl = bulan_berikut(tahun, bm, jb - 1)
        akhir = tgl_aturan(ath, abl, "akhir")
        judul = ("%s %d" % (BULAN[bm - 1], tahun)) if jb == 1 else "%s %d - %s %d" % (
            BULAN[bm - 1], tahun, BULAN[abl - 1], ath)

    acara, kurang = buat_acara(kewajiban, awal, akhir, libur, tahun_ada)
    # tahun rentang yang tidak punya data juga diperingatkan walau tidak ada acara di sana
    for th in range(awal.year, akhir.year + 1):
        if th not in tahun_ada:
            kurang.add(th)
    info = {
        "profil": profil, "kewajiban": kewajiban, "rentang": [awal.isoformat(), akhir.isoformat()],
        "judul_rentang": judul, "label_profil": ", ".join(profil),
        "kewajiban_nama": [(KEWAJIBAN_MASA.get(k) or KEWAJIBAN_TAHUNAN[k])["pajak"] for k in kewajiban],
        "peringatan": pesan_kurang(kurang, tahun_ada),
    }
    if a.hari_ini and fmt == "md":
        teks = keluaran_hari_ini(acara, info, awal, (akhir - awal).days)
    elif fmt == "md":
        teks = keluaran_md(acara, info)
    elif fmt == "checklist":
        teks = keluaran_checklist(acara, info)
    elif fmt == "csv":
        teks = keluaran_csv(acara)
    elif fmt == "json":
        teks = keluaran_json(acara, info)
    else:
        teks = keluaran_ics(acara, info, sekarang_utc)
    data = teks.encode("utf-8")
    if a.keluar:
        try:
            Path(a.keluar).write_bytes(data)
        except OSError as e:
            raise InputSalah("tidak bisa menulis '%s': %s" % (a.keluar, e.strerror or e))
        pesan = "Tersimpan: %s (%d tenggat)" % (a.keluar, len(acara))
        if info["peringatan"]:
            pesan += "\n" + info["peringatan"]
        return (pesan + "\n").encode("utf-8"), None
    return data, (info["peringatan"] if fmt in ("csv", "ics") else None)


def main(argv=None):
    try:
        data, peringatan = jalankan(sys.argv[1:] if argv is None else argv)
    except InputSalah as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return 2
    except KeyboardInterrupt:
        return 130
    if peringatan:
        sys.stderr.write(peringatan + "\n")
    out = getattr(sys.stdout, "buffer", None)
    if out is not None:
        out.write(data)
        out.flush()
    else:
        sys.stdout.write(data.decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
