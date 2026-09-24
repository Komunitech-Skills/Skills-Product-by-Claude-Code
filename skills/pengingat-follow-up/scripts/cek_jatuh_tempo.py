#!/usr/bin/env python3
"""Daftar pantauan follow-up (prospek, piutang, timesheet, janji) + rekap harian + rekap timesheet.

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Lintas OS (Windows: `python`/`py`).
Semua file berada di folder kerja pengguna (default `pengingat/`).

Subperintah
  tambah     Tambah item:      tambah --jenis piutang --nama "Bu Rina" --tanggal "3/10" --nominal "4,5 jt" --perihal "INV-012"
  daftar     Lihat item aktif: daftar [--semua]
  selesai    Tandai selesai:   selesai --id 3            (bisa "3,5")
  tunda      Pindah tanggal:   tunda --id 3 --ke "Senin"
  ubah       Ubah kolom:       ubah --id 3 [--tanggal ..] [--nominal ..] [--nama ..] [--perihal ..] [--catatan ..] [--jenis ..] [--status aktif|selesai]
  hapus      Hapus baris:      hapus --id 3              (hapus permanen, untuk data minimal)
  terkirim   Catat pesan sudah dikirim pemilik (nada draf berikutnya menyesuaikan):
                               terkirim --id 3 [--berikutnya "3 hari lagi"]
  bersihkan  Hapus item selesai yang tanggalnya > N hari lalu:  bersihkan --lebih-dari 30
  rekap      Rekap harian:     rekap [--teks] [--maks-draf 10]
  draf       Draf satu item:   draf --id 3
  catat-jam  Catat timesheet:  catat-jam --klien "PT Maju" --jam "1:30" [--tanggal "hari ini"] [--tarif "150rb"] [--keterangan ".."]
  timesheet  Rekap jam & nilai per klien: timesheet [--periode minggu-ini|minggu-lalu|bulan-ini|bulan-lalu] [--dari ..] [--sampai ..] [--klien ..] [--tarif ..] [--teks]

Opsi umum: --file (default pengingat/DAFTAR.csv), --timesheet-file (default pengingat/timesheet.csv),
--hari-ini (tanggal acuan untuk uji, format bebas), --tz (default Asia/Jakarta; WIB/WITA/WIT juga diterima).

Aturan
  - Tanggal: ISO (2026-10-03), 03-10-2026, 3/10/2026, 3/10, 3 Okt, 3 Oktober 2026, "tgl 3", "besok",
    "lusa", "hari ini", "3 hari lagi", "+3", "Jumat". Urutan selalu hari/bulan (format Indonesia).
    Tahun tidak disebut -> dipilih tanggal terdekat KE DEPAN (>= hari ini) dan diberi catatan;
    kecuali tanggal itu baru lewat <= 60 hari (mis. "20 Sep" diucapkan 1 Okt) -> tahun ini, item TERLAMBAT.
    Tanggal lama tanpa tahun di dalam CSV (diedit manual) -> dipilih tanggal terdekat (maju/mundur).
    Tanggal kerja (catat-jam/timesheet): nama hari = hari itu yang terakhir sudah lewat (termasuk hari ini);
    tanggal kerja di masa depan ditolak.
  - Nominal: 4,5 jt | 4.500.000 | Rp4.500.000 | 750rb | 1,2 M | 4 jt 500 rb. Disimpan bilangan bulat rupiah.
    Ditolak sebagai ambigu: 'm' kecil (juta/miliar?), '4,5,6 jt', '1,500 jt', '1.500 jt'. >= Rp 1 M diberi catatan.
  - Total nominal = penjumlahan bilangan bulat (tanpa float).
  - Timesheet: jam 1:30 | 1,5 | 1.5 | 90m | 90 menit | 2 jam | 1j30m ('1.30' ditolak: jam:menit atau desimal?). Nilai per klien = sum(menit x tarif / 60)
    dihitung pecahan persis, lalu dibulatkan SEKALI ke rupiah terdekat (0,5 ke atas) per klien.
    Total semua klien = jumlah nilai per klien yang sudah dibulatkan.
  - Baris rusak tidak membuat script berhenti: dilaporkan di "baris_ditolak" dengan nomor baris & alasan,
    dan tetap ditulis ulang apa adanya di posisinya saat file disimpan. CSV UTF-8/BOM/ANSI(cp1252), ',' atau ';'.

Kode keluar: 0 = berhasil; 1 = input/perintah salah (pesan "ERROR: ..." di stderr); 2 = ditolak karena
berisi data kontak pribadi (pakai --simpan-kontak bila pemilik memang sengaja).
"""
import argparse
import csv
import io
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from fractions import Fraction

BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
            "September", "Oktober", "November", "Desember"]
BULAN_PENDEK = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
HARI_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
NAMA_BULAN = {}
for _i, _alias in enumerate([
        ("jan", "januari", "january"), ("feb", "febr", "februari", "pebruari", "february"),
        ("mar", "maret", "march"), ("apr", "april"), ("mei", "may"), ("jun", "juni", "june"),
        ("jul", "juli", "july"), ("agu", "agt", "ags", "agus", "agustus", "aug", "august"),
        ("sep", "sept", "september"), ("okt", "oktober", "oct", "october"),
        ("nov", "nop", "november", "nopember"), ("des", "desember", "dec", "december")], start=1):
    for _a in _alias:
        NAMA_BULAN[_a] = _i
NAMA_HARI = {"senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "jum'at": 4, "jumaat": 4,
             "sabtu": 5, "minggu": 6, "ahad": 6}
JENIS = ["piutang", "prospek", "timesheet", "janji", "lainnya"]
STATUS = ["aktif", "selesai"]
KOLOM = ["id", "jenis", "nama", "tanggal", "nominal", "perihal", "status", "catatan", "dibuat", "diingatkan"]
KOLOM_TS = ["tanggal", "klien", "jam", "tarif_per_jam", "keterangan"]
TZ_TETAP = {"asia/jakarta": 7, "asia/pontianak": 7, "wib": 7, "asia/makassar": 8, "wita": 8,
            "asia/jayapura": 9, "wit": 9}


BATAS_BARU_LEWAT = 60  # hari; tanggal tanpa tahun yang baru lewat <= 60 hari dianggap tahun ini (terlambat)


class InputSalah(Exception):
    pass


class DataPribadi(Exception):
    pass


# ---------------------------------------------------------------- waktu & tanggal
def hari_ini_di(tz_nama):
    kunci = (tz_nama or "Asia/Jakarta").strip()
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+
        return datetime.now(ZoneInfo(kunci)).date()
    except Exception:
        pass
    if kunci.lower() in TZ_TETAP:  # tanpa zoneinfo/tzdata (mis. Windows): WIB/WITA/WIT tanpa DST
        return datetime.now(timezone(timedelta(hours=TZ_TETAP[kunci.lower()]))).date()
    raise InputSalah(f"zona waktu '{tz_nama}' tidak dikenal. Pakai mis. Asia/Jakarta, Asia/Makassar, Asia/Jayapura")


def tgl_id(d, pendek=False):
    if pendek:
        return f"{d.day} {BULAN_PENDEK[d.month - 1]} {d.year}"
    return f"{HARI_ID[d.weekday()]}, {d.day} {BULAN_ID[d.month - 1]} {d.year}"


def _coba_tanggal(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def _pilih_tahun(hari, bulan, acuan, arah):
    kandidat = [c for c in (_coba_tanggal(acuan.year + k, bulan, hari) for k in (-1, 0, 1, 2, 3, 4)) if c]
    if not kandidat:
        raise InputSalah(f"tanggal {hari}/{bulan} tidak ada di kalender")
    if arah == "depan":
        lewat = [x for x in kandidat if acuan - timedelta(days=BATAS_BARU_LEWAT) <= x < acuan]
        if lewat:  # mis. "20 Sep" diucapkan 1 Okt: hampir pasti tagihan yang sudah telat, bukan tahun depan
            c = max(lewat)
            return c, (f"Tahun tidak disebut; dipakai {tgl_id(c, True)} yang baru lewat {(acuan - c).days} hari "
                       "(item masuk TERLAMBAT). Kalau maksudnya tahun depan, tulis tahunnya.")
        c = min(x for x in kandidat if x >= acuan)
    elif arah == "lalu":  # tanggal kerja/kejadian: kemunculan terakhir <= hari ini
        dekat_depan = [x for x in kandidat if acuan < x <= acuan + timedelta(days=BATAS_BARU_LEWAT)]
        if dekat_depan:  # mis. "3 Okt" diucapkan 2 Okt: jelas besok, biar pemanggil yang menolak
            return min(dekat_depan), None
        c = max(x for x in kandidat if x <= acuan)
        if (acuan - c).days <= BATAS_BARU_LEWAT:
            return c, None
        return c, f"Tahun tidak disebut; dipakai {tgl_id(c, True)} (sudah {(acuan - c).days} hari lalu). Ubah bila maksudnya lain."
    else:
        c = min(kandidat, key=lambda x: (abs((x - acuan).days), x))
    ket = "terdekat ke depan" if arah == "depan" else "terdekat dari hari ini"
    return c, f"Tahun tidak disebut; dipakai {tgl_id(c, True)} (tanggal {ket}). Ubah bila maksudnya lain."


def parse_tanggal(teks, acuan, arah="depan"):
    """Kembalikan (date, catatan|None).

    arah: 'depan' (jatuh tempo item baru), 'lalu' (tanggal jam kerja: kemunculan terakhir <= hari ini),
    atau 'terdekat' (data lama di CSV / batas periode).
    """
    if teks is None or str(teks).strip() == "":
        raise InputSalah("tanggal kosong")
    asli = str(teks).strip()
    s = asli.lower().replace(",", " ")
    s = re.sub(r"^(tgl\.?|tanggal)\s*", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    if s in ("hari ini", "hr ini", "sekarang", "today"):
        return acuan, None
    if s in ("besok", "bsk", "tomorrow"):
        return acuan + timedelta(days=1), None
    if s == "lusa":
        return acuan + timedelta(days=2), None
    if s in ("kemarin", "kmrn", "yesterday"):
        return acuan - timedelta(days=1), None
    m = re.fullmatch(r"\+?\s*(\d{1,3})\s*(hari|hr|h)?(\s*lagi)?", s)
    if m and (s.startswith("+") or m.group(2)):
        return acuan + timedelta(days=int(m.group(1))), None
    m = re.fullmatch(r"(\d{1,2})\s*minggu\s*lagi", s)
    if m:
        return acuan + timedelta(days=7 * int(m.group(1))), None
    if s == "minggu depan":
        return acuan + timedelta(days=7), "\"minggu depan\" diartikan 7 hari dari hari ini."
    # nama hari ("jumat", "hari jumat", "jumat depan", "senin ini", "senin lalu/kemarin")
    m = re.fullmatch(r"(hari )?([a-z']+)( depan| ini| lalu| kemarin| kmrn)?", s)
    if m and m.group(2) in NAMA_HARI:
        target = NAMA_HARI[m.group(2)]
        mundur = (acuan.weekday() - target) % 7
        if m.group(3) in (" lalu", " kemarin", " kmrn"):
            return acuan - timedelta(days=mundur or 7), None
        if arah == "lalu" or (arah == "terdekat" and m.group(3) is None and mundur <= 3):
            if m.group(3) == " depan":
                raise InputSalah(f"'{asli}' ada di masa depan")
            return acuan - timedelta(days=mundur), None
        selisih = (target - acuan.weekday()) % 7
        cat = None
        if selisih == 0:
            if m.group(3) == " ini":
                return acuan, None
            selisih = 7
            cat = f"Hari ini juga {HARI_ID[target]}; dipakai {HARI_ID[target]} depan. Ubah bila maksudnya hari ini."
        elif m.group(3) == " depan" and selisih < 7:
            cat = f"\"{m.group(2)} depan\" diartikan {HARI_ID[target]} terdekat berikutnya."
        return acuan + timedelta(days=selisih), cat
    # buang nama hari di depan tanggal lengkap ("jumat 3 oktober 2026")
    hari_disebut = None
    m = re.match(r"([a-z']+) (.*)$", s)
    if m and m.group(1) in NAMA_HARI:
        hari_disebut, s = NAMA_HARI[m.group(1)], m.group(2)
    hasil = _parse_tanggal_inti(s, asli, acuan, arah)
    if hari_disebut is not None and hasil[0].weekday() != hari_disebut:
        cat = f"Perhatian: {tgl_id(hasil[0], True)} jatuh pada hari {HARI_ID[hasil[0].weekday()]}, bukan {HARI_ID[hari_disebut]}."
        hasil = (hasil[0], (hasil[1] + " " if hasil[1] else "") + cat)
    return hasil


def _parse_tanggal_inti(s, asli, acuan, arah):
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        d = _coba_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if not d:
            raise InputSalah(f"tanggal '{asli}' tidak ada di kalender")
        return d, None
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})", s)
    if m:
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        d = _coba_tanggal(y, int(m.group(2)), int(m.group(1)))
        if not d:
            raise InputSalah(f"tanggal '{asli}' tidak ada di kalender (urutan dibaca hari/bulan/tahun)")
        return d, None
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})", s)
    if m:
        hari, bulan = int(m.group(1)), int(m.group(2))
        if not 1 <= bulan <= 12:
            raise InputSalah(f"tanggal '{asli}' tidak valid: bulan {bulan} (urutan dibaca hari/bulan)")
        return _pilih_tahun(hari, bulan, acuan, arah)
    m = re.fullmatch(r"(\d{1,2}) ?([a-z]+)\.?(?: (\d{2}|\d{4}))?", s)
    if m and m.group(2) in NAMA_BULAN:
        hari, bulan = int(m.group(1)), NAMA_BULAN[m.group(2)]
        if m.group(3):
            y = int(m.group(3))
            y = y + 2000 if y < 100 else y
            d = _coba_tanggal(y, bulan, hari)
            if not d:
                raise InputSalah(f"tanggal '{asli}' tidak ada di kalender")
            return d, None
        return _pilih_tahun(hari, bulan, acuan, arah)
    m = re.fullmatch(r"(\d{1,2})", s)
    if m:
        hari = int(m.group(1))
        if not 1 <= hari <= 31:
            raise InputSalah(f"tanggal '{asli}' tidak valid")
        y, bln = acuan.year, acuan.month
        for _ in range(14):
            c = _coba_tanggal(y, bln, hari)
            if arah == "lalu":
                break
            if c and (c >= acuan or arah != "depan"):
                return c, (f"Bulan tidak disebut; dipakai {tgl_id(c, True)} (tanggal {hari} terdekat"
                           f"{' ke depan' if arah == 'depan' else ''}). Ubah bila maksudnya lain.")
            bln += 1
            if bln > 12:
                y, bln = y + 1, 1
        if arah == "lalu":
            y, bln = acuan.year, acuan.month
            for _ in range(14):
                c = _coba_tanggal(y, bln, hari)
                if c and c <= acuan:
                    return c, None
                bln -= 1
                if bln < 1:
                    y, bln = y - 1, 12
        raise InputSalah(f"tanggal '{asli}' tidak bisa ditentukan")
    raise InputSalah(f"tanggal '{asli}' tidak dikenali. Contoh yang diterima: 2026-10-03, 3/10/2026, 3/10, 3 Okt, besok")


# ---------------------------------------------------------------- angka
def rupiah(n):
    if n is None:
        return "-"
    return ("-" if n < 0 else "") + "Rp " + f"{abs(int(n)):,}".replace(",", ".")


def bulat(x):
    """Pembulatan ke bilangan bulat terdekat, 0,5 ke atas (untuk nilai >= 0)."""
    if isinstance(x, Fraction):  # pembulatan persis tanpa lewat desimal/float
        q, r = divmod(x.numerator, x.denominator)
        return q + (1 if 2 * r >= x.denominator else 0)
    return int(Decimal(x).quantize(Decimal(1), ROUND_HALF_UP))


POLA_ANGKA_SAH = [
    r"\d+",                          # 4500000
    r"\d{1,3}(\.\d{3})+(,\d+)?",       # 4.500.000 / 4.500.000,50
    r"\d{1,3}(,\d{3})+(\.\d+)?",       # 4,500,000 / 4,500,000.50
    r"\d+,\d+",                      # 4,5
    r"\d+\.\d+",                     # 4.5
]


def _angka_desimal(teks, asli):
    """'4,5' / '4.5' / '4.500' / '4.500.000,50' / '4,500,000' -> Decimal. Pola lain (mis. '4,5,6') ditolak."""
    s = teks
    if not any(re.fullmatch(p, s) for p in POLA_ANGKA_SAH):
        raise InputSalah(f"angka '{asli}' tidak jelas (pemisah titik/koma tidak wajar). "
                         "Contoh yang benar: 4.500.000 | 4,5 jt | 750rb")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        bag = s.split(",")
        s = s.replace(",", ".") if len(bag) == 2 and len(bag[1]) != 3 else s.replace(",", "")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3):
        s = s.replace(".", "")
    try:
        return Decimal(s)
    except InvalidOperation:
        raise InputSalah(f"angka '{asli}' tidak bisa dibaca")


SATUAN = [("miliar", 10**9), ("milyar", 10**9), ("juta", 10**6), ("jt", 10**6), ("ribu", 10**3),
          ("rb", 10**3), ("k", 10**3), ("M", 10**9)]
BATAS_NOMINAL_BESAR = 10**9


def parse_nominal(teks):
    """Kembalikan (int rupiah | None, catatan|None)."""
    if teks is None or str(teks).strip() in ("", "-"):
        return None, None
    asli = str(teks).strip()
    if re.search(r"\d\s*m(?![a-zA-Z])", asli):
        raise InputSalah(f"nominal '{asli}' ambigu: 'm' kecil bisa berarti juta atau miliar. "
                         "Tulis 'jt' untuk juta, atau 'M'/'miliar' untuk miliar")
    # 'M' besar tunggal = miliar: tandai dulu, baru huruf lain dikecilkan
    s = re.sub(r"(?<=[\d\s])M(?![a-zA-Z])", "\x00", asli).lower().replace("\x00", "M")
    s = s.replace("rp.", "").replace("rp", "").replace("idr", "").strip()
    s = re.sub(r"[.,]-$", "", s).strip()
    if s.startswith("-"):
        raise InputSalah(f"nominal '{asli}' negatif")
    pola = r"(\d+(?:[.,]\d+)*)\s*(miliar|milyar|juta|jt|ribu|rb|k|M)(?![a-zA-Z])"
    potong = re.findall(pola, s)
    if potong and re.fullmatch(r"(?:\s*" + pola + r")+\s*", s):
        total = Decimal(0)
        for angka, satuan in potong:
            if not re.fullmatch(r"\d+([.,]\d+)?", angka) or re.fullmatch(r"\d{1,3}[.,]\d{3}", angka):
                raise InputSalah(f"nominal '{asli}' ambigu (titik/koma sebelum satuan). "
                                 "Tulis mis. 1500 jt, 1,5 jt, atau 1.500.000.000")
            total += Decimal(angka.replace(",", ".")) * dict(SATUAN)[satuan]
        nilai = total
    else:
        s2 = s.replace(" ", "")
        if not re.fullmatch(r"\d[\d.,]*", s2):
            raise InputSalah(f"nominal '{asli}' tidak dikenali. Contoh: 4,5 jt | 4.500.000 | Rp4.500.000 | 750rb")
        nilai = _angka_desimal(s2, asli)
    cat = None
    if nilai != nilai.to_integral_value():
        cat = f"Nominal {asli} dibulatkan ke rupiah terdekat."
    n = bulat(nilai)
    if n <= 0:
        raise InputSalah(f"nominal '{asli}' harus lebih dari 0")
    if n < 1000:
        cat = ((cat + " ") if cat else "") + f"Nominal {rupiah(n)} sangat kecil; cek lagi (maksudnya {asli} jt/rb?)."
    if n >= BATAS_NOMINAL_BESAR:
        cat = ((cat + " ") if cat else "") + f"Nominal {rupiah(n)} (>= Rp 1 miliar); pastikan angkanya benar."
    return n, cat


def parse_jam(teks):
    """Durasi kerja -> (menit int, catatan|None)."""
    if teks is None or str(teks).strip() == "":
        raise InputSalah("jam kosong")
    asli = str(teks).strip()
    s = asli.lower().replace(" ", "")
    cat = None
    m = re.fullmatch(r"(\d{1,2}):(\d{1,2})(:00)?", s)
    if m:
        if int(m.group(2)) >= 60:
            raise InputSalah(f"jam '{asli}' tidak valid (menit harus < 60)")
        menit = int(m.group(1)) * 60 + int(m.group(2))
    else:
        m2 = re.search(r"(\d+)([.,])(\d{2})(?!\d)", s)
        if m2 and m2.group(2) == ".":
            raise InputSalah(f"jam '{asli}' ambigu: {m2.group(1)} jam {m2.group(3)} menit, atau "
                             f"{m2.group(1)},{m2.group(3)} jam? Tulis {m2.group(1)}:{m2.group(3)} untuk jam:menit, "
                             f"atau pakai koma untuk desimal ({m2.group(1)},{m2.group(3)})")
        if m2 and int(m2.group(3)) < 60:
            cat = (f"{asli} dibaca {m2.group(1)},{m2.group(3)} jam (desimal). Kalau maksudnya "
                   f"{m2.group(1)} jam {m2.group(3)} menit, tulis {m2.group(1)}:{m2.group(3)}.")
        m = re.fullmatch(r"(?:(\d+(?:[.,]\d+)?)(?:jam|j|h))?(?:(\d+)(?:menit|mnt|min|m))?", s)
        if m and (m.group(1) or m.group(2)):
            jam = Decimal(m.group(1).replace(",", ".")) if m.group(1) else Decimal(0)
            menit_d = jam * 60 + (int(m.group(2)) if m.group(2) else 0)
        elif re.fullmatch(r"\d+(?:[.,]\d+)?", s):
            menit_d = Decimal(s.replace(",", ".")) * 60
        else:
            raise InputSalah(f"jam '{asli}' tidak dikenali. Contoh: 1:30 | 1,5 | 90m | 2 jam")
        menit = bulat(menit_d)
        if Decimal(menit) != menit_d:
            cat = ((cat + " ") if cat else "") + f"Durasi {asli} dibulatkan ke {menit} menit."
    if menit <= 0:
        raise InputSalah(f"jam '{asli}' harus lebih dari 0")
    if menit > 24 * 60:
        raise InputSalah(f"jam '{asli}' lebih dari 24 jam dalam satu baris; pecah per tanggal")
    return menit, cat


def teks_durasi(menit):
    j, m = divmod(menit, 60)
    bag = []
    if j:
        bag.append(f"{j} jam")
    if m:
        bag.append(f"{m} menit")
    return " ".join(bag) or "0 menit"


def jam_desimal(menit):
    d = (Decimal(menit) / 60).quantize(Decimal("0.01"), ROUND_HALF_UP).normalize()
    return format(d, "f").replace(".", ",")


# ---------------------------------------------------------------- privasi
POLA_KONTAK = [
    (re.compile(r"(?<!\d)(?:\+?62|0)[\s.-]?8\d(?:[\s.-]?\d){6,11}(?!\d)"), "nomor HP"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "alamat email"),
    (re.compile(r"(?<!\d)\d{16}(?!\d)"), "angka 16 digit (mirip NIK/No. KK)"),
]


def cek_kontak(nilai_dict):
    for kolom, teks in nilai_dict.items():
        for pola, label in POLA_KONTAK:
            if teks and pola.search(teks):
                return kolom, label
    return None


def aman_csv(teks):
    """Cegah teks dibaca sebagai rumus saat CSV dibuka di Excel/Sheets."""
    teks = (teks or "").replace("\r", " ").replace("\n", " ").strip()
    if teks[:1] in ("=", "+", "@") or (teks[:1] == "-" and len(teks) > 1 and teks[1] != " "):
        return "'" + teks
    return teks


# ---------------------------------------------------------------- file
def baca_csv(path, wajib):
    """Kembalikan (header, [(no_baris, dict|None, alasan|None, sel_mentah)], info). header None = file belum ada."""
    info = []
    if not os.path.exists(path):
        return None, [], info
    with open(path, "rb") as f:
        mentah = f.read()
    try:
        isi = mentah.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            isi = mentah.decode("cp1252")
        except UnicodeDecodeError:
            raise InputSalah(f"file {path} tidak bisa dibaca (encoding tidak dikenal). Buka di Excel lalu "
                             "Simpan Sebagai 'CSV UTF-8 (dipisahkan koma)'")
        info.append(f"File {os.path.basename(path)} berformat ANSI/Windows-1252 (dari Excel lama); dibaca "
                    "dengan aman dan akan disimpan ulang sebagai UTF-8 saat ada perubahan.")
    if not isi.strip():
        return [], [], info
    baris_pertama = isi.splitlines()[0]
    pemisah = ";" if baris_pertama.count(";") > baris_pertama.count(",") else ","
    pembaca = csv.reader(io.StringIO(isi), delimiter=pemisah)
    header = [h.strip().lower() for h in next(pembaca)]
    kurang = [k for k in wajib if k not in header]
    if kurang:
        raise InputSalah(f"file {path} tidak punya kolom wajib: {', '.join(kurang)}. "
                         f"Header yang dibutuhkan: {','.join(wajib)}")
    hasil = []
    for no, sel in enumerate(pembaca, start=2):
        if not any(x.strip() for x in sel):
            continue
        if len(sel) > len(header):
            hasil.append((no, None, f"jumlah kolom ({len(sel)}) lebih banyak dari header ({len(header)}); "
                                    "kemungkinan ada koma di dalam teks tanpa tanda kutip", sel))
            continue
        lengkap = sel + [""] * (len(header) - len(sel))
        hasil.append((no, {header[i]: lengkap[i].strip() for i in range(len(header))}, None, sel))
    return header, hasil, info


def tulis_csv_atomik(path, header, baris):
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", suffix=".csv", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            for b in baris:
                if isinstance(b, list):  # baris rusak: ditulis ulang apa adanya (hanya diamankan dari rumus)
                    w.writerow([aman_csv(x) for x in b])
                else:
                    w.writerow([aman_csv(str(b.get(k, "") or "")) for k in header])
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def muat_daftar(path):
    """Baris rusak TIDAK dibuang: disimpan sebagai {'_no', '_mentah'} di posisi aslinya agar ikut ditulis ulang."""
    header, isi, info = baca_csv(path, ["jenis", "nama", "tanggal"])
    if header is None:
        return list(KOLOM), [], [], info
    for k in KOLOM:
        if k not in header:
            header.append(k)
    baris, rusak = [], []
    for no, b, alasan, sel in isi:
        if b is None:
            rusak.append({"baris": no, "alasan": alasan})
            baris.append({"_no": no, "_mentah": sel})
            continue
        b["_no"] = no
        baris.append(b)
    return header, baris, rusak, info


def item_sah(baris):
    return [b for b in baris if "_mentah" not in b]


def simpan_daftar(path, header, baris):
    tulis_csv_atomik(path, header, [b["_mentah"] if "_mentah" in b else
                                    {k: v for k, v in b.items() if not k.startswith("_")} for b in baris])


def teks_rusak(rusak, info=()):
    L = [f"Catatan: {i}" for i in info]
    if rusak:
        L.append(f"PERHATIAN: {len(rusak)} baris di daftar tidak terbaca (tetap disimpan apa adanya, tidak ikut "
                 "direkap): " + "; ".join(f"baris {r['baris']}: {r['alasan']}" for r in rusak[:5]))
    return ("\n" + "\n".join(L)) if L else ""


def cari_id(baris, teks_id):
    ids = [x.strip().lstrip("#") for x in str(teks_id).split(",") if x.strip()]
    if not ids:
        raise InputSalah("--id kosong")
    hasil = []
    for i in ids:
        cocok = [b for b in item_sah(baris) if (b.get("id") or "").strip() == i]
        if not cocok:
            raise InputSalah(f"item #{i} tidak ada di daftar. Jalankan 'daftar --semua' untuk melihat nomor item")
        if len(cocok) > 1:
            raise InputSalah(f"nomor item #{i} dobel di file (baris {', '.join(str(c['_no']) for c in cocok)}); "
                             "perbaiki kolom id di CSV dulu")
        hasil.append(cocok[0])
    return hasil


def id_baru(baris):
    angka = [int(b["id"]) for b in item_sah(baris) if (b.get("id") or "").strip().isdigit()]
    return str(max(angka) + 1 if angka else 1)


# ---------------------------------------------------------------- item
def normal_jenis(teks):
    s = (teks or "").strip().lower()
    alias = {"tagihan": "piutang", "invoice": "piutang", "utang": "piutang", "hutang": "piutang", "bon": "piutang",
             "kasbon": "piutang", "nota": "piutang", "tempo": "piutang", "calon": "prospek",
             "lead": "prospek", "klien": "prospek", "jam": "timesheet", "janjian": "janji",
             "meeting": "janji", "rapat": "janji", "lain": "lainnya", "": "lainnya"}
    s = alias.get(s, s)
    if s not in JENIS:
        raise InputSalah(f"jenis '{teks}' tidak dikenal. Pilih: {', '.join(JENIS)}")
    return s


ALIAS_STATUS = {"aktif": "aktif", "belum": "aktif", "belum bayar": "aktif", "selesai": "selesai",
                "lunas": "selesai", "sudah bayar": "selesai", "sudah dibayar": "selesai", "beres": "selesai",
                "done": "selesai", "batal": "selesai", "": "aktif"}


def normal_status(teks):
    s = re.sub(r"\s+", " ", (teks or "").strip().lower())
    if s not in ALIAS_STATUS:
        raise InputSalah(f"status '{teks}' tidak dikenal (pakai aktif/selesai; 'lunas' juga diterima)")
    return ALIAS_STATUS[s]


def parse_diingatkan(teks):
    t = (teks or "").strip()
    if t == "":
        return 0
    if not t.isdigit():
        raise InputSalah(f"kolom diingatkan '{teks}' harus angka (jumlah pengingat yang sudah dikirim)")
    return int(t)


def tafsir_item(b, acuan):
    """Validasi satu baris daftar -> dict item siap rekap. Raise InputSalah bila rusak."""
    catatan = []
    jenis = normal_jenis(b.get("jenis"))
    nama = (b.get("nama") or "").strip().lstrip("'")
    if not nama:
        raise InputSalah("kolom nama kosong")
    status = normal_status(b.get("status"))
    diingatkan = parse_diingatkan(b.get("diingatkan"))
    tgl, cat = parse_tanggal(b.get("tanggal"), acuan, arah="terdekat")
    if cat:
        catatan.append(cat)
    nominal, cat = parse_nominal(b.get("nominal"))
    if cat:
        catatan.append(cat)
    return {"id": (b.get("id") or "").strip() or f"baris{b['_no']}", "jenis": jenis, "nama": nama,
            "tanggal": tgl.isoformat(), "tanggal_teks": tgl_id(tgl, True), "nominal": nominal,
            "nominal_teks": rupiah(nominal) if nominal is not None else "",
            "perihal": (b.get("perihal") or "").strip().lstrip("'"),
            "catatan": (b.get("catatan") or "").strip().lstrip("'"), "status": status, "diingatkan": diingatkan,
            "selisih_hari": (tgl - acuan).days, "_tgl": tgl, "_peringatan": catatan}


def sapaan(nama):
    return "Bapak/Ibu" if re.search(r"\d", nama) or re.fullmatch(r"[A-Z0-9-]{2,}", nama) else nama


def kapan_teks(selisih, tgl):
    """Kata waktu yang jujur: 'besok' hanya untuk H-1."""
    if selisih == 0:
        return f"hari ini, {tgl}"
    if selisih == 1:
        return f"besok, {tgl}"
    if selisih == 2:
        return f"lusa, {tgl}"
    return f"pada {tgl}"


def tahap_piutang(hari, diingatkan):
    """Tahap nada (selaras tagih-piutang). hari = hari terlambat (<0 = belum jatuh tempo)."""
    if hari < 0:
        return 1
    if hari == 0:
        return 2
    tahap = 3 if hari <= 6 else 4 if hari <= 13 else 5 if hari <= 29 else 6
    batas = (5 if hari >= 30 else 4) if diingatkan == 0 else 5 if diingatkan == 1 else 6
    return min(tahap, batas)


def draf_pesan(it, acuan):
    """Draf WA untuk pelanggan/klien (dikirim PEMILIK, bukan bot). None bila hanya pengingat pribadi."""
    s = sapaan(it["nama"])
    hari = -it["selisih_hari"]
    per = it["perihal"]
    nom = it["nominal_teks"]
    tgl = it["tanggal_teks"]
    n_ingat = it.get("diingatkan", 0)
    if it["jenis"] == "piutang":
        apa = f"pembayaran {per}" if per else "pembayaran tagihan"
        jumlah = f" sebesar {nom}" if nom else ""
        tahap = tahap_piutang(hari, n_ingat)
        if tahap == 1:
            return (f"Selamat pagi {s}, izin mengingatkan {apa}{jumlah} yang jatuh tempo "
                    f"{kapan_teks(-hari, tgl)}. Pembayaran bisa melalui [rekening]. Abaikan pesan ini jika "
                    "sudah membayar. Terima kasih.")
        if tahap == 2:
            return (f"Selamat pagi {s}, kami mengingatkan {apa}{jumlah} jatuh tempo hari ini, {tgl}. "
                    "Jika sudah transfer, mohon kirimkan bukti transfernya agar bisa kami catat. "
                    "Abaikan pesan ini jika sudah membayar. Terima kasih.")
        if tahap == 3:
            return (f"Selamat pagi {s}, mohon maaf mengganggu. Menurut catatan kami, {apa}{jumlah} yang jatuh "
                    f"tempo {tgl} belum kami terima. Mungkin terlewat; jika sudah transfer, mohon kirimkan "
                    "bukti transfernya. Jika belum, pembayaran bisa melalui [rekening]. Terima kasih.")
        if tahap == 4:
            batas = acuan + timedelta(days=3)
            return (f"Selamat pagi {s}. Kami menindaklanjuti {apa}{jumlah} yang sudah lewat {hari} hari dari "
                    f"jatuh tempo ({tgl}). Mohon informasikan tanggal pasti pembayarannya, paling lambat "
                    f"{tgl_id(batas, True)}. Jika ada kendala, kami terbuka membicarakan jadwal pembayaran. "
                    "Terima kasih.")
        batas = acuan + timedelta(days=7)
        return (f"Yth. {s}, bersama pesan ini kami sampaikan secara tertulis bahwa {apa}{jumlah} yang jatuh "
                f"tempo {tgl} sudah lewat {hari} hari dan belum kami terima. Mohon pembayaran diselesaikan "
                f"paling lambat {tgl_id(batas, True)} melalui [rekening], atau hubungi kami sebelum tanggal "
                "tersebut bila ingin membahas jadwal cicilan secara tertulis. Terima kasih atas perhatiannya.")
    if it["jenis"] == "prospek":
        topik = per or "pembicaraan kita sebelumnya"
        keluar = "Kalau belum jadi prioritas, cukup balas \"nanti\" saja, saya tidak akan mengganggu."
        if n_ingat >= 3:
            return (f"Halo {s}, ini pesan terakhir saya soal {topik} supaya tidak mengganggu. Kalau suatu saat "
                    "dibutuhkan, saya siap membantu kapan saja. Terima kasih atas waktunya.")
        if n_ingat == 2:
            return (f"Halo {s}, supaya lebih mudah memutuskan soal {topik}: apakah lebih cocok kita jadwalkan "
                    f"telepon singkat 10 menit, atau saya kirimkan pilihan yang lebih sederhana dulu? {keluar}")
        if n_ingat == 1:
            return (f"Halo {s}, menyambung {topik}: kalau ada pertanyaan yang belum terjawab (harga, waktu, "
                    f"atau contoh hasil), saya siap kirimkan infonya. {keluar}")
        if hari > 0:
            return (f"Halo {s}, mohon maaf baru menyapa lagi. Terkait {topik}, apakah masih relevan untuk "
                    f"{s} saat ini? Kalau ada yang ingin ditanyakan, saya siap bantu. {keluar}")
        return (f"Halo {s}, semoga harinya lancar. Saya ingin menindaklanjuti {topik}. Apakah ada yang bisa "
                f"saya bantu jelaskan lagi? {keluar}")
    if it["jenis"] == "timesheet":
        periode = per or "periode ini"
        return (f"Selamat sore {s}, berikut rekap jam kerja {periode}: total [TOTAL JAM], nilai [NILAI] "
                "(rincian per tanggal di bawah). Mohon konfirmasinya sebelum kami terbitkan invoice. "
                "Terima kasih.")
    if it["jenis"] == "janji" and hari <= 0:
        topik = f" untuk {per}" if per else ""
        return (f"Halo {s}, mengingatkan janji kita {kapan_teks(-hari, tgl)}{topik}. Apakah jadwalnya masih "
                "sesuai? Terima kasih.")
    return None


def saran_item(it):
    hari = -it["selisih_hari"]
    n = it.get("diingatkan", 0)
    if it["jenis"] == "piutang" and hari >= 7:
        if hari >= 30 and n >= 2:
            return ("Sudah >= 30 hari dan >= 2 kali diingatkan: pertimbangkan surat teguran (somasi) lewat "
                    "skill tagih-piutang (bukan nasihat hukum).")
        return ("Setelah pesan dikirim, balas \"terkirim " + str(it["id"]) + "\" agar nada berikutnya menyesuaikan. "
                "Denda (hanya jika tertulis di kontrak) atau surat resmi: skill tagih-piutang.")
    if it["jenis"] == "prospek":
        return ("Setelah dikirim, balas \"terkirim " + str(it["id"]) + " lanjut 3 hari lagi\" untuk follow-up "
                "berikutnya. Urutan lengkap: skill follow-up-prospek.")
    if it["jenis"] == "timesheet":
        return f"Isi angka dengan perintah: timesheet --klien \"{it['nama']}\" --periode <periode>."
    if it["jenis"] in ("janji", "lainnya") and hari > 0:
        return "Sudah lewat. Tandai selesai atau tunda ke tanggal baru."
    return None


# ---------------------------------------------------------------- rekap
def susun_rekap(path, acuan, maks_draf):
    header, baris, rusak, info = muat_daftar(path)
    grup = {"terlambat": [], "hari_ini": [], "besok": []}
    mendatang, peringatan = [], list(info)
    total_aktif = 0
    for b in item_sah(baris):
        try:
            it = tafsir_item(b, acuan)
        except InputSalah as e:
            rusak.append({"baris": b["_no"], "alasan": str(e)})
            continue
        if it["status"] != "aktif":
            continue
        total_aktif += 1
        for p in it.pop("_peringatan"):
            peringatan.append(f"Item #{it['id']}: {p}")
        temu = cek_kontak({"nama": it["nama"], "perihal": it["perihal"], "catatan": it["catatan"]})
        if temu:
            peringatan.append(f"Item #{it['id']}: kolom {temu[0]} berisi {temu[1]}; sebaiknya dihapus (data minimal).")
        d = it["selisih_hari"]
        if d < 0:
            it["hari_terlambat"] = -d
            grup["terlambat"].append(it)
        elif d == 0:
            grup["hari_ini"].append(it)
        elif d == 1:
            grup["besok"].append(it)
        elif d <= 7:
            mendatang.append(it)
    rusak.sort(key=lambda r: r["baris"])
    grup["terlambat"].sort(key=lambda x: (x["_tgl"], x["jenis"] != "piutang"))
    for k in ("hari_ini", "besok"):
        grup[k].sort(key=lambda x: (x["jenis"] != "piutang", x["nama"].lower()))
    mendatang.sort(key=lambda x: x["_tgl"])
    jml_draf = 0
    for k in ("terlambat", "hari_ini", "besok"):
        for it in grup[k]:
            pesan = draf_pesan(it, acuan)
            if pesan and jml_draf < maks_draf:
                it["draf"] = pesan
                jml_draf += 1
            elif pesan:
                it["draf"] = None
                it["draf_ditunda"] = True
            else:
                it["draf"] = None
            it["saran"] = saran_item(it)

    def piutang(items):
        return [i for i in items if i["jenis"] == "piutang" and i["nominal"] is not None]

    def jumlah(items):
        return sum(i["nominal"] for i in piutang(items))

    ringkas = {
        "piutang_terlambat": jumlah(grup["terlambat"]),
        "piutang_hari_ini": jumlah(grup["hari_ini"]),
        "piutang_besok": jumlah(grup["besok"]),
        "ada_piutang": bool(piutang(grup["terlambat"] + grup["hari_ini"] + grup["besok"])),
    }
    ringkas["total_tertunggak"] = ringkas["piutang_terlambat"] + ringkas["piutang_hari_ini"]
    ringkas["total_tertunggak_teks"] = rupiah(ringkas["total_tertunggak"])
    umur = {"1-30": [0, 0], "31-60": [0, 0], ">60": [0, 0]}
    for i in piutang(grup["terlambat"]):
        k = "1-30" if i["hari_terlambat"] <= 30 else "31-60" if i["hari_terlambat"] <= 60 else ">60"
        umur[k][0] += 1
        umur[k][1] += i["nominal"]
    ringkas["umur_piutang_terlambat"] = {k: {"jumlah_item": v[0], "nominal": v[1], "nominal_teks": rupiah(v[1])}
                                         for k, v in umur.items()}
    for it in [*grup["terlambat"], *grup["hari_ini"], *grup["besok"], *mendatang]:
        it.pop("_tgl", None)
        it.pop("_peringatan", None)
    hasil = {"ok": True, "hari_ini": acuan.isoformat(), "hari_ini_teks": tgl_id(acuan),
             "file": path, "file_ada": os.path.exists(path), "jumlah_aktif": total_aktif,
             "terlambat": grup["terlambat"], "jatuh_tempo_hari_ini": grup["hari_ini"], "besok_h_1": grup["besok"],
             "tujuh_hari_ke_depan": [{"id": i["id"], "jenis": i["jenis"], "nama": i["nama"],
                                     "tanggal_teks": i["tanggal_teks"]} for i in mendatang],
             "ringkasan": ringkas, "baris_ditolak": rusak, "peringatan": peringatan,
             "kosong": not (grup["terlambat"] or grup["hari_ini"] or grup["besok"])}
    hasil["teks"] = teks_rekap(hasil)
    return hasil


def _baris_item(i, it, keterangan):
    bagian = [f"{i}. #{it['id']} {it['jenis'].capitalize()} - {it['nama']}"]
    if it["nominal_teks"]:
        bagian.append(it["nominal_teks"])
    if it["perihal"]:
        bagian.append(it["perihal"])
    bagian.append(keterangan)
    if it.get("diingatkan"):
        bagian.append(f"sudah diingatkan {it['diingatkan']}x")
    s = " | ".join(bagian)
    if it.get("catatan"):
        s += f"\n   Catatan: {it['catatan']}"
    return s


def teks_rekap(h):
    L = [f"PENGINGAT FOLLOW-UP - {h['hari_ini_teks']}", ""]
    if not h["file_ada"]:
        L.append(f"Daftar pantauan belum ada ({h['file']}). Tambahkan item dulu, mis. "
                 "\"ingatkan saya tagih Bu Rina tgl 3 Rp4,5 jt\".")
    elif h["kosong"]:
        L.append("Tidak ada yang jatuh tempo hari ini, besok, atau terlambat.")
        if h["tujuh_hari_ke_depan"]:
            L.append("7 hari ke depan: " + "; ".join(
                f"#{i['id']} {i['nama']} ({i['tanggal_teks']})" for i in h["tujuh_hari_ke_depan"]))
    else:
        if h["terlambat"]:
            L.append(f"TERLAMBAT ({len(h['terlambat'])})")
            for n, it in enumerate(h["terlambat"], 1):
                label = "jatuh tempo" if it["jenis"] == "piutang" else "jadwal"
                L.append(_baris_item(n, it, f"lewat {it['hari_terlambat']} hari ({label} {it['tanggal_teks']})"))
            L.append("")
        if h["jatuh_tempo_hari_ini"]:
            L.append(f"HARI INI ({len(h['jatuh_tempo_hari_ini'])})")
            for n, it in enumerate(h["jatuh_tempo_hari_ini"], 1):
                L.append(_baris_item(n, it, "jatuh tempo hari ini" if it["jenis"] == "piutang" else "hari ini"))
            L.append("")
        if h["besok_h_1"]:
            L.append(f"BESOK / H-1 ({len(h['besok_h_1'])})")
            for n, it in enumerate(h["besok_h_1"], 1):
                L.append(_baris_item(n, it, f"besok, {it['tanggal_teks']}"))
            L.append("")
        r = h["ringkasan"]
        if r["ada_piutang"]:
            L.append(f"Total piutang tertunggak (terlambat + hari ini): {r['total_tertunggak_teks']}")
            u = r["umur_piutang_terlambat"]
            if any(v["jumlah_item"] for v in u.values()):
                L.append("Umur piutang terlambat: " + " | ".join(
                    f"{k} hari: {v['nominal_teks']} ({v['jumlah_item']})" for k, v in u.items() if v["jumlah_item"]))
            if r["piutang_besok"]:
                L.append(f"Piutang jatuh tempo besok: {rupiah(r['piutang_besok'])}")
        if h["tujuh_hari_ke_depan"]:
            L.append("Menyusul 7 hari ke depan: " + "; ".join(
                f"#{i['id']} {i['nama']} ({i['tanggal_teks']})" for i in h["tujuh_hari_ke_depan"]))
        draf = [it for k in ("terlambat", "jatuh_tempo_hari_ini", "besok_h_1") for it in h[k]]
        ada_draf = [it for it in draf if it.get("draf")]
        if ada_draf:
            L += ["", "DRAF PESAN (cek dulu, lalu salin & kirim sendiri dari WA/email Anda)"]
            for it in ada_draf:
                L += ["", f"#{it['id']} untuk {it['nama']}:", it["draf"]]
                if it.get("saran"):
                    L.append(f"(Saran: {it['saran']})")
        ditunda = [f"#{it['id']}" for it in draf if it.get("draf_ditunda")]
        if ditunda:
            L += ["", f"Draf untuk {', '.join(ditunda)} belum ditampilkan agar pesan tidak terlalu panjang. "
                      "Minta: \"draf <nomor>\"."]
        L += ["", "Balas misalnya: \"selesai 3\", \"terkirim 3\", \"tunda 3 ke Senin\", \"hapus 3\"."]
    if h["baris_ditolak"]:
        L += ["", f"PERHATIAN: {len(h['baris_ditolak'])} baris di daftar tidak terbaca dan TIDAK ikut direkap "
                  "(baris tetap disimpan di file; perbaiki lalu rekap ulang):"]
        for r in h["baris_ditolak"][:5]:
            L.append(f"- baris {r['baris']}: {r['alasan']}")
    if h["peringatan"]:
        L += [""] + [f"Catatan: {p}" for p in h["peringatan"][:5]]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(L)).rstrip()


# ---------------------------------------------------------------- timesheet
def rentang_periode(periode, acuan):
    senin = acuan - timedelta(days=acuan.weekday())
    if periode == "minggu-ini":
        return senin, senin + timedelta(days=6)
    if periode == "minggu-lalu":
        return senin - timedelta(days=7), senin - timedelta(days=1)
    awal_bln = acuan.replace(day=1)
    if periode == "bulan-ini":
        berikut = (awal_bln + timedelta(days=32)).replace(day=1)
        return awal_bln, berikut - timedelta(days=1)
    if periode == "bulan-lalu":
        akhir = awal_bln - timedelta(days=1)
        return akhir.replace(day=1), akhir
    if periode == "semua":
        return date(1900, 1, 1), date(2999, 12, 31)
    raise InputSalah(f"periode '{periode}' tidak dikenal (minggu-ini, minggu-lalu, bulan-ini, bulan-lalu, semua)")


def rekap_timesheet(path, acuan, dari, sampai, periode, klien, tarif_default):
    header, isi, info = baca_csv(path, ["tanggal", "klien", "jam"])
    if header is None:
        raise InputSalah(f"file timesheet {path} belum ada. Catat jam dulu dengan 'catat-jam' atau buat CSV "
                         f"berkolom {','.join(KOLOM_TS)}")
    if dari or sampai:
        awal = parse_tanggal(dari, acuan, "terdekat")[0] if dari else date(1900, 1, 1)
        akhir = parse_tanggal(sampai, acuan, "terdekat")[0] if sampai else acuan
    else:
        awal, akhir = rentang_periode(periode or "bulan-ini", acuan)
    if awal > akhir:
        raise InputSalah("tanggal --dari lebih besar dari --sampai")
    tarif_def = parse_nominal(tarif_default)[0] if tarif_default else None
    rusak, catatan, per_klien = [], list(info), {}
    for no, b, alasan, _sel in isi:
        if b is None:
            rusak.append({"baris": no, "alasan": alasan})
            continue
        try:
            tgl, cat = parse_tanggal(b.get("tanggal"), acuan, "lalu")
            if cat:
                catatan.append(f"baris {no}: {cat}")
            if tgl > acuan:
                catatan.append(f"baris {no}: tanggal kerja {tgl_id(tgl, True)} ada di masa depan; cek lagi.")
            nama = (b.get("klien") or "").strip().lstrip("'")
            if not nama:
                raise InputSalah("kolom klien kosong")
            menit, cat = parse_jam(b.get("jam"))
            if cat:
                catatan.append(f"baris {no}: {cat}")
            tarif = parse_nominal(b.get("tarif_per_jam"))[0] if (b.get("tarif_per_jam") or "").strip() else tarif_def
        except InputSalah as e:
            rusak.append({"baris": no, "alasan": str(e)})
            continue
        if not (awal <= tgl <= akhir):
            continue
        if klien and nama.lower() != klien.strip().lower():
            continue
        k = per_klien.setdefault(nama.lower(), {"klien": nama, "menit": 0, "nilai_pecahan": Fraction(0),
                                                "tanpa_tarif_menit": 0, "per_tarif": {}, "rincian": []})
        k["menit"] += menit
        if tarif is None:
            k["tanpa_tarif_menit"] += menit
        else:
            k["nilai_pecahan"] += Fraction(menit * tarif, 60)
            k["per_tarif"][tarif] = k["per_tarif"].get(tarif, 0) + menit
        k["rincian"].append({"tanggal": tgl.isoformat(), "tanggal_teks": tgl_id(tgl, True), "menit": menit,
                             "durasi": teks_durasi(menit), "keterangan": (b.get("keterangan") or "").strip().lstrip("'"),
                             "tarif_per_jam": tarif})
    daftar = []
    for k in sorted(per_klien.values(), key=lambda x: x["klien"].lower()):
        k["rincian"].sort(key=lambda r: r["tanggal"])
        ada_tarif = bool(k["per_tarif"])
        nilai = bulat(k.pop("nilai_pecahan")) if ada_tarif else None
        daftar.append({"klien": k["klien"], "total_menit": k["menit"], "total_durasi": teks_durasi(k["menit"]),
                       "total_jam_desimal": jam_desimal(k["menit"]), "nilai": nilai,
                       "nilai_teks": rupiah(nilai) if nilai is not None else "tarif belum diisi",
                       "per_tarif": [{"tarif_per_jam": t, "tarif_teks": rupiah(t), "menit": m,
                                      "jam_desimal": jam_desimal(m)} for t, m in sorted(k["per_tarif"].items())],
                       "menit_tanpa_tarif": k["tanpa_tarif_menit"], "rincian": k["rincian"]})
    total_nilai = sum(d["nilai"] for d in daftar if d["nilai"] is not None)
    hasil = {"ok": True, "periode": {"dari": awal.isoformat(), "sampai": akhir.isoformat(),
                                     "teks": f"{tgl_id(awal, True)} - {tgl_id(akhir, True)}" if awal.year > 1900 else "semua"},
             "per_klien": daftar, "total_menit": sum(d["total_menit"] for d in daftar),
             "total_nilai": total_nilai, "total_nilai_teks": rupiah(total_nilai),
             "baris_ditolak": rusak, "catatan": catatan,
             "aturan_pembulatan": "Nilai per klien = jumlah (menit x tarif / 60) dihitung persis, dibulatkan sekali "
                                  "ke rupiah terdekat (0,5 ke atas). Total = jumlah nilai per klien."}
    if any(d["menit_tanpa_tarif"] for d in daftar):
        hasil["catatan"].append("Ada jam tanpa tarif (isi kolom tarif_per_jam atau pakai --tarif); nilainya tidak dihitung.")
    hasil["teks"] = teks_timesheet(hasil, bool(klien))
    return hasil


def teks_timesheet(h, satu_klien):
    L = [f"REKAP TIMESHEET {h['periode']['teks']}", ""]
    if not h["per_klien"]:
        L.append("Tidak ada catatan jam pada periode ini.")
    for d in h["per_klien"]:
        tarif = " + ".join(f"{teks_durasi(p['menit'])} x {p['tarif_teks']}/jam" for p in d["per_tarif"])
        L.append(f"- {d['klien']}: {d['total_durasi']} ({'=' if d['total_menit'] * 100 % 60 == 0 else '≈'} {d['total_jam_desimal']} jam)"
                 + (f" | {tarif} = {d['nilai_teks']}" if d["nilai"] is not None else " | tarif belum diisi"))
        if d["menit_tanpa_tarif"] and d["nilai"] is not None:
            L.append(f"  ({teks_durasi(d['menit_tanpa_tarif'])} belum ada tarifnya, tidak ikut dihitung)")
    if len(h["per_klien"]) > 1:
        L += ["", f"Total semua klien: {teks_durasi(h['total_menit'])} | {h['total_nilai_teks']}"]
    if satu_klien and h["per_klien"]:
        d = h["per_klien"][0]
        nilai = f", nilai {d['nilai_teks']}" if d["nilai"] is not None else ""
        L += ["", "DRAF PESAN KE KLIEN (cek dulu, lalu kirim sendiri):",
              f"Selamat sore {sapaan(d['klien'])}, berikut rekap jam kerja periode {h['periode']['teks']}: "
              f"total {d['total_durasi']} ({d['total_jam_desimal']} jam){nilai}. Rincian:"]
        for r in d["rincian"]:
            L.append(f"- {r['tanggal_teks']}: {r['durasi']}" + (f" - {r['keterangan']}" if r["keterangan"] else ""))
        L.append("Mohon konfirmasinya sebelum kami terbitkan invoice. Terima kasih.")
    if h["baris_ditolak"]:
        L += ["", f"PERHATIAN: {len(h['baris_ditolak'])} baris timesheet tidak terbaca dan tidak ikut dihitung:"]
        L += [f"- baris {r['baris']}: {r['alasan']}" for r in h["baris_ditolak"][:5]]
    if h["catatan"]:
        L += [""] + [f"Catatan: {c}" for c in h["catatan"][:5]]
    if h["per_klien"]:
        L += ["", "Nilai dihitung per menit (menit x tarif / 60), dibulatkan ke rupiah terdekat per klien."]
    return "\n".join(L).rstrip()


# ---------------------------------------------------------------- perintah
def keluaran(a, data):
    if getattr(a, "teks", False) and "teks" in data:
        print(data["teks"])
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def publik(it):
    return {k: v for k, v in it.items() if not k.startswith("_")}


def cmd_tambah(a, acuan):
    header, baris, rusak, info = muat_daftar(a.file)
    jenis = normal_jenis(a.jenis)
    nama = (a.nama or "").strip()
    if not nama:
        raise InputSalah("--nama wajib (cukup nama panggilan/kode, mis. \"Bu Rina\" atau \"PLG-07\")")
    if len(nama) > 60:
        raise InputSalah("--nama terlalu panjang; cukup nama panggilan/kode (maks 60 karakter)")
    if not a.simpan_kontak:
        temu = cek_kontak({"nama": nama, "perihal": a.perihal or "", "catatan": a.catatan or ""})
        if temu:
            raise DataPribadi(f"kolom {temu[0]} berisi {temu[1]}. Daftar ini cukup menyimpan nama panggilan/kode; "
                              "kontak sudah ada di HP Anda. Hapus data itu, atau tambahkan --simpan-kontak bila "
                              "pemilik memang sengaja menyimpannya")
    tgl, cat_tgl = parse_tanggal(a.tanggal, acuan, arah="depan") if a.tanggal else (acuan, "Tanggal tidak disebut; dipakai hari ini.")
    nominal, cat_nom = parse_nominal(a.nominal)
    if jenis == "piutang" and nominal is None:
        cat_nom = "Nominal piutang belum diisi; draf pesan akan tanpa angka."
    item = {"id": id_baru(baris), "jenis": jenis, "nama": aman_csv(nama), "tanggal": tgl.isoformat(),
            "nominal": str(nominal) if nominal is not None else "", "perihal": aman_csv(a.perihal),
            "status": "aktif", "catatan": aman_csv(a.catatan), "dibuat": acuan.isoformat(), "diingatkan": ""}
    baris.append(item)
    simpan_daftar(a.file, header, baris)
    catatan = [c for c in (cat_tgl, cat_nom) if c]
    if tgl < acuan and not (cat_tgl and "TERLAMBAT" in cat_tgl):
        catatan.append("Tanggal sudah lewat; item langsung masuk kelompok TERLAMBAT.")
    teks = (f"Tersimpan #{item['id']}: {jenis} - {nama}, {tgl_id(tgl)}"
            + (f", {rupiah(nominal)}" if nominal is not None else "")
            + (f" ({a.perihal})" if a.perihal else "") + "."
            + "".join(f"\nCatatan: {c}" for c in catatan) + teks_rusak(rusak, info))
    keluaran(a, {"ok": True, "aksi": "tambah", "item": {**item, "tanggal_teks": tgl_id(tgl)},
                 "catatan": catatan, "baris_ditolak": rusak, "teks": teks})


def cmd_ubah_status(a, acuan, aksi):
    header, baris, rusak, info = muat_daftar(a.file)
    target = cari_id(baris, a.id)
    ringkas = []
    if aksi == "hapus":
        ids = {id(t) for t in target}
        baris = [b for b in baris if id(b) not in ids]
        ringkas = [f"#{t['id']} {t.get('nama', '')} dihapus permanen" for t in target]
    elif aksi == "selesai":
        for t in target:
            t["status"] = "selesai"
            if a.catatan:
                t["catatan"] = aman_csv(((t.get("catatan") or "") + " | " + a.catatan).strip(" |"))
            ringkas.append(f"#{t['id']} {t.get('nama', '')} ditandai selesai")
    elif aksi == "tunda":
        if not a.ke:
            raise InputSalah("--ke wajib, mis. --ke \"Senin\" atau --ke \"10/10\"")
        baru, cat = parse_tanggal(a.ke, acuan, arah="depan")
        for t in target:
            lama = t.get("tanggal", "")
            t["tanggal"] = baru.isoformat()
            t["status"] = "aktif"
            t["catatan"] = aman_csv(((t.get("catatan") or "") + f" | ditunda dari {lama}").strip(" |"))
            ringkas.append(f"#{t['id']} {t.get('nama', '')} ditunda ke {tgl_id(baru)}" + (f" ({cat})" if cat else ""))
    elif aksi == "terkirim":
        baru, cat = parse_tanggal(a.berikutnya, acuan, arah="depan") if a.berikutnya else (None, None)
        for t in target:
            n = parse_diingatkan(t.get("diingatkan")) + 1
            t["diingatkan"] = str(n)
            teks = f"#{t['id']} {t.get('nama', '')}: tercatat sudah diingatkan {n}x"
            if baru:
                t["tanggal"] = baru.isoformat()
                t["status"] = "aktif"
                teks += f"; follow-up berikutnya {tgl_id(baru)}" + (f" ({cat})" if cat else "")
            ringkas.append(teks)
    simpan_daftar(a.file, header, baris)
    keluaran(a, {"ok": True, "aksi": aksi, "hasil": ringkas, "baris_ditolak": rusak,
                 "teks": "\n".join(ringkas) + teks_rusak(rusak, info)})


def cmd_ubah(a, acuan):
    header, baris, rusak, info = muat_daftar(a.file)
    target = cari_id(baris, a.id)
    if len(target) != 1:
        raise InputSalah("'ubah' hanya untuk satu item sekaligus")
    t = target[0]
    berubah = []
    if not a.simpan_kontak:
        temu = cek_kontak({"nama": a.nama or "", "perihal": a.perihal or "", "catatan": a.catatan or ""})
        if temu:
            raise DataPribadi(f"kolom {temu[0]} berisi {temu[1]}; tidak disimpan (pakai --simpan-kontak bila sengaja)")
    if a.tanggal:
        d, cat = parse_tanggal(a.tanggal, acuan, arah="depan")
        t["tanggal"] = d.isoformat()
        berubah.append(f"tanggal {tgl_id(d)}" + (f" ({cat})" if cat else ""))
    if a.nominal is not None:
        n, _ = parse_nominal(a.nominal)
        t["nominal"] = str(n) if n is not None else ""
        berubah.append(f"nominal {rupiah(n) if n is not None else '(kosong)'}")
    for kolom in ("nama", "perihal"):
        v = getattr(a, kolom)
        if v is not None:
            t[kolom] = aman_csv(v)
            berubah.append(f"{kolom} \"{v}\"")
    if a.catatan is not None:  # catatan DITAMBAHKAN, bukan mengganti yang lama
        t["catatan"] = aman_csv(((t.get("catatan") or "") + " | " + a.catatan).strip(" |"))
        berubah.append(f"catatan ditambah \"{a.catatan}\"")
    if a.jenis:
        t["jenis"] = normal_jenis(a.jenis)
        berubah.append(f"jenis {t['jenis']}")
    if a.status:
        t["status"] = normal_status(a.status)
        berubah.append(f"status {t['status']}")
    if not berubah:
        raise InputSalah("tidak ada yang diubah; sebutkan mis. --tanggal, --nominal, --perihal")
    simpan_daftar(a.file, header, baris)
    teks = f"#{t['id']} diubah: " + "; ".join(berubah) + teks_rusak(rusak, info)
    keluaran(a, {"ok": True, "aksi": "ubah", "id": t["id"], "perubahan": berubah, "teks": teks})


def cmd_bersihkan(a, acuan):
    header, baris, rusak, info = muat_daftar(a.file)
    batas = acuan - timedelta(days=a.lebih_dari)
    sisa, dibuang = [], []
    for b in baris:
        try:
            if "_mentah" in b:
                raise InputSalah("baris rusak")
            d = parse_tanggal(b.get("tanggal"), acuan, "terdekat")[0]
            status = normal_status(b.get("status"))
        except InputSalah:
            sisa.append(b)
            continue
        if status == "selesai" and d < batas:
            dibuang.append(b.get("id", ""))
        else:
            sisa.append(b)
    simpan_daftar(a.file, header, sisa)
    teks = f"{len(dibuang)} item selesai yang tanggalnya sebelum {tgl_id(batas, True)} dihapus." + teks_rusak(rusak, info)
    keluaran(a, {"ok": True, "aksi": "bersihkan", "dihapus_id": dibuang, "teks": teks})


def cmd_daftar(a, acuan):
    header, baris, rusak, info = muat_daftar(a.file)
    items = []
    for b in item_sah(baris):
        try:
            it = tafsir_item(b, acuan)
        except InputSalah as e:
            rusak.append({"baris": b["_no"], "alasan": str(e)})
            continue
        if a.semua or it["status"] == "aktif":
            items.append(it)
    items.sort(key=lambda x: (x["status"] != "aktif", x["_tgl"]))
    L = [f"DAFTAR PANTAUAN ({len(items)} item{'' if a.semua else ' aktif'})"]
    for it in items:
        L.append(f"#{it['id']} {it['tanggal_teks']} | {it['jenis']} | {it['nama']}"
                 + (f" | {it['nominal_teks']}" if it["nominal_teks"] else "")
                 + (f" | {it['perihal']}" if it["perihal"] else "")
                 + (" | SELESAI" if it["status"] == "selesai" else ""))
    rusak.sort(key=lambda r: r["baris"])
    teks = "\n".join(L) + teks_rusak(rusak, info)
    keluaran(a, {"ok": True, "items": [publik(i) for i in items], "baris_ditolak": rusak, "teks": teks})


def cmd_draf(a, acuan):
    header, baris, rusak, info = muat_daftar(a.file)
    t = cari_id(baris, a.id)[0]
    it = tafsir_item(t, acuan)
    pesan = draf_pesan(it, acuan)
    saran = saran_item(it)
    teks = (f"#{it['id']} untuk {it['nama']}:\n{pesan}" if pesan else
            f"#{it['id']} adalah pengingat pribadi ({it['jenis']}); tidak ada draf pesan ke orang lain.")
    if saran:
        teks += f"\n(Saran: {saran})"
    keluaran(a, {"ok": True, "item": publik(it), "draf": pesan, "saran": saran, "teks": teks})


def cmd_catat_jam(a, acuan):
    klien = (a.klien or "").strip()
    if not klien:
        raise InputSalah("--klien wajib")
    menit, cat = parse_jam(a.jam)
    tgl, cat_t = parse_tanggal(a.tanggal, acuan, "lalu") if a.tanggal else (acuan, None)
    if tgl > acuan:
        raise InputSalah(f"tanggal kerja {tgl_id(tgl)} ada di masa depan. Jam kerja hanya dicatat untuk hari ini "
                         "atau hari yang sudah lewat (mis. 'Senin', 'kemarin', '28/9')")
    tarif = parse_nominal(a.tarif)[0] if a.tarif else None
    header, isi, info = baca_csv(a.timesheet_file, ["tanggal", "klien", "jam"])
    if header is None:
        header = list(KOLOM_TS)
    for k in KOLOM_TS:
        if k not in header:
            header.append(k)
    lama = []
    for no, b, alasan, _sel in isi:
        if b is None:
            raise InputSalah(f"file timesheet baris {no} rusak ({alasan}); perbaiki dulu sebelum menambah baris")
        lama.append(b)
    baru = {"tanggal": tgl.isoformat(), "klien": aman_csv(klien), "jam": f"{menit // 60}:{menit % 60:02d}",
            "tarif_per_jam": str(tarif) if tarif else "", "keterangan": aman_csv(a.keterangan)}
    tulis_csv_atomik(a.timesheet_file, header, lama + [baru])
    catatan = [c for c in (cat, cat_t) if c] + list(info)
    teks = (f"Tercatat: {klien}, {tgl_id(tgl)}, {teks_durasi(menit)}" + (f", tarif {rupiah(tarif)}/jam" if tarif else "")
            + "." + "".join(f"\nCatatan: {c}" for c in catatan))
    keluaran(a, {"ok": True, "aksi": "catat-jam", "baris": baru, "catatan": catatan, "teks": teks})


def main(argv=None):
    ap = argparse.ArgumentParser(description="Daftar pantauan follow-up, rekap harian, dan rekap timesheet.")
    ap.add_argument("--file", default=os.path.join("pengingat", "DAFTAR.csv"), help="CSV daftar pantauan")
    ap.add_argument("--timesheet-file", default=os.path.join("pengingat", "timesheet.csv"))
    ap.add_argument("--hari-ini", help="Tanggal acuan (untuk uji), mis. 2026-10-01")
    ap.add_argument("--tz", default="Asia/Jakarta", help="Zona waktu (default Asia/Jakarta)")
    ap.add_argument("--teks", action="store_true", help="Cetak teks siap kirim saja (bukan JSON)")
    sub = ap.add_subparsers(dest="perintah")
    p = sub.add_parser("tambah")
    p.add_argument("--jenis", required=True)
    p.add_argument("--nama", required=True)
    p.add_argument("--tanggal")
    p.add_argument("--nominal")
    p.add_argument("--perihal", default="")
    p.add_argument("--catatan", default="")
    p.add_argument("--simpan-kontak", action="store_true")
    for nama in ("selesai", "hapus", "tunda", "terkirim"):
        p = sub.add_parser(nama)
        p.add_argument("--id", required=True)
        p.add_argument("--catatan", default="")
        if nama == "tunda":
            p.add_argument("--ke")
        if nama == "terkirim":
            p.add_argument("--berikutnya", help="Tanggal follow-up berikutnya, mis. '3 hari lagi'")
    p = sub.add_parser("ubah")
    p.add_argument("--id", required=True)
    for k in ("tanggal", "nominal", "nama", "perihal", "catatan", "jenis", "status"):
        p.add_argument(f"--{k}")
    p.add_argument("--simpan-kontak", action="store_true")
    p = sub.add_parser("bersihkan")
    p.add_argument("--lebih-dari", type=int, default=30)
    p = sub.add_parser("daftar")
    p.add_argument("--semua", action="store_true")
    p = sub.add_parser("rekap")
    p.add_argument("--maks-draf", type=int, default=10)
    p = sub.add_parser("draf")
    p.add_argument("--id", required=True)
    p = sub.add_parser("catat-jam")
    p.add_argument("--klien", required=True)
    p.add_argument("--jam", required=True)
    p.add_argument("--tanggal")
    p.add_argument("--tarif")
    p.add_argument("--keterangan", default="")
    p = sub.add_parser("timesheet")
    p.add_argument("--periode")
    p.add_argument("--dari")
    p.add_argument("--sampai")
    p.add_argument("--klien")
    p.add_argument("--tarif", help="Tarif per jam untuk baris yang kolom tarifnya kosong")
    # izinkan --teks/--hari-ini/--file ditulis setelah subperintah juga
    for sp in sub.choices.values():
        sp.add_argument("--teks", action="store_true", default=argparse.SUPPRESS)
        sp.add_argument("--hari-ini", default=argparse.SUPPRESS)
        sp.add_argument("--file", default=argparse.SUPPRESS)
        sp.add_argument("--timesheet-file", default=argparse.SUPPRESS)
        sp.add_argument("--tz", default=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if not a.perintah:
        ap.print_help()
        return 1
    try:
        dasar = hari_ini_di(a.tz)
        acuan = parse_tanggal(a.hari_ini, dasar, "terdekat")[0] if a.hari_ini else dasar
        if a.perintah == "tambah":
            cmd_tambah(a, acuan)
        elif a.perintah in ("selesai", "hapus", "tunda", "terkirim"):
            cmd_ubah_status(a, acuan, a.perintah)
        elif a.perintah == "ubah":
            cmd_ubah(a, acuan)
        elif a.perintah == "bersihkan":
            cmd_bersihkan(a, acuan)
        elif a.perintah == "daftar":
            cmd_daftar(a, acuan)
        elif a.perintah == "rekap":
            if a.maks_draf < 0:
                raise InputSalah("--maks-draf tidak boleh negatif")
            keluaran(a, susun_rekap(a.file, acuan, a.maks_draf))
        elif a.perintah == "draf":
            cmd_draf(a, acuan)
        elif a.perintah == "catat-jam":
            cmd_catat_jam(a, acuan)
        elif a.perintah == "timesheet":
            keluaran(a, rekap_timesheet(a.timesheet_file, acuan, a.dari, a.sampai, a.periode, a.klien, a.tarif))
        return 0
    except DataPribadi as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except InputSalah as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print(f"ERROR: file tidak bisa dibaca/ditulis: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
