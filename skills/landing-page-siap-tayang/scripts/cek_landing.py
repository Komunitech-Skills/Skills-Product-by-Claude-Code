#!/usr/bin/env python3
"""Periksa file index.html landing page sebelum tayang.

Pemakaian:  python3 scripts/cek_landing.py index.html [--putih domain1,domain2]
(Windows: python atau py). Python standar saja. Hanya membaca file, tanpa jaringan.
Kode keluar: 0 = semua LOLOS, 1 = ada PERLU PERBAIKAN, 2 = file tidak bisa dibaca.
"""
import os
import re
import sys
from html.parser import HTMLParser

BATAS_UKURAN = 300 * 1024
POLA_WA = re.compile(r"^https://wa\.me/(62\d{8,13})(\?text=[^\s]+)?$")
KATA_PELACAK = ("googletagmanager", "google-analytics", "gtag(", "fbq(", "connect.facebook.net",
                "hotjar", "clarity.ms", "analytics.js", "tiktok.com/i18n/pixel", "mixpanel", "segment.com")


class Pengurai(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._di_title = False
        self.meta = {}
        self.viewport = False
        self.tautan = []          # (href, kelas, teks)
        self.script_src = []
        self.link_luar = []
        self.img_luar = []
        self.img_tanpa_alt = 0
        self.h1 = 0
        self.iframe = 0
        self.lang = ""
        self.inline_script = []
        self._di_script = False
        self._a = None

    def handle_starttag(self, tag, attrs):
        a = dict((k, v or "") for k, v in attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._di_title = True
        elif tag == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if n == "viewport" and "width=device-width" in a.get("content", ""):
                self.viewport = True
            if n:
                self.meta[n] = a.get("content", "")
        elif tag == "a":
            self._a = [a.get("href", ""), a.get("class", ""), ""]
        elif tag == "script":
            if a.get("src"):
                self.script_src.append(a["src"])
            else:
                self._di_script = True
        elif tag == "link":
            h = a.get("href", "")
            if re.match(r"^(https?:)?//", h):
                self.link_luar.append(h)
        elif tag == "img":
            s = a.get("src", "")
            if re.match(r"^(https?:)?//", s):
                self.img_luar.append(s)
            if "alt" not in a:
                self.img_tanpa_alt += 1
        elif tag == "h1":
            self.h1 += 1
        elif tag == "iframe":
            self.iframe += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._di_title = False
        elif tag == "script":
            self._di_script = False
        elif tag == "a" and self._a:
            self.tautan.append(tuple(self._a))
            self._a = None

    def handle_data(self, d):
        if self._di_title:
            self.title += d
        if self._di_script:
            self.inline_script.append(d)
        if self._a is not None:
            self._a[2] += d


def host(url):
    m = re.match(r"^(?:https?:)?//([^/:?#]+)", url)
    return m.group(1).lower() if m else ""


def periksa(teks, ukuran, putih=()):
    """Kembalikan daftar (lolos: bool, pesan: str)."""
    p = Pengurai()
    try:
        p.feed(teks)
        p.close()
    except Exception as e:  # HTML rusak berat
        return [(False, "HTML tidak bisa dibaca dengan baik: %s" % e)]
    h = []
    ok = lambda c, y, n: h.append((bool(c), y if c else n))

    ok(p.title.strip() and "[isian" not in p.title, "Judul halaman (title) ada",
       "Judul halaman (title) kosong atau masih berisi [isian]")
    d = p.meta.get("description", "").strip()
    ok(d, "Meta description ada (%d karakter)" % len(d), "Meta description kosong/tidak ada")
    if d and len(d) > 160:
        h.append((False, "Meta description terlalu panjang (%d karakter, sebaiknya maks. 155)" % len(d)))
    ok(p.viewport, "Viewport HP ada", "Tag viewport HP tidak ada (tampilan di HP akan kecil)")
    ok(p.lang, "Atribut bahasa (lang) ada", "Atribut lang di tag html tidak ada")
    ok(p.h1 == 1, "Satu judul utama (h1)", "Jumlah h1 harus tepat 1 (ditemukan %d)" % p.h1)

    wa = [t for t in p.tautan if "wa.me" in t[0]]
    ok(wa, "Ada tautan WhatsApp (%d)" % len(wa), "Tidak ada tautan wa.me")
    salah = [t[0] for t in wa if not POLA_WA.match(t[0].strip())]
    if wa:
        ok(not salah, "Semua tautan wa.me berformat benar (62..., tanpa +/0/spasi)",
           "Tautan wa.me salah format: %s" % "; ".join(s[:70] for s in salah[:3]))
    cta = [t for t in wa if re.search(r"tombol|btn|cta|button", t[1], re.I)]
    ok(cta, "Ada tombol ajakan (CTA) WhatsApp", "Tidak ada tombol CTA bergaya tombol yang menuju wa.me")
    ok(any("melayang" in t[1].lower() or "float" in t[1].lower() or "fixed" in t[1].lower() for t in wa)
       or re.search(r"position\s*:\s*fixed", teks),
       "Tombol WhatsApp melayang ada", "Tombol WhatsApp melayang di HP tidak ada")

    klaim = re.findall(r"(★{3,}|⭐{3,}|terbaik di indonesia|nomor ?1|no\. ?1|dijamin|pasti untung|100% ?aman|paling murah)", teks, re.I)
    ok(not klaim, "Tidak ada klaim berlebihan/bintang (terbaik, dijamin, ★★★)",
       "Ada %d klaim/bintang yang perlu dibuktikan atau dihapus: %s" % (len(klaim), ", ".join(sorted(set(k.lower() for k in klaim))[:5])))
    sisa = len(re.findall(r"\[isian", teks, re.I))
    ok(sisa == 0, "Tidak ada teks [isian...] tersisa",
       "Masih ada %d teks [isian...] yang belum diganti" % sisa)

    putih = tuple(x.strip().lower() for x in putih if x.strip())
    luar = [u for u in p.script_src + p.link_luar + p.img_luar + ([] if not p.iframe else ["(iframe)"])
            if u == "(iframe)" or host(u) not in putih]
    ok(not luar, "Tidak ada script/gaya/gambar dari pihak luar",
       "Ada sumber luar (pelacak/CDN): %s" % "; ".join(x[:60] for x in luar[:4]))
    kode = (" ".join(p.inline_script) + " " + " ".join(p.script_src)).lower()
    ketemu = [k for k in KATA_PELACAK if k in kode]
    ok(not ketemu, "Tidak ada kode pelacak/analitik",
       "Terdeteksi kode pelacak: %s (pasang hanya bila diminta dan beri pemberitahuan cookie)" % ", ".join(ketemu))
    ok(p.img_tanpa_alt == 0, "Semua gambar punya teks alt", "%d gambar tanpa teks alt" % p.img_tanpa_alt)
    ok(ukuran <= BATAS_UKURAN, "Ukuran file %.0f KB (maks. 300 KB)" % (ukuran / 1024),
       "Ukuran file %.0f KB melebihi 300 KB (kecilkan foto)" % (ukuran / 1024))
    return h


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    putih = []
    if "--putih" in argv:
        i = argv.index("--putih")
        putih = argv[i + 1].split(",") if i + 1 < len(argv) else []
        del argv[i:i + 2]
    if len(argv) != 1:
        print("Pemakaian: python3 scripts/cek_landing.py index.html [--putih domain1,domain2]")
        return 2
    try:
        mentah = open(argv[0], "rb").read()
    except OSError as e:
        print("Tidak bisa membuka file: %s" % e)
        return 2
    if not mentah.strip():
        print("PERLU PERBAIKAN: file kosong")
        return 1
    teks = mentah.decode("utf-8", errors="replace")
    hasil = periksa(teks, len(mentah), putih)
    for lolos, pesan in hasil:
        print(("LOLOS: " if lolos else "PERLU PERBAIKAN: ") + pesan)
    gagal = sum(1 for l, _ in hasil if not l)
    print("\nRingkasan: %d lolos, %d perlu perbaikan" % (len(hasil) - gagal, gagal))
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
