#!/usr/bin/env python3
"""Asisten Odoo untuk usaha (Komunitech) - memakai API eksternal RESMI Odoo milik pengguna.

Hanya Python standar (urllib, xmlrpc.client, json). Lintas OS: macOS/Linux `python3`,
Windows `python` atau `py`.

Protokol (dokumentasi resmi Odoo, dicek 30 Sep 2026):
- XML-RPC `/xmlrpc/2/common` + `/xmlrpc/2/object` (Odoo 14-21; usang sejak 19.0, dijadwalkan
  dihapus di Odoo 22 / Online 21.1).
- JSON-2 `POST /json/2/<model>/<metode>` dengan header `Authorization: bearer <kunci API>`
  (Odoo 19 ke atas).
`--protokol otomatis` (default): Odoo 19+ -> json2, selain itu -> xmlrpc.

Prinsip keamanan:
- Default HANYA BACA. Satu-satunya penulisan: DRAF quotation (sale.order berstatus draft),
  hanya dengan `--ya` setelah pratinjau. Tidak ada konfirmasi pesanan, kirim email, posting
  faktur, pembayaran, ubah stok, atau HAPUS/unlink. Metode Odoo yang boleh dipanggil dikunci
  lewat daftar izin (METODE_BACA / METODE_TULIS).
- Kunci API dibaca dari --kunci-file, ENV ODOO_API_KEY, ENV ODOO_API_KEY_FILE, atau
  ~/.komunitech/odoo-kunci.txt (izin 600). Tidak pernah dicetak utuh (tampil ****abcd).
- Host diizinkan: komputer ini, *.odoo.com (https), atau host yang didaftarkan pemilik
  (`atur --izinkan-host`). Internet wajib https. Redirect ditolak (kunci tidak ikut pindah).

Kode keluar: 0 berhasil | 2 argumen/input/alamat salah | 3 Odoo tidak bisa dihubungi |
4 modul/fitur/protokol tidak tersedia | 5 kunci/login salah atau hak akses kurang |
6 galat lain dari Odoo | 7 tidak dibuat: kemungkinan data ganda atau pilihan ambigu |
8 SAAT MENULIS: koneksi putus/timeout/jawaban rusak/galat 5xx - draf MUNGKIN sudah tersimpan,
cek Odoo dulu, JANGAN langsung mengulang.
"""
import argparse
import datetime as dt
import hashlib
import http.client
import ipaddress
import json
import os
import re
import socket
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
import xmlrpc.client
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

VERSI_SKRIP = "1.0.0"
URL_DEFAULT = "http://localhost:8069"
VERSI_RANCANG = (16, 20)          # rentang versi yang dirancang (belum diuji ke Odoo asli)
BATAS_WAKTU = 20
PER_HALAMAN = 200
MAKS_HALAMAN = 50                 # 10.000 baris
MAKS_JAWABAN = 20 * 1024 * 1024   # 20 MB
BATAS_JUMLAH = Decimal(1000000)
BATAS_HARGA = Decimal(100000000000)
MAKS_TELEGRAM = 3500              # batas aman < 4096 karakter satu pesan Telegram

KELUAR_ARG, KELUAR_KONEKSI, KELUAR_MODUL, KELUAR_AKSES, KELUAR_LAIN, KELUAR_DOBEL = 2, 3, 4, 5, 6, 7
KELUAR_TIDAK_PASTI = 8

# Daftar izin metode Odoo. Semua panggilan lewat Odoo.panggil() diperiksa di sini.
METODE_BACA = {"search_read", "search_count", "read", "fields_get", "context_get"}
METODE_TULIS = {("sale.order", "create")}

PPN = {
    "umum": {"efektif": Decimal("0.11"), "label": "PPN 12% x DPP nilai lain 11/12 (efektif 11%)"},
    "mewah": {"efektif": Decimal("0.12"), "label": "PPN 12% x DPP penuh (barang mewah)"},
    "tanpa": {"efektif": Decimal("0"), "label": "tanpa PPN (bukan PKP)"},
}
ZONA = {"WIB": 7, "WITA": 8, "WIT": 9, "Asia/Jakarta": 7, "Asia/Pontianak": 7, "Asia/Makassar": 8,
        "Asia/Jayapura": 9}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
PENANDA = "Draf AI Komunitech"
KUNCI_TERLARANG_KONFIG = ("api_key", "apikey", "kunci", "password", "sandi", "token", "key")

_RAHASIA = []


# ------------------------------------------------------------------ utilitas
class Gagal(Exception):
    def __init__(self, pesan, kode=KELUAR_LAIN, saran=None, mungkin_terkirim=False, status=None):
        super().__init__(pesan)
        self.pesan, self.kode, self.saran = pesan, kode, saran
        self.mungkin_terkirim, self.status = mungkin_terkirim, status


def samarkan_kunci(k):
    if not k:
        return "(kosong)"
    return "****" + k[-4:] if len(k) >= 12 else "****"


def samarkan(teks):
    teks = str(teks)
    for r in _RAHASIA:
        if r and r in teks:
            teks = teks.replace(r, samarkan_kunci(r))
    return teks


def cetak(teks="", file=None):
    print(samarkan(teks), file=file or sys.stdout)


def desimal(nilai):
    if nilai in (None, False, ""):
        return Decimal(0)
    try:
        return Decimal(str(nilai))
    except (InvalidOperation, ValueError):
        return Decimal(0)


def uang(nilai):
    """Nilai float Odoo -> Decimal 2 desimal (hindari 0,1+0,2 float)."""
    return desimal(nilai).quantize(Decimal("0.01"), ROUND_HALF_UP)


def rupiah_bulat(d):
    return Decimal(d).quantize(Decimal(1), ROUND_HALF_UP)


def format_rp(d):
    d = Decimal(d).quantize(Decimal("0.01"), ROUND_HALF_UP)
    neg, d = d < 0, abs(d)
    bulat = int(d)
    sen = int((d - bulat) * 100)
    s = "{:,}".format(bulat).replace(",", ".")
    if sen:
        s += ",{:02d}".format(sen)
    return ("-Rp " if neg else "Rp ") + s


def format_angka(d):
    d = Decimal(d).quantize(Decimal("0.001"), ROUND_HALF_UP).normalize()
    if d == d.to_integral_value():
        return "{:,}".format(int(d)).replace(",", ".")
    bulat, pecahan = str(abs(d)).split(".")
    return ("-" if d < 0 else "") + "{:,}".format(int(bulat)).replace(",", ".") + "," + pecahan


def persen_ubah(sekarang, banding):
    sekarang, banding = Decimal(sekarang), Decimal(banding)
    if banding <= 0:
        return None
    return ((sekarang - banding) / banding * 100).quantize(Decimal("0.1"), ROUND_HALF_UP)


def ke_json(o):
    if isinstance(o, Decimal):
        return int(o) if o == o.to_integral_value() else float(o)
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()
    raise TypeError(str(type(o)))


def inisial(nama):
    bagian = [b for b in re.split(r"[\s,]+", str(nama or "").strip()) if b and b[0].isalnum()]
    return ".".join(b[0].upper() for b in bagian[:3]) + "." if bagian else "?"


def samarkan_hp(no):
    d = re.sub(r"\D", "", str(no or ""))
    if d.startswith("62"):
        d = "0" + d[2:]
    if len(d) < 7:
        return "****" if d else ""
    return d[:4] + "****" + d[-3:]


def samarkan_email(e):
    e = str(e or "")
    if "@" not in e:
        return ""
    a, b = e.split("@", 1)
    return (a[:1] + "***@" + b) if a else "***@" + b


def m2o(v):
    """Nilai many2one Odoo [id, "nama"] atau False -> (id, nama)."""
    if isinstance(v, (list, tuple)) and len(v) >= 2:
        return v[0], str(v[1])
    if isinstance(v, int) and not isinstance(v, bool):
        return v, ""
    return None, ""


def teks_odoo(v):
    """Field teks Odoo: False = kosong."""
    return "" if v in (None, False) else str(v)


def pendek(teks, n=60):
    teks = re.sub(r"\s+", " ", teks_odoo(teks)).strip()
    return teks if len(teks) <= n else teks[: n - 1] + "…"


# ------------------------------------------------------------------ tanggal & zona
def zona_offset(nama):
    if nama not in ZONA:
        raise Gagal("Zona waktu '{}' tidak dikenal. Pakai WIB, WITA, atau WIT.".format(nama), KELUAR_ARG)
    return ZONA[nama]


def hari_ini(offset):
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=offset)).date()


def parse_tanggal(teks, offset):
    t = (teks or "hari-ini").strip().lower()
    if t in ("hari-ini", "hariini", "today", "sekarang"):
        return hari_ini(offset)
    if t in ("kemarin", "yesterday"):
        return hari_ini(offset) - dt.timedelta(days=1)
    for pola in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(teks.strip(), pola).date()
        except ValueError:
            pass
    raise Gagal("Tanggal '{}' tidak dikenali. Contoh: hari-ini, kemarin, 2026-09-30, 30/09/2026.".format(teks),
                KELUAR_ARG)


def tanggal_panjang(t):
    return "{}, {} {} {}".format(HARI[t.weekday()], t.day, BULAN[t.month], t.year)


def rentang_utc(tanggal, offset):
    """Tanggal lokal -> (awal, akhir) string UTC untuk field Datetime Odoo (disimpan UTC)."""
    awal = dt.datetime(tanggal.year, tanggal.month, tanggal.day) - dt.timedelta(hours=offset)
    akhir = awal + dt.timedelta(days=1)
    f = "%Y-%m-%d %H:%M:%S"
    return awal.strftime(f), akhir.strftime(f)


def tanggal_odoo(v):
    if not v:
        return None
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


# ------------------------------------------------------------------ angka gaya Indonesia
def angka_id(x, label, batas=None, nomor=None):
    awal = "Item {}: ".format(nomor) if nomor else ""
    asli = x
    x = re.sub(r"(?i)^rp\.?", "", str(x).replace(" ", ""))
    if x.startswith("-"):
        raise Gagal("{}{} tidak boleh negatif.".format(awal, label), KELUAR_ARG)
    if re.fullmatch(r"\d{1,3}(,\d{3})+", x):
        raise Gagal("{}{} '{}' ambigu (62,500 bisa berarti 62.500 atau 62,5). Tulis 62500 atau 62.500."
                    .format(awal, label, asli), KELUAR_ARG)
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", x):
        x = x.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d+,\d+", x):
        x = x.replace(",", ".")
    if not re.fullmatch(r"\d+(\.\d+)?", x):
        raise Gagal("{}{} '{}' bukan angka biasa (contoh benar: 3, 2,5, 85000, 85.000).".format(awal, label, asli),
                    KELUAR_ARG)
    d = Decimal(x)
    if batas is not None and d > batas:
        raise Gagal("{}{} {} terlalu besar (maks. {}).".format(awal, label, format_angka(d), format_angka(batas)),
                    KELUAR_ARG)
    return d


# ------------------------------------------------------------------ konfigurasi, kunci, host
def folder_komunitech():
    return os.path.join(os.path.expanduser("~"), ".komunitech")


def lokasi_konfig():
    return os.environ.get("ODOO_KONFIG") or os.path.join(folder_komunitech(), "odoo.json")


def lokasi_file_kunci():
    return os.path.join(folder_komunitech(), "odoo-kunci.txt")


def izin_file_aman(path):
    if os.name == "nt":
        return True
    return (stat.S_IMODE(os.stat(path).st_mode) & 0o077) == 0


def baca_konfig():
    """Konfigurasi NON-rahasia (url, db, login, host_diizinkan, protokol, tz). Kembalikan (dict, peringatan)."""
    path = os.path.expanduser(lokasi_konfig())
    if not os.path.isfile(path):
        return {}, []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.loads(f.read(65536))
    except (OSError, ValueError, UnicodeDecodeError) as e:
        raise Gagal("Berkas konfigurasi {} rusak/tidak bisa dibaca ({}).".format(path, type(e).__name__), KELUAR_ARG,
                    saran="Buat ulang dengan perintah `atur` (lihat SKILL.md).")
    if not isinstance(data, dict):
        raise Gagal("Berkas konfigurasi {} harus berisi objek JSON.".format(path), KELUAR_ARG)
    peringatan = []
    for k in list(data):
        if any(t in k.lower() for t in KUNCI_TERLARANG_KONFIG) and k.lower() not in ("host_diizinkan",):
            nilai = data.pop(k)
            if isinstance(nilai, str) and len(nilai) >= 4:
                _RAHASIA.append(nilai)
            peringatan.append("PERINGATAN: berkas konfigurasi {} berisi field '{}' (mirip rahasia). DIABAIKAN. "
                              "Kunci API hanya dibaca dari file kunci/ENV; hapus field itu dari konfigurasi."
                              .format(path, k))
    return data, peringatan


def tulis_konfig(data):
    path = os.path.abspath(os.path.expanduser(lokasi_konfig()))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.name != "nt":
        os.chmod(os.path.dirname(path), 0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def bersihkan_kunci(mentah, sumber):
    mentah = (mentah or "").replace("﻿", "")
    for potong in re.split(r"\s+", mentah):
        if len(potong) >= 4:
            _RAHASIA.append(potong)
    k = mentah.strip()
    if not k:
        return ""
    if re.search(r"\s", k) or not re.fullmatch(r"[\x21-\x7e]+", k):
        raise Gagal("Kunci API dari {} berisi spasi, baris baru, atau karakter aneh, jadi tidak dipakai.".format(sumber),
                    KELUAR_AKSES, saran="Buat kunci baru di Odoo (Preferensi > Keamanan Akun > Kunci API Baru), lalu "
                                        "simpan lagi dengan `simpan-kunci`. File kunci berisi satu baris saja.")
    if len(k) < 8:
        raise Gagal("Kunci API dari {} terlalu pendek.".format(sumber), KELUAR_AKSES)
    return k


def baca_kunci(path_file=None):
    """Urutan: --kunci-file (selalu menang) > ENV ODOO_API_KEY > ENV ODOO_API_KEY_FILE > file default."""
    peringatan = None
    env = os.environ.get("ODOO_API_KEY", "")
    if path_file:
        if env.strip():
            try:
                bersihkan_kunci(env, "ENV ODOO_API_KEY")
            except Gagal:
                pass
            peringatan = ("PERINGATAN: ENV ODOO_API_KEY juga terisi, tetapi DIABAIKAN karena --kunci-file diberikan.")
        path = os.path.expanduser(path_file)
        if not os.path.isfile(path):
            raise Gagal("File kunci {} (dari --kunci-file) tidak ditemukan.".format(path), KELUAR_AKSES,
                        saran="Simpan kunci ke file itu dulu: python3 scripts/odoo.py simpan-kunci --kunci-file \"{}\""
                        .format(path))
    else:
        k = bersihkan_kunci(env, "ENV ODOO_API_KEY")
        if k:
            return k, "ENV ODOO_API_KEY", None
        path = os.path.expanduser(os.environ.get("ODOO_API_KEY_FILE") or lokasi_file_kunci())
    if os.path.isfile(path):
        if not izin_file_aman(path):
            raise Gagal("File kunci {} bisa dibaca pengguna lain. Amankan dulu: chmod 600 \"{}\"".format(path, path),
                        KELUAR_AKSES)
        try:
            with open(path, encoding="utf-8") as f:
                isi = f.read(4096)
        except (OSError, UnicodeDecodeError) as e:
            raise Gagal("File kunci {} tidak bisa dibaca ({}).".format(path, type(e).__name__), KELUAR_AKSES)
        k = bersihkan_kunci(isi, "file " + path)
        if k:
            return k, "file " + path, peringatan
        if path_file:
            raise Gagal("File kunci {} kosong.".format(path), KELUAR_AKSES)
    raise Gagal("Kunci API Odoo belum diatur.", KELUAR_AKSES,
                saran="Buat kunci di Odoo (klik foto profil > Preferensi/My Profile > Keamanan Akun > Kunci API Baru), "
                      "lalu jalankan SENDIRI di terminal: python3 scripts/odoo.py simpan-kunci . "
                      "Jangan tempel kunci di chat.")


def host_odoo_com(host):
    return host.endswith(".odoo.com") and host.count(".") >= 2


def cek_url(url, host_izin):
    """Validasi alamat Odoo + allowlist host. Kembalikan (url_bersih, host, tanpa_proxy:bool, catatan:list)."""
    url = (url or "").strip().rstrip("/")
    for akhiran in ("/xmlrpc/2", "/json/2", "/odoo", "/web"):
        if url.endswith(akhiran):
            url = url[: -len(akhiran)]
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise Gagal("Alamat Odoo '{}' tidak valid. Contoh: http://localhost:8069 atau https://tokosaya.odoo.com"
                    .format(url), KELUAR_ARG)
    if p.username or p.password:
        raise Gagal("Jangan menaruh nama/sandi di alamat Odoo.", KELUAR_ARG)
    if p.query or p.fragment:
        raise Gagal("Alamat Odoo tidak boleh berisi '?' atau '#'. Contoh: https://tokosaya.odoo.com", KELUAR_ARG)
    host = p.hostname.lower().rstrip(".")
    izin = {h.strip().lower().rstrip(".") for h in host_izin if isinstance(h, str) and h.strip()}
    catatan = []
    loopback, privat = host == "localhost" or host.endswith(".localhost"), False
    try:
        ip = ipaddress.ip_address(host)
        loopback = loopback or ip.is_loopback
        privat = ip.is_private and not ip.is_loopback
    except ValueError:
        pass
    if loopback:
        return url, host, True, catatan
    if host_odoo_com(host):
        if p.scheme != "https":
            raise Gagal("Odoo Online (*.odoo.com) wajib memakai https://.", KELUAR_ARG)
        return url, host, False, catatan
    if host not in izin:
        raise Gagal("Host {} belum ada di daftar host yang diizinkan. Demi keamanan, skill ini hanya bicara dengan "
                    "Odoo di komputer ini, *.odoo.com, atau server yang Anda daftarkan sendiri.".format(host), KELUAR_ARG,
                    saran="Jika server itu memang milik Anda, pemilik menjalankan: python3 scripts/odoo.py atur "
                          "--url {} --izinkan-host  (pastikan https:// untuk server di internet).".format(url))
    if p.scheme != "https":
        if privat:
            catatan.append("PERINGATAN: koneksi ke {} memakai http (tidak terenkripsi). Aman hanya di jaringan kantor "
                           "sendiri; sebaiknya https.".format(host))
            return url, host, True, catatan
        raise Gagal("Server Odoo di internet wajib https:// agar kunci API tidak bisa disadap.", KELUAR_ARG)
    return url, host, privat, catatan


# ------------------------------------------------------------------ klien HTTP + Odoo
class _TolakRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Gagal("Odoo mengalihkan permintaan ke {} (kode {}). Kunci API tidak dikirim ulang.".format(newurl, code),
                    KELUAR_ARG, saran="Periksa alamat Odoo (mungkin harus https:// atau alamat lain). Pakai alamat "
                                      "persis seperti di browser setelah halaman login terbuka.")


def _pesan_fault(teks):
    """Ambil baris pesan yang berguna dari faultString Odoo (sering berisi traceback)."""
    baris = [b.strip() for b in str(teks or "").strip().splitlines() if b.strip()]
    if not baris:
        return ""
    akhir = baris[-1]
    akhir = re.sub(r"^(odoo\.exceptions\.|werkzeug\.exceptions\.)?\w+(Error|Exception|Denied|Warning)?:\s*", "", akhir)
    return akhir[:300]


class Odoo:
    def __init__(self, url, db, login, kunci, protokol="otomatis", tanpa_proxy=True, timeout=BATAS_WAKTU):
        self.url, self.db, self.login, self.kunci = url, db, login, kunci
        self.protokol_minta, self.protokol = protokol, None
        self.timeout = timeout
        self.uid = None
        self.versi_info = None
        self.versi = None
        self._fields = {}
        if kunci:
            _RAHASIA.append(kunci)
        handler = [_TolakRedirect()]
        if tanpa_proxy:
            handler.append(urllib.request.ProxyHandler({}))
        self.opener = urllib.request.build_opener(*handler)

    # -------------------------------------------------------------- HTTP dasar
    def _http(self, metode, jalur, body=None, header=None, tulis=False):
        u = self.url + jalur
        h = {"User-Agent": "komunitech-odoo-usaha/" + VERSI_SKRIP}
        h.update(header or {})
        req = urllib.request.Request(u, data=body, headers=h, method=metode)
        try:
            with self.opener.open(req, timeout=self.timeout) as r:
                return r.status, r.read(MAKS_JAWABAN + 1)
        except urllib.error.HTTPError as e:
            try:
                isi = e.read(65536)
            except (http.client.HTTPException, OSError):
                isi = b""
            if tulis and e.code >= 500:
                raise Gagal("Odoo membalas galat server {} saat menyimpan.".format(e.code), KELUAR_TIDAK_PASTI,
                            mungkin_terkirim=True, status=e.code)
            return e.code, isi
        except Gagal:
            raise
        except urllib.error.URLError as e:
            alasan = e.reason
            if tulis and not isinstance(alasan, (ConnectionRefusedError, socket.gaierror)):
                raise Gagal("Odoo tidak menjawab saat menyimpan ({}).".format(alasan), KELUAR_TIDAK_PASTI,
                            mungkin_terkirim=True)
            if isinstance(alasan, socket.gaierror):
                raise Gagal("Nama server {} tidak dikenal (cek ejaan alamat / koneksi internet).".format(self.url),
                            KELUAR_KONEKSI, saran="Buka alamat itu di browser untuk memastikan.")
            if isinstance(alasan, ssl_error_types()):
                raise Gagal("Sertifikat HTTPS server {} tidak valid ({}). Koneksi dihentikan demi keamanan."
                            .format(self.url, alasan), KELUAR_KONEKSI,
                            saran="Pasang sertifikat resmi (mis. Let's Encrypt) di server Odoo Anda.")
            raise Gagal("Odoo di {} tidak bisa dihubungi ({}).".format(self.url, alasan), KELUAR_KONEKSI,
                        saran="Pastikan Odoo menyala dan alamatnya benar (buka di browser). Odoo lokal biasanya "
                              "http://localhost:8069.")
        except (TimeoutError, socket.timeout, OSError, http.client.HTTPException) as e:
            if tulis:
                raise Gagal("Koneksi putus/timeout saat menyimpan ({}).".format(type(e).__name__), KELUAR_TIDAK_PASTI,
                            mungkin_terkirim=True)
            raise Gagal("Odoo tidak menjawab dalam {} detik ({}).".format(self.timeout, type(e).__name__),
                        KELUAR_KONEKSI, saran="Server mungkin sibuk; coba lagi, atau naikkan --timeout.")

    # -------------------------------------------------------------- versi & login
    def cari_versi(self):
        """GET /web/version (Odoo 19+). Gagal -> XML-RPC common.version(). Kembalikan dict versi atau None."""
        try:
            st, isi = self._http("GET", "/web/version", header={"Accept": "application/json"})
            if st == 200:
                d = json.loads(isi.decode("utf-8", "replace"))
                if isinstance(d, dict) and d.get("version_info"):
                    return {"server_version": str(d.get("version") or ""), "server_version_info": d["version_info"]}
        except (ValueError, UnicodeDecodeError):
            pass
        try:
            d = self._xmlrpc("/xmlrpc/2/common", "version", ())
            if isinstance(d, dict):
                return d
        except Gagal as e:
            if e.kode in (KELUAR_KONEKSI, KELUAR_ARG):
                raise
        return None

    @staticmethod
    def angka_mayor(info):
        try:
            v = info[0]
            m = re.search(r"\d+", str(v))
            return int(m.group()) if m else None
        except (TypeError, IndexError):
            return None

    def mulai(self):
        d = self.cari_versi()
        if d:
            self.versi = str(d.get("server_version") or "")
            self.versi_info = d.get("server_version_info") or []
        mayor = self.angka_mayor(self.versi_info) if self.versi_info else None
        p = self.protokol_minta
        if p == "otomatis":
            p = "json2" if (mayor or 0) >= 19 else "xmlrpc"
            if d is None:
                raise Gagal("Alamat {} menjawab, tetapi bukan API Odoo (versi tidak terbaca).".format(self.url),
                            KELUAR_MODUL, saran="Pastikan alamat mengarah ke Odoo (halaman login Odoo terbuka di "
                                                "browser). Paket Odoo Online harus paket Custom agar API aktif.")
        self.protokol = p
        if p == "json2" and mayor is not None and mayor < 19:
            raise Gagal("Protokol JSON-2 baru ada di Odoo 19 ke atas (server ini {}).".format(self.versi), KELUAR_MODUL,
                        saran="Pakai --protokol xmlrpc (atau otomatis).")
        if p == "xmlrpc":
            if not self.db:
                raise Gagal("Nama database Odoo belum diatur (wajib untuk XML-RPC).", KELUAR_ARG,
                            saran="Jalankan `atur --db NAMA_DB`. Nama database terlihat di halaman pilih database "
                                  "(/web/database/selector) atau tanyakan ke penyedia hosting. Odoo Online: biasanya "
                                  "sama dengan nama subdomain.")
            if not self.login:
                raise Gagal("Login (email/username) pengguna API belum diatur (wajib untuk XML-RPC).", KELUAR_ARG,
                            saran="Jalankan `atur --login emailbot@usaha.id`.")
            uid = self._xmlrpc("/xmlrpc/2/common", "authenticate", (self.db, self.login, self.kunci, {}))
            if not uid or isinstance(uid, bool):
                raise Gagal("Login ke Odoo ditolak (kunci API, login, atau nama database salah).", KELUAR_AKSES,
                            saran="Cek login & database dengan `atur`, buat kunci API baru bila perlu, lalu "
                                  "`simpan-kunci --ya`. Kunci API Odoo 19+ punya masa berlaku; mungkin sudah habis.")
            self.uid = int(uid)
        else:
            ctx = self.panggil("res.users", "context_get")
            self.uid = ctx.get("uid") if isinstance(ctx, dict) else None
        return self

    # -------------------------------------------------------------- XML-RPC
    def _xmlrpc(self, jalur, metode, params, tulis=False):
        body = xmlrpc.client.dumps(tuple(params), metode, allow_none=False).encode("utf-8")
        st, isi = self._http("POST", jalur, body, {"Content-Type": "text/xml"}, tulis=tulis)
        if st == 404:
            raise Gagal("Endpoint XML-RPC {} tidak ada di server ini (Odoo 22 / Odoo Online 21.1 ke atas sudah "
                        "menghapusnya, atau alamat salah).".format(jalur), KELUAR_MODUL,
                        saran="Coba --protokol json2 (Odoo 19+), atau periksa alamat Odoo.")
        if st in (401, 403):
            raise Gagal("Akses XML-RPC ditolak (HTTP {}).".format(st), KELUAR_AKSES,
                        saran="Odoo Online: API hanya tersedia di paket Custom (bukan One App Free/Standard).")
        if st != 200:
            raise Gagal("Odoo membalas HTTP {} untuk {}.".format(st, jalur), KELUAR_LAIN)
        if len(isi) > MAKS_JAWABAN:
            raise Gagal("Jawaban Odoo terlalu besar (> 20 MB).", KELUAR_LAIN)
        try:
            hasil, _ = xmlrpc.client.loads(isi, use_builtin_types=True)
        except xmlrpc.client.Fault as f:
            raise self._gagal_fault(f.faultCode, f.faultString, tulis)
        except Exception as e:  # XML rusak/terpotong
            if tulis:
                raise Gagal("Jawaban Odoo rusak/terpotong saat menyimpan ({}).".format(type(e).__name__),
                            KELUAR_TIDAK_PASTI, mungkin_terkirim=True)
            raise Gagal("Jawaban Odoo bukan XML-RPC yang sah ({}).".format(type(e).__name__), KELUAR_LAIN,
                        saran="Periksa alamat Odoo; mungkin ada halaman lain (proxy/login) di depannya.")
        return hasil[0] if hasil else None

    def _gagal_fault(self, kode, teks, tulis=False):
        pesan = _pesan_fault(teks)
        mentah = str(teks or "")
        if kode == 3 or "AccessDenied" in mentah or "Access Denied" in mentah:
            return Gagal("Login/kunci API ditolak Odoo (Access Denied).", KELUAR_AKSES,
                         saran="Kunci mungkin salah, dicabut, atau kedaluwarsa. Buat kunci baru, lalu `simpan-kunci --ya`.")
        if kode == 4 or "AccessError" in mentah:
            return Gagal("Hak akses pengguna API kurang: {}".format(pesan), KELUAR_AKSES,
                         saran="Beri pengguna API hak yang diperlukan (lihat docs/panduan-odoo.md §5), atau pakai "
                               "kunci pengguna lain.")
        if re.search(r"Object .+ doesn't exist|model .+ (does not|doesn't) exist|KeyError: '[a-z_.]+'", mentah):
            return Gagal("Aplikasi/modul Odoo yang dibutuhkan belum terpasang ({}).".format(pesan), KELUAR_MODUL)
        if "does not exist on the model" in mentah or "has no attribute" in mentah:
            return Gagal("Metode tidak tersedia di versi Odoo ini ({}).".format(pesan), KELUAR_MODUL)
        if "Invalid field" in mentah:
            return Gagal("Struktur data Odoo berbeda dari yang dirancang ({}).".format(pesan), KELUAR_MODUL,
                         saran="Jalankan `cek` dan laporkan versi Odoo ke dukungan Komunitech.")
        if kode == 2 or "UserError" in mentah or "ValidationError" in mentah:
            return Gagal("Odoo menolak: {}".format(pesan), KELUAR_LAIN)
        if tulis:
            return Gagal("Odoo membalas galat saat menyimpan: {}".format(pesan), KELUAR_TIDAK_PASTI,
                         mungkin_terkirim=True)
        return Gagal("Galat dari Odoo: {}".format(pesan or "tanpa pesan"), KELUAR_LAIN)

    # -------------------------------------------------------------- JSON-2
    def _json2(self, model, metode, ids=None, kw=None, tulis=False):
        data = dict(kw or {})
        if ids is not None:
            data["ids"] = list(ids)
        body = json.dumps(data).encode("utf-8")
        h = {"Authorization": "bearer " + self.kunci, "Content-Type": "application/json; charset=utf-8",
             "Accept": "application/json"}
        if self.db:
            h["X-Odoo-Database"] = self.db
        st, isi = self._http("POST", "/json/2/{}/{}".format(model, metode), body, h, tulis=tulis)
        teks = isi.decode("utf-8", "replace")
        if len(isi) > MAKS_JAWABAN:
            raise Gagal("Jawaban Odoo terlalu besar (> 20 MB).", KELUAR_LAIN)
        try:
            d = json.loads(teks) if teks.strip() else None
        except ValueError:
            if tulis and st == 200:
                raise Gagal("Jawaban Odoo rusak/terpotong saat menyimpan.", KELUAR_TIDAK_PASTI, mungkin_terkirim=True)
            raise Gagal("Jawaban Odoo bukan JSON (HTTP {}).".format(st), KELUAR_LAIN if st == 200 else KELUAR_MODUL,
                        saran="Periksa alamat Odoo; JSON-2 butuh Odoo 19+ (pakai --protokol xmlrpc untuk versi lama).")
        if st == 200:
            return d
        nama = str(d.get("name") or "") if isinstance(d, dict) else ""
        pesan = pendek(d.get("message") if isinstance(d, dict) else teks, 300)
        if st == 401:
            raise Gagal("Kunci API ditolak Odoo (401: {}).".format(pesan or "Unauthorized"), KELUAR_AKSES,
                        saran="Kunci mungkin salah, dicabut, atau kedaluwarsa. Buat kunci baru, lalu `simpan-kunci --ya`.")
        if st == 403 or "AccessError" in nama:
            raise Gagal("Hak akses pengguna API kurang: {}".format(pesan), KELUAR_AKSES,
                        saran="Beri pengguna API hak yang diperlukan (docs/panduan-odoo.md §5).")
        if st == 404:
            raise Gagal("Model/metode {}/{} tidak ditemukan (aplikasi belum terpasang, atau server bukan Odoo 19+)."
                        .format(model, metode), KELUAR_MODUL)
        if "Invalid field" in pesan or "ValueError" in nama:
            raise Gagal("Struktur data Odoo berbeda dari yang dirancang ({}).".format(pesan), KELUAR_MODUL)
        raise Gagal("Odoo menolak (HTTP {}): {}".format(st, pesan), KELUAR_LAIN)

    # -------------------------------------------------------------- panggilan umum (dengan daftar izin)
    def panggil(self, model, metode, ids=None, **kw):
        tulis = (model, metode) in METODE_TULIS
        if metode not in METODE_BACA and not tulis:
            raise Gagal("Metode {}.{} tidak diizinkan oleh skill ini (hanya baca + draf quotation).".format(model, metode),
                        KELUAR_ARG)
        if self.protokol == "json2":
            return self._json2(model, metode, ids, kw, tulis=tulis)
        args = [list(ids)] if ids is not None else []
        if metode == "create":
            args = [kw.pop("vals_list")]
        return self._xmlrpc("/xmlrpc/2/object", "execute_kw",
                            (self.db, self.uid, self.kunci, model, metode, args, kw), tulis=tulis)

    def fields(self, model):
        if model not in self._fields:
            d = self.panggil(model, "fields_get", attributes=["type"])
            self._fields[model] = d if isinstance(d, dict) else {}
        return self._fields[model]

    def punya_field(self, model, field):
        return field in self.fields(model)

    def cari(self, model, domain, fields, order=None, batas=None):
        hasil, offset = [], 0
        for _ in range(MAKS_HALAMAN):
            n = PER_HALAMAN if batas is None else min(PER_HALAMAN, batas - len(hasil))
            kw = {"domain": domain, "fields": fields, "offset": offset, "limit": n}
            if order:
                kw["order"] = order
            hal = self.panggil(model, "search_read", **kw) or []
            hasil.extend(hal)
            if len(hal) < n or (batas is not None and len(hasil) >= batas):
                break
            offset += n
        return hasil


def ssl_error_types():
    try:
        import ssl
        return (ssl.SSLError, ssl.CertificateError)
    except ImportError:  # pragma: no cover
        return ()


# ------------------------------------------------------------------ data bersama
def mata_uang_perusahaan(api):
    """(id, nama) mata uang perusahaan pengguna API."""
    try:
        u = api.panggil("res.users", "read", [api.uid], fields=["company_id"]) if api.uid else []
        cid, _ = m2o(u[0].get("company_id")) if u else (None, "")
        if cid:
            c = api.panggil("res.company", "read", [cid], fields=["currency_id", "name"])
            if c:
                return m2o(c[0].get("currency_id"))
    except Gagal:
        pass
    return None, ""


def catatan_mata_uang(nama_mu):
    if nama_mu and nama_mu != "IDR":
        return "CATATAN: mata uang perusahaan di Odoo = {} (bukan IDR). Angka tetap ditampilkan dengan awalan Rp " \
               "oleh skill ini; baca sebagai {}.".format(nama_mu, nama_mu)
    return None


# ------------------------------------------------------------------ perintah: atur & simpan-kunci
def cmd_atur(args):
    konfig, peringatan = baca_konfig()
    ubah = False
    for kunci_arg, kunci_konfig in (("url", "url"), ("db", "db"), ("login", "login"), ("protokol", "protokol"),
                                    ("tz", "tz")):
        v = getattr(args, kunci_arg, None)
        if v:
            konfig[kunci_konfig] = v
            ubah = True
    if konfig.get("url"):
        p = urllib.parse.urlsplit(konfig["url"].strip())
        host = (p.hostname or "").lower()
        if args.izinkan_host:
            if not host:
                raise Gagal("Alamat tidak valid; tidak ada host yang bisa diizinkan.", KELUAR_ARG)
            daftar = konfig.get("host_diizinkan") or []
            if host not in daftar:
                daftar.append(host)
                konfig["host_diizinkan"] = daftar
                ubah = True
        cek_url(konfig["url"], konfig.get("host_diizinkan") or [])  # tolak alamat buruk sebelum disimpan
        if host_odoo_com(host) and not konfig.get("db"):
            konfig["db"] = host.split(".")[0]
            ubah = True
            peringatan.append("CATATAN: database diisi otomatis '{}' dari subdomain Odoo Online. Ubah dengan --db "
                              "bila berbeda.".format(konfig["db"]))
    elif args.izinkan_host:
        raise Gagal("--izinkan-host butuh --url.", KELUAR_ARG)
    if args.tz:
        zona_offset(args.tz)
    path = os.path.abspath(os.path.expanduser(lokasi_konfig()))
    if ubah:
        path = tulis_konfig(konfig)
    b = ["KONFIGURASI ODOO ({})".format("disimpan" if ubah else "tidak berubah"),
         "File: {}".format(path)]
    for k in ("url", "db", "login", "protokol", "tz"):
        b.append("- {}: {}".format(k, konfig.get(k) or "(belum diisi)"))
    b.append("- host_diizinkan: {}".format(", ".join(konfig.get("host_diizinkan") or []) or "(hanya lokal & *.odoo.com)"))
    b.append("Kunci API TIDAK disimpan di sini. Simpan terpisah dengan `simpan-kunci` di terminal Anda sendiri.")
    b.extend(peringatan)
    return {"file": path, "konfigurasi": konfig, "teks": "\n".join(b)}


def cmd_simpan_kunci(args):
    import getpass
    path = os.path.abspath(os.path.expanduser(args.kunci_file or lokasi_file_kunci()))
    if os.path.exists(path) and not args.ya:
        raise Gagal("File kunci {} sudah ada. Tidak ditimpa.".format(path), KELUAR_ARG,
                    saran="Untuk kunci KEDUA (mis. pembuat draf) pakai file lain: simpan-kunci --kunci-file "
                          "~/.komunitech/odoo-kunci-draf.txt . Untuk mengganti kunci ini, ulangi dengan --ya.")
    cetak("Kunci akan disimpan di: {}".format(path), file=sys.stderr)
    if sys.stdin.isatty():
        k = getpass.getpass("Tempel kunci API Odoo (tidak akan tampil), lalu Enter: ")
    else:
        k = sys.stdin.readline()
    k = bersihkan_kunci(k, "masukan")
    if not k:
        raise Gagal("Kunci kosong. Tidak ada yang disimpan.", KELUAR_ARG)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.name != "nt":
        os.chmod(os.path.dirname(path), 0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(k + "\n")
    if os.name != "nt":
        os.chmod(path, 0o600)
    return {"file": path, "kunci": samarkan_kunci(k),
            "teks": "Kunci {} disimpan di {} (hanya bisa dibaca akun Anda).".format(samarkan_kunci(k), path)}


# ------------------------------------------------------------------ perintah: cek
MODEL_CEK = [("Kontak/pelanggan", "res.partner"), ("Penjualan (Sales)", "sale.order"),
             ("Faktur (Invoicing)", "account.move"), ("Produk", "product.product"),
             ("Aturan stok minimum (Inventory)", "stock.warehouse.orderpoint")]


def cmd_cek(api, args, catatan_url, sumber_kunci):
    b = ["CEK KONEKSI ODOO", "Alamat: {}".format(api.url),
         "Versi Odoo: {}".format(api.versi or "tidak terbaca"),
         "Protokol: {}".format("JSON-2 (/json/2)" if api.protokol == "json2" else "XML-RPC (/xmlrpc/2, usang sejak 19.0)"),
         "Database: {}".format(api.db or "(tidak dipakai/otomatis)"),
         "Kunci API: {} ({})".format(samarkan_kunci(api.kunci), sumber_kunci)]
    out = {"url": api.url, "versi": api.versi, "protokol": api.protokol, "db": api.db, "uid": api.uid,
           "modul": {}, "catatan": list(catatan_url)}
    try:
        u = api.panggil("res.users", "read", [api.uid], fields=["name", "login", "share"]) if api.uid else []
        if u:
            b.append("Pengguna API: {} ({}) id {}".format(u[0].get("name"), u[0].get("login"), api.uid))
            out["pengguna"] = {"nama": u[0].get("name"), "login": u[0].get("login")}
    except Gagal as e:
        b.append("Pengguna API: tidak terbaca ({})".format(e.pesan))
    _, mu = mata_uang_perusahaan(api)
    b.append("Mata uang perusahaan: {}".format(mu or "tidak terbaca"))
    out["mata_uang"] = mu
    c = catatan_mata_uang(mu)
    if c:
        out["catatan"].append(c)
    b.append("Akses baca:")
    for label, model in MODEL_CEK:
        try:
            n = api.panggil(model, "search_count", domain=[])
            status = "bisa dibaca ({} data)".format(format_angka(n))
            out["modul"][model] = "ok"
        except Gagal as e:
            status = "TIDAK TERPASANG" if e.kode == KELUAR_MODUL else ("TIDAK ADA HAK" if e.kode == KELUAR_AKSES
                                                                         else "galat: " + e.pesan)
            out["modul"][model] = status
        b.append("- {}: {}".format(label, status))
    try:
        api.panggil("ir.config_parameter", "search_count", domain=[])
        out["catatan"].append("RISIKO: kunci ini milik pengguna dengan hak ADMINISTRATOR Pengaturan. Untuk laporan & "
                              "jadwal, buat pengguna khusus berhak minimal (docs/panduan-odoo.md §5).")
        out["admin"] = True
    except Gagal:
        out["admin"] = False
    mayor = api.angka_mayor(api.versi_info) if api.versi_info else None
    if mayor is None or not VERSI_RANCANG[0] <= mayor <= VERSI_RANCANG[1]:
        out["catatan"].append("Versi Odoo ini di luar rentang yang dirancang ({}-{}). Cocokkan angka dengan layar Odoo."
                              .format(*VERSI_RANCANG))
    if api.protokol == "xmlrpc" and mayor and mayor >= 19:
        out["catatan"].append("XML-RPC usang sejak Odoo 19 dan akan dihapus (Odoo 22 / Online 21.1). Pakai --protokol "
                              "json2 atau otomatis.")
    out["catatan"].append("Skill ini belum diuji ke server Odoo asli (hanya server tiruan). Cocokkan angka pertama kali "
                          "dengan layar Odoo.")
    b.append("CATATAN:")
    b.extend("- " + x for x in out["catatan"])
    out["teks"] = "\n".join(b)
    return out


# ------------------------------------------------------------------ perintah: penjualan
def ambil_penjualan(api, tanggal, offset, mu_id):
    """Pesanan penjualan terkonfirmasi (sale.order) + faktur pelanggan terposting (account.move) pada tanggal lokal."""
    awal, akhir = rentang_utc(tanggal, offset)
    hasil = {"tanggal": tanggal, "pesanan": None, "faktur": None, "galat": {}}
    try:
        so = api.cari("sale.order", [["state", "in", ["sale", "done"]], ["date_order", ">=", awal],
                                     ["date_order", "<", akhir]],
                      ["name", "partner_id", "amount_untaxed", "amount_tax", "amount_total", "currency_id",
                       "date_order"], order="date_order asc")
        utama = [s for s in so if mu_id is None or m2o(s.get("currency_id"))[0] in (None, mu_id)]
        lain = [s for s in so if s not in utama]
        hasil["pesanan"] = {
            "jumlah": len(utama),
            "dpp": sum((uang(s.get("amount_untaxed")) for s in utama), Decimal(0)),
            "pajak": sum((uang(s.get("amount_tax")) for s in utama), Decimal(0)),
            "total": sum((uang(s.get("amount_total")) for s in utama), Decimal(0)),
            "ids": [s["id"] for s in utama], "data": utama,
            "mata_uang_lain": [{"nomor": s.get("name"), "mata_uang": m2o(s.get("currency_id"))[1],
                                "total": uang(s.get("amount_total"))} for s in lain]}
    except Gagal as e:
        hasil["galat"]["pesanan"] = e
    try:
        fk = api.cari("account.move", [["move_type", "in", ["out_invoice", "out_refund"]], ["state", "=", "posted"],
                                       ["invoice_date", "=", tanggal.isoformat()]],
                      ["name", "move_type", "partner_id", "amount_untaxed_signed", "amount_tax_signed",
                       "amount_total_signed"])
        hasil["faktur"] = {
            "jumlah": sum(1 for f in fk if f.get("move_type") == "out_invoice"),
            "nota_kredit": sum(1 for f in fk if f.get("move_type") == "out_refund"),
            "dpp": sum((uang(f.get("amount_untaxed_signed")) for f in fk), Decimal(0)),
            "pajak": sum((uang(f.get("amount_tax_signed")) for f in fk), Decimal(0)),
            "total": sum((uang(f.get("amount_total_signed")) for f in fk), Decimal(0))}
    except Gagal as e:
        hasil["galat"]["faktur"] = e
    return hasil


def produk_terlaris(api, order_ids, n=5):
    if not order_ids:
        return []
    baris = api.cari("sale.order.line", [["order_id", "in", order_ids]],
                     ["product_id", "product_uom_qty", "price_subtotal"]) if order_ids else []
    agg = {}
    for r in baris:
        pid, nama = m2o(r.get("product_id"))
        if not pid:
            continue
        a = agg.setdefault(pid, {"nama": nama, "qty": Decimal(0), "nilai": Decimal(0)})
        a["qty"] += desimal(r.get("product_uom_qty"))
        a["nilai"] += uang(r.get("price_subtotal"))
    return sorted(agg.values(), key=lambda a: (-a["nilai"], a["nama"]))[:n]


def _panggil_baca_saja(fungsi, *a):
    try:
        return fungsi(*a), None
    except Gagal as e:
        return None, e


def cmd_penjualan(api, args, offset):
    tgl = parse_tanggal(args.tanggal, offset)
    mu_id, mu = mata_uang_perusahaan(api)
    h = ambil_penjualan(api, tgl, offset, mu_id)
    kmrn = ambil_penjualan(api, tgl - dt.timedelta(days=1), offset, mu_id)
    if h["pesanan"] is None and h["faktur"] is None:
        e = h["galat"].get("pesanan") or h["galat"].get("faktur")
        raise Gagal("Penjualan tidak bisa dibaca: " + e.pesan, e.kode, saran=e.saran)
    b = ["RINGKASAN PENJUALAN ODOO", tanggal_panjang(tgl)]
    out = {"tanggal": tgl, "mata_uang": mu}
    c = catatan_mata_uang(mu)
    if h["pesanan"] is not None:
        p = h["pesanan"]
        b += ["", "PESANAN PENJUALAN TERKONFIRMASI (Sales)", "Jumlah pesanan: {}".format(p["jumlah"]),
              "Total (termasuk pajak): {}".format(format_rp(p["total"])),
              "Sebelum pajak {} | Pajak {}".format(format_rp(p["dpp"]), format_rp(p["pajak"]))]
        if kmrn["pesanan"] is not None:
            pr = persen_ubah(p["total"], kmrn["pesanan"]["total"])
            b.append("Kemarin: {}{}".format(format_rp(kmrn["pesanan"]["total"]),
                                            "" if pr is None else " ({}{}%)".format("+" if pr > 0 else "",
                                                                                   format_angka(pr))))
        if p["jumlah"]:
            b.append("Rata-rata per pesanan: {}".format(format_rp(rupiah_bulat(p["total"] / p["jumlah"]))))
        terlaris, e = _panggil_baca_saja(produk_terlaris, api, p["ids"])
        if terlaris:
            b.append("Produk terlaris (nilai sebelum pajak):")
            for i, t in enumerate(terlaris, 1):
                b.append("{}. {}: {} unit, {}".format(i, pendek(t["nama"], 50), format_angka(t["qty"]),
                                                      format_rp(t["nilai"])))
        elif e:
            b.append("Produk terlaris: tidak bisa dibaca ({})".format(e.pesan))
        if args.rinci and p["data"]:
            b.append("Rincian:")
            for s in p["data"]:
                _, nama = m2o(s.get("partner_id"))
                b.append("- {} {}: {}".format(s.get("name"), inisial(nama) if args.samarkan else pendek(nama, 40),
                                              format_rp(uang(s.get("amount_total")))))
        for x in p["mata_uang_lain"]:
            b.append("CATATAN: {} memakai {} ({}) - tidak dijumlahkan.".format(x["nomor"], x["mata_uang"],
                                                                                format_angka(x["total"])))
        out["pesanan"] = {k: v for k, v in p.items() if k not in ("data", "ids")}
        out["pesanan"]["produk_terlaris"] = terlaris or []
    else:
        b += ["", "PESANAN PENJUALAN: tidak bisa dibaca ({})".format(h["galat"]["pesanan"].pesan)]
    if h["faktur"] is not None:
        f = h["faktur"]
        b += ["", "FAKTUR PELANGGAN DIPOSTING (Invoicing)",
              "Faktur: {}{}".format(f["jumlah"], ", nota kredit: {}".format(f["nota_kredit"]) if f["nota_kredit"] else ""),
              "Total (termasuk pajak, dikurangi nota kredit): {}".format(format_rp(f["total"])),
              "Sebelum pajak {} | Pajak {}".format(format_rp(f["dpp"]), format_rp(f["pajak"]))]
        out["faktur"] = f
    else:
        b += ["", "FAKTUR: tidak bisa dibaca ({})".format(h["galat"]["faktur"].pesan)]
    b += ["", "Pesanan dan faktur adalah dua sudut pandang yang sama; JANGAN dijumlahkan (bisa dobel)."]
    if c:
        b.append(c)
    out["teks"] = "\n".join(b)
    return out


# ------------------------------------------------------------------ perintah: piutang
def kelompok_umur(hari):
    if hari <= 0:
        return "belum jatuh tempo"
    if hari <= 30:
        return "1-30 hari"
    if hari <= 60:
        return "31-60 hari"
    if hari <= 90:
        return "61-90 hari"
    return ">90 hari"


URUT_UMUR = ["belum jatuh tempo", "1-30 hari", "31-60 hari", "61-90 hari", ">90 hari"]


def ambil_piutang(api, per_tanggal):
    fk = api.cari("account.move", [["move_type", "=", "out_invoice"], ["state", "=", "posted"],
                                   ["payment_state", "in", ["not_paid", "partial"]]],
                  ["name", "partner_id", "invoice_date", "invoice_date_due", "amount_total_signed",
                   "amount_residual_signed", "payment_state"], order="invoice_date_due asc")
    daftar = []
    for f in fk:
        sisa = uang(f.get("amount_residual_signed"))
        if sisa <= 0:
            continue
        due = tanggal_odoo(f.get("invoice_date_due")) or tanggal_odoo(f.get("invoice_date"))
        hari = (per_tanggal - due).days if due else 0
        pid, nama = m2o(f.get("partner_id"))
        daftar.append({"nomor": f.get("name"), "pelanggan_id": pid, "pelanggan": nama,
                       "tanggal": tanggal_odoo(f.get("invoice_date")), "jatuh_tempo": due,
                       "total": uang(f.get("amount_total_signed")), "sisa": sisa, "hari_lewat": hari,
                       "umur": kelompok_umur(hari), "sebagian": f.get("payment_state") == "partial"})
    kredit = api.cari("account.move", [["move_type", "=", "out_refund"], ["state", "=", "posted"],
                                       ["payment_state", "in", ["not_paid", "partial"]]],
                      ["name", "amount_residual_signed"])
    nilai_kredit = sum((abs(uang(k.get("amount_residual_signed"))) for k in kredit), Decimal(0))
    return daftar, len(kredit), nilai_kredit


def cmd_piutang(api, args, offset):
    per = parse_tanggal(args.per_tanggal, offset)
    daftar, n_kredit, nilai_kredit = ambil_piutang(api, per)
    _, mu = mata_uang_perusahaan(api)
    total = sum((d["sisa"] for d in daftar), Decimal(0))
    telat = [d for d in daftar if d["hari_lewat"] > 0]
    b = ["PIUTANG PELANGGAN ODOO (per {})".format(tanggal_panjang(per)),
         "Belum lunas: {} faktur, {}".format(len(daftar), format_rp(total)),
         "Lewat jatuh tempo: {} faktur, {}".format(len(telat), format_rp(sum((d["sisa"] for d in telat), Decimal(0))))]
    umur = {k: {"jumlah": 0, "nilai": Decimal(0)} for k in URUT_UMUR}
    for d in daftar:
        umur[d["umur"]]["jumlah"] += 1
        umur[d["umur"]]["nilai"] += d["sisa"]
    b += ["", "UMUR PIUTANG (dari tanggal jatuh tempo)"]
    for k in URUT_UMUR:
        b.append("- {}: {} faktur, {}".format(k, umur[k]["jumlah"], format_rp(umur[k]["nilai"])))
    per_pel = {}
    for d in daftar:
        a = per_pel.setdefault(d["pelanggan_id"], {"nama": d["pelanggan"], "sisa": Decimal(0), "faktur": 0,
                                                    "terlama": 0})
        a["sisa"] += d["sisa"]
        a["faktur"] += 1
        a["terlama"] = max(a["terlama"], d["hari_lewat"])
    nama = (lambda n: inisial(n)) if args.samarkan else (lambda n: pendek(n, 40))
    if per_pel:
        b += ["", "PELANGGAN TERBESAR"]
        for a in sorted(per_pel.values(), key=lambda a: (-a["sisa"], a["nama"]))[:5]:
            b.append("- {}: {} ({} faktur{})".format(nama(a["nama"]), format_rp(a["sisa"]), a["faktur"],
                                                     ", terlama lewat {} hari".format(a["terlama"])
                                                     if a["terlama"] > 0 else ""))
    urut = sorted(daftar, key=lambda d: (-d["hari_lewat"], -d["sisa"]))
    if urut:
        b += ["", "RINCIAN (terlama dulu, maks. {})".format(args.maks)]
        for d in urut[: args.maks]:
            ket = "lewat {} hari".format(d["hari_lewat"]) if d["hari_lewat"] > 0 else (
                "jatuh tempo hari ini" if d["hari_lewat"] == 0 else "jatuh tempo {} hari lagi".format(-d["hari_lewat"]))
            b.append("- {} {}: sisa {}{} | tempo {} | {}".format(
                d["nomor"], nama(d["pelanggan"]), format_rp(d["sisa"]), " (dibayar sebagian)" if d["sebagian"] else "",
                d["jatuh_tempo"].isoformat() if d["jatuh_tempo"] else "-", ket))
        if len(urut) > args.maks:
            b.append("... dan {} faktur lain (pakai --maks untuk melihat semua).".format(len(urut) - args.maks))
    else:
        b += ["", "Tidak ada faktur pelanggan yang belum lunas."]
    if n_kredit:
        b.append("CATATAN: ada {} nota kredit belum dipakai, {}; piutang bersih bisa lebih kecil.".format(
            n_kredit, format_rp(nilai_kredit)))
    c = catatan_mata_uang(mu)
    if c:
        b.append(c)
    b.append("Status bayar = kondisi SAAT INI di Odoo. Faktur draf tidak dihitung.")
    keluar = [dict(d, pelanggan=nama(d["pelanggan"])) for d in urut]
    return {"per_tanggal": per, "total": total, "jumlah": len(daftar), "umur": umur, "faktur": keluar,
            "nota_kredit": {"jumlah": n_kredit, "nilai": nilai_kredit}, "teks": "\n".join(b)}


# ------------------------------------------------------------------ perintah: stok-menipis
def domain_barang_stok(api):
    """Odoo 18+: is_storable = True. Odoo 16-17: type = 'product'."""
    if api.punya_field("product.product", "is_storable"):
        return [["is_storable", "=", True]]
    return [["type", "=", "product"]]


def ambil_stok_menipis(api):
    try:
        op = api.cari("stock.warehouse.orderpoint", [], ["product_id", "location_id", "product_min_qty",
                                                          "product_max_qty", "qty_on_hand", "qty_forecast"])
    except Gagal as e:
        if e.kode == KELUAR_MODUL:
            raise Gagal("Aplikasi Inventori (stok) Odoo belum terpasang atau tidak bisa dibaca, jadi stok TIDAK dinilai.",
                        KELUAR_MODUL, saran="Pasang aplikasi Inventory di Odoo bila ingin memantau stok.")
        raise
    perhatian, dengan_aturan = [], set()
    for o in op:
        pid, nama = m2o(o.get("product_id"))
        dengan_aturan.add(pid)
        mn, mx = desimal(o.get("product_min_qty")), desimal(o.get("product_max_qty"))
        ada, perkiraan = desimal(o.get("qty_on_hand")), desimal(o.get("qty_forecast"))
        if ada < 0:
            status = "MINUS"
        elif ada <= 0:
            status = "HABIS"
        elif ada < mn:
            status = "MENIPIS"
        elif perkiraan < mn:
            status = "PERKIRAAN DI BAWAH MINIMUM"
        else:
            continue
        target = mx if mx > mn else mn
        saran = max(target - perkiraan, Decimal(0))
        perhatian.append({"produk_id": pid, "produk": nama, "lokasi": m2o(o.get("location_id"))[1], "stok": ada,
                          "perkiraan": perkiraan, "minimum": mn, "maksimum": mx, "status": status,
                          "saran_pesan": saran, "aturan": True})
    habis = api.cari("product.product", domain_barang_stok(api) + [["qty_available", "<=", 0]],
                     ["display_name", "default_code", "qty_available", "virtual_available"], batas=500)
    tanpa_aturan = []
    for p in habis:
        if p["id"] in dengan_aturan:
            continue
        ada = desimal(p.get("qty_available"))
        tanpa_aturan.append({"produk_id": p["id"], "produk": teks_odoo(p.get("display_name")), "stok": ada,
                             "perkiraan": desimal(p.get("virtual_available")),
                             "status": "MINUS" if ada < 0 else "HABIS", "aturan": False})
    urut = {"MINUS": 0, "HABIS": 1, "MENIPIS": 2, "PERKIRAAN DI BAWAH MINIMUM": 3}
    perhatian.sort(key=lambda x: (urut[x["status"]], x["produk"]))
    tanpa_aturan.sort(key=lambda x: (urut[x["status"]], x["produk"]))
    return perhatian, tanpa_aturan, len(op)


def cmd_stok_menipis(api, args):
    perhatian, tanpa, n_aturan = ambil_stok_menipis(api)
    b = ["STOK PERLU PERHATIAN (ODOO)",
         "Aturan stok minimum (Reordering Rules) terbaca: {}".format(n_aturan)]
    if perhatian:
        b += ["", "DENGAN ATURAN MINIMUM"]
        for x in perhatian[: args.maks]:
            b.append("- {}: stok {} ({}), perkiraan {}, min {}{} -> saran pesan {}".format(
                pendek(x["produk"], 50), format_angka(x["stok"]), x["status"], format_angka(x["perkiraan"]),
                format_angka(x["minimum"]), ", maks {}".format(format_angka(x["maksimum"])) if x["maksimum"] > x["minimum"]
                else "", format_angka(x["saran_pesan"])))
        if len(perhatian) > args.maks:
            b.append("... dan {} lainnya.".format(len(perhatian) - args.maks))
    else:
        b += ["", "Semua barang yang punya aturan minimum masih aman."]
    if tanpa:
        b += ["", "HABIS/MINUS TANPA ATURAN MINIMUM"]
        for x in tanpa[: args.maks]:
            b.append("- {}: stok {} ({}){}".format(pendek(x["produk"], 50), format_angka(x["stok"]), x["status"],
                                                   ", perkiraan {}".format(format_angka(x["perkiraan"]))
                                                   if x["perkiraan"] != x["stok"] else ""))
        if len(tanpa) > args.maks:
            b.append("... dan {} lainnya.".format(len(tanpa) - args.maks))
    if n_aturan == 0:
        b.append("CATATAN: belum ada aturan stok minimum. Atur di Odoo: Inventori > Konfigurasi/Operasi > Aturan "
                 "Pemesanan Ulang (Reordering Rules) agar 'menipis' bisa dinilai.")
    b.append("Rumus: saran pesan = (maksimum bila diisi, selain itu minimum) - stok perkiraan (forecast), minimal 0.")
    return {"aturan_terbaca": n_aturan, "perhatian": perhatian, "habis_tanpa_aturan": tanpa, "teks": "\n".join(b)}


# ------------------------------------------------------------------ perintah: cari pelanggan / produk
def norm_hp(teks):
    d = re.sub(r"\D", "", str(teks or ""))
    if d.startswith("62"):
        d = "0" + d[2:]
    return d


def cmd_pelanggan_cari(api, args):
    kata = args.kata.strip()
    if len(kata) < 2:
        raise Gagal("Kata pencarian minimal 2 huruf.", KELUAR_ARG)
    f_telp = ["phone"] + (["mobile"] if api.punya_field("res.partner", "mobile") else [])
    hp = norm_hp(kata)
    fields = ["name", "email", "city"] + f_telp
    if len(hp) >= 8 and re.fullmatch(r"[\d\s+\-().]+", kata):
        # Nomor HP: Odoo menyimpan apa adanya (0812-..., +62 812 ...). Saring kasar dengan 4 digit terakhir,
        # lalu cocokkan digit ternormalisasi (62/+62 -> 0) di script.
        domain = ["|"] * (len(f_telp) - 1) + [[f, "ilike", hp[-4:]] for f in f_telp]
        kasar = api.cari("res.partner", domain, fields, order="name asc", batas=500)
        rows = [r for r in kasar if any(norm_hp(r.get(f)).endswith(hp[-9:]) or norm_hp(r.get(f)) == hp
                                        for f in f_telp if r.get(f))][:21]
    else:
        domain = ["|"] * (1 + len(f_telp)) + [["name", "ilike", kata], ["email", "ilike", kata]] + \
                 [[f, "ilike", kata] for f in f_telp]
        rows = api.cari("res.partner", domain, fields, order="name asc", batas=21)
    b = ["PELANGGAN ODOO cocok '{}': {}{}".format(kata, min(len(rows), 20), "+" if len(rows) > 20 else "")]
    hasil = []
    for r in rows[:20]:
        telp = next((teks_odoo(r.get(f)) for f in f_telp if r.get(f)), "")
        hasil.append({"id": r["id"], "nama": teks_odoo(r.get("name")), "telepon": samarkan_hp(telp),
                      "email": samarkan_email(r.get("email")), "kota": teks_odoo(r.get("city"))})
        h = hasil[-1]
        b.append("- ID {}: {}{}{}{}".format(h["id"], h["nama"], " | " + h["telepon"] if h["telepon"] else "",
                                            " | " + h["email"] if h["email"] else "", " | " + h["kota"] if h["kota"] else ""))
    if not rows:
        b.append("Tidak ada yang cocok. Pelanggan baru dibuat manusia di Odoo (Penjualan > Pelanggan).")
    if len(rows) > 20:
        b.append("Terlalu banyak hasil; perjelas kata pencarian.")
    b.append("(Nomor HP & email disamarkan.)")
    return {"hasil": hasil, "teks": "\n".join(b)}


def cmd_produk_cari(api, args):
    kata = args.kata.strip()
    if len(kata) < 2:
        raise Gagal("Kata pencarian minimal 2 huruf.", KELUAR_ARG)
    ada_stok = api.punya_field("product.product", "qty_available")
    fields = ["display_name", "default_code", "list_price", "sale_ok"] + (["qty_available"] if ada_stok else [])
    rows = api.cari("product.product", ["|", "|", ["default_code", "ilike", kata], ["name", "ilike", kata],
                                        ["barcode", "ilike", kata]], fields, order="default_code asc", batas=21)
    b = ["PRODUK ODOO cocok '{}': {}{}".format(kata, min(len(rows), 20), "+" if len(rows) > 20 else "")]
    hasil = []
    for r in rows[:20]:
        h = {"id": r["id"], "kode": teks_odoo(r.get("default_code")), "nama": teks_odoo(r.get("display_name")),
             "harga_jual": uang(r.get("list_price")), "bisa_dijual": bool(r.get("sale_ok"))}
        if ada_stok:
            h["stok"] = desimal(r.get("qty_available"))
        hasil.append(h)
        b.append("- #{} {}: harga jual {}{}{}".format(h["id"], h["nama"], format_rp(h["harga_jual"]),
                                                     ", stok {}".format(format_angka(h["stok"])) if ada_stok else "",
                                                     "" if h["bisa_dijual"] else " (TIDAK untuk dijual)"))
    if not rows:
        b.append("Tidak ada yang cocok.")
    return {"hasil": hasil, "teks": "\n".join(b)}


# ------------------------------------------------------------------ perintah: quotation buat (DRAF)
def parse_item(teks, nomor):
    """'KODE_ATAU_NAMA|jumlah[|harga[|diskon%]]'. Harga = sebelum pajak; kosong = harga jual di Odoo."""
    bagian = [x.strip() for x in str(teks).split("|")]
    if len(bagian) < 2 or not bagian[0]:
        raise Gagal("Item {} '{}' tidak lengkap. Format: \"KODE atau nama produk|jumlah[|harga[|diskon%]]\"."
                    .format(nomor, teks), KELUAR_ARG)
    if len(bagian) > 4:
        raise Gagal("Item {} '{}' punya terlalu banyak bagian '|'.".format(nomor, teks), KELUAR_ARG)
    item = {"nomor": nomor, "ref": bagian[0].lstrip("@").strip(), "harga": None, "diskon": Decimal(0)}
    item["qty"] = angka_id(bagian[1], "jumlah", BATAS_JUMLAH, nomor)
    if item["qty"] == 0:
        raise Gagal("Item {}: jumlah tidak boleh 0.".format(nomor), KELUAR_ARG)
    if len(bagian) >= 3 and bagian[2]:
        item["harga"] = angka_id(bagian[2], "harga", BATAS_HARGA, nomor)
    if len(bagian) == 4 and bagian[3]:
        item["diskon"] = angka_id(bagian[3].rstrip("%"), "diskon", Decimal(100), nomor)
    return item


def cari_produk_item(api, item):
    ref = item["ref"]
    fields = ["display_name", "default_code", "list_price", "sale_ok"]
    if re.fullmatch(r"#\d+", ref):
        rows = api.cari("product.product", [["id", "=", int(ref[1:])]], fields, batas=1)
    else:
        rows = api.cari("product.product", [["default_code", "=", ref]], fields, batas=5)
        if not rows:
            rows = api.cari("product.product", [["name", "=ilike", ref]], fields, batas=5)
        if not rows:
            rows = api.cari("product.product", ["|", ["name", "ilike", ref], ["default_code", "ilike", ref]], fields,
                            batas=6)
    if not rows:
        raise Gagal("Item {}: produk '{}' tidak ditemukan di Odoo.".format(item["nomor"], ref), KELUAR_ARG,
                    saran="Cari dulu dengan `produk cari`. Produk baru dibuat manusia di Odoo.")
    if len(rows) > 1:
        pilihan = "; ".join("#{} {}".format(r["id"], r.get("display_name")) for r in rows[:5])
        raise Gagal("Item {}: '{}' cocok ke beberapa produk: {}. Tanyakan yang mana, lalu pakai #id.".format(
            item["nomor"], ref, pilihan), KELUAR_DOBEL)
    return rows[0]


def hitung_quotation(items, jenis_ppn):
    dpp = Decimal(0)
    for it in items:
        it["subtotal"] = rupiah_bulat(it["qty"] * it["harga"] * (Decimal(100) - it["diskon"]) / Decimal(100))
        dpp += it["subtotal"]
    ppn = (dpp * PPN[jenis_ppn]["efektif"]).quantize(Decimal(1), ROUND_FLOOR)
    return {"dpp": dpp, "dpp_nilai_lain": (dpp * Decimal(11) / Decimal(12)).quantize(Decimal("0.01"), ROUND_HALF_UP),
            "ppn": ppn, "total": dpp + ppn}


def kode_perintah(pid, items, tempo):
    mentah = json.dumps([pid, tempo, [[i["produk_id"], str(i["qty"]), str(i["harga"]), str(i["diskon"])]
                                      for i in items]], sort_keys=True)
    return hashlib.sha256(mentah.encode("utf-8")).hexdigest()[:10]


def cmd_quotation_buat(api, args, offset):
    if not args.item:
        raise Gagal("Belum ada item. Contoh: --item \"KP-250|3\" --item \"Gula Aren 1kg|2|32500\".", KELUAR_ARG)
    if len(args.item) > 100:
        raise Gagal("Maksimal 100 item per quotation.", KELUAR_ARG)
    if not 0 <= args.berlaku <= 365:
        raise Gagal("--berlaku harus 0 sampai 365 hari.", KELUAR_ARG)
    items = [parse_item(t, i) for i, t in enumerate(args.item, 1)]
    pel = api.cari("res.partner", [["id", "=", args.pelanggan]], ["name"], batas=1)
    if not pel:
        raise Gagal("Pelanggan ID {} tidak ditemukan. Cari dulu dengan `pelanggan cari`.".format(args.pelanggan),
                    KELUAR_ARG)
    nama_pel = teks_odoo(pel[0].get("name"))
    catatan = []
    for it in items:
        p = cari_produk_item(api, it)
        it["produk_id"], it["produk"] = p["id"], teks_odoo(p.get("display_name"))
        if it["harga"] is None:
            it["harga"] = uang(p.get("list_price"))
            it["harga_dari_odoo"] = True
        if not p.get("sale_ok"):
            catatan.append("Item {}: produk '{}' ditandai TIDAK untuk dijual di Odoo.".format(it["nomor"], it["produk"]))
    hit = hitung_quotation(items, args.ppn)
    tgl = hari_ini(offset)
    kode = kode_perintah(args.pelanggan, items, args.berlaku)
    b = ["{} DRAF QUOTATION ODOO".format("MEMBUAT" if args.ya else "PRATINJAU"),
         "Pelanggan: {} (ID {})".format(nama_pel, args.pelanggan),
         "Berlaku sampai: {}".format((tgl + dt.timedelta(days=args.berlaku)).isoformat()) if args.berlaku else
         "Berlaku sampai: (default Odoo)"]
    for it in items:
        b.append("{}. {}: {} x {}{}{} = {}".format(
            it["nomor"], it["produk"], format_angka(it["qty"]), format_rp(it["harga"]),
            " (harga jual Odoo)" if it.get("harga_dari_odoo") else "",
            " diskon {}%".format(format_angka(it["diskon"])) if it["diskon"] else "", format_rp(it["subtotal"])))
    b += ["Subtotal sebelum pajak (DPP): {}".format(format_rp(hit["dpp"])),
          "Perkiraan pajak standar Komunitech ({}): {}".format(PPN[args.ppn]["label"], format_rp(hit["ppn"])),
          "Perkiraan total: {}".format(format_rp(hit["total"])),
          "Pajak final dihitung Odoo dari pengaturan pajak produk/pelanggan (bisa berbeda; akan dicocokkan)."]
    b.extend("CATATAN: " + c for c in catatan)
    out = {"pelanggan_id": args.pelanggan, "pelanggan": nama_pel, "kode_perintah": kode,
           "item": [{k: it[k] for k in ("nomor", "produk_id", "produk", "qty", "harga", "diskon", "subtotal")}
                    for it in items], "hitung": hit, "dibuat": False}
    # Cegah dobel: draf dari perintah sama, atau draf AI hari ini ke pelanggan sama dengan DPP sama
    awal, _ = rentang_utc(tgl, offset)
    draf = api.cari("sale.order", [["state", "=", "draft"], ["partner_id", "=", args.pelanggan],
                                   ["origin", "ilike", PENANDA]], ["name", "origin", "amount_untaxed", "create_date"],
                    batas=50)
    kembar = [d for d in draf if kode in teks_odoo(d.get("origin")) or
              (teks_odoo(d.get("create_date")) >= awal and abs(uang(d.get("amount_untaxed")) - hit["dpp"]) < 1)]
    if kembar and not args.tetap_buat:
        b += ["", "DRAF TIDAK DIBUAT: sudah ada draf quotation serupa untuk pelanggan ini:"]
        b.extend("- {} (sebelum pajak {})".format(d.get("name"), format_rp(uang(d.get("amount_untaxed")))) for d in kembar)
        b.append("Periksa draf itu di Odoo. Bila memang perlu draf baru, ulangi dengan --tetap-buat.")
        out["kembar"] = [d.get("name") for d in kembar]
        out["kode_keluar"] = KELUAR_DOBEL
        out["teks"] = "\n".join(b)
        return out
    if not args.ya:
        b += ["", "Belum disimpan. Jika sudah benar dan pengguna menjawab ya, ulangi perintah yang sama dengan --ya."]
        out["teks"] = "\n".join(b)
        return out
    vals = {"partner_id": args.pelanggan, "origin": "{} {}".format(PENANDA, kode),
            "order_line": [[0, 0, {"product_id": it["produk_id"], "product_uom_qty": float(it["qty"]),
                                   "price_unit": float(it["harga"]), "discount": float(it["diskon"])}]
                           for it in items]}
    if args.berlaku:
        vals["validity_date"] = (tgl + dt.timedelta(days=args.berlaku)).isoformat()
    try:
        baru = api.panggil("sale.order", "create", vals_list=[vals])
    except Gagal as e:
        if not e.mungkin_terkirim:
            raise
        b += ["", "BELUM PASTI TERBUAT: {}".format(e.pesan)]
        try:
            ada = api.cari("sale.order", [["origin", "ilike", kode]], ["name", "state"], batas=5)
            if ada:
                b.append("Hasil cek ulang: draf SUDAH ADA di Odoo: {}. Jangan ulangi perintah.".format(
                    ", ".join(teks_odoo(a.get("name")) for a in ada)))
            else:
                b.append("Hasil cek ulang: draf belum terlihat di Odoo. Tunggu 1 menit, cek menu Penjualan > "
                         "Penawaran (cari '{}'), baru putuskan mengulang.".format(kode))
        except Gagal as e2:
            b.append("Cek ulang gagal ({}). Cek manual di Odoo: Penjualan > Penawaran, cari '{}'.".format(e2.pesan, kode))
        out["kode_keluar"] = KELUAR_TIDAK_PASTI
        out["teks"] = "\n".join(b)
        return out
    so_id = baru[0] if isinstance(baru, list) else baru
    out["dibuat"], out["id"] = True, so_id
    try:
        so = api.panggil("sale.order", "read", [so_id], fields=["name", "state", "amount_untaxed", "amount_tax",
                                                                 "amount_total"])[0]
    except (Gagal, IndexError, TypeError) as e:
        b += ["", "TERSIMPAN sebagai draf (ID {}), tetapi gagal dibaca ulang ({}). Periksa di Odoo.".format(
            so_id, getattr(e, "pesan", type(e).__name__))]
        out["teks"] = "\n".join(b)
        return out
    o_dpp, o_pajak, o_total = uang(so.get("amount_untaxed")), uang(so.get("amount_tax")), uang(so.get("amount_total"))
    cocok_dpp = abs(o_dpp - hit["dpp"]) < 1
    cocok_pajak = abs(o_pajak - hit["ppn"]) < 1
    out["odoo"] = {"nomor": so.get("name"), "status": so.get("state"), "dpp": o_dpp, "pajak": o_pajak, "total": o_total,
                   "cocok_dpp": cocok_dpp, "cocok_pajak": cocok_pajak}
    b += ["", "TERSIMPAN: {} (ID {}), status {}".format(so.get("name"), so_id,
                                                        "DRAF/Penawaran" if so.get("state") == "draft" else so.get("state")),
          "Menurut Odoo: sebelum pajak {} | pajak {} | total {}".format(format_rp(o_dpp), format_rp(o_pajak),
                                                                       format_rp(o_total)),
          "Sebelum pajak: {}".format("COCOK" if cocok_dpp else "BEDA {} (harga termasuk pajak di produk, atau "
                                     "pembulatan Odoo)".format(format_rp(o_dpp - hit["dpp"]))),
          "Pajak: {}".format("COCOK" if cocok_pajak else "BEDA {} dari perkiraan standar Komunitech (Odoo memakai pajak "
                             "yang diatur di produk/posisi fiskal; periksa)".format(format_rp(o_pajak - hit["ppn"])))]
    b.append("Draf belum dikirim ke pelanggan. Periksa di Odoo (Penjualan > Penawaran), lalu klik Kirim/Konfirmasi "
             "sendiri bila sudah benar.")
    out["teks"] = "\n".join(b)
    return out


# ------------------------------------------------------------------ perintah: laporan-harian
def cmd_laporan_harian(api, args, offset):
    tgl = parse_tanggal(args.tanggal, offset)
    per = hari_ini(offset) if args.tanggal in (None, "hari-ini") else tgl
    b = ["LAPORAN HARIAN ODOO", tanggal_panjang(tgl)]
    perhatian, galat, out = [], [], {"tanggal": tgl}
    mu_id, mu = mata_uang_perusahaan(api)
    h = ambil_penjualan(api, tgl, offset, mu_id)
    kmrn = ambil_penjualan(api, tgl - dt.timedelta(days=1), offset, mu_id)
    b += ["", "PENJUALAN"]
    if h["pesanan"] is not None:
        p = h["pesanan"]
        pr = persen_ubah(p["total"], kmrn["pesanan"]["total"]) if kmrn["pesanan"] is not None else None
        b.append("Pesanan terkonfirmasi: {}, total {}{}".format(
            p["jumlah"], format_rp(p["total"]), "" if pr is None else " ({}{}% vs kemarin)".format(
                "+" if pr > 0 else "", format_angka(pr))))
        b.append("Sebelum pajak {} | Pajak {}".format(format_rp(p["dpp"]), format_rp(p["pajak"])))
        terlaris, _ = _panggil_baca_saja(produk_terlaris, api, p["ids"], 3)
        if terlaris:
            b.append("Terlaris: " + "; ".join("{} ({})".format(pendek(t["nama"], 30), format_angka(t["qty"]))
                                              for t in terlaris))
        out["pesanan"] = {k: v for k, v in p.items() if k not in ("data", "ids")}
    else:
        galat.append(h["galat"]["pesanan"])
        b.append("Pesanan: tidak bisa dibaca ({})".format(h["galat"]["pesanan"].pesan))
    if h["faktur"] is not None:
        f = h["faktur"]
        b.append("Faktur diposting: {}{}, total {}".format(
            f["jumlah"], " (+{} nota kredit)".format(f["nota_kredit"]) if f["nota_kredit"] else "", format_rp(f["total"])))
        out["faktur"] = f
    else:
        galat.append(h["galat"]["faktur"])
        b.append("Faktur: tidak bisa dibaca ({})".format(h["galat"]["faktur"].pesan))
    b += ["", "PIUTANG (per {})".format(per.isoformat())]
    try:
        daftar, n_kredit, _ = ambil_piutang(api, per)
        telat = sorted([d for d in daftar if d["hari_lewat"] > 0], key=lambda d: (-d["hari_lewat"], -d["sisa"]))
        b.append("Belum lunas: {} faktur, {}".format(len(daftar), format_rp(sum((d["sisa"] for d in daftar), Decimal(0)))))
        b.append("Lewat jatuh tempo: {} faktur, {}".format(len(telat),
                                                           format_rp(sum((d["sisa"] for d in telat), Decimal(0)))))
        for d in telat[:3]:
            b.append("- {} ({}) sisa {}, lewat {} hari".format(d["nomor"], inisial(d["pelanggan"]), format_rp(d["sisa"]),
                                                              d["hari_lewat"]))
        if len(telat) > 3:
            b.append("- ... {} faktur telat lainnya".format(len(telat) - 3))
        if any(d["hari_lewat"] > 60 for d in telat):
            perhatian.append("Ada faktur lewat 60+ hari. Rincian & nama pelanggan: perintah `piutang`.")
        elif telat:
            perhatian.append("Ada {} faktur terlambat. Rincian: perintah `piutang`.".format(len(telat)))
        out["piutang"] = {"jumlah": len(daftar), "telat": len(telat)}
    except Gagal as e:
        galat.append(e)
        b.append("Tidak bisa dibaca ({})".format(e.pesan))
    b += ["", "STOK"]
    try:
        stok, tanpa, _ = ambil_stok_menipis(api)
        semua = stok + tanpa
        if not semua:
            b.append("Tidak ada stok habis/menipis.")
        for x in semua[:5]:
            b.append("- {}: {} ({})".format(pendek(x["produk"], 40), format_angka(x["stok"]), x["status"]))
        if len(semua) > 5:
            b.append("- ... {} barang lainnya (perintah `stok-menipis`)".format(len(semua) - 5))
        n_habis = sum(1 for x in semua if x["status"] in ("HABIS", "MINUS"))
        if n_habis:
            perhatian.append("{} barang habis/minus. Cek pembelian.".format(n_habis))
        out["stok"] = {"perhatian": len(semua), "habis": n_habis}
    except Gagal as e:
        galat.append(e)
        b.append("Tidak bisa dibaca ({})".format(e.pesan))
    if perhatian:
        b += ["", "PERLU PERHATIAN"]
        b.extend("{}. {}".format(i, x) for i, x in enumerate(perhatian, 1))
    c = catatan_mata_uang(mu)
    if c:
        b.append(c)
    b.append("(Nama pelanggan disamarkan. Angka dihitung script dari Odoo.)")
    teks = "\n".join(b)
    if len(teks) > MAKS_TELEGRAM:
        teks = teks[: MAKS_TELEGRAM - 40].rsplit("\n", 1)[0] + "\n... (dipotong; batas pesan Telegram)"
    out["teks"] = teks
    # Satu bagian gagal -> bagian lain tetap dikirim (kode 0). SEMUA bagian gagal -> kode bukan 0 (jadwal tercatat gagal).
    if h["pesanan"] is None and h["faktur"] is None and "piutang" not in out and "stok" not in out:
        out["kode_keluar"] = galat[0].kode
    return out


# ------------------------------------------------------------------ argparse & main
def buat_opsi_umum():
    u = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    u.add_argument("--url", help="Alamat Odoo (default: konfigurasi / ENV ODOO_URL / {})".format(URL_DEFAULT))
    u.add_argument("--db", help="Nama database Odoo (ENV ODOO_DB)")
    u.add_argument("--login", help="Login pengguna API untuk XML-RPC (ENV ODOO_LOGIN)")
    u.add_argument("--kunci-file", help="File kunci API (menang atas ENV ODOO_API_KEY)")
    u.add_argument("--protokol", choices=["otomatis", "xmlrpc", "json2"], help="Default otomatis")
    u.add_argument("--tz", help="WIB (default), WITA, atau WIT")
    u.add_argument("--timeout", type=float, help="Batas tunggu per permintaan, detik (default 20)")
    u.add_argument("--json", action="store_true", help="Keluaran JSON untuk agent")
    return u


def buat_parser():
    umum = buat_opsi_umum()
    ap = argparse.ArgumentParser(prog="odoo.py", allow_abbrev=False,
                                 description="Asisten Odoo (Komunitech). Default hanya baca; menulis hanya DRAF quotation.")
    sub = ap.add_subparsers(dest="perintah")
    at = sub.add_parser("atur", parents=[umum], allow_abbrev=False, help="Simpan konfigurasi NON-rahasia (url, db, login)")
    at.add_argument("--izinkan-host", action="store_true", help="Tambahkan host dari --url ke daftar host yang diizinkan")
    sk = sub.add_parser("simpan-kunci", parents=[umum], allow_abbrev=False, help="Simpan kunci API (izin 600)")
    sk.add_argument("--ya", action="store_true", help="Izinkan menimpa file kunci yang sudah ada")
    sub.add_parser("cek", parents=[umum], allow_abbrev=False, help="Cek koneksi, versi, hak akses")
    pj = sub.add_parser("penjualan", parents=[umum], allow_abbrev=False, help="Ringkasan penjualan per tanggal")
    pj.add_argument("--tanggal", default="hari-ini")
    pj.add_argument("--rinci", action="store_true", help="Tampilkan daftar pesanan")
    pj.add_argument("--samarkan", action="store_true", help="Nama pelanggan jadi inisial")
    pi = sub.add_parser("piutang", parents=[umum], allow_abbrev=False, help="Faktur belum lunas + umur piutang")
    pi.add_argument("--per-tanggal", default="hari-ini")
    pi.add_argument("--samarkan", action="store_true", help="Nama pelanggan jadi inisial")
    pi.add_argument("--maks", type=int, default=30)
    st = sub.add_parser("stok-menipis", parents=[umum], allow_abbrev=False, help="Stok habis/menipis + saran pesan")
    st.add_argument("--maks", type=int, default=50)
    pl = sub.add_parser("pelanggan", allow_abbrev=False, help="Cari pelanggan")
    pls = pl.add_subparsers(dest="aksi")
    plc = pls.add_parser("cari", parents=[umum], allow_abbrev=False)
    plc.add_argument("kata")
    pr = sub.add_parser("produk", allow_abbrev=False, help="Cari produk")
    prs = pr.add_subparsers(dest="aksi")
    prc = prs.add_parser("cari", parents=[umum], allow_abbrev=False)
    prc.add_argument("kata")
    qt = sub.add_parser("quotation", allow_abbrev=False, help="Buat DRAF quotation (penawaran)")
    qts = qt.add_subparsers(dest="aksi")
    qb = qts.add_parser("buat", parents=[umum], allow_abbrev=False)
    qb.add_argument("--pelanggan", type=int, required=True, help="ID pelanggan (dari `pelanggan cari`)")
    qb.add_argument("--item", action="append", help="\"KODE atau nama|jumlah[|harga[|diskon%%]]\" (harga sebelum pajak)")
    qb.add_argument("--berlaku", type=int, default=14, help="Masa berlaku penawaran, hari (default 14; 0 = default Odoo)")
    qb.add_argument("--ppn", choices=sorted(PPN), default="umum", help="Pembanding pajak: umum (default), mewah, tanpa")
    qb.add_argument("--ya", action="store_true", help="Benar-benar simpan draf (tanpa ini hanya pratinjau)")
    qb.add_argument("--tetap-buat", action="store_true", help="Tetap buat walau ada draf serupa")
    lh = sub.add_parser("laporan-harian", parents=[umum], allow_abbrev=False, help="Laporan harian untuk Telegram pemilik")
    lh.add_argument("--tanggal", default="hari-ini")
    return ap


def main(argv=None):
    ap = buat_parser()
    args = ap.parse_args(argv)
    if not args.perintah or (args.perintah in ("pelanggan", "produk", "quotation") and not getattr(args, "aksi", None)):
        ap.print_help()
        return KELUAR_ARG
    try:
        if args.perintah == "simpan-kunci":
            hasil = cmd_simpan_kunci(args)
        elif args.perintah == "atur":
            hasil = cmd_atur(args)
        else:
            konfig, peringatan = baca_konfig()
            for p in peringatan:
                cetak(p, file=sys.stderr)
            tz = args.tz or os.environ.get("ODOO_TZ") or konfig.get("tz") or "WIB"
            offset = zona_offset(tz)
            timeout = args.timeout if args.timeout is not None else BATAS_WAKTU
            if not 0.1 <= timeout <= 120:
                raise Gagal("--timeout harus 0,1 sampai 120 detik.", KELUAR_ARG)
            for nama in ("maks",):
                if hasattr(args, nama) and not 1 <= getattr(args, nama) <= 1000:
                    raise Gagal("--maks harus 1 sampai 1000.", KELUAR_ARG)
            izin = list(konfig.get("host_diizinkan") or []) + \
                [h for h in (os.environ.get("ODOO_HOST_DIIZINKAN") or "").split(",") if h.strip()]
            url, _, tanpa_proxy, catatan_url = cek_url(
                args.url or os.environ.get("ODOO_URL") or konfig.get("url") or URL_DEFAULT, izin)
            db = args.db or os.environ.get("ODOO_DB") or konfig.get("db") or ""
            login = args.login or os.environ.get("ODOO_LOGIN") or konfig.get("login") or ""
            protokol = args.protokol or os.environ.get("ODOO_PROTOKOL") or konfig.get("protokol") or "otomatis"
            if protokol not in ("otomatis", "xmlrpc", "json2"):
                raise Gagal("Protokol '{}' tidak dikenal (otomatis/xmlrpc/json2).".format(protokol), KELUAR_ARG)
            kunci, sumber, peringatan_kunci = baca_kunci(args.kunci_file)
            if peringatan_kunci:
                cetak(peringatan_kunci, file=sys.stderr)
            for c in catatan_url:
                cetak(c, file=sys.stderr)
            api = Odoo(url, db, login, kunci, protokol, tanpa_proxy, timeout).mulai()
            if args.perintah == "cek":
                hasil = cmd_cek(api, args, catatan_url, sumber)
            elif args.perintah == "penjualan":
                hasil = cmd_penjualan(api, args, offset)
            elif args.perintah == "piutang":
                hasil = cmd_piutang(api, args, offset)
            elif args.perintah == "stok-menipis":
                hasil = cmd_stok_menipis(api, args)
            elif args.perintah == "pelanggan":
                hasil = cmd_pelanggan_cari(api, args)
            elif args.perintah == "produk":
                hasil = cmd_produk_cari(api, args)
            elif args.perintah == "quotation":
                hasil = cmd_quotation_buat(api, args, offset)
            else:
                hasil = cmd_laporan_harian(api, args, offset)
    except Gagal as e:
        if getattr(args, "json", False):
            cetak(json.dumps({"ok": False, "kode_keluar": e.kode, "galat": e.pesan, "saran": e.saran},
                             ensure_ascii=False, indent=2))
        else:
            cetak("GAGAL: " + e.pesan, file=sys.stderr)
            if e.saran:
                cetak("Saran: " + e.saran, file=sys.stderr)
        return e.kode
    except KeyboardInterrupt:
        cetak("DIBATALKAN oleh pengguna.", file=sys.stderr)
        return KELUAR_LAIN
    except Exception as e:  # jangan pernah traceback (bisa memuat kunci)
        pesan = "Galat tak terduga ({}): {}".format(type(e).__name__, str(e)[:200])
        if getattr(args, "json", False):
            cetak(json.dumps({"ok": False, "kode_keluar": KELUAR_LAIN, "galat": pesan}, ensure_ascii=False))
        else:
            cetak("GAGAL: " + pesan, file=sys.stderr)
            cetak("Saran: jalankan `cek`; bila tetap gagal, kirim pesan ini (tanpa kunci) ke dukungan Komunitech.",
                  file=sys.stderr)
        return KELUAR_LAIN
    kode = hasil.get("kode_keluar", 0)
    if args.json:
        hasil["ok"] = kode == 0
        cetak(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2))
    else:
        cetak(hasil["teks"])
    return kode


if __name__ == "__main__":
    sys.exit(main())
