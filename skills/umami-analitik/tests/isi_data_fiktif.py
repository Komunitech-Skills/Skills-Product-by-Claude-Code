#!/usr/bin/env python3
"""Isi Umami ASLI (uji pembuat) dengan kunjungan FIKTIF lewat endpoint publik /api/send, lalu hitung
angka yang DIHARAPKAN secara independen dari daftar kunjungan yang sama (bukan dari keluaran skill).

Hanya untuk pengembang Komunitech (folder tests/ tidak ikut paket pembeli).
Semua pengunjung fiktif: IP dari blok dokumentasi 203.0.113.0/24 (RFC 5737), kota dikirim lewat header
cf-ipcountry/cf-ipcity (cara Umami membaca lokasi di belakang Cloudflare).

  python3 tests/isi_data_fiktif.py kirim --url http://127.0.0.1:3000 --website <uuid>
  python3 tests/isi_data_fiktif.py harapan --dari 2026-09-21 --sampai 2026-09-27
"""
import argparse
import datetime as dt
import json
import sys
import urllib.request

WIB = dt.timezone(dt.timedelta(hours=7))
HOST = "keripikbusri.contoh.id"
UA = {
    "android": "Mozilla/5.0 (Linux; Android 14; SM-A155F) AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/139.0.0.0 Mobile Safari/537.36",
    "iphone": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
              "Version/18.5 Mobile/15E148 Safari/604.1",
    "windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/139.0.0.0 Safari/537.36",
    "tablet": "Mozilla/5.0 (Linux; Android 13; SM-X200) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/139.0.0.0 Safari/537.36",
}
SCREEN = {"android": "412x915", "iphone": "390x844", "windows": "2560x1440", "tablet": "800x1340"}

# pengunjung: kode -> (jenis perangkat, ip, negara, kota, kode wilayah)
PENGUNJUNG = {
    "A": ("android", "203.0.113.11", "ID", "Jakarta", "JK"),
    "B": ("android", "203.0.113.12", "ID", "Surabaya", "JI"),
    "C": ("iphone", "203.0.113.13", "ID", "Jakarta", "JK"),
    "D": ("android", "203.0.113.14", "ID", "Bandung", "JB"),
    "E": ("windows", "203.0.113.15", "ID", "Semarang", "JT"),
    "F": ("android", "203.0.113.16", "ID", "Medan", "SU"),
    "G": ("iphone", "203.0.113.17", "MY", "Kuala Lumpur", "14"),
    "H": ("android", "203.0.113.18", "ID", "Makassar", "SN"),
    "I": ("tablet", "203.0.113.19", "ID", "Yogyakarta", "YO"),
    "J": ("android", "203.0.113.20", "ID", "Jakarta", "JK"),
    "K": ("windows", "203.0.113.21", "ID", "Bandung", "JB"),
    "L": ("android", "203.0.113.22", "ID", "Surabaya", "JI"),
    "M": ("iphone", "203.0.113.23", "ID", "Denpasar", "BA"),
    "N": ("android", "203.0.113.24", "ID", "Jakarta", "JK"),
    "O": ("android", "203.0.113.25", "ID", "Palembang", "SS"),
    "P": ("windows", "203.0.113.26", "ID", "Jakarta", "JK"),
}

IG = "?utm_source=instagram&utm_medium=social&utm_campaign=promo-gajian-sep"
TT = "?utm_source=tiktok&utm_medium=video&utm_campaign=promo-gajian-sep"
WA = "?utm_source=whatsapp&utm_medium=status&utm_campaign=promo-gajian-sep"
WA2 = "?utm_source=whatsapp&utm_medium=grup&utm_campaign=reseller-okt"
R_IG, R_TT, R_GOOGLE, R_FB = ("https://l.instagram.com/", "https://www.tiktok.com/", "https://www.google.com/",
                              "https://l.facebook.com/")
BALADO, ORI, CARA, TK = "/produk/keripik-balado", "/produk/keripik-original", "/cara-pesan", "/terima-kasih"
JUDUL = {"/": "Keripik Bu Sri - Renyah Asli Lampung", BALADO: "Keripik Balado 250 g", ORI: "Keripik Original 250 g",
         CARA: "Cara Pesan", TK: "Terima Kasih"}

# kunjungan: (pengunjung, tanggal, jam WIB, query di halaman pertama, referrer, langkah)
# langkah: ("p", path, detik_setelah_mulai) atau ("e", nama_event, detik, data)
KUNJUNGAN = [
    # ---- minggu 14-20 Sep 2026 (pembanding "minggu lalu" untuk laporan minggu 21-27)
    ("A", "2026-09-15", "20:05", "", R_GOOGLE, [("p", "/", 0), ("p", BALADO, 40)]),
    ("B", "2026-09-16", "12:10", "", None, [("p", "/", 0)]),
    ("C", "2026-09-18", "19:30", IG, R_IG, [("p", "/", 0), ("p", ORI, 30), ("e", "klik-wa", 70, {"tombol": "pesan-original"})]),
    ("D", "2026-09-19", "09:15", "", None, [("p", "/", 0)]),
    # ---- minggu 21-27 Sep 2026 (minggu lalu relatif 29 Sep)
    ("A", "2026-09-21", "19:02", IG, R_IG, [("p", "/", 0), ("p", BALADO, 45), ("e", "klik-wa", 90, {"tombol": "pesan-balado"})]),
    ("E", "2026-09-21", "10:20", "", R_GOOGLE, [("p", "/", 0), ("p", CARA, 60), ("p", ORI, 150)]),
    ("F", "2026-09-22", "20:15", TT, R_TT, [("p", "/", 0)]),
    ("G", "2026-09-22", "21:40", IG, R_IG, [("p", "/", 0), ("p", BALADO, 25)]),
    ("H", "2026-09-23", "12:05", WA, None, [("p", "/", 0), ("p", BALADO, 35), ("e", "klik-wa", 80, {"tombol": "pesan-balado"})]),
    ("I", "2026-09-24", "16:30", "", R_FB, [("p", "/", 0)]),
    ("J", "2026-09-25", "19:45", WA, None, [("p", BALADO, 0), ("e", "beli", 50, {"produk": "Keripik Balado 250 g", "nilai": 25000}), ("p", TK, 55)]),
    ("K", "2026-09-26", "08:10", "", None, [("p", "/", 0), ("p", CARA, 90)]),
    ("B", "2026-09-26", "13:00", TT, R_TT, [("p", "/", 0), ("e", "klik-wa", 20, {"tombol": "hero"})]),
    ("L", "2026-09-27", "18:20", IG, R_IG, [("p", "/", 0)]),
    ("A", "2026-09-27", "20:10", "", None, [("p", "/", 0), ("p", ORI, 40), ("e", "beli", 100, {"produk": "Keripik Original 250 g", "nilai": 22000}), ("p", TK, 105)]),
    ("M", "2026-09-27", "21:05", "", R_GOOGLE, [("p", "/", 0), ("p", BALADO, 30), ("p", CARA, 75)]),
    # ---- minggu ini 28-29 Sep 2026 (sampai 29 Sep 14.00 WIB)
    ("N", "2026-09-28", "07:30", WA, None, [("p", "/", 0), ("p", BALADO, 20), ("e", "klik-wa", 50, {"tombol": "pesan-balado"})]),
    ("O", "2026-09-28", "12:15", TT, R_TT, [("p", "/", 0)]),
    ("F", "2026-09-28", "19:40", TT, R_TT, [("p", "/", 0), ("p", BALADO, 35), ("e", "beli", 95, {"produk": "Keripik Balado 250 g", "nilai": 50000}), ("p", TK, 100)]),
    ("P", "2026-09-28", "21:00", WA2, None, [("p", "/", 0), ("p", CARA, 120)]),
    ("C", "2026-09-29", "09:05", IG, R_IG, [("p", "/", 0), ("e", "klik-wa", 15, {"tombol": "hero"})]),
    ("D", "2026-09-29", "11:20", "", R_GOOGLE, [("p", "/", 0)]),
    ("J", "2026-09-29", "13:10", WA2, None, [("p", "/", 0), ("p", ORI, 30), ("p", BALADO, 70)]),
]


def langkah_rata():
    """Semua hit (pageview/event) sebagai dict berurutan waktu."""
    hasil = []
    for kode, tgl, jam, query, ref, langkah in KUNJUNGAN:
        mulai = dt.datetime.fromisoformat(f"{tgl}T{jam}:00").replace(tzinfo=WIB)
        halaman_sebelum = None
        for i, s in enumerate(langkah):
            ts = mulai + dt.timedelta(seconds=s[2])
            if s[0] == "p":
                path = s[1]
                url = f"https://{HOST}{path}" + (query if i == 0 else "")
                referrer = ref if i == 0 else (f"https://{HOST}{halaman_sebelum}" if halaman_sebelum else None)
                hasil.append({"kode": kode, "ts": ts, "jenis": "p", "path": path, "url": url, "ref": referrer,
                              "query": query if i == 0 else ""})
                halaman_sebelum = path
            else:
                path = halaman_sebelum or "/"
                hasil.append({"kode": kode, "ts": ts, "jenis": "e", "nama": s[1], "data": s[3], "path": path,
                              "url": f"https://{HOST}{path}", "ref": None, "query": ""})
    return sorted(hasil, key=lambda h: h["ts"])


def kirim(args):
    n = 0
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    for h in langkah_rata():
        jenis, ip, negara, kota, wil = PENGUNJUNG[h["kode"]]
        payload = {"website": args.website, "hostname": HOST, "url": h["url"], "language": "id-ID",
                   "screen": SCREEN[jenis], "timestamp": int(h["ts"].timestamp()),
                   "title": JUDUL.get(h["path"], "")}
        if h["ref"]:
            payload["referrer"] = h["ref"]
        if h["jenis"] == "e":
            payload["name"] = h["nama"]
            payload["data"] = h["data"]
        req = urllib.request.Request(args.url.rstrip("/") + "/api/send", method="POST",
                                     data=json.dumps({"type": "event", "payload": payload}).encode())
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", UA[jenis])
        req.add_header("X-Forwarded-For", ip)
        req.add_header("cf-ipcountry", negara)
        req.add_header("cf-ipcity", kota)
        req.add_header("cf-region-code", wil)
        with opener.open(req, timeout=20) as r:
            jawab = json.loads(r.read() or b"{}")
            if "sessionId" not in jawab:
                sys.exit(f"gagal kirim: {jawab}")
        n += 1
    print(f"{n} hit terkirim ({len(KUNJUNGAN)} kunjungan, {len(PENGUNJUNG)} pengunjung fiktif)")


def harapan(dari, sampai):
    """Angka yang diharapkan untuk rentang tanggal WIB [dari 00:00, sampai 23:59:59] - rumus Umami 3.4.0:
    kunjungan = pengunjung x jam UTC yang sama; bounce = kunjungan dengan 1 pageview tanpa event;
    lama = selisih pageview pertama-terakhir per kunjungan; halaman/referrer/UTM = jumlah PENGUNJUNG unik."""
    a = dt.datetime.fromisoformat(dari + "T00:00:00").replace(tzinfo=WIB)
    b = dt.datetime.fromisoformat(sampai + "T23:59:59.999").replace(tzinfo=WIB)
    hit = [h for h in langkah_rata() if a <= h["ts"] <= b]
    visit = {}
    for h in hit:
        k = (h["kode"], h["ts"].astimezone(dt.timezone.utc).strftime("%Y%m%d%H"))
        v = visit.setdefault(k, {"pv": [], "ev": 0})
        if h["jenis"] == "p":
            v["pv"].append(h["ts"])
        else:
            v["ev"] += 1
    kv = {k: v for k, v in visit.items() if v["pv"]}
    pv = sum(len(v["pv"]) for v in kv.values())
    bounce = sum(1 for v in kv.values() if len(v["pv"]) == 1 and v["ev"] == 0)
    total = sum(int((max(v["pv"]) - min(v["pv"])).total_seconds()) for v in kv.values())
    pengunjung = {k[0] for k in kv}

    def unik(kunci):
        d = {}
        for h in hit:
            if h["jenis"] == "p":
                x = kunci(h)
                if x:
                    d.setdefault(x, set()).add(h["kode"])
        return dict(sorted(((x, len(s)) for x, s in d.items()), key=lambda t: (-t[1], t[0])))

    def utm(nama):
        return unik(lambda h: dict(p.split("=") for p in h["query"][1:].split("&")).get(nama) if h["query"] else None)

    event = {}
    for h in hit:
        if h["jenis"] == "e":
            event[h["nama"]] = event.get(h["nama"], 0) + 1
    ref = unik(lambda h: (h["ref"] or "").split("/")[2].replace("www.", "") if h["ref"] and HOST not in h["ref"] else None)
    return {
        "pengunjung": len(pengunjung), "kunjungan": len(kv), "tayangan": pv, "bounce": bounce,
        "total_detik": total, "halaman": unik(lambda h: h["path"]), "referrer": ref,
        "utm_source": utm("utm_source"), "utm_campaign": utm("utm_campaign"), "event": event,
        "perangkat": _sesi(pengunjung, 0), "kota": _sesi(pengunjung, 3), "negara": _sesi(pengunjung, 2),
    }


def _sesi(kode_set, idx):
    d = {}
    for k in kode_set:
        x = PENGUNJUNG[k][idx]
        d[x] = d.get(x, 0) + 1
    return dict(sorted(d.items(), key=lambda t: (-t[1], t[0])))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("kirim")
    k.add_argument("--url", default="http://127.0.0.1:3000")
    k.add_argument("--website", required=True)
    h = sub.add_parser("harapan")
    h.add_argument("--dari", required=True)
    h.add_argument("--sampai", required=True)
    a = ap.parse_args()
    if a.cmd == "kirim":
        kirim(a)
    else:
        print(json.dumps(harapan(a.dari, a.sampai), indent=1, ensure_ascii=False))
