#!/usr/bin/env python3
"""Rekap penjualan dari file CSV. Output: JSON ke stdout.

Hanya memakai library standar Python (3.8+).
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime

BULAN = {
    "jan": 1, "januari": 1, "january": 1,
    "feb": 2, "februari": 2, "february": 2, "peb": 2, "pebruari": 2,
    "mar": 3, "maret": 3, "march": 3,
    "apr": 4, "april": 4,
    "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6,
    "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "nopember": 11,
    "des": 12, "desember": 12, "dec": 12, "december": 12,
}
STATUS_BATAL_DEFAULT = ["batal", "dibatalkan", "cancel", "retur", "return", "refund", "gagal", "failed",
                        "pengembalian", "dikembalikan", "belum bayar", "belum dibayar", "unpaid",
                        "menunggu pembayaran", "kedaluwarsa", "expired"]

# Status yang mengandung kata di atas tetapi transaksinya TETAP sah (mis. "Pengembalian Ditolak")
PENGECUALIAN_STATUS = ["ditolak", "rejected", "dibatalkan pembatalannya"]

POLA_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:[ T].*)?$")
POLA_ANGKA_3 = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})(?:[ T].*)?$")
POLA_NAMA_BULAN = re.compile(r"^(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{2}|\d{4})(?:[ T].*)?$")


def _tahun(t):
    t = int(t)
    return t + 2000 if t < 100 else t


def _buat_tanggal(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def deteksi_urutan(teks_tanggal):
    """Untuk tanggal angka a/b/tahun: 'dmy' (Indonesia) atau 'mdy' (AS). Kembalikan (urutan, ambigu)."""
    dmy_pasti = mdy_pasti = False
    for t in teks_tanggal:
        m = POLA_ANGKA_3.match(t.strip())
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12:
            dmy_pasti = True
        if b > 12:
            mdy_pasti = True
    if mdy_pasti and not dmy_pasti:
        return "mdy", False
    return "dmy", not dmy_pasti  # ambigu bila tidak ada bukti hari > 12


def parse_tanggal(teks, urutan="dmy"):
    teks = (teks or "").strip()
    if not teks:
        return None
    m = POLA_ISO.match(teks)
    if m:
        return _buat_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = POLA_ANGKA_3.match(teks)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), _tahun(m.group(3))
        d, bl = (a, b) if urutan == "dmy" else (b, a)
        return _buat_tanggal(y, bl, d)
    m = POLA_NAMA_BULAN.match(teks)
    if m:
        bl = BULAN.get(m.group(2).lower())
        if bl:
            return _buat_tanggal(_tahun(m.group(3)), bl, int(m.group(1)))
    return None


def _grup_ribuan_valid(bagian_bulat, pemisah):
    """'1.250.000' valid; '15000.500' / '15.00' tidak (grup pertama 1–3 digit, sisanya tepat 3)."""
    grup = bagian_bulat.split(pemisah)
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def parse_angka(teks):
    """Angka format Indonesia/Inggris -> float, atau None bila tidak valid/meragukan.

    Mendukung: '15000', 'Rp 15.000', 'Rp. 25000', 'IDR 25.000', 'Rp 15.000,-',
    '15.000,50', '15,000.50', '1.250.000', '12,5'.
    Menolak (None) format ambigu: '15.000.00', '15000.500', notasi ilmiah '1.5E+06'.
    """
    if teks is None:
        return None
    s = str(teks).strip().lower()
    if not s:
        return None
    if re.fullmatch(r"\(.*\)", s):
        s = "-" + s[1:-1].strip()               # format akuntansi (15.000) = negatif
    if re.search(r"\d\s*e\s*[+-]?\s*\d", s):
        return None                               # notasi ilmiah dari Excel
    s = re.sub(r"\b(rp|idr)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)          # akhiran ',-' atau '.-'
    s = re.sub(r"[^\d,.\-]", "", s).strip(".,")
    if not s or s == "-":
        return None
    negatif = s.startswith("-")
    s = s.lstrip("-")
    if "-" in s:
        return None
    digit = sum(c.isdigit() for c in s)
    if "," in s and "." in s:
        # Pemisah desimal adalah yang muncul terakhir; sisanya wajib grup ribuan yang rapi
        desimal = "," if s.rfind(",") > s.rfind(".") else "."
        ribuan = "." if desimal == "," else ","
        bulat, _, pecahan = s.rpartition(desimal)
        if ribuan in pecahan or not _grup_ribuan_valid(bulat, ribuan):
            return None
        s = bulat.replace(ribuan, "") + "." + pecahan
    elif "," in s or "." in s:
        pemisah = "," if "," in s else "."
        bagian = s.split(pemisah)
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = bagian[0] + "." + bagian[1]       # '12,5' / '1.5' -> desimal
        elif _grup_ribuan_valid(s, pemisah):
            s = s.replace(pemisah, "")            # '15.000' / '1.250.000' -> ribuan
        else:
            return None                           # '15.000.00', '15000.500' -> ambigu
    try:
        nilai = float(s)
    except ValueError:
        return None
    # Pengaman: teks ber-4 digit atau lebih tapi hasil < 1 hampir pasti salah baca
    if digit >= 4 and 0 < nilai < 1:
        return None
    return -nilai if negatif else nilai


def baca_csv(path):
    mentah = open(path, "rb").read()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    contoh = teks[:4096]
    try:
        dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
    except csv.Error:
        dialek = csv.excel
    return list(csv.DictReader(io.StringIO(teks), dialect=dialek)), enc


def keluar_error(data):
    print(json.dumps(data, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="Rekap penjualan dari CSV")
    p.add_argument("file")
    p.add_argument("--kolom-tanggal", required=True)
    p.add_argument("--kolom-produk", required=True)
    p.add_argument("--kolom-qty")
    grup = p.add_mutually_exclusive_group(required=True)
    grup.add_argument("--kolom-total", help="Total harga per baris")
    grup.add_argument("--kolom-harga", help="Harga satuan (dikali qty)")
    p.add_argument("--kolom-status", help="Kolom status pesanan (untuk membuang batal/retur)")
    p.add_argument("--kolom-pesanan",
                   help="Kolom nomor pesanan/transaksi (mis. 'No. Pesanan'); jumlah pesanan per hari dihitung unik. "
                        "Tanpa ini, jumlah transaksi = jumlah baris valid.")
    p.add_argument("--abaikan-status",
                   help="Kata status yang dibuang, pisahkan koma. MENGGANTI seluruh daftar bawaan: "
                        + ", ".join(STATUS_BATAL_DEFAULT))
    p.add_argument("--urutan-tanggal", choices=["auto", "dmy", "mdy"], default="auto",
                   help="Urutan tanggal angka: dmy (hari/bulan/tahun, Indonesia) atau mdy (AS)")
    p.add_argument("--top", type=int, default=5)
    a = p.parse_args()

    try:
        baris, encoding = baca_csv(a.file)
    except OSError as e:
        keluar_error({"error": f"Gagal membaca file: {e}"})

    if not baris:
        keluar_error({"error": "File kosong atau hanya berisi judul kolom"})

    kolom = list(baris[0].keys())
    wajib = [a.kolom_tanggal, a.kolom_produk, a.kolom_total or a.kolom_harga]
    wajib += [k for k in (a.kolom_qty, a.kolom_status, a.kolom_pesanan) if k]
    hilang = [k for k in wajib if k not in kolom]
    if hilang:
        keluar_error({"error": "Kolom tidak ditemukan", "hilang": hilang, "kolom_tersedia": kolom})

    abaikan = STATUS_BATAL_DEFAULT
    if a.abaikan_status:
        abaikan = [x.strip().lower() for x in a.abaikan_status.split(",") if x.strip()]

    if a.urutan_tanggal == "auto":
        urutan, ambigu = deteksi_urutan([r.get(a.kolom_tanggal) or "" for r in baris])
    else:
        urutan, ambigu = a.urutan_tanggal, False

    per_produk = defaultdict(lambda: {"qty": 0.0, "omzet": 0.0})
    nama_tampil = {}                 # kunci ternormalisasi -> nama pertama yang ditemui
    varian_nama = defaultdict(set)   # kunci -> semua ejaan asli
    status_dihitung = defaultdict(int)
    per_hari = defaultdict(float)
    baris_per_hari = defaultdict(int)
    pesanan_per_hari = defaultdict(set)
    dilewati = defaultdict(int)
    dibuang_status = defaultdict(int)
    total, n = 0.0, 0

    for r in baris:
        if a.kolom_status:
            st = (r.get(a.kolom_status) or "").strip()
            st_kecil = st.lower()
            if any(k in st_kecil for k in abaikan) and not any(k in st_kecil for k in PENGECUALIAN_STATUS):
                dibuang_status[st] += 1
                continue
            status_dihitung[st or "(kosong)"] += 1
        tgl = parse_tanggal(r.get(a.kolom_tanggal), urutan)
        if tgl is None:
            dilewati["tanggal tidak terbaca"] += 1
            continue
        teks_qty = (r.get(a.kolom_qty) or "").strip() if a.kolom_qty else ""
        qty = parse_angka(teks_qty) if teks_qty else 1.0   # qty kosong dianggap 1
        if qty is None:
            dilewati["qty tidak valid"] += 1
            continue
        if a.kolom_total:
            nilai = parse_angka(r.get(a.kolom_total))
        else:
            harga = parse_angka(r.get(a.kolom_harga))
            nilai = harga * qty if harga is not None else None
        if nilai is None:
            dilewati["harga/total tidak valid atau meragukan"] += 1
            continue
        asli = " ".join((r.get(a.kolom_produk) or "").split()) or "(tanpa nama)"
        kunci = asli.casefold()
        nama_tampil.setdefault(kunci, asli)
        varian_nama[kunci].add(asli)
        produk = nama_tampil[kunci]
        per_produk[produk]["qty"] += qty
        per_produk[produk]["omzet"] += nilai
        per_hari[tgl.isoformat()] += nilai
        baris_per_hari[tgl.isoformat()] += 1
        if a.kolom_pesanan:
            no = (r.get(a.kolom_pesanan) or "").strip()
            pesanan_per_hari[tgl.isoformat()].add(no or "(baris %d)" % n)
        total += nilai
        n += 1

    if n == 0:
        keluar_error({"error": "Tidak ada baris valid", "alasan": dict(dilewati),
                      "dibuang_karena_status": dict(dibuang_status)})

    urut = sorted(per_produk.items(), key=lambda x: x[1]["omzet"], reverse=True)
    hari = sorted(per_hari.items())
    terbaik = max(hari, key=lambda x: x[1])
    terendah = min(hari, key=lambda x: x[1])
    if a.kolom_pesanan:
        transaksi_harian = {k: len(pesanan_per_hari[k]) for k, _ in hari}
        satuan_transaksi = "pesanan unik (kolom {})".format(a.kolom_pesanan)
    else:
        transaksi_harian = {k: baris_per_hari[k] for k, _ in hari}
        satuan_transaksi = "baris transaksi"
    maks_trx = max(transaksi_harian.values())
    tgl_maks_trx = [k for k, v in transaksi_harian.items() if v == maks_trx]
    awal, akhir = date.fromisoformat(hari[0][0]), date.fromisoformat(hari[-1][0])
    hari_kalender = (akhir - awal).days + 1

    peringatan = []
    if ambigu and any(POLA_ANGKA_3.match((r.get(a.kolom_tanggal) or "").strip()) for r in baris):
        peringatan.append("Urutan tanggal ambigu (tidak ada tanggal > 12); dianggap hari/bulan/tahun. "
                          "Konfirmasi ke pengguna; jika format AS, jalankan ulang dengan --urutan-tanggal mdy.")
    if encoding != "utf-8-sig":
        peringatan.append(f"File dibaca dengan encoding {encoding} (bukan UTF-8).")

    hasil = {
        "periode": {"awal": hari[0][0], "akhir": hari[-1][0],
                    "jumlah_hari_kalender": hari_kalender, "jumlah_hari_ada_penjualan": len(hari)},
        "total_omzet": round(total, 2),
        "jumlah_baris_valid": n,
        "rata_rata_omzet_per_hari_kalender": round(total / hari_kalender, 2),
        "rata_rata_omzet_per_hari_berjualan": round(total / len(hari), 2),
        "produk_terlaris": [
            {"produk": k, "qty": round(v["qty"], 2), "omzet": round(v["omzet"], 2),
             "persen_omzet": round(v["omzet"] / total * 100, 1) if total else 0}
            for k, v in urut[: a.top]
        ],
        "jumlah_produk_unik": len(per_produk),
        "hari_terbaik": {"tanggal": terbaik[0], "omzet": round(terbaik[1], 2)},
        "hari_terendah": {"tanggal": terendah[0], "omzet": round(terendah[1], 2)},
        "omzet_harian": {k: round(v, 2) for k, v in hari},
        "hari_transaksi_terbanyak": {"tanggal": tgl_maks_trx[0], "jumlah": maks_trx,
                                     "semua_tanggal_seri": tgl_maks_trx, "satuan": satuan_transaksi},
        "jumlah_transaksi_harian": transaksi_harian,
        "baris_dilewati": sum(dilewati.values()),
        "alasan_dilewati": dict(dilewati),
        "dibuang_karena_status": dict(dibuang_status),
        "status_dihitung": dict(status_dihitung),
        "nama_produk_digabung": {nama_tampil[k]: sorted(v) for k, v in varian_nama.items() if len(v) > 1},
        "urutan_tanggal_dipakai": urutan,
        "peringatan": peringatan,
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
