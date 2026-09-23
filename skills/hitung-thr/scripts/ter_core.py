#!/usr/bin/env python3
"""Inti perhitungan PPh Pasal 21 metode Tarif Efektif Rata-rata (TER).

Dasar: PP 58/2023 (tabel TER), PMK 168/2023 (tata cara), UU 7/2021 HPP (PTKP & tarif Pasal 17),
PMK 105/2025 (PPh 21 DTP tahun 2026). Status aturan per 2026-09-23.

File ini SENGAJA identik di skill pph21-ter, slip-gaji-bpjs, dan hitung-thr agar tiap skill mandiri.
Tabel TER dibaca dari ter_tabel.json di folder yang sama (salinan persis Lampiran PP 58/2023).

Konvensi pembulatan (dijelaskan juga ke pengguna):
- PPh 21 bulanan (TER x bruto) dan PPh proporsional dibulatkan KE BAWAH ke rupiah penuh
  (tidak pernah memotong melebihi tarif). Belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax.
- Penghasilan Kena Pajak (PKP) dibulatkan ke bawah hingga ribuan rupiah penuh (PMK 168/2023 Pasal 8 ayat 4).
- Biaya jabatan dan penghasilan neto dihitung persis (tanpa pembulatan) sebelum PKP dibulatkan.

Hanya library standar Python 3.8+. Tidak ada akses jaringan.
"""
import json
import os
import re
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

TANGGAL_ATURAN = "2026-09-23"
DASAR_ATURAN = ("PP 58/2023 (tarif TER), PMK 168/2023 (tata cara PPh 21), UU 7/2021 HPP "
                "(PTKP & tarif Pasal 17), PMK 105/2025 (PPh 21 DTP 2026)")

NAMA_BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
              "September", "Oktober", "November", "Desember"]

_FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_TABEL = os.path.join(_FOLDER, "ter_tabel.json")

# PTKP setahun (UU 7/2021 Pasal 7 ayat (1); PMK 168/2023 Pasal 9)
PTKP_DIRI = Decimal(54000000)
PTKP_KAWIN = Decimal(4500000)
PTKP_TANGGUNGAN = Decimal(4500000)
MAKS_TANGGUNGAN = 3

# Tarif Pasal 17 ayat (1) huruf a UU PPh (UU 7/2021 HPP): (batas atas lapisan, tarif %)
LAPISAN_PASAL17 = [
    (Decimal(60000000), Decimal(5)),
    (Decimal(250000000), Decimal(15)),
    (Decimal(500000000), Decimal(25)),
    (Decimal(5000000000), Decimal(30)),
    (None, Decimal(35)),
]

# Biaya jabatan (PMK 168/2023 Pasal 10 ayat (2))
BIAYA_JABATAN_PERSEN = Decimal(5)
BIAYA_JABATAN_MAKS_BULAN = Decimal(500000)

# TER harian: batas penggunaan (PMK 168/2023 Pasal 12 ayat (2))
BATAS_TER_HARIAN = Decimal(2500000)

# PMK 105/2025: batas bruto tetap & teratur untuk PPh 21 DTP 2026
BATAS_DTP_BULANAN = Decimal(10000000)
BATAS_DTP_HARIAN = Decimal(500000)

CATATAN_PEMBULATAN = ("PPh 21 dibulatkan ke bawah ke rupiah penuh; PKP dibulatkan ke bawah hingga ribuan "
                      "rupiah (PMK 168/2023 Pasal 8 ayat 4). Pembulatan belum dicocokkan dengan Coretax; "
                      "bila Coretax menampilkan angka berbeda, ikuti Coretax.")

DISCLAIMER = ("Alat bantu hitung, bukan nasihat pajak. Dasar: " + DASAR_ATURAN + ", berlaku per 23 September "
              "2026. Untuk kasus khusus (ekspatriat, pesangon, pensiun, natura, gross-up) hubungi Kring Pajak "
              "1500200 atau konsultan pajak.")


# ---------------------------------------------------------------- angka & format
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3), ("m", 10 ** 9)]


def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise ValueError("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                         "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))


def parse_angka(nilai, nama="angka", boleh_negatif=False):
    """Baca angka format Indonesia: 'Rp 15.000', '15.000,50', '1,5 jt', '10jt', '15000'.

    Titik = pemisah ribuan, koma = desimal. Satu titik diikuti bukan 3 digit (mis. '2.5') dianggap desimal.
    Akhiran: rb/ribu/k (x1.000), jt/juta (x1.000.000), M/miliar (x1.000.000.000).
    """
    if isinstance(nilai, bool) or nilai is None:
        raise ValueError("{}: nilai kosong atau tidak valid".format(nama))
    if isinstance(nilai, Decimal):
        d = nilai
    elif isinstance(nilai, int):
        d = Decimal(nilai)
    elif isinstance(nilai, float):
        d = Decimal(str(nilai))
    else:
        asli = str(nilai)
        s = asli.strip().lower().replace(" ", "").replace(" ", "")
        s = re.sub(r"^(rp|idr)\.?", "", s)
        s = re.sub(r"[,.]-+$", "", s)          # '15.000,-'
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
                s = (bagian[0] or "0") + "." + bagian[1]       # koma tunggal = desimal
            else:
                _cek_ribuan(bagian, asli, nama)                # 1,250,000 (gaya ekspor)
                s = s.replace(",", "")
        elif "." in s:
            bagian = s.split(".")
            if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
                s = (bagian[0] or "0") + "." + bagian[1]       # '2.5', '0.500' = desimal
            else:
                _cek_ribuan(bagian, asli, nama)
                s = s.replace(".", "")
        try:
            d = Decimal(s) * pengali
        except InvalidOperation:
            raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
        if negatif:
            d = -d
    if not d.is_finite():
        raise ValueError("{}: nilai tidak valid".format(nama))
    if d < 0 and not boleh_negatif:
        raise ValueError("{}: tidak boleh negatif ({})".format(nama, nilai))
    return d


def bulat_bawah(d):
    """Bulatkan ke bawah ke rupiah penuh (untuk pajak)."""
    return Decimal(d).quantize(Decimal(1), ROUND_FLOOR)


def bulat_terdekat(d):
    """Bulatkan ke rupiah terdekat (untuk nominal non-pajak, mis. iuran, lembur)."""
    return Decimal(d).quantize(Decimal(1), ROUND_HALF_UP)


def bulat_ribuan_bawah(d):
    """PKP dibulatkan ke bawah hingga ribuan rupiah penuh."""
    d = Decimal(d)
    if d <= 0:
        return Decimal(0)
    return (d / 1000).quantize(Decimal(1), ROUND_FLOOR) * 1000


def format_rp(d, desimal=False):
    """Decimal -> 'Rp 1.250.000' (negatif: '-Rp 1.250.000')."""
    d = Decimal(d).quantize(Decimal("0.01") if desimal else Decimal(1), ROUND_HALF_UP)
    neg = d < 0
    d = abs(d)
    teks = "{:,}".format(int(d)).replace(",", ".")
    if desimal:
        pecahan = "{:.2f}".format(d).split(".")[1]
        if pecahan != "00":
            teks += "," + pecahan
    return ("-" if neg else "") + "Rp " + teks


def format_persen(d):
    d = Decimal(d).normalize()
    teks = "{:f}".format(d)
    if "." in teks:
        teks = teks.rstrip("0").rstrip(".")
    return teks.replace(".", ",") + "%"


def angka_json(d):
    """Decimal -> int bila bulat, selain itu string desimal (agar JSON presisi)."""
    d = Decimal(d)
    if d == d.to_integral_value():
        return int(d)
    return "{:f}".format(d.normalize())


# ---------------------------------------------------------------- tabel TER
_TABEL_CACHE = {}


def muat_tabel(path=None):
    """Baca ter_tabel.json dan ubah tarif ke Decimal. Validasi struktur dasar."""
    path = path or FILE_TABEL
    if path in _TABEL_CACHE:
        return _TABEL_CACHE[path]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except OSError:
        raise RuntimeError("File tabel TER tidak ditemukan: {}. Pastikan ter_tabel.json ada di folder "
                           "scripts/ skill ini.".format(path))
    tabel = {}
    for kunci in ("A", "B", "C", "harian"):
        baris = []
        sebelumnya = Decimal(0)
        for i, (bawah, atas, tarif) in enumerate(data[kunci]):
            bawah = Decimal(bawah)
            if bawah != sebelumnya:
                raise RuntimeError("Tabel TER {} rusak di baris {} (ada celah/tumpang tindih)".format(kunci, i + 1))
            atas_d = None if atas is None else Decimal(atas)
            baris.append((bawah, atas_d, Decimal(str(tarif))))
            sebelumnya = atas_d
        tabel[kunci] = baris
    tabel["kategori_ptkp"] = data["kategori_ptkp"]
    _TABEL_CACHE[path] = tabel
    return tabel


# ---------------------------------------------------------------- PTKP & kategori
def normalisasi_ptkp(teks):
    """'k0', 'K/0', 'tk 3', 'K-2', 'TK/1' -> 'K/0', 'TK/3', ... ; error bila tidak valid."""
    if teks is None:
        raise ValueError("Status PTKP wajib diisi (mis. TK/0, K/1, K/3)")
    s = str(teks).strip().upper().replace(" ", "").replace("-", "/").replace("_", "/")
    m = re.fullmatch(r"(TK|K)/?(\d+)", s)
    if not m:
        raise ValueError("Status PTKP '{}' tidak dikenali. Contoh yang benar: TK/0, TK/1, K/0, K/1, K/2, "
                         "K/3".format(teks))
    status, jml = m.group(1), int(m.group(2))
    if jml > MAKS_TANGGUNGAN:
        raise ValueError("Status PTKP '{}' tidak valid: tanggungan paling banyak 3 orang (pakai {}/3)"
                         .format(teks, status))
    return "{}/{}".format(status, jml)


def kategori_ter(ptkp):
    """Kategori TER bulanan dari status PTKP (PP 58/2023 Pasal 2 ayat 4)."""
    p = normalisasi_ptkp(ptkp)
    for kat, daftar in muat_tabel()["kategori_ptkp"].items():
        if p in daftar:
            return kat
    raise ValueError("Status PTKP '{}' tidak ada di pembagian kategori TER".format(ptkp))


def ptkp_setahun(ptkp):
    p = normalisasi_ptkp(ptkp)
    status, jml = p.split("/")
    total = PTKP_DIRI + PTKP_TANGGUNGAN * int(jml)
    if status == "K":
        total += PTKP_KAWIN
    return total


# ---------------------------------------------------------------- tarif
def _cari_tarif(nilai, baris):
    nilai = Decimal(nilai)
    if nilai < 0:
        raise ValueError("Penghasilan bruto tidak boleh negatif")
    for i, (bawah, atas, tarif) in enumerate(baris):
        # baris pertama: 'sampai dengan atas' (termasuk 0); lainnya: 'di atas bawah s.d. atas'
        if (i == 0 or nilai > bawah) and (atas is None or nilai <= atas):
            return tarif, bawah, atas
    return None


def tarif_ter_bulanan(bruto, kategori):
    """Kembalikan (tarif %, batas_bawah, batas_atas) TER bulanan kategori A/B/C."""
    kategori = str(kategori).upper()
    if kategori not in ("A", "B", "C"):
        raise ValueError("Kategori TER harus A, B, atau C")
    return _cari_tarif(bruto, muat_tabel()[kategori])


def pph_ter_bulanan(bruto, kategori):
    """PPh 21 masa selain Masa Pajak Terakhir = TER bulanan x bruto sebulan (dibulatkan ke bawah)."""
    tarif, _, _ = tarif_ter_bulanan(bruto, kategori)
    return bulat_bawah(Decimal(bruto) * tarif / 100), tarif


def pasal17(pkp):
    """PPh terutang = tarif progresif Pasal 17 ayat (1) huruf a x PKP. Kembalikan (pajak, rincian)."""
    pkp = Decimal(pkp)
    sisa, bawah, pajak, rincian = pkp, Decimal(0), Decimal(0), []
    if pkp <= 0:
        return Decimal(0), []
    for atas, tarif in LAPISAN_PASAL17:
        lebar = sisa if atas is None else min(sisa, atas - bawah)
        if lebar <= 0:
            break
        bagian = lebar * tarif / 100
        rincian.append({"tarif": tarif, "dasar": lebar, "pajak": bagian})
        pajak += bagian
        sisa -= lebar
        if atas is not None:
            bawah = atas
    return pajak, rincian


def pph_harian(bruto_sehari):
    """PPh 21 Pegawai Tidak Tetap yang tidak dibayar bulanan, per hari.

    <= Rp2.500.000 sehari: TER harian x bruto sehari.
    >  Rp2.500.000 sehari: tarif Pasal 17 x 50% bruto sehari (PMK 168/2023 Pasal 12 ayat 2 huruf b).
    Kembalikan dict {metode, tarif, pph}.
    """
    b = Decimal(bruto_sehari)
    if b < 0:
        raise ValueError("Upah sehari tidak boleh negatif")
    if b <= BATAS_TER_HARIAN:
        tarif, _, _ = _cari_tarif(b, muat_tabel()["harian"])
        return {"metode": "TER harian", "tarif": tarif, "dasar": b, "pph": bulat_bawah(b * tarif / 100)}
    dasar = b * Decimal("0.5")
    pajak, rincian = pasal17(dasar)
    return {"metode": "Pasal 17 x 50% bruto", "tarif": None, "dasar": dasar, "pph": bulat_bawah(pajak),
            "rincian_pasal17": rincian}


# ---------------------------------------------------------------- setahun / Masa Pajak Terakhir
def hitung_masa_terakhir(total_bruto, total_iuran, total_zakat, jumlah_bulan, ptkp,
                         pph_sudah_dipotong, disetahunkan=False):
    """Hitung PPh 21 Masa Pajak Terakhir (Desember atau bulan berhenti bekerja).

    - Biaya jabatan = 5% x bruto, maks Rp500.000 x jumlah bulan bekerja (maks Rp6.000.000 setahun).
    - Neto = bruto - biaya jabatan - iuran pensiun/JHT/JP pegawai - zakat lewat pemberi kerja.
    - disetahunkan=True HANYA bila kewajiban pajak subjektif mulai/berakhir di tengah tahun
      (mis. ekspatriat datang/pergi, meninggal): neto x 12/n, pajak x n/12 (PMK 168 Pasal 15 ayat 3).
      Pegawai yang sekadar pindah kerja/berhenti: TIDAK disetahunkan, PTKP tetap penuh.
    """
    n = int(jumlah_bulan)
    if not 1 <= n <= 12:
        raise ValueError("Jumlah bulan bekerja harus 1–12")
    total_bruto = Decimal(total_bruto)
    biaya_jabatan = min(total_bruto * BIAYA_JABATAN_PERSEN / 100, BIAYA_JABATAN_MAKS_BULAN * n)
    pengurang = biaya_jabatan + Decimal(total_iuran) + Decimal(total_zakat)
    neto = total_bruto - pengurang
    neto_dasar = neto * 12 / n if disetahunkan else neto
    ptkp_nilai = ptkp_setahun(ptkp)
    pkp = bulat_ribuan_bawah(neto_dasar - ptkp_nilai)
    pajak_setahun, rincian = pasal17(pkp)
    pajak_terutang = bulat_bawah(pajak_setahun * n / 12) if disetahunkan else bulat_bawah(pajak_setahun)
    pph_akhir = pajak_terutang - Decimal(pph_sudah_dipotong)
    return {
        "total_bruto": total_bruto,
        "biaya_jabatan": biaya_jabatan,
        "biaya_jabatan_maks": BIAYA_JABATAN_MAKS_BULAN * n,
        "iuran_pensiun": Decimal(total_iuran),
        "zakat": Decimal(total_zakat),
        "neto": neto,
        "disetahunkan": disetahunkan,
        "neto_disetahunkan": neto_dasar if disetahunkan else None,
        "ptkp": ptkp_nilai,
        "pkp": pkp,
        "rincian_pasal17": rincian,
        "pph_setahun_penuh": pajak_setahun,
        "pph_terutang": pajak_terutang,
        "pph_sudah_dipotong": Decimal(pph_sudah_dipotong),
        "pph_masa_terakhir": pph_akhir,
    }


def cek_dtp_bulanan(bruto_tetap_teratur):
    """PMK 105/2025: bruto tetap & teratur <= Rp10 jt (Januari 2026 / bulan pertama kerja)."""
    return Decimal(bruto_tetap_teratur) <= BATAS_DTP_BULANAN
