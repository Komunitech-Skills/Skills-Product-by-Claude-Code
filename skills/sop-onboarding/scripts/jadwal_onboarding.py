#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hitung tanggal-tanggal kegiatan onboarding karyawan baru dari tanggal mulai kerja.

Tahap yang dihitung: hari pertama (H1), akhir minggu 1, evaluasi 30/60/90 hari, dan
(khusus PKWTT) akhir masa percobaan 3 bulan (UU 13/2003 Pasal 60 jo. UU 6/2023).
PKWT (karyawan kontrak) TIDAK BOLEH ada masa percobaan (UU 13/2003 Pasal 58 jo. UU 6/2023;
PP 35/2021 Pasal 12) -- lihat references/dasar-hukum-onboarding.md.

Cara hitung tanggal:
  - H1               = tanggal mulai kerja (tidak digeser).
  - Akhir minggu 1    = mulai + 6 hari kalender (hari ke-7).
  - Evaluasi 30/60/90 = mulai + 29/59/89 hari kalender (hari ke-30/60/90, inklusif).
  - Akhir masa percobaan (PKWTT) = tanggal yang sama 3 bulan kemudian, dikurangi 1 hari
    (metode sama dengan skill surat-peringatan-karyawan); TIDAK digeser, ini tanggal hukum.
  - Semua tanggal checkpoint (bukan tanggal hukum) yang jatuh di hari libur (akhir pekan
    sesuai --hari-kerja, atau tanggal di file --libur) DIGESER ke hari kerja BERIKUTNYA,
    kecuali evaluasi akhir masa percobaan yang digeser ke hari kerja SEBELUMNYA (supaya
    evaluasi selesai sebelum batas hukum berakhir).

Contoh:
  python3 jadwal_onboarding.py --mulai 2026-09-28
  python3 jadwal_onboarding.py --mulai "5 Oktober 2026" --hari-kerja 6 --jenis pkwt --format csv
  python3 jadwal_onboarding.py --mulai 2026-10-01 --libur libur_nasional.csv --nama "Rina" --format json

File --libur: CSV dengan kolom "tanggal" (atau kolom pertama), satu tanggal libur per baris,
format bebas seperti --mulai. Baris kosong/komentar (#) diabaikan.

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Input salah -> pesan jelas, keluar kode 2.
"""
import argparse
import calendar
import csv
import io
import json
import re
import sys
from datetime import date, timedelta

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
          "Agustus", "September", "Oktober", "November", "Desember"]
BULAN_ALIAS = {
    "jan": 1, "januari": 1, "january": 1, "feb": 2, "peb": 2, "februari": 2, "pebruari": 2, "february": 2,
    "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6, "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "nopember": 11, "november": 11, "des": 12, "dec": 12, "desember": 12, "december": 12,
}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


class InputSalah(Exception):
    pass


def parse_tanggal(teks, label="tanggal"):
    """Terima 2026-09-28, 28-09-2026, 28/09/2026, 28.09.2026, '28 September 2026', '28 Sep 2026'."""
    s = (teks or "").strip()
    if not s:
        raise InputSalah("{} kosong. Contoh format: 28-09-2026 atau 28 September 2026.".format(label))
    try:
        m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", s)
        if m:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        m = re.fullmatch(r"(?:[A-Za-z]+,\s*)?(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", s)
        if m:
            b = BULAN_ALIAS.get(m.group(2).lower())
            if b is None:
                raise InputSalah("{}: nama bulan '{}' tidak dikenali.".format(label, m.group(2)))
            return date(int(m.group(3)), b, int(m.group(1)))
    except ValueError:
        raise InputSalah("{}: tanggal '{}' tidak ada di kalender (cek hari/bulan).".format(label, s))
    raise InputSalah("{}: format '{}' tidak dikenali. Pakai 28-09-2026, 2026-09-28, atau 28 September 2026."
                      .format(label, s))


def fmt(d):
    return "{}, {} {} {}".format(HARI[d.weekday()], d.day, BULAN[d.month - 1], d.year)


def fmt_pendek(d):
    return "{} {} {}".format(d.day, BULAN[d.month - 1], d.year)


def tambah_bulan(d, n):
    total = d.month - 1 + n
    tahun = d.year + total // 12
    bulan = total % 12 + 1
    hari = min(d.day, calendar.monthrange(tahun, bulan)[1])
    return date(tahun, bulan, hari)


def baca_libur(path):
    """Baca file CSV berisi tanggal libur nasional/perusahaan. Kembalikan set(date)."""
    hasil = set()
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            isi = f.read()
    except OSError as e:
        raise InputSalah("--libur: tidak bisa membaca file '{}' ({}).".format(path, e))
    r = csv.reader(io.StringIO(isi))
    baris_ke = 0
    for row in r:
        baris_ke += 1
        if not row:
            continue
        sel = row[0].strip()
        if not sel or sel.startswith("#"):
            continue
        if baris_ke == 1 and sel.lower() in ("tanggal", "date", "libur"):
            continue  # header kolom pertama
        try:
            hasil.add(parse_tanggal(sel, "--libur baris {}".format(baris_ke)))
        except InputSalah as e:
            raise InputSalah("{} isi='{}'".format(e, sel))
    return hasil


def hari_kerja_p(d, hari_kerja, libur):
    """True bila d adalah hari kerja: bukan akhir pekan (sesuai hari_kerja) dan bukan hari libur."""
    if d in libur:
        return False
    if hari_kerja == 6:
        return d.weekday() != 6  # Minggu libur
    return d.weekday() < 5  # Senin-Jumat kerja (Sabtu & Minggu libur)


def geser_maju(d, hari_kerja, libur, maks=60):
    n = 0
    while not hari_kerja_p(d, hari_kerja, libur):
        d = d + timedelta(days=1)
        n += 1
        if n > maks:
            raise InputSalah("Gagal mencari hari kerja berikutnya dari {} (terlalu banyak hari libur "
                              "berturut-turut, cek file --libur).".format(fmt_pendek(d)))
    return d


def geser_mundur(d, hari_kerja, libur, maks=60):
    n = 0
    while not hari_kerja_p(d, hari_kerja, libur):
        d = d - timedelta(days=1)
        n += 1
        if n > maks:
            raise InputSalah("Gagal mencari hari kerja sebelumnya dari {} (terlalu banyak hari libur "
                              "berturut-turut, cek file --libur).".format(fmt_pendek(d)))
    return d


def hitung_jadwal(mulai, hari_kerja=5, jenis="pkwtt", libur=None):
    if hari_kerja not in (5, 6):
        raise InputSalah("--hari-kerja harus 5 atau 6.")
    if jenis not in ("pkwt", "pkwtt"):
        raise InputSalah("--jenis harus 'pkwt' atau 'pkwtt'.")
    libur = libur or set()

    tahapan = []

    def tambah(kode, nama, tanggal_target, pj, kegiatan, geser="maju", catatan=""):
        asli = tanggal_target
        if geser == "maju":
            disesuaikan = geser_maju(tanggal_target, hari_kerja, libur)
        elif geser == "mundur":
            disesuaikan = geser_mundur(tanggal_target, hari_kerja, libur)
        else:
            disesuaikan = tanggal_target
        tahapan.append({
            "kode": kode,
            "tahap": nama,
            "tanggal_target": asli.isoformat(),
            "tanggal_target_teks": fmt_pendek(asli),
            "tanggal_disesuaikan": disesuaikan.isoformat(),
            "tanggal_disesuaikan_teks": fmt_pendek(disesuaikan),
            "digeser": disesuaikan != asli,
            "penanggung_jawab": pj,
            "kegiatan_target": kegiatan,
            "catatan": catatan,
        })

    tambah("h1", "Hari pertama (H1)", mulai, "Pemilik/Atasan langsung",
           "Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan",
           geser="tidak")
    tambah("minggu1", "Akhir minggu 1", mulai + timedelta(days=6), "Buddy/rekan pendamping",
           "Cek pemahaman tugas dasar & SOP harian, tanya kendala")
    tambah("hari30", "Evaluasi 30 hari", mulai + timedelta(days=29), "Atasan langsung",
           "Evaluasi checklist tugas dasar; beri umpan balik tertulis singkat")
    tambah("hari60", "Evaluasi 60 hari", mulai + timedelta(days=59), "Atasan langsung",
           "Evaluasi kemandirian kerja & kepatuhan SOP")
    tambah("hari90", "Evaluasi 90 hari / akhir orientasi", mulai + timedelta(days=89),
           "Pemilik/Atasan", "Evaluasi akhir masa orientasi (isi formulir evaluasi)")

    if jenis == "pkwtt":
        akhir_target = tambah_bulan(mulai, 3)
        if akhir_target.day < mulai.day:
            akhir_hukum = akhir_target
        else:
            akhir_hukum = akhir_target - timedelta(days=1)
        evaluasi_disarankan = geser_mundur(akhir_hukum, hari_kerja, libur)
        tahapan.append({
            "kode": "akhir_percobaan",
            "tahap": "Akhir masa percobaan (batas hukum)",
            "tanggal_target": akhir_hukum.isoformat(),
            "tanggal_target_teks": fmt_pendek(akhir_hukum),
            "tanggal_disesuaikan": evaluasi_disarankan.isoformat(),
            "tanggal_disesuaikan_teks": fmt_pendek(evaluasi_disarankan),
            "digeser": evaluasi_disarankan != akhir_hukum,
            "penanggung_jawab": "Pemilik/Atasan",
            "kegiatan_target": ("Keputusan lanjut sebagai karyawan tetap atau tidak (evaluasi disarankan "
                                 "selesai paling lambat hari kerja ini, SEBELUM tanggal hukum berakhir)"),
            "catatan": ("Masa percobaan maks. 3 bulan, upah selama percobaan tidak boleh di bawah upah "
                        "minimum (UU 13/2003 Pasal 60 jo. UU 6/2023). Tanggal ini TIDAK digeser walau "
                        "libur; hanya tanggal evaluasi yang disarankan dimajukan."),
        })
    else:
        tahapan.append({
            "kode": "akhir_percobaan",
            "tahap": "Masa percobaan",
            "tanggal_target": None,
            "tanggal_target_teks": "-",
            "tanggal_disesuaikan": None,
            "tanggal_disesuaikan_teks": "-",
            "digeser": False,
            "penanggung_jawab": "-",
            "kegiatan_target": "Tidak berlaku untuk PKWT",
            "catatan": ("PKWT (karyawan kontrak) DILARANG mensyaratkan masa percobaan; bila ada, batal "
                        "demi hukum (UU 13/2003 Pasal 58 jo. UU 6/2023; PP 35/2021 Pasal 12). Evaluasi "
                        "hari 30/60/90 di atas tetap dipakai sebagai pemantauan kinerja biasa, bukan syarat "
                        "kelulusan percobaan."),
        })

    return {
        "tanggal_mulai": mulai.isoformat(),
        "tanggal_mulai_teks": fmt(mulai),
        "hari_kerja_per_minggu": hari_kerja,
        "jenis_karyawan": jenis,
        "jumlah_hari_libur_dimuat": len(libur),
        "tahapan": tahapan,
    }


def ke_markdown(hasil, nama_karyawan=None):
    judul = "Jadwal Onboarding"
    if nama_karyawan:
        judul += " — {}".format(nama_karyawan)
    baris = [
        "# {}".format(judul),
        "",
        "Mulai kerja: **{}**  |  Hari kerja/minggu: **{}**  |  Jenis: **{}**".format(
            hasil["tanggal_mulai_teks"], hasil["hari_kerja_per_minggu"], hasil["jenis_karyawan"].upper()),
        "",
        "| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |",
        "|---|---|---|---|---|---|",
    ]
    for t in hasil["tahapan"]:
        digeser = "Ya" if t["digeser"] else "Tidak"
        baris.append("| {} | {} | {} | {} | {} | {} |".format(
            t["tahap"], t["tanggal_target_teks"], t["tanggal_disesuaikan_teks"], digeser,
            t["penanggung_jawab"], t["kegiatan_target"]))
    baris.append("")
    for t in hasil["tahapan"]:
        if t["catatan"]:
            baris.append("- **{}**: {}".format(t["tahap"], t["catatan"]))
    return "\n".join(baris) + "\n"


def ke_csv(hasil):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["kode", "tahap", "tanggal_target", "tanggal_disesuaikan", "digeser",
                "penanggung_jawab", "kegiatan_target", "catatan"])
    for t in hasil["tahapan"]:
        w.writerow([t["kode"], t["tahap"], t["tanggal_target_teks"], t["tanggal_disesuaikan_teks"],
                    "ya" if t["digeser"] else "tidak", t["penanggung_jawab"], t["kegiatan_target"],
                    t["catatan"]])
    return out.getvalue()


def main():
    p = argparse.ArgumentParser(description="Hitung jadwal onboarding karyawan baru.")
    p.add_argument("--mulai", required=True, help="Tanggal mulai kerja, mis. 2026-09-28")
    p.add_argument("--hari-kerja", type=int, default=5, choices=[5, 6],
                   help="Jumlah hari kerja per minggu (default 5)")
    p.add_argument("--jenis", default="pkwtt", choices=["pkwt", "pkwtt"],
                   help="Jenis hubungan kerja: pkwt (kontrak, tanpa masa percobaan) atau pkwtt (tetap, "
                        "default)")
    p.add_argument("--libur", help="Path file CSV tanggal libur nasional/perusahaan (opsional)")
    p.add_argument("--nama", help="Nama karyawan, untuk judul output saja (opsional)")
    p.add_argument("--format", choices=["markdown", "csv", "json"], default="markdown")
    a = p.parse_args()
    try:
        mulai = parse_tanggal(a.mulai, "--mulai")
        libur = baca_libur(a.libur) if a.libur else set()
        hasil = hitung_jadwal(mulai, hari_kerja=a.hari_kerja, jenis=a.jenis, libur=libur)
    except InputSalah as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        sys.exit(2)

    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    elif a.format == "csv":
        sys.stdout.write(ke_csv(hasil))
    else:
        print(ke_markdown(hasil, nama_karyawan=a.nama))


if __name__ == "__main__":
    main()
