#!/usr/bin/env python3
"""Hitung angka promo untuk live jualan: potongan, persen hemat, harga bundling per pcs.

Aturan pembulatan (agar klaim di live SELALU jujur):
- Harga live dari --diskon-persen dibulatkan KE ATAS ke kelipatan --bulatkan (default Rp 1),
  lalu persen hemat dihitung ULANG dari harga akhir (bukan dari persen yang diminta).
- Persen hemat yang boleh diucapkan ("hemat X%") dibulatkan KE BAWAH ke bilangan bulat.
- Harga per pcs bundling dibulatkan KE ATAS ke rupiah penuh (tidak pernah terdengar lebih murah dari aslinya).

Hanya library standar Python 3.8+. Tidak ada akses jaringan.
Contoh:
  python3 hitung_promo.py --harga-normal "Rp 89.000" --harga-live "Rp 69.000"
  python3 hitung_promo.py --harga-normal 89000 --diskon-persen 20 --bulatkan 1000
  python3 hitung_promo.py --harga-normal 89000 --harga-live 69000 --bundling "3=Rp 189.000"
"""
import argparse
import json
import re
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, InvalidOperation

# Windows: pastikan teks Indonesia/emoji tercetak tanpa error encoding
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def parse_angka(teks, nama):
    """Terima '89000', 'Rp 89.000', '89.000,50', '89,000.50', '89rb', '1,5jt'."""
    if teks is None:
        return None
    asli = str(teks)
    s = asli.strip().lower().replace("rp", "").replace(" ", "")
    pengali = Decimal(1)
    m = re.search(r"(rb|ribu|k|jt|juta)$", s)
    if m:
        pengali = Decimal(1000) if m.group(1) in ("rb", "ribu", "k") else Decimal(1000000)
        s = s[: m.start()]
    if not s or re.search(r"[^\d.,\-]", s):
        galat("{} '{}' bukan angka yang valid. Contoh: 89000 atau \"Rp 89.000\".".format(nama, asli))
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        bagian = s.split(",")
        s = s.replace(",", ".") if (len(bagian) == 2 and len(bagian[1]) != 3) else s.replace(",", "")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3 and pengali == 1):
        s = s.replace(".", "")
    try:
        return Decimal(s) * pengali
    except InvalidOperation:
        galat("{} '{}' bukan angka yang valid.".format(nama, asli))


def rp(x):
    """Format Rupiah Indonesia. Angka pecahan (jarang) ditampilkan 2 desimal apa adanya, tidak dibulatkan."""
    x = Decimal(x)
    if x == x.to_integral_value():
        return "Rp " + "{:,.0f}".format(x).replace(",", ".")
    t = "{:,.2f}".format(x.quantize(Decimal("0.01"), rounding=ROUND_FLOOR))
    return "Rp " + t.replace(",", "_").replace(".", ",").replace("_", ".")


def bulat_atas(x, kelipatan):
    return (x / kelipatan).quantize(Decimal(1), rounding=ROUND_CEILING) * kelipatan


def persen_turun(bagian, total):
    if total == 0:
        return Decimal(0)
    return (bagian / total * 100).quantize(Decimal(1), rounding=ROUND_FLOOR)


def main():
    p = argparse.ArgumentParser(description="Hitung angka promo live jualan (potongan, persen, bundling).")
    p.add_argument("--nama", default="Produk", help="nama produk (untuk label)")
    p.add_argument("--harga-normal", required=True, help="harga jual normal sebelum promo, mis. \"Rp 89.000\"")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--harga-live", help="harga khusus live, mis. \"Rp 69.000\"")
    g.add_argument("--diskon-persen", help="diskon dalam persen, mis. 20 atau 12,5")
    p.add_argument("--bulatkan", default="1",
                   help="kelipatan pembulatan KE ATAS untuk harga dari --diskon-persen (1, 100, 500, 1000). Default 1")
    p.add_argument("--bundling", action="append", default=[],
                   help="paket isi=harga, mis. \"3=Rp 189.000\". Boleh diulang.")
    p.add_argument("--json", action="store_true", help="keluarkan JSON saja")
    a = p.parse_args()

    normal = parse_angka(a.harga_normal, "Harga normal")
    if normal <= 0:
        galat("Harga normal harus lebih dari 0.")
    kelipatan = parse_angka(a.bulatkan, "Kelipatan pembulatan")
    if kelipatan <= 0:
        galat("--bulatkan harus lebih dari 0.")

    hasil = {"nama": a.nama, "harga_normal": int(normal) if normal == normal.to_integral_value() else float(normal),
             "harga_normal_teks": rp(normal), "peringatan": [], "aturan_pembulatan": (
                 "Harga dari diskon persen dibulatkan ke atas ke kelipatan {}; persen hemat dibulatkan ke bawah; "
                 "harga per pcs bundling dibulatkan ke atas ke rupiah penuh.").format(rp(kelipatan))}

    live = None
    if a.diskon_persen is not None:
        d = parse_angka(a.diskon_persen.replace("%", ""), "Diskon persen")
        if not (0 < d < 100):
            galat("Diskon persen harus di antara 0 dan 100 (tidak termasuk 0 dan 100).")
        mentah = normal * (100 - d) / 100
        live = bulat_atas(mentah, kelipatan)
        hasil["diskon_diminta_persen"] = float(d)
        hasil["harga_live_sebelum_bulat"] = float(mentah.quantize(Decimal("0.01")))
    elif a.harga_live is not None:
        live = parse_angka(a.harga_live, "Harga live")

    if live is not None:
        if live <= 0:
            galat("Harga live harus lebih dari 0.")
        if live >= normal:
            galat("Harga live ({}) tidak lebih murah dari harga normal ({}). Ini bukan promo.".format(rp(live), rp(normal)))
        potongan = normal - live
        pct = persen_turun(potongan, normal)
        hasil.update({
            "harga_live": float(live) if live != live.to_integral_value() else int(live),
            "harga_live_teks": rp(live),
            "potongan": float(potongan) if potongan != potongan.to_integral_value() else int(potongan),
            "potongan_teks": rp(potongan),
            "persen_hemat_boleh_diucapkan": int(pct),
            "kalimat_live": "Harga normal {}, khusus live jadi {} — hemat {}{}.".format(
                rp(normal), rp(live), rp(potongan), " (±{}%)".format(int(pct)) if pct >= 1 else ""),
        })
        if pct >= 50:
            hasil["peringatan"].append(
                "Diskon {}%: pastikan {} benar-benar harga jual yang berlaku sebelumnya, bukan harga yang "
                "dinaikkan dulu untuk dicoret (menyesatkan konsumen, lihat references/etika-promo.md).".format(
                    int(pct), rp(normal)))
        if pct < 1:
            hasil["peringatan"].append("Potongan kurang dari 1% — sebut nominal rupiahnya saja, jangan persen.")

    paket = []
    for b in a.bundling:
        if "=" not in b:
            galat("Format --bundling harus isi=harga, mis. \"3=Rp 189.000\" (dapat: '{}').".format(b))
        isi_t, harga_t = b.split("=", 1)
        try:
            isi = int(isi_t.strip())
        except ValueError:
            galat("Isi paket '{}' harus bilangan bulat, mis. 3.".format(isi_t.strip()))
        if isi < 2:
            galat("Isi paket bundling minimal 2 pcs.")
        harga = parse_angka(harga_t, "Harga paket")
        if harga <= 0:
            galat("Harga paket harus lebih dari 0.")
        per_pcs = harga / isi
        per_pcs_bulat = per_pcs.quantize(Decimal(1), rounding=ROUND_CEILING)
        total_normal = normal * isi
        hemat = total_normal - harga
        item = {
            "isi": isi,
            "harga_paket": int(harga) if harga == harga.to_integral_value() else float(harga),
            "harga_paket_teks": rp(harga),
            "harga_per_pcs_teks": rp(per_pcs_bulat),
            "total_jika_beli_satuan_normal_teks": rp(total_normal),
            "hemat_vs_normal_teks": rp(hemat) if hemat > 0 else "Rp 0",
            "persen_hemat_vs_normal_boleh_diucapkan": int(persen_turun(hemat, total_normal)) if hemat > 0 else 0,
            "kalimat_live": "Paket isi {}: {} saja, jadi cuma {} per pcs — hemat {} dibanding beli satuan harga normal.".format(
                isi, rp(harga), rp(per_pcs_bulat), rp(hemat)) if hemat > 0 else None,
        }
        if hemat <= 0:
            hasil["peringatan"].append("Paket isi {} ({}) TIDAK lebih hemat dari harga normal satuan. Jangan disebut promo.".format(
                isi, rp(harga)))
        elif live is not None and per_pcs > live:
            hasil["peringatan"].append(
                "Paket isi {}: harga per pcs ({}) lebih mahal dari harga live satuan ({}). Penonton bisa merasa dirugikan.".format(
                    isi, rp(per_pcs_bulat), rp(live)))
        paket.append(item)
    if paket:
        hasil["bundling"] = paket
    if live is None and not paket:
        galat("Isi salah satu: --harga-live, --diskon-persen, atau --bundling.")

    if a.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        return
    print("== {} ==".format(a.nama))
    print("Harga normal : {}".format(hasil["harga_normal_teks"]))
    if live is not None:
        print("Harga live   : {}".format(hasil["harga_live_teks"]))
        print("Potongan     : {} (boleh diucapkan: hemat {}%)".format(hasil["potongan_teks"],
                                                                     hasil["persen_hemat_boleh_diucapkan"]))
        print("Kalimat live : " + hasil["kalimat_live"])
    for it in paket:
        print("Paket isi {}  : {} → {} per pcs, hemat {} ({}%) vs normal".format(
            it["isi"], it["harga_paket_teks"], it["harga_per_pcs_teks"], it["hemat_vs_normal_teks"],
            it["persen_hemat_vs_normal_boleh_diucapkan"]))
    for w in hasil["peringatan"]:
        print("PERINGATAN: " + w)
    print("Pembulatan: " + hasil["aturan_pembulatan"])


if __name__ == "__main__":
    main()
