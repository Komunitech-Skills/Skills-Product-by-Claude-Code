#!/usr/bin/env python3
"""vikunja-tugas (Komunitech) - asisten tugas/proyek Vikunja untuk tim kecil Indonesia.

Memanggil REST API resmi Vikunja (server milik pengguna sendiri, biasanya http://127.0.0.1:3456)
lewat token API berskop (header 'Authorization: Bearer tk_...'). Python standar saja, tanpa
paket tambahan. Menolak alamat selain komputer/jaringan sendiri kecuali --izinkan-jarak-jauh.

Perintah:
  simpan-kunci    simpan token API ke file lokal (dibaca tersembunyi, tidak pernah dicetak)
  cek             cek server Vikunja & izin token bisa dihubungi
  daftar-proyek   daftar proyek yang bisa dilihat token ini
  hari-ini        tugas jatuh tempo hari ini, belum selesai
  terlambat       tugas jatuh tempo terlewat, belum selesai
  minggu-ini      tugas jatuh tempo 7 hari ke depan, belum selesai
  cari            cari tugas (judul mengandung kata kunci)
  tambah          tambah tugas baru (pratinjau; simpan dengan --ya)
  selesai         tandai tugas selesai (pratinjau; simpan dengan --ya)
  ringkasan       ringkasan tugas terbuka dikelompokkan per anggota
  dari-teks       ubah notulen/rangkuman WA menjadi draf daftar tugas (JSON, belum dikirim)

Windows: pakai `python` atau `py` sebagai ganti `python3`. Tambah --json untuk hasil terstruktur.
"""
import argparse
import datetime as dt
import getpass
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request

VERSI = "1.0.1"
VIKUNJA_TERUJI = ("2.6.0", "v2.6.0")
SINI = os.path.dirname(os.path.abspath(__file__))
FOLDER_SKILL = os.path.dirname(SINI)
KUNCI_DEFAULT = os.path.join(os.path.expanduser("~"), ".komunitech", "vikunja-kunci.txt")
URL_DEFAULT = "http://127.0.0.1:3456"
TOKEN_PREFIX = "tk_"

K_INPUT, K_FILE, K_KONEKSI, K_AUTH, K_TULIS, K_GANDA, K_TAKPASTI = 2, 3, 4, 5, 6, 7, 8

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
BULAN_KATA = {
    "jan": 1, "januari": 1, "feb": 2, "februari": 2, "peb": 2, "mar": 3, "maret": 3, "apr": 4,
    "april": 4, "mei": 5, "jun": 6, "juni": 6, "jul": 7, "juli": 7, "agu": 8, "agt": 8, "ags": 8,
    "agustus": 8, "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "nov": 11,
    "nop": 11, "november": 11, "des": 12, "desember": 12,
}
HARI_KATA = {
    "senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "jum'at": 4, "jum at": 4,
    "sabtu": 5, "minggu": 6,
}
TZ_OFFSET = {"WIB": 7, "WITA": 8, "WIT": 9}
PRIORITAS_LABEL = {0: "tanpa prioritas", 1: "rendah", 2: "sedang", 3: "tinggi", 4: "mendesak",
                   5: "lakukan sekarang"}


class Gagal(Exception):
    def __init__(self, pesan, kode=K_INPUT):
        super().__init__(pesan)
        self.kode = kode


# ============================================================ zona waktu & tanggal


def zona(tz_nama):
    return dt.timezone(dt.timedelta(hours=TZ_OFFSET.get(tz_nama, 7)))


def sekarang(tz_nama):
    return dt.datetime.now(zona(tz_nama))


def format_tanggal_panjang(tanggal):
    return f"{HARI[tanggal.weekday()]}, {tanggal.day} {BULAN[tanggal.month - 1]} {tanggal.year}"


def format_tanggal_pendek(tanggal):
    return f"{tanggal.day} {BULAN[tanggal.month - 1][:3]} {tanggal.year}"


def ke_iso_utc(tanggal, jam=17, menit=0, tz_nama="WIB"):
    """date lokal + jam -> string RFC3339 UTC ('...Z') untuk dikirim ke Vikunja."""
    lokal = dt.datetime(tanggal.year, tanggal.month, tanggal.day, jam, menit, tzinfo=zona(tz_nama))
    return lokal.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dari_iso_utc(teks, tz_nama="WIB"):
    """String RFC3339 dari Vikunja -> datetime lokal (--tz), atau None bila kosong/nol."""
    if not teks or teks.startswith("0001-01-01"):
        return None
    teks = teks.replace("Z", "+00:00")
    try:
        u = dt.datetime.fromisoformat(teks)
    except ValueError:
        return None
    if u.tzinfo is None:
        u = u.replace(tzinfo=dt.timezone.utc)
    return u.astimezone(zona(tz_nama))


_JAM_RE = re.compile(r"\bjam\s+(\d{1,2})[:.](\d{2})\b|\b(\d{1,2}):(\d{2})\b")


def _ambil_jam(teks):
    """Cari 'jam 14:00' / '14:00' di akhir teks -> (jam, menit, sisa_teks) atau (17, 0, teks)."""
    m = _JAM_RE.search(teks)
    if not m:
        return 17, 0, teks
    if m.group(1):
        j, mi = int(m.group(1)), int(m.group(2))
    else:
        j, mi = int(m.group(3)), int(m.group(4))
    if not (0 <= j <= 23 and 0 <= mi <= 59):
        return 17, 0, teks
    return j, mi, (teks[:m.start()] + teks[m.end():]).strip()


def cocok_tanggal_kata(teks, acuan):
    """Cari SATU frasa tanggal Indonesia di dalam teks bebas. -> date atau None (tidak melempar)."""
    t = teks.lower().strip()
    if re.search(r"\bhari ini\b|\bsekarang\b", t):
        return acuan
    if re.search(r"\bbesok\b", t):
        return acuan + dt.timedelta(days=1)
    if re.search(r"\blusa\b", t):
        return acuan + dt.timedelta(days=2)
    m = re.search(r"\b(\d{1,2})\s+hari\s+lagi\b", t)
    if m:
        return acuan + dt.timedelta(days=int(m.group(1)))
    if re.search(r"\bminggu depan\b|\bpekan depan\b", t):
        return acuan + dt.timedelta(days=7)
    m = re.search(r"\b(senin|selasa|rabu|kamis|jum'?at|jum at|sabtu|minggu)\s+depan\b", t)
    if m:
        nama = m.group(1).replace("'", "").replace(" ", "")
        target = HARI_KATA[nama]
        delta = (target - acuan.weekday()) % 7
        if delta == 0:
            delta = 7
        return acuan + dt.timedelta(days=delta + 7)
    m = re.search(r"\b(senin|selasa|rabu|kamis|jum'?at|jum at|sabtu|minggu)\b", t)
    if m:
        nama = m.group(1).replace("'", "").replace(" ", "")
        target = HARI_KATA[nama]
        delta = (target - acuan.weekday()) % 7
        return acuan + dt.timedelta(days=delta)
    m = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", t)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            return dt.date(y, mo, d)
        except ValueError:
            return None
    m = re.search(r"\b(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?\b", t)
    if m:
        d, mo = int(m.group(1)), int(m.group(2))
        y = int(m.group(3)) if m.group(3) else acuan.year
        if y < 100:
            y += 2000
        try:
            hasil = dt.date(y, mo, d)
        except ValueError:
            return None
        if not m.group(3) and hasil < acuan - dt.timedelta(days=1):
            try:
                hasil = dt.date(y + 1, mo, d)
            except ValueError:
                pass
        return hasil
    m = re.search(r"\b(\d{1,2})\s+([a-z]+)\.?(?:\s+(\d{4}))?\b", t)
    if m and m.group(2) in BULAN_KATA:
        d = int(m.group(1))
        mo = BULAN_KATA[m.group(2)]
        y = int(m.group(3)) if m.group(3) else acuan.year
        try:
            hasil = dt.date(y, mo, d)
        except ValueError:
            return None
        if not m.group(3) and hasil < acuan - dt.timedelta(days=1):
            try:
                hasil = dt.date(y + 1, mo, d)
            except ValueError:
                pass
        return hasil
    return None


def parse_tenggat(teks, acuan, tz_nama="WIB"):
    """--tenggat "besok jam 14:00" -> string ISO UTC untuk Vikunja. Melempar Gagal bila tidak jelas."""
    jam, menit, sisa = _ambil_jam(teks)
    tanggal = cocok_tanggal_kata(sisa, acuan)
    if tanggal is None:
        raise Gagal(
            "Tenggat tidak dikenali: " + repr(teks) + ". Format yang didukung: 'hari ini', "
            "'besok', 'lusa', 'N hari lagi', nama hari ('Jumat', 'Jumat depan'), 'minggu depan', "
            "'25/10', '25/10/2026', '25 Oktober 2026', '2026-10-25' — boleh diakhiri 'jam 14:00'.",
            K_INPUT,
        )
    return ke_iso_utc(tanggal, jam, menit, tz_nama), tanggal


# ============================================================ token & konfigurasi


def path_kunci(args):
    if args.kunci_file:
        return os.path.abspath(os.path.expanduser(args.kunci_file))
    return KUNCI_DEFAULT


def cek_izin_file(path):
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        return
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        sys.stderr.write(
            f"PERINGATAN: file kunci {path} bisa dibaca pengguna lain di komputer ini. "
            f"Jalankan: chmod 600 {path}\n"
        )


def simpan_kunci(args):
    path = path_kunci(args)
    if os.path.exists(path) and not args.ya:
        raise Gagal(
            f"File kunci sudah ada: {path}\n"
            f"Untuk mengganti token lama, ulangi perintah ini dengan tambahan --ya. "
            f"Untuk menyimpan token KEDUA (mis. token baca-tulis terpisah), pakai "
            f"--kunci-file <path lain>.",
            K_FILE,
        )
    sys.stderr.write(f"Token akan disimpan di: {path}\n")
    token = getpass.getpass("Tempel token API Vikunja (tidak terlihat), lalu Enter: ").strip()
    if not token:
        raise Gagal("Token kosong, tidak disimpan.", K_INPUT)
    if not token.startswith(TOKEN_PREFIX):
        raise Gagal(
            f"Token Vikunja seharusnya diawali '{TOKEN_PREFIX}'. Salin ulang dari "
            f"Settings > API Tokens di Vikunja (tampil hanya sekali saat dibuat).",
            K_INPUT,
        )
    if re.search(r"\s", token):
        raise Gagal("Token berisi spasi/baris baru — kemungkinan tersalin rusak. Salin ulang.", K_INPUT)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(token + "\n")
    os.chmod(path, 0o600)
    print(f"Token tersimpan di {path} (izin 600).")
    return 0


def ambil_token(args):
    if args.kunci_file:
        if os.environ.get("VIKUNJA_TOKEN"):
            sys.stderr.write(
                "PERINGATAN: --kunci-file dipakai; ENV VIKUNJA_TOKEN DIABAIKAN.\n"
            )
        path = os.path.abspath(os.path.expanduser(args.kunci_file))
        return _baca_file_token(path, "--kunci-file")
    if os.environ.get("VIKUNJA_TOKEN"):
        return os.environ["VIKUNJA_TOKEN"].strip()
    if os.environ.get("VIKUNJA_TOKEN_FILE"):
        return _baca_file_token(os.environ["VIKUNJA_TOKEN_FILE"], "ENV VIKUNJA_TOKEN_FILE")
    return _baca_file_token(KUNCI_DEFAULT, "file kunci default")


def _baca_file_token(path, sumber):
    if not os.path.isfile(path):
        raise Gagal(
            f"File kunci ({sumber}) tidak ditemukan: {path}. Jalankan dulu "
            f"'python3 vikunja.py simpan-kunci' (lihat docs/panduan-vikunja.md bagian 6).",
            K_FILE,
        )
    cek_izin_file(path)
    token = open(path, encoding="utf-8").read().strip()
    if not token:
        raise Gagal(f"File kunci ({sumber}) kosong: {path}.", K_FILE)
    if re.search(r"\s", token):
        raise Gagal(f"File kunci ({sumber}) berisi spasi/baris ganda — simpan ulang dengan 'simpan-kunci'.", K_FILE)
    return token


def tampilkan_token_tersamar(token):
    if len(token) <= 8:
        return "tk_****"
    return token[:6] + "****" + token[-4:]


# ============================================================ HTTP ke Vikunja


def periksa_url(url, izinkan_jarak_jauh):
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https"):
        raise Gagal(f"URL Vikunja tidak valid: {url}", K_INPUT)
    host = (u.hostname or "").lower()
    lokal = host in ("127.0.0.1", "localhost", "::1")
    jaringan_kantor = re.match(r"^(192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.)", host or "")
    if lokal:
        return
    if not izinkan_jarak_jauh:
        raise Gagal(
            f"Alamat Vikunja '{url}' bukan komputer ini (127.0.0.1/localhost). Jangan buka Vikunja "
            f"ke internet (lihat docs/panduan-vikunja.md bagian 4). Bila ini memang server Anda "
            f"sendiri di jaringan kantor/VPS milik sendiri, tegaskan dengan --izinkan-jarak-jauh.",
            K_INPUT,
        )
    if not jaringan_kantor and u.scheme != "https":
        raise Gagal(
            f"Alamat internet '{url}' wajib HTTPS (bukan jaringan kantor 192.168.x/10.x/172.16-31.x). "
            f"Vikunja tidak boleh diakses lewat http biasa di internet terbuka.",
            K_INPUT,
        )
    if jaringan_kantor and u.scheme != "https":
        sys.stderr.write(f"PERINGATAN: {url} memakai http biasa di jaringan kantor, bukan komputer ini sendiri.\n")


def panggil(method, path, args, token=None, body=None, tulis=False, timeout=None):
    periksa_url(args.url, args.izinkan_jarak_jauh)
    timeout = timeout if timeout is not None else getattr(args, "timeout", 15)
    url = args.url.rstrip("/") + "/api/v1" + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if token:
        req.add_header("Authorization", "Bearer " + token)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            mentah = resp.read()
            header_halaman = resp.headers.get("X-Pagination-Total-Pages")
            hasil = json.loads(mentah) if mentah else None
            return hasil, header_halaman
    except urllib.error.HTTPError as e:
        mentah = e.read()
        pesan_server = ""
        try:
            j = json.loads(mentah)
            pesan_server = j.get("message", "")
        except (ValueError, TypeError):
            pass
        if e.code == 401:
            raise Gagal(
                "401 dari Vikunja: token salah/kedaluwarsa/dihapus, ATAU token tidak punya izin "
                f"untuk aksi ini (Vikunja memakai kode 401 untuk kedua kasus). Pesan server: "
                f"{pesan_server or '(kosong)'}. Cek Settings > API Tokens di Vikunja; lihat "
                f"docs/panduan-vikunja.md bagian 6 untuk daftar izin yang dibutuhkan.",
                K_AUTH,
            )
        if e.code == 403:
            raise Gagal(f"403 dari Vikunja: akses ditolak. Pesan server: {pesan_server or '(kosong)'}", K_AUTH)
        if e.code == 404:
            raise Gagal(f"404: tidak ditemukan di Vikunja ({path}). {pesan_server}", K_KONEKSI)
        if e.code == 400:
            raise Gagal(f"Vikunja menolak permintaan (400): {pesan_server or mentah[:200]}", K_INPUT)
        if 500 <= e.code < 600:
            if tulis:
                raise Gagal(
                    f"Vikunja membalas galat server ({e.code}) saat MENULIS. Data MUNGKIN sudah "
                    f"masuk sebagian. Jangan ulangi otomatis — cek Vikunja dulu. Pesan: {pesan_server}",
                    K_TAKPASTI,
                )
            raise Gagal(f"Vikunja membalas galat server ({e.code}): {pesan_server}", K_KONEKSI)
        raise Gagal(f"Vikunja membalas kode {e.code}: {pesan_server or mentah[:200]}", K_KONEKSI)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        if tulis:
            raise Gagal(
                f"Tidak bisa memastikan hasil: koneksi ke Vikunja terputus/timeout saat MENULIS "
                f"({e}). Data MUNGKIN sudah tersimpan sebagian. Jangan ulangi otomatis — buka "
                f"Vikunja di browser dan cek dulu.",
                K_TAKPASTI,
            )
        raise Gagal(
            f"Tidak bisa menghubungi Vikunja di {args.url} ({e}). Pastikan Vikunja menyala "
            f"(docs/panduan-vikunja.md bagian 3/7) dan alamatnya benar.",
            K_KONEKSI,
        )
    except json.JSONDecodeError:
        raise Gagal("Jawaban Vikunja tidak bisa dibaca (terpotong?). Coba lagi.", K_TAKPASTI if tulis else K_KONEKSI)


def ambil_semua_halaman(path_dasar, args, token, query):
    hasil = []
    halaman = 1
    while True:
        q = dict(query)
        q["page"] = halaman
        q["per_page"] = 50
        qs = urllib.parse.urlencode(q)
        data, total_halaman = panggil("GET", path_dasar + "?" + qs, args, token=token)
        if data:
            hasil.extend(data)
        total = int(total_halaman) if total_halaman else 1
        if halaman >= total or not data or halaman >= 20:
            break
        halaman += 1
    return hasil


# ============================================================ info server & proyek


def info_server(args):
    data, _ = panggil("GET", "/info", args)
    return data or {}


def daftar_proyek_mentah(args, token):
    return ambil_semua_halaman("/projects", args, token, {})


def proyek_nyata(proyek):
    """Proyek biasa (id > 0). Vikunja memberi proyek semu id<=0 (mis. -2 'My Open Tasks')."""
    return proyek.get("id", 0) > 0


def cari_proyek(args, token, sebutan):
    proyek = daftar_proyek_mentah(args, token)
    nyata = [p for p in proyek if proyek_nyata(p)]
    if sebutan.lstrip("-").isdigit():
        pid = int(sebutan)
        cocok = [p for p in nyata if p["id"] == pid]
        if cocok:
            return cocok[0]
        raise Gagal(
            f"Proyek id {pid} tidak ditemukan atau token tidak berhak melihatnya. "
            f"Jalankan 'daftar-proyek' untuk melihat daftar yang bisa diakses.",
            K_INPUT,
        )
    kunci = sebutan.strip().lower()
    cocok = [p for p in nyata if kunci in p["title"].lower()]
    if not cocok:
        tersedia = ", ".join(p["title"] for p in nyata) or "(tidak ada proyek terlihat)"
        raise Gagal(f"Proyek '{sebutan}' tidak ditemukan. Proyek yang ada: {tersedia}.", K_INPUT)
    if len(cocok) > 1:
        opsi = "; ".join(f"{p['title']} (id {p['id']})" for p in cocok)
        raise Gagal(f"Nama proyek '{sebutan}' cocok lebih dari satu: {opsi}. Sebutkan id-nya.", K_INPUT)
    return cocok[0]


# ============================================================ tugas: baca


def ambil_tugas(args, token, filter_expr, proyek_id=None, cari_teks=None):
    query = {"filter": filter_expr} if filter_expr else {}
    if cari_teks:
        query["s"] = cari_teks
    if proyek_id:
        path = f"/projects/{proyek_id}/tasks"
    else:
        path = "/tasks"
    return ambil_semua_halaman(path, args, token, query)


def ringkas_tugas(t, tz_nama, proyek_map=None):
    tenggat = dari_iso_utc(t.get("due_date", ""), tz_nama)
    baris = f"- {t['title']}"
    tag = []
    if t.get("priority"):
        tag.append(PRIORITAS_LABEL.get(t["priority"], f"prioritas {t['priority']}"))
    if tenggat:
        tag.append(f"jatuh tempo {format_tanggal_pendek(tenggat.date())}")
    if proyek_map is not None:
        tag.append(f"proyek: {proyek_map.get(t.get('project_id'), '?')}")
    if t.get("assignees"):
        tag.append("PIC: " + ", ".join(a.get("username", "?") for a in t["assignees"]))
    if tag:
        baris += " (" + "; ".join(tag) + ")"
    return baris


def cmd_daftar_proyek(args, token):
    proyek = daftar_proyek_mentah(args, token)
    nyata = sorted((p for p in proyek if proyek_nyata(p)), key=lambda p: p["id"])
    teks = ["DAFTAR PROYEK VIKUNJA"] + [f"- {p['title']} (id {p['id']})" for p in nyata]
    if not nyata:
        teks.append("(belum ada proyek; buat dulu di Vikunja atau minta agent membuatkannya)")
    hasil = {"teks": "\n".join(teks), "proyek": [{"id": p["id"], "judul": p["title"]} for p in nyata]}
    cetak(hasil, args)
    return 0


def _filter_dan_cetak(args, token, judul, filter_expr, proyek_arg, catatan=None):
    proyek_id = None
    nama_proyek = "semua proyek"
    if proyek_arg:
        p = cari_proyek(args, token, proyek_arg)
        proyek_id = p["id"]
        nama_proyek = p["title"]
    tugas = ambil_tugas(args, token, filter_expr, proyek_id=proyek_id)
    tugas.sort(key=lambda t: t.get("due_date") or "9999")
    proyek_map = None
    if proyek_id is None:
        proyek_map = {p["id"]: p["title"] for p in daftar_proyek_mentah(args, token)}
    baris = [ringkas_tugas(t, args.tz, proyek_map) for t in tugas]
    teks = [judul, f"Proyek: {nama_proyek}", f"Jumlah: {len(tugas)}"]
    if catatan:
        teks.append(catatan)
    teks += baris if baris else ["(tidak ada tugas)"]
    hasil = {"teks": "\n".join(teks), "jumlah": len(tugas),
             "tugas": [{"id": t["id"], "judul": t["title"], "done": t["done"],
                        "due_date": t.get("due_date"), "priority": t.get("priority"),
                        "project_id": t.get("project_id")} for t in tugas]}
    cetak(hasil, args)
    return 0


CATATAN_TUMPANG_TINDIH = (
    "Catatan: tugas yang jatuh tempo HARI INI tapi jamnya sudah lewat muncul di sini MAUPUN di "
    "'terlambat' sekaligus (disengaja - 'hari-ini' = rentang tanggal, 'terlambat' = sudah lewat waktu "
    "sekarang). Jangan jumlahkan kedua daftar sebagai tugas unik tanpa mengecek id yang sama."
)


def cmd_hari_ini(args, token):
    now = sekarang(args.tz)
    awal = ke_iso_utc(now.date(), 0, 0, args.tz)
    akhir = ke_iso_utc(now.date() + dt.timedelta(days=1), 0, 0, args.tz)
    f = f"due_date >= {awal} && due_date < {akhir} && done = false"
    return _filter_dan_cetak(args, token, f"TUGAS HARI INI ({format_tanggal_panjang(now.date())})", f,
                              args.proyek, catatan=CATATAN_TUMPANG_TINDIH)


def cmd_terlambat(args, token):
    now = sekarang(args.tz)
    f = f"due_date < {ke_iso_utc(now.date(), now.hour, now.minute, args.tz)} && done = false"
    return _filter_dan_cetak(args, token, "TUGAS TERLAMBAT", f, args.proyek, catatan=CATATAN_TUMPANG_TINDIH)


def cmd_minggu_ini(args, token):
    now = sekarang(args.tz)
    awal = ke_iso_utc(now.date(), 0, 0, args.tz)
    akhir = ke_iso_utc(now.date() + dt.timedelta(days=7), 0, 0, args.tz)
    f = f"due_date >= {awal} && due_date < {akhir} && done = false"
    return _filter_dan_cetak(args, token, "TUGAS 7 HARI KE DEPAN", f, args.proyek)


def cmd_cari(args, token):
    proyek_id = None
    if args.proyek:
        proyek_id = cari_proyek(args, token, args.proyek)["id"]
    tugas = ambil_tugas(args, token, None, proyek_id=proyek_id, cari_teks=args.kata_kunci)
    proyek_map = {p["id"]: p["title"] for p in daftar_proyek_mentah(args, token)} if not proyek_id else None
    baris = [ringkas_tugas(t, args.tz, proyek_map) for t in tugas]
    teks = [f"HASIL CARI: {args.kata_kunci!r}", f"Jumlah: {len(tugas)}"] + (baris or ["(tidak ada hasil)"])
    cetak({"teks": "\n".join(teks), "jumlah": len(tugas),
           "tugas": [{"id": t["id"], "judul": t["title"], "done": t["done"]} for t in tugas]}, args)
    return 0


def cmd_ringkasan(args, token):
    proyek_id = cari_proyek(args, token, args.proyek)["id"] if args.proyek else None
    f = "done = false"
    if args.hanya_terlambat:
        now = sekarang(args.tz)
        f += f" && due_date < {ke_iso_utc(now.date(), now.hour, now.minute, args.tz)}"
    tugas = ambil_tugas(args, token, f, proyek_id=proyek_id)
    per_anggota = {}
    tanpa_pic = []
    for t in tugas:
        assignees = t.get("assignees") or []
        if not assignees:
            tanpa_pic.append(t)
            continue
        for a in assignees:
            per_anggota.setdefault(a.get("username", "?"), []).append(t)
    teks = ["RINGKASAN TUGAS TERBUKA" + (" (hanya terlambat)" if args.hanya_terlambat else "")]
    for nama in sorted(per_anggota):
        daftar = per_anggota[nama]
        teks.append(f"\n{nama} ({len(daftar)} tugas):")
        teks += ["  " + ringkas_tugas(t, args.tz) for t in daftar]
    if tanpa_pic:
        teks.append(f"\nBELUM ADA PIC ({len(tanpa_pic)} tugas):")
        teks += ["  " + ringkas_tugas(t, args.tz) for t in tanpa_pic]
    if not tugas:
        teks.append("(tidak ada tugas terbuka)")
    cetak({"teks": "\n".join(teks),
           "per_anggota": {k: len(v) for k, v in per_anggota.items()},
           "tanpa_pic": len(tanpa_pic)}, args)
    return 0


# ============================================================ tugas: tulis


def resolve_user_id(args, token, proyek_id, username):
    qs = urllib.parse.urlencode({"s": username})
    data, _ = panggil("GET", f"/projects/{proyek_id}/projectusers?{qs}", args, token=token)
    data = data or []
    persis = [u for u in data if u.get("username", "").lower() == username.lower()]
    if persis:
        return persis[0]["id"]
    if len(data) == 1:
        return data[0]["id"]
    if not data:
        raise Gagal(
            f"Anggota '{username}' tidak ditemukan di proyek ini (atau token tidak berizin "
            f"'projects: projectusers'). Pastikan orang itu sudah ditambahkan ke tim/proyek di Vikunja.",
            K_INPUT,
        )
    opsi = ", ".join(u["username"] for u in data)
    raise Gagal(f"Nama '{username}' cocok lebih dari satu: {opsi}. Sebutkan username persis.", K_INPUT)


def _siapkan_item_tugas(args, token, item):
    """item: dict dari --judul/--proyek/... (CLI) ATAU satu baris --batch. -> (proyek, body, ringkasan_teks)"""
    judul = (item.get("judul") or "").strip()
    if not judul:
        raise Gagal("Judul tugas kosong.", K_INPUT)
    proyek_sebutan = item.get("proyek") or getattr(args, "proyek", None)
    if not proyek_sebutan:
        raise Gagal(f"Tugas {judul!r}: proyek tidak disebutkan (--proyek, atau isi field 'proyek' di --batch).", K_INPUT)
    proyek = cari_proyek(args, token, str(proyek_sebutan))
    body = {"title": judul}
    ringkasan = [f"Judul : {judul}", f"Proyek: {proyek['title']} (id {proyek['id']})"]
    tenggat = item.get("tenggat")
    if tenggat:
        iso, tgl = parse_tenggat(str(tenggat), sekarang(args.tz).date(), args.tz)
        body["due_date"] = iso
        ringkasan.append(f"Tenggat: {format_tanggal_panjang(tgl)}")
    prioritas = item.get("prioritas")
    if prioritas not in (None, ""):
        p = int(prioritas)
        if not 0 <= p <= 5:
            raise Gagal("Prioritas harus 0-5 (0=tanpa, 5=lakukan sekarang).", K_INPUT)
        body["priority"] = p
        ringkasan.append(f"Prioritas: {p} ({PRIORITAS_LABEL[p]})")
    catatan = item.get("catatan")
    if catatan:
        body["description"] = str(catatan)
        ringkasan.append(f"Catatan: {catatan}")
    ke = item.get("ke")
    if ke:
        ringkasan.append(f"Ditugaskan ke: {ke}")
    return proyek, body, ke, ringkasan


def cmd_tambah(args, token):
    if args.batch:
        try:
            with open(args.batch, encoding="utf-8") as f:
                daftar_item = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise Gagal(f"Tidak bisa membaca --batch {args.batch}: {e}", K_FILE)
        if not isinstance(daftar_item, list) or not daftar_item:
            raise Gagal("--batch harus berisi daftar (list) tugas JSON, minimal satu.", K_INPUT)
    else:
        if not args.judul:
            raise Gagal("--judul wajib diisi (atau pakai --batch file.json).", K_INPUT)
        daftar_item = [{
            "judul": args.judul, "proyek": args.proyek, "tenggat": args.tenggat,
            "prioritas": args.prioritas, "catatan": args.catatan, "ke": args.ke,
        }]

    disiapkan = [_siapkan_item_tugas(args, token, it) for it in daftar_item]  # validasi semua dulu

    teks_pratinjau = ["PRATINJAU TAMBAH TUGAS" if len(disiapkan) == 1 else
                      f"PRATINJAU TAMBAH {len(disiapkan)} TUGAS"]
    for i, (_, _, _, ringkasan) in enumerate(disiapkan, 1):
        teks_pratinjau.append(f"{i}.")
        teks_pratinjau += ["   " + b for b in ringkasan]
    if not args.ya:
        teks_pratinjau.append("\nBelum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan ke Vikunja.")
        cetak({"teks": "\n".join(teks_pratinjau), "disimpan": False,
               "jumlah": len(disiapkan)}, args)
        return 0

    dibuat = []
    for idx, (proyek, body, ke, ringkasan) in enumerate(disiapkan, 1):
        try:
            data, _ = panggil("PUT", f"/projects/{proyek['id']}/tasks", args, token=token, body=body, tulis=True)
        except Gagal as e:
            e.args = (f"Tugas ke-{idx} ({body['title']!r}) GAGAL disimpan: {e}. "
                      f"{len(dibuat)} tugas sebelumnya SUDAH tersimpan (lihat di bawah); "
                      f"sisanya tidak dicoba lagi.",)
            for d in dibuat:
                sys.stderr.write(f"  sudah tersimpan: #{d['id']} {d['title']}\n")
            raise
        dibuat.append(data)
        if ke:
            try:
                uid = resolve_user_id(args, token, proyek["id"], ke)
                panggil("PUT", f"/tasks/{data['id']}/assignees", args, token=token,
                        body={"user_id": uid}, tulis=True)
                ringkasan.append("-> berhasil ditugaskan")
            except Gagal as e:
                petunjuk = ""
                if e.kode == K_AUTH:
                    petunjuk = (
                        " KEMUNGKINAN BESAR PENYEBAB: token belum dicentang izin grup 'Tasks Assignees' "
                        "(Create + Read All) - ini GRUP TERPISAH dari grup 'Tasks', letaknya di bagian "
                        "sendiri di layar buat token dan mudah terlewat. Buka Settings > API Tokens, "
                        "edit/buat ulang token, cek grup 'Tasks Assignees' (bukan 'Tasks'), lihat "
                        "docs/panduan-vikunja.md bagian 6."
                    )
                sys.stderr.write(
                    f"CATATAN: tugas #{data['id']} tersimpan, tapi GAGAL menugaskan ke '{ke}': {e}.{petunjuk}\n"
                )

    teks = [f"TERSIMPAN {len(dibuat)} TUGAS DI VIKUNJA:"]
    for d in dibuat:
        teks.append(f"- #{d['id']} {d['title']} (proyek id {d['project_id']})")
    cetak({"teks": "\n".join(teks), "disimpan": True,
           "tugas": [{"id": d["id"], "judul": d["title"], "project_id": d["project_id"]} for d in dibuat]}, args)
    return 0


def cmd_selesai(args, token):
    data, _ = panggil("GET", f"/tasks/{args.id}", args, token=token)
    if data.get("done"):
        cetak({"teks": f"Tugas #{args.id} ({data['title']}) memang sudah SELESAI sebelumnya.",
               "disimpan": False, "sudah_selesai": True}, args)
        return 0
    teks = [f"PRATINJAU TANDAI SELESAI: #{args.id} {data['title']}"]
    if not args.ya:
        teks.append("Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan.")
        cetak({"teks": "\n".join(teks), "disimpan": False}, args)
        return 0
    hasil, _ = panggil("POST", f"/tasks/{args.id}", args, token=token, body={"done": True}, tulis=True)
    cetak({"teks": f"SELESAI: #{args.id} {hasil['title']} ditandai selesai di Vikunja.",
           "disimpan": True}, args)
    return 0


# ============================================================ dari-teks (draf, tanpa menulis ke Vikunja)

_POLA_BULLET = re.compile(r"^\s*(?:[-*•]|\d{1,2}[.)])\s+(.*\S)\s*$")
_POLA_PIC = re.compile(r"^([A-Za-z][A-Za-z .]{1,29}?)\s*[:\-–]\s+(.+)$")
_POLA_MENDESAK = re.compile(r"\b(mendesak|urgent|penting|segera|asap)\b", re.IGNORECASE)
_BUKAN_NAMA = {"pic", "catatan", "note", "todo", "tugas", "deadline", "tenggat", "prioritas", "urgent"}


def urai_dari_teks(teks, acuan, anggota_dikenal=None):
    draf, diabaikan = [], 0
    for baris in teks.splitlines():
        m = _POLA_BULLET.match(baris)
        if not m:
            if baris.strip():
                diabaikan += 1
            continue
        isi = m.group(1)
        pic = None
        m2 = _POLA_PIC.match(isi)
        if m2:
            kandidat, sisa = m2.group(1).strip(), m2.group(2).strip()
            kata = kandidat.split()
            cocok_dikenal = anggota_dikenal and kandidat.lower() in {a.lower() for a in anggota_dikenal}
            bukan_nama = kandidat.lower() in _BUKAN_NAMA
            if not bukan_nama and (cocok_dikenal or (1 <= len(kata) <= 3 and all(w[0:1].isupper() for w in kata))):
                pic, isi = kandidat, sisa
        tenggat = cocok_tanggal_kata(isi, acuan)
        prioritas = 4 if _POLA_MENDESAK.search(isi) else None
        draf.append({
            "judul": isi,
            "proyek": None,
            "ke": pic,
            "tenggat": tenggat.isoformat() if tenggat else None,
            "prioritas": prioritas,
            "catatan": None,
            "baris_asal": baris.strip(),
            "_dugaan": True,
        })
    return draf, diabaikan


def cmd_dari_teks(args, token):
    if args.file:
        teks = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    elif args.teks:
        teks = args.teks
    else:
        raise Gagal("Isi teks lewat --teks \"...\", --file <path>, atau --file - (dari stdin).", K_INPUT)
    anggota = [a.strip() for a in args.anggota.split(",")] if args.anggota else None
    draf, diabaikan = urai_dari_teks(teks, sekarang(args.tz).date(), anggota)
    if not draf:
        raise Gagal(
            "Tidak ada baris yang dikenali sebagai tugas. Tulis tiap tugas sebagai baris berawalan "
            "'-', '*', atau '1.'.",
            K_INPUT,
        )
    keluaran = args.keluaran or f"draf-tugas-{sekarang(args.tz).strftime('%Y%m%d-%H%M%S')}.json"
    with open(keluaran, "w", encoding="utf-8") as f:
        json.dump(draf, f, ensure_ascii=False, indent=2)
    teks_out = [f"DRAF {len(draf)} TUGAS (BELUM masuk Vikunja) -> disimpan di: {keluaran}"]
    for i, d in enumerate(draf, 1):
        ket = []
        if d["ke"]:
            ket.append(f"PIC: {d['ke']}")
        if d["tenggat"]:
            ket.append(f"tenggat: {d['tenggat']}")
        if d["prioritas"]:
            ket.append("mendesak")
        teks_out.append(f"{i}. {d['judul']}" + (f" ({'; '.join(ket)})" if ket else ""))
    if diabaikan:
        teks_out.append(f"({diabaikan} baris lain diabaikan — bukan baris berawalan '-'/'*'/angka.)")
    teks_out.append(
        "\nPERIKSA dulu tiap baris (field 'ke' & 'tenggat' hanya TEBAKAN dari kata-kata di teks; "
        "'proyek' masih kosong). Edit file itu bila perlu, isi 'proyek' pada tiap baris ATAU pakai "
        "--proyek di bawah sebagai proyek default untuk baris yang belum diisi, lalu jalankan:\n"
        f"  python3 vikunja.py tambah --batch {keluaran} --proyek <id-atau-nama> --ya"
    )
    cetak({"teks": "\n".join(teks_out), "draf": draf, "diabaikan": diabaikan, "file": keluaran}, args)
    return 0


# ============================================================ cek


def cmd_cek(args):
    teks = ["CEK VIKUNJA", f"Alamat: {args.url}"]
    try:
        info = info_server(args)
    except Gagal as e:
        teks.append(f"TIDAK BISA DIHUBUNGI: {e}")
        cetak({"teks": "\n".join(teks), "terhubung": False}, args)
        return e.kode
    versi = info.get("version", "?")
    teks.append(f"Versi server: {versi}" + ("" if versi in VIKUNJA_TERUJI else " (belum diuji Komunitech)"))
    token = ambil_token(args)
    teks.append(f"Token: {tampilkan_token_tersamar(token)}")
    izin = {}
    for nama, path in (("projects:read_all", "/projects"), ("tasks:read_all", "/tasks")):
        try:
            panggil("GET", path, args, token=token)
            izin[nama] = True
        except Gagal as e:
            izin[nama] = False
            teks.append(f"CATATAN: izin '{nama}' TIDAK BISA DIBACA ({e})")
    teks.append("Izin baca dasar: OK" if all(izin.values()) else "Izin baca dasar: KURANG (lihat CATATAN)")
    cetak({"teks": "\n".join(teks), "terhubung": True, "versi": versi, "izin": izin}, args)
    return 0 if all(izin.values()) else K_AUTH


# ============================================================ keluaran & argparse


def cetak(hasil, args):
    if getattr(args, "json", False):
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(hasil["teks"])


def _tambah_opsi_umum(p):
    p.add_argument("--url", default=os.environ.get("VIKUNJA_URL", URL_DEFAULT))
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--izinkan-jarak-jauh", dest="izinkan_jarak_jauh", action="store_true")
    p.add_argument("--tz", default="WIB", choices=list(TZ_OFFSET))
    p.add_argument("--json", action="store_true")
    p.add_argument("--timeout", type=float, default=15.0, help="Batas waktu tunggu jawaban Vikunja (detik)")


def buat_parser():
    ap = argparse.ArgumentParser(prog="vikunja.py", description="Asisten tugas/proyek Vikunja (Komunitech)")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p = sub.add_parser("simpan-kunci")
    p.add_argument("--kunci-file", dest="kunci_file", default=None)
    p.add_argument("--ya", action="store_true")

    for nama in ("cek", "daftar-proyek"):
        p = sub.add_parser(nama)
        _tambah_opsi_umum(p)

    for nama in ("hari-ini", "terlambat", "minggu-ini"):
        p = sub.add_parser(nama)
        _tambah_opsi_umum(p)
        p.add_argument("--proyek", default=None)

    p = sub.add_parser("cari")
    _tambah_opsi_umum(p)
    p.add_argument("kata_kunci")
    p.add_argument("--proyek", default=None)

    p = sub.add_parser("ringkasan")
    _tambah_opsi_umum(p)
    p.add_argument("--proyek", default=None)
    p.add_argument("--hanya-terlambat", dest="hanya_terlambat", action="store_true")

    p = sub.add_parser("tambah")
    _tambah_opsi_umum(p)
    p.add_argument("--judul", default=None)
    p.add_argument("--proyek", default=None)
    p.add_argument("--tenggat", default=None)
    p.add_argument("--prioritas", type=int, default=None)
    p.add_argument("--catatan", default=None)
    p.add_argument("--ke", default=None)
    p.add_argument("--batch", default=None)
    p.add_argument("--ya", action="store_true")

    p = sub.add_parser("selesai")
    _tambah_opsi_umum(p)
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--ya", action="store_true")

    p = sub.add_parser("dari-teks")
    _tambah_opsi_umum(p)
    p.add_argument("--teks", default=None)
    p.add_argument("--file", default=None)
    p.add_argument("--keluaran", default=None)
    p.add_argument("--anggota", default=None, help="Daftar nama tim dipisah koma, mis. 'Budi,Siti,Andi'")

    return ap


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        if args.perintah == "simpan-kunci":
            return simpan_kunci(args)
        if args.perintah == "cek":
            return cmd_cek(args)
        if args.perintah == "dari-teks":
            return cmd_dari_teks(args, None)
        token = ambil_token(args)
        if args.perintah == "daftar-proyek":
            return cmd_daftar_proyek(args, token)
        if args.perintah == "hari-ini":
            return cmd_hari_ini(args, token)
        if args.perintah == "terlambat":
            return cmd_terlambat(args, token)
        if args.perintah == "minggu-ini":
            return cmd_minggu_ini(args, token)
        if args.perintah == "cari":
            return cmd_cari(args, token)
        if args.perintah == "ringkasan":
            return cmd_ringkasan(args, token)
        if args.perintah == "tambah":
            return cmd_tambah(args, token)
        if args.perintah == "selesai":
            return cmd_selesai(args, token)
        raise Gagal(f"Perintah tidak dikenal: {args.perintah}", K_INPUT)
    except Gagal as e:
        sys.stderr.write(f"GALAT: {e}\n")
        return e.kode


if __name__ == "__main__":
    sys.exit(main())
