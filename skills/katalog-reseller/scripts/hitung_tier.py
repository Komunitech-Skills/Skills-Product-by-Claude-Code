#!/usr/bin/env python3
"""Hitung daftar harga bertingkat reseller/dropshipper/agen dari HPP & target margin produsen
(atau dari harga eceran + diskon per tier), lalu cek margin yang tersisa untuk reseller.

Per produk & tier menghasilkan:
- harga mitra per unit, diskon dari harga eceran anjuran (HET/SRP)
- margin produsen (Rp & %), untung mitra per unit bila menjual di harga eceran dan di harga minimum anjuran
- contoh untung per paket minimal order (untuk pesan rekrut yang jujur)
- peringatan: produsen rugi/tipis, margin mitra tipis, urutan tier tidak masuk akal, selisih tier terlalu kecil

Dua mode:
  margin : harga tier = (HPP + biaya produsen) / (1 - target margin produsen)  -> dibulatkan KE ATAS
           (margin produsen tidak pernah di bawah target).
  diskon : harga tier = harga eceran x (1 - diskon tier)                        -> dibulatkan KE BAWAH
           (diskon yang diterima mitra tidak pernah lebih kecil dari yang dijanjikan).
Harga eceran anjuran boleh dikosongkan di mode margin: script menurunkannya dari tier termahal agar
mitra tier itu mendapat --target-margin-mitra (dibulatkan KE ATAS ke kelipatan --bulatkan-eceran).

Tidak ada bonus rekrut/jenjang: script hanya menghitung harga jual-beli barang.
Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 hitung_tier.py --produk "Serum 20ml" --hpp 28.000 --eceran 89.000 --mode diskon \
      --tier "Dropshipper:1:15" --tier "Reseller:12:25" --tier "Agen:60:35"
  python3 hitung_tier.py --produk "Kopi 250g" --hpp 32.000 --mode margin \
      --tier "Dropshipper:1:45" --tier "Reseller:10:35" --tier "Agen:50:25"
  python3 hitung_tier.py --config produk.json --csv-keluar ~/folder-kerja/daftar-harga-mitra.csv
"""
import argparse
import csv
import io
import json
import os
import re
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

VERSI = "1.0.5"
NOL = Decimal(0)
SERATUS = Decimal(100)
TIER_DEFAULT = {"diskon": ["Dropshipper:1:20", "Reseller:12:25", "Agen:60:35"],
                "margin": ["Dropshipper:1:45", "Reseller:12:35", "Agen:60:25"]}


class GalatInput(Exception):
    pass


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
        raise GalatInput("{}: '{}' bukan angka yang valid. Contoh yang benar: 28000, \"Rp 28.000\", 28rb, 12,5".format(nama, asli))

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
    return ("-Rp " if d < 0 else "Rp ") + "{:,}".format(abs(int(d))).replace(",", ".")


def persen(d):
    return "{:f}".format(Decimal(d).quantize(Decimal("0.1"), ROUND_HALF_UP)).replace(".", ",") + "%"


def bulat(d, kelipatan, arah):
    return (Decimal(d) / kelipatan).to_integral_value(arah) * kelipatan


def ke_json(o):
    if isinstance(o, dict):
        return {k: ke_json(v) for k, v in o.items()}
    if isinstance(o, list):
        return [ke_json(v) for v in o]
    if isinstance(o, Decimal):
        if o == o.to_integral_value():
            return int(o)
        return float(o.quantize(Decimal("0.01"), ROUND_HALF_UP))
    return o


# ---------------------------------------------------------------- tier
def parse_tier(teks, mode):
    if isinstance(teks, dict):
        nama = str(teks.get("nama") or "").strip()
        minq = teks.get("min_beli", teks.get("min_qty"))
        nilai = teks.get("nilai", teks.get("diskon" if mode == "diskon" else "margin"))
        min_mitra = teks.get("min_margin_mitra")
    else:
        bagian = [b.strip() for b in str(teks).split(":")]
        if len(bagian) not in (3, 4):
            raise GalatInput("tier '{}' harus berformat Nama:min_beli:nilai%, mis. \"Reseller:12:25\"".format(teks))
        nama, minq, nilai = bagian[:3]
        min_mitra = bagian[3] if len(bagian) == 4 else None
    if not nama:
        raise GalatInput("nama tier tidak boleh kosong")
    minq = parse_angka(minq, "min beli tier " + nama)
    if minq < 1 or minq != minq.to_integral_value():
        raise GalatInput("min beli tier {} harus bilangan bulat >= 1".format(nama))
    nilai = parse_angka(nilai, "nilai tier " + nama)
    if not NOL <= nilai < SERATUS:
        raise GalatInput("nilai tier {} harus 0 sampai di bawah 100 (persen)".format(nama))
    return {"nama": nama, "min_beli": minq, "nilai": nilai,
            "min_margin_mitra": opsional(min_mitra, "min margin mitra tier " + nama)}


def adalah_dropship(t):
    return "drop" in t["nama"].lower()


def hitung_produk(cfg, tiers, opsi):
    nama = str(cfg.get("produk") or cfg.get("nama") or "Produk").strip()
    lab = "[{}] ".format(nama)
    hpp = parse_angka(cfg.get("hpp"), lab + "HPP")
    if hpp <= 0:
        raise GalatInput(lab + "HPP harus lebih dari 0")
    biaya_prod = opsional(cfg.get("biaya_produsen"), lab + "biaya produsen per unit", opsi["biaya_produsen"])
    eceran = opsional(cfg.get("eceran"), lab + "harga eceran", None)
    fee_mitra = opsional(cfg.get("biaya_jual_mitra"), lab + "biaya jual mitra %", opsi["biaya_jual_mitra"])
    ongkir_mitra = opsional(cfg.get("ongkir_ke_mitra"), lab + "ongkir ke mitra per unit", opsi["ongkir_ke_mitra"])
    maks_bawah = opsional(cfg.get("maks_diskon_konsumen"), lab + "maks diskon konsumen %", opsi["maks_diskon_konsumen"])
    for k, v in (("biaya produsen", biaya_prod), ("ongkir ke mitra", ongkir_mitra)):
        if v < 0:
            raise GalatInput(lab + k + " tidak boleh negatif")
    for k, v in (("biaya jual mitra", fee_mitra), ("maks diskon konsumen", maks_bawah)):
        if not NOL <= v < SERATUS:
            raise GalatInput(lab + k + " harus 0 sampai di bawah 100%")
    mode = opsi["mode"]
    modal = hpp + biaya_prod
    catatan, peringatan = [], []

    harga = []
    for t in tiers:
        if mode == "margin":
            mentah = modal / (1 - t["nilai"] / SERATUS)
            h = bulat(mentah, opsi["bulatkan"], ROUND_CEILING)
        else:
            if eceran is None:
                raise GalatInput(lab + "mode diskon butuh harga eceran (--eceran)")
            mentah = eceran * (1 - t["nilai"] / SERATUS)
            h = bulat(mentah, opsi["bulatkan"], ROUND_FLOOR)
        harga.append(h)

    if eceran is None:
        i_max = max(range(len(harga)), key=lambda i: harga[i])
        tertinggi = harga[i_max]
        o_max = NOL if adalah_dropship(tiers[i_max]) else ongkir_mitra
        tm = opsi["target_margin_mitra"]
        if tm + fee_mitra >= SERATUS:
            raise GalatInput(lab + "target margin mitra + biaya jual mitra harus di bawah 100%")
        # E = (harga tier termahal + ongkir) / (1 - target margin bersih mitra - biaya jual mitra)
        eceran = bulat((tertinggi + o_max) / (1 - tm / SERATUS - fee_mitra / SERATUS), opsi["bulatkan_eceran"], ROUND_CEILING)
        catatan.append("Harga eceran anjuran tidak diisi: diturunkan dari harga tier termahal ({}, tier {}) agar mitra tier itu "
                       "mendapat ±{} BERSIH setelah biaya jual {} dan ongkir {}; rumus (harga + ongkir) ÷ (1 − target − biaya jual), "
                       "dibulatkan ke atas ke kelipatan {} → {}.".format(
                           rp(tertinggi), tiers[i_max]["nama"], persen(tm), persen(fee_mitra), rp(o_max),
                           rp(opsi["bulatkan_eceran"]), rp(eceran)))
        eceran_diturunkan = True
    else:
        eceran_diturunkan = False
        if eceran <= 0:
            raise GalatInput(lab + "harga eceran harus lebih dari 0")
    harga_min = bulat(eceran * (1 - maks_bawah / SERATUS), Decimal(100), ROUND_FLOOR) if maks_bawah > 0 else eceran

    baris = []
    for t, h in zip(tiers, harga):
        ongkir_t = NOL if adalah_dropship(t) else ongkir_mitra  # dropshipper tidak menerima kiriman stok
        m_prod = h - modal
        m_prod_p = m_prod / h * SERATUS if h > 0 else None
        fee = eceran * fee_mitra / SERATUS
        untung = eceran - h - fee - ongkir_t
        untung_p = untung / eceran * SERATUS
        fee_min = harga_min * fee_mitra / SERATUS
        untung_min = harga_min - h - fee_min - ongkir_t
        batas = t["min_margin_mitra"]
        if batas is None:
            batas = opsi["min_margin_dropship"] if adalah_dropship(t) else opsi["min_margin_mitra"]
        status = []
        if m_prod < 0:
            status.append("PRODUSEN RUGI")
        elif m_prod_p < opsi["min_margin_produsen"]:
            status.append("MARGIN PRODUSEN TIPIS")
        if h >= eceran:
            status.append("HARGA MITRA ≥ ECERAN")
        elif untung <= 0:
            status.append("MITRA RUGI")
        elif untung_p < batas:
            status.append("MARGIN MITRA TIPIS")
        if untung_min <= 0 and h < eceran:
            status.append("RUGI DI HARGA MINIMUM")
        baris.append({
            "tier": t["nama"], "min_beli": t["min_beli"], "harga_mitra": h,
            "diskon_dari_eceran_persen": (1 - h / eceran) * SERATUS,
            "margin_produsen_rp": m_prod, "margin_produsen_persen": m_prod_p,
            "untung_mitra_per_unit_di_eceran": untung, "untung_mitra_persen": untung_p,
            "untung_mitra_per_unit_di_harga_minimum": untung_min,
            "batas_margin_mitra_persen": batas, "ongkir_ke_mitra_dihitung": ongkir_t,
            "modal_mitra_min_order": h * t["min_beli"],
            "contoh_untung_min_order_di_eceran": untung * t["min_beli"],
            "status": status or ["AMAN"],
        })
        if status:
            pesan = {
                "PRODUSEN RUGI": "harga mitra {} di bawah modal produsen {}".format(rp(h), rp(modal)),
                "MARGIN PRODUSEN TIPIS": "margin produsen {} di bawah batas {}".format(persen(m_prod_p), persen(opsi["min_margin_produsen"])),
                "HARGA MITRA ≥ ECERAN": "harga mitra {} tidak lebih murah dari harga eceran {}".format(rp(h), rp(eceran)),
                "MITRA RUGI": "mitra rugi {} per unit bila menjual di harga eceran".format(rp(-untung)),
                "MARGIN MITRA TIPIS": "untung mitra {} ({}) di bawah batas {} — mitra sulit bertahan/terdorong banting harga".format(
                    rp(untung), persen(untung_p), persen(batas)),
                "RUGI DI HARGA MINIMUM": "jika mitra menjual di harga minimum {}, untungnya {} (tidak ada ruang diskon)".format(
                    rp(harga_min), rp(untung_min)),
            }
            for s in status:
                peringatan.append("Tier {}: {}.".format(t["nama"], pesan[s]))

    # konsistensi antar tier (urut min_beli)
    urut = sorted(baris, key=lambda b: b["min_beli"])
    for a, b in zip(urut, urut[1:]):
        if a["min_beli"] == b["min_beli"]:
            peringatan.append("Tier {} dan {} punya minimal beli sama ({}).".format(a["tier"], b["tier"], int(a["min_beli"])))
        elif a["harga_mitra"] == b["harga_mitra"]:
            peringatan.append("Tier {} dan {} punya harga mitra SAMA ({}) setelah pembulatan: tidak ada alasan naik tier. "
                              "Bedakan diskon/margin-nya.".format(a["tier"], b["tier"], rp(a["harga_mitra"])))
        elif b["harga_mitra"] > a["harga_mitra"]:
            peringatan.append("Tier {} (beli ≥ {}) lebih MAHAL dari tier {} (beli ≥ {}). Tier dengan pembelian lebih banyak "
                              "harus lebih murah.".format(b["tier"], int(b["min_beli"]), a["tier"], int(a["min_beli"])))
        elif a["harga_mitra"] > 0 and (a["harga_mitra"] - b["harga_mitra"]) / a["harga_mitra"] * SERATUS < opsi["selisih_min_tier"]:
            peringatan.append("Selisih harga {} → {} hanya {} (< {}): kurang menarik untuk naik tier.".format(
                a["tier"], b["tier"], persen((a["harga_mitra"] - b["harga_mitra"]) / a["harga_mitra"] * SERATUS),
                persen(opsi["selisih_min_tier"])))

    ruang = eceran - modal - eceran * fee_mitra / SERATUS - ongkir_mitra
    ruang_p = ruang / eceran * SERATUS
    if ruang_p < opsi["min_margin_produsen"] + opsi["min_margin_mitra"]:
        peringatan.append("Ruang harga total (eceran − modal − biaya jual − ongkir) hanya {} ({} dari eceran): tidak cukup "
                          "untuk margin produsen {} + mitra {}. Pertimbangkan menaikkan harga eceran, menekan HPP, atau "
                          "tidak membuka tier mitra untuk produk ini.".format(rp(ruang), persen(ruang_p),
                                                                          persen(opsi["min_margin_produsen"]),
                                                                          persen(opsi["min_margin_mitra"])))
    if fee_mitra == 0:
        catatan.append("Biaya jual mitra 0%: jika mitra berjualan di marketplace, untung bersihnya lebih kecil "
                       "(isi --biaya-jual-mitra dari Seller Center mitra).")
    return {"produk": nama, "hpp": hpp, "biaya_produsen_per_unit": biaya_prod, "modal_produsen": modal,
            "harga_eceran_anjuran": eceran, "harga_eceran_diturunkan_script": eceran_diturunkan,
            "harga_minimum_anjuran": harga_min, "maks_diskon_konsumen_persen": maks_bawah,
            "ruang_harga_total": ruang, "ruang_harga_total_persen": ruang_p,
            "biaya_jual_mitra_persen": fee_mitra, "ongkir_ke_mitra_per_unit": ongkir_mitra,
            "tier": baris, "catatan": catatan, "peringatan": peringatan}


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
            raise GalatInput("JSON harus berisi daftar \"produk\" (lihat templates/produk-contoh.json)")
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


def tulis_csv(path, hasil):
    """Daftar harga untuk DIBAGIKAN ke mitra: tanpa HPP & margin produsen."""
    try:
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            fees = sorted({persen(h["biaya_jual_mitra_persen"]) for h in hasil})
            ongk = sorted({rp(h["ongkir_ke_mitra_per_unit"]) for h in hasil})
            w.writerow(["Produk", "Tier", "Minimal beli", "Harga mitra per unit", "Harga eceran anjuran",
                        "Harga minimum anjuran",
                        "Perkiraan untung per unit di harga eceran (setelah potongan jualan {} & ongkir {}/unit; dropshipper tanpa ongkir)".format(
                            "/".join(fees), "/".join(ongk)),
                        "Modal minimal order"])
            for h in hasil:
                for b in h["tier"]:
                    w.writerow([h["produk"], b["tier"], int(b["min_beli"]), rp(b["harga_mitra"]),
                                rp(h["harga_eceran_anjuran"]), rp(h["harga_minimum_anjuran"]),
                                rp(b["untung_mitra_per_unit_di_eceran"]), rp(b["modal_mitra_min_order"])])
            w.writerow([])
            w.writerow(["Catatan: untung adalah perkiraan bila semua barang terjual di harga eceran anjuran; bukan jaminan penghasilan. "
                        "Potongan jualan = perkiraan biaya marketplace (cek Seller Center masing-masing)."])
    except OSError as e:
        raise GalatInput("gagal menulis '{}' ({})".format(path, e.strerror))


def cetak_teks(hasil, opsi):
    L = []
    for h in hasil:
        L.append("### {} — HPP {}{} | harga eceran anjuran {}{} | harga minimum anjuran {}".format(
            h["produk"], rp(h["hpp"]),
            " + biaya produsen {}".format(rp(h["biaya_produsen_per_unit"])) if h["biaya_produsen_per_unit"] else "",
            rp(h["harga_eceran_anjuran"]), " (usulan script)" if h["harga_eceran_diturunkan_script"] else "",
            rp(h["harga_minimum_anjuran"])))
        L.append("| Tier | Min. beli | Harga mitra/unit | Diskon dari eceran | Margin produsen | Untung mitra/unit (di eceran) | Untung di harga min. | Status |")
        L.append("|---|---|---|---|---|---|---|---|")
        for b in h["tier"]:
            L.append("| {} | {} pcs | {} | {} | {} ({}) | {} ({}) | {} | {} |".format(
                b["tier"], int(b["min_beli"]), rp(b["harga_mitra"]), persen(b["diskon_dari_eceran_persen"]),
                rp(b["margin_produsen_rp"]), persen(b["margin_produsen_persen"]) if b["margin_produsen_persen"] is not None else "-",
                rp(b["untung_mitra_per_unit_di_eceran"]), persen(b["untung_mitra_persen"]),
                rp(b["untung_mitra_per_unit_di_harga_minimum"]), ", ".join(b["status"])))
        L.append("")
        for b in h["tier"]:
            L.append("- Contoh {}: beli {} pcs = modal {}; jika semua terjual di harga eceran, untung ±{}.".format(
                b["tier"], int(b["min_beli"]), rp(b["modal_mitra_min_order"]), rp(b["contoh_untung_min_order_di_eceran"])))
        if h["biaya_jual_mitra_persen"] or h["ongkir_ke_mitra_per_unit"]:
            L.append("- Untung mitra sudah dikurangi biaya jual {} dan ongkir ke mitra {}/unit (ongkir tidak dikenakan ke tier dropshipper).".format(
                persen(h["biaya_jual_mitra_persen"]), rp(h["ongkir_ke_mitra_per_unit"])))
        for c in h["catatan"]:
            L.append("- Catatan: " + c)
        for w in h["peringatan"]:
            L.append("- PERINGATAN: " + w)
        L.append("")
    L.append("Dasar hitung: mode {}. {} Margin produsen = (harga mitra − HPP − biaya produsen) ÷ harga mitra. "
             "Untung mitra = harga jual − harga mitra − biaya jual − ongkir ke mitra; % dari harga eceran. "
             "Harga minimum anjuran dibulatkan ke bawah ke kelipatan Rp 100.".format(
                 opsi["mode"],
                 "Harga tier dibulatkan KE ATAS ke kelipatan {} (margin produsen ≥ target).".format(rp(opsi["bulatkan"]))
                 if opsi["mode"] == "margin" else
                 "Harga tier dibulatkan KE BAWAH ke kelipatan {} (diskon mitra ≥ yang dijanjikan).".format(rp(opsi["bulatkan"]))))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Hitung harga bertingkat reseller/dropshipper/agen & cek margin mitra.")
    ap.add_argument("--config", help="File JSON/CSV banyak produk (lihat templates/)")
    ap.add_argument("--produk", default="Produk")
    ap.add_argument("--hpp", help="Modal per unit (HPP)")
    ap.add_argument("--eceran", help="Harga eceran anjuran ke konsumen (HET/SRP)")
    ap.add_argument("--mode", choices=["diskon", "margin"], help="diskon: dari harga eceran; margin: dari HPP (default: diskon jika --eceran ada)")
    ap.add_argument("--tier", action="append", help="Nama:min_beli:nilai%%[:min_margin_mitra%%], bisa diulang")
    ap.add_argument("--biaya-produsen", default="0", help="Biaya produsen per unit selain HPP (packing, label, ongkir gudang)")
    ap.add_argument("--biaya-jual-mitra", default="0", help="Perkiraan %% potongan saat mitra menjual (mis. biaya marketplace)")
    ap.add_argument("--ongkir-ke-mitra", default="0", help="Ongkir produsen→mitra per unit yang ditanggung mitra (Rp)")
    ap.add_argument("--maks-diskon-konsumen", default="0", help="Maks. diskon dari harga eceran yang masih diizinkan (%%) → harga minimum anjuran")
    ap.add_argument("--target-margin-mitra", default="20", help="Untuk menurunkan harga eceran bila tidak diisi (%%)")
    ap.add_argument("--min-margin-mitra", default="15", help="Batas untung mitra dianggap tipis (%%, default 15)")
    ap.add_argument("--min-margin-dropship", default="10", help="Batas untuk tier bernama 'drop...' (%%, default 10)")
    ap.add_argument("--min-margin-produsen", default="15", help="Batas margin produsen dianggap tipis (%%, default 15)")
    ap.add_argument("--selisih-min-tier", default="3", help="Selisih harga minimum antar tier (%%)")
    ap.add_argument("--bulatkan", default="100", help="Kelipatan pembulatan harga mitra (default Rp 100)")
    ap.add_argument("--bulatkan-eceran", default="1000", help="Kelipatan pembulatan harga eceran usulan (default Rp 1.000)")
    ap.add_argument("--csv-keluar", help="Tulis daftar harga untuk mitra (tanpa HPP/margin produsen) ke file CSV")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    a = ap.parse_args()
    try:
        opsi = {}
        for k in ("biaya_produsen", "biaya_jual_mitra", "ongkir_ke_mitra", "maks_diskon_konsumen", "target_margin_mitra",
                  "min_margin_mitra", "min_margin_dropship", "min_margin_produsen", "selisih_min_tier",
                  "bulatkan", "bulatkan_eceran"):
            opsi[k] = parse_angka(getattr(a, k), "--" + k.replace("_", "-"))
        if opsi["bulatkan"] <= 0 or opsi["bulatkan_eceran"] <= 0:
            raise GalatInput("kelipatan pembulatan harus lebih dari 0")
        if not NOL <= opsi["target_margin_mitra"] < SERATUS:
            raise GalatInput("--target-margin-mitra harus 0 sampai di bawah 100")
        if a.config:
            data = baca_config(a.config)
            umum = {k: v for k, v in data.items() if k not in ("produk", "tier")}
            for k in ("biaya_produsen", "biaya_jual_mitra", "ongkir_ke_mitra", "maks_diskon_konsumen", "min_margin_mitra",
                      "min_margin_dropship", "min_margin_produsen", "target_margin_mitra"):
                if k in umum and umum[k] not in (None, ""):
                    opsi[k] = parse_angka(umum[k], k)
            mode = a.mode or umum.get("mode")
            tier_mentah = a.tier or data.get("tier")
            produk_cfg = data["produk"]
        else:
            if a.hpp is None:
                raise GalatInput("isi --hpp (modal per unit) atau pakai --config file")
            mode = a.mode
            tier_mentah = a.tier
            produk_cfg = [{"produk": a.produk, "hpp": a.hpp, "eceran": a.eceran}]
        if not mode:
            mode = "diskon" if all((p.get("eceran") not in (None, "")) for p in produk_cfg) else "margin"
        if mode not in ("diskon", "margin"):
            raise GalatInput("mode harus 'diskon' atau 'margin'")
        opsi["mode"] = mode
        tier_default = not tier_mentah
        tiers = [parse_tier(t, mode) for t in (tier_mentah or TIER_DEFAULT[mode])]
        if len({t["nama"].lower() for t in tiers}) != len(tiers):
            raise GalatInput("nama tier tidak boleh kembar")
        hasil = []
        for p in produk_cfg:
            if not isinstance(p, dict):
                raise GalatInput("setiap produk harus berupa objek/baris")
            hasil.append(hitung_produk(p, tiers, opsi))
        if tier_default:
            for h in hasil:
                h["catatan"].insert(0, "Tier memakai CONTOH default ({}) — sesuaikan dengan kebijakanmu.".format(
                    ", ".join(TIER_DEFAULT[mode])))
        if a.csv_keluar:
            a.csv_keluar = os.path.abspath(a.csv_keluar)
            tulis_csv(a.csv_keluar, hasil)
        if a.format == "json":
            print(json.dumps(ke_json({"versi_script": VERSI, "mode": mode, "produk": hasil,
                                      "csv_keluar": a.csv_keluar}), ensure_ascii=False, indent=2))
        else:
            print(cetak_teks(hasil, opsi))
            if a.csv_keluar:
                print("\nDaftar harga untuk mitra (tanpa HPP & margin produsen) disimpan ke: {}".format(a.csv_keluar))
    except GalatInput as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
