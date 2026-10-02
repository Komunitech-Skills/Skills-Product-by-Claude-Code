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


KATA_KELUARGA = ("kiriman", "orang tua", "ortu", "mertua", "keluarga", "adik", "kakak", "nenek", "kakek",
                 "ibu", "bapak", "ayah", "mama", "papa", "emak", "tanggungan", "uang bulanan")
KATA_INVESTASI = ("indodax", "kripto", "crypto", "saham", "reksa", "emas", "investasi", "tokocrypto", "pintu",
                  "bibit", "ajaib", "deposito")


def adalah_keluarga(nama):
    """Kiriman/tanggungan keluarga rutin (ortu, mertua, adik) -> kewajiban rutin keluarga (masuk pokok bawaan)."""
    n = nama.lower()
    return any(re.search(r"(?<![a-z])" + re.escape(k), n) for k in KATA_KELUARGA)


def alasan_bukan_pokok(nama, kel):
    n = nama.lower()
    if any(k in n for k in KATA_INVESTASI):
        return "top-up investasi/tabungan, bukan biaya hidup - bisa dihentikan saat penghasilan berhenti"
    if "arisan" in n:
        return "arisan = tabungan berputar; tambahkan ke pokok bila setorannya wajib dan tidak bisa berhenti"
    if kel == "tabungan":
        return "tabungan/dana darurat/pelunasan ekstra, bukan biaya hidup"
    if kel == "sosial":
        return "sosial/ibadah sukarela, bisa ditunda saat darurat - tambahkan bila memang wajib"
    if kel == "keinginan":
        return "keinginan/jajan/hiburan, bisa dikurangi atau dihentikan saat darurat"
    return "belum dikelompokkan - tanyakan ke pengguna apakah wajib"


def adalah_cicilan(nama):
    """Pos cicilan/utang (PayLater, kartu kredit, KPR, pinjol, leasing, KTA) -> selalu masuk pengeluaran pokok."""
    n = nama.lower()
    if "ekstra" in n or "pelunasan" in n:   # setoran tambahan = tabungan/pelunasan, bukan kewajiban minimum
        return False
    return any(k in n for k in KATA_CICILAN)


def tebak_kelompok(nama):
    n = nama.lower()
    if adalah_cicilan(nama):   # v1.0.6: "Shopee PayLater" = cicilan (wajib), bukan belanja Shopee (keinginan)
        return "wajib"
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


def jenis_pokok(nama, kel):
    """Kembalikan jenis pokok ('cicilan'|'keluarga'|'wajib') atau None bila bukan pokok (aturan bawaan)."""
    if adalah_cicilan(nama):
        return "cicilan"
    if kel == "wajib":
        return "wajib"
    if kel == "sosial" and adalah_keluarga(nama):
        return "keluarga"
    return None


def hitung_anggaran(pemasukan, musiman, pos, pola, pokok_juga=(), bukan_pokok=()):
    """pemasukan/musiman: list (nama, Decimal); pos: list (nama, nilai, kelompok, ditebak).
    pokok_juga/bukan_pokok: nama pos yang dimasukkan/dikeluarkan dari pokok atas keputusan pengguna."""
    juga = set(x.strip().lower() for x in pokok_juga)
    bukan = set(x.strip().lower() for x in bukan_pokok)
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
    # v1.0.6: + kewajiban rutin keluarga (kiriman ortu/mertua/adik) secara bawaan; setiap pos yang TIDAK
    # dihitung pokok dicatat beserta alasannya, agar tidak ada pos yang hilang diam-diam.
    pokok_rinci, pokok_keluar = [], []
    for nm, n, kel, _ in pos:
        if n <= 0:
            continue
        jenis = jenis_pokok(nm, kel)
        if nm.strip().lower() in bukan:
            pokok_keluar.append((nm, n, "dikeluarkan atas keputusan pengguna"))
        elif nm.strip().lower() in juga:
            pokok_rinci.append((nm, n, jenis or "pengguna"))
        elif jenis:
            pokok_rinci.append((nm, n, jenis))
        else:
            pokok_keluar.append((nm, n, alasan_bukan_pokok(nm, kel)))
    pokok = sum((n for _, n, _ in pokok_rinci), NOL)
    # v1.0.7 (uji Telegram 2026-10-02): pisahkan arus RUTIN (gaji tiap bulan) dari MUSIMAN (THR/bonus cair
    # sekali). Setoran/transfer bulanan hanya boleh dari sisa rutin; THR dicadangkan saat cair (tidak dihitung
    # dua kali). Rasio cicilan memakai pemasukan rutin karena THR tidak ada tiap bulan.
    sisa_rutin = total_bulanan - total_keluar
    tambal = max(-sisa_rutin, NOL)                     # kekurangan rutin per bulan yang harus ditutup THR
    basis_cicilan = total_bulanan if total_bulanan > 0 else total_masuk
    return {
        "sisa_rutin": sisa_rutin, "tambal_musiman_per_bulan": tambal,
        "tambal_musiman_setahun": tambal * 12, "musiman_bebas_setahun": total_musiman - tambal * 12,
        "bulan_ditambal_musiman": (int((total_musiman / tambal).to_integral_value(rounding=ROUND_FLOOR))
                                   if tambal > 0 else None),
        "basis_cicilan": basis_cicilan, "basis_cicilan_rutin": total_bulanan > 0,
        "pokok_dana_darurat": pokok, "pokok_rinci": pokok_rinci, "pokok_keluar": pokok_keluar,
        "total_bulanan": total_bulanan, "total_musiman": total_musiman,
        "musiman_per_bulan": musiman_per_bulan, "total_masuk": total_masuk,
        "per_kelompok": per_kelompok, "total_keluar": total_keluar, "sisa": sisa,
        "kebutuhan": kebutuhan, "keinginan": keinginan, "tabungan": tabungan,
        "cicilan": cicilan,
        "basis_pola": basis_cicilan,
        # v1.0.8: banding pola memakai basis yang SAMA dengan rasio cicilan (pemasukan rutin, tanpa THR/12),
        # agar batas tabungan tidak dibandingkan dengan setoran rutin yang tidak memuat THR.
        "target_pola": [bulat(basis_cicilan * p / 100) for p in pola],
    }


KATA_FLEKSIBEL = ("dapur", "makan", "sembako", "belanja", "listrik", "token", "pdam", "air", "gas", "lpg",
                  "pulsa", "kuota", "internet", "wifi", "bensin", "transport", "ojek", "parkir", "galon",
                  "jajan", "laundry", "sabun", "toiletries")
KATA_TIDAK_FLEKSIBEL = ("sewa", "kontrakan", "kos", "kost", "kpr", "sekolah", "spp", "bpjs", "asuransi",
                        "daycare", "obat", "kesehatan", "susu", "popok", "pampers", "iuran", "ipl", "les")
KATA_IBADAH = ("zakat", "perpuluhan", "persembahan", "kolekte", "punia", "infak", "infaq", "sedekah")
# Tahap pemangkasan bertahap (urutan, batas potong maks. per pos): keinginan dulu, lalu kebutuhan yang
# fleksibel (dapur, pulsa, bensin, listrik), lalu sosial non-ibadah & non-kiriman keluarga (kondangan, arisan).
TAHAP_PANGKAS = (("keinginan", Decimal("0.5"), "Keinginan (maks. 50% per pos)"),
                 ("fleksibel", Decimal("0.1"), "Kebutuhan fleksibel (maks. 10% per pos)"),
                 ("sosial", Decimal("0.5"), "Sosial non-ibadah (maks. 50% per pos, opsional)"))
KELIPATAN_PANGKAS = Decimal(10000)
LAMA_BERTAHAP = 3


def _ke_atas_kelipatan(x, k=KELIPATAN_PANGKAS):
    return (Decimal(x) / k).to_integral_value(rounding=ROUND_CEILING) * k


def _ke_bawah_kelipatan(x, k=KELIPATAN_PANGKAS):
    return (Decimal(x) / k).to_integral_value(rounding=ROUND_FLOOR) * k


def tahap_pangkas(nama, kel):
    n = nama.lower()
    if adalah_cicilan(nama) or kel == "tabungan":
        return None
    if kel in ("keinginan", "lain"):
        return "keinginan"
    if kel == "wajib":
        if any(k in n for k in KATA_TIDAK_FLEKSIBEL):
            return None
        return "fleksibel" if any(k in n for k in KATA_FLEKSIBEL) else None
    if kel == "sosial" and not adalah_keluarga(nama) and not any(k in n for k in KATA_IBADAH):
        return "sosial"
    return None


def rencana_pangkas(pemasukan_rutin, pos, tetap=()):
    """Rencana menutup defisit RUTIN (pos non-tabungan > pemasukan rutin) tanpa THR, lewat pemangkasan
    bertahap. Kembalikan dict: defisit (struktural, tanpa pos tabungan), setoran_maks (setoran tabungan
    bulanan yang benar-benar ada dari gaji), potong (list nama, sekarang, potongan, tahap), sisa_defisit."""
    non_tab = sum((n for _, n, kel, _ in pos if kel != "tabungan"), NOL)
    defisit = max(non_tab - pemasukan_rutin, NOL)
    setoran_maks = max(pemasukan_rutin - non_tab, NOL)
    potong, perlu = [], defisit
    for tahap, batas, _ in TAHAP_PANGKAS:
        if perlu <= 0:
            break
        kandidat = []
        for nm, n, kel, _ in pos:
            if nm not in tetap and tahap_pangkas(nm, kel) == tahap:
                cap = _ke_bawah_kelipatan(n * batas)
                if cap > 0:
                    kandidat.append((nm, n, cap))
        total_cap = sum((c for _, _, c in kandidat), NOL)
        if total_cap <= 0:
            continue
        for nm, n, cap in kandidat:
            if total_cap <= perlu:
                ptg = cap
            else:
                ptg = min(cap, _ke_atas_kelipatan(cap * perlu / total_cap))
            if ptg > 0:
                potong.append((nm, n, ptg, tahap))
        perlu -= min(total_cap, sum((p for _, _, p, t in potong if t == tahap), NOL))
    total_potong = sum((p for _, _, p, _ in potong), NOL)
    return {"defisit": defisit, "setoran_maks": setoran_maks, "potong": potong,
            "total_potong": total_potong, "sisa_defisit": max(defisit - total_potong, NOL),
            "lebih": max(total_potong - defisit, NOL)}


def potongan_bulan(potong, m, lama=LAMA_BERTAHAP):
    """Potongan yang sudah berjalan di bulan ke-m (bertahap: m/lama dari potongan penuh, kelipatan Rp10.000)."""
    if m >= lama:
        return sum((p for _, _, p, _ in potong), NOL)
    return sum((min(p, _ke_atas_kelipatan(p * m / lama)) for _, _, p, _ in potong), NOL)


def jadwal_defisit(rp_, musiman_total, bulan_cair, lama=LAMA_BERTAHAP):
    """Baris per bulan: (bulan, potongan berjalan, kekurangan bulan itu, kumulatif) sampai THR cair
    (atau sampai pemangkasan penuh bila tanpa THR)."""
    akhir = max(lama, bulan_cair if musiman_total > 0 else lama)
    baris, kum = [], NOL
    for m in range(1, akhir + 1):
        ptg = potongan_bulan(rp_["potong"], m, lama)
        kurang = max(rp_["defisit"] - ptg, NOL)
        kum += kurang
        baris.append((m, ptg, kurang, kum))
    return baris


def _fmt_lama(m):
    if m is None:
        return "tidak tercapai"
    if m == 0:
        return "sudah tercapai"
    return "{} bulan (~{} th {} bln)".format(m, m // 12, m % 12)


def pos_jeda(pos):
    """v1.0.10: pos kelompok tabungan yang di-NOL-kan selama defisit rutin. Kembalikan list (nama, jumlah, arisan?)."""
    return [(nm, n, "arisan" in nm.lower()) for nm, n, kel, _ in pos if kel == "tabungan" and n > 0]


def kalimat_jeda(jeda, alt, ada_thr, rinci):
    """v1.0.10: tindakan eksplisit untuk pos tabungan yang dijeda (arisan tidak boleh berhenti diam-diam)."""
    out = []
    for nm, n, arisan in jeda:
        if arisan:
            out.append("TINDAKAN: jeda {} {}/bulan selama defisit - bicarakan dengan pengelola arisan (izin cuti "
                       "sementara atau ambil giliran belakangan).".format(nm, rp(n)))
        else:
            out.append("TINDAKAN: hentikan sementara setoran {} {}/bulan sampai defisit tertutup.".format(nm, rp(n)))
    if alt is not None:
        nama = ", ".join(nm for nm, _, a in jeda if a)
        teks = "Bila {} tetap dibayar, kekurangan jadi {}/bulan (bukan {}); setelah pemangkasan penuh masih kurang " \
               "{}/bulan".format(nama, rp(alt["defisit"]), rp(alt["defisit_jeda"]), rp(alt["sisa_defisit"]))
        if alt["sebelum"] > 0:
            teks += ", dan kekurangan {} menjadi {} (bukan {})".format(
                "sebelum {} cair".format(rinci) if ada_thr else "masa transisi", rp(alt["sebelum"]),
                rp(alt["sebelum_jeda"]))
        out.append(teks + ".")
    return out


def analisis_defisit(h, pos, musiman, bulan_cair, saldo, saldo_diisi=True, sisih=None, tetap=(), _alt=True):
    """v1.0.9: hitung seluruh rencana defisit rutin SEKALI (dipakai bagian rencana dan RINGKASAN SIAP TEMPEL).
    Kembalikan None bila tidak ada defisit struktural (pos di luar tabungan <= gaji rutin).
    v1.0.10: pos tabungan yang di-nol-kan (arisan, setoran dana darurat) dicetak sebagai TINDAKAN eksplisit, dan
    untuk arisan dihitung juga kekurangan bila arisan tetap dibayar (`tetap` = nama pos yang tidak dipangkas).
    `sisih` = penyisihan kebutuhan Lebaran dari THR (diambil setelah kekurangan masa transisi tertutup)."""
    rp_ = rencana_pangkas(h["total_bulanan"], pos, tetap)
    if rp_["defisit"] <= 0:
        return None
    ada_thr = bool(musiman) and h["total_musiman"] > 0
    rinci = " + ".join(n for n, _ in musiman) or "THR/bonus"
    baris = jadwal_defisit(rp_, h["total_musiman"] if ada_thr else NOL, bulan_cair)
    pra = [b for b in baris if not ada_thr or b[0] < bulan_cair]       # bulan sebelum THR cair
    sebelum = sum((b[2] for b in pra), NOL)
    bulan_pra = [b[0] for b in pra if b[2] > 0]
    kalimat = []
    jeda = pos_jeda(pos) if _alt else []
    alt = None
    if any(a for _, _, a in jeda):
        arisan = set(nm for nm, _, a in jeda if a)
        pos_alt = [(nm, n, "wajib" if nm in arisan else kel, d) for nm, n, kel, d in pos]
        a2 = analisis_defisit(h, pos_alt, musiman, bulan_cair, saldo, saldo_diisi, sisih, arisan, _alt=False)
        alt = {"defisit": a2["rp"]["defisit"], "sisa_defisit": a2["rp"]["sisa_defisit"], "sebelum": a2["sebelum"],
               "defisit_jeda": rp_["defisit"], "sebelum_jeda": sebelum}
    kalimat += kalimat_jeda(jeda, alt, ada_thr, rinci)
    daftar = "; ".join("{} {} -> {}".format(nm, rp(n), rp(n - p)) for nm, n, p, _ in rp_["potong"])
    if rp_["potong"]:
        kalimat.append("TINDAKAN: defisit rutin {}/bulan ditutup dengan memangkas bertahap dalam {} bulan: {}.".format(
            rp(rp_["defisit"]), LAMA_BERTAHAP, daftar))
    if rp_["sisa_defisit"] > 0:
        kalimat.append("Pemangkasan dalam batas wajar BELUM cukup: setelah dipangkas penuh masih kurang {}/bulan "
                       "- perlu tambahan pemasukan rutin atau meninjau pos besar (tempat tinggal, cicilan), "
                       "bukan utang baru.".format(rp(rp_["sisa_defisit"])))
    # --- Kekurangan sebelum THR cair: cek saldo (v1.0.9, jangan menyuruh 'talangi dari saldo' bila saldo kurang)
    talangan = None
    if sebelum > 0:
        n_pra = len(pra)
        rentang = "bulan ke-{} s.d. ke-{}".format(bulan_pra[0], bulan_pra[-1]) if len(bulan_pra) > 1 else \
            "bulan ke-{}".format(bulan_pra[0])
        awal = "Selama masa transisi{} ({}) masih kurang total {}.".format(
            " sebelum {} cair".format(rinci) if ada_thr else "", rentang, rp(sebelum))
        if saldo >= sebelum:
            kalimat.append(awal + " Saldo tabungan {} cukup untuk menalanginya{} - jangan pakai paylater/pinjol."
                           .format(rp(saldo), "; ganti dari {} saat cair".format(rinci) if ada_thr else ""))
            talangan = {"cukup": True}
        else:
            kurang = sebelum - saldo
            cepat = rp_["sisa_defisit"] * n_pra             # pemangkasan penuh langsung mulai bulan ke-1
            hemat = sebelum - cepat
            per_bln = _ke_atas_kelipatan(kurang / len(bulan_pra))
            tunda = [nm for nm, n, kel, _ in pos if n > 0 and kel != "tabungan" and not adalah_cicilan(nm)
                     and (kel in ("keinginan", "lain") or (kel == "sosial" and not any(
                         x in nm.lower() for x in KATA_IBADAH)))]
            opsi = []
            if hemat > 0:
                opsi.append("(1) percepat pemangkasan - semua potongan langsung penuh mulai bulan ke-1, kekurangan "
                            "{} turun dari {} menjadi {}{}".format(
                                "sebelum {} cair".format(rinci) if ada_thr else "masa transisi", rp(sebelum), rp(cepat),
                                " (tidak perlu talangan)" if cepat <= 0 else (
                                    " (cukup ditalangi saldo)" if cepat <= saldo else "")))
            opsi.append("({}) tambah pemasukan sementara sekitar {}/bulan selama {} bulan (lembur, jualan kecil, "
                        "jasa, jual barang yang tidak terpakai)".format(len(opsi) + 1, rp(per_bln), len(bulan_pra)))
            if tunda:
                opsi.append("({}) tunda/kurangi sementara pos yang bisa ditunda: {}{}".format(
                    len(opsi) + 1, ", ".join(tunda),
                    " (kiriman keluarga hanya bila sudah dibicarakan baik-baik)"
                    if any(adalah_keluarga(x) for x in tunda) else ""))
            kalimat.append(awal + " Saldo tabungan sekarang {}{} TIDAK cukup (kurang {}). Pilihan tanpa utang: {}. "
                           "Jangan ditutup paylater/pinjol/kartu kredit.".format(
                               rp(saldo), "" if saldo_diisi else " (belum diisi, dianggap Rp0)", rp(kurang),
                               "; ".join(opsi)))
            talangan = {"cukup": False, "kurang": kurang, "cepat": cepat, "per_bulan": per_bln, "tunda": tunda}
    # --- Alokasi THR (v1.0.9: selama defisit rutin masih ada, sisa THR dicadangkan dulu untuk defisit)
    thr = None
    if ada_thr:
        sampai_cair = sum((b[2] for b in baris), NOL)
        bebas = h["total_musiman"] - sampai_cair
        akhir = len(baris)
        lebaran = min(sisih, max(bebas, NOL)) if sisih else NOL
        teks_leb = ""
        if sisih:
            teks_leb = "; lalu {} disisihkan untuk kebutuhan Lebaran{}".format(
                rp(lebaran), "" if lebaran == sisih else " (dari rencana {}, hanya itu yang tersisa)".format(rp(sisih)))
            bebas -= lebaran
        if bebas < 0:
            kalimat.append("{} {} tidak cukup menutup kekurangan masa transisi {} - percepat pemangkasan dan "
                           "tambah pemasukan.".format(rinci, rp(h["total_musiman"]), rp(sampai_cair)))
            thr = {"bebas": bebas, "cadangan": NOL, "bulan_cadangan": 0, "ke_dd": NOL, "lebaran": lebaran}
        elif rp_["sisa_defisit"] > 0:
            # cadangan menambal bulan setelah transisi sampai THR berikutnya cair (bulan_cair + 12)
            maks_bulan = bulan_cair + 12 - akhir - 1
            bln = int((bebas / rp_["sisa_defisit"]).to_integral_value(rounding=ROUND_FLOOR))
            bln = min(bln, maks_bulan)
            cadangan = rp_["sisa_defisit"] * bln
            ke_dd = bebas - cadangan
            teks = "{} {} saat cair: {} menutup kekurangan bulan ke-1 s.d. ke-{}{}".format(
                rinci, rp(h["total_musiman"]), rp(sampai_cair), akhir, teks_leb)
            if bln > 0:
                teks += "; dari sisanya {}, sebesar {} DICADANGKAN di rekening terpisah untuk menambal sisa " \
                        "defisit {}/bulan selama {} bulan (bulan ke-{} s.d. ke-{})".format(
                            rp(bebas), rp(cadangan), rp(rp_["sisa_defisit"]), bln, akhir + 1, akhir + bln)
            if bln >= maks_bulan:
                teks += ", sampai {} berikutnya cair; kelebihan {} baru masuk dana darurat.".format(rinci, rp(ke_dd))
            else:
                teks += "; mulai bulan ke-{} sisa defisit belum punya sumber - perlu tambahan pemasukan atau " \
                        "meninjau pos besar. Dana darurat baru diisi setelah defisit tertutup.".format(akhir + bln + 1)
            kalimat.append(teks + " THR bukan solusi tetap.")
            thr = {"bebas": bebas, "cadangan": cadangan, "bulan_cadangan": bln, "ke_dd": ke_dd, "lebaran": lebaran}
        else:
            kalimat.append("{} {} saat cair (bulan ke-{}): {} untuk menutup/mengganti kekurangan masa transisi{}, "
                           "sisanya {} disetor SEKALIGUS ke dana darurat. Tahun berikutnya anggaran sudah pas "
                           "tanpa THR.".format(rinci, rp(h["total_musiman"]), bulan_cair, rp(sampai_cair),
                                               teks_leb, rp(bebas)))
            thr = {"bebas": bebas, "cadangan": NOL, "bulan_cadangan": 0, "ke_dd": bebas, "lebaran": lebaran}
    return {"rp": rp_, "baris": baris, "sebelum": sebelum, "kalimat": kalimat, "talangan": talangan,
            "thr": thr, "rinci": rinci, "ada_thr": ada_thr, "jeda": jeda, "alt_jeda": alt}


def cetak_rencana_defisit(h, a, bulan_cair, bulan_cair_bawaan):
    if a is None:
        return []
    rp_, rinci, ada_thr = a["rp"], a["rinci"], a["ada_thr"]
    out = ["", "## Menutup defisit rutin TANPA bergantung pada THR (pemangkasan bertahap)", "",
           "- Pos bulanan di luar tabungan {} > pemasukan rutin {} -> defisit rutin **{}/bulan**. "
           "Setoran tabungan/dana darurat dari gaji = **Rp0** selama defisit belum tertutup.".format(
               rp(h["total_keluar"] - h["tabungan"]), rp(h["total_bulanan"]), rp(rp_["defisit"])),
           "", "| Pos | Sekarang | Potong | Jadi | Tahap |", "|---|---:|---:|---:|---|"]
    nama_tahap = {t: lbl for t, _, lbl in TAHAP_PANGKAS}
    for nm, n, ptg, tahap in rp_["potong"]:
        out.append("| {} | {} | -{} | {} | {} |".format(nm, rp(n), rp(ptg), rp(n - ptg), nama_tahap[tahap]))
    out.append("| **Total potongan** | | **-{}** | | |".format(rp(rp_["total_potong"])))
    if rp_["sisa_defisit"] > 0:
        out.append("")
        out.append("- Pemangkasan dalam batas wajar BELUM cukup: masih kurang **{}/bulan**. Perlu tambahan "
                   "pemasukan rutin atau meninjau pos besar (tempat tinggal, cicilan - jangan ditutup utang baru)."
                   " THR/bonus hanya penambal SEMENTARA.".format(rp(rp_["sisa_defisit"])))
    elif rp_["lebih"] > 0:
        out.append("")
        out.append("- Setelah pemangkasan penuh ada lebih {}/bulan (pembulatan Rp10.000) -> boleh jadi setoran "
                   "dana darurat bulanan.".format(rp(rp_["lebih"])))
    out += ["", "Jadwal bertahap ({} bulan) dan kekurangan per bulan{}:".format(
        LAMA_BERTAHAP, " sampai {} cair (bulan ke-{}{})".format(
            rinci, bulan_cair, ", asumsi bawaan - tanyakan bulan cairnya" if bulan_cair_bawaan else "")
        if ada_thr else ""), "",
        "| Bulan ke- | Potongan berjalan | Kekurangan bulan itu | Kekurangan kumulatif | Sumber penutup |",
        "|---:|---:|---:|---:|---|"]
    cukup_saldo = a["talangan"] is not None and a["talangan"]["cukup"]
    for m, ptg, kurang, kum in a["baris"]:
        if kurang <= 0:
            sumber = "tertutup pemangkasan"
        elif ada_thr and m >= bulan_cair and kum <= h["total_musiman"]:
            sumber = "{} cair bulan ini".format(rinci) if m == bulan_cair else "dari {} yang sudah cair".format(rinci)
        elif ada_thr and m >= bulan_cair:
            sumber = "BELUM ADA - {} sudah habis; bukan paylater/pinjol".format(rinci)
        elif cukup_saldo:
            sumber = "talangan dari saldo tabungan"
        else:
            sumber = "BELUM ADA - saldo tidak cukup; lihat pilihan tanpa utang di bawah"
        out.append("| {} | {} | {} | {} | {} |".format(m, rp(ptg), rp(kurang), rp(kum), sumber))
    out += ["", "Kalimat ringkasan siap tempel (angka dari script):", ""] + ["> " + x for x in a["kalimat"]]
    out += ["", "- THR/bonus = penambal SEMENTARA masa transisi, bukan sumber tetap untuk menutup defisit tiap "
            "tahun. Jangan menghitung sendiri versi pemangkasan lain: jalankan ulang script dengan nilai pos baru."]
    return out


def kalimat_cicilan(h):
    """Kalimat rasio cicilan siap tempel (v1.0.9) - SATU-SATUNYA angka 'rasio cicilan' yang boleh disebut."""
    if h["cicilan"] <= 0:
        return None
    rasio = h["cicilan"] * 100 / h["basis_cicilan"]
    basis = "gaji rutin" if h["basis_cicilan_rutin"] else "pemasukan"
    nilai = "DI ATAS batas aman 30% - jangan menambah utang baru." if rasio > BATAS_RASIO_CICILAN else \
        "masih dalam batas aman 30% - tetap jangan menambah utang baru tanpa hitungan."
    return "Total cicilan {} = {} dari {} {} — {}".format(
        rp(h["cicilan"]), persen(rasio), basis, rp(h["basis_cicilan"]), nilai)


def setoran_dana_darurat(h, pos):
    """Setoran bulanan ke dana darurat dari gaji: sisa rutin + pos tabungan bernama 'dana darurat'."""
    dd_pos = sum((n for nm, n, kel, _ in pos if kel == "tabungan" and "darurat" in nm.lower()), NOL)
    return max(h["sisa_rutin"] + dd_pos, NOL)


def parse_sisih(teks, thr, nama_thr="THR/bonus"):
    """v1.0.10: --sisih-lebaran (penyisihan kebutuhan Lebaran dari THR sebelum dialokasikan ke dana darurat)."""
    if teks is None:
        return NOL
    v = parse_rupiah(teks, "Sisih kebutuhan Lebaran (--sisih-lebaran)")
    if v > thr:
        raise InputSalah("--sisih-lebaran {} lebih besar dari {} {}. Isi kebutuhan Lebaran yang diambil dari THR "
                         "(mudik, baju, kue, angpau), paling banyak sebesar THR.".format(rp(v), nama_thr, rp(thr)))
    return v


def ringkasan_siap_tempel(h, a, pos, musiman, args, saldo):
    """v1.0.9: blok di paling atas keluaran 'anggaran' berisi kalimat lengkap (angka + penilaian) yang WAJIB
    disalin apa adanya oleh agent, agar angka kunci tidak ditulis ulang/ditafsir sendiri."""
    rinci = " + ".join(n for n, _ in musiman) or "THR/bonus"
    k_ = []
    if a is not None and h["tabungan"] > 0:
        # v1.0.10: SATU angka defisit (basis: pos tabungan dijeda); angka bila tetap dibayar hanya di kalimat jeda
        k_.append("Gaji rutin {}/bulan, pengeluaran di luar pos tabungan {}/bulan -> DEFISIT {}/bulan dari gaji "
                  "(basis: pos tabungan {} DIJEDA selama defisit; dihitung dari gaji saja, karena THR/bonus cair "
                  "sekali, bukan tiap bulan).".format(
                      rp(h["total_bulanan"]), rp(h["total_keluar"] - h["tabungan"]), rp(a["rp"]["defisit"]),
                      rp(h["tabungan"])))
    elif h["sisa_rutin"] >= 0:
        k_.append("Gaji rutin {}/bulan, total pos {}/bulan -> sisa {}/bulan dari gaji; inilah batas setoran "
                  "bulanan.".format(rp(h["total_bulanan"]), rp(h["total_keluar"]), rp(h["sisa_rutin"])))
    else:
        k_.append("Pengeluaran rutin {}/bulan lebih besar dari gaji rutin {} -> DEFISIT {}/bulan (dihitung dari "
                  "gaji saja, karena THR/bonus cair sekali, bukan tiap bulan).".format(
                      rp(h["total_keluar"]), rp(h["total_bulanan"]), rp(-h["sisa_rutin"])))
    kc = kalimat_cicilan(h)
    if kc:
        k_.append(kc)
    if a is not None:
        k_.append("Setoran dana darurat dari gaji Rp0 sampai defisit tertutup.")
        k_ += a["kalimat"]
    elif musiman and h["total_musiman"] > 0:
        if args.sisih_lebaran_rp > 0:
            k_.append("{} {} cair SEKALI (bukan tiap bulan): sisihkan {} untuk kebutuhan Lebaran (mudik, baju, kue, "
                      "angpau), sisanya {} disetor SEKALIGUS saat cair ke dana darurat/target; jangan ditambahkan ke "
                      "setoran bulanan.".format(rinci, rp(h["total_musiman"]), rp(args.sisih_lebaran_rp),
                                                rp(h["total_musiman"] - args.sisih_lebaran_rp)))
        else:
            k_.append("{} {} cair SEKALI (bukan tiap bulan) - setor SEKALIGUS saat cair ke dana darurat/target; "
                      "jangan ditambahkan ke setoran bulanan. Angka ini belum dikurangi kebutuhan Lebaran (mudik, "
                      "baju, kue, angpau) - sebutkan berapa yang perlu disisihkan, nanti setoran THR dihitung "
                      "ulang.".format(rinci, rp(h["total_musiman"])))
    # Dana darurat
    pokok = h["pokok_dana_darurat"]
    if pokok > 0:
        if args.status:
            mn, ideal, ket = STATUS_DANA_DARURAT[args.status]
            bl = sorted(set([mn, ideal]))
        else:
            bl = [3, 6, 9, 12]
        k_.append("Pengeluaran pokok {}/bulan -> target dana darurat {}{}.".format(
            rp(pokok), "; ".join("{} bulan = {}".format(b, rp(pokok * b)) for b in bl),
            "" if args.status else " (status belum diisi - pilih sesuai status)"))
        setoran = setoran_dana_darurat(h, pos) if a is None else NOL
        sekaligus = h["total_musiman"] - args.sisih_lebaran_rp if a is None else NOL
        bagian = []
        for b in bl:
            target = pokok * b
            kurang = max(target - saldo, NOL)
            prog = persen(min(saldo * 100 / target, Decimal(100)), 0)
            if a is not None:
                bagian.append("{} bulan: kurang {} (progres {})".format(b, rp(kurang), prog))
                continue
            lama = (0 if kurang == 0 else (int((kurang / setoran).to_integral_value(rounding=ROUND_CEILING))
                                            if setoran > 0 else None))
            teks = "{} bulan: kurang {} (progres {}), tercapai {} dengan setoran {}/bulan".format(
                b, rp(kurang), prog, _fmt_lama(lama), rp(setoran))
            if sekaligus > 0:
                teks += ", atau {} bila {} {} juga disetor tiap cair (cair pertama bulan ke-{}{})".format(
                    _fmt_lama(lama_dengan_musiman(kurang, setoran, sekaligus, args.bulan_cair_int)),
                    rinci if not args.sisih_lebaran_rp else "sisa " + rinci, rp(sekaligus),
                    args.bulan_cair_int, ", asumsi bawaan" if args.bulan_cair_bawaan else "")
            bagian.append(teks)
        k_.append("Saldo dana darurat sekarang {}{} -> {}.".format(
            rp(saldo), " (belum diisi, dianggap Rp0)" if args.saldo is None else "", "; ".join(bagian)))
        if a is not None:
            k_.append("Dana darurat mulai diisi setelah defisit rutin tertutup; lama tercapai belum bisa "
                      "dijadwalkan.")
    out = ["# RINGKASAN SIAP TEMPEL (salin kalimat ini APA ADANYA - jangan menghitung/menafsir ulang)", ""]
    out += ["> " + x for x in k_]
    if a is not None and a["jeda"]:
        out += ["", "- Kalimat 'TINDAKAN: ...' WAJIB masuk 'Langkah minggu ini' - pos tabungan/arisan tidak boleh "
                "berhenti dibayar tanpa diberitahukan ke pengguna. Defisit yang disebut = angka basis 'pos tabungan "
                "DIJEDA' di atas{}.".format("; angka 'bila arisan tetap dibayar' hanya disebut sebagai syarat"
                                            if a["alt_jeda"] else "")]
    if musiman and h["total_musiman"] > 0 and args.sisih_lebaran is None:
        out += ["", "- PENGINGAT: --sisih-lebaran belum diisi (dianggap Rp0 = seluruh THR untuk dana darurat/defisit). "
                "Tanyakan kebutuhan Lebaran pengguna (mudik, baju, kue, angpau) lalu jalankan ulang dengan "
                "--sisih-lebaran; jangan menyuruh menyetor SELURUH THR tanpa menyebut hal ini."]
    if kc:
        out += ["", "- Jangan menyebut persen satu pos (mis. KPR saja) sebagai \"rasio cicilan\"; rasio cicilan = "
                "kalimat 'Total cicilan ...' di atas."]
    out.append("")
    return out


def alternatif_pokok(pokok, rinci_keluarga, bulan_list):
    """Skenario alternatif dasar dana darurat tanpa kiriman keluarga. rinci_keluarga: list (nama, jumlah).
    Kembalikan list (label, pokok_alt, [(bulan, target)])."""
    hasil = []
    pilihan = [([x], x[0]) for x in rinci_keluarga]
    if len(rinci_keluarga) > 1:
        pilihan.append((list(rinci_keluarga), "semua kiriman keluarga"))
    for daftar, label in pilihan:
        alt = pokok - sum((j for _, j in daftar), NOL)
        hasil.append((label, sum((j for _, j in daftar), NOL), alt, [(b, alt * b) for b in bulan_list]))
    return hasil


def _lama_target(target, saldo, setoran, sekaligus, bulan_cair):
    """(lama setoran saja, lama + THR/bonus) dalam bulan; None = tidak tercapai."""
    kurang = max(target - saldo, NOL)
    if kurang == 0:
        biasa = 0
    elif setoran > 0:
        biasa = int((kurang / setoran).to_integral_value(rounding=ROUND_CEILING))
    else:
        biasa = None
    plus = lama_dengan_musiman(kurang, setoran, sekaligus, bulan_cair) if sekaligus > 0 else None
    return biasa, plus


def _fmt_selisih(lama, baru):
    if lama is None or baru is None:
        return "tidak bisa dibandingkan (ada yang tidak tercapai)"
    d = lama - baru
    return "tidak berubah" if d == 0 else ("{} bulan lebih cepat".format(d) if d > 0 else
                                           "{} bulan lebih lama".format(-d))


def _fmt_bln(m):
    return "tidak tercapai" if m is None else ("sudah tercapai" if m == 0 else "{} bulan".format(m))


def cetak_alternatif_pokok(pokok, rinci_keluarga, bulan_list, lama=None):
    """lama (v1.0.10, opsional) = (saldo, setoran bulanan, setoran sekaligus THR/bonus, bulan_cair): cetak
    perbandingan lama tercapai SEBELUM/SESUDAH per kolom, agar selisih waktu tidak dikarang agent."""
    if not rinci_keluarga or pokok <= 0:
        return []
    out = ["", "## Skenario alternatif dasar dana darurat (siap salin - JANGAN hitung sendiri)", "",
           "| Skenario | Pokok/bulan | " + " | ".join("{} bulan".format(b) for b in bulan_list) + " |",
           "|---|---:|" + "---:|" * len(bulan_list),
           "| Sekarang (kiriman keluarga dimasukkan) | {} | {} |".format(
               rp(pokok), " | ".join(rp(pokok * b) for b in bulan_list))]
    alts = alternatif_pokok(pokok, rinci_keluarga, bulan_list)
    for label, jml, alt, tg in alts:
        out.append("| Tanpa {} ({}) | {} | {} |".format(label, rp(jml), rp(alt), " | ".join(rp(t) for _, t in tg)))
    out += ["", "Kalimat siap tempel:", ""]
    for label, jml, alt, tg in alts:
        out.append("> Bila {} ({}/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi {} dan "
                   "target {} menjadi {}.".format(
                       label, rp(jml), rp(alt), "/".join("{} bulan".format(b) for b, _ in tg),
                       "/".join(rp(t) for _, t in tg)))
    if lama is None:
        return out
    saldo, setoran, sekaligus, bulan_cair = lama
    if setoran <= 0 and sekaligus <= 0:
        return out
    out += ["", "### Lama tercapai sekarang vs skenario (bulan) - setoran tetap {}/bulan{}".format(
        rp(setoran), "; {} sekali setahun mulai bulan ke-{}".format(rp(sekaligus), bulan_cair) if sekaligus > 0 else ""),
        "", "| Skenario | Target | Setoran saja: sekarang -> skenario | Selisih |{}".format(
            " + THR/bonus: sekarang -> skenario | Selisih |" if sekaligus > 0 else ""),
        "|---|---|---|---|" + ("---|---|" if sekaligus > 0 else "")]
    kalimat = []
    for label, jml, alt, tg in alts:
        bagian = []
        for b, t in tg:
            l0, p0 = _lama_target(pokok * b, saldo, setoran, sekaligus, bulan_cair)
            l1, p1 = _lama_target(t, saldo, setoran, sekaligus, bulan_cair)
            baris = "| Tanpa {} | {} bulan | {} -> {} | {} |".format(label, b, _fmt_bln(l0), _fmt_bln(l1),
                                                                    _fmt_selisih(l0, l1))
            teks = "target {} bulan: setoran saja {} -> {} ({})".format(b, _fmt_bln(l0), _fmt_bln(l1),
                                                                         _fmt_selisih(l0, l1))
            if sekaligus > 0:
                baris += " {} -> {} | {} |".format(_fmt_bln(p0), _fmt_bln(p1), _fmt_selisih(p0, p1))
                teks += ", dengan THR/bonus {} -> {} ({})".format(_fmt_bln(p0), _fmt_bln(p1), _fmt_selisih(p0, p1))
            out.append(baris)
            bagian.append(teks)
        kalimat.append("Lama tercapai bila {} tidak dihitung (setoran tetap): {}.".format(label, "; ".join(bagian)))
    out += ["", "Kalimat siap tempel:", ""] + ["> " + x for x in kalimat]
    out += ["", "- Selisih waktu HANYA dari tabel ini, per kolom. Jangan meringkas menjadi \"sekitar setahun lebih "
            "cepat\" bila kolom-kolomnya berbeda (ada yang tidak berubah)."]
    return out


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
    nama_pos = set(n.strip().lower() for n, _, _, _ in pos)
    for opsi, daftar in (("--pokok-juga", args.pokok_juga), ("--bukan-pokok", args.bukan_pokok)):
        for x in daftar or []:
            if x.strip().lower() not in nama_pos:
                raise InputSalah("{} '{}' tidak cocok dengan nama pos mana pun. Tulis persis nama pos, "
                                 "mis. {} \"Kiriman ortu\".".format(opsi, x, opsi))
    h = hitung_anggaran(pemasukan, musiman, pos, pola, args.pokok_juga or (), args.bukan_pokok or ())
    if h["total_masuk"] <= 0:
        raise InputSalah("Total pemasukan per bulan nol. Isi pemasukan bersih yang benar.")
    saldo = NOL
    if args.saldo is not None:
        saldo = cek_nominal_kecil(parse_rupiah(args.saldo, "Saldo dana darurat/tabungan"), args.saldo,
                                  "Saldo dana darurat/tabungan")
    args.sisih_lebaran_rp = parse_sisih(args.sisih_lebaran, h["total_musiman"])
    if args.sisih_lebaran is not None and h["total_musiman"] <= 0:
        raise InputSalah("--sisih-lebaran hanya dipakai bila ada --musiman (THR/bonus).")
    analisis = analisis_defisit(h, pos, musiman, args.bulan_cair_int, saldo, args.saldo is not None,
                                args.sisih_lebaran_rp)
    jeda_tab = analisis is not None and h["tabungan"] > 0
    out = ringkasan_siap_tempel(h, analisis, pos, musiman, args, saldo)
    out += ["# Anggaran Bulanan (zero-based)", "", "## Pemasukan per bulan", "",
            "| Sumber | Jumlah |", "|---|---:|"]
    for n, j in pemasukan:
        out.append("| {} | {} |".format(n, rp(j)))
    if musiman:
        rinci = ", ".join("{} {}".format(n, rp(j)) for n, j in musiman)
        out.append("| Musiman dibagi 12 ({}; total {}/th) | {} |".format(
            rinci, rp(h["total_musiman"]), rp(h["musiman_per_bulan"])))
    out.append("| **Total pemasukan** | **{}** |".format(rp(h["total_masuk"])))
    # v1.0.8: basis persen ditulis di judul kolom. Kolom utama = pemasukan RUTIN (sama dengan basis rasio
    # cicilan & banding pola); bila ada THR/bonus, kolom kedua = termasuk THR/12.
    basis = h["basis_pola"]
    dua = bool(musiman) and h["basis_cicilan_rutin"]
    judul = "% {} ({})".format("pemasukan rutin" if h["basis_cicilan_rutin"] else "pemasukan", rp(basis))
    if dua:
        judul += " | % termasuk THR/12 ({})".format(rp(h["total_masuk"]))
    out += ["", "## Pos pengeluaran & alokasi", "", "| Pos | Kelompok | Jumlah | {} |".format(judul),
            "|---|---|---:|---:|" + ("---:|" if dua else "")]

    def kol(x):
        return persen(x * 100 / basis) + (" | " + persen(x * 100 / h["total_masuk"]) if dua else "")
    for n, j, kel, ditebak in pos:
        out.append("| {} | {}{} | {} | {} |".format(
            n, NAMA_KELOMPOK[kel], " (tebakan)" if ditebak and kel != "lain" else "", rp(j), kol(j)))
    out.append("| **Total dialokasikan** | | **{}** | {} |".format(rp(h["total_keluar"]), kol(h["total_keluar"])))
    isi2 = " |" if dua else ""
    if jeda_tab:
        # v1.0.10: satu angka defisit - basis pos tabungan dijeda (sama dengan RINGKASAN SIAP TEMPEL)
        out.append("| **DEFISIT dari gaji rutin** (pos tabungan {} dijeda) | | **-{}** | pengeluaran di luar tabungan "
                   "> gaji rutin |{}".format(rp(h["tabungan"]), rp(analisis["rp"]["defisit"]), isi2))
    elif musiman and h["sisa_rutin"] < 0:
        # v1.0.9: defisit utama selalu berbasis gaji rutin (THR/12 hanya catatan gambaran setahun)
        out.append("| **DEFISIT dari gaji rutin** | | **{}** | pengeluaran > gaji rutin |{}".format(
            rp(h["sisa_rutin"]), isi2))
    elif h["sisa"] > 0:
        out.append("| **Belum dialokasikan** (termasuk THR/12 bila ada) | | **{}** | harus dijadikan 0 |{}".format(
            rp(h["sisa"]), isi2))
    elif h["sisa"] < 0:
        out.append("| **DEFISIT** | | **{}** | pengeluaran > pemasukan |{}".format(rp(h["sisa"]), isi2))
    else:
        out.append("| **Sisa** | | **Rp0** | zero-based tercapai |{}".format(isi2))
    if dua:
        out.append("")
        out.append("- Saat menyebut persen ke pengguna, sebut basisnya: \"% dari gaji rutin\" (kolom pertama) "
                   "atau \"% termasuk THR/12\" (kolom kedua). Jangan melabeli kolom kedua sebagai \"% gaji\".")
    p = pola
    t = h["target_pola"]
    out += ["", "## Banding pola {}/{}/{} - basis {} {}/bulan".format(
        *([format(x.normalize(), "f") for x in p] + [
            "pemasukan rutin" if h["basis_cicilan_rutin"] else "pemasukan", rp(h["basis_pola"])])), "",
            "| Kelompok | Pola | Batas pola | Rencana kamu | Selisih |", "|---|---:|---:|---:|---:|"]
    baris = [("Kebutuhan (wajib + keluarga/sosial)", p[0], t[0], h["kebutuhan"], "lebih"),
             ("Keinginan", p[1], t[1], h["keinginan"], "lebih"),
             ("Tabungan & pelunasan ekstra", p[2], t[2], h["tabungan"], "kurang")]
    for nama, pp, batas, nyata, arah in baris:
        selisih = nyata - batas
        out.append("| {} | {} | {} | {} | {} |".format(
            nama, persen(pp, 0), rp(batas), rp(nyata), ("+" if selisih > 0 else "") + rp(selisih)))
    if musiman and h["basis_cicilan_rutin"]:
        out += ["", "- Basis banding = gaji rutin (tanpa THR/12), sama dengan rasio cicilan. {} {} (sekali cair) "
                "di luar banding ini - jadikan setoran sekaligus ke dana darurat/target.".format(
                    ", ".join(n for n, _ in musiman), rp(h["total_musiman"]))]
    cat = []
    if h["sisa"] > 0 and h["sisa_rutin"] >= 0:
        rincian = ""
        if musiman:
            rincian = " ({} dari gaji tiap bulan + {} bagian THR/bonus yang cair sekali {})".format(
                rp(max(h["sisa_rutin"], NOL)), rp(h["sisa"] - max(h["sisa_rutin"], NOL)), rp(h["total_musiman"]))
        cat.append("Masih ada {} belum punya tugas{}. Zero-based: arahkan ke dana darurat, pelunasan utang "
                   "berbunga tinggi, atau target tabungan sampai sisa Rp0.".format(rp(h["sisa"]), rincian))
    if h["sisa_rutin"] < 0 or h["sisa"] < 0:
        dr = -h["sisa_rutin"] if h["sisa_rutin"] < 0 else -h["sisa"]
        sisa_thn = h["sisa"]
        if jeda_tab:
            dr = analisis["rp"]["defisit"]
            sisa_thn = h["total_masuk"] - (h["total_keluar"] - h["tabungan"])
        cat.append("DEFISIT {}/bulan dari gaji rutin{}. Kurangi pos Keinginan dulu, lalu tinjau pos lain. Jangan "
                   "menutup defisit dengan utang baru (paylater/pinjol) - itu gali lubang tutup lubang.".format(
                       rp(dr), " (pos tabungan {} dijeda)".format(rp(h["tabungan"])) if jeda_tab else ""))
        if musiman and h["sisa_rutin"] < 0:
            if sisa_thn < 0:
                gamb = "kekurangannya tampak tinggal {}/bulan".format(rp(-sisa_thn))
            else:
                gamb = "kekurangannya tampak tertutup"
            cat.append("Catatan gambaran setahun (bukan angka utama): kalau {} {} dibagi rata ke 12 bulan, {} - "
                       "tetapi THR cair sekali, jadi bulan-bulan sebelum THR cair tetap kurang {}. Yang disebut "
                       "ke pengguna adalah defisit dari gaji rutin.".format(
                           ", ".join(n for n, _ in musiman), rp(h["total_musiman"]), gamb, rp(dr)))
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
    rasio = h["cicilan"] * 100 / h["basis_cicilan"]
    if h["cicilan"] > 0:
        if h["basis_cicilan_rutin"]:
            pesan = "Total cicilan {} = {} dari pemasukan RUTIN per bulan {} (basis tanpa THR/bonus, karena " \
                    "THR tidak ada tiap bulan).".format(rp(h["cicilan"]), persen(rasio), rp(h["basis_cicilan"]))
            if musiman:
                pesan += " Sebagai pembanding, terhadap pemasukan termasuk THR/12: {}.".format(
                    persen(h["cicilan"] * 100 / h["total_masuk"]))
        else:
            pesan = "Total cicilan {} = {} dari pemasukan (hanya ada pemasukan musiman).".format(
                rp(h["cicilan"]), persen(rasio))
        if rasio > BATAS_RASIO_CICILAN:
            pesan += " DI ATAS patokan umum 30% - jangan menambah utang baru; pertimbangkan subperintah utang."
        cat.append(pesan)
    lain = [n for n, _, k, _ in pos if k == "lain"]
    if lain:
        cat.append("Pos belum dikelompokkan (dihitung sebagai Keinginan sementara): {}. Tambahkan "
                   "':wajib'/':sosial'/':keinginan'/':tabungan' di akhir pos.".format(", ".join(lain)))
    ew = [n for n, _, _, _ in pos if any(k in n.lower() for k in KATA_EWALLET)
          and not any(k in n.lower() for k in KATA_INVESTASI)]
    if ew:
        cat.append("Pos {} tampak seperti TOP-UP e-wallet. Top-up hanya pindah dompet, bukan pengeluaran; "
                   "catat menurut pemakaiannya (makan, transport, belanja) agar tidak dobel.".format(", ".join(ew)))
    if musiman:
        cat.append("Pemasukan musiman (THR/bonus) dibagi 12 dan dibulatkan ke bawah HANYA untuk gambaran setahun. "
                   "Uangnya cair sekali - lihat bagian 'Arus kas rutin vs musiman' untuk setoran bulanan yang "
                   "benar-benar ada.")
    if cat:
        out += ["", "## Catatan", ""] + ["- " + c for c in cat]
    if musiman:
        out += cetak_arus_musiman(h, musiman, analisis is not None, analisis["rp"]["defisit"] if jeda_tab else None,
                                  args.sisih_lebaran_rp)
    out += cetak_rencana_defisit(h, analisis, args.bulan_cair_int, args.bulan_cair_bawaan)
    if h["pokok_rinci"] or h["pokok_keluar"]:
        label = {"wajib": "kebutuhan wajib", "cicilan": "cicilan/utang minimum",
                 "keluarga": "kewajiban rutin keluarga", "pengguna": "dimasukkan atas keputusan pengguna"}
        out += ["", "## Dasar dana darurat (pengeluaran pokok per bulan)", "",
                "| Pos DIMASUKKAN ke pokok | Jenis | Jumlah |", "|---|---|---:|"]
        for n, j, jenis in h["pokok_rinci"]:
            out.append("| {} | {} | {} |".format(n, label[jenis], rp(j)))
        out.append("| **Total pengeluaran pokok** | | **{}** |".format(rp(h["pokok_dana_darurat"])))
        if h["pokok_keluar"]:
            out += ["", "| Pos DIKELUARKAN dari pokok | Jumlah | Alasan |", "|---|---:|---|"]
            for n, j, alasan in h["pokok_keluar"]:
                out.append("| {} | {} | {} |".format(n, rp(j), alasan))
        out += ["", "- Pokok = Kebutuhan wajib + SEMUA cicilan/utang minimum (PayLater, kartu kredit, KPR, pinjol, "
                "leasing, KTA) + kewajiban rutin keluarga (kiriman orang tua/mertua/adik) - tetap harus dibayar "
                "walau penghasilan berhenti.",
                "- Sebutkan ke pengguna pos yang dimasukkan DAN yang dikeluarkan beserta alasannya. Bila pengguna "
                "ingin mengubah, jalankan ulang dengan --pokok-juga \"nama pos\" atau --bukan-pokok \"nama pos\".",
                "- Pakai angka ini untuk dana darurat: dana-darurat --pengeluaran-pokok {} --status ...".format(
                    int(h["pokok_dana_darurat"].to_integral_value(rounding=ROUND_HALF_UP)))]
        if args.status:
            mn, ideal, _ = STATUS_DANA_DARURAT[args.status]
            bl = sorted(set([mn, ideal]))
        else:
            bl = [3, 6, 9, 12]
        kel = [(n, j) for n, j, jenis in h["pokok_rinci"] if jenis == "keluarga"]
        lama = None
        if analisis is None:
            lama = (saldo, setoran_dana_darurat(h, pos), h["total_musiman"] - args.sisih_lebaran_rp,
                    args.bulan_cair_int)
        out += cetak_alternatif_pokok(h["pokok_dana_darurat"], kel, bl, lama)
    return "\n".join(out)


def cetak_arus_musiman(h, musiman, defisit_struktural=False, defisit_jeda=None, sisih=NOL):
    """Bagian 'Arus kas rutin vs musiman': mencegah THR dihitung dua kali (sekali sebagai /12 di pemasukan
    bulanan, sekali lagi sebagai setoran sekaligus saat cair)."""
    rinci = ", ".join(n for n, _ in musiman)
    out = ["", "## Arus kas rutin vs musiman (THR/bonus)", "",
           "| Arus | Per bulan | Kapan uangnya ada |", "|---|---:|---|",
           "| Pemasukan rutin (gaji bersih) | {} | tiap bulan |".format(rp(h["total_bulanan"])),
           ("| Total pos dialokasikan | {} | tiap bulan |".format(rp(h["total_keluar"])) if defisit_jeda is None else
            "| Total pos di luar tabungan (pos tabungan {} dijeda) | {} | tiap bulan |".format(
                rp(h["tabungan"]), rp(h["total_keluar"] - h["tabungan"]))),
           "| **Sisa dari pemasukan rutin** | **{}** | tiap bulan |".format(
               rp(h["sisa_rutin"] if defisit_jeda is None else -defisit_jeda)),
           "| {} (setara /12) | {} | SEKALI saat cair: {} |".format(
               rinci, rp(h["musiman_per_bulan"]), rp(h["total_musiman"])), ""]
    if h["sisa_rutin"] >= 0:
        out += ["- Setoran/transfer BULANAN (dana darurat, target, pelunasan ekstra) paling banyak **{}/bulan** - "
                "hanya dari gaji. Jangan menyebut sisa {} sebagai uang yang bisa dipindah tiap bulan: "
                "{} di dalamnya adalah bagian THR/bonus.".format(
                    rp(h["sisa_rutin"]), rp(h["sisa"]), rp(h["musiman_per_bulan"])),
                "- {} **{}** dicadangkan/disetor SEKALIGUS saat cair (mis. langsung ke dana darurat atau "
                "target). Itu setara {} x 12 bulan - jangan ditambahkan lagi ke setoran bulanan "
                "(dihitung dua kali).".format(rinci, rp(h["total_musiman"]), rp(h["musiman_per_bulan"]))]
        if sisih > 0:
            out[-1] = ("- {} **{}** cair SEKALI (setara {} x 12 bulan - jangan ditambahkan lagi ke setoran bulanan). "
                       "Kebutuhan Lebaran disisihkan dulu: **{}**; yang disetor SEKALIGUS ke dana darurat/target = "
                       "**{}**.".format(rinci, rp(h["total_musiman"]), rp(h["musiman_per_bulan"]), rp(sisih),
                                        rp(h["total_musiman"] - sisih)))
    elif defisit_struktural:
        if defisit_jeda is None:
            awal = "- Pos bulanan {} melebihi gaji rutin {} -> DEFISIT {}/bulan dari gaji.".format(
                rp(h["total_keluar"]), rp(h["total_bulanan"]), rp(-h["sisa_rutin"]))
        else:
            awal = "- Pos di luar tabungan {} melebihi gaji rutin {} -> DEFISIT {}/bulan dari gaji (pos tabungan {} " \
                   "dijeda).".format(rp(h["total_keluar"] - h["tabungan"]), rp(h["total_bulanan"]), rp(defisit_jeda),
                                     rp(h["tabungan"]))
        out += [awal + " Rencana penutupnya "
                "(pemangkasan bertahap, kekurangan sebelum {} cair, pemakaian {}) sudah dihitung di RINGKASAN SIAP "
                "TEMPEL dan bagian 'Menutup defisit rutin' - salin dari sana, jangan menyusun rencana "
                "'THR menambal defisit' sendiri.".format(rinci, rinci)]
    else:
        t = h["tambal_musiman_per_bulan"]
        out += ["- PERHATIAN: pos bulanan {} melebihi pemasukan rutin {} -> kurang **{}/bulan** dari gaji. "
                "Kekurangan ini harus ditutup dari {}.".format(
                    rp(h["total_keluar"]), rp(h["total_bulanan"]), rp(t), rinci),
                "- {} {} hanya cukup menutup kekurangan itu selama **{} bulan**{}.".format(
                    rinci, rp(h["total_musiman"]), h["bulan_ditambal_musiman"],
                    "" if h["bulan_ditambal_musiman"] < 12 else " (setahun penuh terpenuhi)")]
        if h["musiman_bebas_setahun"] >= 0:
            out.append("- Setelah menambal 12 bulan ({}), sisa {} yang bebas: **{}** (sekali saat cair).".format(
                rp(h["tambal_musiman_setahun"]), rinci, rp(h["musiman_bebas_setahun"])))
        else:
            out.append("- {} TIDAK cukup menambal setahun: kurang {}. Kurangi pos bulanan.".format(
                rinci, rp(-h["musiman_bebas_setahun"])))
        out.append("- Sebelum {} cair, kekurangan {}/bulan tidak punya sumber. Bila ada pos setoran tabungan, "
                   "turunkan setoran bulanan menjadi maks. {} (sisa gaji) dan pindahkan sisanya ke setoran "
                   "sekaligus saat THR cair.".format(rinci, rp(t), rp(max(h["tabungan"] - t, NOL))))
        out.append("- THR/bonus hanya penambal SEMENTARA. Bila pos di luar tabungan sudah melebihi gaji, lihat "
                   "bagian 'Menutup defisit rutin TANPA bergantung pada THR' di bawah.")
    out.append("- Langkah aksi ke pengguna WAJIB memakai angka di tabel ini: setoran bulanan dari sisa rutin, "
               "THR/bonus sebagai setoran sekaligus saat cair.")
    return out


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


def lama_dengan_musiman(kurang, setoran, sekaligus, bulan_cair, batas=720):
    """Bulan sampai kekurangan tertutup bila tiap bulan disetor `setoran` dan setiap 12 bulan (mulai bulan ke
    `bulan_cair`) disetor `sekaligus` (THR/bonus). None bila tidak tercapai dalam batas."""
    if kurang <= 0:
        return 0
    terkumpul = NOL
    for m in range(1, batas + 1):
        terkumpul += setoran
        if sekaligus > 0 and m >= bulan_cair and (m - bulan_cair) % 12 == 0:
            terkumpul += sekaligus
        if terkumpul >= kurang:
            return m
    return None


def cetak_dana_darurat(args):
    rinci = []
    if args.pengeluaran_pokok is not None:
        dasar = cek_nominal_kecil(parse_rupiah(args.pengeluaran_pokok, "Pengeluaran pokok per bulan",
                                               boleh_nol=not (args.pos or args.cicilan or args.keluarga)),
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
    for t in args.keluarga or []:
        n, j = pisah_nama_jumlah(t, "Kiriman keluarga")
        rinci.append((n, parse_rupiah(j, "Kiriman keluarga '{}'".format(n)), "keluarga"))
    keluar = []
    for t in args.dikeluarkan or []:
        badan, alasan = (t.split(";", 1) + [""])[:2] if ";" in t else (t, "")
        n, j = pisah_nama_jumlah(badan, "Pos dikeluarkan")
        keluar.append((n, parse_rupiah(j, "Pos dikeluarkan '{}'".format(n)),
                       alasan.strip() or "alasan belum ditulis - sebutkan ke pengguna"))
    if not rinci and args.pengeluaran_pokok is None:
        raise InputSalah("Isi --pengeluaran-pokok, atau rincian --pos \"Kontrakan=2jt\" / --keluarga \"Kiriman ortu=1jt\" / "
                         "--cicilan \"PayLater=650rb\".")
    pokok = sum((j for _, j, _ in rinci), NOL)
    if pokok <= 0:
        raise InputSalah("Pengeluaran pokok per bulan tidak boleh Rp0.")
    ada_cicilan = any(c is True for _, _, c in rinci)
    ada_keluarga = any(c == "keluarga" or (c is False and adalah_keluarga(n)) for n, _, c in rinci)
    keluarga_dikeluarkan = any(adalah_keluarga(n) for n, _, _ in keluar)
    saldo = cek_nominal_kecil(parse_rupiah(args.saldo, "Saldo dana darurat"), args.saldo, "Saldo dana darurat")
    setoran = parse_rupiah(args.setoran, "Setoran per bulan")
    sekaligus = parse_rupiah(args.setoran_tahunan, "Setoran sekaligus tahunan (THR/bonus)")
    if args.sisih_lebaran is not None and sekaligus <= 0:
        raise InputSalah("--sisih-lebaran hanya dipakai bersama --setoran-tahunan (THR/bonus).")
    sisih = parse_sisih(args.sisih_lebaran, sekaligus, "--setoran-tahunan")
    thr_kotor = sekaligus
    sekaligus = sekaligus - sisih
    try:
        bulan_cair = int(str(args.bulan_cair).strip())
    except ValueError:
        raise InputSalah("--bulan-cair harus angka bulan 1-12 (THR cair berapa bulan lagi dari sekarang).")
    if not 1 <= bulan_cair <= 12:
        raise InputSalah("--bulan-cair harus 1-12 (THR/bonus cair berapa bulan lagi dari sekarang).")
    ket, hasil = hitung_dana_darurat(pokok, args.status, saldo, setoran)
    for h in hasil:
        h["lama_musiman"] = lama_dengan_musiman(h["kurang"], setoran, sekaligus, bulan_cair) if sekaligus > 0 else None
    out = ["# Dana Darurat", "", "- Status: {} -> target {} bulan pengeluaran pokok".format(
        ket, "-".join(str(h["bulan"]) for h in hasil)),
        "- Pengeluaran pokok per bulan: {}{}".format(rp(pokok), " (rincian di bawah)" if len(rinci) > 1 else ""),
        "- Saldo sekarang: {} | Setoran rutin (dari gaji): {}/bulan".format(rp(saldo), rp(setoran))]
    if sekaligus > 0:
        out.append("- Setoran sekaligus THR/bonus: {} sekali setahun{}, cair bulan ke-{} dari sekarang{} - "
                   "TIDAK termasuk dalam setoran rutin di atas".format(
                       rp(sekaligus), " ({} dikurangi kebutuhan Lebaran {})".format(rp(thr_kotor), rp(sisih))
                       if sisih > 0 else "", bulan_cair, " (asumsi bawaan; tanyakan bulan cairnya)"
                       if args.bulan_cair_bawaan else ""))
    if thr_kotor > 0 and args.sisih_lebaran is None:
        out.append("- PENGINGAT: --sisih-lebaran belum diisi (dianggap Rp0 = seluruh {} ke dana darurat). Tanyakan "
                   "kebutuhan Lebaran (mudik, baju, kue, angpau) lalu jalankan ulang dengan --sisih-lebaran.".format(
                       rp(thr_kotor)))
    out += ["", "| Target | Jumlah | Kekurangan | Lama tercapai (setoran rutin saja) |{} Progres |".format(
                " Lama tercapai (+ THR/bonus) |" if sekaligus > 0 else ""),
            "|---|---:|---:|---:|{}---:|".format("---:|" if sekaligus > 0 else "")]
    for h in hasil:
        if h["lama"] is None:
            lama = "tidak tercapai (setoran Rp0)"
        elif h["lama"] == 0:
            lama = "sudah tercapai"
        else:
            lama = "{} bulan (~{} th {} bln)".format(h["lama"], h["lama"] // 12, h["lama"] % 12)
        blok = int((h["progres"] / 5).to_integral_value(rounding=ROUND_FLOOR))
        kol = ""
        if sekaligus > 0:
            lm = h["lama_musiman"]
            kol = " {} |".format("sudah tercapai" if lm == 0 else (
                "tidak tercapai" if lm is None else "{} bulan (~{} th {} bln)".format(lm, lm // 12, lm % 12)))
        out.append("| {} bulan | {} | {} | {} |{} {} {} |".format(
            h["bulan"], rp(h["target"]), rp(h["kurang"]), lama, kol, "#" * blok + "." * (20 - blok),
            persen(h["progres"], 0)))
    if len(rinci) > 1:
        out += ["", "| Pos DIMASUKKAN ke pokok | Jumlah |", "|---|---:|"]
        for n, j, c in rinci:
            tanda = " (cicilan)" if c is True else (" (kewajiban keluarga)" if c == "keluarga" else "")
            out.append("| {}{} | {} |".format(n, tanda, rp(j)))
        out.append("| **Total pengeluaran pokok** | **{}** |".format(rp(pokok)))
    kel_rinci = [(n, j) for n, j, c in rinci if c == "keluarga" or (c is False and adalah_keluarga(n))]
    out += cetak_alternatif_pokok(pokok, kel_rinci, [h["bulan"] for h in hasil],
                                  (saldo, setoran, sekaligus, bulan_cair))
    if keluar:
        out += ["", "| Pos DIKELUARKAN dari pokok (tidak dijumlahkan) | Jumlah | Alasan |", "|---|---:|---|"]
        for n, j, a in keluar:
            out.append("| {} | {} | {} |".format(n, rp(j), a))
    out += ["", "Catatan:",
            "- Pengeluaran pokok = yang tetap harus dibayar walau penghasilan berhenti (makan, tempat tinggal, "
            "listrik/air, transport, SEMUA cicilan/utang minimum, sekolah, BPJS, kiriman keluarga yang wajib). "
            "Bukan nongkrong/hiburan."]
    if not ada_cicilan:
        out.append("- CEK CICILAN: belum ada cicilan yang tercatat. Bila ada cicilan PayLater, kartu kredit, KPR, "
                   "motor/leasing, KTA, atau pinjol, tambahkan (--cicilan \"PayLater=650rb\") - cicilan tetap "
                   "wajib dibayar saat penghasilan berhenti, jadi masuk dasar dana darurat.")
    if not ada_keluarga and not keluarga_dikeluarkan:
        out.append("- CEK KIRIMAN KELUARGA: belum ada kiriman/tanggungan keluarga tercatat. Bila ada kiriman rutin "
                   "ke orang tua/mertua/adik yang tidak bisa ditunda, tambahkan (--keluarga \"Kiriman ortu=1jt\"); "
                   "bila sengaja tidak dihitung, catat lewat --dikeluarkan \"Kiriman ortu=1jt;alasan\" dan "
                   "sebutkan alasannya ke pengguna.")
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
    a.add_argument("--pokok-juga", action="append",
                   help="Nama pos yang DIMASUKKAN ke dasar dana darurat atas keputusan pengguna (berulang)")
    a.add_argument("--bukan-pokok", action="append",
                   help="Nama pos yang DIKELUARKAN dari dasar dana darurat atas keputusan pengguna (berulang)")
    a.add_argument("--saldo", default=None,
                   help="Saldo dana darurat/tabungan yang bisa dipakai sekarang (bawaan: dianggap Rp0)")
    a.add_argument("--status", default=None, choices=sorted(STATUS_DANA_DARURAT),
                   help="Opsional: status untuk target dana darurat di skenario alternatif")
    a.add_argument("--bulan-cair", default=None,
                   help="THR/bonus cair berapa bulan lagi (1-12; bawaan 12). Dipakai jadwal defisit sampai THR cair")
    a.add_argument("--sisih-lebaran", default=None,
                   help="Kebutuhan Lebaran (mudik/baju/angpau) yang disisihkan dari THR sebelum ke dana darurat")

    d = sub.add_parser("dana-darurat", help="Target dana darurat sesuai status")
    d.add_argument("--pengeluaran-pokok", default=None,
                   help="Pengeluaran pokok per bulan (gabungan). Boleh diganti/ditambah --pos dan --cicilan")
    d.add_argument("--pos", action="append", help="Rincian pos pokok 'nama=jumlah' (berulang)")
    d.add_argument("--cicilan", action="append",
                   help="Cicilan/utang minimum 'nama=jumlah' (PayLater, kartu kredit, KPR, pinjol; berulang) - "
                        "ditambahkan ke pengeluaran pokok")
    d.add_argument("--keluarga", action="append",
                   help="Kewajiban rutin keluarga 'nama=jumlah' (kiriman ortu/mertua/adik), masuk pokok (berulang)")
    d.add_argument("--dikeluarkan", action="append",
                   help="Pos yang TIDAK dihitung pokok 'nama=jumlah;alasan' - hanya dicetak, tidak dijumlahkan")
    d.add_argument("--status", required=True, choices=sorted(STATUS_DANA_DARURAT))
    d.add_argument("--saldo", default="0", help="Dana darurat yang sudah ada")
    d.add_argument("--setoran", default="0", help="Setoran rutin per bulan (dari gaji, TANPA bagian THR/12)")
    d.add_argument("--setoran-tahunan", default="0",
                   help="Setoran sekaligus sekali setahun dari THR/bonus saat cair (opsional)")
    d.add_argument("--bulan-cair", default=None,
                   help="THR/bonus cair berapa bulan lagi dari sekarang (1-12; bawaan 12 = paling hati-hati)")
    d.add_argument("--sisih-lebaran", default=None,
                   help="Kebutuhan Lebaran yang disisihkan dari --setoran-tahunan sebelum ke dana darurat")

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
    if args.perintah in ("dana-darurat", "anggaran"):
        args.bulan_cair_bawaan = args.bulan_cair is None
        if args.bulan_cair is None:
            args.bulan_cair = "12"
        if args.perintah == "anggaran":
            try:
                args.bulan_cair_int = int(str(args.bulan_cair).strip())
            except ValueError:
                args.bulan_cair_int = 0
            if not 1 <= args.bulan_cair_int <= 12:
                sys.stderr.write("Input belum benar: --bulan-cair harus 1-12 (THR/bonus cair berapa bulan lagi "
                                 "dari sekarang).\n")
                return 2
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
