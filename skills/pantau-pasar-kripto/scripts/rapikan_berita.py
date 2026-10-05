#!/usr/bin/env python3
"""Rapikan daftar berita untuk ringkasan kripto: hanya butir ber-URL artikel asli (v1.0.8).

Input: file JSON (atau stdin dengan `-`) berisi daftar objek
  [{"judul": "...", "url": "https://media.com/artikel", "media": "CoinDesk", "tanggal": "2 Okt 2026"}, ...]
Aturan:
- URL sah = http(s) dengan path artikel (bukan beranda) dan BUKAN redirect agregator
  (news.google.com, t.co, bit.ly, dst.).
- Butir tanpa URL sah: dibuang (default), atau dengan `--tandai` ditaruh di AKHIR dengan
  label "[tanpa tautan]".
- Judul duplikat dibuang. Maks `--maks` butir ber-URL (default 5).
Keluaran: teks siap tempel (default) atau JSON (`--keluaran json`). Python standar saja.

Pakai: python3 rapikan_berita.py berita.json [--tandai] [--maks 5]
"""

import argparse
import json
import sys
from urllib.parse import urlparse

AGREGATOR = ("news.google.com", "t.co", "bit.ly", "tinyurl.com", "lnkd.in", "flip.it", "ow.ly")


def url_sah(url):
    if not isinstance(url, str) or not url.strip():
        return False, "tanpa URL"
    u = urlparse(url.strip())
    if u.scheme not in ("http", "https") or not u.netloc:
        return False, "URL tidak valid"
    host = u.netloc.lower().split(":")[0]
    if any(host == a or host.endswith("." + a) for a in AGREGATOR):
        return False, "redirect agregator, bukan URL artikel asli"
    if u.path in ("", "/") and not u.query:
        return False, "hanya beranda situs"
    return True, ""


def rapikan(daftar, maks=5, tandai=False):
    if not isinstance(daftar, list):
        raise ValueError("Input harus daftar (list) berita.")
    sah, tanpa, dilihat = [], [], set()
    for b in daftar:
        if not isinstance(b, dict):
            continue
        judul = str(b.get("judul") or "").strip()
        if not judul or judul.lower() in dilihat:
            continue
        dilihat.add(judul.lower())
        ok, alasan = url_sah(b.get("url"))
        item = {"judul": judul, "url": (b.get("url") or "").strip() if ok else None,
                "media": str(b.get("media") or "").strip(), "tanggal": str(b.get("tanggal") or "").strip(),
                "alasan": alasan}
        (sah if ok else tanpa).append(item)
    return sah[:maks], (tanpa if tandai else []), len(tanpa)


def ke_teks(sah, tanpa, jumlah_dibuang):
    baris = []
    for i, b in enumerate(sah, 1):
        info = ", ".join(x for x in (b["media"], b["tanggal"]) if x)
        baris.append(f"{i}. {b['judul']}" + (f" ({info})" if info else "") + f"\n   {b['url']}")
    for b in tanpa:
        info = ", ".join(x for x in (b["media"], b["tanggal"]) if x)
        baris.append(f"- [tanpa tautan] {b['judul']}" + (f" ({info})" if info else "")
                     + " -- tautan asli belum didapat")
    if not sah and not tanpa:
        baris.append("Tidak ada berita ber-tautan sumber yang bisa ditampilkan.")
    if jumlah_dibuang and not tanpa:
        baris.append(f"({jumlah_dibuang} berita tanpa tautan asli tidak ditampilkan.)")
    return "\n".join(baris)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rapikan daftar berita: hanya URL artikel asli.")
    ap.add_argument("berkas", help="File JSON daftar berita, atau '-' untuk stdin.")
    ap.add_argument("--tandai", action="store_true", help="Taruh butir tanpa URL di akhir dengan label [tanpa tautan].")
    ap.add_argument("--maks", type=int, default=5)
    ap.add_argument("--keluaran", choices=["teks", "json"], default="teks")
    args = ap.parse_args(argv)
    try:
        if args.berkas == "-":
            data = json.load(sys.stdin)
        else:
            with open(args.berkas, encoding="utf-8") as f:
                data = json.load(f)
        sah, tanpa, n = rapikan(data, args.maks, args.tandai)
    except (OSError, ValueError) as e:  # JSONDecodeError turunan ValueError
        print(f"Error: {e}", file=sys.stderr)
        return 1
    if args.keluaran == "json":
        print(json.dumps({"berita": sah, "tanpa_tautan": tanpa, "jumlah_tanpa_tautan": n},
                         ensure_ascii=False, indent=2))
    else:
        print(ke_teks(sah, tanpa, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
