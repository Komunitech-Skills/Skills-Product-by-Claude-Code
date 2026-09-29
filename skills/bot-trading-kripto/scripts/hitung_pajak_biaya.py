#!/usr/bin/env python3
"""Hitung fee & PPh final aset kripto (Decimal) -- rekap dari bot/transaksi.csv atau satu transaksi.

Dasar: PMK 50/2025 (berlaku 1 Agustus 2025) -- PPh Pasal 22 final atas penjualan aset kripto:
  0,21% dari nilai transaksi lewat PAKD/PPMSE dalam negeri (dipungut otomatis oleh bursa),
  1%    lewat platform luar negeri (bila platform tidak ditunjuk DJP, penjual menyetor sendiri).
Pasangan RUPIAH: pembeli tidak dikenai PPh ini (nilai = uang yang dibayar pembeli, Pasal 12 ayat (5) huruf a).
Pasangan KRIPTO-KRIPTO (mis. BTCUSDT, USDT = aset kripto) = tukar-menukar (swap): PPh atas nilai MASING-MASING
aset yang diserahkan (Pasal 11 ayat (2) huruf b, Pasal 12 ayat (5) huruf b) -> sisi BELI juga kena;
rekap di bawah menjumlahkan kolom pajak_pph dari SEMUA baris (beli & jual).
Penyerahan aset kripto tidak dikenai PPN (Pasal 2 ayat (1)); jasa platform/fee dikenai PPN (Pasal 2 ayat (2)
huruf a) yang dipungut bursa dan sudah termasuk dalam angka fee dari bursa.
Sumber: teks resmi https://jdih.kemenkeu.go.id/api/download/66a7633b-9e1b-4a54-9046-5320aa96c7e1/2025pmkeuangan050.pdf
& https://www.pajak.go.id/index.php/en/node/118105 (dibaca 2026-09-29).
Pembulatan: PPh dibulatkan ke BAWAH ke rupiah; fee ke rupiah terdekat. BELUM dicocokkan dengan Coretax.

  python3 hitung_pajak_biaya.py --nilai-jual 15000000 --pajak domestik --fee-persen 0.2
  python3 hitung_pajak_biaya.py --transaksi bot/transaksi.csv [--kurs USDT=16500]   (rekap per bulan)
Rekap dipisah PER MATA UANG KUTIPAN (IDR, USDT, USDC, BTC, ...) dan tidak pernah menjumlahkan mata uang
berbeda. Konversi ke rupiah hanya dengan kurs yang Anda isi sendiri (--kurs), ditandai PERKIRAAN.
"""

import argparse
import csv
import json
import sys
from collections import OrderedDict
from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_UP

TARIF = {"domestik": Decimal("0.0021"), "luar_negeri": Decimal("0.01")}
CATATAN = ("Dasar: PMK 50/2025 (berlaku 1 Agustus 2025), dicek 2026-09-29 di teks resmi JDIH Kemenkeu. Pasangan "
           "kripto-kripto (swap): PPh juga di sisi beli. Pembulatan belum "
           "dicocokkan dengan Coretax. Ini alat bantu hitung, bukan nasihat pajak -- konfirmasi ke konsultan pajak/DJP.")


def dec(s, nama):
    try:
        x = Decimal(str(s).strip())
    except InvalidOperation:
        raise ValueError(f"{nama} '{s}' bukan angka")
    if not x.is_finite() or x < 0:
        raise ValueError(f"{nama} harus angka >= 0")
    return x


def rp(x):
    return int(x.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def satu(nilai_jual, pajak, fee_persen):
    pph = (nilai_jual * TARIF[pajak]).quantize(Decimal("1"), rounding=ROUND_DOWN)
    fee = (nilai_jual * fee_persen / 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return {"nilai_jual": rp(nilai_jual), "tarif_pph_persen": str(TARIF[pajak] * 100), "pph": int(pph),
            "fee": int(fee), "diterima_bersih": rp(nilai_jual - pph - fee), "catatan": CATATAN}


# Kutipan dikenali dari akhiran nama pasangan Binance (terpanjang dulu). Indodax: akhiran "_idr".
KUTIPAN_DIKENAL = ("FDUSD", "USDT", "USDC", "TUSD", "BUSD", "USDP", "EURI", "IDRT", "BIDR", "DAI", "IDR", "BTC",
                   "ETH", "BNB", "EUR", "TRY", "BRL", "JPY", "GBP", "AUD", "XRP", "SOL", "DOGE", "TRX", "USD")
NOL = Decimal(0)


def kutipan_dari_pasangan(pasangan):
    p = (pasangan or "").strip()
    if "_" in p:
        return p.rsplit("_", 1)[1].upper()
    p = p.upper()
    for k in sorted(KUTIPAN_DIKENAL, key=len, reverse=True):
        if p.endswith(k) and len(p) > len(k):
            return k
    raise ValueError(f"mata uang kutipan pasangan '{pasangan}' tidak dikenali")


def angka_kutipan(x, kutipan, pajak=False):
    """IDR -> rupiah bulat (int); lainnya -> teks 8 desimal. PPh dibulatkan ke BAWAH."""
    if kutipan == "IDR":
        return int(x.quantize(Decimal("1"), rounding=ROUND_DOWN if pajak else ROUND_HALF_UP))
    q = x.quantize(Decimal("0.00000001"), rounding=ROUND_DOWN if pajak else ROUND_HALF_UP)
    return format(q.normalize(), "f") if q else "0"


def parse_kurs(daftar):
    """['USDT=16500', 'BTC=1500000000'] -> {'USDT': Decimal(...)}. Kurs = rupiah per 1 unit kutipan."""
    out = {}
    for item in daftar or []:
        if "=" not in item:
            raise ValueError(f"--kurs '{item}' harus berbentuk KUTIPAN=ANGKA, mis. USDT=16500")
        k, v = item.split("=", 1)
        k = k.strip().upper()
        if k == "IDR":
            raise ValueError("--kurs untuk IDR tidak perlu (rupiah tidak dikonversi)")
        x = dec(v, f"kurs {k}")
        if x <= 0:
            raise ValueError(f"kurs {k} harus lebih dari 0")
        out[k] = x
    return out


def rekap(path, kurs=None):
    """Rekap per bulan PER MATA UANG KUTIPAN. Mata uang berbeda TIDAK pernah dijumlahkan.
    Konversi ke rupiah hanya bila pengguna memberi kurs (--kurs USDT=16500), ditandai PERKIRAAN."""
    kurs = kurs or {}
    per_bulan = OrderedDict()
    rusak = []
    with open(path, encoding="utf-8-sig") as f:
        for no, b in enumerate(csv.DictReader(f), start=2):
            try:
                bulan = b["waktu"][:7]
                kut = kutipan_dari_pasangan(b["pasangan"])
                if b["sisi"] not in ("jual", "beli"):
                    raise ValueError(f"sisi '{b['sisi']}' tidak dikenal")
                fee = dec(b["fee"], "fee")
                bruto = dec(b["bruto"], "bruto")
                pph = dec(b.get("pajak_pph") or "0", "pajak_pph")
                r = per_bulan.setdefault(bulan, OrderedDict()).setdefault(kut, {
                    "jumlah_jual": 0, "jumlah_beli": 0, "nilai_jual": NOL, "nilai_beli": NOL,
                    "pph": NOL, "pph_sisi_beli": NOL, "fee": NOL})
                r["fee"] += fee
                r["pph"] += pph
                if b["sisi"] == "jual":
                    r["jumlah_jual"] += 1
                    r["nilai_jual"] += bruto
                else:
                    r["jumlah_beli"] += 1
                    r["nilai_beli"] += bruto
                    r["pph_sisi_beli"] += pph
            except (KeyError, ValueError, AttributeError) as e:
                rusak.append({"baris": no, "alasan": str(e)})
    hasil = OrderedDict()
    total = OrderedDict()
    tanpa_kurs = set()
    for bulan, per_kut in per_bulan.items():
        hasil[bulan] = OrderedDict()
        for kut, r in per_kut.items():
            t = total.setdefault(kut, {k: (0 if isinstance(v, int) else NOL) for k, v in r.items()})
            for k, v in r.items():
                t[k] += v
            hasil[bulan][kut] = ringkas(kut, r, kurs, tanpa_kurs)
    total_out = OrderedDict((kut, ringkas(kut, t, kurs, tanpa_kurs)) for kut, t in total.items())
    peringatan = []
    if tanpa_kurs:
        peringatan.append("Pasangan non-rupiah (" + ", ".join(sorted(tanpa_kurs)) + ") dilaporkan dalam mata uang "
                          "kutipannya, TIDAK dijumlahkan sebagai rupiah. Untuk perkiraan rupiah, isi kurs sendiri, "
                          "--kurs " + sorted(tanpa_kurs)[0] + "=<rupiah per 1 " + sorted(tanpa_kurs)[0] + ">.")
    if len(total) > 1:
        peringatan.append("Ada lebih dari satu mata uang kutipan; jumlahkan ke rupiah hanya setelah dikonversi dengan "
                          "kurs yang sah (lihat references/regulasi-pajak.md, Pasal 12 ayat (7) PMK 50/2025).")
    return {"per_bulan": hasil, "total_per_mata_uang": total_out, "baris_bermasalah": rusak,
            "peringatan": peringatan, "catatan": CATATAN}


def ringkas(kut, r, kurs, tanpa_kurs):
    out = OrderedDict([("mata_uang", kut), ("jumlah_jual", r["jumlah_jual"]), ("jumlah_beli", r["jumlah_beli"]),
                       ("nilai_jual", angka_kutipan(r["nilai_jual"], kut)),
                       ("nilai_beli", angka_kutipan(r["nilai_beli"], kut)),
                       ("pph", angka_kutipan(r["pph"], kut, pajak=True)),
                       ("pph_sisi_beli", angka_kutipan(r["pph_sisi_beli"], kut, pajak=True)),
                       ("fee", angka_kutipan(r["fee"], kut))])
    if kut == "IDR":
        return out
    k = kurs.get(kut)
    if k is None:
        tanpa_kurs.add(kut)
        return out
    out["perkiraan_rupiah"] = OrderedDict([
        ("label", f"PERKIRAAN - dikonversi dengan kurs yang ANDA masukkan (1 {kut} = Rp{teks_desimal(k)}), "
                  "bukan kurs resmi pajak; cocokkan dengan kurs yang sah sebelum lapor."),
        ("kurs_dari_pengguna", teks_desimal(k)),
        ("nilai_jual_idr", rp(r["nilai_jual"] * k)), ("nilai_beli_idr", rp(r["nilai_beli"] * k)),
        ("pph_idr", int((r["pph"] * k).quantize(Decimal("1"), rounding=ROUND_DOWN))),
        ("pph_sisi_beli_idr", int((r["pph_sisi_beli"] * k).quantize(Decimal("1"), rounding=ROUND_DOWN))),
        ("fee_idr", rp(r["fee"] * k))])
    return out


def teks_desimal(x):
    return format(x.normalize(), "f")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hitung fee & PPh final kripto (PMK 50/2025)")
    ap.add_argument("--nilai-jual")
    ap.add_argument("--pajak", choices=tuple(TARIF), default="domestik")
    ap.add_argument("--fee-persen", default="0")
    ap.add_argument("--transaksi")
    ap.add_argument("--kurs-idr", help="(lama) sama dengan --kurs USDT=<angka>")
    ap.add_argument("--kurs", action="append", default=[],
                    help="kurs rupiah per 1 unit kutipan, boleh berulang: --kurs USDT=16500 --kurs BTC=1500000000")
    a = ap.parse_args(argv)
    try:
        if a.transaksi:
            kurs = parse_kurs(a.kurs)
            if a.kurs_idr:
                kurs.setdefault("USDT", parse_kurs(["USDT=" + a.kurs_idr])["USDT"])
            out = rekap(a.transaksi, kurs)
        elif a.nilai_jual:
            out = satu(dec(a.nilai_jual, "nilai jual"), a.pajak, dec(a.fee_persen, "fee"))
        else:
            print("Isi --nilai-jual atau --transaksi.")
            return 1
    except (ValueError, FileNotFoundError) as e:
        print(json.dumps({"status": "error", "pesan": str(e)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "ok", **out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
