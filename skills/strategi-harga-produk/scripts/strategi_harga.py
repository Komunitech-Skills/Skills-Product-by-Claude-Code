#!/usr/bin/env python3
"""Kalkulator strategi harga untuk UMKM (Python standar saja, tanpa internet).

Jalankan: python3 scripts/strategi_harga.py <perintah> [opsi]   (Windows: py atau python)

Perintah:
  margin      margin vs markup, harga dari target margin/markup
  bep         titik impas (unit & rupiah) dari biaya tetap bulanan
  tangga      tangga harga eceran/reseller/grosir/agen dengan margin minimum
  diskon      dampak diskon/potongan/beli-X-gratis-Y: volume tambahan agar laba kotor tetap
  bundel      cek harga paket/bundling (hemat pembeli vs margin kita)
  elastisitas simulasi naik/turun harga (ESTIMASI, bukan kepastian)
  cantik      kandidat harga psikologis (Rp x.900, Rp x9.900, Rp x9.000, bulat)
  ppn         harga dengan PPN untuk PKP (sebelum/termasuk PPN)

Semua uang memakai Decimal. Aturan pembulatan (standar library Komunitech):
  - harga hasil diskon / total baris: dibulatkan ke rupiah terdekat (setengah ke atas)
  - harga MINIMUM agar margin tercapai: dibulatkan KE ATAS (agar target tidak meleset)
  - jumlah unit yang dibutuhkan (BEP, volume impas): dibulatkan KE ATAS
  - PPN: dihitung dari DPP persis lalu dibulatkan KE BAWAH sekali
"""
import argparse
import re
import sys
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal as D, InvalidOperation

NOL = D(0)
SATU = D(1)
SERATUS = D(100)
TARIF_PPN_BIASA = D("0.11")   # 12% x DPP nilai lain 11/12 = 11% efektif (barang/jasa non-mewah)
TARIF_PPN_MEWAH = D("0.12")   # barang mewah kena PPnBM: 12% x harga penuh


class InputError(ValueError):
    """Input pengguna tidak bisa dipakai. Pesan ditulis untuk orang awam."""


# ---------------------------------------------------------------- pembulatan & format

def bulat(x):
    return D(x).quantize(SATU, rounding=ROUND_HALF_UP)


def ke_atas(x):
    return D(x).quantize(SATU, rounding=ROUND_CEILING)


def ke_bawah(x):
    return D(x).quantize(SATU, rounding=ROUND_FLOOR)


def kelipatan(x, k, arah="dekat"):
    x, k = D(x), D(k)
    mode = {"dekat": ROUND_HALF_UP, "atas": ROUND_CEILING, "bawah": ROUND_FLOOR}[arah]
    return (x / k).quantize(SATU, rounding=mode) * k


def rp(x):
    """Format Rupiah Indonesia: Rp52.300 ; desimal ditampilkan bila ada (Rp12.345,67)."""
    x = D(x)
    tanda = "-" if x < 0 else ""
    x = abs(x)
    if x == x.to_integral_value():
        utuh, des = str(int(x)), ""
    else:
        q = x.quantize(D("0.01"), rounding=ROUND_HALF_UP)
        utuh, des = str(q).split(".")
        des = "," + des
    kelompok = []
    while len(utuh) > 3:
        kelompok.insert(0, utuh[-3:])
        utuh = utuh[:-3]
    kelompok.insert(0, utuh)
    return f"{tanda}Rp{'.'.join(kelompok)}{des}"


def pct(x, desimal=2):
    """Pecahan -> teks persen gaya Indonesia: 0.2581 -> 25,81%."""
    q = (D(x) * SERATUS).quantize(D(1).scaleb(-desimal), rounding=ROUND_HALF_UP)
    s = f"{q}".replace(".", ",")
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s + "%"


def angka(x):
    x = D(x)
    s = f"{int(x):,}".replace(",", ".") if x == x.to_integral_value() else str(x).replace(".", ",")
    return s


# ---------------------------------------------------------------- parsing input awam

_POLA_RIBUAN = re.compile(r"^\d{1,3}(\.\d{3})+(,\d+)?$")
_POLA_RIBUAN_KOMA = re.compile(r"^\d{1,3}(,\d{3})+$")


def parse_rupiah(nilai, boleh_nol=False, nama="angka"):
    """'Rp52.300', '52300', '52,3rb', '1,2jt', '12.345,67' -> Decimal."""
    if isinstance(nilai, (int, D)):
        x = D(nilai)
    elif isinstance(nilai, float):
        x = D(str(nilai))
    else:
        if nilai is None:
            raise InputError(f"{nama} kosong")
        s = str(nilai).strip().lower().replace(" ", "")
        s = re.sub(r"^(rp\.?|idr)", "", s)
        s = re.sub(r",-$", "", s)
        kali = SATU
        m = re.match(r"^(.*?)(rb|ribu|k|jt|juta)$", s)
        if m:
            s, suf = m.group(1), m.group(2)
            kali = D(1000) if suf in ("rb", "ribu", "k") else D(1000000)
            if _POLA_RIBUAN.match(s) and "," not in s:
                s = s.replace(".", "")
            else:
                s = s.replace(",", ".")
        elif _POLA_RIBUAN.match(s):
            s = s.replace(".", "").replace(",", ".")
        elif _POLA_RIBUAN_KOMA.match(s):
            s = s.replace(",", "")
        elif re.match(r"^\d+,\d{1,2}$", s):
            s = s.replace(",", ".")
        if not re.match(r"^\d+(\.\d+)?$", s):
            raise InputError(f"{nama} '{nilai}' tidak terbaca sebagai rupiah (contoh benar: 52.300, 52rb, 1,2jt)")
        try:
            x = D(s) * kali
        except InvalidOperation:
            raise InputError(f"{nama} '{nilai}' tidak terbaca sebagai rupiah")
    if x < 0 or (x == 0 and not boleh_nol):
        raise InputError(f"{nama} harus lebih dari 0 (didapat {nilai})")
    return x


def parse_persen(nilai, nama="persen", boleh_negatif=False, maks=D(100)):
    """'15', '15%', '12,5%' -> pecahan Decimal 0.15. Angka SELALU dianggap persen."""
    s = str(nilai).strip().replace(" ", "").replace("%", "").replace(",", ".")
    if s.startswith("+"):
        s = s[1:]
    if not re.match(r"^-?\d+(\.\d+)?$", s):
        raise InputError(f"{nama} '{nilai}' tidak terbaca (contoh benar: 15 atau 12,5%)")
    x = D(s)
    if x < 0 and not boleh_negatif:
        raise InputError(f"{nama} tidak boleh negatif (didapat {nilai})")
    if abs(x) > maks:
        raise InputError(f"{nama} {nilai}% di luar batas wajar (maks {maks}%)")
    return x / SERATUS


def _cek_biaya(biaya):
    if biaya >= 1:
        raise InputError("biaya persen (potongan marketplace dsb.) harus di bawah 100%")


def harga_minimum(hpp, margin_min, biaya=NOL):
    """Harga terkecil (rupiah bulat, ke atas) agar margin >= margin_min setelah potongan biaya%."""
    if margin_min + biaya >= 1:
        raise InputError(f"target margin {pct(margin_min)} + biaya {pct(biaya)} mencapai 100% atau lebih; tidak mungkin tercapai")
    return ke_atas(D(hpp) / (1 - biaya - margin_min))


# ---------------------------------------------------------------- 1. margin vs markup

def hitung_margin(hpp, harga=None, margin=None, markup=None, biaya=NOL):
    """Satu dari harga/margin/markup wajib diisi. Kembalikan dict lengkap."""
    hpp = D(hpp)
    _cek_biaya(biaya)
    diisi = [v is not None for v in (harga, margin, markup)]
    if sum(diisi) != 1:
        raise InputError("isi tepat satu: harga jual, target margin, atau target markup")
    if margin is not None:
        harga = harga_minimum(hpp, margin, biaya)
        sumber = f"dari target margin {pct(margin)} (dibulatkan ke atas)"
    elif markup is not None:
        harga = ke_atas(hpp * (1 + markup) / (1 - biaya))
        sumber = f"dari target markup {pct(markup)} (dibulatkan ke atas)"
    else:
        harga = D(harga)
        sumber = "harga yang diberikan"
    potongan = harga * biaya
    laba = harga - potongan - hpp
    return {
        "hpp": hpp, "harga": harga, "sumber": sumber, "biaya": biaya,
        "potongan": potongan, "laba": laba,
        "margin": laba / harga, "markup": laba / hpp,
    }


def margin_ke_markup(m):
    if m >= 1:
        raise InputError("margin harus di bawah 100%")
    return m / (1 - m)


def markup_ke_margin(k):
    return k / (1 + k)


# ---------------------------------------------------------------- 2. BEP

def hitung_bep(biaya_tetap, harga, biaya_var, biaya=NOL, target_laba=NOL, hari_jual=None, volume=None):
    _cek_biaya(biaya)
    harga, biaya_var = D(harga), D(biaya_var)
    kontribusi = harga * (1 - biaya) - biaya_var
    if kontribusi <= 0:
        raise InputError(f"harga {rp(harga)} tidak menutup modal per unit + potongan; setiap penjualan rugi, BEP tidak ada")
    unit = ke_atas((D(biaya_tetap) + D(target_laba)) / kontribusi)
    hasil = {
        "kontribusi": kontribusi, "rasio_kontribusi": kontribusi / harga,
        "unit": unit, "omzet": unit * harga,
        "biaya_tetap": D(biaya_tetap), "target_laba": D(target_laba),
    }
    if hari_jual:
        hasil["per_hari"] = ke_atas(unit / D(hari_jual))
        hasil["hari_jual"] = hari_jual
    if volume is not None:
        v = D(volume)
        hasil["volume"] = v
        hasil["laba_sekarang"] = v * kontribusi - D(biaya_tetap)
        unit_bep = ke_atas(D(biaya_tetap) / kontribusi)
        hasil["batas_aman"] = (v - unit_bep) / v if v > 0 else NOL
    return hasil


# ---------------------------------------------------------------- 3. tangga harga

def parse_level(teks):
    """'Reseller:10:15' (diskon 15%) atau 'Agen:50:=38000' (harga langsung)."""
    bagian = str(teks).split(":")
    if len(bagian) != 3 or not bagian[0].strip():
        raise InputError(f"level '{teks}' harus berformat Nama:minimal_beli:diskon%  (mis. Reseller:10:15 atau Agen:50:=38000)")
    nama, mq, nilai = bagian[0].strip(), bagian[1].strip(), bagian[2].strip()
    if not mq.isdigit() or int(mq) < 1:
        raise InputError(f"minimal beli di level '{nama}' harus angka bulat >= 1")
    if nilai.startswith("="):
        return {"nama": nama, "min": int(mq), "harga_langsung": parse_rupiah(nilai[1:], nama=f"harga {nama}")}
    return {"nama": nama, "min": int(mq), "diskon": parse_persen(nilai, nama=f"diskon {nama}", maks=D(99))}


def hitung_tangga(harga_ecer, hpp, level, margin_min, biaya=NOL, kelipatan_rp=None):
    _cek_biaya(biaya)
    harga_ecer, hpp = D(harga_ecer), D(hpp)
    batas = harga_minimum(hpp, margin_min, biaya)
    diskon_maks = 1 - batas / harga_ecer
    baris, peringatan = [], []
    for lv in sorted(level, key=lambda x: x["min"]):
        if "harga_langsung" in lv:
            h = lv["harga_langsung"]
        else:
            h = bulat(harga_ecer * (1 - lv["diskon"]))
        if kelipatan_rp:
            h = kelipatan(h, kelipatan_rp)
        laba = h * (1 - biaya) - hpp
        b = {"nama": lv["nama"], "min": lv["min"], "harga": h,
             "diskon": 1 - h / harga_ecer, "laba": laba, "margin": laba / h,
             "laba_min_beli": laba * lv["min"]}
        b["aman"] = b["margin"] >= margin_min
        if not b["aman"]:
            peringatan.append(f"{lv['nama']}: margin {pct(b['margin'])} di bawah minimum {pct(margin_min)}; harga terendah yang aman {rp(batas)}")
        baris.append(b)
    for a, b in zip(baris, baris[1:]):
        if b["harga"] > a["harga"]:
            peringatan.append(f"{b['nama']} (beli banyak) lebih mahal dari {a['nama']}; tangga harga terbalik")
    if diskon_maks < 0:
        peringatan.insert(0, f"harga eceran {rp(harga_ecer)} sendiri sudah di bawah margin minimum; naikkan harga eceran atau tekan HPP")
    return {"batas": batas, "diskon_maks": diskon_maks, "baris": baris, "peringatan": peringatan,
            "harga_ecer": harga_ecer, "hpp": hpp, "margin_min": margin_min, "biaya": biaya}


# ---------------------------------------------------------------- 4. dampak diskon

def parse_bxgy(teks):
    m = re.match(r"^\s*(\d+)\s*[:+/x]\s*(\d+)\s*$", str(teks))
    if not m or int(m.group(1)) < 1 or int(m.group(2)) < 1:
        raise InputError(f"'{teks}' harus berformat beli:gratis, mis. 2:1 untuk 'beli 2 gratis 1'")
    return int(m.group(1)), int(m.group(2))


def hitung_diskon(harga, hpp, diskon=None, potongan=None, bxgy=None, volume=None, biaya=NOL, margin_min=None):
    _cek_biaya(biaya)
    harga, hpp = D(harga), D(hpp)
    if sum(v is not None for v in (diskon, potongan, bxgy)) != 1:
        raise InputError("isi tepat satu jenis promo: diskon %, potongan rupiah, atau beli-X-gratis-Y")
    if diskon is not None:
        if diskon >= 1:
            raise InputError("diskon harus di bawah 100%")
        harga_promo = bulat(harga * (1 - diskon))
        label = f"diskon {pct(diskon)}"
    elif potongan is not None:
        if potongan >= harga:
            raise InputError("potongan harga tidak boleh sama atau melebihi harga jual")
        harga_promo = harga - D(potongan)
        label = f"potongan {rp(potongan)}"
    else:
        x, y = bxgy
        harga_promo = harga * x / (x + y)   # harga efektif per unit, TIDAK dibulatkan
        label = f"beli {x} gratis {y}"
    laba_normal = harga * (1 - biaya) - hpp
    if laba_normal <= 0:
        raise InputError(f"di harga normal {rp(harga)} saja sudah tidak untung (HPP + potongan >= harga); perbaiki harga dulu")
    laba_promo = harga_promo * (1 - biaya) - hpp
    h = {"label": label, "harga": harga, "harga_promo": harga_promo, "diskon_efektif": 1 - harga_promo / harga,
         "laba_normal": laba_normal, "laba_promo": laba_promo,
         "margin_normal": laba_normal / harga, "margin_promo": laba_promo / harga_promo,
         "rugi": laba_promo <= 0}
    if not h["rugi"]:
        faktor = laba_normal / laba_promo
        h["faktor"] = faktor
        h["tambahan"] = faktor - 1
        if volume is not None:
            h["volume"] = D(volume)
            h["volume_perlu"] = ke_atas(D(volume) * faktor)
            h["laba_kotor_normal"] = D(volume) * laba_normal
    if margin_min is not None:
        batas = harga_minimum(hpp, margin_min, biaya)
        h["batas"] = batas
        h["diskon_maks"] = 1 - batas / harga
    return h


# ---------------------------------------------------------------- 5. bundel

def parse_item(teks):
    """'Roti Sobek:28000:11500' atau 'Roti Sobek:28000:11500:2' (qty)."""
    b = str(teks).split(":")
    if len(b) not in (3, 4) or not b[0].strip():
        raise InputError(f"item '{teks}' harus berformat Nama:harga:hpp[:jumlah], mis. Bolu Pandan:45000:19000")
    qty = 1
    if len(b) == 4:
        if not b[3].strip().isdigit() or int(b[3]) < 1:
            raise InputError(f"jumlah item '{b[0]}' harus angka bulat >= 1")
        qty = int(b[3])
    return {"nama": b[0].strip(), "harga": parse_rupiah(b[1], nama=f"harga {b[0]}"),
            "hpp": parse_rupiah(b[2], nama=f"HPP {b[0]}"), "qty": qty}


def hitung_bundel(item, harga_bundel, biaya_tambahan=NOL, biaya=NOL, margin_min=None):
    _cek_biaya(biaya)
    if not item:
        raise InputError("isi minimal 2 item untuk paket")
    harga_bundel = D(harga_bundel)
    total = sum(i["harga"] * i["qty"] for i in item)
    hpp_isi = sum(i["hpp"] * i["qty"] for i in item)
    hpp_bundel = hpp_isi + D(biaya_tambahan)
    laba_bundel = harga_bundel * (1 - biaya) - hpp_bundel
    laba_terpisah = total * (1 - biaya) - hpp_isi
    h = {"total_normal": total, "hpp_isi": hpp_isi, "hpp_bundel": hpp_bundel, "harga_bundel": harga_bundel,
         "hemat": total - harga_bundel, "hemat_persen": (total - harga_bundel) / total,
         "laba_bundel": laba_bundel, "margin_bundel": laba_bundel / harga_bundel,
         "laba_terpisah": laba_terpisah, "margin_terpisah": laba_terpisah / total,
         "peringatan": []}
    if harga_bundel >= total:
        h["peringatan"].append("harga paket tidak lebih murah dari beli satuan; pembeli tidak punya alasan pilih paket")
    if laba_bundel <= 0:
        h["peringatan"].append("paket ini RUGI per paket")
    elif laba_terpisah > 0:
        h["faktor"] = laba_terpisah / laba_bundel
    if margin_min is not None:
        h["batas"] = harga_minimum(hpp_bundel, margin_min, biaya)
        h["margin_min"] = margin_min
        if harga_bundel < h["batas"]:
            h["peringatan"].append(f"margin paket {pct(h['margin_bundel'])} di bawah minimum {pct(margin_min)}; harga paket terendah yang aman {rp(h['batas'])}")
    return h


# ---------------------------------------------------------------- 6. elastisitas (ESTIMASI)

ELASTISITAS_BAWAAN = [D("-0.5"), D("-1"), D("-2")]


def hitung_elastisitas(harga, volume, hpp, perubahan=None, elastisitas=None, biaya=NOL, biaya_tetap=NOL,
                       harga_baru=None):
    """Perkiraan garis lurus: volume baru = volume x (1 + e x perubahan harga).

    Skenario bisa berupa persen perubahan (harga baru dibulatkan ke rupiah terdekat)
    dan/atau harga baru langsung (persen dihitung persis dari harga itu)."""
    _cek_biaya(biaya)
    harga, volume, hpp = D(harga), D(volume), D(hpp)
    daftar = [(dp, bulat(harga * (1 + dp)) if dp > -1 else None) for dp in (perubahan or [])]
    daftar += [(D(hb) / harga - 1, D(hb)) for hb in (harga_baru or [])]
    if not daftar:
        raise InputError("isi minimal satu skenario: perubahan harga % atau harga baru")
    el = elastisitas or ELASTISITAS_BAWAAN
    laba_unit = harga * (1 - biaya) - hpp
    dasar = volume * laba_unit - D(biaya_tetap)
    skenario = []
    for dp, hb in daftar:
        if dp <= -1:
            raise InputError("penurunan harga harus kurang dari 100%")
        lu = hb * (1 - biaya) - hpp
        s = {"perubahan": dp, "harga_baru": hb, "laba_unit": lu, "hasil": []}
        if lu > 0:
            s["volume_impas"] = ke_atas(volume * laba_unit / lu)
            if dp != 0:
                s["elastisitas_impas"] = (volume * laba_unit / lu / volume - 1) / dp
        for e in el:
            vb = volume * (1 + e * dp)
            if vb < 0:
                vb = NOL
            vb = bulat(vb)
            laba = vb * lu - D(biaya_tetap)
            s["hasil"].append({"e": e, "volume": vb, "omzet": vb * hb, "laba": laba, "selisih": laba - dasar})
        skenario.append(s)
    return {"dasar": dasar, "laba_unit": laba_unit, "skenario": skenario,
            "peringatan_besar": any(abs(dp) > D("0.2") for dp, _ in daftar)}


# ---------------------------------------------------------------- 7. harga cantik

def kandidat_cantik(harga):
    p = D(harga)
    c = {}

    def tambah(nilai, pola):
        if nilai > 0 and nilai not in c:
            c[nilai] = pola

    for langkah, kurang, pola, syarat in (
        (D(10000), D(100), "akhiran 9.900", p >= 10000),
        (D(10000), D(1000), "akhiran 9.000", p >= 50000),
        (D(1000), D(100), "akhiran 900", True),
    ):
        if not syarat:
            continue
        atas = kelipatan(p + kurang, langkah, "atas") - kurang
        bawah = kelipatan(p + kurang, langkah, "bawah") - kurang
        tambah(atas, pola)
        tambah(bawah, pola)
    if p < 10000:
        tambah(kelipatan(p, 500, "atas"), "kelipatan 500")
        tambah(kelipatan(p, 500, "bawah"), "kelipatan 500")
    tambah(kelipatan(p, 5000 if p >= 100000 else 1000, "atas"), "angka bulat (kesan premium)")
    return sorted(c.items())


def hitung_cantik(harga, hpp=None, margin_min=None, biaya=NOL, harga_min=None):
    _cek_biaya(biaya)
    batas = None
    if hpp is not None and margin_min is not None:
        batas = harga_minimum(hpp, margin_min, biaya)
    if harga_min is not None:
        batas = max(batas or NOL, D(harga_min))
    baris = []
    for nilai, pola in kandidat_cantik(harga):
        b = {"harga": nilai, "pola": pola, "selisih": nilai - D(harga)}
        if hpp is not None:
            b["laba"] = nilai * (1 - biaya) - D(hpp)
            b["margin"] = b["laba"] / nilai
        b["aman"] = None if batas is None else nilai >= batas
        baris.append(b)
    return {"harga": D(harga), "batas": batas, "baris": baris}


# ---------------------------------------------------------------- 8. PPN (PKP)

def hitung_ppn(harga, mode="belum", mewah=False):
    """mode 'belum': harga = DPP. mode 'termasuk': harga = DPP + PPN, cari DPP bulat terbesar."""
    t = TARIF_PPN_MEWAH if mewah else TARIF_PPN_BIASA
    harga = D(harga)
    if mode == "belum":
        dpp = harga
        ppn = ke_bawah(dpp * t)
    elif mode == "termasuk":
        dpp = ke_bawah(harga / (1 + t))
        while dpp + 1 + ke_bawah((dpp + 1) * t) <= harga:
            dpp += 1
        while dpp > 0 and dpp + ke_bawah(dpp * t) > harga:
            dpp -= 1
        ppn = ke_bawah(dpp * t)
    else:
        raise InputError("mode PPN harus 'belum' atau 'termasuk'")
    total = dpp + ppn
    return {"dpp": dpp, "ppn": ppn, "total": total, "sisa": harga - total if mode == "termasuk" else NOL,
            "tarif": t, "mewah": mewah, "mode": mode}


# ---------------------------------------------------------------- keluaran teks

def tabel(kepala, baris):
    lebar = [max(len(str(x)) for x in kol) for kol in zip(kepala, *baris)]
    garis = lambda r: "| " + " | ".join(str(x).ljust(w) for x, w in zip(r, lebar)) + " |"
    return "\n".join([garis(kepala), "|" + "|".join("-" * (w + 2) for w in lebar) + "|"] + [garis(r) for r in baris])


def cetak_margin(h):
    out = [f"HPP/modal per unit : {rp(h['hpp'])}",
           f"Harga jual         : {rp(h['harga'])}  ({h['sumber']})"]
    if h["biaya"]:
        out.append(f"{'Potongan ' + pct(h['biaya']):<19}: {rp(bulat(h['potongan']))}")
    out += [f"Laba kotor/unit    : {rp(bulat(h['laba']))}",
            f"Margin (laba/harga): {pct(h['margin'])}",
            f"Markup (laba/HPP)  : {pct(h['markup'])}",
            "Catatan: margin dihitung dari HARGA JUAL, markup dari HPP. Markup 50% = margin 33,33%, bukan 50%."]
    return "\n".join(out)


def cetak_bep(h):
    out = [f"Laba kontribusi per unit : {rp(bulat(h['kontribusi']))} ({pct(h['rasio_kontribusi'])} dari harga)",
           f"Biaya tetap per bulan    : {rp(h['biaya_tetap'])}"]
    if h["target_laba"]:
        out.append(f"Target laba bersih       : {rp(h['target_laba'])}")
    judul = "Unit harus terjual/bulan" if h["target_laba"] else "BEP (titik impas)       "
    out += [f"{judul} : {angka(h['unit'])} unit (dibulatkan ke atas)",
            f"Omzet setara             : {rp(h['omzet'])}"]
    if "per_hari" in h:
        out.append(f"Per hari ({h['hari_jual']} hari jual)  : {angka(h['per_hari'])} unit")
    if "volume" in h:
        out.append(f"Penjualan sekarang       : {angka(h['volume'])} unit -> laba/rugi {rp(bulat(h['laba_sekarang']))}/bulan")
        out.append(f"Batas aman (margin of safety): {pct(h['batas_aman'])} penjualan boleh turun sebelum rugi")
    return "\n".join(out)


def cetak_tangga(h):
    rows = [[b["nama"], f">= {b['min']}", rp(b["harga"]), pct(b["diskon"]), rp(bulat(b["laba"])),
             pct(b["margin"]), rp(bulat(b["laba_min_beli"])), "OK" if b["aman"] else "DI BAWAH MIN"] for b in h["baris"]]
    out = [tabel(["Level", "Min beli", "Harga/unit", "Diskon", "Laba/unit", "Margin", "Laba di min beli", "Status"], rows),
           "",
           f"Margin minimum {pct(h['margin_min'])} -> harga terendah yang aman {rp(h['batas'])} "
           f"(diskon maksimal {pct(max(h['diskon_maks'], NOL))} dari eceran)"]
    out += ["PERHATIAN: " + p for p in h["peringatan"]]
    return "\n".join(out)


def cetak_diskon(h):
    out = [f"Promo              : {h['label']} (diskon efektif {pct(h['diskon_efektif'])})",
           f"Harga normal       : {rp(h['harga'])} -> laba {rp(bulat(h['laba_normal']))}/unit (margin {pct(h['margin_normal'])})",
           f"Harga saat promo   : {rp(h['harga_promo'])} -> laba {rp(h['laba_promo'])}/unit (margin {pct(h['margin_promo'])})"]
    if h["rugi"]:
        out.append("PERHATIAN: promo ini RUGI per unit. Menambah penjualan justru menambah rugi. Kecilkan promo.")
    else:
        out.append(f"Agar laba kotor TETAP sama, penjualan harus naik {pct(h['tambahan'])} (x{str(h['faktor'].quantize(D('0.01'), ROUND_HALF_UP)).replace('.', ',')})")
        if "volume" in h:
            out.append(f"Dari {angka(h['volume'])} unit -> minimal {angka(h['volume_perlu'])} unit (laba kotor normal {rp(bulat(h['laba_kotor_normal']))})")
    if "batas" in h:
        out.append(f"Diskon maksimal agar margin >= minimum: {pct(max(h['diskon_maks'], NOL))} (harga terendah {rp(h['batas'])})")
    return "\n".join(out)


def cetak_bundel(h):
    out = [f"Total beli satuan   : {rp(h['total_normal'])}",
           f"Harga paket         : {rp(h['harga_bundel'])} -> pembeli hemat {rp(h['hemat'])} ({pct(h['hemat_persen'])})",
           f"HPP paket           : {rp(h['hpp_bundel'])} (isi {rp(h['hpp_isi'])} + kemasan/tambahan {rp(h['hpp_bundel'] - h['hpp_isi'])})",
           f"Laba per paket      : {rp(bulat(h['laba_bundel']))} (margin {pct(h['margin_bundel'])})",
           f"Kalau dijual satuan : laba {rp(bulat(h['laba_terpisah']))} (margin {pct(h['margin_terpisah'])})"]
    if "faktor" in h:
        out.append(f"Paket harus menambah transaksi {pct(h['faktor'] - 1)} agar laba kotor sama dengan jual satuan "
                   "(kalau paket menarik pembeli baru / isi yang tadinya tak dibeli, ini mudah tercapai)")
    if "batas" in h:
        out.append(f"Harga paket terendah untuk margin {pct(h['margin_min'])}: {rp(h['batas'])}")
    out += ["PERHATIAN: " + p for p in h["peringatan"]]
    return "\n".join(out)


def cetak_elastisitas(h):
    out = ["ESTIMASI - bukan kepastian. Elastisitas = seberapa peka pembeli pada harga "
           "(-0,5 tidak peka, -1 sedang, -2 sangat peka). Model garis lurus, wajar untuk perubahan kecil.",
           f"Laba saat ini: {rp(bulat(h['dasar']))} (laba/unit {rp(bulat(h['laba_unit']))})", ""]
    for s in h["skenario"]:
        arah = "naik" if s["perubahan"] > 0 else "turun"
        out.append(f"Harga {arah} {pct(abs(s['perubahan']))} -> {rp(s['harga_baru'])} (laba/unit {rp(bulat(s['laba_unit']))})")
        if "volume_impas" in s:
            teks = f"  Volume impas (PASTI, bukan estimasi): {angka(s['volume_impas'])} unit agar laba sama"
            if "elastisitas_impas" in s:
                teks += f"; elastisitas impas {str(s['elastisitas_impas'].quantize(D('0.01'), ROUND_HALF_UP)).replace('.', ',')}"
            out.append(teks)
        else:
            out.append("  PERHATIAN: di harga ini setiap unit rugi")
        rows = [[str(r["e"]).replace(".", ","), angka(r["volume"]), rp(r["omzet"]), rp(bulat(r["laba"])),
                 ("+" if r["selisih"] > 0 else "") + rp(bulat(r["selisih"]))] for r in s["hasil"]]
        out.append(tabel(["Elastisitas", "Volume (est.)", "Omzet (est.)", "Laba (est.)", "Selisih"], rows))
        out.append("")
    if h["peringatan_besar"]:
        out.append("PERHATIAN: ada perubahan > 20%; perkiraan garis lurus makin tidak akurat. Uji kecil dulu.")
    return "\n".join(out).rstrip()


def cetak_cantik(h):
    rows = []
    for b in h["baris"]:
        r = [rp(b["harga"]), b["pola"], ("+" if b["selisih"] > 0 else "") + rp(b["selisih"])]
        if "margin" in b:
            r += [rp(bulat(b["laba"])), pct(b["margin"])]
        if b["aman"] is not None:
            r.append("OK" if b["aman"] else "di bawah batas")
        rows.append(r)
    kepala = ["Kandidat", "Pola", "Selisih"]
    if h["baris"] and "margin" in h["baris"][0]:
        kepala += ["Laba/unit", "Margin"]
    if h["batas"] is not None:
        kepala.append("Status")
    out = [f"Harga hitungan: {rp(h['harga'])}", tabel(kepala, rows)]
    if h["batas"] is not None:
        out.append(f"Batas harga terendah: {rp(h['batas'])}")
    return "\n".join(out)


def cetak_ppn(h, status):
    out = []
    if status == "non-pkp":
        out.append("SIMULASI SAJA: penjual BUKAN PKP tidak boleh memungut/mencantumkan PPN. Pasang harga tanpa PPN.")
    elif status == "belum-tahu":
        out.append("Pengingat: hanya PKP (Pengusaha Kena Pajak) yang memungut PPN. Pastikan status usahamu.")
    tarif = "12% penuh (barang mewah)" if h["mewah"] else "12% x DPP nilai lain 11/12 = 11% efektif"
    out += [f"Tarif  : {tarif}",
            f"DPP (harga sebelum PPN): {rp(h['dpp'])}",
            f"PPN    : {rp(h['ppn'])} (dibulatkan ke bawah)",
            f"Total  : {rp(h['total'])}"]
    if h["mode"] == "termasuk":
        out.append(f"Sisa pembulatan: {rp(h['sisa'])}")
    out.append("Margin & laba dihitung dari DPP, bukan dari harga termasuk PPN (PPN bukan pendapatan). "
               "Pembulatan belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax.")
    return "\n".join(out)


# ---------------------------------------------------------------- CLI

def _opsi_biaya(p):
    p.add_argument("--biaya-persen", default="0", help="potongan % dari harga jual (admin marketplace, dll). Default 0")


def buat_parser():
    ap = argparse.ArgumentParser(description="Kalkulator strategi harga (Rupiah, Decimal).")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p = sub.add_parser("margin", help="margin vs markup")
    p.add_argument("--hpp", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--harga")
    g.add_argument("--margin", help="target margin %% dari harga jual")
    g.add_argument("--markup", help="target markup %% dari HPP")
    _opsi_biaya(p)

    p = sub.add_parser("bep", help="titik impas")
    p.add_argument("--biaya-tetap", required=True, help="biaya tetap per bulan (sewa, gaji tetap, listrik dasar, cicilan alat)")
    p.add_argument("--harga", required=True)
    p.add_argument("--hpp", required=True, help="biaya variabel per unit (bahan, kemasan, upah borongan)")
    p.add_argument("--target-laba", default="0")
    p.add_argument("--hari-jual", type=int)
    p.add_argument("--volume", help="penjualan per bulan sekarang (unit)")
    _opsi_biaya(p)

    p = sub.add_parser("tangga", help="tangga harga reseller/grosir")
    p.add_argument("--harga-ecer", required=True)
    p.add_argument("--hpp", required=True)
    p.add_argument("--level", action="append", required=True, help="Nama:min_beli:diskon%%  atau Nama:min_beli:=harga")
    p.add_argument("--margin-min", required=True)
    p.add_argument("--kelipatan", help="bulatkan harga level ke kelipatan ini (mis. 500)")
    _opsi_biaya(p)

    p = sub.add_parser("diskon", help="dampak promo pada volume")
    p.add_argument("--harga", required=True)
    p.add_argument("--hpp", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--diskon", help="diskon %%")
    g.add_argument("--potongan", help="potongan rupiah per unit")
    g.add_argument("--beli-gratis", help="beli:gratis, mis. 2:1")
    p.add_argument("--volume", help="penjualan normal (unit) dalam periode yang sama")
    p.add_argument("--margin-min")
    _opsi_biaya(p)

    p = sub.add_parser("bundel", help="cek harga paket")
    p.add_argument("--item", action="append", required=True, help="Nama:harga:hpp[:jumlah]")
    p.add_argument("--harga-bundel", required=True)
    p.add_argument("--biaya-tambahan", default="0", help="kemasan/hampers/kartu tambahan per paket")
    p.add_argument("--margin-min")
    _opsi_biaya(p)

    p = sub.add_parser("elastisitas", help="simulasi naik/turun harga (ESTIMASI)")
    p.add_argument("--harga", required=True)
    p.add_argument("--volume", required=True)
    p.add_argument("--hpp", required=True)
    p.add_argument("--ubah", action="append", help="perubahan harga %%, mis. 10 atau -10 (bisa diulang)")
    p.add_argument("--harga-baru", action="append", help="harga baru langsung, mis. 29.900 (bisa diulang)")
    p.add_argument("--elastisitas", action="append", help="mis. -1,5 (bisa diulang). Default -0,5 / -1 / -2")
    p.add_argument("--biaya-tetap", default="0")
    _opsi_biaya(p)

    p = sub.add_parser("cantik", help="kandidat harga psikologis")
    p.add_argument("--harga", required=True)
    p.add_argument("--hpp")
    p.add_argument("--margin-min")
    p.add_argument("--harga-min", help="batas bawah lain (mis. dari harga-jual-marketplace)")
    _opsi_biaya(p)

    p = sub.add_parser("ppn", help="harga dengan PPN (PKP)")
    p.add_argument("--harga", required=True)
    p.add_argument("--mode", choices=["belum", "termasuk"], default="belum")
    p.add_argument("--status-pkp", choices=["pkp", "non-pkp", "belum-tahu"], default="belum-tahu")
    p.add_argument("--mewah", action="store_true")
    return ap


def _parse_el(s):
    t = str(s).strip().replace(",", ".")
    if not re.match(r"^-?\d+(\.\d+)?$", t):
        raise InputError(f"elastisitas '{s}' tidak terbaca (contoh: -1,5)")
    e = D(t)
    if e > 0:
        raise InputError("elastisitas harga hampir selalu negatif (harga naik -> penjualan turun); tulis mis. -1,5")
    return e


def jalankan(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # angka negatif seperti "-1,5" / "-10" setelah opsi: gabungkan jadi --opsi=-1,5 agar tidak dikira opsi
    rapi = []
    for tok in argv:
        if rapi and re.match(r"^-\d", tok) and rapi[-1].startswith("--") and "=" not in rapi[-1]:
            rapi[-1] = f"{rapi[-1]}={tok}"
        else:
            rapi.append(tok)
    a = buat_parser().parse_args(rapi)
    biaya = parse_persen(getattr(a, "biaya_persen", "0"), nama="biaya persen", maks=D(99))
    if a.perintah == "margin":
        h = hitung_margin(parse_rupiah(a.hpp, nama="HPP"),
                          harga=parse_rupiah(a.harga, nama="harga") if a.harga else None,
                          margin=parse_persen(a.margin, nama="margin", maks=D(99)) if a.margin else None,
                          markup=parse_persen(a.markup, nama="markup", maks=D(10000)) if a.markup else None,
                          biaya=biaya)
        return cetak_margin(h)
    if a.perintah == "bep":
        h = hitung_bep(parse_rupiah(a.biaya_tetap, boleh_nol=True, nama="biaya tetap"), parse_rupiah(a.harga, nama="harga"),
                       parse_rupiah(a.hpp, boleh_nol=True, nama="HPP"), biaya,
                       parse_rupiah(a.target_laba, boleh_nol=True, nama="target laba"), a.hari_jual,
                       parse_rupiah(a.volume, boleh_nol=True, nama="volume") if a.volume else None)
        return cetak_bep(h)
    if a.perintah == "tangga":
        h = hitung_tangga(parse_rupiah(a.harga_ecer, nama="harga eceran"), parse_rupiah(a.hpp, nama="HPP"),
                          [parse_level(x) for x in a.level], parse_persen(a.margin_min, nama="margin minimum", maks=D(99)),
                          biaya, parse_rupiah(a.kelipatan, nama="kelipatan") if a.kelipatan else None)
        return cetak_tangga(h)
    if a.perintah == "diskon":
        h = hitung_diskon(parse_rupiah(a.harga, nama="harga"), parse_rupiah(a.hpp, nama="HPP"),
                          diskon=parse_persen(a.diskon, nama="diskon") if a.diskon else None,
                          potongan=parse_rupiah(a.potongan, nama="potongan") if a.potongan else None,
                          bxgy=parse_bxgy(a.beli_gratis) if a.beli_gratis else None,
                          volume=parse_rupiah(a.volume, nama="volume") if a.volume else None,
                          biaya=biaya,
                          margin_min=parse_persen(a.margin_min, nama="margin minimum", maks=D(99)) if a.margin_min else None)
        return cetak_diskon(h)
    if a.perintah == "bundel":
        item = [parse_item(x) for x in a.item]
        if len(item) < 2 and item[0]["qty"] < 2:
            raise InputError("paket butuh minimal 2 item (atau 1 item dengan jumlah >= 2)")
        h = hitung_bundel(item, parse_rupiah(a.harga_bundel, nama="harga paket"),
                          parse_rupiah(a.biaya_tambahan, boleh_nol=True, nama="biaya tambahan"), biaya,
                          parse_persen(a.margin_min, nama="margin minimum", maks=D(99)) if a.margin_min else None)
        return cetak_bundel(h)
    if a.perintah == "elastisitas":
        h = hitung_elastisitas(parse_rupiah(a.harga, nama="harga"), parse_rupiah(a.volume, nama="volume"),
                               parse_rupiah(a.hpp, nama="HPP"),
                               [parse_persen(x, nama="perubahan harga", boleh_negatif=True, maks=D(99)) for x in (a.ubah or [])],
                               [_parse_el(x) for x in a.elastisitas] if a.elastisitas else None,
                               biaya, parse_rupiah(a.biaya_tetap, boleh_nol=True, nama="biaya tetap"),
                               [parse_rupiah(x, nama="harga baru") for x in (a.harga_baru or [])])
        return cetak_elastisitas(h)
    if a.perintah == "cantik":
        h = hitung_cantik(parse_rupiah(a.harga, nama="harga"),
                          parse_rupiah(a.hpp, nama="HPP") if a.hpp else None,
                          parse_persen(a.margin_min, nama="margin minimum", maks=D(99)) if a.margin_min else None,
                          biaya, parse_rupiah(a.harga_min, nama="harga minimum") if a.harga_min else None)
        return cetak_cantik(h)
    if a.perintah == "ppn":
        h = hitung_ppn(parse_rupiah(a.harga, nama="harga"), a.mode, a.mewah)
        return cetak_ppn(h, a.status_pkp)
    raise InputError("perintah tidak dikenal")


def main(argv=None):
    try:
        print(jalankan(argv))
        return 0
    except InputError as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
