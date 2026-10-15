#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hitung tanggal-tanggal kegiatan onboarding karyawan baru dari tanggal mulai kerja.

Tahap yang dihitung: hari pertama (H1), akhir minggu 1, evaluasi checkpoint 30/60/90 hari, dan
(khusus PKWTT) batas hukum + tanggal evaluasi keputusan akhir masa percobaan 3 bulan
(UU 13/2003 Pasal 60 jo. UU 6/2023). PKWT (karyawan kontrak) TIDAK BOLEH ada masa percobaan
(PP 35/2021 Pasal 12; sejalan dengan UU 13/2003 Pasal 58 jo. UU 6/2023) -- lihat
references/dasar-hukum-onboarding.md.

Cara hitung tanggal (identik dengan penjelasan manual di SKILL.md langkah 3 -- jaga keduanya tetap sama):
  - H1                = tanggal mulai kerja (tidak digeser; diperingatkan bila jatuh di hari libur/akhir
                        pekan, saran tanggal kerja berikutnya diberikan tapi TIDAK otomatis dipakai).
  - Akhir minggu 1     = mulai + 6 hari kalender (hari ke-7); digeser MAJU ke hari kerja berikutnya.
  - Checkpoint 30/60/90 = mulai + 29/59/89 hari kalender (hari ke-30/60/90, inklusif); digeser MAJU.
    Checkpoint 90 hari HANYA pemantauan kinerja rutin -- untuk PKWTT ini BUKAN batas keputusan masa
    percobaan (lihat baris "evaluasi_percobaan" terpisah); bila jatuh setelah batas hukum, script
    menambahkan peringatan eksplisit di catatannya.
  - Batas hukum akhir masa percobaan (PKWTT) = tanggal yang sama persis 3 bulan kalender kemudian; bila
    bulan target tidak punya tanggal itu (mis. 31 Jan -> April cuma 30 hari), batas = hari TERAKHIR bulan
    target (tanpa dikurangi 1 hari lagi); bila tanggal itu ADA di bulan target, batas = tanggal itu
    dikurangi 1 hari. Contoh: mulai 14 Des 2026 -> 14 Mar 2027 - 1 hari = batas 13 Mar 2027. Tanggal batas
    hukum ini TIDAK PERNAH digeser walau jatuh di hari libur -- itu tanggal hukum tetap.
    CATATAN: cara menghitung tanggal PERSIS ini (termasuk klip akhir bulan) adalah TAFSIR umum yang
    dipakai skill ini -- UU 13/2003 Pasal 60 hanya menyebut "paling lama 3 (tiga) bulan" dan tidak
    merinci metode hitung tanggal per hari, ini BUKAN kepastian hukum. Ikuti tanggal yang tertulis di
    perjanjian kerja/surat pengangkatan bila berbeda, dan konsultasikan ke Disnaker/konsultan HR bila
    ragu -- lihat references/dasar-hukum-onboarding.md.
  - Evaluasi keputusan akhir masa percobaan (PKWTT) = hari kerja ke-5 dihitung MUNDUR dari batas hukum,
    dengan hari kerja terakhir yang <= batas hukum dihitung sebagai hari kerja ke-1 (jadi mundur 4 hari
    kerja lagi dari situ), supaya keputusan lanjut/tidak sempat diambil dan diproses SEBELUM batas hukum
    berakhir. Baris ini SELALU <= batas hukum, tidak pernah melewatinya.
  - Semua tanggal checkpoint (H1 dikecualikan, batas hukum dikecualikan) yang jatuh di hari libur (akhir
    pekan sesuai --hari-kerja, hari libur nasional/cuti bersama bawaan 2026 & 2027 di
    references/libur-nasional-*.csv yang dipakai OTOMATIS bila ditemukan, atau tanggal tambahan di
    --libur) DIGESER ke hari kerja BERIKUTNYA (checkpoint) atau SEBELUMNYA (evaluasi akhir percobaan,
    supaya evaluasi selesai sebelum batas hukum berakhir).
  - Cuti bersama (kolom "jenis"="cuti" di CSV libur bawaan): bagi pekerja SWASTA, cuti bersama pemerintah
    bersifat FAKULTATIF (mengikuti kebijakan/perjanjian kerja masing-masing perusahaan, sesuai SKB 3
    Menteri), bukan hari libur wajib seperti hari libur nasional. Secara DEFAULT skill ini tetap
    memperlakukan cuti bersama sebagai hari bukan-kerja (lebih aman: jadwal & evaluasi jadi lebih awal,
    tidak pernah lebih lambat dari seharusnya). Pakai --cuti-bersama-hari-kerja bila perusahaan pengguna
    TIDAK meliburkan cuti bersama, supaya tanggal-tanggal itu dihitung sebagai hari kerja biasa.

Contoh:
  python3 jadwal_onboarding.py --mulai 2026-09-28
  python3 jadwal_onboarding.py --mulai "5 Oktober 2026" --hari-kerja 6 --jenis pkwt --format csv
  python3 jadwal_onboarding.py --mulai 2026-10-01 --libur libur_tambahan.csv --nama "Rina" --format json
  python3 jadwal_onboarding.py --mulai 2026-10-01 --tanpa-libur-bawaan   # matikan libur nasional bawaan

Libur nasional & cuti bersama bawaan: dimuat otomatis dari references/libur-nasional-2026.csv dan
-2027.csv (folder sibling scripts/ di skill ini) bila file itu ada, sesuai tahun tanggal mulai s.d.
tahun+1. Sumber: SKB 3 Menteri (sama seperti skill kalender-pajak), cek ulang tiap tahun. Tahun di luar
2026-2027 tidak punya data bawaan -- script memberi peringatan dan pengguna perlu memakai --libur sendiri.

File --libur / file libur bawaan: CSV dengan kolom "tanggal" (atau kolom pertama) di baris pertama sebagai
data atau header, satu tanggal libur per baris, format bebas seperti --mulai. Baris kosong/komentar (#)
diabaikan; kolom lain (mis. "jenis", "keterangan") diabaikan.

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Input salah -> pesan jelas, keluar kode 2.
"""
import argparse
import calendar
import csv
import io
import json
import os
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

# Rentang tahun tanggal mulai yang didukung. Dibatasi jauh di bawah batas maksimum date() Python (9999)
# supaya perhitungan +3 bulan / +90 hari / geser hari kerja tidak pernah meluap (OverflowError) -- lihat
# temuan P3 "tanggal tahun 9999 atau di luar rentang -> Traceback".
TAHUN_MIN = 1900
TAHUN_MAKS = 9900

# Berapa hari kerja buffer antara evaluasi keputusan akhir masa percobaan dan batas hukum, supaya
# keputusan lanjut/tidak sempat diambil & diproses sebelum batas berakhir.
BUFFER_EVALUASI_PERCOBAAN_HARI_KERJA = 5

SKRIP_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCES_DIR = os.path.join(os.path.dirname(SKRIP_DIR), "references")


class InputSalah(Exception):
    pass


def _cek_rentang_tahun(d, label, s):
    """Tolak tahun di luar TAHUN_MIN..TAHUN_MAKS dengan pesan ramah, supaya perhitungan +3 bulan/+90 hari
    di bawah tidak pernah meluap (OverflowError -> Traceback), dan tahun tidak wajar ditolak lebih awal."""
    if d.year < TAHUN_MIN or d.year > TAHUN_MAKS:
        raise InputSalah("{}: tahun {} pada '{}' di luar rentang yang didukung ({}-{}). Cek kembali "
                          "tanggalnya.".format(label, d.year, s, TAHUN_MIN, TAHUN_MAKS))
    return d


def parse_tanggal(teks, label="tanggal"):
    """Terima 2026-09-28, 28-09-2026, 28/09/2026, 28.09.2026, '28 September 2026', '28 Sep 2026'."""
    s = (teks or "").strip()
    if not s:
        raise InputSalah("{} kosong. Contoh format: 28-09-2026 atau 28 September 2026.".format(label))
    try:
        m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
        if m:
            return _cek_rentang_tahun(date(int(m.group(1)), int(m.group(2)), int(m.group(3))), label, s)
        m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", s)
        if m:
            return _cek_rentang_tahun(date(int(m.group(3)), int(m.group(2)), int(m.group(1))), label, s)
        m = re.fullmatch(r"(?:[A-Za-z]+,\s*)?(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", s)
        if m:
            b = BULAN_ALIAS.get(m.group(2).lower())
            if b is None:
                raise InputSalah("{}: nama bulan '{}' tidak dikenali.".format(label, m.group(2)))
            return _cek_rentang_tahun(date(int(m.group(3)), b, int(m.group(1))), label, s)
    except (ValueError, OverflowError):
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


def _pisah_csv(isi):
    """Tebak pemisah kolom CSV: koma (default/bawaan) atau titik-koma (ekspor Excel lokal Indonesia,
    mis. 'tanggal;keterangan'). Dilihat dari baris data/header pertama yang bukan kosong/komentar."""
    for baris in isi.splitlines():
        s = baris.strip()
        if not s or s.startswith("#"):
            continue
        return ";" if s.count(";") > s.count(",") else ","
    return ","


def baca_libur(path, kecualikan_cuti_bersama=False):
    """Baca file CSV berisi tanggal libur nasional/perusahaan. Kolom pertama = tanggal (wajib); kolom
    kedua opsional = jenis ("libur" atau "cuti" -- cuti bersama). Pemisah koma atau titik-koma (ekspor
    Excel ID) sama-sama didukung. Kembalikan set(date).

    Cuti bersama bagi pekerja SWASTA bersifat FAKULTATIF (ikut kebijakan perusahaan, SKB 3 Menteri),
    bukan hari libur wajib. Bila kecualikan_cuti_bersama=True, baris berjenis "cuti" TIDAK dimasukkan ke
    hasil (dianggap hari kerja biasa) -- lihat --cuti-bersama-hari-kerja."""
    hasil = set()
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            isi = f.read()
    except OSError as e:
        raise InputSalah("--libur: tidak bisa membaca file '{}' ({}).".format(path, e))
    r = csv.reader(io.StringIO(isi), delimiter=_pisah_csv(isi))
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
        jenis = row[1].strip().lower() if len(row) > 1 else ""
        if kecualikan_cuti_bersama and jenis == "cuti":
            continue  # cuti bersama fakultatif utk swasta -- dianggap hari kerja bila flag aktif
        try:
            hasil.add(parse_tanggal(sel, "--libur baris {}".format(baris_ke)))
        except InputSalah as e:
            raise InputSalah("{} isi='{}'".format(e, sel))
    return hasil


def libur_bawaan(tahun_dari, tahun_sampai, kecualikan_cuti_bersama=False):
    """Muat references/libur-nasional-<tahun>.csv (bila ada) untuk tahun_dari..tahun_sampai inklusif.
    Kembalikan (set(date) gabungan, list tahun yang filenya ditemukan, list tahun yang TIDAK ada filenya)."""
    gabungan = set()
    ditemukan = []
    tidak_ada = []
    for tahun in range(tahun_dari, tahun_sampai + 1):
        path = os.path.join(REFERENCES_DIR, "libur-nasional-{}.csv".format(tahun))
        if os.path.isfile(path):
            gabungan |= baca_libur(path, kecualikan_cuti_bersama=kecualikan_cuti_bersama)
            ditemukan.append(tahun)
        else:
            tidak_ada.append(tahun)
    return gabungan, ditemukan, tidak_ada


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


def mundur_n_hari_kerja(d, n, hari_kerja, libur, maks=90):
    """Dari d (boleh bukan hari kerja), cari hari kerja ke-n mundur (n=1 -> hari kerja <= d yang
    terakhir; n=BUFFER -> n hari kerja sebelum itu, dihitung mundur satu per satu)."""
    hasil = geser_mundur(d, hari_kerja, libur, maks=maks)
    for _ in range(n - 1):
        hasil = geser_mundur(hasil - timedelta(days=1), hari_kerja, libur, maks=maks)
    return hasil


def hitung_batas_hukum_percobaan(mulai):
    """Batas hukum akhir masa percobaan PKWTT: tanggal sama persis 3 bulan kalender kemudian; bila bulan
    target tidak punya tanggal itu, pakai hari terakhir bulan itu (tanpa -1 hari lagi); bila ada,
    dikurangi 1 hari. Lihat penjelasan lengkap di header modul ini & SKILL.md langkah 3."""
    target = tambah_bulan(mulai, 3)
    if target.day < mulai.day:
        return target  # sudah diklip ke hari terakhir bulan target
    return target - timedelta(days=1)


def hitung_jadwal(mulai, hari_kerja=5, jenis="pkwtt", libur=None, libur_bawaan_info=None,
                   cuti_bersama_hari_kerja=False):
    if hari_kerja not in (5, 6):
        raise InputSalah("--hari-kerja harus 5 atau 6.")
    if jenis not in ("pkwt", "pkwtt"):
        raise InputSalah("--jenis harus 'pkwt' atau 'pkwtt'.")
    libur = libur or set()

    tahapan = []
    peringatan = []

    def tambah(kode, nama, tanggal_target, pj, kegiatan, geser="maju", catatan=""):
        asli = tanggal_target
        if geser == "maju":
            disesuaikan = geser_maju(tanggal_target, hari_kerja, libur)
        elif geser == "mundur":
            disesuaikan = geser_mundur(tanggal_target, hari_kerja, libur)
        else:
            disesuaikan = tanggal_target
        entri = {
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
        }
        tahapan.append(entri)
        return entri

    # --- H1: tidak digeser, hanya diperingatkan bila jatuh di hari bukan kerja ---
    h1_entri = tambah("h1", "Hari pertama (H1)", mulai, "Pemilik/Atasan langsung",
                       "Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan",
                       geser="tidak")
    if not hari_kerja_p(mulai, hari_kerja, libur):
        saran = geser_maju(mulai, hari_kerja, libur)
        pesan = ("⚠️ Tanggal mulai {} jatuh di hari libur/akhir pekan (bukan hari kerja). H1 TIDAK "
                 "otomatis digeser -- konfirmasi ke pengguna, saran: geser ke hari kerja berikutnya, "
                 "{}.".format(fmt_pendek(mulai), fmt_pendek(saran)))
        h1_entri["catatan"] = pesan
        peringatan.append(pesan)

    tambah("minggu1", "Akhir minggu 1", mulai + timedelta(days=6), "Buddy/rekan pendamping",
           "Cek pemahaman tugas dasar & SOP harian, tanya kendala")
    tambah("hari30", "Checkpoint 30 hari", mulai + timedelta(days=29), "Atasan langsung",
           "Evaluasi checklist tugas dasar; beri umpan balik tertulis singkat")
    tambah("hari60", "Checkpoint 60 hari", mulai + timedelta(days=59), "Atasan langsung",
           "Evaluasi kemandirian kerja & kepatuhan SOP")
    catatan_90 = ("Pemantauan kinerja rutin, BUKAN batas keputusan masa percobaan." if jenis == "pkwtt"
                  else "Evaluasi akhir orientasi (isi formulir evaluasi kinerja).")
    hari90_entri = tambah("hari90", "Checkpoint 90 hari", mulai + timedelta(days=89),
                           "Pemilik/Atasan", "Evaluasi checkpoint orientasi", catatan=catatan_90)

    if jenis == "pkwtt":
        akhir_hukum = hitung_batas_hukum_percobaan(mulai)
        tahapan.append({
            "kode": "batas_percobaan",
            "tahap": "Batas hukum akhir masa percobaan (PKWTT)",
            "tanggal_target": akhir_hukum.isoformat(),
            "tanggal_target_teks": fmt_pendek(akhir_hukum),
            "tanggal_disesuaikan": akhir_hukum.isoformat(),
            "tanggal_disesuaikan_teks": fmt_pendek(akhir_hukum),
            "digeser": False,
            "penanggung_jawab": "-",
            "kegiatan_target": "Tanggal hukum tetap (informasi, bukan tanggal kegiatan) -- TIDAK PERNAH "
                                "digeser walau jatuh di hari libur.",
            "catatan": ("Masa percobaan maksimal 3 bulan sejak {} (UU 13/2003 Pasal 60 jo. UU 6/2023). "
                        "Definisi batas (TAFSIR perhitungan ini, bukan kepastian hukum -- UU tidak merinci cara "
                        "hitung tanggal per hari): tanggal sama persis 3 bulan kalender kemudian; bila "
                        "bulan target tidak punya tanggal itu, pakai hari terakhir bulan itu; bila ada, "
                        "dikurangi 1 hari. Ikuti tanggal di perjanjian kerja bila berbeda; konsultasikan "
                        "ke Disnaker/konsultan HR bila ragu.".format(fmt_pendek(mulai))),
        })
        evaluasi_percobaan = mundur_n_hari_kerja(akhir_hukum, BUFFER_EVALUASI_PERCOBAAN_HARI_KERJA,
                                                  hari_kerja, libur)
        tahapan.append({
            "kode": "evaluasi_percobaan",
            "tahap": "Evaluasi keputusan akhir masa percobaan (PKWTT)",
            "tanggal_target": evaluasi_percobaan.isoformat(),
            "tanggal_target_teks": fmt_pendek(evaluasi_percobaan),
            "tanggal_disesuaikan": evaluasi_percobaan.isoformat(),
            "tanggal_disesuaikan_teks": fmt_pendek(evaluasi_percobaan),
            "digeser": False,
            "penanggung_jawab": "Pemilik/Atasan",
            "kegiatan_target": ("Isi formulir evaluasi & putuskan lanjut sebagai karyawan tetap atau "
                                 "tidak, SELALU sebelum/tepat batas hukum di atas ({} hari kerja lebih "
                                 "awal, supaya keputusan sempat diproses).".format(
                                     BUFFER_EVALUASI_PERCOBAAN_HARI_KERJA)),
            "catatan": ("Terpisah dari checkpoint 90 hari di atas. Upah selama masa percobaan tidak boleh "
                        "di bawah upah minimum (UU 13/2003 Pasal 60 jo. UU 6/2023), kecuali usaha mikro & "
                        "kecil (⚠️ PERLU REVIEW: Pasal 90B jo. UU 6/2023 & PP 36/2021 Pasal 36 jo. PP "
                        "51/2023 -- lihat references/dasar-hukum-onboarding.md)."),
        })
        if date.fromisoformat(hari90_entri["tanggal_disesuaikan"]) > akhir_hukum:
            pesan = ("⚠️ Checkpoint 90 hari ({}) jatuh SETELAH batas hukum masa percobaan ({}). Jangan "
                     "pakai checkpoint 90 hari untuk keputusan lanjut/tidak -- pakai baris \"Evaluasi "
                     "keputusan akhir masa percobaan\" ({}).".format(
                         hari90_entri["tanggal_disesuaikan_teks"], fmt_pendek(akhir_hukum),
                         fmt_pendek(evaluasi_percobaan)))
            hari90_entri["catatan"] = (hari90_entri["catatan"] + " " + pesan).strip()
            peringatan.append(pesan)
    else:
        tahapan.append({
            "kode": "percobaan_pkwt",
            "tahap": "Masa percobaan",
            "tanggal_target": None,
            "tanggal_target_teks": "-",
            "tanggal_disesuaikan": None,
            "tanggal_disesuaikan_teks": "-",
            "digeser": False,
            "penanggung_jawab": "-",
            "kegiatan_target": "Tidak berlaku untuk PKWT",
            "catatan": ("PKWT (karyawan kontrak) DILARANG mensyaratkan masa percobaan (PP 35/2021 Pasal "
                        "12); bila tetap dicantumkan, klausul itu batal demi hukum dan masa kerja tetap "
                        "dihitung (sejalan dengan UU 13/2003 Pasal 58 jo. UU 6/2023). Checkpoint "
                        "30/60/90 di atas tetap dipakai sebagai pemantauan kinerja biasa (isi formulir "
                        "evaluasi kinerja versi PKWT), bukan syarat kelulusan percobaan."),
        })

    return {
        "tanggal_mulai": mulai.isoformat(),
        "tanggal_mulai_teks": fmt(mulai),
        "hari_kerja_per_minggu": hari_kerja,
        "jenis_karyawan": jenis,
        "jumlah_hari_libur_dimuat": len(libur),
        "libur_bawaan_ditemukan": (libur_bawaan_info or {}).get("ditemukan", []),
        "libur_bawaan_tidak_ada": (libur_bawaan_info or {}).get("tidak_ada", []),
        "cuti_bersama_dianggap_hari_kerja": cuti_bersama_hari_kerja,
        "peringatan": peringatan,
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
    ]
    if hasil.get("peringatan"):
        for p in hasil["peringatan"]:
            baris.append("> {}".format(p))
        baris.append("")
    baris += [
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
    if hasil.get("libur_bawaan_tidak_ada"):
        baris.append("- Tidak ada data libur nasional bawaan untuk tahun {} -- tambahkan sendiri lewat "
                      "`--libur`.".format(", ".join(str(y) for y in hasil["libur_bawaan_tidak_ada"])))
    if hasil.get("cuti_bersama_dianggap_hari_kerja"):
        baris.append("- `--cuti-bersama-hari-kerja` aktif: tanggal cuti bersama dihitung sebagai hari "
                      "kerja biasa (hanya hari libur nasional yang meliburkan jadwal), karena cuti "
                      "bersama bersifat fakultatif bagi pekerja swasta.")
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
    p.add_argument("--libur", help="Path file CSV tanggal libur tambahan/perusahaan (opsional, "
                                    "digabung dengan libur nasional bawaan)")
    p.add_argument("--tanpa-libur-bawaan", action="store_true",
                   help="Matikan pemuatan otomatis references/libur-nasional-*.csv")
    p.add_argument("--cuti-bersama-hari-kerja", action="store_true",
                   help="Anggap tanggal cuti bersama (jenis=cuti di CSV libur) sebagai hari kerja biasa -- "
                        "pakai bila perusahaan pengguna TIDAK meliburkan cuti bersama (fakultatif bagi "
                        "swasta, SKB 3 Menteri). Default: cuti bersama tetap dihitung sebagai libur.")
    p.add_argument("--nama", help="Nama karyawan, untuk judul output saja (opsional)")
    p.add_argument("--format", choices=["markdown", "csv", "json"], default="markdown")
    a = p.parse_args()
    try:
        mulai = parse_tanggal(a.mulai, "--mulai")
        libur = set()
        info_bawaan = {"ditemukan": [], "tidak_ada": []}
        if not a.tanpa_libur_bawaan:
            libur, ditemukan, tidak_ada = libur_bawaan(
                mulai.year, mulai.year + 1, kecualikan_cuti_bersama=a.cuti_bersama_hari_kerja)
            info_bawaan = {"ditemukan": ditemukan, "tidak_ada": tidak_ada}
        if a.libur:
            libur |= baca_libur(a.libur, kecualikan_cuti_bersama=a.cuti_bersama_hari_kerja)
        hasil = hitung_jadwal(mulai, hari_kerja=a.hari_kerja, jenis=a.jenis, libur=libur,
                               libur_bawaan_info=info_bawaan,
                               cuti_bersama_hari_kerja=a.cuti_bersama_hari_kerja)
    except (InputSalah, OverflowError) as e:
        pesan = e if isinstance(e, InputSalah) else (
            "Tanggal di luar rentang yang bisa dihitung (terlalu ekstrem). Gunakan tahun antara {} dan "
            "{}.".format(TAHUN_MIN, TAHUN_MAKS))
        print("ERROR: {}".format(pesan), file=sys.stderr)
        sys.exit(2)

    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    elif a.format == "csv":
        sys.stdout.write(ke_csv(hasil))
    else:
        print(ke_markdown(hasil, nama_karyawan=a.nama))


if __name__ == "__main__":
    main()
