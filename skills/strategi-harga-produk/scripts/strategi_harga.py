#!/usr/bin/env python3
"""Kalkulator strategi harga untuk UMKM (Python standar saja, tanpa internet).

Jalankan: python3 scripts/strategi_harga.py <perintah> [opsi]   (Windows: py atau python)

Perintah:
  margin      margin vs markup, harga dari target margin/markup, cek status vs margin minimum
  bep         titik impas (unit & rupiah) dari biaya tetap bulanan
  tangga      tangga harga eceran/reseller/grosir/agen + untung reseller di harga eceran anjuran
  diskon      dampak diskon/potongan/beli-X-gratis-Y: volume tambahan agar laba kotor tetap, selalu dengan
              DISKON MAKSIMAL terhadap margin minimum & harga beli reseller/agen; --rentang 10-20 = tabel rentang
  bundel      cek harga paket/bundling (hemat pembeli vs margin kita)
  elastisitas simulasi naik/turun harga (ESTIMASI, bukan kepastian)
  cantik      kandidat harga psikologis (Rp x.900, Rp x9.900, Rp x9.000, bulat)
  ppn         harga dengan PPN untuk PKP (sebelum/termasuk PPN)

PKP: semua perintah hitungan menerima --ppn termasuk (harga yang dimasukkan = harga tayang
SUDAH termasuk PPN) atau --ppn belum (harga yang dimasukkan = DPP). Margin & laba selalu dari
DPP; potongan persen (marketplace) dihitung dari harga tayang termasuk PPN.

Semua uang memakai Decimal. Aturan pembulatan (standar library Komunitech):
  - harga hasil diskon / total baris: dibulatkan ke rupiah terdekat (setengah ke atas)
  - harga MINIMUM agar margin tercapai: dibulatkan KE ATAS (agar target tidak meleset)
  - jumlah unit yang dibutuhkan (BEP, volume impas): dibulatkan KE ATAS
  - PPN: dihitung dari DPP persis lalu dibulatkan KE BAWAH sekali
  - harga termasuk PPN: DPP = rupiah bulat terbesar dengan DPP + PPN <= harga; sisa ditampilkan
"""
import argparse
import re
import sys
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal as D, InvalidOperation

VERSI = "1.0.9"
NOL = D(0)
SATU = D(1)
SERATUS = D(100)
TARIF_PPN_BIASA = D("0.11")   # 12% x DPP nilai lain 11/12 = 11% efektif (barang/jasa non-mewah)
TARIF_PPN_MEWAH = D("0.12")   # barang mewah kena PPnBM: 12% x harga penuh
MARGIN_RESELLER_BAWAAN = D("0.10")
# margin minimum bawaan per kategori (dipakai bila pengguna tidak menyebut --margin-min)
MARGIN_MIN_KATEGORI = {
    "pangan": (D("0.40"), "pangan: makanan/minuman, termasuk hampers/parsel makanan, kue, sambal, frozen food"),
    "jasa": (D("0.50"), "jasa"),
    "umum": (D("0.30"), "barang umum non-pangan"),
}


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
    """'Rp52.300', '52300', '52,3rb', '1,2jt', '12.345,67' -> Decimal.

    Titik = pemisah ribuan (gaya Indonesia). Angka seperti '12.5' atau '1.25' ambigu
    (dua belas ribu lima ratus? dua belas koma lima?) sehingga DITOLAK, bukan ditebak."""
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
        elif re.match(r"^\d+\.\d+$", s):
            raise InputError(f"{nama} '{nilai}' ambigu: titik dipakai sebagai pemisah ribuan. "
                             f"Tulis mis. 12.500 (dua belas ribu lima ratus) atau 12,5rb")
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


def _cek_positif(harga, apa):
    if D(harga) <= 0:
        raise InputError(f"{apa} menjadi Rp0 setelah dihitung/dibulatkan; perbesar harga atau kecilkan diskon/kelipatan")


# ---------------------------------------------------------------- PPN (PKP)

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


class Pajak:
    """Cara membaca harga yang dimasukkan pengguna.

    mode None      : bukan PKP. harga = pendapatan (DPP) = harga tayang.
    mode 'belum'   : harga yang dimasukkan = DPP (sebelum PPN); harga tayang = DPP + PPN.
    mode 'termasuk': harga yang dimasukkan = harga tayang termasuk PPN; DPP dicari mundur.
    Laba & margin selalu dari DPP. Potongan persen (marketplace) dihitung dari harga tayang.
    """

    def __init__(self, mode=None, mewah=False):
        if mode not in (None, "belum", "termasuk"):
            raise InputError("mode PPN harus 'belum' atau 'termasuk'")
        self.mode = mode
        self.mewah = mewah
        self.tarif = TARIF_PPN_MEWAH if mewah else TARIF_PPN_BIASA

    @property
    def aktif(self):
        return self.mode is not None

    def ppn_dari_dpp(self, dpp):
        return ke_bawah(D(dpp) * self.tarif) if self.aktif else NOL

    def pecah(self, harga):
        """harga (satuan input) -> (dpp, harga tayang)."""
        harga = D(harga)
        if self.mode == "termasuk":
            h = hitung_ppn(harga, "termasuk", self.mewah)
            if h["dpp"] <= 0:
                raise InputError(f"harga {rp(harga)} terlalu kecil untuk dipisah DPP dan PPN-nya")
            return h["dpp"], harga
        if self.mode == "belum":
            return harga, harga + self.ppn_dari_dpp(harga)
        return harga, harga

    def dari_dpp(self, dpp):
        """DPP -> harga dalam satuan input (untuk 'termasuk' = DPP + PPN)."""
        return D(dpp) + self.ppn_dari_dpp(dpp) if self.mode == "termasuk" else D(dpp)

    def laba(self, harga, hpp, biaya=NOL):
        dpp, tayang = self.pecah(harga)
        return dpp - biaya * tayang - D(hpp)

    def margin(self, harga, hpp, biaya=NOL):
        dpp, _ = self.pecah(harga)
        return self.laba(harga, hpp, biaya) / dpp

    def minimum(self, hpp, margin_min, biaya=NOL):
        """Harga terkecil (satuan input, rupiah bulat) agar margin (dari DPP) >= margin_min."""
        hpp = D(hpp)
        if not self.aktif:
            if margin_min + biaya >= 1:
                raise InputError(f"target margin {pct(margin_min)} + biaya {pct(biaya)} mencapai 100% atau lebih; tidak mungkin tercapai")
            return ke_atas(hpp / (1 - biaya - margin_min))
        if margin_min + biaya * (1 + self.tarif) >= 1:
            raise InputError(f"target margin {pct(margin_min)} + potongan {pct(biaya)} (dihitung dari harga termasuk PPN) "
                             "mencapai 100% atau lebih; tidak mungkin tercapai")

        def cukup(d):
            return d - biaya * (d + self.ppn_dari_dpp(d)) - hpp >= margin_min * d

        # PPN dibulatkan ke bawah: dpp x tarif - 1 < PPN <= dpp x tarif, sehingga DPP terkecil yang cukup
        # pasti ada di rentang [(HPP - biaya) / k, HPP / k] dengan k = 1 - margin - biaya x (1 + tarif).
        # Rentang itu discan dari bawah (fungsi laba bisa naik-turun sedikit karena pembulatan PPN).
        k = 1 - margin_min - biaya * (1 + self.tarif)
        d = max(ke_bawah((hpp - biaya) / k), SATU)
        while not cukup(d):
            d += 1
        return self.dari_dpp(d)

    def label(self):
        if self.mode == "termasuk":
            return "harga yang dimasukkan SUDAH termasuk PPN"
        if self.mode == "belum":
            return "harga yang dimasukkan = DPP (belum termasuk PPN)"
        return "bukan PKP (tanpa PPN)"


TANPA_PPN = Pajak()


def harga_minimum(hpp, margin_min, biaya=NOL, pajak=TANPA_PPN):
    """Harga terkecil (rupiah bulat, ke atas) agar margin >= margin_min setelah potongan biaya%."""
    return pajak.minimum(hpp, margin_min, biaya)


def _rincian_ppn(pajak, harga):
    """Teks 'DPP x | PPN y | harga tayang z [| sisa]' untuk satu harga."""
    dpp, tayang = pajak.pecah(harga)
    ppn = pajak.ppn_dari_dpp(dpp)
    teks = f"DPP {rp(dpp)} + PPN {rp(ppn)} = {rp(dpp + ppn)}"
    if pajak.mode == "termasuk" and tayang - dpp - ppn:
        teks += f" (sisa pembulatan {rp(tayang - dpp - ppn)})"
    return teks


CATATAN_PPN = ("Margin & laba dihitung dari DPP (PPN bukan pendapatan). Pembulatan PPN belum dicocokkan dengan "
               "Coretax; bila berbeda, ikuti Coretax. Hanya PKP yang boleh memungut PPN.")


# ---------------------------------------------------------------- 1. margin vs markup

def hitung_margin(hpp, harga=None, margin=None, markup=None, biaya=NOL, pajak=TANPA_PPN, margin_min=None):
    """Satu dari harga/margin/markup wajib diisi. Kembalikan dict lengkap."""
    hpp = D(hpp)
    _cek_biaya(biaya)
    diisi = [v is not None for v in (harga, margin, markup)]
    if sum(diisi) != 1:
        raise InputError("isi tepat satu: harga jual, target margin, atau target markup")
    if margin is not None:
        harga = pajak.minimum(hpp, margin, biaya)
        sumber = f"dari target margin {pct(margin)} (dibulatkan ke atas)"
    elif markup is not None:
        # markup = laba / HPP: cari harga terkecil dengan laba >= k x HPP (= "HPP x (1 + k)" dengan margin 0)
        harga = pajak.minimum(hpp * (1 + markup), NOL, biaya)
        sumber = f"dari target markup {pct(markup)} (dibulatkan ke atas)"
    else:
        harga = D(harga)
        sumber = "harga yang diberikan"
    dpp, tayang = pajak.pecah(harga)
    potongan = biaya * tayang
    laba = dpp - potongan - hpp
    h = {
        "hpp": hpp, "harga": harga, "sumber": sumber, "biaya": biaya, "pajak": pajak,
        "dpp": dpp, "tayang": tayang, "ppn": pajak.ppn_dari_dpp(dpp),
        "potongan": potongan, "laba": laba,
        "margin": laba / dpp, "markup": laba / hpp, "peringatan": [],
    }
    if laba <= 0:
        h["peringatan"].append(f"harga di bawah modal (HPP + potongan): setiap unit RUGI {rp(bulat(-laba))}")
    elif hpp * SERATUS < dpp:
        h["peringatan"].append("HPP kurang dari 1% harga jual; cek lagi penulisan angka (mis. 12.500 vs 12,5)")
    if margin_min is not None:
        h["margin_min"] = margin_min
        h["batas"] = pajak.minimum(hpp, margin_min, biaya)
        h["aman"] = h["margin"] >= margin_min
        if not h["aman"]:
            h["peringatan"].append(f"margin {pct(h['margin'])} DI BAWAH minimum {pct(margin_min)}; "
                                   f"harga terendah yang aman {rp(h['batas'])}")
    return h


def margin_ke_markup(m):
    if m >= 1:
        raise InputError("margin harus di bawah 100%")
    return m / (1 - m)


def markup_ke_margin(k):
    return k / (1 + k)


# ---------------------------------------------------------------- 2. BEP

def hitung_bep(biaya_tetap, harga, biaya_var, biaya=NOL, target_laba=NOL, hari_jual=None, volume=None,
               pajak=TANPA_PPN):
    _cek_biaya(biaya)
    if hari_jual is not None and int(hari_jual) <= 0:
        raise InputError(f"hari jual harus angka bulat lebih dari 0 (didapat {hari_jual})")
    harga, biaya_var = D(harga), D(biaya_var)
    dpp, tayang = pajak.pecah(harga)
    kontribusi = dpp - biaya * tayang - biaya_var
    if kontribusi <= 0:
        raise InputError(f"harga {rp(harga)} tidak menutup modal per unit + potongan; setiap penjualan rugi, BEP tidak ada")
    unit = ke_atas((D(biaya_tetap) + D(target_laba)) / kontribusi)
    hasil = {
        "kontribusi": kontribusi, "rasio_kontribusi": kontribusi / dpp,
        "unit": unit, "omzet": unit * harga, "omzet_dpp": unit * dpp, "pajak": pajak,
        "biaya_tetap": D(biaya_tetap), "target_laba": D(target_laba),
    }
    if hari_jual is not None:
        hasil["per_hari"] = ke_atas(unit / D(hari_jual))
        hasil["hari_jual"] = int(hari_jual)
    if volume is not None:
        v = D(volume)
        hasil["volume"] = v
        hasil["laba_sekarang"] = v * kontribusi - D(biaya_tetap)
        unit_bep = ke_atas(D(biaya_tetap) / kontribusi)
        hasil["unit_bep"] = unit_bep
        if v >= unit_bep and v > 0:
            hasil["batas_aman"] = (v - unit_bep) / v
        else:
            hasil["kurang"] = unit_bep - v
            hasil["kurang_persen"] = (unit_bep - v) / unit_bep if unit_bep > 0 else NOL
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


def hitung_tangga(harga_ecer, hpp, level, margin_min, biaya=NOL, kelipatan_rp=None, pajak=TANPA_PPN,
                  harga_anjuran=None, margin_reseller_min=MARGIN_RESELLER_BAWAAN, harga_promo=None):
    """Tangga harga. Untung reseller dihitung dari harga eceran anjuran (default = harga eceran toko)
    dikurangi harga beli reseller, keduanya harga tayang (yang benar-benar dibayar/diterima)."""
    _cek_biaya(biaya)
    harga_ecer, hpp = D(harga_ecer), D(hpp)
    anjuran = harga_ecer if harga_anjuran is None else D(harga_anjuran)
    batas = pajak.minimum(hpp, margin_min, biaya)
    diskon_maks = 1 - batas / harga_ecer
    _, tayang_anjuran = pajak.pecah(anjuran)
    baris, peringatan = [], []
    if anjuran > harga_ecer:
        peringatan.append(f"harga eceran anjuran reseller {rp(anjuran)} LEBIH MAHAL dari harga eceran toko {rp(harga_ecer)}; "
                          "pembeli akan beli langsung ke toko. Samakan anjuran dengan harga toko yang berlaku")
    elif anjuran < harga_ecer:
        peringatan.append(f"harga eceran anjuran reseller {rp(anjuran)} lebih murah dari harga eceran toko {rp(harga_ecer)}; "
                          "reseller akan 'membanting' harga toko. Samakan anjuran dengan harga toko yang berlaku")
    for lv in sorted(level, key=lambda x: x["min"]):
        if "harga_langsung" in lv:
            h = lv["harga_langsung"]
        else:
            h = bulat(harga_ecer * (1 - lv["diskon"]))
        if kelipatan_rp:
            h = kelipatan(h, kelipatan_rp)
        _cek_positif(h, f"harga level {lv['nama']}")
        dpp, tayang = pajak.pecah(h)
        laba = dpp - biaya * tayang - hpp
        b = {"nama": lv["nama"], "min": lv["min"], "harga": h, "dpp": dpp, "tayang": tayang,
             "diskon": 1 - h / harga_ecer, "laba": laba, "margin": laba / dpp,
             "laba_min_beli": laba * lv["min"]}
        b["aman"] = b["margin"] >= margin_min
        if not b["aman"]:
            peringatan.append(f"{lv['nama']}: margin {pct(b['margin'])} di bawah minimum {pct(margin_min)}; harga terendah yang aman {rp(batas)}")
        if h > harga_ecer:
            peringatan.append(f"{lv['nama']}: harga {rp(h)} lebih mahal dari harga eceran {rp(harga_ecer)}")
        # level penjual ulang = semua level selain eceran toko sendiri (min beli 1 di harga eceran)
        b["reseller"] = not (lv["min"] == 1 and h == harga_ecer)
        if b["reseller"]:
            b["untung_reseller"] = tayang_anjuran - tayang
            b["margin_reseller"] = b["untung_reseller"] / tayang_anjuran
            if b["untung_reseller"] <= 0:
                peringatan.append(f"{lv['nama']}: harga beli {rp(h)} tidak lebih murah dari harga eceran anjuran "
                                  f"{rp(anjuran)}; reseller TIDAK UNTUNG")
            elif b["margin_reseller"] < margin_reseller_min:
                peringatan.append(f"{lv['nama']}: untung reseller hanya {rp(b['untung_reseller'])}/unit "
                                  f"({pct(b['margin_reseller'])}), di bawah {pct(margin_reseller_min)}; reseller kurang tertarik")
        baris.append(b)
    for hp in (harga_promo or []):
        hp = D(hp)
        for b in baris:
            if b["reseller"] and b["harga"] >= hp:
                peringatan.append(_pesan_konflik(hp, b["nama"], b["harga"]))
    for a, b in zip(baris, baris[1:]):
        if b["harga"] > a["harga"]:
            peringatan.append(f"{b['nama']} (beli banyak) lebih mahal dari {a['nama']}; tangga harga terbalik")
    if diskon_maks < 0:
        peringatan.insert(0, f"harga eceran {rp(harga_ecer)} sendiri sudah di bawah margin minimum; naikkan harga eceran atau tekan HPP")
    return {"batas": batas, "diskon_maks": diskon_maks, "baris": baris, "peringatan": peringatan,
            "harga_ecer": harga_ecer, "anjuran": anjuran, "hpp": hpp, "margin_min": margin_min, "biaya": biaya,
            "pajak": pajak, "margin_reseller_min": margin_reseller_min}


# ---------------------------------------------------------------- 4. dampak diskon

def _pesan_konflik(harga_promo, nama, harga_beli):
    sama = "SAMA DENGAN" if harga_promo == harga_beli else "LEBIH MURAH dari"
    return (f"KONFLIK KANAL - harga promo konsumen {rp(harga_promo)} {sama} harga beli {nama} {rp(harga_beli)}; "
            f"{nama} akan merasa dirugikan (konsumen bisa beli semurah/lebih murah dari dia) dan bisa memborong stok promo. "
            f"Pilihan: kecilkan diskon agar harga promo di atas {rp(harga_beli)}, batasi kuota/maks beli per pembeli, "
            f"atau beri {nama} harga khusus/kompensasi selama promo")


def parse_harga_reseller(teks):
    """'Agen:26250' atau '26250' (nama default 'reseller')."""
    t = str(teks).strip()
    if ":" in t:
        nama, nilai = t.rsplit(":", 1)
        nama = nama.strip() or "reseller"
    else:
        nama, nilai = "reseller", t
    return nama, parse_rupiah(nilai, nama=f"harga {nama}")


def parse_bxgy(teks):
    m = re.match(r"^\s*(\d+)\s*[:+/x]\s*(\d+)\s*$", str(teks))
    if not m or int(m.group(1)) < 1 or int(m.group(2)) < 1:
        raise InputError(f"'{teks}' harus berformat beli:gratis, mis. 2:1 untuk 'beli 2 gratis 1'")
    return int(m.group(1)), int(m.group(2))


def hitung_diskon(harga, hpp, diskon=None, potongan=None, bxgy=None, volume=None, biaya=NOL, margin_min=None,
                  pajak=TANPA_PPN, harga_reseller=None, kanal=None):
    _cek_biaya(biaya)
    harga, hpp = D(harga), D(hpp)
    if sum(v is not None for v in (diskon, potongan, bxgy)) != 1:
        raise InputError("isi tepat satu jenis promo: diskon %, potongan rupiah, atau beli-X-gratis-Y")
    dpp, tayang = pajak.pecah(harga)
    if diskon is not None:
        if diskon >= 1:
            raise InputError("diskon harus di bawah 100%")
        harga_promo = bulat(harga * (1 - diskon))
        _cek_positif(harga_promo, "harga promo")
        dpp_promo, tayang_promo = pajak.pecah(harga_promo)
        label = f"diskon {pct(diskon)}"
    elif potongan is not None:
        if potongan >= harga:
            raise InputError("potongan harga tidak boleh sama atau melebihi harga jual")
        harga_promo = harga - D(potongan)
        dpp_promo, tayang_promo = pajak.pecah(harga_promo)
        label = f"potongan {rp(potongan)}"
    else:
        x, y = bxgy
        faktor_b = D(x) / D(x + y)
        harga_promo = harga * faktor_b   # harga efektif per unit, TIDAK dibulatkan
        dpp_promo, tayang_promo = dpp * faktor_b, tayang * faktor_b
        label = f"beli {x} gratis {y}"
    laba_normal = dpp - biaya * tayang - hpp
    if laba_normal <= 0:
        raise InputError(f"di harga normal {rp(harga)} saja sudah tidak untung (HPP + potongan >= harga); perbaiki harga dulu")
    laba_promo = dpp_promo - biaya * tayang_promo - hpp
    h = {"label": label, "harga": harga, "harga_promo": harga_promo, "diskon_efektif": 1 - harga_promo / harga,
         "dpp": dpp, "dpp_promo": dpp_promo, "pajak": pajak, "bxgy": bxgy is not None,
         "laba_normal": laba_normal, "laba_promo": laba_promo,
         "margin_normal": laba_normal / dpp, "margin_promo": laba_promo / dpp_promo,
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
        batas = pajak.minimum(hpp, margin_min, biaya)
        h["batas"] = batas
        h["margin_min"] = margin_min
        h["diskon_maks"] = 1 - batas / harga
        h["promo_aman"] = h["margin_promo"] >= margin_min
    h["konflik"] = []
    for nama, hb in (harga_reseller or []):
        if harga_promo <= D(hb):
            h["konflik"].append(_pesan_konflik(bulat(harga_promo), nama, D(hb)))
    h["kanal"] = kanal
    h["biaya"] = biaya
    # v1.0.7: promo marketplace - pembanding kedua = laba normal jual langsung (tanpa potongan)
    if kanal == "marketplace" and biaya > 0 and not h["rugi"]:
        laba_langsung = dpp - hpp
        h["laba_langsung"] = laba_langsung
        h["langsung_faktor"] = laba_langsung / laba_promo
        if volume is not None:
            h["langsung_volume"] = ke_atas(D(volume) * h["langsung_faktor"])
    return h


def _harga_diskon(harga, persen):
    """Harga promo (rupiah terdekat) untuk diskon persen (Decimal pecahan, mis. 0,14)."""
    return bulat(harga * (1 - persen))


def _lolos_batas(harga, hpp, persen, biaya, margin_min, pajak, harga_reseller):
    """True bila diskon `persen` tidak menembus margin minimum, tidak rugi, dan promo DI ATAS semua harga beli reseller."""
    hp = _harga_diskon(harga, persen)
    if hp <= 0:
        return False
    dpp_p, tayang_p = pajak.pecah(hp)
    laba = dpp_p - biaya * tayang_p - hpp
    if laba <= 0:
        return False
    if margin_min is not None and laba / dpp_p < margin_min:
        return False
    return all(hp > D(hb) for _, hb in (harga_reseller or []))


def hitung_batas_diskon(harga, hpp, biaya=NOL, margin_min=None, pajak=TANPA_PPN, harga_reseller=None):
    """DISKON MAKSIMAL per batas bawah (margin minimum, harga beli tiap reseller/agen, atau impas bila tidak ada
    keduanya) + diskon bulat (persen utuh) terbesar yang memenuhi SEMUA batas sekaligus beserta harga promonya."""
    harga, hpp = D(harga), D(hpp)
    batas = []
    if margin_min is not None:
        b = pajak.minimum(hpp, margin_min, biaya)
        batas.append({"nama": f"margin minimum {pct(margin_min)}", "harga_batas": b, "boleh_sama": True})
    for nama, hb in (harga_reseller or []):
        batas.append({"nama": f"harga beli {nama}", "harga_batas": D(hb), "boleh_sama": False})
    if not batas:
        b = pajak.minimum(hpp, NOL, biaya)
        batas.append({"nama": "impas (laba Rp0, belum ada margin minimum)", "harga_batas": b, "boleh_sama": True})
    for x in batas:
        x["diskon_maks"] = max(1 - x["harga_batas"] / harga, NOL)
    # diskon persen utuh terbesar yang lolos semua batas (dicek ulang dengan hitungan penuh, termasuk PPN & potongan)
    p = int((min(x["diskon_maks"] for x in batas) * SERATUS).to_integral_value(rounding=ROUND_FLOOR))
    p = min(max(p, 0), 99)
    while p > 0 and not _lolos_batas(harga, hpp, D(p) / SERATUS, biaya, margin_min, pajak, harga_reseller):
        p -= 1
    bulat_maks = D(p) / SERATUS
    return {"harga": harga, "batas": batas, "bulat_maks": bulat_maks, "tanpa_mm": margin_min is None,
            "harga_bulat_maks": _harga_diskon(harga, bulat_maks)}


def cetak_batas_diskon(b):
    out = ["DISKON MAKSIMAL (salin angka dari sini; jangan menghitung persen/harga promo sendiri):"]
    for x in b["batas"]:
        if x["diskon_maks"] <= 0:
            out.append(f"- {x['nama']} {rp(x['harga_batas'])}: harga normal {rp(b['harga'])} sudah di/bawah batas ini -> "
                       f"TIDAK ADA ruang diskon")
        elif x["boleh_sama"]:
            out.append(f"- {x['nama']}: harga promo terendah {rp(x['harga_batas'])} -> DISKON MAKSIMAL {pct(x['diskon_maks'])}")
        else:
            out.append(f"- {x['nama']} {rp(x['harga_batas'])}: harga promo harus DI ATAS angka ini -> diskon harus KURANG DARI "
                       f"{pct(x['diskon_maks'])} (tepat {pct(x['diskon_maks'])} = harga promo sama dengan harga beli = bentrok kanal)")
    if b["tanpa_mm"]:
        out.append("PERHATIAN: margin minimum belum diisi, jadi lantai margin BELUM dicek; ulangi dengan --margin-min atau --kategori")
    if b["bulat_maks"] > 0:
        out.append(f"DISKON MAKSIMAL (persen bulat, memenuhi semua batas di atas): {pct(b['bulat_maks'])} -> "
                   f"harga promo {rp(b['harga_bulat_maks'])}")
    else:
        out.append("DISKON MAKSIMAL (persen bulat, memenuhi semua batas di atas): 0% -> promo diskon TIDAK DISARANKAN; "
                   "pakai bonus/paket atau kuota terbatas")
    return "\n".join(out)


def parse_rentang(teks):
    """'15-17' atau '10-30:5' (langkah) -> list persen Decimal pecahan."""
    m = re.match(r"^\s*(\d+(?:,\d+)?)\s*-\s*(\d+(?:,\d+)?)\s*(?::\s*(\d+(?:,\d+)?))?\s*$", str(teks))
    if not m:
        raise InputError(f"rentang '{teks}' harus berformat awal-akhir atau awal-akhir:langkah, mis. 15-17 atau 10-30:5")
    a, z = D(m.group(1).replace(",", ".")), D(m.group(2).replace(",", "."))
    langkah = D(m.group(3).replace(",", ".")) if m.group(3) else SATU
    if a > z:
        a, z = z, a
    if langkah <= 0 or z >= SERATUS or (z - a) / langkah > 50:
        raise InputError("rentang diskon harus di bawah 100%, langkah > 0, dan maksimal 51 baris")
    hasil, x = [], a
    while x <= z:
        hasil.append(x / SERATUS)
        x += langkah
    return hasil


def hitung_rentang(harga, hpp, daftar, volume=None, biaya=NOL, margin_min=None, pajak=TANPA_PPN, harga_reseller=None):
    baris = []
    for d in daftar:
        h = hitung_diskon(harga, hpp, diskon=d, volume=volume, biaya=biaya, margin_min=margin_min, pajak=pajak,
                          harga_reseller=harga_reseller) if d > 0 else None
        if h is None:
            continue
        status = []
        if h["rugi"]:
            status.append("RUGI")
        elif margin_min is not None and not h["promo_aman"]:
            status.append("DI BAWAH MIN")
        for nama, hb in (harga_reseller or []):
            if h["harga_promo"] <= D(hb):
                status.append(f"KONFLIK {nama}")
        baris.append([pct(d), rp(h["harga_promo"]), rp(bulat(h["laba_promo"])), pct(h["margin_promo"]),
                      "-" if h["rugi"] or "volume_perlu" not in h else angka(h["volume_perlu"]),
                      ", ".join(status) or "OK"])
    return baris


def cetak_rentang(baris, ada_volume):
    kepala = ["Diskon", "Harga promo", "Laba/unit", "Margin", "Volume perlu" if ada_volume else "Volume perlu (isi --volume)", "Status"]
    return "TABEL RENTANG DISKON (salin baris dari sini):\n" + tabel(kepala, baris)


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


def hitung_bundel(item, harga_bundel, biaya_tambahan=NOL, biaya=NOL, margin_min=None, pajak=TANPA_PPN):
    _cek_biaya(biaya)
    if not item:
        raise InputError("isi minimal 2 item untuk paket")
    harga_bundel = D(harga_bundel)
    total = sum(i["harga"] * i["qty"] for i in item)
    hpp_isi = sum(i["hpp"] * i["qty"] for i in item)
    hpp_bundel = hpp_isi + D(biaya_tambahan)
    dpp_satuan, tayang_satuan = NOL, NOL
    for i in item:
        d, t = pajak.pecah(i["harga"])
        dpp_satuan += d * i["qty"]
        tayang_satuan += t * i["qty"]
    dpp_b, tayang_b = pajak.pecah(harga_bundel)
    laba_bundel = dpp_b - biaya * tayang_b - hpp_bundel
    laba_terpisah = dpp_satuan - biaya * tayang_satuan - hpp_isi
    h = {"total_normal": total, "hpp_isi": hpp_isi, "hpp_bundel": hpp_bundel, "harga_bundel": harga_bundel,
         "dpp_bundel": dpp_b, "dpp_satuan": dpp_satuan, "pajak": pajak,
         "hemat": total - harga_bundel, "hemat_persen": (total - harga_bundel) / total,
         "laba_bundel": laba_bundel, "margin_bundel": laba_bundel / dpp_b,
         "laba_terpisah": laba_terpisah, "margin_terpisah": laba_terpisah / dpp_satuan,
         "peringatan": []}
    if harga_bundel >= total:
        h["peringatan"].append("harga paket tidak lebih murah dari beli satuan; pembeli tidak punya alasan pilih paket")
    if laba_bundel <= 0:
        h["peringatan"].append("paket ini RUGI per paket")
    elif laba_terpisah > 0:
        h["faktor"] = laba_terpisah / laba_bundel
    if margin_min is not None:
        h["batas"] = pajak.minimum(hpp_bundel, margin_min, biaya)
        h["margin_min"] = margin_min
        h["aman"] = h["margin_bundel"] >= margin_min
        if not h["aman"]:
            h["peringatan"].append(f"margin paket {pct(h['margin_bundel'])} DI BAWAH minimum {pct(margin_min)}; harga paket terendah yang aman {rp(h['batas'])}")
    return h


# ---------------------------------------------------------------- 6. elastisitas (ESTIMASI)

ELASTISITAS_BAWAAN = [D("-0.5"), D("-1"), D("-2")]


def hitung_elastisitas(harga, volume, hpp, perubahan=None, elastisitas=None, biaya=NOL, biaya_tetap=NOL,
                       harga_baru=None, pajak=TANPA_PPN):
    """Perkiraan garis lurus: volume baru = volume x (1 + e x perubahan harga).

    Skenario bisa berupa persen perubahan (harga baru dibulatkan ke rupiah terdekat)
    dan/atau harga baru langsung (persen dihitung persis dari harga itu)."""
    _cek_biaya(biaya)
    harga, volume, hpp = D(harga), D(volume), D(hpp)
    for dp in (perubahan or []):
        if dp <= -1:
            raise InputError("penurunan harga harus kurang dari 100%")
    daftar = [(dp, bulat(harga * (1 + dp))) for dp in (perubahan or [])]
    daftar += [(D(hb) / harga - 1, D(hb)) for hb in (harga_baru or [])]
    if not daftar:
        raise InputError("isi minimal satu skenario: perubahan harga % atau harga baru")
    el = elastisitas or ELASTISITAS_BAWAAN
    laba_unit = pajak.laba(harga, hpp, biaya)
    dasar = volume * laba_unit - D(biaya_tetap)
    skenario = []
    for dp, hb in daftar:
        _cek_positif(hb, "harga baru")
        lu = pajak.laba(hb, hpp, biaya)
        s = {"perubahan": dp, "harga_baru": hb, "laba_unit": lu, "hasil": []}
        if lu > 0 and laba_unit > 0:
            s["volume_impas"] = ke_atas(volume * laba_unit / lu)
            if dp != 0:
                s["elastisitas_impas"] = (laba_unit / lu - 1) / dp
        for e in el:
            vb = volume * (1 + e * dp)
            if vb < 0:
                vb = NOL
            vb = bulat(vb)
            laba = vb * lu - D(biaya_tetap)
            s["hasil"].append({"e": e, "volume": vb, "omzet": vb * hb, "laba": laba, "selisih": laba - dasar})
        skenario.append(s)
    return {"dasar": dasar, "laba_unit": laba_unit, "skenario": skenario, "pajak": pajak,
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


def hitung_cantik(harga, hpp=None, margin_min=None, biaya=NOL, harga_min=None, pajak=TANPA_PPN):
    _cek_biaya(biaya)
    batas = None
    if hpp is not None and margin_min is not None:
        batas = pajak.minimum(hpp, margin_min, biaya)
    if harga_min is not None:
        batas = max(batas or NOL, D(harga_min))
    baris = []
    for nilai, pola in kandidat_cantik(harga):
        b = {"harga": nilai, "pola": pola, "selisih": nilai - D(harga)}
        dpp, _ = pajak.pecah(nilai)
        b["dpp"] = dpp
        if hpp is not None:
            b["laba"] = pajak.laba(nilai, hpp, biaya)
            b["margin"] = b["laba"] / dpp
        b["aman"] = None if batas is None else nilai >= batas
        baris.append(b)
    return {"harga": D(harga), "batas": batas, "baris": baris, "pajak": pajak}


# ---------------------------------------------------------------- keluaran teks

def tabel(kepala, baris):
    lebar = [max(len(str(x)) for x in kol) for kol in zip(kepala, *baris)]
    garis = lambda r: "| " + " | ".join(str(x).ljust(w) for x, w in zip(r, lebar)) + " |"
    return "\n".join([garis(kepala), "|" + "|".join("-" * (w + 2) for w in lebar) + "|"] + [garis(r) for r in baris])


def _kepala_ppn(pajak):
    if not pajak.aktif:
        return []
    tarif = "12% penuh (barang mewah)" if pajak.mewah else "12% x DPP nilai lain 11/12 = 11% efektif"
    return [f"Mode PPN: {pajak.label()}; tarif {tarif}. Margin = laba / DPP."]


def _ekor_ppn(pajak):
    return [CATATAN_PPN] if pajak.aktif else []


def cetak_margin(h):
    pajak = h["pajak"]
    out = _kepala_ppn(pajak)
    out += [f"HPP/modal per unit : {rp(h['hpp'])}"]
    if pajak.aktif:
        judul = "Harga tayang (termasuk PPN)" if pajak.mode == "termasuk" else "Harga sebelum PPN (DPP)"
        out.append(f"{judul}: {rp(h['harga'])}  ({h['sumber']})")
        out.append(f"Rincian            : {_rincian_ppn(pajak, h['harga'])}")
        if pajak.mode == "belum":
            out.append(f"Harga tayang termasuk PPN: {rp(h['tayang'])}")
    else:
        out.append(f"Harga jual         : {rp(h['harga'])}  ({h['sumber']})")
    if h["biaya"]:
        out.append(f"{'Potongan ' + pct(h['biaya']):<19}: {rp(bulat(h['potongan']))}")
    dasar = "DPP" if pajak.aktif else "harga"
    out += [f"Laba kotor/unit    : {rp(bulat(h['laba']))}",
            f"Margin (laba/{dasar}): {pct(h['margin'])}",
            f"Markup (laba/HPP)  : {pct(h['markup'])}"]
    if "margin_min" in h:
        out.append(f"Status vs margin minimum {pct(h['margin_min'])}: {'OK' if h['aman'] else 'DI BAWAH MIN'} "
                   f"(harga terendah yang aman {rp(h['batas'])})")
    out += ["PERHATIAN: " + p for p in h["peringatan"]]
    out.append("Catatan: margin dihitung dari HARGA JUAL" + (" (DPP)" if pajak.aktif else "") +
               ", markup dari HPP. Markup 50% = margin 33,33%, bukan 50%.")
    out += _ekor_ppn(pajak)
    return "\n".join(out)


def cetak_bep(h):
    out = _kepala_ppn(h["pajak"])
    out += [f"Laba kontribusi per unit : {rp(bulat(h['kontribusi']))} ({pct(h['rasio_kontribusi'])} dari "
            f"{'DPP' if h['pajak'].aktif else 'harga'})",
            f"Biaya tetap per bulan    : {rp(h['biaya_tetap'])}"]
    if h["target_laba"]:
        out.append(f"Target laba bersih       : {rp(h['target_laba'])}")
    judul = "Unit harus terjual/bulan" if h["target_laba"] else "BEP (titik impas)       "
    out += [f"{judul} : {angka(h['unit'])} unit (dibulatkan ke atas)",
            f"Omzet setara             : {rp(h['omzet'])}"]
    if h["pajak"].aktif:
        out.append(f"Omzet setara (DPP)       : {rp(h['omzet_dpp'])}")
    if "per_hari" in h:
        out.append(f"Per hari ({h['hari_jual']} hari jual)  : {angka(h['per_hari'])} unit")
    if "volume" in h:
        out.append(f"Penjualan sekarang       : {angka(h['volume'])} unit -> laba/rugi {rp(bulat(h['laba_sekarang']))}/bulan")
        if "batas_aman" in h:
            out.append(f"Batas aman (margin of safety): {pct(h['batas_aman'])} penjualan boleh turun sebelum rugi")
        else:
            out.append(f"PERHATIAN: penjualan masih kurang {angka(h['kurang'])} unit ({pct(h['kurang_persen'])}) "
                       f"dari titik impas {angka(h['unit_bep'])} unit; usaha masih rugi")
    out += _ekor_ppn(h["pajak"])
    return "\n".join(out)


def cetak_tangga(h):
    pajak = h["pajak"]
    rows = []
    for b in h["baris"]:
        r = [b["nama"], f">= {b['min']}", rp(b["harga"])]
        if pajak.aktif:
            r.append(rp(b["dpp"]))
        r += [pct(b["diskon"]), rp(bulat(b["laba"])), pct(b["margin"]), rp(bulat(b["laba_min_beli"]))]
        r.append(f"{rp(b['untung_reseller'])} ({pct(b['margin_reseller'])})" if b["reseller"] else "-")
        r.append("OK" if b["aman"] else "DI BAWAH MIN")
        rows.append(r)
    kepala = ["Level", "Min beli", "Harga/unit"] + (["DPP"] if pajak.aktif else [])
    kepala += ["Diskon", "Laba kita/unit", "Margin", "Laba di min beli", "Untung reseller/unit", "Status"]
    out = _kepala_ppn(pajak)
    out += [tabel(kepala, rows),
            "",
            f"Harga eceran toko {rp(h['harga_ecer'])}; harga eceran anjuran untuk reseller {rp(h['anjuran'])} "
            "(untung reseller = anjuran - harga beli reseller). Bila harga toko naik, naikkan anjuran bersamaan.",
            f"Margin minimum {pct(h['margin_min'])} -> harga terendah yang aman {rp(h['batas'])} "
            f"(diskon maksimal {pct(max(h['diskon_maks'], NOL))} dari eceran)"]
    out += ["PERHATIAN: " + p for p in h["peringatan"]]
    out += _ekor_ppn(pajak)
    return "\n".join(out)


def cetak_diskon(h):
    pajak = h["pajak"]
    dasar = "DPP" if pajak.aktif else "harga"
    ket_promo = " (harga efektif per unit)" if h["bxgy"] else ""
    out = _kepala_ppn(pajak)
    out += [f"Promo              : {h['label']} (diskon efektif {pct(h['diskon_efektif'])})",
            f"Harga normal       : {rp(h['harga'])} -> laba {rp(bulat(h['laba_normal']))}/unit (margin {pct(h['margin_normal'])} dari {dasar})",
            f"Harga saat promo   : {rp(h['harga_promo'])}{ket_promo} -> laba {rp(bulat(h['laba_promo']))}/unit (margin {pct(h['margin_promo'])})"]
    if h["rugi"]:
        out.append("PERHATIAN: promo ini RUGI per unit. Menambah penjualan justru menambah rugi. Kecilkan promo.")
    else:
        out.append(f"Agar laba kotor TETAP sama, penjualan harus naik {pct(h['tambahan'])} (x{str(h['faktor'].quantize(D('0.01'), ROUND_HALF_UP)).replace('.', ',')})")
        if "volume" in h:
            out.append(f"Dari {angka(h['volume'])} unit -> minimal {angka(h['volume_perlu'])} unit (laba kotor normal {rp(bulat(h['laba_kotor_normal']))})")
    if "batas" in h:
        if not h["promo_aman"] and not h["rugi"]:
            out.append(f"PERHATIAN: margin saat promo {pct(h['margin_promo'])} DI BAWAH minimum {pct(h['margin_min'])}")
    out += ["PERHATIAN: " + p for p in h.get("konflik", [])]
    if h.get("kanal") == "marketplace":
        if h["biaya"] == 0:
            out.append("PERHATIAN: promo di marketplace tetapi potongan marketplace 0%; event (flash sale/11.11/12.12/Harbolnas) "
                       "hampir selalu kena admin + biaya layanan/program. Isi --biaya-persen (rincian dari harga-jual-marketplace) "
                       "atau tulis asumsi potongan yang dipakai")
        else:
            out.append(f"Potongan marketplace dihitung {pct(h['biaya'])} dari harga jual (tulis di Asumsi; cek ulang di harga-jual-marketplace)")
    elif h.get("biaya") == 0 and h.get("kanal") is None:
        out.append("Catatan: potongan kanal dihitung 0% (jual langsung). Bila promo ini di marketplace, ulangi dengan --biaya-persen")
    out += _ekor_ppn(pajak)
    return "\n".join(out)


def cetak_bundel(h):
    pajak = h["pajak"]
    out = _kepala_ppn(pajak)
    out += [f"Total beli satuan   : {rp(h['total_normal'])}",
            f"Harga paket         : {rp(h['harga_bundel'])} -> pembeli hemat {rp(h['hemat'])} ({pct(h['hemat_persen'])})"]
    if pajak.aktif:
        out.append(f"Rincian paket       : {_rincian_ppn(pajak, h['harga_bundel'])}")
    dasar = " dari DPP" if pajak.aktif else ""
    out += [f"HPP paket           : {rp(h['hpp_bundel'])} (isi {rp(h['hpp_isi'])} + kemasan/tambahan {rp(h['hpp_bundel'] - h['hpp_isi'])})",
            f"Laba per paket      : {rp(bulat(h['laba_bundel']))} (margin {pct(h['margin_bundel'])}{dasar})",
            f"Kalau dijual satuan : laba {rp(bulat(h['laba_terpisah']))} (margin {pct(h['margin_terpisah'])}{dasar})"]
    if "faktor" in h:
        out.append(f"Paket harus menambah transaksi {pct(h['faktor'] - 1)} agar laba kotor sama dengan jual satuan "
                   "(kalau paket menarik pembeli baru / isi yang tadinya tak dibeli, ini mudah tercapai)")
    if "batas" in h:
        out.append(f"Status vs margin minimum {pct(h['margin_min'])}: {'OK' if h['aman'] else 'DI BAWAH MIN'}")
        out.append(f"Harga paket terendah untuk margin {pct(h['margin_min'])}: {rp(h['batas'])}")
    out += ["PERHATIAN: " + p for p in h["peringatan"]]
    out += _ekor_ppn(pajak)
    return "\n".join(out)


def cetak_elastisitas(h):
    out = _kepala_ppn(h["pajak"])
    out += ["ESTIMASI - bukan kepastian. Elastisitas = seberapa peka pembeli pada harga "
            "(-0,5 tidak peka, -1 sedang, -2 sangat peka). Model garis lurus, wajar untuk perubahan kecil.",
            f"Laba saat ini: {rp(bulat(h['dasar']))} (laba/unit {rp(bulat(h['laba_unit']))})", ""]
    for s in h["skenario"]:
        arah = "naik" if s["perubahan"] > 0 else ("turun" if s["perubahan"] < 0 else "tetap")
        out.append(f"Harga {arah} {pct(abs(s['perubahan']))} -> {rp(s['harga_baru'])} (laba/unit {rp(bulat(s['laba_unit']))})")
        if "volume_impas" in s:
            teks = f"  Volume impas (PASTI, bukan estimasi): {angka(s['volume_impas'])} unit agar laba sama"
            if "elastisitas_impas" in s:
                teks += f"; elastisitas impas {str(s['elastisitas_impas'].quantize(D('0.01'), ROUND_HALF_UP)).replace('.', ',')}"
            out.append(teks)
        elif s["laba_unit"] <= 0:
            out.append("  PERHATIAN: di harga ini setiap unit rugi")
        else:
            out.append("  PERHATIAN: di harga lama setiap unit rugi; volume impas tidak berlaku")
        rows = [[str(r["e"]).replace(".", ","), angka(r["volume"]), rp(r["omzet"]), rp(bulat(r["laba"])),
                 ("+" if r["selisih"] > 0 else "") + rp(bulat(r["selisih"]))] for r in s["hasil"]]
        out.append(tabel(["Elastisitas", "Volume (est.)", "Omzet (est.)", "Laba (est.)", "Selisih"], rows))
        out.append("")
    if h["peringatan_besar"]:
        out.append("PERHATIAN: ada perubahan > 20%; perkiraan garis lurus makin tidak akurat. Uji kecil dulu.")
    out += _ekor_ppn(h["pajak"])
    return "\n".join(out).rstrip()


def cetak_cantik(h):
    pajak = h["pajak"]
    rows = []
    for b in h["baris"]:
        r = [rp(b["harga"]), b["pola"], ("+" if b["selisih"] > 0 else "") + rp(b["selisih"])]
        if pajak.aktif:
            r.append(rp(b["dpp"]))
        if "margin" in b:
            r += [rp(bulat(b["laba"])), pct(b["margin"])]
        if b["aman"] is not None:
            r.append("OK" if b["aman"] else "DI BAWAH MIN")
        rows.append(r)
    kepala = ["Kandidat", "Pola", "Selisih"] + (["DPP"] if pajak.aktif else [])
    if h["baris"] and "margin" in h["baris"][0]:
        kepala += ["Laba/unit", "Margin"]
    if h["batas"] is not None:
        kepala.append("Status")
    out = _kepala_ppn(pajak)
    out += [f"Harga hitungan: {rp(h['harga'])}", tabel(kepala, rows)]
    if h["batas"] is not None:
        out.append(f"Batas harga terendah: {rp(h['batas'])} (kandidat DI BAWAH MIN jangan dipakai)")
    out += _ekor_ppn(pajak)
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


# ---------------------------------------------------------------- RINGKASAN SIAP TEMPEL (v1.0.7)
# Uji OpenClaw 1.0.6: model menulis "DISKON MAKSIMAL 9% -> Rp185.185 (masih di atas margin 40%)" sendiri padahal
# script mencetak 34,07% DI BAWAH MIN / TIDAK ADA ruang diskon. Kini setiap perintah hitungan mencetak kalimat
# siap kirim berisi SEMUA angka kunci + penilaiannya; agent wajib menyalinnya apa adanya.

JUDUL_RINGKASAN = ("=== RINGKASAN SIAP TEMPEL (salin kalimat ini apa adanya; JANGAN menulis angka harga/diskon/margin "
                   "yang tidak tercetak script - butuh angka lain? jalankan script lagi. Tabel di blok ini disalin UTUH; "
                   "baris/sel yang tidak ada = jalankan script lagi; DILARANG '~', 'kira-kira', 'hitung jika perlu', "
                   "atau baris ringkas seperti '15%+') ===")
AKHIR_RINGKASAN = "=== AKHIR RINGKASAN ==="


def blok_ringkasan(kalimat):
    # baris yang diawali "|" (tabel) atau berisi baris baru dicetak apa adanya
    return "\n".join([JUDUL_RINGKASAN] + [k if k.startswith("|") or "\n" in k else f"- {k}" for k in kalimat]
                     + [AKHIR_RINGKASAN])


def tabel_harga_promo(daftar_harga, hpp, persen, biaya, mm, pajak):
    """v1.0.9: untuk tiap harga normal, harga promo (diskon `persen`) + laba & margin promo + status - siap salin utuh."""
    rows = []
    for hn in daftar_harga:
        hn = D(hn)
        dpp, tayang = pajak.pecah(hn)
        laba_n = dpp - biaya * tayang - hpp
        if laba_n <= 0:
            rows.append([rp(hn), "RUGI", "-", "-", "-", "RUGI"])
            continue
        h = hitung_diskon(hn, hpp, diskon=persen, biaya=biaya, margin_min=mm, pajak=pajak)
        if h["rugi"]:
            status = "RUGI"
        elif mm is None:
            status = "margin min belum diisi"
        else:
            status = "OK" if h["promo_aman"] else "DI BAWAH MIN"
        rows.append([rp(hn), pct(h["margin_normal"]), rp(h["harga_promo"]), rp(bulat(h["laba_promo"])),
                     pct(h["margin_promo"]), status])
    kepala = ["Harga normal", "Margin normal", f"Harga promo (diskon {pct(persen)})", "Laba promo/unit",
              "Margin promo", "Status promo"]
    return tabel(kepala, rows)


def _kalimat_ruang_diskon(harga, hpp, biaya, mm, pajak, harga_reseller=None):
    """Kalimat DISKON MAKSIMAL dari harga `harga` (dihitung lewat hitung_batas_diskon, bukan kira-kira)."""
    b = hitung_batas_diskon(harga, hpp, biaya, mm, pajak, harga_reseller)
    syarat = "margin minimum " + pct(mm) if mm is not None else "impas (margin minimum belum diisi)"
    if harga_reseller:
        syarat += " dan harga beli " + ", ".join(n for n, _ in harga_reseller)
    if b["bulat_maks"] > 0:
        return (f"Dari harga {rp(D(harga))}: DISKON MAKSIMAL {pct(b['bulat_maks'])} -> harga promo "
                f"{rp(b['harga_bulat_maks'])} (batas: {syarat}); diskon lebih besar dari ini TIDAK DISARANKAN.")
    return (f"Dari harga {rp(D(harga))}: TIDAK ADA ruang diskon (DISKON MAKSIMAL 0%; diskon berapa pun menembus "
            f"batas {syarat}) -> promo diskon TIDAK DISARANKAN; pakai bonus/paket/kuota terbatas, bukan potongan harga.")


def _harga_normal_untuk_diskon(hpp, mm, biaya, pajak, persen, batas):
    """Harga normal (rupiah bulat) terkecil yang masih punya ruang diskon `persen` tanpa menembus margin minimum."""
    h = ke_atas(D(batas) / (1 - persen))
    while not _lolos_batas(h, hpp, persen, biaya, mm, pajak, None):
        h += 1
    while h > batas and _lolos_batas(h - 1, hpp, persen, biaya, mm, pajak, None):
        h -= 1
    return h


def _contoh_harga_aman(hpp, mm, biaya, pajak, batas, jumlah=4):
    """Harga cantik >= lantai (dari kandidat_cantik di sekitar lantai), maks `jumlah`."""
    c = hitung_cantik(batas, hpp, mm, biaya, None, pajak)
    return [b["harga"] for b in c["baris"] if b["aman"]][:jumlah]


def ringkasan_margin(h):
    pajak = h["pajak"]
    k = []
    ket = ""
    if pajak.aktif:
        ket = (f" (termasuk PPN; DPP {rp(h['dpp'])})" if pajak.mode == "termasuk"
               else f" (sebelum PPN; harga tayang termasuk PPN {rp(h['tayang'])})")
    pot = f" setelah potongan {pct(h['biaya'])}" if h["biaya"] else ""
    if h["laba"] <= 0:
        k.append(f"Harga {rp(h['harga'])}{ket}: RUGI {rp(bulat(-h['laba']))}/unit{pot} - harga ini TIDAK BOLEH dipakai.")
    else:
        k.append(f"Harga {rp(h['harga'])}{ket}: laba {rp(bulat(h['laba']))}/unit{pot}, margin {pct(h['margin'])}, "
                 f"markup {pct(h['markup'])}.")
    if pajak.aktif and pajak.mode == "termasuk" and h["laba"] > 0:
        # v1.0.8: dua cara hitung KELIRU dicetak terpisah dengan label eksplisit (uji 1.0.7: model menyebut
        # angka "PPN tidak dipisah" sebagai hasil "dibagi 1,12")
        if not pajak.mewah:
            dpp112 = bulat(h["harga"] / D("1.12"))
            laba112 = dpp112 - h["biaya"] * h["tayang"] - h["hpp"]
            k.append(f"KELIRU cara 1 - bila harga DIBAGI 1,12 (tarif 12% penuh, salah untuk barang non-mewah): DPP "
                     f"{rp(dpp112)}, margin {pct(laba112 / dpp112)} - jangan dipakai.")
        salah = (h["harga"] - h["biaya"] * h["tayang"] - h["hpp"]) / h["harga"]
        k.append(f"KELIRU cara 2 - bila PPN TIDAK DIPISAH sama sekali (seluruh {rp(h['harga'])} dianggap pendapatan): "
                 f"margin terlihat {pct(salah)} - jangan dipakai.")
        k.append(f"BENAR - PPN dipisah dengan tarif efektif 11% (12% x DPP nilai lain 11/12): DPP {rp(h['dpp'])}, "
                 f"margin {pct(h['margin'])}.")
    if "margin_min" in h:
        mm, batas = h["margin_min"], h["batas"]
        if h["aman"]:
            k.append(f"Status: OK, di atas margin minimum {pct(mm)} (harga terendah yang aman {rp(batas)}).")
        else:
            k.append(f"Status: DI BAWAH MIN - margin minimum {pct(mm)} butuh harga paling rendah {rp(batas)}; "
                     f"harga {rp(h['harga'])} (termasuk sebagai 'harga lama' sementara/pre-order) hanya boleh disebut "
                     f"dengan PERINGATAN: di bawah margin minimum {pct(mm)} (lantai {rp(batas)}).")
        if h["laba"] > 0 and h["harga"] > batas:
            k.append(_kalimat_ruang_diskon(h["harga"], h["hpp"], h["biaya"], mm, pajak))
        k.append(f"Dari harga lantai {rp(batas)}: TIDAK ADA ruang diskon - JANGAN tawarkan diskon/promo potongan harga "
                 f"dari harga ini dan jangan menulis 'dari lantai nanti ada ruang promo'. Yang bisa dilakukan: naikkan "
                 f"harga normal di atas lantai, tekan HPP/biaya, atau promo tanpa potongan harga (bonus/paket/kuota).")
        ruang = [f"diskon {pct(x)} butuh harga normal minimal {rp(_harga_normal_untuk_diskon(h['hpp'], mm, h['biaya'], pajak, x, batas))}"
                 for x in (D("0.05"), D("0.10"))]
        k.append("Agar ADA ruang promo: " + "; ".join(ruang) +
                 " (lalu cek dengan `diskon --harga <harga normal> --rentang`).")
        contoh = _contoh_harga_aman(h["hpp"], mm, h["biaya"], pajak, batas)
        if contoh:
            k.append(f"Contoh harga cantik yang aman (>= lantai {rp(batas)}; hanya angka ini yang boleh dipakai sebagai "
                     f"contoh/'misal'): {', '.join(rp(x) for x in contoh)}.")
    return k


def ringkasan_diskon_target(h, persen):
    """v1.0.9: harga normal minimal agar diskon `persen` tetap >= margin minimum + harga cantik di atasnya + tabel promo."""
    if "margin_min" not in h:
        raise InputError("--diskon-target butuh margin minimum: isi --margin-min atau --kategori")
    if persen <= 0:
        raise InputError("--diskon-target harus lebih dari 0")
    mm, pajak = h["margin_min"], h["pajak"]
    hmin = _harga_normal_untuk_diskon(h["hpp"], mm, h["biaya"], pajak, persen, h["batas"])
    c = hitung_cantik(hmin, h["hpp"], mm, h["biaya"], hmin, pajak)
    cantik = [b["harga"] for b in c["baris"] if b["harga"] >= hmin][:4]
    k = [f"Agar bisa diskon {pct(persen)} tanpa menembus margin minimum {pct(mm)}: harga normal minimal {rp(hmin)}; "
         f"harga cantik di atasnya: {', '.join(rp(x) for x in cantik) or 'TIDAK ADA'}.",
         f"Tabel promo diskon {pct(persen)} dari harga-harga itu (salin utuh; harga lain = jalankan script lagi):",
         tabel_harga_promo([hmin] + cantik, h["hpp"], persen, h["biaya"], mm, pajak)]
    return k


def _harga_khusus_reseller(harga_promo, nama, batas):
    """Saran harga khusus reseller/agen selama promo: < harga promo dan >= lantai margin."""
    atas = ke_atas(D(harga_promo)) - 1   # rupiah bulat terbesar yang masih DI BAWAH harga promo
    if batas is None:
        return (f"Bila {nama} diberi harga khusus selama promo: harus di bawah {rp(bulat(harga_promo))} "
                f"(paling tinggi {rp(atas)}); lantai margin belum dicek - jalankan ulang dengan --kategori/--margin-min.")
    if atas < batas:
        return (f"Harga khusus {nama} selama promo TIDAK MUNGKIN: harus di bawah {rp(bulat(harga_promo))} tetapi lantai "
                f"margin {rp(batas)} -> kecilkan diskon atau batasi kuota, jangan turunkan harga {nama}.")
    contoh = kelipatan(atas, D(500), "bawah")
    teks = (f"Bila {nama} diberi harga khusus selama promo: rentang aman {rp(batas)} s.d. {rp(atas)} "
            f"(di bawah harga promo {rp(bulat(harga_promo))}, tidak di bawah lantai margin)")
    if contoh >= batas and contoh != atas:
        untung = bulat(harga_promo) - contoh
        teks += f"; contoh angka bulat {rp(contoh)} (untung {nama} bila jual di harga promo {rp(untung)}/unit"
        teks += ", tipis - mengecilkan diskon biasanya lebih masuk akal)" if untung < bulat(harga_promo) / 10 else ")"
    return teks + "."


def ringkasan_diskon(h, mm, hpp, reseller):
    pajak = h["pajak"]
    k = []
    ef = " (harga efektif per unit)" if h["bxgy"] else ""
    k.append(f"Promo {h['label']} dari harga {rp(h['harga'])} -> harga promo {rp(h['harga_promo'])}{ef}: laba "
             f"{rp(bulat(h['laba_promo']))}/unit (margin {pct(h['margin_promo'])}), dibanding harga normal laba "
             f"{rp(bulat(h['laba_normal']))}/unit (margin {pct(h['margin_normal'])}).")
    if h["rugi"]:
        k.append("Status: RUGI per unit - promo ini TIDAK DISARANKAN (makin laku makin rugi).")
    elif mm is not None and not h["promo_aman"]:
        k.append(f"Status: DI BAWAH MIN - margin saat promo {pct(h['margin_promo'])} di bawah minimum {pct(mm)} "
                 f"(lantai {rp(h['batas'])}) -> promo ini TIDAK DISARANKAN.")
    elif mm is not None:
        k.append(f"Status: OK - margin saat promo {pct(h['margin_promo'])} masih di atas minimum {pct(mm)} (lantai {rp(h['batas'])}).")
    else:
        k.append("Margin minimum BELUM diisi - jangan menilai promo ini aman; jalankan ulang dengan --kategori atau --margin-min.")
    if not h["rugi"]:
        kanal = (f"dibanding harga normal di kanal yang sama (potongan {pct(h['biaya'])})" if h["biaya"]
                 else "dibanding harga normal (potongan kanal 0%)")
        teks = f"Agar laba kotor tetap sama, penjualan harus naik {pct(h['tambahan'])} {kanal}"
        if "volume" in h:
            teks += f": dari {angka(h['volume'])} jadi minimal {angka(h['volume_perlu'])} unit"
        if h["tambahan"] > 1:
            teks += " - kenaikan > 100%, TIDAK DISARANKAN"
        k.append(teks + ".")
        if "langsung_faktor" in h:
            teks = (f"Bila penjualan normal Anda selama ini lewat jual langsung (tanpa potongan, laba "
                    f"{rp(bulat(h['laba_langsung']))}/unit), penjualan harus naik {pct(h['langsung_faktor'] - 1)}")
            if "volume" in h:
                teks += f": dari {angka(h['volume'])} jadi minimal {angka(h['langsung_volume'])} unit"
            k.append(teks + ".")
    for nama, hb in reseller:
        if h["harga_promo"] <= D(hb):
            sama = "SAMA DENGAN" if bulat(h["harga_promo"]) == D(hb) else "LEBIH MURAH dari"
            k.append(f"KONFLIK KANAL: harga promo {rp(bulat(h['harga_promo']))} {sama} harga beli {nama} {rp(D(hb))} - "
                     f"wajib disampaikan; solusi: kecilkan diskon, batasi kuota/maks beli, atau harga khusus {nama}.")
            # reseller membeli langsung (tanpa potongan marketplace): lantai margin dihitung dengan potongan 0%
            lantai_r = pajak.minimum(hpp, mm, NOL) if mm is not None else None
            k.append(_harga_khusus_reseller(h["harga_promo"], nama, lantai_r))
    k.append(_kalimat_ruang_diskon(h["harga"], hpp, h["biaya"], mm, pajak, reseller))
    return k


def ringkasan_rentang(harga, baris, teks_batas_kalimat):
    ok = [b for b in baris if b[-1] == "OK"]
    k = []
    if ok:
        rentang = (f"{ok[0][0]} s.d. {ok[-1][0]} (harga promo {ok[0][1]} s.d. {ok[-1][1]})" if len(ok) > 1
                   else f"hanya {ok[0][0]} (harga promo {ok[0][1]})")
        k.append(f"Dari harga {rp(D(harga))}, diskon berstatus OK di tabel: {rentang}"
                 + ("; baris lain DI BAWAH MIN/KONFLIK/RUGI - jangan disarankan." if len(ok) < len(baris) else "."))
    else:
        k.append(f"Dari harga {rp(D(harga))}, TIDAK ADA diskon berstatus OK di rentang ini - jangan sarankan satu pun.")
    k.append(teks_batas_kalimat)
    return k


def ringkasan_tangga(h):
    k = []
    for b in h["baris"]:
        teks = (f"{b['nama']} (min beli {b['min']}): {rp(b['harga'])}/unit, laba kita {rp(bulat(b['laba']))}/unit, "
                f"margin {pct(b['margin'])} - {'OK' if b['aman'] else 'DI BAWAH MIN (jangan dipakai)'}")
        if b["reseller"]:
            teks += f"; untung {b['nama']} di harga anjuran {rp(h['anjuran'])}: {rp(b['untung_reseller'])}/unit ({pct(b['margin_reseller'])})"
        k.append(teks + ".")
    k.append(f"Lantai margin {pct(h['margin_min'])}: tidak ada level (termasuk harga khusus saat promo) di bawah {rp(h['batas'])}.")
    k += [p if p.startswith("KONFLIK") else "PERHATIAN: " + p for p in h["peringatan"]]
    return k


def ringkasan_bundel(h):
    k = [f"Paket {rp(h['harga_bundel'])} (beli satuan {rp(h['total_normal'])}, pembeli hemat {rp(h['hemat'])} = "
         f"{pct(h['hemat_persen'])}): laba {rp(bulat(h['laba_bundel']))}/paket, margin {pct(h['margin_bundel'])}."]
    if "batas" in h:
        k.append(f"Status: {'OK' if h['aman'] else 'DI BAWAH MIN (jangan dipakai)'} - harga paket terendah untuk margin "
                 f"{pct(h['margin_min'])}: {rp(h['batas'])}.")
    k += ["PERHATIAN: " + p for p in h["peringatan"]]
    return k


def ringkasan_cantik(h, persen=None, hpp=None, mm=None, biaya=NOL):
    if h["batas"] is None:
        k = ["Lantai belum dicek (isi --hpp dan --margin-min/--kategori) - kandidat belum boleh direkomendasikan."]
    else:
        ok = [rp(b["harga"]) for b in h["baris"] if b["aman"]]
        tidak = [rp(b["harga"]) for b in h["baris"] if not b["aman"]]
        k = [f"Harga cantik yang boleh dipakai (>= lantai {rp(h['batas'])}): {', '.join(ok) if ok else 'TIDAK ADA'}."]
        if tidak:
            k.append(f"DI BAWAH MIN, jangan dipakai: {', '.join(tidak)}.")
    if persen is not None and hpp is not None:
        k.append(f"Tabel promo diskon {pct(persen)} untuk SEMUA kandidat (salin utuh; harga lain = jalankan script lagi):")
        k.append(tabel_harga_promo([b["harga"] for b in h["baris"]], hpp, persen, biaya, mm, h["pajak"]))
    return k


def ringkasan_bep(h):
    judul = "Agar mencapai target laba" if h["target_laba"] else "Titik impas"
    k = [f"{judul}: {angka(h['unit'])} unit/bulan (omzet {rp(h['omzet'])})"
         + (f", {angka(h['per_hari'])} unit/hari ({h['hari_jual']} hari jual)" if "per_hari" in h else "") + "."]
    if "volume" in h:
        if "batas_aman" in h:
            k.append(f"Penjualan sekarang {angka(h['volume'])} unit -> laba {rp(bulat(h['laba_sekarang']))}/bulan; "
                     f"penjualan boleh turun {pct(h['batas_aman'])} sebelum rugi.")
        else:
            k.append(f"Penjualan sekarang {angka(h['volume'])} unit -> RUGI {rp(bulat(-h['laba_sekarang']))}/bulan; "
                     f"kurang {angka(h['kurang'])} unit dari titik impas.")
    return k


# ---------------------------------------------------------------- CLI

def _opsi_biaya(p):
    p.add_argument("--kategori", choices=sorted(MARGIN_MIN_KATEGORI),
                   help="kategori produk untuk margin minimum bawaan bila --margin-min tidak diisi: "
                        "pangan 40%%, jasa 50%%, umum 30%%")
    p.add_argument("--biaya-persen", default="0", help="potongan %% dari harga jual (admin marketplace, dll). Default 0")
    p.add_argument("--ppn", choices=["termasuk", "belum"],
                   help="khusus PKP: 'termasuk' = harga yang dimasukkan sudah termasuk PPN; 'belum' = harga = DPP")
    p.add_argument("--mewah", action="store_true", help="barang mewah (PPN 12%% penuh)")


def buat_parser():
    ap = argparse.ArgumentParser(description="Kalkulator strategi harga (Rupiah, Decimal).")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p = sub.add_parser("margin", help="margin vs markup")
    p.add_argument("--hpp", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--harga")
    g.add_argument("--margin", help="target margin %% dari harga jual")
    g.add_argument("--markup", help="target markup %% dari HPP")
    p.add_argument("--margin-min", help="tandai status OK / DI BAWAH MIN terhadap margin minimum ini")
    p.add_argument("--diskon-target", help="diskon %% yang ingin bisa diberikan: cetak harga normal minimal + "
                                           "harga cantik di atasnya beserta harga & margin promo")
    _opsi_biaya(p)

    p = sub.add_parser("bep", help="titik impas")
    p.add_argument("--biaya-tetap", required=True, help="biaya tetap per bulan (sewa, gaji tetap, listrik dasar, cicilan alat)")
    p.add_argument("--harga", required=True)
    p.add_argument("--hpp", required=True, help="biaya variabel per unit (bahan, kemasan, upah borongan)")
    p.add_argument("--target-laba", default="0")
    p.add_argument("--hari-jual", help="jumlah hari jual per bulan (angka bulat > 0)")
    p.add_argument("--volume", help="penjualan per bulan sekarang (unit)")
    _opsi_biaya(p)

    p = sub.add_parser("tangga", help="tangga harga reseller/grosir")
    p.add_argument("--harga-ecer", required=True)
    p.add_argument("--hpp", required=True)
    p.add_argument("--level", action="append", required=True, help="Nama:min_beli:diskon%%  atau Nama:min_beli:=harga")
    p.add_argument("--margin-min")
    p.add_argument("--kelipatan", help="bulatkan harga level ke kelipatan ini (mis. 500)")
    p.add_argument("--harga-anjuran", help="harga eceran anjuran untuk reseller. Default = --harga-ecer (disarankan sama)")
    p.add_argument("--margin-reseller-min", default="10", help="untung reseller minimal %% dari harga anjuran. Default 10")
    p.add_argument("--harga-promo", action="append",
                   help="harga promo konsumen yang direncanakan (mis. flash sale), bisa diulang; cek konflik kanal")
    _opsi_biaya(p)

    p = sub.add_parser("diskon", help="dampak promo pada volume")
    p.add_argument("--harga", required=True)
    p.add_argument("--hpp", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--diskon", help="diskon %%")
    g.add_argument("--potongan", help="potongan rupiah per unit")
    g.add_argument("--beli-gratis", help="beli:gratis, mis. 2:1")
    g.add_argument("--rentang", help="tabel rentang diskon %%, mis. 15-17 atau 10-30:5 (awal-akhir:langkah)")
    p.add_argument("--volume", help="penjualan normal (unit) dalam periode yang sama")
    p.add_argument("--margin-min")
    p.add_argument("--harga-reseller", action="append",
                   help="harga beli reseller/agen, format Nama:harga (mis. Agen:26250), bisa diulang; cek konflik kanal")
    p.add_argument("--kanal", choices=["langsung", "marketplace"],
                   help="kanal promo; 'marketplace' memberi PERHATIAN bila --biaya-persen 0")
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
    p.add_argument("--diskon", help="diskon %% rencana promo: cetak harga promo + margin promo + status untuk tiap kandidat")
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


def _parse_hari(s):
    t = str(s).strip()
    if not re.match(r"^-?\d+$", t) or int(t) <= 0:
        raise InputError(f"hari jual harus angka bulat lebih dari 0 (didapat {s})")
    return int(t)


def _mm(nilai):
    return parse_persen(nilai, nama="margin minimum", maks=D(99)) if nilai else None


def _wajib_mm(mm):
    if mm is None:
        raise InputError("tangga butuh margin minimum: isi --margin-min <persen> atau --kategori pangan/jasa/umum")
    return mm


def _mm_pakai(a):
    """(margin_min, keterangan) dari --margin-min (pengguna) atau default --kategori; (None, None) bila keduanya kosong."""
    if getattr(a, "margin_min", None):
        return _mm(a.margin_min), "disebut pengguna"
    kat = getattr(a, "kategori", None)
    if kat:
        nilai, ket = MARGIN_MIN_KATEGORI[kat]
        return nilai, f"default kategori {ket}"
    return None, None


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
    pajak = Pajak(getattr(a, "ppn", None), getattr(a, "mewah", False)) if a.perintah != "ppn" else TANPA_PPN
    mm, ket_mm = _mm_pakai(a)
    hasil, ring = _jalankan_perintah(a, biaya, pajak, mm)
    if ring:
        hasil = blok_ringkasan(ring) + "\n\n" + hasil
    if mm is not None and a.perintah in ("margin", "tangga", "diskon", "bundel", "cantik"):
        hasil = f"Margin minimum dipakai: {pct(mm)} ({ket_mm}) - tulis di bagian Asumsi\n" + hasil
    return hasil


def _jalankan_perintah(a, biaya, pajak, mm):
    if a.perintah == "margin":
        h = hitung_margin(parse_rupiah(a.hpp, nama="HPP"),
                          harga=parse_rupiah(a.harga, nama="harga") if a.harga else None,
                          margin=parse_persen(a.margin, nama="margin", maks=D(99)) if a.margin else None,
                          markup=parse_persen(a.markup, nama="markup", maks=D(10000)) if a.markup else None,
                          biaya=biaya, pajak=pajak, margin_min=mm)
        ring = ringkasan_margin(h)
        if a.diskon_target:
            ring += ringkasan_diskon_target(h, parse_persen(a.diskon_target, nama="diskon target", maks=D(99)))
        return cetak_margin(h), ring
    if a.perintah == "bep":
        h = hitung_bep(parse_rupiah(a.biaya_tetap, boleh_nol=True, nama="biaya tetap"), parse_rupiah(a.harga, nama="harga"),
                       parse_rupiah(a.hpp, boleh_nol=True, nama="HPP"), biaya,
                       parse_rupiah(a.target_laba, boleh_nol=True, nama="target laba"),
                       _parse_hari(a.hari_jual) if a.hari_jual is not None else None,
                       parse_rupiah(a.volume, boleh_nol=True, nama="volume") if a.volume else None, pajak=pajak)
        return cetak_bep(h), ringkasan_bep(h)
    if a.perintah == "tangga":
        h = hitung_tangga(parse_rupiah(a.harga_ecer, nama="harga eceran"), parse_rupiah(a.hpp, nama="HPP"),
                          [parse_level(x) for x in a.level], _wajib_mm(mm),
                          biaya, parse_rupiah(a.kelipatan, nama="kelipatan") if a.kelipatan else None, pajak=pajak,
                          harga_anjuran=parse_rupiah(a.harga_anjuran, nama="harga anjuran") if a.harga_anjuran else None,
                          margin_reseller_min=parse_persen(a.margin_reseller_min, nama="margin reseller minimum", maks=D(99)),
                          harga_promo=[parse_rupiah(x, nama="harga promo") for x in (a.harga_promo or [])])
        return cetak_tangga(h), ringkasan_tangga(h)
    if a.perintah == "diskon":
        harga_d, hpp_d = parse_rupiah(a.harga, nama="harga"), parse_rupiah(a.hpp, nama="HPP")
        reseller = [parse_harga_reseller(x) for x in (a.harga_reseller or [])]
        vol = parse_rupiah(a.volume, nama="volume") if a.volume else None
        if hpp_d >= harga_d:
            raise InputError(f"di harga normal {rp(harga_d)} saja sudah tidak untung (HPP >= harga); perbaiki harga dulu")
        teks_batas = cetak_batas_diskon(hitung_batas_diskon(harga_d, hpp_d, biaya, mm, pajak, reseller))
        if a.rentang:
            baris = hitung_rentang(harga_d, hpp_d, parse_rentang(a.rentang), vol, biaya, mm, pajak, reseller)
            teks = _kepala_ppn(pajak) + [cetak_rentang(baris, vol is not None), teks_batas] + _ekor_ppn(pajak)
            ring = ringkasan_rentang(harga_d, baris, _kalimat_ruang_diskon(harga_d, hpp_d, biaya, mm, pajak, reseller))
            ring.append("Tabel rentang (salin SEMUA baris apa adanya; diskon di luar tabel = jalankan --rentang lagi):")
            ring.append(cetak_rentang(baris, vol is not None).split("\n", 1)[1])
            if mm is None:
                ring.append("Margin minimum BELUM diisi - jalankan ulang dengan --kategori atau --margin-min sebelum menilai aman.")
            return "\n".join(teks), ring
        h = hitung_diskon(parse_rupiah(a.harga, nama="harga"), parse_rupiah(a.hpp, nama="HPP"),
                          diskon=parse_persen(a.diskon, nama="diskon") if a.diskon else None,
                          potongan=parse_rupiah(a.potongan, nama="potongan") if a.potongan else None,
                          bxgy=parse_bxgy(a.beli_gratis) if a.beli_gratis else None,
                          volume=parse_rupiah(a.volume, nama="volume") if a.volume else None,
                          biaya=biaya, margin_min=mm, pajak=pajak,
                          harga_reseller=reseller, kanal=a.kanal)
        return cetak_diskon(h) + "\n" + teks_batas, ringkasan_diskon(h, mm, hpp_d, reseller)
    if a.perintah == "bundel":
        item = [parse_item(x) for x in a.item]
        if len(item) < 2 and item[0]["qty"] < 2:
            raise InputError("paket butuh minimal 2 item (atau 1 item dengan jumlah >= 2)")
        h = hitung_bundel(item, parse_rupiah(a.harga_bundel, nama="harga paket"),
                          parse_rupiah(a.biaya_tambahan, boleh_nol=True, nama="biaya tambahan"), biaya,
                          mm, pajak=pajak)
        return cetak_bundel(h), ringkasan_bundel(h)
    if a.perintah == "elastisitas":
        h = hitung_elastisitas(parse_rupiah(a.harga, nama="harga"), parse_rupiah(a.volume, nama="volume"),
                               parse_rupiah(a.hpp, nama="HPP"),
                               [parse_persen(x, nama="perubahan harga", boleh_negatif=True, maks=D(99)) for x in (a.ubah or [])],
                               [_parse_el(x) for x in a.elastisitas] if a.elastisitas else None,
                               biaya, parse_rupiah(a.biaya_tetap, boleh_nol=True, nama="biaya tetap"),
                               [parse_rupiah(x, nama="harga baru") for x in (a.harga_baru or [])], pajak=pajak)
        return cetak_elastisitas(h), None
    if a.perintah == "cantik":
        h = hitung_cantik(parse_rupiah(a.harga, nama="harga"),
                          parse_rupiah(a.hpp, nama="HPP") if a.hpp else None,
                          mm,
                          biaya, parse_rupiah(a.harga_min, nama="harga minimum") if a.harga_min else None, pajak=pajak)
        persen = parse_persen(a.diskon, nama="diskon", maks=D(99)) if a.diskon else None
        if persen is not None and not a.hpp:
            raise InputError("--diskon di perintah cantik butuh --hpp agar margin promo bisa dihitung")
        return cetak_cantik(h), ringkasan_cantik(h, persen, parse_rupiah(a.hpp, nama="HPP") if a.hpp else None, mm, biaya)
    if a.perintah == "ppn":
        h = hitung_ppn(parse_rupiah(a.harga, nama="harga"), a.mode, a.mewah)
        return cetak_ppn(h, a.status_pkp), None
    raise InputError("perintah tidak dikenal")


def main(argv=None):
    try:
        print(jalankan(argv))
        return 0
    except InputError as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    except (ArithmeticError, InvalidOperation) as e:   # jaring pengaman: jangan pernah tampilkan traceback
        print(f"GAGAL: angka tidak bisa dihitung ({type(e).__name__}); periksa lagi input (harga/diskon/kelipatan)",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
