#!/usr/bin/env python3
"""listmonk.py - pembantu newsletter untuk listmonk milik pengguna (Python standar saja).

Memanggil REST API listmonk (/api/...). Tidak menyalin kode listmonk.
Kunci/token TIDAK pernah dicetak. Pengiriman ke daftar penerima dijaga gerbang
konfirmasi: harus menyebut jumlah penerima yang sudah ditunjukkan ke pengguna.

Kode keluar: 0 sukses | 2 pemakaian salah | 3 konfigurasi/berkas | 4 tidak bisa
menghubungi server | 5 ditolak server (akses/kredensial) | 6 DITOLAK aturan
keamanan skill | 7 ambigu/tidak ditemukan.
"""
import argparse
import csv
import getpass
import hashlib
import io
import ipaddress
import json
import os
import re
import stat
import unicodedata
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

VERSI = "1.0.1"
DIR_KONFIG = os.path.join(os.path.expanduser("~"), ".komunitech")
F_ALAMAT = os.path.join(DIR_KONFIG, "listmonk-alamat.txt")
F_AKUN = os.path.join(DIR_KONFIG, "listmonk-akun.txt")
F_TOKEN = os.path.join(DIR_KONFIG, "listmonk-token.txt")
F_UJI = os.path.join(DIR_KONFIG, "listmonk-uji.json")
F_ALAMAT_UJI = os.path.join(DIR_KONFIG, "listmonk-alamat-uji.txt")
F_LOG_IMPOR = os.path.join(DIR_KONFIG, "listmonk-log-impor.jsonl")
MAKS_ALAMAT_UJI = 3
ALAMAT_BAWAAN = "http://localhost:9000"
TZ = {"WIB": 7, "WITA": 8, "WIT": 9}
MAKS_BERKAS = 50 * 1024 * 1024
# Sumber persetujuan. Ini HANYA pengaman tambahan (kata kunci mudah dielak); tanggung jawab
# tetap pada pemilik daftar. Aturan: sumber TERLARANG selalu ditolak; sumber SAH dikenali dari
# kata kunci; sumber TAK DIKENAL wajib dikonfirmasi pengguna dan jawabannya dicatat.
_TERLARANG = [
    r"\b(beli|dibeli|membeli|belian|sewa|disewa|menyewa|jual[- ]?beli|bought|purchased|rented|buy)\b",
    r"scrap", r"crawl", r"harvest", r"vendor", r"suplier", r"supplier", r"broker", r"reseller data",
    r"databas", r"data ?base", r"bocor", r"leak", r"curi", r"stolen", r"bekas", r"hack",
    r"\b(grup|group|grub|gc|wag)\b", r"\bwa ?(grup|group|gc)\b", r"grup ?(wa|whatsapp|telegram|tele|fb|facebook)",
    r"teman", r"kenalan", r"kawan", r"sahabat", r"saudara", r"tetangga", r"rekan", r"kolega", r"friend",
    r"dapat dari", r"dapet dari", r"dari orang", r"dikasih", r"dikirimin\b", r"dititip", r"titip", r"tukar", r"barter",
    r"marketplace", r"tokopedia", r"shopee", r"lazada", r"bukalapak", r"tiktok ?shop",
    r"instagram", r"\big\b", r"facebook", r"linkedin", r"medsos", r"media sosial", r"followers?", r"pengikut",
    r"google maps", r"direktori", r"directory", r"yellow ?pages", r"website orang", r"cari di", r"ambil dari",
    r"copy", r"salin", r"\bhasil (ambil|kumpul|cari|unduh|download)\b", r"\bbot\b", r"cold ?(email|mail|list)",
    r"tidak (tahu|ingat)", r"nggak (tahu|ingat|tau)", r"gak (tahu|ingat|tau)", r"\blupa\b", r"entah", r"unknown", r"tak diketahui",
    r"pokoknya", r"semua orang", r"asal (kirim|ambil)",
]
_RE_TERLARANG = re.compile("|".join(_TERLARANG), re.I)
# bentuk tanpa spasi/tanda baca, untuk mengelak ejaan "s c r a p" / "b3li"
_STEM_PADAT = ("scrap", "vendor", "database", "grupwa", "wagrup", "grupwhatsapp", "curian", "bocor", "dibeli",
               "membeli", "harvest", "crawl", "hasilbeli", "hasilbeli", "temanku", "dapatdari", "marketplace")
_LEET = str.maketrans("013457@$", "oieastas")
_SAH = re.compile(
    r"(formulir|\bform\b|web ?form|halaman (daftar|pendaftaran)|pendaftaran (di |lewat )?(website|situs|web|online)|"
    r"(daftar|subscribe|berlangganan) (sendiri )?(lewat|di|via|melalui) (website|situs|web|form|formulir)|landing ?page|"
    r"(checkout|check-?out|kasir online).{0,40}(opt-?in|centang|tickbox|checkbox|setuju|persetujuan)|"
    r"(opt-?in|centang|tickbox|checkbox|setuju|persetujuan).{0,40}(checkout|check-?out)|"
    r"persetujuan tertulis|surat persetujuan|tanda tangan|ditandatangani|"
    r"persetujuan (yang )?(direkam|terekam)|rekaman persetujuan|persetujuan rekaman|recorded consent|written consent|"
    r"consent form|mendaftar sendiri|\bqr)", re.I)


def normal_sumber(teks):
    t = unicodedata.normalize("NFKD", teks or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t.lower()


def klasifikasi_sumber(teks):
    """-> 'terlarang' | 'sah' | 'tak_dikenal'. Terlarang menang atas sah."""
    t = normal_sumber(teks)
    varian = [t, t.translate(_LEET)]
    for v in varian:
        if _RE_TERLARANG.search(v):
            return "terlarang"
        padat = re.sub(r"[^a-z0-9]", "", v)
        if any(st in padat for st in _STEM_PADAT):
            return "terlarang"
    if _SAH.search(t):
        return "sah"
    return "tak_dikenal"


KATA_SPAM = ["gratis!!!", "100% untung", "pasti untung", "klik sekarang!!!", "menang undian",
             "transfer dulu", "hadiah pasti", "free money"]
RE_EMAIL = re.compile(r"^[A-Za-z0-9._%+\-']+@[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?)+$")
TYPO = {"gmial.com": "gmail.com", "gmai.com": "gmail.com", "gmail.co": "gmail.com",
        "gmail.con": "gmail.com", "gmal.com": "gmail.com", "yahooo.com": "yahoo.com",
        "yaho.com": "yahoo.com", "yahoo.co": "yahoo.com", "hotmial.com": "hotmail.com",
        "gmail.cm": "gmail.com", "outlok.com": "outlook.com"}


class Galat(Exception):
    def __init__(self, pesan, kode=1):
        super().__init__(pesan)
        self.kode = kode


def cetak(*a):
    print(*a)


def rp_angka(n):
    return f"{n:,}".replace(",", ".")


def persen(x):
    return f"{x:.1f}".replace(".", ",") + "%"


# ---------------------------------------------------------------- konfigurasi
def baca_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def tulis_rahasia(path, isi):
    os.makedirs(DIR_KONFIG, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(isi.strip() + "\n")
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def host_lokal(host):
    if host in ("localhost",) or host.endswith(".local") or "." not in host:
        return True
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False


class Konfig:
    def __init__(self, args):
        url = getattr(args, "url", None) or os.environ.get("LISTMONK_URL") or baca_file(F_ALAMAT) or ALAMAT_BAWAAN
        url = url.strip().rstrip("/")
        p = urllib.parse.urlparse(url)
        if p.scheme not in ("http", "https") or not p.hostname:
            raise Galat("Alamat listmonk tidak valid (harus diawali http:// atau https://).", 2)
        if not host_lokal(p.hostname):
            if p.scheme != "https":
                raise Galat("Alamat internet wajib HTTPS (token bisa terbaca orang lain bila http).", 2)
            if not getattr(args, "izinkan_jarak_jauh", False):
                raise Galat("Alamat ini server internet. Jalankan dengan --izinkan-jarak-jauh HANYA bila "
                            "Anda sendiri yang mengetik alamat itu.", 2)
        self.url = url
        self.lokal = host_lokal(p.hostname)
        self.user = os.environ.get("LISTMONK_USER") or baca_file(F_AKUN)
        tok = os.environ.get("LISTMONK_TOKEN", "")
        if not tok:
            tf = getattr(args, "token_file", None) or os.environ.get("LISTMONK_TOKEN_FILE") or F_TOKEN
            tok = baca_file(tf)
            if not tok and (getattr(args, "token_file", None) or os.environ.get("LISTMONK_TOKEN_FILE")):
                raise Galat(f"File token '{tf}' tidak ditemukan/kosong.", 3)
        self.token = tok

    def butuh_akun(self):
        if not self.user or not self.token:
            raise Galat("Akun API belum disimpan. Minta pengguna menjalankan SENDIRI: "
                        "python3 scripts/listmonk.py simpan-akun (lihat docs/panduan-listmonk.md).", 3)


class _TanpaRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def buka_url(cfg, req):
    handlers = [_TanpaRedirect()]
    if cfg.lokal:
        handlers.append(urllib.request.ProxyHandler({}))
    return urllib.request.build_opener(*handlers).open(req, timeout=30)


def samarkan(teks, cfg):
    if cfg.token:
        teks = teks.replace(cfg.token, "****")
    return teks


def api(cfg, metode, path, data=None, params=None, multipart=None, ok404=False):
    cfg.butuh_akun()
    url = cfg.url + "/api" + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    headers = {"Authorization": f"token {cfg.user}:{cfg.token}", "Accept": "application/json",
               "User-Agent": "komunitech-listmonk/" + VERSI}
    body = None
    if multipart is not None:
        b = "----kt" + uuid.uuid4().hex
        parts = []
        for nama, (fn, isi, ctype) in multipart.items():
            h = f'--{b}\r\nContent-Disposition: form-data; name="{nama}"'
            if fn:
                h += f'; filename="{fn}"'
            h += f"\r\nContent-Type: {ctype}\r\n\r\n"
            parts.append(h.encode() + (isi if isinstance(isi, bytes) else isi.encode("utf-8")) + b"\r\n")
        body = b"".join(parts) + f"--{b}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={b}"
    elif data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=metode)
    try:
        with buka_url(cfg, req) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        raw = e.read()
        pesan = ""
        try:
            pesan = json.loads(raw).get("message", "")
        except Exception:
            pass
        pesan = samarkan(str(pesan), cfg)[:300]
        if e.code in (301, 302, 303, 307, 308):
            raise Galat(f"listmonk mengalihkan (HTTP {e.code}). Simpan alamat tujuan akhir dengan "
                        "'simpan-alamat' (mis. http -> https).", 4)
        if e.code == 404 and ok404:
            return None
        if e.code in (401, 403):
            raise Galat(f"Ditolak listmonk (HTTP {e.code}): {pesan or 'akun/token salah atau tidak berhak'}. "
                        "Periksa akun API dan perannya (docs/panduan-listmonk.md).", 5)
        if e.code == 404:
            if not pesan:
                raise Galat(f"Tidak ditemukan (HTTP 404) di {path}. Alamat ini mungkin BUKAN server listmonk "
                            "(atau listmonk versi lama/alamat kurang awalan). Periksa alamat dengan 'cek'.", 7)
            raise Galat(f"Tidak ditemukan (HTTP 404) di {path}: {pesan}", 7)
        raise Galat(f"listmonk menolak (HTTP {e.code}): {pesan}", 5 if e.code < 500 else 4)
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        raise Galat(f"Tidak bisa menghubungi listmonk di {cfg.url}. Pastikan listmonk menyala dan alamat benar. "
                    f"({samarkan(str(getattr(e, 'reason', e)), cfg)[:120]})", 4)
    try:
        return json.loads(raw)
    except ValueError:
        raise Galat("Jawaban bukan JSON - mungkin ini bukan server listmonk.", 4)


# ---------------------------------------------------------------- berkas kontak
def baca_teks(path):
    if not os.path.isfile(path):
        raise Galat(f"Berkas tidak ditemukan: {path}", 3)
    if os.path.getsize(path) > MAKS_BERKAS:
        raise Galat("Berkas terlalu besar (>50 MB).", 3)
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def kolom_xlsx(path):
    """Baca lembar pertama .xlsx (stdlib zipfile) -> list baris (list string)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise Galat("Berkas .xlsx rusak atau bukan Excel asli. Simpan ulang dari Excel sebagai .csv.", 3)
    with z:
        if sum(i.file_size for i in z.infolist()) > MAKS_BERKAS * 4:
            raise Galat("Isi .xlsx terlalu besar setelah dibuka.", 3)
        nama = z.namelist()
        ss = []
        if "xl/sharedStrings.xml" in nama:
            try:
                akar_ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
            except ET.ParseError:
                raise Galat("Daftar teks Excel rusak/tidak terbaca. Simpan ulang dari Excel sebagai .csv.", 3)
            for si in akar_ss.findall("m:si", ns):
                ss.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        sheets = sorted(n for n in nama if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        if not sheets:
            raise Galat("Tidak ada lembar kerja di berkas Excel.", 3)
        rows = []
        try:
            akar = ET.fromstring(z.read(sheets[0]))
        except (ET.ParseError, KeyError, ValueError):
            raise Galat("Isi lembar Excel rusak/tidak terbaca. Simpan ulang dari Excel sebagai .csv.", 3)
        for r in akar.iter("{%s}row" % ns["m"]):
            baris = {}
            for c in r.findall("m:c", ns):
                ref = c.get("r", "")
                huruf = re.match(r"[A-Z]+", ref)
                idx = 0
                for ch in (huruf.group(0) if huruf else "A"):
                    idx = idx * 26 + ord(ch) - 64
                t = c.get("t")
                v = c.find("m:v", ns)
                if t == "s" and v is not None and v.text is not None:
                    try:
                        val = ss[int(v.text)] if 0 <= int(v.text) < len(ss) else ""
                    except ValueError:
                        val = ""
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % ns["m"]))
                else:
                    val = v.text if v is not None and v.text is not None else ""
                baris[idx - 1] = val
            if baris:
                rows.append([baris.get(i, "") for i in range(max(baris) + 1)])
        return rows


def baca_baris_kontak(path):
    if path.lower().endswith((".xlsx", ".xlsm")):
        if not os.path.isfile(path):
            raise Galat(f"Berkas tidak ditemukan: {path}", 3)
        return kolom_xlsx(path)
    if path.lower().endswith(".xls"):
        raise Galat("Format .xls lama tidak didukung. Buka di Excel lalu Simpan Sebagai .xlsx atau .csv.", 3)
    teks = baca_teks(path)
    sampel = teks[:4096]
    delim = max([",", ";", "\t", "|"], key=lambda d: sampel.count(d))
    return list(csv.reader(io.StringIO(teks), delimiter=delim))


NAMA_EMAIL = ("email", "e-mail", "surel", "alamat email", "email address", "mail")
NAMA_NAMA = ("name", "nama", "nama lengkap", "nama pelanggan", "full name")
NAMA_IZIN = ("setuju", "persetujuan", "consent", "izin", "opt-in", "optin", "berlangganan", "subscribe")
NEGATIF = {"tidak", "no", "n", "0", "false", "tdk", "batal", "unsubscribe", "berhenti", "belum"}
# Kolom persetujuan: HANYA nilai ini yang dianggap setuju. Kosong/tidak jelas = TIDAK setuju.
POSITIF = {"ya", "y", "yes", "iya", "ya.", "setuju", "sudah", "ok", "oke", "true", "1", "benar", "agree", "opt-in", "optin"}
NAMA_SUMBER = ("sumber", "source", "asal", "origin", "dari mana", "asal kontak")


def bersihkan_teks(t, maks):
    """Buang karakter kontrol dan awalan =+-@ (injeksi rumus Excel) sepenuhnya."""
    t = "".join(c for c in (t or "") if c >= " " and c != "\x7f")
    t = re.sub(r"^[=+\-@\s|]+", "", t.strip())
    return t[:maks]


def analisis_kontak(rows, kol_email=None, kol_nama=None):
    if not rows:
        raise Galat("Berkas kosong.", 3)
    header = [h.strip() for h in rows[0]]
    low = [h.lower() for h in header]

    def cari(pilihan, dipaksa):
        if dipaksa:
            if dipaksa.lower() not in low:
                raise Galat(f"Kolom '{dipaksa}' tidak ada. Kolom yang ada: {', '.join(header)}", 3)
            return low.index(dipaksa.lower())
        for p in pilihan:
            if p in low:
                return low.index(p)
        return None

    ie = cari(NAMA_EMAIL, kol_email)
    baris_data = rows[1:]
    if ie is None:
        # mungkin tanpa header: kolom yang berisi email
        cocok = [i for i in range(len(rows[0])) if RE_EMAIL.match(rows[0][i].strip())]
        if cocok:
            ie = cocok[0]
            header = [f"kolom{i + 1}" for i in range(len(rows[0]))]
            low = header
            baris_data = rows
        else:
            raise Galat("Kolom email tidak ditemukan. Beri nama kolom 'email' atau pakai --kolom-email.", 3)
    inama = cari(NAMA_NAMA, kol_nama)
    iizin = None
    for p in NAMA_IZIN:
        if p in low:
            iizin = low.index(p)
            break
    isum = None
    for p in NAMA_SUMBER:
        if p in low:
            isum = low.index(p)
            break
    hasil = {"ok": [], "tidak_valid": [], "duplikat": [], "tanpa_izin": [], "izin_kosong": 0, "mencurigakan": [],
             "kosong": 0, "formula_dibersihkan": 0, "sumber_terlarang": [],
             "kolom_ekstra": [h for i, h in enumerate(header) if i not in (ie, inama, iizin) and h]}
    lihat = set()
    for n, r in enumerate(baris_data, start=2):
        if not any(c.strip() for c in r):
            hasil["kosong"] += 1
            continue
        em = (r[ie] if ie < len(r) else "").strip().strip("<>").lower()
        if not RE_EMAIL.match(em) or ".." in em or len(em) > 254:
            hasil["tidak_valid"].append((n, em))
            continue
        if isum is not None and isum < len(r) and klasifikasi_sumber(r[isum]) == "terlarang":
            hasil["sumber_terlarang"].append((n, em))
            continue
        if iizin is not None:
            nilai = (r[iizin].strip().lower() if iizin < len(r) else "")
            if nilai not in POSITIF:  # kosong / tidak jelas / negatif = tidak setuju
                hasil["tanpa_izin"].append((n, em))
                if not nilai:
                    hasil["izin_kosong"] += 1
                continue
        if em in lihat:
            hasil["duplikat"].append((n, em))
            continue
        lihat.add(em)
        dom = em.split("@")[1]
        if dom in TYPO:
            hasil["mencurigakan"].append((n, em, f"mungkin maksudnya @{TYPO[dom]}"))
        nama = (r[inama].strip() if inama is not None and inama < len(r) else "")
        bersih = bersihkan_teks(nama, 200)
        if bersih != nama.strip()[:200]:
            hasil["formula_dibersihkan"] += 1
        nama = bersih
        if not nama:
            nama = re.sub(r"[._\-\d]+", " ", em.split("@")[0]).strip().title() or em.split("@")[0]
        attr = {}
        for i, h in enumerate(header):
            if i in (ie, inama, iizin) or not h or i >= len(r) or not r[i].strip():
                continue
            nilai_attr = bersihkan_teks(r[i], 500)
            if nilai_attr != r[i].strip()[:500]:
                hasil["formula_dibersihkan"] += 1
            if nilai_attr:
                attr[bersihkan_teks(h, 100) or h] = nilai_attr
        hasil["ok"].append({"email": em, "name": nama, "attributes": attr})
    return hasil


def tulis_csv_bersih(daftar, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["email", "name", "attributes"])
        for d in daftar:
            w.writerow([d["email"], d["name"], json.dumps(d["attributes"], ensure_ascii=False)])


def laporan_kontak(h, tulis=cetak):
    tulis(f"Kontak valid dan siap diimpor : {rp_angka(len(h['ok']))}")
    tulis(f"Email tidak valid (dibuang)   : {rp_angka(len(h['tidak_valid']))}")
    tulis(f"Duplikat (dibuang)            : {rp_angka(len(h['duplikat']))}")
    tulis(f"Menolak/belum setuju (dibuang): {rp_angka(len(h['tanpa_izin']))}")
    if h.get("izin_kosong"):
        tulis(f"  - {rp_angka(h['izin_kosong'])} di antaranya kolom persetujuan KOSONG (kosong dianggap TIDAK setuju).")
    if h.get("sumber_terlarang"):
        tulis(f"Sumber kolom 'sumber' tergolong tidak berizin (dibuang): {rp_angka(len(h['sumber_terlarang']))}")
    if h.get("formula_dibersihkan"):
        tulis(f"Sel bertanda rumus (=,+,-,@) dibersihkan: {rp_angka(h['formula_dibersihkan'])}")
    tulis(f"Baris kosong                  : {rp_angka(h['kosong'])}")
    if h["mencurigakan"]:
        tulis(f"Perlu dicek manual (salah ketik?) - TETAP disertakan: {len(h['mencurigakan'])}")
        for n, e, s in h["mencurigakan"][:10]:
            tulis(f"  baris {n}: {samar_email(e)} ({s})")
    if h["tidak_valid"]:
        tulis("Contoh baris tidak valid: " + ", ".join(f"baris {n}" for n, _ in h["tidak_valid"][:10]))
    if h["kolom_ekstra"]:
        tulis("Kolom tambahan disimpan sebagai atribut: " + ", ".join(h["kolom_ekstra"]))


def samar_email(e):
    if "@" not in e:
        return e[:1] + "***"
    u, d = e.split("@", 1)
    return (u[:1] + "***@" + d) if len(u) > 1 else ("*@" + d)


# ---------------------------------------------------------------- perintah: konfigurasi
def cmd_simpan_alamat(args):
    url = args.alamat.strip().rstrip("/")
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise Galat("Alamat harus diawali http:// atau https://", 2)
    if not host_lokal(p.hostname) and p.scheme != "https":
        raise Galat("Alamat internet wajib HTTPS.", 2)
    os.makedirs(DIR_KONFIG, exist_ok=True)
    with open(F_ALAMAT, "w", encoding="utf-8") as f:
        f.write(url + "\n")
    cetak(f"Alamat disimpan: {url}")


def cmd_simpan_akun(args):
    if not sys.stdin.isatty() and not args.dari_stdin:
        raise Galat("Perintah ini harus dijalankan pengguna sendiri di terminal (token diketik tersembunyi). "
                    "Agent jangan meminta token di chat.", 3)
    if os.path.exists(F_TOKEN) and not args.ya:
        raise Galat("Token sudah tersimpan. Tambahkan --ya untuk menimpa.", 3)
    user = args.pengguna or input("Nama pengguna API (mis. agen): ").strip()
    tok = getpass.getpass("Tempel token API (tidak tampil): ").strip() if not args.dari_stdin else sys.stdin.readline().strip()
    if not user or not tok:
        raise Galat("Nama pengguna dan token wajib diisi.", 2)
    os.makedirs(DIR_KONFIG, exist_ok=True)
    tulis_rahasia(F_AKUN, user)
    tulis_rahasia(F_TOKEN, tok)
    cetak(f"Tersimpan di {DIR_KONFIG} (izin hanya pemilik). Token tidak ditampilkan.")


def cmd_cek(args):
    cfg = Konfig(args)
    cetak(f"Alamat listmonk: {cfg.url}")
    if not cfg.user or not cfg.token:
        raise Galat("Akun API belum tersimpan (jalankan 'simpan-akun').", 3)
    cetak(f"Akun API: {cfg.user} | token: {'*' * 8} (tersimpan)")
    d = api(cfg, "GET", "/lists", params={"per_page": 1, "minimal": "true"})
    total = d.get("data", {}).get("total", len(d.get("data", {}).get("results", [])))
    cetak(f"NYAMBUNG. Jumlah list terlihat: {total}")
    try:
        c = api(cfg, "GET", "/campaigns", params={"per_page": 1})
        cetak(f"Kampanye terlihat: {c['data'].get('total', '?')}")
    except Galat as e:
        cetak(f"Catatan: akun tidak bisa melihat kampanye ({e})")


# ---------------------------------------------------------------- perintah: list & pelanggan
def ambil_semua(cfg, path, params=None, kunci="results"):
    hasil, page = [], 1
    while True:
        p = dict(params or {})
        p.update(page=page, per_page=200)
        d = api(cfg, "GET", path, params=p)["data"]
        hasil += d.get(kunci, [])
        if len(hasil) >= d.get("total", 0) or not d.get(kunci) or page > 500:
            return hasil, d.get("total", len(hasil))
        page += 1


def cmd_daftar_list(args):
    cfg = Konfig(args)
    hasil, _ = ambil_semua(cfg, "/lists", {"minimal": "false"})
    if args.json:
        cetak(json.dumps([{k: l.get(k) for k in ("id", "name", "type", "optin", "subscriber_count")} for l in hasil], ensure_ascii=False))
        return
    cetak(f"{'ID':>4}  {'Nama':<30} {'Tipe':<8} {'Opt-in':<7} {'Pelanggan':>9}")
    for l in hasil:
        cetak(f"{l['id']:>4}  {l['name'][:30]:<30} {l['type']:<8} {l['optin']:<7} {rp_angka(l.get('subscriber_count', 0)):>9}")
    if not hasil:
        cetak("(belum ada list)")
    cetak("Catatan: 'Pelanggan' dari cache listmonk, bisa tertinggal beberapa menit.")


def cmd_buat_list(args):
    cfg = Konfig(args)
    d = api(cfg, "POST", "/lists", data={"name": args.nama, "type": args.tipe, "optin": args.optin,
                                          "tags": args.tag or [], "description": args.deskripsi or ""})
    l = d["data"]
    cetak(f"List dibuat: #{l['id']} {l['name']} (tipe {l['type']}, opt-in {l['optin']})")
    if l["optin"] != "double":
        cetak("PERHATIAN: opt-in 'single' - orang langsung berlangganan tanpa konfirmasi email. "
              "Untuk newsletter, 'double' lebih aman (bukti persetujuan UU PDP).")


def cari_list(cfg, ref):
    hasil, _ = ambil_semua(cfg, "/lists", {"minimal": "false"})
    if str(ref).isdigit():
        for l in hasil:
            if l["id"] == int(ref):
                return l
        raise Galat(f"List #{ref} tidak ditemukan.", 7)
    cocok = [l for l in hasil if ref.lower() in l["name"].lower()]
    if len(cocok) == 1:
        return cocok[0]
    raise Galat(f"Nama list '{ref}' cocok dengan {len(cocok)} list. Pakai nomor ID dari 'daftar-list'.", 7)


def hitung_pelanggan(cfg, list_id, status):
    d = api(cfg, "GET", "/subscribers", params={"list_id": list_id, "subscription_status": status, "per_page": 1})
    return d["data"].get("total", 0)


def cmd_periksa_kontak(args):
    h = analisis_kontak(baca_baris_kontak(args.berkas), args.kolom_email, args.kolom_nama)
    laporan_kontak(h)
    if args.keluaran:
        tulis_csv_bersih(h["ok"], args.keluaran)
        cetak(f"CSV bersih ditulis: {args.keluaran}")
    cetak("INGAT: pastikan tiap orang di berkas ini SUDAH setuju menerima email Anda (lihat SKILL.md, UU PDP).")


def catat_impor(rekam):
    """Tambahkan satu baris JSON ke log impor lokal (tanpa email/kontak, izin 600)."""
    rekam = dict(rekam, waktu=datetime.now().isoformat(timespec="seconds"))
    os.makedirs(DIR_KONFIG, exist_ok=True)
    fd = os.open(F_LOG_IMPOR, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as f:
        f.write(json.dumps(rekam, ensure_ascii=False) + "\n")


def sidik_berkas(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except OSError:
        return ""


def cmd_impor(args):
    sumber = (args.sumber_persetujuan or "").strip()
    if not args.saya_punya_izin or not sumber:
        raise Galat("DITOLAK: impor wajib menyebut asal persetujuan (--sumber-persetujuan \"...\") dan "
                    "--saya-punya-izin. Sumber yang sah: formulir di website, kotak opt-in saat checkout, atau "
                    "persetujuan tertulis/terekam. Tanyakan pengguna: dari mana kontak ini dan bagaimana mereka setuju?", 6)
    berkas = os.path.basename(args.berkas)
    kelas = klasifikasi_sumber(sumber)
    if kelas != "terlarang" and klasifikasi_sumber(berkas) == "terlarang":
        kelas = "terlarang"
    rekam = {"berkas": berkas[:80], "sidik_berkas": sidik_berkas(args.berkas), "list": str(args.list),
             "sumber": sumber[:200], "klasifikasi": kelas}
    if kelas == "terlarang":
        catat_impor(dict(rekam, hasil="ditolak-sumber-terlarang"))
        raise Galat("DITOLAK: sumber seperti grup WA, vendor, beli/sewa, database, scraping, marketplace, "
                    "medsos, atau 'dapat dari teman' bukan persetujuan. Orang-orang itu tidak pernah setuju "
                    "menerima email Anda (UU PDP 27/2022) dan email Anda bisa diblokir. Impor hanya orang yang "
                    "mendaftar sendiri: formulir website, kotak opt-in saat checkout, atau persetujuan "
                    "tertulis/terekam.", 6)
    konfirmasi = (args.pengguna_konfirmasi_setuju or "").strip()
    if kelas == "tak_dikenal":
        if len(konfirmasi) < 10 or klasifikasi_sumber(konfirmasi) == "terlarang":
            catat_impor(dict(rekam, hasil="ditolak-sumber-belum-dikonfirmasi"))
            raise Galat("DITOLAK: sumber persetujuan ini tidak dikenali sebagai sumber yang sah. TANYAKAN pengguna: "
                        "'Apakah setiap orang di daftar ini sendiri yang mendaftar/setuju menerima email Anda? "
                        "Lewat apa (formulir website, opt-in saat checkout, atau persetujuan tertulis/terekam)?' "
                        "Bila pengguna menegaskan YA, ulangi dengan --pengguna-konfirmasi-setuju \"<jawaban "
                        "pengguna apa adanya>\". Jawaban dicatat di log lokal.", 6)
        rekam["konfirmasi_pengguna"] = konfirmasi[:300]
    if args.sudah_terkonfirmasi and kelas != "sah":
        catat_impor(dict(rekam, hasil="ditolak-terkonfirmasi-tanpa-bukti"))
        raise Galat("DITOLAK: --sudah-terkonfirmasi hanya untuk sumber yang jelas sah (formulir website, checkout "
                    "opt-in, persetujuan tertulis/terekam) dan yang buktinya Anda pegang.", 6)
    cfg = Konfig(args)
    l = cari_list(cfg, args.list)
    h = analisis_kontak(baca_baris_kontak(args.berkas), args.kolom_email, args.kolom_nama)
    laporan_kontak(h)
    if not h["ok"]:
        raise Galat("Tidak ada kontak valid untuk diimpor.", 3)
    status = "confirmed" if args.sudah_terkonfirmasi else "unconfirmed"
    if status == "confirmed" and l["optin"] == "double":
        cetak("PERHATIAN: memakai --sudah-terkonfirmasi (Anda memegang bukti persetujuan tiap orang).")
    cetak(f"Tujuan: list #{l['id']} '{l['name']}' (opt-in {l['optin']}), status langganan awal: {status}")
    if h.get("sumber_terlarang"):
        catat_impor(dict(rekam, hasil="ditolak-kolom-sumber-terlarang"))
        raise Galat("DITOLAK: kolom 'sumber' di berkas menyebut asal yang tidak berizin (beli/grup WA/scraping/dll) "
                    f"pada {len(h['sumber_terlarang'])} baris. Pisahkan hanya orang yang mendaftar sendiri, lalu ulangi.", 6)
    if not args.ya:
        cetak("BELUM DIIMPOR. Tunjukkan ringkasan ini ke pengguna, lalu jalankan ulang dengan --ya.")
        raise Galat("Menunggu konfirmasi (--ya).", 6)
    tmp = io.StringIO()
    w = csv.writer(tmp)
    w.writerow(["email", "name", "attributes"])
    for d in h["ok"]:
        d["attributes"]["sumber_persetujuan"] = args.sumber_persetujuan[:200]
        d["attributes"]["diimpor"] = datetime.now().strftime("%Y-%m-%d")
        w.writerow([d["email"], d["name"], json.dumps(d["attributes"], ensure_ascii=False)])
    params = {"mode": "subscribe", "subscription_status": status, "delim": ",", "lists": [l["id"]],
              "overwrite": False}
    api(cfg, "POST", "/import/subscribers",
        multipart={"params": (None, json.dumps(params), "application/json"),
                   "file": ("kontak.csv", tmp.getvalue(), "text/csv")})
    import time
    for _ in range(60):
        st = api(cfg, "GET", "/import/subscribers")["data"]
        if st.get("status") in ("finished", "failed", "stopped", "none"):
            break
        time.sleep(1)
    cetak(f"Impor {st.get('status')}: {st.get('imported', 0)} dari {st.get('total', 0)} baris.")
    cetak("CATATAN: angka ini menghitung baris yang diproses. Kontak yang SEBELUMNYA berhenti berlangganan atau "
          "diblokir di listmonk TIDAK dihidupkan lagi (sengaja, menghormati pilihan mereka).")
    catat_impor(dict(rekam, hasil="diimpor", status_awal=status, baris=len(h["ok"])))
    if l["optin"] == "double" and status == "unconfirmed":
        cetak("LANGKAH BERIKUTNYA: kirim email konfirmasi (double opt-in) dengan 'kirim-optin'. "
              "Hanya yang klik konfirmasi yang akan menerima newsletter.")


def cmd_kirim_optin(args):
    cfg = Konfig(args)
    l = cari_list(cfg, args.list)
    if l["optin"] != "double":
        raise Galat("List ini opt-in 'single'; tidak ada email konfirmasi yang perlu dikirim.", 2)
    subs, total = ambil_semua(cfg, "/subscribers", {"list_id": l["id"], "subscription_status": "unconfirmed"})
    cetak(f"Email konfirmasi akan dikirim ke {rp_angka(total)} orang berstatus 'belum konfirmasi' di list '{l['name']}'.")
    if not args.ya or args.konfirmasi_penerima != total:
        cetak(f"BELUM DIKIRIM. Tanya pengguna, lalu ulangi dengan --ya --konfirmasi-penerima {total}")
        raise Galat("Menunggu konfirmasi.", 6)
    ok = 0
    for s in subs:
        api(cfg, "POST", f"/subscribers/{s['id']}/optin")
        ok += 1
    cetak(f"Email konfirmasi terkirim ke {ok} orang.")


def cmd_daftar_pelanggan(args):
    cfg = Konfig(args)
    l = cari_list(cfg, args.list)
    cetak(f"List #{l['id']} '{l['name']}' (opt-in {l['optin']})")
    label = {"confirmed": "Sudah konfirmasi", "unconfirmed": "Belum konfirmasi", "unsubscribed": "Berhenti"}
    for st in ("confirmed", "unconfirmed", "unsubscribed"):
        cetak(f"  {label[st]:<18}: {rp_angka(hitung_pelanggan(cfg, l['id'], st))}")
    if args.contoh:
        d = api(cfg, "GET", "/subscribers", params={"list_id": l["id"], "per_page": args.contoh})
        for s in d["data"]["results"]:
            cetak(f"  - {samar_email(s['email'])} ({str(s.get('name', ''))[:30]}) {s.get('status', '?')}")


def cari_email(cfg, em):
    """Cari pelanggan dengan email persis (pakai parameter 'search', tanpa izin SQL)."""
    d = api(cfg, "GET", "/subscribers", params={"search": em, "per_page": 50})
    return [x for x in d["data"]["results"] if x["email"].lower() == em.lower()]


def cmd_hapus_pelanggan(args):
    cfg = Konfig(args)
    res = cari_email(cfg, args.email)
    if not res:
        raise Galat("Email itu tidak ada di listmonk.", 7)
    cetak(f"Ditemukan: {samar_email(res[0]['email'])} (#{res[0]['id']}). Ini menghapus permanen data orang tsb "
          "(hak hapus data - UU PDP).")
    if not args.ya:
        raise Galat("BELUM DIHAPUS. Ulangi dengan --ya setelah pengguna setuju.", 6)
    api(cfg, "DELETE", f"/subscribers/{res[0]['id']}")
    cetak("Terhapus.")


# ---------------------------------------------------------------- kampanye
def sidik(kamp):
    return hashlib.sha256((str(kamp.get("subject", "")) + "\0" + str(kamp.get("body", "")) + "\0" +
                           str(kamp.get("template_id", "")) + "\0" + str(kamp.get("content_type", "")) + "\0" +
                           str(kamp.get("from_email", ""))).encode("utf-8")).hexdigest()[:16]


def muat_uji():
    try:
        with open(F_UJI, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def simpan_uji(cfg, kamp, alamat=""):
    """Catatan uji-kirim lokal: kunci = alamat server + id kampanye; nilai memuat sidik isi (subjek+isi+template+pengirim)."""
    d = muat_uji()
    d[f"{cfg.url}#{kamp['id']}"] = {"sidik": sidik(kamp), "ke": samar_email(alamat) if alamat else "",
                                    "waktu": datetime.now().isoformat(timespec="seconds")}
    os.makedirs(DIR_KONFIG, exist_ok=True)
    with open(F_UJI, "w", encoding="utf-8") as f:
        json.dump(d, f)


def sudah_diuji(cfg, kamp):
    return muat_uji().get(f"{cfg.url}#{kamp['id']}", {}).get("sidik") == sidik(kamp)


def ambil_kampanye(cfg, ref):
    if not str(ref).isdigit():
        raise Galat("Pakai nomor ID kampanye (lihat 'daftar-kampanye').", 2)
    d = api(cfg, "GET", f"/campaigns/{int(ref)}", params={"no_body": "false"}, ok404=True)
    if d is None:
        raise Galat(f"Kampanye #{ref} tidak ditemukan.", 7)
    return d["data"]


def ambil_template(cfg, tid):
    if not tid:
        return ""
    d = api(cfg, "GET", f"/templates/{tid}", ok404=True)
    return (d or {}).get("data", {}).get("body", "") or ""


RE_KOMENTAR = re.compile(r"<!--.*?-->|\{\{/\*.*?\*/\}\}|\{\{-?\s*/\*.*?\*/\s*-?\}\}", re.S)
RE_TAG_BERHENTI = re.compile(r"\{\{-?\s*UnsubscribeURL\s*-?\}\}")


def punya_tautan_berhenti(teks):
    """Tag {{ UnsubscribeURL }} harus ada DI LUAR komentar HTML/template. Komentar tidak dihitung."""
    return bool(RE_TAG_BERHENTI.search(RE_KOMENTAR.sub("", teks or "")))


def lint_kampanye(cfg, k):
    """Kembalikan (galat[], peringatan[])."""
    g, p = [], []
    body = (k.get("body") or "")
    tpl = ambil_template(cfg, k.get("template_id")) if k.get("content_type") != "visual" else ""
    if not punya_tautan_berhenti(body) and not punya_tautan_berhenti(tpl):
        g.append("Tidak ada tautan berhenti berlangganan yang berfungsi: tag {{ UnsubscribeURL }} harus ada di isi "
                 "atau template DI LUAR komentar (tautan di dalam <!-- --> tidak dihitung). Wajib ada.")

    if not (k.get("subject") or "").strip():
        g.append("Subjek kosong.")
    if not k.get("lists"):
        g.append("Kampanye belum memilih list penerima.")
    subj = k.get("subject") or ""
    if len(subj) > 90:
        p.append(f"Subjek {len(subj)} karakter - terlalu panjang (ideal <60).")
    letters = [c for c in subj if c.isalpha()]
    if len(letters) > 8 and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        p.append("Subjek banyak HURUF BESAR - rawan masuk spam.")
    if subj.count("!") > 1:
        p.append("Subjek banyak tanda seru - rawan masuk spam.")
    isi = (subj + " " + body).lower()
    for kata in KATA_SPAM:
        if kata in isi:
            p.append(f"Ada kata/klaim berisiko spam atau menyesatkan: '{kata}'.")
    if "{{" not in subj and "Subscriber" not in body:
        p.append("Belum ada personalisasi (mis. {{ .Subscriber.FirstName }}) - opsional.")
    if not re.search(r"(jl\.|jalan|alamat|wa\b|whatsapp|hubungi|kontak|@)", re.sub(r"<[^>]+>", " ", body).lower()):
        p.append("Tidak terlihat identitas/kontak pengirim di isi email - cantumkan nama usaha & cara menghubungi.")
    if not k.get("from_email"):
        p.append("Alamat pengirim kosong (akan pakai bawaan listmonk).")
    return g, p


def perkirakan_penerima(cfg, k):
    total = 0
    detail = []
    for l in k.get("lists", []):
        info = cari_list(cfg, l["id"])
        conf = hitung_pelanggan(cfg, l["id"], "confirmed")
        unc = hitung_pelanggan(cfg, l["id"], "unconfirmed") if info["optin"] != "double" else 0
        n = conf + unc
        total += n
        detail.append((info["name"], info["optin"], n))
    return total, detail


def cmd_daftar_template(args):
    cfg = Konfig(args)
    for t in api(cfg, "GET", "/templates")["data"]:
        cetak(f"#{t['id']:<3} {t['name'][:40]:<40} {t['type']}{'  (bawaan)' if t.get('is_default') else ''}")


def baca_isi(path, tipe):
    if not os.path.isfile(path):
        raise Galat(f"Berkas isi tidak ditemukan: {path}", 3)
    teks = baca_teks(path)
    if re.search(r"<\s*script\b", teks, re.I):
        raise Galat("Isi email mengandung <script>. Tidak dipakai di email; hapus dulu.", 3)
    return teks


def cmd_buat_kampanye(args):
    cfg = Konfig(args)
    ids = []
    for ref in args.list:
        ids.append(cari_list(cfg, ref)["id"])
    tipe = args.tipe
    body = baca_isi(args.isi_file, tipe)
    data = {"name": args.nama, "subject": args.subjek, "lists": ids, "type": "regular", "content_type": tipe,
            "body": body, "messenger": "email", "template_id": args.template, "tags": args.tag or []}
    if args.dari:
        data["from_email"] = args.dari
    k = api(cfg, "POST", "/campaigns", data=data)["data"]
    cetak(f"Draf kampanye dibuat: #{k['id']} '{k['name']}' - status {k['status']} (BELUM dikirim ke siapa pun).")
    kk = ambil_kampanye(cfg, k["id"])
    g, p = lint_kampanye(cfg, kk)
    for x in g:
        cetak("GALAT   : " + x)
    for x in p:
        cetak("SARAN   : " + x)
    cetak(f"Langkah berikutnya: uji-kirim {k['id']} --ke <email Anda>")


def cmd_periksa_kampanye(args):
    cfg = Konfig(args)
    k = ambil_kampanye(cfg, args.id)
    g, p = lint_kampanye(cfg, k)
    cetak(f"Kampanye #{k['id']} '{k['name']}' - status {k['status']} - subjek: {k['subject']}")
    for x in g:
        cetak("GALAT   : " + x)
    for x in p:
        cetak("SARAN   : " + x)
    if not g and not p:
        cetak("Tidak ada masalah terdeteksi.")
    cetak("Sudah diuji-kirim (isi sama persis): " + ("YA" if sudah_diuji(cfg, k) else "BELUM"))
    if g:
        raise Galat("Ada galat yang harus diperbaiki.", 6)


def cmd_daftar_kampanye(args):
    cfg = Konfig(args)
    hasil = api(cfg, "GET", "/campaigns", params={"per_page": args.batas, "order_by": "created_at", "order": "DESC",
                                                   "no_body": "true"})["data"]["results"]
    for k in hasil:
        cetak(f"#{k['id']:<4} {k['status']:<10} terkirim {k.get('sent', 0)}/{k.get('to_send', 0)}  {k['name'][:40]}")
    if not hasil:
        cetak("(belum ada kampanye)")


def muat_alamat_uji():
    try:
        with open(F_ALAMAT_UJI, encoding="utf-8") as f:
            baris = [x.strip().lower() for x in f.read().splitlines()]
    except OSError:
        return []
    return [x for x in baris if x and RE_EMAIL.match(x)][:MAKS_ALAMAT_UJI]


def cmd_simpan_alamat_uji(args):
    """Pemilik mendaftarkan alamat emailnya sendiri untuk uji-kirim. Hanya lewat terminal manusia."""
    if not sys.stdin.isatty():
        raise Galat("Perintah ini harus dijalankan pengguna sendiri di terminal. Agent tidak boleh menambah alamat uji.", 3)
    em = args.email.strip().lower()
    if not RE_EMAIL.match(em) or len(em) > 254:
        raise Galat("Alamat email tidak valid.", 2)
    ada = muat_alamat_uji()
    if em in ada:
        cetak("Alamat itu sudah terdaftar sebagai alamat uji.")
        return
    if len(ada) >= MAKS_ALAMAT_UJI:
        raise Galat(f"Maksimal {MAKS_ALAMAT_UJI} alamat uji. Hapus baris di {F_ALAMAT_UJI} bila perlu mengganti.", 2)
    jawab = input(f"Ketik 'ini email saya' untuk menyatakan {samar_email(em)} adalah email MILIK ANDA SENDIRI: ").strip().lower()
    if jawab != "ini email saya":
        raise Galat("Dibatalkan.", 2)
    os.makedirs(DIR_KONFIG, exist_ok=True)
    with open(F_ALAMAT_UJI, "w", encoding="utf-8") as f:
        f.write("\n".join(ada + [em]) + "\n")
    cetak(f"Alamat uji tersimpan ({len(ada) + 1}/{MAKS_ALAMAT_UJI}).")


def cmd_uji_kirim(args):
    cfg = Konfig(args)
    izin = muat_alamat_uji()
    if not izin:
        raise Galat("DITOLAK: belum ada alamat uji milik Anda. Pengguna menjalankan SENDIRI di terminal: "
                    "python3 scripts/listmonk.py simpan-alamat-uji --email emailanda@... "
                    "(uji-kirim hanya boleh ke alamat milik pemilik).", 6)
    em = (args.ke or "").strip().lower()
    if not em:
        if len(izin) != 1:
            raise Galat("Ada beberapa alamat uji; sebut salah satu dengan --ke.", 2)
        em = izin[0]
    if em not in izin:
        raise Galat("DITOLAK: uji-kirim hanya ke alamat uji milik pemilik yang sudah didaftarkan "
                    "(simpan-alamat-uji). Alamat lain tidak diterima.", 6)
    k = ambil_kampanye(cfg, args.id)
    if k["status"] not in ("draft", "scheduled", "paused"):
        raise Galat(f"Kampanye berstatus {k['status']}; uji-kirim hanya untuk draf/terjadwal/jeda.", 2)
    g, _ = lint_kampanye(cfg, k)
    if g:
        for x in g:
            cetak("GALAT   : " + x)
        raise Galat("DITOLAK: perbaiki galat di atas dulu; uji-kirim tidak dicatat sebagai lulus.", 6)
    ada = cari_email(cfg, em)
    if not ada:
        api(cfg, "POST", "/subscribers", data={"email": em, "name": args.nama_uji or "Uji Pemilik", "status": "enabled",
                                                "lists": [], "attribs": {"catatan": "alamat uji internal"}})
        cetak("Alamat uji dicatat sebagai pelanggan internal (tanpa list, tidak akan menerima kampanye).")
    payload = {k2: k.get(k2) for k2 in ("name", "subject", "type", "content_type", "body", "template_id", "messenger",
                                        "from_email", "headers", "altbody")}
    payload["lists"] = [l["id"] for l in k.get("lists", [])]
    payload["subscribers"] = [em]
    api(cfg, "POST", f"/campaigns/{k['id']}/test", data=payload)
    simpan_uji(cfg, k, em)
    cetak(f"Email uji dikirim ke {samar_email(em)}. Minta pengguna memeriksa kotak masuk DAN folder spam: "
          "tampilan HP, tautan, tautan berhenti berlangganan (buka tautannya, harus tampil halaman berhenti).")


def parse_waktu(teks, tz):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})[ T](\d{1,2}):(\d{2})$", teks.strip())
    if not m:
        raise Galat("Format waktu: 'YYYY-MM-DD HH:MM' (mis. 2026-10-05 09:00).", 2)
    y, mo, d, h, mi = map(int, m.groups())
    try:
        dt = datetime(y, mo, d, h, mi, tzinfo=timezone(timedelta(hours=TZ[tz])))
    except ValueError:
        raise Galat("Tanggal/jam tidak valid.", 2)
    return dt


def gerbang_kirim(cfg, k, args, aksi):
    if k["status"] not in ("draft", "scheduled", "paused"):
        raise Galat(f"Kampanye berstatus '{k['status']}'; tidak bisa {aksi}.", 2)
    g, p = lint_kampanye(cfg, k)
    total, detail = perkirakan_penerima(cfg, k)
    cetak(f"KAMPANYE #{k['id']} '{k['name']}'  subjek: {k['subject']}")
    for n, o, c in detail:
        cetak(f"  list '{n}' (opt-in {o}): {rp_angka(c)} penerima")
    cetak(f"  PERKIRAAN PENERIMA: maks. {rp_angka(total)} orang (yang sudah konfirmasi/berlaku; blokir & berhenti tidak dihitung)")
    for x in g:
        cetak("  GALAT: " + x)
    for x in p:
        cetak("  saran: " + x)
    if g:
        raise Galat("DITOLAK: perbaiki galat di atas dulu.", 6)
    diuji = sudah_diuji(cfg, k)
    cetak("  Uji-kirim ke diri sendiri: " + ("SUDAH (isi sama)" if diuji else "BELUM / isi berubah sejak uji"))
    if not diuji:
        raise Galat("DITOLAK: lakukan 'uji-kirim' ke email Anda sendiri dulu (isi harus sama persis).", 6)
    if total == 0:
        raise Galat("DITOLAK: penerima 0. Impor kontak & kirim konfirmasi opt-in dulu.", 6)
    if not args.ya or args.konfirmasi_penerima is None:
        cetak(f"BELUM {aksi.upper()}. WAJIB tanya pengguna: 'Kirim ke sekitar {rp_angka(total)} orang di list tsb? (ya/tidak)'. "
              f"Bila ya: ulangi dengan --ya --konfirmasi-penerima {total}")
        raise Galat("Menunggu konfirmasi pengguna.", 6)
    if args.konfirmasi_penerima != total:
        raise Galat(f"DITOLAK: jumlah konfirmasi ({args.konfirmasi_penerima}) tidak sama dengan perkiraan "
                    f"sekarang ({total}). Tunjukkan angka terbaru ke pengguna.", 6)
    return total


def cmd_kirim(args):
    cfg = Konfig(args)
    k = ambil_kampanye(cfg, args.id)
    total = gerbang_kirim(cfg, k, args, "dikirim")
    api(cfg, "PUT", f"/campaigns/{k['id']}/status", data={"status": "running"})
    cetak(f"Kampanye #{k['id']} mulai dikirim ke sekitar {rp_angka(total)} penerima. Pantau: statistik {k['id']}")


def cmd_jadwal(args):
    cfg = Konfig(args)
    k = ambil_kampanye(cfg, args.id)
    dt = parse_waktu(args.waktu, args.tz)
    if dt < datetime.now(timezone.utc) + timedelta(minutes=5):
        raise Galat("Waktu harus minimal 5 menit dari sekarang.", 2)
    total = gerbang_kirim(cfg, k, args, "dijadwalkan")
    upd = {f: k.get(f) for f in ("name", "subject", "type", "content_type", "body", "template_id", "messenger",
                                 "from_email", "tags", "headers", "altbody", "archive")}
    upd["lists"] = [l["id"] for l in k.get("lists", [])]
    upd["send_at"] = dt.isoformat()
    api(cfg, "PUT", f"/campaigns/{k['id']}", data=upd)
    api(cfg, "PUT", f"/campaigns/{k['id']}/status", data={"status": "scheduled"})
    cetak(f"Kampanye #{k['id']} dijadwalkan {args.waktu} {args.tz} untuk sekitar {rp_angka(total)} penerima. "
          "listmonk harus tetap menyala pada jam itu.")


def cmd_ubah_status(args, status, kata):
    cfg = Konfig(args)
    k = ambil_kampanye(cfg, args.id)
    if not args.ya:
        cetak(f"Kampanye #{k['id']} '{k['name']}' status {k['status']} akan {kata}.")
        raise Galat("Ulangi dengan --ya setelah pengguna setuju.", 6)
    if k["status"] == "scheduled" and status == "cancelled":
        status = "draft"  # listmonk: jadwal dibatalkan dengan mengembalikan ke draf
        kata = "dikembalikan ke draf (jadwal dibatalkan)"
    api(cfg, "PUT", f"/campaigns/{k['id']}/status", data={"status": status})
    cetak(f"Kampanye #{k['id']} {kata}.")


def cmd_statistik(args):
    cfg = Konfig(args)
    k = ambil_kampanye(cfg, args.id)
    sent = k.get("sent", 0) or 0
    v, c, b = k.get("views", 0) or 0, k.get("clicks", 0) or 0, k.get("bounces", 0) or 0
    cetak(f"STATISTIK KAMPANYE #{k['id']}: {k['name']}")
    cetak(f"Status: {k['status']} | subjek: {k['subject']}")
    cetak(f"Terkirim: {rp_angka(sent)} dari {rp_angka(k.get('to_send', 0) or 0)}")
    if sent:
        cetak(f"Dibuka (perkiraan): {rp_angka(v)} = {persen(v * 100 / sent)}")
        cetak(f"Klik tautan       : {rp_angka(c)} = {persen(c * 100 / sent)}")
        cetak(f"Gagal terkirim    : {rp_angka(b)} = {persen(b * 100 / sent)}")
        if v:
            cetak(f"Klik dibanding dibuka: {persen(c * 100 / v)}")
    else:
        cetak("Belum ada email terkirim, jadi belum ada angka buka/klik.")
    cetak("CATATAN: angka 'dibuka' memakai piksel gambar; bisa kurang (gambar diblokir) atau lebih "
          "(pemindai privasi mis. Apple Mail). Angka klik lebih bisa dipercaya.")
    if sent and args.tautan:
        dari = (k.get("created_at") or "2020-01-01")[:10]
        sampai = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
        try:
            ln = api(cfg, "GET", "/campaigns/analytics/links", params={"id": k["id"], "from": dari, "to": sampai})["data"]
            cetak("Tautan paling diklik:")
            for x in sorted(ln, key=lambda z: -z.get("count", 0))[:10]:
                cetak(f"  {x.get('count', 0):>5}  {str(x.get('url', ''))[:80]}")
            if not ln:
                cetak("  (belum ada klik)")
        except Galat as e:
            cetak(f"  (analitik tautan tidak tersedia: {e})")


# ---------------------------------------------------------------- CLI
def buat_parser():
    p = argparse.ArgumentParser(prog="listmonk.py", description="Pembantu newsletter listmonk (Komunitech).",
                                allow_abbrev=False)
    sub = p.add_subparsers(dest="perintah", required=True)
    _tambah = sub.add_parser

    def _tambah_ketat(*a, **k):
        k.setdefault("allow_abbrev", False)
        return _tambah(*a, **k)
    sub.add_parser = _tambah_ketat

    def umum(s):
        s.add_argument("--url", help="alamat listmonk (bawaan http://localhost:9000)")
        s.add_argument("--izinkan-jarak-jauh", action="store_true")
        s.add_argument("--token-file")
        s.add_argument("--json", action="store_true")
        return s

    s = sub.add_parser("simpan-alamat"); s.add_argument("alamat"); s.set_defaults(f=cmd_simpan_alamat)
    s = sub.add_parser("simpan-akun"); s.add_argument("--pengguna"); s.add_argument("--ya", action="store_true")
    s.add_argument("--dari-stdin", action="store_true", help=argparse.SUPPRESS); s.set_defaults(f=cmd_simpan_akun)
    s = umum(sub.add_parser("cek")); s.set_defaults(f=cmd_cek)
    s = umum(sub.add_parser("daftar-list")); s.set_defaults(f=cmd_daftar_list)
    s = umum(sub.add_parser("buat-list")); s.add_argument("--nama", required=True)
    s.add_argument("--tipe", choices=["private", "public"], default="private")
    s.add_argument("--optin", choices=["double", "single"], default="double")
    s.add_argument("--tag", action="append"); s.add_argument("--deskripsi"); s.set_defaults(f=cmd_buat_list)
    s = sub.add_parser("periksa-kontak", help="offline: periksa CSV/Excel"); s.add_argument("berkas")
    s.add_argument("--kolom-email"); s.add_argument("--kolom-nama"); s.add_argument("--keluaran")
    s.set_defaults(f=cmd_periksa_kontak)
    s = umum(sub.add_parser("impor")); s.add_argument("berkas"); s.add_argument("--list", required=True)
    s.add_argument("--sumber-persetujuan"); s.add_argument("--saya-punya-izin", action="store_true")
    s.add_argument("--pengguna-konfirmasi-setuju", help="jawaban pengguna apa adanya, untuk sumber yang tak dikenal")
    s.add_argument("--sudah-terkonfirmasi", action="store_true")
    s.add_argument("--kolom-email"); s.add_argument("--kolom-nama"); s.add_argument("--ya", action="store_true")
    s.set_defaults(f=cmd_impor)
    s = umum(sub.add_parser("kirim-optin")); s.add_argument("--list", required=True)
    s.add_argument("--ya", action="store_true"); s.add_argument("--konfirmasi-penerima", type=int)
    s.set_defaults(f=cmd_kirim_optin)
    s = umum(sub.add_parser("daftar-pelanggan")); s.add_argument("--list", required=True)
    s.add_argument("--contoh", type=int, default=0); s.set_defaults(f=cmd_daftar_pelanggan)
    s = umum(sub.add_parser("hapus-pelanggan")); s.add_argument("--email", required=True)
    s.add_argument("--ya", action="store_true"); s.set_defaults(f=cmd_hapus_pelanggan)
    s = umum(sub.add_parser("template")); s.set_defaults(f=cmd_daftar_template)
    s = umum(sub.add_parser("buat-kampanye")); s.add_argument("--nama", required=True)
    s.add_argument("--subjek", required=True); s.add_argument("--list", action="append", required=True)
    s.add_argument("--isi-file", required=True); s.add_argument("--tipe", choices=["html", "markdown", "richtext"], default="html")
    s.add_argument("--template", type=int, default=1); s.add_argument("--dari"); s.add_argument("--tag", action="append")
    s.set_defaults(f=cmd_buat_kampanye)
    s = umum(sub.add_parser("periksa-kampanye")); s.add_argument("id"); s.set_defaults(f=cmd_periksa_kampanye)
    s = umum(sub.add_parser("daftar-kampanye")); s.add_argument("--batas", type=int, default=10); s.set_defaults(f=cmd_daftar_kampanye)
    s = sub.add_parser("simpan-alamat-uji"); s.add_argument("--email", required=True); s.set_defaults(f=cmd_simpan_alamat_uji)
    s = umum(sub.add_parser("uji-kirim")); s.add_argument("id"); s.add_argument("--ke")
    s.add_argument("--nama-uji"); s.set_defaults(f=cmd_uji_kirim)
    for nama, fn in (("kirim", cmd_kirim), ("jadwal", cmd_jadwal)):
        s = umum(sub.add_parser(nama)); s.add_argument("id")
        if nama == "jadwal":
            s.add_argument("--waktu", required=True); s.add_argument("--tz", choices=list(TZ), default="WIB")
        s.add_argument("--ya", action="store_true"); s.add_argument("--konfirmasi-penerima", type=int)
        s.set_defaults(f=fn)
    for nama, st, kata in (("jeda", "paused", "dijeda"), ("batalkan", "cancelled", "dibatalkan")):
        s = umum(sub.add_parser(nama)); s.add_argument("id"); s.add_argument("--ya", action="store_true")
        s.set_defaults(f=(lambda a, st=st, kata=kata: cmd_ubah_status(a, st, kata)))
    s = umum(sub.add_parser("statistik")); s.add_argument("id"); s.add_argument("--tautan", action="store_true")
    s.set_defaults(f=cmd_statistik)
    return p


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        args.f(args)
    except Galat as e:
        print(("GALAT: " if e.kode != 6 else "") + str(e), file=sys.stderr)
        return e.kode
    except BrokenPipeError:
        return 0
    except KeyboardInterrupt:
        print("Dibatalkan.", file=sys.stderr)
        return 2
    except Exception as e:  # jangan tampilkan Traceback mentah (bisa memuat data); sebut jenis galatnya saja
        print(f"GALAT tak terduga ({type(e).__name__}). Periksa berkas/alamat, atau kerjakan manual lewat layar listmonk.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
