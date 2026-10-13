#!/usr/bin/env python3
"""Kalkulator klinis untuk TENAGA KESEHATAN (alat bantu keputusan, bukan diagnosis).

Hanya library standar Python. Tanpa internet, tanpa menyimpan data apa pun.

Perintah (jalankan dari folder skill; Windows: ganti python3 dengan python atau py):
  python3 scripts/klinis.py map --sistolik 120 --diastolik 80
  python3 scripts/klinis.py faktor-preeklampsia                 # daftar kode faktor
  python3 scripts/klinis.py preeklampsia --faktor nullipara,obesitas --sistolik 118 --diastolik 82 [--gejala pandangan-kabur]
  python3 scripts/klinis.py kehamilan --hpht 2026-03-10 [--siklus 30] [--tanggal-periksa 2026-09-29]
                                      [--usg-tanggal 2026-05-02 --usg-minggu 7 --usg-hari 3]
  python3 scripts/klinis.py bb-hamil --tinggi 155 --bb-prahamil 62 [--bb-sekarang 68 --usia-minggu 24] [--kembar]
  python3 scripts/klinis.py imt --tinggi 165 --berat 72 [--lingkar-perut 92 --jk L]
  python3 scripts/klinis.py imt-batch --file pasien.csv       # kolom: id,tinggi,berat[,lingkar_perut,jk]
  python3 scripts/klinis.py kognitif --instrumen moca --skor 24 --pendidikan-tahun 9

Tambahkan --json SEBELUM sub-perintah untuk keluaran JSON (mis. klinis.py --json imt ...).
Kode keluar 1 = input tidak valid (pesan jelas di stderr). Pada map/preeklampsia, kode
gejala/faktor tak dikenal TIDAK membatalkan tanda bahaya: hasil dicetak dulu, lalu kode tak
dikenal + daftar kode valid di stderr, baru keluar 1.
Setiap hasil memuat sumber pedoman + tahun dan kalimat "alat bantu, bukan pengganti penilaian klinis".
"""
import argparse
import calendar
import json
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from fractions import Fraction

VERSI = "1.0.6"
PENAFIAN = ("Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. "
            "Keputusan klinis tetap pada dokter/bidan yang memeriksa.")

SUMBER = {
    "kia": "Kemenkes RI, Buku Kesehatan Ibu dan Anak (Buku KIA) edisi terbaru - cetakan Ditjen "
           "Kesehatan Primer dan Komunitas 2025 (ISBN 978-623-301-149-5) - lembar skrining "
           "preeklampsia usia kehamilan < 20 minggu",
    "nice": "NICE NG133 Hypertension in pregnancy: diagnosis and management (2019, "
            "diperbarui 2023) - rekomendasi 1.1.2-1.1.3 faktor risiko preeklampsia",
    "map": "Rumus MAP = (sistolik + 2 x diastolik) / 3; ambang MAP >= 90 mmHg dari Buku KIA "
           "(cetakan 2025)",
    "bahaya_td": "NICE NG133 (2019, diperbarui 2023) - definisi hipertensi dalam kehamilan "
                 "(>= 140/90 mmHg) dan hipertensi berat (>= 160/110 mmHg); ACOG Practice "
                 "Bulletin No. 222 Gestational Hypertension and Preeclampsia (2020) - "
                 "rentang berat >= 160 sistolik atau >= 110 diastolik",
    "bahaya_gejala": "Buku KIA (cetakan 2025) - tanda bahaya pada ibu hamil; NICE NG133 "
                     "(2019, diperbarui 2023) - gejala preeklampsia berat",
    "td_rendah": "NHLBI (NIH), Low Blood Pressure - definisi TD rendah < 90/60 mmHg (halaman "
                 "diperbarui 24 Mar 2022, https://www.nhlbi.nih.gov/health/low-blood-pressure); "
                 "ambang sistolik < 90 atau diastolik < 60 dipakai sebagai penanda konservatif "
                 "(PERLU REVIEW tenaga medis)",
    "naegele": "Aturan Naegele (HPHT + 7 hari - 3 bulan + 1 tahun); penyesuaian siklus = "
               "modifikasi umum (siklus - 28 hari)",
    "acog": "ACOG Committee Opinion No. 700 Methods for Estimating the Due Date (2017, "
            "reaffirmed 2025)",
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


# ---------------------------------------------------------------- MAP & tanda bahaya

def baca_td(sistolik, diastolik, boleh_parsial=False):
    """Validasi TD. Dengan boleh_parsial=True salah satu boleh None (tidak diisi)."""
    if sistolik is None and diastolik is None:
        raise InputSalah("isi sistolik dan/atau diastolik")
    if not boleh_parsial and (sistolik is None or diastolik is None):
        raise InputSalah("isi sistolik DAN diastolik")
    s = d = None
    if sistolik is not None:
        s = desimal(sistolik, "sistolik")
        if not (Decimal(50) <= s <= Decimal(300)):
            raise InputSalah(f"sistolik {sistolik}: di luar rentang wajar 50-300 mmHg")
    if diastolik is not None:
        d = desimal(diastolik, "diastolik")
        if not (Decimal(20) <= d <= Decimal(200)):
            raise InputSalah(f"diastolik {diastolik}: di luar rentang wajar 20-200 mmHg")
    if s is not None and d is not None and d >= s:
        raise InputSalah("diastolik harus lebih kecil dari sistolik (mungkin tertukar?)")
    return s, d


def teks_td(s, d):
    return f"{s if s is not None else '?'}/{d if d is not None else '?'}"


def catatan_td_parsial(s, d):
    """Kalimat untuk TD yang hanya terisi sebagian (None bila lengkap/kosong)."""
    if s is not None and d is None:
        return ("Diastolik TIDAK diisi: ambang tanda bahaya hanya dinilai dari sistolik; MAP "
                "tidak dihitung. Ukur/lengkapi diastolik sebelum menyimpulkan.")
    if d is not None and s is None:
        return ("Sistolik TIDAK diisi: ambang tanda bahaya hanya dinilai dari diastolik; MAP "
                "tidak dihitung. Ukur/lengkapi sistolik sebelum menyimpulkan.")
    return None


# Tanda bahaya: diperiksa SEBELUM saran rutin apa pun. PERLU REVIEW tenaga medis.
GEJALA_BAHAYA = {
    "nyeri-kepala-hebat": "Nyeri kepala hebat / tidak hilang",
    "pandangan-kabur": "Gangguan penglihatan / pandangan kabur",
    "nyeri-ulu-hati": "Nyeri ulu hati / perut kanan atas",
    "kejang": "Kejang",
    "penurunan-kesadaran": "Penurunan kesadaran",
    "sesak": "Sesak napas",
    "bengkak-mendadak": "Bengkak mendadak pada wajah/tangan/kaki",
    "perdarahan": "Perdarahan dari jalan lahir",
    "ketuban-pecah": "Air ketuban keluar sebelum waktunya",
    "gerak-janin-berkurang": "Gerakan janin berkurang / tidak terasa",
    "demam-tinggi": "Demam tinggi",
    "muntah-terus": "Muntah terus-menerus, tidak bisa makan/minum",
}


def baca_gejala(gejala):
    """Kembalikan (kode dikenal, kode tidak dikenal). Kode tak dikenal TIDAK menghentikan
    pemeriksaan tanda bahaya; pemanggil melaporkannya setelah hasil dicetak."""
    kode, salah = [], []
    for g in gejala or []:
        g = g.strip().lower()
        if not g:
            continue
        (kode if g in GEJALA_BAHAYA else salah).append(g)
    return sorted(set(kode)), salah


def cek_tanda_bahaya(s=None, d=None, gejala=()):
    """Lapisan tanda bahaya generik. Mengembalikan None bila tidak ada tanda bahaya.

    - TD >= 160 sistolik ATAU >= 110 diastolik, atau ada gejala bahaya -> SEGERA evaluasi/rujuk.
    - TD >= 140 sistolik ATAU >= 90 diastolik -> evaluasi hipertensi & rujuk/konsultasi HARI INI.
    - TD < 90 sistolik ATAU < 60 diastolik -> TD rendah, evaluasi klinis (PERLU REVIEW medis).
    Semuanya TIDAK PERNAH boleh berakhir dengan saran 'ANC rutin'.
    s atau d boleh None (TD parsial): nilai yang ada tetap dinilai.
    """
    alasan, sumber = [], []
    berat = hipertensi = rendah = False
    tinggi_s = s is not None and s >= 160
    tinggi_d = d is not None and d >= 110
    ht_s = s is not None and s >= 140
    ht_d = d is not None and d >= 90
    if s is not None or d is not None:
        td = teks_td(s, d)
        if tinggi_s or tinggi_d:
            berat = True
            alasan.append(f"TD {td} mmHg dalam rentang BERAT (>= 160 sistolik atau >= 110 "
                          "diastolik)")
            sumber.append(SUMBER["bahaya_td"])
        elif ht_s or ht_d:
            hipertensi = True
            alasan.append(f"TD {td} mmHg dalam rentang hipertensi (>= 140 sistolik atau >= 90 "
                          "diastolik)")
            sumber.append(SUMBER["bahaya_td"])
        if (s is not None and s < 90) or (d is not None and d < 60):
            rendah = True
            alasan.append(f"TD {td} mmHg RENDAH (< 90 sistolik atau < 60 diastolik) - TD rendah, "
                          "evaluasi klinis sesuai protokol (nilai perdarahan, dehidrasi, syok; "
                          "PERLU REVIEW medis)")
            sumber.append(SUMBER["td_rendah"])
    if gejala:
        berat = True
        alasan.append("Gejala bahaya: " + "; ".join(GEJALA_BAHAYA[g] for g in gejala))
        sumber.append(SUMBER["bahaya_gejala"])
    if not alasan:
        return None
    if berat:
        kategori = "TANDA BAHAYA - SEGERA EVALUASI/RUJUK"
        tindak = ("SEGERA evaluasi/rujuk sesuai protokol kegawatdaruratan fasilitas Anda "
                  "(jangan menunggu kunjungan berikutnya).")
    elif hipertensi:
        kategori = "TD RENTANG HIPERTENSI - EVALUASI/RUJUK HARI INI"
        tindak = ("Ukur ulang sesuai prosedur baku, lalu segera evaluasi/rujuk atau konsultasi "
                  "dokter sesuai protokol fasilitas HARI INI: nilai hipertensi dalam kehamilan "
                  "(kronik bila < 20 minggu; gestasional/preeklampsia bila >= 20 minggu - cek "
                  "proteinuria & gejala). Tidak cukup ditangani sebagai kunjungan rutin.")
    else:
        kategori = "TD RENDAH - EVALUASI KLINIS SESUAI PROTOKOL"
        tindak = ("TD rendah - ukur ulang sesuai prosedur baku lalu evaluasi klinis sesuai "
                  "protokol fasilitas HARI INI (nilai keadaan umum, nadi, perdarahan, "
                  "dehidrasi, tanda syok). Tidak cukup ditangani sebagai kunjungan rutin. "
                  "Ambang < 90/60 PERLU REVIEW tenaga medis.")
    if rendah and (berat or hipertensi):
        tindak += " Juga ada komponen TD rendah - evaluasi klinis sesuai protokol."
    return {"kategori": kategori, "alasan": alasan, "tindak_lanjut": tindak, "sumber": sumber}


def hitung_map(sistolik, diastolik, gejala=None, boleh_parsial=False):
    """MAP + lapisan tanda bahaya. boleh_parsial=True (CLI): bila hanya satu nilai TD diisi,
    tanda bahaya tetap dinilai dari nilai yang ada; MAP tidak dihitung."""
    s, d = baca_td(sistolik, diastolik, boleh_parsial)
    kode_gejala, gejala_salah = baca_gejala(gejala)
    hasil = {"perintah": "map", "tanda_bahaya": None, "peringatan": None,
             "sistolik": str(s) if s is not None else "tidak diisi",
             "diastolik": str(d) if d is not None else "tidak diisi",
             "map_mmhg": None, "map_90_atau_lebih": None, "catatan": [],
             "sumber": [], "penafian": PENAFIAN}
    parsial = catatan_td_parsial(s, d)
    if parsial:
        hasil["peringatan"] = parsial
    else:
        tepat = (Fraction(s) + 2 * Fraction(d)) / 3  # dibandingkan tanpa pembulatan
        tampil = bulat(Decimal(tepat.numerator) / Decimal(tepat.denominator))
        hasil["map_mmhg"] = str(tampil)
        hasil["map_90_atau_lebih"] = tepat >= 90
        hasil["catatan"].append("Dibandingkan dengan nilai tepat (tanpa pembulatan) terhadap "
                                "ambang Buku KIA MAP >= 90. Ukur ulang sesuai prosedur baku bila "
                                "hasil di sekitar 90.")
        hasil["sumber"].append(SUMBER["map"])
    bahaya = cek_tanda_bahaya(s, d, kode_gejala)
    if bahaya:
        hasil["tanda_bahaya"] = (bahaya["kategori"] + ": " + "; ".join(bahaya["alasan"]) +
                                 ". Bila pasien hamil: " + bahaya["tindak_lanjut"])
        hasil["sumber"] += bahaya["sumber"]
    if gejala_salah:
        hasil["kode_tidak_dikenal"] = ["gejala: " + g for g in gejala_salah]
        hasil["catatan"].append("Ada kode gejala tidak dikenal (belum dinilai): " +
                                ", ".join(gejala_salah) + ". Petakan ke kode yang valid dan "
                                "jalankan ulang; gejala itu bisa jadi tanda bahaya.")
    if not hasil["sumber"]:
        hasil["sumber"].append(SUMBER["bahaya_td"])
    return hasil


# ---------------------------------------------------------------- preeklampsia

FAKTOR = {
    # kode: (label, kategori Buku KIA (cetakan 2025) atau None, kategori NICE NG133 atau None)
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
    "map-90": ("MAP >= 90 mmHg", "sedang", None),
    "proteinuria": ("Proteinuria (dipstik > +1 pada 2 kali periksa berjarak 6 jam, atau "
                    "kuantitatif 300 mg/24 jam)", "sedang", None),
    "riwayat-preeklampsia": ("Multipara dengan riwayat preeklampsia sebelumnya", "tinggi", "tinggi"),
    "riwayat-hipertensi-kehamilan": ("Hipertensi pada kehamilan sebelumnya TANPA diagnosis "
                                     "preeklampsia (mis. hipertensi gestasional)", None, "tinggi"),
    "kehamilan-multipel": ("Kehamilan multipel (kembar)", "tinggi", "sedang"),
    "diabetes-pregestasional": ("Diabetes melitus tipe 1 atau 2 (sudah ada sebelum hamil)",
                                "tinggi", "tinggi"),
    "diabetes-gestasional": ("Diabetes yang pertama kali muncul saat hamil (gestasional)",
                             "tinggi", None),
    "diabetes": ("Diabetes dalam kehamilan (jenis tidak disebut)", "tinggi", None),
    "hipertensi-kronik": ("Hipertensi kronik", "tinggi", "tinggi"),
    "penyakit-ginjal": ("Penyakit ginjal (kronik)", "tinggi", "tinggi"),
    "autoimun": ("Penyakit autoimun / SLE", "tinggi", "tinggi"),
    "antifosfolipid": ("Sindrom antifosfolipid (APS)", "tinggi", "tinggi"),
}
# "usia-ibu-40" otomatis juga memenuhi "usia-ibu-35"; "imt-35" otomatis memenuhi "obesitas".
TURUNAN = {"usia-ibu-40": "usia-ibu-35", "imt-35": "obesitas"}
NAMA_PEDOMAN = {"kia": "Buku KIA (cetakan 2025)", "nice": "NICE NG133"}
ATURAN = {
    "kia": "Buku KIA (cetakan 2025): >= 2 faktor risiko sedang dan/atau >= 1 faktor risiko "
           "tinggi -> ibu berisiko preeklampsia -> rujukan terencana.",
    "nice": "NICE NG133 (rek. 1.1.2): >= 1 faktor risiko tinggi atau > 1 faktor risiko sedang.",
}


def daftar_faktor():
    return {"perintah": "faktor-preeklampsia",
            "faktor": [{"kode": k, "label": v[0], "buku_kia": v[1] or "tidak tercantum",
                        "nice_ng133": v[2] or "tidak tercantum"} for k, v in FAKTOR.items()],
            "gejala_bahaya": [f"{k} = {v}" for k, v in GEJALA_BAHAYA.items()],
            "catatan": ["Kode 'diabetes' hanya untuk pedoman KIA bila jenis tidak diketahui; "
                        "untuk NICE pakai diabetes-pregestasional atau diabetes-gestasional.",
                        "Gejala bahaya dipakai lewat --gejala; bila ada, hasil selalu "
                        "'SEGERA EVALUASI/RUJUK'."],
            "sumber": [SUMBER["kia"], SUMBER["nice"]], "penafian": PENAFIAN}


def skrining_preeklampsia(faktor, sistolik=None, diastolik=None, usia_ibu=None, imt=None,
                          pedoman="kia", gejala=None):
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
    masalah_kode = ["faktor: " + f for f in tidak_dikenal]
    if pedoman == "nice" and "diabetes" in kode:
        kode.discard("diabetes")
        masalah_kode.append("faktor: diabetes (pedoman NICE membedakan jenis: pakai "
                            "diabetes-pregestasional untuk DM tipe 1/2 atau diabetes-gestasional)")
    kode_gejala, gejala_salah = baca_gejala(gejala)
    masalah_kode += ["gejala: " + g for g in gejala_salah]
    turunan_otomatis = []
    hasil_map = None
    s = d = None
    td_parsial = None
    if sistolik is not None or diastolik is not None:
        s, d = baca_td(sistolik, diastolik, boleh_parsial=True)
        td_parsial = catatan_td_parsial(s, d)
    if s is not None and d is not None:
        hasil_map = hitung_map(s, d)
        if hasil_map["map_90_atau_lebih"]:
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

    # 1) LAPISAN TANDA BAHAYA - diperiksa sebelum saran rutin apa pun.
    bahaya = cek_tanda_bahaya(s, d, kode_gejala)

    # 2) Klasifikasi faktor risiko menurut SATU pedoman terpilih (tidak dicampur).
    idx = 1 if pedoman == "kia" else 2
    tinggi = sorted(k for k in kode if FAKTOR[k][idx] == "tinggi")
    sedang = sorted(k for k in kode if FAKTOR[k][idx] == "sedang")
    if pedoman == "kia":  # hindari hitung ganda faktor yang saling mencakup
        sedang = [k for k in sedang if k not in ("usia-ibu-40", "imt-35")]
    tidak_dinilai = sorted(k for k in kode - tersirat if FAKTOR[k][idx] is None)

    nama = NAMA_PEDOMAN[pedoman]
    berisiko = bool(tinggi) or len(sedang) >= 2
    if tinggi:
        kategori_faktor = f"RISIKO TINGGI (>= 1 faktor tinggi) - {nama}"
    elif len(sedang) >= 2:
        # Label sesuai makna pedoman: >= 2 faktor sedang = "ibu berisiko preeklampsia"
        # (Buku KIA) -> rujukan terencana; BUKAN "risiko menengah".
        if pedoman == "kia":
            kategori_faktor = ("BERISIKO PREEKLAMPSIA - perlu rujukan terencana "
                               f"(>= 2 faktor risiko sedang) - {nama}")
        else:
            kategori_faktor = ("BERISIKO PREEKLAMPSIA - memenuhi kriteria risiko "
                               f"(> 1 faktor risiko sedang) - {nama}")
    elif len(sedang) == 1:
        kategori_faktor = f"1 FAKTOR RISIKO SEDANG - {nama}"
    else:
        kategori_faktor = "TIDAK DITEMUKAN FAKTOR RISIKO dari daftar yang diisi"
    if berisiko:
        arti_faktor = (
            "Memenuhi kriteria ibu berisiko preeklampsia menurut Buku KIA. Buku KIA: pemeriksaan "
            "kehamilan, proses melahirkan, dan pemeriksaan nifas dilaksanakan di Rumah Sakit; "
            "lakukan rujukan terencana (tidak perlu menunggu inpartu). Pelaksanaan sesuai "
            "protokol fasilitas & keputusan dokter." if pedoman == "kia" else
            "Memenuhi kriteria risiko NICE NG133; pertimbangkan tata laksana pencegahan dan "
            "rencana pemantauan sesuai pedoman - keputusan dokter.")
    elif len(sedang) == 1:
        arti_faktor = ("Belum memenuhi kriteria rujukan (" + ATURAN[pedoman] + ") Lanjutkan ANC "
                       "rutin, ukur tekanan darah tiap kunjungan, nilai ulang bila ada faktor baru.")
    else:
        arti_faktor = ("Tidak berarti bebas risiko; skrining hanya sebaik data yang diisi. "
                       "Lanjutkan ANC rutin.")
    # Jangan pernah "Lanjutkan ANC rutin" polos bila TD belum lengkap / ada kode tak dikenal.
    peringatan = []
    if s is None and d is None and not kode_gejala:
        peringatan.append("Tanda bahaya (TD/gejala) belum diperiksa - ukur TD dan tanyakan gejala "
                          "bahaya sebelum menyimpulkan.")
    elif td_parsial:
        peringatan.append(td_parsial)
    if masalah_kode:
        peringatan.append("Ada kode tidak dikenal (" + "; ".join(masalah_kode) + ") - belum "
                          "dinilai; kategori bisa berubah setelah kode diperbaiki.")
    if peringatan and not berisiko:
        arti_faktor = arti_faktor.replace(
            "Lanjutkan ANC", "Hanya bila TD lengkap & gejala bahaya sudah diperiksa dan normal: "
            "lanjutkan ANC")

    sumber = [SUMBER[pedoman]]
    if hasil_map:
        sumber.append(SUMBER["map"])
    if bahaya:
        kategori = bahaya["kategori"]
        arti = (bahaya["tindak_lanjut"] + " Skrining faktor risiko di bawah hanya pelengkap, "
                "bukan pengganti penanganan ini.")
        if berisiko:
            arti += " Faktor risiko: " + arti_faktor
        tanda = "; ".join(bahaya["alasan"])
        sumber += [x for x in bahaya["sumber"] if x not in sumber]
    else:
        kategori, arti, tanda = kategori_faktor, arti_faktor, None

    catatan = ["Aturan kategori: " + ATURAN[pedoman] +
               " Hanya faktor dari daftar pedoman ini yang dihitung (tidak dicampur)."]
    if bahaya:
        catatan.append("Tanda bahaya diperiksa lebih dulu (sumber ambang/gejala: lihat baris "
                       "Sumber); saran kunjungan rutin tidak berlaku.")
    for k in tidak_dinilai:
        lain = "nice" if pedoman == "kia" else "kia"
        kat_lain = FAKTOR[k][2 if lain == "nice" else 1]
        catatan.append(f"'{FAKTOR[k][0]}' tidak tercantum di {nama} (tidak dihitung)" +
                       (f"; di {NAMA_PEDOMAN[lain]} = faktor {kat_lain} - pertimbangkan klinis."
                        if kat_lain else "."))
    belum = [nm for nm, ks in (("hipertensi kronik", ("hipertensi-kronik",)),
                               ("diabetes", ("diabetes-pregestasional", "diabetes-gestasional", "diabetes")),
                               ("penyakit ginjal", ("penyakit-ginjal",)),
                               ("autoimun/APS", ("autoimun", "antifosfolipid")))
             if not any(x in kode for x in ks)]
    if belum:
        catatan.append("Belum ditanyakan (anggap tidak ada, konfirmasi ke pasien): " + ", ".join(belum) + ".")
    if pedoman == "kia":
        catatan.append("Buku KIA: skrining dilakukan pada usia kehamilan < 20 minggu.")
    catatan.append("Keputusan terapi/obat pencegahan (termasuk dosis) BUKAN bagian alat ini - "
                   "ikuti PNPK/pedoman dan resep dokter.")
    hasil = {
        "perintah": "preeklampsia", "pedoman": nama, "tanda_bahaya": tanda,
        "peringatan": " ".join(peringatan) or None,
        "kategori": kategori, "arti": arti,
        "kategori_faktor_risiko": kategori_faktor if bahaya else None,
        "faktor_tinggi": [FAKTOR[k][0] for k in tinggi],
        "faktor_sedang": [FAKTOR[k][0] for k in sedang],
        "faktor_dari_angka": turunan_otomatis,
        "map": hasil_map["map_mmhg"] if hasil_map else None,
        "catatan": catatan, "sumber": sumber, "penafian": PENAFIAN,
    }
    if masalah_kode:
        hasil["kode_tidak_dikenal"] = masalah_kode
    return hasil


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
    ada_usg = bool(usg_tanggal) and usg_minggu is not None
    ga_hpht = hpl_hpht = None
    if hpht and not 21 <= siklus <= 45:
        if not ada_usg:
            raise InputSalah(f"siklus {siklus} hari di luar 21-45 hari: HPHT kurang andal, "
                             "pakai penanggalan USG (isi tanggal USG & usia saat USG)")
        catatan.append(f"Siklus {siklus} hari di luar 21-45 hari: HPHT TIDAK ANDAL, tidak "
                       "dipakai; penanggalan memakai USG.")
        hpht = None
    if hpht:
        h = tanggal(hpht, "HPHT")
        if h > periksa:
            raise InputSalah("HPHT tidak boleh setelah tanggal periksa")
        koreksi = siklus - 28
        ga_cek = (periksa - h).days - koreksi
        if ga_cek < 0:
            raise InputSalah("dengan koreksi siklus, usia kehamilan negatif - cek HPHT/siklus")
        if ga_cek > 44 * 7:
            if not ada_usg:
                raise InputSalah(f"usia kehamilan dari HPHT {minggu_hari(ga_cek)} (> 44 minggu) - "
                                 "cek tahun HPHT/tanggal periksa")
            catatan.append(f"Usia kehamilan dari HPHT {minggu_hari(ga_cek)} (> 44 minggu): HPHT "
                           "TIDAK ANDAL (cek tahun HPHT), tidak dipakai; penanggalan memakai USG.")
            hpht = None
    if hpht:
        # Naegele: +7 hari, lalu +9 bulan (setara -3 bulan +1 tahun)
        naeg, disesuaikan = tambah_bulan(h + timedelta(days=7), 9)
        naeg = naeg + timedelta(days=koreksi)
        hpl_hpht = h + timedelta(days=280 + koreksi)
        ga_hpht = ga_cek
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
    hasil["sumber"] = ([SUMBER["naegele"]] if ga_hpht is not None else []) + (
        [SUMBER["acog"]] if ga_usg is not None else [])
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
    def kelas(t):  # kurang / normal / lebih - untuk membandingkan dua sistem kategori
        return ("kurang" if t.startswith(("Berat badan kurang", "Kurus")) else
                "normal" if t.startswith("Normal") else "lebih")
    if kelas(kategori_ap(i)) != kelas(kategori_kemenkes(i)):
        hasil["catatan"].append(
            "Kategori Asia-Pasifik dan Kemenkes berbeda untuk IMT ini. Asia-Pasifik (WPRO 2000) "
            "lazim untuk risiko metabolik/klinis individu; ambang Kemenkes (Permenkes 41/2014) "
            "lazim untuk laporan gizi/posbindu sesuai format dinas. Pakai yang diminta "
            "fasilitas Anda dan sebutkan acuannya.")
    if lingkar_perut is not None:
        lp = desimal(lingkar_perut, "lingkar perut")
        if not Decimal(40) <= lp <= Decimal(250):
            raise InputSalah(f"lingkar perut {lingkar_perut}: di luar rentang wajar 40-250 cm")
        jk = (jk or "").strip().upper()[:1]
        hasil["lingkar_perut_cm"] = str(lp)
        if jk not in ("L", "P"):
            hasil["lingkar_perut"] = ("tidak dinilai - isi jenis kelamin L atau P (batas "
                                      "L >= 90 cm, P >= 80 cm)")
            return hasil
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
    hasil["catatan"].append("Keterbatasan: IOM 2009 menyatakan pedomannya tidak dimaksudkan untuk "
                            "populasi yang jauh lebih pendek/kurus dari perempuan Amerika; untuk "
                            "ibu Indonesia pakai sebagai acuan umum, bukan target mutlak.")
    if bb_sekarang is not None:
        sekarang = berat_kg(bb_sekarang, "BB sekarang")
        naik = sekarang - kg
        hasil["kenaikan_sejauh_ini_kg"] = str(bulat(naik))
        if usia_minggu is not None:
            u = desimal(usia_minggu, "usia kehamilan (minggu)")
            if not Decimal(0) <= u <= Decimal(44):
                raise InputSalah("usia kehamilan harus 0-44 minggu")
            hasil["usia_kehamilan_minggu"] = str(u)
            n = bulat(naik)  # posisi dibandingkan dengan angka yang DITAMPILKAN (1 desimal)
            if not kembar and u > 13:
                lo = bulat(Decimal("0.5") + desimal(laju[0], "laju") * (u - 13))
                hi = bulat(Decimal("2") + desimal(laju[1], "laju") * (u - 13))
                hasil["perkiraan_rentang_saat_ini_kg"] = f"{lo}-{hi}"
                posisi = "di bawah" if n < lo else "di atas" if n > hi else "di dalam"
                hasil["posisi"] = f"Kenaikan {n} kg {posisi} perkiraan rentang {lo}-{hi} kg"
                hasil["catatan"].append(
                    "Perkiraan rentang saat ini = turunan: trimester 1 0,5-2 kg + laju IOM x "
                    "(minggu - 13). Bukan tabel resmi; pakai sebagai gambaran kasar.")
            elif not kembar:
                lo, hi = Decimal("0.5"), Decimal("2.0")
                hasil["perkiraan_trimester_1_kg"] = f"{lo}-{hi}"
                posisi = "di bawah" if n < lo else "di atas" if n > hi else "di dalam"
                hasil["posisi"] = (f"Kenaikan {n} kg {posisi} asumsi IOM trimester 1 "
                                   f"({lo}-{hi} kg)")
                hasil["catatan"].append(
                    "Usia <= 13 minggu: IOM tidak memberi laju mingguan; asumsi kenaikan total "
                    "trimester 1 = 0,5-2 kg. Mual/muntah bisa membuat BB turun - nilai klinis.")
            else:
                hasil["catatan"].append("Kehamilan kembar: IOM hanya memberi rekomendasi total "
                                        "(provisional), tanpa rentang per usia kehamilan.")
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
        hasil["catatan"].append("Alat ini HANYA menafsirkan skor total yang dimasukkan nakes; "
                                "tidak memuat/mereproduksi formulir atau butir MMSE. Formulir MMSE "
                                "berhak cipta (PAR Inc.) - pemakaian formulir memerlukan "
                                "lisensi/izin milik pengguna sendiri dari pemegang hak cipta.")
        hasil["catatan"].append("Tidak ada koreksi pendidikan di alat ini: pada pendidikan rendah/"
                                "buta huruf, skor bisa rendah tanpa gangguan - nilai klinis.")
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
        hasil["catatan"].append("Alat ini HANYA menafsirkan skor total yang dimasukkan nakes; "
                                "tidak memuat/mereproduksi formulir, butir, atau instruksi MoCA. "
                                "Pemakaian formulir MoCA memerlukan lisensi/izin dan pelatihan-"
                                "sertifikasi milik pengguna sendiri dari pemegang hak cipta "
                                "(MoCA Cognition; sertifikasi wajib sejak 2019).")
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
        hasil["catatan"].append("Skor dipengaruhi pendidikan, bahasa, dan gangguan sensorik.")
    else:
        raise InputSalah("instrumen harus mmse, moca, atau amt")
    hasil["catatan"].append("Singkirkan dulu delirium (onset mendadak, fluktuatif - perlu "
                            "evaluasi segera), depresi, gangguan penglihatan/pendengaran, dan "
                            "efek obat sebelum menafsirkan skor rendah.")
    hasil["catatan"].append("Hasil skrining bukan diagnosis demensia/gangguan kognitif.")
    return hasil


# ---------------------------------------------------------------- IMT batch (CSV)

def imt_batch(teks_csv):
    """CSV berkolom: id,tinggi,berat[,lingkar_perut,jk]. Baris salah dilaporkan, tidak menghentikan."""
    import csv
    import io
    teks_csv = teks_csv.lstrip("\ufeff")
    kepala = next((x for x in teks_csv.splitlines() if x.strip()), "")
    # Ekspor Excel lokal Indonesia sering memakai titik koma (;) dan koma desimal.
    pemisah = ";" if kepala.count(";") > kepala.count(",") else ","
    baca = csv.DictReader(io.StringIO(teks_csv), delimiter=pemisah, restkey="__lebih__")
    kolom = [(c or "").strip().lower() for c in (baca.fieldnames or [])]
    if not {"tinggi", "berat"} <= set(kolom):
        raise InputSalah("CSV wajib berkolom minimal: id,tinggi,berat (opsional lingkar_perut,jk). "
                         "Pemisah kolom harus koma (,) atau titik koma (;); baris pertama = "
                         "nama kolom")
    catatan = ["IMT dibulatkan 1 desimal (setengah ke atas) lalu dikategorikan. Hanya "
               "dewasa >= 18 tahun, tidak untuk ibu hamil/anak. LP: L >= 90, P >= 80 cm."]
    if pemisah == ";":
        catatan.append("Pemisah titik koma (;) terdeteksi; koma desimal (1,65) dibaca benar.")
    baris, n_ok, n_salah = [], 0, 0
    for no, r in enumerate(baca, start=2):
        lebih = r.pop("__lebih__", None)
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        label = r.get("id") or f"baris {no}"
        if lebih is not None:
            baris.append(f"{label} | GAGAL - TIDAK DIHITUNG: kolom berlebih "
                         f"({len(kolom) + len(lebih)} nilai untuk {len(kolom)} kolom). Petunjuk: "
                         "kemungkinan koma desimal tanpa tanda kutip (mis. 1,65) - pakai titik "
                         "desimal (1.65), beri tanda kutip (\"1,65\"), atau simpan dengan pemisah "
                         "titik koma (;)")
            n_salah += 1
            continue
        try:
            h = imt_dewasa(r.get("tinggi"), r.get("berat"), r.get("lingkar_perut") or None,
                           r.get("jk") or None)
            lp = f" | LP {h['lingkar_perut_cm']}: {h['lingkar_perut']}" if "lingkar_perut" in h else ""
            baris.append(f"{label} | IMT {h['imt']} | AP: {h['kategori_asia_pasifik']} | "
                         f"Kemenkes: {h['kategori_kemenkes']}{lp}")
            n_ok += 1
        except InputSalah as e:
            baris.append(f"{label} | TIDAK DIHITUNG: {e}")
            n_salah += 1
    if not baris:
        raise InputSalah("CSV tidak berisi baris data")
    return {"perintah": "imt-batch", "hasil_per_pasien": baris,
            "ringkasan": f"{n_ok} dihitung, {n_salah} tidak dihitung (cek data)",
            "catatan": catatan,
            "sumber": [SUMBER["ap"], SUMBER["kemenkes_imt"]], "penafian": PENAFIAN}


# ---------------------------------------------------------------- tampilan

LABEL = {
    "tanda_bahaya": "!! TANDA BAHAYA", "peringatan": "!! PERHATIAN",
    "kode_tidak_dikenal": "Kode tidak dikenal (belum dinilai)", "map_mmhg": "MAP (mmHg)", "map_90_atau_lebih": "MAP >= 90",
    "kategori": "KATEGORI", "kategori_faktor_risiko": "Kategori faktor risiko (pelengkap)",
    "perkiraan_trimester_1_kg": "Asumsi IOM trimester 1 (kg)",
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
                    print(f"  {f['kode']:<29} KIA: {f['buku_kia']:<16} NICE: "
                          f"{f['nice_ng133']:<16} {f['label']}")
                continue
            if k in ("gejala_bahaya", "hasil_per_pasien"):
                print(LABEL.get(k, k.replace('_', ' ').capitalize()) + ":")
                for x in v:
                    print(f"  {x}")
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
    a.add_argument("--sistolik")
    a.add_argument("--diastolik")
    a.add_argument("--gejala", default="")
    sub.add_parser("faktor-preeklampsia")
    a = sub.add_parser("preeklampsia")
    a.add_argument("--faktor", default="")
    a.add_argument("--sistolik")
    a.add_argument("--diastolik")
    a.add_argument("--usia-ibu")
    a.add_argument("--imt")
    a.add_argument("--pedoman", default="kia", choices=["kia", "nice"])
    a.add_argument("--gejala", default="", help="kode gejala bahaya, dipisah koma")
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
    a = sub.add_parser("imt-batch")
    a.add_argument("--file", required=True, help="CSV: id,tinggi,berat[,lingkar_perut,jk]; '-' = stdin")
    a = sub.add_parser("kognitif")
    a.add_argument("--instrumen", required=True)
    a.add_argument("--skor", required=True)
    a.add_argument("--pendidikan-tahun")
    ar = p.parse_args(argv)
    try:
        if ar.perintah == "map":
            h = hitung_map(ar.sistolik, ar.diastolik, ar.gejala.split(","), boleh_parsial=True)
        elif ar.perintah == "faktor-preeklampsia":
            h = daftar_faktor()
        elif ar.perintah == "preeklampsia":
            h = skrining_preeklampsia(ar.faktor.split(","), ar.sistolik, ar.diastolik,
                                      ar.usia_ibu, ar.imt, ar.pedoman, ar.gejala.split(","))
        elif ar.perintah == "kehamilan":
            h = kalkulator_kehamilan(ar.hpht, ar.siklus, ar.tanggal_periksa, ar.usg_tanggal,
                                     ar.usg_minggu, ar.usg_hari)
        elif ar.perintah == "bb-hamil":
            h = bb_hamil(ar.tinggi, ar.bb_prahamil, ar.bb_sekarang, ar.usia_minggu, ar.kembar)
        elif ar.perintah == "imt":
            h = imt_dewasa(ar.tinggi, ar.berat, ar.lingkar_perut, ar.jk)
        elif ar.perintah == "imt-batch":
            try:
                if ar.file == "-":
                    teks = sys.stdin.read()
                else:
                    with open(ar.file, encoding="utf-8-sig") as f:
                        teks = f.read()
            except OSError as e:
                raise InputSalah(f"berkas CSV tidak bisa dibaca: {e.strerror}")
            h = imt_batch(teks)
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
    if h.get("kode_tidak_dikenal"):
        # Hasil (termasuk tanda bahaya) SUDAH dicetak; baru laporkan kode & keluar 1.
        print("Input tidak valid: kode tidak dikenal: " + "; ".join(h["kode_tidak_dikenal"]),
              file=sys.stderr)
        print("Kode gejala valid: " + ", ".join(GEJALA_BAHAYA), file=sys.stderr)
        print("Kode faktor valid: " + ", ".join(FAKTOR), file=sys.stderr)
        print("Perbaiki kode lalu jalankan ulang (daftar lengkap: python3 scripts/klinis.py "
              "faktor-preeklampsia).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
