#!/usr/bin/env python3
"""Alat hitung skill atur-keuangan-pribadi (keuangan pribadi & keluarga Indonesia).

Hanya pustaka standar Python 3.7+, tanpa akses jaringan, tanpa menyimpan data.
Jalankan dengan `python3` (Windows: `python` atau `py`).

Subperintah:
  anggaran       Anggaran bulanan zero-based + perbandingan pola 50/30/20
  dana-darurat   Target dana darurat 3-12 bulan sesuai status + lama mencapainya
  utang          Rencana pelunasan utang Avalanche / Snowball / banding (jadwal bulanan)
  konversi-flat  Ubah bunga flat (leasing/KTA) ke bunga efektif setara
  target         Tabungan bulanan untuk target (DP rumah, sekolah anak, haji, pensiun)

Contoh cepat:
  python3 keuangan.py anggaran --pemasukan "Gaji=7,5jt" --musiman "THR=7,5jt" \
      --pos "Kontrakan=1,8jt" --pos "Kiriman ortu=750rb" --pos "Nongkrong=400rb:keinginan"
  python3 keuangan.py dana-darurat --pengeluaran-pokok 4,5jt --status anak --saldo 6jt --setoran 750rb
  python3 keuangan.py utang --utang "Kartu kredit;8jt;1,75%/bln;400rb;kk" \
      --utang "Paylater;2,5jt;3%/bln;300rb;paylater" --ekstra 500rb --metode banding
  python3 keuangan.py konversi-flat --pokok 18jt --bunga-flat "12%/th" --tenor 24
  python3 keuangan.py target --nama "DP rumah" --biaya-sekarang 60jt --tahun 5 --inflasi 4

Semua uang memakai Decimal. Bunga bulanan dibulatkan ke rupiah terdekat (setengah ke atas);
tabungan bulanan yang dibutuhkan dibulatkan KE ATAS agar target tidak kurang Rp1.
Hasil adalah alat bantu perencanaan, BUKAN nasihat keuangan/investasi.
"""
import argparse
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING, ROUND_FLOOR, localcontext, getcontext

getcontext().prec = 60

BATAS_BULAN_SIMULASI = 600          # 50 tahun
BATAS_BUNGA_KK_BULAN = Decimal("1.75")      # BI: maks 1,75%/bulan sejak Juli 2021 (cek ulang)
BATAS_BUNGA_PINJOL_BULAN = Decimal("3")     # OJK: pinjol konsumtif maks 0,1%/hari (2026) ~ 3%/bulan
BATAS_RASIO_CICILAN = Decimal("30")         # patokan umum: total cicilan <= 30% pemasukan

SATU = Decimal(1)
NOL = Decimal(0)


class InputSalah(Exception):
    """Kesalahan input yang dijelaskan ke pengguna tanpa traceback."""


# Peringatan input (bukan galat) yang dicetak di awal keluaran. Dikosongkan tiap main().
PERINGATAN_INPUT = []
BATAS_NOMINAL_KECIL = Decimal(10000)
BATAS_BUNGA_TANPA_SATUAN = Decimal(3)   # angka < 3 tanpa satuan: kemungkinan besar per BULAN


def cek_nominal_kecil(nilai, asli, nama, tambahan=""):
    """Nominal gaji/saldo/pokok < Rp10.000 hampir pasti salah ketik (mis. '1.500' maksudnya 1,5 juta)."""
    if nilai is None or nilai <= 0 or nilai >= BATAS_NOMINAL_KECIL:
        return nilai
    saran = [rp(nilai * 1000)]
    if nilai < 10:
        saran.insert(0, rp(nilai * 1000000))
    PERINGATAN_INPUT.append(
        "{} '{}' dibaca {} - sangat kecil untuk kolom ini. Jika maksudnya {}, tulis lengkap dengan satuan "
        "(mis. 1,5jt, 750rb, 1.500.000) lalu hitung ulang.{}".format(nama, asli, rp(nilai), " atau ".join(saran),
                                                                    tambahan))
    return nilai


def _bersatuan_ribu(teks):
    """True bila jumlah ditulis dengan satuan kata (5rb, 5 ribu, 5k, 1jt): nominal kecil memang disengaja."""
    return bool(re.search(r"(rb|ribu|k|jt|juta|miliar|milyar)\s*$", str(teks).strip().lower().replace(",-", "")))


# ---------------------------------------------------------------------------
# Pembulatan & format
# ---------------------------------------------------------------------------

def bulat(x):
    """Rupiah terdekat, setengah ke atas."""
    return Decimal(x).quantize(SATU, rounding=ROUND_HALF_UP)


def bulat_atas(x):
    return Decimal(x).quantize(SATU, rounding=ROUND_CEILING)


def bulat_bawah(x):
    return Decimal(x).quantize(SATU, rounding=ROUND_FLOOR)


def rp(x):
    """Format Rupiah gaya Indonesia: Rp1.500.000 (tanpa sen)."""
    n = bulat(x)
    tanda = "-" if n < 0 else ""
    s = "{:,}".format(abs(int(n))).replace(",", ".")
    return "{}Rp{}".format(tanda, s)


def persen(x, digit=1):
    q = Decimal(1).scaleb(-digit)
    s = str(Decimal(x).quantize(q, rounding=ROUND_HALF_UP)).replace(".", ",")
    return s + "%"


# ---------------------------------------------------------------------------
# Parsing angka rupiah & persen gaya Indonesia
# ---------------------------------------------------------------------------

_SATUAN = [
    (("miliar", "milyar"), Decimal("1000000000")),
    (("juta", "jt"), Decimal("1000000")),
    (("ribu", "rb", "k"), Decimal("1000")),
]


def _angka_polos(s, ada_satuan):
    """Ubah '1.500.000', '1.500.000,50', '1,5', '1.5', '1,500,000' -> Decimal."""
    if not s or not re.fullmatch(r"[0-9.,]+", s) or not re.search(r"[0-9]", s):
        raise ValueError
    titik, koma = s.count("."), s.count(",")
    if titik and koma:
        # pemisah yang muncul terakhir = desimal
        if s.rfind(",") > s.rfind("."):
            ribuan, desimal = ".", ","
        else:
            ribuan, desimal = ",", "."
        bagian_bulat, bagian_desimal = s.rsplit(desimal, 1)
        if not re.fullmatch(r"\d{1,3}(\%s\d{3})*" % ribuan, bagian_bulat):
            raise ValueError
        return Decimal(bagian_bulat.replace(ribuan, "") + "." + bagian_desimal)
    pemisah = "." if titik else ("," if koma else None)
    if pemisah is None:
        return Decimal(s)
    jumlah = s.count(pemisah)
    kiri, kanan = s.split(pemisah, 1)
    if ada_satuan and jumlah == 1:
        # "1,5jt" / "1.5jt" -> desimal
        if not kiri or not kanan:
            raise ValueError
        return Decimal(kiri + "." + kanan)
    if re.fullmatch(r"\d{1,3}(\%s\d{3})+" % pemisah, s):
        return Decimal(s.replace(pemisah, ""))       # pemisah ribuan
    if jumlah == 1 and pemisah == "," and 1 <= len(kanan) <= 2 and kiri:
        return Decimal(kiri + "." + kanan)           # sen: "1500000,50"
    raise ValueError


def parse_rupiah(teks, nama="jumlah", boleh_nol=True):
    """Terima 'Rp1.500.000', '1,5jt', '750rb', '2 juta', '1500000', 'Rp 1.500.000,-'."""
    if teks is None:
        raise InputSalah("{} belum diisi.".format(nama))
    asli = str(teks)
    s = asli.strip().lower().replace(" ", "").replace(" ", "")
    s = s.replace(",-", "").replace(".-", "")
    if s.startswith("-") or s.startswith("rp-") or s.startswith("idr-") or s.startswith("minus"):
        raise InputSalah("{} tidak boleh negatif: '{}'.".format(nama, asli))
    for awalan in ("rp.", "rp", "idr"):
        if s.startswith(awalan):
            s = s[len(awalan):]
            break
    if s.endswith("m") and not s.endswith("miliar") and not s.endswith("milyar"):
        raise InputSalah(
            "'{}' ambigu ('M' bisa berarti juta atau miliar). Tulis 'juta'/'jt' atau 'miliar'.".format(asli))
    faktor = SATU
    ada_satuan = False
    for kata, f in _SATUAN:
        for k in kata:
            if s.endswith(k):
                s = s[: -len(k)]
                faktor, ada_satuan = f, True
                break
        if ada_satuan:
            break
    try:
        nilai = _angka_polos(s, ada_satuan) * faktor
    except (ValueError, ArithmeticError):
        raise InputSalah(
            "{} '{}' tidak terbaca. Contoh yang benar: Rp1.500.000, 1500000, 1,5jt, 750rb.".format(nama, asli))
    if nilai < 0:
        raise InputSalah("{} tidak boleh negatif: '{}'.".format(nama, asli))
    if not boleh_nol and nilai == 0:
        raise InputSalah("{} harus lebih dari nol: '{}'.".format(nama, asli))
    return nilai


class Bunga(object):
    """Bunga bulanan = pct * kali / bagi (disimpan terpisah agar pembagian terjadi sekali)."""

    def __init__(self, pct, kali, bagi, periode):
        self.pct, self.kali, self.bagi, self.periode = pct, kali, bagi, periode

    def per_bulan_persen(self):
        return self.pct * self.kali * 100 / self.bagi

    def bunga_dari(self, saldo):
        return bulat(saldo * self.pct * self.kali / self.bagi)


def _fmt_pct(pct):
    s = format(pct.normalize(), "f")
    return s.replace(".", ",") + "%"


def parse_bunga(teks, nama="bunga", periode_bawaan="th"):
    """'24%', '24%/th', '1,75%/bln', '0,1%/hari', '12 per tahun' -> Bunga."""
    if teks is None or str(teks).strip() == "":
        raise InputSalah("{} belum diisi.".format(nama))
    asli = str(teks)
    s = asli.strip().lower().replace(" ", "")
    # jenis bunga yang ikut ditulis ('0,9%/bln flat', '1,5%/bln efektif'): dicatat, lalu dibuang dari angka
    tanda = None
    for kata in ("efektif", "flat"):
        if kata in s:
            if tanda:
                raise InputSalah("{} '{}' menyebut flat DAN efektif. Pilih salah satu.".format(nama, asli))
            tanda = kata
            s = s.replace(kata, "")
    s = s.replace("persen", "%")          # '1,5 persen per bulan' -> '1,5%perbulan'
    periode = periode_bawaan
    satuan_ditulis = False
    pola_periode = [
        ("hari", ("/hari", "perhari", "sehari", "/hr", "harian")),
        ("bln", ("/bulan", "perbulan", "sebulan", "/bln", "bulanan", "/bl")),
        ("th", ("/tahun", "pertahun", "setahun", "/thn", "/th", "p.a.", "p.a", "pa", "tahunan", "/tahunan")),
    ]
    for kode, akhiran in pola_periode:
        for a in akhiran:
            if s.endswith(a):
                s = s[: -len(a)]
                periode, satuan_ditulis = kode, True
                break
        else:
            continue
        break
    s = s.rstrip("%")
    if s.startswith("-"):
        raise InputSalah("{} tidak boleh negatif: '{}'.".format(nama, asli))
    if not re.fullmatch(r"\d+([.,]\d+)?", s or ""):
        raise InputSalah(
            "{} '{}' tidak terbaca. Contoh: 24%/th, 1,75%/bln, 18% setahun, 1,5 persen per bulan, "
            "0,1%/hari.".format(nama, asli))
    pct = Decimal(s.replace(",", "."))
    b = buat_bunga(pct, periode, nama, asli, eksplisit=satuan_ditulis)
    b.tanda = tanda
    return b


def buat_bunga(pct, periode, nama="bunga", asli=None, eksplisit=True):
    """periode: 'th' | 'bln' | 'hari'. eksplisit=False bila pengguna tidak menyebut satuan."""
    if periode == "th":
        b = Bunga(pct, 1, 1200, "per tahun")
    elif periode == "bln":
        b = Bunga(pct, 1, 100, "per bulan")
    else:
        b = Bunga(pct, 30, 100, "per hari (dihitung 30 hari/bulan)")
    if b.per_bulan_persen() > 50:
        raise InputSalah("{} '{}' = {} per bulan, tidak wajar. Periksa lagi angkanya.".format(
            nama, asli if asli is not None else _fmt_pct(pct), persen(b.per_bulan_persen(), 2)))
    b.kode, b.eksplisit, b.asli = periode, eksplisit, asli
    b.tanda = None
    return b


_PER = {"bulan": "bln", "bln": "bln", "bulanan": "bln", "tahun": "th", "th": "th", "thn": "th",
        "tahunan": "th", "hari": "hari", "harian": "hari"}


def terapkan_per(b, per, nama):
    """Pakai satuan dari opsi --per untuk bunga TANPA satuan; tolak bila bertentangan."""
    if per is None:
        return b
    kode = _PER[per]
    if b.eksplisit:
        if b.kode != kode:
            raise InputSalah("{} '{}' sudah bersatuan {}, tetapi --per {}. Pilih salah satu.".format(
                nama, b.asli, b.periode, per))
        return b
    baru = buat_bunga(b.pct, kode, nama, b.asli, eksplisit=True)
    baru.tanda = getattr(b, "tanda", None)
    return baru


def pesan_bunga_ambigu(b, nama):
    x = _fmt_pct(b.pct)
    return ("{} '{}' tanpa satuan: {} per BULAN atau per TAHUN? Untuk kartu kredit/KTA/paylater/pinjol di "
            "Indonesia, angka di bawah 3 biasanya per BULAN. Tulis jelas, mis. '{}/bln' atau '{}/th' "
            "(atau pakai --per bulan / --per tahun).".format(nama, b.asli, x, x, x))


def parse_persen_tahunan(teks, nama):
    if teks is None:
        return None
    s = str(teks).strip().lower().replace(" ", "")
    for a in ("pertahun", "setahun", "/tahun", "/thn", "/th", "p.a.", "p.a"):
        if s.endswith(a):
            s = s[: -len(a)]
            break
    s = s.replace("persen", "%").rstrip("%").replace(",", ".")
    if s.startswith("-"):
        raise InputSalah("{} tidak boleh negatif: '{}'. Isi 0 jika tidak ada.".format(nama, teks))
    if not re.fullmatch(r"\d+(\.\d+)?", s):
        raise InputSalah("{} '{}' tidak terbaca. Contoh: 4 atau 4,5%.".format(nama, teks))
    v = Decimal(s)
    if v > 50:
        raise InputSalah("{} {}% per tahun tidak wajar untuk perencanaan. Periksa lagi.".format(nama, teks))
    return v


def pisah_nama_jumlah(teks, label):
    if "=" in teks:
        n, j = teks.rsplit("=", 1)
        n = n.strip() or label
    else:
        n, j = label, teks
    return n, j


# ---------------------------------------------------------------------------
# 1. Anggaran
# ---------------------------------------------------------------------------

KATA_KELOMPOK = [
    ("tabungan", ("tabung", "dana darurat", "investasi", "pensiun", "arisan", "haji", "umrah", "umroh",
                  "dp rumah", "pendidikan anak", "dana pendidikan", "ekstra utang", "pelunasan",
                  "reksa", "deposito", "emas")),
    ("sosial", ("kiriman", "orang tua", "ortu", "mertua", "keluarga", "adik", "zakat", "perpuluhan",
                "sedekah", "infak", "infaq", "persembahan", "kolekte", "kondangan", "sumbangan",
                "punia", "dana punia")),
    ("keinginan", ("nongkrong", "jajan", "kopi", "langganan", "netflix", "spotify", "youtube",
                   "hiburan", "liburan", "jalan-jalan", "belanja online", "shopee", "tokopedia",
                   "skincare", "hobi", "rokok", "game", "makan di luar", "ngopi", "fashion", "baju")),
    ("wajib", ("sewa", "kontrakan", "kos", "kost", "kpr", "listrik", "token", "pdam", "air",
               "internet", "wifi", "pulsa", "kuota", "makan", "dapur", "sembako", "belanja bulanan",
               "transport", "bensin", "ojek", "parkir", "cicilan", "kredit", "angsuran", "sekolah",
               "spp", "bpjs", "asuransi", "obat", "kesehatan", "gas", "lpg", "iuran", "ipl",
               "sampah", "galon", "susu", "popok", "pampers", "art", "pembantu", "daycare", "les", "kartu kredit",
               "paylater", "pinjol", "kta")),
]
NAMA_KELOMPOK = {
    "wajib": "Kebutuhan wajib",
    "sosial": "Keluarga & sosial/ibadah",
    "keinginan": "Keinginan",
    "tabungan": "Tabungan, dana darurat & pelunasan ekstra",
    "lain": "Belum dikelompokkan",
}
KATA_CICILAN = ("cicilan", "kpr", "kredit", "angsuran", "paylater", "pay later", "pinjol", "kta", "leasing",
                "spaylater", "kredivo", "akulaku", "pinjaman")
KATA_EWALLET = ("gopay", "ovo", "shopeepay", "linkaja", "top up", "topup", "top-up", "e-wallet",
                "ewallet", "saldo dana", "isi dana")


def adalah_cicilan(nama):
    """Pos cicilan/utang (PayLater, kartu kredit, KPR, pinjol, leasing, KTA) -> selalu masuk pengeluaran pokok."""
    n = nama.lower()
    if "ekstra" in n or "pelunasan" in n:   # setoran tambahan = tabungan/pelunasan, bukan kewajiban minimum
        return False
    return any(k in n for k in KATA_CICILAN)


def tebak_kelompok(nama):
    n = nama.lower()
    for kelompok, kata in KATA_KELOMPOK:
        for k in kata:
            if re.search(r"(?<![a-z])" + re.escape(k), n):
                return kelompok
    return "lain"


def parse_pos(teks):
    kelompok = None
    badan = teks
    m = re.match(r"^(.*):\s*(wajib|kebutuhan|sosial|keluarga|keinginan|tabungan)\s*$", teks, re.I)
    if m:
        badan = m.group(1)
        k = m.group(2).lower()
        kelompok = {"kebutuhan": "wajib", "keluarga": "sosial"}.get(k, k)
    if "=" not in badan:
        raise InputSalah("Pos '{}' harus berformat nama=jumlah, mis. \"Kontrakan=1,5jt\".".format(teks))
    nama, jumlah = badan.rsplit("=", 1)
    nama = nama.strip()
    if not nama:
        raise InputSalah("Pos '{}' belum punya nama.".format(teks))
    if ":" in jumlah:
        label = jumlah.split(":", 1)[1].strip()
        raise InputSalah("Pos '{}': label kelompok '{}' tidak dikenal. Label harus wajib, sosial, keinginan, "
                         "atau tabungan (mis. \"{}={}:keinginan\"), atau hapus labelnya.".format(
                             teks, label, nama, jumlah.split(":", 1)[0].strip()))
    nilai = parse_rupiah(jumlah, "Pos '{}'".format(nama))
    # v1.0.3: pos yang wajar bernilai kecil (parkir 5.000, sampah 8.000) tidak diperingatkan kecuali < Rp1.000;
    # pos lain < Rp10.000 tetap diperingatkan (mis. "Makan=1.500" hampir pasti 1,5 juta). Input ber-"Rp" = disengaja.
    pos_wajar_kecil = re.search(r"parkir|jajan|sampah|iuran|ronda|kas rt|sumbangan|infak|infaq|sedekah|tip|"
                                r"air galon|galon|gas|pulsa|kuota|tol|ojek|angkot|kopi|rokok|cemilan|camilan",
                                nama.lower())
    batas = Decimal(1000) if pos_wajar_kecil else BATAS_NOMINAL_KECIL
    if (not _bersatuan_ribu(jumlah) and not jumlah.strip().lower().startswith("rp")
            and nilai is not None and nilai < batas):
        cek_nominal_kecil(nilai, jumlah.strip(), "Pos '{}'".format(nama),
                          " Jika memang {}, abaikan peringatan ini (atau tulis {}rb).".format(
                              rp(nilai), format(nilai / 1000, "f").rstrip("0").rstrip(".").replace(".", ",")))
    return nama, nilai, (kelompok or tebak_kelompok(nama)), kelompok is None


def parse_pola(teks):
    bagian = re.split(r"[/\-:]", teks.strip())
    if len(bagian) != 3:
        raise InputSalah("Pola '{}' harus 3 angka, mis. 50/30/20 atau 60/20/20.".format(teks))
    try:
        angka = [Decimal(b.strip().rstrip("%").replace(",", ".")) for b in bagian]
    except ArithmeticError:
        raise InputSalah("Pola '{}' tidak terbaca.".format(teks))
    if any(a < 0 for a in angka) or sum(angka) != 100:
        raise InputSalah("Pola '{}' harus berjumlah 100 dan tidak negatif.".format(teks))
    return angka


def hitung_anggaran(pemasukan, musiman, pos, pola):
    """pemasukan/musiman: list (nama, Decimal); pos: list (nama, nilai, kelompok, ditebak)."""
    total_bulanan = sum((j for _, j in pemasukan), NOL)
    total_musiman = sum((j for _, j in musiman), NOL)
    musiman_per_bulan = bulat_bawah(total_musiman / 12)
    total_masuk = total_bulanan + musiman_per_bulan
    per_kelompok = {k: NOL for k in NAMA_KELOMPOK}
    for _, nilai, kel, _ in pos:
        per_kelompok[kel] += nilai
    total_keluar = sum(per_kelompok.values(), NOL)
    sisa = total_masuk - total_keluar
    kebutuhan = per_kelompok["wajib"] + per_kelompok["sosial"]
    keinginan = per_kelompok["keinginan"] + per_kelompok["lain"]
    tabungan = per_kelompok["tabungan"]
    cicilan = sum((n for nm, n, _, _ in pos if adalah_cicilan(nm)), NOL)
    # v1.0.5: dasar dana darurat = semua pos wajib + SEMUA cicilan/utang minimum (apa pun kelompoknya).
    pokok_rinci = [(nm, n) for nm, n, kel, _ in pos if n > 0 and (kel == "wajib" or adalah_cicilan(nm))]
    pokok = sum((n for _, n in pokok_rinci), NOL)
    return {
        "pokok_dana_darurat": pokok, "pokok_rinci": pokok_rinci,
        "total_bulanan": total_bulanan, "total_musiman": total_musiman,
        "musiman_per_bulan": musiman_per_bulan, "total_masuk": total_masuk,
        "per_kelompok": per_kelompok, "total_keluar": total_keluar, "sisa": sisa,
        "kebutuhan": kebutuhan, "keinginan": keinginan, "tabungan": tabungan,
        "cicilan": cicilan,
        "target_pola": [bulat(total_masuk * p / 100) for p in pola],
    }


def cetak_anggaran(args):
    pemasukan = []
    for t in args.pemasukan or []:
        n, j = pisah_nama_jumlah(t, "Pemasukan")
        pemasukan.append((n, cek_nominal_kecil(parse_rupiah(j, "Pemasukan '{}'".format(n)), j,
                                               "Pemasukan '{}'".format(n))))
    musiman = []
    for t in args.musiman or []:
        n, j = pisah_nama_jumlah(t, "Pemasukan musiman")
        musiman.append((n, cek_nominal_kecil(parse_rupiah(j, "Pemasukan musiman '{}'".format(n)), j,
                                             "Pemasukan musiman '{}'".format(n))))
    if not pemasukan and not musiman:
        raise InputSalah("Isi minimal satu --pemasukan (pemasukan bersih per bulan), mis. --pemasukan \"Gaji=6jt\".")
    pos = [parse_pos(t) for t in (args.pos or [])]
    pola = parse_pola(args.pola)
    h = hitung_anggaran(pemasukan, musiman, pos, pola)
    if h["total_masuk"] <= 0:
        raise InputSalah("Total pemasukan per bulan nol. Isi pemasukan bersih yang benar.")
    out = ["# Anggaran Bulanan (zero-based)", "", "## Pemasukan per bulan", "",
           "| Sumber | Jumlah |", "|---|---:|"]
    for n, j in pemasukan:
        out.append("| {} | {} |".format(n, rp(j)))
    if musiman:
        rinci = ", ".join("{} {}".format(n, rp(j)) for n, j in musiman)
        out.append("| Musiman dibagi 12 ({}; total {}/th) | {} |".format(
            rinci, rp(h["total_musiman"]), rp(h["musiman_per_bulan"])))
    out.append("| **Total pemasukan** | **{}** |".format(rp(h["total_masuk"])))
    out += ["", "## Pos pengeluaran & alokasi", "", "| Pos | Kelompok | Jumlah | % pemasukan |",
            "|---|---|---:|---:|"]
    for n, j, kel, ditebak in pos:
        out.append("| {} | {}{} | {} | {} |".format(
            n, NAMA_KELOMPOK[kel], " (tebakan)" if ditebak and kel != "lain" else "",
            rp(j), persen(j * 100 / h["total_masuk"])))
    out.append("| **Total dialokasikan** | | **{}** | {} |".format(
        rp(h["total_keluar"]), persen(h["total_keluar"] * 100 / h["total_masuk"])))
    if h["sisa"] > 0:
        out.append("| **Belum dialokasikan** | | **{}** | harus dijadikan 0 |".format(rp(h["sisa"])))
    elif h["sisa"] < 0:
        out.append("| **DEFISIT** | | **{}** | pengeluaran > pemasukan |".format(rp(h["sisa"])))
    else:
        out.append("| **Sisa** | | **Rp0** | zero-based tercapai |")
    p = pola
    t = h["target_pola"]
    out += ["", "## Banding pola {}/{}/{}".format(*[format(x.normalize(), "f") for x in p]), "",
            "| Kelompok | Pola | Batas pola | Rencana kamu | Selisih |", "|---|---:|---:|---:|---:|"]
    baris = [("Kebutuhan (wajib + keluarga/sosial)", p[0], t[0], h["kebutuhan"], "lebih"),
             ("Keinginan", p[1], t[1], h["keinginan"], "lebih"),
             ("Tabungan & pelunasan ekstra", p[2], t[2], h["tabungan"], "kurang")]
    for nama, pp, batas, nyata, arah in baris:
        selisih = nyata - batas
        out.append("| {} | {} | {} | {} | {} |".format(
            nama, persen(pp, 0), rp(batas), rp(nyata), ("+" if selisih > 0 else "") + rp(selisih)))
    cat = []
    if h["sisa"] > 0:
        cat.append("Masih ada {} belum punya tugas. Zero-based: arahkan ke dana darurat, pelunasan utang "
                   "berbunga tinggi, atau target tabungan sampai sisa Rp0.".format(rp(h["sisa"])))
    if h["sisa"] < 0:
        cat.append("DEFISIT {}. Kurangi pos Keinginan dulu, lalu tinjau pos lain. Jangan menutup defisit "
                   "dengan utang baru (paylater/pinjol) - itu gali lubang tutup lubang.".format(rp(-h["sisa"])))
    if h["kebutuhan"] > t[0]:
        if pola[0] < 60:
            cat.append("Kebutuhan melebihi batas pola. Wajar untuk keluarga dengan tanggungan atau kota "
                       "mahal; coba pola 60/20/20 dan pastikan tabungan tetap ada.")
        else:
            cat.append("Kebutuhan tetap melebihi batas pola {}%. Cek pos terbesar (tempat tinggal, cicilan, "
                       "dapur) dan jangan menambah cicilan baru; tabungan sekecil apa pun tetap jalan.".format(
                           format(pola[0].normalize(), "f")))
    if h["tabungan"] < t[2]:
        cat.append("Tabungan di bawah pola. Mulai dari jumlah kecil yang rutin (bayar diri sendiri dulu "
                   "di hari gajian).")
    rasio = h["cicilan"] * 100 / h["total_masuk"]
    if h["cicilan"] > 0:
        pesan = "Total cicilan {} = {} dari pemasukan.".format(rp(h["cicilan"]), persen(rasio))
        if rasio > BATAS_RASIO_CICILAN:
            pesan += " DI ATAS patokan umum 30% - jangan menambah utang baru; pertimbangkan subperintah utang."
        cat.append(pesan)
    lain = [n for n, _, k, _ in pos if k == "lain"]
    if lain:
        cat.append("Pos belum dikelompokkan (dihitung sebagai Keinginan sementara): {}. Tambahkan "
                   "':wajib'/':sosial'/':keinginan'/':tabungan' di akhir pos.".format(", ".join(lain)))
    ew = [n for n, _, _, _ in pos if any(k in n.lower() for k in KATA_EWALLET)]
    if ew:
        cat.append("Pos {} tampak seperti TOP-UP e-wallet. Top-up hanya pindah dompet, bukan pengeluaran; "
                   "catat menurut pemakaiannya (makan, transport, belanja) agar tidak dobel.".format(", ".join(ew)))
    if musiman:
        cat.append("Pemasukan musiman (THR/bonus) dibagi 12 dan dibulatkan ke bawah. Simpan saat cair, "
                   "lalu 'gaji'-kan ke anggaran tiap bulan; jangan dianggap uang bebas.")
    if cat:
        out += ["", "## Catatan", ""] + ["- " + c for c in cat]
    if h["pokok_rinci"]:
        out += ["", "## Dasar dana darurat (pengeluaran pokok per bulan)", "",
                "| Pos pokok | Jumlah |", "|---|---:|"]
        for n, j in h["pokok_rinci"]:
            out.append("| {}{} | {} |".format(n, " (cicilan)" if adalah_cicilan(n) else "", rp(j)))
        out.append("| **Total pengeluaran pokok** | **{}** |".format(rp(h["pokok_dana_darurat"])))
        sosial = [n for n, j, kel, _ in pos if kel == "sosial" and j > 0 and not adalah_cicilan(n)]
        out += ["", "- Pokok = semua pos Kebutuhan wajib + SEMUA cicilan/utang minimum (PayLater, kartu kredit, "
                "KPR, pinjol, leasing, KTA) - tetap harus dibayar walau penghasilan berhenti.",
                "- Pakai angka ini untuk dana darurat: dana-darurat --pengeluaran-pokok {} --status ...".format(
                    int(h["pokok_dana_darurat"].to_integral_value(rounding=ROUND_HALF_UP)))]
        if sosial:
            out.append("- Pos keluarga/sosial ({}) BELUM dihitung pokok; tambahkan bila tetap wajib dibayar "
                       "(mis. kiriman orang tua yang tidak bisa ditunda).".format(", ".join(sosial)))
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 2. Dana darurat
# ---------------------------------------------------------------------------

STATUS_DANA_DARURAT = {
    "pns": (3, 6, "PNS/pegawai tetap berpenghasilan sangat stabil"),
    "lajang": (3, 6, "Lajang tanpa tanggungan"),
    "menikah": (6, 9, "Menikah tanpa anak"),
    "anak": (9, 12, "Menikah/orang tua tunggal dengan anak atau tanggungan"),
    "lepas": (12, 12, "Pekerja lepas/freelancer/pemilik usaha, penghasilan tidak tetap"),
}


def hitung_dana_darurat(pokok, status, saldo, setoran):
    mn, ideal, ket = STATUS_DANA_DARURAT[status]
    hasil = []
    for bulan in sorted(set([mn, ideal])):
        target = pokok * bulan
        kurang = max(target - saldo, NOL)
        if kurang == 0:
            lama = 0
        elif setoran > 0:
            lama = int((kurang / setoran).to_integral_value(rounding=ROUND_CEILING))
        else:
            lama = None
        prog = min(saldo * 100 / target, Decimal(100)) if target > 0 else Decimal(100)
        hasil.append({"bulan": bulan, "target": target, "kurang": kurang, "lama": lama, "progres": prog})
    return ket, hasil


def cetak_dana_darurat(args):
    rinci = []
    if args.pengeluaran_pokok is not None:
        dasar = cek_nominal_kecil(parse_rupiah(args.pengeluaran_pokok, "Pengeluaran pokok per bulan",
                                               boleh_nol=not (args.pos or args.cicilan)),
                                  args.pengeluaran_pokok, "Pengeluaran pokok per bulan")
        if dasar > 0:
            rinci.append(("Pengeluaran pokok (angka gabungan)", dasar, False))
    for t in args.pos or []:
        n, j = pisah_nama_jumlah(t, "Pos pokok")
        rinci.append((n, cek_nominal_kecil(parse_rupiah(j, "Pos pokok '{}'".format(n)), j,
                                           "Pos pokok '{}'".format(n)), adalah_cicilan(n)))
    for t in args.cicilan or []:
        n, j = pisah_nama_jumlah(t, "Cicilan")
        rinci.append((n, parse_rupiah(j, "Cicilan '{}'".format(n)), True))
    if not rinci and args.pengeluaran_pokok is None:
        raise InputSalah("Isi --pengeluaran-pokok, atau rincian --pos \"Kontrakan=2jt\" / "
                         "--cicilan \"PayLater=650rb\".")
    pokok = sum((j for _, j, _ in rinci), NOL)
    if pokok <= 0:
        raise InputSalah("Pengeluaran pokok per bulan tidak boleh Rp0.")
    ada_cicilan = any(c for _, _, c in rinci)
    saldo = cek_nominal_kecil(parse_rupiah(args.saldo, "Saldo dana darurat"), args.saldo, "Saldo dana darurat")
    setoran = parse_rupiah(args.setoran, "Setoran per bulan")
    ket, hasil = hitung_dana_darurat(pokok, args.status, saldo, setoran)
    out = ["# Dana Darurat", "", "- Status: {} -> target {} bulan pengeluaran pokok".format(
        ket, "-".join(str(h["bulan"]) for h in hasil)),
        "- Pengeluaran pokok per bulan: {}{}".format(rp(pokok), " (rincian di bawah)" if len(rinci) > 1 else ""),
        "- Saldo sekarang: {} | Setoran rutin: {}/bulan".format(rp(saldo), rp(setoran)), "",
        "| Target | Jumlah | Kekurangan | Lama tercapai | Progres |", "|---|---:|---:|---:|---:|"]
    for h in hasil:
        if h["lama"] is None:
            lama = "tidak tercapai (setoran Rp0)"
        elif h["lama"] == 0:
            lama = "sudah tercapai"
        else:
            lama = "{} bulan (~{} th {} bln)".format(h["lama"], h["lama"] // 12, h["lama"] % 12)
        blok = int((h["progres"] / 5).to_integral_value(rounding=ROUND_FLOOR))
        out.append("| {} bulan | {} | {} | {} | {} {} |".format(
            h["bulan"], rp(h["target"]), rp(h["kurang"]), lama, "#" * blok + "." * (20 - blok),
            persen(h["progres"], 0)))
    if len(rinci) > 1:
        out += ["", "| Pos pokok | Jumlah |", "|---|---:|"]
        for n, j, c in rinci:
            out.append("| {}{} | {} |".format(n, " (cicilan)" if c else "", rp(j)))
        out.append("| **Total pengeluaran pokok** | **{}** |".format(rp(pokok)))
    out += ["", "Catatan:",
            "- Pengeluaran pokok = yang tetap harus dibayar walau penghasilan berhenti (makan, tempat tinggal, "
            "listrik/air, transport, SEMUA cicilan/utang minimum, sekolah, BPJS, kiriman keluarga yang wajib). "
            "Bukan nongkrong/hiburan."]
    if not ada_cicilan:
        out.append("- CEK CICILAN: belum ada cicilan yang tercatat. Bila ada cicilan PayLater, kartu kredit, KPR, "
                   "motor/leasing, KTA, atau pinjol, tambahkan (--cicilan \"PayLater=650rb\") - cicilan tetap "
                   "wajib dibayar saat penghasilan berhenti, jadi masuk dasar dana darurat.")
    out += [
            "- Simpan di tempat terpisah yang aman dan cepat dicairkan (bukan instrumen yang nilainya naik-turun).",
            "- Punya utang berbunga tinggi (kartu kredit/paylater/pinjol)? Kumpulkan dana darurat awal ~1 bulan "
            "pengeluaran pokok dulu, lalu fokus lunasi utang, baru lengkapi dana darurat."]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 3. Utang: avalanche / snowball
# ---------------------------------------------------------------------------

class Utang(object):
    def __init__(self, nama, saldo, bunga, minimum, jenis):
        self.nama, self.saldo, self.bunga, self.minimum, self.jenis = nama, saldo, bunga, minimum, jenis


JENIS_UTANG = ("kk", "kta", "paylater", "pinjol", "kpr", "motor", "mobil", "keluarga", "lain")


def parse_utang(teks, per=None):
    bagian = [b.strip() for b in teks.split(";")]
    if len(bagian) not in (4, 5):
        raise InputSalah(
            "Utang '{}' harus berformat nama;saldo;bunga;cicilan_minimum[;jenis], "
            "mis. \"Kartu kredit;8jt;1,75%/bln;400rb;kk\".".format(teks))
    nama = bagian[0] or "Utang"
    saldo = cek_nominal_kecil(parse_rupiah(bagian[1], "Saldo utang '{}'".format(nama)), bagian[1],
                              "Saldo utang '{}'".format(nama))
    nb = "Bunga utang '{}'".format(nama)
    bunga = terapkan_per(parse_bunga(bagian[2], nb), per, nb)
    if bunga.tanda == "flat":
        raise InputSalah("{} '{}' adalah bunga FLAT. Ubah dulu ke bunga efektif dengan subperintah konversi-flat, "
                         "lalu isi hasilnya (mis. '1,6275%/bln efektif').".format(nb, bagian[2]))
    if not bunga.eksplisit and 0 < bunga.pct < BATAS_BUNGA_TANPA_SATUAN:
        # angka kecil tanpa satuan: salah tafsir = hasil meleset belasan kali lipat -> tanya, jangan menebak
        raise InputSalah(pesan_bunga_ambigu(bunga, nb))
    minimum = parse_rupiah(bagian[3], "Cicilan minimum '{}'".format(nama))
    jenis = (bagian[4].lower() if len(bagian) == 5 and bagian[4] else "lain")
    if jenis not in JENIS_UTANG:
        raise InputSalah("Jenis utang '{}' tidak dikenal. Pilih: {}.".format(jenis, ", ".join(JENIS_UTANG)))
    if minimum == 0 and saldo > 0:
        raise InputSalah("Cicilan minimum '{}' Rp0. Isi cicilan minimum per bulan yang ditagih.".format(nama))
    return Utang(nama, saldo, bunga, minimum, jenis)


def urutan(daftar, metode):
    idx = list(range(len(daftar)))
    if metode == "avalanche":
        return sorted(idx, key=lambda i: (-daftar[i].bunga.per_bulan_persen(), daftar[i].saldo, i))
    return sorted(idx, key=lambda i: (daftar[i].saldo, -daftar[i].bunga.per_bulan_persen(), i))


def simulasi(daftar, anggaran, metode, batas=BATAS_BULAN_SIMULASI):
    """Kembalikan dict hasil. Anggaran = total bayar semua utang per bulan (tetap)."""
    saldo = [u.saldo for u in daftar]
    total_bunga = [NOL] * len(daftar)
    total_bayar = [NOL] * len(daftar)
    lunas = [0 if s == 0 else None for s in saldo]
    prioritas = urutan(daftar, metode)
    jadwal = []
    bulan = 0
    macet = False
    while any(s > 0 for s in saldo) and bulan < batas:
        bulan += 1
        total_awal = sum(saldo, NOL)
        rinci = {}
        for i, u in enumerate(daftar):
            if saldo[i] > 0:
                b = u.bunga.bunga_dari(saldo[i])
                saldo[i] += b
                total_bunga[i] += b
                rinci[i] = [NOL, b]
        sisa = anggaran
        for i in prioritas:
            if saldo[i] > 0:
                bayar = min(daftar[i].minimum, saldo[i], sisa)
                saldo[i] -= bayar
                sisa -= bayar
                rinci[i][0] += bayar
        for i in prioritas:
            if saldo[i] > 0 and sisa > 0:
                bayar = min(sisa, saldo[i])
                saldo[i] -= bayar
                sisa -= bayar
                rinci[i][0] += bayar
        for i in rinci:
            total_bayar[i] += rinci[i][0]
            if saldo[i] == 0 and lunas[i] is None:
                lunas[i] = bulan
            jadwal.append((bulan, daftar[i].nama, rinci[i][0], rinci[i][1], rinci[i][0] - rinci[i][1], saldo[i]))
        if any(s > 0 for s in saldo) and sum(saldo, NOL) >= total_awal:
            # total utang tidak turun: dengan anggaran tetap tidak akan pernah turun -> hentikan
            macet = True
            break
    selesai = all(s == 0 for s in saldo)
    return {"metode": metode, "bulan": bulan if selesai else None, "lunas": lunas, "macet": macet, "bulan_macet": bulan,
            "total_bunga": sum(total_bunga, NOL), "bunga_per": total_bunga,
            "total_bayar": sum(total_bayar, NOL), "sisa_saldo": saldo, "jadwal": jadwal,
            "prioritas": prioritas}


def peringatan_utang(daftar, anggaran):
    p = []
    for u in daftar:
        b1 = u.bunga.bunga_dari(u.saldo)
        pb = u.bunga.per_bulan_persen()
        if u.saldo > 0 and u.minimum <= b1:
            p.append("'{}': cicilan minimum {} TIDAK menutup bunga bulan pertama {}. Kalau hanya bayar minimum, "
                     "utang ini tidak akan pernah lunas (bisa terus membesar).".format(u.nama, rp(u.minimum), rp(b1)))
        if u.jenis == "kk" and pb > BATAS_BUNGA_KK_BULAN:
            p.append("'{}': bunga {}/bulan di atas batas bunga kartu kredit BI 1,75%/bulan. Cek ulang tagihan "
                     "atau tanyakan ke bank.".format(u.nama, persen(pb, 2)))
        if pb > BATAS_BUNGA_PINJOL_BULAN:
            p.append("'{}': bunga {}/bulan melebihi batas pinjol konsumtif berizin OJK (0,1%/hari ~ 3%/bulan, "
                     "berlaku 2026). Curigai PINJOL ILEGAL: cek legalitas di ojk.go.id, Kontak OJK 157, "
                     "atau WA 081-157-157-157.".format(u.nama, persen(pb, 2)))
        if not getattr(u.bunga, "eksplisit", True) and u.bunga.pct > 0:
            p.append("'{}': bunga '{}' tanpa satuan DIANGGAP {}/tahun. Jika maksudnya per bulan, tulis '{}/bln' "
                     "(hasil akan sangat berbeda).".format(u.nama, u.bunga.asli, _fmt_pct(u.bunga.pct),
                                                           _fmt_pct(u.bunga.pct)))
        if u.jenis in ("kta", "motor", "mobil") and getattr(u.bunga, "tanda", None) != "efektif":
            p.append("'{}': bila bunganya FLAT, ubah dulu ke bunga efektif dengan subperintah konversi-flat; "
                     "simulasi ini menghitung bunga dari SISA saldo (efektif). Bila sudah efektif, tandai dengan "
                     "kata 'efektif' (mis. '1,6275%/bln efektif') agar catatan ini tidak muncul.".format(u.nama))
    total_b1 = sum((u.bunga.bunga_dari(u.saldo) for u in daftar), NOL)
    if anggaran <= total_b1:
        p.append("Anggaran pelunasan {} <= total bunga bulan pertama {}. Dengan anggaran ini utang tidak "
                 "akan berkurang. Naikkan anggaran atau hubungi kreditur untuk restrukturisasi.".format(
                     rp(anggaran), rp(total_b1)))
    return p


def cetak_hasil_metode(h, daftar):
    nama = {"avalanche": "AVALANCHE (bunga tertinggi dulu)", "snowball": "SNOWBALL (saldo terkecil dulu)"}
    out = ["## {}".format(nama[h["metode"]]), "",
           "Urutan serangan: " + " -> ".join(daftar[i].nama for i in h["prioritas"]), "",
           "| Utang | Saldo awal | Bunga | Lunas bulan ke- | Total bunga |", "|---|---:|---|---:|---:|"]
    for i, u in enumerate(daftar):
        out.append("| {} | {} | {} {} | {} | {} |".format(
            u.nama, rp(u.saldo), _fmt_pct(u.bunga.pct), u.bunga.periode,
            h["lunas"][i] if h["lunas"][i] is not None else "belum lunas", rp(h["bunga_per"][i])))
    if h["bulan"] is None:
        out.append("")
        if h["macet"]:
            out.append("**TIDAK AKAN LUNAS dengan anggaran ini:** pada bulan ke-{} total utang tidak berkurang "
                       "(bunga >= pembayaran). Sisa saldo: {}.".format(h["bulan_macet"], rp(sum(h["sisa_saldo"], NOL))))
        else:
            out.append("**TIDAK LUNAS dalam {} bulan.** Sisa saldo: {}.".format(
                BATAS_BULAN_SIMULASI, rp(sum(h["sisa_saldo"], NOL))))
    else:
        out.append("")
        out.append("**Semua lunas dalam {} bulan (~{} th {} bln). Total bunga {}. Total dibayar {}.**".format(
            h["bulan"], h["bulan"] // 12, h["bulan"] % 12, rp(h["total_bunga"]), rp(h["total_bayar"])))
    return out


def cetak_jadwal(h):
    out = ["", "### Jadwal bulanan ({})".format(h["metode"]), "",
           "| Bulan | Utang | Bayar | Bunga | Pokok | Sisa saldo |", "|---:|---|---:|---:|---:|---:|"]
    for bl, nm, bayar, bunga, pokok, sisa in h["jadwal"]:
        out.append("| {} | {} | {} | {} | {} | {} |".format(bl, nm, rp(bayar), rp(bunga), rp(pokok), rp(sisa)))
    return out


def cetak_utang(args):
    if not args.utang:
        raise InputSalah("Isi minimal satu --utang \"nama;saldo;bunga;cicilan_minimum[;jenis]\".")
    daftar = [parse_utang(t, args.per) for t in args.utang]
    total_min = sum((u.minimum for u in daftar if u.saldo > 0), NOL)
    if args.anggaran is not None and args.ekstra is not None:
        raise InputSalah("Pakai salah satu: --anggaran (total bayar semua utang per bulan) ATAU --ekstra.")
    if args.anggaran is not None:
        anggaran = parse_rupiah(args.anggaran, "Anggaran pelunasan per bulan")
        if anggaran < total_min:
            raise InputSalah("Anggaran {} lebih kecil dari total cicilan minimum {}. Minimal harus {} "
                             "agar tidak telat bayar.".format(rp(anggaran), rp(total_min), rp(total_min)))
    else:
        anggaran = total_min + parse_rupiah(args.ekstra or "0", "Ekstra per bulan")
    out = ["# Rencana Pelunasan Utang", "",
           "- Total cicilan minimum: {} | Anggaran pelunasan: {}/bulan (ekstra {})".format(
               rp(total_min), rp(anggaran), rp(anggaran - total_min)),
           "- Asumsi: bunga dihitung dari sisa saldo tiap bulan (efektif), dibulatkan ke rupiah terdekat; "
           "bunga per tahun dibagi 12, per hari dikali 30; tidak ada utang/belanja baru, denda, atau biaya lain; "
           "anggaran tetap dan cicilan minimum utang yang lunas dialihkan ke utang berikutnya.", ""]
    per = peringatan_utang(daftar, anggaran)
    if per:
        out += ["## PERINGATAN", ""] + ["- " + x for x in per] + [""]
    metode = ["avalanche", "snowball"] if args.metode == "banding" else [args.metode]
    hasil = [simulasi(daftar, anggaran, m) for m in metode]
    for h in hasil:
        out += cetak_hasil_metode(h, daftar) + [""]
    if len(hasil) == 2:
        a, s = hasil
        out += ["## Banding", ""]
        if a["bulan"] is not None and s["bulan"] is not None:
            hemat = s["total_bunga"] - a["total_bunga"]
            pertama_a = min(x for x in a["lunas"] if x is not None)
            pertama_s = min(x for x in s["lunas"] if x is not None)
            out.append("- Avalanche menghemat bunga {} dibanding Snowball; lama lunas {} vs {} bulan.".format(
                rp(hemat), a["bulan"], s["bulan"]))
            out.append("- Utang pertama lunas: bulan ke-{} (Avalanche) vs bulan ke-{} (Snowball).".format(
                pertama_a, pertama_s))
            if hemat > 0:
                out.append("- Pilih Avalanche jika disiplin & ingin paling hemat. Pilih Snowball jika butuh "
                           "kemenangan cepat agar semangat; selisih biayanya {}.".format(rp(hemat)))
            else:
                out.append("- Kedua metode sama biayanya untuk kasus ini; pilih yang paling mudah dijalani.")
        else:
            out.append("- Setidaknya satu metode tidak lunas dengan anggaran ini. Naikkan anggaran dulu, "
                       "atau minta restrukturisasi resmi ke kreditur.")
    if args.jadwal:
        for h in hasil:
            out += cetak_jadwal(h)
    out += ["", "Jangan menutup utang dengan utang baru (gali lubang tutup lubang). Kesulitan bayar? Hubungi "
            "kreditur untuk restrukturisasi secara resmi; pengaduan: Kontak OJK 157.",
            "Ditawari take over/refinancing/konsolidasi? Bandingkan TOTAL bunga sisa utang lama (tabel di atas) "
            "dengan total bunga pinjaman baru (bunga efektif + tenor baru) DITAMBAH biaya provisi/admin/asuransi "
            "dan penalti pelunasan dipercepat utang lama. Tenor lebih panjang membuat cicilan ringan tetapi "
            "total bunga bisa lebih besar."]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 4. Konversi bunga flat -> efektif
# ---------------------------------------------------------------------------

def nilai_kini_anuitas(cicilan, r, n):
    if r == 0:
        return cicilan * n
    return cicilan * (1 - (1 + r) ** (-n)) / r


def cari_bunga_efektif_bulanan(pokok, cicilan, n):
    """Bisection: r bulanan sehingga PV anuitas(cicilan, r, n) = pokok."""
    if cicilan * n <= pokok:
        return NOL
    lo, hi = NOL, Decimal("1")
    for _ in range(200):
        mid = (lo + hi) / 2
        if nilai_kini_anuitas(cicilan, mid, n) > pokok:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def parse_bunga_flat(teks, per):
    """Bunga flat -> (Bunga, ambigu). Terima '10,8', '10,8%/thn', '0,9%/bln', '0,9% per bulan'."""
    nama = "Bunga flat"
    b = terapkan_per(parse_bunga(teks, nama), per, nama)
    if b.tanda == "efektif":
        raise InputSalah("{} '{}' ditandai EFEKTIF. Subperintah ini mengubah bunga FLAT ke efektif; bunga efektif "
                         "bisa langsung dipakai di subperintah utang.".format(nama, teks))
    ambigu = (not b.eksplisit) and 0 < b.pct < BATAS_BUNGA_TANPA_SATUAN
    return b, ambigu


def _blok_flat(pokok, n, b, sudah_bayar, judul=None):
    """Satu tafsiran bunga flat. b: Bunga (periode diketahui). Kembalikan (baris, r_bulanan)."""
    flat_th = b.per_bulan_persen() * 12            # persen flat per tahun
    bunga_bln = bulat(pokok * flat_th / 1200)
    pokok_bln = pokok / n
    cicilan = bulat(pokok_bln + pokok * flat_th / 1200)
    out = []
    if judul:
        out += ["## " + judul, ""]
    if b.kode == "th":
        teks_bunga = "{}/tahun".format(_fmt_pct(b.pct))
    elif b.kode == "bln":
        teks_bunga = "{}/bulan (= {}/tahun)".format(_fmt_pct(b.pct), _fmt_pct(flat_th))
    else:
        teks_bunga = "{}/hari x 30 hari (= {}/tahun)".format(_fmt_pct(b.pct), _fmt_pct(flat_th))
    out.append("- Pokok {}, bunga flat {}, tenor {} bulan".format(rp(pokok), teks_bunga, n))
    out.append("- Rumus flat: cicilan = pokok/tenor + pokok x bunga_flat/12 = {} + {} = **{}**".format(
        rp(pokok_bln), rp(bunga_bln), rp(cicilan)))
    return out + _blok_efektif(pokok, n, cicilan, sudah_bayar)


def _blok_efektif(pokok, n, cicilan, sudah_bayar):
    total = cicilan * n
    total_bunga = total - pokok
    if total_bunga < 0:
        raise InputSalah("Total cicilan {} lebih kecil dari pokok {}. Periksa angka.".format(rp(total), rp(pokok)))
    r = cari_bunga_efektif_bulanan(pokok, cicilan, n)
    out = ["- Total dibayar {} | total bunga {}".format(rp(total), rp(total_bunga)),
           "- **Bunga efektif setara: {}/bulan = {}/tahun**".format(persen(r * 100, 3), persen(r * 1200, 2)),
           "- Untuk subperintah utang (lebih presisi): {}/bln".format(persen(r * 100, 4)),
           "", "Artinya: pinjaman ini sama mahalnya dengan pinjaman berbunga efektif {}/tahun (bunga dihitung "
           "dari sisa pokok). Bandingkan penawaran selalu dengan bunga EFEKTIF, bukan flat.".format(
               persen(r * 1200, 2))]
    if sudah_bayar is not None:
        sisa = bulat(nilai_kini_anuitas(cicilan, r, n - sudah_bayar))
        out += ["", "- Setelah {} kali bayar, perkiraan sisa pokok (metode efektif): **{}** untuk {} cicilan "
                "tersisa. Pakai angka ini + bunga efektif di subperintah utang. Nilai pelunasan dipercepat "
                "resmi bisa berbeda (ada penalti/aturan kontrak) - tanyakan ke kreditur.".format(
                    sudah_bayar, rp(sisa), n - sudah_bayar)]
    return out


def cetak_konversi_flat(args):
    pokok = cek_nominal_kecil(parse_rupiah(args.pokok, "Pokok pinjaman", boleh_nol=False), args.pokok,
                              "Pokok pinjaman")
    try:
        n = int(args.tenor)
    except (TypeError, ValueError):
        raise InputSalah("Tenor '{}' harus bilangan bulat bulan, mis. 24.".format(args.tenor))
    if n <= 0 or n > 600:
        raise InputSalah("Tenor harus 1-600 bulan.")
    if args.cicilan is None and args.bunga_flat is None:
        raise InputSalah("Isi --bunga-flat dengan satuan jelas (mis. '10,8%/th' atau '0,9%/bln') atau "
                         "--cicilan (cicilan per bulan dari kontrak).")
    k = None
    if args.sudah_bayar is not None:
        try:
            k = int(args.sudah_bayar)
        except ValueError:
            raise InputSalah("--sudah-bayar harus bilangan bulat.")
        if k < 0 or k >= n:
            raise InputSalah("--sudah-bayar harus 0 sampai {} (kurang dari tenor).".format(n - 1))
    out = ["# Konversi Bunga Flat -> Efektif", ""]
    if args.cicilan is not None:
        cicilan = parse_rupiah(args.cicilan, "Cicilan per bulan", boleh_nol=False)
        out.append("- Pokok {}, cicilan {}/bulan x {} bulan (dari kontrak)".format(rp(pokok), rp(cicilan), n))
        return "\n".join(out + _blok_efektif(pokok, n, cicilan, k))
    b, ambigu = parse_bunga_flat(args.bunga_flat, args.per)
    if ambigu:
        x = _fmt_pct(b.pct)
        out += ["## PERINGATAN: satuan bunga tidak disebut", "",
                "- '{}' bisa berarti {} per BULAN atau {} per TAHUN - hasilnya berbeda jauh. Untuk KTA/kredit "
                "di Indonesia, angka di bawah 3 hampir selalu per BULAN. Kedua tafsiran ditampilkan di bawah; "
                "PASTIKAN ke pengguna/kontrak, lalu ulangi dengan '{}/bln' atau '{}/th' (atau --per bulan / "
                "--per tahun). Jangan memakai hasil sebelum satuan dipastikan.".format(args.bunga_flat, x, x, x, x),
                ""]
        out += _blok_flat(pokok, n, buat_bunga(b.pct, "bln", "Bunga flat", b.asli),
                          k, "Tafsiran A: {} per BULAN (paling mungkin)".format(x))
        out += [""] + _blok_flat(pokok, n, buat_bunga(b.pct, "th", "Bunga flat", b.asli),
                                 k, "Tafsiran B: {} per TAHUN".format(x))
        return "\n".join(out)
    out += _blok_flat(pokok, n, b, k)
    if not b.eksplisit and b.pct > 0:
        out += ["", "Catatan: '{}' tanpa satuan DIANGGAP {}/tahun. Jika di kontrak tertulis per bulan, ulangi "
                "dengan '{}/bln'.".format(args.bunga_flat, _fmt_pct(b.pct), _fmt_pct(b.pct))]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 5. Target keuangan
# ---------------------------------------------------------------------------

def hitung_target(biaya_sekarang, bulan, inflasi, imbal, terkumpul):
    i_bln = inflasi / 1200
    r = imbal / 1200
    biaya_nanti = bulat(biaya_sekarang * (1 + i_bln) ** bulan)
    tumbuh = terkumpul * (1 + r) ** bulan
    kurang = biaya_nanti - tumbuh
    if kurang <= 0:
        return biaya_nanti, bulat(tumbuh), NOL
    if r == 0:
        pmt = kurang / bulan
    else:
        pmt = kurang * r / ((1 + r) ** bulan - 1)
    return biaya_nanti, bulat(tumbuh), bulat_atas(pmt)


def bulan_sampai_target(biaya_sekarang, inflasi, imbal, terkumpul, setoran, batas=720):
    """Bulan pertama m (setor akhir bulan) saat tabungan >= biaya ikut inflasi. None bila > batas."""
    i_bln = inflasi / 1200
    r = imbal / 1200
    if terkumpul >= bulat(biaya_sekarang):
        return 0, bulat(biaya_sekarang)
    tab = terkumpul
    for m in range(1, batas + 1):
        tab = tab * (1 + r) + setoran
        nanti = bulat(biaya_sekarang * (1 + i_bln) ** m)
        if tab >= nanti:
            return m, nanti
    return None, None


def cetak_target(args):
    if args.jenis == "pensiun":
        if args.pengeluaran_bulanan is None:
            raise InputSalah("Untuk pensiun isi --pengeluaran-bulanan (nilai uang SEKARANG) dan --lama-pensiun.")
        belanja = cek_nominal_kecil(
            parse_rupiah(args.pengeluaran_bulanan, "Pengeluaran bulanan saat pensiun", boleh_nol=False),
            args.pengeluaran_bulanan, "Pengeluaran bulanan saat pensiun")
        try:
            lama = int(args.lama_pensiun)
        except (TypeError, ValueError):
            raise InputSalah("--lama-pensiun harus bilangan bulat tahun, mis. 20.")
        if lama <= 0 or lama > 50:
            raise InputSalah("--lama-pensiun harus 1-50 tahun.")
        biaya = belanja * 12 * lama
    else:
        if args.biaya_sekarang is None:
            raise InputSalah("Isi --biaya-sekarang (harga target bila dibeli hari ini).")
        biaya = cek_nominal_kecil(parse_rupiah(args.biaya_sekarang, "Biaya sekarang", boleh_nol=False),
                                  args.biaya_sekarang, "Biaya sekarang")
    if args.bulan is not None and args.tahun is not None:
        raise InputSalah("Pakai salah satu: --tahun atau --bulan.")
    try:
        bulan = int(args.bulan) if args.bulan is not None else (
            int(Decimal(str(args.tahun).replace(",", ".")) * 12) if args.tahun is not None else None)
    except (ValueError, ArithmeticError):
        raise InputSalah("Jangka waktu harus angka (tahun atau bulan).")
    if bulan is None:
        raise InputSalah("Isi jangka waktu: --tahun (mis. 5) atau --bulan (mis. 36).")
    if bulan <= 0 or bulan > 720:
        raise InputSalah("Jangka waktu harus 1 bulan sampai 60 tahun.")
    inflasi = parse_persen_tahunan(args.inflasi, "Inflasi")
    imbal = parse_persen_tahunan(args.imbal, "Imbal hasil") if args.imbal is not None else NOL
    terkumpul = cek_nominal_kecil(parse_rupiah(args.terkumpul, "Dana terkumpul"), args.terkumpul, "Dana terkumpul")
    nanti, tumbuh, pmt = hitung_target(biaya, bulan, inflasi, imbal, terkumpul)
    out = ["# Target: {}".format(args.nama), "",
           "| Asumsi | Nilai |", "|---|---:|",
           "| {} | {} |".format("Kebutuhan dana pensiun (nilai hari ini)" if args.jenis == "pensiun"
                                 else "Biaya bila dibeli hari ini", rp(biaya)),
           "| Jangka waktu | {} bulan (~{} th {} bln) |".format(bulan, bulan // 12, bulan % 12),
           "| Inflasi (asumsi, per tahun) | {} |".format(_fmt_pct(inflasi)),
           "| Imbal hasil tabungan (asumsi, per tahun) | {} |".format(_fmt_pct(imbal)),
           "| Dana sudah terkumpul | {} |".format(rp(terkumpul)), "",
           "| Hasil | Nilai |", "|---|---:|",
           "| Perkiraan biaya saat dibutuhkan | **{}** |".format(rp(nanti)),
           "| Dana terkumpul pada saat itu | {} |".format(rp(tumbuh)),
           "| **Tabungan yang dibutuhkan per bulan** | **{}** |".format(rp(pmt))]
    if args.jenis == "pensiun":
        out.append("")
        out.append("Pensiun: kebutuhan = pengeluaran bulanan x 12 x {} tahun (nilai hari ini), lalu dinaikkan "
                   "inflasi. Asumsi sederhana: selama pensiun imbal hasil sama dengan inflasi. Kurangi dengan "
                   "perkiraan JHT/JP BPJS atau pensiun kantor bila ada (isi di --terkumpul).".format(lama))
    cukup_sekarang = terkumpul >= bulat(biaya)
    if cukup_sekarang:
        out += ["", "**Dana terkumpul {} sudah cukup untuk harga sekarang {}** (bila dibeli/dibayar sekarang).".format(
            rp(terkumpul), rp(biaya))]
        if pmt > 0:
            out.append("Bila menunggu {} bulan, biaya diperkirakan naik menjadi {} karena inflasi, sedangkan dana "
                       "menjadi {}: perlu tambahan tabungan {} per bulan.".format(bulan, rp(nanti), rp(tumbuh),
                                                                                   rp(pmt)))
        else:
            out.append("Bila menunggu {} bulan pun dana diperkirakan tetap cukup ({} vs biaya {}).".format(
                bulan, rp(tumbuh), rp(nanti)))
    if args.kemampuan is not None:
        mampu = parse_rupiah(args.kemampuan, "Kemampuan menabung per bulan")
        if cukup_sekarang:
            if pmt > 0 and mampu < pmt:
                out.append("Bila menunggu, kemampuan {} per bulan kurang {} dari tambahan yang dibutuhkan.".format(
                    rp(mampu), rp(pmt - mampu)))
            elif pmt > 0:
                out.append("Bila menunggu, kemampuan {} per bulan cukup (sisa {}).".format(rp(mampu),
                                                                                     rp(mampu - pmt)))
        elif mampu < pmt:
            out += ["", "**Kurang {} per bulan** dari kemampuan {}. Pilihan: perpanjang waktu, turunkan target, "
                    "atau tambah pemasukan.".format(rp(pmt - mampu), rp(mampu))]
        else:
            out += ["", "Kemampuan {} per bulan cukup (sisa {}).".format(rp(mampu), rp(mampu - pmt))]
        m, nanti_m = (0, None) if cukup_sekarang else bulan_sampai_target(biaya, inflasi, imbal, terkumpul, mampu)
        if m == 0:
            pass    # sudah dijelaskan di atas (cukup untuk harga sekarang)
        elif m is None:
            out.append("Dengan menabung {}/bulan, target TIDAK tercapai dalam 60 tahun (kenaikan biaya karena "
                       "inflasi lebih cepat dari tabungan). Naikkan setoran atau turunkan target.".format(rp(mampu)))
        else:
            out.append("**Dengan menabung {}/bulan, target tercapai di bulan ke-{} (~{} th {} bln)**, saat "
                       "biayanya diperkirakan {} (asumsi inflasi & imbal hasil yang sama).".format(
                           rp(mampu), m, m // 12, m % 12, rp(nanti_m)))
    out += ["", "Rumus: biaya_nanti = biaya x (1 + inflasi/12)^bulan; tabungan/bulan = (biaya_nanti - "
            "terkumpul x (1+r)^bulan) x r / ((1+r)^bulan - 1), r = imbal/12 (jika r = 0: dibagi jumlah bulan). "
            "Setoran di akhir bulan, dibulatkan ke atas. Angka inflasi & imbal hasil adalah ASUMSI, bukan janji; "
            "tidak ada rekomendasi produk investasi."]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("Input belum benar: {}\nLihat bantuan: python3 keuangan.py {} -h\n".format(
            message, "<subperintah>"))
        sys.exit(2)


def buat_parser():
    ap = Parser(description="Alat hitung keuangan pribadi & keluarga (Rupiah). Bukan nasihat keuangan.")
    sub = ap.add_subparsers(dest="perintah", parser_class=Parser)
    sub.required = True

    a = sub.add_parser("anggaran", help="Anggaran bulanan zero-based + banding 50/30/20")
    a.add_argument("--pemasukan", action="append", help="Pemasukan BERSIH per bulan, 'nama=jumlah' (boleh berulang)")
    a.add_argument("--musiman", action="append", help="Pemasukan TAHUNAN (THR/bonus), 'nama=jumlah' - dibagi 12")
    a.add_argument("--pos", action="append", help="Pos 'nama=jumlah[:wajib|sosial|keinginan|tabungan]' (berulang)")
    a.add_argument("--pola", default="50/30/20", help="Pola kebutuhan/keinginan/tabungan, mis. 60/20/20")

    d = sub.add_parser("dana-darurat", help="Target dana darurat sesuai status")
    d.add_argument("--pengeluaran-pokok", default=None,
                   help="Pengeluaran pokok per bulan (gabungan). Boleh diganti/ditambah --pos dan --cicilan")
    d.add_argument("--pos", action="append", help="Rincian pos pokok 'nama=jumlah' (berulang)")
    d.add_argument("--cicilan", action="append",
                   help="Cicilan/utang minimum 'nama=jumlah' (PayLater, kartu kredit, KPR, pinjol; berulang) - "
                        "ditambahkan ke pengeluaran pokok")
    d.add_argument("--status", required=True, choices=sorted(STATUS_DANA_DARURAT))
    d.add_argument("--saldo", default="0", help="Dana darurat yang sudah ada")
    d.add_argument("--setoran", default="0", help="Setoran rutin per bulan")

    u = sub.add_parser("utang", help="Pelunasan utang avalanche/snowball/banding")
    u.add_argument("--utang", action="append", help="'nama;saldo;bunga;cicilan_minimum[;jenis]' (berulang)")
    u.add_argument("--ekstra", default=None, help="Uang tambahan di atas total cicilan minimum per bulan")
    u.add_argument("--anggaran", default=None, help="ATAU total uang untuk semua utang per bulan")
    u.add_argument("--metode", default="banding", choices=["avalanche", "snowball", "banding"])
    u.add_argument("--jadwal", action="store_true", help="Tampilkan jadwal bulanan lengkap")
    u.add_argument("--per", default=None, choices=["bulan", "tahun", "hari"],
                   help="Satuan untuk bunga yang ditulis TANPA satuan (mis. '2' -> 2%%/bln bila --per bulan)")

    k = sub.add_parser("konversi-flat", help="Bunga flat -> efektif setara")
    k.add_argument("--pokok", required=True)
    k.add_argument("--tenor", required=True, help="Jumlah bulan")
    k.add_argument("--bunga-flat", default=None,
                   help="Bunga flat DENGAN satuan: '10,8%%/th' atau '0,9%%/bln' (tanpa satuan: >=3 dianggap per "
                        "tahun; <3 ditampilkan dua tafsiran)")
    k.add_argument("--per", default=None, choices=["bulan", "tahun", "hari"],
                   help="Satuan --bunga-flat bila tidak ditulis di angkanya")
    k.add_argument("--cicilan", default=None, help="ATAU cicilan per bulan dari kontrak")
    k.add_argument("--sudah-bayar", default=None, help="Jumlah cicilan yang sudah dibayar (opsional)")

    t = sub.add_parser("target", help="Tabungan bulanan untuk target keuangan")
    t.add_argument("--nama", default="Target keuangan")
    t.add_argument("--jenis", default="umum", choices=["umum", "rumah", "pendidikan", "haji", "umrah", "pensiun"])
    t.add_argument("--biaya-sekarang", default=None)
    t.add_argument("--tahun", default=None)
    t.add_argument("--bulan", default=None)
    t.add_argument("--inflasi", default="4", help="Asumsi inflasi %%/tahun (bawaan 4)")
    t.add_argument("--imbal", default=None, help="Asumsi imbal hasil %%/tahun (bawaan 0)")
    t.add_argument("--terkumpul", default="0")
    t.add_argument("--kemampuan", default=None, help="Kemampuan menabung per bulan (opsional)")
    t.add_argument("--pengeluaran-bulanan", default=None, help="Khusus pensiun: nilai hari ini")
    t.add_argument("--lama-pensiun", default="20", help="Khusus pensiun: tahun (bawaan 20)")
    return ap


def gabung_nilai_negatif(argv):
    """'--saldo -500rb' -> '--saldo=-500rb' agar pesan galat berbahasa Indonesia ('tidak boleh negatif'),
    bukan pesan argparse berbahasa Inggris."""
    hasil, i = [], 0
    while i < len(argv):
        a = argv[i]
        if (a.startswith("--") and "=" not in a and i + 1 < len(argv)
                and re.match(r"^-(\d|rp|idr)", argv[i + 1].strip().lower())):
            hasil.append(a + "=" + argv[i + 1])
            i += 2
            continue
        hasil.append(a)
        i += 1
    return hasil


def main(argv=None):
    del PERINGATAN_INPUT[:]
    argv = gabung_nilai_negatif(list(sys.argv[1:] if argv is None else argv))
    args = buat_parser().parse_args(argv)
    fungsi = {"anggaran": cetak_anggaran, "dana-darurat": cetak_dana_darurat, "utang": cetak_utang,
              "konversi-flat": cetak_konversi_flat, "target": cetak_target}[args.perintah]
    try:
        teks = fungsi(args)
    except InputSalah as e:
        sys.stderr.write("Input belum benar: {}\n".format(e))
        return 2
    except KeyboardInterrupt:
        return 130
    except Exception as e:  # jaring pengaman: tidak menampilkan traceback ke pengguna awam
        sys.stderr.write("Terjadi kesalahan tak terduga ({}). Periksa format input atau hitung manual "
                         "dengan rumus di SKILL.md.\n".format(type(e).__name__))
        return 3
    if PERINGATAN_INPUT:
        teks = "\n".join(["## PERINGATAN INPUT (periksa dulu)", ""] + ["- " + x for x in PERINGATAN_INPUT]
                         + [""]) + "\n" + teks
    try:
        sys.stdout.write(teks + "\n")
    except UnicodeEncodeError:
        sys.stdout.write(teks.encode("ascii", "replace").decode("ascii") + "\n")
    sys.stdout.write("\nBukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan "
                     "bersertifikat.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
