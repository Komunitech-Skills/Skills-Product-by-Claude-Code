#!/usr/bin/env python3
"""Hitung selisih & persen perubahan antara dua angka (Python standar, Decimal).

Dipakai oleh skill `presentasi-data-ke-atasan` agar angka pendukung ("3 angka
pendukung") di ringkasan untuk atasan/investor/bank tidak dikira-kira. Menerima
beberapa pasangan angka sekaligus (mis. omzet lama vs baru, biaya iklan lama vs
baru) dan mengeluarkan JSON siap dibaca agent.

Pembulatan (sesuai standar library ini, CLAUDE.md Tahap 4):
- Nominal Rupiah (nilai lama, nilai baru, selisih) dibulatkan ke rupiah terdekat.
- Persen perubahan dibulatkan ke 1 angka desimal (ROUND_HALF_UP), bukan dipotong.
- Bila nilai lama = 0, persen perubahan tidak didefinisikan → dilaporkan sebagai
  null dengan keterangan, bukan dipaksakan jadi angka.

Pemakaian:
    python3 hitung_perubahan.py --pasangan "Omzet:32000000:24500000" \
        --pasangan "Biaya iklan:4000000:5600000"

Format satu --pasangan: "Label:nilai_lama:nilai_baru" (angka polos, tanpa "Rp"
atau titik ribuan; agent yang membersihkan input pengguna dulu sebelum memanggil
script ini, mis. dengan skill `analisis-excel`/`rekap-penjualan-csv` bila sumbernya
file, atau langsung dari angka yang disebutkan pengguna di chat).

Bisa juga dipakai untuk menghitung dari daftar angka satu kolom (mis. omzet 7
hari terakhir) dengan --daftar, untuk mendapat total, rata-rata, min, max.
"""
import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


def format_angka(d: Decimal) -> int:
    """Bulatkan nilai bilangan bulat terdekat (dipakai untuk Rupiah maupun angka lain,
    mis. total/rata-rata di --daftar yang belum tentu Rupiah)."""
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def persen(lama: Decimal, baru: Decimal):
    if lama == 0:
        return None
    hasil = (baru - lama) / lama * Decimal("100")
    return float(hasil.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def proses_pasangan(spek: str):
    bagian = spek.split(":")
    if len(bagian) != 3:
        raise ValueError(f"format harus 'Label:nilai_lama:nilai_baru', dapat: {spek!r}")
    label, s_lama, s_baru = bagian
    try:
        lama = Decimal(s_lama.strip())
        baru = Decimal(s_baru.strip())
    except InvalidOperation:
        raise ValueError(f"angka tidak valid di {spek!r} (jangan pakai 'Rp'/titik ribuan)")
    selisih = baru - lama
    p = persen(lama, baru)
    if p is None:
        catatan = "nilai lama = 0, persen tidak didefinisikan"
    elif lama < 0:
        catatan = ("nilai lama negatif — persen perubahan dari basis negatif tidak "
                   "intuitif (bisa berlawanan arah dengan tanda 'naik/turun'); "
                   "sampaikan ke pengguna arah dan selisih Rupiah saja, jangan tampilkan "
                   "persennya mentah-mentah")
    else:
        catatan = None
    return {
        "label": label.strip(),
        "nilai_lama": format_angka(lama),
        "nilai_baru": format_angka(baru),
        "selisih": format_angka(selisih),
        "arah": "naik" if selisih > 0 else ("turun" if selisih < 0 else "tetap"),
        "persen_perubahan": p,
        "catatan": catatan,
    }


def proses_daftar(nama_spek: str):
    if "=" not in nama_spek:
        raise ValueError(f"format --daftar harus 'Label=angka1,angka2,...', dapat: {nama_spek!r}")
    label, s_angka = nama_spek.split("=", 1)
    angka = []
    for token in s_angka.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            angka.append(Decimal(token))
        except InvalidOperation:
            raise ValueError(f"angka tidak valid di daftar {label!r}: {token!r}")
    if not angka:
        raise ValueError(f"daftar {label!r} kosong")
    total = sum(angka)
    rata = total / Decimal(len(angka))
    return {
        "label": label.strip(),
        "jumlah_data": len(angka),
        "total": format_angka(total),
        "rata_rata": format_angka(rata),
        "min": format_angka(min(angka)),
        "max": format_angka(max(angka)),
    }


def main():
    ap = argparse.ArgumentParser(description="Hitung selisih/persen perubahan & ringkasan daftar angka")
    ap.add_argument("--pasangan", action="append", default=[],
                     help="'Label:nilai_lama:nilai_baru', bisa diulang")
    ap.add_argument("--daftar", action="append", default=[],
                     help="'Label=angka1,angka2,...', bisa diulang")
    args = ap.parse_args()

    if not args.pasangan and not args.daftar:
        print(json.dumps({"error": "isi minimal satu --pasangan atau --daftar"}, ensure_ascii=False))
        sys.exit(1)

    hasil = {"pasangan": [], "daftar": []}
    try:
        for p in args.pasangan:
            hasil["pasangan"].append(proses_pasangan(p))
        for d in args.daftar:
            hasil["daftar"].append(proses_daftar(d))
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(hasil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
