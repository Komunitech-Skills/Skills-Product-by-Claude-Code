#!/usr/bin/env python3
"""Ubah tenggat relatif dari catatan rapat ("besok", "Jumat depan", "akhir bulan") menjadi
tanggal nyata, berdasarkan tanggal rapat. Juga bisa mengecek nama hari suatu tanggal.

Contoh:
  python3 tanggal_relatif.py --rapat 21-09-2026 --ekspresi "jumat depan" "besok" "akhir bulan"
  python3 tanggal_relatif.py --rapat 21-09-2026 --ekspresi "3 hari lagi" "minggu depan" --format teks
  python3 tanggal_relatif.py --cek 02-10-2026

Aturan tafsir (hasil ambigu selalu diberi alternatif + catatan):
  - "besok" = +1 hari; "lusa" = +2 hari; "N hari lagi" = +N hari; "N minggu lagi" = +7N hari.
  - "minggu depan" (tanpa nama hari) = Senin minggu berikutnya.
  - "<hari> ini" = hari itu di minggu yang sama (Senin–Minggu); jika sudah lewat -> ambigu.
  - "<hari>" saja = kemunculan terdekat SETELAH tanggal rapat.
  - "<hari> minggu depan" = hari itu di minggu BERIKUTNYA (Senin–Minggu) -> pasti.
  - "<hari> depan" = diartikan sama, tetapi karena orang sering memaknainya sebagai hari
    terdekat, hasil diberi alternatif dan status "ambigu" bila keduanya berbeda.
  - "minggu ini" = ambigu (pekan ini s.d. Jumat, atau hari Minggu).
  - Rapat hari MINGGU: "minggu depan", "<hari> depan", dan "<hari> minggu depan" selalu
    "ambigu" (pekan depan bisa dimulai besok atau pekan setelahnya); alternatif = +7 hari.
  - "akhir minggu" = Jumat minggu yang sama; "akhir bulan" = hari terakhir bulan itu;
    "awal bulan depan" = tanggal 1 bulan berikutnya.
  - Awalan batas waktu dikenali lalu ekspresi sisanya ditafsir dengan aturan di atas:
    "sebelum/sblm/sebelom X" -> field batas="sebelum" (tenggat_teks "Sebelum Rabu, ..."; bila diartikan
    ketat, selesai paling lambat sehari sebelumnya -> disebut di catatan);
    "paling lambat/plg lambat/paling telat/maks/maksimal/max/deadline/tenggat/batas/s.d./s/d/sampai/hingga X"
    -> batas="paling_lambat" (tenggat_teks "Paling lambat Senin, ...").
    Contoh: "sebelum rabu", "sblm jumat", "paling lambat senin depan", "maks besok".
Hanya library standar Python 3.8+. Tanpa akses jaringan. Versi 1.0.3 (2026-10-01).
"""
import argparse
import calendar
import json
import re
import sys
from datetime import date, timedelta

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
BULAN_ALIAS = {
    "jan": 1, "januari": 1, "feb": 2, "peb": 2, "februari": 2, "mar": 3, "maret": 3, "apr": 4,
    "april": 4, "mei": 5, "jun": 6, "juni": 6, "jul": 7, "juli": 7, "agu": 8, "agt": 8,
    "agustus": 8, "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10,
    "nov": 11, "nop": 11, "november": 11, "nopember": 11, "des": 12, "desember": 12,
}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
HARI_ALIAS = {"senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "jum'at": 4,
              "sabtu": 5, "minggu": 6, "ahad": 6}


CATATAN_MINGGU = ("Rapat hari Minggu: 'minggu depan' bisa dimulai besok (Senin) atau pekan "
                  "setelahnya. Mohon dikonfirmasi.")


class InputSalah(Exception):
    pass


def parse_tanggal(teks, label):
    s = (teks or "").strip()
    if not s:
        raise InputSalah(f"{label} kosong. Contoh: 21-09-2026 atau 21 September 2026.")
    try:
        m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", s)
        if m:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        m = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", s)
        if m:
            b = BULAN_ALIAS.get(m.group(2).lower())
            if b is None:
                raise InputSalah(f"{label}: nama bulan '{m.group(2)}' tidak dikenali.")
            return date(int(m.group(3)), b, int(m.group(1)))
    except ValueError:
        raise InputSalah(f"{label}: tanggal '{s}' tidak ada di kalender.")
    raise InputSalah(f"{label}: format '{s}' tidak dikenali. Pakai 21-09-2026 atau 21 September 2026.")


def teks(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


_AWALAN = re.compile(
    r"^(?:(sebelum|sblm|sebelom|sblum)|(paling lambat|plg lambat|plg lmbt|paling telat|maksimal|maks\.?|max|"
    r"deadline|tenggat|batas|s\.\s?d\.?|s/d|sd|sampai|smp|hingga))\s+(.+)$")


def tafsir(ekspresi, rapat):
    e0 = re.sub(r"\s+", " ", ekspresi.strip().lower())
    m = _AWALAN.match(e0)
    if m and m.group(3).strip():
        hasil = tafsir(m.group(3), rapat)
        hasil["ekspresi"] = ekspresi
        if hasil.get("tanggal"):
            d = date.fromisoformat(hasil["tanggal"])
            if m.group(1):
                hasil["batas"] = "sebelum"
                hasil["tenggat_teks"] = "Sebelum " + teks(d)
                tambah = (f"'Sebelum' {teks(d)}: bila diartikan ketat, selesai paling lambat "
                          f"{teks(d - timedelta(days=1))}.")
            else:
                hasil["batas"] = "paling_lambat"
                hasil["tenggat_teks"] = "Paling lambat " + teks(d)
                tambah = ""
            hasil["catatan"] = " ".join(x for x in (hasil["catatan"], tambah) if x)
        return hasil
    e = e0
    senin_ini = rapat - timedelta(days=rapat.weekday())
    minggu_rapat = rapat.weekday() == 6  # rapat hari Minggu
    hasil = {"ekspresi": ekspresi, "status": "pasti", "alternatif": None, "catatan": ""}

    def set_(d, status="pasti", alt=None, cat=""):
        hasil.update({"tanggal": d.isoformat(), "tanggal_teks": teks(d), "tenggat_teks": teks(d),
                      "batas": None, "status": status,
                      "alternatif": teks(alt) if alt else None, "catatan": cat})
        return hasil

    if e in ("hari ini", "sekarang"):
        return set_(rapat)
    if e == "besok":
        return set_(rapat + timedelta(days=1))
    if e == "lusa":
        return set_(rapat + timedelta(days=2))
    m = re.fullmatch(r"(\d{1,3}) (hari|minggu|pekan) (lagi|ke depan)", e)
    if m:
        n = int(m.group(1)) * (1 if m.group(2) == "hari" else 7)
        return set_(rapat + timedelta(days=n))
    if e in ("minggu depan", "pekan depan"):
        d = senin_ini + timedelta(days=7)
        if minggu_rapat:
            return set_(d, "ambigu", d + timedelta(days=7), CATATAN_MINGGU)
        return set_(d, "perkiraan",
                    cat="Tidak menyebut hari; diartikan Senin minggu depan. Mohon dikonfirmasi.")
    if e in ("minggu ini", "pekan ini"):
        return set_(senin_ini + timedelta(days=4), "ambigu", senin_ini + timedelta(days=6),
                    "'Minggu ini' bisa berarti pekan ini (diartikan paling lambat Jumat) atau hari Minggu.")
    if e in ("akhir minggu", "akhir pekan", "akhir minggu ini"):
        return set_(senin_ini + timedelta(days=4), "perkiraan",
                    alt=senin_ini + timedelta(days=6),
                    cat="Diartikan Jumat (hari kerja terakhir). Alternatif: Minggu.")
    if e in ("akhir bulan", "akhir bulan ini"):
        akhir = date(rapat.year, rapat.month, calendar.monthrange(rapat.year, rapat.month)[1])
        return set_(akhir)
    if e in ("awal bulan depan", "bulan depan"):
        th, bl = (rapat.year + 1, 1) if rapat.month == 12 else (rapat.year, rapat.month + 1)
        st = "pasti" if e.startswith("awal") else "perkiraan"
        return set_(date(th, bl, 1), st,
                    cat="" if st == "pasti" else "Hanya 'bulan depan'; diartikan tanggal 1. Mohon dikonfirmasi.")
    m = re.fullmatch(r"(hari )?([a-z']+)( ini| depan| minggu depan| pekan depan)?", e)
    if m and m.group(2) in HARI_ALIAS:
        h = HARI_ALIAS[m.group(2)]
        suf = (m.group(3) or "").strip()
        terdekat = rapat + timedelta(days=((h - rapat.weekday()) % 7) or 7)
        if suf == "ini":
            d = senin_ini + timedelta(days=h)
            if d < rapat:
                return set_(d, "ambigu", terdekat, "Hari itu sudah lewat pada minggu rapat.")
            return set_(d)
        if suf:  # depan / minggu depan
            d = senin_ini + timedelta(days=7 + h)
            if minggu_rapat:
                return set_(d, "ambigu", d + timedelta(days=7), CATATAN_MINGGU)
            if suf == "depan" and d != terdekat:
                return set_(d, "ambigu", terdekat,
                            "'Depan' bisa berarti minggu berikutnya atau hari terdekat. Mohon dikonfirmasi.")
            return set_(d)
        return set_(terdekat)
    hasil.update({"status": "tidak_dikenali", "tanggal": None, "tanggal_teks": None, "tenggat_teks": None,
                  "batas": None,
                  "catatan": "Ekspresi tidak dikenali; biarkan apa adanya dan tandai ⚠️ di notulen."})
    return hasil


def main():
    p = argparse.ArgumentParser(description="Konversi tenggat relatif rapat ke tanggal nyata.")
    p.add_argument("--rapat", help="Tanggal rapat, mis. 21-09-2026")
    p.add_argument("--ekspresi", nargs="+", help='Ekspresi relatif, mis. "jumat depan" "besok"')
    p.add_argument("--cek", nargs="+", help="Tanggal yang ingin dicek nama harinya")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    a = p.parse_args()
    try:
        if not a.ekspresi and not a.cek:
            raise InputSalah("Isi --ekspresi (bersama --rapat) atau --cek.")
        out = {}
        if a.ekspresi:
            if not a.rapat:
                raise InputSalah("--ekspresi butuh --rapat (tanggal rapat).")
            r = parse_tanggal(a.rapat, "--rapat")
            out["tanggal_rapat"] = teks(r)
            out["hasil"] = [tafsir(x, r) for x in a.ekspresi]
        if a.cek:
            out["cek_hari"] = [teks(parse_tanggal(x, "--cek")) for x in a.cek]
    except InputSalah as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    if a.format == "json":
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    if "tanggal_rapat" in out:
        print(f"Tanggal rapat: {out['tanggal_rapat']}")
        for h in out["hasil"]:
            baris = f"- \"{h['ekspresi']}\" -> {h.get('tenggat_teks') or '(tidak dikenali)'} [{h['status']}]"
            if h["alternatif"]:
                baris += f" | alternatif: {h['alternatif']}"
            if h["catatan"]:
                baris += f" | {h['catatan']}"
            print(baris)
    for c in out.get("cek_hari", []):
        print(f"Cek hari: {c}")


if __name__ == "__main__":
    main()
