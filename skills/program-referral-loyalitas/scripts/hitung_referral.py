#!/usr/bin/env python3
"""Kalkulator program referral & loyalitas untuk UMKM (Python standar saja, tanpa internet).

Jalankan: python3 scripts/hitung_referral.py <perintah> [opsi]   (Windows: py atau python)

Perintah:
  biaya     biaya per referral berhasil, laba pesanan pertama setelah hadiah, total program
  impas     titik impas hadiah: butuh berapa pesanan agar balik modal, batas hadiah aman
  poin      nilai poin loyalitas: persen hadiah dari belanja, porsi dari margin, liability poin
  simulasi  simulasi skenario referral (ESTIMASI): perujuk -> teman -> pembeli -> laba/ROI

Aturan (standar library Komunitech): uang memakai Decimal; nominal rupiah dibulatkan ke rupiah
terdekat (setengah ke atas); batas hadiah maksimal dibulatkan KE BAWAH (tidak pernah melebihi
batas); jumlah pesanan/orang yang dibutuhkan dibulatkan KE ATAS; poin per transaksi
dibulatkan KE BAWAH (hanya kelipatan penuh). Persen ditulis angka biasa (15 = 15%).
Hadiah boleh ditulis rupiah (15rb, 15.000) atau persen dari nilai pesanan (10%).
"""
import argparse
import re
import sys
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal as D, InvalidOperation

NOL = D(0)
SATU = D(1)
SERATUS = D(100)
PORSI_AMAN_BAWAAN = D(30)      # aturan praktis: total hadiah <= 30% dari laba kotor seumur pelanggan
BATAS_PERHATIAN_POIN = D("0.5")  # aturan praktis: hadiah poin <= 50% dari margin kotor
PORSI_SARAN_PESANAN_PERTAMA = D("0.5")  # saran konservatif: total hadiah <= 50% laba kotor pesanan pertama


class InputError(ValueError):
    """Input pengguna tidak bisa dipakai. Pesan ditulis untuk orang awam."""


# ---------------------------------------------------------------- pembulatan & format

def bulat(x):
    return D(x).quantize(SATU, rounding=ROUND_HALF_UP)


def ke_atas(x):
    return D(x).quantize(SATU, rounding=ROUND_CEILING)


def ke_bawah(x):
    return D(x).quantize(SATU, rounding=ROUND_FLOOR)


def rp(x):
    x = D(x)
    tanda = "-" if x < 0 else ""
    x = abs(x)
    if x == x.to_integral_value():
        utuh, des = str(int(x)), ""
    else:
        q = x.quantize(D("0.01"), rounding=ROUND_HALF_UP)
        utuh, des = str(q).split(".")
        des = "," + des
    kel = []
    while len(utuh) > 3:
        kel.insert(0, utuh[-3:])
        utuh = utuh[:-3]
    kel.insert(0, utuh)
    return f"{tanda}Rp{'.'.join(kel)}{des}"


def pct(x, desimal=2):
    q = (D(x) * SERATUS).quantize(D(1).scaleb(-desimal), rounding=ROUND_HALF_UP)
    s = f"{q}".replace(".", ",")
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s + "%"


def angka(x):
    x = D(x)
    if x == x.to_integral_value():
        return f"{int(x):,}".replace(",", ".")
    return str(x.normalize()).replace(".", ",")


# ---------------------------------------------------------------- parsing input awam

_RIBUAN = re.compile(r"^\d{1,3}(\.\d{3})+(,\d+)?$")      # 40.000 | 1.500.000 | 38.000,50
_RIBUAN_KOMA = re.compile(r"^\d{1,3}(,\d{3})+$")          # 52,300 (gaya Inggris)
_AKHIRAN = re.compile(r"^(.*?)(rb|ribu|k|jt|juta)$")


def _bersihkan(nilai, nama):
    if nilai is None:
        raise InputError(f"{nama} kosong")
    s = str(nilai).strip().lower().replace(" ", "")
    if not s:
        raise InputError(f"{nama} kosong")
    if s.startswith("-"):
        raise InputError(f"{nama} tidak boleh negatif (didapat {nilai})")
    return s


def _pisah_akhiran(s):
    m = _AKHIRAN.match(s)
    if not m:
        return s, None
    return m.group(1), (D(1000) if m.group(2) in ("rb", "ribu", "k") else D(1000000))


def _angka_berakhiran(s, nilai, nama):
    """Bagian angka sebelum rb/jt: '1,5' / '1.5' = desimal, '1.500' = ribuan."""
    if _RIBUAN.match(s) and "," not in s:
        s = s.replace(".", "")
    elif re.match(r"^\d+[.,]\d+$", s):
        s = s.replace(",", ".")
    if not re.match(r"^\d+(\.\d+)?$", s):
        raise InputError(f"{nama} '{nilai}' tidak terbaca (contoh benar: 40rb, 1,5jt)")
    return D(s)


def parse_rupiah(nilai, boleh_nol=False, nama="angka"):
    """'Rp52.300', '52300', '1.500.000', '52,3rb', '1,2jt' -> Decimal. Angka ambigu seperti '12.5' DITOLAK."""
    if isinstance(nilai, (int, D)):
        x = D(nilai)
    else:
        s = _bersihkan(nilai, nama)
        s = re.sub(r"^(rp\.?|idr)", "", s)
        s = re.sub(r"(,-|\.-)$", "", s)
        s, kali = _pisah_akhiran(s)
        if kali is not None:
            x = _angka_berakhiran(s, nilai, nama) * kali
        else:
            if _RIBUAN.match(s):
                s = s.replace(".", "").replace(",", ".")
            elif _RIBUAN_KOMA.match(s):
                s = s.replace(",", "")
            elif re.match(r"^\d+,\d{1,2}$", s):
                if 1 <= int(s.split(",")[0]) < 1000:
                    raise InputError(f"{nama} '{nilai}' ambigu: Rp{s} kurang dari seribu rupiah. "
                                     f"Maksud Anda {s}rb atau {s}jt? Tulis mis. {s}rb")
                s = s.replace(",", ".")
            elif re.match(r"^\d+\.\d+$", s):
                raise InputError(f"{nama} '{nilai}' ambigu: titik dipakai sebagai pemisah ribuan. "
                                 f"Tulis mis. 12.500 (dua belas ribu lima ratus) atau 12,5rb")
            if not re.match(r"^\d+(\.\d+)?$", s):
                raise InputError(f"{nama} '{nilai}' tidak terbaca sebagai rupiah (contoh benar: 52.300, 52rb, 1,2jt)")
            try:
                x = D(s)
            except InvalidOperation:
                raise InputError(f"{nama} '{nilai}' tidak terbaca sebagai rupiah")
    if x < 0 or (x == 0 and not boleh_nol):
        raise InputError(f"{nama} harus lebih dari 0 (didapat {nilai})" if not boleh_nol
                         else f"{nama} tidak boleh negatif (didapat {nilai})")
    return x


def parse_jumlah(nilai, nama="angka", boleh_nol=False, bulat_saja=False):
    """Jumlah (orang, poin, kali, bulan) - BUKAN rupiah.

    bulat_saja=True  (poin, pelanggan, referral): '40.000' / '1.500.000' = ribuan; '40rb', '1,5jt' boleh.
    bulat_saja=False (frekuensi, bulan, pesanan ulang): desimal pakai koma ('0,25', '1,5');
                     '1.000' atau '1,000' AMBIGU (seribu atau satu?) -> GAGAL, tidak ditebak.
    """
    s = _bersihkan(nilai, nama)
    if re.match(r"^(rp|idr)", s):
        raise InputError(f"{nama} adalah jumlah, bukan rupiah; tulis tanpa 'Rp' (mis. 40.000 atau 40000)")
    s, kali = _pisah_akhiran(s)
    if kali is not None:
        x = _angka_berakhiran(s, nilai, nama) * kali
    elif re.match(r"^\d+$", s):
        x = D(s)
    elif _RIBUAN.match(s):
        if bulat_saja or "," in s:
            x = D(s.replace(".", "").replace(",", "."))
        else:
            raise InputError(f"{nama} '{nilai}' ambigu: bisa dibaca {s.replace('.', '')} atau {s.replace('.', ',')}. "
                             f"Untuk desimal pakai koma (mis. 1,5); untuk ribuan tulis tanpa titik (mis. 1000)")
    elif _RIBUAN_KOMA.match(s) and not s.startswith("0,"):
        raise InputError(f"{nama} '{nilai}' ambigu: koma bisa berarti desimal atau ribuan. "
                         f"Tulis ribuan dengan titik (mis. 1.000) atau desimal dengan satu/dua angka di belakang koma (mis. 1,5)")
    elif re.match(r"^\d+,\d+$", s):
        x = D(s.replace(",", "."))
    elif re.match(r"^\d+\.\d+$", s):
        raise InputError(f"{nama} '{nilai}' ambigu: titik di Indonesia adalah pemisah ribuan. "
                         f"Untuk desimal pakai koma (mis. 1,5)")
    else:
        raise InputError(f"{nama} '{nilai}' tidak terbaca (tulis angka biasa, mis. 2, 1,5, atau 40.000)")
    if bulat_saja and x != x.to_integral_value():
        raise InputError(f"{nama} harus bilangan bulat (didapat {nilai})")
    if x < 0 or (x == 0 and not boleh_nol):
        raise InputError(f"{nama} harus lebih dari 0 (didapat {nilai})")
    return x


def parse_persen(nilai, nama="persen", maks=D(100)):
    """'15', '15%', '12,5%', '12.5' -> pecahan Decimal 0.15. Angka SELALU dianggap persen.
    '1.000' / '12,500' (tiga angka di belakang pemisah) AMBIGU -> GAGAL."""
    s = _bersihkan(nilai, nama).replace("%", "")
    if re.match(r"^\d+[.,]\d{3}", s) and not re.match(r"^0[.,]", s):
        raise InputError(f"{nama} '{nilai}' ambigu: tulis persen dengan koma desimal, mis. 12,5 (bukan 1.000 atau 12,500)")
    s = s.replace(",", ".")
    if not re.match(r"^\d+(\.\d+)?$", s):
        raise InputError(f"{nama} '{nilai}' tidak terbaca (contoh benar: 15 atau 12,5%; tidak boleh negatif)")
    x = D(s)
    if x > maks:
        raise InputError(f"{nama} {str(nilai).strip().rstrip('%')}% di luar batas wajar (maks {maks}%)")
    return x / SERATUS


def parse_margin(nilai):
    m = parse_persen(nilai, "margin", D(99))
    if m <= 0:
        raise InputError("margin harus lebih dari 0% dan kurang dari 100% (margin = laba kotor / harga jual)")
    return m


def parse_hadiah(nilai, aov, nama="hadiah"):
    """'15rb' -> Rp15.000 ; '10%' -> 10% dari nilai pesanan (dibulatkan ke rupiah terdekat)."""
    if nilai is None:
        return NOL
    if str(nilai).strip().endswith("%"):
        return bulat(aov * parse_persen(nilai, nama))
    return bulat(parse_rupiah(nilai, boleh_nol=True, nama=nama))


def parse_skenario(teks):
    """'realistis:10:2:25' = nama : % pelanggan yang merujuk : teman per perujuk : % teman yang beli."""
    bagian = str(teks).split(":")
    if len(bagian) != 4 or not bagian[0].strip():
        raise InputError(f"skenario '{teks}' salah format; tulis nama:%merujuk:teman_per_perujuk:%beli, "
                         f"mis. realistis:10:2:25")
    return {"nama": bagian[0].strip(),
            "merujuk": parse_persen(bagian[1], "persen pelanggan yang merujuk"),
            "teman": parse_jumlah(bagian[2], "teman per perujuk", boleh_nol=True),
            "beli": parse_persen(bagian[3], "persen teman yang membeli")}


SKENARIO_BAWAAN = ["konservatif:5:1:20", "realistis:10:2:25", "optimis:15:2:30"]


# ---------------------------------------------------------------- inti hitungan

def biaya_referral(aov, margin, pemberi, teman, lain):
    """Biaya per referral BERHASIL (dibayar hanya bila teman benar-benar membeli)."""
    lpo = bulat(aov * margin)                     # laba kotor per pesanan
    total = pemberi + teman + lain
    setelah = lpo - total
    h = {"aov": aov, "margin": margin, "lpo": lpo, "pemberi": pemberi, "teman": teman, "lain": lain,
         "biaya": total, "laba_setelah": setelah, "persen_aov": total / aov,
         "persen_laba": total / lpo if lpo > 0 else None}
    h["pesanan_tambahan"] = ke_atas(-setelah / lpo) if setelah < 0 and lpo > 0 else NOL
    return h


def titik_impas(aov, margin, pemberi, teman, lain, frekuensi, umur, porsi):
    h = biaya_referral(aov, margin, pemberi, teman, lain)
    lpo, biaya = h["lpo"], h["biaya"]
    if lpo <= 0:
        raise InputError("laba kotor per pesanan Rp0 setelah pembulatan; perbesar nilai pesanan atau margin")
    h["frekuensi"], h["umur"], h["porsi"] = frekuensi, umur, porsi
    h["pesanan_impas"] = max(SATU, ke_atas(biaya / lpo)) if biaya > 0 else SATU
    h["bulan_impas"] = ke_atas((h["pesanan_impas"] - 1) / frekuensi)
    h["pesanan_seumur"] = frekuensi * umur
    h["ltv"] = bulat(lpo * h["pesanan_seumur"])
    h["batas_aman"] = ke_bawah(h["ltv"] * porsi)
    h["pemberi_maks"] = max(NOL, h["batas_aman"] - teman - lain)
    h["impas_pertama"] = lpo
    # saran konservatif: pesanan pertama tetap menyisakan >= separuh laba kotor, dan tidak melewati batas atas
    h["pemberi_saran"] = min(h["pemberi_maks"], max(NOL, ke_bawah(lpo * PORSI_SARAN_PESANAN_PERTAMA) - teman - lain))
    if biaya <= h["batas_aman"] and h["laba_setelah"] >= 0:
        h["status"] = "AMAN"
    elif biaya <= h["batas_aman"]:
        h["status"] = "RUGI DI PESANAN PERTAMA"
    elif biaya <= h["ltv"]:
        h["status"] = "PERHATIAN"
    else:
        h["status"] = "TIDAK DISARANKAN"
    return h


def nilai_poin(belanja_per_poin, nilai, margin, aov=None, omzet=None, breakage=NOL, beredar=None, min_tukar=None):
    rate = nilai / belanja_per_poin
    h = {"belanja_per_poin": belanja_per_poin, "nilai": nilai, "margin": margin, "rate": rate,
         "porsi_margin": rate / margin, "breakage": breakage}
    if rate >= margin:
        h["status"] = "RUGI"
    elif rate / margin > BATAS_PERHATIAN_POIN:
        h["status"] = "PERHATIAN"
    else:
        h["status"] = "OK"
    h["rate_efektif"] = rate * (1 - breakage)
    if aov is not None:
        poin = ke_bawah(aov / belanja_per_poin)
        val = poin * nilai
        h["aov"], h["poin_per_pesanan"], h["nilai_per_pesanan"] = aov, poin, val
        h["rate_nyata"] = val / aov
        h["laba_kotor"] = bulat(aov * margin)
        h["laba_setelah_tukar"] = h["laba_kotor"] - val
    if omzet is not None:
        h["omzet"] = omzet
        h["biaya_maks"] = bulat(omzet * rate)
        h["biaya_perkiraan"] = bulat(omzet * rate * (1 - breakage))
    if beredar is not None:
        h["beredar"] = beredar
        h["liab_maks"] = beredar * nilai
        h["liab_perkiraan"] = bulat(beredar * nilai * (1 - breakage))
    if min_tukar is not None:
        h["min_tukar"] = min_tukar
        h["belanja_min"] = min_tukar * belanja_per_poin
        h["hadiah_min"] = min_tukar * nilai
    return h


def simulasi(pelanggan, aov, margin, pemberi, teman, lain, skenario, ulang, anggaran, cac):
    per = biaya_referral(aov, margin, pemberi, teman, lain)
    hasil = []
    for s in skenario:
        perujuk = bulat(pelanggan * s["merujuk"])
        diajak = bulat(perujuk * s["teman"])
        pembeli = bulat(diajak * s["beli"])
        biaya = pembeli * per["biaya"]
        laba_kotor = pembeli * per["lpo"] * (1 + ulang)
        omzet = bulat(pembeli * aov * (1 + ulang))
        bersih = laba_kotor - biaya
        hasil.append({"nama": s["nama"], "perujuk": perujuk, "diajak": diajak, "pembeli": pembeli,
                      "biaya": biaya, "omzet": omzet, "laba_kotor": laba_kotor, "bersih": bersih,
                      "roi": bersih / biaya if biaya > 0 else None,
                      "lewat_anggaran": anggaran is not None and biaya > anggaran})
    return per, hasil


# ---------------------------------------------------------------- tampilan

def _peringatan_pesanan(h):
    out = []
    if h["laba_setelah"] < 0:
        out.append(f"PERHATIAN: hadiah lebih besar dari laba kotor pesanan pertama (rugi {rp(-h['laba_setelah'])} per referral). "
                   f"Balik modal hanya bila teman membeli lagi, minimal {angka(h['pesanan_tambahan'])} pesanan ulang.")
    return out


def cetak_biaya(h, jumlah, anggaran, cac):
    out = [f"BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)",
           f"Nilai pesanan pertama rata-rata : {rp(h['aov'])}  |  margin kotor {pct(h['margin'])}",
           f"Laba kotor pesanan pertama      : {rp(h['lpo'])} (sebelum hadiah)",
           f"Hadiah pemberi (perujuk)        : {rp(h['pemberi'])}",
           f"Hadiah/diskon teman             : {rp(h['teman'])}",
           f"Biaya lain per referral         : {rp(h['lain'])}",
           f"BIAYA PER REFERRAL              : {rp(h['biaya'])} = {pct(h['persen_aov'])} dari nilai pesanan"
           + (f", {pct(h['persen_laba'])} dari laba kotor" if h["persen_laba"] is not None else ""),
           f"Laba pesanan pertama setelah hadiah: {rp(h['laba_setelah'])}"]
    out += _peringatan_pesanan(h)
    if jumlah is not None:
        total = h["biaya"] * jumlah
        out.append(f"Program {angka(jumlah)} referral berhasil: total biaya {rp(total)}; total laba kotor pesanan pertama "
                   f"{rp(h['lpo'] * jumlah)}; laba setelah hadiah {rp(h['laba_setelah'] * jumlah)}")
        if anggaran is not None:
            sisa = anggaran - total
            out.append(f"Anggaran {rp(anggaran)}: " + (f"cukup (sisa {rp(sisa)})" if sisa >= 0
                                                       else f"TIDAK CUKUP (kurang {rp(-sisa)})"))
    elif anggaran is not None:
        n = ke_bawah(anggaran / h["biaya"]) if h["biaya"] > 0 else None
        if n is not None:
            out.append(f"Anggaran {rp(anggaran)} cukup untuk maksimal {angka(n)} referral berhasil.")
    if cac is not None:
        banding = "LEBIH MURAH" if h["biaya"] < cac else ("SAMA" if h["biaya"] == cac else "LEBIH MAHAL")
        out.append(f"Pembanding: biaya per pelanggan baru dari iklan {rp(cac)} -> referral {banding} "
                   f"(selisih {rp(abs(cac - h['biaya']))}).")
    out.append("Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.")
    return "\n".join(out)


def cetak_impas(h):
    out = [f"TITIK IMPAS HADIAH REFERRAL",
           f"Laba kotor per pesanan          : {rp(h['lpo'])} (nilai pesanan {rp(h['aov'])}, margin {pct(h['margin'])})",
           f"Biaya per referral              : {rp(h['biaya'])} (pemberi {rp(h['pemberi'])} + teman {rp(h['teman'])} + lain {rp(h['lain'])})",
           f"Balik modal setelah             : pesanan ke-{angka(h['pesanan_impas'])} milik teman"
           + (" (langsung di pesanan pertama)" if h["pesanan_impas"] == 1
              else f", sekitar bulan ke-{angka(h['bulan_impas'])} bila belanja {angka(h['frekuensi'])}x per bulan"),
           f"Hadiah maks agar impas di pesanan pertama: {rp(h['impas_pertama'])} (total pemberi + teman + lain)",
           f"Perkiraan laba kotor seumur pelanggan: {rp(h['ltv'])} ({angka(h['pesanan_seumur'])} pesanan; asumsi "
           f"{angka(h['frekuensi'])}x per bulan selama {angka(h['umur'])} bulan)",
           f"Batas hadiah aman ({pct(h['porsi'], 0)} dari laba seumur pelanggan): {rp(h['batas_aman'])} total per referral",
           f"BATAS ATAS hadiah pemberi (bukan anjuran; di atas ini melewati batas aman): {rp(h['pemberi_maks'])}",
           f"Hadiah pemberi SARAN (konservatif: total hadiah maks. 50% laba pesanan pertama): {rp(h['pemberi_saran'])}",
           f"STATUS: {h['status']}"]
    if h["pemberi_saran"] == 0:
        out.append("Catatan: hadiah teman + biaya lain sudah memakai 50% atau lebih laba pesanan pertama; tidak ada ruang hadiah pemberi versi konservatif.")
    if h["laba_setelah"] < 0:
        out.append(f"PERHATIAN: RUGI {rp(-h['laba_setelah'])} per referral di pesanan pertama. Balik modal hanya bila teman membeli lagi "
                   f"sampai pesanan ke-{angka(h['pesanan_impas'])}; bila teman hanya membeli sekali, program ini rugi.")
    if h["status"] == "PERHATIAN":
        out.append("PERHATIAN: biaya di atas batas aman tetapi masih di bawah laba seumur pelanggan; aman hanya bila pelanggan benar-benar rutin membeli.")
    if h["status"] == "TIDAK DISARANKAN":
        out.append("PERHATIAN: biaya per referral lebih besar dari seluruh laba kotor perkiraan seumur pelanggan; turunkan hadiah.")
    if h["pesanan_impas"] > h["pesanan_seumur"]:
        out.append("PERHATIAN: pesanan yang dibutuhkan untuk balik modal lebih banyak dari perkiraan pesanan seumur pelanggan.")
    out.append("Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.")
    return "\n".join(out)


def cetak_poin(h):
    out = [f"NILAI POIN LOYALITAS",
           f"Aturan: tiap belanja {rp(h['belanja_per_poin'])} = 1 poin; 1 poin ditukar senilai {rp(h['nilai'])}",
           f"Hadiah poin = {pct(h['rate'])} dari belanja = {pct(h['porsi_margin'])} dari margin kotor {pct(h['margin'])}",
           f"STATUS: {h['status']}"]
    if h["status"] == "RUGI":
        out.append("PERHATIAN: hadiah poin sama dengan atau melebihi margin kotor; setiap penukaran poin membuat usaha rugi.")
    elif h["status"] == "PERHATIAN":
        out.append("PERHATIAN: hadiah poin memakai lebih dari separuh margin kotor (aturan praktis); sisakan ruang untuk biaya operasional.")
    if h["breakage"] > 0:
        out.append(f"Bila {pct(h['breakage'])} poin tidak pernah ditukar (perkiraan): biaya efektif {pct(h['rate_efektif'])} dari belanja.")
    if "aov" in h:
        out.append(f"Pesanan {rp(h['aov'])}: dapat {angka(h['poin_per_pesanan'])} poin (dibulatkan ke bawah) = {rp(h['nilai_per_pesanan'])} "
                   f"({pct(h['rate_nyata'])} dari pesanan). Laba kotor pesanan {rp(h['laba_kotor'])}; setelah poin ditukar {rp(h['laba_setelah_tukar'])}.")
    if "omzet" in h:
        out.append(f"Omzet {rp(h['omzet'])}/bulan: biaya poin maksimal (semua ditukar) {rp(h['biaya_maks'])}"
                   + (f"; perkiraan {rp(h['biaya_perkiraan'])} (ESTIMASI)" if h["breakage"] > 0 else "") + ".")
    if "beredar" in h:
        out.append(f"LIABILITY (kewajiban) poin beredar {angka(h['beredar'])} poin: maksimal {rp(h['liab_maks'])} bila semua ditukar"
                   + (f"; perkiraan {rp(h['liab_perkiraan'])} (ESTIMASI)" if h["breakage"] > 0 else "") + ".")
        out.append("Sisihkan dana sebesar liability maksimal bila ingin aman; bila pembukuan formal, tanyakan akuntan cara mencatatnya.")
    if "min_tukar" in h:
        out.append(f"Minimum tukar {angka(h['min_tukar'])} poin = belanja kumulatif {rp(h['belanja_min'])}, hadiah {rp(h['hadiah_min'])}.")
    return "\n".join(out)


def cetak_simulasi(per, hasil, pelanggan, ulang, anggaran, cac):
    out = [f"SIMULASI REFERRAL (ESTIMASI, bukan kepastian) - {angka(pelanggan)} pelanggan aktif",
           f"Biaya per referral berhasil {rp(per['biaya'])}; laba kotor per pesanan {rp(per['lpo'])}; "
           f"pesanan ulang per teman baru: {angka(ulang)}"]
    for r in hasil:
        roi = "-" if r["roi"] is None else pct(r["roi"])
        out.append(f"- {r['nama']}: {angka(r['perujuk'])} perujuk -> {angka(r['diajak'])} teman diajak -> {angka(r['pembeli'])} pembeli baru | "
                   f"omzet {rp(r['omzet'])} | biaya hadiah {rp(r['biaya'])} | laba kotor {rp(r['laba_kotor'])} | "
                   f"laba setelah hadiah {rp(r['bersih'])} | ROI {roi}")
        if r["lewat_anggaran"]:
            out.append(f"  PERHATIAN: biaya {rp(r['biaya'])} melebihi anggaran {rp(anggaran)}; pasang batas kuota hadiah.")
    if per["laba_setelah"] < 0 and ulang == 0:
        out.append(f"PERHATIAN: tiap referral rugi {rp(-per['laba_setelah'])} bila teman hanya membeli sekali; simulasi memperlihatkan angka rugi tersebut.")
    if cac is not None:
        banding = "lebih murah" if per["biaya"] < cac else "tidak lebih murah"
        out.append(f"Pembanding iklan: {rp(cac)} per pelanggan baru -> referral {banding} ({rp(per['biaya'])} per pembeli baru).")
    out.append("Angka skenario adalah asumsi awal, bukan patokan pasar; ganti dengan data Anda setelah 1 bulan berjalan.")
    return "\n".join(out)


# ---------------------------------------------------------------- CLI

def buat_parser():
    p = argparse.ArgumentParser(prog="hitung_referral", allow_abbrev=False,
                                description="Kalkulator program referral & loyalitas UMKM")
    sub = p.add_subparsers(dest="perintah", required=True)

    def umum(sp, aov_wajib=True):
        sp.add_argument("--aov", required=aov_wajib, help="nilai pesanan pertama rata-rata (Rp)")
        sp.add_argument("--margin", required=True, help="margin kotor %% (laba kotor / harga jual)")
        sp.add_argument("--hadiah-pemberi", default="0", help="hadiah untuk perujuk: Rp (15rb) atau %% pesanan (10%%)")
        sp.add_argument("--hadiah-teman", default="0", help="hadiah/diskon untuk teman: Rp atau %% pesanan")
        sp.add_argument("--biaya-lain", default="0", help="biaya lain per referral berhasil (kartu, kemasan, ongkir), Rp")

    b = sub.add_parser("biaya", allow_abbrev=False)
    umum(b)
    b.add_argument("--jumlah-referral", help="jumlah referral berhasil yang direncanakan")
    b.add_argument("--anggaran", help="anggaran hadiah maksimal (Rp)")
    b.add_argument("--cac-iklan", help="biaya iklan per pelanggan baru sebagai pembanding (Rp)")

    i = sub.add_parser("impas", allow_abbrev=False)
    umum(i)
    i.add_argument("--frekuensi-bulan", default="1", help="pembelian per pelanggan per bulan (asumsi). Default 1")
    i.add_argument("--umur-bulan", default="6", help="berapa bulan pelanggan bertahan (asumsi). Default 6")
    i.add_argument("--porsi-ltv", default="30", help="porsi maksimal laba seumur pelanggan untuk hadiah, %%. Default 30")

    o = sub.add_parser("poin", allow_abbrev=False)
    o.add_argument("--belanja-per-poin", required=True, help="belanja (Rp) untuk mendapat 1 poin")
    o.add_argument("--nilai-poin", required=True, help="nilai tukar 1 poin (Rp)")
    o.add_argument("--margin", required=True, help="margin kotor %%")
    o.add_argument("--aov", help="nilai pesanan tipikal (Rp)")
    o.add_argument("--omzet-bulan", help="omzet program per bulan (Rp)")
    o.add_argument("--breakage", default="0", help="perkiraan %% poin yang tidak pernah ditukar (kedaluwarsa/lupa). Default 0")
    o.add_argument("--poin-beredar", help="jumlah poin yang belum ditukar sekarang")
    o.add_argument("--minimum-tukar", help="minimum poin untuk menukar")

    s = sub.add_parser("simulasi", allow_abbrev=False)
    umum(s)
    s.add_argument("--pelanggan-aktif", required=True, help="jumlah pelanggan aktif yang diajak program")
    s.add_argument("--skenario", action="append", help="nama:%%merujuk:teman_per_perujuk:%%beli (boleh diulang). "
                                                        "Bawaan: konservatif, realistis, optimis")
    s.add_argument("--pesanan-ulang", default="0", help="pesanan ulang rata-rata per teman baru (asumsi). Default 0")
    s.add_argument("--anggaran", help="anggaran hadiah maksimal (Rp)")
    s.add_argument("--cac-iklan", help="biaya iklan per pelanggan baru sebagai pembanding (Rp)")
    return p


def jalankan(argv=None):
    a = buat_parser().parse_args(argv)
    if a.perintah == "poin":
        return cetak_poin(nilai_poin(
            parse_rupiah(a.belanja_per_poin, nama="belanja per poin"), parse_rupiah(a.nilai_poin, nama="nilai poin"),
            parse_margin(a.margin),
            aov=parse_rupiah(a.aov, nama="nilai pesanan") if a.aov else None,
            omzet=parse_rupiah(a.omzet_bulan, nama="omzet") if a.omzet_bulan else None,
            breakage=parse_persen(a.breakage, "breakage", D(99)),
            beredar=parse_jumlah(a.poin_beredar, "poin beredar", boleh_nol=True, bulat_saja=True) if a.poin_beredar else None,
            min_tukar=parse_jumlah(a.minimum_tukar, "minimum tukar", bulat_saja=True) if a.minimum_tukar else None))
    aov = parse_rupiah(a.aov, nama="nilai pesanan")
    margin = parse_margin(a.margin)
    pem = parse_hadiah(a.hadiah_pemberi, aov, "hadiah pemberi")
    tem = parse_hadiah(a.hadiah_teman, aov, "hadiah teman")
    lain = parse_hadiah(a.biaya_lain, aov, "biaya lain")
    anggaran = parse_rupiah(a.anggaran, nama="anggaran") if getattr(a, "anggaran", None) else None
    cac = parse_rupiah(a.cac_iklan, nama="biaya iklan") if getattr(a, "cac_iklan", None) else None
    if a.perintah == "biaya":
        jml = parse_jumlah(a.jumlah_referral, "jumlah referral", bulat_saja=True) if a.jumlah_referral else None
        return cetak_biaya(biaya_referral(aov, margin, pem, tem, lain), jml, anggaran, cac)
    if a.perintah == "impas":
        frek = parse_jumlah(a.frekuensi_bulan, "frekuensi per bulan")
        umur = parse_jumlah(a.umur_bulan, "umur pelanggan (bulan)")
        porsi = parse_persen(a.porsi_ltv, "porsi laba", D(100))
        if porsi <= 0:
            raise InputError("porsi laba harus lebih dari 0%")
        return cetak_impas(titik_impas(aov, margin, pem, tem, lain, frek, umur, porsi))
    if a.perintah == "simulasi":
        pel = parse_jumlah(a.pelanggan_aktif, "pelanggan aktif", bulat_saja=True)
        sken = [parse_skenario(x) for x in (a.skenario or SKENARIO_BAWAAN)]
        ulang = parse_jumlah(a.pesanan_ulang, "pesanan ulang", boleh_nol=True)
        per, hasil = simulasi(pel, aov, margin, pem, tem, lain, sken, ulang, anggaran, cac)
        return cetak_simulasi(per, hasil, pel, ulang, anggaran, cac)
    raise InputError("perintah tidak dikenal")


def main(argv=None):
    try:
        print(jalankan(argv))
        return 0
    except InputError as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    except (ArithmeticError, InvalidOperation) as e:
        print(f"GAGAL: angka tidak bisa dihitung ({type(e).__name__}); periksa lagi input", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
