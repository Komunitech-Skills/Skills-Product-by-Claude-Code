#!/usr/bin/env python3
"""Hitung simulasi skema kerja sama untuk proposal: konsinyasi, bagi hasil, reseller.

Hanya library standar Python (3.8+). Tidak ada akses jaringan.

Contoh:
  # Konsinyasi: produk dijual Rp 25.000, toko dapat 20%, modal Rp 14.000, skenario 50/100/200 pcs per bulan
  python3 hitung_skema.py konsinyasi --harga-jual "Rp 25.000" --porsi-toko 20% --modal 14000 --skenario "50;100;200"

  # Konsinyasi dengan harga titip (toko bebas menjual Rp 25.000, pemilik terima Rp 20.000 per pcs)
  python3 hitung_skema.py konsinyasi --harga-jual 25000 --harga-titip 20000 --skenario 100

  # Bagi hasil omzet 30% untuk mitra
  python3 hitung_skema.py bagi-hasil --porsi-mitra 30% --skenario "10jt;25jt;50jt"

  # Reseller: HET Rp 150.000, diskon reseller 20%, modal 90rb, skenario 20/50/100 pcs
  python3 hitung_skema.py reseller --het 150000 --diskon-reseller 20% --modal 90rb --skenario "20;50;100"

Pembulatan: nilai per unit dan total dibulatkan ke rupiah terdekat (0,5 ke atas).
Total dihitung dari nilai tepat per unit x jumlah, lalu dibulatkan sekali.
"""
import argparse
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class InputSalah(Exception):
    pass


def parse_angka(teks, nama="angka"):
    if teks is None or str(teks).strip() == "":
        raise InputSalah(f"{nama} kosong")
    s = str(teks).strip().lower().replace(" ", "")
    s = re.sub(r"[.,]-$", "", s)  # "Rp 25.000,-"
    pengali = Decimal(1)
    for akhiran, kali in (("juta", 10**6), ("jt", 10**6), ("ribu", 10**3), ("rb", 10**3), ("k", 10**3)):
        if s.endswith(akhiran):
            s = s[: -len(akhiran)]
            pengali = Decimal(kali)
            break
    s = s.replace("rp", "").replace("idr", "")
    if pengali != 1 and re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        raise InputSalah(f"{nama} ambigu: {teks!r}. Tulis tanpa titik (mis. 1500rb) atau pakai koma desimal (mis. 1,5jt)")
    if not re.fullmatch(r"-?[\d.,]+", s or "x"):
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        b = s.split(",")
        s = s.replace(",", ".") if len(b) == 2 and len(b[1]) != 3 else s.replace(",", "")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3 and pengali == 1):
        s = s.replace(".", "")
    try:
        return Decimal(s) * pengali
    except InvalidOperation:
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")


def parse_persen(teks, nama):
    p = parse_angka(str(teks).strip().rstrip("%"), nama)
    if p < 0 or p > 100:
        raise InputSalah(f"{nama} harus antara 0 dan 100%: {teks!r}")
    return p


def bulat(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rupiah(n):
    n = bulat(n)
    return ("-" if n < 0 else "") + f"Rp {abs(n):,}".replace(",", ".")


def persen_id(p):
    p = Decimal(p).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    s = format(p, "f")
    return (s[:-2] if s.endswith(".0") else s.replace(".", ",")) + "%"


PETUNJUK_PEMISAH = "Pisahkan beberapa skenario dengan titik koma, mis. '10;20;30' atau '10jt;25jt;50jt'."


def _pecah_koma(bagian, nama):
    """Pecah satu potong teks yang mungkin berisi koma. Kembalikan list potongan angka."""
    b = re.sub(r"\s*[.,]-$", "", bagian.strip())  # 'Rp 25.000,-' -> 'Rp 25.000'
    if re.search(r"\d\s+\d", b):
        raise InputSalah(f"{nama} ambigu: {bagian!r} berisi angka yang dipisah spasi. " + PETUNJUK_PEMISAH)
    n = b.count(",")
    if n == 0:
        return [b]
    if n >= 2 and re.search(r"(?i)\d,\d{1,2}\s*(jt|juta|rb|ribu|k)\b", b):
        raise InputSalah(f"{nama} ambigu: {bagian!r} mencampur koma desimal dan koma pemisah. " + PETUNJUK_PEMISAH
                         + " Contoh: '1,5jt;2,5jt'.")
    if n >= 2:
        # '10,20,30' -> 3 skenario (koma sebagai pemisah daftar)
        return [x for x in b.split(",") if x.strip()]
    kiri, kanan = [x.strip().lower() for x in b.split(",")]
    satuan = re.compile(r".*(jt|juta|rb|ribu|k)$")
    # '1,5jt' -> satu angka desimal; 'Rp 7.777.777,50' -> satu angka desimal
    if re.fullmatch(r"\d+", kiri.replace(" ", "")) and satuan.match(kanan) and re.fullmatch(r"\d{1,2}\s*(jt|juta|rb|ribu|k)", kanan):
        return [b]
    if re.fullmatch(r"(rp|idr)?\s*\d{1,3}(\.\d{3})+", kiri) and re.fullmatch(r"\d{1,2}", kanan):
        return [b]
    # '10jt,25jt' / 'Rp 10.000,Rp 20.000' -> dua skenario
    if (satuan.match(kiri) or kiri.startswith(("rp", "idr"))) and (satuan.match(kanan) or kanan.startswith(("rp", "idr"))):
        return [kiri, kanan]
    raise InputSalah(f"{nama} ambigu: {bagian!r} bisa berarti satu angka desimal atau dua skenario. " + PETUNJUK_PEMISAH)


def parse_skenario(teks, nama, bilangan_bulat=True):
    """Terima '10;20;30', '10/20/30', '10, 20, 30', '10,20,30', '10jt;25jt', '1,5jt;2,5jt'."""
    hasil = []
    potong = [b for b in re.split(r"[;/]|,\s+", teks.strip()) if b.strip()]
    bagian = []
    for b in potong:
        bagian.extend(_pecah_koma(b, nama))
    for b in bagian:
        v = parse_angka(b, nama)
        if v <= 0:
            raise InputSalah(f"{nama} harus lebih dari 0: {b!r}. " + PETUNJUK_PEMISAH)
        if bilangan_bulat and v != v.to_integral():
            raise InputSalah(f"{nama} harus bilangan bulat (jumlah unit): {b!r}. " + PETUNJUK_PEMISAH)
        hasil.append(v)
    if not hasil:
        raise InputSalah(f"{nama} kosong. " + PETUNJUK_PEMISAH)
    if len(hasil) > 5:
        raise InputSalah(f"{nama} maksimal 5 skenario")
    return hasil


def label_skenario(n):
    return {1: ["Estimasi"], 2: ["Pesimis", "Optimis"], 3: ["Pesimis", "Realistis", "Optimis"]}.get(
        n, [f"Skenario {i}" for i in range(1, n + 1)])


def konsinyasi(a):
    hj = parse_angka(a.harga_jual, "harga jual")
    if hj <= 0:
        raise InputSalah("harga jual harus lebih dari 0")
    if a.harga_titip and a.porsi_toko:
        raise InputSalah("pilih salah satu: --porsi-toko ATAU --harga-titip, jangan keduanya")
    if a.harga_titip:
        ht = parse_angka(a.harga_titip, "harga titip")
        if ht <= 0 or ht > hj:
            raise InputSalah("harga titip harus lebih dari 0 dan tidak lebih besar dari harga jual")
        toko_unit = hj - ht
        porsi = toko_unit / hj * 100
    elif a.porsi_toko:
        porsi = parse_persen(a.porsi_toko, "porsi toko")
        toko_unit = hj * porsi / 100
    else:
        raise InputSalah("isi --porsi-toko (mis. 20%) atau --harga-titip (mis. 20000)")
    pemilik_unit = hj - toko_unit
    modal = parse_angka(a.modal, "modal") if a.modal else None
    if modal is not None and modal < 0:
        raise InputSalah("modal tidak boleh negatif")
    peringatan = []
    if modal is not None and modal > pemilik_unit:
        peringatan.append("Modal per unit lebih besar dari bagian pemilik barang: skema ini RUGI untuk pemilik barang.")
    skenario = []
    for lbl, q in zip(label_skenario(len(a.skenario_v)), a.skenario_v):
        omzet, toko = bulat(hj * q), bulat(toko_unit * q)
        s = {"skenario": lbl, "unit_terjual": int(q), "omzet": omzet,
             "bagian_toko": toko, "bagian_pemilik_barang": omzet - toko}
        if modal is not None:
            s["laba_kotor_pemilik_barang"] = bulat((pemilik_unit - modal) * q)
        skenario.append(s)
    return {
        "skema": "konsinyasi",
        "per_unit": {"harga_jual": bulat(hj), "porsi_toko_persen": float(round(porsi, 2)),
                     "bagian_toko": bulat(toko_unit), "bagian_pemilik_barang": bulat(hj) - bulat(toko_unit),
                     "modal": bulat(modal) if modal is not None else None,
                     "laba_kotor_pemilik_per_unit": bulat(pemilik_unit - modal) if modal is not None else None},
        "periode": a.periode, "skenario": skenario, "peringatan": peringatan,
        "catatan": ["Barang yang tidak laku dikembalikan ke pemilik barang sesuai kesepakatan (tidak dihitung).",
                    "Pembulatan: omzet & bagian toko dibulatkan ke rupiah terdekat (0,5 ke atas); bagian pemilik = omzet - bagian toko, sehingga selalu menjumlah tepat."],
    }


def bagi_hasil(a):
    if not a.porsi_mitra:
        raise InputSalah("isi --porsi-mitra, mis. 30%")
    porsi = parse_persen(a.porsi_mitra, "porsi mitra")
    dasar = "laba bersih" if a.dasar == "laba" else "omzet"
    skenario = []
    for lbl, v in zip(label_skenario(len(a.skenario_v)), a.skenario_v):
        mitra = v * porsi / 100
        skenario.append({"skenario": lbl, dasar.replace(" ", "_"): bulat(v),
                         "bagian_mitra": bulat(mitra), "bagian_pemilik_usaha": bulat(v) - bulat(mitra)})
    return {"skema": "bagi-hasil", "dasar_bagi_hasil": dasar, "porsi_mitra_persen": float(porsi),
            "porsi_pemilik_persen": float(100 - porsi), "periode": a.periode, "skenario": skenario,
            "peringatan": (["Ada nilai omzet/laba di bawah Rp 10.000 — kemungkinan satuan terlewat "
                            "(maksud Anda '10jt;25jt;50jt'?). Konfirmasi ke pengguna."]
                           if any(v < 10000 for v in a.skenario_v) else []),
            "catatan": [f"Bagi hasil dihitung dari {dasar}. Definisikan '{dasar}' secara tertulis di perjanjian.",
                        "Pembulatan: bagian mitra dibulatkan ke rupiah terdekat; sisanya bagian pemilik usaha."]}


def reseller(a):
    het = parse_angka(a.het, "HET/harga jual ke konsumen")
    if het <= 0:
        raise InputSalah("HET harus lebih dari 0")
    if a.harga_reseller and a.diskon_reseller:
        raise InputSalah("pilih salah satu: --harga-reseller ATAU --diskon-reseller")
    if a.harga_reseller:
        hr = parse_angka(a.harga_reseller, "harga reseller")
    elif a.diskon_reseller:
        hr = het * (100 - parse_persen(a.diskon_reseller, "diskon reseller")) / 100
    else:
        raise InputSalah("isi --harga-reseller atau --diskon-reseller")
    if hr <= 0 or hr > het:
        raise InputSalah("harga reseller harus lebih dari 0 dan tidak lebih besar dari HET")
    modal = parse_angka(a.modal, "modal") if a.modal else None
    peringatan = []
    if modal is not None and modal > hr:
        peringatan.append("Modal per unit lebih besar dari harga reseller: produsen RUGI di skema ini.")
    skenario = []
    for lbl, q in zip(label_skenario(len(a.skenario_v)), a.skenario_v):
        s = {"skenario": lbl, "unit": int(q), "belanja_reseller": bulat(hr * q),
             "potensi_untung_reseller": bulat((het - hr) * q)}
        if modal is not None:
            s["laba_kotor_produsen"] = bulat((hr - modal) * q)
        skenario.append(s)
    return {"skema": "reseller", "per_unit": {
        "het": bulat(het), "harga_reseller": bulat(hr), "untung_reseller": bulat(het - hr),
        "margin_reseller_persen": float(round((het - hr) / het * 100, 2)),
        "modal": bulat(modal) if modal is not None else None,
        "laba_kotor_produsen_per_unit": bulat(hr - modal) if modal is not None else None},
        "periode": a.periode, "skenario": skenario, "peringatan": peringatan,
        "catatan": ["Untung reseller = HET - harga reseller, belum dikurangi ongkir/biaya jualan reseller.",
                    "Pembulatan: rupiah terdekat (0,5 ke atas)."]}


def teks(h):
    b = [f"Skema: {h['skema']} (periode: {h['periode']})"]
    if h["skema"] == "konsinyasi":
        u = h["per_unit"]
        b.append(f"Per unit: harga jual {rupiah(u['harga_jual'])} | toko {rupiah(u['bagian_toko'])} "
                 f"({persen_id(u['porsi_toko_persen'])}) | pemilik barang {rupiah(u['bagian_pemilik_barang'])}")
        if u["modal"] is not None:
            b.append(f"Modal {rupiah(u['modal'])} -> laba kotor pemilik {rupiah(u['laba_kotor_pemilik_per_unit'])}/unit")
        b += ["", "| Skenario | Terjual | Omzet | Bagian toko | Bagian pemilik barang |" +
              (" Laba kotor pemilik |" if u["modal"] is not None else ""),
              "|---|---|---|---|---|" + ("---|" if u["modal"] is not None else "")]
        for s in h["skenario"]:
            b.append(f"| {s['skenario']} | {s['unit_terjual']} | {rupiah(s['omzet'])} | {rupiah(s['bagian_toko'])} | "
                     f"{rupiah(s['bagian_pemilik_barang'])} |" +
                     (f" {rupiah(s['laba_kotor_pemilik_barang'])} |" if u["modal"] is not None else ""))
    elif h["skema"] == "bagi-hasil":
        b.append(f"Dasar: {h['dasar_bagi_hasil']} | mitra {persen_id(h['porsi_mitra_persen'])} | "
                 f"pemilik usaha {persen_id(h['porsi_pemilik_persen'])}")
        b += ["", f"| Skenario | {h['dasar_bagi_hasil'].capitalize()} | Bagian mitra | Bagian pemilik usaha |",
              "|---|---|---|---|"]
        k = h["dasar_bagi_hasil"].replace(" ", "_")
        for s in h["skenario"]:
            b.append(f"| {s['skenario']} | {rupiah(s[k])} | {rupiah(s['bagian_mitra'])} | {rupiah(s['bagian_pemilik_usaha'])} |")
    else:
        u = h["per_unit"]
        b.append(f"Per unit: HET {rupiah(u['het'])} | harga reseller {rupiah(u['harga_reseller'])} | "
                 f"untung reseller {rupiah(u['untung_reseller'])} ({persen_id(u['margin_reseller_persen'])})")
        if u["modal"] is not None:
            b.append(f"Modal {rupiah(u['modal'])} -> laba kotor produsen {rupiah(u['laba_kotor_produsen_per_unit'])}/unit")
        m = u["modal"] is not None
        b += ["", "| Skenario | Unit | Belanja reseller | Potensi untung reseller |" + (" Laba kotor produsen |" if m else ""),
              "|---|---|---|---|" + ("---|" if m else "")]
        for s in h["skenario"]:
            b.append(f"| {s['skenario']} | {s['unit']} | {rupiah(s['belanja_reseller'])} | "
                     f"{rupiah(s['potensi_untung_reseller'])} |" + (f" {rupiah(s['laba_kotor_produsen'])} |" if m else ""))
    for p in h["peringatan"]:
        b.append(f"\nPERINGATAN: {p}")
    b.append("")
    b += [f"* {c}" for c in h["catatan"]]
    return "\n".join(b)


def main():
    p = argparse.ArgumentParser(description="Simulasi angka skema kerja sama untuk proposal")
    sub = p.add_subparsers(dest="skema")

    def umum(sp, ket):
        sp.add_argument("--skenario", required=True, help=ket)
        sp.add_argument("--periode", default="per bulan", help="Label periode, default 'per bulan'")
        sp.add_argument("--format", choices=["teks", "json", "keduanya"], default="keduanya")

    k = sub.add_parser("konsinyasi", help="Titip jual: toko dapat persentase / selisih harga titip")
    k.add_argument("--harga-jual", required=True)
    k.add_argument("--porsi-toko", help="Persentase untuk toko/penjual, mis. 20%%")
    k.add_argument("--harga-titip", help="Harga yang diterima pemilik barang per unit")
    k.add_argument("--modal", help="Modal/HPP per unit pemilik barang (opsional)")
    umum(k, "Jumlah unit terjual, 1–5 nilai, mis. '50;100;200'")

    bh = sub.add_parser("bagi-hasil", help="Bagi hasil dari omzet/laba")
    bh.add_argument("--porsi-mitra", help="Persentase untuk mitra, mis. 30%%")
    bh.add_argument("--dasar", choices=["omzet", "laba"], default="omzet")
    umum(bh, "Nilai omzet/laba, 1–5 nilai, mis. '10jt;25jt;50jt'")

    r = sub.add_parser("reseller", help="Harga reseller vs HET")
    r.add_argument("--het", required=True, help="Harga eceran tertinggi / harga jual ke konsumen")
    r.add_argument("--harga-reseller")
    r.add_argument("--diskon-reseller", help="mis. 20%%")
    r.add_argument("--modal", help="Modal/HPP per unit produsen (opsional)")
    umum(r, "Jumlah unit, 1–5 nilai, mis. '20;50;100'")

    a = p.parse_args()
    if not a.skema:
        print("ERROR: pilih skema: konsinyasi, bagi-hasil, atau reseller", file=sys.stderr)
        sys.exit(1)
    try:
        a.skenario_v = parse_skenario(a.skenario, "skenario", bilangan_bulat=(a.skema != "bagi-hasil"))
        h = {"konsinyasi": konsinyasi, "bagi-hasil": bagi_hasil, "reseller": reseller}[a.skema](a)
    except InputSalah as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    if a.format in ("teks", "keduanya"):
        print(teks(h))
    if a.format == "keduanya":
        print("\n--- JSON ---")
    if a.format in ("json", "keduanya"):
        print(json.dumps(h, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
