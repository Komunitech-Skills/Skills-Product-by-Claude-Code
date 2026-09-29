#!/usr/bin/env python3
"""umami-analitik (Komunitech) - laporan analitik web dari Umami milik pengguna sendiri.

Umami = analitik web open-source (MIT), tanpa cookie, pengganti Google Analytics yang dipasang di
komputer/server milik pengguna. Script ini hanya MEMBACA data lewat REST API resmi Umami
(header 'Authorization: Bearer <kunci API umami_...>'). Python standar saja, tanpa paket tambahan.

Perintah:
  simpan-kunci    simpan kunci API (atau sandi) Umami ke file lokal (dibaca tersembunyi, tidak dicetak)
  simpan-alamat   simpan alamat server Umami (mis. https://analitik.tokosaya.id) ke file lokal
  cek             cek server, akun, dan daftar website yang bisa dibaca
  situs           daftar website (nama, domain, id)
  ringkasan       pengunjung, kunjungan, tayangan, bounce, rata-rata lama per periode (+ pembanding)
  halaman         halaman teratas (tayangan & pengunjung), atau halaman masuk/keluar
  sumber          sumber trafik: kanal (sosial/pencarian/langsung) + situs perujuk (referrer)
  utm             kampanye UTM: sumber, medium, kampanye, konten
  pengunjung      perangkat, negara, kota (+ browser, sistem operasi, bahasa)
  banding         minggu ini vs minggu lalu (atau periode lain) berdampingan
  konversi        event konversi (klik WA, beli, dll) + data event (produk, nilai)
  tautan          klik tautan pelacak Umami (Links: bio IG/TikTok, QR, tombol WA) per periode
  ekspor-csv      ekspor semua angka periode ke CSV (siap Excel)
  laporan-mingguan  ringkasan satu pesan untuk Telegram (jadwal OpenClaw)

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

VERSI = "1.0.0"
UMAMI_TERUJI = "3.4.0"
FOLDER_KUNCI = os.path.join(os.path.expanduser("~"), ".komunitech")
KUNCI_DEFAULT = os.path.join(FOLDER_KUNCI, "umami-kunci.txt")
ALAMAT_DEFAULT = os.path.join(FOLDER_KUNCI, "umami-alamat.txt")
URL_DEFAULT = "http://localhost:3000"

K_INPUT, K_FILE, K_KONEKSI, K_AUTH, K_GANDA = 2, 3, 4, 5, 7

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
TZ = {"WIB": (7, "Asia/Jakarta"), "WITA": (8, "Asia/Makassar"), "WIT": (9, "Asia/Jayapura")}
PERIODE = ["hari-ini", "kemarin", "7hari", "30hari", "minggu-ini", "minggu-lalu", "bulan-ini", "bulan-lalu"]
KANAL = {
    "direct": "Langsung (termasuk WA/aplikasi tanpa UTM)",
    "organicSocial": "Media sosial (organik)", "paidSocial": "Media sosial (iklan)",
    "organicSearch": "Pencarian Google dll (organik)", "paidSearch": "Pencarian (iklan)",
    "paidAds": "Iklan (gclid/fbclid/ttclid)", "referral": "Situs lain (rujukan)", "email": "Email",
    "sms": "SMS", "affiliate": "Afiliasi", "llm": "Asisten AI (ChatGPT dll)",
    "organicVideo": "Video (organik)", "paidVideo": "Video (iklan)",
    "organicShopping": "Belanja/marketplace (organik)", "paidShopping": "Belanja (iklan)",
}
PERANGKAT = {"mobile": "HP", "desktop": "Komputer (layar besar)", "laptop": "Laptop", "tablet": "Tablet"}
NEGARA = {"ID": "Indonesia", "MY": "Malaysia", "SG": "Singapura", "US": "Amerika Serikat", "AU": "Australia",
          "JP": "Jepang", "SA": "Arab Saudi", "NL": "Belanda", "TW": "Taiwan", "HK": "Hong Kong", "CN": "Tiongkok",
          "KR": "Korea Selatan", "IN": "India", "TL": "Timor Leste", "BN": "Brunei", "PH": "Filipina",
          "TH": "Thailand", "VN": "Vietnam", "DE": "Jerman", "GB": "Inggris"}
SESI = ("device", "country", "city", "region", "browser", "os", "language", "screen")
# kolom per-halaman/per-sumber: Umami 3.4.0 mengembalikan bounce & lama = 0 di metrics/expanded, jadi tidak dipakai
KOLOM_EVENT = ("path", "entry", "exit", "referrer", "domain", "title", "query", "event", "hostname", "utmSource",
               "utmMedium", "utmCampaign", "utmContent", "utmTerm")
PROPERTI_NILAI = ("nilai", "value", "harga", "total", "revenue", "omzet", "amount")


class Gagal(Exception):
    def __init__(self, pesan, kode=K_INPUT):
        super().__init__(pesan)
        self.kode = kode


# ============================================================ angka & tanggal


def angka(n):
    """Nilai API (int / '11' / None) -> int."""
    try:
        return int(float(n or 0))
    except (TypeError, ValueError):
        return 0


def ribuan(n):
    return f"{int(n):,}".replace(",", ".")


def desimal(x, digit=1):
    s = f"{x:.{digit}f}".replace(".", ",")
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s


def persen(bagian, total, digit=1):
    if not total:
        return "-"
    return desimal(bagian * 100 / total, digit) + "%"


def durasi(detik):
    detik = int(detik)
    if detik < 60:
        return f"{detik} dtk"
    m, s = divmod(detik, 60)
    if m < 60:
        return f"{m} mnt {s} dtk" if s else f"{m} mnt"
    j, m = divmod(m, 60)
    return f"{j} jam {m} mnt"


def perubahan(kini, lalu, lebih_kecil_lebih_baik=False):
    """'naik 7 (+175%)' / 'turun 2 (-20%)' / 'sama' / 'baru (sebelumnya 0)'."""
    if kini == lalu:
        return "sama"
    if not lalu:
        return "baru"
    beda = kini - lalu
    arah = "naik" if beda > 0 else "turun"
    tanda = "+" if beda > 0 else "-"
    teks_beda = desimal(abs(beda), 1) if isinstance(beda, float) else ribuan(abs(beda))
    return f"{arah} {teks_beda} ({tanda}{desimal(abs(beda) * 100 / lalu, 0)}%)"


def zona(tz):
    return dt.timezone(dt.timedelta(hours=TZ[tz][0]))


def tgl_panjang(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def tgl_pendek(d):
    return f"{d.day} {BULAN[d.month - 1][:3]} {d.year}"


def _awal_hari(d, tz):
    return dt.datetime(d.year, d.month, d.day, tzinfo=zona(tz))


def _geser_bulan(d, n):
    m = d.month - 1 + n
    y, m = d.year + m // 12, m % 12 + 1
    hari_maks = [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30,
                 31][m - 1]
    return d.replace(year=y, month=m, day=min(d.day, hari_maks))


def rentang(args):
    """-> dict awal/akhir (datetime aware, inklusif s.d. akhir-1ms) + pembanding + label."""
    tz = args.tz
    if args.sekarang:
        try:
            now = dt.datetime.fromisoformat(args.sekarang)
        except ValueError:
            raise Gagal("--sekarang harus berformat YYYY-MM-DDTHH:MM, mis. 2026-09-29T08:00.", K_INPUT)
        now = now.replace(tzinfo=zona(tz)) if now.tzinfo is None else now.astimezone(zona(tz))
    else:
        now = dt.datetime.now(zona(tz))
    hari = _awal_hari(now.date(), tz)
    if args.dari or args.sampai:
        if not (args.dari and args.sampai):
            raise Gagal("Isi --dari dan --sampai sekaligus (YYYY-MM-DD), mis. --dari 2026-09-01 --sampai 2026-09-30.")
        try:
            d1, d2 = dt.date.fromisoformat(args.dari), dt.date.fromisoformat(args.sampai)
        except ValueError:
            raise Gagal("Tanggal harus berformat YYYY-MM-DD, mis. 2026-09-01.", K_INPUT)
        if d2 < d1:
            raise Gagal("--sampai lebih awal dari --dari.", K_INPUT)
        awal, akhir = _awal_hari(d1, tz), _awal_hari(d2, tz) + dt.timedelta(days=1)
        panjang = akhir - awal
        b_awal, b_akhir = awal - panjang, awal
        label = f"{tgl_pendek(d1)} - {tgl_pendek(d2)}"
    else:
        p = args.periode
        if p == "hari-ini":
            awal, akhir = hari, now
            b_awal, b_akhir = awal - dt.timedelta(days=1), now - dt.timedelta(days=1)
            label = f"hari ini, {tgl_panjang(hari)} s.d. pukul {now:%H.%M}"
        elif p == "kemarin":
            awal, akhir = hari - dt.timedelta(days=1), hari
            b_awal, b_akhir = awal - dt.timedelta(days=1), awal
            label = f"kemarin, {tgl_panjang(awal)}"
        elif p in ("7hari", "30hari"):
            n = 7 if p == "7hari" else 30
            awal, akhir = hari - dt.timedelta(days=n - 1), now
            b_awal, b_akhir = awal - dt.timedelta(days=n), now - dt.timedelta(days=n)
            label = f"{n} hari terakhir, {tgl_pendek(awal)} - {tgl_pendek(hari)} (s.d. pukul {now:%H.%M})"
        elif p == "minggu-ini":
            awal, akhir = hari - dt.timedelta(days=now.weekday()), now
            b_awal, b_akhir = awal - dt.timedelta(days=7), now - dt.timedelta(days=7)
            label = f"minggu ini, Senin {tgl_pendek(awal)} s.d. {tgl_panjang(hari)} pukul {now:%H.%M}"
        elif p == "minggu-lalu":
            akhir = hari - dt.timedelta(days=now.weekday())
            awal = akhir - dt.timedelta(days=7)
            b_awal, b_akhir = awal - dt.timedelta(days=7), awal
            label = f"minggu lalu, Senin {tgl_pendek(awal)} - Minggu {tgl_pendek(akhir - dt.timedelta(days=1))}"
        elif p == "bulan-ini":
            awal, akhir = hari.replace(day=1), now
            b_awal, b_akhir = _geser_bulan(awal, -1), _geser_bulan(now, -1)
            label = f"bulan ini, 1 {BULAN[now.month - 1]} s.d. {tgl_pendek(hari)} pukul {now:%H.%M}"
        elif p == "bulan-lalu":
            akhir = hari.replace(day=1)
            awal = _geser_bulan(akhir, -1)
            b_awal, b_akhir = _geser_bulan(awal, -1), awal
            label = f"bulan lalu, {BULAN[awal.month - 1]} {awal.year}"
        else:
            raise Gagal(f"Periode tidak dikenal: {p}. Pilihan: {', '.join(PERIODE)}.", K_INPUT)
    b_akhir_incl = b_akhir - dt.timedelta(milliseconds=1)
    lb = tgl_pendek(b_awal) if b_awal.date() == b_akhir_incl.date() else f"{tgl_pendek(b_awal)} - {tgl_pendek(b_akhir_incl)}"
    if (b_akhir.hour, b_akhir.minute, b_akhir.second) != (0, 0, 0):
        lb += f" pukul {b_akhir:%H.%M} (sama panjang)"
    return {"awal": awal, "akhir": akhir, "b_awal": b_awal, "b_akhir": b_akhir, "label": label,
            "label_banding": lb, "sekarang": now}


def ms(d):
    return int(d.timestamp() * 1000)


def query_rentang(r, banding=False, tz="WIB"):
    a, b = (r["b_awal"], r["b_akhir"]) if banding else (r["awal"], r["akhir"])
    return {"startAt": ms(a), "endAt": ms(b) - 1, "timezone": TZ[tz][1]}


# ============================================================ kunci & alamat


def cek_izin_file(path):
    if os.name == "nt":
        return
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        return
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        sys.stderr.write(f"PERINGATAN: file {path} bisa dibaca pengguna lain. Jalankan: chmod 600 {path}\n")


def _tulis_rahasia(path, isi):
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
        f.write(isi + "\n")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def simpan_kunci(args):
    path = os.path.abspath(os.path.expanduser(args.kunci_file)) if args.kunci_file else KUNCI_DEFAULT
    if os.path.exists(path) and not args.ya:
        raise Gagal(f"File kunci sudah ada: {path}\nUntuk mengganti, ulangi dengan --ya.", K_FILE)
    sys.stderr.write(f"Kunci akan disimpan di: {path}\n")
    kunci = getpass.getpass("Tempel kunci API Umami (diawali umami_, tidak terlihat), lalu Enter: ").strip()
    if not kunci:
        raise Gagal("Kunci kosong, tidak disimpan.", K_INPUT)
    if re.search(r"\s", kunci):
        raise Gagal("Kunci berisi spasi/baris baru - kemungkinan tersalin rusak. Salin ulang.", K_INPUT)
    if not kunci.startswith("umami_"):
        sys.stderr.write("Catatan: ini bukan kunci API (tidak diawali umami_), akan dipakai sebagai SANDI akun. "
                         "Nama akun diisi lewat ENV UMAMI_USERNAME. Kunci API (Umami 3.4+) lebih disarankan.\n")
    _tulis_rahasia(path, kunci)
    print(f"Kunci tersimpan di {path} (izin 600).")
    return 0


def simpan_alamat(args):
    alamat = args.alamat.strip().rstrip("/")
    periksa_url(alamat, izinkan_publik=True)
    os.makedirs(FOLDER_KUNCI, mode=0o700, exist_ok=True)
    with open(ALAMAT_DEFAULT, "w", encoding="utf-8") as f:
        f.write(alamat + "\n")
    print(f"Alamat Umami tersimpan di {ALAMAT_DEFAULT}: {alamat}")
    return 0


def _baca_file(path, sumber):
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.isfile(path):
        raise Gagal(f"File kunci ({sumber}) tidak ditemukan: {path}. Jalankan dulu "
                    f"'python3 umami.py simpan-kunci' (docs/panduan-umami.md bagian 7).", K_FILE)
    cek_izin_file(path)
    with open(path, encoding="utf-8") as f:
        isi = f.read().strip()
    if not isi or re.search(r"\s", isi):
        raise Gagal(f"File kunci ({sumber}) kosong atau berisi spasi - simpan ulang dengan 'simpan-kunci --ya'.",
                    K_FILE)
    return isi


def ambil_rahasia(args):
    if args.kunci_file:
        return _baca_file(args.kunci_file, "--kunci-file")
    if os.environ.get("UMAMI_API_KEY"):
        return os.environ["UMAMI_API_KEY"].strip()
    if os.environ.get("UMAMI_API_KEY_FILE"):
        return _baca_file(os.environ["UMAMI_API_KEY_FILE"], "ENV UMAMI_API_KEY_FILE")
    if os.environ.get("UMAMI_PASSWORD"):
        return os.environ["UMAMI_PASSWORD"]
    return _baca_file(KUNCI_DEFAULT, "file kunci default")


def samarkan(k):
    if k.startswith("umami_") and len(k) > 14:
        return k[:8] + "****" + k[-4:]
    return "(sandi, disembunyikan)"


def alamat_awal():
    """--url > ENV UMAMI_URL > file simpan-alamat > http://localhost:3000. -> (url, dari_pengguna)."""
    if os.environ.get("UMAMI_URL"):
        return os.environ["UMAMI_URL"].strip(), True
    if os.path.isfile(ALAMAT_DEFAULT):
        with open(ALAMAT_DEFAULT, encoding="utf-8") as f:
            isi = f.read().strip()
        if isi:
            return isi, True
    return URL_DEFAULT, False


# ============================================================ HTTP ke Umami

_POLA_LAN = r"^(192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.)"
_SUDAH_DIPERINGATKAN = set()


def host_lokal(url):
    h = (urllib.parse.urlsplit(url).hostname or "").lower()
    return h in ("127.0.0.1", "localhost", "::1") or h.endswith(".localhost")


def host_lokal_atau_lan(url):
    h = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host_lokal(url) or re.match(_POLA_LAN, h) is not None


def periksa_url(url, izinkan_publik):
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise Gagal(f"Alamat Umami tidak valid: {url!r}. Contoh: http://localhost:3000 atau "
                    f"https://analitik.tokosaya.id", K_INPUT)
    if u.path not in ("", "/") or u.query:
        raise Gagal(f"Alamat Umami cukup sampai nama domain/port (tanpa /api, /login, dst): {url!r}.", K_INPUT)
    if host_lokal(url):
        return
    if re.match(_POLA_LAN, u.hostname):
        if u.scheme != "https" and url not in _SUDAH_DIPERINGATKAN:
            _SUDAH_DIPERINGATKAN.add(url)
            sys.stderr.write(f"PERINGATAN: {url} memakai http biasa di jaringan kantor (bukan komputer ini).\n")
        return
    if u.scheme != "https":
        raise Gagal(f"Alamat internet '{url}' wajib HTTPS (kunci API ikut terkirim; http biasa tidak terenkripsi). "
                    f"Pasang HTTPS dulu (docs/panduan-umami.md bagian 4).", K_INPUT)
    if not izinkan_publik:
        raise Gagal(f"Alamat '{url}' adalah server internet. Demi keamanan kunci, alamat server internet hanya "
                    f"dipakai bila disimpan pengguna sendiri (ENV UMAMI_URL atau 'simpan-alamat'), atau "
                    f"ditegaskan dengan --izinkan-jarak-jauh saat pengguna sendiri mengetik alamatnya.", K_INPUT)


class _TolakPengalihan(urllib.request.HTTPRedirectHandler):
    """Jangan ikuti redirect: header Authorization bisa terbawa ke alamat lain atau turun ke http."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Gagal(f"Server Umami mengalihkan (HTTP {code}) ke {newurl!r}. Demi keamanan kunci, skill TIDAK "
                    f"mengikuti pengalihan. Pakai alamat tujuan akhir yang benar (mis. versi https:// atau tanpa "
                    f"/login) lewat ENV UMAMI_URL / simpan-alamat (panduan bagian 11).", K_KONEKSI)


def buat_opener(url):
    proxy = urllib.request.ProxyHandler({}) if host_lokal_atau_lan(url) else urllib.request.ProxyHandler()
    return urllib.request.build_opener(proxy, _TolakPengalihan())


class Klien:
    def __init__(self, args):
        self.args = args
        self.url = args.url.rstrip("/")
        self.bearer = None
        self.akun = None

    def _minta(self, method, path, query=None, body=None, bearer=None):
        url = self.url + "/api" + path + ("?" + urllib.parse.urlencode(query) if query else "")
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", f"komunitech-umami-analitik/{VERSI}")
        if bearer:
            req.add_header("Authorization", "Bearer " + bearer)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with buat_opener(url).open(req, timeout=self.args.timeout) as resp:
                mentah = resp.read()
                return 200, (json.loads(mentah) if mentah else None)
        except urllib.error.HTTPError as e:
            mentah = e.read() or b""
            try:
                j = json.loads(mentah)
            except (ValueError, TypeError):
                j = None
            return e.code, j
        except Gagal:
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            raise Gagal(f"Tidak bisa menghubungi Umami di {self.url} ({getattr(e, 'reason', e)}). Pastikan Umami "
                        f"menyala dan alamatnya benar (ENV UMAMI_URL / simpan-alamat; panduan bagian 3).", K_KONEKSI)
        except ValueError:
            raise Gagal("Jawaban server bukan JSON - alamat salah (bukan Umami?) atau terpotong.", K_KONEKSI)

    def masuk(self):
        """Siapkan bearer: kunci API langsung, atau login nama+sandi (token sesi hanya di memori)."""
        if self.bearer:
            return
        rahasia = ambil_rahasia(self.args)
        self.rahasia_samaran = samarkan(rahasia)
        if rahasia.startswith("umami_"):
            self.bearer = rahasia
            return
        nama = os.environ.get("UMAMI_USERNAME")
        if not nama:
            raise Gagal("Yang tersimpan adalah sandi, tapi nama akun belum diisi. Set ENV UMAMI_USERNAME (mis. "
                        "agen-baca), atau lebih baik buat kunci API di Umami 3.4+ (panduan bagian 7).", K_INPUT)
        kode, j = self._minta("POST", "/auth/login", body={"username": nama, "password": rahasia})
        if kode == 401:
            raise Gagal("Login Umami ditolak (401): nama akun/sandi salah.", K_AUTH)
        if kode != 200 or not isinstance(j, dict):
            raise Gagal(f"Login Umami gagal (kode {kode}). Periksa alamat server.", K_KONEKSI)
        if j.get("requiresTwoFactor"):
            raise Gagal("Akun ini memakai verifikasi 2 langkah (2FA), jadi tidak bisa login otomatis dengan sandi. "
                        "Pakai kunci API (Settings > API keys, Umami 3.4+).", K_AUTH)
        self.bearer = j.get("token")
        if not self.bearer:
            raise Gagal("Login Umami tidak mengembalikan token.", K_KONEKSI)

    def get(self, path, query=None):
        self.masuk()
        kode, j = self._minta("GET", path, query=query, bearer=self.bearer)
        if kode == 200:
            return j
        pesan = ""
        if isinstance(j, dict):
            e = j.get("error")
            pesan = (e.get("message") if isinstance(e, dict) else e) or j.get("message") or ""
            if isinstance(e, dict) and e.get("errors"):
                pesan += " " + json.dumps(e["errors"], ensure_ascii=False)[:200]
        if kode == 401:
            if path != "/me":
                k2, _ = self._minta("GET", "/me", bearer=self.bearer)
                if k2 == 200:
                    raise Gagal("401 dari Umami: akun kunci ini TIDAK PUNYA AKSES ke website/data tersebut (atau id "
                                "website salah). Jalankan 'situs' untuk melihat website yang bisa dibaca; atur akses "
                                "lewat tim di Umami (panduan bagian 7). Jangan mencoba lewat jalan lain.", K_AUTH)
            raise Gagal("401 dari Umami: kunci API salah, sudah dihapus, atau sandi akun diganti. Buat kunci baru "
                        "(Settings > API keys) lalu 'simpan-kunci --ya' (panduan bagian 7).", K_AUTH)
        if kode == 403:
            raise Gagal(f"403 dari Umami: akses ditolak ({pesan or '-'}).", K_AUTH)
        if kode == 404:
            raise Gagal(f"404 dari Umami ({path}): tidak ditemukan. Alamat salah (bukan Umami?), atau versi Umami "
                        f"terlalu lama untuk fitur ini (skill diuji dengan Umami {UMAMI_TERUJI}).", K_KONEKSI)
        if kode == 400:
            raise Gagal(f"Umami menolak permintaan (400): {pesan or '-'}", K_INPUT)
        if 500 <= kode < 600:
            raise Gagal(f"Umami membalas galat server ({kode}). Cek 'docker compose ps' / log Umami; coba lagi "
                        f"sebentar.", K_KONEKSI)
        raise Gagal(f"Umami membalas kode {kode}: {pesan or '-'}", K_KONEKSI)

    def saya(self):
        if self.akun is None:
            me = self.get("/me") or {}
            u = me.get("user") or {}
            # jawaban /me berisi token/kunci: JANGAN pernah dicetak/disimpan. Ambil field aman saja.
            self.akun = {"username": u.get("username"), "role": u.get("role"), "isAdmin": bool(u.get("isAdmin")),
                         "authType": me.get("authType") or "sesi"}
        return self.akun


# ============================================================ website


def _baris(data):
    return (data.get("data") if isinstance(data, dict) else data) or []


def daftar_situs(k):
    """Website milik akun + website tim tempat akun menjadi anggota (termasuk anggota 'view-only').
    Catatan Umami 3.4.0: includeTeams hanya mencakup tim yang DIMILIKI/DIKELOLA akun, jadi tim diambil terpisah."""
    hasil, lihat = [], set()

    def tambah(s, tim=None):
        if s.get("id") and s["id"] not in lihat:
            lihat.add(s["id"])
            hasil.append({"id": s["id"], "nama": s.get("name") or "", "domain": s.get("domain") or "",
                          "tim": tim or ("ya" if s.get("teamId") else None)})

    for s in _baris(k.get("/websites", {"includeTeams": "true", "pageSize": 200})):
        tambah(s)
    for t in _baris(k.get("/me/teams", {"pageSize": 100})):
        # jawaban tim berisi kode undangan & daftar anggota: hanya id & nama tim yang dipakai
        for s in _baris(k.get(f"/teams/{t.get('id')}/websites", {"pageSize": 200})):
            tambah(s, t.get("name") or "tim")
    return hasil


def pilih_situs(k, args):
    sebut = (args.situs or os.environ.get("UMAMI_SITUS") or "").strip()
    semua = daftar_situs(k)
    if not semua:
        raise Gagal("Akun ini belum bisa membaca website apa pun di Umami. Tambahkan website (Settings > Websites) "
                    "atau masukkan akun ke tim yang memegang website itu (panduan bagian 5 & 7).", K_INPUT)
    if not sebut:
        if len(semua) == 1:
            return semua[0]
        opsi = "; ".join(f"{s['nama']} ({s['domain']})" for s in semua)
        raise Gagal(f"Ada {len(semua)} website: {opsi}. Sebutkan dengan --situs <nama/domain>.", K_GANDA)
    kecil = sebut.lower()
    persis = [s for s in semua if kecil in (s["id"].lower(), s["nama"].lower(), s["domain"].lower())]
    if len(persis) == 1:
        return persis[0]
    cocok = persis or [s for s in semua if kecil in s["nama"].lower() or kecil in s["domain"].lower()]
    if len(cocok) == 1:
        return cocok[0]
    if not cocok:
        ada = "; ".join(f"{s['nama']} ({s['domain']})" for s in semua)
        raise Gagal(f"Website '{sebut}' tidak ditemukan. Yang bisa dibaca: {ada}.", K_INPUT)
    opsi = "; ".join(f"{s['nama']} ({s['domain']}, id {s['id']})" for s in cocok)
    raise Gagal(f"'{sebut}' cocok dengan {len(cocok)} website: {opsi}. Sebutkan domain lengkap atau id.", K_GANDA)


# ============================================================ pengambilan data


def statistik(k, situs, r, banding, tz):
    q = query_rentang(r, banding, tz)
    s = k.get(f"/websites/{situs['id']}/stats", q) or {}
    return olah_stat(s)


def olah_stat(s):
    v, kj, pv, b, t = (angka(s.get(x)) for x in ("visitors", "visits", "pageviews", "bounces", "totaltime"))
    b = min(b, kj)
    return {"pengunjung": v, "kunjungan": kj, "tayangan": pv, "bounce": b, "total_detik": t,
            "bounce_persen": round(b * 100 / kj, 1) if kj else None,
            "rata_detik": int(t / kj) if kj else 0,
            "halaman_per_kunjungan": round(pv / kj, 2) if kj else None}


def metrik(k, situs, r, jenis, tz, banding=False, batas=None, diperluas=False, filter_=None):
    q = query_rentang(r, banding, tz)
    q["type"] = jenis
    if batas:
        q["limit"] = batas
    q.update(filter_ or {})
    path = f"/websites/{situs['id']}/metrics" + ("/expanded" if diperluas else "")
    data = k.get(path, q) or []
    hasil = []
    for d in data if isinstance(data, list) else []:
        if diperluas:
            hasil.append({"nama": d.get("name") if d.get("name") is not None else "",
                          "tayangan": angka(d.get("pageviews")), "pengunjung": angka(d.get("visitors")),
                          "kunjungan": angka(d.get("visits")), "bounce": angka(d.get("bounces")),
                          "total_detik": angka(d.get("totaltime"))})
        else:
            baris = {"nama": d.get("x") if d.get("x") is not None else "", "jumlah": angka(d.get("y"))}
            if d.get("country"):
                baris["negara"] = d["country"]
            hasil.append(baris)
    # urutan tetap (angka terbesar dulu, seri -> nama A-Z); Umami tidak menjamin urutan baris yang seri
    if diperluas:
        kunci = "kunjungan" if jenis == "channel" else ("pengunjung" if jenis in SESI else "tayangan")
        hasil.sort(key=lambda d: (-d[kunci], -d["pengunjung"], str(d["nama"])))
    else:
        hasil.sort(key=lambda d: (-d["jumlah"], str(d["nama"])))
    return hasil


def label_negara(kode):
    if not kode:
        return "(tidak diketahui)"
    return f"{NEGARA.get(kode, kode)}"


def label_kosong(x):
    return x if x not in (None, "") else "(tidak diketahui)"


# ============================================================ keluaran teks


def kepala(judul, situs, r, dengan_banding=True):
    baris = [f"{judul}: {situs['nama']} ({situs['domain']})", f"Periode: {r['label']}"]
    if dengan_banding:
        baris.append(f"Pembanding: {r['label_banding']}")
    return baris


def tabel(baris, kolom, lebar_nama=34):
    """baris: list of list (kolom pertama teks). kolom: judul kolom."""
    if not baris:
        return ["  (belum ada data pada periode ini)"]
    keluar = []
    lebar = [max(len(str(kolom[i])), *(len(str(b[i])) for b in baris)) for i in range(1, len(kolom))]
    keluar.append("  " + f"{kolom[0]:<{lebar_nama}}" + "".join(f"  {kolom[i]:>{lebar[i - 1]}}" for i in range(1, len(kolom))))
    for b in baris:
        nama = str(b[0])
        if len(nama) > lebar_nama:
            nama = nama[:lebar_nama - 1] + "~"
        keluar.append("  " + f"{nama:<{lebar_nama}}" + "".join(f"  {str(b[i]):>{lebar[i - 1]}}" for i in range(1, len(kolom))))
    return keluar


def teks_ringkasan(s, b=None):
    def baris(label, kini, lalu=None, fmt=ribuan, kecil_lebih_baik=False):
        t = f"- {label:<22}: {fmt(kini)}"
        if lalu is not None:
            t += f"   (sebelumnya {fmt(lalu)}; {perubahan(kini, lalu, kecil_lebih_baik)})"
        return t

    L = []
    L.append(baris("Pengunjung unik", s["pengunjung"], b and b["pengunjung"]))
    L.append(baris("Kunjungan", s["kunjungan"], b and b["kunjungan"]))
    L.append(baris("Tayangan halaman", s["tayangan"], b and b["tayangan"]))
    bp = "-" if s["bounce_persen"] is None else desimal(s["bounce_persen"]) + "%"
    t = f"- {'Bounce rate':<22}: {bp} ({ribuan(s['bounce'])} dari {ribuan(s['kunjungan'])} kunjungan hanya 1 halaman tanpa klik)"
    if b is not None:
        bb = "-" if b["bounce_persen"] is None else desimal(b["bounce_persen"]) + "%"
        t += f"   (sebelumnya {bb})"
    L.append(t)
    t = f"- {'Rata-rata lama':<22}: {durasi(s['rata_detik'])} per kunjungan"
    if b is not None:
        t += f"   (sebelumnya {durasi(b['rata_detik'])})"
    L.append(t)
    hk = "-" if s["halaman_per_kunjungan"] is None else desimal(s["halaman_per_kunjungan"], 1)
    L.append(f"- {'Halaman per kunjungan':<22}: {hk}")
    return L


# ============================================================ perintah


def cmd_cek(k, args):
    teks = ["CEK UMAMI", f"Alamat: {k.url}"]
    kode, j = k._minta("GET", "/heartbeat")
    if kode != 200 or not isinstance(j, dict) or not j.get("ok"):
        raise Gagal(f"Alamat {k.url} menjawab (kode {kode}) tapi bukan server Umami yang sehat. Periksa alamat/port "
                    f"(bawaan Umami: port 3000).", K_KONEKSI)
    teks.append("Server: menyala (heartbeat OK)")
    k.masuk()
    teks.append(f"Kunci: {k.rahasia_samaran}")
    a = k.saya()
    peran = {"admin": "ADMIN (sebaiknya pakai akun khusus 'view-only' untuk AI)", "user": "user (bisa mengubah "
             "website miliknya; untuk AI lebih aman akun view-only)", "view-only": "view-only (hanya lihat - disarankan)"}
    teks.append(f"Akun: {a['username']} - peran {peran.get(a['role'], a['role'])}; masuk lewat "
                f"{'kunci API' if a['authType'] == 'api-key' else 'login sandi'}")
    situs = daftar_situs(k)
    teks.append(f"Website yang bisa dibaca: {len(situs)}")
    for s in situs:
        teks.append(f"  - {s['nama']} ({s['domain']}) id {s['id']}" + (f" [tim {s['tim']}]" if s["tim"] and s["tim"] != "ya" else (" [tim]" if s["tim"] else "")))
    if not situs:
        teks.append("  (belum ada - tambahkan website atau masukkan akun ke tim; panduan bagian 5 & 7)")
    teks.append(f"Catatan: skill diuji dengan Umami {UMAMI_TERUJI}. Versi lain: cocokkan angka penting dengan layar "
                f"Umami.")
    return {"teks": "\n".join(teks), "akun": a, "situs": situs}


def cmd_situs(k, args):
    s = daftar_situs(k)
    teks = [f"WEBSITE DI UMAMI ({len(s)})"] + [f"- {x['nama']} | {x['domain']} | id {x['id']}" for x in s]
    return {"teks": "\n".join(teks), "situs": s}


def cmd_ringkasan(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    s = statistik(k, situs, r, False, args.tz)
    b = statistik(k, situs, r, True, args.tz)
    teks = kepala("RINGKASAN WEBSITE", situs, r) + teks_ringkasan(s, b)
    if s["pengunjung"] == 0:
        teks.append("Belum ada pengunjung tercatat. Bila website sudah ramai, cek kode pelacak (panduan bagian 5).")
    teks.append("Catatan: pengunjung unik dihitung per perangkat+browser (tanpa cookie); satu orang dengan HP & "
                "laptop terhitung 2.")
    return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "statistik": s, "pembanding": b}


def _periode_json(r):
    return {"awal": r["awal"].isoformat(), "akhir": r["akhir"].isoformat(), "label": r["label"],
            "pembanding_awal": r["b_awal"].isoformat(), "pembanding_akhir": r["b_akhir"].isoformat()}


def cmd_halaman(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    if args.jenis in ("masuk", "keluar"):
        data = metrik(k, situs, r, "entry" if args.jenis == "masuk" else "exit", args.tz, batas=args.batas)
        judul = "HALAMAN MASUK (pertama dibuka)" if args.jenis == "masuk" else "HALAMAN KELUAR (terakhir dibuka)"
        teks = kepala(judul, situs, r, False) + tabel([[d["nama"], ribuan(d["jumlah"])] for d in data],
                                                       ["Halaman", "Pengunjung"])
        return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "halaman": data}
    data = metrik(k, situs, r, "path", args.tz, batas=args.batas, diperluas=True)
    total = statistik(k, situs, r, False, args.tz)
    baris = [[d["nama"], ribuan(d["tayangan"]), ribuan(d["pengunjung"]), persen(d["pengunjung"], total["pengunjung"], 0)]
             for d in data]
    teks = kepala("HALAMAN TERATAS", situs, r, False) + tabel(baris, ["Halaman", "Tayangan", "Pengunjung", "% pengunjung"])
    teks.append(f"Total: {ribuan(total['tayangan'])} tayangan dari {ribuan(total['pengunjung'])} pengunjung unik.")
    return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "halaman": data, "total": total}


def cmd_sumber(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    kanal = metrik(k, situs, r, "channel", args.tz, diperluas=True)
    ref = metrik(k, situs, r, "referrer", args.tz, batas=args.batas, diperluas=True)
    total_kj = sum(d["kunjungan"] for d in kanal)
    teks = kepala("SUMBER TRAFIK", situs, r, False)
    teks.append("Kanal (per kunjungan):")
    teks += tabel([[KANAL.get(d["nama"], d["nama"]), ribuan(d["kunjungan"]), persen(d["kunjungan"], total_kj, 0),
                    ribuan(d["pengunjung"])] for d in kanal], ["Kanal", "Kunjungan", "%", "Pengunjung"], 46)
    teks.append("Situs perujuk (referrer):")
    teks += tabel([[d["nama"], ribuan(d["pengunjung"]), ribuan(d["kunjungan"])] for d in ref],
                  ["Situs", "Pengunjung", "Kunjungan"])
    if any(d["nama"] == "direct" for d in kanal):
        teks.append("Catatan: klik dari WhatsApp, Telegram, aplikasi, atau QR biasanya TIDAK membawa alamat asal, "
                    "jadi masuk 'Langsung'. Pakai tautan ber-UTM (perintah utm) agar terlihat jelas.")
    return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "kanal": kanal, "referrer": ref}


def cmd_utm(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    bagian = [("utmCampaign", "Kampanye (utm_campaign)"), ("utmSource", "Sumber (utm_source)"),
              ("utmMedium", "Medium (utm_medium)"), ("utmContent", "Konten (utm_content)")]
    hasil, teks = {}, kepala("KAMPANYE UTM", situs, r, False)
    for jenis, judul in bagian:
        data = metrik(k, situs, r, jenis, args.tz, batas=args.batas, diperluas=True)
        hasil[jenis] = data
        if not data and jenis == "utmContent":
            continue
        teks.append(judul + ":")
        teks += tabel([[d["nama"], ribuan(d["pengunjung"]), ribuan(d["kunjungan"]), ribuan(d["tayangan"])] for d in data],
                      ["Nilai", "Pengunjung", "Kunjungan", "Tayangan"])
    if not any(hasil.values()):
        teks.append("Belum ada kunjungan ber-UTM. Buat tautan kampanye (panduan bagian 8), mis. "
                    "https://tokoanda.id/?utm_source=instagram&utm_medium=bio&utm_campaign=promo-gajian")
    teks.append("Catatan: angka UTM dihitung dari halaman yang dibuka lewat tautan ber-UTM. Umami tidak menempelkan "
                "UTM ke event (klik WA/beli), jadi konversi per kampanye tidak dihitung di sini.")
    return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "utm": hasil}


def cmd_pengunjung(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    bagian = [("device", "Perangkat"), ("country", "Negara"), ("city", "Kota")]
    if args.semua:
        bagian += [("browser", "Browser"), ("os", "Sistem operasi"), ("language", "Bahasa")]
    total = statistik(k, situs, r, False, args.tz)["pengunjung"]
    hasil, teks = {}, kepala("PROFIL PENGUNJUNG", situs, r, False)
    for jenis, judul in bagian:
        data = metrik(k, situs, r, jenis, args.tz, batas=args.batas)
        hasil[jenis] = data
        teks.append(judul + ":")
        baris = []
        for d in data:
            if jenis == "device":
                nama = PERANGKAT.get(d["nama"], label_kosong(d["nama"]))
            elif jenis == "country":
                nama = label_negara(d["nama"])
            elif jenis == "city":
                nama = label_kosong(d["nama"]) + (f", {label_negara(d.get('negara'))}" if d.get("negara") else "")
            else:
                nama = label_kosong(d["nama"])
            baris.append([nama, ribuan(d["jumlah"]), persen(d["jumlah"], total, 0)])
        teks += tabel(baris, [judul, "Pengunjung", "%"])
    teks.append(f"Total pengunjung unik: {ribuan(total)}. Lokasi diperkirakan dari alamat IP (kota bisa meleset, "
                f"mis. pengguna data seluler tercatat di kota lain).")
    return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "pengunjung": hasil, "total": total}


def daftar_tautan(k):
    """Tautan pelacak Umami (fitur Links: https://<umami>/q/<slug> -> alamat tujuan) milik akun + tim."""
    hasil, lihat = [], set()
    sumber = [_baris(k.get("/links", {"pageSize": 200}))]
    for t in _baris(k.get("/me/teams", {"pageSize": 100})):
        sumber.append(_baris(k.get(f"/teams/{t.get('id')}/links", {"pageSize": 200})))
    for daftar in sumber:
        for l in daftar:
            if l.get("id") and l["id"] not in lihat:
                lihat.add(l["id"])
                hasil.append({"id": l["id"], "nama": l.get("name") or "", "slug": l.get("slug") or "",
                              "tujuan": l.get("url") or ""})
    return hasil


def cmd_tautan(k, args):
    r = rentang(args)
    semua = daftar_tautan(k)
    teks = [f"TAUTAN PELACAK (Umami Links)", f"Periode: {r['label']}", f"Pembanding: {r['label_banding']}"]
    if not semua:
        teks.append("Belum ada tautan pelacak yang bisa dibaca akun ini. Buat di Umami: Links > Create link "
                    "(panduan bagian 5c) - cocok untuk bio Instagram/TikTok, QR di kemasan, atau tombol WA.")
        return {"teks": "\n".join(teks), "periode": _periode_json(r), "tautan": []}
    baris, data = [], []
    for t in semua:
        entitas = {"id": t["id"]}
        s = statistik(k, entitas, r, False, args.tz)
        b = statistik(k, entitas, r, True, args.tz)
        ref = metrik(k, entitas, r, "referrer", args.tz, batas=3)
        t2 = dict(t, klik=s["tayangan"], pengunjung=s["pengunjung"], klik_sebelumnya=b["tayangan"], referrer=ref)
        data.append(t2)
        baris.append([t["nama"] or t["slug"], ribuan(s["tayangan"]), ribuan(s["pengunjung"]), ribuan(b["tayangan"]),
                      ", ".join(f"{x['nama']} ({ribuan(x['jumlah'])})" for x in ref) or "-"])
    data.sort(key=lambda x: (-x["klik"], x["nama"]))
    baris.sort(key=lambda x: (-int(x[1].replace(".", "")), x[0]))
    teks += tabel(baris, ["Tautan", "Klik", "Pengunjung", "Sebelumnya", "Asal klik teratas"], 26)
    teks.append("Klik = berapa kali tautan dibuka (termasuk orang yang sama berulang). Tautan dibuka dari aplikasi "
                "WA/Telegram biasanya tanpa asal klik.")
    return {"teks": "\n".join(teks), "periode": _periode_json(r), "tautan": data}


def _event(k, situs, r, tz, banding=False):
    return metrik(k, situs, r, "event", tz, banding=banding, diperluas=True)


def cmd_banding(k, args):
    situs = pilih_situs(k, args)
    if not (args.dari or args.sampai) and args.periode == "7hari":
        args.periode = "minggu-ini"
    r = rentang(args)
    s, b = statistik(k, situs, r, False, args.tz), statistik(k, situs, r, True, args.tz)
    ev, evb = _event(k, situs, r, args.tz), _event(k, situs, r, args.tz, True)
    teks = kepala("PERBANDINGAN", situs, r)
    baris = [
        ["Pengunjung unik", ribuan(s["pengunjung"]), ribuan(b["pengunjung"]), perubahan(s["pengunjung"], b["pengunjung"])],
        ["Kunjungan", ribuan(s["kunjungan"]), ribuan(b["kunjungan"]), perubahan(s["kunjungan"], b["kunjungan"])],
        ["Tayangan halaman", ribuan(s["tayangan"]), ribuan(b["tayangan"]), perubahan(s["tayangan"], b["tayangan"])],
        ["Bounce rate", "-" if s["bounce_persen"] is None else desimal(s["bounce_persen"]) + "%",
         "-" if b["bounce_persen"] is None else desimal(b["bounce_persen"]) + "%",
         _ubah_poin(s["bounce_persen"], b["bounce_persen"])],
        ["Rata-rata lama", durasi(s["rata_detik"]), durasi(b["rata_detik"]),
         _ubah_durasi(s["rata_detik"], b["rata_detik"])],
    ]
    nama_ev = [d["nama"] for d in ev] + [d["nama"] for d in evb if d["nama"] not in {e["nama"] for e in ev}]
    peta, petab = {d["nama"]: d for d in ev}, {d["nama"]: d for d in evb}
    for n in nama_ev:
        a, c = peta.get(n, {}).get("tayangan", 0), petab.get(n, {}).get("tayangan", 0)
        baris.append([f"Event '{n}'", ribuan(a), ribuan(c), perubahan(a, c)])
    teks += tabel(baris, ["Ukuran", "Periode ini", "Pembanding", "Perubahan"], 22)
    if args.periode in ("minggu-ini", "hari-ini", "7hari", "30hari", "bulan-ini") and not args.dari:
        teks.append("Catatan: periode berjalan dibandingkan dengan rentang yang SAMA PANJANG sampai jam yang sama "
                    "(adil, bukan minggu penuh vs setengah minggu).")
    return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "statistik": s, "pembanding": b,
            "event": ev, "event_pembanding": evb}


def _ubah_durasi(a, b):
    if a == b:
        return "sama"
    if not b:
        return "baru"
    return f"{'naik' if a > b else 'turun'} {durasi(abs(a - b))} ({'+' if a > b else '-'}{desimal(abs(a - b) * 100 / b, 0)}%)"


def _ubah_poin(a, b):
    if a is None or b is None:
        return "-"
    if a == b:
        return "sama"
    return f"{'naik' if a > b else 'turun'} {desimal(abs(a - b))} poin"


def cmd_konversi(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    total = statistik(k, situs, r, False, args.tz)
    ev = _event(k, situs, r, args.tz)
    evb = {d["nama"]: d for d in _event(k, situs, r, args.tz, True)}
    q = query_rentang(r, False, args.tz)
    props = k.get(f"/websites/{situs['id']}/event-data/events", q) or []
    teks = kepala("KONVERSI (EVENT)", situs, r)
    if not ev:
        teks.append("Belum ada event tercatat. Tambahkan atribut data-umami-event pada tombol WA/Beli "
                    "(panduan bagian 6), lalu tunggu ada pengunjung yang klik.")
    baris = []
    for d in ev:
        lalu = evb.get(d["nama"], {}).get("tayangan", 0)
        baris.append([d["nama"], ribuan(d["tayangan"]), ribuan(d["pengunjung"]),
                      persen(d["pengunjung"], total["pengunjung"]), ribuan(lalu)])
    if ev:
        teks += tabel(baris, ["Event", "Jumlah", "Pengunjung", "Tingkat konversi", "Sebelumnya"], 24)
        teks.append(f"Tingkat konversi = pengunjung yang melakukan event / {ribuan(total['pengunjung'])} pengunjung "
                    f"unik periode ini.")
    rinci = []
    for p in props if isinstance(props, list) else []:
        nama_ev, prop = p.get("eventName"), p.get("propertyName")
        if not nama_ev or not prop:
            continue
        nilai = k.get(f"/websites/{situs['id']}/event-data/values", dict(q, event=nama_ev, propertyName=prop)) or []
        isi = [{"nilai": v.get("value"), "jumlah": angka(v.get("total"))} for v in nilai]
        item = {"event": nama_ev, "properti": prop, "nilai": isi}
        if prop.lower() in PROPERTI_NILAI:
            try:
                item["jumlah_total"] = sum(float(str(v["nilai"]).replace(",", ".")) * v["jumlah"] for v in isi)
            except ValueError:
                pass
        rinci.append(item)
    for it in rinci:
        if "jumlah_total" in it:
            teks.append(f"- {it['event']} / {it['properti']}: total {_rupiah_atau_angka(it['jumlah_total'])} dari "
                        f"{ribuan(sum(v['jumlah'] for v in it['nilai']))} event (dari data tombol, BUKAN omzet resmi - "
                        f"cocokkan dengan catatan penjualan)")
        else:
            isi = sorted(it["nilai"], key=lambda v: (-v["jumlah"], str(v["nilai"])))
            teks.append(f"- {it['event']} / {it['properti']}: " + "; ".join(f"{v['nilai']} ({ribuan(v['jumlah'])})"
                                                                            for v in isi[:8]))
    return {"teks": "\n".join(teks), "situs": situs, "periode": _periode_json(r), "event": ev, "rincian": rinci,
            "total": total}


def _rupiah_atau_angka(x):
    if abs(x - round(x)) < 1e-9:
        return "Rp" + ribuan(round(x))
    return desimal(x, 2)


# ============================================================ ekspor & laporan


_PEMICU_RUMUS = ("=", "+", "-", "@", "\t", "\r")


def aman_csv(v):
    """Cegah injeksi rumus Excel: teks diawali = + - @ diberi tanda petik satu."""
    if isinstance(v, str) and v and v[0] in _PEMICU_RUMUS:
        return "'" + v
    return v


def cmd_ekspor_csv(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    koma = args.pemisah == "koma"
    sep = "," if koma else ";"

    def dsm(x):
        if x is None:
            return ""
        s = f"{x:.1f}" if isinstance(x, float) else str(x)
        return s if koma else s.replace(".", ",")

    s = statistik(k, situs, r, False, args.tz)
    rows = [["bagian", "nama", "pengunjung", "kunjungan", "tayangan", "bounce", "bounce_persen", "rata_detik"]]
    rows.append(["ringkasan", "total", s["pengunjung"], s["kunjungan"], s["tayangan"], s["bounce"],
                 dsm(s["bounce_persen"]), s["rata_detik"]])
    for jenis, bag in (("path", "halaman"), ("channel", "kanal"), ("referrer", "referrer"), ("utmSource", "utm_source"),
                       ("utmMedium", "utm_medium"), ("utmCampaign", "utm_campaign"), ("event", "event"),
                       ("device", "perangkat"), ("country", "negara"), ("city", "kota")):
        for d in metrik(k, situs, r, jenis, args.tz, diperluas=True):
            ada_bounce = jenis not in KOLOM_EVENT and d["kunjungan"]
            bp = round(d["bounce"] * 100 / d["kunjungan"], 1) if ada_bounce else None
            rata = int(d["total_detik"] / d["kunjungan"]) if ada_bounce else ""
            if jenis == "channel":
                nama = KANAL.get(d["nama"], d["nama"]).split(" (")[0]
            elif jenis == "device":
                nama = PERANGKAT.get(d["nama"], label_kosong(d["nama"]))
            elif jenis == "country":
                nama = label_negara(d["nama"])
            else:
                nama = label_kosong(d["nama"])
            rows.append([bag, aman_csv(nama), d["pengunjung"], d["kunjungan"], d["tayangan"],
                         d["bounce"] if ada_bounce else "", dsm(bp), rata])
    q = query_rentang(r, False, args.tz)
    q["unit"] = "day"
    harian = k.get(f"/websites/{situs['id']}/pageviews", q) or {}
    ses = {str(x.get("x"))[:10]: angka(x.get("y")) for x in harian.get("sessions") or []}
    for x in harian.get("pageviews") or []:
        tgl = str(x.get("x"))[:10]
        rows.append(["harian", tgl, ses.get(tgl, 0), "", angka(x.get("y")), "", "", ""])
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=sep, lineterminator="\n")
    w.writerow([f"# Umami - {situs['nama']} ({situs['domain']}) - {r['label']} - zona {args.tz}"])
    w.writerows(rows)
    isi = buf.getvalue()
    nama = args.keluaran or f"umami-{re.sub(r'[^a-z0-9]+', '-', situs['domain'].lower()).strip('-')}-" \
                            f"{r['awal']:%Y%m%d}-{(r['akhir'] - dt.timedelta(milliseconds=1)):%Y%m%d}.csv"
    with open(nama, "w", encoding="utf-8-sig", newline="") as f:
        f.write(isi)
    teks = [f"CSV tersimpan: {os.path.abspath(nama)}", f"Isi: {len(rows) - 1} baris (ringkasan, halaman, kanal, "
            f"referrer, UTM, event, perangkat, negara, kota, harian). Pemisah '{sep}'."]
    teks.append("Catatan: kolom 'pengunjung' per halaman/sumber = pengunjung unik di baris itu (tidak bisa dijumlah "
                "antarbaris). Baris 'harian': pengunjung per hari.")
    return {"teks": "\n".join(teks), "file": os.path.abspath(nama), "baris": len(rows) - 1}


def cmd_laporan_mingguan(k, args):
    situs = pilih_situs(k, args)
    r = rentang(args)
    s, b = statistik(k, situs, r, False, args.tz), statistik(k, situs, r, True, args.tz)
    hal = metrik(k, situs, r, "path", args.tz, batas=5, diperluas=True)
    kanal = metrik(k, situs, r, "channel", args.tz, diperluas=True)
    kamp = metrik(k, situs, r, "utmCampaign", args.tz, batas=5)
    src = metrik(k, situs, r, "utmSource", args.tz, batas=5)
    ev = _event(k, situs, r, args.tz)
    evb = {d["nama"]: d for d in _event(k, situs, r, args.tz, True)}
    dev = metrik(k, situs, r, "device", args.tz)
    kota = metrik(k, situs, r, "city", args.tz, batas=3)
    T = [f"Laporan web {situs['nama']} ({situs['domain']})", f"Periode: {r['label']}",
         f"Pembanding: {r['label_banding']}", ""]
    T += teks_ringkasan(s, b)
    if ev:
        T += ["", "Konversi:"]
        for d in ev[:6]:
            lalu = evb.get(d["nama"], {}).get("tayangan", 0)
            T.append(f"- {d['nama']}: {ribuan(d['tayangan'])}x oleh {ribuan(d['pengunjung'])} pengunjung "
                     f"({persen(d['pengunjung'], s['pengunjung'])}); sebelumnya {ribuan(lalu)}x")
    if hal:
        T += ["", "Halaman teratas:"] + [f"{i}. {d['nama']} - {ribuan(d['tayangan'])} tayangan, "
                                          f"{ribuan(d['pengunjung'])} pengunjung" for i, d in enumerate(hal, 1)]
    if kanal:
        tot = sum(d["kunjungan"] for d in kanal)
        T += ["", "Sumber:"] + [f"- {KANAL.get(d['nama'], d['nama']).split(' (')[0]}: {ribuan(d['kunjungan'])} kunjungan "
                                f"({persen(d['kunjungan'], tot, 0)})" for d in kanal[:5]]
    if kamp or src:
        T += ["", "Kampanye UTM (pengunjung):"]
        T += [f"- kampanye {d['nama']}: {ribuan(d['jumlah'])}" for d in kamp]
        T += [f"- sumber {d['nama']}: {ribuan(d['jumlah'])}" for d in src]
    if dev:
        T += ["", "Perangkat: " + ", ".join(f"{PERANGKAT.get(d['nama'], label_kosong(d['nama']))} "
                                           f"{persen(d['jumlah'], s['pengunjung'], 0)}" for d in dev)]
    if kota:
        T.append("Kota teratas: " + ", ".join(f"{label_kosong(d['nama'])} ({ribuan(d['jumlah'])})" for d in kota))
    if s["pengunjung"] == 0:
        T += ["", "Belum ada pengunjung tercatat pada periode ini. Cek kode pelacak di website (panduan bagian 5)."]
    T += ["", "Sumber data: Umami milik Anda (tanpa cookie). Pengunjung unik = perangkat+browser."]
    teks = "\n".join(T)
    if len(teks) > 3900:
        teks = teks[:3850] + "\n...(dipotong; lihat detail di layar Umami)"
    return {"teks": teks, "situs": situs, "periode": _periode_json(r), "statistik": s, "pembanding": b}


# ============================================================ argparse


def cetak(hasil, args):
    if getattr(args, "json", False):
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    else:
        print(hasil["teks"])


def _opsi_umum(p, periode_default="7hari", periode=True):
    p.add_argument("--url", default=None, help="Alamat Umami (default: ENV UMAMI_URL, simpan-alamat, "
                                              "atau http://localhost:3000)")
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--izinkan-jarak-jauh", dest="izinkan_jarak_jauh", action="store_true",
                   help="Izinkan --url server internet (HTTPS) yang diketik pengguna sendiri")
    p.add_argument("--situs", default=None, help="Nama/domain/id website (default ENV UMAMI_SITUS)")
    p.add_argument("--tz", default="WIB", choices=list(TZ))
    p.add_argument("--json", action="store_true")
    p.add_argument("--timeout", type=float, default=20.0)
    if periode:
        p.add_argument("--periode", default=periode_default, choices=PERIODE)
        p.add_argument("--dari", default=None, help="Tanggal awal YYYY-MM-DD (bersama --sampai)")
        p.add_argument("--sampai", default=None, help="Tanggal akhir YYYY-MM-DD (inklusif)")
        p.add_argument("--sekarang", default=None, help=argparse.SUPPRESS)
        p.add_argument("--batas", type=int, default=10, help="Jumlah baris teratas")


def buat_parser():
    ap = argparse.ArgumentParser(prog="umami.py", description="Laporan analitik web Umami (Komunitech)")
    ap.add_argument("--versi", action="version", version=f"umami-analitik {VERSI}")
    sub = ap.add_subparsers(dest="perintah", required=True)
    p = sub.add_parser("simpan-kunci")
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--ya", action="store_true")
    p = sub.add_parser("simpan-alamat")
    p.add_argument("alamat")
    _opsi_umum(sub.add_parser("cek"), periode=False)
    _opsi_umum(sub.add_parser("situs"), periode=False)
    for nama in ("ringkasan", "sumber", "utm", "konversi"):
        _opsi_umum(sub.add_parser(nama))
    p = sub.add_parser("halaman")
    _opsi_umum(p)
    p.add_argument("--jenis", choices=["teratas", "masuk", "keluar"], default="teratas")
    p = sub.add_parser("pengunjung")
    _opsi_umum(p)
    p.add_argument("--semua", action="store_true", help="Tambah browser, sistem operasi, bahasa")
    _opsi_umum(sub.add_parser("banding"), "minggu-ini")
    _opsi_umum(sub.add_parser("tautan"))
    p = sub.add_parser("ekspor-csv")
    _opsi_umum(p)
    p.add_argument("--keluaran", default=None)
    p.add_argument("--pemisah", choices=["titik-koma", "koma"], default="titik-koma")
    _opsi_umum(sub.add_parser("laporan-mingguan"), "minggu-lalu")
    return ap


PERINTAH = {"cek": cmd_cek, "situs": cmd_situs, "ringkasan": cmd_ringkasan, "halaman": cmd_halaman,
            "sumber": cmd_sumber, "utm": cmd_utm, "pengunjung": cmd_pengunjung, "banding": cmd_banding,
            "konversi": cmd_konversi, "tautan": cmd_tautan, "ekspor-csv": cmd_ekspor_csv, "laporan-mingguan": cmd_laporan_mingguan}


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        if args.perintah == "simpan-kunci":
            return simpan_kunci(args)
        if args.perintah == "simpan-alamat":
            return simpan_alamat(args)
        if args.url:
            args.url = args.url.strip().rstrip("/")
            periksa_url(args.url, izinkan_publik=args.izinkan_jarak_jauh)
        else:
            args.url, dari_pengguna = alamat_awal()
            args.url = args.url.rstrip("/")
            periksa_url(args.url, izinkan_publik=dari_pengguna)
        if getattr(args, "batas", 10) is not None and getattr(args, "batas", 10) < 1:
            raise Gagal("--batas minimal 1.", K_INPUT)
        if hasattr(args, "periode"):
            rentang(args)  # validasi tanggal sebelum menghubungi server
        hasil = PERINTAH[args.perintah](Klien(args), args)
        cetak(hasil, args)
        return 0
    except Gagal as e:
        sys.stderr.write(f"GALAT: {e}\n")
        return e.kode
    except KeyboardInterrupt:
        sys.stderr.write("Dibatalkan.\n")
        return 130


if __name__ == "__main__":
    sys.exit(main())
