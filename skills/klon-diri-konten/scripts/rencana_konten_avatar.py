#!/usr/bin/env python3
"""Hitung kebutuhan menit/kredit avatar per bulan vs batas paket, plus biaya dalam Rupiah.

Hanya Python standar. Angka uang memakai Decimal, dibulatkan ke rupiah terdekat (setengah ke atas).

Contoh (--anggaran opsional, dalam Rupiah):
  python3 scripts/rencana_konten_avatar.py --paket paket.json --video 12 --menit 0.75 --revisi 25 --kurs 16500
Windows: pakai `python` atau `py`. Format paket.json: lihat examples/contoh-paket.json
"""
import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_HALF_UP

SATUAN = {"menit", "kredit"}
MATA_UANG = {"IDR", "USD"}
BATAS_ATAS = Decimal(10) ** 12


class DataBuruk(ValueError):
    """Input pengguna tidak valid."""


def dec(nilai, nama, minimum=Decimal(0)):
    if isinstance(nilai, bool) or nilai is None:
        raise DataBuruk(f"'{nama}' harus berupa angka, bukan {nilai!r}")
    try:
        d = Decimal(str(nilai).strip().replace(",", "."))
    except (InvalidOperation, ValueError):
        raise DataBuruk(f"'{nama}' bukan angka: {nilai!r}")
    if not d.is_finite():
        raise DataBuruk(f"'{nama}' tidak valid: {nilai!r}")
    if d < minimum:
        raise DataBuruk(f"'{nama}' tidak boleh kurang dari {minimum}: {nilai!r}")
    if d > BATAS_ATAS:
        raise DataBuruk(f"'{nama}' terlalu besar (maks {BATAS_ATAS}): {nilai!r}")
    return d


def rupiah(d):
    return int(d.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def muat_paket(data):
    if not isinstance(data, list) or not data:
        raise DataBuruk("tabel paket harus berupa daftar (list) berisi minimal 1 paket")
    hasil = []
    for i, p in enumerate(data, start=1):
        if not isinstance(p, dict):
            raise DataBuruk(f"paket ke-{i} bukan objek")
        nama = str(p.get("nama", "")).strip()
        if not nama:
            raise DataBuruk(f"paket ke-{i}: 'nama' kosong")
        satuan = str(p.get("satuan", "menit")).lower()
        if satuan not in SATUAN:
            raise DataBuruk(f"paket '{nama}': 'satuan' harus menit atau kredit")
        mu = str(p.get("mata_uang", "IDR")).upper()
        if mu not in MATA_UANG:
            raise DataBuruk(f"paket '{nama}': 'mata_uang' harus IDR atau USD")
        batas = dec(p.get("batas_bulanan"), f"{nama}.batas_bulanan")
        if batas == 0:
            raise DataBuruk(f"paket '{nama}': 'batas_bulanan' harus lebih dari 0")
        kpm = dec(p.get("kredit_per_menit", 1), f"{nama}.kredit_per_menit")
        if kpm == 0:
            raise DataBuruk(f"paket '{nama}': 'kredit_per_menit' harus lebih dari 0")
        tambahan = p.get("biaya_tambahan_per_satuan")
        hasil.append({
            "nama": nama, "satuan": satuan, "mata_uang": mu,
            "harga": dec(p.get("harga_bulanan"), f"{nama}.harga_bulanan"),
            "batas": batas, "kredit_per_menit": kpm,
            "tambahan": None if tambahan is None else dec(tambahan, f"{nama}.biaya_tambahan_per_satuan"),
        })
    return hasil


def hitung(paket, video, menit_per_video, revisi_persen, kurs, anggaran=None):
    """Kembalikan (menit_butuh, daftar hasil per paket)."""
    video = dec(video, "video", Decimal(1))
    menit_per_video = dec(menit_per_video, "menit per video")
    if menit_per_video == 0:
        raise DataBuruk("'menit per video' harus lebih dari 0")
    revisi = dec(revisi_persen, "revisi")
    kurs = dec(kurs, "kurs")
    anggaran = None if anggaran is None else dec(anggaran, "anggaran")
    menit_butuh = video * menit_per_video * (Decimal(1) + revisi / Decimal(100))
    keluar = []
    for p in paket:
        butuh = menit_butuh if p["satuan"] == "menit" else menit_butuh * p["kredit_per_menit"]
        if p["mata_uang"] == "USD" and kurs == 0:
            raise DataBuruk(f"paket '{p['nama']}' berharga USD, isi --kurs (Rp per 1 USD)")
        faktor = kurs if p["mata_uang"] == "USD" else Decimal(1)
        harga_idr = p["harga"] * faktor
        kurang = max(Decimal(0), butuh - p["batas"])
        if kurang == 0:
            status, total, catatan = "cukup", harga_idr, ""
        elif p["tambahan"] is not None:
            total = harga_idr + kurang * p["tambahan"] * faktor
            status, catatan = "tambah-satuan", f"beli tambahan {kurang.quantize(Decimal('0.01'))} {p['satuan']}"
        else:
            n = int((butuh / p["batas"]).to_integral_value(rounding=ROUND_CEILING))
            total, status, catatan = harga_idr * n, "kurang", f"setara {n} langganan/bulan atau naik paket"
        if anggaran is not None and status != "kurang" and rupiah(total) > anggaran:
            catatan = (catatan + "; " if catatan else "") + "melebihi anggaran"
            status = "lewat-anggaran"
        keluar.append({
            "nama": p["nama"], "satuan": p["satuan"], "butuh": butuh, "batas": p["batas"],
            "sisa": max(Decimal(0), p["batas"] - butuh), "status": status,
            "biaya_idr": rupiah(total), "catatan": catatan,
            "biaya_per_menit_idr": rupiah(total / menit_butuh),
        })
    return menit_butuh, keluar


def cetak(menit_butuh, hasil):
    q = lambda d: f"{d.quantize(Decimal('0.01'))}"
    print(f"Kebutuhan render (termasuk revisi): {q(menit_butuh)} menit/bulan")
    print(f"{'Paket':<22}{'Butuh':>10}{'Batas':>10}{'Sisa':>9}  {'Status':<14}{'Biaya/bulan':>14}{'Rp/menit':>10}")
    for h in hasil:
        print(f"{h['nama'][:21]:<22}{q(h['butuh']):>10}{q(h['batas']):>10}{q(h['sisa']):>9}  "
              f"{h['status']:<14}{'Rp{:,}'.format(h['biaya_idr']).replace(',', '.'):>14}"
              f"{'Rp{:,}'.format(h['biaya_per_menit_idr']).replace(',', '.'):>10}"
              + (f"  ({h['catatan']})" if h["catatan"] else ""))
    layak = [h for h in hasil if h["status"] in ("cukup", "tambah-satuan")]
    if layak:
        b = min(layak, key=lambda h: h["biaya_idr"])
        print(f"Termurah yang mencukupi: {b['nama']} (Rp{b['biaya_idr']:,}".replace(",", ".") + "/bulan)")
    else:
        print("PERINGATAN: tidak ada paket yang mencukupi DAN masuk anggaran. Kurangi jumlah video/durasi/revisi, "
              "naikkan anggaran, atau rekam sebagian video secara manual.")
    print("Catatan: harga adalah input Anda, cek ulang di halaman resmi; belum termasuk pajak/biaya bank.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paket", required=True, help="berkas JSON tabel paket")
    ap.add_argument("--video", required=True, help="jumlah video per bulan")
    ap.add_argument("--menit", required=True, help="menit per video (mis. 0.75 = 45 detik)")
    ap.add_argument("--revisi", default="25", help="persen tambahan untuk render ulang (default 25)")
    ap.add_argument("--kurs", default="0", help="Rp per 1 USD, wajib bila ada paket USD")
    ap.add_argument("--anggaran", default=None, help="batas biaya per bulan (Rp); paket di atasnya tidak direkomendasikan")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    a = ap.parse_args(argv)
    try:
        try:
            with open(a.paket, encoding="utf-8") as f:
                data = json.load(f)
        except OSError as e:
            raise DataBuruk(f"tidak bisa membaca {a.paket}: {e.strerror}")
        except json.JSONDecodeError as e:
            raise DataBuruk(f"{a.paket} bukan JSON valid: {e}")
        mb, hasil = hitung(muat_paket(data), a.video, a.menit, a.revisi, a.kurs, a.anggaran)
    except (DataBuruk, ArithmeticError) as e:
        print(f"GALAT: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"menit_butuh": str(mb), "paket": [
            {**h, "butuh": str(h["butuh"]), "batas": str(h["batas"]), "sisa": str(h["sisa"])} for h in hasil]},
            ensure_ascii=False, indent=2))
    else:
        cetak(mb, hasil)
    return 0


if __name__ == "__main__":
    sys.exit(main())
