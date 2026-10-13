#!/usr/bin/env python3
"""Hitung selisih & persen perubahan antara dua angka (Python standar, Decimal).

Dipakai oleh skill `presentasi-data-ke-atasan` agar angka pendukung ("3 angka
pendukung") di ringkasan untuk atasan/investor/bank tidak dikira-kira. Menerima
beberapa pasangan angka sekaligus (mis. omzet lama vs baru, biaya iklan lama vs
baru) dan mengeluarkan JSON siap dibaca agent.

Pembulatan (sesuai standar library ini, standar pembulatan library Komunitech):
- Nominal Rupiah (nilai lama, nilai baru, selisih) dibulatkan ke rupiah terdekat.
- Persen perubahan dibulatkan ke 1 angka desimal (ROUND_HALF_UP), bukan dipotong.
- Bila nilai lama = 0, persen perubahan tidak didefinisikan → dilaporkan sebagai
  null dengan keterangan, bukan dipaksakan jadi angka.
- Bila nilai lama negatif (mis. laba rugi -Rp5.000.000 → Rp2.000.000), persen
  perubahan tetap dihitung matematis tapi disertai "catatan" yang mengingatkan agent
  agar tidak menampilkan persen tersebut mentah-mentah ke pengguna (bisa berlawanan
  arah dengan tanda naik/turun) — cukup sebut arah & selisih Rupiah.

Pemakaian:
    python3 hitung_perubahan.py --pasangan "Omzet:32000000:24500000" \
        --pasangan "Biaya iklan:4000000:5600000"

Format satu --pasangan: "Label:nilai_lama:nilai_baru". Angka boleh polos (32000000)
atau format Indonesia seperti yang diketik pengguna: 38.000 / 1.250.000 (titik =
ribuan), 38.000,50 atau 2,5 (koma = desimal), Rp38.000 / Rp 38.000, 38rb, 1,5jt.
Bentuk ragu seperti 38.5 (titik diikuti 1-2 angka) atau 1,500 (koma diikuti tepat
3 angka) DITOLAK dengan pesan jelas, tidak ditebak diam-diam.

Bisa juga dipakai untuk menghitung dari daftar angka satu kolom (mis. omzet 7
hari terakhir) dengan --daftar, untuk mendapat total, rata-rata, min, max.
Pemisah --daftar: koma ("Stok=18,24,29") atau titik-koma bila ada koma desimal
/ rb / jt ("Omzet=1,5jt;2jt;850rb").
"""
import argparse
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


def format_angka(d: Decimal) -> int:
    """Bulatkan nilai bilangan bulat terdekat (dipakai untuk Rupiah maupun angka lain,
    mis. total/rata-rata di --daftar yang belum tentu Rupiah)."""
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


SATUAN = (("ribu", 1000), ("rb", 1000), ("k", 1000), ("juta", 10 ** 6), ("jt", 10 ** 6),
          ("miliar", 10 ** 9), ("milyar", 10 ** 9))
SARAN = "Contoh yang benar: 38000, 38.000, Rp38.000, 1.250.000,50, 2,5, 38rb, 1,5jt."


def punya_satuan(teks: str) -> bool:
    return re.search(r"(ribu|rb|k|juta|jt|miliar|milyar)$", teks.strip().lower()) is not None


def baca_angka(teks: str) -> Decimal:
    """Baca angka gaya Indonesia. Titik = ribuan, koma = desimal. Bentuk ragu -> ValueError."""
    asli = str(teks).strip()
    s = asli.lower().replace("\u00a0", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    neg = s.startswith("-")
    s = s.lstrip("-")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    kali = 1
    for akhiran, k in SATUAN:
        if s.endswith(akhiran) and s[: -len(akhiran)]:
            s, kali = s[: -len(akhiran)], k
            break
    if re.fullmatch(r"\d+", s):
        pass
    elif kali != 1 and re.fullmatch(r"\d+[.,]\d+", s):                 # 1,5jt / 1.5jt
        s = s.replace(",", ".")
    elif re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+(,\d+)?", s):            # 38.000 / 1.250.000,50
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"[1-9]\d{0,2},\d{3}", s):                        # 1,500 -> ragu
        raise ValueError(f"angka {asli!r} meragukan (1,5 atau 1.500?). {SARAN}")
    elif re.fullmatch(r"\d+,\d+", s):                                   # 2,5 / 38000,50
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d{4,}\.\d{1,2}", s):                           # 38000.5 (format mesin)
        pass
    elif re.fullmatch(r"\d+\.\d+", s):                                  # 38.5 / 0.5 -> ragu
        raise ValueError(f"angka {asli!r} meragukan (titik dibaca ribuan; untuk desimal pakai koma, "
                         f"mis. 38,5; untuk ribuan 38.500). {SARAN}")
    else:
        raise ValueError(f"angka tidak valid: {asli!r}. {SARAN}")
    try:
        d = Decimal(s) * kali
    except InvalidOperation:
        raise ValueError(f"angka tidak valid: {asli!r}. {SARAN}")
    return -d if neg else d


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
        lama = baca_angka(s_lama)
        baru = baca_angka(s_baru)
    except ValueError as e:
        raise ValueError(f"{e} (di {spek!r})")
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
    token_list = [t.strip() for t in s_angka.split(";" if ";" in s_angka else ",") if t.strip()]
    if ";" not in s_angka and len({punya_satuan(t) for t in token_list}) > 1:
        # mis. "1,5jt,2jt" -> "1" | "5jt" | "2jt": koma desimal tertukar dengan pemisah
        raise ValueError(f"daftar {label!r} mencampur angka ber-satuan (rb/jt) dan tanpa satuan dengan pemisah "
                         "koma; bila ada koma desimal, pisahkan dengan titik-koma, mis. 'Omzet=1,5jt;2jt'")
    for token in token_list:
        try:
            angka.append(baca_angka(token))
        except ValueError as e:
            raise ValueError(f"{e} (di daftar {label!r})")
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
