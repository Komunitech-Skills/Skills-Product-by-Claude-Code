#!/usr/bin/env python3
"""kanboard-papan-kerja (Komunitech) - asisten papan kerja Kanboard milik pengguna sendiri.

Memanggil JSON-RPC API resmi Kanboard (POST <alamat>/jsonrpc.php, HTTP Basic Auth) di server
milik pengguna (biasanya http://127.0.0.1:8080). Python standar saja (urllib), tanpa paket tambahan.
Komunitech tidak berafiliasi dengan proyek Kanboard.

Perintah:
  simpan-kunci   simpan nama pengguna + token API ke file lokal (izin 600; token dibaca tersembunyi)
  status-kunci   cek SAJA apakah kunci sudah tersimpan (YA/TIDAK + nama pengguna); token tidak
                 pernah ditampilkan dan Kanboard tidak dihubungi
  atur           simpan alamat Kanboard default & (opsional) daftarkan host server sendiri
  cek            cek koneksi, versi, mode akses, zona waktu
  daftar-papan   daftar papan (project) yang bisa dilihat
  kolom          kolom sebuah papan + jumlah kartu terbuka + batas WIP
  hari-ini       kartu jatuh tempo hari ini (belum ditutup)
  terlambat      kartu lewat jatuh tempo (belum ditutup)
  macet          kartu yang tidak berpindah kolom >= N hari (default 3), di luar kolom terakhir
  laporan        ringkasan siap kirim Telegram: terlambat + hari ini + macet
  template       daftar template papan per jenis usaha (tanpa koneksi)
  buat-papan     buat papan dari template (pratinjau; simpan dengan --ya)
  tambah-kartu   buat kartu baru (pratinjau; simpan dengan --ya)
  pindah-kartu   pindahkan kartu ke kolom lain (pratinjau; simpan dengan --ya)

Keamanan: TIDAK ADA perintah hapus/tutup/ubah pengguna. Metode JSON-RPC yang boleh dipanggil dikunci
lewat daftar izin (METODE_BACA / METODE_TULIS). Redirect ditolak. Host selain komputer ini harus
didaftarkan pemilik (`atur --izinkan-host`); internet wajib https.

Kode keluar: 0 berhasil | 2 input/alamat salah | 3 file kunci/konfigurasi | 4 Kanboard tidak bisa
dihubungi / data tidak ada | 5 login salah atau hak kurang | 7 tidak dibuat: ganda/ambigu |
8 SAAT MENULIS koneksi putus/timeout/galat server - data MUNGKIN sudah tersimpan, cek dulu, JANGAN ulangi.
Windows: pakai `python` atau `py` sebagai ganti `python3`.
"""
import argparse
import base64
import datetime as dt
import getpass
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

VERSI_SKRIP = "1.0.7"
KANBOARD_TERUJI = ("v1.2.54", "1.2.54")
URL_DEFAULT = "http://127.0.0.1:8080"
FOLDER_KONF = os.path.join(os.path.expanduser("~"), ".komunitech")
KUNCI_DEFAULT = os.path.join(FOLDER_KONF, "kanboard-kunci.json")
KONFIG_DEFAULT = os.path.join(FOLDER_KONF, "kanboard-konfig.json")
MAKS_JAWABAN = 20 * 1024 * 1024
MAKS_TELEGRAM = 3500
MAKS_BARIS_BAGIAN = 10

K_INPUT, K_FILE, K_KONEKSI, K_AUTH, K_GANDA, K_TAKPASTI = 2, 3, 4, 5, 7, 8

# Daftar izin metode JSON-RPC. Semua panggilan lewat Kanboard.rpc() diperiksa di sini.
METODE_BACA = {
    "getVersion", "getTimezone", "getMe", "getMyProjects", "getAllProjects", "getProjectById",
    "getColumns", "getAllTasks", "getTask", "getAssignableUsers", "getActiveSwimlanes",
}
METODE_TULIS = {"createProject", "createMyPrivateProject", "updateColumn", "addColumn", "createTask",
                "moveTaskPosition"}

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
BULAN_KATA = {
    "jan": 1, "januari": 1, "feb": 2, "februari": 2, "peb": 2, "mar": 3, "maret": 3, "apr": 4,
    "april": 4, "mei": 5, "jun": 6, "juni": 6, "jul": 7, "juli": 7, "agu": 8, "agt": 8, "ags": 8,
    "agustus": 8, "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "nov": 11,
    "nop": 11, "november": 11, "des": 12, "desember": 12,
}
HARI_KATA = {"senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "sabtu": 5, "minggu": 6}
TZ_OFFSET = {"WIB": 7, "WITA": 8, "WIT": 9}
# Cadangan bila modul zoneinfo/tzdata tidak ada (mis. Windows tanpa paket tzdata).
TZ_SERVER_CADANGAN = {"UTC": 0, "Etc/UTC": 0, "GMT": 0, "Etc/GMT": 0, "Asia/Jakarta": 7,
                      "Asia/Pontianak": 7, "Asia/Makassar": 8, "Asia/Jayapura": 9}

# Template papan per jenis usaha: (judul kolom, batas WIP 0=tanpa batas, keterangan)
TEMPLATE = {
    "produksi": {
        "nama": "Alur Produksi (konveksi, makanan, kerajinan, percetakan)",
        "kolom": [
            ("Order Masuk", 0, "Pesanan baru yang sudah dikonfirmasi pelanggan"),
            ("Siapkan Bahan", 0, "Belanja/cek stok bahan baku"),
            ("Produksi", 5, "Sedang dikerjakan; batasi agar tidak menumpuk"),
            ("Cek Kualitas", 0, "QC sebelum dikemas"),
            ("Siap Kirim", 0, "Sudah dikemas, menunggu kurir/diambil"),
            ("Selesai", 0, "Sudah diterima pelanggan"),
        ],
    },
    "order-pengiriman": {
        "nama": "Order & Pengiriman (toko online, distributor)",
        "kolom": [
            ("Pesanan Baru", 0, "Masuk dari WA/marketplace, belum dicek"),
            ("Menunggu Bayar", 0, "Invoice terkirim, pembayaran belum masuk"),
            ("Dikemas", 0, "Sudah bayar, sedang disiapkan"),
            ("Dikirim", 0, "Sudah diserahkan ke kurir; isi nomor resi di deskripsi"),
            ("Retur/Komplain", 0, "Perlu ditindaklanjuti"),
            ("Diterima", 0, "Sampai di pelanggan (kolom terakhir = beres)"),
        ],
    },
    "konten": {
        "nama": "Produksi Konten (media sosial, iklan)",
        "kolom": [
            ("Ide", 0, "Bank ide konten"),
            ("Naskah", 0, "Caption/skrip sedang ditulis"),
            ("Desain/Syuting", 3, "Produksi visual/video"),
            ("Review", 0, "Dicek pemilik/klien"),
            ("Terjadwal", 0, "Sudah dijadwalkan tayang"),
            ("Tayang", 0, "Sudah dipublikasikan"),
        ],
    },
    "proyek-jasa": {
        "nama": "Proyek Jasa (konsultan, agensi, kontraktor, freelancer)",
        "kolom": [
            ("Prospek/Brief", 0, "Calon klien & kebutuhan awal"),
            ("Penawaran", 0, "Penawaran harga terkirim"),
            ("Dikerjakan", 4, "Proyek berjalan"),
            ("Revisi Klien", 0, "Menunggu/menerapkan revisi"),
            ("Tagihan", 0, "Invoice terkirim, belum lunas"),
            ("Selesai", 0, "Lunas & ditutup"),
        ],
    },
}


class Gagal(Exception):
    def __init__(self, pesan, kode=K_INPUT, saran=None):
        super().__init__(pesan)
        self.kode = kode
        self.saran = saran


_RAHASIA = []


def samarkan(teks):
    teks = str(teks)
    for r in _RAHASIA:
        if r and len(r) >= 8:
            teks = teks.replace(r, "****")
    return teks


# ============================================================ tanggal & zona waktu


def zona_lokal(tz_nama):
    return dt.timezone(dt.timedelta(hours=TZ_OFFSET.get(tz_nama, 7)))


def sekarang(tz_nama):
    return dt.datetime.now(zona_lokal(tz_nama))


def zona_server(nama):
    """Nama zona waktu Kanboard (mis. 'UTC', 'Asia/Jakarta') -> tzinfo."""
    nama = (nama or "UTC").strip()
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(nama)
    except Exception:  # modul/tzdata tidak ada atau nama tidak dikenal
        pass
    if nama in TZ_SERVER_CADANGAN:
        return dt.timezone(dt.timedelta(hours=TZ_SERVER_CADANGAN[nama]))
    raise Gagal(
        f"Zona waktu Kanboard '{nama}' tidak bisa dihitung di komputer ini.", K_INPUT,
        saran="Di Kanboard: Pengaturan > Pengaturan Aplikasi > Zona waktu, pilih Asia/Jakarta "
              "(atau UTC), lalu ulangi.")


def tgl_pendek(d):
    return f"{d.day} {BULAN[d.month - 1][:3]} {d.year}"


def tgl_panjang(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def epoch_ke_lokal(nilai, tz_nama):
    try:
        n = int(nilai or 0)
    except (TypeError, ValueError):
        return None
    if n <= 0:
        return None
    return dt.datetime.fromtimestamp(n, zona_lokal(tz_nama))


_KET = r"(?:\s*(pagi|siang|sore|petang|malam))?"
_JAM_RE = re.compile(
    r"\b(?:jam|pukul)\s+(\d{1,2})(?:[:.](\d{2}))?(?![\d:./-])" + _KET
    + r"|(?<![\d/.:-])(\d{1,2})[:.](\d{2})(?![\d/.:-])" + _KET)


def baca_jam(jam, menit, ket, teks_jam):
    """Jam tulisan orang Indonesia -> (jam24, menit). Jam 1-6 tanpa keterangan = ambigu -> Gagal (tanya)."""
    if not (0 <= jam <= 23 and 0 <= menit <= 59):
        raise Gagal(f"Jam tidak valid di tenggat: {teks_jam!r}", K_INPUT)
    if jam >= 13 or teks_jam.startswith("0") and not ket:  # 24 jam eksplisit ('14:00', '03:00')
        return jam, menit
    if ket == "pagi":
        return (0 if jam == 12 else jam), menit
    if ket == "siang":
        return (jam + 12 if 1 <= jam <= 6 else jam), menit
    if ket in ("sore", "petang"):
        return (jam + 12 if 1 <= jam <= 11 else jam), menit
    if ket == "malam":
        return (0 if jam == 12 else jam + 12 if 5 <= jam <= 11 else jam), menit
    if 1 <= jam <= 6:
        raise Gagal(f"Jam {teks_jam!r} tidak jelas: {jam:02d}:{menit:02d} dini hari atau {jam + 12}:{menit:02d}?",
                    K_INPUT, saran=f"Tanyakan ke pengguna, lalu tulis dengan keterangan: 'jam {jam} sore' "
                                   f"({jam + 12}:{menit:02d}) atau format 24 jam '{jam + 12}:{menit:02d}' / "
                                   f"'{jam:02d}:{menit:02d}' (dini hari).")
    return jam, menit


def cari_tanggal(teks, acuan, info=None):
    """Satu frasa tanggal Indonesia -> date atau None. info (dict) diisi bila tahun tidak disebut."""
    t = teks.lower().strip().replace("jum'at", "jumat")
    if info is None:
        info = {}
    if re.search(r"\bbesok lusa\b|\bkapan[- ]?kapan\b", t):  # ungkapan 'suatu saat', bukan tanggal
        return None
    if re.search(r"\bhari ini\b", t):
        return acuan
    if re.search(r"\bkemarin\b", t):
        return acuan - dt.timedelta(days=1)
    if re.search(r"\bbesok\b", t):
        return acuan + dt.timedelta(days=1)
    if re.search(r"\blusa\b", t):
        return acuan + dt.timedelta(days=2)
    m = re.search(r"\b(\d{1,3})\s+hari\s+lagi\b", t)
    if m:
        return acuan + dt.timedelta(days=int(m.group(1)))
    if re.search(r"\bakhir bulan( ini)?\b", t):
        besok_bulan = (acuan.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        return besok_bulan - dt.timedelta(days=1)
    if re.search(r"\bawal bulan depan\b", t):
        return (acuan.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    if re.search(r"\b(minggu|pekan) depan\b", t):
        return acuan + dt.timedelta(days=7)
    m = re.search(r"\b(senin|selasa|rabu|kamis|jumat|sabtu|minggu)(\s+depan)?\b", t)
    if m:
        if m.group(2):  # 'Jumat depan' = hari itu di minggu kalender berikutnya (Senin-Minggu)
            return acuan + dt.timedelta(days=7 - acuan.weekday() + HARI_KATA[m.group(1)])
        return acuan + dt.timedelta(days=(HARI_KATA[m.group(1)] - acuan.weekday()) % 7)
    m = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", t)
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = re.search(r"\b(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?\b", t)
    if m:
        d, mo = int(m.group(1)), int(m.group(2))
        y = int(m.group(3)) if m.group(3) else acuan.year
        y = y + 2000 if y < 100 else y
        return _tanggal_aman(y, mo, d, acuan, bool(m.group(3)), info)
    m = re.search(r"\b(\d{1,2})\s+([a-z]+)\.?(?:\s+(\d{4}))?\b", t)
    if m and m.group(2) in BULAN_KATA:
        y = int(m.group(3)) if m.group(3) else acuan.year
        return _tanggal_aman(y, BULAN_KATA[m.group(2)], int(m.group(1)), acuan, bool(m.group(3)), info)
    return None


def _tanggal_aman(y, mo, d, acuan, tahun_disebut, info=None):
    """Tanggal tanpa tahun yang sudah lewat TIDAK diam-diam dipindah ke tahun depan, kecuali sudah lewat > 60 hari
    (dianggap maksud tahun depan). Kedua kasus dicatat di info agar diberi PERINGATAN."""
    try:
        hasil = dt.date(y, mo, d)
    except ValueError:
        return None
    if not tahun_disebut:
        if info is not None:
            info["tanpa_tahun"] = True
        if hasil < acuan - dt.timedelta(days=60):
            try:
                hasil = dt.date(y + 1, mo, d)
                if info is not None:
                    info["digeser"] = True
            except ValueError:
                pass
    return hasil


def parse_tenggat_lengkap(teks, acuan):
    """'besok jam 3 sore' -> (date, jam, menit, [peringatan]). Default jam 17:00."""
    jam, menit, sisa, peringatan = 17, 0, teks, []
    m = _JAM_RE.search(teks)
    if m:
        if m.group(1):
            j, mn, ket, mentah = int(m.group(1)), int(m.group(2) or 0), m.group(3), m.group(1)
        else:
            j, mn, ket, mentah = int(m.group(4)), int(m.group(5)), m.group(6), m.group(4)
        jam, menit = baca_jam(j, mn, ket, mentah)
        sisa = (teks[:m.start()] + teks[m.end():]).strip()
    info = {}
    tanggal = cari_tanggal(sisa, acuan, info)
    if tanggal is None:
        raise Gagal(
            f"Tenggat tidak dikenali: {teks!r}.", K_INPUT,
            saran="Format yang didukung: 'hari ini', 'besok', 'lusa', 'N hari lagi', nama hari "
                  "('Jumat', 'Jumat depan'), 'minggu depan', 'akhir bulan', 'awal bulan depan', '25/10' (tanggal/bulan), '25/10/2026', "
                  "'25 Oktober 2026', '2026-10-25'; boleh ditambah 'jam 14:00', '10.00' atau 'jam 3 sore'.")
    if info.get("digeser"):
        peringatan.append(f"PERINGATAN: tanggal tanpa tahun sudah lewat jauh, dibaca sebagai tahun {tanggal.year}. "
                          f"Benar tahun {tanggal.year}? (sebutkan tahunnya bila bukan)")
    elif info.get("tanpa_tahun") and tanggal < acuan:
        peringatan.append(f"PERINGATAN: tanggal {tanggal.day:02d}/{tanggal.month:02d} tahun {tanggal.year} SUDAH LEWAT "
                          f"(hari ini {acuan.day:02d}/{acuan.month:02d}/{acuan.year}). Maksudnya tahun "
                          f"{tanggal.year + 1}? Minta pengguna menyebut tahunnya (mis. {tanggal.day:02d}/"
                          f"{tanggal.month:02d}/{tanggal.year + 1}).")
    return tanggal, jam, menit, peringatan


def parse_tenggat(teks, acuan):
    """Versi ringkas: (date, jam, menit). Peringatan tersedia lewat parse_tenggat_lengkap."""
    return parse_tenggat_lengkap(teks, acuan)[:3]


def tenggat_ke_server(tanggal, jam, menit, tz_lokal, tz_server):
    """Waktu lokal pengguna -> teks 'Y-m-d H:i' di zona waktu server Kanboard (format resmi Kanboard)."""
    lokal = dt.datetime(tanggal.year, tanggal.month, tanggal.day, jam, menit, tzinfo=zona_lokal(tz_lokal))
    return lokal.astimezone(tz_server).strftime("%Y-%m-%d %H:%M"), int(lokal.timestamp())


# ============================================================ kunci & konfigurasi


def _tulis_600(path, isi):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(isi)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def cek_izin_file(path):
    if os.name == "nt":
        return
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        return
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        sys.stderr.write(f"PERINGATAN: file {path} bisa dibaca pengguna lain. Jalankan: chmod 600 {path}\n")


def cmd_simpan_kunci(args):
    path = os.path.abspath(os.path.expanduser(args.kunci_file or KUNCI_DEFAULT))
    if os.path.exists(path) and not args.ya:
        raise Gagal(f"File kunci sudah ada: {path}", K_FILE,
                    saran="Untuk mengganti, ulangi dengan --ya. Untuk token kedua (mis. baca-tulis), "
                          "pakai --kunci-file <path lain>.")
    sys.stderr.write(f"Kunci akan disimpan di: {path}\n")
    pengguna = input("Nama pengguna Kanboard (username; 'jsonrpc' untuk token aplikasi): ").strip()
    if not pengguna or re.search(r"[\s:]", pengguna):
        raise Gagal("Nama pengguna kosong atau berisi spasi/titik dua.", K_INPUT)
    token = getpass.getpass("Tempel token API Kanboard (tidak terlihat), lalu Enter: ").strip()
    if not token:
        raise Gagal("Token kosong, tidak disimpan.", K_INPUT)
    if re.search(r"\s", token):
        raise Gagal("Token berisi spasi/baris baru - kemungkinan tersalin rusak. Salin ulang.", K_INPUT)
    _tulis_600(path, json.dumps({"pengguna": pengguna, "token": token}) + "\n")
    print(f"Kunci tersimpan di {path} (izin 600). Token tidak ditampilkan.")
    return 0


def _kunci_dan_sumber(args):
    """-> (pengguna, token, sumber). Urutan: --kunci-file, ENV pasangan, ENV file, file default."""
    if args.kunci_file:
        u, t = _baca_kunci(os.path.abspath(os.path.expanduser(args.kunci_file)), "--kunci-file")
        return u, t, "file yang ditunjuk --kunci-file"
    u, t = os.environ.get("KANBOARD_USER", "").strip(), os.environ.get("KANBOARD_TOKEN", "").strip()
    if u and t:
        return u, t, "variabel lingkungan KANBOARD_USER + KANBOARD_TOKEN"
    if bool(u) != bool(t):
        raise Gagal("KANBOARD_USER dan KANBOARD_TOKEN harus diisi berpasangan (salah satunya kosong).", K_FILE,
                    saran="Isi keduanya, atau kosongkan keduanya dan pakai file kunci (simpan-kunci).")
    if os.environ.get("KANBOARD_KUNCI_FILE"):
        u, t = _baca_kunci(os.path.expanduser(os.environ["KANBOARD_KUNCI_FILE"]), "ENV KANBOARD_KUNCI_FILE")
        return u, t, "file yang ditunjuk KANBOARD_KUNCI_FILE"
    u, t = _baca_kunci(KUNCI_DEFAULT, "file kunci default")
    return u, t, "file kunci default di komputer ini"


def ambil_kunci(args):
    u, t, _ = _kunci_dan_sumber(args)
    return u, t


def cmd_status_kunci(args):
    """Hanya-baca: ada/tidaknya kunci tersimpan. TIDAK menampilkan token, TIDAK menghubungi Kanboard."""
    try:
        pengguna, token, sumber = _kunci_dan_sumber(args)
    except Gagal as e:
        teks = ["KUNCI TERSIMPAN: TIDAK", "Alasan: " + str(e).split(": ")[0],
                "UNTUK AGEN SAJA (jangan disalin ke chat): pakai templat B di SKILL.md (bahasa awam, tanpa "
                "perintah/folder/path); jangan memakai kunci yang ditempel pengguna."]
        cetak({"teks": samarkan("\n".join(teks)), "kunci_tersimpan": False}, args)
        return K_FILE
    _RAHASIA.append(token)
    konf = baca_konfig()
    try:
        alamat = cek_url(args.url or os.environ.get("KANBOARD_URL") or konf.get("url") or URL_DEFAULT,
                         konf.get("host_izin", []))[0]
    except Gagal as e:
        alamat = "belum valid (" + str(e) + ")"
    teks = ["KUNCI TERSIMPAN: YA", f"Pengguna: {pengguna}", f"Sumber: {sumber}", f"Alamat Kanboard: {alamat}",
            "Token tidak ditampilkan dan Kanboard belum dihubungi. UNTUK AGEN SAJA (jangan disalin ke chat): "
            "lanjutkan pekerjaan dengan kunci ini (perintah baca dulu, lalu pratinjau + tanya 'ya')."]
    cetak({"teks": samarkan("\n".join(teks)), "kunci_tersimpan": True, "pengguna": pengguna,
           "sumber": sumber, "alamat": alamat}, args)
    return 0


def _baca_kunci(path, sumber):
    if not os.path.isfile(path):
        raise Gagal(f"File kunci ({sumber}) tidak ditemukan: {path}", K_FILE,
                    saran="UNTUK AGEN SAJA (jangan disalin ke chat pemilik): beri tahu pemilik dengan kalimat "
                          "awam (SKILL.md, templat B) bahwa kunci akses belum tersimpan; penyimpanannya "
                          "dilakukan pemilik/teknisinya sendiri lewat 'simpan-kunci' atau panduan Kanboard "
                          "bagian 5. Jangan minta token ditempel di chat.")
    cek_izin_file(path)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        u, t = str(data["pengguna"]).strip(), str(data["token"]).strip()
    except (ValueError, KeyError, TypeError, OSError):
        raise Gagal(f"File kunci ({sumber}) rusak: {path}", K_FILE,
                    saran="UNTUK AGEN SAJA (jangan disalin ke chat pemilik): kunci perlu disimpan ulang oleh "
                          "pemilik/teknisinya ('simpan-kunci --ya'); beri tahu pemilik dengan kalimat awam "
                          "(SKILL.md, templat B).")
    if not u or not t:
        raise Gagal(f"File kunci ({sumber}) kosong: {path}", K_FILE)
    return u, t


def baca_konfig():
    try:
        with open(KONFIG_DEFAULT, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def cmd_atur(args):
    url, host, _, catatan = cek_url(args.url, [urllib.parse.urlsplit(args.url.strip()).hostname or ""]
                                    if args.izinkan_host else baca_konfig().get("host_izin", []))
    konf = baca_konfig()
    izin = set(konf.get("host_izin", []))
    if args.izinkan_host:
        izin.add(host)
    baru = {"url": url, "host_izin": sorted(izin)}
    teks = [f"Alamat Kanboard default: {url}"]
    if args.izinkan_host:
        teks.append(f"Host didaftarkan sebagai server milik sendiri: {host}")
    teks += catatan
    if not args.ya:
        teks.append("PRATINJAU - belum disimpan. Ulangi dengan --ya bila benar.")
        print("\n".join(teks))
        return 0
    _tulis_600(KONFIG_DEFAULT, json.dumps(baru, indent=2) + "\n")
    teks.append(f"Tersimpan di {KONFIG_DEFAULT}.")
    print("\n".join(teks))
    return 0


# ============================================================ alamat & HTTP


def cek_url(url, host_izin):
    """Validasi alamat + allowlist host. -> (url_bersih, host, tanpa_proxy, catatan)."""
    url = (url or "").strip().rstrip("/")
    if url.endswith("/jsonrpc.php"):
        url = url[: -len("/jsonrpc.php")].rstrip("/")
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise Gagal(f"Alamat Kanboard '{url}' tidak valid. Contoh: http://127.0.0.1:8080", K_INPUT)
    if p.username or p.password:
        raise Gagal("Jangan menaruh nama/sandi di alamat Kanboard; pakai simpan-kunci.", K_INPUT)
    if p.query or p.fragment:
        raise Gagal("Alamat Kanboard tidak boleh berisi '?' atau '#'.", K_INPUT)
    host = p.hostname.lower().rstrip(".")
    izin = {str(h).strip().lower().rstrip(".") for h in host_izin if str(h).strip()}
    loopback, privat = host == "localhost", False
    try:
        ip = ipaddress.ip_address(host)
        loopback = loopback or ip.is_loopback
        privat = ip.is_private and not ip.is_loopback
    except ValueError:
        pass
    if loopback:
        return url, host, True, []
    if host not in izin:
        raise Gagal(
            f"Host {host} belum ada di daftar host yang diizinkan. Demi keamanan, skill ini hanya bicara "
            f"dengan Kanboard di komputer ini atau server yang Anda daftarkan sendiri.", K_INPUT,
            saran=f"Bila server itu memang milik Anda, pemilik menjalankan: python3 scripts/kanboard.py atur "
                  f"--url {url} --izinkan-host --ya  (server di internet wajib https://).")
    if p.scheme != "https":
        if privat:
            return url, host, True, [f"PERINGATAN: koneksi ke {host} memakai http (tidak terenkripsi); aman "
                                     f"hanya di jaringan kantor sendiri."]
        raise Gagal("Kanboard di internet wajib https:// agar token tidak bisa disadap.", K_INPUT)
    return url, host, privat, []


class _TolakRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Gagal(f"Kanboard mengalihkan permintaan ke {newurl} (kode {code}). Token tidak dikirim ulang.",
                    K_INPUT, saran="Periksa alamat (mungkin harus https:// atau tanpa/ dengan subfolder).")


class Kanboard:
    def __init__(self, args):
        self.args = args
        konf = baca_konfig()
        url_arg = args.url or os.environ.get("KANBOARD_URL") or konf.get("url") or URL_DEFAULT
        self.url, self.host, tanpa_proxy, self.catatan = cek_url(url_arg, konf.get("host_izin", []))
        self.pengguna, self.token = ambil_kunci(args)
        _RAHASIA.append(self.token)
        handler = [_TolakRedirect()]
        if tanpa_proxy:
            handler.append(urllib.request.ProxyHandler({}))
        self.opener = urllib.request.build_opener(*handler)
        self._id = 0
        self._tz_server = None
        self._mode = None
        self._versi = None

    def rpc(self, metode, params=None, tulis=False):
        if metode not in METODE_BACA and metode not in METODE_TULIS:
            raise Gagal(f"Metode '{metode}' tidak ada di daftar izin skill ini (tanpa hapus/ubah pengguna).", K_INPUT)
        tulis = tulis or metode in METODE_TULIS
        self._id += 1
        body = {"jsonrpc": "2.0", "method": metode, "id": self._id}
        if params is not None:
            body["params"] = params
        auth = base64.b64encode(f"{self.pengguna}:{self.token}".encode("utf-8")).decode("ascii")
        req = urllib.request.Request(
            self.url + "/jsonrpc.php", data=json.dumps(body).encode("utf-8"), method="POST",
            headers={"Content-Type": "application/json", "Authorization": "Basic " + auth,
                     "User-Agent": "komunitech-kanboard-papan-kerja/" + VERSI_SKRIP})
        try:
            with self.opener.open(req, timeout=self.args.timeout) as r:
                mentah = r.read(MAKS_JAWABAN + 1)
                status = r.status
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                mentah = e.read(65536)
            except (OSError, http.client.HTTPException):
                mentah = b""
            if status >= 500 and status != 501:
                if tulis:
                    raise Gagal(f"Kanboard membalas galat server {status} saat MENULIS.", K_TAKPASTI,
                                saran="Data MUNGKIN sudah tersimpan. Jangan ulangi otomatis - buka Kanboard di "
                                      "browser dan cek dulu.")
                raise Gagal(f"Kanboard membalas galat server {status}.", K_KONEKSI,
                            saran="Cek log server Kanboard; coba lagi beberapa saat.")
        except Gagal:
            raise
        except urllib.error.URLError as e:
            alasan = e.reason
            if tulis and not isinstance(alasan, (ConnectionRefusedError, socket.gaierror)):
                raise Gagal(f"Koneksi ke Kanboard terputus/timeout saat MENULIS ({alasan}).", K_TAKPASTI,
                            saran="Data MUNGKIN sudah tersimpan. Jangan ulangi otomatis - cek Kanboard dulu.")
            raise Gagal(f"Kanboard di {self.url} tidak bisa dihubungi ({alasan}).", K_KONEKSI,
                        saran="Pastikan Kanboard menyala (docs/panduan-kanboard.md bagian 3) dan alamatnya "
                              "benar - buka alamat itu di browser.")
        except (TimeoutError, socket.timeout, OSError, http.client.HTTPException) as e:
            if tulis:
                raise Gagal(f"Koneksi putus/timeout saat MENULIS ({type(e).__name__}).", K_TAKPASTI,
                            saran="Data MUNGKIN sudah tersimpan. Jangan ulangi otomatis - cek Kanboard dulu.")
            raise Gagal(f"Kanboard tidak menjawab dalam {self.args.timeout:g} detik ({type(e).__name__}).",
                        K_KONEKSI, saran="Cek Kanboard menyala; bila lambat, tambah --timeout 60.")
        if len(mentah) > MAKS_JAWABAN:
            raise Gagal("Jawaban Kanboard terlalu besar (>20 MB). Dihentikan demi keamanan.", K_KONEKSI)
        if status == 401:
            raise Gagal("401 dari Kanboard: nama pengguna atau token salah.", K_AUTH,
                        saran="UNTUK AGEN SAJA (jangan disalin ke chat pemilik): kunci tersimpan ditolak Kanboard; "
                              "beri tahu pemilik dengan kalimat awam (SKILL.md, templat C). Pemilik/teknisinya "
                              "membuat token baru di Kanboard (Profil saya > API, atau Pengaturan > API untuk "
                              "'jsonrpc') lalu menyimpannya ulang ('simpan-kunci --ya'). Akun dengan 2FA wajib "
                              "memakai token, bukan sandi.")
        try:
            data = json.loads(mentah.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            if tulis:
                raise Gagal("Jawaban Kanboard saat MENULIS tidak bisa dibaca.", K_TAKPASTI,
                            saran="Data MUNGKIN sudah tersimpan. Cek Kanboard dulu.")
            raise Gagal(f"Jawaban dari {self.url}/jsonrpc.php bukan JSON-RPC Kanboard (kode HTTP {status}).",
                        K_KONEKSI, saran="Pastikan alamat menunjuk ke Kanboard (bukan aplikasi lain).")
        if not isinstance(data, dict):
            raise Gagal("Jawaban Kanboard tidak dikenali.", K_TAKPASTI if tulis else K_KONEKSI)
        if "error" in data and data["error"]:
            err = data["error"] if isinstance(data["error"], dict) else {"message": str(data["error"])}
            kode, pesan = err.get("code"), str(err.get("message", ""))[:200]
            if kode == 403 or status == 403:
                raise Gagal(f"403 Forbidden untuk '{metode}': akun ini tidak berhak, ATAU id papan/kartu tidak "
                            f"ada (Kanboard memakai 403 untuk keduanya).", K_AUTH,
                            saran="Cek id lewat daftar-papan/hari-ini; bila benar, minta admin Kanboard menambahkan "
                                  "akun ini sebagai anggota/manajer papan itu.")
            if kode == 401:
                raise Gagal("401 dari Kanboard: nama pengguna atau token salah.", K_AUTH)
            if kode == -32601:
                raise Gagal(f"Kanboard tidak mengenal metode '{metode}' (versi terlalu lama?).", K_KONEKSI,
                            saran="Perbarui Kanboard ke rilis terbaru (diuji: v1.2.54).")
            raise Gagal(f"Kanboard menolak '{metode}' (kode {kode}): {pesan}", K_INPUT)
        return data.get("result")

    # -------------------------------------------------- info dasar
    def versi(self):
        if self._versi is None:
            self._versi = str(self.rpc("getVersion") or "?")
        return self._versi

    def mode(self):
        """'pengguna' (username+token pribadi) atau 'aplikasi' (jsonrpc + token aplikasi)."""
        if self._mode is None:
            if self.pengguna == "jsonrpc":
                self._mode = ("aplikasi", None)
            else:
                me = self.rpc("getMe") or {}
                self._mode = ("pengguna", {"id": me.get("id"), "username": me.get("username"),
                                           "nama": me.get("name"), "peran": me.get("role")})
        return self._mode

    def tz_server(self):
        if self._tz_server is None:
            nama = self.rpc("getTimezone") or "UTC"
            self._tz_server = (nama, zona_server(nama))
        return self._tz_server

    def papan(self):
        mode, _ = self.mode()
        hasil = self.rpc("getAllProjects" if mode == "aplikasi" else "getMyProjects") or []
        return sorted([p for p in hasil if isinstance(p, dict)], key=lambda p: int(p.get("id", 0)))

    def kolom(self, pid):
        return sorted(self.rpc("getColumns", {"project_id": int(pid)}) or [], key=lambda c: int(c.get("position", 0)))

    def kartu(self, pid):
        return self.rpc("getAllTasks", {"project_id": int(pid), "status_id": 1}) or []

    def anggota(self, pid):
        try:
            hasil = self.rpc("getAssignableUsers", {"project_id": int(pid)}) or {}
        except Gagal:
            return {}
        if isinstance(hasil, list):  # PHP bisa mengirim array kosong
            return {}
        return {int(k): str(v) for k, v in hasil.items() if str(k).isdigit()}


# ============================================================ pembantu


def cetak(hasil, args):
    if getattr(args, "json", False):
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(hasil["teks"])


def cari_papan(kb, sebutan):
    semua = kb.papan()
    s = str(sebutan).strip()
    if s.isdigit():
        cocok = [p for p in semua if int(p["id"]) == int(s)]
        if cocok:
            return cocok[0]
        raise Gagal(f"Papan id {s} tidak ditemukan / akun ini bukan anggotanya.", K_INPUT,
                    saran="Jalankan daftar-papan untuk melihat papan yang bisa diakses.")
    persis = [p for p in semua if p["name"].strip().lower() == s.lower()]
    cocok = persis or [p for p in semua if s.lower() in p["name"].lower()]
    if not cocok:
        ada = ", ".join(p["name"] for p in semua) or "(tidak ada papan terlihat)"
        raise Gagal(f"Papan '{s}' tidak ditemukan. Papan yang ada: {ada}.", K_INPUT)
    if len(cocok) > 1:
        raise Gagal("Nama papan '{}' cocok lebih dari satu: {}. Sebutkan id-nya.".format(
            s, "; ".join(f"{p['name']} (id {p['id']})" for p in cocok)), K_GANDA)
    return cocok[0]


def cari_kolom(kolom, sebutan):
    s = str(sebutan).strip()
    if s.isdigit():
        cocok = [c for c in kolom if int(c["id"]) == int(s)]
    else:
        cocok = [c for c in kolom if c["title"].strip().lower() == s.lower()] or \
                [c for c in kolom if s.lower() in c["title"].lower()]
    if not cocok:
        raise Gagal(f"Kolom '{s}' tidak ada di papan ini. Kolom yang ada: "
                    + ", ".join(c["title"] for c in kolom) + ".", K_INPUT)
    if len(cocok) > 1:
        raise Gagal(f"Nama kolom '{s}' cocok lebih dari satu: " + ", ".join(c["title"] for c in cocok)
                    + ". Tulis nama lengkapnya.", K_GANDA)
    return cocok[0]


def papan_sasaran(kb, args):
    if getattr(args, "papan", None):
        return [cari_papan(kb, args.papan)]
    return [p for p in kb.papan() if int(p.get("is_active", 1)) == 1]


def kumpulkan(kb, args):
    """Kartu terbuka dari papan sasaran, diperkaya nama papan/kolom/PIC."""
    hasil = []
    for p in papan_sasaran(kb, args):
        kolom = kb.kolom(p["id"])
        peta_kolom = {int(c["id"]): c for c in kolom}
        terakhir = int(kolom[-1]["id"]) if kolom else None
        orang = kb.anggota(p["id"])
        for t in kb.kartu(p["id"]):
            if int(t.get("is_active", 1)) != 1:
                continue
            kid = int(t.get("column_id", 0))
            oid = int(t.get("owner_id") or 0)
            hasil.append({
                "id": int(t["id"]), "judul": str(t.get("title", "")), "papan": p["name"], "papan_id": int(p["id"]),
                "kolom": peta_kolom.get(kid, {}).get("title", f"kolom {kid}"), "kolom_id": kid,
                "kolom_terakhir": kid == terakhir, "pic": (orang.get(oid) or f"pengguna #{oid}") if oid else "",
                "date_due": int(t.get("date_due") or 0), "date_moved": int(t.get("date_moved") or 0),
            })
    return hasil


def baris_kartu(k, tz, tampil=("tenggat",)):
    tag = [f"papan: {k['papan']}", f"kolom: {k['kolom']}"]
    if "tenggat" in tampil and k["date_due"]:
        due = epoch_ke_lokal(k["date_due"], tz)
        tag.insert(0, "jatuh tempo " + tgl_pendek(due) + (f" {due:%H:%M}" if (due.hour, due.minute) != (0, 0) else ""))
    if "macet" in tampil:
        tag.insert(0, f"diam {k['hari_diam']} hari")
    if k["pic"]:
        tag.append("PIC: " + k["pic"])
    return f"- #{k['id']} {k['judul']} (" + "; ".join(tag) + ")"


def pilah(kartu, tz, hari_macet):
    now = sekarang(tz)
    hari_ini = now.date()
    batas = now.timestamp()
    telat, hini, macet = [], [], []
    for k in kartu:
        if k["date_due"]:
            due = epoch_ke_lokal(k["date_due"], tz)
            if due.date() == hari_ini and not k["kolom_terakhir"]:
                hini.append(k)
            if k["date_due"] < batas and not k["kolom_terakhir"]:
                telat.append(k)
        if not k["kolom_terakhir"] and k["date_moved"]:
            diam = int((batas - k["date_moved"]) // 86400)
            if diam >= hari_macet:
                macet.append(dict(k, hari_diam=diam))
    telat.sort(key=lambda k: k["date_due"])
    hini.sort(key=lambda k: k["date_due"])
    macet.sort(key=lambda k: -k["hari_diam"])
    return telat, hini, macet


def _laporan_satu(judul, daftar, tz, tampil, cakupan, catatan=None):
    teks = [judul, f"Papan: {cakupan}", f"Jumlah: {len(daftar)}"]
    if catatan:
        teks.append(catatan)
    teks += [baris_kartu(k, tz, tampil) for k in daftar] or ["(tidak ada kartu)"]
    return "\n".join(teks)


CATATAN_KOLOM_TERAKHIR = ("Kartu di kolom TERAKHIR papan (mis. Selesai/Tayang/Diterima) dianggap beres dan "
                          "tidak dihitung terlambat/macet.")


def cmd_baca(kb, args):
    kartu = kumpulkan(kb, args)
    cakupan = cari_papan(kb, args.papan)["name"] if args.papan else "semua papan aktif"
    telat, hini, macet = pilah(kartu, args.tz, getattr(args, "hari", 3))
    if args.perintah == "terlambat":
        daftar, judul, tampil = telat, "KARTU TERLAMBAT", ("tenggat",)
        cat = CATATAN_KOLOM_TERAKHIR
    elif args.perintah == "hari-ini":
        daftar, judul, tampil = hini, f"KARTU JATUH TEMPO HARI INI ({tgl_panjang(sekarang(args.tz))})", ("tenggat",)
        cat = ("Kartu tanpa tanggal jatuh tempo dan kartu di kolom terakhir (beres) tidak muncul di sini. Kartu jatuh tempo hari ini yang jamnya sudah "
               "lewat muncul di sini MAUPUN di 'terlambat' - jangan dijumlahkan sebagai kartu unik.")
    else:
        daftar, tampil = macet, ("macet", "tenggat")
        judul = f"KARTU MACET (tidak pindah kolom >= {args.hari} hari)"
        cat = CATATAN_KOLOM_TERAKHIR
    hasil = {"teks": _laporan_satu(judul, daftar, args.tz, tampil, cakupan, cat), "jumlah": len(daftar),
             "kartu": daftar}
    cetak(hasil, args)
    return 0


def cmd_laporan(kb, args):
    kartu = kumpulkan(kb, args)
    telat, hini, macet = pilah(kartu, args.tz, args.hari)
    now = sekarang(args.tz)
    teks = [f"LAPORAN PAPAN KERJA - {tgl_panjang(now)} {now:%H:%M} {args.tz}",
            f"Papan: {cari_papan(kb, args.papan)['name'] if args.papan else 'semua papan aktif'} | "
            f"kartu terbuka: {len(kartu)}",
            f"Terlambat {len(telat)} | Jatuh tempo hari ini {len(hini)} | Macet >= {args.hari} hari {len(macet)}", ""]
    for judul, daftar, tampil in (("TERLAMBAT", telat, ("tenggat",)), ("HARI INI", hini, ("tenggat",)),
                                  (f"MACET >= {args.hari} HARI", macet, ("macet",))):
        teks.append(f"{judul} ({len(daftar)})")
        teks += [baris_kartu(k, args.tz, tampil) for k in daftar[:MAKS_BARIS_BAGIAN]] or ["- (tidak ada)"]
        if len(daftar) > MAKS_BARIS_BAGIAN:
            teks.append(f"- ...dan {len(daftar) - MAKS_BARIS_BAGIAN} kartu lain (lihat di Kanboard)")
        teks.append("")
    hasil_teks = "\n".join(teks).rstrip()
    if len(hasil_teks) > MAKS_TELEGRAM:
        hasil_teks = hasil_teks[:MAKS_TELEGRAM - 60].rsplit("\n", 1)[0] + "\n...(dipotong; lihat detail di Kanboard)"
    cetak({"teks": hasil_teks, "terlambat": len(telat), "hari_ini": len(hini), "macet": len(macet),
           "kartu_terbuka": len(kartu)}, args)
    return 0


def cmd_cek(kb, args):
    versi = kb.versi()
    mode, me = kb.mode()
    tz_nama, _ = kb.tz_server()
    papan = kb.papan()
    teks = ["KANBOARD TERHUBUNG", f"Alamat: {kb.url}", f"Versi: {versi}"]
    if versi not in KANBOARD_TERUJI:
        teks.append(f"Catatan: versi ini belum diuji Komunitech (diuji: v1.2.54). Tetap jalan; cocokkan hasil "
                    f"penting dengan layar Kanboard.")
    if mode == "aplikasi":
        teks.append("Mode: token APLIKASI (pengguna 'jsonrpc') - akses penuh ke SEMUA papan. Untuk pemakaian "
                    "harian lebih aman memakai token pribadi pengguna (panduan bagian 5).")
    else:
        teks.append(f"Mode: token pribadi pengguna '{me.get('username')}' (peran {me.get('peran')}) - hanya "
                    f"papan tempat akun ini jadi anggota.")
        if me.get("peran") == "app-user":
            teks.append("Catatan: peran app-user hanya bisa membuat papan PRIBADI (buat-papan --pribadi).")
    teks.append(f"Zona waktu server Kanboard: {tz_nama}")
    teks.append(f"Papan terlihat: {len(papan)}")
    teks += kb.catatan
    cetak({"teks": "\n".join(teks), "versi": versi, "mode": mode, "zona_server": tz_nama,
           "jumlah_papan": len(papan)}, args)
    return 0


def cmd_daftar_papan(kb, args):
    papan = kb.papan()
    teks = ["DAFTAR PAPAN KANBOARD"]
    for p in papan:
        status = "" if int(p.get("is_active", 1)) == 1 else " [nonaktif]"
        pribadi = " [pribadi]" if int(p.get("is_private", 0)) == 1 else ""
        teks.append(f"- {p['name']} (id {p['id']}){pribadi}{status}")
    if not papan:
        teks.append("(belum ada papan yang bisa dilihat akun ini; buat dengan buat-papan atau minta admin "
                    "menambahkan akun ini ke papan)")
    cetak({"teks": "\n".join(teks), "papan": [{"id": int(p["id"]), "nama": p["name"],
                                               "aktif": int(p.get("is_active", 1)) == 1} for p in papan]}, args)
    return 0


def cmd_kolom(kb, args):
    p = cari_papan(kb, args.papan)
    kolom = kb.kolom(p["id"])
    kartu = [t for t in kb.kartu(p["id"]) if int(t.get("is_active", 1)) == 1]
    teks = [f"KOLOM PAPAN: {p['name']} (id {p['id']})"]
    data = []
    for c in kolom:
        n = sum(1 for t in kartu if int(t.get("column_id", 0)) == int(c["id"]))
        batas = int(c.get("task_limit") or 0)
        tanda = f" / batas {batas}" + (" - MELEBIHI BATAS" if n > batas else "") if batas else ""
        teks.append(f"{c['position']}. {c['title']} (id {c['id']}): {n} kartu{tanda}")
        data.append({"id": int(c["id"]), "judul": c["title"], "posisi": int(c["position"]), "kartu": n,
                     "batas": batas})
    cetak({"teks": "\n".join(teks), "papan_id": int(p["id"]), "kolom": data}, args)
    return 0


def cmd_template(args):
    teks = ["TEMPLATE PAPAN (pakai: buat-papan --jenis <kode> --nama \"...\")"]
    for kode, t in TEMPLATE.items():
        kol = " > ".join(k[0] + (f" [maks {k[1]}]" if k[1] else "") for k in t["kolom"])
        teks.append(f"- {kode}: {t['nama']}\n  {kol}")
    cetak({"teks": "\n".join(teks), "template": {k: [c[0] for c in v["kolom"]] for k, v in TEMPLATE.items()}}, args)
    return 0


def cmd_buat_papan(kb, args):
    if args.jenis not in TEMPLATE:
        raise Gagal(f"Jenis '{args.jenis}' tidak dikenal. Pilihan: {', '.join(TEMPLATE)}.", K_INPUT)
    nama = (args.nama or "").strip()
    if not nama or len(nama) > 255:
        raise Gagal("Nama papan wajib diisi (maks 255 karakter), mis. --nama \"Produksi Konveksi Ayu\".", K_INPUT)
    t = TEMPLATE[args.jenis]
    mode, me = kb.mode()
    if args.pribadi and mode == "aplikasi":
        raise Gagal("--pribadi hanya untuk token pribadi pengguna (bukan 'jsonrpc').", K_INPUT)
    ada = [p for p in kb.papan() if p["name"].strip().lower() == nama.lower()]
    if ada:
        raise Gagal(f"Papan bernama '{nama}' sudah ada (id {ada[0]['id']}). Tidak dibuat ganda.", K_GANDA,
                    saran="Pakai nama lain, atau pakai papan yang sudah ada.")
    teks = [f"PRATINJAU PAPAN BARU: {nama}", f"Template: {args.jenis} - {t['nama']}",
            "Jenis: " + ("PRIBADI (hanya Anda)" if args.pribadi else "papan tim (anggota diatur admin di Kanboard)"),
            "Kolom:"]
    teks += [f"  {i}. {k[0]}" + (f" (batas {k[1]} kartu)" if k[1] else "") + f" - {k[2]}"
             for i, k in enumerate(t["kolom"], 1)]
    if not args.ya:
        teks.append("Belum ada yang dibuat. Simpan ke Kanboard? (ya/tidak)")
        cetak({"teks": "\n".join(teks), "pratinjau": True}, args)
        return 0
    keterangan = f"Template {args.jenis} (Komunitech)"
    if args.pribadi:
        pid = kb.rpc("createMyPrivateProject", {"name": nama, "description": keterangan})
    else:
        try:
            pid = kb.rpc("createProject", {"name": nama, "description": keterangan})
        except Gagal as e:
            if e.kode != K_AUTH:
                raise
            raise Gagal("Akun ini tidak boleh membuat papan TIM (peran Kanboard 'User' biasa). Tidak ada yang dibuat.",
                        K_AUTH, saran="Pilihan: (1) buat papan pribadi dengan --pribadi; (2) minta admin Kanboard "
                                      "mengubah peran akun ini menjadi Manager (Pengguna > ubah > Peran).")
    if not pid:
        raise Gagal("Kanboard menolak membuat papan (nama tidak valid?).", K_INPUT)
    pid = int(pid)
    sudah = []
    try:
        lama = kb.kolom(pid)
        for i, (judul, batas, ket) in enumerate(t["kolom"]):
            if i < len(lama):
                ok = kb.rpc("updateColumn", {"column_id": int(lama[i]["id"]), "title": judul,
                                             "task_limit": batas, "description": ket})
            else:
                ok = kb.rpc("addColumn", {"project_id": pid, "title": judul, "task_limit": batas,
                                          "description": ket})
            if not ok:
                raise Gagal(f"Kanboard menolak kolom '{judul}'.", K_TAKPASTI)
            sudah.append(judul)
    except Gagal as e:
        raise Gagal(f"Papan '{nama}' (id {pid}) SUDAH dibuat, tetapi pengaturan kolom berhenti: {e}. Kolom yang "
                    f"sudah diatur: {', '.join(sudah) or '(belum ada)'}.", K_TAKPASTI,
                    saran="Jangan jalankan buat-papan lagi (akan ditolak karena nama sama). Lengkapi kolom sisanya "
                          "di Kanboard: buka papan > ikon roda > Kolom.")
    teks = [f"PAPAN DIBUAT: {nama} (id {pid})", f"Template: {args.jenis} - {t['nama']}", "Kolom:"]
    teks += [f"  {i}. {k}" for i, k in enumerate(sudah, 1)]
    ekstra = kb.kolom(pid)[len(t["kolom"]):]
    if ekstra:
        teks.append("Catatan: papan ini punya kolom bawaan tambahan yang TIDAK dihapus skill: "
                    + ", ".join(c["title"] for c in ekstra) + ". Hapus manual di Kanboard bila tidak perlu.")
    teks.append(f"Buka: {kb.url}/?controller=BoardViewController&action=show&project_id={pid}")
    cetak({"teks": "\n".join(teks), "papan_id": pid, "kolom": sudah}, args)
    return 0


def cmd_tambah_kartu(kb, args):
    judul = (args.judul or "").strip()
    if not judul or len(judul) > 200:
        raise Gagal("Judul kartu wajib diisi (maks 200 karakter).", K_INPUT)
    if not args.papan:
        raise Gagal("Sebutkan papannya: --papan \"nama atau id\" (lihat daftar-papan).", K_INPUT)
    p = cari_papan(kb, args.papan)
    kolom = kb.kolom(p["id"])
    if not kolom:
        raise Gagal("Papan ini belum punya kolom.", K_INPUT)
    kol = cari_kolom(kolom, args.kolom) if args.kolom else kolom[0]
    params = {"title": judul, "project_id": int(p["id"]), "column_id": int(kol["id"])}
    ringkas = [f"PRATINJAU KARTU BARU", f"Papan: {p['name']} (id {p['id']})", f"Kolom: {kol['title']}",
               f"Judul: {judul}"]
    if args.tenggat:
        tgl, jam, menit, peringatan = parse_tenggat_lengkap(args.tenggat, sekarang(args.tz).date())
        tz_nama, tzs = kb.tz_server()
        params["date_due"], epoch = tenggat_ke_server(tgl, jam, menit, args.tz, tzs)
        ringkas.append(f"Jatuh tempo: {tgl_panjang(tgl)} jam {jam:02d}:{menit:02d} {args.tz}")
        ringkas += peringatan
        if epoch < sekarang(args.tz).timestamp():
            ringkas.append("PERINGATAN: jatuh tempo ini SUDAH LEWAT - kartu langsung tercatat terlambat. Benar?")
    if args.ke:
        orang = kb.anggota(p["id"])
        kunci = args.ke.strip().lower()
        persis = [(i, n) for i, n in orang.items() if n.lower() == kunci]
        if not persis and len(kunci) < 2:
            raise Gagal(f"Nama PIC '{args.ke}' terlalu pendek untuk dicocokkan.", K_INPUT,
                        saran="Tulis minimal 2 huruf nama, atau nama lengkapnya.")
        cocok = persis or [(i, n) for i, n in orang.items() if kunci in n.lower()]
        if not cocok:
            raise Gagal(f"Anggota '{args.ke}' tidak ditemukan di papan ini. Yang bisa ditugaskan: "
                        + (", ".join(orang.values()) or "(tidak ada)") + ".", K_INPUT,
                        saran="Tambahkan orang itu sebagai anggota papan di Kanboard (ikon roda > Izin), atau "
                              "buat kartu tanpa --ke.")
        if len(cocok) > 1:
            raise Gagal(f"'{args.ke}' cocok lebih dari satu: " + ", ".join(n for _, n in cocok) + ".", K_GANDA)
        params["owner_id"] = int(cocok[0][0])
        ringkas.append(f"PIC: {cocok[0][1]}" + ("" if persis else f" (dicocokkan sebagian dari '{args.ke.strip()}' - benar?)"))
    if args.catatan:
        params["description"] = args.catatan[:5000]
        ringkas.append(f"Catatan: {args.catatan[:200]}")
    kembar = [t for t in kb.kartu(p["id"]) if str(t.get("title", "")).strip().lower() == judul.lower()]
    if kembar and not args.boleh_ganda:
        raise Gagal(f"Sudah ada kartu terbuka berjudul sama di papan ini (#{kembar[0]['id']}). Tidak dibuat ganda.",
                    K_GANDA, saran="Bila memang kartu berbeda, ulangi dengan --boleh-ganda atau ubah judulnya.")
    if not args.ya:
        ringkas.append("Belum disimpan. Simpan ke Kanboard? (ya/tidak)")
        cetak({"teks": "\n".join(ringkas), "pratinjau": True, "params": params}, args)
        return 0
    tid = kb.rpc("createTask", params)
    if not tid:
        raise Gagal("Kanboard menolak membuat kartu (data tidak valid atau PIC tidak boleh ditugaskan).", K_INPUT)
    ringkas[0] = f"KARTU DIBUAT: #{tid}"
    cetak({"teks": "\n".join(ringkas), "kartu_id": int(tid)}, args)
    return 0


def cmd_pindah_kartu(kb, args):
    t = kb.rpc("getTask", {"task_id": int(args.id)})
    if not t:
        raise Gagal(f"Kartu #{args.id} tidak ditemukan.", K_KONEKSI)
    pid = int(t["project_id"])
    kolom = kb.kolom(pid)
    tujuan = cari_kolom(kolom, args.ke_kolom)
    asal = next((c["title"] for c in kolom if int(c["id"]) == int(t["column_id"])), f"kolom {t['column_id']}")
    teks = [f"PRATINJAU PINDAH KARTU #{t['id']}: {t['title']}", f"Dari: {asal}", f"Ke: {tujuan['title']}"]
    if int(t["column_id"]) == int(tujuan["id"]):
        teks[0] = f"KARTU #{t['id']} SUDAH di kolom {tujuan['title']} - tidak ada yang diubah."
        cetak({"teks": "\n".join(teks[:1]), "berubah": False}, args)
        return 0
    if int(t.get("is_active", 1)) != 1:
        raise Gagal(f"Kartu #{t['id']} sudah DITUTUP di Kanboard; buka kembali lewat layar Kanboard bila perlu.",
                    K_INPUT)
    if not args.ya:
        teks.append("Belum dipindah. Lanjut? (ya/tidak)")
        cetak({"teks": "\n".join(teks), "pratinjau": True}, args)
        return 0
    ok = kb.rpc("moveTaskPosition", {"project_id": pid, "task_id": int(t["id"]), "column_id": int(tujuan["id"]),
                                     "position": 1, "swimlane_id": int(t.get("swimlane_id") or 0)})
    if not ok:
        raise Gagal("Kanboard menolak memindahkan kartu.", K_INPUT)
    teks[0] = f"KARTU DIPINDAH #{t['id']}: {t['title']}"
    cetak({"teks": "\n".join(teks), "berubah": True}, args)
    return 0


# ============================================================ argparse


def _opsi_umum(p):
    p.add_argument("--url", default=None, help="Alamat Kanboard (default: ENV KANBOARD_URL / atur / "
                                               + URL_DEFAULT + ")")
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--tz", default="WIB", choices=list(TZ_OFFSET))
    p.add_argument("--json", action="store_true")
    p.add_argument("--timeout", type=float, default=20.0, help="Batas tunggu jawaban (detik)")


def buat_parser():
    ap = argparse.ArgumentParser(prog="kanboard.py", description="Asisten papan kerja Kanboard (Komunitech)",
                                 allow_abbrev=False)
    sub = ap.add_subparsers(dest="perintah", required=True)
    p = sub.add_parser("simpan-kunci", allow_abbrev=False)
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--ya", action="store_true")
    p = sub.add_parser("status-kunci", allow_abbrev=False)
    p.add_argument("--url", default=None)
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("atur", allow_abbrev=False)
    p.add_argument("--url", required=True)
    p.add_argument("--izinkan-host", dest="izinkan_host", action="store_true")
    p.add_argument("--ya", action="store_true")
    p = sub.add_parser("template", allow_abbrev=False)
    p.add_argument("--json", action="store_true")
    for nama in ("cek", "daftar-papan"):
        _opsi_umum(sub.add_parser(nama, allow_abbrev=False))
    p = sub.add_parser("kolom", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--papan", required=True)
    for nama in ("hari-ini", "terlambat", "macet", "laporan"):
        p = sub.add_parser(nama, allow_abbrev=False)
        _opsi_umum(p)
        p.add_argument("--papan", default=None)
        if nama in ("macet", "laporan"):
            p.add_argument("--hari", type=int, default=3, help="Ambang macet dalam hari (default 3)")
    p = sub.add_parser("buat-papan", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--jenis", required=True, choices=list(TEMPLATE))
    p.add_argument("--nama", required=True)
    p.add_argument("--pribadi", action="store_true")
    p.add_argument("--ya", action="store_true")
    p = sub.add_parser("tambah-kartu", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--papan", default=None)
    p.add_argument("--judul", default=None)
    p.add_argument("--kolom", default=None)
    p.add_argument("--tenggat", default=None)
    p.add_argument("--ke", default=None)
    p.add_argument("--catatan", default=None)
    p.add_argument("--boleh-ganda", dest="boleh_ganda", action="store_true")
    p.add_argument("--ya", action="store_true")
    p = sub.add_parser("pindah-kartu", allow_abbrev=False)
    _opsi_umum(p)
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--ke-kolom", dest="ke_kolom", required=True)
    p.add_argument("--ya", action="store_true")
    return ap


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        if getattr(args, "hari", 3) < 1 or getattr(args, "hari", 3) > 365:
            raise Gagal("--hari harus 1 sampai 365.", K_INPUT)
        if getattr(args, "timeout", 20) <= 0:
            raise Gagal("--timeout harus lebih dari 0.", K_INPUT)
        if args.perintah == "simpan-kunci":
            return cmd_simpan_kunci(args)
        if args.perintah == "status-kunci":
            return cmd_status_kunci(args)
        if args.perintah == "atur":
            return cmd_atur(args)
        if args.perintah == "template":
            return cmd_template(args)
        kb = Kanboard(args)
        peta = {"cek": cmd_cek, "daftar-papan": cmd_daftar_papan, "kolom": cmd_kolom, "hari-ini": cmd_baca,
                "terlambat": cmd_baca, "macet": cmd_baca, "laporan": cmd_laporan, "buat-papan": cmd_buat_papan,
                "tambah-kartu": cmd_tambah_kartu, "pindah-kartu": cmd_pindah_kartu}
        return peta[args.perintah](kb, args)
    except Gagal as e:
        sys.stderr.write("GAGAL: " + samarkan(e) + "\n")
        if e.saran:
            sys.stderr.write("SARAN: " + samarkan(e.saran) + "\n")
        return e.kode
    except KeyboardInterrupt:
        sys.stderr.write("Dibatalkan.\n")
        return 130
    except Exception as e:  # data tak terduga dari server: pesan ramah, bukan traceback
        sys.stderr.write("GAGAL: Data dari Kanboard tidak sesuai bentuk yang diharapkan "
                         f"({type(e).__name__}).\n")
        sys.stderr.write("SARAN: Pastikan alamat menunjuk ke Kanboard asli (versi v1.2.x) lalu ulangi; bila tetap "
                         "begini, jangan ulangi perintah tulis sebelum mengecek Kanboard.\n")
        return K_KONEKSI


if __name__ == "__main__":
    sys.exit(main())
