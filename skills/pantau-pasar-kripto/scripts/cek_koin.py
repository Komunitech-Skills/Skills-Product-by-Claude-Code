#!/usr/bin/env python3
"""Fakta dasar satu koin untuk riset (v1.0.10) -- SATU perintah, angka dihitung, bukan ditebak.

Mengambil (tanpa API key, Python standar): CoinGecko search + data koin (harga IDR/USD, % 24 jam,
kapitalisasi saat ini, pasokan, situs/whitepaper/explorer, daftar bursa dari ticker) dan daftar
pair Indodax (`https://indodax.com/api/pairs`) -- jumlah pair DIHITUNG dari data itu dan dicek
apakah koin tersebut punya pair di Indodax. Setiap fakta disertai URL sumber & jam WIB.
Tidak ada kesimpulan beli/jual; "ada/tidak ada di bursa" BUKAN status legal (cek PAKD/DAKD OJK).

Pakai:
  python3 cek_koin.py PI                 # kode/simbol atau nama ("pi network")
  python3 cek_koin.py --id pi-network    # bila id CoinGecko sudah pasti
  (Windows: python atau py)
Uji tanpa jaringan: --data-file contoh.json berisi {"search":{...},"coin":{...},"indodax_pairs":[...]}
(bagian yang tidak ada di file = dianggap gagal diambil).

Kode keluar: 0 = ok (sebagian bagian boleh gagal, disebut jujur), 3 = semua sumber gagal,
1 = error input / koin tidak ditemukan.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

WIB = timezone(timedelta(hours=7))
UA = "komunitech-pantau-pasar-kripto/1.0"
CG = "https://api.coingecko.com/api/v3"
URL_PAIRS = "https://indodax.com/api/pairs"
# Nama bursa Indonesia (dicocokkan ke nama bursa di ticker CoinGecko, huruf kecil).
BURSA_ID = ("indodax", "tokocrypto", "pintu", "reku", "rekeningku", "triv", "upbit indonesia",
            "mobee", "ajaib", "pluang", "nanovest", "digitalexchange.id", "fasset", "indonesia")


def ambil_json(url, timeout, percobaan=3):
    """GET JSON; HTTP 429 (batas laju CoinGecko) dicoba ulang dengan jeda singkat."""
    for i in range(percobaan):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == percobaan - 1:
                raise
            try:
                jeda = float(e.headers.get("Retry-After") or 0)
            except (TypeError, ValueError):
                jeda = 0
            time.sleep(min(max(jeda, 3.0 * (i + 1)), 15.0))


def rupiah(x):
    if x is None:
        return "tidak tersedia"
    if x >= 1000:
        return "Rp" + f"{round(x):,}".replace(",", ".")
    return "Rp" + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def usd(x):
    if x is None:
        return "tidak tersedia"
    if x >= 1:
        return "US$" + f"{round(x):,}".replace(",", ".")
    return "US$" + f"{x:.4f}".replace(".", ",")


def angka(x):
    return "tidak tersedia" if x is None else f"{round(x):,}".replace(",", ".")


def persen(x):
    return "tidak tersedia" if x is None else f"{x:+.2f}%".replace(".", ",")


def jam_wib(iso):
    if not iso:
        return "jam tidak tersedia"
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return "jam tidak tersedia"
    if d.tzinfo is None:
        return "jam tidak tersedia"
    return d.astimezone(WIB).strftime("%d-%m-%Y %H:%M WIB")


def pilih_kandidat(search, kueri):
    """Fungsi murni: pilih id CoinGecko dari hasil search. Simbol/nama/id persis dulu,
    lalu peringkat kapitalisasi terbaik. Kembalikan (terpilih, lain_bersimbol_sama)."""
    koin = (search or {}).get("coins") or []
    q = kueri.strip().lower()
    persis = [c for c in koin if q in (str(c.get("symbol", "")).lower(), str(c.get("name", "")).lower(),
                                       str(c.get("id", "")).lower())]
    if not persis:
        return None, []
    persis.sort(key=lambda c: (c.get("market_cap_rank") is None, c.get("market_cap_rank") or 0))
    terpilih = persis[0]
    sim = str(terpilih.get("symbol", "")).lower()
    lain = [c["id"] for c in koin if c is not terpilih and str(c.get("symbol", "")).lower() == sim]
    return terpilih, lain


def cek_indodax(pairs, simbol, cg_id):
    """Fungsi murni: hitung jumlah pair & cari pair koin ini (simbol atau coingecko_id persis)."""
    if not isinstance(pairs, list):
        raise ValueError("format daftar pair Indodax tidak dikenali")
    s = simbol.lower()
    cocok = [p.get("id") for p in pairs if isinstance(p, dict) and (
        str(p.get("traded_currency", "")).lower() == s or (cg_id and p.get("coingecko_id") == cg_id))]
    return len(pairs), [c for c in cocok if c]


def susun(kueri, data, sekarang):
    """data: {"search","coin","indodax_pairs"} (None = gagal) + "galat": {bagian: alasan}."""
    galat = data.get("galat", {})
    baris, fakta = [], {}
    coin = data.get("coin")
    lain = data.get("lain_bersimbol_sama") or []
    if coin:
        md = coin.get("market_data") or {}
        cg_id = coin.get("id")
        simbol = str(coin.get("symbol", "")).upper()
        hal = f"https://www.coingecko.com/en/coins/{cg_id}"
        harga_idr = (md.get("current_price") or {}).get("idr")
        harga_usd = (md.get("current_price") or {}).get("usd")
        p24 = (md.get("price_change_percentage_24h_in_currency") or {}).get("idr")
        mcap = (md.get("market_cap") or {}).get("usd")
        fakta.update({"id": cg_id, "simbol": simbol, "harga_idr": harga_idr, "harga_usd": harga_usd,
                      "perubahan_24jam_idr_persen": p24, "kapitalisasi_usd": mcap,
                      "peringkat_kapitalisasi": coin.get("market_cap_rank"),
                      "jam_data": jam_wib(md.get("last_updated"))})
        baris.append(f"Fakta koin: {coin.get('name')} ({simbol}) -- id CoinGecko `{cg_id}`")
        baris.append(f"- Harga: {rupiah(harga_idr)} / {usd(harga_usd)}; 24 jam (dalam Rupiah): {persen(p24)} "
                     f"-- CoinGecko, data {jam_wib(md.get('last_updated'))}. {hal}")
        rank = coin.get("market_cap_rank")
        baris.append(f"- Kapitalisasi pasar saat ini: {usd(mcap)}" + (f" (peringkat #{rank} di CoinGecko)" if rank else "")
                     + f". {hal}")
        baris.append(f"- Pasokan: beredar {angka(md.get('circulating_supply'))}; total {angka(md.get('total_supply'))}; "
                     f"maksimum {angka(md.get('max_supply'))} {simbol}. {hal}")
        links = coin.get("links") or {}
        situs = next((u for u in links.get("homepage") or [] if u), None)
        wp = links.get("whitepaper") or None
        if isinstance(wp, dict):
            wp = wp.get("link")
        explorer = next((u for u in links.get("blockchain_site") or [] if u), None)
        baris.append(f"- Situs resmi: {situs or 'tidak tercatat'} · Whitepaper: {wp or 'tidak tercatat'} · "
                     f"Explorer: {explorer or 'tidak tercatat'} (dari data CoinGecko; buka untuk cek isi & tanggalnya)")
        bursa = sorted({(t.get("market") or {}).get("name") for t in coin.get("tickers") or []} - {None})
        bursa_id = [b for b in bursa if any(k in b.lower() for k in BURSA_ID)]
        fakta.update({"jumlah_bursa_di_ticker": len(bursa), "bursa": bursa, "bursa_indonesia_di_ticker": bursa_id})
        baris.append(f"- Bursa di data ticker CoinGecko (maks. 100 ticker pertama): {len(bursa)} bursa"
                     + (f" ({', '.join(bursa[:12])}{', ...' if len(bursa) > 12 else ''})" if bursa else "")
                     + f"; bursa Indonesia di daftar itu: {', '.join(bursa_id) if bursa_id else 'tidak ada'}. "
                     f"{hal}#markets")
        if lain:
            baris.append(f"- Hati-hati tertukar: koin lain bersimbol sama di CoinGecko: {', '.join(lain[:5])}.")
    else:
        cg_id = None
        simbol = kueri.upper() if kueri.replace("-", "").isalnum() and " " not in kueri else ""
        baris.append(f"Data CoinGecko untuk '{kueri}' tidak bisa diambil ({galat.get('coin') or galat.get('search') or 'gagal'})"
                     " -- harga/kapitalisasi tidak ditulis (tidak dikarang).")
    pairs = data.get("indodax_pairs")
    if pairs is not None:
        try:
            n, cocok = cek_indodax(pairs, simbol or "\0", cg_id)
            fakta.update({"jumlah_pair_indodax": n, "pair_indodax_koin_ini": cocok if simbol else None})
            status = (", ".join(cocok) if cocok else "TIDAK ADA") if simbol else "belum bisa dicek (simbol belum pasti)"
            baris.append(f"- Indodax: {n} pair (dihitung dari {URL_PAIRS}, {sekarang:%d-%m-%Y %H:%M} WIB); "
                         f"pair {simbol or kueri}: {status}"
                         + (f" -- https://indodax.com/market/{cocok[0].upper()}" if cocok else "") + ".")
        except ValueError as e:
            baris.append(f"- Indodax: daftar pair tidak bisa dibaca ({e}) -- jangan sebut jumlah pair.")
    else:
        baris.append(f"- Indodax: daftar pair gagal diambil ({galat.get('indodax', 'gagal')}) -- jangan sebut jumlah pair.")
    baris.append("- Bursa lokal lain (Tokocrypto, Pintu, Reku, dll.): cek di aplikasi/daftar aset resmi bursa itu.")
    baris.append("Catatan: ada/tidak ada di bursa BUKAN status legal. Di Indonesia aset kripto diawasi OJK "
                 "(POJK 27/2024); cek bursa di daftar PAKD berizin OJK dan aset di DAKD bursanya (references/regulasi.md).")
    return "\n".join(baris), fakta


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fakta dasar satu koin (CoinGecko + pair Indodax), satu perintah.")
    ap.add_argument("kueri", nargs="?", help="Simbol atau nama koin, mis. PI atau \"pi network\".")
    ap.add_argument("--id", default=None, help="id CoinGecko bila sudah pasti (lewati pencarian).")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--keluaran", choices=["teks", "json"], default="teks")
    ap.add_argument("--data-file", default=None, help="Mode uji offline: JSON {search, coin, indodax_pairs}.")
    args = ap.parse_args(argv)
    kueri = (args.kueri or args.id or "").strip()
    if not kueri:
        print("Error: sebutkan simbol/nama koin, mis. cek_koin.py PI", file=sys.stderr)
        return 1
    sekarang = datetime.now(WIB)
    galat, data = {}, {}

    if args.data_file:
        try:
            with open(args.data_file, encoding="utf-8") as f:
                uji = json.load(f)
        except (OSError, ValueError) as e:
            print(f"Error: --data-file tidak bisa dibaca: {e}", file=sys.stderr)
            return 1

        def dapat(bagian, _url):
            if uji.get(bagian) is None:
                raise RuntimeError("tidak ada di data uji")
            return uji[bagian]
    else:
        def dapat(_bagian, url):
            return ambil_json(url, args.timeout)

    cg_id = args.id
    if not cg_id:
        try:
            terpilih, lain = pilih_kandidat(dapat("search", f"{CG}/search?query={quote(kueri)}"), kueri)
            if terpilih is None:
                print(f"Koin '{kueri}' tidak ditemukan persis di pencarian CoinGecko -- tanyakan nama lengkap/"
                      "id CoinGecko ke pengguna; jangan menebak.")
                return 1
            cg_id, data["lain_bersimbol_sama"] = terpilih["id"], lain
        except Exception as e:  # noqa: BLE001
            galat["search"] = str(e)
    if cg_id:
        try:
            data["coin"] = dapat("coin", f"{CG}/coins/{quote(cg_id)}?localization=false&tickers=true"
                                         "&market_data=true&community_data=false&developer_data=false&sparkline=false")
        except Exception as e:  # noqa: BLE001
            galat["coin"] = str(e)
    try:
        data["indodax_pairs"] = dapat("indodax_pairs", URL_PAIRS)
    except Exception as e:  # noqa: BLE001
        galat["indodax"] = str(e)
    data["galat"] = galat

    teks, fakta = susun(kueri, data, sekarang)
    semua_gagal = data.get("coin") is None and data.get("indodax_pairs") is None
    if args.keluaran == "json":
        print(json.dumps({"status": "gagal" if semua_gagal else "ok", "fakta": fakta, "galat": galat,
                          "teks": teks}, ensure_ascii=False, indent=2))
    else:
        print(teks)
    return 3 if semua_gagal else 0


if __name__ == "__main__":
    sys.exit(main())
