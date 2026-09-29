#!/usr/bin/env python3
"""inventree-gudang (Komunitech) - asisten gudang/stok InvenTree untuk usaha Indonesia.

Memanggil REST API resmi InvenTree (server milik pengguna sendiri) dengan token API
(header 'Authorization: Token inv-...'). Python standar saja, tanpa paket tambahan.
Menolak alamat selain komputer/jaringan sendiri kecuali --izinkan-jarak-jauh.

Perintah baca:
  simpan-kunci      simpan token API ke file lokal (dibaca tersembunyi, tidak pernah dicetak)
  cek               cek server InvenTree, versi, dan hak akses token
  cari              cari barang (nama / kode IPN / deskripsi)
  stok              stok satu barang per lokasi & batch
  lokasi            daftar lokasi gudang, atau isi satu lokasi
  stok-menipis      barang di bawah stok minimum + saran jumlah pesan
  po-terbuka        pesanan pembelian (PO) yang belum diterima penuh
  bom               daftar bahan (BOM) satu produk + maksimal bisa diproduksi
  produksi-ringkas  kebutuhan bahan untuk N unit produk, atau daftar perintah produksi terbuka
  ekspor-csv        ekspor stok ke CSV (per item/batch atau per barang)
  laporan-harian    ringkasan harian (stok menipis + PO terbuka + produksi) untuk jadwal
  opname-draf       buat lembar hitung fisik (CSV) untuk satu lokasi
Perintah tulis (selalu pratinjau dulu; menulis hanya dengan --ya):
  opname            baca lembar hitung fisik yang sudah diisi -> selisih -> simpan hasil hitung
  terima-barang     terima barang dari PO ke gudang (dengan kode batch)

Windows: pakai `python` atau `py` sebagai ganti `python3`. Tambah --json untuk hasil terstruktur.
"""
import argparse
import csv
import datetime as dt
import getpass
import io
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation, ROUND_FLOOR

VERSI = "1.0.1"
INVENTREE_TERUJI = ("1.5.6",)
API_TERUJI = 530
KUNCI_DEFAULT = os.path.join(os.path.expanduser("~"), ".komunitech", "inventree-kunci.txt")
URL_DEFAULT = "http://localhost"
BATAS_HALAMAN = 100
MAKS_HALAMAN = 50

K_INPUT, K_FILE, K_KONEKSI, K_AUTH, K_TULIS, K_GANDA, K_TAKPASTI = 2, 3, 4, 5, 6, 7, 8

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
TZ_OFFSET = {"WIB": 7, "WITA": 8, "WIT": 9}
STATUS_PO = {10: "Belum dikirim ke pemasok", 20: "Sudah dipesan", 25: "Ditahan", 30: "Selesai",
             40: "Batal", 50: "Hilang", 60: "Dikembalikan"}
STATUS_PRODUKSI = {10: "Menunggu", 20: "Sedang produksi", 25: "Ditahan", 30: "Batal", 40: "Selesai"}


class Gagal(Exception):
    def __init__(self, pesan, kode=K_INPUT):
        super().__init__(pesan)
        self.kode = kode


# ============================================================ angka & tanggal


def ke_desimal(nilai):
    """Angka dari API (float/str) -> Decimal tanpa galat biner (lewat str)."""
    if nilai is None or nilai == "":
        return Decimal(0)
    if isinstance(nilai, Decimal):
        return nilai
    try:
        return Decimal(str(nilai))
    except InvalidOperation:
        return Decimal(0)


def baca_angka_pengguna(teks):
    """'12,5' / '1.200' / '1.200,5' / '12.5' / '1200' -> Decimal. Melempar ValueError bila tidak jelas."""
    t = str(teks).strip().replace(" ", "")
    if not t:
        raise ValueError("kosong")
    if not re.fullmatch(r"-?[\d.,]+", t):
        raise ValueError(f"bukan angka: {teks!r}")
    if "," in t and "." in t:
        # gaya Indonesia 1.200,5 (titik ribuan, koma desimal)
        if t.rfind(",") > t.rfind("."):
            t = t.replace(".", "").replace(",", ".")
        else:  # gaya Inggris 1,200.5
            t = t.replace(",", "")
    elif "," in t:
        t = t.replace(",", ".")
    elif t.count(".") == 1 and re.fullmatch(r"-?\d{1,3}\.\d{3}", t):
        # '1.200' = seribu dua ratus (titik ribuan gaya Indonesia). '1.5' tetap satu koma lima.
        t = t.replace(".", "")
    elif t.count(".") > 1:
        t = t.replace(".", "")
    try:
        return Decimal(t)
    except InvalidOperation:
        raise ValueError(f"bukan angka: {teks!r}")


def dec(nilai):
    """Decimal -> string angka mesin tanpa nol berlebih ('90', '12.5') untuk --json. None tetap None."""
    if nilai is None:
        return None
    return f"{ke_desimal(nilai).normalize():f}"


def fmt(nilai):
    """Decimal -> '1.200' / '12,5' / '0,05' (gaya Indonesia, tanpa nol di belakang)."""
    d = ke_desimal(nilai)
    if d == d.to_integral_value():
        s = f"{int(d):,}".replace(",", ".")
        return s
    d = d.normalize()
    bulat, _, pecahan = f"{d:f}".partition(".")
    neg = bulat.startswith("-")
    bulat = f"{abs(int(bulat)):,}".replace(",", ".")
    return ("-" if neg else "") + bulat + "," + pecahan


def fmt_rp(nilai):
    d = ke_desimal(nilai).quantize(Decimal(1))
    return "Rp" + f"{int(d):,}".replace(",", ".")


def zona(tz_nama):
    return dt.timezone(dt.timedelta(hours=TZ_OFFSET.get(tz_nama, 7)))


def hari_ini(tz_nama):
    return dt.datetime.now(zona(tz_nama)).date()


def tgl_panjang(tanggal):
    return f"{HARI[tanggal.weekday()]}, {tanggal.day} {BULAN[tanggal.month - 1]} {tanggal.year}"


def tgl_pendek(teks):
    if not teks:
        return "-"
    try:
        d = dt.date.fromisoformat(str(teks)[:10])
    except ValueError:
        return str(teks)
    return f"{d.day} {BULAN[d.month - 1][:3]} {d.year}"


def satuan(part_detail):
    u = (part_detail or {}).get("units") or ""
    return f" {u}" if u else ""


# ============================================================ token & konfigurasi


def cek_izin_file(path):
    if os.name == "nt":
        return
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        return
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        sys.stderr.write(f"PERINGATAN: file kunci {path} bisa dibaca pengguna lain. Jalankan: chmod 600 {path}\n")


def token_wajar(token):
    return token.startswith("inv-") or re.fullmatch(r"[0-9a-f]{40}", token) is not None


def simpan_kunci(args):
    path = os.path.abspath(os.path.expanduser(args.kunci_file)) if args.kunci_file else KUNCI_DEFAULT
    if os.path.exists(path) and not args.ya:
        raise Gagal(
            f"File kunci sudah ada: {path}\nUntuk mengganti token lama, ulangi dengan --ya. Untuk menyimpan "
            f"token KEDUA (mis. token akun baca-tulis terpisah), pakai --kunci-file <path lain>.", K_FILE)
    sys.stderr.write(f"Token akan disimpan di: {path}\n")
    token = getpass.getpass("Tempel token API InvenTree (tidak terlihat), lalu Enter: ").strip()
    if not token:
        raise Gagal("Token kosong, tidak disimpan.", K_INPUT)
    if re.search(r"\s", token):
        raise Gagal("Token berisi spasi/baris baru - kemungkinan tersalin rusak. Salin ulang.", K_INPUT)
    if not token_wajar(token):
        raise Gagal("Token InvenTree seharusnya diawali 'inv-' (InvenTree 1.x). Salin ulang dari halaman "
                    "profil pengguna > Access Tokens (tampil hanya sekali saat dibuat).", K_INPUT)
    folder = os.path.dirname(path)
    baru = not os.path.isdir(folder)
    os.makedirs(folder, mode=0o700, exist_ok=True)
    if baru:
        try:
            os.chmod(folder, 0o700)
        except OSError:
            pass
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(token + "\n")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    print(f"Token tersimpan di {path} (izin 600).")
    return 0


def _baca_file_token(path, sumber):
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.isfile(path):
        raise Gagal(f"File kunci ({sumber}) tidak ditemukan: {path}. Jalankan dulu "
                    f"'python3 inventree.py simpan-kunci' (lihat docs/panduan-inventree.md bagian 6).", K_FILE)
    cek_izin_file(path)
    with open(path, encoding="utf-8") as f:
        token = f.read().strip()
    if not token:
        raise Gagal(f"File kunci ({sumber}) kosong: {path}.", K_FILE)
    if re.search(r"\s", token):
        raise Gagal(f"File kunci ({sumber}) berisi spasi/baris ganda - simpan ulang dengan 'simpan-kunci'.", K_FILE)
    return token


def ambil_token(args):
    if args.kunci_file:
        if os.environ.get("INVENTREE_API_TOKEN"):
            sys.stderr.write("PERINGATAN: --kunci-file dipakai; ENV INVENTREE_API_TOKEN DIABAIKAN.\n")
        return _baca_file_token(args.kunci_file, "--kunci-file")
    if os.environ.get("INVENTREE_API_TOKEN"):
        return os.environ["INVENTREE_API_TOKEN"].strip()
    if os.environ.get("INVENTREE_API_TOKEN_FILE"):
        return _baca_file_token(os.environ["INVENTREE_API_TOKEN_FILE"], "ENV INVENTREE_API_TOKEN_FILE")
    return _baca_file_token(KUNCI_DEFAULT, "file kunci default")


def samarkan(token):
    if len(token) <= 10:
        return "****"
    return token[:6] + "****" + token[-4:]


# ============================================================ HTTP ke InvenTree


_SUDAH_DIPERINGATKAN = set()
_POLA_LAN = r"^(192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.)"


def host_lokal_atau_lan(url):
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return (host in ("127.0.0.1", "localhost", "::1") or host.endswith(".localhost")
            or re.match(_POLA_LAN, host) is not None)


def periksa_url(url, izinkan_jarak_jauh):
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise Gagal(f"URL InvenTree tidak valid: {url!r}. Contoh: http://localhost atau http://127.0.0.1:8000", K_INPUT)
    host = u.hostname.lower()
    if host in ("127.0.0.1", "localhost", "::1") or host.endswith(".localhost"):
        return
    kantor = re.match(_POLA_LAN, host)
    if not izinkan_jarak_jauh:
        raise Gagal(
            f"Alamat InvenTree '{url}' bukan komputer ini (localhost/127.0.0.1). Jangan buka InvenTree ke "
            f"internet (docs/panduan-inventree.md bagian 4). Bila ini memang server Anda sendiri di jaringan "
            f"kantor/VPS milik sendiri, tegaskan dengan --izinkan-jarak-jauh.", K_INPUT)
    if not kantor and u.scheme != "https":
        raise Gagal(f"Alamat internet '{url}' wajib HTTPS. InvenTree tidak boleh diakses lewat http biasa di "
                    f"internet terbuka (token ikut terkirim tanpa enkripsi).", K_INPUT)
    if kantor and u.scheme != "https" and url not in _SUDAH_DIPERINGATKAN:
        _SUDAH_DIPERINGATKAN.add(url)
        sys.stderr.write(f"PERINGATAN: {url} memakai http biasa di jaringan kantor, bukan komputer ini sendiri.\n")


class _TolakPengalihan(urllib.request.HTTPRedirectHandler):
    """Jangan pernah mengikuti redirect: header Authorization (token) bisa terbawa ke alamat lain
    yang belum lolos periksa_url, atau HTTPS turun ke HTTP."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Gagal(
            f"InvenTree di {req.full_url.split('/api')[0]} mengalihkan (HTTP {code}) ke {newurl!r}. Demi keamanan "
            f"token, skill TIDAK mengikuti pengalihan. Pakai alamat tujuan akhir yang benar sebagai --url / ENV "
            f"INVENTREE_API_HOST (mis. versi https:// atau port yang benar; panduan bagian 11).", K_KONEKSI)


def buat_opener(url):
    """Alamat komputer ini / jaringan kantor: proxy dari ENV (HTTP_PROXY/HTTPS_PROXY) DIABAIKAN supaya token
    tidak pernah lewat proxy. Alamat internet (hanya HTTPS + --izinkan-jarak-jauh) memakai setelan proxy sistem."""
    proxy = urllib.request.ProxyHandler({}) if host_lokal_atau_lan(url) else urllib.request.ProxyHandler()
    return urllib.request.build_opener(proxy, _TolakPengalihan())


def panggil(method, path, args, token=None, body=None, tulis=False):
    periksa_url(args.url, args.izinkan_jarak_jauh)
    url = args.url.rstrip("/") + "/api" + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/json")
    if token:
        req.add_header("Authorization", "Token " + token)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with buat_opener(url).open(req, timeout=args.timeout) as resp:
            mentah = resp.read()
            return json.loads(mentah) if mentah else None
    except urllib.error.HTTPError as e:
        mentah = e.read() or b""
        try:
            j = json.loads(mentah)
        except (ValueError, TypeError):
            j = None
        pesan = ""
        if isinstance(j, dict):
            pesan = j.get("detail") or json.dumps(j, ensure_ascii=False)[:400]
        elif j is not None:
            pesan = json.dumps(j, ensure_ascii=False)[:400]
        if e.code == 401:
            raise Gagal("401 dari InvenTree: token salah, kedaluwarsa, atau sudah dicabut "
                        f"(pesan server: {pesan or '-'}). Buat token baru di profil pengguna > Access Tokens, "
                        "lalu 'simpan-kunci --ya'. Lihat docs/panduan-inventree.md bagian 6.", K_AUTH)
        if e.code == 403:
            raise Gagal("403 dari InvenTree: akun pemilik token TIDAK PUNYA HAK untuk aksi ini "
                        f"({method} {path}; pesan server: {pesan or '-'}). Atur grup/peran akun itu di "
                        "Admin Center > Users/Groups (panduan bagian 6). Jangan mencoba lewat jalan lain.", K_AUTH)
        if e.code == 404:
            raise Gagal(f"404: tidak ditemukan di InvenTree ({path}). Periksa id/kode, atau alamat server "
                        f"salah (bukan InvenTree?). {pesan}", K_KONEKSI)
        if e.code == 400:
            raise Gagal(f"InvenTree menolak data (400): {pesan or mentah[:300]!r}", K_TULIS if tulis else K_INPUT)
        if 500 <= e.code < 600:
            if tulis:
                raise Gagal(f"InvenTree membalas galat server ({e.code}) saat MENULIS. Data MUNGKIN sudah masuk "
                            f"sebagian. JANGAN ulangi otomatis - cek dulu di layar InvenTree.", K_TAKPASTI)
            saran = (" (502/503/504 biasanya: InvenTree sedang menyala/mati atau kotak server mati - cek "
                     "'docker compose ps' di folder InvenTree)") if e.code in (502, 503, 504) else ""
            raise Gagal(f"InvenTree membalas galat server ({e.code}){saran}. Coba lagi sebentar; bila terus, cek log "
                        f"InvenTree.", K_KONEKSI)
        raise Gagal(f"InvenTree membalas kode {e.code}: {pesan or mentah[:200]!r}", K_KONEKSI)
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        if tulis:
            raise Gagal(f"Koneksi ke InvenTree terputus/timeout saat MENULIS ({e}). Hasilnya TIDAK PASTI - data "
                        f"MUNGKIN sudah tersimpan. JANGAN ulangi otomatis; buka InvenTree dan cek riwayat stok "
                        f"dulu.", K_TAKPASTI)
        raise Gagal(f"Tidak bisa menghubungi InvenTree di {args.url} ({e}). Pastikan InvenTree menyala "
                    f"(panduan bagian 3/7) dan alamatnya benar (ENV INVENTREE_API_HOST atau --url).", K_KONEKSI)
    except ValueError:
        raise Gagal("Jawaban InvenTree tidak bisa dibaca (bukan JSON - alamat salah atau terpotong?).",
                    K_TAKPASTI if tulis else K_KONEKSI)


def ambil_semua(path, args, token, query=None):
    """GET daftar dengan limit/offset. Menerima jawaban {count,results} maupun list biasa."""
    hasil, offset = [], 0
    for _ in range(MAKS_HALAMAN):
        q = dict(query or {})
        q["limit"], q["offset"] = BATAS_HALAMAN, offset
        data = panggil("GET", path + "?" + urllib.parse.urlencode(q), args, token)
        if isinstance(data, list):
            return hasil + data
        if not isinstance(data, dict):
            break
        baris = data.get("results") or []
        hasil.extend(baris)
        offset += len(baris)
        if not baris or offset >= int(data.get("count") or 0):
            break
    return hasil


# ============================================================ pencarian barang & lokasi


def ringkas_barang(p):
    kode = p.get("IPN") or f"id {p['pk']}"
    return f"{p['name']} [{kode}]"


def cari_barang(args, token, sebutan, syarat=None):
    """Nama/kode/id -> satu part. Kode IPN persis & nama persis menang. Ambigu -> Gagal dengan pilihan."""
    s = str(sebutan).strip()
    if not s:
        raise Gagal("Nama/kode barang kosong.", K_INPUT)
    if s.startswith("#") and s[1:].isdigit():
        return panggil("GET", f"/part/{int(s[1:])}/", args, token)
    q = {"search": s, "active": "true"}
    q.update(syarat or {})
    kandidat = ambil_semua("/part/", args, token, q)
    if not kandidat:
        raise Gagal(f"Barang '{s}' tidak ditemukan. Coba kata lain, atau jalankan 'cari <kata>'.", K_INPUT)
    kecil = s.lower()
    persis = [p for p in kandidat if (p.get("IPN") or "").lower() == kecil] or \
             [p for p in kandidat if p["name"].lower() == kecil]
    if len(persis) == 1:
        return persis[0]
    if len(kandidat) == 1:
        return kandidat[0]
    opsi = "; ".join(f"{ringkas_barang(p)} (#{p['pk']})" for p in kandidat[:10])
    lebih = f" (+{len(kandidat) - 10} lagi)" if len(kandidat) > 10 else ""
    raise Gagal(f"'{s}' cocok dengan {len(kandidat)} barang: {opsi}{lebih}. Sebutkan kode (IPN) atau #id.", K_GANDA)


def cari_lokasi(args, token, sebutan):
    s = str(sebutan).strip()
    if s.startswith("#") and s[1:].isdigit():
        return panggil("GET", f"/stock/location/{int(s[1:])}/", args, token)
    semua = ambil_semua("/stock/location/", args, token)
    kecil = s.lower()
    persis = [l for l in semua if l["name"].lower() == kecil or (l.get("pathstring") or "").lower() == kecil]
    if len(persis) == 1:
        return persis[0]
    cocok = persis or [l for l in semua if kecil in (l.get("pathstring") or l["name"]).lower()]
    if len(cocok) == 1:
        return cocok[0]
    if not cocok:
        ada = ", ".join(l.get("pathstring") or l["name"] for l in semua) or "(belum ada lokasi)"
        raise Gagal(f"Lokasi '{s}' tidak ditemukan. Lokasi yang ada: {ada}.", K_INPUT)
    opsi = "; ".join(f"{l.get('pathstring')} (#{l['pk']})" for l in cocok)
    raise Gagal(f"Lokasi '{s}' cocok lebih dari satu: {opsi}. Sebutkan jalur lengkap atau #id.", K_GANDA)


def nama_lokasi(item):
    ld = item.get("location_detail") or {}
    return ld.get("pathstring") or ld.get("name") or ("(tanpa lokasi)" if not item.get("location") else f"#{item['location']}")


# ============================================================ perintah baca


def cmd_cek(args):
    teks = ["CEK INVENTREE", f"Alamat: {args.url}"]
    try:
        info = panggil("GET", "/", args) or {}
    except Gagal as e:
        teks.append(f"TIDAK BISA DIHUBUNGI: {e}")
        cetak({"teks": "\n".join(teks), "terhubung": False}, args)
        return e.kode
    if info.get("server") != "InvenTree":
        raise Gagal(f"Alamat {args.url} menjawab, tapi bukan InvenTree. Periksa alamat/port.", K_KONEKSI)
    versi, api = info.get("version", "?"), info.get("apiVersion")
    catatan = "" if versi in INVENTREE_TERUJI else " (belum diuji Komunitech - cocokkan angka penting di layar InvenTree)"
    teks.append(f"Versi server: {versi} (API {api}){catatan}")
    token = ambil_token(args)
    teks.append(f"Token: {samarkan(token)}")
    me = panggil("GET", "/user/me/", args, token) or {}
    teks.append(f"Akun: {me.get('username', '?')}" + (" (SUPERUSER - sebaiknya pakai akun khusus berhak terbatas)"
                                                      if me.get("is_superuser") else ""))
    peran = (panggil("GET", "/user/roles/", args, token) or {}).get("roles") or {}
    perlu = [("part", "view", "lihat barang"), ("stock", "view", "lihat stok"),
             ("stock_location", "view", "lihat lokasi"), ("purchase_order", "view", "lihat PO"),
             ("build", "view", "lihat produksi"), ("bom", "view", "lihat BOM"),
             ("stock", "change", "opname (tulis)"), ("purchase_order", "change", "terima barang (tulis)")]
    hak = {}
    for role, aksi, label in perlu:
        ok = aksi in (peran.get(role) or [])
        hak[f"{role}:{aksi}"] = ok
        teks.append(f"- {label}: {'YA' if ok else 'tidak'}")
    baca_ok = all(hak[f"{r}:view"] for r in ("part", "stock", "stock_location"))
    teks.append("Hak baca dasar: OK" if baca_ok else "Hak baca dasar: KURANG (atur grup akun, panduan bagian 6)")
    if hak["stock:change"] or hak["purchase_order:change"]:
        teks.append("Catatan: token ini BISA MENULIS. Untuk jadwal otomatis pakai akun baca-saja.")
    cetak({"teks": "\n".join(teks), "terhubung": True, "versi": versi, "api": api, "akun": me.get("username"),
           "hak": hak}, args)
    return 0 if baca_ok else K_AUTH


def cmd_cari(args, token):
    hasil = ambil_semua("/part/", args, token, {"search": args.kata, "active": "true"})
    teks = [f"HASIL CARI BARANG: {args.kata!r}", f"Jumlah: {len(hasil)}"]
    data = []
    for p in hasil[:args.maks]:
        stok = ke_desimal(p.get("total_in_stock", p.get("in_stock")))
        mn = ke_desimal(p.get("minimum_stock"))
        tanda = " - DI BAWAH MINIMUM" if mn > 0 and stok < mn else ""
        teks.append(f"- {ringkas_barang(p)} | {p.get('category_name') or '-'} | stok {fmt(stok)}{satuan(p)}"
                    f"{f' (min {fmt(mn)})' if mn > 0 else ''}{tanda}")
        data.append({"id": p["pk"], "kode": p.get("IPN"), "nama": p["name"], "kategori": p.get("category_name"),
                     "stok": dec(stok), "minimum": dec(mn), "satuan": p.get("units") or ""})
    if len(hasil) > args.maks:
        teks.append(f"(+{len(hasil) - args.maks} lagi; persempit kata kunci atau --maks)")
    if not hasil:
        teks.append("(tidak ada barang yang cocok)")
    cetak({"teks": "\n".join(teks), "jumlah": len(hasil), "barang": data}, args)
    return 0


def item_stok(args, token, query):
    q = {"in_stock": "true", "location_detail": "true", "part_detail": "true"}
    q.update(query)
    return ambil_semua("/stock/", args, token, q)


def cmd_stok(args, token):
    p = cari_barang(args, token, args.barang)
    q = {"part": p["pk"]}
    judul_lok = ""
    if args.lokasi:
        lok = cari_lokasi(args, token, args.lokasi)
        q.update({"location": lok["pk"], "cascade": "true"})
        judul_lok = f" di {lok.get('pathstring') or lok['name']}"
    items = item_stok(args, token, q)
    items.sort(key=lambda i: (nama_lokasi(i), i.get("batch") or ""))
    total = sum((ke_desimal(i["quantity"]) for i in items), Decimal(0))
    teralokasi = sum((ke_desimal(i.get("allocated")) for i in items), Decimal(0))
    u = satuan(p)
    teks = [f"STOK {ringkas_barang(p)}{judul_lok}", f"Total: {fmt(total)}{u} ({len(items)} item stok)"]
    if teralokasi > 0:
        teks.append(f"Sudah dialokasikan (produksi/penjualan): {fmt(teralokasi)}{u}; bebas: {fmt(total - teralokasi)}{u}")
    mn = ke_desimal(p.get("minimum_stock"))
    if mn > 0 and not args.lokasi:
        teks.append(f"Minimum: {fmt(mn)}{u}" + (" - DI BAWAH MINIMUM" if total < mn else ""))
    per_lok = {}
    for i in items:
        per_lok.setdefault(nama_lokasi(i), []).append(i)
    for lok, daftar in per_lok.items():
        sub = sum((ke_desimal(i["quantity"]) for i in daftar), Decimal(0))
        teks.append(f"\n{lok}: {fmt(sub)}{u}")
        for i in daftar:
            ket = [f"batch {i['batch']}" if i.get("batch") else "tanpa batch"]
            if i.get("serial"):
                ket.append(f"SN {i['serial']}")
            if i.get("expiry_date"):
                ket.append(f"kedaluwarsa {tgl_pendek(i['expiry_date'])}" + (" (SUDAH LEWAT)" if i.get("expired") else ""))
            if i.get("status_text") and i.get("status") != 10:
                ket.append(f"status {i['status_text']}")
            teks.append(f"  - {fmt(i['quantity'])}{u} ({'; '.join(ket)}) [id stok {i['pk']}]")
    if not items:
        teks.append("(tidak ada stok tercatat)")
    cetak({"teks": "\n".join(teks), "barang": {"id": p["pk"], "kode": p.get("IPN"), "nama": p["name"]},
           "total": dec(total), "item": [{"id": i["pk"], "lokasi": nama_lokasi(i), "batch": i.get("batch"),
                                          "jumlah": dec(ke_desimal(i["quantity"]))} for i in items]}, args)
    return 0


def cmd_lokasi(args, token):
    if not args.nama:
        semua = ambil_semua("/stock/location/", args, token)
        semua.sort(key=lambda l: l.get("pathstring") or l["name"])
        teks = ["LOKASI GUDANG (jumlah item stok termasuk sub-lokasi)"] + [f"- {l.get('pathstring') or l['name']} ({l.get('items', 0)} item stok) [#{l['pk']}]"
                                    for l in semua]
        if not semua:
            teks.append("(belum ada lokasi; buat di InvenTree: Stock > Locations)")
        cetak({"teks": "\n".join(teks), "lokasi": [{"id": l["pk"], "jalur": l.get("pathstring")} for l in semua]}, args)
        return 0
    lok = cari_lokasi(args, token, args.nama)
    items = item_stok(args, token, {"location": lok["pk"], "cascade": "true"})
    items.sort(key=lambda i: ((i.get("part_detail") or {}).get("name", ""), i.get("batch") or ""))
    teks = [f"ISI LOKASI {lok.get('pathstring') or lok['name']} (termasuk sub-lokasi)", f"Jumlah item stok: {len(items)}"]
    for i in items:
        pd = i.get("part_detail") or {}
        teks.append(f"- {pd.get('name', '?')} [{pd.get('IPN') or '-'}]: {fmt(i['quantity'])}{satuan(pd)}"
                    f" ({'batch ' + i['batch'] if i.get('batch') else 'tanpa batch'}; {nama_lokasi(i)})")
    if not items:
        teks.append("(kosong)")
    cetak({"teks": "\n".join(teks), "lokasi": lok.get("pathstring"), "jumlah": len(items)}, args)
    return 0


def data_stok_menipis(args, token):
    daftar = ambil_semua("/part/", args, token, {"low_stock": "true", "active": "true"})
    hasil = []
    for p in daftar:
        stok = ke_desimal(p.get("total_in_stock", p.get("in_stock")))
        mn = ke_desimal(p.get("minimum_stock"))
        dipesan = ke_desimal(p.get("ordering"))
        # 'building' = output yang sedang dikerjakan; 'scheduled_to_build' = sisa perintah produksi terbuka
        # (termasuk yang masih Menunggu). Pakai yang lebih besar supaya BO Pending ikut dihitung.
        diproduksi = max(ke_desimal(p.get("building")), ke_desimal(p.get("scheduled_to_build")))
        dibutuhkan = ke_desimal(p.get("required_for_build_orders")) + ke_desimal(p.get("required_for_sales_orders"))
        kurang = mn - stok
        saran = mn - stok - dipesan - diproduksi
        hasil.append({"id": p["pk"], "kode": p.get("IPN"), "nama": p["name"], "kategori": p.get("category_name") or "-",
                      "satuan": p.get("units") or "", "stok": stok, "minimum": mn, "kurang": kurang,
                      "dipesan": dipesan, "diproduksi": diproduksi, "dibutuhkan": dibutuhkan, "saran": saran if saran > 0 else Decimal(0),
                      "rakitan": bool(p.get("assembly"))})
    hasil.sort(key=lambda r: (r["kategori"], -(r["kurang"] / r["minimum"] if r["minimum"] else 0)))
    return hasil


def teks_stok_menipis(hasil):
    teks = [f"STOK MENIPIS (di bawah minimum): {len(hasil)} barang"]
    kat = None
    for r in hasil:
        if r["kategori"] != kat:
            kat = r["kategori"]
            teks.append(f"\n{kat}:")
        u = f" {r['satuan']}" if r["satuan"] else ""
        baris = f"- {r['nama']} [{r['kode'] or '-'}]: stok {fmt(r['stok'])}{u}, minimum {fmt(r['minimum'])}{u}, kurang {fmt(r['kurang'])}{u}"
        ket = []
        if r["dipesan"] > 0:
            ket.append(f"sedang dipesan {fmt(r['dipesan'])}{u}")
        if r["diproduksi"] > 0:
            ket.append(f"dalam perintah produksi terbuka {fmt(r['diproduksi'])}{u}")
        if r["dibutuhkan"] > 0:
            ket.append(f"dibutuhkan produksi/penjualan terbuka {fmt(r['dibutuhkan'])}{u}")
        if r["saran"] > 0:
            ket.append(f"perlu {'diproduksi' if r['rakitan'] else 'dipesan'} lagi min. {fmt(r['saran'])}{u}")
        else:
            ket.append("kekurangan terhadap minimum sudah tertutup pesanan/produksi berjalan")
        teks.append(baris + " (" + "; ".join(ket) + ")")
    if not hasil:
        teks.append("(semua barang yang punya stok minimum masih aman)")
    return teks


def cmd_stok_menipis(args, token):
    hasil = data_stok_menipis(args, token)
    teks = teks_stok_menipis(hasil)
    teks.append("\nCatatan: hanya barang yang diberi 'Minimum Stock' di InvenTree yang diperiksa. 'Perlu dipesan' = "
                "minimum - stok - sedang dipesan - dalam perintah produksi terbuka (kebutuhan produksi/penjualan terbuka ditampilkan terpisah, tidak ditambahkan).")
    cetak({"teks": "\n".join(teks), "jumlah": len(hasil),
           "barang": [{k: (dec(v) if isinstance(v, Decimal) else v) for k, v in r.items()} for r in hasil]}, args)
    return 0


def data_po_terbuka(args, token, pemasok=None):
    q = {"outstanding": "true", "supplier_detail": "true"}
    daftar = ambil_semua("/order/po/", args, token, q)
    if pemasok:
        daftar = [o for o in daftar if pemasok.lower() in (o.get("supplier_name") or "").lower()]
    daftar.sort(key=lambda o: (o.get("target_date") or "9999", o.get("reference") or ""))
    return daftar


def baris_po(args, token, po_pk):
    return ambil_semua("/order/po-line/", args, token, {"order": po_pk, "part_detail": "true"})


def cmd_po_terbuka(args, token):
    daftar = data_po_terbuka(args, token, args.pemasok)
    teks = [f"PO TERBUKA (belum diterima penuh): {len(daftar)}"]
    data = []
    for o in daftar:
        telat = " - TERLAMBAT" if o.get("overdue") else ""
        teks.append(f"\n{o['reference']} | {o.get('supplier_name') or '-'} | {STATUS_PO.get(o.get('status'), o.get('status_text'))}"
                    f" | target {tgl_pendek(o.get('target_date'))}{telat} | {o.get('completed_lines', 0)}/{o.get('line_items', 0)} baris lengkap")
        sisa_list = []
        for ln in baris_po(args, token, o["pk"]):
            pesan, terima = ke_desimal(ln["quantity"]), ke_desimal(ln.get("received"))
            sisa = pesan - terima
            if sisa <= 0:
                continue
            pd = ln.get("part_detail") or {}
            kemasan = ke_desimal((ln.get("supplier_part_detail") or {}).get("pack_quantity_native") or 1)
            if kemasan == 1:
                ket_sat = satuan(pd)
            else:
                ket_sat = (f" kemasan pemasok (1 kemasan = {fmt(kemasan)}{satuan(pd)}; sisa = "
                           f"{fmt(sisa * kemasan)}{satuan(pd)})")
            teks.append(f"  - {pd.get('name', ln.get('internal_part_name', '?'))} [{pd.get('IPN') or '-'}]: dipesan {fmt(pesan)},"
                        f" diterima {fmt(terima)}, sisa {fmt(sisa)}{ket_sat}")
            sisa_list.append({"baris": ln["pk"], "kode": pd.get("IPN"), "sisa": dec(sisa)})
        data.append({"id": o["pk"], "nomor": o["reference"], "pemasok": o.get("supplier_name"),
                     "status": o.get("status"), "target": o.get("target_date"), "terlambat": bool(o.get("overdue")),
                     "total": o.get("total_price"), "sisa": sisa_list})
    if not daftar:
        teks.append("(tidak ada PO terbuka)")
    cetak({"teks": "\n".join(teks), "po": data}, args)
    return 0


def hitung_bom(args, token, part, jumlah=None):
    baris = ambil_semua("/bom/", args, token, {"part": part["pk"], "sub_part_detail": "true"})
    hasil, maks = [], None
    for b in baris:
        per_unit = ke_desimal(b["quantity"])
        setup = ke_desimal(b.get("setup_quantity"))
        tersedia = ke_desimal(b.get("available_stock")) + ke_desimal(b.get("available_substitute_stock")) + \
            (ke_desimal(b.get("available_variant_stock")) if b.get("allow_variants") else Decimal(0))
        bisa = None
        if per_unit > 0 and not b.get("optional") and not b.get("consumable"):
            bisa = ((tersedia - setup) / per_unit).to_integral_value(rounding=ROUND_FLOOR)
            bisa = max(bisa, Decimal(0))
            maks = bisa if maks is None else min(maks, bisa)
        r = {"komponen": b.get("sub_part_detail") or {}, "per_unit": per_unit, "setup": setup, "tersedia": tersedia,
             "dipesan": ke_desimal(b.get("on_order")), "bisa": bisa, "opsional": bool(b.get("optional")),
             "habis_pakai": bool(b.get("consumable")), "attrition": ke_desimal(b.get("attrition"))}
        if jumlah is not None:
            butuh = per_unit * jumlah + setup
            if r["attrition"] > 0:
                butuh = butuh * (Decimal(1) + r["attrition"] / Decimal(100))
            r["butuh"] = butuh
            r["kurang"] = max(butuh - tersedia, Decimal(0))
        hasil.append(r)
    return hasil, (maks if maks is not None else Decimal(0))


def cmd_bom(args, token):
    p = cari_barang(args, token, args.produk)
    if not p.get("assembly"):
        raise Gagal(f"{ringkas_barang(p)} bukan produk rakitan (Assembly) di InvenTree, jadi tidak punya BOM. "
                    f"Centang 'Assembly' di data barang bila memang diproduksi sendiri.", K_INPUT)
    baris, maks = hitung_bom(args, token, p)
    teks = [f"BOM {ringkas_barang(p)} (bahan per 1 unit)"]
    for r in baris:
        k = r["komponen"]
        ket = [f"stok tersedia {fmt(r['tersedia'])}{satuan(k)}"]
        if r["bisa"] is not None:
            ket.append(f"cukup untuk {fmt(r['bisa'])} unit")
        if r["opsional"]:
            ket.append("opsional")
        if r["habis_pakai"]:
            ket.append("habis pakai, tidak dihitung")
        if r["setup"] > 0:
            ket.append(f"+ setup {fmt(r['setup'])} per produksi")
        teks.append(f"- {k.get('name', '?')} [{k.get('IPN') or '-'}]: {fmt(r['per_unit'])}{satuan(k)} ({'; '.join(ket)})")
    if not baris:
        teks.append("(BOM masih kosong - isi di InvenTree: buka barang > tab Bill of Materials)")
    else:
        teks.append(f"\nMaksimal bisa diproduksi dari stok sekarang: {fmt(maks)} unit"
                    " (dibatasi bahan dengan angka 'cukup untuk' terkecil; stok yang sudah dialokasikan tidak dihitung)")
    cetak({"teks": "\n".join(teks), "maks_produksi": dec(maks),
           "bom": [{"kode": r["komponen"].get("IPN"), "nama": r["komponen"].get("name"), "per_unit": dec(r["per_unit"]),
                    "tersedia": dec(r["tersedia"]), "cukup_untuk": None if r["bisa"] is None else dec(r["bisa"])}
                   for r in baris]}, args)
    return 0


def data_produksi_terbuka(args, token):
    daftar = ambil_semua("/build/", args, token, {"outstanding": "true", "part_detail": "true"})
    daftar.sort(key=lambda b: (b.get("target_date") or "9999", b.get("reference") or ""))
    return daftar


def cmd_produksi_ringkas(args, token):
    if args.produk:
        if args.jumlah is None:
            raise Gagal("Sebutkan juga --jumlah (berapa unit yang mau diproduksi).", K_INPUT)
        try:
            n = baca_angka_pengguna(args.jumlah)
        except ValueError as e:
            raise Gagal(f"--jumlah tidak valid: {e}", K_INPUT)
        if n <= 0:
            raise Gagal("--jumlah harus lebih dari 0.", K_INPUT)
        p = cari_barang(args, token, args.produk)
        if not p.get("assembly"):
            raise Gagal(f"{ringkas_barang(p)} bukan produk rakitan (Assembly), tidak punya BOM.", K_INPUT)
        baris, maks = hitung_bom(args, token, p, n)
        teks = [f"KEBUTUHAN BAHAN: {fmt(n)} unit {ringkas_barang(p)}"]
        kurang_ada = False
        for r in baris:
            k = r["komponen"]
            if r["habis_pakai"]:
                teks.append(f"- {k.get('name')} : habis pakai (tidak dihitung)")
                continue
            status = "CUKUP" if r["kurang"] == 0 else f"KURANG {fmt(r['kurang'])}{satuan(k)}"
            if r["kurang"] > 0 and not r["opsional"]:
                kurang_ada = True
            tambah = f"; sedang dipesan {fmt(r['dipesan'])}" if r["dipesan"] > 0 and r["kurang"] > 0 else ""
            teks.append(f"- {k.get('name', '?')} [{k.get('IPN') or '-'}]: butuh {fmt(r['butuh'])}{satuan(k)}, "
                        f"tersedia {fmt(r['tersedia'])} -> {status}{tambah}{' (opsional)' if r['opsional'] else ''}")
        teks.append(f"\nKesimpulan: {'BAHAN BELUM CUKUP' if kurang_ada else 'bahan CUKUP'} untuk {fmt(n)} unit. "
                    f"Maksimal dari stok sekarang: {fmt(maks)} unit.")
        teks.append("Hitungan: butuh = per unit x jumlah (+ setup, + susut % bila diisi di BOM); tersedia = stok bebas "
                    "(belum dialokasikan) termasuk pengganti.")
        cetak({"teks": "\n".join(teks), "cukup": not kurang_ada, "maks_produksi": dec(maks),
               "bahan": [{"kode": r["komponen"].get("IPN"), "butuh": dec(r.get("butuh")), "tersedia": dec(r["tersedia"]),
                          "kurang": dec(r.get("kurang"))} for r in baris]}, args)
        return 0
    daftar = data_produksi_terbuka(args, token)
    teks = [f"PERINTAH PRODUKSI TERBUKA: {len(daftar)}"]
    for b in daftar:
        pd = b.get("part_detail") or {}
        jml, selesai = ke_desimal(b["quantity"]), ke_desimal(b.get("completed"))
        telat = " - TERLAMBAT" if b.get("overdue") else ""
        teks.append(f"- {b['reference']} {pd.get('name', b.get('part_name', '?'))}: {fmt(selesai)}/{fmt(jml)} selesai | "
                    f"{STATUS_PRODUKSI.get(b.get('status'), b.get('status_text'))} | target {tgl_pendek(b.get('target_date'))}{telat}")
    if not daftar:
        teks.append("(tidak ada perintah produksi terbuka)")
    teks.append("Untuk cek bahan: produksi-ringkas --produk <kode> --jumlah <unit>")
    cetak({"teks": "\n".join(teks), "produksi": [{"nomor": b["reference"], "produk": b.get("part_name"),
                                                 "jumlah": dec(ke_desimal(b["quantity"])), "selesai": dec(ke_desimal(b.get("completed"))),
                                                 "target": b.get("target_date"), "terlambat": bool(b.get("overdue"))}
                                                for b in daftar]}, args)
    return 0


def tulis_csv(path, kolom, baris, pemisah):
    if path == "-":
        f = io.StringIO()
    else:
        d = os.path.dirname(os.path.abspath(path))
        os.makedirs(d, exist_ok=True)
        f = open(path, "w", encoding="utf-8-sig", newline="")
    w = csv.writer(f, delimiter=pemisah)
    w.writerow(kolom)
    for b in baris:
        w.writerow([_aman_csv(x) for x in b])
    if path == "-":
        sys.stdout.write(f.getvalue())
    else:
        f.close()


def _aman_csv(nilai):
    """Cegah injeksi rumus Excel (=, +, -, @ di awal teks)."""
    s = "" if nilai is None else str(nilai)
    if s and s[0] in "=+-@" and not re.fullmatch(r"-?[\d.,]+", s):
        return "'" + s
    return s


def angka_csv(d, pemisah):
    s = f"{ke_desimal(d).normalize():f}"
    return s.replace(".", ",") if pemisah == ";" else s


def cmd_ekspor_csv(args, token):
    pem = ";" if args.pemisah == "titik-koma" else ","
    keluaran = args.keluaran or f"stok-{args.jenis}-{hari_ini(args.tz).isoformat()}.csv"
    if args.jenis == "barang":
        daftar = ambil_semua("/part/", args, token, {"active": "true"})
        daftar.sort(key=lambda p: (p.get("category_name") or "", p["name"]))
        kolom = ["kode", "nama", "kategori", "satuan", "stok", "minimum", "sedang_dipesan", "status"]
        baris = []
        for p in daftar:
            stok, mn = ke_desimal(p.get("total_in_stock", p.get("in_stock"))), ke_desimal(p.get("minimum_stock"))
            baris.append([p.get("IPN") or "", p["name"], p.get("category_name") or "", p.get("units") or "",
                          angka_csv(stok, pem), angka_csv(mn, pem), angka_csv(p.get("ordering"), pem),
                          "DI BAWAH MINIMUM" if mn > 0 and stok < mn else "aman"])
    else:
        q = {}
        if args.lokasi:
            lok = cari_lokasi(args, token, args.lokasi)
            q = {"location": lok["pk"], "cascade": "true"}
        daftar = item_stok(args, token, q)
        daftar.sort(key=lambda i: (nama_lokasi(i), (i.get("part_detail") or {}).get("name", "")))
        kolom = ["id_stok", "kode", "nama", "lokasi", "batch", "jumlah", "satuan", "kedaluwarsa", "status", "tgl_opname_terakhir"]
        baris = []
        for i in daftar:
            pd = i.get("part_detail") or {}
            baris.append([i["pk"], pd.get("IPN") or "", pd.get("name", ""), nama_lokasi(i), i.get("batch") or "",
                          angka_csv(i["quantity"], pem), pd.get("units") or "", i.get("expiry_date") or "",
                          i.get("status_text") or "", i.get("stocktake_date") or ""])
    tulis_csv(keluaran, kolom, baris, pem)
    if keluaran != "-":
        cetak({"teks": f"EKSPOR CSV ({args.jenis}): {len(baris)} baris -> {keluaran}\nPemisah kolom '{pem}'"
                       f"{' (desimal koma, cocok Excel Indonesia)' if pem == ';' else ''}.",
               "file": keluaran, "baris": len(baris)}, args)
    return 0


def cmd_laporan_harian(args, token):
    tgl = hari_ini(args.tz)
    teks = [f"LAPORAN GUDANG HARIAN - {tgl_panjang(tgl)}"]
    menipis = data_stok_menipis(args, token)
    teks += [""] + teks_stok_menipis(menipis)
    po = data_po_terbuka(args, token)
    telat = [o for o in po if o.get("overdue")]
    teks.append(f"\nPO TERBUKA: {len(po)} ({len(telat)} terlambat)")
    for o in po[:10]:
        teks.append(f"- {o['reference']} {o.get('supplier_name') or '-'}: target {tgl_pendek(o.get('target_date'))}"
                    f"{' - TERLAMBAT' if o.get('overdue') else ''}")
    if len(po) > 10:
        teks.append(f"(+{len(po) - 10} PO lagi: jalankan po-terbuka)")
    prod = data_produksi_terbuka(args, token)
    teks.append(f"\nPRODUKSI TERBUKA: {len(prod)}")
    for b in prod[:10]:
        teks.append(f"- {b['reference']} {b.get('part_name', '?')}: {fmt(b.get('completed'))}/{fmt(b['quantity'])} | "
                    f"target {tgl_pendek(b.get('target_date'))}{' - TERLAMBAT' if b.get('overdue') else ''}")
    teks.append("\n(Laporan otomatis, hanya membaca InvenTree. Angka dari InvenTree apa adanya.)")
    cetak({"teks": "\n".join(teks), "stok_menipis": len(menipis), "po_terbuka": len(po), "po_terlambat": len(telat),
           "produksi_terbuka": len(prod)}, args)
    return 0


# ============================================================ opname (hitung fisik)

KOLOM_OPNAME = ["id_stok", "kode", "nama", "lokasi", "batch", "satuan", "stok_sistem", "stok_fisik", "catatan"]


def cmd_opname_draf(args, token):
    lok = cari_lokasi(args, token, args.lokasi)
    semua = item_stok(args, token, {"location": lok["pk"], "cascade": "true"})
    items = [i for i in semua if not i.get("serial")]
    ada_seri = len(semua) - len(items)
    items.sort(key=lambda i: (nama_lokasi(i), (i.get("part_detail") or {}).get("name", ""), i.get("batch") or ""))
    pem = ";" if args.pemisah == "titik-koma" else ","
    slug = re.sub(r"[^a-z0-9]+", "-", (lok.get("pathstring") or lok["name"]).lower()).strip("-")
    keluaran = args.keluaran or f"opname-{slug}-{hari_ini(args.tz).isoformat()}.csv"
    baris = []
    for i in items:
        pd = i.get("part_detail") or {}
        baris.append([i["pk"], pd.get("IPN") or "", pd.get("name", ""), nama_lokasi(i), i.get("batch") or "",
                      pd.get("units") or "", angka_csv(i["quantity"], pem), "", ""])
    tulis_csv(keluaran, KOLOM_OPNAME, baris, pem)
    teks = [f"LEMBAR OPNAME {lok.get('pathstring') or lok['name']}: {len(baris)} item -> {keluaran}",
            "Cara isi: cetak/buka di Excel, hitung barang fisik, isi kolom 'stok_fisik' (boleh koma: 12,5).",
            "Kosongkan 'stok_fisik' untuk item yang TIDAK dihitung. Jangan ubah kolom id_stok & stok_sistem.",
            f"Lalu: python3 inventree.py opname --file {keluaran}   (pratinjau selisih, belum menyimpan)"]
    if ada_seri:
        teks.append(f"Catatan: {ada_seri} item ber-nomor seri tidak dimasukkan (cek per unit di layar InvenTree).")
    cetak({"teks": "\n".join(teks), "file": keluaran, "jumlah": len(baris)}, args)
    return 0


def baca_lembar_opname(path):
    if not os.path.isfile(path):
        raise Gagal(f"File opname tidak ditemukan: {path}", K_FILE)
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        mentah = f.read()
    if not mentah.strip():
        raise Gagal("File opname kosong.", K_FILE)
    baris_pertama = mentah.splitlines()[0]
    pem = ";" if baris_pertama.count(";") > baris_pertama.count(",") else ","
    rd = csv.DictReader(io.StringIO(mentah), delimiter=pem)
    kolom = [c.strip().lower() for c in (rd.fieldnames or [])]
    wajib = {"id_stok", "stok_sistem", "stok_fisik"}
    if not wajib.issubset(kolom):
        raise Gagal(f"Kolom wajib tidak ada: {sorted(wajib - set(kolom))}. Pakai lembar dari 'opname-draf' "
                    f"(kolom: {', '.join(KOLOM_OPNAME)}).", K_FILE)
    isi, lewati, salah = [], [], []
    for no, r in enumerate(rd, start=2):
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        if not any(r.values()):
            continue
        ident = f"baris {no} ({r.get('nama') or r.get('kode') or r.get('id_stok')})"
        if not r.get("stok_fisik"):
            lewati.append(ident)
            continue
        try:
            sid = int(r["id_stok"])
            sistem = baca_angka_pengguna(r["stok_sistem"])
            fisik = baca_angka_pengguna(r["stok_fisik"])
        except (ValueError, KeyError) as e:
            salah.append(f"{ident}: {e}")
            continue
        if fisik < 0:
            salah.append(f"{ident}: stok fisik negatif ({r['stok_fisik']})")
            continue
        isi.append({"id": sid, "kode": r.get("kode", ""), "nama": r.get("nama", ""), "lokasi": r.get("lokasi", ""),
                    "batch": r.get("batch", ""), "satuan": r.get("satuan", ""), "sistem_lembar": sistem,
                    "fisik": fisik, "catatan": r.get("catatan", ""), "baris": no})
    ids = [x["id"] for x in isi]
    ganda = sorted({i for i in ids if ids.count(i) > 1})
    if ganda:
        salah.append(f"id_stok muncul lebih dari sekali: {ganda}")
    return isi, lewati, salah


BATAS_CATATAN = 500  # kolom catatan riwayat stok InvenTree 1.5.6 maks. 512 karakter


def susun_catatan_opname(tanggal, catatan_umum, isi):
    """Satu catatan transaksi untuk semua item (API /stock/count/ hanya menerima satu 'notes'). Catatan per baris
    lembar ditempel dengan id stoknya supaya tidak hilang diam-diam; dipotong rapi bila melebihi batas InvenTree."""
    teks = f"Opname {tanggal.isoformat()} via Komunitech inventree-gudang"
    if catatan_umum:
        teks += f": {catatan_umum}"
    per_baris = [f"id {x['id']} ({x['nama'] or x['kode']}): {x['catatan']}" for x in isi if x.get("catatan")]
    if per_baris:
        teks += " | Catatan baris: " + "; ".join(per_baris)
    if len(teks) > BATAS_CATATAN:
        teks = teks[:BATAS_CATATAN - 20].rstrip() + " ...(terpotong)"
    return teks


def cmd_opname(args, token):
    isi, lewati, salah = baca_lembar_opname(args.file)
    if salah:
        raise Gagal("Lembar opname berisi data yang tidak jelas - perbaiki dulu, TIDAK ADA yang disimpan:\n- " +
                    "\n- ".join(salah), K_INPUT)
    if not isi:
        raise Gagal("Tidak ada baris dengan 'stok_fisik' terisi. Isi dulu hasil hitung fisik.", K_INPUT)
    berubah = []
    for x in isi:
        try:
            now = panggil("GET", f"/stock/{x['id']}/", args, token)
        except Gagal as e:
            if e.kode == K_KONEKSI and "404" in str(e):
                raise Gagal(f"Item stok id {x['id']} ({x['nama']}) sudah tidak ada di InvenTree (habis/dihapus/digabung "
                            f"sejak lembar dibuat). Buat lembar baru dengan 'opname-draf'.", K_INPUT)
            raise
        x["sistem_kini"] = ke_desimal(now.get("quantity"))
        x["selisih"] = x["fisik"] - x["sistem_kini"]
        if x["sistem_kini"] != x["sistem_lembar"]:
            berubah.append(x)
    teks = [f"PRATINJAU OPNAME dari {os.path.basename(args.file)}: {len(isi)} item dihitung"
            + (f", {len(lewati)} dilewati (stok_fisik kosong)" if lewati else "")]
    beda = [x for x in isi if x["selisih"] != 0]
    for x in isi:
        u = f" {x['satuan']}" if x["satuan"] else ""
        tanda = "sama" if x["selisih"] == 0 else ("LEBIH " if x["selisih"] > 0 else "KURANG ") + fmt(abs(x["selisih"])) + u
        teks.append(f"- {x['nama']} [{x['kode'] or '-'}] {x['lokasi']}{' batch ' + x['batch'] if x['batch'] else ''}: "
                    f"sistem {fmt(x['sistem_kini'])}{u}, fisik {fmt(x['fisik'])}{u} -> {tanda}"
                    + (f" | catatan: {x['catatan']}" if x["catatan"] else ""))
    teks.append(f"\nRingkasan: {len(beda)} item selisih, {len(isi) - len(beda)} item sama.")
    if berubah:
        teks.append("\nBERHENTI: stok berikut BERUBAH di InvenTree sejak lembar dibuat (ada transaksi masuk/keluar):")
        for x in berubah:
            teks.append(f"- {x['nama']} (id {x['id']}): di lembar {fmt(x['sistem_lembar'])}, sekarang {fmt(x['sistem_kini'])}")
        teks.append("Hitung ulang item itu atau buat lembar baru ('opname-draf'). Tidak ada yang disimpan.")
        cetak({"teks": "\n".join(teks), "disimpan": False, "berubah": [x["id"] for x in berubah]}, args)
        return K_INPUT
    data_json = [{"id": x["id"], "nama": x["nama"], "sistem": dec(x["sistem_kini"]), "fisik": dec(x["fisik"]),
                  "selisih": dec(x["selisih"])} for x in isi]
    if not args.ya:
        ada_cat = any(x["catatan"] for x in isi)
        teks.append("\nBelum disimpan. Periksa angka di atas. Bila benar, ulangi perintah yang sama + --ya. "
                    "Semua item yang dihitung (termasuk yang sama) dicatat di riwayat stok InvenTree; tanggal opname "
                    "terakhir (stocktake) hanya berubah pada item yang jumlahnya berubah."
                    + (" Catatan per baris ikut disimpan di catatan transaksi." if ada_cat else ""))
        cetak({"teks": "\n".join(teks), "disimpan": False, "item": data_json}, args)
        return 0
    catatan = susun_catatan_opname(hari_ini(args.tz), args.catatan, isi)
    body = {"items": [{"pk": x["id"], "quantity": f"{x['fisik']:f}"} for x in isi], "notes": catatan}
    panggil("POST", "/stock/count/", args, token, body=body, tulis=True)
    teks2 = [f"TERSIMPAN: hasil opname {len(isi)} item dicatat di InvenTree ({len(beda)} item disesuaikan).",
             f"Catatan transaksi: {catatan}",
             "Riwayat tiap item bisa dilihat di InvenTree: buka item stok > tab Stock Tracking."]
    cetak({"teks": "\n".join(teks2), "disimpan": True, "item": data_json}, args)
    return 0


# ============================================================ terima barang dari PO


def cari_po(args, token, sebutan):
    s = str(sebutan).strip()
    if s.startswith("#") and s[1:].isdigit():
        return panggil("GET", f"/order/po/{int(s[1:])}/", args, token)
    semua = ambil_semua("/order/po/", args, token, {"search": s})
    persis = [o for o in semua if (o.get("reference") or "").lower() == s.lower()]
    if len(persis) == 1:
        return persis[0]
    if len(semua) == 1:
        return semua[0]
    if not semua:
        raise Gagal(f"PO '{s}' tidak ditemukan. Jalankan 'po-terbuka' untuk melihat nomor PO.", K_INPUT)
    raise Gagal(f"'{s}' cocok dengan beberapa PO: {', '.join(o['reference'] for o in semua[:10])}. Sebutkan nomor persis.", K_GANDA)


def urai_baris_terima(teks):
    """'BB-001=150, Minyak Goreng=40' -> [(sebutan, Decimal)]"""
    hasil = []
    for bagian in re.split(r"[;\n]|,(?=\s*[^\d\s])", teks):
        bagian = bagian.strip()
        if not bagian:
            continue
        if "=" not in bagian:
            raise Gagal(f"Format --baris salah di {bagian!r}. Contoh: --baris \"BB-001=150; BB-002=40\"", K_INPUT)
        kiri, kanan = bagian.rsplit("=", 1)
        try:
            n = baca_angka_pengguna(kanan)
        except ValueError:
            raise Gagal(f"Jumlah tidak valid di {bagian!r}.", K_INPUT)
        if n <= 0:
            raise Gagal(f"Jumlah harus lebih dari 0 di {bagian!r}.", K_INPUT)
        hasil.append((kiri.strip(), n))
    if not hasil:
        raise Gagal("--baris kosong.", K_INPUT)
    return hasil


def _label_baris(ln):
    pd = ln.get("part_detail") or {}
    sku = f", SKU pemasok {ln['sku']}" if ln.get("sku") else ""
    return f"{pd.get('IPN') or '-'} {pd.get('name', '?')} (#{pd.get('pk', ln.get('part'))}{sku})"


def pilih_baris_po(sebutan, terbuka, po):
    """Cocokkan sebutan barang ke baris PO terbuka. Urutan: #id barang -> IPN persis -> nama persis -> SKU persis
    -> (baru) potongan IPN/nama. Kecocokan PERSIS selalu menang atas potongan (PK-05 tidak bentrok dengan PK-05B)."""
    s = sebutan.strip()
    kecil = s.lower()

    def pd(ln):
        return ln.get("part_detail") or {}

    if s.startswith("#") and s[1:].isdigit():
        pid = int(s[1:])
        tahap = [[x for x in terbuka if pd(x[0]).get("pk", x[0].get("part")) == pid]]
    else:
        tahap = [
            [x for x in terbuka if (pd(x[0]).get("IPN") or "").lower() == kecil],
            [x for x in terbuka if (pd(x[0]).get("name") or "").lower() == kecil],
            [x for x in terbuka if (x[0].get("sku") or "").lower() == kecil],
            [x for x in terbuka if kecil in (pd(x[0]).get("IPN") or "").lower()
             or kecil in (pd(x[0]).get("name") or "").lower()],
        ]
    for cocok in tahap:
        if len(cocok) == 1:
            return cocok[0]
        if len(cocok) > 1:
            raise Gagal(f"'{s}' cocok dengan lebih dari satu baris {po['reference']}: " +
                        "; ".join(_label_baris(l) for l, _ in cocok) +
                        ". Sebutkan kode (IPN) persis, #id barang, atau SKU pemasok.", K_GANDA)
    raise Gagal(f"'{s}' tidak ada di baris terbuka {po['reference']}. Baris terbuka: " +
                "; ".join(_label_baris(l) for l, _ in terbuka), K_INPUT)


def cmd_terima_barang(args, token):
    po = cari_po(args, token, args.po)
    if po.get("status") not in (20, 25):
        raise Gagal(f"{po['reference']} berstatus '{STATUS_PO.get(po.get('status'), po.get('status_text'))}'. Barang hanya "
                    f"bisa diterima dari PO berstatus 'Sudah dipesan' (Placed). Ubah status di layar InvenTree bila perlu.",
                    K_INPUT)
    lines = baris_po(args, token, po["pk"])
    terbuka = []
    for ln in lines:
        sisa = ke_desimal(ln["quantity"]) - ke_desimal(ln.get("received"))
        if sisa > 0:
            terbuka.append((ln, sisa))
    if not terbuka:
        raise Gagal(f"Semua baris {po['reference']} sudah diterima penuh.", K_INPUT)
    rencana = []
    if args.semua:
        rencana = [(ln, sisa) for ln, sisa in terbuka]
    elif args.baris:
        for sebutan, n in urai_baris_terima(args.baris):
            ln, sisa = pilih_baris_po(sebutan, terbuka, po)
            if any(ln["pk"] == r[0]["pk"] for r in rencana):
                raise Gagal(f"'{sebutan}' disebut lebih dari sekali di --baris (baris PO yang sama). Gabungkan jumlahnya "
                            f"dalam satu entri, atau jalankan terpisah per batch.", K_INPUT)
            if n > sisa:
                raise Gagal(f"{(ln.get('part_detail') or {}).get('name')}: diterima {fmt(n)} melebihi sisa pesanan {fmt(sisa)}. "
                            f"Kelebihan barang dicatat manual di InvenTree (atau ubah jumlah PO dulu).", K_INPUT)
            rencana.append((ln, n))
    else:
        raise Gagal("Sebutkan barang yang diterima: --baris \"BB-001=150; BB-002=40\" atau --semua (semua sisa).", K_INPUT)
    lokasi = None
    if args.lokasi:
        lokasi = cari_lokasi(args, token, args.lokasi)
    elif po.get("destination"):
        lokasi = panggil("GET", f"/stock/location/{po['destination']}/", args, token)
    teks = [f"PRATINJAU TERIMA BARANG {po['reference']} dari {po.get('supplier_name') or '-'}",
            f"Masuk ke lokasi: {lokasi.get('pathstring') if lokasi else '(lokasi tujuan baris PO / belum ditentukan)'}"]
    if args.batch:
        teks.append(f"Kode batch: {args.batch}")
    peringatan = []
    for ln, n in rencana:
        pd = ln.get("part_detail") or {}
        spd = ln.get("supplier_part_detail") or {}
        kemasan = ke_desimal(spd.get("pack_quantity_native") or 1)
        teks.append(f"- {pd.get('name', '?')} [{pd.get('IPN') or '-'}]: terima {fmt(n)}"
                    f"{satuan(pd) if kemasan == 1 else f' kemasan pemasok (= {fmt(n * kemasan)}{satuan(pd)} stok)'} (sisa pesanan {fmt(ke_desimal(ln['quantity']) - ke_desimal(ln.get('received')))})")
        if kemasan != 1:
            peringatan.append(f"{pd.get('name')}: 1 kemasan pemasok = {fmt(kemasan)}{satuan(pd)}; jumlah di atas dalam KEMASAN.")
        if pd.get("trackable"):
            peringatan.append(f"{pd.get('name')}: barang ber-nomor seri - terima lewat layar InvenTree (skill ini tidak mengisi nomor seri).")
    if not lokasi and not all(ln.get("destination") for ln, _ in rencana):
        raise Gagal("Lokasi tujuan belum jelas. Tambahkan --lokasi \"Gudang Utama/Rak A\".", K_INPUT)
    if any("nomor seri" in p for p in peringatan):
        raise Gagal("\n".join(peringatan), K_INPUT)
    teks += [f"PERHATIAN: {p}" for p in peringatan]
    if not args.ya:
        teks.append("\nBelum disimpan. Cocokkan dengan surat jalan/nota pemasok. Bila benar, ulangi perintah + --ya.")
        cetak({"teks": "\n".join(teks), "disimpan": False}, args)
        return 0
    items = []
    for ln, n in rencana:
        it = {"line_item": ln["pk"], "quantity": f"{n:f}", "status": 10}
        if args.batch:
            it["batch_code"] = args.batch
        if args.kedaluwarsa:
            it["expiry_date"] = args.kedaluwarsa
        items.append(it)
    body = {"items": items}
    if lokasi:
        body["location"] = lokasi["pk"]
    panggil("POST", f"/order/po/{po['pk']}/receive/", args, token, body=body, tulis=True)
    teks2 = [f"TERSIMPAN: {len(items)} baris diterima dari {po['reference']} ke "
             f"{lokasi.get('pathstring') if lokasi else 'lokasi tujuan baris PO'}" + (f" (batch {args.batch})" if args.batch else "") + "."]
    for ln, n in rencana:
        pdx = ln.get("part_detail") or {}
        kemasan = ke_desimal((ln.get("supplier_part_detail") or {}).get("pack_quantity_native") or 1)
        if kemasan == 1:
            teks2.append(f"- {pdx.get('name')}: +{fmt(n)}{satuan(pdx)}")
        else:
            teks2.append(f"- {pdx.get('name')}: +{fmt(n)} kemasan pemasok = +{fmt(n * kemasan)}{satuan(pdx)} stok")
    teks2.append("Cek: 'po-terbuka' (sisa pesanan) atau 'stok <kode>'.")
    cetak({"teks": "\n".join(teks2), "disimpan": True}, args)
    return 0


# ============================================================ keluaran & argparse


def cetak(hasil, args):
    if getattr(args, "json", False):
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    else:
        print(hasil["teks"])


def _opsi_umum(p):
    p.add_argument("--url", default=os.environ.get("INVENTREE_API_HOST", URL_DEFAULT),
                   help="Alamat InvenTree (default ENV INVENTREE_API_HOST atau http://localhost)")
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--izinkan-jarak-jauh", dest="izinkan_jarak_jauh", action="store_true")
    p.add_argument("--tz", default="WIB", choices=list(TZ_OFFSET))
    p.add_argument("--json", action="store_true")
    p.add_argument("--timeout", type=float, default=20.0, help="Batas tunggu jawaban InvenTree (detik)")


def buat_parser():
    ap = argparse.ArgumentParser(prog="inventree.py", description="Asisten gudang InvenTree (Komunitech)", allow_abbrev=False)
    ap.add_argument("--versi", action="version", version=f"inventree-gudang {VERSI}")
    sub = ap.add_subparsers(dest="perintah", required=True)
    p = sub.add_parser("simpan-kunci", allow_abbrev=False)
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--ya", action="store_true")
    for nama in ("cek", "stok-menipis", "laporan-harian"):
        _opsi_umum(sub.add_parser(nama, allow_abbrev=False))
    p = sub.add_parser("cari", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("kata")
    p.add_argument("--maks", type=int, default=30)
    p = sub.add_parser("stok", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("barang")
    p.add_argument("--lokasi", default=None)
    p = sub.add_parser("lokasi", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("nama", nargs="?", default=None)
    p = sub.add_parser("po-terbuka", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--pemasok", default=None)
    p = sub.add_parser("bom", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("produk")
    p = sub.add_parser("produksi-ringkas", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--produk", default=None)
    p.add_argument("--jumlah", default=None)
    p = sub.add_parser("ekspor-csv", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--jenis", choices=["item", "barang"], default="item")
    p.add_argument("--lokasi", default=None)
    p.add_argument("--keluaran", default=None)
    p.add_argument("--pemisah", choices=["titik-koma", "koma"], default="titik-koma")
    p = sub.add_parser("opname-draf", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--lokasi", required=True)
    p.add_argument("--keluaran", default=None)
    p.add_argument("--pemisah", choices=["titik-koma", "koma"], default="titik-koma")
    p = sub.add_parser("opname", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--file", required=True)
    p.add_argument("--catatan", default=None)
    p.add_argument("--ya", action="store_true")
    p = sub.add_parser("terima-barang", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--po", required=True)
    p.add_argument("--baris", default=None)
    p.add_argument("--semua", action="store_true")
    p.add_argument("--lokasi", default=None)
    p.add_argument("--batch", default=None)
    p.add_argument("--kedaluwarsa", default=None, help="Tanggal kedaluwarsa YYYY-MM-DD (opsional)")
    p.add_argument("--ya", action="store_true")
    return ap


PERINTAH = {
    "cari": cmd_cari, "stok": cmd_stok, "lokasi": cmd_lokasi, "stok-menipis": cmd_stok_menipis,
    "po-terbuka": cmd_po_terbuka, "bom": cmd_bom, "produksi-ringkas": cmd_produksi_ringkas,
    "ekspor-csv": cmd_ekspor_csv, "laporan-harian": cmd_laporan_harian, "opname-draf": cmd_opname_draf,
    "opname": cmd_opname, "terima-barang": cmd_terima_barang,
}


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        if args.perintah == "simpan-kunci":
            return simpan_kunci(args)
        if args.perintah == "cek":
            return cmd_cek(args)
        if getattr(args, "kedaluwarsa", None):
            try:
                dt.date.fromisoformat(args.kedaluwarsa)
            except ValueError:
                raise Gagal("--kedaluwarsa harus berformat YYYY-MM-DD, mis. 2027-03-31.", K_INPUT)
        periksa_url(args.url, args.izinkan_jarak_jauh)
        token = ambil_token(args)
        return PERINTAH[args.perintah](args, token)
    except Gagal as e:
        sys.stderr.write(f"GALAT: {e}\n")
        return e.kode
    except KeyboardInterrupt:
        sys.stderr.write("Dibatalkan.\n")
        return 130


if __name__ == "__main__":
    sys.exit(main())
