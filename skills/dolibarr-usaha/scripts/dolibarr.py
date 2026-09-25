#!/usr/bin/env python3
"""Asisten Dolibarr lokal untuk UMKM (Komunitech) - memakai REST API resmi Dolibarr.

Hanya Python standar (urllib). Lintas OS: macOS/Linux `python3`, Windows `python` atau `py`.

Prinsip keamanan:
- Default HANYA BACA. Perintah yang menulis (tambah pelanggan, buat draf invoice) hanya
  menampilkan PRATINJAU kecuali diberi `--ya`.
- Invoice selalu dibuat sebagai DRAF. Script ini tidak punya perintah validasi, kirim,
  bayar, atau hapus.
- Kunci API dibaca dari --kunci-file (selalu menang), ENV DOLIBARR_API_KEY, atau file lokal berizin ketat; tidak pernah
  dicetak (disamarkan) dan tidak pernah dikirim lewat proxy untuk alamat lokal.
- Alamat selain komputer ini (localhost) ditolak kecuali `--izinkan-url-luar`.

Perintah:
  cek                              koneksi, versi, modul, hak akses kunci API
  simpan-kunci                     simpan kunci API ke file lokal (izin 600)
  pelanggan cari KATA              cari pelanggan (nama/alias/email/telepon/kode)
  pelanggan tambah --nama ...      tambah pelanggan (pratinjau; --ya untuk menyimpan)
  invoice buat --pelanggan ID --item ...   buat DRAF invoice (pratinjau; --ya untuk menyimpan)
  piutang                          invoice belum lunas + umur piutang
  stok [KATA]                      cek stok produk; `stok --menipis` hanya yang menipis/habis
  laporan-harian                   ringkasan penjualan harian untuk pemilik (jadwal OpenClaw)

Kode keluar: 0 berhasil | 2 argumen/input salah | 3 Dolibarr tidak bisa dihubungi |
4 modul/API belum aktif | 5 kunci salah/hak akses kurang | 6 galat lain dari Dolibarr |
7 tidak dibuat karena kemungkinan data ganda (pelanggan/draf sudah ada, atau draf kosong/belum
lengkap tertinggal dari percobaan yang terputus) | 8 koneksi putus/timeout SAAT MENULIS: data mungkin
sudah (sebagian) tersimpan, atau draf tersimpan tetapi tidak lengkap - cek Dolibarr, JANGAN langsung mengulang.
"""
import argparse
import datetime as dt
import hashlib
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
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

VERSI_SKRIP = "1.0.4"
URL_DEFAULT = "http://localhost/dolibarr"
VERSI_TERUJI = ("22.0.4", "24.0.1")
BATAS_WAKTU = 20
BATAS_JUMLAH = Decimal(1000000)          # jumlah per baris
BATAS_HARGA = Decimal(100000000000)      # Rp 100 miliar per satuan
BATAS_TEMPO = 3650                       # hari
PER_HALAMAN = 100
MAKS_HALAMAN = 50  # 5.000 baris; cukup untuk UMKM, mencegah loop tanpa akhir

# Tarif efektif PPN (standar library Komunitech): umum = 12% x DPP 11/12 = 11% x DPP.
# Di Dolibarr, tarif yang dipakai di baris invoice: umum 11, mewah 12, tanpa 0.
PPN = {
    "umum": {"tarif_dolibarr": Decimal("11"), "efektif": Decimal("0.11"),
             "label": "PPN 12% x DPP nilai lain 11/12 (efektif 11%)"},
    "mewah": {"tarif_dolibarr": Decimal("12"), "efektif": Decimal("0.12"),
              "label": "PPN 12% x DPP penuh (barang mewah)"},
    "tanpa": {"tarif_dolibarr": Decimal("0"), "efektif": Decimal("0"),
              "label": "tanpa PPN (bukan PKP / dibebaskan)"},
}

ZONA = {"WIB": 7, "WITA": 8, "WIT": 9, "Asia/Jakarta": 7, "Asia/Pontianak": 7,
        "Asia/Makassar": 8, "Asia/Jayapura": 9}
NAMA_ZONA = {7: "WIB", 8: "WITA", 9: "WIT"}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]

KELUAR_ARG, KELUAR_KONEKSI, KELUAR_MODUL, KELUAR_AKSES, KELUAR_LAIN, KELUAR_DOBEL = 2, 3, 4, 5, 6, 7
KELUAR_TIDAK_PASTI = 8  # tulis terputus: data mungkin sudah (sebagian) tersimpan di Dolibarr

PENANDA_DRAF = "Draf dibuat oleh skill dolibarr-usaha"

_RAHASIA = []  # nilai yang wajib disamarkan dari semua keluaran


# ------------------------------------------------------------------ utilitas umum
class Gagal(Exception):
    def __init__(self, pesan, kode=KELUAR_LAIN, http=None, saran=None, mungkin_terkirim=False):
        super().__init__(pesan)
        self.pesan = pesan
        self.kode = kode
        self.http = http
        self.saran = saran
        # True = permintaan TULIS mungkin sudah sampai & diproses Dolibarr walau jawabannya tidak diterima
        self.mungkin_terkirim = mungkin_terkirim


def samarkan(teks):
    teks = str(teks)
    for r in _RAHASIA:
        if r and r in teks:
            teks = teks.replace(r, samarkan_kunci(r))
    return teks


def samarkan_kunci(k):
    if not k:
        return "(kosong)"
    return "****" + k[-4:] if len(k) >= 12 else "****"


def cetak(teks="", file=None):
    print(samarkan(teks), file=file or sys.stdout)


def desimal(nilai, bawaan=Decimal(0)):
    if nilai is None or nilai == "":
        return bawaan
    try:
        return Decimal(str(nilai))
    except (InvalidOperation, ValueError):
        return bawaan


def rupiah_bulat(d):
    return Decimal(d).quantize(Decimal(1), ROUND_HALF_UP)


def format_rp(d):
    d = Decimal(d)
    neg = d < 0
    d = abs(d)
    bulat = d.quantize(Decimal(1), ROUND_FLOOR)
    pecahan = d - bulat
    s = "{:,}".format(int(bulat)).replace(",", ".")
    if pecahan:
        sen = (pecahan * 100).quantize(Decimal(1), ROUND_HALF_UP)
        if sen == 100:
            s = "{:,}".format(int(bulat) + 1).replace(",", ".")
        else:
            s += ",{:02d}".format(int(sen))
    return ("-Rp " if neg else "Rp ") + s


def format_angka(d):
    d = Decimal(d).normalize()
    if d == d.to_integral_value():
        return "{:,}".format(int(d)).replace(",", ".")
    return str(d).replace(".", ",")


def persen_ubah(sekarang, banding):
    """(sekarang - banding) / banding x 100, 1 desimal, 0,05 menjauhi nol. None bila tak bisa."""
    sekarang, banding = Decimal(sekarang), Decimal(banding)
    if banding <= 0:
        return None
    p = ((sekarang - banding) / banding * 100).quantize(Decimal("0.1"), ROUND_HALF_UP)
    return p


def ke_json(o):
    if isinstance(o, Decimal):
        return int(o) if o == o.to_integral_value() else float(o)
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()
    raise TypeError(str(type(o)))


def inisial(nama):
    bagian = [b for b in re.split(r"\s+", str(nama or "").strip()) if b]
    return ".".join(b[0].upper() for b in bagian[:3]) + "." if bagian else "?"


# ------------------------------------------------------------------ tanggal & zona
def zona_offset(nama):
    if nama not in ZONA:
        raise Gagal("Zona waktu '{}' tidak dikenal. Pakai WIB, WITA, atau WIT.".format(nama), KELUAR_ARG)
    return ZONA[nama]


def sekarang_lokal(offset):
    return dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=offset)


def tanggal_dari_ts(ts, offset):
    """Timestamp tanggal Dolibarr (detik UTC) -> tanggal kalender di zona toko.

    Kolom tanggal Dolibarr (tanggal invoice, jatuh tempo) dikirim sebagai timestamp tengah malam
    menurut zona PHP server, yang bisa berbeda dengan zona toko (mis. DoliWamp = UTC, server Bali =
    WITA, hosting luar negeri). Dibulatkan ke tanggal terdekat (+12 jam kurang 1 detik lalu dipotong) agar
    tidak mundur/maju satu hari selama server paling jauh 12 jam di barat atau 11 jam di timur zona toko."""
    if ts in (None, "", 0, "0"):
        return None
    try:
        t = int(float(ts))
        return (dt.datetime.fromtimestamp(t, dt.timezone.utc) + dt.timedelta(hours=offset + 12, seconds=-1)).date()
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def ts_siang(tanggal, offset):
    """Tanggal -> timestamp jam 12.00 zona toko (aman dari geser tanggal di server)."""
    siang = dt.datetime(tanggal.year, tanggal.month, tanggal.day, 12, 0,
                        tzinfo=dt.timezone(dt.timedelta(hours=offset)))
    return int(siang.timestamp())


def parse_tanggal(teks, offset):
    hari_ini = sekarang_lokal(offset).date()
    t = (teks or "hari-ini").strip().lower()
    if t in ("hari-ini", "hariini", "today", "sekarang"):
        return hari_ini
    if t in ("kemarin", "yesterday"):
        return hari_ini - dt.timedelta(days=1)
    for pola in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(teks.strip(), pola).date()
        except ValueError:
            pass
    raise Gagal("Tanggal '{}' tidak dikenali. Contoh: hari-ini, kemarin, 2026-09-24, 24/09/2026."
                .format(teks), KELUAR_ARG)


def tanggal_panjang(t):
    return "{}, {} {} {}".format(HARI[t.weekday()], t.day, BULAN[t.month], t.year)


# ------------------------------------------------------------------ konfigurasi & kunci
def lokasi_file_kunci():
    return os.path.join(os.path.expanduser("~"), ".komunitech", "dolibarr-kunci.txt")


def izin_file_aman(path):
    if os.name == "nt":
        return True  # Windows: izin diatur lewat folder profil pengguna
    mode = stat.S_IMODE(os.stat(path).st_mode)
    return (mode & 0o077) == 0


def bersihkan_kunci(mentah, sumber):
    """Kunci API harus satu baris tanpa spasi. Spasi/baris baru di ujung dibuang; di tengah = ditolak.
    Semua potongan nilai mentah didaftarkan sebagai rahasia agar tidak pernah tercetak utuh."""
    mentah = (mentah or "").replace("\ufeff", "")
    for potong in re.split(r"\s+", mentah):
        if len(potong) >= 4:
            _RAHASIA.append(potong)
    k = mentah.strip()
    if not k:
        return ""
    if re.search(r"\s", k) or not re.fullmatch(r"[\x21-\x7e]+", k):
        raise Gagal("Kunci API dari {} berisi spasi, baris baru, atau karakter aneh di tengahnya, jadi tidak "
                    "dipakai.".format(sumber), KELUAR_AKSES,
                    saran="Salin ulang kunci dari Dolibarr (tombol salin di kolom Token for API) lalu simpan "
                          "lagi dengan `simpan-kunci`. File kunci harus berisi satu baris saja.")
    if len(k) < 8:
        raise Gagal("Kunci API dari {} terlalu pendek (kurang dari 8 karakter).".format(sumber), KELUAR_AKSES)
    return k


def baca_kunci(path_file=None):
    """Urutan sumber kunci: --kunci-file (eksplisit, selalu menang) > ENV DOLIBARR_API_KEY >
    ENV DOLIBARR_API_KEY_FILE > file default. Mengembalikan (kunci, sumber, peringatan)."""
    peringatan = None
    env_mentah = os.environ.get("DOLIBARR_API_KEY", "")
    if path_file:
        # Nilai eksplisit menang. ENV tetap didaftarkan sebagai rahasia (tidak pernah tercetak), tidak divalidasi.
        if env_mentah.strip():
            try:
                bersihkan_kunci(env_mentah, "ENV DOLIBARR_API_KEY")
            except Gagal:
                pass
            peringatan = ("PERINGATAN: ENV DOLIBARR_API_KEY juga terisi, tetapi DIABAIKAN karena --kunci-file "
                          "diberikan. Kunci yang dipakai: file {}. Kosongkan ENV itu bila tidak diperlukan."
                          .format(os.path.expanduser(path_file)))
        path = os.path.expanduser(path_file)
        if not os.path.isfile(path):
            raise Gagal("File kunci {} (dari --kunci-file) tidak ditemukan.".format(path), KELUAR_AKSES,
                        saran="Periksa ejaan path, atau simpan kunci ke file itu dulu dengan: "
                              "python3 scripts/dolibarr.py simpan-kunci --kunci-file \"{}\"".format(path))
    else:
        k = bersihkan_kunci(env_mentah, "ENV DOLIBARR_API_KEY")
        if k:
            return k, "ENV DOLIBARR_API_KEY", None
        path = os.path.expanduser(os.environ.get("DOLIBARR_API_KEY_FILE") or lokasi_file_kunci())
    if os.path.isfile(path):
        if not izin_file_aman(path):
            raise Gagal("File kunci {} bisa dibaca pengguna lain. Amankan dulu dengan: chmod 600 \"{}\""
                        .format(path, path), KELUAR_AKSES)
        try:
            with open(path, encoding="utf-8") as f:
                isi = f.read(4096)
        except (OSError, UnicodeDecodeError) as e:
            raise Gagal("File kunci {} tidak bisa dibaca ({}).".format(path, type(e).__name__), KELUAR_AKSES)
        k = bersihkan_kunci(isi, "file " + path)
        if k:
            return k, "file " + path, peringatan
        if path_file:
            raise Gagal("File kunci {} (dari --kunci-file) kosong.".format(path), KELUAR_AKSES,
                        saran="Isi lagi dengan: python3 scripts/dolibarr.py simpan-kunci --kunci-file \"{}\" --ya"
                              .format(path))
    raise Gagal(
        "Kunci API Dolibarr belum diatur.",
        KELUAR_AKSES,
        saran="Buat kunci di Dolibarr (Pengguna & Grup > user API > Token for API), lalu jalankan "
              "SENDIRI di terminal: python3 scripts/dolibarr.py simpan-kunci . Jangan tempel kunci di chat.")


def cek_url(url, izinkan_luar):
    """Validasi URL dasar Dolibarr. Kembalikan (url_bersih, lokal:bool, catatan:list)."""
    url = (url or "").strip().rstrip("/")
    if url.endswith("/api/index.php"):
        url = url[: -len("/api/index.php")]
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise Gagal("Alamat Dolibarr '{}' tidak valid. Contoh: http://localhost/dolibarr".format(url), KELUAR_ARG)
    if p.username or p.password:
        raise Gagal("Jangan menaruh nama/sandi di alamat Dolibarr.", KELUAR_ARG)
    host = p.hostname.lower()
    catatan = []
    loopback = host == "localhost" or host.endswith(".localhost")
    privat = False
    try:
        ip = ipaddress.ip_address(host)
        loopback = loopback or ip.is_loopback
        privat = ip.is_private and not ip.is_loopback
    except ValueError:
        pass
    if loopback:
        return url, True, catatan
    if not izinkan_luar:
        raise Gagal(
            "Alamat {} bukan komputer ini. Demi keamanan, skill ini hanya bicara dengan Dolibarr lokal."
            .format(host), KELUAR_ARG,
            saran="Jika Dolibarr memang di komputer/server lain milik Anda, ulangi dengan --izinkan-url-luar "
                  "(atau ENV DOLIBARR_IZINKAN_URL_LUAR=1) dan pastikan memakai https://.")
    if p.scheme != "https":
        if privat:
            catatan.append("PERINGATAN: koneksi ke {} memakai http (tidak terenkripsi). Aman hanya di jaringan "
                           "kantor sendiri; sebaiknya pakai https.".format(host))
        else:
            raise Gagal("Alamat internet wajib https:// agar kunci API tidak bisa disadap.", KELUAR_ARG)
    else:
        catatan.append("Terhubung ke Dolibarr di luar komputer ini ({}). Pastikan server itu milik Anda."
                       .format(host))
    return url, privat, catatan


# ------------------------------------------------------------------ klien HTTP
class _TolakRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Gagal("Dolibarr mengalihkan permintaan ke {} (kode {}). Kunci API tidak dikirim ulang."
                    .format(newurl, code), KELUAR_LAIN,
                    saran="Periksa alamat DOLIBARR_URL (mungkin harus https:// atau ada '/' berbeda).")


def _pesan_error_json(body):
    try:
        d = json.loads(body)
    except (ValueError, TypeError):
        return None
    if isinstance(d, dict) and isinstance(d.get("error"), dict):
        return str(d["error"].get("message") or "")
    return None


class Dolibarr:
    def __init__(self, url, kunci, lokal=True):
        self.url = url
        self.kunci = kunci
        _RAHASIA.append(kunci)
        handler = [_TolakRedirect()]
        if lokal:
            handler.append(urllib.request.ProxyHandler({}))  # jangan lewatkan kunci ke proxy
        self.opener = urllib.request.build_opener(*handler)

    def minta(self, metode, jalur, params=None, data=None, daftar=False):
        u = "{}/api/index.php/{}".format(self.url, jalur.lstrip("/"))
        if params:
            u += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        body = None
        header = {"DOLAPIKEY": self.kunci, "Accept": "application/json",
                  "User-Agent": "komunitech-dolibarr-usaha/" + VERSI_SKRIP}
        if data is not None:
            body = json.dumps(data).encode("utf-8")
            header["Content-Type"] = "application/json"
        req = urllib.request.Request(u, data=body, headers=header, method=metode)
        try:
            with self.opener.open(req, timeout=BATAS_WAKTU) as r:
                kode, teks = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            kode, teks = e.code, e.read().decode("utf-8", "replace")
        except Gagal:
            raise
        except urllib.error.URLError as e:
            # Koneksi ditolak / nama tidak dikenal = permintaan pasti belum terkirim. Selain itu (timeout,
            # putus saat mengirim) permintaan tulis mungkin sudah sampai.
            if metode != "GET" and not isinstance(e.reason, (ConnectionRefusedError, socket.gaierror)):
                raise self._gagal_tulis(e.reason)
            raise Gagal("Dolibarr di {} tidak bisa dihubungi ({}).".format(self.url, e.reason),
                        KELUAR_KONEKSI,
                        saran="Nyalakan Dolibarr dulu (Windows: menu Start > Dolibarr > Tools > Start DoliWamp server), "
                              "lalu buka {} di browser untuk memastikan.".format(self.url))
        except (TimeoutError, OSError) as e:
            if metode != "GET":
                raise self._gagal_tulis(e)
            raise Gagal("Dolibarr tidak menjawab dalam {} detik ({}).".format(BATAS_WAKTU, e), KELUAR_KONEKSI,
                        saran="Komputer mungkin sibuk atau Dolibarr macet; coba lagi, atau mulai ulang DoliWamp.")
        return self._olah(kode, teks, daftar)

    @staticmethod
    def _gagal_tulis(sebab):
        """Timeout/putus pada permintaan TULIS: jangan sarankan 'coba lagi' (bisa dobel) - minta cek dulu (C1)."""
        return Gagal("Koneksi ke Dolibarr putus atau tidak dijawab dalam {} detik SAAT MENGIRIM data ({}). "
                     "Data ini MUNGKIN SUDAH TERSIMPAN di Dolibarr.".format(BATAS_WAKTU, sebab), KELUAR_TIDAK_PASTI,
                     saran="JANGAN langsung mengulang perintah. Buka Dolibarr di browser dan periksa dulu apakah "
                           "datanya sudah masuk (pelanggan: menu Pihak Ketiga; invoice: menu Tagihan/Nota, status "
                           "Draf). Ulangi hanya bila memang belum ada.",
                     mungkin_terkirim=True)

    def _olah(self, kode, teks, daftar):
        pesan = _pesan_error_json(teks)
        polos = re.sub(r"<[^>]+>", "", teks or "").strip()
        if kode == 200:
            try:
                return json.loads(teks) if teks.strip() else None
            except ValueError:
                if re.search(r"\bApi\b.*(must be enabled|harus diaktifkan)", polos, re.I | re.S):
                    raise Gagal("Modul 'API / Web services (REST server)' di Dolibarr belum aktif.", KELUAR_MODUL,
                                saran="Masuk Dolibarr sebagai admin > Pengaturan > Modul/Aplikasi > aktifkan "
                                      "'API / Layanan Web (server REST)'. Lihat docs/panduan-dolibarr.md.")
                raise Gagal("Jawaban Dolibarr bukan data JSON (mungkin alamat salah): {}"
                            .format(polos[:160]), KELUAR_LAIN,
                            saran="Pastikan DOLIBARR_URL menunjuk ke folder Dolibarr, mis. http://localhost/dolibarr")
        if kode == 401:
            raise Gagal("Kunci API ditolak Dolibarr (401). Kunci salah, sudah diganti, atau user-nya nonaktif.",
                        KELUAR_AKSES, http=401,
                        saran="Buat ulang kunci di Dolibarr (Pengguna & Grup > user API > Token for API) "
                              "lalu simpan lagi dengan `simpan-kunci`.")
        if kode == 403:
            raise Gagal("Ditolak Dolibarr (403: {}). User API belum punya hak untuk ini, atau modulnya belum "
                        "aktif.".format(pesan or "Forbidden"), KELUAR_AKSES, http=403,
                        saran="Jalankan `cek` untuk melihat modul & hak yang kurang; atur di Dolibarr "
                              "(Pengguna & Grup > user API > Izin). Lihat docs/panduan-dolibarr.md.")
        if kode == 404:
            if daftar and pesan is not None:
                return []  # Dolibarr menjawab 404 untuk daftar kosong (mis. pihak ketiga)
            if pesan is not None:
                raise Gagal("Data tidak ditemukan di Dolibarr ({}).".format(pesan), KELUAR_LAIN, http=404)
            raise Gagal("Alamat API tidak ditemukan (404). DOLIBARR_URL kemungkinan salah.", KELUAR_ARG, http=404,
                        saran="Buka alamat Dolibarr Anda di browser; salin bagian sebelum '/index.php' atau "
                              "'/admin', mis. http://localhost/dolibarr")
        if kode == 501:
            raise Gagal("Modul Dolibarr untuk data ini belum aktif ({}).".format(polos[:120] or "501"),
                        KELUAR_MODUL, http=501,
                        saran="Aktifkan modulnya di Pengaturan > Modul/Aplikasi (Pihak Ketiga, Nota/Invoice, "
                              "Produk, Stok).")
        if kode == 503 and "not allowed from your IP" in (teks or ""):
            raise Gagal("Dolibarr menolak alamat IP komputer ini untuk API.", KELUAR_AKSES, http=503)
        raise Gagal("Dolibarr mengembalikan galat {}: {}".format(kode, pesan or polos[:200]), KELUAR_LAIN, http=kode)

    def daftar_semua(self, jalur, params):
        hasil = []
        for hal in range(MAKS_HALAMAN):
            p = dict(params)
            p.update({"limit": PER_HALAMAN, "page": hal})
            bagian = self.minta("GET", jalur, p, daftar=True) or []
            if isinstance(bagian, dict) and "data" in bagian:
                bagian = bagian["data"]
            if not isinstance(bagian, list):
                raise Gagal("Bentuk jawaban {} tidak dikenal (bukan daftar).".format(jalur), KELUAR_LAIN)
            hasil.extend(bagian)
            if len(bagian) < PER_HALAMAN:
                break
        return hasil


def kata_aman(teks):
    """Bersihkan kata kunci pencarian untuk sqlfilters Dolibarr (tanpa kutip/kurung/wildcard)."""
    t = re.sub(r"[()'\"%\\:_*]", " ", str(teks or ""))
    t = re.sub(r"\s+", " ", t).strip()
    return t[:60]


# ------------------------------------------------------------------ perintah: cek
HAK_PENTING = [
    ("societe", "lire", None, "baca pelanggan (Pihak Ketiga)"),
    ("societe", "client", "voir", "lihat SEMUA pelanggan (bukan hanya yang ditautkan)"),
    ("facture", "lire", None, "baca invoice/nota pelanggan"),
    ("produit", "lire", None, "baca produk"),
    ("stock", "lire", None, "baca stok"),
    ("societe", "creer", None, "tambah/ubah pelanggan (menulis)"),
    ("facture", "creer", None, "buat/ubah draf invoice (menulis)"),
]
HAK_BERISIKO = [
    ("facture", "invoice_advance", "validate", "memvalidasi invoice"),
    ("facture", "paiement", None, "mencatat pembayaran"),
    ("facture", "supprimer", None, "menghapus invoice"),
    ("facture", "invoice_advance", "send", "mengirim invoice lewat email"),
    ("societe", "supprimer", None, "menghapus pelanggan"),
    ("produit", "creer", None, "mengubah produk/harga"),
    ("produit", "supprimer", None, "menghapus produk"),
    ("stock", "mouvement", "creer", "mengubah stok"),
    ("user", "user", "creer", "membuat/mengubah pengguna"),
]


def punya_hak(hak, modul, a, b):
    m = hak.get(modul) or {}
    v = m.get(a)
    if b is None:
        return (not isinstance(v, dict)) and bool(v)
    return isinstance(v, dict) and bool(v.get(b))


def cmd_cek(api, args, catatan_url, sumber_kunci):
    out = {"url": api.url, "kunci": samarkan_kunci(api.kunci), "sumber_kunci": sumber_kunci,
           "catatan": list(catatan_url)}
    st = api.minta("GET", "status")
    s = (st or {}).get("success") or {}
    versi = str(s.get("dolibarr_version") or "?")
    out["versi"] = versi
    out["versi_teruji"] = versi in VERSI_TERUJI
    if str(s.get("access_locked", "0")) not in ("0", "", "None"):
        out["catatan"].append("Dolibarr sedang dikunci untuk login tertentu (MAIN_ONLY_LOGIN_ALLOWED).")

    user = None
    try:
        user = api.minta("GET", "users/info", {"includepermissions": 1})
    except Gagal as e:
        if e.http != 403:
            raise
        out["catatan"].append("Daftar hak akses tidak bisa dibaca (user API tidak punya hak "
                              "'Buat/ubah pengguna sendiri'). Hak diperkirakan dari uji baca di bawah.")
    hak = {}
    if isinstance(user, dict):
        out["login"] = user.get("login")
        out["admin"] = str(user.get("admin")) == "1"
        hak = user.get("rights") or {}
        out["hak"] = {label: punya_hak(hak, m, a, b) for m, a, b, label in HAK_PENTING}
        out["hak_berisiko"] = [label for m, a, b, label in HAK_BERISIKO if punya_hak(hak, m, a, b)]

    uji = [("thirdparties", "Pihak Ketiga (pelanggan)"), ("invoices", "Nota/Invoice pelanggan"),
           ("products", "Produk"), ("warehouses", "Stok (gudang)")]
    out["modul"] = {}
    for jalur, label in uji:
        try:
            api.minta("GET", jalur, {"limit": 1}, daftar=True)
            out["modul"][label] = "aktif, bisa dibaca"
        except Gagal as e:
            if e.kode == KELUAR_MODUL:
                out["modul"][label] = "BELUM AKTIF"
            elif e.http == 403:
                out["modul"][label] = "TIDAK BISA DIBACA (modul belum aktif, atau user API tidak punya hak baca)"
            else:
                raise
    if not out["versi_teruji"]:
        out["catatan"].append("Versi {} belum diuji oleh Komunitech (teruji: {}). Periksa hasil dengan teliti."
                              .format(versi, ", ".join(VERSI_TERUJI)))
    if out.get("admin"):
        out["catatan"].append("Kunci ini milik user ADMIN. Sebaiknya buat user khusus API dengan hak minimal "
                              "(lihat docs/panduan-dolibarr.md bagian 'User khusus API').")
    if out.get("hak", {}).get("buat/ubah draf invoice (menulis)"):
        out["catatan"].append("Hak 'Buat/ubah invoice' di Dolibarr juga mengizinkan MEMVALIDASI dan MENANDAI LUNAS "
                              "invoice lewat API (bukan hanya draf). Skill ini tidak punya perintah itu, tetapi "
                              "kunci ini mampu. Untuk laporan terjadwal pakai kunci user baca-saja terpisah.")
    if out.get("hak_berisiko"):
        out["catatan"].append("User API punya hak yang tidak dibutuhkan skill ini: {}. Cabut di Dolibarr "
                              "agar lebih aman.".format(", ".join(out["hak_berisiko"])))

    b = ["CEK DOLIBARR", "Alamat: {}".format(api.url), "Versi Dolibarr: {}{}".format(
        versi, "" if out["versi_teruji"] else " (belum diuji Komunitech)"),
         "Kunci API: {} (dari {})".format(out["kunci"], sumber_kunci)]
    if "login" in out:
        b.append("User API: {}{}".format(out["login"], " (ADMIN)" if out.get("admin") else ""))
    b.append("")
    b.append("MODUL")
    for label, v in out["modul"].items():
        b.append("- {}: {}".format(label, v))
    if out.get("hak"):
        b.append("")
        b.append("HAK AKSES KUNCI")
        for label, ada in out["hak"].items():
            b.append("- [{}] {}".format("x" if ada else " ", label))
    if out["catatan"]:
        b.append("")
        b.append("CATATAN")
        for i, c in enumerate(out["catatan"], 1):
            b.append("{}. {}".format(i, c))
    out["teks"] = "\n".join(b)
    return out


# ------------------------------------------------------------------ perintah: simpan-kunci
def cmd_simpan_kunci(args):
    import getpass
    path = os.path.abspath(os.path.expanduser(args.kunci_file or lokasi_file_kunci()))
    if os.path.exists(path) and not args.ya:
        lama = ""
        try:
            with open(path, encoding="utf-8") as f:
                lama = bersihkan_kunci(f.read(4096), "file " + path)
        except (Gagal, OSError, UnicodeDecodeError):
            pass
        raise Gagal("File kunci {} sudah ada{}. Tidak ditimpa.".format(
            path, " (berisi kunci {})".format(samarkan_kunci(lama)) if lama else ""), KELUAR_ARG,
            saran="Untuk kunci KEDUA (mis. pembuat draf) pakai file lain: simpan-kunci --kunci-file "
                  "~/.komunitech/dolibarr-kunci-draf.txt . Untuk mengganti kunci ini, ulangi dengan --ya.")
    cetak("Kunci akan disimpan di: {}".format(path), file=sys.stderr)
    if sys.stdin.isatty():
        k = getpass.getpass("Tempel kunci API Dolibarr (tidak akan tampil), lalu Enter: ").strip()
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
    teks = "Kunci {} disimpan di {} (hanya bisa dibaca akun Anda){}.".format(
        samarkan_kunci(k), path, "" if args.kunci_file else " - file default, dipakai laporan terjadwal")
    return {"file": path, "kunci": samarkan_kunci(k), "teks": teks}


# ------------------------------------------------------------------ perintah: pelanggan
def ringkas_pelanggan(t):
    return {"id": int(t.get("id")), "nama": t.get("name") or t.get("nom") or "",
            "alias": t.get("name_alias") or "", "kode": t.get("code_client") or "",
            "telepon": t.get("phone") or t.get("phone_mobile") or "", "email": t.get("email") or "",
            "kota": t.get("town") or "", "status": "aktif" if str(t.get("status", "1")) == "1" else "nonaktif"}


def norm_hp(teks):
    """Nomor telepon -> bentuk baku 08xxx: buang spasi/strip/titik/kurung; +62/62 -> 0; 8xx -> 08xx."""
    d = re.sub(r"\D", "", str(teks or ""))
    if d.startswith("62"):
        d = "0" + d[2:]
    elif d.startswith("8"):
        d = "0" + d
    return d


def mirip_nomor(kata):
    """Kata pencarian yang berupa nomor telepon (>= 6 angka, hanya angka/spasi/strip/titik/+/kurung)."""
    return bool(re.fullmatch(r"[\d\s\-\.\+\(\)]+", kata or "")) and len(re.sub(r"\D", "", kata)) >= 6


PROP_PELANGGAN = "id,name,name_alias,code_client,phone,phone_mobile,email,town,status"


def semua_pelanggan(api):
    return api.daftar_semua("thirdparties", {"sortfield": "t.nom", "sortorder": "ASC",
                                             "properties": PROP_PELANGGAN})


def cari_pelanggan(api, kata):
    if mirip_nomor(kata):
        # Nomor disimpan Dolibarr apa adanya (0812-..., +62 812 ...): cocokkan setelah dinormalkan.
        cari = norm_hp(kata)
        return [ringkas_pelanggan(t) for t in semua_pelanggan(api)
                if any(cari in norm_hp(t.get(f)) for f in ("phone", "phone_mobile") if t.get(f))]
    k = kata_aman(kata)
    if len(k) < 2:
        raise Gagal("Kata pencarian terlalu pendek (minimal 2 huruf/angka).", KELUAR_ARG)
    kolom = ["t.nom", "t.name_alias", "t.email", "t.phone", "t.code_client"]
    filt = " or ".join("({}:like:'%{}%')".format(c, k) for c in kolom)
    data = api.daftar_semua("thirdparties", {"sqlfilters": "(" + filt + ")", "sortfield": "t.nom",
                                             "sortorder": "ASC", "properties": PROP_PELANGGAN})
    return [ringkas_pelanggan(t) for t in data]


def cmd_pelanggan_cari(api, args):
    hasil = cari_pelanggan(api, args.kata)
    b = ["CARI PELANGGAN: '{}'".format(norm_hp(args.kata) if mirip_nomor(args.kata) else kata_aman(args.kata))]
    if not hasil:
        b.append("Tidak ada pelanggan yang cocok. Untuk menambah: pelanggan tambah --nama \"...\"")
    for p in hasil[:30]:
        info = [x for x in (p["kode"], p["telepon"], p["email"], p["kota"]) if x]
        b.append("- ID {}: {}{}{}".format(p["id"], p["nama"], " ({})".format(p["alias"]) if p["alias"] else "",
                                          " | " + " | ".join(info) if info else ""))
    if len(hasil) > 30:
        b.append("... dan {} lainnya. Persempit kata pencarian.".format(len(hasil) - 30))
    return {"kata": kata_aman(args.kata), "jumlah": len(hasil), "pelanggan": hasil, "teks": "\n".join(b)}


def cmd_pelanggan_tambah(api, args):
    nama = (args.nama or "").strip()
    if len(nama) < 2:
        raise Gagal("Nama pelanggan wajib diisi (--nama).", KELUAR_ARG)
    telp = re.sub(r"[^\d+]", "", args.telepon or "")
    if args.telepon and not re.fullmatch(r"\+?\d{8,15}", telp):
        raise Gagal("Nomor telepon '{}' tidak wajar (8-15 angka).".format(args.telepon), KELUAR_ARG)
    email = (args.email or "").strip()
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise Gagal("Email '{}' tidak valid.".format(email), KELUAR_ARG)
    data = {"name": nama, "client": 1, "code_client": "auto", "country_id": 118}
    if telp:
        data["phone"] = telp
    if email:
        data["email"] = email
    if args.alamat:
        data["address"] = args.alamat.strip()
    if args.kota:
        data["town"] = args.kota.strip()
    if args.catatan:
        data["note_private"] = args.catatan.strip()

    mirip = []
    try:
        mirip = [dict(p, alasan="nama mirip") for p in cari_pelanggan(api, nama)]
    except Gagal as e:
        if e.kode != KELUAR_ARG:
            raise
    if telp or email:
        # Ganda per nomor HP (dinormalkan 62.../+62/strip) dan per email (huruf kecil)
        sudah = {p["id"] for p in mirip}
        hp = norm_hp(telp)
        for t in semua_pelanggan(api):
            alasan = []
            if hp and any(norm_hp(t.get(f)) == hp for f in ("phone", "phone_mobile") if t.get(f)):
                alasan.append("nomor HP sama")
            if email and (t.get("email") or "").strip().lower() == email.lower():
                alasan.append("email sama")
            if alasan:
                p = ringkas_pelanggan(t)
                if p["id"] in sudah:
                    for m in mirip:
                        if m["id"] == p["id"]:
                            m["alasan"] += ", " + ", ".join(alasan)
                else:
                    mirip.append(dict(p, alasan=", ".join(alasan)))
    b = ["PRATINJAU PELANGGAN BARU" if not args.ya else "TAMBAH PELANGGAN",
         "Nama: {}".format(nama), "Telepon: {}".format(telp or "-"), "Email: {}".format(email or "-"),
         "Alamat: {}".format(data.get("address", "-")), "Kota: {}".format(data.get("town", "-")),
         "Kode pelanggan: dibuat otomatis oleh Dolibarr", "Negara: Indonesia"]
    out = {"data": data, "mirip": mirip, "dibuat": False}
    if mirip:
        b.append("")
        b.append("Kemungkinan pelanggan yang sama sudah ada:")
        for p in mirip[:5]:
            b.append("- ID {}: {} {} {} ({})".format(p["id"], p["nama"], p["telepon"], p["email"], p["alasan"])
                     .replace("  ", " "))
        if not args.tetap_buat:
            b.append("Tidak dibuat untuk mencegah data ganda. Pakai ID di atas, atau ulangi dengan --tetap-buat.")
            if args.ya:
                out["kode_keluar"] = KELUAR_DOBEL
            out["teks"] = "\n".join(b)
            return out
    if not args.ya:
        b.append("")
        b.append("Belum disimpan. Jika sudah benar, ulangi perintah yang sama dengan --ya.")
        out["teks"] = "\n".join(b)
        return out
    new_id = api.minta("POST", "thirdparties", data=data)
    out["dibuat"] = True
    out["id"] = int(new_id)
    try:
        t = api.minta("GET", "thirdparties/{}".format(int(new_id)))
        out["pelanggan"] = ringkas_pelanggan(t)
        b.append("")
        b.append("TERSIMPAN: ID {} kode {}".format(out["id"], out["pelanggan"]["kode"] or "-"))
    except Gagal:
        b.append("")
        b.append("TERSIMPAN: ID {}".format(out["id"]))
    out["teks"] = "\n".join(b)
    return out


# ------------------------------------------------------------------ perintah: invoice buat
def parse_item(teks, nomor):
    """'deskripsi|qty|harga[|diskon%]' atau '@REF|qty[|harga][|diskon%]'."""
    bagian = [x.strip() for x in str(teks).split("|")]
    if len(bagian) < 2 or not bagian[0]:
        raise Gagal("Item {} '{}' tidak lengkap. Format: \"nama|jumlah|harga\" atau \"@KODEPRODUK|jumlah\"."
                    .format(nomor, teks), KELUAR_ARG)

    def angka(x, label):
        asli = x
        x = re.sub(r"(?i)^rp\.?", "", x.replace(" ", ""))
        if x.startswith("-"):
            raise Gagal("Item {}: {} tidak boleh negatif.".format(nomor, label), KELUAR_ARG)
        if re.fullmatch(r"\d{1,3}(,\d{3})+", x):
            # "62,500" / "1,250,000": gaya Inggris (ribuan) atau desimal? Jangan menebak.
            raise Gagal("Item {}: {} '{}' ambigu (62,500 bisa berarti Rp 62.500 atau Rp 62,50). Tulis tanpa "
                        "pemisah, mis. 62500, atau pakai titik untuk ribuan: 62.500.".format(nomor, label, asli),
                        KELUAR_ARG)
        if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", x):
            x = x.replace(".", "").replace(",", ".")
        elif re.fullmatch(r"\d+,\d+", x):
            x = x.replace(",", ".")
        if not re.fullmatch(r"\d+(\.\d+)?", x):
            raise Gagal("Item {}: {} '{}' bukan angka biasa (contoh benar: 3, 2,5, 85000, 85.000)."
                        .format(nomor, label, asli), KELUAR_ARG)
        d = Decimal(x)
        batas = BATAS_JUMLAH if label == "jumlah" else BATAS_HARGA
        if label != "diskon" and d > batas:
            raise Gagal("Item {}: {} {} terlalu besar (maks. {}). Periksa lagi angkanya."
                        .format(nomor, label, format_angka(d), format_angka(batas)), KELUAR_ARG)
        return d

    item = {"nomor": nomor, "produk_ref": None, "deskripsi": bagian[0], "harga": None,
            "diskon": Decimal(0)}
    if bagian[0].startswith("@"):
        item["produk_ref"] = bagian[0][1:].strip()
        item["deskripsi"] = None
    item["qty"] = angka(bagian[1], "jumlah")
    if item["qty"] == 0:
        raise Gagal("Item {}: jumlah tidak boleh 0.".format(nomor), KELUAR_ARG)
    if len(bagian) >= 3 and bagian[2] != "":
        item["harga"] = angka(bagian[2], "harga")
    if len(bagian) >= 4 and bagian[3] != "":
        item["diskon"] = angka(bagian[3].rstrip("%"), "diskon")
        if item["diskon"] > 100:
            raise Gagal("Item {}: diskon maksimal 100%.".format(nomor), KELUAR_ARG)
    if item["harga"] is None and not item["produk_ref"]:
        raise Gagal("Item {}: harga wajib diisi untuk barang/jasa tanpa kode produk.".format(nomor), KELUAR_ARG)
    return item


def hitung_invoice(items, jenis_ppn):
    """Hitung sendiri (standar library): total baris dibulatkan ke rupiah terdekat,
    PPN = DPP x tarif efektif, dibulatkan ke BAWAH sekali di tingkat invoice."""
    dpp = Decimal(0)
    for it in items:
        kotor = it["qty"] * it["harga"]
        it["total_baris"] = rupiah_bulat(kotor * (Decimal(100) - it["diskon"]) / Decimal(100))
        dpp += it["total_baris"]
    tarif = PPN[jenis_ppn]["efektif"]
    ppn_tepat = dpp * tarif
    ppn = ppn_tepat.quantize(Decimal(1), ROUND_FLOOR)
    return {"dpp": dpp, "ppn": ppn, "ppn_tepat": ppn_tepat, "total": dpp + ppn,
            "dpp_nilai_lain": (dpp * Decimal(11) / Decimal(12)).quantize(Decimal("0.01"), ROUND_HALF_UP)
            if jenis_ppn == "umum" else None}


def dpp_cara_dolibarr(items):
    """DPP seperti yang disimpan Dolibarr (total baris dibulatkan ke 2 desimal, per baris).
    Hanya untuk mengenali draf kembar; BUKAN angka hitungan Komunitech."""
    return sum((it["qty"] * it["harga"] * (Decimal(100) - it["diskon"]) / Decimal(100))
               .quantize(Decimal("0.01"), ROUND_HALF_UP) for it in items)


def draf_kembar(draf, items, dpp):
    """Draf dianggap kembar bila total_ht Dolibarr berselisih < Rp 1 dari DPP Komunitech (baris dibulatkan ke
    rupiah) ATAU dari DPP cara Dolibarr (baris 2 desimal). Dolibarr menyimpan sen, jadi pembandingan persis
    dengan DPP yang sudah dibulatkan meloloskan draf ganda (B1 v1.0.2)."""
    acuan = (Decimal(dpp), dpp_cara_dolibarr(items))
    hasil = []
    for d in draf:
        th = desimal(d.get("total_ht"), None)
        if th is not None and any(abs(th - a) < 1 for a in acuan):
            hasil.append(d)
    return hasil


def cmd_invoice_buat(api, args, offset):
    if not args.item:
        raise Gagal("Minimal satu --item. Contoh: --item \"Kopi 250g|3|85000\"", KELUAR_ARG)
    items = [parse_item(t, i) for i, t in enumerate(args.item, 1)]
    try:
        pel = api.minta("GET", "thirdparties/{}".format(int(args.pelanggan)))
    except ValueError:
        raise Gagal("--pelanggan harus ID angka. Cari dulu: pelanggan cari \"nama\"", KELUAR_ARG)
    except Gagal as e:
        if e.http == 404:
            raise Gagal("Pelanggan ID {} tidak ada. Cari dulu: pelanggan cari \"nama\"".format(args.pelanggan),
                        KELUAR_ARG)
        raise
    pel = ringkas_pelanggan(pel)

    for it in items:
        if it["produk_ref"]:
            try:
                p = api.minta("GET", "products/ref/{}".format(urllib.parse.quote(it["produk_ref"], safe="")))
            except Gagal as e:
                if e.http == 404:
                    raise Gagal("Produk dengan kode '{}' tidak ada di Dolibarr.".format(it["produk_ref"]), KELUAR_ARG)
                raise
            it["fk_product"] = int(p["id"])
            it["deskripsi"] = p.get("label") or it["produk_ref"]
            it["jenis"] = int(p.get("type") or 0)
            if it["harga"] is None:
                it["harga"] = desimal(p.get("price"))
            tva_produk = desimal(p.get("tva_tx"), None)
            if tva_produk is not None and tva_produk != PPN[args.ppn]["tarif_dolibarr"]:
                it["catatan"] = "tarif PPN produk di Dolibarr {}%, invoice memakai {}%".format(
                    format_angka(tva_produk), format_angka(PPN[args.ppn]["tarif_dolibarr"]))
        else:
            it["fk_product"] = None
            it["jenis"] = 1 if args.jasa else 0

    hit = hitung_invoice(items, args.ppn)
    tgl = parse_tanggal(args.tanggal, offset)
    tempo = tgl + dt.timedelta(days=args.jatuh_tempo)

    b = ["PRATINJAU DRAF INVOICE" if not args.ya else "DRAF INVOICE",
         "Pelanggan: {} (ID {})".format(pel["nama"], pel["id"]),
         "Tanggal: {} | jatuh tempo: {} ({} hari)".format(tgl.isoformat(), tempo.isoformat(), args.jatuh_tempo), ""]
    for it in items:
        b.append("{}. {} - {} x {}{} = {}".format(
            it["nomor"], it["deskripsi"], format_angka(it["qty"]), format_rp(it["harga"]),
            " diskon {}%".format(format_angka(it["diskon"])) if it["diskon"] else "", format_rp(it["total_baris"])))
        if it.get("catatan"):
            b.append("   catatan: " + it["catatan"])
    b += ["", "Hitungan Komunitech ({}):".format(PPN[args.ppn]["label"]),
          "DPP (jumlah harga sebelum pajak): {}".format(format_rp(hit["dpp"]))]
    if hit["dpp_nilai_lain"] is not None:
        b.append("DPP nilai lain 11/12 (informasi faktur): {}".format(format_rp(hit["dpp_nilai_lain"])))
    b += ["PPN: {} (dari {} dibulatkan ke bawah)".format(format_rp(hit["ppn"]), format_rp(hit["ppn_tepat"])),
          "TOTAL: {}".format(format_rp(hit["total"]))]
    out = {"pelanggan": pel, "items": items, "hitungan": hit, "jenis_ppn": args.ppn,
           "tanggal": tgl, "jatuh_tempo": tempo, "dibuat": False}

    if not args.ya:
        b += ["", "Belum dikirim ke Dolibarr. Jika sudah benar, ulangi perintah yang sama dengan --ya.",
              "Invoice akan dibuat sebagai DRAF (belum sah, belum bernomor final, tidak dikirim ke pelanggan)."]
        out["teks"] = "\n".join(b)
        return out

    # Cegah dobel (B1) dan draf tertinggal dari percobaan yang terputus (C1) sebelum membuat draf baru.
    kode = kode_perintah(pel["id"], items, args.ppn, tgl, tempo, args.catatan)
    draf = api.daftar_semua("invoices", {"status": "draft", "thirdparty_ids": pel["id"],
                                         "properties": "id,ref,total_ht,date,note_private"})
    kembar = draf_kembar(draf, items, hit["dpp"])
    id_kembar = {d.get("id") for d in kembar}
    tertinggal = [(d, k) for d, k in draf_tertinggal(draf, kode) if d.get("id") not in id_kembar]
    if (kembar or tertinggal) and not args.tetap_buat:
        b[0] = "DRAF INVOICE TIDAK DIBUAT ({})".format(
            "kemungkinan dobel" if kembar else "ada draf belum lengkap dari percobaan sebelumnya")
        b.append("")
        if kembar:
            b.append("DIBATALKAN: sudah ada draf untuk pelanggan ini dengan jumlah sama: {}.".format(
                ", ".join("{} (ID {})".format(d.get("ref"), d.get("id")) for d in kembar)))
        if tertinggal:
            b.append("{} ini punya draf yang tampaknya tertinggal dari percobaan sebelumnya yang "
                     "terputus:".format("Selain itu, pelanggan" if kembar else "DIBATALKAN: pelanggan"))
            for d, k in tertinggal:
                if k == "kosong":
                    ket = "kosong, Rp 0 (belum ada barang)"
                else:
                    ket = "dari perintah yang sama tetapi belum lengkap/berbeda (DPP di Dolibarr {}, seharusnya " \
                          "sekitar {})".format(format_rp(desimal(d.get("total_ht"))), format_rp(hit["dpp"]))
                b.append("- {} (ID {}): {}".format(d.get("ref"), d.get("id"), ket))
            b.append("Yang perlu dicek di Dolibarr (menu Tagihan/Nota, invoice pelanggan berstatus Draf): buka "
                     "draf di atas, lalu lengkapi barisnya sesuai pratinjau di atas, ATAU hapus draf itu dan "
                     "jalankan ulang perintah ini.")
            b.append("Jika memang ingin draf baru tanpa mengurus draf itu, ulangi dengan --tetap-buat.")
        else:
            b.append("Periksa di Dolibarr. Jika memang ingin draf baru, ulangi dengan --tetap-buat.")
        out["kembar"] = kembar
        out["draf_tertinggal"] = [dict(d, keadaan=k) for d, k in tertinggal]
        out["kode_keluar"] = KELUAR_DOBEL
        out["teks"] = "\n".join(b)
        return out

    kepala = {"socid": pel["id"], "type": 0, "date": ts_siang(tgl, offset),
              "date_lim_reglement": ts_siang(tempo, offset),
              "note_private": "{} (Komunitech). Periksa sebelum validasi. Kode perintah: {}".format(PENANDA_DRAF, kode)}
    if args.catatan:
        kepala["note_public"] = args.catatan.strip()
    out["kode_perintah"] = kode
    try:
        inv_id = int(api.minta("POST", "invoices", data=kepala))
    except Gagal as e:
        if not e.mungkin_terkirim:
            raise
        return _kepala_tidak_pasti(api, pel, kode, e, b, out)
    out["id"] = inv_id
    out["dibuat"] = True
    masalah = None
    for it in items:
        baris = {"desc": it["deskripsi"], "label": "", "subprice": str(it["harga"]), "qty": str(it["qty"]),
                 "tva_tx": str(PPN[args.ppn]["tarif_dolibarr"]), "localtax1_tx": 0, "localtax2_tx": 0,
                 "fk_product": it["fk_product"], "remise_percent": str(it["diskon"]), "date_start": "",
                 "date_end": "", "fk_code_ventilation": 0, "info_bits": 0, "fk_remise_except": None,
                 "price_base_type": "HT", "product_type": it["jenis"], "rang": -1, "special_code": 0,
                 "fk_parent_line": 0, "fk_fournprice": None, "pa_ht": 0, "array_options": [],
                 "situation_percent": 100, "fk_prev_id": None, "fk_unit": None, "origin": "", "origin_id": 0,
                 "ref_ext": ""}
        try:
            api.minta("POST", "invoices/{}/lines".format(inv_id), data=baris)
        except Gagal as e:
            masalah = {"nomor": it["nomor"], "deskripsi": it["deskripsi"], "pesan": e.pesan,
                       "mungkin_masuk": e.mungkin_terkirim}
            break
    try:
        inv = api.minta("GET", "invoices/{}".format(inv_id))
        galat_baca = None
    except Gagal as e:
        inv, galat_baca = None, e.pesan
    if masalah or not isinstance(inv, dict):
        return _draf_tidak_lengkap(inv_id, inv, galat_baca, masalah, items, hit, b, out)

    out["ref"] = inv.get("ref")
    out["lengkap"] = True
    out["status_dolibarr"] = str(inv.get("statut", inv.get("status")))
    dol = {"dpp": desimal(inv.get("total_ht")), "ppn": desimal(inv.get("total_tva")),
           "total": desimal(inv.get("total_ttc"))}
    out["dolibarr"] = dol
    beda = {k: dol[k] - hit[k] for k in ("dpp", "ppn", "total") if dol[k] != hit[k]}
    out["beda"] = beda
    b += ["", "TERSIMPAN SEBAGAI DRAF: {} (ID {}), status Dolibarr: {}".format(
        inv.get("ref"), inv_id, "draf" if out["status_dolibarr"] == "0" else out["status_dolibarr"])]
    b += ["Angka di Dolibarr: DPP {} | PPN {} | total {}".format(
        format_rp(dol["dpp"]), format_rp(dol["ppn"]), format_rp(dol["total"]))]
    if not beda:
        b.append("COCOK dengan hitungan Komunitech.")
    else:
        b.append("BEDA dengan hitungan Komunitech: " + "; ".join(
            "{} {}{}".format(k.upper(), "+" if v > 0 else "", format_rp(v)) for k, v in beda.items()))
        if "dpp" in beda:
            b.append("Selisih DPP: Dolibarr menyimpan total baris dengan sen (2 desimal), standar Komunitech "
                     "membulatkan total baris ke rupiah terdekat.")
        b.append("Sebab umum selisih PPN: Dolibarr menghitung PPN per baris lalu membulatkan ke terdekat (2 desimal, atau "
                 "sesuai pengaturan 'Maks. desimal untuk harga total'), sedangkan standar Komunitech menghitung "
                 "PPN dari total DPP lalu membulatkan ke bawah sekali. Selisih kecil (Rp 0-beberapa rupiah) wajar. "
                 "Draf TIDAK diubah otomatis; pemilik memutuskan. Nilai PPN resmi mengikuti faktur di Coretax.")
    b.append("Langkah berikut dilakukan MANUSIA di Dolibarr: periksa draf > Validasi > kirim/cetak.")
    out["teks"] = "\n".join(b)
    return out


def kode_perintah(socid, items, jenis_ppn, tgl, tempo, catatan):
    """Sidik 10 heksa dari isi perintah (pelanggan, tanggal, PPN, item). Disimpan di catatan privat draf agar
    pengulangan perintah yang SAMA setelah koneksi putus mengenali draf sebagian miliknya (C1 v1.0.3)."""
    isi = [int(socid), jenis_ppn, tgl.isoformat(), tempo.isoformat(), (catatan or "").strip(),
           [[it["deskripsi"], str(it["qty"]), str(it["harga"]), str(it["diskon"]), it["fk_product"], it["jenis"]]
            for it in items]]
    return hashlib.sha256(json.dumps(isi, ensure_ascii=False).encode("utf-8")).hexdigest()[:10]


def draf_tertinggal(draf, kode):
    """Draf pelanggan yang tampaknya sisa percobaan terputus: KOSONG (DPP 0; termasuk sisa versi lama tanpa kode
    perintah) atau berkode perintah sama (bisa sebagian). Yang jumlahnya sudah sama ditangani draf_kembar."""
    hasil = []
    for d in draf:
        th = desimal(d.get("total_ht"), None)
        if th == 0:
            hasil.append((d, "kosong"))
        elif "Kode perintah: " + kode in str(d.get("note_private") or ""):
            hasil.append((d, "sebagian"))
    return hasil


def _kepala_tidak_pasti(api, pel, kode, galat, b, out):
    """POST invoices terputus/timeout: draf mungkin sudah terbuat (kosong). Baca ulang, laporkan jujur, kode 8."""
    b[0] = "DRAF INVOICE BELUM PASTI TERBUAT"
    b += ["", "PERHATIAN: " + galat.pesan]
    try:
        draf = api.daftar_semua("invoices", {"status": "draft", "thirdparty_ids": pel["id"],
                                             "properties": "id,ref,total_ht,date,note_private"})
        temu = [d for d in draf if "Kode perintah: " + kode in str(d.get("note_private") or "")]
        dicek = True
    except Gagal:
        temu, dicek = [], False
    if temu:
        b.append("Dicek ulang: draf {} SUDAH TERBUAT di Dolibarr, tetapi masih KOSONG (belum ada barang)."
                 .format(", ".join("{} (ID {})".format(d.get("ref"), d.get("id")) for d in temu)))
    elif dicek:
        b.append("Dicek ulang: belum ada draf baru untuk pelanggan ini di Dolibarr. Bisa jadi Dolibarr masih "
                 "memprosesnya, jadi tunggu 1-2 menit lalu periksa lagi.")
    else:
        b.append("Dolibarr juga belum bisa dihubungi untuk dicek ulang, jadi belum pasti draf sudah terbuat atau belum.")
    b += ["JANGAN mengulang perintah ini sebelum mengecek Dolibarr.",
          "Yang perlu dicek: buka Dolibarr di browser > menu Tagihan/Nota > invoice pelanggan berstatus Draf untuk "
          "{}. Jika ada draf KOSONG (Rp 0) bercatatan '{}', hapus draf itu, lalu jalankan ulang perintah ini. "
          "Selama draf kosong itu masih ada, pengulangan akan ditahan (tidak membuat draf kedua)."
          .format(pel["nama"], PENANDA_DRAF)]
    out["dibuat"] = bool(temu)
    out["lengkap"] = False
    out["draf_tertinggal"] = [dict(d, keadaan="kosong") for d in temu]
    out["galat"] = galat.pesan
    out["kode_keluar"] = KELUAR_TIDAK_PASTI
    out["teks"] = "\n".join(b)
    return out


def _draf_tidak_lengkap(inv_id, inv, galat_baca, masalah, items, hit, b, out):
    """Draf sudah ada tetapi ada baris gagal/tidak pasti, atau isinya tidak bisa dibaca ulang. Kode 8, tanpa
    penutup 'Validasi' dan tanpa penjelasan selisih sen (tidak berlaku untuk draf sebagian)."""
    n = len(items)
    ref = inv.get("ref") if isinstance(inv, dict) else None
    nama = "{} (ID {})".format(ref, inv_id) if ref else "ID {}".format(inv_id)
    b[0] = "DRAF INVOICE TIDAK LENGKAP" if masalah else "DRAF INVOICE TERSIMPAN, BELUM BISA DIPERIKSA"
    b += ["", "Draf {} sudah ada di Dolibarr (status draf, belum sah).".format(nama)]
    if masalah:
        if masalah["mungkin_masuk"]:
            b.append("Baris {} ({}): Dolibarr tidak menjawab. Baris ini MUNGKIN sudah masuk, mungkin juga belum."
                     .format(masalah["nomor"], masalah["deskripsi"]))
        else:
            b.append("Baris {} ({}) DITOLAK Dolibarr ({}); baris ini tidak masuk."
                     .format(masalah["nomor"], masalah["deskripsi"], masalah["pesan"]))
        if masalah["nomor"] < n:
            b.append("Baris {} belum dikirim.".format(masalah["nomor"] + 1) if masalah["nomor"] + 1 == n else
                     "Baris {} s.d. {} belum dikirim.".format(masalah["nomor"] + 1, n))
        out["gagal_baris"] = (masalah["nomor"], masalah["pesan"])
        out["baris_mungkin_masuk"] = masalah["mungkin_masuk"]
    else:
        b.append("Semua {} baris sudah diterima Dolibarr, tetapi isi draf tidak bisa dibaca ulang ({})."
                 .format(n, str(galat_baca).rstrip(".")))
    if isinstance(inv, dict):
        baris = inv.get("lines")
        jml = "{} baris, ".format(len(baris)) if isinstance(baris, list) else ""
        dpp = desimal(inv.get("total_ht"))
        b.append("Isi draf di Dolibarr sekarang: {}DPP {} (seharusnya {} baris, DPP sekitar {})."
                 .format(jml, format_rp(dpp), n, format_rp(hit["dpp"])))
        out["ref"] = ref
        out["dolibarr"] = {"dpp": dpp, "ppn": desimal(inv.get("total_tva")), "total": desimal(inv.get("total_ttc"))}
    if masalah:
        b.append("Yang perlu dicek di Dolibarr (menu Tagihan/Nota > draf {}): cocokkan barisnya dengan daftar di "
                 "atas. Tambahkan baris yang kurang (dan hapus baris yang dobel) secara manual, ATAU hapus draf ini "
                 "lalu jalankan ulang perintah yang sama.".format(nama))
    else:
        b.append("Yang perlu dicek di Dolibarr (menu Tagihan/Nota > draf {}): pastikan ada {} baris dan totalnya "
                 "sesuai hitungan Komunitech di atas. JANGAN mengulang perintah ini, karena draf sudah ada."
                 .format(nama, n))
    b += ["Selama draf ini masih ada, perintah yang sama akan ditahan (tidak membuat draf kedua).",
          "Draf ini jangan disahkan dulu sebelum isinya lengkap dan sudah dicek manusia."]
    out["lengkap"] = False
    out["kode_keluar"] = KELUAR_TIDAK_PASTI
    out["teks"] = "\n".join(b)
    return out


# ------------------------------------------------------------------ perintah: piutang
KELOMPOK_UMUR = [("belum jatuh tempo", None, 0), ("lewat 1-30 hari", 1, 30), ("lewat 31-60 hari", 31, 60),
                 ("lewat 61-90 hari", 61, 90), ("lewat > 90 hari", 91, None)]


def kelompok_umur(hari_lewat):
    for label, lo, hi in KELOMPOK_UMUR:
        if lo is None and hari_lewat <= 0:
            return label
        if lo is not None and hari_lewat >= lo and (hi is None or hari_lewat <= hi):
            return label
    return KELOMPOK_UMUR[-1][0]


def ambil_piutang(api, offset, hari_ini):
    data = api.daftar_semua("invoices", {"status": "unpaid", "sortfield": "t.date_lim_reglement",
                                         "sortorder": "ASC",
                                         "properties": "id,ref,socid,type,date,date_lim_reglement,total_ttc,"
                                                       "remaintopay,totalpaid,multicurrency_code"})
    baris, catatan = [], []
    for inv in data:
        if str(inv.get("type")) == "2":
            continue  # nota kredit/retur, bukan piutang
        sisa = desimal(inv.get("remaintopay"), None)
        if sisa is None:
            sisa = desimal(inv.get("total_ttc")) - desimal(inv.get("totalpaid"))
        if sisa <= 0:
            catatan.append("{} sudah terbayar penuh tetapi belum ditandai lunas di Dolibarr.".format(inv.get("ref")))
            continue
        tempo = tanggal_dari_ts(inv.get("date_lim_reglement"), offset) or tanggal_dari_ts(inv.get("date"), offset)
        lewat = (hari_ini - tempo).days if tempo else 0
        mc = inv.get("multicurrency_code")
        if mc and mc != "IDR":
            catatan.append("{} memakai mata uang {} (angka ditampilkan apa adanya).".format(inv.get("ref"), mc))
        baris.append({"id": int(inv["id"]), "ref": inv.get("ref"), "socid": int(inv.get("socid") or 0),
                      "tanggal": tanggal_dari_ts(inv.get("date"), offset), "jatuh_tempo": tempo,
                      "hari_lewat": lewat, "kelompok": kelompok_umur(lewat), "total": desimal(inv.get("total_ttc")),
                      "terbayar": desimal(inv.get("totalpaid")), "sisa": sisa})
    return baris, catatan


def nama_pelanggan(api, ids):
    ids = sorted({i for i in ids if i})
    nama = {}
    for mulai in range(0, len(ids), 50):
        potong = ids[mulai:mulai + 50]
        try:
            d = api.daftar_semua("thirdparties", {"sqlfilters": "(t.rowid:in:{})".format(
                ",".join(str(i) for i in potong)), "properties": "id,name"})
        except Gagal as e:
            if e.http == 403:
                return {}
            raise
        for t in d:
            nama[int(t["id"])] = t.get("name") or ""
    return nama


def cmd_piutang(api, args, offset):
    hari_ini = parse_tanggal(args.per_tanggal, offset)
    baris, catatan = ambil_piutang(api, offset, hari_ini)
    nama = nama_pelanggan(api, [x["socid"] for x in baris]) if baris else {}
    for x in baris:
        n = nama.get(x["socid"]) or "Pelanggan #{}".format(x["socid"])
        x["pelanggan"] = inisial(n) if args.samarkan else n
    baris.sort(key=lambda x: (-x["hari_lewat"], -x["sisa"]))
    ringkas = {label: {"jumlah": 0, "nilai": Decimal(0)} for label, _, _ in KELOMPOK_UMUR}
    for x in baris:
        ringkas[x["kelompok"]]["jumlah"] += 1
        ringkas[x["kelompok"]]["nilai"] += x["sisa"]
    total = sum((x["sisa"] for x in baris), Decimal(0))
    b = ["PIUTANG BELUM LUNAS per {}".format(hari_ini.isoformat())]
    if not baris:
        b.append("Tidak ada invoice tervalidasi yang belum lunas.")
    else:
        b.append("Total sisa tagihan: {} ({} invoice)".format(format_rp(total), len(baris)))
        b.append("")
        b.append("UMUR PIUTANG (dihitung dari tanggal jatuh tempo)")
        for label, _, _ in KELOMPOK_UMUR:
            r = ringkas[label]
            if r["jumlah"]:
                b.append("- {}: {} invoice, {}".format(label, r["jumlah"], format_rp(r["nilai"])))
        b.append("")
        b.append("RINCIAN (paling lama terlambat di atas)")
        for x in baris[:args.maks]:
            status = ("lewat {} hari".format(x["hari_lewat"]) if x["hari_lewat"] > 0 else
                      "jatuh tempo hari ini" if x["hari_lewat"] == 0 else
                      "jatuh tempo {} hari lagi".format(-x["hari_lewat"]))
            b.append("- {} | {} | sisa {}{} | tempo {} ({})".format(
                x["ref"], x["pelanggan"], format_rp(x["sisa"]),
                " (sudah dibayar {})".format(format_rp(x["terbayar"])) if x["terbayar"] > 0 else "",
                x["jatuh_tempo"].isoformat() if x["jatuh_tempo"] else "-", status))
        if len(baris) > args.maks:
            b.append("... dan {} invoice lainnya (pakai --maks).".format(len(baris) - args.maks))
    if catatan:
        b.append("")
        b.append("CATATAN")
        b += ["- " + c for c in catatan]
    return {"per_tanggal": hari_ini, "total": total, "jumlah": len(baris), "umur": ringkas,
            "invoice": baris, "catatan": catatan, "teks": "\n".join(b)}


# ------------------------------------------------------------------ perintah: stok
def pastikan_stok_aktif(api):
    """Pastikan modul Stok aktif & bisa dibaca. Tanpa ini Dolibarr tetap mengirim daftar produk tetapi TANPA
    jumlah stok, sehingga semua barang akan tampak 'habis' (alarm palsu).

    Diamati pada Dolibarr 24.0.1: modul Stok mati ATAU user tanpa hak stok -> GET /warehouses = 403 dan produk
    tanpa stock_reel. Pembeda yang andal: daftar API di explorer/swagger.json hanya memuat /warehouses bila
    modul Stok aktif (tidak bergantung hak user). Cadangan: setup/modules (khusus admin), lalu /users/info."""
    try:
        api.minta("GET", "warehouses", {"limit": 1}, daftar=True)
        return
    except Gagal as e:
        if e.kode != KELUAR_MODUL and e.http != 403:
            raise
        mati = True if e.kode == KELUAR_MODUL else None
    if mati is None:
        try:
            sw = api.minta("GET", "explorer/swagger.json")
            if isinstance(sw, dict) and isinstance(sw.get("paths"), dict) and len(sw["paths"]) > 5:
                mati = not any(k.startswith("/warehouses") for k in sw["paths"])
        except Gagal as e2:
            if e2.kode == KELUAR_KONEKSI:
                raise
    if mati is None:
        try:
            mods = api.minta("GET", "setup/modules")
            if isinstance(mods, list):
                mati = "stock" not in [str(m).lower() for m in mods]
        except Gagal as e2:
            if e2.kode == KELUAR_KONEKSI:
                raise
    if mati is None:
        try:
            u = api.minta("GET", "users/info", {"includepermissions": 1})
            if punya_hak((u or {}).get("rights") or {}, "stock", "lire", None):
                mati = True  # hak ada tetapi tetap ditolak -> modul yang mati
        except Gagal as e2:
            if e2.kode == KELUAR_KONEKSI:
                raise
    if mati:
        raise Gagal("Modul Stok belum aktif di Dolibarr, jadi jumlah stok tidak dicatat. Status habis/menipis "
                    "tidak dinilai.", KELUAR_MODUL,
                    saran="Jika ingin memantau stok: Pengaturan > Modul/Aplikasi > aktifkan 'Stok'.")
    if mati is False:
        raise Gagal("User API belum punya hak 'Baca gudang dan stok' (modul Stok aktif), jadi stok tidak dinilai.",
                    KELUAR_AKSES, http=403,
                    saran="Dolibarr > Pengguna & Grup > user API > Izin > Stok > Baca gudang dan stok. "
                          "Lihat docs/panduan-dolibarr.md bagian 6.")
    raise Gagal("Stok tidak bisa dibaca: modul Stok belum aktif, atau user API tidak punya hak 'Baca gudang dan "
                "stok' (Dolibarr tidak memberi tahu yang mana). Status habis/menipis tidak dinilai.",
                KELUAR_AKSES, http=403,
                saran="Periksa keduanya: Pengaturan > Modul/Aplikasi > Stok, dan Izin user API "
                      "(docs/panduan-dolibarr.md bagian 5-6).")


def ambil_produk(api, kata=None):
    pastikan_stok_aktif(api)
    params = {"mode": 1, "includestockdata": 1, "sortfield": "t.ref", "sortorder": "ASC",
              "properties": "id,ref,label,status,status_buy,type,stock_reel,seuil_stock_alerte,desiredstock,"
                            "price,stock_warehouse"}
    if kata:
        k = kata_aman(kata)
        if len(k) < 2:
            raise Gagal("Kata pencarian terlalu pendek (minimal 2 huruf/angka).", KELUAR_ARG)
        params["sqlfilters"] = "((t.ref:like:'%{0}%') or (t.label:like:'%{0}%') or (t.barcode:like:'%{0}%'))" \
            .format(k)
    data = api.daftar_semua("products", params)
    hasil = []
    tanpa_angka = 0
    for p in data:
        if str(p.get("type", "0")) != "0":
            continue
        if str(p.get("status", "1")) == "0" and str(p.get("status_buy", "1")) == "0":
            continue  # produk nonaktif (tidak dijual & tidak dibeli)
        if p.get("stock_reel") in (None, ""):
            tanpa_angka += 1
            continue
        stok = desimal(p.get("stock_reel"))
        batas = desimal(p.get("seuil_stock_alerte"), None)
        ingin = desimal(p.get("desiredstock"), None)
        if stok <= 0:
            status = "MINUS" if stok < 0 else "HABIS"
        elif batas is not None and batas > 0 and stok < batas:
            status = "MENIPIS"
        else:
            status = "aman"
        target = ingin if ingin is not None and ingin > 0 else batas
        saran = (target - stok) if status != "aman" and target is not None and target > 0 and stok < target \
            else Decimal(0)
        hasil.append({"id": int(p["id"]), "ref": p.get("ref"), "nama": p.get("label") or "",
                      "stok": stok, "batas_minimum": batas if batas and batas > 0 else None,
                      "stok_ideal": ingin if ingin and ingin > 0 else None, "status": status,
                      "saran_beli": saran,
                      "dijual": str(p.get("status", "1")) == "1"})
    if tanpa_angka and not hasil:
        raise Gagal("Dolibarr tidak mengirim jumlah stok untuk produk (modul Stok mati atau hak baca stok kurang). "
                    "Status habis/menipis tidak dinilai.", KELUAR_MODUL)
    return hasil


def cmd_stok(api, args):
    produk = ambil_produk(api, args.kata)
    urutan = {"MINUS": 0, "HABIS": 1, "MENIPIS": 2, "aman": 3}
    perlu = [p for p in produk if p["status"] != "aman"]
    tampil = perlu if args.menipis else produk
    tampil = sorted(tampil, key=lambda p: (urutan[p["status"]], p["ref"] or ""))
    tanpa_batas = [p for p in produk if p["batas_minimum"] is None and p["status"] == "aman"]
    b = ["STOK PRODUK{}".format(" (menipis/habis)" if args.menipis else "")
         + (" - cari '{}'".format(kata_aman(args.kata)) if args.kata else "")]
    if not produk:
        b.append("Belum ada produk barang di Dolibarr{}.".format(" yang cocok" if args.kata else ""))
    else:
        b.append("Minus {} | habis {} | menipis {} | dari {} produk barang".format(
            sum(p["status"] == "MINUS" for p in produk), sum(p["status"] == "HABIS" for p in produk),
            sum(p["status"] == "MENIPIS" for p in produk), len(produk)))
        if args.menipis and not perlu:
            b.append("Semua stok aman.")
        for p in tampil[:args.maks]:
            batas = " (min {})".format(format_angka(p["batas_minimum"])) if p["batas_minimum"] is not None else ""
            saran = " -> beli {}".format(format_angka(p["saran_beli"])) if p["saran_beli"] > 0 else ""
            b.append("- {} {}: stok {}{} {}{}".format(p["ref"], p["nama"], format_angka(p["stok"]), batas,
                                                     p["status"], saran))
        if len(tampil) > args.maks:
            b.append("... dan {} lainnya (pakai --maks).".format(len(tampil) - args.maks))
        if tanpa_batas:
            b.append("Catatan: {} produk belum punya batas stok minimum di Dolibarr, jadi tidak bisa dinilai "
                     "menipis.".format(len(tanpa_batas)))
    return {"produk": tampil, "jumlah_produk": len(produk), "perlu_perhatian": len(perlu),
            "tanpa_batas_minimum": len(tanpa_batas), "teks": "\n".join(b)}


# ------------------------------------------------------------------ perintah: laporan harian
def penjualan_tanggal(api, tgl, offset):
    """Invoice tervalidasi/lunas/ditutup ber-tanggal `tgl` (tanggal invoice, bukan tanggal bayar)."""
    f = "(t.datef:=:'{}')".format(tgl.isoformat())
    data = api.daftar_semua("invoices", {"sqlfilters": f, "properties": "id,ref,type,statut,status,total_ht,"
                                                                          "total_tva,total_ttc,remaintopay,paye,date"})
    r = {"nota": 0, "retur": 0, "dpp": Decimal(0), "ppn": Decimal(0), "total": Decimal(0),
         "belum_dibayar": Decimal(0), "draf": 0, "batal": 0}
    for inv in data:
        st = str(inv.get("statut", inv.get("status")))
        if st == "0":
            r["draf"] += 1
            continue
        if st == "3":
            r["batal"] += 1
            continue
        if str(inv.get("type")) == "2":
            r["retur"] += 1
        else:
            r["nota"] += 1
        r["dpp"] += desimal(inv.get("total_ht"))
        r["ppn"] += desimal(inv.get("total_tva"))
        r["total"] += desimal(inv.get("total_ttc"))
        if str(inv.get("type")) != "2" and st != "2" and str(inv.get("paye", "0")) != "1":
            r["belum_dibayar"] += max(desimal(inv.get("remaintopay")), Decimal(0))
    return r


def cmd_laporan_harian(api, args, offset):
    tgl = parse_tanggal(args.tanggal, offset)
    zona = NAMA_ZONA.get(offset, "")
    out = {"tanggal": tgl, "bagian": {}, "perhatian": []}
    b = ["LAPORAN HARIAN DOLIBARR", tanggal_panjang(tgl),
         "Dibuat {} {}".format(sekarang_lokal(offset).strftime("%Y-%m-%d %H:%M"), zona), ""]

    def bagian(nama, fungsi):
        try:
            return fungsi()
        except Gagal as e:
            if e.kode == KELUAR_KONEKSI:
                raise
            out["bagian"][nama] = {"galat": e.pesan}
            out.setdefault("kode_galat", []).append(e.kode)
            return None

    hari = bagian("penjualan", lambda: penjualan_tanggal(api, tgl, offset))
    b.append("PENJUALAN (invoice tervalidasi bertanggal ini)")
    if hari is None:
        b.append("Tidak bisa dibaca: {}".format(out["bagian"]["penjualan"]["galat"]))
    else:
        kem = bagian("kemarin", lambda: penjualan_tanggal(api, tgl - dt.timedelta(days=1), offset))
        out["bagian"]["penjualan"] = hari
        b.append("Total (termasuk PPN): {}".format(format_rp(hari["total"])))
        b.append("DPP {} | PPN {}".format(format_rp(hari["dpp"]), format_rp(hari["ppn"])))
        b.append("Invoice: {}{}".format(hari["nota"], " | retur/nota kredit: {}".format(hari["retur"])
                                         if hari["retur"] else ""))
        if hari["nota"]:
            b.append("Belum dibayar dari penjualan ini: {}".format(format_rp(hari["belum_dibayar"])))
        if kem is not None:
            p = persen_ubah(hari["total"], kem["total"])
            if p is None:
                b.append("vs kemarin: {} (persen tidak dihitung)".format(format_rp(kem["total"])))
            else:
                arah = "naik" if p > 0 else "turun" if p < 0 else "sama"
                b.append("vs kemarin: {} -> {} {}%".format(format_rp(kem["total"]), arah,
                                                          str(abs(p)).replace(".", ",")))
        if hari["draf"]:
            out["perhatian"].append("{} draf invoice bertanggal {} belum divalidasi (belum dihitung sebagai "
                                    "penjualan).".format(hari["draf"], "hari ini" if tgl == sekarang_lokal(offset).date()
                                                         else tgl.isoformat()))
    b.append("")

    pi = bagian("piutang", lambda: ambil_piutang(api, offset, tgl))
    b.append("PIUTANG" if tgl == sekarang_lokal(offset).date() else
             "PIUTANG (status bayar saat ini; umur dihitung per {})".format(tgl.isoformat()))
    if pi is None:
        b.append("Tidak bisa dibaca: {}".format(out["bagian"]["piutang"]["galat"]))
    else:
        baris, _ = pi
        total = sum((x["sisa"] for x in baris), Decimal(0))
        lewat = [x for x in baris if x["hari_lewat"] > 0]
        nilai_lewat = sum((x["sisa"] for x in lewat), Decimal(0))
        out["bagian"]["piutang"] = {"total": total, "jumlah": len(baris), "terlambat": len(lewat),
                                    "nilai_terlambat": nilai_lewat}
        b.append("Belum lunas: {} invoice, {}".format(len(baris), format_rp(total)))
        b.append("Terlambat: {} invoice, {}".format(len(lewat), format_rp(nilai_lewat)))
        for x in sorted(lewat, key=lambda x: -x["hari_lewat"])[:3]:
            b.append("- {} sisa {}, lewat {} hari".format(x["ref"], format_rp(x["sisa"]), x["hari_lewat"]))
        if lewat:
            out["perhatian"].append("Ada {} invoice terlambat. Rincian & nama pelanggan: perintah `piutang`."
                                    .format(len(lewat)))
    b.append("")

    st = bagian("stok", lambda: ambil_produk(api))
    b.append("STOK")
    if st is None:
        b.append("Tidak bisa dibaca: {}".format(out["bagian"]["stok"]["galat"]))
    else:
        perlu = [p for p in st if p["status"] != "aman"]
        out["bagian"]["stok"] = {"perlu_perhatian": len(perlu), "jumlah_produk": len(st)}
        if not st:
            b.append("Belum ada produk barang.")
        elif not perlu:
            b.append("Semua stok aman ({} produk).".format(len(st)))
        else:
            b.append("Perlu perhatian: {} dari {} produk".format(len(perlu), len(st)))
            urut = {"MINUS": 0, "HABIS": 1, "MENIPIS": 2}
            for p in sorted(perlu, key=lambda p: (urut[p["status"]], p["ref"] or ""))[:5]:
                b.append("- {} {}: stok {} {}".format(p["ref"], p["nama"], format_angka(p["stok"]), p["status"]))
            if len(perlu) > 5:
                b.append("... dan {} lainnya (perintah `stok --menipis`).".format(len(perlu) - 5))
    gagal = [k for k in ("penjualan", "piutang", "stok") if "galat" in (out["bagian"].get(k) or {})]
    if len(gagal) == 3:
        raise Gagal("Laporan tidak bisa dibuat: semua bagian gagal dibaca ({}).".format(
            out["bagian"]["penjualan"]["galat"]), out["kode_galat"][0],
            saran="Jalankan `cek` untuk melihat modul & hak akses yang kurang.")
    if out["perhatian"]:
        b += ["", "PERLU PERHATIAN"] + ["{}. {}".format(i, c) for i, c in enumerate(out["perhatian"], 1)]
    b += ["", "Sumber: Dolibarr {} (hanya dibaca).".format(api.url)]
    out["teks"] = "\n".join(b)
    return out


# ------------------------------------------------------------------ CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen tidak valid ({}).\nLihat bantuan: python3 dolibarr.py --help\n"
                         .format(message))
        sys.exit(KELUAR_ARG)


# Opsi umum boleh ditulis di depan ATAU di belakang subperintah. Tiap tingkat parser menyimpan ke dest
# sendiri (default SUPPRESS) lalu digabung di gabung_opsi_umum(); nilai berbeda di dua posisi = ditolak.
OPSI_UMUM = ("url", "kunci_file", "izinkan_url_luar", "tz", "json")
BAWAAN_UMUM = {"url": None, "kunci_file": None, "izinkan_url_luar": False, "tz": "WIB", "json": False}
TINGKAT = ("_t0_", "_t1_", "_t2_")


def buat_umum(awalan):
    u = argparse.ArgumentParser(add_help=False)
    d = argparse.SUPPRESS
    u.add_argument("--url", dest=awalan + "url", default=d,
                   help="Alamat Dolibarr (default ENV DOLIBARR_URL atau {})".format(URL_DEFAULT))
    u.add_argument("--kunci-file", dest=awalan + "kunci_file", default=d,
                   help="File kunci API; bila diisi, menang atas ENV DOLIBARR_API_KEY "
                        "(default ~/.komunitech/dolibarr-kunci.txt)")
    u.add_argument("--izinkan-url-luar", dest=awalan + "izinkan_url_luar", action="store_const", const=True,
                   default=d, help="Izinkan Dolibarr di komputer lain (wajib https untuk internet)")
    u.add_argument("--tz", dest=awalan + "tz", default=d, help="WIB (default), WITA, atau WIT")
    u.add_argument("--json", dest=awalan + "json", action="store_const", const=True, default=d,
                   help="Keluaran JSON untuk agent")
    return u


def gabung_opsi_umum(args):
    for nama in OPSI_UMUM:
        nilai = [getattr(args, t + nama) for t in TINGKAT if hasattr(args, t + nama)]
        beda = sorted({str(v) for v in nilai})
        if len(beda) > 1:
            raise Gagal("Opsi --{} ditulis lebih dari sekali dengan nilai berbeda ({}). Tulis satu kali saja."
                        .format(nama.replace("_", "-"), " / ".join(beda)), KELUAR_ARG)
        setattr(args, nama, nilai[0] if nilai else BAWAAN_UMUM[nama])
    return args


def buat_parser():
    umum = buat_umum(TINGKAT[0])
    umum1 = buat_umum(TINGKAT[1])
    umum2 = buat_umum(TINGKAT[2])

    ap = ParserID(prog="dolibarr.py", description="Asisten Dolibarr lokal (Komunitech). Default hanya baca.",
                  parents=[umum])
    sub = ap.add_subparsers(dest="perintah", parser_class=ParserID)
    sub.add_parser("cek", parents=[umum1], help="Cek koneksi, versi, modul, hak akses")
    sk = sub.add_parser("simpan-kunci", parents=[umum1], help="Simpan kunci API ke file lokal (izin 600)")
    sk.add_argument("--ya", action="store_true", help="Izinkan menimpa file kunci yang sudah ada")

    pel = sub.add_parser("pelanggan", parents=[umum1], help="Cari/tambah pelanggan")
    ps = pel.add_subparsers(dest="aksi", parser_class=ParserID)
    c = ps.add_parser("cari", parents=[umum2])
    c.add_argument("kata")
    t = ps.add_parser("tambah", parents=[umum2])
    t.add_argument("--nama", required=True)
    t.add_argument("--telepon")
    t.add_argument("--email")
    t.add_argument("--alamat")
    t.add_argument("--kota")
    t.add_argument("--catatan")
    t.add_argument("--ya", action="store_true", help="Benar-benar simpan (tanpa ini hanya pratinjau)")
    t.add_argument("--tetap-buat", action="store_true", help="Tetap buat walau ada nama mirip")

    inv = sub.add_parser("invoice", parents=[umum1], help="Buat draf invoice")
    isub = inv.add_subparsers(dest="aksi", parser_class=ParserID)
    ib = isub.add_parser("buat", parents=[umum2])
    ib.add_argument("--pelanggan", required=True, help="ID pelanggan (dari `pelanggan cari`)")
    ib.add_argument("--item", action="append", help="\"nama|jumlah|harga[|diskon%%]\" atau \"@KODE|jumlah[|harga]\"")
    ib.add_argument("--ppn", choices=sorted(PPN), default="umum",
                    help="umum = 12%% x DPP 11/12 (default), mewah = 12%% penuh, tanpa = tanpa PPN")
    ib.add_argument("--jasa", action="store_true", help="Baris tanpa kode produk dicatat sebagai jasa")
    ib.add_argument("--tanggal", default="hari-ini")
    ib.add_argument("--jatuh-tempo", type=int, default=14, help="Hari sampai jatuh tempo (default 14)")
    ib.add_argument("--catatan", help="Catatan publik di invoice")
    ib.add_argument("--ya", action="store_true", help="Benar-benar buat draf (tanpa ini hanya pratinjau)")
    ib.add_argument("--tetap-buat", action="store_true", help="Tetap buat walau ada draf kembar")

    pi = sub.add_parser("piutang", parents=[umum1], help="Invoice belum lunas + umur piutang")
    pi.add_argument("--per-tanggal", default="hari-ini")
    pi.add_argument("--samarkan", action="store_true", help="Nama pelanggan jadi inisial")
    pi.add_argument("--maks", type=int, default=30)

    s = sub.add_parser("stok", parents=[umum1], help="Cek stok produk")
    s.add_argument("kata", nargs="?")
    s.add_argument("--menipis", action="store_true", help="Hanya yang menipis/habis/minus")
    s.add_argument("--maks", type=int, default=50)

    lh = sub.add_parser("laporan-harian", parents=[umum1], help="Ringkasan harian untuk pemilik")
    lh.add_argument("--tanggal", default="hari-ini")
    return ap


def main(argv=None):
    ap = buat_parser()
    args = ap.parse_args(argv)
    args.json = any(getattr(args, t + "json", False) for t in TINGKAT)
    if not args.perintah or (args.perintah in ("pelanggan", "invoice") and not getattr(args, "aksi", None)):
        ap.print_help()
        return KELUAR_ARG
    try:
        gabung_opsi_umum(args)
        if args.perintah == "simpan-kunci":
            hasil = cmd_simpan_kunci(args)
        else:
            offset = zona_offset(args.tz)
            if args.perintah == "invoice" and not 0 <= args.jatuh_tempo <= BATAS_TEMPO:
                raise Gagal("--jatuh-tempo harus 0 sampai {} hari.".format(BATAS_TEMPO), KELUAR_ARG)
            luar = args.izinkan_url_luar or os.environ.get("DOLIBARR_IZINKAN_URL_LUAR") == "1"
            url, lokal, catatan_url = cek_url(args.url or os.environ.get("DOLIBARR_URL") or URL_DEFAULT, luar)
            kunci, sumber, peringatan_kunci = baca_kunci(args.kunci_file)
            if peringatan_kunci:
                cetak(peringatan_kunci, file=sys.stderr)
            api = Dolibarr(url, kunci, lokal)
            if args.perintah == "cek":
                hasil = cmd_cek(api, args, catatan_url, sumber)
            elif args.perintah == "pelanggan":
                hasil = cmd_pelanggan_cari(api, args) if args.aksi == "cari" else cmd_pelanggan_tambah(api, args)
            elif args.perintah == "invoice":
                hasil = cmd_invoice_buat(api, args, offset)
            elif args.perintah == "piutang":
                hasil = cmd_piutang(api, args, offset)
            elif args.perintah == "stok":
                hasil = cmd_stok(api, args)
            else:
                hasil = cmd_laporan_harian(api, args, offset)
            if catatan_url and args.perintah != "cek":
                hasil["teks"] = "\n".join(catatan_url) + "\n\n" + hasil["teks"]
            if peringatan_kunci:
                hasil["peringatan_kunci"] = peringatan_kunci
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
    except Exception as e:  # jangan pernah traceback (bisa memuat kunci); pesan tetap disamarkan
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
