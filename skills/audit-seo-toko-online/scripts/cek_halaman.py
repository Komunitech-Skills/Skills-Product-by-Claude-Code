#!/usr/bin/env python3
"""Bantuan teknis untuk skill audit-seo-toko-online: baca SATU FILE HTML LOKAL
(hasil simpan/unduh halaman, bukan mengakses internet) dan hitung fakta SEO
dasarnya secara persis — bukan kira-kira.

Hanya memakai pustaka standar Python (3.7+), tanpa akses jaringan sama sekali.
Jalankan dengan `python3` (Windows: `python` atau `py`).

Contoh:
  python3 cek_halaman.py halaman.html
  python3 cek_halaman.py halaman.html --kata-kunci "keripik pedas Bandung"
  python3 cek_halaman.py halaman.html --url "https://tokosaya.com/produk/keripik-pedas"
  python3 cek_halaman.py halaman.html --json > hasil.json

Batas yang dipakai (batas aman umum yang sama dipakai skill copy-landing-page
dan listing-marketplace di library ini, BUKAN patokan resmi Google — Google
memotong tampilan berdasarkan lebar piksel, bukan jumlah karakter, jadi ini
hanya perkiraan):
  - Judul (title)        : idealnya 30-60 karakter
  - Meta description     : idealnya 70-155 karakter

Keterbatasan yang WAJIB disebutkan ke pengguna (jangan menyembunyikan ini):
  - Skrip ini TIDAK mengakses internet. Tautan rusak dicek dari FORMATNYA saja
    (kosong, "#", "javascript:...", ada spasi mentah) — bukan dicek apakah
    halaman tujuannya benar-benar hidup (butuh koneksi internet untuk itu).
  - Kecepatan halaman, Core Web Vitals, dan skor mobile TIDAK dihitung skrip
    ini (butuh membuka halaman sungguhan) — itu sebabnya bagian itu memakai
    ceklis manual di references/kecepatan-mobile.md, bukan angka dari skrip.
  - Banyak plugin SEO (mis. Yoast, AIOSEO, RankMath) menyisipkan JSON-LD lewat
    JavaScript setelah halaman dimuat. Kalau file HTML diambil dengan "Simpan
    Halaman" dari browser (bukan "Lihat Sumber Halaman"), JSON-LD hasil render
    JS biasanya SUDAH ikut tersimpan. Kalau diambil dengan cara lain (mis.
    curl atau download HTML mentah), JSON-LD berbasis JS bisa tidak muncul —
    skrip ini hanya bisa melaporkan apa yang ADA di file, bukan menebak yang
    tidak terlihat.
  - "Paragraf awal" diambil dari elemen <p> PERTAMA yang ditemukan di file,
    apa adanya (tidak mendeteksi mana bagian menu/header). Kalau template
    situs meletakkan <p> di menu/header sebelum konten utama, hasilnya bisa
    tidak mewakili — periksa manual kalau hasilnya terasa aneh.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BATAS_TITLE_MIN = 30
BATAS_TITLE_MAKS = 60
BATAS_DESC_MIN = 70
BATAS_DESC_MAKS = 155

OG_WAJIB = ["og:title", "og:description", "og:image", "og:type"]

POLA_SPASI_MENTAH = re.compile(r"\s")
POLA_CHARSET = re.compile(rb'charset=["\']?\s*([A-Za-z0-9_-]+)', re.IGNORECASE)


class InputSalah(Exception):
    pass


# ---------------------------------------------------------------------------
# Pembacaan file (tahan encoding aneh & file rusak/kosong)
# ---------------------------------------------------------------------------

def baca_html(path):
    """Baca file HTML lokal, coba tebak encoding dari <meta charset>, lalu
    fallback UTF-8 dan terakhir latin-1 (tidak pernah gagal total, supaya
    skrip tetap jalan untuk file berencoding aneh — hanya diberi catatan)."""
    p = Path(path)
    if not p.is_file():
        raise InputSalah(f"file tidak ditemukan: {path}")
    mentah = p.read_bytes()
    if not mentah.strip():
        raise InputSalah("file HTML kosong (0 karakter isi)")

    catatan_encoding = None
    cocok = POLA_CHARSET.search(mentah[:4096])
    urutan_coba = []
    if cocok:
        urutan_coba.append(cocok.group(1).decode("ascii", errors="ignore"))
    urutan_coba += ["utf-8"]

    for enc in urutan_coba:
        try:
            return mentah.decode(enc), len(mentah), None
        except (LookupError, UnicodeDecodeError):
            continue
    # Fallback terakhir: latin-1 tidak pernah gagal, tapi karakter non-Latin
    # (mis. emoji, huruf beraksen) bisa tampil salah — beri tahu pengguna.
    catatan_encoding = (
        "Encoding file tidak terbaca sebagai UTF-8 dan berbeda dari deklarasi "
        "<meta charset>. Ditampilkan pakai fallback latin-1 — beberapa huruf "
        "(aksen, emoji) mungkin tampil salah. Simpan ulang file sebagai UTF-8 "
        "kalau ini terjadi."
    )
    return mentah.decode("latin-1"), len(mentah), catatan_encoding


# ---------------------------------------------------------------------------
# Parser HTML (stdlib, tanpa dependensi luar)
# ---------------------------------------------------------------------------

class EkstrakHalaman(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self.meta_description = None
        self.meta_robots = None
        self.canonical = None
        self.html_lang = None
        self.headings = []  # [(level, teks)]
        self.images = []  # [{"src", "punya_alt", "alt_kosong"}]
        self.links = []  # [{"href", "punya_href"}]
        self.og = {}
        self.jsonld_raw = []
        self.paragraf_awal = None

        self._buffer = []
        self._in_title = False
        self._heading_level = None
        self._in_jsonld = False
        self._in_paragraf_awal = False

    @staticmethod
    def _attr(attrs, nama):
        for k, v in attrs:
            if k and k.lower() == nama:
                return v
        return None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
            self._buffer = []
        elif tag == "meta":
            nama = (self._attr(attrs, "name") or "").lower()
            prop = (self._attr(attrs, "property") or "").lower()
            konten = self._attr(attrs, "content")
            if nama == "description" and konten is not None:
                self.meta_description = konten
            elif nama == "robots" and konten is not None:
                self.meta_robots = konten
            elif prop.startswith("og:") and konten is not None:
                self.og[prop] = konten
        elif tag == "link":
            rel = (self._attr(attrs, "rel") or "").lower()
            href = self._attr(attrs, "href")
            if "canonical" in rel.split() and href:
                self.canonical = href
        elif tag == "html":
            lang = self._attr(attrs, "lang")
            if lang:
                self.html_lang = lang
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading_level = int(tag[1])
            self._buffer = []
        elif tag == "img":
            src = self._attr(attrs, "src") or ""
            punya_alt = any(k and k.lower() == "alt" for k, v in attrs)
            alt_val = self._attr(attrs, "alt")
            alt_kosong = punya_alt and (alt_val is None or not alt_val.strip())
            self.images.append({"src": src, "punya_alt": punya_alt, "alt_kosong": alt_kosong})
        elif tag == "a":
            href = self._attr(attrs, "href")
            self.links.append({"href": href, "punya_href": href is not None})
        elif tag == "script":
            tipe = (self._attr(attrs, "type") or "").lower()
            if tipe == "application/ld+json":
                self._in_jsonld = True
                self._buffer = []
        elif tag == "p" and self.paragraf_awal is None:
            self._in_paragraf_awal = True
            self._buffer = []

    def handle_data(self, data):
        if self._in_title or self._heading_level is not None or self._in_jsonld or self._in_paragraf_awal:
            self._buffer.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title" and self._in_title:
            self.title = "".join(self._buffer).strip()
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._heading_level is not None:
            teks = "".join(self._buffer).strip()
            self.headings.append((self._heading_level, teks))
            self._heading_level = None
        elif tag == "script" and self._in_jsonld:
            self.jsonld_raw.append("".join(self._buffer))
            self._in_jsonld = False
        elif tag == "p" and self._in_paragraf_awal:
            teks = "".join(self._buffer).strip()
            if teks:
                self.paragraf_awal = teks
            self._in_paragraf_awal = False


def ekstrak(html_teks):
    parser = EkstrakHalaman()
    parser.feed(html_teks)
    # WAJIB dipanggil: html.parser (stdlib) menahan data yang belum pasti
    # selesai sampai close() dipanggil (dianggap "mungkin masih ada input
    # susulan"). Tanpa ini, dokumen yang berakhir di tengah tag/elemen raw
    # text (lihat perbaiki_tag_rawtext_tidak_tertutup di bawah) tidak
    # memicu callback SAMA SEKALI untuk sisa dokumen — bukan cuma diam-diam
    # salah, tapi benar-benar tidak diproses.
    parser.close()
    return parser


# Elemen yang oleh html.parser stdlib dianggap "raw text": begitu tag ini
# terbuka, SEMUA isi di dalamnya (termasuk tag HTML lain di dalamnya)
# dianggap teks polos sampai ditemukan tag penutup yang PERSIS cocok.
# (stdlib: HTMLParser.RCDATA_CONTENT_ELEMENTS = ("textarea", "title"),
# HTMLParser.CDATA_CONTENT_ELEMENTS termasuk "script"/"style".)
TAG_RAWTEXT = ("title", "textarea", "script", "style")
_POLA_BUKA_RAWTEXT = re.compile(r"<(%s)\b[^>]*>" % "|".join(TAG_RAWTEXT), re.IGNORECASE)
_POLA_TAG_LAIN = re.compile(r"<[a-zA-Z/]")


def perbaiki_tag_rawtext_tidak_tertutup(html_teks):
    """Deteksi & pulihkan tag <title>/<textarea>/<script>/<style> yang tidak
    ditutup (</title>, dst. hilang).

    Kalau tag ini tidak ditutup, html.parser stdlib diam-diam menelan SISA
    SELURUH DOKUMEN sebagai "isi"-nya, tanpa peringatan apa pun — title, meta,
    heading, gambar, dan JSON-LD sesudahnya ikut hilang total tanpa jejak.
    Ini bisa terjadi kalau pengguna awam menyalin-tempel "Lihat Sumber
    Halaman" secara terpotong, atau ada bug kecil di template situsnya.

    Perbaikan yang dilakukan (bukan tebak-tebakan, cuma pemulihan wajar):
    kalau ditemukan tag rawtext tanpa penutup yang cocok di sisa dokumen,
    tag itu dianggap "seharusnya sudah ditutup" tepat SEBELUM markah HTML
    (tag) berikutnya muncul — mis. <title>Judul Toko<meta ...> dianggap
    sebagai <title>Judul Toko</title><meta ...> — supaya sisa dokumen bisa
    diparse ulang secara normal. Kalau tidak ada markah lain sama sekali
    sesudahnya, ditutup paksa di akhir dokumen (dokumen memang berhenti di
    tengah elemen ini, bukan menelan struktur lain).

    Mengembalikan (html_hasil_perbaikan, daftar_pesan_peringatan).
    """
    peringatan = []
    potongan = []
    posisi = 0
    n = len(html_teks)

    while posisi < n:
        m_buka = _POLA_BUKA_RAWTEXT.search(html_teks, posisi)
        if not m_buka:
            potongan.append(html_teks[posisi:])
            break

        tag = m_buka.group(1).lower()
        awal_isi = m_buka.end()
        pola_tutup = re.compile(r"</\s*%s\s*>" % tag, re.IGNORECASE)
        m_tutup = pola_tutup.search(html_teks, awal_isi)

        if m_tutup:
            # Ditutup dengan benar — salin apa adanya, tidak perlu diperbaiki.
            potongan.append(html_teks[posisi:m_tutup.end()])
            posisi = m_tutup.end()
            continue

        # Tidak ada tag penutup yang cocok di SISA DOKUMEN sama sekali.
        m_tag_lain = _POLA_TAG_LAIN.search(html_teks, awal_isi)
        if m_tag_lain:
            titik_potong = m_tag_lain.start()
            potongan.append(html_teks[posisi:titik_potong])
            potongan.append(f"</{tag}>")
            posisi = titik_potong
        else:
            potongan.append(html_teks[posisi:])
            potongan.append(f"</{tag}>")
            posisi = n

        peringatan.append(
            f"HTML rusak: tag <{tag}> tidak ditutup (</{tag}> hilang) — dianggap "
            "ditutup otomatis sebelum markah berikutnya supaya sisa halaman tetap "
            "terbaca, tapi hasil audit untuk bagian ini mungkin tidak lengkap. "
            "Cek ulang cara pengambilan HTML-nya (mis. ambil ulang dengan "
            "\"Simpan Halaman Sebagai... HTML lengkap\", bukan salin sebagian)."
        )

    return "".join(potongan), peringatan


# ---------------------------------------------------------------------------
# Analisis per bagian (fungsi murni, gampang dites satu-satu)
# ---------------------------------------------------------------------------

def analisis_title(title):
    if not title:
        return {"ada": False, "panjang": 0, "status": "KOSONG",
                "pesan": "Tidak ada tag <title>. Google biasanya membuat judul sendiri dari isi halaman — hasilnya tidak bisa dikontrol."}
    panjang = len(title)
    if panjang < BATAS_TITLE_MIN:
        status, pesan = "PENDEK", f"Judul cuma {panjang} karakter — kemungkinan kurang deskriptif, ruang di hasil pencarian belum dipakai maksimal."
    elif panjang <= BATAS_TITLE_MAKS:
        status, pesan = "PAS", f"Panjang {panjang} karakter, dalam rentang aman ({BATAS_TITLE_MIN}-{BATAS_TITLE_MAKS})."
    else:
        status, pesan = "PANJANG", f"Panjang {panjang} karakter, kemungkinan terpotong (...) di hasil pencarian Google (perkiraan berbasis jumlah karakter, Google sebenarnya memotong berdasarkan lebar piksel)."
    return {"ada": True, "teks": title, "panjang": panjang, "status": status, "pesan": pesan}


def analisis_meta_description(desc):
    if not desc:
        return {"ada": False, "panjang": 0, "status": "KOSONG",
                "pesan": "Tidak ada meta description. Google akan mengambil cuplikan acak dari isi halaman untuk ditampilkan — tidak bisa dikontrol."}
    panjang = len(desc)
    if panjang < BATAS_DESC_MIN:
        status, pesan = "PENDEK", f"Cuma {panjang} karakter — ruang untuk meyakinkan orang klik belum dipakai maksimal."
    elif panjang <= BATAS_DESC_MAKS:
        status, pesan = "PAS", f"Panjang {panjang} karakter, dalam rentang aman ({BATAS_DESC_MIN}-{BATAS_DESC_MAKS})."
    else:
        status, pesan = "PANJANG", f"Panjang {panjang} karakter, kemungkinan terpotong (...) di hasil pencarian Google (perkiraan berbasis karakter, bukan patokan resmi)."
    return {"ada": True, "teks": desc, "panjang": panjang, "status": status, "pesan": pesan}


def analisis_heading(headings):
    h1_list = [teks for lvl, teks in headings if lvl == 1]
    lompatan = []
    max_terlihat = 0
    for lvl, teks in headings:
        if lvl > max_terlihat + 1:
            lompatan.append({"dari": max_terlihat, "ke": lvl, "teks_heading": teks})
        max_terlihat = max(max_terlihat, lvl)
    kosong = [f"H{lvl}" for lvl, teks in headings if not teks]
    return {
        "total": len(headings),
        "jumlah_h1": len(h1_list),
        "isi_h1": h1_list,
        "urutan": [{"level": lvl, "teks": teks} for lvl, teks in headings],
        "lompatan_level": lompatan,
        "heading_teks_kosong": kosong,
    }


def analisis_gambar(images):
    tanpa_atribut_alt = [im["src"] for im in images if not im["punya_alt"]]
    alt_kosong = [im["src"] for im in images if im["punya_alt"] and im["alt_kosong"]]
    return {
        "total": len(images),
        "tanpa_atribut_alt": tanpa_atribut_alt,
        "alt_kosong": alt_kosong,
    }


def _format_bermasalah(href):
    if href is None:
        return "tidak_ada_href"
    h = href.strip()
    if h == "" or h == "#":
        return "kosong_atau_pagar"
    if h.lower().startswith("javascript:"):
        return "javascript_pseudo_link"
    if POLA_SPASI_MENTAH.search(h):
        return "mengandung_spasi_mentah"
    return None


def analisis_tautan(links):
    bermasalah = []
    for l in links:
        alasan = _format_bermasalah(l["href"])
        if alasan:
            bermasalah.append({"href": l["href"], "alasan": alasan})
    return {"total": len(links), "bermasalah": bermasalah}


def analisis_canonical(canonical, url=None):
    hasil = {"ada": bool(canonical), "nilai": canonical}
    if canonical and url:
        hasil["sama_dengan_url"] = canonical.rstrip("/") == url.rstrip("/")
    return hasil


def analisis_robots(meta_robots):
    if not meta_robots:
        return {"ada": False, "noindex": False}
    nilai = meta_robots.lower()
    return {"ada": True, "nilai": meta_robots, "noindex": "noindex" in nilai, "nofollow": "nofollow" in nilai}


def analisis_og(og):
    hilang = [k for k in OG_WAJIB if k not in og]
    return {"ditemukan": og, "wajib_hilang": hilang}


def analisis_jsonld(blok_list):
    hasil = []
    for i, mentah in enumerate(blok_list, start=1):
        teks = mentah.strip()
        entri = {"urutan": i}
        if not teks:
            entri.update(valid=False, error="blok JSON-LD kosong")
            hasil.append(entri)
            continue
        try:
            data = json.loads(teks)
        except json.JSONDecodeError as e:
            entri.update(valid=False, error=f"JSON tidak valid: {e.msg} (baris {e.lineno}, kolom {e.colno})")
            hasil.append(entri)
            continue
        entri["valid"] = True
        objek_list = data if isinstance(data, list) else [data]
        if isinstance(data, dict) and "@graph" in data and isinstance(data["@graph"], list):
            objek_list = data["@graph"]
        tipe_semua = []
        catatan = []
        for obj in objek_list:
            if not isinstance(obj, dict):
                continue
            tipe = obj.get("@type")
            tipe_list = tipe if isinstance(tipe, list) else [tipe] if tipe else []
            tipe_semua += [t for t in tipe_list if t]
            if "LocalBusiness" in tipe_list or any(str(t).endswith("Business") for t in tipe_list):
                catatan += _cek_localbusiness(obj)
            if "Product" in tipe_list:
                catatan += _cek_product(obj)
        entri["tipe"] = tipe_semua
        entri["catatan"] = catatan
        hasil.append(entri)
    return hasil


def _cek_localbusiness(obj):
    catatan = []
    if not obj.get("name"):
        catatan.append("LocalBusiness: field 'name' tidak ada.")
    alamat = obj.get("address")
    if not alamat:
        catatan.append("LocalBusiness: field 'address' tidak ada — penting untuk usaha lokal Indonesia (harus cocok dengan Google Business Profile).")
    elif isinstance(alamat, dict):
        for f in ("streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry"):
            if not alamat.get(f):
                catatan.append(f"LocalBusiness.address: field '{f}' tidak ada.")
    if not obj.get("telephone"):
        catatan.append("LocalBusiness: field 'telephone' tidak ada — penting untuk konsistensi NAP (Nama-Alamat-Telepon).")
    if not (obj.get("openingHoursSpecification") or obj.get("openingHours")):
        catatan.append("LocalBusiness: jam operasional (openingHours/openingHoursSpecification) tidak ada — opsional tapi disarankan.")
    return catatan


def _cek_product(obj):
    catatan = []
    if not obj.get("name"):
        catatan.append("Product: field 'name' tidak ada.")
    if not obj.get("image"):
        catatan.append("Product: field 'image' tidak ada.")
    tawaran = obj.get("offers")
    if not tawaran:
        catatan.append("Product: field 'offers' (harga) tidak ada.")
    else:
        tawaran_list = tawaran if isinstance(tawaran, list) else [tawaran]
        for t in tawaran_list:
            if not isinstance(t, dict):
                continue
            if not t.get("price") and not t.get("priceSpecification"):
                catatan.append("Product.offers: 'price' tidak ada.")
            if not t.get("priceCurrency"):
                catatan.append("Product.offers: 'priceCurrency' tidak ada (harus 'IDR' untuk toko Indonesia).")
            if not t.get("availability"):
                catatan.append("Product.offers: 'availability' tidak ada (mis. https://schema.org/InStock).")
    if "aggregateRating" in obj or "review" in obj:
        catatan.append("Product punya aggregateRating/review — PASTIKAN datanya asli, bukan dikarang (rating/ulasan palsu melanggar UU Perlindungan Konsumen & aturan Google).")
    return catatan


def analisis_kata_kunci(kata_kunci, title, headings, paragraf_awal, url):
    if not kata_kunci:
        return None
    kk = kata_kunci.lower().strip()
    h1_gabungan = " ".join(teks for lvl, teks in headings if lvl == 1).lower()
    return {
        "kata_kunci": kata_kunci,
        "di_title": bool(title) and kk in title.lower(),
        "di_h1": kk in h1_gabungan,
        "di_url": bool(url) and kk.replace(" ", "-") in url.lower(),
        "di_paragraf_awal": bool(paragraf_awal) and kk in paragraf_awal.lower(),
    }


def ukuran_halaman(jumlah_bytes):
    kb = jumlah_bytes / 1024
    if kb < 100:
        catatan = "Ukuran HTML mentah kecil, kemungkinan bukan penyebab lambat."
    elif kb < 300:
        catatan = "Ukuran HTML sedang — cek juga ukuran gambar/CSS/JS (tidak terhitung di sini)."
    else:
        catatan = "HTML mentah cukup besar untuk sekadar teks/markup — periksa apakah ada kode/komentar berlebih yang bisa dibersihkan."
    return {"bytes": jumlah_bytes, "kb": round(kb, 1), "catatan": catatan,
            "peringatan": "Ini hanya ukuran file HTML mentah (belum termasuk gambar, CSS, JS, dan belum dikompresi/gzip) — bukan waktu muat sungguhan."}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def analisis_lengkap(path, kata_kunci=None, url=None):
    html_teks, jumlah_bytes, catatan_encoding = baca_html(path)
    html_diperbaiki, peringatan_html_rusak = perbaiki_tag_rawtext_tidak_tertutup(html_teks)
    p = ekstrak(html_diperbaiki)
    return {
        "catatan_encoding": catatan_encoding,
        "peringatan_html_rusak": peringatan_html_rusak,
        "title": analisis_title(p.title),
        "meta_description": analisis_meta_description(p.meta_description),
        "heading": analisis_heading(p.headings),
        "gambar": analisis_gambar(p.images),
        "tautan": analisis_tautan(p.links),
        "canonical": analisis_canonical(p.canonical, url),
        "robots": analisis_robots(p.meta_robots),
        "open_graph": analisis_og(p.og),
        "json_ld": analisis_jsonld(p.jsonld_raw),
        "kata_kunci": analisis_kata_kunci(kata_kunci, p.title, p.headings, p.paragraf_awal, url),
        "html_lang": p.html_lang,
        "paragraf_awal": p.paragraf_awal,
        "ukuran_halaman": ukuran_halaman(jumlah_bytes),
    }


def cetak_teks(hasil):
    def judul(t):
        print(f"\n== {t} ==")

    if hasil["catatan_encoding"]:
        print(f"[PERINGATAN ENCODING] {hasil['catatan_encoding']}")
    for p in hasil.get("peringatan_html_rusak") or []:
        print(f"[PERINGATAN HTML RUSAK] {p}")

    judul("Judul (title)")
    t = hasil["title"]
    print(f"Status: {t['status']}")
    if t["ada"]:
        print(f"Teks : {t['teks']}")
    print(t["pesan"])

    judul("Meta description")
    d = hasil["meta_description"]
    print(f"Status: {d['status']}")
    if d["ada"]:
        print(f"Teks : {d['teks']}")
    print(d["pesan"])

    judul("Heading (H1-H6)")
    h = hasil["heading"]
    print(f"Jumlah H1: {h['jumlah_h1']} ({'baik' if h['jumlah_h1'] == 1 else 'PERIKSA: idealnya tepat 1'})")
    for x in h["isi_h1"]:
        print(f"  H1: {x}")
    if h["lompatan_level"]:
        for lp in h["lompatan_level"]:
            print(f"  [PERINGATAN] Lompat dari H{lp['dari']} ke H{lp['ke']} di heading: \"{lp['teks_heading']}\"")
    else:
        print("  Urutan heading tidak melompat level.")
    if h["heading_teks_kosong"]:
        print(f"  [PERINGATAN] Heading tanpa teks: {', '.join(h['heading_teks_kosong'])}")

    judul("Gambar & teks alternatif (alt)")
    g = hasil["gambar"]
    print(f"Total gambar: {g['total']}")
    print(f"Tanpa atribut alt sama sekali: {len(g['tanpa_atribut_alt'])}")
    for src in g["tanpa_atribut_alt"][:5]:
        print(f"  - {src}")
    print(f"Atribut alt ada tapi kosong: {len(g['alt_kosong'])}")
    for src in g["alt_kosong"][:5]:
        print(f"  - {src}")

    judul("Tautan (format saja, bukan cek hidup/mati)")
    l = hasil["tautan"]
    print(f"Total tautan <a>: {l['total']}")
    print(f"Format bermasalah: {len(l['bermasalah'])}")
    for b in l["bermasalah"][:10]:
        print(f"  - {b['href']!r} ({b['alasan']})")

    judul("Canonical")
    c = hasil["canonical"]
    print(f"Ada: {c['ada']}" + (f" -> {c['nilai']}" if c["ada"] else ""))
    if "sama_dengan_url" in c:
        print(f"Sama dengan URL yang diberikan: {c['sama_dengan_url']}")

    judul("Meta robots")
    r = hasil["robots"]
    if not r["ada"]:
        print("Tidak ada meta robots (berarti default: boleh diindeks & diikuti).")
    else:
        print(f"Nilai: {r['nilai']}")
        if r["noindex"]:
            print("[PERINGATAN] noindex ditemukan — halaman ini DIMINTA agar TIDAK muncul di Google.")
    print("Catatan: X-Robots-Tag lewat header HTTP tidak bisa dicek dari file HTML saja.")

    judul("Open Graph (tampilan saat dibagikan ke WhatsApp/Facebook/dll.)")
    og = hasil["open_graph"]
    print(f"Ditemukan: {', '.join(og['ditemukan']) if og['ditemukan'] else '(tidak ada)'}")
    if og["wajib_hilang"]:
        print(f"[PERINGATAN] Tag penting belum ada: {', '.join(og['wajib_hilang'])}")

    judul("Data terstruktur (JSON-LD)")
    if not hasil["json_ld"]:
        print("Tidak ditemukan blok JSON-LD di file ini.")
    for blok in hasil["json_ld"]:
        if not blok.get("valid"):
            print(f"  Blok #{blok['urutan']}: [ERROR] {blok['error']}")
            continue
        print(f"  Blok #{blok['urutan']}: valid JSON. Tipe: {', '.join(blok['tipe']) or '(tidak ada @type)'}")
        for c2 in blok["catatan"]:
            print(f"    - {c2}")

    if hasil["kata_kunci"]:
        judul(f"Kata kunci utama: \"{hasil['kata_kunci']['kata_kunci']}\"")
        kk = hasil["kata_kunci"]
        for label, kunci in (("Muncul di title", "di_title"), ("Muncul di H1", "di_h1"),
                              ("Muncul di URL", "di_url"), ("Muncul di paragraf awal", "di_paragraf_awal")):
            print(f"  {label}: {'YA' if kk[kunci] else 'TIDAK'}")

    judul("Ukuran halaman (HTML mentah saja)")
    u = hasil["ukuran_halaman"]
    print(f"{u['bytes']} bytes (~{u['kb']} KB). {u['catatan']}")
    print(f"Catatan: {u['peringatan']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cek dasar SEO dari file HTML lokal (tanpa akses internet)")
    ap.add_argument("file", help="Path file HTML lokal yang akan dicek")
    ap.add_argument("--kata-kunci", default=None, help="Kata kunci utama yang ditarget, mis. 'keripik pedas Bandung'")
    ap.add_argument("--url", default=None, help="URL asli halaman (opsional) untuk cek canonical & kata kunci di URL")
    ap.add_argument("--json", action="store_true", help="Cetak hasil sebagai JSON mentah, bukan teks")
    args = ap.parse_args(argv)

    try:
        hasil = analisis_lengkap(args.file, kata_kunci=args.kata_kunci, url=args.url)
    except InputSalah as e:
        print(f"Input tidak valid: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        cetak_teks(hasil)
    return 0


if __name__ == "__main__":
    sys.exit(main())
