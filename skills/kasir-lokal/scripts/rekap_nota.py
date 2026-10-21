#!/usr/bin/env python3
"""rekap_nota.py (kasir-lokal, Komunitech) - rekap dari daftar nota yang DITEMPEL di chat.

Untuk pemilik yang belum memakai database kasir: daftar nota (teks bebas per baris, blok
"Nota 001 ...", atau CSV) dihitung tanpa menyimpan apa pun:
  - nota BATAL/void DIKECUALIKAN (didaftar terpisah),
  - qty per menu (porsi) dan jumlah nota per menu dihitung TERPISAH,
  - rupiah per metode bayar, bon (belum dibayar) dipisah dari uang masuk,
  - opsional cocok laci (--kas-awal, --kas-fisik),
  - "RINGKASAN SIAP TEMPEL untuk grup": agregat saja, tanpa nama/nomor pelanggan dan tanpa
    rincian bon per orang.

Hanya library standar Python 3.8+, tanpa jaringan, tidak menulis file (kecuali --csv).

Contoh:
  python3 rekap_nota.py nota.txt --tanggal "Sabtu, 3 Oktober 2026" --kas-awal 300rb --kas-fisik 441rb
  python3 rekap_nota.py - < nota.txt --json
  python3 rekap_nota.py --teks "Nota 001: 2 Kopi Susu @18rb - tunai" --json

Format teks yang dibaca (satu nota per baris, atau baris "Nota X" diikuti baris item sampai baris kosong):
  Nota 001: 2 Kopi Susu @18.000, 1 Roti Bakar Coklat @15rb - tunai
  Nota 005 - Pak Hendra (0812-xxx) - 4 Nasi Goreng Kampung = 100.000 - transfer
  Nota 011: 1 Kopi Susu 18rb - tunai - BATAL
  012 | Es Kopi Susu x1 | 20rb | qris
Harga: "@18rb" = harga satuan; angka lain ("= 36.000", "36rb", "Rp36.000") = jumlah baris.
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import OrderedDict
from decimal import ROUND_HALF_UP, Decimal

VERSI = "1.1.8"

METODE_LABEL = OrderedDict([
    ("tunai", "Tunai"), ("qris", "QRIS"), ("transfer", "Transfer"), ("debit", "Kartu debit/kredit"),
    ("ewallet", "E-wallet"), ("bon", "Bon (belum dibayar)"),
])
RE_METODE = [
    ("bon", r"\b(bon|ngebon|utang|hutang|ngutang|piutang|kasbon|belum\s+(?:di)?bayar|bayar\s+nanti|tempo)\b"),
    ("qris", r"\bqris\b"),
    ("transfer", r"\b(transfer|tf|trf|bca|bri|bni|mandiri|bsi)\b"),
    ("debit", r"\b(debit|kartu\s+kredit|edc)\b"),
    ("ewallet", r"\b(gopay|ovo|dana|shopeepay|linkaja|e-?wallet)\b"),
    ("tunai", r"\b(tunai|cash|kontan)\b"),
]
RE_BATAL = re.compile(r"\b(batal|dibatalkan|void|cancel|cancelled|canceled)\b", re.I)
RE_PENGGANTI = re.compile(r"\b(pengganti|ganti|gantinya|diganti|koreksi|menggantikan)\b", re.I)
RE_HEADER_NOTA = re.compile(
    r"^\s*[-*•]?\s*(?:nota|no\.?\s*nota|struk|trx|transaksi)\s*(?:no\.?)?\s*[#:.]?\s*"
    r"([A-Za-z]{0,4}[-/]?\d[\w\-/]*)\s*[:.)\-–—|]?\s*(.*)$", re.I)
RE_HEADER_ANGKA = re.compile(r"^\s*[-*•]?\s*#?(\d{1,6})\s*[.):|\-–—]\s+(.*)$")
RE_TELP = re.compile(r"(?:\+?62[\s\-.]?|\b0)8\d{1,4}(?:[\-. ]?\d{2,5}){1,4}\b")
RE_JAM = re.compile(r"\b(?:jam\s*)?\d{1,2}[:.]\d{2}(?:\s*(?:wib|wita|wit))?\b(?!\d)", re.I)
RE_HONORIFIK = re.compile(r"\b(pak|bu|bpk|ibu|mas|mbak|mba|kak|bang|om|tante|a\.?\s?n\.?|atas\s+nama|pelanggan|cust(?:omer)?)\b.*$",
                          re.I)
SATUAN = r"(?:x|×|pcs|porsi|gelas|cup|bks|bungkus|buah|bh|piring|botol|btl|mangkok|mangkuk|potong|ptg|pack|pak)"
KATA_ANGKA = {"satu": 1, "se": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6, "tujuh": 7,
              "delapan": 8, "sembilan": 9, "sepuluh": 10}
RE_PENGISI = re.compile(r"\b(bayar|dibayar|lunas|total|jumlah|ttl|nota|menu|pesanan|order)\b", re.I)


class Gagal(Exception):
    pass


# ---------------------------------------------------------------------------
# Angka & rupiah
# ---------------------------------------------------------------------------


def bulat(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rp(n):
    s = "{:,}".format(bulat(n)).replace(",", ".")
    return "Rp " + s if not s.startswith("-") else "-Rp " + s[1:]


def fqty(q):
    q = Decimal(q)
    if q == q.to_integral_value():
        return str(int(q))
    return ("%s" % q.normalize()).replace(".", ",")


def _grup_ok(bagian):
    return 1 <= len(bagian[0]) <= 3 and all(len(x) == 3 for x in bagian[1:])


def parse_rp(teks):
    """'18.000', 'Rp 18.000', '18rb', '18 ribu', '18k', '1,5jt', '18000' -> Decimal; None bila bukan angka."""
    if teks is None:
        return None
    s = str(teks).strip().lower()
    s = re.sub(r"^(rp|idr)\.?\s*", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s).strip()
    kali = Decimal(1)
    m = re.search(r"\s*(jt|juta|rb|ribu|k)$", s)
    if m:
        kali = Decimal(1000000) if m.group(1) in ("jt", "juta") else Decimal(1000)
        s = s[:m.start()].strip()
    if not re.fullmatch(r"\d[\d.,]*", s or ""):
        return None
    if "," in s and "." in s:
        return None
    pem = "," if "," in s else ("." if "." in s else None)
    if pem:
        bag = s.split(pem)
        if kali != 1 and len(bag) == 2:
            s = bag[0] + "." + bag[1]
        elif _grup_ok(bag):
            s = s.replace(pem, "")
        else:
            return None
    try:
        return Decimal(s) * kali
    except ArithmeticError:
        return None


def parse_qty(teks):
    s = str(teks).strip().lower()
    if s in KATA_ANGKA:
        return Decimal(KATA_ANGKA[s])
    if re.fullmatch(r"\d+(?:[.,]\d+)?", s):
        return Decimal(s.replace(",", "."))
    return None


# ---------------------------------------------------------------------------
# Parsing nota
# ---------------------------------------------------------------------------

RE_ANGKA_RP = r"(?:rp\.?\s*)?\d[\d.,]*\s*(?:rb|ribu|k|jt|juta)?"


def deteksi_metode(teks):
    t = teks.lower()
    ada = []
    for kode, pola in RE_METODE:
        if re.search(pola, t):
            ada.append(kode)
    return ada


def deteksi_batal(teks):
    for m in RE_BATAL.finditer(teks):
        sebelum = teks[max(0, m.start() - 30):m.start()]
        if RE_PENGGANTI.search(sebelum):
            continue
        return True
    return False


def bersihkan_nama(nama):
    asli = nama
    nama = RE_HONORIFIK.sub("", nama)
    buang_nama_orang = nama.strip() != asli.strip()
    for _, pola in RE_METODE:
        nama = re.sub(pola, " ", nama, flags=re.I)
    nama = RE_BATAL.sub(" ", nama)
    nama = RE_PENGISI.sub(" ", nama)
    nama = re.sub(r"[^\w\s&'/\-]", " ", nama)
    nama = re.sub(r"\s+", " ", nama).strip(" -/'&")
    return nama, buang_nama_orang


def parse_segmen(seg):
    """Kembalikan dict item, ('total', Decimal), atau None (bukan item)."""
    s = seg.strip()
    if not s:
        return None
    low = s.lower()
    m = re.match(r"^(?:total|jumlah|ttl|grand\s*total)\b\s*[:=]?\s*(" + RE_ANGKA_RP + r")\s*$", low)
    if m:
        v = parse_rp(m.group(1))
        return ("total", v) if v is not None else None
    harga_satuan = subtotal = None
    m = re.search(r"@\s*(" + RE_ANGKA_RP + r")", s, re.I)
    if m:
        harga_satuan = parse_rp(m.group(1))
        s = s[:m.start()] + " " + s[m.end():]
    m = re.search(r"=\s*(" + RE_ANGKA_RP + r")", s, re.I)
    if m:
        subtotal = parse_rp(m.group(1))
        s = s[:m.start()] + " " + s[m.end():]
    if subtotal is None:
        # angka rupiah tanpa @: "Rp36.000", "36rb", "36.000" (ribuan bertitik)
        m = re.search(r"(?:rp\.?\s*\d[\d.,]*\s*(?:rb|ribu|k|jt)?|\b\d+(?:[.,]\d+)?\s*(?:rb|ribu|k|jt)\b|\b\d{1,3}(?:\.\d{3})+\b)",
                      s, re.I)
        if m:
            v = parse_rp(m.group(0))
            if v is not None:
                subtotal = v
                s = s[:m.start()] + " " + s[m.end():]
    s = re.sub(r"\s+", " ", s).strip(" -:")
    qty = None
    m = re.match(r"^(\d+(?:[.,]\d+)?|" + "|".join(KATA_ANGKA) + r")\s*" + SATUAN + r"?\.?\s+(.+)$", s, re.I)
    if m and parse_qty(m.group(1)) is not None:
        qty, nama = parse_qty(m.group(1)), m.group(2)
    else:
        m = re.match(r"^(.+?)\s*(?:x|×)\s*(\d+(?:[.,]\d+)?)$", s, re.I) or \
            re.match(r"^(.+?)\s+(\d+(?:[.,]\d+)?)\s*" + SATUAN + r"?$", s, re.I)
        if m:
            qty, nama = parse_qty(m.group(2)), m.group(1)
        else:
            nama = s
    punya_bayar = bool(deteksi_metode(seg))
    if qty is None:
        if harga_satuan is None and subtotal is None:
            return None  # mis. nama pelanggan, "tunai"
        if punya_bayar:
            return None  # "tunai 50rb", "transfer 100rb" = nominal bayar, bukan item
    nama, buang = bersihkan_nama(nama)
    if not re.search(r"[A-Za-z]", nama):
        return None
    if qty is None:
        qty = Decimal(1)
        asumsi_qty = True
    else:
        asumsi_qty = False
    if qty <= 0:
        return None
    if subtotal is None and harga_satuan is not None:
        subtotal = Decimal(bulat(qty * harga_satuan))
    return {"menu": nama, "qty": qty, "harga_satuan": harga_satuan, "subtotal": subtotal,
            "asumsi_qty_1": asumsi_qty, "nama_orang_dibuang": buang}


def pecah_segmen(teks):
    t = RE_TELP.sub(" ", teks)
    t = re.sub(r"\S+@\S+\.\w+", " ", t)
    t = RE_JAM.sub(" ", t)
    t = t.replace("(", ",").replace(")", ",").replace("[", ",").replace("]", ",")
    bag = re.split(r"[,;|\n+&]|\s[-–—]\s|\s[-–—]|[-–—]\s|\bdan\b", t)
    return [b for b in (x.strip() for x in bag) if b]


def kunci_menu(nama):
    return re.sub(r"\s+", " ", nama.strip().lower())


def tampil_menu(nama):
    return " ".join(w if (w.isupper() and len(w) <= 4) else w[:1].upper() + w[1:].lower() for w in nama.split())


def baca_teks(teks):
    """Kembalikan list blok (id, teks_nota, nomor_baris)."""
    baris = teks.splitlines()
    ada_nota_kata = any(RE_HEADER_NOTA.match(b) for b in baris)
    blok, cur, diabaikan = [], None, []
    for i, b in enumerate(baris, 1):
        if not b.strip():
            if cur:
                blok.append(cur)
                cur = None
            continue
        m = RE_HEADER_NOTA.match(b) if ada_nota_kata else RE_HEADER_ANGKA.match(b)
        if m:
            if cur:
                blok.append(cur)
            cur = {"id": m.group(1).strip(), "teks": m.group(2), "baris": i}
        elif cur:
            cur["teks"] += "\n" + b
        elif ada_nota_kata:
            diabaikan.append({"baris": i, "teks": b.strip(), "alasan": "di luar blok nota"})
        else:
            # tanpa penanda nota sama sekali: tiap baris = satu nota
            blok.append({"id": None, "teks": b, "baris": i})
    if cur:
        blok.append(cur)
    n = 0
    for bk in blok:
        n += 1
        if bk["id"] is None:
            bk["id"] = "%03d" % n
    return blok, diabaikan


def nota_dari_blok(bk, peringatan, diabaikan):
    teks = bk["teks"]
    nota = {"id": bk["id"], "baris": bk["baris"], "item": [], "batal": deteksi_batal(teks), "total_ditulis": None}
    metode = deteksi_metode(teks)
    if "bon" in metode:
        nota["metode"] = "bon"
    elif len(metode) == 1:
        nota["metode"] = metode[0]
    elif not metode:
        nota["metode"] = "tidak-disebut"
    else:
        nota["metode"] = "campuran"
    for seg in pecah_segmen(teks):
        h = parse_segmen(seg)
        if h is None:
            if not deteksi_metode(seg) and not RE_BATAL.search(seg) and re.search(r"[A-Za-z]", seg):
                diabaikan.append({"nota": bk["id"], "teks": seg, "alasan": "bukan item (tanpa jumlah/harga)"})
            continue
        if isinstance(h, tuple):
            nota["total_ditulis"] = h[1]
            continue
        nota["item"].append(h)
    return nota


def baca_csv(teks):
    try:
        dialek = csv.Sniffer().sniff(teks[:2048], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    rows = list(csv.reader(io.StringIO(teks), dialek))
    if not rows:
        raise Gagal("File CSV kosong.")
    hdr = [re.sub(r"[^a-z]", "", h.lower()) for h in rows[0]]

    def cari(*nama):
        for n in nama:
            if n in hdr:
                return hdr.index(n)
        return None
    k = {"nota": cari("nota", "nonota", "no", "nomornota", "idnota"),
         "menu": cari("menu", "produk", "item", "namamenu", "namaproduk", "barang"),
         "qty": cari("qty", "jumlah", "porsi", "kuantitas", "banyak"),
         "harga": cari("harga", "hargasatuan"),
         "subtotal": cari("subtotal", "totalbaris", "jumlahrp", "nilai", "total"),
         "bayar": cari("bayar", "metode", "carabayar", "metodebayar", "pembayaran"),
         "status": cari("status", "keterangan", "ket", "catatan")}
    if k["nota"] is None or k["menu"] is None:
        raise Gagal("CSV perlu kolom nota dan menu/produk. Kolom terbaca: %s" % ", ".join(rows[0]))
    notas = OrderedDict()
    peringatan = []

    def sel(r, kol):
        return r[k[kol]].strip() if k[kol] is not None and k[kol] < len(r) else ""
    for no, r in enumerate(rows[1:], 2):
        if not any(c.strip() for c in r):
            continue
        nid = sel(r, "nota")
        if not nid:
            peringatan.append("Baris %d: nomor nota kosong, dilewati." % no)
            continue
        n = notas.setdefault(nid, {"id": nid, "baris": no, "item": [], "batal": False, "total_ditulis": None,
                                   "_metode": set()})
        if deteksi_batal(sel(r, "status")):
            n["batal"] = True
        m = deteksi_metode(sel(r, "bayar") + " " + sel(r, "status"))
        n["_metode"].update(m)
        qty = parse_qty(sel(r, "qty") or "1")
        if qty is None or qty <= 0:
            peringatan.append("Baris %d: jumlah '%s' tidak terbaca, baris dilewati." % (no, sel(r, "qty")))
            continue
        harga = parse_rp(sel(r, "harga")) if sel(r, "harga") else None
        sub = parse_rp(sel(r, "subtotal")) if sel(r, "subtotal") else None
        if sub is None and harga is not None:
            sub = Decimal(bulat(qty * harga))
        nama, buang = bersihkan_nama(sel(r, "menu"))
        if not nama:
            peringatan.append("Baris %d: nama menu kosong, dilewati." % no)
            continue
        n["item"].append({"menu": nama, "qty": qty, "harga_satuan": harga, "subtotal": sub,
                          "asumsi_qty_1": not sel(r, "qty"), "nama_orang_dibuang": buang})
    for n in notas.values():
        m = n.pop("_metode")
        n["metode"] = "bon" if "bon" in m else (m.pop() if len(m) == 1 else ("tidak-disebut" if not m else "campuran"))
    return list(notas.values()), peringatan, []


def tampak_csv(teks):
    pertama = teks.strip().splitlines()[0].lower() if teks.strip() else ""
    return bool(re.search(r"\bnota\b|\bno\b", pertama)) and bool(re.search(r"menu|produk|item|barang", pertama)) \
        and bool(re.search(r"[,;\t]", pertama)) and "@" not in pertama


# ---------------------------------------------------------------------------
# Hitung
# ---------------------------------------------------------------------------


def hitung(notas, batal_paksa=(), bukan_batal=(), kas_awal=None, kas_fisik=None, kas_masuk=Decimal(0),
           kas_keluar=Decimal(0)):
    peringatan, perlu_dicek = [], []
    batal_paksa = {x.strip() for x in batal_paksa if x.strip()}
    bukan_batal = {x.strip() for x in bukan_batal if x.strip()}
    terlihat = {}
    sah, batal = [], []
    for n in notas:
        if n["id"] in batal_paksa:
            n["batal"] = True
        if n["id"] in bukan_batal:
            n["batal"] = False
        if n["id"] in terlihat:
            perlu_dicek.append("Nomor nota %s muncul lebih dari sekali (baris %s dan %s); keduanya dihitung. Kalau "
                               "tertempel dobel, hapus salah satu lalu ulangi." % (n["id"], terlihat[n["id"]], n["baris"]))
        terlihat[n["id"]] = n["baris"]
        if not n["item"]:
            perlu_dicek.append("Nota %s: tidak ada item yang terbaca (tulis seperti '2 Kopi Susu @18rb')." % n["id"])
        lengkap = all(it["subtotal"] is not None for it in n["item"])
        jumlah_item = sum((it["subtotal"] for it in n["item"] if it["subtotal"] is not None), Decimal(0))
        if n["item"] and lengkap:
            n["jumlah"] = jumlah_item
            if n["total_ditulis"] is not None and n["total_ditulis"] != jumlah_item:
                perlu_dicek.append("Nota %s: total tertulis %s, tetapi jumlah item %s. Dipakai jumlah item; cek nota."
                                   % (n["id"], rp(n["total_ditulis"]), rp(jumlah_item)))
        elif n["total_ditulis"] is not None:
            n["jumlah"] = n["total_ditulis"]
            if n["item"]:
                peringatan.append("Nota %s: sebagian item tanpa harga; dipakai total tertulis %s (rupiah per menu "
                                  "untuk nota ini tidak lengkap)." % (n["id"], rp(n["total_ditulis"])))
        else:
            n["jumlah"] = None
        for it in n["item"]:
            if it["asumsi_qty_1"]:
                peringatan.append("Nota %s: jumlah '%s' tidak ditulis, dianggap 1." % (n["id"], tampil_menu(it["menu"])))
            if it["nama_orang_dibuang"]:
                peringatan.append("Nota %s: bagian yang tampak seperti nama orang dibuang dari nama menu '%s'."
                                  % (n["id"], tampil_menu(it["menu"])))
        (batal if n["batal"] else sah).append(n)
    for n in sah:
        if n["jumlah"] is None:
            perlu_dicek.append("Nota %s: tidak ada harga/total, rupiahnya belum bisa dihitung." % n["id"])
        if n["metode"] == "tidak-disebut":
            perlu_dicek.append("Nota %s: cara bayar tidak disebut (tunai/QRIS/transfer/bon?)." % n["id"])
        if n["metode"] == "campuran":
            perlu_dicek.append("Nota %s: lebih dari satu cara bayar; tidak dimasukkan ke rincian per metode. "
                               "Pisahkan nominalnya per metode." % n["id"])
    # harga satuan tidak konsisten
    hs = {}
    for n in sah:
        for it in n["item"]:
            if it["subtotal"] is not None and it["qty"]:
                hs.setdefault(kunci_menu(it["menu"]), set()).add(Decimal(it["subtotal"]) / it["qty"])
    for km, vals in hs.items():
        if len(vals) > 1:
            perlu_dicek.append("Harga per porsi '%s' berbeda antar nota (%s). Cek apakah angka di nota itu harga satuan "
                               "(pakai @) atau jumlah baris." % (tampil_menu(km), ", ".join(rp(v) for v in sorted(vals))))

    menu = OrderedDict()
    for n in sah:
        dilihat = set()
        for it in n["item"]:
            km = kunci_menu(it["menu"])
            m = menu.setdefault(km, {"menu": tampil_menu(it["menu"]), "porsi": Decimal(0), "nota": 0,
                                     "omzet": Decimal(0), "omzet_lengkap": True})
            m["porsi"] += it["qty"]
            if km not in dilihat:
                m["nota"] += 1
                dilihat.add(km)
            if it["subtotal"] is None:
                m["omzet_lengkap"] = False
            else:
                m["omzet"] += it["subtotal"]
    daftar_menu = sorted(menu.values(), key=lambda m: (-m["porsi"], -m["omzet"], m["menu"]))

    per_metode = OrderedDict((k, {"nota": 0, "jumlah": Decimal(0)}) for k in METODE_LABEL)
    for n in sah:
        if n["metode"] in per_metode and n["jumlah"] is not None:
            per_metode[n["metode"]]["nota"] += 1
            per_metode[n["metode"]]["jumlah"] += n["jumlah"]
    rupiah_lengkap = all(n["jumlah"] is not None and n["metode"] in per_metode for n in sah)
    omzet = sum((n["jumlah"] for n in sah if n["jumlah"] is not None), Decimal(0))
    bon = per_metode["bon"]
    uang_masuk = sum((v["jumlah"] for k, v in per_metode.items() if k != "bon"), Decimal(0))
    kas = None
    if kas_awal is not None:
        seharusnya = kas_awal + per_metode["tunai"]["jumlah"] + kas_masuk - kas_keluar
        kas = {"kas_awal": kas_awal, "tunai": per_metode["tunai"]["jumlah"], "kas_masuk": kas_masuk,
               "kas_keluar": kas_keluar, "seharusnya": seharusnya}
        if kas_fisik is not None:
            kas["fisik"] = kas_fisik
            kas["selisih"] = kas_fisik - seharusnya
    return {"sah": sah, "batal": batal, "menu": daftar_menu, "per_metode": per_metode, "omzet": omzet,
            "uang_masuk": uang_masuk, "bon": bon, "rupiah_lengkap": rupiah_lengkap,
            "porsi_total": sum((m["porsi"] for m in daftar_menu), Decimal(0)), "kas": kas,
            "peringatan": peringatan, "perlu_dicek": perlu_dicek}


def label_selisih(s):
    if s == 0:
        return "PAS (selisih Rp 0)"
    return ("LEBIH %s" if s > 0 else "KURANG %s") % rp(abs(s))


def teks_pemilik(h, tanggal):
    t = ["REKAP DARI NOTA TEMPEL%s (untuk pemilik)" % (" - " + tanggal if tanggal else "")]
    t.append("Nota sah: %d | nota batal (tidak dihitung): %d%s" % (
        len(h["sah"]), len(h["batal"]), (" -> " + ", ".join(n["id"] for n in h["batal"])) if h["batal"] else ""))
    t.append("Total porsi/qty terjual: %s" % fqty(h["porsi_total"]))
    t.append("Omzet tercatat (termasuk bon): %s%s" % (rp(h["omzet"]), "" if h["rupiah_lengkap"] else " (BELUM LENGKAP, lihat PERLU DICEK)"))
    t.append("Uang masuk (tanpa bon): %s" % rp(h["uang_masuk"]))
    t.append("Per cara bayar:")
    for k, v in h["per_metode"].items():
        if v["nota"]:
            ids = [n["id"] for n in h["sah"] if n["metode"] == k]
            t.append("- %-20s %s (%d nota: %s)" % (METODE_LABEL[k], rp(v["jumlah"]), v["nota"], ", ".join(ids)))
    t.append("Per menu (porsi | nota | rupiah):")
    for i, m in enumerate(h["menu"], 1):
        t.append("%d. %s - %s porsi - %d nota - %s%s" % (i, m["menu"], fqty(m["porsi"]), m["nota"], rp(m["omzet"]),
                                                        "" if m["omzet_lengkap"] else " (sebagian tanpa harga)"))
    if h["kas"]:
        k = h["kas"]
        t.append("Cocok laci: kas awal %s + tunai %s%s%s = seharusnya %s" % (
            rp(k["kas_awal"]), rp(k["tunai"]), (" + kas masuk %s" % rp(k["kas_masuk"])) if k["kas_masuk"] else "",
            (" - kas keluar %s" % rp(k["kas_keluar"])) if k["kas_keluar"] else "", rp(k["seharusnya"])))
        if "fisik" in k:
            t.append("Uang fisik %s -> %s" % (rp(k["fisik"]), label_selisih(k["selisih"])))
            if k["selisih"] != 0:
                t.append("Kemungkinan: kembalian keliru, pengeluaran kecil dari laci belum dicatat, QRIS/transfer "
                         "tercatat tunai, atau salah hitung. Cek dulu, jangan menuduh siapa pun.")
    if h["bon"]["nota"]:
        t.append("Bon belum dibayar: %d nota, %s -> catat di buku-piutang (rincian nama TIDAK untuk grup karyawan)."
                 % (h["bon"]["nota"], rp(h["bon"]["jumlah"])))
    return "\n".join(t)


def teks_grup(h, tanggal, tanpa_rupiah=False, top=3):
    t = ["RINGKASAN SIAP TEMPEL untuk grup%s" % (" - " + tanggal if tanggal else "")]
    t.append("Nota sah: %d%s" % (len(h["sah"]), (" (%d nota batal tidak dihitung)" % len(h["batal"])) if h["batal"] else ""))
    t.append("Total terjual: %s porsi" % fqty(h["porsi_total"]))
    if h["menu"]:
        t.append("Menu terlaris (porsi):")
        for i, m in enumerate(h["menu"][:top], 1):
            t.append("%d. %s - %s porsi (%d nota)" % (i, m["menu"], fqty(m["porsi"]), m["nota"]))
    if not tanpa_rupiah:
        t.append("Omzet tercatat: %s" % rp(h["omzet"]))
        rinci = ", ".join("%s %s" % (METODE_LABEL[k], rp(v["jumlah"])) for k, v in h["per_metode"].items()
                          if v["nota"] and k != "bon")
        t.append("Uang masuk: %s%s" % (rp(h["uang_masuk"]), (" (" + rinci + ")") if rinci else ""))
        if h["bon"]["nota"]:
            t.append("Bon belum dibayar: %d nota, total %s (dicatat pemilik)" % (h["bon"]["nota"], rp(h["bon"]["jumlah"])))
        if h["kas"] and "selisih" in h["kas"]:
            t.append("Laci: %s" % label_selisih(h["kas"]["selisih"]))
    return "\n".join(t)


def ke_json(x):
    if isinstance(x, Decimal):
        return int(x) if x == x.to_integral_value() else float(x)
    if isinstance(x, dict):
        return {k: ke_json(v) for k, v in x.items() if not k.startswith("_")}
    if isinstance(x, (list, tuple)):
        return [ke_json(v) for v in x]
    return x


def rekap_dari_teks(teks, **opsi):
    if tampak_csv(teks):
        notas, peringatan_baca, diabaikan = baca_csv(teks)
        sumber = "csv"
    else:
        blok, diabaikan = baca_teks(teks)
        peringatan_baca = []
        notas = [nota_dari_blok(b, peringatan_baca, diabaikan) for b in blok]
        sumber = "teks"
    if not notas:
        raise Gagal("Tidak ada nota yang terbaca. Tempel nota satu per baris, mis. "
                    "'Nota 001: 2 Kopi Susu @18rb - tunai'.")
    tanggal = opsi.pop("tanggal", "") or ""
    tanpa_rupiah = opsi.pop("tanpa_rupiah", False)
    h = hitung(notas, **opsi)
    h["peringatan"] = peringatan_baca + h["peringatan"]
    h["sumber"] = sumber
    h["diabaikan"] = diabaikan
    h["teks"] = teks_pemilik(h, tanggal)
    if h["perlu_dicek"]:
        h["teks"] += "\nPERLU DICEK (%d):\n" % len(h["perlu_dicek"]) + "\n".join("- " + p for p in h["perlu_dicek"])
    h["teks_grup"] = teks_grup(h, tanggal, tanpa_rupiah)
    return h


def ringkas_json(h):
    nota = [{"id": n["id"], "metode": n["metode"], "jumlah": n["jumlah"],
             "item": [{"menu": tampil_menu(i["menu"]), "qty": i["qty"], "subtotal": i["subtotal"]} for i in n["item"]]}
            for n in h["sah"]]
    out = {"ok": True, "versi": VERSI, "mode": "baca", "sumber": h["sumber"],
           "nota_sah": len(h["sah"]), "nota_batal": [n["id"] for n in h["batal"]],
           "porsi_total": h["porsi_total"], "omzet_tercatat": h["omzet"], "uang_masuk": h["uang_masuk"],
           "rupiah_lengkap": h["rupiah_lengkap"],
           "per_metode": {k: v for k, v in h["per_metode"].items() if v["nota"]},
           "menu": h["menu"], "kas": h["kas"], "nota": nota,
           "peringatan": h["peringatan"], "perlu_dicek": h["perlu_dicek"],
           "diabaikan": h["diabaikan"], "teks": h["teks"], "teks_grup": h["teks_grup"]}
    return ke_json(out)


def angka_opsi(teks, nama):
    if teks is None:
        return None
    v = parse_rp(teks)
    if v is None:
        raise Gagal("Angka %s '%s' tidak terbaca. Contoh: 300000, Rp 300.000, 300rb." % (nama, teks))
    return v


def main(argv=None):
    p = argparse.ArgumentParser(description="Rekap dari nota yang ditempel (tanpa database).", allow_abbrev=False)
    p.add_argument("sumber", nargs="?", default=None, help="File teks/CSV nota, atau - untuk stdin")
    p.add_argument("--teks", help="Isi nota langsung sebagai teks")
    p.add_argument("--tanggal", default="", help="Label tanggal untuk judul, mis. 'Sabtu, 3 Oktober 2026'")
    p.add_argument("--batal", default="", help="Nomor nota yang dipaksa dianggap batal, pisah koma")
    p.add_argument("--bukan-batal", default="", help="Nomor nota yang terdeteksi batal tetapi sebenarnya sah")
    p.add_argument("--kas-awal")
    p.add_argument("--kas-fisik")
    p.add_argument("--kas-masuk", default="0")
    p.add_argument("--kas-keluar", default="0")
    p.add_argument("--grup-tanpa-rupiah", action="store_true", help="Ringkasan grup tanpa angka rupiah")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    try:
        if a.teks is not None:
            teks = a.teks
        elif a.sumber in (None, "-"):
            teks = sys.stdin.read()
        else:
            with open(a.sumber, "rb") as f:
                mentah = f.read()
            for enc in ("utf-8-sig", "cp1252"):
                try:
                    teks = mentah.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
        kas_fisik = angka_opsi(a.kas_fisik, "kas fisik")
        kas_awal = angka_opsi(a.kas_awal, "kas awal")
        if kas_fisik is not None and kas_awal is None:
            raise Gagal("Untuk cocok laci, isi juga --kas-awal (modal laci pagi).")
        h = rekap_dari_teks(teks, tanggal=a.tanggal, tanpa_rupiah=a.grup_tanpa_rupiah,
                            batal_paksa=a.batal.split(","), bukan_batal=a.bukan_batal.split(","),
                            kas_awal=kas_awal, kas_fisik=kas_fisik,
                            kas_masuk=angka_opsi(a.kas_masuk, "kas masuk"),
                            kas_keluar=angka_opsi(a.kas_keluar, "kas keluar"))
    except (Gagal, OSError) as e:
        pesan = str(e) if isinstance(e, Gagal) else "File tidak bisa dibaca: %s" % e
        if a.json:
            print(json.dumps({"ok": False, "error": pesan}, ensure_ascii=False))
        else:
            print("GAGAL: " + pesan, file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(ringkas_json(h), ensure_ascii=False, indent=1))
    else:
        print(h["teks"])
        print()
        print(h["teks_grup"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
