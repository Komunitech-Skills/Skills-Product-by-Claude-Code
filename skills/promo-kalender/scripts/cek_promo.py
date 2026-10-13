#!/usr/bin/env python3
"""Cek margin promo & susun jadwal kampanye untuk momen belanja (9.9, 10.10, 11.11, 12.12, gajian, dll.).

Subperintah:
  margin  : harga normal + HPP + mekanisme promo -> harga efektif, laba & margin per unit SEBELUM vs SESUDAH
            promo, diskon maksimal agar tidak rugi, kenaikan penjualan yang dibutuhkan, dan titik impas anggaran.
            Status per produk: RUGI / TIPIS / AMAN.
  jadwal  : tanggal momen -> linimasa kampanye lengkap dengan nama hari (standar H-14 s.d. H+7;
            pola lebaran & back to school H-30 s.d. H+14).

Mekanisme promo yang didukung (per produk): diskon persen, harga promo/flash sale, potongan Rp per unit,
bundling "3=Rp 189.000", beli-gratis "2+1", voucher per pesanan (Rp atau % dengan batas maksimum),
subsidi ongkir per pesanan, cashback yang ditanggung penjual (%), hadiah/biaya tambahan per unit.

Aturan pembulatan (dijelaskan juga di output):
- Harga promo dari diskon persen dibulatkan KE ATAS ke kelipatan --bulatkan (default Rp 100) supaya penjual
  tidak rugi karena pembulatan; persen diskon NYATA dihitung ulang dari harga akhir dan "diskon yang boleh
  diklaim" dibulatkan KE BAWAH ke bilangan bulat (klaim tidak pernah lebih besar dari kenyataan).
- Perhitungan internal memakai desimal penuh; tampilan Rupiah dibulatkan ke rupiah terdekat.
- Diskon maksimal agar tidak rugi dibulatkan KE BAWAH (1 desimal); harga impas dibulatkan KE ATAS ke rupiah.

Biaya platform (admin, layanan, program ongkir) TIDAK disimpan di script: isi sendiri dari Seller Center.
Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 cek_promo.py margin --produk "Kaos Polos" --harga-normal "Rp 89.000" --hpp 52.000 --diskon-persen 25
  python3 cek_promo.py margin --harga-normal 89000 --hpp 52000 --bundling "3=Rp 229.000" --biaya-platform 10
  python3 cek_promo.py margin --config promo.json
  python3 cek_promo.py jadwal --momen 11.11 --dari 2026-09-23
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

VERSI = "1.0.4"
NOL = Decimal(0)
SERATUS = Decimal(100)


class GalatInput(Exception):
    pass


PERINGATAN_INPUT = []


# ---------------------------------------------------------------- angka & format
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3)]


def parse_angka(nilai, nama="angka"):
    """Baca angka format Indonesia: 'Rp 15.000', '15.000,50', '1,5 jt', '89rb', '12,5%', 15000."""
    if nilai is None or isinstance(nilai, bool):
        raise GalatInput("{}: nilai kosong".format(nama))
    if isinstance(nilai, (int, Decimal)):
        return Decimal(nilai)
    if isinstance(nilai, float):
        return Decimal(str(nilai))
    asli = str(nilai)
    s = asli.strip().lower().replace(" ", "").replace(" ", "")
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
        raise GalatInput("{}: '{}' bukan angka yang valid. Contoh yang benar: 89000, \"Rp 89.000\", 89rb, 12,5".format(nama, asli))

    def cek_ribuan(bagian):
        if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
            raise GalatInput("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                             "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))

    if "," in s and "." in s:
        if s.rfind(",") < s.rfind("."):
            raise GalatInput("{}: '{}' memakai format Inggris. Tulis 1.250.000,50 (titik ribuan, koma desimal)".format(nama, asli))
        utuh, _, desimal = s.rpartition(",")
        cek_ribuan(utuh.split("."))
        s = utuh.replace(".", "") + "." + desimal
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2:
            if len(bagian[1]) == 3 and bagian[0] not in ("", "0"):
                PERINGATAN_INPUT.append("{}: '{}' dibaca sebagai {},{} (koma = desimal). Jika maksudnya ribuan, "
                                        "tulis {}.{}".format(nama, asli, bagian[0], bagian[1], bagian[0], bagian[1]))
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            cek_ribuan(bagian)
            s = s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            cek_ribuan(bagian)
            s = s.replace(".", "")
    try:
        d = Decimal(s) * pengali
    except InvalidOperation:
        raise GalatInput("{}: '{}' bukan angka yang valid".format(nama, asli))
    return -d if negatif else d


def opsional(v, nama, default=None):
    if v is None or (isinstance(v, str) and not v.strip()):
        return default
    return parse_angka(v, nama)


def rp(d):
    d = Decimal(d).quantize(Decimal(1), ROUND_HALF_UP)
    teks = "{:,}".format(abs(int(d))).replace(",", ".")
    return ("-Rp " if d < 0 else "Rp ") + teks


def persen(d, digit=1):
    q = Decimal(1).scaleb(-digit)
    d = Decimal(d).quantize(q, ROUND_HALF_UP)
    return "{:f}".format(d).replace(".", ",") + "%"


def angka_json(d, digit=2):
    if d is None:
        return None
    d = Decimal(d)
    if d == d.to_integral_value():
        return int(d)
    return float(d.quantize(Decimal(1).scaleb(-digit), ROUND_HALF_UP))


def bulat_atas(d, kelipatan):
    return (Decimal(d) / kelipatan).to_integral_value(ROUND_CEILING) * kelipatan


# ---------------------------------------------------------------- model promo
def siapkan_produk(cfg, default_nama="Produk"):
    nama = str(cfg.get("produk") or cfg.get("nama") or default_nama).strip()
    label = "[{}] ".format(nama)
    normal = parse_angka(cfg.get("harga_normal"), label + "harga normal")
    hpp = parse_angka(cfg.get("hpp"), label + "HPP/modal")
    if normal <= 0:
        raise GalatInput(label + "harga normal harus lebih dari 0")
    if hpp < 0:
        raise GalatInput(label + "HPP tidak boleh negatif")
    p = {
        "nama": nama, "harga_normal": normal, "hpp": hpp,
        "biaya_platform": opsional(cfg.get("biaya_platform"), label + "biaya platform %", NOL),
        "biaya_per_pesanan": opsional(cfg.get("biaya_per_pesanan"), label + "biaya per pesanan", NOL),
        "biaya_lain": opsional(cfg.get("biaya_lain"), label + "biaya lain per unit", NOL),
        "subsidi_ongkir": opsional(cfg.get("subsidi_ongkir"), label + "subsidi ongkir per pesanan", NOL),
        "cashback": opsional(cfg.get("cashback"), label + "cashback %", NOL),
        "target_unit": opsional(cfg.get("target_unit"), label + "target unit"),
        "unit_normal": opsional(cfg.get("unit_normal"), label + "unit normal"),
        "anggaran": opsional(cfg.get("anggaran"), label + "anggaran", NOL),
        "item_per_pesanan": opsional(cfg.get("item_per_pesanan"), label + "item per pesanan"),
    }
    for k in ("biaya_platform", "cashback"):
        if not NOL <= p[k] < SERATUS:
            raise GalatInput(label + "{} harus 0 sampai di bawah 100%".format(k.replace("_", " ")))
    for k in ("biaya_per_pesanan", "biaya_lain", "subsidi_ongkir", "anggaran"):
        if p[k] < 0:
            raise GalatInput(label + "{} tidak boleh negatif".format(k.replace("_", " ")))
    for k in ("target_unit", "unit_normal", "item_per_pesanan"):
        if p[k] is not None and (p[k] < 0 or p[k] != p[k].to_integral_value()):
            raise GalatInput(label + "{} harus bilangan bulat >= 0".format(k.replace("_", " ")))
    if p["item_per_pesanan"] is not None and p["item_per_pesanan"] < 1:
        raise GalatInput(label + "item per pesanan minimal 1")

    # mekanisme harga (maks. satu)
    mek = [k for k in ("diskon_persen", "harga_promo", "potongan_rp", "bundling", "beli_gratis")
           if cfg.get(k) not in (None, "")]
    if len(mek) > 1:
        raise GalatInput(label + "pilih satu mekanisme harga saja (ada: {}). Voucher, subsidi ongkir, cashback "
                         "boleh digabung.".format(", ".join(mek)))
    bulatkan = opsional(cfg.get("bulatkan"), label + "bulatkan", Decimal(100))
    if bulatkan <= 0:
        raise GalatInput(label + "kelipatan pembulatan harus > 0")
    qty_paket = Decimal(1)
    catatan = []
    jenis = mek[0] if mek else "tanpa_potongan_harga"
    if jenis == "diskon_persen":
        d = parse_angka(cfg["diskon_persen"], label + "diskon %")
        if not NOL < d < SERATUS:
            raise GalatInput(label + "diskon persen harus di antara 0 dan 100")
        mentah = normal * (1 - d / SERATUS)
        harga_paket = bulat_atas(mentah, bulatkan)
        if harga_paket > normal:
            harga_paket = normal
        if harga_paket != mentah:
            catatan.append("Harga promo {} dibulatkan KE ATAS dari {} ke kelipatan {}.".format(
                rp(harga_paket), rp(mentah), rp(bulatkan)))
        label_mek = "Diskon {}".format(persen(d, 2).replace(",00%", "%"))
    elif jenis == "harga_promo":
        harga_paket = parse_angka(cfg["harga_promo"], label + "harga promo")
        if harga_paket <= 0:
            raise GalatInput(label + "harga promo harus lebih dari 0")
        if harga_paket > normal:
            raise GalatInput(label + "harga promo ({}) lebih tinggi dari harga normal ({})".format(rp(harga_paket), rp(normal)))
        label_mek = "Harga promo/flash sale {}".format(rp(harga_paket))
    elif jenis == "potongan_rp":
        pot = parse_angka(cfg["potongan_rp"], label + "potongan Rp")
        if not NOL < pot < normal:
            raise GalatInput(label + "potongan harus lebih dari 0 dan kurang dari harga normal")
        harga_paket = normal - pot
        label_mek = "Potongan {} per unit".format(rp(pot))
    elif jenis == "bundling":
        m = re.match(r"^\s*(\d+)\s*(?:pcs|x|buah|item)?\s*[=:@]\s*(.+)$", str(cfg["bundling"]), re.I)
        if not m:
            raise GalatInput(label + "format bundling harus 'jumlah=harga', mis. \"3=Rp 229.000\"")
        qty_paket = Decimal(int(m.group(1)))
        if qty_paket < 2:
            raise GalatInput(label + "bundling minimal 2 unit")
        harga_paket = parse_angka(m.group(2), label + "harga bundling")
        if harga_paket <= 0:
            raise GalatInput(label + "harga bundling harus lebih dari 0")
        if harga_paket > normal * qty_paket:
            raise GalatInput(label + "harga bundling lebih mahal dari beli satuan ({})".format(rp(normal * qty_paket)))
        label_mek = "Bundling {} unit = {}".format(int(qty_paket), rp(harga_paket))
    elif jenis == "beli_gratis":
        m = re.match(r"^\s*(\d+)\s*\+\s*(\d+)\s*$", str(cfg["beli_gratis"]))
        if not m or int(m.group(1)) < 1 or int(m.group(2)) < 1:
            raise GalatInput(label + "format beli-gratis harus 'beli+gratis', mis. \"2+1\"")
        bayar, gratis = int(m.group(1)), int(m.group(2))
        qty_paket = Decimal(bayar + gratis)
        harga_paket = normal * bayar
        label_mek = "Beli {} gratis {}".format(bayar, gratis)
    else:
        harga_paket = normal
        label_mek = "Tanpa potongan harga"
    p.update({"jenis": jenis, "label_mekanisme": label_mek, "harga_paket": harga_paket, "qty_paket": qty_paket,
              "bulatkan": bulatkan, "catatan": catatan})

    # voucher per pesanan
    v = cfg.get("voucher")
    p["voucher"] = {"jenis": "tidak", "nilai": NOL, "maks": None, "min_belanja": NOL}
    if v not in (None, "", 0, "0"):
        teks = str(v).strip()
        if teks.endswith("%"):
            nilai = parse_angka(teks, label + "voucher %")
            if not NOL < nilai < SERATUS:
                raise GalatInput(label + "voucher persen harus di antara 0 dan 100")
            p["voucher"] = {"jenis": "persen", "nilai": nilai,
                            "maks": opsional(cfg.get("maks_voucher"), label + "maks voucher"), "min_belanja": NOL}
        else:
            nilai = parse_angka(teks, label + "voucher Rp")
            if nilai <= 0:
                raise GalatInput(label + "voucher harus lebih dari 0")
            p["voucher"] = {"jenis": "rp", "nilai": nilai, "maks": None, "min_belanja": NOL}
        p["voucher"]["min_belanja"] = opsional(cfg.get("min_belanja"), label + "minimum belanja", NOL)
    return p


def hitung_pesanan(p, kotor, qty, pakai_promo):
    """Hitung satu pesanan berisi qty unit dengan total harga (sebelum voucher) = kotor. Kembalikan dict rincian."""
    voucher = NOL
    if pakai_promo and p["voucher"]["jenis"] != "tidak" and kotor >= p["voucher"]["min_belanja"]:
        if p["voucher"]["jenis"] == "rp":
            voucher = min(p["voucher"]["nilai"], kotor)
        else:
            voucher = kotor * p["voucher"]["nilai"] / SERATUS
            if p["voucher"]["maks"] is not None:
                voucher = min(voucher, p["voucher"]["maks"])
    dibayar = kotor - voucher
    platform = dibayar * p["biaya_platform"] / SERATUS
    cashback = dibayar * p["cashback"] / SERATUS if pakai_promo else NOL
    ongkir = p["subsidi_ongkir"] if pakai_promo else NOL
    modal = (p["hpp"] + (p["biaya_lain"] if pakai_promo else NOL)) * qty
    laba = dibayar - platform - cashback - ongkir - p["biaya_per_pesanan"] - modal
    return {"qty": qty, "harga_kotor": kotor, "voucher": voucher, "dibayar_pembeli": dibayar,
            "biaya_platform": platform, "cashback": cashback, "subsidi_ongkir": ongkir,
            "biaya_per_pesanan": p["biaya_per_pesanan"], "modal": modal, "laba": laba,
            "laba_per_unit": laba / qty, "margin": (laba / dibayar * SERATUS) if dibayar > 0 else None}


def analisis_produk(p, batas_tipis):
    qty = p["item_per_pesanan"] if p["item_per_pesanan"] is not None else p["qty_paket"]
    if p["jenis"] in ("bundling", "beli_gratis") and qty % p["qty_paket"] != 0:
        raise GalatInput("[{}] item per pesanan harus kelipatan isi paket ({})".format(p["nama"], int(p["qty_paket"])))
    normal = hitung_pesanan(p, p["harga_normal"], Decimal(1), False)
    promo = hitung_pesanan(p, p["harga_paket"] * qty / p["qty_paket"], qty, True)

    # harga efektif per unit yang benar-benar dibayar pembeli (setelah voucher)
    efektif = promo["dibayar_pembeli"] / qty
    diskon_nyata = (1 - efektif / p["harga_normal"]) * SERATUS
    klaim = diskon_nyata.to_integral_value(ROUND_FLOOR)

    # harga impas per unit (sebelum voucher & dengan biaya promo lain tetap), untuk menentukan diskon maksimal
    f = (p["biaya_platform"] + p["cashback"]) / SERATUS
    biaya_tetap_unit = p["hpp"] + p["biaya_lain"] + (p["subsidi_ongkir"] + p["biaya_per_pesanan"]) / qty
    impas = (biaya_tetap_unit / (1 - f)).to_integral_value(ROUND_CEILING) if f < 1 else None
    harga_min_aman = None
    if (f + batas_tipis / SERATUS) < 1:
        harga_min_aman = (biaya_tetap_unit / (1 - f - batas_tipis / SERATUS)).to_integral_value(ROUND_CEILING)
    diskon_maks = None
    if impas is not None:
        diskon_maks = ((1 - impas / p["harga_normal"]) * SERATUS).quantize(Decimal("0.1"), ROUND_FLOOR)

    lpu = promo["laba_per_unit"]
    margin = promo["margin"]
    if lpu < 0:
        status = "RUGI"
    elif margin is None or margin < batas_tipis:
        status = "TIPIS"
    else:
        status = "AMAN"

    hasil = {
        "produk": p["nama"], "mekanisme": p["label_mekanisme"], "status": status,
        "harga_normal": p["harga_normal"], "hpp": p["hpp"],
        "unit_per_pesanan": qty,
        "harga_efektif_per_unit": efektif, "diskon_nyata_persen": diskon_nyata,
        "diskon_boleh_diklaim_persen": klaim,
        "normal": {k: v for k, v in normal.items()},
        "promo_per_pesanan": {k: v for k, v in promo.items()},
        "laba_per_unit_normal": normal["laba_per_unit"], "margin_normal_persen": normal["margin"],
        "laba_per_unit_promo": lpu, "margin_promo_persen": margin,
        "penurunan_laba_per_unit": normal["laba_per_unit"] - lpu,
        "harga_impas_per_unit": impas, "diskon_maksimal_agar_tidak_rugi_persen": diskon_maks,
        "voucher_per_unit": promo["voucher"] / qty,
        "diskon_harga_maks_jika_voucher_tetap_persen": (
            ((1 - (impas + promo["voucher"] / qty) / p["harga_normal"]) * SERATUS).quantize(Decimal("0.1"), ROUND_FLOOR)
            if impas is not None and promo["voucher"] > 0 else None),
        "harga_minimal_margin_aman": harga_min_aman,
        "catatan": list(p["catatan"]), "peringatan": [],
    }
    w = hasil["peringatan"]
    if p["hpp"] >= p["harga_normal"]:
        w.append("HPP sudah sama/lebih besar dari harga normal: produk ini rugi bahkan tanpa promo.")
    if normal["laba_per_unit"] > 0 and lpu > 0:
        kali = normal["laba_per_unit"] / lpu
        hasil["kelipatan_penjualan_agar_laba_sama"] = kali
        if p["unit_normal"] is not None and p["unit_normal"] > 0:
            hasil["unit_normal"] = p["unit_normal"]
            hasil["unit_dibutuhkan_agar_laba_sama"] = (p["unit_normal"] * kali).to_integral_value(ROUND_CEILING)
    if status == "RUGI":
        if diskon_maks is not None and diskon_maks > 0:
            w.append("RUGI {} per unit saat promo. Kecilkan diskon (maks. {} agar impas) atau pakai mekanisme lain "
                     "(bundling, hadiah kecil, gratis ongkir terbatas).".format(rp(-lpu), persen(diskon_maks)))
        else:
            w.append("RUGI {} per unit saat promo, dan dengan biaya promo ini TIDAK ADA ruang diskon sama sekali "
                     "(harga impas {} ≥ harga normal). Kurangi subsidi/cashback/biaya promo, tinjau ulang harga jual normal "
                     "(skill harga-jual-marketplace), atau jangan ikutkan produk ini.".format(rp(-lpu), rp(impas) if impas else "-"))
    elif status == "TIPIS":
        w.append("Margin promo {} di bawah batas aman {}. Sedikit saja biaya tak terduga (retur, iklan) bisa membuat rugi.".format(
            persen(margin) if margin is not None else "-", persen(batas_tipis)))
    if diskon_nyata >= 50:
        w.append("Diskon ≥ 50%: pastikan harga normal memang harga jual sebelumnya (dilarang menaikkan harga sebelum "
                 "diskon/obral — UU 8/1999 Pasal 11 huruf f) dan kuota/waktu promo benar-benar dipenuhi (Pasal 12).")
    if p["voucher"]["jenis"] != "tidak" and promo["voucher"] == 0:
        w.append("Voucher tidak terpakai pada simulasi ini karena belanja per pesanan di bawah minimum belanja.")

    # kampanye
    if p["target_unit"] is not None:
        tu = p["target_unit"]
        pesanan = (tu / qty).to_integral_value(ROUND_CEILING)
        kamp = {"target_unit": tu, "perkiraan_pesanan": pesanan,
                "omzet_dibayar_pembeli": efektif * tu, "laba_kotor_promo": lpu * tu,
                "anggaran": p["anggaran"], "laba_setelah_anggaran": lpu * tu - p["anggaran"]}
        if p["anggaran"] > 0 and lpu > 0:
            kamp["unit_impas_anggaran"] = (p["anggaran"] / lpu).to_integral_value(ROUND_CEILING)
        if p["unit_normal"] is not None:
            kamp["laba_jika_tanpa_promo"] = normal["laba_per_unit"] * p["unit_normal"]
            kamp["selisih_vs_tanpa_promo"] = kamp["laba_setelah_anggaran"] - kamp["laba_jika_tanpa_promo"]
        if kamp["laba_setelah_anggaran"] < 0:
            if p["anggaran"] > 0:
                w.append("Setelah anggaran {}, kampanye produk ini rugi {}.".format(rp(p["anggaran"]), rp(-kamp["laba_setelah_anggaran"])))
            else:
                w.append("Dengan target {} unit, kampanye produk ini rugi {}.".format(int(tu), rp(-kamp["laba_setelah_anggaran"])))
        hasil["kampanye"] = kamp
    elif p["anggaran"] > 0 and lpu > 0:
        hasil["kampanye"] = {"anggaran": p["anggaran"],
                             "unit_impas_anggaran": (p["anggaran"] / lpu).to_integral_value(ROUND_CEILING)}
    return hasil


def baca_config(path):
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except OSError as e:
        raise GalatInput("file '{}' tidak bisa dibaca ({})".format(path, e.strerror))
    teks = None
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if not teks or not teks.strip():
        raise GalatInput("file config kosong")
    if path.lower().endswith(".json"):
        try:
            data = json.loads(teks)
        except ValueError as e:
            raise GalatInput("JSON tidak valid: {}".format(e))
        if isinstance(data, list):
            data = {"produk": data}
        if not isinstance(data, dict) or not isinstance(data.get("produk"), list) or not data["produk"]:
            raise GalatInput("JSON harus berisi daftar \"produk\" (lihat templates/promo-contoh.json)")
        return data
    try:
        dialek = csv.Sniffer().sniff(teks[:2048], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    rows = [{(k or "").strip().lower().replace(" ", "_"): (v or "").strip() for k, v in r.items()}
            for r in csv.DictReader(io.StringIO(teks), dialect=dialek)]
    rows = [r for r in rows if any(r.values())]
    if not rows:
        raise GalatInput("CSV tidak berisi baris produk")
    return {"produk": rows}


# ---------------------------------------------------------------- output
def ke_json(o):
    if isinstance(o, dict):
        return {k: ke_json(v) for k, v in o.items()}
    if isinstance(o, list):
        return [ke_json(v) for v in o]
    if isinstance(o, Decimal):
        return angka_json(o)
    return o


def cetak_margin(hasil_list, ringkas, batas_tipis, meta):
    L = []
    ikon = {"RUGI": "⛔ RUGI", "TIPIS": "⚠️ TIPIS", "AMAN": "✅ AMAN"}
    for h in hasil_list:
        pr = h["promo_per_pesanan"]
        L.append("### {} — {}  [{}]".format(h["produk"], h["mekanisme"], ikon[h["status"]]))
        L.append("| Komponen | Harga normal (per unit) | Promo (per pesanan {} unit) |".format(int(h["unit_per_pesanan"])))
        L.append("|---|---|---|")
        n = h["normal"]
        L.append("| Harga sebelum voucher | {} | {} |".format(rp(n["harga_kotor"]), rp(pr["harga_kotor"])))
        if pr["voucher"]:
            L.append("| Voucher toko | - | -{} |".format(rp(pr["voucher"])))
        L.append("| Dibayar pembeli | {} | {} |".format(rp(n["dibayar_pembeli"]), rp(pr["dibayar_pembeli"])))
        if n["biaya_platform"] or pr["biaya_platform"]:
            L.append("| Biaya platform | -{} | -{} |".format(rp(n["biaya_platform"]), rp(pr["biaya_platform"])))
        if pr["cashback"]:
            L.append("| Cashback ditanggung penjual | - | -{} |".format(rp(pr["cashback"])))
        if pr["subsidi_ongkir"]:
            L.append("| Subsidi ongkir | - | -{} |".format(rp(pr["subsidi_ongkir"])))
        if pr["biaya_per_pesanan"]:
            L.append("| Biaya per pesanan | -{} | -{} |".format(rp(n["biaya_per_pesanan"]), rp(pr["biaya_per_pesanan"])))
        L.append("| Modal (HPP{}) | -{} | -{} |".format(" + biaya promo" if pr["modal"] != h["hpp"] * pr["qty"] else "",
                                                    rp(n["modal"]), rp(pr["modal"])))
        L.append("| **Laba** | **{}** | **{}** |".format(rp(n["laba"]), rp(pr["laba"])))
        L.append("| Laba per unit | {} | {} |".format(rp(h["laba_per_unit_normal"]), rp(h["laba_per_unit_promo"])))
        L.append("| Margin (laba ÷ dibayar pembeli) | {} | {} |".format(
            persen(h["margin_normal_persen"]) if h["margin_normal_persen"] is not None else "-",
            persen(h["margin_promo_persen"]) if h["margin_promo_persen"] is not None else "-"))
        L.append("")
        L.append("- Harga efektif per unit: {} (hemat nyata {}; klaim aman: \"hemat {}%\")".format(
            rp(h["harga_efektif_per_unit"]), persen(h["diskon_nyata_persen"]), int(h["diskon_boleh_diklaim_persen"])))
        if h["harga_impas_per_unit"] is not None and h["voucher_per_unit"] > 0:
            L.append("- Harga impas per unit yang DIBAYAR pembeli (laba Rp 0): {} → diskon maksimal TOTAL (termasuk voucher): {}".format(
                rp(h["harga_impas_per_unit"]), persen(h["diskon_maksimal_agar_tidak_rugi_persen"])))
            d2 = h["diskon_harga_maks_jika_voucher_tetap_persen"]
            L.append("- Jika voucher {}/unit tetap berjalan, diskon harga maksimal hanya: {}".format(
                rp(h["voucher_per_unit"]), persen(d2) if d2 is not None and d2 > 0 else "0% (tidak ada ruang diskon tambahan)"))
        elif h["harga_impas_per_unit"] is not None:
            L.append("- Harga impas per unit (laba Rp 0): {} → diskon maksimal agar tidak rugi: {}".format(
                rp(h["harga_impas_per_unit"]), persen(h["diskon_maksimal_agar_tidak_rugi_persen"])))
        if h["harga_minimal_margin_aman"] is not None:
            L.append("- Harga minimal agar margin tetap {}: {}".format(persen(batas_tipis), rp(h["harga_minimal_margin_aman"])))
        if "kelipatan_penjualan_agar_laba_sama" in h:
            teks = "- Agar laba total sama dengan hari biasa, penjualan harus {}x lipat".format(
                str(Decimal(h["kelipatan_penjualan_agar_laba_sama"]).quantize(Decimal("0.01"), ROUND_HALF_UP)).replace(".", ","))
            if "unit_dibutuhkan_agar_laba_sama" in h:
                teks += " (dari {} unit biasa → minimal {} unit saat promo)".format(
                    int(h["unit_normal"]), int(h["unit_dibutuhkan_agar_laba_sama"]))
            L.append(teks)
        k = h.get("kampanye")
        if k:
            if "target_unit" in k:
                L.append("- Kampanye: target {} unit → dibayar pembeli {}, laba sebelum anggaran {}, anggaran {}, "
                         "**laba bersih kampanye {}**".format(int(k["target_unit"]), rp(k["omzet_dibayar_pembeli"]),
                                                             rp(k["laba_kotor_promo"]), rp(k["anggaran"]),
                                                             rp(k["laba_setelah_anggaran"])))
                if "laba_jika_tanpa_promo" in k:
                    L.append("- Dibanding tanpa promo (laba {}): selisih {}".format(
                        rp(k["laba_jika_tanpa_promo"]), rp(k["selisih_vs_tanpa_promo"])))
            if "unit_impas_anggaran" in k:
                L.append("- Anggaran {} baru tertutup setelah terjual {} unit.".format(rp(k["anggaran"]), int(k["unit_impas_anggaran"])))
        for c in h["catatan"]:
            L.append("- Catatan: " + c)
        for w in h["peringatan"]:
            L.append("- PERINGATAN: " + w)
        L.append("")
    if ringkas:
        L.append("### Ringkasan kampanye")
        L.append("| Produk | Status | Laba/unit promo | Margin promo | Diskon maks. impas |")
        L.append("|---|---|---|---|---|")
        for h in hasil_list:
            L.append("| {} | {} | {} | {} | {} |".format(
                h["produk"], h["status"], rp(h["laba_per_unit_promo"]),
                persen(h["margin_promo_persen"]) if h["margin_promo_persen"] is not None else "-",
                persen(h["diskon_maksimal_agar_tidak_rugi_persen"]) if h["diskon_maksimal_agar_tidak_rugi_persen"] is not None else "-"))
        if ringkas.get("catatan"):
            L.append("")
            L.append("Catatan: " + ringkas["catatan"])
        if ringkas.get("total_target_unit"):
            L.append("")
            L.append("Total target {} unit, dibayar pembeli {}, laba sebelum anggaran {}, anggaran {}, **laba bersih {}**.".format(
                int(ringkas["total_target_unit"]), rp(ringkas["total_omzet"]), rp(ringkas["total_laba_kotor"]),
                rp(ringkas["total_anggaran"]), rp(ringkas["laba_bersih_kampanye"])))
    L.append("")
    L.append("Dasar hitung: margin = laba ÷ uang yang dibayar pembeli. Biaya platform {}. Pembulatan: harga promo dari "
             "diskon % dibulatkan ke atas; klaim diskon dibulatkan ke bawah; tampilan Rupiah dibulatkan ke rupiah terdekat.".format(
                 meta))
    return "\n".join(L)


# ---------------------------------------------------------------- jadwal
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN_ID = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
            "Oktober", "November", "Desember"]
TANGGAL_KEMBAR = {"1.1": (1, 1), "2.2": (2, 2), "3.3": (3, 3), "4.4": (4, 4), "5.5": (5, 5), "6.6": (6, 6),
                  "7.7": (7, 7), "8.8": (8, 8), "9.9": (9, 9), "10.10": (10, 10), "11.11": (11, 11),
                  "12.12": (12, 12), "harbolnas": (12, 12), "tahun-baru": (1, 1), "tahunbaru": (1, 1)}
FASE = [
    (-14, "Persiapan", "Tetapkan produk & mekanisme, cek margin (subperintah margin), pesan stok & bahan kemasan, daftar kampanye di Seller Center bila ada."),
    (-7, "Pemanasan (teaser)", "Umumkan tanggal promo, ajak simpan/wishlist produk & ikuti toko; siapkan materi foto/video."),
    (-3, "Pengingat", "Bagikan voucher yang bisa diklaim lebih dulu; broadcast ke pelanggan yang sudah setuju menerima pesan."),
    (-1, "Hitung mundur", "Pengingat terakhir + jam mulai; cek stok, harga, dan kuota flash sale sudah benar di sistem."),
    (0, "HARI H", "Promo berjalan; pantau stok & chat tiap 2–3 jam; live/story di jam ramai; jangan ubah syarat di tengah jalan."),
    (1, "Perpanjangan terbatas (opsional)", "Hanya jika sejak awal diumumkan; kalau tidak, akhiri tepat waktu."),
    (3, "Kirim & layani", "Selesaikan pengiriman pesanan promo; balas ulasan & komplain."),
    (7, "Evaluasi", "Bandingkan target vs realisasi (unit, laba, anggaran); catat pelajaran untuk momen berikutnya."),
]


FASE_LEBARAN = [
    (-30, "Persiapan besar", "Hitung margin, pesan stok/bahan hampers & kemasan, tetapkan batas pre-order; ingat stok pemasok ikut tutup saat libur."),
    (-21, "Pre-order & pemanasan", "Buka pre-order hampers/paket Lebaran; konten persiapan Ramadan/Lebaran yang sopan."),
    (-14, "THR mulai cair (umumnya paling lambat H-7)", "Promo utama & bundling; ingatkan batas pesan. THR wajib dibayar paling lambat H-7 (cek surat edaran Kemnaker tahun berjalan)."),
    (-10, "Batas kirim antarkota", "Umumkan batas akhir pengiriman antarkota — tanyakan jadwal operasional kurir yang dipakai, jangan menebak."),
    (-7, "Puncak belanja", "Flash sale/pengingat terakhir untuk kiriman antarkota; siapkan pengiriman instan dalam kota."),
    (-3, "Last call dalam kota", "Hanya pengiriman instan/ambil sendiri; informasikan jadwal libur toko."),
    (0, "HARI RAYA", "Ucapan hari raya tanpa jualan keras."),
    (3, "Toko buka kembali", "Info jadwal kirim & balas chat yang tertunda; balas ulasan."),
    (14, "Evaluasi", "Bandingkan target vs realisasi, catat stok sisa & pelajaran untuk tahun depan."),
]
FASE_KILAT = [
    (-3, "Persiapan kilat", "Cek margin, stok, dan harga di sistem; siapkan 1–2 materi promo sederhana."),
    (-1, "Pengumuman", "Umumkan promo + jam mulai ke pelanggan yang setuju menerima pesan."),
    (0, "HARI H", "Promo berjalan; pantau stok & chat."),
    (3, "Evaluasi", "Target vs realisasi."),
]
FASE_PANJANG = [
    (-30, "Persiapan", "Hitung margin, pesan stok (ukuran/varian lengkap), siapkan foto & bundling kebutuhan."),
    (-21, "Pemanasan", "Konten daftar kebutuhan/tips; buka pre-order bila perlu."),
    (-14, "Promo utama dibuka", "Bundling & diskon mulai; pengingat gajian/THR bila bertepatan."),
    (-7, "Puncak", "Pengingat batas kirim agar barang tiba sebelum hari H."),
    (0, "HARI H", "Sisa stok, promo last call untuk yang terlambat."),
    (7, "Pasca", "Layani penukaran ukuran/retur, balas ulasan."),
    (14, "Evaluasi", "Target vs realisasi, stok sisa, pelajaran."),
]


def parse_tanggal_iso(teks, nama):
    try:
        y, m, d = (int(x) for x in str(teks).strip().split("-"))
        return date(y, m, d)
    except (ValueError, TypeError):
        raise GalatInput("{} '{}' harus berformat YYYY-MM-DD, mis. 2026-11-11".format(nama, teks))


def fmt_tgl(d):
    return "{}, {} {} {}".format(HARI[d.weekday()], d.day, BULAN_ID[d.month], d.year)


def buat_jadwal(args):
    dari = parse_tanggal_iso(args.dari, "--dari") if args.dari else date.today()
    kunci = (args.momen or "").strip().lower()
    catatan = []
    if args.tanggal:
        hari_h = parse_tanggal_iso(args.tanggal, "--tanggal")
        nama = args.momen or "Momen"
    elif kunci in TANGGAL_KEMBAR:
        bl, tg = TANGGAL_KEMBAR[kunci]
        hari_h = date(dari.year, bl, tg)
        if hari_h < dari:
            hari_h = date(dari.year + 1, bl, tg)
        nama = {"harbolnas": "12.12 Harbolnas", "tahun-baru": "Tahun Baru", "tahunbaru": "Tahun Baru"}.get(kunci, args.momen)
        if kunci in ("12.12", "harbolnas"):
            catatan.append("Harbolnas biasanya berpusat di 12.12; tanggal & mekanisme resmi tiap tahun bisa berbeda — cek pengumuman panitia/marketplace.")
    elif kunci == "gajian":
        tg = args.tanggal_gajian
        if not 1 <= tg <= 28:
            raise GalatInput("--tanggal-gajian harus 1–28")
        hari_h = date(dari.year, dari.month, tg)
        if (hari_h - dari).days < 7:
            if hari_h >= dari:
                catatan.append("Gajian tgl {} bulan ini tinggal {} hari: linimasa memakai bulan berikutnya. Untuk promo "
                               "bulan ini, pakai versi kilat (--tanggal {} --pola kilat).".format(
                                   tg, (hari_h - dari).days, hari_h.isoformat()))
            hari_h = date(dari.year + (dari.month == 12), dari.month % 12 + 1, tg)
        nama = "Gajian (tgl {})".format(tg)
        catatan.append("Tanggal gajian berbeda per target pembeli (swasta sering tgl 25/akhir bulan, ASN awal bulan) — sesuaikan.")
    elif kunci in ("ramadan", "lebaran", "idulfitri", "imlek", "back-to-school", "tahun-ajaran"):
        raise GalatInput("tanggal '{}' berubah tiap tahun — isi --tanggal YYYY-MM-DD sesuai SKB 3 Menteri/kalender "
                         "sekolah (atau tanggal perkiraan yang diberi label).".format(args.momen))
    else:
        raise GalatInput("momen '{}' tidak dikenal. Pakai 9.9, 10.10, 11.11, 12.12, harbolnas, tahun-baru, gajian, "
                         "atau isi --tanggal YYYY-MM-DD untuk momen lain.".format(args.momen))
    if hari_h < dari:
        catatan.append("Tanggal momen sudah lewat dari tanggal acuan.")
    pola = args.pola
    if pola == "auto":
        nm = (args.momen or "").lower()
        if re.search(r"lebaran|idul\s*fitri|idulfitri|ramadan|hari\s*raya", nm):
            pola = "lebaran"
        elif re.search(r"sekolah|ajaran|school", nm):
            pola = "panjang"
        else:
            pola = "standar"
    fase_dipakai = {"standar": FASE, "lebaran": FASE_LEBARAN, "panjang": FASE_PANJANG, "kilat": FASE_KILAT}[pola]
    akhir = hari_h
    if args.sampai:
        akhir = parse_tanggal_iso(args.sampai, "--sampai")
        if akhir < hari_h:
            raise GalatInput("--sampai tidak boleh sebelum hari H")
        if (akhir - hari_h).days > 31:
            raise GalatInput("rentang promo lebih dari 31 hari — pecah menjadi beberapa kampanye")
    if pola == "lebaran":
        catatan.append("Tanggal Ramadan/Idulfitri mengikuti SKB 3 Menteri & sidang isbat Kemenag; tandai '(perkiraan)' bila belum resmi.")
    baris = []
    for offset, fase, isi in fase_dipakai:
        acuan = akhir if offset > 0 else hari_h
        tgl = acuan + timedelta(days=offset)
        if offset == 0:
            label = "H" if akhir == hari_h else "H (s.d. {})".format(fmt_tgl(akhir))
        elif offset > 0 and akhir != hari_h:
            label = "Selesai+{}".format(offset)
        else:
            label = "H{}{}".format("+" if offset > 0 else "-", abs(offset))
        baris.append({"hari_ke": label, "tanggal": tgl.isoformat(), "tanggal_asli": tgl.isoformat(),
                      "tanggal_teks": fmt_tgl(tgl), "fase": fase, "kegiatan": isi, "sudah_lewat": False, "digeser": False})
    sisa = (hari_h - dari).days
    # fase sebelum hari H yang tanggalnya sudah lewat BENAR-BENAR digeser ke hari tersisa (dari .. H-1), urutan tetap
    lewat = [b for b in baris if b["tanggal"] < dari.isoformat() and b["tanggal"] < hari_h.isoformat()]
    if lewat and sisa >= 1:
        k = len(lewat)
        berikut = [b["tanggal"] for b in baris if dari.isoformat() <= b["tanggal"] < hari_h.isoformat()]
        batas = min([date.fromisoformat(t) for t in berikut] + [hari_h])
        jendela = max((batas - dari).days, 1)
        for i, b in enumerate(lewat):
            baru = dari + timedelta(days=(i * jendela) // k)
            b.update({"tanggal": baru.isoformat(), "tanggal_teks": fmt_tgl(baru), "digeser": True})
        catatan.append("Sisa waktu hanya {} hari: {} fase persiapan yang tanggal aslinya sudah lewat DIGESER ke "
                       "{} s.d. {} (urutan tetap; kerjakan lebih ringkas).".format(
                           sisa, k, fmt_tgl(dari), fmt_tgl(hari_h - timedelta(days=1))))
    elif lewat:
        catatan.append("Hari H sudah hari ini/lewat: fase persiapan tidak bisa dijalankan sesuai jadwal.")
    for b in baris:
        b["sudah_lewat"] = b["tanggal"] < dari.isoformat()
    return {"momen": nama, "pola": pola, "hari_h": hari_h.isoformat(), "sampai": akhir.isoformat(), "hari_h_teks": fmt_tgl(hari_h),
            "tanggal_acuan": dari.isoformat(), "sisa_hari": sisa, "linimasa": baris, "catatan": catatan}


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Cek margin promo & jadwal kampanye momen belanja.")
    sub = ap.add_subparsers(dest="perintah")
    m = sub.add_parser("margin", help="Cek margin sebelum/sesudah promo")
    m.add_argument("--config", help="File JSON/CSV berisi banyak produk (lihat templates/)")
    m.add_argument("--produk", default="Produk")
    m.add_argument("--harga-normal")
    m.add_argument("--hpp", help="Modal per unit (HPP), termasuk kemasan")
    m.add_argument("--diskon-persen")
    m.add_argument("--harga-promo", help="Harga promo/flash sale per unit")
    m.add_argument("--potongan-rp", help="Potongan Rp per unit")
    m.add_argument("--bundling", help="Paket, mis. \"3=Rp 229.000\"")
    m.add_argument("--beli-gratis", help="mis. \"2+1\" (beli 2 gratis 1)")
    m.add_argument("--voucher", help="Voucher per pesanan: \"10.000\" atau \"10%%\"")
    m.add_argument("--maks-voucher")
    m.add_argument("--min-belanja")
    m.add_argument("--subsidi-ongkir", help="Ongkir yang ditanggung penjual per pesanan (Rp)")
    m.add_argument("--cashback", help="Cashback yang ditanggung penjual (%% dari yang dibayar pembeli)")
    m.add_argument("--biaya-platform", help="Total %% potongan marketplace (admin+layanan+pembayaran), isi dari Seller Center")
    m.add_argument("--biaya-per-pesanan", help="Biaya tetap per pesanan (Rp)")
    m.add_argument("--biaya-lain", help="Biaya promo tambahan per unit, mis. hadiah/kemasan khusus (Rp)")
    m.add_argument("--item-per-pesanan", help="Unit per pesanan untuk simulasi (default 1, atau isi paket)")
    m.add_argument("--target-unit")
    m.add_argument("--unit-normal", help="Penjualan biasa (unit) pada periode sepanjang promo, untuk pembanding")
    m.add_argument("--anggaran", help="Anggaran tetap kampanye: iklan, materi, dll. (Rp)")
    m.add_argument("--bulatkan", help="Kelipatan pembulatan harga promo dari diskon %% (default 100)")
    m.add_argument("--batas-tipis", default="10", help="Margin minimum yang dianggap aman (%%, default 10)")
    m.add_argument("--format", choices=["teks", "json"], default="teks")
    j = sub.add_parser("jadwal", help="Linimasa kampanye H-14 s.d. H+7")
    j.add_argument("--momen", required=True, help="9.9, 10.10, 11.11, 12.12, harbolnas, tahun-baru, gajian, atau nama bebas + --tanggal")
    j.add_argument("--tanggal", help="Tanggal hari H (YYYY-MM-DD) untuk momen yang tanggalnya berubah")
    j.add_argument("--tanggal-gajian", type=int, default=25)
    j.add_argument("--dari", help="Tanggal acuan (YYYY-MM-DD), default hari ini")
    j.add_argument("--pola", choices=["auto", "standar", "lebaran", "panjang", "kilat"], default="auto",
                   help="standar H-14..H+7; lebaran H-30..H+14; panjang (back to school) H-30..H+14; kilat H-3..H+3")
    j.add_argument("--sampai", help="Tanggal akhir promo (YYYY-MM-DD) untuk promo beberapa hari; fase sesudah H dihitung dari tanggal ini")
    j.add_argument("--format", choices=["teks", "json"], default="teks")
    args = ap.parse_args()
    if not args.perintah:
        ap.print_help()
        sys.exit(2)
    try:
        if args.perintah == "jadwal":
            h = buat_jadwal(args)
            if args.format == "json":
                print(json.dumps(h, ensure_ascii=False, indent=2))
            else:
                print("### Linimasa kampanye {} — hari H {}".format(h["momen"], h["hari_h_teks"]))
                print("| Hari | Tanggal | Fase | Kegiatan |")
                print("|---|---|---|---|")
                for b in h["linimasa"]:
                    ket = " (digeser dari {})".format(b["tanggal_asli"]) if b["digeser"] else (" (sudah lewat)" if b["sudah_lewat"] else "")
                    print("| {} | {}{} | {} | {} |".format(b["hari_ke"], b["tanggal_teks"], ket, b["fase"], b["kegiatan"]))
                for c in h["catatan"]:
                    print("- Catatan: " + c)
            return
        batas = parse_angka(args.batas_tipis, "--batas-tipis")
        if not NOL <= batas < SERATUS:
            raise GalatInput("--batas-tipis harus 0 sampai di bawah 100")
        if args.config:
            data = baca_config(args.config)
            umum = {k: v for k, v in data.items() if k != "produk"}
            produk_cfg = []
            for i, r in enumerate(data["produk"], 1):
                if not isinstance(r, dict):
                    raise GalatInput("produk ke-{} harus berupa objek".format(i))
                gabung = dict((k, v) for k, v in umum.items() if k not in ("anggaran_kampanye",))
                gabung.update({k: v for k, v in r.items() if v not in (None, "")})
                produk_cfg.append(gabung)
            anggaran_kampanye = opsional(umum.get("anggaran_kampanye"), "anggaran_kampanye", NOL)
        else:
            if args.harga_normal is None or args.hpp is None:
                raise GalatInput("isi --harga-normal dan --hpp (atau pakai --config file)")
            produk_cfg = [{k: getattr(args, k) for k in (
                "produk", "harga_normal", "hpp", "diskon_persen", "harga_promo", "potongan_rp", "bundling",
                "beli_gratis", "voucher", "maks_voucher", "min_belanja", "subsidi_ongkir", "cashback",
                "biaya_platform", "biaya_per_pesanan", "biaya_lain", "item_per_pesanan", "target_unit",
                "unit_normal", "anggaran", "bulatkan")}]
            anggaran_kampanye = NOL
            umum = {}
        hasil = [analisis_produk(siapkan_produk(c, "Produk {}".format(i)), batas) for i, c in enumerate(produk_cfg, 1)]
        ringkas = None
        nama_c = Counter(h["produk"].strip().lower() for h in hasil)
        mode_opsi = (args.config and str(umum.get("bandingkan", "")).lower() in ("true", "1", "ya", "yes")) or \
            any(v > 1 for v in nama_c.values())
        if mode_opsi and len(hasil) > 1:
            ringkas = {"jumlah_produk": len(hasil), "mode": "perbandingan_opsi",
                       "status": {s: sum(1 for h in hasil if h["status"] == s) for s in ("RUGI", "TIPIS", "AMAN")},
                       "catatan": "Ada beberapa opsi untuk produk yang sama (atau \"bandingkan\": true): total TIDAK dijumlah. "
                                  "Pilih satu opsi per produk, lalu jalankan ulang untuk rencana final."}
        elif len(hasil) > 1 or anggaran_kampanye > 0:
            tot_unit = sum((h["kampanye"]["target_unit"] for h in hasil if "kampanye" in h and "target_unit" in h["kampanye"]), NOL)
            ringkas = {"jumlah_produk": len(hasil),
                       "status": {s: sum(1 for h in hasil if h["status"] == s) for s in ("RUGI", "TIPIS", "AMAN")}}
            if tot_unit:
                tk = sum((h["kampanye"]["laba_kotor_promo"] for h in hasil if "kampanye" in h and "target_unit" in h["kampanye"]), NOL)
                ta = sum((h["kampanye"]["anggaran"] for h in hasil if "kampanye" in h), NOL) + anggaran_kampanye
                ringkas.update({"total_target_unit": tot_unit,
                                "total_omzet": sum((h["kampanye"]["omzet_dibayar_pembeli"] for h in hasil if "kampanye" in h and "target_unit" in h["kampanye"]), NOL),
                                "total_laba_kotor": tk, "total_anggaran": ta, "laba_bersih_kampanye": tk - ta})
        biaya_meta = "diisi pengguna (cek Seller Center)" if any(h["normal"]["biaya_platform"] for h in hasil) \
            else "TIDAK dihitung (0%) — jika jualan di marketplace, isi --biaya-platform"
        if args.format == "json":
            print(json.dumps(ke_json({"versi_script": VERSI, "batas_margin_aman_persen": batas, "produk": hasil,
                                      "ringkasan": ringkas, "biaya_platform": biaya_meta,
                                      "peringatan_input": PERINGATAN_INPUT}), ensure_ascii=False, indent=2))
        else:
            print(cetak_margin(hasil, ringkas, batas, biaya_meta))
            for w in PERINGATAN_INPUT:
                print("PERINGATAN INPUT: " + w)
    except GalatInput as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
