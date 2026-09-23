#!/usr/bin/env python3
"""Hitung rincian Surat Penawaran Harga (SPH): subtotal, diskon, ongkir, PPN, total, terbilang.

Hanya memakai library standar Python (3.8+). Tidak ada akses jaringan.

Contoh:
  python3 hitung_sph.py \
    --item "Kursi kantor ergonomis|10|unit|Rp 1.250.000|5%" \
    --item "Meja kerja 120x60|10|unit|Rp 950.000" \
    --diskon-total "Rp 250.000" --ongkir "Rp 300.000" \
    --ppn pkp --nomor-urut 12 --kode "SPH/MKS" --berlaku-hari 14

Aturan pembulatan (dijelaskan juga di output):
  - Semua nilai rupiah dibulatkan ke rupiah penuh terdekat (>= 0,5 naik) per baris.
  - PPN non-mewah = 12% x (11/12 x DPP), dihitung tepat lalu dibulatkan sekali ke rupiah terdekat.
"""
import argparse
import csv
import json
import re
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from fractions import Fraction

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
ROMAWI = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


class InputSalah(Exception):
    pass


# ---------- utilitas angka ----------
def parse_angka(teks, nama="angka"):
    """Terima '15000', 'Rp 15.000', '15.000,50', '1,5', '15,000.50', '1.5jt', '250rb'."""
    if teks is None:
        raise InputSalah(f"{nama} kosong")
    s = str(teks).strip().lower().replace(" ", "")
    pengali = Decimal(1)
    for akhiran, kali in (("juta", 10**6), ("jt", 10**6), ("ribu", 10**3), ("rb", 10**3), ("k", 10**3)):
        if s.endswith(akhiran):
            s = s[: -len(akhiran)]
            pengali = Decimal(kali)
            break
    s = s.replace("rp", "").replace("idr", "")
    if not re.fullmatch(r"-?[\d.,]+", s or "x"):
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3 and pengali == 1):
        s = s.replace(".", "")
    try:
        return Decimal(s) * pengali
    except InvalidOperation:
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")


def bulat(x):
    """Bulatkan ke rupiah penuh terdekat (0,5 ke atas)."""
    if isinstance(x, Fraction):
        x = Decimal(x.numerator) / Decimal(x.denominator)
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rupiah(n):
    tanda = "-" if n < 0 else ""
    return f"{tanda}Rp {abs(int(n)):,}".replace(",", ".")


def angka_id(d):
    """Tampilkan qty: 10 -> '10', 2.5 -> '2,5'."""
    d = Decimal(d).normalize()
    if d == d.to_integral():
        return f"{int(d):,}".replace(",", ".")
    return format(d, "f").replace(".", ",")


def parse_diskon(teks, dasar, nama):
    """'10%' -> persen dari dasar; 'Rp 5.000' -> nominal. Kembalikan (nominal_int, label)."""
    if teks is None or str(teks).strip() in ("", "-", "0"):
        return 0, ""
    t = str(teks).strip()
    if t.endswith("%"):
        p = parse_angka(t[:-1], nama)
        if p < 0 or p > 100:
            raise InputSalah(f"{nama} harus 0–100%: {teks!r}")
        return bulat(Decimal(dasar) * p / 100), f"{angka_id(p)}%"
    n = parse_angka(t, nama)
    if n < 0:
        raise InputSalah(f"{nama} tidak boleh negatif: {teks!r}")
    return bulat(n), rupiah(bulat(n))


def terbilang(n):
    satuan = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan",
              "sembilan", "sepuluh", "sebelas"]

    def t(x):
        if x < 12:
            return satuan[x]
        if x < 20:
            return t(x - 10) + " belas"
        if x < 100:
            return (t(x // 10) + " puluh " + t(x % 10)).strip()
        if x < 200:
            return ("seratus " + t(x - 100)).strip()
        if x < 1000:
            return (t(x // 100) + " ratus " + t(x % 100)).strip()
        if x < 2000:
            return ("seribu " + t(x - 1000)).strip()
        for besar, nama in ((10**12, "triliun"), (10**9, "miliar"), (10**6, "juta"), (10**3, "ribu")):
            if x >= besar:
                return (t(x // besar) + f" {nama} " + t(x % besar)).strip()
        return ""

    if n == 0:
        return "Nol Rupiah"
    hasil = re.sub(r"\s+", " ", t(abs(n))).strip()
    return ("Minus " if n < 0 else "") + hasil.title() + " Rupiah"


def tgl_id(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


# ---------- input item ----------
def item_dari_teks(teks, no):
    bagian = [b.strip() for b in teks.split("|")]
    if len(bagian) < 4:
        raise InputSalah(
            f"item ke-{no} kurang lengkap: {teks!r}. Format: 'Nama|qty|satuan|harga|diskon(opsional)'")
    return {"nama": bagian[0], "qty": bagian[1], "satuan": bagian[2], "harga": bagian[3],
            "diskon": bagian[4] if len(bagian) > 4 else ""}


def item_dari_csv(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            contoh = f.read(4096)
            f.seek(0)
            try:
                dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
            except csv.Error:
                dialek = csv.excel
            baris = list(csv.DictReader(f, dialect=dialek))
    except OSError as e:
        raise InputSalah(f"file item tidak bisa dibuka: {e}")
    hasil = []
    for b in baris:
        k = {str(kunci).strip().lower(): (v or "").strip() for kunci, v in b.items() if kunci}
        if not any(k.values()):
            continue
        hasil.append({"nama": k.get("nama", ""), "qty": k.get("qty", ""), "satuan": k.get("satuan", "pcs"),
                      "harga": k.get("harga", ""), "diskon": k.get("diskon", "")})
    if not hasil:
        raise InputSalah("file item kosong. Kolom yang dibutuhkan: nama, qty, satuan, harga, diskon (opsional)")
    return hasil


def hitung(args):
    mentah = []
    for i, t in enumerate(args.item or [], start=1):
        mentah.append(item_dari_teks(t, i))
    if args.file:
        mentah.extend(item_dari_csv(args.file))
    if not mentah:
        raise InputSalah("belum ada item. Tambahkan minimal satu --item atau --file")

    items = []
    for no, it in enumerate(mentah, start=1):
        if not it["nama"]:
            raise InputSalah(f"item ke-{no}: nama barang/jasa kosong")
        qty = parse_angka(it["qty"], f"qty item ke-{no}")
        harga = parse_angka(it["harga"], f"harga item ke-{no}")
        if qty <= 0:
            raise InputSalah(f"item ke-{no} ({it['nama']}): qty harus lebih dari 0")
        if harga < 0:
            raise InputSalah(f"item ke-{no} ({it['nama']}): harga tidak boleh negatif")
        bruto = bulat(qty * harga)
        disk, label = parse_diskon(it["diskon"], bruto, f"diskon item ke-{no}")
        if disk > bruto:
            raise InputSalah(f"item ke-{no} ({it['nama']}): diskon ({rupiah(disk)}) melebihi jumlah ({rupiah(bruto)})")
        items.append({
            "no": no, "nama": it["nama"], "qty": angka_id(qty), "satuan": it["satuan"] or "pcs",
            "harga_satuan": bulat(harga), "jumlah_bruto": bruto,
            "diskon": disk, "diskon_label": label, "jumlah": bruto - disk,
        })

    subtotal = sum(i["jumlah"] for i in items)
    diskon_total, diskon_total_label = parse_diskon(args.diskon_total, subtotal, "diskon total")
    if diskon_total > subtotal:
        raise InputSalah(f"diskon total ({rupiah(diskon_total)}) melebihi subtotal ({rupiah(subtotal)})")
    ongkir = bulat(parse_angka(args.ongkir, "ongkir")) if args.ongkir else 0
    if ongkir < 0:
        raise InputSalah("ongkir tidak boleh negatif")
    setelah_diskon = subtotal - diskon_total
    dasar = setelah_diskon + ongkir

    tarif = Fraction(parse_angka(args.tarif_ppn, "tarif PPN")) / 100
    if args.ppn == "tidak":
        rasio = Fraction(0)
    elif args.ppn == "pkp":
        rasio = Fraction(11, 12)
    else:  # mewah
        rasio = Fraction(1)
    efektif = tarif * rasio  # 12% x 11/12 = 11%

    catatan = []
    if args.ppn == "tidak":
        dpp, dpp_nilai_lain, ppn, total = dasar, 0, 0, dasar
        catatan.append("Tanpa PPN (penjual bukan PKP / tidak memungut PPN).")
    elif args.harga_termasuk_ppn:
        dpp = bulat(Fraction(dasar) / (1 + efektif))
        ppn = dasar - dpp
        total = dasar
        dpp_nilai_lain = bulat(Fraction(dpp) * rasio)
        catatan.append("Harga yang dimasukkan sudah termasuk PPN; DPP dihitung mundur = harga / (1 + tarif efektif).")
    else:
        dpp = dasar
        dpp_nilai_lain = bulat(Fraction(dpp) * rasio)
        ppn = bulat(Fraction(dpp) * efektif)
        total = dpp + ppn
    if args.ppn == "pkp":
        catatan.append("PPN barang/jasa non-mewah: 12% x DPP nilai lain (11/12 x harga jual) = efektif 11% (PMK 131/2024).")
    elif args.ppn == "mewah":
        catatan.append("PPN barang mewah: 12% x harga jual penuh (PPnBM, jika ada, belum dihitung).")
    catatan.append("Pembulatan: setiap nilai rupiah dibulatkan ke rupiah penuh terdekat (0,5 ke atas). "
                   "PPN dihitung dari nilai tepat lalu dibulatkan sekali; faktur pajak resmi di Coretax bisa selisih Rp 1.")

    tgl = datetime.strptime(args.tanggal, "%Y-%m-%d").date() if args.tanggal else date.today()
    if args.berlaku_hari < 1:
        raise InputSalah("masa berlaku minimal 1 hari")
    berlaku = tgl + timedelta(days=args.berlaku_hari)
    nomor = None
    if args.nomor_urut is not None:
        if args.nomor_urut < 1:
            raise InputSalah("nomor urut minimal 1")
        nomor = f"{args.nomor_urut:03d}/{args.kode.strip('/')}/{ROMAWI[tgl.month - 1]}/{tgl.year}"

    return {
        "nomor_surat": nomor,
        "tanggal": tgl.isoformat(), "tanggal_teks": tgl_id(tgl),
        "berlaku_sampai": berlaku.isoformat(), "berlaku_sampai_teks": tgl_id(berlaku),
        "masa_berlaku_hari": args.berlaku_hari,
        "items": items,
        "subtotal": subtotal,
        "diskon_total": diskon_total, "diskon_total_label": diskon_total_label,
        "setelah_diskon": setelah_diskon,
        "ongkir": ongkir,
        "mode_ppn": args.ppn,
        "harga_termasuk_ppn": bool(args.harga_termasuk_ppn),
        "dpp": dpp, "dpp_nilai_lain": dpp_nilai_lain,
        "tarif_ppn_persen": float(tarif * 100),
        "tarif_efektif_persen": float(efektif * 100),
        "ppn": ppn,
        "total": total,
        "terbilang": terbilang(total),
        "catatan": catatan,
    }


def teks_rapi(h):
    baris = []
    if h["nomor_surat"]:
        baris.append(f"Nomor        : {h['nomor_surat']}")
    baris.append(f"Tanggal      : {h['tanggal_teks']}")
    baris.append(f"Berlaku s.d. : {h['berlaku_sampai_teks']} ({h['masa_berlaku_hari']} hari)")
    baris.append("")
    baris.append("| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |")
    baris.append("|---|---|---|---|---|---|---|")
    for i in h["items"]:
        d = f"{i['diskon_label']} ({rupiah(i['diskon'])})" if i["diskon"] and i["diskon_label"].endswith("%") \
            else (rupiah(i["diskon"]) if i["diskon"] else "-")
        baris.append(f"| {i['no']} | {i['nama']} | {i['qty']} | {i['satuan']} | {rupiah(i['harga_satuan'])} | {d} | {rupiah(i['jumlah'])} |")
    baris.append("")
    baris.append(f"Subtotal                 : {rupiah(h['subtotal'])}")
    if h["diskon_total"]:
        lbl = f" ({h['diskon_total_label']})" if h["diskon_total_label"].endswith("%") else ""
        baris.append(f"{'Diskon tambahan' + lbl:<25}: -{rupiah(h['diskon_total'])}")
    if h["ongkir"]:
        baris.append(f"Ongkos kirim             : {rupiah(h['ongkir'])}")
    if h["mode_ppn"] != "tidak":
        baris.append(f"DPP (harga jual)         : {rupiah(h['dpp'])}")
        if h["mode_ppn"] == "pkp":
            baris.append(f"DPP nilai lain (11/12)   : {rupiah(h['dpp_nilai_lain'])}")
        baris.append(f"{'PPN ' + format(h['tarif_ppn_persen'], 'g') + '%':<25}: {rupiah(h['ppn'])}")
    baris.append(f"TOTAL                    : {rupiah(h['total'])}")
    baris.append(f"Terbilang                : {h['terbilang']}")
    baris.append("")
    for c in h["catatan"]:
        baris.append(f"* {c}")
    return "\n".join(baris)


def main():
    p = argparse.ArgumentParser(description="Hitung rincian Surat Penawaran Harga (SPH)")
    p.add_argument("--item", action="append",
                   help="'Nama|qty|satuan|harga|diskon'. Diskon opsional: '10%%' atau 'Rp 5.000' (per baris). Bisa diulang.")
    p.add_argument("--file", help="CSV item dengan kolom: nama,qty,satuan,harga,diskon")
    p.add_argument("--diskon-total", help="Diskon atas subtotal: '5%%' atau 'Rp 100.000'")
    p.add_argument("--ongkir", help="Ongkos kirim/biaya pasang (ikut DPP bila PKP)")
    p.add_argument("--ppn", choices=["tidak", "pkp", "mewah"], default="tidak",
                   help="tidak = penjual bukan PKP (default); pkp = non-mewah 12%% x 11/12; mewah = 12%% penuh")
    p.add_argument("--tarif-ppn", default="12", help="Tarif PPN dalam persen (default 12)")
    p.add_argument("--harga-termasuk-ppn", action="store_true", help="Harga item sudah termasuk PPN")
    p.add_argument("--tanggal", help="Tanggal surat YYYY-MM-DD (default hari ini)")
    p.add_argument("--berlaku-hari", type=int, default=14, help="Masa berlaku penawaran (default 14 hari)")
    p.add_argument("--nomor-urut", type=int, help="Nomor urut surat, mis. 12 -> 012/...")
    p.add_argument("--kode", default="SPH", help="Kode surat/usaha, mis. 'SPH/MKS' (default SPH)")
    p.add_argument("--format", choices=["teks", "json", "keduanya"], default="keduanya")
    args = p.parse_args()

    try:
        if args.tanggal:
            try:
                datetime.strptime(args.tanggal, "%Y-%m-%d")
            except ValueError:
                raise InputSalah(f"format tanggal harus YYYY-MM-DD, mis. 2026-09-23 (diberikan: {args.tanggal!r})")
        h = hitung(args)
    except InputSalah as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format in ("teks", "keduanya"):
        print(teks_rapi(h))
    if args.format == "keduanya":
        print("\n--- JSON ---")
    if args.format in ("json", "keduanya"):
        print(json.dumps(h, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
