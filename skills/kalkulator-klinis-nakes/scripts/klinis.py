#!/usr/bin/env python3
"""Kalkulator klinis untuk TENAGA KESEHATAN (alat bantu keputusan, bukan diagnosis).

Hanya library standar Python. Tanpa internet, tanpa menyimpan data apa pun.

Perintah (jalankan dari folder skill; Windows: ganti python3 dengan python atau py):
  python3 scripts/klinis.py map --sistolik 120 --diastolik 80
  python3 scripts/klinis.py faktor-preeklampsia                 # daftar kode faktor
  python3 scripts/klinis.py preeklampsia --faktor nullipara,obesitas --sistolik 118 --diastolik 82
  python3 scripts/klinis.py kehamilan --hpht 2026-03-10 [--siklus 30] [--tanggal-periksa 2026-09-29]
                                      [--usg-tanggal 2026-05-02 --usg-minggu 7 --usg-hari 3]
  python3 scripts/klinis.py bb-hamil --tinggi 155 --bb-prahamil 62 [--bb-sekarang 68 --usia-minggu 24] [--kembar]
  python3 scripts/klinis.py imt --tinggi 165 --berat 72 [--lingkar-perut 92 --jk L]
  python3 scripts/klinis.py kognitif --instrumen moca --skor 24 --pendidikan-tahun 9

Tambahkan --json untuk keluaran JSON. Kode keluar 1 = input tidak valid (pesan jelas di stderr).
Setiap hasil memuat sumber pedoman + tahun dan kalimat "alat bantu, bukan pengganti penilaian klinis".
"""
import argparse
import calendar
import json
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from fractions import Fraction

VERSI = "1.0.0"
PENAFIAN = ("Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. "
            "Keputusan klinis tetap pada dokter/bidan yang memeriksa.")

SUMBER = {
    "kia": "Kemenkes RI, Buku Kesehatan Ibu dan Anak (Buku KIA) 2023 - lembar skrining "
           "preeklampsia usia kehamilan < 20 minggu",
    "nice": "NICE NG133 Hypertension in pregnancy: diagnosis and management (2019, "
            "diperbarui 2023) - bagian 1.1 faktor risiko preeklampsia",
    "map": "Rumus MAP = (sistolik + 2 x diastolik) / 3; ambang MAP > 90 mmHg dari Buku KIA 2023",
    "naegele": "Aturan Naegele (HPHT + 7 hari - 3 bulan + 1 tahun); penyesuaian siklus = "
               "modifikasi umum (siklus - 28 hari)",
    "acog": "ACOG Committee Opinion No. 700 Methods for Estimating the Due Date (2017)",
    "iom": "Institute of Medicine & National Research Council, Weight Gain During Pregnancy: "
           "Reexamining the Guidelines (2009)",
    "ap": "WHO WPRO/IASO/IOTF, The Asia-Pacific Perspective: Redefining Obesity and its "
          "Treatment (2000)",
    "kemenkes_imt": "Kemenkes RI, Pedoman Gizi Seimbang (Permenkes No. 41 Tahun 2014) - "
                    "batas ambang IMT Indonesia",
    "mmse": "Folstein dkk. 1975 (J Psychiatr Res 12:189-198); rentang Tombaugh & McIntyre 1992 "
            "(J Am Geriatr Soc 40:922-935)",
    "moca": "Nasreddine dkk. 2005 (J Am Geriatr Soc 53:695-699): >= 26 normal, +1 poin bila "
            "pendidikan <= 12 tahun; MoCA-Ina: Husein dkk. 2010 (Neurona 27(4)) - batas "
            "khusus Indonesia belum ditetapkan dalam studi validasi itu",
    "amt": "Hodkinson 1972 (Age Ageing 1:233-238); pembagian 8-10 / 4-7 / 0-3 sesuai formulir "
           "AMT Permenkes No. 67 Tahun 2015 (PERLU REVIEW tenaga medis)",
}


class InputSalah(ValueError):
    """Input tidak valid; pesan ditampilkan apa adanya ke pengguna."""


# ---------------------------------------------------------------- utilitas angka & tanggal

def desimal(teks, nama):
    """Ubah teks (koma atau titik desimal) menjadi Decimal. Tolak kosong/bukan angka."""
    if isinstance(teks, (int, Decimal)):
        return Decimal(teks)
    s = str(teks).strip().replace(" ", "")
    if s.count(",") == 1 and "." not in s:
        s = s.replace(",", ".")
    try:
        d = Decimal(s)
    except InvalidOperation:
        raise InputSalah(f"{nama}: '{teks}' bukan angka")
    if not d.is_finite():
        raise InputSalah(f"{nama}: '{teks}' bukan angka")
    return d


def bulat(d, tempat="0.1"):
    return d.quantize(Decimal(tempat), rounding=ROUND_HALF_UP)


def tanggal(teks, nama):
    s = str(teks).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise InputSalah(f"{nama}: '{teks}' bukan tanggal valid (pakai TTTT-BB-HH atau HH-BB-TTTT)")


def tambah_bulan(d, n):
    """Tambah n bulan kalender; bila tanggal tidak ada (mis. 31 Feb) turun ke akhir bulan."""
    total = d.month - 1 + n
    th, bl = d.year + total // 12, total % 12 + 1
    hari = min(d.day, calendar.monthrange(th, bl)[1])
    return date(th, bl, hari), hari != d.day


def minggu_hari(hari):
    return f"{hari // 7} minggu {hari % 7} hari"


def fmt_tgl(d):
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
             "September", "Oktober", "November", "Desember"]
    return f"{d.day} {bulan[d.month - 1]} {d.year} ({d.isoformat()})"


def tinggi_m(teks):
    """Tinggi badan: angka >= 3 dianggap cm, < 3 dianggap meter. Batas wajar 50-250 cm."""
    t = desimal(teks, "tinggi")
    cm = t * 100 if t < 3 else t
    if not Decimal(50) <= cm <= Decimal(250):
        raise InputSalah(f"tinggi {teks}: di luar rentang wajar 50-250 cm (cek satuan: cm atau m)")
    return cm / 100


def berat_kg(teks, nama="berat"):
    b = desimal(teks, nama)
    if not Decimal(20) <= b <= Decimal(350):
        raise InputSalah(f"{nama} {teks} kg: di luar rentang wajar dewasa 20-350 kg "
                         "(skill ini hanya untuk dewasa/ibu hamil; cek satuan kg)")
    return b


# ---------------------------------------------------------------- MAP

def hitung_map(sistolik, diastolik):
    s, d = desimal(sistolik, "sistolik"), desimal(diastolik, "diastolik")
    if not (Decimal(50) <= s <= Decimal(300)):
        raise InputSalah(f"sistolik {sistolik}: di luar rentang wajar 50-300 mmHg")
    if not (Decimal(20) <= d <= Decimal(200)):
        raise InputSalah(f"diastolik {diastolik}: di luar rentang wajar 20-200 mmHg")
    if d >= s:
        raise InputSalah("diastolik harus lebih kecil dari sistolik (mungkin tertukar?)")
    tepat = (Fraction(s) + 2 * Fraction(d)) / 3  # dibandingkan tanpa pembulatan
    tampil = bulat(Decimal(tepat.numerator) / Decimal(tepat.denominator))
    return {
        "perintah": "map", "sistolik": str(s), "diastolik": str(d),
        "map_mmhg": str(tampil), "map_lebih_dari_90": tepat > 90,
        "catatan": ["Dibandingkan dengan nilai tepat (tanpa pembulatan). Ukur ulang sesuai "
                    "prosedur baku bila hasil di sekitar 90."],
        "sumber": [SUMBER["map"]], "penafian": PENAFIAN,
    }


# ---------------------------------------------------------------- preeklampsia

FAKTOR = {
    # kode: (label, kategori Buku KIA 2023, kategori NICE NG133 atau None)
    "pasangan-baru": ("Multipara dengan kehamilan oleh pasangan baru", "sedang", None),
    "reproduksi-berbantu": ("Kehamilan dengan teknologi reproduksi berbantu (bayi tabung, "
                            "obat induksi ovulasi)", "sedang", None),
    "usia-ibu-35": ("Usia ibu >= 35 tahun", "sedang", None),
    "usia-ibu-40": ("Usia ibu >= 40 tahun", "sedang", "sedang"),
    "nullipara": ("Nullipara (kehamilan pertama)", "sedang", "sedang"),
    "jarak-10-tahun": ("Multipara dengan jarak kehamilan sebelumnya > 10 tahun", "sedang", "sedang"),
    "riwayat-keluarga": ("Riwayat preeklampsia pada ibu atau saudara perempuan", "sedang", "sedang"),
    "obesitas": ("Obesitas sebelum hamil (IMT > 30 kg/m2)", "sedang", None),
    "imt-35": ("IMT >= 35 kg/m2 saat kunjungan pertama", "sedang", "sedang"),
    "map-90": ("MAP > 90 mmHg", "sedang", None),
    "riwayat-preeklampsia": ("Riwayat preeklampsia / penyakit hipertensi pada kehamilan "
                             "sebelumnya", "tinggi", "tinggi"),
    "kehamilan-multipel": ("Kehamilan multipel (kembar)", "tinggi", "sedang"),
    "diabetes": ("Diabetes dalam kehamilan / diabetes tipe 1 atau 2", "tinggi", "tinggi"),
    "hipertensi-kronik": ("Hipertensi kronik", "tinggi", "tinggi"),
    "penyakit-ginjal": ("Penyakit ginjal (kronik)", "tinggi", "tinggi"),
    "autoimun": ("Penyakit autoimun / SLE", "tinggi", "tinggi"),
    "antifosfolipid": ("Sindrom antifosfolipid (APS)", "tinggi", "tinggi"),
    "proteinuria": ("Proteinuria (dipstik > +1 pada 2 kali periksa berjarak 6 jam, atau "
                    "kuantitatif 300 mg/24 jam)", "tinggi", None),
}
# "usia-ibu-40" otomatis juga memenuhi "usia-ibu-35"; "imt-35" otomatis memenuhi "obesitas".
TURUNAN = {"usia-ibu-40": "usia-ibu-35", "imt-35": "obesitas"}


def daftar_faktor():
    return {"perintah": "faktor-preeklampsia",
            "faktor": [{"kode": k, "label": v[0], "buku_kia_2023": v[1],
                        "nice_ng133": v[2] or "tidak tercantum"} for k, v in FAKTOR.items()],
            "sumber": [SUMBER["kia"], SUMBER["nice"]], "penafian": PENAFIAN}


def skrining_preeklampsia(faktor, sistolik=None, diastolik=None, usia_ibu=None, imt=None,
                          pedoman="kia"):
    if pedoman not in ("kia", "nice"):
        raise InputSalah("pedoman harus 'kia' atau 'nice'")
    kode = set()
    tidak_dikenal = []
    for f in faktor:
        f = f.strip().lower()
        if not f:
            continue
        if f in FAKTOR:
            kode.add(f)
        else:
            tidak_dikenal.append(f)
    if tidak_dikenal:
        raise InputSalah("kode faktor tidak dikenal: " + ", ".join(tidak_dikenal) +
                         " (lihat: python3 scripts/klinis.py faktor-preeklampsia)")
    turunan_otomatis = []
    hasil_map = None
    if (sistolik is None) != (diastolik is None):
        raise InputSalah("isi sistolik DAN diastolik untuk menghitung MAP")
    if sistolik is not None:
        hasil_map = hitung_map(sistolik, diastolik)
        if hasil_map["map_lebih_dari_90"]:
            if "map-90" not in kode:
                turunan_otomatis.append("map-90")
            kode.add("map-90")
    if usia_ibu is not None:
        u = desimal(usia_ibu, "usia ibu")
        if not Decimal(10) <= u <= Decimal(60):
            raise InputSalah(f"usia ibu {usia_ibu}: di luar rentang wajar 10-60 tahun")
        for batas, k in ((35, "usia-ibu-35"), (40, "usia-ibu-40")):
            if u >= batas and k not in kode:
                kode.add(k)
                turunan_otomatis.append(k)
    if imt is not None:
        i = bulat(desimal(imt, "IMT"))
        if not Decimal(10) <= i <= Decimal(80):
            raise InputSalah(f"IMT {imt}: di luar rentang wajar 10-80")
        for cek, k in ((i > 30, "obesitas"), (i >= 35, "imt-35")):
            if cek and k not in kode:
                kode.add(k)
                turunan_otomatis.append(k)
    tersirat = set()
    for a, b in TURUNAN.items():
        if a in kode and b not in kode:
            kode.add(b)
            tersirat.add(b)

    idx = 1 if pedoman == "kia" else 2
    tinggi = sorted(k for k in kode if FAKTOR[k][idx] == "tinggi")
    sedang = sorted(k for k in kode if FAKTOR[k][idx] == "sedang")
    # hindari hitung ganda faktor yang saling mencakup
    if pedoman == "kia":
        sedang = [k for k in sedang if k not in ("usia-ibu-40", "imt-35")]
    else:
        sedang = [k for k in sedang if FAKTOR[k][2] is not None]
    tidak_dinilai = sorted(k for k in kode - tersirat if FAKTOR[k][idx] is None)

    if tinggi:
        kategori = "RISIKO TINGGI"
        arti = ("Terdapat >= 1 faktor risiko tinggi. " +
                ("Sesuai Buku KIA 2023: pertimbangkan rujukan/konsultasi dokter (SpOG) dan "
                 "pemantauan sesuai PNPK/pedoman yang berlaku." if pedoman == "kia" else
                 "NICE NG133 menggolongkan ibu ini berisiko tinggi; pertimbangkan tata laksana "
                 "pencegahan sesuai pedoman - keputusan dokter."))
    elif len(sedang) >= 2:
        kategori = "RISIKO SEDANG (>= 2 faktor sedang)"
        arti = ("Terdapat >= 2 faktor risiko sedang. " +
                ("Sesuai Buku KIA 2023 memenuhi kriteria rujukan/konsultasi dokter; "
                 "pertimbangkan tindak lanjut sesuai PNPK/pedoman." if pedoman == "kia" else
                 "NICE NG133: > 1 faktor sedang termasuk kelompok yang dipertimbangkan untuk "
                 "pencegahan sesuai pedoman - keputusan dokter."))
    elif len(sedang) == 1:
        kategori = "1 FAKTOR RISIKO SEDANG"
        arti = ("Belum memenuhi kriteria (>= 2 sedang atau >= 1 tinggi). Lanjutkan ANC rutin, "
                "ukur tekanan darah tiap kunjungan, nilai ulang bila ada faktor baru.")
    else:
        kategori = "TIDAK DITEMUKAN FAKTOR RISIKO dari daftar yang diisi"
        arti = ("Tidak berarti bebas risiko; skrining hanya sebaik data yang diisi. "
                "Lanjutkan ANC rutin.")

    sumber = [SUMBER["kia"] if pedoman == "kia" else SUMBER["nice"]]
    if hasil_map:
        sumber.append(SUMBER["map"])
    catatan = []
    if tidak_dinilai:
        catatan.append("Faktor tidak termasuk daftar pedoman terpilih (tidak dihitung): " +
                       ", ".join(tidak_dinilai))
    if pedoman == "kia":
        catatan.append("Buku KIA: skrining dilakukan pada usia kehamilan < 20 minggu.")
    catatan.append("Keputusan terapi/obat pencegahan (termasuk dosis) BUKAN bagian alat ini - "
                   "ikuti PNPK/pedoman dan resep dokter.")
    return {
        "perintah": "preeklampsia", "pedoman": pedoman, "kategori": kategori, "arti": arti,
        "faktor_tinggi": [FAKTOR[k][0] for k in tinggi],
        "faktor_sedang": [FAKTOR[k][0] for k in sedang],
        "faktor_dari_angka": turunan_otomatis,
        "map": hasil_map["map_mmhg"] if hasil_map else None,
        "catatan": catatan, "sumber": sumber, "penafian": PENAFIAN,
    }


# ---------------------------------------------------------------- kehamilan

AMBANG_REDATING = [  # (usia USG sampai dengan [hari], selisih maksimum [hari]) - ACOG CO 700
    (8 * 7 + 6, 5), (13 * 7 + 6, 7), (15 * 7 + 6, 7), (21 * 7 + 6, 10), (27 * 7 + 6, 14),
    (10 ** 6, 21),
]


def trimester(hari):
    if hari <= 13 * 7 + 6:
        return "Trimester 1"
    if hari <= 27 * 7 + 6:
        return "Trimester 2"
    return "Trimester 3"


def kalkulator_kehamilan(hpht=None, siklus=28, tanggal_periksa=None, usg_tanggal=None,
                         usg_minggu=None, usg_hari=0, hari_ini=None):
    periksa = tanggal(tanggal_periksa, "tanggal periksa") if tanggal_periksa else (
        hari_ini or date.today())
    catatan = []
    hasil = {"perintah": "kehamilan", "tanggal_periksa": fmt_tgl(periksa)}
    try:
        siklus = int(str(siklus).strip())
    except ValueError:
        raise InputSalah(f"siklus '{siklus}' harus bilangan bulat (hari)")
    if not 21 <= siklus <= 45:
        raise InputSalah(f"siklus {siklus} hari di luar 21-45 hari: HPHT kurang andal, "
                         "pakai penanggalan USG")
    ga_hpht = hpl_hpht = None
    if hpht:
        h = tanggal(hpht, "HPHT")
        if h > periksa:
            raise InputSalah("HPHT tidak boleh setelah tanggal periksa")
        koreksi = siklus - 28
        # Naegele: +7 hari, lalu +9 bulan (setara -3 bulan +1 tahun)
        naeg, disesuaikan = tambah_bulan(h + timedelta(days=7), 9)
        naeg = naeg + timedelta(days=koreksi)
        hpl_hpht = h + timedelta(days=280 + koreksi)
        ga_hpht = (periksa - h).days - koreksi
        if ga_hpht < 0:
            raise InputSalah("dengan koreksi siklus, usia kehamilan negatif - cek HPHT/siklus")
        if ga_hpht > 44 * 7:
            raise InputSalah(f"usia kehamilan dari HPHT {minggu_hari(ga_hpht)} (> 44 minggu) - "
                             "cek tahun HPHT/tanggal periksa")
        hasil["hpht"] = fmt_tgl(h)
        hasil["siklus_hari"] = siklus
        hasil["hpl_naegele"] = fmt_tgl(naeg)
        hasil["hpl_280_hari"] = fmt_tgl(hpl_hpht)
        hasil["usia_kehamilan_hpht"] = minggu_hari(ga_hpht)
        if koreksi:
            catatan.append(f"Siklus {siklus} hari: HPL & usia kehamilan digeser {koreksi:+d} hari "
                           "(modifikasi umum Naegele; bukan bagian ACOG CO 700).")
        if disesuaikan:
            catatan.append("Tanggal +9 bulan tidak ada di kalender (mis. 31 Februari); "
                           "dibulatkan ke akhir bulan. Pakai HPL 280 hari sebagai acuan.")
        if naeg != hpl_hpht:
            catatan.append("HPL Naegele (kalender) dan HPHT+280 hari bisa berbeda 1-3 hari karena "
                           "panjang bulan berbeda; keduanya ditampilkan.")
    ga_usg = None
    if usg_tanggal or usg_minggu is not None:
        if not (usg_tanggal and usg_minggu is not None):
            raise InputSalah("untuk USG isi tanggal USG DAN usia kehamilan saat USG (minggu, hari)")
        ut = tanggal(usg_tanggal, "tanggal USG")
        if ut > periksa:
            raise InputSalah("tanggal USG tidak boleh setelah tanggal periksa")
        try:
            um, uh = int(usg_minggu), int(usg_hari or 0)
        except ValueError:
            raise InputSalah("usia kehamilan saat USG harus bilangan bulat minggu & hari")
        if not (0 <= uh <= 6 and 4 <= um <= 42):
            raise InputSalah("usia kehamilan saat USG harus 4-42 minggu dan 0-6 hari")
        usg_saat = um * 7 + uh
        ga_usg = usg_saat + (periksa - ut).days
        if ga_usg > 44 * 7:
            raise InputSalah("usia kehamilan dari USG > 44 minggu - cek tanggal USG")
        hpl_usg = ut + timedelta(days=280 - usg_saat)
        hasil["usg"] = f"{fmt_tgl(ut)}, usia {minggu_hari(usg_saat)}"
        hasil["hpl_usg"] = fmt_tgl(hpl_usg)
        hasil["usia_kehamilan_usg"] = minggu_hari(ga_usg)
        if hpht:
            ga_hpht_saat_usg = (ut - tanggal(hpht, "HPHT")).days - (siklus - 28)
            selisih = abs(ga_hpht_saat_usg - usg_saat)
            batas = next(b for s, b in AMBANG_REDATING if usg_saat <= s)
            pakai_usg = selisih > batas
            hasil["selisih_hpht_vs_usg_hari"] = selisih
            hasil["ambang_acog_hari"] = batas
            hasil["penanggalan_dipakai"] = "USG" if pakai_usg else "HPHT"
            catatan.append(
                f"Selisih HPHT vs USG {selisih} hari; ambang ACOG untuk USG usia "
                f"{minggu_hari(usg_saat)} adalah > {batas} hari -> "
                + ("pertimbangkan penanggalan ulang dengan USG." if pakai_usg else
                   "HPHT tetap dipakai."))
            if usg_saat > 21 * 7 + 6:
                catatan.append("USG pertama setelah 22 minggu: penanggalan kurang akurat "
                               "(ACOG menyebut suboptimal) - rencanakan pemantauan pertumbuhan.")
        else:
            hasil["penanggalan_dipakai"] = "USG"
    if ga_hpht is None and ga_usg is None:
        raise InputSalah("isi HPHT atau data USG")
    final = ga_usg if hasil.get("penanggalan_dipakai") == "USG" else ga_hpht
    hasil["usia_kehamilan"] = minggu_hari(final)
    hasil["trimester"] = trimester(final)
    hasil["catatan"] = catatan
    hasil["sumber"] = [SUMBER["naegele"], SUMBER["acog"]]
    hasil["penafian"] = PENAFIAN
    return hasil


# ---------------------------------------------------------------- IMT & kenaikan BB hamil

IOM = [  # (batas bawah IMT, label, total tunggal, total kembar, laju/minggu T2-T3)
    (Decimal("0"), "Berat badan kurang (< 18,5)", ("12,5", "18"), None, ("0,44", "0,58")),
    (Decimal("18.5"), "Normal (18,5-24,9)", ("11,5", "16"), ("17", "25"), ("0,35", "0,50")),
    (Decimal("25"), "Berat badan lebih (25,0-29,9)", ("7", "11,5"), ("14", "23"), ("0,23", "0,33")),
    (Decimal("30"), "Obesitas (>= 30,0)", ("5", "9"), ("11", "19"), ("0,17", "0,27")),
]


def hitung_imt(tinggi, berat):
    m = tinggi_m(tinggi)
    kg = berat_kg(berat)
    return bulat(kg / (m * m)), m, kg


def kategori_ap(i):
    if i < Decimal("18.5"):
        return "Berat badan kurang (< 18,5)"
    if i <= Decimal("22.9"):
        return "Normal (18,5-22,9)"
    if i <= Decimal("24.9"):
        return "Berat badan lebih / berisiko (23,0-24,9)"
    if i <= Decimal("29.9"):
        return "Obesitas I (25,0-29,9)"
    return "Obesitas II (>= 30,0)"


def kategori_kemenkes(i):
    if i < Decimal("17"):
        return "Kurus - kekurangan BB tingkat berat (< 17,0)"
    if i <= Decimal("18.4"):
        return "Kurus - kekurangan BB tingkat ringan (17,0-18,4)"
    if i <= Decimal("25"):
        return "Normal (18,5-25,0)"
    if i <= Decimal("27"):
        return "Gemuk - kelebihan BB tingkat ringan (25,1-27,0)"
    return "Gemuk - kelebihan BB tingkat berat / obesitas (> 27,0)"


def imt_dewasa(tinggi, berat, lingkar_perut=None, jk=None):
    i, m, kg = hitung_imt(tinggi, berat)
    hasil = {"perintah": "imt", "tinggi_cm": str(bulat(m * 100)), "berat_kg": str(kg),
             "imt": str(i), "kategori_asia_pasifik": kategori_ap(i),
             "kategori_kemenkes": kategori_kemenkes(i), "catatan": [],
             "sumber": [SUMBER["ap"], SUMBER["kemenkes_imt"]], "penafian": PENAFIAN}
    hasil["catatan"].append("IMT dibulatkan 1 desimal (setengah ke atas) lalu dikategorikan. "
                            "Hanya untuk dewasa >= 18 tahun, tidak untuk ibu hamil/anak.")
    if lingkar_perut is not None:
        lp = desimal(lingkar_perut, "lingkar perut")
        if not Decimal(40) <= lp <= Decimal(250):
            raise InputSalah(f"lingkar perut {lingkar_perut}: di luar rentang wajar 40-250 cm")
        jk = (jk or "").strip().upper()[:1]
        if jk not in ("L", "P"):
            raise InputSalah("isi jenis kelamin L atau P untuk menilai lingkar perut")
        batas = Decimal(90) if jk == "L" else Decimal(80)
        hasil["lingkar_perut_cm"] = str(lp)
        hasil["lingkar_perut"] = (f"{'>=' if lp >= batas else '<'} {batas} cm -> " +
                                  ("obesitas sentral (batas Asia-Pasifik)" if lp >= batas
                                   else "di bawah batas obesitas sentral"))
        if lp == batas:
            hasil["catatan"].append(f"Tepat {batas} cm: WPRO 2000 memakai >= {batas}; materi "
                                    f"Kemenkes menulis 'lebih dari {batas}'. Ukur ulang.")
    return hasil


def bb_hamil(tinggi, bb_prahamil, bb_sekarang=None, usia_minggu=None, kembar=False):
    i, m, kg = hitung_imt(tinggi, bb_prahamil)
    baris = [b for b in IOM if i >= b[0]][-1]
    _, label, total, total_kembar, laju = baris
    hasil = {"perintah": "bb-hamil", "imt_prahamil": str(i), "kategori_iom": label,
             "catatan": [], "sumber": [SUMBER["iom"]], "penafian": PENAFIAN}
    if kembar:
        if total_kembar is None:
            hasil["rekomendasi_total_kg"] = "Tidak ada rekomendasi IOM untuk IMT < 18,5 (kembar)"
        else:
            hasil["rekomendasi_total_kg"] = f"{total_kembar[0]}-{total_kembar[1]} kg (kembar, provisional IOM)"
    else:
        hasil["rekomendasi_total_kg"] = f"{total[0]}-{total[1]} kg"
        hasil["laju_trimester_2_3_kg_per_minggu"] = f"{laju[0]}-{laju[1]}"
    hasil["catatan"].append("IOM memakai batas IMT WHO internasional (bukan Asia-Pasifik).")
    if bb_sekarang is not None:
        sekarang = berat_kg(bb_sekarang, "BB sekarang")
        naik = sekarang - kg
        hasil["kenaikan_sejauh_ini_kg"] = str(bulat(naik))
        if usia_minggu is not None:
            u = desimal(usia_minggu, "usia kehamilan (minggu)")
            if not Decimal(0) <= u <= Decimal(44):
                raise InputSalah("usia kehamilan harus 0-44 minggu")
            hasil["usia_kehamilan_minggu"] = str(u)
            if not kembar and u > 13:
                lo = Decimal("0.5") + desimal(laju[0], "laju") * (u - 13)
                hi = Decimal("2") + desimal(laju[1], "laju") * (u - 13)
                hasil["perkiraan_rentang_saat_ini_kg"] = f"{bulat(lo)}-{bulat(hi)}"
                posisi = ("di bawah" if naik < bulat(lo) else "di atas" if naik > bulat(hi)
                          else "di dalam")
                hasil["posisi"] = f"Kenaikan {bulat(naik)} kg {posisi} perkiraan rentang"
                hasil["catatan"].append(
                    "Perkiraan rentang saat ini = turunan: trimester 1 0,5-2 kg + laju IOM x "
                    "(minggu - 13). Bukan tabel resmi; pakai sebagai gambaran kasar.")
    return hasil


# ---------------------------------------------------------------- kognitif (skor total saja)

def kognitif(instrumen, skor, pendidikan_tahun=None):
    ins = (instrumen or "").strip().lower().replace("-", "")
    try:
        s = int(str(skor).strip())
    except ValueError:
        raise InputSalah(f"skor '{skor}' harus bilangan bulat")
    hasil = {"perintah": "kognitif", "catatan": [], "penafian": PENAFIAN}
    if ins in ("mmse",):
        if not 0 <= s <= 30:
            raise InputSalah("skor MMSE harus 0-30")
        if s >= 24:
            kat = "24-30: tidak ada indikasi gangguan kognitif pada skrining ini"
        elif s >= 18:
            kat = "18-23: di bawah batas skrining (rentang ringan) - pertimbangkan evaluasi lanjut"
        else:
            kat = "0-17: di bawah batas skrining (rentang berat) - pertimbangkan evaluasi lanjut"
        hasil.update(instrumen="MMSE", skor=s, interpretasi=kat, sumber=[SUMBER["mmse"]])
        hasil["catatan"].append("Skor dipengaruhi pendidikan, bahasa, dan gangguan sensorik. "
                                "MMSE berhak cipta (PAR Inc.) - skill ini tidak memuat butir tes.")
    elif ins in ("moca", "mocaina"):
        if not 0 <= s <= 30:
            raise InputSalah("skor MoCA harus 0-30")
        if pendidikan_tahun is None:
            raise InputSalah("MoCA butuh lama pendidikan (tahun) untuk koreksi +1 poin")
        p = int(pendidikan_tahun)
        if not 0 <= p <= 30:
            raise InputSalah("lama pendidikan harus 0-30 tahun")
        tambah = 1 if (p <= 12 and s < 30) else 0
        akhir = s + tambah
        kat = ("normal pada skrining ini (>= 26)" if akhir >= 26 else
               "di bawah batas skrining 26 - pertimbangkan evaluasi lanjut")
        hasil.update(instrumen="MoCA / MoCA-Ina", skor_mentah=s, koreksi_pendidikan=tambah,
                     skor_akhir=akhir, interpretasi=kat, sumber=[SUMBER["moca"]])
        hasil["catatan"].append("MoCA mewajibkan pelatihan & sertifikasi pemeriksa (sejak 2019). "
                                "Skill ini hanya menafsirkan skor total yang Anda masukkan.")
        hasil["catatan"].append("Batas 26 adalah versi asli; studi validasi MoCA-Ina 2010 belum "
                                "menetapkan batas khusus Indonesia.")
        if p <= 12 and s == 30:
            hasil["catatan"].append("Skor sudah maksimum 30; koreksi tidak menambah.")
    elif ins in ("amt", "amts"):
        if not 0 <= s <= 10:
            raise InputSalah("skor AMT harus 0-10")
        kat = ("8-10: normal" if s >= 8 else
               "4-7: gangguan ingatan sedang pada skrining - pertimbangkan evaluasi lanjut"
               if s >= 4 else
               "0-3: gangguan ingatan berat pada skrining - pertimbangkan evaluasi lanjut")
        hasil.update(instrumen="AMT (Abbreviated Mental Test)", skor=s, interpretasi=kat,
                     sumber=[SUMBER["amt"]])
    else:
        raise InputSalah("instrumen harus mmse, moca, atau amt")
    hasil["catatan"].append("Hasil skrining bukan diagnosis demensia/gangguan kognitif.")
    return hasil


# ---------------------------------------------------------------- tampilan

LABEL = {
    "map_mmhg": "MAP (mmHg)", "map_lebih_dari_90": "MAP > 90", "kategori": "KATEGORI",
    "arti": "Arti", "faktor_tinggi": "Faktor risiko tinggi", "faktor_sedang": "Faktor risiko sedang",
    "faktor_dari_angka": "Faktor terisi otomatis dari angka", "hpl_naegele": "HPL (Naegele)",
    "hpl_280_hari": "HPL (HPHT + 280 hari)", "hpl_usg": "HPL (USG)",
    "usia_kehamilan": "USIA KEHAMILAN DIPAKAI", "penanggalan_dipakai": "Penanggalan dipakai",
    "map": "MAP (mmHg)", "hpht": "HPHT", "usg": "USG", "siklus_hari": "Siklus (hari)",
    "usia_kehamilan_hpht": "Usia kehamilan menurut HPHT",
    "usia_kehamilan_usg": "Usia kehamilan menurut USG",
    "selisih_hpht_vs_usg_hari": "Selisih HPHT vs USG (hari)",
    "ambang_acog_hari": "Ambang ACOG (hari)", "imt": "IMT (kg/m2)",
    "imt_prahamil": "IMT pra-hamil (kg/m2)", "kategori_iom": "Kategori IMT (IOM)",
    "kategori_asia_pasifik": "Kategori Asia-Pasifik", "kategori_kemenkes": "Kategori Kemenkes",
    "rekomendasi_total_kg": "Rekomendasi kenaikan total",
    "laju_trimester_2_3_kg_per_minggu": "Laju trimester 2-3 (kg/minggu)",
    "kenaikan_sejauh_ini_kg": "Kenaikan sejauh ini (kg)",
    "perkiraan_rentang_saat_ini_kg": "Perkiraan rentang saat ini (kg)",
    "tinggi_cm": "Tinggi (cm)", "berat_kg": "Berat (kg)", "lingkar_perut_cm": "Lingkar perut (cm)",
    "usia_kehamilan_minggu": "Usia kehamilan (minggu)",
}


def cetak(h):
    for k, v in h.items():
        if k in ("perintah", "catatan", "sumber", "penafian"):
            continue
        if isinstance(v, bool):
            v = "ya" if v else "tidak"
        if isinstance(v, list):
            if k == "faktor":
                for f in v:
                    print(f"  {f['kode']:<22} KIA: {f['buku_kia_2023']:<7} NICE: "
                          f"{f['nice_ng133']:<16} {f['label']}")
                continue
            v = "; ".join(v) if v else "-"
        if v is None:
            continue
        print(f"{LABEL.get(k, k.replace('_', ' ').capitalize())}: {v}")
    for c in h.get("catatan", []):
        print(f"Catatan: {c}")
    for s in h.get("sumber", []):
        print(f"Sumber: {s}")
    print(f"PENTING: {h['penafian']}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Kalkulator klinis untuk tenaga kesehatan (v" + VERSI + ")")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="perintah", required=True)
    a = sub.add_parser("map")
    a.add_argument("--sistolik", required=True)
    a.add_argument("--diastolik", required=True)
    sub.add_parser("faktor-preeklampsia")
    a = sub.add_parser("preeklampsia")
    a.add_argument("--faktor", default="")
    a.add_argument("--sistolik")
    a.add_argument("--diastolik")
    a.add_argument("--usia-ibu")
    a.add_argument("--imt")
    a.add_argument("--pedoman", default="kia", choices=["kia", "nice"])
    a = sub.add_parser("kehamilan")
    a.add_argument("--hpht")
    a.add_argument("--siklus", default="28")
    a.add_argument("--tanggal-periksa")
    a.add_argument("--usg-tanggal")
    a.add_argument("--usg-minggu")
    a.add_argument("--usg-hari", default="0")
    a = sub.add_parser("bb-hamil")
    a.add_argument("--tinggi", required=True)
    a.add_argument("--bb-prahamil", required=True)
    a.add_argument("--bb-sekarang")
    a.add_argument("--usia-minggu")
    a.add_argument("--kembar", action="store_true")
    a = sub.add_parser("imt")
    a.add_argument("--tinggi", required=True)
    a.add_argument("--berat", required=True)
    a.add_argument("--lingkar-perut")
    a.add_argument("--jk")
    a = sub.add_parser("kognitif")
    a.add_argument("--instrumen", required=True)
    a.add_argument("--skor", required=True)
    a.add_argument("--pendidikan-tahun")
    ar = p.parse_args(argv)
    try:
        if ar.perintah == "map":
            h = hitung_map(ar.sistolik, ar.diastolik)
        elif ar.perintah == "faktor-preeklampsia":
            h = daftar_faktor()
        elif ar.perintah == "preeklampsia":
            h = skrining_preeklampsia(ar.faktor.split(","), ar.sistolik, ar.diastolik,
                                      ar.usia_ibu, ar.imt, ar.pedoman)
        elif ar.perintah == "kehamilan":
            h = kalkulator_kehamilan(ar.hpht, ar.siklus, ar.tanggal_periksa, ar.usg_tanggal,
                                     ar.usg_minggu, ar.usg_hari)
        elif ar.perintah == "bb-hamil":
            h = bb_hamil(ar.tinggi, ar.bb_prahamil, ar.bb_sekarang, ar.usia_minggu, ar.kembar)
        elif ar.perintah == "imt":
            h = imt_dewasa(ar.tinggi, ar.berat, ar.lingkar_perut, ar.jk)
        else:
            pend = None
            if ar.pendidikan_tahun is not None:
                try:
                    pend = int(ar.pendidikan_tahun)
                except ValueError:
                    raise InputSalah("lama pendidikan harus bilangan bulat tahun")
            h = kognitif(ar.instrumen, ar.skor, pend)
    except InputSalah as e:
        print(f"Input tidak valid: {e}", file=sys.stderr)
        return 1
    if ar.json:
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        cetak(h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
