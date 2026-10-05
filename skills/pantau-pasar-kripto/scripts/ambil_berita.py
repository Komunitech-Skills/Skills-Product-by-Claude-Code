#!/usr/bin/env python3
"""Ambil + rapikan berita kripto dari RSS publik dalam SATU perintah (v1.0.10).

Tanpa API key, Python standar saja (urllib + xml.etree), lintas OS. Mengganti puluhan
pengambilan web manual: script mengambil beberapa RSS media kripto sekaligus (paralel),
menyaring per koin & rentang hari, membuang judul ganda, tautan redirect/beranda, dan judul
berisi prediksi/analisis/target harga, lalu mencetak daftar FINAL siap tempel (URL artikel
asli, tanpa parameter utm).

Pakai:
  python3 ambil_berita.py ETH SOL                 # 7 hari terakhir, maks 4 butir per koin
  python3 ambil_berita.py BTC --hari 1 --maks 5   # ringkasan pagi
  python3 ambil_berita.py "PI:pi network" --hari 14   # KODE:kata kunci tambahan (koma)
  (Windows: python atau py)
Uji tanpa jaringan: --rss-file <file.xml> (boleh berulang) + --sekarang 2026-10-05T12:00:00+07:00

Kode keluar: 0 = ok (termasuk "tidak ada berita" yang dinyatakan jujur), 3 = SEMUA sumber
gagal diambil (jaringan mati/diblokir) -- jangan menulis berita dari ingatan, 1 = error input.
"""

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

try:
    from rapikan_berita import url_sah
except ImportError:  # dipanggil dari folder lain tanpa sys.path skrip
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from rapikan_berita import url_sah

WIB = timezone(timedelta(hours=7))
UA = "komunitech-pantau-pasar-kripto/1.0 (+RSS reader)"

# Sumber umum (disaring per kata kunci koin) -- RSS publik, tanpa kunci.
SUMBER_UMUM = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "The Block": "https://www.theblock.co/rss.xml",
    "Decrypt": "https://decrypt.co/feed",
}
# Sumber per koin: RSS tag Cointelegraph (slug = nama koin).
CT_TAG = "https://cointelegraph.com/rss/tag/{slug}"

ALIAS = {
    "BTC": ["bitcoin"], "ETH": ["ethereum", "ether"], "SOL": ["solana"],
    "XRP": ["xrp", "ripple"], "BNB": ["bnb", "bnb chain"], "DOGE": ["dogecoin"],
    "ADA": ["cardano"], "TON": ["toncoin", "telegram open network"], "PI": ["pi network"],
    "USDT": ["tether"], "USDC": ["usdc"], "TRX": ["tron"], "AVAX": ["avalanche"],
    "DOT": ["polkadot"], "LINK": ["chainlink"], "SUI": ["sui"], "POL": ["polygon"],
    "MATIC": ["polygon"], "LTC": ["litecoin"], "SHIB": ["shiba inu"], "NEAR": ["near protocol"],
}

# Judul yang memuat prediksi/target/analisis harga = proyeksi -> TIDAK ditampilkan.
POLA_PROYEKSI = re.compile(
    r"price (prediction|analysis|forecast|outlook)|predict(ion|ions|s|ed)?\b(?! market)|forecast|"
    r"price target|targets? \$|could (hit|reach|rally|drop|fall|surge|soar|climb|crash|flip|top)|"
    r"(will|to) (hit|reach|surpass|overtake|flip|top) |flippening|\bflip(s|ping)? (eth|btc|bitcoin|ethereum|solana)|"
    r"\beyes \$|next \$|support (level|zone|at)|key support|resistance|bullish|bearish|breakout|"
    r"sell signal|buy signal|should you (buy|sell)",
    re.IGNORECASE,
)


def bersihkan_url(url):
    u = urlparse(url.strip())
    q = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True)
         if not k.lower().startswith("utm_")]
    return urlunparse(u._replace(query=urlencode(q), fragment=""))


def parse_tanggal(teks):
    if not teks:
        return None
    teks = teks.strip()
    try:
        d = parsedate_to_datetime(teks)
    except (TypeError, ValueError, IndexError):
        d = None
    if d is None:
        try:
            d = datetime.fromisoformat(teks.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d


def _teks(el, *nama):
    for n in nama:
        x = el.find(n)
        if x is not None:
            if x.text and x.text.strip():
                return x.text.strip()
            if x.get("href"):
                return x.get("href").strip()
    return ""


def parse_rss(xml_bytes, media):
    """RSS 2.0 atau Atom -> daftar dict {judul,url,media,waktu,kategori}. Rusak -> ValueError."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        raise ValueError(f"RSS rusak: {e}")
    atom = "{http://www.w3.org/2005/Atom}"
    items = root.findall(".//item") or root.findall(f".//{atom}entry")
    hasil = []
    for it in items:
        judul = _teks(it, "title", f"{atom}title")
        url = _teks(it, "link", f"{atom}link")
        waktu = parse_tanggal(_teks(it, "pubDate", f"{atom}published", f"{atom}updated",
                                    "{http://purl.org/dc/elements/1.1/}date"))
        kategori = [c.text.strip() for c in it.findall("category") if c.text]
        kategori += [c.get("term", "") for c in it.findall(f"{atom}category")]
        if judul:
            hasil.append({"judul": " ".join(judul.split()), "url": url, "media": media,
                          "waktu": waktu, "kategori": kategori})
    return hasil


def ambil(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def nama_media(url):
    host = urlparse(url).netloc.lower()
    for kunci, nama in (("cointelegraph", "Cointelegraph"), ("coindesk", "CoinDesk"),
                        ("theblock", "The Block"), ("decrypt", "Decrypt")):
        if kunci in host:
            return nama
    return host.replace("www.", "") or "RSS"


def baca_koin(teks):
    kode, _, tambahan = teks.partition(":")
    kode = kode.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{1,12}", kode):
        raise ValueError(f"Kode koin '{teks}' tidak dikenali -- tulis seperti ETH atau \"PI:pi network\".")
    kata = list(ALIAS.get(kode, []))
    kata += [k.strip().lower() for k in tambahan.split(",") if k.strip()]
    slug = (kata[0] if kata else kode.lower()).replace(" ", "-")
    return {"kode": kode, "kata": kata, "slug": slug}


def cocok(item, koin):
    teks = item["judul"] + " | " + " ".join(item.get("kategori") or [])
    if re.search(r"\b" + re.escape(koin["kode"]) + r"\b", teks):  # kode huruf besar, persis
        return True
    return any(re.search(r"\b" + re.escape(k) + r"\b", teks, re.IGNORECASE) for k in koin["kata"])


def mirip(a, b, ambang=0.6):
    """Judul hampir sama (berita yang sama dari media berbeda): >= 60% kata penting judul terpendek."""
    if not a or not b:
        return False
    return len(a & b) / min(len(a), len(b)) >= ambang


def kumpulkan(daftar_koin, hasil_sumber, sekarang, hari, maks):
    """hasil_sumber: list (nama_sumber, koin_kode_atau_None, items). Fungsi murni (teruji offline)."""
    batas = sekarang - timedelta(days=hari)
    per_koin = {k["kode"]: [] for k in daftar_koin}
    dilihat_url, dilihat_judul, dilihat_kata = set(), set(), []
    dibuang = {"proyeksi": 0, "tautan_tidak_sah": 0, "di_luar_rentang": 0}
    calon = []
    for _nama, kode_tag, items in hasil_sumber:
        for it in items:
            calon.append((kode_tag, it))
    calon.sort(key=lambda x: x[1]["waktu"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    for kode_tag, it in calon:
        if not it["waktu"] or it["waktu"] < batas or it["waktu"] > sekarang + timedelta(hours=1):
            dibuang["di_luar_rentang"] += 1
            continue
        ok, _ = url_sah(it["url"])
        if not ok:
            dibuang["tautan_tidak_sah"] += 1
            continue
        url = bersihkan_url(it["url"])
        kunci_judul = re.sub(r"\W+", " ", it["judul"].lower()).strip()
        kata_judul = {w for w in kunci_judul.split() if len(w) > 3}
        if url in dilihat_url or kunci_judul in dilihat_judul or any(
                mirip(kata_judul, lain) for lain in dilihat_kata):
            continue
        target = None
        for k in daftar_koin:
            if (kode_tag == k["kode"]) or cocok(it, k):
                target = k["kode"]
                break
        if target is None:
            continue
        dilihat_url.add(url)
        dilihat_judul.add(kunci_judul)
        dilihat_kata.append(kata_judul)
        if POLA_PROYEKSI.search(it["judul"]):
            dibuang["proyeksi"] += 1
            continue
        if len(per_koin[target]) < maks:
            per_koin[target].append({
                "judul": it["judul"], "url": url, "media": it["media"],
                "tanggal": it["waktu"].astimezone(WIB).strftime("%d-%m-%Y"),
            })
    return per_koin, dibuang


def ke_teks(per_koin, dibuang, gagal, hari, sekarang, jumlah_sumber_ok):
    baris = [f"Berita {hari} hari terakhir (RSS publik, diambil {sekarang.astimezone(WIB):%d-%m-%Y %H:%M} WIB). "
             "Judul asli media; ringkas ke Bahasa Indonesia TANPA menambah angka/prediksi."]
    for kode, daftar in per_koin.items():
        baris.append(f"\n{kode}:")
        if not daftar:
            baris.append(f"- Tidak ada berita {kode} di sumber RSS dalam {hari} hari terakhir.")
        for i, b in enumerate(daftar, 1):
            baris.append(f"{i}. {b['judul']} ({b['media']}, {b['tanggal']})\n   {b['url']}")
    if dibuang["proyeksi"]:
        baris.append(f"\n({dibuang['proyeksi']} judul berisi prediksi/analisis/target harga tidak ditampilkan.)")
    if gagal:
        baris.append("Sumber gagal diambil: " + "; ".join(gagal) + f" ({jumlah_sumber_ok} sumber lain berhasil).")
    return "\n".join(baris)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ambil + rapikan berita kripto dari RSS publik (satu perintah).")
    ap.add_argument("koin", nargs="+", help="Kode koin, mis. ETH SOL, atau \"PI:pi network\" (kata kunci tambahan).")
    ap.add_argument("--hari", type=int, default=7, help="Rentang hari ke belakang. Default 7 (ringkasan pagi: 1).")
    ap.add_argument("--maks", type=int, default=4, help="Maks butir per koin. Default 4.")
    ap.add_argument("--timeout", type=float, default=8.0)
    ap.add_argument("--keluaran", choices=["teks", "json"], default="teks")
    ap.add_argument("--rss-file", action="append", default=None,
                    help="Mode uji offline: file RSS/Atom lokal, opsional KODE=file untuk feed tag koin (boleh berulang).")
    ap.add_argument("--sekarang", default=None, help="Waktu acuan ISO (uji), default jam sekarang.")
    args = ap.parse_args(argv)
    try:
        daftar_koin = [baca_koin(k) for k in args.koin]
        if args.hari < 1 or args.maks < 1:
            raise ValueError("--hari dan --maks minimal 1.")
        sekarang = parse_tanggal(args.sekarang) if args.sekarang else datetime.now(timezone.utc)
        if sekarang is None:
            raise ValueError("--sekarang tidak dikenali (pakai format ISO, mis. 2026-10-05T12:00:00+07:00).")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    hasil_sumber, gagal = [], []
    if args.rss_file:
        for isian in args.rss_file:
            kode, sep, path = isian.partition("=")
            if not sep or not re.fullmatch(r"[A-Za-z0-9]{1,12}", kode):
                kode, path = None, isian
            try:
                with open(path, "rb") as f:
                    data = f.read()
                hasil_sumber.append((path, kode.upper() if kode else None, parse_rss(data, _media_dari_file(data))))
            except (OSError, ValueError) as e:
                gagal.append(f"{path}: {e}")
    else:
        tugas = [(nama, None, url) for nama, url in SUMBER_UMUM.items()]
        tugas += [(f"Cointelegraph/{k['slug']}", k["kode"], CT_TAG.format(slug=k["slug"])) for k in daftar_koin]

        def kerja(t):
            nama, kode, url = t
            try:
                return (nama, kode, parse_rss(ambil(url, args.timeout), nama.split("/")[0])), None
            except Exception as e:  # noqa: BLE001 -- sumber apa pun gagal = dicatat, tidak crash
                alasan = getattr(e, "reason", None) or getattr(e, "code", None) or e
                return None, f"{nama} ({alasan})"

        with ThreadPoolExecutor(max_workers=6) as ex:
            for hasil, err in ex.map(kerja, tugas):
                if hasil:
                    hasil_sumber.append(hasil)
                if err:
                    gagal.append(err)

    if not hasil_sumber:
        pesan = ("Berita tidak bisa diambil saat ini -- semua sumber RSS gagal (" + "; ".join(gagal) +
                 "). Jangan menulis berita dari ingatan; sampaikan ini apa adanya, harga & ambang tetap jalan.")
        if args.keluaran == "json":
            print(json.dumps({"status": "gagal", "pesan": pesan, "sumber_gagal": gagal}, ensure_ascii=False, indent=2))
        else:
            print(pesan)
        return 3

    per_koin, dibuang = kumpulkan(daftar_koin, hasil_sumber, sekarang, args.hari, args.maks)
    if args.keluaran == "json":
        print(json.dumps({"status": "ok", "hari": args.hari, "berita": per_koin, "dibuang": dibuang,
                          "sumber_gagal": gagal}, ensure_ascii=False, indent=2))
    else:
        print(ke_teks(per_koin, dibuang, gagal, args.hari, sekarang, len(hasil_sumber)))
    return 0


def _media_dari_file(data):
    m = re.search(rb"<link>\s*https?://([^<\s/]+)", data)
    return nama_media("https://" + m.group(1).decode("ascii", "ignore")) if m else "RSS"


if __name__ == "__main__":
    sys.exit(main())
