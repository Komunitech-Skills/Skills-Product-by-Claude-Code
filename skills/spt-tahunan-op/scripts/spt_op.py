#!/usr/bin/env python3
"""Kalkulator SPT Tahunan PPh Orang Pribadi (Indonesia) — penghasilan non-final, tarif Pasal 17 UU HPP.

Menghitung: penghasilan neto (pekerjaan, usaha/pekerjaan bebas dengan NPPN atau pembukuan, lain-lain)
− zakat → PTKP → PKP (dibulatkan ke bawah ribuan) → PPh terutang Pasal 17 → kredit pajak →
kurang bayar / lebih bayar / nihil, plus perkiraan angsuran PPh 25, batas lapor, dan checklist dokumen.

Contoh:
  python3 spt_op.py --status TK/0 --a1 114jt 3jt
  python3 spt_op.py --status K/1 --a1 90jt 1.350.000 --a1 60jt 0
  python3 spt_op.py --status TK/1 --nppn 240jt 50 --nppn-diberitahukan ya --pph21-lain 2,4jt
  python3 spt_op.py --status K/2 --a1 120jt 2.625.000 --nppn 300jt 32 --nppn-diberitahukan ya \\
      --zakat 5jt --pph25 6jt
  python3 spt_op.py --status TK/0 --a1 114jt 3jt --omzet-final 600jt --pph-final 500rb --format json

Angka format Indonesia: titik = ribuan, koma = desimal (1.250.000,50), akhiran rb/ribu/k, jt/juta,
miliar/milyar. Angka yang ambigu (1,500 · 2.5jt · 1,250,000 · 5m) DITOLAK. "5,054 miliar" diterima (= 5.054.000.000).

Hanya library standar Python 3.8+. Tanpa akses jaringan. Keluar kode 2 bila input salah.
Tidak mengisi atau mengirim SPT ke DJP — hanya menghitung.
"""
import argparse
import datetime
import json
import re
import sys
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP

VERSI = "1.0.7"

# ------------------------------------------------------------------ konstanta aturan
PTKP_DIRI = Decimal(54000000)        # UU 7/2021 HPP Pasal 7 ayat (1); PMK 101/2016
PTKP_KAWIN = Decimal(4500000)
PTKP_ISTRI_GABUNG = Decimal(54000000)
PTKP_TANGGUNGAN = Decimal(4500000)   # per orang, maks 3
MAKS_TANGGUNGAN = 3

# Lapisan tarif Pasal 17 ayat (1) huruf a UU PPh s.t.d.t.d. UU 7/2021 HPP (sejak TP 2022)
LAPISAN = [
    (Decimal(60000000), Decimal("0.05")),
    (Decimal(250000000), Decimal("0.15")),
    (Decimal(500000000), Decimal("0.25")),
    (Decimal(5000000000), Decimal("0.30")),
    (None, Decimal("0.35")),
]

BATAS_NPPN = Decimal(4800000000)     # peredaran bruto < Rp4,8 M setahun
BIAYA_JABATAN_PERSEN = Decimal("0.05")
BIAYA_JABATAN_MAKS_BULAN = Decimal(500000)
BATAS_LB_PENDAHULUAN_USAHA = Decimal(100000000)
DENDA_TELAT_LAPOR = Decimal(100000)  # UU KUP Pasal 7 ayat (1)

DASAR_ATURAN = ("UU PPh s.t.d.t.d. UU 7/2021 (HPP) Pasal 7 & 17; PMK 101/PMK.010/2016 (PTKP); PMK 168/2023 "
                "(biaya jabatan, pembulatan PKP); PER-17/PJ/2015 & PMK 81/2024 (NPPN); PP 55/2022 jo. PP 20/2026 "
                "(PPh final UMKM); PP 60/2010 (zakat); PER-11/PJ/2025 (bentuk SPT Coretax); UU KUP Pasal 3 & 7; "
                "KEP-55/PJ/2026 (penghapusan sanksi TP 2025)")
DISCLAIMER = ("Alat bantu hitung, bukan konsultan pajak dan bukan nasihat pajak. Dasar: " + DASAR_ATURAN +
              "; dicek per 30 September 2026. Pembulatan belum dicocokkan dengan hitungan otomatis Coretax. "
              "Skill ini tidak mengisi atau mengirim SPT atas nama Anda. Cocokkan dengan Coretax DJP, "
              "Kring Pajak 1500200, atau konsultan pajak terdaftar sebelum melapor.")


class InputError(Exception):
    pass


# ------------------------------------------------------------------ angka
_AKHIRAN = [
    ("miliar", 10 ** 9), ("milyar", 10 ** 9),
    ("juta", 10 ** 6), ("ribu", 10 ** 3), ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3),
]


def parse_angka(nilai, nama="angka", boleh_negatif=False):
    """Baca angka format Indonesia. Tolak (InputError) bila ambigu.

    Diterima: 15000 · 15.000 · 1.250.000,50 · 2,5jt · 500rb · 1,2 miliar · Rp 3.000.000 · 3.000.000,-
    Ditolak : 1,500 (koma + 3 digit: ribuan gaya Inggris atau desimal?) · 2.5 / 2.5jt (titik bukan
              ribuan) · 1,250,000 / 1,250.50 (format Inggris) · 1.25.000 (kelompok salah) · 5m / 5M
              (juta atau miliar?).
    """
    if nilai is None:
        raise InputError("{}: nilai kosong".format(nama))
    asli = str(nilai)
    s = asli.strip().lower().replace(" ", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    negatif = False
    if s.startswith("-"):
        negatif, s = True, s[1:]
    if re.fullmatch(r"[\d.,]+m", s):
        raise InputError("{}: '{}' ambigu (M = juta atau miliar?). Contoh yang benar: '5,054 miliar', "
                         "'5.054.000.000', atau '250jt'".format(nama, asli))
    pengali = 1
    for akh, kali in _AKHIRAN:
        if s.endswith(akh):
            s, pengali = s[: -len(akh)], kali
            break
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise InputError("{}: '{}' bukan angka yang valid".format(nama, asli))
    if s.count(",") > 1:
        raise InputError("{}: '{}' memakai koma sebagai pemisah ribuan (gaya Inggris). Tulis 1.250.000".format(
            nama, asli))
    if "," in s:
        utuh, desimal = s.split(",")
        if "." in desimal:
            raise InputError("{}: '{}' memakai format Inggris. Tulis titik untuk ribuan, koma untuk desimal, "
                             "mis. 1.250.000,50".format(nama, asli))
        if not desimal:
            raise InputError("{}: '{}' tidak lengkap setelah koma".format(nama, asli))
        if len(desimal) == 3 and "." not in utuh and pengali != 10 ** 9:
            if pengali > 1:
                raise InputError("{}: '{}' ambigu (koma + 3 angka sebelum satuan). Contoh yang benar: 1,5jt "
                                 "(satu setengah juta) atau 1.500jt (seribu lima ratus juta)".format(nama, asli))
            raise InputError("{}: '{}' ambigu (1,500 = seribu lima ratus atau satu koma lima?). Tulis 1.500 "
                             "untuk ribuan atau 1,5 untuk desimal".format(nama, asli))
    else:
        utuh, desimal = s, ""
    if "." in utuh:
        grup = utuh.split(".")
        if not (1 <= len(grup[0]) <= 3 and grup[0] != "0" and all(len(g) == 3 for g in grup[1:])):
            raise InputError("{}: '{}' ambigu/tidak valid: titik hanya untuk pemisah ribuan (1.250.000); "
                             "pakai koma untuk desimal (2,5jt)".format(nama, asli))
        utuh = utuh.replace(".", "")
    if not utuh:
        raise InputError("{}: '{}' bukan angka yang valid".format(nama, asli))
    d = Decimal(utuh + ("." + desimal if desimal else "")) * pengali
    if negatif:
        d = -d
    if d < 0 and not boleh_negatif:
        raise InputError(pesan_negatif(nama, asli))
    return d


def pesan_negatif(nama, asli):
    """Pesan ramah untuk angka negatif; saran rugi usaha hanya untuk angka penghasilan."""
    pesan = "{}: angka tidak boleh negatif ({}). Isi dengan angka positif, mis. 5jt atau 5.000.000".format(nama, asli)
    if any(k in nama for k in ("neto", "bruto", "omzet")):
        pesan += ". Bila maksudnya rugi usaha: kompensasi kerugian di luar cakupan skill ini — konsultasikan ke " \
                 "konsultan pajak"
    return pesan


def cek_negatif_argv(argv):
    """argparse menganggap '-10jt' sebagai nama opsi. Tangkap lebih dulu agar pesannya ramah."""
    for i, tok in enumerate(argv):
        if re.match(r"^-\s*(rp\.?\s*)?\d", str(tok), re.IGNORECASE):
            opsi = next((argv[j] for j in range(i - 1, -1, -1) if str(argv[j]).startswith("--")), "angka")
            raise InputError(pesan_negatif(opsi, tok))


def parse_persen(nilai, nama):
    s = str(nilai).strip().rstrip("%").strip()
    p = parse_angka(s, nama)
    if not (Decimal(0) < p <= Decimal(100)):
        raise InputError("{}: persen norma harus di atas 0 dan paling tinggi 100 (sekarang {})".format(nama, nilai))
    return p


def bulat_bawah(d, satuan=1):
    satuan = Decimal(satuan)
    return (Decimal(d) / satuan).quantize(Decimal(1), ROUND_FLOOR) * satuan


def bulat_terdekat(d):
    return Decimal(d).quantize(Decimal(1), ROUND_HALF_UP)


def format_rp(d):
    d = Decimal(d)
    neg = d < 0
    d = abs(d)
    if d == d.to_integral_value():
        teks = "{:,}".format(int(d)).replace(",", ".")
    else:
        q = d.quantize(Decimal("0.01"), ROUND_HALF_UP)
        utuh, des = str(q).split(".")
        teks = "{:,}".format(int(utuh)).replace(",", ".") + "," + des
    return ("-Rp " if neg else "Rp ") + teks


def format_persen(p):
    s = str(Decimal(p).normalize())
    if "E" in s:
        s = "{:f}".format(Decimal(p))
    return s.replace(".", ",") + "%"


# ------------------------------------------------------------------ PTKP & tarif
def parse_status(teks):
    s = str(teks or "").strip().upper().replace(" ", "").replace("-", "/")
    m = re.fullmatch(r"(TK|K|K/I)/?(\d+)", s)
    if not m:
        raise InputError("Status '{}' tidak dikenali. Contoh: TK/0, TK/2, K/0, K/3, K/I/1 "
                         "(K/I = penghasilan istri digabung dengan suami)".format(teks))
    jenis, n = m.group(1), int(m.group(2))
    if n > MAKS_TANGGUNGAN:
        raise InputError("Status '{}': tanggungan paling banyak 3 orang untuk PTKP. Pakai {}/3".format(teks, jenis))
    return jenis, n


def hitung_ptkp(jenis, n):
    rincian = [("Wajib pajak sendiri", PTKP_DIRI)]
    if jenis in ("K", "K/I"):
        rincian.append(("Status kawin", PTKP_KAWIN))
    if jenis == "K/I":
        rincian.append(("Istri yang penghasilannya digabung", PTKP_ISTRI_GABUNG))
    if n:
        rincian.append(("Tanggungan {} orang × {}".format(n, format_rp(PTKP_TANGGUNGAN)), PTKP_TANGGUNGAN * n))
    return sum((r[1] for r in rincian), Decimal(0)), rincian


def pph_pasal17(pkp):
    """Kembalikan (total, rincian lapisan) untuk PKP (sudah dibulatkan)."""
    sisa, bawah, total, rincian = Decimal(pkp), Decimal(0), Decimal(0), []
    for atas, tarif in LAPISAN:
        if sisa <= 0:
            break
        lebar = sisa if atas is None else min(sisa, atas - bawah)
        pajak = lebar * tarif
        rincian.append({"lapisan_dari": bawah, "lapisan_sampai": atas, "dasar": lebar,
                        "tarif_persen": tarif * 100, "pajak": pajak})
        total += pajak
        sisa -= lebar
        if atas is not None:
            bawah = atas
    return bulat_bawah(total), rincian


# ------------------------------------------------------------------ tenggat NPPN tahun berjalan
def status_nppn_tahun_berjalan(hari_ini):
    """Bandingkan batas pemberitahuan NPPN TAHUN BERJALAN (31 Maret) dengan tanggal acuan.

    Dasar: UU PPh Ps. 14 ayat (2) & (5); PMK 81/2024 Ps. 450 ayat (2) — pemberitahuan dalam 3 bulan pertama
    tahun pajak; tanpa pemberitahuan dianggap memilih pembukuan. Penguncian pembukuan: PMK 81/2024 Ps. 463
    s.t.d.d. PMK 1/2026 (menurut DJP) — PERLU REVIEW konsultan pajak.
    """
    tp = hari_ini.year
    batas = datetime.date(tp, 3, 31)
    lewat = hari_ini > batas
    if not lewat:
        pesan = ("Pemberitahuan NPPN untuk tahun pajak {tp}: batas 31 Maret {tp} BELUM lewat per {h} (sisa {n} hari). "
                 "Bila ingin memakai NPPN tahun {tp} dan belum memberitahukan, sampaikan lewat Coretax (layanan "
                 "AS.04-01) sebelum tanggal itu.").format(tp=tp, h=hari_ini.isoformat(), n=(batas - hari_ini).days)
    else:
        pesan = ("Pemberitahuan NPPN untuk tahun pajak {tp}: batas 31 Maret {tp} SUDAH LEWAT per {h} — JANGAN "
                 "menyarankan mengirimnya lagi untuk tahun {tp}. Bila belum disampaikan, untuk tahun pajak {tp} Anda "
                 "dianggap memilih PEMBUKUAN (UU PPh Ps. 14 ayat (5); PMK 81/2024 Ps. 450): mulai catat pembukuan "
                 "(pemasukan, biaya, laba-rugi) sekarang. Pemberitahuan berikutnya hanya bisa untuk tahun pajak {tp1} "
                 "(1 Januari–31 Maret {tp1}), TETAPI menurut DJP wajib pajak yang sudah menyelenggarakan pembukuan "
                 "tidak dapat kembali ke NPPN (PMK 81/2024 Ps. 463 s.t.d.d. PMK 1/2026) — pastikan ke KPP/konsultan "
                 "pajak apakah status 'dianggap pembukuan' ikut mengunci sebelum mengandalkan NPPN {tp1}.").format(
                     tp=tp, tp1=tp + 1, h=hari_ini.isoformat())
    return {"tahun_pajak": tp, "batas": batas.isoformat(), "sudah_lewat": lewat, "pesan": pesan}


# ------------------------------------------------------------------ status tenggat lapor SPT Tahunan
DASAR_DENDA = ("UU KUP Pasal 7 ayat (1) (UU 6/1983 s.t.d.t.d. UU 7/2021 tentang HPP; nominal Rp100.000 untuk "
               "SPT Tahunan PPh Orang Pribadi berlaku sejak 1 Januari 2008, tidak diubah UU HPP)")
DASAR_BUNGA = ("UU KUP Pasal 9 ayat (2b) jo. ayat (2a)–(2c) s.t.d.t.d. UU 7/2021 tentang HPP (berlaku sejak "
               "29 Oktober 2021): bunga per bulan = (suku bunga acuan + 5%) ÷ 12 yang ditetapkan Menteri Keuangan "
               "lewat KMK tarif bunga yang BERUBAH TIAP BULAN; dihitung sejak jatuh tempo sampai tanggal bayar, "
               "bagian bulan dihitung 1 bulan penuh, paling lama 24 bulan")
CEK_TARIF_BUNGA = ("Cek tarif bunga bulan berjalan di KMK tarif bunga terbaru: fiskal.kemenkeu.go.id (menu tarif "
                   "bunga) atau pajak.go.id, atau tanyakan Kring Pajak 1500200. Tarif TIDAK dikarang di sini.")


def tambah_bulan(tgl, n):
    """Tambah n bulan; tanggal dijepit ke akhir bulan (31 Mar + 1 bulan = 30 Apr)."""
    m = tgl.month - 1 + n
    th, bl = tgl.year + m // 12, m % 12 + 1
    akhir = (datetime.date(th + (bl == 12), bl % 12 + 1, 1) - datetime.timedelta(days=1)).day
    return datetime.date(th, bl, min(tgl.day, akhir))


def bulan_terlambat(batas, hari_ini):
    """Jumlah bulan keterlambatan, bagian bulan dihitung penuh (0 bila belum lewat)."""
    if hari_ini <= batas:
        return 0
    n = (hari_ini.year - batas.year) * 12 + hari_ini.month - batas.month
    n = max(n, 1)
    while tambah_bulan(batas, n) < hari_ini:
        n += 1
    while n > 1 and tambah_bulan(batas, n - 1) >= hari_ini:
        n -= 1
    return n


def status_tenggat(tahun, hari_ini, batas, batas_bebas_sanksi, status_spt):
    """Status tenggat lapor SPT Tahunan OP per tanggal acuan + konsekuensi umum (tanpa menghitung bunga)."""
    kb = status_spt == "KURANG BAYAR"
    d = {"tanggal_acuan": hari_ini.isoformat(), "batas_lapor": batas.isoformat(), "kode": None,
         "sisa_hari": None, "hari_terlambat": 0, "bulan_terlambat": 0, "konsekuensi": [], "saran": "", "ringkas": ""}
    if hari_ini <= batas:
        sisa = (batas - hari_ini).days
        d.update(kode="BELUM_LEWAT", sisa_hari=sisa)
        d["ringkas"] = ("BELUM LEWAT — per {} batas lapor {} masih {} hari lagi{}.".format(
            hari_ini.isoformat(), batas.isoformat(), sisa, " (hari terakhir)" if sisa == 0 else ""))
        d["saran"] = ("Lapor{} sebelum {}; paling aman beberapa hari lebih awal.".format(
            " dan bayar kurang bayar" if kb else "", batas.isoformat()))
        d["konsekuensi"].append("Bila lewat {}: denda telat lapor Rp100.000 — {}.".format(batas.isoformat(),
                                                                                       DASAR_DENDA))
        if kb:
            d["konsekuensi"].append("Kurang bayar yang dibayar setelah jatuh tempo kena bunga per bulan — {}. {}".format(
                DASAR_BUNGA, CEK_TARIF_BUNGA))
        return d
    hari_telat = (hari_ini - batas).days
    bln = bulan_terlambat(batas, hari_ini)
    d.update(hari_terlambat=hari_telat, bulan_terlambat=bln)
    if batas_bebas_sanksi and hari_ini <= batas_bebas_sanksi:
        sisa = (batas_bebas_sanksi - hari_ini).days
        d.update(kode="LEWAT_MASA_BEBAS_SANKSI", sisa_hari=sisa)
        d["ringkas"] = ("JATUH TEMPO SUDAH LEWAT ({}), tetapi per {} masih dalam masa penghapusan sanksi "
                        "KEP-55/PJ/2026 s.d. {} (sisa {} hari).".format(batas.isoformat(), hari_ini.isoformat(),
                                                                        batas_bebas_sanksi.isoformat(), sisa))
        d["saran"] = "SEGERA lapor{} paling lambat {} agar denda & bunga tidak ditagih.".format(
            " dan bayar" if kb else "", batas_bebas_sanksi.isoformat())
        d["konsekuensi"].append("Lewat {}: denda Rp100.000 — {}{}.".format(
            batas_bebas_sanksi.isoformat(), DASAR_DENDA,
            "; ditambah bunga atas kurang bayar" if kb else ""))
        return d
    d["kode"] = "TERLAMBAT"
    d["ringkas"] = ("SUDAH TERLAMBAT — batas lapor {} sudah lewat {} hari per {} (± {} bulan; bagian bulan dihitung "
                    "penuh){}.".format(batas.isoformat(), hari_telat, hari_ini.isoformat(), bln,
                                       "; masa bebas sanksi KEP-55/PJ/2026 s.d. {} juga sudah berakhir".format(
                                           batas_bebas_sanksi.isoformat()) if batas_bebas_sanksi else ""))
    d["konsekuensi"].append("Denda telat lapor SPT Tahunan OP Rp100.000 (sekali per SPT, ditagih lewat STP) — {}."
                            .format(DASAR_DENDA))
    if kb:
        d["konsekuensi"].append(
            "Kurang bayar yang belum disetor: bunga per bulan × kurang bayar × jumlah bulan terlambat (saat ini "
            "± {} bulan, maks. 24) — {}. {}".format(min(bln, 24), DASAR_BUNGA, CEK_TARIF_BUNGA))
    else:
        d["konsekuensi"].append("Hasil bukan kurang bayar → tidak ada bunga telat bayar; yang berlaku denda telat "
                                "lapor saja.")
    d["konsekuensi"].append("Makin lama ditunda, bunga kurang bayar makin besar dan DJP dapat mengirim surat "
                            "teguran/STP." if kb else "Makin lama ditunda, DJP dapat mengirim surat teguran/STP.")
    d["saran"] = ("SEGERA lapor{} — jangan ditunda lagi. Bila ragu angkanya, konsultasikan singkat dulu ke Kring "
                  "Pajak 1500200/KPP/konsultan pajak, lalu lapor secepatnya.".format(
                      " dan bayar kurang bayar (makin cepat bayar, bunga makin kecil)" if kb else ""))
    return d


# ------------------------------------------------------------------ hitung utama
def hitung(args, hari_ini=None):
    jenis, n = parse_status(args.status)
    hari_ini = hari_ini or datetime.date.today()
    tahun = args.tahun or (hari_ini.year - 1)
    if not 2022 <= tahun <= 2100:
        raise InputError("--tahun {} di luar cakupan (tarif UU HPP berlaku sejak tahun pajak 2022)".format(tahun))

    catatan, peringatan = [], []
    if hari_ini.year <= tahun:
        peringatan.append("Tahun pajak {} belum berakhir per {}: hasil ini PERKIRAAN. Hitung ulang setelah semua "
                          "bukti potong tahun {} diterima (biasanya Januari–Februari {}).".format(
                              tahun, hari_ini.isoformat(), tahun, tahun + 1))

    # --- pekerjaan (bukti potong A1/A2)
    pekerjaan = []
    for i, (neto, pph) in enumerate(args.a1 or [], start=1):
        pekerjaan.append({"sumber": "Bukti potong #{} (neto dari bukti potong)".format(i),
                          "neto": parse_angka(neto, "--a1 #{} neto".format(i)),
                          "pph21": parse_angka(pph, "--a1 #{} PPh 21".format(i))})
    for i, vals in enumerate(args.a1_bruto or [], start=1):
        if not 2 <= len(vals) <= 4:
            raise InputError("--a1-bruto butuh 2–4 nilai: BRUTO PPH21 [BULAN_BEKERJA=12] [IURAN_PENSIUN_PEGAWAI=0]")
        bruto = parse_angka(vals[0], "--a1-bruto #{} bruto".format(i))
        pph = parse_angka(vals[1], "--a1-bruto #{} PPh 21".format(i))
        bulan = 12
        if len(vals) >= 3:
            if not re.fullmatch(r"\d{1,2}", vals[2]) or not 1 <= int(vals[2]) <= 12:
                raise InputError("--a1-bruto #{}: bulan bekerja harus 1–12 (sekarang '{}')".format(i, vals[2]))
            bulan = int(vals[2])
        iuran = parse_angka(vals[3], "--a1-bruto #{} iuran".format(i)) if len(vals) == 4 else Decimal(0)
        bj = min(bulat_terdekat(bruto * BIAYA_JABATAN_PERSEN), BIAYA_JABATAN_MAKS_BULAN * bulan)
        neto = bruto - bj - iuran
        if neto < 0:
            raise InputError("--a1-bruto #{}: neto negatif — periksa bruto & iuran".format(i))
        pekerjaan.append({"sumber": "Bukti potong #{} (dihitung dari bruto {} − biaya jabatan {} − iuran {})".format(
            len(args.a1 or []) + i, format_rp(bruto), format_rp(bj), format_rp(iuran)),
            "neto": neto, "pph21": pph})
        catatan.append("Neto bukti potong #{} dihitung dari bruto. Bila bukti potong A1/A2 mencantumkan angka "
                       "'penghasilan neto', pakai angka itu (--a1) — lebih tepat.".format(len(args.a1 or []) + i))
    if len(pekerjaan) >= 2:
        catatan.append("Punya {} bukti potong pekerjaan: tiap pemberi kerja sudah memakai PTKP penuh, jadi saat "
                       "digabung di SPT hampir selalu KURANG BAYAR. Ini normal, bukan kesalahan.".format(
                           len(pekerjaan)))

    # --- usaha / pekerjaan bebas
    usaha = []
    bruto_nppn = Decimal(0)
    for i, (bruto, persen) in enumerate(args.nppn or [], start=1):
        b = parse_angka(bruto, "--nppn #{} bruto".format(i))
        p = parse_persen(persen, "--nppn #{} persen".format(i))
        bruto_nppn += b
        usaha.append({"sumber": "Usaha/pekerjaan bebas #{} — NPPN {} × {}".format(i, format_persen(p), format_rp(b)),
                      "bruto": b, "persen_norma": p, "neto": bulat_terdekat(b * p / 100), "metode": "NPPN"})
    for i, neto in enumerate(args.pembukuan_neto or [], start=1):
        usaha.append({"sumber": "Usaha/pekerjaan bebas (pembukuan) #{}".format(i), "bruto": None,
                      "persen_norma": None, "neto": parse_angka(neto, "--pembukuan-neto #{}".format(i)),
                      "metode": "pembukuan"})

    omzet_final = parse_angka(args.omzet_final, "--omzet-final") if args.omzet_final else Decimal(0)
    pph_final = parse_angka(args.pph_final, "--pph-final") if args.pph_final else Decimal(0)
    if pph_final and not omzet_final:
        raise InputError("--pph-final diisi tanpa --omzet-final. Isi omzet setahun yang kena PPh final 0,5%")
    final_salah = (parse_angka(args.final_salah_skema, "--final-salah-skema")
                   if args.final_salah_skema else Decimal(0))
    if final_salah and not usaha:
        raise InputError("--final-salah-skema diisi tanpa penghasilan pekerjaan bebas. Hitung dulu penghasilan "
                         "pekerjaan bebas itu dengan --nppn BRUTO PERSEN atau --pembukuan-neto NETO")

    if args.nppn:
        total_bruto_usaha = bruto_nppn + omzet_final
        if total_bruto_usaha >= BATAS_NPPN:
            raise InputError("Peredaran bruto usaha/pekerjaan bebas {} ≥ Rp4,8 miliar: NPPN tidak boleh dipakai. "
                             "Wajib pembukuan — pakai --pembukuan-neto dan konsultasikan ke konsultan pajak".format(
                                 format_rp(total_bruto_usaha)))
        if args.nppn_diberitahukan == "tidak":
            peringatan.append("Anda memakai NPPN tetapi BELUM memberitahukan DJP dalam 3 bulan pertama tahun pajak "
                              "{}. Menurut DJP, tanpa pemberitahuan Anda dianggap memilih PEMBUKUAN, sehingga neto "
                              "harus dari pembukuan (hasil NPPN di bawah hanya simulasi). Konsultasikan segera."
                              .format(tahun))
        elif args.nppn_diberitahukan is None:
            peringatan.append("Pastikan pemberitahuan penggunaan NPPN sudah disampaikan ke DJP paling lambat 31 Maret "
                              "{} (Coretax, layanan AS.04-01). Tanpa itu, Anda dianggap wajib pembukuan.".format(tahun))
        catatan.append("Persen norma NPPN wajib dicocokkan dengan lampiran PER-17/PJ/2015 sesuai KLU dan wilayah "
                       "(10 ibu kota provinsi / ibu kota provinsi lain / daerah lain).")

    lain = parse_angka(args.lain_neto, "--lain-neto") if args.lain_neto else Decimal(0)
    zakat = parse_angka(args.zakat, "--zakat") if args.zakat else Decimal(0)

    if not pekerjaan and not usaha and not lain:
        if omzet_final:
            catatan.append("Hanya ada penghasilan final PP 55: tidak ada PPh Pasal 17. SPT tetap wajib dilapor "
                           "(omzet, PPh final disetor, harta & utang).")
        else:
            raise InputError("Tidak ada penghasilan yang diisi. Isi minimal satu: --a1, --a1-bruto, --nppn, "
                             "--pembukuan-neto, --lain-neto, atau --omzet-final")

    neto_kerja = sum((p["neto"] for p in pekerjaan), Decimal(0))
    neto_usaha = sum((u["neto"] for u in usaha), Decimal(0))
    neto_bruto_total = neto_kerja + neto_usaha + lain
    zakat_dipakai = min(zakat, neto_bruto_total)
    if zakat > neto_bruto_total:
        peringatan.append("Zakat {} lebih besar dari total penghasilan neto {}; yang bisa dikurangkan hanya {}.".format(
            format_rp(zakat), format_rp(neto_bruto_total), format_rp(zakat_dipakai)))
    if zakat:
        catatan.append("Zakat hanya boleh dikurangkan bila dibayar ke BAZNAS/LAZ/lembaga yang disahkan pemerintah "
                       "dan ada bukti setor. Zakat yang sudah dipotong lewat kantor (tercantum di bukti potong A1) "
                       "JANGAN dimasukkan lagi di --zakat.")
    neto = neto_bruto_total - zakat_dipakai

    ptkp, rincian_ptkp = hitung_ptkp(jenis, n)
    pkp_mentah = max(Decimal(0), neto - ptkp)
    pkp = bulat_bawah(pkp_mentah, 1000)
    pph_terutang, lapisan = pph_pasal17(pkp)

    kredit = []
    for p in pekerjaan:
        if p["pph21"]:
            kredit.append(("PPh 21 — " + p["sumber"].split(" (")[0], p["pph21"]))
    for label, attr in (("PPh 21 bukan pegawai / lainnya (bukti potong)", "pph21_lain"),
                        ("PPh 22 dipungut", "pph22"), ("PPh 23 dipotong", "pph23"),
                        ("Angsuran PPh 25 yang sudah dibayar", "pph25")):
        v = getattr(args, attr)
        if v:
            kredit.append((label, parse_angka(v, "--" + attr.replace("_", "-"))))
    total_kredit = sum((k[1] for k in kredit), Decimal(0))
    selisih = pph_terutang - total_kredit
    if selisih > 0:
        status_spt = "KURANG BAYAR"
    elif selisih < 0:
        status_spt = "LEBIH BAYAR"
    else:
        status_spt = "NIHIL"

    # --- PPh 25 tahun berikutnya (hanya bila ada usaha/pekerjaan bebas non-final)
    pph25_berikut = None
    if usaha:
        kredit_non25 = total_kredit - (parse_angka(args.pph25, "--pph25") if args.pph25 else Decimal(0))
        pph25_berikut = bulat_bawah(max(Decimal(0), pph_terutang - kredit_non25) / 12)
        catatan.append("Perkiraan angsuran PPh 25 tahun {} = (PPh terutang − PPh 21/22/23 yang dipotong) ÷ 12 "
                       "(UU PPh Pasal 25 ayat (1)). Cocokkan dengan Lampiran 4 di Coretax.".format(tahun + 1))

    # --- cek kewajaran: karyawan 1 pemberi kerja seharusnya umumnya NIHIL
    cek_a1_tunggal = (len(pekerjaan) == 1 and not usaha and not lain and not zakat and jenis != "K/I"
                      and not any(getattr(args, a) for a in ("pph21_lain", "pph22", "pph23", "pph25"))
                      and status_spt != "NIHIL")
    if cek_a1_tunggal:
        peringatan.append(
            "Anda hanya punya 1 pemberi kerja, tetapi hasilnya {} {}. Biasanya kantor sudah menghitung ulang pajak "
            "setahun di gaji bulan terakhir (Desember atau bulan keluar), sehingga hasil SPT karyawan 1 kantor "
            "umumnya NIHIL. Sebelum lapor/bayar, CEK ULANG bukti potong A1 dengan HRD/bagian gaji: (1) status "
            "PTKP di A1 sama dengan status Anda per 1 Januari (mis. sudah menikah/punya anak tapi belum "
            "diperbarui di kantor); (2) angka 'penghasilan neto' dan 'PPh 21 dipotong' yang Anda masukkan sama "
            "persis dengan A1{}; (3) tidak ada A1 lain (mis. kantor lama/pembetulan). Bila A1 memang begitu, "
            "hasil ini yang dipakai; selisih kecil (beberapa rupiah) bisa karena pembulatan.".format(
                status_spt, format_rp(abs(selisih)),
                " (neto Anda dihitung dari bruto — minta angka neto di A1)" if args.a1_bruto else ""))

    # --- batas waktu: UU KUP Pasal 3 ayat (3) huruf b — paling lambat 3 bulan setelah akhir tahun pajak
    batas = datetime.date(tahun + 1, 3, 31)
    batas_bebas_sanksi = None
    if tahun == 2025:
        batas_bebas_sanksi = datetime.date(2026, 4, 30)
        ket_batas = ("31 Maret 2026 (jatuh tempo formal tetap). Khusus tahun pajak 2025: sanksi "
                     "administrasi (denda & bunga) dihapus bila lapor dan/atau bayar paling lambat 30 April 2026 "
                     "(KEP-55/PJ/2026)")
    else:
        ket_batas = ("31 Maret {} (3 bulan setelah akhir tahun pajak). Bila jatuh pada Sabtu/Minggu/hari libur, "
                     "cek pengumuman DJP terbaru — paling aman lapor sebelum tanggal itu".format(tahun + 1))
    sudah_lewat = hari_ini > batas
    bunga_kb = ("; kurang bayar yang dibayar setelah jatuh tempo juga kena bunga per bulan (UU KUP Pasal 9 s.t.d.t.d. "
                "UU HPP; tarif KMK bulanan — tidak dihitung di sini)" if status_spt == "KURANG BAYAR" else "")
    tenggat = status_tenggat(tahun, hari_ini, batas, batas_bebas_sanksi, status_spt)
    if sudah_lewat and batas_bebas_sanksi and hari_ini <= batas_bebas_sanksi:
        peringatan.append("Jatuh tempo ({}) sudah lewat per {}, tetapi masih dalam masa penghapusan sanksi "
                          "KEP-55/PJ/2026: lapor{} paling lambat {} agar denda & bunga tidak ditagih.".format(
                              batas.isoformat(), hari_ini.isoformat(),
                              " dan bayar" if status_spt == "KURANG BAYAR" else "", batas_bebas_sanksi.isoformat()))
    elif sudah_lewat:
        peringatan.append("Batas lapor ({}) SUDAH LEWAT per {}{}. SEGERA laporkan; denda telat lapor SPT "
                          "Tahunan OP Rp100.000 (UU KUP Pasal 7 ayat (1)) ditagih lewat STP{}.".format(
                              batas.isoformat(), hari_ini.isoformat(),
                              " (masa penghapusan sanksi KEP-55/PJ/2026 s.d. {} juga sudah berakhir)".format(
                                  batas_bebas_sanksi.isoformat()) if batas_bebas_sanksi else "", bunga_kb))

    if omzet_final:
        catatan.append("Omzet PPh final 0,5% ({}) TIDAK ikut dihitung tarif Pasal 17; dilaporkan di lampiran "
                       "penghasilan final / rekap peredaran bruto beserta PPh final yang sudah disetor ({}).".format(
                           format_rp(omzet_final), format_rp(pph_final)))
        catatan.append("PPh final 0,5% hanya untuk penghasilan USAHA (dagang, produksi, jasa biasa). Penghasilan "
                       "dari PEKERJAAN BEBAS (mis. dokter, pengacara, notaris, akuntan, arsitek, konsultan, "
                       "seniman/influencer, penceramah, penulis, agen/perantara) tidak boleh memakai 0,5% — hitung "
                       "dengan NPPN/pembukuan (--nppn / --pembukuan-neto). Dasar: PP 55/2022 Pasal 56 s.t.d.d. "
                       "PP 20/2026.")
        if pph_final:
            perkiraan = bulat_bawah(max(Decimal(0), omzet_final - Decimal(500000000)) * Decimal("0.005"))
            if abs(pph_final - perkiraan) > Decimal(10000):
                catatan.append("Cek kewajaran PPh final: 0,5% × (omzet {} − Rp500 juta bebas pajak) = {}, sedangkan "
                               "yang Anda isi {}. Perbedaan bisa wajar (mis. PPh dipungut marketplace/pemungut, "
                               "omzet belum tercatat per bulan), tetapi cocokkan dengan bukti setor.".format(
                                   format_rp(omzet_final), format_rp(perkiraan), format_rp(pph_final)))
        if omzet_final <= Decimal(500000000) and not pph_final:
            catatan.append("Omzet final setahun tidak lebih dari Rp500 juta: untuk orang pribadi bagian ini bebas PPh "
                           "final 0,5% (PP 55/2022 s.t.d.d. UU HPP), tetapi omzetnya tetap dilaporkan di SPT.")
        if omzet_final > BATAS_NPPN:
            peringatan.append("Omzet final di atas Rp4,8 miliar: tahun berikutnya tidak lagi memenuhi syarat PPh final "
                              "0,5% — konsultasikan ke konsultan pajak.")
    nppn_berjalan = None
    if usaha or omzet_final:
        nppn_berjalan = status_nppn_tahun_berjalan(hari_ini)
        (peringatan if nppn_berjalan["sudah_lewat"] else catatan).append(nppn_berjalan["pesan"])
    if final_salah:
        peringatan.append(
            "PPh final 0,5% {} terlanjur disetor atas penghasilan PEKERJAAN BEBAS (salah skema): TIDAK "
            "dikreditkan di hitungan ini dan JANGAN dilaporkan sebagai penghasilan final (Lampiran 2/L-3B) — "
            "penghasilannya sudah dihitung lewat NPPN/pembukuan. Uang itu bisa diminta kembali lewat permohonan "
            "pengembalian pajak yang seharusnya tidak terutang di Coretax (menu Pembayaran, formulir restitusi); "
            "pemindahbukuan umumnya TIDAK bisa karena setoran PPh final UMKM dianggap sebagai penyampaian SPT Masa "
            "(PMK 81/2024 Pasal 109 ayat (3)). Pastikan prosedurnya ke KPP/Kring Pajak 1500200 atau konsultan "
            "pajak sebelum mengajukan.".format(format_rp(final_salah)))
    if jenis == "K/I":
        catatan.append("Status K/I: seluruh penghasilan & kredit pajak istri sudah harus dimasukkan ke angka di atas. "
                       "Istri yang hanya bekerja pada 1 pemberi kerja (sudah dipotong) dan tidak terkait usaha suami "
                       "biasanya TIDAK digabung → pakai status K/.. biasa.")
    if status_spt == "LEBIH BAYAR":
        lb = -selisih
        if not usaha or lb <= BATAS_LB_PENDAHULUAN_USAHA:
            catatan.append("Lebih bayar {}: pilih 'dikembalikan' (restitusi; untuk kondisi Anda umumnya lewat "
                           "pengembalian pendahuluan, Pasal 17D UU KUP) atau 'dikompensasikan' ke tahun depan. "
                           "Siapkan semua bukti potong asli.".format(format_rp(lb)))
        else:
            catatan.append("Lebih bayar {} di atas Rp100 juta dengan usaha/pekerjaan bebas: restitusi umumnya melalui "
                           "pemeriksaan — konsultasikan ke konsultan pajak.".format(format_rp(lb)))
    if status_spt == "KURANG BAYAR":
        catatan.append("Kurang bayar (PPh Pasal 29) wajib dilunasi SEBELUM SPT dikirim. Di Coretax, SPT kurang bayar "
                       "masuk 'SPT menunggu pembayaran' dan kode billing dibuat otomatis.")

    hasil = {
        "versi_script": VERSI,
        "tahun_pajak": tahun,
        "status_ptkp": "{}/{}".format(jenis, n),
        "pekerjaan": pekerjaan,
        "usaha": usaha,
        "penghasilan_lain_neto": lain,
        "neto_pekerjaan": neto_kerja,
        "neto_usaha": neto_usaha,
        "jumlah_neto_sebelum_zakat": neto_bruto_total,
        "zakat_dikurangkan": zakat_dipakai,
        "penghasilan_neto": neto,
        "ptkp": ptkp,
        "rincian_ptkp": [{"komponen": r[0], "nilai": r[1]} for r in rincian_ptkp],
        "pkp_sebelum_bulat": pkp_mentah,
        "pkp": pkp,
        "lapisan_pasal17": lapisan,
        "pph_terutang": pph_terutang,
        "kredit_pajak": [{"komponen": k[0], "nilai": k[1]} for k in kredit],
        "total_kredit": total_kredit,
        "selisih": selisih,
        "status_spt": status_spt,
        "omzet_final_pp55": omzet_final,
        "pph_final_disetor": pph_final,
        "pph_final_salah_skema": final_salah,
        "perkiraan_pph25_per_bulan_tahun_berikut": pph25_berikut,
        "batas_lapor": batas.isoformat(),
        "batas_bebas_sanksi_kep55": batas_bebas_sanksi.isoformat() if batas_bebas_sanksi else None,
        "cek_ulang_a1_ke_hrd": cek_a1_tunggal,
        "keterangan_batas": ket_batas,
        "batas_sudah_lewat": sudah_lewat,
        "status_tenggat": tenggat,
        "tanggal_acuan": hari_ini.isoformat(),
        "nppn_tahun_berjalan": nppn_berjalan,
        "peringatan": peringatan,
        "catatan": catatan,
        "checklist_dokumen": checklist(pekerjaan, usaha, zakat, omzet_final, args, jenis, status_spt),
        "disclaimer": DISCLAIMER,
    }
    return hasil


def checklist(pekerjaan, usaha, zakat, omzet_final, args, jenis, status_spt):
    c = ["Akun Coretax aktif (login NIK/NPWP 16 digit) + kode verifikasi/otorisasi untuk tanda tangan SPT",
         "Daftar HARTA per 31 Desember (tanah/bangunan, kendaraan, tabungan, deposito, emas, investasi) "
         "dengan tahun perolehan & nilai",
         "Daftar UTANG per 31 Desember (KPR, kredit kendaraan, pinjaman) — nama pemberi pinjaman & sisa pokok",
         "Data keluarga & tanggungan (NIK) sesuai keadaan 1 Januari"]
    if pekerjaan:
        c.append("Bukti potong PPh 21 dari SETIAP pemberi kerja ({} lembar; A1 swasta / A2 ASN) — cek sudah muncul "
                 "otomatis di Coretax".format(len(pekerjaan)))
    if args.pph21_lain:
        c.append("Bukti potong PPh 21 bukan pegawai (honor/fee) dari tiap pemberi penghasilan")
    if args.pph22 or args.pph23:
        c.append("Bukti potong/pungut PPh 22 / PPh 23 (Bukti Potong Unifikasi)")
    if args.pph25:
        c.append("Bukti setor (NTPN) angsuran PPh 25 bulanan")
    if any(u["metode"] == "NPPN" for u in usaha):
        c.append("Rekap peredaran bruto per bulan (pencatatan) + bukti pemberitahuan penggunaan NPPN ke DJP")
    if any(u["metode"] == "pembukuan" for u in usaha):
        c.append("Laporan keuangan (neraca & laba rugi) + rekonsiliasi fiskal dari pembukuan")
    if h_final_salah(args):
        c.append("Bukti setor (NTPN) PPh final 0,5% yang salah skema — untuk permohonan pengembalian pajak yang "
                 "seharusnya tidak terutang (bukan untuk Lampiran 2)")
    if omzet_final:
        c.append("Rekap omzet PP 55 per bulan + bukti setor (NTPN) PPh final 0,5% / dokumen tagihan marketplace")
    if zakat:
        c.append("Bukti setor zakat dari BAZNAS/LAZ resmi (nama, NIK/NPWP, jumlah, tanggal, nama lembaga)")
    if jenis == "K/I":
        c.append("Seluruh bukti potong & data penghasilan istri (digabung)")
    if status_spt == "KURANG BAYAR":
        c.append("Saldo untuk melunasi PPh Pasal 29 (kode billing dari Coretax) sebelum SPT dikirim")
    if status_spt == "LEBIH BAYAR":
        c.append("Nomor rekening bank atas nama sendiri bila memilih restitusi")
    return c


# ------------------------------------------------------------------ output
def ke_json(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj == obj.to_integral_value() else float(obj)
    if isinstance(obj, dict):
        return {k: ke_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [ke_json(v) for v in obj]
    return obj


def h_final_salah(args):
    return bool(getattr(args, "final_salah_skema", None))


def teks(h):
    b = ["## Hitungan SPT Tahunan PPh Orang Pribadi — Tahun Pajak {} (status {})".format(
        h["tahun_pajak"], h["status_ptkp"]), ""]
    t = h["status_tenggat"]
    b += ["**⏰ Status tenggat lapor (per {}): {}**".format(t["tanggal_acuan"], t["ringkas"]),
          "- Saran: " + t["saran"]] + ["- " + k for k in t["konsekuensi"]] + [""]
    b += ["**1. Penghasilan neto**", "", "| Sumber | Neto |", "|---|---|"]
    for p in h["pekerjaan"]:
        b.append("| {} | {} |".format(p["sumber"], format_rp(p["neto"])))
    for u in h["usaha"]:
        b.append("| {} | {} |".format(u["sumber"], format_rp(u["neto"])))
    if h["penghasilan_lain_neto"]:
        b.append("| Penghasilan lain (non-final) | {} |".format(format_rp(h["penghasilan_lain_neto"])))
    b.append("| **Jumlah** | **{}** |".format(format_rp(h["jumlah_neto_sebelum_zakat"])))
    if h["zakat_dikurangkan"]:
        b.append("| Dikurangi zakat (BAZNAS/LAZ resmi) | −{} |".format(format_rp(h["zakat_dikurangkan"])))
    b.append("| **Penghasilan neto** | **{}** |".format(format_rp(h["penghasilan_neto"])))
    b += ["", "**2. PTKP & Penghasilan Kena Pajak (PKP)**", ""]
    for r in h["rincian_ptkp"]:
        b.append("- {}: {}".format(r["komponen"], format_rp(r["nilai"])))
    b.append("- **PTKP {}: {}**".format(h["status_ptkp"], format_rp(h["ptkp"])))
    b.append("- PKP = {} − {} = {} → dibulatkan ke bawah ribuan: **{}**".format(
        format_rp(h["penghasilan_neto"]), format_rp(h["ptkp"]), format_rp(h["pkp_sebelum_bulat"]), format_rp(h["pkp"])))
    b += ["", "**3. PPh terutang (tarif Pasal 17 UU HPP)**", ""]
    if not h["lapisan_pasal17"]:
        b.append("- PKP Rp 0 → PPh terutang Rp 0")
    for l in h["lapisan_pasal17"]:
        b.append("- {} × {} = {}".format(format_persen(l["tarif_persen"]), format_rp(l["dasar"]), format_rp(l["pajak"])))
    b.append("- **PPh terutang: {}**".format(format_rp(h["pph_terutang"])))
    b += ["", "**4. Kredit pajak (sudah dipotong/dibayar)**", ""]
    if not h["kredit_pajak"]:
        b.append("- (tidak ada)")
    for k in h["kredit_pajak"]:
        b.append("- {}: {}".format(k["komponen"], format_rp(k["nilai"])))
    b.append("- **Total kredit: {}**".format(format_rp(h["total_kredit"])))
    b += ["", "**5. Hasil: {}**".format(h["status_spt"])]
    if h["status_spt"] == "KURANG BAYAR":
        b.append("PPh terutang {} − kredit {} = **{} harus disetor (PPh Pasal 29) sebelum lapor**.".format(
            format_rp(h["pph_terutang"]), format_rp(h["total_kredit"]), format_rp(h["selisih"])))
    elif h["status_spt"] == "LEBIH BAYAR":
        b.append("Kredit {} − PPh terutang {} = **{} lebih bayar**.".format(
            format_rp(h["total_kredit"]), format_rp(h["pph_terutang"]), format_rp(-h["selisih"])))
    else:
        b.append("Pajak yang sudah dipotong sama dengan PPh terutang — tidak ada yang perlu disetor.")
    if h["perkiraan_pph25_per_bulan_tahun_berikut"] is not None:
        b.append("Perkiraan angsuran PPh 25 tahun {}: **{} per bulan**.".format(
            h["tahun_pajak"] + 1, format_rp(h["perkiraan_pph25_per_bulan_tahun_berikut"])))
    if h["omzet_final_pp55"]:
        b.append("Info: omzet PPh final 0,5% {} (PPh final disetor {}) dilaporkan terpisah, tidak mengubah angka di atas."
                 .format(format_rp(h["omzet_final_pp55"]), format_rp(h["pph_final_disetor"])))
    if h.get("pph_final_salah_skema"):
        b.append("Info: PPh final 0,5% salah skema {} tidak dikreditkan dan tidak dilaporkan di Lampiran 2 — "
                 "lihat Peringatan (pengembalian lewat Coretax).".format(format_rp(h["pph_final_salah_skema"])))
    label = ""
    if h["batas_sudah_lewat"]:
        label = " — JATUH TEMPO SUDAH LEWAT"
        bs = h.get("batas_bebas_sanksi_kep55")
        if bs and h["tanggal_acuan"] <= bs:
            label += " (masih masa bebas sanksi s.d. {})".format(bs)
    b += ["", "**Batas lapor:** {}{} — status per {}: {}".format(
        h["keterangan_batas"], label, h["status_tenggat"]["tanggal_acuan"], h["status_tenggat"]["kode"])]
    if h["peringatan"]:
        b += ["", "**⚠️ Peringatan**"] + ["- " + p for p in h["peringatan"]]
    if h["catatan"]:
        b += ["", "**Catatan**"] + ["- " + c for c in h["catatan"]]
    b += ["", "**Checklist dokumen**"] + ["- [ ] " + c for c in h["checklist_dokumen"]]
    b += ["", "_" + h["disclaimer"] + "_"]
    return "\n".join(b)


# ------------------------------------------------------------------ CLI
def buat_parser():
    ap = argparse.ArgumentParser(
        prog="spt_op.py", allow_abbrev=False,
        description="Hitung SPT Tahunan PPh Orang Pribadi (tarif Pasal 17 UU HPP). Hanya menghitung — tidak "
                    "mengisi/mengirim SPT.")
    ap.add_argument("--status", required=True, help="Status PTKP awal tahun: TK/0..3, K/0..3, K/I/0..3")
    ap.add_argument("--tahun", type=int, help="Tahun pajak (default: tahun lalu)")
    ap.add_argument("--a1", nargs=2, action="append", metavar=("NETO", "PPH21"),
                    help="Per bukti potong A1/A2: penghasilan neto & PPh 21 dipotong. Ulangi untuk tiap pemberi kerja")
    ap.add_argument("--a1-bruto", nargs="+", action="append", metavar="NILAI",
                    help="Cadangan bila neto tidak diketahui: BRUTO PPH21 [BULAN=12] [IURAN_PENSIUN_PEGAWAI=0]")
    ap.add_argument("--nppn", nargs=2, action="append", metavar=("BRUTO", "PERSEN"),
                    help="Usaha/pekerjaan bebas dengan norma: peredaran bruto setahun & persen norma PER-17/PJ/2015")
    ap.add_argument("--nppn-diberitahukan", choices=["ya", "tidak"],
                    help="Sudah memberitahukan penggunaan NPPN ke DJP dalam 3 bulan pertama tahun pajak?")
    ap.add_argument("--pembukuan-neto", action="append", metavar="NETO",
                    help="Neto fiskal usaha/pekerjaan bebas dari pembukuan (tidak boleh negatif)")
    ap.add_argument("--lain-neto", help="Penghasilan neto lain yang TIDAK final (mis. sewa non-final, royalti)")
    ap.add_argument("--omzet-final", help="Omzet setahun yang dikenai PPh final 0,5%% PP 55 (info, tidak dihitung "
                                          "Pasal 17)")
    ap.add_argument("--pph-final", help="Total PPh final 0,5%% yang sudah disetor/dipungut setahun (info)")
    ap.add_argument("--final-salah-skema", help="PPh final 0,5%% yang TERLANJUR disetor atas penghasilan pekerjaan "
                                                "bebas (salah skema): tidak dikreditkan, tidak masuk Lampiran 2")
    ap.add_argument("--zakat", help="Zakat/sumbangan keagamaan wajib ke lembaga resmi, di luar yang dipotong kantor")
    ap.add_argument("--pph21-lain", help="Total PPh 21 lain (bukti potong bukan pegawai/honor) di luar --a1")
    ap.add_argument("--pph22", help="Total PPh 22 yang dipungut (dapat dikreditkan)")
    ap.add_argument("--pph23", help="Total PPh 23 yang dipotong")
    ap.add_argument("--pph25", help="Total angsuran PPh 25 yang sudah dibayar tahun itu")
    ap.add_argument("--hari-ini", help="Tanggal acuan YYYY-MM-DD (default: hari ini)")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    return ap


def main(argv=None):
    ap = buat_parser()
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        cek_negatif_argv(argv)
    except InputError as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    args = ap.parse_args(argv)
    try:
        hari = None
        if args.hari_ini:
            try:
                hari = datetime.date.fromisoformat(args.hari_ini)
            except ValueError:
                raise InputError("--hari-ini harus YYYY-MM-DD (sekarang '{}')".format(args.hari_ini))
        h = hitung(args, hari)
    except InputError as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(ke_json(h), ensure_ascii=False, indent=2))
    else:
        print(teks(h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
