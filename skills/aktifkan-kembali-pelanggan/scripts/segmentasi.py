#!/usr/bin/env python3
"""Alat bantu skill aktifkan-kembali-pelanggan: membaca CSV ekspor penjualan,
membagi pelanggan pasif ke segmen berdasarkan hari sejak beli terakhir,
menghitung ringkasan angka, dan menyusun jadwal 3 pesan dalam 4 minggu.

Hanya pustaka standar Python (3.7+). Tidak ada akses jaringan. Tidak mengirim
pesan apa pun: script ini hanya MENGHITUNG. Pesan dikirim manusia satu per satu.
Jalankan dengan `python3` (Windows: `python` atau `py`).

Contoh:
  python3 segmentasi.py data.csv
  python3 segmentasi.py data.csv --hari-ini 2026-10-05 --per-hari 8
  python3 segmentasi.py data.csv --kecualikan jangan-dihubungi.txt --csv-keluar jadwal.csv
  python3 segmentasi.py data.csv --json
"""
import argparse
import csv
import io
import json
import re
import sys
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Segmen: (kode, nama, hari_min, hari_maks) -- hari_maks None = tanpa batas atas
AMBANG_PASIF_DEFAULT = 45
BATAS_SEGMEN = [  # batas bawah hari; ambang pasif dipakai untuk A
    ("B", "Senyap", 91),
    ("C", "Lama hilang", 181),
    ("D", "Sangat lama", 366),
]
NAMA_A = "Baru senyap"
JEDA_PESAN2 = 10   # hari setelah pesan 1
JEDA_PESAN3 = 14   # hari setelah pesan 2 (total 24 hari, di dalam 4 minggu)
PER_HARI_DEFAULT = 10
PER_HARI_MAKS_DISARANKAN = 15

ALIAS = {
    "nama": ["nama", "name", "nama_pelanggan", "pelanggan", "customer", "nama_customer"],
    "hp": ["no_hp", "nohp", "hp", "no_wa", "nowa", "wa", "whatsapp", "telepon", "telp",
           "nomor", "nomor_hp", "nomor_wa", "phone", "no_telepon", "no_telp"],
    "tanggal": ["tanggal_beli_terakhir", "tgl_beli_terakhir", "beli_terakhir", "terakhir_beli",
                "tanggal_terakhir", "tgl_terakhir", "last_order", "last_purchase",
                "tanggal_transaksi_terakhir", "tanggal"],
    "total": ["total_belanja", "total", "belanja", "omzet", "total_pembelian", "nilai",
              "total_transaksi_rp"],
    "produk": ["produk", "produk_terakhir", "produk_dibeli", "barang", "item", "menu", "layanan",
               "nama_produk", "product", "produk_favorit"],
    "transaksi": ["jumlah_transaksi", "jumlah_order", "jml_transaksi", "jml_order",
                  "frekuensi", "order_count"],
}
WAJIB = ["nama", "hp", "tanggal", "total"]

BULAN = {
    "januari": 1, "jan": 1, "februari": 2, "feb": 2, "pebruari": 2, "maret": 3, "mar": 3,
    "april": 4, "apr": 4, "mei": 5, "juni": 6, "jun": 6, "juli": 7, "jul": 7,
    "agustus": 8, "agu": 8, "agt": 8, "ags": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9,
    "oktober": 10, "okt": 10, "oct": 10, "november": 11, "nov": 11, "nopember": 11,
    "desember": 12, "des": 12, "dec": 12,
}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def normalisasi_header(h):
    h = (h or "").strip().lower().lstrip("﻿")
    h = re.sub(r"[\s\-./]+", "_", h)
    return re.sub(r"[^a-z0-9_]", "", h).strip("_")


def petakan_kolom(headers):
    """Kembalikan {kunci: nama_kolom_asli}. Alias lebih awal di daftar menang."""
    norm = {normalisasi_header(h): h for h in headers if h is not None}
    hasil = {}
    for kunci, daftar in ALIAS.items():
        for a in daftar:
            if a in norm:
                hasil[kunci] = norm[a]
                break
    return hasil


def parse_tanggal(teks):
    """Terima dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy, yyyy-mm-dd, '5 Maret 2026'.
    Mengembalikan (date|None, pesan_error|None). Format bulan/hari/tahun TIDAK
    didukung: angka pertama selalu dibaca sebagai hari."""
    s = (teks or "").strip()
    if not s:
        return None, "tanggal kosong"
    s = re.split(r"[ T]\d{1,2}:\d{2}", s)[0].strip()  # buang jam bila ada
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        y, mo, d = int(m[1]), int(m[2]), int(m[3])
    else:
        m = re.fullmatch(r"(\d{1,2})[-/. ](\d{1,2})[-/. ](\d{2}|\d{4})", s)
        if m:
            d, mo, y = int(m[1]), int(m[2]), int(m[3])
            if y < 100:
                y += 2000
        else:
            m = re.fullmatch(r"(\d{1,2})[-/. ]+([A-Za-z]+)[-/. ,]+(\d{2}|\d{4})", s)
            if not m or m[2].lower() not in BULAN:
                return None, "format tanggal tidak dikenali '%s' (pakai dd/mm/yyyy)" % s
            d, mo, y = int(m[1]), BULAN[m[2].lower()], int(m[3])
            if y < 100:
                y += 2000
    try:
        return date(y, mo, d), None
    except ValueError:
        return None, "tanggal tidak ada di kalender '%s' (dibaca dd/mm/yyyy)" % s


def parse_rupiah(teks):
    """'Rp 1.250.000' / '1250000' / '1,250,000' / '1.250.000,50' -> Decimal (rupiah)."""
    s = (teks or "").strip()
    if not s:
        return None, "total belanja kosong"
    s = re.sub(r"(?i)^\s*(rp\.?|idr)\s*", "", s).replace(" ", "")
    if s.startswith("-"):
        return None, "total belanja negatif '%s'" % teks.strip()
    if re.fullmatch(r"\d+", s):
        v = s
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", s):          # 1.250.000(,50)
        v = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", s):          # 1,250,000(.50)
        v = s.replace(",", "")
    elif re.fullmatch(r"\d+[.,]\d{1,2}", s):                    # 1250000,50
        v = s.replace(",", ".")
    else:
        return None, "total belanja bukan angka '%s'" % teks.strip()
    try:
        return Decimal(v).quantize(Decimal("1"), rounding=ROUND_HALF_UP), None
    except InvalidOperation:
        return None, "total belanja bukan angka '%s'" % teks.strip()


def normalisasi_hp(teks):
    """Kembalikan (62xxxxxxxxxx|None, pesan_error|None). Nomor seluler Indonesia saja."""
    s = (teks or "").strip()
    if not s:
        return None, "nomor kosong"
    if re.search(r"\d[eE][+\-]?\d", s) or re.search(r"\.\d+[eE]", s):
        return None, "nomor rusak (format ilmiah Excel '%s'); format kolom sebagai Teks lalu ekspor ulang" % s
    d = re.sub(r"[\s\-.()+_]", "", s)
    if not d.isascii() or not d.isdigit():
        return None, "nomor mengandung huruf/simbol '%s'" % s
    if d.startswith("00"):
        d = d[2:]
    if d.startswith("620"):
        d = "62" + d[3:]
    elif d.startswith("0"):
        d = "62" + d[1:]
    elif d.startswith("8"):
        d = "62" + d
    if not re.fullmatch(r"628\d{8,11}", d):
        return None, "bukan nomor seluler Indonesia yang wajar '%s'" % s
    return d, None


def baca_csv(path):
    with open(path, "rb") as f:
        raw = f.read()
    if b"\x00" in raw[:4096]:
        raise ValueError("file ini bukan CSV teks (tampak berkas biner/Excel .xlsx). Simpan sebagai CSV dulu.")
    for enc in ("utf-8-sig", "cp1252"):
        try:
            teks = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("encoding file tidak dikenali")
    contoh = teks[:2048]
    delim = ";" if contoh.count(";") > contoh.count(",") else ","
    if contoh.count("\t") > max(contoh.count(";"), contoh.count(",")):
        delim = "\t"
    rd = csv.reader(io.StringIO(teks), delimiter=delim)
    baris = [r for r in rd if any(c.strip() for c in r)]
    if not baris:
        raise ValueError("file kosong")
    return baris[0], baris[1:]


def muat_pengecualian(path):
    """Satu nomor atau nama per baris (komentar '#' diabaikan). -> (set_nomor, set_nama)."""
    nomor, nama = set(), set()
    with open(path, encoding="utf-8-sig") as f:
        for ln in f:
            ln = ln.split("#")[0].strip()
            if not ln:
                continue
            h, _ = normalisasi_hp(ln)
            if h:
                nomor.add(h)
            else:
                nama.add(ln.lower())
    return nomor, nama


# ---------------------------------------------------------------------------
# Segmentasi & jadwal
# ---------------------------------------------------------------------------

def segmen_untuk(hari, ambang):
    if hari < ambang:
        return None
    kode, nama = "A", NAMA_A
    for k, n, batas in BATAS_SEGMEN:
        if hari >= batas:
            kode, nama = k, n
    return kode, nama


def geser_dari_minggu(d):
    return d + timedelta(days=1) if d.weekday() == 6 else d  # Minggu -> Senin


def susun_jadwal(pelanggan, mulai, per_hari):
    """Alokasi serakah: pelanggan nilai tertinggi dulu. Maks `per_hari` pesan per
    hari kirim (semua pesan dihitung), tidak ada pengiriman hari Minggu."""
    beban = {}

    def tempatkan(paling_awal):
        d = geser_dari_minggu(paling_awal)
        while beban.get(d, 0) >= per_hari or d.weekday() == 6:
            d += timedelta(days=1)
        beban[d] = beban.get(d, 0) + 1
        return d

    for p in pelanggan:  # sudah terurut prioritas
        d1 = tempatkan(mulai)
        d2 = tempatkan(d1 + timedelta(days=JEDA_PESAN2))
        d3 = tempatkan(d2 + timedelta(days=JEDA_PESAN3))
        p["jadwal"] = [d1, d2, d3]
    return beban


def rupiah(x):
    return "Rp" + "{:,}".format(int(x)).replace(",", ".")


def proses(path, hari_ini, ambang, per_hari, mulai, kecuali_nomor, kecuali_nama, target_balik):
    headers, baris = baca_csv(path)
    kolom = petakan_kolom(headers)
    hilang = [k for k in WAJIB if k not in kolom]
    if hilang:
        raise ValueError(
            "kolom wajib tidak ditemukan: %s. Kolom di file: %s. Nama kolom yang dikenali: "
            "nama, no_hp (atau wa/telepon), tanggal_beli_terakhir, total_belanja."
            % (", ".join(hilang), ", ".join(h for h in headers if h.strip())))
    idx = {k: headers.index(v) for k, v in kolom.items()}

    def sel(r, k):
        i = idx.get(k)
        return r[i].strip() if i is not None and i < len(r) else ""

    ditolak, peringatan, gabung = [], [], {}
    for no, r in enumerate(baris, start=2):  # baris 1 = header
        nama = sel(r, "nama")
        label = nama or "(tanpa nama)"
        hp, e1 = normalisasi_hp(sel(r, "hp"))
        tgl, e2 = parse_tanggal(sel(r, "tanggal"))
        tot, e3 = parse_rupiah(sel(r, "total"))
        galat = [e for e in (e1, e2, e3) if e]
        if not galat and tgl > hari_ini:
            galat.append("tanggal beli terakhir di masa depan (%s)" % tgl.isoformat())
        if galat:
            ditolak.append({"baris": no, "nama": label, "alasan": "; ".join(galat)})
            continue
        trx = 1
        if "transaksi" in idx and sel(r, "transaksi"):
            t = sel(r, "transaksi")
            trx = int(t) if t.isdigit() else 1
        if not nama:
            nama = "[nama pelanggan]"
            peringatan.append("baris %d: nama kosong, ditulis [nama pelanggan]" % no)
        produk = sel(r, "produk")
        if hp in gabung:
            g = gabung[hp]
            if tgl > g["tanggal"] and produk:
                g["produk"] = produk  # produk dari pembelian terbaru
            elif not g["produk"]:
                g["produk"] = produk
            g["tanggal"] = max(g["tanggal"], tgl)
            g["total"] += tot
            g["transaksi"] += trx
            peringatan.append("baris %d: nomor %s sudah ada (%s), digabung: tanggal terbaru, total dijumlahkan"
                              % (no, hp, g["nama"]))
        else:
            gabung[hp] = {"nama": nama, "hp": hp, "tanggal": tgl, "total": tot, "transaksi": trx, "baris": no,
                         "produk": produk}

    aktif, dikecualikan, sasaran = 0, [], []
    for p in gabung.values():
        p["hari"] = (hari_ini - p["tanggal"]).days
        if p["hp"] in kecuali_nomor or p["nama"].lower() in kecuali_nama:
            dikecualikan.append(p)
            continue
        seg = segmen_untuk(p["hari"], ambang)
        if seg is None:
            aktif += 1
            continue
        p["kode"], p["segmen"] = seg
        p["tag"] = "langganan" if p["transaksi"] >= 3 else ("beli %dx" % p["transaksi"] if "transaksi" in idx else "")
        sasaran.append(p)

    sasaran.sort(key=lambda p: (-p["total"], p["hari"], p["nama"].lower()))
    beban = susun_jadwal(sasaran, mulai, per_hari) if sasaran else {}

    ringkas = []
    for kode, nama in [("A", NAMA_A)] + [(k, n) for k, n, _ in BATAS_SEGMEN]:
        isi = [p for p in sasaran if p["kode"] == kode]
        jml = len(isi)
        jumlah_rp = sum((p["total"] for p in isi), Decimal(0))
        rata = (jumlah_rp / jml).quantize(Decimal("1"), rounding=ROUND_HALF_UP) if jml else Decimal(0)
        # nilai belanja segmen = rata-rata belanja x jumlah pelanggan (= jumlah total persis)
        skenario_n = (Decimal(jml) * target_balik / 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        skenario_rp = (jumlah_rp * target_balik / 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        ringkas.append({"kode": kode, "segmen": nama, "jumlah": jml, "rata_rata": rata,
                        "potensi": jumlah_rp, "skenario_pelanggan": skenario_n,
                        "skenario_omzet": skenario_rp})
    return {
        "hari_ini": hari_ini, "ambang": ambang, "baris_dibaca": len(baris),
        "dipakai": len(gabung), "aktif": aktif, "ditolak": ditolak, "peringatan": peringatan,
        "dikecualikan": dikecualikan, "sasaran": sasaran, "ringkas": ringkas,
        "target_balik": target_balik, "per_hari": per_hari, "beban": beban,
        "kolom_dikenali": {k: v for k, v in kolom.items()},
    }


# ---------------------------------------------------------------------------
# Keluaran
# ---------------------------------------------------------------------------

def cetak(h):
    o = []
    o.append("UNTUK AGENT SAJA -- ringkasan hitungan. Jangan tempel mentah ke pengguna; "
             "sampaikan hasilnya dengan bahasa biasa.")
    o.append("Tanggal acuan: %s | Baris data dibaca: %d | Pelanggan unik valid: %d | Ditolak: %d"
             % (h["hari_ini"].isoformat(), h["baris_dibaca"], h["dipakai"], len(h["ditolak"])))
    o.append("Dianggap pasif bila sudah >= %d hari sejak beli terakhir. Masih aktif (tidak dihubungi): %d"
             % (h["ambang"], h["aktif"]))
    if h["dikecualikan"]:
        o.append("Dikecualikan (daftar jangan-dihubungi): %d" % len(h["dikecualikan"]))
    o.append("")
    o.append("SEGMEN (hari sejak beli terakhir)")
    o.append("  A Baru senyap : %d-90 hari | B Senyap : 91-180 | C Lama hilang : 181-365 | D Sangat lama : 366+"
             % h["ambang"])
    o.append("  kode | segmen       | jumlah | rata-rata belanja | nilai belanja (rata-rata x jumlah) | "
             "skenario %s%% kembali" % format(h["target_balik"].normalize(), "f"))
    tot_j = tot_p = tot_s = 0
    for r in h["ringkas"]:
        o.append("  %s    | %-12s | %6d | %17s | %34s | %s"
                 % (r["kode"], r["segmen"], r["jumlah"], rupiah(r["rata_rata"]), rupiah(r["potensi"]),
                    rupiah(r["skenario_omzet"])))
        tot_j += r["jumlah"]; tot_p += r["potensi"]; tot_s += r["skenario_omzet"]
    o.append("  TOTAL: %d pelanggan pasif | nilai belanja historis %s | skenario %s (kira-kira %s pelanggan kembali)"
             % (tot_j, rupiah(tot_p), rupiah(tot_s),
                (Decimal(tot_j) * h["target_balik"] / 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))
    o.append("  Catatan: angka 'nilai belanja' = rata-rata belanja per pelanggan x jumlah (bukan ramalan). "
             "Skenario = ASUMSI persentase kembali yang bisa diubah (--target-balik), bukan janji hasil.")
    o.append("")
    if h["sasaran"]:
        awal = min(p["jadwal"][0] for p in h["sasaran"])
        akhir = max(p["jadwal"][2] for p in h["sasaran"])
        n_pesan = 3 * len(h["sasaran"])
        o.append("JADWAL (%d pelanggan x 3 pesan = %d pesan; maks %d pesan/hari; tanpa hari Minggu; "
                 "mulai %s, selesai paling lambat %s)" % (len(h["sasaran"]), n_pesan, h["per_hari"],
                                                          awal.isoformat(), akhir.isoformat()))
        o.append("  Urutan = nilai belanja terbesar dulu. Pesan 2 & 3 HANYA bila pelanggan belum membalas "
                 "dan tidak komplain/minta berhenti.")
        o.append("  no | segmen | nama | no_wa | hari | total | tag | produk terakhir | pesan1 | pesan2 | pesan3")
        for i, p in enumerate(h["sasaran"], 1):
            j = p["jadwal"]
            o.append("  %d | %s | %s | %s | %d | %s | %s | %s | %s | %s | %s"
                     % (i, p["kode"], p["nama"], p["hp"], p["hari"], rupiah(p["total"]), p["tag"] or "-",
                        p["produk"] or "-", j[0].isoformat(), j[1].isoformat(), j[2].isoformat()))
        if h["per_hari"] > PER_HARI_MAKS_DISARANKAN:
            o.append("  PERINGATAN: > %d pesan/hari dari satu nomor WA terlalu agresif; risiko dianggap spam."
                     % PER_HARI_MAKS_DISARANKAN)
    else:
        o.append("JADWAL: tidak ada pelanggan pasif yang bisa dihubungi.")
    if h["ditolak"]:
        o.append("")
        o.append("PERLU DILENGKAPI / BARIS DITOLAK (%d) -- tidak masuk jadwal:" % len(h["ditolak"]))
        for d in h["ditolak"]:
            o.append("  baris %d | %s | %s" % (d["baris"], d["nama"], d["alasan"]))
    if h["peringatan"]:
        o.append("")
        o.append("CATATAN DATA:")
        for w in h["peringatan"]:
            o.append("  " + w)
    return "\n".join(o)


def tulis_csv(h, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["no", "segmen", "nama", "no_wa", "link_wa", "hari_sejak_beli", "total_belanja",
                    "tag", "produk_terakhir", "pesan_ke", "tanggal_kirim", "status"])
        n = 0
        for p in h["sasaran"]:
            n += 1
            for k, d in enumerate(p["jadwal"], 1):
                w.writerow([n, p["kode"], p["nama"], p["hp"], "https://wa.me/" + p["hp"], p["hari"],
                            int(p["total"]), p["tag"], p["produk"], k, d.isoformat(), "belum"])


def ke_json(h):
    def enc(o):
        if isinstance(o, (date,)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return int(o)
        raise TypeError(type(o))
    d = {k: v for k, v in h.items() if k not in ("beban", "dikecualikan")}
    d["dikecualikan"] = len(h["dikecualikan"])
    d["target_balik"] = float(h["target_balik"])
    return json.dumps(d, default=enc, ensure_ascii=False, indent=2)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Segmentasi pelanggan pasif + jadwal 3 pesan (hanya menghitung).")
    ap.add_argument("csv", help="file CSV ekspor penjualan")
    ap.add_argument("--hari-ini", help="tanggal acuan YYYY-MM-DD (default: hari ini)")
    ap.add_argument("--mulai", help="tanggal pesan pertama YYYY-MM-DD (default: tanggal acuan)")
    ap.add_argument("--aktif-hari", type=int, default=AMBANG_PASIF_DEFAULT,
                    help="pelanggan dianggap pasif bila >= sekian hari sejak beli terakhir (default 45)")
    ap.add_argument("--per-hari", type=int, default=PER_HARI_DEFAULT, help="maks pesan per hari (default 10)")
    ap.add_argument("--target-balik", default="10", help="skenario persen pelanggan yang kembali (default 10)")
    ap.add_argument("--kecualikan", help="file teks: nomor/nama yang JANGAN dihubungi, satu per baris")
    ap.add_argument("--csv-keluar", help="tulis jadwal ke file CSV ini")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    a = ap.parse_args(argv)

    try:
        hari_ini = date.fromisoformat(a.hari_ini) if a.hari_ini else date.today()
        mulai = date.fromisoformat(a.mulai) if a.mulai else hari_ini
        target = Decimal(a.target_balik.replace(",", "."))
        if not (Decimal(0) <= target <= 100):
            raise ValueError("--target-balik harus 0-100")
        if a.per_hari < 1 or a.aktif_hari < 1:
            raise ValueError("--per-hari dan --aktif-hari minimal 1")
    except (ValueError, InvalidOperation) as e:
        print("Argumen tidak valid: %s" % e, file=sys.stderr)
        return 2
    kn, kna = set(), set()
    try:
        if a.kecualikan:
            kn, kna = muat_pengecualian(a.kecualikan)
        h = proses(a.csv, hari_ini, a.aktif_hari, a.per_hari, mulai, kn, kna, target)
    except FileNotFoundError as e:
        print("File tidak ditemukan: %s" % e.filename, file=sys.stderr)
        return 2
    except (ValueError, OSError, csv.Error) as e:
        print("Tidak bisa memproses: %s" % e, file=sys.stderr)
        return 2
    if a.csv_keluar:
        tulis_csv(h, a.csv_keluar)
    print(ke_json(h) if a.json else cetak(h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
