#!/usr/bin/env python3
"""Hitung PPh Final UMKM 0,5% per bulan + pelacak omzet kumulatif setahun.

Dasar (dicocokkan dengan naskah/terbitan resmi pada 2026-10-14):
- PP 55/2022 sebagaimana diubah PP 20/2026 (ditetapkan & diundangkan 22 April 2026).
  * Orang pribadi (OP): omzet s.d. Rp500.000.000 setahun TIDAK dikenai pajak; 0,5% hanya atas bagian omzet
    kumulatif di atas Rp500 juta (bulan saat melewati dihitung proporsional).
  * Badan (PT perorangan, koperasi, dan CV/firma/PT yang masih dalam masa peralihan): 0,5% x seluruh omzet.
  * Pasal 59 PP 55/2022 (batas 7 tahun OP, 4 tahun PT perorangan) DIHAPUS oleh PP 20/2026 Pasal I angka 6.
    Koperasi tetap 4 tahun (Pasal 57 ayat (2) huruf f) dengan peralihan s.d. 2029 (Pasal II angka 1 huruf b);
    CV/firma/PT selain perorangan hanya meneruskan sisa jangka waktu lama (Pasal II angka 1 huruf e).
- PMK 37/2025 + FAQ DJP versi 1 Juli 2026 (no. 14-15): PPh 22 yang dipungut marketplace atas pedagang yang
  memenuhi kriteria PP 20/2026 = bagian pelunasan PPh final. Dihitung per bulan: selisih kurang disetor
  sendiri; selisih lebih dapat diajukan permohonan pengembalian.
- PMK 81/2024 Pasal 94 & 100: setor paling lambat tanggal 15 bulan berikutnya; bila libur -> hari kerja berikutnya.

Pembulatan: PPh final per bulan dibulatkan ke bawah ke rupiah penuh. Selisih PPh final - PPh 22 juga dibulatkan
ke bawah (tidak pernah menyetor atau meminta kembali melebihi selisih sebenarnya).

Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 pph_final.py --jenis op --tahun 2026 --omzet 45jt 60jt 80jt 120jt 150jt 90jt
  python3 pph_final.py --jenis op --tahun 2026 --bulan-awal 8 --omzet 73jt 66jt --omzet-sebelumnya 448,5jt --pph22 180rb 165rb
  python3 pph_final.py --tahun 2026 --bulan-awal 7 --omzet-sebelumnya 410jt --omzet 95jt 88jt 102jt 100jt 100jt 100jt --proyeksi-mulai 10
  python3 pph_final.py --kemungkinan --tahun 2026 --bulan-awal 10 --omzet 85jt
  python3 pph_final.py --jenis badan --file omzet.csv --format json
  python3 pph_final.py --tampilan tabel --tahun 2026 --omzet 45jt 60jt     (tabel lebar untuk terminal/file)

Tampilan (v1.0.6): bawaan `--tampilan chat` = blok siap salin untuk Telegram/WhatsApp, TANPA tabel dan tanpa blok
kode (satu baris pendek per bulan: bulan · omzet · PPh; kena pajak, PPh 22, batas setor & status di baris keterangan;
catatan dipersingkat), maks. 3.800 karakter; data sangat panjang -> makin ringkas, atau dibagi dua pesan dengan baris
`<<< PESAN BERIKUTNYA >>>` (tiap bagian maks. 3.800). `--tampilan tabel` = tabel Markdown lebar (terminal/IDE/file).
Angka keduanya sama.
"""
import argparse
import calendar
import csv
import datetime
import json
import os
import re
import sys
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

VERSI = "1.0.6"
TANGGAL_ATURAN = "2026-10-14"
DASAR_ATURAN = ("PP 55/2022 jo. PP 20/2026 (PPh final UMKM 0,5%); PMK 37/2025 dan FAQ DJP versi 1 Juli 2026 "
                "(PPh 22 marketplace); PMK 81/2024 (batas setor)")
DASAR_ATURAN_CHAT = "PP 55/2022 jo. PP 20/2026; PMK 37/2025 & FAQ DJP 1 Juli 2026 (PPh 22 marketplace); PMK 81/2024"
TARIF = Decimal("0.005")
BATAS_BEBAS_OP = Decimal(500000000)
BATAS_OMZET_UMKM = Decimal(4800000000)
TAHUN_PP20 = 2026  # PP 20/2026 berlaku 22 April 2026

NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
# PP 55/2022 Pasal 59 (lama): jangka waktu tarif 0,5%. Untuk OP & PT perorangan sudah DIHAPUS oleh PP 20/2026;
# angka di bawah hanya dipakai untuk masa peralihan koperasi, CV, firma, dan PT selain perorangan.
JANGKA_WAKTU_LAMA = {"op": 7, "pt-perorangan": 4, "koperasi": 4, "cv": 4, "firma": 4, "pt": 3}
NAMA_BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
              "September", "Oktober", "November", "Desember"]
NAMA_BULAN_PENDEK = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
ALIAS_BULAN = {
    "jan": 1, "feb": 2, "peb": 2, "mar": 3, "apr": 4, "mei": 5, "may": 5, "jun": 6, "jul": 7,
    "agu": 8, "agt": 8, "ags": 8, "aug": 8, "sep": 9, "okt": 10, "oct": 10, "nov": 11, "nop": 11,
    "des": 12, "dec": 12,
}
LABEL_BADAN = {"pt-perorangan": "PT perorangan", "koperasi": "Koperasi", "cv": "CV", "firma": "Firma",
               "pt": "PT", "lainnya": "lainnya"}


# ---------------------------------------------------------------- angka & format
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3), ("m", 10 ** 9)]


def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise ValueError("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                         "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))


def parse_angka(nilai, nama="angka"):
    """Baca angka format Indonesia: 'Rp 15.000', '15.000,50', '1,5 jt', '4,8 M', '15000'."""
    if isinstance(nilai, bool) or nilai is None:
        raise ValueError("{}: nilai kosong atau tidak valid".format(nama))
    if isinstance(nilai, Decimal):
        return nilai
    if isinstance(nilai, int):
        return Decimal(nilai)
    if isinstance(nilai, float):
        return Decimal(str(nilai))
    asli = str(nilai)
    s = asli.strip().lower().replace("\u00a0", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    if s.endswith("%"):
        s = s[:-1]
    pengali = 1
    for akhiran, kali in _PENGALI:
        if s.endswith(akhiran):
            s, pengali = s[: -len(akhiran)], kali
            break
    negatif = s.startswith("-")
    if negatif:
        s = s[1:]
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    if "," in s and "." in s:
        if s.rfind(",") < s.rfind("."):
            raise ValueError("{}: '{}' memakai format Inggris. Tulis dengan titik untuk ribuan dan koma "
                             "untuk desimal, mis. 1.250.000,50".format(nama, asli))
        utuh, _, desimal = s.rpartition(",")
        _cek_ribuan(utuh.split("."), asli, nama)
        s = utuh.replace(".", "") + "." + desimal
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2:
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(".", "")
    try:
        d = Decimal(s) * pengali
    except InvalidOperation:
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    return -d if negatif else d


def format_rp(d, desimal=False):
    """Format Rupiah standar library: "Rp1.250.000" (tanpa spasi); desimal hanya bila ada pecahan."""
    d = Decimal(d).quantize(Decimal("0.01") if desimal else Decimal(1), ROUND_HALF_UP)
    neg = d < 0
    d = abs(d)
    teks = "{:,}".format(int(d)).replace(",", ".")
    if desimal:
        pecahan = "{:.2f}".format(d).split(".")[1]
        if pecahan != "00":
            teks += "," + pecahan
    return ("-" if neg else "") + "Rp" + teks


def ke_json(d):
    if isinstance(d, Decimal):
        return int(d) if d == d.to_integral_value() else float(d.quantize(Decimal("0.01"), ROUND_HALF_UP))
    raise TypeError(str(type(d)))


# ---------------------------------------------------------------- input
def parse_bulan(teks):
    s = str(teks).strip().lower()
    if re.fullmatch(r"\d{1,2}", s):
        b = int(s)
    else:
        m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})", s) or re.fullmatch(r"(\d{1,2})[-/.](\d{4})", s)
        if m:
            a, c = m.groups()
            b = int(c) if len(a) == 4 else int(a)
        else:
            b = ALIAS_BULAN.get(s[:3])
            if b is None:
                raise ValueError("bulan '{}' tidak dikenali (pakai 1-12 atau nama bulan, mis. 'Januari')"
                                 .format(teks))
    if not 1 <= b <= 12:
        raise ValueError("bulan '{}' di luar 1-12".format(teks))
    return b


def cari_kolom(header, kata):
    for i, h in enumerate(header):
        h2 = re.sub(r"[^a-z0-9]", "", h.lower())
        if any(k in h2 for k in kata):
            return i
    return None


def baca_file(path):
    """CSV (bulan;omzet;pph22) atau JSON [{bulan, omzet, pph22}] -> list (bulan, omzet, pph22)."""
    try:
        with open(path, encoding="utf-8-sig", newline="") as f:
            isi = f.read()
    except OSError as e:
        raise ValueError("file '{}' tidak bisa dibaca: {}".format(path, e.strerror or e))
    if not isi.strip():
        raise ValueError("file '{}' kosong".format(path))
    data = []
    if path.lower().endswith(".json"):
        try:
            obj = json.loads(isi)
        except json.JSONDecodeError as e:
            raise ValueError("JSON tidak valid (baris {}): {}".format(e.lineno, e.msg))
        if isinstance(obj, dict):
            obj = obj.get("bulan") or obj.get("data") or []
        if not isinstance(obj, list):
            raise ValueError("JSON harus berupa daftar: [{\"bulan\": 1, \"omzet\": 45000000}, ...]")
        for i, r in enumerate(obj, 1):
            if not isinstance(r, dict) or "bulan" not in r or "omzet" not in r:
                raise ValueError("data ke-{} wajib punya 'bulan' dan 'omzet'".format(i))
            data.append((parse_bulan(r["bulan"]), parse_angka(r["omzet"], "omzet data ke-{}".format(i)),
                         parse_angka(r.get("pph22", 0) or 0, "pph22 data ke-{}".format(i))))
        return data
    try:
        dialek = csv.Sniffer().sniff(isi[:2048], delimiters=";,\t|")
    except csv.Error:
        dialek = csv.excel
    baris = [r for r in csv.reader(isi.splitlines(), dialek) if any(c.strip() for c in r)]
    header = baris[0]
    ib = cari_kolom(header, ["bulan", "month", "periode", "masa"])
    io = cari_kolom(header, ["omzet", "omset", "peredaran", "penjualan", "bruto", "revenue", "sales"])
    ip = cari_kolom(header, ["pph22", "pph", "marketplace", "dipungut"])
    if ib is None or io is None:
        raise ValueError("CSV wajib punya kolom 'bulan' dan 'omzet' di baris pertama (header). "
                         "Contoh: bulan;omzet;pph22")
    for no, r in enumerate(baris[1:], 2):
        if len(r) <= max(ib, io):
            raise ValueError("baris {} CSV tidak lengkap: {}".format(no, r))
        pph = r[ip] if ip is not None and ip < len(r) and r[ip].strip() else "0"
        data.append((parse_bulan(r[ib]), parse_angka(r[io], "omzet baris {}".format(no)),
                     parse_angka(pph, "pph22 baris {}".format(no))))
    return data


# ---------------------------------------------------------------- tanggal
def batas_setor(tahun, bulan):
    """Tanggal 15 bulan berikutnya (PMK 81/2024 Pasal 94)."""
    if bulan == 12:
        return datetime.date(tahun + 1, 1, 15)
    return datetime.date(tahun, bulan + 1, 15)


_LIBUR_CACHE = {}


def libur_nasional(tahun):
    """Libur nasional + cuti bersama dari references/libur-nasional-<tahun>.csv (SKB 3 menteri).
    Mengembalikan dict tanggal -> keterangan, atau None bila data tahun itu belum ada."""
    if tahun not in _LIBUR_CACHE:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references",
                            "libur-nasional-{}.csv".format(tahun))
        data = None
        if os.path.isfile(path):
            data = {}
            with open(path, encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f):
                    try:
                        data[datetime.date.fromisoformat(r["tanggal"].strip())] = (r.get("keterangan") or "").strip()
                    except (KeyError, ValueError, AttributeError):
                        continue
        _LIBUR_CACHE[tahun] = data
    return _LIBUR_CACHE[tahun]


def geser_hari_kerja(tgl):
    """Batas setor jatuh hari libur -> hari kerja berikutnya (PMK 81/2024 Ps. 100 ayat 1).
    Hari libur = Sabtu, Minggu, libur nasional, cuti bersama. Kembalikan (tanggal, alasan[], data_libur_lengkap)."""
    alasan = []
    lengkap = True
    while True:
        libur = libur_nasional(tgl.year)
        if libur is None:
            lengkap = False
        if tgl.weekday() >= 5:
            alasan.append("{} {}".format(NAMA_HARI[tgl.weekday()], format_tgl_pendek(tgl)))
        elif libur and tgl in libur:
            alasan.append("{} ({})".format(format_tgl_pendek(tgl), libur[tgl]))
        else:
            return tgl, alasan, lengkap
        tgl += datetime.timedelta(days=1)


def format_tgl_pendek(tgl):
    return "{} {}".format(tgl.day, NAMA_BULAN[tgl.month - 1])


def format_tgl(tgl):
    """'Rabu 14 Oktober 2026'."""
    return "{} {} {} {}".format(NAMA_HARI[tgl.weekday()], tgl.day, NAMA_BULAN[tgl.month - 1], tgl.year)


def format_tgl_tabel(tgl):
    """'Rabu 18 Feb 2026' (untuk kolom tabel)."""
    return "{} {} {} {}".format(NAMA_HARI[tgl.weekday()], tgl.day, NAMA_BULAN_PENDEK[tgl.month - 1], tgl.year)


def status_relatif(tgl, hari_ini):
    """'sudah lewat' / 'hari ini' / 'besok' / '' terhadap tanggal acuan."""
    if hari_ini is None:
        return ""
    selisih = (tgl - hari_ini).days
    if selisih < 0:
        return "sudah lewat"
    if selisih == 0:
        return "hari ini"
    if selisih == 1:
        return "besok"
    return ""


def keterangan_jarak(tgl, hari_ini):
    """'hari ini' / 'besok' / '12 hari lagi' / 'sudah lewat 29 hari'."""
    selisih = (tgl - hari_ini).days
    if selisih == 0:
        return "hari ini"
    if selisih == 1:
        return "besok"
    if selisih > 1:
        return "{} hari lagi".format(selisih)
    return "sudah lewat {} hari".format(-selisih)


def akhir_bulan(tahun, bulan):
    return datetime.date(tahun, bulan, calendar.monthrange(tahun, bulan)[1])


def rentang_bulan(rows):
    if not rows:
        return "-"
    a, b = rows[0]["nama_bulan"], rows[-1]["nama_bulan"]
    return a if a == b else "{}–{}".format(a, b)


def daftar_bulan_ringkas(nomor):
    """[1,2,3,5] -> 'Januari–Maret, Mei' (bulan berurutan diringkas jadi rentang)."""
    bagian, awal = [], None
    for i, b in enumerate(nomor):
        if awal is None:
            awal = b
        if i + 1 == len(nomor) or nomor[i + 1] != b + 1:
            bagian.append(NAMA_BULAN[awal - 1] if awal == b else "{}–{}".format(NAMA_BULAN[awal - 1], NAMA_BULAN[b - 1]))
            awal = None
    return ", ".join(bagian)


def bulat_bawah(d):
    return Decimal(d).quantize(Decimal(1), ROUND_FLOOR)


def kredit_pph22(pph, pph22):
    """PPh 22 marketplace = bagian pelunasan PPh final masa yang sama (FAQ DJP PMK 37/2025 no. 14-15).
    Kembalikan (setor_sendiri, lebih_dipungut), keduanya dibulatkan ke bawah ke rupiah penuh."""
    selisih = pph - pph22
    if selisih > 0:
        return bulat_bawah(selisih), Decimal(0)
    return Decimal(0), bulat_bawah(-selisih)


# ---------------------------------------------------------------- jangka waktu (PP 20/2026)
def catatan_jangka_waktu(jenis, jenis_badan, tahun, tahun_terdaftar):
    """Jangka waktu pemakaian tarif 0,5% setelah PP 20/2026 (naskah resmi, dicek 2026-10-14)."""
    kunci = "op" if jenis == "op" else jenis_badan
    if kunci in ("op", "pt-perorangan"):
        label = "orang pribadi" if kunci == "op" else "PT perorangan"
        gabung = (" (digabung dengan omzet PT perorangan yang Anda dirikan)" if kunci == "op" else
                  " (digabung dengan omzet pendirinya dan PT perorangan lain miliknya)")
        teks = ("Jangka waktu tarif 0,5% untuk {}: tidak ada lagi batas tahun. PP 20/2026 (berlaku 22 April 2026, "
                "Pasal I angka 6) menghapus Pasal 59 PP 55/2022 yang dulu membatasi {} tahun pajak; tarif 0,5% boleh "
                "dipakai selama omzet setahun{} tidak melebihi Rp4,8 miliar dan Anda tidak memilih tarif umum."
                .format(label, JANGKA_WAKTU_LAMA[kunci], gabung))
        return teks + _tambahan_peralihan(kunci, tahun, tahun_terdaftar)

    return _jangka_waktu_badan_lain(kunci, tahun, tahun_terdaftar)


def catatan_jangka_waktu_chat(jenis, jenis_badan, tahun, tahun_terdaftar, ringkas=False):
    """Versi pendek untuk tampilan chat (ringkas=True: lebih pendek lagi); isi aturan sama dengan
    catatan_jangka_waktu()."""
    kunci = "op" if jenis == "op" else jenis_badan
    if kunci in ("op", "pt-perorangan"):
        label = "orang pribadi" if kunci == "op" else "PT perorangan"
        gabung = (" (digabung PT perorangan yang Anda dirikan)" if kunci == "op" else
                  " (digabung omzet pendirinya dan PT perorangan lain miliknya)")
        if ringkas:
            teks = ("Tarif 0,5% {} tanpa batas tahun (PP 20/2026, berlaku 22 April 2026, Pasal I angka 6, menghapus "
                    "Pasal 59 PP 55/2022) selama omzet setahun{} tidak lebih dari Rp4,8 miliar dan Anda tidak memilih "
                    "tarif umum.".format(label, gabung))
        else:
            teks = ("Tarif 0,5% untuk {} kini tanpa batas tahun: PP 20/2026 (berlaku 22 April 2026, Pasal I angka 6) "
                    "menghapus Pasal 59 PP 55/2022 (dulu {} tahun), selama omzet setahun{} tidak lebih dari Rp4,8 "
                    "miliar dan Anda tidak memilih tarif umum.".format(label, JANGKA_WAKTU_LAMA[kunci], gabung))
        return teks + _tambahan_peralihan(kunci, tahun, tahun_terdaftar, ringkas=True)
    return catatan_jangka_waktu(jenis, jenis_badan, tahun, tahun_terdaftar)


def _tambahan_peralihan(kunci, tahun, tahun_terdaftar, ringkas=False):
    """Tambahan untuk OP/PT perorangan yang menyebut tahun NPWP (aturan peralihan PP 20/2026 Pasal II)."""
    if tahun_terdaftar is None:
        return ""
    akhir_lama = max(tahun_terdaftar, 2018) + JANGKA_WAKTU_LAMA[kunci] - 1
    if kunci == "pt-perorangan" and akhir_lama < 2025:
        # Pasal II angka 1 huruf a hanya menyebut PT perorangan yang batas lamanya berakhir 2025.
        if ringkas:
            return (" NPWP {}: batas lama berakhir {} dan tidak disebut di aturan peralihan PP 20/2026; pastikan ke "
                    "DJP apakah tahun pajak {} boleh memakai 0,5%.".format(tahun_terdaftar, akhir_lama, tahun))
        return (" Batas lama Anda (NPWP {}) berakhir {}; aturan peralihan PP 20/2026 tidak menyebut PT "
                "perorangan yang batasnya berakhir sebelum 2025, jadi pastikan ke DJP apakah tahun pajak {} "
                "boleh memakai 0,5%.".format(tahun_terdaftar, akhir_lama, tahun))
    if akhir_lama in (2024, 2025):
        if ringkas:
            return (" NPWP {}: batas lama {}, boleh 0,5% lagi (PP 20/2026 Pasal II angka 1 huruf a).".format(
                tahun_terdaftar, akhir_lama))
        return (" Batas lama Anda (NPWP {}) sebenarnya berakhir {}, tetapi PP 20/2026 Pasal II angka 1 "
                "huruf a membolehkan kembali memakai 0,5%.".format(tahun_terdaftar, akhir_lama))
    return ""


def _jangka_waktu_badan_lain(kunci, tahun, tahun_terdaftar):
    """Koperasi, CV, firma, PT biasa, atau bentuk badan belum disebut."""
    if kunci == "koperasi":
        dasar = ("Koperasi: tarif 0,5% paling lama 4 tahun pajak sejak terdaftar (PP 20/2026 Pasal 57 ayat (2) "
                 "huruf f); koperasi yang terdaftar sebelum 22 April 2026 dan batas lamanya berakhir 2024–2029 "
                 "boleh memakai 0,5% sampai tahun pajak 2029 (Pasal II angka 1 huruf b).")
        if tahun_terdaftar is None:
            return dasar + " Sebutkan tahun NPWP koperasi terdaftar agar tahun akhirnya dihitung."
        akhir_lama = max(tahun_terdaftar, 2018) + 3
        if tahun_terdaftar <= TAHUN_PP20 and 2024 <= akhir_lama <= 2029:
            akhir = 2029
        elif tahun_terdaftar <= TAHUN_PP20:
            akhir = akhir_lama
        else:
            akhir = tahun_terdaftar + 3
        return dasar + " NPWP {} -> tarif 0,5% s.d. tahun pajak {}.{}".format(
            tahun_terdaftar, akhir, _status_akhir(tahun, akhir))

    if kunci in ("cv", "firma", "pt"):
        n = JANGKA_WAKTU_LAMA[kunci]
        label = LABEL_BADAN[kunci]
        dasar = ("{} sudah dikeluarkan dari skema 0,5% oleh PP 20/2026 (Pasal 57 ayat (1)). Yang terdaftar sebelum "
                 "22 April 2026 hanya boleh meneruskan sisa jangka waktu lamanya, yaitu {} tahun pajak sejak terdaftar "
                 "(paling awal dihitung 2018), selama masih memenuhi syarat (Pasal II angka 1 huruf e)."
                 .format(label, n))
        if tahun_terdaftar is None:
            return dasar + " Sebutkan tahun NPWP terdaftar agar tahun akhirnya dihitung."
        if tahun_terdaftar > TAHUN_PP20:
            return dasar + (" NPWP {} terdaftar setelah aturan ini berlaku, jadi tidak bisa memakai 0,5%; hasil di "
                            "atas hanya simulasi.".format(tahun_terdaftar))
        akhir = max(tahun_terdaftar, 2018) + n - 1
        teks = dasar + " NPWP {} -> tarif 0,5% s.d. tahun pajak {}.".format(tahun_terdaftar, akhir)
        if tahun_terdaftar == TAHUN_PP20:
            teks += " Ini hanya berlaku bila terdaftar sebelum 22 April 2026; bila sesudahnya, tidak bisa memakai 0,5%."
        return teks + _status_akhir(tahun, akhir)

    return ("Jangka waktu tarif 0,5% setelah PP 20/2026: PT perorangan tanpa batas tahun; koperasi 4 tahun pajak "
            "(peralihan s.d. 2029 bagi yang terdaftar sebelum 22 April 2026); CV, firma, dan PT biasa hanya "
            "meneruskan sisa jangka waktu lama. Sebutkan bentuk badan dan tahun NPWP terdaftar agar dihitung.")


def _status_akhir(tahun, akhir):
    if tahun > akhir:
        return (" PERHATIAN: tahun pajak {} sudah MELEWATI batas itu, jadi hasil 0,5% di atas tidak berlaku; "
                "pajaknya memakai tarif umum dengan pembukuan.".format(tahun))
    if tahun == akhir:
        return " Tahun pajak {} adalah tahun TERAKHIR memakai 0,5%.".format(tahun)
    return ""


# ---------------------------------------------------------------- perhitungan bulanan
def hitung(data, jenis, tahun, omzet_sebelumnya=Decimal(0), hari_ini=None, proyeksi_mulai=None,
           marketplace=False):
    if not data:
        raise ValueError("belum ada data omzet")
    if len(data) > 12:
        raise ValueError("maksimal 12 bulan dalam satu tahun pajak")
    dilihat = set()
    for b, o, p in data:
        if b in dilihat:
            raise ValueError("bulan {} diisi lebih dari sekali".format(NAMA_BULAN[b - 1]))
        dilihat.add(b)
        if o < 0:
            raise ValueError("omzet {} tidak boleh negatif".format(NAMA_BULAN[b - 1]))
        if p < 0:
            raise ValueError("PPh 22 {} tidak boleh negatif".format(NAMA_BULAN[b - 1]))
    if omzet_sebelumnya < 0:
        raise ValueError("omzet sebelumnya tidak boleh negatif")
    data = sorted(data)
    if proyeksi_mulai is not None and not any(b >= proyeksi_mulai for b, _, _ in data):
        raise ValueError("bulan proyeksi ({}) tidak ada di data omzet".format(NAMA_BULAN[proyeksi_mulai - 1]))
    kumulatif = omzet_sebelumnya
    rows = []
    catatan = []
    # Tampilan chat: pasangan (teks biasa, teks ringkas) - teks ringkas dipakai bila blok chat terlalu panjang
    # (tingkat >= 2). Isi, angka, tanggal & pasal sama dengan `catatan`; hanya kalimatnya lebih pendek.
    catatan_chat = []
    bulan_lewat_500 = None
    bulan_lewat_500_angka = None
    bulan_lewat_48 = None
    if jenis == "op" and omzet_sebelumnya >= BATAS_BEBAS_OP:
        bulan_lewat_500 = "sebelum periode ini"
    for b, omzet, pph22 in data:
        proyeksi = proyeksi_mulai is not None and b >= proyeksi_mulai
        sebelum = kumulatif
        kumulatif = sebelum + omzet
        if jenis == "op":
            # Hanya bagian omzet di atas Rp500 juta (kumulatif setahun) yang kena pajak
            kena = max(kumulatif - max(sebelum, BATAS_BEBAS_OP), Decimal(0))
        else:
            kena = omzet
        pph = bulat_bawah(kena * TARIF)
        setor, lebih = kredit_pph22(pph, pph22)
        tgl15 = batas_setor(tahun, b)
        tgl_kerja, alasan_geser, libur_lengkap = geser_hari_kerja(tgl15)
        status = status_relatif(tgl_kerja, hari_ini) if (setor > 0 and not proyeksi) else ""
        ket = []
        if proyeksi:
            ket.append("proyeksi")
        if jenis == "op" and sebelum <= BATAS_BEBAS_OP < kumulatif:
            bulan_lewat_500, bulan_lewat_500_angka = NAMA_BULAN[b - 1], b
            ket.append("melewati Rp500 juta; hanya {} yang kena pajak".format(format_rp(kena, True)))
        elif jenis == "op" and kumulatif <= BATAS_BEBAS_OP:
            ket.append("masih dalam Rp500 juta bebas")
        if sebelum <= BATAS_OMZET_UMKM < kumulatif:
            bulan_lewat_48 = NAMA_BULAN[b - 1]
            ket.append("omzet setahun melewati Rp4,8 miliar")
        if pph22 > 0:
            if lebih > 0:
                ket.append("PPh 22 lebih dipungut, bisa diminta kembali")
            elif setor == 0:
                ket.append("lunas lewat PPh 22 marketplace")
        rows.append({
            "bulan": b,
            "nama_bulan": NAMA_BULAN[b - 1],
            "proyeksi": proyeksi,
            "omzet": omzet,
            "omzet_kumulatif": kumulatif,
            "omzet_kena_pajak": kena,
            "pph_final": pph,
            "pph22_dipungut": pph22,
            "setor_sendiri": setor,
            "lebih_dipungut": lebih,
            "setor_paling_lambat": tgl15.isoformat(),
            "setor_hari_kerja": tgl_kerja.isoformat(),
            "setor_hari_kerja_teks": format_tgl(tgl_kerja),
            "batas_setor_hari_libur": tgl_kerja != tgl15,
            "alasan_geser": alasan_geser,
            "data_libur_lengkap": libur_lengkap,
            "status_batas": status,
            "batas_setor_sudah_lewat": status == "sudah lewat",
            "keterangan": "; ".join(ket),
        })

    aktual = [r for r in rows if not r["proyeksi"]]
    proy = [r for r in rows if r["proyeksi"]]
    jumlah = lambda rs, k: sum((r[k] for r in rs), Decimal(0))  # noqa: E731
    mode_pph22 = any(r["pph22_dipungut"] > 0 for r in rows)
    sisa_bebas = max(BATAS_BEBAS_OP - kumulatif, Decimal(0)) if jenis == "op" else None

    terdekat = None
    if hari_ini is not None:
        akan = [r for r in aktual if r["setor_sendiri"] > 0
                and datetime.date.fromisoformat(r["setor_hari_kerja"]) >= hari_ini]
        if akan:
            r = akan[0]
            tk = datetime.date.fromisoformat(r["setor_hari_kerja"])
            terdekat = {"bulan": r["nama_bulan"], "tanggal": r["setor_hari_kerja"], "tanggal_teks": format_tgl(tk),
                        "jarak": keterangan_jarak(tk, hari_ini), "setor_sendiri": r["setor_sendiri"]}

    bulan_ada = [r["bulan"] for r in rows]
    if bulan_ada[0] > 1 and omzet_sebelumnya == 0:
        catatan.append("Data mulai {}. Omzet bulan sebelumnya di tahun {} dianggap Rp0; bila ada, sebutkan totalnya "
                       "agar batas Rp500 juta dihitung benar.".format(NAMA_BULAN[bulan_ada[0] - 1], tahun))
        catatan_chat.append(("Omzet {} sebelum {} dianggap Rp0; bila ada, sebutkan totalnya agar batas Rp500 juta "
                             "dihitung benar.".format(tahun, NAMA_BULAN[bulan_ada[0] - 1]),) * 2)
    celah = [NAMA_BULAN[x - 1] for x in range(bulan_ada[0], bulan_ada[-1] + 1) if x not in bulan_ada]
    if celah:
        catatan.append("Bulan tanpa data dianggap omzet Rp0: {}.".format(", ".join(celah)))
        catatan_chat.append((catatan[-1],) * 2)
    if proy:
        catatan.append("Bulan {} memakai omzet perkiraan (proyeksi), bukan data nyata; angkanya akan berubah bila "
                       "omzet sebenarnya berbeda.".format(rentang_bulan(proy)))
        catatan_chat.append(("{} memakai omzet perkiraan (proyeksi); angkanya berubah bila omzet sebenarnya "
                             "berbeda.".format(rentang_bulan(proy)),) * 2)
    if bulan_lewat_48:
        teks = ("Omzet kumulatif melewati Rp4,8 miliar pada {}. Tahun pajak ini umumnya masih memakai 0,5%, tetapi "
                "mulai tahun pajak berikutnya memakai tarif umum dengan pembukuan.".format(bulan_lewat_48))
        if jenis == "op":
            teks += (" Menurut PP 20/2026 Pasal 57 ayat (2) huruf e dan ayat (4), orang pribadi (digabung PT "
                     "perorangan yang didirikannya) yang omzetnya melewati Rp4,8 miliar tidak bisa lagi memakai 0,5% "
                     "di tahun-tahun berikutnya.")
        catatan.append(teks + " Pastikan ke DJP/konsultan pajak.")
        catatan_chat.append(("Omzet setahun melewati Rp4,8 miliar pada {}: tahun pajak ini umumnya masih 0,5%, tetapi "
                             "mulai tahun pajak berikutnya memakai tarif umum dengan pembukuan{}. Pastikan ke "
                             "DJP/konsultan pajak.".format(
                                 bulan_lewat_48, "; orang pribadi (digabung PT perorangan yang didirikannya) tidak "
                                 "bisa lagi memakai 0,5% di tahun-tahun berikutnya (PP 20/2026 Pasal 57 ayat (2) huruf e "
                                 "& ayat (4))" if jenis == "op" else ""),) * 2)
    elif kumulatif > BATAS_OMZET_UMKM * Decimal("0.8"):
        catatan.append("Omzet kumulatif sudah di atas 80% dari batas Rp4,8 miliar. Siapkan pembukuan bila "
                       "batas terlewati.")
        catatan_chat.append((catatan[-1],) * 2)
    libur_belum_ada = set()
    for r in rows:
        if r["batas_setor_hari_libur"] and r["setor_sendiri"] > 0:
            tk = datetime.date.fromisoformat(r["setor_hari_kerja"])
            catatan.append("Setoran masa {} {}: tanggal 15 jatuh pada hari libur ({}) -> boleh disetor paling "
                           "lambat hari kerja berikutnya, {} (PMK 81/2024 Pasal 100 ayat (1)).{}".format(
                               r["nama_bulan"], tahun, ", ".join(r["alasan_geser"]), format_tgl(tk),
                               "" if r["data_libur_lengkap"] else " Data libur nasional/cuti bersama tahun itu "
                               "belum tersedia di hitungan ini (hanya Sabtu/Minggu yang dicek); cek kalender pajak DJP."))
            if not r["data_libur_lengkap"]:
                libur_belum_ada.add(datetime.date.fromisoformat(r["setor_paling_lambat"]).year)
    # Tampilan chat: tanggal hari kerja hasil geser sudah tertulis di baris tiap bulan ("tgl 15 libur").
    if libur_belum_ada:
        catatan_chat.append(("Data libur nasional/cuti bersama {} belum tersedia (hanya Sabtu/Minggu yang dicek); "
                             "cek kalender pajak DJP.".format(", ".join(str(x) for x in sorted(libur_belum_ada))),) * 2)
    lewat = [r for r in aktual if r["batas_setor_sudah_lewat"]]
    if lewat:
        daftar_lewat = ", ".join("{} ({})".format(r["nama_bulan"], format_rp(r["setor_sendiri"])) for r in lewat)
        catatan.append("Batas setor sudah lewat per {} untuk: {}. Bila belum disetor, segera setor dan tanyakan ke DJP "
                       "kemungkinan sanksi administrasi keterlambatan.".format(format_tgl(hari_ini), daftar_lewat))
        catatan_chat.append((
            "Batas setor sudah lewat per {} untuk: {}. Bila belum disetor, segera setor dan tanyakan ke DJP soal sanksi "
            "keterlambatan.".format(format_tgl(hari_ini), daftar_lewat),
            "Batas setor sudah lewat per {}: {} (lihat baris tiap bulan). Bila belum disetor, segera setor; tanyakan "
            "ke DJP soal sanksi.".format(
                format_tgl(hari_ini), daftar_bulan_ringkas([r["bulan"] for r in lewat]))))
    if mode_pph22:
        catatan.append("PPh 22 yang dipungut marketplace sudah diperhitungkan sebagai bagian pelunasan PPh final tiap "
                       "bulan: kekurangannya disetor sendiri, kelebihannya dapat diajukan permohonan pengembalian ke DJP "
                       "(FAQ DJP PMK 37/2025 versi 1 Juli 2026, no. 14-15). Simpan bukti pungut atau dokumen tagihan "
                       "dari marketplace.")
        catatan_chat.append((
            "PPh 22 marketplace = bagian pelunasan PPh final bulan itu: kurangnya disetor sendiri, lebihnya bisa "
            "diajukan pengembalian ke DJP (FAQ DJP PMK 37/2025 no. 14-15). Simpan bukti pungutnya.",
            "PPh 22 marketplace = bagian pelunasan PPh final bulan itu: kurang disetor sendiri, lebih bisa diajukan "
            "pengembalian ke DJP (FAQ DJP PMK 37/2025 no. 14-15). Simpan bukti pungut."))
        bebas_tapi_dipungut = [r["nama_bulan"] for r in rows if jenis == "op" and r["pph_final"] == 0
                               and r["pph22_dipungut"] > 0 and r["omzet_kumulatif"] <= BATAS_BEBAS_OP]
        if bebas_tapi_dipungut:
            catatan.append("Pada {} marketplace memungut PPh 22 padahal omzet setahun Anda belum lewat Rp500 juta. "
                           "Agar tidak dipungut lagi, sampaikan surat pernyataan bermeterai omzet s.d. Rp500 juta ke "
                           "marketplace (FAQ DJP PMK 37/2025 no. 16).".format(", ".join(bebas_tapi_dipungut)))
            daftar_bebas = daftar_bulan_ringkas([NAMA_BULAN.index(x) + 1 for x in bebas_tapi_dipungut])
            catatan_chat.append((
                "{}: marketplace memungut PPh 22 padahal omzet setahun belum lewat Rp500 juta. Agar tidak dipungut "
                "lagi, kirim surat pernyataan bermeterai omzet s.d. Rp500 juta ke marketplace (FAQ DJP PMK 37/2025 "
                "no. 16).".format(daftar_bebas),
                "{}: PPh 22 dipungut padahal omzet belum lewat Rp500 juta; agar tidak dipungut lagi, kirim surat "
                "pernyataan bermeterai omzet s.d. Rp500 juta ke marketplace (FAQ DJP PMK 37/2025 no. 16).".format(
                    daftar_bebas)))
    if (jenis == "op" and bulan_lewat_500_angka and (marketplace or mode_pph22)
            and not (proyeksi_mulai and bulan_lewat_500_angka >= proyeksi_mulai)):
        batas_sp = akhir_bulan(tahun, bulan_lewat_500_angka)
        teks = ("Omzet setahun Anda melewati Rp500 juta pada {}: bila Anda pernah menyampaikan surat pernyataan omzet "
                "s.d. Rp500 juta ke marketplace, sampaikan surat pernyataan bermeterai bahwa omzet sudah melewati "
                "Rp500 juta paling lambat {} (FAQ DJP PMK 37/2025 no. 9).".format(bulan_lewat_500, format_tgl(batas_sp)))
        teks_chat = ("Bila dulu pernah mengirim surat pernyataan omzet s.d. Rp500 juta ke marketplace: omzet lewat "
                     "Rp500 juta pada {}, jadi kirim surat pernyataan bermeterai baru bahwa omzet sudah melewati "
                     "Rp500 juta paling lambat {} (FAQ DJP PMK 37/2025 no. 9).".format(bulan_lewat_500,
                                                                                       format_tgl(batas_sp)))
        ringkas = ("Bila pernah kirim surat pernyataan omzet s.d. Rp500 juta ke marketplace: kirim surat pernyataan "
                   "bermeterai baru bahwa omzet sudah melewati Rp500 juta, paling lambat {} (FAQ DJP PMK 37/2025 "
                   "no. 9).".format(format_tgl(batas_sp)))
        if hari_ini is not None and hari_ini > batas_sp:
            teks += " Tanggal itu sudah lewat; bila belum, segera sampaikan."
            teks_chat += " Tanggal itu sudah lewat; bila belum, segera kirim."
            ringkas += " Sudah lewat: bila belum, segera kirim."
        catatan.append(teks)
        catatan_chat.append((teks_chat, ringkas))
    return {
        "versi": VERSI,
        "jenis_wp": jenis,
        "tahun": tahun,
        "omzet_sebelumnya": omzet_sebelumnya,
        "hari_ini": hari_ini.isoformat() if hari_ini else None,
        "hari_ini_teks": format_tgl(hari_ini) if hari_ini else None,
        "mode_pph22": mode_pph22,
        "bulan": rows,
        "ringkasan": {
            "rentang_data_nyata": rentang_bulan(aktual),
            "rentang_semua": rentang_bulan(rows),
            "total_omzet_periode": jumlah(rows, "omzet"),
            "omzet_kumulatif_tahun": kumulatif,
            "total_pph_final": jumlah(rows, "pph_final"),
            "total_pph_final_data_nyata": jumlah(aktual, "pph_final"),
            "total_pph_final_proyeksi": jumlah(proy, "pph_final"),
            "ada_proyeksi": bool(proy),
            "total_pph22_dipungut": jumlah(rows, "pph22_dipungut"),
            "total_setor_sendiri_data_nyata": jumlah(aktual, "setor_sendiri"),
            "total_setor_sendiri_proyeksi": jumlah(proy, "setor_sendiri"),
            "total_lebih_dipungut": jumlah(rows, "lebih_dipungut"),
            "sisa_omzet_bebas_pajak": sisa_bebas,
            "bulan_mulai_kena_pajak": bulan_lewat_500,
            "bulan_melewati_4_8_miliar": bulan_lewat_48,
            "batas_setor_terdekat": terdekat,
            "bulan_batas_setor_sudah_lewat": [r["nama_bulan"] for r in lewat],
        },
        "catatan": catatan,
        "_catatan_chat": catatan_chat,  # hanya untuk teks_chat(); dibuang dari keluaran JSON
    }


CATATAN_TETAP = [
    "Tarif 0,5% dihitung dari OMZET (peredaran bruto), bukan dari laba.",
    "Pembulatan: PPh tiap bulan dan selisihnya dengan PPh 22 dibulatkan ke bawah ke rupiah penuh; belum dicocokkan "
    "dengan Coretax - bila berbeda, ikuti Coretax.",
    "Batas setor = tanggal 15 bulan berikutnya (PMK 81/2024 Pasal 94); bila jatuh Sabtu/Minggu/libur nasional/cuti "
    "bersama, boleh disetor hari kerja berikutnya (Pasal 100 ayat (1)). Data libur: SKB 3 menteri 2026 & 2027; "
    "pemerintah bisa mengubahnya, cek kalender pajak DJP.",
    "Tidak berlaku untuk penghasilan dari jasa pekerjaan bebas (mis. dokter, notaris, konsultan, pengajar, "
    "influencer/selebgram/vloger, seniman) dan penghasilan lain yang dikecualikan PP 55/2022 jo. PP 20/2026.",
]


# Pasangan (teks biasa, teks ringkas untuk blok chat yang terlalu panjang); keduanya selalu tampil.
CATATAN_TETAP_CHAT = [
    ("Tarif 0,5% dari omzet (peredaran bruto), bukan laba. Tidak berlaku untuk jasa pekerjaan bebas (mis. dokter, "
     "notaris, konsultan, influencer) dan penghasilan lain yang dikecualikan PP 55/2022 jo. PP 20/2026.",
     "Tarif dari omzet, bukan laba; tidak untuk jasa pekerjaan bebas & penghasilan lain yang dikecualikan "
     "PP 55/2022 jo. PP 20/2026."),
    ("Batas setor tgl 15 bulan berikutnya; bila libur (termasuk cuti bersama), hari kerja berikutnya (PMK 81/2024 "
     "Pasal 94 & 100). Data libur dari SKB 3 menteri 2026-2027 dan bisa berubah; cek kalender pajak DJP.",
     "Batas setor tgl 15 bulan berikutnya, hari libur digeser ke hari kerja (PMK 81/2024 Pasal 94 & 100; data libur "
     "SKB 3 menteri, bisa berubah)."),
    ("Pembulatan: PPh dan selisihnya dengan PPh 22 dibulatkan ke bawah ke rupiah penuh; belum dicocokkan dengan "
     "Coretax - bila berbeda, ikuti Coretax.",) * 2,
]


def catatan_jenis(jenis):
    if jenis == "op":
        return ["Orang pribadi: omzet s.d. Rp500 juta setahun tidak dikenai PPh final. Batas ini untuk total "
                "omzet SEMUA usaha Anda dalam setahun (toko online dan offline digabung)."]
    return ["Badan: 0,5% x seluruh omzet, tanpa pembebasan Rp500 juta."]


def catatan_jenis_chat(jenis):
    """Pasangan (teks biasa, teks ringkas/None); untuk badan selalu tampil."""
    if jenis == "op":
        return [("Rp500 juta bebas pajak berlaku untuk total omzet SEMUA usaha Anda setahun (online + offline "
                 "digabung).", None)]
    return [(catatan_jenis(jenis)[0],) * 2]


# ---------------------------------------------------------------- mode data belum lengkap
def hitung_kemungkinan(bulan, omzet, tahun, hari_ini, pph22=Decimal(0)):
    """Satu bulan omzet, jenis WP & omzet sebelumnya belum diketahui -> tabel kemungkinan."""
    if omzet < 0 or pph22 < 0:
        raise ValueError("omzet dan PPh 22 tidak boleh negatif")
    penuh = bulat_bawah(omzet * TARIF)
    nb = NAMA_BULAN[bulan - 1]
    rentang = ("Januari–{} {}".format(NAMA_BULAN[bulan - 2], tahun) if bulan > 2 else "Januari {}".format(tahun))
    baris = []
    if bulan == 1:
        op = bulat_bawah(max(omzet - BATAS_BEBAS_OP, Decimal(0)) * TARIF)
        baris.append(("Orang pribadi (Januari = awal hitungan Rp500 juta)", op, op))
    else:
        if omzet <= BATAS_BEBAS_OP:
            ambang = BATAS_BEBAS_OP - omzet
            baris.append(("Orang pribadi, omzet {} paling banyak {}".format(rentang, format_rp(ambang)),
                          Decimal(0), Decimal(0)))
            if ambang < BATAS_BEBAS_OP:
                baris.append(("Orang pribadi, omzet {} di atas {} tetapi di bawah Rp500.000.000".format(
                    rentang, format_rp(ambang)), Decimal(0), penuh))
        else:
            minimal = bulat_bawah((omzet - BATAS_BEBAS_OP) * TARIF)
            baris.append(("Orang pribadi, belum ada omzet {}".format(rentang), minimal, minimal))
            baris.append(("Orang pribadi, omzet {} di bawah Rp500.000.000".format(rentang), minimal, penuh))
        baris.append(("Orang pribadi, omzet {} sudah Rp500.000.000 atau lebih".format(rentang), penuh, penuh))
    baris.append(("Badan (PT perorangan, koperasi)", penuh, penuh))
    tgl15 = batas_setor(tahun, bulan)
    tk, alasan, lengkap = geser_hari_kerja(tgl15)
    hasil = []
    for kondisi, mn, mx in baris:
        item = {"kondisi": kondisi, "pph_min": mn, "pph_max": mx}
        if mn == mx:
            item["pph_teks"] = format_rp(mn)
            if pph22 > 0:
                setor, lebih = kredit_pph22(mn, pph22)
                item["setor_sendiri"], item["lebih_dipungut"] = setor, lebih
                item["kurang_lebih_teks"] = _teks_kurang_lebih(mn, pph22, setor, lebih)
        else:
            item["pph_teks"] = "antara {} dan {} (0,5% x bagian omzet kumulatif di atas Rp500 juta)".format(
                format_rp(mn), format_rp(mx))
            if pph22 > 0:
                item["kurang_lebih_teks"] = "tergantung omzet sebelumnya"
        hasil.append(item)
    catatan = ["Hasil pasti bisa dihitung setelah bentuk usaha (pribadi atau badan) dan total omzet {} diketahui."
               .format(rentang) if bulan > 1 else
               "Hasil pasti bisa dihitung setelah bentuk usaha (pribadi atau badan) diketahui.",
               "Batas Rp500 juta (khusus orang pribadi) dihitung dari total omzet SEMUA usaha sejak Januari."]
    if pph22 > 0:
        catatan.append("PPh 22 yang dipungut marketplace adalah bagian pelunasan PPh final: kekurangannya disetor "
                       "sendiri, kelebihannya dapat diajukan pengembalian (FAQ DJP PMK 37/2025 no. 14-15).")
    if tk != tgl15:
        catatan.append("Tanggal 15 jatuh pada hari libur ({}) -> boleh disetor paling lambat {} (PMK 81/2024 Pasal "
                       "100 ayat (1)).".format(", ".join(alasan), format_tgl(tk)))
    return {
        "versi": VERSI,
        "mode": "kemungkinan",
        "tahun": tahun,
        "bulan": bulan,
        "nama_bulan": nb,
        "omzet": omzet,
        "pph22_dipungut": pph22,
        "hari_ini": hari_ini.isoformat(),
        "hari_ini_teks": format_tgl(hari_ini),
        "kemungkinan": hasil,
        "setor_paling_lambat": tgl15.isoformat(),
        "setor_hari_kerja": tk.isoformat(),
        "setor_hari_kerja_teks": format_tgl(tk),
        "jarak_batas_setor": keterangan_jarak(tk, hari_ini),
        "data_libur_lengkap": lengkap,
        "catatan": catatan,
    }


def _teks_kurang_lebih(pph, pph22, setor, lebih):
    if setor > 0:
        return "kurang {} (setor sendiri)".format(format_rp(setor))
    if lebih > 0:
        return "lebih {}".format(format_rp(lebih))
    if pph > 0 or pph22 > 0:
        return "lunas"
    return "-"


# ---------------------------------------------------------------- output
def _kaki(out):
    out.append("")
    out.append("_Dasar: {}. Berlaku per {}. Ini alat bantu hitung, bukan nasihat pajak. Untuk kepastian, hubungi "
               "DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak._".format(DASAR_ATURAN, TANGGAL_ATURAN))


def teks_markdown(h, jenis_badan):
    r = h["ringkasan"]
    label = "Orang pribadi" if h["jenis_wp"] == "op" else "Badan" + (
        " - {}".format(LABEL_BADAN[jenis_badan]) if jenis_badan else "")
    out = ["## PPh Final UMKM 0,5% - Tahun {} ({})".format(h["tahun"], label), ""]
    if h["hari_ini_teks"]:
        out.append("Hari ini (tanggal acuan hitungan): {}".format(h["hari_ini_teks"]))
    if h["omzet_sebelumnya"]:
        out.append("Omzet tahun ini sebelum periode tabel: {}".format(format_rp(h["omzet_sebelumnya"], True)))
    out.append("")
    m22 = h["mode_pph22"]
    if m22:
        out.append("| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 dipungut marketplace "
                   "| Kurang/lebih setor | Setor paling lambat | Keterangan |")
        out.append("|---|---:|---:|---:|---:|---:|---|---|---|")
    else:
        out.append("| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | Setor paling lambat "
                   "| Keterangan |")
        out.append("|---|---:|---:|---:|---:|---|---|")
    for b in h["bulan"]:
        if b["setor_sendiri"] > 0:
            tk = datetime.date.fromisoformat(b["setor_hari_kerja"])
            setor_txt = format_tgl_tabel(tk) + (" (tgl 15 libur)" if b["batas_setor_hari_libur"] else "")
            if b["status_batas"]:
                setor_txt += " - " + b["status_batas"].upper()
        else:
            setor_txt = "-"
        sel = [b["nama_bulan"] + (" (proyeksi)" if b["proyeksi"] else ""), format_rp(b["omzet"], True),
               format_rp(b["omzet_kumulatif"], True), format_rp(b["omzet_kena_pajak"], True), format_rp(b["pph_final"])]
        if m22:
            sel += [format_rp(b["pph22_dipungut"], True) if b["pph22_dipungut"] else "-",
                    _teks_kurang_lebih(b["pph_final"], b["pph22_dipungut"], b["setor_sendiri"], b["lebih_dipungut"])]
        sel += [setor_txt, b["keterangan"] or "-"]
        out.append("| " + " | ".join(sel) + " |")
    kosong_kanan = ["", ""]
    if r["ada_proyeksi"]:
        nyata = [b for b in h["bulan"] if not b["proyeksi"]]
        if nyata:
            sel = ["**Subtotal data nyata ({})**".format(r["rentang_data_nyata"]),
                   "**{}**".format(format_rp(sum((b["omzet"] for b in nyata), Decimal(0)), True)), "", "",
                   "**{}**".format(format_rp(r["total_pph_final_data_nyata"]))]
            if m22:
                sel += [format_rp(sum((b["pph22_dipungut"] for b in nyata), Decimal(0)), True),
                        "kurang {}".format(format_rp(r["total_setor_sendiri_data_nyata"]))]
            out.append("| " + " | ".join(sel + kosong_kanan) + " |")
        sel = ["**Total termasuk proyeksi ({})**".format(r["rentang_semua"]),
               "**{}**".format(format_rp(r["total_omzet_periode"], True)), "", "",
               "**{}**".format(format_rp(r["total_pph_final"]))]
    else:
        sel = ["**Total ({})**".format(r["rentang_semua"]), "**{}**".format(format_rp(r["total_omzet_periode"], True)),
               "", "", "**{}**".format(format_rp(r["total_pph_final"]))]
    if m22:
        tot = "kurang {}".format(format_rp(r["total_setor_sendiri_data_nyata"] + r["total_setor_sendiri_proyeksi"]))
        if r["total_lebih_dipungut"]:
            tot += "; lebih {}".format(format_rp(r["total_lebih_dipungut"]))
        sel += [format_rp(r["total_pph22_dipungut"], True), tot]
    out.append("| " + " | ".join(sel + kosong_kanan) + " |")
    out.append("")
    out.append("**Ringkasan**")
    out.append("- Omzet kumulatif tahun {}{}: {}".format(h["tahun"], " (termasuk proyeksi)" if r["ada_proyeksi"] else "",
                                                         format_rp(r["omzet_kumulatif_tahun"], True)))
    if r["ada_proyeksi"]:
        if r["rentang_data_nyata"] != "-":
            out.append("- Total PPh final data nyata ({}): {}".format(r["rentang_data_nyata"],
                                                                     format_rp(r["total_pph_final_data_nyata"])))
        out.append("- Perkiraan total PPh final termasuk proyeksi ({}): {}".format(r["rentang_semua"],
                                                                                   format_rp(r["total_pph_final"])))
    else:
        out.append("- Total PPh final ({}): {}".format(r["rentang_semua"], format_rp(r["total_pph_final"])))
    if m22:
        out.append("- PPh 22 yang sudah dipungut marketplace: {}".format(format_rp(r["total_pph22_dipungut"], True)))
        out.append("- Total kurang setor (disetor sendiri){}: {}".format(
            " data nyata" if r["ada_proyeksi"] else "", format_rp(r["total_setor_sendiri_data_nyata"])))
        if r["total_lebih_dipungut"]:
            out.append("- Total lebih dipungut (dapat diajukan pengembalian): {}".format(
                format_rp(r["total_lebih_dipungut"])))
    t = r["batas_setor_terdekat"]
    if t:
        out.append("- Batas setor terdekat yang belum lewat: {} ({}), masa {}, setor sendiri {}".format(
            t["tanggal_teks"], t["jarak"], t["bulan"], format_rp(t["setor_sendiri"])))
    if h["jenis_wp"] == "op":
        if r["sisa_omzet_bebas_pajak"] > 0:
            out.append("- Sisa omzet bebas pajak tahun ini: {}".format(format_rp(r["sisa_omzet_bebas_pajak"], True)))
        elif r["bulan_mulai_kena_pajak"]:
            out.append("- Batas Rp500 juta bebas pajak sudah terlewati ({}).".format(r["bulan_mulai_kena_pajak"]))
        else:
            out.append("- Omzet tepat mencapai batas Rp500 juta: belum ada omzet yang kena pajak, tetapi mulai rupiah "
                       "berikutnya seluruh omzet kena 0,5%.")
    out.append("- Sisa ruang sebelum batas Rp4,8 miliar: {}".format(
        format_rp(max(BATAS_OMZET_UMKM - r["omzet_kumulatif_tahun"], Decimal(0)), True)))
    out.append("")
    out.append("**Catatan penting**")
    for c in h["catatan"]:
        out.append("- " + c)
    _kaki(out)
    return "\n".join(out)


def teks_kemungkinan(h):
    out = ["## Perkiraan PPh Final UMKM 0,5% - {} {} (data belum lengkap)".format(h["nama_bulan"], h["tahun"]), "",
           "Hari ini (tanggal acuan hitungan): {}".format(h["hari_ini_teks"]),
           "Omzet {} {}: {}".format(h["nama_bulan"], h["tahun"], format_rp(h["omzet"], True))]
    if h["pph22_dipungut"]:
        out.append("PPh 22 dipungut marketplace {}: {}".format(h["nama_bulan"], format_rp(h["pph22_dipungut"], True)))
    out.append("")
    m22 = h["pph22_dipungut"] > 0
    out.append("| Kondisi usaha Anda | PPh final 0,5% {} |{}".format(h["nama_bulan"], " Kurang/lebih setor |" if m22 else ""))
    out.append("|---|---:|{}".format("---|" if m22 else ""))
    for k in h["kemungkinan"]:
        out.append("| {} | {} |{}".format(k["kondisi"], k["pph_teks"],
                                         " {} |".format(k.get("kurang_lebih_teks", "-")) if m22 else ""))
    out.append("")
    tk = datetime.date.fromisoformat(h["setor_hari_kerja"])
    out.append("Setor paling lambat (masa {} {}): {} ({}).".format(h["nama_bulan"], h["tahun"], format_tgl(tk),
                                                                   h["jarak_batas_setor"]))
    out.append("")
    out.append("**Catatan penting**")
    for c in h["catatan"]:
        out.append("- " + c)
    _kaki(out)
    return "\n".join(out)


# ---------------------------------------------------------------- tampilan chat (Telegram/WhatsApp)
# Tanpa tabel & tanpa blok kode: OpenClaw mengubah tabel Markdown menjadi blok kode monospace di Telegram, yang
# harus digeser ke samping di ponsel. Baris data (judul, per bulan, ringkasan) pendek (<= 60 karakter tampil untuk
# omzet bulanan di bawah Rp1 miliar tanpa sen; +-67 bila miliar & bersen); keterangan & catatan berupa kalimat biasa
# yang dilipat otomatis oleh aplikasi chat. Angka sama persis dengan tampilan tabel. Hanya karakter cp1252 (Windows).
BATAS_CHAT = 3800  # karakter; satu pesan Telegram maks. 4.096, sisakan ruang untuk kalimat pembuka & pertanyaan
PENANDA_PESAN = "<<< PESAN BERIKUTNYA >>>"
# Tingkat ringkas (dipakai berurutan sampai blok <= BATAS_CHAT):
#   0 = normal; 1 = bulan berurutan yang lunas lewat PPh 22 ikut digabung (jumlah per bulan tetap disebut);
#   2 = keterangan bulan & catatan versi ringkas (isi, angka, tanggal, pasal sama);
#   3 = baris bulan tanpa omzet, "paling lambat" -> "s.d.", kaki dasar aturan dipersingkat.
# Bila tingkat 3 pun > BATAS_CHAT: blok dibagi dua dengan baris PENANDA_PESAN sebelum **Ringkasan**.
TINGKAT_RINGKAS_MAKS = 3


def _kaki_chat(out, tingkat=0):
    tgl = datetime.date.fromisoformat(TANGGAL_ATURAN)
    out.append("")
    if tingkat >= 3:
        out.append("_Dasar: PP 55/2022 jo. PP 20/2026; PMK 37/2025; PMK 81/2024. Berlaku per {} {}. Bukan nasihat "
                   "pajak; kepastian: Kring Pajak 1500200 atau konsultan pajak._".format(format_tgl_pendek(tgl), tgl.year))
        return
    out.append("_Dasar: {}. Berlaku per {} {}. Alat bantu hitung, bukan nasihat pajak; kepastian: Kring Pajak "
               "1500200 atau konsultan pajak._".format(DASAR_ATURAN_CHAT, format_tgl_pendek(tgl), tgl.year))


def _baris_bulan_chat(nama, omzet, pph, tingkat=0):
    """Satu baris pendek per bulan, maks. 3 kolom: bulan · omzet · PPh final (tingkat 3: tanpa omzet)."""
    if tingkat >= 3:
        return "**{}** · PPh {}".format(nama, format_rp(pph))
    return "**{}** · omzet {} · PPh {}".format(nama, format_rp(omzet, True), format_rp(pph))


def _istimewa(b, jenis):
    sebelum = b["omzet_kumulatif"] - b["omzet"]
    return ((jenis == "op" and sebelum <= BATAS_BEBAS_OP < b["omzet_kumulatif"])
            or sebelum <= BATAS_OMZET_UMKM < b["omzet_kumulatif"])


def _jenis_kelompok(b, jenis, tingkat):
    """'bebas' (OP masih dalam Rp500 juta) / 'lunas' (tertutup PPh 22, mulai tingkat 1) / None."""
    if b["proyeksi"] or _istimewa(b, jenis):
        return None
    if jenis == "op" and b["omzet_kumulatif"] <= BATAS_BEBAS_OP and b["pph_final"] == 0:
        return "bebas"
    if tingkat >= 1 and b["pph22_dipungut"] > 0 and b["setor_sendiri"] == 0 and b["lebih_dipungut"] == 0:
        return "lunas"
    return None


def _kelompok_chat(rows, jenis, tingkat=0):
    """Gabungkan bulan berurutan sejenis (bukan proyeksi); bulan lain tetap satu per satu."""
    kelompok = []
    for b in rows:
        jk = _jenis_kelompok(b, jenis, tingkat)
        akhir = kelompok[-1] if kelompok else None
        if jk and akhir and akhir[0] == jk and akhir[1][-1]["bulan"] == b["bulan"] - 1:
            akhir[1].append(b)
        else:
            kelompok.append((jk, [b]))
    return kelompok


def _batas_chat(b, tingkat):
    tk = datetime.date.fromisoformat(b["setor_hari_kerja"])
    tanda = [x for x in ("tgl 15 libur" if b["batas_setor_hari_libur"] else "", b["status_batas"].upper()) if x]
    return "{} {}{}".format("s.d." if tingkat >= 3 else "paling lambat", format_tgl_tabel(tk),
                            " ({})".format("; ".join(tanda)) if tanda else "")


def _teks_pph22_chat(p22, setor, lebih, batas, tingkat):
    """'Dipungut marketplace X; kurang/lebih/lunas ...' (tingkat >= 2: lebih pendek). Hanya karakter yang ada di
    cp1252 agar keluaran tidak gagal saat dibaca agent lewat pipa di Windows."""
    if tingkat >= 2:
        awal = "PPh 22 {}".format(format_rp(p22, True))
        if setor > 0:
            return "{}; kurang {}, setor {}.".format(awal, format_rp(setor), batas)
        if lebih > 0:
            return "{}; lebih {} (bisa diminta kembali).".format(awal, format_rp(lebih))
        return "{}; lunas.".format(awal)
    awal = "Dipungut marketplace {}".format(format_rp(p22, True))
    if setor > 0:
        return "{}; kurang {}, setor sendiri {}.".format(awal, format_rp(setor), batas)
    if lebih > 0:
        return "{}; lebih {} (bisa diminta kembali), tidak perlu setor.".format(awal, format_rp(lebih))
    return "{}; lunas.".format(awal)


def _keterangan_bulan_chat(b, jenis, tingkat=0):
    """Kalimat keterangan tiap bulan: kena pajak, 4,8 miliar, PPh 22 (kurang/lebih), batas setor & status."""
    bag = []
    sebelum = b["omzet_kumulatif"] - b["omzet"]
    if jenis == "op" and sebelum <= BATAS_BEBAS_OP < b["omzet_kumulatif"]:
        bag.append("Melewati Rp500 juta; yang kena pajak hanya {}.".format(format_rp(b["omzet_kena_pajak"], True)))
    elif jenis == "op" and b["omzet_kumulatif"] <= BATAS_BEBAS_OP:
        bag.append("Masih dalam Rp500 juta bebas.")
    if sebelum <= BATAS_OMZET_UMKM < b["omzet_kumulatif"]:
        bag.append("Omzet setahun melewati Rp4,8 miliar.")
    setor, lebih, p22 = b["setor_sendiri"], b["lebih_dipungut"], b["pph22_dipungut"]
    batas = _batas_chat(b, tingkat) if setor > 0 else ""
    if p22 > 0:
        bag.append(_teks_pph22_chat(p22, setor, lebih, batas, tingkat))
    elif setor > 0:
        bag.append("Setor {}.".format(batas))
    elif not bag:
        bag.append("Tidak ada setoran.")
    return " ".join(bag)


def _baris_kelompok_chat(jk, grup, tingkat):
    """Bulan yang digabung: jumlah per bulan (PPh 22 / lebih dipungut) tetap disebut untuk tiap masa."""
    jumlah = lambda k: sum((b[k] for b in grup), Decimal(0))  # noqa: E731
    kepala = _baris_bulan_chat(rentang_bulan(grup), jumlah("omzet"), jumlah("pph_final"), tingkat)
    pendek = lambda b: NAMA_BULAN_PENDEK[b["bulan"] - 1]  # noqa: E731
    if jk == "bebas":
        ket = "Total {} bulan; masih dalam Rp500 juta bebas.".format(len(grup))
        dgn = [b for b in grup if b["pph22_dipungut"] > 0]
        if not dgn:
            ket += " Tidak ada setoran."
        elif any(b["lebih_dipungut"] > 0 for b in dgn):
            ket += " PPh 22 dipungut marketplace = lebih dipungut (bisa diminta kembali): {}; total {}.".format(
                ", ".join("{} {}".format(pendek(b), format_rp(b["lebih_dipungut"])) for b in dgn
                          if b["lebih_dipungut"] > 0), format_rp(jumlah("lebih_dipungut")))
        else:
            ket += " PPh 22 dipungut {}; lunas.".format(format_rp(jumlah("pph22_dipungut"), True))
    else:
        ket = "Total {} bulan; lunas lewat PPh 22 marketplace: {}.".format(
            len(grup), ", ".join("{} {}".format(pendek(b), format_rp(b["pph22_dipungut"], True)) for b in grup))
    return [kepala, ket]


def teks_chat(h, jenis_badan):
    """Blok siap salin untuk chat: <= BATAS_CHAT karakter (makin panjang data, makin ringkas). Bila tingkat paling
    ringkas pun masih terlalu panjang, blok dibagi dua dengan baris PENANDA_PESAN (tiap bagian <= BATAS_CHAT)."""
    for tingkat in range(TINGKAT_RINGKAS_MAKS + 1):
        teks = _teks_chat(h, jenis_badan, tingkat)
        if len(teks) <= BATAS_CHAT:
            return teks
    for tingkat in range(TINGKAT_RINGKAS_MAKS + 1):
        teks = _teks_chat(h, jenis_badan, tingkat, bagi=True)
        if all(len(x.strip("\n")) <= BATAS_CHAT for x in teks.split(PENANDA_PESAN)):
            return teks
    return teks


def _teks_chat(h, jenis_badan, tingkat, bagi=False):
    r = h["ringkasan"]
    jenis = h["jenis_wp"]
    label = "Orang pribadi" if jenis == "op" else "Badan" + (
        " - {}".format(LABEL_BADAN[jenis_badan]) if jenis_badan else "")
    out = ["**PPh Final UMKM 0,5% · {} · {}**".format(h["tahun"], label)]
    if h["hari_ini_teks"]:
        out.append("Hari ini (tanggal acuan hitungan): {}".format(h["hari_ini_teks"]))
    if h["omzet_sebelumnya"]:
        out.append("Omzet {} sebelum {}: {}".format(h["tahun"], h["bulan"][0]["nama_bulan"],
                                                   format_rp(h["omzet_sebelumnya"], True)))
    out.append("")
    out.append("**Per bulan**")
    for jk, grup in _kelompok_chat(h["bulan"], jenis, tingkat):
        if jk and len(grup) > 1:
            out.extend(_baris_kelompok_chat(jk, grup, tingkat))
            continue
        b = grup[0]
        out.append(_baris_bulan_chat(b["nama_bulan"] + (" (proyeksi)" if b["proyeksi"] else ""), b["omzet"],
                                     b["pph_final"], tingkat))
        out.append(_keterangan_bulan_chat(b, jenis, tingkat))
    out.append("")
    if bagi:
        out.append(PENANDA_PESAN)
        out.append("")
    out.append("**Ringkasan**")
    out.append("- Omzet kumulatif {}{}: {}".format(h["tahun"], " (termasuk proyeksi)" if r["ada_proyeksi"] else "",
                                                  format_rp(r["omzet_kumulatif_tahun"], True)))
    if r["ada_proyeksi"]:
        if r["rentang_data_nyata"] != "-":
            out.append("- PPh final data nyata ({}): {}".format(r["rentang_data_nyata"],
                                                               format_rp(r["total_pph_final_data_nyata"])))
        out.append("- PPh termasuk proyeksi ({}): {}".format(r["rentang_semua"], format_rp(r["total_pph_final"])))
    else:
        out.append("- Total PPh final {}: {}".format(r["rentang_semua"], format_rp(r["total_pph_final"])))
    if h["mode_pph22"]:
        out.append("- Dipungut marketplace: {}".format(format_rp(r["total_pph22_dipungut"], True)))
        out.append("- Kurang setor (setor sendiri){}: {}".format(" data nyata" if r["ada_proyeksi"] else "",
                                                                format_rp(r["total_setor_sendiri_data_nyata"])))
        if r["total_lebih_dipungut"]:
            out.append("- Lebih dipungut (bisa diminta kembali): {}".format(format_rp(r["total_lebih_dipungut"])))
    t = r["batas_setor_terdekat"]
    if t:
        out.append("- Setor terdekat: {} (masa {})".format(format_rp(t["setor_sendiri"]), t["bulan"]))
        out.append("- Paling lambat: {} ({})".format(format_tgl_tabel(datetime.date.fromisoformat(t["tanggal"])),
                                                     t["jarak"]))
    if jenis == "op":
        if r["sisa_omzet_bebas_pajak"] > 0:
            out.append("- Sisa omzet bebas pajak: {}".format(format_rp(r["sisa_omzet_bebas_pajak"], True)))
        elif r["bulan_mulai_kena_pajak"]:
            out.append("- Batas Rp500 juta bebas terlewati: {}".format(r["bulan_mulai_kena_pajak"]))
        else:
            out.append("- Tepat Rp500 juta: omzet berikutnya kena 0,5%")
    out.append("- Sisa sebelum batas Rp4,8 miliar: {}".format(
        format_rp(max(BATAS_OMZET_UMKM - r["omzet_kumulatif_tahun"], Decimal(0)), True)))
    out.append("")
    out.append("**Catatan penting**")
    for biasa, ringkas in h["catatan_chat"]:
        c = ringkas if tingkat >= 2 else biasa
        if c:
            out.append("- " + c)
    _kaki_chat(out, tingkat)
    return "\n".join(out)


def teks_kemungkinan_chat(h):
    nb, th = h["nama_bulan"], h["tahun"]
    out = ["**Perkiraan PPh Final UMKM 0,5% · {} {}**".format(nb, th),
           "Data belum lengkap, jadi ini kemungkinan hasilnya.",
           "Hari ini (tanggal acuan hitungan): {}".format(h["hari_ini_teks"]),
           "Omzet {} {}: {}".format(nb, th, format_rp(h["omzet"], True))]
    m22 = h["pph22_dipungut"] > 0
    if m22:
        out.append("Dipungut marketplace {}: {}".format(nb, format_rp(h["pph22_dipungut"], True)))
    out.append("")
    out.append("**Kemungkinan PPh {}**".format(nb))
    for k in h["kemungkinan"]:
        if k["pph_min"] == k["pph_max"]:
            nilai = "**{}**".format(format_rp(k["pph_min"]))
        else:
            nilai = "**{} s.d. {}** (0,5% x bagian omzet kumulatif di atas Rp500 juta)".format(
                format_rp(k["pph_min"]), format_rp(k["pph_max"]))
        out.append("- {}: {}{}".format(k["kondisi"], nilai,
                                       "; setelah PPh 22: {}".format(k.get("kurang_lebih_teks", "-")) if m22 else ""))
    out.append("")
    out.append("**Batas setor masa {} {}**".format(nb, th))
    out.append("{} ({})".format(format_tgl_tabel(datetime.date.fromisoformat(h["setor_hari_kerja"])),
                                h["jarak_batas_setor"]))
    out.append("")
    out.append("**Catatan penting**")
    for c in h["catatan"]:
        out.append("- " + c)
    _kaki_chat(out)
    return "\n".join(out)


class ParserID(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen tidak valid ({}).\nLihat bantuan: python3 pph_final.py --help\n"
                         .format(message))
        sys.exit(2)


def main(argv=None):
    p = ParserID(description="PPh Final UMKM 0,5% per bulan + pelacak omzet kumulatif setahun (v{}).".format(VERSI))
    p.add_argument("--jenis", choices=["op", "badan"], default="op",
                   help="'op' = orang pribadi (default, bebas Rp500 juta pertama); 'badan' = PT perorangan, koperasi, dll.")
    p.add_argument("--jenis-badan", choices=["pt-perorangan", "koperasi", "cv", "firma", "pt", "lainnya"],
                   help="Bentuk badan (menentukan catatan jangka waktu tarif 0,5%%).")
    p.add_argument("--tahun", type=int, default=datetime.date.today().year, help="Tahun pajak")
    p.add_argument("--omzet", nargs="+", help="Omzet per bulan berurutan, mis. 45jt 60jt 'Rp 80.000.000'")
    p.add_argument("--bulan-awal", default="1", help="Bulan untuk nilai --omzet pertama (default 1 = Januari)")
    p.add_argument("--pph22", nargs="+",
                   help="PPh 22 yang sudah dipungut marketplace per bulan (urutan sama dengan --omzet); dikreditkan")
    p.add_argument("--file", help="CSV (kolom bulan;omzet;pph22) atau JSON sebagai ganti --omzet")
    p.add_argument("--omzet-sebelumnya", default="0",
                   help="Omzet kumulatif tahun ini SEBELUM bulan pertama data (default 0)")
    p.add_argument("--proyeksi-mulai",
                   help="Bulan pertama yang berisi omzet PERKIRAAN (mis. 10 = Oktober dst.); subtotal data nyata dipisah")
    p.add_argument("--marketplace", action="store_true",
                   help="Pengguna berjualan di marketplace (untuk pengingat surat pernyataan omzet > Rp500 juta)")
    p.add_argument("--kemungkinan", action="store_true",
                   help="Data belum lengkap: satu bulan omzet, jenis WP & omzet sebelumnya belum diketahui")
    p.add_argument("--tahun-terdaftar", type=int,
                   help="Tahun NPWP terdaftar (dipakai untuk koperasi, CV, firma, PT; OP & PT perorangan tanpa batas)")
    p.add_argument("--hari-ini", help="Tanggal acuan (YYYY-MM-DD, default tanggal komputer)")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    p.add_argument("--tampilan", choices=["chat", "tabel"], default="chat",
                   help="Untuk --format teks: 'chat' (bawaan) = blok siap salin untuk Telegram/WhatsApp tanpa tabel; "
                        "'tabel' = tabel Markdown lebar untuk terminal/file")
    a = p.parse_args(argv)

    try:
        if a.jenis == "op" and a.jenis_badan:
            raise ValueError("--jenis-badan hanya untuk --jenis badan")
        if not 2000 <= a.tahun <= 2100:
            raise ValueError("tahun {} tidak masuk akal".format(a.tahun))
        if a.tahun_terdaftar is not None and not 1980 <= a.tahun_terdaftar <= a.tahun:
            raise ValueError("--tahun-terdaftar {} tidak masuk akal (harus 1980 s.d. tahun pajak {})".format(
                a.tahun_terdaftar, a.tahun))
        if a.file and a.omzet:
            raise ValueError("pakai salah satu: --omzet atau --file")
        try:
            hari_ini = (datetime.datetime.strptime(a.hari_ini.strip(), "%Y-%m-%d").date() if a.hari_ini
                        else datetime.date.today())
        except ValueError:
            raise ValueError("--hari-ini '{}' tidak valid (pakai format 2026-10-14)".format(a.hari_ini))
        if a.file:
            data = baca_file(a.file)
        elif a.omzet:
            awal = parse_bulan(a.bulan_awal)
            if awal + len(a.omzet) - 1 > 12:
                raise ValueError("{} nilai omzet mulai {} melewati Desember".format(len(a.omzet), NAMA_BULAN[awal - 1]))
            pph22 = a.pph22 or []
            if len(pph22) > len(a.omzet):
                raise ValueError("jumlah nilai --pph22 lebih banyak dari --omzet")
            data = []
            for i, o in enumerate(a.omzet):
                b = awal + i
                data.append((b, parse_angka(o, "omzet " + NAMA_BULAN[b - 1]),
                             parse_angka(pph22[i], "pph22 " + NAMA_BULAN[b - 1]) if i < len(pph22) else Decimal(0)))
        else:
            raise ValueError("isi omzet dengan --omzet atau --file")
        if a.kemungkinan:
            if len(data) != 1:
                raise ValueError("--kemungkinan hanya untuk SATU bulan omzet")
            b, o, p22 = data[0]
            hasil = hitung_kemungkinan(b, o, a.tahun, hari_ini, p22)
        else:
            proyeksi = parse_bulan(a.proyeksi_mulai) if a.proyeksi_mulai else None
            hasil = hitung(data, a.jenis, a.tahun, parse_angka(a.omzet_sebelumnya, "omzet sebelumnya"), hari_ini,
                           proyeksi, a.marketplace)
    except ValueError as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        return 2

    hasil["dasar_aturan"] = DASAR_ATURAN
    hasil["berlaku_per"] = TANGGAL_ATURAN
    hasil["disclaimer"] = ("Alat bantu hitung, bukan nasihat pajak. Konfirmasi ke DJP (Kring Pajak 1500200) "
                           "atau konsultan pajak.")
    if a.kemungkinan:
        hasil["catatan"] += CATATAN_TETAP[:2]
        if a.format == "json":
            print(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2))
        else:
            print(teks_kemungkinan_chat(hasil) if a.tampilan == "chat" else teks_kemungkinan(hasil))
        return 0
    hasil["catatan"] = (catatan_jenis(a.jenis)
                        + [catatan_jangka_waktu(a.jenis, a.jenis_badan, a.tahun, a.tahun_terdaftar)]
                        + hasil["catatan"] + CATATAN_TETAP)
    # (teks biasa, teks ringkas): teks ringkas dipakai bila blok chat terlalu panjang (None = tidak ditampilkan).
    hasil["catatan_chat"] = (catatan_jenis_chat(a.jenis)
                             + [(catatan_jangka_waktu_chat(a.jenis, a.jenis_badan, a.tahun, a.tahun_terdaftar),
                                 catatan_jangka_waktu_chat(a.jenis, a.jenis_badan, a.tahun, a.tahun_terdaftar, True))]
                             + hasil.pop("_catatan_chat") + CATATAN_TETAP_CHAT)
    hasil["tahun_terdaftar"] = a.tahun_terdaftar
    if a.format == "json":
        hasil["jenis_badan"] = a.jenis_badan
        del hasil["catatan_chat"]  # JSON tetap sama dengan versi sebelumnya
        print(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2))
    elif a.tampilan == "chat":
        print(teks_chat(hasil, a.jenis_badan))
    else:
        print(teks_markdown(hasil, a.jenis_badan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
